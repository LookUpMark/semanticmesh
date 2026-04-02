# AB-20 — 02_intermediate_finance — Run Analysis

**Timestamp:** 2026-03-30 21:53:46  
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

Builder skipped (`--no-builder`).

## Query Evaluation Summary

| Metric | Value |
|--------|-------|
| Questions | 25 |
| Grounded | **25/25 (100%)** |
| Avg GT Coverage | 100% |
| Avg Top Score | 0.4753 |
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
> The retrieved context does not provide a separate business definition for “checking account.” It does show that Checking is one of the valid `account_type` values in `ACCOUNTS` for the business concept Account / Deposit Account.

From the context, a checking account is therefore an Account or Deposit Account whose `account_type` is `Checking`. Accounts are defined as financial arrangements between…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_7`, `parent_chunk_data_dictionary.md_8`, `parent_chunk_data_dictionary.md_9`, `physical banking location→BRANCHES`, `Deposit Account→ACCOUNTS`, `parent_chunk_data_dictionary.md_10`, `parent_chunk_business_glossary.md_0`, `Deposit Account`

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
> The retrieved context only shows that both Savings and MoneyMarket are valid `account_type` values in the `accounts` table / Account business concept.

From the context, I can say:
Savings is an account type.
MoneyMarket is an account type.
Both are deposit account types managed in `ACCOUNTS`, which tracks balances, interest, fees, status, and lifecycle dates.

The context does not provide a busin…

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
> From the Interest concept, APR and APY are both interest measures, but they apply in different contexts.

APR stands for Annual Percentage Rate and is used for loans. It reflects the cost of borrowing money.

APY stands for Annual Percentage Yield and is used for deposits. It reflects the return on deposited money, and the context states that APY accounts for compounding.

So, in this glossary: AP…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_10`, `parent_chunk_business_glossary.md_2`, `parent_chunk_business_glossary.md_0`, `parent_chunk_business_glossary.md_1`, `parent_chunk_data_dictionary.md_7`, `parent_chunk_data_dictionary.md_11`, `parent_chunk_data_dictionary.md_8`, `Automated Teller Machine`

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
> The retrieved context does not define what “KYC Level 2” means. It only states that KYC is tracked in `CUSTOMERS` via the `kyc_status` attribute and that valid KYC levels must be `Level1`, `Level2`, or `Level3`.

So, from the available context, I can say that `Level2` is one of the permitted KYC levels, but its specific business meaning or criteria are not provided.

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_12`, `Customer Master Data→CUSTOMERS`, `parent_chunk_data_dictionary.md_7`, `parent_chunk_data_dictionary.md_4`, `parent_chunk_business_glossary.md_0`, `Customer Master Data`, `parent_chunk_business_glossary.md_1`, `parent_chunk_data_dictionary.md_5`

**Context previews (first 3):**

1. _## Entity Relationship Summary  **Key Relationships: ** - customers ←→ accounts (many-to-many via customer_account) - accounts → accounts (self-reference for parent-child hierarchy) - accounts → trans…_

2. _Business concept 'Customer Master Data' — The table is explicitly described as the core customer dimension and contains identity, contact, KYC, risk, and preferred-flag attributes, which is characteri…_

3. _## accounts  **Description: ** Deposit account master table supporting multiple account types (checking, savings, money market, CD, investment). Implements parent-child hierarchy for portfolio aggrega…_

---

### ✅ 5 — How does the schema support different account subtypes and their varying requirements?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.1891 | **Gate:** `proceed_with_warning`

**Expected answer:**
> The accounts table has an account_subtype column (VARCHAR 30, nullable) that stores values like Premium or Standard to differentiate within each account_type. Combined with the minimum_balance and monthly_fee columns, each account can have different requirements configured per subtype. The account_t…

**System answer:**
> The schema supports subtype variation primarily through the `ACCOUNTS` table, which is the core master record for deposit accounts. It separates broad product category from finer-grained variation by storing both `account_type` and `account_subtype`.

`account_type` captures the main product class and supports values such as Checking, Savings, MoneyMarket, CD, and Investment. `account_subtype` is …

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_7`, `Deposit Account→ACCOUNTS`, `parent_chunk_data_dictionary.md_12`, `parent_chunk_data_dictionary.md_8`, `parent_chunk_data_dictionary.md_9`, `parent_chunk_data_dictionary.md_11`, `parent_chunk_data_dictionary.md_10`, `Deposit Account`

