# AB-01 — 02_intermediate_finance — Run Analysis

**Timestamp:** 2026-03-30 21:38:52  
**Run tag:** `v5`

## Configuration

| Parameter | Value |
|-----------|-------|
| Extraction model | `LLM (gpt-5.4-nano-2026-03-17)` |
| Reasoning model | `gpt-5.4-2026-03-05` |
| Embedding model | `BAAI/bge-m3` |
| Retrieval mode | `vector` |
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
| Avg Top Score | 0.0945 |
| Avg Chunk Count | 5.0 |
| Abstained | 0 |

## RAGAS Metrics

RAGAS evaluation not enabled for this run.

## Per-Question Deep Dive

### ✅ 1 — What is a checking account?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0040 | **Gate:** `proceed_with_warning`

**Expected answer:**
> A checking account is one of five account types (Checking, Savings, MoneyMarket, CD, Investment) defined by the CHECK constraint on the accounts table. According to the business glossary, accounts are financial arrangements for deposit, withdrawal, and management of funds. The schema tracks current_…

**System answer:**
> I cannot find a specific definition of “checking account” in the retrieved context.

What the context does show is that a checking account would fall under the broader Deposit Account concept, because the Deposit Account table is described as the core master record for bank deposit accounts and includes account number, type, subtype, balances, interest, fees, status, and lifecycle dates. So the kn…

**Sources retrieved (5):** `Deposit Account`, `Account Activity`, `Customer Account Relationship`, `Customer Master Data`, `Automated Teller Machine`

**Context previews (first 3):**

1. _Deposit Account: This table is the core master record for bank deposit accounts, with account number, type, subtype, balances, interest, fees, status, and lifecycle dates. The description explicitly s…_

2. _Account Activity: The table is explicitly a transaction fact table and its columns capture balance-affecting events tied to an account, including transaction_type, amount, transaction_date, status, an…_

3. _Customer Account Relationship: The DDL explicitly describes this as a junction table implementing a many-to-many relationship between customers and accounts, with relationship attributes like role, pr…_

---

### ✅ 2 — What is the difference between a savings account and a money market account?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0003 | **Gate:** `proceed_with_warning`

**Expected answer:**
> Both savings and money market are account types defined in the accounts table CHECK constraint. The business glossary Interest section provides example rates: Standard Savings earns 0.25% APY (with monthly compounding), Premium Savings earns 0.50% APY (with daily compounding), while Money Market ear…

**System answer:**
> From the retrieved context, I can only say that both would fall, if present, under the broader “Deposit Account” concept, which is described as the core master record for bank deposit accounts and includes account number, type, subtype, balances, interest, fees, status, and lifecycle dates.

However, the context does not mention “savings account” or “money market account” specifically, and it does…

**Sources retrieved (5):** `Deposit Account`, `Account Activity`, `Customer Account Relationship`, `Customer Master Data`, `Automated Teller Machine`

**Context previews (first 3):**

1. _Deposit Account: This table is the core master record for bank deposit accounts, with account number, type, subtype, balances, interest, fees, status, and lifecycle dates. The description explicitly s…_

2. _Account Activity: The table is explicitly a transaction fact table and its columns capture balance-affecting events tied to an account, including transaction_type, amount, transaction_date, status, an…_

3. _Customer Account Relationship: The DDL explicitly describes this as a junction table implementing a many-to-many relationship between customers and accounts, with relationship attributes like role, pr…_

---

### ✅ 3 — What is APR versus APY?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0002 | **Gate:** `proceed_with_warning`

**Expected answer:**
> APR (Annual Percentage Rate) is the annual cost of a loan including interest and fees, used for loan products. APY (Annual Percentage Yield) is the effective annual rate including compounding effects for deposit products. APY is higher than the nominal rate when compounding is more frequent than ann…

**System answer:**
> The retrieved context does not define APR or APY, so I cannot explain the difference between them from this knowledge graph alone.

What is known from the context is only that the Deposit Account concept includes interest-related attributes as part of the core master record for bank deposit accounts, along with balances, fees, status, and lifecycle dates. However, the context does not provide any …

**Sources retrieved (5):** `Automated Teller Machine`, `Account Activity`, `Customer Master Data`, `Customer Account Relationship`, `Deposit Account`

**Context previews (first 3):**

1. _Automated Teller Machine…_

