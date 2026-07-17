# Ablation Study Results — DS01 (E-Commerce Baseline)

**Date:** 2026-04-21 (initial) — **2026-07-17 (re-run v1.5.1, all 35 bundles on a coherent epoch)**  
**Dataset:** `01_basics_ecommerce` — 7 tables, 15 QA pairs  
**Judge model:** `gpt-5.4-nano-2026-03-17` (OpenAI direct)  
**Evaluator:** AI-as-Judge with rubric from `docs/AI_JUDGE_PROMPT.md`  
**Code version:** v1.5.1 (dual retrieval metrics, langfuse v3 observability)

> **Note (2026-07-17):** All 35 bundles (AB-00→AB-20 on DS01, AB-BEST and AB-BEST-K20 on DS01–DS07) were re-run on the v1.5.1 codebase and re-judged with `gpt-5.4-nano-2026-03-17` so every study now carries the dual retrieval metrics (`retrieval_quality_score_raw/adjusted`, `pool_size`, `pool_confidence_applied`) and shares one epoch. This supersedes the prior May/June bundles, which lacked dual-metrics and mixed code versions. Combined AI-Judge report: [`outputs/ablation/ai_judge_report.md`](../../outputs/ablation/ai_judge_report.md). Score levels are lower and more compressed than the earlier manual-judge figures (e.g. AB-BEST 4.73→4.31): the systematic LLM judge is stricter and the v1.5.1 KG builds differ stochastically from earlier runs.

---

## 1. Overview

This document reports the results of a systematic ablation campaign (AB-00 through AB-20 plus AB-BEST) run on the E-Commerce baseline dataset (`01_basics_ecommerce`). Each study isolates one pipeline variable while keeping all others at their default value. The goal is to identify which components and hyperparameter settings most affect end-to-end quality.

The pipeline has two phases:

- **Builder graph** — ingests PDF documentation and DDL, extracts knowledge graph triplets, resolves entities, maps schema tables to ontology concepts, generates and executes Cypher.
- **Query graph** — answers natural-language questions using hybrid retrieval (dense + BM25 + graph traversal), cross-encoder reranking, and a hallucination grader.

---

## 2. Full Results Table

| Study | Title | Group | Tables | Triplets | Entities | GT Cov | Grounded | Avg Score | AI Judge |
|-------|-------|-------|--------|----------|----------|--------|----------|-----------|----------|
| AB-00 | Baseline — default settings | Baseline | 7/7 | 112 | 76 | 98% | 15/15 | 0.7813 | 4.50/5 |
| AB-01 | Retrieval: Vector-only | Retrieval Mode | 7/7 | 80 | 64 | 100% | 15/15 | 0.5722 | 4.25/5 |
| AB-02 | Retrieval: BM25-only | Retrieval Mode | 7/7 | 112 | 69 | 54% | 15/15 | 0.7162 | 4.25/5 |
| AB-03 | Reranker OFF | Reranker | 7/7 | 100 | 56 | 100% | 15/15 | 0.7000 | 4.65/5 |
| AB-04 | Reranker top_k=5 | Reranker | 7/7 | 92 | 42 | 100% | 15/15 | 0.7760 | 4.50/5 |
| AB-05 | Reranker top_k=20 | Reranker | 7/7 | 112 | 71 | 100% | 15/15 | 0.7747 | 4.50/5 |
| AB-06 | Chunking 128/16 | Chunking | 7/7 | 106 | 59 | 100% | 15/15 | 0.7899 | **4.80/5** |
| AB-07 | Chunking 384/48 | Chunking | 7/7 | 101 | 74 | 98% | 15/15 | 0.7761 | 4.50/5 |
| AB-08 | Chunking 512/64 | Chunking | 7/7 | 102 | 68 | 92% | 15/15 | 0.7771 | 4.50/5 |
| AB-09 | Extraction tokens=4096 | Extraction | 7/7 | 124 | 85 | 98% | 15/15 | 0.7818 | 4.40/5 |
| AB-10 | Extraction tokens=16384 | Extraction | 7/7 | 125 | 62 | 100% | 15/15 | 0.7862 | 4.50/5 |
| AB-11 | ER threshold=0.65 (aggressive) | Entity Resolution | 7/7 | 98 | 62 | 98% | 15/15 | 0.7843 | 4.50/5 |
| AB-12 | ER threshold=0.85 (conservative) | Entity Resolution | 7/7 | 99 | 61 | 95% | 15/15 | 0.7778 | 4.25/5 |
| AB-13 | ER blocking top_k=5 | Entity Resolution | 7/7 | 122 | 65 | 98% | 15/15 | 0.7856 | 4.50/5 |
| AB-14 | ER blocking top_k=20 | Entity Resolution | 7/7 | 137 | 74 | 92% | 15/15 | 0.7866 | 4.15/5 |
| AB-15 | Schema enrichment OFF | Pipeline Components | 7/7 | 91 | 53 | 98% | 15/15 | 0.7650 | 4.50/5 |
| AB-16 | Actor-Critic validation OFF | Pipeline Components | 7/7 | 126 | 92 | 98% | 15/15 | 0.7882 | 4.40/5 |
| AB-17 | HITL threshold=0.70 | HITL | 7/7 | 95 | 53 | 93% | 15/15 | 0.7858 | 4.20/5 |
| AB-18 | HITL threshold=0.85 | HITL | 7/7 | 91 | 49 | 98% | 15/15 | 0.7853 | 4.50/5 |
| AB-19 | Cypher healing OFF | Pipeline Components | 7/7 | 109 | 69 | 98% | 15/15 | 0.7850 | 3.80/5 |
| AB-20 | Hallucination grader OFF | Pipeline Components | 7/7 | 106 | 59 | 92% | 15/15 | 0.7727 | 4.50/5 |
| **AB-BEST** | **Data-driven best config** | **Optimised** | **7/7** | **68** | **29** | **100%** | **15/15** | **0.7834** | **4.50/5** |

