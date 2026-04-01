# AB-09 — 02_intermediate_finance — Run Analysis

**Timestamp:** 2026-03-31 21:31:32  
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
| Triplets extracted | 503 |
| Entities resolved | 223 |
| Tables parsed | 8 |
| Tables completed | 8 |

## Query Evaluation Summary

| Metric | Value |
|--------|-------|
| Questions | 25 |
| Grounded | **25/25 (100%)** |
| Avg GT Coverage | 100% |
| Avg Top Score | 0.4720 |
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
> A checking account is a type of deposit account. In the provided context, it appears as one of the `account_type` values in the `ACCOUNTS` table under the business concept “Deposit Account Types (Checking, Savings, Money Market, CD, Investment).”

More generally, the glossary defines an Account as “a financial arrangement between a customer and the bank that allows deposit, withdrawal, and managem…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_7`, `Deposit Account Types (Checking, Savings, Money Market, CD, Investment)→ACCOUNTS`, `parent_chunk_data_dictionary.md_8`, `parent_chunk_data_dictionary.md_9`, `parent_chunk_data_dictionary.md_10`, `parent_chunk_data_dictionary.md_12`, `parent_chunk_business_glossary.md_0`, `Deposit Account Types (Checking, Savings, Money Market, CD, Investment)`

**Context previews (first 3):**

1. _## accounts  **Description: ** Deposit account master table supporting multiple account types (checking, savings, money market, CD, investment). Implements parent-child hierarchy for portfolio aggrega…_

2. _Business concept 'Deposit Account Types (Checking, Savings, Money Market, CD, Investment)' is implemented by physical table ACCOUNTS (columns: account_id, account_number, account_type, account_subtype…_

3. _## customer_account  **Description: ** Junction table implementing many-to-many relationship between customers and accounts. Supports joint ownership, authorized signers, and custodial relationships. …_

---

### ✅ 2 — What is the difference between a savings account and a money market account?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.6601 | **Gate:** `proceed`

**Expected answer:**
> Both savings and money market are account types defined in the accounts table CHECK constraint. The business glossary Interest section provides example rates: Standard Savings earns 0.25% APY (with monthly compounding), Premium Savings earns 0.50% APY (with daily compounding), while Money Market ear…

**System answer:**
> The retrieved context does not define a business distinction between a savings account and a money market account.

From the context, both are simply listed as deposit account types: `Savings` and `MoneyMarket`, represented in the `ACCOUNTS.account_type` column under the business concept “Deposit Account Types (Checking, Savings, Money Market, CD, Investment).”

For either type, the `accounts` tab…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_7`, `Deposit Account Types (Checking, Savings, Money Market, CD, Investment)→ACCOUNTS`, `parent_chunk_data_dictionary.md_10`, `parent_chunk_data_dictionary.md_9`, `parent_chunk_data_dictionary.md_8`, `parent_chunk_data_dictionary.md_12`, `parent_chunk_data_dictionary.md_11`, `parent_chunk_business_glossary.md_0`

**Context previews (first 3):**

1. _## accounts  **Description: ** Deposit account master table supporting multiple account types (checking, savings, money market, CD, investment). Implements parent-child hierarchy for portfolio aggrega…_

