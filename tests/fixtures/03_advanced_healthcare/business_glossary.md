# Business Glossary - Advanced Healthcare Management System

## Patient Management

**Patient**
An individual receiving medical care, treatment, or services from the healthcare organization. Each patient has a unique medical record number and may have multiple episodes of care across different time periods. Patients can be identified by their medical record number (MRN), which is distinct from any external insurance identifiers.

**Patient Registration**
The process of capturing essential demographic and administrative information when a patient first presents to the healthcare system. This includes personal details, emergency contacts, insurance information, and consent forms.

## Clinical Concepts

**Diagnosis**
The identification of a disease, condition, or injury based on clinical evaluation, laboratory results, and diagnostic imaging. Diagnoses are coded using ICD-10-CM (International Classification of Diseases, 10th Revision, Clinical Modification) for billing and epidemiological purposes. A patient may have multiple concurrent diagnoses with varying levels of clinical priority.

**Principal Diagnosis**
The primary condition identified after study as chiefly responsible for admission of the patient to the healthcare facility. This diagnosis determines the primary diagnosis-related group (DRG) for billing purposes.

**Comorbidity**
Any additional diagnosis that exists simultaneously with the principal diagnosis. Comorbidities affect patient complexity scores and reimbursement levels under risk-adjusted payment models.

**Treatment**
Any medical intervention, therapeutic procedure, or clinical action taken to address a diagnosed condition. Treatments range from medication administration to surgical procedures and behavioral therapies. Each treatment is linked to specific diagnoses through clinical justification.

**Medication**
Any pharmaceutical substance administered to a patient for therapeutic purposes. Medications include prescription drugs, over-the-counter medications, and controlled substances. Each medication record includes dosage, route of administration, frequency, and prescribing provider.

**Medication Reconciliation**
The process of comparing a patient's medication orders to all medications the patient has been taking to avoid errors, omissions, duplications, and drug interactions.

**LabResult**
The outcome of diagnostic laboratory tests performed on patient specimens (blood, urine, tissue, etc.). Results include quantitative values, reference ranges, abnormality flags, and interpreting pathologist notes. Results are timestamped and linked to specific test orders.

## Provider & Organizational Structure

**Provider**
A licensed healthcare professional authorized to deliver medical services within their scope of practice. Provider types include physicians (MD/DO), nurse practitioners (NP), physician assistants (PA), registered nurses (RN), and clinical specialists. Each provider has unique National Provider Identifier (NPI) numbers and hospital credentialing status.

**Attending Physician**
The primary physician responsible for a patient's care during an admission or encounter. This physician has ultimate authority over treatment decisions and discharge planning.

**Consulting Physician**
A specialist called upon to provide expert opinion or manage specific aspects of a patient's condition beyond the attending physician's expertise.

**Department**
An organizational unit within the healthcare facility dedicated to specific medical specialties or services (e.g., Emergency Department, Cardiology, Oncology, Radiology). Departments have hierarchical relationships and may be subdivided into sub-specialties.

**Service Line**
A strategic grouping of related departments focused on a specific patient population or disease continuum (e.g., Heart & Vascular, Neuroscience, Orthopedics). Service lines are used for operational and financial reporting.

## Financial & Administrative

**Insurance**
A third-party payer contract that provides coverage for medical services. Insurance types include private commercial plans, Medicare (federal), Medicaid (state), and TRICARE (military). Each insurance plan has specific coverage policies, prior authorization requirements, and cost-sharing structures.

**Prior Authorization**
The process of obtaining advance approval from an insurance payer before certain services, treatments, or medications can be provided. Authorization requirements vary by payer, procedure, and medical necessity criteria.

**Claim**
A formal request for payment submitted to an insurance payer for services rendered to an insured patient. Claims include procedure codes (CPT/HCPCS), diagnosis codes (ICD-10), modifiers, and charges. Claims may be submitted on a fee-for-service or bundled payment basis.