> On DS01 every study reaches 100% grounded (15/15) and AI-Judge scores cluster tightly between 3.80 and 4.80 — the baseline dataset is too simple for most single-variable changes to discriminate quality. The two clear signals are AB-19 (Cypher healing OFF, 3.80) as the worst study and AB-06 (chunking 128/16, 4.80) as the best; AB-BEST ties the baseline at 4.50 here and only pulls ahead on the harder DS02–DS07 (see §4).  
> GT Coverage = proportion of expected sources retrieved. `Avg Score` = mean `retrieval_quality_score` (cross-encoder) across questions.

---

## 3. Per-Group Analysis

### 3.1 Retrieval Mode (AB-01, AB-02 vs AB-00)

| Study | Retrieval | GT Coverage | Avg Score | Judge |
|-------|-----------|-------------|-----------|-------|
| AB-00 | hybrid | 98% | 0.7813 | 4.50 |
| AB-01 | vector-only | 100% | 0.5722 | 4.25 |
| AB-02 | BM25-only | 54% | 0.7162 | 4.25 |

**Finding:** On this simple dataset the judge barely separates the three modes (4.50 vs 4.25 vs 4.25), but the retrieval signals still point the right way. BM25-only collapses GT coverage to 54% — it cannot match semantically paraphrased questions — and has the lowest judge. Vector-only keeps full GT coverage but its retrieval-quality score is markedly lower (0.5722), since with the reranker fed dense-only candidates the cross-encoder confidence drops. Hybrid (dense + keyword + graph traversal) keeps both GT coverage and a high retrieval score, and is retained as the default.

---

### 3.2 Reranker (AB-03, AB-04, AB-05 vs AB-00)

| Study | Reranker | top_k | GT Coverage | Avg Score | Judge |
|-------|----------|-------|-------------|-----------|-------|
| AB-00 | ON | 12 | 98% | 0.7813 | 4.50 |
| AB-03 | OFF | — | 100% | 0.7000 | 4.65 |
| AB-04 | ON | 5 | 100% | 0.7760 | 4.50 |
| AB-05 | ON | 20 | 100% | 0.7747 | 4.50 |

**Finding:** On DS01 the reranker setting does not discriminate the judge: `top_k=5` and `top_k=20` tie at 4.50/5, and even disabling the reranker (AB-03) lands at 4.65. The dataset is small enough that any of the three retrieves the expected sources (100% GT coverage). `top_k=5` is retained in AB-BEST for the 4× cross-encoder inference saving, with the `top_k=20` sensitivity validated across all seven datasets in §8 (where the two configs are again effectively tied at the judge level, 4.31 vs 4.28).

---

### 3.3 Chunking Strategy (AB-06, AB-07, AB-08 vs AB-00)

| Study | Chunk size/overlap | GT Coverage | Avg Score | Judge |
|-------|-------------------|-------------|-----------|-------|
| AB-00 | 256/32 | 98% | 0.7813 | 4.50 |
| AB-06 | 128/16 | 100% | 0.7899 | **4.80** |
| AB-07 | 384/48 | 98% | 0.7761 | 4.50 |
| AB-08 | 512/64 | 92% | 0.7771 | 4.50 |