2. _Account Activity: The table is explicitly a transaction fact table and its columns capture balance-affecting events tied to an account, including transaction_type, amount, transaction_date, status, an…_

3. _Customer Master Data: The table is explicitly described as the core customer dimension and contains identity, contact, KYC, risk, and preferred-flag attributes, which is characteristic of customer mas…_

---

### ✅ 4 — What is KYC Level 2?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0041 | **Gate:** `proceed_with_warning`

**Expected answer:**
> The customers table has a kyc_status column with a CHECK constraint allowing Level1, Level2, and Level3. The business glossary states that Level1 is the minimum requirement for account opening, Level3 is required for high-value accounts and international transfers, and risk_profile determines eligib…

**System answer:**
> The retrieved context does not define “KYC Level 2.” It only states that Customer Master Data contains KYC-related attributes as part of the core customer dimension. There is no description of KYC levels, their meanings, criteria, or allowed values in the provided context.

**Sources retrieved (5):** `Customer Master Data`, `Automated Teller Machine`, `Customer Account Relationship`, `Account Activity`, `Deposit Account`

**Context previews (first 3):**

1. _Customer Master Data: The table is explicitly described as the core customer dimension and contains identity, contact, KYC, risk, and preferred-flag attributes, which is characteristic of customer mas…_

2. _Automated Teller Machine…_

3. _Customer Account Relationship: The DDL explicitly describes this as a junction table implementing a many-to-many relationship between customers and accounts, with relationship attributes like role, pr…_

---

### ✅ 5 — How does the schema support different account subtypes and their varying requirements?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0626 | **Gate:** `proceed_with_warning`

**Expected answer:**
> The accounts table has an account_subtype column (VARCHAR 30, nullable) that stores values like Premium or Standard to differentiate within each account_type. Combined with the minimum_balance and monthly_fee columns, each account can have different requirements configured per subtype. The account_t…

**System answer:**
> The retrieved context shows that the schema supports subtype variation primarily through the Deposit Account table. It is described as the core master record for bank deposit accounts and explicitly includes both account type and account subtype, which indicates the model can distinguish broad product categories and finer-grained variants within them.

The same table also carries the operational a…

**Sources retrieved (5):** `Deposit Account`, `Customer Account Relationship`, `Account Activity`, `Customer Master Data`, `Automated Teller Machine`

**Context previews (first 3):**

1. _Deposit Account: This table is the core master record for bank deposit accounts, with account number, type, subtype, balances, interest, fees, status, and lifecycle dates. The description explicitly s…_

2. _Customer Account Relationship: The DDL explicitly describes this as a junction table implementing a many-to-many relationship between customers and accounts, with relationship attributes like role, pr…_

3. _Account Activity: The table is explicitly a transaction fact table and its columns capture balance-affecting events tied to an account, including transaction_type, amount, transaction_date, status, an…_

---

### ✅ 6 — What types of loan products does the bank offer?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0025 | **Gate:** `proceed_with_warning`

**Expected answer:**
> The bank offers five loan types defined by the CHECK constraint on loans.loan_type: (1) Mortgage — secured by real estate, glossary example shows $350,000 at 5.50% APR for 360 months; (2) Personal Loan — unsecured, example $15,000 at 8.50% APR for 48 months; (3) Auto Loan — secured by vehicle, examp…

**System answer:**
> The retrieved context does not describe any loan products. It only covers the business concepts Deposit Account, Customer Master Data, Customer Account Relationship, Account Activity, and Automated Teller Machine. Based on this context, I cannot determine what types of loan products the bank offers.

**Sources retrieved (5):** `Deposit Account`, `Customer Master Data`, `Customer Account Relationship`, `Account Activity`, `Automated Teller Machine`

**Context previews (first 3):**

1. _Deposit Account: This table is the core master record for bank deposit accounts, with account number, type, subtype, balances, interest, fees, status, and lifecycle dates. The description explicitly s…_

2. _Customer Master Data: The table is explicitly described as the core customer dimension and contains identity, contact, KYC, risk, and preferred-flag attributes, which is characteristic of customer mas…_

3. _Customer Account Relationship: The DDL explicitly describes this as a junction table implementing a many-to-many relationship between customers and accounts, with relationship attributes like role, pr…_

---

### ✅ 7 — What is the daily ATM withdrawal limit for standard customers?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0004 | **Gate:** `proceed_with_warning`

