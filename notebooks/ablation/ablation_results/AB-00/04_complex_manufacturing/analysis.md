# AB-00 — 04_complex_manufacturing — Run Analysis

**Timestamp:** 2026-03-30 19:13:32  
**Run tag:** `post-fix-v5`

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
| Triplets extracted | 371 |
| Entities resolved | 124 |
| Tables parsed | 13 |
| Tables completed | 13 |

## Query Evaluation Summary

| Metric | Value |
|--------|-------|
| Questions | 40 |
| Grounded | **40/40 (100%)** |
| Avg GT Coverage | 100% |
| Avg Top Score | 0.4150 |
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
> In the manufacturing system, the `product` table stores core master data for manufactured items, including finished goods, assemblies, and components. The physical schema shown stores `product_id` as the unique product identifier, `product_name`, `product_type`, `parent_product_id`, `base_cost`, `lead_time_days`, and `is_active`.

The product classification in `product_type` is `FINISHED_GOOD`, `A…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_3`, `parent_chunk_data_dictionary.md_6`, `Route Steps→ROUTE`, `parent_chunk_data_dictionary.md_5`, `parent_chunk_data_dictionary.md_7`, `parent_chunk_business_glossary.md_0`, `parent_chunk_business_glossary.md_1`, `parent_chunk_business_glossary.md_2`

**Context previews (first 3):**

1. _# Manufacturing Data Dictionary  This data dictionary documents the database schema for the manufacturing supply chain system. It includes all tables, columns, data types, constraints, and relationshi…_

2. _## work_order  Represents production jobs for manufacturing products with hierarchical work order support.  | Column | Data Type | Constraints | Description | |--------|-----------|-------------|-----…_

3. _Business concept 'Route Steps' — The table is clearly step-granular: `sequence_number`, `operation_name`, `work_center`, `cycle_time_minutes`, and `setup_time_minutes` describe individual routing step…_

---

### ✅ QA-002 — How are components defined in the manufacturing database?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.5910 | **Gate:** `proceed`

**Expected answer:**
> Components are defined with a unique identifier (component_id), descriptive name (component_name), category grouping (component_category), unit of measure (unit_of_measure), standard unit cost (standard_cost), and optional reference to technical specifications (specification_id). Components represen…

**System answer:**
> In the retrieved context, components are defined both as a business concept and through specific schema structures.

A Component is described in the business glossary as an atomic raw material or purchased part that cannot be further broken down into simpler manufactured items. Components are the building blocks used in manufacturing and are procured from external suppliers.

At the physical schem…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_3`, `a parent product, a component product (which can be either a component or sub-assembly), the required quantity, unit of measure, and hierarchical level in the product structure→COMPONENT`, `parent_chunk_data_dictionary.md_4`, `parent_chunk_data_dictionary.md_5`, `Approved Supplier Link→COMPONENT_SUPPLIER`, `BOM entry→BOM`, `parent_chunk_data_dictionary.md_6`, `parent_chunk_business_glossary.md_0`

**Context previews (first 3):**

1. _# Manufacturing Data Dictionary  This data dictionary documents the database schema for the manufacturing supply chain system. It includes all tables, columns, data types, constraints, and relationshi…_

2. _Business concept 'a parent product, a component product (which can be either a component or sub-assembly), the required quantity, unit of measure, and hierarchical level in the product structure' is i…_

3. _## bom  Bill of Materials defining product composition and hierarchical structure. Supports recursive relationships for multi-level assemblies.  | Column | Data Type | Constraints | Description | |---…_

---

### ✅ QA-003 — What is the purpose of the Bill of Materials (BOM) table?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.9118 | **Gate:** `proceed`

**Expected answer:**
> The BOM table defines the hierarchical structure of products by specifying which components or sub-assemblies are required to manufacture each parent product. It records the unique BOM entry identifier (bom_id), parent product being built (parent_product_id), component or sub-assembly product (compo…

**System answer:**
> The Bill of Materials table, `bom`, defines product composition and hierarchical structure. Its purpose is to record which component products go into a parent product, including the required `quantity`, `unit_of_measure`, whether the component `is_optional`, and the `bom_level` depth in the hierarchy.

From the schema, `bom` supports recursive, multi-level assemblies because both `parent_product_i…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_4`, `BOM→PRODUCT`, `BOM entry→BOM`, `parent_chunk_data_dictionary.md_3`, `parent_chunk_data_dictionary.md_7`, `parent_chunk_data_dictionary.md_8`, `parent_chunk_business_glossary.md_0`, `Material Transfers`

**Context previews (first 3):**

1. _## bom  Bill of Materials defining product composition and hierarchical structure. Supports recursive relationships for multi-level assemblies.  | Column | Data Type | Constraints | Description | |---…_

2. _Relationship: BOM references PRODUCT via foreign key COMPONENT_PRODUCT_ID -> PRODUCT.PRODUCT_ID.…_

3. _Business concept 'BOM entry' is implemented by physical table BOM (columns: bom_id, parent_product_id, component_product_id, quantity, unit_of_measure, bom_level, is_optional).…_

---

### ✅ QA-004 — What supplier information does the system maintain?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0325 | **Gate:** `proceed_with_warning`

**Expected answer:**
> Suppliers are tracked with a unique identifier (supplier_id), legal business name (supplier_name), primary contact email (contact_email), primary contact phone number (contact_phone), performance rating from 1.0 to 5.0 (rating), and preferred supplier status flag (is_preferred).

**System answer:**
> The system maintains supplier master data in the `SUPPLIER` table, which stores external vendor information for component procurement. From the retrieved context, the supplier attributes are `supplier_id`, `supplier_name`, `contact_email`, `contact_phone`, `rating`, and `is_preferred`. The business concept “Preferred supplier for this component” is mapped to `SUPPLIER`, so preferred status is expl…

**Sources retrieved (12):** `Preferred supplier for this component→SUPPLIER`, `parent_chunk_data_dictionary.md_4`, `Material Transfers`, `SHIPMENT→SUPPLIER`, `Material Transfers→SHIPMENT`, `parent_chunk_data_dictionary.md_8`, `COMPONENT_SUPPLIER→SUPPLIER`, `Approved Supplier Link→COMPONENT_SUPPLIER`

**Context previews (first 3):**

1. _Business concept 'Preferred supplier for this component' is implemented by physical table SUPPLIER (columns: supplier_id, supplier_name, contact_email, contact_phone, rating, is_preferred).…_

2. _## bom  Bill of Materials defining product composition and hierarchical structure. Supports recursive relationships for multi-level assemblies.  | Column | Data Type | Constraints | Description | |---…_

3. _Material Transfers: The DDL explicitly labels the table as material transfers and its columns model directional movements with shipment_type plus source/destination references to warehouse, supplier, …_

---

### ✅ QA-005 — How are warehouses represented in the schema?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.3381 | **Gate:** `proceed`

**Expected answer:**
> Warehouses are defined with a unique identifier (warehouse_id), descriptive name (warehouse_name), full street address (address), city location (city), state or province (state), total storage capacity in cubic meters (capacity), and optional manager identifier (manager_id).

**System answer:**
> Warehouses are represented by the physical table `WAREHOUSE`, which stores physical storage location information for inventory management and implements the business concept of geographic location information.

The `WAREHOUSE` table has these columns: `warehouse_id` as the primary key and unique warehouse identifier, `warehouse_name` as the required warehouse name, `address`, `city`, `state`, `cap…