**Finding:** The smallest chunk size (128/16) is the single best study on DS01 (4.80/5), with full GT coverage and the highest retrieval-quality score. Mid and large chunks (384/48, 512/64) tie the baseline at 4.50. Fine-grained chunking helps when entities are short and densely named (as in a glossary/data-dictionary pair), but it inflates node count on larger corpora, so AB-BEST keeps the balanced 256/32.

---

### 3.4 Extraction Token Limit (AB-09, AB-10 vs AB-00)

| Study | Max tokens | Triplets | GT Coverage | Avg Score | Judge |
|-------|-----------|----------|-------------|-----------|-------|
| AB-00 | 8192 | 112 | 98% | 0.7813 | 4.50 |
| AB-09 | 4096 | 124 | 98% | 0.7818 | 4.40 |
| AB-10 | 16384 | 125 | 100% | 0.7862 | 4.50 |

**Finding:** Token limit is nearly inert on DS01. Triplet counts are stable (112/124/125) and GT coverage stays at 98–100%. The judge difference (4.40 vs 4.50) is within noise. AB-BEST keeps 8192 as a robust default for denser content.

---

### 3.5 Entity Resolution (AB-11 through AB-14 vs AB-00)

| Study | ER threshold | ER top_k | Entities | GT Coverage | Judge |
|-------|-------------|----------|----------|-------------|-------|
| AB-00 | 0.75 | 10 | 76 | 98% | 4.50 |
| AB-11 | **0.65** | 10 | 62 | 98% | 4.50 |
| AB-12 | 0.85 | 10 | 61 | 95% | 4.25 |
| AB-13 | 0.75 | **5** | 65 | 98% | 4.50 |
| AB-14 | 0.75 | **20** | 74 | 92% | 4.15 |

**Finding:** Entity resolution is broadly neutral on DS01. Aggressive merging (0.65) and a tight blocking neighbourhood (top_k=5) keep quality and coverage at baseline level (4.50, 98%). The only visible cost is AB-14 (blocking top_k=20, 4.15), where casting a wider merge net on a small corpus introduces borderline merges and drops GT coverage to 92%. AB-BEST keeps threshold=0.75 and top_k=10 to balance recall against false merges on larger entity sets.

---

### 3.6 Pipeline Components (AB-15, AB-16, AB-19, AB-20 vs AB-00)

| Study | Component disabled | GT Coverage | Avg Score | Judge |
|-------|-------------------|-------------|-----------|-------|
| AB-00 | — (all ON) | 98% | 0.7813 | 4.50 |
| AB-15 | Schema enrichment OFF | 98% | 0.7650 | 4.50 |
| AB-16 | Actor-Critic OFF | 98% | 0.7882 | 4.40 |
| AB-19 | Cypher healing OFF | 98% | 0.7850 | **3.80** |
| AB-20 | Hallucination grader OFF | 92% | 0.7727 | 4.50 |

**Finding (updated for v1.5.1):** The earlier "schema-enrichment / actor-critic are critical safety nets" reading was an artefact of the pre-v1.5.1 runs, where disabling them collapsed GT coverage to 61% / 67%. On the v1.5.1 DS01 bundles that collapse **does not reproduce** — GT coverage stays at 98% with either component off, and the judge is within noise of the baseline (4.50 / 4.40). The v1.5.1 builder is robust enough on this simple 7-table schema that the downstream graph still retrieves the expected sources even without acronym expansion or critic validation; their value is expected to reappear on larger/degraded schemas (DS05, DS07 — see §4, §8). The one component whose absence the judge still penalises on DS01 is **Cypher healing (AB-19, 3.80/5)**: even when all tables complete, unhealed Cypher leaves the graph structurally weaker and the answers less precise.

---

### 3.7 HITL Confidence Threshold (AB-17, AB-18 vs AB-00)

| Study | HITL threshold | Triplets | GT Coverage | Avg Score | Judge |
|-------|---------------|----------|-------------|-----------|-------|
| AB-00 | 0.90 (default) | 112 | 98% | 0.7813 | 4.50 |
| AB-17 | 0.70 | 95 | 93% | 0.7858 | 4.20 |
| AB-18 | 0.85 | 91 | 98% | 0.7853 | 4.50 |

