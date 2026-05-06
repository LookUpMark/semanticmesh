"""Unit tests for src.config.provider_detection."""

from __future__ import annotations

import os
from unittest.mock import patch

import pytest

from src.config.provider_detection import (
    _is_free_model,
    _strip_free_suffix,
    detect_provider,
    is_openai_reasoning_model,
)


class TestDetectProvider:
    """Test detect_provider routing rules."""

    @pytest.mark.parametrize(
        "model,expected",
        [
            ("ollama/llama3.1", "ollama"),
            ("groq/llama3-70b-8192", "groq"),
            ("bedrock/anthropic.claude-3-sonnet", "bedrock"),
            ("google/gemini-2.0-flash", "google"),
            ("vertex_ai/gemini-pro", "google"),
            ("azure/gpt-4o", "azure"),
            ("azure_openai/gpt-4o", "azure"),
            ("nvidia/llama-3.1-70b", "nvidia"),
            ("deepseek/deepseek-coder", "deepseek"),
            ("xai/grok-2", "xai"),
            ("cohere/command-r-plus", "cohere"),
            ("together/meta-llama/Llama-3", "together"),
            ("hf/meta-llama/llama-3", "huggingface"),
            ("huggingface/meta-llama/llama-3", "huggingface"),
            ("mistral/mistral-large", "mistral"),
            ("openrouter/openai/gpt-4o", "openrouter"),
            ("lmstudio/some-model", "lmstudio"),
        ],
    )
    def test_named_prefix_routing(self, model: str, expected: str) -> None:
        with patch.dict(os.environ, {"LLM_PROVIDER": "auto"}):
            assert detect_provider(model) == expected

    @pytest.mark.parametrize(
        "model",
        [
            "openai/gpt-4.1:free",
            "meta-llama/llama-3.3-70b-instruct:free",
            "anthropic/claude-3.5-sonnet",
        ],
    )
    def test_slash_without_named_prefix_routes_to_openrouter(self, model: str) -> None:
        with patch.dict(os.environ, {"LLM_PROVIDER": "auto"}):
            assert detect_provider(model) == "openrouter"

    @pytest.mark.parametrize(
        "model",
        ["gpt-4.1", "gpt-5-nano-2025-08-07", "o3-mini", "o4-mini", "text-embedding-3-large"],
    )
    def test_bare_openai_prefixes(self, model: str) -> None:
        with patch.dict(os.environ, {"LLM_PROVIDER": "auto"}):
            assert detect_provider(model) == "openai"

    @pytest.mark.parametrize("model", ["claude-3.5-sonnet", "claude-4-opus"])
    def test_bare_anthropic_prefix(self, model: str) -> None:
        with patch.dict(os.environ, {"LLM_PROVIDER": "auto"}):
            assert detect_provider(model) == "anthropic"

    @pytest.mark.parametrize(
        "model,expected",
        [
            ("gemini-2.0-flash", "google"),
            ("mistral-large-latest", "mistral"),
            ("command-r-plus", "cohere"),
            ("deepseek-chat", "deepseek"),
            ("grok-2", "xai"),
        ],
    )
    def test_bare_provider_prefixes(self, model: str, expected: str) -> None:
        with patch.dict(os.environ, {"LLM_PROVIDER": "auto"}):
            assert detect_provider(model) == expected

    def test_fallback_to_lmstudio(self) -> None:
        with patch.dict(os.environ, {"LLM_PROVIDER": "auto"}):
            assert detect_provider("my-local-model") == "lmstudio"

    def test_global_override_applies(self) -> None:
        with patch.dict(os.environ, {"LLM_PROVIDER": "openrouter"}):
            assert detect_provider("gpt-4.1") == "openrouter"

    def test_named_prefix_wins_over_global_override(self) -> None:
        with patch.dict(os.environ, {"LLM_PROVIDER": "openrouter"}):
            assert detect_provider("ollama/llama3") == "ollama"


class TestIsOpenaiReasoningModel:
    @pytest.mark.parametrize(
        "model",
        ["o1-preview", "o3-mini", "o4-mini", "gpt-5-nano-2025-08-07", "gpt-5.4-mini"],
    )
    def test_reasoning_models(self, model: str) -> None:
        assert is_openai_reasoning_model(model) is True

    @pytest.mark.parametrize("model", ["gpt-4o-mini", "gpt-4.1", "claude-3.5-sonnet"])
    def test_non_reasoning_models(self, model: str) -> None:
        assert is_openai_reasoning_model(model) is False


class TestFreeSuffix:
    def test_strip_free_suffix(self) -> None:
        assert _strip_free_suffix("openai/gpt-oss-120b:free") == "openai/gpt-oss-120b"
        assert _strip_free_suffix("openai/gpt-4o") == "openai/gpt-4o"

    def test_is_free_model(self) -> None:
        assert _is_free_model("meta-llama/llama-3.3:free") is True
        assert _is_free_model("gpt-4.1") is False
