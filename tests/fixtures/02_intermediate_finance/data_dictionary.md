# Retail Banking Data Dictionary

This document provides comprehensive schema documentation for the retail banking database, including table structures, column definitions, constraints, and business concept mappings.

---

## customers

**Description:** Core customer dimension table containing master data for all individual and corporate banking customers. Includes KYC (Know Your Customer) compliance status, risk profiling for investment suitability, and preferred customer flags for VIP treatment.

**Primary Key:** `customer_id` (INTEGER, auto-increment)

**Column Details:**

| Column | Type | Description | Nullable |
|--------|------|-------------|----------|
| customer_id | INTEGER | Unique customer identifier (primary key) | NO |
| first_name | VARCHAR(50) | Customer's first name | NO |
| last_name | VARCHAR(50) | Customer's last name | NO |
| tax_id | VARCHAR(11) | Tax identification number (SSN/EIN), must be unique | NO |
| email | VARCHAR(100) | Primary email address for notifications | NO |
| phone | VARCHAR(20) | Primary phone number | YES |
| address | VARCHAR(200) | Street address | NO |
| city | VARCHAR(50) | City of residence | NO |
| state | VARCHAR(2) | Two-letter state code | NO |
| zip_code | VARCHAR(10) | ZIP or postal code | NO |
| kyc_status | VARCHAR(20) | KYC verification level: Level1/Level2/Level3 | NO |
| risk_profile | VARCHAR(20) | Investment risk tolerance: Conservative/Moderate/Aggressive | NO |
| customer_since | DATE | Date customer relationship began | NO |
| is_preferred | BOOLEAN | VIP flag for fee waivers and priority service | NO |
| created_at | TIMESTAMP | Record creation timestamp | NO |
| updated_at | TIMESTAMP | Record last modification timestamp | NO |

**Default Values:**
- kyc_status: 'Level1'
- risk_profile: 'Moderate'
- customer_since: CURRENT_DATE
- is_preferred: 0 (false)
- created_at: CURRENT_TIMESTAMP
- updated_at: CURRENT_TIMESTAMP

**Constraints:**
- CHECK (kyc_status IN ('Level1', 'Level2', 'Level3'))
- CHECK (risk_profile IN ('Conservative', 'Moderate', 'Aggressive'))
- UNIQUE (tax_id)

**Indexes:**
- idx_customers_tax_id ON (tax_id)
- idx_customers_name ON (last_name, first_name)
- idx_customers_kyc ON (kyc_status)

**Business Concept Mapping:** Maps to **Customer** business glossary concept

---

## branches

**Description:** Physical bank locations including full-service branches, satellite offices, and ATM-only locations. Tracks staffing levels, operating hours, ATM counts, and branch status for operational management.

**Primary Key:** `branch_id` (INTEGER, auto-increment)

**Column Details:**

| Column | Type | Description | Nullable |
|--------|------|-------------|----------|
| branch_id | INTEGER | Unique branch identifier (primary key) | NO |
| branch_code | VARCHAR(4) | 4-digit branch code, must be unique | NO |
| branch_name | VARCHAR(100) | Human-readable branch name | NO |
| branch_type | VARCHAR(20) | Type: FullService/Satellite/ATMOnly | NO |
| address | VARCHAR(200) | Street address | NO |
| city | VARCHAR(50) | City where branch is located | NO |
| state | VARCHAR(2) | Two-letter state code | NO |
| zip_code | VARCHAR(10) | ZIP or postal code | NO |
| phone | VARCHAR(20) | Branch phone number | YES |
| hours | VARCHAR(100) | Operating hours (e.g., "Mon-Fri 9AM-5PM") | YES |
| atm_count | INTEGER | Number of ATMs at this branch | NO |
| teller_count | INTEGER | Number of teller stations | NO |
| manager_name | VARCHAR(100) | Name of branch manager | YES |
| opened_date | DATE | Date branch opened | NO |
| status | VARCHAR(20) | Current status: Active/TemporarilyClosed/PermanentlyClosed | NO |
| created_at | TIMESTAMP | Record creation timestamp | NO |

