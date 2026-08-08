# Changelog — v1.7.4

**Date:** 2026-08-08
**Type:** Patch — unified front-matter styling (abstract / riassunto / ringraziamenti)

## Summary

Docs-only release. The thesis front-matter text sections (English abstract, Italian riassunto, ringraziamenti) are given a single consistent typographic style, the Italian section titles are corrected, and a blank page is added between the riassunto and the ringraziamenti. No application source changes.

## What's new

- **Unified heading style** — the English abstract previously used the centered `abstract` environment; it now uses a `\chapter*{Abstract}` heading, matching the left-aligned chapter headings already used by the riassunto (`\sommario`) and the ringraziamenti (`\ringraziamenti`). All three front-matter sections now share the same heading style.
- **Unified body style** — the abstract (`content/abstract.tex`) and the riassunto (`content/summary.tex`) bodies are wrapped in the same locally-scoped block style already used by the acknowledgements: zero `\parindent` with `\parskip = \baselineskip` inside a `\begingroup`/`\endgroup`, so paragraphs are flush-left with a blank line between them. The change does not leak into the rest of the thesis.
- **Italian section titles** — the Italian summary was rendered as "Summary" (the document language is English); it is now "Riassunto" via an Italian `\summaryname` caption override (`common/new_commands.tex`) and a `\italiano`/`\english` language wrap around the section (correct title + Italian hyphenation). The ringraziamenti heading likewise changes from "Acknowledgements" to "Ringraziamenti" (Italian caption + `\italiano`).
- **Blank page** — a `\paginavuota` is inserted between the riassunto and the ringraziamenti (the previous `\cleardoublepage` produced no blank page under `oneside`). The front-matter now alternates content / blank page consistently (also after the abstract and before the Table of Contents).

## Verification

- **Build:** nuclear-clean manual passes (`pdflatex` → `biber` → `pdflatex` → `pdflatex`, `biber` in `/usr/bin/vendor_perl`) → 0 LaTeX errors, 0 undefined references/citations, 85 pages. Rendered PDF checked: `Abstract` (EN) on its page, `Riassunto` (IT) with a blank page after it, `Ringraziamenti` (IT) on the following page.
- **Unit:** 561 tests unchanged — docs-only change, no `src/` or `tests/` files touched.

## Files

- `docs/overleaf/thesis.tex` — front-matter: `\chapter*{Abstract}`, `\italiano`/`\english` wraps, `\paginavuota` between riassunto and ringraziamenti
- `docs/overleaf/common/new_commands.tex` — Italian `\summaryname` → "Riassunto"
- `docs/overleaf/content/abstract.tex` — body wrapped in block style
- `docs/overleaf/content/summary.tex` — body wrapped in block style
- `docs/changelogs/CHANGELOG-v1.7.4.md` — new
- `pyproject.toml` — version `1.7.3` → `1.7.4`
