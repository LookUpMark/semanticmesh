# AI-Judge Evaluation: AB-BEST-K20/03_advanced_healthcare
**Evaluator:** (`gpt-5.4-nano-2026-03-17`) using `docs/AI_JUDGE_PROMPT.md`  
**Date:** 2026-07-17

---

# Ablation Study Evaluation: AB-BEST-K20 — 03_advanced_healthcare

## Executive Summary
This ablation (AB-BEST-K20) shows **strong end-to-end architectural performance**: all 10 builder tables are completed with no Cypher failures, and the query graph reports **100% grounded answers** with **avg_gt_coverage=1.0** and healthy **avg_top_score=0.727**. However, several per-question responses indicate the system often answered at the **schema/query-instruction level** rather than producing data-driven outputs (counts/rates/rankings), which is not penalized by the provided “grounded/coverage” signals but is a potential **evaluation mismatch** versus what “answer” is expected to contain in this dataset.

## Scores

| Dimension | Score (1-5) | Weight | Weighted |
|---|---:|---:|---:|
| Builder Quality | 5 | 25% | 1.25 |
| Retrieval Effectiveness | 5 | 25% | 1.25 |
| Answer Quality | 4 | 30% | 1.20 |
| Pipeline Health | 5 | 10% | 0.50 |
| Ablation Impact | N/A | 10% | 0.00 |
| **Overall** |  |  | **4.20** |

## Dimension Analysis

### 1. Builder Quality (5/5)
- `tables_completed`: **10/10**, `all_tables_completed=true`
- `cypher_failed=false`, `failed_mappings=[]`, `ingestion_errors=[]`
- Triplet extraction: **259 triplets**, with **196 entities resolved** → triplet density is healthy (no sign of extraction/ER collapse).
- Overall: builder pipeline is stable and complete.

### 2. Retrieval Effectiveness (5/5)
- `query_report.grounded_rate=1.0`
- `avg_gt_coverage=1.0` and `avg_top_score=0.727` (consistent with a strong reranker signal)
- `abstained_count=0` and `gate_abstentions=0`: the retrieval/gating system did not incorrectly abstain.
- Per-question: all shown questions have high stated retrieval quality; importantly, even multi-hop/temporal ones show `gt_coverage=1.0`.

### 3. Answer Quality (4/5)
Most answers are **semantically correct** and strongly aligned with the expected schema-level facts (tables/columns/constraints, join paths, historization rules).
- Strong examples:
  - **Q001** accurately lists patient-related tables and FK relationships.
  - **Q002/Q003/Q004** correctly describe coding/classification, medication structure, and provider/department organization.
- Minor concern (why not 5):
  - For “analytics” questions (privacy/aggregation and rates/rankings), several answers explicitly claim they *cannot compute* operational results because only schema metadata is available (e.g., **Q016**, **Q020**, **Q028**, **Q030**). These are plausible if the KG truly contains no instance data, but the rubric here is about correctness vs expected answers. The bundle’s metrics still mark them grounded with `gt_coverage=1.0`, suggesting the expected answers in this study likely also accept “how to query / what would be computed” rather than actual computed values.
  - Some “as-of” and “active as of date” questions similarly provide query logic more than an example result—again consistent with schema-centric expected answers.

### 4. Pipeline Health (5/5)
- `pipeline_health.total_grader_rejections=0`
- `grader_inconsistencies=0`, `gate_abstentions=0`
- `cypher_failed=false`, `failed_mappings_count=0`, `ingestion_errors_count=0`
- Builder and query elapsed times are reported as **0** (likely missing/rounded in the bundle), but no instability signals appear.

### 5. Ablation Impact (N/A)
- The rubric requests comparing against baseline (AB-00) using `ablation_context`, but the provided bundle contains no `ablation_context` and we cannot verify what changed vs baseline.
- Therefore, ablation impact cannot be scored reliably.

## Per-Question Deep Dive

### Q001: What tables store information about patients?
- **Type:** concept_lookup | **Difficulty:** simple
- **Verdict:** CORRECT
- **Expected:** patients table demographics/admin (MRN, name, DOB, gender, contact, emergency contacts); related tables via FKs (diagnoses, treatments, medications, lab_results, appointments, claims)
- **Generated:** PATIENTS plus related tables via FK relationships to `patients.patient_id`
- **Analysis:** Matches expected table coverage and FK linkage intent.
- **Retrieval:** gt_coverage=1.0, top_score=0.979861259172271, gate=proceed

