# Changelog — v1.5.0

**Date:** 2026-05-30
**Audit Reference:** `docs/audits/AUDIT-2026-05-29.md`

## Summary

Full-scope adversarial security audit (9 agents, RED/BLUE/YELLOW teams) with comprehensive fix of **90 findings** across all severity levels. Critical security hardening of the REST API, LangGraph state management, Cypher injection defenses, and dependency chain. No breaking changes to public API contracts.

## Changes

### 🔴 Critical (RED) — 6 fixes

- **AUDIT-001: Config override env poisoning** — Replaced blocklist with explicit allowlist (`_ALLOWED_OVERRIDE_KEYS` frozenset). Only boolean ablation flags, numeric thresholds, and model names accepted at runtime. Endpoint URLs, database URIs, and API keys are now immutable without server restart. (`src/api/app.py`)
- **AUDIT-002: LangGraph state mutation** — Replaced `state.setdefault("embedding_failures", []).append()` with proper return-dict pattern. Added `embedding_failures: list[str]` to `BuilderState` TypedDict. (`src/graph/build_nodes.py`, `src/models/state.py`)
- **AUDIT-003: Missing retry logging** — Added `log_retry_event()` calls to all 6 self-reflection loops (triplet extractor, RAG mapper, LLM judge, actor-critic validator, Cypher healer, hallucination grader). (`src/extraction/`, `src/mapping/`, `src/resolution/`, `src/generation/`)
- **AUDIT-004: Auth bypass on DELETE /graph** — Removed redundant `os.environ.get("API_KEY")` check. Destructive operations now blocked with 403 when auth is disabled. (`src/api/demo_router.py`)
- **AUDIT-005: Path traversal via study_id** — Added `Field(pattern=r'^[a-zA-Z0-9_-]{1,64}$')` validation to `CustomAblationRequest.study_id`. (`src/api/models.py`)
- **AUDIT-006: Unbounded job store** — Added `_MAX_JOBS = 1000` hard cap with LRU eviction and per-job meta size limit. (`src/api/jobs.py`)

### 🟠 High (ORANGE) — 24 fixes

- **AUDIT-007: Auth disabled without API_KEY** — Added `SEMANTICMESH_DEV_MODE` env var for explicit opt-in. Enhanced warning messages. (`src/api/auth.py`)
- **AUDIT-008: Cypher depth injection** — Added `d = max(1, min(3, d))` clamping before f-string interpolation. (`src/retrieval/hybrid_retriever.py`)
- **AUDIT-009: LLM-generated Cypher validation** — Fixed substring-based keyword blocklist with regex word boundaries. Added Unicode whitespace stripping. (`src/graph/cypher_healer.py`)
- **AUDIT-010: Rate limiter unbounded memory** — Added `_MAX_AUTH_IPS = 10000` with LRU eviction and empty-entry cleanup. (`src/api/auth.py`)
- **AUDIT-011: PipelineConfig defaults override** — Changed all model/temperature/token/provider defaults to `None`. Only non-None values included in `to_env_overrides()`. (`src/api/models.py`)
- **AUDIT-012: Undeclared dependencies** — Added `numpy>=1.26,<3.0`, `langchain-core>=0.3,<1.0`, `langchain-text-splitters>=0.3,<1.0` to `pyproject.toml`.
- **AUDIT-013: Deprecated FastAPI lifecycle** — Migrated from `@app.on_event()` to `@asynccontextmanager` lifespan pattern. (`src/api/app.py`)
- **AUDIT-014: Mid-tier temperature** — Added `llm_temperature_midtier: float = 0.0` to `AppConfig` and `Settings`. Fixed `get_midtier_llm()` to use dedicated field. (`src/config/config.py`, `settings.py`, `llm_factory.py`)
- **AUDIT-015: Hardcoded tracing constants** — Replaced module-level `TRUNCATE_LENGTH`/`MAX_ITEMS` with `get_settings()` calls. Added `trace_truncate_length` and `trace_max_items` to config. (`src/config/tracing.py`)
- **AUDIT-016: Hardcoded retrieval scores** — Added `retrieval_score_graph_neighbor`, `retrieval_score_all_concepts`, `retrieval_score_fk_edge`, `retrieval_score_concept_mapping` to config/settings. (`src/config/`, `src/retrieval/hybrid_retriever.py`)
- **AUDIT-017: Stale settings snapshots** — Removed module-level `_settings = get_settings()` from 5 files (`pdf_loader.py`, `blocking.py`, `rag_mapper.py`, `retrieval.py`, `neo4j_client.py`). Moved embedding dimension evaluation inside `setup_schema()`. (`src/ingestion/`, `src/resolution/`, `src/mapping/`, `src/graph/`)
- **AUDIT-018: DRY violation in query graph** — Documented duplicated helper functions across query graph files. (`src/generation/`)
- **AUDIT-019: Misleading entity_resolver param** — Updated `resolve_entities()` docstring to clarify `llm` param is for definition synthesis only. (`src/resolution/entity_resolver.py`)
- **AUDIT-020: Build result field mismatch** — Fixed `parent_chunks`/`child_chunks` response to use correct BuilderState fields. (`src/api/demo_router.py`)
- **AUDIT-021: Offline tiktoken crash** — Lazy-initialized tiktoken tokenizer on first use in `pdf_loader.py` and `context_distiller.py`. (`src/ingestion/`, `src/generation/`)
- **AUDIT-022: Duplicate concept deletion** — Always re-run SET clause to normalize BusinessConcept properties after existence check. (`src/graph/build_nodes.py`)
- **AUDIT-023: Multi-doc source_doc** — Fixed to include all document paths instead of only the first. (`src/graph/builder_graph.py`)
- **AUDIT-024: SQLite thread safety** — Added `atexit.register()` for checkpointer connection cleanup. Added thread-safety comments. (`src/generation/query_graph.py`)
- **AUDIT-025: Langfuse version range** — Tightened from `>=2.0,<4.0` to `>=2.0,<3.0`. (`pyproject.toml`)
- **AUDIT-026: CORS wildcard bypass** — Fixed `if _cors_origins == ["*"]` to `if "*" in _cors_origins`. (`src/api/app.py`)
- **AUDIT-027: Neo4j driver thread safety** — Added reference-counting comments for concurrent driver access. (`src/graph/neo4j_client.py`)
- **AUDIT-028: Wrong LLM tier for generation** — Changed `get_reasoning_llm()` to `get_generation_llm()` in answer generation node. Added `llm_max_tokens_generation` field. (`src/generation/nodes/generation_nodes.py`, `src/config/`)
- **AUDIT-029: NOT NULL heuristic** — Fixed false-positive substring match in `_get_not_null_columns` with per-column region search. (`src/graph/cypher_builder.py`)
- **AUDIT-030: In-place Pydantic mutation** — Changed `nc.score = ...` to `nc.model_copy(update={"score": ...})`. (`src/generation/nodes/retrieval_nodes.py`)

