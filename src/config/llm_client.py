"""Provider-agnostic LLM interface.

Defines:
  - LLMProtocol: Structural typing.Protocol for any BaseChatModel
  - InstrumentedLLM: Proxy wrapper with retry and logging
  - FallbackLLM: Automatic free→paid fallback on rate limits

Usage::
    llm = InstrumentedLLM(ChatOpenRouter(model="qwen/qwen3-coder:free"), name="reasoning")
    llm = FallbackLLM(primary=free_model, fallback=paid_model, name="reasoning")
"""

from __future__ import annotations

import logging
import threading
import time
from typing import Any, Protocol, runtime_checkable

from langchain_core.language_models import BaseChatModel
from langchain_core.messages import AIMessage, BaseMessage
from tenacity import (
    AsyncRetrying,
    RetryError,
    Retrying,
    before_sleep_log,
    retry_if_exception_type,
    stop_after_attempt,
    wait_exponential,
)

from src.config.logging import NodeTimer, get_logger

logger: logging.Logger = get_logger(__name__)


# ── Global LLM Usage Tracker ─────────────────────────────────────────────────

_usage_lock = threading.Lock()
_usage_counters: dict[str, dict[str, int]] = {}
# Structure: {"reasoning": {"input_tokens": N, "output_tokens": N, "calls": N}, ...}


def _record_usage(tier: str, input_tokens: int, output_tokens: int) -> None:
    """Record token usage for a given tier (thread-safe)."""
    with _usage_lock:
        if tier not in _usage_counters:
            _usage_counters[tier] = {"input_tokens": 0, "output_tokens": 0, "calls": 0}
        _usage_counters[tier]["input_tokens"] += input_tokens
        _usage_counters[tier]["output_tokens"] += output_tokens
        _usage_counters[tier]["calls"] += 1


def get_llm_usage_summary() -> dict[str, dict[str, int]]:
    """Return cumulative LLM usage per tier since last reset.

    Returns:
        Dict mapping tier name to {"input_tokens", "output_tokens", "calls"}.
    """
    with _usage_lock:
        return {k: dict(v) for k, v in _usage_counters.items()}


def reset_llm_usage() -> None:
    """Reset all usage counters (call before a new pipeline run)."""
    with _usage_lock:
        _usage_counters.clear()


# ── Exceptions that warrant a retry ──────────────────────────────────────────

try:
    from openai import APITimeoutError, RateLimitError

    _RETRYABLE: tuple[type[Exception], ...] = (RateLimitError, APITimeoutError)
except ImportError:
    _RETRYABLE = (Exception,)


# ── LLMProtocol ───────────────────────────────────────────────────────────────


@runtime_checkable
class LLMProtocol(Protocol):
    """Structural protocol for any LangChain BaseChatModel subclass.

    All BaseChatModel subclasses satisfy this protocol implicitly.
    Pipeline nodes use this to stay decoupled from concrete providers.
    """

    def invoke(
        self,
        input: list[BaseMessage] | str,
        **kwargs: Any,
    ) -> AIMessage:
        """Synchronous single-turn invocation."""
        ...

    async def ainvoke(
        self,
        input: list[BaseMessage] | str,
        **kwargs: Any,
    ) -> AIMessage:
        """Asynchronous single-turn invocation."""
        ...


# ── InstrumentedLLM ───────────────────────────────────────────────────────────


