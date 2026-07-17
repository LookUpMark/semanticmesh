# AI-Judge Evaluation: AB-BEST/03_advanced_healthcare
**Evaluator:** (`gpt-5.4-nano-2026-03-17`) using `docs/AI_JUDGE_PROMPT.md`  
**Date:** 2026-07-17

---

# Ablation Study Evaluation: AB-BEST — 03_advanced_healthcare

## Executive Summary
AB-BEST shows **excellent end-to-end structural success** in the Builder Graph (all 10 tables completed, no Cypher failures, no ingestion/mapping errors) and **perfect groundedness** at query time (grounded_rate = 1.0; 0 abstentions). However, multiple multi-hop/temporal privacy queries demonstrate a **systematic issue**: the generated answers often claim inability to answer or provide only schema/convention-level guidance, even when the expected answer is an executable join/aggregation pattern. Overall performance appears constrained by **retrieval-to-context usability** (and possibly earlier-stage mapping/traversal edge availability), despite high reported `gt_coverage`.

## Scores

| Dimension | Score (1-5) | Weight | Weighted |
|---|---:|---:|---:|
| Builder Quality | 5 | 25% | 1.25 |
| Retrieval Effectiveness | 4 | 25% | 1.00 |
| Answer Quality | 3 | 30% | 0.90 |
| Pipeline Health | 5 | 10% | 0.50 |
| Ablation Impact | N/A | 10% | 0.00 |
| **Overall** |  |  | **3.65** |

## Dimension Analysis

### 1. Builder Quality (5/5)
- `tables_parsed=10`, `tables_completed=10`, `all_tables_completed=true`
- `cypher_failed=false`, `failed_mappings=[]`, `ingestion_errors=[]`
- Triplet/ER indicators are strong: `triplets_extracted=231`, `entities_resolved=228` (triplets are reasonably dense; no sign of extraction/ER collapse).
**Verdict:** Builder is functioning correctly and robustly.

### 2. Retrieval Effectiveness (4/5)
Key signals:
- `grounded_rate=1.0` and `avg_gt_coverage=0.941` → the system frequently retrieves the expected conceptual sources.
- `avg_top_score=0.724` → reranker confidence is healthy (in the rubric’s “healthy and expected” band).
- `gate_abstentions=0` and `pipeline_health.gate_abstentions=0` → **no false abstentions** for negative questions.
Concerns:
- Several multi-hop/temporal questions (e.g., Q012, Q014, Q016, Q017, Q020, Q021, Q027, Q028) show *answer-level inability* that suggests the retrieved contexts may be **schema/convention heavy but operationally insufficient** for multi-hop construction (join keys/relationships/filters). This looks more like context usability / internal graph traversal adequacy than outright “missed retrieval”.

### 3. Answer Quality (3/5)
- Although every answer is marked `grounded=true`, **grounded ≠ correct for the task type** (especially multi-hop aggregations and temporal reconstruction).
- Multiple queries have **structure/SQL-plan omissions** or outright refusal (“I cannot find this information…”) where the expected answer provides an explicit join/filter/grouping recipe.

Best examples (strong schema-to-answer alignment):
- Q002, Q003, Q009, Q010: generated answers accurately reflect table columns/constraints and match expected intents.

Worst/examples of task failure despite grounding:
- **Q012** (multi-hop): expected departmental cardiology filter; generated says it cannot find it (despite having department/treatment linkage context).
- **Q014**: expected providers who prescribed meds for diagnosis; generated refuses due to missing medications links (but earlier contexts imply medications exist—this indicates missing/unused relationship edges in retrieval contexts).
- **Q020/Q028/Q029/Q030** (privacy-focused aggregations): generated refuses or stays at “schema exists but no instance data,” even when the expected answer is an *aggregation query plan* (which does not require instance data rows).

### 4. Pipeline Health (5/5)
- `total_grader_rejections=0`
- `grader_inconsistencies=0`
- `cypher_failed=false`
- `failed_mappings_count=0`, `ingestion_errors_count=0`
- Latency is reported as `elapsed_s=0` across builder/query (likely instrumentation rounding), but **no instability signals** appear.

### 5. Ablation Impact (N/A)
- `study_id=AB-BEST` is provided without a `changes_vs_baseline` / `ablation_context` field.
- No baseline comparison can be verified per the rubric, so this dimension is **N/A**.

