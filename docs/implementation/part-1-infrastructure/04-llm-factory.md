# Part 1 — `src/config/llm_factory.py`

## 1. Purpose & Context

**Epic:** EP-01 — US-01-01

**Architectural design:** The factory is the single seam that selects a concrete `BaseChatModel` implementation. All pipeline nodes depend only on `LLMProtocol` (see `04b-llm-client.md`) — they never import a provider class directly. Provider selection is fully automatic: `detect_provider()` infers the backend from the model name string alone, so switching providers requires only a settings change — no code edits anywhere.

**Multi-provider support:** The factory now supports four backends through a unified `make_llm()` builder:

| Provider | Detection rule | LangChain class |
|---|---|---|
| `openrouter` | model name contains `"/"` | `ChatOpenAI` (OpenRouter base URL) |
| `openai` | starts with `gpt-`, `o1-`, `o2-`, `o3-`, `o4-`, or `text-` | `ChatOpenAI` (OpenAI base URL) |
| `anthropic` | starts with `claude-` | `ChatAnthropic` |
| `lmstudio` | everything else | `ChatOpenAI` (LM Studio base URL) |

Three distinct LLM roles exist because they use different temperatures and model slugs:

| Factory | Model setting | Temperature | Used by |
|---|---|---|---|
| `get_reasoning_llm()` | `llm_model_reasoning` | `temperature_reasoning` (default `0.0`) | Mapping, Cypher Gen, ER judge, Critic, Grader, Enrichment |
| `get_extraction_llm()` | `llm_model_extraction` | `temperature_extraction` (default `0.0`) | Triplet Extractor; LM Studio path disables thinking for JSON output |
| `get_generation_llm()` | `llm_model_reasoning` | `temperature_generation` (default `0.3`) | Answer Generator |

---

## 2. Prerequisites

- `settings.py` complete (step 2) — including `openrouter_api_key`, `openrouter_base_url`, `llm_max_tokens_reasoning`
- `llm_client.py` complete (step 4b) — `InstrumentedLLM`, `LLMProtocol`

---

## 3. Public API

| Symbol | Returns | Description |
|---|---|---|
| `detect_provider(model)` | `str` | Infer provider name from model string |
| `make_llm(model, temperature, max_tokens, role, ...)` | `LLMProtocol` | Build and wrap a provider-specific LLM |
| `get_reasoning_llm()` | `LLMProtocol` | Cached deterministic LLM for reasoning tasks |
| `get_extraction_llm()` | `LLMProtocol` | Cached SLM for JSON-mode extraction |
| `get_generation_llm()` | `LLMProtocol` | Cached LLM with T=0.3 for answer generation |
| `reconfigure_from_env()` | `None` | Clear LRU caches and reload settings (notebook use) |

`get_reasoning_llm()`, `get_extraction_llm()`, and `get_generation_llm()` are `@lru_cache(maxsize=8)` — calling them multiple times returns the same `InstrumentedLLM` instance until `reconfigure_from_env()` is called.

> **Design note:** All getter functions call `get_settings()` at invocation time rather than reading a module-level `settings` alias. This ensures they always see up-to-date configuration after `reconfigure_from_env()` clears the cache.

---

## 4. Full Implementation

