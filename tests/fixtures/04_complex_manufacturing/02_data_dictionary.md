# Manufacturing Data Dictionary

This data dictionary documents the database schema for the manufacturing supply chain system. It includes all tables, columns, data types, constraints, and relationships. Special attention is given to self-referential relationships that support hierarchical product structures.

## product

Stores all manufactured items including finished goods, assemblies, and components. Supports hierarchical product relationships via self-referencing foreign key.

| Column | Data Type | Constraints | Description |
|--------|-----------|-------------|-------------|
| product_id | VARCHAR(20) | PRIMARY KEY | Unique product identifier |
| product_name | VARCHAR(100) | NOT NULL | Product name |
| product_type | product_type_t | NOT NULL, DEFAULT 'FINISHED_GOOD' | Product classification: FINISHED_GOOD, ASSEMBLY, COMPONENT |
| parent_product_id | VARCHAR(20) | FOREIGN KEY → product(product_id) | Parent product for hierarchical assemblies |
| base_cost | DECIMAL(10,2) | NOT NULL, DEFAULT 0.00, CHECK >= 0 | Base manufacturing cost |
| lead_time_days | INT | NOT NULL, DEFAULT 0, CHECK >= 0 | Procurement or production lead time |
| is_active | yes_no_t | NOT NULL, DEFAULT 'Y' | Active status flag |

**Indexes:**
- `idx_product_parent` on parent_product_id (WHERE NOT NULL) — supports hierarchical queries

**Self-Referential Relationship:**
- `parent_product_id` references `product_id` — enables multi-level product assemblies
- A product can contain other products as components via BOM
- Supports unlimited nesting depth for complex assemblies

## component

Stores atomic raw materials and purchased parts that are procured from external suppliers.

| Column | Data Type | Constraints | Description |
|--------|-----------|-------------|-------------|
| component_id | VARCHAR(20) | PRIMARY KEY | Unique component identifier |
| component_name | VARCHAR(100) | NOT NULL | Component name |
| component_category | VARCHAR(50) | | Component category classification |
| unit_of_measure | VARCHAR(10) | NOT NULL, DEFAULT 'EA' | Unit of measure (EA, KG, M, L, etc.) |
| standard_cost | DECIMAL(10,2) | NOT NULL, DEFAULT 0.00, CHECK >= 0 | Standard procurement cost |
| specification_id | VARCHAR(20) | | Technical specification reference |

**Relationships:**
- Many-to-many with supplier via component_supplier junction table
- One-to-many with inventory
- Optional relationship with specification

## bom

Bill of Materials defining product composition and hierarchical structure. Supports recursive relationships for multi-level assemblies.

| Column | Data Type | Constraints | Description |
|--------|-----------|-------------|-------------|
| bom_id | VARCHAR(20) | PRIMARY KEY | Unique BOM identifier |
| parent_product_id | VARCHAR(20) | NOT NULL, FOREIGN KEY → product(product_id) | Parent product (what is being built) |
| component_product_id | VARCHAR(20) | NOT NULL, FOREIGN KEY → product(product_id) | Component product (what goes into it) |
| quantity | DECIMAL(10,3) | NOT NULL, DEFAULT 1.000, CHECK > 0 | Required quantity |
| unit_of_measure | VARCHAR(10) | NOT NULL, DEFAULT 'EA' | Unit of measure |
| bom_level | INT | NOT NULL, DEFAULT 0, CHECK >= 0 | Depth in product hierarchy |
| is_optional | yes_no_t | NOT NULL, DEFAULT 'N' | Whether component is optional |

**Indexes:**
- `idx_bom_parent` on parent_product_id — BOM explosion queries
- `idx_bom_level` on bom_level — hierarchical queries

**Constraints:**
- `uq_bom_structure` UNIQUE (parent_product_id, component_product_id) — prevents duplicate entries

**Self-Referential Structure:**
- Both `parent_product_id` and `component_product_id` reference the product table
- Enables representation of multi-level assemblies (e.g., Bicycle → Wheel → Spoke)
- `bom_level` tracks depth for performance optimization

## supplier

Stores external vendor information for component procurement.

| Column | Data Type | Constraints | Description |
|--------|-----------|-------------|-------------|
| supplier_id | VARCHAR(20) | PRIMARY KEY | Unique supplier identifier |
| supplier_name | VARCHAR(100) | NOT NULL | Supplier name |
| contact_email | VARCHAR(100) | | Contact email address |
| contact_phone | VARCHAR(20) | | Contact phone number |
| rating | DECIMAL(3,2) | NOT NULL, DEFAULT 3.00, CHECK 1.0-5.0 | Performance rating |
| is_preferred | yes_no_t | NOT NULL, DEFAULT 'N' | Preferred supplier flag |

