# Part 1 — `src/config/settings.py`

## 1. Purpose & Context

**Epic:** EP-01 — US-01-02 — Settings & Secret Management

Loads every configurable parameter from environment variables / `.env` file. Provides a module-level singleton `settings` so all other modules import config in one line. Uses `pydantic-settings` for automatic env-var parsing, type coercion, and validation.

**Architectural capability:** Only model *identifiers* and *thresholds* live here. The concrete `BaseChatModel` subclass — `ChatOpenRouter`, `ChatOpenAI`, `ChatOllama`, `ChatAnthropic`, etc. — is selected inside `llm_factory.py`. Swapping provider requires changing one import and one constructor call there; `settings.py` is untouched.

**Thesis constraint (zero budget, no local GPU):** All thesis runs use OpenRouter Free Tier via `OPENROUTER_API_KEY`. The two Qwen Free-Tier model slugs below cover the SLM extraction role (originally NuExtract) and the reasoning / generation role.

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
"""EP-01: Application settings loaded from environment / .env file."""

from __future__ import annotations

from functools import lru_cache

from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        secrets_dir="/run/secrets",
        extra="ignore",
    )

    # ── Neo4j ──────────────────────────────────────────────────────────────────
    neo4j_uri: str = "bolt://localhost:7687"
    neo4j_user: str = "neo4j"
    neo4j_password: SecretStr = SecretStr("neo4j")

    # ── LLM — thesis: OpenRouter Free Tier; architecture: any BaseChatModel ───
    # Swap llm_model_* values (and ChatOpenRouter in llm_factory.py) to route
    # to any provider: gpt-4o, claude-3-5-sonnet, llama via vLLM, etc.
    openrouter_api_key: SecretStr = SecretStr("")   # OPENROUTER_API_KEY env var
    llm_model_reasoning: str = "qwen/qwen3-coder:free"                    # reasoning + generation
    llm_model_extraction: str = "qwen/qwen3-next-80b-a3b-instruct:free"   # SLM extraction
    llm_temperature_extraction: float = 0.0
    llm_temperature_reasoning: float = 0.0
    llm_temperature_generation: float = 0.3

    # ── Embeddings & Reranking ─────────────────────────────────────────────────
    embedding_model: str = "BAAI/bge-m3"
    reranker_model: str = "BAAI/bge-reranker-large"
    reranker_top_k: int = 5

    # ── Entity Resolution ──────────────────────────────────────────────────────
    er_blocking_top_k: int = 10
    er_similarity_threshold: float = 0.85

    # ── Confidence & Loop Guards ───────────────────────────────────────────────
    confidence_threshold: float = 0.90
    max_reflection_attempts: int = 3
    max_cypher_healing_attempts: int = 3
    max_hallucination_retries: int = 3
    max_llm_retries: int = 3                # InstrumentedLLM retry attempts on rate-limit/timeout

    # ── Chunking ───────────────────────────────────────────────────────────────
    chunk_size: int = 512
    chunk_overlap: int = 64

    # ── Retrieval ──────────────────────────────────────────────────────────────
    retrieval_vector_top_k: int = 20
    retrieval_bm25_top_k: int = 10
    retrieval_graph_depth: int = 2

    # ── Few-Shot ───────────────────────────────────────────────────────────────
    few_shot_cypher_examples: int = 5

    # ── Ablation Flags ─────────────────────────────────────────────────────────
    enable_schema_enrichment: bool = True
    retrieval_mode: str = "hybrid"          # "hybrid" | "vector" | "bm25"
    enable_cypher_healing: bool = True
    enable_critic_validation: bool = True
    enable_reranker: bool = True
    enable_hallucination_grader: bool = True

    # ── Logging ────────────────────────────────────────────────────────────────
    log_level: str = "INFO"


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """Return the singleton Settings instance (cached after first call)."""
    return Settings()


# Module-level singleton — import with:
#   from src.config.settings import settings
settings: Settings = get_settings()
```

### Field Notes

| Field | Default | Notes |
|---|---|---|
| `openrouter_api_key` | `""` | `SecretStr` — set via `OPENROUTER_API_KEY`; obtain at openrouter.ai/keys |
| `llm_model_extraction` | `"qwen/qwen3-next-80b-a3b-instruct:free"` | Thesis SLM — fills NuExtract role without local GPU; drop-in for any JSON-mode model |
| `llm_model_reasoning` | `"qwen/qwen3-coder:free"` | Thesis reasoning/generation model — replace slug for any OpenRouter or other provider model |
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
