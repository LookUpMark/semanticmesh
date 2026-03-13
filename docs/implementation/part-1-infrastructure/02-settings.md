# Part 1 — `src/config/settings.py`

## 1. Purpose & Context

**Epic:** EP-01 — US-01-02 — Settings & Secret Management

Loads every configurable parameter from environment variables / `.env` file. Provides a module-level singleton `settings` so all other modules import config in one line. Uses `pydantic-settings` for automatic env-var parsing, type coercion, and validation.

**Architectural capability:** Only model *identifiers* and *thresholds* live here. The concrete `BaseChatModel` subclass — `ChatOpenRouter`, `ChatOpenAI`, `ChatOllama`, `ChatAnthropic`, etc. — is selected inside `llm_factory.py`. Swapping provider requires changing one import and one constructor call there; `settings.py` is untouched.

**Thesis constraint:** All thesis runs use a local LM Studio endpoint (`LMSTUDIO_BASE_URL`). Set `LLM_MODEL_REASONING` and `LLM_MODEL_EXTRACTION` to the model name shown in LM Studio's model loader (default: `"local-model"`).

---

## 2. Prerequisites

- `pyproject.toml` populated (step 1)
- `.env.example` copied to `.env` and filled in

---

## 3. Public API

| Symbol | Type | Description |
|---|---|---|
| `Settings` | `BaseSettings` subclass | All config fields |
| `get_settings()` | `() -> Settings` | Cached factory (lru_cache) |
| `settings` | `Settings` | Module-level singleton |

---

## 4. Full Implementation