**Context previews (first 3):**

1. _## accounts  **Description: ** Deposit account master table supporting multiple account types (checking, savings, money market, CD, investment). Implements parent-child hierarchy for portfolio aggrega…_

2. _Business concept 'Deposit Account' — This table is the core master record for bank deposit accounts, with account number, type, subtype, balances, interest, fees, status, and lifecycle dates. The desc…_

3. _## Entity Relationship Summary  **Key Relationships: ** - customers ←→ accounts (many-to-many via customer_account) - accounts → accounts (self-reference for parent-child hierarchy) - accounts → trans…_

---

### ✅ 6 — What types of loan products does the bank offer?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.4020 | **Gate:** `proceed`

**Expected answer:**
> The bank offers five loan types defined by the CHECK constraint on loans.loan_type: (1) Mortgage — secured by real estate, glossary example shows $350,000 at 5.50% APR for 360 months; (2) Personal Loan — unsecured, example $15,000 at 8.50% APR for 48 months; (3) Auto Loan — secured by vehicle, examp…

**System answer:**
> The bank’s loan products, as defined in the LOANS table, are Mortgage, Personal, Auto, HELOC, and CreditCard. The table description says the loan portfolio tracks all lending products including mortgages, personal loans, auto loans, HELOCs, and credit cards.

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_10`, `parent_chunk_data_dictionary.md_12`, `physical banking location→BRANCHES`, `parent_chunk_data_dictionary.md_7`, `loan amortization, balances, and maturity dates→LOANS`, `LOANS→CUSTOMERS`, `parent_chunk_business_glossary.md_1`, `parent_chunk_business_glossary.md_2`

**Context previews (first 3):**

1. _## loans  **Description: ** Loan portfolio table tracking all lending products including mortgages, personal loans, auto loans, HELOCs, and credit cards. Records original terms, amortization schedules…_

2. _## Entity Relationship Summary  **Key Relationships: ** - customers ←→ accounts (many-to-many via customer_account) - accounts → accounts (self-reference for parent-child hierarchy) - accounts → trans…_

3. _Business concept 'physical banking location' — A physical banking location where customers can access in-person services including teller transactions, account opening, loan applications, and financia…_

---

### ✅ 7 — What is the daily ATM withdrawal limit for standard customers?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.3743 | **Gate:** `proceed`

**Expected answer:**
> The cards table has an atm_daily_limit column with a default value of $500. The business glossary Card Examples confirm this: a standard Debit Card has a $500 ATM limit, while a Premium Debit card has a $2,000 ATM limit. The daily_limit column (default $3,000) controls POS spending separately. These…

**System answer:**
> The retrieved context does not provide a numeric daily ATM withdrawal limit for standard customers.

What it does show is that the CARDS table stores an `atm_daily_limit` column, so ATM withdrawal limits are tracked at the card level. The ACCOUNTS table also mentions `account_subtype` with examples including `Standard`, but the context does not define any rule that maps a standard customer or stan…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_11`, `Payment card issuance table for debit, credit, and ATM cards→CARDS`, `parent_chunk_data_dictionary.md_6`, `parent_chunk_data_dictionary.md_12`, `parent_chunk_data_dictionary.md_7`, `physical banking location→BRANCHES`, `parent_chunk_business_glossary.md_3`, `parent_chunk_business_glossary.md_1`

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
> In the `ACCOUNTS` hierarchy, a parent account is an account that other accounts roll up to through `ACCOUNTS.PARENT_ACCOUNT_ID -> ACCOUNTS.ACCOUNT_ID`, while a child account is an account whose `parent_account_id` points to another account.