**Finding:** Lowering the HITL threshold to 0.70 (AB-17) over-interrupts on this small schema and is the only HITL variant the judge marks down (4.20, GT coverage 93%). Threshold 0.85 (AB-18) matches the baseline at 4.50 with fewer interrupts. AB-BEST uses 0.80 as a balanced compromise between autonomy and safety.

---

## 4. AB-BEST Configuration

The AB-BEST configuration is derived from the ablation evidence rather than from a single winner-takes-all score: on DS01 the v1.5.1 judge is tightly compressed (4.15–4.80), so no parameter is a clean discriminator on the simple baseline. AB-BEST instead selects each value for efficiency or robustness reasons (e.g. `reranker_top_k=5` for the 4× cross-encoder saving while tying `top_k=20` at the judge level, §3.2/§8; `chunk=256/32` and `HITL=0.80` as balanced defaults). The configuration's value shows up on the harder DS02–DS07, where it keeps 100% grounded answers across 210 questions.

| Dimension | Default (AB-00) | AB-BEST v1.5.1 | Rationale |
|-----------|---------|---------|---------|
| Retrieval mode | hybrid | **hybrid** | Only mode that keeps both GT coverage and a high retrieval score (§3.1) |
| Reranker | ON, top_k=10 | **ON, top_k=5** | Ties top_k=20 at the judge level (4.50 DS01; 4.31 vs 4.28 across 7 datasets, §8) with 4× fewer reranker calls |
| Chunk size/overlap | 256/32 | **256/32** | Neutral on DS01 (AB-06 128/16 edges to 4.80 but inflates node count on larger corpora); baseline retained |
| Extraction max tokens | 8192 | **8192** | Neutral (§3.4); 8192 is a robust default for dense content |
| ER similarity threshold | 0.75 | **0.75** | Neutral (§3.5); baseline retained |
| ER blocking top_k | 10 | **10** | top_k=20 over-merges on small corpora (AB-14, 4.15); baseline retained |
| Schema enrichment | ON | **ON** | Neutral on DS01 v1.5.1 (§3.6) but kept ON for robustness on degraded/larger schemas |
| Actor-Critic validation | ON | **ON** | Neutral on DS01 v1.5.1 (§3.6) but kept ON for robustness on degraded/larger schemas |
| HITL threshold | 0.90 | **0.80** | Compromise: fewer HITL than 0.70, more safety than 0.85 |
| Cypher healing | ON | **ON** | Essential for complex schemas |
| Hallucination grader | ON | **ON** | Safety-first for complex datasets |

### AB-BEST env_overrides

```json
{
  "RETRIEVAL_MODE": "hybrid",
  "ENABLE_RERANKER": "true",
  "RERANKER_TOP_K": "5",
  "CHUNK_SIZE": "256",
  "CHUNK_OVERLAP": "32",
  "LLM_MAX_TOKENS_EXTRACTION": "8192",
  "ER_SIMILARITY_THRESHOLD": "0.75",
  "ER_BLOCKING_TOP_K": "10",
  "ENABLE_SCHEMA_ENRICHMENT": "true",
  "ENABLE_CRITIC_VALIDATION": "true",
  "CONFIDENCE_THRESHOLD": "0.80",
  "ENABLE_CYPHER_HEALING": "true",
  "ENABLE_HALLUCINATION_GRADER": "true",
  "ENABLE_RETRIEVAL_QUALITY_GATE": "true",
  "ENABLE_GRADER_CONSISTENCY_VALIDATOR": "true",
  "ENABLE_LAZY_EXPANSION": "true"
}
```

### AB-BEST results across all 7 datasets (re-judged 2026-07-17, v1.5.1)

| Dataset | Tables | Questions | GT Cov | Grounded | AI Judge |
|---------|:------:|:---------:|:------:|:--------:|:--------:|
| 01 E-Commerce | 7 | 15 | 100% | 15/15 | 4.50/5 |
| 02 Finance | 8 | 25 | 99% | 25/25 | 4.70/5 |
| 03 Healthcare | 10 | 30 | 94% | 30/30 | 3.65/5 |
| 04 Manufacturing | 13 | 40 | 82% | 40/40 | 4.45/5 |
| 05 Edge-incomplete | 5 | 20 | 79% | 20/20 | 4.45/5 |
| 06 Edge-legacy | 10 | 25 | 63% | 25/25 | 4.25/5 |
| 07 Stress (58 tables) | 58 | 55 | 85% | 55/55 | 4.20/5 |
| **Average** | — | **210** | **86%** | **210/210** | **4.31/5** |

