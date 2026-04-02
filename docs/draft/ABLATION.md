# Ablation Studies Plan

> **Project:** Multi-Agent Framework for Semantic Discovery & GraphRAG
> **Version:** 2.0 — Updated March 2026
> **Companion documents:** [SPECS.md](./SPECS.md), [REQUIREMENTS.md](./REQUIREMENTS.md), [DATASET.md](./DATASET.md), [TEST_PLAN.md](./TEST_PLAN.md)
> **Purpose:** Define formal ablation experiments to quantify the contribution of each architectural component. Results feed into the thesis evaluation chapter.

---

## Table of Contents

1. [Motivation](#1-motivation)
2. [Ablation Matrix](#2-ablation-matrix)
3. [Study Descriptions](#3-study-descriptions)
4. [Configuration Flags](#4-configuration-flags)
5. [Dataset & Evaluation Protocol](#5-dataset--evaluation-protocol)
6. [Results Summary](#6-results-summary)
7. [Execution Protocol](#7-execution-protocol)
8. [Reporting Template](#8-reporting-template)

---

## 1. Motivation

The system is built from many interacting components (enrichment, hybrid retrieval, reranking, healing loops, actor-critic validation, hallucination grading, entity resolution, chunking strategies). Each adds latency and LLM cost. Ablation studies isolate each component's **marginal contribution** to output quality, answering:

- *Does removing component X significantly degrade quality?*
- *Is the latency/cost trade-off justified?*
- *What are the optimal hyperparameters for each component?*
- *Which components are essential vs nice-to-have?*

The 21 studies in this plan cover binary toggles (ON/OFF) and parametric sweeps across six dimensions: retrieval mode, reranking, chunking, extraction capacity, entity resolution, and validation/grading pipeline stages.

---

## 2. Ablation Matrix

All 21 experiments are defined in `src/evaluation/ablation_runner.py` as `ABLATION_MATRIX`. Each study varies exactly one dimension from the baseline (AB-00).

| ID | Component / Parameter | Description | Primary Metric | RAGAS |
|---|---|---|---|---|
| **AB-00** | — | Baseline: default settings (hybrid retrieval, reranker ON, chunking 256/32) | faithfulness | Yes |
| **AB-01** | Retrieval mode | Vector-only retrieval — no BM25, no graph traversal | context_precision | Yes |
| **AB-02** | Retrieval mode | BM25-only retrieval — no vector, no graph traversal | context_precision | Yes |
| **AB-03** | Reranker | Reranker OFF — raw hybrid pool ranking | context_precision | Yes |
| **AB-04** | Reranker pool | Reranker `top_k=5` — smaller reranking pool | context_precision | No |
| **AB-05** | Reranker pool | Reranker `top_k=20` — larger reranking pool | context_precision | No |
| **AB-06** | Chunking | Chunk size 128 / overlap 16 — smaller chunks | context_recall | Yes |
| **AB-07** | Chunking | Chunk size 384 / overlap 48 — larger chunks | context_recall | Yes |
| **AB-08** | Chunking | Chunk size 512 / overlap 64 — largest chunks | context_recall | Yes |
| **AB-09** | Extraction tokens | `max_tokens_extraction=4096` — conservative limit | faithfulness | No |
| **AB-10** | Extraction tokens | `max_tokens_extraction=16384` — generous limit | faithfulness | No |
| **AB-11** | ER similarity | `er_similarity_threshold=0.65` — aggressive merging | context_precision | No |
| **AB-12** | ER similarity | `er_similarity_threshold=0.85` — conservative merging | context_precision | No |
| **AB-13** | ER blocking | `er_blocking_top_k=5` — smaller candidate set | context_precision | No |
| **AB-14** | ER blocking | `er_blocking_top_k=20` — larger candidate set | context_precision | No |
| **AB-15** | Schema enrichment | Schema enrichment OFF — no LLM acronym expansion | context_precision | Yes |
| **AB-16** | Actor-Critic | Actor-Critic validation OFF — accept all mapping proposals | context_precision | Yes |
| **AB-17** | Confidence threshold | `confidence_threshold=0.70` — more HITL interrupts | faithfulness | No |
| **AB-18** | Confidence threshold | `confidence_threshold=0.85` — fewer HITL interrupts | faithfulness | No |
| **AB-19** | Cypher healing | Cypher healing OFF — immediate fail on syntax error | faithfulness | Yes |
| **AB-20** | Hallucination grader | Hallucination grader OFF — return first answer without grading | faithfulness | No |

---

## 3. Study Descriptions

### 3.1 Retrieval Mode Studies (AB-01, AB-02)

**Hypothesis:** The hybrid retrieval approach (Vector + BM25 + Graph traversal) with RRF fusion outperforms any single channel because each captures different information: dense vectors capture semantic similarity, BM25 captures exact lexical matches, and graph traversal captures topological context.

| Study | `RETRIEVAL_MODE` | Channels Active |
|---|---|---|
| AB-00 (baseline) | `hybrid` | Vector + BM25 + Graph |
| AB-01 | `vector` | Vector only |
| AB-02 | `bm25` | BM25 only |

### 3.2 Reranker Studies (AB-03, AB-04, AB-05)

**Hypothesis:** The cross-encoder reranker (bge-reranker-v2-m3) significantly improves ranking quality over raw RRF fusion at the cost of additional latency. The size of the reranking pool (`top_k`) affects the quality-latency trade-off.

| Study | `ENABLE_RERANKER` | `RERANKER_TOP_K` |
|---|---|---|
| AB-00 (baseline) | `true` | 10 (default) |
| AB-03 | `false` | — |
| AB-04 | `true` | 5 |
| AB-05 | `true` | 20 |

### 3.3 Chunking Studies (AB-06, AB-07, AB-08)

**Hypothesis:** Chunk size affects the density-coverage trade-off. Smaller chunks give more focused context but risk splitting related information across chunks. Larger chunks provide more context per retrieval hit but may dilute relevance.

| Study | `CHUNK_SIZE` | `CHUNK_OVERLAP` |
|---|---|---|
| AB-00 (baseline) | 256 | 32 |
| AB-06 | 128 | 16 |
| AB-07 | 384 | 48 |
| AB-08 | 512 | 64 |

### 3.4 Extraction Token Studies (AB-09, AB-10)

**Hypothesis:** The maximum tokens available for extraction determines how many triplets the SLM can extract per chunk. A conservative limit may truncate rich passages; a generous limit allows complete extraction of dense content.

| Study | `LLM_MAX_TOKENS_EXTRACTION` |
|---|---|
| AB-00 (baseline) | 8192 (default) |
| AB-09 | 4096 |
| AB-10 | 16384 |

### 3.5 Entity Resolution Studies (AB-11 through AB-14)

**Hypothesis:** Entity resolution quality depends on blocking parameters. Lower similarity thresholds produce more merging (risk: false merges), higher thresholds produce less merging (risk: duplicate entities). Blocking `top_k` controls candidate set size for the LLM judge.

| Study | `ER_SIMILARITY_THRESHOLD` | `ER_BLOCKING_TOP_K` |
|---|---|---|
| AB-00 (baseline) | 0.75 | 10 |
| AB-11 | 0.65 | 10 |
| AB-12 | 0.85 | 10 |
| AB-13 | 0.75 | 5 |
| AB-14 | 0.75 | 20 |

### 3.6 Pipeline Component Toggles (AB-15 through AB-20)

These are binary ON/OFF studies testing the marginal contribution of individual pipeline components.

| Study | Component | Setting |
|---|---|---|
| AB-15 | Schema Enrichment | `ENABLE_SCHEMA_ENRICHMENT=false` |
| AB-16 | Actor-Critic Validation | `ENABLE_CRITIC_VALIDATION=false` |
| AB-17 | Confidence (lower) | `CONFIDENCE_THRESHOLD=0.70` |
| AB-18 | Confidence (higher) | `CONFIDENCE_THRESHOLD=0.85` |
| AB-19 | Cypher Healing | `ENABLE_CYPHER_HEALING=false` |
| AB-20 | Hallucination Grader | `ENABLE_HALLUCINATION_GRADER=false` |

---

## 4. Configuration Flags

All ablation toggles are centralised in `src/config/settings.py` as `Settings` fields. Each study overrides exactly one or two environment variables:

```python
# ── Ablation Flags (src/config/settings.py) ────────────────────────────────────
enable_schema_enrichment: bool = True       # AB-15: set False to skip
enable_cypher_healing: bool = True          # AB-19: set False to skip
enable_critic_validation: bool = True       # AB-16: set False to skip
enable_reranker: bool = True                # AB-03: set False to skip
enable_hallucination_grader: bool = True    # AB-20: set False to skip
enable_retrieval_quality_gate: bool = True
enable_grader_consistency_validator: bool = True
enable_spacy_heuristics: bool = True
enable_lazy_expansion: bool = True
use_lazy_extraction: bool = False
retrieval_mode: str = "hybrid"              # AB-01/02: "vector" | "bm25"

# ── Tunable Parameters ──────────────────────────────────────────────────────────
chunk_size: int = 256                       # AB-06/07/08
chunk_overlap: int = 32
reranker_top_k: int = 10                    # AB-04/05
er_similarity_threshold: float = 0.75       # AB-11/12
er_blocking_top_k: int = 10                # AB-13/14
confidence_threshold: float = 0.90          # AB-17/18
llm_max_tokens_extraction: int = 8192       # AB-09/10
```

These flags **must not affect production defaults** — they exist solely for controlled experiments. Default values represent the full (baseline) pipeline.

---

## 5. Dataset & Evaluation Protocol

### 5.1 Evaluation Datasets

Each ablation study is executed against **six synthetic datasets** of increasing complexity:

| ID | Name | Tables | Complexity |
|---|---|---|---|
| DS01 | `01_basics_ecommerce` | 7 | Basic e-commerce schema |
| DS02 | `02_intermediate_finance` | — | Intermediate finance domain |
| DS03 | `03_advanced_healthcare` | — | Advanced healthcare domain |
| DS04 | `04_edge_cases_temporal` | — | Temporal/edge-case patterns |
| DS05 | `05_cross_domain_logistics` | — | Cross-domain logistics |
| DS06 | `06_stress_test_wide` | — | Wide table stress test |

### 5.2 Evaluation Method

Each run produces a `run.json` with pipeline metrics (triplets, entities, tables processed, Cypher success rate). An **AI Judge** (GPT-5.4-mini) evaluates each run across five dimensions:

| Dimension | Weight | Description |
|---|---|---|
| **Builder** | 1.0 | Triplet quality, entity resolution accuracy, mapping correctness |
| **Retrieval** | 1.0 | Context relevancy, chunk quality, coverage |
| **Answer** | 1.0 | Faithfulness, completeness, grounding |
| **Pipeline** | 1.0 | Robustness, error handling, completeness |
| **Ablation** | 0.5 | Study-specific impact assessment (only for non-baseline) |

The **Overall Score** is the weighted mean (scale 1.0–5.0).

### 5.3 RAGAS Metrics

Studies marked `run_ragas=True` additionally collect automated RAGAS metrics:

- **Faithfulness** — fraction of answer claims supported by context
- **Context Precision** — signal-to-noise ratio of retrieved chunks
- **Context Recall** — coverage of gold-standard entities

---

## 6. Results Summary

Campaign results across 126 runs (21 studies x 6 datasets). All scores are AI Judge Overall (1.0–5.0 scale).

### 6.1 Score Summary Table

| Study | Description | Mean | Min | Max | Delta vs Baseline |
|---|---|---|---|---|---|
| **AB-00** | Baseline (hybrid, reranker ON, 256/32) | **4.15** | 3.95 | 4.25 | — |
| AB-01 | Vector-only retrieval | 2.49 | 2.05 | 3.10 | -1.66 |
| AB-02 | BM25-only retrieval | 3.33 | 2.80 | 3.90 | -0.82 |
| AB-03 | Reranker OFF | 3.65 | 2.95 | 4.00 | -0.50 |
| AB-04 | Reranker top_k=5 | 3.21 | 2.85 | 3.90 | -0.94 |
| AB-05 | Reranker top_k=20 | 3.68 | 3.20 | 4.40 | -0.47 |
| AB-06 | Chunking 128/16 | 4.27 | 3.95 | 4.60 | +0.12 |
| AB-07 | Chunking 384/48 | 4.17 | 3.95 | 4.35 | +0.02 |
| AB-08 | Chunking 512/64 | 4.37 | 3.95 | 4.70 | +0.22 |
| AB-09 | Extraction tokens=4096 | 4.20 | 3.95 | 4.50 | +0.05 |
| **AB-10** | **Extraction tokens=16384** | **4.46** | **4.25** | **4.75** | **+0.31** |
| AB-11 | ER threshold=0.65 | 4.08 | 3.95 | 4.20 | -0.07 |
| AB-12 | ER threshold=0.85 | 4.33 | 3.95 | 4.90 | +0.18 |
| AB-13 | ER blocking top_k=5 | 4.18 | 3.95 | 4.45 | +0.03 |
| AB-14 | ER blocking top_k=20 | 4.17 | 3.95 | 4.35 | +0.02 |
| AB-15 | Schema enrichment OFF | 4.11 | 3.95 | 4.25 | -0.04 |
| AB-16 | Actor-Critic OFF | 4.22 | 3.95 | 4.45 | +0.07 |
| AB-17 | Confidence threshold=0.70 | 4.16 | 3.70 | 4.65 | +0.01 |
| AB-18 | Confidence threshold=0.85 | 4.27 | 3.70 | 4.75 | +0.12 |
| AB-19 | Cypher healing OFF | 3.63 | 3.35 | 4.00 | -0.52 |
| AB-20 | Hallucination grader OFF | 3.35 | 2.95 | 4.50 | -0.80 |

### 6.2 Key Findings

1. **Best configuration:** AB-10 (extraction tokens=16384) achieved the highest mean score of 4.46, outperforming the baseline by +0.31. More extraction budget allows richer triplets.

2. **Most critical components (large degradation when OFF):**
   - **Hybrid retrieval** is essential: vector-only (AB-01, -1.66) and BM25-only (AB-02, -0.82) perform dramatically worse
   - **Hallucination grader** (AB-20, -0.80): removing grading significantly hurts answer quality
   - **Cypher healing** (AB-19, -0.52): direct fail on syntax errors causes measurable degradation
   - **Reranker** (AB-03, -0.50): raw hybrid pool without reranking is notably worse

3. **Chunking:** Larger chunks (AB-08, 512/64, +0.22) slightly outperform the baseline, suggesting the default 256/32 is somewhat conservative.

4. **Entity resolution:** Conservative merging (AB-12, threshold=0.85, +0.18) slightly improves over the default 0.75, suggesting fewer false merges help quality.

5. **Low-impact components:**
   - Schema enrichment (AB-15, -0.04): minimal impact, likely because LLMs can already interpret abbreviated names
   - Actor-Critic (AB-16, +0.07): disabling the critic did not hurt — possibly because current LLMs produce high-quality first-pass mappings
   - ER blocking top_k (AB-13/14): nearly identical to baseline regardless of candidate set size

---

## 7. Execution Protocol

### 7.1 Environment

- All ablation runs executed on the **same hardware** and **same LLM models** (gpt-5.4-nano extraction, gpt-5.4-mini midtier, gpt-5.4 reasoning)
- Same Neo4j 5.x instance, database cleared between runs
- Each study is a separate invocation of `src/evaluation/ablation_runner.py`

### 7.2 Run Procedure

The ablation runner (`scripts/run_ablation_full.py`) automates the full campaign:

1. For each study ID in `ABLATION_MATRIX`:
   a. Override environment variables per `env_overrides`
   b. Clear Neo4j database
   c. Run the full builder + query pipeline on each dataset
   d. Save `run.json` with metrics
2. AI Judge evaluates each run independently, producing `ai_judge.md`
3. Score extraction and aggregation via `scripts/generate_ablation_report.py`

### 7.3 Invocation

```bash
# Single study on one dataset
python -m scripts.run_ablation_full --study AB-10 --dataset DS01

# Full campaign (all studies, all datasets)
python -m scripts.run_ablation_full --all

# AI Judge evaluation
python -m scripts.run_ai_judge --study AB-10 --dataset DS01

# Generate aggregate report
python -m scripts.generate_ablation_report
```

---

## 8. Reporting Template

Each ablation result is documented in the following format:

### AB-XX — [Component Name]

**Date:** YYYY-MM-DD
**LLM Configuration:** gpt-5.4-nano / gpt-5.4-mini / gpt-5.4

#### Results

| Dataset | Overall | Builder | Retrieval | Answer | Pipeline |
|---|---|---|---|---|---|
| DS01 | | | | | |
| DS02 | | | | | |
| ... | | | | | |
| **Mean** | | | | | |

#### Observations
- [Key findings in 2-3 bullet points]

#### Conclusion
- [Is the component's contribution significant?]
- [Is the latency/cost trade-off justified?]

---

## Appendix: ABLATION_MATRIX Source

The canonical definition of all studies lives in `src/evaluation/ablation_runner.py`:

```python
ABLATION_MATRIX = {
    "AB-00": {
        "description": "Baseline — default settings",
        "env_overrides": {},
        "primary_metric": "faithfulness",
        "run_ragas": True,
    },
    "AB-01": {
        "description": "Vector-only retrieval",
        "env_overrides": {"RETRIEVAL_MODE": "vector"},
        "primary_metric": "context_precision",
        "run_ragas": True,
    },
    # ... (21 entries total — see source file for full definitions)
}
```
