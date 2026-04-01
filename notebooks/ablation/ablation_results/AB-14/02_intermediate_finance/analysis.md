# AB-14 — 02_intermediate_finance — Run Analysis

**Timestamp:** 2026-04-01 05:02:28  
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
| Triplets extracted | 589 |
| Entities resolved | 225 |
| Tables parsed | 8 |
| Tables completed | 8 |

## Query Evaluation Summary

| Metric | Value |
|--------|-------|
| Questions | 25 |
| Grounded | **25/25 (100%)** |
| Avg GT Coverage | 100% |
| Avg Top Score | 0.4841 |
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
> A checking account is not separately defined in the retrieved context, but it is identified as one of the valid `account_type` values for the business concept Account and for the `accounts` table (`Checking`, `Savings`, `MoneyMarket`, `CD`, `Investment`).

From the Account definition, a checking account is therefore a type of account: a financial arrangement between a customer and the bank that al…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_7`, `parent_chunk_data_dictionary.md_8`, `parent_chunk_data_dictionary.md_9`, `parent_chunk_data_dictionary.md_10`, `parent_chunk_business_glossary.md_0`, `parent_chunk_business_glossary.md_1`, `parent_chunk_business_glossary.md_2`, `parent_chunk_business_glossary.md_3`

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
> From the retrieved context, both Savings and MoneyMarket are supported `account_type` values for an `accounts` record, and both fall under the broader business concept of an Account as a deposit vehicle for managing funds.

However, the context does not provide a business definition or rule that distinguishes a savings account from a money market account. It does not describe differences in featur…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_7`, `parent_chunk_data_dictionary.md_10`, `parent_chunk_data_dictionary.md_9`, `parent_chunk_data_dictionary.md_8`, `parent_chunk_data_dictionary.md_12`, `parent_chunk_data_dictionary.md_11`, `Customer Account Relationship→CUSTOMER_ACCOUNT`, `parent_chunk_business_glossary.md_0`

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
> From the Interest concept: APR is Annual Percentage Rate and is for loans, while APY is Annual Percentage Yield and is for deposits. The context also states that APY accounts for compounding, and interest may involve compounding frequency such as daily, monthly, or annually. In business context, banks charge interest on loans and pay interest on deposits, so APR aligns to borrowing cost and APY al…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_10`, `parent_chunk_business_glossary.md_2`, `parent_chunk_business_glossary.md_0`, `parent_chunk_business_glossary.md_1`, `parent_chunk_data_dictionary.md_7`, `parent_chunk_data_dictionary.md_11`, `parent_chunk_data_dictionary.md_8`, `Automated Teller Machine→ATMS`

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
> The retrieved context does not define what “KYC Level 2” means.

What it does say is that KYC is tracked on the customer master data table, `CUSTOMERS`, via the `kyc_status` attribute for the business concept “Bank Customer,” and the enforced valid KYC levels are `Level1`, `Level2`, or `Level3`. But there is no description in the provided context of the criteria, permissions, or business meaning s…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_12`, `Bank Customer→CUSTOMERS`, `parent_chunk_data_dictionary.md_7`, `parent_chunk_data_dictionary.md_4`, `parent_chunk_business_glossary.md_0`, `Bank Customer`, `parent_chunk_business_glossary.md_1`, `parent_chunk_data_dictionary.md_5`

**Context previews (first 3):**

1. _## Entity Relationship Summary  **Key Relationships: ** - customers ←→ accounts (many-to-many via customer_account) - accounts → accounts (self-reference for parent-child hierarchy) - accounts → trans…_

2. _Business concept 'Bank Customer' — The table is explicitly described as the core customer dimension/master data for all banking customers and contains identifying, contact, KYC, and risk-profile attri…_

3. _## accounts  **Description: ** Deposit account master table supporting multiple account types (checking, savings, money market, CD, investment). Implements parent-child hierarchy for portfolio aggrega…_

---

### ✅ 5 — How does the schema support different account subtypes and their varying requirements?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.1891 | **Gate:** `proceed_with_warning`

**Expected answer:**
> The accounts table has an account_subtype column (VARCHAR 30, nullable) that stores values like Premium or Standard to differentiate within each account_type. Combined with the minimum_balance and monthly_fee columns, each account can have different requirements configured per subtype. The account_t…

**System answer:**
> The schema supports account subtype variation primarily in the `ACCOUNTS` table. That table is described as the deposit account master supporting multiple account types, specifically `Checking`, `Savings`, `MoneyMarket`, `CD`, and `Investment`, and it includes an `account_subtype` column for subtype values such as `Premium`, `Student`, and `Standard`.