### Q002: How are medical diagnoses coded and classified?
- **Type:** concept_lookup | **Difficulty:** simple
- **Verdict:** CORRECT
- **Expected:** DIAGNOSES.icd_10_code + diagnosis_type in {principal, comorbidity, admitting, secondary}; include name/provider/date/resolution
- **Generated:** ICD-10-CM + principal/comorbidity definitions; mentions diagnosis name/provider/date/resolution and DRG context
- **Analysis:** Semantically aligned; slight extra claims about DRG/billing context are consistent.
- **Retrieval:** gt_coverage=1.0, top_score=0.7 (raw 0.686), gate=proceed

### Q003: What information is tracked for medications prescribed to patients?
- **Type:** concept_lookup | **Difficulty:** simple
- **Verdict:** CORRECT
- **Expected:** medication_name, NDC, dosage, route, frequency, prescribing provider, start/end; active has NULL end_date; valid_from/valid_to historization
- **Generated:** Covers all fields and lifecycle/audit/soft-delete; active uses NULL end_date
- **Analysis:** Correct and complete at schema level.
- **Retrieval:** gt_coverage=1.0, top_score=0.8410438772856567, gate=proceed

### Q004: How are healthcare providers organized and tracked?
- **Type:** concept_lookup | **Difficulty:** simple
- **Verdict:** CORRECT
- **Expected:** PROVIDERS: NPI unique, name, provider_type, specialty, department_id; is_active/is_deleted; historization
- **Generated:** Full PROVIDERS + DEPARTMENTS join and lifecycle fields; includes indexes/business rules
- **Analysis:** Matches expected.
- **Retrieval:** gt_coverage=1.0, top_score=0.7 (raw 0.55), gate=proceed

### Q005: What is the structure of departments and how do they relate to each other?
- **Type:** concept_lookup | **Difficulty:** simple
- **Verdict:** CORRECT
- **Expected:** DEPARTMENTS fields + self-referential parent_department_id + service_line/location + is_active/is_deleted
- **Generated:** Correct description of hierarchy and validity/audit fields
- **Analysis:** Matches expected.
- **Retrieval:** gt_coverage=1.0, top_score=0.7 (raw 0.55), gate=proceed

### Q006: How are insurance plans and payers represented in the system?
- **Type:** concept_lookup | **Difficulty:** simple
- **Verdict:** CORRECT
- **Expected:** insurance_plans fields + plan_type; prior_auth_required; is_active; historization; patients.primary_insurance_id FK
- **Generated:** Correctly uses insurance_plans schema + indirect payer via plan records + FK links from patients/claims
- **Analysis:** Matches expected.
- **Retrieval:** gt_coverage=1.0, top_score=0.7 (raw 0.55), gate=proceed

### Q007: What constitutes an insurance claim and what is its lifecycle?
- **Type:** concept_lookup | **Difficulty:** simple
- **Verdict:** CORRECT
- **Expected:** claims table fields + status workflow; denial_reason for denied claims
- **Generated:** Correct claim definition + claim_status states + denial_reason + soft-delete/historization
- **Analysis:** Matches expected.
- **Retrieval:** gt_coverage=1.0, top_score=0.7 (raw 0.55), gate=proceed

### Q008: How are patient appointments scheduled and tracked?
- **Type:** concept_lookup | **Difficulty:** simple
- **Verdict:** CORRECT
- **Expected:** appointments fields + appointment_type/status workflow + cancellation_reason requirements
- **Generated:** Matches appointment schema, allowed types/statuses, and cancellation/no-show rules
- **Analysis:** Matches expected.
- **Retrieval:** gt_coverage=1.0, top_score=0.7 (raw 0.55), gate=proceed

### Q009: What information is captured in laboratory test results?
- **Type:** concept_lookup | **Difficulty:** simple
- **Verdict:** CORRECT
- **Expected:** lab_results fields including test_name/LOINC, value/unit, reference_range, is_abnormal, ordering_provider_id, result_date, notes
- **Generated:** Matches fields and abnormal-rule description; includes historization/audit
- **Analysis:** Matches expected.
- **Retrieval:** gt_coverage=1.0, top_score=0.8185918194864789, gate=proceed