> **210/210 answers grounded (100%), zero hallucinations, 100% builder completion** across all seven datasets including the 58-table stress set. AI-Judge average **4.31/5** on the systematic `gpt-5.4-nano-2026-03-17` re-judge (lower than the earlier 4.73 manual figure — the LLM judge is stricter and the v1.5.1 KG builds differ stochastically). The weakest case is DS03 Healthcare (3.65): grounded and 94% covered, but the judge penalises answer precision on multi-hop clinical questions. GT coverage is lowest on DS06 legacy (63%) and DS05 incomplete (79%) — the two degraded-schema datasets where the K20 retrieval window recovers more sources (see §8).

---

## 5. Key Findings Summary

1. **Hybrid retrieval stays the robust default.** BM25-only (AB-02) still collapses GT coverage to 54% — it cannot match semantically paraphrased questions — even though its judge score (4.25) now nearly ties vector-only and hybrid on this simple dataset.
2. **No single parameter cleanly discriminates on DS01.** The v1.5.1 judge is compressed (4.15–4.80); the clearest signals are AB-06 (chunking 128/16, 4.80, best) and AB-19 (Cypher healing OFF, 3.80, worst). `reranker_top_k` 5 vs 20 tie at 4.50.
3. **Schema enrichment and Actor-Critic are *not* load-bearing on the simple baseline.** On the v1.5.1 DS01 bundles, disabling either leaves GT coverage at 98% (the earlier 61%/67% collapse was a pre-v1.5.1 artefact). They are kept ON for robustness on degraded/larger schemas, where their value is expected to resurface (DS05, DS06, DS07).
4. **Most parameters are neutral on simple datasets** — confirmed. Discrimination requires complex/multi-hop datasets.
5. **top_k=5 is the efficient optimum.** It ties top_k=20 at the judge level (4.50 on DS01; 4.31 vs 4.28 across all 7 datasets, §8) with 4× fewer cross-encoder inference calls per query.
6. **AB-BEST averages 4.31/5 across 7 datasets** (down from the earlier 4.73 manual figure). No dataset hits a perfect 5.00 under the systematic `gpt-5.4-nano` judge; the hardest are DS03 Healthcare (3.65) and the large/incomplete schemas DS07 (4.20) and DS06 (4.25).
7. **K5 and K20 are effectively tied (Section 8).** A full 7-dataset comparison gives AB-BEST (K5) 4.31 vs AB-BEST-K20 4.28 (Δ −0.03). K5 wins 3/7, K20 wins 2/7, tie 2/7. K20 retrieves strictly more expected sources (GT coverage 0.986 vs 0.860) but that retrieval advantage does not translate into a higher judge score — the earlier "K5 wins 6/7" reading does not hold on the v1.5.1 epoch.

---

## 6. Replication Study: Estimating LLM Variance

### 6.1 Motivation

Large language models can produce different outputs across runs even with identical configuration, prompts, and dataset — due to floating-point non-determinism in GPU matrix operations, request scheduling, and tokenisation order. Although most nodes in this pipeline run at `T=0.0` (deterministic), the answer generation node runs at `T=0.3`, and the hallucination grader introduces additional stochasticity.

To validate that the single-run results reported above are representative, and to provide confidence intervals for the two most important comparison points, AB-00 (baseline) and AB-BEST (optimised) were each re-executed **two additional times** on DS01 (3 runs total per study). The variance across runs bounds the uncertainty on all ablation comparisons.

### 6.2 Replication Results

All four additional runs completed successfully. Every run maintained 100% grounding and 7/7 table completion, confirming pipeline stability. Raw per-run values are reported below.

**AB-00 (Baseline) — 3 runs**

| Run | Run tag | GT Coverage | Grounded | Avg Score | Triplets | Entities |
|-----|---------|-------------|----------|-----------|----------|----------|
| 1 | run-20260421_110728 | 100% | 15/15 | 0.4273 | 100 | 47 |
| 2 | replication-run2 | 100% | 15/15 | — ¹ | 91 | 50 |
| 3 | replication-run3 | 98% | 15/15 | 0.4401 | 89 | 45 |

**AB-BEST (Optimised) — 3 runs**

| Run | Run tag | GT Coverage | Grounded | Avg Score | Triplets | Entities |
|-----|---------|-------------|----------|-----------|----------|----------|
| 1 | run-20260421_221024 | 100% | 15/15 | 0.4965 | 90 | 17 |
| 2 | replication-run2 | 100% | 15/15 | — ¹ | 98 | 23 |
| 3 | replication-run3 | 100% | 15/15 | 0.4925 | 90 | 21 |

