# AB-16 — 04_complex_manufacturing — Run Analysis

**Timestamp:** 2026-03-31 05:13:26  
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
| Triplets extracted | 429 |
| Entities resolved | 127 |
| Tables parsed | 13 |
| Tables completed | 13 |

## Query Evaluation Summary

| Metric | Value |
|--------|-------|
| Questions | 40 |
| Grounded | **40/40 (100%)** |
| Avg GT Coverage | 100% |
| Avg Top Score | 0.4157 |
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
> Products are stored in the `product` table, which represents any manufactured item in the system, including finished goods, assemblies, and components. For each product, the system stores a unique `product_id` (`VARCHAR(20)`, primary key), `product_name` (`VARCHAR(100)`, not null), `product_type` (`product_type_t`, not null, default `FINISHED_GOOD`) with allowed classifications `FINISHED_GOOD`, `A…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_3`, `Work Order→WORK_ORDER`, `parent_chunk_data_dictionary.md_6`, `parent_chunk_data_dictionary.md_5`, `parent_chunk_data_dictionary.md_7`, `parent_chunk_business_glossary.md_0`, `parent_chunk_business_glossary.md_1`, `parent_chunk_business_glossary.md_2`

**Context previews (first 3):**

1. _# Manufacturing Data Dictionary  This data dictionary documents the database schema for the manufacturing supply chain system. It includes all tables, columns, data types, constraints, and relationshi…_

2. _Business concept 'Work Order' — The table is explicitly described as production jobs and contains core work order attributes such as product, ordered/completed quantities, status, priority, planned da…_

3. _## work_order  Represents production jobs for manufacturing products with hierarchical work order support.  | Column | Data Type | Constraints | Description | |--------|-----------|-------------|-----…_

---

### ✅ QA-002 — How are components defined in the manufacturing database?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.5910 | **Gate:** `proceed`

**Expected answer:**
> Components are defined with a unique identifier (component_id), descriptive name (component_name), category grouping (component_category), unit of measure (unit_of_measure), standard unit cost (standard_cost), and optional reference to technical specifications (specification_id). Components represen…

**System answer:**
> Components are defined in the manufacturing database at both the business-concept level and the schema level.

At the business level, a Component is described as an atomic raw material or purchased part that cannot be further broken down into simpler manufactured items. Components are the building blocks used in manufacturing and are procured from external suppliers.

