# Data Dictionary - Advanced Healthcare Management System

## Database Overview
**Database Name**: `advanced_healthcare_db`
**Schema Version**: `3.2.1`
**Environment**: Production
**Last Updated**: 2025-03-15

---

## PATIENTS Table
**Purpose**: Store current and historical patient demographic and administrative information.

| Column Name | Data Type | Constraint | Description |
|-------------|-----------|------------|-------------|
| patient_id | INTEGER | PRIMARY KEY | Surrogate key for patient records |
| mrn | VARCHAR(20) | UNIQUE NOT NULL | Medical Record Number - unique patient identifier |
| first_name | VARCHAR(50) | NOT NULL | Patient's legal first name |
| last_name | VARCHAR(50) | NOT NULL | Patient's legal last name |
| date_of_birth | DATE | NOT NULL | Patient's date of birth for age calculation |
| gender | VARCHAR(10) | NOT NULL, CHECK IN ('M', 'F', 'O', 'U') | Gender: Male, Female, Other, Unknown |
| phone | VARCHAR(20) | | Primary contact phone number |
| email | VARCHAR(100) | | Primary email address |
| emergency_contact_name | VARCHAR(100) | | Name of emergency contact person |
| emergency_contact_phone | VARCHAR(20) | | Emergency contact phone number |
| primary_insurance_id | INTEGER | FK → insurance_plans.plan_id | Primary insurance coverage |
| is_deleted | BOOLEAN | DEFAULT FALSE | Soft delete flag - true if record logically deleted |
| valid_from | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | Record validity start date |
| valid_to | TIMESTAMP | | Record validity end date (NULL for current) |
| created_at | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | Record creation timestamp |
| updated_at | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | Record last update timestamp |

**Indexes**:
- `idx_patients_mrn` on (mrn) WHERE is_deleted = FALSE
- `idx_patients_name` on (last_name, first_name) WHERE is_deleted = FALSE
- `idx_patients_dob` on (date_of_birth) WHERE is_deleted = FALSE
- `idx_patients_validity` on (valid_from, valid_to)

**Business Rules**:
- MRN is immutable and never reused
- Soft deletes are used for audit compliance
- Historical records maintained for legal requirements (typically 7-10 years)

---

## DIAGNOSES Table
**Purpose**: Store patient diagnosis records with ICD-10 coding and temporal tracking.

| Column Name | Data Type | Constraint | Description |
|-------------|-----------|------------|-------------|
| diagnosis_id | INTEGER | PRIMARY KEY | Surrogate key for diagnosis records |
| patient_id | INTEGER | FK → patients.patient_id, NOT NULL | Patient receiving the diagnosis |
| icd_10_code | VARCHAR(10) | NOT NULL | ICD-10-CM diagnosis code (e.g., I10, E11.9) |
| diagnosis_name | VARCHAR(255) | NOT NULL | Full diagnosis description |
| diagnosis_type | VARCHAR(20) | CHECK IN ('principal', 'comorbidity', 'admitting', 'secondary') | Type/classification of diagnosis |
| provider_id | INTEGER | FK → providers.provider_id | Provider who made the diagnosis |
| diagnosis_date | DATE | NOT NULL | Date diagnosis was clinically confirmed |
| resolution_date | DATE | | Date condition was resolved (NULL if ongoing) |
| is_deleted | BOOLEAN | DEFAULT FALSE | Soft delete flag |
| valid_from | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | Record validity start date |
| valid_to | TIMESTAMP | | Record validity end date |
| created_at | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | Record creation timestamp |
| updated_at | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | Record last update timestamp |

**Indexes**:
- `idx_diagnoses_patient` on (patient_id) WHERE is_deleted = FALSE
- `idx_diagnoses_code` on (icd_10_code) WHERE is_deleted = FALSE
- `idx_diagnoses_date` on (diagnosis_date) WHERE is_deleted = FALSE
- `idx_diagnoses_provider` on (provider_id) WHERE is_deleted = FALSE
- `idx_diagnoses_validity` on (valid_from, valid_to)

**Business Rules**:
- A patient can have multiple diagnoses on the same date
- Only one diagnosis can be marked as 'principal' per encounter
- Historical diagnoses preserved for longitudinal care tracking

---

## TREATMENTS Table
**Purpose**: Store medical treatments and procedures performed on patients.

