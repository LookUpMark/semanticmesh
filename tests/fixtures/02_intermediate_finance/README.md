# 02_intermediate_finance Dataset

## Domain Overview
**Banking & Finance** - Intermediate complexity dataset focusing on core banking operations, customer account management, and transaction processing.

## Complexity Level: Intermediate
- **8 Core Concepts**: Account, Customer, Transaction, Loan, Interest, Branch, ATM, Card
- **6 Database Tables** with realistic banking relationships
- **Junction Tables**: Many-to-many relationships (Customer ↔ Account)
- **Self-References**: Account hierarchy (parent-child accounts)
- **Calculated Columns**: Interest computations, balance calculations
- **25 QA Pairs**: Testing direct mapping, multi-hop queries, attribute lookups, and negative cases

## Business Domain
This dataset models a **retail banking system** with the following key entities:

### Core Concepts
1. **Account**: Deposit accounts (savings, checking), investment accounts, with hierarchical relationships
2. **Customer**: Bank customers with personal information, KYC status, and risk profiles
3. **Transaction**: Financial transactions including transfers, payments, withdrawals, and deposits
4. **Loan**: Credit products including mortgages, personal loans, and lines of credit
5. **Interest**: Interest rates, APY, calculations for savings and loan products
6. **Branch**: Physical bank locations with services, hours, and staff
7. **ATM**: Automated teller machines with location, status, and capabilities
8. **Card**: Debit and credit cards linked to accounts with security features

### Schema Features
- **Many-to-Many**: Customers can have multiple accounts; accounts can have multiple joint owners
- **Account Hierarchy**: Parent-child relationships for sub-accounts and portfolio grouping
- **Transaction Types**: Debit, credit, transfer, payment, withdrawal, deposit, fee
- **Loan Management**: Application, approval, disbursement, repayment tracking
- **Interest Calculation**: Compound interest, tiered rates, promotional rates
- **Branch Services**: Full-service branches, satellite locations, ATM-only locations
- **Card Security**: CVV, PIN, chip technology, contactless payments

## Files Included
1. **business_glossary.pdf** - Banking terminology, product definitions, business rules
2. **data_dictionary.pdf** - Technical schema documentation, column descriptions, relationships
3. **schema.sql** - DDL with 6 tables, constraints, indexes, and sample data
4. **gold_standard.json** - 25 QA pairs for evaluation

## Query Patterns Tested
- **Direct Mapping**: Basic concept lookups (e.g., "What is a checking account?")
- **Multi-Hop Queries**: Customer → Accounts → Transactions (2-3 hops)
- **Multi-Hop Queries**: Branch → Accounts → Customers (reverse navigation)
- **Attribute Lookup**: Interest rates, balances, transaction limits
- **Negative Cases**: Accounts without customers, cancelled transactions, rejected loans
- **Aggregation**: Total balances, transaction counts, average interest rates
- **Temporal Queries**: Transaction history, loan maturity dates, card expiry

## Difficulty Factors
- **Junction Table Navigation**: Must traverse customer_account link table
- **Self-Reference Handling**: Account hierarchy requires recursive queries
- **Calculated Fields**: Interest computations, balance aggregations
- **Multiple Pathways**: Same entity reachable via different routes
- **Business Logic**: Understanding banking concepts (APY vs APR, holds, clearing)
- **Edge Cases**: Dormant accounts, closed loans, lost cards, inactive ATMs

## Use Cases
This dataset tests the RAG system's ability to:
- Navigate many-to-many relationships through junction tables
- Handle hierarchical data structures (account trees)
- Understand financial terminology and calculations
- Trace transaction flows across accounts
- Resolve ambiguous terms (e.g., "balance" vs "available balance")
- Handle negative and missing data appropriately
