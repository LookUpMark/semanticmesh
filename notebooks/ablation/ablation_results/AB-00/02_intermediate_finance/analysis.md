# AB-00 — 02_intermediate_finance — Run Analysis

**Timestamp:** 2026-03-30 18:17:59  
**Run tag:** `post-fix-v5`

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
| Triplets extracted | 631 |
| Entities resolved | 237 |
| Tables parsed | 8 |
| Tables completed | 8 |

## Query Evaluation Summary

| Metric | Value |
|--------|-------|
| Questions | 25 |
| Grounded | **25/25 (100%)** |
| Avg GT Coverage | 100% |
| Avg Top Score | 0.4836 |
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
> A checking account is an Account whose `account_type` is `Checking` in the `accounts` table.

From the business glossary, an Account is “a financial arrangement between a customer and the bank that allows deposit, withdrawal, and management of funds.” In this schema, checking is one of the valid account types alongside `Savings`, `MoneyMarket`, `CD`, and `Investment`.

A checking account therefore…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_7`, `parent_chunk_data_dictionary.md_8`, `parent_chunk_data_dictionary.md_9`, `parent_chunk_data_dictionary.md_10`, `parent_chunk_data_dictionary.md_12`, `balances, interest accrual, fees, and account lifecycle status→ACCOUNTS`, `all account activity→TRANSACTIONS`, `parent_chunk_business_glossary.md_0`

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
> The retrieved context does not define a business difference between a savings account and a money market account.

What it does say is that both Savings and MoneyMarket are valid `account_type` values for the `ACCOUNTS` table and for the `Account` business concept. In the schema, accounts of these types are tracked using the same core attributes, including `current_balance`, `available_balance`, `…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_7`, `parent_chunk_data_dictionary.md_10`, `parent_chunk_data_dictionary.md_9`, `parent_chunk_data_dictionary.md_8`, `parent_chunk_data_dictionary.md_12`, `parent_chunk_data_dictionary.md_11`, `balances, interest accrual, fees, and account lifecycle status→ACCOUNTS`, `LOANS→ACCOUNTS`

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
> From the `Interest` business concept, APR is Annual Percentage Rate and is used for loans, while APY is Annual Percentage Yield and is used for deposits.

APR relates to the cost of borrowing money. APY relates to the return on depositing money. The context also states that APY accounts for compounding.

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
> The retrieved context does not define the meaning of “KYC Level 2.” It only states that in the retail banking schema, customer KYC is tracked in the `customers` table via `kyc_status`, and that valid KYC levels are `Level1`, `Level2`, or `Level3`.

So, from the available context, “KYC Level 2” is one of the allowed KYC status values for a customer, but its specific business definition is not provi…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_12`, `Customer Master Data→CUSTOMERS`, `parent_chunk_data_dictionary.md_7`, `parent_chunk_data_dictionary.md_4`, `parent_chunk_business_glossary.md_0`, `Customer Master Data`, `parent_chunk_business_glossary.md_1`, `parent_chunk_data_dictionary.md_5`

**Context previews (first 3):**

1. _## Entity Relationship Summary  **Key Relationships: ** - customers ←→ accounts (many-to-many via customer_account) - accounts → accounts (self-reference for parent-child hierarchy) - accounts → trans…_

2. _Business concept 'Customer Master Data' — The table description explicitly says it is the core customer dimension containing master data for all individual and corporate banking customers, which align…_

3. _## accounts  **Description: ** Deposit account master table supporting multiple account types (checking, savings, money market, CD, investment). Implements parent-child hierarchy for portfolio aggrega…_

---

### ✅ 5 — How does the schema support different account subtypes and their varying requirements?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.1891 | **Gate:** `proceed_with_warning`

**Expected answer:**
> The accounts table has an account_subtype column (VARCHAR 30, nullable) that stores values like Premium or Standard to differentiate within each account_type. Combined with the minimum_balance and monthly_fee columns, each account can have different requirements configured per subtype. The account_t…

**System answer:**
> The schema supports account variation primarily in the `accounts` table. It includes both `account_type` and `account_subtype`, where `account_type` identifies the main category of account and is defined as `Checking`, `Savings`, `MoneyMarket`, `CD`, or `Investment`, and `account_subtype` is a nullable field for more specific variants such as `Premium`, `Student`, or `Standard`.

