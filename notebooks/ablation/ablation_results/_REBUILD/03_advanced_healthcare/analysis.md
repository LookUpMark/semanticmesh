# _REBUILD — 03_advanced_healthcare — Run Analysis

**Timestamp:** 2026-03-31 16:40:49  
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
| Triplets extracted | 464 |
| Entities resolved | 264 |
| Tables parsed | 10 |
| Tables completed | 10 |

## Query Evaluation Summary

| Metric | Value |
|--------|-------|
| Questions | 1 |
| Grounded | **1/1 (100%)** |
| Avg GT Coverage | 100% |
| Avg Top Score | 0.9546 |
| Avg Chunk Count | 12.0 |
| Abstained | 0 |

## RAGAS Metrics

RAGAS evaluation not enabled for this run.

## Per-Question Deep Dive

### ✅ Q001 — What tables store information about patients?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.9546 | **Gate:** `proceed`

**Expected answer:**
> The patients table stores demographic and administrative information including MRN, name, date of birth, gender, contact details, and emergency contacts. Additionally, patient-related data is stored in diagnoses, treatments, medications, lab_results, appointments, and claims tables through foreign k…

**System answer:**
> From the retrieved context, the main table that stores patient information is PATIENTS. It stores current and historical patient demographic and administrative information, including patient_id, mrn, first_name, last_name, date_of_birth, gender, phone, email, emergency contact fields, primary_insurance_id, and temporal/history fields such as is_deleted, valid_from, valid_to, created_at, and update…

**Sources retrieved (12):** `Store patient diagnosis records with ICD-10 coding and temporal tracking→DIAGNOSES`, `Patient Demographics→PATIENTS`, `Appointments→APPOINTMENTS`, `Diagnostic laboratory test results for patients→LAB_RESULTS`, `parent_chunk_data_dictionary.md_10`, `parent_chunk_data_dictionary.md_3`, `Appointments`, `parent_chunk_data_dictionary.md_9`

**Context previews (first 3):**

1. _Business concept 'Store patient diagnosis records with ICD-10 coding and temporal tracking' is implemented by physical table DIAGNOSES (columns: diagnosis_id, patient_id, icd_10_code, diagnosis_name, …_

2. _Business concept 'Patient Demographics' — The table is explicitly described as storing current and historical patient demographic and administrative information, with fields for identity, contact deta…_

3. _Business concept 'Appointments' — The table is explicitly titled APPOINTMENTS and stores appointment_id, patient_id, provider_id, appointment_date/time, status, and cancellation details, which directl…_

---

## Anomalies & Observations

No anomalies detected. All questions grounded with acceptable RAGAS scores.