The same `ACCOUNTS` record also carries the a…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_7`, `parent_chunk_data_dictionary.md_12`, `balances, interest accrual, fees, and account lifecycle status→ACCOUNTS`, `parent_chunk_data_dictionary.md_8`, `Payment Card→CARDS`, `parent_chunk_data_dictionary.md_9`, `Customer Account Relationship`, `parent_chunk_business_glossary.md_0`

**Context previews (first 3):**

1. _## accounts  **Description: ** Deposit account master table supporting multiple account types (checking, savings, money market, CD, investment). Implements parent-child hierarchy for portfolio aggrega…_

2. _## Entity Relationship Summary  **Key Relationships: ** - customers ←→ accounts (many-to-many via customer_account) - accounts → accounts (self-reference for parent-child hierarchy) - accounts → trans…_

3. _Business concept 'balances, interest accrual, fees, and account lifecycle status' is implemented by physical table ACCOUNTS (columns: account_id, account_number, account_type, account_subtype, parent_…_

---

### ✅ 6 — What types of loan products does the bank offer?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.6931 | **Gate:** `proceed`

**Expected answer:**
> The bank offers five loan types defined by the CHECK constraint on loans.loan_type: (1) Mortgage — secured by real estate, glossary example shows $350,000 at 5.50% APR for 360 months; (2) Personal Loan — unsecured, example $15,000 at 8.50% APR for 48 months; (3) Auto Loan — secured by vehicle, examp…

**System answer:**
> The bank offers these loan products in the `LOANS` table’s `loan_type` domain: Mortgage, Personal, Auto, HELOC, and CreditCard. The business concept description for `LOANS` also describes the lending portfolio as including mortgages, personal loans, auto loans, HELOCs, and credit cards.

**Sources retrieved (12):** `Loan portfolio table tracking all lending products including mortgages, personal loans, auto loans, HELOCs, and credit cards→LOANS`, `parent_chunk_data_dictionary.md_10`, `parent_chunk_data_dictionary.md_12`, `parent_chunk_data_dictionary.md_7`, `in-person services including teller transactions, account opening, loan applications, and financial advisory services→TRANSACTIONS`, `Bank Customer→CUSTOMERS`, `Loan portfolio table tracking all lending products including mortgages, personal loans, auto loans, HELOCs, and credit cards`, `parent_chunk_business_glossary.md_1`

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
> The retrieved context does not provide a specific daily ATM withdrawal limit for standard customers, so this cannot be determined.

What is known from the context is only schema-level metadata: the `CARDS` table includes an `atm_daily_limit` column, and the `ACCOUNTS` table includes an `account_subtype` with examples such as `Standard`. The context also says cards track spending limits and are lin…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_11`, `Payment Card→CARDS`, `parent_chunk_data_dictionary.md_6`, `parent_chunk_data_dictionary.md_12`, `parent_chunk_data_dictionary.md_7`, `Automated Teller Machine→ATMS`, `parent_chunk_business_glossary.md_3`, `parent_chunk_business_glossary.md_1`

**Context previews (first 3):**

1. _## cards  **Description: ** Payment card issuance table for debit, credit, and ATM cards. Links cards to both customer and account. Tracks security features (chip, contactless, PIN), spending limits, …_

2. _Business concept 'Payment Card' — The table is a card issuance master with card number, type, network, CVV, limits, status, and issuance dates, which aligns strongly with a payment card entity. It als…_

3. _## atms  **Description: ** ATM locations including branch-attached machines, drive-through ATMs, and standalone units. Tracks cash balances for replenishment scheduling, GPS coordinates for location s…_

---

### ✅ 8 — What is the difference between a parent account and a child account?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.3098 | **Gate:** `proceed`

