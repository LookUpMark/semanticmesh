# AB-07 — 02_intermediate_finance — Run Analysis

**Timestamp:** 2026-03-31 07:31:00  
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
| Chunk size / overlap | `384 / 48` |
| ER similarity threshold | `0.75` |

## Builder Results

| Metric | Value |
|--------|-------|
| Triplets extracted | 597 |
| Entities resolved | 235 |
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
> From the retrieved context, a checking account is not separately defined as its own business concept. What the context does say is that `accounts` / the business concept “Account” is “a financial arrangement between a customer and the bank that allows deposit, withdrawal, and management of funds,” and one of the allowed `account_type` values is `Checking` in the `ACCOUNTS` table.

So, based on the…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_7`, `parent_chunk_data_dictionary.md_8`, `parent_chunk_data_dictionary.md_9`, `Deposit Account→ACCOUNTS`, `parent_chunk_data_dictionary.md_10`, `parent_chunk_business_glossary.md_0`, `parent_chunk_business_glossary.md_1`, `Deposit Account`

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
> From the retrieved context, both savings accounts and money market accounts are treated as deposit account types within the same `ACCOUNTS` table. The `account_type` column explicitly allows both `Savings` and `MoneyMarket`, and the business glossary lists both as valid account types under the broader `Account` concept.

What the context does support is this: both would share the same deposit-acco…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_7`, `parent_chunk_data_dictionary.md_10`, `Deposit Account→ACCOUNTS`, `parent_chunk_data_dictionary.md_8`, `parent_chunk_data_dictionary.md_12`, `parent_chunk_data_dictionary.md_11`, `parent_chunk_business_glossary.md_0`, `parent_chunk_business_glossary.md_2`

**Context previews (first 3):**

1. _## accounts  **Description: ** Deposit account master table supporting multiple account types (checking, savings, money market, CD, investment). Implements parent-child hierarchy for portfolio aggrega…_

2. _## loans  **Description: ** Loan portfolio table tracking all lending products including mortgages, personal loans, auto loans, HELOCs, and credit cards. Records original terms, amortization schedules…_

3. _Business concept 'Deposit Account' — The table is explicitly described as deposit accounts and contains core account master data such as account number, type, subtype, balances, interest rate, fees, s…_

---

### ✅ 3 — What is APR versus APY?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.9609 | **Gate:** `proceed`

**Expected answer:**
> APR (Annual Percentage Rate) is the annual cost of a loan including interest and fees, used for loan products. APY (Annual Percentage Yield) is the effective annual rate including compounding effects for deposit products. APY is higher than the nominal rate when compounding is more frequent than ann…

**System answer:**
> In the context of Interest, APR is the Annual Percentage Rate and is used for loans, while APY is the Annual Percentage Yield and is used for deposits.

The context also states that APY accounts for compounding. So the distinction given is:
APR: loan-related annual percentage rate.
APY: deposit-related annual percentage yield that reflects compounding.

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
> The retrieved context only states that valid KYC levels are `Level1`, `Level2`, and `Level3` under the enforced business rules. It does not provide a definition or meaning specific to `Level2`.

