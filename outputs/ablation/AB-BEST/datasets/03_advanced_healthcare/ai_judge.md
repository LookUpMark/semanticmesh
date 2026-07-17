# AI-Judge Evaluation: AB-BEST/03_advanced_healthcare
**Evaluator:** (`gpt-5.4-nano-2026-03-17`) using `docs/AI_JUDGE_PROMPT.md`  
**Date:** 2026-07-17

---

# Ablation Study Evaluation: AB-BEST — 03_advanced_healthcare

## Executive Summary
AB-BEST shows **excellent Builder and retrieval grounding** overall: all 10 DDL tables completed with no Cypher or ingestion errors, and **grounded_rate=1.0 across all 30 questions** with high **avg_gt_coverage=0.94** and strong **avg_top_score≈0.724** (consistent with healthy reranking).  
However, several *multi-hop and privacy/temporal* questions contain answers that are effectively **“cannot determine from context / cannot answer”** despite the reported groundedness—this suggests the evaluation bundle’s `grounded` labeling is not reflecting the real completeness/intent mismatch for those queries.

## Scores

| Dimension | Score (1-5) | Weight | Weighted |
|---|---:|---:|---:|
| Builder Quality | 5 | 25% | 1.25 |
| Retrieval Effectiveness | 4 | 25% | 1.00 |
| Answer Quality | 2 | 30% | 0.60 |
| Pipeline Health | 5 | 10% | 0.50 |
| Ablation Impact | 5 | 10% | 0.50 |
| **Overall** |  |  | **3.85** |

## Dimension Analysis

### 1. Builder Quality (5/5)
- `tables_parsed=10`, `tables_completed=10`, `all_tables_completed=true`
- `cypher_failed=false`, `failed_mappings=[]`, `ingestion_errors=[]`
- `triplets_extracted=231`, `entities_resolved=228` → triplet density is healthy (no sign of weak extraction/ER collapse).
**Verdict:** Builder pipeline is fully functional with no detectable structural issues.

### 2. Retrieval Effectiveness (4/5)
- `grounded_rate=1.0` and `avg_gt_coverage=0.941` indicates the system is consistently retrieving the right KG sources.
- `avg_top_score=0.724` is in the expected healthy band for a cross-encoder reranker (and slightly above 0.7 threshold behaviors seen in similar setups).
- `pipeline_health.questions_with_low_retrieval_score=0` and `gate_abstentions=0` → no retrieval-triggered abstentions.

**Concern:** multiple questions that should be answerable via schema-level joins instead report “cannot determine / cannot answer” (e.g., Q012, Q014, Q016, Q020, Q028). That points to **answer-generation sufficiency and/or context usefulness**, not retrieval failure—so retrieval is “good,” but not translating into correct query-instruction responses.

### 3. Answer Quality (2/5)
Although `grounded=true` for every question, the *semantic correctness vs. expected answer intent* is mixed:
- Several intermediate/advanced **multi-hop** questions return “I cannot find this information…” or generic uncertainty despite context that should support the query shape.
- Several **privacy-focused aggregated** questions also fail to provide the expected aggregation/query pattern.

Examples (worst 3):
- **Q012 (multi-hop)** “Which patients have received treatments from cardiology department providers?”  
  Expected: join patients→treatments→providers→departments filter Cardiology and return patient MRN/name/treatment/provider.  
  Generated: explicitly says it cannot find it. Despite listing relevant tables and FKs in contexts, it never provides the required join logic or fields.  
- **Q014 (multi-hop)** “Which providers have prescribed medications to patients with a specific diagnosis?”  
  Expected: diagnoses→patients→medications→providers filtered by ICD-10.  
  Generated: “cannot find… medications/prescriptions table/link…” (despite earlier questions demonstrating medication table/foreign keys exist).
- **Q016 (multi-hop)** “Which departments have the highest volume of patient appointments?”  
  Expected: appointments→departments join, group/count, exclude canceled/no-show.  
  Generated: says cannot compute highest volume; again does not provide the correct grouping logic even though schema-level requirements are described.