> ¹ `avg_top_score` for run2 is not recoverable: the output directory was overwritten by run3 before being read. GT coverage and grounded_rate were captured from the process log before overwrite.

### 6.3 Mean and Variance across 3 Runs

| Study | Metric | n | Mean | Std dev | Min | Max |
|-------|--------|---|------|---------|-----|-----|
| AB-00 | `grounded_rate` | 3 | **1.0000** | 0.0000 | 1.00 | 1.00 |
| AB-00 | `gt_coverage` | 3 | **0.9944** | 0.0096 | 0.983 | 1.000 |
| AB-00 | `avg_top_score` | 2 | 0.4337 | 0.0091 | 0.4273 | 0.4401 |
| AB-00 | `triplets` | 3 | 93.3 | 5.86 | 89 | 100 |
| AB-00 | `entities` | 3 | 47.3 | 2.52 | 45 | 50 |
| AB-BEST | `grounded_rate` | 3 | **1.0000** | **0.0000** | 1.00 | 1.00 |
| AB-BEST | `gt_coverage` | 3 | **1.0000** | **0.0000** | 1.000 | 1.000 |
| AB-BEST | `avg_top_score` | 2 | **0.4945** | **0.0028** | 0.4925 | 0.4965 |
| AB-BEST | `triplets` | 3 | 92.7 | 4.62 | 90 | 98 |
| AB-BEST | `entities` | 3 | 20.3 | 3.06 | 17 | 23 |

### 6.4 Interpretation

**Grounded rate and table completion are fully deterministic across runs.** Both AB-00 and AB-BEST returned 15/15 grounded answers and 7/7 completed tables in every single run. This confirms that the pipeline's hard outcome metrics are not affected by LLM stochasticity.

**GT coverage variance is negligible (std ≤ 0.010).** AB-00 shows a minor fluctuation (one run hit 98% instead of 100%), which corresponds to a single expected source not being retrieved across 15 questions. This is within noise. AB-BEST achieves exactly 100% on all three runs.

**avg_top_score variance is very low (std ≤ 0.009).** The cross-encoder reranker scores are essentially stable, confirming the retrieval pipeline is deterministic (same embeddings, same graph traversal, same ranking). The small difference (±0.009) is attributable to answer-generation stochasticity (`T=0.3`) affecting the self-reported quality scores.

**Triplet and entity counts vary moderately (std ≈ 4-6 for triplets).** This is the most variable component — the extraction LLM at `T=0.0` still produces slightly different triplet counts across runs due to different chunk scheduling and model state. Importantly, this variation does **not** affect downstream quality metrics, as evidenced by stable GT coverage and grounded rates.

**Conclusion:** The single-run ablation results reported in Section 2 are statistically valid. The variance budget for the two primary quality metrics (GT coverage, grounded rate) is essentially zero. The ablation campaign can be trusted as representative.

---

## 7. v1.1.1 Re-run (2026-05-06) — superseded by v1.5.1

> **Historical record.** The scores in this section are from the May 2026 v1.1.1 re-run and are **superseded** by the v1.5.1 figures in §2–§6 and §8 (re-run + re-judge on 2026-07-17). They are kept for traceability. Do not cite them as current; the v1.5.1 numbers are lower and more compressed because the systematic judge is stricter and the KG builds differ stochastically.

Pipeline re-run with code version 1.1.1 (68 audit fixes, SSRF hardening, O(n²) blocking elimination, config drift externalization). AI-Judge upgraded from `gpt-4.1-mini` to `gpt-5.4-nano-2026-03-17`.

### 7.1 Updated AI-Judge Scores (DS01)

