# Changelog — v1.5.3

**Date:** 2026-07-17
**Audit Reference:** docs/audits/AUDIT-2026-07-17-thesis.md
**Type:** Patch — thesis groundedness audit + chapter 6 expansion + citation/code corrections (no runtime behaviour change)

## Summary

A full two-axis audit of the Overleaf thesis (`docs/overleaf/`) against (a) the actual SemanticMesh codebase and (b) the cited papers. Run as two multi-agent workflows under ultracode (2.5M subagent tokens): a **code-grounding audit** (226 claims across ch1–ch6) and a **citation audit** (83 `\cite{}` claims against 49 local PDFs). Result: ~90 % of code claims grounded and 88 % of citations verified, with **0 critical errors**. 16 factual corrections were applied and chapter 6 was expanded from a 37-line stub into a full, grounded Conclusions chapter. No `src/` runtime behaviour changed.

## Documentation Changes

### Chapter 6 — Conclusions (expanded, grounded)
Rewrote the thin 37-line Conclusions stub into a complete chapter:
- **§6.1 Summary of Contributions** — 6 evidence-grounded contributions; the Actor-Critic item is corrected to the verified "single mid-tier LLM, two prompt-separated roles" design (not "separate LLM instances").
- **§6.2 Empirical Summary** — the v1.5.1 evidence (AB-BEST 4.31/5 across 7 datasets, 210/210 grounded answers, K5 vs K20 tied at 4.31/4.28 with recall decoupled from judged quality, the retrieval-quality-score floor / dual metrics).
- **§6.3 System Limitations** — honestly split into *observed* (DS03 multi-hop precision, degraded-schema coverage, score floor) and *design-extrapolated* limitations (wide tables, >1000-table scale, embedding drift) that are qualitative and unmeasured at the stated thresholds.
- **§6.4 Future Research Directions** — 6 concrete directions grounded in the audit gaps (community detection, intra-table chunking, domain SLM fine-tuning, adaptive top-k, text-to-Cypher, active learning from HITL).

### Code-grounding corrections (Phase D1)
Verified against `src/` before applying:
- **ch1 (HIGH):** Actor-Critic description corrected — `parallel_mapping.py:39` and `validation_nodes.py:37` share one `get_midtier_llm()` singleton; roles differ by prompt, not by model instance.
- **ch4:** removed the false `UNWIND` claim (absent from few-shot/builder/prompt); relocated SHA-256 change detection to `file_registry.py`; ER judge corrected to the mid-tier; vector search reframed around the dominant `businessconcept_embedding` index; LLM-factory tiers corrected (4 dedicated env vars, lightweight reuses extraction); SQLGlot dialects corrected to 4 (+T-SQL) with the regex-pre-cleaning caveat.
- **ch1/ch2:** the "providers (OpenRouter, OpenAI, Anthropic, local)" list expanded to the twelve backends actually implemented.
- **ch1/ch2:** the "fully grounded answers consistently scored below 0.2" answer-relevancy claim corrected to "as low as 0.16, per-question aggregate ≈ 0.73".
- **ch2 Table 2.1:** SemanticMesh "Community detection = Cosine clustering" → "None (planned future work)" (entity-resolution blocking is not community detection).

### Citation corrections (Phase D2)
Verified against the cited PDFs:
- **ch2 (SIG):** RAGAS description corrected to the paper's three reference-free aspects (faithfulness, answer relevance, context relevance); context precision/recall noted as library extensions, with context recall no longer reference-free.
- **ch2 (SIG):** GRAG "Graph construction = LLM-based" corrected in both comparison tables — GRAG consumes pre-existing graphs (`hu2025grag` §3–4).
- **ch2 (MIN):** BGE-M3 mechanism corrected to self-knowledge distillation (Multi-Granularity = input-length handling, `chen2024bgeM3` Intro).
- **ch2 (MIN):** CRAG "out-of-distribution queries" → "noisy or ambiguous queries" (the paper never uses OOD; `yan2024corrective`).

### Sources added
Six cited papers that had no local PDF were downloaded (via the `wiki-add-source` skill) into `docs/overleaf/literature/<bibkey>.pdf`, bringing local coverage to 49 PDFs:
`blondel2008fast`, `traag2019from`, `cormack2009reciprocalrankfusionoutperforms`, `lewis2020bart`, `raffel2020exploring`, `wei2022chainofthoughtpromptingelicitsreasoning`.

## Verification

- **Code-grounding audit:** 226 claims; 10 fixes applied; 12 LOW (phrasing/nuance) reported in the audit doc.
- **Citation audit:** 83 claims; 73 VERIFIED, 10 PARTIALLY; 6 fixes applied; 0 PDF-mismatch; 13 missing-citation recommendations reported (4 significant: GSM8K, HotpotQA, FEVER, bge-reranker-v2-m3 — left to the author).
- **LaTeX build:** `pdflatex` succeeds, 73 pages, no errors. **Tooling caveat:** `biber` is not installed in this environment, so the 2 brand-new ch6 citations (`blondel2008fast`, `traag2019from`) render `[?]` until `biber` is installed and the thesis rebuilt; the `.tex`/`.bib` sources are correct.

## Known follow-ups (not in this release)

- Install `biber` and rebuild so the 2 new ch6 citations resolve.
- Optionally add bib entries for the 4 significant missing citations (GSM8K, HotpotQA, FEVER, bge-reranker-v2-m3).
- The thesis abstract (`content/abstract.tex` / `content/summary.tex`) is still a placeholder and is not included in the build (commented out in `thesis.tex`).