From the context, this hierarchy is used for portfolio aggregation, and the example given is that investment accounts can contain child accounts. So the pract…

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
> The retrieved context shows that the `CARDS` table has a `status` column and that cards track card status, but it does not define the meaning of the specific card status value `Frozen`.

The only explicit definition of `Frozen` in the context is for the business concept `Account`, where account status values include `Active, Dormant, Frozen, Closed`. However, the context does not state that the sa…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_7`, `parent_chunk_data_dictionary.md_10`, `parent_chunk_data_dictionary.md_11`, `parent_chunk_data_dictionary.md_6`, `parent_chunk_data_dictionary.md_9`, `Payment card issuance table for debit, credit, and ATM cards→CARDS`, `parent_chunk_business_glossary.md_0`, `parent_chunk_business_glossary.md_3`

**Context previews (first 3):**

1. _## accounts  **Description: ** Deposit account master table supporting multiple account types (checking, savings, money market, CD, investment). Implements parent-child hierarchy for portfolio aggrega…_

2. _## loans  **Description: ** Loan portfolio table tracking all lending products including mortgages, personal loans, auto loans, HELOCs, and credit cards. Records original terms, amortization schedules…_

3. _## cards  **Description: ** Payment card issuance table for debit, credit, and ATM cards. Links cards to both customer and account. Tracks security features (chip, contactless, PIN), spending limits, …_

---

### ✅ 10 — How does the transactions table track the impact of each transaction on account balances?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.8055 | **Gate:** `proceed`

**Expected answer:**
> The transactions table includes a balance_after column (DECIMAL 15,2) that records the account balance after each transaction is applied. Combined with the amount column, transaction_type (Debit/Credit/Transfer/Payment/Withdrawal/Deposit/Fee), and status (Pending/Posted/Failed/Cancelled/OnHold), thi…

**System answer:**
> The `TRANSACTIONS` table tracks balance impact at the account-activity level by storing each balance-affecting event as a separate row tied to an account through `account_id`, which is a foreign key to `ACCOUNTS.ACCOUNT_ID`.

It records the impact using these fields together:
`transaction_type` identifies the kind of event (`Debit`, `Credit`, `Transfer`, `Payment`, `Withdrawal`, `Deposit`, `Fee`).…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_9`, `TRANSACTIONS→ACCOUNTS`, `Account Activity→TRANSACTIONS`, `parent_chunk_data_dictionary.md_7`, `ACCOUNTS→BRANCHES`, `Deposit Account→ACCOUNTS`, `ACCOUNTS→ACCOUNTS`, `parent_chunk_data_dictionary.md_10`

**Context previews (first 3):**

1. _## transactions  **Description: ** Transaction fact table recording all account activity. Supports multiple transaction types including debits, credits, transfers, and withdrawals. Tracks calculated f…_

2. _Relationship: TRANSACTIONS references ACCOUNTS via foreign key ACCOUNT_ID -> ACCOUNTS.ACCOUNT_ID.…_

3. _Business concept 'Account Activity' — The table is explicitly a transaction fact table and its columns capture balance-affecting events tied to an account, including transaction_type, amount, transact…_

---

### ✅ 11 — How does the customer_account junction table support multiple ownership types?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.9865 | **Gate:** `proceed`

**Expected answer:**
> The customer_account table implements a many-to-many relationship between customers and accounts with a composite primary key (customer_id, account_id). It supports four relationship types via CHECK constraint: Owner, JointOwner, AuthorizedSigner, and Custodian. The is_primary flag designates the pr…

**System answer:**
> The `CUSTOMER_ACCOUNT` junction table supports multiple ownership types by modeling the customer–account link as a many-to-many relationship, so one customer can be tied to multiple accounts and one account can be tied to multiple customers.