Best 3 (still not perfect, but closest to expected intent):
- **Q001 (patients tables)** correct mapping of patient-related tables at schema/relationship level.
- **Q002 (diagnosis coding/classification)** includes ICD-10 field + diagnosis_type set values and principal/comorbidity/admitting/secondary—high alignment.
- **Q010 (treatments documentation)** very complete schema-driven answer including required columns, constraints, historization, soft delete.

**Bottom line:** The system appears to be “grounded in retrieved chunks” but fails to meet **task completion** on many multi-hop/aggregation/temporal privacy questions.

### 4. Pipeline Health (5/5)
- `total_grader_rejections=0`, `grader_inconsistencies=0`, `gate_abstentions=0`
- `cypher_failed=false`, `failed_mappings_count=0`, `ingestion_errors_count=0`
- Latencies are reported as `elapsed_s=0` in builder/query reports (likely a logging artifact), but no stability failures are present.

### 5. Ablation Impact (5/5)
- Study is labeled **AB-BEST** and no ablation flags are shown as disabled in `config`; it looks like the best/combined configuration (hybrid retrieval + reranker enabled).
- Observed behavior matches the “best case”: complete builder, strong retrieval confidence, no pipeline errors.
**Verdict:** consistent with a “best” configuration.

---

## Per-Question Deep Dive

### Q001: What tables store information about patients?
- **Type:** concept_lookup | **Difficulty:** simple
- **Verdict:** CORRECT
- **Expected:** patients table + related patient clinical/admin tables via FK (diagnoses/treatments/medications/lab_results/appointments/claims)
- **Generated:** Correctly identifies `patients` as storing demographics/admin/contacts and references related tables (e.g., `treatments`)
- **Analysis:** Matches expected schema-level coverage; no missing key patient-related tables.
- **Retrieval:** gt_coverage=1.0, top_score=0.9432431035, gate=proceed

### Q002: How are medical diagnoses coded and classified?
- **Type:** concept_lookup | **Difficulty:** simple
- **Verdict:** CORRECT
- **Expected:** diagnoses.icd_10_code; diagnosis_type values principal/comorbidity/admitting/secondary; diagnosis/provider/dates
- **Generated:** Correct ICD-10 storage + diagnosis_type CHECK values + principal rules + resolution_date logic
- **Analysis:** Strong alignment with expected facts and classifications.
- **Retrieval:** gt_coverage=1.0, top_score=0.7 (raw 0.686), gate=proceed

### Q003: What information is tracked for medications prescribed to patients?
- **Type:** concept_lookup | **Difficulty:** simple
- **Verdict:** PARTIALLY_CORRECT
- **Expected:** medication_name, NDC, dosage, route, frequency, prescribing provider, start/end, historization; active end_date NULL
- **Generated:** Mentions identifiers, drug details, dosing/route, prescription period, audit timestamps—**does not explicitly cover** NDC, frequency, and active end_date NULL in the presented answer
- **Analysis:** Mostly correct but less complete than expected.
- **Retrieval:** gt_coverage=1.0, top_score=0.7604728132, gate=proceed

### Q004: How are healthcare providers organized and tracked?
- **Type:** concept_lookup | **Difficulty:** simple
- **Verdict:** PARTIALLY_CORRECT
- **Expected:** providers table: NPI, name, provider_type set, specialty, department affiliation, is_active/is_deleted, temporal historization
- **Generated:** Includes NPI, provider_type values, dept linkage, is_active, valid_from; misses explicit is_deleted flag mention and some column details
- **Analysis:** Near-complete but not fully matching the expected field list.
- **Retrieval:** gt_coverage=1.0, top_score=0.7 (raw 0.55), gate=proceed

### Q005: What is the structure of departments and how do they relate to each other?
- **Type:** concept_lookup | **Difficulty:** simple
- **Verdict:** CORRECT
- **Expected:** department_name/code, parent_department_id hierarchy, service_line, location, is_active/is_deleted
- **Generated:** Correctly describes hierarchy via `parent_department_id` and key columns
- **Analysis:** Matches expected structure (though one FK wording is a bit inconsistent).
- **Retrieval:** gt_coverage=1.0, top_score=0.7 (raw 0.55), gate=proceed

