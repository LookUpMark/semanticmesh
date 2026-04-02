# AB-11 — 02_intermediate_finance — Run Analysis

**Timestamp:** 2026-04-01 00:25:28  
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
| ER similarity threshold | `0.65` |

## Builder Results

| Metric | Value |
|--------|-------|
| Triplets extracted | 626 |
| Entities resolved | 60 |
| Tables parsed | 8 |
| Tables completed | 8 |

## Query Evaluation Summary

| Metric | Value |
|--------|-------|
| Questions | 25 |
| Grounded | **25/25 (100%)** |
| Avg GT Coverage | 100% |
| Avg Top Score | 0.4756 |
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
> A checking account is a type of deposit account in the `accounts` table, identified by `account_type = Checking`.

From the business glossary, an account is a financial arrangement between a customer and the bank that allows deposit, withdrawal, and management of funds. In this schema, checking accounts are part of the `ACCOUNTS` table’s deposit-account scope, which includes attributes such as `ac…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_7`, `parent_chunk_data_dictionary.md_8`, `FullService branch→TRANSACTIONS`, `parent_chunk_data_dictionary.md_9`, `parent_chunk_data_dictionary.md_10`, `Deposit Account→ACCOUNTS`, `parent_chunk_business_glossary.md_0`, `parent_chunk_business_glossary.md_1`

**Context previews (first 3):**

1. _## accounts  **Description: ** Deposit account master table supporting multiple account types (checking, savings, money market, CD, investment). Implements parent-child hierarchy for portfolio aggrega…_

2. _## customer_account  **Description: ** Junction table implementing many-to-many relationship between customers and accounts. Supports joint ownership, authorized signers, and custodial relationships. …_

3. _Business concept 'FullService branch' — A physical banking location where customers can access in-person services including teller transactions, account opening, loan applications, and financial advis…_

---

### ✅ 2 — What is the difference between a savings account and a money market account?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.6601 | **Gate:** `proceed`

**Expected answer:**
> Both savings and money market are account types defined in the accounts table CHECK constraint. The business glossary Interest section provides example rates: Standard Savings earns 0.25% APY (with monthly compounding), Premium Savings earns 0.50% APY (with daily compounding), while Money Market ear…

**System answer:**
> From the retrieved context, both savings accounts and money market accounts appear only as valid `account_type` values in `ACCOUNTS` / the Account business concept: `Savings` and `MoneyMarket`.

The context does not provide a business definition that distinguishes a savings account from a money market account, so I cannot state the difference between them from this knowledge graph alone.

What the…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_7`, `parent_chunk_data_dictionary.md_10`, `parent_chunk_data_dictionary.md_9`, `Deposit Account→ACCOUNTS`, `parent_chunk_data_dictionary.md_8`, `parent_chunk_data_dictionary.md_12`, `parent_chunk_data_dictionary.md_11`, `parent_chunk_business_glossary.md_0`

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
> In the `Interest` business concept, APR and APY are distinguished as follows: APR is Annual Percentage Rate and is used for loans, while APY is Annual Percentage Yield and is used for deposits. The context also states that APY accounts for compounding, whereas interest in general is expressed as an annual percentage rate.

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
> The retrieved context only shows that KYC is tracked on the `customers` table via the `kyc_status` column, and that valid KYC levels are `Level1`, `Level2`, or `Level3`.

It does not define what `Level2` specifically means, what requirements it represents, or how it differs from `Level1` or `Level3`.

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_12`, `system status updates and customer notifications→CUSTOMERS`, `parent_chunk_data_dictionary.md_7`, `parent_chunk_data_dictionary.md_4`, `parent_chunk_business_glossary.md_0`, `parent_chunk_business_glossary.md_1`, `parent_chunk_data_dictionary.md_5`, `parent_chunk_business_glossary.md_3`

**Context previews (first 3):**

1. _## Entity Relationship Summary  **Key Relationships: ** - customers ←→ accounts (many-to-many via customer_account) - accounts → accounts (self-reference for parent-child hierarchy) - accounts → trans…_