**Explanation of Benefits (EOB)**
A document from the insurance payer explaining what services were covered, what portion was paid to the provider, and what financial responsibility remains for the patient (deductibles, copayments, coinsurance).

**Coordination of Benefits (COB)**
The process of determining which insurance plan pays first when a patient is covered by multiple payers. Rules are governed by state law and contract terms.

## Scheduling & Access

**Appointment**
A scheduled encounter between a patient and a provider for clinical services. Appointments can be in-person office visits, telehealth consultations, or procedural sessions. Status types include scheduled, confirmed, checked-in, in-progress, completed, canceled, and no-show.

**Appointment Type**
The classification of an appointment based on purpose, duration, and resource requirements. Types include new patient evaluation, established patient follow-up, annual wellness visit, procedure, and imaging.

**Patient Access**
The functional area responsible for scheduling, registration, insurance verification, pre-certification, and financial counseling. Patient Access departments are often the first point of contact for patients entering the healthcare system.

## Clinical Workflows

**Clinical Documentation**
The creation and maintenance of electronic health record entries reflecting patient care, clinical decision-making, and treatment plans. Documentation must meet regulatory standards for completeness, accuracy, and timeliness.

**Care Coordination**
The deliberate organization of patient care activities between multiple participants involved in a patient's care to facilitate appropriate delivery of healthcare services. Coordination includes transitions of care, specialist referrals, and post-acute planning.

**Transitions of Care**
The movement of patients between healthcare settings, locations, or levels of care. Critical transition points include admission, transfer between units, discharge to post-acute facilities, and home health referral.

## Data Quality & Integrity

**Data Governance**
The policies, processes, and standards ensuring high-quality data throughout its lifecycle. Governance includes data stewardship, quality metrics, privacy protocols, and audit trails.

**Historization**
The practice of maintaining time-bounded versions of data records to capture state changes over time. Effective dating (valid_from, valid_to) allows reconstruction of historical states for auditing and clinical review.

**Soft Delete**
A logical deletion mechanism where records are marked as inactive rather than physically removed. Soft deletes preserve audit trails and allow recovery of accidentally deleted records.

## Regulatory & Privacy

**HIPAA (Health Insurance Portability and Accountability Act)**
Federal legislation regulating the use and disclosure of Protected Health Information (PHI). HIPAA establishes national standards for privacy, security, and breach notification.

**Protected Health Information (PHI)**
Individually identifiable health information transmitted or maintained in electronic, paper, or oral forms. PHI includes demographic data, medical histories, test results, and insurance information.

**Minimum Necessary Standard**
The HIPAA principle that only the minimum amount of PHI necessary to accomplish the intended purpose should be used, disclosed, or requested.

**Patient Privacy Rights**
Under HIPAA, patients have rights to access their medical records, request amendments, obtain an accounting of disclosures, and request restrictions on certain uses and disclosures of their information.

## Billing & Revenue Cycle

**Charge Capture**
The process of recording services and procedures for billing purposes. Charges must be captured at the time of service and linked to appropriate billing codes.

**Claim Scrubbing**
Automated validation of claims against payer-specific rules, coding guidelines, and regulatory requirements before submission. Scrubbing reduces claim rejections and denials.

**Denial Management**
The systematic process of tracking, analyzing, and appealing claim denials from payers. Effective denial management identifies root causes and implements corrective actions.

**Revenue Cycle Management**
The administrative and clinical functions that contribute to the capture, management, and collection of patient service revenue. The cycle spans from patient scheduling through final payment collection.

## Quality & Performance

**Clinical Quality Measures**
Standardized metrics assessing the quality of care delivered across specific conditions and procedures. Examples include readmission rates, mortality rates, complication rates, and adherence to evidence-based guidelines.

**Value-Based Care**
Payment models that reward healthcare providers for delivering high-quality, cost-efficient care rather than volume of services. Models include Accountable Care Organizations (ACOs) and bundled payments.

**Population Health**
The health outcomes of a group of individuals, including the distribution of such outcomes within the group. Population health management focuses on improving outcomes for defined patient panels through preventive care and chronic disease management.