| Column Name | Data Type | Constraint | Description |
|-------------|-----------|------------|-------------|
| treatment_id | INTEGER | PRIMARY KEY | Surrogate key for treatment records |
| patient_id | INTEGER | FK → patients.patient_id, NOT NULL | Patient receiving treatment |
| diagnosis_id | INTEGER | FK → diagnoses.diagnosis_id | Primary diagnosis indication for treatment |
| treatment_name | VARCHAR(255) | NOT NULL | Description of treatment or procedure |
| cpt_code | VARCHAR(10) | CPT/HCPCS procedure code for billing |
| provider_id | INTEGER | FK → providers.provider_id, NOT NULL | Provider performing treatment |
| department_id | INTEGER | FK → departments.department_id | Department where treatment occurred |
| treatment_date | DATE | NOT NULL | Date treatment was performed |
| treatment_status | VARCHAR(20) | CHECK IN ('scheduled', 'completed', 'canceled', 'in_progress') | Current status of treatment |
| notes | TEXT | | Clinical notes or observations |
| is_deleted | BOOLEAN | DEFAULT FALSE | Soft delete flag |
| valid_from | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | Record validity start date |
| valid_to | TIMESTAMP | | Record validity end date |
| created_at | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | Record creation timestamp |
| updated_at | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | Record last update timestamp |

**Indexes**:
- `idx_treatments_patient` on (patient_id) WHERE is_deleted = FALSE
- `idx_treatments_diagnosis` on (diagnosis_id) WHERE is_deleted = FALSE
- `idx_treatments_provider` on (provider_id) WHERE is_deleted = FALSE
- `idx_treatments_department` on (department_id) WHERE is_deleted = FALSE
- `idx_treatments_date` on (treatment_date) WHERE is_deleted = FALSE
- `idx_treatments_validity` on (valid_from, valid_to)

**Business Rules**:
- Treatments must link to a diagnosis for clinical justification
- CPT codes required for billable procedures
- Treatment can be rescheduled (soft delete + new record)

---

## MEDICATIONS Table
**Purpose**: Store patient medication prescriptions and administrations.

| Column Name | Data Type | Constraint | Description |
|-------------|-----------|------------|-------------|
| medication_id | INTEGER | PRIMARY KEY | Surrogate key for medication records |
| patient_id | INTEGER | FK → patients.patient_id, NOT NULL | Patient receiving medication |
| medication_name | VARCHAR(255) | NOT NULL | Generic or brand medication name |
| ndc_code | VARCHAR(11) | National Drug Code for identification |
| dosage | VARCHAR(50) | NOT NULL | Dosage amount (e.g., '10mg', '500mg') |
| route | VARCHAR(20) | CHECK IN ('oral', 'IV', 'IM', 'topical', 'inhaled', 'subcutaneous') | Route of administration |
| frequency | VARCHAR(50) | NOT NULL | Administration frequency (e.g., 'BID', 'TID', 'PRN') |
| prescribing_provider_id | INTEGER | FK → providers.provider_id, NOT NULL | Provider who prescribed medication |
| start_date | DATE | NOT NULL | Date medication therapy started |
| end_date | DATE | | Date medication therapy ended (NULL if ongoing) |
| is_deleted | BOOLEAN | DEFAULT FALSE | Soft delete flag |
| valid_from | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | Record validity start date |
| valid_to | TIMESTAMP | | Record validity end date |
| created_at | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | Record creation timestamp |
| updated_at | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | Record last update timestamp |

**Indexes**:
- `idx_medications_patient` on (patient_id) WHERE is_deleted = FALSE
- `idx_medications_provider` on (prescribing_provider_id) WHERE is_deleted = FALSE
- `idx_medications_dates` on (start_date, end_date) WHERE is_deleted = FALSE
- `idx_medications_ndc` on (ndc_code) WHERE is_deleted = FALSE
- `idx_medications_validity` on (valid_from, valid_to)

**Business Rules**:
- Medication reconciliation required on admission and discharge
- Active medications have NULL end_date and is_deleted = FALSE
- Prescription changes create new records (historization)

---

## LAB_RESULTS Table
**Purpose**: Store diagnostic laboratory test results for patients.

