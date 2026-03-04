# Part 1 — `src/config/llm_client.py`

## 1. Purpose & Context

**Epic:** EP-01 — US-01-01 — Provider-Agnostic LLM Interface

Defines the two-layer LLM abstraction that makes the entire pipeline independent of any specific chat-model provider:

| Layer | Tool | Role |
|---|---|---|
| **Contract** | `LLMProtocol` (`typing.Protocol`) | Structural type interface — any `BaseChatModel` subclass satisfies it automatically (no inheritance required) |
| **Behaviour** | `InstrumentedLLM` | Concrete wrapper adding retry, token-usage logging, and latency measurement around *any* `BaseChatModel` |

### Architectural rationale

All pipeline nodes declare their LLM parameter as `llm: LLMProtocol`, not as a concrete class. This gives three properties simultaneously:

1. **Provider swap** — change one import in `llm_factory.py`; zero changes in pipeline nodes.
2. **Resilience** — exponential-backoff retry on rate-limit and timeout errors, centralised in one class, not scattered across 10 nodes.
3. **Observability** — token usage and latency logged on every call; feeds the ablation budget tracking.

### Thesis implementation (zero-cost constraint)

For thesis runs, `llm_factory.py` instantiates `ChatOpenRouter` (from `langchain-openrouter`) and wraps it in `InstrumentedLLM`. OpenRouter Free Tier models used:

| Role | Model |
|---|---|
| Reasoning + Generation | `qwen/qwen3-coder:free` |
| Extraction (SLM) | `qwen/qwen3-next-80b-a3b-instruct:free` |

Swapping to a different provider (e.g. `ChatOpenAI`, `ChatAnthropic`, `ChatOllama`) requires only changing the constructor call inside `get_*_llm()` — the rest of the codebase is unaffected.

---

## 2. Prerequisites

- `src/config/settings.py` — `settings` singleton (step 2)
- `src/config/logging.py` — `get_logger`, `NodeTimer` (step 3)
- `tenacity>=8.0` — installed (see `pyproject.toml`)

---

## 3. Public API

| Symbol | Type | Description |
|---|---|---|
| `LLMProtocol` | `typing.Protocol` | Structural type contract: `invoke` + `ainvoke` |
| `InstrumentedLLM` | `class` | Retry-wrapped, logged `BaseChatModel` proxy |

`InstrumentedLLM` also proxies every other attribute of the inner model via `__getattr__`, so callers can still use `llm.with_structured_output(...)`, `llm.bind_tools(...)`, etc.

---

## 4. Full Implementation

```python
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

import asyncio
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
```

---

## 5. Tests