The related customer concept is implemented by the `CUSTOMERS` table, which includes a `kyc_status` column, but the context does not describe what each KYC level represents.

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_12`, `an individual or corporate entity that maintains a banking relationship with the institution, having completed Know Your Customer (KYC) verification→CUSTOMERS`, `parent_chunk_data_dictionary.md_7`, `parent_chunk_data_dictionary.md_4`, `parent_chunk_business_glossary.md_0`, `an individual or corporate entity that maintains a banking relationship with the institution, having completed Know Your Customer (KYC) verification`, `parent_chunk_business_glossary.md_1`, `parent_chunk_data_dictionary.md_5`

**Context previews (first 3):**

1. _## Entity Relationship Summary  **Key Relationships: ** - customers ←→ accounts (many-to-many via customer_account) - accounts → accounts (self-reference for parent-child hierarchy) - accounts → trans…_

2. _Business concept 'an individual or corporate entity that maintains a banking relationship with the institution, having completed Know Your Customer (KYC) verification' — An individual or corporate ent…_

3. _## accounts  **Description: ** Deposit account master table supporting multiple account types (checking, savings, money market, CD, investment). Implements parent-child hierarchy for portfolio aggrega…_

---

### ✅ 5 — How does the schema support different account subtypes and their varying requirements?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.1891 | **Gate:** `proceed_with_warning`

**Expected answer:**
> The accounts table has an account_subtype column (VARCHAR 30, nullable) that stores values like Premium or Standard to differentiate within each account_type. Combined with the minimum_balance and monthly_fee columns, each account can have different requirements configured per subtype. The account_t…

**System answer:**
> The schema supports account subtypes primarily through the `ACCOUNTS` table, which stores both `account_type` and `account_subtype` on each account record rather than using separate tables for each product variant.

From the context, `account_type` identifies the major product category: Checking, Savings, MoneyMarket, CD, or Investment. `account_subtype` provides a finer-grained variant within tho…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_7`, `parent_chunk_data_dictionary.md_12`, `Deposit Account→ACCOUNTS`, `parent_chunk_data_dictionary.md_8`, `Loan Type (Mortgage, Personal, Auto, HELOC, CreditCard)→LOANS`, `parent_chunk_data_dictionary.md_9`, `parent_chunk_data_dictionary.md_11`, `Deposit Account`

**Context previews (first 3):**

1. _## accounts  **Description: ** Deposit account master table supporting multiple account types (checking, savings, money market, CD, investment). Implements parent-child hierarchy for portfolio aggrega…_

2. _## Entity Relationship Summary  **Key Relationships: ** - customers ←→ accounts (many-to-many via customer_account) - accounts → accounts (self-reference for parent-child hierarchy) - accounts → trans…_

3. _Business concept 'Deposit Account' — The table is explicitly described as deposit accounts and contains core account master data such as account number, type, subtype, balances, interest rate, fees, s…_

---

### ✅ 6 — What types of loan products does the bank offer?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.4020 | **Gate:** `proceed`

**Expected answer:**
> The bank offers five loan types defined by the CHECK constraint on loans.loan_type: (1) Mortgage — secured by real estate, glossary example shows $350,000 at 5.50% APR for 360 months; (2) Personal Loan — unsecured, example $15,000 at 8.50% APR for 48 months; (3) Auto Loan — secured by vehicle, examp…