### Q006: How are insurance plans and payers represented in the system?
- **Type:** concept_lookup | **Difficulty:** simple
- **Verdict:** CORRECT
- **Expected:** insurance_plans fields + payer_name/plan_type/prior_auth_required + is_active + historization; patients.primary_insurance_id FK
- **Generated:** Correctly describes insurance_plans attributes (plan_type, prior_auth_required, is_active, validity/audit) and links via claims.insurance_plan_id
- **Analysis:** Mostly aligned; mentions patients linkage indirectly but does not explicitly restate primary_insurance_id.
- **Retrieval:** gt_coverage=1.0, top_score=0.7 (raw 0.55), gate=proceed

### Q007: What constitutes an insurance claim and what is its lifecycle?
- **Type:** concept_lookup | **Difficulty:** simple
- **Verdict:** CORRECT
- **Expected:** claims table fields + claim_status workflow + denial_reason for denied
- **Generated:** Correct claim definition, lifecycle states, financial fields, audit + soft delete + valid_from/valid_to
- **Analysis:** Strong match to expected lifecycle.
- **Retrieval:** gt_coverage=1.0, top_score=0.7 (raw 0.55), gate=proceed

### Q008: How are patient appointments scheduled and tracked?
- **Type:** concept_lookup | **Difficulty:** simple
- **Verdict:** PARTIALLY_CORRECT
- **Expected:** appointment columns + type/status workflow + cancellation_reason + appointment types
- **Generated:** Correctly covers scheduling, provider/department links, status types, soft delete; **does not explicitly include** appointment_type allowed set or cancellation_reason
- **Analysis:** Good but incomplete relative to expected detail.
- **Retrieval:** gt_coverage=1.0, top_score=0.7 (raw 0.55), gate=proceed

### Q009: What information is captured in laboratory test results?
- **Type:** concept_lookup | **Difficulty:** simple
- **Verdict:** PARTIALLY_CORRECT
- **Expected:** test_name + LOINC code, test_value, unit, reference_range, is_abnormal, ordering_provider_id, result_date, notes; abnormal indexed
- **Generated:** Mentions reference_range/provider/result date/metadata; **does not explicitly confirm** LOINC code or is_abnormal mechanics/flag use
- **Analysis:** Directionally correct but missing some expected specifics.
- **Retrieval:** gt_coverage=1.0, top_score=0.8398653507, gate=proceed

### Q010: How are medical treatments and procedures documented?
- **Type:** concept_lookup | **Difficulty:** simple
- **Verdict:** CORRECT
- **Expected:** treatments columns (patient_id/diagnosis_id/name/CPT/provider/department/date/status/notes) + diagnosis necessity + status set + historization
- **Generated:** Very complete: includes required constraints and fields + historization/soft delete + diagnosis linkage
- **Analysis:** Excellent alignment.
- **Retrieval:** gt_coverage=1.0, top_score=0.7 (raw 0.55), gate=proceed

### Q011: What are all the diagnoses for a specific patient, including the providers who diagnosed them?
- **Type:** multi_hop | **Difficulty:** intermediate
- **Verdict:** PARTIALLY_CORRECT
- **Expected:** exact join pattern patients→diagnoses→providers with filters and fields
- **Generated:** Explains conceptually, but **does not provide exact join/filter column names** and admits it cannot provide exact query/join
- **Analysis:** Missing required “join path” specificity.
- **Retrieval:** gt_coverage=0.8333, top_score=0.8571713509, gate=proceed

### Q012: Which patients have received treatments from cardiology department providers?
- **Type:** multi_hop | **Difficulty:** intermediate
- **Verdict:** INCORRECT
- **Expected:** join patients→treatments→providers→departments filter department_name='Cardiology' and return patient MRN/name/treatment/provider
- **Generated:** “I cannot find this information…”, does not provide the requested join/query logic
- **Analysis:** Fails task completion despite context claiming existence of provider/department linkage.
- **Retrieval:** gt_coverage=1.0, top_score=0.7 (raw 0.55), gate=proceed

