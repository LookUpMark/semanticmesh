# Part 1 — `src/config/llm_factory.py`

## 1. Purpose & Context

**Epic:** EP-01 — US-01-01

**Architectural design:** The factory is the single seam that selects a concrete `BaseChatModel` implementation. All pipeline nodes depend only on `LLMProtocol` (see `04b-llm-client.md`) — they never import a provider class directly. Swapping from `ChatOpenRouter` to `ChatOpenAI`, `ChatAnthropic`, `ChatOllama`, or any other LangChain chat-model requires changing one import line and one constructor call here, with zero changes elsewhere.

**Thesis constraint (zero budget, no local GPU):** All three factories return `InstrumentedLLM`-wrapped `ChatOpenRouter` instances backed by OpenRouter Free Tier. `ChatOpenRouter` (from `langchain-openrouter`) reads `OPENROUTER_API_KEY` from the environment automatically — no `base_url` wiring required.

Three distinct LLM roles exist because they use different temperatures and model slugs:

| Factory | Model setting | Temperature | Used by |
|---|---|---|---|
| `get_reasoning_llm()` | `llm_model_reasoning` (`qwen/qwen3-coder:free`) | `0.0` | Mapping, Cypher Gen, ER judge, Critic, Grader, Enrichment |
| `get_extraction_llm()` | `llm_model_extraction` (`qwen/qwen3-next-80b-a3b-instruct:free`) | `0.0` | Triplet Extractor (SLM — replaces NuExtract) |
| `get_generation_llm()` | `llm_model_reasoning` (`qwen/qwen3-coder:free`) | `0.3` | Answer Generator |

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

Builds InstrumentedLLM-wrapped ChatOpenRouter instances from settings.
All callers import from here — no pipeline node constructs an LLM object directly.

Architecture: replace `ChatOpenRouter` with any LangChain BaseChatModel subclass
(ChatOpenAI, ChatAnthropic, ChatOllama, ChatHuggingFace, …) to switch provider.
Only this file changes — all pipeline nodes depend on LLMProtocol.

Thesis: ChatOpenRouter @ OpenRouter Free Tier.  OPENROUTER_API_KEY must be set.
"""

from __future__ import annotations

from functools import lru_cache

from langchain_openrouter import ChatOpenRouter

from src.config.llm_client import InstrumentedLLM, LLMProtocol
from src.config.settings import settings


@lru_cache(maxsize=1)
def get_reasoning_llm() -> LLMProtocol:
    """Return a cached LLM for reasoning tasks (mapping, Cypher, grading).

    Thesis   : ChatOpenRouter @ qwen/qwen3-coder:free, T=0.0
    Swap to  : ChatOpenAI(model="gpt-4o") | ChatAnthropic(model="claude-3-5-sonnet-20241022")
    """
    return InstrumentedLLM(
        ChatOpenRouter(
            model=settings.llm_model_reasoning,
            temperature=settings.llm_temperature_reasoning,
        ),
        name="reasoning",
        max_retries=settings.max_llm_retries,
    )


@lru_cache(maxsize=1)
def get_extraction_llm() -> LLMProtocol:
    """Return a cached SLM for JSON-mode extraction.

    Thesis   : ChatOpenRouter @ qwen/qwen3-next-80b-a3b-instruct:free, T=0.0
    Originally designed for NuExtract (local GPU); any instruction-tuned
    model with JSON-mode support is a valid drop-in.
    """
    return InstrumentedLLM(
        ChatOpenRouter(
            model=settings.llm_model_extraction,
            temperature=settings.llm_temperature_extraction,
        ),
        name="extraction",
        max_retries=settings.max_llm_retries,
    )


@lru_cache(maxsize=1)
def get_generation_llm() -> LLMProtocol:
    """Return a cached LLM for natural-language answer generation.

    Thesis   : ChatOpenRouter @ qwen/qwen3-coder:free, T=0.3
    Same model as reasoning but higher temperature for fluency.
    """
    return InstrumentedLLM(
        ChatOpenRouter(
            model=settings.llm_model_reasoning,
            temperature=settings.llm_temperature_generation,
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