**System answer:**
> The bank offers these loan product types, as defined by the `LOANS.loan_type` field and the “Loan Type” business concept: Mortgage, Personal, Auto, HELOC, and CreditCard. The `loans` table description also says it tracks all lending products including mortgages, personal loans, auto loans, HELOCs, and credit cards.

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_10`, `Loan Type (Mortgage, Personal, Auto, HELOC, CreditCard)→LOANS`, `parent_chunk_data_dictionary.md_12`, `parent_chunk_data_dictionary.md_7`, `LOANS→CUSTOMERS`, `Loan Type (Mortgage, Personal, Auto, HELOC, CreditCard)`, `parent_chunk_business_glossary.md_1`, `parent_chunk_business_glossary.md_2`

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
> The retrieved context does not provide a numeric daily ATM withdrawal limit for standard customers.

What it does provide is the schema location of that information. The CARDS table includes an `atm_daily_limit` column, and the table description says it tracks spending limits and security features for issued cards. CARDS is linked to both `accounts` and `customers` through `account_id` and `custom…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_11`, `Payment card issuance table for debit, credit, and ATM cards→CARDS`, `parent_chunk_data_dictionary.md_6`, `parent_chunk_data_dictionary.md_9`, `parent_chunk_data_dictionary.md_12`, `parent_chunk_data_dictionary.md_7`, `Automated Teller Machine→ATMS`, `parent_chunk_business_glossary.md_3`

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
> A parent account is an account in `ACCOUNTS` that serves as the higher-level account in the table’s self-referencing hierarchy, used for portfolio aggregation. The context says this hierarchy is implemented through `ACCOUNTS.PARENT_ACCOUNT_ID -> ACCOUNTS.ACCOUNT_ID`, and specifically notes that investment accounts can contain child accounts.

A child account is an `ACCOUNTS` row whose `parent_acco…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_7`, `parent_chunk_data_dictionary.md_12`, `Deposit Account→ACCOUNTS`, `ACCOUNTS→ACCOUNTS`, `parent_chunk_data_dictionary.md_8`, `parent_chunk_data_dictionary.md_9`, `parent_chunk_data_dictionary.md_11`, `parent_chunk_data_dictionary.md_10`

**Context previews (first 3):**

1. _## accounts  **Description: ** Deposit account master table supporting multiple account types (checking, savings, money market, CD, investment). Implements parent-child hierarchy for portfolio aggrega…_

2. _## Entity Relationship Summary  **Key Relationships: ** - customers ←→ accounts (many-to-many via customer_account) - accounts → accounts (self-reference for parent-child hierarchy) - accounts → trans…_

3. _Business concept 'Deposit Account' — The table is explicitly described as deposit accounts and contains core account master data such as account number, type, subtype, balances, interest rate, fees, s…_

---

### ✅ 9 — What does the status 'Frozen' mean for a card?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0630 | **Gate:** `proceed_with_warning`

**Expected answer:**
> The cards table has a status column with four states defined by CHECK constraint: Active, Frozen, Blocked, and Expired. The business glossary states that lost or stolen cards must be immediately blocked to prevent fraud, and that expired cards are automatically renewed. The glossary distinguishes Fr…

**System answer:**
> The retrieved context does not define what `Frozen` means for a card.

What it does show is that the `cards` table (`CARDS`) has a `status` column and that cards track “card status,” but no card status values or definitions are provided. The term `Frozen` appears only in the business glossary for the `Account` concept, where account statuses are listed as `Active, Dormant, Frozen, Closed`.

So, ba…

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
> The `TRANSACTIONS` table tracks balance impact in two complementary ways.

First, each row is tied to a specific deposit account through `account_id`, which is a foreign key to `ACCOUNTS.ACCOUNT_ID`. That means the effect of a transaction is recorded against a particular account.

Second, it stores a calculated field, `balance_after`, described in the table/business concept as the balance after th…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_9`, `TRANSACTIONS→ACCOUNTS`, `parent_chunk_data_dictionary.md_7`, `Human-readable transaction description→TRANSACTIONS`, `ACCOUNTS→BRANCHES`, `Deposit Account→ACCOUNTS`, `ACCOUNTS→ACCOUNTS`, `parent_chunk_data_dictionary.md_10`

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
> The `customer_account` table supports multiple ownership types by storing the relationship between a customer and an account as its own record, rather than embedding ownership directly in either entity. It is explicitly a many-to-many junction table between customers and accounts, so a single account can be linked to multiple customers and a single customer can be linked to multiple accounts.

