# 02_intermediate_finance Dataset - Creation Summary

## Overview
Successfully created the 02_intermediate_finance dataset for banking & finance domain testing.

## Files Created (5 files)

### 1. README.md (3.8 KB)
- Dataset overview and complexity explanation
- 8 core concepts documented
- Query patterns tested
- Difficulty factors explained

### 2. business_glossary.pdf (24 KB)
- 9 comprehensive sections covering banking terminology
- Account products (checking, savings, money market, CDs)
- Customer classification (KYC levels, risk profiles)
- Transaction types and processing rules
- Loan products (mortgage, personal, auto, HELOC)
- Interest calculations (APR vs APY, compounding)
- Branch network services
- ATM functionality
- Card products and security
- Banking operations and fees
- Regulatory requirements

### 3. data_dictionary.pdf (61 KB)
- Complete schema documentation for 8 tables
- Detailed column specifications
- Index definitions
- Relationship mappings
- Business rules per table
- Relationship diagram

### 4. schema.sql (29 KB)
- Complete DDL for 8 tables
- Foreign key constraints
- Check constraints for enums
- Indexes for performance
- Sample data for all tables:
  - 10 customers
  - 17 accounts (with parent-child hierarchy)
  - 24 customer_account relationships (junction table)
  - 24 transactions
  - 10 loans
  - 5 branches
  - 7 ATMs
  - 12 cards

### 5. gold_standard.json (17 KB)
- 25 comprehensive QA pairs
- Category breakdown:
  - Direct Mapping: 10 questions
  - Multi-hop: 12 questions
  - Negative: 3 questions
- Difficulty distribution:
  - Easy: 10 questions
  - Medium: 13 questions
  - Hard: 2 questions
- Entity coverage across all 8 concepts

## Dataset Characteristics

### Schema Complexity
- **8 tables**: customers, accounts, customer_account, transactions, loans, branches, atms, cards
- **Junction table**: customer_account (many-to-many customers ↔ accounts)
- **Self-reference**: accounts.parent_account_id (account hierarchy)
- **Calculated columns**: interest_earned, balance_after, ownership_percentage

### Data Distribution
- 10 customers with varying KYC levels and risk profiles
- 17 accounts including checking, savings, money market, CDs, and investment portfolios
- 2 parent-child account hierarchies (PORT-001 and PORT-002)
- 24 transactions covering debits, credits, withdrawals, deposits, transfers, and fees
- 10 loans including mortgages, personal loans, auto loans, HELOC, and credit cards
- 5 branches (3 full-service, 1 satellite, 1 ATM-only)
- 7 ATMs (branch and standalone)
- 12 cards (debit, credit, and ATM cards)

### Query Patterns Tested
1. **Direct Mapping**: Basic concept lookups (10 questions)
2. **Multi-hop**: Customer → Accounts → Transactions (12 questions)
3. **Negative Cases**: Failed transactions, out-of-service ATMs (3 questions)

### Key Features
- Realistic banking terminology and workflows
- Joint ownership scenarios (50/50 splits)
- Account hierarchies with parent-child relationships
- Various transaction statuses (Pending, Posted, Failed, Cancelled)
- Multiple card types and statuses
- Loan lifecycle representation (Active, PaidOff)
- Branch and ATM operational statuses
- Interest calculations with tiered rates
- Regulatory compliance (KYC levels, Regulation D)

## Verification
- SQL syntax validated successfully
- All foreign key constraints satisfied
- Sample data inserted correctly:
  - 10 customers
  - 17 accounts
  - 24 customer_account junction records
  - 24 transactions
  - 10 loans
  - 5 branches
  - 7 ATMs
  - 12 cards

## Usage
This dataset is designed to test RAG systems on:
- Navigating many-to-many relationships via junction tables
- Understanding financial terminology and calculations
- Tracing transaction flows across accounts
- Handling hierarchical data structures
- Processing negative and missing data
- Multi-hop queries across 3+ tables
- Attribute lookups with calculated fields
