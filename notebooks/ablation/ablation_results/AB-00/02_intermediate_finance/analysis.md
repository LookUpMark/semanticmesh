# AB-00 — 02_intermediate_finance — Run Analysis

**Timestamp:** 2026-03-26 20:18:51  
**Run tag:** `run-20260326_210140`

## Configuration

| Parameter | Value |
|-----------|-------|
| Extraction model | `LLM (gpt-5.4-nano)` |
| Reasoning model | `gpt-5.4-mini` |
| Embedding model | `BAAI/bge-m3` |
| Retrieval mode | `hybrid` |
| Reranker | `True` |
| Reranker top_k | `10` |
| Chunk size / overlap | `256 / 32` |
| ER similarity threshold | `0.75` |

## Builder Results

| Metric | Value |
|--------|-------|
| Triplets extracted | 653 |
| Entities resolved | 262 |
| Tables parsed | 8 |
| Tables completed | 8 |

## Query Evaluation Summary

| Metric | Value |
|--------|-------|
| Questions | 15 |
| Grounded | **15/15 (100%)** |
| Avg GT Coverage | 100% |
| Avg Top Score | 0.4678 |
| Avg Chunk Count | 10.0 |
| Abstained | 0 |

## RAGAS Metrics

| Metric | Value | Interpretation |
|--------|-------|----------------|
| Faithfulness | **0.9867** | Answers grounded in context |
| Answer Relevancy | **0.1089** | Answers relevant to question |
| Context Precision | **0.1333** | Retrieved chunks are on-topic |
| Context Recall | **0.1167** | All needed context retrieved |

## Per-Question Deep Dive

### ✅ 1 — What is a checking account?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.7250 | **Gate:** `proceed`

**Expected answer:**
> A checking account is a transactional deposit account designed for day-to-day spending. Key features include unlimited transactions, debit card access, bill pay, and check writing. Standard checking has a minimum balance requirement of $100 with a $12 monthly maintenance fee that can be waived with …

**System answer:**
> A checking account appears to be one of the allowed account types in the `accounts` table, and it falls under the broader `Account` concept defined as a financial arrangement between a customer and the bank for depositing, withdrawing, and managing funds. The context does not provide a more specific definition of checking beyond that.

**RAGAS scores:**

| f | ar | cp | cr |
|---|----|----|-----|
| 1.00 | 0.00 | 0.00 | 0.25 |

**Sources retrieved (10):** `parent_chunk_data_dictionary.md_12`, `parent_chunk_data_dictionary.md_11`, `parent_chunk_data_dictionary.md_13`, `parent_chunk_data_dictionary.md_14`, `parent_chunk_business_glossary.md_0`, `parent_chunk_business_glossary.md_7`, `parent_chunk_business_glossary.md_1`, `a physical banking location where customers can access in-person services including teller transactions, account opening, loan applications, and financial advisory services`

**Context previews (first 3):**