It captures the type of relationship in `relationship_type`, with the documented values `Owner`, `JointOwner`, `AuthorizedSigner`, and `Custodian`. This is w…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_8`, `Customer Account Relationship→CUSTOMER_ACCOUNT`, `parent_chunk_data_dictionary.md_12`, `CUSTOMER_ACCOUNT→CUSTOMERS`, `parent_chunk_data_dictionary.md_7`, `CUSTOMER_ACCOUNT→ACCOUNTS`, `parent_chunk_data_dictionary.md_9`, `parent_chunk_data_dictionary.md_11`

**Context previews (first 3):**

1. _## customer_account  **Description: ** Junction table implementing many-to-many relationship between customers and accounts. Supports joint ownership, authorized signers, and custodial relationships. …_

2. _Business concept 'Customer Account Relationship' — The DDL explicitly describes this as a junction table implementing a many-to-many relationship between customers and accounts, with relationship attr…_

3. _## Entity Relationship Summary  **Key Relationships: ** - customers ←→ accounts (many-to-many via customer_account) - accounts → accounts (self-reference for parent-child hierarchy) - accounts → trans…_

---

### ✅ 12 — What is the difference between current_balance and available_balance in the accounts table?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.8328 | **Gate:** `proceed`

**Expected answer:**
> The accounts table tracks two separate balance fields: current_balance includes all transactions including pending ones, while available_balance excludes holds and pending transactions and represents what the customer can actually withdraw. The business glossary confirms this distinction, stating th…

**System answer:**
> The retrieved context shows that `ACCOUNTS` stores both `current_balance` and `available_balance`, and the business glossary treats “Current Balance vs. Available Balance” as an important account attribute. However, it does not give an explicit column-by-column definition of the difference.

From the context, the safest interpretation is that they are distinct balance measures on the same account,…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_7`, `Deposit Account→ACCOUNTS`, `parent_chunk_data_dictionary.md_10`, `Account Activity→TRANSACTIONS`, `parent_chunk_data_dictionary.md_6`, `parent_chunk_data_dictionary.md_9`, `ACCOUNTS→ACCOUNTS`, `ACCOUNTS→BRANCHES`

**Context previews (first 3):**

1. _## accounts  **Description: ** Deposit account master table supporting multiple account types (checking, savings, money market, CD, investment). Implements parent-child hierarchy for portfolio aggrega…_

2. _Business concept 'Deposit Account' — This table is the core master record for bank deposit accounts, with account number, type, subtype, balances, interest, fees, status, and lifecycle dates. The desc…_

3. _## loans  **Description: ** Loan portfolio table tracking all lending products including mortgages, personal loans, auto loans, HELOCs, and credit cards. Records original terms, amortization schedules…_

---

### ✅ 13 — How are loans linked to both customers and accounts in the schema?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.8105 | **Gate:** `proceed`

**Expected answer:**
> The loans table has a customer_id foreign key referencing the customers table (the borrower) and an optional account_id foreign key referencing the accounts table (for linked payment accounts). Each loan belongs to exactly one customer, and can optionally be connected to an account for automatic pay…

**System answer:**
> In the schema, `LOANS` links directly to both `CUSTOMERS` and `ACCOUNTS` through foreign keys in the `loans` table.