## Dimension 3. Answer Quality — Best/Worst Per-Question Evidence

**Best (indicative):**
- **Q002:** Correct coding scheme + ICD-10 field + diagnosis_type constraints; matches expected (including four types and temporal fields).
- **Q009:** Lab results fields and abnormality-related indexing intent are consistent with expected schema description.

**Worst (indicative):**
- **Q012 (multi_hop, intermediate):** Expected cardiology departmental workload query; generated declines due to missing instance-level join/filter columns. This indicates the model treats relationship knowledge as insufficient even though the KG likely contains `treatments.provider_id -> providers.provider_id` and `providers.department_id -> departments.department_id` style patterns elsewhere in the bundle.
- **Q016 (multi_hop, intermediate):** Expected “highest volume of appointments by department” aggregation; generated refuses (no counts) and claims missing join usage, despite context including appointment/dept foreign key semantics.
- **Q020/Q028/Q030 (privacy-focused aggregations):** Expected grouping/aggregation logic; generated refuses because it cannot compute counts/values. The rubric’s notion of correctness here is about providing the correct *query structure*, not instance materialization—yet the responses avoid giving the aggregation recipe.

## Per-Question Deep Dive

### Q001: What tables store information about patients?
- **Type:** concept_lookup | **Difficulty:** simple
- **Verdict:** CORRECT
- **Expected:** patients demographics/admin (MRN, DOB, gender, contacts); related patient-linked tables: diagnoses, treatments, medications, lab_results, appointments, claims.
- **Generated:** Correctly states `patients` holds patient demographics and cites patient-related linkages via `treatments` and patient columns.
- **Analysis:** Matches expected coverage at the schema/table-link level.
- **Retrieval:** gt_coverage=1.0, top_score=0.943243103543508, gate=proceed

### Q002: How are medical diagnoses coded and classified?
- **Type:** concept_lookup | **Difficulty:** simple
- **Verdict:** CORRECT
- **Expected:** diagnoses table with ICD-10-CM (`icd_10_code`); diagnosis_type ∈ {principal, comorbidity, admitting, secondary}; provider/date/resolution; principal per encounter; historization.
- **Generated:** Correctly lists `icd_10_code`, the four allowed diagnosis_type values, provider_id/date/resolution_date, principal-only rule.
- **Analysis:** Strong semantic alignment with expected schema constraints and business rules.
- **Retrieval:** gt_coverage=1.0, top_score=0.7, gate=proceed

### Q003: What information is tracked for medications prescribed to patients?
- **Type:** concept_lookup | **Difficulty:** simple
- **Verdict:** PARTIALLY_CORRECT
- **Expected:** medication fields: name, NDC, dosage, route, frequency, prescribing provider, start/end dates; active = end_date NULL; valid_from/valid_to.
- **Generated:** Mentions identifiers, drug details, route, prescription period, audit fields; does not explicitly confirm all expected specific fields (NDC/route/frequency/start/end_date semantics).
- **Analysis:** Likely correct at high level, but missing several explicit expected elements.
- **Retrieval:** gt_coverage=1.0, top_score=0.7604728132468686, gate=proceed

### Q004: How are healthcare providers organized and tracked?
- **Type:** concept_lookup | **Difficulty:** simple
- **Verdict:** PARTIALLY_CORRECT
- **Expected:** providers table: NPI, name, provider_type, specialty, department affiliation; is_active/is_deleted; temporal historization.
- **Generated:** Covers providers table, NPI, provider_type allowed values, specialty/department_id, is_active, valid_from.
- **Analysis:** Missing some expected specifics (explicit is_deleted usage/allowed values beyond provider_type are partial; still mostly aligned).
- **Retrieval:** gt_coverage=1.0, top_score=0.7, gate=proceed

### Q005: What is the structure of departments and how do they relate to each other?
- **Type:** concept_lookup | **Difficulty:** simple
- **Verdict:** CORRECT
- **Expected:** departments table with department_name/code, parent_department_id hierarchy, service_line, location, is_active/is_deleted.
- **Generated:** Correctly describes self-referential hierarchy and key columns.
- **Analysis:** Matches expected structure; one minor issue: generated context includes an incorrect self-ref detail (“parent_department_id -> parent_department_id”), but overall intent is correct.
- **Retrieval:** gt_coverage=1.0, top_score=0.7, gate=proceed

