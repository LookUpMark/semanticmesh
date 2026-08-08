# Changelog — v1.7.3

**Date:** 2026-08-08
**Type:** Patch — final Italian thesis acknowledgements

## Summary

Docs-only release. The thesis acknowledgements (`\ringraziamenti`) section, previously a Lorem-ipsum placeholder, is replaced with the complete, final Italian text. No application source changes.

## What's new

- **`docs/overleaf/content/acknowledgements.tex`** — the Lorem-ipsum placeholder is replaced with the full acknowledgements text, in Italian. In order: supervisor (Prof.\ Paolo Garza); company tutor (Marco Bartolini, Data Reply); Politecnico di Torino (the difficulty, anxiety and weight of every exam as a forge for resilience); former Unikore colleagues --- the "Gentlemen" (Vito, Zaf, Gab, Filippo) and Giovanni; friends from high school (Filippo, Giuseppe, Francesco), the Turin circle (Christian \& Elsa, childhood friend Viviana, the Borsellino residence, Pietro \& Carmine, and the close-knit Giada/Samuele/Nicolò), and childhood friends (Marco, Giorgia, Giovanni, Silvana); the Lopez family with a remembrance of those no longer here; in-laws (Enza, Roberto, Chiara) and relatives (Teresa, Dino, Andrea, Riccardo); grandparents (Giuseppe, Cettina); partner Giulia (eight years together, future shared in Turin); and parents, with the thesis dedication and an anecdote on their unconditional support. A closing reflection declines the classic self-thanking, followed by a forward look at the first role as \emph{Machine Learning Engineer} at the Intesa Sanpaolo tower. Paragraph spacing is scoped locally (zero `\parindent`, `\parskip = \baselineskip` inside a `\begingroup`/`\endgroup`) so each acknowledgement is visually separated without affecting the rest of the thesis.

## Verification

- **Unit:** 561 tests unchanged --- docs-only change, no `src/` or `tests/` files touched.
- **Thesis PDF** (`thesis.pdf`, gitignored, rebuilt locally): not rebuilt for this release. The `.tex` uses only standard LaTeX commands and compiles within the existing `\ringraziamenti` environment; rebuild with the nuclear-clean manual-pass sequence when a rendered PDF is needed.

## Files

- `docs/overleaf/content/acknowledgements.tex` — placeholder replaced with final text (+45/-2)
- `docs/changelogs/CHANGELOG-v1.7.3.md` — new
- `pyproject.toml` — version `1.7.2` → `1.7.3`
