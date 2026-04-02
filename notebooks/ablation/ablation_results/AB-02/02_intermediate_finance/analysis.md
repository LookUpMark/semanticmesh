# AB-02 — 02_intermediate_finance — Run Analysis

**Timestamp:** 2026-03-30 21:44:09  
**Run tag:** `v5`

## Configuration

| Parameter | Value |
|-----------|-------|
| Extraction model | `LLM (gpt-5.4-nano-2026-03-17)` |
| Reasoning model | `gpt-5.4-2026-03-05` |
| Embedding model | `BAAI/bge-m3` |
| Retrieval mode | `bm25` |
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
| Avg Top Score | 0.4658 |
| Avg Chunk Count | 9.8 |
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
> The retrieved context does not provide a separate definition of a checking account. It does show that “Checking” is one of the possible Account Type values under the business concept Account.

From the glossary, an Account is “a financial arrangement between a customer and the bank that allows deposit, withdrawal, and management of funds.” Accounts are the primary vehicle for customer banking rela…

**Sources retrieved (10):** `parent_chunk_data_dictionary.md_8`, `parent_chunk_business_glossary.md_0`, `Deposit Account`, `parent_chunk_business_glossary.md_1`, `parent_chunk_business_glossary.md_2`, `physical banking location`, `parent_chunk_business_glossary.md_3`, `Account Activity`

**Context previews (first 3):**

1. _## customer_account  **Description: ** Junction table implementing many-to-many relationship between customers and accounts. Supports joint ownership, authorized signers, and custodial relationships. …_

2. _# Retail Banking Business Glossary  This document defines the core business concepts and terminology used in the retail banking domain.  ---  ## Account  **Definition: ** A financial arrangement betwe…_

3. _Deposit Account: This table is the core master record for bank deposit accounts, with account number, type, subtype, balances, interest, fees, status, and lifecycle dates. The description explicitly s…_

---

### ✅ 2 — What is the difference between a savings account and a money market account?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.6601 | **Gate:** `proceed`

**Expected answer:**
> Both savings and money market are account types defined in the accounts table CHECK constraint. The business glossary Interest section provides example rates: Standard Savings earns 0.25% APY (with monthly compounding), Premium Savings earns 0.50% APY (with daily compounding), while Money Market ear…

**System answer:**
> The retrieved context does not define a business difference between a savings account and a money market account.

What it does say is that, in the Account business glossary, both "Savings" and "MoneyMarket" appear as possible Account Type values. The same Account concept includes attributes such as current balance, available balance, interest rate, interest earned, minimum balance requirements, m…

**Sources retrieved (10):** `parent_chunk_data_dictionary.md_8`, `parent_chunk_business_glossary.md_0`, `parent_chunk_business_glossary.md_2`, `parent_chunk_business_glossary.md_1`, `Deposit Account`, `physical banking location`, `Account Activity`, `parent_chunk_business_glossary.md_3`

**Context previews (first 3):**

1. _## customer_account  **Description: ** Junction table implementing many-to-many relationship between customers and accounts. Supports joint ownership, authorized signers, and custodial relationships. …_

2. _# Retail Banking Business Glossary  This document defines the core business concepts and terminology used in the retail banking domain.  ---  ## Account  **Definition: ** A financial arrangement betwe…_

3. _## Interest  **Definition: ** The cost of borrowing money (paid by borrower) or the return on depositing money (paid by bank), expressed as an annual percentage rate. **Business Context:** Interest is…_

---

### ✅ 3 — What is APR versus APY?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.9609 | **Gate:** `proceed`

**Expected answer:**
> APR (Annual Percentage Rate) is the annual cost of a loan including interest and fees, used for loan products. APY (Annual Percentage Yield) is the effective annual rate including compounding effects for deposit products. APY is higher than the nominal rate when compounding is more frequent than ann…

**System answer:**
> In the `Interest` business concept, APR means Annual Percentage Rate and is used for loans, while APY means Annual Percentage Yield and is used for deposits.

The context distinguishes them this way: interest is expressed as an annual percentage rate, APR applies to borrowing, and APY applies to deposit products. It also states that APY accounts for compounding, which makes it specifically relevan…

**Sources retrieved (10):** `parent_chunk_data_dictionary.md_10`, `parent_chunk_business_glossary.md_2`, `parent_chunk_business_glossary.md_0`, `parent_chunk_business_glossary.md_1`, `parent_chunk_data_dictionary.md_11`, `parent_chunk_data_dictionary.md_8`, `Account Activity`, `parent_chunk_data_dictionary.md_5`

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
> The retrieved context does not define what “KYC Level 2” specifically means. It only states that customer master data in `customers` includes KYC compliance information, and that valid KYC levels are constrained to `Level1`, `Level2`, or `Level3`.

So from the available context, the most that can be said is that “KYC Level 2” is one of the allowed KYC levels for a customer record in `customers`, b…