### Q006: How are insurance plans and payers represented in the system?
- **Type:** concept_lookup | **Difficulty:** simple
- **Verdict:** CORRECT
- **Expected:** insurance_plans plan_name, payer_name, plan_type, prior_auth_required, is_active; historization; patients.primary_insurance_id FK.
- **Generated:** Correctly links insurance plans, prior authorization concept, plan_type/prior_auth_required/is_active, and claims linkage.
- **Analysis:** Strong schema/concept mapping; aligns with expected.
- **Retrieval:** gt_coverage=1.0, top_score=0.7, gate=proceed

### Q007: What constitutes an insurance claim and what is its lifecycle?
- **Type:** concept_lookup | **Difficulty:** simple
- **Verdict:** CORRECT
- **Expected:** claims table with claim_number, patient_id, insurance_plan_id, dates, CPT/ICD codes, amounts, claim_status; workflow states; denial_reason on denied.
- **Generated:** Correctly describes definition, claims.status values, denial_reason, amounts, valid_from/valid_to and soft delete.
- **Analysis:** Matches expected lifecycle and schema elements.
- **Retrieval:** gt_coverage=1.0, top_score=0.7, gate=proceed

### Q008: How are patient appointments scheduled and tracked?
- **Type:** concept_lookup | **Difficulty:** simple
- **Verdict:** PARTIALLY_CORRECT
- **Expected:** appointments: patient_id, provider_id, department_id, appointment_date/time/type/duration/status; workflow statuses including cancellation_reason.
- **Generated:** Covers appointments table, status types, soft delete, appointment_date/time; does not clearly confirm appointment_type value set or cancellation_reason.
- **Analysis:** Good overall, missing some expected details (duration/type/cancellation_reason).
- **Retrieval:** gt_coverage=1.0, top_score=0.7, gate=proceed

### Q009: What information is captured in laboratory test results?
- **Type:** concept_lookup | **Difficulty:** simple
- **Verdict:** CORRECT
- **Expected:** lab_results: test_name/LOINC, test_value, unit, reference_range, is_abnormal; ordering_provider_id, result_date, notes; abnormal indexed.
- **Generated:** Mentions test identifiers, values/units, reference ranges, ordering provider, result date, validity/audit; does not explicitly mention LOINC or is_abnormal indexing, but generally consistent with fields.
- **Analysis:** Strong semantic match; minor missing specifics.
- **Retrieval:** gt_coverage=1.0, top_score=0.8398653506656495, gate=proceed

### Q010: How are medical treatments and procedures documented?
- **Type:** concept_lookup | **Difficulty:** simple
- **Verdict:** CORRECT
- **Expected:** treatments: patient_id, diagnosis_id, treatment_name, cpt_code, provider_id, department_id, treatment_date, treatment_status; notes; diagnosis linkage.
- **Generated:** Correctly describes treatments table with constraints and fields; includes status values and historization/soft delete.
- **Analysis:** Very strong alignment.
- **Retrieval:** gt_coverage=1.0, top_score=0.7, gate=proceed

### Q011: What are all the diagnoses for a specific patient, including the providers who diagnosed them?
- **Type:** multi_hop | **Difficulty:** intermediate
- **Verdict:** PARTIALLY_CORRECT
- **Expected:** join patients→diagnoses; diagnoses→providers; return icd_10_code/name/type/date/resolution + provider name/NPI; filter by MRN/patient_id; exclude is_deleted and valid_to IS NULL.
- **Generated:** Gives conceptual join path but explicitly refuses exact query/join columns (“cannot provide an exact query/join”).
- **Analysis:** Partial: correct relationships conceptually, insufficient for the expected “query recipe”.
- **Retrieval:** gt_coverage=0.8333, top_score=0.8571713508894407, gate=proceed