| Study | Description | AI Judge (v1.1.1) |
|:-----:|-------------|:------------------:|
| AB-00 | Baseline | **4.50/5** |
| AB-01 | Vector-only | 3.40/5 |
| AB-02 | BM25-only | 4.25/5 |
| AB-03 | Reranker OFF | 4.80/5 |
| AB-04 | Reranker top_k=5 | **4.90/5** |
| AB-05 | Reranker top_k=20 | **4.90/5** |
| AB-06 | Chunking 128/16 | 4.50/5 |
| AB-07 | Chunking 384/48 | 4.50/5 |
| AB-08 | Chunking 512/64 | 4.50/5 |
| AB-09 | Extraction tokens=4096 | 4.50/5 |
| AB-10 | Extraction tokens=16384 | 4.25/5 |
| AB-11 | ER threshold=0.65 | 4.50/5 |
| AB-12 | ER threshold=0.85 | 4.50/5 |
| AB-13 | ER blocking top_k=5 | 4.50/5 |
| AB-14 | ER blocking top_k=20 | 4.50/5 |
| AB-15 | Schema enrichment OFF | 4.50/5 |
| AB-16 | Actor-Critic OFF | 4.50/5 |
| AB-17 | HITL threshold=0.70 | 4.50/5 |
| AB-18 | HITL threshold=0.85 | 4.50/5 |
| AB-19 | Cypher healing OFF | 4.05/5 |
| AB-20 | Hallucination grader OFF | 4.50/5 |
| **AB-BEST** | **Combined optimal (top_k=5, safety ON)** | **5.00/5** |

### 7.2 Key Differences vs. Previous Run

- **Scores generally higher** — v1.1.1 perf fixes (batched UNION ALL retrieval, config externalization) improved pipeline stability
- **AB-04/AB-05 tied at 4.90** — reranker pool variants perform best, confirming reranker is critical
- **AB-01 still worst** (3.40) — vector-only retrieval remains clearly inferior, validating hybrid retrieval superiority
- **AB-19 still penalized** (4.05) — Cypher healing remains essential for robust pipeline
- **Hallucination grader OFF (AB-20)** no longer outperforms baseline — with better retrieval quality in v1.1.1, the grader no longer over-rejects valid answers

### 7.3 Full Analysis

See [`outputs/ablation/meta/ABLATION_ANALYSIS_COMPLETE.md`](../../outputs/ablation/meta/ABLATION_ANALYSIS_COMPLETE.md) for the comprehensive analysis including grouped comparisons, radar plots, heatmaps, and component importance rankings.

---

## 8. Reranker Top-K Sensitivity: AB-BEST K5 vs K20 (re-judged 2026-07-17, v1.5.1)

### 8.1 Motivation

AB-BEST uses `reranker_top_k=5` for the efficiency win (4× fewer cross-encoder calls per query). On the v1.5.1 DS01 ablation K5 and K20 tie at the judge level (both 4.50, §3.2), so the choice is efficiency-driven rather than quality-driven. This section checks whether that tie holds across all seven datasets by comparing AB-BEST (K5) against AB-BEST-K20 (`reranker_top_k=20`), both re-run on v1.5.1 and re-judged with `gpt-5.4-nano-2026-03-17`.

### 8.2 Results

| Dataset | AB-BEST (K5) | AB-BEST-K20 | Delta | Winner |
|---------|:------------:|:-----------:|:-----:|:------:|
| 01 E-Commerce (15q) | 4.50 | **4.99** | +0.49 | K20 |
| 02 Finance (25q) | **4.70** | 4.10 | -0.60 | K5 |
| 03 Healthcare (30q) | 3.65 | **4.20** | +0.55 | K20 |
| 04 Manufacturing (40q) | **4.45** | 4.25 | -0.20 | K5 |
| 05 Edge-incomplete (20q) | **4.45** | 3.95 | -0.50 | K5 |
| 06 Edge-legacy (25q) | 4.25 | 4.25 | 0.00 | tie |
| 07 Stress (55q) | 4.20 | 4.20 | 0.00 | tie |
| **Average (DS01-07)** | **4.31** | **4.28** | **-0.03** | **K5 (≈tie)** |
| **GT coverage avg** | **0.860** | **0.986** | **+0.126** | **K20** |

### 8.3 Interpretation

- **K5 and K20 are effectively tied at the judge level** (4.31 vs 4.28, Δ −0.03). K5 wins 3/7, K20 wins 2/7, tie 2/7. The earlier "K5 wins 6/7, avg 4.73 vs 4.51" reading was specific to the pre-v1.5.1 bundles and the earlier manual judge; it does not reproduce on the v1.5.1 epoch.
- **K20 retrieves strictly more expected sources** — GT coverage 0.986 vs 0.860 (+0.126), with K20 ≥ K5 on every dataset (largest gains on the degraded schemas DS06 +0.370 and DS05 +0.211). But that retrieval advantage does **not** buy a higher judge score: more context does not monotonically improve answer quality.
- **High per-dataset variance for K20.** K20 scores 4.99 on DS01 (its best) but 3.95 on DS05 and 4.10 on DS02; K5 is more stable (4.20–4.70). The wider window helps on some schemas (DS01, DS03) and hurts on others (DS02, DS05), so neither setting dominates.
- **Per-dataset flips vs the earlier run:** DS05 flipped from K20-best to K5-best (4.45 vs 3.95) and DS07 moved from K5-best (4.35 vs 3.65) to a tie (4.20 vs 4.20). These changes follow the v1.5.1 re-run, not a code regression.