**Sources retrieved (10):** `parent_chunk_data_dictionary.md_12`, `parent_chunk_data_dictionary.md_4`, `parent_chunk_business_glossary.md_0`, `Customer Master Data`, `parent_chunk_business_glossary.md_1`, `parent_chunk_data_dictionary.md_8`, `parent_chunk_data_dictionary.md_10`, `parent_chunk_business_glossary.md_2`

**Context previews (first 3):**

1. _## Entity Relationship Summary  **Key Relationships: ** - customers ←→ accounts (many-to-many via customer_account) - accounts → accounts (self-reference for parent-child hierarchy) - accounts → trans…_

2. _# Retail Banking Data Dictionary  This document provides comprehensive schema documentation for the retail banking database, including table structures, column definitions, constraints, and business c…_

3. _# Retail Banking Business Glossary  This document defines the core business concepts and terminology used in the retail banking domain.  ---  ## Account  **Definition: ** A financial arrangement betwe…_

---

### ✅ 5 — How does the schema support different account subtypes and their varying requirements?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0650 | **Gate:** `proceed_with_warning`

**Expected answer:**
> The accounts table has an account_subtype column (VARCHAR 30, nullable) that stores values like Premium or Standard to differentiate within each account_type. Combined with the minimum_balance and monthly_fee columns, each account can have different requirements configured per subtype. The account_t…

**System answer:**
> The retrieved context shows that different account subtypes are supported within a single core account structure rather than through separate subtype tables.

The key support is the Deposit Account master record, which explicitly includes account number, type, subtype, balances, interest, fees, status, and lifecycle dates. That means subtype is stored as an attribute of the core account record, al…

**Sources retrieved (10):** `parent_chunk_data_dictionary.md_12`, `Deposit Account`, `parent_chunk_business_glossary.md_0`, `parent_chunk_data_dictionary.md_4`, `parent_chunk_business_glossary.md_1`, `parent_chunk_business_glossary.md_2`, `Customer Account Relationship`, `Account Activity`

**Context previews (first 3):**

1. _## Entity Relationship Summary  **Key Relationships: ** - customers ←→ accounts (many-to-many via customer_account) - accounts → accounts (self-reference for parent-child hierarchy) - accounts → trans…_

2. _Deposit Account: This table is the core master record for bank deposit accounts, with account number, type, subtype, balances, interest, fees, status, and lifecycle dates. The description explicitly s…_

3. _# Retail Banking Business Glossary  This document defines the core business concepts and terminology used in the retail banking domain.  ---  ## Account  **Definition: ** A financial arrangement betwe…_

---

### ✅ 6 — What types of loan products does the bank offer?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.4020 | **Gate:** `proceed`

**Expected answer:**
> The bank offers five loan types defined by the CHECK constraint on loans.loan_type: (1) Mortgage — secured by real estate, glossary example shows $350,000 at 5.50% APR for 360 months; (2) Personal Loan — unsecured, example $15,000 at 8.50% APR for 48 months; (3) Auto Loan — secured by vehicle, examp…

**System answer:**
> The bank offers these loan products in the `loans` table: mortgages, personal loans, auto loans, HELOCs, and credit cards. The `loan_type` column enumerates them as `Mortgage`, `Personal`, `Auto`, `HELOC`, and `CreditCard`.

**Sources retrieved (10):** `parent_chunk_data_dictionary.md_10`, `parent_chunk_data_dictionary.md_9`, `parent_chunk_business_glossary.md_1`, `parent_chunk_business_glossary.md_2`, `parent_chunk_business_glossary.md_0`, `physical banking location`, `Deposit Account`, `Customer Master Data`

**Context previews (first 3):**

1. _## loans  **Description: ** Loan portfolio table tracking all lending products including mortgages, personal loans, auto loans, HELOCs, and credit cards. Records original terms, amortization schedules…_

2. _## transactions  **Description: ** Transaction fact table recording all account activity. Supports multiple transaction types including debits, credits, transfers, and withdrawals. Tracks calculated f…_

3. _## Transaction  **Definition: ** Any financial activity that affects the balance of an account, including debits, credits, transfers, withdrawals, and fees. **Business Context:** Transactions represen…_

---

### ✅ 7 — What is the daily ATM withdrawal limit for standard customers?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.3743 | **Gate:** `proceed`

**Expected answer:**
> The cards table has an atm_daily_limit column with a default value of $500. The business glossary Card Examples confirm this: a standard Debit Card has a $500 ATM limit, while a Premium Debit card has a $2,000 ATM limit. The daily_limit column (default $3,000) controls POS spending separately. These…

**System answer:**
> The retrieved context does not specify a numeric daily ATM withdrawal limit for standard customers.