`LOANS.customer_id` is a required foreign key to `CUSTOMERS.customer_id`, and the table description identifies this as the borrower link. The relationship metadata also states: `LOANS` references `CUSTOMERS` via `CUSTOMER_ID -> CUSTOMERS.CUSTOMER_ID`. The entity relationship summary…

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
> The system supports these transaction types in `TRANSACTIONS`: Debit, Credit, Transfer, Payment, Withdrawal, Deposit, and Fee. The `transactions` table description also says it records all account activity and supports debits, credits, transfers, and withdrawals, while the `Transaction` business definition and `Account Activity` mapping add the full set above. Related transaction attributes includ…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_9`, `parent_chunk_data_dictionary.md_7`, `Deposit Account→ACCOUNTS`, `physical banking location→BRANCHES`, `Account Activity→TRANSACTIONS`, `parent_chunk_data_dictionary.md_6`, `parent_chunk_data_dictionary.md_11`, `Deposit Account`

**Context previews (first 3):**

1. _## transactions  **Description: ** Transaction fact table recording all account activity. Supports multiple transaction types including debits, credits, transfers, and withdrawals. Tracks calculated f…_

2. _## accounts  **Description: ** Deposit account master table supporting multiple account types (checking, savings, money market, CD, investment). Implements parent-child hierarchy for portfolio aggrega…_

3. _Business concept 'Deposit Account' — This table is the core master record for bank deposit accounts, with account number, type, subtype, balances, interest, fees, status, and lifecycle dates. The desc…_

---

### ✅ 15 — How does the schema support joint account ownership between multiple customers?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.4870 | **Gate:** `proceed`

**Expected answer:**
> Joint ownership is implemented through the customer_account junction table, which creates a many-to-many relationship between customers and accounts. Each row has a relationship_type CHECK constraint allowing Owner, JointOwner, AuthorizedSigner, or Custodian. The ownership_percentage field (DECIMAL …

**System answer:**
> The schema supports joint account ownership through the `CUSTOMER_ACCOUNT` junction table, which implements a many-to-many relationship between `CUSTOMERS` and `ACCOUNTS`. This means one customer can be linked to multiple accounts, and one account can be linked to multiple customers.

`CUSTOMER_ACCOUNT` uses a composite primary key of (`customer_id`, `account_id`) and has foreign keys to `CUSTOMER…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_8`, `parent_chunk_data_dictionary.md_12`, `Customer Account Relationship→CUSTOMER_ACCOUNT`, `parent_chunk_data_dictionary.md_7`, `parent_chunk_data_dictionary.md_11`, `CUSTOMER_ACCOUNT→CUSTOMERS`, `CUSTOMER_ACCOUNT→ACCOUNTS`, `Customer Account Relationship`

**Context previews (first 3):**

1. _## customer_account  **Description: ** Junction table implementing many-to-many relationship between customers and accounts. Supports joint ownership, authorized signers, and custodial relationships. …_

2. _## Entity Relationship Summary  **Key Relationships: ** - customers ←→ accounts (many-to-many via customer_account) - accounts → accounts (self-reference for parent-child hierarchy) - accounts → trans…_

3. _Business concept 'Customer Account Relationship' — The DDL explicitly describes this as a junction table implementing a many-to-many relationship between customers and accounts, with relationship attr…_

---

### ✅ 16 — What information does the cards table track and how are cards linked to customers and accounts?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.9528 | **Gate:** `proceed`

**Expected answer:**
> The cards table links to both accounts (account_id FK) and customers (customer_id FK), tracking card_type (Debit/Credit/ATM), card_network (Visa/Mastercard/Discover/AmericanExpress), card_number, cardholder name, expiration_date, and CVV. For spending controls it stores credit_limit (nullable, for c…

**System answer:**
> The `CARDS` table is the payment card issuance table for debit, credit, and ATM cards. It tracks card issuance and card servicing information including the linked account and cardholder, the card number, card type, card network, card name, expiration date, CVV, credit limit, daily spending limit, ATM daily limit, whether a PIN is set, whether the card has a chip, whether contactless is enabled, ca…

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
> The schema handles interest rates in both deposit and loan products by storing an `interest_rate` column in each product’s core master table, but the surrounding data captured differs by product type.

For deposit products, the business concept “Deposit Account” is implemented by `ACCOUNTS`. That table includes `interest_rate` along with deposit-specific fields such as `current_balance`, `availabl…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_12`, `Deposit Account→ACCOUNTS`, `parent_chunk_data_dictionary.md_10`, `parent_chunk_data_dictionary.md_7`, `loan amortization, balances, and maturity dates→LOANS`, `LOANS→CUSTOMERS`, `LOANS→ACCOUNTS`, `parent_chunk_business_glossary.md_2`

**Context previews (first 3):**

1. _## Entity Relationship Summary  **Key Relationships: ** - customers ←→ accounts (many-to-many via customer_account) - accounts → accounts (self-reference for parent-child hierarchy) - accounts → trans…_

2. _Business concept 'Deposit Account' — This table is the core master record for bank deposit accounts, with account number, type, subtype, balances, interest, fees, status, and lifecycle dates. The desc…_

3. _## loans  **Description: ** Loan portfolio table tracking all lending products including mortgages, personal loans, auto loans, HELOCs, and credit cards. Records original terms, amortization schedules…_

---

### ✅ 18 — What types of branches does the bank operate and how do they differ in capabilities?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.1556 | **Gate:** `proceed_with_warning`

**Expected answer:**
> The branches table supports three types via CHECK constraint: FullService, Satellite, and ATMOnly. The business glossary details each: FullService branches offer complete banking services including loan origination, financial advisors, and safe deposit boxes; Satellite branches have limited hours an…

**System answer:**
> The bank operates three branch types in `BRANCHES.branch_type`: `FullService`, `Satellite`, and `ATMOnly`.

From the context, `BRANCHES` represents physical bank locations, and the related business concept “physical banking location” says these locations support in-person services such as teller transactions, account opening, loan applications, and financial advisory services. The `branches` descr…

**Sources retrieved (12):** `physical banking location→BRANCHES`, `parent_chunk_data_dictionary.md_12`, `parent_chunk_data_dictionary.md_7`, `parent_chunk_data_dictionary.md_6`, `Deposit Account→ACCOUNTS`, `ATMS→BRANCHES`, `parent_chunk_data_dictionary.md_5`, `parent_chunk_business_glossary.md_2`

**Context previews (first 3):**

1. _Business concept 'physical banking location' — A physical banking location where customers can access in-person services including teller transactions, account opening, loan applications, and financia…_

2. _## Entity Relationship Summary  **Key Relationships: ** - customers ←→ accounts (many-to-many via customer_account) - accounts → accounts (self-reference for parent-child hierarchy) - accounts → trans…_

3. _## accounts  **Description: ** Deposit account master table supporting multiple account types (checking, savings, money market, CD, investment). Implements parent-child hierarchy for portfolio aggrega…_

---

### ✅ 19 — How are ATMs related to branches in the schema and what types of ATMs exist?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.6184 | **Gate:** `proceed`

**Expected answer:**
> The atms table has an optional branch_id foreign key referencing branches. When branch_id is NULL, the ATM is standalone and not affiliated with any branch. ATM types are defined by CHECK constraint: Branch (on-premises), DriveThrough (vehicle-accessible), and Standalone (independent locations). Eac…

**System answer:**
> ATMs are related to branches through the `ATMS.branch_id` foreign key, which references `BRANCHES.branch_id`. In the schema, this is a one-to-many relationship from `BRANCHES` to `ATMS`, meaning one branch can have many ATMs. The `branch_id` column in `ATMS` is nullable, and the ATM table description explicitly says it is `NULL for standalone` ATMs. That aligns with the business rule that standalo…

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
> The retrieved context does not define a full end-to-end loan lifecycle from application through completion with explicit stages or status values.

From the context, the covered lifecycle is:

A loan application may be initiated at a branch, because the business concept implemented by BRANCHES says a physical banking location supports “loan applications” and in-person services.

Once a loan exists …

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_10`, `parent_chunk_data_dictionary.md_7`, `Deposit Account→ACCOUNTS`, `loan amortization, balances, and maturity dates→LOANS`, `parent_chunk_data_dictionary.md_12`, `physical banking location→BRANCHES`, `parent_chunk_business_glossary.md_2`, `parent_chunk_business_glossary.md_1`

