# HANDOFF

## Goal
Complete the v1.5.1 ablation campaign end-to-end on the SemanticMesh GraphRAG pipeline — finish AB-BEST-K20 DS03-07, re-run all single-variable studies (AB-00..AB-20) on the v1.5.1 codebase, run the AI Judge on all 35 evaluation bundles, and align `docs/ablation/RESULTS.md` + the Overleaf thesis (`docs/overleaf/`) to the new results.

## Current state
- **Branch `dev`, clean, NOT pushed.** 9 session commits (`29b99d4`..`91dd5b5`).
- **AB-BEST-K20 DS03-07:** run complete, grounded 100%, dual-metrics present (`29b99d4`).
- **AB-00..AB-20 DS01:** re-run on v1.5.1 code, all 21 grounded 100%, all carry dual-metrics (`fe54603`). Replaces stale June bundles that lacked dual-metrics.
- **AI Judge:** all 35 bundles judged with `gpt-5.4-nano-2026-03-17`, coherent v1.5.1 epoch (`d9153ac`). Per-bundle `ai_judge.md` + combined `outputs/ablation/ai_judge_report.md`.
- **Docs aligned:** `RESULTS.md` (`a88758b`) and `chapter5.tex` (`a651ed0`) rewritten on new scores + 2 new thesis subsections (K5/K20 sensitivity, dual-metrics floor).
- **Langfuse v3 fix** live (`0f4a32a`): warning gone, tracing re-enabled.
- **Neo4j:** container `thesis-neo4j` is DOWN (stopped at end of last run). `--auto-neo4j` restarts it.

## Files touched
- `src/config/observability.py` — langfuse import bumped to v3 path `from langfuse.langchain import CallbackHandler` (line 49).
- `pyproject.toml` — `langfuse>=3.0,<4.0` (was `<3.0`, AUDIT-025 pin incompatible with langchain 1.x).
- `docs/ablation/RESULTS.md` — §2 table, §3 per-group, §4 AB-BEST 7-ds, §5 findings, §7 marked superseded, §8 K5/K20 all rewritten on v1.5.1 scores.
- `docs/overleaf/content/chapters/chapter5.tex` — ablation_results table + 3 subsections rewritten; added `sec:eval:topk_sensitivity` and `sec:eval:dual_metrics`.
- `outputs/ablation/AB-*/datasets/*/evaluation_bundle.json` — 35 bundles (21 re-run + 14 prior v1.5.1).
- `outputs/ablation/AB-*/datasets/*/ai_judge.md` — 35 judge reports.
- `outputs/ablation/ai_judge_report.md` — combined judge report.

## Decisions made
- Re-run AB-00..20 on v1.5.1 (not just re-judge stale bundles) - user chose this for scientific coherence; June bundles lacked dual-metrics and mixed code versions, making cross-study score comparison unreliable.
- AI Judge replaces prior manual scores - systematic `gpt-5.4-nano` judge is reproducible; manual scores were not. Documented as a methodology note.
- Langfuse upgraded to v3 (not disabled) - code already used the v3 import path; only the pyproject pin blocked it. Restores tracing rather than dropping observability.
- AB-BEST keeps `reranker_top_k=5` on efficiency grounds (4× reranker saving), not quality dominance - K5 and K20 are judge-tied (4.31 vs 4.28).
- Corrected (not hidden) the stale conclusions - "K5 wins 6/7", "schema/actor-critic critical" do not hold on v1.5.1; rewritten honestly in RESULTS §3.6/§5/§8 and thesis.

## Constraints
- AI Judge scores live in `ai_judge.md` (markdown), NOT in the bundle JSON `score` field. Parse regex: `\*\*Overall\*\*.*?\*\*([0-5]\.\d{1,2})\*\*`.
- `run_ai_judge.py --all` default discovers only AB-01..AB-20 × DS01-06 — must pass explicit `--studies` (incl. AB-00, AB-BEST, AB-BEST-K20) and `--datasets` (incl. 07) for full coverage.
- `flush_observability()` stays safe via existing try/except — v3 `LangchainCallbackHandler` has no `.flush()`.
- Each pipeline run clears the Neo4j graph (`--clear-graph=True`), so studies/datasets are independent.
- CRLF warnings on thesis CSVs are benign (git normalizes to LF).
- Thesis is written in English; conversation with user is in Italian.

