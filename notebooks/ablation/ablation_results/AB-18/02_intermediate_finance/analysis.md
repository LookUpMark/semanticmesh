# AB-18 — 02_intermediate_finance — Run Analysis

**Timestamp:** 2026-03-31 16:35:59  
**Run tag:** `v5`

## Configuration

| Parameter | Value |
|-----------|-------|
| Extraction model | `LLM (gpt-5.4-nano-2026-03-17)` |
| Reasoning model | `gpt-5.4-2026-03-05` |
| Embedding model | `BAAI/bge-m3` |
| Retrieval mode | `hybrid` |
| Reranker | `True` |
| Reranker top_k | `12` |
| Chunk size / overlap | `256 / 32` |
| ER similarity threshold | `0.75` |

## Builder Results

| Metric | Value |
|--------|-------|
| Triplets extracted | 596 |
| Entities resolved | 235 |
| Tables parsed | 8 |
| Tables completed | 8 |

## Query Evaluation Summary

| Metric | Value |
|--------|-------|
| Questions | 25 |
| Grounded | **25/25 (100%)** |
| Avg GT Coverage | 100% |
| Avg Top Score | 0.2714 |
| Avg Chunk Count | 11.8 |
| Abstained | 0 |

## RAGAS Metrics

RAGAS evaluation not enabled for this run.

## Per-Question Deep Dive

### ✅ 1 — What is a checking account?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.6477 | **Gate:** `proceed`

**Expected answer:**
> A checking account is one of five account types (Checking, Savings, MoneyMarket, CD, Investment) defined by the CHECK constraint on the accounts table. According to the business glossary, accounts are financial arrangements for deposit, withdrawal, and management of funds. The schema tracks current_…

**System answer:**
> The retrieved context does not provide a separate definition for “checking account” specifically. From the `accounts` table and the `Account` business glossary, a checking account is an `Account` whose `account_type` is `Checking`.

An `Account` is defined as a financial arrangement between a customer and the bank that allows deposit, withdrawal, and management of funds. Accounts are the primary v…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_7`, `parent_chunk_data_dictionary.md_8`, `parent_chunk_data_dictionary.md_9`, `parent_chunk_data_dictionary.md_10`, `parent_chunk_data_dictionary.md_12`, `parent_chunk_data_dictionary.md_11`, `parent_chunk_business_glossary.md_0`, `parent_chunk_business_glossary.md_1`

**Context previews (first 3):**

1. _## accounts  **Description: ** Deposit account master table supporting multiple account types (checking, savings, money market, CD, investment). Implements parent-child hierarchy for portfolio aggrega…_

2. _## customer_account  **Description: ** Junction table implementing many-to-many relationship between customers and accounts. Supports joint ownership, authorized signers, and custodial relationships. …_

3. _## transactions  **Description: ** Transaction fact table recording all account activity. Supports multiple transaction types including debits, credits, transfers, and withdrawals. Tracks calculated f…_

---

### ✅ 2 — What is the difference between a savings account and a money market account?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.6601 | **Gate:** `proceed`

**Expected answer:**
> Both savings and money market are account types defined in the accounts table CHECK constraint. The business glossary Interest section provides example rates: Standard Savings earns 0.25% APY (with monthly compounding), Premium Savings earns 0.50% APY (with daily compounding), while Money Market ear…

**System answer:**
> From the retrieved context, both savings accounts and money market accounts are treated as deposit account types in the `accounts` table: `account_type` can be `Savings` or `MoneyMarket`.

The context does not provide a business definition or rule that distinguishes a savings account from a money market account specifically. What it does say is that accounts in general share attributes such as cur…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_7`, `parent_chunk_data_dictionary.md_10`, `parent_chunk_data_dictionary.md_9`, `parent_chunk_data_dictionary.md_8`, `parent_chunk_data_dictionary.md_12`, `parent_chunk_data_dictionary.md_11`, `parent_chunk_data_dictionary.md_6`, `parent_chunk_business_glossary.md_0`

**Context previews (first 3):**

1. _## accounts  **Description: ** Deposit account master table supporting multiple account types (checking, savings, money market, CD, investment). Implements parent-child hierarchy for portfolio aggrega…_

2. _## loans  **Description: ** Loan portfolio table tracking all lending products including mortgages, personal loans, auto loans, HELOCs, and credit cards. Records original terms, amortization schedules…_

3. _## transactions  **Description: ** Transaction fact table recording all account activity. Supports multiple transaction types including debits, credits, transfers, and withdrawals. Tracks calculated f…_

---

### ✅ 3 — What is APR versus APY?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.9609 | **Gate:** `proceed`

**Expected answer:**
> APR (Annual Percentage Rate) is the annual cost of a loan including interest and fees, used for loan products. APY (Annual Percentage Yield) is the effective annual rate including compounding effects for deposit products. APY is higher than the nominal rate when compounding is more frequent than ann…

**System answer:**
> APR is Annual Percentage Rate, and in the context it is the annual percentage measure used for loans. APY is Annual Percentage Yield, and it is the annual percentage measure used for deposits.