**Context previews (first 3):**

1. _## loans  **Description: ** Loan portfolio table tracking all lending products including mortgages, personal loans, auto loans, HELOCs, and credit cards. Records original terms, amortization schedules…_

2. _## accounts  **Description: ** Deposit account master table supporting multiple account types (checking, savings, money market, CD, investment). Implements parent-child hierarchy for portfolio aggrega…_

3. _Business concept 'Deposit Account' — This table is the core master record for bank deposit accounts, with account number, type, subtype, balances, interest, fees, status, and lifecycle dates. The desc…_

---

### ✅ 21 — What does preferred customer status mean and how is it tracked in the schema?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.5129 | **Gate:** `proceed`

**Expected answer:**
> Preferred status is tracked via the is_preferred boolean flag in the customers table (default: false). The business glossary states that preferred customers receive waived fees, preferred interest rates, and priority service. The glossary examples show preferred customers with longer tenure and high…

**System answer:**
> Preferred customer status means VIP treatment for a customer. In the schema, this is tracked in the `customers` table, which is the core customer dimension / customer master data table and is described as including “preferred customer flags for VIP treatment.”

Schema-wise, it is stored as the `is_preferred` column on `CUSTOMERS`. This fits the business concept of Customer Master Data because that…

**Sources retrieved (12):** `Customer Master Data→CUSTOMERS`, `parent_chunk_data_dictionary.md_12`, `parent_chunk_data_dictionary.md_11`, `parent_chunk_data_dictionary.md_10`, `parent_chunk_data_dictionary.md_8`, `parent_chunk_data_dictionary.md_7`, `CARDS→CUSTOMERS`, `parent_chunk_data_dictionary.md_4`