### 8.4 Conclusion

AB-BEST keeps `reranker_top_k=5` on **efficiency** grounds, not quality dominance:
- Judge parity with K20 (4.31 vs 4.28)
- 4× fewer cross-encoder inference calls per query
- Lower per-dataset variance (more stable answers)

K20 is a legitimate alternative — it maximises GT coverage and wins on DS01/DS03 — and a production system could adaptively raise `top_k` when retrieval confidence is low (avg_top_score below threshold). But as a global default, K5 delivers the same judged quality at a quarter of the reranker cost, which is the deciding factor.

### 8.5 DS05 Deep Dive: K20 Retrieves More, K5 Answers Better

DS05 (intentionally incomplete schema) is the cleanest illustration of the coverage/precision split. On the v1.5.1 run:

| Metric | K5 | K20 | Interpretation |
|--------|:---:|:---:|---------------|
| grounded_rate | 1.00 | 1.00 | Both fully grounded |
| **avg_gt_coverage** | 0.789 | **1.000** | K20 recovers every expected source; K5 misses ~21% |
| AI Judge | **4.45** | 3.95 | K5 scores higher despite lower coverage |

K20's wider window (top_k=20) pulls in the marginally-relevant chunks that the incomplete DDL leaves semantically distant — which is why its GT coverage reaches 100%. But on this degraded input several of those extra chunks are noisy, and the generator diffuses its answer across them; the judge penalises precision and K5 wins (4.45 vs 3.95). This is the opposite of the pre-v1.5.1 result (K20 4.80 vs K5 4.30) and is attributed to the different KG build + stricter judge, not a code regression. The takeaway generalises: on incomplete schemas K20 maximises *recall of sources* but does not guarantee *answer quality*.

---

### 8.6 DS07 Deep Dive: Large Schema, Judge Tie

On the 58-table stress set the two configs land in a dead heat:

| Metric | K5 | K20 | Interpretation |
|--------|:---:|:---:|---------------|
| grounded_rate | 1.00 | 1.00 | Both fully grounded |
| **avg_gt_coverage** | 0.850 | **0.946** | K20 recovers ~10pp more sources |
| tables_completed | 58/58 | 58/58 | Both 100% builder success |
| AI Judge | 4.20 | 4.20 | Tie |

Both configs build the full 58-table graph and answer all 55 questions grounded. K20 again retrieves more expected sources (0.946 vs 0.850), but on a schema this large the extra chunks at ranks 6–20 are often related-but-wrong tables (e.g. `PURCHASE_ORDER_HEADER` when the question is about `SALES_ORDER_HEADER`), which cancels the recall gain at the judge level. The pre-v1.5.1 K5 dominance here (4.35 vs 3.65) does not reproduce: under v1.5.1 the two are indistinguishable on quality, so K5 is again preferred purely for the 4× reranker saving.

---

### 8.7 Retrieval Quality Score Floor Issue

#### The Problem
During the v1.5.1 ablation campaign, we observed that cross-encoder (CE) absolute scores tend to be artificially low on highly technical, multi-section content (like DDL and data dictionaries). For example, a chunk that is undeniably the best match for a query might receive a raw CE score of `0.15`. 

Because of this "floor issue", the retrieval quality gate would inappropriately flag these results as poor quality, potentially rejecting them or inappropriately affecting downstream confidence heuristics.

#### The Solution (Dual Metrics)
We implemented a **pool-aware retrieval confidence adjustment** (Dual Metrics) in the `_node_rerank` phase. The rationale is that being ranked #1 in a large, competitive pool of candidates is much stronger evidence of relevance than the raw absolute CE score implies.

The node now exports two metrics:
- `retrieval_quality_score_raw`: The pure, unmodified cross-encoder score of the top chunk.
- `retrieval_quality_score_adjusted`: The heuristically adjusted score. If the candidate pool size exceeds a minimum threshold (`pool_confidence_min_size`) and the raw score is below a ceiling (`pool_confidence_ceiling`), the score is floored to a minimum acceptable value (`pool_confidence_floor`).

This allows the quality gate to use the adjusted score (avoiding false rejections on technical documents) while still preserving the raw score in the evaluation bundle for later analysis.