**Default Values:**
- atm_count: 0
- teller_count: 0
- opened_date: CURRENT_DATE
- status: 'Active'
- created_at: CURRENT_TIMESTAMP

**Constraints:**
- CHECK (branch_type IN ('FullService', 'Satellite', 'ATMOnly'))
- CHECK (status IN ('Active', 'TemporarilyClosed', 'PermanentlyClosed'))
- UNIQUE (branch_code)

**Indexes:**
- idx_branches_code ON (branch_code)
- idx_branches_type ON (branch_type)
- idx_branches_city ON (city, state)

**Business Concept Mapping:** Maps to **Branch** business glossary concept

---

## atms

**Description:** ATM locations including branch-attached machines, drive-through ATMs, and standalone units. Tracks cash balances for replenishment scheduling, GPS coordinates for location services, and operational status for availability management.

**Primary Key:** `atm_id` (INTEGER, auto-increment)

**Column Details:**

| Column | Type | Description | Nullable |
|--------|------|-------------|----------|
| atm_id | INTEGER | Unique ATM identifier (primary key) | NO |
| atm_code | VARCHAR(10) | Unique ATM code | NO |
| branch_id | INTEGER | Foreign key to branches (NULL for standalone) | YES |
| location | VARCHAR(200) | Human-readable location description | NO |
| latitude | DECIMAL(10,6) | GPS latitude coordinate | YES |
| longitude | DECIMAL(11,6) | GPS longitude coordinate | YES |
| atm_type | VARCHAR(20) | Type: Standalone/Branch/DriveThrough | NO |
| status | VARCHAR(20) | Status: Operational/OutOfService/OutOfCash | NO |
| cash_balance | DECIMAL(12,2) | Current cash on hand | YES |
| last_replenished | TIMESTAMP | Last cash replenishment timestamp | YES |
| supports_deposit | BOOLEAN | Whether ATM accepts deposits | NO |
| supports_cardless | BOOLEAN | Whether ATM supports mobile/cardless withdrawals | NO |
| installed_date | DATE | Date ATM was installed | NO |
| created_at | TIMESTAMP | Record creation timestamp | NO |

**Default Values:**
- status: 'Operational'
- supports_deposit: 1 (true)
- supports_cardless: 0 (false)
- installed_date: CURRENT_DATE
- created_at: CURRENT_TIMESTAMP

**Constraints:**
- CHECK (atm_type IN ('Standalone', 'Branch', 'DriveThrough'))
- CHECK (status IN ('Operational', 'OutOfService', 'OutOfCash'))
- UNIQUE (atm_code)
- FOREIGN KEY (branch_id) REFERENCES branches(branch_id)

**Indexes:**
- idx_atms_branch ON (branch_id)
- idx_atms_status ON (status)
- idx_atms_location ON (location)

**Business Concept Mapping:** Maps to **ATM** business glossary concept

---

## accounts

**Description:** Deposit account master table supporting multiple account types (checking, savings, money market, CD, investment). Implements parent-child hierarchy for portfolio aggregation (investment accounts contain child accounts). Tracks balances, interest accrual, fees, and account lifecycle status.

**Primary Key:** `account_id` (INTEGER, auto-increment)

**Column Details:**

| Column | Type | Description | Nullable |
|--------|------|-------------|----------|
| account_id | INTEGER | Unique account identifier (primary key) | NO |
| account_number | VARCHAR(16) | Human-readable account number, must be unique | NO |
| account_type | VARCHAR(20) | Type: Checking/Savings/MoneyMarket/CD/Investment | NO |
| account_subtype | VARCHAR(30) | Subtype (e.g., Premium, Student, Standard) | YES |
| parent_account_id | INTEGER | Parent account for hierarchy (NULL for top-level) | YES |
| branch_id | INTEGER | Foreign key to branches (home branch) | YES |
| status | VARCHAR(20) | Status: Active/Dormant/Frozen/Closed | NO |
| current_balance | DECIMAL(15,2) | Current balance including pending transactions | NO |
| available_balance | DECIMAL(15,2) | Balance available for withdrawal (excludes holds) | NO |
| interest_rate | DECIMAL(5,4) | Annual interest rate (NULL for non-interest accounts) | YES |
| interest_earned | DECIMAL(15,2) | Year-to-date interest earned | NO |
| minimum_balance | DECIMAL(15,2) | Required minimum balance to avoid fees | NO |
| monthly_fee | DECIMAL(10,2) | Monthly maintenance fee | NO |
| opened_date | DATE | Account open date | NO |
| closed_date | DATE | Account close date (NULL if active) | YES |
| last_transaction_date | TIMESTAMP | Timestamp of last transaction | YES |
| created_at | TIMESTAMP | Record creation timestamp | NO |
| updated_at | TIMESTAMP | Record last modification timestamp | NO |

