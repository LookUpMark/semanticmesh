# Changelog - v1.0.3

**Date:** 2026-04-22

## Summary

Full ablation study campaign completed (AB-00 -> AB-20 + AB-BEST on DS01). PDF ingestion was migrated to the native LangChain `langchain-opendataloader-pdf` integration. Test coverage was expanded with 6 new test files covering API endpoints, auth, jobs, schema validation, PDF loader integration, and settings override, bringing the suite to 468+ passing tests. All ablation test correctness issues were fixed.

---

## Changes

### Evaluation - Ablation Campaign

- Ran all 22 ablation studies (AB-00 -> AB-20 + AB-BEST) on DS01 (`01_basics_ecommerce`).
  Each study produced: `evaluation_bundle.json`, `run.json`, `analysis.md`, `ai_judge.md`, per-question CSV, summary CSV, and 3 thesis-ready plots (`coverage_by_difficulty`, `gt_coverage_bar`, `retrieval_score_dist`).
- Updated `docs/ablation/RESULTS.md` with final AI-Judge verdicts and per-dimension winner analysis for all 22 conditions.
- Updated `src/evaluation/ablation_runner.py`: AB-BEST configuration updated with data-driven optimal settings derived from AI-Judge analysis on DS01:
  - Hybrid retrieval, reranker ON `top_k=20`
  - Chunk size 128/16, parent 512/64
  - ER threshold 0.65, blocking `top_k=5`
  - HITL confidence 0.85
  - Hallucination grader OFF
- Deleted intermediate finance dataset files and associated plots (cleanup).

### Ingestion - PDF Loader Migration

- `src/ingestion/pdf_loader.py`: Migrated from `opendataloader-pdf` (manual JSON parsing via temp directory) to the native LangChain integration `OpenDataLoaderPDFLoader`. Removed `_parse_odl_json()`, `_SKIP_TYPES`, `import tempfile`, and `import json`. Added `_lc_docs_to_documents()` helper. All loaders now use `format="markdown"` to preserve heading hierarchy for hierarchical splitting.
- `pyproject.toml`: Replaced `"opendataloader-pdf>=0.1"` with `"langchain-opendataloader-pdf>=2.0"`.

### Tests - New Coverage

Six new test files were added:

| File | Tests | Coverage |
|------|------:|---------|
| `tests/integration/test_api_endpoints.py` | 21 | Health, Auth (401/403/429), Config GET/POST, Query endpoint, Jobs lifecycle, `PipelineConfig` validation, ablation matrix/datasets |
| `tests/integration/test_settings_override.py` | 5 | Settings singleton, reload, env-var override, `_settings_override` context manager |
| `tests/integration/test_pdf_loader_integration.py` | 5 | PDF -> hierarchical chunks flow, batch source metadata, mixed PDF+Markdown, edge cases |
| `tests/unit/test_schemas_validation.py` | 21 | `Document`, `Chunk`, `Triplet` (confidence bounds), `GraderDecision` (action enum), `RetrievedChunk` (source_type), `PipelineConfig` (temperature/tokens/retrieval_mode/vector_top_k) |
| `tests/unit/test_jobs.py` | 8 | Job CRUD, full lifecycle, `set_failed`, thread safety (50 concurrent creates) |
| `tests/unit/test_auth.py` | 7 | API key auth, rate limiting after 5 failures, IP-isolated counters, constant-time comparison |

### Tests - Existing Test Fixes

- `tests/unit/test_pdf_loader.py`: Replaced `TestParseOdlJson` with `TestLcDocsToDocuments`; all mocks were updated from `patch("...opendataloader_pdf.convert")` to `patch("...OpenDataLoaderPDFLoader")`. 23/23 passing.
- `tests/evaluation/test_ablation.py`: Fixed 4 correctness issues:
  1. `test_cache_cleared_after_block` - switched from miss-count comparison to object-identity check; `lru_cache.cache_clear()` resets counters to 0.
  2. `test_returns_dict_of_floats` - used `side_effect` (fresh dict copy per call) to prevent `_ZERO_METRICS` in-place mutation; added `_RAGAS_KEYS` snapshot.
  3. `test_env_override_applied_during_run` - fixed `capture_metrics` signature to accept `run_ragas=` kwarg.
  4. `test_all_experiments_run_without_error` - added `patch(_PATCH_BUILDER, ...)` so all 22 studies validate routing logic without real LLM/Neo4j calls.

### Dependency Update

- `pyproject.toml`: `"opendataloader-pdf>=0.1"` -> `"langchain-opendataloader-pdf>=2.0"`

---

## Files Changed

| Action | File |
|--------|------|
| Added | `docs/changelogs/CHANGELOG-v1.0.3.md` |
| Added | `tests/integration/test_api_endpoints.py` |
| Added | `tests/integration/test_settings_override.py` |
| Added | `tests/integration/test_pdf_loader_integration.py` |
| Added | `tests/unit/test_schemas_validation.py` |
| Added | `tests/unit/test_jobs.py` |
| Added | `tests/unit/test_auth.py` |
| Added | `outputs/ablation/AB-{00..20,BEST}/...` (ablation run artefacts) |
| Modified | `src/ingestion/pdf_loader.py` |
| Modified | `src/evaluation/ablation_runner.py` |
| Modified | `tests/unit/test_pdf_loader.py` |
| Modified | `tests/evaluation/test_ablation.py` |
| Modified | `docs/ablation/RESULTS.md` |
| Modified | `pyproject.toml` (dependency + version bump to 1.0.3) |
| Modified | `.gitignore` |

---

## Verification

- Unit tests: 468 passed, 0 failed (excluding Docker-dependent integration tests)
- `tests/evaluation/test_ablation.py`: 8/8 fast tests passing; 3 real-builder integration tests passing with Neo4j running
- All ablation artefacts verified: 22 x `evaluation_bundle.json` present, AI-Judge complete
- Dependency install: `langchain-opendataloader-pdf==2.0.0` confirmed