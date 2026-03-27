# AB-00 — 02_intermediate_finance — Run Analysis

**Timestamp:** 2026-03-27 11:41:56  
**Run tag:** `ds02-v2`

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
| Triplets extracted | 589 |
| Entities resolved | 231 |
| Tables parsed | 8 |
| Tables completed | 8 |

## Query Evaluation Summary

| Metric | Value |
|--------|-------|
| Questions | 25 |
| Grounded | **25/25 (100%)** |
| Avg GT Coverage | 100% |
| Avg Top Score | 0.2826 |
| Avg Chunk Count | 12.0 |
| Abstained | 0 |

## RAGAS Metrics

RAGAS evaluation not enabled for this run.

## Per-Question Deep Dive

### ✅ 1 — What is a checking account?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.6477 | **Gate:** `proceed`

**Expected answer:**
> A checking account is a transactional deposit account designed for day-to-day spending. Key features include unlimited transactions, debit card access, bill pay, and check writing. Standard checking has a minimum balance requirement of $100 with a $12 monthly maintenance fee that can be waived with …

**System answer:**
> A checking account is a type of deposit account represented in the `accounts` table with `account_type = 'Checking'`. In the business glossary, an account is “a financial arrangement between a customer and the bank that allows deposit, withdrawal, and management of funds,” and `accounts` tracks attributes like balances, interest accrual, fees, and lifecycle status for the account type.

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_7`, `parent_chunk_data_dictionary.md_8`, `parent_chunk_data_dictionary.md_9`, `parent_chunk_data_dictionary.md_10`, `parent_chunk_data_dictionary.md_12`, `parent_chunk_data_dictionary.md_11`, `parent_chunk_business_glossary.md_0`, `parent_chunk_business_glossary.md_1`

**Context previews (first 3):**

1. _## accounts  **Description: ** Deposit account master table supporting multiple account types (checking, savings, money market, CD, investment). Implements parent-child hierarchy for portfolio aggrega…_

2. _## customer_account  **Description: ** Junction table implementing many-to-many relationship between customers and accounts. Supports joint ownership, authorized signers, and custodial relationships. …_

3. _## transactions  **Description: ** Transaction fact table recording all account activity. Supports multiple transaction types including debits, credits, transfers, and withdrawals. Tracks calculated f…_

---

### ✅ 2 — What is the difference between a savings account and a money market account?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.6601 | **Gate:** `proceed`

**Expected answer:**
> A savings account is an interest-bearing account for accumulating funds with Federal Regulation D limiting withdrawals to 6 per month. It has tiered interest rates from 0.01% to 0.50% APY based on balance. A money market account is a hybrid savings/checking account with higher interest rates (0.15% …

**System answer:**
> In the retrieved context, both “Savings” and “MoneyMarket” appear only as possible values of `accounts.account_type` (along with Checking, CD, and Investment). The context does not provide any additional business definition or criteria that distinguish a savings account from a money market account (e.g., different interest calculation, fees, features, or balance requirements).  

So, from the know…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_7`, `parent_chunk_data_dictionary.md_10`, `parent_chunk_data_dictionary.md_9`, `parent_chunk_data_dictionary.md_8`, `parent_chunk_data_dictionary.md_12`, `parent_chunk_data_dictionary.md_11`, `LOANS→ACCOUNTS`, `parent_chunk_business_glossary.md_0`

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
> In the **Interest** business concept, **APR (Annual Percentage Rate)** is the annual percentage rate used for interest on **loans**, while **APY (Annual Percentage Yield)** is used for **deposits**. The context also notes that these relate to whether interest is **simple vs. compound** and the **compounding frequency** (daily, monthly, annually).

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
> KYC Level 2 is enhanced due diligence requiring occupation verification and source of funds documentation beyond the basic identity verification (SSN, ID, address) required for Level 1. Level 2 is required for premium products and large transactions. Level 3 is for high-net-worth individuals requiri…

