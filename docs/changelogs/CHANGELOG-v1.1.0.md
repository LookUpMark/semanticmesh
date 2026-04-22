# Changelog — v1.1.0

**Date:** 2026-04-22
**Audit Reference:** docs/audits/AUDIT-2026-04-22.md

## Summary

Production readiness audit — 22 issues fixed across security, correctness, and documentation. Critical RRF fusion bug fixed in hybrid retrieval (thesis validity). API hardened with allowlist-based config endpoint, DELETE confirmation, error info masking, and dataset path restrictions. All doc inconsistencies resolved.

## Changes

### Critical (RED)

- **Fixed `merge_results` — true RRF implementation** (`src/retrieval/hybrid_retriever.py`): Replaced incorrect max-score dedup with Reciprocal Rank Fusion (`score = sum(1/(k+rank))` per source, `k=60`). Previous code compared BM25/vector/graph scores directly (apples-to-oranges). Updated unit tests to verify RRF scoring.

### High (ORANGE)

- **API auth — prominent startup warning** (`src/api/auth.py`): Box-drawing banner logged when `API_KEY` unset, making disabled auth visible in logs.
- **API config — allowlist + sensitive key block** (`src/api/app.py`): Replaced fragile blocklist with `Settings.model_fields` allowlist for `POST /api/v1/config`. Uppercase env var aliases accepted. Sensitive keys (`NEO4J_PASSWORD`, `*_API_KEY`) explicitly blocked even if in Settings.
- **CORS — restrictive default** (`src/api/app.py`): Default origins changed from `*` to `http://127.0.0.1:8000,http://localhost:8000`. Warning logged when wildcard used.

### Medium (YELLOW)

- **`best_proposal` None guard** (`src/graph/validation_nodes.py`): Added None-safe access for `best_proposal.mapped_concept` and `.confidence` in critic exhaustion path.
- **Missing `BuilderState` fields** (`src/models/state.py`): Added `validation_error: str | None` and `parent_chunks: list[Chunk]` declarations.
- **Thread-safe `_settings_override`** (`src/evaluation/ablation_runner.py`): Wrapped env var mutation in `threading.Lock` to prevent concurrent API request races.
- **Deep copy in `get_job`** (`src/api/jobs.py`): `copy.deepcopy` prevents mutable shared state between API callers.
- **Error info masking** (`src/api/demo_router.py`): All 500 responses now return generic `"Internal server error. Check server logs."` instead of `str(exc)`.
- **DELETE confirmation** (`src/api/demo_router.py`): `DELETE /graph` requires `?confirm=true` query parameter.
- **Dataset path restriction** (`src/api/ablation_router.py`): Custom ablation datasets restricted to `tests/fixtures/` and `data/` subdirectories.
- **Hardcoded Neo4j password removed** (`scripts/neo4j_lifecycle.py`): `NEO4J_PASSWORD` env var now required; script exits with clear error if unset.
- **Cypher apostrophe fixer** (`src/graph/cypher_generator.py`): Guard for unmatched single quotes — appends rest of string unchanged instead of dropping last character.
- **`azure_openai_api_version` in Settings** (`src/config/settings.py`): Field now overridable via `AZURE_OPENAI_API_VERSION` env var.
- **`langchain-anthropic` + `langchain-ollama`** (`pyproject.toml`): Added missing dependencies.
- **Doc consistency** (`CLAUDE.md`, `README.md`, `src/generation/nodes/retrieval_nodes.py`):
  - Removed non-existent `safe_json_loads` reference
  - Fixed reranker model name: `bge-reranker-large` → `bge-reranker-v2-m3`
  - Fixed function name: `_clean_json()` → `clean_json()`
  - Removed non-existent `notebooks/ablation/` references
  - Fixed `cd semanticmesh` → `cd thesis`
  - Fixed Docker container name: `neo4j-semanticmesh` → `neo4j-thesis`
  - Added missing OpenAI prefixes: `o2-*`, `text-*`

### Low (GREEN)

- **Dead logic removed** (`src/generation/nodes/retrieval_nodes.py`): `max(top_k*4, top_k)` → `top_k * 4`.
- **Silent pass → logged** (`src/graph/builder_graph.py`, `src/graph/neo4j_client.py`, `src/ingestion/schema_enricher.py`): BM25 cache invalidation, driver close, and column skip errors now logged.
- **Array JSON support** (`src/utils/json_utils.py`): `clean_json()` now extracts `[...]` arrays in addition to `{...}` objects.
- **`sqlite_checkpoint_path` in config.py** (`src/config/config.py`): Added to `AppConfig` dataclass for consistency with Settings.
- **Installed `langchain-opendataloader-pdf`** — resolved missing module causing 2 test collection errors.

## Verification

- Unit tests: **397 passed, 0 failed**
- Integration tests (API): **21 passed, 0 failed**
- Integration tests (Neo4j): **9 passed, 16 ERROR** (Docker fixture — environment, not code)
- Stale reference grep: **0 hits** for `bge-reranker-large`, `safe_json_loads`, `_clean_json`, `semanticmesh`
