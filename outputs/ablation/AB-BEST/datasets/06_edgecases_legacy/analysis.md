# AB-BEST — 06_edgecases_legacy — Run Analysis

**Timestamp:** 2026-05-05 13:47:39  
**Run tag:** `run-20260505_150918`

## Configuration

| Parameter | Value |
|-----------|-------|
| Extraction model | `LLM (gpt-5-nano-2025-08-07)` |
| Reasoning model | `gpt-5.4-nano-2026-03-17` |
| Embedding model | `BAAI/bge-m3` |
| Retrieval mode | `hybrid` |
| Reranker | `True` |
| Reranker top_k | `20` |
| Chunk size / overlap | `128 / 16` |
| ER similarity threshold | `0.65` |

## Builder Results

| Metric | Value |
|--------|-------|
| Triplets extracted | 192 |
| Entities resolved | 149 |
| Tables parsed | 10 |
| Tables completed | 10 |

## Query Evaluation Summary

| Metric | Value |
|--------|-------|
| Questions | 1 |
| Grounded | **1/1 (100%)** |
| Avg GT Coverage | 100% |
| Avg Top Score | 0.9921 |
| Avg Chunk Count | 24.0 |
| Abstained | 0 |

## RAGAS Metrics

RAGAS evaluation not enabled for this run.

## Per-Question Deep Dive

### ✅ 1 — What is the purpose of the tblCustomer table?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0000 | **Gate:** `proceed`

**Expected answer:**
> The tblCustomer table stores customer master data including customer codes, names, email addresses, and region information. It uses Hungarian notation with the str prefix for string fields and contains both legacy fields (strCustID, strFullName) and new migration compatibility fields (cust_id, custo…

**System answer:**
> 

**Sources retrieved (12):** `parent_chunk_data_dictionary.txt_4`, `parent_chunk_business_glossary.md_0`, `parent_chunk_data_dictionary.txt_5`, `parent_chunk_business_glossary.md_3`, `parent_chunk_data_dictionary.txt_7`, `VW_SALESORDERHDR→TBLCUSTOMER`, `parent_chunk_business_glossary.md_2`, `parent_chunk_data_dictionary.txt_6`

---

## Anomalies & Observations

No anomalies detected. All questions grounded with acceptable RAGAS scores.