### Q012: Which patients have received treatments from cardiology department providers?
- **Type:** multi_hop | **Difficulty:** intermediate
- **Verdict:** INCORRECT
- **Expected:** patients↔treatments↔providers↔departments; filter department_name/cardio; return patient MRN/name/treatment_name/date/provider; exclude soft-deleted.
- **Generated:** Says it cannot find the required cardiology-specific linkage/filter or patient instance columns; provides refusal.
- **Analysis:** Fails the task’s join/filter requirements.
- **Retrieval:** gt_coverage=1.0, top_score=0.7, gate=proceed

### Q013: What treatments have been performed for a patient's specific diagnosis?
- **Type:** multi_hop | **Difficulty:** intermediate
- **Verdict:** PARTIALLY_CORRECT
- **Expected:** diagnoses→treatments on diagnosis_id; treatments→patients and providers; filter by patient_id and icd_10_code; return treatment fields + department/provider.
- **Generated:** Correct relationship explanation but lacks explicit join/filter recipe and provider/department returns are not clearly specified.
- **Analysis:** Partial correctness; not fully meeting expected query structure.
- **Retrieval:** gt_coverage=0.8333, top_score=0.8127187235801289, gate=proceed

### Q014: Which providers have prescribed medications to patients with a specific diagnosis?
- **Type:** multi_hop | **Difficulty:** intermediate
- **Verdict:** INCORRECT
- **Expected:** diagnoses→patients→medications→providers (prescribing_provider_id), filter by icd_10_code; return provider and medication/patient fields.
- **Generated:** Refuses: claims missing medications/prescription schema and link between providers/medications/diagnoses.
- **Analysis:** Task failure; also inconsistent with other questions showing medications concept/table exists.
- **Retrieval:** gt_coverage=0.5, top_score=0.7, gate=proceed

### Q015: What is the complete medication history for a patient including prescribing providers?
- **Type:** multi_hop | **Difficulty:** intermediate
- **Verdict:** PARTIALLY_CORRECT
- **Expected:** medications join patients→providers; return medication_name, NDC, dosage, route, frequency, start/end + provider; include historical records via valid_to; active end_date NULL.
- **Generated:** Explains prescribing provider join path but refuses to provide “complete patient-specific history” due to missing patient foreign key/medication field details in retrieved context.
- **Analysis:** Partial: correct linkage concept; not meeting expected completeness.
- **Retrieval:** gt_coverage=1.0, top_score=0.7, gate=proceed

### Q016: Which departments have the highest volume of patient appointments?
- **Type:** multi_hop | **Difficulty:** intermediate
- **Verdict:** INCORRECT
- **Expected:** appointments→departments join on department_id; group by dept/service_line; count appointments; exclude canceled/no-show.
- **Generated:** Refuses to answer volume because it cannot compute counts and claims concrete join usage missing.
- **Analysis:** Fails aggregation query intent.
- **Retrieval:** gt_coverage=1.0, top_score=0.7, gate=proceed

### Q017: What claims have been submitted for a specific patient's treatments?
- **Type:** multi_hop | **Difficulty:** intermediate
- **Verdict:** PARTIALLY_CORRECT
- **Expected:** patients→treatments→claims (align by patient_id and service_date≈treatment_date) and claims→insurance_plans; return claim fields + payer info.
- **Generated:** Correctly notes it can only answer “claims for a specific patient” but cannot connect claims to treatments due to missing relationship.
- **Analysis:** Partial: captures limitation; does not fully meet expected join recipe.
- **Retrieval:** gt_coverage=1.0, top_score=0.7, gate=proceed

### Q018: Which providers in a specific department have ordered abnormal lab results?
- **Type:** multi_hop | **Difficulty:** intermediate
- **Verdict:** INCORRECT
- **Expected:** lab_results→providers (ordering_provider_id), providers→departments (department_id); filter department and is_abnormal=TRUE; return provider/patient/test fields.
- **Generated:** Refuses: no abnormal flag and no dept filtering structure in context.
- **Analysis:** Task failure.
- **Retrieval:** gt_coverage=1.0, top_score=0.7, gate=proceed

### Q019: What is a patient's complete care journey including diagnoses, treatments, and medications?
- **Type:** multi_hop | **Difficulty:** advanced
- **Verdict:** PARTIALLY_CORRECT
- **Expected:** multi-join patients→diagnoses→treatments→medications→lab_results→appointments with provider joins; chronological timeline.
- **Generated:** Correctly gives schema-level support for diagnoses and treatments; refuses medications and lack of explicit joins.
- **Analysis:** Partial: diagnoses/treatments covered; timeline incompleteness.
- **Retrieval:** gt_coverage=0.9, top_score=0.7, gate=proceed