What it does show is that the `cards` table tracks spending limits and links each card to both a customer and an account, so an ATM withdrawal limit would most likely be governed at the card level. The ATM business concept confirms that ATMs support cash withdrawal transactions, and the `Transactio…

**Sources retrieved (10):** `parent_chunk_data_dictionary.md_11`, `parent_chunk_data_dictionary.md_6`, `parent_chunk_data_dictionary.md_7`, `parent_chunk_business_glossary.md_3`, `parent_chunk_business_glossary.md_1`, `parent_chunk_business_glossary.md_2`, `parent_chunk_business_glossary.md_0`, `Payment card issuance table for debit, credit, and ATM cards`

**Context previews (first 3):**

1. _## cards  **Description: ** Payment card issuance table for debit, credit, and ATM cards. Links cards to both customer and account. Tracks security features (chip, contactless, PIN), spending limits, …_

2. _## atms  **Description: ** ATM locations including branch-attached machines, drive-through ATMs, and standalone units. Tracks cash balances for replenishment scheduling, GPS coordinates for location s…_

3. _## accounts  **Description: ** Deposit account master table supporting multiple account types (checking, savings, money market, CD, investment). Implements parent-child hierarchy for portfolio aggrega…_

---

### ✅ 8 — What is the difference between a parent account and a child account?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.3098 | **Gate:** `proceed`

**Expected answer:**
> The accounts table supports parent-child hierarchies through the parent_account_id self-referencing foreign key, with a CHECK constraint preventing circular references (parent_account_id != account_id). The data dictionary describes this as supporting portfolio aggregation where parent accounts (typ…

**System answer:**
> A parent account is the higher-level account in the account hierarchy, used for portfolio aggregation. In the `accounts` table description, this hierarchy is used especially for investment relationships, where investment accounts contain child accounts.

A child account is an account linked under a parent account within that hierarchy. It rolls up into the parent for relationship or portfolio orga…

**Sources retrieved (10):** `parent_chunk_data_dictionary.md_7`, `parent_chunk_business_glossary.md_0`, `parent_chunk_business_glossary.md_1`, `parent_chunk_business_glossary.md_2`, `Account Activity`, `Deposit Account`, `parent_chunk_business_glossary.md_3`, `Customer Account Relationship`

**Context previews (first 3):**

1. _## accounts  **Description: ** Deposit account master table supporting multiple account types (checking, savings, money market, CD, investment). Implements parent-child hierarchy for portfolio aggrega…_

2. _# Retail Banking Business Glossary  This document defines the core business concepts and terminology used in the retail banking domain.  ---  ## Account  **Definition: ** A financial arrangement betwe…_

3. _## Transaction  **Definition: ** Any financial activity that affects the balance of an account, including debits, credits, transfers, withdrawals, and fees. **Business Context:** Transactions represen…_

---

### ✅ 9 — What does the status 'Frozen' mean for a card?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0610 | **Gate:** `proceed_with_warning`

**Expected answer:**
> The cards table has a status column with four states defined by CHECK constraint: Active, Frozen, Blocked, and Expired. The business glossary states that lost or stolen cards must be immediately blocked to prevent fraud, and that expired cards are automatically renewed. The glossary distinguishes Fr…

**System answer:**
> The retrieved context does not define a card status of “Frozen,” and it does not mention a card entity at all.

The only relevant fact in the context is under the business concept Account, where “Account Status” includes “Active, Dormant, Frozen, Closed.” However, the context does not explain what “Frozen” means there.

So, based strictly on the retrieved context: “Frozen” is listed only as an Acc…

**Sources retrieved (10):** `parent_chunk_data_dictionary.md_6`, `parent_chunk_business_glossary.md_0`, `parent_chunk_business_glossary.md_3`, `parent_chunk_business_glossary.md_1`, `parent_chunk_data_dictionary.md_4`, `parent_chunk_business_glossary.md_2`, `Deposit Account`, `Account Activity`

**Context previews (first 3):**

1. _## atms  **Description: ** ATM locations including branch-attached machines, drive-through ATMs, and standalone units. Tracks cash balances for replenishment scheduling, GPS coordinates for location s…_

2. _# Retail Banking Business Glossary  This document defines the core business concepts and terminology used in the retail banking domain.  ---  ## Account  **Definition: ** A financial arrangement betwe…_

3. _## ATM  **Definition: ** Automated Teller Machine - a self-service banking terminal that allows customers to perform basic transactions without teller assistance. **Business Context:** ATMs extend ban…_

---

### ✅ 10 — How does the transactions table track the impact of each transaction on account balances?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.8055 | **Gate:** `proceed`

**Expected answer:**
> The transactions table includes a balance_after column (DECIMAL 15,2) that records the account balance after each transaction is applied. Combined with the amount column, transaction_type (Debit/Credit/Transfer/Payment/Withdrawal/Deposit/Fee), and status (Pending/Posted/Failed/Cancelled/OnHold), thi…

**System answer:**
> The `transactions` table tracks balance impact in two connected ways.

First, it ties every transaction to a specific account through `account_id`, which is a foreign key to `accounts`, so each balance-affecting event is associated with the account it changes.

Second, it stores both the nature of the event and the resulting balance state. The table includes `transaction_type`, with supported valu…

**Sources retrieved (10):** `parent_chunk_data_dictionary.md_9`, `parent_chunk_data_dictionary.md_7`, `Account Activity`, `parent_chunk_business_glossary.md_1`, `Deposit Account`, `parent_chunk_business_glossary.md_0`, `parent_chunk_business_glossary.md_3`, `parent_chunk_business_glossary.md_2`

**Context previews (first 3):**

1. _## transactions  **Description: ** Transaction fact table recording all account activity. Supports multiple transaction types including debits, credits, transfers, and withdrawals. Tracks calculated f…_

2. _## accounts  **Description: ** Deposit account master table supporting multiple account types (checking, savings, money market, CD, investment). Implements parent-child hierarchy for portfolio aggrega…_

3. _Account Activity: The table is explicitly a transaction fact table and its columns capture balance-affecting events tied to an account, including transaction_type, amount, transaction_date, status, an…_

---

### ✅ 11 — How does the customer_account junction table support multiple ownership types?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.9865 | **Gate:** `proceed`

**Expected answer:**
> The customer_account table implements a many-to-many relationship between customers and accounts with a composite primary key (customer_id, account_id). It supports four relationship types via CHECK constraint: Owner, JointOwner, AuthorizedSigner, and Custodian. The is_primary flag designates the pr…

**System answer:**
> The `customer_account` table supports multiple ownership types by acting as the many-to-many junction between `customers` and `accounts`. This means one customer can be linked to multiple accounts, and one account can be linked to multiple customers.

It stores the ownership or access role in `relationship_type`, which can be `Owner`, `JointOwner`, `AuthorizedSigner`, or `Custodian`. That is how t…

**Sources retrieved (9):** `parent_chunk_data_dictionary.md_8`, `parent_chunk_data_dictionary.md_12`, `parent_chunk_data_dictionary.md_9`, `Customer Account Relationship`, `Deposit Account`, `parent_chunk_business_glossary.md_1`, `parent_chunk_business_glossary.md_2`, `Customer Master Data`

**Context previews (first 3):**

1. _## customer_account  **Description: ** Junction table implementing many-to-many relationship between customers and accounts. Supports joint ownership, authorized signers, and custodial relationships. …_

2. _## Entity Relationship Summary  **Key Relationships: ** - customers ←→ accounts (many-to-many via customer_account) - accounts → accounts (self-reference for parent-child hierarchy) - accounts → trans…_

3. _## transactions  **Description: ** Transaction fact table recording all account activity. Supports multiple transaction types including debits, credits, transfers, and withdrawals. Tracks calculated f…_

---

### ✅ 12 — What is the difference between current_balance and available_balance in the accounts table?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.8328 | **Gate:** `proceed`

**Expected answer:**
> The accounts table tracks two separate balance fields: current_balance includes all transactions including pending ones, while available_balance excludes holds and pending transactions and represents what the customer can actually withdraw. The business glossary confirms this distinction, stating th…

**System answer:**
> From the retrieved context, I cannot state a defined difference between `current_balance` and `available_balance`.

What the context does say is that the `accounts` table “tracks balances,” and the Retail Banking Business Glossary lists “Current Balance vs. Available Balance” as key Account attributes. However, the retrieved context does not provide a column-level definition, business rule, or cal…

**Sources retrieved (9):** `parent_chunk_data_dictionary.md_7`, `parent_chunk_data_dictionary.md_8`, `parent_chunk_business_glossary.md_0`, `Account Activity`, `parent_chunk_business_glossary.md_1`, `Deposit Account`, `parent_chunk_business_glossary.md_2`, `Customer Master Data`

**Context previews (first 3):**

1. _## accounts  **Description: ** Deposit account master table supporting multiple account types (checking, savings, money market, CD, investment). Implements parent-child hierarchy for portfolio aggrega…_

2. _## customer_account  **Description: ** Junction table implementing many-to-many relationship between customers and accounts. Supports joint ownership, authorized signers, and custodial relationships. …_

3. _# Retail Banking Business Glossary  This document defines the core business concepts and terminology used in the retail banking domain.  ---  ## Account  **Definition: ** A financial arrangement betwe…_

---

### ✅ 13 — How are loans linked to both customers and accounts in the schema?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.8105 | **Gate:** `proceed`

**Expected answer:**
> The loans table has a customer_id foreign key referencing the customers table (the borrower) and an optional account_id foreign key referencing the accounts table (for linked payment accounts). Each loan belongs to exactly one customer, and can optionally be connected to an account for automatic pay…

**System answer:**
> In the schema, `loans` are linked to customers directly through `loans.customer_id`, which is a non-null foreign key to `customers`. The relationship summary describes this as `customers → loans` in a one-to-many relationship, meaning a customer can have multiple loans, and each loan must belong to a customer.

Loans can also be linked to accounts through `loans.account_id`, which is an optional f…

**Sources retrieved (10):** `parent_chunk_data_dictionary.md_12`, `parent_chunk_data_dictionary.md_10`, `parent_chunk_data_dictionary.md_8`, `parent_chunk_data_dictionary.md_11`, `Customer Account Relationship`, `parent_chunk_business_glossary.md_1`, `parent_chunk_business_glossary.md_0`, `parent_chunk_business_glossary.md_2`

**Context previews (first 3):**

1. _## Entity Relationship Summary  **Key Relationships: ** - customers ←→ accounts (many-to-many via customer_account) - accounts → accounts (self-reference for parent-child hierarchy) - accounts → trans…_

2. _## loans  **Description: ** Loan portfolio table tracking all lending products including mortgages, personal loans, auto loans, HELOCs, and credit cards. Records original terms, amortization schedules…_

3. _## customer_account  **Description: ** Junction table implementing many-to-many relationship between customers and accounts. Supports joint ownership, authorized signers, and custodial relationships. …_

---

### ✅ 14 — What types of transactions does the system support and how does their status lifecycle work?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.3394 | **Gate:** `proceed`

**Expected answer:**
> The transactions table supports seven transaction types via CHECK constraint: Debit, Credit, Transfer, Payment, Withdrawal, Deposit, and Fee. Each transaction also has a status lifecycle with five states: Pending (initial default), Posted (final), Failed, Cancelled, and OnHold. The business glossary…

**System answer:**
> The system supports these transaction types in `transactions.transaction_type`: Debit, Credit, Transfer, Payment, Withdrawal, Deposit, and Fee. The `Transaction` business definition describes these as financial activities that affect an account balance, and it also states the business rules that debit transactions reduce account balance while credit transactions increase account balance. The trans…

**Sources retrieved (10):** `parent_chunk_data_dictionary.md_9`, `parent_chunk_data_dictionary.md_7`, `Deposit Account`, `parent_chunk_business_glossary.md_1`, `parent_chunk_business_glossary.md_3`, `parent_chunk_business_glossary.md_0`, `Account Activity`, `parent_chunk_business_glossary.md_2`

**Context previews (first 3):**

1. _## transactions  **Description: ** Transaction fact table recording all account activity. Supports multiple transaction types including debits, credits, transfers, and withdrawals. Tracks calculated f…_

2. _## accounts  **Description: ** Deposit account master table supporting multiple account types (checking, savings, money market, CD, investment). Implements parent-child hierarchy for portfolio aggrega…_

3. _Deposit Account: This table is the core master record for bank deposit accounts, with account number, type, subtype, balances, interest, fees, status, and lifecycle dates. The description explicitly s…_

---

### ✅ 15 — How does the schema support joint account ownership between multiple customers?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.4869 | **Gate:** `proceed`

**Expected answer:**
> Joint ownership is implemented through the customer_account junction table, which creates a many-to-many relationship between customers and accounts. Each row has a relationship_type CHECK constraint allowing Owner, JointOwner, AuthorizedSigner, or Custodian. The ownership_percentage field (DECIMAL …

**System answer:**
> The schema supports joint account ownership through the `customer_account` table, which is explicitly defined as a junction table between `customers` and `accounts`. The relationship summary states that `customers` and `accounts` are connected in a many-to-many relationship via `customer_account`, which means one customer can be linked to multiple accounts and one account can be linked to multiple…

**Sources retrieved (10):** `parent_chunk_data_dictionary.md_8`, `parent_chunk_data_dictionary.md_12`, `parent_chunk_data_dictionary.md_9`, `Customer Account Relationship`, `parent_chunk_business_glossary.md_0`, `parent_chunk_data_dictionary.md_4`, `parent_chunk_business_glossary.md_2`, `parent_chunk_business_glossary.md_1`

**Context previews (first 3):**

1. _## customer_account  **Description: ** Junction table implementing many-to-many relationship between customers and accounts. Supports joint ownership, authorized signers, and custodial relationships. …_

2. _## Entity Relationship Summary  **Key Relationships: ** - customers ←→ accounts (many-to-many via customer_account) - accounts → accounts (self-reference for parent-child hierarchy) - accounts → trans…_

3. _## transactions  **Description: ** Transaction fact table recording all account activity. Supports multiple transaction types including debits, credits, transfers, and withdrawals. Tracks calculated f…_

---

### ✅ 16 — What information does the cards table track and how are cards linked to customers and accounts?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.9528 | **Gate:** `proceed`

**Expected answer:**
> The cards table links to both accounts (account_id FK) and customers (customer_id FK), tracking card_type (Debit/Credit/ATM), card_network (Visa/Mastercard/Discover/AmericanExpress), card_number, cardholder name, expiration_date, and CVV. For spending controls it stores credit_limit (nullable, for c…

**System answer:**
> The `cards` table is the payment card issuance table for debit, credit, and ATM cards. It tracks card issuance details and includes the cardholder and linked account, along with security and usage information. From the context, it tracks security features such as chip, contactless, and PIN, as well as spending limits and card status. It also supports multiple card networks: Visa, Mastercard, Disco…

**Sources retrieved (9):** `parent_chunk_data_dictionary.md_11`, `parent_chunk_data_dictionary.md_10`, `parent_chunk_data_dictionary.md_12`, `Customer Account Relationship`, `parent_chunk_business_glossary.md_3`, `parent_chunk_business_glossary.md_0`, `parent_chunk_business_glossary.md_1`, `parent_chunk_business_glossary.md_2`

**Context previews (first 3):**

1. _## cards  **Description: ** Payment card issuance table for debit, credit, and ATM cards. Links cards to both customer and account. Tracks security features (chip, contactless, PIN), spending limits, …_

2. _## loans  **Description: ** Loan portfolio table tracking all lending products including mortgages, personal loans, auto loans, HELOCs, and credit cards. Records original terms, amortization schedules…_

3. _## Entity Relationship Summary  **Key Relationships: ** - customers ←→ accounts (many-to-many via customer_account) - accounts → accounts (self-reference for parent-child hierarchy) - accounts → trans…_

---

### ✅ 17 — How does the schema handle interest rates across deposit and loan products?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0574 | **Gate:** `proceed_with_warning`

**Expected answer:**
> Interest rates are stored differently for deposits and loans. The accounts table has an interest_rate column (nullable DECIMAL 5,4) and interest_earned for year-to-date tracking. The loans table has its own interest_rate column representing APR. The business glossary explains that APR (Annual Percen…

**System answer:**
> The schema handles interest differently for deposit products and loan products, but within a common business concept of Interest as an annual rate.

For deposit products, interest is centered on the `accounts` table. The `accounts` table is described as the deposit account master table and explicitly says it tracks balances, interest accrual, fees, and account lifecycle status. The business glossa…

**Sources retrieved (10):** `parent_chunk_data_dictionary.md_12`, `parent_chunk_data_dictionary.md_10`, `parent_chunk_data_dictionary.md_7`, `parent_chunk_business_glossary.md_2`, `parent_chunk_business_glossary.md_0`, `parent_chunk_business_glossary.md_1`, `parent_chunk_data_dictionary.md_4`, `Deposit Account`

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
> The bank operates three branch types in `branches.branch_type`: `FullService`, `Satellite`, and `ATMOnly`.

From the `branches` table, these are described at a high level as full-service branches, satellite offices, and ATM-only locations. The branch data model also tracks operational attributes such as staffing levels, operating hours, ATM counts, and branch status.

However, the retrieved contex…

**Sources retrieved (10):** `parent_chunk_data_dictionary.md_7`, `parent_chunk_data_dictionary.md_9`, `parent_chunk_data_dictionary.md_5`, `parent_chunk_business_glossary.md_2`, `parent_chunk_business_glossary.md_3`, `parent_chunk_business_glossary.md_1`, `parent_chunk_business_glossary.md_0`, `Customer Master Data`

**Context previews (first 3):**

1. _## accounts  **Description: ** Deposit account master table supporting multiple account types (checking, savings, money market, CD, investment). Implements parent-child hierarchy for portfolio aggrega…_

2. _## transactions  **Description: ** Transaction fact table recording all account activity. Supports multiple transaction types including debits, credits, transfers, and withdrawals. Tracks calculated f…_

3. _## branches  **Description: ** Physical bank locations including full-service branches, satellite offices, and ATM-only locations. Tracks staffing levels, operating hours, ATM counts, and branch statu…_

---

### ✅ 19 — How are ATMs related to branches in the schema and what types of ATMs exist?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.5614 | **Gate:** `proceed`

**Expected answer:**
> The atms table has an optional branch_id foreign key referencing branches. When branch_id is NULL, the ATM is standalone and not affiliated with any branch. ATM types are defined by CHECK constraint: Branch (on-premises), DriveThrough (vehicle-accessible), and Standalone (independent locations). Eac…

**System answer:**
> In the schema, ATMs are related to branches as a one-to-many relationship: `branches → atms`. The `atms` table has a `branch_id` column that is a foreign key to `branches`. That means a branch can have multiple ATMs, and an ATM may be associated with a branch. The context also states that `branch_id` is nullable in `atms`, specifically for standalone ATMs, so not every ATM must belong to a branch.…

**Sources retrieved (9):** `parent_chunk_data_dictionary.md_6`, `parent_chunk_data_dictionary.md_12`, `parent_chunk_data_dictionary.md_7`, `parent_chunk_business_glossary.md_3`, `parent_chunk_data_dictionary.md_5`, `parent_chunk_business_glossary.md_2`, `parent_chunk_data_dictionary.md_4`, `parent_chunk_business_glossary.md_1`

**Context previews (first 3):**

1. _## atms  **Description: ** ATM locations including branch-attached machines, drive-through ATMs, and standalone units. Tracks cash balances for replenishment scheduling, GPS coordinates for location s…_

2. _## Entity Relationship Summary  **Key Relationships: ** - customers ←→ accounts (many-to-many via customer_account) - accounts → accounts (self-reference for parent-child hierarchy) - accounts → trans…_

3. _## accounts  **Description: ** Deposit account master table supporting multiple account types (checking, savings, money market, CD, investment). Implements parent-child hierarchy for portfolio aggrega…_

---

### ✅ 20 — What is the lifecycle of a loan from application to completion?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0067 | **Gate:** `proceed_with_warning`

**Expected answer:**
> The loans table tracks loan status through five states defined by CHECK constraint: Pending (application submitted, default), Approved (credit approved but not yet funded), Active (loan funded and being repaid), PaidOff (fully repaid), and Defaulted (borrower failed to repay). Each loan records orig…

**System answer:**
> The retrieved context does not define a full loan lifecycle from application to completion. It does not provide stages such as underwriting, approval, disbursement, payoff, closure, or charge-off, so those cannot be stated.

What the context does show is the servicing-side lifecycle after a loan exists in the portfolio. The `loans` table is described as a loan portfolio table for servicing and por…

**Sources retrieved (10):** `parent_chunk_data_dictionary.md_10`, `parent_chunk_business_glossary.md_2`, `parent_chunk_business_glossary.md_1`, `Deposit Account`, `physical banking location`, `parent_chunk_business_glossary.md_0`, `parent_chunk_business_glossary.md_3`, `Customer Master Data`

**Context previews (first 3):**

1. _## loans  **Description: ** Loan portfolio table tracking all lending products including mortgages, personal loans, auto loans, HELOCs, and credit cards. Records original terms, amortization schedules…_

2. _## Interest  **Definition: ** The cost of borrowing money (paid by borrower) or the return on depositing money (paid by bank), expressed as an annual percentage rate. **Business Context:** Interest is…_

3. _## Transaction  **Definition: ** Any financial activity that affects the balance of an account, including debits, credits, transfers, withdrawals, and fees. **Business Context:** Transactions represen…_

---

### ✅ 21 — What does preferred customer status mean and how is it tracked in the schema?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.5129 | **Gate:** `proceed`

**Expected answer:**
> Preferred status is tracked via the is_preferred boolean flag in the customers table (default: false). The business glossary states that preferred customers receive waived fees, preferred interest rates, and priority service. The glossary examples show preferred customers with longer tenure and high…

**System answer:**
> Preferred customer status means a customer is flagged for VIP treatment. In the retrieved context, this is described in the `customers` table, which is the core customer dimension/master data table and includes “preferred customer flags for VIP treatment.”

So, in the schema, it is tracked at the customer master-data level in `customers`, alongside other customer attributes such as identity, conta…

**Sources retrieved (10):** `parent_chunk_data_dictionary.md_11`, `parent_chunk_data_dictionary.md_4`, `Customer Master Data`, `parent_chunk_business_glossary.md_0`, `parent_chunk_business_glossary.md_1`, `Customer Account Relationship`, `parent_chunk_business_glossary.md_2`, `parent_chunk_business_glossary.md_3`

**Context previews (first 3):**

1. _## cards  **Description: ** Payment card issuance table for debit, credit, and ATM cards. Links cards to both customer and account. Tracks security features (chip, contactless, PIN), spending limits, …_

2. _# Retail Banking Data Dictionary  This document provides comprehensive schema documentation for the retail banking database, including table structures, column definitions, constraints, and business c…_

3. _Customer Master Data: The table is explicitly described as the core customer dimension and contains identity, contact, KYC, risk, and preferred-flag attributes, which is characteristic of customer mas…_

---

### ✅ 22 — How does the accounts table support interest tracking and what business rules govern interest?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.3042 | **Gate:** `proceed`

**Expected answer:**
> The accounts table has interest_rate (nullable DECIMAL for the annual rate) and interest_earned (DECIMAL for year-to-date interest credited). The business glossary states that deposit interest is credited monthly (typically the first day of the month) and that APY accounts for compounding effects. P…

**System answer:**
> The `accounts` table supports interest tracking at the deposit-account master level. Its description says it is the master table for deposit account products such as Checking, Savings, Money Market, CD, and Investment, and that it tracks balances, interest accrual, fees, and account lifecycle status. This aligns with the business concept of `Account`, whose key attributes include interest rate and…

**Sources retrieved (10):** `parent_chunk_data_dictionary.md_7`, `parent_chunk_data_dictionary.md_12`, `parent_chunk_data_dictionary.md_10`, `parent_chunk_business_glossary.md_2`, `Deposit Account`, `parent_chunk_business_glossary.md_0`, `parent_chunk_business_glossary.md_1`, `Account Activity`

**Context previews (first 3):**

1. _## accounts  **Description: ** Deposit account master table supporting multiple account types (checking, savings, money market, CD, investment). Implements parent-child hierarchy for portfolio aggrega…_

2. _## Entity Relationship Summary  **Key Relationships: ** - customers ←→ accounts (many-to-many via customer_account) - accounts → accounts (self-reference for parent-child hierarchy) - accounts → trans…_

3. _## loans  **Description: ** Loan portfolio table tracking all lending products including mortgages, personal loans, auto loans, HELOCs, and credit cards. Records original terms, amortization schedules…_

---

### ✅ 23 — Can an account exist without any customer linked to it?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0876 | **Gate:** `proceed_with_warning`

**Expected answer:**
> Looking at the schema, there is no database-level constraint that forces every account to have a customer_account row. The accounts table has no direct foreign key to customers — the relationship is through the customer_account junction table with a composite primary key (customer_id, account_id). H…

**System answer:**
> The retrieved context does not state whether an `accounts` record can exist without any linked customer.

What it does say is that `customers` and `accounts` are related many-to-many through `customer_account`, and that a `customer_account` row requires both the customer and the account to already exist. That supports only the rule for creating a link in the junction table, not a rule that every a…

**Sources retrieved (10):** `parent_chunk_data_dictionary.md_12`, `parent_chunk_data_dictionary.md_10`, `Customer Account Relationship`, `parent_chunk_business_glossary.md_3`, `parent_chunk_business_glossary.md_0`, `parent_chunk_business_glossary.md_1`, `parent_chunk_business_glossary.md_2`, `Customer Master Data`

**Context previews (first 3):**

1. _## Entity Relationship Summary  **Key Relationships: ** - customers ←→ accounts (many-to-many via customer_account) - accounts → accounts (self-reference for parent-child hierarchy) - accounts → trans…_

2. _## loans  **Description: ** Loan portfolio table tracking all lending products including mortgages, personal loans, auto loans, HELOCs, and credit cards. Records original terms, amortization schedules…_

3. _Customer Account Relationship: The DDL explicitly describes this as a junction table implementing a many-to-many relationship between customers and accounts, with relationship attributes like role, pr…_

---

### ✅ 24 — How does the schema handle failed or cancelled transactions?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.2042 | **Gate:** `proceed`

**Expected answer:**
> The transactions table has a status column with CHECK constraint allowing Pending, Posted, Failed, Cancelled, and OnHold states. The business glossary explains that failed transactions are logged for audit but do not affect the account balance — the balance_after field would reflect no change. Poste…

**System answer:**
> The schema handles failed or cancelled transactions through the transaction/account activity table’s `status` attribute.

From the `Transaction` business concept, transaction status can be `Pending`, `Posted`, `Failed`, `Cancelled`, or `OnHold`. The same context says transactions normally move through operational states such as `Pending → Posted`, which implies that `Failed` and `Cancelled` are re…

**Sources retrieved (10):** `parent_chunk_data_dictionary.md_12`, `parent_chunk_business_glossary.md_1`, `parent_chunk_business_glossary.md_0`, `parent_chunk_business_glossary.md_3`, `parent_chunk_business_glossary.md_2`, `parent_chunk_data_dictionary.md_4`, `Account Activity`, `Customer Master Data`

**Context previews (first 3):**

1. _## Entity Relationship Summary  **Key Relationships: ** - customers ←→ accounts (many-to-many via customer_account) - accounts → accounts (self-reference for parent-child hierarchy) - accounts → trans…_

2. _## Transaction  **Definition: ** Any financial activity that affects the balance of an account, including debits, credits, transfers, withdrawals, and fees. **Business Context:** Transactions represen…_

3. _# Retail Banking Business Glossary  This document defines the core business concepts and terminology used in the retail banking domain.  ---  ## Account  **Definition: ** A financial arrangement betwe…_

---

### ✅ 25 — What operational states can an ATM have and what do they mean for available services?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.4507 | **Gate:** `proceed`

**Expected answer:**
> ATMs have three operational states defined by CHECK constraint: Operational (fully functional for all supported transactions), OutOfService (technical issue preventing all transactions), and OutOfCash (cash depleted, preventing withdrawals). The business glossary explains that cash replenishment is …

**System answer:**
> An ATM can have these status values: `Operational`, `OutOfService`, and `OutOfCash`, as stated in the `ATM` business concept.

The retrieved context also says the `atms` table tracks operational status for availability management. However, it does not explicitly define what services are available or unavailable in each of those states. It does identify supported ATM features such as `Deposit` and …

**Sources retrieved (10):** `parent_chunk_data_dictionary.md_6`, `parent_chunk_data_dictionary.md_12`, `parent_chunk_business_glossary.md_3`, `parent_chunk_data_dictionary.md_5`, `parent_chunk_business_glossary.md_1`, `parent_chunk_business_glossary.md_2`, `physical banking location`, `parent_chunk_business_glossary.md_0`

**Context previews (first 3):**

1. _## atms  **Description: ** ATM locations including branch-attached machines, drive-through ATMs, and standalone units. Tracks cash balances for replenishment scheduling, GPS coordinates for location s…_

2. _## Entity Relationship Summary  **Key Relationships: ** - customers ←→ accounts (many-to-many via customer_account) - accounts → accounts (self-reference for parent-child hierarchy) - accounts → trans…_

3. _## ATM  **Definition: ** Automated Teller Machine - a self-service banking terminal that allows customers to perform basic transactions without teller assistance. **Business Context:** ATMs extend ban…_

---

## Anomalies & Observations

No anomalies detected. All questions grounded with acceptable RAGAS scores.