**Context previews (first 3):**

1. _Business concept 'Customer Master Data' — The table is explicitly described as the core customer dimension and contains identity, contact, KYC, risk, and preferred-flag attributes, which is characteri…_

2. _## Entity Relationship Summary  **Key Relationships: ** - customers ←→ accounts (many-to-many via customer_account) - accounts → accounts (self-reference for parent-child hierarchy) - accounts → trans…_

3. _## cards  **Description: ** Payment card issuance table for debit, credit, and ATM cards. Links cards to both customer and account. Tracks security features (chip, contactless, PIN), spending limits, …_

---

### ✅ 22 — How does the accounts table support interest tracking and what business rules govern interest?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.3044 | **Gate:** `proceed`

**Expected answer:**
> The accounts table has interest_rate (nullable DECIMAL for the annual rate) and interest_earned (DECIMAL for year-to-date interest credited). The business glossary states that deposit interest is credited monthly (typically the first day of the month) and that APY accounts for compounding effects. P…

**System answer:**
> The `ACCOUNTS` table supports interest tracking directly. Its description says it “tracks balances, interest accrual, fees, and account lifecycle status,” and its columns include `interest_rate` and `interest_earned`. It also includes `current_balance` and `available_balance`, so interest can be stored alongside the account’s balance position, plus `account_type`, `account_subtype`, `status`, `ope…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_7`, `Deposit Account→ACCOUNTS`, `parent_chunk_data_dictionary.md_12`, `parent_chunk_data_dictionary.md_10`, `ACCOUNTS→BRANCHES`, `ACCOUNTS→ACCOUNTS`, `parent_chunk_data_dictionary.md_8`, `parent_chunk_business_glossary.md_2`

**Context previews (first 3):**

1. _## accounts  **Description: ** Deposit account master table supporting multiple account types (checking, savings, money market, CD, investment). Implements parent-child hierarchy for portfolio aggrega…_

2. _Business concept 'Deposit Account' — This table is the core master record for bank deposit accounts, with account number, type, subtype, balances, interest, fees, status, and lifecycle dates. The desc…_

3. _## Entity Relationship Summary  **Key Relationships: ** - customers ←→ accounts (many-to-many via customer_account) - accounts → accounts (self-reference for parent-child hierarchy) - accounts → trans…_

---

