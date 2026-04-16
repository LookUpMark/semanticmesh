# AB-BEST-OPENROUTER — 02_intermediate_finance — Run Analysis

**Timestamp:** 2026-04-15 17:12:58  
**Run tag:** `ds02-20260415`

## Configuration

| Parameter | Value |
|-----------|-------|
| Extraction model | `LLM (openai/gpt-4.1-nano)` |
| Reasoning model | `openai/gpt-oss-120b` |
| Embedding model | `BAAI/bge-m3` |
| Retrieval mode | `hybrid` |
| Reranker | `True` |
| Reranker top_k | `12` |
| Chunk size / overlap | `256 / 32` |
| ER similarity threshold | `0.75` |

## Builder Results

| Metric | Value |
|--------|-------|
| Triplets extracted | 155 |
| Entities resolved | 138 |
| Tables parsed | 8 |
| Tables completed | 8 |

## Query Evaluation Summary

| Metric | Value |
|--------|-------|
| Questions | 25 |
| Grounded | **25/25 (100%)** |
| Avg GT Coverage | 100% |
| Avg Top Score | 0.4798 |
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
> A **checking account** is one of the account types defined in the retail‑banking data model. It is a deposit‑account record stored in the **ACCOUNTS** table (see chunk [1] and the concept mapping in chunk [3]) where the column **account_type** has the value “Checking”.  

In the business glossary (chunk [7]), an **Account** is described as “a financial arrangement between a customer and the bank t…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_7`, `parent_chunk_data_dictionary.md_8`, `Account→ACCOUNTS`, `Branch→BRANCHES`, `parent_chunk_data_dictionary.md_9`, `parent_chunk_data_dictionary.md_10`, `parent_chunk_business_glossary.md_0`, `Account`

**Context previews (first 3):**

1. _## accounts  **Description: ** Deposit account master table supporting multiple account types (checking, savings, money market, CD, investment). Implements parent-child hierarchy for portfolio aggrega…_

2. _## customer_account  **Description: ** Junction table implementing many-to-many relationship between customers and accounts. Supports joint ownership, authorized signers, and custodial relationships. …_

3. _Business concept 'Account' — This table stores information about bank accounts, including account details, balances, interest, and status history. is implemented by physical table ACCOUNTS (columns: a…_

---

### ✅ 2 — What is the difference between a savings account and a money market account?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.6601 | **Gate:** `proceed`

**Expected answer:**
> Both savings and money market are account types defined in the accounts table CHECK constraint. The business glossary Interest section provides example rates: Standard Savings earns 0.25% APY (with monthly compounding), Premium Savings earns 0.50% APY (with daily compounding), while Money Market ear…

**System answer:**
> The schema defines **account_type** as a column in the **accounts** table that can hold values such as **“Savings”** and **“MoneyMarket.”** Both are listed as separate deposit‑account types (along with Checking, CD, Investment, etc.). The retrieved material does not provide any further attributes or business‑rule details that distinguish a savings account from a money‑market account, so the only c…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_7`, `parent_chunk_data_dictionary.md_10`, `parent_chunk_data_dictionary.md_9`, `parent_chunk_data_dictionary.md_8`, `parent_chunk_data_dictionary.md_12`, `parent_chunk_data_dictionary.md_11`, `Account→ACCOUNTS`, `parent_chunk_business_glossary.md_0`

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
> **APR (Annual Percentage Rate)** – the interest rate that is quoted for **loans**. It represents the cost of borrowing money on an annual basis.

**APY (Annual Percentage Yield)** – the interest rate that is quoted for **deposits**. It reflects the total return a depositor earns in a year, taking into account any compounding of interest.

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
> The retrieved metadata defines KYC (Know‑Your‑Customer) compliance levels as a controlled set of values:

- **Allowed KYC levels:** Level1, **Level2**, Level3  

