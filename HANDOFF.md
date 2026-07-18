# HANDOFF

## Goal
Ship and document the SemanticMesh GraphRAG thesis project at code v1.5.1. The thesis-side work (audit, citation completion, abstract, biber-resolved build) is now complete and released as **v1.5.4**. Remaining work is optional polish (minor citations, Italian summary).

## Current state
- **Branch `dev` = `origin/dev` = `main` = `origin/main` = `2f52656`, clean, fully pushed.** Tag `v1.5.4` is HEAD.
- **Release v1.5.4 live:** https://github.com/LookUpMark/semanticmesh/releases/tag/v1.5.4 (thesis bibliography completion + abstract + biber-resolved build; docs-only, no `src/` runtime change).
- **4 significant missing citations resolved** (the D2 audit recs): `cobbe2021gsm8k`, `yang2018hotpotqa`, `thorne2018fever`, `xiao2023cpack` added to `bibliography.bib` and `\cite{}`-d in ch2 (GSM8K, HotpotQA+FEVER) and ch3 (bge-reranker-v2-m3 / C-Pack).
- **Thesis abstract written** (`content/abstract.tex`, English, grounded on v1.5.1 results) and the `abstract` env uncommented in `thesis.tex:57-59`.
- **`biber` is installed and works** — binary in `/usr/bin/vendor_perl/biber` (NOT on default PATH). Build now resolves all citations.
- **Thesis builds clean:** `latexmk` → **74 pages, 0 undefined citations, 0 `[?]`** in `thesis.pdf`.
- **`.gitignore` hardened** with LaTeX glossaries/beamer/synctex patterns (the thesis `\input`s `glossaries.tex`).
- **Prior releases intact:** v1.5.2 (doc alignment), v1.5.3 (thesis audit + ch6). `v1.5.1` tag was never created (version line jumped v1.5.0 → v1.5.2).
- **Code is at v1.5.1 behaviour** — v1.5.2/v1.5.3/v1.5.4 are docs/thesis-only releases. 530 unit tests pass.

## Files touched
- `docs/overleaf/bibliography.bib` — +4 entries (GSM8K, HotpotQA, FEVER, C-Pack).
- `docs/overleaf/content/chapters/chapter2.tex` — cite GSM8K (§Reasoning), HotpotQA+FEVER (§Agentic RAG).
- `docs/overleaf/content/chapters/chapter3.tex` — cite bge-reranker-v2-m3 (§Query Phase 2).
- `docs/overleaf/content/abstract.tex` — final English abstract written (was 1-line placeholder).
- `docs/overleaf/thesis.tex` — uncommented `abstract` env (lines 57-59).
- `.gitignore` — LaTeX glossaries/beamer/synctex build-artifact patterns.
- `docs/changelogs/CHANGELOG-v1.5.4.md` — release notes (new).
- `HANDOFF.md` — this file.

## Decisions made
- **No `Co-Authored-By` in any commit, ever** — permanent user rule; saved to memory (`no-commit-coauthor.md`). Overrides the default Claude Code trailer convention.
- **Cite bge-reranker-v2-m3 via `xiao2023cpack` (C-Pack paper)** — the model is introduced there; that is the canonical citable source, not a model-card URL.
- **Release v1.5.4 = docs/thesis-only** — kept separate from any future code bump so the patch is independently revertable, matching the v1.5.2/v1.5.3 split convention.
- **`gh release create v1.5.4` uses the tag, not `--target main`** — the tag already points at `2f52656`; targeting the branch would have pinned the release to the wrong ref if main lagged.
- **`.gitignore` gained glossaries patterns** — `glossaries.tex` is already `\input`; if `\makeglossaries` is ever enabled, `.glg/.gls/.acr` etc. would otherwise leak into the tree.
- **biber invoked via `PATH="/usr/bin/vendor_perl:$PATH"`** — the Arch `biber` package installs there but it is not on the session PATH; persisted to memory (`thesis-build-biber-path.md`).

## Constraints
- **`biber` is not on the default PATH.** Build cmd: `PATH="/usr/bin/vendor_perl:$PATH" latexmk -pdf -interaction=nonstopmode thesis.tex` (from `docs/overleaf/`).
- **`latexmk` caches a failed `biber` run in `.fdb_latexmk`.** If it loops on "gave an error in previous invocation", run `latexmk -C thesis.tex` first, then rebuild.
- **HANDOFF.md is BOTH tracked and gitignored.** The `.gitignore` entry (`HANDOFF.md`, line ~111) is inert because the file is already tracked — so edits to HANDOFF.md DO show up in `git status` and must be committed. To actually stop tracking it, `git rm --cached HANDOFF.md` first.
- **AI Judge scores live in `ai_judge.md` (markdown), not the bundle JSON `score` field.** Parse regex: `\*\*Overall\*\*.*?\*\*([0-5]\.\d{1,2})\*\*`.
- **`run_ai_judge.py --all`** discovers only AB-01..AB-20 × DS01-06 by default; pass explicit `--studies` (AB-00, AB-BEST, AB-BEST-K20) and `--datasets` (incl. 07) for full coverage.
- Each pipeline run clears the Neo4j graph (`--clear-graph=True`); container `thesis-neo4j` is down by default, `--auto-neo4j` restarts it.
- Thesis is written in English; conversation with the user is in Italian + caveman mode.
- **Pushing to `main` and creating a release trip the auto-mode safety classifier** unless the user has explicitly confirmed in-turn. Single-purpose commands (`git push origin dev`, then `git push origin dev:main`, then `gh release create`); compound bash is denied.