**System answer:**
> The knowledge graph only states that KYC levels must be one of Level1, Level2, or Level3 (under the entity relationship/business rules summary). It does not define what “KYC Level 2” specifically entails (e.g., required checks or criteria).

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_12`, `parent_chunk_data_dictionary.md_7`, `parent_chunk_data_dictionary.md_4`, `Customer Master Data`, `parent_chunk_business_glossary.md_0`, `parent_chunk_business_glossary.md_1`, `parent_chunk_data_dictionary.md_5`, `parent_chunk_business_glossary.md_3`

**Context previews (first 3):**

1. _## Entity Relationship Summary  **Key Relationships: ** - customers ←→ accounts (many-to-many via customer_account) - accounts → accounts (self-reference for parent-child hierarchy) - accounts → trans…_

2. _## accounts  **Description: ** Deposit account master table supporting multiple account types (checking, savings, money market, CD, investment). Implements parent-child hierarchy for portfolio aggrega…_

3. _# Retail Banking Data Dictionary  This document provides comprehensive schema documentation for the retail banking database, including table structures, column definitions, constraints, and business c…_

---

### ✅ 5 — What is the minimum balance requirement for a premium checking account?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.8639 | **Gate:** `proceed`

**Expected answer:**
> Premium checking accounts require a minimum balance of $2,500. This minimum must be maintained to avoid the monthly maintenance fee and qualify for premium benefits including waived fees, preferred interest rates, and higher transaction limits.

**System answer:**
> I cannot find the minimum balance requirement for a “premium checking” account in the retrieved context. The schema/business concept for **Account** mentions “Minimum Balance Requirements” generally, and the **accounts** table includes **account_type** and **account_subtype** (e.g., “Premium”), but the retrieved context does not provide any numeric minimum-balance rule for premium checking (or any…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_7`, `parent_chunk_data_dictionary.md_8`, `parent_chunk_data_dictionary.md_10`, `parent_chunk_data_dictionary.md_12`, `parent_chunk_data_dictionary.md_11`, `parent_chunk_data_dictionary.md_6`, `parent_chunk_business_glossary.md_0`, `parent_chunk_business_glossary.md_2`

**Context previews (first 3):**

1. _## accounts  **Description: ** Deposit account master table supporting multiple account types (checking, savings, money market, CD, investment). Implements parent-child hierarchy for portfolio aggrega…_

2. _## customer_account  **Description: ** Junction table implementing many-to-many relationship between customers and accounts. Supports joint ownership, authorized signers, and custodial relationships. …_

3. _## loans  **Description: ** Loan portfolio table tracking all lending products including mortgages, personal loans, auto loans, HELOCs, and credit cards. Records original terms, amortization schedules…_

---

### ✅ 6 — What types of loan products does the bank offer?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.6931 | **Gate:** `proceed`

**Expected answer:**
> The bank offers five types of loan products: (1) Mortgage - secured real estate loans with 15-30 year terms at 5.5%-7.5% APR; (2) Personal Loan - unsecured loans for $1,000-$40,000 with 12-60 month terms at 7.0%-18.0% APR; (3) Auto Loan - secured vehicle loans for $5,000-$75,000 with 24-72 month ter…

**System answer:**
> The bank offers loans covering these loan product types: mortgages, personal loans, auto loans, HELOCs (Home Equity Lines of Credit), and credit cards (as listed under the `loans` table’s `loan_type` values).

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_10`, `parent_chunk_data_dictionary.md_12`, `parent_chunk_data_dictionary.md_7`, `LOANS→CUSTOMERS`, `LOANS→ACCOUNTS`, `Loan portfolio table tracking all lending products including mortgages, personal loans, auto loans, HELOCs, and credit cards`, `parent_chunk_business_glossary.md_1`, `parent_chunk_business_glossary.md_2`

**Context previews (first 3):**

1. _## loans  **Description: ** Loan portfolio table tracking all lending products including mortgages, personal loans, auto loans, HELOCs, and credit cards. Records original terms, amortization schedules…_

2. _## Entity Relationship Summary  **Key Relationships: ** - customers ←→ accounts (many-to-many via customer_account) - accounts → accounts (self-reference for parent-child hierarchy) - accounts → trans…_

3. _## accounts  **Description: ** Deposit account master table supporting multiple account types (checking, savings, money market, CD, investment). Implements parent-child hierarchy for portfolio aggrega…_

---

### ✅ 7 — What is the daily ATM withdrawal limit for standard customers?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.3743 | **Gate:** `proceed`

**Expected answer:**
> The daily ATM withdrawal limit for standard customers is $500. Premium customers have a higher limit of $2,000 per day. Out-of-network ATM withdrawals incur a $3.00 fee plus any fee charged by the ATM owner.

**System answer:**
> I cannot find this information in the knowledge graph.

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_11`, `parent_chunk_data_dictionary.md_6`, `parent_chunk_data_dictionary.md_12`, `parent_chunk_data_dictionary.md_7`, `parent_chunk_business_glossary.md_3`, `parent_chunk_business_glossary.md_1`, `parent_chunk_business_glossary.md_2`, `parent_chunk_business_glossary.md_0`

**Context previews (first 3):**

1. _## cards  **Description: ** Payment card issuance table for debit, credit, and ATM cards. Links cards to both customer and account. Tracks security features (chip, contactless, PIN), spending limits, …_

2. _## atms  **Description: ** ATM locations including branch-attached machines, drive-through ATMs, and standalone units. Tracks cash balances for replenishment scheduling, GPS coordinates for location s…_

3. _## Entity Relationship Summary  **Key Relationships: ** - customers ←→ accounts (many-to-many via customer_account) - accounts → accounts (self-reference for parent-child hierarchy) - accounts → trans…_

