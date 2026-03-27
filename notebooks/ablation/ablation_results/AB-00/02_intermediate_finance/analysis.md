# AB-00 — 02_intermediate_finance — Run Analysis

**Timestamp:** 2026-03-27 15:11:27  
**Run tag:** `post-fix-v2`

## Configuration

| Parameter | Value |
|-----------|-------|
| Extraction model | `LLM (gpt-5.4-nano-2026-03-17)` |
| Reasoning model | `gpt-5.4-nano-2026-03-17` |
| Embedding model | `BAAI/bge-m3` |
| Retrieval mode | `hybrid` |
| Reranker | `True` |
| Reranker top_k | `12` |
| Chunk size / overlap | `256 / 32` |
| ER similarity threshold | `0.75` |

## Builder Results

| Metric | Value |
|--------|-------|
| Triplets extracted | 588 |
| Entities resolved | 221 |
| Tables parsed | 7 |
| Tables completed | 7 |

## Query Evaluation Summary

| Metric | Value |
|--------|-------|
| Questions | 25 |
| Grounded | **25/25 (100%)** |
| Avg GT Coverage | 100% |
| Avg Top Score | 0.4981 |
| Avg Chunk Count | 12.0 |
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
> A checking account is an account where `account_type` in the `accounts` table has the value “Checking” (the schema notes `account_type` can be one of: Checking/Savings/MoneyMarket/CD/Investment). Checking accounts are deposit account types tracked in `accounts` along with balances (e.g., `current_balance` and `available_balance`), interest fields, fees (e.g., `monthly_fee`), and lifecycle status.

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_7`, `parent_chunk_data_dictionary.md_8`, `Account Balances and Status→ACCOUNTS`, `parent_chunk_data_dictionary.md_9`, `parent_chunk_data_dictionary.md_10`, `parent_chunk_business_glossary.md_0`, `parent_chunk_business_glossary.md_1`, `parent_chunk_business_glossary.md_2`

**Context previews (first 3):**

1. _## accounts  **Description: ** Deposit account master table supporting multiple account types (checking, savings, money market, CD, investment). Implements parent-child hierarchy for portfolio aggrega…_

2. _## customer_account  **Description: ** Junction table implementing many-to-many relationship between customers and accounts. Supports joint ownership, authorized signers, and custodial relationships. …_

3. _Business concept 'Account Balances and Status' — The table is a master record for deposit accounts and includes current/available balances, interest rate and interest earned, recurring fee fields, and…_

---

### ✅ 2 — What is the difference between a savings account and a money market account?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.6601 | **Gate:** `proceed`

**Expected answer:**
> Both savings and money market are account types defined in the accounts table CHECK constraint. The business glossary Interest section provides example rates: Standard Savings earns 0.25% APY (with monthly compounding), Premium Savings earns 0.50% APY (with daily compounding), while Money Market ear…

**System answer:**
> In the provided knowledge graph, the `accounts` table classifies deposit accounts by `account_type`, which includes both `Savings` and `MoneyMarket`. However, the context does not define any business differences between a Savings account and a Money Market account beyond them being different values of `account_type` (and optional `account_subtype`).

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_7`, `parent_chunk_data_dictionary.md_10`, `parent_chunk_data_dictionary.md_9`, `Account Balances and Status→ACCOUNTS`, `parent_chunk_data_dictionary.md_8`, `parent_chunk_data_dictionary.md_12`, `parent_chunk_data_dictionary.md_11`, `parent_chunk_business_glossary.md_0`

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
> APR (Annual Percentage Rate) and APY (Annual Percentage Yield) are both “interest rate” measures described under the business concept **Interest**. APR is the annual percentage rate for interest on loans (paid by the borrower), while APY is the annual percentage yield used for deposits and accounts for compounding (APY reflects the effect of compounding, whereas APR is the annual rate concept).

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_10`, `parent_chunk_business_glossary.md_2`, `parent_chunk_business_glossary.md_0`, `parent_chunk_business_glossary.md_1`, `parent_chunk_data_dictionary.md_7`, `parent_chunk_data_dictionary.md_11`, `parent_chunk_data_dictionary.md_8`, `Account Balances and Status→ACCOUNTS`

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
> The retrieved context only states that KYC levels must be one of **Level1, Level2, or Level3** (from the Entity Relationship Summary). It also indicates that the **Bank Customer** concept is implemented in the **`CUSTOMERS`** table with a **`kyc_status`** field that stores KYC verification status.

However, the context does **not** provide what **“KYC Level 2”** specifically means (e.g., the crite…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_12`, `Bank Customer→CUSTOMERS`, `parent_chunk_data_dictionary.md_7`, `parent_chunk_data_dictionary.md_4`, `parent_chunk_business_glossary.md_0`, `Bank Customer`, `parent_chunk_business_glossary.md_1`, `parent_chunk_data_dictionary.md_5`

**Context previews (first 3):**