It …

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_8`, `Customer Account Relationship→CUSTOMER_ACCOUNT`, `Customer Account Relationship`, `parent_chunk_data_dictionary.md_12`, `CUSTOMER_ACCOUNT→CUSTOMERS`, `parent_chunk_data_dictionary.md_7`, `CUSTOMER_ACCOUNT→ACCOUNTS`, `parent_chunk_data_dictionary.md_9`

**Context previews (first 3):**

1. _## customer_account  **Description: ** Junction table implementing many-to-many relationship between customers and accounts. Supports joint ownership, authorized signers, and custodial relationships. …_

2. _Business concept 'Customer Account Relationship' — The table is explicitly described as a junction table implementing a many-to-many relationship between customers and accounts, with foreign keys to b…_

3. _Customer Account Relationship: The table is explicitly described as a junction table implementing a many-to-many relationship between customers and accounts, with foreign keys to both customers and ac…_

---

### ✅ 12 — What is the difference between current_balance and available_balance in the accounts table?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.8328 | **Gate:** `proceed`

**Expected answer:**
> The accounts table tracks two separate balance fields: current_balance includes all transactions including pending ones, while available_balance excludes holds and pending transactions and represents what the customer can actually withdraw. The business glossary confirms this distinction, stating th…

**System answer:**
> The retrieved context shows that the ACCOUNTS table tracks both `current_balance` and `available_balance`, and the business glossary explicitly treats “Current Balance vs. Available Balance” as an important account attribute.

However, the retrieved context does not provide an explicit definition of the difference between those two columns. It confirms they are distinct balance fields in the `ACCO…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_7`, `Deposit Account→ACCOUNTS`, `parent_chunk_data_dictionary.md_10`, `parent_chunk_data_dictionary.md_6`, `parent_chunk_data_dictionary.md_9`, `ACCOUNTS→ACCOUNTS`, `ACCOUNTS→BRANCHES`, `parent_chunk_business_glossary.md_0`

**Context previews (first 3):**

1. _## accounts  **Description: ** Deposit account master table supporting multiple account types (checking, savings, money market, CD, investment). Implements parent-child hierarchy for portfolio aggrega…_

2. _Business concept 'Deposit Account' — The table is explicitly described as deposit accounts and contains core account master data such as account number, type, subtype, balances, interest rate, fees, s…_

3. _## loans  **Description: ** Loan portfolio table tracking all lending products including mortgages, personal loans, auto loans, HELOCs, and credit cards. Records original terms, amortization schedules…_

---

### ✅ 13 — How are loans linked to both customers and accounts in the schema?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.8105 | **Gate:** `proceed`

**Expected answer:**
> The loans table has a customer_id foreign key referencing the customers table (the borrower) and an optional account_id foreign key referencing the accounts table (for linked payment accounts). Each loan belongs to exactly one customer, and can optionally be connected to an account for automatic pay…

**System answer:**
> In the schema, `LOANS` links directly to both `CUSTOMERS` and `ACCOUNTS` through foreign keys in the `loans` table.

`LOANS.CUSTOMER_ID` is a required foreign key to `CUSTOMERS.CUSTOMER_ID`, so every loan must be associated with a customer borrower. The relationship is described as `customers → loans` one-to-many, meaning one customer can have multiple loans.

`LOANS.ACCOUNT_ID` is an optional for…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_12`, `LOANS→CUSTOMERS`, `LOANS→ACCOUNTS`, `Customer Account Relationship`, `Customer Account Relationship→CUSTOMER_ACCOUNT`, `parent_chunk_data_dictionary.md_10`, `CUSTOMER_ACCOUNT→CUSTOMERS`, `parent_chunk_data_dictionary.md_8`

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
> The system supports these transaction types in `TRANSACTIONS`: Debit, Credit, Transfer, Payment, Withdrawal, Deposit, and Fee.

