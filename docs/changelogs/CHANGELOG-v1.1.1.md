# Changelog — v1.1.1

**Date:** 2026-05-06  
**Audit Reference:** docs/audits/AUDIT-2026-05-06.md

## Summary

Full adversarial audit (9 agents, 68 findings) — all findings resolved. Security hardening (SSRF prevention, Cypher dual-guard), performance optimizations (O(n²) elimination, UNION ALL queries), complete config drift externalization, and unit test suite expanded from 405 → 508. Pipeline re-run (AB-01→AB-20) in progress with latest code.

## Changes

### Critical (RED) — Security

- **SSRF URL validation** (`src/config/model_builders.py`): New `_validate_base_url()` blocks non-http/https schemes, cloud metadata endpoints (169.254.169.254, metadata.google.internal, 100.100.100.200), and link-local IPs. Applied to all 3 builder paths (OpenRouter, LM Studio, OpenAI-compatible).
- **Cypher injection — dual guard** (`src/graph/cypher_healer.py`): Expanded blocklist (CREATE/ALTER/DROP USER/ROLE, GRANT/REVOKE/DENY, LOAD CSV) + positive first-keyword allowlist (MERGE, MATCH, WITH, UNWIND, RETURN, OPTIONAL, CALL).
- **PipelineConfig SSRF** (`src/api/models.py`): `@model_validator` restricts `lmstudio_base_url` to http/https + blocks metadata endpoints. *(Already resolved in prior commit.)*
- **`_logger` undefined** (`src/api/app.py`): Added `from src.config.logging import get_logger; _logger = get_logger(__name__)`. *(Already resolved in prior commit.)*

### High (ORANGE) — Logic & Security

- **Prompt injection mitigation** (`src/generation/answer_generator.py`): User query XML-escaped before template interpolation.
- **Embedding write failure tracking** (`src/graph/build_nodes.py`): `state["embedding_failures"]` list populated on Neo4j write error.
- **Entity resolver fallback** (`src/resolution/entity_resolver.py`): Singleton definition fallback returns `entity_name` instead of empty string.
- **FallbackLLM race condition** (`src/config/llm_client.py`): Lock acquired before `_get_current_model()` in `__getattr__`.
- **Grader correction gate** (`src/generation/hallucination_grader.py`): `max_consistency_corrections = 2` — allows 2+ corrections before defaulting to pass.
- **Input list bounds** (`src/api/models.py`): `BuildRequest.doc_paths` (max 100), `ddl_paths` (max 50), `SaveConversationRequest.messages` (max 500).
- **Config override type safety** (`src/api/app.py`): `try/except` around `reload_settings()` reverts env vars on validation failure.
- **Model name injection** (`src/api/models.py`): Regex `^[a-zA-Z0-9/_.\-:]+$` validates all model name fields.

### Medium (YELLOW) — Performance

- **O(n²) blocking elimination** (`src/resolution/blocking.py`): Replaced full cosine similarity matrix with batched normalized dot-product + `np.argpartition` for top-k. Memory: O(n×k) instead of O(n²).
- **UNION ALL Neo4j query** (`src/retrieval/hybrid_retriever.py`): Merged 3 separate `build_node_index()` queries into single UNION ALL.
- **RRF constant externalized** (`src/generation/nodes/retrieval_nodes.py`): Both `merge_results()` calls use `settings.retrieval_rrf_constant`.

### Medium (YELLOW) — Config Drift (C-001→C-031)

- **Polling interval** (`src/api/demo_router.py`): `0.5` → `settings.api_polling_interval`
- **Reranker weights** (`src/retrieval/reranker.py`): 4 constants → `settings.reranker_weight_{rerank,vector,bm25,graph}`
- **Embedding batch size** (`src/retrieval/embeddings.py`): `32` → `settings.embedding_batch_size`
- **Heuristic confidence** (`src/extraction/heuristic_extractor.py`): `0.55` → `settings.heuristic_extraction_confidence`
- **SpaCy confidence** (`src/extraction/heuristic_extractor.py`): `0.60` → `settings.heuristic_spacy_confidence`
- **ER threshold step** (`src/resolution/blocking.py`): `0.05` → `settings.er_threshold_step` (2 sites)
- **Critic timeout** (`src/mapping/validator.py`): `120` → `settings.llm_request_timeout`
- **Pool confidence ceiling** (`src/generation/nodes/retrieval_nodes.py`): `0.75` → `settings.pool_confidence_ceiling`
- **Context score gate** (`src/generation/answer_generator.py`): `0.10` → `settings.retrieval_context_score_gate`
- **Mapping fallback penalty** (`src/mapping/rag_mapper.py`): `0.05` → `settings.er_threshold_step`
- **New config fields**: `pool_confidence_ceiling`, `heuristic_spacy_confidence`

