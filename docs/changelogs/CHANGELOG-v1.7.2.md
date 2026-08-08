# Changelog — v1.7.2

**Date:** 2026-08-08
**Type:** Patch — Italian thesis sommario aligned to the English abstract

## Summary

Docs-only release. The Italian summary (sommario) inside the thesis is rewritten as a clean, faithful equivalent of the English abstract — same three-paragraph structure, same key results, no anglicisms. No application source changes.

## What's new

- **`docs/overleaf/content/summary.tex`** — the Italian sommario was a standalone write-up with anglicisms (e.g. "bridging il gap") and did not mirror the English abstract. Rewritten to match `content/abstract.tex` in structure and content: semantic-gap problem; two-graph CQRS architecture (Builder/Query), two-stage entity resolution, three self-reflection loops, hybrid retrieval with reciprocal rank fusion; evaluation (7 datasets, 111 tables, 210 questions, AI-Judge; AB-BEST 210/210 grounded, 4.31/5) including the two ablation findings (baseline indistinguishable; recall decoupled from quality, $k{=}5$ vs $k{=}20$). Fits one page, parallel to the English abstract.

## Verification

- **Build:** `pdflatex` + `biber` (clean pass) → 0 LaTeX errors, 0 undefined refs/citations; thesis PDF rebuilt, sommario renders on a single page.
- **Unit:** 561 tests unchanged — docs-only change, no `src/` or `tests/` files touched.

## Files

- `docs/overleaf/content/summary.tex` — rewritten (5 insertions, 10 deletions)
- `docs/changelogs/CHANGELOG-v1.7.2.md` — new
- `pyproject.toml` — version `1.7.1` → `1.7.2`