**Sources retrieved (12):** `INVENTORY→WAREHOUSE`, `BATCH→WAREHOUSE`, `WORK_ORDER→WAREHOUSE`, `SHIPMENT→WAREHOUSE`, `parent_chunk_data_dictionary.md_6`, `parent_chunk_data_dictionary.md_5`, `geographic location information→WAREHOUSE`, `Material Transfers`

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
> The `INVENTORY` table tracks stock levels of components and products at specific warehouse locations. It represents the actual inventory held in each warehouse and records `quantity_on_hand`, `quantity_reserved`, `reorder_threshold`, and `last_restock_date`.

Each inventory record is tied to a `warehouse_id` and references either a `component_id` or a `product_id`—the two are exclusive, so a singl…

**Sources retrieved (12):** `INVENTORY→PRODUCT`, `Batches for traceability and inventory management→INVENTORY`, `INVENTORY→WAREHOUSE`, `INVENTORY→COMPONENT`, `parent_chunk_data_dictionary.md_5`, `Batches for traceability and inventory management→BATCH`, `parent_chunk_data_dictionary.md_7`, `parent_chunk_data_dictionary.md_8`

**Context previews (first 3):**

1. _Relationship: INVENTORY references PRODUCT via foreign key PRODUCT_ID -> PRODUCT.PRODUCT_ID.…_

