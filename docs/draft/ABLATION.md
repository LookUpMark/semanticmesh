# Ablation Studies Plan

> **Project:** Multi-Agent Framework for Semantic Discovery & GraphRAG
> **Version:** 1.0 — March 2026
> **Companion documents:** [SPECS.md](./SPECS.md), [REQUIREMENTS.md](./REQUIREMENTS.md), [DATASET.md](./DATASET.md), [TEST_PLAN.md](./TEST_PLAN.md)
> **Purpose:** Define formal ablation experiments to quantify the contribution of each architectural component. Results feed into the thesis evaluation chapter.

---

## Table of Contents

1. [Motivation](#1-motivation)
2. [Ablation Matrix](#2-ablation-matrix)
3. [AB-01 — Schema Enrichment Impact](#ab-01--schema-enrichment-impact)
4. [AB-02 — Hybrid Retrieval vs Vector-Only](#ab-02--hybrid-retrieval-vs-vector-only)
5. [AB-03 — Cypher Healing Loop Contribution](#ab-03--cypher-healing-loop-contribution)
6. [AB-04 — Actor-Critic Validation Impact](#ab-04--actor-critic-validation-impact)
7. [AB-05 — Cross-Encoder Reranking Value](#ab-05--cross-encoder-reranking-value)
8. [AB-06 — Hallucination Grader Effectiveness](#ab-06--hallucination-grader-effectiveness)
9. [Execution Protocol](#7-execution-protocol)
10. [Reporting Template](#8-reporting-template)

---

## 1. Motivation

The system is built from many interacting components (enrichment, hybrid retrieval, reranking, healing loops, actor-critic validation, hallucination grading). Each adds latency and LLM cost. Ablation studies isolate each component's **marginal contribution** to output quality, answering:

- *Does removing component X significantly degrade quality?*
- *Is the latency/cost trade-off justified?*
- *Which components are essential vs nice-to-have?*

These experiments produce the **quantitative results** that form the core of the thesis evaluation chapter. Without them, architectural claims remain anecdotal.

---

## 2. Ablation Matrix

Overview of all planned experiments:

| ID | Component Ablated | Baseline | Variant | Primary Metric | Secondary Metrics |
|---|---|---|---|---|---|
| AB-01 | Schema Enrichment | Full pipeline | Skip `enrich_schema` node | Mapping accuracy (% correct concept assignments) | Embedding cosine similarity (enriched vs original), HITL correction rate |
| AB-02 | Hybrid Retrieval | Vector + BM25 + Reranker | Vector-only (no BM25, no reranker) | Context Relevancy (RAGAS), Answer Correctness | Faithfulness, Recall@K |
| AB-03 | Cypher Healing | Up to 3 retries | No healing (fail on first error) | Cypher execution success rate (%) | `cypher_healing_rate` (custom metric), avg healing rounds |
| AB-04 | Actor-Critic | Critic validation enabled | Skip critic (accept all proposals) | Mapping precision, false positive rate | `hitl_confidence_agreement`, avg confidence |
| AB-05 | Cross-Encoder Reranker | Reranker enabled | Retrieve Top-K directly from hybrid pool | Answer Correctness (RAGAS), Faithfulness | Latency (ms), Context Relevancy |
| AB-06 | Hallucination Grader | Grader loop enabled | Return first answer without grading | Faithfulness (RAGAS) | Answer Correctness, avg grading rounds |

---

## AB-01 — Schema Enrichment Impact

### Hypothesis
LLM Schema Enrichment resolves the lexical gap between cryptic DDL identifiers (`TB_CST`, `ORD_DT`) and business glossary terminology. Without it, embedding similarity between table metadata and business concepts degrades, leading to lower mapping quality.

### Setup

| Condition | Description |
|---|---|
| **Baseline** | Full pipeline with `enrich_schema` node active |
| **Variant** | `enrich_schema` node disabled; `TableSchema` passed directly to `rag_mapping` without enrichment |

### Metrics

| Metric | How to Measure |
|---|---|
| **Mapping accuracy** | % of tables correctly mapped to their gold-standard concept (from `gold_standard.json`) |
| **Embedding similarity** | Average cosine similarity between table query embedding and correct concept embedding (enriched names vs original names) |
| **HITL correction rate** | % of mappings that the human reviewer overrides — lower is better |

### Expected Outcome
With enrichment: mapping accuracy ≥ 85%. Without enrichment: accuracy drops by 15-25% on tables with heavily abbreviated names (e.g., `TB_CST_ORD` vs `Customer Orders`).

### Implementation Notes
- Toggle via `settings.ENABLE_SCHEMA_ENRICHMENT: bool = True`
- In `builder_graph.py`, conditionally skip the `enrich_schema` node when flag is `False`
- Run both conditions on the **same DDL dataset** (`complex_schema.sql` — 9 tables)
- Record per-table results for granular analysis

---

## AB-02 — Hybrid Retrieval vs Vector-Only

### Hypothesis
BM25 captures exact lexical matches (e.g., column names, acronyms) that dense vector retrieval may miss. The hybrid approach combined with cross-encoder reranking returns higher-quality context chunks than vector-only search.

### Setup

| Condition | Description |
|---|---|
| **Baseline** | Hybrid retrieval: Vector Top-K + BM25 Top-K → merged → Cross-Encoder rerank → Top-N |
| **Variant A** | Vector-only: Vector Top-K → Top-N (no BM25, no reranker) |
| **Variant B** | Vector + BM25, no reranker: merged pool → Top-N by raw score fusion |

### Metrics

| Metric | Source |
|---|---|
| **Context Relevancy** | RAGAS |
| **Answer Correctness** | RAGAS |
| **Faithfulness** | RAGAS |
| **Recall@K** | Custom: % of gold-relevant chunks present in Top-K retrieved |
| **Latency** | Wall-clock time per query (ms) |

### Expected Outcome
Hybrid + reranker should yield the best Context Relevancy and Faithfulness. Vector-only should have lowest latency but worst recall on queries containing exact technical terms.

### Implementation Notes
- Toggle via `settings.RETRIEVAL_MODE: Literal["hybrid", "vector_only", "hybrid_no_rerank"]`
- Use the **same 20 gold-standard QA pairs** for all conditions
- Report results as mean ± std across all 20 queries

---

## AB-03 — Cypher Healing Loop Contribution

### Hypothesis
LLM-generated Cypher often contains syntax errors or references non-existent properties/labels. The healing loop (retry with error message) recovers a significant percentage of failed queries that would otherwise be lost.

### Setup

| Condition | Description |
|---|---|
| **Baseline** | Cypher generation with up to 3 healing retries |
| **Variant** | No healing: first Cypher failure → immediate error to user |

### Metrics

| Metric | How to Measure |
|---|---|
| **Execution success rate** | % of generated Cypher statements that execute without error |
| **`cypher_healing_rate`** | Custom metric: `healed_count / (healed_count + failed_count)` |
| **Avg healing rounds** | Mean number of retries before success (baseline only) |
| **Latency overhead** | Additional time (ms) introduced by healing retries |

### Expected Outcome
Without healing, success rate drops by 20-40%. Most Cypher failures are fixable within 1-2 retries (trivial syntax issues).

### Implementation Notes
- Toggle via `settings.ENABLE_CYPHER_HEALING: bool = True`
- When disabled, `Fix_Cypher_LLM` node is replaced with a direct error edge
- Test on the full DDL dataset (all 9 tables → Cypher for each mapping)

---

## AB-04 — Actor-Critic Validation Impact

### Hypothesis
The Actor-Critic loop catches low-confidence or incorrect mapping proposals before they reach the knowledge graph. Without the Critic, false-positive mappings increase and the HITL reviewer must catch more errors.

### Setup

| Condition | Description |
|---|---|
| **Baseline** | Critic validation enabled: proposals below `CONFIDENCE_THRESHOLD` are rejected/refined |
| **Variant** | Skip critic: all `MappingProposal`s accepted as-is |

### Metrics

| Metric | How to Measure |
|---|---|
| **Mapping precision** | % of accepted mappings that are correct (gold standard comparison) |
| **False positive rate** | % of accepted mappings that are incorrect |
| **`hitl_confidence_agreement`** | Custom: does the human agree with the system's confidence? |
| **Avg confidence** | Mean confidence score of accepted mappings |

### Expected Outcome
Without the Critic, false positives increase by 10-20%. The Critic is especially valuable for borderline cases (confidence 0.6-0.85).

---

## AB-05 — Cross-Encoder Reranking Value

### Hypothesis
The cross-encoder reranker (BGE-reranker-large) significantly improves ranking quality over raw embedding similarity + BM25 score fusion, at the cost of additional latency.

### Setup

| Condition | Description |
|---|---|
| **Baseline** | Full hybrid retrieval with cross-encoder reranking |
| **Variant** | Hybrid retrieval → merged pool sorted by reciprocal rank fusion (no cross-encoder) |

### Metrics

| Metric | Source |
|---|---|
| **Context Relevancy** | RAGAS |
| **Answer Correctness** | RAGAS |
| **Latency per query** | Wall-clock (ms) |
| **NDCG@5** | Custom: normalized discounted cumulative gain at Top-5 |

### Expected Outcome
Reranker improves Context Relevancy by 5-15% but adds 50-200ms per query. Trade-off is justified for batch governance queries but may matter for interactive use.

---

## AB-06 — Hallucination Grader Effectiveness

### Hypothesis
The hallucination grading loop filters unfaithful answers and triggers regeneration, reducing the rate of hallucinated content in final responses.

### Setup

| Condition | Description |
|---|---|
| **Baseline** | Hallucination grader active: up to 3 regeneration cycles |
| **Variant** | Return first generated answer without grading |

### Metrics

| Metric | Source |
|---|---|
| **Faithfulness** | RAGAS |
| **Answer Correctness** | RAGAS |
| **Avg grading rounds** | Mean number of regeneration attempts (baseline only) |
| **Latency overhead** | Additional time (ms) from grading loop |

### Expected Outcome
Without grading, Faithfulness score drops by 10-20%. Most unfaithful answers are caught in the first grading round.

---

## 7. Execution Protocol

### 7.1 Environment

- All ablation runs executed on the **same hardware** (GPU/CPU specs to be documented)
- Same LLM model and temperature settings across all runs
- Same seed/checkpoint for reproducibility (`MemorySaver` snapshots)
- Neo4j testcontainer with identical data preloaded

### 7.2 Dataset

Use the **gold-standard dataset** defined in [DATASET.md](./DATASET.md):
- **Builder ablations (AB-01, AB-03, AB-04):** 9-table DDL + business glossary PDF → 50 gold mappings
- **Query ablations (AB-02, AB-05, AB-06):** 20 gold-standard QA pairs with expected answers + source chunks

### 7.3 Run Procedure

1. Run baseline (full pipeline) — record all metrics
2. For each ablation variant:
   a. Toggle the relevant setting
   b. Clear Neo4j data (builder ablations) or use same KG (query ablations)
   c. Run identical input through the pipeline
   d. Record all metrics
3. Statistical comparison: paired t-test or Wilcoxon signed-rank test (n ≥ 20)
4. Report effect size (Cohen's d) alongside p-value

### 7.4 Number of Runs

- Each condition run **3 times minimum** (to account for LLM non-determinism even at T=0.0)
- Report mean ± std for all metrics

---

## 8. Reporting Template

Each ablation result should be documented in the following format:

### AB-XX — [Component Name]

**Date:** YYYY-MM-DD
**Hardware:** [GPU model, RAM, CPU]
**LLM Configuration:** [model slug, temperature, openrouter_api_key (masked)]

#### Results

| Metric | Baseline (mean ± std) | Variant (mean ± std) | Δ | p-value | Effect Size |
|---|---|---|---|---|---|
| Primary metric | | | | | |
| Secondary metric 1 | | | | | |
| Secondary metric 2 | | | | | |

#### Observations
- [Key findings in 2-3 bullet points]

#### Conclusion
- [Is the component's contribution statistically significant?]
- [Is the latency/cost trade-off justified?]

---

## Appendix: Configuration Flags for Ablation

All ablation toggles centralised in `src/config/settings.py`:

```python
# ── Ablation Flags ────────────────────────────────────────────────────────────
ENABLE_SCHEMA_ENRICHMENT: bool = True       # AB-01: set False to skip
RETRIEVAL_MODE: str = "hybrid"              # AB-02: "hybrid" | "vector_only" | "hybrid_no_rerank"
ENABLE_CYPHER_HEALING: bool = True          # AB-03: set False to skip
ENABLE_CRITIC_VALIDATION: bool = True       # AB-04: set False to skip
ENABLE_RERANKER: bool = True                # AB-05: set False to skip
ENABLE_HALLUCINATION_GRADER: bool = True    # AB-06: set False to skip
```

These flags **must not affect production defaults** — they exist solely for controlled experiments. Default values are all `True` / `"hybrid"`.
