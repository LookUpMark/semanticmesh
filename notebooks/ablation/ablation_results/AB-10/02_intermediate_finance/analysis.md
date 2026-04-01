# AB-10 — 02_intermediate_finance — Run Analysis

**Timestamp:** 2026-03-31 22:58:25  
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
| Triplets extracted | 596 |
| Entities resolved | 224 |
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
> The retrieved context does not provide a separate business glossary definition for “checking account.” From the available context, a checking account is one of the supported `account_type` values in the `accounts` table and in the broader `Account` business concept.

Based on that context, it is a type of deposit account within the bank’s account model. The `accounts` table supports multiple accou…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_7`, `parent_chunk_data_dictionary.md_8`, `parent_chunk_data_dictionary.md_9`, `parent_chunk_data_dictionary.md_10`, `Deposit Account→ACCOUNTS`, `parent_chunk_business_glossary.md_0`, `parent_chunk_business_glossary.md_1`, `parent_chunk_business_glossary.md_2`

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

What it does show is that both are supported deposit account types:
The `accounts.account_type` column allows `Checking`, `Savings`, `MoneyMarket`, `CD`, and `Investment`, and the `Account` glossary likewise lists `Checking, Savings, MoneyMarket, CD, Investment` as account types.

So,…

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
> From the Interest concept, APR and APY are both annual percentage measures, but they apply to different banking contexts.

APR, or Annual Percentage Rate, is for loans. It represents the annual percentage rate charged to a borrower as part of the cost of borrowing money.

APY, or Annual Percentage Yield, is for deposits. It represents the return paid on deposited money, and the context specificall…

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
> The retrieved context shows that KYC is tracked in the `CUSTOMERS` table via the `kyc_status` column, and it enforces that valid KYC levels are `Level1`, `Level2`, or `Level3`.

However, the context does not define what `Level2` specifically means, how it differs from `Level1` or `Level3`, or what criteria determine it.

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
> The schema supports account subtypes through the `ACCOUNTS` table, which physically implements the deposit account master record. It has both `account_type` and `account_subtype`, so the model can distinguish broad account categories and then refine them with a subtype. The retrieved context explicitly says `account_type` can be `Checking`, `Savings`, `MoneyMarket`, `CD`, or `Investment`, and `acc…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_7`, `parent_chunk_data_dictionary.md_12`, `Deposit Account→ACCOUNTS`, `parent_chunk_data_dictionary.md_8`, `parent_chunk_data_dictionary.md_9`, `parent_chunk_data_dictionary.md_11`, `Loan portfolio table loan_type (Mortgage/Personal/Auto/HELOC/CreditCard)→LOANS`, `parent_chunk_business_glossary.md_0`

**Context previews (first 3):**

1. _## accounts  **Description: ** Deposit account master table supporting multiple account types (checking, savings, money market, CD, investment). Implements parent-child hierarchy for portfolio aggrega…_

2. _## Entity Relationship Summary  **Key Relationships: ** - customers ←→ accounts (many-to-many via customer_account) - accounts → accounts (self-reference for parent-child hierarchy) - accounts → trans…_

3. _Business concept 'Deposit Account' — The table stores core deposit-account attributes such as account number, type, balances, interest, fees, lifecycle dates, and status, which indicates it physically…_

---

### ✅ 6 — What types of loan products does the bank offer?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.4020 | **Gate:** `proceed`

**Expected answer:**
> The bank offers five loan types defined by the CHECK constraint on loans.loan_type: (1) Mortgage — secured by real estate, glossary example shows $350,000 at 5.50% APR for 360 months; (2) Personal Loan — unsecured, example $15,000 at 8.50% APR for 48 months; (3) Auto Loan — secured by vehicle, examp…

**System answer:**
> The bank offers these loan products, represented by `LOANS.loan_type`: Mortgage, Personal, Auto, HELOC, and CreditCard. The `loans` table description also states the loan portfolio tracks mortgages, personal loans, auto loans, HELOCs, and credit cards.

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_10`, `Loan portfolio table loan_type (Mortgage/Personal/Auto/HELOC/CreditCard)→LOANS`, `parent_chunk_data_dictionary.md_12`, `parent_chunk_data_dictionary.md_7`, `in-person services including teller transactions, account opening, loan applications, and financial advisory services→TRANSACTIONS`, `parent_chunk_business_glossary.md_1`, `Loan portfolio table loan_type (Mortgage/Personal/Auto/HELOC/CreditCard)`, `parent_chunk_business_glossary.md_2`

