# Part 1 — `src/config/llm_factory.py`

## 1. Purpose & Context

**Epic:** EP-01 — US-01-01

Provides three cached factory functions that build `ChatOpenAI` instances sourced entirely from `settings`. All pipeline nodes import from here — no node constructs an LLM object directly. This enforces the invariant that model names and temperatures are always from the environment.

Three distinct LLM roles exist because they use different temperatures:

| Factory | Model setting | Temperature | Used by |
|---|---|---|---|
| `get_reasoning_llm()` | `llm_model_reasoning` | `0.0` | Mapping, Cypher Gen, ER judge, Critic, Grader, Enrichment |
| `get_extraction_llm()` | `llm_model_extraction` | `0.0` | Triplet Extractor (SLM) |
| `get_generation_llm()` | `llm_model_reasoning` | `0.3` | Answer Generator |

---

## 2. Prerequisites

- `settings.py` complete (step 2)

---

## 3. Public API

| Function | Returns | Description |
|---|---|---|
| `get_reasoning_llm()` | `ChatOpenAI` | Deterministic LLM for reasoning tasks |
| `get_extraction_llm()` | `ChatOpenAI` | SLM for JSON-mode extraction |
| `get_generation_llm()` | `ChatOpenAI` | LLM with T=0.3 for answer generation |

All three are `@lru_cache(maxsize=1)` — calling them multiple times returns the same object.

---

## 4. Full Implementation

```python
"""EP-01: LLM client factory.

Builds `ChatOpenAI` instances from `settings`. All callers should use these
factories rather than constructing LLM objects directly so that model names,
base_url, and temperatures are always sourced from the environment.
"""

from __future__ import annotations

from functools import lru_cache

from langchain_openai import ChatOpenAI

from src.config.settings import settings


@lru_cache(maxsize=1)
def get_reasoning_llm() -> ChatOpenAI:
    """Return a cached ChatOpenAI for reasoning tasks (mapping, Cypher, grading).

    Model      : settings.llm_model_reasoning  (e.g. 'qwen2.5-coder:32b')
    Temperature: 0.0 — deterministic, structured output
    """
    return ChatOpenAI(
        model=settings.llm_model_reasoning,
        base_url=settings.llm_base_url,
        api_key=settings.llm_api_key.get_secret_value(),
        temperature=settings.llm_temperature_reasoning,
    )


@lru_cache(maxsize=1)
def get_extraction_llm() -> ChatOpenAI:
    """Return a cached ChatOpenAI for SLM extraction tasks.

    Model      : settings.llm_model_extraction  (e.g. 'nuextract')
    Temperature: 0.0 — deterministic JSON-mode output
    """
    return ChatOpenAI(
        model=settings.llm_model_extraction,
        base_url=settings.llm_base_url,
        api_key=settings.llm_api_key.get_secret_value(),
        temperature=settings.llm_temperature_extraction,
    )


@lru_cache(maxsize=1)
def get_generation_llm() -> ChatOpenAI:
    """Return a cached ChatOpenAI for natural-language answer generation.

    Model      : settings.llm_model_reasoning  (same model, higher temperature)
    Temperature: 0.3 — slight creativity for fluent user-facing answers
    """
    return ChatOpenAI(
        model=settings.llm_model_reasoning,
        base_url=settings.llm_base_url,
        api_key=settings.llm_api_key.get_secret_value(),
        temperature=settings.llm_temperature_generation,
    )
```

---

## 5. Tests

**File:** `tests/unit/test_settings.py` (add to existing file, or create a separate `test_llm_factory.py`)

```python
"""Unit tests for src/config/llm_factory.py"""

from unittest.mock import patch

from langchain_openai import ChatOpenAI

from src.config.llm_factory import (
    get_extraction_llm,
    get_generation_llm,
    get_reasoning_llm,
)


class TestLlmFactory:
    def test_get_reasoning_llm_returns_chat_openai(self) -> None:
        llm = get_reasoning_llm()
        assert isinstance(llm, ChatOpenAI)

    def test_get_extraction_llm_returns_chat_openai(self) -> None:
        llm = get_extraction_llm()
        assert isinstance(llm, ChatOpenAI)

    def test_get_generation_llm_returns_chat_openai(self) -> None:
        llm = get_generation_llm()
        assert isinstance(llm, ChatOpenAI)

    def test_reasoning_llm_temperature(self) -> None:
        llm = get_reasoning_llm()
        assert llm.temperature == 0.0

    def test_generation_llm_temperature(self) -> None:
        llm = get_generation_llm()
        assert llm.temperature == 0.3

    def test_extraction_llm_temperature(self) -> None:
        llm = get_extraction_llm()
        assert llm.temperature == 0.0

    def test_reasoning_and_generation_same_model(self) -> None:
        # Both use llm_model_reasoning but different temperatures
        r = get_reasoning_llm()
        g = get_generation_llm()
        assert r.model_name == g.model_name

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
