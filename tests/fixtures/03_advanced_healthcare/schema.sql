-- Advanced Healthcare Management System Database Schema
-- Schema Version: 3.2.1
-- Database: advanced_healthcare_db
-- Last Updated: 2025-03-15

-- Enable temporal tables for historization
SET TIMEZONE = 'UTC';

-- ==============================================================================
-- PATIENTS Table
-- Purpose: Store current and historical patient demographic and administrative information
-- ==============================================================================
CREATE TABLE patients (
    patient_id SERIAL PRIMARY KEY,
    mrn VARCHAR(20) UNIQUE NOT NULL,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    date_of_birth DATE NOT NULL,
    gender VARCHAR(10) NOT NULL CHECK (gender IN ('M', 'F', 'O', 'U')),
    phone VARCHAR(20),
    email VARCHAR(100),
    emergency_contact_name VARCHAR(100),
    emergency_contact_phone VARCHAR(20),
    primary_insurance_id INTEGER REFERENCES insurance_plans(plan_id),
    is_deleted BOOLEAN DEFAULT FALSE,
    valid_from TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    valid_to TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Indexes for patients
CREATE INDEX idx_patients_mrn ON patients(mrn) WHERE is_deleted = FALSE;
CREATE INDEX idx_patients_name ON patients(last_name, first_name) WHERE is_deleted = FALSE;
CREATE INDEX idx_patients_dob ON patients(date_of_birth) WHERE is_deleted = FALSE;
CREATE INDEX idx_patients_validity ON patients(valid_from, valid_to);

-- ==============================================================================
-- INSURANCE_PLANS Table
-- Purpose: Store insurance payer and plan information for coverage
-- ==============================================================================
CREATE TABLE insurance_plans (
    plan_id SERIAL PRIMARY KEY,
    plan_name VARCHAR(100) NOT NULL,
    payer_name VARCHAR(100) NOT NULL,
    plan_type VARCHAR(20) NOT NULL CHECK (plan_type IN ('commercial', 'medicare', 'medicaid', 'tricare', 'self_pay')),
    prior_auth_required BOOLEAN DEFAULT FALSE,
    is_active BOOLEAN DEFAULT TRUE,
    is_deleted BOOLEAN DEFAULT FALSE,
    valid_from TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    valid_to TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Indexes for insurance_plans
CREATE INDEX idx_insurance_payer ON insurance_plans(payer_name) WHERE is_deleted = FALSE;
CREATE INDEX idx_insurance_type ON insurance_plans(plan_type) WHERE is_deleted = FALSE;
CREATE INDEX idx_insurance_active ON insurance_plans(is_active) WHERE is_active = TRUE AND is_deleted = FALSE;
CREATE INDEX idx_insurance_validity ON insurance_plans(valid_from, valid_to);

-- ==============================================================================
-- DEPARTMENTS Table
-- Purpose: Store organizational department and service line structure
-- ==============================================================================
CREATE TABLE departments (
    department_id SERIAL PRIMARY KEY,
    department_name VARCHAR(100) NOT NULL,
    department_code VARCHAR(20) UNIQUE NOT NULL,
    parent_department_id INTEGER REFERENCES departments(department_id),
    service_line VARCHAR(100),
    location VARCHAR(100),
    is_active BOOLEAN DEFAULT TRUE,
    is_deleted BOOLEAN DEFAULT FALSE,
    valid_from TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    valid_to TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Indexes for departments
CREATE INDEX idx_departments_code ON departments(department_code) WHERE is_deleted = FALSE;
CREATE INDEX idx_departments_parent ON departments(parent_department_id) WHERE is_deleted = FALSE;
CREATE INDEX idx_departments_service_line ON departments(service_line) WHERE is_deleted = FALSE;
CREATE INDEX idx_departments_active ON departments(is_active) WHERE is_active = TRUE AND is_deleted = FALSE;
CREATE INDEX idx_departments_validity ON departments(valid_from, valid_to);

-- ==============================================================================
-- PROVIDERS Table
-- Purpose: Store healthcare provider information and credentials
-- ==============================================================================
CREATE TABLE providers (
    provider_id SERIAL PRIMARY KEY,
    npi VARCHAR(10) UNIQUE NOT NULL,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    provider_type VARCHAR(50) NOT NULL CHECK (provider_type IN ('MD', 'DO', 'NP', 'PA', 'RN', 'PT', 'Other')),
    specialty VARCHAR(100),
    department_id INTEGER REFERENCES departments(department_id),
    is_active BOOLEAN DEFAULT TRUE,
    is_deleted BOOLEAN DEFAULT FALSE,
    valid_from TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    valid_to TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Indexes for providers
CREATE INDEX idx_providers_npi ON providers(npi) WHERE is_deleted = FALSE;
CREATE INDEX idx_providers_name ON providers(last_name, first_name) WHERE is_deleted = FALSE;
CREATE INDEX idx_providers_department ON providers(department_id) WHERE is_deleted = FALSE;
CREATE INDEX idx_providers_active ON providers(is_active) WHERE is_active = TRUE AND is_deleted = FALSE;
CREATE INDEX idx_providers_validity ON providers(valid_from, valid_to);

-- ==============================================================================
-- DIAGNOSES Table
-- Purpose: Store patient diagnosis records with ICD-10 coding and temporal tracking
-- ==============================================================================
CREATE TABLE diagnoses (
    diagnosis_id SERIAL PRIMARY KEY,
    patient_id INTEGER NOT NULL REFERENCES patients(patient_id),
    icd_10_code VARCHAR(10) NOT NULL,
    diagnosis_name VARCHAR(255) NOT NULL,
    diagnosis_type VARCHAR(20) CHECK (diagnosis_type IN ('principal', 'comorbidity', 'admitting', 'secondary')),
    provider_id INTEGER REFERENCES providers(provider_id),
    diagnosis_date DATE NOT NULL,
    resolution_date DATE,
    is_deleted BOOLEAN DEFAULT FALSE,
    valid_from TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    valid_to TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Indexes for diagnoses
CREATE INDEX idx_diagnoses_patient ON diagnoses(patient_id) WHERE is_deleted = FALSE;
CREATE INDEX idx_diagnoses_code ON diagnoses(icd_10_code) WHERE is_deleted = FALSE;
CREATE INDEX idx_diagnoses_date ON diagnoses(diagnosis_date) WHERE is_deleted = FALSE;
CREATE INDEX idx_diagnoses_provider ON diagnoses(provider_id) WHERE is_deleted = FALSE;
CREATE INDEX idx_diagnoses_validity ON diagnoses(valid_from, valid_to);

-- ==============================================================================
-- TREATMENTS Table
-- Purpose: Store medical treatments and procedures performed on patients
-- ==============================================================================
CREATE TABLE treatments (
    treatment_id SERIAL PRIMARY KEY,
    patient_id INTEGER NOT NULL REFERENCES patients(patient_id),
    diagnosis_id INTEGER REFERENCES diagnoses(diagnosis_id),
    treatment_name VARCHAR(255) NOT NULL,
    cpt_code VARCHAR(10),
    provider_id INTEGER NOT NULL REFERENCES providers(provider_id),
    department_id INTEGER REFERENCES departments(department_id),
    treatment_date DATE NOT NULL,
    treatment_status VARCHAR(20) CHECK (treatment_status IN ('scheduled', 'completed', 'canceled', 'in_progress')),
    notes TEXT,
    is_deleted BOOLEAN DEFAULT FALSE,
    valid_from TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    valid_to TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Indexes for treatments
CREATE INDEX idx_treatments_patient ON treatments(patient_id) WHERE is_deleted = FALSE;
CREATE INDEX idx_treatments_diagnosis ON treatments(diagnosis_id) WHERE is_deleted = FALSE;
CREATE INDEX idx_treatments_provider ON treatments(provider_id) WHERE is_deleted = FALSE;
CREATE INDEX idx_treatments_department ON treatments(department_id) WHERE is_deleted = FALSE;
CREATE INDEX idx_treatments_date ON treatments(treatment_date) WHERE is_deleted = FALSE;
CREATE INDEX idx_treatments_validity ON treatments(valid_from, valid_to);

-- ==============================================================================
-- MEDICATIONS Table
-- Purpose: Store patient medication prescriptions and administrations
-- ==============================================================================
CREATE TABLE medications (
    medication_id SERIAL PRIMARY KEY,
    patient_id INTEGER NOT NULL REFERENCES patients(patient_id),
    medication_name VARCHAR(255) NOT NULL,
    ndc_code VARCHAR(11),
    dosage VARCHAR(50) NOT NULL,
    route VARCHAR(20) CHECK (route IN ('oral', 'IV', 'IM', 'topical', 'inhaled', 'subcutaneous')),
    frequency VARCHAR(50) NOT NULL,
    prescribing_provider_id INTEGER NOT NULL REFERENCES providers(provider_id),
    start_date DATE NOT NULL,
    end_date DATE,
    is_deleted BOOLEAN DEFAULT FALSE,
    valid_from TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    valid_to TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Indexes for medications
CREATE INDEX idx_medications_patient ON medications(patient_id) WHERE is_deleted = FALSE;
CREATE INDEX idx_medications_provider ON medications(prescribing_provider_id) WHERE is_deleted = FALSE;
CREATE INDEX idx_medications_dates ON medications(start_date, end_date) WHERE is_deleted = FALSE;
CREATE INDEX idx_medications_ndc ON medications(ndc_code) WHERE is_deleted = FALSE;
CREATE INDEX idx_medications_validity ON medications(valid_from, valid_to);

-- ==============================================================================
-- LAB_RESULTS Table
-- Purpose: Store diagnostic laboratory test results for patients
-- ==============================================================================
CREATE TABLE lab_results (
    lab_result_id SERIAL PRIMARY KEY,
    patient_id INTEGER NOT NULL REFERENCES patients(patient_id),
    test_name VARCHAR(255) NOT NULL,
    loinc_code VARCHAR(10),
    test_value VARCHAR(100),
    unit VARCHAR(20),
    reference_range VARCHAR(100),
    is_abnormal BOOLEAN DEFAULT FALSE,
    ordering_provider_id INTEGER REFERENCES providers(provider_id),
    result_date DATE NOT NULL,
    notes TEXT,
    is_deleted BOOLEAN DEFAULT FALSE,
    valid_from TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    valid_to TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Indexes for lab_results
CREATE INDEX idx_lab_results_patient ON lab_results(patient_id) WHERE is_deleted = FALSE;
CREATE INDEX idx_lab_results_test ON lab_results(test_name) WHERE is_deleted = FALSE;
CREATE INDEX idx_lab_results_date ON lab_results(result_date) WHERE is_deleted = FALSE;
CREATE INDEX idx_lab_results_abnormal ON lab_results(is_abnormal) WHERE is_abnormal = TRUE AND is_deleted = FALSE;
CREATE INDEX idx_lab_results_validity ON lab_results(valid_from, valid_to);

-- ==============================================================================
-- APPOINTMENTS Table
-- Purpose: Store patient appointment scheduling and encounter information
-- ==============================================================================
CREATE TABLE appointments (
    appointment_id SERIAL PRIMARY KEY,
    patient_id INTEGER NOT NULL REFERENCES patients(patient_id),
    provider_id INTEGER NOT NULL REFERENCES providers(provider_id),
    department_id INTEGER REFERENCES departments(department_id),
    appointment_date DATE NOT NULL,
    appointment_time TIME NOT NULL,
    appointment_type VARCHAR(50) CHECK (appointment_type IN ('new_patient', 'established', 'consultation', 'follow_up', 'procedure', 'telehealth')),
    duration_minutes INTEGER DEFAULT 30,
    appointment_status VARCHAR(20) CHECK (appointment_status IN ('scheduled', 'confirmed', 'checked_in', 'in_progress', 'completed', 'canceled', 'no_show')),
    cancellation_reason VARCHAR(255),
    is_deleted BOOLEAN DEFAULT FALSE,
    valid_from TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    valid_to TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Indexes for appointments
CREATE INDEX idx_appointments_patient ON appointments(patient_id) WHERE is_deleted = FALSE;
CREATE INDEX idx_appointments_provider ON appointments(provider_id) WHERE is_deleted = FALSE;
CREATE INDEX idx_appointments_datetime ON appointments(appointment_date, appointment_time) WHERE is_deleted = FALSE;
CREATE INDEX idx_appointments_status ON appointments(appointment_status) WHERE is_deleted = FALSE;
CREATE INDEX idx_appointments_validity ON appointments(valid_from, valid_to);

-- ==============================================================================
-- CLAIMS Table
-- Purpose: Store insurance claims and billing information for services rendered
-- ==============================================================================
CREATE TABLE claims (
    claim_id SERIAL PRIMARY KEY,
    patient_id INTEGER NOT NULL REFERENCES patients(patient_id),
    insurance_plan_id INTEGER NOT NULL REFERENCES insurance_plans(plan_id),
    claim_number VARCHAR(50) UNIQUE NOT NULL,
    service_date DATE NOT NULL,
    submission_date DATE NOT NULL,
    cpt_code VARCHAR(10) NOT NULL,
    icd_10_code VARCHAR(10) NOT NULL,
    amount_charged DECIMAL(10,2) NOT NULL,
    amount_allowed DECIMAL(10,2),
    amount_paid DECIMAL(10,2) DEFAULT 0.00,
    claim_status VARCHAR(20) CHECK (claim_status IN ('submitted', 'pending', 'approved', 'denied', 'partially_paid', 'appealed')),
    denial_reason VARCHAR(255),
    is_deleted BOOLEAN DEFAULT FALSE,
    valid_from TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    valid_to TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Indexes for claims
CREATE INDEX idx_claims_patient ON claims(patient_id) WHERE is_deleted = FALSE;
CREATE INDEX idx_claims_insurance ON claims(insurance_plan_id) WHERE is_deleted = FALSE;
CREATE INDEX idx_claims_number ON claims(claim_number) WHERE is_deleted = FALSE;
CREATE INDEX idx_claims_status ON claims(claim_status) WHERE is_deleted = FALSE;
CREATE INDEX idx_claims_service_date ON claims(service_date) WHERE is_deleted = FALSE;
CREATE INDEX idx_claims_validity ON claims(valid_from, valid_to);

-- ==============================================================================
-- TRIGGERS for updated_at timestamp management
-- ==============================================================================
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Apply updated_at triggers to all tables
CREATE TRIGGER update_patients_updated_at BEFORE UPDATE ON patients
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_insurance_plans_updated_at BEFORE UPDATE ON insurance_plans
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_departments_updated_at BEFORE UPDATE ON departments
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_providers_updated_at BEFORE UPDATE ON providers
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_diagnoses_updated_at BEFORE UPDATE ON diagnoses
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_treatments_updated_at BEFORE UPDATE ON treatments
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_medications_updated_at BEFORE UPDATE ON medications
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_lab_results_updated_at BEFORE UPDATE ON lab_results
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_appointments_updated_at BEFORE UPDATE ON appointments
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_claims_updated_at BEFORE UPDATE ON claims
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- ==============================================================================
-- VIEWS for common queries (excluding soft-deleted records)
-- ==============================================================================

-- Current active patients
CREATE OR REPLACE VIEW v_active_patients AS
SELECT patient_id, mrn, first_name, last_name, date_of_birth, gender, phone, email,
       emergency_contact_name, emergency_contact_phone, primary_insurance_id
FROM patients
WHERE is_deleted = FALSE AND valid_to IS NULL;

-- Current active providers
CREATE OR REPLACE VIEW v_active_providers AS
SELECT provider_id, npi, first_name, last_name, provider_type, specialty, department_id
FROM providers
WHERE is_deleted = FALSE AND valid_to IS NULL AND is_active = TRUE;

-- Current active departments
CREATE OR REPLACE VIEW v_active_departments AS
SELECT department_id, department_name, department_code, parent_department_id,
       service_line, location
FROM departments
WHERE is_deleted = FALSE AND valid_to IS NULL AND is_active = TRUE;

-- Current active diagnoses
CREATE OR REPLACE VIEW v_active_diagnoses AS
SELECT d.diagnosis_id, d.patient_id, d.icd_10_code, d.diagnosis_name,
       d.diagnosis_type, d.provider_id, d.diagnosis_date, d.resolution_date,
       p.first_name || ' ' || p.last_name AS patient_name,
       pr.first_name || ' ' || pr.last_name AS provider_name
FROM diagnoses d
JOIN patients p ON d.patient_id = p.patient_id
LEFT JOIN providers pr ON d.provider_id = pr.provider_id
WHERE d.is_deleted = FALSE AND d.valid_to IS NULL;

-- Current active medications
CREATE OR REPLACE VIEW v_active_medications AS
SELECT m.medication_id, m.patient_id, m.medication_name, m.ndc_code,
       m.dosage, m.route, m.frequency, m.prescribing_provider_id,
       m.start_date, m.end_date,
       p.first_name || ' ' || p.last_name AS patient_name,
       pr.first_name || ' ' || pr.last_name AS provider_name
FROM medications m
JOIN patients p ON m.patient_id = p.patient_id
JOIN providers pr ON m.prescribing_provider_id = pr.provider_id
WHERE m.is_deleted = FALSE AND m.valid_to IS NULL;

-- Current active treatments
CREATE OR REPLACE VIEW v_active_treatments AS
SELECT t.treatment_id, t.patient_id, t.diagnosis_id, t.treatment_name,
       t.cpt_code, t.provider_id, t.department_id, t.treatment_date,
       t.treatment_status, t.notes,
       p.first_name || ' ' || p.last_name AS patient_name,
       pr.first_name || ' ' || pr.last_name AS provider_name,
       d.department_name
FROM treatments t
JOIN patients p ON t.patient_id = p.patient_id
JOIN providers pr ON t.provider_id = pr.provider_id
LEFT JOIN departments d ON t.department_id = d.department_id
WHERE t.is_deleted = FALSE AND t.valid_to IS NULL;

-- Current active lab results
CREATE OR REPLACE VIEW v_active_lab_results AS
SELECT lr.lab_result_id, lr.patient_id, lr.test_name, lr.loinc_code,
       lr.test_value, lr.unit, lr.reference_range, lr.is_abnormal,
       lr.ordering_provider_id, lr.result_date, lr.notes,
       p.first_name || ' ' || p.last_name AS patient_name,
       pr.first_name || ' ' || pr.last_name AS provider_name
FROM lab_results lr
JOIN patients p ON lr.patient_id = p.patient_id
LEFT JOIN providers pr ON lr.ordering_provider_id = pr.provider_id
WHERE lr.is_deleted = FALSE AND lr.valid_to IS NULL;

-- Current active appointments
CREATE OR REPLACE VIEW v_active_appointments AS
SELECT a.appointment_id, a.patient_id, a.provider_id, a.department_id,
       a.appointment_date, a.appointment_time, a.appointment_type,
       a.duration_minutes, a.appointment_status, a.cancellation_reason,
       p.first_name || ' ' || p.last_name AS patient_name,
       pr.first_name || ' ' || pr.last_name AS provider_name,
       d.department_name
FROM appointments a
JOIN patients p ON a.patient_id = p.patient_id
JOIN providers pr ON a.provider_id = pr.provider_id
LEFT JOIN departments d ON a.department_id = d.department_id
WHERE a.is_deleted = FALSE AND a.valid_to IS NULL;

-- Current active claims
CREATE OR REPLACE VIEW v_active_claims AS
SELECT c.claim_id, c.patient_id, c.insurance_plan_id, c.claim_number,
       c.service_date, c.submission_date, c.cpt_code, c.icd_10_code,
       c.amount_charged, c.amount_allowed, c.amount_paid, c.claim_status,
       c.denial_reason,
       p.first_name || ' ' || p.last_name AS patient_name,
       ip.plan_name, ip.payer_name, ip.plan_type
FROM claims c
JOIN patients p ON c.patient_id = p.patient_id
JOIN insurance_plans ip ON c.insurance_plan_id = ip.plan_id
WHERE c.is_deleted = FALSE AND c.valid_to IS NULL;

-- ==============================================================================
-- COMMENTS for table documentation
-- ==============================================================================

COMMENT ON TABLE patients IS 'Patient demographic and administrative information with historization';
COMMENT ON TABLE insurance_plans IS 'Insurance payer and plan coverage information';
COMMENT ON TABLE departments IS 'Organizational department structure with hierarchical relationships';
COMMENT ON TABLE providers IS 'Healthcare provider credentials and affiliations';
COMMENT ON TABLE diagnoses IS 'Patient diagnoses with ICD-10 coding and temporal tracking';
COMMENT ON TABLE treatments IS 'Medical treatments and procedures with clinical linkages';
COMMENT ON TABLE medications IS 'Medication prescriptions and administration records';
COMMENT ON TABLE lab_results IS 'Diagnostic laboratory test results and interpretations';
COMMENT ON TABLE appointments IS 'Patient appointment scheduling and encounter tracking';
COMMENT ON TABLE claims IS 'Insurance claims and billing information';

COMMENT ON COLUMN patients.mrn IS 'Medical Record Number - unique immutable patient identifier';
COMMENT ON COLUMN patients.valid_to IS 'NULL for current records, non-NULL for historical records';
COMMENT ON COLUMN patients.is_deleted IS 'Soft delete flag for audit compliance';

COMMENT ON COLUMN diagnoses.diagnosis_type IS 'principal, comorbidity, admitting, or secondary';
COMMENT ON COLUMN diagnoses.resolution_date IS 'NULL if condition is ongoing';

COMMENT ON COLUMN medications.ndc_code IS 'National Drug Code for medication identification';
COMMENT ON COLUMN medications.end_date IS 'NULL if medication is currently active';

COMMENT ON COLUMN lab_results.loinc_code IS 'Logical Observation Identifiers Names and Codes';
COMMENT ON COLUMN lab_results.is_abnormal IS 'TRUE if result is outside reference range';

COMMENT ON COLUMN providers.npi IS 'National Provider Identifier - unique federal identifier';

COMMENT ON COLUMN claims.claim_number IS 'Unique identifier in format: {payer_code}-{YYYYMMDD}-{sequence}';
COMMENT ON COLUMN claims.claim_status IS 'submitted, pending, approved, denied, partially_paid, or appealed';