From the Interest concept, both are key interest attributes, but they apply to different sides of banking: APR for borrowing and APY for deposit returns. The context also states that APY accounts for compou…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_10`, `parent_chunk_business_glossary.md_2`, `parent_chunk_business_glossary.md_0`, `parent_chunk_business_glossary.md_1`, `parent_chunk_data_dictionary.md_7`, `parent_chunk_data_dictionary.md_11`, `parent_chunk_data_dictionary.md_8`, `parent_chunk_data_dictionary.md_6`

**Context previews (first 3):**

1. _## loans  **Description: ** Loan portfolio table tracking all lending products including mortgages, personal loans, auto loans, HELOCs, and credit cards. Records original terms, amortization schedules…_

2. _## Interest  **Definition: ** The cost of borrowing money (paid by borrower) or the return on depositing money (paid by bank), expressed as an annual percentage rate. **Business Context:** Interest is…_

3. _# Retail Banking Business Glossary  This document defines the core business concepts and terminology used in the retail banking domain.  ---  ## Account  **Definition: ** A financial arrangement betwe…_

---

### ✅ 4 — What is KYC Level 2?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.6105 | **Gate:** `proceed`

**Expected answer:**
> The customers table has a kyc_status column with a CHECK constraint allowing Level1, Level2, and Level3. The business glossary states that Level1 is the minimum requirement for account opening, Level3 is required for high-value accounts and international transfers, and risk_profile determines eligib…

**System answer:**
> The context shows that KYC is a customer compliance attribute in the `customers` table, and the enforced valid KYC levels are `Level1`, `Level2`, and `Level3`. However, it does not define what `Level2` specifically means or how it differs from the other levels. So from the retrieved context, I can say only that KYC Level 2 is one of the allowed customer KYC levels, but its exact business definitio…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_12`, `parent_chunk_data_dictionary.md_7`, `parent_chunk_data_dictionary.md_4`, `parent_chunk_business_glossary.md_0`, `parent_chunk_business_glossary.md_1`, `parent_chunk_data_dictionary.md_5`, `parent_chunk_business_glossary.md_3`, `parent_chunk_data_dictionary.md_8`

**Context previews (first 3):**

1. _## Entity Relationship Summary  **Key Relationships: ** - customers ←→ accounts (many-to-many via customer_account) - accounts → accounts (self-reference for parent-child hierarchy) - accounts → trans…_

2. _## accounts  **Description: ** Deposit account master table supporting multiple account types (checking, savings, money market, CD, investment). Implements parent-child hierarchy for portfolio aggrega…_

3. _# Retail Banking Data Dictionary  This document provides comprehensive schema documentation for the retail banking database, including table structures, column definitions, constraints, and business c…_

---

### ✅ 5 — How does the schema support different account subtypes and their varying requirements?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.1891 | **Gate:** `proceed_with_warning`

**Expected answer:**
> The accounts table has an account_subtype column (VARCHAR 30, nullable) that stores values like Premium or Standard to differentiate within each account_type. Combined with the minimum_balance and monthly_fee columns, each account can have different requirements configured per subtype. The account_t…

**System answer:**
> The schema supports different account subtypes primarily through the `accounts` master table, which uses classification fields instead of separate tables per product. In `accounts`, `account_type` stores the major product category and explicitly supports `Checking`, `Savings`, `MoneyMarket`, `CD`, and `Investment`. It also has an `account_subtype` column for finer-grained variants such as `Premium…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_7`, `parent_chunk_data_dictionary.md_12`, `parent_chunk_data_dictionary.md_8`, `parent_chunk_data_dictionary.md_9`, `parent_chunk_data_dictionary.md_11`, `parent_chunk_data_dictionary.md_10`, `CARDS→ACCOUNTS`, `parent_chunk_business_glossary.md_0`

**Context previews (first 3):**

1. _## accounts  **Description: ** Deposit account master table supporting multiple account types (checking, savings, money market, CD, investment). Implements parent-child hierarchy for portfolio aggrega…_

2. _## Entity Relationship Summary  **Key Relationships: ** - customers ←→ accounts (many-to-many via customer_account) - accounts → accounts (self-reference for parent-child hierarchy) - accounts → trans…_

3. _## customer_account  **Description: ** Junction table implementing many-to-many relationship between customers and accounts. Supports joint ownership, authorized signers, and custodial relationships. …_

---

### ✅ 6 — What types of loan products does the bank offer?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.4020 | **Gate:** `proceed`

**Expected answer:**
> The bank offers five loan types defined by the CHECK constraint on loans.loan_type: (1) Mortgage — secured by real estate, glossary example shows $350,000 at 5.50% APR for 360 months; (2) Personal Loan — unsecured, example $15,000 at 8.50% APR for 48 months; (3) Auto Loan — secured by vehicle, examp…