class InstrumentedLLM:
    """Proxy wrapper with retry, latency logging, and token-usage logging.

    Delegates undefined attributes to the inner BaseChatModel via __getattr__.

    Args:
        model: Any BaseChatModel instance (e.g., ChatOpenRouter).
        name: Logical role name for logging ("reasoning", "extraction", "generation").
        max_retries: Maximum retry attempts on retryable errors.
    """

    def __init__(
        self,
        model: BaseChatModel,
        *,
        name: str,
        max_retries: int = 3,
    ) -> None:
        self._model = model
        self._name = name
        self._max_retries = max_retries
        self._logger: logging.Logger = get_logger(f"llm.{name}")

    # ── sync invoke ───────────────────────────────────────────────────────────

    def invoke(
        self,
        input: list[BaseMessage] | str,
        **kwargs: Any,
    ) -> AIMessage:
        """Invoke the model with retry and structured logging."""
        kwargs = self._inject_observability_callbacks(kwargs)
        attempt = 0
        try:
            for attempt_ctx in Retrying(
                retry=retry_if_exception_type(_RETRYABLE),
                wait=wait_exponential(multiplier=1, min=2, max=30),
                stop=stop_after_attempt(self._max_retries),
                before_sleep=before_sleep_log(self._logger, logging.WARNING),
                reraise=True,
            ):
                with attempt_ctx:
                    attempt += 1
                    with NodeTimer() as t:
                        response: AIMessage = self._model.invoke(input, **kwargs)
                    self._log_call(response, elapsed_ms=t.elapsed_ms, attempt=attempt)
                    return response
        except RetryError as exc:
            self._logger.error(
                "llm.%s invoke failed after %d attempts: %s",
                self._name,
                self._max_retries,
                exc,
            )
            raise
        raise RuntimeError("Unreachable")  # pragma: no cover

    # ── async invoke ──────────────────────────────────────────────────────────

    async def ainvoke(
        self,
        input: list[BaseMessage] | str,
        **kwargs: Any,
    ) -> AIMessage:
        """Asynchronous invoke with retry and structured logging."""
        kwargs = self._inject_observability_callbacks(kwargs)
        attempt = 0
        try:
            async for attempt_ctx in AsyncRetrying(
                retry=retry_if_exception_type(_RETRYABLE),
                wait=wait_exponential(multiplier=1, min=2, max=30),
                stop=stop_after_attempt(self._max_retries),
                before_sleep=before_sleep_log(self._logger, logging.WARNING),
                reraise=True,
            ):
                with attempt_ctx:
                    attempt += 1
                    start = time.perf_counter()
                    response = await self._model.ainvoke(input, **kwargs)
                    elapsed_ms = (time.perf_counter() - start) * 1000
                    self._log_call(response, elapsed_ms=elapsed_ms, attempt=attempt)
                    return response
        except RetryError as exc:
            self._logger.error(
                "llm.%s ainvoke failed after %d attempts: %s",
                self._name,
                self._max_retries,
                exc,
            )
            raise
        raise RuntimeError("Unreachable")  # pragma: no cover

    # ── transparent delegation ─────────────────────────────────────────────────

    def __getattr__(self, item: str) -> Any:
        """Delegate undefined attributes to the inner model."""
        return getattr(self._model, item)

    # ── internals ─────────────────────────────────────────────────────────────

    def _log_call(
        self,
        response: AIMessage,
        *,
        elapsed_ms: float,
        attempt: int,
    ) -> None:
        """Emit a structured INFO log line with token usage and latency."""
        usage = getattr(response, "usage_metadata", None) or {}
        self._logger.info(
            "llm.%s call completed | attempt=%d | latency_ms=%.1f | "
            "input_tokens=%s | output_tokens=%s | total_tokens=%s",
            self._name,
            attempt,
            elapsed_ms,
            usage.get("input_tokens", "?"),
            usage.get("output_tokens", "?"),
            usage.get("total_tokens", "?"),
        )
        # Accumulate in global tracker
        in_tok = usage.get("input_tokens", 0)
        out_tok = usage.get("output_tokens", 0)
        if isinstance(in_tok, int) and isinstance(out_tok, int):
            _record_usage(self._name, in_tok, out_tok)

    def __repr__(self) -> str:
        return f"InstrumentedLLM(name={self._name!r}, model={self._model!r})"

    def _inject_observability_callbacks(self, kwargs: dict[str, Any]) -> dict[str, Any]:
        """Merge observability callbacks into kwargs (Langfuse, etc.)."""
        from src.config.observability import get_observability_callbacks

        obs_callbacks = get_observability_callbacks()
        if not obs_callbacks:
            return kwargs

        # LangChain accepts callbacks either as top-level kwarg or inside config dict
        existing = kwargs.get("config", {}).get("callbacks", []) or kwargs.get("callbacks", [])
        merged = list(existing) + obs_callbacks

        if "config" in kwargs:
            kwargs["config"] = {**kwargs["config"], "callbacks": merged}
        else:
            kwargs["config"] = {"callbacks": merged}
        return kwargs


# ── FallbackLLM ─────────────────────────────────────────────────────────────