---

### ✅ 8 — What is the difference between a parent account and a child account?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.3098 | **Gate:** `proceed`

**Expected answer:**
> A parent account is a primary account that aggregates sub-accounts for portfolio management and reporting. Parent accounts do not hold balances directly; they summarize child account totals. A child account is a sub-account linked to a parent account for organizational purposes, such as in portfolio…

**System answer:**
> In this schema, an account can participate in a parent-child hierarchy used for portfolio aggregation.

A parent account is the higher-level account used to group related accounts for relationship/portfolio purposes (the “investment accounts contain child accounts” model described under `accounts`). A child account is the subordinate account that rolls up under a parent for that aggregation.

The …

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_7`, `parent_chunk_data_dictionary.md_12`, `ACCOUNTS→ACCOUNTS`, `parent_chunk_data_dictionary.md_8`, `parent_chunk_data_dictionary.md_9`, `parent_chunk_data_dictionary.md_11`, `parent_chunk_data_dictionary.md_10`, `CARDS→ACCOUNTS`

**Context previews (first 3):**

1. _## accounts  **Description: ** Deposit account master table supporting multiple account types (checking, savings, money market, CD, investment). Implements parent-child hierarchy for portfolio aggrega…_

2. _## Entity Relationship Summary  **Key Relationships: ** - customers ←→ accounts (many-to-many via customer_account) - accounts → accounts (self-reference for parent-child hierarchy) - accounts → trans…_

3. _Relationship: ACCOUNTS references ACCOUNTS via foreign key PARENT_ACCOUNT_ID -> ACCOUNTS.ACCOUNT_ID.…_

---

### ✅ 9 — What does the status 'Frozen' mean for a card?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0630 | **Gate:** `proceed_with_warning`

**Expected answer:**
> A 'Frozen' card status means the card is temporarily suspended due to suspected fraudulent activity detected by monitoring, customer request (lost card, traveling), or negative account status. Frozen cards cannot process transactions. The freeze can be reversed after identity verification to reactiv…

**System answer:**
> I cannot find this information in the knowledge graph.

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_7`, `parent_chunk_data_dictionary.md_10`, `parent_chunk_data_dictionary.md_11`, `parent_chunk_data_dictionary.md_6`, `parent_chunk_data_dictionary.md_9`, `CARDS→CUSTOMERS`, `parent_chunk_business_glossary.md_0`, `parent_chunk_business_glossary.md_3`

**Context previews (first 3):**

1. _## accounts  **Description: ** Deposit account master table supporting multiple account types (checking, savings, money market, CD, investment). Implements parent-child hierarchy for portfolio aggrega…_

2. _## loans  **Description: ** Loan portfolio table tracking all lending products including mortgages, personal loans, auto loans, HELOCs, and credit cards. Records original terms, amortization schedules…_

3. _## cards  **Description: ** Payment card issuance table for debit, credit, and ATM cards. Links cards to both customer and account. Tracks security features (chip, contactless, PIN), spending limits, …_

---

### ✅ 10 — What is the overdraft fee?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.1067 | **Gate:** `proceed_with_warning`

**Expected answer:**
> The overdraft fee is $35 per overdraft transaction, with a maximum of 4 overdraft fees per day ($140 total). An overdraft protection transfer from savings to cover the overdraft costs $12. No overdraft fee is charged if the account balance is within $10 at the end of the business day. The fee applie…

**System answer:**
> I cannot find this information in the knowledge graph.

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_9`, `parent_chunk_data_dictionary.md_7`, `parent_chunk_business_glossary.md_1`, `parent_chunk_business_glossary.md_0`, `parent_chunk_data_dictionary.md_4`, `Account balance and lifecycle`, `parent_chunk_data_dictionary.md_10`, `parent_chunk_data_dictionary.md_11`

**Context previews (first 3):**

1. _## transactions  **Description: ** Transaction fact table recording all account activity. Supports multiple transaction types including debits, credits, transfers, and withdrawals. Tracks calculated f…_

2. _## accounts  **Description: ** Deposit account master table supporting multiple account types (checking, savings, money market, CD, investment). Implements parent-child hierarchy for portfolio aggrega…_

3. _## Transaction  **Definition: ** Any financial activity that affects the balance of an account, including debits, credits, transfers, withdrawals, and fees. **Business Context:** Transactions represen…_

---

### ✅ 11 — What accounts does James Wilson have?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0023 | **Gate:** `proceed_with_warning`

**Expected answer:**
> James Wilson has a portfolio of three accounts: (1) Checking account CHK-001001 with a current balance of $5,240.35, (2) Savings account SAV-001001 with a current balance of $15,250.75, and (3) 12-month Certificate of Deposit CD-001001 with a current balance of $50,000.00 earning 4.50% APY. His acco…

**System answer:**
> The retrieved context only provides schema-level structures for mapping customers to accounts, not any specific customer records or their identifiers. It defines the `customers` table (with `first_name`, `last_name`, and `tax_id`) and the `customer_account` junction table that maps `customer_id` to `account_id` (including fields like `relationship_type`, `is_primary`, and `ownership_percentage`).
…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_7`, `parent_chunk_data_dictionary.md_12`, `parent_chunk_data_dictionary.md_10`, `parent_chunk_data_dictionary.md_8`, `parent_chunk_data_dictionary.md_9`, `parent_chunk_data_dictionary.md_11`, `ACCOUNTS→BRANCHES`, `ACCOUNTS→ACCOUNTS`