**Default Values:**
- status: 'Active'
- current_balance: 0.00
- available_balance: 0.00
- interest_earned: 0.00
- minimum_balance: 0.00
- monthly_fee: 0.00
- opened_date: CURRENT_DATE
- created_at: CURRENT_TIMESTAMP
- updated_at: CURRENT_TIMESTAMP

**Constraints:**
- CHECK (account_type IN ('Checking', 'Savings', 'MoneyMarket', 'CD', 'Investment'))
- CHECK (status IN ('Active', 'Dormant', 'Frozen', 'Closed'))
- CHECK (parent_account_id != account_id) -- No self-reference
- UNIQUE (account_number)
- FOREIGN KEY (parent_account_id) REFERENCES accounts(account_id)
- FOREIGN KEY (branch_id) REFERENCES branches(branch_id)

**Indexes:**
- idx_accounts_type ON (account_type)
- idx_accounts_status ON (status)
- idx_accounts_parent ON (parent_account_id)
- idx_accounts_branch ON (branch_id)
- idx_accounts_balance ON (current_balance)

**Business Concept Mapping:** Maps to **Account** business glossary concept

---

## customer_account

**Description:** Junction table implementing many-to-many relationship between customers and accounts. Supports joint ownership, authorized signers, and custodial relationships. Tracks ownership percentages and primary owner designation for billing and legal purposes.

**Primary Key:** Composite (`customer_id`, `account_id`)

**Column Details:**

| Column | Type | Description | Nullable |
|--------|------|-------------|----------|
| customer_id | INTEGER | Foreign key to customers (part of PK) | NO |
| account_id | INTEGER | Foreign key to accounts (part of PK) | NO |
| relationship_type | VARCHAR(20) | Relationship: Owner/JointOwner/AuthorizedSigner/Custodian | NO |
| is_primary | BOOLEAN | Whether this is the primary owner | NO |
| ownership_percentage | DECIMAL(5,2) | Percentage ownership (0.00-100.00) | NO |
| linked_date | DATE | Date relationship was established | NO |
| unlinked_date | DATE | Date relationship was terminated | YES |
| created_at | TIMESTAMP | Record creation timestamp | NO |

**Default Values:**
- relationship_type: 'Owner'
- is_primary: 0 (false)
- ownership_percentage: 100.00
- linked_date: CURRENT_DATE
- created_at: CURRENT_TIMESTAMP

**Constraints:**
- CHECK (relationship_type IN ('Owner', 'JointOwner', 'AuthorizedSigner', 'Custodian'))
- PRIMARY KEY (customer_id, account_id)
- FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
- FOREIGN KEY (account_id) REFERENCES accounts(account_id)

**Indexes:**
- idx_customer_account_customer ON (customer_id)
- idx_customer_account_account ON (account_id)
- idx_customer_account_role ON (relationship_type)
- idx_customer_account_primary ON (is_primary, customer_id)

**Business Concept Mapping:** Maps to **Customer** and **Account** relationship

---

## transactions

**Description:** Transaction fact table recording all account activity. Supports multiple transaction types including debits, credits, transfers, and withdrawals. Tracks calculated fields (balance_after) and includes location data for POS and ATM transactions for fraud detection.

**Primary Key:** `transaction_id` (INTEGER, auto-increment)

**Column Details:**