**System answer:**
> The bank offers these loan products, as shown in the `loans` table and its `loan_type` field: Mortgage, Personal, Auto, HELOC, and CreditCard. The `loans` table description also states the loan portfolio includes mortgages, personal loans, auto loans, HELOCs, and credit cards.

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_10`, `parent_chunk_data_dictionary.md_12`, `parent_chunk_data_dictionary.md_7`, `parent_chunk_data_dictionary.md_9`, `parent_chunk_business_glossary.md_1`, `parent_chunk_business_glossary.md_2`, `parent_chunk_business_glossary.md_0`, `parent_chunk_data_dictionary.md_4`

**Context previews (first 3):**

1. _## loans  **Description: ** Loan portfolio table tracking all lending products including mortgages, personal loans, auto loans, HELOCs, and credit cards. Records original terms, amortization schedules…_

2. _## Entity Relationship Summary  **Key Relationships: ** - customers ←→ accounts (many-to-many via customer_account) - accounts → accounts (self-reference for parent-child hierarchy) - accounts → trans…_

3. _## accounts  **Description: ** Deposit account master table supporting multiple account types (checking, savings, money market, CD, investment). Implements parent-child hierarchy for portfolio aggrega…_

---

### ✅ 7 — What is the daily ATM withdrawal limit for standard customers?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.3743 | **Gate:** `proceed`

**Expected answer:**
> The cards table has an atm_daily_limit column with a default value of $500. The business glossary Card Examples confirm this: a standard Debit Card has a $500 ATM limit, while a Premium Debit card has a $2,000 ATM limit. The daily_limit column (default $3,000) controls POS spending separately. These…

**System answer:**
> The retrieved context does not provide a specific numeric daily ATM withdrawal limit for standard customers.

What it does provide is the schema location for this information: the CARDS table includes an `atm_daily_limit` column, and the card issuance concept explicitly says cards track spending limits and ATM daily limits. Cards are linked to both the customer (`customer_id`) and the account (`ac…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_11`, `Payment card issuance table for debit, credit, and ATM cards→CARDS`, `parent_chunk_data_dictionary.md_6`, `parent_chunk_data_dictionary.md_12`, `parent_chunk_data_dictionary.md_7`, `parent_chunk_data_dictionary.md_8`, `parent_chunk_business_glossary.md_3`, `parent_chunk_business_glossary.md_1`

**Context previews (first 3):**

1. _## cards  **Description: ** Payment card issuance table for debit, credit, and ATM cards. Links cards to both customer and account. Tracks security features (chip, contactless, PIN), spending limits, …_

2. _Business concept 'Payment card issuance table for debit, credit, and ATM cards' is implemented by physical table CARDS (columns: card_id, account_id, customer_id, card_number, card_type, card_network,…_

3. _## atms  **Description: ** ATM locations including branch-attached machines, drive-through ATMs, and standalone units. Tracks cash balances for replenishment scheduling, GPS coordinates for location s…_

---

### ✅ 8 — What is the difference between a parent account and a child account?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.3098 | **Gate:** `proceed`

**Expected answer:**
> The accounts table supports parent-child hierarchies through the parent_account_id self-referencing foreign key, with a CHECK constraint preventing circular references (parent_account_id != account_id). The data dictionary describes this as supporting portfolio aggregation where parent accounts (typ…

**System answer:**
> In the retrieved context, the difference is only defined in terms of the `accounts` table’s self-referencing hierarchy.

A parent account is an `accounts` record that serves as the parent in that hierarchy, while a child account is an `accounts` record linked under another account through that same self-reference. The documented purpose of this hierarchy is portfolio aggregation, and the context s…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_7`, `parent_chunk_data_dictionary.md_12`, `parent_chunk_data_dictionary.md_8`, `parent_chunk_data_dictionary.md_9`, `parent_chunk_data_dictionary.md_11`, `parent_chunk_data_dictionary.md_10`, `CARDS→ACCOUNTS`, `parent_chunk_business_glossary.md_0`

**Context previews (first 3):**

1. _## accounts  **Description: ** Deposit account master table supporting multiple account types (checking, savings, money market, CD, investment). Implements parent-child hierarchy for portfolio aggrega…_

2. _## Entity Relationship Summary  **Key Relationships: ** - customers ←→ accounts (many-to-many via customer_account) - accounts → accounts (self-reference for parent-child hierarchy) - accounts → trans…_

3. _## customer_account  **Description: ** Junction table implementing many-to-many relationship between customers and accounts. Supports joint ownership, authorized signers, and custodial relationships. …_

---

### ✅ 9 — What does the status 'Frozen' mean for a card?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0630 | **Gate:** `proceed_with_warning`

**Expected answer:**
> The cards table has a status column with four states defined by CHECK constraint: Active, Frozen, Blocked, and Expired. The business glossary states that lost or stolen cards must be immediately blocked to prevent fraud, and that expired cards are automatically renewed. The glossary distinguishes Fr…

**System answer:**
> The retrieved context shows that the `cards` / `CARDS` table has a `status` column, but it does not define the meaning of the specific card status value `Frozen`.

The only place `Frozen` appears in the provided context is for the business concept Account, where account status includes `Active, Dormant, Frozen, Closed`. That definition applies to accounts, not cards.

