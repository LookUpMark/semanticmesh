# AB-BEST — 03_advanced_healthcare — Run Analysis

**Timestamp:** 2026-05-04 19:46:10  
**Run tag:** `run-20260504_213821`

## Configuration

| Parameter | Value |
|-----------|-------|
| Extraction model | `LLM (openai/gpt-4.1-nano)` |
| Reasoning model | `openai/gpt-oss-120b` |
| Embedding model | `BAAI/bge-m3` |
| Retrieval mode | `hybrid` |
| Reranker | `True` |
| Reranker top_k | `20` |
| Chunk size / overlap | `128 / 16` |
| ER similarity threshold | `0.65` |

## Builder Results

| Metric | Value |
|--------|-------|
| Triplets extracted | 132 |
| Entities resolved | 157 |
| Tables parsed | 10 |
| Tables completed | 10 |

## Query Evaluation Summary

| Metric | Value |
|--------|-------|
| Questions | 1 |
| Grounded | **1/1 (100%)** |
| Avg GT Coverage | 100% |
| Avg Top Score | 0.8860 |
| Avg Chunk Count | 20.0 |
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

**Sources retrieved (11):** `parent_chunk_data_dictionary.md_10`, `parent_chunk_data_dictionary.md_11`, `parent_chunk_data_dictionary.md_3`, `Diagnosis`, `parent_chunk_data_dictionary.md_9`, `parent_chunk_data_dictionary.md_6`, `parent_chunk_data_dictionary.md_5`, `parent_chunk_data_dictionary.md_4`

---

## Anomalies & Observations

No anomalies detected. All questions grounded with acceptable RAGAS scores.
