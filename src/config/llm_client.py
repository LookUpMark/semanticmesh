"""Provider-agnostic LLM interface.

EP-01: Defines:
  - LLMProtocol  — structural typing.Protocol; any BaseChatModel satisfies it.
  - InstrumentedLLM — proxy wrapper that adds retry, latency logging, and
    token-usage logging around any BaseChatModel instance.
  - FallbackLLM — wrapper that automatically switches from free to paid models
    on rate limit errors (HTTP 429).

Usage::

    # In tests — mock the narrowest possible interface
    llm = MagicMock(spec=LLMProtocol)

    # In production — wrap the concrete provider
    from langchain_openrouter import ChatOpenRouter
    llm = InstrumentedLLM(ChatOpenRouter(model="qwen/qwen3-coder:free"), name="reasoning")

    # With automatic free→paid fallback on rate limits
    llm = FallbackLLM(
        primary=ChatOpenRouter(model="openai/gpt-oss-120b:free"),
        fallback=ChatOpenRouter(model="openai/gpt-oss-120b"),
        name="reasoning"
    )
"""

from __future__ import annotations

import logging
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

# ── Exceptions that warrant a retry ──────────────────────────────────────────
# Covers RateLimitError (HTTP 429) and timeout from any OpenAI-compatible endpoint.

try:
    from openai import APITimeoutError, RateLimitError

    _RETRYABLE: tuple[type[Exception], ...] = (RateLimitError, APITimeoutError)
except ImportError:  # openai package not installed
    _RETRYABLE = (Exception,)  # fallback: retry on any error


# ── LLMProtocol ───────────────────────────────────────────────────────────────


@runtime_checkable
class LLMProtocol(Protocol):
    """Structural protocol satisfied by any LangChain BaseChatModel subclass.

    Pipeline nodes annotate their LLM parameter as ``llm: LLMProtocol``.
    This keeps them decoupled from any concrete provider class.

    All ``BaseChatModel`` subclasses (ChatOpenRouter, ChatOpenAI, ChatOllama,
    ChatAnthropic, ChatHuggingFace, …) satisfy this protocol implicitly.
    ``InstrumentedLLM`` also satisfies it explicitly.
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
    """Proxy wrapper that adds retry, latency logging, and token-usage logging.

    Delegates every attribute not explicitly overridden to the inner
    ``BaseChatModel`` instance via ``__getattr__``, so callers can still use
    ``llm.with_structured_output(...)``, ``llm.bind_tools(...)``, etc.

    Args:
        model:       Any ``BaseChatModel`` instance (e.g. ``ChatOpenRouter``).
        name:        Logical role name for logging (``"reasoning"``, ``"extraction"``,
                     ``"generation"``).
        max_retries: Maximum retry attempts on retryable errors (default from settings).
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
        # unreachable — satisfies type checker
        raise RuntimeError("Unreachable")  # pragma: no cover

    # ── async invoke ──────────────────────────────────────────────────────────

    async def ainvoke(
        self,
        input: list[BaseMessage] | str,
        **kwargs: Any,
    ) -> AIMessage:
        """Asynchronous invoke with retry and structured logging."""
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
        """Delegate every other attribute to the inner model.

        This allows callers to use ``llm.with_structured_output(...)``,
        ``llm.bind_tools(...)``, ``llm.stream(...)``, etc. without any
        explicit forwarding code in this wrapper.
        """
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

    def __repr__(self) -> str:
        return f"InstrumentedLLM(name={self._name!r}, model={self._model!r})"


# ── FallbackLLM ─────────────────────────────────────────────────────────────


