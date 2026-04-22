# AB-BEST — 03_advanced_healthcare — Run Analysis

**Timestamp:** 2026-04-21 20:43:25  
**Run tag:** `run-20260421_221024`

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
| Triplets extracted | 42 |
| Entities resolved | 40 |
| Tables parsed | 10 |
| Tables completed | 10 |

## Query Evaluation Summary

| Metric | Value |
|--------|-------|
| Questions | 30 |
| Grounded | **30/30 (100%)** |
| Avg GT Coverage | 90% |
| Avg Top Score | 0.2895 |
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

**Sources retrieved (12):** `Patient Appointment→APPOINTMENTS`, `Treatment Record→TREATMENTS`, `Personal Details Emergency→PATIENTS`, `Laboratory Test Results→LAB_RESULTS`, `parent_chunk_data_dictionary.md_10`, `parent_chunk_data_dictionary.md_11`, `Treatment Record`, `Patient Appointment`

---

### ✅ Q002 — How are medical diagnoses coded and classified?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0000 | **Gate:** `proceed`

**Expected answer:**
> Diagnoses are stored in the diagnoses table with ICD-10-CM codes (icd_10_code field). They are classified into four types: 'principal' (primary condition), 'comorbidity' (additional conditions), 'admitting' (condition causing admission), and 'secondary'. Each diagnosis includes the diagnosis name, t…

**System answer:**
> 

**Sources retrieved (12):** `Additional Diagnosis That→DIAGNOSES`, `Treatment Record→TREATMENTS`, `parent_chunk_data_dictionary.md_10`, `parent_chunk_business_glossary.md_0`, `parent_chunk_data_dictionary.md_4`, `parent_chunk_business_glossary.md_1`, `parent_chunk_data_dictionary.md_5`, `Treatment Record`

---

### ✅ Q003 — What information is tracked for medications prescribed to patients?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0000 | **Gate:** `proceed`

**Expected answer:**
> The medications table tracks medication name, National Drug Code (NDC), dosage, route of administration (oral, IV, IM, topical, inhaled, subcutaneous), frequency, prescribing provider, start date, and end date. Active medications have a NULL end_date. The table uses temporal historization with valid…

**System answer:**
> 

**Sources retrieved (12):** `Treatment Record→TREATMENTS`, `Medication Administration To→MEDICATIONS`, `Laboratory Test Results→LAB_RESULTS`, `Personal Details Emergency→PATIENTS`, `parent_chunk_data_dictionary.md_10`, `Treatment Record`, `parent_chunk_business_glossary.md_0`, `parent_chunk_data_dictionary.md_6`

---

### ✅ Q004 — How are healthcare providers organized and tracked?

**Status:** GROUNDED  
**GT Coverage:** 50% | **Top Score:** 0.0000 | **Gate:** `proceed`

**Expected answer:**
> Providers are stored in the providers table with a unique National Provider Identifier (NPI), name, provider type (MD, DO, NP, PA, RN, PT, Other), specialty, and department affiliation. Providers have is_active and is_deleted flags for status tracking. The table uses temporal historization to track …

**System answer:**
> 

**Sources retrieved (12):** `Healthcare Providers For→PROVIDERS`, `Department→DEPARTMENTS`, `Patient Appointment→APPOINTMENTS`, `parent_chunk_data_dictionary.md_10`, `parent_chunk_business_glossary.md_2`, `Healthcare Providers For`, `parent_chunk_data_dictionary.md_8`, `parent_chunk_business_glossary.md_0`

---

### ✅ Q005 — What is the structure of departments and how do they relate to each other?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0000 | **Gate:** `proceed`