**Context previews (first 3):**

1. _## accounts  **Description: ** Deposit account master table supporting multiple account types (checking, savings, money market, CD, investment). Implements parent-child hierarchy for portfolio aggrega…_

2. _## Entity Relationship Summary  **Key Relationships: ** - customers ←→ accounts (many-to-many via customer_account) - accounts → accounts (self-reference for parent-child hierarchy) - accounts → trans…_

3. _## loans  **Description: ** Loan portfolio table tracking all lending products including mortgages, personal loans, auto loans, HELOCs, and credit cards. Records original terms, amortization schedules…_

---

### ✅ 12 — What is the current balance of Mary Johnson's savings account?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0868 | **Gate:** `proceed_with_warning`

**Expected answer:**
> Mary Johnson's savings account SAV-003001 has a current balance of $48,750.50. This is a premium savings account earning 5.00% APY with a $2,500 minimum balance requirement. The account has earned $243.75 in year-to-date interest and has no monthly maintenance fee. Her account is held at the Downtow…

**System answer:**
> I cannot determine the current balance of Mary Johnson’s savings account from the retrieved context. The knowledge graph content provided here includes only schema/table descriptions (for example, the `accounts` table “tracks balances” and the `customer_account` junction links customers to accounts), but it does not include any customer record for “Mary Johnson,” any specific savings account recor…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_7`, `parent_chunk_data_dictionary.md_10`, `parent_chunk_data_dictionary.md_9`, `parent_chunk_data_dictionary.md_6`, `parent_chunk_data_dictionary.md_8`, `parent_chunk_data_dictionary.md_11`, `parent_chunk_business_glossary.md_0`, `parent_chunk_business_glossary.md_1`

**Context previews (first 3):**

1. _## accounts  **Description: ** Deposit account master table supporting multiple account types (checking, savings, money market, CD, investment). Implements parent-child hierarchy for portfolio aggrega…_

2. _## loans  **Description: ** Loan portfolio table tracking all lending products including mortgages, personal loans, auto loans, HELOCs, and credit cards. Records original terms, amortization schedules…_

3. _## transactions  **Description: ** Transaction fact table recording all account activity. Supports multiple transaction types including debits, credits, transfers, and withdrawals. Tracks calculated f…_

---

### ✅ 13 — What loans does Michael Rodriguez have?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0019 | **Gate:** `proceed_with_warning`

**Expected answer:**
> Michael Rodriguez has two active loans: (1) An auto loan for $35,000 at 6.50% APR with a 60-month term, monthly payment of $684.57, and current balance due of $28,000.00; (2) He is also a joint owner on a mortgage with Elizabeth Clark for $425,000 at 6.00% APR with a 360-month term, monthly payment …

**System answer:**
> I cannot determine what loans Michael Rodriguez has from the retrieved context. The knowledge graph provides only schema-level information (for example, the `loans` table and that `customers → loans` is one-to-many via `loans.customer_id`), but it does not include any customer records or loan records identifying “Michael Rodriguez,” nor any data to link his name to a `customer_id`.

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_10`, `parent_chunk_data_dictionary.md_12`, `parent_chunk_business_glossary.md_1`, `parent_chunk_business_glossary.md_2`, `Loan portfolio table tracking all lending products including mortgages, personal loans, auto loans, HELOCs, and credit cards`, `parent_chunk_data_dictionary.md_7`, `parent_chunk_data_dictionary.md_8`, `parent_chunk_data_dictionary.md_9`

**Context previews (first 3):**

1. _## loans  **Description: ** Loan portfolio table tracking all lending products including mortgages, personal loans, auto loans, HELOCs, and credit cards. Records original terms, amortization schedules…_

2. _## Entity Relationship Summary  **Key Relationships: ** - customers ←→ accounts (many-to-many via customer_account) - accounts → accounts (self-reference for parent-child hierarchy) - accounts → trans…_

3. _## Transaction  **Definition: ** Any financial activity that affects the balance of an account, including debits, credits, transfers, withdrawals, and fees. **Business Context:** Transactions represen…_

---

### ✅ 14 — What transactions occurred in Patricia Davis's checking account in February 2024?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0054 | **Gate:** `proceed_with_warning`

