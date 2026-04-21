# AB-BEST — 02_intermediate_finance — Run Analysis

**Timestamp:** 2026-04-21 08:41:31  
**Run tag:** `run-20260421_094804`

## Configuration

| Parameter | Value |
|-----------|-------|
| Extraction model | `LLM (openai/gpt-4.1-nano)` |
| Reasoning model | `openai/gpt-oss-120b` |
| Embedding model | `BAAI/bge-m3` |
| Retrieval mode | `hybrid` |
| Reranker | `True` |
| Reranker top_k | `10` |
| Chunk size / overlap | `256 / 32` |
| ER similarity threshold | `0.65` |

## Builder Results

| Metric | Value |
|--------|-------|
| Triplets extracted | 142 |
| Entities resolved | 48 |
| Tables parsed | 8 |
| Tables completed | 8 |

## Query Evaluation Summary

| Metric | Value |
|--------|-------|
| Questions | 25 |
| Grounded | **25/25 (100%)** |
| Avg GT Coverage | 88% |
| Avg Top Score | 0.4719 |
| Avg Chunk Count | 10.0 |
| Abstained | 0 |

## RAGAS Metrics

RAGAS evaluation not enabled for this run.

## Per-Question Deep Dive

### ✅ 1 — What is a checking account?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0000 | **Gate:** `proceed`

**Expected answer:**
> A checking account is one of five account types (Checking, Savings, MoneyMarket, CD, Investment) defined by the CHECK constraint on the accounts table. According to the business glossary, accounts are financial arrangements for deposit, withdrawal, and management of funds. The schema tracks current_…

**System answer:**
> 

**Sources retrieved (10):** `parent_chunk_data_dictionary.md_7`, `parent_chunk_data_dictionary.md_8`, `Bank Account→ACCOUNTS`, `parent_chunk_data_dictionary.md_9`, `parent_chunk_business_glossary.md_0`, `Bank Account`, `parent_chunk_business_glossary.md_1`, `parent_chunk_business_glossary.md_2`

---

### ✅ 2 — What is the difference between a savings account and a money market account?

**Status:** GROUNDED  
**GT Coverage:** 50% | **Top Score:** 0.0000 | **Gate:** `proceed`

**Expected answer:**
> Both savings and money market are account types defined in the accounts table CHECK constraint. The business glossary Interest section provides example rates: Standard Savings earns 0.25% APY (with monthly compounding), Premium Savings earns 0.50% APY (with daily compounding), while Money Market ear…

**System answer:**
> 

**Sources retrieved (10):** `parent_chunk_data_dictionary.md_7`, `parent_chunk_data_dictionary.md_10`, `parent_chunk_data_dictionary.md_9`, `parent_chunk_data_dictionary.md_8`, `parent_chunk_data_dictionary.md_12`, `parent_chunk_data_dictionary.md_11`, `parent_chunk_business_glossary.md_0`, `parent_chunk_business_glossary.md_2`

---

### ✅ 3 — What is APR versus APY?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0000 | **Gate:** `proceed`

**Expected answer:**
> APR (Annual Percentage Rate) is the annual cost of a loan including interest and fees, used for loan products. APY (Annual Percentage Yield) is the effective annual rate including compounding effects for deposit products. APY is higher than the nominal rate when compounding is more frequent than ann…

**System answer:**
> 

**Sources retrieved (10):** `parent_chunk_data_dictionary.md_10`, `parent_chunk_business_glossary.md_2`, `parent_chunk_business_glossary.md_0`, `parent_chunk_business_glossary.md_1`, `parent_chunk_data_dictionary.md_7`, `parent_chunk_data_dictionary.md_11`, `parent_chunk_data_dictionary.md_8`, `parent_chunk_business_glossary.md_3`

---

### ✅ 4 — What is KYC Level 2?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0000 | **Gate:** `proceed`

**Expected answer:**
> The customers table has a kyc_status column with a CHECK constraint allowing Level1, Level2, and Level3. The business glossary states that Level1 is the minimum requirement for account opening, Level3 is required for high-value accounts and international transfers, and risk_profile determines eligib…

**System answer:**
> 

**Sources retrieved (10):** `parent_chunk_data_dictionary.md_12`, `Know Your Customer→CUSTOMERS`, `parent_chunk_data_dictionary.md_7`, `parent_chunk_data_dictionary.md_4`, `parent_chunk_business_glossary.md_0`, `Know Your Customer`, `parent_chunk_business_glossary.md_1`, `parent_chunk_data_dictionary.md_5`

---