```python
"""EP-01: Multi-provider LLM client factory.

Builds InstrumentedLLM-wrapped LangChain chat-model instances.
Provider is inferred automatically from the model name — no separate
provider config field is needed.

All callers import from here — no pipeline node constructs an LLM object
directly. All getter functions use get_settings() (not a module-level alias)
so reconfigure_from_env() takes effect immediately.

Supported providers (auto-detected from model name):
    openrouter : model contains "/"          → ChatOpenAI @ OpenRouter
    openai     : starts with gpt-/o1-.../text- → ChatOpenAI @ OpenAI
    anthropic  : starts with claude-         → ChatAnthropic
    lmstudio   : everything else             → ChatOpenAI @ LM Studio
"""

from __future__ import annotations

from functools import lru_cache

from langchain_anthropic import ChatAnthropic
from langchain_openai import ChatOpenAI

from src.config.llm_client import InstrumentedLLM, LLMProtocol
from src.config.settings import get_settings, reload_settings


_OPENAI_PREFIXES = ("gpt-", "o1-", "o2-", "o3-", "o4-", "text-")


def detect_provider(model: str) -> str:
    """Infer provider from model name — no config field required.

    Rules (evaluated in order):
        1. model contains "/"         → "openrouter"
        2. starts with gpt-/o*-/text- → "openai"
        3. starts with "claude-"      → "anthropic"
        4. anything else              → "lmstudio"

    Args:
        model: Model identifier string (e.g. ``"meta-llama/llama-3-8b-instruct"``).

    Returns:
        One of ``"openrouter"``, ``"openai"``, ``"anthropic"``, ``"lmstudio"``.
    """
    if "/" in model:
        return "openrouter"
    if model.startswith(_OPENAI_PREFIXES):
        return "openai"
    if model.startswith("claude-"):
        return "anthropic"
    return "lmstudio"


def make_llm(
    model: str,
    temperature: float,
    max_tokens: int,
    role: str,
) -> LLMProtocol:
    """Build a provider-appropriate LLM and wrap it in InstrumentedLLM.

    Provider is auto-detected via ``detect_provider(model)``.  All settings
    are read fresh from ``get_settings()`` so the result reflects the current
    environment (important after ``reconfigure_from_env()``).

    Args:
        model:       Model identifier string passed to the provider.
        temperature: Sampling temperature (0.0 = deterministic).
        max_tokens:  Maximum combined thinking + output token budget.
                     Critical for OpenRouter models with mandatory thinking
                     (e.g. ``gpt-oss-120b``) — caps the total budget.
        role:        Human-readable role label attached to ``InstrumentedLLM``
                     (e.g. ``"reasoning"``, ``"extraction"``, ``"generation"``).

    Returns:
        ``InstrumentedLLM``-wrapped chat model satisfying ``LLMProtocol``.
    """
    settings = get_settings()
    provider = detect_provider(model)

    if provider == "openrouter":
        llm = ChatOpenAI(
            model=model,
            temperature=temperature,
            max_tokens=max_tokens,
            base_url=settings.openrouter_base_url,
            api_key=settings.openrouter_api_key.get_secret_value(),
        )
    elif provider == "openai":
        llm = ChatOpenAI(
            model=model,
            temperature=temperature,
            max_tokens=max_tokens,
            api_key=settings.openai_api_key.get_secret_value(),
        )
    elif provider == "anthropic":
        llm = ChatAnthropic(
            model=model,
            temperature=temperature,
            max_tokens=max_tokens,
            api_key=settings.anthropic_api_key.get_secret_value(),
        )
    else:  # lmstudio
        llm = ChatOpenAI(
            model=model,
            temperature=temperature,
            max_tokens=max_tokens,
            base_url=settings.lmstudio_base_url,
            api_key="lm-studio",
        )

    return InstrumentedLLM(llm, role=role)


@lru_cache(maxsize=8)
def get_reasoning_llm() -> LLMProtocol:
    """Return a cached LLM for reasoning tasks (mapping, Cypher, grading).

    Provider is auto-detected from ``settings.llm_model_reasoning``.
    Cache is cleared by ``reconfigure_from_env()``.
    """
    settings = get_settings()
    return make_llm(
        model=settings.llm_model_reasoning,
        temperature=settings.llm_temperature_reasoning,
        max_tokens=settings.llm_max_tokens_reasoning,
        role="reasoning",
    )


@lru_cache(maxsize=8)
def get_extraction_llm() -> LLMProtocol:
    """Return a cached SLM for JSON-mode extraction.

    If the detected provider is ``openrouter``, delegates to ``make_llm()``.
    Otherwise uses the LM Studio path with thinking explicitly disabled
    (``extra_body={"enable_thinking": False}``) — necessary for Qwen3-style
    thinking models to emit plain JSON instead of chain-of-thought output.

    Cache is cleared by ``reconfigure_from_env()``.
    """
    settings = get_settings()
    model = settings.llm_model_extraction
    provider = detect_provider(model)

    if provider == "openrouter":
        return make_llm(
            model=model,
            temperature=settings.llm_temperature_extraction,
            max_tokens=settings.llm_max_tokens_extraction,
            role="extraction",
        )

    # LM Studio path — disable thinking mode for reliable JSON output
    llm = ChatOpenAI(
        model=model,
        temperature=settings.llm_temperature_extraction,
        max_tokens=settings.llm_max_tokens_extraction,
        base_url=settings.lmstudio_base_url,
        api_key="lm-studio",
        extra_body={"enable_thinking": False},
    )
    return InstrumentedLLM(llm, role="extraction")


@lru_cache(maxsize=8)
def get_generation_llm() -> LLMProtocol:
    """Return a cached LLM for natural-language answer generation.

    Uses the reasoning model at a higher temperature (``temperature_generation``,
    default 0.3) for greater fluency.  Provider is auto-detected.
    Cache is cleared by ``reconfigure_from_env()``.
    """
    settings = get_settings()
    return make_llm(
        model=settings.llm_model_reasoning,
        temperature=settings.llm_temperature_generation,
        max_tokens=settings.llm_max_tokens_reasoning,
        role="generation",
    )


def reconfigure_from_env() -> None:
    """Clear all LRU caches and reload settings from the current environment.

    Call this in notebooks after mutating ``os.environ`` to switch models or
    providers without restarting the kernel:

    .. code-block:: python

        import os
        os.environ["LLM_MODEL_REASONING"] = "claude-sonnet-4-5"
        from src.config.llm_factory import reconfigure_from_env
        reconfigure_from_env()
        # get_reasoning_llm() now returns a ChatAnthropic instance

    Implementation: calls ``reload_settings()`` (which mutates the module-level
    ``settings`` alias in-place) then clears the three getter caches so the next
    call rebuilds LLM instances from the updated config.
    """
    reload_settings()
    get_reasoning_llm.cache_clear()
    get_extraction_llm.cache_clear()
    get_generation_llm.cache_clear()
```