So, from the available contex…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_7`, `parent_chunk_data_dictionary.md_10`, `parent_chunk_data_dictionary.md_11`, `parent_chunk_data_dictionary.md_6`, `parent_chunk_data_dictionary.md_9`, `Payment card issuance table for debit, credit, and ATM cards→CARDS`, `parent_chunk_business_glossary.md_0`, `parent_chunk_business_glossary.md_3`

**Context previews (first 3):**

1. _## accounts  **Description: ** Deposit account master table supporting multiple account types (checking, savings, money market, CD, investment). Implements parent-child hierarchy for portfolio aggrega…_

2. _## loans  **Description: ** Loan portfolio table tracking all lending products including mortgages, personal loans, auto loans, HELOCs, and credit cards. Records original terms, amortization schedules…_

3. _## cards  **Description: ** Payment card issuance table for debit, credit, and ATM cards. Links cards to both customer and account. Tracks security features (chip, contactless, PIN), spending limits, …_

---

### ✅ 10 — How does the transactions table track the impact of each transaction on account balances?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.7230 | **Gate:** `proceed`

**Expected answer:**
> The transactions table includes a balance_after column (DECIMAL 15,2) that records the account balance after each transaction is applied. Combined with the amount column, transaction_type (Debit/Credit/Transfer/Payment/Withdrawal/Deposit/Fee), and status (Pending/Posted/Failed/Cancelled/OnHold), thi…

**System answer:**
> The `transactions` table tracks balance impact primarily by storing each transaction against an `account_id` and recording a calculated `balance_after` value for the account after that transaction. The table is described as a transaction fact table recording all account activity, and it supports transaction types including `Debit`, `Credit`, `Transfer`, `Payment`, `Withdrawal`, `Deposit`, and `Fee…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_9`, `parent_chunk_data_dictionary.md_7`, `parent_chunk_data_dictionary.md_10`, `CARDS→ACCOUNTS`, `parent_chunk_data_dictionary.md_12`, `parent_chunk_data_dictionary.md_11`, `parent_chunk_data_dictionary.md_8`, `CARDS→CUSTOMERS`

**Context previews (first 3):**

1. _## transactions  **Description: ** Transaction fact table recording all account activity. Supports multiple transaction types including debits, credits, transfers, and withdrawals. Tracks calculated f…_

2. _## accounts  **Description: ** Deposit account master table supporting multiple account types (checking, savings, money market, CD, investment). Implements parent-child hierarchy for portfolio aggrega…_

3. _## loans  **Description: ** Loan portfolio table tracking all lending products including mortgages, personal loans, auto loans, HELOCs, and credit cards. Records original terms, amortization schedules…_

---

### ✅ 11 — How does the customer_account junction table support multiple ownership types?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.9865 | **Gate:** `proceed`

**Expected answer:**
> The customer_account table implements a many-to-many relationship between customers and accounts with a composite primary key (customer_id, account_id). It supports four relationship types via CHECK constraint: Owner, JointOwner, AuthorizedSigner, and Custodian. The is_primary flag designates the pr…

**System answer:**
> The `customer_account` table supports multiple ownership types by implementing the many-to-many relationship between `customers` and `accounts`. This means a single customer can be linked to multiple accounts, and a single account can be linked to multiple customers.

It supports specific ownership and access arrangements through the `relationship_type` column, which can store:
`Owner`, `JointOwne…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_8`, `parent_chunk_data_dictionary.md_12`, `parent_chunk_data_dictionary.md_7`, `parent_chunk_data_dictionary.md_9`, `parent_chunk_data_dictionary.md_11`, `parent_chunk_business_glossary.md_1`, `CARDS→CUSTOMERS`, `parent_chunk_data_dictionary.md_10`

**Context previews (first 3):**

1. _## customer_account  **Description: ** Junction table implementing many-to-many relationship between customers and accounts. Supports joint ownership, authorized signers, and custodial relationships. …_

2. _## Entity Relationship Summary  **Key Relationships: ** - customers ←→ accounts (many-to-many via customer_account) - accounts → accounts (self-reference for parent-child hierarchy) - accounts → trans…_

3. _## accounts  **Description: ** Deposit account master table supporting multiple account types (checking, savings, money market, CD, investment). Implements parent-child hierarchy for portfolio aggrega…_

---

### ✅ 12 — What is the difference between current_balance and available_balance in the accounts table?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.8328 | **Gate:** `proceed`

**Expected answer:**
> The accounts table tracks two separate balance fields: current_balance includes all transactions including pending ones, while available_balance excludes holds and pending transactions and represents what the customer can actually withdraw. The business glossary confirms this distinction, stating th…

**System answer:**
> Based on the retrieved context, I can only say that `current_balance` and `available_balance` are distinct balance-related account attributes in the `Account` business concept and the `accounts` table is described as tracking balances.

The context does not explicitly define `current_balance` separately from `available_balance`, and it does not state the exact calculation or business meaning of th…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_7`, `parent_chunk_data_dictionary.md_10`, `parent_chunk_data_dictionary.md_6`, `parent_chunk_data_dictionary.md_9`, `parent_chunk_data_dictionary.md_8`, `CARDS→ACCOUNTS`, `parent_chunk_data_dictionary.md_12`, `parent_chunk_data_dictionary.md_11`

**Context previews (first 3):**

1. _## accounts  **Description: ** Deposit account master table supporting multiple account types (checking, savings, money market, CD, investment). Implements parent-child hierarchy for portfolio aggrega…_

2. _## loans  **Description: ** Loan portfolio table tracking all lending products including mortgages, personal loans, auto loans, HELOCs, and credit cards. Records original terms, amortization schedules…_

3. _## atms  **Description: ** ATM locations including branch-attached machines, drive-through ATMs, and standalone units. Tracks cash balances for replenishment scheduling, GPS coordinates for location s…_

---

### ✅ 13 — How are loans linked to both customers and accounts in the schema?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0012 | **Gate:** `proceed_with_warning`

**Expected answer:**
> The loans table has a customer_id foreign key referencing the customers table (the borrower) and an optional account_id foreign key referencing the accounts table (for linked payment accounts). Each loan belongs to exactly one customer, and can optionally be connected to an account for automatic pay…

**System answer:**
> I cannot determine how loans are linked to customers and accounts from the retrieved context.

