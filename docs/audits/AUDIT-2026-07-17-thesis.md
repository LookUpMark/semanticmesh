# Thesis Groundedness Audit — 2026-07-17

**Scope:** Full review of the SemanticMesh thesis (`docs/overleaf/`) against (a) the actual codebase (`src/`, `outputs/`, `docs/ablation/`) and (b) the cited papers (`docs/overleaf/literature/`).
**Method:** Two multi-agent workflows (ultracode) — a code-grounding audit (6 chapter agents + adversarial verify) and a citation audit (45 cited-work agents + an uncited-concept scan). 2.5M subagent tokens total.
**Outcome:** 226 code claims audited (~90 % grounded), 83 citation claims verified (88 %). **0 critical errors.** 16 factual fixes applied across ch1/ch2/ch4/ch6; chapter 6 expanded from a 37-line stub into a full grounded Conclusions chapter.

---

## Phase D1 — Code-Grounding Audit

**Workflow:** `thesis-code-grounding-audit` — one agent per chapter (ch1–ch6) extracts every factual claim and verifies it against `src/`, `outputs/ablation/`, `docs/ablation/RESULTS.md`, `pyproject.toml`, `src/prompts/templates.py`.

**Coverage:** 226 claims. Grounding: yes 194 / partial 20 / no 2 / n/a 10. **22 problems** (1 high, 8 medium, 13 low). Adversarial re-verify stage crashed on a script typo (`dubuous`); stage-1 findings were recovered from `journal.jsonl` and the flagged claims were hand-verified against code before fixing.

### D1 fixes applied (10)

| # | Sev | Ch | Claim (before) | Fix | Code evidence |
|---|---|----|----------------|-----|---------------|
| 1 | HIGH | ch1 | Actor-Critic uses "separate Actor and Critic LLM instances" | Rewritten: a **single mid-tier LLM** plays two prompt-separated roles (Actor/Critic), Self-Refine-style | `parallel_mapping.py:39`, `validation_nodes.py:37` both call `get_midtier_llm()` |
| 2 | MED | ch4 | Few-shot Cypher uses `MERGE` and `UNWIND` | `UNWIND` removed; described as `MERGE`+`WITH`+`ON CREATE/ON MATCH SET`, plus the new single-statement guard | `grep UNWIND` = 0 across few-shot/builder/prompt |
| 3 | MED | ch4 | SHA-256 change detection in `pdf_loader.py` | Moved to `file_registry.py` (invoked from Builder graph) | `file_registry.py:compute_file_sha:44`, `builder_graph.py:448-482` |
| 4 | MED | ch4 | ER judge uses the "lightweight LLM tier" | Corrected to **mid-tier** | `entity_resolver.py:174-176` (`get_midtier_llm`) |
| 5 | MED | ch4 | Vector search over "child chunk embeddings" | Dominant index is `businessconcept_embedding` (+ `attribute_embedding`, `chunk_embedding`) | `hybrid_retriever.py:130,183,252` |
| 6 | MED | ch4 | Five tiers "configured via tier-specific env vars" | 4 tiers have dedicated env vars; lightweight reuses extraction | `llm_factory.py:332-473` (`get_lightweight_llm` reuses `LLM_*_EXTRACTION`) |
| 7 | MED | ch4 | SQLGlot "avoids regex", dialects PostgreSQL/MySQL/Oracle | AST parse (regex retained only for pre-cleaning); +T-SQL = 4 dialects | `ddl_parser.py:5,103,154,319-326` |
| 8 | MED | ch1 | Provider list "(OpenRouter, OpenAI, Anthropic, local)" | Twelve backends enumerated | `model_builders.py` (12 builders) |
| 9 | MED | ch1+ch2 | "fully grounded answers consistently scored below 0.2" answer relevancy | Rewritten: min 0.16, per-question aggregate ≈ 0.73 | `docs/AI_JUDGE_PROMPT.md:16` (min) + RAGAS bundle (agg 0.73) |
| 10 | MED | ch2 | Table 2.1 SemanticMesh "Community detection = Cosine clustering" | Changed to "None (planned future work)" — ER blocking ≠ community detection | no graph community-detection stage exists |

### D1 reported, not fixed (12 LOW — phrasing/nuance)