### ✅ 5 — How does the schema support different account subtypes and their varying requirements?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0000 | **Gate:** `proceed`

**Expected answer:**
> The accounts table has an account_subtype column (VARCHAR 30, nullable) that stores values like Premium or Standard to differentiate within each account_type. Combined with the minimum_balance and monthly_fee columns, each account can have different requirements configured per subtype. The account_t…

**System answer:**
> 

**Sources retrieved (10):** `parent_chunk_data_dictionary.md_7`, `parent_chunk_data_dictionary.md_12`, `Bank Account→ACCOUNTS`, `parent_chunk_data_dictionary.md_8`, `parent_chunk_data_dictionary.md_9`, `parent_chunk_data_dictionary.md_11`, `parent_chunk_business_glossary.md_0`, `parent_chunk_business_glossary.md_1`

---

### ✅ 6 — What types of loan products does the bank offer?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0000 | **Gate:** `proceed`

**Expected answer:**
> The bank offers five loan types defined by the CHECK constraint on loans.loan_type: (1) Mortgage — secured by real estate, glossary example shows $350,000 at 5.50% APR for 360 months; (2) Personal Loan — unsecured, example $15,000 at 8.50% APR for 48 months; (3) Auto Loan — secured by vehicle, examp…

**System answer:**
> 

**Sources retrieved (10):** `parent_chunk_data_dictionary.md_10`, `parent_chunk_data_dictionary.md_12`, `Physical Banking Location→BRANCHES`, `Loan Agreement→LOANS`, `parent_chunk_data_dictionary.md_7`, `parent_chunk_business_glossary.md_1`, `parent_chunk_business_glossary.md_2`, `parent_chunk_business_glossary.md_0`

---

### ✅ 7 — What is the daily ATM withdrawal limit for standard customers?

**Status:** GROUNDED  
**GT Coverage:** 50% | **Top Score:** 0.0000 | **Gate:** `proceed`

**Expected answer:**
> The cards table has an atm_daily_limit column with a default value of $500. The business glossary Card Examples confirm this: a standard Debit Card has a $500 ATM limit, while a Premium Debit card has a $2,000 ATM limit. The daily_limit column (default $3,000) controls POS spending separately. These…

**System answer:**
> 

**Sources retrieved (10):** `parent_chunk_data_dictionary.md_11`, `Bank Card→CARDS`, `parent_chunk_data_dictionary.md_6`, `parent_chunk_data_dictionary.md_12`, `parent_chunk_data_dictionary.md_7`, `parent_chunk_business_glossary.md_3`, `parent_chunk_business_glossary.md_1`, `parent_chunk_business_glossary.md_2`

---

### ✅ 8 — What is the difference between a parent account and a child account?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0000 | **Gate:** `proceed`