What is known from the context is that it describes a healthcare schema, including tables such as PATIENTS, CLAIMS, PROVIDERS, TREATMENTS, DIAGNOSES, APPOINTMENTS, MEDICATIONS, and LAB_RESULTS, plus healthcare business glossary terms. The context does not include any LOANS table, CUSTOMERS table, ACCOUNT…

**Sources retrieved (11):** `parent_chunk_data_dictionary.md_10`, `parent_chunk_data_dictionary.md_3`, `parent_chunk_business_glossary.md_0`, `parent_chunk_business_glossary.md_1`, `parent_chunk_business_glossary.md_2`, `parent_chunk_data_dictionary.md_8`, `parent_chunk_data_dictionary.md_5`, `parent_chunk_data_dictionary.md_4`

**Context previews (first 3):**

1. _## CLAIMS Table **Purpose**: Store insurance claims and billing information for services rendered. | Column Name | Data Type | Constraint | Description | |-------------|-----------|------------|------…_

2. _# Data Dictionary - Advanced Healthcare Management System  ## Database Overview **Database Name**: `advanced_healthcare_db` **Schema Version**: `3.2.1` **Environment**: Production **Last Updated**: 20…_

3. _# Business Glossary - Advanced Healthcare Management System ## Patient Management **Patient** An individual receiving medical care, treatment, or services from the healthcare organization. Each patien…_

---

### ✅ 14 — What types of transactions does the system support and how does their status lifecycle work?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0048 | **Gate:** `proceed_with_warning`

**Expected answer:**
> The transactions table supports seven transaction types via CHECK constraint: Debit, Credit, Transfer, Payment, Withdrawal, Deposit, and Fee. Each transaction also has a status lifecycle with five states: Pending (initial default), Posted (final), Failed, Cancelled, and OnHold. The business glossary…

**System answer:**
> The retrieved context does not define a single generic “transaction” entity, but it does show the main transaction-like records the system supports at the schema and business-process level.

Operational transactions supported by the schema include appointments in `APPOINTMENTS`, insurance claims in `CLAIMS`, treatments/procedures in `TREATMENTS`, medications in `MEDICATIONS`, diagnoses in `DIAGNOS…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_10`, `parent_chunk_data_dictionary.md_11`, `parent_chunk_business_glossary.md_0`, `parent_chunk_business_glossary.md_1`, `parent_chunk_data_dictionary.md_3`, `parent_chunk_data_dictionary.md_8`, `parent_chunk_data_dictionary.md_9`, `parent_chunk_data_dictionary.md_5`

**Context previews (first 3):**

1. _## CLAIMS Table **Purpose**: Store insurance claims and billing information for services rendered. | Column Name | Data Type | Constraint | Description | |-------------|-----------|------------|------…_

2. _## General Conventions  ### Temporal Validity Pattern All major tables use `valid_from` and `valid_to` timestamps for historization: - Current records have `valid_to = NULL` - Historical records have …_

3. _# Business Glossary - Advanced Healthcare Management System ## Patient Management **Patient** An individual receiving medical care, treatment, or services from the healthcare organization. Each patien…_

---

### ✅ 15 — How does the schema support joint account ownership between multiple customers?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0006 | **Gate:** `proceed_with_warning`

