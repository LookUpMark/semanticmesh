# AB-BEST — 03_advanced_healthcare — Run Analysis

**Timestamp:** 2026-05-05 13:29:20  
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
| Triplets extracted | 252 |
| Entities resolved | 207 |
| Tables parsed | 10 |
| Tables completed | 10 |

## Query Evaluation Summary

| Metric | Value |
|--------|-------|
| Questions | 1 |
| Grounded | **1/1 (100%)** |
| Avg GT Coverage | 100% |
| Avg Top Score | 0.9946 |
| Avg Chunk Count | 23.0 |
| Abstained | 0 |

## RAGAS Metrics

RAGAS evaluation not enabled for this run.

## Per-Question Deep Dive

### ✅ Q001 — What tables store information about patients?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0000 | **Gate:** `proceed`

**Expected answer:**
> The patients table stores demographic and administrative information including MRN, name, date of birth, gender, contact details, and emergency contacts. Additionally, patient-related data is stored in diagnoses, treatments, medications, lab_results, appointments, and claims tables through foreign k…

**System answer:**
> 

**Sources retrieved (11):** `parent_chunk_data_dictionary.md_10`, `parent_chunk_data_dictionary.md_11`, `Patients Table`, `parent_chunk_data_dictionary.md_3`, `Patient Diagnoses`, `parent_chunk_data_dictionary.md_9`, `parent_chunk_data_dictionary.md_6`, `parent_chunk_data_dictionary.md_5`

---

## Anomalies & Observations

No anomalies detected. All questions grounded with acceptable RAGAS scores.
