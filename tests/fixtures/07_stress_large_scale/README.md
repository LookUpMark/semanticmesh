# Dataset 07: Enterprise ERP Stress Test

## Overview

This is a large-scale stress test dataset designed to evaluate GraphRAG system performance under realistic enterprise conditions. It models a complete ERP system with 37 interconnected tables and complex business scenarios spanning multiple business units.

**Scale Characteristics:**
- **37 database tables** with 150+ relationships
- **50+ business concepts** across 8 business units
- **55 QA pairs** in gold standard
- **Multi-hop queries** requiring 4-10 table joins
- **Hierarchical data structures** (BOMs, accounts, projects)
- **Entity resolution scenarios** for duplicate detection

## Business Units Modeled

1. **Sales & Customer Management** (7 tables)
   - Customer types, customers, addresses, contacts
   - Products, categories, price lists
   - Sales orders, invoices, payments

2. **Procurement & Supplier Management** (6 tables)
   - Suppliers, contracts, addresses, contacts
   - Purchase orders, receipts

3. **Inventory & Warehousing** (7 tables)
   - Warehouses, zones, bins
   - Inventory on-hand, transactions
   - Stock transfers

4. **Production & Manufacturing** (5 tables)
   - Production lines, BOMs
   - Work orders, materials, schedules

5. **Quality & Compliance** (3 tables)
   - Quality standards, inspections
   - Non-conformance reports

6. **Finance & Accounting** (7 tables)
   - Chart of accounts, journal entries
   - Accounts receivable/payable
   - Budgets, accounting periods

7. **Human Resources** (5 tables)
   - Departments, positions, employees
   - Time entries

8. **Logistics & Shipping** (4 tables)
   - Carriers, routes, shipments

9. **System & Security** (4 tables)
   - Users, roles, audit logs

## Key Features

### Complexity Factors

- **Foreign Key Density**: Average of 4+ foreign keys per table
- **Many-to-Many Relationships**: Sales orders ↔ Products, Projects ↔ Employees
- **Self-Join Hierarchies**: BOMs, Chart of Accounts, Project Tasks
- **Composite Keys**: Several tables use multi-column primary keys
- **Circular References**: Project Manager → Employee → Department → Manager

### Query Patterns Tested

1. **Multi-hop Retrieval** (4-10 table joins)
2. **Hierarchical Traversal** (recursive BOM lookups)
3. **Entity Resolution** (duplicate detection across customers)
4. **Complex Aggregation** (grouping by multiple dimensions)
5. **Temporal Analysis** (date ranges, aging calculations)
6. **Variance Analysis** (actual vs. budget, planned vs. actual)
7. **Network Analysis** (supply chain dependency mapping)

## File Descriptions

### 01_business_glossary.md (288 lines)
Comprehensive business glossary defining 50+ concepts across all business units. Each concept includes:
- Definition and business context
- Key attributes and data points
- Related concepts and relationships
- Business rules and constraints

**Purpose**: Provides semantic context for entity extraction and relationship mapping.

### 02_enterprise_schema.sql (985 lines)
Complete DDL schema for 37 tables with realistic enterprise complexity:
- Primary keys, foreign keys, and constraints
- Indexes for query performance
- CHECK constraints for data validation
- Computed columns for derived values
- JSON columns for audit trail

**Purpose**: Tests schema ingestion, table relationship mapping, and Cypher generation.

### 03_complex_scenarios.md (780 lines)
Eight detailed business scenarios requiring complex multi-table queries:
1. Order-to-Cash Cross-Business-Unit Analysis (8 tables)
2. Procurement-to-Pay Performance Analysis (9 tables)
3. Multi-Warehouse Inventory Optimization (10 tables)
4. Production Cost & Efficiency Analysis (8 tables)
5. Customer Entity Resolution & Deduplication (6 tables)
6. Financial Statement Generation (7 tables)
7. Supply Chain Risk Assessment (8 tables)
8. Project Profitability & Resource Utilization (7 tables)

**Purpose**: Provides end-to-end test scenarios that mirror real-world business questions.

### 04_gold_standard.json (551 lines)
55 curated QA pairs with metadata including:
- Question complexity rating (medium, high, very high)
- Tables involved (4-10 tables per query)
- Query pattern description
- Expected result format
- Answer type (aggregation, filtering, hierarchical, entity_resolution)

