# 05_edgecases_incomplete Dataset

## Purpose

This dataset tests the system's robustness against imperfect, real-world data that contains intentional inconsistencies, missing documentation, and ambiguities. Unlike pristine test datasets, this reflects the messy state of many production systems.

## Domain

Generic business/enterprise system (intentionally ambiguous to test disambiguation capabilities).

## Files

| File | Description |
|------|-------------|
| `business_glossary.txt` | Contains incomplete definitions, circular references, and ambiguous synonyms |
| `data_dictionary.txt` | Has duplicate columns, missing constraints, conflicting references, and inconsistent naming |
| `schema.sql` | DDL with naming inconsistencies (snake_case vs camelCase), missing FK constraints, and duplicate columns |
| `gold_standard.json` | 20 QA pairs testing how the system handles edge cases |
| `README.md` | This file |

## Edge Cases Included

### 1. Incomplete Documentation
- Glossary entries marked as `[definition incomplete]` or `[definition needs clarification]`
- Missing status value definitions
- Circular definitions (Revenue ↔ Sales)

### 2. Naming Inconsistencies
- Mix of snake_case and camelCase in same table
- Duplicate columns with different names (firstName vs first_name)
- Ambiguous table names (ORDER_ITEMS vs ORDER_DETAILS)

### 3. Ambiguous Relationships
- Conflicting FK references (customer_id vs CustomerID)
- Unclear cardinality (one-to-one vs one-to-many)
- Missing or unenforced FK constraints

### 4. Duplicate Concepts
- Customer, Client, Account Holder, End User
- Product, Item, SKU, Inventory Item, Merchandise
- Order, Transaction, Purchase, Sales Order, Quote
- Payment, Invoice, Bill, Receipt

### 5. Missing Constraints
- No NOT NULL constraints
- No CHECK constraints on status columns
- No UNIQUE constraints on natural keys
- FK constraints documented but not enforced

### 6. Conflicting Information
- Multiple date columns for same purpose (order_date, OrderDate, created_at)
- Multiple price columns with unclear distinction (unit_price vs current_price)
- Data types inconsistent for same concept (TIMESTAMP vs DATETIME)

## Test Categories in gold_standard.json

1. **missing_definition** - System should identify incomplete definitions
2. **duplicate_columns** - System should recognize duplicate/redundant columns
3. **conflicting_references** - System should identify ambiguous FK references
4. **missing_constraint** - System should find available info despite gaps
5. **ambiguous_synonyms** - System should surface related terms
6. **circular_definition** - System should detect circular references
7. **conflicting_cardinality** - System should identify conflicting signals
8. **missing_enum_values** - System should avoid hallucinating values
9. **naming_ambiguity** - System should use actual DDL while documenting aliases
10. **missing_workflow** - System should identify missing process documentation

## Expected System Behaviors

### Graceful Degradation
- Provide best available answer given incomplete documentation
- Acknowledge gaps rather than hallucinate
- Surface uncertainty when information conflicts

### Robustness
- Handle inconsistent naming conventions
- Work with missing constraints
- Identify and flag schema issues

### Disambiguation
- Surface related concepts when definitions overlap
- Note circular or ambiguous definitions
- Present conflicting information to user

## Usage in Evaluation

```python
from tests.fixtures.gold_standard import load_qa_pairs

qa_pairs = load_qa_pairs("05_edgecases_incomplete")
# Returns list of 20 QA pairs testing various edge cases
```

## Notes

- This dataset is intentionally messy to test real-world scenarios
- Documentation includes explicit notes about known issues
- Some answers may be "information not available" - this is expected
- The goal is to test system robustness, not to achieve perfect scores
