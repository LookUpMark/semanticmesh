# HANDOFF

## Status: ✅ Session complete (2026-07-17)

Campaign v1.5.1 completa + AI Judge su tutti i 35 bundle + docs/tesi allineati.

## Cosa è stato fatto (commit in `dev`)
1. `29b99d4` — AB-BEST-K20 DS03-07 completato (grounded 100%, dual-metrics, 93.5m).
2. `0f4a32a` — fix langfuse: bump v3 (v2 incompatibile langchain 1.x; warning sparito, tracing riattivato).
3. `e51b83a` — AI Judge su 35 bundle (primo passaggio, score poi rifatti in `d9153ac`).
4. `4a58893` — HANDOFF refresh (stop intermedio).
5. `fe54603` — ri-run AB-00..AB-20 su DS01 con codice v1.5.1 (dual-metrics su tutti, grounded 100%).
6. `d9153ac` — ri-giudizio 35 bundle v1.5.1 con `--force` (epoca coerente).
7. `a88758b` — RESULTS.md allineato ai nuovi score.
8. `a651ed0` — chapter5.tex (tesi) allineato + 2 nuove subsection (K5/K20 sensitivity, dual-metrics floor).

## Risultati headline (v1.5.1, judge `gpt-5.4-nano-2026-03-17`)
- **35 bundle**, tutti grounded 100%, dual-metrics su tutti.
- **AB-BEST (K5) 7-ds avg 4.31** (gt 0.860); **AB-BEST-K20 7-ds avg 4.28** (gt 0.986). Δ −0.03 → **parità**. K5 vince 3/7, K20 2/7, tie 2/7.
- Su DS01: AB-19 Cypher-off peggiore (3.80), AB-06 chunking 128/16 migliore (4.80), AB-04/AB-05 reranker k5/k20 pari (4.50/4.50).
- **Narrativa storica corretta:** "K5 wins 6/7" e "schema/actor-critic critical" NON reggono su v1.5.1 (judge più severo + build stocastico diverso). Documentato onestamente in RESULTS §3.6/§5/§8 e tesi.
- Langfuse v3 funzionante. Warning soft pipeline (Cypher multi-stmt → deterministic fallback) = debito tecnico, non rottura.

## Cambiamenti di conclusioni (importante)
- Score AB-BEST 4.73→4.31 (judge sistematico più severo del manuale).
- K5 vs K20: da "K5 dominates" a "parità, K5 retained per efficienza".
- Schema enrichment / Actor-Critic: da "critical safety net (GT collapse)" a "neutral su DS01 v1.5.1, valore su dataset complessi".
- DS05 deep-dive: capovolto (K20-win → K5-win). DS07: K5-win → tie.

## Note tecniche
- Neo4j container `thesis-neo4j` — `--auto-neo4j` lo gestisce (start/stop).
- AI Judge script: `scripts/run_ai_judge.py --all --force --studies ... --datasets ...`.
- Score nei file `ai_judge.md` (NON nel bundle JSON). Parser regex: `\*\*Overall\*\*.*?\*\*([0-5]\.\d{1,2})\*\*`.
- CRLF warning git = benigno.

## Possibili proseguimenti (non richiesti)
- Rifinire narrative tesi dove i nuovi score abbassano toni (es. abstract/conclusion se citavano 4.73).
- Migliorare LLM Cypher generator (ridurre fallback multi-statement).
- Valutare adaptive top_k (K20 quando avg_top_score basso).