From the business definition of `Transaction`, these are financial activities that affect an account balance. The context also states these rules: debit transactions reduce account balance, credit transactions increase account balance, and transaction amounts are stored a…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_9`, `parent_chunk_data_dictionary.md_7`, `Automated Teller Machine→ATMS`, `Human-readable transaction description→TRANSACTIONS`, `parent_chunk_data_dictionary.md_6`, `parent_chunk_data_dictionary.md_11`, `Deposit Account→ACCOUNTS`, `parent_chunk_business_glossary.md_1`

**Context previews (first 3):**

1. _## transactions  **Description: ** Transaction fact table recording all account activity. Supports multiple transaction types including debits, credits, transfers, and withdrawals. Tracks calculated f…_

2. _## accounts  **Description: ** Deposit account master table supporting multiple account types (checking, savings, money market, CD, investment). Implements parent-child hierarchy for portfolio aggrega…_

3. _Business concept 'Automated Teller Machine' — a self-service banking terminal that allows customers to perform basic transactions without teller assistance. is implemented by physical table ATMS (colu…_

---

### ✅ 15 — How does the schema support joint account ownership between multiple customers?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.4870 | **Gate:** `proceed`

**Expected answer:**
> Joint ownership is implemented through the customer_account junction table, which creates a many-to-many relationship between customers and accounts. Each row has a relationship_type CHECK constraint allowing Owner, JointOwner, AuthorizedSigner, or Custodian. The ownership_percentage field (DECIMAL …

**System answer:**
> The schema supports joint account ownership through the `CUSTOMER_ACCOUNT` table, which is explicitly a junction table implementing a many-to-many relationship between `CUSTOMERS` and `ACCOUNTS`. This means one customer can be linked to multiple accounts, and one account can be linked to multiple customers.

At the schema level, joint ownership is represented by storing one row per customer-accoun…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_8`, `parent_chunk_data_dictionary.md_12`, `Customer Account Relationship`, `Customer Account Relationship→CUSTOMER_ACCOUNT`, `parent_chunk_data_dictionary.md_7`, `parent_chunk_data_dictionary.md_11`, `CUSTOMER_ACCOUNT→CUSTOMERS`, `parent_chunk_business_glossary.md_0`

**Context previews (first 3):**

1. _## customer_account  **Description: ** Junction table implementing many-to-many relationship between customers and accounts. Supports joint ownership, authorized signers, and custodial relationships. …_

2. _## Entity Relationship Summary  **Key Relationships: ** - customers ←→ accounts (many-to-many via customer_account) - accounts → accounts (self-reference for parent-child hierarchy) - accounts → trans…_

3. _Customer Account Relationship: The table is explicitly described as a junction table implementing a many-to-many relationship between customers and accounts, with foreign keys to both customers and ac…_

---

### ✅ 16 — What information does the cards table track and how are cards linked to customers and accounts?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.9528 | **Gate:** `proceed`