The same `account…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_7`, `parent_chunk_data_dictionary.md_12`, `balances, interest accrual, fees, and account lifecycle status→ACCOUNTS`, `parent_chunk_data_dictionary.md_8`, `parent_chunk_data_dictionary.md_9`, `all account activity→TRANSACTIONS`, `Owner/JointOwner/AuthorizedSigner/Custodian→CUSTOMER_ACCOUNT`, `parent_chunk_data_dictionary.md_11`

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
> The bank’s loan products, as described by the `LOANS` table and its business concept, are mortgages, personal loans, auto loans, HELOCs, and credit cards. In the `loan_type` column, these appear as `Mortgage`, `Personal`, `Auto`, `HELOC`, and `CreditCard`.

**Sources retrieved (12):** `Loan portfolio table tracking all lending products including mortgages, personal loans, auto loans, HELOCs, and credit cards→LOANS`, `parent_chunk_data_dictionary.md_10`, `parent_chunk_data_dictionary.md_12`, `parent_chunk_data_dictionary.md_7`, `LOANS→CUSTOMERS`, `Customer Master Data→CUSTOMERS`, `Loan portfolio table tracking all lending products including mortgages, personal loans, auto loans, HELOCs, and credit cards`, `parent_chunk_business_glossary.md_1`

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
> The retrieved context does not provide a numeric daily ATM withdrawal limit for standard customers.

What it does show is that the `cards` table stores an `atm_daily_limit` column, and the business concept mapping for `CARDS` includes that same field. The `accounts` table also shows `account_subtype` can include examples like `Standard`, but the context does not define any rule that maps a standar…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_11`, `Card ID and Card Number (PAN)→CARDS`, `parent_chunk_data_dictionary.md_6`, `parent_chunk_data_dictionary.md_12`, `parent_chunk_data_dictionary.md_7`, `parent_chunk_data_dictionary.md_8`, `parent_chunk_business_glossary.md_3`, `parent_chunk_business_glossary.md_1`

**Context previews (first 3):**

1. _## cards  **Description: ** Payment card issuance table for debit, credit, and ATM cards. Links cards to both customer and account. Tracks security features (chip, contactless, PIN), spending limits, …_

2. _Business concept 'Card ID and Card Number (PAN)' is implemented by physical table CARDS (columns: card_id, account_id, customer_id, card_number, card_type, card_network, card_name, expiration_date, cv…_

3. _## atms  **Description: ** ATM locations including branch-attached machines, drive-through ATMs, and standalone units. Tracks cash balances for replenishment scheduling, GPS coordinates for location s…_

---

### ✅ 8 — What is the difference between a parent account and a child account?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.3098 | **Gate:** `proceed`

**Expected answer:**
> The accounts table supports parent-child hierarchies through the parent_account_id self-referencing foreign key, with a CHECK constraint preventing circular references (parent_account_id != account_id). The data dictionary describes this as supporting portfolio aggregation where parent accounts (typ…

**System answer:**
> In the `accounts` table, a parent account is an account that other accounts reference through `parent_account_id`, while a child account is an account whose `parent_account_id` points to another row in `ACCOUNTS.ACCOUNT_ID`.

The purpose of this relationship is hierarchical portfolio aggregation: the schema says `accounts` supports a parent-child hierarchy, and specifically notes that investment a…

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
> The retrieved context does not define what the card status 'Frozen' means.

What the context does say is that the `cards` table includes a `status` column and tracks card status, but no status values or business rule definitions for card statuses are provided. The only place 'Frozen' appears in the retrieved context is for the business concept Account, where account status values include Active, D…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_7`, `parent_chunk_data_dictionary.md_10`, `parent_chunk_data_dictionary.md_11`, `parent_chunk_data_dictionary.md_6`, `parent_chunk_data_dictionary.md_9`, `Card ID and Card Number (PAN)→CARDS`, `parent_chunk_business_glossary.md_0`, `parent_chunk_business_glossary.md_3`

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
> The `TRANSACTIONS` table tracks balance impact in two complementary ways.

First, each row is tied to a specific account through `account_id`, which is a foreign key to `ACCOUNTS.ACCOUNT_ID`. That establishes which account the transaction affects.

