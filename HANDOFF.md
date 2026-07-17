# HANDOFF

## Goal
Allineare TUTTA la documentazione (`docs/ablation/RESULTS.md`) e la tesi
(`docs/overleaf/`) ai risultati della campagna ablation v1.5.1, dopo aver
completato AB-BEST-K20 DS03-07 e ri-eseguito l'AI Judge su tutti i bundle.
Riassunto in italiano con utente; docs/tesi rimangono in inglese.

## Current state
- **Branch:** `dev`, clean, up to date con origin.
- **Commits di questa sessione (in ordine):**
  - `29b99d4` — AB-BEST-K20 DS03-07 completato (5 dataset, grounded 100%, dual-metrics, 93.5m).
  - `0f4a32a` — fix langfuse: bump a v3 (v2 incompatibile con langchain 1.x).
  - `e51b83a` — AI Judge su tutti i 35 bundle (`gpt-5.4-nano-2026-03-17`).
- **Neo4j:** container `thesis-neo4j` FERMO (docker stop). `--auto-neo4j` lo riavvia al prossimo run.
- **Bundle totali:** 35 (AB-00..AB-20 × DS01 = 21; AB-BEST × DS01-07 = 7; AB-BEST-K20 × DS01-07 = 7).

## Decisioni prese (con utente, 2026-07-17)
1. **Ri-run AB-00..20 con codice v1.5.1** — i bundle AB-00..20 sono STALE (giugno, pre-dual-metrics, `dual=False`). Per RESULTS/tesi coerenti vanno ri-runnati con lo stesso codice di AB-BEST/K20. Utente ha scelto questa opzione (la più pulita scientificamente).
2. **AI Judge sostituisce score manuali** — i nuovi score `gpt-5.4-nano` sistematici sostituiscono i vecchi score manuali in RESULTS.md/tesi, con nota metodologica.

## Score AI Judge preliminari (su bundle attuali, PRIMA del ri-run AB-00..20)
> Attenzione: score AB-00..20 qui sotto sono su bundle STALE pre-v1.5.1. Van rifatti dopo ri-run.
- **AB-BEST (K5) DS01-07:** 4.70 / 4.45 / 3.85 / 4.45 / 4.25 / 4.00 / 4.45 → **avg 4.31**
- **AB-BEST-K20 DS01-07:** 4.20 / 4.60 / 4.70 / 3.95 / 4.20 / 4.25 / 4.20 → **avg 4.30**
- **K5 vs K20 = parità** (Δ -0.01). K5 vince 4/7, K20 vince 3/7. **Sovverte la narrativa storica** (vecchi: K5 4.73 vs K20 4.51, K5 6/7).
- AB-00..20 (DS01, stale): AB-00=4.50, AB-01=3.65, AB-02=3.70, AB-04=4.20, AB-05=4.50, AB-19=3.45... (da rifare).

## GT coverage v1.5.1 (dai bundle, già validi)
K20 ≥ K5 su tutti i 7 dataset (K5 avg 0.860, K20 avg 0.986). Δ max: DS06 legacy +0.370 (K5 0.63→K20 1.00), DS05 +0.211.

## Next exact steps (riprendi da qui)
1. **Ri-run AB-00..20 v1.5.1 su DS01** (era INTERROTTO a 0/21):
   ```bash
   cd /home/marcantoniolopez/Documenti/github/semanticmesh
   export NEO4J_CONTAINER_NAME=thesis-neo4j NEO4J_URI=bolt://localhost:7687
   .venv/bin/python -m scripts.run_pipeline --all-studies \
     --datasets tests/fixtures/01_basics_ecommerce/gold_standard.json --auto-neo4j
   ```
   ~1-1.5h. Verifica: `grep -c "✅ AB-" /tmp/rerun.log` = 21; bundle hanno `retrieval_quality_score_raw` (dual=True).

2. **Ri-giudica 35 bundle** (--force, così coerenti epoca v1.5.1):
   ```bash
   .venv/bin/python -m scripts.run_ai_judge --all --force \
     --studies AB-00 AB-01 AB-02 AB-03 AB-04 AB-05 AB-06 AB-07 AB-08 AB-09 AB-10 AB-11 AB-12 AB-13 AB-14 AB-15 AB-16 AB-17 AB-18 AB-19 AB-20 AB-BEST AB-BEST-K20 \
     --datasets 01_basics_ecommerce 02_intermediate_finance 03_advanced_healthcare 04_complex_manufacturing 05_edgecases_incomplete 06_edgecases_legacy 07_stress_large_scale \
     --output outputs/ablation/ai_judge_report.md
   ```

3. **Allinea docs/tesi** con score nuovi:
   - `docs/ablation/RESULTS.md`: sez 2 (tabella AB-00..20), sez 4 (AB-BEST 7-ds, avg 4.31), sez 8 (K5 vs K20 parità 4.31/4.30, **riscrivere narrative 8.3-8.6** — non regge "K5 strictly better"), sez 5 key findings.
   - `docs/overleaf/content/chapters/chapter5.tex`: tabella `ablation_results` (riga ~71) score nuovi; sez `reranker_impact` (AB-04=4.20 vs AB-05=4.50, **non più entrambi 4.90**); aggiungi sez K20/dual-metrics/floor-issue (ASSENTI dalla tesi, esistono solo in RESULTS.md).
   - Tesi in **inglese**.

4. **Commit** risultati ri-run + judge + doc alignment. Aggiorna questo HANDOFF o rimuovilo.

## Constraints / note
- **Langfuse v3 fixato** (`0f4a32a`): warning sparito, tracing riattivato. `flush_observability` resta safe (try/except, v3 handler non ha `.flush()`).
- **Warning soft pipeline** (non rottura, fallback gestiscono): Cypher multi-statement→deterministic retry, healer DELETE-block→retry, 1 grader timeout→pass. LLM cypher generator migliorabile (debito tecnico).
- **CRLF warning** git: benigno (normalizza LF).
- **AI judge script:** `scripts/run_ai_judge.py`. Score in `ai_judge.md` (NON in bundle JSON). Aggrega `scripts/generate_ablation_report.py`.
- **Formato score:** tabella 5 dimensioni weighted → Overall. Parse: `\*\*Overall\*\*.*?\*\*([0-5]\.\d{1,2})\*\*`.

## Files chiave
- `scripts/run_pipeline.py` — runner ablation (`--all-studies`, `--datasets`, `--auto-neo4j`)
- `scripts/run_ai_judge.py` — AI judge (`--all --force --studies --datasets --output`)
- `docs/ablation/RESULTS.md` — risultati ablation (449 righe, da aggiornare)
- `docs/overleaf/content/chapters/chapter5.tex` — Evaluation (sez 5.4 Empirical Results)
- `src/config/observability.py:49` — import langfuse v3 (`from langfuse.langchain import CallbackHandler`)
- `outputs/ablation/ai_judge_report.md` — report combinato AI judge