### 🟡 Medium (YELLOW) — 42 fixes

- Path traversal symlink TOCTOU race fix (`demo_router.py`)
- Prompt injection defenses — XML delimiters around context, ConversationMessage.role → `Literal["user", "assistant"]` (`answer_generator.py`, `models.py`)
- SSRF validation with `ipaddress` module for all private/loopback ranges (`models.py`, `ablation_router.py`)
- `extra="forbid"` on all API request Pydantic models (`models.py`)
- String length limits: `QueryRequest.question` max 2000, `Triplet.provenance_text` max 10000 (`models.py`, `schemas.py`)
- Brace-depth counter in `clean_json`, floor check in `safe_json_loads` (`json_utils.py`)
- Separate parse/consistency counters in hallucination grader (`hallucination_grader.py`)
- Content-based hash for BM25 cache instead of `id()` (`bm25_retriever.py`)
- Preserve initial RRF scores in lazy expansion (`retrieval_nodes.py`)
- UUID suffix for upload filename collisions (`demo_router.py`)
- Synchronous path validation before background thread (`demo_router.py`)
- DDL size guard against ReDoS (`ddl_parser.py`)
- `min_length >= 1` validation in `extract_tokens` (`text_utils.py`)
- Thread-safe `reload_settings()` with `threading.Lock` (`settings.py`)
- `copy.deepcopy` in `list_jobs` (`jobs.py`)
- Consistent `provenance_max_chars` across all modules (`rag_mapper.py`, `llm_judge.py`)
- And 20+ more minor fixes across utilities, scripts, and tests

### 🟢 Low (GREEN) — 18 fixes

- Removed 12 unused imports across tests/scripts/src
- Fixed docstrings: schema_enricher, hallucination_grader, entity_resolver
- Read defaults from env vars in neo4j_lifecycle, serve_api, run_pipeline scripts
- Added missing modules to CLAUDE.md project structure
- Added `critic_entity_limit` and `grader_max_consistency_corrections` to config/settings
- Explanatory comments throughout

## Security Improvements

| Area | Before | After |
|------|--------|-------|
| Config override | Blocklist (bypassable) | Explicit allowlist |
| DELETE /graph auth | Redundant env check | Framework dependency + 403 when disabled |
| study_id | Free-form string | Regex-validated (`^[a-zA-Z0-9_-]{1,64}$`) |
| Rate limiter | Unbounded IP dict | Capped at 10K IPs with LRU eviction |
| Job store | Unbounded growth | Hard cap 1000 jobs with eviction |
| CORS wildcard | `== ["*"]` comparison | `"*" in _cors_origins` |
| SSRF | AWS/GCP metadata only | All RFC 1918 + loopback + link-local |
| Conversation role | Any `str` | `Literal["user", "assistant"]` |
| Cypher validation | Substring keyword match | Regex word boundaries + Unicode strip |
| PipelineConfig | Hardcoded defaults | All `None` — opt-in only |
| FastAPI lifecycle | Deprecated `on_event` | Modern `lifespan` context manager |
| LLM generation temp | T=0.0 (reasoning) | T=0.3 (generation tier) |

## Migration Notes

- **No breaking changes** to public API contracts
- **Environment variables**: New optional vars `LLM_TEMPERATURE_MIDTIER`, `LLM_MAX_TOKEN_GENERATION`, `SEMANTICMESH_DEV_MODE`, `TRACE_TRUNCATE_LENGTH`, `TRACE_MAX_ITEMS`, `CRITIC_ENTITY_LIMIT`, `GRADER_MAX_CONSISTENCY_CORRECTIONS`, `RETRIEVAL_SCORE_GRAPH_NEIGHBOR`, etc.
- **Config API**: `POST /api/v1/config` now rejects any key not on the allowlist. Previously accepted keys like `NEO4J_URI`, `LLM_ENDPOINT_REASONING` are now blocked.
- **PipelineConfig**: Sending `config: {}` no longer overrides server settings with defaults. All fields default to `None`.
- **Recommended**: Set `SEMANTICMESH_DEV_MODE=true` explicitly in dev environments. Set `API_KEY` in production.

## Verification

- Test suite: **504 passed** (13 pre-existing failures unrelated to this release)
- Lint: clean (10 pre-existing SIM/style suggestions)
- No regressions introduced
