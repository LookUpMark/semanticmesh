# Changelog — v1.5.2

**Date:** 2026-07-17
**Type:** Patch — documentation alignment to the v1.5.1 codebase and re-judged results (no behavior change)

## Summary

Aligns all human-facing documentation with the current code (v1.5.1: dual retrieval metrics, langfuse v3 observability) and the 2026-07-17 re-judge of all 35 evaluation bundles by the systematic AI Judge (`gpt-5.4-nano-2026-03-17`). The headline correction is the public `README.md` evaluation section, which still carried pre-v1.5.1 manual-judge figures (5.00/5, AB-BEST 4.73 average) and two superseded conclusions ("K5 wins 6/7", "schema/actor-critic are critical safety nets"). No source-code behavior changes; this release makes the docs honest about the lower, more compressed v1.5.1 scores.

## Documentation Changes

### README.md
- **Evaluation Results (AB-BEST) table rewritten** on the v1.5.1 per-dataset scores: DS01 4.50, DS02 4.70, DS03 3.65, DS04 4.45, DS05 4.45, DS06 4.25, DS07 4.20 — average **4.31/5** (down from the stale 4.73 manual figure). Added the GT-coverage column and the v1.5.1 note explaining the stricter systematic judge and stochastic KG builds.
- **Ablation Campaign table rewritten** with representative DS01 v1.5.1 scores: AB-06 (chunking 128/16) best at 4.80, AB-19 (Cypher healing OFF) worst at 3.80, AB-00 baseline 4.50 (was incorrectly 4.25).
- **Key findings rewritten** (5 bullets): removed the false "K5 validated across all 7 datasets — K5 wins 6/7" and "Schema enrichment and Actor-Critic are critical safety nets — drops GT coverage ≥33 pp". Replaced with the v1.5.1 reading: hybrid retrieval stays robust (BM25-only collapses GT to 54%); no single parameter discriminates on the simple DS01 baseline (judge compressed 3.80–4.80); `top_k=5` is the efficient optimum (ties K20 at 4.31 vs 4.28 with 4× fewer cross-encoder calls); schema enrichment and Actor-Critic are kept ON for robustness on degraded/larger schemas, not for DS01 quality (GT stays 98% with either off — the earlier ≥33 pp collapse was a pre-v1.5.1 artefact); Cypher healing is the one component the judge still penalises on DS01.
- **Version references** bumped: changelog range `v1.0.0 → v1.4.2` → `v1.0.0 → v1.5.1` (two occurrences).

### pyproject.toml
- **`version` 1.4.2 → 1.5.2.** The pin was stale: the code has been at v1.5.1 behavior (dual retrieval metrics, langfuse v3) since the v1.5.1 ML-audit + ablation re-run, but the version string was never advanced past 1.4.2.

### docs/draft/ABLATION.md
- Added a top **superseded banner**: this file is the ablation *plan* (methodology, study matrix, configuration flags); the authoritative *current results* live in `docs/ablation/RESULTS.md` (re-run on v1.5.1, re-judged 2026-07-17). The v1.0.x / v1.1.1 score tables preserved in §6 are marked historical, not current.

### docs/audits/AUDIT-2026-05-29.md
- **AUDIT-025 (langfuse version range)** annotated with its v1.5.1 resolution. The audit suggested tightening to `langfuse>=2.0,<3.0`; v1.5.1 instead adopted `langfuse>=3.0,<4.0` because langfuse 2.x is incompatible with langchain 1.x regardless of import path (v2 imports `langchain.callbacks.base`, removed in 1.x). Cross-references `src/config/observability.py:49` and `pyproject.toml:49`.

## Verification

- **Stale-claim sweep:** `grep` for `wins 6/7`, `critical safety net`, `drops GT coverage ≥33 pp`, `4.73`, `5.00`, `4.90`, `3.40` across `README.md`, `docs/overleaf/content/`, `docs/ablation/RESULTS.md` — the only remaining hits are inside `RESULTS.md` where the text explicitly states the earlier reading *does not hold* on v1.5.1 (honest corrections, not stale claims).
- **Thesis chapters checked clean:** `chapter1.tex` (contributions), `chapter5.tex` (Evaluation — already aligned to v1.5.1 in a prior commit, including the new `sec:eval:topk_sensitivity` and `sec:eval:dual_metrics` subsections), `chapter6.tex` (Conclusions) — no stale scores or superseded claims.
- **Bundle/judge counts:** 35 `evaluation_bundle.json` + 35 `ai_judge.md` confirmed present; spot-checked bundles carry `grounded_rate=1.0` and dual retrieval metrics.
- **No code behavior change:** no `src/` file touched in this release; `pytest` suite unaffected.

## Known follow-ups (not in this release)

- `docs/overleaf/content/abstract.tex` is empty and `summary.tex` is still Lorem ipsum — the thesis abstract is unwritten (content gap, not a drift issue).
- Git tag `v1.5.1` was never created; this release tags the line as `v1.5.2`.
- Local `main` branch is orphaned from `origin/main` (no common ancestor); the release fast-forwards `origin/main` to `dev` via `git push origin dev:main` and repoints local `main` afterward.