class FallbackLLM:
    """LLM wrapper with automatic free→paid fallback on rate limits.

    Switches to the fallback model on first rate limit error (HTTP 429),
    avoiding retry delays. Once switched, all future calls use the fallback.

    Args:
        primary: The primary (usually free) BaseChatModel.
        fallback: The fallback (paid) BaseChatModel.
        name: Logical role name for logging.
    """

    _RATE_LIMIT_ERRORS: tuple[type[Exception], ...] = _RETRYABLE

    def __init__(
        self,
        primary: BaseChatModel,
        fallback: BaseChatModel,
        *,
        name: str,
    ) -> None:
        self._primary = primary
        self._fallback = fallback
        self._name = name
        self._using_fallback = False
        self._fallback_lock = threading.Lock()
        self._logger: logging.Logger = get_logger(f"llm.{name}")

    def __getattr__(self, item: str) -> Any:
        with self._fallback_lock:
            model = self._get_current_model()
        return getattr(model, item)

    @property
    def temperature(self) -> float:
        return self._get_current_model().temperature

    @property
    def model(self) -> str:
        return self._get_current_model().model

    def _should_use_fallback(self) -> bool:
        return self._using_fallback

    def _get_current_model(self) -> BaseChatModel:
        return self._fallback if self._should_use_fallback() else self._primary

    def invoke(
        self,
        input: list[BaseMessage] | str,
        **kwargs: Any,
    ) -> AIMessage:
        """Invoke with immediate free→paid fallback on rate limit."""
        with self._fallback_lock:
            if self._using_fallback:
                return self._invoke_with_logging(self._fallback, input, **kwargs)

        try:
            with NodeTimer() as t:
                response = self._primary.invoke(input, **kwargs)
            self._log_call(response, model="primary", elapsed_ms=t.elapsed_ms, attempt=1)
            return response
        except Exception as exc:
            if self._is_rate_limit_error(exc):
                self._logger.warning(
                    "Rate limit hit on primary model, switching to fallback for all future calls"
                )
                with self._fallback_lock:
                    self._using_fallback = True
                return self._invoke_with_logging(self._fallback, input, **kwargs)
            raise

    def _invoke_with_logging(
        self,
        model: BaseChatModel,
        input: list[BaseMessage] | str,
        **kwargs: Any,
    ) -> AIMessage:
        with NodeTimer() as t:
            response = model.invoke(input, **kwargs)
        model_name = "fallback" if model is self._fallback else "primary"
        self._log_call(response, model=model_name, elapsed_ms=t.elapsed_ms, attempt=1)
        return response

    async def ainvoke(
        self,
        input: list[BaseMessage] | str,
        **kwargs: Any,
    ) -> AIMessage:
        """Async invoke with immediate free→paid fallback."""
        if self._using_fallback:
            return await self._ainvoke_with_logging(self._fallback, input, **kwargs)

        try:
            start = time.perf_counter()
            response = await self._primary.ainvoke(input, **kwargs)
            elapsed_ms = (time.perf_counter() - start) * 1000
            self._log_call(response, model="primary", elapsed_ms=elapsed_ms, attempt=1)
            return response
        except Exception as exc:
            if self._is_rate_limit_error(exc):
                self._logger.warning(
                    "Rate limit hit on primary model, switching to fallback for all future calls"
                )
                self._using_fallback = True
                return await self._ainvoke_with_logging(self._fallback, input, **kwargs)
            raise

    async def _ainvoke_with_logging(
        self,
        model: BaseChatModel,
        input: list[BaseMessage] | str,
        **kwargs: Any,
    ) -> AIMessage:
        start = time.perf_counter()
        response = await model.ainvoke(input, **kwargs)
        elapsed_ms = (time.perf_counter() - start) * 1000
        model_name = "fallback" if model is self._fallback else "primary"
        self._log_call(response, model=model_name, elapsed_ms=elapsed_ms, attempt=1)
        return response

    def _is_rate_limit_error(self, exc: Exception) -> bool:
        if isinstance(exc, self._RATE_LIMIT_ERRORS):
            return True
        exc_str = str(exc).lower()
        return bool("rate limit" in exc_str or "429" in exc_str)

    def _log_call(
        self,
        response: AIMessage,
        *,
        model: str,
        elapsed_ms: float,
        attempt: int,
    ) -> None:
        """Emit a structured INFO log line with token usage and latency."""
        usage = getattr(response, "usage_metadata", None) or {}
        self._logger.info(
            "llm.%s call completed | model=%s | attempt=%d | latency_ms=%.1f | "
            "input_tokens=%s | output_tokens=%s | total_tokens=%s",
            self._name,
            model,
            attempt,
            elapsed_ms,
            usage.get("input_tokens", "?"),
            usage.get("output_tokens", "?"),
            usage.get("total_tokens", "?"),
        )
        # Accumulate in global tracker
        in_tok = usage.get("input_tokens", 0)
        out_tok = usage.get("output_tokens", 0)
        if isinstance(in_tok, int) and isinstance(out_tok, int):
            _record_usage(self._name, in_tok, out_tok)

    def __repr__(self) -> str:
        mode = "fallback" if self._using_fallback else "primary"
        return f"FallbackLLM(name={self._name!r}, mode={mode!r})"