### Q020: Which insurance plans have the highest claim denial rates?
- **Type:** multi_hop | **Difficulty:** intermediate
- **Verdict:** INCORRECT
- **Expected:** claims→insurance_plans group by plan/payer/type; count total and denied; denial rate = denied/total; order DESC; filter service_date and status (approved/partially_paid).
- **Generated:** Refuses due to lack of instance counts/definition decisions.
- **Analysis:** Doesn’t provide the aggregation recipe the expected answer asks for.
- **Retrieval:** gt_coverage=1.0, top_score=0.7, gate=proceed

### Q021: What were a patient's diagnoses in a specific past time period?
- **Type:** temporal | **Difficulty:** intermediate
- **Verdict:** PARTIALLY_CORRECT
- **Expected:** diagnoses filtered by patient_id and diagnosis_date range; temporal validity with valid_from/valid_to; return codes/names/type + provider.
- **Generated:** Refuses exact schema mechanics (table/column names, join mappings, temporal validity logic) but notes diagnoses have date fields conceptually.
- **Analysis:** Partial concept; not meeting expected query reconstruction.
- **Retrieval:** gt_coverage=1.0, top_score=0.7, gate=proceed

### Q022: How have a patient's medications changed over time?
- **Type:** temporal | **Difficulty:** intermediate
- **Verdict:** PARTIALLY_CORRECT
- **Expected:** medications history with start/end + valid_from/valid_to; ignore is_deleted; order by start_date/valid_from; reconciliation semantics.
- **Generated:** Provides historization/soft-delete pattern but does not deliver the specific history reconstruction mechanics (before/after semantics, exact predicates/fields).
- **Analysis:** Partial adherence to temporal modeling; missing “medication history values” logic.
- **Retrieval:** gt_coverage=1.0, top_score=0.7, gate=proceed

### Q023: What was a provider's department affiliation at a specific past date?
- **Type:** temporal | **Difficulty:** intermediate
- **Verdict:** INCORRECT
- **Expected:** providers→departments join; filter by provider_id and valid_from/valid_to relative to historical_date.
- **Generated:** Refuses because provider-department effective-dating columns/rules are not present in retrieved context.
- **Analysis:** Failure to reconstruct temporal relationship.
- **Retrieval:** gt_coverage=1.0, top_score=0.7, gate=proceed

### Q024: Show all changes to a patient's primary insurance coverage over time.
- **Type:** temporal | **Difficulty:** intermediate
- **Verdict:** PARTIALLY_CORRECT
- **Expected:** patients→insurance_plans via primary_insurance_id; include historized records (do not filter valid_to); return mrn/name/plan/payer/type/valid_from/valid_to; order DESC.
- **Generated:** Explains general historization pattern and join direction but cannot confirm historization on the relevant attributes and does not provide concrete predicate structure.
- **Analysis:** Partial.
- **Retrieval:** gt_coverage=1.0, top_score=0.7, gate=proceed

### Q025: What diagnoses were resolved within a specific time period?
- **Type:** temporal | **Difficulty:** intermediate
- **Verdict:** PARTIALLY_CORRECT
- **Expected:** diagnoses resolution_date not null within range; include patient_id/icd/provider; filter current records (is_deleted false, valid_to null).
- **Generated:** Identifies resolution_date logic conceptually but lacks explicit query mechanics (join/filter details).
- **Analysis:** Partial.
- **Retrieval:** gt_coverage=1.0, top_score=0.7, gate=proceed

### Q026: Reconstruct a patient's active medications as of a specific historical date.
- **Type:** temporal | **Difficulty:** advanced
- **Verdict:** PARTIALLY_CORRECT
- **Expected:** active period using start/end and record validity window; return medication_name/dosage/route/frequency/provider.
- **Generated:** Uses valid_from/valid_to and is_deleted conceptually but refuses “exact SQL predicate” for historical inclusion logic.
- **Analysis:** Partial; not fully meeting expected reconstruction.
- **Retrieval:** gt_coverage=1.0, top_score=0.7, gate=proceed