### ✅ 23 — Can an account exist without any customer linked to it?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.1394 | **Gate:** `proceed_with_warning`

**Expected answer:**
> Looking at the schema, there is no database-level constraint that forces every account to have a customer_account row. The accounts table has no direct foreign key to customers — the relationship is through the customer_account junction table with a composite primary key (customer_id, account_id). H…

**System answer:**
> Based on the retrieved schema information, yes: the context does not show any rule that every account must have at least one linked customer.

What the context does show is that customer-to-account linkage is handled through the `CUSTOMER_ACCOUNT` junction table, where `account_id` and `customer_id` are both required, and “the `customer_account` junction table requires both customer and account to…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_8`, `Customer Account Relationship→CUSTOMER_ACCOUNT`, `CUSTOMER_ACCOUNT→CUSTOMERS`, `parent_chunk_data_dictionary.md_12`, `CUSTOMER_ACCOUNT→ACCOUNTS`, `parent_chunk_data_dictionary.md_11`, `parent_chunk_data_dictionary.md_10`, `Customer Account Relationship`

**Context previews (first 3):**

1. _## customer_account  **Description: ** Junction table implementing many-to-many relationship between customers and accounts. Supports joint ownership, authorized signers, and custodial relationships. …_

2. _Business concept 'Customer Account Relationship' — The DDL explicitly describes this as a junction table implementing a many-to-many relationship between customers and accounts, with relationship attr…_

3. _Relationship: CUSTOMER_ACCOUNT references CUSTOMERS via foreign key CUSTOMER_ID -> CUSTOMERS.CUSTOMER_ID.…_

---

### ✅ 24 — How does the schema handle failed or cancelled transactions?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.2042 | **Gate:** `proceed`

**Expected answer:**
> The transactions table has a status column with CHECK constraint allowing Pending, Posted, Failed, Cancelled, and OnHold states. The business glossary explains that failed transactions are logged for audit but do not affect the account balance — the balance_after field would reflect no change. Poste…

**System answer:**
> The schema handles failed or cancelled transactions in the `TRANSACTIONS` table by storing a transaction `status` for each account activity record. The business definition of `Transaction` explicitly includes the status values `Pending`, `Posted`, `Failed`, `Cancelled`, and `OnHold`, so failed or cancelled items are represented as transaction rows whose `status` is `Failed` or `Cancelled`.

This i…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_9`, `parent_chunk_data_dictionary.md_12`, `parent_chunk_data_dictionary.md_7`, `TRANSACTIONS→ACCOUNTS`, `Account Activity→TRANSACTIONS`, `parent_chunk_business_glossary.md_1`, `parent_chunk_business_glossary.md_0`, `parent_chunk_business_glossary.md_3`

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
> An ATM can have these operational states in the ATM business concept and ATMS table metadata: Operational, OutOfService, and OutOfCash.

Operational means the ATM is available for customer self-service use. From the context, those services can include basic transactions without teller assistance, and potentially deposit or cardless withdrawal if the specific ATM supports those features through `su…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_6`, `physical banking location→BRANCHES`, `Automated Teller Machine→ATMS`, `ATMS→BRANCHES`, `parent_chunk_data_dictionary.md_12`, `parent_chunk_data_dictionary.md_11`, `parent_chunk_data_dictionary.md_9`, `parent_chunk_business_glossary.md_3`

**Context previews (first 3):**

1. _## atms  **Description: ** ATM locations including branch-attached machines, drive-through ATMs, and standalone units. Tracks cash balances for replenishment scheduling, GPS coordinates for location s…_

2. _Business concept 'physical banking location' — A physical banking location where customers can access in-person services including teller transactions, account opening, loan applications, and financia…_

3. _Business concept 'Automated Teller Machine' is implemented by physical table ATMS (columns: atm_id, atm_code, branch_id, location, latitude, longitude, atm_type, status, cash_balance, last_replenished…_

---

## Anomalies & Observations

No anomalies detected. All questions grounded with acceptable RAGAS scores.