```python
"""EP-01: Application settings loaded from environment / .env file.

Sensitive values (API keys, passwords) are loaded from environment variables.
Non-sensitive defaults are defined in config.py and can be overridden via env vars.
"""

from __future__ import annotations

from functools import lru_cache

from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict

from src.config.config import DEFAULT_CONFIG


class Settings(BaseSettings):
    """Application settings with environment variable override support.

    Environment variables:
        NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD
        LMSTUDIO_BASE_URL (default: http://localhost:1234/v1)
        LLM_MODEL_REASONING, LLM_MODEL_EXTRACTION
        LLM_TEMPERATURE_EXTRACTION, LLM_TEMPERATURE_REASONING, LLM_TEMPERATURE_GENERATION
        LLM_MAX_TOKENS_EXTRACTION (default: 16384)
        EMBEDDING_MODEL, RERANKER_MODEL
        ER_BLOCKING_TOP_K, ER_SIMILARITY_THRESHOLD
        CONFIDENCE_THRESHOLD, MAX_REFLECTION_ATTEMPTS, MAX_CYPHER_HEALING_ATTEMPTS
        CHUNK_SIZE, CHUNK_OVERLAP
        RETRIEVAL_VECTOR_TOP_K, RETRIEVAL_BM25_TOP_K, RETRIEVAL_GRAPH_DEPTH
        FEW_SHOT_CYPHER_EXAMPLES
        ENABLE_SCHEMA_ENRICHMENT, RETRIEVAL_MODE
        ENABLE_CYPHER_HEALING, ENABLE_CRITIC_VALIDATION, ENABLE_RERANKER, ENABLE_HALLUCINATION_GRADER
        LOG_LEVEL
    """

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        secrets_dir="/run/secrets",
        extra="ignore",
    )

    # ── Neo4j ──────────────────────────────────────────────────────────────────
    neo4j_uri: str = DEFAULT_CONFIG.neo4j_uri
    neo4j_user: str = DEFAULT_CONFIG.neo4j_user
    neo4j_password: SecretStr = SecretStr("neo4j")  # Override via NEO4J_PASSWORD

    # ── LLM ─────────────────────────────────────────────────────────────────────
    lmstudio_base_url: str = DEFAULT_CONFIG.lmstudio_base_url
    openrouter_api_key: SecretStr = Field(default=SecretStr(""), env="OPENROUTER_API_KEY")
    openrouter_base_url: str = Field(default=DEFAULT_CONFIG.openrouter_base_url, env="OPENROUTER_BASE_URL")
    llm_model_reasoning: str = DEFAULT_CONFIG.llm_model_reasoning
    llm_model_extraction: str = DEFAULT_CONFIG.llm_model_extraction
    llm_temperature_extraction: float = DEFAULT_CONFIG.llm_temperature_extraction
    llm_temperature_reasoning: float = DEFAULT_CONFIG.llm_temperature_reasoning
    llm_temperature_generation: float = DEFAULT_CONFIG.llm_temperature_generation
    llm_max_tokens_extraction: int = DEFAULT_CONFIG.llm_max_tokens_extraction
    llm_max_tokens_reasoning: int = Field(default=DEFAULT_CONFIG.llm_max_tokens_reasoning, env="LLM_MAX_TOKENS_REASONING")

    # ── Embeddings & Reranking ─────────────────────────────────────────────────
    embedding_model: str = DEFAULT_CONFIG.embedding_model
    reranker_model: str = DEFAULT_CONFIG.reranker_model
    reranker_top_k: int = DEFAULT_CONFIG.reranker_top_k

    # ── Entity Resolution ──────────────────────────────────────────────────────
    er_blocking_top_k: int = DEFAULT_CONFIG.er_blocking_top_k
    er_similarity_threshold: float = DEFAULT_CONFIG.er_similarity_threshold

    # ── Confidence & Loop Guards ───────────────────────────────────────────────
    confidence_threshold: float = DEFAULT_CONFIG.confidence_threshold
    max_reflection_attempts: int = DEFAULT_CONFIG.max_reflection_attempts
    max_cypher_healing_attempts: int = DEFAULT_CONFIG.max_cypher_healing_attempts
    max_hallucination_retries: int = DEFAULT_CONFIG.max_hallucination_retries
    max_llm_retries: int = DEFAULT_CONFIG.max_llm_retries

    # ── Chunking ───────────────────────────────────────────────────────────────
    chunk_size: int = DEFAULT_CONFIG.chunk_size
    chunk_overlap: int = DEFAULT_CONFIG.chunk_overlap

    # ── Retrieval ──────────────────────────────────────────────────────────────
    retrieval_vector_top_k: int = DEFAULT_CONFIG.retrieval_vector_top_k
    retrieval_bm25_top_k: int = DEFAULT_CONFIG.retrieval_bm25_top_k
    retrieval_graph_depth: int = DEFAULT_CONFIG.retrieval_graph_depth

    # ── Few-Shot ───────────────────────────────────────────────────────────────
    few_shot_cypher_examples: int = DEFAULT_CONFIG.few_shot_cypher_examples

    # ── Ablation Flags ─────────────────────────────────────────────────────────
    enable_schema_enrichment: bool = DEFAULT_CONFIG.enable_schema_enrichment
    retrieval_mode: str = DEFAULT_CONFIG.retrieval_mode
    enable_cypher_healing: bool = DEFAULT_CONFIG.enable_cypher_healing
    enable_critic_validation: bool = DEFAULT_CONFIG.enable_critic_validation
    enable_reranker: bool = DEFAULT_CONFIG.enable_reranker
    enable_hallucination_grader: bool = DEFAULT_CONFIG.enable_hallucination_grader

    # ── Logging ────────────────────────────────────────────────────────────────
    log_level: str = DEFAULT_CONFIG.log_level


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """Return the singleton Settings instance (cached after first call)."""
    return Settings()


def reload_settings() -> None:
    """Force-reload Settings from the current ``os.environ``.

    Clears the ``get_settings`` LRU cache, creates a fresh ``Settings()``
    instance, then **mutates the module-level** ``settings`` **alias in-place**
    so that existing ``from src.config.settings import settings`` bindings
    across all already-imported modules immediately see the new values —
    without requiring a kernel restart.

    Why in-place mutation?  If ``reload_settings()`` simply reassigned the
    module attribute (``settings_module.settings = new_instance``), callers
    that have already done ``from settings import settings`` would keep a
    reference to the *old* object.  Mutating ``settings.__dict__`` propagates
    the change to every reference simultaneously.

    Typical notebook usage::

        import os
        os.environ["LLM_MODEL_REASONING"] = "claude-sonnet-4-5"
        from src.config.llm_factory import reconfigure_from_env
        reconfigure_from_env()  # calls reload_settings() then clears LLM caches
    """
    import src.config.settings as _mod

    get_settings.cache_clear()
    new = Settings()
    _mod.settings.__dict__.update(new.__dict__)


# Module-level singleton — import with:
#   from src.config.settings import settings
settings: Settings = get_settings()
```

### Field Notes

| Field | Default | Notes |
|---|---|---|
| `lmstudio_base_url` | `"http://localhost:1234/v1"` | LM Studio OpenAI-compatible endpoint — set via `LMSTUDIO_BASE_URL` |
| `openrouter_api_key` | `""` | OpenRouter API key — set via `OPENROUTER_API_KEY` |
| `openrouter_base_url` | `"https://openrouter.ai/api/v1"` | OpenRouter base URL — set via `OPENROUTER_BASE_URL` |
| `llm_model_extraction` | `"local-model"` | Model name as shown in LM Studio's loader — set via `LLM_MODEL_EXTRACTION` |
| `llm_model_reasoning` | `"local-model"` | Model name as shown in LM Studio's loader — set via `LLM_MODEL_REASONING` |
| `llm_max_tokens_extraction` | `16384` | Max output tokens for extraction — prevents JSON truncation; set via `LLM_MAX_TOKENS_EXTRACTION` |
| `llm_max_tokens_reasoning` | `8192` | Max token budget for reasoning/generation — caps thinking + output for OpenRouter models with mandatory thinking; set via `LLM_MAX_TOKENS_REASONING` |
| `llm_temperature_extraction` | `0.0` | SLM must be deterministic |
| `llm_temperature_generation` | `0.3` | Slight creativity for fluent answers |
| `max_llm_retries` | `3` | Max retry attempts in `InstrumentedLLM` on rate-limit / timeout |
| `confidence_threshold` | `0.90` | Below this → HITL breakpoint triggered |
| `er_similarity_threshold` | `0.85` | Cosine similarity cut-off for ER blocking |
| `retrieval_mode` | `"hybrid"` | Ablation: set to `"vector"` or `"bm25"` to disable components |
| `enable_cypher_healing` | `True` | Ablation: set `False` to measure self-repair contribution |

