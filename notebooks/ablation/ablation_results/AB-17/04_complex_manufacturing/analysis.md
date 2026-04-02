# AB-17 — 04_complex_manufacturing — Run Analysis

**Timestamp:** 2026-04-01 19:20:33  
**Run tag:** `v5`

## Configuration

| Parameter | Value |
|-----------|-------|
| Extraction model | `LLM (gpt-5.4-nano-2026-03-17)` |
| Reasoning model | `gpt-5.4-2026-03-05` |
| Embedding model | `BAAI/bge-m3` |
| Retrieval mode | `hybrid` |
| Reranker | `True` |
| Reranker top_k | `12` |
| Chunk size / overlap | `256 / 32` |
| ER similarity threshold | `0.75` |

## Builder Results

| Metric | Value |
|--------|-------|
| Triplets extracted | 393 |
| Entities resolved | 131 |
| Tables parsed | 13 |
| Tables completed | 13 |

## Query Evaluation Summary

| Metric | Value |
|--------|-------|
| Questions | 40 |
| Grounded | **40/40 (100%)** |
| Avg GT Coverage | 100% |
| Avg Top Score | 0.4240 |
| Avg Chunk Count | 12.0 |
| Abstained | 0 |

## RAGAS Metrics

RAGAS evaluation not enabled for this run.

## Per-Question Deep Dive

### ✅ QA-001 — What information is stored about products in the manufacturing system?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.8872 | **Gate:** `proceed`

**Expected answer:**
> Products are tracked with a unique identifier (product_id), descriptive name (product_name), classification as finished good, assembly, or component (product_type), optional parent product reference for hierarchical structures (parent_product_id), standard unit cost (base_cost), typical procurement …