## Attempts and failures
- Langfuse import `from langfuse.callback import CallbackHandler` (v2 path) - fails because v2 imports `langchain.callbacks.base`, removed in langchain 1.x - Lesson: langfuse 2.x is fundamentally incompatible with langchain 1.x regardless of import path; v3 is required.
- First AI Judge pass on AB-00..20 - scored stale June bundles, not v1.5.1 - Lesson: bundle epoch must match before judging; re-ran AB-00..20 then `--force` re-judged.
- Edit on RESULTS §8 header+table in one call - string-not-found due to line shifts from earlier edits - Lesson: re-Read exact lines before large Edits after prior edits shift offsets.

## Open issues
- `dev` is 9 commits ahead of `origin/dev`, not pushed.
- Soft pipeline warnings persist (non-blocking, fallback-handled): LLM emits multi-statement Cypher (~38× per run → deterministic builder retry), cypher_healer blocks DELETE (~10× → retry), 1 grader timeout → default pass. Indicates the LLM Cypher generator could be improved (tech debt).
- `uv.lock` declared langfuse 3.15.0 even before the pyproject fix (lock was ahead of constraint); `uv lock` not re-run after the pin change — currently consistent, but a future `uv sync` should be watched.

## Next exact steps
1. Decide on push: `git push origin dev` (if ready) or keep local for review.
2. Optional: skim thesis `abstract.tex`, `chapter1.tex` (contributions), `chapter6.tex` (conclusions) for any lingering 4.73/5.00 references — grep found none, but a human read is prudent before submission.
3. Optional: improve the LLM Cypher generator to reduce multi-statement emissions (reduce deterministic-builder fallback load).
4. Optional: prototype adaptive `top_k` (raise to 20 when `avg_top_score` < threshold) — K20 maximises GT coverage (0.986 vs 0.860) without hurting judge score.

## Commands / checks
- Verify 35 bundles grounded + dual-metrics:
  `.venv/bin/python -c "import json,glob; [print(s.split('/')[-3], json.load(open(s)).get('query_report',{}).get('grounded_rate'), any('retrieval_quality_score_raw' in q for q in json.load(open(s)).get('per_question',[]))) for s in sorted(glob.glob('outputs/ablation/AB-*/datasets/*/evaluation_bundle.json'))]"`
- Re-extract all Overall scores: grep `\*\*Overall\*\*.*?\*\*([0-5]\.\d{1,2})\*\*` in each `ai_judge.md`.
- Re-run a single study: `NEO4J_CONTAINER_NAME=thesis-neo4j NEO4J_URI=bolt://localhost:7687 .venv/bin/python -m scripts.run_pipeline --study AB-BEST-K20 --datasets tests/fixtures/07_stress_large_scale/gold_standard.json --auto-neo4j`
- Re-judge: `.venv/bin/python -m scripts.run_ai_judge --all --force --studies AB-00 AB-01 ... AB-BEST AB-BEST-K20 --datasets 01_basics_ecommerce ... 07_stress_large_scale --output outputs/ablation/ai_judge_report.md`
- Build thesis: `cd docs/overleaf && latexmk -pdf thesis.tex` (verify new subsections render).

## References
- commit `29b99d4` - AB-BEST-K20 DS03-07 complete with dual metrics
- commit `0f4a32a` - langfuse v3 bump (langchain 1.x compat)
- commit `e51b83a` - AI Judge on 35 bundles (first pass)
- commit `4a58893` - mid-session HANDOFF refresh (forced stop)
- commit `fe54603` - re-run AB-00..AB-20 on v1.5.1
- commit `d9153ac` - re-judge 35 bundles on v1.5.1 coherent epoch
- commit `a88758b` - RESULTS.md aligned to v1.5.1
- commit `a651ed0` - chapter5.tex (thesis) aligned + 2 new subsections
- commit `91dd5b5` - HANDOFF session-complete
- `scripts/run_ai_judge.py` - AI Judge runner (`--force`, per-bundle `ai_judge.md`)
- `scripts/run_pipeline.py` - ablation runner (`--all-studies`, `--datasets`, `--auto-neo4j`)
- `docs/AI_JUDGE_PROMPT.md` - judge rubric (system prompt)
- `src/generation/nodes/retrieval_nodes.py:377-389` - dual-metrics pool-confidence logic