**Relationships:**
- One-to-many with shipment (inbound)
- Many-to-many with component via component_supplier

## component_supplier

Junction table linking components to their approved suppliers with pricing and lead time information.

| Column | Data Type | Constraints | Description |
|--------|-----------|-------------|-------------|
| component_supplier_id | VARCHAR(20) | PRIMARY KEY | Unique relationship identifier |
| component_id | VARCHAR(20) | NOT NULL, FOREIGN KEY → component(component_id) | Component reference |
| supplier_id | VARCHAR(20) | NOT NULL, FOREIGN KEY → supplier(supplier_id) | Supplier reference |
| is_preferred | yes_no_t | NOT NULL, DEFAULT 'N' | Preferred supplier for this component |
| lead_time_days | INT | NOT NULL, DEFAULT 0 | Procurement lead time |
| unit_price | DECIMAL(10,2) | NOT NULL, DEFAULT 0.00, CHECK >= 0 | Negotiated unit price |

**Indexes:**
- `idx_cs_component` on component_id
- `idx_cs_supplier` on supplier_id

**Constraints:**
- `uq_component_supplier` UNIQUE (component_id, supplier_id) — prevents duplicate supplier associations

## warehouse

Stores physical storage location information for inventory management.

| Column | Data Type | Constraints | Description |
|--------|-----------|-------------|-------------|
| warehouse_id | VARCHAR(20) | PRIMARY KEY | Unique warehouse identifier |
| warehouse_name | VARCHAR(100) | NOT NULL | Warehouse name |
| address | VARCHAR(200) | | Street address |
| city | VARCHAR(50) | | City location |
| state | VARCHAR(50) | | State or province |
| capacity | INT | NOT NULL, DEFAULT 0, CHECK > 0 | Storage capacity |
| manager_id | VARCHAR(20) | | Warehouse manager reference |

**Relationships:**
- One-to-many with inventory
- One-to-many with shipment
- One-to-many with work_order
- One-to-many with batch

## inventory

Tracks stock levels for components and products at specific warehouse locations.

| Column | Data Type | Constraints | Description |
|--------|-----------|-------------|-------------|
| inventory_id | VARCHAR(20) | PRIMARY KEY | Unique inventory identifier |
| warehouse_id | VARCHAR(20) | NOT NULL, FOREIGN KEY → warehouse(warehouse_id) | Warehouse location |
| component_id | VARCHAR(20) | FOREIGN KEY → component(component_id) | Component reference (exclusive with product_id) |
| product_id | VARCHAR(20) | FOREIGN KEY → product(product_id) | Product reference (exclusive with component_id) |
| quantity_on_hand | DECIMAL(10,2) | NOT NULL, DEFAULT 0.00, CHECK >= 0 | Available quantity |
| quantity_reserved | DECIMAL(10,2) | NOT NULL, DEFAULT 0.00, CHECK >= 0 | Reserved quantity |
| reorder_threshold | DECIMAL(10,2) | NOT NULL, DEFAULT 0.00 | Reorder trigger level |
| last_restock_date | DATE | | Last restock timestamp |

**Indexes:**
- `idx_inventory_component` on component_id (WHERE NOT NULL)
- `idx_inventory_product` on product_id (WHERE NOT NULL)
- `idx_inventory_warehouse` on warehouse_id

**Constraints:**
- `chk_inventory_item` EXCLUDE — ensures either component_id OR product_id is set, not both

## work_order

Represents production jobs for manufacturing products with hierarchical work order support.

| Column | Data Type | Constraints | Description |
|--------|-----------|-------------|-------------|
| work_order_id | VARCHAR(20) | PRIMARY KEY | Unique work order identifier |
| product_id | VARCHAR(20) | NOT NULL, FOREIGN KEY → product(product_id) | Product to manufacture |
| parent_work_order | VARCHAR(20) | FOREIGN KEY → work_order(work_order_id) | Parent work order for decomposition |
| quantity_ordered | DECIMAL(10,2) | NOT NULL, DEFAULT 0.00, CHECK > 0 | Quantity to produce |
| quantity_completed | DECIMAL(10,2) | NOT NULL, DEFAULT 0.00, CHECK >= 0, <= ordered | Quantity completed |
| status | status_t | NOT NULL, DEFAULT 'PENDING' | PENDING, IN_PROGRESS, COMPLETED, CLOSED |
| priority | priority_t | NOT NULL, DEFAULT 'MEDIUM' | LOW, MEDIUM, HIGH, URGENT |
| planned_start_date | DATE | | Planned start date |
| planned_end_date | DATE | | Planned end date |
| warehouse_id | VARCHAR(20) | FOREIGN KEY → warehouse(warehouse_id) | Production location |

