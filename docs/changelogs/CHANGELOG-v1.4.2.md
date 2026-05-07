# Changelog — v1.4.2

**Date:** 2026-05-07

## Summary

Documentation consistency patch — fixed 40+ inconsistencies across 8 markdown files. No code changes.

## Changes

### Documentation (Critical)

- **Updated LLM model names in README.md and RUNNING_SERVICES.md**: `gpt-4.1` / `gpt-4.1-nano` → `gpt-5.4-nano-2026-03-17` / `gpt-5-nano-2025-08-07`. These user-facing docs showed model names from two generations ago.
- **Fixed changelog version range in README.md**: `v1.0.0 → v1.2.0` → `v1.0.0 → v1.4.1` (project structure section) and `v1.0.0 → v1.4.0` → `v1.0.0 → v1.4.1` (documentation table).

### Documentation (Data Integrity)

- **Fixed AB-BEST-K20 average calculation** in `docs/ablation/RESULTS.md` and `docs/changelogs/CHANGELOG-v1.4.0.md`: K20 average was reported as 4.53 but actual arithmetic mean of (4.65+4.60+4.35+4.65+4.80+4.90+3.65)/7 = **4.51**. Delta corrected from -0.20 to **-0.22**. Propagated to README.md.
- **Fixed AB-00 default column in RESULTS.md Section 4**: `reranker_top_k` was listed as 20 (should be 10, the baseline default at time of run); `HITL threshold` was listed as 0.80 (should be 0.90, the code default — 0.80 is the AB-BEST override).
- **Fixed Section 3.3 stale reference**: Text said "top_k=20 reranker pool" for AB-BEST but AB-BEST uses top_k=5.

### Documentation (Design Docs Alignment)

- **`docs/draft/REQUIREMENTS.md`**: `reranker_top_k` default 10→5; `.env` example block: `CHUNK_SIZE` 512→256, `CHUNK_OVERLAP` 64→32, `ER_SIMILARITY_THRESHOLD` 0.85→0.75; US-02-02 story text aligned with actual defaults; removed non-existent `notebooks/` from project structure; updated model name examples.
- **`docs/draft/ADR.md`**: `er_similarity_threshold` default 0.85→0.75 in ADR-11.
- **`docs/draft/ABLATION.md`**: Updated from 6 to 7 datasets with correct fixture directory names; 126→147 runs; `reranker_top_k` default 10→5; model names aligned; AI Judge model updated.
- **`docs/draft/SPECS.md`**: LLM factory tier table model names aligned with `src/config/config.py`.

## Migration Notes

- No breaking changes. Documentation-only release.
- Study guide files (gitignored) also updated on disk.
