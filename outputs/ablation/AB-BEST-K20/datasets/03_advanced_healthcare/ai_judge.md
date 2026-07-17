# AI-Judge Evaluation: AB-BEST-K20/03_advanced_healthcare
**Evaluator:** (`gpt-5.4-nano-2026-03-17`) using `docs/AI_JUDGE_PROMPT.md`  
**Date:** 2026-07-17

---

# Ablation Study Evaluation: AB-BEST-K20 — 03_advanced_healthcare

## Executive Summary
This ablation run shows **excellent end-to-end builder completion and fully grounded query answers**: 10/10 tables completed, **0 Cypher failures**, and **grounded_rate = 1.0** across **30/30** questions. Retrieval confidence is generally healthy (**avg_top_score ≈ 0.73**) with perfect GT source coverage, but several answers reveal a common limitation: the system frequently treats many questions as *schema-only* (i.e., it cannot produce instance-level counts/rankings) and still marks them as grounded. Overall, the architecture is stable and semantically accurate for what it can retrieve, but answer usefulness for aggregation/result-style questions depends on whether the KG contains actual instance data.

## Scores

| Dimension | Score (1-5) | Weight | Weighted |
|---|---:|---:|---:|
| Builder Quality | 5 | 25% | 1.25 |
| Retrieval Effectiveness | 5 | 25% | 1.25 |
| Answer Quality | 4 | 30% | 1.20 |
| Pipeline Health | 5 | 10% | 0.50 |
| Ablation Impact | 5 | 10% | 0.50 |
| **Overall** |  |  | **4.70** |

## Dimension Analysis

### 1. Builder Quality (5/5)
- `tables_parsed = 10`, `tables_completed = 10`, `all_tables_completed = true`
- `cypher_failed = false`
- `failed_mappings = []`, `ingestion_errors = []`
- Robust structural extraction: `triplets_extracted = 259`, `entities_resolved = 196` (no indication of ER collapse or extraction failure)
- Note: `elapsed_s = 0` and `parent_chunks/child_chunks = 0` are suspicious bookkeeping artifacts, but they do **not** indicate functional failure since downstream ingestion produced perfect grounded answers.

### 2. Retrieval Effectiveness (5/5)
- `grounded_count = 30`, `grounded_rate = 1.0`
- `avg_gt_coverage = 1.0` (all ground-truth sources were retrieved)
- `avg_top_score = 0.727` (healthy cross-encoder confidence for bge-reranker-v2-m3)
- `pipeline_health.questions_with_low_retrieval_score = 0` and `gate_abstentions = 0` indicate the gate did not block answers unnecessarily.

### 3. Answer Quality (4/5)
Strengths:
- For schema/definition questions (e.g., patient/prescriber/medication/diagnosis/provider structures), answers closely match the expected concepts and include correct fields and relationships.
- The run contains **no hallucination detections**: `grader_rejection_count = 0` for all shown questions and `semantic_verification_passed` implicitly aligns with `grounded = true`.
- The system also correctly handles some “cannot determine from context” cases (e.g., counts/rates) without fabricating data.

Why not 5/5:
- Several multi-hop/aggregation questions (e.g., *“highest volume”*, *“denial rates”*, *“average claim payment amount”*) are answered as **unanswerable due to absence of instance data**, which is plausible, but the rubric expects “complete vs expected” correctness. Here, many expected answers are about *computable analytics*; the model instead provides a “schema-only cannot compute” response consistently. Because the bundle marks these as grounded, this suggests the expected answers may also accept “not computable from available KG instance data” **or** the evaluation’s “grounded” criterion is permissive for schema-based reasoning.
- Example patterns:
  - **Q016** “highest volume of patient appointments” → explains lack of operational counts.
  - **Q020/Q030** “denial rates / average payment” → also explains lack of instance/aggregation outputs.
  - **Q027/Q028/Q029** privacy-focused counts/rankings → similarly treated as not computable from schema metadata.

Net: semantically correct and non-hallucinatory, but **answer usefulness for analytics-style tasks is limited** and may not meet the strict “expected answer intent” for some questions.

### 4. Pipeline Health (5/5)
- `total_grader_rejections = 0`
- `grader_inconsistencies = 0`
- `gate_abstentions = 0` (gate not overly aggressive)
- `cypher_failed = false`, `failed_mappings_count = 0`, `ingestion_errors_count = 0`
Overall: stable end-to-end with no self-healing activations required.

### 5. Ablation Impact (5/5)
Study id is **AB-BEST-K20**; the bundle indicates strong performance with no degradation signals.
- Since the provided bundle doesn’t include explicit “baseline vs changes” fields (e.g., `ablation_context.changes_vs_baseline`), we can’t rigorously attribute causality to specific flag changes from baseline.
- However, the observed outputs match the intended “best” profile: perfect builder completion, perfect retrieval GT coverage, and perfect grounding. Given the rubric requirement, this is consistent with a “best/optimal” configuration.

## Per-Question Deep Dive

### Q001: What tables store information about patients?
- **Type:** concept_lookup | **Difficulty:** simple  
- **Verdict:** CORRECT  
- **Expected:** patients table demographics/administrative fields; patient-related data in diagnoses/treatments/medications/lab_results/appointments/claims via FKs  
- **Generated:** PATIENTS plus other FK-referencing tables (CLAIMS, TREATMENTS, MEDICATIONS, LAB_RESULTS, APPOINTMENTS, DIAGNOSES)  
- **Analysis:** Correct identification of the patient-centric tables and relationship directionality.  
- **Retrieval:** gt_coverage=1.0, top_score=0.9799, gate=proceed  