**Expected answer:**
> The cards table has an atm_daily_limit column with a default value of $500. The business glossary Card Examples confirm this: a standard Debit Card has a $500 ATM limit, while a Premium Debit card has a $2,000 ATM limit. The daily_limit column (default $3,000) controls POS spending separately. These…

**System answer:**
> I cannot determine the daily ATM withdrawal limit for standard customers from the retrieved context.

What the context does show is only high-level schema/business concept metadata: an Automated Teller Machine concept is present, and there are related concepts for Customer Master Data, Deposit Account, Customer Account Relationship, and Account Activity. However, no limit amounts, customer tier de…

**Sources retrieved (5):** `Customer Master Data`, `Customer Account Relationship`, `Deposit Account`, `Automated Teller Machine`, `Account Activity`

**Context previews (first 3):**

1. _Customer Master Data: The table is explicitly described as the core customer dimension and contains identity, contact, KYC, risk, and preferred-flag attributes, which is characteristic of customer mas…_

2. _Customer Account Relationship: The DDL explicitly describes this as a junction table implementing a many-to-many relationship between customers and accounts, with relationship attributes like role, pr…_

3. _Deposit Account: This table is the core master record for bank deposit accounts, with account number, type, subtype, balances, interest, fees, status, and lifecycle dates. The description explicitly s…_

---

### ✅ 8 — What is the difference between a parent account and a child account?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0001 | **Gate:** `proceed_with_warning`