- **ch6 limitations** (>100 cols, >1000 tables, embedding drift): kept but reframed as *design-extrapolated, not measured* (largest fixture DS07 = 58 tables, 33 cols).
- **ch3 query Phase 3** "few-shot prompting": answer generation uses system-prompt selection, not few-shot (few-shot is only in Cypher/mapping).
- **ch2** entity-resolution pipeline wording; Actor-Critic "different LLM instances" (same root as #1, in related-work prose); illustrative prompt-role table.
- **ch5** results-table caption "v1.5.1": accurate for the results (code is now 1.5.2/1.5.3); left as-is.

---

## Phase D2 — Citation Audit

**Workflow:** `thesis-citation-audit` — one agent per cited work reads the thesis claim sentence(s) + the matching `literature/<key>.pdf` and returns a verdict; plus an uncited-concept scan. Uses the `citation-audit` skill methodology.

**Sources downloaded (6)** via the `wiki-add-source` skill (arXiv + author pages), placed in `docs/overleaf/literature/` with the `<bibkey>.pdf` convention:
`blondel2008fast`, `traag2019from`, `cormack2009reciprocalrankfusionoutperforms`, `lewis2020bart`, `raffel2020exploring`, `wei2022chainofthoughtpromptingelicitsreasoning`.

**Coverage:** 83 citation claims. **73 VERIFIED, 10 PARTIALLY VERIFIED, 0 UNVERIFIED, 0 critical, 0 PDF-mismatch** (all 49 PDFs match their bib entries, including the 6 new downloads). 4 software/doc sources (GDPR, spaCy, LangGraph docs, sqlglot) have no PDF and were verified at the code-usage level.

### D2 fixes applied (6)

| # | Sev | Ch | Claim (before) | Fix | PDF evidence |
|---|---|----|----------------|-----|--------------|
| 1 | SIG | ch2 | RAGAS "four reference-free dimensions" | Paper defines **3** reference-free aspects (faithfulness, answer relevance, context relevance); context precision/recall are library extensions and context recall is **not** reference-free | `es2025ragas…pdf` Sec. 3 |
| 2 | SIG | ch2 | GRAG "Graph construction = LLM-based" (both comparison tables) | GRAG **consumes pre-existing graphs**, does not construct them → "N/A (consumes graphs)" / "No" | `hu2025grag….pdf` §3–4 |
| 3 | MIN | ch2 | BGE-M3 three representations via "multi-granularity objectives" | Mechanism = **self-knowledge distillation**; Multi-Granularity = input-length handling | `chen2024bgeM3….pdf` Intro |
| 4 | MIN | ch2 | CRAG improves robustness on "out-of-distribution queries" | Paper never uses OOD; changed to "noisy or ambiguous queries" | `yan2024corrective….pdf` |
| 5 | MIN | ch1+ch2 | answer-relevancy "consistently below 0.2" | See D1 #9 | — |
| 6 | MIN | ch4 | SQLGlot "avoids regex" | Already softened in the D1 pass (#7) | — |

### D2 missing-citation recommendations (13, not added)

Concepts described with a factual assertion but no `\cite{}` in scope. The 4 **significant** ones would require new bib entries and are left to the author:

- **GSM8K** (ch2:212), **HotpotQA** (ch2:94), **FEVER** (ch2:94) — benchmarks used to report scores.
- **bge-reranker-v2-m3** (ch3:195) — model card / Xiao et al.

Minor: BM25 (ch1:43), MT-Bench (ch2:246), GPT-4 (ch2:246), CQRS (ch1:37), PEFT/LoRA (ch6), LangChain (ch3:97), sqlglot duplicate-cite (ch3:115), gpt-5.4-nano (ch5:44), Collibra/Alation (ch1:20).

---

## Phase D3 — Chapter 6 Expansion

`chapter6.tex` expanded from a 37-line stub into a full grounded Conclusions chapter:
- **§6.1 Summary of Contributions** — 6 evidence-grounded items (Actor-Critic corrected to single-model two-role framing).
- **§6.2 Empirical Summary** — v1.5.1 results (AB-BEST 4.31/5, 210/210 grounded, K5/K20 tied 4.31 vs 4.28, recall ≠ quality, retrieval-quality floor / dual metrics).
- **§6.3 System Limitations** — honestly split into *observed* (DS03 3.65 multi-hop; DS05/06 coverage; score floor) and *design-extrapolated* (wide tables, >1000 tables, embedding drift — all unmeasured at the stated thresholds).
- **§6.4 Future Research Directions** — 6 concrete items grounded in identified gaps (community detection, intra-table chunking, SLM fine-tuning, adaptive top-k, text-to-Cypher, active learning from HITL).

ch6's 3 new citations (`blondel2008fast`, `traag2019from`, `tiwari2025autocypherimprovingllmscypher`) were verified against their PDFs.

---

## Verification

- **LaTeX build:** `pdflatex` succeeds, 73 pages, no `!` errors, no undefined references. chapter 6 (§6.1–6.4) renders correctly.
- **Caveat (tooling):** the env has **no `biber`**, so the stale `thesis.bbl` resolves all previously-cited keys but the 2 brand-new ch6 keys (`blondel2008fast`, `traag2019from`) render `[?]` until `biber` is installed and the thesis rebuilt (`sudo pacman -S texlive-biberextra && latexmk -pdf thesis.tex`). The `.tex`/`.bib` sources are correct regardless.
- **No code-behaviour change** in this audit (thesis-only); the `src/` Cypher-generator single-statement guard from the prior commit is reflected in ch4.
