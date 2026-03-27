# AB-00 — 02_intermediate_finance — Run Analysis

**Timestamp:** 2026-03-27 17:45:09  
**Run tag:** `post-fix-v3`

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
| Triplets extracted | 599 |
| Entities resolved | 231 |
| Tables parsed | 8 |
| Tables completed | 8 |

## Query Evaluation Summary

| Metric | Value |
|--------|-------|
| Questions | 25 |
| Grounded | **25/25 (100%)** |
| Avg GT Coverage | 100% |
| Avg Top Score | 0.4794 |
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
> A checking account is one of the deposit account types supported by the `accounts` table, where `account_type` can be “Checking” (along with “Savings”, “MoneyMarket”, “CD”, and “Investment”). The `accounts` description also states that accounts allow deposit, withdrawal, and management of funds, and that the table tracks balances, interest accrual, fees, and account lifecycle status.

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_7`, `parent_chunk_data_dictionary.md_8`, `parent_chunk_data_dictionary.md_9`, `parent_chunk_data_dictionary.md_10`, `Account Balances and Status→ACCOUNTS`, `parent_chunk_data_dictionary.md_12`, `parent_chunk_business_glossary.md_0`, `parent_chunk_business_glossary.md_1`

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
> From the retrieved context, both “Savings” and “MoneyMarket” are simply values of `accounts.account_type` (the accounts table supports multiple account types: Checking, Savings, MoneyMarket, CD, Investment). The context does not provide any additional behavioral or product-specific rules that distinguish a savings account from a money market account (for example, no separate definitions for how in…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_7`, `parent_chunk_data_dictionary.md_10`, `Account Balances and Status→ACCOUNTS`, `parent_chunk_data_dictionary.md_9`, `parent_chunk_data_dictionary.md_8`, `parent_chunk_data_dictionary.md_12`, `parent_chunk_data_dictionary.md_11`, `parent_chunk_business_glossary.md_0`

**Context previews (first 3):**

1. _## accounts  **Description: ** Deposit account master table supporting multiple account types (checking, savings, money market, CD, investment). Implements parent-child hierarchy for portfolio aggrega…_

2. _## loans  **Description: ** Loan portfolio table tracking all lending products including mortgages, personal loans, auto loans, HELOCs, and credit cards. Records original terms, amortization schedules…_

3. _Business concept 'Account Balances and Status' — The table stores deposit-account monetary attributes (current_balance, available_balance, minimum_balance, interest_rate, interest_earned, monthly_fee)…_

---

### ✅ 3 — What is APR versus APY?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.9609 | **Gate:** `proceed`

**Expected answer:**
> APR (Annual Percentage Rate) is the annual cost of a loan including interest and fees, used for loan products. APY (Annual Percentage Yield) is the effective annual rate including compounding effects for deposit products. APY is higher than the nominal rate when compounding is more frequent than ann…

**System answer:**
> APR (Annual Percentage Rate) is the annual percentage rate that applies to interest, and APY (Annual Percentage Yield) is used for deposits to reflect compound interest. In the “Interest” business concept, APR is listed as “Interest Rate (annual percentage) - APR (Annual Percentage Rate) - for loans” and APY is listed as “APY (Annual Percentage Yield) - for deposits,” with APY accounting for compo…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_10`, `parent_chunk_business_glossary.md_2`, `parent_chunk_business_glossary.md_0`, `parent_chunk_business_glossary.md_1`, `parent_chunk_data_dictionary.md_7`, `parent_chunk_data_dictionary.md_11`, `parent_chunk_data_dictionary.md_8`, `Primary owner designation→CUSTOMER_ACCOUNT`

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
> The retrieved context only states a business rule that KYC levels must be one of **Level1, Level2, or Level3**. It does not define what **KYC Level 2** specifically means (e.g., criteria, required documentation, or behavioral/eligibility implications). The meaning of “KYC Level 2” therefore remains unavailable in the knowledge graph.

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_12`, `Core customer dimension table containing master data for all individual and corporate banking customers→CUSTOMERS`, `parent_chunk_data_dictionary.md_7`, `parent_chunk_data_dictionary.md_4`, `parent_chunk_business_glossary.md_0`, `parent_chunk_business_glossary.md_1`, `parent_chunk_data_dictionary.md_5`, `parent_chunk_business_glossary.md_3`

**Context previews (first 3):**