**Expected answer:**
> Patricia Davis's checking account CHK-004001 had two transactions in February 2024: (1) A debit of $75.50 on February 13 for a point-of-sale purchase at Target Store #4567 in Chicago, IL, reducing her balance to $1,675.75; (2) A credit of $1,500.00 on February 12 from a mobile check deposit, bringin…

**System answer:**
> I cannot find this information in the knowledge graph.

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_12`, `parent_chunk_data_dictionary.md_9`, `parent_chunk_data_dictionary.md_7`, `TRANSACTIONS→ACCOUNTS`, `parent_chunk_data_dictionary.md_10`, `parent_chunk_data_dictionary.md_11`, `parent_chunk_business_glossary.md_0`, `parent_chunk_business_glossary.md_1`

**Context previews (first 3):**

1. _## Entity Relationship Summary  **Key Relationships: ** - customers ←→ accounts (many-to-many via customer_account) - accounts → accounts (self-reference for parent-child hierarchy) - accounts → trans…_

2. _## transactions  **Description: ** Transaction fact table recording all account activity. Supports multiple transaction types including debits, credits, transfers, and withdrawals. Tracks calculated f…_

3. _## accounts  **Description: ** Deposit account master table supporting multiple account types (checking, savings, money market, CD, investment). Implements parent-child hierarchy for portfolio aggrega…_

---

### ✅ 15 — Which customers are joint owners on Robert Chen's accounts?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0226 | **Gate:** `proceed_with_warning`

**Expected answer:**
> Linda Thompson is a joint owner on both of Robert Chen's accounts with 50% ownership each: checking account CHK-002001 and savings account SAV-002001. Robert Chen also has joint ownership (50%) on William Harris's savings account SAV-006001. All three customers have Level 2 or Level 3 KYC status and…

**System answer:**
> I cannot determine which customers are joint owners on Robert Chen’s accounts from the retrieved knowledge graph, because it only contains schema-level metadata (e.g., the `customer_account` junction table and its `relationship_type` values like `JointOwner`) and does not include the actual customer records (such as “Robert Chen”) or the specific rows linking Robert Chen to accounts and other co-o…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_8`, `parent_chunk_data_dictionary.md_7`, `parent_chunk_data_dictionary.md_12`, `parent_chunk_data_dictionary.md_10`, `parent_chunk_data_dictionary.md_11`, `parent_chunk_data_dictionary.md_9`, `Relationship Type`, `parent_chunk_business_glossary.md_0`

**Context previews (first 3):**

1. _## customer_account  **Description: ** Junction table implementing many-to-many relationship between customers and accounts. Supports joint ownership, authorized signers, and custodial relationships. …_

2. _## accounts  **Description: ** Deposit account master table supporting multiple account types (checking, savings, money market, CD, investment). Implements parent-child hierarchy for portfolio aggrega…_

3. _## Entity Relationship Summary  **Key Relationships: ** - customers ←→ accounts (many-to-many via customer_account) - accounts → accounts (self-reference for parent-child hierarchy) - accounts → trans…_

---

### ✅ 16 — What cards does Mary Johnson have?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0013 | **Gate:** `proceed_with_warning`

**Expected answer:**
> Mary Johnson has three cards: (1) A Visa debit card ending in 0366 linked to her checking account CHK-003001 with a $5,000 daily limit and $1,000 ATM limit, chip and contactless enabled, active status; (2) A Visa credit card ending in 0840 with a $25,000 credit limit, $5,000 daily limit, chip and co…