1. _## Entity Relationship Summary  **Key Relationships: ** - customers ←→ accounts (many-to-many via customer_account) - accounts → accounts (self-reference for parent-child hierarchy) - accounts → trans…_

2. _Business concept 'Bank Customer' — The table defines a core customer master record (customer_id, personal details, tax_id, contact info, and address) and includes KYC verification and risk profiling f…_

3. _## accounts  **Description: ** Deposit account master table supporting multiple account types (checking, savings, money market, CD, investment). Implements parent-child hierarchy for portfolio aggrega…_

---

### ✅ 5 — How does the schema support different account subtypes and their varying requirements?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.1891 | **Gate:** `proceed_with_warning`

**Expected answer:**
> The accounts table has an account_subtype column (VARCHAR 30, nullable) that stores values like Premium or Standard to differentiate within each account_type. Combined with the minimum_balance and monthly_fee columns, each account can have different requirements configured per subtype. The account_t…

**System answer:**
> The schema supports different account subtypes by recording a subtype value directly on each account in the `accounts` table via the `account_subtype` column (e.g., “Premium, Student, Standard”). 

For requirements, the `accounts` table stores the requirement-related fields at the account level—specifically `minimum_balance` and `monthly_fee`—alongside other account-level balance, fee, and lifecyc…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_7`, `parent_chunk_data_dictionary.md_12`, `Account Balances and Status→ACCOUNTS`, `parent_chunk_data_dictionary.md_8`, `parent_chunk_data_dictionary.md_9`, `parent_chunk_data_dictionary.md_11`, `parent_chunk_business_glossary.md_0`, `parent_chunk_data_dictionary.md_4`

**Context previews (first 3):**

1. _## accounts  **Description: ** Deposit account master table supporting multiple account types (checking, savings, money market, CD, investment). Implements parent-child hierarchy for portfolio aggrega…_

2. _## Entity Relationship Summary  **Key Relationships: ** - customers ←→ accounts (many-to-many via customer_account) - accounts → accounts (self-reference for parent-child hierarchy) - accounts → trans…_

3. _Business concept 'Account Balances and Status' — The table is a master record for deposit accounts and includes current/available balances, interest rate and interest earned, recurring fee fields, and…_

---

### ✅ 6 — What types of loan products does the bank offer?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.6931 | **Gate:** `proceed`

**Expected answer:**
> The bank offers five loan types defined by the CHECK constraint on loans.loan_type: (1) Mortgage — secured by real estate, glossary example shows $350,000 at 5.50% APR for 360 months; (2) Personal Loan — unsecured, example $15,000 at 8.50% APR for 48 months; (3) Auto Loan — secured by vehicle, examp…

**System answer:**
> The bank offers loan products including mortgages, personal loans, auto loans, HELOCs, and credit cards, as described by the business concept implemented by the physical table LOANS (column `loan_type`).

**Sources retrieved (12):** `Loan portfolio table tracking all lending products including mortgages, personal loans, auto loans, HELOCs, and credit cards→LOANS`, `parent_chunk_data_dictionary.md_10`, `parent_chunk_data_dictionary.md_12`, `parent_chunk_data_dictionary.md_7`, `Bank Customer→CUSTOMERS`, `LOANS→CUSTOMERS`, `Loan portfolio table tracking all lending products including mortgages, personal loans, auto loans, HELOCs, and credit cards`, `parent_chunk_business_glossary.md_1`

**Context previews (first 3):**

1. _Business concept 'Loan portfolio table tracking all lending products including mortgages, personal loans, auto loans, HELOCs, and credit cards' is implemented by physical table LOANS (columns: loan_id…_

2. _## loans  **Description: ** Loan portfolio table tracking all lending products including mortgages, personal loans, auto loans, HELOCs, and credit cards. Records original terms, amortization schedules…_

3. _## Entity Relationship Summary  **Key Relationships: ** - customers ←→ accounts (many-to-many via customer_account) - accounts → accounts (self-reference for parent-child hierarchy) - accounts → trans…_

---

### ✅ 7 — What is the daily ATM withdrawal limit for standard customers?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.3743 | **Gate:** `proceed`

**Expected answer:**
> The cards table has an atm_daily_limit column with a default value of $500. The business glossary Card Examples confirm this: a standard Debit Card has a $500 ATM limit, while a Premium Debit card has a $2,000 ATM limit. The daily_limit column (default $3,000) controls POS spending separately. These…

**System answer:**
> I cannot find this information in the knowledge graph.

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_11`, `parent_chunk_data_dictionary.md_6`, `parent_chunk_data_dictionary.md_12`, `parent_chunk_data_dictionary.md_7`, `ATM Location→ATMS`, `Branch service locations→BRANCHES`, `parent_chunk_business_glossary.md_3`, `parent_chunk_business_glossary.md_1`

**Context previews (first 3):**

1. _## cards  **Description: ** Payment card issuance table for debit, credit, and ATM cards. Links cards to both customer and account. Tracks security features (chip, contactless, PIN), spending limits, …_