**Expected answer:**
> Joint ownership is implemented through the customer_account junction table, which creates a many-to-many relationship between customers and accounts. Each row has a relationship_type CHECK constraint allowing Owner, JointOwner, AuthorizedSigner, or Custodian. The ownership_percentage field (DECIMAL …

**System answer:**
> The retrieved context does not provide enough information to answer how the schema supports joint account ownership between multiple customers.

What is known from the context is that the schema shown is for an Advanced Healthcare Management System, with tables such as `PATIENTS`, `CLAIMS`, `PROVIDERS`, `DIAGNOSES`, `APPOINTMENTS`, `TREATMENTS`, `MEDICATIONS`, and `LAB_RESULTS`. The relationships …

**Sources retrieved (11):** `parent_chunk_data_dictionary.md_10`, `parent_chunk_business_glossary.md_0`, `parent_chunk_business_glossary.md_1`, `parent_chunk_data_dictionary.md_8`, `parent_chunk_business_glossary.md_2`, `parent_chunk_data_dictionary.md_4`, `parent_chunk_data_dictionary.md_3`, `parent_chunk_data_dictionary.md_9`

**Context previews (first 3):**

1. _## CLAIMS Table **Purpose**: Store insurance claims and billing information for services rendered. | Column Name | Data Type | Constraint | Description | |-------------|-----------|------------|------…_

2. _# Business Glossary - Advanced Healthcare Management System ## Patient Management **Patient** An individual receiving medical care, treatment, or services from the healthcare organization. Each patien…_

3. _## Financial & Administrative **Insurance** A third-party payer contract that provides coverage for medical services. Insurance types include private commercial plans, Medicare (federal), Medicaid (st…_

---

### ✅ 16 — What information does the cards table track and how are cards linked to customers and accounts?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0048 | **Gate:** `proceed_with_warning`

**Expected answer:**
> The cards table links to both accounts (account_id FK) and customers (customer_id FK), tracking card_type (Debit/Credit/ATM), card_network (Visa/Mastercard/Discover/AmericanExpress), card_number, cardholder name, expiration_date, and CVV. For spending controls it stores credit_limit (nullable, for c…

**System answer:**
> I cannot determine that from the retrieved context.

The context provided is for an Advanced Healthcare Management System and includes metadata for tables such as `patients`, `claims`, `medications`, `providers`, `diagnoses`, `appointments`, `treatments`, and `lab_results`, plus glossary definitions for healthcare and insurance concepts. It does not include a `cards` table, a `customers` table, or…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_10`, `parent_chunk_data_dictionary.md_11`, `parent_chunk_data_dictionary.md_3`, `parent_chunk_business_glossary.md_0`, `parent_chunk_data_dictionary.md_6`, `parent_chunk_data_dictionary.md_8`, `parent_chunk_data_dictionary.md_4`, `parent_chunk_data_dictionary.md_9`

**Context previews (first 3):**

1. _## CLAIMS Table **Purpose**: Store insurance claims and billing information for services rendered. | Column Name | Data Type | Constraint | Description | |-------------|-----------|------------|------…_

2. _## General Conventions  ### Temporal Validity Pattern All major tables use `valid_from` and `valid_to` timestamps for historization: - Current records have `valid_to = NULL` - Historical records have …_

3. _# Data Dictionary - Advanced Healthcare Management System  ## Database Overview **Database Name**: `advanced_healthcare_db` **Schema Version**: `3.2.1` **Environment**: Production **Last Updated**: 20…_

---

### ✅ 17 — How does the schema handle interest rates across deposit and loan products?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0009 | **Gate:** `proceed_with_warning`

**Expected answer:**
> Interest rates are stored differently for deposits and loans. The accounts table has an interest_rate column (nullable DECIMAL 5,4) and interest_earned for year-to-date tracking. The loans table has its own interest_rate column representing APR. The business glossary explains that APR (Annual Percen…

**System answer:**
> The retrieved context does not contain enough information to answer how the schema handles interest rates across deposit and loan products.

What is known from the context is that it describes an Advanced Healthcare Management System schema, including healthcare-focused tables such as `patients`, `providers`, `appointments`, `diagnoses`, `treatments`, `medications`, `lab_results`, and `claims`, pl…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_11`, `parent_chunk_data_dictionary.md_10`, `parent_chunk_data_dictionary.md_3`, `parent_chunk_business_glossary.md_0`, `parent_chunk_business_glossary.md_1`, `parent_chunk_data_dictionary.md_8`, `parent_chunk_business_glossary.md_2`, `parent_chunk_data_dictionary.md_9`

**Context previews (first 3):**

1. _## General Conventions  ### Temporal Validity Pattern All major tables use `valid_from` and `valid_to` timestamps for historization: - Current records have `valid_to = NULL` - Historical records have …_

2. _## CLAIMS Table **Purpose**: Store insurance claims and billing information for services rendered. | Column Name | Data Type | Constraint | Description | |-------------|-----------|------------|------…_

3. _# Data Dictionary - Advanced Healthcare Management System  ## Database Overview **Database Name**: `advanced_healthcare_db` **Schema Version**: `3.2.1` **Environment**: Production **Last Updated**: 20…_

---

### ✅ 18 — What types of branches does the bank operate and how do they differ in capabilities?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0019 | **Gate:** `proceed_with_warning`

**Expected answer:**
> The branches table supports three types via CHECK constraint: FullService, Satellite, and ATMOnly. The business glossary details each: FullService branches offer complete banking services including loan origination, financial advisors, and safe deposit boxes; Satellite branches have limited hours an…

**System answer:**
> I cannot determine what types of bank branches are operated or how their capabilities differ from the retrieved context. The context is about an Advanced Healthcare Management System and includes healthcare-related schema and glossary entries such as PATIENTS, PROVIDERS, APPOINTMENTS, CLAIMS, DIAGNOSES, TREATMENTS, MEDICATIONS, and LAB_RESULTS, plus healthcare business concepts like insurance, cla…

**Sources retrieved (11):** `parent_chunk_data_dictionary.md_10`, `parent_chunk_business_glossary.md_0`, `parent_chunk_data_dictionary.md_8`, `parent_chunk_data_dictionary.md_3`, `parent_chunk_data_dictionary.md_9`, `parent_chunk_business_glossary.md_1`, `parent_chunk_data_dictionary.md_4`, `parent_chunk_data_dictionary.md_6`

**Context previews (first 3):**

1. _## CLAIMS Table **Purpose**: Store insurance claims and billing information for services rendered. | Column Name | Data Type | Constraint | Description | |-------------|-----------|------------|------…_

2. _# Business Glossary - Advanced Healthcare Management System ## Patient Management **Patient** An individual receiving medical care, treatment, or services from the healthcare organization. Each patien…_

3. _## PROVIDERS Table **Purpose**: Store healthcare provider information and credentials. | Column Name | Data Type | Constraint | Description | |-------------|-----------|------------|-------------| | p…_

---

### ✅ 19 — How are ATMs related to branches in the schema and what types of ATMs exist?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0011 | **Gate:** `proceed_with_warning`

**Expected answer:**
> The atms table has an optional branch_id foreign key referencing branches. When branch_id is NULL, the ATM is standalone and not affiliated with any branch. ATM types are defined by CHECK constraint: Branch (on-premises), DriveThrough (vehicle-accessible), and Standalone (independent locations). Eac…

**System answer:**
> I cannot find this information in the knowledge graph.

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_11`, `parent_chunk_data_dictionary.md_10`, `parent_chunk_business_glossary.md_0`, `parent_chunk_data_dictionary.md_3`, `parent_chunk_business_glossary.md_2`, `parent_chunk_data_dictionary.md_5`, `parent_chunk_data_dictionary.md_6`, `parent_chunk_data_dictionary.md_8`

**Context previews (first 3):**

1. _## General Conventions  ### Temporal Validity Pattern All major tables use `valid_from` and `valid_to` timestamps for historization: - Current records have `valid_to = NULL` - Historical records have …_

2. _## CLAIMS Table **Purpose**: Store insurance claims and billing information for services rendered. | Column Name | Data Type | Constraint | Description | |-------------|-----------|------------|------…_

3. _# Business Glossary - Advanced Healthcare Management System ## Patient Management **Patient** An individual receiving medical care, treatment, or services from the healthcare organization. Each patien…_

---

### ✅ 20 — What is the lifecycle of a loan from application to completion?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0011 | **Gate:** `proceed_with_warning`

**Expected answer:**
> The loans table tracks loan status through five states defined by CHECK constraint: Pending (application submitted, default), Approved (credit approved but not yet funded), Active (loan funded and being repaid), PaidOff (fully repaid), and Defaulted (borrower failed to repay). Each loan records orig…

**System answer:**
> I cannot find this information in the knowledge graph.

**Sources retrieved (12):** `parent_chunk_business_glossary.md_1`, `parent_chunk_data_dictionary.md_10`, `parent_chunk_data_dictionary.md_11`, `parent_chunk_business_glossary.md_0`, `parent_chunk_data_dictionary.md_9`, `parent_chunk_data_dictionary.md_5`, `parent_chunk_data_dictionary.md_8`, `parent_chunk_business_glossary.md_2`

**Context previews (first 3):**

1. _## Financial & Administrative **Insurance** A third-party payer contract that provides coverage for medical services. Insurance types include private commercial plans, Medicare (federal), Medicaid (st…_

2. _## CLAIMS Table **Purpose**: Store insurance claims and billing information for services rendered. | Column Name | Data Type | Constraint | Description | |-------------|-----------|------------|------…_

3. _## General Conventions  ### Temporal Validity Pattern All major tables use `valid_from` and `valid_to` timestamps for historization: - Current records have `valid_to = NULL` - Historical records have …_

---

### ✅ 21 — What does preferred customer status mean and how is it tracked in the schema?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0020 | **Gate:** `proceed_with_warning`

**Expected answer:**
> Preferred status is tracked via the is_preferred boolean flag in the customers table (default: false). The business glossary states that preferred customers receive waived fees, preferred interest rates, and priority service. The glossary examples show preferred customers with longer tenure and high…

**System answer:**
> I cannot determine “preferred customer status” from the retrieved context.

What is known from the context is that this is a healthcare schema (`advanced_healthcare_db`) centered on entities such as `PATIENTS`, `APPOINTMENTS`, `TREATMENTS`, `DIAGNOSES`, `MEDICATIONS`, `CLAIMS`, and `PROVIDERS`. The business glossary defines healthcare concepts like Patient, Appointment, Claim, Insurance, Diagnosis…

**Sources retrieved (10):** `parent_chunk_data_dictionary.md_10`, `parent_chunk_data_dictionary.md_3`, `parent_chunk_data_dictionary.md_5`, `parent_chunk_data_dictionary.md_9`, `parent_chunk_business_glossary.md_0`, `parent_chunk_data_dictionary.md_8`, `parent_chunk_business_glossary.md_2`, `parent_chunk_business_glossary.md_1`

**Context previews (first 3):**

1. _## CLAIMS Table **Purpose**: Store insurance claims and billing information for services rendered. | Column Name | Data Type | Constraint | Description | |-------------|-----------|------------|------…_

2. _# Data Dictionary - Advanced Healthcare Management System  ## Database Overview **Database Name**: `advanced_healthcare_db` **Schema Version**: `3.2.1` **Environment**: Production **Last Updated**: 20…_

3. _## TREATMENTS Table **Purpose**: Store medical treatments and procedures performed on patients. | Column Name | Data Type | Constraint | Description | |-------------|-----------|------------|---------…_

---

### ✅ 22 — How does the accounts table support interest tracking and what business rules govern interest?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0017 | **Gate:** `proceed_with_warning`

**Expected answer:**
> The accounts table has interest_rate (nullable DECIMAL for the annual rate) and interest_earned (DECIMAL for year-to-date interest credited). The business glossary states that deposit interest is credited monthly (typically the first day of the month) and that APY accounts for compounding effects. P…

**System answer:**
> I cannot determine how an `accounts` table supports interest tracking or what business rules govern interest from the retrieved context.

What is present in the context is healthcare schema and glossary information for tables such as `patients`, `claims`, `diagnoses`, `treatments`, `medications`, `providers`, `appointments`, and `lab_results`, plus general data-governance conventions like `valid_f…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_10`, `parent_chunk_data_dictionary.md_11`, `parent_chunk_business_glossary.md_2`, `parent_chunk_data_dictionary.md_4`, `parent_chunk_business_glossary.md_0`, `parent_chunk_business_glossary.md_1`, `parent_chunk_data_dictionary.md_3`, `parent_chunk_data_dictionary.md_5`

**Context previews (first 3):**

1. _## CLAIMS Table **Purpose**: Store insurance claims and billing information for services rendered. | Column Name | Data Type | Constraint | Description | |-------------|-----------|------------|------…_

2. _## General Conventions  ### Temporal Validity Pattern All major tables use `valid_from` and `valid_to` timestamps for historization: - Current records have `valid_to = NULL` - Historical records have …_

3. _## Billing & Revenue Cycle **Charge Capture** The process of recording services and procedures for billing purposes. Charges must be captured at the time of service and linked to appropriate billing c…_

---

### ✅ 23 — Can an account exist without any customer linked to it?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0011 | **Gate:** `proceed_with_warning`

**Expected answer:**
> Looking at the schema, there is no database-level constraint that forces every account to have a customer_account row. The accounts table has no direct foreign key to customers — the relationship is through the customer_account junction table with a composite primary key (customer_id, account_id). H…

**System answer:**
> The retrieved context is insufficient to determine that. It contains healthcare concepts and tables such as PATIENTS, APPOINTMENTS, DIAGNOSES, TREATMENTS, MEDICATIONS, CLAIMS, and PROVIDERS, but it does not mention an ACCOUNT entity, a CUSTOMER entity, or any relationship between them. Based on the provided context alone, I cannot tell whether an account can exist without a linked customer.

**Sources retrieved (12):** `parent_chunk_business_glossary.md_0`, `parent_chunk_data_dictionary.md_9`, `parent_chunk_business_glossary.md_2`, `parent_chunk_data_dictionary.md_4`, `parent_chunk_business_glossary.md_1`, `parent_chunk_data_dictionary.md_5`, `parent_chunk_data_dictionary.md_10`, `Patient Demographics→PATIENTS`

**Context previews (first 3):**

1. _# Business Glossary - Advanced Healthcare Management System ## Patient Management **Patient** An individual receiving medical care, treatment, or services from the healthcare organization. Each patien…_

2. _## APPOINTMENTS Table **Purpose**: Store patient appointment scheduling and encounter information. | Column Name | Data Type | Constraint | Description | |-------------|-----------|------------|------…_

3. _## Billing & Revenue Cycle **Charge Capture** The process of recording services and procedures for billing purposes. Charges must be captured at the time of service and linked to appropriate billing c…_

---

### ✅ 24 — How does the schema handle failed or cancelled transactions?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0039 | **Gate:** `proceed_with_warning`

**Expected answer:**
> The transactions table has a status column with CHECK constraint allowing Pending, Posted, Failed, Cancelled, and OnHold states. The business glossary explains that failed transactions are logged for audit but do not affect the account balance — the balance_after field would reflect no change. Poste…

**System answer:**
> The retrieved context does not show a general `transactions` table or any explicit schema pattern for “failed” transactions.

What it does show is that the schema handles record lifecycle generically through two cross-table patterns. First, all major tables use historization with `valid_from` and `valid_to`: current records have `valid_to = NULL`, historical versions have non-`NULL` `valid_to`, an…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_10`, `parent_chunk_data_dictionary.md_11`, `parent_chunk_data_dictionary.md_5`, `parent_chunk_data_dictionary.md_3`, `parent_chunk_data_dictionary.md_9`, `parent_chunk_business_glossary.md_1`, `parent_chunk_business_glossary.md_0`, `parent_chunk_data_dictionary.md_6`

**Context previews (first 3):**

1. _## CLAIMS Table **Purpose**: Store insurance claims and billing information for services rendered. | Column Name | Data Type | Constraint | Description | |-------------|-----------|------------|------…_

2. _## General Conventions  ### Temporal Validity Pattern All major tables use `valid_from` and `valid_to` timestamps for historization: - Current records have `valid_to = NULL` - Historical records have …_

3. _## TREATMENTS Table **Purpose**: Store medical treatments and procedures performed on patients. | Column Name | Data Type | Constraint | Description | |-------------|-----------|------------|---------…_

---

### ✅ 25 — What operational states can an ATM have and what do they mean for available services?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0011 | **Gate:** `proceed_with_warning`

**Expected answer:**
> ATMs have three operational states defined by CHECK constraint: Operational (fully functional for all supported transactions), OutOfService (technical issue preventing all transactions), and OutOfCash (cash depleted, preventing withdrawals). The business glossary explains that cash replenishment is …

**System answer:**
> I cannot determine ATM operational states or what they mean for available services from the retrieved context.

What is known from the context is that it describes an Advanced Healthcare Management System: healthcare business concepts such as Patient, Diagnosis, Treatment, Medication, Claim, Insurance, and Appointment, along with tables such as `patients`, `appointments`, `providers`, `diagnoses`,…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_11`, `parent_chunk_data_dictionary.md_10`, `parent_chunk_business_glossary.md_0`, `parent_chunk_data_dictionary.md_3`, `parent_chunk_business_glossary.md_2`, `parent_chunk_data_dictionary.md_6`, `parent_chunk_data_dictionary.md_5`, `parent_chunk_data_dictionary.md_8`

**Context previews (first 3):**

1. _## General Conventions  ### Temporal Validity Pattern All major tables use `valid_from` and `valid_to` timestamps for historization: - Current records have `valid_to = NULL` - Historical records have …_

2. _## CLAIMS Table **Purpose**: Store insurance claims and billing information for services rendered. | Column Name | Data Type | Constraint | Description | |-------------|-----------|------------|------…_

3. _# Business Glossary - Advanced Healthcare Management System ## Patient Management **Patient** An individual receiving medical care, treatment, or services from the healthcare organization. Each patien…_

---

## Anomalies & Observations

No anomalies detected. All questions grounded with acceptable RAGAS scores.