| Column Name | Data Type | Constraint | Description |
|-------------|-----------|------------|-------------|
| lab_result_id | INTEGER | PRIMARY KEY | Surrogate key for lab result records |
| patient_id | INTEGER | FK → patients.patient_id, NOT NULL | Patient associated with result |
| test_name | VARCHAR(255) | NOT NULL | Name of laboratory test performed |
| loinc_code | VARCHAR(10) | Logical Observation Identifiers Names and Codes |
| test_value | VARCHAR(100) | | Numeric or categorical result value |
| unit | VARCHAR(20) | | Unit of measurement (e.g., 'mg/dL', 'cells/μL') |
| reference_range | VARCHAR(100) | | Expected normal range for patient population |
| is_abnormal | BOOLEAN | DEFAULT FALSE | Flag indicating result outside reference range |
| ordering_provider_id | INTEGER | FK → providers.provider_id | Provider who ordered the test |
| result_date | DATE | NOT NULL | Date test was performed/resulted |
| notes | TEXT | | Pathologist or technician notes |
| is_deleted | BOOLEAN | DEFAULT FALSE | Soft delete flag |
| valid_from | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | Record validity start date |
| valid_to | TIMESTAMP | | Record validity end date |
| created_at | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | Record creation timestamp |
| updated_at | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | Record last update timestamp |

**Indexes**:
- `idx_lab_results_patient` on (patient_id) WHERE is_deleted = FALSE
- `idx_lab_results_test` on (test_name) WHERE is_deleted = FALSE
- `idx_lab_results_date` on (result_date) WHERE is_deleted = FALSE
- `idx_lab_results_abnormal` on (is_abnormal) WHERE is_abnormal = TRUE AND is_deleted = FALSE
- `idx_lab_results_validity` on (valid_from, valid_to)

**Business Rules**:
- LOINC codes standardize test names across systems
- Abnormal flags automatically calculated based on reference ranges
- Critical results require immediate provider notification

---

## PROVIDERS Table
**Purpose**: Store healthcare provider information and credentials.

| Column Name | Data Type | Constraint | Description |
|-------------|-----------|------------|-------------|
| provider_id | INTEGER | PRIMARY KEY | Surrogate key for provider records |
| npi | VARCHAR(10) | UNIQUE NOT NULL | National Provider Identifier |
| first_name | VARCHAR(50) | NOT NULL | Provider's first name |
| last_name | VARCHAR(50) | NOT NULL | Provider's last name |
| provider_type | VARCHAR(50) | CHECK IN ('MD', 'DO', 'NP', 'PA', 'RN', 'PT', 'Other') | Provider credential type |
| specialty | VARCHAR(100) | | Medical specialty (e.g., 'Cardiology', 'Internal Medicine') |
| department_id | INTEGER | FK → departments.department_id | Primary department affiliation |
| is_active | BOOLEAN | DEFAULT TRUE | Provider active status |
| is_deleted | BOOLEAN | DEFAULT FALSE | Soft delete flag |
| valid_from | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | Record validity start date |
| valid_to | TIMESTAMP | | Record validity end date |
| created_at | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | Record creation timestamp |
| updated_at | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | Record last update timestamp |

**Indexes**:
- `idx_providers_npi` on (npi) WHERE is_deleted = FALSE
- `idx_providers_name` on (last_name, first_name) WHERE is_deleted = FALSE
- `idx_providers_department` on (department_id) WHERE is_deleted = FALSE
- `idx_providers_active` on (is_active) WHERE is_active = TRUE AND is_deleted = FALSE
- `idx_providers_validity` on (valid_from, valid_to)

**Business Rules**:
- NPI is a unique federal identifier assigned for life
- Providers may have privileges in multiple departments
- Credentialing status managed externally (not in this table)

---

## DEPARTMENTS Table
**Purpose**: Store organizational department and service line structure.

| Column Name | Data Type | Constraint | Description |
|-------------|-----------|------------|-------------|
| department_id | INTEGER | PRIMARY KEY | Surrogate key for department records |
| department_name | VARCHAR(100) | NOT NULL | Department name |
| department_code | VARCHAR(20) | UNIQUE NOT NULL | Standard department abbreviation |
| parent_department_id | INTEGER | FK → departments.department_id | Parent department for hierarchy |
| service_line | VARCHAR(100) | | Strategic service line affiliation |
| location | VARCHAR(100) | | Physical location within facility |
| is_active | BOOLEAN | DEFAULT TRUE | Department active status |
| is_deleted | BOOLEAN | DEFAULT FALSE | Soft delete flag |
| valid_from | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | Record validity start date |
| valid_to | TIMESTAMP | | Record validity end date |
| created_at | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | Record creation timestamp |
| updated_at | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | Record last update timestamp |