**Expected answer:**
> The accounts table supports parent-child hierarchies through the parent_account_id self-referencing foreign key, with a CHECK constraint preventing circular references (parent_account_id != account_id). The data dictionary describes this as supporting portfolio aggregation where parent accounts (typ…

**System answer:**
> 

**Sources retrieved (10):** `parent_chunk_data_dictionary.md_7`, `parent_chunk_data_dictionary.md_12`, `ACCOUNTS→ACCOUNTS`, `Bank Account→ACCOUNTS`, `parent_chunk_data_dictionary.md_8`, `parent_chunk_data_dictionary.md_9`, `parent_chunk_data_dictionary.md_11`, `parent_chunk_business_glossary.md_0`

---

### ✅ 9 — What does the status 'Frozen' mean for a card?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0000 | **Gate:** `proceed`

**Expected answer:**
> The cards table has a status column with four states defined by CHECK constraint: Active, Frozen, Blocked, and Expired. The business glossary states that lost or stolen cards must be immediately blocked to prevent fraud, and that expired cards are automatically renewed. The glossary distinguishes Fr…

**System answer:**
> 

**Sources retrieved (10):** `parent_chunk_data_dictionary.md_7`, `parent_chunk_data_dictionary.md_10`, `parent_chunk_data_dictionary.md_11`, `Bank Card→CARDS`, `parent_chunk_data_dictionary.md_6`, `parent_chunk_data_dictionary.md_9`, `parent_chunk_business_glossary.md_0`, `parent_chunk_business_glossary.md_3`

---

### ✅ 10 — How does the transactions table track the impact of each transaction on account balances?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0000 | **Gate:** `proceed`

**Expected answer:**
> The transactions table includes a balance_after column (DECIMAL 15,2) that records the account balance after each transaction is applied. Combined with the amount column, transaction_type (Debit/Credit/Transfer/Payment/Withdrawal/Deposit/Fee), and status (Pending/Posted/Failed/Cancelled/OnHold), thi…

**System answer:**
> 

**Sources retrieved (10):** `parent_chunk_data_dictionary.md_9`, `TRANSACTIONS→ACCOUNTS`, `Account Transaction→TRANSACTIONS`, `parent_chunk_data_dictionary.md_7`, `ACCOUNTS→BRANCHES`, `ACCOUNTS→ACCOUNTS`, `Bank Account→ACCOUNTS`, `parent_chunk_data_dictionary.md_10`

---

### ✅ 11 — How does the customer_account junction table support multiple ownership types?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0000 | **Gate:** `proceed`

**Expected answer:**
> The customer_account table implements a many-to-many relationship between customers and accounts with a composite primary key (customer_id, account_id). It supports four relationship types via CHECK constraint: Owner, JointOwner, AuthorizedSigner, and Custodian. The is_primary flag designates the pr…

**System answer:**
> 

**Sources retrieved (10):** `parent_chunk_data_dictionary.md_8`, `Customer Account Relationship→CUSTOMER_ACCOUNT`, `parent_chunk_data_dictionary.md_12`, `CUSTOMER_ACCOUNT→CUSTOMERS`, `parent_chunk_data_dictionary.md_7`, `CUSTOMER_ACCOUNT→ACCOUNTS`, `parent_chunk_data_dictionary.md_9`, `parent_chunk_data_dictionary.md_11`

---

### ✅ 12 — What is the difference between current_balance and available_balance in the accounts table?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0000 | **Gate:** `proceed`

**Expected answer:**
> The accounts table tracks two separate balance fields: current_balance includes all transactions including pending ones, while available_balance excludes holds and pending transactions and represents what the customer can actually withdraw. The business glossary confirms this distinction, stating th…

**System answer:**
> 

**Sources retrieved (10):** `parent_chunk_data_dictionary.md_7`, `Bank Account→ACCOUNTS`, `parent_chunk_data_dictionary.md_10`, `Account Transaction→TRANSACTIONS`, `parent_chunk_data_dictionary.md_9`, `parent_chunk_business_glossary.md_0`, `parent_chunk_business_glossary.md_1`, `Bank Account`

---

### ✅ 13 — How are loans linked to both customers and accounts in the schema?

**Status:** GROUNDED  
**GT Coverage:** 83% | **Top Score:** 0.0000 | **Gate:** `proceed`

**Expected answer:**
> The loans table has a customer_id foreign key referencing the customers table (the borrower) and an optional account_id foreign key referencing the accounts table (for linked payment accounts). Each loan belongs to exactly one customer, and can optionally be connected to an account for automatic pay…

**System answer:**
> 

**Sources retrieved (10):** `parent_chunk_data_dictionary.md_12`, `LOANS→CUSTOMERS`, `LOANS→ACCOUNTS`, `parent_chunk_data_dictionary.md_10`, `CUSTOMER_ACCOUNT→CUSTOMERS`, `parent_chunk_data_dictionary.md_8`, `CUSTOMER_ACCOUNT→ACCOUNTS`, `Customer Account Relationship→CUSTOMER_ACCOUNT`

---

### ✅ 14 — What types of transactions does the system support and how does their status lifecycle work?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0000 | **Gate:** `proceed`

**Expected answer:**
> The transactions table supports seven transaction types via CHECK constraint: Debit, Credit, Transfer, Payment, Withdrawal, Deposit, and Fee. Each transaction also has a status lifecycle with five states: Pending (initial default), Posted (final), Failed, Cancelled, and OnHold. The business glossary…

**System answer:**
> 

**Sources retrieved (10):** `parent_chunk_data_dictionary.md_9`, `parent_chunk_data_dictionary.md_7`, `Account Transaction→TRANSACTIONS`, `Physical Banking Location→BRANCHES`, `parent_chunk_data_dictionary.md_6`, `parent_chunk_data_dictionary.md_11`, `parent_chunk_business_glossary.md_1`, `parent_chunk_business_glossary.md_3`

---

### ✅ 15 — How does the schema support joint account ownership between multiple customers?

**Status:** GROUNDED  
**GT Coverage:** 60% | **Top Score:** 0.0000 | **Gate:** `proceed`

**Expected answer:**
> Joint ownership is implemented through the customer_account junction table, which creates a many-to-many relationship between customers and accounts. Each row has a relationship_type CHECK constraint allowing Owner, JointOwner, AuthorizedSigner, or Custodian. The ownership_percentage field (DECIMAL …

**System answer:**
> 

**Sources retrieved (10):** `parent_chunk_data_dictionary.md_8`, `parent_chunk_data_dictionary.md_12`, `Customer Account Relationship→CUSTOMER_ACCOUNT`, `parent_chunk_data_dictionary.md_7`, `parent_chunk_data_dictionary.md_11`, `Customer Account Relationship`, `parent_chunk_business_glossary.md_0`, `parent_chunk_data_dictionary.md_4`

---

### ✅ 16 — What information does the cards table track and how are cards linked to customers and accounts?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0000 | **Gate:** `proceed`

**Expected answer:**
> The cards table links to both accounts (account_id FK) and customers (customer_id FK), tracking card_type (Debit/Credit/ATM), card_network (Visa/Mastercard/Discover/AmericanExpress), card_number, cardholder name, expiration_date, and CVV. For spending controls it stores credit_limit (nullable, for c…

**System answer:**
> 

**Sources retrieved (10):** `parent_chunk_data_dictionary.md_11`, `CARDS→CUSTOMERS`, `CARDS→ACCOUNTS`, `Bank Card→CARDS`, `Customer Account Relationship→CUSTOMER_ACCOUNT`, `parent_chunk_data_dictionary.md_10`, `CUSTOMER_ACCOUNT→CUSTOMERS`, `Customer Account Relationship`

---

### ✅ 17 — How does the schema handle interest rates across deposit and loan products?

**Status:** GROUNDED  
**GT Coverage:** 80% | **Top Score:** 0.0000 | **Gate:** `proceed`

**Expected answer:**
> Interest rates are stored differently for deposits and loans. The accounts table has an interest_rate column (nullable DECIMAL 5,4) and interest_earned for year-to-date tracking. The loans table has its own interest_rate column representing APR. The business glossary explains that APR (Annual Percen…

**System answer:**
> 

**Sources retrieved (10):** `parent_chunk_data_dictionary.md_12`, `parent_chunk_data_dictionary.md_10`, `parent_chunk_data_dictionary.md_7`, `Loan Agreement→LOANS`, `LOANS→CUSTOMERS`, `Bank Account→ACCOUNTS`, `parent_chunk_business_glossary.md_2`, `parent_chunk_business_glossary.md_0`

---

### ✅ 18 — What types of branches does the bank operate and how do they differ in capabilities?

**Status:** GROUNDED  
**GT Coverage:** 50% | **Top Score:** 0.0000 | **Gate:** `proceed`

**Expected answer:**
> The branches table supports three types via CHECK constraint: FullService, Satellite, and ATMOnly. The business glossary details each: FullService branches offer complete banking services including loan origination, financial advisors, and safe deposit boxes; Satellite branches have limited hours an…

**System answer:**
> 

**Sources retrieved (10):** `Physical Banking Location→BRANCHES`, `parent_chunk_data_dictionary.md_12`, `parent_chunk_data_dictionary.md_7`, `parent_chunk_data_dictionary.md_6`, `Atm→ATMS`, `parent_chunk_data_dictionary.md_5`, `parent_chunk_business_glossary.md_2`, `parent_chunk_business_glossary.md_3`

---

### ✅ 19 — How are ATMs related to branches in the schema and what types of ATMs exist?

**Status:** GROUNDED  
**GT Coverage:** 75% | **Top Score:** 0.0000 | **Gate:** `proceed`

**Expected answer:**
> The atms table has an optional branch_id foreign key referencing branches. When branch_id is NULL, the ATM is standalone and not affiliated with any branch. ATM types are defined by CHECK constraint: Branch (on-premises), DriveThrough (vehicle-accessible), and Standalone (independent locations). Eac…

**System answer:**
> 

**Sources retrieved (10):** `ATMS→BRANCHES`, `parent_chunk_data_dictionary.md_6`, `parent_chunk_data_dictionary.md_12`, `Atm→ATMS`, `Physical Banking Location→BRANCHES`, `parent_chunk_business_glossary.md_3`, `parent_chunk_data_dictionary.md_5`, `parent_chunk_business_glossary.md_2`

---

### ✅ 20 — What is the lifecycle of a loan from application to completion?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0000 | **Gate:** `proceed`

**Expected answer:**
> The loans table tracks loan status through five states defined by CHECK constraint: Pending (application submitted, default), Approved (credit approved but not yet funded), Active (loan funded and being repaid), PaidOff (fully repaid), and Defaulted (borrower failed to repay). Each loan records orig…

**System answer:**
> 

**Sources retrieved (10):** `parent_chunk_data_dictionary.md_10`, `parent_chunk_data_dictionary.md_7`, `Loan Agreement→LOANS`, `parent_chunk_data_dictionary.md_12`, `Physical Banking Location→BRANCHES`, `parent_chunk_business_glossary.md_2`, `parent_chunk_business_glossary.md_1`, `Loan Agreement`

---

### ✅ 21 — What does preferred customer status mean and how is it tracked in the schema?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0000 | **Gate:** `proceed`

**Expected answer:**
> Preferred status is tracked via the is_preferred boolean flag in the customers table (default: false). The business glossary states that preferred customers receive waived fees, preferred interest rates, and priority service. The glossary examples show preferred customers with longer tenure and high…

**System answer:**
> 

**Sources retrieved (10):** `Know Your Customer→CUSTOMERS`, `parent_chunk_data_dictionary.md_12`, `parent_chunk_data_dictionary.md_11`, `parent_chunk_data_dictionary.md_10`, `parent_chunk_data_dictionary.md_8`, `parent_chunk_data_dictionary.md_7`, `parent_chunk_data_dictionary.md_4`, `Know Your Customer`

---

### ✅ 22 — How does the accounts table support interest tracking and what business rules govern interest?

**Status:** GROUNDED  
**GT Coverage:** 50% | **Top Score:** 0.0000 | **Gate:** `proceed`

**Expected answer:**
> The accounts table has interest_rate (nullable DECIMAL for the annual rate) and interest_earned (DECIMAL for year-to-date interest credited). The business glossary states that deposit interest is credited monthly (typically the first day of the month) and that APY accounts for compounding effects. P…

**System answer:**
> 

**Sources retrieved (10):** `parent_chunk_data_dictionary.md_7`, `Bank Account→ACCOUNTS`, `parent_chunk_data_dictionary.md_12`, `parent_chunk_data_dictionary.md_10`, `ACCOUNTS→BRANCHES`, `ACCOUNTS→ACCOUNTS`, `parent_chunk_business_glossary.md_2`, `parent_chunk_business_glossary.md_0`

---

### ✅ 23 — Can an account exist without any customer linked to it?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0000 | **Gate:** `proceed`

**Expected answer:**
> Looking at the schema, there is no database-level constraint that forces every account to have a customer_account row. The accounts table has no direct foreign key to customers — the relationship is through the customer_account junction table with a composite primary key (customer_id, account_id). H…

**System answer:**
> 

**Sources retrieved (10):** `parent_chunk_data_dictionary.md_8`, `CUSTOMER_ACCOUNT→CUSTOMERS`, `parent_chunk_data_dictionary.md_12`, `CUSTOMER_ACCOUNT→ACCOUNTS`, `Customer Account Relationship→CUSTOMER_ACCOUNT`, `parent_chunk_data_dictionary.md_11`, `parent_chunk_data_dictionary.md_10`, `Customer Account Relationship`

---

### ✅ 24 — How does the schema handle failed or cancelled transactions?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0000 | **Gate:** `proceed`

**Expected answer:**
> The transactions table has a status column with CHECK constraint allowing Pending, Posted, Failed, Cancelled, and OnHold states. The business glossary explains that failed transactions are logged for audit but do not affect the account balance — the balance_after field would reflect no change. Poste…

**System answer:**
> 

**Sources retrieved (10):** `parent_chunk_data_dictionary.md_9`, `parent_chunk_data_dictionary.md_12`, `parent_chunk_data_dictionary.md_7`, `TRANSACTIONS→ACCOUNTS`, `Account Transaction→TRANSACTIONS`, `parent_chunk_business_glossary.md_1`, `parent_chunk_business_glossary.md_0`, `parent_chunk_business_glossary.md_3`

---

### ✅ 25 — What operational states can an ATM have and what do they mean for available services?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0000 | **Gate:** `proceed`

**Expected answer:**
> ATMs have three operational states defined by CHECK constraint: Operational (fully functional for all supported transactions), OutOfService (technical issue preventing all transactions), and OutOfCash (cash depleted, preventing withdrawals). The business glossary explains that cash replenishment is …

**System answer:**
> 

**Sources retrieved (10):** `parent_chunk_data_dictionary.md_6`, `Atm→ATMS`, `Physical Banking Location→BRANCHES`, `ATMS→BRANCHES`, `parent_chunk_data_dictionary.md_12`, `parent_chunk_business_glossary.md_3`, `parent_chunk_data_dictionary.md_5`, `parent_chunk_business_glossary.md_1`

---

## Anomalies & Observations

No anomalies detected. All questions grounded with acceptable RAGAS scores.