| Column | Type | Description | Nullable |
|--------|------|-------------|----------|
| transaction_id | INTEGER | Unique transaction identifier (primary key) | NO |
| account_id | INTEGER | Foreign key to accounts | NO |
| transaction_type | VARCHAR(20) | Type: Debit/Credit/Transfer/Payment/Withdrawal/Deposit/Fee | NO |
| amount | DECIMAL(15,2) | Transaction amount (always positive) | NO |
| currency | VARCHAR(3) | Currency code (default: USD) | NO |
| transaction_date | TIMESTAMP | When transaction occurred | NO |
| status | VARCHAR(20) | Status: Pending/Posted/Failed/Cancelled/OnHold | NO |
| balance_after | DECIMAL(15,2) | Account balance after transaction | YES |
| description | VARCHAR(200) | Human-readable transaction description | YES |
| reference_number | VARCHAR(50) | Reference code for reconciliation | YES |
| external_account | VARCHAR(30) | External account involved (transfers) | YES |
| location | VARCHAR(100) | Location where transaction occurred | YES |
| created_at | TIMESTAMP | Record creation timestamp | NO |

**Default Values:**
- currency: 'USD'
- transaction_date: CURRENT_TIMESTAMP
- status: 'Pending'
- created_at: CURRENT_TIMESTAMP

**Constraints:**
- CHECK (transaction_type IN ('Debit', 'Credit', 'Transfer', 'Payment', 'Withdrawal', 'Deposit', 'Fee'))
- CHECK (status IN ('Pending', 'Posted', 'Failed', 'Cancelled', 'OnHold'))
- FOREIGN KEY (account_id) REFERENCES accounts(account_id)

**Indexes:**
- idx_transactions_account ON (account_id)
- idx_transactions_date ON (transaction_date)
- idx_transactions_type ON (transaction_type)
- idx_transactions_status ON (status)
- idx_transactions_account_date ON (account_id, transaction_date DESC)

**Business Concept Mapping:** Maps to **Transaction** business glossary concept

---

## loans

**Description:** Loan portfolio table tracking all lending products including mortgages, personal loans, auto loans, HELOCs, and credit cards. Records original terms, amortization schedules, current balances, and maturity dates for loan servicing and portfolio management.

**Primary Key:** `loan_id` (INTEGER, auto-increment)

**Column Details:**

| Column | Type | Description | Nullable |
|--------|------|-------------|----------|
| loan_id | INTEGER | Unique loan identifier (primary key) | NO |
| customer_id | INTEGER | Foreign key to customers (borrower) | NO |
| loan_type | VARCHAR(20) | Type: Mortgage/Personal/Auto/HELOC/CreditCard | NO |
| account_id | INTEGER | Foreign key to accounts (optional, for linked accounts) | YES |
| principal_amount | DECIMAL(15,2) | Original loan principal | NO |
| interest_rate | DECIMAL(5,4) | Annual interest rate (APR) | NO |
| term_months | INTEGER | Loan term in months (0 for revolving credit) | NO |
| monthly_payment | DECIMAL(10,2) | Required monthly payment | NO |
| balance_due | DECIMAL(15,2) | Current outstanding balance | NO |
| origination_date | DATE | Date loan was originated | NO |
| maturity_date | DATE | Date loan is scheduled to be paid off | NO |
| status | VARCHAR(20) | Status: Pending/Approved/Active/PaidOff/Defaulted | NO |
| created_at | TIMESTAMP | Record creation timestamp | NO |

**Default Values:**
- status: 'Pending'
- created_at: CURRENT_TIMESTAMP

**Constraints:**
- CHECK (loan_type IN ('Mortgage', 'Personal', 'Auto', 'HELOC', 'CreditCard'))
- CHECK (status IN ('Pending', 'Approved', 'Active', 'PaidOff', 'Defaulted'))
- FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
- FOREIGN KEY (account_id) REFERENCES accounts(account_id)

**Indexes:**
- idx_loans_customer ON (customer_id)
- idx_loans_account ON (account_id)
- idx_loans_type ON (loan_type)
- idx_loans_status ON (status)
- idx_loans_maturity ON (maturity_date)

**Business Concept Mapping:** Maps to **Loan** and **Interest** business glossary concepts