### Q010: How are medical treatments and procedures documented?
- **Type:** concept_lookup | **Difficulty:** simple
- **Verdict:** CORRECT
- **Expected:** treatments fields + diagnosis justification + provider/department linkage
- **Generated:** Correct mapping of required fields, diagnosis justification, status/stamps
- **Analysis:** Matches expected.
- **Retrieval:** gt_coverage=1.0, top_score=0.7 (raw 0.55), gate=proceed

### Q011: What are all the diagnoses for a specific patient, including the providers who diagnosed them?
- **Type:** multi_hop | **Difficulty:** intermediate
- **Verdict:** CORRECT
- **Expected:** diagnoses join to providers via provider_id; return code/name/type/date/resolution + provider name/NPI; filter by MRN/patient_id; exclude soft-deleted
- **Generated:** Correct join path and soft-delete filtering; discusses excluding deleted diagnoses
- **Analysis:** Correct schema join logic (even if it doesn’t list every expected output column explicitly).
- **Retrieval:** gt_coverage=1.0, top_score=0.7 (raw 0.55), gate=proceed

### Q012: Which patients have received treatments from cardiology department providers?
- **Type:** multi_hop | **Difficulty:** intermediate
- **Verdict:** PARTIALLY_CORRECT
- **Expected:** join patients→treatments→providers→departments; filter Cardiology; return patient MRN/name + treatment info + provider name
- **Generated:** Correct join/filter logic but explicitly states it can’t list actual patient records (instance data)
- **Analysis:** Logic is correct; answer may be incomplete depending on whether expected includes actual rows vs query pattern.
- **Retrieval:** gt_coverage=1.0, top_score=0.7 (raw 0.55), gate=proceed

### Q013: What treatments have been performed for a patient's specific diagnosis?
- **Type:** multi_hop | **Difficulty:** intermediate
- **Verdict:** CORRECT
- **Expected:** join diagnoses→treatments; filter by patient_id and icd_10_code; return treatment/provider/department/billing/timing/status
- **Generated:** Correct join logic and filtering conventions (soft-delete/current record)
- **Analysis:** Semantically aligned.
- **Retrieval:** gt_coverage=1.0, top_score=0.9690324847372525, gate=proceed

### Q014: Which providers have prescribed medications to patients with a specific diagnosis?
- **Type:** multi_hop | **Difficulty:** intermediate
- **Verdict:** CORRECT
- **Expected:** diagnoses→patients→medications→providers; filter by icd_10_code; return provider + patient + medication fields incl prescription dates
- **Generated:** Correct join path diagnoses(patient_id) → medications(patient_id) → prescribing_provider_id → providers
- **Analysis:** Correctly identifies the relationship chain; does not fully expand every requested return attribute.
- **Retrieval:** gt_coverage=1.0, top_score=0.7 (raw 0.55), gate=proceed

### Q015: What is the complete medication history for a patient including prescribing providers?
- **Type:** multi_hop | **Difficulty:** intermediate
- **Verdict:** PARTIALLY_CORRECT
- **Expected:** actual medication history fields + include historical records (valid_to not null for changes)
- **Generated:** Explains how to query history but repeatedly claims it can’t produce actual records from schema-only context
- **Analysis:** Query-plan is good; “complete medication history” outputs likely missing if instance data expected.
- **Retrieval:** gt_coverage=1.0, top_score=0.7025300573952054, gate=proceed

### Q016: Which departments have the highest volume of patient appointments?
- **Type:** multi_hop | **Difficulty:** intermediate
- **Verdict:** CORRECTLY_ABSTAINED (by “can’t compute”)
- **Expected:** aggregate counts by department (exclude canceled/no_show), order DESC
- **Generated:** Explicitly states inability to compute counts due to metadata-only context
- **Analysis:** Correctly avoids fabricating rankings; however, the bundle still marks grounded/gt_coverage=1.0.
- **Retrieval:** gt_coverage=1.0, top_score=0.7 (raw 0.55), gate=proceed

### Q017: What claims have been submitted for a specific patient's treatments?
- **Type:** multi_hop | **Difficulty:** intermediate
- **Verdict:** CORRECT
- **Expected:** treatments→claims by patient_id and service_date ~ treatment_date; return claim number/codes/amounts/status/payer info
- **Generated:** Correctly identifies relationship via shared patient_id and uses claim_status/submission_date
- **Analysis:** Correct relationship logic; doesn’t fully nail the “service_date ≈ treatment_date” approximation.
- **Retrieval:** gt_coverage=1.0, top_score=0.7 (raw 0.5818), gate=proceed