---

## 5. Tests

**File:** `tests/unit/test_settings.py`

```python
"""Unit tests for src/config/settings.py"""

import os
from unittest.mock import patch

import pytest

from src.config.settings import Settings, get_settings


class TestSettingsDefaults:
    def test_default_neo4j_uri(self) -> None:
        s = Settings()
        assert s.neo4j_uri == "bolt://localhost:7687"

    def test_default_temperatures(self) -> None:
        s = Settings()
        assert s.llm_temperature_extraction == 0.0
        assert s.llm_temperature_reasoning == 0.0
        assert s.llm_temperature_generation == 0.3

    def test_default_thresholds_in_range(self) -> None:
        s = Settings()
        assert 0.0 <= s.confidence_threshold <= 1.0
        assert 0.0 <= s.er_similarity_threshold <= 1.0

    def test_default_loop_guards_positive(self) -> None:
        s = Settings()
        assert s.max_reflection_attempts > 0
        assert s.max_cypher_healing_attempts > 0
        assert s.max_hallucination_retries > 0

    def test_ablation_flags_default_true(self) -> None:
        s = Settings()
        assert s.enable_schema_enrichment is True
        assert s.enable_cypher_healing is True
        assert s.enable_reranker is True

    def test_secret_str_not_exposed(self) -> None:
        s = Settings()
        # SecretStr repr must not expose the value
        assert "neo4j" not in repr(s.neo4j_password)


class TestSettingsFromEnv:
    def test_override_via_env(self) -> None:
        with patch.dict(os.environ, {"NEO4J_URI": "bolt://myhost:7688"}):
            s = Settings()
            assert s.neo4j_uri == "bolt://myhost:7688"

    def test_override_confidence_threshold(self) -> None:
        with patch.dict(os.environ, {"CONFIDENCE_THRESHOLD": "0.80"}):
            s = Settings()
            assert s.confidence_threshold == 0.80

    def test_override_ablation_flag(self) -> None:
        with patch.dict(os.environ, {"ENABLE_SCHEMA_ENRICHMENT": "false"}):
            s = Settings()
            assert s.enable_schema_enrichment is False

    def test_secret_accessible_via_method(self) -> None:
        with patch.dict(os.environ, {"NEO4J_PASSWORD": "secret123"}):
            s = Settings()
            assert s.neo4j_password.get_secret_value() == "secret123"


class TestGetSettingsSingleton:
    def test_get_settings_returns_settings_instance(self) -> None:
        s = get_settings()
        assert isinstance(s, Settings)

    def test_singleton_same_object(self) -> None:
        # lru_cache ensures same object is returned
        s1 = get_settings()
        s2 = get_settings()
        assert s1 is s2
```

---

## 6. Smoke Test

```bash
python -c "from src.config.settings import settings; print(settings.neo4j_uri)"
```

Expected: `bolt://localhost:7687` (or your overridden value from `.env`)

---

## 7. Dynamic Reconfiguration

### The Module-Level Binding Problem

Python caches imported names at the call site:

```python
from src.config.settings import settings  # binds the name 'settings' to the current object
```

If `reload_settings()` simply did `settings_module.settings = new_instance`, every module that had already executed that import statement would still hold a reference to the *old* `Settings` object. Reassigning the module attribute does not update those existing references.

### The In-Place Mutation Solution

`reload_settings()` solves this by **mutating the existing object's `__dict__`** rather than replacing the object:

```python
_mod.settings.__dict__.update(new.__dict__)
```

This overwrites every field on the *same object in memory* that all callers already hold a reference to. The object identity (memory address) does not change — only its contents do.

### Correct Notebook Pattern

```python
import os

# 1. Change the environment variable
os.environ["LLM_MODEL_REASONING"] = "claude-sonnet-4-5"

# 2. Call reconfigure_from_env() — this calls reload_settings() internally,
#    then clears the LLM factory's lru_cache so new LLM instances are built.
from src.config.llm_factory import reconfigure_from_env
reconfigure_from_env()

# 3. All subsequent calls now use the new model
from src.config.llm_factory import get_reasoning_llm
llm = get_reasoning_llm()  # ChatAnthropic, not ChatOpenAI
```

> **Never** call `reload_settings()` directly in notebooks — always use `reconfigure_from_env()`, which also clears the LLM factory caches. Calling only `reload_settings()` would update `settings` but leave stale LLM instances cached.
