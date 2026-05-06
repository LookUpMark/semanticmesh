# Ablation Study — Results Report

**Generated:** 2026-05-06
**Evaluator:** AI Judge (`gpt-5.4-nano-2026-03-17`)
**Pipeline:** Multi-Agent GraphRAG for Data Governance

---

## 1. Best Configuration Results (AB-BEST)

Full pipeline with all features enabled, evaluated across 7 datasets:

| Dataset | Tables | Questions | Builder | Retrieval | Answer | Pipeline | Overall |
|---------|:------:|:---------:|:-------:|:---------:|:------:|:--------:|:-------:|
| 01_basics_ecommerce | 7 | 15 | 5 | 5 | 5 | 5 | **4.50** |
| 02_intermediate_finance | 9 | 20 | 5 | 5 | 5 | 5 | **4.50** |
| 03_advanced_healthcare | 10 | 30 | 5 | 5 | 5 | 5 | **4.50** |
| 04_complex_manufacturing | 13 | 40 | 5 | 5 | 5 | 5 | **4.50** |
| 05_edgecases_incomplete | 5 | 20 | 5 | 5 | 5 | 5 | **4.50** |
| 06_edgecases_legacy | 8 | 25 | 5 | 5 | 5 | 5 | **4.50** |
| 07_stress_large_scale | 58 | 55 | 5 | 5 | 5 | 5 | **4.50** |
| **Average** | **110** | **205** | **5.00** | **5.00** | **5.00** | **5.00** | **4.50** |

> 205/205 answers grounded (100%), zero hallucinations across all datasets.

## 2. Ablation Studies (ds01_basics_ecommerce)

Each study toggles one pipeline component to measure its contribution:

| Study | Description | Builder | Retrieval | Answer | Pipeline | Overall | Δ vs AB-00 |
|:-----:|-------------|:-------:|:---------:|:------:|:--------:|:-------:|:----------:|
| **AB-00** | Baseline — default settings | 5 | 4 | 5 | 5 | **4.25** | baseline |
| **AB-01** | Retrieval: Vector-only (no BM25, no | 5 | 3 | 3 | 5 | **3.80** | -0.45 |
| **AB-02** | Retrieval: BM25-only (no vector, no | 5 | 3 | 4 | 5 | **4.10** | -0.15 |
| **AB-03** | Retrieval: Reranker OFF (raw hybrid | 5 | 4 | 4 | 5 | **4.35** | +0.10 |
| **AB-04** | Reranker top_k=5 (smaller pool) | 5 | 4 | 4 | 5 | **3.95** | -0.30 |
| **AB-05** | Reranker top_k=20 (larger pool) | 5 | 4 | 5 | 5 | **4.65** | +0.40 |
| **AB-06** | Chunking 128/16 (smaller chunks) | 5 | 4 | 5 | 5 | **4.65** | +0.40 |
| **AB-07** | Chunking 384/48 (larger chunks) | 5 | 4 | 5 | 4 | **4.55** | +0.30 |
| **AB-08** | Chunking 512/64 (largest chunks) | 5 | 4 | 5 | 5 | **4.65** | +0.40 |
| **AB-09** | Extraction max tokens=4096 (conserv | 5 | 4 | 4 | 5 | **4.35** | +0.10 |
| **AB-10** | Extraction max tokens=16384 (genero | 5 | 4 | 5 | 5 | **4.25** | baseline |
| **AB-11** | ER similarity threshold=0.65 (aggre | 5 | 4 | 5 | 5 | **4.65** | +0.40 |
| **AB-12** | ER similarity threshold=0.85 (conse | 5 | 4 | 5 | 5 | **4.25** | baseline |
| **AB-13** | ER blocking top_k=5 (smaller candid | 5 | 4 | 5 | 4 | **4.55** | +0.30 |
| **AB-14** | ER blocking top_k=20 (larger candid | 5 | 4 | 5 | 5 | **4.25** | baseline |
| **AB-15** | Schema enrichment OFF | 5 | 4 | 5 | 5 | **4.25** | baseline |
| **AB-16** | Actor–Critic validation OFF | 5 | 3 | 5 | 4 | **3.90** | -0.35 |
| **AB-17** | HITL confidence threshold=0.70 | 5 | 4 | 5 | 5 | **4.25** | baseline |
| **AB-18** | HITL confidence threshold=0.85 | 5 | 4 | 5 | 5 | **4.75** | +0.50 |
| **AB-19** | Cypher healing OFF | 4 | 4 | 5 | 4 | **4.30** | +0.05 |
| **AB-20** | Hallucination grader OFF | 5 | 4 | 5 | 5 | **4.65** | +0.40 |

## 3. Key Findings

### Most Critical Components (removal hurts most)

| Rank | Study | Description | Score | Impact |
|:----:|:-----:|-------------|:-----:|:------:|
| 1 | AB-01 | Retrieval: Vector-only (no BM25, no grap | 3.80 | -0.45 |
| 2 | AB-16 | Actor–Critic validation OFF | 3.90 | -0.35 |
| 3 | AB-04 | Reranker top_k=5 (smaller pool) | 3.95 | -0.30 |
| 4 | AB-02 | Retrieval: BM25-only (no vector, no grap | 4.10 | -0.15 |
| 5 | AB-00 | Baseline — default settings | 4.25 | +0.00 |

### Best Configurations (above baseline)

- **AB-18** (HITL confidence threshold=0.85): 4.75 (+0.50)
- **AB-05** (Reranker top_k=20 (larger pool)): 4.65 (+0.40)
- **AB-06** (Chunking 128/16 (smaller chunks)): 4.65 (+0.40)
- **AB-08** (Chunking 512/64 (largest chunks)): 4.65 (+0.40)
- **AB-11** (ER similarity threshold=0.65 (aggressive merging)): 4.65 (+0.40)

## 4. Summary

- **AB-BEST average:** 4.50/5 across 7 datasets (110 tables, 205 questions)
- **All answers grounded:** 205/205 (100%) — zero hallucinations
- **Perfect dimension scores:** Builder 5/5, Retrieval 5/5, Answer 5/5, Pipeline 5/5 on all 7 datasets
- **Ablation baseline (AB-00 ds01):** 4.25
- **Worst ablation:** AB-01 (Retrieval: Vector-only (no BM25, no graph)) at 3.80
- **Best ablation:** AB-18 (HITL confidence threshold=0.85) at 4.75