### Q027: Count the number of patients per department without exposing individual patient identities.
- **Type:** privacy_focused | **Difficulty:** intermediate
- **Verdict:** INCORRECT
- **Expected:** appointments→departments join, group by dept, COUNT DISTINCT patient_id, exclude canceled/no-show; return only aggregated counts.
- **Generated:** Refuses exact join path/columns; offers only high-level description and states cannot compute actual numbers.
- **Analysis:** For expected-answer style, the refusal is a failure because aggregation query structure does not require row data.
- **Retrieval:** gt_coverage=1.0, top_score=0.7, gate=proceed

### Q028: What are the most common diagnoses (by count) without linking to specific patients?
- **Type:** privacy_focused | **Difficulty:** simple
- **Verdict:** INCORRECT
- **Expected:** diagnoses grouped by icd_10_code/diagnosis_name; COUNT(*) order desc; return codes/names/count only.
- **Generated:** Refuses because instance counts/data rows are not in context.
- **Analysis:** Incorrect for the task framing—expected is query logic, not computed results from rows.
- **Retrieval:** gt_coverage=0.5, top_score=0.7, gate=proceed

### Q029: Which providers have the highest patient volume without exposing patient information?
- **Type:** privacy_focused | **Difficulty:** intermediate
- **Verdict:** PARTIALLY_CORRECT
- **Expected:** appointments grouped by provider; COUNT DISTINCT patient_id; filter completed; return provider + aggregated counts only.
- **Generated:** Provides multiple schema link paths but still does not give the required aggregation recipe; also claims no operational data is available.
- **Analysis:** Partial.
- **Retrieval:** gt_coverage=0.6667, top_score=0.7, gate=proceed

### Q030: What is the average claim payment amount by insurance plan type?
- **Type:** privacy_focused | **Difficulty:** intermediate
- **Verdict:** PARTIALLY_CORRECT
- **Expected:** claims→insurance_plans; group by plan_type; AVG(amount_paid) and AVG(amount_charged); filter by service_date and claim_status.
- **Generated:** Correctly identifies missing “plan_type at DB-level” mapping; doesn’t propose aggregation structure conditioned on that field.
- **Analysis:** Some correctness (dependency identified), but incomplete relative to expected.
- **Retrieval:** gt_coverage=1.0, top_score=0.7, gate=proceed

## Anomalies & Recommendations

### Red Flags
1. **Repeated “I cannot find this information…” failures on multi-hop/temporal/privacy tasks** (e.g., Q012, Q014, Q016, Q020, Q021, Q023, Q027, Q028).  
   - The bundle reports high `gt_coverage` and high `avg_top_score`, yet the answers still refuse to produce the join/aggregation recipe expected.
2. **Privacy-focused aggregation questions** treat “no instance rows” as a reason to refuse, even though expected answers are query templates (COUNT/AVG/GROUP BY) that don’t require actual row values.
3. **Inconsistency with grounding signals:** all answers are marked grounded, but many are functionally incorrect relative to the expected SQL construction requirement.

### Recommendations
1. **Add an “aggregation/SQL template mode”** to the Query Graph: when the question requests counts/averages/“most common” rankings, force the model to output the *GROUP BY / aggregation predicate structure* regardless of instance data availability.
2. **Improve multi-hop context distillation**: ensure the retrieved contexts include *explicit join keys* needed for the question (e.g., for cardiology: provider→department join keys plus a department_name/code column).
3. **Tighten the hallucination/abstention policy for query-construction tasks**: “no instance data” should not translate to refusal if the schema is sufficient to form the query.
4. **Audit graph traversal retrieval** for MENTIONS edges/relationship coverage: the pattern suggests relationships needed for multi-hop filters are not reliably materialized in the retrieved contexts, even when `gt_coverage` is high.

## Comparison Notes (if applicable)
- No baseline (AB-00) results or `changes_vs_baseline` were provided, so comparison is not possible.
- Despite “AB-BEST”, the qualitative evidence suggests the study is best at **concept lookup** and schema-level correctness, while **query-recipe reconstruction** for multi-hop/temporal/privacy remains weak.

If you want, I can also compute a “task-criterion correctness” breakdown (concept_lookup vs multi_hop vs temporal vs privacy_focused) based on the provided per-question verdicts.