### Q018: Which providers in a specific department have ordered abnormal lab results?
- **Type:** multi_hop | **Difficulty:** intermediate
- **Verdict:** CORRECT
- **Expected:** lab_results→providers→departments; filter department; is_abnormal=TRUE; return provider/patient/test/timing fields
- **Generated:** Correct join and filter logic; mentions soft-delete/index conditioning
- **Analysis:** Correct at schema/query level.
- **Retrieval:** gt_coverage=1.0, top_score=0.7 (raw 0.55), gate=proceed

### Q019: What is a patient's complete care journey including diagnoses, treatments, and medications?
- **Type:** multi_hop | **Difficulty:** advanced
- **Verdict:** PARTIALLY_CORRECT
- **Expected:** multi-joins across diagnoses/treatments/medications/lab_results/appointments; group/order chronologically
- **Generated:** Correctly outlines diagnoses↔treatments relationships and includes medications at a high level, but notes missing exact medication column details; doesn’t fully implement the full join/grouping spec
- **Analysis:** Likely incomplete relative to expected longitudinal timeline requirements.
- **Retrieval:** gt_coverage=1.0, top_score=0.7 (raw 0.55), gate=proceed

### Q020: Which insurance plans have the highest claim denial rates?
- **Type:** multi_hop | **Difficulty:** intermediate
- **Verdict:** CORRECTLY_ABSTAINED (by “cannot compute denial rates”)
- **Expected:** compute denial rate = denied/total for each plan_type; order DESC; filter by service_date range/current period
- **Generated:** States aggregation cannot be computed from schema-only context
- **Analysis:** Avoids hallucinating computed denial rates.
- **Retrieval:** gt_coverage=1.0, top_score=0.7 (raw 0.55), gate=proceed

### Q021: What were a patient's diagnoses in a specific past time period?
- **Type:** temporal | **Difficulty:** intermediate
- **Verdict:** CORRECT
- **Expected:** filter by patient_id and diagnosis_date range + historization validity windows
- **Generated:** Describes diagnosis_date and valid_from/valid_to concepts; indicates filtering by patient_id and is_deleted
- **Analysis:** Correct directionally; may not fully match expected predicate structure, but aligned.
- **Retrieval:** gt_coverage=1.0, top_score=0.7 (raw 0.55), gate=proceed

### Q022: How have a patient's medications changed over time?
- **Type:** temporal | **Difficulty:** intermediate
- **Verdict:** CORRECT
- **Expected:** query all medications without filtering out historical records; show new records per change; order by start_date DESC
- **Generated:** Correctly explains historization (valid_to, valid_from) and historized changes-as-new-records concept
- **Analysis:** Matches expected intent.
- **Retrieval:** gt_coverage=1.0, top_score=0.7 (raw 0.55), gate=proceed

### Q023: What was a provider's department affiliation at a specific past date?
- **Type:** temporal | **Difficulty:** intermediate
- **Verdict:** CORRECTLY_ABSTAINED (schema-only limitation)
- **Expected:** providers valid_from/valid_to containment with department join
- **Generated:** Explains how to query but says it can’t determine actual affiliation without operational records
- **Analysis:** Doesn’t fabricate; acceptable given metadata-only.
- **Retrieval:** gt_coverage=1.0, top_score=0.7 (raw 0.55), gate=proceed

### Q024: Show all changes to a patient's primary insurance coverage over time.
- **Type:** temporal | **Difficulty:** intermediate
- **Verdict:** CORRECT
- **Expected:** patients joined to insurance_plans via primary_insurance_id; include historized valid_to (don’t filter it out); order valid_from DESC
- **Generated:** Correctly uses historized patients.valid_from/valid_to + join for plan attributes
- **Analysis:** Matches expected.
- **Retrieval:** gt_coverage=1.0, top_score=0.7 (raw 0.55), gate=proceed

### Q025: What diagnoses were resolved within a specific time period?
- **Type:** temporal | **Difficulty:** intermediate
- **Verdict:** CORRECT
- **Expected:** resolution_date within range; resolution_date non-null; exclude ongoing; filter current records; include patient/icd/name/provider
- **Generated:** Correctly identifies resolution_date usage and non-null constraint.
- **Analysis:** Aligned with expected logic.
- **Retrieval:** gt_coverage=1.0, top_score=0.7 (raw 0.55), gate=proceed