2. _Business concept 'system status updates and customer notifications' is implemented by physical table CUSTOMERS (columns: customer_id, first_name, last_name, tax_id, email, phone, address, city, state,…_

3. _## accounts  **Description: ** Deposit account master table supporting multiple account types (checking, savings, money market, CD, investment). Implements parent-child hierarchy for portfolio aggrega…_

---

### ✅ 5 — How does the schema support different account subtypes and their varying requirements?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.1891 | **Gate:** `proceed_with_warning`

**Expected answer:**
> The accounts table has an account_subtype column (VARCHAR 30, nullable) that stores values like Premium or Standard to differentiate within each account_type. Combined with the minimum_balance and monthly_fee columns, each account can have different requirements configured per subtype. The account_t…

**System answer:**
> The schema supports account subtypes primarily in the `ACCOUNTS` table. It separates broad product category from finer-grained variation by storing both `account_type` and `account_subtype`.

`account_type` captures the major account classes: Checking, Savings, MoneyMarket, CD, and Investment. `account_subtype` is a nullable field used for more specific variants such as Premium, Student, and Stand…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_7`, `parent_chunk_data_dictionary.md_12`, `Deposit Account→ACCOUNTS`, `parent_chunk_data_dictionary.md_8`, `Card→CARDS`, `parent_chunk_data_dictionary.md_9`, `parent_chunk_business_glossary.md_0`, `Deposit Account`

**Context previews (first 3):**

1. _## accounts  **Description: ** Deposit account master table supporting multiple account types (checking, savings, money market, CD, investment). Implements parent-child hierarchy for portfolio aggrega…_

2. _## Entity Relationship Summary  **Key Relationships: ** - customers ←→ accounts (many-to-many via customer_account) - accounts → accounts (self-reference for parent-child hierarchy) - accounts → trans…_

3. _Business concept 'Deposit Account' — The table is explicitly scoped to deposit accounts and includes deposit-product attributes such as interest_rate, interest_earned, minimum_balance, monthly_fee, an…_

---

### ✅ 6 — What types of loan products does the bank offer?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.4020 | **Gate:** `proceed`

**Expected answer:**
> The bank offers five loan types defined by the CHECK constraint on loans.loan_type: (1) Mortgage — secured by real estate, glossary example shows $350,000 at 5.50% APR for 360 months; (2) Personal Loan — unsecured, example $15,000 at 8.50% APR for 48 months; (3) Auto Loan — secured by vehicle, examp…

**System answer:**
> The bank offers these loan product types in the `LOANS` table: Mortgage, Personal, Auto, HELOC, and CreditCard. The `loans` description also says the loan portfolio tracks mortgages, personal loans, auto loans, HELOCs, and credit cards.

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_10`, `parent_chunk_data_dictionary.md_12`, `FullService branch→TRANSACTIONS`, `parent_chunk_data_dictionary.md_7`, `Loan term in months (0 for revolving credit)→LOANS`, `LOANS→CUSTOMERS`, `parent_chunk_business_glossary.md_1`, `parent_chunk_business_glossary.md_2`

**Context previews (first 3):**

1. _## loans  **Description: ** Loan portfolio table tracking all lending products including mortgages, personal loans, auto loans, HELOCs, and credit cards. Records original terms, amortization schedules…_

2. _## Entity Relationship Summary  **Key Relationships: ** - customers ←→ accounts (many-to-many via customer_account) - accounts → accounts (self-reference for parent-child hierarchy) - accounts → trans…_

3. _Business concept 'FullService branch' — A physical banking location where customers can access in-person services including teller transactions, account opening, loan applications, and financial advis…_

---

### ✅ 7 — What is the daily ATM withdrawal limit for standard customers?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.3743 | **Gate:** `proceed`

**Expected answer:**
> The cards table has an atm_daily_limit column with a default value of $500. The business glossary Card Examples confirm this: a standard Debit Card has a $500 ATM limit, while a Premium Debit card has a $2,000 ATM limit. The daily_limit column (default $3,000) controls POS spending separately. These…

**System answer:**
> The retrieved context does not state a numeric daily ATM withdrawal limit for standard customers.

What it does provide is the schema and business structure around that question: the CARDS table stores an `atm_daily_limit` column, so ATM withdrawal limits are tracked at the card level. That table links each card to both `customer_id` and `account_id`. Separately, the ACCOUNTS table includes an `ac…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_11`, `Card→CARDS`, `parent_chunk_data_dictionary.md_6`, `parent_chunk_data_dictionary.md_12`, `parent_chunk_data_dictionary.md_7`, `Branches→BRANCHES`, `Automated Teller Machine→ATMS`, `parent_chunk_business_glossary.md_3`

**Context previews (first 3):**

1. _## cards  **Description: ** Payment card issuance table for debit, credit, and ATM cards. Links cards to both customer and account. Tracks security features (chip, contactless, PIN), spending limits, …_

2. _Business concept 'Card' — The table is explicitly described as storing debit, credit, and ATM cards, with core attributes such as card number, type, network, holder name, expiration date, CVV, limits,…_

3. _## atms  **Description: ** ATM locations including branch-attached machines, drive-through ATMs, and standalone units. Tracks cash balances for replenishment scheduling, GPS coordinates for location s…_

---

### ✅ 8 — What is the difference between a parent account and a child account?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.3098 | **Gate:** `proceed`

**Expected answer:**
> The accounts table supports parent-child hierarchies through the parent_account_id self-referencing foreign key, with a CHECK constraint preventing circular references (parent_account_id != account_id). The data dictionary describes this as supporting portfolio aggregation where parent accounts (typ…

**System answer:**
> In this schema, the difference is defined by the self-referencing hierarchy in `ACCOUNTS` using `parent_account_id`.

A parent account is an `ACCOUNTS` record that other accounts point to through `ACCOUNTS.PARENT_ACCOUNT_ID -> ACCOUNTS.ACCOUNT_ID`. Its purpose is portfolio aggregation. The context specifically says the hierarchy supports cases where investment accounts contain child accounts.

A c…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_7`, `parent_chunk_data_dictionary.md_12`, `ACCOUNTS→ACCOUNTS`, `Deposit Account→ACCOUNTS`, `parent_chunk_data_dictionary.md_8`, `parent_chunk_data_dictionary.md_9`, `parent_chunk_data_dictionary.md_11`, `parent_chunk_data_dictionary.md_10`

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
> The retrieved context does not define what `Frozen` means for a card.

It confirms that the `CARDS` table has a `status` column (`CARDS.status`) and that the Card business concept includes “status” as a core attribute, but it does not list allowed card status values or explain any card status meanings.

The only place `Frozen` appears in the context is under the `Account` business glossary, where …

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_7`, `parent_chunk_data_dictionary.md_10`, `parent_chunk_data_dictionary.md_11`, `Card→CARDS`, `parent_chunk_data_dictionary.md_6`, `parent_chunk_data_dictionary.md_9`, `parent_chunk_business_glossary.md_0`, `parent_chunk_business_glossary.md_3`

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
> The `TRANSACTIONS` table tracks the impact of each transaction on account balances primarily through the `balance_after` column, which stores the account balance after that transaction is applied. This lets each row show not just the transaction amount, but the resulting balance state for the linked account.

The table is tied to the affected account through `account_id`, a foreign key to `ACCOUNT…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_9`, `TRANSACTIONS→ACCOUNTS`, `parent_chunk_data_dictionary.md_7`, `FullService branch→TRANSACTIONS`, `Deposit Account→ACCOUNTS`, `ACCOUNTS→BRANCHES`, `ACCOUNTS→ACCOUNTS`, `parent_chunk_data_dictionary.md_10`

**Context previews (first 3):**

1. _## transactions  **Description: ** Transaction fact table recording all account activity. Supports multiple transaction types including debits, credits, transfers, and withdrawals. Tracks calculated f…_

2. _Relationship: TRANSACTIONS references ACCOUNTS via foreign key ACCOUNT_ID -> ACCOUNTS.ACCOUNT_ID.…_

3. _## accounts  **Description: ** Deposit account master table supporting multiple account types (checking, savings, money market, CD, investment). Implements parent-child hierarchy for portfolio aggrega…_

---

### ✅ 11 — How does the customer_account junction table support multiple ownership types?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.9865 | **Gate:** `proceed`

**Expected answer:**
> The customer_account table implements a many-to-many relationship between customers and accounts with a composite primary key (customer_id, account_id). It supports four relationship types via CHECK constraint: Owner, JointOwner, AuthorizedSigner, and Custodian. The is_primary flag designates the pr…

**System answer:**
> The `customer_account` table supports multiple ownership types by acting as a many-to-many junction between `customers` and `accounts`, so a single customer can be linked to multiple accounts and a single account can be linked to multiple customers.

It distinguishes the role each customer has on an account through the `relationship_type` column, which is described with these values: `Owner`, `Joi…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_8`, `Customer Account Relationship→CUSTOMER_ACCOUNT`, `parent_chunk_data_dictionary.md_12`, `CUSTOMER_ACCOUNT→CUSTOMERS`, `parent_chunk_data_dictionary.md_7`, `CUSTOMER_ACCOUNT→ACCOUNTS`, `parent_chunk_data_dictionary.md_9`, `parent_chunk_data_dictionary.md_11`

**Context previews (first 3):**

1. _## customer_account  **Description: ** Junction table implementing many-to-many relationship between customers and accounts. Supports joint ownership, authorized signers, and custodial relationships. …_

2. _Business concept 'Customer Account Relationship' — The DDL explicitly describes a junction table for a many-to-many relationship between customers and accounts, with relationship_type, is_primary, own…_

3. _## Entity Relationship Summary  **Key Relationships: ** - customers ←→ accounts (many-to-many via customer_account) - accounts → accounts (self-reference for parent-child hierarchy) - accounts → trans…_

---

### ✅ 12 — What is the difference between current_balance and available_balance in the accounts table?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.8328 | **Gate:** `proceed`

**Expected answer:**
> The accounts table tracks two separate balance fields: current_balance includes all transactions including pending ones, while available_balance excludes holds and pending transactions and represents what the customer can actually withdraw. The business glossary confirms this distinction, stating th…

**System answer:**
> The retrieved context shows that the `accounts` table stores both `current_balance` and `available_balance` as separate balance fields, and the Account glossary explicitly treats “Current Balance vs. Available Balance” as a key attribute of an account.

However, the retrieved context does not explicitly define the difference between those two fields or give a calculation rule for each one. It only…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_7`, `Deposit Account→ACCOUNTS`, `parent_chunk_data_dictionary.md_10`, `parent_chunk_data_dictionary.md_6`, `parent_chunk_data_dictionary.md_9`, `ACCOUNTS→ACCOUNTS`, `ACCOUNTS→BRANCHES`, `FullService branch→TRANSACTIONS`

**Context previews (first 3):**

1. _## accounts  **Description: ** Deposit account master table supporting multiple account types (checking, savings, money market, CD, investment). Implements parent-child hierarchy for portfolio aggrega…_

2. _Business concept 'Deposit Account' — The table is explicitly scoped to deposit accounts and includes deposit-product attributes such as interest_rate, interest_earned, minimum_balance, monthly_fee, an…_

3. _## loans  **Description: ** Loan portfolio table tracking all lending products including mortgages, personal loans, auto loans, HELOCs, and credit cards. Records original terms, amortization schedules…_

---

### ✅ 13 — How are loans linked to both customers and accounts in the schema?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.8105 | **Gate:** `proceed`

**Expected answer:**
> The loans table has a customer_id foreign key referencing the customers table (the borrower) and an optional account_id foreign key referencing the accounts table (for linked payment accounts). Each loan belongs to exactly one customer, and can optionally be connected to an account for automatic pay…

**System answer:**
> In the schema, loans are linked through the `LOANS` table using two foreign keys. `LOANS.customer_id` is a required foreign key to `CUSTOMERS.customer_id`, so each loan must be associated with a customer as the borrower. The relationship summary also describes this as `customers → loans` being one-to-many, meaning a customer can have multiple loans.

`LOANS.account_id` is a foreign key to `ACCOUNT…

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
> The system supports these transaction types in `transactions.transaction_type`: Debit, Credit, Transfer, Payment, Withdrawal, Deposit, and Fee. The `transactions` table description also says it records all account activity and explicitly supports debits, credits, transfers, and withdrawals, while the `Transaction` business definition broadens that to the full set above.

The status lifecycle is de…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_9`, `parent_chunk_data_dictionary.md_7`, `FullService branch→TRANSACTIONS`, `system status updates and customer notifications→CUSTOMERS`, `parent_chunk_data_dictionary.md_6`, `Automated Teller Machine→ATMS`, `parent_chunk_data_dictionary.md_11`, `parent_chunk_business_glossary.md_1`

**Context previews (first 3):**

1. _## transactions  **Description: ** Transaction fact table recording all account activity. Supports multiple transaction types including debits, credits, transfers, and withdrawals. Tracks calculated f…_

2. _## accounts  **Description: ** Deposit account master table supporting multiple account types (checking, savings, money market, CD, investment). Implements parent-child hierarchy for portfolio aggrega…_

3. _Business concept 'FullService branch' — A physical banking location where customers can access in-person services including teller transactions, account opening, loan applications, and financial advis…_

---

### ✅ 15 — How does the schema support joint account ownership between multiple customers?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.4870 | **Gate:** `proceed`

**Expected answer:**
> Joint ownership is implemented through the customer_account junction table, which creates a many-to-many relationship between customers and accounts. Each row has a relationship_type CHECK constraint allowing Owner, JointOwner, AuthorizedSigner, or Custodian. The ownership_percentage field (DECIMAL …

**System answer:**
> The schema supports joint account ownership through the `customer_account` table, which is explicitly a junction table between `customers` and `accounts`. This creates a many-to-many relationship, so one customer can be linked to multiple accounts and one account can be linked to multiple customers.

The implementation details in `CUSTOMER_ACCOUNT` are what make joint ownership possible. Its compo…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_8`, `Customer Account Relationship→CUSTOMER_ACCOUNT`, `parent_chunk_data_dictionary.md_12`, `parent_chunk_data_dictionary.md_7`, `parent_chunk_data_dictionary.md_11`, `CUSTOMER_ACCOUNT→CUSTOMERS`, `CUSTOMER_ACCOUNT→ACCOUNTS`, `Customer Account Relationship`

**Context previews (first 3):**

1. _## customer_account  **Description: ** Junction table implementing many-to-many relationship between customers and accounts. Supports joint ownership, authorized signers, and custodial relationships. …_

2. _Business concept 'Customer Account Relationship' — The DDL explicitly describes a junction table for a many-to-many relationship between customers and accounts, with relationship_type, is_primary, own…_

3. _## Entity Relationship Summary  **Key Relationships: ** - customers ←→ accounts (many-to-many via customer_account) - accounts → accounts (self-reference for parent-child hierarchy) - accounts → trans…_

---

### ✅ 16 — What information does the cards table track and how are cards linked to customers and accounts?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.9528 | **Gate:** `proceed`

**Expected answer:**
> The cards table links to both accounts (account_id FK) and customers (customer_id FK), tracking card_type (Debit/Credit/ATM), card_network (Visa/Mastercard/Discover/AmericanExpress), card_number, cardholder name, expiration_date, and CVV. For spending controls it stores credit_limit (nullable, for c…

**System answer:**
> The `CARDS` table is a payment card issuance table for debit, credit, and ATM cards. It stores card-level information including the card number, card type, card network, cardholder name, expiration date, CVV, credit limit, daily limit, ATM daily limit, whether a PIN is set, whether the card has a chip, whether contactless is enabled, card status, issued date, last used date, and created timestamp.…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_11`, `CARDS→CUSTOMERS`, `CARDS→ACCOUNTS`, `parent_chunk_data_dictionary.md_10`, `Card→CARDS`, `CUSTOMER_ACCOUNT→CUSTOMERS`, `CUSTOMER_ACCOUNT→ACCOUNTS`, `parent_chunk_data_dictionary.md_8`

**Context previews (first 3):**

1. _## cards  **Description: ** Payment card issuance table for debit, credit, and ATM cards. Links cards to both customer and account. Tracks security features (chip, contactless, PIN), spending limits, …_

2. _Relationship: CARDS references CUSTOMERS via foreign key CUSTOMER_ID -> CUSTOMERS.CUSTOMER_ID.…_

3. _Relationship: CARDS references ACCOUNTS via foreign key ACCOUNT_ID -> ACCOUNTS.ACCOUNT_ID.…_

---

### ✅ 17 — How does the schema handle interest rates across deposit and loan products?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0692 | **Gate:** `proceed_with_warning`

**Expected answer:**
> Interest rates are stored differently for deposits and loans. The accounts table has an interest_rate column (nullable DECIMAL 5,4) and interest_earned for year-to-date tracking. The loans table has its own interest_rate column representing APR. The business glossary explains that APR (Annual Percen…

**System answer:**
> The schema handles interest rates directly on both deposit and loan product tables, but in different business contexts.

For deposit products, interest is stored on the `ACCOUNTS` table, which is explicitly mapped to the business concept `Deposit Account`. Relevant columns are `interest_rate` and `interest_earned`, along with other deposit-product fields such as `current_balance`, `available_balan…

**Sources retrieved (12):** `Deposit Account→ACCOUNTS`, `parent_chunk_data_dictionary.md_12`, `parent_chunk_data_dictionary.md_10`, `parent_chunk_data_dictionary.md_7`, `Loan term in months (0 for revolving credit)→LOANS`, `LOANS→CUSTOMERS`, `LOANS→ACCOUNTS`, `Deposit Account`

**Context previews (first 3):**

1. _Business concept 'Deposit Account' — The table is explicitly scoped to deposit accounts and includes deposit-product attributes such as interest_rate, interest_earned, minimum_balance, monthly_fee, an…_

2. _## Entity Relationship Summary  **Key Relationships: ** - customers ←→ accounts (many-to-many via customer_account) - accounts → accounts (self-reference for parent-child hierarchy) - accounts → trans…_

3. _## loans  **Description: ** Loan portfolio table tracking all lending products including mortgages, personal loans, auto loans, HELOCs, and credit cards. Records original terms, amortization schedules…_

---

### ✅ 18 — What types of branches does the bank operate and how do they differ in capabilities?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.1556 | **Gate:** `proceed_with_warning`

**Expected answer:**
> The branches table supports three types via CHECK constraint: FullService, Satellite, and ATMOnly. The business glossary details each: FullService branches offer complete banking services including loan origination, financial advisors, and safe deposit boxes; Satellite branches have limited hours an…

**System answer:**
> The bank operates three branch types in the `branches` / `BRANCHES` table: `FullService`, `Satellite`, and `ATMOnly`. The `branch_type` column is defined as `FullService/Satellite/ATMOnly`, and the Branches business concept says the master list spans those three location types.

The only branch type whose capabilities are explicitly described in the retrieved context is `FullService branch`. It is…

**Sources retrieved (12):** `Branches→BRANCHES`, `FullService branch→TRANSACTIONS`, `parent_chunk_data_dictionary.md_12`, `parent_chunk_data_dictionary.md_7`, `parent_chunk_data_dictionary.md_6`, `parent_chunk_data_dictionary.md_5`, `Branches`, `parent_chunk_business_glossary.md_2`

**Context previews (first 3):**

1. _Business concept 'Branches' — The table is the master list of physical banking locations and includes branch-level identifiers, address, hours, manager, status, and subtype fields spanning FullService…_

2. _Business concept 'FullService branch' — A physical banking location where customers can access in-person services including teller transactions, account opening, loan applications, and financial advis…_

3. _## Entity Relationship Summary  **Key Relationships: ** - customers ←→ accounts (many-to-many via customer_account) - accounts → accounts (self-reference for parent-child hierarchy) - accounts → trans…_

---

### ✅ 19 — How are ATMs related to branches in the schema and what types of ATMs exist?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.6184 | **Gate:** `proceed`

**Expected answer:**
> The atms table has an optional branch_id foreign key referencing branches. When branch_id is NULL, the ATM is standalone and not affiliated with any branch. ATM types are defined by CHECK constraint: Branch (on-premises), DriveThrough (vehicle-accessible), and Standalone (independent locations). Eac…

**System answer:**
> In the schema, ATMs are stored in the ATMS table and branches are stored in BRANCHES. The relationship is ATMS.branch_id → BRANCHES.branch_id. This means each ATM can optionally reference a branch, and the overall cardinality is branches → atms as one-to-many: one branch can have many ATMs.

The relationship is optional on the ATM side because ATMS.branch_id is nullable. The context explicitly say…

**Sources retrieved (12):** `ATMS→BRANCHES`, `parent_chunk_data_dictionary.md_6`, `parent_chunk_data_dictionary.md_12`, `Branches→BRANCHES`, `Automated Teller Machine→ATMS`, `parent_chunk_business_glossary.md_3`, `Branches`, `parent_chunk_data_dictionary.md_5`

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
> The retrieved context does not define a full loan workflow with application stages, approval steps, or completion outcomes. What it does state is this: a customer can make a loan application at a FullService branch, which is defined as a physical banking location offering in-person services including loan applications and financial advisory services.

After a loan exists, its lifecycle is represen…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_10`, `parent_chunk_data_dictionary.md_7`, `Loan term in months (0 for revolving credit)→LOANS`, `parent_chunk_data_dictionary.md_12`, `FullService branch→TRANSACTIONS`, `parent_chunk_business_glossary.md_2`, `parent_chunk_business_glossary.md_1`, `Loan term in months (0 for revolving credit)`

**Context previews (first 3):**

1. _## loans  **Description: ** Loan portfolio table tracking all lending products including mortgages, personal loans, auto loans, HELOCs, and credit cards. Records original terms, amortization schedules…_

2. _## accounts  **Description: ** Deposit account master table supporting multiple account types (checking, savings, money market, CD, investment). Implements parent-child hierarchy for portfolio aggrega…_

3. _Business concept 'Loan term in months (0 for revolving credit)' is implemented by physical table LOANS (columns: loan_id, customer_id, loan_type, account_id, principal_amount, interest_rate, term_mont…_

---

### ✅ 21 — What does preferred customer status mean and how is it tracked in the schema?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.5129 | **Gate:** `proceed`

**Expected answer:**
> Preferred status is tracked via the is_preferred boolean flag in the customers table (default: false). The business glossary states that preferred customers receive waived fees, preferred interest rates, and priority service. The glossary examples show preferred customers with longer tenure and high…

**System answer:**
> Preferred customer status means the customer is flagged for VIP treatment. In the schema, this is tracked directly on the `CUSTOMERS` table, which is the core customer master table, using the `is_preferred` column.

From the context, `CUSTOMERS` stores master data for all individual and corporate banking customers and includes “preferred customer flags for VIP treatment.” There is no separate pref…

**Sources retrieved (12):** `system status updates and customer notifications→CUSTOMERS`, `parent_chunk_data_dictionary.md_12`, `parent_chunk_data_dictionary.md_11`, `parent_chunk_data_dictionary.md_10`, `parent_chunk_data_dictionary.md_8`, `parent_chunk_data_dictionary.md_7`, `Card→CARDS`, `CARDS→CUSTOMERS`

**Context previews (first 3):**

1. _Business concept 'system status updates and customer notifications' is implemented by physical table CUSTOMERS (columns: customer_id, first_name, last_name, tax_id, email, phone, address, city, state,…_

2. _## Entity Relationship Summary  **Key Relationships: ** - customers ←→ accounts (many-to-many via customer_account) - accounts → accounts (self-reference for parent-child hierarchy) - accounts → trans…_

3. _## cards  **Description: ** Payment card issuance table for debit, credit, and ATM cards. Links cards to both customer and account. Tracks security features (chip, contactless, PIN), spending limits, …_

---

### ✅ 22 — How does the accounts table support interest tracking and what business rules govern interest?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.3044 | **Gate:** `proceed`

**Expected answer:**
> The accounts table has interest_rate (nullable DECIMAL for the annual rate) and interest_earned (DECIMAL for year-to-date interest credited). The business glossary states that deposit interest is credited monthly (typically the first day of the month) and that APY accounts for compounding effects. P…

**System answer:**
> The `ACCOUNTS` table supports interest tracking directly at the account level because it is explicitly scoped to deposit accounts and includes the deposit-product columns `interest_rate` and `interest_earned`, along with related balance and product fields such as `current_balance`, `available_balance`, `minimum_balance`, and `monthly_fee`. The table description also states that it tracks interest …

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_7`, `Deposit Account→ACCOUNTS`, `parent_chunk_data_dictionary.md_12`, `parent_chunk_data_dictionary.md_10`, `ACCOUNTS→BRANCHES`, `ACCOUNTS→ACCOUNTS`, `parent_chunk_data_dictionary.md_8`, `Loan term in months (0 for revolving credit)→LOANS`

**Context previews (first 3):**

1. _## accounts  **Description: ** Deposit account master table supporting multiple account types (checking, savings, money market, CD, investment). Implements parent-child hierarchy for portfolio aggrega…_

2. _Business concept 'Deposit Account' — The table is explicitly scoped to deposit accounts and includes deposit-product attributes such as interest_rate, interest_earned, minimum_balance, monthly_fee, an…_

3. _## Entity Relationship Summary  **Key Relationships: ** - customers ←→ accounts (many-to-many via customer_account) - accounts → accounts (self-reference for parent-child hierarchy) - accounts → trans…_

---

### ✅ 23 — Can an account exist without any customer linked to it?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.2188 | **Gate:** `proceed`

**Expected answer:**
> Looking at the schema, there is no database-level constraint that forces every account to have a customer_account row. The accounts table has no direct foreign key to customers — the relationship is through the customer_account junction table with a composite primary key (customer_id, account_id). H…

**System answer:**
> The retrieved context does not explicitly answer that.

What it does say is that `CUSTOMER_ACCOUNT` is the junction table for the many-to-many relationship between customers and accounts, and that the junction table “requires both customer and account to exist” when a link row is created (`CUSTOMER_ACCOUNT.customer_id -> CUSTOMERS.customer_id` and `CUSTOMER_ACCOUNT.account_id -> ACCOUNTS.account_i…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_8`, `Customer Account Relationship→CUSTOMER_ACCOUNT`, `CUSTOMER_ACCOUNT→CUSTOMERS`, `parent_chunk_data_dictionary.md_12`, `CUSTOMER_ACCOUNT→ACCOUNTS`, `parent_chunk_data_dictionary.md_11`, `parent_chunk_data_dictionary.md_10`, `Customer Account Relationship`

**Context previews (first 3):**

1. _## customer_account  **Description: ** Junction table implementing many-to-many relationship between customers and accounts. Supports joint ownership, authorized signers, and custodial relationships. …_

2. _Business concept 'Customer Account Relationship' — The DDL explicitly describes a junction table for a many-to-many relationship between customers and accounts, with relationship_type, is_primary, own…_

3. _Relationship: CUSTOMER_ACCOUNT references CUSTOMERS via foreign key CUSTOMER_ID -> CUSTOMERS.CUSTOMER_ID.…_

---

### ✅ 24 — How does the schema handle failed or cancelled transactions?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.2042 | **Gate:** `proceed`

**Expected answer:**
> The transactions table has a status column with CHECK constraint allowing Pending, Posted, Failed, Cancelled, and OnHold states. The business glossary explains that failed transactions are logged for audit but do not affect the account balance — the balance_after field would reflect no change. Poste…

**System answer:**
> The schema handles failed or cancelled transactions by recording them in the `transactions` table with a `status` value. The `Transaction` business concept explicitly lists transaction statuses as `Pending`, `Posted`, `Failed`, `Cancelled`, and `OnHold`, and the `TRANSACTIONS` table mapping includes a `status` column alongside `transaction_id`, `account_id`, `transaction_type`, `amount`, `currency…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_9`, `parent_chunk_data_dictionary.md_12`, `parent_chunk_data_dictionary.md_7`, `TRANSACTIONS→ACCOUNTS`, `FullService branch→TRANSACTIONS`, `parent_chunk_business_glossary.md_1`, `parent_chunk_business_glossary.md_0`, `parent_chunk_business_glossary.md_3`

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
> From the retrieved context, an ATM can have these status values: Operational, OutOfService, and OutOfCash. The ATM concept says status is used for availability management, and the ATMS table stores this status along with feature flags such as supports_deposit and supports_cardless.

What can be stated confidently is:
Operational indicates the ATM is available for use.
OutOfService indicates the AT…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_6`, `Automated Teller Machine→ATMS`, `Branches→BRANCHES`, `Card→CARDS`, `ATMS→BRANCHES`, `parent_chunk_business_glossary.md_3`, `parent_chunk_data_dictionary.md_5`, `parent_chunk_business_glossary.md_1`

**Context previews (first 3):**

1. _## atms  **Description: ** ATM locations including branch-attached machines, drive-through ATMs, and standalone units. Tracks cash balances for replenishment scheduling, GPS coordinates for location s…_

2. _Business concept 'Automated Teller Machine' — The table stores ATM identifiers, codes, location, geographic coordinates, type, status, cash balance, replenishment timestamp, and feature flags such as …_

3. _Business concept 'Branches' — The table is the master list of physical banking locations and includes branch-level identifiers, address, hours, manager, status, and subtype fields spanning FullService…_

---

## Anomalies & Observations

No anomalies detected. All questions grounded with acceptable RAGAS scores.