**Expected answer:**
> Departments are stored in the departments table with department_name, department_code, parent_department_id (self-referential foreign key for hierarchy), service_line (strategic grouping), and location. Departments can have parent departments creating a hierarchical structure (e.g., Cardiology as a …

**System answer:**
> 

**Sources retrieved (12):** `Department→DEPARTMENTS`, `parent_chunk_data_dictionary.md_10`, `parent_chunk_business_glossary.md_1`, `parent_chunk_data_dictionary.md_8`, `parent_chunk_data_dictionary.md_9`, `parent_chunk_data_dictionary.md_5`, `parent_chunk_business_glossary.md_0`, `parent_chunk_data_dictionary.md_3`

---

### ✅ Q006 — How are insurance plans and payers represented in the system?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0000 | **Gate:** `proceed`

**Expected answer:**
> The insurance_plans table stores plan_name, payer_name (insurance company), plan_type (commercial, medicare, medicaid, tricare, self_pay), and prior_auth_required flag. Plans have is_active status and use temporal historization. The patients table references insurance_plans via primary_insurance_id …

**System answer:**
> 

**Sources retrieved (12):** `Insurance Plan→INSURANCE_PLANS`, `parent_chunk_data_dictionary.md_10`, `Claim Scrubbing→CLAIMS`, `Personal Details Emergency→PATIENTS`, `parent_chunk_business_glossary.md_1`, `Insurance Plan`, `parent_chunk_data_dictionary.md_3`, `parent_chunk_business_glossary.md_0`

---

### ✅ Q007 — What constitutes an insurance claim and what is its lifecycle?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0000 | **Gate:** `proceed`

**Expected answer:**
> Claims are stored in the claims table with claim_number (unique identifier), patient_id, insurance_plan_id, service_date, submission_date, CPT code (procedure), ICD-10 code (diagnosis), amounts (charged, allowed, paid), and claim_status. Status workflow includes: submitted → pending → approved/denie…

**System answer:**
> 

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_10`, `Claim Scrubbing→CLAIMS`, `Insurance Plan→INSURANCE_PLANS`, `Personal Details Emergency→PATIENTS`, `parent_chunk_business_glossary.md_1`, `parent_chunk_business_glossary.md_2`, `parent_chunk_business_glossary.md_0`, `parent_chunk_data_dictionary.md_3`

---

### ✅ Q008 — How are patient appointments scheduled and tracked?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0000 | **Gate:** `proceed`

**Expected answer:**
> The appointments table stores patient_id, provider_id, department_id, appointment_date, appointment_time, appointment_type (new_patient, established, consultation, follow_up, procedure, telehealth), duration_minutes, and appointment_status. Status workflow: scheduled → confirmed → checked_in → in_pr…

**System answer:**
> 

**Sources retrieved (12):** `Patient Appointment→APPOINTMENTS`, `Treatment Record→TREATMENTS`, `Medication Administration To→MEDICATIONS`, `Personal Details Emergency→PATIENTS`, `parent_chunk_data_dictionary.md_10`, `Additional Diagnosis That→DIAGNOSES`, `Claim Scrubbing→CLAIMS`, `Patient Appointment`

---

### ✅ Q009 — What information is captured in laboratory test results?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0000 | **Gate:** `proceed`

**Expected answer:**
> Lab results are stored in the lab_results table with test_name, LOINC code (Logical Observation Identifiers Names and Codes), test_value, unit of measurement, reference_range, is_abnormal flag, ordering_provider_id, result_date, and notes. The is_abnormal flag is automatically set when results fall …

**System answer:**
> 

**Sources retrieved (12):** `Laboratory Test Results→LAB_RESULTS`, `Additional Diagnosis That→DIAGNOSES`, `Laboratory Test Results`, `parent_chunk_business_glossary.md_0`, `parent_chunk_data_dictionary.md_7`, `Additional Diagnosis That`, `Treatment Record→TREATMENTS`, `Personal Details Emergency→PATIENTS`

---

### ✅ Q010 — How are medical treatments and procedures documented?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0000 | **Gate:** `proceed`

**Expected answer:**
> The treatments table stores patient_id, diagnosis_id (for clinical justification), treatment_name, CPT code (for billing), provider_id, department_id, treatment_date, treatment_status (scheduled, completed, canceled, in_progress), and clinical notes. Treatments link to both providers and departments…

**System answer:**
> 

**Sources retrieved (12):** `Treatment Record→TREATMENTS`, `Medication Administration To→MEDICATIONS`, `Healthcare Providers For→PROVIDERS`, `Treatment Record`, `parent_chunk_data_dictionary.md_5`, `parent_chunk_business_glossary.md_1`, `parent_chunk_business_glossary.md_2`, `Additional Diagnosis That→DIAGNOSES`

---

### ✅ Q011 — What are all the diagnoses for a specific patient, including the providers who diagnosed them?

**Status:** GROUNDED  
**GT Coverage:** 50% | **Top Score:** 0.0000 | **Gate:** `proceed`

**Expected answer:**
> To get all diagnoses for a patient with provider information, join the patients table to diagnoses on patient_id, then left join to providers on provider_id. The query returns icd_10_code, diagnosis_name, diagnosis_type, diagnosis_date, resolution_date, and the provider's name (first_name, last_name…

**System answer:**
> 

**Sources retrieved (12):** `Treatment Record→TREATMENTS`, `Additional Diagnosis That→DIAGNOSES`, `parent_chunk_data_dictionary.md_10`, `Laboratory Test Results→LAB_RESULTS`, `parent_chunk_data_dictionary.md_11`, `Medication Administration To→MEDICATIONS`, `Healthcare Providers For→PROVIDERS`, `Claim Scrubbing→CLAIMS`

---

### ✅ Q012 — Which patients have received treatments from cardiology department providers?

**Status:** GROUNDED  
**GT Coverage:** 62% | **Top Score:** 0.0000 | **Gate:** `proceed`

**Expected answer:**
> Join patients to treatments on patient_id, treatments to providers on provider_id, and providers to departments on department_id. Filter where department_name = 'Cardiology' (or department_code). Return patient MRN, name, treatment_name, treatment_date, and provider name. Exclude soft-deleted record…

**System answer:**
> 

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_10`, `Treatment Record→TREATMENTS`, `Healthcare Providers For→PROVIDERS`, `Medication Administration To→MEDICATIONS`, `Patient Appointment→APPOINTMENTS`, `Laboratory Test Results→LAB_RESULTS`, `Personal Details Emergency→PATIENTS`, `parent_chunk_data_dictionary.md_8`

---

### ✅ Q013 — What treatments have been performed for a patient's specific diagnosis?

**Status:** GROUNDED  
**GT Coverage:** 83% | **Top Score:** 0.0000 | **Gate:** `proceed`

**Expected answer:**
> Join diagnoses to treatments on diagnosis_id, then treatments to patients on patient_id and providers on provider_id. Filter by patient_id and specific icd_10_code. Return treatment_name, CPT code, treatment_date, treatment_status, department_name, and provider name. This links clinical conditions t…

**System answer:**
> 

**Sources retrieved (12):** `Treatment Record→TREATMENTS`, `Additional Diagnosis That→DIAGNOSES`, `Medication Administration To→MEDICATIONS`, `parent_chunk_data_dictionary.md_10`, `Laboratory Test Results→LAB_RESULTS`, `Claim Scrubbing→CLAIMS`, `parent_chunk_business_glossary.md_0`, `Treatment Record`

---

### ✅ Q014 — Which providers have prescribed medications to patients with a specific diagnosis?

**Status:** GROUNDED  
**GT Coverage:** 83% | **Top Score:** 0.0000 | **Gate:** `proceed`

**Expected answer:**
> Join diagnoses to patients on patient_id, patients to medications on patient_id, and medications to providers on prescribing_provider_id. Filter by specific icd_10_code. Return provider name, NPI, specialty, patient name, medication_name, dosage, and prescription dates. This supports medication patt…

**System answer:**
> 

**Sources retrieved (12):** `Treatment Record→TREATMENTS`, `Additional Diagnosis That→DIAGNOSES`, `Medication Administration To→MEDICATIONS`, `parent_chunk_data_dictionary.md_10`, `Healthcare Providers For→PROVIDERS`, `Laboratory Test Results→LAB_RESULTS`, `parent_chunk_business_glossary.md_0`, `parent_chunk_business_glossary.md_1`

---

### ✅ Q015 — What is the complete medication history for a patient including prescribing providers?

**Status:** GROUNDED  
**GT Coverage:** 67% | **Top Score:** 0.0000 | **Gate:** `proceed`

**Expected answer:**
> Join patients to medications on patient_id, then medications to providers on prescribing_provider_id. Filter by patient_id. Return medication_name, NDC code, dosage, route, frequency, start_date, end_date, and provider name. Include historical records (valid_to IS NOT NULL) to show medication change…

**System answer:**
> 

**Sources retrieved (12):** `Medication Administration To→MEDICATIONS`, `Treatment Record→TREATMENTS`, `Laboratory Test Results→LAB_RESULTS`, `parent_chunk_data_dictionary.md_10`, `Personal Details Emergency→PATIENTS`, `Additional Diagnosis That→DIAGNOSES`, `Patient Appointment→APPOINTMENTS`, `parent_chunk_business_glossary.md_0`

---

### ✅ Q016 — Which departments have the highest volume of patient appointments?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0000 | **Gate:** `proceed`

**Expected answer:**
> Join appointments to departments on department_id and patients on patient_id. Group by department_id, department_name, and service_line. Count appointments and optionally filter by appointment_date range. Order by count DESC to identify high-volume departments. Exclude canceled and no-show appointme…

**System answer:**
> 

**Sources retrieved (12):** `Patient Appointment→APPOINTMENTS`, `Department→DEPARTMENTS`, `Treatment Record→TREATMENTS`, `parent_chunk_data_dictionary.md_10`, `Medication Administration To→MEDICATIONS`, `Personal Details Emergency→PATIENTS`, `parent_chunk_business_glossary.md_1`, `parent_chunk_data_dictionary.md_9`

---

### ✅ Q017 — What claims have been submitted for a specific patient's treatments?

**Status:** GROUNDED  
**GT Coverage:** 67% | **Top Score:** 0.0000 | **Gate:** `proceed`

**Expected answer:**
> Join patients to treatments on patient_id, treatments to claims on patient_id and service_date ≈ treatment_date, and claims to insurance_plans on insurance_plan_id. Filter by patient_id. Return claim_number, service_date, CPT code, ICD-10 code, amount_charged, amount_paid, claim_status, payer_name, …

**System answer:**
> 

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_10`, `Claim Scrubbing→CLAIMS`, `Treatment Record→TREATMENTS`, `Medication Administration To→MEDICATIONS`, `Personal Details Emergency→PATIENTS`, `Patient Appointment→APPOINTMENTS`, `Laboratory Test Results→LAB_RESULTS`, `parent_chunk_business_glossary.md_1`

---

### ✅ Q018 — Which providers in a specific department have ordered abnormal lab results?

**Status:** GROUNDED  
**GT Coverage:** 83% | **Top Score:** 0.0000 | **Gate:** `proceed`

**Expected answer:**
> Join lab_results to providers on ordering_provider_id, providers to departments on department_id. Filter by department_id and is_abnormal = TRUE. Return provider name, NPI, specialty, patient name, test_name, test_value, reference_range, and result_date. Order by result_date DESC. This identifies pr…

**System answer:**
> 

**Sources retrieved (12):** `Laboratory Test Results→LAB_RESULTS`, `Department→DEPARTMENTS`, `Healthcare Providers For→PROVIDERS`, `Additional Diagnosis That→DIAGNOSES`, `Treatment Record→TREATMENTS`, `Patient Appointment→APPOINTMENTS`, `parent_chunk_data_dictionary.md_10`, `parent_chunk_data_dictionary.md_7`

---

### ✅ Q019 — What is a patient's complete care journey including diagnoses, treatments, and medications?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0000 | **Gate:** `proceed`

**Expected answer:**
> Perform multiple joins from patients: to diagnoses (patient_id), to treatments (patient_id), to medications (patient_id), to lab_results (patient_id), and to appointments (patient_id). Include provider joins for clinical context. Group by clinical event date (diagnosis_date, treatment_date, start_da…

**System answer:**
> 

**Sources retrieved (12):** `Treatment Record→TREATMENTS`, `Medication Administration To→MEDICATIONS`, `Additional Diagnosis That→DIAGNOSES`, `Healthcare Providers For→PROVIDERS`, `Personal Details Emergency→PATIENTS`, `Patient Appointment→APPOINTMENTS`, `parent_chunk_business_glossary.md_0`, `parent_chunk_business_glossary.md_1`

---

### ✅ Q020 — Which insurance plans have the highest claim denial rates?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0000 | **Gate:** `proceed`

**Expected answer:**
> Join claims to insurance_plans on insurance_plan_id. Group by plan_id, payer_name, and plan_type. Count total claims and count claims where claim_status = 'denied'. Calculate denial rate as (denied_claims / total_claims) * 100. Order by denial rate DESC. Filter by service_date range for current peri…

**System answer:**
> 

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_10`, `Claim Scrubbing→CLAIMS`, `parent_chunk_data_dictionary.md_11`, `Insurance Plan→INSURANCE_PLANS`, `Personal Details Emergency→PATIENTS`, `parent_chunk_business_glossary.md_1`, `parent_chunk_business_glossary.md_2`, `parent_chunk_data_dictionary.md_3`

---

### ✅ Q021 — What were a patient's diagnoses in a specific past time period?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0000 | **Gate:** `proceed`

**Expected answer:**
> Query the diagnoses table filtered by patient_id and date range (diagnosis_date >= start_date AND diagnosis_date <= end_date). Additionally check temporal validity: valid_from <= query_date AND (valid_to IS NULL OR valid_to > query_date). Return icd_10_code, diagnosis_name, diagnosis_type, provider …

**System answer:**
> 

**Sources retrieved (12):** `Treatment Record→TREATMENTS`, `parent_chunk_data_dictionary.md_10`, `Additional Diagnosis That→DIAGNOSES`, `Laboratory Test Results→LAB_RESULTS`, `Claim Scrubbing→CLAIMS`, `Personal Details Emergency→PATIENTS`, `Medication Administration To→MEDICATIONS`, `parent_chunk_business_glossary.md_0`

---

### ✅ Q022 — How have a patient's medications changed over time?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0000 | **Gate:** `proceed`

**Expected answer:**
> Query medications table for patient_id including historical records (ignore is_deleted and valid_to filters). Return medication_name, dosage, start_date, end_date, valid_from, valid_to. Order by start_date DESC, valid_from DESC. Changes appear as new records with end_date on the old record and start…

**System answer:**
> 

**Sources retrieved (12):** `Medication Administration To→MEDICATIONS`, `Treatment Record→TREATMENTS`, `parent_chunk_data_dictionary.md_10`, `Additional Diagnosis That→DIAGNOSES`, `parent_chunk_data_dictionary.md_11`, `Laboratory Test Results→LAB_RESULTS`, `Personal Details Emergency→PATIENTS`, `Patient Appointment→APPOINTMENTS`

---

### ✅ Q023 — What was a provider's department affiliation at a specific past date?

**Status:** GROUNDED  
**GT Coverage:** 75% | **Top Score:** 0.0000 | **Gate:** `proceed`

**Expected answer:**
> Query providers table joined to departments on department_id. Filter by provider_id and check temporal validity: valid_from <= historical_date AND (valid_to IS NULL OR valid_to > historical_date). Return provider name, department_name, department_code, and service_line. This reconstructs organizatio…

**System answer:**
> 

**Sources retrieved (12):** `Healthcare Providers For→PROVIDERS`, `Treatment Record→TREATMENTS`, `Patient Appointment→APPOINTMENTS`, `Department→DEPARTMENTS`, `parent_chunk_data_dictionary.md_10`, `Medication Administration To→MEDICATIONS`, `Additional Diagnosis That→DIAGNOSES`, `parent_chunk_data_dictionary.md_8`

---

### ✅ Q024 — Show all changes to a patient's primary insurance coverage over time.

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0000 | **Gate:** `proceed`

**Expected answer:**
> Query patients table joined to insurance_plans on primary_insurance_id. Include historical records by not filtering on valid_to. Return mrn, patient name, plan_name, payer_name, plan_type, valid_from, valid_to. Order by valid_from DESC. Insurance changes appear as new patient records with updated pr…

**System answer:**
> 

**Sources retrieved (12):** `Personal Details Emergency→PATIENTS`, `parent_chunk_data_dictionary.md_11`, `parent_chunk_data_dictionary.md_10`, `Claim Scrubbing→CLAIMS`, `Insurance Plan→INSURANCE_PLANS`, `Treatment Record→TREATMENTS`, `Patient Appointment→APPOINTMENTS`, `parent_chunk_data_dictionary.md_3`

---

### ✅ Q025 — What diagnoses were resolved within a specific time period?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0000 | **Gate:** `proceed`

**Expected answer:**
> Query diagnoses table where resolution_date IS NOT NULL and resolution_date falls within the date range. Include patient_id, icd_10_code, diagnosis_name, diagnosis_date, resolution_date, and provider. Join to patients for names. Filter for current records (is_deleted = FALSE, valid_to IS NULL). This…

**System answer:**
> 

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_10`, `Additional Diagnosis That→DIAGNOSES`, `Treatment Record→TREATMENTS`, `Claim Scrubbing→CLAIMS`, `parent_chunk_data_dictionary.md_4`, `parent_chunk_business_glossary.md_0`, `parent_chunk_data_dictionary.md_5`, `parent_chunk_data_dictionary.md_8`

---

### ✅ Q026 — Reconstruct a patient's active medications as of a specific historical date.

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0000 | **Gate:** `proceed`

**Expected answer:**
> Query medications for patient_id where: (1) start_date <= historical_date AND (end_date IS NULL OR end_date > historical_date) for medication active period, AND (2) valid_from <= historical_date AND (valid_to IS NULL OR valid_to > historical_date) for record validity. Return medication_name, dosage,…

**System answer:**
> 

**Sources retrieved (12):** `Medication Administration To→MEDICATIONS`, `parent_chunk_data_dictionary.md_11`, `Treatment Record→TREATMENTS`, `parent_chunk_data_dictionary.md_10`, `Additional Diagnosis That→DIAGNOSES`, `Laboratory Test Results→LAB_RESULTS`, `Personal Details Emergency→PATIENTS`, `Patient Appointment→APPOINTMENTS`

---

### ✅ Q027 — Count the number of patients per department without exposing individual patient identities.

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0000 | **Gate:** `proceed`

**Expected answer:**
> Join appointments to departments on department_id. Group by department_id, department_name, service_line. Count DISTINCT patient_id for privacy (prevents counting multiple appointments per patient). Filter by appointment_date range and exclude canceled/no-show status. Return aggregated counts only—n…

**System answer:**
> 

**Sources retrieved (12):** `Department→DEPARTMENTS`, `Patient Appointment→APPOINTMENTS`, `Healthcare Providers For→PROVIDERS`, `Personal Details Emergency→PATIENTS`, `Treatment Record→TREATMENTS`, `parent_chunk_data_dictionary.md_10`, `Medication Administration To→MEDICATIONS`, `parent_chunk_data_dictionary.md_3`

---

### ✅ Q028 — What are the most common diagnoses (by count) without linking to specific patients?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0000 | **Gate:** `proceed`

**Expected answer:**
> Query diagnoses table grouped by icd_10_code and diagnosis_name. COUNT(*) each diagnosis. Order by count DESC. Return only icd_10_code, diagnosis_name, and count—no patient identifiers, MRNs, or names. Optionally filter by diagnosis_date range. This epidemiological analysis follows HIPAA de-identifi…

**System answer:**
> 

**Sources retrieved (12):** `Claim Scrubbing→CLAIMS`, `parent_chunk_data_dictionary.md_10`, `Additional Diagnosis That→DIAGNOSES`, `Treatment Record→TREATMENTS`, `Laboratory Test Results→LAB_RESULTS`, `Personal Details Emergency→PATIENTS`, `parent_chunk_business_glossary.md_0`, `parent_chunk_data_dictionary.md_4`

---

### ✅ Q029 — Which providers have the highest patient volume without exposing patient information?

**Status:** GROUNDED  
**GT Coverage:** 83% | **Top Score:** 0.0000 | **Gate:** `proceed`

**Expected answer:**
> Join appointments to providers on provider_id. Group by provider_id, provider name, NPI, specialty, department. COUNT DISTINCT patient_id for unique patient count (not appointment count). Filter by appointment_date range and completed status. Return only provider information and aggregated counts—no…

**System answer:**
> 

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_10`, `Personal Details Emergency→PATIENTS`, `Healthcare Providers For→PROVIDERS`, `Treatment Record→TREATMENTS`, `Patient Appointment→APPOINTMENTS`, `Claim Scrubbing→CLAIMS`, `Laboratory Test Results→LAB_RESULTS`, `parent_chunk_business_glossary.md_0`

---

### ✅ Q030 — What is the average claim payment amount by insurance plan type?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0000 | **Gate:** `proceed`

**Expected answer:**
> Join claims to insurance_plans on insurance_plan_id. Group by plan_type (commercial, medicare, medicaid, tricare, self_pay). Calculate AVG(amount_paid) and AVG(amount_charged). Filter by service_date range and claim_status = 'approved' or 'partially_paid'. Return only plan_type and aggregated averag…

**System answer:**
> 

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_10`, `Claim Scrubbing→CLAIMS`, `Insurance Plan→INSURANCE_PLANS`, `parent_chunk_data_dictionary.md_11`, `Personal Details Emergency→PATIENTS`, `Healthcare Providers For→PROVIDERS`, `parent_chunk_business_glossary.md_1`, `parent_chunk_data_dictionary.md_3`

---

## Anomalies & Observations

No anomalies detected. All questions grounded with acceptable RAGAS scores.
