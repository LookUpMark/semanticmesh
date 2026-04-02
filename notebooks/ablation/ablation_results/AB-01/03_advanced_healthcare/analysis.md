# AB-01 — 03_advanced_healthcare — Run Analysis

**Timestamp:** 2026-03-30 22:18:24  
**Run tag:** `v5`

## Configuration

| Parameter | Value |
|-----------|-------|
| Extraction model | `LLM (gpt-5.4-nano-2026-03-17)` |
| Reasoning model | `gpt-5.4-2026-03-05` |
| Embedding model | `BAAI/bge-m3` |
| Retrieval mode | `vector` |
| Reranker | `True` |
| Reranker top_k | `12` |
| Chunk size / overlap | `256 / 32` |
| ER similarity threshold | `0.75` |

## Builder Results

Builder skipped (`--no-builder`).

## Query Evaluation Summary

| Metric | Value |
|--------|-------|
| Questions | 30 |
| Grounded | **30/30 (100%)** |
| Avg GT Coverage | 100% |
| Avg Top Score | 0.1477 |
| Avg Chunk Count | 4.0 |
| Abstained | 0 |

## RAGAS Metrics

RAGAS evaluation not enabled for this run.

## Per-Question Deep Dive

### ✅ Q001 — What tables store information about patients?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.8783 | **Gate:** `proceed`

**Expected answer:**
> The patients table stores demographic and administrative information including MRN, name, date of birth, gender, contact details, and emergency contacts. Additionally, patient-related data is stored in diagnoses, treatments, medications, lab_results, appointments, and claims tables through foreign k…

**System answer:**
> From the retrieved context, the tables that store patient-related information are the Laboratory Test Result table, the Patient Appointment table, and the CLAIMS table.

The Laboratory Test Result table stores patient-linked diagnostic lab results, including test name, LOINC code, value, units, reference range, abnormal flag, and result date.

The Patient Appointment table stores patient appointme…

**Sources retrieved (4):** `Laboratory Test Result`, `Medical Treatment`, `Insurance Claim`, `Patient Appointment`

**Context previews (first 3):**

1. _Laboratory Test Result: The table stores patient-linked test outcomes with fields for test name, LOINC code, value, units, reference range, abnormal flag, and result date, which directly matches diagn…_

2. _Medical Treatment: Medical treatments and procedures performed on patients.…_

3. _Insurance Claim: The table is explicitly labeled as CLAIMS and its columns capture claim identifiers, patient and insurance plan references, billing amounts, claim status, and denial reasons. This ali…_

---

### ✅ Q002 — How are medical diagnoses coded and classified?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0072 | **Gate:** `proceed_with_warning`

**Expected answer:**
> Diagnoses are stored in the diagnoses table with ICD-10-CM codes (icd_10_code field). They are classified into four types: 'principal' (primary condition), 'comorbidity' (additional conditions), 'admitting' (condition causing admission), and 'secondary'. Each diagnosis includes the diagnosis name, t…

**System answer:**
> I cannot determine how medical diagnoses are coded and classified from the retrieved context.

What is known from the context is that it describes these concepts: CLAIMS for insurance claims and billing information, a laboratory test result table with fields such as test name and LOINC code, Medical Treatment for treatments and procedures, and Patient Appointment for scheduling and encounter infor…

**Sources retrieved (4):** `Insurance Claim`, `Laboratory Test Result`, `Medical Treatment`, `Patient Appointment`

**Context previews (first 3):**

1. _Insurance Claim: The table is explicitly labeled as CLAIMS and its columns capture claim identifiers, patient and insurance plan references, billing amounts, claim status, and denial reasons. This ali…_

2. _Laboratory Test Result: The table stores patient-linked test outcomes with fields for test name, LOINC code, value, units, reference range, abnormal flag, and result date, which directly matches diagn…_

3. _Medical Treatment: Medical treatments and procedures performed on patients.…_

---

### ✅ Q003 — What information is tracked for medications prescribed to patients?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0226 | **Gate:** `proceed_with_warning`

**Expected answer:**
> The medications table tracks medication name, National Drug Code (NDC), dosage, route of administration (oral, IV, IM, topical, inhaled, subcutaneous), frequency, prescribing provider, start date, and end date. Active medications have a NULL end_date. The table uses temporal historization with valid…

**System answer:**
> The retrieved context does not provide enough information to say what information is tracked for medications prescribed to patients.

What is known from the context is that it includes:
Insurance Claim, which tracks claim identifiers, patient and insurance plan references, billing amounts, claim status, and denial reasons;
Patient Appointment, which tracks appointment scheduling and encounter deta…

**Sources retrieved (4):** `Insurance Claim`, `Patient Appointment`, `Medical Treatment`, `Laboratory Test Result`

**Context previews (first 3):**

1. _Insurance Claim: The table is explicitly labeled as CLAIMS and its columns capture claim identifiers, patient and insurance plan references, billing amounts, claim status, and denial reasons. This ali…_

2. _Patient Appointment: The table is explicitly documented as storing patient appointment scheduling and encounter information, and its columns capture appointment date/time, patient, provider, departmen…_

3. _Medical Treatment: Medical treatments and procedures performed on patients.…_

