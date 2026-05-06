"""Unit tests for src/config/llm_factory.py — UT-04"""

from __future__ import annotations

import os

import pytest

from src.config.llm_client import InstrumentedLLM, LLMProtocol
from src.config.llm_factory import (
    get_extraction_llm,
    get_generation_llm,
    get_reasoning_llm,
)


@pytest.fixture(autouse=True)
def set_openrouter_api_key() -> None:
    """Set OPENROUTER_API_KEY for all tests in this module.

    ChatOpenRouter requires this environment variable to be set for
    Pydantic validation. The actual value doesn't matter for unit tests
    since we're not making real API calls.
    """
    os.environ["OPENROUTER_API_KEY"] = "test_key_for_unit_tests"


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
        # Reasoning models (gpt-5*, o-series) don't support temperature → None
        temp = llm._model.temperature  # type: ignore[attr-defined]
        assert temp is None or temp == 0.0

    def test_generation_llm_temperature(self) -> None:
        llm = get_generation_llm()
        # Reasoning models ignore temperature; standard models use 0.3
        temp = llm._model.temperature  # type: ignore[attr-defined]
        assert temp is None or temp == 0.3

    def test_extraction_llm_temperature(self) -> None:
        llm = get_extraction_llm()
        # Reasoning models (gpt-5*) don't support temperature → None
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