### Q013: What treatments have been performed for a patient's specific diagnosis?
- **Type:** multi_hop | **Difficulty:** intermediate
- **Verdict:** PARTIALLY_CORRECT
- **Expected:** diagnoses→treatments→patients→providers, filter by patient_id and ICD-10; return treatment/provider/department/date/status
- **Generated:** Provides conceptual linkage, but lacks exact join/filter details for ICD-10 and provider/dept return fields
- **Analysis:** Under-specifies compared to expected.
- **Retrieval:** gt_coverage=0.8333, top_score=0.8127187236, gate=proceed

### Q014: Which providers have prescribed medications to patients with a specific diagnosis?
- **Type:** multi_hop | **Difficulty:** intermediate
- **Verdict:** INCORRECT
- **Expected:** diagnoses→patients→medications→providers filter ICD-10; return provider name/NPI/specialty + patient name + medication/dosage/dates
- **Generated:** “I cannot find…”; states missing medication linkages though other questions show medications+provider linkage exists in schema context
- **Analysis:** Contradiction with earlier schema signals; fails required join/query logic.
- **Retrieval:** gt_coverage=0.5, top_score=0.7 (raw 0.55), gate=proceed

### Q015: What is the complete medication history for a patient including prescribing providers?
- **Type:** multi_hop | **Difficulty:** intermediate
- **Verdict:** PARTIALLY_CORRECT
- **Expected:** medication fields (name, NDC, dosage, route, frequency, start/end), prescribing provider, include historized (valid_to not null)
- **Generated:** Notes cannot provide complete patient-specific history; lists prescribing provider join but claims missing patient foreign key/fields
- **Analysis:** Too conservative; incomplete vs expected.
- **Retrieval:** gt_coverage=1.0, top_score=0.7 (raw 0.55), gate=proceed

### Q016: Which departments have the highest volume of patient appointments?
- **Type:** multi_hop | **Difficulty:** intermediate
- **Verdict:** INCORRECT
- **Expected:** appointments→departments group/count (exclude canceled/no-show), order DESC
- **Generated:** Says cannot find volume computation; does not provide grouping logic.
- **Analysis:** Fails aggregation intent.
- **Retrieval:** gt_coverage=1.0, top_score=0.7 (raw 0.55), gate=proceed

### Q017: What claims have been submitted for a specific patient's treatments?
- **Type:** multi_hop | **Difficulty:** intermediate
- **Verdict:** INCORRECT
- **Expected:** treatments→claims join (via patient_id/service_date approx), return claim+payer/plan fields
- **Generated:** Says no relationship between claims and treatments described; partially answers “claims for a patient”
- **Analysis:** Not fully correct for “for treatments” join requirement.
- **Retrieval:** gt_coverage=1.0, top_score=0.7 (raw 0.55), gate=proceed

### Q018: Which providers in a specific department have ordered abnormal lab results?
- **Type:** multi_hop | **Difficulty:** intermediate
- **Verdict:** INCORRECT
- **Expected:** lab_results.abnormal filter + ordering_provider→department filter; return provider/patient/test fields
- **Generated:** “cannot determine abnormal… does not provide abnormal flag/structure; cannot filter department”
- **Analysis:** Under-uses retrieved schema; fails task completion.
- **Retrieval:** gt_coverage=1.0, top_score=0.7 (raw 0.55), gate=proceed

### Q019: What is a patient's complete care journey including diagnoses, treatments, and medications?
- **Type:** multi_hop | **Difficulty:** advanced
- **Verdict:** PARTIALLY_CORRECT
- **Expected:** multi-join timeline across diagnoses/treatments/medications/lab_results/appointments with chronological ordering
- **Generated:** Claims schema context insufficient for complete journey; explicitly says medications not present in context (but earlier context exists in other queries)
- **Analysis:** Likely overly conservative; does not produce the expected longitudinal plan.
- **Retrieval:** gt_coverage=0.9, top_score=0.7 (raw 0.55), gate=proceed