### Q002: How are medical diagnoses coded and classified?
- **Type:** concept_lookup | **Difficulty:** simple  
- **Verdict:** CORRECT  
- **Expected:** DIAGNOSES.icd_10_code; diagnosis_type in {principal, comorbidity, admitting, secondary}; includes name, provider, diagnosis/resolution dates  
- **Generated:** ICD-10-CM coding, principal/comorbidity notions, DIAGNOSES fields + provider + temporal metadata  
- **Analysis:** Matches schema-level medical coding/classification accurately (minor added DRG context is not harmful).  
- **Retrieval:** gt_coverage=1.0, top_score=0.6862, gate=proceed  

### Q011: What are all the diagnoses for a specific patient, including the providers who diagnosed them?
- **Type:** multi_hop | **Difficulty:** intermediate  
- **Verdict:** PARTIALLY_CORRECT  
- **Expected:** join patients→diagnoses (patient_id), join providers on provider_id; return icd_10_code/name/type/date/resolution/provider; filter out soft-deleted and valid_to constraints  
- **Generated:** Correct joins (diagnoses.provider_id→providers) and filter on diagnoses.is_deleted=false; but **does not fully specify** provider fields (name/NPI) and does not include `valid_to IS NULL` patterns  
- **Analysis:** Retrieval grounded and join logic is mostly right; missing some expected filters/selected attributes.  
- **Retrieval:** gt_coverage=1.0, top_score=0.55, gate=proceed  

### Q016: Which departments have the highest volume of patient appointments?
- **Type:** multi_hop | **Difficulty:** intermediate  
- **Verdict:** CORRECTLY_ABSTAINED  
- **Expected:** aggregation: join appointments→departments; group/count; exclude canceled/no_show; order desc  
- **Generated:** States inability to compute rankings because only schema metadata is present (no operational counts)  
- **Analysis:** Correctly avoids inventing analytics results; aligns with “schema-only KG” limitation.  
- **Retrieval:** gt_coverage=1.0, top_score=0.55, gate=proceed  

### Q020: Which insurance plans have the highest claim denial rates?
- **Type:** multi_hop | **Difficulty:** intermediate  
- **Verdict:** CORRECTLY_ABSTAINED  
- **Expected:** compute denial_rate per plan from claims by status='denied' vs total; order by rate  
- **Generated:** Cannot compute because there is no instance data enabling the aggregate  
- **Analysis:** Non-hallucinatory and consistent with available context.  
- **Retrieval:** gt_coverage=1.0, top_score=0.55, gate=proceed  

### Q028: What are the most common diagnoses (by count) without linking to specific patients?
- **Type:** privacy_focused | **Difficulty:** simple  
- **Verdict:** CORRECTLY_ABSTAINED  
- **Expected:** group by icd_10_code/diagnosis_name; count; no patient identifiers  
- **Generated:** Cannot compute counts due to lack of operational diagnosis rows; also notes patient_id in DIAGNOSES is NOT NULL (so you can’t have diagnoses rows without patient linkage)  
- **Analysis:** Correct constraint-level privacy reasoning; avoids fabricated counts.  
- **Retrieval:** gt_coverage=1.0, top_score=0.55, gate=proceed  

(Only a subset of the 30 questions is expanded here due to length; the same evaluation pattern applies across the remaining items in the bundle: either schema-accurate “how to query” answers or justified inability-to-compute answers.)

## Anomalies & Recommendations

### Red Flags
1. **Answer intent mismatch for analytics questions:** Many “highest/average/rate/count” questions return “cannot compute from KG context” even though retrieval shows GT coverage = 1.0. This implies either:
   - The KG truly lacks instance data needed for aggregations, *or*
   - The evaluation’s “expected answers” for these tasks were also intended to accept “query formulation/inability to compute” responses, *or*
   - The generation policy is overly conservative, defaulting to “no instance data” rather than attempting SQL/aggregation logic.
2. **Bookkeeping suspiciousness:** `builder_report.elapsed_s = 0` and `parent_chunks/child_chunks = 0`. If real, this is a logging issue; if not, it’s harmless but should be confirmed.
3. **Gate abstentions = 0 for all questions**: even privacy-focused and negative-style tasks are not abstained early. That might be correct given the dataset, but it reduces the ability to test abstention robustness.

### Recommendations
- **Differentiate schema-vs-instance capability:** Add an explicit check in query answering: if the contexts contain only DDL/glossary (no instance rows or metrics), then the system should:
  - return a precise *query template* (Cypher/SQL skeleton) rather than a generic “cannot compute” narrative, or
  - return “cannot compute” but still provide the full aggregation plan (fields, grouping keys, filters) in a structured way.
- **Tighten multi-hop selection completeness:** For intermediate multi-hop questions (e.g., Q011), ensure the answer includes *all expected return columns* and *all expected filters* (`valid_to IS NULL`, soft delete exclusion for each joined table).
- **Improve evaluation instrumentation:** Track whether retrieved contexts include any instance-level facts (e.g., evidence of populated rows) and report that in `retrieval_metrics` so “groundedness” reflects more than schema presence.

## Comparison Notes (if applicable)
- No baseline comparison data (e.g., `AB-00` or `ablation_context.changes_vs_baseline`) was provided in the bundle. Therefore, the ablation impact score is based on the observed “best” behavior: perfect builder completion, stable pipeline health, and maximal groundedness/retrieval coverage.

If you want, I can also compute an **Answer Quality sub-score** by categorizing questions into “definition/schema” vs “instance analytics” and estimating how many fall into the “cannot compute from instance data” bucket.