# Changelog — v1.5.1

**Date:** 2026-06-28
**Audit Reference:** docs/audits/ML-AUDIT-2026-06-28.md
**Type:** Patch — adversarial-audit bug fixes (no API/behavior contract changes for correct callers)

## Summary

Fixes all 18 findings from the 2026-06-28 adversarial ML-audit swarm (9 finders → per-finding refute → consolidation). The headline defect (RED): the preset-ablation endpoint read `run_query()`/`BuilderState` with non-existent keys, silently emitting empty answers, 0.0 scores and always-grounded verdicts — invalidating every preset-ablation run. A cluster of ORANGE eval-validity issues (gold-standard few-shot leakage, silent table loss + broken Pipeline-Health metric, KG-provenance `MENTIONS` edges, same-basename PDF merging) is resolved in the same pass. All fixes are minimal (S/M effort) and root-caused; each is annotated `AUDIT-067`–`AUDIT-081` at the fix site.

## Fixes Applied

### Critical (RED)
- **F-001:** Preset-ablation task now reads `run_query()` via a shared `_query_fields()` helper using the correct contract keys (`final_answer`, `retrieved_contexts`, `retrieval_quality_score`, `retrieval_chunk_count`, `grader_grounded`). The custom and preset paths can no longer diverge. (`src/api/ablation_router.py`)

### High (ORANGE)
- **F-002:** Preset-ablation task now reads `BuilderState` via a shared `_builder_summary()` helper using `entities`/`tables` (not the non-existent `resolved_entities`/`table_schemas`). (`src/api/ablation_router.py`)
- **F-003:** Few-shot example banks (`few_shot_mapping.json`, `few_shot_cypher.json`) rewritten to an off-domain (aviation) set with zero overlap against any `gold_standard.json` fixture — eliminating gold-standard leakage into live mapping/Cypher prompts during eval. (`src/data/`, `tests/unit/test_few_shot.py`)
- **F-004:** `MENTIONS` edges now MATCH `:ParentChunk {parent_chunk_index}` instead of child `:Chunk {chunk_index}`, so BusinessConcepts link to the parent chunks triplets were actually extracted from. (`src/graph/build_nodes.py`, `src/graph/builder_graph.py`)
- **F-005:** `_record_failed_table()` writes `failed_mappings` at both retry-exhaustion points, so a table that fails mapping is recorded (not silently dropped) and the Pipeline-Health metric can report real failures. (`src/graph/validation_nodes.py`)
- **F-006:** `load_pdfs_batch` detects duplicate basenames and falls back to per-path loads, so same-basename PDFs are no longer merged into one bucket. (`src/ingestion/pdf_loader.py`)

### Medium (YELLOW)
- **F-007 / F-011:** `reconfigure_from_env()` now clears the cached embeddings/reranker singletons and calls `reset_observability()`, so runtime config changes take effect everywhere (Langfuse no longer stays silently off). (`src/config/llm_factory.py`)
- **F-008:** DDL parser resolves implicit-PK FK references (`REFERENCES table` without a column list) to `{table}.{fk_col}` on both column-level and table-level paths. (`src/ingestion/ddl_parser.py`)
- **F-009:** `critic_review` catches `TypeError` from non-dict JSON, restoring the approve-by-default safety net. (`src/mapping/validator.py`)
- **F-010:** `extract_triplets` guards `isinstance(data, dict)` before unpacking, honoring the reflection retry budget. (`src/extraction/triplet_extractor.py`)
- **F-012:** LLM-Cypher concept rename wrapped in `try/except ConstraintError` → logs and continues instead of aborting after partial writes. (`src/graph/build_nodes.py`)
- **F-013:** Attribute-node embeddings use `settings.embedding_batch_size` instead of a hardcoded 32. (`src/graph/build_nodes.py`)
- **F-014:** `coverage_rate` is now `None` (not `1.0`) for empty `expected_sources`, and `None` is filtered before averaging — on both eval paths. (`src/config/tracing.py`, `src/api/ablation_router.py`)
- **F-015:** RAGAS per-metric timeouts now yield `None` (not `0.0`); `_mean` skips `None`; the trace row flags `ragas_error="timeout"`. (`src/evaluation/ragas_runner.py`)
- **F-016:** Ablation report best/worst markers are computed via argmax/argmin from the data instead of hardcoded AB-10/AB-01. (`scripts/generate_ablation_report.py`)
- **F-017:** Added `set_global_seed()` (env `RANDOM_SEED`, default 42) called at CLI and API startup; corrected the "deterministic" wording (T=0.0 governs LLM sampling only, not GPU embedding/reranker numerics). (`src/config/config.py`, `scripts/run_pipeline.py`, `scripts/serve_api.py`)

### Low (GREEN)
- **F-018:** Heuristic extractor patterns compiled with `re.IGNORECASE` and matched against the original sentence, eliminating Unicode `.lower()` length-shift span corruption. (`src/extraction/heuristic_extractor.py`)

## ML Pipeline Changes

- **Data Pipeline:** de-contaminated few-shot bank (F-003); PDF basename-collision guard (F-006); implicit-FK resolution (F-008); Unicode-span fix (F-018).
- **Model / Graph Architecture:** correct `MENTIONS` provenance (F-004); `failed_mappings` accounting (F-005); rename constraint guard (F-012); config-driven Attribute batch size (F-013); reflection-loop error nets (F-009, F-010); complete cache invalidation (F-007/F-011).
- **Evaluation:** correct preset-ablation contracts (F-001, F-002); honest coverage averaging (F-014); RAGAS timeout handling (F-015); data-derived markers (F-016); global RNG seeding (F-017).

## Verification

- **Compile:** all 16 touched files OK (`py_compile`).
- **Lint:** all touched files ruff-clean.
- **Unit suite (`pytest tests/unit/ -m "not slow"`):** **514 passed**, 3 errors — all `fixture 'mocker' not found` in `test_llm_client.py` (missing `pytest-mock` plugin; file untouched by this change). Credential-bound `test_llm_factory.py` / `test_entity_resolver.py` tests pass with `OPENAI_API_KEY` set. **No regressions.**
- **Integration (Neo4j):** not run in this environment — run `pytest -m integration` against a live Neo4j before production rollout (F-004 / F-005 / F-012 touch DB write paths).
