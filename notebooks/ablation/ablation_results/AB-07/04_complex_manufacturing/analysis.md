# AB-07 — 04_complex_manufacturing — Run Analysis

**Timestamp:** 2026-03-31 17:53:44  
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
| Chunk size / overlap | `384 / 48` |
| ER similarity threshold | `0.75` |

## Builder Results

| Metric | Value |
|--------|-------|
| Triplets extracted | 371 |
| Entities resolved | 131 |
| Tables parsed | 13 |
| Tables completed | 13 |

## Query Evaluation Summary

| Metric | Value |
|--------|-------|
| Questions | 40 |
| Grounded | **40/40 (100%)** |
| Avg GT Coverage | 100% |
| Avg Top Score | 0.4237 |
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
> The manufacturing system stores product information in the `product` table. A product represents any manufactured item, including finished goods, assemblies, and components.

For each product, the system stores a unique `product_id` (`VARCHAR(20)`, primary key), `product_name` (`VARCHAR(100)`, not null), `product_type` (`product_type_t`, not null, default `FINISHED_GOOD`), `parent_product_id` (`VA…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_3`, `Actual stock levels of components and products stored in specific warehouses→WAREHOUSE`, `Warehouse Stock Levels→INVENTORY`, `parent_chunk_data_dictionary.md_6`, `parent_chunk_data_dictionary.md_5`, `parent_chunk_data_dictionary.md_7`, `parent_chunk_business_glossary.md_0`, `parent_chunk_business_glossary.md_1`

**Context previews (first 3):**

1. _# Manufacturing Data Dictionary  This data dictionary documents the database schema for the manufacturing supply chain system. It includes all tables, columns, data types, constraints, and relationshi…_

2. _Business concept 'Actual stock levels of components and products stored in specific warehouses' is implemented by physical table WAREHOUSE (columns: warehouse_id, warehouse_name, address, city, state,…_

3. _Business concept 'Warehouse Stock Levels' — The table records stock quantities on hand and reserved, reorder threshold, and last restock date, all tied to a warehouse and either a component or product…_

---

### ✅ QA-002 — How are components defined in the manufacturing database?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.5910 | **Gate:** `proceed`

**Expected answer:**
> Components are defined with a unique identifier (component_id), descriptive name (component_name), category grouping (component_category), unit of measure (unit_of_measure), standard unit cost (standard_cost), and optional reference to technical specifications (specification_id). Components represen…

**System answer:**
> Components are defined as atomic raw materials or purchased parts that cannot be further broken down into simpler manufactured items. In the business glossary, they are described as the building blocks used in manufacturing and as items procured from external suppliers.

In the schema, component information appears in two connected ways. First, the `product` table includes components as one of the…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_3`, `Bill of Materials Entry→BOM`, `parent_chunk_data_dictionary.md_4`, `components they can provide through approved supplier relationships→COMPONENT_SUPPLIER`, `parent_chunk_data_dictionary.md_5`, `parent_chunk_business_glossary.md_0`, `parent_chunk_business_glossary.md_1`, `parent_chunk_business_glossary.md_2`

**Context previews (first 3):**

1. _# Manufacturing Data Dictionary  This data dictionary documents the database schema for the manufacturing supply chain system. It includes all tables, columns, data types, constraints, and relationshi…_

2. _Business concept 'Bill of Materials Entry' — The table directly models parent_product_id to component_product_id relationships with quantity, unit_of_measure, bom_level, and is_optional, which matches…_

3. _## bom  Bill of Materials defining product composition and hierarchical structure. Supports recursive relationships for multi-level assemblies.  | Column | Data Type | Constraints | Description | |---…_

---

### ✅ QA-003 — What is the purpose of the Bill of Materials (BOM) table?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.9127 | **Gate:** `proceed`

**Expected answer:**
> The BOM table defines the hierarchical structure of products by specifying which components or sub-assemblies are required to manufacture each parent product. It records the unique BOM entry identifier (bom_id), parent product being built (parent_product_id), component or sub-assembly product (compo…

**System answer:**
> The Bill of Materials table, `bom`, defines product composition and hierarchical structure. It stores BOM entries that link a `parent_product_id` to a `component_product_id`, showing what component goes into what parent product, along with `quantity`, `unit_of_measure`, `bom_level`, and `is_optional`.

Its purpose is to support multi-level assemblies through recursive relationships: both `parent_p…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_4`, `Bill of Materials Entry→BOM`, `BOM→PRODUCT`, `parent_chunk_data_dictionary.md_3`, `parent_chunk_data_dictionary.md_7`, `parent_chunk_data_dictionary.md_8`, `Bill of Materials Entry`, `parent_chunk_business_glossary.md_0`

**Context previews (first 3):**

1. _## bom  Bill of Materials defining product composition and hierarchical structure. Supports recursive relationships for multi-level assemblies.  | Column | Data Type | Constraints | Description | |---…_

2. _Business concept 'Bill of Materials Entry' — The table directly models parent_product_id to component_product_id relationships with quantity, unit_of_measure, bom_level, and is_optional, which matches…_

3. _Relationship: BOM references PRODUCT via foreign key COMPONENT_PRODUCT_ID -> PRODUCT.PRODUCT_ID.…_

---

### ✅ QA-004 — What supplier information does the system maintain?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.3048 | **Gate:** `proceed`

**Expected answer:**
> Suppliers are tracked with a unique identifier (supplier_id), legal business name (supplier_name), primary contact email (contact_email), primary contact phone number (contact_phone), performance rating from 1.0 to 5.0 (rating), and preferred supplier status flag (is_preferred).

**System answer:**
> The system maintains supplier information at both the supplier-profile level and the supplier-relationship level.

The core supplier master data is the business concept “Supplier Profile,” implemented by the SUPPLIER table. From the context, this table stores supplier identity and contact details, along with procurement-oriented attributes. Its columns are supplier_id, supplier_name, contact_email…

**Sources retrieved (12):** `Supplier Profile→SUPPLIER`, `parent_chunk_data_dictionary.md_4`, `Material Transfer`, `SHIPMENT→SUPPLIER`, `components they can provide through approved supplier relationships→COMPONENT_SUPPLIER`, `Material Transfer→SHIPMENT`, `parent_chunk_data_dictionary.md_8`, `COMPONENT_SUPPLIER→SUPPLIER`

**Context previews (first 3):**

1. _Business concept 'Supplier Profile' — The table stores supplier identity plus contact details, performance rating, and preferred status, which aligns most closely with a supplier profile rather than a…_

2. _## bom  Bill of Materials defining product composition and hierarchical structure. Supports recursive relationships for multi-level assemblies.  | Column | Data Type | Constraints | Description | |---…_

3. _Material Transfer: The table is explicitly described as a shipment/material transfer record and its columns capture transfer type, source/destination references, ship and arrival dates, and status. Th…_

---

### ✅ QA-005 — How are warehouses represented in the schema?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.3381 | **Gate:** `proceed`

**Expected answer:**
> Warehouses are defined with a unique identifier (warehouse_id), descriptive name (warehouse_name), full street address (address), city location (city), state or province (state), total storage capacity in cubic meters (capacity), and optional manager identifier (manager_id).

**System answer:**
> Warehouses are represented by the `warehouse` table (`WAREHOUSE`), which models a physical storage location for inventory management. It stores one row per warehouse and includes these columns: `warehouse_id` as the primary key, `warehouse_name`, `address`, `city`, `state`, `capacity`, and `manager_id`.

From the business description, a warehouse is a physical location where materials, components,…

**Sources retrieved (12):** `INVENTORY→WAREHOUSE`, `BATCH→WAREHOUSE`, `WORK_ORDER→WAREHOUSE`, `SHIPMENT→WAREHOUSE`, `parent_chunk_data_dictionary.md_6`, `Actual stock levels of components and products stored in specific warehouses→WAREHOUSE`, `parent_chunk_data_dictionary.md_5`, `Material Transfer→SHIPMENT`

**Context previews (first 3):**

1. _Relationship: INVENTORY references WAREHOUSE via foreign key WAREHOUSE_ID -> WAREHOUSE.WAREHOUSE_ID.…_

2. _Relationship: BATCH references WAREHOUSE via foreign key WAREHOUSE_ID -> WAREHOUSE.WAREHOUSE_ID.…_

3. _Relationship: WORK_ORDER references WAREHOUSE via foreign key WAREHOUSE_ID -> WAREHOUSE.WAREHOUSE_ID.…_

---

### ✅ QA-006 — What does the inventory table track?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.7192 | **Gate:** `proceed`

**Expected answer:**
> The inventory table tracks real-time stock levels including a unique record identifier (inventory_id), warehouse location (warehouse_id), component identifier for materials (component_id) or product identifier for finished goods (product_id), current physical stock quantity (quantity_on_hand), quant…

**System answer:**
> The `INVENTORY` table tracks actual stock levels of components and products stored in specific warehouses. It records, for each inventory record, the warehouse, either a component or a product, the quantity on hand, quantity reserved, reorder threshold, and last restock date.

From the context, its columns are `inventory_id`, `warehouse_id`, `component_id`, `product_id`, `quantity_on_hand`, `quant…

**Sources retrieved (12):** `Warehouse Stock Levels→INVENTORY`, `INVENTORY→PRODUCT`, `INVENTORY→WAREHOUSE`, `Work Order`, `INVENTORY→COMPONENT`, `parent_chunk_data_dictionary.md_5`, `Work Order→WORK_ORDER`, `parent_chunk_data_dictionary.md_7`

**Context previews (first 3):**

1. _Business concept 'Warehouse Stock Levels' — The table records stock quantities on hand and reserved, reorder threshold, and last restock date, all tied to a warehouse and either a component or product…_

2. _Relationship: INVENTORY references PRODUCT via foreign key PRODUCT_ID -> PRODUCT.PRODUCT_ID.…_

3. _Relationship: INVENTORY references WAREHOUSE via foreign key WAREHOUSE_ID -> WAREHOUSE.WAREHOUSE_ID.…_

---

### ✅ QA-007 — How are work orders structured in the manufacturing system?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.4854 | **Gate:** `proceed`

**Expected answer:**
> Work orders represent production jobs with a unique identifier (work_order_id), product to be manufactured (product_id), optional parent work order for nested hierarchies (parent_work_order), quantity to produce (quantity_ordered), quantity completed so far (quantity_completed), current status (PEND…

**System answer:**
> Work orders in the manufacturing system are represented by the `WORK_ORDER` table and the business concept `Work Order`. A work order is a production job for manufacturing a product, identified by `work_order_id` as the primary key. Each work order must reference a product through `product_id -> PRODUCT.PRODUCT_ID`, so every work order is tied to the specific product being manufactured.

The struc…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_6`, `Work Order`, `Work Order→WORK_ORDER`, `WORK_ORDER→PRODUCT`, `WORK_ORDER→WORK_ORDER`, `parent_chunk_data_dictionary.md_3`, `WORK_ORDER→WAREHOUSE`, `parent_chunk_data_dictionary.md_5`

**Context previews (first 3):**

1. _## work_order  Represents production jobs for manufacturing products with hierarchical work order support.  | Column | Data Type | Constraints | Description | |--------|-----------|-------------|-----…_

2. _Work Order: The table name, primary key, and foreign keys align directly with the business entity describing work orders. Its columns track planned versus completed quantities, status, priority, and p…_

3. _Business concept 'Work Order' — The table name, primary key, and foreign keys align directly with the business entity describing work orders. Its columns track planned versus completed quantities, sta…_

---

### ✅ QA-008 — What information is captured in the shipment table?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.9732 | **Gate:** `proceed`

**Expected answer:**
> Shipments track material transfers with a unique identifier (shipment_id), shipment type (INBOUND from suppliers, OUTBOUND to customers, INTERNAL between warehouses), destination warehouse (warehouse_id), source supplier for inbound (supplier_id), destination customer for outbound (customer_id), shi…

**System answer:**
> The `shipment` table captures material transfer records. It tracks transfers between warehouses, suppliers, and customers, rather than a generic shipment abstraction.

It stores the following information: a unique shipment identifier (`shipment_id`); the transfer type (`shipment_type`), which can be `INBOUND`, `OUTBOUND`, or `INTERNAL`; the warehouse involved (`warehouse_id`, foreign key to `wareh…

**Sources retrieved (12):** `Material Transfer`, `Material Transfer→SHIPMENT`, `SHIPMENT→WAREHOUSE`, `SHIPMENT→SUPPLIER`, `parent_chunk_data_dictionary.md_8`, `parent_chunk_data_dictionary.md_5`, `parent_chunk_business_glossary.md_0`, `parent_chunk_business_glossary.md_1`

**Context previews (first 3):**

1. _Material Transfer: The table is explicitly described as a shipment/material transfer record and its columns capture transfer type, source/destination references, ship and arrival dates, and status. Th…_

2. _Business concept 'Material Transfer' — The table is explicitly described as a shipment/material transfer record and its columns capture transfer type, source/destination references, ship and arrival d…_

3. _Relationship: SHIPMENT references WAREHOUSE via foreign key WAREHOUSE_ID -> WAREHOUSE.WAREHOUSE_ID.…_

---

### ✅ QA-009 — How does the quality control system record inspections?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.9540 | **Gate:** `proceed`

**Expected answer:**
> Quality control records are stored with a unique identifier (qc_id), associated production batch (batch_id), applicable specification requirements (specification_id), inspection date (qc_date), inspection type (INCOMING for supplier materials, IN_PROCESS during manufacturing, FINAL for finished good…

**System answer:**
> The quality control system records inspections as QC records in the physical table QUALITY_CONTROL, which implements the business concept Quality Control (QC). Each inspection is stored with qc_id as the unique inspection identifier, batch_id to identify the production batch being inspected, specification_id to identify the technical specification being tested, qc_date for when the inspection occu…

**Sources retrieved (12):** `Quality Control (QC)→QUALITY_CONTROL`, `BOM→PRODUCT`, `parent_chunk_data_dictionary.md_3`, `BATCH→PRODUCT`, `BATCH→WAREHOUSE`, `Material Transfer`, `parent_chunk_business_glossary.md_2`, `parent_chunk_business_glossary.md_0`

**Context previews (first 3):**

1. _Business concept 'Quality Control (QC)' is implemented by physical table QUALITY_CONTROL (columns: qc_id, batch_id, specification_id, qc_date, qc_type, inspector_id, result, defect_count, notes).…_

2. _Relationship: BOM references PRODUCT via foreign key COMPONENT_PRODUCT_ID -> PRODUCT.PRODUCT_ID.…_

3. _# Manufacturing Data Dictionary  This data dictionary documents the database schema for the manufacturing supply chain system. It includes all tables, columns, data types, constraints, and relationshi…_

---

### ✅ QA-010 — What do specification records define?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.7558 | **Gate:** `proceed`

**Expected answer:**
> Specifications define technical requirements with a unique identifier (specification_id), descriptive name (specification_name), version number, effective date, specification type (DIMENSIONAL, MATERIAL, PERFORMANCE), critical parameter being measured (critical_parameter), acceptable minimum value (…

**System answer:**
> Specification records define the technical requirements, standards, and acceptance criteria for materials and products. In this schema, a Specification captures the specification name and version, effective date, specification type, the critical parameter being tested, acceptable minimum and maximum values, and the unit of measure. These records are used to define the quality requirements that QC …

**Sources retrieved (12):** `a standard cost, unit of measure, and may be associated with technical specifications that define quality requirements→SPECIFICATION`, `parent_chunk_data_dictionary.md_7`, `Quality Control (QC)→QUALITY_CONTROL`, `Warehouse Stock Levels→INVENTORY`, `parent_chunk_data_dictionary.md_3`, `parent_chunk_business_glossary.md_2`, `parent_chunk_business_glossary.md_0`, `a standard cost, unit of measure, and may be associated with technical specifications that define quality requirements`

**Context previews (first 3):**

1. _Business concept 'a standard cost, unit of measure, and may be associated with technical specifications that define quality requirements' is implemented by physical table SPECIFICATION (columns: speci…_

2. _## specification  Defines technical requirements and acceptance criteria for materials and products.  | Column | Data Type | Constraints | Description | |--------|-----------|-------------|-----------…_

3. _Business concept 'Quality Control (QC)' is implemented by physical table QUALITY_CONTROL (columns: qc_id, batch_id, specification_id, qc_date, qc_type, inspector_id, result, defect_count, notes).…_

---

### ✅ QA-011 — How can I find which suppliers provide specific components?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.3227 | **Gate:** `proceed`

**Expected answer:**
> Query the component_supplier table which links components to their approved suppliers. This table contains the component identifier (component_id), supplier identifier (supplier_id), preferred supplier flag (is_preferred), lead time in days (lead_time_days), and unit price (unit_price). Join with th…

**System answer:**
> Use the `COMPONENT_SUPPLIER` table. It implements the business concept of “components they can provide through approved supplier relationships” and contains the linking columns `component_id` and `supplier_id`, plus relationship attributes `is_preferred`, `lead_time_days`, and `unit_price`.

To find suppliers for a specific component, use this path: `COMPONENT.COMPONENT_ID` → `COMPONENT_SUPPLIER.C…

**Sources retrieved (12):** `components they can provide through approved supplier relationships→COMPONENT_SUPPLIER`, `parent_chunk_data_dictionary.md_5`, `parent_chunk_data_dictionary.md_4`, `Actual stock levels of components and products stored in specific warehouses→WAREHOUSE`, `parent_chunk_data_dictionary.md_3`, `Warehouse Stock Levels→INVENTORY`, `components they can provide through approved supplier relationships`, `parent_chunk_business_glossary.md_0`

**Context previews (first 3):**

1. _Business concept 'components they can provide through approved supplier relationships' is implemented by physical table COMPONENT_SUPPLIER (columns: component_supplier_id, component_id, supplier_id, i…_

2. _## warehouse  Stores physical storage location information for inventory management.  | Column | Data Type | Constraints | Description | |--------|-----------|-------------|-------------| | warehouse_…_

3. _## bom  Bill of Materials defining product composition and hierarchical structure. Supports recursive relationships for multi-level assemblies.  | Column | Data Type | Constraints | Description | |---…_

---

### ✅ QA-012 — How do I trace which components are needed to fulfill a work order?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.2334 | **Gate:** `proceed`

**Expected answer:**
> Start with the work_order table to get the product_id being manufactured. Join to the bom table using product_id as parent_product_id to find all direct components and sub-assemblies. For each component_product_id, if it is an ASSEMBLY type product, recursively query the bom table again to explode m…

**System answer:**
> Use `WORK_ORDER` as the starting point.

A work order is implemented by `WORK_ORDER` with these relevant columns: `work_order_id`, `product_id`, `parent_work_order`, `quantity_ordered`, `quantity_completed`, `status`, `priority`, `planned_start_date`, `planned_end_date`, and `warehouse_id`. To trace what is needed for a specific work order, first identify the row by `WORK_ORDER.work_order_id`, the…

**Sources retrieved (12):** `Work Order`, `parent_chunk_data_dictionary.md_5`, `Work Order→WORK_ORDER`, `parent_chunk_data_dictionary.md_6`, `parent_chunk_data_dictionary.md_3`, `components they can provide through approved supplier relationships→COMPONENT_SUPPLIER`, `Warehouse Stock Levels→INVENTORY`, `parent_chunk_data_dictionary.md_8`

**Context previews (first 3):**

1. _Work Order: The table name, primary key, and foreign keys align directly with the business entity describing work orders. Its columns track planned versus completed quantities, status, priority, and p…_

2. _## warehouse  Stores physical storage location information for inventory management.  | Column | Data Type | Constraints | Description | |--------|-----------|-------------|-------------| | warehouse_…_

3. _Business concept 'Work Order' — The table name, primary key, and foreign keys align directly with the business entity describing work orders. Its columns track planned versus completed quantities, sta…_

---

### ✅ QA-013 — How can I identify which warehouses have available inventory for specific components?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.8876 | **Gate:** `proceed`

**Expected answer:**
> Query the inventory table filtered by component_id, joining with the warehouse table to get warehouse names and locations. Calculate available quantity as quantity_on_hand minus quantity_reserved. Filter for records where available quantity is greater than zero. Results show warehouse names, locatio…

**System answer:**
> Use the INVENTORY table as the starting point, because it records stock levels by warehouse and by item. For specific components, filter INVENTORY by COMPONENT_ID, then join to WAREHOUSE through the documented foreign key INVENTORY.WAREHOUSE_ID -> WAREHOUSE.WAREHOUSE_ID to identify the warehouse location and details.

From the retrieved context, the relevant structure is:
INVENTORY has inventory_i…

**Sources retrieved (12):** `Actual stock levels of components and products stored in specific warehouses→WAREHOUSE`, `parent_chunk_data_dictionary.md_5`, `Warehouse Stock Levels→INVENTORY`, `INVENTORY→WAREHOUSE`, `INVENTORY→COMPONENT`, `parent_chunk_data_dictionary.md_3`, `parent_chunk_data_dictionary.md_8`, `Actual stock levels of components and products stored in specific warehouses`

**Context previews (first 3):**

1. _Business concept 'Actual stock levels of components and products stored in specific warehouses' is implemented by physical table WAREHOUSE (columns: warehouse_id, warehouse_name, address, city, state,…_

2. _## warehouse  Stores physical storage location information for inventory management.  | Column | Data Type | Constraints | Description | |--------|-----------|-------------|-------------| | warehouse_…_

3. _Business concept 'Warehouse Stock Levels' — The table records stock quantities on hand and reserved, reorder threshold, and last restock date, all tied to a warehouse and either a component or product…_

---

### ✅ QA-014 — How do I find which shipments delivered materials from a specific supplier?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.3189 | **Gate:** `proceed`

**Expected answer:**
> Query the shipment table filtering by supplier_id and shipment_type = 'INBOUND'. Join with the warehouse table to show destination warehouses. Filter for status = 'DELIVERED' and include actual_arrival date. Results can be ordered by ship_date descending to show most recent deliveries first.

**System answer:**
> Use the SHIPMENT table, which implements the Material Transfer concept.

To find shipments that delivered materials from a specific supplier, filter SHIPMENT by supplier and by inbound delivered status. The relevant logic comes from these facts in the schema: SHIPMENT tracks material transfers, supplier_id is only valid for INBOUND shipments because of the chk_supplier_inbound constraint, and stat…

**Sources retrieved (12):** `Material Transfer`, `Material Transfer→SHIPMENT`, `parent_chunk_data_dictionary.md_8`, `SHIPMENT→SUPPLIER`, `parent_chunk_data_dictionary.md_5`, `Supplier Profile→SUPPLIER`, `parent_chunk_data_dictionary.md_7`, `parent_chunk_business_glossary.md_1`

**Context previews (first 3):**

1. _Material Transfer: The table is explicitly described as a shipment/material transfer record and its columns capture transfer type, source/destination references, ship and arrival dates, and status. Th…_

2. _Business concept 'Material Transfer' — The table is explicitly described as a shipment/material transfer record and its columns capture transfer type, source/destination references, ship and arrival d…_

3. _## shipment  Tracks material transfers between warehouses, suppliers, and customers.  | Column | Data Type | Constraints | Description | |--------|-----------|-------------|-------------| | shipment_i…_

---

### ✅ QA-015 — How can I determine which quality control inspections were performed on a specific production batch?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.9779 | **Gate:** `proceed`

**Expected answer:**
> Query the quality_control table filtered by batch_id. Join with the specification table to get requirement details (specification_name, spec_type, acceptable ranges). Include qc_date, qc_type (INCOMING, IN_PROCESS, FINAL), result (PASS, FAIL, CONDITIONAL), and defect_count. This shows the complete i…

**System answer:**
> Use the `QUALITY_CONTROL` table, which implements the business concept “Quality Control (QC).” To determine which inspections were performed on a specific production batch, find all `QUALITY_CONTROL` records where `QUALITY_CONTROL.batch_id` matches the target batch’s `BATCH.batch_id`.

The key join path is `BATCH.batch_id = QUALITY_CONTROL.batch_id`. The `QUALITY_CONTROL` rows for that batch ident…

**Sources retrieved (12):** `Quality Control (QC)→QUALITY_CONTROL`, `parent_chunk_data_dictionary.md_7`, `Production batch reference→BATCH`, `BATCH→PRODUCT`, `parent_chunk_data_dictionary.md_5`, `parent_chunk_data_dictionary.md_6`, `parent_chunk_data_dictionary.md_3`, `parent_chunk_business_glossary.md_2`

**Context previews (first 3):**

1. _Business concept 'Quality Control (QC)' is implemented by physical table QUALITY_CONTROL (columns: qc_id, batch_id, specification_id, qc_date, qc_type, inspector_id, result, defect_count, notes).…_

2. _## specification  Defines technical requirements and acceptance criteria for materials and products.  | Column | Data Type | Constraints | Description | |--------|-----------|-------------|-----------…_

3. _Business concept 'Production batch reference' is implemented by physical table BATCH (columns: batch_id, product_id, production_date, quantity_produced, warehouse_id, expiry_date, qc_status).…_

---

### ✅ QA-016 — How do I track which work orders are in progress at a specific warehouse?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.7311 | **Gate:** `proceed`

**Expected answer:**
> Query the work_order table filtering by warehouse_id and status = 'IN_PROGRESS'. Join with the product table to get product names and types. Include quantity_ordered, quantity_completed, priority, planned_end_date, and calculate progress percentage as (quantity_completed / quantity_ordered * 100). O…

**System answer:**
> Use the `WORK_ORDER` table and filter by both the warehouse and the work order status.

The relevant relationship is `WORK_ORDER.WAREHOUSE_ID -> WAREHOUSE.WAREHOUSE_ID`, so a work order is tied to its production location through `warehouse_id`. In the `work_order` table, the `status` column is defined with values `PENDING`, `IN_PROGRESS`, `COMPLETED`, and `CLOSED`. To track work orders that are cu…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_5`, `Work Order→WORK_ORDER`, `parent_chunk_data_dictionary.md_6`, `WORK_ORDER→WAREHOUSE`, `Work Order`, `Warehouse Stock Levels→INVENTORY`, `Actual stock levels of components and products stored in specific warehouses→WAREHOUSE`, `parent_chunk_data_dictionary.md_8`

**Context previews (first 3):**

1. _## warehouse  Stores physical storage location information for inventory management.  | Column | Data Type | Constraints | Description | |--------|-----------|-------------|-------------| | warehouse_…_

2. _Business concept 'Work Order' — The table name, primary key, and foreign keys align directly with the business entity describing work orders. Its columns track planned versus completed quantities, sta…_

3. _## work_order  Represents production jobs for manufacturing products with hierarchical work order support.  | Column | Data Type | Constraints | Description | |--------|-----------|-------------|-----…_

---

### ✅ QA-017 — How can I find which components need reordering based on current inventory levels?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.3710 | **Gate:** `proceed`

**Expected answer:**
> Query the inventory table and filter where quantity_on_hand minus quantity_reserved is less than reorder_threshold. Join with the component table to get component names, categories, and standard costs. Join with the warehouse table for location information. Results identify which components are belo…

**System answer:**
> Use the INVENTORY table, because it is the table that tracks warehouse stock levels for components and products. For components specifically, filter to inventory records where component_id is populated, since INVENTORY supports either a component or a product per record, not both.

The relevant INVENTORY columns are:
inventory_id, warehouse_id, component_id, product_id, quantity_on_hand, quantity_…

**Sources retrieved (12):** `Warehouse Stock Levels→INVENTORY`, `parent_chunk_data_dictionary.md_5`, `Actual stock levels of components and products stored in specific warehouses→WAREHOUSE`, `INVENTORY→COMPONENT`, `parent_chunk_data_dictionary.md_3`, `parent_chunk_data_dictionary.md_7`, `parent_chunk_business_glossary.md_1`, `Warehouse Stock Levels`

**Context previews (first 3):**

1. _Business concept 'Warehouse Stock Levels' — The table records stock quantities on hand and reserved, reorder threshold, and last restock date, all tied to a warehouse and either a component or product…_

2. _## warehouse  Stores physical storage location information for inventory management.  | Column | Data Type | Constraints | Description | |--------|-----------|-------------|-------------| | warehouse_…_

3. _Business concept 'Actual stock levels of components and products stored in specific warehouses' is implemented by physical table WAREHOUSE (columns: warehouse_id, warehouse_name, address, city, state,…_

---

### ✅ QA-018 — How do I determine the manufacturing route for a specific product?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0525 | **Gate:** `proceed_with_warning`

**Expected answer:**
> Query the route table filtering by product_id, ordered by sequence_number ascending. For each operation, retrieve operation_name, work_center, cycle_time_minutes, and setup_time_minutes. Join with the product table to get product details. The sequence of operations shows the complete manufacturing w…

**System answer:**
> Use the `ROUTE` table. It implements the manufacturing production workflow information and contains the route definition for each product through `product_id`.

To determine the manufacturing route for a specific product, trace it as `PRODUCT.product_id` → `ROUTE.product_id`, because `ROUTE` references `PRODUCT` via the foreign key `PRODUCT_ID -> PRODUCT.PRODUCT_ID`.

For the selected product, loo…

**Sources retrieved (12):** `product structures, materials management, production workflows, and quality assurance processes→ROUTE`, `parent_chunk_data_dictionary.md_6`, `ROUTE→PRODUCT`, `parent_chunk_data_dictionary.md_3`, `parent_chunk_data_dictionary.md_7`, `parent_chunk_data_dictionary.md_5`, `parent_chunk_data_dictionary.md_8`, `Warehouse Stock Levels→INVENTORY`

**Context previews (first 3):**

1. _Business concept 'product structures, materials management, production workflows, and quality assurance processes' is implemented by physical table ROUTE (columns: route_id, product_id, route_name, se…_

2. _## work_order  Represents production jobs for manufacturing products with hierarchical work order support.  | Column | Data Type | Constraints | Description | |--------|-----------|-------------|-----…_

3. _Relationship: ROUTE references PRODUCT via foreign key PRODUCT_ID -> PRODUCT.PRODUCT_ID.…_

---

### ✅ QA-019 — How can I find which batches are stored at a specific warehouse and their QC status?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.7533 | **Gate:** `proceed`

**Expected answer:**
> Query the batch table filtering by warehouse_id. Join with the product table to get product names and types. Include production_date, quantity_produced, expiry_date, and qc_status (PENDING, PASSED, FAILED, QUARANTINED). Filter by qc_status to isolate batches requiring quality attention or ready for …

**System answer:**
> Use the BATCH table as the primary source. The business concept “Production batch reference” is implemented by BATCH, and BATCH includes both warehouse_id and qc_status. It also has a foreign key relationship to WAREHOUSE through BATCH.warehouse_id -> WAREHOUSE.warehouse_id.

So, to find which batches are stored at a specific warehouse and their QC status, filter BATCH by the target warehouse_id. …

**Sources retrieved (12):** `Production batch reference→BATCH`, `parent_chunk_data_dictionary.md_5`, `Actual stock levels of components and products stored in specific warehouses→WAREHOUSE`, `Warehouse Stock Levels→INVENTORY`, `BATCH→WAREHOUSE`, `Quality Control (QC)→QUALITY_CONTROL`, `parent_chunk_data_dictionary.md_6`, `parent_chunk_data_dictionary.md_8`

**Context previews (first 3):**

1. _Business concept 'Production batch reference' is implemented by physical table BATCH (columns: batch_id, product_id, production_date, quantity_produced, warehouse_id, expiry_date, qc_status).…_

2. _## warehouse  Stores physical storage location information for inventory management.  | Column | Data Type | Constraints | Description | |--------|-----------|-------------|-------------| | warehouse_…_

3. _Business concept 'Actual stock levels of components and products stored in specific warehouses' is implemented by physical table WAREHOUSE (columns: warehouse_id, warehouse_name, address, city, state,…_

---

### ✅ QA-020 — How do I identify which specifications apply to specific components?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.2550 | **Gate:** `proceed`

**Expected answer:**
> Query the component table and join with the specification table via specification_id. Include component_name, component_category, and specification details (specification_name, spec_type, critical_parameter, min_value, max_value, unit_of_measure). This shows the technical requirements that each comp…

**System answer:**
> Use the `COMPONENT` table’s `specification_id` column to link a component to its applicable specification in the `SPECIFICATION` table.

From the retrieved context, the business concept for components is implemented by `COMPONENT(component_id, component_name, component_category, unit_of_measure, standard_cost, specification_id)`, and `SPECIFICATION` has primary key `specification_id` plus the spec…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_5`, `negotiated pricing and lead times per component→COMPONENT`, `parent_chunk_data_dictionary.md_7`, `Warehouse Stock Levels→INVENTORY`, `parent_chunk_data_dictionary.md_3`, `Actual stock levels of components and products stored in specific warehouses→WAREHOUSE`, `a standard cost, unit of measure, and may be associated with technical specifications that define quality requirements→SPECIFICATION`, `parent_chunk_data_dictionary.md_4`

**Context previews (first 3):**

1. _## warehouse  Stores physical storage location information for inventory management.  | Column | Data Type | Constraints | Description | |--------|-----------|-------------|-------------| | warehouse_…_

2. _Business concept 'negotiated pricing and lead times per component' is implemented by physical table COMPONENT (columns: component_id, component_name, component_category, unit_of_measure, standard_cost…_

3. _## specification  Defines technical requirements and acceptance criteria for materials and products.  | Column | Data Type | Constraints | Description | |--------|-----------|-------------|-----------…_

---

### ✅ QA-021 — How can I perform a complete BOM explosion to find all components required for a finished product?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.3509 | **Gate:** `proceed`

**Expected answer:**
> Use a recursive query starting from the product_id of the finished good. At each level, join the bom table to find component_product_id entries. For each component, check if product_type is 'ASSEMBLY' or 'FINISHED_GOOD'. If so, recursively query bom again using that component_product_id as the new p…

**System answer:**
> At the schema level, a complete BOM explosion is based on the `bom` table, which is the table that “defines product composition and hierarchical structure” and “supports recursive relationships for multi-level assemblies.”

You would start with the finished product’s `product.product_id` and use `bom.parent_product_id` to find its BOM entries. Each BOM entry gives you the required `component_produ…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_4`, `parent_chunk_data_dictionary.md_3`, `Bill of Materials Entry→BOM`, `BOM→PRODUCT`, `parent_chunk_data_dictionary.md_5`, `parent_chunk_data_dictionary.md_7`, `parent_chunk_data_dictionary.md_6`, `parent_chunk_data_dictionary.md_8`

**Context previews (first 3):**

1. _## bom  Bill of Materials defining product composition and hierarchical structure. Supports recursive relationships for multi-level assemblies.  | Column | Data Type | Constraints | Description | |---…_

2. _# Manufacturing Data Dictionary  This data dictionary documents the database schema for the manufacturing supply chain system. It includes all tables, columns, data types, constraints, and relationshi…_

3. _Business concept 'Bill of Materials Entry' — The table directly models parent_product_id to component_product_id relationships with quantity, unit_of_measure, bom_level, and is_optional, which matches…_

---

### ✅ QA-022 — How do I calculate the total material cost for a product including all sub-assemblies?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.2332 | **Gate:** `proceed`

**Expected answer:**
> Perform a recursive BOM explosion to find all leaf-level components. For each leaf component, join with the component table to get standard_cost. Multiply standard_cost by the accumulated quantity from the BOM traversal. Sum all component costs to get total material cost. This calculation must trave…

**System answer:**
> From the retrieved context, the schema-supported way to calculate a product’s total material cost including all sub-assemblies is to do a recursive BOM roll-up using `bom` and `product`.

The relevant structure is this: `bom` defines the composition of a product through `parent_product_id` → `component_product_id`, with `quantity`, `unit_of_measure`, `bom_level`, and `is_optional`. Both `parent_pr…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_3`, `parent_chunk_data_dictionary.md_4`, `parent_chunk_data_dictionary.md_7`, `parent_chunk_data_dictionary.md_8`, `Bill of Materials Entry→BOM`, `parent_chunk_data_dictionary.md_6`, `parent_chunk_data_dictionary.md_5`, `(product_id, sequence_number)→PRODUCT`

**Context previews (first 3):**

1. _# Manufacturing Data Dictionary  This data dictionary documents the database schema for the manufacturing supply chain system. It includes all tables, columns, data types, constraints, and relationshi…_

2. _## bom  Bill of Materials defining product composition and hierarchical structure. Supports recursive relationships for multi-level assemblies.  | Column | Data Type | Constraints | Description | |---…_

3. _## specification  Defines technical requirements and acceptance criteria for materials and products.  | Column | Data Type | Constraints | Description | |--------|-----------|-------------|-----------…_

---

### ✅ QA-023 — How can I find all parent products that contain a specific component anywhere in their BOM structure?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.5213 | **Gate:** `proceed`

**Expected answer:**
> Use a recursive reverse traversal of the BOM. Start with the component_id as the initial parent_product_id. Find all records where this product appears as component_product_id in the bom table. For each parent_product_id found, check if it appears as a component_product_id in other bom records (is a…

**System answer:**
> Use the `bom` table as a recursive hierarchy.

The schema shows that `bom.parent_product_id` is “what is being built” and `bom.component_product_id` is “what goes into it,” and the table explicitly “supports recursive relationships for multi-level assemblies.” So to find every parent product that contains a specific component anywhere in the structure, start from BOM rows where `component_product_…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_4`, `parent_chunk_data_dictionary.md_3`, `Bill of Materials Entry→BOM`, `BOM→PRODUCT`, `PRODUCT→PRODUCT`, `parent_chunk_data_dictionary.md_6`, `parent_chunk_data_dictionary.md_8`, `parent_chunk_data_dictionary.md_5`

**Context previews (first 3):**

1. _## bom  Bill of Materials defining product composition and hierarchical structure. Supports recursive relationships for multi-level assemblies.  | Column | Data Type | Constraints | Description | |---…_

2. _# Manufacturing Data Dictionary  This data dictionary documents the database schema for the manufacturing supply chain system. It includes all tables, columns, data types, constraints, and relationshi…_

3. _Business concept 'Bill of Materials Entry' — The table directly models parent_product_id to component_product_id relationships with quantity, unit_of_measure, bom_level, and is_optional, which matches…_

---

### ✅ QA-024 — How do I identify work orders that require a specific component, considering nested sub-assemblies?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.3651 | **Gate:** `proceed`

**Expected answer:**
> First, perform reverse BOM traversal to find all parent products that contain the target component at any level. Then query the work_order table where product_id is in the set of parent products found. This includes work orders for finished goods that contain the component indirectly through sub-ass…

**System answer:**
> Use the `work_order`, `bom`, and `product` structures together.

A work order requires a component when the product being manufactured in `work_order.product_id` has that component somewhere in its Bill of Materials. The direct join starts at `work_order.product_id = bom.parent_product_id`. That gives the first level of components for the work order’s product.

To handle nested sub-assemblies, do …

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_6`, `parent_chunk_data_dictionary.md_5`, `parent_chunk_data_dictionary.md_3`, `Work Order`, `Work Order→WORK_ORDER`, `parent_chunk_data_dictionary.md_4`, `WORK_ORDER→WORK_ORDER`, `WORK_ORDER→PRODUCT`

**Context previews (first 3):**

1. _## work_order  Represents production jobs for manufacturing products with hierarchical work order support.  | Column | Data Type | Constraints | Description | |--------|-----------|-------------|-----…_

2. _## warehouse  Stores physical storage location information for inventory management.  | Column | Data Type | Constraints | Description | |--------|-----------|-------------|-------------| | warehouse_…_

3. _# Manufacturing Data Dictionary  This data dictionary documents the database schema for the manufacturing supply chain system. It includes all tables, columns, data types, constraints, and relationshi…_

---

### ✅ QA-025 — How can I determine the maximum BOM depth level for any product?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.2424 | **Gate:** `proceed`

**Expected answer:**
> Use a recursive query on the bom table, incrementing a level counter at each traversal. Start with bom_level = 0 and add 1 for each recursive step. Track the maximum level reached across all product hierarchies. This identifies the most complex product structures with the deepest nesting.

**System answer:**
> From the retrieved context, the depth indicator already exists in the `BOM` table as `bom_level`. That column is defined as the “Depth in product hierarchy,” with `DEFAULT 0` and `CHECK >= 0`, and the table is explicitly described as supporting recursive, multi-level assemblies.

So, to determine the maximum BOM depth level:

For the entire system, you would look at the highest value in `BOM.bom_l…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_4`, `parent_chunk_data_dictionary.md_3`, `Bill of Materials Entry→BOM`, `BOM→PRODUCT`, `parent_chunk_data_dictionary.md_7`, `parent_chunk_data_dictionary.md_5`, `parent_chunk_data_dictionary.md_6`, `Warehouse Stock Levels→INVENTORY`

**Context previews (first 3):**

1. _## bom  Bill of Materials defining product composition and hierarchical structure. Supports recursive relationships for multi-level assemblies.  | Column | Data Type | Constraints | Description | |---…_

2. _# Manufacturing Data Dictionary  This data dictionary documents the database schema for the manufacturing supply chain system. It includes all tables, columns, data types, constraints, and relationshi…_

3. _Business concept 'Bill of Materials Entry' — The table directly models parent_product_id to component_product_id relationships with quantity, unit_of_measure, bom_level, and is_optional, which matches…_

---

### ✅ QA-026 — How do I find all products that have a specific product as a sub-assembly at any level?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.2392 | **Gate:** `proceed`

**Expected answer:**
> Perform a recursive search starting with the target product_id as the initial component_product_id in the bom table. For each parent_product_id found, check if that parent appears as a component in other bom entries. Continue recursively until reaching products that are not used as components elsewh…

**System answer:**
> Use the BOM hierarchy, not just the product name column, because the `bom` table is the structure that explicitly defines composition: `bom.parent_product_id` is the product being built, and `bom.component_product_id` is what goes into it. The context says this supports recursive, multi-level assemblies such as “Bicycle → Wheel → Spoke.”

To find all products that contain a specific product as a s…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_3`, `parent_chunk_data_dictionary.md_4`, `parent_chunk_data_dictionary.md_5`, `Warehouse Stock Levels→INVENTORY`, `parent_chunk_data_dictionary.md_7`, `Bill of Materials Entry→BOM`, `Actual stock levels of components and products stored in specific warehouses→WAREHOUSE`, `parent_chunk_data_dictionary.md_6`

**Context previews (first 3):**

1. _# Manufacturing Data Dictionary  This data dictionary documents the database schema for the manufacturing supply chain system. It includes all tables, columns, data types, constraints, and relationshi…_

2. _## bom  Bill of Materials defining product composition and hierarchical structure. Supports recursive relationships for multi-level assemblies.  | Column | Data Type | Constraints | Description | |---…_

3. _## warehouse  Stores physical storage location information for inventory management.  | Column | Data Type | Constraints | Description | |--------|-----------|-------------|-------------| | warehouse_…_

---

### ✅ QA-027 — How can I calculate the total lead time for a product including all sub-assembly lead times?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.3462 | **Gate:** `proceed`

**Expected answer:**
> Perform a recursive BOM explosion to find all components and sub-assemblies. For each product_id in the hierarchy, retrieve lead_time_days from the product table. The total lead time is the maximum of all lead times in the hierarchy (representing the longest dependency chain), or optionally sum lead…

**System answer:**
> From the retrieved context, the schema supports this calculation at the product-structure level, but it does not define a single mandated formula for “total lead time.” What it does provide is the hierarchy and the lead-time field you would use.

The core source column is `product.lead_time_days`, described as the procurement or production lead time for a product. To include sub-assemblies, you ne…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_3`, `(product_id, sequence_number)→PRODUCT`, `negotiated pricing and lead times per component→COMPONENT`, `components they can provide through approved supplier relationships→COMPONENT_SUPPLIER`, `parent_chunk_data_dictionary.md_4`, `parent_chunk_data_dictionary.md_7`, `parent_chunk_data_dictionary.md_6`, `parent_chunk_data_dictionary.md_8`

**Context previews (first 3):**

1. _# Manufacturing Data Dictionary  This data dictionary documents the database schema for the manufacturing supply chain system. It includes all tables, columns, data types, constraints, and relationshi…_

2. _Business concept '(product_id, sequence_number)' is implemented by physical table PRODUCT (columns: product_id, product_name, product_type, parent_product_id, base_cost, lead_time_days, is_active).…_

3. _Business concept 'negotiated pricing and lead times per component' is implemented by physical table COMPONENT (columns: component_id, component_name, component_category, unit_of_measure, standard_cost…_

---

### ✅ QA-028 — How do I generate a complete indented BOM report showing the hierarchical structure?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.4180 | **Gate:** `proceed`

**Expected answer:**
> Use a recursive query on the bom table that tracks the current depth level. Start with the top-level product (parent_product_id where product has no parent_product_id). At each level, output component details indented by depth level. Include product_name, quantity, and unit_of_measure. Recursively p…

**System answer:**
> To generate a complete indented BOM report, use the `bom` table as the primary source, because it is the table that directly defines product composition and hierarchical structure. It contains the exact BOM line attributes needed for the report: `parent_product_id`, `component_product_id`, `quantity`, `unit_of_measure`, `bom_level`, and `is_optional`.

The join path is:

`bom.parent_product_id -> …

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_4`, `parent_chunk_data_dictionary.md_3`, `Bill of Materials Entry→BOM`, `parent_chunk_data_dictionary.md_6`, `parent_chunk_data_dictionary.md_8`, `BOM→PRODUCT`, `product structures, materials management, production workflows, and quality assurance processes→ROUTE`, `parent_chunk_business_glossary.md_0`

**Context previews (first 3):**

1. _## bom  Bill of Materials defining product composition and hierarchical structure. Supports recursive relationships for multi-level assemblies.  | Column | Data Type | Constraints | Description | |---…_

2. _# Manufacturing Data Dictionary  This data dictionary documents the database schema for the manufacturing supply chain system. It includes all tables, columns, data types, constraints, and relationshi…_

3. _Business concept 'Bill of Materials Entry' — The table directly models parent_product_id to component_product_id relationships with quantity, unit_of_measure, bom_level, and is_optional, which matches…_

---

### ✅ QA-029 — How can I find which components appear most frequently across all product BOMs?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.1587 | **Gate:** `proceed_with_warning`

**Expected answer:**
> Perform BOM explosion for all products and aggregate occurrences of each leaf-level component. Count how many distinct product hierarchies contain each component. Join with component table for component names. Order by frequency descending to identify common components that should be prioritized for…

**System answer:**
> Use the `bom` table as the source, because it directly stores each BOM entry as a `parent_product_id` to `component_product_id` relationship.

To find which components appear most frequently across all product BOMs, count BOM rows grouped by `bom.component_product_id`, then sort the counts descending. If you want readable names, join `bom.component_product_id` to `product.product_id` and return `p…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_4`, `parent_chunk_data_dictionary.md_3`, `Bill of Materials Entry→BOM`, `BOM→PRODUCT`, `parent_chunk_data_dictionary.md_5`, `Warehouse Stock Levels→INVENTORY`, `Actual stock levels of components and products stored in specific warehouses→WAREHOUSE`, `parent_chunk_data_dictionary.md_7`

**Context previews (first 3):**

1. _## bom  Bill of Materials defining product composition and hierarchical structure. Supports recursive relationships for multi-level assemblies.  | Column | Data Type | Constraints | Description | |---…_

2. _# Manufacturing Data Dictionary  This data dictionary documents the database schema for the manufacturing supply chain system. It includes all tables, columns, data types, constraints, and relationshi…_

3. _Business concept 'Bill of Materials Entry' — The table directly models parent_product_id to component_product_id relationships with quantity, unit_of_measure, bom_level, and is_optional, which matches…_

---

### ✅ QA-030 — How do I detect circular references in the BOM structure to prevent infinite loops?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.1295 | **Gate:** `proceed_with_warning`

**Expected answer:**
> Use a recursive query with a cycle detection check. Track the path of visited product_ids at each recursion level. If a product_id appears twice in the same path, a circular reference exists. Alternatively, check if any bom record has parent_product_id = component_product_id (direct self-reference),…

**System answer:**
> The retrieved context does not document a specific rule, constraint, or SQL procedure for detecting circular BOM references.

What is known from the context is that circular-reference analysis would have to be done against the recursive structure in the `bom` table. The relevant columns are `bom.parent_product_id` and `bom.component_product_id`, and both are foreign keys to `product(product_id)`. …

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_4`, `parent_chunk_data_dictionary.md_3`, `BOM→PRODUCT`, `Bill of Materials Entry→BOM`, `parent_chunk_data_dictionary.md_8`, `parent_chunk_data_dictionary.md_7`, `parent_chunk_business_glossary.md_0`, `Bill of Materials Entry`

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
> From the retrieved context, you can determine the complete product structure for a finished product, but you cannot fully determine the complete supplier chain for that structure because the context does not show a table that links a supplier to a specific product, component, or BOM line.

The part that is supported is the product and sub-assembly explosion. Start with the finished product in `pro…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_3`, `parent_chunk_data_dictionary.md_4`, `parent_chunk_data_dictionary.md_8`, `parent_chunk_data_dictionary.md_6`, `Supplier Profile→SUPPLIER`, `parent_chunk_data_dictionary.md_7`, `Material Transfer→SHIPMENT`, `Bill of Materials Entry→BOM`

**Context previews (first 3):**

1. _# Manufacturing Data Dictionary  This data dictionary documents the database schema for the manufacturing supply chain system. It includes all tables, columns, data types, constraints, and relationshi…_

2. _## bom  Bill of Materials defining product composition and hierarchical structure. Supports recursive relationships for multi-level assemblies.  | Column | Data Type | Constraints | Description | |---…_

3. _## shipment  Tracks material transfers between warehouses, suppliers, and customers.  | Column | Data Type | Constraints | Description | |--------|-----------|-------------|-------------| | shipment_i…_

---

### ✅ QA-032 — How do I check if sufficient inventory exists across all warehouses to fulfill a work order?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.4035 | **Gate:** `proceed`

**Expected answer:**
> For the work_order's product_id, perform recursive BOM explosion to get all required components with quantities. For each component, sum the available quantity (quantity_on_hand - quantity_reserved) across all warehouses from the inventory table. Compare aggregated available inventory against requir…

**System answer:**
> From the retrieved context, you can only answer this at a schema level, not with a definitive business rule.

What is known is that `WORK_ORDER` identifies the product to manufacture through `WORK_ORDER.product_id`, tracks `quantity_ordered` and `quantity_completed`, and is linked to a production location through `WORK_ORDER.warehouse_id`. The `INVENTORY` table stores actual stock levels by wareho…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_5`, `parent_chunk_data_dictionary.md_6`, `Warehouse Stock Levels→INVENTORY`, `Work Order→WORK_ORDER`, `INVENTORY→WAREHOUSE`, `Work Order`, `Actual stock levels of components and products stored in specific warehouses→WAREHOUSE`, `WORK_ORDER→WAREHOUSE`

**Context previews (first 3):**

1. _## warehouse  Stores physical storage location information for inventory management.  | Column | Data Type | Constraints | Description | |--------|-----------|-------------|-------------| | warehouse_…_

2. _## work_order  Represents production jobs for manufacturing products with hierarchical work order support.  | Column | Data Type | Constraints | Description | |--------|-----------|-------------|-----…_

3. _Business concept 'Warehouse Stock Levels' — The table records stock quantities on hand and reserved, reorder threshold, and last restock date, all tied to a warehouse and either a component or product…_

---

### ✅ QA-033 — How can I find which quality control inspections failed for components from specific suppliers?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.4561 | **Gate:** `proceed`

**Expected answer:**
> Query the quality_control table filtering by result = 'FAIL'. Join with the batch table to get product_id and production_date. Join with the bom table recursively to trace which products contain failed components. Join with component_supplier and supplier tables to identify the source supplier. Filt…

**System answer:**
> From the retrieved context, you can only answer this partially at the schema level.

Failed quality inspections are stored in `QUALITY_CONTROL`, using `result`. To find failures, you would filter `QUALITY_CONTROL.result = 'FAIL'`. The relevant QC fields available are `qc_id`, `batch_id`, `specification_id`, `qc_date`, `qc_type`, `inspector_id`, `result`, `defect_count`, and `notes`.

Supplier-to-c…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_5`, `parent_chunk_data_dictionary.md_3`, `Quality Control (QC)→QUALITY_CONTROL`, `components they can provide through approved supplier relationships→COMPONENT_SUPPLIER`, `parent_chunk_data_dictionary.md_4`, `Actual stock levels of components and products stored in specific warehouses→WAREHOUSE`, `COMPONENT_SUPPLIER→SUPPLIER`, `parent_chunk_data_dictionary.md_8`

**Context previews (first 3):**

1. _## warehouse  Stores physical storage location information for inventory management.  | Column | Data Type | Constraints | Description | |--------|-----------|-------------|-------------| | warehouse_…_

2. _# Manufacturing Data Dictionary  This data dictionary documents the database schema for the manufacturing supply chain system. It includes all tables, columns, data types, constraints, and relationshi…_

3. _Business concept 'Quality Control (QC)' is implemented by physical table QUALITY_CONTROL (columns: qc_id, batch_id, specification_id, qc_date, qc_type, inspector_id, result, defect_count, notes).…_

---

### ✅ QA-034 — How do I calculate the total manufacturing time for a work order including all sub-assembly work orders?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.1599 | **Gate:** `proceed_with_warning`

**Expected answer:**
> Query the work_order table starting with the parent work_order. Find all child work_orders where parent_work_order matches the current work_order_id. For each work order (parent and children), join with the route table on product_id to get all operations. Sum (cycle_time_minutes * quantity) plus set…

**System answer:**
> From the retrieved context, you can identify the work orders and route-time fields involved, but you cannot derive a fully supported business formula for “total manufacturing time.”

What is known is this: `WORK_ORDER.parent_work_order` is a self-reference to `WORK_ORDER.work_order_id`, and the context says this “enables work order decomposition” so a large production job can be broken into child …

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_6`, `parent_chunk_data_dictionary.md_3`, `Work Order→WORK_ORDER`, `Work Order`, `parent_chunk_data_dictionary.md_7`, `parent_chunk_data_dictionary.md_5`, `parent_chunk_data_dictionary.md_4`, `product structures, materials management, production workflows, and quality assurance processes→ROUTE`

**Context previews (first 3):**

1. _## work_order  Represents production jobs for manufacturing products with hierarchical work order support.  | Column | Data Type | Constraints | Description | |--------|-----------|-------------|-----…_

2. _# Manufacturing Data Dictionary  This data dictionary documents the database schema for the manufacturing supply chain system. It includes all tables, columns, data types, constraints, and relationshi…_

3. _Business concept 'Work Order' — The table name, primary key, and foreign keys align directly with the business entity describing work orders. Its columns track planned versus completed quantities, sta…_

---

### ✅ QA-035 — How can I identify which shipments are overdue and their impact on work orders?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0719 | **Gate:** `proceed_with_warning`

**Expected answer:**
> Query the shipment table filtering for status = 'SHIPPED' where actual_arrival is NULL and estimated_arrival is in the past (overdue). Join with the component_supplier table via supplier_id and component_id to identify which components are delayed. Perform reverse BOM lookup to find which parent pro…

**System answer:**
> The knowledge graph contains schema-level metadata only, not live shipment or work order records, so it cannot tell you which specific shipments are overdue. It does show how to identify them structurally and how to trace their possible impact on work orders.

To identify overdue shipments, use the SHIPMENT table. The relevant columns are shipment_id, shipment_type, warehouse_id, supplier_id, cust…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_5`, `Work Order`, `parent_chunk_data_dictionary.md_8`, `Work Order→WORK_ORDER`, `parent_chunk_data_dictionary.md_6`, `Material Transfer→SHIPMENT`, `Material Transfer`, `WORK_ORDER→PRODUCT`

**Context previews (first 3):**

1. _## warehouse  Stores physical storage location information for inventory management.  | Column | Data Type | Constraints | Description | |--------|-----------|-------------|-------------| | warehouse_…_

2. _Work Order: The table name, primary key, and foreign keys align directly with the business entity describing work orders. Its columns track planned versus completed quantities, status, priority, and p…_

3. _## shipment  Tracks material transfers between warehouses, suppliers, and customers.  | Column | Data Type | Constraints | Description | |--------|-----------|-------------|-------------| | shipment_i…_

---

### ✅ QA-036 — How do I find which batches are approaching or past expiry and contain components from specific suppliers?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.1479 | **Gate:** `proceed_with_warning`

**Expected answer:**
> Query the batch table filtering for expiry_date within a warning window (e.g., next 30 days) or past expiry. Join with the bom table recursively on product_id to trace all components used in those batches. Join with component_supplier and supplier tables to filter by specific suppliers. Results iden…

**System answer:**
> From the retrieved context, you can identify expiry risk at the batch level from the BATCH table, but you cannot fully answer the supplier/component part with the available schema.

To find batches approaching or past expiry, use BATCH.expiry_date from the BATCH table described as “Tracks production lots for traceability and inventory management.” Relevant columns are batch_id, product_id, product…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_5`, `Warehouse Stock Levels→INVENTORY`, `Actual stock levels of components and products stored in specific warehouses→WAREHOUSE`, `parent_chunk_data_dictionary.md_7`, `parent_chunk_data_dictionary.md_3`, `Production batch reference→BATCH`, `parent_chunk_business_glossary.md_2`, `parent_chunk_business_glossary.md_1`

**Context previews (first 3):**

1. _## warehouse  Stores physical storage location information for inventory management.  | Column | Data Type | Constraints | Description | |--------|-----------|-------------|-------------| | warehouse_…_

2. _Business concept 'Warehouse Stock Levels' — The table records stock quantities on hand and reserved, reorder threshold, and last restock date, all tied to a warehouse and either a component or product…_

3. _Business concept 'Actual stock levels of components and products stored in specific warehouses' is implemented by physical table WAREHOUSE (columns: warehouse_id, warehouse_name, address, city, state,…_

---

### ✅ QA-037 — How can I generate a material requirements plan showing when to order components based on work order schedules?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0433 | **Gate:** `proceed_with_warning`

**Expected answer:**
> Query all work_orders with status 'PENDING' ordered by planned_start_date. For each work_order, perform BOM explosion to get required components and quantities. For each component, query inventory for current available stock across warehouses. Calculate net requirements = (required quantity * work_o…

**System answer:**
> From the retrieved schema, you can generate the component demand side of a material requirements plan, but you cannot support a factual rule for “when to order” components. The context provides the scheduling and quantity inputs, not an MRP calculation or ordering-date formula.

The core join path starts with WORK_ORDER, because it contains the production schedule and demand driver: `work_order_id…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_6`, `parent_chunk_data_dictionary.md_7`, `Work Order→WORK_ORDER`, `parent_chunk_data_dictionary.md_5`, `Work Order`, `parent_chunk_data_dictionary.md_4`, `parent_chunk_data_dictionary.md_3`, `Bill of Materials Entry→BOM`

**Context previews (first 3):**

1. _## work_order  Represents production jobs for manufacturing products with hierarchical work order support.  | Column | Data Type | Constraints | Description | |--------|-----------|-------------|-----…_

2. _## specification  Defines technical requirements and acceptance criteria for materials and products.  | Column | Data Type | Constraints | Description | |--------|-----------|-------------|-----------…_

3. _Business concept 'Work Order' — The table name, primary key, and foreign keys align directly with the business entity describing work orders. Its columns track planned versus completed quantities, sta…_

---

### ✅ QA-038 — How do I trace the complete genealogy of a component from supplier through batch to finished goods?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0748 | **Gate:** `proceed_with_warning`

**Expected answer:**
> Start with a shipment from the supplier (shipment table with supplier_id and shipment_type = 'INBOUND'). Track to inventory updates via component_id and warehouse_id. Identify batches that consumed the component via reverse BOM lookup (batch.product_id → bom hierarchy → component_id). Query quality_…

**System answer:**
> From the retrieved context, you can only trace this genealogy partially at the schema level.

The supplier side starts with `COMPONENT_SUPPLIER`, which implements approved supplier relationships and links `component_id` to `supplier_id`, with attributes such as `is_preferred`, `lead_time_days`, and `unit_price`. That gives you the supplier-to-component relationship. `SHIPMENT` can then show materi…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_3`, `parent_chunk_data_dictionary.md_7`, `parent_chunk_data_dictionary.md_5`, `parent_chunk_data_dictionary.md_8`, `parent_chunk_data_dictionary.md_4`, `components they can provide through approved supplier relationships→COMPONENT_SUPPLIER`, `COMPONENT_SUPPLIER→COMPONENT`, `Bill of Materials Entry→BOM`

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
> From the retrieved context, this can only be answered partially at the schema level.

What is known is that product structure and multi-product component usage can be analyzed from `bom`, and supplier options can be analyzed from `COMPONENT_SUPPLIER` plus `SUPPLIER`, but the context does not show a complete link between those two areas.

The part you can determine from the context is this: the `bo…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_4`, `parent_chunk_data_dictionary.md_3`, `components they can provide through approved supplier relationships→COMPONENT_SUPPLIER`, `parent_chunk_data_dictionary.md_5`, `parent_chunk_data_dictionary.md_8`, `parent_chunk_data_dictionary.md_7`, `Supplier Profile→SUPPLIER`, `COMPONENT_SUPPLIER→COMPONENT`

**Context previews (first 3):**

1. _## bom  Bill of Materials defining product composition and hierarchical structure. Supports recursive relationships for multi-level assemblies.  | Column | Data Type | Constraints | Description | |---…_

2. _# Manufacturing Data Dictionary  This data dictionary documents the database schema for the manufacturing supply chain system. It includes all tables, columns, data types, constraints, and relationshi…_

3. _Business concept 'components they can provide through approved supplier relationships' is implemented by physical table COMPONENT_SUPPLIER (columns: component_supplier_id, component_id, supplier_id, i…_

---

### ✅ QA-040 — How do I calculate the total landed cost for a product including component costs, supplier lead times, and manufacturing operations?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.1922 | **Gate:** `proceed_with_warning`

**Expected answer:**
> Perform recursive BOM explosion to get all leaf components. For each component, query component_supplier to get unit_price from primary supplier. Multiply by accumulated BOM quantity for material cost. Add shipping costs (estimated from shipment history). Query route table for the product to get all…

**System answer:**
> From the retrieved context, you cannot derive a complete total landed-cost formula for a product. The knowledge graph provides schema metadata and some cost-related columns, but it does not provide a full landed-cost calculation rule, the complete `BOM` definition, or the quantity requirements needed to roll component costs up into a finished product.

What the context does support is this schema-…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_3`, `components they can provide through approved supplier relationships→COMPONENT_SUPPLIER`, `negotiated pricing and lead times per component→COMPONENT`, `(product_id, sequence_number)→PRODUCT`, `parent_chunk_data_dictionary.md_6`, `parent_chunk_data_dictionary.md_7`, `parent_chunk_data_dictionary.md_5`, `parent_chunk_data_dictionary.md_8`

**Context previews (first 3):**

1. _# Manufacturing Data Dictionary  This data dictionary documents the database schema for the manufacturing supply chain system. It includes all tables, columns, data types, constraints, and relationshi…_

2. _Business concept 'components they can provide through approved supplier relationships' is implemented by physical table COMPONENT_SUPPLIER (columns: component_supplier_id, component_id, supplier_id, i…_

3. _Business concept 'negotiated pricing and lead times per component' is implemented by physical table COMPONENT (columns: component_id, component_name, component_category, unit_of_measure, standard_cost…_

---

## Anomalies & Observations

No anomalies detected. All questions grounded with acceptable RAGAS scores.