**Expected answer:**
> The accounts table supports parent-child hierarchies through the parent_account_id self-referencing foreign key, with a CHECK constraint preventing circular references (parent_account_id != account_id). The data dictionary describes this as supporting portfolio aggregation where parent accounts (typ…

**System answer:**
> In the `ACCOUNTS` hierarchy, a parent account is an account that other accounts reference through `ACCOUNTS.PARENT_ACCOUNT_ID`, while a child account is an account whose `parent_account_id` points to another row in `ACCOUNTS`.

The business purpose of this hierarchy is portfolio aggregation: the `accounts` table is described as supporting a parent-child structure where, for example, investment acc…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_7`, `parent_chunk_data_dictionary.md_12`, `ACCOUNTS→ACCOUNTS`, `balances, interest accrual, fees, and account lifecycle status→ACCOUNTS`, `parent_chunk_data_dictionary.md_8`, `parent_chunk_data_dictionary.md_9`, `parent_chunk_data_dictionary.md_11`, `parent_chunk_data_dictionary.md_10`

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
> The retrieved context confirms that `CARDS` has a `status` column and that the `cards` table “tracks ... card status,” but it does not define the meaning of specific card status values such as `Frozen`.

The only `Frozen` status definition visible in the context is for the business concept `Account`, where account status includes `Active, Dormant, Frozen, Closed`. There is no corresponding busines…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_7`, `parent_chunk_data_dictionary.md_10`, `parent_chunk_data_dictionary.md_11`, `Payment Card→CARDS`, `parent_chunk_data_dictionary.md_6`, `parent_chunk_data_dictionary.md_9`, `parent_chunk_business_glossary.md_0`, `parent_chunk_business_glossary.md_3`

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
> The `TRANSACTIONS` table tracks balance impact in three connected ways.

First, each row is tied to a specific account through `account_id`, which is a foreign key to `ACCOUNTS.ACCOUNT_ID`. That identifies which account balance the transaction affects.

Second, the table stores the transaction classification in `transaction_type`, with supported values including `Debit`, `Credit`, `Transfer`, `Pay…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_9`, `TRANSACTIONS→ACCOUNTS`, `in-person services including teller transactions, account opening, loan applications, and financial advisory services→TRANSACTIONS`, `parent_chunk_data_dictionary.md_7`, `balances, interest accrual, fees, and account lifecycle status→ACCOUNTS`, `ACCOUNTS→BRANCHES`, `ACCOUNTS→ACCOUNTS`, `parent_chunk_data_dictionary.md_10`

**Context previews (first 3):**

1. _## transactions  **Description: ** Transaction fact table recording all account activity. Supports multiple transaction types including debits, credits, transfers, and withdrawals. Tracks calculated f…_

2. _Relationship: TRANSACTIONS references ACCOUNTS via foreign key ACCOUNT_ID -> ACCOUNTS.ACCOUNT_ID.…_

3. _Business concept 'in-person services including teller transactions, account opening, loan applications, and financial advisory services' is implemented by physical table TRANSACTIONS (columns: transac…_

---

### ✅ 11 — How does the customer_account junction table support multiple ownership types?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.9865 | **Gate:** `proceed`

**Expected answer:**
> The customer_account table implements a many-to-many relationship between customers and accounts with a composite primary key (customer_id, account_id). It supports four relationship types via CHECK constraint: Owner, JointOwner, AuthorizedSigner, and Custodian. The is_primary flag designates the pr…

**System answer:**
> The `customer_account` table supports multiple ownership types by acting as a many-to-many junction between `customers` and `accounts`, so a single customer can be linked to multiple accounts and a single account can be linked to multiple customers.

It distinguishes the type of relationship through the `relationship_type` column, which is described as supporting `Owner`, `JointOwner`, `Authorized…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_8`, `Customer Account Relationship`, `Customer Account Relationship→CUSTOMER_ACCOUNT`, `parent_chunk_data_dictionary.md_12`, `CUSTOMER_ACCOUNT→CUSTOMERS`, `parent_chunk_data_dictionary.md_7`, `CUSTOMER_ACCOUNT→ACCOUNTS`, `parent_chunk_data_dictionary.md_9`

**Context previews (first 3):**

1. _## customer_account  **Description: ** Junction table implementing many-to-many relationship between customers and accounts. Supports joint ownership, authorized signers, and custodial relationships. …_

2. _Customer Account Relationship: The table is explicitly described as a many-to-many junction between customers and accounts, with foreign keys to both and attributes that characterize the linkage (rela…_

3. _Business concept 'Customer Account Relationship' — The table is explicitly described as a many-to-many junction between customers and accounts, with foreign keys to both and attributes that characteri…_

---

### ✅ 12 — What is the difference between current_balance and available_balance in the accounts table?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.8328 | **Gate:** `proceed`

**Expected answer:**
> The accounts table tracks two separate balance fields: current_balance includes all transactions including pending ones, while available_balance excludes holds and pending transactions and represents what the customer can actually withdraw. The business glossary confirms this distinction, stating th…

**System answer:**
> The retrieved context shows that the `ACCOUNTS` table stores both `current_balance` and `available_balance` as separate account attributes, and the business glossary explicitly lists “Current Balance vs. Available Balance” as a key attribute of the Account concept.

However, the context provided here does not explicitly define each field or state the exact difference between `current_balance` and …

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_7`, `balances, interest accrual, fees, and account lifecycle status→ACCOUNTS`, `parent_chunk_data_dictionary.md_10`, `parent_chunk_data_dictionary.md_6`, `parent_chunk_data_dictionary.md_9`, `in-person services including teller transactions, account opening, loan applications, and financial advisory services→TRANSACTIONS`, `ACCOUNTS→ACCOUNTS`, `ACCOUNTS→BRANCHES`

**Context previews (first 3):**

1. _## accounts  **Description: ** Deposit account master table supporting multiple account types (checking, savings, money market, CD, investment). Implements parent-child hierarchy for portfolio aggrega…_

2. _Business concept 'balances, interest accrual, fees, and account lifecycle status' is implemented by physical table ACCOUNTS (columns: account_id, account_number, account_type, account_subtype, parent_…_

3. _## loans  **Description: ** Loan portfolio table tracking all lending products including mortgages, personal loans, auto loans, HELOCs, and credit cards. Records original terms, amortization schedules…_

---

### ✅ 13 — How are loans linked to both customers and accounts in the schema?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.8105 | **Gate:** `proceed`

**Expected answer:**
> The loans table has a customer_id foreign key referencing the customers table (the borrower) and an optional account_id foreign key referencing the accounts table (for linked payment accounts). Each loan belongs to exactly one customer, and can optionally be connected to an account for automatic pay…

**System answer:**
> In the schema, loans are linked directly in the `LOANS` table through two foreign keys.

`LOANS.customer_id` is a required foreign key to `CUSTOMERS.customer_id`, so every loan must be associated with a customer. This is also reflected in the relationship summary as `customers → loans (one-to-many)`.

`LOANS.account_id` is an optional foreign key to `ACCOUNTS.account_id`, so a loan can also be lin…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_12`, `LOANS→CUSTOMERS`, `LOANS→ACCOUNTS`, `Customer Account Relationship`, `parent_chunk_data_dictionary.md_10`, `Customer Account Relationship→CUSTOMER_ACCOUNT`, `CUSTOMER_ACCOUNT→CUSTOMERS`, `parent_chunk_data_dictionary.md_8`

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
> The system supports these transaction types in `TRANSACTIONS.transaction_type`: Debit, Credit, Transfer, Payment, Withdrawal, Deposit, and Fee. The `transactions` table is described as recording all account activity, and the `Transaction` business definition confirms the same set of supported financial activities. The table also stores `amount` (always positive), `currency`, `transaction_date`, `b…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_9`, `parent_chunk_data_dictionary.md_7`, `balances, interest accrual, fees, and account lifecycle status→ACCOUNTS`, `in-person services including teller transactions, account opening, loan applications, and financial advisory services→TRANSACTIONS`, `Automated Teller Machine→ATMS`, `parent_chunk_data_dictionary.md_6`, `parent_chunk_business_glossary.md_1`, `parent_chunk_business_glossary.md_3`

**Context previews (first 3):**

1. _## transactions  **Description: ** Transaction fact table recording all account activity. Supports multiple transaction types including debits, credits, transfers, and withdrawals. Tracks calculated f…_

2. _## accounts  **Description: ** Deposit account master table supporting multiple account types (checking, savings, money market, CD, investment). Implements parent-child hierarchy for portfolio aggrega…_

3. _Business concept 'balances, interest accrual, fees, and account lifecycle status' is implemented by physical table ACCOUNTS (columns: account_id, account_number, account_type, account_subtype, parent_…_

---

### ✅ 15 — How does the schema support joint account ownership between multiple customers?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.4870 | **Gate:** `proceed`

**Expected answer:**
> Joint ownership is implemented through the customer_account junction table, which creates a many-to-many relationship between customers and accounts. Each row has a relationship_type CHECK constraint allowing Owner, JointOwner, AuthorizedSigner, or Custodian. The ownership_percentage field (DECIMAL …

**System answer:**
> The schema supports joint account ownership through the `customer_account` table, which is explicitly a many-to-many junction between `customers` and `accounts`. This means one customer can be linked to multiple accounts, and one account can be linked to multiple customers.

At the schema level, joint ownership is represented by storing multiple rows in `CUSTOMER_ACCOUNT` for the same `account_id`…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_8`, `parent_chunk_data_dictionary.md_12`, `Customer Account Relationship`, `Customer Account Relationship→CUSTOMER_ACCOUNT`, `parent_chunk_data_dictionary.md_7`, `parent_chunk_data_dictionary.md_11`, `CUSTOMER_ACCOUNT→CUSTOMERS`, `CUSTOMER_ACCOUNT→ACCOUNTS`

**Context previews (first 3):**

1. _## customer_account  **Description: ** Junction table implementing many-to-many relationship between customers and accounts. Supports joint ownership, authorized signers, and custodial relationships. …_

2. _## Entity Relationship Summary  **Key Relationships: ** - customers ←→ accounts (many-to-many via customer_account) - accounts → accounts (self-reference for parent-child hierarchy) - accounts → trans…_

3. _Customer Account Relationship: The table is explicitly described as a many-to-many junction between customers and accounts, with foreign keys to both and attributes that characterize the linkage (rela…_

---

### ✅ 16 — What information does the cards table track and how are cards linked to customers and accounts?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.9528 | **Gate:** `proceed`

**Expected answer:**
> The cards table links to both accounts (account_id FK) and customers (customer_id FK), tracking card_type (Debit/Credit/ATM), card_network (Visa/Mastercard/Discover/AmericanExpress), card_number, cardholder name, expiration_date, and CVV. For spending controls it stores credit_limit (nullable, for c…

**System answer:**
> The `cards` table is a payment card issuance table for debit, credit, and ATM cards. It tracks card issuance and operational details including the card number (`card_number`, unique PAN), card type (`card_type`: Debit/Credit/ATM), network (`card_network`), card name, expiration date, CVV, credit limit, daily spending limit, ATM daily limit, whether a PIN is set (`pin_set`), whether the card has a …

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_11`, `CARDS→CUSTOMERS`, `CARDS→ACCOUNTS`, `Customer Account Relationship`, `parent_chunk_data_dictionary.md_10`, `CUSTOMER_ACCOUNT→CUSTOMERS`, `CUSTOMER_ACCOUNT→ACCOUNTS`, `Customer Account Relationship→CUSTOMER_ACCOUNT`

**Context previews (first 3):**

1. _## cards  **Description: ** Payment card issuance table for debit, credit, and ATM cards. Links cards to both customer and account. Tracks security features (chip, contactless, PIN), spending limits, …_

2. _Relationship: CARDS references CUSTOMERS via foreign key CUSTOMER_ID -> CUSTOMERS.CUSTOMER_ID.…_

3. _Relationship: CARDS references ACCOUNTS via foreign key ACCOUNT_ID -> ACCOUNTS.ACCOUNT_ID.…_

---

### ✅ 17 — How does the schema handle interest rates across deposit and loan products?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0574 | **Gate:** `proceed_with_warning`

**Expected answer:**
> Interest rates are stored differently for deposits and loans. The accounts table has an interest_rate column (nullable DECIMAL 5,4) and interest_earned for year-to-date tracking. The loans table has its own interest_rate column representing APR. The business glossary explains that APR (Annual Percen…

**System answer:**
> The schema handles interest rates separately for deposit products in ACCOUNTS and lending products in LOANS, with the business meaning defined in the Interest glossary.

For deposit products, the ACCOUNTS table stores interest-related fields including interest_rate and interest_earned. ACCOUNTS covers deposit account types such as Checking, Savings, MoneyMarket, CD, and Investment, and its busines…

**Sources retrieved (12):** `Loan portfolio table tracking all lending products including mortgages, personal loans, auto loans, HELOCs, and credit cards→LOANS`, `parent_chunk_data_dictionary.md_12`, `parent_chunk_data_dictionary.md_10`, `parent_chunk_data_dictionary.md_7`, `LOANS→CUSTOMERS`, `balances, interest accrual, fees, and account lifecycle status→ACCOUNTS`, `LOANS→ACCOUNTS`, `parent_chunk_business_glossary.md_2`

**Context previews (first 3):**

1. _Business concept 'Loan portfolio table tracking all lending products including mortgages, personal loans, auto loans, HELOCs, and credit cards' is implemented by physical table LOANS (columns: loan_id…_

2. _## Entity Relationship Summary  **Key Relationships: ** - customers ←→ accounts (many-to-many via customer_account) - accounts → accounts (self-reference for parent-child hierarchy) - accounts → trans…_

3. _## loans  **Description: ** Loan portfolio table tracking all lending products including mortgages, personal loans, auto loans, HELOCs, and credit cards. Records original terms, amortization schedules…_

---

### ✅ 18 — What types of branches does the bank operate and how do they differ in capabilities?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.1556 | **Gate:** `proceed_with_warning`

**Expected answer:**
> The branches table supports three types via CHECK constraint: FullService, Satellite, and ATMOnly. The business glossary details each: FullService branches offer complete banking services including loan origination, financial advisors, and safe deposit boxes; Satellite branches have limited hours an…

**System answer:**
> The bank operates three branch types in `BRANCHES.branch_type`: `FullService`, `Satellite`, and `ATMOnly`.

From the business concept and `branches` table description, these correspond to full-service branches, satellite offices, and ATM-only locations. The `BRANCHES` table tracks attributes such as `hours`, `atm_count`, `teller_count`, and `manager_name`, so the branch model distinguishes locatio…

**Sources retrieved (12):** `Bank branch locations (full-service, satellite, and ATM-only)→BRANCHES`, `parent_chunk_data_dictionary.md_12`, `parent_chunk_data_dictionary.md_7`, `parent_chunk_data_dictionary.md_6`, `Automated Teller Machine→ATMS`, `Bank Customer→CUSTOMERS`, `parent_chunk_data_dictionary.md_5`, `parent_chunk_business_glossary.md_2`

**Context previews (first 3):**

1. _Business concept 'Bank branch locations (full-service, satellite, and ATM-only)' is implemented by physical table BRANCHES (columns: branch_id, branch_code, branch_name, branch_type, address, city, st…_

2. _## Entity Relationship Summary  **Key Relationships: ** - customers ←→ accounts (many-to-many via customer_account) - accounts → accounts (self-reference for parent-child hierarchy) - accounts → trans…_

3. _## accounts  **Description: ** Deposit account master table supporting multiple account types (checking, savings, money market, CD, investment). Implements parent-child hierarchy for portfolio aggrega…_

---

### ✅ 19 — How are ATMs related to branches in the schema and what types of ATMs exist?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.6184 | **Gate:** `proceed`

**Expected answer:**
> The atms table has an optional branch_id foreign key referencing branches. When branch_id is NULL, the ATM is standalone and not affiliated with any branch. ATM types are defined by CHECK constraint: Branch (on-premises), DriveThrough (vehicle-accessible), and Standalone (independent locations). Eac…

**System answer:**
> In the schema, `ATMS` is related to `BRANCHES` through the foreign key `ATMS.BRANCH_ID -> BRANCHES.BRANCH_ID`. The relationship is one-to-many from `BRANCHES` to `ATMS`, meaning one branch can have multiple ATMs. The `atms` table description also states that `branch_id` is nullable, which indicates that some ATMs are standalone and therefore not linked to a branch.

The business rules clarify how …

**Sources retrieved (12):** `ATMS→BRANCHES`, `parent_chunk_data_dictionary.md_6`, `parent_chunk_data_dictionary.md_12`, `Automated Teller Machine→ATMS`, `Bank branch locations (full-service, satellite, and ATM-only)→BRANCHES`, `parent_chunk_business_glossary.md_3`, `parent_chunk_data_dictionary.md_5`, `parent_chunk_business_glossary.md_2`

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
> The retrieved context does not define a full loan lifecycle from application to completion, so I cannot describe an application workflow, approval stages, loan-specific status meanings, or a formal completion/closure process.

What the context does show is this: “loan applications” are mentioned only as part of the business concept “in-person services including teller transactions, account opening…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_10`, `parent_chunk_data_dictionary.md_7`, `balances, interest accrual, fees, and account lifecycle status→ACCOUNTS`, `Loan portfolio table tracking all lending products including mortgages, personal loans, auto loans, HELOCs, and credit cards→LOANS`, `parent_chunk_data_dictionary.md_12`, `in-person services including teller transactions, account opening, loan applications, and financial advisory services→TRANSACTIONS`, `parent_chunk_business_glossary.md_2`, `parent_chunk_business_glossary.md_1`

**Context previews (first 3):**

1. _## loans  **Description: ** Loan portfolio table tracking all lending products including mortgages, personal loans, auto loans, HELOCs, and credit cards. Records original terms, amortization schedules…_

2. _## accounts  **Description: ** Deposit account master table supporting multiple account types (checking, savings, money market, CD, investment). Implements parent-child hierarchy for portfolio aggrega…_

3. _Business concept 'balances, interest accrual, fees, and account lifecycle status' is implemented by physical table ACCOUNTS (columns: account_id, account_number, account_type, account_subtype, parent_…_

---

### ✅ 21 — What does preferred customer status mean and how is it tracked in the schema?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.5129 | **Gate:** `proceed`

**Expected answer:**
> Preferred status is tracked via the is_preferred boolean flag in the customers table (default: false). The business glossary states that preferred customers receive waived fees, preferred interest rates, and priority service. The glossary examples show preferred customers with longer tenure and high…

**System answer:**
> Preferred customer status means a preferred customer flag used for VIP treatment. In the schema, it is tracked at the customer level in the `CUSTOMERS` table through the `is_preferred` column.

This comes from the `customers` table description, which says it includes “preferred customer flags for VIP treatment,” and from the business concept mapping for `Bank Customer`, which maps that concept to …

**Sources retrieved (12):** `Bank Customer→CUSTOMERS`, `parent_chunk_data_dictionary.md_12`, `parent_chunk_data_dictionary.md_11`, `parent_chunk_data_dictionary.md_10`, `parent_chunk_data_dictionary.md_8`, `Loan portfolio table tracking all lending products including mortgages, personal loans, auto loans, HELOCs, and credit cards→LOANS`, `parent_chunk_data_dictionary.md_7`, `parent_chunk_data_dictionary.md_4`

**Context previews (first 3):**

1. _Business concept 'Bank Customer' — The table is explicitly described as the core customer dimension/master data for all banking customers and contains identifying, contact, KYC, and risk-profile attri…_

2. _## Entity Relationship Summary  **Key Relationships: ** - customers ←→ accounts (many-to-many via customer_account) - accounts → accounts (self-reference for parent-child hierarchy) - accounts → trans…_

3. _## cards  **Description: ** Payment card issuance table for debit, credit, and ATM cards. Links cards to both customer and account. Tracks security features (chip, contactless, PIN), spending limits, …_

---

### ✅ 22 — How does the accounts table support interest tracking and what business rules govern interest?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.3044 | **Gate:** `proceed`

**Expected answer:**
> The accounts table has interest_rate (nullable DECIMAL for the annual rate) and interest_earned (DECIMAL for year-to-date interest credited). The business glossary states that deposit interest is credited monthly (typically the first day of the month) and that APY accounts for compounding effects. P…

**System answer:**
> The `ACCOUNTS` table supports interest tracking directly through the columns `interest_rate` and `interest_earned`. The table description states it tracks “balances, interest accrual, fees, and account lifecycle status,” and the physical mapping confirms these columns exist alongside `current_balance`, `available_balance`, `minimum_balance`, `monthly_fee`, `opened_date`, `closed_date`, and `last_t…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_7`, `balances, interest accrual, fees, and account lifecycle status→ACCOUNTS`, `Loan portfolio table tracking all lending products including mortgages, personal loans, auto loans, HELOCs, and credit cards→LOANS`, `parent_chunk_data_dictionary.md_12`, `parent_chunk_data_dictionary.md_10`, `ACCOUNTS→BRANCHES`, `ACCOUNTS→ACCOUNTS`, `parent_chunk_data_dictionary.md_8`

**Context previews (first 3):**

1. _## accounts  **Description: ** Deposit account master table supporting multiple account types (checking, savings, money market, CD, investment). Implements parent-child hierarchy for portfolio aggrega…_

2. _Business concept 'balances, interest accrual, fees, and account lifecycle status' is implemented by physical table ACCOUNTS (columns: account_id, account_number, account_type, account_subtype, parent_…_

3. _Business concept 'Loan portfolio table tracking all lending products including mortgages, personal loans, auto loans, HELOCs, and credit cards' is implemented by physical table LOANS (columns: loan_id…_

---

### ✅ 23 — Can an account exist without any customer linked to it?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.1525 | **Gate:** `proceed_with_warning`

**Expected answer:**
> Looking at the schema, there is no database-level constraint that forces every account to have a customer_account row. The accounts table has no direct foreign key to customers — the relationship is through the customer_account junction table with a composite primary key (customer_id, account_id). H…

**System answer:**
> The retrieved context does not state that an account must have at least one linked customer.

What it does say is that customers and accounts are connected through the `customer_account` junction table, which implements a many-to-many relationship, and that any `customer_account` row requires both a valid `customer_id` and `account_id` to exist. That means a relationship record cannot exist withou…

**Sources retrieved (12):** `Customer Account Relationship`, `parent_chunk_data_dictionary.md_8`, `Customer Account Relationship→CUSTOMER_ACCOUNT`, `CUSTOMER_ACCOUNT→CUSTOMERS`, `parent_chunk_data_dictionary.md_12`, `CUSTOMER_ACCOUNT→ACCOUNTS`, `parent_chunk_data_dictionary.md_11`, `parent_chunk_data_dictionary.md_10`

**Context previews (first 3):**

1. _Customer Account Relationship: The table is explicitly described as a many-to-many junction between customers and accounts, with foreign keys to both and attributes that characterize the linkage (rela…_

2. _## customer_account  **Description: ** Junction table implementing many-to-many relationship between customers and accounts. Supports joint ownership, authorized signers, and custodial relationships. …_

3. _Business concept 'Customer Account Relationship' — The table is explicitly described as a many-to-many junction between customers and accounts, with foreign keys to both and attributes that characteri…_

---

### ✅ 24 — How does the schema handle failed or cancelled transactions?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.2042 | **Gate:** `proceed`

**Expected answer:**
> The transactions table has a status column with CHECK constraint allowing Pending, Posted, Failed, Cancelled, and OnHold states. The business glossary explains that failed transactions are logged for audit but do not affect the account balance — the balance_after field would reflect no change. Poste…

**System answer:**
> The schema handles failed or cancelled transactions through the `transactions` table’s `status` field.

From the `Transaction` business concept, transaction status can be `Pending`, `Posted`, `Failed`, `Cancelled`, or `OnHold`. This means a transaction is still retained as a transaction record, but its lifecycle state indicates whether it failed or was cancelled rather than successfully posted. Th…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_9`, `parent_chunk_data_dictionary.md_12`, `parent_chunk_data_dictionary.md_7`, `TRANSACTIONS→ACCOUNTS`, `in-person services including teller transactions, account opening, loan applications, and financial advisory services→TRANSACTIONS`, `Automated Teller Machine→ATMS`, `parent_chunk_business_glossary.md_1`, `parent_chunk_business_glossary.md_0`

**Context previews (first 3):**

1. _## transactions  **Description: ** Transaction fact table recording all account activity. Supports multiple transaction types including debits, credits, transfers, and withdrawals. Tracks calculated f…_

2. _## Entity Relationship Summary  **Key Relationships: ** - customers ←→ accounts (many-to-many via customer_account) - accounts → accounts (self-reference for parent-child hierarchy) - accounts → trans…_

3. _## accounts  **Description: ** Deposit account master table supporting multiple account types (checking, savings, money market, CD, investment). Implements parent-child hierarchy for portfolio aggrega…_

---

### ✅ 25 — What operational states can an ATM have and what do they mean for available services?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.4507 | **Gate:** `proceed`

**Expected answer:**
> ATMs have three operational states defined by CHECK constraint: Operational (fully functional for all supported transactions), OutOfService (technical issue preventing all transactions), and OutOfCash (cash depleted, preventing withdrawals). The business glossary explains that cash replenishment is …

**System answer:**
> For the ATM business concept and the `ATMS` table, the operational status values shown in the context are `Operational`, `OutOfService`, and `OutOfCash`.

`Operational` means the ATM is available for use as a self-service banking terminal. In that state, the services a customer can use depend on the ATM’s supported features recorded in `ATMS`, specifically `supports_deposit` and `supports_cardless…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_6`, `Automated Teller Machine→ATMS`, `Bank branch locations (full-service, satellite, and ATM-only)→BRANCHES`, `ATMS→BRANCHES`, `parent_chunk_data_dictionary.md_12`, `Payment Card→CARDS`, `parent_chunk_data_dictionary.md_11`, `parent_chunk_business_glossary.md_3`

**Context previews (first 3):**

1. _## atms  **Description: ** ATM locations including branch-attached machines, drive-through ATMs, and standalone units. Tracks cash balances for replenishment scheduling, GPS coordinates for location s…_

2. _Business concept 'Automated Teller Machine' — a self-service banking terminal that allows customers to perform basic transactions without teller assistance. is implemented by physical table ATMS (colu…_

3. _Business concept 'Bank branch locations (full-service, satellite, and ATM-only)' is implemented by physical table BRANCHES (columns: branch_id, branch_code, branch_name, branch_type, address, city, st…_

---

## Anomalies & Observations

No anomalies detected. All questions grounded with acceptable RAGAS scores.