**Context previews (first 3):**

1. _## loans  **Description: ** Loan portfolio table tracking all lending products including mortgages, personal loans, auto loans, HELOCs, and credit cards. Records original terms, amortization schedules…_

2. _Business concept 'Loan portfolio table loan_type (Mortgage/Personal/Auto/HELOC/CreditCard)' is implemented by physical table LOANS (columns: loan_id, customer_id, loan_type, account_id, principal_amou…_

3. _## Entity Relationship Summary  **Key Relationships: ** - customers ←→ accounts (many-to-many via customer_account) - accounts → accounts (self-reference for parent-child hierarchy) - accounts → trans…_

---

### ✅ 7 — What is the daily ATM withdrawal limit for standard customers?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.3743 | **Gate:** `proceed`

**Expected answer:**
> The cards table has an atm_daily_limit column with a default value of $500. The business glossary Card Examples confirm this: a standard Debit Card has a $500 ATM limit, while a Premium Debit card has a $2,000 ATM limit. The daily_limit column (default $3,000) controls POS spending separately. These…

**System answer:**
> The retrieved context does not provide a numeric daily ATM withdrawal limit for standard customers.

What it does provide is the relevant schema evidence: the CARDS table includes an `atm_daily_limit` column, and the table is described as tracking spending limits for issued debit, credit, and ATM cards. CARDS is linked to both `customer_id` and `account_id`, so ATM withdrawal limits are stored at …

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_11`, `Payment card issuance table for debit, credit, and ATM cards→CARDS`, `parent_chunk_data_dictionary.md_6`, `parent_chunk_data_dictionary.md_12`, `parent_chunk_data_dictionary.md_7`, `Automated Teller Machine→ATMS`, `parent_chunk_data_dictionary.md_8`, `parent_chunk_business_glossary.md_3`

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
> A parent account is an account in the `ACCOUNTS` hierarchy that other accounts roll up to for portfolio aggregation. The context states that the `accounts` table supports a parent-child hierarchy and that investment accounts can contain child accounts. A child account is an account that is linked to another account through `parent_account_id`, which references `ACCOUNTS.ACCOUNT_ID`.

So, the diffe…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_7`, `parent_chunk_data_dictionary.md_12`, `Deposit Account→ACCOUNTS`, `ACCOUNTS→ACCOUNTS`, `parent_chunk_data_dictionary.md_8`, `parent_chunk_data_dictionary.md_9`, `parent_chunk_data_dictionary.md_11`, `parent_chunk_data_dictionary.md_10`

**Context previews (first 3):**

1. _## accounts  **Description: ** Deposit account master table supporting multiple account types (checking, savings, money market, CD, investment). Implements parent-child hierarchy for portfolio aggrega…_

2. _## Entity Relationship Summary  **Key Relationships: ** - customers ←→ accounts (many-to-many via customer_account) - accounts → accounts (self-reference for parent-child hierarchy) - accounts → trans…_

3. _Business concept 'Deposit Account' — The table stores core deposit-account attributes such as account number, type, balances, interest, fees, lifecycle dates, and status, which indicates it physically…_

---

### ✅ 9 — What does the status 'Frozen' mean for a card?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0630 | **Gate:** `proceed_with_warning`

**Expected answer:**
> The cards table has a status column with four states defined by CHECK constraint: Active, Frozen, Blocked, and Expired. The business glossary states that lost or stolen cards must be immediately blocked to prevent fraud, and that expired cards are automatically renewed. The glossary distinguishes Fr…

**System answer:**
> The retrieved context does not define what `Frozen` means for a card.

What the context does show is that the `cards` business concept, implemented by physical table `CARDS`, includes a `status` column and that the table “tracks ... card status.” However, it does not list valid card status values or explain the meaning of any specific card status.

The only place `Frozen` appears in the retrieved …

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
> The `TRANSACTIONS` table tracks balance impact in two connected ways.

First, each row is tied to a specific account through `account_id`, which is a foreign key to `ACCOUNTS.ACCOUNT_ID`. That identifies which account the activity affects.

Second, it stores both the transaction details and the resulting balance state. The key columns are:
`transaction_type`, which indicates whether the activity i…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_9`, `TRANSACTIONS→ACCOUNTS`, `in-person services including teller transactions, account opening, loan applications, and financial advisory services→TRANSACTIONS`, `parent_chunk_data_dictionary.md_7`, `Deposit Account→ACCOUNTS`, `ACCOUNTS→BRANCHES`, `ACCOUNTS→ACCOUNTS`, `parent_chunk_data_dictionary.md_10`

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
> The `customer_account` table supports multiple ownership types by acting as a many-to-many junction between `CUSTOMERS` and `ACCOUNTS`, so a single account can be linked to multiple customers and a single customer can be linked to multiple accounts.

It distinguishes the type of relationship through `relationship_type`, which is defined as `Owner`, `JointOwner`, `AuthorizedSigner`, or `Custodian`.…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_8`, `Customer Account Relationship→CUSTOMER_ACCOUNT`, `parent_chunk_data_dictionary.md_12`, `CUSTOMER_ACCOUNT→CUSTOMERS`, `parent_chunk_data_dictionary.md_7`, `CUSTOMER_ACCOUNT→ACCOUNTS`, `parent_chunk_data_dictionary.md_9`, `Deposit Account→ACCOUNTS`

**Context previews (first 3):**

1. _## customer_account  **Description: ** Junction table implementing many-to-many relationship between customers and accounts. Supports joint ownership, authorized signers, and custodial relationships. …_

2. _Business concept 'Customer Account Relationship' — The DDL explicitly describes this as a junction table implementing a many-to-many relationship between customers and accounts, with relationship-spec…_

3. _## Entity Relationship Summary  **Key Relationships: ** - customers ←→ accounts (many-to-many via customer_account) - accounts → accounts (self-reference for parent-child hierarchy) - accounts → trans…_

---

### ✅ 12 — What is the difference between current_balance and available_balance in the accounts table?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.8328 | **Gate:** `proceed`

**Expected answer:**
> The accounts table tracks two separate balance fields: current_balance includes all transactions including pending ones, while available_balance excludes holds and pending transactions and represents what the customer can actually withdraw. The business glossary confirms this distinction, stating th…

**System answer:**
> The retrieved context shows that the `ACCOUNTS` table stores both `current_balance` and `available_balance` as separate balance attributes for a deposit account, and the business glossary explicitly lists “Current Balance vs. Available Balance” as a key account attribute.

However, the retrieved context does not explicitly define the semantic difference between those two columns. It confirms they …

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_7`, `Deposit Account→ACCOUNTS`, `parent_chunk_data_dictionary.md_10`, `parent_chunk_data_dictionary.md_6`, `parent_chunk_data_dictionary.md_9`, `in-person services including teller transactions, account opening, loan applications, and financial advisory services→TRANSACTIONS`, `ACCOUNTS→ACCOUNTS`, `ACCOUNTS→BRANCHES`

**Context previews (first 3):**

1. _## accounts  **Description: ** Deposit account master table supporting multiple account types (checking, savings, money market, CD, investment). Implements parent-child hierarchy for portfolio aggrega…_

2. _Business concept 'Deposit Account' — The table stores core deposit-account attributes such as account number, type, balances, interest, fees, lifecycle dates, and status, which indicates it physically…_

3. _## loans  **Description: ** Loan portfolio table tracking all lending products including mortgages, personal loans, auto loans, HELOCs, and credit cards. Records original terms, amortization schedules…_

---

### ✅ 13 — How are loans linked to both customers and accounts in the schema?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.8105 | **Gate:** `proceed`

**Expected answer:**
> The loans table has a customer_id foreign key referencing the customers table (the borrower) and an optional account_id foreign key referencing the accounts table (for linked payment accounts). Each loan belongs to exactly one customer, and can optionally be connected to an account for automatic pay…

**System answer:**
> In the schema, `LOANS` links to both `CUSTOMERS` and `ACCOUNTS` through foreign keys on the `loans` table.

`LOANS.customer_id` is a required foreign key to `CUSTOMERS.customer_id`, so every loan must be associated with a borrower in `CUSTOMERS`. This is also reflected in the relationship summary as `customers → loans` being one-to-many.

`LOANS.account_id` is an optional foreign key to `ACCOUNTS.…

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
> The system supports these transaction types in `TRANSACTIONS.transaction_type`: Debit, Credit, Transfer, Payment, Withdrawal, Deposit, and Fee. The `transactions` table is described as recording all account activity and specifically supports debits, credits, transfers, and withdrawals, while the column definition and the `Transaction` business concept expand the full supported set to Debit/Credit/…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_9`, `parent_chunk_data_dictionary.md_7`, `Deposit Account→ACCOUNTS`, `in-person services including teller transactions, account opening, loan applications, and financial advisory services→TRANSACTIONS`, `Automated Teller Machine→ATMS`, `parent_chunk_data_dictionary.md_6`, `Deposit Account`, `parent_chunk_business_glossary.md_1`

**Context previews (first 3):**

1. _## transactions  **Description: ** Transaction fact table recording all account activity. Supports multiple transaction types including debits, credits, transfers, and withdrawals. Tracks calculated f…_

2. _## accounts  **Description: ** Deposit account master table supporting multiple account types (checking, savings, money market, CD, investment). Implements parent-child hierarchy for portfolio aggrega…_

3. _Business concept 'Deposit Account' — The table stores core deposit-account attributes such as account number, type, balances, interest, fees, lifecycle dates, and status, which indicates it physically…_

---

### ✅ 15 — How does the schema support joint account ownership between multiple customers?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.4870 | **Gate:** `proceed`

**Expected answer:**
> Joint ownership is implemented through the customer_account junction table, which creates a many-to-many relationship between customers and accounts. Each row has a relationship_type CHECK constraint allowing Owner, JointOwner, AuthorizedSigner, or Custodian. The ownership_percentage field (DECIMAL …

**System answer:**
> The schema supports joint account ownership through the `customer_account` table, which is explicitly described as a junction table implementing a many-to-many relationship between `customers` and `accounts`. This means one customer can be linked to multiple accounts, and one account can be linked to multiple customers.

At the physical level, `customer_account` uses a composite primary key of (`c…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_8`, `parent_chunk_data_dictionary.md_12`, `Customer Account Relationship→CUSTOMER_ACCOUNT`, `parent_chunk_data_dictionary.md_7`, `parent_chunk_data_dictionary.md_11`, `Deposit Account→ACCOUNTS`, `Customer Account Relationship`, `parent_chunk_business_glossary.md_0`

**Context previews (first 3):**

1. _## customer_account  **Description: ** Junction table implementing many-to-many relationship between customers and accounts. Supports joint ownership, authorized signers, and custodial relationships. …_

2. _## Entity Relationship Summary  **Key Relationships: ** - customers ←→ accounts (many-to-many via customer_account) - accounts → accounts (self-reference for parent-child hierarchy) - accounts → trans…_

3. _Business concept 'Customer Account Relationship' — The DDL explicitly describes this as a junction table implementing a many-to-many relationship between customers and accounts, with relationship-spec…_

---

### ✅ 16 — What information does the cards table track and how are cards linked to customers and accounts?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.9528 | **Gate:** `proceed`

**Expected answer:**
> The cards table links to both accounts (account_id FK) and customers (customer_id FK), tracking card_type (Debit/Credit/ATM), card_network (Visa/Mastercard/Discover/AmericanExpress), card_number, cardholder name, expiration_date, and CVV. For spending controls it stores credit_limit (nullable, for c…

**System answer:**
> The `CARDS` table is the payment card issuance table for debit, credit, and ATM cards. It tracks cards issued to customers and linked accounts, including card identity and product details, security features, limits, lifecycle, and usage timing.

From the context, the table includes these card attributes: `card_id`, `account_id`, `customer_id`, `card_number`, `card_type`, `card_network`, `card_name…

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
> The schema handles interest rates in two different master tables, one for deposit products and one for loan products.

For deposit products, the physical table is ACCOUNTS, which implements the “Deposit Account” concept. It stores both interest_rate and interest_earned, along with balances, fees, and lifecycle dates. This means deposit interest is modeled as part of the account master record, not …

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_12`, `Deposit Account→ACCOUNTS`, `parent_chunk_data_dictionary.md_10`, `parent_chunk_data_dictionary.md_7`, `Loan portfolio table loan_type (Mortgage/Personal/Auto/HELOC/CreditCard)→LOANS`, `LOANS→CUSTOMERS`, `LOANS→ACCOUNTS`, `parent_chunk_business_glossary.md_2`

**Context previews (first 3):**

1. _## Entity Relationship Summary  **Key Relationships: ** - customers ←→ accounts (many-to-many via customer_account) - accounts → accounts (self-reference for parent-child hierarchy) - accounts → trans…_

2. _Business concept 'Deposit Account' — The table stores core deposit-account attributes such as account number, type, balances, interest, fees, lifecycle dates, and status, which indicates it physically…_

3. _## loans  **Description: ** Loan portfolio table tracking all lending products including mortgages, personal loans, auto loans, HELOCs, and credit cards. Records original terms, amortization schedules…_

---

### ✅ 18 — What types of branches does the bank operate and how do they differ in capabilities?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.1556 | **Gate:** `proceed_with_warning`

**Expected answer:**
> The branches table supports three types via CHECK constraint: FullService, Satellite, and ATMOnly. The business glossary details each: FullService branches offer complete banking services including loan origination, financial advisors, and safe deposit boxes; Satellite branches have limited hours an…

**System answer:**
> The bank operates three branch types in `BRANCHES.branch_type`: `FullService`, `Satellite`, and `ATMOnly`.

From the retrieved context, these correspond to physical bank locations described as full-service branches, satellite offices, and ATM-only locations. The `BRANCHES` table tracks operational attributes for these locations, including `hours`, `atm_count`, `teller_count`, `manager_name`, `open…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_12`, `physical banking location→BRANCHES`, `parent_chunk_data_dictionary.md_7`, `parent_chunk_data_dictionary.md_6`, `Deposit Account→ACCOUNTS`, `Automated Teller Machine→ATMS`, `ATMS→BRANCHES`, `parent_chunk_data_dictionary.md_5`

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
> In the schema, ATMs are stored in the `ATMS` table and branches are stored in the `BRANCHES` table. The relationship is `ATMS.branch_id -> BRANCHES.branch_id`, so each ATM can reference a branch through the `branch_id` foreign key. This makes the relationship one-to-many from branches to ATMs: one branch can have many ATMs. The `branch_id` column in `ATMS` is nullable, which means some ATMs are st…

**Sources retrieved (12):** `ATMS→BRANCHES`, `parent_chunk_data_dictionary.md_6`, `parent_chunk_data_dictionary.md_12`, `Automated Teller Machine→ATMS`, `physical banking location→BRANCHES`, `parent_chunk_data_dictionary.md_9`, `parent_chunk_business_glossary.md_3`, `parent_chunk_data_dictionary.md_5`

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
> The retrieved context does not define a full loan lifecycle from application to completion. It only supports a partial view.

It shows that “loan applications” are mentioned as part of the business concept of in-person services, and that concept is mapped to the TRANSACTIONS table. However, the context does not define a specific loan-application workflow, stages, decision process, or transition ru…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_10`, `parent_chunk_data_dictionary.md_7`, `Deposit Account→ACCOUNTS`, `Loan portfolio table loan_type (Mortgage/Personal/Auto/HELOC/CreditCard)→LOANS`, `parent_chunk_data_dictionary.md_12`, `in-person services including teller transactions, account opening, loan applications, and financial advisory services→TRANSACTIONS`, `parent_chunk_business_glossary.md_2`, `parent_chunk_business_glossary.md_1`

**Context previews (first 3):**

1. _## loans  **Description: ** Loan portfolio table tracking all lending products including mortgages, personal loans, auto loans, HELOCs, and credit cards. Records original terms, amortization schedules…_

2. _## accounts  **Description: ** Deposit account master table supporting multiple account types (checking, savings, money market, CD, investment). Implements parent-child hierarchy for portfolio aggrega…_

3. _Business concept 'Deposit Account' — The table stores core deposit-account attributes such as account number, type, balances, interest, fees, lifecycle dates, and status, which indicates it physically…_

---

### ✅ 21 — What does preferred customer status mean and how is it tracked in the schema?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.5129 | **Gate:** `proceed`

**Expected answer:**
> Preferred status is tracked via the is_preferred boolean flag in the customers table (default: false). The business glossary states that preferred customers receive waived fees, preferred interest rates, and priority service. The glossary examples show preferred customers with longer tenure and high…

**System answer:**
> Preferred customer status means a customer is flagged for VIP treatment. The retrieved context states that the `customers` table “includes KYC compliance status, risk profiling for investment suitability, and preferred customer flags for VIP treatment.”

In the schema, this is tracked in the `CUSTOMERS` table, which is the core customer dimension/master data table for all individual and corporate …

**Sources retrieved (12):** `Core customer dimension table containing master data for all individual and corporate banking customers→CUSTOMERS`, `parent_chunk_data_dictionary.md_12`, `parent_chunk_data_dictionary.md_11`, `parent_chunk_data_dictionary.md_10`, `parent_chunk_data_dictionary.md_8`, `parent_chunk_data_dictionary.md_7`, `CARDS→CUSTOMERS`, `parent_chunk_data_dictionary.md_6`

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
> The `ACCOUNTS` table supports interest tracking by storing both the rate and the accumulated interest on each deposit account. In the physical table `ACCOUNTS`, the relevant columns are `interest_rate` and `interest_earned`, and the table description explicitly says it tracks “interest accrual.” The broader deposit-account implementation also includes `current_balance` and `available_balance`, whi…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_7`, `Deposit Account→ACCOUNTS`, `parent_chunk_data_dictionary.md_12`, `parent_chunk_data_dictionary.md_10`, `ACCOUNTS→BRANCHES`, `ACCOUNTS→ACCOUNTS`, `parent_chunk_data_dictionary.md_8`, `CARDS→ACCOUNTS`

**Context previews (first 3):**

1. _## accounts  **Description: ** Deposit account master table supporting multiple account types (checking, savings, money market, CD, investment). Implements parent-child hierarchy for portfolio aggrega…_

2. _Business concept 'Deposit Account' — The table stores core deposit-account attributes such as account number, type, balances, interest, fees, lifecycle dates, and status, which indicates it physically…_

3. _## Entity Relationship Summary  **Key Relationships: ** - customers ←→ accounts (many-to-many via customer_account) - accounts → accounts (self-reference for parent-child hierarchy) - accounts → trans…_

---

### ✅ 23 — Can an account exist without any customer linked to it?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.1394 | **Gate:** `proceed_with_warning`

**Expected answer:**
> Looking at the schema, there is no database-level constraint that forces every account to have a customer_account row. The accounts table has no direct foreign key to customers — the relationship is through the customer_account junction table with a composite primary key (customer_id, account_id). H…

**System answer:**
> The retrieved context does not establish whether every `ACCOUNTS` row must have at least one linked `CUSTOMER_ACCOUNT` row.

What it does say is that `CUSTOMER_ACCOUNT` is the junction table for the many-to-many relationship between customers and accounts, and that each `CUSTOMER_ACCOUNT` row requires both a valid customer and a valid account because `customer_id` and `account_id` are non-null for…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_8`, `CUSTOMER_ACCOUNT→CUSTOMERS`, `parent_chunk_data_dictionary.md_12`, `Customer Account Relationship→CUSTOMER_ACCOUNT`, `CUSTOMER_ACCOUNT→ACCOUNTS`, `parent_chunk_data_dictionary.md_11`, `parent_chunk_data_dictionary.md_10`, `Deposit Account→ACCOUNTS`

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
> The schema handles failed or cancelled transactions in the `TRANSACTIONS` table by storing a transaction `status`. The retrieved context explicitly says the `Transaction` business concept supports these states: `Pending`, `Posted`, `Failed`, `Cancelled`, and `OnHold`, and that transactions flow through lifecycle states such as `Pending → Posted`.

So, a failed or cancelled transaction is represent…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_9`, `parent_chunk_data_dictionary.md_12`, `parent_chunk_data_dictionary.md_7`, `TRANSACTIONS→ACCOUNTS`, `in-person services including teller transactions, account opening, loan applications, and financial advisory services→TRANSACTIONS`, `parent_chunk_business_glossary.md_1`, `parent_chunk_business_glossary.md_0`, `parent_chunk_business_glossary.md_3`

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
> An ATM can have these status values in the context: Operational, OutOfService, and OutOfCash. This is shown in the ATM business concept and the ATMS table metadata, where status is tracked for availability management.

The same context also says ATMs may support features such as Deposit and Cardless Withdrawal, represented in ATMS by supports_deposit and supports_cardless.

However, the retrieved …

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_6`, `Automated Teller Machine→ATMS`, `ATMS→BRANCHES`, `parent_chunk_data_dictionary.md_12`, `parent_chunk_data_dictionary.md_11`, `physical banking location→BRANCHES`, `parent_chunk_data_dictionary.md_9`, `parent_chunk_business_glossary.md_3`

**Context previews (first 3):**

1. _## atms  **Description: ** ATM locations including branch-attached machines, drive-through ATMs, and standalone units. Tracks cash balances for replenishment scheduling, GPS coordinates for location s…_

2. _Business concept 'Automated Teller Machine' — a self-service banking terminal that allows customers to perform basic transactions without teller assistance. is implemented by physical table ATMS (colu…_

3. _Relationship: ATMS references BRANCHES via foreign key BRANCH_ID -> BRANCHES.BRANCH_ID.…_

---

## Anomalies & Observations

No anomalies detected. All questions grounded with acceptable RAGAS scores.