class FallbackLLM:
    """LLM wrapper that automatically falls back to a paid model on rate limits.

    When the primary (free) model hits rate limit errors (HTTP 429), this wrapper
    immediately switches to the fallback (paid) model for the current request
    and all subsequent requests. This provides seamless free→paid fallback without
    manual intervention.

    Unlike InstrumentedLLM which retries on rate limits, FallbackLLM switches
    to the paid model immediately on the first rate limit error, avoiding
    the delays associated with waiting for free tier rate limits to reset.

    Args:
        primary:     The primary (usually free) BaseChatModel to use.
        fallback:    The fallback (paid) BaseChatModel to use when rate limits are hit.
        name:        Logical role name for logging.

    Example:
        Create a free→paid fallback pair:
        >>> free_model = ChatOpenRouter(model="openai/gpt-oss-120b:free")
        >>> paid_model = ChatOpenRouter(model="openai/gpt-oss-120b")
        >>> llm = FallbackLLM(free_model, paid_model, name="reasoning")
        >>> # First call uses free model
        >>> response = llm.invoke("Hello")
        >>> # If rate limit is hit, immediately switches to paid model
    """

    _RATE_LIMIT_ERRORS: tuple[type[Exception], ...] = _RETRYABLE

    def __init__(
        self,
        primary: BaseChatModel,
        fallback: BaseChatModel,
        *,
        name: str,
    ) -> None:
        self._primary = primary  # Raw BaseChatModel, not InstrumentedLLM
        self._fallback = fallback  # Raw BaseChatModel, not InstrumentedLLM
        self._name = name
        self._using_fallback = False
        self._logger: logging.Logger = get_logger(f"llm.{name}")

    def __getattr__(self, item: str) -> Any:
        # Delegate attribute access to the currently active model (primary or fallback)
        return getattr(self._get_current_model(), item)

    @property
    def temperature(self) -> float:
        return getattr(self._get_current_model(), "temperature")

    @property
    def model(self) -> str:
        return getattr(self._get_current_model(), "model")

    def _should_use_fallback(self) -> bool:
        """Check if we should use the fallback model based on past rate limits."""
        return self._using_fallback

    def _get_current_model(self) -> BaseChatModel:
        """Get the current active model (primary or fallback)."""
        return self._fallback if self._should_use_fallback() else self._primary

    def invoke(
        self,
        input: list[BaseMessage] | str,
        **kwargs: Any,
    ) -> AIMessage:
        """Invoke with immediate free→paid fallback on rate limit.

        Strategy:
        1. Try primary (free) model ONCE (no retries on rate limit)
        2. If rate limit is hit, immediately switch to fallback (paid)
        3. Once switched, all future calls use the fallback model
        4. Non-rate-limit errors are still raised normally
        """
        # If already using fallback, just call it directly
        if self._using_fallback:
            return self._invoke_with_logging(self._fallback, input, **kwargs)

        # Try primary model
        try:
            with NodeTimer() as t:
                response = self._primary.invoke(input, **kwargs)
            self._log_call(response, model="primary", elapsed_ms=t.elapsed_ms, attempt=1)
            return response
        except Exception as exc:
            if self._is_rate_limit_error(exc):
                # Switch to fallback immediately
                self._logger.warning(
                    "Rate limit hit on primary model, switching to fallback for all future calls"
                )
                self._using_fallback = True
                return self._invoke_with_logging(self._fallback, input, **kwargs)
            # For non-rate-limit errors, re-raise
            raise

    def _invoke_with_logging(
        self,
        model: BaseChatModel,
        input: list[BaseMessage] | str,
        **kwargs: Any,
    ) -> AIMessage:
        """Invoke with logging (used after switching to fallback or for direct calls)."""
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
        """Async invoke with logging."""
        start = time.perf_counter()
        response = await model.ainvoke(input, **kwargs)
        elapsed_ms = (time.perf_counter() - start) * 1000
        model_name = "fallback" if model is self._fallback else "primary"
        self._log_call(response, model=model_name, elapsed_ms=elapsed_ms, attempt=1)
        return response

    def _is_rate_limit_error(self, exc: Exception) -> bool:
        """Check if an exception is a rate limit error."""
        # Direct rate limit error
        if isinstance(exc, self._RATE_LIMIT_ERRORS):
            return True
        # Check for error message containing rate limit indicators
        exc_str = str(exc).lower()
        if "rate limit" in exc_str or "429" in exc_str:
            return True
        return False

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

    def __getattr__(self, item: str) -> Any:
        """Delegate attributes to the current active model."""
        return getattr(self._get_current_model(), item)

    def __repr__(self) -> str:
        mode = "fallback" if self._using_fallback else "primary"
        return f"FallbackLLM(name={self._name!r}, mode={mode!r})"