Thus, **KYC Level 2** is one of the three permitted KYC status values for a customer (the others being Level1 and Level3). The context does not provide a further description of what distinguishes Level 2 from the other levels.

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_12`, `Core Customer Dimension→CUSTOMERS`, `parent_chunk_data_dictionary.md_7`, `parent_chunk_data_dictionary.md_4`, `parent_chunk_business_glossary.md_0`, `parent_chunk_business_glossary.md_1`, `parent_chunk_data_dictionary.md_5`, `parent_chunk_data_dictionary.md_8`

**Context previews (first 3):**

1. _## Entity Relationship Summary  **Key Relationships: ** - customers ←→ accounts (many-to-many via customer_account) - accounts → accounts (self-reference for parent-child hierarchy) - accounts → trans…_

2. _Business concept 'Core Customer Dimension' — Core customer dimension table containing master data for all individual and corporate banking customers. is implemented by physical table CUSTOMERS (column…_

3. _## accounts  **Description: ** Deposit account master table supporting multiple account types (checking, savings, money market, CD, investment). Implements parent-child hierarchy for portfolio aggrega…_

---

### ✅ 5 — How does the schema support different account subtypes and their varying requirements?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.1891 | **Gate:** `proceed_with_warning`

**Expected answer:**
> The accounts table has an account_subtype column (VARCHAR 30, nullable) that stores values like Premium or Standard to differentiate within each account_type. Combined with the minimum_balance and monthly_fee columns, each account can have different requirements configured per subtype. The account_t…

**System answer:**
> The schema captures account sub‑types directly in the **ACCOUNTS** table and provides the fields needed to store the different data and rules that each sub‑type may require.

* **Account‑type and sub‑type columns** – `account_type` (Checking, Savings, MoneyMarket, CD, Investment) identifies the broad product family, while `account_subtype` (e.g., Premium, Student, Standard) records the more specif…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_7`, `parent_chunk_data_dictionary.md_12`, `Account→ACCOUNTS`, `parent_chunk_data_dictionary.md_8`, `parent_chunk_data_dictionary.md_9`, `parent_chunk_data_dictionary.md_11`, `parent_chunk_data_dictionary.md_10`, `Linked Account And Customer→CUSTOMER_ACCOUNT`

**Context previews (first 3):**

1. _## accounts  **Description: ** Deposit account master table supporting multiple account types (checking, savings, money market, CD, investment). Implements parent-child hierarchy for portfolio aggrega…_

2. _## Entity Relationship Summary  **Key Relationships: ** - customers ←→ accounts (many-to-many via customer_account) - accounts → accounts (self-reference for parent-child hierarchy) - accounts → trans…_

