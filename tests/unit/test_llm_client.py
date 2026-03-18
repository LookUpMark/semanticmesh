"""Unit tests for src/config/llm_client.py — UT-04b"""

from __future__ import annotations

import asyncio
import logging
from unittest.mock import AsyncMock, MagicMock

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
        inner.invoke.assert_called_once_with(
            [],
        )
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
        result = asyncio.run(llm.ainvoke([]))
        assert result.content == "ok"

    def test_async_passes_kwargs(self) -> None:
        inner = _make_inner()
        llm = InstrumentedLLM(inner, name="test")
        asyncio.run(llm.ainvoke([], stop=["\n"]))
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
        inner = _make_inner(_make_response(tokens=42))
        llm = InstrumentedLLM(inner, name="reasoning")
        with caplog.at_level(logging.INFO, logger="llm.reasoning"):
            llm.invoke([])
        assert any("input_tokens=42" in r.message for r in caplog.records)

    def test_repr_contains_name(self) -> None:
        inner = _make_inner()
        llm = InstrumentedLLM(inner, name="extraction")
        assert "extraction" in repr(llm)