### Medium (YELLOW) — Test Gaps Closed (7/7 files)

| File | Tests Added |
|------|-------------|
| `src/config/provider_detection.py` | 32 (all detection routes, reasoning model check, free suffix) |
| `src/retrieval/bm25_retriever.py` | 9 (search, expansion, cache, empty input) |
| `src/ingestion/file_registry.py` | 12 (SHA compute, status check, register, orphan, purge) |
| `src/graph/kg_registry.py` | 15 (list, save, load, eject, delete, rename snapshots) |
| `src/graph/conversation_registry.py` | 10 (CRUD, auto-title, snapshot association) |
| `src/retrieval/node_utils.py` | 7 (text flattening, fallbacks, edge cases) |
| `src/mapping/retrieval.py` | 5 (query building, top-k retrieval) |

### Low (GREEN)

- **JSON depth guard** (`src/utils/json_utils.py`): `safe_json_loads()` with max 50 levels nesting.
- **Neo4j driver close** (`src/graph/neo4j_client.py`): Exception promoted from debug to warning.
- **Redundant import alias** (`src/api/demo_router.py`): Removed `_settings_override as _settings_override`.
- **Dependency bounds** (`pyproject.toml`): All LangChain deps already capped (`<1.0` / `<2.0`).

## Verification

| Check | Result |
|-------|--------|
| `pytest tests/unit/ -q` | **508 passed**, 0 failed |
| `ruff check src/ scripts/` | **All checks passed!** (0 errors, 0 warnings) |
| `ruff format --check src/ scripts/` | All files formatted |
| Pipeline AB-01→AB-20 | In progress |

## Commits

| Hash | Description |
|------|-------------|
| `d1568e0` | Security fixes batch 1 (prompt injection, embedding failures, ER fallback, race condition) |
| `c2e2f9d` | Security fixes batch 2 (JSON depth guard, driver close warning) |
| `5862406` | AI Judge path fix |
| `7423ee9` | AB-01→AB-04 fresh results |
| `b487ddc` | Performance P-001 (UNION ALL) + P-002 (O(n²) elimination) |
| `2dd95ff` | Config drift C-023→C-031 |
| `a151c6c` | SSRF URL validation + input bounds + 66 new tests |
| `0a60345` | 4 test gap files (kg_registry, conversations, node_utils, mapping/retrieval) |
| `7443783` | Code cleanup: ruff --fix (290 fixes), dead code removal, drop TCH rule |
| `d7f91c3` | Code style: ruff format (40 files) |
| `0249354` | Fix all remaining ruff warnings (E501, B023, N806, B905, UP031, SIM103) |

### Code Cleanup (Post-Audit)

- **Ruff --fix** (290 auto-fixes): import sorting (I001), syntax upgrades (UP), simplifications (SIM)
- **Ruff format**: 40 files reformatted to consistent style
- **Dead code removal**: 3 unused variables (`cfg`, `candidate_text`, `idx_arr`)
- **TCH rule dropped**: Incompatible with LangGraph runtime TypedDict resolution (`from __future__ import annotations` + `TYPE_CHECKING` breaks StateGraph channel introspection)
- **E501 resolved**: All 68 long lines broken across 15 files
- **B023 resolved**: Loop variable binding via default argument pattern
- **B905/UP031/SIM103**: `zip(strict=False)`, f-string upgrades, inline returns
- **Per-file-ignores**: Added for framework patterns (A002 shadow in Pydantic models, BLE001 in resilient pipeline nodes)
- **Final state**: `ruff check src/ scripts/` → **All checks passed!**