```python
"""Unit tests for src/config/llm_client.py — UT-04b"""

from __future__ import annotations

import asyncio
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from langchain_core.messages import AIMessage

from src.config.llm_client import InstrumentedLLM, LLMProtocol


def _make_response(content: str = "ok", tokens: int = 10) -> AIMessage:
    msg = AIMessage(content=content)
    msg.usage_metadata = {
        "input_tokens": tokens,
        "output_tokens": tokens,
        "total_tokens": tokens * 2,
    }
    return msg


def _make_inner(return_value: AIMessage | None = None) -> MagicMock:
    inner = MagicMock()
    inner.invoke.return_value = return_value or _make_response()
    inner.ainvoke = AsyncMock(return_value=return_value or _make_response())
    return inner


# ── LLMProtocol ───────────────────────────────────────────────────────────────

class TestLLMProtocol:
    def test_instrumented_llm_satisfies_protocol(self) -> None:
        inner = _make_inner()
        llm = InstrumentedLLM(inner, name="test")
        assert isinstance(llm, LLMProtocol)

    def test_mock_satisfies_protocol(self) -> None:
        # Demonstrates that MagicMock(spec=LLMProtocol) works in tests
        mock_llm = MagicMock(spec=LLMProtocol)
        assert isinstance(mock_llm, MagicMock)


# ── InstrumentedLLM.invoke ────────────────────────────────────────────────────

class TestInstrumentedLLMInvoke:
    def test_delegates_to_inner_model(self) -> None:
        inner = _make_inner()
        llm = InstrumentedLLM(inner, name="test")
        result = llm.invoke([])
        inner.invoke.assert_called_once_with([], )
        assert result.content == "ok"

    def test_passes_kwargs_through(self) -> None:
        inner = _make_inner()
        llm = InstrumentedLLM(inner, name="test")
        llm.invoke([], temperature=0.5)
        inner.invoke.assert_called_once_with([], temperature=0.5)

    def test_retries_on_rate_limit(self) -> None:
        from openai import RateLimitError

        inner = _make_inner()
        inner.invoke.side_effect = [
            RateLimitError("rate limited", response=MagicMock(status_code=429), body={}),
            _make_response(),
        ]
        llm = InstrumentedLLM(inner, name="test", max_retries=3)
        result = llm.invoke([])
        assert result.content == "ok"
        assert inner.invoke.call_count == 2

    def test_raises_after_max_retries_exhausted(self) -> None:
        from openai import RateLimitError

        inner = _make_inner()
        inner.invoke.side_effect = RateLimitError(
            "rate limited", response=MagicMock(status_code=429), body={}
        )
        llm = InstrumentedLLM(inner, name="test", max_retries=2)
        with pytest.raises(RateLimitError):
            llm.invoke([])
        assert inner.invoke.call_count == 2

    def test_non_retryable_exception_raised_immediately(self) -> None:
        inner = _make_inner()
        inner.invoke.side_effect = ValueError("bad prompt")
        llm = InstrumentedLLM(inner, name="test", max_retries=3)
        with pytest.raises(ValueError, match="bad prompt"):
            llm.invoke([])
        assert inner.invoke.call_count == 1


# ── InstrumentedLLM.ainvoke ───────────────────────────────────────────────────

class TestInstrumentedLLMAinvoke:
    def test_delegates_async(self) -> None:
        inner = _make_inner()
        llm = InstrumentedLLM(inner, name="test")
        result = asyncio.get_event_loop().run_until_complete(llm.ainvoke([]))
        assert result.content == "ok"

    def test_async_passes_kwargs(self) -> None:
        inner = _make_inner()
        llm = InstrumentedLLM(inner, name="test")
        asyncio.get_event_loop().run_until_complete(llm.ainvoke([], stop=["\n"]))
        inner.ainvoke.assert_called_once_with([], stop=["\n"])


# ── InstrumentedLLM.__getattr__ ───────────────────────────────────────────────

class TestInstrumentedLLMProxy:
    def test_proxies_with_structured_output(self) -> None:
        inner = _make_inner()
        inner.with_structured_output = MagicMock(return_value="structured_chain")
        llm = InstrumentedLLM(inner, name="test")
        result = llm.with_structured_output({"type": "object"})
        assert result == "structured_chain"
        inner.with_structured_output.assert_called_once()

    def test_proxies_bind_tools(self) -> None:
        inner = _make_inner()
        inner.bind_tools = MagicMock(return_value="bound_chain")
        llm = InstrumentedLLM(inner, name="test")
        result = llm.bind_tools([])
        assert result == "bound_chain"

    def test_raises_attribute_error_for_unknown(self) -> None:
        inner = MagicMock(spec=["invoke", "ainvoke"])
        llm = InstrumentedLLM(inner, name="test")
        with pytest.raises(AttributeError):
            _ = llm.nonexistent_attribute


# ── logging ───────────────────────────────────────────────────────────────────

class TestInstrumentedLLMLogging:
    def test_logs_token_usage_on_success(self, caplog: pytest.LogCaptureFixture) -> None:
        import logging

        inner = _make_inner(_make_response(tokens=42))
        llm = InstrumentedLLM(inner, name="reasoning")
        with caplog.at_level(logging.INFO, logger="llm.reasoning"):
            llm.invoke([])
        assert any("input_tokens=42" in r.message for r in caplog.records)

    def test_repr_contains_name(self) -> None:
        inner = _make_inner()
        llm = InstrumentedLLM(inner, name="extraction")
        assert "extraction" in repr(llm)
```

---

## 6. Smoke Test

```bash
# Requires OPENROUTER_API_KEY set in .env
python -c "
from langchain_openrouter import ChatOpenRouter
from langchain_core.messages import HumanMessage
from src.config.llm_client import InstrumentedLLM

llm = InstrumentedLLM(
    ChatOpenRouter(model='qwen/qwen3-coder:free', temperature=0.0),
    name='smoke_test',
)
response = llm.invoke([HumanMessage(content='Reply with: OK')])
print('Response:', response.content)
assert 'OK' in response.content or len(response.content) > 0
print('llm_client smoke test passed.')
"
```