Second, the table stores both the transaction characteristics and the resulting balance state. The relevant columns are `transaction_type`, `amount`, `…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_9`, `TRANSACTIONS→ACCOUNTS`, `all account activity→TRANSACTIONS`, `parent_chunk_data_dictionary.md_7`, `balances, interest accrual, fees, and account lifecycle status→ACCOUNTS`, `ACCOUNTS→BRANCHES`, `ACCOUNTS→ACCOUNTS`, `parent_chunk_data_dictionary.md_10`

**Context previews (first 3):**

1. _## transactions  **Description: ** Transaction fact table recording all account activity. Supports multiple transaction types including debits, credits, transfers, and withdrawals. Tracks calculated f…_

2. _Relationship: TRANSACTIONS references ACCOUNTS via foreign key ACCOUNT_ID -> ACCOUNTS.ACCOUNT_ID.…_

3. _Business concept 'all account activity' is implemented by physical table TRANSACTIONS (columns: transaction_id, account_id, transaction_type, amount, currency, transaction_date, status, balance_after,…_

---

### ✅ 11 — How does the customer_account junction table support multiple ownership types?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.9865 | **Gate:** `proceed`

**Expected answer:**
> The customer_account table implements a many-to-many relationship between customers and accounts with a composite primary key (customer_id, account_id). It supports four relationship types via CHECK constraint: Owner, JointOwner, AuthorizedSigner, and Custodian. The is_primary flag designates the pr…

**System answer:**
> The `customer_account` table supports multiple ownership types by implementing the many-to-many relationship between `customers` and `accounts`, so a single customer can be linked to multiple accounts and a single account can be linked to multiple customers.

It captures the ownership or access role in `relationship_type`, which is defined as `Owner`, `JointOwner`, `AuthorizedSigner`, or `Custodia…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_8`, `Owner/JointOwner/AuthorizedSigner/Custodian→CUSTOMER_ACCOUNT`, `parent_chunk_data_dictionary.md_12`, `CUSTOMER_ACCOUNT→CUSTOMERS`, `parent_chunk_data_dictionary.md_7`, `CUSTOMER_ACCOUNT→ACCOUNTS`, `parent_chunk_data_dictionary.md_9`, `parent_chunk_data_dictionary.md_11`

**Context previews (first 3):**

1. _## customer_account  **Description: ** Junction table implementing many-to-many relationship between customers and accounts. Supports joint ownership, authorized signers, and custodial relationships. …_

2. _Business concept 'Owner/JointOwner/AuthorizedSigner/Custodian' is implemented by physical table CUSTOMER_ACCOUNT (columns: customer_id, account_id, relationship_type, is_primary, ownership_percentage,…_

3. _## Entity Relationship Summary  **Key Relationships: ** - customers ←→ accounts (many-to-many via customer_account) - accounts → accounts (self-reference for parent-child hierarchy) - accounts → trans…_

---

### ✅ 12 — What is the difference between current_balance and available_balance in the accounts table?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.8328 | **Gate:** `proceed`

**Expected answer:**
> The accounts table tracks two separate balance fields: current_balance includes all transactions including pending ones, while available_balance excludes holds and pending transactions and represents what the customer can actually withdraw. The business glossary confirms this distinction, stating th…

**System answer:**
> The retrieved context shows that `ACCOUNTS` stores both `current_balance` and `available_balance` as separate columns, and the business glossary identifies “Current Balance vs. Available Balance” as a key account attribute. However, the exact business rule defining how `current_balance` differs from `available_balance` is not provided in the available context.

So, from the knowledge graph, the su…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_7`, `balances, interest accrual, fees, and account lifecycle status→ACCOUNTS`, `parent_chunk_data_dictionary.md_10`, `parent_chunk_data_dictionary.md_6`, `parent_chunk_data_dictionary.md_9`, `ACCOUNTS→ACCOUNTS`, `ACCOUNTS→BRANCHES`, `Loan portfolio table tracking all lending products including mortgages, personal loans, auto loans, HELOCs, and credit cards→LOANS`

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
> In the schema, `LOANS` links to `CUSTOMERS` through `LOANS.CUSTOMER_ID -> CUSTOMERS.CUSTOMER_ID` and to `ACCOUNTS` through `LOANS.ACCOUNT_ID -> ACCOUNTS.ACCOUNT_ID`.

From the `loans` table definition, `customer_id` is required (`NOT NULL`) and is described as the foreign key to the borrower in `customers`, so every loan must be associated with a customer. This matches the entity relationship summ…

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
> The system’s transaction activity is implemented in the TRANSACTIONS table and supports these transaction types through `transaction_type`: Debit, Credit, Transfer, Payment, Withdrawal, Deposit, and Fee.

From the business definition of Transaction, these are financial activities that affect an account balance. The context also states that debit transactions reduce the account balance and credit t…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_9`, `parent_chunk_data_dictionary.md_7`, `balances, interest accrual, fees, and account lifecycle status→ACCOUNTS`, `all account activity→TRANSACTIONS`, `parent_chunk_data_dictionary.md_6`, `parent_chunk_data_dictionary.md_11`, `Automated Teller Machine→ATMS`, `parent_chunk_data_dictionary.md_12`

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
> The schema supports joint account ownership through the `customer_account` table, which is a junction table between `customers` and `accounts`. This implements a many-to-many relationship, so one customer can be linked to multiple accounts and one account can be linked to multiple customers.

For joint ownership specifically, `customer_account.relationship_type` stores the role of each customer on…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_8`, `Owner/JointOwner/AuthorizedSigner/Custodian→CUSTOMER_ACCOUNT`, `parent_chunk_data_dictionary.md_12`, `parent_chunk_data_dictionary.md_7`, `parent_chunk_data_dictionary.md_11`, `CUSTOMER_ACCOUNT→CUSTOMERS`, `CUSTOMER_ACCOUNT→ACCOUNTS`, `parent_chunk_business_glossary.md_0`

**Context previews (first 3):**

1. _## customer_account  **Description: ** Junction table implementing many-to-many relationship between customers and accounts. Supports joint ownership, authorized signers, and custodial relationships. …_

2. _Business concept 'Owner/JointOwner/AuthorizedSigner/Custodian' is implemented by physical table CUSTOMER_ACCOUNT (columns: customer_id, account_id, relationship_type, is_primary, ownership_percentage,…_

3. _## Entity Relationship Summary  **Key Relationships: ** - customers ←→ accounts (many-to-many via customer_account) - accounts → accounts (self-reference for parent-child hierarchy) - accounts → trans…_

---

### ✅ 16 — What information does the cards table track and how are cards linked to customers and accounts?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.9528 | **Gate:** `proceed`

**Expected answer:**
> The cards table links to both accounts (account_id FK) and customers (customer_id FK), tracking card_type (Debit/Credit/ATM), card_network (Visa/Mastercard/Discover/AmericanExpress), card_number, cardholder name, expiration_date, and CVV. For spending controls it stores credit_limit (nullable, for c…

**System answer:**
> The `cards` table is the payment card issuance table. It tracks debit, credit, and ATM cards, including the cardholder and linked account, security features, limits, network, and lifecycle/status information.

From the context, `CARDS` includes these tracked attributes: `card_id` as the primary key; `account_id` as the linked account; `customer_id` as the cardholder; `card_number` as the PAN and i…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_11`, `CARDS→CUSTOMERS`, `CARDS→ACCOUNTS`, `parent_chunk_data_dictionary.md_10`, `CUSTOMER_ACCOUNT→CUSTOMERS`, `CUSTOMER_ACCOUNT→ACCOUNTS`, `parent_chunk_data_dictionary.md_8`, `parent_chunk_data_dictionary.md_12`

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
> The schema handles interest rates separately for deposit products and loan products, using different tables with a shared `interest_rate` field.

For deposit products, interest is stored in `ACCOUNTS`. The `accounts` table supports account types including Checking, Savings, MoneyMarket, CD, and Investment, and it explicitly includes `interest_rate` and `interest_earned`. Its description says it tr…

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
> The retrieved context says the bank operates three branch types in `BRANCHES.branch_type`: `FullService`, `Satellite`, and `ATMOnly`.

What is known from the context is limited to the fact that these are the defined branch type values. The `branches` table description says branches are “physical bank locations including full-service branches, satellite offices, and ATM-only locations,” and that th…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_12`, `physical banking location→BRANCHES`, `parent_chunk_data_dictionary.md_7`, `parent_chunk_data_dictionary.md_6`, `Customer Master Data→CUSTOMERS`, `ATMS→BRANCHES`, `parent_chunk_data_dictionary.md_5`, `parent_chunk_business_glossary.md_2`

**Context previews (first 3):**

1. _## Entity Relationship Summary  **Key Relationships: ** - customers ←→ accounts (many-to-many via customer_account) - accounts → accounts (self-reference for parent-child hierarchy) - accounts → trans…_

2. _Business concept 'physical banking location' is implemented by physical table BRANCHES (columns: branch_id, branch_code, branch_name, branch_type, address, city, state, zip_code, phone, hours, atm_cou…_

3. _## accounts  **Description: ** Deposit account master table supporting multiple account types (checking, savings, money market, CD, investment). Implements parent-child hierarchy for portfolio aggrega…_

---

### ✅ 19 — How are ATMs related to branches in the schema and what types of ATMs exist?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.6184 | **Gate:** `proceed`

**Expected answer:**
> The atms table has an optional branch_id foreign key referencing branches. When branch_id is NULL, the ATM is standalone and not affiliated with any branch. ATM types are defined by CHECK constraint: Branch (on-premises), DriveThrough (vehicle-accessible), and Standalone (independent locations). Eac…

**System answer:**
> In the schema, ATMs are stored in the ATMS table and branches are stored in the BRANCHES table. The relationship is ATMS.branch_id → BRANCHES.branch_id, so each ATM can reference a branch through the branch_id foreign key. The entity relationship summary describes this as branches → atms in a one-to-many relationship, meaning one branch can have multiple ATMs. The ATMS table also says branch_id is…

**Sources retrieved (12):** `ATMS→BRANCHES`, `parent_chunk_data_dictionary.md_6`, `parent_chunk_data_dictionary.md_12`, `Automated Teller Machine→ATMS`, `physical banking location→BRANCHES`, `parent_chunk_data_dictionary.md_9`, `parent_chunk_data_dictionary.md_11`, `parent_chunk_business_glossary.md_3`

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
> The retrieved context does not describe a full loan lifecycle from application through completion, so that cannot be determined here.

What is known from the context is that the `LOANS` table represents loans after they are part of the portfolio. It tracks lending products including mortgages, personal loans, auto loans, HELOCs, and credit cards, and stores `loan_id`, `customer_id`, `loan_type`, o…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_10`, `parent_chunk_data_dictionary.md_7`, `balances, interest accrual, fees, and account lifecycle status→ACCOUNTS`, `Loan portfolio table tracking all lending products including mortgages, personal loans, auto loans, HELOCs, and credit cards→LOANS`, `parent_chunk_data_dictionary.md_12`, `parent_chunk_business_glossary.md_2`, `parent_chunk_business_glossary.md_1`, `balances, interest accrual, fees, and account lifecycle status`

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
> Preferred customer status refers to a customer being flagged for VIP treatment. In the schema, it is tracked in the `CUSTOMERS` table, which is the core customer master data table for all individual and corporate banking customers. The specific column is `is_preferred`.

This comes directly from the `customers` table description, which states that it includes “preferred customer flags for VIP trea…

**Sources retrieved (12):** `Customer Master Data→CUSTOMERS`, `parent_chunk_data_dictionary.md_12`, `parent_chunk_data_dictionary.md_11`, `parent_chunk_data_dictionary.md_10`, `parent_chunk_data_dictionary.md_8`, `Loan portfolio table tracking all lending products including mortgages, personal loans, auto loans, HELOCs, and credit cards→LOANS`, `parent_chunk_data_dictionary.md_7`, `parent_chunk_data_dictionary.md_4`

**Context previews (first 3):**

1. _Business concept 'Customer Master Data' — The table description explicitly says it is the core customer dimension containing master data for all individual and corporate banking customers, which align…_

2. _## Entity Relationship Summary  **Key Relationships: ** - customers ←→ accounts (many-to-many via customer_account) - accounts → accounts (self-reference for parent-child hierarchy) - accounts → trans…_

3. _## cards  **Description: ** Payment card issuance table for debit, credit, and ATM cards. Links cards to both customer and account. Tracks security features (chip, contactless, PIN), spending limits, …_

---

### ✅ 22 — How does the accounts table support interest tracking and what business rules govern interest?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.3044 | **Gate:** `proceed`

**Expected answer:**
> The accounts table has interest_rate (nullable DECIMAL for the annual rate) and interest_earned (DECIMAL for year-to-date interest credited). The business glossary states that deposit interest is credited monthly (typically the first day of the month) and that APY accounts for compounding effects. P…

**System answer:**
> The `ACCOUNTS` table supports interest tracking directly through the columns `interest_rate` and `interest_earned`. From the table description, it is a deposit account master table for account types such as Checking, Savings, MoneyMarket, CD, and Investment, and it explicitly tracks balances, interest accrual, fees, and account lifecycle status. The mapped physical columns relevant to interest are…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_7`, `balances, interest accrual, fees, and account lifecycle status→ACCOUNTS`, `Loan portfolio table tracking all lending products including mortgages, personal loans, auto loans, HELOCs, and credit cards→LOANS`, `parent_chunk_data_dictionary.md_12`, `parent_chunk_data_dictionary.md_10`, `ACCOUNTS→BRANCHES`, `ACCOUNTS→ACCOUNTS`, `parent_chunk_data_dictionary.md_8`

**Context previews (first 3):**

1. _## accounts  **Description: ** Deposit account master table supporting multiple account types (checking, savings, money market, CD, investment). Implements parent-child hierarchy for portfolio aggrega…_

2. _Business concept 'balances, interest accrual, fees, and account lifecycle status' is implemented by physical table ACCOUNTS (columns: account_id, account_number, account_type, account_subtype, parent_…_

3. _Business concept 'Loan portfolio table tracking all lending products including mortgages, personal loans, auto loans, HELOCs, and credit cards' is implemented by physical table LOANS (columns: loan_id…_

---

### ✅ 23 — Can an account exist without any customer linked to it?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.1394 | **Gate:** `proceed_with_warning`

**Expected answer:**
> Looking at the schema, there is no database-level constraint that forces every account to have a customer_account row. The accounts table has no direct foreign key to customers — the relationship is through the customer_account junction table with a composite primary key (customer_id, account_id). H…

**System answer:**
> The retrieved context does not state a rule that every account must be linked to at least one customer.

What it does say is that customers and accounts have a many-to-many relationship through `customer_account`, and that the `customer_account` junction table “requires both customer and account to exist.” That means a link row cannot exist unless both the `CUSTOMERS` and `ACCOUNTS` records alread…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_8`, `CUSTOMER_ACCOUNT→CUSTOMERS`, `parent_chunk_data_dictionary.md_12`, `CUSTOMER_ACCOUNT→ACCOUNTS`, `Owner/JointOwner/AuthorizedSigner/Custodian→CUSTOMER_ACCOUNT`, `parent_chunk_data_dictionary.md_11`, `parent_chunk_data_dictionary.md_10`, `LOANS→CUSTOMERS`

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
> The schema handles failed or cancelled transactions through the `TRANSACTIONS` table, which implements the business concept of “all account activity.” That table includes a `status` column, and the `Transaction` business definition explicitly lists valid transaction states as `Pending`, `Posted`, `Failed`, `Cancelled`, and `OnHold`.

So, failed or cancelled transactions are not described as separa…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_9`, `parent_chunk_data_dictionary.md_12`, `parent_chunk_data_dictionary.md_7`, `TRANSACTIONS→ACCOUNTS`, `all account activity→TRANSACTIONS`, `parent_chunk_business_glossary.md_1`, `parent_chunk_business_glossary.md_0`, `parent_chunk_business_glossary.md_3`

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
> An ATM can have three status values in the context: Operational, OutOfService, and OutOfCash. The ATM business definition and the ATMS table both indicate that status is tracked for availability management.

The context also explicitly says the ATMS table tracks cash_balance and last_replenished for replenishment scheduling, and it records ATM type as Standalone, Branch, or DriveThrough. However, …

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_6`, `Automated Teller Machine→ATMS`, `ATMS→BRANCHES`, `parent_chunk_data_dictionary.md_12`, `parent_chunk_data_dictionary.md_11`, `physical banking location→BRANCHES`, `parent_chunk_data_dictionary.md_9`, `Card ID and Card Number (PAN)→CARDS`

**Context previews (first 3):**

1. _## atms  **Description: ** ATM locations including branch-attached machines, drive-through ATMs, and standalone units. Tracks cash balances for replenishment scheduling, GPS coordinates for location s…_

2. _Business concept 'Automated Teller Machine' is implemented by physical table ATMS (columns: atm_id, atm_code, branch_id, location, latitude, longitude, atm_type, status, cash_balance, last_replenished…_

3. _Relationship: ATMS references BRANCHES via foreign key BRANCH_ID -> BRANCHES.BRANCH_ID.…_

---

## Anomalies & Observations

No anomalies detected. All questions grounded with acceptable RAGAS scores.