**Expected answer:**
> The cards table links to both accounts (account_id FK) and customers (customer_id FK), tracking card_type (Debit/Credit/ATM), card_network (Visa/Mastercard/Discover/AmericanExpress), card_number, cardholder name, expiration_date, and CVV. For spending controls it stores credit_limit (nullable, for c…

**System answer:**
> The `cards` table is the payment card issuance table for debit, credit, and ATM cards. It tracks cards issued to cardholders and linked accounts, including card identity, type, network, security features, limits, status, and usage timing.

From the context, it tracks these attributes in `CARDS`: `card_id` (primary key), `account_id`, `customer_id`, `card_number` (PAN, unique), `card_type` (Debit/C…

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
> The schema handles interest rates directly on the product master tables rather than through a separate interest table.

For deposit products, the business concept "Deposit Account" is implemented by `ACCOUNTS`. That table includes `interest_rate` and `interest_earned`, along with balances, fees, status, and lifecycle dates such as `opened_date`, `closed_date`, and `last_transaction_date`. The `acc…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_12`, `Deposit Account→ACCOUNTS`, `parent_chunk_data_dictionary.md_10`, `Loan Type (Mortgage, Personal, Auto, HELOC, CreditCard)→LOANS`, `parent_chunk_data_dictionary.md_7`, `LOANS→CUSTOMERS`, `LOANS→ACCOUNTS`, `parent_chunk_business_glossary.md_2`

**Context previews (first 3):**

1. _## Entity Relationship Summary  **Key Relationships: ** - customers ←→ accounts (many-to-many via customer_account) - accounts → accounts (self-reference for parent-child hierarchy) - accounts → trans…_

2. _Business concept 'Deposit Account' — The table is explicitly described as deposit accounts and contains core account master data such as account number, type, subtype, balances, interest rate, fees, s…_

3. _## loans  **Description: ** Loan portfolio table tracking all lending products including mortgages, personal loans, auto loans, HELOCs, and credit cards. Records original terms, amortization schedules…_

---

### ✅ 18 — What types of branches does the bank operate and how do they differ in capabilities?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.1556 | **Gate:** `proceed_with_warning`

**Expected answer:**
> The branches table supports three types via CHECK constraint: FullService, Satellite, and ATMOnly. The business glossary details each: FullService branches offer complete banking services including loan origination, financial advisors, and safe deposit boxes; Satellite branches have limited hours an…

**System answer:**
> The bank operates three branch types in the `BRANCHES` table via `branch_type`: `FullService`, `Satellite`, and `ATMOnly`.

The retrieved context describes `branches` as physical bank locations including full-service branches, satellite offices, and ATM-only locations. It also shows that branches track operational attributes such as `hours`, `atm_count`, `teller_count`, `manager_name`, `status`, a…

**Sources retrieved (12):** `Bank branch→BRANCHES`, `parent_chunk_data_dictionary.md_12`, `parent_chunk_data_dictionary.md_7`, `parent_chunk_data_dictionary.md_6`, `Deposit Account→ACCOUNTS`, `Automated Teller Machine→ATMS`, `parent_chunk_data_dictionary.md_5`, `parent_chunk_business_glossary.md_2`

**Context previews (first 3):**

1. _Business concept 'Bank branch' is implemented by physical table BRANCHES (columns: branch_id, branch_code, branch_name, branch_type, address, city, state, zip_code, phone, hours, atm_count, teller_cou…_

2. _## Entity Relationship Summary  **Key Relationships: ** - customers ←→ accounts (many-to-many via customer_account) - accounts → accounts (self-reference for parent-child hierarchy) - accounts → trans…_

3. _## accounts  **Description: ** Deposit account master table supporting multiple account types (checking, savings, money market, CD, investment). Implements parent-child hierarchy for portfolio aggrega…_

---

### ✅ 19 — How are ATMs related to branches in the schema and what types of ATMs exist?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.6184 | **Gate:** `proceed`

**Expected answer:**
> The atms table has an optional branch_id foreign key referencing branches. When branch_id is NULL, the ATM is standalone and not affiliated with any branch. ATM types are defined by CHECK constraint: Branch (on-premises), DriveThrough (vehicle-accessible), and Standalone (independent locations). Eac…

**System answer:**
> In the schema, ATMs are implemented by the `ATMS` table and branches by the `BRANCHES` table. `ATMS.branch_id` is a foreign key to `BRANCHES.branch_id`, so each ATM can reference a branch, and the relationship is one-to-many from branches to ATMs. The `branch_id` column in `ATMS` is nullable, which means some ATMs are standalone and not attached to any branch. The relationship summary also states …

**Sources retrieved (12):** `ATMS→BRANCHES`, `parent_chunk_data_dictionary.md_6`, `parent_chunk_data_dictionary.md_12`, `Automated Teller Machine→ATMS`, `Bank branch→BRANCHES`, `parent_chunk_data_dictionary.md_9`, `parent_chunk_business_glossary.md_3`, `parent_chunk_data_dictionary.md_5`

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
> The retrieved context does not define a full loan lifecycle from application to completion, so I cannot describe the application, underwriting, approval, funding, delinquency, payoff, or closure steps with confidence.

What is documented is the schema-level structure of `LOANS` and a few related business rules. The `loans` table tracks lending products such as Mortgage, Personal, Auto, HELOC, and …

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_10`, `parent_chunk_data_dictionary.md_7`, `Loan Type (Mortgage, Personal, Auto, HELOC, CreditCard)→LOANS`, `parent_chunk_data_dictionary.md_12`, `parent_chunk_business_glossary.md_2`, `parent_chunk_business_glossary.md_1`, `Loan Type (Mortgage, Personal, Auto, HELOC, CreditCard)`, `an individual or corporate entity that maintains a banking relationship with the institution, having completed Know Your Customer (KYC) verification→CUSTOMERS`

**Context previews (first 3):**

1. _## loans  **Description: ** Loan portfolio table tracking all lending products including mortgages, personal loans, auto loans, HELOCs, and credit cards. Records original terms, amortization schedules…_

2. _## accounts  **Description: ** Deposit account master table supporting multiple account types (checking, savings, money market, CD, investment). Implements parent-child hierarchy for portfolio aggrega…_

3. _Business concept 'Loan Type (Mortgage, Personal, Auto, HELOC, CreditCard)' is implemented by physical table LOANS (columns: loan_id, customer_id, loan_type, account_id, principal_amount, interest_rate…_

---

### ✅ 21 — What does preferred customer status mean and how is it tracked in the schema?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.5129 | **Gate:** `proceed`

**Expected answer:**
> Preferred status is tracked via the is_preferred boolean flag in the customers table (default: false). The business glossary states that preferred customers receive waived fees, preferred interest rates, and priority service. The glossary examples show preferred customers with longer tenure and high…

**System answer:**
> In this schema, preferred customer status means a customer is flagged for VIP treatment. That meaning comes from the `customers` table description, which says it includes “preferred customer flags for VIP treatment.”

It is tracked in the physical table `CUSTOMERS` using the column `is_preferred`. The `CUSTOMERS` table is the core customer master table for individual and corporate banking customer…

**Sources retrieved (12):** `an individual or corporate entity that maintains a banking relationship with the institution, having completed Know Your Customer (KYC) verification→CUSTOMERS`, `parent_chunk_data_dictionary.md_12`, `parent_chunk_data_dictionary.md_11`, `parent_chunk_data_dictionary.md_10`, `parent_chunk_data_dictionary.md_8`, `parent_chunk_data_dictionary.md_7`, `CARDS→CUSTOMERS`, `parent_chunk_data_dictionary.md_6`

**Context previews (first 3):**

1. _Business concept 'an individual or corporate entity that maintains a banking relationship with the institution, having completed Know Your Customer (KYC) verification' — An individual or corporate ent…_

2. _## Entity Relationship Summary  **Key Relationships: ** - customers ←→ accounts (many-to-many via customer_account) - accounts → accounts (self-reference for parent-child hierarchy) - accounts → trans…_

3. _## cards  **Description: ** Payment card issuance table for debit, credit, and ATM cards. Links cards to both customer and account. Tracks security features (chip, contactless, PIN), spending limits, …_

---

### ✅ 22 — How does the accounts table support interest tracking and what business rules govern interest?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.3044 | **Gate:** `proceed`

**Expected answer:**
> The accounts table has interest_rate (nullable DECIMAL for the annual rate) and interest_earned (DECIMAL for year-to-date interest credited). The business glossary states that deposit interest is credited monthly (typically the first day of the month) and that APY accounts for compounding effects. P…

**System answer:**
> The `ACCOUNTS` table supports interest tracking directly because it is the deposit account master table and is described as tracking balances, interest accrual, fees, and account lifecycle status. Its interest-related columns are `interest_rate`, which stores the rate on the deposit account, and `interest_earned`, which stores the amount of interest earned. The table also includes related financia…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_7`, `Deposit Account→ACCOUNTS`, `parent_chunk_data_dictionary.md_12`, `parent_chunk_data_dictionary.md_10`, `ACCOUNTS→BRANCHES`, `ACCOUNTS→ACCOUNTS`, `parent_chunk_data_dictionary.md_8`, `Loan Type (Mortgage, Personal, Auto, HELOC, CreditCard)→LOANS`

**Context previews (first 3):**

1. _## accounts  **Description: ** Deposit account master table supporting multiple account types (checking, savings, money market, CD, investment). Implements parent-child hierarchy for portfolio aggrega…_

2. _Business concept 'Deposit Account' — The table is explicitly described as deposit accounts and contains core account master data such as account number, type, subtype, balances, interest rate, fees, s…_

3. _## Entity Relationship Summary  **Key Relationships: ** - customers ←→ accounts (many-to-many via customer_account) - accounts → accounts (self-reference for parent-child hierarchy) - accounts → trans…_

---

### ✅ 23 — Can an account exist without any customer linked to it?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.1394 | **Gate:** `proceed_with_warning`

**Expected answer:**
> Looking at the schema, there is no database-level constraint that forces every account to have a customer_account row. The accounts table has no direct foreign key to customers — the relationship is through the customer_account junction table with a composite primary key (customer_id, account_id). H…

**System answer:**
> The retrieved context does not explicitly determine this.

What is supported by the context is that customer-to-account links are modeled through the CUSTOMER_ACCOUNT junction table, which implements a many-to-many relationship between customers and accounts. Each CUSTOMER_ACCOUNT row must reference an existing customer and an existing account, and it stores association details such as relationshi…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_8`, `Customer Account Relationship→CUSTOMER_ACCOUNT`, `CUSTOMER_ACCOUNT→CUSTOMERS`, `parent_chunk_data_dictionary.md_12`, `CUSTOMER_ACCOUNT→ACCOUNTS`, `parent_chunk_data_dictionary.md_11`, `Customer Account Relationship`, `parent_chunk_data_dictionary.md_10`

**Context previews (first 3):**

1. _## customer_account  **Description: ** Junction table implementing many-to-many relationship between customers and accounts. Supports joint ownership, authorized signers, and custodial relationships. …_

2. _Business concept 'Customer Account Relationship' — The table is explicitly described as a junction table implementing a many-to-many relationship between customers and accounts, with foreign keys to b…_

3. _Relationship: CUSTOMER_ACCOUNT references CUSTOMERS via foreign key CUSTOMER_ID -> CUSTOMERS.CUSTOMER_ID.…_

---

### ✅ 24 — How does the schema handle failed or cancelled transactions?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.2042 | **Gate:** `proceed`

**Expected answer:**
> The transactions table has a status column with CHECK constraint allowing Pending, Posted, Failed, Cancelled, and OnHold states. The business glossary explains that failed transactions are logged for audit but do not affect the account balance — the balance_after field would reflect no change. Poste…

**System answer:**
> The schema handles failed or cancelled transactions through the `TRANSACTIONS` table’s `status` field. The business concept `Transaction` explicitly defines the valid transaction states as `Pending`, `Posted`, `Failed`, `Cancelled`, and `OnHold`, and the concept-to-table mapping shows that `TRANSACTIONS` includes a `status` column along with `transaction_date`, `balance_after`, `description`, `ref…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_9`, `parent_chunk_data_dictionary.md_12`, `parent_chunk_data_dictionary.md_7`, `TRANSACTIONS→ACCOUNTS`, `Human-readable transaction description→TRANSACTIONS`, `Automated Teller Machine→ATMS`, `parent_chunk_business_glossary.md_1`, `parent_chunk_business_glossary.md_0`

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
> An ATM can have three operational states in the context: `Operational`, `OutOfService`, and `OutOfCash`. These come from the ATM business concept and the `ATMS` table, which tracks `status` for availability management.

The retrieved context does not define exactly what services are available in each state. It does show that ATM features are tracked separately through `supports_deposit` and `suppo…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_6`, `Automated Teller Machine→ATMS`, `ATMS→BRANCHES`, `parent_chunk_data_dictionary.md_12`, `parent_chunk_data_dictionary.md_11`, `parent_chunk_data_dictionary.md_9`, `Bank branch→BRANCHES`, `parent_chunk_business_glossary.md_3`

**Context previews (first 3):**

1. _## atms  **Description: ** ATM locations including branch-attached machines, drive-through ATMs, and standalone units. Tracks cash balances for replenishment scheduling, GPS coordinates for location s…_

2. _Business concept 'Automated Teller Machine' — a self-service banking terminal that allows customers to perform basic transactions without teller assistance. is implemented by physical table ATMS (colu…_

3. _Relationship: ATMS references BRANCHES via foreign key BRANCH_ID -> BRANCHES.BRANCH_ID.…_

---

## Anomalies & Observations

No anomalies detected. All questions grounded with acceptable RAGAS scores.