At the schema level, componen…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_3`, `a parent product, a component product (which can be either a component or sub-assembly), the required quantity, unit of measure, and hierarchical level in the product structure→COMPONENT`, `parent_chunk_data_dictionary.md_4`, `The Bill of Materials (BOM)→BOM`, `parent_chunk_data_dictionary.md_5`, `Component Supplier→COMPONENT_SUPPLIER`, `Component Supplier`, `parent_chunk_business_glossary.md_0`

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
> The Bill of Materials (BOM) table defines product composition and hierarchical structure. It records which component products go into a parent product, along with the required quantity, unit of measure, BOM level, and whether a component is optional. It supports recursive, multi-level assemblies because both `parent_product_id` and `component_product_id` reference `product(product_id)`, enabling s…

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
> The system maintains supplier information at three related schema levels.

In the supplier master table, SUPPLIER stores external vendor information for component procurement. From the context, this includes supplier_id, supplier_name, contact_email, contact_phone, rating, and is_preferred. The table description also shows supplier_id as the primary key and supplier_name as required.

For supplier…

**Sources retrieved (12):** `Preferred supplier for this component→SUPPLIER`, `parent_chunk_data_dictionary.md_4`, `Component Supplier`, `SHIPMENT→SUPPLIER`, `Component Supplier→COMPONENT_SUPPLIER`, `Shipment`, `parent_chunk_data_dictionary.md_8`, `COMPONENT_SUPPLIER→SUPPLIER`

**Context previews (first 3):**

1. _Business concept 'Preferred supplier for this component' is implemented by physical table SUPPLIER (columns: supplier_id, supplier_name, contact_email, contact_phone, rating, is_preferred).…_

2. _## bom  Bill of Materials defining product composition and hierarchical structure. Supports recursive relationships for multi-level assemblies.  | Column | Data Type | Constraints | Description | |---…_

3. _Component Supplier: The table is explicitly described as a many-to-many relationship linking components to approved suppliers, and its foreign keys plus unique constraint confirm it is the junction en…_

---

### ✅ QA-005 — How are warehouses represented in the schema?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.3381 | **Gate:** `proceed`

**Expected answer:**
> Warehouses are defined with a unique identifier (warehouse_id), descriptive name (warehouse_name), full street address (address), city location (city), state or province (state), total storage capacity in cubic meters (capacity), and optional manager identifier (manager_id).

**System answer:**
> Warehouses are represented by the physical table `WAREHOUSE`, which implements the business concept of a warehouse as a physical storage location and also the concept of geographic location information.

In the schema, `WAREHOUSE` stores these columns: `warehouse_id` as the primary key and unique warehouse identifier, `warehouse_name`, `address`, `city`, `state`, `capacity`, and `manager_id`. The …

**Sources retrieved (12):** `INVENTORY→WAREHOUSE`, `BATCH→WAREHOUSE`, `WORK_ORDER→WAREHOUSE`, `SHIPMENT→WAREHOUSE`, `parent_chunk_data_dictionary.md_6`, `parent_chunk_data_dictionary.md_5`, `geographic location information→WAREHOUSE`, `Shipment`

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
> The `inventory` table tracks stock levels of components and products at specific warehouse locations. It represents the actual inventory held in a warehouse and includes:

`inventory_id` as the unique inventory record identifier, `warehouse_id` for the warehouse location, `component_id` or `product_id` as the stored item reference, `quantity_on_hand`, `quantity_reserved`, `reorder_threshold`, and …

**Sources retrieved (12):** `INVENTORY→PRODUCT`, `Batches for traceability and inventory management→INVENTORY`, `INVENTORY→WAREHOUSE`, `INVENTORY→COMPONENT`, `parent_chunk_data_dictionary.md_5`, `Batches for traceability and inventory management→BATCH`, `parent_chunk_data_dictionary.md_7`, `parent_chunk_data_dictionary.md_8`

**Context previews (first 3):**

1. _Relationship: INVENTORY references PRODUCT via foreign key PRODUCT_ID -> PRODUCT.PRODUCT_ID.…_

2. _Business concept 'Batches for traceability and inventory management' is implemented by physical table INVENTORY (columns: inventory_id, warehouse_id, component_id, product_id, quantity_on_hand, quanti…_

3. _Relationship: INVENTORY references WAREHOUSE via foreign key WAREHOUSE_ID -> WAREHOUSE.WAREHOUSE_ID.…_

---

### ✅ QA-007 — How are work orders structured in the manufacturing system?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.7343 | **Gate:** `proceed`

**Expected answer:**
> Work orders represent production jobs with a unique identifier (work_order_id), product to be manufactured (product_id), optional parent work order for nested hierarchies (parent_work_order), quantity to produce (quantity_ordered), quantity completed so far (quantity_completed), current status (PEND…

**System answer:**
> Work orders in the manufacturing system are structured as production jobs in the `WORK_ORDER` table, which implements the business concept of a manufacturing work order for hierarchical production planning and tracking.

Each work order is identified by `work_order_id` and is tied to the product being manufactured through `product_id`, which is a required foreign key to `PRODUCT.PRODUCT_ID`. The t…

**Sources retrieved (12):** `Work Order→WORK_ORDER`, `parent_chunk_data_dictionary.md_6`, `WORK_ORDER→PRODUCT`, `WORK_ORDER→WORK_ORDER`, `parent_chunk_data_dictionary.md_3`, `WORK_ORDER→WAREHOUSE`, `a parent product, a component product (which can be either a component or sub-assembly), the required quantity, unit of measure, and hierarchical level in the product structure→COMPONENT`, `parent_chunk_data_dictionary.md_8`

**Context previews (first 3):**

1. _Business concept 'Work Order' — The table is explicitly described as production jobs and contains core work order attributes such as product, ordered/completed quantities, status, priority, planned da…_

2. _## work_order  Represents production jobs for manufacturing products with hierarchical work order support.  | Column | Data Type | Constraints | Description | |--------|-----------|-------------|-----…_

3. _Relationship: WORK_ORDER references PRODUCT via foreign key PRODUCT_ID -> PRODUCT.PRODUCT_ID.…_

---

### ✅ QA-008 — What information is captured in the shipment table?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.9810 | **Gate:** `proceed`

**Expected answer:**
> Shipments track material transfers with a unique identifier (shipment_id), shipment type (INBOUND from suppliers, OUTBOUND to customers, INTERNAL between warehouses), destination warehouse (warehouse_id), source supplier for inbound (supplier_id), destination customer for outbound (customer_id), shi…

**System answer:**
> The SHIPMENT table captures material transfer information between warehouses, suppliers, and customers. It records the unique shipment identifier in shipment_id, the shipment category in shipment_type, the related warehouse in warehouse_id, the supplier in supplier_id, and the customer in customer_id.

It also captures shipment timing and lifecycle details: ship_date, estimated_arrival, actual_arr…

**Sources retrieved (12):** `Shipment`, `Shipment→SHIPMENT`, `SHIPMENT→WAREHOUSE`, `SHIPMENT→SUPPLIER`, `parent_chunk_data_dictionary.md_8`, `parent_chunk_data_dictionary.md_5`, `parent_chunk_business_glossary.md_0`, `parent_chunk_business_glossary.md_1`

**Context previews (first 3):**

1. _Shipment: The table is explicitly labeled as SHIPMENT and contains shipment-specific fields such as shipment_type, ship_date, estimated_arrival, actual_arrival, and status. Its foreign keys to warehou…_

2. _Business concept 'Shipment' — The table is explicitly labeled as SHIPMENT and contains shipment-specific fields such as shipment_type, ship_date, estimated_arrival, actual_arrival, and status. Its for…_

3. _Relationship: SHIPMENT references WAREHOUSE via foreign key WAREHOUSE_ID -> WAREHOUSE.WAREHOUSE_ID.…_

---

### ✅ QA-009 — How does the quality control system record inspections?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.9540 | **Gate:** `proceed`

**Expected answer:**
> Quality control records are stored with a unique identifier (qc_id), associated production batch (batch_id), applicable specification requirements (specification_id), inspection date (qc_date), inspection type (INCOMING for supplier materials, IN_PROCESS during manufacturing, FINAL for finished good…

**System answer:**
> The quality control system records inspections in the `QUALITY_CONTROL` table, which implements the business concept “inspection and testing records for quality assurance.” Each inspection is stored as one QC record with these fields: `qc_id`, `batch_id`, `specification_id`, `qc_date`, `qc_type`, `inspector_id`, `result`, `defect_count`, and `notes`.

From the business description, a QC record rep…

**Sources retrieved (12):** `inspection and testing records for quality assurance→QUALITY_CONTROL`, `BOM→PRODUCT`, `parent_chunk_data_dictionary.md_3`, `BATCH→PRODUCT`, `BATCH→WAREHOUSE`, `parent_chunk_business_glossary.md_2`, `inspection and testing records for quality assurance`, `parent_chunk_business_glossary.md_0`

**Context previews (first 3):**

1. _Business concept 'inspection and testing records for quality assurance' is implemented by physical table QUALITY_CONTROL (columns: qc_id, batch_id, specification_id, qc_date, qc_type, inspector_id, re…_

2. _Relationship: BOM references PRODUCT via foreign key COMPONENT_PRODUCT_ID -> PRODUCT.PRODUCT_ID.…_

3. _# Manufacturing Data Dictionary  This data dictionary documents the database schema for the manufacturing supply chain system. It includes all tables, columns, data types, constraints, and relationshi…_

---

### ✅ QA-010 — What do specification records define?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.7558 | **Gate:** `proceed`

**Expected answer:**
> Specifications define technical requirements with a unique identifier (specification_id), descriptive name (specification_name), version number, effective date, specification type (DIMENSIONAL, MATERIAL, PERFORMANCE), critical parameter being measured (critical_parameter), acceptable minimum value (…

**System answer:**
> Specification records define the technical requirements, standards, and acceptance criteria for materials and products. In this schema, a specification includes the specification name, version, effective date, specification type (`DIMENSIONAL`, `MATERIAL`, or `PERFORMANCE`), the critical parameter being tested, and the acceptable minimum and maximum values with a unit of measure. These records are…

**Sources retrieved (12):** `inspection and testing records for quality assurance→QUALITY_CONTROL`, `version numbers, effective dates, specification types (dimensional, material, performance), critical parameters to test, and acceptable value ranges with units of measure→SPECIFICATION`, `parent_chunk_data_dictionary.md_7`, `a parent product, a component product (which can be either a component or sub-assembly), the required quantity, unit of measure, and hierarchical level in the product structure→COMPONENT`, `parent_chunk_data_dictionary.md_3`, `parent_chunk_business_glossary.md_2`, `parent_chunk_business_glossary.md_0`, `version numbers, effective dates, specification types (dimensional, material, performance), critical parameters to test, and acceptable value ranges with units of measure`

**Context previews (first 3):**

1. _Business concept 'inspection and testing records for quality assurance' is implemented by physical table QUALITY_CONTROL (columns: qc_id, batch_id, specification_id, qc_date, qc_type, inspector_id, re…_

2. _Business concept 'version numbers, effective dates, specification types (dimensional, material, performance), critical parameters to test, and acceptable value ranges with units of measure' is impleme…_

3. _## specification  Defines technical requirements and acceptance criteria for materials and products.  | Column | Data Type | Constraints | Description | |--------|-----------|-------------|-----------…_

---

### ✅ QA-011 — How can I find which suppliers provide specific components?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.1645 | **Gate:** `proceed_with_warning`

**Expected answer:**
> Query the component_supplier table which links components to their approved suppliers. This table contains the component identifier (component_id), supplier identifier (supplier_id), preferred supplier flag (is_preferred), lead time in days (lead_time_days), and unit price (unit_price). Join with th…

**System answer:**
> Use the `COMPONENT_SUPPLIER` table. In the context, `COMPONENT_SUPPLIER` is explicitly the many-to-many junction between components and approved suppliers.

To find suppliers for a specific component, follow this join path: `COMPONENT.component_id` → `COMPONENT_SUPPLIER.component_id`, then `COMPONENT_SUPPLIER.supplier_id` → `SUPPLIER.supplier_id`.

At the schema level, the relevant tables and colu…

**Sources retrieved (12):** `Component Supplier→COMPONENT_SUPPLIER`, `Component Supplier`, `parent_chunk_data_dictionary.md_5`, `parent_chunk_data_dictionary.md_4`, `parent_chunk_data_dictionary.md_3`, `parent_chunk_data_dictionary.md_8`, `parent_chunk_business_glossary.md_0`, `parent_chunk_business_glossary.md_1`

**Context previews (first 3):**

1. _Business concept 'Component Supplier' — The table is explicitly described as a many-to-many relationship linking components to approved suppliers, and its foreign keys plus unique constraint confirm i…_

2. _Component Supplier: The table is explicitly described as a many-to-many relationship linking components to approved suppliers, and its foreign keys plus unique constraint confirm it is the junction en…_

3. _## warehouse  Stores physical storage location information for inventory management.  | Column | Data Type | Constraints | Description | |--------|-----------|-------------|-------------| | warehouse_…_

---

### ✅ QA-012 — How do I trace which components are needed to fulfill a work order?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.2334 | **Gate:** `proceed`

**Expected answer:**
> Start with the work_order table to get the product_id being manufactured. Join to the bom table using product_id as parent_product_id to find all direct components and sub-assemblies. For each component_product_id, if it is an ASSEMBLY type product, recursively query the bom table again to explode m…

**System answer:**
> To trace which components are needed for a work order, start with the `WORK_ORDER` table and follow the product structure.

A work order identifies the item to manufacture through `WORK_ORDER.product_id`, and it may also be decomposed into child work orders through `WORK_ORDER.parent_work_order` referencing `WORK_ORDER.work_order_id`. So if the production job is hierarchical, you should first trac…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_5`, `Work Order→WORK_ORDER`, `parent_chunk_data_dictionary.md_6`, `Batches for traceability and inventory management→INVENTORY`, `parent_chunk_data_dictionary.md_3`, `parent_chunk_data_dictionary.md_8`, `a parent product, a component product (which can be either a component or sub-assembly), the required quantity, unit of measure, and hierarchical level in the product structure→COMPONENT`, `parent_chunk_data_dictionary.md_7`

