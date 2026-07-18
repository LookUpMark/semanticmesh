# HANDOFF

## Goal
Ship and document the SemanticMesh GraphRAG thesis project. The thesis is **complete and released** as **v1.5.6** (final polish with Italian summary). All three releases v1.5.4/v1.5.5/v1.5.6 are docs/thesis-only patches building on v1.5.1 code behavior. 530 unit tests pass.

## Current state
- **Branch `dev` = `origin/dev` = `main` = `origin/main` = `2442fd5`, clean, fully pushed.** Tags `v1.5.4`, `v1.5.5`, `v1.5.6` are HEAD.
- **Release v1.5.6 live**: https://github.com/LookUpMark/semanticmesh/releases/tag/v1.5.6 (Italian summary completion, thesis multilingual front matter complete)
- **Release v1.5.5 live**: https://github.com/LookUpMark/semanticmesh/releases/tag/v1.5.5 (9 minor citations + 5 new tables + data grounding fixes)
- **Release v1.5.4 live**: https://github.com/LookUpMark/semanticmesh/releases/tag/v1.5.4 (4 missing citations + abstract + biber-resolved build)
- **Thesis builds clean**: `latexmk` → **79 pages**, 0 undefined citations, 0 `[?]` in `thesis.pdf`
- **Front matter complete**: English abstract (`content/abstract.tex`) + Italian summary (`content/summary.tex`) both integrated in build
- **`.gitignore` hardened**: LaTeX build artifacts, local utility scripts, uv lock ignored
- **Prior releases intact**: v1.5.2 (doc alignment), v1.5.3 (thesis audit + ch6), v1.5.4 (citations + abstract)
- **Code is at v1.5.1 behavior** — v1.5.2/v1.5.3/v1.5.4/v1.5.5/v1.5.6 are docs/thesis-only releases. 530 unit tests pass.

## Files touched
- `docs/changelogs/CHANGELOG-v1.5.6.md` — release notes (Italian summary completion)
- `docs/changelogs/CHANGELOG-v1.5.5.md` — release notes (9 minor citations + 5 tables + data grounding)
- `docs/overleaf/bibliography.bib` — +14 entries (4 significant from v1.5.4 + 9 minor from v1.5.5): BM25, CQRS, GPT-4, LangChain, PEFT/LoRA, sqlglot, gpt-5.4-nano, Collibra, Alation
- `docs/overleaf/content/chapters/chapter1.tex` — citazioni CQRS, BM25, Collibra/Alation + tabella Summary of Contributions
- `docs/overleaf/content/chapters/chapter2.tex` — citazione GPT-4 per MT-Bench
- `docs/overleaf/content/chapters/chapter3.tex` — citazioni LangChain, sqlglot (3 occorrenze)
- `docs/overleaf/content/chapters/chapter4.tex` — tabella Builder Components (file paths corretti), tabella REST API Endpoints
- `docs/overleaf/content/chapters/chapter5.tex` — tabella Key Findings from Ablation Study (claim precision migliorata), citazione gpt-5.4-nano (3 occorrenze)
- `docs/overleaf/content/chapters/chapter6.tex` — tabella AB-BEST Evaluation Results (dati DS02/DS04/DS05 corretti), citazione PEFT/LoRA, Unicode fix (≈ → $\approx$)
- `docs/overleaf/content/summary.tex` — Italian summary written from scratch (150 words, grounded su v1.5.1 results)
- `docs/overleaf/thesis.tex` — uncommented Italian summary environment (lines 71–77)
- `docs/overleaf/common/packages.tex` — added `\usepackage{float}` for `[H]` placement specifier
- `.gitignore` — hardened with LaTeX build artifacts, local utility scripts, uv lock patterns

## Decisions made
- **No `Co-Authored-By` in any commit** — permanent user rule; saved to memory (`no-commit-coauthor.md`)
- **9 minor citations added via separate bib entries** — decisione di documentare anche citazioni minor (vendor products, model releases) per completezza bibliografica
- **Table placement forced with `[H]`** — decisione di forzare rendering nel punto esatto con `[H]` invece di `[htbp]` per evitare float separation, costo -1 pagina ma placement corretto
- **Italian summary integrated in build** — decisione de-commentare `\sommario` environment per completare front matter multilingue
- **Data grounding corrections applied** — DS02 (4.70), DS04 (4.45), DS05 (4.45) corrected in results table; builder component file paths corrected; ER threshold claims precision-improved
- **Local utility scripts removed from version control** — `run_remainder.sh`, `run_remainder_linux.sh`, `uv.lock` untracked ma mantenuti in filesystem per uso locale

