"""Provider-agnostic LLM interface.

EP-01: Defines:
  - LLMProtocol  — structural typing.Protocol; any BaseChatModel satisfies it.
  - InstrumentedLLM — proxy wrapper that adds retry, latency logging, and
    token-usage logging around any BaseChatModel instance.

Usage::

    # In tests — mock the narrowest possible interface
    llm = MagicMock(spec=LLMProtocol)

    # In production — wrap the concrete provider
    from langchain_openrouter import ChatOpenRouter
    llm = InstrumentedLLM(ChatOpenRouter(model="qwen/qwen3-coder:free"), name="reasoning")
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
                self._name, self._max_retries, exc,
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
                self._name, self._max_retries, exc,
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