**Indexes:**
- `idx_work_order_product` on product_id
- `idx_work_order_parent` on parent_work_order (WHERE NOT NULL)
- `idx_work_order_status` on status
- `idx_work_order_dates` on (planned_start_date, planned_end_date)

**Constraints:**
- `chk_dates_consistent` — ensures end_date >= start_date

**Self-Referential Relationship:**
- `parent_work_order` references `work_order_id` — enables work order decomposition
- A large production job can be broken into child work orders
- Supports complex production planning and tracking

## quality_control

Stores inspection and testing records for quality assurance.

| Column | Data Type | Constraints | Description |
|--------|-----------|-------------|-------------|
| qc_id | VARCHAR(20) | PRIMARY KEY | Unique QC identifier |
| batch_id | VARCHAR(20) | | Production batch reference |
| specification_id | VARCHAR(20) | | Specification being tested |
| qc_date | DATE | NOT NULL | Inspection date |
| qc_type | qc_type_t | NOT NULL | INCOMING, IN_PROCESS, FINAL |
| inspector_id | VARCHAR(20) | | Inspector reference |
| result | qc_result_t | NOT NULL | PASS, FAIL, CONDITIONAL |
| defect_count | INT | NOT NULL, DEFAULT 0, CHECK >= 0 | Number of defects found |
| notes | TEXT | | Inspection notes |

**Indexes:**
- `idx_qc_batch` on batch_id (WHERE NOT NULL)
- `idx_qc_specification` on specification_id (WHERE NOT NULL)
- `idx_qc_date` on qc_date
- `idx_qc_result` on result

## specification

Defines technical requirements and acceptance criteria for materials and products.

| Column | Data Type | Constraints | Description |
|--------|-----------|-------------|-------------|
| specification_id | VARCHAR(20) | PRIMARY KEY | Unique specification identifier |
| specification_name | VARCHAR(100) | NOT NULL | Specification name |
| version | VARCHAR(10) | NOT NULL | Specification version |
| effective_date | DATE | NOT NULL | Effective date |
| spec_type | spec_type_t | NOT NULL | DIMENSIONAL, MATERIAL, PERFORMANCE |
| critical_parameter | VARCHAR(100) | | Parameter being tested |
| min_value | DECIMAL(10,3) | | Minimum acceptable value |
| max_value | DECIMAL(10,3) | | Maximum acceptable value |
| unit_of_measure | VARCHAR(10) | | Test unit of measure |

**Indexes:**
- `idx_specification_type` on spec_type
- `idx_specification_effective` on effective_date

**Constraints:**
- `chk_min_max` — ensures max_value >= min_value

## batch

Tracks production lots for traceability and inventory management.

| Column | Data Type | Constraints | Description |
|--------|-----------|-------------|-------------|
| batch_id | VARCHAR(20) | PRIMARY KEY | Unique batch identifier |
| product_id | VARCHAR(20) | NOT NULL, FOREIGN KEY → product(product_id) | Product produced |
| production_date | DATE | NOT NULL | Production date |
| quantity_produced | DECIMAL(10,2) | NOT NULL, DEFAULT 0.00, CHECK > 0 | Quantity produced |
| warehouse_id | VARCHAR(20) | FOREIGN KEY → warehouse(warehouse_id) | Storage location |
| expiry_date | DATE | | Expiry date (if applicable) |
| qc_status | qc_status_t | NOT NULL, DEFAULT 'PENDING' | PENDING, PASSED, FAILED, QUARANTINED |

**Indexes:**
- `idx_batch_product` on product_id
- `idx_batch_date` on production_date
- `idx_batch_warehouse` on warehouse_id
- `idx_batch_qc_status` on qc_status

**Constraints:**
- `chk_expiry_after_production` — ensures expiry_date >= production_date

## route

Defines manufacturing workflow steps and operations for product production.