**Indexes**:
- `idx_departments_code` on (department_code) WHERE is_deleted = FALSE
- `idx_departments_parent` on (parent_department_id) WHERE is_deleted = FALSE
- `idx_departments_service_line` on (service_line) WHERE is_deleted = FALSE
- `idx_departments_active` on (is_active) WHERE is_active = TRUE AND is_deleted = FALSE
- `idx_departments_validity` on (valid_from, valid_to)

**Business Rules**:
- Department codes are used for scheduling and billing
- Hierarchical structure supports organizational reporting
- Service lines group departments for strategic planning

---

## APPOINTMENTS Table
**Purpose**: Store patient appointment scheduling and encounter information.

| Column Name | Data Type | Constraint | Description |
|-------------|-----------|------------|-------------|
| appointment_id | INTEGER | PRIMARY KEY | Surrogate key for appointment records |
| patient_id | INTEGER | FK → patients.patient_id, NOT NULL | Patient scheduled for appointment |
| provider_id | INTEGER | FK → providers.provider_id, NOT NULL | Provider conducting appointment |
| department_id | INTEGER | FK → departments.department_id | Department for appointment |
| appointment_date | DATE | NOT NULL | Scheduled date of appointment |
| appointment_time | TIME | NOT NULL | Scheduled time of appointment |
| appointment_type | VARCHAR(50) | CHECK IN ('new_patient', 'established', 'consultation', 'follow_up', 'procedure', 'telehealth') | Type of appointment |
| duration_minutes | INTEGER | DEFAULT 30 | Expected duration in minutes |
| appointment_status | VARCHAR(20) | CHECK IN ('scheduled', 'confirmed', 'checked_in', 'in_progress', 'completed', 'canceled', 'no_show') | Current status |
| cancellation_reason | VARCHAR(255) | | Reason if appointment canceled |
| is_deleted | BOOLEAN | DEFAULT FALSE | Soft delete flag |
| valid_from | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | Record validity start date |
| valid_to | TIMESTAMP | | Record validity end date |
| created_at | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | Record creation timestamp |
| updated_at | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | Record last update timestamp |

**Indexes**:
- `idx_appointments_patient` on (patient_id) WHERE is_deleted = FALSE
- `idx_appointments_provider` on (provider_id) WHERE is_deleted = FALSE
- `idx_appointments_datetime` on (appointment_date, appointment_time) WHERE is_deleted = FALSE
- `idx_appointments_status` on (appointment_status) WHERE is_deleted = FALSE
- `idx_appointments_validity` on (valid_from, valid_to)

**Business Rules**:
- Appointment status workflow must follow state transitions
- Cancellations require documented reasons
- No-show tracking for patient attendance metrics

---

## INSURANCE_PLANS Table
**Purpose**: Store insurance payer and plan information for coverage.

| Column Name | Data Type | Constraint | Description |
|-------------|-----------|------------|-------------|
| plan_id | INTEGER | PRIMARY KEY | Surrogate key for insurance plan records |
| plan_name | VARCHAR(100) | NOT NULL | Insurance plan name |
| payer_name | VARCHAR(100) | NOT NULL | Insurance company or payer name |
| plan_type | VARCHAR(20) | CHECK IN ('commercial', 'medicare', 'medicaid', 'tricare', 'self_pay') | Type of insurance coverage |
| prior_auth_required | BOOLEAN | DEFAULT FALSE | Whether plan requires prior authorization |
| is_active | BOOLEAN | DEFAULT TRUE | Plan active status |
| is_deleted | BOOLEAN | DEFAULT FALSE | Soft delete flag |
| valid_from | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | Record validity start date |
| valid_to | TIMESTAMP | | Record validity end date |
| created_at | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | Record creation timestamp |
| updated_at | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | Record last update timestamp |

**Indexes**:
- `idx_insurance_payer` on (payer_name) WHERE is_deleted = FALSE
- `idx_insurance_type` on (plan_type) WHERE is_deleted = FALSE
- `idx_insurance_active` on (is_active) WHERE is_active = TRUE AND is_deleted = FALSE
- `idx_insurance_validity` on (valid_from, valid_to)

**Business Rules**:
- Plan names are not globally unique (payer_name + plan_name is unique)
- Prior authorization requirements affect claim submission workflows
- Medicare/Medicaid plans have mandated coverage policies

---

## CLAIMS Table
**Purpose**: Store insurance claims and billing information for services rendered.

