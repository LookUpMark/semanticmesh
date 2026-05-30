"""FastAPI application — mounts both the E2E Demo and Ablation Studies APIs."""

from __future__ import annotations

import logging
import os
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, ConfigDict

from src.api.ablation_router import router as ablation_router
from src.api.auth import require_api_key
from src.api.demo_router import router as demo_router
from src.config.logging import get_logger
from src.config.observability import flush_observability, is_langfuse_enabled, is_langsmith_enabled

_logger = get_logger(__name__)

# ── Session File Logging (module-level state for lifespan) ─────────────────────

_SESSION_LOG_DIR = Path("outputs/api")
_session_run_dir: Path | None = None
_session_file_handler: logging.FileHandler | None = None


# AUDIT-013 (ORANGE): Replace deprecated on_event with lifespan async context manager.
@asynccontextmanager
async def _lifespan(app: FastAPI) -> AsyncGenerator[dict[str, Any], None]:
    """Application lifespan: startup and shutdown logic in one context manager.

    Replaces the deprecated @app.on_event("startup") / @app.on_event("shutdown")
    pattern which is scheduled for removal in FastAPI 1.0.
    """
    global _session_file_handler, _session_run_dir  # noqa: PLW0603

    # ── Startup ────────────────────────────────────────────────────────────
    # Log observability status
    if is_langsmith_enabled():
        _logger.info("Observability: LangSmith tracing ENABLED")
    if is_langfuse_enabled():
        _logger.info("Observability: Langfuse tracing ENABLED")

    # Set up session file logging
    timestamp = datetime.now(UTC).strftime("%Y%m%d_%H%M%S")
    _session_run_dir = _SESSION_LOG_DIR / f"session_{timestamp}"
    _session_run_dir.mkdir(parents=True, exist_ok=True)
    log_path = _session_run_dir / "session.log"

    from pythonjsonlogger import jsonlogger  # noqa: PLC0415

    handler = logging.FileHandler(log_path, encoding="utf-8")
    formatter = jsonlogger.JsonFormatter(
        fmt="%(asctime)s %(name)s %(levelname)s %(message)s",
        datefmt="%Y-%m-%dT%H:%M:%S",
        rename_fields={"asctime": "ts", "name": "logger", "levelname": "level"},
    )
    handler.setFormatter(formatter)
    logging.getLogger().addHandler(handler)
    _session_file_handler = handler
    _logger.info("API session log: %s", log_path)

    yield {}  # Application runs here

    # ── Shutdown ───────────────────────────────────────────────────────────
    flush_observability()

    import json  # noqa: PLC0415

    from src.config.llm_client import get_llm_usage_summary  # noqa: PLC0415

    usage = get_llm_usage_summary()
    if usage and _session_run_dir:
        _logger.info("LLM usage summary: %s", json.dumps(usage, default=str))
        summary_path = _session_run_dir / "usage.json"
        summary_path.write_text(json.dumps(usage, indent=2, default=str), encoding="utf-8")

    if _session_file_handler:
        _session_file_handler.flush()
        _session_file_handler.close()
        logging.getLogger().removeHandler(_session_file_handler)
        _session_file_handler = None