| Column | Data Type | Constraints | Description |
|--------|-----------|-------------|-------------|
| route_id | VARCHAR(20) | PRIMARY KEY | Unique route identifier |
| product_id | VARCHAR(20) | NOT NULL, FOREIGN KEY → product(product_id) | Product reference |
| route_name | VARCHAR(100) | NOT NULL | Route name |
| sequence_number | INT | NOT NULL, CHECK > 0 | Operation sequence |
| operation_name | VARCHAR(100) | NOT NULL | Operation description |
| work_center | VARCHAR(50) | | Work center location |
| cycle_time_minutes | DECIMAL(8,2) | NOT NULL, DEFAULT 0.00, CHECK >= 0 | Per-unit processing time |
| setup_time_minutes | DECIMAL(8,2) | NOT NULL, DEFAULT 0.00, CHECK >= 0 | Fixed setup time |

**Indexes:**
- `idx_route_product` on product_id
- `idx_route_sequence` on (product_id, sequence_number)

**Constraints:**
- `uq_route_sequence` UNIQUE (product_id, sequence_number) — prevents duplicate sequences
- `chk_times_nonnegative` — ensures times are non-negative

## shipment

Tracks material transfers between warehouses, suppliers, and customers.

| Column | Data Type | Constraints | Description |
|--------|-----------|-------------|-------------|
| shipment_id | VARCHAR(20) | PRIMARY KEY | Unique shipment identifier |
| shipment_type | shipment_type_t | NOT NULL | INBOUND, OUTBOUND, INTERNAL |
| warehouse_id | VARCHAR(20) | FOREIGN KEY → warehouse(warehouse_id) | Warehouse reference |
| supplier_id | VARCHAR(20) | FOREIGN KEY → supplier(supplier_id) | Supplier (inbound only) |
| customer_id | VARCHAR(20) | | Customer reference (outbound) |
| ship_date | DATE | NOT NULL | Shipment date |
| estimated_arrival | DATE | | Estimated arrival date |
| actual_arrival | DATE | | Actual arrival date |
| status | shipment_status_t | NOT NULL, DEFAULT 'PENDING' | PENDING, SHIPPED, DELIVERED, CANCELLED |

**Indexes:**
- `idx_shipment_warehouse` on warehouse_id
- `idx_shipment_supplier` on supplier_id (WHERE NOT NULL)
- `idx_shipment_dates` on (ship_date, estimated_arrival)
- `idx_shipment_status` on status

**Constraints:**
- `chk_shipment_dates` — ensures actual_arrival >= ship_date
- `chk_supplier_inbound` — ensures supplier_id is only set for INBOUND shipments

---

## Key Self-Referential Relationships

### Product Hierarchy
The `product` table's `parent_product_id` column references `product_id`, enabling multi-level product assemblies:
- Level 0: Finished Good (e.g., "Bicycle")
- Level 1: Assemblies (e.g., "Wheel Assembly" → parent "Bicycle")
- Level 2: Sub-assemblies (e.g., "Spoke Set" → parent "Wheel Assembly")

### BOM Recursion
The `bom` table has two foreign keys to `product`:
- `parent_product_id` — the product being built
- `component_product_id` — what goes into it

Both reference `product.product_id`, enabling recursive BOM structures where a component_product_id can itself be a parent_product_id in other BOM entries.

### Work Order Decomposition
The `work_order` table's `parent_work_order` column references `work_order_id`, enabling:
- Parent work order for complete production run
- Child work orders for sub-assemblies or operations
- Hierarchical production planning and tracking

## Enum Types

```sql
product_type_t: ENUM ('FINISHED_GOOD', 'ASSEMBLY', 'COMPONENT')
status_t: ENUM ('PENDING', 'IN_PROGRESS', 'COMPLETED', 'CLOSED')
priority_t: ENUM ('LOW', 'MEDIUM', 'HIGH', 'URGENT')
shipment_type_t: ENUM ('INBOUND', 'OUTBOUND', 'INTERNAL')
shipment_status_t: ENUM ('PENDING', 'SHIPPED', 'DELIVERED', 'CANCELLED')
qc_type_t: ENUM ('INCOMING', 'IN_PROCESS', 'FINAL')
qc_result_t: ENUM ('PASS', 'FAIL', 'CONDITIONAL')
spec_type_t: ENUM ('DIMENSIONAL', 'MATERIAL', 'PERFORMANCE')
qc_status_t: ENUM ('PENDING', 'PASSED', 'FAILED', 'QUARANTINED')
yes_no_t: ENUM ('Y', 'N')
```