3. _Business concept 'Account' — This table stores information about bank accounts, including account details, balances, interest, and status history. is implemented by physical table ACCOUNTS (columns: a…_

---

### ✅ 6 — What types of loan products does the bank offer?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.4020 | **Gate:** `proceed`

**Expected answer:**
> The bank offers five loan types defined by the CHECK constraint on loans.loan_type: (1) Mortgage — secured by real estate, glossary example shows $350,000 at 5.50% APR for 360 months; (2) Personal Loan — unsecured, example $15,000 at 8.50% APR for 48 months; (3) Auto Loan — secured by vehicle, examp…

**System answer:**
> The bank’s loan portfolio includes the following product types, as defined by the **loan_type** column in the LOANS table:

- Mortgage  
- Personal  
- Auto  
- HELOC (Home Equity Line of Credit)  
- Credit Card  

These are the loan product categories recorded in the loan table’s schema.

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_10`, `parent_chunk_data_dictionary.md_12`, `Branch→BRANCHES`, `parent_chunk_data_dictionary.md_7`, `Loan→LOANS`, `parent_chunk_business_glossary.md_1`, `parent_chunk_business_glossary.md_2`, `parent_chunk_business_glossary.md_0`

**Context previews (first 3):**

1. _## loans  **Description: ** Loan portfolio table tracking all lending products including mortgages, personal loans, auto loans, HELOCs, and credit cards. Records original terms, amortization schedules…_

2. _## Entity Relationship Summary  **Key Relationships: ** - customers ←→ accounts (many-to-many via customer_account) - accounts → accounts (self-reference for parent-child hierarchy) - accounts → trans…_

3. _Business concept 'Branch' — A physical banking location where customers can access in‑person services such as teller transactions, account opening, loan applications, and financial advisory services. …_

---

### ✅ 7 — What is the daily ATM withdrawal limit for standard customers?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.3743 | **Gate:** `proceed`

**Expected answer:**
> The cards table has an atm_daily_limit column with a default value of $500. The business glossary Card Examples confirm this: a standard Debit Card has a $500 ATM limit, while a Premium Debit card has a $2,000 ATM limit. The daily_limit column (default $3,000) controls POS spending separately. These…

**System answer:**
> The retrieved knowledge graph defines a **`cards`** table that includes an **`atm_daily_limit`** column (see the “Business concept ‘Card Number Pan’” mapping). This column is intended to store the daily ATM‑withdrawal limit that applies to each issued card.

However, the context does **not** contain:

* a business rule that sets a specific numeric limit for “standard customers,” nor
* any default …

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_11`, `Card Number Pan→CARDS`, `parent_chunk_data_dictionary.md_6`, `parent_chunk_data_dictionary.md_12`, `parent_chunk_data_dictionary.md_7`, `Automated Teller Machine→ATMS`, `Branch→BRANCHES`, `parent_chunk_business_glossary.md_3`

**Context previews (first 3):**

1. _## cards  **Description: ** Payment card issuance table for debit, credit, and ATM cards. Links cards to both customer and account. Tracks security features (chip, contactless, PIN), spending limits, …_

2. _Business concept 'Card Number Pan' — Key Attributes: - Card ID and Card Number (PAN) is implemented by physical table CARDS (columns: card_id, account_id, customer_id, card_number, card_type, card_net…_

3. _## atms  **Description: ** ATM locations including branch-attached machines, drive-through ATMs, and standalone units. Tracks cash balances for replenishment scheduling, GPS coordinates for location s…_

---

### ✅ 8 — What is the difference between a parent account and a child account?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.3098 | **Gate:** `proceed`

**Expected answer:**
> The accounts table supports parent-child hierarchies through the parent_account_id self-referencing foreign key, with a CHECK constraint preventing circular references (parent_account_id != account_id). The data dictionary describes this as supporting portfolio aggregation where parent accounts (typ…

**System answer:**
> **Parent account** – an account that can be the target of the self‑referencing foreign key **PARENT_ACCOUNT_ID** (see [3]). In other words, other rows in the **ACCOUNTS** table may point to its **ACCOUNT_ID** as their parent, allowing the account to act as a container for a portfolio of related accounts (as described in the table description [1] and the entity‑relationship summary [2]).

**Child a…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_7`, `parent_chunk_data_dictionary.md_12`, `ACCOUNTS→ACCOUNTS`, `Account→ACCOUNTS`, `parent_chunk_data_dictionary.md_8`, `parent_chunk_data_dictionary.md_9`, `parent_chunk_data_dictionary.md_11`, `parent_chunk_data_dictionary.md_10`

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
> The schema includes a **status** column for the **CARDS** table (see the “Card Number Pan” concept mapping, which lists `status` among the card attributes). This tells us that each card record can have a status value such as “Active”, “Closed”, etc.

However, the retrieved documentation does **not** provide a definition of what the status value **“Frozen”** specifically means for a card. The only …

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_7`, `parent_chunk_data_dictionary.md_10`, `parent_chunk_data_dictionary.md_11`, `parent_chunk_data_dictionary.md_6`, `parent_chunk_data_dictionary.md_9`, `Card Number Pan→CARDS`, `parent_chunk_business_glossary.md_0`, `parent_chunk_business_glossary.md_3`

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
> The **TRANSACTIONS** fact table records the effect of each posting on the related account by:

1. **Linking the transaction to an account** – the column `account_id` is a foreign key that points to the primary key `account_id` in the **ACCOUNTS** table, so every row is tied to the specific account whose balance is affected.

2. **Storing the post‑transaction balance** – the column `balance_after` …

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_9`, `TRANSACTIONS→ACCOUNTS`, `parent_chunk_data_dictionary.md_7`, `Operational Heartbeat Of→TRANSACTIONS`, `Account→ACCOUNTS`, `ACCOUNTS→BRANCHES`, `ACCOUNTS→ACCOUNTS`, `parent_chunk_data_dictionary.md_10`

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
> The **customer_account** junction table is designed to capture any kind of link a customer can have to an account. It does this through several dedicated columns:

* **relationship_type** – a `VARCHAR(20)` field that records the nature of the link. The allowed values listed in the schema are **Owner**, **JointOwner**, **AuthorizedSigner**, and **Custodian**, so the same table can represent sole ow…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_8`, `parent_chunk_data_dictionary.md_12`, `Linked Account And Customer→CUSTOMER_ACCOUNT`, `CUSTOMER_ACCOUNT→CUSTOMERS`, `parent_chunk_data_dictionary.md_7`, `CUSTOMER_ACCOUNT→ACCOUNTS`, `parent_chunk_data_dictionary.md_9`, `parent_chunk_data_dictionary.md_11`

**Context previews (first 3):**

1. _## customer_account  **Description: ** Junction table implementing many-to-many relationship between customers and accounts. Supports joint ownership, authorized signers, and custodial relationships. …_

2. _## Entity Relationship Summary  **Key Relationships: ** - customers ←→ accounts (many-to-many via customer_account) - accounts → accounts (self-reference for parent-child hierarchy) - accounts → trans…_

3. _Business concept 'Linked Account And Customer' — Key Attributes: - Linked Account and Customer is implemented by physical table CUSTOMER_ACCOUNT (columns: customer_id, account_id, relationship_type, i…_

---

### ✅ 12 — What is the difference between current_balance and available_balance in the accounts table?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.8328 | **Gate:** `proceed`

**Expected answer:**
> The accounts table tracks two separate balance fields: current_balance includes all transactions including pending ones, while available_balance excludes holds and pending transactions and represents what the customer can actually withdraw. The business glossary confirms this distinction, stating th…

**System answer:**
> The **ACCOUNTS** table (see the Business Concept “Account” in the retrieved context) contains two separate balance columns:

* **current_balance** – the total amount of money recorded in the account.  
* **available_balance** – the portion of that total that is actually usable for transactions (i.e., the balance after accounting for holds, pending debits, or other restrictions).

The retail‑bankin…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_7`, `Account→ACCOUNTS`, `parent_chunk_data_dictionary.md_10`, `Loan→LOANS`, `parent_chunk_data_dictionary.md_6`, `parent_chunk_data_dictionary.md_9`, `ACCOUNTS→ACCOUNTS`, `ACCOUNTS→BRANCHES`

**Context previews (first 3):**

1. _## accounts  **Description: ** Deposit account master table supporting multiple account types (checking, savings, money market, CD, investment). Implements parent-child hierarchy for portfolio aggrega…_

2. _Business concept 'Account' — This table stores information about bank accounts, including account details, balances, interest, and status history. is implemented by physical table ACCOUNTS (columns: a…_

3. _## loans  **Description: ** Loan portfolio table tracking all lending products including mortgages, personal loans, auto loans, HELOCs, and credit cards. Records original terms, amortization schedules…_

---

### ✅ 13 — How are loans linked to both customers and accounts in the schema?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.8105 | **Gate:** `proceed`

**Expected answer:**
> The loans table has a customer_id foreign key referencing the customers table (the borrower) and an optional account_id foreign key referencing the accounts table (for linked payment accounts). Each loan belongs to exactly one customer, and can optionally be connected to an account for automatic pay…

**System answer:**
> In the retail‑banking schema the **LOANS** table contains two foreign‑key columns that connect a loan record to the other master entities:

* **customer_id** – a non‑nullable column that references **CUSTOMERS.CUSTOMER_ID** (see the FK relationship in chunk [2] and the column list in chunk [5]). This creates a one‑to‑many link: each loan is tied to a single borrower, while a customer can have many…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_12`, `LOANS→CUSTOMERS`, `LOANS→ACCOUNTS`, `Linked Account And Customer→CUSTOMER_ACCOUNT`, `parent_chunk_data_dictionary.md_10`, `CUSTOMER_ACCOUNT→CUSTOMERS`, `parent_chunk_data_dictionary.md_8`, `CUSTOMER_ACCOUNT→ACCOUNTS`

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
> The **transactions** fact table defines the kinds of activity the system records and the column that holds each transaction’s current state.

**Supported transaction types** (from the `transaction_type` column description in the *transactions* table)  
- Debit  
- Credit  
- Transfer  
- Payment  
- Withdrawal  
- Deposit  
- Fee  

**Status lifecycle** (from the transaction business definition)  …

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_9`, `parent_chunk_data_dictionary.md_7`, `Automated Teller Machine→ATMS`, `Operational Heartbeat Of→TRANSACTIONS`, `Branch→BRANCHES`, `parent_chunk_data_dictionary.md_6`, `parent_chunk_data_dictionary.md_11`, `parent_chunk_data_dictionary.md_12`

**Context previews (first 3):**

1. _## transactions  **Description: ** Transaction fact table recording all account activity. Supports multiple transaction types including debits, credits, transfers, and withdrawals. Tracks calculated f…_

2. _## accounts  **Description: ** Deposit account master table supporting multiple account types (checking, savings, money market, CD, investment). Implements parent-child hierarchy for portfolio aggrega…_

3. _Business concept 'Automated Teller Machine' — Automated Teller Machine - a self-service banking terminal that allows customers to perform basic transactions without teller assistance. is implemented b…_

---

### ✅ 15 — How does the schema support joint account ownership between multiple customers?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.4870 | **Gate:** `proceed`

**Expected answer:**
> Joint ownership is implemented through the customer_account junction table, which creates a many-to-many relationship between customers and accounts. Each row has a relationship_type CHECK constraint allowing Owner, JointOwner, AuthorizedSigner, or Custodian. The ownership_percentage field (DECIMAL …

**System answer:**
> The schema models joint ownership through the **CUSTOMER_ACCOUNT** junction table. This table creates a many‑to‑many link between **CUSTOMERS** and **ACCOUNTS** (Entity Relationship Summary) and its primary key is the composite (`customer_id`, `account_id`). Each row records a specific relationship between a customer and an account, and the column **relationship_type** can hold values such as Owne…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_8`, `parent_chunk_data_dictionary.md_12`, `Linked Account And Customer→CUSTOMER_ACCOUNT`, `parent_chunk_data_dictionary.md_7`, `parent_chunk_data_dictionary.md_11`, `CUSTOMER_ACCOUNT→CUSTOMERS`, `CUSTOMER_ACCOUNT→ACCOUNTS`, `parent_chunk_business_glossary.md_0`

**Context previews (first 3):**

1. _## customer_account  **Description: ** Junction table implementing many-to-many relationship between customers and accounts. Supports joint ownership, authorized signers, and custodial relationships. …_

2. _## Entity Relationship Summary  **Key Relationships: ** - customers ←→ accounts (many-to-many via customer_account) - accounts → accounts (self-reference for parent-child hierarchy) - accounts → trans…_

3. _Business concept 'Linked Account And Customer' — Key Attributes: - Linked Account and Customer is implemented by physical table CUSTOMER_ACCOUNT (columns: customer_id, account_id, relationship_type, i…_

---

### ✅ 16 — What information does the cards table track and how are cards linked to customers and accounts?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.9528 | **Gate:** `proceed`

**Expected answer:**
> The cards table links to both accounts (account_id FK) and customers (customer_id FK), tracking card_type (Debit/Credit/ATM), card_network (Visa/Mastercard/Discover/AmericanExpress), card_number, cardholder name, expiration_date, and CVV. For spending controls it stores credit_limit (nullable, for c…

**System answer:**
> The **cards** table is the issuance record for debit, credit and ATM cards. According to its description it **tracks**:

* security‑feature information – whether the card has a chip, contactless capability and a PIN,  
* spending‑limit information, and  
* the card’s status (e.g., active, suspended).

It also records the card’s primary account number, the type of card (debit, credit, ATM) and the …

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_11`, `CARDS→CUSTOMERS`, `CARDS→ACCOUNTS`, `parent_chunk_data_dictionary.md_10`, `Linked Account And Customer→CUSTOMER_ACCOUNT`, `CUSTOMER_ACCOUNT→CUSTOMERS`, `CUSTOMER_ACCOUNT→ACCOUNTS`, `parent_chunk_data_dictionary.md_8`

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
> The retail‑banking schema records the applicable rate for each product directly in the product’s master table:

* **Deposit (account) products** – The **ACCOUNTS** table contains an **`interest_rate`** column (numeric) that stores the annual rate assigned to the account, and an **`interest_earned`** column that holds the amount of interest that has been accrued/credited. The business‑glossary entr…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_12`, `parent_chunk_data_dictionary.md_10`, `parent_chunk_data_dictionary.md_7`, `Loan→LOANS`, `LOANS→CUSTOMERS`, `LOANS→ACCOUNTS`, `Account→ACCOUNTS`, `parent_chunk_business_glossary.md_2`

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
> The bank’s **BRANCHES** table defines a **branch_type** column whose allowed values are:

- **FullService**  
- **Satellite**  
- **ATMOnly**

These three types are listed in the branch description (chunk [7]) as “full‑service branches, satellite offices, and ATM‑only locations.” The generic business concept for a branch (chunks [1] and [9]) states that a branch is a physical location where custom…

**Sources retrieved (12):** `Branch→BRANCHES`, `parent_chunk_data_dictionary.md_12`, `parent_chunk_data_dictionary.md_7`, `parent_chunk_data_dictionary.md_6`, `Account→ACCOUNTS`, `Automated Teller Machine→ATMS`, `parent_chunk_data_dictionary.md_5`, `parent_chunk_business_glossary.md_2`

**Context previews (first 3):**

1. _Business concept 'Branch' — A physical banking location where customers can access in‑person services such as teller transactions, account opening, loan applications, and financial advisory services. …_

2. _## Entity Relationship Summary  **Key Relationships: ** - customers ←→ accounts (many-to-many via customer_account) - accounts → accounts (self-reference for parent-child hierarchy) - accounts → trans…_

3. _## accounts  **Description: ** Deposit account master table supporting multiple account types (checking, savings, money market, CD, investment). Implements parent-child hierarchy for portfolio aggrega…_

---

### ✅ 19 — How are ATMs related to branches in the schema and what types of ATMs exist?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.6184 | **Gate:** `proceed`

**Expected answer:**
> The atms table has an optional branch_id foreign key referencing branches. When branch_id is NULL, the ATM is standalone and not affiliated with any branch. ATM types are defined by CHECK constraint: Branch (on-premises), DriveThrough (vehicle-accessible), and Standalone (independent locations). Eac…

**System answer:**
> In the data model the **ATMS** table is linked to the **BRANCHES** table through the column **branch_id**:

* **Foreign‑key relationship** – ATMS.branch_id → BRANCHES.branch_id (the key is nullable, so an ATM can exist without being attached to a branch).  
* **Cardinality** – One branch can have many ATMs (the Entity‑Relationship Summary lists “branches → atms (one‑to‑many)”), while each ATM is a…

**Sources retrieved (12):** `ATMS→BRANCHES`, `parent_chunk_data_dictionary.md_6`, `parent_chunk_data_dictionary.md_12`, `Automated Teller Machine→ATMS`, `Branch→BRANCHES`, `parent_chunk_business_glossary.md_3`, `parent_chunk_data_dictionary.md_5`, `parent_chunk_business_glossary.md_2`

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
> The retrieved knowledge graph only defines the **loan** entity at the schema‑level; it does not contain a detailed, step‑by‑step process description for a loan’s lifecycle.  

What the context does provide are the data elements that are used to record each stage of a loan’s life:

* **Loan table (LOANS)** – stores one row per loan agreement.  
  * Columns include **origination_date** (the date the…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_10`, `Loan→LOANS`, `parent_chunk_data_dictionary.md_7`, `parent_chunk_data_dictionary.md_12`, `Branch→BRANCHES`, `parent_chunk_business_glossary.md_2`, `parent_chunk_business_glossary.md_1`, `Loan`

**Context previews (first 3):**

1. _## loans  **Description: ** Loan portfolio table tracking all lending products including mortgages, personal loans, auto loans, HELOCs, and credit cards. Records original terms, amortization schedules…_

2. _Business concept 'Loan' — This table stores information about loan agreements, including borrower details, loan terms, payment schedules, and current status. is implemented by physical table LOANS (co…_

3. _## accounts  **Description: ** Deposit account master table supporting multiple account types (checking, savings, money market, CD, investment). Implements parent-child hierarchy for portfolio aggrega…_

---

### ✅ 21 — What does preferred customer status mean and how is it tracked in the schema?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.5129 | **Gate:** `proceed`

**Expected answer:**
> Preferred status is tracked via the is_preferred boolean flag in the customers table (default: false). The business glossary states that preferred customers receive waived fees, preferred interest rates, and priority service. The glossary examples show preferred customers with longer tenure and high…

**System answer:**
> The schema treats “preferred customer” as a **VIP flag** on the core customer master record.  

* **Business meaning** – In the retail‑banking business glossary the Core Customer Dimension is described as containing “preferred customer flags for VIP treatment.” Thus a preferred customer is simply a client that the bank marks for special or premium handling.  

* **How it is stored** – The **CUSTOM…

**Sources retrieved (12):** `Core Customer Dimension→CUSTOMERS`, `parent_chunk_data_dictionary.md_12`, `parent_chunk_data_dictionary.md_11`, `parent_chunk_data_dictionary.md_10`, `parent_chunk_data_dictionary.md_8`, `parent_chunk_data_dictionary.md_7`, `CARDS→CUSTOMERS`, `parent_chunk_data_dictionary.md_6`

**Context previews (first 3):**

1. _Business concept 'Core Customer Dimension' — Core customer dimension table containing master data for all individual and corporate banking customers. is implemented by physical table CUSTOMERS (column…_

2. _## Entity Relationship Summary  **Key Relationships: ** - customers ←→ accounts (many-to-many via customer_account) - accounts → accounts (self-reference for parent-child hierarchy) - accounts → trans…_

3. _## cards  **Description: ** Payment card issuance table for debit, credit, and ATM cards. Links cards to both customer and account. Tracks security features (chip, contactless, PIN), spending limits, …_

---

### ✅ 22 — How does the accounts table support interest tracking and what business rules govern interest?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.3044 | **Gate:** `proceed`

**Expected answer:**
> The accounts table has interest_rate (nullable DECIMAL for the annual rate) and interest_earned (DECIMAL for year-to-date interest credited). The business glossary states that deposit interest is credited monthly (typically the first day of the month) and that APY accounts for compounding effects. P…

**System answer:**
> The **ACCOUNTS** physical table contains dedicated columns for interest, so the table can record both the rate that applies to the deposit and the amount that has been earned. According to the concept‑to‑table mapping (chunk [2]), the columns are:

* **interest_rate** – the annual percentage rate attached to the account.  
* **interest_earned** – the cumulative interest that has been credited to t…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_7`, `Account→ACCOUNTS`, `parent_chunk_data_dictionary.md_12`, `parent_chunk_data_dictionary.md_10`, `ACCOUNTS→BRANCHES`, `ACCOUNTS→ACCOUNTS`, `parent_chunk_data_dictionary.md_8`, `Loan→LOANS`

**Context previews (first 3):**

1. _## accounts  **Description: ** Deposit account master table supporting multiple account types (checking, savings, money market, CD, investment). Implements parent-child hierarchy for portfolio aggrega…_

2. _Business concept 'Account' — This table stores information about bank accounts, including account details, balances, interest, and status history. is implemented by physical table ACCOUNTS (columns: a…_

3. _## Entity Relationship Summary  **Key Relationships: ** - customers ←→ accounts (many-to-many via customer_account) - accounts → accounts (self-reference for parent-child hierarchy) - accounts → trans…_

---

### ✅ 23 — Can an account exist without any customer linked to it?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.3355 | **Gate:** `proceed`

**Expected answer:**
> Looking at the schema, there is no database-level constraint that forces every account to have a customer_account row. The accounts table has no direct foreign key to customers — the relationship is through the customer_account junction table with a composite primary key (customer_id, account_id). H…

**System answer:**
> Yes. In the schema an **account** can exist without any customer linked to it. The only integrity rule that involves customers and accounts is the **customer_account** junction table, which “requires both customer and account to exist” when a link is recorded (Entity Relationship Summary, chunk [4]). There is no foreign‑key or cascade rule that forces every account row to have a corresponding entr…

**Sources retrieved (12):** `Linked Account And Customer→CUSTOMER_ACCOUNT`, `parent_chunk_data_dictionary.md_8`, `CUSTOMER_ACCOUNT→CUSTOMERS`, `parent_chunk_data_dictionary.md_12`, `CUSTOMER_ACCOUNT→ACCOUNTS`, `parent_chunk_data_dictionary.md_11`, `parent_chunk_data_dictionary.md_10`, `Linked Account And Customer`

**Context previews (first 3):**

1. _Business concept 'Linked Account And Customer' — Key Attributes: - Linked Account and Customer is implemented by physical table CUSTOMER_ACCOUNT (columns: customer_id, account_id, relationship_type, i…_

2. _## customer_account  **Description: ** Junction table implementing many-to-many relationship between customers and accounts. Supports joint ownership, authorized signers, and custodial relationships. …_

3. _Relationship: CUSTOMER_ACCOUNT references CUSTOMERS via foreign key CUSTOMER_ID -> CUSTOMERS.CUSTOMER_ID.…_

---

### ✅ 24 — How does the schema handle failed or cancelled transactions?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.2042 | **Gate:** `proceed`

**Expected answer:**
> The transactions table has a status column with CHECK constraint allowing Pending, Posted, Failed, Cancelled, and OnHold states. The business glossary explains that failed transactions are logged for audit but do not affect the account balance — the balance_after field would reflect no change. Poste…

**System answer:**
> The retail‑banking schema records the outcome of every transaction in the **TRANSACTIONS** fact table. In addition to the basic fields (transaction_id, account_id, transaction_type, amount, currency, etc.), the table includes a **status** column (see the “Operational Heartbeat Of” mapping in chunk [5]).  

The **status** column is defined by the business concept “Transaction” (chunk [7]) and can c…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_9`, `parent_chunk_data_dictionary.md_12`, `parent_chunk_data_dictionary.md_7`, `TRANSACTIONS→ACCOUNTS`, `Operational Heartbeat Of→TRANSACTIONS`, `Automated Teller Machine→ATMS`, `parent_chunk_business_glossary.md_1`, `parent_chunk_business_glossary.md_0`

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
> The ATM entity (see the “ATM” definition in the retrieved context) has a **status** attribute that can take one of three operational values:

* **Operational** – the machine is fully functional. When the status is Operational the ATM can provide all of its supported services, including cash dispensing, deposits and any card‑less withdrawal features that are configured.

* **OutOfService** – the ma…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_6`, `Automated Teller Machine→ATMS`, `Branch→BRANCHES`, `ATMS→BRANCHES`, `parent_chunk_data_dictionary.md_12`, `parent_chunk_data_dictionary.md_11`, `parent_chunk_business_glossary.md_3`, `parent_chunk_data_dictionary.md_5`

**Context previews (first 3):**

1. _## atms  **Description: ** ATM locations including branch-attached machines, drive-through ATMs, and standalone units. Tracks cash balances for replenishment scheduling, GPS coordinates for location s…_

2. _Business concept 'Automated Teller Machine' — Automated Teller Machine - a self-service banking terminal that allows customers to perform basic transactions without teller assistance. is implemented b…_

3. _Business concept 'Branch' — A physical banking location where customers can access in‑person services such as teller transactions, account opening, loan applications, and financial advisory services. …_

---

## Anomalies & Observations

No anomalies detected. All questions grounded with acceptable RAGAS scores.
