# AB-19 — 02_intermediate_finance — Run Analysis

**Timestamp:** 2026-03-31 03:02:58  
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
| Triplets extracted | 609 |
| Entities resolved | 230 |
| Tables parsed | 8 |
| Tables completed | 8 |

## Query Evaluation Summary

| Metric | Value |
|--------|-------|
| Questions | 25 |
| Grounded | **25/25 (100%)** |
| Avg GT Coverage | 100% |
| Avg Top Score | 0.4791 |
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
> A checking account is an `account_type` value of the `accounts` table within the broader business concept of an Account or Deposit Account.

From the context, an Account is “a financial arrangement between a customer and the bank that allows deposit, withdrawal, and management of funds,” and the `accounts` table supports multiple account types including `Checking`, `Savings`, `MoneyMarket`, `CD`, …

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_7`, `parent_chunk_data_dictionary.md_8`, `Deposit Account→ACCOUNTS`, `parent_chunk_data_dictionary.md_9`, `parent_chunk_data_dictionary.md_10`, `parent_chunk_data_dictionary.md_12`, `parent_chunk_business_glossary.md_0`, `parent_chunk_business_glossary.md_1`

**Context previews (first 3):**

1. _## accounts  **Description: ** Deposit account master table supporting multiple account types (checking, savings, money market, CD, investment). Implements parent-child hierarchy for portfolio aggrega…_

2. _## customer_account  **Description: ** Junction table implementing many-to-many relationship between customers and accounts. Supports joint ownership, authorized signers, and custodial relationships. …_

3. _Business concept 'Deposit Account' — The table is explicitly described as deposit accounts and contains core account master data such as account number, type, balances, status, interest, fees, and ope…_

---

### ✅ 2 — What is the difference between a savings account and a money market account?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.6601 | **Gate:** `proceed`

**Expected answer:**
> Both savings and money market are account types defined in the accounts table CHECK constraint. The business glossary Interest section provides example rates: Standard Savings earns 0.25% APY (with monthly compounding), Premium Savings earns 0.50% APY (with daily compounding), while Money Market ear…

**System answer:**
> The retrieved context only shows that both Savings and MoneyMarket are valid account types in the `accounts` table / Account business concept. Specifically, `accounts.account_type` can be `Checking`, `Savings`, `MoneyMarket`, `CD`, or `Investment`.

It does not provide a business definition or rule explaining how a savings account differs from a money market account. So from the knowledge graph, I…

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
> From the retrieved context, APR and APY are both interest-related annual percentage measures, but they apply to different banking products.

APR means Annual Percentage Rate and is used for loans. It represents the cost of borrowing money.

APY means Annual Percentage Yield and is used for deposits. It represents the return paid by the bank on deposited money, and the context explicitly states tha…

**Sources retrieved (12):** `parent_chunk_business_glossary.md_2`, `parent_chunk_business_glossary.md_0`, `parent_chunk_business_glossary.md_1`, `parent_chunk_data_dictionary.md_7`, `parent_chunk_data_dictionary.md_11`, `parent_chunk_data_dictionary.md_8`, `parent_chunk_data_dictionary.md_6`, `parent_chunk_business_glossary.md_3`

**Context previews (first 3):**

1. _## Interest  **Definition: ** The cost of borrowing money (paid by borrower) or the return on depositing money (paid by bank), expressed as an annual percentage rate. **Business Context:** Interest is…_

2. _# Retail Banking Business Glossary  This document defines the core business concepts and terminology used in the retail banking domain.  ---  ## Account  **Definition: ** A financial arrangement betwe…_

3. _## Transaction  **Definition: ** Any financial activity that affects the balance of an account, including debits, credits, transfers, withdrawals, and fees. **Business Context:** Transactions represen…_

---

### ✅ 4 — What is KYC Level 2?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.6105 | **Gate:** `proceed`

**Expected answer:**
> The customers table has a kyc_status column with a CHECK constraint allowing Level1, Level2, and Level3. The business glossary states that Level1 is the minimum requirement for account opening, Level3 is required for high-value accounts and international transfers, and risk_profile determines eligib…

**System answer:**
> The retrieved context shows that KYC refers to Know Your Customer, and that KYC levels are constrained to Level1, Level2, or Level3. It also shows KYC status is stored on the CUSTOMERS table in the KYC_STATUS column as part of customer compliance data.

However, the context does not define what Level2 specifically means, how it differs from Level1 or Level3, or what criteria determine it.

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_12`, `Customer→CUSTOMERS`, `parent_chunk_data_dictionary.md_7`, `parent_chunk_data_dictionary.md_4`, `parent_chunk_business_glossary.md_0`, `Customer`, `parent_chunk_business_glossary.md_1`, `parent_chunk_data_dictionary.md_5`

**Context previews (first 3):**