**System answer:**
> I cannot find this information in the knowledge graph.

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_11`, `parent_chunk_data_dictionary.md_10`, `parent_chunk_data_dictionary.md_7`, `parent_chunk_data_dictionary.md_6`, `parent_chunk_data_dictionary.md_12`, `parent_chunk_data_dictionary.md_9`, `parent_chunk_data_dictionary.md_8`, `parent_chunk_business_glossary.md_3`

**Context previews (first 3):**

1. _## cards  **Description: ** Payment card issuance table for debit, credit, and ATM cards. Links cards to both customer and account. Tracks security features (chip, contactless, PIN), spending limits, …_

2. _## loans  **Description: ** Loan portfolio table tracking all lending products including mortgages, personal loans, auto loans, HELOCs, and credit cards. Records original terms, amortization schedules…_

3. _## accounts  **Description: ** Deposit account master table supporting multiple account types (checking, savings, money market, CD, investment). Implements parent-child hierarchy for portfolio aggrega…_

---

### ✅ 17 — What is the interest rate on James Wilson's CD?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0456 | **Gate:** `proceed_with_warning`

**Expected answer:**
> James Wilson's 12-month Certificate of Deposit CD-001001 has an interest rate of 4.50% APY. The CD has a principal amount of $50,000.00, was opened on February 15, 2023, matures on February 15, 2024, and has earned $2,250.00 in interest to date. This promotional rate is higher than the standard 12-m…

**System answer:**
> I can’t determine the interest rate on James Wilson’s CD from the retrieved context.

What the context does show is that CDs exist as an `account_type` value in the `accounts` table (“Type: Checking/Savings/MoneyMarket/CD/Investment”) and that the banking glossary defines interest rates (e.g., APR/APY) as a business concept. The context also includes customer identity fields (`customers.first_name…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_7`, `parent_chunk_data_dictionary.md_10`, `parent_chunk_business_glossary.md_2`, `parent_chunk_business_glossary.md_0`, `parent_chunk_business_glossary.md_1`, `parent_chunk_data_dictionary.md_4`, `parent_chunk_data_dictionary.md_8`, `parent_chunk_data_dictionary.md_9`

**Context previews (first 3):**

1. _## accounts  **Description: ** Deposit account master table supporting multiple account types (checking, savings, money market, CD, investment). Implements parent-child hierarchy for portfolio aggrega…_

2. _## loans  **Description: ** Loan portfolio table tracking all lending products including mortgages, personal loans, auto loans, HELOCs, and credit cards. Records original terms, amortization schedules…_

3. _## Interest  **Definition: ** The cost of borrowing money (paid by borrower) or the return on depositing money (paid by bank), expressed as an annual percentage rate. **Business Context:** Interest is…_

---

### ✅ 18 — What branch does Robert Chen bank at and what are its services?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0083 | **Gate:** `proceed_with_warning`

**Expected answer:**
> Robert Chen banks at the Westside Branch (branch code 0002) at 456 Oak Avenue, Los Angeles, CA 90001. This is a full-service branch with 2 tellers, 3 ATMs, and managed by Sarah Mitchell. Services include Monday-Friday 9AM-6PM and Saturday 9AM-2PM hours, loan officers, financial advisors, safe deposi…

**System answer:**
> I cannot find this information in the knowledge graph.

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_7`, `parent_chunk_data_dictionary.md_12`, `parent_chunk_data_dictionary.md_10`, `parent_chunk_data_dictionary.md_6`, `parent_chunk_data_dictionary.md_8`, `parent_chunk_data_dictionary.md_11`, `parent_chunk_data_dictionary.md_9`, `parent_chunk_business_glossary.md_2`

**Context previews (first 3):**

1. _## accounts  **Description: ** Deposit account master table supporting multiple account types (checking, savings, money market, CD, investment). Implements parent-child hierarchy for portfolio aggrega…_

2. _## Entity Relationship Summary  **Key Relationships: ** - customers ←→ accounts (many-to-many via customer_account) - accounts → accounts (self-reference for parent-child hierarchy) - accounts → trans…_

3. _## loans  **Description: ** Loan portfolio table tracking all lending products including mortgages, personal loans, auto loans, HELOCs, and credit cards. Records original terms, amortization schedules…_

---

### ✅ 19 — What ATMs are available at the Downtown Headquarters branch?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0454 | **Gate:** `proceed_with_warning`

**Expected answer:**
> The Downtown Headquarters branch has 4 ATMs: (1) ATM-0001 is a branch ATM at 123 Main Street, operational with $85,000 cash balance, supports deposits and cardless transactions; (2) ATM-0002 is a drive-through ATM at the same address, operational with $45,000 cash balance, supports deposits and card…

**System answer:**
> The retrieved context does not specify which ATMs are available at any specific branch name such as “Downtown Headquarters.” It only defines the `atms` table (with `branch_id` referencing `branches.branch_id`, plus an operational status field and location details) and the `branches` table (which includes `branch_name`).  

So, the context provides the schema needed to identify ATMs for a given `br…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_6`, `ATMS→BRANCHES`, `parent_chunk_data_dictionary.md_11`, `parent_chunk_data_dictionary.md_7`, `parent_chunk_business_glossary.md_3`, `parent_chunk_business_glossary.md_2`, `parent_chunk_data_dictionary.md_5`, `parent_chunk_business_glossary.md_1`

**Context previews (first 3):**

1. _## atms  **Description: ** ATM locations including branch-attached machines, drive-through ATMs, and standalone units. Tracks cash balances for replenishment scheduling, GPS coordinates for location s…_

2. _Relationship: ATMS references BRANCHES via foreign key BRANCH_ID -> BRANCHES.BRANCH_ID.…_

3. _## cards  **Description: ** Payment card issuance table for debit, credit, and ATM cards. Links cards to both customer and account. Tracks security features (chip, contactless, PIN), spending limits, …_

---

### ✅ 20 — What is the status of Jennifer Martinez's personal loan application?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0033 | **Gate:** `proceed_with_warning`