1. _**Constraints: ** - CHECK (account_type IN ('Checking', 'Savings', 'MoneyMarket', 'CD', 'Investment')) - CHECK (status IN ('Active', 'Dormant', 'Frozen', 'Closed')) - CHECK (parent_account_id != accou…_

2. _## accounts  **Description: ** Deposit account master table supporting multiple account types (checking, savings, money market, CD, investment). Implements parent-child hierarchy for portfolio aggrega…_

3. _## customer_account  **Description: ** Junction table implementing many-to-many relationship between customers and accounts. Supports joint ownership, authorized signers, and custodial relationships. …_

---

### ✅ 2 — What is the difference between a savings account and a money market account?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.6894 | **Gate:** `proceed`

**Expected answer:**
> A savings account is an interest-bearing account for accumulating funds with Federal Regulation D limiting withdrawals to 6 per month. It has tiered interest rates from 0.01% to 0.50% APY based on balance. A money market account is a hybrid savings/checking account with higher interest rates (0.15% …

**System answer:**
> The retrieved context identifies both Savings and MoneyMarket as account types in the accounts table, but it does not describe any difference between them. I cannot determine the difference from the provided information.

**RAGAS scores:**

| f | ar | cp | cr |
|---|----|----|-----|
| 1.00 | 0.00 | 0.00 | 0.00 |

**Sources retrieved (10):** `parent_chunk_data_dictionary.md_11`, `parent_chunk_data_dictionary.md_12`, `parent_chunk_data_dictionary.md_15`, `parent_chunk_data_dictionary.md_14`, `parent_chunk_business_glossary.md_0`, `parent_chunk_business_glossary.md_4`, `Checking, Savings, Money Market, CD, Investment`, `parent_chunk_business_glossary.md_2`

**Context previews (first 3):**

1. _## accounts  **Description: ** Deposit account master table supporting multiple account types (checking, savings, money market, CD, investment). Implements parent-child hierarchy for portfolio aggrega…_

2. _**Constraints: ** - CHECK (account_type IN ('Checking', 'Savings', 'MoneyMarket', 'CD', 'Investment')) - CHECK (status IN ('Active', 'Dormant', 'Frozen', 'Closed')) - CHECK (parent_account_id != accou…_

3. _## loans  **Description: ** Loan portfolio table tracking all lending products including mortgages, personal loans, auto loans, HELOCs, and credit cards. Records original terms, amortization schedules…_

---

### ✅ 3 — What is APR versus APY?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.9818 | **Gate:** `proceed`

**Expected answer:**
> APR (Annual Percentage Rate) is the annual cost of a loan including interest and fees, used for loan products. APY (Annual Percentage Yield) is the effective annual rate including compounding effects for deposit products. APY is higher than the nominal rate when compounding is more frequent than ann…

**System answer:**
> From the retrieved context, “Interest” is defined as the cost of borrowing money or the return on depositing money, expressed as an annual percentage rate. The context does not define APY, so I cannot determine the difference between APR and APY from the knowledge graph.

**RAGAS scores:**

| f | ar | cp | cr |
|---|----|----|-----|
| 1.00 | 0.00 | 0.00 | 0.25 |

**Sources retrieved (10):** `parent_chunk_data_dictionary.md_15`, `parent_chunk_business_glossary.md_4`, `parent_chunk_business_glossary.md_0`, `parent_chunk_business_glossary.md_3`, `parent_chunk_data_dictionary.md_11`, `parent_chunk_data_dictionary.md_16`, `parent_chunk_data_dictionary.md_13`, `Borrowing Arrangement`

**Context previews (first 3):**

1. _## loans  **Description: ** Loan portfolio table tracking all lending products including mortgages, personal loans, auto loans, HELOCs, and credit cards. Records original terms, amortization schedules…_

2. _## Interest  **Definition: ** The cost of borrowing money (paid by borrower) or the return on depositing money (paid by bank), expressed as an annual percentage rate. **Business Context:** Interest is…_

3. _# Retail Banking Business Glossary  This document defines the core business concepts and terminology used in the retail banking domain.  ---  ## Account  **Definition: ** A financial arrangement betwe…_

---

### ✅ 4 — What is KYC Level 2?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.9219 | **Gate:** `proceed`

**Expected answer:**
> KYC Level 2 is enhanced due diligence requiring occupation verification and source of funds documentation beyond the basic identity verification (SSN, ID, address) required for Level 1. Level 2 is required for premium products and large transactions. Level 3 is for high-net-worth individuals requiri…

**System answer:**
> The retrieved context mentions KYC only as a compliance/status attribute for customers and says customers have completed Know Your Customer (KYC) verification, but it does not define “KYC Level 2.” From the provided context, I cannot determine what KYC Level 2 means.

**RAGAS scores:**

| f | ar | cp | cr |
|---|----|----|-----|
| 1.00 | 0.00 | 0.00 | 0.00 |

**Sources retrieved (10):** `parent_chunk_data_dictionary.md_18`, `parent_chunk_data_dictionary.md_11`, `parent_chunk_business_glossary.md_1`, `parent_chunk_data_dictionary.md_8`, `parent_chunk_business_glossary.md_3`, `Customer Master Data`, `parent_chunk_business_glossary.md_7`, `parent_chunk_data_dictionary.md_13`

**Context previews (first 3):**

1. _## Entity Relationship Summary  **Key Relationships: ** - customers ←→ accounts (many-to-many via customer_account) - accounts → accounts (self-reference for parent-child hierarchy) - accounts → trans…_

2. _## accounts  **Description: ** Deposit account master table supporting multiple account types (checking, savings, money market, CD, investment). Implements parent-child hierarchy for portfolio aggrega…_

3. _## Customer  **Definition: ** An individual or corporate entity that maintains a banking relationship with the institution, having completed Know Your Customer (KYC) verification. **Business Context:*…_

---

### ✅ 5 — What is the minimum balance requirement for a premium checking account?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.9110 | **Gate:** `proceed`

**Expected answer:**
> Premium checking accounts require a minimum balance of $2,500. This minimum must be maintained to avoid the monthly maintenance fee and qualify for premium benefits including waived fees, preferred interest rates, and higher transaction limits.

**System answer:**
> I cannot determine the minimum balance requirement for a premium checking account from the retrieved context. The context only says the `accounts` table supports `Checking` accounts and other account types, and the Retail Banking Business Glossary defines an `Account`, but it does not provide any minimum balance requirement or any “premium checking” details.

**RAGAS scores:**

| f | ar | cp | cr |
|---|----|----|-----|
| 1.00 | 0.00 | 0.00 | 0.00 |

**Sources retrieved (10):** `parent_chunk_data_dictionary.md_11`, `parent_chunk_data_dictionary.md_12`, `parent_chunk_data_dictionary.md_13`, `parent_chunk_data_dictionary.md_15`, `parent_chunk_business_glossary.md_0`, `parent_chunk_business_glossary.md_7`, `parent_chunk_business_glossary.md_1`, `parent_chunk_business_glossary.md_3`

**Context previews (first 3):**

1. _## accounts  **Description: ** Deposit account master table supporting multiple account types (checking, savings, money market, CD, investment). Implements parent-child hierarchy for portfolio aggrega…_

2. _**Constraints: ** - CHECK (account_type IN ('Checking', 'Savings', 'MoneyMarket', 'CD', 'Investment')) - CHECK (status IN ('Active', 'Dormant', 'Frozen', 'Closed')) - CHECK (parent_account_id != accou…_

3. _## customer_account  **Description: ** Junction table implementing many-to-many relationship between customers and accounts. Supports joint ownership, authorized signers, and custodial relationships. …_

---

### ✅ 6 — What types of loan products does the bank offer?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.7005 | **Gate:** `proceed`

**Expected answer:**
> The bank offers five types of loan products: (1) Mortgage - secured real estate loans with 15-30 year terms at 5.5%-7.5% APR; (2) Personal Loan - unsecured loans for $1,000-$40,000 with 12-60 month terms at 7.0%-18.0% APR; (3) Auto Loan - secured vehicle loans for $5,000-$75,000 with 24-72 month ter…

**System answer:**
> The loans table indicates the bank offers mortgages, personal loans, auto loans, HELOCs, and credit cards.

**RAGAS scores:**

| f | ar | cp | cr |
|---|----|----|-----|
| 1.00 | 0.76 | 1.00 | 1.00 |

**Sources retrieved (10):** `parent_chunk_data_dictionary.md_15`, `parent_chunk_data_dictionary.md_18`, `parent_chunk_data_dictionary.md_11`, `parent_chunk_business_glossary.md_3`, `parent_chunk_business_glossary.md_5`, `parent_chunk_business_glossary.md_0`, `parent_chunk_business_glossary.md_4`, `parent_chunk_business_glossary.md_1`

**Context previews (first 3):**

1. _## loans  **Description: ** Loan portfolio table tracking all lending products including mortgages, personal loans, auto loans, HELOCs, and credit cards. Records original terms, amortization schedules…_

2. _## Entity Relationship Summary  **Key Relationships: ** - customers ←→ accounts (many-to-many via customer_account) - accounts → accounts (self-reference for parent-child hierarchy) - accounts → trans…_

3. _## accounts  **Description: ** Deposit account master table supporting multiple account types (checking, savings, money market, CD, investment). Implements parent-child hierarchy for portfolio aggrega…_

---

### ✅ 7 — What is the daily ATM withdrawal limit for standard customers?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.6511 | **Gate:** `proceed`

**Expected answer:**
> The daily ATM withdrawal limit for standard customers is $500. Premium customers have a higher limit of $2,000 per day. Out-of-network ATM withdrawals incur a $3.00 fee plus any fee charged by the ATM owner.

**System answer:**
> I cannot find this information in the knowledge graph. The retrieved context mentions that the Card concept tracks spending limits and that ATM-related entities exist, but it does not specify any daily ATM withdrawal limit for standard customers.

**RAGAS scores:**

| f | ar | cp | cr |
|---|----|----|-----|
| 1.00 | 0.00 | 0.00 | 0.00 |

**Sources retrieved (10):** `parent_chunk_data_dictionary.md_16`, `parent_chunk_data_dictionary.md_10`, `parent_chunk_data_dictionary.md_18`, `parent_chunk_business_glossary.md_7`, `parent_chunk_business_glossary.md_6`, `parent_chunk_business_glossary.md_2`, `parent_chunk_business_glossary.md_5`, `parent_chunk_business_glossary.md_0`

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
> The context does not define separate business meanings for “parent account” and “child account.” It only shows that `accounts` has a self-referencing hierarchy via `PARENT_ACCOUNT_ID -> ACCOUNTS.ACCOUNT_ID`, and that investment accounts can contain child accounts for portfolio aggregation.

**RAGAS scores:**

| f | ar | cp | cr |
|---|----|----|-----|
| 1.00 | 0.88 | 1.00 | 0.25 |

**Sources retrieved (10):** `parent_chunk_data_dictionary.md_11`, `parent_chunk_data_dictionary.md_18`, `parent_chunk_data_dictionary.md_12`, `ACCOUNTS→ACCOUNTS`, `parent_chunk_data_dictionary.md_13`, `parent_chunk_data_dictionary.md_14`, `parent_chunk_data_dictionary.md_16`, `parent_chunk_data_dictionary.md_15`

**Context previews (first 3):**

1. _## accounts  **Description: ** Deposit account master table supporting multiple account types (checking, savings, money market, CD, investment). Implements parent-child hierarchy for portfolio aggrega…_

2. _## Entity Relationship Summary  **Key Relationships: ** - customers ←→ accounts (many-to-many via customer_account) - accounts → accounts (self-reference for parent-child hierarchy) - accounts → trans…_

3. _**Constraints: ** - CHECK (account_type IN ('Checking', 'Savings', 'MoneyMarket', 'CD', 'Investment')) - CHECK (status IN ('Active', 'Dormant', 'Frozen', 'Closed')) - CHECK (parent_account_id != accou…_

---

### ✅ 9 — What does the status 'Frozen' mean for a card?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.4898 | **Gate:** `proceed`

**Expected answer:**
> A 'Frozen' card status means the card is temporarily suspended due to suspected fraudulent activity detected by monitoring, customer request (lost card, traveling), or negative account status. Frozen cards cannot process transactions. The freeze can be reversed after identity verification to reactiv…

**System answer:**
> The retrieved context shows that card status can be one of the values in the `cards` table, including `Frozen`, but it does not define what `Frozen` means. So I can confirm that `Frozen` is a valid card status in the `cards` concept, but the specific business meaning is not provided in the context.

**RAGAS scores:**

| f | ar | cp | cr |
|---|----|----|-----|
| 1.00 | 0.00 | 0.00 | 0.00 |

**Sources retrieved (10):** `parent_chunk_data_dictionary.md_17`, `parent_chunk_data_dictionary.md_11`, `parent_chunk_data_dictionary.md_12`, `parent_chunk_data_dictionary.md_15`, `parent_chunk_data_dictionary.md_16`, `parent_chunk_data_dictionary.md_10`, `parent_chunk_data_dictionary.md_14`, `parent_chunk_business_glossary.md_7`

**Context previews (first 3):**

1. _**Constraints: ** - CHECK (card_type IN ('Debit', 'Credit', 'ATM')) - CHECK (card_network IN ('Visa', 'Mastercard', 'Discover', 'AmericanExpress')) - CHECK (status IN ('Active', 'Frozen', 'Blocked', '…_

2. _## accounts  **Description: ** Deposit account master table supporting multiple account types (checking, savings, money market, CD, investment). Implements parent-child hierarchy for portfolio aggrega…_

3. _**Constraints: ** - CHECK (account_type IN ('Checking', 'Savings', 'MoneyMarket', 'CD', 'Investment')) - CHECK (status IN ('Active', 'Dormant', 'Frozen', 'Closed')) - CHECK (parent_account_id != accou…_

---

### ✅ 10 — What is the overdraft fee?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0945 | **Gate:** `proceed_with_warning`

**Expected answer:**
> The overdraft fee is $35 per overdraft transaction, with a maximum of 4 overdraft fees per day ($140 total). An overdraft protection transfer from savings to cover the overdraft costs $12. No overdraft fee is charged if the account balance is within $10 at the end of the business day. The fee applie…

**System answer:**
> The retrieved context does not define an overdraft fee, so I cannot determine what it is from the provided information.

**RAGAS scores:**

| f | ar | cp | cr |
|---|----|----|-----|
| 1.00 | 0.00 | 0.00 | 0.00 |

**Sources retrieved (10):** `parent_chunk_data_dictionary.md_14`, `parent_chunk_data_dictionary.md_11`, `parent_chunk_business_glossary.md_2`, `parent_chunk_business_glossary.md_0`, `parent_chunk_data_dictionary.md_8`, `parent_chunk_data_dictionary.md_15`, `parent_chunk_data_dictionary.md_16`, `parent_chunk_business_glossary.md_4`

**Context previews (first 3):**

1. _## transactions  **Description: ** Transaction fact table recording all account activity. Supports multiple transaction types including debits, credits, transfers, and withdrawals. Tracks calculated f…_

2. _## accounts  **Description: ** Deposit account master table supporting multiple account types (checking, savings, money market, CD, investment). Implements parent-child hierarchy for portfolio aggrega…_

3. _## Transaction  **Definition: ** Any financial activity that affects the balance of an account, including debits, credits, transfers, withdrawals, and fees. **Business Context:** Transactions represen…_

---

### ✅ 11 — What accounts does James Wilson have?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.3761 | **Gate:** `proceed`

**Expected answer:**
> James Wilson has a portfolio of three accounts: (1) Checking account CHK-001001 with a current balance of $5,240.35, (2) Savings account SAV-001001 with a current balance of $15,250.75, and (3) 12-month Certificate of Deposit CD-001001 with a current balance of $50,000.00 earning 4.50% APY. His acco…

**System answer:**
> I can’t determine which accounts James Wilson has from the retrieved context, because it only describes the `accounts` and `customer_account` tables and their relationships, not any specific customer record for James Wilson. The grounded takeaway is that customer-to-account links are stored in `customer_account`, but James Wilson’s associated accounts are not provided here.

**RAGAS scores:**

| f | ar | cp | cr |
|---|----|----|-----|
| 0.80 | 0.00 | 0.00 | 0.00 |

**Sources retrieved (10):** `parent_chunk_data_dictionary.md_11`, `parent_chunk_data_dictionary.md_12`, `parent_chunk_data_dictionary.md_18`, `parent_chunk_data_dictionary.md_15`, `parent_chunk_data_dictionary.md_13`, `parent_chunk_data_dictionary.md_14`, `parent_chunk_data_dictionary.md_16`, `parent_chunk_business_glossary.md_1`

**Context previews (first 3):**

1. _## accounts  **Description: ** Deposit account master table supporting multiple account types (checking, savings, money market, CD, investment). Implements parent-child hierarchy for portfolio aggrega…_

2. _**Constraints: ** - CHECK (account_type IN ('Checking', 'Savings', 'MoneyMarket', 'CD', 'Investment')) - CHECK (status IN ('Active', 'Dormant', 'Frozen', 'Closed')) - CHECK (parent_account_id != accou…_

3. _## Entity Relationship Summary  **Key Relationships: ** - customers ←→ accounts (many-to-many via customer_account) - accounts → accounts (self-reference for parent-child hierarchy) - accounts → trans…_

---

### ✅ 12 — What is the current balance of Mary Johnson's savings account?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.1101 | **Gate:** `proceed_with_warning`

**Expected answer:**
> Mary Johnson's savings account SAV-003001 has a current balance of $48,750.50. This is a premium savings account earning 5.00% APY with a $2,500 minimum balance requirement. The account has earned $243.75 in year-to-date interest and has no monthly maintenance fee. Her account is held at the Downtow…

**System answer:**
> I cannot find this information in the knowledge graph.

**RAGAS scores:**

| f | ar | cp | cr |
|---|----|----|-----|
| 1.00 | 0.00 | 0.00 | 0.00 |

**Sources retrieved (10):** `parent_chunk_data_dictionary.md_11`, `parent_chunk_data_dictionary.md_12`, `parent_chunk_data_dictionary.md_15`, `parent_chunk_data_dictionary.md_14`, `parent_chunk_data_dictionary.md_10`, `parent_chunk_data_dictionary.md_13`, `parent_chunk_business_glossary.md_0`, `parent_chunk_business_glossary.md_1`

**Context previews (first 3):**

1. _## accounts  **Description: ** Deposit account master table supporting multiple account types (checking, savings, money market, CD, investment). Implements parent-child hierarchy for portfolio aggrega…_

2. _**Constraints: ** - CHECK (account_type IN ('Checking', 'Savings', 'MoneyMarket', 'CD', 'Investment')) - CHECK (status IN ('Active', 'Dormant', 'Frozen', 'Closed')) - CHECK (parent_account_id != accou…_

3. _## loans  **Description: ** Loan portfolio table tracking all lending products including mortgages, personal loans, auto loans, HELOCs, and credit cards. Records original terms, amortization schedules…_

---

### ✅ 13 — What loans does Michael Rodriguez have?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0019 | **Gate:** `proceed_with_warning`

**Expected answer:**
> Michael Rodriguez has two active loans: (1) An auto loan for $35,000 at 6.50% APR with a 60-month term, monthly payment of $684.57, and current balance due of $28,000.00; (2) He is also a joint owner on a mortgage with Elizabeth Clark for $425,000 at 6.00% APR with a 360-month term, monthly payment …

**System answer:**
> I cannot find this information in the knowledge graph.

**RAGAS scores:**

| f | ar | cp | cr |
|---|----|----|-----|
| 1.00 | 0.00 | 0.00 | 0.00 |

**Sources retrieved (10):** `parent_chunk_data_dictionary.md_15`, `parent_chunk_data_dictionary.md_18`, `parent_chunk_business_glossary.md_3`, `parent_chunk_business_glossary.md_4`, `parent_chunk_data_dictionary.md_11`, `parent_chunk_data_dictionary.md_13`, `parent_chunk_data_dictionary.md_14`, `parent_chunk_data_dictionary.md_12`

**Context previews (first 3):**

1. _## loans  **Description: ** Loan portfolio table tracking all lending products including mortgages, personal loans, auto loans, HELOCs, and credit cards. Records original terms, amortization schedules…_

2. _## Entity Relationship Summary  **Key Relationships: ** - customers ←→ accounts (many-to-many via customer_account) - accounts → accounts (self-reference for parent-child hierarchy) - accounts → trans…_

3. _## Loan  **Definition: ** A financial arrangement where the bank lends a principal amount to a customer, who repays with interest over a specified term according to a fixed schedule. **Business Contex…_

---

### ✅ 14 — What transactions occurred in Patricia Davis's checking account in February 2024?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0309 | **Gate:** `proceed_with_warning`

**Expected answer:**
> Patricia Davis's checking account CHK-004001 had two transactions in February 2024: (1) A debit of $75.50 on February 13 for a point-of-sale purchase at Target Store #4567 in Chicago, IL, reducing her balance to $1,675.75; (2) A credit of $1,500.00 on February 12 from a mobile check deposit, bringin…

**System answer:**
> I cannot determine which transactions occurred in Patricia Davis’s checking account in February 2024 from the retrieved context. What is known is that the `transactions` table records account activity and references `accounts`, and that `accounts` includes a `Checking` account type. However, the context does not include any Patricia Davis account records, transaction rows, or February 2024 transac…

**RAGAS scores:**

| f | ar | cp | cr |
|---|----|----|-----|
| 1.00 | 0.00 | 0.00 | 0.00 |

**Sources retrieved (10):** `parent_chunk_data_dictionary.md_14`, `parent_chunk_data_dictionary.md_11`, `parent_chunk_data_dictionary.md_12`, `TRANSACTIONS→ACCOUNTS`, `parent_chunk_business_glossary.md_1`, `parent_chunk_business_glossary.md_7`, `Financial Transaction, Account Activity, Bank Transaction`, `parent_chunk_business_glossary.md_0`

**Context previews (first 3):**

1. _## transactions  **Description: ** Transaction fact table recording all account activity. Supports multiple transaction types including debits, credits, transfers, and withdrawals. Tracks calculated f…_

2. _## accounts  **Description: ** Deposit account master table supporting multiple account types (checking, savings, money market, CD, investment). Implements parent-child hierarchy for portfolio aggrega…_

3. _**Constraints: ** - CHECK (account_type IN ('Checking', 'Savings', 'MoneyMarket', 'CD', 'Investment')) - CHECK (status IN ('Active', 'Dormant', 'Frozen', 'Closed')) - CHECK (parent_account_id != accou…_

---

### ✅ 15 — Which customers are joint owners on Robert Chen's accounts?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0226 | **Gate:** `proceed_with_warning`

**Expected answer:**
> Linda Thompson is a joint owner on both of Robert Chen's accounts with 50% ownership each: checking account CHK-002001 and savings account SAV-002001. Robert Chen also has joint ownership (50%) on William Harris's savings account SAV-006001. All three customers have Level 2 or Level 3 KYC status and…

**System answer:**
> I cannot determine which customers are joint owners on Robert Chen’s accounts from the retrieved context. The context only tells us that the `customer_account` table supports many-to-many customer-account relationships, including joint ownership, but it does not provide any row-level data or any record for Robert Chen.

**RAGAS scores:**

| f | ar | cp | cr |
|---|----|----|-----|
| 1.00 | 0.00 | 0.00 | 0.00 |

**Sources retrieved (10):** `parent_chunk_data_dictionary.md_13`, `parent_chunk_data_dictionary.md_11`, `parent_chunk_data_dictionary.md_18`, `parent_chunk_data_dictionary.md_12`, `parent_chunk_data_dictionary.md_15`, `parent_chunk_data_dictionary.md_17`, `parent_chunk_business_glossary.md_0`, `parent_chunk_data_dictionary.md_8`

**Context previews (first 3):**

1. _## customer_account  **Description: ** Junction table implementing many-to-many relationship between customers and accounts. Supports joint ownership, authorized signers, and custodial relationships. …_

2. _## accounts  **Description: ** Deposit account master table supporting multiple account types (checking, savings, money market, CD, investment). Implements parent-child hierarchy for portfolio aggrega…_

3. _## Entity Relationship Summary  **Key Relationships: ** - customers ←→ accounts (many-to-many via customer_account) - accounts → accounts (self-reference for parent-child hierarchy) - accounts → trans…_

---

## Anomalies & Observations

- **1**: Very low context precision (0.00) — many off-topic chunks retrieved
- **2**: Very low context precision (0.00) — many off-topic chunks retrieved
- **3**: Very low context precision (0.00) — many off-topic chunks retrieved
- **4**: Very low context precision (0.00) — many off-topic chunks retrieved
- **5**: Very low context precision (0.00) — many off-topic chunks retrieved
- **7**: Very low context precision (0.00) — many off-topic chunks retrieved
- **9**: Very low context precision (0.00) — many off-topic chunks retrieved
- **10**: Very low context precision (0.00) — many off-topic chunks retrieved
- **11**: Very low context precision (0.00) — many off-topic chunks retrieved
- **12**: Very low context precision (0.00) — many off-topic chunks retrieved
- **13**: Very low context precision (0.00) — many off-topic chunks retrieved
- **14**: Very low context precision (0.00) — many off-topic chunks retrieved
- **15**: Very low context precision (0.00) — many off-topic chunks retrieved