**Distribution:**
- Medium complexity: 32 questions (4-5 joins)
- High complexity: 19 questions (6-8 joins)
- Very high complexity: 4 questions (9-10 joins)

**Purpose**: Automated evaluation of retrieval accuracy and answer quality.

## Usage Examples

### Example 1: Multi-Hop Query
**Question**: "What are the top 5 customers by total order value in the last 90 days, and what is their credit score and payment history?"

**Required Tables**: customer → customer_type → sales_order → invoice → payment

**Graph Traversal**: 5 hops with date filtering and aggregation

### Example 2: Hierarchical Query
**Question**: "What is the complete bill of materials for product 'Industrial Assembly Robot ARM-500' including all sub-assemblies and raw materials?"

**Required Tables**: product → bill_of_materials (recursive self-join)

**Graph Traversal**: Multi-level BOM tree traversal

### Example 3: Entity Resolution
**Question**: "Which customers have duplicate records based on matching tax IDs or similar names, and what orders should be merged?"

**Required Tables**: customer (self-join for similarity) → customer_address → customer_contact → sales_order → invoice

**Graph Traversal**: Similarity matching + relationship analysis

## Performance Expectations

Based on query complexity:

| Complexity | Tables | Expected Time | Use Case |
|------------|--------|---------------|----------|
| Simple | 2-3 | < 1s | Basic lookups |
| Medium | 4-5 | 1-3s | Common business queries |
| High | 6-8 | 3-8s | Cross-domain analysis |
| Very High | 9-10 | 8-15s | Enterprise reporting |

## Integration with Test Suite

This dataset can be used with the existing test framework:

```python
from src.ingestion.pdf_loader import load_pdf
from src.ingestion.ddl_parser import parse_ddl

# Load business glossary
glossary_doc = load_pdf("tests/fixtures/07_stress_large_scale/01_business_glossary.md")

# Parse schema
schema = parse_ddl("tests/fixtures/07_stress_large_scale/02_enterprise_schema.sql")

# Load gold standard
import json
with open("tests/fixtures/07_stress_large_scale/04_gold_standard.json") as f:
    gold_standard = json.load(f)

# Run evaluation
for qa in gold_standard["qa_pairs"]:
    result = query_graph(qa["question"])
    evaluate_result(result, qa)
```

## Key Challenges

This dataset tests specific challenges:

1. **Scale**: 37 tables is significantly larger than previous datasets (5-15 tables)
2. **Density**: Rich interconnections require intelligent path selection
3. **Hierarchy**: Recursive queries test graph navigation capabilities
4. **Ambiguity**: Entity names may be similar (e.g., "Industrial Control System" vs "Industrial Control Panel")
5. **Context**: Questions require understanding business context (e.g., "overdue" means due_date < current_date AND balance_due > 0)
6. **Aggregation**: Complex GROUP BY operations with multiple dimensions

## Comparison with Other Datasets

| Dataset | Tables | Concepts | Business Units | Purpose |
|---------|--------|----------|----------------|---------|
| 01_simple | 5 | 15 | 1 | Basic functionality |
| 02_medium | 12 | 30 | 3 | Standard operations |
| 03_complex | 18 | 40 | 4 | Cross-domain queries |
| **07_stress** | **37** | **50+** | **8** | **Performance & scale** |

## Notes for Graph Construction

When building the knowledge graph from this dataset:

1. **Entity Extraction**: Pay attention to entity variations (e.g., "ACME Manufacturing Inc." vs "ACME Manufacturing Company")
2. **Relationship Types**: Use specific relationship types (REFERENCES, ORDERS_FROM, SUPPLIES_TO, etc.)
3. **Property Preservation**: Maintain all business attributes (credit scores, ratings, dates) as node properties
4. **Index Creation**: Create indexes on frequently queried properties (customer_number, order_number, product_name)
5. **Batch Processing**: Due to scale, use batch upserts for large datasets

## Maintenance

This dataset should be updated to reflect:
- New business scenarios as they're identified
- Additional QA pairs for edge case testing
- Schema changes as the ERP system evolves
- Performance baselines as the system improves

## References

- ERP System Architecture: Standard enterprise resource planning concepts
- Data Model Patterns: Industry-standard database design patterns
- GraphRAG Evaluation: Testing knowledge graph-based question answering
