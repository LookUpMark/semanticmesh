"""FastAPI application — mounts both the E2E Demo and Ablation Studies APIs."""

from __future__ import annotations

import os

from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from src.api.ablation_router import router as ablation_router
from src.api.auth import require_api_key
from src.api.demo_router import router as demo_router

app = FastAPI(
    title="GraphRAG Thesis API",
    version="1.0.0",
    summary=(
        "Multi-Agent Framework for Semantic Discovery & GraphRAG — "
        "REST interface for end-to-end demos and ablation studies."
    ),
    description="""
## Authentication

All `/api/v1/*` endpoints require an `X-API-Key` header when the `API_KEY`
environment variable is set on the server.

Use the **Authorize** button (🔒) at the top of this page to enter your key —
Swagger will include it in every request automatically.

> **Local / dev mode:** if `API_KEY` is not set, authentication is disabled and
> all requests pass through without a key.

---

## E2E Demo  `/api/v1/demo/`

Drive the full GraphRAG pipeline interactively:

**KG Build**
- `POST /demo/build` — start async KG build from server-side file paths
- `POST /demo/build/upload` — start async KG build from uploaded files (no server paths needed)
- `GET  /demo/build/{job_id}` — poll build status and metrics

**Query**
- `POST /demo/query` — answer a question synchronously from the current KG

**Full Pipeline (build + query)**
- `POST /demo/pipeline` — start full async E2E pipeline from server-side paths
- `POST /demo/pipeline/upload` — start full async E2E from uploaded files
- `GET  /demo/pipeline/{job_id}` — poll pipeline status and per-question answers

**Utility**
- `GET /demo/jobs` — list all submitted build/pipeline jobs
- `GET /demo/graph/stats` — live Neo4j node/edge counts

---

## Ablation Studies  `/api/v1/ablation/`

Run, monitor, and compare ablation experiments:

**Reference**
- `GET /ablation/matrix` — browse 21 predefined AB-00…AB-20 conditions
- `GET /ablation/datasets` — list available gold-standard evaluation fixtures

**Launch**
- `POST /ablation/run/preset` — launch a predefined AB-XX study (flags auto-applied from matrix)
- `POST /ablation/run/custom` — launch a fully custom run (any flags + hyperparameters)

**Monitor**
- `GET /ablation/status/{job_id}` — poll status, summary metrics, and RAGAS scores
- `GET /ablation/jobs` — list all submitted ablation jobs

**Results**
- `GET /ablation/bundle/{study_id}/{dataset_id}` — download full evaluation bundle JSON
- `GET /ablation/evaluate/{study_id}/{dataset_id}` — AI-as-Judge payload (system prompt + bundle)
    """,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
)

# Allow all origins in development (tighten for production if needed)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# All /api/v1/* routes require an API key (no-op when API_KEY env var is not set)
app.include_router(demo_router, prefix="/api/v1", dependencies=[Depends(require_api_key)])
app.include_router(ablation_router, prefix="/api/v1", dependencies=[Depends(require_api_key)])


@app.get("/health", tags=["Health"])
def health() -> dict[str, str]:
    """Liveness probe — returns 200 OK when the server is up. No auth required."""
    return {"status": "ok"}


# ── Runtime Configuration Overrides ──────────────────────────────────────────
# Allows the frontend Settings page to push env-var overrides to the running
# server without a restart.  Overrides are applied in-process only; they are
# NOT written to .env.  Sensitive keys (API credentials) are accepted here but
# never echoed back in GET responses.

_SENSITIVE_KEYS = frozenset({
    "OPENROUTER_API_KEY", "OPENAI_API_KEY", "ANTHROPIC_API_KEY",
    "GROQ_API_KEY", "MISTRAL_API_KEY", "NEO4J_PASSWORD", "API_KEY",
})


class ServerConfigRequest(BaseModel):
    overrides: dict[str, str]