1. _## Entity Relationship Summary  **Key Relationships: ** - customers ←→ accounts (many-to-many via customer_account) - accounts → accounts (self-reference for parent-child hierarchy) - accounts → trans…_

2. _Business concept 'Customer' — The table is explicitly described as the core customer dimension and contains master data for individual and corporate banking customers. Its columns (name, tax ID, conta…_

3. _## accounts  **Description: ** Deposit account master table supporting multiple account types (checking, savings, money market, CD, investment). Implements parent-child hierarchy for portfolio aggrega…_

---

### ✅ 5 — How does the schema support different account subtypes and their varying requirements?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.1891 | **Gate:** `proceed_with_warning`

**Expected answer:**
> The accounts table has an account_subtype column (VARCHAR 30, nullable) that stores values like Premium or Standard to differentiate within each account_type. Combined with the minimum_balance and monthly_fee columns, each account can have different requirements configured per subtype. The account_t…

**System answer:**
> The retrieved context shows that deposit account subtype support is centered on the `ACCOUNTS` table.

`ACCOUNTS` has both `ACCOUNT_TYPE` and `ACCOUNT_SUBTYPE`. `ACCOUNT_TYPE` identifies the major product category and is described with values `Checking`, `Savings`, `MoneyMarket`, `CD`, and `Investment`. `ACCOUNT_SUBTYPE` stores a finer classification, with examples such as `Premium`, `Student`, an…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_7`, `parent_chunk_data_dictionary.md_12`, `Deposit Account→ACCOUNTS`, `parent_chunk_data_dictionary.md_8`, `parent_chunk_data_dictionary.md_9`, `parent_chunk_data_dictionary.md_11`, `parent_chunk_data_dictionary.md_10`, `parent_chunk_business_glossary.md_0`

**Context previews (first 3):**

1. _## accounts  **Description: ** Deposit account master table supporting multiple account types (checking, savings, money market, CD, investment). Implements parent-child hierarchy for portfolio aggrega…_

2. _## Entity Relationship Summary  **Key Relationships: ** - customers ←→ accounts (many-to-many via customer_account) - accounts → accounts (self-reference for parent-child hierarchy) - accounts → trans…_

3. _Business concept 'Deposit Account' — The table is explicitly described as deposit accounts and contains core account master data such as account number, type, balances, status, interest, fees, and ope…_

---

### ✅ 6 — What types of loan products does the bank offer?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.4020 | **Gate:** `proceed`

**Expected answer:**
> The bank offers five loan types defined by the CHECK constraint on loans.loan_type: (1) Mortgage — secured by real estate, glossary example shows $350,000 at 5.50% APR for 360 months; (2) Personal Loan — unsecured, example $15,000 at 8.50% APR for 48 months; (3) Auto Loan — secured by vehicle, examp…

**System answer:**
> The bank offers these loan product types, as defined in the `loans` table and its `loan_type` column: Mortgage, Personal, Auto, HELOC, and CreditCard. The `loans` table description also states it tracks lending products including mortgages, personal loans, auto loans, HELOCs, and credit cards.

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_10`, `parent_chunk_data_dictionary.md_12`, `Loan→LOANS`, `parent_chunk_data_dictionary.md_7`, `Customer→CUSTOMERS`, `LOANS→CUSTOMERS`, `parent_chunk_business_glossary.md_1`, `parent_chunk_business_glossary.md_2`

**Context previews (first 3):**

1. _## loans  **Description: ** Loan portfolio table tracking all lending products including mortgages, personal loans, auto loans, HELOCs, and credit cards. Records original terms, amortization schedules…_

2. _## Entity Relationship Summary  **Key Relationships: ** - customers ←→ accounts (many-to-many via customer_account) - accounts → accounts (self-reference for parent-child hierarchy) - accounts → trans…_

3. _Business concept 'Loan' — The table stores core loan attributes such as borrower, principal, interest rate, term, amortization balance, origination date, maturity date, and lifecycle status, which dir…_

---

### ✅ 7 — What is the daily ATM withdrawal limit for standard customers?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.3743 | **Gate:** `proceed`

**Expected answer:**
> The cards table has an atm_daily_limit column with a default value of $500. The business glossary Card Examples confirm this: a standard Debit Card has a $500 ATM limit, while a Premium Debit card has a $2,000 ATM limit. The daily_limit column (default $3,000) controls POS spending separately. These…

**System answer:**
> The retrieved context does not state a specific daily ATM withdrawal limit amount for standard customers.

What it does show is that the physical table CARDS includes an `ATM_DAILY_LIMIT` column, and the table description says cards track spending limits. It also shows the ACCOUNTS table has an `account_subtype` column with examples including `Standard`, `Premium`, and `Student`. However, the cont…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_11`, `Payment Card Issuance→CARDS`, `parent_chunk_data_dictionary.md_6`, `parent_chunk_data_dictionary.md_12`, `parent_chunk_data_dictionary.md_7`, `Banking Center→BRANCHES`, `Automated Teller Machine→ATMS`, `parent_chunk_business_glossary.md_3`

**Context previews (first 3):**

1. _## cards  **Description: ** Payment card issuance table for debit, credit, and ATM cards. Links cards to both customer and account. Tracks security features (chip, contactless, PIN), spending limits, …_

2. _Business concept 'Payment Card Issuance' — The table description explicitly states it stores debit, credit, and ATM cards and links each card to a customer and account. The columns capture card number…_

3. _## atms  **Description: ** ATM locations including branch-attached machines, drive-through ATMs, and standalone units. Tracks cash balances for replenishment scheduling, GPS coordinates for location s…_

---

### ✅ 8 — What is the difference between a parent account and a child account?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.3098 | **Gate:** `proceed`

**Expected answer:**
> The accounts table supports parent-child hierarchies through the parent_account_id self-referencing foreign key, with a CHECK constraint preventing circular references (parent_account_id != account_id). The data dictionary describes this as supporting portfolio aggregation where parent accounts (typ…

**System answer:**
> A parent account is an account in `ACCOUNTS` that other accounts reference through `PARENT_ACCOUNT_ID`, while a child account is an account whose `PARENT_ACCOUNT_ID` points to another row in `ACCOUNTS.ACCOUNT_ID`.

From the context, this hierarchy exists to support portfolio aggregation, and specifically “investment accounts contain child accounts.” So the parent account serves as the higher-level…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_7`, `parent_chunk_data_dictionary.md_12`, `Deposit Account→ACCOUNTS`, `ACCOUNTS→ACCOUNTS`, `parent_chunk_data_dictionary.md_8`, `parent_chunk_data_dictionary.md_9`, `parent_chunk_data_dictionary.md_11`, `parent_chunk_data_dictionary.md_10`

**Context previews (first 3):**

1. _## accounts  **Description: ** Deposit account master table supporting multiple account types (checking, savings, money market, CD, investment). Implements parent-child hierarchy for portfolio aggrega…_

2. _## Entity Relationship Summary  **Key Relationships: ** - customers ←→ accounts (many-to-many via customer_account) - accounts → accounts (self-reference for parent-child hierarchy) - accounts → trans…_

3. _Business concept 'Deposit Account' — The table is explicitly described as deposit accounts and contains core account master data such as account number, type, balances, status, interest, fees, and ope…_

---

### ✅ 9 — What does the status 'Frozen' mean for a card?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0630 | **Gate:** `proceed_with_warning`

**Expected answer:**
> The cards table has a status column with four states defined by CHECK constraint: Active, Frozen, Blocked, and Expired. The business glossary states that lost or stolen cards must be immediately blocked to prevent fraud, and that expired cards are automatically renewed. The glossary distinguishes Fr…

**System answer:**
> From the retrieved context, I can only confirm that the `CARDS` table has a `STATUS` column and that payment card issuance “tracks ... card status.” The context also says cards are linked to a customer and an account.

However, the retrieved context does not define the meaning of any specific card status value, including `Frozen`. The glossary does mention `Frozen` as an account status under the b…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_7`, `parent_chunk_data_dictionary.md_10`, `parent_chunk_data_dictionary.md_11`, `Payment Card Issuance→CARDS`, `parent_chunk_data_dictionary.md_6`, `parent_chunk_data_dictionary.md_9`, `parent_chunk_business_glossary.md_0`, `parent_chunk_business_glossary.md_3`

**Context previews (first 3):**

1. _## accounts  **Description: ** Deposit account master table supporting multiple account types (checking, savings, money market, CD, investment). Implements parent-child hierarchy for portfolio aggrega…_

2. _## loans  **Description: ** Loan portfolio table tracking all lending products including mortgages, personal loans, auto loans, HELOCs, and credit cards. Records original terms, amortization schedules…_

3. _## cards  **Description: ** Payment card issuance table for debit, credit, and ATM cards. Links cards to both customer and account. Tracks security features (chip, contactless, PIN), spending limits, …_

---

### ✅ 10 — How does the transactions table track the impact of each transaction on account balances?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.8454 | **Gate:** `proceed`

**Expected answer:**
> The transactions table includes a balance_after column (DECIMAL 15,2) that records the account balance after each transaction is applied. Combined with the amount column, transaction_type (Debit/Credit/Transfer/Payment/Withdrawal/Deposit/Fee), and status (Pending/Posted/Failed/Cancelled/OnHold), thi…

**System answer:**
> The `TRANSACTIONS` table tracks each transaction’s impact on an account balance in several coordinated ways.

It links every transaction to a specific account through `ACCOUNT_ID`, which is a foreign key to `ACCOUNTS.ACCOUNT_ID`. That establishes which deposit account the activity affects.

For the financial effect itself, the table stores `TRANSACTION_TYPE`, `AMOUNT`, and `BALANCE_AFTER`. The `AM…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_9`, `TRANSACTIONS→ACCOUNTS`, `Financial Transaction→TRANSACTIONS`, `parent_chunk_data_dictionary.md_7`, `Deposit Account→ACCOUNTS`, `ACCOUNTS→BRANCHES`, `ACCOUNTS→ACCOUNTS`, `parent_chunk_data_dictionary.md_10`

**Context previews (first 3):**

1. _## transactions  **Description: ** Transaction fact table recording all account activity. Supports multiple transaction types including debits, credits, transfers, and withdrawals. Tracks calculated f…_

2. _Relationship: TRANSACTIONS references ACCOUNTS via foreign key ACCOUNT_ID -> ACCOUNTS.ACCOUNT_ID.…_

3. _Business concept 'Financial Transaction' — The table is explicitly described as a transaction fact table for all account activity, with fields such as transaction_type, amount, status, transaction_dat…_

---

### ✅ 11 — How does the customer_account junction table support multiple ownership types?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.9865 | **Gate:** `proceed`

**Expected answer:**
> The customer_account table implements a many-to-many relationship between customers and accounts with a composite primary key (customer_id, account_id). It supports four relationship types via CHECK constraint: Owner, JointOwner, AuthorizedSigner, and Custodian. The is_primary flag designates the pr…

**System answer:**
> The `customer_account` table supports multiple ownership types by acting as the many-to-many junction between `customers` and `accounts`. That means one customer can be linked to multiple accounts, and one account can be linked to multiple customers.

It distinguishes the kind of relationship through `relationship_type`, which is defined as `Owner`, `JointOwner`, `AuthorizedSigner`, or `Custodian`…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_8`, `Customer Account Relationship→CUSTOMER_ACCOUNT`, `parent_chunk_data_dictionary.md_12`, `CUSTOMER_ACCOUNT→CUSTOMERS`, `parent_chunk_data_dictionary.md_7`, `CUSTOMER_ACCOUNT→ACCOUNTS`, `Deposit Account→ACCOUNTS`, `parent_chunk_data_dictionary.md_9`

**Context previews (first 3):**

1. _## customer_account  **Description: ** Junction table implementing many-to-many relationship between customers and accounts. Supports joint ownership, authorized signers, and custodial relationships. …_

2. _Business concept 'Customer Account Relationship' — The DDL explicitly labels this as a junction table for a many-to-many relationship between customers and accounts, with relationship_type, is_primary…_

3. _## Entity Relationship Summary  **Key Relationships: ** - customers ←→ accounts (many-to-many via customer_account) - accounts → accounts (self-reference for parent-child hierarchy) - accounts → trans…_

---

### ✅ 12 — What is the difference between current_balance and available_balance in the accounts table?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.8328 | **Gate:** `proceed`

**Expected answer:**
> The accounts table tracks two separate balance fields: current_balance includes all transactions including pending ones, while available_balance excludes holds and pending transactions and represents what the customer can actually withdraw. The business glossary confirms this distinction, stating th…

**System answer:**
> The retrieved context does not specify the precise difference between `current_balance` and `available_balance`.

What it does show is that the `ACCOUNTS` table includes both columns, `CURRENT_BALANCE` and `AVAILABLE_BALANCE`, and the Retail Banking Business Glossary lists “Current Balance vs. Available Balance” as a key attribute of an Account. However, no explicit definition or calculation rule …

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_7`, `Deposit Account→ACCOUNTS`, `parent_chunk_data_dictionary.md_10`, `Financial Transaction→TRANSACTIONS`, `parent_chunk_data_dictionary.md_6`, `parent_chunk_data_dictionary.md_9`, `Automated Teller Machine→ATMS`, `ACCOUNTS→ACCOUNTS`

**Context previews (first 3):**

1. _## accounts  **Description: ** Deposit account master table supporting multiple account types (checking, savings, money market, CD, investment). Implements parent-child hierarchy for portfolio aggrega…_

2. _Business concept 'Deposit Account' — The table is explicitly described as deposit accounts and contains core account master data such as account number, type, balances, status, interest, fees, and ope…_

3. _## loans  **Description: ** Loan portfolio table tracking all lending products including mortgages, personal loans, auto loans, HELOCs, and credit cards. Records original terms, amortization schedules…_

---

### ✅ 13 — How are loans linked to both customers and accounts in the schema?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.8105 | **Gate:** `proceed`

**Expected answer:**
> The loans table has a customer_id foreign key referencing the customers table (the borrower) and an optional account_id foreign key referencing the accounts table (for linked payment accounts). Each loan belongs to exactly one customer, and can optionally be connected to an account for automatic pay…

**System answer:**
> In the schema, `LOANS` is linked directly to both `CUSTOMERS` and `ACCOUNTS` through foreign keys on the `loans` table.

`LOANS.CUSTOMER_ID` references `CUSTOMERS.CUSTOMER_ID`. The `loans` table describes `customer_id` as a non-null foreign key to customers, identifying the borrower. The relationship summary also states `customers → loans` is one-to-many, so one customer can have multiple loans.

…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_12`, `LOANS→CUSTOMERS`, `LOANS→ACCOUNTS`, `parent_chunk_data_dictionary.md_10`, `CUSTOMER_ACCOUNT→CUSTOMERS`, `parent_chunk_data_dictionary.md_8`, `CUSTOMER_ACCOUNT→ACCOUNTS`, `Customer Account Relationship→CUSTOMER_ACCOUNT`

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
> The system supports these transaction types in `transactions.transaction_type`: Debit, Credit, Transfer, Payment, Withdrawal, Deposit, and Fee. The `transactions` table is described as recording all account activity, and the `Transaction` business concept defines a transaction as any financial activity that affects an account balance, including those same types.

For lifecycle and status, the `Tra…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_9`, `parent_chunk_data_dictionary.md_7`, `Automated Teller Machine→ATMS`, `Automated Teller Machine`, `Loan→LOANS`, `Financial Transaction→TRANSACTIONS`, `parent_chunk_data_dictionary.md_6`, `parent_chunk_business_glossary.md_1`

**Context previews (first 3):**

1. _## transactions  **Description: ** Transaction fact table recording all account activity. Supports multiple transaction types including debits, credits, transfers, and withdrawals. Tracks calculated f…_

2. _## accounts  **Description: ** Deposit account master table supporting multiple account types (checking, savings, money market, CD, investment). Implements parent-child hierarchy for portfolio aggrega…_

3. _Business concept 'Automated Teller Machine' — The table is explicitly described as ATM locations and includes ATM-specific attributes such as atm_code, atm_type, cash_balance, last_replenished, and su…_

---

### ✅ 15 — How does the schema support joint account ownership between multiple customers?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.4870 | **Gate:** `proceed`

**Expected answer:**
> Joint ownership is implemented through the customer_account junction table, which creates a many-to-many relationship between customers and accounts. Each row has a relationship_type CHECK constraint allowing Owner, JointOwner, AuthorizedSigner, or Custodian. The ownership_percentage field (DECIMAL …

**System answer:**
> The schema supports joint account ownership through the `customer_account` table, which is explicitly defined as a junction table for the many-to-many relationship between `customers` and `accounts`. This means a single account can be linked to multiple customers, and a single customer can be linked to multiple accounts.

At the schema level, each relationship is stored as a row in `CUSTOMER_ACCOU…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_8`, `parent_chunk_data_dictionary.md_12`, `Customer Account Relationship→CUSTOMER_ACCOUNT`, `parent_chunk_data_dictionary.md_7`, `Deposit Account→ACCOUNTS`, `parent_chunk_data_dictionary.md_11`, `Customer Account Relationship`, `parent_chunk_business_glossary.md_0`

**Context previews (first 3):**

1. _## customer_account  **Description: ** Junction table implementing many-to-many relationship between customers and accounts. Supports joint ownership, authorized signers, and custodial relationships. …_

2. _## Entity Relationship Summary  **Key Relationships: ** - customers ←→ accounts (many-to-many via customer_account) - accounts → accounts (self-reference for parent-child hierarchy) - accounts → trans…_

3. _Business concept 'Customer Account Relationship' — The DDL explicitly labels this as a junction table for a many-to-many relationship between customers and accounts, with relationship_type, is_primary…_

---

### ✅ 16 — What information does the cards table track and how are cards linked to customers and accounts?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.9563 | **Gate:** `proceed`

**Expected answer:**
> The cards table links to both accounts (account_id FK) and customers (customer_id FK), tracking card_type (Debit/Credit/ATM), card_network (Visa/Mastercard/Discover/AmericanExpress), card_number, cardholder name, expiration_date, and CVV. For spending controls it stores credit_limit (nullable, for c…

**System answer:**
> The `CARDS` table is the payment card issuance table. It stores debit, credit, and ATM cards, and tracks both identifying and operational card details. From the context, it captures the card number (`CARD_NUMBER`), card type (`CARD_TYPE`), card network (`CARD_NETWORK`), card name (`CARD_NAME`), expiration date (`EXPIRATION_DATE`), CVV (`CVV`), credit limit (`CREDIT_LIMIT`), daily spending limit (`…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_11`, `Payment Card Issuance→CARDS`, `CARDS→CUSTOMERS`, `CARDS→ACCOUNTS`, `parent_chunk_data_dictionary.md_10`, `CUSTOMER_ACCOUNT→CUSTOMERS`, `CUSTOMER_ACCOUNT→ACCOUNTS`, `parent_chunk_data_dictionary.md_8`

**Context previews (first 3):**

1. _## cards  **Description: ** Payment card issuance table for debit, credit, and ATM cards. Links cards to both customer and account. Tracks security features (chip, contactless, PIN), spending limits, …_

2. _Business concept 'Payment Card Issuance' — The table description explicitly states it stores debit, credit, and ATM cards and links each card to a customer and account. The columns capture card number…_

3. _Relationship: CARDS references CUSTOMERS via foreign key CUSTOMER_ID -> CUSTOMERS.CUSTOMER_ID.…_

---

### ✅ 17 — How does the schema handle interest rates across deposit and loan products?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0574 | **Gate:** `proceed_with_warning`

**Expected answer:**
> Interest rates are stored differently for deposits and loans. The accounts table has an interest_rate column (nullable DECIMAL 5,4) and interest_earned for year-to-date tracking. The loans table has its own interest_rate column representing APR. The business glossary explains that APR (Annual Percen…

**System answer:**
> The schema uses a common interest-rate field on both deposit and loan products, but it supports them differently through their surrounding attributes.

For deposit products, the physical table is ACCOUNTS, which implements the “Deposit Account” concept. It includes INTEREST_RATE and INTEREST_EARNED, along with balances, fees, and lifecycle dates. The business glossary for Account says deposit acco…

**Sources retrieved (12):** `Loan→LOANS`, `parent_chunk_data_dictionary.md_12`, `parent_chunk_data_dictionary.md_10`, `parent_chunk_data_dictionary.md_7`, `Deposit Account→ACCOUNTS`, `LOANS→CUSTOMERS`, `parent_chunk_business_glossary.md_2`, `Loan`

**Context previews (first 3):**

1. _Business concept 'Loan' — The table stores core loan attributes such as borrower, principal, interest rate, term, amortization balance, origination date, maturity date, and lifecycle status, which dir…_

2. _## Entity Relationship Summary  **Key Relationships: ** - customers ←→ accounts (many-to-many via customer_account) - accounts → accounts (self-reference for parent-child hierarchy) - accounts → trans…_

3. _## loans  **Description: ** Loan portfolio table tracking all lending products including mortgages, personal loans, auto loans, HELOCs, and credit cards. Records original terms, amortization schedules…_

---

### ✅ 18 — What types of branches does the bank operate and how do they differ in capabilities?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.1556 | **Gate:** `proceed_with_warning`

**Expected answer:**
> The branches table supports three types via CHECK constraint: FullService, Satellite, and ATMOnly. The business glossary details each: FullService branches offer complete banking services including loan origination, financial advisors, and safe deposit boxes; Satellite branches have limited hours an…

**System answer:**
> The bank operates three branch types in the `branches` table, stored in `branches.branch_type`: `FullService`, `Satellite`, and `ATMOnly`.

From the context, they differ as follows:

`FullService` branches are physical bank locations in the broader “Banking Center” sense and are tracked with operating and service-related attributes such as `hours`, `atm_count`, staffing levels like `teller_count`,…

**Sources retrieved (12):** `Banking Center→BRANCHES`, `parent_chunk_data_dictionary.md_12`, `parent_chunk_data_dictionary.md_7`, `Automated Teller Machine→ATMS`, `parent_chunk_data_dictionary.md_6`, `Automated Teller Machine`, `parent_chunk_data_dictionary.md_5`, `parent_chunk_business_glossary.md_2`

**Context previews (first 3):**

1. _Business concept 'Banking Center' — The table stores physical bank location records with codes, names, address details, operating hours, staffing counts, and status, which aligns well with a banking c…_

2. _## Entity Relationship Summary  **Key Relationships: ** - customers ←→ accounts (many-to-many via customer_account) - accounts → accounts (self-reference for parent-child hierarchy) - accounts → trans…_

3. _## accounts  **Description: ** Deposit account master table supporting multiple account types (checking, savings, money market, CD, investment). Implements parent-child hierarchy for portfolio aggrega…_

---

### ✅ 19 — How are ATMs related to branches in the schema and what types of ATMs exist?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.6184 | **Gate:** `proceed`

**Expected answer:**
> The atms table has an optional branch_id foreign key referencing branches. When branch_id is NULL, the ATM is standalone and not affiliated with any branch. ATM types are defined by CHECK constraint: Branch (on-premises), DriveThrough (vehicle-accessible), and Standalone (independent locations). Eac…

**System answer:**
> In the schema, `ATMS` is related to `BRANCHES` through the foreign key `ATMS.BRANCH_ID -> BRANCHES.BRANCH_ID`. This means a branch can have many ATMs (`branches -> atms` is one-to-many), while each ATM can reference one branch. The `branch_id` column in `ATMS` is nullable, which is specifically used for standalone ATMs that are not affiliated with any branch. The relationship has no cascade by def…

**Sources retrieved (12):** `ATMS→BRANCHES`, `parent_chunk_data_dictionary.md_6`, `Automated Teller Machine`, `Automated Teller Machine→ATMS`, `parent_chunk_data_dictionary.md_12`, `Banking Center→BRANCHES`, `parent_chunk_data_dictionary.md_9`, `parent_chunk_business_glossary.md_3`

**Context previews (first 3):**

1. _Relationship: ATMS references BRANCHES via foreign key BRANCH_ID -> BRANCHES.BRANCH_ID.…_

2. _## atms  **Description: ** ATM locations including branch-attached machines, drive-through ATMs, and standalone units. Tracks cash balances for replenishment scheduling, GPS coordinates for location s…_

3. _Automated Teller Machine: The table is explicitly described as ATM locations and includes ATM-specific attributes such as atm_code, atm_type, cash_balance, last_replenished, and support flags for depo…_

---

### ✅ 20 — What is the lifecycle of a loan from application to completion?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0583 | **Gate:** `proceed_with_warning`

**Expected answer:**
> The loans table tracks loan status through five states defined by CHECK constraint: Pending (application submitted, default), Approved (credit approved but not yet funded), Active (loan funded and being repaid), PaidOff (fully repaid), and Defaulted (borrower failed to repay). Each loan records orig…

**System answer:**
> The retrieved context does not describe a loan lifecycle “from application to completion.” It does not include any application, underwriting, approval, funding, payoff, or closure workflow.

What it does show is how the loan is represented once it exists as a servicing record in the `LOANS` table. The `Loan` business concept is implemented by `LOANS`, which stores the borrower (`CUSTOMER_ID`), loa…

**Sources retrieved (12):** `Loan→LOANS`, `parent_chunk_data_dictionary.md_10`, `parent_chunk_data_dictionary.md_7`, `parent_chunk_data_dictionary.md_12`, `LOANS→CUSTOMERS`, `Loan`, `parent_chunk_business_glossary.md_2`, `parent_chunk_business_glossary.md_1`

**Context previews (first 3):**

1. _Business concept 'Loan' — The table stores core loan attributes such as borrower, principal, interest rate, term, amortization balance, origination date, maturity date, and lifecycle status, which dir…_

2. _## loans  **Description: ** Loan portfolio table tracking all lending products including mortgages, personal loans, auto loans, HELOCs, and credit cards. Records original terms, amortization schedules…_

3. _## accounts  **Description: ** Deposit account master table supporting multiple account types (checking, savings, money market, CD, investment). Implements parent-child hierarchy for portfolio aggrega…_

---

### ✅ 21 — What does preferred customer status mean and how is it tracked in the schema?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.5129 | **Gate:** `proceed`

**Expected answer:**
> Preferred status is tracked via the is_preferred boolean flag in the customers table (default: false). The business glossary states that preferred customers receive waived fees, preferred interest rates, and priority service. The glossary examples show preferred customers with longer tenure and high…

**System answer:**
> Preferred customer status means a customer is flagged for VIP treatment. In the schema, this is part of the Customer concept implemented by the `CUSTOMERS` table, which is described as the core customer dimension for individual and corporate banking customers.

It is tracked directly in `CUSTOMERS` through the `IS_PREFERRED` column. The same table also stores the broader customer master data aroun…

**Sources retrieved (12):** `Customer→CUSTOMERS`, `parent_chunk_data_dictionary.md_12`, `parent_chunk_data_dictionary.md_11`, `parent_chunk_data_dictionary.md_10`, `parent_chunk_data_dictionary.md_8`, `parent_chunk_data_dictionary.md_7`, `Loan→LOANS`, `parent_chunk_data_dictionary.md_4`

**Context previews (first 3):**

1. _Business concept 'Customer' — The table is explicitly described as the core customer dimension and contains master data for individual and corporate banking customers. Its columns (name, tax ID, conta…_

2. _## Entity Relationship Summary  **Key Relationships: ** - customers ←→ accounts (many-to-many via customer_account) - accounts → accounts (self-reference for parent-child hierarchy) - accounts → trans…_

3. _## cards  **Description: ** Payment card issuance table for debit, credit, and ATM cards. Links cards to both customer and account. Tracks security features (chip, contactless, PIN), spending limits, …_

---

### ✅ 22 — How does the accounts table support interest tracking and what business rules govern interest?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.3044 | **Gate:** `proceed`

**Expected answer:**
> The accounts table has interest_rate (nullable DECIMAL for the annual rate) and interest_earned (DECIMAL for year-to-date interest credited). The business glossary states that deposit interest is credited monthly (typically the first day of the month) and that APY accounts for compounding effects. P…

**System answer:**
> The `ACCOUNTS` table supports interest tracking directly through its interest-related attributes and account lifecycle data. In the concept-to-table mapping, `ACCOUNTS` includes `INTEREST_RATE` and `INTEREST_EARNED`, and the table description says it “tracks balances, interest accrual, fees, and account lifecycle status.” The broader account definition also identifies “Interest Rate and Interest E…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_7`, `Deposit Account→ACCOUNTS`, `Loan→LOANS`, `parent_chunk_data_dictionary.md_12`, `parent_chunk_data_dictionary.md_10`, `ACCOUNTS→BRANCHES`, `ACCOUNTS→ACCOUNTS`, `parent_chunk_business_glossary.md_2`

**Context previews (first 3):**

1. _## accounts  **Description: ** Deposit account master table supporting multiple account types (checking, savings, money market, CD, investment). Implements parent-child hierarchy for portfolio aggrega…_

2. _Business concept 'Deposit Account' — The table is explicitly described as deposit accounts and contains core account master data such as account number, type, balances, status, interest, fees, and ope…_

3. _Business concept 'Loan' — The table stores core loan attributes such as borrower, principal, interest rate, term, amortization balance, origination date, maturity date, and lifecycle status, which dir…_

---

### ✅ 23 — Can an account exist without any customer linked to it?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.1394 | **Gate:** `proceed_with_warning`

**Expected answer:**
> Looking at the schema, there is no database-level constraint that forces every account to have a customer_account row. The accounts table has no direct foreign key to customers — the relationship is through the customer_account junction table with a composite primary key (customer_id, account_id). H…

**System answer:**
> The retrieved context does not explicitly say whether every account must be linked to at least one customer.

What is known from the context is that customer-to-account linkage is modeled through the `CUSTOMER_ACCOUNT` junction table, which implements a many-to-many relationship between customers and accounts. A `CUSTOMER_ACCOUNT` row requires both an existing customer and an existing account, bec…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_8`, `Customer Account Relationship→CUSTOMER_ACCOUNT`, `CUSTOMER_ACCOUNT→CUSTOMERS`, `parent_chunk_data_dictionary.md_12`, `CUSTOMER_ACCOUNT→ACCOUNTS`, `parent_chunk_data_dictionary.md_11`, `parent_chunk_data_dictionary.md_10`, `Payment Card Issuance→CARDS`

**Context previews (first 3):**

1. _## customer_account  **Description: ** Junction table implementing many-to-many relationship between customers and accounts. Supports joint ownership, authorized signers, and custodial relationships. …_

2. _Business concept 'Customer Account Relationship' — The DDL explicitly labels this as a junction table for a many-to-many relationship between customers and accounts, with relationship_type, is_primary…_

3. _Relationship: CUSTOMER_ACCOUNT references CUSTOMERS via foreign key CUSTOMER_ID -> CUSTOMERS.CUSTOMER_ID.…_

---

### ✅ 24 — How does the schema handle failed or cancelled transactions?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.2042 | **Gate:** `proceed`

**Expected answer:**
> The transactions table has a status column with CHECK constraint allowing Pending, Posted, Failed, Cancelled, and OnHold states. The business glossary explains that failed transactions are logged for audit but do not affect the account balance — the balance_after field would reflect no change. Poste…

**System answer:**
> From the retrieved context, failed or cancelled transactions are handled at the schema level through the `STATUS` field on the `TRANSACTIONS` table.

The `TRANSACTIONS` table is the physical implementation of the business concept `Financial Transaction`, and its documented columns include `STATUS`, `TRANSACTION_DATE`, `BALANCE_AFTER`, `DESCRIPTION`, and `REFERENCE_NUMBER`. The business definition …

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_9`, `parent_chunk_data_dictionary.md_12`, `parent_chunk_data_dictionary.md_7`, `TRANSACTIONS→ACCOUNTS`, `Financial Transaction→TRANSACTIONS`, `parent_chunk_business_glossary.md_1`, `parent_chunk_business_glossary.md_0`, `parent_chunk_business_glossary.md_3`

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
> An ATM can have these status values: Operational, OutOfService, and OutOfCash.

From the retrieved context, these are the ATM “Status” values, and the ATMS table description says status is tracked “for availability management.” The ATM concept also identifies supported features as separate attributes, specifically Deposit and Cardless Withdrawal, but the context does not define how those features …

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_6`, `Automated Teller Machine→ATMS`, `Banking Center→BRANCHES`, `Automated Teller Machine`, `Payment Card Issuance→CARDS`, `ATMS→BRANCHES`, `parent_chunk_business_glossary.md_3`, `parent_chunk_data_dictionary.md_5`

**Context previews (first 3):**

1. _## atms  **Description: ** ATM locations including branch-attached machines, drive-through ATMs, and standalone units. Tracks cash balances for replenishment scheduling, GPS coordinates for location s…_

2. _Business concept 'Automated Teller Machine' — The table is explicitly described as ATM locations and includes ATM-specific attributes such as atm_code, atm_type, cash_balance, last_replenished, and su…_

3. _Business concept 'Banking Center' — The table stores physical bank location records with codes, names, address details, operating hours, staffing counts, and status, which aligns well with a banking c…_

---

## Anomalies & Observations

No anomalies detected. All questions grounded with acceptable RAGAS scores.
