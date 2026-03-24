# Dataset 06: Edge Cases - Legacy System Migration

## Overview
This dataset tests a Knowledge Graph construction system's ability to handle real-world legacy database schemas with numerous anti-patterns, naming inconsistencies, and data quality issues commonly found in production systems undergoing migration.

## Domain
E-commerce legacy system (CustomerMaster v3.2.1) - circa 2008-2015

## Purpose
Test the system's robustness against:
- Hungarian notation prefixes
- SQL reserved words as identifiers
- Inappropriate data types
- Inconsistent naming conventions
- Abbreviated column names
- Misleading table prefixes
- Denormalized redundant fields
- Security anti-patterns
- Deprecated fields coexisting with current fields

## Files

### 01_schema.sql
**DDL file** defining 10 tables with authentic legacy anti-patterns:

**Tables:**
1. `tblCustomer` - Customer master (Hungarian notation, wrong ID type)
2. `tblProduct` - Product catalog (deprecated fields, wrong cost type)
3. `vw_SalesOrderHdr` - Order headers (misleading vw_ prefix, it's a table)
4. `ord_line_item` - Order line items (abbreviated naming, redundant fields)
5. `inv_txn_log` - Inventory transactions (heavily abbreviated names)
6. `Group` - Product categories (SQL reserved word)
7. `User` - System users (SQL reserved word, security issues)
8. `tblOrderStatusHistory` - Order status audit (verbose naming)
9. `tblShippingCarrier` - Shipping methods (Hungarian notation)
10. `tblPayment` - Payment records (security violation)

**Anti-Patterns Demonstrated:**
- Table prefixes: `tbl_`, `vw_`, `ord_`, `inv_`, no prefix
- Hungarian notation: `str`, `int`, `lng`, `flt`, `bol`, `dtm`
- Reserved words: `Group`, `User`
- Wrong types: VARCHAR for IDs, VARCHAR for money
- Mixed conventions within same schema
- Abbreviated names: `txn_id`, `txn_dt`, `prod_id`
- Redundant denormalized fields
- Security violations (plaintext card numbers)

### 02_data_dictionary.txt
**Comprehensive data dictionary** documenting:
- Field specifications for all 10 tables
- Business rules and constraints
- Legacy naming conventions explanation
- Data quality issues identified
- Migration notes and recommendations
- Security and compliance violations
- Performance concerns

### 03_business_glossary.pdf.md
**Business glossary** (in PDF-like markdown format) covering:
- Core business entities (Customer, Order, Product, Line Item, etc.)
- Domain-specific terminology (Backorder, Fulfillment, Authorization)
- Status workflow definitions
- Legacy system quirks explanation
- Cross-reference table relationships
- Migration priority guidelines
- Data quality issues summary

### gold_standard.json
**25 QA pairs** testing edge case handling:

| ID | Edge Case Tested | Question Focus |
|----|------------------|----------------|
| 1-2 | Hungarian notation | Customer table structure and ID handling |
| 3 | Misleading prefix | vw_SalesOrderHdr is a table, not view |
| 4 | Reserved words | Group and User table names |
| 5 | Misleading notation | intCustID is VARCHAR, not INT |
| 6 | Abbreviated names | inv_txn_log heavily abbreviated fields |
| 7 | Wrong data type | unit_cost is VARCHAR, should be DECIMAL |
| 8 | Denormalization | Redundant product data in line items |
| 9 | Check constraints | Order status enum values |
| 10 | Security violation | Plaintext card numbers in tblPayment |
| 11 | Hungarian notation | bolActive boolean flag usage |
| 12 | Abbreviated codes | Inventory transaction types (IN/OUT/ADJ) |
| 13 | Self-reference | Group table hierarchical structure |
| 14 | Migration fields | Old and new columns coexisting |
| 15 | Audit trail | Order status history tracking |
| 16 | Mixed conventions | Inconsistent naming across tables |
| 17 | Deprecated fields | Legacy fields in tblProduct |
| 18 | Template values | Tracking URL with placeholders |
| 19 | Security + reserved word | User table password hashing issues |
| 20 | Misleading notation | flt prefix for DECIMAL fields |
| 21 | Date conventions | dtm vs dt vs Date inconsistency |
| 22 | Multiple prefixes | Table naming pattern analysis |
| 23 | Foreign keys | Explicit and implicit relationships |
| 24 | Formatted values | SKU format and uniqueness |
| 25 | Critical issues | Summary of data quality problems |

## Anti-Patterns Catalog

### 1. Hungarian Notation
**Pattern:** Type encoding in variable names
- `str` = string (VARCHAR)
- `int` = integer (INT)
- `lng` = long integer (INT)
- `flt` = float/money (DECIMAL)
- `bol` = boolean (BIT)
- `dtm` = datetime (DATETIME)

**Problem:** Type can change without name update, misleading prefixes

**Examples:**
- `intCustID` is actually VARCHAR(50)
- `fltPrice` is DECIMAL, not FLOAT
- `lngOrderID` is regular INT, not "long"

### 2. Table Prefix Inconsistency
**Pattern:** Multiple naming conventions in same schema
- `tblCustomer`, `tblProduct` - tbl prefix
- `vw_SalesOrderHdr` - vw prefix (but it's a table!)
- `ord_line_item` - domain prefix
- `inv_txn_log` - domain prefix
- `Group`, `User` - no prefix (reserved words)

**Problem:** No consistency, difficult to query programmatically

### 3. SQL Reserved Words
**Pattern:** Using reserved words as identifiers
- `Group` - table name (requires [Group] or "Group")
- `User` - table name (requires [User] or "User")

**Problem:** Requires quoting in queries, syntax errors

### 4. Inappropriate Data Types
**Pattern:** Using wrong types for data
- `strCustID` VARCHAR(50) - should be INT
- `tblProduct.unit_cost` VARCHAR(20) - should be DECIMAL
- `tblPayment.CardNumberText` VARCHAR(100) - should be tokenized

**Problem:** Cannot perform calculations, security risk

### 5. Abbreviated Names
**Pattern:** Heavy abbreviation reducing readability
- `txn_id` - transaction_id
- `txn_dt` - transaction_date
- `txn_type` - transaction_type
- `prod_id` - product_id
- `cust_nm` - customer_name (in queries, not schema)

**Problem:** Ambiguous, difficult for new developers

### 6. Denormalized Redundant Fields
**Pattern:** Copying data across tables for "performance"
- `ord_line_item.product_code` - copies `tblProduct.strSKU`
- `ord_line_item.item_name` - copies product name snapshot

**Problem:** Data inconsistency risk, update overhead

### 7. Misleading Prefixes
**Pattern:** Prefix suggests wrong structure
- `vw_SalesOrderHdr` - suggests view but is table
- `intCustID` - suggests integer but is VARCHAR
- `fltPrice` - suggests float but is DECIMAL

**Problem:** Developer confusion, incorrect assumptions

### 8. Coexisting Deprecated Fields
**Pattern:** Old and new fields both present
- `tblProduct.strSKU` (current) vs `prod_num` (deprecated)
- `tblProduct.strDescription` (current) vs `item_desc` (deprecated)
- `tblCustomer.strCustID` (legacy) vs `cust_id` (new)

**Problem:** Unclear which to use, migration complexity

### 9. Security Anti-Patterns
**Pattern:** Storing sensitive data inappropriately
- `CardNumberText` - plaintext card numbers
- `PasswordHash` - unsalted SHA-256

**Problem:** PCI compliance violation, security risk

### 10. Inconsistent Case
**Pattern:** Mixed case conventions
- `CustomerMaster` (PascalCase) - in documentation
- `tblCustomer` (lowercase with prefix) - in schema
- `ord_line_item` (snake_case) - in schema

**Problem:** Difficult to reference correctly

## Usage in Testing

### Knowledge Graph Construction
This dataset tests the system's ability to:

1. **Extract entities despite naming noise**
   - Recognize `tblCustomer` and `Customer` as same entity
   - Map `intCustID` to customer identifier despite misleading prefix
   - Handle abbreviated names (`txn_id`) vs full names

2. **Handle reserved words correctly**
   - Escape `Group` and `User` in generated Cypher
   - Prevent syntax errors in queries
   - Maintain readability in graph labels

3. **Infer correct semantics from bad types**
   - Understand `strCustID` functions as primary key despite VARCHAR
   - Recognize `unit_cost` as monetary field despite wrong type
   - Handle relationships with type mismatches

4. **Resolve deprecated vs current fields**
   - Prioritize current fields (`strSKU`) over deprecated (`prod_num`)
   - Handle migration compatibility fields (`cust_id` alongside `strCustID`)
   - Understand historical context for redundant fields

5. **Maintain data quality awareness**
   - Flag security violations (plaintext card numbers)
   - Identify missing foreign key constraints
   - Note misleading prefixes in documentation

### Evaluation Metrics
When evaluating on this dataset:

1. **Entity Extraction Accuracy**
   - Correct identification of all 10 tables
   - Proper handling of reserved word table names
   - Recognition of entities despite prefix noise

2. **Relationship Extraction**
   - Correct FK relationships despite type mismatches
   - Handling of implicit relationships (not enforced by FK)
   - Recognition of self-referencing relationships

3. **Semantic Understanding**
   - Correct mapping of abbreviated names to concepts
   - Distinguishing deprecated from current fields
   - Understanding business rules from constraints

4. **Query Generation**
   - Proper escaping of reserved words in Cypher
   - Correct handling of misleading prefixes
   - Safe queries despite schema anti-patterns

## Integration with Test Suite

### pytest Example
```python
import pytest
from src.extraction.triplet_extractor import extract_triplets
from src.ingestion.ddl_parser import parse_ddl

@pytest.mark.integration
def test_legacy_schema_triplet_extraction():
    """Test triplet extraction from legacy schema with anti-patterns"""
    ddl_path = "tests/fixtures/06_edgecases_legacy/01_schema.sql"
    schema = parse_ddl(ddl_path)

    triplets = extract_triplets(schema)

    # Should extract entities despite naming issues
    assert any(t.entity == "tblCustomer" for t in triplets)
    assert any(t.entity == "vw_SalesOrderHdr" for t in triplets)
    assert any(t.entity == "Group" for t in triplets)  # Reserved word
    assert any(t.entity == "User" for t in triplets)   # Reserved word

    # Should handle misleading prefixes
    assert any("intCustID" in t.description for t in triplets)

    # Should recognize relationships despite type mismatches
    assert any(
        t.subject == "vw_SalesOrderHdr" and
        t.object == "tblCustomer"
        for t in triplets
    )
```

### RAGAS Evaluation
```python
from src.evaluation.ragas_runner import run_ragas_evaluation

results = run_ragas_evaluation(
    dataset_path="tests/fixtures/06_edgecases_legacy",
    gold_standard="tests/fixtures/06_edgecases_legacy/gold_standard.json"
)

# Focus on:
# - faithfulness: Does system correctly interpret anti-patterns?
# - answer_relevancy: Are answers accurate despite naming noise?
# - context_precision: Does retrieval handle reserved words?
```

## Migration Context

This schema represents a realistic migration scenario:

**Source System:** CustomerMaster v3.2.1 (c. 2008)
- AS/400 legacy system roots
- Windows VB6 application layer
- SQL Server 2008 database
- Multiple developers over 7 years

**Target System:** New ERP Platform (2015)
- Modern ORM with conventional naming
- Integer surrogate keys
- Proper data types
- Tokenized payment data
- Consistent naming conventions

**Migration Challenges:**
1. Maintain business logic during transition
2. Map legacy identifiers to new keys
3. Clean up data quality issues
4. Preserve historical data integrity
5. Handle coexistence period (dual writes)

## Expected System Behavior

### Successful Handling
- Correctly extracts all entities despite anti-patterns
- Generates valid Cypher with proper escaping
- Maintains semantic accuracy
- Provides clear mapping documentation
- Flags data quality issues

### Common Failure Modes
- **Prefix confusion:** Treating `intCustID` as integer when it's VARCHAR
- **Reserved word errors:** Generating invalid Cypher without escaping
- **Type mismatches:** Failing to join on VARCHAR-to-VARCHAR FKs
- **Ambiguity:** Cannot distinguish deprecated from current fields
- **Abbreviation explosion:** Cannot expand `txn_dt` to `transaction_date`

## References

- **Schema anti-patterns:** https://www.kitchensoap.com/2012/03/05/legacy-code-and-the-wolf-at-the-door/
- **Hungarian notation issues:** https://blog.codinghorror.com/hungarian notation-and-other-programming-evils/
- **SQL reserved words:** https://www.postgresql.org/docs/current/sql-keywords-appendix.html
- **Data migration best practices:** https://www.amazon.com/Data-Migration-Bible-Your-Management/dp/1906176070

## Changelog

- **2025-03-23**: Initial dataset creation with 10 tables, 25 QA pairs
- Anticipated: Add query complexity examples
- Anticipated: Add Cypher query examples with proper escaping