@app.get("/api/v1/config", tags=["Configuration"], dependencies=[Depends(require_api_key)])
def get_config() -> dict[str, str]:
    """Return current non-sensitive runtime configuration values."""
    from src.config.settings import get_settings
    s = get_settings()
    return {
        "LLM_PROVIDER": s.llm_provider,
        "LLM_MODEL_REASONING": s.llm_model_reasoning,
        "LLM_MODEL_EXTRACTION": s.llm_model_extraction,
        "LLM_MODEL_MIDTIER": s.llm_model_midtier,
        "LLM_TEMPERATURE_EXTRACTION": str(s.llm_temperature_extraction),
        "LLM_TEMPERATURE_REASONING": str(s.llm_temperature_reasoning),
        "LLM_TEMPERATURE_GENERATION": str(s.llm_temperature_generation),
        "LLM_MAX_TOKENS_EXTRACTION": str(s.llm_max_tokens_extraction),
        "LLM_MAX_TOKENS_REASONING": str(s.llm_max_tokens_reasoning),
        "LMSTUDIO_BASE_URL": s.lmstudio_base_url,
        "CHUNK_SIZE": str(s.chunk_size),
        "CHUNK_OVERLAP": str(s.chunk_overlap),
        "PARENT_CHUNK_SIZE": str(s.parent_chunk_size),
        "PARENT_CHUNK_OVERLAP": str(s.parent_chunk_overlap),
        "ER_BLOCKING_TOP_K": str(s.er_blocking_top_k),
        "ER_SIMILARITY_THRESHOLD": str(s.er_similarity_threshold),
        "RETRIEVAL_MODE": s.retrieval_mode,
        "RETRIEVAL_VECTOR_TOP_K": str(s.retrieval_vector_top_k),
        "RETRIEVAL_BM25_TOP_K": str(s.retrieval_bm25_top_k),
        "RERANKER_TOP_K": str(s.reranker_top_k),
        "CONFIDENCE_THRESHOLD": str(s.confidence_threshold),
        "MAX_REFLECTION_ATTEMPTS": str(s.max_reflection_attempts),
        "MAX_CYPHER_HEALING_ATTEMPTS": str(s.max_cypher_healing_attempts),
        "MAX_HALLUCINATION_RETRIES": str(s.max_hallucination_retries),
        "ENABLE_SINGLETON_LLM_DEFINITIONS": str(s.enable_singleton_llm_definitions).lower(),
        "CRITIC_CONFIDENCE_GATE": str(s.critic_confidence_gate),
        "MAX_REFLECTION_ATTEMPTS_REASONING": str(s.max_reflection_attempts_reasoning),
        "ENABLE_SCHEMA_ENRICHMENT": str(s.enable_schema_enrichment).lower(),
        "ENABLE_CYPHER_HEALING": str(s.enable_cypher_healing).lower(),
        "ENABLE_CRITIC_VALIDATION": str(s.enable_critic_validation).lower(),
        "ENABLE_HALLUCINATION_GRADER": str(s.enable_hallucination_grader).lower(),
        "ENABLE_RERANKER": str(s.enable_reranker).lower(),
        "ENABLE_RETRIEVAL_QUALITY_GATE": str(s.enable_retrieval_quality_gate).lower(),
        "ENABLE_GRADER_CONSISTENCY_VALIDATOR": str(s.enable_grader_consistency_validator).lower(),
        "ENABLE_SPACY_HEURISTICS": str(s.enable_spacy_heuristics).lower(),
        "ENABLE_LAZY_EXPANSION": str(s.enable_lazy_expansion).lower(),
        "USE_LAZY_EXTRACTION": str(s.use_lazy_extraction).lower(),
        "LOG_LEVEL": s.log_level,
        "ENABLE_DEBUG_TRACE": str(s.enable_debug_trace).lower(),
    }


@app.post("/api/v1/config", tags=["Configuration"], dependencies=[Depends(require_api_key)])
def set_config(req: ServerConfigRequest) -> dict[str, object]:
    """Apply runtime env-var overrides to the running server (no restart needed).

    Overrides are applied in-process via os.environ and the settings cache is
    reloaded.  Sensitive keys are accepted but never echoed back.
    """
    applied: list[str] = []
    for key, value in req.overrides.items():
        if value:  # ignore empty strings (skip clearing)
            os.environ[key] = value
            applied.append(key)

    if applied:
        from src.config.llm_factory import reconfigure_from_env
        from src.config.settings import reload_settings
        reload_settings()
        reconfigure_from_env()

    # Return applied keys but mask sensitive values
    return {
        "applied": applied,
        "masked": [k for k in applied if k in _SENSITIVE_KEYS],
    }