---

### ✅ Q004 — How are healthcare providers organized and tracked?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0020 | **Gate:** `proceed_with_warning`

**Expected answer:**
> Providers are stored in the providers table with a unique National Provider Identifier (NPI), name, provider type (MD, DO, NP, PA, RN, PT, Other), specialty, and department affiliation. Providers have is_active and is_deleted flags for status tracking. The table uses temporal historization to track …

**System answer:**
> From the retrieved context, healthcare providers are only tracked in the `Patient Appointment` concept. That table stores appointment scheduling and encounter information and includes columns for `provider` and `department`, along with appointment date/time, patient, type, duration, status, and cancellation reason.

The context therefore supports only this: a provider is recorded on each patient a…

**Sources retrieved (4):** `Insurance Claim`, `Patient Appointment`, `Medical Treatment`, `Laboratory Test Result`

**Context previews (first 3):**

1. _Insurance Claim: The table is explicitly labeled as CLAIMS and its columns capture claim identifiers, patient and insurance plan references, billing amounts, claim status, and denial reasons. This ali…_

2. _Patient Appointment: The table is explicitly documented as storing patient appointment scheduling and encounter information, and its columns capture appointment date/time, patient, provider, departmen…_

3. _Medical Treatment: Medical treatments and procedures performed on patients.…_

---

### ✅ Q005 — What is the structure of departments and how do they relate to each other?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0016 | **Gate:** `proceed_with_warning`