2. _Business concept 'Deposit Account Types (Checking, Savings, Money Market, CD, Investment)' is implemented by physical table ACCOUNTS (columns: account_id, account_number, account_type, account_subtype…_

3. _## loans  **Description: ** Loan portfolio table tracking all lending products including mortgages, personal loans, auto loans, HELOCs, and credit cards. Records original terms, amortization schedules…_

---

### ✅ 3 — What is APR versus APY?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.9609 | **Gate:** `proceed`

**Expected answer:**
> APR (Annual Percentage Rate) is the annual cost of a loan including interest and fees, used for loan products. APY (Annual Percentage Yield) is the effective annual rate including compounding effects for deposit products. APY is higher than the nominal rate when compounding is more frequent than ann…

**System answer:**
> From the Interest concept, APR and APY are two different interest measures.

APR means Annual Percentage Rate and is used for loans.

APY means Annual Percentage Yield and is used for deposits.

The context also states that APY accounts for compounding effects. Interest in banking is expressed as an annual percentage rate, and compounding frequency can be daily, monthly, or annually. So, based on …

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_10`, `parent_chunk_business_glossary.md_2`, `parent_chunk_business_glossary.md_0`, `parent_chunk_business_glossary.md_1`, `parent_chunk_data_dictionary.md_7`, `parent_chunk_data_dictionary.md_11`, `parent_chunk_data_dictionary.md_8`, `Human-readable transaction description→TRANSACTIONS`

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
> The retrieved context does not define what “KYC Level 2” means. It only states that KYC is tracked in the `CUSTOMERS` table through the `kyc_status` column, and that valid KYC levels are `Level1`, `Level2`, or `Level3`. No business definition, criteria, or requirements for Level 2 are provided in the knowledge graph.

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_12`, `KYC (Know Your Customer) compliance status, risk profiling for investment suitability, and preferred customer flags for VIP treatment→CUSTOMERS`, `parent_chunk_data_dictionary.md_7`, `parent_chunk_data_dictionary.md_4`, `parent_chunk_business_glossary.md_0`, `KYC (Know Your Customer) compliance status, risk profiling for investment suitability, and preferred customer flags for VIP treatment`, `parent_chunk_business_glossary.md_1`, `parent_chunk_data_dictionary.md_5`

**Context previews (first 3):**

1. _## Entity Relationship Summary  **Key Relationships: ** - customers ←→ accounts (many-to-many via customer_account) - accounts → accounts (self-reference for parent-child hierarchy) - accounts → trans…_

2. _Business concept 'KYC (Know Your Customer) compliance status, risk profiling for investment suitability, and preferred customer flags for VIP treatment' is implemented by physical table CUSTOMERS (col…_

3. _## accounts  **Description: ** Deposit account master table supporting multiple account types (checking, savings, money market, CD, investment). Implements parent-child hierarchy for portfolio aggrega…_

---

### ✅ 5 — How does the schema support different account subtypes and their varying requirements?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.1891 | **Gate:** `proceed_with_warning`

**Expected answer:**
> The accounts table has an account_subtype column (VARCHAR 30, nullable) that stores values like Premium or Standard to differentiate within each account_type. Combined with the minimum_balance and monthly_fee columns, each account can have different requirements configured per subtype. The account_t…

**System answer:**
> The schema supports account subtypes primarily in the `accounts` table. It has both `account_type` and `account_subtype`:

`account_type` stores the main product category: Checking, Savings, MoneyMarket, CD, or Investment.

`account_subtype` stores a more specific subtype, and the context gives examples such as Premium, Student, and Standard. This column is nullable, so a subtype is optional.

The…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_7`, `parent_chunk_data_dictionary.md_12`, `Deposit Account Types (Checking, Savings, Money Market, CD, Investment)→ACCOUNTS`, `parent_chunk_data_dictionary.md_8`, `parent_chunk_data_dictionary.md_9`, `Loan portfolio table loan_type (Mortgage, Personal, Auto, HELOC, CreditCard)→CARDS`, `parent_chunk_data_dictionary.md_11`, `parent_chunk_business_glossary.md_0`

**Context previews (first 3):**

1. _## accounts  **Description: ** Deposit account master table supporting multiple account types (checking, savings, money market, CD, investment). Implements parent-child hierarchy for portfolio aggrega…_

2. _## Entity Relationship Summary  **Key Relationships: ** - customers ←→ accounts (many-to-many via customer_account) - accounts → accounts (self-reference for parent-child hierarchy) - accounts → trans…_

3. _Business concept 'Deposit Account Types (Checking, Savings, Money Market, CD, Investment)' is implemented by physical table ACCOUNTS (columns: account_id, account_number, account_type, account_subtype…_

---

### ✅ 6 — What types of loan products does the bank offer?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.4020 | **Gate:** `proceed`

**Expected answer:**
> The bank offers five loan types defined by the CHECK constraint on loans.loan_type: (1) Mortgage — secured by real estate, glossary example shows $350,000 at 5.50% APR for 360 months; (2) Personal Loan — unsecured, example $15,000 at 8.50% APR for 48 months; (3) Auto Loan — secured by vehicle, examp…

**System answer:**
> The bank’s loan products, as defined by the `loans` / `LOANS` schema, are Mortgage, Personal, Auto, HELOC, and CreditCard. The `loans` table description also refers to these as mortgages, personal loans, auto loans, HELOCs, and credit cards.

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_10`, `Loan portfolio table loan_type (Mortgage, Personal, Auto, HELOC, CreditCard)→CARDS`, `parent_chunk_data_dictionary.md_12`, `parent_chunk_data_dictionary.md_7`, `Loan amortization, balances, and maturity dates→LOANS`, `Deposit Account Types (Checking, Savings, Money Market, CD, Investment)→ACCOUNTS`, `parent_chunk_business_glossary.md_1`, `Loan portfolio table loan_type (Mortgage, Personal, Auto, HELOC, CreditCard)`

**Context previews (first 3):**

1. _## loans  **Description: ** Loan portfolio table tracking all lending products including mortgages, personal loans, auto loans, HELOCs, and credit cards. Records original terms, amortization schedules…_

2. _Business concept 'Loan portfolio table loan_type (Mortgage, Personal, Auto, HELOC, CreditCard)' is implemented by physical table CARDS (columns: card_id, account_id, customer_id, card_number, card_typ…_

3. _## Entity Relationship Summary  **Key Relationships: ** - customers ←→ accounts (many-to-many via customer_account) - accounts → accounts (self-reference for parent-child hierarchy) - accounts → trans…_

---

### ✅ 7 — What is the daily ATM withdrawal limit for standard customers?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.3743 | **Gate:** `proceed`

**Expected answer:**
> The cards table has an atm_daily_limit column with a default value of $500. The business glossary Card Examples confirm this: a standard Debit Card has a $500 ATM limit, while a Premium Debit card has a $2,000 ATM limit. The daily_limit column (default $3,000) controls POS spending separately. These…

**System answer:**
> The retrieved context does not provide a numeric daily ATM withdrawal limit for standard customers.

What it does show is that the `cards` table stores an `atm_daily_limit` column, and the `accounts` table includes `account_subtype` with examples such as `Premium`, `Student`, and `Standard`. A card is linked to both `customer_id` and `account_id`, and `accounts → cards` is a one-to-many relationsh…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_11`, `Loan portfolio table loan_type (Mortgage, Personal, Auto, HELOC, CreditCard)→CARDS`, `parent_chunk_data_dictionary.md_6`, `parent_chunk_data_dictionary.md_12`, `parent_chunk_data_dictionary.md_7`, `parent_chunk_data_dictionary.md_8`, `parent_chunk_business_glossary.md_3`, `parent_chunk_business_glossary.md_1`

**Context previews (first 3):**

1. _## cards  **Description: ** Payment card issuance table for debit, credit, and ATM cards. Links cards to both customer and account. Tracks security features (chip, contactless, PIN), spending limits, …_

2. _Business concept 'Loan portfolio table loan_type (Mortgage, Personal, Auto, HELOC, CreditCard)' is implemented by physical table CARDS (columns: card_id, account_id, customer_id, card_number, card_typ…_

3. _## atms  **Description: ** ATM locations including branch-attached machines, drive-through ATMs, and standalone units. Tracks cash balances for replenishment scheduling, GPS coordinates for location s…_

---

### ✅ 8 — What is the difference between a parent account and a child account?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.3098 | **Gate:** `proceed`

**Expected answer:**
> The accounts table supports parent-child hierarchies through the parent_account_id self-referencing foreign key, with a CHECK constraint preventing circular references (parent_account_id != account_id). The data dictionary describes this as supporting portfolio aggregation where parent accounts (typ…

**System answer:**
> In the `accounts` table, a parent account is an account that other accounts reference through `PARENT_ACCOUNT_ID`, while a child account is an account whose `parent_account_id` points to another row in `ACCOUNTS.ACCOUNT_ID`.

The hierarchy exists to support portfolio aggregation. The context specifically says investment accounts can contain child accounts, so a parent account functions as the high…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_7`, `parent_chunk_data_dictionary.md_12`, `ACCOUNTS→ACCOUNTS`, `Deposit Account Types (Checking, Savings, Money Market, CD, Investment)→ACCOUNTS`, `parent_chunk_data_dictionary.md_8`, `parent_chunk_data_dictionary.md_9`, `parent_chunk_data_dictionary.md_11`, `parent_chunk_data_dictionary.md_10`

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
> I cannot determine the meaning of card status 'Frozen' from the retrieved context.

The context shows that the `cards` table has a `status` column and that it tracks card status, but it does not provide definitions for card status values or explain what 'Frozen' means for a card. The only visible 'Frozen' status in the retrieved context appears under the Account business concept, not Card, so that…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_7`, `parent_chunk_data_dictionary.md_10`, `parent_chunk_data_dictionary.md_11`, `parent_chunk_data_dictionary.md_6`, `parent_chunk_data_dictionary.md_9`, `Loan portfolio table loan_type (Mortgage, Personal, Auto, HELOC, CreditCard)→CARDS`, `parent_chunk_business_glossary.md_0`, `parent_chunk_business_glossary.md_3`

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

First, each row is tied to a specific account through `account_id`, which is a foreign key to `ACCOUNTS.ACCOUNT_ID`, so the transaction’s effect is associated with one account.

Second, the table stores both the transaction amount and the resulting account balance:
`amount` is the transaction amount and is “always positive,…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_9`, `TRANSACTIONS→ACCOUNTS`, `parent_chunk_data_dictionary.md_7`, `Human-readable transaction description→TRANSACTIONS`, `ACCOUNTS→BRANCHES`, `ACCOUNTS→ACCOUNTS`, `parent_chunk_data_dictionary.md_10`, `CARDS→ACCOUNTS`

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
> The `customer_account` table supports multiple ownership types by acting as a many-to-many junction between `customers` and `accounts`, so one customer can be linked to multiple accounts and one account can be linked to multiple customers.

It represents different relationship roles through the `relationship_type` column, which is defined as `Owner`, `JointOwner`, `AuthorizedSigner`, or `Custodian…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_8`, `Customer Account Relationship→CUSTOMER_ACCOUNT`, `parent_chunk_data_dictionary.md_12`, `CUSTOMER_ACCOUNT→CUSTOMERS`, `parent_chunk_data_dictionary.md_7`, `CUSTOMER_ACCOUNT→ACCOUNTS`, `parent_chunk_data_dictionary.md_9`, `parent_chunk_data_dictionary.md_11`

**Context previews (first 3):**

1. _## customer_account  **Description: ** Junction table implementing many-to-many relationship between customers and accounts. Supports joint ownership, authorized signers, and custodial relationships. …_

2. _Business concept 'Customer Account Relationship' — The DDL explicitly labels this as a junction table implementing a many-to-many relationship between customers and accounts, with keys and attributes …_

3. _## Entity Relationship Summary  **Key Relationships: ** - customers ←→ accounts (many-to-many via customer_account) - accounts → accounts (self-reference for parent-child hierarchy) - accounts → trans…_

---

### ✅ 12 — What is the difference between current_balance and available_balance in the accounts table?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.8328 | **Gate:** `proceed`

**Expected answer:**
> The accounts table tracks two separate balance fields: current_balance includes all transactions including pending ones, while available_balance excludes holds and pending transactions and represents what the customer can actually withdraw. The business glossary confirms this distinction, stating th…

**System answer:**
> The `ACCOUNTS` table contains both `current_balance` and `available_balance` as separate columns, and the business glossary explicitly treats “Current Balance vs. Available Balance” as a key account attribute.

However, the retrieved context does not provide an explicit definition of how `current_balance` differs from `available_balance`, nor does it give the exact calculation rule for each field.…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_7`, `Deposit Account Types (Checking, Savings, Money Market, CD, Investment)→ACCOUNTS`, `parent_chunk_data_dictionary.md_10`, `parent_chunk_data_dictionary.md_6`, `parent_chunk_data_dictionary.md_9`, `ACCOUNTS→ACCOUNTS`, `ACCOUNTS→BRANCHES`, `Loan amortization, balances, and maturity dates→LOANS`

**Context previews (first 3):**

1. _## accounts  **Description: ** Deposit account master table supporting multiple account types (checking, savings, money market, CD, investment). Implements parent-child hierarchy for portfolio aggrega…_

2. _Business concept 'Deposit Account Types (Checking, Savings, Money Market, CD, Investment)' is implemented by physical table ACCOUNTS (columns: account_id, account_number, account_type, account_subtype…_

3. _## loans  **Description: ** Loan portfolio table tracking all lending products including mortgages, personal loans, auto loans, HELOCs, and credit cards. Records original terms, amortization schedules…_

---

### ✅ 13 — How are loans linked to both customers and accounts in the schema?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.8105 | **Gate:** `proceed`

**Expected answer:**
> The loans table has a customer_id foreign key referencing the customers table (the borrower) and an optional account_id foreign key referencing the accounts table (for linked payment accounts). Each loan belongs to exactly one customer, and can optionally be connected to an account for automatic pay…

**System answer:**
> Loans are linked directly through the `LOANS` table using two foreign keys.

`LOANS.CUSTOMER_ID` references `CUSTOMERS.CUSTOMER_ID`, which makes the borrower relationship mandatory because `customer_id` in `LOANS` is defined as `NOT NULL`. The relationship metadata explicitly states: `LOANS` references `CUSTOMERS` via `CUSTOMER_ID -> CUSTOMERS.CUSTOMER_ID`. The entity summary also describes this a…

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
> The system supports these transaction types in `TRANSACTIONS` / the `Transaction` business concept: Debit, Credit, Transfer, Payment, Withdrawal, Deposit, and Fee.

From the business definition, a transaction is any financial activity that affects an account balance. The context also gives these behavioral rules: debit transactions reduce account balance, credit transactions increase account balan…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_9`, `parent_chunk_data_dictionary.md_7`, `Human-readable transaction description→TRANSACTIONS`, `parent_chunk_data_dictionary.md_6`, `Deposit Account Types (Checking, Savings, Money Market, CD, Investment)→ACCOUNTS`, `parent_chunk_data_dictionary.md_11`, `Automated Teller Machine→ATMS`, `parent_chunk_data_dictionary.md_12`

**Context previews (first 3):**

1. _## transactions  **Description: ** Transaction fact table recording all account activity. Supports multiple transaction types including debits, credits, transfers, and withdrawals. Tracks calculated f…_

2. _## accounts  **Description: ** Deposit account master table supporting multiple account types (checking, savings, money market, CD, investment). Implements parent-child hierarchy for portfolio aggrega…_

3. _Business concept 'Human-readable transaction description' is implemented by physical table TRANSACTIONS (columns: transaction_id, account_id, transaction_type, amount, currency, transaction_date, stat…_

---

### ✅ 15 — How does the schema support joint account ownership between multiple customers?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.4870 | **Gate:** `proceed`

**Expected answer:**
> Joint ownership is implemented through the customer_account junction table, which creates a many-to-many relationship between customers and accounts. Each row has a relationship_type CHECK constraint allowing Owner, JointOwner, AuthorizedSigner, or Custodian. The ownership_percentage field (DECIMAL …

**System answer:**
> The schema supports joint account ownership through the `customer_account` table, which is explicitly defined as a junction table for the many-to-many relationship between `customers` and `accounts`. This means one customer can be linked to multiple accounts, and one account can be linked to multiple customers.

In `customer_account`, each row connects a `customer_id` to an `account_id`. The compo…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_8`, `parent_chunk_data_dictionary.md_12`, `Customer Account Relationship→CUSTOMER_ACCOUNT`, `parent_chunk_data_dictionary.md_7`, `parent_chunk_data_dictionary.md_11`, `CUSTOMER_ACCOUNT→CUSTOMERS`, `CUSTOMER_ACCOUNT→ACCOUNTS`, `Customer Account Relationship`

**Context previews (first 3):**

1. _## customer_account  **Description: ** Junction table implementing many-to-many relationship between customers and accounts. Supports joint ownership, authorized signers, and custodial relationships. …_

2. _## Entity Relationship Summary  **Key Relationships: ** - customers ←→ accounts (many-to-many via customer_account) - accounts → accounts (self-reference for parent-child hierarchy) - accounts → trans…_

3. _Business concept 'Customer Account Relationship' — The DDL explicitly labels this as a junction table implementing a many-to-many relationship between customers and accounts, with keys and attributes …_

---

### ✅ 16 — What information does the cards table track and how are cards linked to customers and accounts?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.9528 | **Gate:** `proceed`

**Expected answer:**
> The cards table links to both accounts (account_id FK) and customers (customer_id FK), tracking card_type (Debit/Credit/ATM), card_network (Visa/Mastercard/Discover/AmericanExpress), card_number, cardholder name, expiration_date, and CVV. For spending controls it stores credit_limit (nullable, for c…

**System answer:**
> The `cards` table is the payment card issuance table. It tracks cards for debit, credit, and ATM products, and stores information about the card itself, its security features, usage limits, and lifecycle status.

From the context, it tracks:
`card_id` as the primary key; `account_id` for the linked account; `customer_id` for the cardholder; `card_number` as the unique PAN; `card_type` (Debit/Credi…

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
> The schema handles interest differently for deposit products and loan products, using separate tables aligned to the business meaning of interest.

For deposit products, the physical table is ACCOUNTS. The business concept “Deposit Account Types (Checking, Savings, Money Market, CD, Investment)” maps to ACCOUNTS, which includes the columns interest_rate and interest_earned, along with balances suc…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_12`, `parent_chunk_data_dictionary.md_10`, `parent_chunk_data_dictionary.md_7`, `Loan amortization, balances, and maturity dates→LOANS`, `Deposit Account Types (Checking, Savings, Money Market, CD, Investment)→ACCOUNTS`, `LOANS→CUSTOMERS`, `LOANS→ACCOUNTS`, `Loan portfolio table loan_type (Mortgage, Personal, Auto, HELOC, CreditCard)→CARDS`

**Context previews (first 3):**

1. _## Entity Relationship Summary  **Key Relationships: ** - customers ←→ accounts (many-to-many via customer_account) - accounts → accounts (self-reference for parent-child hierarchy) - accounts → trans…_

2. _## loans  **Description: ** Loan portfolio table tracking all lending products including mortgages, personal loans, auto loans, HELOCs, and credit cards. Records original terms, amortization schedules…_

3. _## accounts  **Description: ** Deposit account master table supporting multiple account types (checking, savings, money market, CD, investment). Implements parent-child hierarchy for portfolio aggrega…_

---

### ✅ 18 — What types of branches does the bank operate and how do they differ in capabilities?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.1556 | **Gate:** `proceed_with_warning`

**Expected answer:**
> The branches table supports three types via CHECK constraint: FullService, Satellite, and ATMOnly. The business glossary details each: FullService branches offer complete banking services including loan origination, financial advisors, and safe deposit boxes; Satellite branches have limited hours an…

**System answer:**
> The bank operates three branch types, stored in `BRANCHES.branch_type`: `FullService`, `Satellite`, and `ATMOnly`.

From the `branches` definition, these are all physical bank locations, described as full-service branches, satellite offices, and ATM-only locations. Their operational differences are represented in the `BRANCHES` table through fields such as `teller_count`, `atm_count`, `hours`, `ma…

**Sources retrieved (12):** `Banking Center→BRANCHES`, `parent_chunk_data_dictionary.md_12`, `parent_chunk_data_dictionary.md_7`, `Deposit Account Types (Checking, Savings, Money Market, CD, Investment)→ACCOUNTS`, `parent_chunk_data_dictionary.md_6`, `ATMS→BRANCHES`, `ACCOUNTS→BRANCHES`, `parent_chunk_data_dictionary.md_5`

**Context previews (first 3):**

1. _Business concept 'Banking Center' is implemented by physical table BRANCHES (columns: branch_id, branch_code, branch_name, branch_type, address, city, state, zip_code, phone, hours, atm_count, teller_…_

2. _## Entity Relationship Summary  **Key Relationships: ** - customers ←→ accounts (many-to-many via customer_account) - accounts → accounts (self-reference for parent-child hierarchy) - accounts → trans…_

3. _## accounts  **Description: ** Deposit account master table supporting multiple account types (checking, savings, money market, CD, investment). Implements parent-child hierarchy for portfolio aggrega…_

---

### ✅ 19 — How are ATMs related to branches in the schema and what types of ATMs exist?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.6184 | **Gate:** `proceed`

**Expected answer:**
> The atms table has an optional branch_id foreign key referencing branches. When branch_id is NULL, the ATM is standalone and not affiliated with any branch. ATM types are defined by CHECK constraint: Branch (on-premises), DriveThrough (vehicle-accessible), and Standalone (independent locations). Eac…

**System answer:**
> ATMs are related to branches through `ATMS.branch_id` → `BRANCHES.branch_id`. The schema explicitly states that `ATMS` references `BRANCHES` via this foreign key, and the entity relationship summary describes this as a one-to-many relationship from `branches` to `atms`, meaning one branch can have many ATMs.

The `branch_id` column in `ATMS` is nullable, which is important to the business rule: st…

**Sources retrieved (12):** `ATMS→BRANCHES`, `parent_chunk_data_dictionary.md_6`, `parent_chunk_data_dictionary.md_12`, `Automated Teller Machine→ATMS`, `Banking Center→BRANCHES`, `parent_chunk_data_dictionary.md_9`, `parent_chunk_data_dictionary.md_11`, `parent_chunk_business_glossary.md_3`

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
> The retrieved context does not define a loan lifecycle from application to completion. It contains schema-level metadata about the `LOANS` table and related business concepts, but it does not describe application, approval, funding, payoff, closure, charge-off, or any explicit “completion” process.

What the context does say is that `LOANS` is the loan portfolio table for lending products includin…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_10`, `parent_chunk_data_dictionary.md_7`, `Loan amortization, balances, and maturity dates→LOANS`, `parent_chunk_data_dictionary.md_12`, `Loan portfolio table loan_type (Mortgage, Personal, Auto, HELOC, CreditCard)→CARDS`, `parent_chunk_business_glossary.md_2`, `parent_chunk_business_glossary.md_1`, `Loan amortization, balances, and maturity dates`

**Context previews (first 3):**

1. _## loans  **Description: ** Loan portfolio table tracking all lending products including mortgages, personal loans, auto loans, HELOCs, and credit cards. Records original terms, amortization schedules…_

2. _## accounts  **Description: ** Deposit account master table supporting multiple account types (checking, savings, money market, CD, investment). Implements parent-child hierarchy for portfolio aggrega…_

3. _Business concept 'Loan amortization, balances, and maturity dates' is implemented by physical table LOANS (columns: loan_id, customer_id, loan_type, account_id, principal_amount, interest_rate, term_m…_

---

### ✅ 21 — What does preferred customer status mean and how is it tracked in the schema?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.5129 | **Gate:** `proceed`

**Expected answer:**
> Preferred status is tracked via the is_preferred boolean flag in the customers table (default: false). The business glossary states that preferred customers receive waived fees, preferred interest rates, and priority service. The glossary examples show preferred customers with longer tenure and high…

**System answer:**
> Preferred customer status means a customer is marked for VIP treatment. In the schema, this business concept is part of the customers domain alongside KYC compliance status and investment risk profiling.

It is tracked in the CUSTOMERS table, specifically through the is_preferred column. The concept-to-table mapping explicitly says that “KYC compliance status, risk profiling for investment suitabi…

**Sources retrieved (12):** `KYC (Know Your Customer) compliance status, risk profiling for investment suitability, and preferred customer flags for VIP treatment→CUSTOMERS`, `parent_chunk_data_dictionary.md_12`, `parent_chunk_data_dictionary.md_11`, `parent_chunk_data_dictionary.md_10`, `parent_chunk_data_dictionary.md_8`, `parent_chunk_data_dictionary.md_7`, `CARDS→CUSTOMERS`, `parent_chunk_data_dictionary.md_4`

**Context previews (first 3):**

1. _Business concept 'KYC (Know Your Customer) compliance status, risk profiling for investment suitability, and preferred customer flags for VIP treatment' is implemented by physical table CUSTOMERS (col…_

2. _## Entity Relationship Summary  **Key Relationships: ** - customers ←→ accounts (many-to-many via customer_account) - accounts → accounts (self-reference for parent-child hierarchy) - accounts → trans…_

3. _## cards  **Description: ** Payment card issuance table for debit, credit, and ATM cards. Links cards to both customer and account. Tracks security features (chip, contactless, PIN), spending limits, …_

---

### ✅ 22 — How does the accounts table support interest tracking and what business rules govern interest?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.3044 | **Gate:** `proceed`

**Expected answer:**
> The accounts table has interest_rate (nullable DECIMAL for the annual rate) and interest_earned (DECIMAL for year-to-date interest credited). The business glossary states that deposit interest is credited monthly (typically the first day of the month) and that APY accounts for compounding effects. P…

**System answer:**
> The `ACCOUNTS` table supports interest tracking through the columns `interest_rate` and `interest_earned`, and its description explicitly says it tracks interest accrual. The business concept mapping for deposit account types confirms that `ACCOUNTS` includes `interest_rate`, `interest_earned`, `current_balance`, `available_balance`, `minimum_balance`, `monthly_fee`, and lifecycle dates/status fie…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_7`, `parent_chunk_data_dictionary.md_12`, `Deposit Account Types (Checking, Savings, Money Market, CD, Investment)→ACCOUNTS`, `parent_chunk_data_dictionary.md_10`, `ACCOUNTS→BRANCHES`, `ACCOUNTS→ACCOUNTS`, `parent_chunk_data_dictionary.md_8`, `Loan amortization, balances, and maturity dates→LOANS`

**Context previews (first 3):**

1. _## accounts  **Description: ** Deposit account master table supporting multiple account types (checking, savings, money market, CD, investment). Implements parent-child hierarchy for portfolio aggrega…_

2. _## Entity Relationship Summary  **Key Relationships: ** - customers ←→ accounts (many-to-many via customer_account) - accounts → accounts (self-reference for parent-child hierarchy) - accounts → trans…_

3. _Business concept 'Deposit Account Types (Checking, Savings, Money Market, CD, Investment)' is implemented by physical table ACCOUNTS (columns: account_id, account_number, account_type, account_subtype…_

---

### ✅ 23 — Can an account exist without any customer linked to it?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.1394 | **Gate:** `proceed_with_warning`

**Expected answer:**
> Looking at the schema, there is no database-level constraint that forces every account to have a customer_account row. The accounts table has no direct foreign key to customers — the relationship is through the customer_account junction table with a composite primary key (customer_id, account_id). H…

**System answer:**
> The retrieved context does not explicitly say whether every account must have at least one linked customer.

What the context does say is that `CUSTOMER_ACCOUNT` is a junction table implementing a many-to-many relationship between `customers` and `accounts`, and that any row in `CUSTOMER_ACCOUNT` requires both a valid `customer_id` and a valid `account_id` to exist. It also says customers and acco…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_8`, `CUSTOMER_ACCOUNT→CUSTOMERS`, `parent_chunk_data_dictionary.md_12`, `CUSTOMER_ACCOUNT→ACCOUNTS`, `Customer Account Relationship→CUSTOMER_ACCOUNT`, `parent_chunk_data_dictionary.md_11`, `parent_chunk_data_dictionary.md_10`, `parent_chunk_business_glossary.md_3`

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
> The schema handles failed or cancelled transactions through the `TRANSACTIONS` table’s `status` attribute. The business concept `Transaction` defines the allowed transaction states as `Pending`, `Posted`, `Failed`, `Cancelled`, and `OnHold`, and the concept notes that transactions flow through multiple states, specifically “Pending → Posted,” while also creating audit trails for regulatory complia…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_9`, `parent_chunk_data_dictionary.md_12`, `parent_chunk_data_dictionary.md_7`, `TRANSACTIONS→ACCOUNTS`, `Human-readable transaction description→TRANSACTIONS`, `parent_chunk_business_glossary.md_1`, `parent_chunk_business_glossary.md_0`, `parent_chunk_business_glossary.md_3`

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
> The retrieved context lists three ATM status values for the `ATMS.status` attribute: `Operational`, `OutOfService`, and `OutOfCash`. It also says ATM records include supported features such as deposit and cardless withdrawal (`supports_deposit`, `supports_cardless`).

However, the context does not define what each status specifically means for service availability. It does not state, for example, …

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_6`, `Automated Teller Machine→ATMS`, `ATMS→BRANCHES`, `parent_chunk_data_dictionary.md_12`, `parent_chunk_data_dictionary.md_11`, `Banking Center→BRANCHES`, `parent_chunk_data_dictionary.md_9`, `parent_chunk_business_glossary.md_3`

**Context previews (first 3):**

1. _## atms  **Description: ** ATM locations including branch-attached machines, drive-through ATMs, and standalone units. Tracks cash balances for replenishment scheduling, GPS coordinates for location s…_

2. _Business concept 'Automated Teller Machine' is implemented by physical table ATMS (columns: atm_id, atm_code, branch_id, location, latitude, longitude, atm_type, status, cash_balance, last_replenished…_

3. _Relationship: ATMS references BRANCHES via foreign key BRANCH_ID -> BRANCHES.BRANCH_ID.…_

---

## Anomalies & Observations

No anomalies detected. All questions grounded with acceptable RAGAS scores.