**System answer:**
> The manufacturing system stores product information in the `PRODUCT` table. From the schema, each product record includes a unique `product_id` (`VARCHAR(20)`, primary key), `product_name` (`VARCHAR(100)`, not null), `product_type` (not null, default `FINISHED_GOOD`), `parent_product_id` (foreign key to `product(product_id)`), `base_cost` (nonnegative decimal), `lead_time_days` (nonnegative intege…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_3`, `Route Step`, `Route Step→ROUTE`, `Work Order→WORK_ORDER`, `parent_chunk_data_dictionary.md_6`, `parent_chunk_business_glossary.md_0`, `parent_chunk_business_glossary.md_1`, `Work Order`

**Context previews (first 3):**

1. _# Manufacturing Data Dictionary  This data dictionary documents the database schema for the manufacturing supply chain system. It includes all tables, columns, data types, constraints, and relationshi…_

2. _Route Step: The table stores ordered manufacturing operations for a product, including operation name, work center, sequence number, cycle time, and setup time, which matches the route step concept ex…_

3. _Business concept 'Route Step' — The table stores ordered manufacturing operations for a product, including operation name, work center, sequence number, cycle time, and setup time, which matches the r…_

---

### ✅ QA-002 — How are components defined in the manufacturing database?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.5910 | **Gate:** `proceed`

**Expected answer:**
> Components are defined with a unique identifier (component_id), descriptive name (component_name), category grouping (component_category), unit of measure (unit_of_measure), standard unit cost (standard_cost), and optional reference to technical specifications (specification_id). Components represen…

**System answer:**
> In the business glossary, a Component is defined as an atomic raw material or purchased part that cannot be further broken down into simpler manufactured items. Components are the building blocks used in manufacturing and are procured from external suppliers.

In the physical schema, this concept is implemented by the COMPONENT table, which contains the columns component_id, component_name, compon…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_3`, `a parent product, a component product (which can be either a component or sub-assembly), the required quantity, unit of measure, and hierarchical level in the product structure→COMPONENT`, `parent_chunk_data_dictionary.md_4`, `The Bill of Materials (BOM)→BOM`, `parent_chunk_data_dictionary.md_5`, `Component Supplier Junction→COMPONENT_SUPPLIER`, `parent_chunk_business_glossary.md_0`, `parent_chunk_business_glossary.md_1`

**Context previews (first 3):**

1. _# Manufacturing Data Dictionary  This data dictionary documents the database schema for the manufacturing supply chain system. It includes all tables, columns, data types, constraints, and relationshi…_

2. _Business concept 'a parent product, a component product (which can be either a component or sub-assembly), the required quantity, unit of measure, and hierarchical level in the product structure' is i…_

3. _## bom  Bill of Materials defining product composition and hierarchical structure. Supports recursive relationships for multi-level assemblies.  | Column | Data Type | Constraints | Description | |---…_

---

### ✅ QA-003 — What is the purpose of the Bill of Materials (BOM) table?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.9858 | **Gate:** `proceed`

**Expected answer:**
> The BOM table defines the hierarchical structure of products by specifying which components or sub-assemblies are required to manufacture each parent product. It records the unique BOM entry identifier (bom_id), parent product being built (parent_product_id), component or sub-assembly product (compo…

**System answer:**
> The Bill of Materials (BOM) table implements the Bill of Materials business concept by defining how products are composed. Its purpose is to record the relationship between a parent product and its component products, including the required quantity, unit of measure, hierarchy level, and whether a component is optional.

From the schema, BOM supports hierarchical and recursive product structures b…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_4`, `The Bill of Materials (BOM)→BOM`, `BOM→PRODUCT`, `parent_chunk_data_dictionary.md_3`, `parent_chunk_data_dictionary.md_7`, `parent_chunk_data_dictionary.md_8`, `The Bill of Materials (BOM)`, `parent_chunk_business_glossary.md_0`

**Context previews (first 3):**

1. _## bom  Bill of Materials defining product composition and hierarchical structure. Supports recursive relationships for multi-level assemblies.  | Column | Data Type | Constraints | Description | |---…_

2. _Business concept 'The Bill of Materials (BOM)' is implemented by physical table BOM (columns: bom_id, parent_product_id, component_product_id, quantity, unit_of_measure, bom_level, is_optional).…_

3. _Relationship: BOM references PRODUCT via foreign key COMPONENT_PRODUCT_ID -> PRODUCT.PRODUCT_ID.…_

---

### ✅ QA-004 — What supplier information does the system maintain?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0325 | **Gate:** `proceed_with_warning`

**Expected answer:**
> Suppliers are tracked with a unique identifier (supplier_id), legal business name (supplier_name), primary contact email (contact_email), primary contact phone number (contact_phone), performance rating from 1.0 to 5.0 (rating), and preferred supplier status flag (is_preferred).

**System answer:**
> The system maintains supplier information in the `SUPPLIER` table, which stores external vendor information for component procurement. From the retrieved context, the supplier attributes are `supplier_id`, `supplier_name`, `contact_email`, `contact_phone`, `rating`, and `is_preferred`.

Supplier information is also maintained in related schema structures. The `COMPONENT_SUPPLIER` table is a many-t…

**Sources retrieved (12):** `Preferred supplier for this component→SUPPLIER`, `parent_chunk_data_dictionary.md_4`, `SHIPMENT→SUPPLIER`, `parent_chunk_data_dictionary.md_8`, `COMPONENT_SUPPLIER→SUPPLIER`, `Component Supplier Junction→COMPONENT_SUPPLIER`, `parent_chunk_data_dictionary.md_3`, `shipment_type_t ENUM ('INBOUND', 'OUTBOUND', 'INTERNAL')→SHIPMENT`

**Context previews (first 3):**

1. _Business concept 'Preferred supplier for this component' is implemented by physical table SUPPLIER (columns: supplier_id, supplier_name, contact_email, contact_phone, rating, is_preferred).…_

2. _## bom  Bill of Materials defining product composition and hierarchical structure. Supports recursive relationships for multi-level assemblies.  | Column | Data Type | Constraints | Description | |---…_

3. _Relationship: SHIPMENT references SUPPLIER via foreign key SUPPLIER_ID -> SUPPLIER.SUPPLIER_ID.…_

---

### ✅ QA-005 — How are warehouses represented in the schema?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.3381 | **Gate:** `proceed`

**Expected answer:**
> Warehouses are defined with a unique identifier (warehouse_id), descriptive name (warehouse_name), full street address (address), city location (city), state or province (state), total storage capacity in cubic meters (capacity), and optional manager identifier (manager_id).

**System answer:**
> Warehouses are represented by the physical table `WAREHOUSE`, which models a physical storage location in the supply chain. It stores `warehouse_id` as the primary key, along with `warehouse_name`, `address`, `city`, `state`, `capacity`, and `manager_id`. The schema description says a warehouse is a location where materials, components, and finished goods are stored, with defined capacity limits, …

**Sources retrieved (12):** `INVENTORY→WAREHOUSE`, `BATCH→WAREHOUSE`, `WORK_ORDER→WAREHOUSE`, `SHIPMENT→WAREHOUSE`, `parent_chunk_data_dictionary.md_6`, `parent_chunk_data_dictionary.md_5`, `geographic location information→WAREHOUSE`, `Work Order→WORK_ORDER`

**Context previews (first 3):**

1. _Relationship: INVENTORY references WAREHOUSE via foreign key WAREHOUSE_ID -> WAREHOUSE.WAREHOUSE_ID.…_

2. _Relationship: BATCH references WAREHOUSE via foreign key WAREHOUSE_ID -> WAREHOUSE.WAREHOUSE_ID.…_

3. _Relationship: WORK_ORDER references WAREHOUSE via foreign key WAREHOUSE_ID -> WAREHOUSE.WAREHOUSE_ID.…_

---

### ✅ QA-006 — What does the inventory table track?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.5349 | **Gate:** `proceed`

**Expected answer:**
> The inventory table tracks real-time stock levels including a unique record identifier (inventory_id), warehouse location (warehouse_id), component identifier for materials (component_id) or product identifier for finished goods (product_id), current physical stock quantity (quantity_on_hand), quant…

**System answer:**
> The `inventory` table tracks stock levels of components and products at specific warehouse locations.

From the context, each inventory record represents inventory held in a `warehouse` and supports either a `component` or a `product` in a single record, but not both at once. It captures:

`inventory_id` as the unique inventory record,
`warehouse_id` for the storage location,
`component_id` or `pr…

**Sources retrieved (12):** `INVENTORY→PRODUCT`, `Batches for traceability and inventory management→INVENTORY`, `INVENTORY→WAREHOUSE`, `INVENTORY→COMPONENT`, `parent_chunk_data_dictionary.md_5`, `parent_chunk_data_dictionary.md_7`, `Work Order→WORK_ORDER`, `parent_chunk_data_dictionary.md_8`

**Context previews (first 3):**

1. _Relationship: INVENTORY references PRODUCT via foreign key PRODUCT_ID -> PRODUCT.PRODUCT_ID.…_

2. _Business concept 'Batches for traceability and inventory management' is implemented by physical table INVENTORY (columns: inventory_id, warehouse_id, component_id, product_id, quantity_on_hand, quanti…_

3. _Relationship: INVENTORY references WAREHOUSE via foreign key WAREHOUSE_ID -> WAREHOUSE.WAREHOUSE_ID.…_

---

### ✅ QA-007 — How are work orders structured in the manufacturing system?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.7003 | **Gate:** `proceed`

**Expected answer:**
> Work orders represent production jobs with a unique identifier (work_order_id), product to be manufactured (product_id), optional parent work order for nested hierarchies (parent_work_order), quantity to produce (quantity_ordered), quantity completed so far (quantity_completed), current status (PEND…

**System answer:**
> Work orders in this manufacturing system are represented by the `WORK_ORDER` table and model production jobs for manufacturing products. The structure includes a unique identifier, the product being manufactured, optional linkage to a parent work order, planned and completed quantities, lifecycle status, priority, planned dates, and the warehouse where production is staged.

At the schema level, `…

**Sources retrieved (12):** `Work Order→WORK_ORDER`, `parent_chunk_data_dictionary.md_6`, `Route Step`, `WORK_ORDER→PRODUCT`, `Route Step→ROUTE`, `WORK_ORDER→WORK_ORDER`, `parent_chunk_data_dictionary.md_3`, `WORK_ORDER→WAREHOUSE`

**Context previews (first 3):**

1. _Business concept 'Work Order' — The table is explicitly labeled as a work order / production jobs table and contains the core attributes of a manufacturing job: product, planned quantities, status, pr…_

2. _## work_order  Represents production jobs for manufacturing products with hierarchical work order support.  | Column | Data Type | Constraints | Description | |--------|-----------|-------------|-----…_

3. _Route Step: The table stores ordered manufacturing operations for a product, including operation name, work center, sequence number, cycle time, and setup time, which matches the route step concept ex…_

---

### ✅ QA-008 — What information is captured in the shipment table?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.7724 | **Gate:** `proceed`

**Expected answer:**
> Shipments track material transfers with a unique identifier (shipment_id), shipment type (INBOUND from suppliers, OUTBOUND to customers, INTERNAL between warehouses), destination warehouse (warehouse_id), source supplier for inbound (supplier_id), destination customer for outbound (customer_id), shi…

**System answer:**
> The `shipment` table captures material transfer records between warehouses, suppliers, and customers.

It stores the shipment’s unique identifier in `shipment_id`, the shipment type in `shipment_type`, and the related warehouse in `warehouse_id`. The shipment type is `INBOUND`, `OUTBOUND`, or `INTERNAL`. It also captures `supplier_id` for supplier-linked shipments and `customer_id` for customer-li…

**Sources retrieved (12):** `shipment_type_t ENUM ('INBOUND', 'OUTBOUND', 'INTERNAL')→SHIPMENT`, `SHIPMENT→WAREHOUSE`, `SHIPMENT→SUPPLIER`, `parent_chunk_data_dictionary.md_8`, `parent_chunk_data_dictionary.md_5`, `parent_chunk_business_glossary.md_0`, `parent_chunk_business_glossary.md_1`, `Route Step`

**Context previews (first 3):**

1. _Business concept 'shipment_type_t ENUM ('INBOUND', 'OUTBOUND', 'INTERNAL')' is implemented by physical table SHIPMENT (columns: shipment_id, shipment_type, warehouse_id, supplier_id, customer_id, ship…_

2. _Relationship: SHIPMENT references WAREHOUSE via foreign key WAREHOUSE_ID -> WAREHOUSE.WAREHOUSE_ID.…_

3. _Relationship: SHIPMENT references SUPPLIER via foreign key SUPPLIER_ID -> SUPPLIER.SUPPLIER_ID.…_

---

### ✅ QA-009 — How does the quality control system record inspections?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.9540 | **Gate:** `proceed`

**Expected answer:**
> Quality control records are stored with a unique identifier (qc_id), associated production batch (batch_id), applicable specification requirements (specification_id), inspection date (qc_date), inspection type (INCOMING for supplier materials, IN_PROCESS during manufacturing, FINAL for finished good…

**System answer:**
> The quality control system records inspections in the physical table QUALITY_CONTROL, which implements the business concept Quality Control inspections. This table stores one record per inspection using qc_id as the unique QC identifier, and includes batch_id, specification_id, qc_date, qc_type, inspector_id, result, defect_count, and notes.

From the business definition, these inspection records …

**Sources retrieved (12):** `Quality Control inspections→QUALITY_CONTROL`, `BOM→PRODUCT`, `the product produced, production date, quantity produced, warehouse location, expiry date (if applicable), and quality control status→PRODUCT`, `parent_chunk_data_dictionary.md_3`, `BATCH→PRODUCT`, `parent_chunk_business_glossary.md_2`, `Quality Control inspections`, `parent_chunk_business_glossary.md_0`

**Context previews (first 3):**

1. _Business concept 'Quality Control inspections' is implemented by physical table QUALITY_CONTROL (columns: qc_id, batch_id, specification_id, qc_date, qc_type, inspector_id, result, defect_count, notes…_

2. _Relationship: BOM references PRODUCT via foreign key COMPONENT_PRODUCT_ID -> PRODUCT.PRODUCT_ID.…_

3. _Business concept 'the product produced, production date, quantity produced, warehouse location, expiry date (if applicable), and quality control status' is implemented by physical table PRODUCT (colum…_

---

### ✅ QA-010 — What do specification records define?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.7558 | **Gate:** `proceed`

**Expected answer:**
> Specifications define technical requirements with a unique identifier (specification_id), descriptive name (specification_name), version number, effective date, specification type (DIMENSIONAL, MATERIAL, PERFORMANCE), critical parameter being measured (critical_parameter), acceptable minimum value (…

**System answer:**
> Specification records define the technical requirements, standards, and acceptance criteria for materials and products. They capture what quality requirements must be met, including the specification name and version, effective date, specification type (`DIMENSIONAL`, `MATERIAL`, or `PERFORMANCE`), the critical parameter being tested, and the acceptable minimum and maximum values with the relevant…

**Sources retrieved (12):** `a standard cost, unit of measure, and may be associated with technical specifications that define quality requirements→SPECIFICATION`, `parent_chunk_data_dictionary.md_7`, `Quality Control inspections→QUALITY_CONTROL`, `a parent product, a component product (which can be either a component or sub-assembly), the required quantity, unit of measure, and hierarchical level in the product structure→COMPONENT`, `parent_chunk_data_dictionary.md_3`, `parent_chunk_business_glossary.md_2`, `parent_chunk_business_glossary.md_0`, `a standard cost, unit of measure, and may be associated with technical specifications that define quality requirements`

**Context previews (first 3):**

1. _Business concept 'a standard cost, unit of measure, and may be associated with technical specifications that define quality requirements' is implemented by physical table SPECIFICATION (columns: speci…_

2. _## specification  Defines technical requirements and acceptance criteria for materials and products.  | Column | Data Type | Constraints | Description | |--------|-----------|-------------|-----------…_

3. _Business concept 'Quality Control inspections' is implemented by physical table QUALITY_CONTROL (columns: qc_id, batch_id, specification_id, qc_date, qc_type, inspector_id, result, defect_count, notes…_

---

### ✅ QA-011 — How can I find which suppliers provide specific components?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.1645 | **Gate:** `proceed_with_warning`

**Expected answer:**
> Query the component_supplier table which links components to their approved suppliers. This table contains the component identifier (component_id), supplier identifier (supplier_id), preferred supplier flag (is_preferred), lead time in days (lead_time_days), and unit price (unit_price). Join with th…

**System answer:**
> Use the `COMPONENT_SUPPLIER` table. In the retrieved context, it is explicitly the many-to-many junction between components and suppliers, with these columns: `component_supplier_id`, `component_id`, `supplier_id`, `is_preferred`, `lead_time_days`, and `unit_price`.

To find which suppliers provide a specific component, trace this join path: `COMPONENT` → `COMPONENT_SUPPLIER` → `SUPPLIER`.

The re…

**Sources retrieved (12):** `Component Supplier Junction→COMPONENT_SUPPLIER`, `parent_chunk_data_dictionary.md_5`, `parent_chunk_data_dictionary.md_4`, `parent_chunk_data_dictionary.md_3`, `parent_chunk_data_dictionary.md_8`, `parent_chunk_business_glossary.md_0`, `Component Supplier Junction`, `parent_chunk_business_glossary.md_1`

**Context previews (first 3):**

1. _Business concept 'Component Supplier Junction' — The table is explicitly a many-to-many junction between component and supplier, with a uniqueness constraint on the pair and fields for preferred statu…_

2. _## warehouse  Stores physical storage location information for inventory management.  | Column | Data Type | Constraints | Description | |--------|-----------|-------------|-------------| | warehouse_…_

3. _## bom  Bill of Materials defining product composition and hierarchical structure. Supports recursive relationships for multi-level assemblies.  | Column | Data Type | Constraints | Description | |---…_

---

### ✅ QA-012 — How do I trace which components are needed to fulfill a work order?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.2334 | **Gate:** `proceed`

**Expected answer:**
> Start with the work_order table to get the product_id being manufactured. Join to the bom table using product_id as parent_product_id to find all direct components and sub-assemblies. For each component_product_id, if it is an ASSEMBLY type product, recursively query the bom table again to explode m…

**System answer:**
> From the provided context, you can trace a work order only up to the product being built and its product hierarchy, not the exact component requirements.

At the schema level, start with `WORK_ORDER`. Use `work_order_id` to locate the job, then read `WORK_ORDER.product_id` to identify the product being manufactured. Join `WORK_ORDER.product_id = PRODUCT.product_id` to get the product record in `pr…

**Sources retrieved (12):** `Work Order→WORK_ORDER`, `parent_chunk_data_dictionary.md_5`, `parent_chunk_data_dictionary.md_6`, `Batches for traceability and inventory management→INVENTORY`, `Component Supplier Junction→COMPONENT_SUPPLIER`, `parent_chunk_data_dictionary.md_3`, `parent_chunk_data_dictionary.md_8`, `parent_chunk_business_glossary.md_1`

**Context previews (first 3):**

1. _Business concept 'Work Order' — The table is explicitly labeled as a work order / production jobs table and contains the core attributes of a manufacturing job: product, planned quantities, status, pr…_

2. _## warehouse  Stores physical storage location information for inventory management.  | Column | Data Type | Constraints | Description | |--------|-----------|-------------|-------------| | warehouse_…_

3. _## work_order  Represents production jobs for manufacturing products with hierarchical work order support.  | Column | Data Type | Constraints | Description | |--------|-----------|-------------|-----…_

---

### ✅ QA-013 — How can I identify which warehouses have available inventory for specific components?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.8215 | **Gate:** `proceed`

**Expected answer:**
> Query the inventory table filtered by component_id, joining with the warehouse table to get warehouse names and locations. Calculate available quantity as quantity_on_hand minus quantity_reserved. Filter for records where available quantity is greater than zero. Results show warehouse names, locatio…

**System answer:**
> Use the `inventory` table as the starting point. It stores stock levels at the warehouse level and includes `warehouse_id`, `component_id`, `quantity_on_hand`, `quantity_reserved`, `reorder_threshold`, and `last_restock_date`. The `inventory` table references `warehouse` through `inventory.warehouse_id -> warehouse.warehouse_id`, and it references `component` through `inventory.component_id -> com…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_5`, `INVENTORY→WAREHOUSE`, `Batches for traceability and inventory management→INVENTORY`, `INVENTORY→COMPONENT`, `parent_chunk_data_dictionary.md_3`, `parent_chunk_data_dictionary.md_8`, `parent_chunk_data_dictionary.md_6`, `parent_chunk_data_dictionary.md_4`

**Context previews (first 3):**

1. _## warehouse  Stores physical storage location information for inventory management.  | Column | Data Type | Constraints | Description | |--------|-----------|-------------|-------------| | warehouse_…_

2. _Relationship: INVENTORY references WAREHOUSE via foreign key WAREHOUSE_ID -> WAREHOUSE.WAREHOUSE_ID.…_

3. _Business concept 'Batches for traceability and inventory management' is implemented by physical table INVENTORY (columns: inventory_id, warehouse_id, component_id, product_id, quantity_on_hand, quanti…_

---

### ✅ QA-014 — How do I find which shipments delivered materials from a specific supplier?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.2401 | **Gate:** `proceed`

**Expected answer:**
> Query the shipment table filtering by supplier_id and shipment_type = 'INBOUND'. Join with the warehouse table to show destination warehouses. Filter for status = 'DELIVERED' and include actual_arrival date. Results can be ordered by ship_date descending to show most recent deliveries first.

**System answer:**
> Use the `shipment` table as the primary source. To find shipments that delivered materials from a specific supplier, filter `shipment` by the supplier and by delivered inbound shipments:

Join path: `shipment.supplier_id -> supplier.supplier_id`. If you also want the receiving location, `shipment.warehouse_id -> warehouse.warehouse_id`.

The relevant shipment logic in the context is:
`shipment.sup…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_8`, `SHIPMENT→SUPPLIER`, `shipment_type_t ENUM ('INBOUND', 'OUTBOUND', 'INTERNAL')→SHIPMENT`, `parent_chunk_data_dictionary.md_5`, `parent_chunk_data_dictionary.md_7`, `parent_chunk_data_dictionary.md_3`, `Component Supplier Junction→COMPONENT_SUPPLIER`, `parent_chunk_data_dictionary.md_4`

**Context previews (first 3):**

1. _## shipment  Tracks material transfers between warehouses, suppliers, and customers.  | Column | Data Type | Constraints | Description | |--------|-----------|-------------|-------------| | shipment_i…_

2. _Relationship: SHIPMENT references SUPPLIER via foreign key SUPPLIER_ID -> SUPPLIER.SUPPLIER_ID.…_

3. _Business concept 'shipment_type_t ENUM ('INBOUND', 'OUTBOUND', 'INTERNAL')' is implemented by physical table SHIPMENT (columns: shipment_id, shipment_type, warehouse_id, supplier_id, customer_id, ship…_

---

### ✅ QA-015 — How can I determine which quality control inspections were performed on a specific production batch?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.9779 | **Gate:** `proceed`

**Expected answer:**
> Query the quality_control table filtered by batch_id. Join with the specification table to get requirement details (specification_name, spec_type, acceptable ranges). Include qc_date, qc_type (INCOMING, IN_PROCESS, FINAL), result (PASS, FAIL, CONDITIONAL), and defect_count. This shows the complete i…

**System answer:**
> To determine which quality control inspections were performed on a specific production batch, use the `QUALITY_CONTROL` table and match it to the batch through `batch_id`.

The schema-level path is `BATCH.batch_id = QUALITY_CONTROL.batch_id`. The `QUALITY_CONTROL` table implements the business concept “Quality Control inspections” and contains the inspection records for a batch in these columns: `…

**Sources retrieved (12):** `Quality Control inspections→QUALITY_CONTROL`, `parent_chunk_data_dictionary.md_7`, `Production batch reference→BATCH`, `the product produced, production date, quantity produced, warehouse location, expiry date (if applicable), and quality control status→PRODUCT`, `BATCH→PRODUCT`, `parent_chunk_data_dictionary.md_5`, `parent_chunk_business_glossary.md_2`, `Quality Control inspections`

**Context previews (first 3):**

1. _Business concept 'Quality Control inspections' is implemented by physical table QUALITY_CONTROL (columns: qc_id, batch_id, specification_id, qc_date, qc_type, inspector_id, result, defect_count, notes…_

2. _## specification  Defines technical requirements and acceptance criteria for materials and products.  | Column | Data Type | Constraints | Description | |--------|-----------|-------------|-----------…_

3. _Business concept 'Production batch reference' is implemented by physical table BATCH (columns: batch_id, product_id, production_date, quantity_produced, warehouse_id, expiry_date, qc_status).…_

---

### ✅ QA-016 — How do I track which work orders are in progress at a specific warehouse?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.7311 | **Gate:** `proceed`

**Expected answer:**
> Query the work_order table filtering by warehouse_id and status = 'IN_PROGRESS'. Join with the product table to get product names and types. Include quantity_ordered, quantity_completed, priority, planned_end_date, and calculate progress percentage as (quantity_completed / quantity_ordered * 100). O…

**System answer:**
> To track work orders that are in progress at a specific warehouse, use the `WORK_ORDER` table and its foreign key to `WAREHOUSE`.

`WORK_ORDER` contains the work-order status and warehouse assignment:
- `work_order_id`
- `product_id`
- `parent_work_order`
- `quantity_ordered`
- `quantity_completed`
- `status`
- `priority`
- `planned_start_date`
- `planned_end_date`
- `warehouse_id`

A work order i…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_5`, `parent_chunk_data_dictionary.md_6`, `Work Order→WORK_ORDER`, `WORK_ORDER→WAREHOUSE`, `parent_chunk_data_dictionary.md_8`, `parent_chunk_data_dictionary.md_7`, `Batches for traceability and inventory management→INVENTORY`, `WORK_ORDER→WORK_ORDER`

**Context previews (first 3):**

1. _## warehouse  Stores physical storage location information for inventory management.  | Column | Data Type | Constraints | Description | |--------|-----------|-------------|-------------| | warehouse_…_

2. _## work_order  Represents production jobs for manufacturing products with hierarchical work order support.  | Column | Data Type | Constraints | Description | |--------|-----------|-------------|-----…_

3. _Business concept 'Work Order' — The table is explicitly labeled as a work order / production jobs table and contains the core attributes of a manufacturing job: product, planned quantities, status, pr…_

---

### ✅ QA-017 — How can I find which components need reordering based on current inventory levels?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.3023 | **Gate:** `proceed`

**Expected answer:**
> Query the inventory table and filter where quantity_on_hand minus quantity_reserved is less than reorder_threshold. Join with the component table to get component names, categories, and standard costs. Join with the warehouse table for location information. Results identify which components are belo…

**System answer:**
> Use the INVENTORY table. It is the table that tracks stock levels and reorder thresholds, with these relevant columns: inventory_id, warehouse_id, component_id, product_id, quantity_on_hand, quantity_reserved, reorder_threshold, and last_restock_date.

At the schema level, the way to find components that need reordering is to select INVENTORY records where component_id is populated, because each i…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_5`, `Batches for traceability and inventory management→INVENTORY`, `INVENTORY→COMPONENT`, `parent_chunk_data_dictionary.md_3`, `parent_chunk_data_dictionary.md_7`, `parent_chunk_data_dictionary.md_4`, `a parent product, a component product (which can be either a component or sub-assembly), the required quantity, unit of measure, and hierarchical level in the product structure→COMPONENT`, `Component Supplier Junction→COMPONENT_SUPPLIER`

**Context previews (first 3):**

1. _## warehouse  Stores physical storage location information for inventory management.  | Column | Data Type | Constraints | Description | |--------|-----------|-------------|-------------| | warehouse_…_

2. _Business concept 'Batches for traceability and inventory management' is implemented by physical table INVENTORY (columns: inventory_id, warehouse_id, component_id, product_id, quantity_on_hand, quanti…_

3. _Relationship: INVENTORY references COMPONENT via foreign key COMPONENT_ID -> COMPONENT.COMPONENT_ID.…_

---

### ✅ QA-018 — How do I determine the manufacturing route for a specific product?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.7482 | **Gate:** `proceed`

**Expected answer:**
> Query the route table filtering by product_id, ordered by sequence_number ascending. For each operation, retrieve operation_name, work_center, cycle_time_minutes, and setup_time_minutes. Join with the product table to get product details. The sequence of operations shows the complete manufacturing w…

**System answer:**
> Use the `ROUTE` table, which implements the `Route Step` concept.

To determine the manufacturing route for a specific product, identify the product in `PRODUCT`, then retrieve all `ROUTE` rows where `ROUTE.product_id = PRODUCT.product_id`. The foreign key relationship is explicitly `ROUTE.PRODUCT_ID -> PRODUCT.PRODUCT_ID`.

The route is stored as ordered manufacturing operations, so the key colum…

**Sources retrieved (12):** `Route Step`, `Route Step→ROUTE`, `parent_chunk_data_dictionary.md_6`, `ROUTE→PRODUCT`, `parent_chunk_data_dictionary.md_3`, `Work Order→WORK_ORDER`, `parent_chunk_data_dictionary.md_7`, `the product produced, production date, quantity produced, warehouse location, expiry date (if applicable), and quality control status→PRODUCT`

**Context previews (first 3):**

1. _Route Step: The table stores ordered manufacturing operations for a product, including operation name, work center, sequence number, cycle time, and setup time, which matches the route step concept ex…_

2. _Business concept 'Route Step' — The table stores ordered manufacturing operations for a product, including operation name, work center, sequence number, cycle time, and setup time, which matches the r…_

3. _## work_order  Represents production jobs for manufacturing products with hierarchical work order support.  | Column | Data Type | Constraints | Description | |--------|-----------|-------------|-----…_

---

### ✅ QA-019 — How can I find which batches are stored at a specific warehouse and their QC status?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.7533 | **Gate:** `proceed`

**Expected answer:**
> Query the batch table filtering by warehouse_id. Join with the product table to get product names and types. Include production_date, quantity_produced, expiry_date, and qc_status (PENDING, PASSED, FAILED, QUARANTINED). Filter by qc_status to isolate batches requiring quality attention or ready for …

**System answer:**
> At the schema level, the direct way is to query the `BATCH` table, because `BATCH` stores both the warehouse reference and the batch QC status.

Use this path:
`WAREHOUSE.warehouse_id` → `BATCH.warehouse_id`

Relevant `BATCH` columns are:
`batch_id`, `product_id`, `production_date`, `quantity_produced`, `warehouse_id`, `expiry_date`, `qc_status`

Relevant `WAREHOUSE` columns are:
`warehouse_id`, `…

**Sources retrieved (12):** `Production batch reference→BATCH`, `parent_chunk_data_dictionary.md_5`, `BATCH→WAREHOUSE`, `Quality Control inspections→QUALITY_CONTROL`, `the product produced, production date, quantity produced, warehouse location, expiry date (if applicable), and quality control status→PRODUCT`, `parent_chunk_data_dictionary.md_6`, `Batches for traceability and inventory management→INVENTORY`, `parent_chunk_data_dictionary.md_8`

**Context previews (first 3):**

1. _Business concept 'Production batch reference' is implemented by physical table BATCH (columns: batch_id, product_id, production_date, quantity_produced, warehouse_id, expiry_date, qc_status).…_

2. _## warehouse  Stores physical storage location information for inventory management.  | Column | Data Type | Constraints | Description | |--------|-----------|-------------|-------------| | warehouse_…_

3. _Relationship: BATCH references WAREHOUSE via foreign key WAREHOUSE_ID -> WAREHOUSE.WAREHOUSE_ID.…_

---

### ✅ QA-020 — How do I identify which specifications apply to specific components?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.2550 | **Gate:** `proceed`

**Expected answer:**
> Query the component table and join with the specification table via specification_id. Include component_name, component_category, and specification details (specification_name, spec_type, critical_parameter, min_value, max_value, unit_of_measure). This shows the technical requirements that each comp…

**System answer:**
> To identify which specifications apply to specific components, use the relationship implied by the `COMPONENT` table’s `specification_id` column and the `SPECIFICATION` table’s primary key `specification_id`.

From the context:
`COMPONENT` includes `component_id`, `component_name`, `component_category`, `unit_of_measure`, `standard_cost`, and `specification_id`.
`SPECIFICATION` includes `specifica…

**Sources retrieved (12):** `a parent product, a component product (which can be either a component or sub-assembly), the required quantity, unit of measure, and hierarchical level in the product structure→COMPONENT`, `parent_chunk_data_dictionary.md_5`, `parent_chunk_data_dictionary.md_7`, `parent_chunk_data_dictionary.md_3`, `a standard cost, unit of measure, and may be associated with technical specifications that define quality requirements→SPECIFICATION`, `parent_chunk_data_dictionary.md_4`, `Component Supplier Junction→COMPONENT_SUPPLIER`, `parent_chunk_business_glossary.md_0`

**Context previews (first 3):**

1. _Business concept 'a parent product, a component product (which can be either a component or sub-assembly), the required quantity, unit of measure, and hierarchical level in the product structure' is i…_

2. _## warehouse  Stores physical storage location information for inventory management.  | Column | Data Type | Constraints | Description | |--------|-----------|-------------|-------------| | warehouse_…_

3. _## specification  Defines technical requirements and acceptance criteria for materials and products.  | Column | Data Type | Constraints | Description | |--------|-----------|-------------|-----------…_

---

### ✅ QA-021 — How can I perform a complete BOM explosion to find all components required for a finished product?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.3509 | **Gate:** `proceed`

**Expected answer:**
> Use a recursive query starting from the product_id of the finished good. At each level, join the bom table to find component_product_id entries. For each component, check if product_type is 'ASSEMBLY' or 'FINISHED_GOOD'. If so, recursively query bom again using that component_product_id as the new p…

**System answer:**
> To perform a complete BOM explosion for a finished product, use the `bom` table as the core hierarchy and the `product` table to identify what each node represents.

Start with the finished product in `product`, using `product.product_id` as the root and `product.product_type = 'FINISHED_GOOD'` if you want to confirm it is a finished good. Then join from that product to `bom` on:

`bom.parent_prod…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_4`, `parent_chunk_data_dictionary.md_3`, `The Bill of Materials (BOM)→BOM`, `BOM→PRODUCT`, `a parent product, a component product (which can be either a component or sub-assembly), the required quantity, unit of measure, and hierarchical level in the product structure→COMPONENT`, `parent_chunk_data_dictionary.md_5`, `parent_chunk_data_dictionary.md_7`, `parent_chunk_data_dictionary.md_6`

**Context previews (first 3):**

1. _## bom  Bill of Materials defining product composition and hierarchical structure. Supports recursive relationships for multi-level assemblies.  | Column | Data Type | Constraints | Description | |---…_

2. _# Manufacturing Data Dictionary  This data dictionary documents the database schema for the manufacturing supply chain system. It includes all tables, columns, data types, constraints, and relationshi…_

3. _Business concept 'The Bill of Materials (BOM)' is implemented by physical table BOM (columns: bom_id, parent_product_id, component_product_id, quantity, unit_of_measure, bom_level, is_optional).…_

---

### ✅ QA-022 — How do I calculate the total material cost for a product including all sub-assemblies?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.2332 | **Gate:** `proceed`

**Expected answer:**
> Perform a recursive BOM explosion to find all leaf-level components. For each leaf component, join with the component table to get standard_cost. Multiply standard_cost by the accumulated quantity from the BOM traversal. Sum all component costs to get total material cost. This calculation must trave…

**System answer:**
> Use the `bom` table to recursively explode the product structure, and use `product.base_cost` as the directly joinable cost field in the retrieved schema.

The schema path is: start with the target product in `product.product_id`, join to `bom.parent_product_id` to get its immediate components in `bom.component_product_id`, then join each `component_product_id` back to `product.product_id`. If a c…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_3`, `a parent product, a component product (which can be either a component or sub-assembly), the required quantity, unit of measure, and hierarchical level in the product structure→COMPONENT`, `parent_chunk_data_dictionary.md_4`, `parent_chunk_data_dictionary.md_7`, `parent_chunk_data_dictionary.md_8`, `The Bill of Materials (BOM)→BOM`, `parent_chunk_data_dictionary.md_6`, `the product produced, production date, quantity produced, warehouse location, expiry date (if applicable), and quality control status→PRODUCT`

**Context previews (first 3):**

1. _# Manufacturing Data Dictionary  This data dictionary documents the database schema for the manufacturing supply chain system. It includes all tables, columns, data types, constraints, and relationshi…_

2. _Business concept 'a parent product, a component product (which can be either a component or sub-assembly), the required quantity, unit of measure, and hierarchical level in the product structure' is i…_

3. _## bom  Bill of Materials defining product composition and hierarchical structure. Supports recursive relationships for multi-level assemblies.  | Column | Data Type | Constraints | Description | |---…_

---

### ✅ QA-023 — How can I find all parent products that contain a specific component anywhere in their BOM structure?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.5213 | **Gate:** `proceed`

**Expected answer:**
> Use a recursive reverse traversal of the BOM. Start with the component_id as the initial parent_product_id. Find all records where this product appears as component_product_id in the bom table. For each parent_product_id found, check if it appears as a component_product_id in other bom records (is a…

**System answer:**
> Use the `bom` table as the recursive hierarchy, because the Bill of Materials is implemented by `BOM(bom_id, parent_product_id, component_product_id, quantity, unit_of_measure, bom_level, is_optional)` and both `parent_product_id` and `component_product_id` are foreign keys to `product(product_id)`.

The schema-level path is:

`PRODUCT` for the target component → `BOM.component_product_id` → `BOM.…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_4`, `parent_chunk_data_dictionary.md_3`, `The Bill of Materials (BOM)→BOM`, `a parent product, a component product (which can be either a component or sub-assembly), the required quantity, unit of measure, and hierarchical level in the product structure→COMPONENT`, `BOM→PRODUCT`, `PRODUCT→PRODUCT`, `parent_chunk_data_dictionary.md_6`, `parent_chunk_data_dictionary.md_8`

**Context previews (first 3):**

1. _## bom  Bill of Materials defining product composition and hierarchical structure. Supports recursive relationships for multi-level assemblies.  | Column | Data Type | Constraints | Description | |---…_

2. _# Manufacturing Data Dictionary  This data dictionary documents the database schema for the manufacturing supply chain system. It includes all tables, columns, data types, constraints, and relationshi…_

3. _Business concept 'The Bill of Materials (BOM)' is implemented by physical table BOM (columns: bom_id, parent_product_id, component_product_id, quantity, unit_of_measure, bom_level, is_optional).…_

---

### ✅ QA-024 — How do I identify work orders that require a specific component, considering nested sub-assemblies?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.3651 | **Gate:** `proceed`

**Expected answer:**
> First, perform reverse BOM traversal to find all parent products that contain the target component at any level. Then query the work_order table where product_id is in the set of parent products found. This includes work orders for finished goods that contain the component indirectly through sub-ass…

**System answer:**
> Use `WORK_ORDER` together with the recursive structure in `BOM`.

At the schema level, the path is:

`WORK_ORDER.product_id` → `BOM.parent_product_id` → `BOM.component_product_id`

To handle nested sub-assemblies, you do not stop at the first `BOM` row. Because `BOM` is explicitly recursive and both `parent_product_id` and `component_product_id` reference `PRODUCT(product_id)`, you repeatedly foll…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_6`, `parent_chunk_data_dictionary.md_5`, `a parent product, a component product (which can be either a component or sub-assembly), the required quantity, unit of measure, and hierarchical level in the product structure→COMPONENT`, `parent_chunk_data_dictionary.md_3`, `parent_chunk_data_dictionary.md_4`, `Work Order→WORK_ORDER`, `WORK_ORDER→WORK_ORDER`, `parent_chunk_business_glossary.md_1`

**Context previews (first 3):**

1. _## work_order  Represents production jobs for manufacturing products with hierarchical work order support.  | Column | Data Type | Constraints | Description | |--------|-----------|-------------|-----…_

2. _## warehouse  Stores physical storage location information for inventory management.  | Column | Data Type | Constraints | Description | |--------|-----------|-------------|-------------| | warehouse_…_

3. _Business concept 'a parent product, a component product (which can be either a component or sub-assembly), the required quantity, unit of measure, and hierarchical level in the product structure' is i…_

---

### ✅ QA-025 — How can I determine the maximum BOM depth level for any product?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.2424 | **Gate:** `proceed`

**Expected answer:**
> Use a recursive query on the bom table, incrementing a level counter at each traversal. Start with bom_level = 0 and add 1 for each recursive step. Track the maximum level reached across all product hierarchies. This identifies the most complex product structures with the deepest nesting.

**System answer:**
> Use the `bom` table, because it stores the hierarchy and explicitly includes `bom_level`, which is “depth in product hierarchy” and is indexed for hierarchical queries.

At the schema level, the maximum BOM depth is the highest value in `bom.bom_level`.

If you want the overall deepest BOM anywhere in the system, take the maximum of `bom_level` across the entire `bom` table.

If you want the maxim…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_4`, `parent_chunk_data_dictionary.md_3`, `The Bill of Materials (BOM)→BOM`, `BOM→PRODUCT`, `parent_chunk_data_dictionary.md_7`, `parent_chunk_data_dictionary.md_5`, `parent_chunk_data_dictionary.md_6`, `a parent product, a component product (which can be either a component or sub-assembly), the required quantity, unit of measure, and hierarchical level in the product structure→COMPONENT`

**Context previews (first 3):**

1. _## bom  Bill of Materials defining product composition and hierarchical structure. Supports recursive relationships for multi-level assemblies.  | Column | Data Type | Constraints | Description | |---…_

2. _# Manufacturing Data Dictionary  This data dictionary documents the database schema for the manufacturing supply chain system. It includes all tables, columns, data types, constraints, and relationshi…_

3. _Business concept 'The Bill of Materials (BOM)' is implemented by physical table BOM (columns: bom_id, parent_product_id, component_product_id, quantity, unit_of_measure, bom_level, is_optional).…_

---

### ✅ QA-026 — How do I find all products that have a specific product as a sub-assembly at any level?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.2948 | **Gate:** `proceed`

**Expected answer:**
> Perform a recursive search starting with the target product_id as the initial component_product_id in the bom table. For each parent_product_id found, check if that parent appears as a component in other bom entries. Continue recursively until reaching products that are not used as components elsewh…

**System answer:**
> Use the `bom` table to trace upward through the product structure.

Start with the specific product in `bom.component_product_id`. Any row where `component_product_id = <target product_id>` gives you an immediate parent in `bom.parent_product_id`; that parent is a product that contains the target as a sub-assembly or component. To find products at any higher level, continue recursively: take each …

**Sources retrieved (12):** `a parent product, a component product (which can be either a component or sub-assembly), the required quantity, unit of measure, and hierarchical level in the product structure→COMPONENT`, `parent_chunk_data_dictionary.md_3`, `parent_chunk_data_dictionary.md_4`, `parent_chunk_data_dictionary.md_5`, `parent_chunk_data_dictionary.md_7`, `The Bill of Materials (BOM)→BOM`, `parent_chunk_data_dictionary.md_6`, `parent_chunk_data_dictionary.md_8`

**Context previews (first 3):**

1. _Business concept 'a parent product, a component product (which can be either a component or sub-assembly), the required quantity, unit of measure, and hierarchical level in the product structure' is i…_

2. _# Manufacturing Data Dictionary  This data dictionary documents the database schema for the manufacturing supply chain system. It includes all tables, columns, data types, constraints, and relationshi…_

3. _## bom  Bill of Materials defining product composition and hierarchical structure. Supports recursive relationships for multi-level assemblies.  | Column | Data Type | Constraints | Description | |---…_

---

### ✅ QA-027 — How can I calculate the total lead time for a product including all sub-assembly lead times?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.3462 | **Gate:** `proceed`

**Expected answer:**
> Perform a recursive BOM explosion to find all components and sub-assemblies. For each product_id in the hierarchy, retrieve lead_time_days from the product table. The total lead time is the maximum of all lead times in the hierarchy (representing the longest dependency chain), or optionally sum lead…

**System answer:**
> From the retrieved context, the schema supports tracing a product’s full multi-level structure, but it does not define a specific business rule for how “total lead time” must be aggregated. What can be answered from the knowledge graph is how to derive it structurally.

Use the `product` table as the starting point for the finished item. Its `lead_time_days` column stores the procurement or produc…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_3`, `the product produced, production date, quantity produced, warehouse location, expiry date (if applicable), and quality control status→PRODUCT`, `Component Supplier Junction→COMPONENT_SUPPLIER`, `a parent product, a component product (which can be either a component or sub-assembly), the required quantity, unit of measure, and hierarchical level in the product structure→COMPONENT`, `parent_chunk_data_dictionary.md_4`, `Route Step→ROUTE`, `parent_chunk_data_dictionary.md_7`, `parent_chunk_data_dictionary.md_6`

**Context previews (first 3):**

1. _# Manufacturing Data Dictionary  This data dictionary documents the database schema for the manufacturing supply chain system. It includes all tables, columns, data types, constraints, and relationshi…_

2. _Business concept 'the product produced, production date, quantity produced, warehouse location, expiry date (if applicable), and quality control status' is implemented by physical table PRODUCT (colum…_

3. _Business concept 'Component Supplier Junction' — The table is explicitly a many-to-many junction between component and supplier, with a uniqueness constraint on the pair and fields for preferred statu…_

---

### ✅ QA-028 — How do I generate a complete indented BOM report showing the hierarchical structure?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.4180 | **Gate:** `proceed`

**Expected answer:**
> Use a recursive query on the bom table that tracks the current depth level. Start with the top-level product (parent_product_id where product has no parent_product_id). At each level, output component details indented by depth level. Include product_name, quantity, and unit_of_measure. Recursively p…

**System answer:**
> Use the `bom` table as the primary hierarchy source and join it to `product` twice: once for the parent item and once for the component item. The core path is `bom.parent_product_id → product.product_id` for the assembly being built, and `bom.component_product_id → product.product_id` for the child item included in that assembly.

To generate a complete indented BOM report, start with the top-leve…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_4`, `parent_chunk_data_dictionary.md_3`, `a parent product, a component product (which can be either a component or sub-assembly), the required quantity, unit of measure, and hierarchical level in the product structure→COMPONENT`, `parent_chunk_data_dictionary.md_6`, `parent_chunk_data_dictionary.md_8`, `The Bill of Materials (BOM)→BOM`, `Work Order→WORK_ORDER`, `parent_chunk_business_glossary.md_0`

**Context previews (first 3):**

1. _## bom  Bill of Materials defining product composition and hierarchical structure. Supports recursive relationships for multi-level assemblies.  | Column | Data Type | Constraints | Description | |---…_

2. _# Manufacturing Data Dictionary  This data dictionary documents the database schema for the manufacturing supply chain system. It includes all tables, columns, data types, constraints, and relationshi…_

3. _Business concept 'a parent product, a component product (which can be either a component or sub-assembly), the required quantity, unit of measure, and hierarchical level in the product structure' is i…_

---

### ✅ QA-029 — How can I find which components appear most frequently across all product BOMs?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.1587 | **Gate:** `proceed_with_warning`

**Expected answer:**
> Perform BOM explosion for all products and aggregate occurrences of each leaf-level component. Count how many distinct product hierarchies contain each component. Join with component table for component names. Order by frequency descending to identify common components that should be prioritized for…

**System answer:**
> Use the BOM table as the primary source, because the business concept “The Bill of Materials (BOM)” is implemented by physical table BOM with the columns `bom_id`, `parent_product_id`, `component_product_id`, `quantity`, `unit_of_measure`, `bom_level`, and `is_optional`.

At the schema level, the basic way to find which components appear most frequently is to count how often each `BOM.component_pr…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_4`, `parent_chunk_data_dictionary.md_3`, `The Bill of Materials (BOM)→BOM`, `BOM→PRODUCT`, `parent_chunk_data_dictionary.md_5`, `a parent product, a component product (which can be either a component or sub-assembly), the required quantity, unit of measure, and hierarchical level in the product structure→COMPONENT`, `parent_chunk_data_dictionary.md_7`, `Batches for traceability and inventory management→INVENTORY`

**Context previews (first 3):**

1. _## bom  Bill of Materials defining product composition and hierarchical structure. Supports recursive relationships for multi-level assemblies.  | Column | Data Type | Constraints | Description | |---…_

2. _# Manufacturing Data Dictionary  This data dictionary documents the database schema for the manufacturing supply chain system. It includes all tables, columns, data types, constraints, and relationshi…_

3. _Business concept 'The Bill of Materials (BOM)' is implemented by physical table BOM (columns: bom_id, parent_product_id, component_product_id, quantity, unit_of_measure, bom_level, is_optional).…_

---

### ✅ QA-030 — How do I detect circular references in the BOM structure to prevent infinite loops?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.1295 | **Gate:** `proceed_with_warning`

**Expected answer:**
> Use a recursive query with a cycle detection check. Track the path of visited product_ids at each recursion level. If a product_id appears twice in the same path, a circular reference exists. Alternatively, check if any bom record has parent_product_id = component_product_id (direct self-reference),…

**System answer:**
> From the retrieved context, the BOM hierarchy is modeled in the `bom` table using `parent_product_id` and `component_product_id`, and both columns are foreign keys to `product(product_id)`. That means the BOM is recursive and supports multi-level assemblies. The relevant schema elements are `bom.parent_product_id`, `bom.component_product_id`, and `bom.bom_level`; there is also an index on `parent_…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_4`, `parent_chunk_data_dictionary.md_3`, `BOM→PRODUCT`, `The Bill of Materials (BOM)→BOM`, `parent_chunk_data_dictionary.md_8`, `parent_chunk_data_dictionary.md_7`, `parent_chunk_business_glossary.md_0`, `The Bill of Materials (BOM)`

**Context previews (first 3):**

1. _## bom  Bill of Materials defining product composition and hierarchical structure. Supports recursive relationships for multi-level assemblies.  | Column | Data Type | Constraints | Description | |---…_

2. _# Manufacturing Data Dictionary  This data dictionary documents the database schema for the manufacturing supply chain system. It includes all tables, columns, data types, constraints, and relationshi…_

3. _Relationship: BOM references PRODUCT via foreign key COMPONENT_PRODUCT_ID -> PRODUCT.PRODUCT_ID.…_

---

### ✅ QA-031 — How can I determine the complete supplier chain for a finished product, including suppliers for all sub-assemblies?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.4929 | **Gate:** `proceed`

**Expected answer:**
> First, perform recursive BOM explosion to find all leaf-level components in the product hierarchy. Then query the component_supplier table for each component_id to find approved suppliers. Join with the supplier table to get supplier names, ratings, and contact information. Include supplier-specific…

**System answer:**
> From the retrieved context, you can determine the full product structure of a finished product, but you cannot fully determine the complete supplier chain for that structure.

What is supported is the hierarchical explosion of the finished product through `bom` and `product`. Start with the finished good in `product` using `product.product_id`, then traverse `bom.parent_product_id -> bom.component…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_3`, `a parent product, a component product (which can be either a component or sub-assembly), the required quantity, unit of measure, and hierarchical level in the product structure→COMPONENT`, `parent_chunk_data_dictionary.md_4`, `parent_chunk_data_dictionary.md_8`, `parent_chunk_data_dictionary.md_6`, `parent_chunk_data_dictionary.md_7`, `Component Supplier Junction→COMPONENT_SUPPLIER`, `parent_chunk_business_glossary.md_0`

**Context previews (first 3):**

1. _# Manufacturing Data Dictionary  This data dictionary documents the database schema for the manufacturing supply chain system. It includes all tables, columns, data types, constraints, and relationshi…_

2. _Business concept 'a parent product, a component product (which can be either a component or sub-assembly), the required quantity, unit of measure, and hierarchical level in the product structure' is i…_

3. _## bom  Bill of Materials defining product composition and hierarchical structure. Supports recursive relationships for multi-level assemblies.  | Column | Data Type | Constraints | Description | |---…_

---

### ✅ QA-032 — How do I check if sufficient inventory exists across all warehouses to fulfill a work order?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.4035 | **Gate:** `proceed`

**Expected answer:**
> For the work_order's product_id, perform recursive BOM explosion to get all required components with quantities. For each component, sum the available quantity (quantity_on_hand - quantity_reserved) across all warehouses from the inventory table. Compare aggregated available inventory against requir…

**System answer:**
> Use the `WORK_ORDER` and `INVENTORY` tables.

At the schema level, the check is:

1. Find the work order in `WORK_ORDER` by `work_order_id`.
2. Use `WORK_ORDER.product_id` to find matching product inventory rows in `INVENTORY.product_id`.
3. Sum inventory across all warehouses, using `INVENTORY.warehouse_id` if you want to see the warehouse-by-warehouse breakdown or join to `WAREHOUSE` for warehou…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_5`, `parent_chunk_data_dictionary.md_6`, `Work Order→WORK_ORDER`, `INVENTORY→WAREHOUSE`, `WORK_ORDER→WAREHOUSE`, `Batches for traceability and inventory management→INVENTORY`, `parent_chunk_data_dictionary.md_8`, `parent_chunk_data_dictionary.md_7`

**Context previews (first 3):**

1. _## warehouse  Stores physical storage location information for inventory management.  | Column | Data Type | Constraints | Description | |--------|-----------|-------------|-------------| | warehouse_…_

2. _## work_order  Represents production jobs for manufacturing products with hierarchical work order support.  | Column | Data Type | Constraints | Description | |--------|-----------|-------------|-----…_

3. _Business concept 'Work Order' — The table is explicitly labeled as a work order / production jobs table and contains the core attributes of a manufacturing job: product, planned quantities, status, pr…_

---

### ✅ QA-033 — How can I find which quality control inspections failed for components from specific suppliers?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.4561 | **Gate:** `proceed`

**Expected answer:**
> Query the quality_control table filtering by result = 'FAIL'. Join with the batch table to get product_id and production_date. Join with the bom table recursively to trace which products contain failed components. Join with component_supplier and supplier tables to identify the source supplier. Filt…

**System answer:**
> From the retrieved context, the part that is directly supported is the quality-control side and the component-to-supplier side, but the context does not provide the full join path between them.

The supported schema facts are:

`QUALITY_CONTROL` implements the business concept “Quality Control inspections” and has these columns: `qc_id`, `batch_id`, `specification_id`, `qc_date`, `qc_type`, `inspe…

**Sources retrieved (12):** `Quality Control inspections→QUALITY_CONTROL`, `parent_chunk_data_dictionary.md_5`, `parent_chunk_data_dictionary.md_3`, `Component Supplier Junction→COMPONENT_SUPPLIER`, `parent_chunk_data_dictionary.md_4`, `COMPONENT_SUPPLIER→SUPPLIER`, `parent_chunk_data_dictionary.md_8`, `parent_chunk_business_glossary.md_2`

**Context previews (first 3):**

1. _Business concept 'Quality Control inspections' is implemented by physical table QUALITY_CONTROL (columns: qc_id, batch_id, specification_id, qc_date, qc_type, inspector_id, result, defect_count, notes…_

2. _## warehouse  Stores physical storage location information for inventory management.  | Column | Data Type | Constraints | Description | |--------|-----------|-------------|-------------| | warehouse_…_

3. _# Manufacturing Data Dictionary  This data dictionary documents the database schema for the manufacturing supply chain system. It includes all tables, columns, data types, constraints, and relationshi…_

---

### ✅ QA-034 — How do I calculate the total manufacturing time for a work order including all sub-assembly work orders?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.1599 | **Gate:** `proceed_with_warning`

**Expected answer:**
> Query the work_order table starting with the parent work_order. Find all child work_orders where parent_work_order matches the current work_order_id. For each work order (parent and children), join with the route table on product_id to get all operations. Sum (cycle_time_minutes * quantity) plus set…

**System answer:**
> From the retrieved context, the schema supports a work-order-tree plus route-step aggregation approach.

The relevant join path is:

WORK_ORDER.work_order_id → recursively to WORK_ORDER.parent_work_order to collect the main work order and all child/sub-assembly work orders, then for each of those work orders use WORK_ORDER.product_id → ROUTE.product_id.

That path is supported by these facts in th…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_6`, `Work Order→WORK_ORDER`, `parent_chunk_data_dictionary.md_3`, `Route Step→ROUTE`, `Route Step`, `a parent product, a component product (which can be either a component or sub-assembly), the required quantity, unit of measure, and hierarchical level in the product structure→COMPONENT`, `parent_chunk_data_dictionary.md_7`, `parent_chunk_data_dictionary.md_5`

**Context previews (first 3):**

1. _## work_order  Represents production jobs for manufacturing products with hierarchical work order support.  | Column | Data Type | Constraints | Description | |--------|-----------|-------------|-----…_

2. _Business concept 'Work Order' — The table is explicitly labeled as a work order / production jobs table and contains the core attributes of a manufacturing job: product, planned quantities, status, pr…_

3. _# Manufacturing Data Dictionary  This data dictionary documents the database schema for the manufacturing supply chain system. It includes all tables, columns, data types, constraints, and relationshi…_

---

### ✅ QA-035 — How can I identify which shipments are overdue and their impact on work orders?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0719 | **Gate:** `proceed_with_warning`

**Expected answer:**
> Query the shipment table filtering for status = 'SHIPPED' where actual_arrival is NULL and estimated_arrival is in the past (overdue). Join with the component_supplier table via supplier_id and component_id to identify which components are delayed. Perform reverse BOM lookup to find which parent pro…

**System answer:**
> From the provided schema, you can identify overdue shipments from `SHIPMENT` using the date and status fields, and then assess likely work-order impact through the shared `warehouse_id`.

A shipment can be evaluated with these `SHIPMENT` columns: `shipment_id`, `shipment_type`, `warehouse_id`, `ship_date`, `estimated_arrival`, `actual_arrival`, and `status`. The available shipment statuses are `PE…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_5`, `parent_chunk_data_dictionary.md_8`, `parent_chunk_data_dictionary.md_6`, `Work Order→WORK_ORDER`, `WORK_ORDER→PRODUCT`, `WORK_ORDER→WAREHOUSE`, `shipment_type_t ENUM ('INBOUND', 'OUTBOUND', 'INTERNAL')→SHIPMENT`, `SHIPMENT→WAREHOUSE`

**Context previews (first 3):**

1. _## warehouse  Stores physical storage location information for inventory management.  | Column | Data Type | Constraints | Description | |--------|-----------|-------------|-------------| | warehouse_…_

2. _## shipment  Tracks material transfers between warehouses, suppliers, and customers.  | Column | Data Type | Constraints | Description | |--------|-----------|-------------|-------------| | shipment_i…_

3. _## work_order  Represents production jobs for manufacturing products with hierarchical work order support.  | Column | Data Type | Constraints | Description | |--------|-----------|-------------|-----…_

---

### ✅ QA-036 — How do I find which batches are approaching or past expiry and contain components from specific suppliers?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.1479 | **Gate:** `proceed_with_warning`

**Expected answer:**
> Query the batch table filtering for expiry_date within a warning window (e.g., next 30 days) or past expiry. Join with the bom table recursively on product_id to trace all components used in those batches. Join with component_supplier and supplier tables to filter by specific suppliers. Results iden…

**System answer:**
> From the retrieved context, only part of this can be answered.

What is known:
The relevant table for expiry is BATCH, which stores batch_id, product_id, production_date, quantity_produced, warehouse_id, expiry_date, and qc_status. So batches that are past expiry or nearing expiry would have to be identified from BATCH.expiry_date. The context also says batches are used for traceability and invent…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_5`, `parent_chunk_data_dictionary.md_7`, `Batches for traceability and inventory management→INVENTORY`, `parent_chunk_data_dictionary.md_3`, `Production batch reference→BATCH`, `parent_chunk_data_dictionary.md_8`, `Component Supplier Junction→COMPONENT_SUPPLIER`, `parent_chunk_data_dictionary.md_4`

**Context previews (first 3):**

1. _## warehouse  Stores physical storage location information for inventory management.  | Column | Data Type | Constraints | Description | |--------|-----------|-------------|-------------| | warehouse_…_

2. _## specification  Defines technical requirements and acceptance criteria for materials and products.  | Column | Data Type | Constraints | Description | |--------|-----------|-------------|-----------…_

3. _Business concept 'Batches for traceability and inventory management' is implemented by physical table INVENTORY (columns: inventory_id, warehouse_id, component_id, product_id, quantity_on_hand, quanti…_

---

### ✅ QA-037 — How can I generate a material requirements plan showing when to order components based on work order schedules?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0433 | **Gate:** `proceed_with_warning`

**Expected answer:**
> Query all work_orders with status 'PENDING' ordered by planned_start_date. For each work_order, perform BOM explosion to get required components and quantities. For each component, query inventory for current available stock across warehouses. Calculate net requirements = (required quantity * work_o…

**System answer:**
> The retrieved context does not define a full, approved material requirements planning procedure, so I cannot determine the exact business rule for “when to order” components. In particular, the context does not provide purchase order tables, supplier-ordering workflow, lot-sizing rules, safety stock policy, calendar logic, or a documented MRP formula. What it does provide is enough to outline a sc…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_6`, `parent_chunk_data_dictionary.md_7`, `Work Order→WORK_ORDER`, `parent_chunk_data_dictionary.md_5`, `parent_chunk_data_dictionary.md_4`, `parent_chunk_data_dictionary.md_3`, `Component Supplier Junction→COMPONENT_SUPPLIER`, `parent_chunk_business_glossary.md_1`

**Context previews (first 3):**

1. _## work_order  Represents production jobs for manufacturing products with hierarchical work order support.  | Column | Data Type | Constraints | Description | |--------|-----------|-------------|-----…_

2. _## specification  Defines technical requirements and acceptance criteria for materials and products.  | Column | Data Type | Constraints | Description | |--------|-----------|-------------|-----------…_

3. _Business concept 'Work Order' — The table is explicitly labeled as a work order / production jobs table and contains the core attributes of a manufacturing job: product, planned quantities, status, pr…_

---

### ✅ QA-038 — How do I trace the complete genealogy of a component from supplier through batch to finished goods?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0748 | **Gate:** `proceed_with_warning`

**Expected answer:**
> Start with a shipment from the supplier (shipment table with supplier_id and shipment_type = 'INBOUND'). Track to inventory updates via component_id and warehouse_id. Identify batches that consumed the component via reverse BOM lookup (batch.product_id → bom hierarchy → component_id). Query quality_…

**System answer:**
> From the retrieved context, you can only trace this genealogy partially, not completely.

At the supplier end, the starting point is `COMPONENT_SUPPLIER`, which is the many-to-many junction between components and suppliers. Use `COMPONENT_SUPPLIER.component_id` to identify the component, and `COMPONENT_SUPPLIER.supplier_id` to reach the supplier. This table also carries procurement terms for that …

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_3`, `parent_chunk_data_dictionary.md_7`, `parent_chunk_data_dictionary.md_5`, `parent_chunk_data_dictionary.md_8`, `Batches for traceability and inventory management→INVENTORY`, `Component Supplier Junction→COMPONENT_SUPPLIER`, `parent_chunk_data_dictionary.md_4`, `parent_chunk_business_glossary.md_2`

**Context previews (first 3):**

1. _# Manufacturing Data Dictionary  This data dictionary documents the database schema for the manufacturing supply chain system. It includes all tables, columns, data types, constraints, and relationshi…_

2. _## specification  Defines technical requirements and acceptance criteria for materials and products.  | Column | Data Type | Constraints | Description | |--------|-----------|-------------|-----------…_

3. _## warehouse  Stores physical storage location information for inventory management.  | Column | Data Type | Constraints | Description | |--------|-----------|-------------|-------------| | warehouse_…_

---

### ✅ QA-039 — How can I find alternative suppliers for components that are critical for multiple products?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0772 | **Gate:** `proceed_with_warning`

**Expected answer:**
> Perform BOM explosion for all active products and count component usage frequency. Identify high-frequency components. Query component_supplier table to find all suppliers for these components. Filter to suppliers with rating >= 4.0 (high quality) and is_preferred = 'Y'. For each component, list alt…

**System answer:**
> From the retrieved context, I can only answer this at the schema level, and only partially.

What is clear is that the “alternative suppliers” side is modeled by `COMPONENT_SUPPLIER`, which is explicitly a many-to-many junction between components and suppliers. It contains `component_id`, `supplier_id`, `is_preferred`, `lead_time_days`, and `unit_price`, with a uniqueness constraint on the compone…

**Sources retrieved (12):** `Component Supplier Junction→COMPONENT_SUPPLIER`, `parent_chunk_data_dictionary.md_4`, `parent_chunk_data_dictionary.md_3`, `Preferred supplier for this component→SUPPLIER`, `parent_chunk_data_dictionary.md_5`, `parent_chunk_data_dictionary.md_8`, `parent_chunk_data_dictionary.md_7`, `COMPONENT_SUPPLIER→COMPONENT`

**Context previews (first 3):**

1. _Business concept 'Component Supplier Junction' — The table is explicitly a many-to-many junction between component and supplier, with a uniqueness constraint on the pair and fields for preferred statu…_

2. _## bom  Bill of Materials defining product composition and hierarchical structure. Supports recursive relationships for multi-level assemblies.  | Column | Data Type | Constraints | Description | |---…_

3. _# Manufacturing Data Dictionary  This data dictionary documents the database schema for the manufacturing supply chain system. It includes all tables, columns, data types, constraints, and relationshi…_

---

### ✅ QA-040 — How do I calculate the total landed cost for a product including component costs, supplier lead times, and manufacturing operations?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.1922 | **Gate:** `proceed_with_warning`

**Expected answer:**
> Perform recursive BOM explosion to get all leaf components. For each component, query component_supplier to get unit_price from primary supplier. Multiply by accumulated BOM quantity for material cost. Add shipping costs (estimated from shipment history). Query route table for the product to get all…

**System answer:**
> From the retrieved context, a complete total landed cost calculation cannot be determined.

What is available is this schema-level information:

For the product itself, the `product` table contains `product_id`, `base_cost`, and `lead_time_days`. That means you can identify a product’s stored base manufacturing cost directly from `product.base_cost`, and its own procurement or production lead time…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_3`, `Route Step`, `Component Supplier Junction→COMPONENT_SUPPLIER`, `Route Step→ROUTE`, `the product produced, production date, quantity produced, warehouse location, expiry date (if applicable), and quality control status→PRODUCT`, `a parent product, a component product (which can be either a component or sub-assembly), the required quantity, unit of measure, and hierarchical level in the product structure→COMPONENT`, `parent_chunk_data_dictionary.md_6`, `parent_chunk_data_dictionary.md_7`

**Context previews (first 3):**

1. _# Manufacturing Data Dictionary  This data dictionary documents the database schema for the manufacturing supply chain system. It includes all tables, columns, data types, constraints, and relationshi…_

2. _Route Step: The table stores ordered manufacturing operations for a product, including operation name, work center, sequence number, cycle time, and setup time, which matches the route step concept ex…_

3. _Business concept 'Component Supplier Junction' — The table is explicitly a many-to-many junction between component and supplier, with a uniqueness constraint on the pair and fields for preferred statu…_

---

## Anomalies & Observations

No anomalies detected. All questions grounded with acceptable RAGAS scores.