2. _Business concept 'Batches for traceability and inventory management' is implemented by physical table INVENTORY (columns: inventory_id, warehouse_id, component_id, product_id, quantity_on_hand, quanti…_

3. _Relationship: INVENTORY references WAREHOUSE via foreign key WAREHOUSE_ID -> WAREHOUSE.WAREHOUSE_ID.…_

---

### ✅ QA-007 — How are work orders structured in the manufacturing system?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.4854 | **Gate:** `proceed`

**Expected answer:**
> Work orders represent production jobs with a unique identifier (work_order_id), product to be manufactured (product_id), optional parent work order for nested hierarchies (parent_work_order), quantity to produce (quantity_ordered), quantity completed so far (quantity_completed), current status (PEND…

**System answer:**
> Work orders are represented by the `WORK_ORDER` table and model production jobs for manufacturing products with hierarchical support. Each work order has a unique identifier in `work_order_id` and is tied to the product being manufactured through `product_id`, which is a foreign key to `PRODUCT.PRODUCT_ID`.

The structure supports decomposition of large production jobs into smaller child work orde…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_6`, `Work Order→WORK_ORDER`, `WORK_ORDER→PRODUCT`, `WORK_ORDER→WORK_ORDER`, `parent_chunk_data_dictionary.md_3`, `WORK_ORDER→WAREHOUSE`, `Route Steps→ROUTE`, `parent_chunk_business_glossary.md_0`

**Context previews (first 3):**

1. _## work_order  Represents production jobs for manufacturing products with hierarchical work order support.  | Column | Data Type | Constraints | Description | |--------|-----------|-------------|-----…_

2. _Business concept 'Work Order' — The table is explicitly labeled as WORK_ORDER and contains core work order attributes such as product_id, quantity ordered/completed, status, priority, planned dates, a…_

3. _Relationship: WORK_ORDER references PRODUCT via foreign key PRODUCT_ID -> PRODUCT.PRODUCT_ID.…_

---

### ✅ QA-008 — What information is captured in the shipment table?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.6545 | **Gate:** `proceed`

**Expected answer:**
> Shipments track material transfers with a unique identifier (shipment_id), shipment type (INBOUND from suppliers, OUTBOUND to customers, INTERNAL between warehouses), destination warehouse (warehouse_id), source supplier for inbound (supplier_id), destination customer for outbound (customer_id), shi…

**System answer:**
> The `shipment` table captures material transfer information between warehouses, suppliers, and customers. It is described as the physical implementation of the business concept “Material Transfers,” and it models directional movements using `shipment_type` plus source/destination references.

It stores:
`shipment_id`, the unique shipment identifier;
`shipment_type`, which must be `INBOUND`, `OUTBO…

**Sources retrieved (12):** `Material Transfers→SHIPMENT`, `SHIPMENT→WAREHOUSE`, `SHIPMENT→SUPPLIER`, `Material Transfers`, `parent_chunk_data_dictionary.md_8`, `parent_chunk_data_dictionary.md_5`, `parent_chunk_business_glossary.md_0`, `parent_chunk_business_glossary.md_1`

**Context previews (first 3):**

1. _Business concept 'Material Transfers' — The DDL explicitly labels the table as material transfers and its columns model directional movements with shipment_type plus source/destination references to w…_

2. _Relationship: SHIPMENT references WAREHOUSE via foreign key WAREHOUSE_ID -> WAREHOUSE.WAREHOUSE_ID.…_

3. _Relationship: SHIPMENT references SUPPLIER via foreign key SUPPLIER_ID -> SUPPLIER.SUPPLIER_ID.…_

---

### ✅ QA-009 — How does the quality control system record inspections?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.9540 | **Gate:** `proceed`

**Expected answer:**
> Quality control records are stored with a unique identifier (qc_id), associated production batch (batch_id), applicable specification requirements (specification_id), inspection date (qc_date), inspection type (INCOMING for supplier materials, IN_PROCESS during manufacturing, FINAL for finished good…

**System answer:**
> The quality control system records inspections in the physical table QUALITY_CONTROL, which implements the business concept “Quality Control inspections.”

An inspection record includes:
qc_id as the unique inspection identifier, batch_id to link the inspection to a production batch, specification_id to link it to the specification being tested, qc_date, qc_type, inspector_id, result, defect_count…

**Sources retrieved (12):** `Quality Control inspections→QUALITY_CONTROL`, `BOM→PRODUCT`, `Material Transfers`, `parent_chunk_data_dictionary.md_3`, `BATCH→PRODUCT`, `Material Transfers→SHIPMENT`, `parent_chunk_business_glossary.md_2`, `Quality Control inspections`

**Context previews (first 3):**

1. _Business concept 'Quality Control inspections' is implemented by physical table QUALITY_CONTROL (columns: qc_id, batch_id, specification_id, qc_date, qc_type, inspector_id, result, defect_count, notes…_

2. _Relationship: BOM references PRODUCT via foreign key COMPONENT_PRODUCT_ID -> PRODUCT.PRODUCT_ID.…_

3. _Material Transfers: The DDL explicitly labels the table as material transfers and its columns model directional movements with shipment_type plus source/destination references to warehouse, supplier, …_

---

### ✅ QA-010 — What do specification records define?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.7558 | **Gate:** `proceed`

**Expected answer:**
> Specifications define technical requirements with a unique identifier (specification_id), descriptive name (specification_name), version number, effective date, specification type (DIMENSIONAL, MATERIAL, PERFORMANCE), critical parameter being measured (critical_parameter), acceptable minimum value (…

**System answer:**
> Specification records define the technical requirements, standards, and acceptance criteria for materials and products. They include version numbers, effective dates, specification types (DIMENSIONAL, MATERIAL, PERFORMANCE), the critical parameter being tested, acceptable minimum and maximum values, and the unit of measure. These records are used to ensure manufactured products meet requirements a…

**Sources retrieved (12):** `version numbers, effective dates, specification types (dimensional, material, performance)→SPECIFICATION`, `parent_chunk_data_dictionary.md_7`, `Quality Control inspections→QUALITY_CONTROL`, `a parent product, a component product (which can be either a component or sub-assembly), the required quantity, unit of measure, and hierarchical level in the product structure→COMPONENT`, `parent_chunk_data_dictionary.md_3`, `parent_chunk_business_glossary.md_2`, `parent_chunk_business_glossary.md_0`, `parent_chunk_business_glossary.md_1`

**Context previews (first 3):**

1. _Business concept 'version numbers, effective dates, specification types (dimensional, material, performance)' is implemented by physical table SPECIFICATION (columns: specification_id, specification_n…_

2. _## specification  Defines technical requirements and acceptance criteria for materials and products.  | Column | Data Type | Constraints | Description | |--------|-----------|-------------|-----------…_

3. _Business concept 'Quality Control inspections' is implemented by physical table QUALITY_CONTROL (columns: qc_id, batch_id, specification_id, qc_date, qc_type, inspector_id, result, defect_count, notes…_

---

### ✅ QA-011 — How can I find which suppliers provide specific components?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.1935 | **Gate:** `proceed_with_warning`

**Expected answer:**
> Query the component_supplier table which links components to their approved suppliers. This table contains the component identifier (component_id), supplier identifier (supplier_id), preferred supplier flag (is_preferred), lead time in days (lead_time_days), and unit price (unit_price). Join with th…

**System answer:**
> Use the `COMPONENT_SUPPLIER` table. In the context, this is explicitly the many-to-many junction that represents approved supplier relationships for components.

To find which suppliers provide a specific component, follow this schema path:
`COMPONENT` → `COMPONENT_SUPPLIER` → `SUPPLIER`

The joins are:
`COMPONENT_SUPPLIER.component_id = COMPONENT.component_id`
and
`COMPONENT_SUPPLIER.supplier_id …

**Sources retrieved (12):** `Approved Supplier Link→COMPONENT_SUPPLIER`, `parent_chunk_data_dictionary.md_5`, `parent_chunk_data_dictionary.md_4`, `parent_chunk_data_dictionary.md_3`, `parent_chunk_data_dictionary.md_8`, `Approved Supplier Link`, `parent_chunk_business_glossary.md_0`, `parent_chunk_business_glossary.md_1`

**Context previews (first 3):**

1. _Business concept 'Approved Supplier Link' — The table is explicitly a many-to-many junction between components and suppliers, with a unique component-supplier pair and attributes for preferred status,…_

2. _## warehouse  Stores physical storage location information for inventory management.  | Column | Data Type | Constraints | Description | |--------|-----------|-------------|-------------| | warehouse_…_

3. _## bom  Bill of Materials defining product composition and hierarchical structure. Supports recursive relationships for multi-level assemblies.  | Column | Data Type | Constraints | Description | |---…_

---

### ✅ QA-012 — How do I trace which components are needed to fulfill a work order?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.2334 | **Gate:** `proceed`

**Expected answer:**
> Start with the work_order table to get the product_id being manufactured. Join to the bom table using product_id as parent_product_id to find all direct components and sub-assemblies. For each component_product_id, if it is an ASSEMBLY type product, recursively query the bom table again to explode m…

**System answer:**
> To trace the components needed for a work order, start with `WORK_ORDER`. The key row is identified by `work_order_id`, and the product being manufactured is in `WORK_ORDER.product_id`. Join `WORK_ORDER.product_id` to `PRODUCT.product_id` to identify the finished good or assembly the work order is producing.

From there, the retrieved context shows two relevant structure mechanisms. First, `PRODUC…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_5`, `Work Order→WORK_ORDER`, `parent_chunk_data_dictionary.md_6`, `Batches for traceability and inventory management→INVENTORY`, `parent_chunk_data_dictionary.md_3`, `parent_chunk_data_dictionary.md_8`, `a parent product, a component product (which can be either a component or sub-assembly), the required quantity, unit of measure, and hierarchical level in the product structure→COMPONENT`, `parent_chunk_data_dictionary.md_7`

**Context previews (first 3):**

1. _## warehouse  Stores physical storage location information for inventory management.  | Column | Data Type | Constraints | Description | |--------|-----------|-------------|-------------| | warehouse_…_

2. _Business concept 'Work Order' — The table is explicitly labeled as WORK_ORDER and contains core work order attributes such as product_id, quantity ordered/completed, status, priority, planned dates, a…_

3. _## work_order  Represents production jobs for manufacturing products with hierarchical work order support.  | Column | Data Type | Constraints | Description | |--------|-----------|-------------|-----…_

---

### ✅ QA-013 — How can I identify which warehouses have available inventory for specific components?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.8215 | **Gate:** `proceed`

**Expected answer:**
> Query the inventory table filtered by component_id, joining with the warehouse table to get warehouse names and locations. Calculate available quantity as quantity_on_hand minus quantity_reserved. Filter for records where available quantity is greater than zero. Results show warehouse names, locatio…

**System answer:**
> Use the `inventory` table as the starting point and join it to `warehouse` through `inventory.warehouse_id = warehouse.warehouse_id`.

The relevant path is:
`inventory.component_id` → target component, and `inventory.warehouse_id` → `warehouse.warehouse_id` for the warehouse details.

From the context, `inventory` tracks stock levels of components and products at specific warehouse locations, and …

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_5`, `INVENTORY→WAREHOUSE`, `Batches for traceability and inventory management→INVENTORY`, `INVENTORY→COMPONENT`, `parent_chunk_data_dictionary.md_3`, `parent_chunk_data_dictionary.md_8`, `parent_chunk_data_dictionary.md_6`, `Batches for traceability and inventory management→BATCH`

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
> Use the `SHIPMENT` table and filter it by supplier and delivery status.

From the schema, `shipment.supplier_id` is a foreign key to `supplier.supplier_id`, and the `chk_supplier_inbound` constraint ensures `supplier_id` is only populated for `INBOUND` shipments. So, to find shipments that delivered materials from a specific supplier, the schema supports this logic:

- `shipment.supplier_id = <spe…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_8`, `Material Transfers`, `SHIPMENT→SUPPLIER`, `Material Transfers→SHIPMENT`, `parent_chunk_data_dictionary.md_5`, `parent_chunk_data_dictionary.md_7`, `parent_chunk_data_dictionary.md_3`, `parent_chunk_data_dictionary.md_4`

**Context previews (first 3):**

1. _## shipment  Tracks material transfers between warehouses, suppliers, and customers.  | Column | Data Type | Constraints | Description | |--------|-----------|-------------|-------------| | shipment_i…_

2. _Material Transfers: The DDL explicitly labels the table as material transfers and its columns model directional movements with shipment_type plus source/destination references to warehouse, supplier, …_

3. _Relationship: SHIPMENT references SUPPLIER via foreign key SUPPLIER_ID -> SUPPLIER.SUPPLIER_ID.…_

---

### ✅ QA-015 — How can I determine which quality control inspections were performed on a specific production batch?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.9779 | **Gate:** `proceed`

**Expected answer:**
> Query the quality_control table filtered by batch_id. Join with the specification table to get requirement details (specification_name, spec_type, acceptable ranges). Include qc_date, qc_type (INCOMING, IN_PROCESS, FINAL), result (PASS, FAIL, CONDITIONAL), and defect_count. This shows the complete i…

**System answer:**
> Use the `QUALITY_CONTROL` table, which implements the business concept “Quality Control inspections.” QC inspections are linked directly to production batches through `QUALITY_CONTROL.batch_id`.

To determine which inspections were performed on a specific batch, filter `QUALITY_CONTROL` for the target `batch_id`. The relevant inspection details available in that table are `qc_id`, `batch_id`, `spe…

**Sources retrieved (12):** `Quality Control inspections→QUALITY_CONTROL`, `parent_chunk_data_dictionary.md_7`, `Batches for traceability and inventory management→BATCH`, `BATCH→PRODUCT`, `parent_chunk_data_dictionary.md_5`, `parent_chunk_data_dictionary.md_6`, `parent_chunk_data_dictionary.md_3`, `BATCH→WAREHOUSE`

**Context previews (first 3):**

1. _Business concept 'Quality Control inspections' is implemented by physical table QUALITY_CONTROL (columns: qc_id, batch_id, specification_id, qc_date, qc_type, inspector_id, result, defect_count, notes…_

2. _## specification  Defines technical requirements and acceptance criteria for materials and products.  | Column | Data Type | Constraints | Description | |--------|-----------|-------------|-----------…_

3. _Business concept 'Batches for traceability and inventory management' is implemented by physical table BATCH (columns: batch_id, product_id, production_date, quantity_produced, warehouse_id, expiry_dat…_

---

### ✅ QA-016 — How do I track which work orders are in progress at a specific warehouse?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.7311 | **Gate:** `proceed`

**Expected answer:**
> Query the work_order table filtering by warehouse_id and status = 'IN_PROGRESS'. Join with the product table to get product names and types. Include quantity_ordered, quantity_completed, priority, planned_end_date, and calculate progress percentage as (quantity_completed / quantity_ordered * 100). O…

**System answer:**
> Use the WORK_ORDER table, because it contains both the work order status and the warehouse reference. To find work orders in progress at a specific warehouse, filter WORK_ORDER where status = 'IN_PROGRESS' and warehouse_id equals the target warehouse.

If you need warehouse details such as name or location, join WORK_ORDER to WAREHOUSE on WORK_ORDER.warehouse_id = WAREHOUSE.warehouse_id. That rela…

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
> Use the `INVENTORY` table as the starting point. The retrieved context defines `Inventory` as tracking stock levels for components and products in specific warehouses, including `quantity_on_hand`, `quantity_reserved`, `reorder_threshold`, and `last_restock_date`. It also states that reorder thresholds are used “to trigger procurement.”

To find components that may need reordering at the schema le…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_5`, `Batches for traceability and inventory management→INVENTORY`, `INVENTORY→COMPONENT`, `parent_chunk_data_dictionary.md_3`, `parent_chunk_data_dictionary.md_7`, `parent_chunk_data_dictionary.md_4`, `a parent product, a component product (which can be either a component or sub-assembly), the required quantity, unit of measure, and hierarchical level in the product structure→COMPONENT`, `parent_chunk_data_dictionary.md_6`

**Context previews (first 3):**

1. _## warehouse  Stores physical storage location information for inventory management.  | Column | Data Type | Constraints | Description | |--------|-----------|-------------|-------------| | warehouse_…_

2. _Business concept 'Batches for traceability and inventory management' is implemented by physical table INVENTORY (columns: inventory_id, warehouse_id, component_id, product_id, quantity_on_hand, quanti…_

3. _Relationship: INVENTORY references COMPONENT via foreign key COMPONENT_ID -> COMPONENT.COMPONENT_ID.…_

---

### ✅ QA-018 — How do I determine the manufacturing route for a specific product?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.7691 | **Gate:** `proceed`

**Expected answer:**
> Query the route table filtering by product_id, ordered by sequence_number ascending. For each operation, retrieve operation_name, work_center, cycle_time_minutes, and setup_time_minutes. Join with the product table to get product details. The sequence of operations shows the complete manufacturing w…

**System answer:**
> To determine the manufacturing route for a specific product, use the `ROUTE` table at the step level. The context describes `ROUTE` as implementing the business concept “Route Steps,” where each row is an individual routing step for a product, identified by `product_id` and ordered by `sequence_number`. For the target product, filter `ROUTE.product_id` to that product’s ID and read the resulting r…

**Sources retrieved (12):** `Route Steps→ROUTE`, `parent_chunk_data_dictionary.md_6`, `ROUTE→PRODUCT`, `parent_chunk_data_dictionary.md_3`, `parent_chunk_data_dictionary.md_7`, `parent_chunk_data_dictionary.md_8`, `parent_chunk_data_dictionary.md_4`, `Work Order→WORK_ORDER`

**Context previews (first 3):**

1. _Business concept 'Route Steps' — The table is clearly step-granular: `sequence_number`, `operation_name`, `work_center`, `cycle_time_minutes`, and `setup_time_minutes` describe individual routing step…_

2. _## work_order  Represents production jobs for manufacturing products with hierarchical work order support.  | Column | Data Type | Constraints | Description | |--------|-----------|-------------|-----…_

3. _Relationship: ROUTE references PRODUCT via foreign key PRODUCT_ID -> PRODUCT.PRODUCT_ID.…_

---

### ✅ QA-019 — How can I find which batches are stored at a specific warehouse and their QC status?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.7533 | **Gate:** `proceed`

**Expected answer:**
> Query the batch table filtering by warehouse_id. Join with the product table to get product names and types. Include production_date, quantity_produced, expiry_date, and qc_status (PENDING, PASSED, FAILED, QUARANTINED). Filter by qc_status to isolate batches requiring quality attention or ready for …

**System answer:**
> Use the `BATCH` table, because the business concept “Batches for traceability and inventory management” is implemented by `BATCH`, and it contains both the storage location and QC status fields you need: `batch_id`, `product_id`, `production_date`, `quantity_produced`, `warehouse_id`, `expiry_date`, and `qc_status`.

To find batches stored at a specific warehouse, filter `BATCH.warehouse_id` for t…

**Sources retrieved (12):** `Batches for traceability and inventory management→BATCH`, `parent_chunk_data_dictionary.md_5`, `BATCH→WAREHOUSE`, `Quality Control inspections→QUALITY_CONTROL`, `parent_chunk_data_dictionary.md_6`, `Batches for traceability and inventory management→INVENTORY`, `parent_chunk_data_dictionary.md_8`, `Work Order→WORK_ORDER`

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
> To identify which specifications apply to specific components, use the `COMPONENT` table’s `specification_id` and link it to `SPECIFICATION.specification_id`.

From the context, the physical table `COMPONENT` includes these columns: `component_id`, `component_name`, `component_category`, `unit_of_measure`, `standard_cost`, and `specification_id`. The `SPECIFICATION` table defines the specification…

**Sources retrieved (12):** `a parent product, a component product (which can be either a component or sub-assembly), the required quantity, unit of measure, and hierarchical level in the product structure→COMPONENT`, `parent_chunk_data_dictionary.md_5`, `parent_chunk_data_dictionary.md_7`, `parent_chunk_data_dictionary.md_3`, `Approved Supplier Link→COMPONENT_SUPPLIER`, `parent_chunk_data_dictionary.md_4`, `version numbers, effective dates, specification types (dimensional, material, performance)→SPECIFICATION`, `parent_chunk_business_glossary.md_0`

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
> To perform a complete BOM explosion for a finished product, use the `product` and `bom` tables together and traverse the hierarchy recursively.

Start with the target row in `product`, using `product.product_id`. If you want specifically a finished product, the `product_type` classification includes `FINISHED_GOOD`, `ASSEMBLY`, and `COMPONENT`, so the starting product can be identified as a finish…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_4`, `parent_chunk_data_dictionary.md_3`, `BOM entry→BOM`, `BOM→PRODUCT`, `a parent product, a component product (which can be either a component or sub-assembly), the required quantity, unit of measure, and hierarchical level in the product structure→COMPONENT`, `parent_chunk_data_dictionary.md_5`, `parent_chunk_data_dictionary.md_7`, `parent_chunk_data_dictionary.md_6`

**Context previews (first 3):**

1. _## bom  Bill of Materials defining product composition and hierarchical structure. Supports recursive relationships for multi-level assemblies.  | Column | Data Type | Constraints | Description | |---…_

2. _# Manufacturing Data Dictionary  This data dictionary documents the database schema for the manufacturing supply chain system. It includes all tables, columns, data types, constraints, and relationshi…_

3. _Business concept 'BOM entry' is implemented by physical table BOM (columns: bom_id, parent_product_id, component_product_id, quantity, unit_of_measure, bom_level, is_optional).…_

---

### ✅ QA-022 — How do I calculate the total material cost for a product including all sub-assemblies?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.2332 | **Gate:** `proceed`

**Expected answer:**
> Perform a recursive BOM explosion to find all leaf-level components. For each leaf component, join with the component table to get standard_cost. Multiply standard_cost by the accumulated quantity from the BOM traversal. Sum all component costs to get total material cost. This calculation must trave…

**System answer:**
> The retrieved context supports tracing a product’s full multi-level structure, but it does not define an exact cost rollup formula for “total material cost.”

What is known from the context is this: the `product` table stores each manufactured item, including finished goods, assemblies, and components, with `product.product_id`, `product.product_type`, `product.base_cost`, and the self-referential…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_3`, `a parent product, a component product (which can be either a component or sub-assembly), the required quantity, unit of measure, and hierarchical level in the product structure→COMPONENT`, `parent_chunk_data_dictionary.md_4`, `parent_chunk_data_dictionary.md_7`, `parent_chunk_data_dictionary.md_8`, `parent_chunk_data_dictionary.md_6`, `parent_chunk_data_dictionary.md_5`, `(product_id, sequence_number)→PRODUCT`

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
> Use the `bom` table as the traversal table, because `BOM` is the business concept for a BOM entry and it stores both `parent_product_id` and `component_product_id`. Both columns reference `product(product_id)`, and the schema explicitly says this supports recursive, multi-level assemblies.

The lookup path is:

Start with `bom.component_product_id = <the specific component's product_id>`.  
That g…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_4`, `parent_chunk_data_dictionary.md_3`, `a parent product, a component product (which can be either a component or sub-assembly), the required quantity, unit of measure, and hierarchical level in the product structure→COMPONENT`, `BOM entry→BOM`, `BOM→PRODUCT`, `PRODUCT→PRODUCT`, `parent_chunk_data_dictionary.md_6`, `parent_chunk_data_dictionary.md_8`

**Context previews (first 3):**

1. _## bom  Bill of Materials defining product composition and hierarchical structure. Supports recursive relationships for multi-level assemblies.  | Column | Data Type | Constraints | Description | |---…_

2. _# Manufacturing Data Dictionary  This data dictionary documents the database schema for the manufacturing supply chain system. It includes all tables, columns, data types, constraints, and relationshi…_

3. _Business concept 'a parent product, a component product (which can be either a component or sub-assembly), the required quantity, unit of measure, and hierarchical level in the product structure' is i…_

---

### ✅ QA-024 — How do I identify work orders that require a specific component, considering nested sub-assemblies?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.3651 | **Gate:** `proceed`

**Expected answer:**
> First, perform reverse BOM traversal to find all parent products that contain the target component at any level. Then query the work_order table where product_id is in the set of parent products found. This includes work orders for finished goods that contain the component indirectly through sub-ass…

**System answer:**
> From the retrieved context, the schema-level relationships are:

WORK_ORDER.product_id identifies the product being manufactured, and it is a foreign key to PRODUCT.product_id. BOM defines product composition, where BOM.parent_product_id is the product being built and BOM.component_product_id is the product that goes into it; both columns reference PRODUCT.product_id. BOM also includes quantity, u…

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
> Use the `bom` table, because it explicitly stores the hierarchy depth in `bom.bom_level`, which is described as the “depth in product hierarchy” and is included for “performance optimization.”

For a specific product, identify the product in `product.product_id`, then look at all `bom` rows where `bom.parent_product_id = product.product_id`. The maximum BOM depth for that product is the highest va…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_4`, `parent_chunk_data_dictionary.md_3`, `BOM entry→BOM`, `BOM→PRODUCT`, `parent_chunk_data_dictionary.md_7`, `parent_chunk_data_dictionary.md_5`, `parent_chunk_data_dictionary.md_6`, `a parent product, a component product (which can be either a component or sub-assembly), the required quantity, unit of measure, and hierarchical level in the product structure→COMPONENT`

**Context previews (first 3):**

1. _## bom  Bill of Materials defining product composition and hierarchical structure. Supports recursive relationships for multi-level assemblies.  | Column | Data Type | Constraints | Description | |---…_

2. _# Manufacturing Data Dictionary  This data dictionary documents the database schema for the manufacturing supply chain system. It includes all tables, columns, data types, constraints, and relationshi…_

3. _Business concept 'BOM entry' is implemented by physical table BOM (columns: bom_id, parent_product_id, component_product_id, quantity, unit_of_measure, bom_level, is_optional).…_

---

### ✅ QA-026 — How do I find all products that have a specific product as a sub-assembly at any level?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.2948 | **Gate:** `proceed`

**Expected answer:**
> Perform a recursive search starting with the target product_id as the initial component_product_id in the bom table. For each parent_product_id found, check if that parent appears as a component in other bom entries. Continue recursively until reaching products that are not used as components elsewh…

**System answer:**
> Use the `bom` table as the primary hierarchy, because it is the Bill of Materials table that stores `parent_product_id` and `component_product_id`, and it explicitly “supports recursive relationships for multi-level assemblies.”

At the schema level, the trace is:

Start with the target product in `bom.component_product_id`. Any row where `component_product_id = <specific product_id>` gives you an…

**Sources retrieved (12):** `a parent product, a component product (which can be either a component or sub-assembly), the required quantity, unit of measure, and hierarchical level in the product structure→COMPONENT`, `parent_chunk_data_dictionary.md_3`, `parent_chunk_data_dictionary.md_4`, `parent_chunk_data_dictionary.md_5`, `parent_chunk_data_dictionary.md_7`, `Route Steps→ROUTE`, `parent_chunk_data_dictionary.md_6`, `BOM entry→BOM`

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
> From the retrieved context, I can only answer this partially.

What is known is that `product.lead_time_days` stores the procurement or production lead time for each product, and the product structure can be traversed recursively through the `bom` table. The relevant schema path is: start with the target row in `product`, join `bom.parent_product_id` to that product’s `product_id`, then join `bom.…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_3`, `(product_id, sequence_number)→PRODUCT`, `Approved Supplier Link→COMPONENT_SUPPLIER`, `a parent product, a component product (which can be either a component or sub-assembly), the required quantity, unit of measure, and hierarchical level in the product structure→COMPONENT`, `parent_chunk_data_dictionary.md_4`, `Route Steps→ROUTE`, `parent_chunk_data_dictionary.md_7`, `parent_chunk_data_dictionary.md_6`

**Context previews (first 3):**

1. _# Manufacturing Data Dictionary  This data dictionary documents the database schema for the manufacturing supply chain system. It includes all tables, columns, data types, constraints, and relationshi…_

2. _Business concept '(product_id, sequence_number)' is implemented by physical table PRODUCT (columns: product_id, product_name, product_type, parent_product_id, base_cost, lead_time_days, is_active).…_

3. _Business concept 'Approved Supplier Link' — The table is explicitly a many-to-many junction between components and suppliers, with a unique component-supplier pair and attributes for preferred status,…_

---

### ✅ QA-028 — How do I generate a complete indented BOM report showing the hierarchical structure?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.4180 | **Gate:** `proceed`

**Expected answer:**
> Use a recursive query on the bom table that tracks the current depth level. Start with the top-level product (parent_product_id where product has no parent_product_id). At each level, output component details indented by depth level. Include product_name, quantity, and unit_of_measure. Recursively p…

**System answer:**
> To generate a complete indented BOM report, use the `bom` table as the hierarchy driver and the `product` table to resolve readable product details.

The core join pattern is: `bom.parent_product_id -> product.product_id` to identify the assembly being built, and `bom.component_product_id -> product.product_id` to identify the component or sub-assembly used in it. Because both BOM columns referenc…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_4`, `parent_chunk_data_dictionary.md_3`, `a parent product, a component product (which can be either a component or sub-assembly), the required quantity, unit of measure, and hierarchical level in the product structure→COMPONENT`, `parent_chunk_data_dictionary.md_6`, `parent_chunk_data_dictionary.md_8`, `BOM entry→BOM`, `Work Order→WORK_ORDER`, `BOM→PRODUCT`

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
> Use the `bom` table as the source, because a BOM entry is the parent-product / component-product relationship and is implemented by `BOM(bom_id, parent_product_id, component_product_id, quantity, unit_of_measure, bom_level, is_optional)`.

To find which items appear most frequently across product BOMs, count how many `bom` rows use the same `component_product_id`. The key path is `bom.component_pr…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_4`, `parent_chunk_data_dictionary.md_3`, `BOM entry→BOM`, `BOM→PRODUCT`, `parent_chunk_data_dictionary.md_5`, `a parent product, a component product (which can be either a component or sub-assembly), the required quantity, unit of measure, and hierarchical level in the product structure→COMPONENT`, `parent_chunk_data_dictionary.md_7`, `Batches for traceability and inventory management→INVENTORY`

**Context previews (first 3):**

1. _## bom  Bill of Materials defining product composition and hierarchical structure. Supports recursive relationships for multi-level assemblies.  | Column | Data Type | Constraints | Description | |---…_

2. _# Manufacturing Data Dictionary  This data dictionary documents the database schema for the manufacturing supply chain system. It includes all tables, columns, data types, constraints, and relationshi…_

3. _Business concept 'BOM entry' is implemented by physical table BOM (columns: bom_id, parent_product_id, component_product_id, quantity, unit_of_measure, bom_level, is_optional).…_

---

### ✅ QA-030 — How do I detect circular references in the BOM structure to prevent infinite loops?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.1295 | **Gate:** `proceed_with_warning`

**Expected answer:**
> Use a recursive query with a cycle detection check. Track the path of visited product_ids at each recursion level. If a product_id appears twice in the same path, a circular reference exists. Alternatively, check if any bom record has parent_product_id = component_product_id (direct self-reference),…

**System answer:**
> Use the `bom` table as the traversal source. The recursive path is `bom.parent_product_id -> bom.component_product_id`, then from that component into the next BOM row by joining `current.component_product_id = next.parent_product_id`. A circular reference exists if that recursive walk reaches a `product_id` that has already appeared earlier in the same path, especially if a descendant `component_p…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_4`, `parent_chunk_data_dictionary.md_3`, `BOM→PRODUCT`, `BOM entry→BOM`, `parent_chunk_data_dictionary.md_8`, `parent_chunk_data_dictionary.md_7`, `parent_chunk_data_dictionary.md_6`, `parent_chunk_business_glossary.md_0`

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
> From the available schema metadata, you can determine most of the supplier chain at the structure level by combining the product hierarchy in `PRODUCT` and `BOM` with supplier relationships in `COMPONENT_SUPPLIER` and `SUPPLIER`.

The trace starts with the finished product in `PRODUCT`, where `product_type` can be `FINISHED_GOOD`, `ASSEMBLY`, or `COMPONENT`. To expand everything that makes up that…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_3`, `a parent product, a component product (which can be either a component or sub-assembly), the required quantity, unit of measure, and hierarchical level in the product structure→COMPONENT`, `parent_chunk_data_dictionary.md_4`, `parent_chunk_data_dictionary.md_8`, `parent_chunk_data_dictionary.md_6`, `Approved Supplier Link→COMPONENT_SUPPLIER`, `parent_chunk_data_dictionary.md_7`, `Route Steps→ROUTE`

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
> From the retrieved context, the schema-level way to check this is to compare the work order’s required product quantity from `work_order` to the total available inventory for that same product in `inventory` across all warehouses.

Use `work_order.work_order_id` to find the row in `work_order`, then take:
`work_order.product_id` — the product being manufactured, and
`work_order.quantity_ordered` a…

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

Failed quality control inspections are stored in the physical table `QUALITY_CONTROL`, which implements the business concept “Quality Control inspections.” The relevant columns are `qc_id`, `batch_id`, `specification_id`, `qc_date`, `qc_type`, `inspector_id`, `result`, `defect_count`, and `notes`. To find failures…

**Sources retrieved (12):** `Quality Control inspections→QUALITY_CONTROL`, `parent_chunk_data_dictionary.md_5`, `parent_chunk_data_dictionary.md_3`, `Approved Supplier Link→COMPONENT_SUPPLIER`, `parent_chunk_data_dictionary.md_4`, `COMPONENT_SUPPLIER→SUPPLIER`, `parent_chunk_data_dictionary.md_8`, `parent_chunk_business_glossary.md_2`

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
> From the retrieved context, you can identify the relevant work orders and their route-step time fields, but the context does not define an official formula for “total manufacturing time.”

Schema-level tracing works like this: start with `WORK_ORDER.work_order_id`, then follow the self-referencing `WORK_ORDER.parent_work_order` relationship to collect all child work orders in the hierarchy, becaus…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_6`, `parent_chunk_data_dictionary.md_3`, `Work Order→WORK_ORDER`, `Route Steps→ROUTE`, `a parent product, a component product (which can be either a component or sub-assembly), the required quantity, unit of measure, and hierarchical level in the product structure→COMPONENT`, `parent_chunk_data_dictionary.md_7`, `parent_chunk_data_dictionary.md_5`, `parent_chunk_business_glossary.md_0`

**Context previews (first 3):**

1. _## work_order  Represents production jobs for manufacturing products with hierarchical work order support.  | Column | Data Type | Constraints | Description | |--------|-----------|-------------|-----…_

2. _# Manufacturing Data Dictionary  This data dictionary documents the database schema for the manufacturing supply chain system. It includes all tables, columns, data types, constraints, and relationshi…_

3. _Business concept 'Work Order' — The table is explicitly labeled as WORK_ORDER and contains core work order attributes such as product_id, quantity ordered/completed, status, priority, planned dates, a…_

---

### ✅ QA-035 — How can I identify which shipments are overdue and their impact on work orders?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0719 | **Gate:** `proceed_with_warning`

**Expected answer:**
> Query the shipment table filtering for status = 'SHIPPED' where actual_arrival is NULL and estimated_arrival is in the past (overdue). Join with the component_supplier table via supplier_id and component_id to identify which components are delayed. Perform reverse BOM lookup to find which parent pro…

**System answer:**
> From the retrieved schema, you can only determine this at a schema level; the knowledge graph describes tables, columns, and relationships, not actual shipment or work order records.

For shipments, the relevant table is `SHIPMENT`. It provides `shipment_id`, `shipment_type`, `warehouse_id`, `supplier_id`, `customer_id`, `ship_date`, `estimated_arrival`, `actual_arrival`, and `status`. The documen…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_5`, `parent_chunk_data_dictionary.md_8`, `parent_chunk_data_dictionary.md_6`, `Work Order→WORK_ORDER`, `WORK_ORDER→PRODUCT`, `WORK_ORDER→WAREHOUSE`, `SHIPMENT→WAREHOUSE`, `parent_chunk_data_dictionary.md_3`

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
> Use the `BATCH` table for the expiry check and the `BOM` table for the “contains components” part.

The documented expiry path is straightforward: `BATCH` has `batch_id`, `product_id`, `production_date`, `quantity_produced`, `warehouse_id`, and `expiry_date`. To find expired batches, compare `BATCH.expiry_date` to the date you are evaluating against. To find batches “approaching expiry,” the schem…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_5`, `Batches for traceability and inventory management→BATCH`, `parent_chunk_data_dictionary.md_7`, `Batches for traceability and inventory management→INVENTORY`, `parent_chunk_data_dictionary.md_3`, `Approved Supplier Link→COMPONENT_SUPPLIER`, `parent_chunk_data_dictionary.md_8`, `parent_chunk_data_dictionary.md_4`

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
> From the retrieved metadata, the schema-level way to build this is to start from `WORK_ORDER`, then explode the required structure through `BOM`, and then use `PRODUCT.lead_time_days` to back-calculate when the needed component should be available.

`WORK_ORDER` gives you the production schedule inputs: `work_order_id`, `product_id`, `quantity_ordered`, `quantity_completed`, `status`, `priority`, …

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_6`, `parent_chunk_data_dictionary.md_7`, `Work Order→WORK_ORDER`, `parent_chunk_data_dictionary.md_5`, `parent_chunk_data_dictionary.md_4`, `parent_chunk_data_dictionary.md_3`, `Approved Supplier Link→COMPONENT_SUPPLIER`, `WORK_ORDER→WORK_ORDER`

**Context previews (first 3):**

1. _## work_order  Represents production jobs for manufacturing products with hierarchical work order support.  | Column | Data Type | Constraints | Description | |--------|-----------|-------------|-----…_

2. _## specification  Defines technical requirements and acceptance criteria for materials and products.  | Column | Data Type | Constraints | Description | |--------|-----------|-------------|-----------…_

3. _Business concept 'Work Order' — The table is explicitly labeled as WORK_ORDER and contains core work order attributes such as product_id, quantity ordered/completed, status, priority, planned dates, a…_

---

### ✅ QA-038 — How do I trace the complete genealogy of a component from supplier through batch to finished goods?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0748 | **Gate:** `proceed_with_warning`

**Expected answer:**
> Start with a shipment from the supplier (shipment table with supplier_id and shipment_type = 'INBOUND'). Track to inventory updates via component_id and warehouse_id. Identify batches that consumed the component via reverse BOM lookup (batch.product_id → bom hierarchy → component_id). Query quality_…

**System answer:**
> The retrieved context does not contain enough information to trace a complete end-to-end genealogy from a specific supplier-sourced component through production batches into specific finished goods. What it does provide is the schema-level structure for part of that path, and the gaps are important.

From the context, the part that is known is:

A supplier can be linked to a component through `COM…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_3`, `parent_chunk_data_dictionary.md_7`, `parent_chunk_data_dictionary.md_5`, `parent_chunk_data_dictionary.md_8`, `Batches for traceability and inventory management→INVENTORY`, `parent_chunk_data_dictionary.md_4`, `Approved Supplier Link→COMPONENT_SUPPLIER`, `Batches for traceability and inventory management→BATCH`

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
> The retrieved context does not define what makes a component “critical,” so I cannot give a schema-supported rule for criticality.

What the context does support is this schema-level approach:

First, use `bom` to find components that are used in more than one product. In `bom`, `parent_product_id` is the product being built and `component_product_id` is the product used as a component. Because `b…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_4`, `Approved Supplier Link→COMPONENT_SUPPLIER`, `parent_chunk_data_dictionary.md_3`, `Preferred supplier for this component→SUPPLIER`, `parent_chunk_data_dictionary.md_5`, `parent_chunk_data_dictionary.md_8`, `parent_chunk_data_dictionary.md_7`, `parent_chunk_business_glossary.md_0`

**Context previews (first 3):**

1. _## bom  Bill of Materials defining product composition and hierarchical structure. Supports recursive relationships for multi-level assemblies.  | Column | Data Type | Constraints | Description | |---…_

2. _Business concept 'Approved Supplier Link' — The table is explicitly a many-to-many junction between components and suppliers, with a unique component-supplier pair and attributes for preferred status,…_

3. _# Manufacturing Data Dictionary  This data dictionary documents the database schema for the manufacturing supply chain system. It includes all tables, columns, data types, constraints, and relationshi…_

---

### ✅ QA-040 — How do I calculate the total landed cost for a product including component costs, supplier lead times, and manufacturing operations?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.1922 | **Gate:** `proceed_with_warning`

**Expected answer:**
> Perform recursive BOM explosion to get all leaf components. For each component, query component_supplier to get unit_price from primary supplier. Multiply by accumulated BOM quantity for material cost. Add shipping costs (estimated from shipment history). Query route table for the product to get all…

**System answer:**
> From the retrieved context alone, I cannot give a complete landed-cost formula for a product. The context provides some relevant schema elements, but it does not provide all of the relationships and cost attributes needed to calculate “total landed cost,” especially for component quantity rollups and manufacturing operations.

What is supported by the context is this: the `product` table contains …

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_3`, `Approved Supplier Link→COMPONENT_SUPPLIER`, `(product_id, sequence_number)→PRODUCT`, `a parent product, a component product (which can be either a component or sub-assembly), the required quantity, unit of measure, and hierarchical level in the product structure→COMPONENT`, `parent_chunk_data_dictionary.md_6`, `parent_chunk_data_dictionary.md_7`, `parent_chunk_data_dictionary.md_5`, `parent_chunk_data_dictionary.md_8`

**Context previews (first 3):**

1. _# Manufacturing Data Dictionary  This data dictionary documents the database schema for the manufacturing supply chain system. It includes all tables, columns, data types, constraints, and relationshi…_

2. _Business concept 'Approved Supplier Link' — The table is explicitly a many-to-many junction between components and suppliers, with a unique component-supplier pair and attributes for preferred status,…_

3. _Business concept '(product_id, sequence_number)' is implemented by physical table PRODUCT (columns: product_id, product_name, product_type, parent_product_id, base_cost, lead_time_days, is_active).…_

---

## Anomalies & Observations

No anomalies detected. All questions grounded with acceptable RAGAS scores.