**Context previews (first 3):**

1. _## warehouse  Stores physical storage location information for inventory management.  | Column | Data Type | Constraints | Description | |--------|-----------|-------------|-------------| | warehouse_…_

2. _Business concept 'Work Order' — The table is explicitly described as production jobs and contains core work order attributes such as product, ordered/completed quantities, status, priority, planned da…_

3. _## work_order  Represents production jobs for manufacturing products with hierarchical work order support.  | Column | Data Type | Constraints | Description | |--------|-----------|-------------|-----…_

---

### ✅ QA-013 — How can I identify which warehouses have available inventory for specific components?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.8215 | **Gate:** `proceed`

**Expected answer:**
> Query the inventory table filtered by component_id, joining with the warehouse table to get warehouse names and locations. Calculate available quantity as quantity_on_hand minus quantity_reserved. Filter for records where available quantity is greater than zero. Results show warehouse names, locatio…

**System answer:**
> The knowledge graph provides the schema path, not actual inventory records. To identify warehouses tied to inventory records for specific components, use the `inventory` table and join it to `warehouse` through `inventory.warehouse_id = warehouse.warehouse_id`.

For the component side, use `inventory.component_id`, which is a foreign key to `component(component_id)`. The `inventory` table is defin…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_5`, `INVENTORY→WAREHOUSE`, `Batches for traceability and inventory management→INVENTORY`, `INVENTORY→COMPONENT`, `parent_chunk_data_dictionary.md_3`, `parent_chunk_data_dictionary.md_8`, `parent_chunk_data_dictionary.md_6`, `Batches for traceability and inventory management→BATCH`

**Context previews (first 3):**

1. _## warehouse  Stores physical storage location information for inventory management.  | Column | Data Type | Constraints | Description | |--------|-----------|-------------|-------------| | warehouse_…_

2. _Relationship: INVENTORY references WAREHOUSE via foreign key WAREHOUSE_ID -> WAREHOUSE.WAREHOUSE_ID.…_

3. _Business concept 'Batches for traceability and inventory management' is implemented by physical table INVENTORY (columns: inventory_id, warehouse_id, component_id, product_id, quantity_on_hand, quanti…_

---

### ✅ QA-014 — How do I find which shipments delivered materials from a specific supplier?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.3752 | **Gate:** `proceed`

**Expected answer:**
> Query the shipment table filtering by supplier_id and shipment_type = 'INBOUND'. Join with the warehouse table to show destination warehouses. Filter for status = 'DELIVERED' and include actual_arrival date. Results can be ordered by ship_date descending to show most recent deliveries first.

**System answer:**
> Use the `SHIPMENT` table. It tracks material transfers, and its supplier link is `supplier_id`.

To find shipments that delivered materials from a specific supplier, filter `SHIPMENT` on:

- `supplier_id` = the supplier you want
- `shipment_type = 'INBOUND'`, because the constraint `chk_supplier_inbound` says `supplier_id` is only set for inbound shipments
- `status = 'DELIVERED'`, since delivered…

**Sources retrieved (12):** `Shipment`, `parent_chunk_data_dictionary.md_8`, `Shipment→SHIPMENT`, `SHIPMENT→SUPPLIER`, `parent_chunk_data_dictionary.md_5`, `parent_chunk_data_dictionary.md_7`, `parent_chunk_data_dictionary.md_3`, `parent_chunk_data_dictionary.md_4`

**Context previews (first 3):**

1. _Shipment: The table is explicitly labeled as SHIPMENT and contains shipment-specific fields such as shipment_type, ship_date, estimated_arrival, actual_arrival, and status. Its foreign keys to warehou…_

2. _## shipment  Tracks material transfers between warehouses, suppliers, and customers.  | Column | Data Type | Constraints | Description | |--------|-----------|-------------|-------------| | shipment_i…_

3. _Business concept 'Shipment' — The table is explicitly labeled as SHIPMENT and contains shipment-specific fields such as shipment_type, ship_date, estimated_arrival, actual_arrival, and status. Its for…_

---

### ✅ QA-015 — How can I determine which quality control inspections were performed on a specific production batch?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.9779 | **Gate:** `proceed`

**Expected answer:**
> Query the quality_control table filtered by batch_id. Join with the specification table to get requirement details (specification_name, spec_type, acceptable ranges). Include qc_date, qc_type (INCOMING, IN_PROCESS, FINAL), result (PASS, FAIL, CONDITIONAL), and defect_count. This shows the complete i…

**System answer:**
> To determine which quality control inspections were performed on a specific production batch, use the QUALITY_CONTROL table and filter it by the batch identifier.

The key relationship is QUALITY_CONTROL.batch_id → BATCH.batch_id. The QUALITY_CONTROL table stores the inspection records for quality assurance and includes these relevant columns: qc_id, batch_id, specification_id, qc_date, qc_type, i…

**Sources retrieved (12):** `inspection and testing records for quality assurance→QUALITY_CONTROL`, `parent_chunk_data_dictionary.md_7`, `Batches for traceability and inventory management→BATCH`, `BATCH→PRODUCT`, `parent_chunk_data_dictionary.md_5`, `parent_chunk_data_dictionary.md_6`, `parent_chunk_data_dictionary.md_3`, `BATCH→WAREHOUSE`

**Context previews (first 3):**

1. _Business concept 'inspection and testing records for quality assurance' is implemented by physical table QUALITY_CONTROL (columns: qc_id, batch_id, specification_id, qc_date, qc_type, inspector_id, re…_

2. _## specification  Defines technical requirements and acceptance criteria for materials and products.  | Column | Data Type | Constraints | Description | |--------|-----------|-------------|-----------…_

3. _Business concept 'Batches for traceability and inventory management' is implemented by physical table BATCH (columns: batch_id, product_id, production_date, quantity_produced, warehouse_id, expiry_dat…_

---

### ✅ QA-016 — How do I track which work orders are in progress at a specific warehouse?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.7311 | **Gate:** `proceed`

**Expected answer:**
> Query the work_order table filtering by warehouse_id and status = 'IN_PROGRESS'. Join with the product table to get product names and types. Include quantity_ordered, quantity_completed, priority, planned_end_date, and calculate progress percentage as (quantity_completed / quantity_ordered * 100). O…

**System answer:**
> Use the `WORK_ORDER` table, because it represents production jobs and includes both `status` and `warehouse_id`. A work order is “in progress” when `WORK_ORDER.status = 'IN_PROGRESS'`. To limit the results to a specific warehouse, filter on `WORK_ORDER.warehouse_id`.

The direct relationship is `WORK_ORDER.warehouse_id -> WAREHOUSE.warehouse_id`, so the basic tracking path is `WORK_ORDER` to `WARE…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_5`, `parent_chunk_data_dictionary.md_6`, `WORK_ORDER→WAREHOUSE`, `Work Order→WORK_ORDER`, `parent_chunk_data_dictionary.md_8`, `parent_chunk_data_dictionary.md_7`, `Batches for traceability and inventory management→INVENTORY`, `Batches for traceability and inventory management→BATCH`

**Context previews (first 3):**

1. _## warehouse  Stores physical storage location information for inventory management.  | Column | Data Type | Constraints | Description | |--------|-----------|-------------|-------------| | warehouse_…_

2. _## work_order  Represents production jobs for manufacturing products with hierarchical work order support.  | Column | Data Type | Constraints | Description | |--------|-----------|-------------|-----…_

3. _Relationship: WORK_ORDER references WAREHOUSE via foreign key WAREHOUSE_ID -> WAREHOUSE.WAREHOUSE_ID.…_

---

### ✅ QA-017 — How can I find which components need reordering based on current inventory levels?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.3023 | **Gate:** `proceed`

**Expected answer:**
> Query the inventory table and filter where quantity_on_hand minus quantity_reserved is less than reorder_threshold. Join with the component table to get component names, categories, and standard costs. Join with the warehouse table for location information. Results identify which components are belo…

**System answer:**
> Use the INVENTORY table, because it is the table that “tracks stock levels for components and products at specific warehouse locations” and includes the fields used for replenishment: inventory_id, warehouse_id, component_id, product_id, quantity_on_hand, quantity_reserved, reorder_threshold, and last_restock_date.

At the schema level, the procedure is:

Filter INVENTORY to component stock only b…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_5`, `Batches for traceability and inventory management→INVENTORY`, `INVENTORY→COMPONENT`, `parent_chunk_data_dictionary.md_3`, `parent_chunk_data_dictionary.md_7`, `parent_chunk_data_dictionary.md_4`, `a parent product, a component product (which can be either a component or sub-assembly), the required quantity, unit of measure, and hierarchical level in the product structure→COMPONENT`, `Component Supplier→COMPONENT_SUPPLIER`