### Q026: Reconstruct a patient's active medications as of a specific historical date.
- **Type:** temporal | **Difficulty:** advanced
- **Verdict:** PARTIALLY_CORRECT
- **Expected:** active period by start_date/end_date AND record validity by valid_from/valid_to
- **Generated:** Uses historization valid_from/valid_to and soft-delete exclusion; mentions end_date NULL for active, but doesn’t fully express the combined predicate structure (both as-of comparisons).
- **Analysis:** Mostly correct but likely missing one key “active period” condition framing.
- **Retrieval:** gt_coverage=1.0, top_score=0.7 (raw 0.55), gate=proceed

### Q027: Count the number of patients per department without exposing individual patient identities.
- **Type:** privacy_focused | **Difficulty:** intermediate
- **Verdict:** PARTIALLY_CORRECT
- **Expected:** aggregate counts (COUNT DISTINCT patient_id), exclude canceled/no-show, return aggregated counts only
- **Generated:** Correct privacy approach conceptually, but notes missing operational context for exact counts and doesn’t fully specify cancellation/no-show filtering in the final method.
- **Analysis:** Query logic is plausible but not fully operationalized.
- **Retrieval:** gt_coverage=1.0, top_score=0.7 (raw 0.55), gate=proceed

### Q028: What was a provider’s most common diagnoses? (privacy-focused count)
- **Type:** privacy_focused | **Difficulty:** simple
- **Verdict:** CORRECTLY_ABSTAINED (schema-only)
- **Expected:** diagnosis counts by icd_10_code/diagnosis_name without patient identifiers
- **Generated:** Claims instance data not present; concludes cannot compute counts
- **Analysis:** Avoids hallucination; but depends on whether KG includes instance rows.
- **Retrieval:** gt_coverage=1.0, top_score=0.7 (raw 0.55), gate=proceed

### Q029: Which providers have the highest patient volume without exposing patient information?
- **Type:** privacy_focused | **Difficulty:** intermediate
- **Verdict:** PARTIALLY_CORRECT
- **Expected:** aggregate provider volume (COUNT DISTINCT patient_id), filter by completed status, order DESC
- **Generated:** Correctly explains how volume could be computed, but cannot rank due to lack of operational instance data
- **Analysis:** Method is correct; output (ranking) may be missing.
- **Retrieval:** gt_coverage=1.0, top_score=0.7 (raw 0.55), gate=proceed

### Q030: What is the average claim payment amount by insurance plan type?
- **Type:** privacy_focused | **Difficulty:** intermediate
- **Verdict:** CORRECTLY_ABSTAINED (schema-only limitation)
- **Expected:** AVG(amount_paid) and AVG(amount_charged) grouped by plan_type; filter approved/partially_paid
- **Generated:** States aggregation cannot be computed from schema-only context
- **Analysis:** Avoids fabricating computed averages.
- **Retrieval:** gt_coverage=1.0, top_score=0.7 (raw 0.55), gate=proceed

## Anomalies & Recommendations

### Red Flags
- **Schema-first answers for analytics queries:** Multiple “highest/average/count/rates” questions result in “cannot compute” responses. This is only acceptable if the KG truly lacks instance data; otherwise it indicates the query engine/generation is not executing the required Cypher or the evaluation dataset expects literal computed outputs.
- **Evaluation signal inconsistency:** Despite these “cannot compute” statements, `gt_coverage=1.0` and `grounded=true` across all questions. That suggests the dataset’s “expected answers” likely focus on **query logic**, not actual computed results—or the grading proxy is aligned to retrieval/grounding rather than numeric correctness.

### Recommendations
1. **Clarify expected answer contract** for privacy/aggregation/“highest/average/rate” queries:
   - If instance data exists, add verification that the generated answer includes computed values.
   - If instance data does not exist, update rubric/benchmarks to judge “query blueprint correctness” explicitly.
2. Add a **“requires aggregation execution” check** in the query graph:
   - If question asks for counts/rates/averages/rankings, ensure the pipeline actually produces results (or abstains with a standardized “no instance data” message).
3. Introduce a **grader dimension for operationality**:
   - Distinguish “schema/query instruction is correct” from “query execution result is missing.”

## Comparison Notes (if applicable)
- No baseline (AB-00) bundle or `ablation_context.changes_vs_baseline` was provided, so a strict comparison cannot be performed.