**Expected answer:**
> Jennifer Martinez has an active personal loan (loan ID 70010) for $5,000 at 12.00% APR with a 24-month term. The monthly payment is $235.37 and the current balance due is $4,200.00. The loan was originated January 5, 2024 and matures January 5, 2026. Payments are automatically drafted from her check…

**System answer:**
> I cannot find this information in the knowledge graph.

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_10`, `parent_chunk_data_dictionary.md_7`, `parent_chunk_data_dictionary.md_9`, `parent_chunk_data_dictionary.md_6`, `parent_chunk_data_dictionary.md_11`, `parent_chunk_data_dictionary.md_12`, `parent_chunk_business_glossary.md_1`, `parent_chunk_business_glossary.md_2`

**Context previews (first 3):**

1. _## loans  **Description: ** Loan portfolio table tracking all lending products including mortgages, personal loans, auto loans, HELOCs, and credit cards. Records original terms, amortization schedules…_

2. _## accounts  **Description: ** Deposit account master table supporting multiple account types (checking, savings, money market, CD, investment). Implements parent-child hierarchy for portfolio aggrega…_

3. _## transactions  **Description: ** Transaction fact table recording all account activity. Supports multiple transaction types including debits, credits, transfers, and withdrawals. Tracks calculated f…_

---

### ✅ 21 — Which customers have preferred status and why?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.4332 | **Gate:** `proceed`

**Expected answer:**
> Four customers have preferred status: (1) James Wilson - combined deposit balance of $70,491.10 and 5+ years tenure; (2) Mary Johnson - combined deposit balance of $151,000.50 and 8+ years tenure; (3) Michael Rodriguez - active loan relationship and combined deposit balance of $20,850.75; (4) Elizab…

**System answer:**
> The knowledge graph does not provide which specific customers have “preferred” status, because it contains schema-level metadata (table/column definitions) rather than customer records.

What it does say is that the `customers` table includes “preferred customer flags for VIP treatment,” so the “why” is to mark customers for VIP treatment under the `customers` business concept. However, the contex…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_10`, `parent_chunk_data_dictionary.md_8`, `parent_chunk_data_dictionary.md_6`, `parent_chunk_data_dictionary.md_11`, `parent_chunk_data_dictionary.md_12`, `parent_chunk_data_dictionary.md_7`, `parent_chunk_data_dictionary.md_9`, `parent_chunk_data_dictionary.md_4`

**Context previews (first 3):**

1. _## loans  **Description: ** Loan portfolio table tracking all lending products including mortgages, personal loans, auto loans, HELOCs, and credit cards. Records original terms, amortization schedules…_

2. _## customer_account  **Description: ** Junction table implementing many-to-many relationship between customers and accounts. Supports joint ownership, authorized signers, and custodial relationships. …_

3. _## atms  **Description: ** ATM locations including branch-attached machines, drive-through ATMs, and standalone units. Tracks cash balances for replenishment scheduling, GPS coordinates for location s…_

---

### ✅ 22 — What is the total interest earned across all savings accounts this year?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0557 | **Gate:** `proceed_with_warning`

**Expected answer:**
> Based on the year-to-date interest earned field, the total interest credited across all savings accounts in January 2024 was $365.37. This includes interest from: SAV-001001 ($38.12), SAV-002001 ($3.50), SAV-003001 ($243.75), SAV-004001 ($7.80), SAV-005001 ($16.70), SAV-006001 ($55.50), and MM-00300…

**System answer:**
> The retrieved context describes the schema and business concepts, not the actual year’s account-level results needed to compute a total.

From the `accounts` table description, account master data “tracks balances, interest accrual, fees, and account lifecycle status,” and the glossary notes attributes such as “interest_rate/interest_earned.” However, the context does not provide any transaction r…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_7`, `parent_chunk_data_dictionary.md_10`, `parent_chunk_data_dictionary.md_8`, `parent_chunk_data_dictionary.md_12`, `parent_chunk_data_dictionary.md_11`, `parent_chunk_data_dictionary.md_6`, `parent_chunk_business_glossary.md_0`, `parent_chunk_business_glossary.md_2`

**Context previews (first 3):**

1. _## accounts  **Description: ** Deposit account master table supporting multiple account types (checking, savings, money market, CD, investment). Implements parent-child hierarchy for portfolio aggrega…_

2. _## loans  **Description: ** Loan portfolio table tracking all lending products including mortgages, personal loans, auto loans, HELOCs, and credit cards. Records original terms, amortization schedules…_

3. _## customer_account  **Description: ** Junction table implementing many-to-many relationship between customers and accounts. Supports joint ownership, authorized signers, and custodial relationships. …_

---

### ✅ 23 — What accounts have no customers linked to them?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0960 | **Gate:** `proceed_with_warning`

**Expected answer:**
> All accounts in the system have at least one customer linked. The customer_account junction table ensures that every account has at least one Owner relationship. This is enforced by the business rule that accounts cannot exist without customer ownership. Joint accounts have multiple customers linked…

**System answer:**
> I cannot determine which specific accounts have no customers linked to them from the retrieved context, because it only contains schema-level metadata (e.g., the `customer_account` junction table that links customers to accounts via `customer_id` and `account_id`), not the actual rows needed to check for missing relationships. To answer the question, you would need to evaluate `accounts` against t…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_8`, `parent_chunk_data_dictionary.md_10`, `CUSTOMER_ACCOUNT→CUSTOMERS`, `parent_chunk_data_dictionary.md_11`, `CUSTOMER_ACCOUNT→ACCOUNTS`, `parent_chunk_data_dictionary.md_12`, `LOANS→CUSTOMERS`, `CARDS→CUSTOMERS`