### Q020: Which insurance plans have the highest claim denial rates?
- **Type:** multi_hop | **Difficulty:** intermediate
- **Verdict:** INCORRECT
- **Expected:** claims→insurance_plans group/count denied and compute denial_rate
- **Generated:** Says no instance-level data or denial-rate definition; cannot compute highest denial rates
- **Analysis:** Fails aggregation/query intent; schema-level query shape should be possible.
- **Retrieval:** gt_coverage=1.0, top_score=0.7 (raw 0.55), gate=proceed

### Q021: What were a patient's diagnoses in a specific past time period?
- **Type:** temporal | **Difficulty:** intermediate
- **Verdict:** PARTIALLY_CORRECT
- **Expected:** diagnoses filtered by resolution_date/date range + temporal validity logic + return codes/names/provider
- **Generated:** Says cannot answer instance-level due to missing join/filter column names and historical rules
- **Analysis:** Under-specified vs expected query instructions.
- **Retrieval:** gt_coverage=1.0, top_score=0.7 (raw 0.55), gate=proceed

### Q022: How have a patient's medications changed over time?
- **Type:** temporal | **Difficulty:** intermediate
- **Verdict:** PARTIALLY_CORRECT
- **Expected:** medications with active periods + historized changes (valid_to/end_date transitions)
- **Generated:** Explains historization/soft delete pattern but does not provide the concrete change-over-time reconstruction logic the expected answer calls for
- **Analysis:** More concept than procedure.
- **Retrieval:** gt_coverage=1.0, top_score=0.7 (raw 0.55), gate=proceed

### Q023: What was a provider's department affiliation at a specific past date?
- **Type:** temporal | **Difficulty:** intermediate
- **Verdict:** PARTIALLY_CORRECT
- **Expected:** provider→department with effective dating at historical_date (valid_from/valid_to)
- **Generated:** Says missing column names/effective-dating logic
- **Analysis:** Incomplete vs expected temporal reconstruction.
- **Retrieval:** gt_coverage=1.0, top_score=0.7 (raw 0.55), gate=proceed

### Q024: Show all changes to a patient's primary insurance coverage over time.
- **Type:** temporal | **Difficulty:** intermediate
- **Verdict:** PARTIALLY_CORRECT
- **Expected:** patients→insurance_plans using primary_insurance_id, include historized versions (valid_from/valid_to) order by valid_from DESC
- **Generated:** Provides relationship + general historization approach but cannot confirm exact SQL-level filters across patients/insurance_plans
- **Analysis:** Lacks the precise required reconstruction logic.
- **Retrieval:** gt_coverage=1.0, top_score=0.7 (raw 0.55), gate=proceed

### Q025: What diagnoses were resolved within a specific time period?
- **Type:** temporal | **Difficulty:** intermediate
- **Verdict:** PARTIALLY_CORRECT
- **Expected:** resolution_date not null and in-range + join to provider/patient filters
- **Generated:** Talks about availability of resolution_date but does not provide the concrete filtering/returned fields procedure.
- **Analysis:** Needs more explicit query logic.
- **Retrieval:** gt_coverage=1.0, top_score=0.7 (raw 0.55), gate=proceed

### Q026: Reconstruct a patient's active medications as of a specific historical date.
- **Type:** temporal | **Difficulty:** advanced
- **Verdict:** PARTIALLY_CORRECT
- **Expected:** active period logic using start/end + record validity window using valid_from/valid_to
- **Generated:** Correctly outlines general historization/soft delete approach but stops short of the required “as-of date inclusion” predicate
- **Analysis:** Missing the key as-of condition.
- **Retrieval:** gt_coverage=1.0, top_score=0.7 (raw 0.55), gate=proceed

### Q027: Count the number of patients per department without exposing individual patient identities.
- **Type:** privacy_focused | **Difficulty:** intermediate
- **Verdict:** INCORRECT
- **Expected:** aggregate counts DISTINCT patient_id per department via appointments filter canceled/no-show and date range; no identifiers
- **Generated:** Says cannot determine join paths/columns needed; does not provide aggregation query structure
- **Analysis:** Fails privacy aggregation task.
- **Retrieval:** gt_coverage=1.0, top_score=0.7 (raw 0.55), gate=proceed

