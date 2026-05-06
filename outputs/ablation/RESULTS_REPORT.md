# Ablation Study — Results Report

**Generated:** 2026-05-06
**Evaluator:** AI Judge (`gpt-5.4-nano-2026-03-17`)
**Pipeline:** Multi-Agent GraphRAG for Data Governance

---

## 1. Best Configuration Results (AB-BEST)

Full pipeline with all features enabled, evaluated across 6 datasets:

| Dataset | Builder | Retrieval | Answer | Pipeline | Overall |
|---------|:-------:|:---------:|:------:|:--------:|:-------:|
| 01_basics_ecommerce | 5 | 5 | 5 | 5 | **4.50** |
| 02_intermediate_finance | 5 | 5 | 5 | 5 | **4.50** |
| 03_advanced_healthcare | 5 | 5 | 5 | 5 | **4.50** |
| 04_complex_manufacturing | 5 | 5 | 5 | 5 | **4.50** |
| 05_edgecases_incomplete | 5 | 5 | 5 | 5 | **4.50** |
| 06_edgecases_legacy | 5 | 5 | 5 | 5 | **4.50** |
| **Average** | **5.00** | **5.00** | **5.00** | **5.00** | **4.50** |

## 2. Ablation Studies (ds01_basics_ecommerce)

Each study disables one pipeline component to measure its contribution:

| Study | Builder | Retrieval | Answer | Pipeline | Ablation | Overall |
|:-----:|:-------:|:---------:|:------:|:--------:|:--------:|:-------:|
| **AB-00** (Baseline — default settin) | 5 | 4 | 5 | 5 | N/A | **4.25** |
| **AB-01** (Retrieval: Vector-only (n) | 5 | 3 | 3 | 5 | 4 | **3.80** |
| **AB-02** (Retrieval: BM25-only (no ) | 5 | 3 | 4 | 5 | 4 | **4.10** |
| **AB-03** (Retrieval: Reranker OFF () | 5 | 4 | 4 | 5 | 4 | **4.35** |
| **AB-04** (Reranker top_k=5 (smaller) | 5 | 4 | 4 | 5 | N/A | **3.95** |
| **AB-05** (Reranker top_k=20 (larger) | 5 | 4 | 5 | 5 | 4 | **4.65** |
| **AB-06** (Chunking 128/16 (smaller ) | 5 | 4 | 5 | 5 | 4 | **4.65** |
| **AB-07** (Chunking 384/48 (larger c) | 5 | 4 | 5 | 4 | 4 | **4.55** |
| **AB-08** (Chunking 512/64 (largest ) | 5 | 4 | 5 | 5 | 4 | **4.65** |
| **AB-09** (Extraction max tokens=409) | 5 | 4 | 4 | 5 | 4 | **4.35** |
| **AB-10** (Extraction max tokens=163) | 5 | 4 | 5 | 5 | N/A | **4.25** |
| **AB-11** (ER similarity threshold=0) | 5 | 4 | 5 | 5 | 4 | **4.65** |
| **AB-12** (ER similarity threshold=0) | 5 | 4 | 5 | 5 | N/A | **4.25** |
| **AB-13** (ER blocking top_k=5 (smal) | 5 | 4 | 5 | 4 | 4 | **4.55** |
| **AB-14** (ER blocking top_k=20 (lar) | 5 | 4 | 5 | 5 | N/A | **4.25** |
| **AB-15** (Schema enrichment OFF) | 5 | 4 | 5 | 5 | N/A | **4.25** |
| **AB-16** (Actor–Critic validation O) | 5 | 3 | 5 | 4 | N/A | **3.90** |
| **AB-17** (HITL confidence threshold) | 5 | 4 | 5 | 5 | N/A | **4.25** |
| **AB-18** (HITL confidence threshold) | 5 | 4 | 5 | 5 | 5 | **4.75** |
| **AB-19** (Cypher healing OFF) | 4 | 4 | 5 | 4 | 4 | **4.30** |
| **AB-20** (Hallucination grader OFF) | 5 | 4 | 5 | 5 | 4 | **4.65** |

## 3. Key Findings

### Components with Highest Impact (removal hurts most)

| Rank | Study | Overall | Delta vs Baseline |
|:----:|:-----:|:-------:|:-----------------:|
| 1 | AB-01 (Retrieval: Vector-only (no BM2) | 3.80 | -0.45 |
| 2 | AB-16 (Actor–Critic validation OFF) | 3.90 | -0.35 |
| 3 | AB-04 (Reranker top_k=5 (smaller pool) | 3.95 | -0.30 |
| 4 | AB-02 (Retrieval: BM25-only (no vecto) | 4.10 | -0.15 |
| 5 | AB-00 (Baseline — default settings) | 4.25 | +0.00 |

### Top Performers (above baseline)

- **AB-18** (HITL confidence threshold=0.85): 4.75 (+0.50)
- **AB-05** (Reranker top_k=20 (larger pool)): 4.65 (+0.40)
- **AB-06** (Chunking 128/16 (smaller chunks)): 4.65 (+0.40)
- **AB-08** (Chunking 512/64 (largest chunks)): 4.65 (+0.40)
- **AB-11** (ER similarity threshold=0.65 (aggressive merging)): 4.65 (+0.40)

## 4. Summary

- **AB-BEST average:** 4.50/5 across 6 datasets
- **All datasets grounded:** 100% (zero hallucinations)
- **Baseline (AB-00 ds01):** 4.25
- **Best ablation (ds01):** AB-18 at 4.75
- **Worst ablation (ds01):** AB-01 at 3.80