## Attempts and failures
- **`git push origin dev:main` + `gh release create` denied by classifier (first attempt)** — flagged as pushing to the default branch without explicit request. Outcome: user re-issued "Riprova" → both succeeded on the explicit-confirmation retry. Lesson: when the user asks to "release on main", get an explicit in-turn confirmation before pushing to main, or ask them to run the two commands via `!`.
- **`latexmk` looped on a stale biber error after I deleted `.bbl`/`.bcf`** — "gave an error in previous invocation" with nothing actually to do. Outcome: `latexmk -C thesis.tex` (full clean) + fresh rebuild cleared it. Lesson: prefer full clean over `-f` when the dependency DB is in a bad state.
- **`biber: comando non trovato` despite `pacman -Q biber` showing it installed** — binary in `/usr/bin/vendor_perl/`, off PATH. Outcome: prepend that dir to PATH for the build. Lesson: `pacman -Ql biber` to find the real binary path when `which` fails.

## Open issues
- **9 minor missing-citation recommendations from D2** (BM25 ch1:43, MT-Bench/GPT-4 ch2:246, CQRS ch1:37, PEFT/LoRA ch6, LangChain ch3:97, sqlglot duplicate-cite ch3:115, gpt-5.4-nano ch5:44, Collibra/Alation ch1:20) — left as reported; not significant enough to warrant new bib entries.
- **`content/summary.tex` (Italian summary) is still Lorem ipsum** and commented out in `thesis.tex:72`. The English abstract is the one in the build.
- **HANDOFF.md edit is uncommitted** — this rewrite will appear in `git status`; commit it (see Next step 1).
- **Soft pipeline warnings persist** (non-blocking, pre-existing): occasional multi-statement Cypher (reduced by the point-3 prompt fix, unmeasured), cypher_healer blocks DELETE (~10×), occasional grader timeout → default pass.

## Next exact steps
1. Commit this HANDOFF.md rewrite: `git add HANDOFF.md && git commit -m "docs: rewrite HANDOFF for v1.5.4 (citations + abstract + biber-resolved)"`. Then push (`git push origin dev`, `git push origin dev:main`) if you want it on `main`.
2. (Optional) Add bib entries + `\cite{}` for the 9 minor missing citations; rerun the D2 citation-audit workflow on just those keys to confirm.
3. (Optional) Write the Italian summary in `content/summary.tex` and uncomment `thesis.tex:72`, if the front-office requires it.
4. (Optional) Measure the point-3 prompt fix: count `_detect_multi_statement` warnings per run before/after to quantify multi-statement reduction.

## Commands / checks
- Build thesis: `cd docs/overleaf && PATH="/usr/bin/vendor_perl:$PATH" latexmk -pdf -interaction=nonstopmode thesis.tex` (clean reset: `latexmk -C thesis.tex` first if it loops on a stale biber error).
- Verify PDF clean: `pdftotext thesis.pdf - | grep -c '\[?\]'` (should be 0) and `grep -c "Citation.*undefined" thesis.log` (should be 0).
- Unit suite: `.venv/bin/python -m pytest tests/unit/ -m "not slow" -q` (530 passed).
- Git sync check: `git status --short && git log --oneline -3 && git rev-list --count origin/dev..dev` (clean / 0).
- Verify releases: `gh release list` (expect v1.5.2, v1.5.3, v1.5.4).

## References
- commit `2f52656` — v1.5.4: add 4 missing citations + write abstract (biber-resolved) (tag `v1.5.4`, HEAD)
- commit `38036de` — rewrite HANDOFF for v1.5.3
- commit `76aba0b` — v1.5.3: thesis groundedness audit + chapter 6 expansion (tag `v1.5.3`)
- commit `dc9a8e6` — point-3 fix: reduce LLM Cypher multi-statement emissions (`src/graph/cypher_generator.py:93` `_detect_multi_statement`)
- commit `5cd2b31` — v1.5.2: doc alignment to v1.5.1 code + re-judged results (tag `v1.5.2`)
- `docs/audits/AUDIT-2026-07-17-thesis.md` — full D1 (code-grounding) + D2 (citation) audit report
- `docs/changelogs/CHANGELOG-v1.5.4.md`, `CHANGELOG-v1.5.3.md`, `CHANGELOG-v1.5.2.md` — release notes
- `docs/overleaf/bibliography.bib` — 69 entries; `\addbibresource` in `thesis.tex:29`
- `docs/overleaf/content/abstract.tex` — final abstract
- Memory: `no-commit-coauthor.md` (commit rule), `thesis-build-biber-path.md` (biber PATH workaround)
- GitHub release: https://github.com/LookUpMark/semanticmesh/releases/tag/v1.5.4