**Context previews (first 3):**

1. _## warehouse  Stores physical storage location information for inventory management.  | Column | Data Type | Constraints | Description | |--------|-----------|-------------|-------------| | warehouse_…_

2. _Business concept 'Batches for traceability and inventory management' is implemented by physical table INVENTORY (columns: inventory_id, warehouse_id, component_id, product_id, quantity_on_hand, quanti…_

3. _Relationship: INVENTORY references COMPONENT via foreign key COMPONENT_ID -> COMPONENT.COMPONENT_ID.…_

---

### ✅ QA-018 — How do I determine the manufacturing route for a specific product?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0413 | **Gate:** `proceed_with_warning`

**Expected answer:**
> Query the route table filtering by product_id, ordered by sequence_number ascending. For each operation, retrieve operation_name, work_center, cycle_time_minutes, and setup_time_minutes. Join with the product table to get product details. The sequence of operations shows the complete manufacturing w…

**System answer:**
> Based on the schema, determine a product’s manufacturing route by linking `PRODUCT` to `ROUTE` through the foreign key `ROUTE.product_id -> PRODUCT.product_id`.

Use the product’s identifier from `PRODUCT.product_id` to find all matching rows in `ROUTE`. The relevant join path is `PRODUCT.product_id = ROUTE.product_id`. If you start from a product name, first locate the product in `PRODUCT` using …

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_6`, `ROUTE→PRODUCT`, `parent_chunk_data_dictionary.md_3`, `parent_chunk_data_dictionary.md_7`, `Work Order→WORK_ORDER`, `uq_route_sequence→ROUTE`, `a unique identifier, name, type classification, base cost, and lead time for procurement or production→PRODUCT`, `parent_chunk_data_dictionary.md_8`

**Context previews (first 3):**

1. _## work_order  Represents production jobs for manufacturing products with hierarchical work order support.  | Column | Data Type | Constraints | Description | |--------|-----------|-------------|-----…_

2. _Relationship: ROUTE references PRODUCT via foreign key PRODUCT_ID -> PRODUCT.PRODUCT_ID.…_

3. _# Manufacturing Data Dictionary  This data dictionary documents the database schema for the manufacturing supply chain system. It includes all tables, columns, data types, constraints, and relationshi…_

---

### ✅ QA-019 — How can I find which batches are stored at a specific warehouse and their QC status?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.7533 | **Gate:** `proceed`

**Expected answer:**
> Query the batch table filtering by warehouse_id. Join with the product table to get product names and types. Include production_date, quantity_produced, expiry_date, and qc_status (PENDING, PASSED, FAILED, QUARANTINED). Filter by qc_status to isolate batches requiring quality attention or ready for …

**System answer:**
> Use the BATCH table. The business concept “Batches for traceability and inventory management” is implemented by BATCH, and it includes both the storage location and the QC status: `batch_id`, `product_id`, `production_date`, `quantity_produced`, `warehouse_id`, `expiry_date`, and `qc_status`.

To find batches stored at a specific warehouse, filter `BATCH.warehouse_id` for that warehouse. The schem…

**Sources retrieved (12):** `Batches for traceability and inventory management→BATCH`, `parent_chunk_data_dictionary.md_5`, `BATCH→WAREHOUSE`, `inspection and testing records for quality assurance→QUALITY_CONTROL`, `parent_chunk_data_dictionary.md_6`, `Batches for traceability and inventory management→INVENTORY`, `parent_chunk_data_dictionary.md_8`, `Work Order→WORK_ORDER`

**Context previews (first 3):**

1. _Business concept 'Batches for traceability and inventory management' is implemented by physical table BATCH (columns: batch_id, product_id, production_date, quantity_produced, warehouse_id, expiry_dat…_

2. _## warehouse  Stores physical storage location information for inventory management.  | Column | Data Type | Constraints | Description | |--------|-----------|-------------|-------------| | warehouse_…_

3. _Relationship: BATCH references WAREHOUSE via foreign key WAREHOUSE_ID -> WAREHOUSE.WAREHOUSE_ID.…_

---

### ✅ QA-020 — How do I identify which specifications apply to specific components?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.2550 | **Gate:** `proceed`

**Expected answer:**
> Query the component table and join with the specification table via specification_id. Include component_name, component_category, and specification details (specification_name, spec_type, critical_parameter, min_value, max_value, unit_of_measure). This shows the technical requirements that each comp…

**System answer:**
> To identify which specification applies to a specific component, use the direct relationship from COMPONENT to SPECIFICATION.

The schema shows that COMPONENT has these relevant columns: component_id, component_name, component_category, unit_of_measure, standard_cost, and specification_id. SPECIFICATION has specification_id as its primary key, along with specification_name, version, effective_date…

**Sources retrieved (12):** `a parent product, a component product (which can be either a component or sub-assembly), the required quantity, unit of measure, and hierarchical level in the product structure→COMPONENT`, `parent_chunk_data_dictionary.md_5`, `parent_chunk_data_dictionary.md_7`, `parent_chunk_data_dictionary.md_3`, `version numbers, effective dates, specification types (dimensional, material, performance), critical parameters to test, and acceptable value ranges with units of measure→SPECIFICATION`, `parent_chunk_data_dictionary.md_4`, `Component Supplier→COMPONENT_SUPPLIER`, `parent_chunk_business_glossary.md_0`

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
> To perform a complete BOM explosion for a finished product, use the `bom` table as the recursive structure and the `product` table to identify the starting item and classify each exploded row.

Start with the finished product in `product`, using its `product_id` and `product_type = FINISHED_GOOD`. The first-level explosion is all rows in `bom` where `bom.parent_product_id = product.product_id`. Ea…

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
> From the retrieved context, the supported part is the product-structure traversal, not an official costing formula.

To include all sub-assemblies, start from the target product in `product` and recursively traverse the `bom` table using `bom.parent_product_id -> bom.component_product_id`, where both columns reference `product(product_id)`. This is the schema path for a BOM explosion:

`product.pr…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_3`, `a parent product, a component product (which can be either a component or sub-assembly), the required quantity, unit of measure, and hierarchical level in the product structure→COMPONENT`, `parent_chunk_data_dictionary.md_4`, `parent_chunk_data_dictionary.md_7`, `parent_chunk_data_dictionary.md_8`, `The Bill of Materials (BOM)→BOM`, `parent_chunk_data_dictionary.md_6`, `parent_chunk_data_dictionary.md_5`

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
> Use the `bom` table recursively.

The BOM is implemented by `bom(bom_id, parent_product_id, component_product_id, quantity, unit_of_measure, bom_level, is_optional)`, and both `parent_product_id` and `component_product_id` are foreign keys to `product(product_id)`. Because the BOM supports recursive multi-level assemblies, the way to find every parent product that contains a given component anywhe…

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
> Use the `work_order` table as the starting point and traverse the product structure through `bom`.

At the schema level, the core path is `work_order.product_id` → `bom.parent_product_id`. The `work_order` row tells you which `product` is being built, and the `bom` table defines which `component_product_id` values are required for that parent product. To handle nested sub-assemblies, you must recu…

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
> Use the `bom` table. The schema explicitly says `bom_level` is the “depth in product hierarchy” and that it “tracks depth for performance optimization,” so the maximum BOM depth is determined from `BOM.bom_level`.

If you want the maximum depth across the whole system, take the highest value in `BOM.bom_level`.

If you want the maximum depth for a specific product, trace that product’s BOM structu…

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
> Use the `bom` table as the primary path, because it is the Bill of Materials and is explicitly designed for recursive, multi-level product composition.

Start with the specific product in `bom.component_product_id`. Then recursively walk upward through `bom.parent_product_id` to find every parent product that includes it directly or indirectly. To return product details, join each discovered `pare…

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
> Use the `PRODUCT` and `BOM` tables together.

`PRODUCT.lead_time_days` stores the lead time for each manufactured item, and `BOM` defines the multi-level assembly structure through `BOM.parent_product_id` and `BOM.component_product_id`, both of which reference `PRODUCT.product_id`. Because `BOM` is explicitly described as supporting recursive relationships for multi-level assemblies, it is the mai…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_3`, `a unique identifier, name, type classification, base cost, and lead time for procurement or production→PRODUCT`, `Component Supplier→COMPONENT_SUPPLIER`, `a parent product, a component product (which can be either a component or sub-assembly), the required quantity, unit of measure, and hierarchical level in the product structure→COMPONENT`, `Component Supplier`, `parent_chunk_data_dictionary.md_4`, `parent_chunk_data_dictionary.md_7`, `parent_chunk_data_dictionary.md_6`

**Context previews (first 3):**

1. _# Manufacturing Data Dictionary  This data dictionary documents the database schema for the manufacturing supply chain system. It includes all tables, columns, data types, constraints, and relationshi…_

2. _Business concept 'a unique identifier, name, type classification, base cost, and lead time for procurement or production' is implemented by physical table PRODUCT (columns: product_id, product_name, p…_

3. _Business concept 'Component Supplier' — The table is explicitly described as a many-to-many relationship linking components to approved suppliers, and its foreign keys plus unique constraint confirm i…_

---

### ✅ QA-028 — How do I generate a complete indented BOM report showing the hierarchical structure?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.4180 | **Gate:** `proceed`

**Expected answer:**
> Use a recursive query on the bom table that tracks the current depth level. Start with the top-level product (parent_product_id where product has no parent_product_id). At each level, output component details indented by depth level. Include product_name, quantity, and unit_of_measure. Recursively p…

**System answer:**
> Use the `bom` table as the primary source for the report, because the context explicitly says the Bill of Materials is implemented by physical table `BOM` with columns `bom_id`, `parent_product_id`, `component_product_id`, `quantity`, `unit_of_measure`, `bom_level`, and `is_optional`. It also says `bom` “defines product composition and hierarchical structure” and “supports recursive relationships …

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_4`, `parent_chunk_data_dictionary.md_3`, `a parent product, a component product (which can be either a component or sub-assembly), the required quantity, unit of measure, and hierarchical level in the product structure→COMPONENT`, `parent_chunk_data_dictionary.md_6`, `parent_chunk_data_dictionary.md_8`, `The Bill of Materials (BOM)→BOM`, `BOM→PRODUCT`, `parent_chunk_business_glossary.md_0`

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
> Use the `bom` table as the primary source, because The Bill of Materials is implemented by physical table `BOM` with columns `bom_id`, `parent_product_id`, `component_product_id`, `quantity`, `unit_of_measure`, `bom_level`, and `is_optional`.

To find which components appear most frequently across all product BOMs, count occurrences of `bom.component_product_id` across all `bom` rows. Then join `b…

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
> The retrieved context does not describe a concrete method for detecting circular references in the BOM, so I cannot state a supported algorithm for preventing infinite loops.

What the context does establish is that the `bom` table represents a recursive product structure: `parent_product_id` and `component_product_id` both reference `product(product_id)`, and the table is explicitly described as …

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_4`, `parent_chunk_data_dictionary.md_3`, `BOM→PRODUCT`, `The Bill of Materials (BOM)→BOM`, `parent_chunk_data_dictionary.md_8`, `parent_chunk_data_dictionary.md_7`, `parent_chunk_data_dictionary.md_6`, `parent_chunk_business_glossary.md_0`

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
> From the retrieved context, you can determine this at the schema level in two parts:

First, explode the finished product’s structure recursively. The product structure is modeled in two related ways:

The `product` table stores every manufactured item, including `FINISHED_GOOD`, `ASSEMBLY`, and `COMPONENT`, and supports hierarchy through `parent_product_id -> product(product_id)`.

The `bom` tabl…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_3`, `a parent product, a component product (which can be either a component or sub-assembly), the required quantity, unit of measure, and hierarchical level in the product structure→COMPONENT`, `parent_chunk_data_dictionary.md_4`, `parent_chunk_data_dictionary.md_8`, `Component Supplier→COMPONENT_SUPPLIER`, `parent_chunk_data_dictionary.md_6`, `parent_chunk_data_dictionary.md_7`, `Shipment→SHIPMENT`

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
> Use the `work_order` and `inventory` tables.

At the schema level, the check is:

Join `work_order.product_id` to `inventory.product_id`, because a work order identifies the product to manufacture and inventory can store product stock by warehouse. Then, if you want warehouse-level visibility, join `inventory.warehouse_id` to `warehouse.warehouse_id`.

To determine whether enough stock exists acro…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_5`, `parent_chunk_data_dictionary.md_6`, `INVENTORY→WAREHOUSE`, `Work Order→WORK_ORDER`, `WORK_ORDER→WAREHOUSE`, `Batches for traceability and inventory management→INVENTORY`, `parent_chunk_data_dictionary.md_8`, `parent_chunk_data_dictionary.md_7`

**Context previews (first 3):**

1. _## warehouse  Stores physical storage location information for inventory management.  | Column | Data Type | Constraints | Description | |--------|-----------|-------------|-------------| | warehouse_…_

2. _## work_order  Represents production jobs for manufacturing products with hierarchical work order support.  | Column | Data Type | Constraints | Description | |--------|-----------|-------------|-----…_

3. _Relationship: INVENTORY references WAREHOUSE via foreign key WAREHOUSE_ID -> WAREHOUSE.WAREHOUSE_ID.…_

---

### ✅ QA-033 — How can I find which quality control inspections failed for components from specific suppliers?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.4561 | **Gate:** `proceed`

**Expected answer:**
> Query the quality_control table filtering by result = 'FAIL'. Join with the batch table to get product_id and production_date. Join with the bom table recursively to trace which products contain failed components. Join with component_supplier and supplier tables to identify the source supplier. Filt…

**System answer:**
> From the retrieved context, you can answer this only partially at the schema level.

To find failed quality inspections for component items, the supported join path is `QUALITY_CONTROL.batch_id -> batch.batch_id -> batch.product_id -> product.product_id`. `QUALITY_CONTROL` stores the inspection record with columns `qc_id`, `batch_id`, `specification_id`, `qc_date`, `qc_type`, `inspector_id`, `resu…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_5`, `parent_chunk_data_dictionary.md_3`, `inspection and testing records for quality assurance→QUALITY_CONTROL`, `Component Supplier→COMPONENT_SUPPLIER`, `Component Supplier`, `parent_chunk_data_dictionary.md_4`, `COMPONENT_SUPPLIER→SUPPLIER`, `parent_chunk_data_dictionary.md_8`

**Context previews (first 3):**

1. _## warehouse  Stores physical storage location information for inventory management.  | Column | Data Type | Constraints | Description | |--------|-----------|-------------|-------------| | warehouse_…_

2. _# Manufacturing Data Dictionary  This data dictionary documents the database schema for the manufacturing supply chain system. It includes all tables, columns, data types, constraints, and relationshi…_

3. _Business concept 'inspection and testing records for quality assurance' is implemented by physical table QUALITY_CONTROL (columns: qc_id, batch_id, specification_id, qc_date, qc_type, inspector_id, re…_

---

### ✅ QA-034 — How do I calculate the total manufacturing time for a work order including all sub-assembly work orders?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.1599 | **Gate:** `proceed_with_warning`

**Expected answer:**
> Query the work_order table starting with the parent work_order. Find all child work_orders where parent_work_order matches the current work_order_id. For each work order (parent and children), join with the route table on product_id to get all operations. Sum (cycle_time_minutes * quantity) plus set…

**System answer:**
> From the retrieved context, the schema supports this at the work-order hierarchy level, but it does not define a single official formula for “total manufacturing time.”

What the context does provide is the structure you would use:

Start with `WORK_ORDER.work_order_id` for the top-level work order, then recursively collect all descendant work orders using the self-referential relationship `WORK_O…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_6`, `Work Order→WORK_ORDER`, `parent_chunk_data_dictionary.md_3`, `a parent product, a component product (which can be either a component or sub-assembly), the required quantity, unit of measure, and hierarchical level in the product structure→COMPONENT`, `parent_chunk_data_dictionary.md_7`, `parent_chunk_data_dictionary.md_5`, `parent_chunk_data_dictionary.md_4`, `parent_chunk_business_glossary.md_0`

**Context previews (first 3):**

1. _## work_order  Represents production jobs for manufacturing products with hierarchical work order support.  | Column | Data Type | Constraints | Description | |--------|-----------|-------------|-----…_

2. _Business concept 'Work Order' — The table is explicitly described as production jobs and contains core work order attributes such as product, ordered/completed quantities, status, priority, planned da…_

3. _# Manufacturing Data Dictionary  This data dictionary documents the database schema for the manufacturing supply chain system. It includes all tables, columns, data types, constraints, and relationshi…_

---

### ✅ QA-035 — How can I identify which shipments are overdue and their impact on work orders?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0719 | **Gate:** `proceed_with_warning`

**Expected answer:**
> Query the shipment table filtering for status = 'SHIPPED' where actual_arrival is NULL and estimated_arrival is in the past (overdue). Join with the component_supplier table via supplier_id and component_id to identify which components are delayed. Perform reverse BOM lookup to find which parent pro…

**System answer:**
> From the retrieved context alone, I cannot determine which shipments are “overdue,” because no overdue business rule is defined. The `SHIPMENT` table includes `ship_date`, `estimated_arrival`, `actual_arrival`, and `status` (`PENDING`, `SHIPPED`, `DELIVERED`, `CANCELLED`), and it has a constraint that `actual_arrival >= ship_date`, but the context does not state any rule such as “estimated_arrival…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_5`, `parent_chunk_data_dictionary.md_8`, `parent_chunk_data_dictionary.md_6`, `Work Order→WORK_ORDER`, `Shipment`, `Shipment→SHIPMENT`, `WORK_ORDER→PRODUCT`, `WORK_ORDER→WAREHOUSE`

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
> Start with BATCH, because it is the table that holds the expiry information for each production lot: `batch_id`, `product_id`, `production_date`, `quantity_produced`, `warehouse_id`, `expiry_date`, and `qc_status`.

To find batches that are past expiry, filter `BATCH.expiry_date` to be earlier than your reference date. To find batches approaching expiry, use a cutoff window based on `expiry_date`;…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_5`, `Batches for traceability and inventory management→BATCH`, `parent_chunk_data_dictionary.md_7`, `Batches for traceability and inventory management→INVENTORY`, `parent_chunk_data_dictionary.md_3`, `Component Supplier→COMPONENT_SUPPLIER`, `Component Supplier`, `parent_chunk_data_dictionary.md_8`

**Context previews (first 3):**

1. _## warehouse  Stores physical storage location information for inventory management.  | Column | Data Type | Constraints | Description | |--------|-----------|-------------|-------------| | warehouse_…_

2. _Business concept 'Batches for traceability and inventory management' is implemented by physical table BATCH (columns: batch_id, product_id, production_date, quantity_produced, warehouse_id, expiry_dat…_

3. _## specification  Defines technical requirements and acceptance criteria for materials and products.  | Column | Data Type | Constraints | Description | |--------|-----------|-------------|-----------…_

---

### ✅ QA-037 — How can I generate a material requirements plan showing when to order components based on work order schedules?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0433 | **Gate:** `proceed_with_warning`

**Expected answer:**
> Query all work_orders with status 'PENDING' ordered by planned_start_date. For each work_order, perform BOM explosion to get required components and quantities. For each component, query inventory for current available stock across warehouses. Calculate net requirements = (required quantity * work_o…

**System answer:**
> You can generate this at the schema level by using `WORK_ORDER` as the schedule driver and `BOM` as the material explosion structure.

Join `WORK_ORDER.product_id` to `BOM.parent_product_id` to find the components required for each production job. The core work order fields for planning are `work_order_id`, `product_id`, `quantity_ordered`, `quantity_completed`, `planned_start_date`, `planned_end_…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_6`, `parent_chunk_data_dictionary.md_7`, `parent_chunk_data_dictionary.md_5`, `Work Order→WORK_ORDER`, `parent_chunk_data_dictionary.md_4`, `parent_chunk_data_dictionary.md_3`, `Component Supplier→COMPONENT_SUPPLIER`, `The Bill of Materials (BOM)→BOM`

**Context previews (first 3):**

1. _## work_order  Represents production jobs for manufacturing products with hierarchical work order support.  | Column | Data Type | Constraints | Description | |--------|-----------|-------------|-----…_

2. _## specification  Defines technical requirements and acceptance criteria for materials and products.  | Column | Data Type | Constraints | Description | |--------|-----------|-------------|-----------…_

3. _## warehouse  Stores physical storage location information for inventory management.  | Column | Data Type | Constraints | Description | |--------|-----------|-------------|-------------| | warehouse_…_

---

### ✅ QA-038 — How do I trace the complete genealogy of a component from supplier through batch to finished goods?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0748 | **Gate:** `proceed_with_warning`

**Expected answer:**
> Start with a shipment from the supplier (shipment table with supplier_id and shipment_type = 'INBOUND'). Track to inventory updates via component_id and warehouse_id. Identify batches that consumed the component via reverse BOM lookup (batch.product_id → bom hierarchy → component_id). Query quality_…

**System answer:**
> From the retrieved context, you cannot trace a fully verified end-to-end genealogy of a component from supplier through a specific production batch to a specific finished-good batch. The schema shown supports only a partial, warehouse- and structure-level trace.

The supplier side starts in COMPONENT_SUPPLIER. Use COMPONENT_SUPPLIER.component_id to find approved suppliers via COMPONENT_SUPPLIER.su…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_3`, `parent_chunk_data_dictionary.md_7`, `parent_chunk_data_dictionary.md_5`, `parent_chunk_data_dictionary.md_8`, `Batches for traceability and inventory management→INVENTORY`, `parent_chunk_data_dictionary.md_4`, `Component Supplier→COMPONENT_SUPPLIER`, `Component Supplier`

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
> From the retrieved context, you can answer this at the schema level in two parts.

First, identify components that are critical to multiple products from the `bom` and `product` structures. The `bom` table defines which `component_product_id` goes into which `parent_product_id`, and both columns reference `product(product_id)`. Because `bom` supports multi-level assemblies, a component can appear …

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_4`, `Component Supplier→COMPONENT_SUPPLIER`, `Component Supplier`, `parent_chunk_data_dictionary.md_3`, `Preferred supplier for this component→SUPPLIER`, `parent_chunk_data_dictionary.md_5`, `parent_chunk_data_dictionary.md_8`, `parent_chunk_data_dictionary.md_7`

**Context previews (first 3):**

1. _## bom  Bill of Materials defining product composition and hierarchical structure. Supports recursive relationships for multi-level assemblies.  | Column | Data Type | Constraints | Description | |---…_

2. _Business concept 'Component Supplier' — The table is explicitly described as a many-to-many relationship linking components to approved suppliers, and its foreign keys plus unique constraint confirm i…_

3. _Component Supplier: The table is explicitly described as a many-to-many relationship linking components to approved suppliers, and its foreign keys plus unique constraint confirm it is the junction en…_

---

### ✅ QA-040 — How do I calculate the total landed cost for a product including component costs, supplier lead times, and manufacturing operations?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.1922 | **Gate:** `proceed_with_warning`

**Expected answer:**
> Perform recursive BOM explosion to get all leaf components. For each component, query component_supplier to get unit_price from primary supplier. Multiply by accumulated BOM quantity for material cost. Add shipping costs (estimated from shipment history). Query route table for the product to get all…

**System answer:**
> The retrieved context supports only a partial, schema-level answer.

For a target product, the available starting point is PRODUCT. PRODUCT contains product_id, product_name, product_type, parent_product_id, base_cost, lead_time_days, and is_active. If the product is an assembly, the schema supports hierarchical roll-up through the self-reference PRODUCT.parent_product_id → PRODUCT.product_id, and…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_3`, `Component Supplier→COMPONENT_SUPPLIER`, `a unique identifier, name, type classification, base cost, and lead time for procurement or production→PRODUCT`, `Component Supplier`, `a parent product, a component product (which can be either a component or sub-assembly), the required quantity, unit of measure, and hierarchical level in the product structure→COMPONENT`, `parent_chunk_data_dictionary.md_6`, `parent_chunk_data_dictionary.md_7`, `parent_chunk_data_dictionary.md_5`

**Context previews (first 3):**

1. _# Manufacturing Data Dictionary  This data dictionary documents the database schema for the manufacturing supply chain system. It includes all tables, columns, data types, constraints, and relationshi…_

2. _Business concept 'Component Supplier' — The table is explicitly described as a many-to-many relationship linking components to approved suppliers, and its foreign keys plus unique constraint confirm i…_

3. _Business concept 'a unique identifier, name, type classification, base cost, and lead time for procurement or production' is implemented by physical table PRODUCT (columns: product_id, product_name, p…_

---

## Anomalies & Observations

No anomalies detected. All questions grounded with acceptable RAGAS scores.