---

## cards

**Description:** Payment card issuance table for debit, credit, and ATM cards. Links cards to both customer and account. Tracks security features (chip, contactless, PIN), spending limits, and card status. Supports multiple networks (Visa, Mastercard, Discover, American Express).

**Primary Key:** `card_id` (INTEGER, auto-increment)

**Column Details:**

| Column | Type | Description | Nullable |
|--------|------|-------------|----------|
| card_id | INTEGER | Unique card identifier (primary key) | NO |
| account_id | INTEGER | Foreign key to accounts (linked account) | NO |
| customer_id | INTEGER | Foreign key to customers (cardholder) | NO |
| card_number | VARCHAR(20) | Primary Account Number (PAN), must be unique | NO |
| card_type | VARCHAR(20) | Type: Debit/Credit/ATM | NO |
| card_network | VARCHAR(20) | Network: Visa/Mastercard/Discover/AmericanExpress | NO |
| card_name | VARCHAR(50) | Cardholder name as printed on card | NO |
| expiration_date | VARCHAR(5) | Expiration date (MM/YY format) | NO |
| cvv | VARCHAR(4) | Card Verification Value (security code) | NO |
| credit_limit | DECIMAL(12,2) | Credit limit (NULL for debit cards) | YES |
| daily_limit | DECIMAL(10,2) | Maximum daily POS spending | NO |
| atm_daily_limit | DECIMAL(10,2) | Maximum daily ATM withdrawal | NO |
| pin_set | BOOLEAN | Whether PIN has been set by customer | NO |
| has_chip | BOOLEAN | Whether card has EMV chip | NO |
| contactless_enabled | BOOLEAN | Whether tap-to-pay is enabled | NO |
| status | VARCHAR(20) | Status: Active/Frozen/Blocked/Expired | NO |
| issued_date | DATE | Date card was issued | NO |
| last_used_date | TIMESTAMP | Timestamp of last transaction | YES |
| created_at | TIMESTAMP | Record creation timestamp | NO |

**Default Values:**
- daily_limit: 3000.00
- atm_daily_limit: 500.00
- pin_set: 0 (false)
- has_chip: 1 (true)
- contactless_enabled: 1 (true)
- status: 'Active'
- issued_date: CURRENT_DATE
- created_at: CURRENT_TIMESTAMP

**Constraints:**
- CHECK (card_type IN ('Debit', 'Credit', 'ATM'))
- CHECK (card_network IN ('Visa', 'Mastercard', 'Discover', 'AmericanExpress'))
- CHECK (status IN ('Active', 'Frozen', 'Blocked', 'Expired'))
- UNIQUE (card_number)
- FOREIGN KEY (account_id) REFERENCES accounts(account_id)
- FOREIGN KEY (customer_id) REFERENCES customers(customer_id)

**Indexes:**
- idx_cards_account ON (account_id)
- idx_cards_customer ON (customer_id)
- idx_cards_number ON (card_number)
- idx_cards_status ON (status)

**Business Concept Mapping:** Maps to **Card** business glossary concept

---

## Entity Relationship Summary

**Key Relationships:**
- customers ←→ accounts (many-to-many via customer_account)
- accounts → accounts (self-reference for parent-child hierarchy)
- accounts → transactions (one-to-many)
- customers → loans (one-to-many)
- accounts → cards (one-to-many)
- branches → accounts (one-to-many)
- branches → atms (one-to-many)

**Cascade Rules:**
- All foreign keys have NO CASCADE by default (manual integrity management)
- customer_account junction table requires both customer and account to exist

**Business Rules Enforced:**
- Account numbers must be unique
- Tax IDs must be unique
- Branch codes must be unique
- ATM codes must be unique
- Card numbers must be unique
- Account hierarchy prevents circular references (parent != child)
- KYC levels must be Level1, Level2, or Level3
- Risk profiles must be Conservative, Moderate, or Aggressive

---

**Document Version:** 1.0
**Last Updated:** 2024-02-15
**Database:** Retail Banking Schema (Intermediate Complexity)
**Table Count:** 8
**Total Columns:** 143 (across all tables)