app = FastAPI(
    lifespan=_lifespan,
    title="GraphRAG Thesis API",
    version="1.4.2",
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

_cors_origins = os.environ.get("CORS_ORIGINS", "http://127.0.0.1:8000,http://localhost:8000").split(
    ","
)
# AUDIT-026 (ORANGE): Check each individual origin for wildcard, not the whole list.
if "*" in _cors_origins:
    _logger.error(
        "CORS_ORIGINS contains '*' — rejecting wildcard. "
        "Set explicit origins (e.g. 'http://localhost:3000,http://localhost:8000')."
    )
    _cors_origins = ["http://127.0.0.1:8000", "http://localhost:8000"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=_cors_origins,
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
# AUDIT-001 (RED): Explicit ALLOWLIST of keys that may be overridden at runtime.
# Only safe, non-sensitive settings are permitted.  Infrastructure URLs, secrets,
# auth keys, and provider endpoints are NEVER accepted — those require a server restart.
#
# Allowed categories:
#   - Boolean ablation flags (enable_*)
#   - Numeric thresholds and limits
#   - String identifiers (study_name)
#
# NEVER allow: LLM_ENDPOINT_*, NEO4J_*, *_BASE_URL, *_API_KEY, *_PASSWORD,
#   LMSTUDIO_*, CORS_*, LANGCHAIN_*, LANGFUSE_*, LOG_LEVEL, ENABLE_DEBUG_TRACE,
#   or any key not listed below.

_ALLOWED_OVERRIDE_KEYS: frozenset[str] = frozenset(
    {
        # ── Boolean ablation flags ─────────────────────────────────────────
        "ENABLE_SCHEMA_ENRICHMENT",
        "ENABLE_CYPHER_HEALING",
        "ENABLE_CRITIC_VALIDATION",
        "ENABLE_HALLUCINATION_GRADER",
        "ENABLE_RERANKER",
        "ENABLE_RETRIEVAL_QUALITY_GATE",
        "ENABLE_GRADER_CONSISTENCY_VALIDATOR",
        "ENABLE_SPACY_HEURISTICS",
        "ENABLE_LAZY_EXPANSION",
        "USE_LAZY_EXTRACTION",
        # ── Numeric thresholds ──────────────────────────────────────────────
        "CONFIDENCE_THRESHOLD",
        "ER_SIMILARITY_THRESHOLD",
        "ER_BLOCKING_TOP_K",
        "RERANKER_TOP_K",
        "RETRIEVAL_VECTOR_TOP_K",
        "RETRIEVAL_BM25_TOP_K",
        "RETRIEVAL_GRAPH_DEPTH",
        "MAX_REFLECTION_ATTEMPTS",
        "MAX_CYPHER_HEALING_ATTEMPTS",
        "MAX_HALLUCINATION_RETRIES",
        "CHUNK_SIZE",
        "CHUNK_OVERLAP",
        "PARENT_CHUNK_SIZE",
        "PARENT_CHUNK_OVERLAP",
        "PROVENANCE_MAX_CHARS",
        "EMBEDDING_DIMENSIONS",
        "MAPPING_CONCURRENCY",
        "LLM_MAX_TOKENS_EXTRACTION",
        "LLM_MAX_TOKENS_REASONING",
        "LLM_TEMPERATURE_EXTRACTION",
        "LLM_TEMPERATURE_REASONING",
        "LLM_TEMPERATURE_GENERATION",
        # ── String names ────────────────────────────────────────────────────
        "STUDY_NAME",
        "RETRIEVAL_MODE",
        "LLM_MODEL_REASONING",
        "LLM_MODEL_EXTRACTION",
        "LLM_MODEL_MIDTIER",
        "LLM_MODEL_GENERATION",
        "LLM_PROVIDER",
    }
)


class ServerConfigRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    overrides: dict[str, str]


# AUDIT-072 (YELLOW): TODO — Restrict the config endpoint to admin-only access.
# Currently any authenticated user can read all model names, chunk sizes, thresholds,
# feature flags, and internal URLs. Consider adding a separate ADMIN_API_KEY or
# restricting this endpoint to a dedicated /admin/ prefix.
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

    AUDIT-001 (RED): Uses an explicit ALLOWLIST — only keys in
    ``_ALLOWED_OVERRIDE_KEYS`` are accepted.  All other keys (secrets, endpoints,
    infrastructure) are silently blocked.  Overrides are applied in-process only
    via os.environ and the settings cache is reloaded on success.
    """
    applied: list[str] = []
    blocked: list[str] = []
    errors: list[str] = []
    for key, value in req.overrides.items():
        # AUDIT-001: Only allow keys on the explicit allowlist
        if key.upper() not in _ALLOWED_OVERRIDE_KEYS:
            blocked.append(key)
            continue
        if value:
            os.environ[key.upper()] = value
            applied.append(key.upper())

    if applied:
        from src.config.llm_factory import reconfigure_from_env
        from src.config.settings import reload_settings

        try:
            reload_settings()
            reconfigure_from_env()
        except Exception as exc:
            # Revert applied env vars on validation failure
            for key in applied:
                os.environ.pop(key, None)
            errors.append(f"Settings validation failed: {type(exc).__name__}")
            applied.clear()

    return {
        "applied": applied,
        "blocked": blocked,
        "errors": errors,
    }