**Context previews (first 3):**

1. _## customer_account  **Description: ** Junction table implementing many-to-many relationship between customers and accounts. Supports joint ownership, authorized signers, and custodial relationships. …_

2. _## loans  **Description: ** Loan portfolio table tracking all lending products including mortgages, personal loans, auto loans, HELOCs, and credit cards. Records original terms, amortization schedules…_

3. _Relationship: CUSTOMER_ACCOUNT references CUSTOMERS via foreign key CUSTOMER_ID -> CUSTOMERS.CUSTOMER_ID.…_

---

### ✅ 24 — What transactions failed to post and why?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.2462 | **Gate:** `proceed`

**Expected answer:**
> One transaction failed to post: Transaction ID 900015, a $25.00 point-of-sale debit at a gas station on Jennifer Martinez's checking account CHK-006001 on February 13, 2024. The transaction failed due to insufficient funds in the account. The transaction status is 'Failed' and no funds were moved. T…

**System answer:**
> The retrieved knowledge graph does not provide enough detail to answer “what transactions failed to post and why.”

In the schema excerpt for `transactions` (concept/table `transactions`), the listed columns include `transaction_id`, `account_id`, `transaction_type`, `amount`, and `currency`, and it does not show any fields for failure reason, failure code, or failure message. Also, the knowledge …

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_9`, `parent_chunk_data_dictionary.md_7`, `parent_chunk_data_dictionary.md_12`, `parent_chunk_data_dictionary.md_8`, `parent_chunk_data_dictionary.md_11`, `parent_chunk_data_dictionary.md_10`, `TRANSACTIONS→ACCOUNTS`, `parent_chunk_data_dictionary.md_6`

**Context previews (first 3):**

1. _## transactions  **Description: ** Transaction fact table recording all account activity. Supports multiple transaction types including debits, credits, transfers, and withdrawals. Tracks calculated f…_

2. _## accounts  **Description: ** Deposit account master table supporting multiple account types (checking, savings, money market, CD, investment). Implements parent-child hierarchy for portfolio aggrega…_

3. _## Entity Relationship Summary  **Key Relationships: ** - customers ←→ accounts (many-to-many via customer_account) - accounts → accounts (self-reference for parent-child hierarchy) - accounts → trans…_

---

### ✅ 25 — Which ATMs are currently out of service or out of cash?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.7221 | **Gate:** `proceed`

**Expected answer:**
> Two ATMs have issues: (1) ATM-0004 at 456 Oak Avenue (Westside Branch) is 'OutOfCash' with $0.00 balance - it was last replenished February 14, 2024 at 8:00 AM but deposits may still work; (2) STANDALONE-002 at 987 Birch Road in the Grocery Store is 'OutOfService' with $15,000 cash balance - this is…

**System answer:**
> The retrieved context indicates that the **`atms`** table tracks an ATM **operational status** with possible values including **Operational**, **OutOfService**, and **OutOfCash** (see the ATM business context in **“ATM”**).

However, the knowledge graph content provided here includes **schema/business definitions only** and does **not** include any actual ATM records or a specific “status” column …

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_6`, `parent_chunk_data_dictionary.md_11`, `parent_chunk_data_dictionary.md_9`, `parent_chunk_data_dictionary.md_12`, `ATMS→BRANCHES`, `parent_chunk_business_glossary.md_3`, `parent_chunk_data_dictionary.md_5`, `parent_chunk_business_glossary.md_1`

**Context previews (first 3):**

1. _## atms  **Description: ** ATM locations including branch-attached machines, drive-through ATMs, and standalone units. Tracks cash balances for replenishment scheduling, GPS coordinates for location s…_

2. _## cards  **Description: ** Payment card issuance table for debit, credit, and ATM cards. Links cards to both customer and account. Tracks security features (chip, contactless, PIN), spending limits, …_

3. _## transactions  **Description: ** Transaction fact table recording all account activity. Supports multiple transaction types including debits, credits, transfers, and withdrawals. Tracks calculated f…_

---

## Anomalies & Observations

No anomalies detected. All questions grounded with acceptable RAGAS scores.