**Expected answer:**
> Departments are stored in the departments table with department_name, department_code, parent_department_id (self-referential foreign key for hierarchy), service_line (strategic grouping), and location. Departments can have parent departments creating a hierarchical structure (e.g., Cardiology as a …

**System answer:**
> I cannot determine the structure of departments or how departments relate to each other from the retrieved context.

The only department-related information present is in the Patient Appointment concept: the appointment table stores scheduling and encounter information and includes a department reference along with appointment date/time, patient, provider, type, duration, status, and cancellation …

**Sources retrieved (4):** `Insurance Claim`, `Patient Appointment`, `Medical Treatment`, `Laboratory Test Result`

**Context previews (first 3):**

1. _Insurance Claim: The table is explicitly labeled as CLAIMS and its columns capture claim identifiers, patient and insurance plan references, billing amounts, claim status, and denial reasons. This ali…_

2. _Patient Appointment: The table is explicitly documented as storing patient appointment scheduling and encounter information, and its columns capture appointment date/time, patient, provider, departmen…_

3. _Medical Treatment: Medical treatments and procedures performed on patients.…_

---

### ✅ Q006 — How are insurance plans and payers represented in the system?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0222 | **Gate:** `proceed_with_warning`

**Expected answer:**
> The insurance_plans table stores plan_name, payer_name (insurance company), plan_type (commercial, medicare, medicaid, tricare, self_pay), and prior_auth_required flag. Plans have is_active status and use temporal historization. The patients table references insurance_plans via primary_insurance_id …

**System answer:**
> From the retrieved context, insurance plans are represented indirectly through the CLAIMS table: the Insurance Claim concept says CLAIMS stores claim identifiers, patient references, insurance plan references, billing amounts, claim status, and denial reasons. That means the system includes an insurance plan reference as part of each claim record.

The context does not describe a separate insuranc…

**Sources retrieved (4):** `Insurance Claim`, `Patient Appointment`, `Medical Treatment`, `Laboratory Test Result`

**Context previews (first 3):**

1. _Insurance Claim: The table is explicitly labeled as CLAIMS and its columns capture claim identifiers, patient and insurance plan references, billing amounts, claim status, and denial reasons. This ali…_

2. _Patient Appointment: The table is explicitly documented as storing patient appointment scheduling and encounter information, and its columns capture appointment date/time, patient, provider, departmen…_

3. _Medical Treatment: Medical treatments and procedures performed on patients.…_

---

### ✅ Q007 — What constitutes an insurance claim and what is its lifecycle?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0650 | **Gate:** `proceed_with_warning`

**Expected answer:**
> Claims are stored in the claims table with claim_number (unique identifier), patient_id, insurance_plan_id, service_date, submission_date, CPT code (procedure), ICD-10 code (diagnosis), amounts (charged, allowed, paid), and claim_status. Status workflow includes: submitted → pending → approved/denie…

**System answer:**
> An insurance claim, based on the retrieved context, is represented by the CLAIMS table and consists of claim identifiers, references to the patient and insurance plan, billing amounts, claim status, and denial reasons. The context also states that this aligns with storing insurance claims and billing information for services rendered.

The lifecycle of an insurance claim is not described in the re…

**Sources retrieved (4):** `Insurance Claim`, `Medical Treatment`, `Patient Appointment`, `Laboratory Test Result`

**Context previews (first 3):**

1. _Insurance Claim: The table is explicitly labeled as CLAIMS and its columns capture claim identifiers, patient and insurance plan references, billing amounts, claim status, and denial reasons. This ali…_

2. _Medical Treatment: Medical treatments and procedures performed on patients.…_

3. _Patient Appointment: The table is explicitly documented as storing patient appointment scheduling and encounter information, and its columns capture appointment date/time, patient, provider, departmen…_

---

### ✅ Q008 — How are patient appointments scheduled and tracked?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.9189 | **Gate:** `proceed`

**Expected answer:**
> The appointments table stores patient_id, provider_id, department_id, appointment_date, appointment_time, appointment_type (new_patient, established, consultation, follow_up, procedure, telehealth), duration_minutes, and appointment_status. Status workflow: scheduled → confirmed → checked_in → in_pr…

**System answer:**
> Patient appointments are scheduled and tracked through the Patient Appointment table, which is documented as storing patient appointment scheduling and encounter information.

From the available context, scheduling is represented by the appointment date/time and by linking the appointment to the patient, provider, and department. Tracking is represented through the appointment’s type, duration, st…

**Sources retrieved (4):** `Insurance Claim`, `Patient Appointment`, `Medical Treatment`, `Laboratory Test Result`

**Context previews (first 3):**

1. _Insurance Claim: The table is explicitly labeled as CLAIMS and its columns capture claim identifiers, patient and insurance plan references, billing amounts, claim status, and denial reasons. This ali…_

2. _Patient Appointment: The table is explicitly documented as storing patient appointment scheduling and encounter information, and its columns capture appointment date/time, patient, provider, departmen…_

3. _Medical Treatment: Medical treatments and procedures performed on patients.…_

---

### ✅ Q009 — What information is captured in laboratory test results?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.8784 | **Gate:** `proceed`

**Expected answer:**
> Lab results are stored in the lab_results table with test_name, LOINC code (Logical Observation Identifiers Names and Codes), test_value, unit of measurement, reference_range, is_abnormal flag, ordering_provider_id, result_date, and notes. The is_abnormal flag is automatically set when results fall …

**System answer:**
> Laboratory test results capture patient-linked test outcomes, including the test name, LOINC code, result value, units, reference range, abnormal flag, and result date. The context also states that this table is specifically for laboratory test results for patients.

**Sources retrieved (4):** `Laboratory Test Result`, `Insurance Claim`, `Patient Appointment`, `Medical Treatment`

**Context previews (first 3):**

1. _Laboratory Test Result: The table stores patient-linked test outcomes with fields for test name, LOINC code, value, units, reference range, abnormal flag, and result date, which directly matches diagn…_

2. _Insurance Claim: The table is explicitly labeled as CLAIMS and its columns capture claim identifiers, patient and insurance plan references, billing amounts, claim status, and denial reasons. This ali…_

3. _Patient Appointment: The table is explicitly documented as storing patient appointment scheduling and encounter information, and its columns capture appointment date/time, patient, provider, departmen…_

---

### ✅ Q010 — How are medical treatments and procedures documented?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.5231 | **Gate:** `proceed`

**Expected answer:**
> The treatments table stores patient_id, diagnosis_id (for clinical justification), treatment_name, CPT code (for billing), provider_id, department_id, treatment_date, treatment_status (scheduled, completed, canceled, in_progress), and clinical notes. Treatments link to both providers and departments…

**System answer:**
> The retrieved context only identifies the business concept Medical Treatment as “medical treatments and procedures performed on patients.”

It does not provide any table name, column definitions, or documentation details showing how those treatments and procedures are recorded in the schema. So from the available context, I can only say that medical treatments and procedures are represented as the…

**Sources retrieved (4):** `Insurance Claim`, `Medical Treatment`, `Patient Appointment`, `Laboratory Test Result`

**Context previews (first 3):**

1. _Insurance Claim: The table is explicitly labeled as CLAIMS and its columns capture claim identifiers, patient and insurance plan references, billing amounts, claim status, and denial reasons. This ali…_

2. _Medical Treatment: Medical treatments and procedures performed on patients.…_

3. _Patient Appointment: The table is explicitly documented as storing patient appointment scheduling and encounter information, and its columns capture appointment date/time, patient, provider, departmen…_

---

### ✅ Q011 — What are all the diagnoses for a specific patient, including the providers who diagnosed them?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0034 | **Gate:** `proceed_with_warning`

**Expected answer:**
> To get all diagnoses for a patient with provider information, join the patients table to diagnoses on patient_id, then left join to providers on provider_id. The query returns icd_10_code, diagnosis_name, diagnosis_type, diagnosis_date, resolution_date, and the provider's name (first_name, last_name…

**System answer:**
> I cannot answer this from the retrieved context because it does not include any diagnosis table, diagnosis concept, or schema describing how diagnoses are stored.

The available context only mentions these schema-level concepts:
Insurance Claim via CLAIMS, which stores claim identifiers, patient and insurance plan references, billing amounts, claim status, and denial reasons.
Laboratory Test Resul…

**Sources retrieved (4):** `Insurance Claim`, `Laboratory Test Result`, `Medical Treatment`, `Patient Appointment`

**Context previews (first 3):**

1. _Insurance Claim: The table is explicitly labeled as CLAIMS and its columns capture claim identifiers, patient and insurance plan references, billing amounts, claim status, and denial reasons. This ali…_

2. _Laboratory Test Result: The table stores patient-linked test outcomes with fields for test name, LOINC code, value, units, reference range, abnormal flag, and result date, which directly matches diagn…_

3. _Medical Treatment: Medical treatments and procedures performed on patients.…_

---

### ✅ Q012 — Which patients have received treatments from cardiology department providers?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0008 | **Gate:** `proceed_with_warning`

**Expected answer:**
> Join patients to treatments on patient_id, treatments to providers on provider_id, and providers to departments on department_id. Filter where department_name = 'Cardiology' (or department_code). Return patient MRN, name, treatment_name, treatment_date, and provider name. Exclude soft-deleted record…

**System answer:**
> The retrieved context does not contain enough information to determine which specific patients have received treatments from cardiology department providers.

What is known from the context is only high-level metadata:
The knowledge graph includes a business concept for Medical Treatment, described as medical treatments and procedures performed on patients. It also includes a Patient Appointment c…

**Sources retrieved (4):** `Medical Treatment`, `Patient Appointment`, `Laboratory Test Result`, `Insurance Claim`

**Context previews (first 3):**

1. _Medical Treatment: Medical treatments and procedures performed on patients.…_

2. _Patient Appointment: The table is explicitly documented as storing patient appointment scheduling and encounter information, and its columns capture appointment date/time, patient, provider, departmen…_

3. _Laboratory Test Result: The table stores patient-linked test outcomes with fields for test name, LOINC code, value, units, reference range, abnormal flag, and result date, which directly matches diagn…_

---

### ✅ Q013 — What treatments have been performed for a patient's specific diagnosis?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.9073 | **Gate:** `proceed`

**Expected answer:**
> Join diagnoses to treatments on diagnosis_id, then treatments to patients on patient_id and providers on provider_id. Filter by patient_id and specific icd_10_code. Return treatment_name, CPT code, treatment_date, treatment_status, department_name, and provider name. This links clinical conditions t…

**System answer:**
> From the provided context, I can only say that the relevant business concept is Medical Treatment, described as “medical treatments and procedures performed on patients.”

The context does not provide a table definition, columns, or relationships for Medical Treatment, and it does not show any link between treatments and a patient’s specific diagnosis. It also does not contain patient-level record…

**Sources retrieved (4):** `Insurance Claim`, `Medical Treatment`, `Laboratory Test Result`, `Patient Appointment`

**Context previews (first 3):**

1. _Insurance Claim: The table is explicitly labeled as CLAIMS and its columns capture claim identifiers, patient and insurance plan references, billing amounts, claim status, and denial reasons. This ali…_

2. _Medical Treatment: Medical treatments and procedures performed on patients.…_

3. _Laboratory Test Result: The table stores patient-linked test outcomes with fields for test name, LOINC code, value, units, reference range, abnormal flag, and result date, which directly matches diagn…_

---

### ✅ Q014 — Which providers have prescribed medications to patients with a specific diagnosis?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0117 | **Gate:** `proceed_with_warning`

**Expected answer:**
> Join diagnoses to patients on patient_id, patients to medications on patient_id, and medications to providers on prescribing_provider_id. Filter by specific icd_10_code. Return provider name, NPI, specialty, patient name, medication_name, dosage, and prescription dates. This supports medication patt…

**System answer:**
> From the retrieved context, this cannot be determined.

What is known is limited to high-level concepts: "Patient Appointment" includes patient, provider, department, appointment type, status, and related scheduling fields; "Medical Treatment" is described only as medical treatments and procedures performed on patients; "Laboratory Test Result" stores patient-linked lab outcomes; and "Insurance Cl…

**Sources retrieved (4):** `Medical Treatment`, `Laboratory Test Result`, `Insurance Claim`, `Patient Appointment`

**Context previews (first 3):**

1. _Medical Treatment: Medical treatments and procedures performed on patients.…_

2. _Laboratory Test Result: The table stores patient-linked test outcomes with fields for test name, LOINC code, value, units, reference range, abnormal flag, and result date, which directly matches diagn…_

3. _Insurance Claim: The table is explicitly labeled as CLAIMS and its columns capture claim identifiers, patient and insurance plan references, billing amounts, claim status, and denial reasons. This ali…_

---

### ✅ Q015 — What is the complete medication history for a patient including prescribing providers?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0045 | **Gate:** `proceed_with_warning`

**Expected answer:**
> Join patients to medications on patient_id, then medications to providers on prescribing_provider_id. Filter by patient_id. Return medication_name, NDC code, dosage, route, frequency, start_date, end_date, and provider name. Include historical records (valid_to IS NOT NULL) to show medication change…

**System answer:**
> From the retrieved context, this cannot be determined.

What is known is limited to these concepts: Insurance Claim/CLAIMS, Patient Appointment, Medical Treatment, and Laboratory Test Result. The only provider-related detail in the context is that the Patient Appointment table includes a provider column for appointments. There is no table, column, or concept in the provided context for medications…

**Sources retrieved (4):** `Insurance Claim`, `Patient Appointment`, `Medical Treatment`, `Laboratory Test Result`

**Context previews (first 3):**

1. _Insurance Claim: The table is explicitly labeled as CLAIMS and its columns capture claim identifiers, patient and insurance plan references, billing amounts, claim status, and denial reasons. This ali…_

2. _Patient Appointment: The table is explicitly documented as storing patient appointment scheduling and encounter information, and its columns capture appointment date/time, patient, provider, departmen…_

3. _Medical Treatment: Medical treatments and procedures performed on patients.…_

---

### ✅ Q016 — Which departments have the highest volume of patient appointments?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0221 | **Gate:** `proceed_with_warning`

**Expected answer:**
> Join appointments to departments on department_id and patients on patient_id. Group by department_id, department_name, and service_line. Count appointments and optionally filter by appointment_date range. Order by count DESC to identify high-volume departments. Exclude canceled and no-show appointme…

**System answer:**
> From the retrieved context, this cannot be determined.

What is known is that the Patient Appointment table stores appointment scheduling and encounter information, including a department field along with appointment date/time, patient, provider, type, duration, status, and cancellation reason. That means the schema supports analyzing appointment volume by department.

However, the context provide…

**Sources retrieved (4):** `Insurance Claim`, `Patient Appointment`, `Medical Treatment`, `Laboratory Test Result`

**Context previews (first 3):**

1. _Insurance Claim: The table is explicitly labeled as CLAIMS and its columns capture claim identifiers, patient and insurance plan references, billing amounts, claim status, and denial reasons. This ali…_

2. _Patient Appointment: The table is explicitly documented as storing patient appointment scheduling and encounter information, and its columns capture appointment date/time, patient, provider, departmen…_

3. _Medical Treatment: Medical treatments and procedures performed on patients.…_

---

### ✅ Q017 — What claims have been submitted for a specific patient's treatments?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0502 | **Gate:** `proceed_with_warning`

**Expected answer:**
> Join patients to treatments on patient_id, treatments to claims on patient_id and service_date ≈ treatment_date, and claims to insurance_plans on insurance_plan_id. Filter by patient_id. Return claim_number, service_date, CPT code, ICD-10 code, amount_charged, amount_paid, claim_status, payer_name, …

**System answer:**
> I cannot identify which claims have been submitted for a specific patient’s treatments from the provided context, because the knowledge graph here contains only schema-level business metadata, not actual claim or treatment records.

From the available context, the relevant structure is:

The business concept Insurance Claim maps to a table explicitly labeled CLAIMS. Its columns capture claim ident…

**Sources retrieved (4):** `Insurance Claim`, `Medical Treatment`, `Patient Appointment`, `Laboratory Test Result`

**Context previews (first 3):**

1. _Insurance Claim: The table is explicitly labeled as CLAIMS and its columns capture claim identifiers, patient and insurance plan references, billing amounts, claim status, and denial reasons. This ali…_

2. _Medical Treatment: Medical treatments and procedures performed on patients.…_

3. _Patient Appointment: The table is explicitly documented as storing patient appointment scheduling and encounter information, and its columns capture appointment date/time, patient, provider, departmen…_

---

### ✅ Q018 — Which providers in a specific department have ordered abnormal lab results?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0066 | **Gate:** `proceed_with_warning`

**Expected answer:**
> Join lab_results to providers on ordering_provider_id, providers to departments on department_id. Filter by department_id and is_abnormal = TRUE. Return provider name, NPI, specialty, patient name, test_name, test_value, reference_range, and result_date. Order by result_date DESC. This identifies pr…

**System answer:**
> From the retrieved context, this cannot be determined.

What is known is:
The “Laboratory Test Result” table stores patient-linked lab outcomes and includes test name, LOINC code, value, units, reference range, abnormal flag, and result date.
The “Patient Appointment” table stores appointment and encounter information and includes patient, provider, and department, along with appointment date/time…

**Sources retrieved (4):** `Insurance Claim`, `Laboratory Test Result`, `Patient Appointment`, `Medical Treatment`

**Context previews (first 3):**

1. _Insurance Claim: The table is explicitly labeled as CLAIMS and its columns capture claim identifiers, patient and insurance plan references, billing amounts, claim status, and denial reasons. This ali…_

2. _Laboratory Test Result: The table stores patient-linked test outcomes with fields for test name, LOINC code, value, units, reference range, abnormal flag, and result date, which directly matches diagn…_

3. _Patient Appointment: The table is explicitly documented as storing patient appointment scheduling and encounter information, and its columns capture appointment date/time, patient, provider, departmen…_

---

### ✅ Q019 — What is a patient's complete care journey including diagnoses, treatments, and medications?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0582 | **Gate:** `proceed_with_warning`

**Expected answer:**
> Perform multiple joins from patients: to diagnoses (patient_id), to treatments (patient_id), to medications (patient_id), to lab_results (patient_id), and to appointments (patient_id). Include provider joins for clinical context. Group by clinical event date (diagnosis_date, treatment_date, start_da…

**System answer:**
> The retrieved context is not sufficient to describe a patient’s complete care journey.

What is supported by the context is only a partial, schema-level picture of care-related information. A “Patient Appointment” table/business concept exists and stores appointment scheduling and encounter information, including appointment date/time, patient, provider, department, type, duration, status, and can…

**Sources retrieved (4):** `Insurance Claim`, `Medical Treatment`, `Patient Appointment`, `Laboratory Test Result`

**Context previews (first 3):**

1. _Insurance Claim: The table is explicitly labeled as CLAIMS and its columns capture claim identifiers, patient and insurance plan references, billing amounts, claim status, and denial reasons. This ali…_

2. _Medical Treatment: Medical treatments and procedures performed on patients.…_

3. _Patient Appointment: The table is explicitly documented as storing patient appointment scheduling and encounter information, and its columns capture appointment date/time, patient, provider, departmen…_

---

### ✅ Q020 — Which insurance plans have the highest claim denial rates?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0152 | **Gate:** `proceed_with_warning`

**Expected answer:**
> Join claims to insurance_plans on insurance_plan_id. Group by plan_id, payer_name, and plan_type. Count total claims and count claims where claim_status = 'denied'. Calculate denial rate as (denied_claims / total_claims) * 100. Order by denial rate DESC. Filter by service_date range for current peri…

**System answer:**
> I cannot determine which insurance plans have the highest claim denial rates from the provided context, because it contains only schema-level metadata, not actual claim records.

What the context does show is that the CLAIMS table stores the fields needed to answer this operationally: claim identifiers, patient and insurance plan references, billing amounts, claim status, and denial reasons. Based…

**Sources retrieved (4):** `Insurance Claim`, `Medical Treatment`, `Patient Appointment`, `Laboratory Test Result`

**Context previews (first 3):**

1. _Insurance Claim: The table is explicitly labeled as CLAIMS and its columns capture claim identifiers, patient and insurance plan references, billing amounts, claim status, and denial reasons. This ali…_

2. _Medical Treatment: Medical treatments and procedures performed on patients.…_

3. _Patient Appointment: The table is explicitly documented as storing patient appointment scheduling and encounter information, and its columns capture appointment date/time, patient, provider, departmen…_

---

### ✅ Q021 — What were a patient's diagnoses in a specific past time period?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0034 | **Gate:** `proceed_with_warning`

**Expected answer:**
> Query the diagnoses table filtered by patient_id and date range (diagnosis_date >= start_date AND diagnosis_date <= end_date). Additionally check temporal validity: valid_from <= query_date AND (valid_to IS NULL OR valid_to > query_date). Return icd_10_code, diagnosis_name, diagnosis_type, provider …

**System answer:**
> I cannot answer that directly from the retrieved context because it does not include any diagnosis concept, diagnosis table, or diagnosis-related columns.

What the context does show is schema-level metadata for other patient-linked domains: laboratory test results include patient-linked outcomes and a result date; patient appointments include patient, provider, department, appointment date/time, …

**Sources retrieved (4):** `Insurance Claim`, `Laboratory Test Result`, `Patient Appointment`, `Medical Treatment`

**Context previews (first 3):**

1. _Insurance Claim: The table is explicitly labeled as CLAIMS and its columns capture claim identifiers, patient and insurance plan references, billing amounts, claim status, and denial reasons. This ali…_

2. _Laboratory Test Result: The table stores patient-linked test outcomes with fields for test name, LOINC code, value, units, reference range, abnormal flag, and result date, which directly matches diagn…_

3. _Patient Appointment: The table is explicitly documented as storing patient appointment scheduling and encounter information, and its columns capture appointment date/time, patient, provider, departmen…_

---

### ✅ Q022 — How have a patient's medications changed over time?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0007 | **Gate:** `proceed_with_warning`

**Expected answer:**
> Query medications table for patient_id including historical records (ignore is_deleted and valid_to filters). Return medication_name, dosage, start_date, end_date, valid_from, valid_to. Order by start_date DESC, valid_from DESC. Changes appear as new records with end_date on the old record and start…

**System answer:**
> I cannot determine how a patient’s medications changed over time from the retrieved context.

What the context does cover is limited to these schema/business concepts:
Insurance Claim, which stores claim identifiers, patient and insurance plan references, billing amounts, claim status, and denial reasons;
Medical Treatment, described only as medical treatments and procedures performed on patients;…

**Sources retrieved (4):** `Insurance Claim`, `Medical Treatment`, `Patient Appointment`, `Laboratory Test Result`

**Context previews (first 3):**

1. _Insurance Claim: The table is explicitly labeled as CLAIMS and its columns capture claim identifiers, patient and insurance plan references, billing amounts, claim status, and denial reasons. This ali…_

2. _Medical Treatment: Medical treatments and procedures performed on patients.…_

3. _Patient Appointment: The table is explicitly documented as storing patient appointment scheduling and encounter information, and its columns capture appointment date/time, patient, provider, departmen…_

---

### ✅ Q023 — What was a provider's department affiliation at a specific past date?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0015 | **Gate:** `proceed_with_warning`

**Expected answer:**
> Query providers table joined to departments on department_id. Filter by provider_id and check temporal validity: valid_from <= historical_date AND (valid_to IS NULL OR valid_to > historical_date). Return provider name, department_name, department_code, and service_line. This reconstructs organizatio…

**System answer:**
> From the retrieved context, the only relevant source is Patient Appointment. It stores appointment scheduling and encounter information, including appointment date/time, provider, and department.

So, for a specific past date, you could identify the department associated with a provider only through a Patient Appointment record for that date/time, using the provider, appointment date/time, and dep…

**Sources retrieved (4):** `Patient Appointment`, `Laboratory Test Result`, `Insurance Claim`, `Medical Treatment`

**Context previews (first 3):**

1. _Patient Appointment: The table is explicitly documented as storing patient appointment scheduling and encounter information, and its columns capture appointment date/time, patient, provider, departmen…_

2. _Laboratory Test Result: The table stores patient-linked test outcomes with fields for test name, LOINC code, value, units, reference range, abnormal flag, and result date, which directly matches diagn…_

3. _Insurance Claim: The table is explicitly labeled as CLAIMS and its columns capture claim identifiers, patient and insurance plan references, billing amounts, claim status, and denial reasons. This ali…_

---

### ✅ Q024 — Show all changes to a patient's primary insurance coverage over time.

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0052 | **Gate:** `proceed_with_warning`

**Expected answer:**
> Query patients table joined to insurance_plans on primary_insurance_id. Include historical records by not filtering on valid_to. Return mrn, patient name, plan_name, payer_name, plan_type, valid_from, valid_to. Order by valid_from DESC. Insurance changes appear as new patient records with updated pr…

**System answer:**
> I cannot answer this as asked from the retrieved context.

The available context only describes the CLAIMS concept at a high level: it stores claim identifiers, patient and insurance plan references, billing amounts, claim status, and denial reasons. That means the knowledge provided supports insurance claim billing data, not insurance coverage history.

Specifically, the retrieved context does no…

**Sources retrieved (4):** `Insurance Claim`, `Patient Appointment`, `Medical Treatment`, `Laboratory Test Result`

**Context previews (first 3):**

1. _Insurance Claim: The table is explicitly labeled as CLAIMS and its columns capture claim identifiers, patient and insurance plan references, billing amounts, claim status, and denial reasons. This ali…_

2. _Patient Appointment: The table is explicitly documented as storing patient appointment scheduling and encounter information, and its columns capture appointment date/time, patient, provider, departmen…_

3. _Medical Treatment: Medical treatments and procedures performed on patients.…_

---

### ✅ Q025 — What diagnoses were resolved within a specific time period?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0002 | **Gate:** `proceed_with_warning`

**Expected answer:**
> Query diagnoses table where resolution_date IS NOT NULL and resolution_date falls within the date range. Include patient_id, icd_10_code, diagnosis_name, diagnosis_date, resolution_date, and provider. Join to patients for names. Filter for current records (is_deleted = FALSE, valid_to IS NULL). This…

**System answer:**
> From the retrieved context, this cannot be determined.

What is known is that the context includes schema/business-concept metadata for:
Patient Appointment, with appointment date/time, patient, provider, department, type, duration, status, and cancellation reason;
Insurance Claim, with claim identifiers, patient and insurance plan references, billing amounts, claim status, and denial reasons;
Lab…

**Sources retrieved (4):** `Patient Appointment`, `Insurance Claim`, `Laboratory Test Result`, `Medical Treatment`

**Context previews (first 3):**

1. _Patient Appointment: The table is explicitly documented as storing patient appointment scheduling and encounter information, and its columns capture appointment date/time, patient, provider, departmen…_

2. _Insurance Claim: The table is explicitly labeled as CLAIMS and its columns capture claim identifiers, patient and insurance plan references, billing amounts, claim status, and denial reasons. This ali…_

3. _Laboratory Test Result: The table stores patient-linked test outcomes with fields for test name, LOINC code, value, units, reference range, abnormal flag, and result date, which directly matches diagn…_

---

### ✅ Q026 — Reconstruct a patient's active medications as of a specific historical date.

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0018 | **Gate:** `proceed_with_warning`

**Expected answer:**
> Query medications for patient_id where: (1) start_date <= historical_date AND (end_date IS NULL OR end_date > historical_date) for medication active period, AND (2) valid_from <= historical_date AND (valid_to IS NULL OR valid_to > historical_date) for record validity. Return medication_name, dosage,…

**System answer:**
> From the retrieved context, this cannot be determined.

What is known is that the knowledge graph only describes these concepts:
Insurance Claim, with claim identifiers, patient and insurance plan references, billing amounts, claim status, and denial reasons;
Medical Treatment, described only as medical treatments and procedures performed on patients;
Laboratory Test Result, with patient-linked te…

**Sources retrieved (4):** `Insurance Claim`, `Medical Treatment`, `Laboratory Test Result`, `Patient Appointment`

**Context previews (first 3):**

1. _Insurance Claim: The table is explicitly labeled as CLAIMS and its columns capture claim identifiers, patient and insurance plan references, billing amounts, claim status, and denial reasons. This ali…_

2. _Medical Treatment: Medical treatments and procedures performed on patients.…_

3. _Laboratory Test Result: The table stores patient-linked test outcomes with fields for test name, LOINC code, value, units, reference range, abnormal flag, and result date, which directly matches diagn…_

---

### ✅ Q027 — Count the number of patients per department without exposing individual patient identities.

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0026 | **Gate:** `proceed_with_warning`

**Expected answer:**
> Join appointments to departments on department_id. Group by department_id, department_name, service_line. Count DISTINCT patient_id for privacy (prevents counting multiple appointments per patient). Filter by appointment_date range and exclude canceled/no-show status. Return aggregated counts only—n…

**System answer:**
> The retrieved context only provides schema-level metadata, not actual patient records, so I cannot produce the counts themselves from the knowledge graph.

Based on the available schema, the relevant source is the Patient Appointment table, because it stores both the patient reference and the department. To count patients per department without exposing identities, use that table and aggregate by …

**Sources retrieved (4):** `Insurance Claim`, `Patient Appointment`, `Medical Treatment`, `Laboratory Test Result`

**Context previews (first 3):**

1. _Insurance Claim: The table is explicitly labeled as CLAIMS and its columns capture claim identifiers, patient and insurance plan references, billing amounts, claim status, and denial reasons. This ali…_

2. _Patient Appointment: The table is explicitly documented as storing patient appointment scheduling and encounter information, and its columns capture appointment date/time, patient, provider, departmen…_

3. _Medical Treatment: Medical treatments and procedures performed on patients.…_

---

### ✅ Q028 — What are the most common diagnoses (by count) without linking to specific patients?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0033 | **Gate:** `proceed_with_warning`

**Expected answer:**
> Query diagnoses table grouped by icd_10_code and diagnosis_name. COUNT(*) each diagnosis. Order by count DESC. Return only icd_10_code, diagnosis_name, and count—no patient identifiers, MRNs, or names. Optionally filter by diagnosis_date range. This epidemiological analysis follows HIPAA de-identifi…

**System answer:**
> The retrieved context does not provide enough information to determine the most common diagnoses by count. It contains only high-level business concepts for Laboratory Test Result, Medical Treatment, Patient Appointment, and Insurance Claim, and no diagnosis-specific table, diagnosis codes, or aggregate record counts.

Because the knowledge graph here appears to contain schema-level/business metad…

**Sources retrieved (4):** `Laboratory Test Result`, `Medical Treatment`, `Patient Appointment`, `Insurance Claim`

**Context previews (first 3):**

1. _Laboratory Test Result: The table stores patient-linked test outcomes with fields for test name, LOINC code, value, units, reference range, abnormal flag, and result date, which directly matches diagn…_

2. _Medical Treatment: Medical treatments and procedures performed on patients.…_

3. _Patient Appointment: The table is explicitly documented as storing patient appointment scheduling and encounter information, and its columns capture appointment date/time, patient, provider, departmen…_

---

### ✅ Q029 — Which providers have the highest patient volume without exposing patient information?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0007 | **Gate:** `proceed_with_warning`

**Expected answer:**
> Join appointments to providers on provider_id. Group by provider_id, provider name, NPI, specialty, department. COUNT DISTINCT patient_id for unique patient count (not appointment count). Filter by appointment_date range and completed status. Return only provider information and aggregated counts—no…

**System answer:**
> This cannot be determined from the retrieved context.

What is known is that the Patient Appointment concept stores appointment scheduling and encounter information, including patient, provider, appointment date/time, department, type, duration, status, and cancellation reason. That means provider-linked appointment data exists at the schema/concept level.

What cannot be determined is which provi…

**Sources retrieved (4):** `Insurance Claim`, `Patient Appointment`, `Medical Treatment`, `Laboratory Test Result`

**Context previews (first 3):**

1. _Insurance Claim: The table is explicitly labeled as CLAIMS and its columns capture claim identifiers, patient and insurance plan references, billing amounts, claim status, and denial reasons. This ali…_

2. _Patient Appointment: The table is explicitly documented as storing patient appointment scheduling and encounter information, and its columns capture appointment date/time, patient, provider, departmen…_

3. _Medical Treatment: Medical treatments and procedures performed on patients.…_

---

### ✅ Q030 — What is the average claim payment amount by insurance plan type?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0126 | **Gate:** `proceed_with_warning`

**Expected answer:**
> Join claims to insurance_plans on insurance_plan_id. Group by plan_type (commercial, medicare, medicaid, tricare, self_pay). Calculate AVG(amount_paid) and AVG(amount_charged). Filter by service_date range and claim_status = 'approved' or 'partially_paid'. Return only plan_type and aggregated averag…

**System answer:**
> The retrieved context does not provide enough information to answer that as asked.

It tells us that the CLAIMS table stores claim identifiers, patient and insurance plan references, billing amounts, claim status, and denial reasons. However, it does not mention a claim payment amount field, an insurance plan type attribute, or any table that defines insurance plans in more detail.

So, from the a…

**Sources retrieved (4):** `Insurance Claim`, `Patient Appointment`, `Medical Treatment`, `Laboratory Test Result`

**Context previews (first 3):**

1. _Insurance Claim: The table is explicitly labeled as CLAIMS and its columns capture claim identifiers, patient and insurance plan references, billing amounts, claim status, and denial reasons. This ali…_

2. _Patient Appointment: The table is explicitly documented as storing patient appointment scheduling and encounter information, and its columns capture appointment date/time, patient, provider, departmen…_

3. _Medical Treatment: Medical treatments and procedures performed on patients.…_

---

## Anomalies & Observations

No anomalies detected. All questions grounded with acceptable RAGAS scores.
