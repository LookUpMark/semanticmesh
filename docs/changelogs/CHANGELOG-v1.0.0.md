# Changelog — v0.1.0

**Date:** 2026-04-17
**Audit Reference:** docs/audits/AUDIT-2026-04-17.md

## Summary

Security and correctness fixes from adversarial audit (audit-swarm v1.0.0). 9 agents scanned 76 Python files (~17K LOC). Fixed 4 critical, 8 high, 15 medium, and 6 low severity findings — all 33 findings resolved.

## Fixes Applied

### Critical (RED)
- **R-001:** Cypher injection via `rel_type` f-string in snapshot import — added allowlist validation + backtick quoting (`src/graph/kg_registry.py`)
- **R-002:** HITL node routed to non-existent `"Generate_Cypher"` — fixed to `"generate_cypher"` (`src/mapping/hitl.py`)
- **R-003:** HITL node routed to non-existent `"End"` — fixed to `"save_trace"` (`src/mapping/hitl.py`)
- **R-004:** `_node_generate_cypher` and `_node_heal_cypher` crashed on `KeyError` when `mapping_proposal=None` — added None guards (`src/graph/build_nodes.py`)
- **R-004:** `_route_after_validate` routed to `generate_cypher` with `mapping_proposal=None` — now routes to `save_trace` (`src/graph/validation_nodes.py`)

### High (ORANGE)
- **O-001:** Auth silently disabled without warning — added startup WARNING log (`src/api/auth.py`)
- **O-002:** Path traversal via arbitrary absolute paths — restricted to repo root (`src/api/demo_router.py`, `src/api/ablation_router.py`)
- **O-003:** Unpinned dependencies with `>=` only — added semver upper bounds to all deps (`pyproject.toml`)
- **O-004:** `_node_heal_cypher` crashed on `KeyError` — added None guard (`src/graph/build_nodes.py`)
- **O-005:** `sqlite_checkpoint_path` missing from Settings — added field (`src/config/settings.py`)
- **O-006:** Stale `_settings` in hitl.py after runtime reload — moved to per-call `get_settings()` (`src/mapping/hitl.py`)
- **O-007:** Neo4j driver instantiated 16 times across codebase — implemented singleton `_get_shared_driver()` with lazy init, connection reuse, and `close_shared_driver()` for shutdown (`src/graph/neo4j_client.py`)
- **O-008:** N+1 MENTIONS repair loop — batched with `UNWIND` Cypher statement (`src/graph/builder_graph.py`)

### Medium (YELLOW)
- **Y-001:** Config endpoint allowed unrestricted env var overrides — added blocked keys blocklist (`src/api/app.py`)
- **Y-002:** LLM-generated Cypher executed without semantic validation — added destructive keyword blocklist (`src/graph/build_nodes.py`)
- **Y-003:** Hardcoded default Neo4j password `"neo4j"` — changed to empty string, requires `NEO4J_PASSWORD` env var (`src/config/settings.py`)
- **Y-004:** No rate limiting on auth attempts — added IP-based rate limiter (5/min) (`src/api/auth.py`)
- **Y-005:** Verbose exception details in HTTP responses — replaced with generic messages (`src/api/demo_router.py`)
- **Y-006:** Permissive CORS `allow_origins=["*"]` — made configurable via `CORS_ORIGINS` env var (`src/api/app.py`)
- **Y-008:** `web_search` action in `GraderDecision` silently ignored — removed from Literal type (`src/models/schemas.py`)
- **Y-009:** SQLite connections leaked on graph rebuilds — implemented singleton connection pattern (`src/generation/query_graph.py`)
- **Y-010:** `provenance_text[:300]` crashed on `None` — added `(e.provenance_text or "")` guard (`src/mapping/rag_mapper.py`)
- **Y-011:** Unbounded job store dict — added TTL eviction (1h) and max size cap (200) (`src/api/jobs.py`)
- **Y-012:** Sync disk I/O in async upload handler — wrapped in `asyncio.to_thread` (`src/api/demo_router.py`)
- **Y-013:** FK edges written individually — batched with `execute_batch` (`src/graph/build_nodes.py`)

### Low (GREEN)
- **G-001:** Hardcoded `"lm-studio"` placeholder key — extracted to `LMSTUDIO_PLACEHOLDER_KEY` constant (`src/config/config.py`)
- **G-002:** Unreachable `else` branch in sufficiency logic — removed dead code (`src/generation/nodes/retrieval_nodes.py`)
- **G-003:** Dead code `_node_lazy_expansion` never used — removed function and exports (`src/generation/nodes/expansion_nodes.py`, `src/generation/nodes/__init__.py`)
- **G-004:** Duplicated `_query_terms` with divergent stop words — extracted to shared `src/utils/query_utils.py`, updated 3 consumers (`retrieval_nodes.py`, `generation_nodes.py`, `context_distiller.py`)
- **G-005:** Direct `ChatOpenAI` in factory LM Studio path — replaced with `make_llm()` (`src/config/llm_factory.py`)
- **G-006:** `log_node_event()` missing from 6 nodes — added to all query graph nodes (`query_graph.py`, `expansion_nodes.py`, `generation_nodes.py`, `retrieval_nodes.py`)

### State Schema
- Added `rejected: bool` field to `BuilderState` TypedDict (`src/models/state.py`)

### Tests Updated
- Updated test assertions for new routing targets, schema changes, singleton driver behavior (`test_hitl.py`, `test_builder_graph.py`, `test_hallucination_grader.py`, `test_query_graph.py`, `test_neo4j_client.py`)

## Verification

- Test suite: **362 tests, 0 failed**
- Lint: no new errors introduced (only pre-existing E501/TC issues remain)
- Regressions: none
