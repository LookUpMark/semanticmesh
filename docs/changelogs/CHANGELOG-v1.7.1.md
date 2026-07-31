# Changelog — v1.7.1

**Date:** 2026-07-31
**Type:** Patch — slim runtime image + thesis summary

## Summary

Two maintenance changes on top of v1.7.0: (1) the Docker runtime image is slimmed by removing development-only dependencies and the editable install from the production build; (2) a standalone English thesis summary (3-page PDF) is added under `docs/overleaf/` for supervisor review and portal upload. No application source changes.

## What's new

- **`Dockerfile`** — builder stage now runs `pip install .` instead of `pip install -e ".[dev]"`. Drops the editable install and the `dev` extras (pytest, ruff, mypy, testcontainers) from the runtime image, which are unused at runtime. Image shrinks from 24.2 GB / 8.66 GB actual to 9.72 GB / 3.24 GB actual.
- **`docs/overleaf/summary.tex`** + **`summary.pdf`** — standalone English thesis summary, separate from `thesis.tex`. Three pages, grounded on the thesis chapters (evaluation results: v1.5.1). Covers context/problem, the five-capability gap no existing system fills, the two-graph architecture and implementation, evaluation (AI-Judge + ablation), key findings, limitations, and future work. Works cited by name (Collibra, GraphRAG, Self-RAG, RAGAS); no numeric citation markers.

## Verification

- **Slim image:** `docker build -t thesis-api:slim .` succeeds; `docker run … curl localhost:8000/health` → `{"status":"ok"}`; entrypoint imports (`src.api.app`, `scripts.serve_api`) OK under the non-editable install. `src/` confirmed to import no dev-only packages.
- **Unit:** 561 tests pass, zero regressions (Dockerfile and docs only — no source touched).
- **Summary:** `pdflatex summary.tex` → 3 pages, page 3 nearly full, no LaTeX errors.

## Files

- `Dockerfile` — modified (line 5: `pip install .`)
- `docs/overleaf/summary.tex` — new (standalone English summary source)
- `docs/overleaf/summary.pdf` — new (rendered deliverable)
- `docs/changelogs/CHANGELOG-v1.7.1.md` — new
- `pyproject.toml` — version `1.7.0` → `1.7.1`