2. _## atms  **Description: ** ATM locations including branch-attached machines, drive-through ATMs, and standalone units. Tracks cash balances for replenishment scheduling, GPS coordinates for location s…_

3. _## Entity Relationship Summary  **Key Relationships: ** - customers ←→ accounts (many-to-many via customer_account) - accounts → accounts (self-reference for parent-child hierarchy) - accounts → trans…_

---

### ✅ 8 — What is the difference between a parent account and a child account?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.3098 | **Gate:** `proceed`

**Expected answer:**
> The accounts table supports parent-child hierarchies through the parent_account_id self-referencing foreign key, with a CHECK constraint preventing circular references (parent_account_id != account_id). The data dictionary describes this as supporting portfolio aggregation where parent accounts (typ…

**System answer:**
> In the `accounts` table, a “parent account” and “child account” are distinguished by the self-referencing hierarchy:

A parent account is an account that other accounts roll up under for portfolio aggregation—specifically, “investment accounts contain child accounts.” This is represented by the `parent_account_id` field in the `accounts` table (a foreign key reference back to `accounts.account_id`…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_7`, `parent_chunk_data_dictionary.md_12`, `ACCOUNTS→ACCOUNTS`, `Account Balances and Status→ACCOUNTS`, `parent_chunk_data_dictionary.md_8`, `parent_chunk_data_dictionary.md_9`, `parent_chunk_data_dictionary.md_11`, `parent_chunk_data_dictionary.md_10`

**Context previews (first 3):**

1. _## accounts  **Description: ** Deposit account master table supporting multiple account types (checking, savings, money market, CD, investment). Implements parent-child hierarchy for portfolio aggrega…_

2. _## Entity Relationship Summary  **Key Relationships: ** - customers ←→ accounts (many-to-many via customer_account) - accounts → accounts (self-reference for parent-child hierarchy) - accounts → trans…_

3. _Relationship: ACCOUNTS references ACCOUNTS via foreign key PARENT_ACCOUNT_ID -> ACCOUNTS.ACCOUNT_ID.…_

---

### ✅ 9 — What does the status 'Frozen' mean for a card?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0630 | **Gate:** `proceed_with_warning`

**Expected answer:**
> The cards table has a status column with four states defined by CHECK constraint: Active, Frozen, Blocked, and Expired. The business glossary states that lost or stolen cards must be immediately blocked to prevent fraud, and that expired cards are automatically renewed. The glossary distinguishes Fr…

**System answer:**
> In the provided context, “Frozen” is defined as an Account Status value (see the **Account** business concept: “Account Status (Active, Dormant, Frozen, Closed)”). 

The **cards** table description says it “tracks … card status,” but the context does not define any card status values or explain what a card status of “Frozen” would mean.

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_7`, `parent_chunk_data_dictionary.md_10`, `parent_chunk_data_dictionary.md_11`, `parent_chunk_data_dictionary.md_6`, `parent_chunk_data_dictionary.md_9`, `ATM Location→ATMS`, `parent_chunk_business_glossary.md_0`, `parent_chunk_business_glossary.md_3`

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
> The `transactions` table tracks the impact on account balances using the calculated field `balance_after` (“Tracks calculated fields (balance_after)”) alongside the transaction details that determine the balance movement, such as `transaction_type`, `amount`, `currency`, and the transaction timing/status (`transaction_date`, `status`). The business concept for “Financial Transaction” also describe…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_9`, `TRANSACTIONS→ACCOUNTS`, `Financial Transaction→TRANSACTIONS`, `parent_chunk_data_dictionary.md_7`, `Account Balances and Status→ACCOUNTS`, `ATM Location→ATMS`, `ACCOUNTS→BRANCHES`, `ACCOUNTS→ACCOUNTS`

**Context previews (first 3):**

1. _## transactions  **Description: ** Transaction fact table recording all account activity. Supports multiple transaction types including debits, credits, transfers, and withdrawals. Tracks calculated f…_

2. _Relationship: TRANSACTIONS references ACCOUNTS via foreign key ACCOUNT_ID -> ACCOUNTS.ACCOUNT_ID.…_

3. _Business concept 'Financial Transaction' — The table is explicitly described as a transaction fact table for all account activity and contains the core attributes of a financial transaction: account_i…_

---

### ✅ 11 — How does the customer_account junction table support multiple ownership types?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.9865 | **Gate:** `proceed`

**Expected answer:**
> The customer_account table implements a many-to-many relationship between customers and accounts with a composite primary key (customer_id, account_id). It supports four relationship types via CHECK constraint: Owner, JointOwner, AuthorizedSigner, and Custodian. The is_primary flag designates the pr…

**System answer:**
> The `customer_account` table supports multiple ownership/authorization types by using the `relationship_type` column, which classifies the customer-to-account role. The allowed values are Owner, JointOwner, AuthorizedSigner, and Custodian. This is the core semantic driver for the “Account Relationship Role” business concept, with additional fields `is_primary` (to indicate the primary owner) and `…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_8`, `Account Relationship Role→CUSTOMER_ACCOUNT`, `parent_chunk_data_dictionary.md_12`, `CUSTOMER_ACCOUNT→CUSTOMERS`, `parent_chunk_data_dictionary.md_7`, `CUSTOMER_ACCOUNT→ACCOUNTS`, `parent_chunk_data_dictionary.md_9`, `parent_chunk_data_dictionary.md_11`

**Context previews (first 3):**

1. _## customer_account  **Description: ** Junction table implementing many-to-many relationship between customers and accounts. Supports joint ownership, authorized signers, and custodial relationships. …_

2. _Business concept 'Account Relationship Role' — The table implements the customer-to-account relationship role via relationship_type with values Owner, JointOwner, AuthorizedSigner, and Custodian, whic…_

3. _## Entity Relationship Summary  **Key Relationships: ** - customers ←→ accounts (many-to-many via customer_account) - accounts → accounts (self-reference for parent-child hierarchy) - accounts → trans…_

---

### ✅ 12 — What is the difference between current_balance and available_balance in the accounts table?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.8433 | **Gate:** `proceed`

**Expected answer:**
> The accounts table tracks two separate balance fields: current_balance includes all transactions including pending ones, while available_balance excludes holds and pending transactions and represents what the customer can actually withdraw. The business glossary confirms this distinction, stating th…

**System answer:**
> In the `accounts` table (and its mapped business concept “Account Balances and Status”), `current_balance` and `available_balance` are tracked as separate attributes.

However, the retrieved context does not define what specifically distinguishes them operationally (for example, how holds, pending transactions, or availability rules affect the two). So I can only confirm that the table stores both…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_7`, `Account Balances and Status→ACCOUNTS`, `parent_chunk_data_dictionary.md_10`, `parent_chunk_data_dictionary.md_6`, `Financial Transaction→TRANSACTIONS`, `parent_chunk_data_dictionary.md_9`, `ATM Location→ATMS`, `ACCOUNTS→ACCOUNTS`

**Context previews (first 3):**

1. _## accounts  **Description: ** Deposit account master table supporting multiple account types (checking, savings, money market, CD, investment). Implements parent-child hierarchy for portfolio aggrega…_

2. _Business concept 'Account Balances and Status' — The table is a master record for deposit accounts and includes current/available balances, interest rate and interest earned, recurring fee fields, and…_

3. _## loans  **Description: ** Loan portfolio table tracking all lending products including mortgages, personal loans, auto loans, HELOCs, and credit cards. Records original terms, amortization schedules…_

---

### ✅ 13 — How are loans linked to both customers and accounts in the schema?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.8105 | **Gate:** `proceed`

**Expected answer:**
> The loans table has a customer_id foreign key referencing the customers table (the borrower) and an optional account_id foreign key referencing the accounts table (for linked payment accounts). Each loan belongs to exactly one customer, and can optionally be connected to an account for automatic pay…

**System answer:**
> In the schema, the physical table `LOANS` is linked to both customers and accounts through foreign keys:

`LOANS.customer_id` is a foreign key to `CUSTOMERS.CUSTOMER_ID`, linking each loan to its borrower customer, and `LOANS.account_id` is a foreign key to `ACCOUNTS.ACCOUNT_ID`, which is optional (“optional, for linked accounts”) for associating the loan with an account.

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_12`, `LOANS→CUSTOMERS`, `LOANS→ACCOUNTS`, `parent_chunk_data_dictionary.md_10`, `CUSTOMER_ACCOUNT→CUSTOMERS`, `parent_chunk_data_dictionary.md_8`, `CUSTOMER_ACCOUNT→ACCOUNTS`, `parent_chunk_data_dictionary.md_11`

**Context previews (first 3):**

1. _## Entity Relationship Summary  **Key Relationships: ** - customers ←→ accounts (many-to-many via customer_account) - accounts → accounts (self-reference for parent-child hierarchy) - accounts → trans…_

2. _Relationship: LOANS references CUSTOMERS via foreign key CUSTOMER_ID -> CUSTOMERS.CUSTOMER_ID.…_

3. _Relationship: LOANS references ACCOUNTS via foreign key ACCOUNT_ID -> ACCOUNTS.ACCOUNT_ID.…_

---

### ✅ 14 — What types of transactions does the system support and how does their status lifecycle work?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.3394 | **Gate:** `proceed`

**Expected answer:**
> The transactions table supports seven transaction types via CHECK constraint: Debit, Credit, Transfer, Payment, Withdrawal, Deposit, and Fee. Each transaction also has a status lifecycle with five states: Pending (initial default), Posted (final), Failed, Cancelled, and OnHold. The business glossary…

**System answer:**
> The system supports these transaction types: Debit, Credit, Transfer, Payment, Withdrawal, Deposit, and Fee (from the `transactions.transaction_type` definition in the **transactions** table).

For transaction status lifecycle, the business concept **Transaction** states that transactions “flow through multiple states (Pending → Posted)” and also lists the possible `status` values as: Pending, Pos…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_9`, `parent_chunk_data_dictionary.md_7`, `Account Balances and Status→ACCOUNTS`, `Financial Transaction→TRANSACTIONS`, `ATM Location→ATMS`, `parent_chunk_data_dictionary.md_6`, `Account Balances and Status`, `parent_chunk_business_glossary.md_1`

**Context previews (first 3):**

1. _## transactions  **Description: ** Transaction fact table recording all account activity. Supports multiple transaction types including debits, credits, transfers, and withdrawals. Tracks calculated f…_

2. _## accounts  **Description: ** Deposit account master table supporting multiple account types (checking, savings, money market, CD, investment). Implements parent-child hierarchy for portfolio aggrega…_

3. _Business concept 'Account Balances and Status' — The table is a master record for deposit accounts and includes current/available balances, interest rate and interest earned, recurring fee fields, and…_

---

### ✅ 15 — How does the schema support joint account ownership between multiple customers?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.4870 | **Gate:** `proceed`

**Expected answer:**
> Joint ownership is implemented through the customer_account junction table, which creates a many-to-many relationship between customers and accounts. Each row has a relationship_type CHECK constraint allowing Owner, JointOwner, AuthorizedSigner, or Custodian. The ownership_percentage field (DECIMAL …

**System answer:**
> The schema supports joint account ownership through the many-to-many junction table `customer_account`, which links multiple records from `customers` to a single `accounts` record using the composite primary key (`customer_id`, `account_id`). Joint ownership is represented by entries where `relationship_type` is set to `JointOwner`, and the table also stores `ownership_percentage` for each custome…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_8`, `parent_chunk_data_dictionary.md_12`, `Account Relationship Role→CUSTOMER_ACCOUNT`, `parent_chunk_data_dictionary.md_7`, `parent_chunk_data_dictionary.md_11`, `CUSTOMER_ACCOUNT→CUSTOMERS`, `Account Relationship Role`, `parent_chunk_business_glossary.md_0`

**Context previews (first 3):**

1. _## customer_account  **Description: ** Junction table implementing many-to-many relationship between customers and accounts. Supports joint ownership, authorized signers, and custodial relationships. …_

2. _## Entity Relationship Summary  **Key Relationships: ** - customers ←→ accounts (many-to-many via customer_account) - accounts → accounts (self-reference for parent-child hierarchy) - accounts → trans…_

3. _Business concept 'Account Relationship Role' — The table implements the customer-to-account relationship role via relationship_type with values Owner, JointOwner, AuthorizedSigner, and Custodian, whic…_

---

### ✅ 16 — What information does the cards table track and how are cards linked to customers and accounts?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.9528 | **Gate:** `proceed`

**Expected answer:**
> The cards table links to both accounts (account_id FK) and customers (customer_id FK), tracking card_type (Debit/Credit/ATM), card_network (Visa/Mastercard/Discover/AmericanExpress), card_number, cardholder name, expiration_date, and CVV. For spending controls it stores credit_limit (nullable, for c…

**System answer:**
> The `cards` table is a payment card issuance table for debit, credit, and ATM cards. It tracks the card’s security features (such as chip, contactless, and PIN), spending limits, and card status. It also supports multiple card networks (Visa, Mastercard, Discover, American Express). In addition, it stores the card identifiers including a unique `card_id` and a unique `card_number` (PAN), plus `car…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_11`, `parent_chunk_data_dictionary.md_10`, `CUSTOMER_ACCOUNT→CUSTOMERS`, `CUSTOMER_ACCOUNT→ACCOUNTS`, `parent_chunk_data_dictionary.md_8`, `parent_chunk_data_dictionary.md_12`, `Loan portfolio table tracking all lending products including mortgages, personal loans, auto loans, HELOCs, and credit cards→LOANS`, `ACCOUNTS→ACCOUNTS`

**Context previews (first 3):**

1. _## cards  **Description: ** Payment card issuance table for debit, credit, and ATM cards. Links cards to both customer and account. Tracks security features (chip, contactless, PIN), spending limits, …_

2. _## loans  **Description: ** Loan portfolio table tracking all lending products including mortgages, personal loans, auto loans, HELOCs, and credit cards. Records original terms, amortization schedules…_

3. _Relationship: CUSTOMER_ACCOUNT references CUSTOMERS via foreign key CUSTOMER_ID -> CUSTOMERS.CUSTOMER_ID.…_

---

### ✅ 17 — How does the schema handle interest rates across deposit and loan products?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0574 | **Gate:** `proceed_with_warning`

**Expected answer:**
> Interest rates are stored differently for deposits and loans. The accounts table has an interest_rate column (nullable DECIMAL 5,4) and interest_earned for year-to-date tracking. The loans table has its own interest_rate column representing APR. The business glossary explains that APR (Annual Percen…

**System answer:**
> The schema models interest rates separately for deposit accounts and loans.

For deposit products, the business concept “Account Balances and Status” is implemented by the physical table `ACCOUNTS`, which includes `interest_rate` and `interest_earned` (along with `current_balance` and `available_balance`). The context also notes that deposit interest is credited monthly.

For loan products, the bu…

**Sources retrieved (12):** `Loan portfolio table tracking all lending products including mortgages, personal loans, auto loans, HELOCs, and credit cards→LOANS`, `parent_chunk_data_dictionary.md_12`, `Account Balances and Status→ACCOUNTS`, `parent_chunk_data_dictionary.md_10`, `parent_chunk_data_dictionary.md_7`, `LOANS→CUSTOMERS`, `parent_chunk_business_glossary.md_2`, `Account Balances and Status`

**Context previews (first 3):**

1. _Business concept 'Loan portfolio table tracking all lending products including mortgages, personal loans, auto loans, HELOCs, and credit cards' is implemented by physical table LOANS (columns: loan_id…_

2. _## Entity Relationship Summary  **Key Relationships: ** - customers ←→ accounts (many-to-many via customer_account) - accounts → accounts (self-reference for parent-child hierarchy) - accounts → trans…_

3. _Business concept 'Account Balances and Status' — The table is a master record for deposit accounts and includes current/available balances, interest rate and interest earned, recurring fee fields, and…_

---

### ✅ 18 — What types of branches does the bank operate and how do they differ in capabilities?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.1556 | **Gate:** `proceed_with_warning`

**Expected answer:**
> The branches table supports three types via CHECK constraint: FullService, Satellite, and ATMOnly. The business glossary details each: FullService branches offer complete banking services including loan origination, financial advisors, and safe deposit boxes; Satellite branches have limited hours an…

**System answer:**
> The bank operates three branch types as defined in the `branches` table’s `branch_type`: `FullService`, `Satellite`, and `ATMOnly` (see the `branch_type` column in the `branches` concept/description and table mapping under “Branch service locations” and “branches”).

They differ in capabilities through the operational attributes stored on the branch record: `teller_count` and `atm_count` (staffing…

**Sources retrieved (12):** `Branch service locations→BRANCHES`, `parent_chunk_data_dictionary.md_12`, `parent_chunk_data_dictionary.md_7`, `ATM Location→ATMS`, `parent_chunk_data_dictionary.md_6`, `parent_chunk_data_dictionary.md_5`, `Branch service locations`, `parent_chunk_business_glossary.md_2`

**Context previews (first 3):**

1. _Business concept 'Branch service locations' — The table stores physical location master data for bank branches/ATMs (address, phone, city/state/zip) and operational attributes that characterize servic…_

2. _## Entity Relationship Summary  **Key Relationships: ** - customers ←→ accounts (many-to-many via customer_account) - accounts → accounts (self-reference for parent-child hierarchy) - accounts → trans…_

3. _## accounts  **Description: ** Deposit account master table supporting multiple account types (checking, savings, money market, CD, investment). Implements parent-child hierarchy for portfolio aggrega…_

---

### ✅ 19 — How are ATMs related to branches in the schema and what types of ATMs exist?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.6184 | **Gate:** `proceed`

**Expected answer:**
> The atms table has an optional branch_id foreign key referencing branches. When branch_id is NULL, the ATM is standalone and not affiliated with any branch. ATM types are defined by CHECK constraint: Branch (on-premises), DriveThrough (vehicle-accessible), and Standalone (independent locations). Eac…

**System answer:**
> In the schema, ATMs are related to branches through a foreign key: `ATMS.branch_id` references `BRANCHES.BRANCH_ID` (so a given ATM may be linked to a branch, and the context notes `branch_id` is NULL for standalone ATMs). In addition, the entity relationship summary states `branches → atms` is a one-to-many relationship (one branch can have many ATMs).

The types of ATMs that exist are: Standalon…

**Sources retrieved (12):** `ATMS→BRANCHES`, `parent_chunk_data_dictionary.md_6`, `parent_chunk_data_dictionary.md_12`, `ATM Location→ATMS`, `Branch service locations→BRANCHES`, `parent_chunk_data_dictionary.md_9`, `parent_chunk_business_glossary.md_3`, `Branch service locations`

**Context previews (first 3):**

1. _Relationship: ATMS references BRANCHES via foreign key BRANCH_ID -> BRANCHES.BRANCH_ID.…_

2. _## atms  **Description: ** ATM locations including branch-attached machines, drive-through ATMs, and standalone units. Tracks cash balances for replenishment scheduling, GPS coordinates for location s…_

3. _## Entity Relationship Summary  **Key Relationships: ** - customers ←→ accounts (many-to-many via customer_account) - accounts → accounts (self-reference for parent-child hierarchy) - accounts → trans…_

---

### ✅ 20 — What is the lifecycle of a loan from application to completion?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0067 | **Gate:** `proceed_with_warning`

**Expected answer:**
> The loans table tracks loan status through five states defined by CHECK constraint: Pending (application submitted, default), Approved (credit approved but not yet funded), Active (loan funded and being repaid), PaidOff (fully repaid), and Defaulted (borrower failed to repay). Each loan records orig…

**System answer:**
> I cannot find this information in the knowledge graph.

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_10`, `parent_chunk_data_dictionary.md_7`, `Account Balances and Status→ACCOUNTS`, `Loan portfolio table tracking all lending products including mortgages, personal loans, auto loans, HELOCs, and credit cards→LOANS`, `parent_chunk_data_dictionary.md_12`, `parent_chunk_business_glossary.md_2`, `parent_chunk_business_glossary.md_1`, `Account Balances and Status`

**Context previews (first 3):**

1. _## loans  **Description: ** Loan portfolio table tracking all lending products including mortgages, personal loans, auto loans, HELOCs, and credit cards. Records original terms, amortization schedules…_

2. _## accounts  **Description: ** Deposit account master table supporting multiple account types (checking, savings, money market, CD, investment). Implements parent-child hierarchy for portfolio aggrega…_

3. _Business concept 'Account Balances and Status' — The table is a master record for deposit accounts and includes current/available balances, interest rate and interest earned, recurring fee fields, and…_

---

### ✅ 21 — What does preferred customer status mean and how is it tracked in the schema?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.5129 | **Gate:** `proceed`

**Expected answer:**
> Preferred status is tracked via the is_preferred boolean flag in the customers table (default: false). The business glossary states that preferred customers receive waived fees, preferred interest rates, and priority service. The glossary examples show preferred customers with longer tenure and high…

**System answer:**
> In the schema, “preferred customer status” means the customer has a preferred/VIP flag set for customer treatment. This is tracked in the physical table `CUSTOMERS` by the column `is_preferred` (along with other customer master fields like `kyc_status` and `risk_profile`). The business concept mapping for “Bank Customer” also notes that the presence of the preferred/VIP flag aligns with implementi…

**Sources retrieved (12):** `Bank Customer→CUSTOMERS`, `parent_chunk_data_dictionary.md_12`, `parent_chunk_data_dictionary.md_11`, `parent_chunk_data_dictionary.md_10`, `parent_chunk_data_dictionary.md_8`, `Loan portfolio table tracking all lending products including mortgages, personal loans, auto loans, HELOCs, and credit cards→LOANS`, `parent_chunk_data_dictionary.md_7`, `parent_chunk_data_dictionary.md_4`

**Context previews (first 3):**

1. _Business concept 'Bank Customer' — The table defines a core customer master record (customer_id, personal details, tax_id, contact info, and address) and includes KYC verification and risk profiling f…_

2. _## Entity Relationship Summary  **Key Relationships: ** - customers ←→ accounts (many-to-many via customer_account) - accounts → accounts (self-reference for parent-child hierarchy) - accounts → trans…_

3. _## cards  **Description: ** Payment card issuance table for debit, credit, and ATM cards. Links cards to both customer and account. Tracks security features (chip, contactless, PIN), spending limits, …_

---

### ✅ 22 — How does the accounts table support interest tracking and what business rules govern interest?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.5952 | **Gate:** `proceed`

**Expected answer:**
> The accounts table has interest_rate (nullable DECIMAL for the annual rate) and interest_earned (DECIMAL for year-to-date interest credited). The business glossary states that deposit interest is credited monthly (typically the first day of the month) and that APY accounts for compounding effects. P…

**System answer:**
> The `ACCOUNTS` table supports interest tracking by including both an `interest_rate` field and an `interest_earned` field. In the business concept “Account Balances and Status,” this table is described as a master record for deposit accounts that includes “interest rate and interest earned,” along with current/available balances and related fee and lifecycle status attributes.

The business rules …

**Sources retrieved (12):** `Account Balances and Status→ACCOUNTS`, `parent_chunk_data_dictionary.md_7`, `Loan portfolio table tracking all lending products including mortgages, personal loans, auto loans, HELOCs, and credit cards→LOANS`, `parent_chunk_data_dictionary.md_12`, `parent_chunk_data_dictionary.md_10`, `ACCOUNTS→BRANCHES`, `ACCOUNTS→ACCOUNTS`, `Account Balances and Status`

**Context previews (first 3):**

1. _Business concept 'Account Balances and Status' — The table is a master record for deposit accounts and includes current/available balances, interest rate and interest earned, recurring fee fields, and…_

2. _## accounts  **Description: ** Deposit account master table supporting multiple account types (checking, savings, money market, CD, investment). Implements parent-child hierarchy for portfolio aggrega…_

3. _Business concept 'Loan portfolio table tracking all lending products including mortgages, personal loans, auto loans, HELOCs, and credit cards' is implemented by physical table LOANS (columns: loan_id…_

---

### ✅ 23 — Can an account exist without any customer linked to it?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.1394 | **Gate:** `proceed_with_warning`

**Expected answer:**
> Looking at the schema, there is no database-level constraint that forces every account to have a customer_account row. The accounts table has no direct foreign key to customers — the relationship is through the customer_account junction table with a composite primary key (customer_id, account_id). H…

**System answer:**
> The retrieved context does not state any rule or constraint that an entry in `ACCOUNTS` must have at least one related row in the `CUSTOMER_ACCOUNT` junction table (`customer_account` is described as a many-to-many link between customers and accounts, with FK relationships to `CUSTOMERS` and `ACCOUNTS`). Because the context only provides schema-level metadata (and not a specific “required”/minimum…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_8`, `CUSTOMER_ACCOUNT→CUSTOMERS`, `parent_chunk_data_dictionary.md_12`, `CUSTOMER_ACCOUNT→ACCOUNTS`, `Account Relationship Role→CUSTOMER_ACCOUNT`, `parent_chunk_data_dictionary.md_11`, `parent_chunk_data_dictionary.md_10`, `parent_chunk_business_glossary.md_3`

**Context previews (first 3):**

1. _## customer_account  **Description: ** Junction table implementing many-to-many relationship between customers and accounts. Supports joint ownership, authorized signers, and custodial relationships. …_

2. _Relationship: CUSTOMER_ACCOUNT references CUSTOMERS via foreign key CUSTOMER_ID -> CUSTOMERS.CUSTOMER_ID.…_

3. _## Entity Relationship Summary  **Key Relationships: ** - customers ←→ accounts (many-to-many via customer_account) - accounts → accounts (self-reference for parent-child hierarchy) - accounts → trans…_

---

### ✅ 24 — How does the schema handle failed or cancelled transactions?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.2042 | **Gate:** `proceed`

**Expected answer:**
> The transactions table has a status column with CHECK constraint allowing Pending, Posted, Failed, Cancelled, and OnHold states. The business glossary explains that failed transactions are logged for audit but do not affect the account balance — the balance_after field would reflect no change. Poste…

**System answer:**
> The schema handles failed or cancelled transactions using the `status` attribute on the `transactions` table (a transaction fact table for all account activity). The business concept for `Transaction` states that transactions “flow through multiple states (Pending → Posted)” and it lists the possible `Status` values as `Pending, Posted, Failed, Cancelled, OnHold`. Therefore, a failed or cancelled …

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_9`, `parent_chunk_data_dictionary.md_12`, `parent_chunk_data_dictionary.md_7`, `TRANSACTIONS→ACCOUNTS`, `Financial Transaction→TRANSACTIONS`, `parent_chunk_business_glossary.md_1`, `parent_chunk_business_glossary.md_0`, `parent_chunk_business_glossary.md_3`

**Context previews (first 3):**

1. _## transactions  **Description: ** Transaction fact table recording all account activity. Supports multiple transaction types including debits, credits, transfers, and withdrawals. Tracks calculated f…_

2. _## Entity Relationship Summary  **Key Relationships: ** - customers ←→ accounts (many-to-many via customer_account) - accounts → accounts (self-reference for parent-child hierarchy) - accounts → trans…_

3. _## accounts  **Description: ** Deposit account master table supporting multiple account types (checking, savings, money market, CD, investment). Implements parent-child hierarchy for portfolio aggrega…_

---

### ✅ 25 — What operational states can an ATM have and what do they mean for available services?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.5109 | **Gate:** `proceed`

**Expected answer:**
> ATMs have three operational states defined by CHECK constraint: Operational (fully functional for all supported transactions), OutOfService (technical issue preventing all transactions), and OutOfCash (cash depleted, preventing withdrawals). The business glossary explains that cash replenishment is …

**System answer:**
> An ATM’s operational state is captured in `ATMS.status`, which the knowledge graph describes as “operational status for availability management.” The defined status values are `Operational`, `OutOfService`, and `OutOfCash`.

However, the retrieved context does not specify what specific services (e.g., deposit vs. cardless withdrawal) are available or unavailable for each of those states. It only s…

**Sources retrieved (12):** `ATM Location→ATMS`, `parent_chunk_data_dictionary.md_6`, `Branch service locations→BRANCHES`, `ATMS→BRANCHES`, `parent_chunk_data_dictionary.md_12`, `parent_chunk_data_dictionary.md_11`, `ATM Location`, `Branch service locations`

**Context previews (first 3):**

1. _Business concept 'ATM Location' — The table is explicitly described as “ATM locations (standalone and branch ATMs)” and contains location-specific attributes like atm_code, location address, latitude/…_

2. _## atms  **Description: ** ATM locations including branch-attached machines, drive-through ATMs, and standalone units. Tracks cash balances for replenishment scheduling, GPS coordinates for location s…_

3. _Business concept 'Branch service locations' — The table stores physical location master data for bank branches/ATMs (address, phone, city/state/zip) and operational attributes that characterize servic…_

---

## Anomalies & Observations

No anomalies detected. All questions grounded with acceptable RAGAS scores.