**Expected answer:**
> The accounts table supports parent-child hierarchies through the parent_account_id self-referencing foreign key, with a CHECK constraint preventing circular references (parent_account_id != account_id). The data dictionary describes this as supporting portfolio aggregation where parent accounts (typ…

**System answer:**
> The retrieved context does not define the difference between a parent account and a child account.

What it does say is that the Deposit Account table is the core master record for bank deposit accounts and that it “supports deposit accounts with hierarchy.” From that, we can say only that the schema recognizes a hierarchical relationship among deposit accounts.

However, the context does not prov…

**Sources retrieved (5):** `Account Activity`, `Deposit Account`, `Customer Account Relationship`, `Customer Master Data`, `Automated Teller Machine`

**Context previews (first 3):**

1. _Account Activity: The table is explicitly a transaction fact table and its columns capture balance-affecting events tied to an account, including transaction_type, amount, transaction_date, status, an…_

2. _Deposit Account: This table is the core master record for bank deposit accounts, with account number, type, subtype, balances, interest, fees, status, and lifecycle dates. The description explicitly s…_

3. _Customer Account Relationship: The DDL explicitly describes this as a junction table implementing a many-to-many relationship between customers and accounts, with relationship attributes like role, pr…_

---

### ✅ 9 — What does the status 'Frozen' mean for a card?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0001 | **Gate:** `proceed_with_warning`

**Expected answer:**
> The cards table has a status column with four states defined by CHECK constraint: Active, Frozen, Blocked, and Expired. The business glossary states that lost or stolen cards must be immediately blocked to prevent fraud, and that expired cards are automatically renewed. The glossary distinguishes Fr…

**System answer:**
> The retrieved context does not define card statuses, and it does not mention a card entity at all. What is known is that the Deposit Account table includes a status field as part of the core master record for deposit accounts, and the Account Activity table also includes a status field for transactions. However, the context provides no status code definitions and no explanation of a card status va…

**Sources retrieved (5):** `Deposit Account`, `Account Activity`, `Customer Master Data`, `Customer Account Relationship`, `Automated Teller Machine`

**Context previews (first 3):**

1. _Deposit Account: This table is the core master record for bank deposit accounts, with account number, type, subtype, balances, interest, fees, status, and lifecycle dates. The description explicitly s…_

2. _Account Activity: The table is explicitly a transaction fact table and its columns capture balance-affecting events tied to an account, including transaction_type, amount, transaction_date, status, an…_

3. _Customer Master Data: The table is explicitly described as the core customer dimension and contains identity, contact, KYC, risk, and preferred-flag attributes, which is characteristic of customer mas…_

---

### ✅ 10 — How does the transactions table track the impact of each transaction on account balances?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.8058 | **Gate:** `proceed`

**Expected answer:**
> The transactions table includes a balance_after column (DECIMAL 15,2) that records the account balance after each transaction is applied. Combined with the amount column, transaction_type (Debit/Credit/Transfer/Payment/Withdrawal/Deposit/Fee), and status (Pending/Posted/Failed/Cancelled/OnHold), thi…

**System answer:**
> The transactions table is represented in the context as Account Activity. It tracks the impact of each transaction on an account balance because it is explicitly described as a transaction fact table for balance-affecting events tied to an account.

From the available context, the key columns involved are:
transaction_type, which identifies the kind of balance-affecting event;
amount, which captur…

**Sources retrieved (5):** `Account Activity`, `Deposit Account`, `Customer Account Relationship`, `Customer Master Data`, `Automated Teller Machine`

**Context previews (first 3):**

1. _Account Activity: The table is explicitly a transaction fact table and its columns capture balance-affecting events tied to an account, including transaction_type, amount, transaction_date, status, an…_

2. _Deposit Account: This table is the core master record for bank deposit accounts, with account number, type, subtype, balances, interest, fees, status, and lifecycle dates. The description explicitly s…_

3. _Customer Account Relationship: The DDL explicitly describes this as a junction table implementing a many-to-many relationship between customers and accounts, with relationship attributes like role, pr…_

---

### ✅ 11 — How does the customer_account junction table support multiple ownership types?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.7074 | **Gate:** `proceed`

**Expected answer:**
> The customer_account table implements a many-to-many relationship between customers and accounts with a composite primary key (customer_id, account_id). It supports four relationship types via CHECK constraint: Owner, JointOwner, AuthorizedSigner, and Custodian. The is_primary flag designates the pr…

**System answer:**
> The retrieved context does not list specific ownership types. What it does say is that the customer_account table is a junction table implementing a many-to-many relationship between customers and accounts. That structure allows one customer to be linked to multiple accounts and one account to be linked to multiple customers.

It supports different ownership arrangements through relationship-level…

**Sources retrieved (5):** `Customer Account Relationship`, `Deposit Account`, `Customer Master Data`, `Account Activity`, `Automated Teller Machine`

**Context previews (first 3):**

1. _Customer Account Relationship: The DDL explicitly describes this as a junction table implementing a many-to-many relationship between customers and accounts, with relationship attributes like role, pr…_

2. _Deposit Account: This table is the core master record for bank deposit accounts, with account number, type, subtype, balances, interest, fees, status, and lifecycle dates. The description explicitly s…_

3. _Customer Master Data: The table is explicitly described as the core customer dimension and contains identity, contact, KYC, risk, and preferred-flag attributes, which is characteristic of customer mas…_

---

### ✅ 12 — What is the difference between current_balance and available_balance in the accounts table?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0235 | **Gate:** `proceed_with_warning`

**Expected answer:**
> The accounts table tracks two separate balance fields: current_balance includes all transactions including pending ones, while available_balance excludes holds and pending transactions and represents what the customer can actually withdraw. The business glossary confirms this distinction, stating th…

**System answer:**
> I cannot determine the difference between current_balance and available_balance from the retrieved context.

The only relevant context is the Deposit Account concept, which says the table contains account number, type, subtype, balances, interest, fees, status, and lifecycle dates. However, it does not provide column-level definitions for current_balance or available_balance, so the distinction be…

**Sources retrieved (5):** `Account Activity`, `Deposit Account`, `Customer Master Data`, `Customer Account Relationship`, `Automated Teller Machine`

**Context previews (first 3):**

1. _Account Activity: The table is explicitly a transaction fact table and its columns capture balance-affecting events tied to an account, including transaction_type, amount, transaction_date, status, an…_

2. _Deposit Account: This table is the core master record for bank deposit accounts, with account number, type, subtype, balances, interest, fees, status, and lifecycle dates. The description explicitly s…_

3. _Customer Master Data: The table is explicitly described as the core customer dimension and contains identity, contact, KYC, risk, and preferred-flag attributes, which is characteristic of customer mas…_

---

### ✅ 13 — How are loans linked to both customers and accounts in the schema?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.1219 | **Gate:** `proceed_with_warning`

**Expected answer:**
> The loans table has a customer_id foreign key referencing the customers table (the borrower) and an optional account_id foreign key referencing the accounts table (for linked payment accounts). Each loan belongs to exactly one customer, and can optionally be connected to an account for automatic pay…

**System answer:**
> The retrieved context does not describe any loan table, loan concept, or any relationship linking loans to customers or accounts, so it is not possible to determine how loans are linked in the schema.

What is known from the context is that customers and accounts are linked through Customer Account Relationship, which is explicitly a many-to-many junction table between customers and accounts and i…

**Sources retrieved (5):** `Customer Account Relationship`, `Customer Master Data`, `Deposit Account`, `Account Activity`, `Automated Teller Machine`

**Context previews (first 3):**

1. _Customer Account Relationship: The DDL explicitly describes this as a junction table implementing a many-to-many relationship between customers and accounts, with relationship attributes like role, pr…_

2. _Customer Master Data: The table is explicitly described as the core customer dimension and contains identity, contact, KYC, risk, and preferred-flag attributes, which is characteristic of customer mas…_

3. _Deposit Account: This table is the core master record for bank deposit accounts, with account number, type, subtype, balances, interest, fees, status, and lifecycle dates. The description explicitly s…_

---

### ✅ 14 — What types of transactions does the system support and how does their status lifecycle work?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0504 | **Gate:** `proceed_with_warning`

**Expected answer:**
> The transactions table supports seven transaction types via CHECK constraint: Debit, Credit, Transfer, Payment, Withdrawal, Deposit, and Fee. Each transaction also has a status lifecycle with five states: Pending (initial default), Posted (final), Failed, Cancelled, and OnHold. The business glossary…

**System answer:**
> From the retrieved context, the system supports account-level, balance-affecting transactions through the Account Activity table. What is explicitly known is that each transaction record includes transaction_type, amount, transaction_date, status, and balance_after, and may also capture contextual details such as external_account and location.

However, the context does not enumerate the actual tr…

**Sources retrieved (5):** `Deposit Account`, `Account Activity`, `Customer Master Data`, `Customer Account Relationship`, `Automated Teller Machine`

**Context previews (first 3):**

1. _Deposit Account: This table is the core master record for bank deposit accounts, with account number, type, subtype, balances, interest, fees, status, and lifecycle dates. The description explicitly s…_

2. _Account Activity: The table is explicitly a transaction fact table and its columns capture balance-affecting events tied to an account, including transaction_type, amount, transaction_date, status, an…_

3. _Customer Master Data: The table is explicitly described as the core customer dimension and contains identity, contact, KYC, risk, and preferred-flag attributes, which is characteristic of customer mas…_

---

### ✅ 15 — How does the schema support joint account ownership between multiple customers?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0167 | **Gate:** `proceed_with_warning`

**Expected answer:**
> Joint ownership is implemented through the customer_account junction table, which creates a many-to-many relationship between customers and accounts. Each row has a relationship_type CHECK constraint allowing Owner, JointOwner, AuthorizedSigner, or Custodian. The ownership_percentage field (DECIMAL …

**System answer:**
> The schema supports joint account ownership through the Customer Account Relationship, which is explicitly described as a junction table implementing a many-to-many relationship between customers and accounts.

That means a single customer from Customer Master Data can be linked to multiple records in Deposit Account, and a single deposit account can be linked to multiple customers. This is the me…

**Sources retrieved (5):** `Customer Account Relationship`, `Deposit Account`, `Customer Master Data`, `Account Activity`, `Automated Teller Machine`

**Context previews (first 3):**

1. _Customer Account Relationship: The DDL explicitly describes this as a junction table implementing a many-to-many relationship between customers and accounts, with relationship attributes like role, pr…_

2. _Deposit Account: This table is the core master record for bank deposit accounts, with account number, type, subtype, balances, interest, fees, status, and lifecycle dates. The description explicitly s…_

3. _Customer Master Data: The table is explicitly described as the core customer dimension and contains identity, contact, KYC, risk, and preferred-flag attributes, which is characteristic of customer mas…_

---

### ✅ 16 — What information does the cards table track and how are cards linked to customers and accounts?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.3905 | **Gate:** `proceed`

**Expected answer:**
> The cards table links to both accounts (account_id FK) and customers (customer_id FK), tracking card_type (Debit/Credit/ATM), card_network (Visa/Mastercard/Discover/AmericanExpress), card_number, cardholder name, expiration_date, and CVV. For spending controls it stores credit_limit (nullable, for c…

**System answer:**
> The retrieved context does not mention a cards table, any card-related columns, or any direct card-to-customer or card-to-account relationship, so I cannot state what the cards table tracks or how cards are linked specifically.

What the context does provide is the customer-to-account linkage model. The Customer Account Relationship concept is explicitly described as a junction table that implemen…

**Sources retrieved (5):** `Customer Account Relationship`, `Customer Master Data`, `Account Activity`, `Deposit Account`, `Automated Teller Machine`

**Context previews (first 3):**

1. _Customer Account Relationship: The DDL explicitly describes this as a junction table implementing a many-to-many relationship between customers and accounts, with relationship attributes like role, pr…_

2. _Customer Master Data: The table is explicitly described as the core customer dimension and contains identity, contact, KYC, risk, and preferred-flag attributes, which is characteristic of customer mas…_

3. _Account Activity: The table is explicitly a transaction fact table and its columns capture balance-affecting events tied to an account, including transaction_type, amount, transaction_date, status, an…_

---

### ✅ 17 — How does the schema handle interest rates across deposit and loan products?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0034 | **Gate:** `proceed_with_warning`

**Expected answer:**
> Interest rates are stored differently for deposits and loans. The accounts table has an interest_rate column (nullable DECIMAL 5,4) and interest_earned for year-to-date tracking. The loans table has its own interest_rate column representing APR. The business glossary explains that APR (Annual Percen…

**System answer:**
> From the retrieved context, only the deposit side is covered. The Deposit Account table is described as the core master record for bank deposit accounts, and it includes interest along with account number, type, subtype, balances, fees, status, and lifecycle dates. That indicates the schema stores some interest-related information directly on deposit accounts.

The context does not include any loa…

**Sources retrieved (5):** `Deposit Account`, `Customer Master Data`, `Customer Account Relationship`, `Account Activity`, `Automated Teller Machine`

**Context previews (first 3):**

1. _Deposit Account: This table is the core master record for bank deposit accounts, with account number, type, subtype, balances, interest, fees, status, and lifecycle dates. The description explicitly s…_

2. _Customer Master Data: The table is explicitly described as the core customer dimension and contains identity, contact, KYC, risk, and preferred-flag attributes, which is characteristic of customer mas…_

3. _Customer Account Relationship: The DDL explicitly describes this as a junction table implementing a many-to-many relationship between customers and accounts, with relationship attributes like role, pr…_

---

### ✅ 18 — What types of branches does the bank operate and how do they differ in capabilities?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0003 | **Gate:** `proceed_with_warning`

**Expected answer:**
> The branches table supports three types via CHECK constraint: FullService, Satellite, and ATMOnly. The business glossary details each: FullService branches offer complete banking services including loan origination, financial advisors, and safe deposit boxes; Satellite branches have limited hours an…

**System answer:**
> The retrieved context does not describe any bank branch types or their capabilities.

It only contains schema/business-concept information for Customer Master Data, Deposit Account, Customer Account Relationship, Account Activity, and a mention of Automated Teller Machine. There is no information about branch categories, operating models, or how different branches differ in capability.

**Sources retrieved (5):** `Customer Master Data`, `Deposit Account`, `Customer Account Relationship`, `Account Activity`, `Automated Teller Machine`

**Context previews (first 3):**

1. _Customer Master Data: The table is explicitly described as the core customer dimension and contains identity, contact, KYC, risk, and preferred-flag attributes, which is characteristic of customer mas…_

2. _Deposit Account: This table is the core master record for bank deposit accounts, with account number, type, subtype, balances, interest, fees, status, and lifecycle dates. The description explicitly s…_

3. _Customer Account Relationship: The DDL explicitly describes this as a junction table implementing a many-to-many relationship between customers and accounts, with relationship attributes like role, pr…_

---

### ✅ 19 — How are ATMs related to branches in the schema and what types of ATMs exist?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0011 | **Gate:** `proceed_with_warning`

**Expected answer:**
> The atms table has an optional branch_id foreign key referencing branches. When branch_id is NULL, the ATM is standalone and not affiliated with any branch. ATM types are defined by CHECK constraint: Branch (on-premises), DriveThrough (vehicle-accessible), and Standalone (independent locations). Eac…

**System answer:**
> From the retrieved context, I can only determine that “Automated Teller Machine” exists as a business concept.

The context does not provide any schema details showing how ATMs relate to branches. It also does not list any ATM types. There are no table definitions, columns, keys, or relationship descriptions for ATM or branch in the provided context, so the branch linkage and ATM type classificati…

**Sources retrieved (5):** `Deposit Account`, `Customer Master Data`, `Customer Account Relationship`, `Account Activity`, `Automated Teller Machine`

**Context previews (first 3):**

1. _Deposit Account: This table is the core master record for bank deposit accounts, with account number, type, subtype, balances, interest, fees, status, and lifecycle dates. The description explicitly s…_

2. _Customer Master Data: The table is explicitly described as the core customer dimension and contains identity, contact, KYC, risk, and preferred-flag attributes, which is characteristic of customer mas…_

3. _Customer Account Relationship: The DDL explicitly describes this as a junction table implementing a many-to-many relationship between customers and accounts, with relationship attributes like role, pr…_

---

### ✅ 20 — What is the lifecycle of a loan from application to completion?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0024 | **Gate:** `proceed_with_warning`

**Expected answer:**
> The loans table tracks loan status through five states defined by CHECK constraint: Pending (application submitted, default), Approved (credit approved but not yet funded), Active (loan funded and being repaid), PaidOff (fully repaid), and Defaulted (borrower failed to repay). Each loan records orig…

**System answer:**
> I cannot determine the lifecycle of a loan from application to completion from the retrieved context.

What the context does contain is schema-level information for deposit banking, not loans: a Deposit Account master record with status and lifecycle dates, Customer Master Data, a Customer Account Relationship junction table, Account Activity as a transaction fact table, and an Automated Teller Ma…

**Sources retrieved (5):** `Deposit Account`, `Customer Master Data`, `Customer Account Relationship`, `Account Activity`, `Automated Teller Machine`

**Context previews (first 3):**

1. _Deposit Account: This table is the core master record for bank deposit accounts, with account number, type, subtype, balances, interest, fees, status, and lifecycle dates. The description explicitly s…_

2. _Customer Master Data: The table is explicitly described as the core customer dimension and contains identity, contact, KYC, risk, and preferred-flag attributes, which is characteristic of customer mas…_

3. _Customer Account Relationship: The DDL explicitly describes this as a junction table implementing a many-to-many relationship between customers and accounts, with relationship attributes like role, pr…_

---

### ✅ 21 — What does preferred customer status mean and how is it tracked in the schema?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0188 | **Gate:** `proceed_with_warning`

**Expected answer:**
> Preferred status is tracked via the is_preferred boolean flag in the customers table (default: false). The business glossary states that preferred customers receive waived fees, preferred interest rates, and priority service. The glossary examples show preferred customers with longer tenure and high…

**System answer:**
> From the retrieved context, “preferred customer status” is only evidenced as a preferred-flag attribute in Customer Master Data. The context does not define what “preferred” means in business terms, and it does not provide any eligibility rules, operational criteria, lifecycle rules, or downstream effects of that status.

What can be said is that Customer Master Data is described as the core custo…

**Sources retrieved (5):** `Customer Master Data`, `Customer Account Relationship`, `Account Activity`, `Deposit Account`, `Automated Teller Machine`

**Context previews (first 3):**

1. _Customer Master Data: The table is explicitly described as the core customer dimension and contains identity, contact, KYC, risk, and preferred-flag attributes, which is characteristic of customer mas…_

2. _Customer Account Relationship: The DDL explicitly describes this as a junction table implementing a many-to-many relationship between customers and accounts, with relationship attributes like role, pr…_

3. _Account Activity: The table is explicitly a transaction fact table and its columns capture balance-affecting events tied to an account, including transaction_type, amount, transaction_date, status, an…_

---

### ✅ 22 — How does the accounts table support interest tracking and what business rules govern interest?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0578 | **Gate:** `proceed_with_warning`

**Expected answer:**
> The accounts table has interest_rate (nullable DECIMAL for the annual rate) and interest_earned (DECIMAL for year-to-date interest credited). The business glossary states that deposit interest is credited monthly (typically the first day of the month) and that APY accounts for compounding effects. P…

**System answer:**
> The retrieved context indicates that the relevant accounts table is Deposit Account. It supports interest tracking at the schema level because the table includes interest-related data as part of the core master record for deposit accounts, alongside account number, type, subtype, balances, fees, status, and lifecycle dates. This means interest is stored as an account-level attribute within the dep…

**Sources retrieved (5):** `Deposit Account`, `Account Activity`, `Customer Account Relationship`, `Customer Master Data`, `Automated Teller Machine`

**Context previews (first 3):**

1. _Deposit Account: This table is the core master record for bank deposit accounts, with account number, type, subtype, balances, interest, fees, status, and lifecycle dates. The description explicitly s…_

2. _Account Activity: The table is explicitly a transaction fact table and its columns capture balance-affecting events tied to an account, including transaction_type, amount, transaction_date, status, an…_

3. _Customer Account Relationship: The DDL explicitly describes this as a junction table implementing a many-to-many relationship between customers and accounts, with relationship attributes like role, pr…_

---

### ✅ 23 — Can an account exist without any customer linked to it?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0879 | **Gate:** `proceed_with_warning`

**Expected answer:**
> Looking at the schema, there is no database-level constraint that forces every account to have a customer_account row. The accounts table has no direct foreign key to customers — the relationship is through the customer_account junction table with a composite primary key (customer_id, account_id). H…

**System answer:**
> From the retrieved context, a customer-to-account link is stored in a separate junction table, Customer Account Relationship, which implements a many-to-many relationship between customers and accounts and holds attributes such as role, primary flag, ownership percentage, and link dates. The account itself is stored in Deposit Account as the core master record for bank deposit accounts.

That mean…

**Sources retrieved (5):** `Customer Account Relationship`, `Customer Master Data`, `Account Activity`, `Deposit Account`, `Automated Teller Machine`

**Context previews (first 3):**

1. _Customer Account Relationship: The DDL explicitly describes this as a junction table implementing a many-to-many relationship between customers and accounts, with relationship attributes like role, pr…_

2. _Customer Master Data: The table is explicitly described as the core customer dimension and contains identity, contact, KYC, risk, and preferred-flag attributes, which is characteristic of customer mas…_

3. _Account Activity: The table is explicitly a transaction fact table and its columns capture balance-affecting events tied to an account, including transaction_type, amount, transaction_date, status, an…_

---

### ✅ 24 — How does the schema handle failed or cancelled transactions?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0006 | **Gate:** `proceed_with_warning`

**Expected answer:**
> The transactions table has a status column with CHECK constraint allowing Pending, Posted, Failed, Cancelled, and OnHold states. The business glossary explains that failed transactions are logged for audit but do not affect the account balance — the balance_after field would reflect no change. Poste…

**System answer:**
> The retrieved context does not describe any explicit handling rules for failed or cancelled transactions.

What it does say is that the Account Activity table is a transaction fact table for balance-affecting account events, and it includes a status column along with transaction_type, amount, transaction_date, and balance_after. So, at the schema level, transaction status is captured in Account Ac…

**Sources retrieved (5):** `Account Activity`, `Customer Master Data`, `Deposit Account`, `Customer Account Relationship`, `Automated Teller Machine`

**Context previews (first 3):**

1. _Account Activity: The table is explicitly a transaction fact table and its columns capture balance-affecting events tied to an account, including transaction_type, amount, transaction_date, status, an…_

2. _Customer Master Data: The table is explicitly described as the core customer dimension and contains identity, contact, KYC, risk, and preferred-flag attributes, which is characteristic of customer mas…_

3. _Deposit Account: This table is the core master record for bank deposit accounts, with account number, type, subtype, balances, interest, fees, status, and lifecycle dates. The description explicitly s…_

---

### ✅ 25 — What operational states can an ATM have and what do they mean for available services?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0007 | **Gate:** `proceed_with_warning`

**Expected answer:**
> ATMs have three operational states defined by CHECK constraint: Operational (fully functional for all supported transactions), OutOfService (technical issue preventing all transactions), and OutOfCash (cash depleted, preventing withdrawals). The business glossary explains that cash replenishment is …

**System answer:**
> From the retrieved context, only the business concept name "Automated Teller Machine" is present. The context does not provide any ATM operational states, status values, or descriptions of how those states affect available services.

So, what can be stated from the context is only that ATM exists as a business concept. What cannot be determined from the context are:
the possible operational states…

**Sources retrieved (5):** `Customer Master Data`, `Account Activity`, `Customer Account Relationship`, `Deposit Account`, `Automated Teller Machine`

**Context previews (first 3):**

1. _Customer Master Data: The table is explicitly described as the core customer dimension and contains identity, contact, KYC, risk, and preferred-flag attributes, which is characteristic of customer mas…_

2. _Account Activity: The table is explicitly a transaction fact table and its columns capture balance-affecting events tied to an account, including transaction_type, amount, transaction_date, status, an…_

3. _Customer Account Relationship: The DDL explicitly describes this as a junction table implementing a many-to-many relationship between customers and accounts, with relationship attributes like role, pr…_

---

## Anomalies & Observations

No anomalies detected. All questions grounded with acceptable RAGAS scores.
