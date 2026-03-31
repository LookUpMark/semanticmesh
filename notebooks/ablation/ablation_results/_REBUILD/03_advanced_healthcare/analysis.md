# _REBUILD — 03_advanced_healthcare — Run Analysis

**Timestamp:** 2026-03-30 23:02:40  
**Run tag:** `v5-rebuild`

## Configuration

| Parameter | Value |
|-----------|-------|
| Extraction model | `LLM (gpt-5.4-nano-2026-03-17)` |
| Reasoning model | `gpt-5.4-2026-03-05` |
| Embedding model | `BAAI/bge-m3` |
| Retrieval mode | `hybrid` |
| Reranker | `True` |
| Reranker top_k | `12` |
| Chunk size / overlap | `256 / 32` |
| ER similarity threshold | `0.75` |

## Builder Results

| Metric | Value |
|--------|-------|
| Triplets extracted | 429 |
| Entities resolved | 239 |
| Tables parsed | 10 |
| Tables completed | 10 |

## Query Evaluation Summary

| Metric | Value |
|--------|-------|
| Questions | 1 |
| Grounded | **1/1 (100%)** |
| Avg GT Coverage | 100% |
| Avg Top Score | 0.9577 |
| Avg Chunk Count | 12.0 |
| Abstained | 0 |

## RAGAS Metrics

RAGAS evaluation not enabled for this run.

## Per-Question Deep Dive

### ✅ Q001 — What tables store information about patients?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.9577 | **Gate:** `proceed`

**Expected answer:**
> The patients table stores demographic and administrative information including MRN, name, date of birth, gender, contact details, and emergency contacts. Additionally, patient-related data is stored in diagnoses, treatments, medications, lab_results, appointments, and claims tables through foreign k…

**System answer:**
> The primary table for patient information is PATIENTS, which implements the Patient Master Record concept and stores core identity, demographic, contact, emergency contact, and insurance linkage data. Its columns include patient_id, mrn, first_name, last_name, date_of_birth, gender, phone, email, emergency_contact_name, emergency_contact_phone, primary_insurance_id, is_deleted, valid_from, valid_t…

**Sources retrieved (12):** `Store patient diagnosis records with ICD-10 coding and temporal tracking→DIAGNOSES`, `Patient Master Record→PATIENTS`, `insurance claims and billing information for services rendered→CLAIMS`, `Laboratory Test Result→LAB_RESULTS`, `parent_chunk_data_dictionary.md_10`, `Patient Master Record`, `parent_chunk_data_dictionary.md_3`, `Laboratory Test Result`

**Context previews (first 3):**

1. _Business concept 'Store patient diagnosis records with ICD-10 coding and temporal tracking' is implemented by physical table DIAGNOSES (columns: diagnosis_id, patient_id, icd_10_code, diagnosis_name, …_

2. _Business concept 'Patient Master Record' — The table stores core patient identity, demographic, contact, emergency contact, and insurance linkage data with temporal historization, which is characteris…_

3. _Business concept 'insurance claims and billing information for services rendered' — Store insurance claims and billing information for services rendered. is implemented by physical table CLAIMS (colum…_

---

## Anomalies & Observations

No anomalies detected. All questions grounded with acceptable RAGAS scores.