| Column Name | Data Type | Constraint | Description |
|-------------|-----------|------------|-------------|
| claim_id | INTEGER | PRIMARY KEY | Surrogate key for claim records |
| patient_id | INTEGER | FK → patients.patient_id, NOT NULL | Patient associated with claim |
| insurance_plan_id | INTEGER | FK → insurance_plans.plan_id, NOT NULL | Insurance plan billed |
| claim_number | VARCHAR(50) | UNIQUE NOT NULL | Unique claim identifier for tracking |
| service_date | DATE | NOT NULL | Date of service |
| submission_date | DATE | NOT NULL | Date claim submitted to payer |
| cpt_code | VARCHAR(10) | NOT NULL | Procedure code billed |
| icd_10_code | VARCHAR(10) | NOT NULL | Diagnosis code supporting medical necessity |
| amount_charged | DECIMAL(10,2) | NOT NULL | Amount billed to insurance |
| amount_allowed | DECIMAL(10,2) | | Payer's allowed amount |
| amount_paid | DECIMAL(10,2) | DEFAULT 0.00 | Amount actually paid by payer |
| claim_status | VARCHAR(20) | CHECK IN ('submitted', 'pending', 'approved', 'denied', 'partially_paid', 'appealed') | Current claim status |
| denial_reason | VARCHAR(255) | | Reason if claim denied |
| is_deleted | BOOLEAN | DEFAULT FALSE | Soft delete flag |
| valid_from | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | Record validity start date |
| valid_to | TIMESTAMP | | Record validity end date |
| created_at | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | Record creation timestamp |
| updated_at | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | Record last update timestamp |

**Indexes**:
- `idx_claims_patient` on (patient_id) WHERE is_deleted = FALSE
- `idx_claims_insurance` on (insurance_plan_id) WHERE is_deleted = FALSE
- `idx_claims_number` on (claim_number) WHERE is_deleted = FALSE
- `idx_claims_status` on (claim_status) WHERE is_deleted = FALSE
- `idx_claims_service_date` on (service_date) WHERE is_deleted = FALSE
- `idx_claims_validity` on (valid_from, valid_to)

**Business Rules**:
- Claim number format: {payer_code}-{YYYYMMDD}-{sequence}
- Claims must link to valid diagnosis for medical necessity
- Denial reasons trigger appeal workflows when clinically appropriate

---

## Foreign Key Relationships

### Patient Relationships
- `patients.primary_insurance_id` → `insurance_plans.plan_id`
- `diagnoses.patient_id` → `patients.patient_id`
- `treatments.patient_id` → `patients.patient_id`
- `medications.patient_id` → `patients.patient_id`
- `lab_results.patient_id` → `patients.patient_id`
- `appointments.patient_id` → `patients.patient_id`
- `claims.patient_id` → `patients.patient_id`

### Provider Relationships
- `diagnoses.provider_id` → `providers.provider_id`
- `treatments.provider_id` → `providers.provider_id`
- `medications.prescribing_provider_id` → `providers.provider_id`
- `lab_results.ordering_provider_id` → `providers.provider_id`
- `appointments.provider_id` → `providers.provider_id`
- `providers.department_id` → `departments.department_id`

### Department Relationships
- `treatments.department_id` → `departments.department_id`
- `appointments.department_id` → `departments.department_id`
- `departments.parent_department_id` → `departments.department_id` (self-referential)

### Clinical Linkages
- `treatments.diagnosis_id` → `diagnoses.diagnosis_id`

## General Conventions

### Temporal Validity Pattern
All major tables use `valid_from` and `valid_to` timestamps for historization:
- Current records have `valid_to = NULL`
- Historical records have non-NULL `valid_to`
- Queries must include `WHERE valid_to IS NULL` to retrieve current data
- Historical analysis possible by querying all records

### Soft Delete Pattern
All tables include `is_deleted` flag:
- `is_deleted = FALSE` for active records
- `is_deleted = TRUE` for logically deleted records
- Queries must include `WHERE is_deleted = FALSE` to exclude deleted records
- Soft deletes preserve audit trail

### Audit Timestamps
All tables include:
- `created_at` - set once on INSERT
- `updated_at` - updated on each UPDATE

### Naming Conventions
- Table names: plural_snake_case (e.g., `insurance_plans`, `lab_results`)
- Column names: snake_case
- Foreign keys: `{table}_{column}` (e.g., `patient_id`, `provider_id`)
- Indexes: `idx_{table}_{column(s)}_{condition}`