## Constraints
- **`biber` is not on the default PATH.** Build cmd: `PATH="/usr/bin/vendor_perl:$PATH" latexmk -pdf -interaction=nonstopmode thesis.tex` (from `docs/overleaf/`)
- **`latexmk` caches a failed `biber` run in `.fdb_latexmk`.** If it loops on "gave an error in previous invocation", run `latexmk -C thesis.tex` first, then rebuild
- **`.gitignore` applies to new files only.** `run_remainder.sh`, `run_remainder_linux.sh`, `uv.lock` were already tracked; required `git rm --cached` + commit to untrack them
- **AI Judge scores live in `ai_judge.md` (markdown), not the bundle JSON** `score` field.** Parse regex: `\*\*Overall\*\.*?\*\*([0-5]\.\d{1,2})\*\*`
- **`run_ai_judge.py --all`** discovers only AB-01..AB-20 × DS01-06 by default; pass explicit `--studies` (AB-00, AB-BEST, AB-BEST-K20) and `--datasets` (incl. 07) for full coverage
- **Each pipeline run clears the Neo4j graph (`--clear-graph=True`)**; container `thesis-neo4j` is down by default, `--auto-neo4j` restarts it
- **Thesis written in English; Italian summary added for multilingual front matter**
- **Pushing to `main` and creating a release trips the auto-mode safety classifier** unless the user has explicitly confirmed in-turn. Single-purpose commands (`git push origin dev`, then `git push origin dev:main`, then `gh release create`); compound bash is denied.

## Attempts and failures
- **D2 minor citations initially omitted** — Outcome: added in v1.5.5. Lesson: D2 audit flagged them as "minor" but still important for completezza bibliografica.
- **Table data not grounded in first draft** — DS02 (4.48→4.70), DS04 (4.20→4.45), DS05 (4.28→4.45) were incorrect. Outcome: corrected against `docs/ablation/RESULTS.md`. Lesson: always verify numbers against primary data sources.
- **Builder component file paths incorrect** — `extraction_node.py`, `entity_resolver.py`, `enrichment_node.py`, etc. didn't match `src/` structure. Outcome: corrected with actual paths from `find` command. Lesson: tool-generated paths may be outdated.
- **Unicode character `≈` caused LaTeX error** — not supported in default font encoding. Outcome: replaced with `$\approx$`. Lesson: use LaTeX math mode for special characters.
- **Tables floating away from insertion point** — `[htbp]` placement caused tables to render pages away from citation. Outcome: added `\usepackage{float}` and used `[H]` specifier for exact placement. Lesson: `[H]` is more restrictive but guarantees positioning.
- **Page count decreased from 79 to 78 with `[H]`** — placement forcing reduced vertical space optimization. Outcome: accepted trade-off for correct positioning. Final count: 79 pages after Italian summary addition.

## Open issues
None — thesis is complete, documented, and released. All audit recommendations from D1/D2 have been addressed or documented as intentional omissions.

## Next exact steps
No next steps — thesis v1.5.6 is complete. Optional future work (not immediate):
- Write Italian summary if front-office requires it (NOW COMPLETED in v1.5.6)
- Add more tables/diagrams if page count needs further increase (79 pages is sufficient)
- Merge `dev` → `main` and create release (COMPLETED in v1.5.6)

## Commands / checks
- **Build thesis:** `cd docs/overleaf && PATH="/usr/bin/vendor_perl:$PATH" latexmk -pdf -interaction=nonstopmode thesis.tex`
- **Verify PDF:** `pdftotext thesis.pdf - | grep -c '\[?\]'` (should be 0), `grep -c "Citation.*undefined" thesis.log` (should be 0)
- **Unit suite:** `.venv/bin/python -m pytest tests/unit/ -m "not slow" -q` (530 passed)
- **Git sync check:** `git status --short && git log --oneline -3 && git rev-list --count origin/dev..dev` (clean / 0)
- **Verify releases:** `gh release list` (expect v1.5.4, v1.5.5, v1.5.6 at top)

## References
- commit `2442fd5` — v1.5.6: Italian summary completion + .gitignore cleanup (tag `v1.5.6`, HEAD)
- commit `6630842` — docs(thesis): v1.5.6 — Italian summary completion (parent of 2442fd5)
- commit `c1d5376` — docs(thesis): v1.5.5 — minor citations polish + 5 new tables + data grounding fixes (tag `v1.5.5`)
- commit `2f52656` — docs(thesis): v1.5.4 — add 4 missing citations + write abstract (biber-resolved) (tag `v1.5.4`)
- GitHub release: https://github.com/LookUpMark/semanticmesh/releases/tag/v1.5.6
- Memory: `no-commit-coauthor.md` (commit rule), `thesis-build-biber-path.md` (biber PATH workaround)
- `docs/audits/AUDIT-2026-07-17-thesis.md` — full D1 (code-grounding) + D2 (citation) audit report
- `docs/changelogs/CHANGELOG-v1.5.6.md`, `CHANGELOG-v1.5.5.md`, `CHANGELOG-v1.5.4.md` — release notes
