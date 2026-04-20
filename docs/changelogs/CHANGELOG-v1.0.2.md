# Changelog — v1.1.0

**Date:** 2026-04-17

## Summary

Refactored `scripts/` directory: consolidated three redundant scripts into two unified, modular runners. Added `ABLATION_DESC` metadata to `ablation_runner.py` as single source of truth. AI Judge now uses the project's `make_llm()` factory instead of raw OpenAI client. Net reduction: **1559 lines deleted, 293 lines added**.

## Changes

### Scripts

- **Added `scripts/run_pipeline.py`:** Unified pipeline runner replacing `run_ab00.py` + `run_ablation_full.py`. Supports `--study`, `--studies`, `--all-studies`, `--best`, `--dataset`, `--datasets`, `--all-datasets`, `--no-builder`, `--ragas`, `--lazy`, `--smoke`, `--max-samples`, `--auto-neo4j`, `--output-dir`. Output standardised to `outputs/ablation/{study_id}/datasets/{dataset_id}/`.
- **Rewrote `scripts/run_ai_judge.py`:** Uses `make_llm()` from `src.config.llm_factory` instead of raw `openai.OpenAI`. Added `--all` mode (auto-discovers un-judged bundles, replaces `run_judge_all.sh`). Added `--studies`, `--datasets` filters and `--force` flag.
- **Cleaned `scripts/generate_ablation_report.py`:** Removed 170-line `ABLATION_DESC` dict — now imports from `src/evaluation/ablation_runner.py`. Added `argparse`, `sys`, and `ROOT` path setup for proper module resolution.
- **Deleted `scripts/run_ab00.py`** (724 lines) — merged into `run_pipeline.py`.
- **Deleted `scripts/run_ablation_full.py`** (823 lines) — merged into `run_pipeline.py`.
- **Deleted `scripts/run_judge_all.sh`** (47 lines) — functionality moved to `run_ai_judge.py --all`.

### Source Code

- **Extended `src/evaluation/ablation_runner.py`:** Added `ABLATION_DESC` dict with extended metadata (title, group, hypothesis, affected_components) for all 22 studies (AB-00 through AB-20 + AB-BEST). Single source of truth for ablation study metadata.

### Configuration

- **Updated `pyproject.toml`:** New entry points: `pipeline-run = "scripts.run_pipeline:main"`, `ai-judge = "scripts.run_ai_judge:main"`. `ablation-run` kept as backward-compat alias for `pipeline-run`.

### Documentation

- **Updated `CLAUDE.md`:** CLI entry points, project structure tree, and Scripts section updated to reflect new script names and CLI flags.
- **Updated `README.md`:** Ablation CLI examples updated to use `run_pipeline.py`.
- **Updated `docs/draft/ABLATION.md`:** References to `run_ablation_full.py` updated to `run_pipeline.py`.

## Files Changed

| Action | File |
|--------|------|
| New | `scripts/run_pipeline.py` |
| Deleted | `scripts/run_ab00.py`, `scripts/run_ablation_full.py`, `scripts/run_judge_all.sh` |
| Modified | `scripts/run_ai_judge.py`, `scripts/generate_ablation_report.py`, `src/evaluation/ablation_runner.py` |
| Modified | `pyproject.toml`, `CLAUDE.md`, `README.md`, `docs/draft/ABLATION.md` |

## Verification

- Unit tests: PASSED (362 tests, 0 failures)
- All CLI `--help` outputs verified
- Syntax: all Python files parse correctly
- Stale references: none (`grep` clean)