1. _## Entity Relationship Summary  **Key Relationships: ** - customers ←→ accounts (many-to-many via customer_account) - accounts → accounts (self-reference for parent-child hierarchy) - accounts → trans…_

2. _Business concept 'Core customer dimension table containing master data for all individual and corporate banking customers' is implemented by physical table CUSTOMERS (columns: customer_id, first_name,…_

3. _## accounts  **Description: ** Deposit account master table supporting multiple account types (checking, savings, money market, CD, investment). Implements parent-child hierarchy for portfolio aggrega…_

---

### ✅ 5 — How does the schema support different account subtypes and their varying requirements?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.1891 | **Gate:** `proceed_with_warning`

**Expected answer:**
> The accounts table has an account_subtype column (VARCHAR 30, nullable) that stores values like Premium or Standard to differentiate within each account_type. Combined with the minimum_balance and monthly_fee columns, each account can have different requirements configured per subtype. The account_t…

**System answer:**
> The schema supports different account subtypes through the `accounts` table by storing both an `account_type` and an optional `account_subtype`.

In `accounts`, `account_type` is a required field with values like Checking/Savings/MoneyMarket/CD/Investment, and `account_subtype` is a nullable field intended for finer-grained subtype classification (examples given include “Premium”, “Student”, and “…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_7`, `parent_chunk_data_dictionary.md_12`, `Account Balances and Status→ACCOUNTS`, `parent_chunk_data_dictionary.md_8`, `Loan Type (Mortgage, Personal, Auto, HELOC, CreditCard)→LOANS`, `parent_chunk_data_dictionary.md_9`, `parent_chunk_data_dictionary.md_11`, `parent_chunk_data_dictionary.md_10`

**Context previews (first 3):**

1. _## accounts  **Description: ** Deposit account master table supporting multiple account types (checking, savings, money market, CD, investment). Implements parent-child hierarchy for portfolio aggrega…_

2. _## Entity Relationship Summary  **Key Relationships: ** - customers ←→ accounts (many-to-many via customer_account) - accounts → accounts (self-reference for parent-child hierarchy) - accounts → trans…_

3. _Business concept 'Account Balances and Status' — The table stores deposit-account monetary attributes (current_balance, available_balance, minimum_balance, interest_rate, interest_earned, monthly_fee)…_

---

### ✅ 6 — What types of loan products does the bank offer?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.4020 | **Gate:** `proceed`

**Expected answer:**
> The bank offers five loan types defined by the CHECK constraint on loans.loan_type: (1) Mortgage — secured by real estate, glossary example shows $350,000 at 5.50% APR for 360 months; (2) Personal Loan — unsecured, example $15,000 at 8.50% APR for 48 months; (3) Auto Loan — secured by vehicle, examp…

**System answer:**
> The bank offers the following loan product types: Mortgage, Personal, Auto, HELOC, and CreditCard. These are represented by the business concept “Loan Type (Mortgage, Personal, Auto, HELOC, CreditCard)” in the `LOANS` table via the `loan_type` column.

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_10`, `Loan Type (Mortgage, Personal, Auto, HELOC, CreditCard)→LOANS`, `parent_chunk_data_dictionary.md_12`, `parent_chunk_data_dictionary.md_7`, `LOANS→CUSTOMERS`, `parent_chunk_data_dictionary.md_9`, `Bank physical locations (full-service branches, satellite offices, and ATM-only locations)→BRANCHES`, `Loan Type (Mortgage, Personal, Auto, HELOC, CreditCard)`

**Context previews (first 3):**

1. _## loans  **Description: ** Loan portfolio table tracking all lending products including mortgages, personal loans, auto loans, HELOCs, and credit cards. Records original terms, amortization schedules…_

2. _Business concept 'Loan Type (Mortgage, Personal, Auto, HELOC, CreditCard)' is implemented by physical table LOANS (columns: loan_id, customer_id, loan_type, account_id, principal_amount, interest_rate…_

3. _## Entity Relationship Summary  **Key Relationships: ** - customers ←→ accounts (many-to-many via customer_account) - accounts → accounts (self-reference for parent-child hierarchy) - accounts → trans…_

---

### ✅ 7 — What is the daily ATM withdrawal limit for standard customers?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.3743 | **Gate:** `proceed`

**Expected answer:**
> The cards table has an atm_daily_limit column with a default value of $500. The business glossary Card Examples confirm this: a standard Debit Card has a $500 ATM limit, while a Premium Debit card has a $2,000 ATM limit. The daily_limit column (default $3,000) controls POS spending separately. These…

**System answer:**
> The daily ATM withdrawal limit is stored as the card master attribute `atm_daily_limit` in the `cards` table (described under “Card security and limits” as the “atm_daily_limit”).  

However, the retrieved context does not define what a “standard customer” is or how that customer category maps to a specific `atm_daily_limit` value, so the specific limit for “standard customers” remains unavailable…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_11`, `Card security and limits→CARDS`, `parent_chunk_data_dictionary.md_6`, `parent_chunk_data_dictionary.md_12`, `parent_chunk_data_dictionary.md_7`, `parent_chunk_data_dictionary.md_8`, `parent_chunk_business_glossary.md_3`, `parent_chunk_business_glossary.md_1`

**Context previews (first 3):**

1. _## cards  **Description: ** Payment card issuance table for debit, credit, and ATM cards. Links cards to both customer and account. Tracks security features (chip, contactless, PIN), spending limits, …_

2. _Business concept 'Card security and limits' — The table primarily stores card master attributes: security capabilities (chip, contactless, PIN) plus spending limits (credit_limit, daily_limit, atm_dai…_

3. _## atms  **Description: ** ATM locations including branch-attached machines, drive-through ATMs, and standalone units. Tracks cash balances for replenishment scheduling, GPS coordinates for location s…_

---

### ✅ 8 — What is the difference between a parent account and a child account?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.3098 | **Gate:** `proceed`

**Expected answer:**
> The accounts table supports parent-child hierarchies through the parent_account_id self-referencing foreign key, with a CHECK constraint preventing circular references (parent_account_id != account_id). The data dictionary describes this as supporting portfolio aggregation where parent accounts (typ…

**System answer:**
> In this schema, a parent account and a child account are distinguished by the self-referencing portfolio hierarchy on the `ACCOUNTS` table.

A parent account is an account record whose `parent_account_id` is used to relate it to other accounts in a hierarchy for “portfolio aggregation” (the context states that “investment accounts contain child accounts”). A child account is an account record that…

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
> I cannot find this information in the knowledge graph.

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_7`, `parent_chunk_data_dictionary.md_10`, `parent_chunk_data_dictionary.md_11`, `Card security and limits→CARDS`, `parent_chunk_data_dictionary.md_6`, `parent_chunk_data_dictionary.md_9`, `parent_chunk_business_glossary.md_0`, `Card security and limits`

**Context previews (first 3):**

1. _## accounts  **Description: ** Deposit account master table supporting multiple account types (checking, savings, money market, CD, investment). Implements parent-child hierarchy for portfolio aggrega…_

2. _## loans  **Description: ** Loan portfolio table tracking all lending products including mortgages, personal loans, auto loans, HELOCs, and credit cards. Records original terms, amortization schedules…_

3. _## cards  **Description: ** Payment card issuance table for debit, credit, and ATM cards. Links cards to both customer and account. Tracks security features (chip, contactless, PIN), spending limits, …_

---

### ✅ 10 — How does the transactions table track the impact of each transaction on account balances?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.8621 | **Gate:** `proceed`

**Expected answer:**
> The transactions table includes a balance_after column (DECIMAL 15,2) that records the account balance after each transaction is applied. Combined with the amount column, transaction_type (Debit/Credit/Transfer/Payment/Withdrawal/Deposit/Fee), and status (Pending/Posted/Failed/Cancelled/OnHold), thi…

**System answer:**
> The `transactions` table tracks the impact of each transaction on account balances using the calculated field `balance_after` described in the `transactions` table definition (“Tracks calculated fields (balance_after)”). In the business concept mapping for the `TRANSACTIONS` table, the table is also described as recording financial activity that affects an account’s balance, with fields including …

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_9`, `TRANSACTIONS→ACCOUNTS`, `Financial Transaction→TRANSACTIONS`, `parent_chunk_data_dictionary.md_7`, `Account Balances and Status→ACCOUNTS`, `ACCOUNTS→BRANCHES`, `ACCOUNTS→ACCOUNTS`, `parent_chunk_data_dictionary.md_10`

**Context previews (first 3):**

1. _## transactions  **Description: ** Transaction fact table recording all account activity. Supports multiple transaction types including debits, credits, transfers, and withdrawals. Tracks calculated f…_

2. _Relationship: TRANSACTIONS references ACCOUNTS via foreign key ACCOUNT_ID -> ACCOUNTS.ACCOUNT_ID.…_

3. _Business concept 'Financial Transaction' — The table is explicitly described as a transaction fact table for all account activity and includes transaction identifiers, account_id linkage, transaction_…_

---

### ✅ 11 — How does the customer_account junction table support multiple ownership types?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.9865 | **Gate:** `proceed`

**Expected answer:**
> The customer_account table implements a many-to-many relationship between customers and accounts with a composite primary key (customer_id, account_id). It supports four relationship types via CHECK constraint: Owner, JointOwner, AuthorizedSigner, and Custodian. The is_primary flag designates the pr…

**System answer:**
> The `customer_account` junction table supports multiple ownership types by storing a `relationship_type` column with values described as “Owner/JointOwner/AuthorizedSigner/Custodian.” It links `customers` to `accounts` via the composite primary key (`customer_id`, `account_id`), so a single customer and account pair can be associated under the appropriate ownership/authorization/custodial role usi…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_8`, `Primary owner designation→CUSTOMER_ACCOUNT`, `parent_chunk_data_dictionary.md_12`, `CUSTOMER_ACCOUNT→CUSTOMERS`, `parent_chunk_data_dictionary.md_7`, `CUSTOMER_ACCOUNT→ACCOUNTS`, `parent_chunk_data_dictionary.md_9`, `parent_chunk_data_dictionary.md_11`

**Context previews (first 3):**

1. _## customer_account  **Description: ** Junction table implementing many-to-many relationship between customers and accounts. Supports joint ownership, authorized signers, and custodial relationships. …_

2. _Business concept 'Primary owner designation' — The table includes an is_primary BOOLEAN flag that directly implements whether a customer is designated as the primary owner of an account. While ownersh…_

3. _## Entity Relationship Summary  **Key Relationships: ** - customers ←→ accounts (many-to-many via customer_account) - accounts → accounts (self-reference for parent-child hierarchy) - accounts → trans…_

---

### ✅ 12 — What is the difference between current_balance and available_balance in the accounts table?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.8804 | **Gate:** `proceed`

**Expected answer:**
> The accounts table tracks two separate balance fields: current_balance includes all transactions including pending ones, while available_balance excludes holds and pending transactions and represents what the customer can actually withdraw. The business glossary confirms this distinction, stating th…

**System answer:**
> In the `ACCOUNTS` table (deposit-account master), both `current_balance` and `available_balance` are described only at a high level as “Current Balance vs. Available Balance,” but the retrieved context does not define how they differ (for example, what adjustments or holds affect `available_balance`). So the knowledge graph provides the existence and business relevance of both fields, but not the …

**Sources retrieved (12):** `Account Balances and Status→ACCOUNTS`, `parent_chunk_data_dictionary.md_7`, `parent_chunk_data_dictionary.md_10`, `parent_chunk_data_dictionary.md_6`, `Financial Transaction→TRANSACTIONS`, `parent_chunk_data_dictionary.md_9`, `ACCOUNTS→ACCOUNTS`, `ACCOUNTS→BRANCHES`

**Context previews (first 3):**

1. _Business concept 'Account Balances and Status' — The table stores deposit-account monetary attributes (current_balance, available_balance, minimum_balance, interest_rate, interest_earned, monthly_fee)…_

2. _## accounts  **Description: ** Deposit account master table supporting multiple account types (checking, savings, money market, CD, investment). Implements parent-child hierarchy for portfolio aggrega…_

3. _## loans  **Description: ** Loan portfolio table tracking all lending products including mortgages, personal loans, auto loans, HELOCs, and credit cards. Records original terms, amortization schedules…_

---

### ✅ 13 — How are loans linked to both customers and accounts in the schema?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.8105 | **Gate:** `proceed`

**Expected answer:**
> The loans table has a customer_id foreign key referencing the customers table (the borrower) and an optional account_id foreign key referencing the accounts table (for linked payment accounts). Each loan belongs to exactly one customer, and can optionally be connected to an account for automatic pay…

**System answer:**
> In the schema, loans are linked to both customers and accounts through foreign keys in the `loans` table. Specifically, `loans.customer_id` is a foreign key referencing `CUSTOMERS.CUSTOMER_ID` (borrower), and `loans.account_id` is a foreign key referencing `ACCOUNTS.ACCOUNT_ID` with the note that it is optional (`account_id` is nullable).

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
> The system supports multiple transaction types in the `TRANSACTIONS` table: Debit, Credit, Transfer, Payment, Withdrawal, Deposit, and Fee (the `transaction_type` field). For transaction status, the “Transaction” business definition states that transactions flow through multiple states: Pending → Posted (and it also enumerates possible statuses as Pending, Posted, Failed, Cancelled, and OnHold).

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_9`, `parent_chunk_data_dictionary.md_7`, `Account Balances and Status→ACCOUNTS`, `Card security and limits→CARDS`, `Financial Transaction→TRANSACTIONS`, `parent_chunk_data_dictionary.md_6`, `Account Balances and Status`, `Card security and limits`

**Context previews (first 3):**

1. _## transactions  **Description: ** Transaction fact table recording all account activity. Supports multiple transaction types including debits, credits, transfers, and withdrawals. Tracks calculated f…_

2. _## accounts  **Description: ** Deposit account master table supporting multiple account types (checking, savings, money market, CD, investment). Implements parent-child hierarchy for portfolio aggrega…_

3. _Business concept 'Account Balances and Status' — The table stores deposit-account monetary attributes (current_balance, available_balance, minimum_balance, interest_rate, interest_earned, monthly_fee)…_

---

### ✅ 15 — How does the schema support joint account ownership between multiple customers?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.4870 | **Gate:** `proceed`

**Expected answer:**
> Joint ownership is implemented through the customer_account junction table, which creates a many-to-many relationship between customers and accounts. Each row has a relationship_type CHECK constraint allowing Owner, JointOwner, AuthorizedSigner, or Custodian. The ownership_percentage field (DECIMAL …

**System answer:**
> The schema supports joint account ownership through the junction table `customer_account`, which implements a many-to-many relationship between `customers` and `accounts`. Each row in `customer_account` links one `customer_id` to one `account_id` (composite primary key: `customer_id`, `account_id`) and records the `relationship_type` (including `Owner/JointOwner/AuthorizedSigner/Custodian`). It al…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_8`, `parent_chunk_data_dictionary.md_12`, `Primary owner designation→CUSTOMER_ACCOUNT`, `parent_chunk_data_dictionary.md_7`, `parent_chunk_data_dictionary.md_11`, `CUSTOMER_ACCOUNT→CUSTOMERS`, `CUSTOMER_ACCOUNT→ACCOUNTS`, `parent_chunk_business_glossary.md_0`

**Context previews (first 3):**

1. _## customer_account  **Description: ** Junction table implementing many-to-many relationship between customers and accounts. Supports joint ownership, authorized signers, and custodial relationships. …_

2. _## Entity Relationship Summary  **Key Relationships: ** - customers ←→ accounts (many-to-many via customer_account) - accounts → accounts (self-reference for parent-child hierarchy) - accounts → trans…_

3. _Business concept 'Primary owner designation' — The table includes an is_primary BOOLEAN flag that directly implements whether a customer is designated as the primary owner of an account. While ownersh…_

---

### ✅ 16 — What information does the cards table track and how are cards linked to customers and accounts?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.9528 | **Gate:** `proceed`

**Expected answer:**
> The cards table links to both accounts (account_id FK) and customers (customer_id FK), tracking card_type (Debit/Credit/ATM), card_network (Visa/Mastercard/Discover/AmericanExpress), card_number, cardholder name, expiration_date, and CVV. For spending controls it stores credit_limit (nullable, for c…

**System answer:**
> The `cards` table tracks payment card master attributes for debit, credit, and ATM cards, including security capabilities (chip, contactless, PIN), spending limits (`credit_limit`, `daily_limit`, `atm_daily_limit`), and operational status (`status`). It also stores card lifecycle attributes such as `issued_date` and `expiration_date`, as well as card identity fields like `card_number` (PAN, requir…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_11`, `CARDS→CUSTOMERS`, `CARDS→ACCOUNTS`, `parent_chunk_data_dictionary.md_10`, `CUSTOMER_ACCOUNT→CUSTOMERS`, `CUSTOMER_ACCOUNT→ACCOUNTS`, `Card security and limits→CARDS`, `parent_chunk_data_dictionary.md_8`

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
> The schema captures interest rates separately for deposit and loan products in their respective tables.

For deposit accounts, the business concept “Account Balances and Status” is implemented by the physical table `ACCOUNTS`, which includes `interest_rate` (annual percentage rate for deposits) and `interest_earned` (along with balances like `current_balance` and `available_balance`, and `monthly_…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_12`, `Account Balances and Status→ACCOUNTS`, `parent_chunk_data_dictionary.md_10`, `Loan Type (Mortgage, Personal, Auto, HELOC, CreditCard)→LOANS`, `parent_chunk_data_dictionary.md_7`, `LOANS→CUSTOMERS`, `LOANS→ACCOUNTS`, `parent_chunk_business_glossary.md_2`

**Context previews (first 3):**

1. _## Entity Relationship Summary  **Key Relationships: ** - customers ←→ accounts (many-to-many via customer_account) - accounts → accounts (self-reference for parent-child hierarchy) - accounts → trans…_

2. _Business concept 'Account Balances and Status' — The table stores deposit-account monetary attributes (current_balance, available_balance, minimum_balance, interest_rate, interest_earned, monthly_fee)…_

3. _## loans  **Description: ** Loan portfolio table tracking all lending products including mortgages, personal loans, auto loans, HELOCs, and credit cards. Records original terms, amortization schedules…_

---

### ✅ 18 — What types of branches does the bank operate and how do they differ in capabilities?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.1556 | **Gate:** `proceed_with_warning`

**Expected answer:**
> The branches table supports three types via CHECK constraint: FullService, Satellite, and ATMOnly. The business glossary details each: FullService branches offer complete banking services including loan origination, financial advisors, and safe deposit boxes; Satellite branches have limited hours an…

**System answer:**
> The bank operates physical locations represented in the `branches` table, where `branch_type` can be `FullService`, `Satellite`, or `ATMOnly`.

The retrieved context does not explicitly define a capability comparison (for example, it does not state that `FullService` specifically includes teller staffing while `ATMOnly` does not). What it does support is that the `BRANCHES` schema tracks operation…

**Sources retrieved (12):** `Bank physical locations (full-service branches, satellite offices, and ATM-only locations)→BRANCHES`, `parent_chunk_data_dictionary.md_12`, `parent_chunk_data_dictionary.md_7`, `parent_chunk_data_dictionary.md_6`, `ATMS→BRANCHES`, `parent_chunk_data_dictionary.md_5`, `parent_chunk_business_glossary.md_2`, `Bank physical locations (full-service branches, satellite offices, and ATM-only locations)`

**Context previews (first 3):**

1. _Business concept 'Bank physical locations (full-service branches, satellite offices, and ATM-only locations)' is implemented by physical table BRANCHES (columns: branch_id, branch_code, branch_name, b…_

2. _## Entity Relationship Summary  **Key Relationships: ** - customers ←→ accounts (many-to-many via customer_account) - accounts → accounts (self-reference for parent-child hierarchy) - accounts → trans…_

3. _## accounts  **Description: ** Deposit account master table supporting multiple account types (checking, savings, money market, CD, investment). Implements parent-child hierarchy for portfolio aggrega…_

---

### ✅ 19 — How are ATMs related to branches in the schema and what types of ATMs exist?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.6184 | **Gate:** `proceed`

**Expected answer:**
> The atms table has an optional branch_id foreign key referencing branches. When branch_id is NULL, the ATM is standalone and not affiliated with any branch. ATM types are defined by CHECK constraint: Branch (on-premises), DriveThrough (vehicle-accessible), and Standalone (independent locations). Eac…

**System answer:**
> In the schema, ATMs are related to branches through a foreign key: `ATMS` has `branch_id`, which references `BRANCHES.BRANCH_ID` (i.e., `ATMS.BRANCH_ID -> BRANCHES.BRANCH_ID`). The `branch_id` in `ATMS` is nullable, which indicates that some ATMs can exist without a branch (standalone units).

The types of ATMs are captured by the `atm_type` attribute. The business definition lists these types as …

**Sources retrieved (12):** `ATMS→BRANCHES`, `parent_chunk_data_dictionary.md_6`, `parent_chunk_data_dictionary.md_12`, `Automated Teller Machine→ATMS`, `Bank physical locations (full-service branches, satellite offices, and ATM-only locations)→BRANCHES`, `parent_chunk_data_dictionary.md_9`, `parent_chunk_business_glossary.md_3`, `parent_chunk_data_dictionary.md_5`

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
> I cannot find the loan “lifecycle from application to completion” in the retrieved context.

What the knowledge graph does provide is schema-level information for loans in the table `LOANS`: it includes lifecycle-related dates and state fields—`origination_date`, `maturity_date`, and `status`—and it describes the table as tracking “original terms” plus “current balances” for “loan servicing and po…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_10`, `Card security and limits→CARDS`, `parent_chunk_data_dictionary.md_7`, `Account Balances and Status→ACCOUNTS`, `Loan Type (Mortgage, Personal, Auto, HELOC, CreditCard)→LOANS`, `parent_chunk_data_dictionary.md_12`, `parent_chunk_business_glossary.md_2`, `parent_chunk_business_glossary.md_1`

**Context previews (first 3):**

1. _## loans  **Description: ** Loan portfolio table tracking all lending products including mortgages, personal loans, auto loans, HELOCs, and credit cards. Records original terms, amortization schedules…_

2. _Business concept 'Card security and limits' — The table primarily stores card master attributes: security capabilities (chip, contactless, PIN) plus spending limits (credit_limit, daily_limit, atm_dai…_

3. _## accounts  **Description: ** Deposit account master table supporting multiple account types (checking, savings, money market, CD, investment). Implements parent-child hierarchy for portfolio aggrega…_

---

### ✅ 21 — What does preferred customer status mean and how is it tracked in the schema?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.5129 | **Gate:** `proceed`

**Expected answer:**
> Preferred status is tracked via the is_preferred boolean flag in the customers table (default: false). The business glossary states that preferred customers receive waived fees, preferred interest rates, and priority service. The glossary examples show preferred customers with longer tenure and high…

**System answer:**
> In this schema, “preferred customer status” means that the customer is flagged as a preferred (VIP) customer for special treatment.

It is tracked in the physical table `CUSTOMERS` (mapped from the business concept “Core customer dimension table containing master data for all individual and corporate banking customers”) using the column `is_preferred`. The `CUSTOMERS` table also includes other mas…

**Sources retrieved (12):** `Core customer dimension table containing master data for all individual and corporate banking customers→CUSTOMERS`, `parent_chunk_data_dictionary.md_12`, `parent_chunk_data_dictionary.md_11`, `parent_chunk_data_dictionary.md_10`, `parent_chunk_data_dictionary.md_8`, `parent_chunk_data_dictionary.md_7`, `Card security and limits→CARDS`, `CARDS→CUSTOMERS`

**Context previews (first 3):**

1. _Business concept 'Core customer dimension table containing master data for all individual and corporate banking customers' is implemented by physical table CUSTOMERS (columns: customer_id, first_name,…_

2. _## Entity Relationship Summary  **Key Relationships: ** - customers ←→ accounts (many-to-many via customer_account) - accounts → accounts (self-reference for parent-child hierarchy) - accounts → trans…_

3. _## cards  **Description: ** Payment card issuance table for debit, credit, and ATM cards. Links cards to both customer and account. Tracks security features (chip, contactless, PIN), spending limits, …_

---

### ✅ 22 — How does the accounts table support interest tracking and what business rules govern interest?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.3044 | **Gate:** `proceed`

**Expected answer:**
> The accounts table has interest_rate (nullable DECIMAL for the annual rate) and interest_earned (DECIMAL for year-to-date interest credited). The business glossary states that deposit interest is credited monthly (typically the first day of the month) and that APY accounts for compounding effects. P…

**System answer:**
> The `accounts` table supports interest tracking by storing both the interest settings and the accumulated interest for deposit accounts. In particular, the business concept mapping “Account Balances and Status” (implemented by the physical `ACCOUNTS` table) states that it includes deposit-account monetary attributes such as `interest_rate` and `interest_earned` (alongside balances like `current_ba…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_7`, `Account Balances and Status→ACCOUNTS`, `parent_chunk_data_dictionary.md_12`, `parent_chunk_data_dictionary.md_10`, `ACCOUNTS→BRANCHES`, `ACCOUNTS→ACCOUNTS`, `parent_chunk_data_dictionary.md_8`, `parent_chunk_business_glossary.md_2`

**Context previews (first 3):**

1. _## accounts  **Description: ** Deposit account master table supporting multiple account types (checking, savings, money market, CD, investment). Implements parent-child hierarchy for portfolio aggrega…_

2. _Business concept 'Account Balances and Status' — The table stores deposit-account monetary attributes (current_balance, available_balance, minimum_balance, interest_rate, interest_earned, monthly_fee)…_

3. _## Entity Relationship Summary  **Key Relationships: ** - customers ←→ accounts (many-to-many via customer_account) - accounts → accounts (self-reference for parent-child hierarchy) - accounts → trans…_

---

### ✅ 23 — Can an account exist without any customer linked to it?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.1394 | **Gate:** `proceed_with_warning`

**Expected answer:**
> Looking at the schema, there is no database-level constraint that forces every account to have a customer_account row. The accounts table has no direct foreign key to customers — the relationship is through the customer_account junction table with a composite primary key (customer_id, account_id). H…

**System answer:**
> The retrieved context does not state any rule that an `ACCOUNTS` record must have at least one linked row in the `customer_account` junction table. It only specifies that `customer_account` is the many-to-many junction between `customers` and `accounts` (with a composite primary key of `customer_id`, `account_id`) and that “the customer_account junction table requires both customer and account to …

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_8`, `Primary owner designation→CUSTOMER_ACCOUNT`, `CUSTOMER_ACCOUNT→CUSTOMERS`, `parent_chunk_data_dictionary.md_12`, `CUSTOMER_ACCOUNT→ACCOUNTS`, `parent_chunk_data_dictionary.md_11`, `parent_chunk_data_dictionary.md_10`, `parent_chunk_business_glossary.md_3`

**Context previews (first 3):**

1. _## customer_account  **Description: ** Junction table implementing many-to-many relationship between customers and accounts. Supports joint ownership, authorized signers, and custodial relationships. …_

2. _Business concept 'Primary owner designation' — The table includes an is_primary BOOLEAN flag that directly implements whether a customer is designated as the primary owner of an account. While ownersh…_

3. _Relationship: CUSTOMER_ACCOUNT references CUSTOMERS via foreign key CUSTOMER_ID -> CUSTOMERS.CUSTOMER_ID.…_

---

### ✅ 24 — How does the schema handle failed or cancelled transactions?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.2042 | **Gate:** `proceed`

**Expected answer:**
> The transactions table has a status column with CHECK constraint allowing Pending, Posted, Failed, Cancelled, and OnHold states. The business glossary explains that failed transactions are logged for audit but do not affect the account balance — the balance_after field would reflect no change. Poste…

**System answer:**
> The schema models failed or cancelled transactions using the transaction “status” attribute in the transaction fact table (concept **Transaction** / table **transactions**). The business context states transactions flow through states including **Pending → Posted**, and the status values explicitly include **Failed** and **Cancelled** (along with **OnHold**).  

Beyond recording that state in the …

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_9`, `parent_chunk_data_dictionary.md_12`, `parent_chunk_data_dictionary.md_7`, `TRANSACTIONS→ACCOUNTS`, `parent_chunk_business_glossary.md_1`, `parent_chunk_business_glossary.md_0`, `parent_chunk_business_glossary.md_3`, `parent_chunk_business_glossary.md_2`

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
> In the `ATMS` business concept / table `atms`, the operational `status` values an ATM can have are `Operational`, `OutOfService`, and `OutOfCash`.

The context only states that this `status` is used for “availability management.” It does not explicitly define, in operational terms, what additional services are enabled/disabled for `OutOfCash` (or `OutOfService`) beyond the status labels themselves…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_6`, `Card security and limits→CARDS`, `Bank physical locations (full-service branches, satellite offices, and ATM-only locations)→BRANCHES`, `Automated Teller Machine→ATMS`, `ATMS→BRANCHES`, `parent_chunk_data_dictionary.md_12`, `parent_chunk_data_dictionary.md_11`, `Card security and limits`

**Context previews (first 3):**

1. _## atms  **Description: ** ATM locations including branch-attached machines, drive-through ATMs, and standalone units. Tracks cash balances for replenishment scheduling, GPS coordinates for location s…_

2. _Business concept 'Card security and limits' — The table primarily stores card master attributes: security capabilities (chip, contactless, PIN) plus spending limits (credit_limit, daily_limit, atm_dai…_

3. _Business concept 'Bank physical locations (full-service branches, satellite offices, and ATM-only locations)' is implemented by physical table BRANCHES (columns: branch_id, branch_code, branch_name, b…_

---

## Anomalies & Observations

No anomalies detected. All questions grounded with acceptable RAGAS scores.
