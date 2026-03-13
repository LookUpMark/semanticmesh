# Part 1 — `src/config/llm_factory.py`

## 1. Purpose & Context

**Epic:** EP-01 — US-01-01

**Architectural design:** The factory is the single seam that selects a concrete `BaseChatModel` implementation. All pipeline nodes depend only on `LLMProtocol` (see `04b-llm-client.md`) — they never import a provider class directly. Swapping from `ChatOpenAI` to `ChatOpenRouter`, `ChatAnthropic`, `ChatOllama`, or any other LangChain chat-model requires changing one import line and one constructor call here, with zero changes elsewhere.

**Thesis constraint:** All three factories return `InstrumentedLLM`-wrapped `ChatOpenAI` instances pointed at a local LM Studio endpoint (OpenAI-compatible API). `ChatOpenAI` (from `langchain-openai`) connects to the URL configured in `LMSTUDIO_BASE_URL` (default: `http://localhost:1234/v1`). The API key is the literal string `"lm-studio"` — LM Studio ignores authentication.

Three distinct LLM roles exist because they use different temperatures and model slugs:

| Factory | Model setting | Temperature | Used by |
|---|---|---|---|
| `get_reasoning_llm()` | `llm_model_reasoning` (`"local-model"`, override via `LLM_MODEL_REASONING`) | `0.0` | Mapping, Cypher Gen, ER judge, Critic, Grader, Enrichment |
| `get_extraction_llm()` | `llm_model_extraction` (`"local-model"`, override via `LLM_MODEL_EXTRACTION`) | `0.0` | Triplet Extractor (SLM); `max_tokens=16384` to prevent JSON truncation; `enable_thinking=False` disables chain-of-thought on Qwen3-style thinking models |
| `get_generation_llm()` | `llm_model_reasoning` (`"local-model"`, override via `LLM_MODEL_REASONING`) | `0.3` | Answer Generator |

---

## 2. Prerequisites

- `settings.py` complete (step 2)
- `llm_client.py` complete (step 4b) — `InstrumentedLLM`, `LLMProtocol`

---

## 3. Public API

| Function | Returns | Description |
|---|---|---|
| `get_reasoning_llm()` | `LLMProtocol` | Deterministic LLM for reasoning tasks |
| `get_extraction_llm()` | `LLMProtocol` | SLM for JSON-mode extraction |
| `get_generation_llm()` | `LLMProtocol` | LLM with T=0.3 for answer generation |

All three are `@lru_cache(maxsize=1)` — calling them multiple times returns the same `InstrumentedLLM` object.

---

## 4. Full Implementation

```python
"""EP-01: LLM client factory.

Builds InstrumentedLLM-wrapped ChatOpenAI instances pointed at a local
LM Studio endpoint (OpenAI-compatible API).
All callers import from here — no pipeline node constructs an LLM object directly.

Architecture: replace `ChatOpenAI` with any LangChain BaseChatModel subclass
(ChatOpenRouter, ChatAnthropic, ChatOllama, …) to switch provider.
Only this file changes — all pipeline nodes depend on LLMProtocol.

Thesis: ChatOpenAI → LM Studio @ http://localhost:1234/v1 (local model).
Set LMSTUDIO_BASE_URL, LLM_MODEL_REASONING, LLM_MODEL_EXTRACTION via env/.env
to customise the endpoint and model names.
"""

from __future__ import annotations

from functools import lru_cache
from typing import TYPE_CHECKING

from langchain_openai import ChatOpenAI

from src.config.llm_client import InstrumentedLLM, LLMProtocol
from src.config.settings import settings

if TYPE_CHECKING:
    from langchain_core.embeddings import Embeddings


@lru_cache(maxsize=1)
def get_reasoning_llm() -> LLMProtocol:
    """Return a cached LLM for reasoning tasks (mapping, Cypher, grading).

    Thesis   : ChatOpenAI → LM Studio, T=0.0
    Swap to  : ChatOpenRouter | ChatAnthropic | ChatOllama
    """
    return InstrumentedLLM(
        ChatOpenAI(
            model=settings.llm_model_reasoning,
            temperature=settings.llm_temperature_reasoning,
            base_url=settings.lmstudio_base_url,
            api_key="lm-studio",  # LM Studio ignores auth; any non-empty string works
        ),
        name="reasoning",
        max_retries=settings.max_llm_retries,
    )


@lru_cache(maxsize=1)
def get_extraction_llm() -> LLMProtocol:
    """Return a cached SLM for JSON-mode extraction.

    Thesis   : ChatOpenAI → LM Studio, T=0.0, max_tokens=16384
    Originally designed for NuExtract (local GPU); any instruction-tuned
    model with JSON-mode support is a valid drop-in.

    Note: ``max_tokens`` is set high (16k) to prevent JSON truncation.
    ``chat_template_kwargs: {enable_thinking: false}`` disables chain-of-thought
    on Qwen3-style thinking models in LM Studio; silently ignored by non-thinking models.
    """
    return InstrumentedLLM(
        ChatOpenAI(
            model=settings.llm_model_extraction,
            temperature=settings.llm_temperature_extraction,
            max_tokens=settings.llm_max_tokens_extraction,
            base_url=settings.lmstudio_base_url,
            api_key="lm-studio",
            model_kwargs={"extra_body": {"chat_template_kwargs": {"enable_thinking": False}}},
        ),
        name="extraction",
        max_retries=settings.max_llm_retries,
    )


@lru_cache(maxsize=1)
def get_generation_llm() -> LLMProtocol:
    """Return a cached LLM for natural-language answer generation.

    Thesis   : ChatOpenAI → LM Studio, T=0.3
    Same model as reasoning but higher temperature for fluency.
    """
    return InstrumentedLLM(
        ChatOpenAI(
            model=settings.llm_model_reasoning,
            temperature=settings.llm_temperature_generation,
            base_url=settings.lmstudio_base_url,
            api_key="lm-studio",
        ),
        name="generation",
        max_retries=settings.max_llm_retries,
    )
```

---

## 5. Tests

```python
"""Unit tests for src/config/llm_factory.py"""

from src.config.llm_client import InstrumentedLLM, LLMProtocol
from src.config.llm_factory import (
    get_extraction_llm,
    get_generation_llm,
    get_reasoning_llm,
)


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
        assert llm._model.temperature == 0.0

    def test_generation_llm_temperature(self) -> None:
        llm = get_generation_llm()
        assert llm._model.temperature == 0.3

    def test_extraction_llm_temperature(self) -> None:
        llm = get_extraction_llm()
        assert llm._model.temperature == 0.0

    def test_reasoning_and_generation_same_model_slug(self) -> None:
        r = get_reasoning_llm()
        g = get_generation_llm()
        assert r._model.model == g._model.model

    def test_singleton_same_object(self) -> None:
        llm1 = get_reasoning_llm()
        llm2 = get_reasoning_llm()
        assert llm1 is llm2
```

---

## 6. Smoke Test

```bash
python -c "
from src.config.llm_factory import get_reasoning_llm, get_extraction_llm, get_generation_llm
r = get_reasoning_llm()
e = get_extraction_llm()
g = get_generation_llm()
print(f'Reasoning T={r.temperature}, Extraction T={e.temperature}, Generation T={g.temperature}')
assert r is get_reasoning_llm(), 'Not a singleton!'
print('LLM factory OK')
"
```

Expected: `Reasoning T=0.0, Extraction T=0.0, Generation T=0.3` then `LLM factory OK`
