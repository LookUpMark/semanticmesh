"""Unit tests for src/config/llm_factory.py — UT-04"""

from __future__ import annotations

import os
from unittest.mock import patch

import pytest

from src.config.llm_client import InstrumentedLLM, LLMProtocol
from src.config.llm_factory import (
    _build_effort_kwargs,
    _resolve_provider,
    get_extraction_llm,
    get_generation_llm,
    get_reasoning_llm,
)


@pytest.fixture(autouse=True)
def set_openrouter_api_key() -> None:
    """Set OPENROUTER_API_KEY for all tests in this module."""
    os.environ["OPENROUTER_API_KEY"] = "test_key_for_unit_tests"


class TestResolveProvider:
    def test_explicit_tier_provider_wins(self) -> None:
        assert _resolve_provider("openai", "ollama/llama3") == "openai"

    def test_global_override_when_tier_empty(self) -> None:
        with patch.dict(os.environ, {"LLM_PROVIDER": "openrouter"}):
            from src.config.settings import reload_settings

            reload_settings()
            assert _resolve_provider("", "gpt-4.1") == "openrouter"

    def test_auto_detection_when_both_empty(self) -> None:
        with patch.dict(os.environ, {"LLM_PROVIDER": "auto"}):
            from src.config.settings import reload_settings

            reload_settings()
            assert _resolve_provider("", "ollama/llama3") == "ollama"

    def test_empty_string_tier_falls_through(self) -> None:
        with patch.dict(os.environ, {"LLM_PROVIDER": "auto"}):
            from src.config.settings import reload_settings

            reload_settings()
            assert _resolve_provider("", "gpt-4.1") == "openai"


class TestBuildEffortKwargs:
    def test_openai_effort(self) -> None:
        assert _build_effort_kwargs("high", "openai") == {"reasoning_effort": "high"}

    def test_openrouter_effort(self) -> None:
        assert _build_effort_kwargs("medium", "openrouter") == {"reasoning": {"effort": "medium"}}

    def test_empty_effort_returns_none(self) -> None:
        assert _build_effort_kwargs("", "openai") is None

    def test_none_effort_returns_none(self) -> None:
        assert _build_effort_kwargs("none", "openai") is None

    def test_unsupported_provider_returns_none(self) -> None:
        assert _build_effort_kwargs("high", "anthropic") is None


class TestLlmFactory:
    def test_get_reasoning_llm_satisfies_protocol(self) -> None:
        llm = get_reasoning_llm()
        assert isinstance(llm, LLMProtocol)

    def test_get_extraction_llm_satisfies_protocol(self) -> None:
        llm = get_extraction_llm()
        assert isinstance(llm, LLMProtocol)

    def test_get_generation_llm_satisfies_protocol(self) -> None:
        llm = get_generation_llm()
        assert isinstance(llm, LLMProtocol)

    def test_all_are_instrumented(self) -> None:
        assert isinstance(get_reasoning_llm(), InstrumentedLLM)
        assert isinstance(get_extraction_llm(), InstrumentedLLM)
        assert isinstance(get_generation_llm(), InstrumentedLLM)

    def test_reasoning_llm_temperature(self) -> None:
        llm = get_reasoning_llm()
        temp = llm._model.temperature  # type: ignore[attr-defined]
        assert temp is None or temp == 0.0

    def test_generation_llm_temperature(self) -> None:
        llm = get_generation_llm()
        temp = llm._model.temperature  # type: ignore[attr-defined]
        assert temp is None or temp == 0.3

    def test_extraction_llm_temperature(self) -> None:
        llm = get_extraction_llm()
        temp = llm._model.temperature  # type: ignore[attr-defined]
        assert temp is None or temp == 0.0

    def test_reasoning_and_generation_same_model_slug(self) -> None:
        r = get_reasoning_llm()
        g = get_generation_llm()
        assert r._model.model == g._model.model  # type: ignore[attr-defined]

    def test_singleton_same_object(self) -> None:
        llm1 = get_reasoning_llm()
        llm2 = get_reasoning_llm()
        assert llm1 is llm2