### Q028: What are the most common diagnoses (by count) without linking to specific patients?
- **Type:** privacy_focused | **Difficulty:** simple
- **Verdict:** INCORRECT
- **Expected:** diagnoses grouped by icd_10_code/diagnosis_name with COUNT(*) ordered DESC
- **Generated:** Refuses to compute because no instance counts/rows; does not provide the correct schema-level aggregation query shape
- **Analysis:** The task is query-construction/aggregation, not execution-time counts.
- **Retrieval:** gt_coverage=0.5, top_score=0.7 (raw 0.55), gate=proceed

### Q029: Which providers have the highest patient volume without exposing patient information?
- **Type:** privacy_focused | **Difficulty:** intermediate
- **Verdict:** PARTIALLY_CORRECT
- **Expected:** aggregate DISTINCT patient_id per provider using appointments filter completed, date range; return only provider info + counts
- **Generated:** Explains inability to answer without operational counts but provides some schema path reasoning and privacy filtering principles
- **Analysis:** Partially addresses what to do, but not the concrete query specification.
- **Retrieval:** gt_coverage=0.6667, top_score=0.7 (raw 0.55), gate=proceed

### Q030: What is the average claim payment amount by insurance plan type?
- **Type:** privacy_focused | **Difficulty:** intermediate
- **Verdict:** PARTIALLY_CORRECT
- **Expected:** group by plan_type and compute AVG(amount_paid/amount_charged) with claim_status filter
- **Generated:** Correctly describes calculation concept but says insurance plan type is not defined in schema; thus cannot provide full query.
- **Analysis:** More conceptual than actionable; still misses key schema element mapping.
- **Retrieval:** gt_coverage=1.0, top_score=0.7 (raw 0.55), gate=proceed

---

## Anomalies & Recommendations

### Red Flags
1. **Groundedness is not aligning with task success.** Many incorrect/underdelivered answers are marked `grounded=true` with `gate_decision=proceed`, even when the response admits it cannot provide the required join/query shape (e.g., Q012, Q014, Q016, Q020, Q028).
2. **Excessive “cannot determine” behavior on multi-hop/aggregation tasks** despite `gt_coverage` being high (often 1.0). This suggests the LLM is not leveraging the retrieved schema evidence to construct the requested join/aggregation pattern.
3. **Evaluation mismatch for aggregation/temporal questions:** several failures stem from treating “no instance-level data” as an inability to provide query construction steps. The expected answers are largely about **query structure**, not computed numeric results.

### Recommendations
- **Tighten the query-intent contract:** For multi-hop/temporal/privacy questions, enforce that the generator must output:
  1) the join path (tables/keys),
  2) the required filters (temporal validity, soft delete, status),
  3) the returned fields and grouping/aggregation logic—*even if instance counts are not computable*.
- **Recalibrate semantic grading vs groundedness:** Update internal grader logic (or evaluation labeling) so that “admits inability to provide joins/aggregation even though schema evidence exists” is considered a correctness failure, not merely a grounding success.
- **Add schema-to-join reconstruction prompting:** In Query Graph answer generation, inject an explicit “schema assembly checklist” using retrieved contexts’ FK lines (e.g., `X.patient_id -> patients.patient_id`) to force join-path completion.
- **Specifically audit medications/prescriptions linkage handling:** Q014 and Q015 suggest inconsistent usage of the medications foreign key and patient scoping; add a rule-based extraction step for the exact FK column names from contexts.

---

## Comparison Notes (if applicable)
AB-BEST appears to be the “best” configuration (hybrid retrieval + reranker enabled, no ablations disabled), and it **does** achieve best-in-class Builder completeness and retrieval confidence.  
The remaining degradation is therefore likely in **Answer Generation / context utilization for join-and-aggregation tasks**, not in retrieval or graph construction.