### Key Design Decisions

| Decision | Rationale |
|---|---|
| Provider detection from model name | Eliminates a redundant `PROVIDER=` env var. The model slug already encodes the provider (e.g. `meta-llama/...` → OpenRouter, `claude-*` → Anthropic). |
| `get_settings()` inside each getter | Module-level `settings` alias is frozen at import time. Calling `get_settings()` at invocation time picks up the fresh instance created by `reload_settings()`. |
| LM Studio `enable_thinking: False` | LM Studio's `/chat/completions` API passes `extra_body` to the model's chat template. Qwen3-style models emit reasoning tokens by default; disabling this is required for deterministic JSON output. |
| `max_tokens` caps total budget | OpenRouter models with mandatory thinking (e.g. `gpt-oss-120b`) consume tokens for both the chain-of-thought and the final response. Setting `max_tokens` explicitly prevents silent truncation of the output. |
| `@lru_cache(maxsize=8)` | Raised from `maxsize=1` to accommodate concurrent notebook experiments with multiple configurations in the same process. |

---

## 5. Tests

```python
"""Unit tests for src/config/llm_factory.py"""

from unittest.mock import MagicMock, patch

import pytest

from src.config.llm_factory import (
    detect_provider,
    get_extraction_llm,
    get_generation_llm,
    get_reasoning_llm,
    reconfigure_from_env,
)


class TestDetectProvider:
    def test_slash_in_model_is_openrouter(self) -> None:
        assert detect_provider("meta-llama/llama-3-8b-instruct") == "openrouter"

    def test_gpt_prefix_is_openai(self) -> None:
        assert detect_provider("gpt-4o") == "openai"

    def test_o1_prefix_is_openai(self) -> None:
        assert detect_provider("o1-preview") == "openai"

    def test_claude_prefix_is_anthropic(self) -> None:
        assert detect_provider("claude-sonnet-4-5") == "anthropic"

    def test_unknown_is_lmstudio(self) -> None:
        assert detect_provider("qwen3-14b") == "lmstudio"
        assert detect_provider("local-model") == "lmstudio"

    def test_text_prefix_is_openai(self) -> None:
        assert detect_provider("text-embedding-3-small") == "openai"


class TestGettersReturnLLMProtocol:
    def test_reasoning_llm_is_instrumented(self) -> None:
        from src.config.llm_client import InstrumentedLLM
        llm = get_reasoning_llm()
        assert isinstance(llm, InstrumentedLLM)

    def test_extraction_llm_is_instrumented(self) -> None:
        from src.config.llm_client import InstrumentedLLM
        llm = get_extraction_llm()
        assert isinstance(llm, InstrumentedLLM)

    def test_generation_llm_is_instrumented(self) -> None:
        from src.config.llm_client import InstrumentedLLM
        llm = get_generation_llm()
        assert isinstance(llm, InstrumentedLLM)

    def test_singleton_same_object(self) -> None:
        assert get_reasoning_llm() is get_reasoning_llm()

    def test_reconfigure_clears_cache(self) -> None:
        llm_before = get_reasoning_llm()
        reconfigure_from_env()
        llm_after = get_reasoning_llm()
        # After cache clear a new instance is built (different object)
        assert llm_before is not llm_after
```

---

## 6. Smoke Test

```bash
python -c "
from src.config.llm_factory import detect_provider, get_reasoning_llm, reconfigure_from_env

# Provider detection
assert detect_provider('gpt-4o') == 'openai'
assert detect_provider('claude-sonnet-4-5') == 'anthropic'
assert detect_provider('meta-llama/llama-3-8b') == 'openrouter'
assert detect_provider('local-model') == 'lmstudio'
print('detect_provider OK')

# Singleton and reconfigure
r1 = get_reasoning_llm()
r2 = get_reasoning_llm()
assert r1 is r2, 'Not a singleton before reconfigure'
reconfigure_from_env()
r3 = get_reasoning_llm()
assert r1 is not r3, 'Cache not cleared by reconfigure_from_env'
print('reconfigure_from_env OK')
print('LLM factory smoke test passed.')
"
```
