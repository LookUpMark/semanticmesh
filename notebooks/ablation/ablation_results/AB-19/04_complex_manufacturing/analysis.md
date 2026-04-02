# AB-19 — 04_complex_manufacturing — Run Analysis

**Timestamp:** 2026-03-31 03:49:17  
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
| Triplets extracted | 448 |
| Entities resolved | 130 |
| Tables parsed | 13 |
| Tables completed | 13 |

## Query Evaluation Summary

| Metric | Value |
|--------|-------|
| Questions | 40 |
| Grounded | **40/40 (100%)** |
| Avg GT Coverage | 100% |
| Avg Top Score | 0.4518 |
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
> Products are stored in the `PRODUCT` table. For each product, the system stores a unique `PRODUCT_ID`/`product_id` (VARCHAR(20), primary key), `PRODUCT_NAME`/`product_name` (required), `PRODUCT_TYPE`/`product_type` (required, default `FINISHED_GOOD`), `PARENT_PRODUCT_ID`/`parent_product_id` (a self-referencing foreign key to another product), `BASE_COST`/`base_cost` (required, default 0.00, nonneg…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_3`, `Work Order→WORK_ORDER`, `Warehouse Inventory Levels`, `parent_chunk_business_glossary.md_0`, `parent_chunk_business_glossary.md_1`, `Work Order`, `parent_chunk_business_glossary.md_2`, `Product→PRODUCT`

**Context previews (first 3):**

1. _# Manufacturing Data Dictionary  This data dictionary documents the database schema for the manufacturing supply chain system. It includes all tables, columns, data types, constraints, and relationshi…_

2. _Business concept 'Work Order' — The table stores production job records with a product reference, ordered and completed quantities, status, priority, planned dates, and an optional parent work order f…_

3. _Warehouse Inventory Levels: The table stores stock by warehouse with references to either a component or product, plus on-hand, reserved, reorder, and last restock fields. This aligns closely with the…_

---

### ✅ QA-002 — How are components defined in the manufacturing database?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.5910 | **Gate:** `proceed`

**Expected answer:**
> Components are defined with a unique identifier (component_id), descriptive name (component_name), category grouping (component_category), unit of measure (unit_of_measure), standard unit cost (standard_cost), and optional reference to technical specifications (specification_id). Components represen…

**System answer:**
> In the manufacturing database, “components” are defined in two closely related ways in the retrieved context.

At the business-concept level, a Component represents atomic raw materials or purchased parts that cannot be further broken down into simpler manufactured items. They are the building blocks used in manufacturing and are procured from external suppliers.

At the schema level, this concept…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_3`, `Bill of Materials Entry→BOM`, `parent_chunk_data_dictionary.md_4`, `parent_chunk_data_dictionary.md_5`, `parent_chunk_business_glossary.md_0`, `parent_chunk_business_glossary.md_1`, `Bill of Materials Entry`, `parent_chunk_business_glossary.md_2`

**Context previews (first 3):**

1. _# Manufacturing Data Dictionary  This data dictionary documents the database schema for the manufacturing supply chain system. It includes all tables, columns, data types, constraints, and relationshi…_

2. _Business concept 'Bill of Materials Entry' — The table stores parent_product_id, component_product_id, quantity, unit_of_measure, and bom_level, which exactly matches a BOM line item/entry defining pr…_

3. _## bom  Bill of Materials defining product composition and hierarchical structure. Supports recursive relationships for multi-level assemblies.  | Column | Data Type | Constraints | Description | |---…_

---

### ✅ QA-003 — What is the purpose of the Bill of Materials (BOM) table?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.9678 | **Gate:** `proceed`

**Expected answer:**
> The BOM table defines the hierarchical structure of products by specifying which components or sub-assemblies are required to manufacture each parent product. It records the unique BOM entry identifier (bom_id), parent product being built (parent_product_id), component or sub-assembly product (compo…

**System answer:**
> The BOM table represents Bill of Materials entries that define product composition and hierarchical structure. It stores each parent-to-component relationship as an individual BOM line item, using `parent_product_id` for the product being built and `component_product_id` for the product that goes into it, along with `quantity`, `unit_of_measure`, `bom_level`, and `is_optional`.

Its purpose is to …

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_4`, `Bill of Materials Entry→BOM`, `BOM→PRODUCT`, `Product→PRODUCT`, `parent_chunk_data_dictionary.md_3`, `source and destination locations`, `Supplier→SUPPLIER`, `Bill of Materials Entry`

**Context previews (first 3):**

1. _## bom  Bill of Materials defining product composition and hierarchical structure. Supports recursive relationships for multi-level assemblies.  | Column | Data Type | Constraints | Description | |---…_

2. _Business concept 'Bill of Materials Entry' — The table stores parent_product_id, component_product_id, quantity, unit_of_measure, and bom_level, which exactly matches a BOM line item/entry defining pr…_

3. _Relationship: BOM references PRODUCT via foreign key COMPONENT_PRODUCT_ID -> PRODUCT.PRODUCT_ID.…_

---

### ✅ QA-004 — What supplier information does the system maintain?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.7663 | **Gate:** `proceed`

**Expected answer:**
> Suppliers are tracked with a unique identifier (supplier_id), legal business name (supplier_name), primary contact email (contact_email), primary contact phone number (contact_phone), performance rating from 1.0 to 5.0 (rating), and preferred supplier status flag (is_preferred).

**System answer:**
> The system maintains supplier master data in the SUPPLIER table for the business concept of an external vendor/company supplying materials or goods. The stored core supplier information is: unique supplier identifier, supplier name, contact email, contact phone, performance rating, and preferred status. In physical terms, those columns are SUPPLIER_ID, SUPPLIER_NAME, CONTACT_EMAIL, CONTACT_PHONE, …

**Sources retrieved (12):** `Supplier→SUPPLIER`, `parent_chunk_data_dictionary.md_4`, `Component-Supplier Relationship`, `SHIPMENT→SUPPLIER`, `parent_chunk_data_dictionary.md_8`, `COMPONENT_SUPPLIER→SUPPLIER`, `Component-Supplier Relationship→COMPONENT_SUPPLIER`, `parent_chunk_data_dictionary.md_3`

**Context previews (first 3):**

1. _Business concept 'Supplier' — The table stores core supplier master data: unique supplier identifier, supplier name, contact details, performance rating, and preferred status. This aligns directly wit…_

2. _## bom  Bill of Materials defining product composition and hierarchical structure. Supports recursive relationships for multi-level assemblies.  | Column | Data Type | Constraints | Description | |---…_

3. _Component-Supplier Relationship: The table is explicitly described as a many-to-many component-supplier junction and contains foreign keys to both component and supplier, plus relationship attributes …_

---

### ✅ QA-005 — How are warehouses represented in the schema?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.3381 | **Gate:** `proceed`

**Expected answer:**
> Warehouses are defined with a unique identifier (warehouse_id), descriptive name (warehouse_name), full street address (address), city location (city), state or province (state), total storage capacity in cubic meters (capacity), and optional manager identifier (manager_id).

**System answer:**
> Warehouses are represented by the physical table `WAREHOUSE`, which is the warehouse master record for physical storage locations used in inventory management and the supply chain.

In the schema, `WAREHOUSE` has these columns: `WAREHOUSE_ID` as the primary key and unique warehouse identifier, `WAREHOUSE_NAME` for the warehouse name, `ADDRESS`, `CITY`, and `STATE` for geographic location informati…

**Sources retrieved (12):** `INVENTORY→WAREHOUSE`, `BATCH→WAREHOUSE`, `WORK_ORDER→WAREHOUSE`, `SHIPMENT→WAREHOUSE`, `parent_chunk_data_dictionary.md_6`, `Warehouse Inventory Levels`, `parent_chunk_data_dictionary.md_5`, `geographic location information→WAREHOUSE`

**Context previews (first 3):**

1. _Relationship: INVENTORY references WAREHOUSE via foreign key WAREHOUSE_ID -> WAREHOUSE.WAREHOUSE_ID.…_

2. _Relationship: BATCH references WAREHOUSE via foreign key WAREHOUSE_ID -> WAREHOUSE.WAREHOUSE_ID.…_

3. _Relationship: WORK_ORDER references WAREHOUSE via foreign key WAREHOUSE_ID -> WAREHOUSE.WAREHOUSE_ID.…_

---

### ✅ QA-006 — What does the inventory table track?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.6318 | **Gate:** `proceed`

**Expected answer:**
> The inventory table tracks real-time stock levels including a unique record identifier (inventory_id), warehouse location (warehouse_id), component identifier for materials (component_id) or product identifier for finished goods (product_id), current physical stock quantity (quantity_on_hand), quant…

**System answer:**
> The `INVENTORY` table tracks stock levels of components and products at specific warehouse locations. From the context, it represents the business concept of “Warehouse Inventory Levels” and stores actual inventory by warehouse, with references to either a component or a product, but not both in the same record.

Specifically, it tracks:
the warehouse (`WAREHOUSE_ID`),
the item being stocked as ei…

**Sources retrieved (12):** `Warehouse Inventory Levels`, `Warehouse Inventory Levels→INVENTORY`, `INVENTORY→PRODUCT`, `INVENTORY→WAREHOUSE`, `INVENTORY→COMPONENT`, `parent_chunk_data_dictionary.md_5`, `Production Batch→BATCH`, `parent_chunk_data_dictionary.md_7`

**Context previews (first 3):**

1. _Warehouse Inventory Levels: The table stores stock by warehouse with references to either a component or product, plus on-hand, reserved, reorder, and last restock fields. This aligns closely with the…_

2. _Business concept 'Warehouse Inventory Levels' — The table stores stock by warehouse with references to either a component or product, plus on-hand, reserved, reorder, and last restock fields. This ali…_

3. _Relationship: INVENTORY references PRODUCT via foreign key PRODUCT_ID -> PRODUCT.PRODUCT_ID.…_

---

### ✅ QA-007 — How are work orders structured in the manufacturing system?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.7417 | **Gate:** `proceed`

**Expected answer:**
> Work orders represent production jobs with a unique identifier (work_order_id), product to be manufactured (product_id), optional parent work order for nested hierarchies (parent_work_order), quantity to produce (quantity_ordered), quantity completed so far (quantity_completed), current status (PEND…

**System answer:**
> Work orders are implemented by the `WORK_ORDER` table and represent production jobs or manufacturing runs for producing a specific product. The structure is hierarchical: each work order has a unique identifier in `WORK_ORDER_ID`, and `PARENT_WORK_ORDER` is an optional self-referencing foreign key to `WORK_ORDER.WORK_ORDER_ID`, which allows a large production job to be decomposed into child work o…

**Sources retrieved (12):** `Work Order→WORK_ORDER`, `parent_chunk_data_dictionary.md_6`, `WORK_ORDER→PRODUCT`, `WORK_ORDER→WORK_ORDER`, `parent_chunk_data_dictionary.md_3`, `WORK_ORDER→WAREHOUSE`, `Route→ROUTE`, `parent_chunk_data_dictionary.md_8`

**Context previews (first 3):**

1. _Business concept 'Work Order' — The table stores production job records with a product reference, ordered and completed quantities, status, priority, planned dates, and an optional parent work order f…_

2. _## work_order  Represents production jobs for manufacturing products with hierarchical work order support.  | Column | Data Type | Constraints | Description | |--------|-----------|-------------|-----…_

3. _Relationship: WORK_ORDER references PRODUCT via foreign key PRODUCT_ID -> PRODUCT.PRODUCT_ID.…_

---

### ✅ QA-008 — What information is captured in the shipment table?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.9317 | **Gate:** `proceed`

**Expected answer:**
> Shipments track material transfers with a unique identifier (shipment_id), shipment type (INBOUND from suppliers, OUTBOUND to customers, INTERNAL between warehouses), destination warehouse (warehouse_id), source supplier for inbound (supplier_id), destination customer for outbound (customer_id), shi…

**System answer:**
> The `SHIPMENT` table captures material transfer records between warehouses, suppliers, and customers. It is explicitly described as a shipment/transfer record that tracks source and destination locations through foreign keys indicating origin and recipient parties or locations, along with shipment type, dates, and status.

It stores the following information: `shipment_id` as the unique shipment i…

**Sources retrieved (12):** `source and destination locations`, `source and destination locations→SHIPMENT`, `SHIPMENT→WAREHOUSE`, `SHIPMENT→SUPPLIER`, `parent_chunk_data_dictionary.md_8`, `parent_chunk_business_glossary.md_0`, `Component-Supplier Relationship`, `Supplier`

**Context previews (first 3):**

1. _source and destination locations: The table is explicitly a shipment/transfer record with shipment type, ship/arrival dates, status, and foreign keys indicating origin and recipient parties or locatio…_

2. _Business concept 'source and destination locations' — The table is explicitly a shipment/transfer record with shipment type, ship/arrival dates, status, and foreign keys indicating origin and recipien…_

3. _Relationship: SHIPMENT references WAREHOUSE via foreign key WAREHOUSE_ID -> WAREHOUSE.WAREHOUSE_ID.…_

---

### ✅ QA-009 — How does the quality control system record inspections?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.9540 | **Gate:** `proceed`

**Expected answer:**
> Quality control records are stored with a unique identifier (qc_id), associated production batch (batch_id), applicable specification requirements (specification_id), inspection date (qc_date), inspection type (INCOMING for supplier materials, IN_PROCESS during manufacturing, FINAL for finished good…

**System answer:**
> The quality control system records inspections as individual inspection/test records in the physical table QUALITY_CONTROL. This table implements the business concept of inspection and testing records for quality assurance.

Each inspection record includes QC_ID as the unique identifier, along with BATCH_ID and SPECIFICATION_ID to tie the inspection to a specific production lot and the technical r…

**Sources retrieved (12):** `inspection and testing records for quality assurance→QUALITY_CONTROL`, `BOM→PRODUCT`, `parent_chunk_data_dictionary.md_3`, `BATCH→PRODUCT`, `BATCH→WAREHOUSE`, `parent_chunk_business_glossary.md_2`, `inspection and testing records for quality assurance`, `parent_chunk_business_glossary.md_0`

**Context previews (first 3):**

1. _Business concept 'inspection and testing records for quality assurance' — The columns qc_date, qc_type, inspector_id, result, defect_count, and notes indicate individual inspection/test records rather…_

2. _Relationship: BOM references PRODUCT via foreign key COMPONENT_PRODUCT_ID -> PRODUCT.PRODUCT_ID.…_

3. _# Manufacturing Data Dictionary  This data dictionary documents the database schema for the manufacturing supply chain system. It includes all tables, columns, data types, constraints, and relationshi…_

---

### ✅ QA-010 — What do specification records define?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.7558 | **Gate:** `proceed`

**Expected answer:**
> Specifications define technical requirements with a unique identifier (specification_id), descriptive name (specification_name), version number, effective date, specification type (DIMENSIONAL, MATERIAL, PERFORMANCE), critical parameter being measured (critical_parameter), acceptable minimum value (…

**System answer:**
> Specification records define the technical requirements, standards, and acceptance criteria for materials and products. The context says they include the specification identifier, name, version, effective date, specification type, critical parameter being tested, acceptable value range through minimum and maximum values, and unit of measure. They are used as the requirements that quality control t…

**Sources retrieved (12):** `inspection and testing records for quality assurance→QUALITY_CONTROL`, `Specification→SPECIFICATION`, `parent_chunk_data_dictionary.md_7`, `Component→COMPONENT`, `parent_chunk_business_glossary.md_2`, `inspection and testing records for quality assurance`, `Specification`, `parent_chunk_business_glossary.md_0`

**Context previews (first 3):**

1. _Business concept 'inspection and testing records for quality assurance' — The columns qc_date, qc_type, inspector_id, result, defect_count, and notes indicate individual inspection/test records rather…_

2. _Business concept 'Specification' — The table name and columns align directly with the business concept of a specification: identifier, name, version, effective date, type, critical parameter, and acce…_

3. _## specification  Defines technical requirements and acceptance criteria for materials and products.  | Column | Data Type | Constraints | Description | |--------|-----------|-------------|-----------…_

---

### ✅ QA-011 — How can I find which suppliers provide specific components?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.1645 | **Gate:** `proceed_with_warning`

**Expected answer:**
> Query the component_supplier table which links components to their approved suppliers. This table contains the component identifier (component_id), supplier identifier (supplier_id), preferred supplier flag (is_preferred), lead time in days (lead_time_days), and unit price (unit_price). Join with th…

**System answer:**
> Use the many-to-many junction table COMPONENT_SUPPLIER. The context says this table implements the “Component-Supplier Relationship” concept and contains both foreign keys needed to trace suppliers for a component.

The join path is COMPONENT_SUPPLIER.COMPONENT_ID -> COMPONENT.COMPONENT_ID and COMPONENT_SUPPLIER.SUPPLIER_ID -> SUPPLIER.SUPPLIER_ID. In practice, to find which suppliers provide a sp…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_5`, `parent_chunk_data_dictionary.md_4`, `parent_chunk_data_dictionary.md_3`, `Warehouse Inventory Levels→INVENTORY`, `parent_chunk_business_glossary.md_0`, `parent_chunk_business_glossary.md_1`, `Component-Supplier Relationship`, `Component-Supplier Relationship→COMPONENT_SUPPLIER`

**Context previews (first 3):**

1. _## warehouse  Stores physical storage location information for inventory management.  | Column | Data Type | Constraints | Description | |--------|-----------|-------------|-------------| | warehouse_…_

2. _## bom  Bill of Materials defining product composition and hierarchical structure. Supports recursive relationships for multi-level assemblies.  | Column | Data Type | Constraints | Description | |---…_

3. _# Manufacturing Data Dictionary  This data dictionary documents the database schema for the manufacturing supply chain system. It includes all tables, columns, data types, constraints, and relationshi…_

---

### ✅ QA-012 — How do I trace which components are needed to fulfill a work order?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.2334 | **Gate:** `proceed`

**Expected answer:**
> Start with the work_order table to get the product_id being manufactured. Join to the bom table using product_id as parent_product_id to find all direct components and sub-assemblies. For each component_product_id, if it is an ASSEMBLY type product, recursively query the bom table again to explode m…

**System answer:**
> To trace the components needed for a work order, start with `WORK_ORDER`. The key link is `WORK_ORDER.PRODUCT_ID -> PRODUCT.PRODUCT_ID`, which tells you which product the work order is manufacturing.

From there, the context shows two relevant structure mechanisms:

First, `PRODUCT` supports hierarchy through `PARENT_PRODUCT_ID -> PRODUCT.PRODUCT_ID`, so products can be organized as multi-level as…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_5`, `Work Order→WORK_ORDER`, `parent_chunk_data_dictionary.md_6`, `parent_chunk_data_dictionary.md_3`, `Warehouse Inventory Levels→INVENTORY`, `parent_chunk_data_dictionary.md_8`, `parent_chunk_data_dictionary.md_7`, `WORK_ORDER→PRODUCT`

**Context previews (first 3):**

1. _## warehouse  Stores physical storage location information for inventory management.  | Column | Data Type | Constraints | Description | |--------|-----------|-------------|-------------| | warehouse_…_

2. _Business concept 'Work Order' — The table stores production job records with a product reference, ordered and completed quantities, status, priority, planned dates, and an optional parent work order f…_

3. _## work_order  Represents production jobs for manufacturing products with hierarchical work order support.  | Column | Data Type | Constraints | Description | |--------|-----------|-------------|-----…_

---

### ✅ QA-013 — How can I identify which warehouses have available inventory for specific components?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.8215 | **Gate:** `proceed`

**Expected answer:**
> Query the inventory table filtered by component_id, joining with the warehouse table to get warehouse names and locations. Calculate available quantity as quantity_on_hand minus quantity_reserved. Filter for records where available quantity is greater than zero. Results show warehouse names, locatio…

**System answer:**
> Use the `INVENTORY` table to find stock records for the component, and join it to `WAREHOUSE` to identify the warehouse details.

The relevant relationship is `INVENTORY.WAREHOUSE_ID -> WAREHOUSE.WAREHOUSE_ID`.

For component-specific inventory, use these `INVENTORY` fields:
`COMPONENT_ID` to identify the component,
`WAREHOUSE_ID` to link to the warehouse,
`QUANTITY_ON_HAND`,
`QUANTITY_RESERVED`,
…

**Sources retrieved (12):** `Warehouse Inventory Levels`, `parent_chunk_data_dictionary.md_5`, `Warehouse Inventory Levels→INVENTORY`, `INVENTORY→WAREHOUSE`, `INVENTORY→COMPONENT`, `parent_chunk_data_dictionary.md_3`, `parent_chunk_data_dictionary.md_8`, `parent_chunk_data_dictionary.md_6`

**Context previews (first 3):**

1. _Warehouse Inventory Levels: The table stores stock by warehouse with references to either a component or product, plus on-hand, reserved, reorder, and last restock fields. This aligns closely with the…_

2. _## warehouse  Stores physical storage location information for inventory management.  | Column | Data Type | Constraints | Description | |--------|-----------|-------------|-------------| | warehouse_…_

3. _Business concept 'Warehouse Inventory Levels' — The table stores stock by warehouse with references to either a component or product, plus on-hand, reserved, reorder, and last restock fields. This ali…_

---

### ✅ QA-014 — How do I find which shipments delivered materials from a specific supplier?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.2401 | **Gate:** `proceed`

**Expected answer:**
> Query the shipment table filtering by supplier_id and shipment_type = 'INBOUND'. Join with the warehouse table to show destination warehouses. Filter for status = 'DELIVERED' and include actual_arrival date. Results can be ordered by ship_date descending to show most recent deliveries first.

**System answer:**
> Use the `SHIPMENT` table as the starting point and connect it to `SUPPLIER` through the foreign key `SHIPMENT.SUPPLIER_ID -> SUPPLIER.SUPPLIER_ID`.

From the schema, shipments tied to a supplier are inbound shipments, because `chk_supplier_inbound` ensures `supplier_id` is only set for `INBOUND` shipments. To find shipments that delivered materials from a specific supplier, filter for that supplie…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_8`, `SHIPMENT→SUPPLIER`, `source and destination locations→SHIPMENT`, `Supplier→SUPPLIER`, `parent_chunk_data_dictionary.md_5`, `parent_chunk_data_dictionary.md_7`, `parent_chunk_business_glossary.md_1`, `Supplier`

**Context previews (first 3):**

1. _## shipment  Tracks material transfers between warehouses, suppliers, and customers.  | Column | Data Type | Constraints | Description | |--------|-----------|-------------|-------------| | shipment_i…_

2. _Relationship: SHIPMENT references SUPPLIER via foreign key SUPPLIER_ID -> SUPPLIER.SUPPLIER_ID.…_

3. _Business concept 'source and destination locations' — The table is explicitly a shipment/transfer record with shipment type, ship/arrival dates, status, and foreign keys indicating origin and recipien…_

---

### ✅ QA-015 — How can I determine which quality control inspections were performed on a specific production batch?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.9779 | **Gate:** `proceed`

**Expected answer:**
> Query the quality_control table filtered by batch_id. Join with the specification table to get requirement details (specification_name, spec_type, acceptable ranges). Include qc_date, qc_type (INCOMING, IN_PROCESS, FINAL), result (PASS, FAIL, CONDITIONAL), and defect_count. This shows the complete i…

**System answer:**
> To determine which quality control inspections were performed on a specific production batch, look in the QUALITY_CONTROL table and filter by the batch identifier.

The relevant link is QUALITY_CONTROL.BATCH_ID to BATCH.BATCH_ID, because QC records are associated with specific production batches and the BATCH table stores the production lot. For a given batch, the inspection records are the rows i…

**Sources retrieved (12):** `inspection and testing records for quality assurance→QUALITY_CONTROL`, `Production Batch→BATCH`, `parent_chunk_data_dictionary.md_7`, `BATCH→PRODUCT`, `parent_chunk_data_dictionary.md_5`, `parent_chunk_data_dictionary.md_6`, `parent_chunk_data_dictionary.md_3`, `parent_chunk_business_glossary.md_2`

**Context previews (first 3):**

1. _Business concept 'inspection and testing records for quality assurance' — The columns qc_date, qc_type, inspector_id, result, defect_count, and notes indicate individual inspection/test records rather…_

2. _Business concept 'Production Batch' — The table is explicitly labeled as a BATCH table for production lots and contains batch-specific attributes such as product_id, production_date, quantity_produced…_

3. _## specification  Defines technical requirements and acceptance criteria for materials and products.  | Column | Data Type | Constraints | Description | |--------|-----------|-------------|-----------…_

---

### ✅ QA-016 — How do I track which work orders are in progress at a specific warehouse?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.7311 | **Gate:** `proceed`

**Expected answer:**
> Query the work_order table filtering by warehouse_id and status = 'IN_PROGRESS'. Join with the product table to get product names and types. Include quantity_ordered, quantity_completed, priority, planned_end_date, and calculate progress percentage as (quantity_completed / quantity_ordered * 100). O…

**System answer:**
> Use the `WORK_ORDER` table, because it stores production job records and includes both `status` and `warehouse_id`.

To find work orders that are currently in progress at a specific warehouse, filter `WORK_ORDER` where `STATUS = 'IN_PROGRESS'` and `WAREHOUSE_ID` matches the warehouse you care about. The direct relationship is `WORK_ORDER.WAREHOUSE_ID -> WAREHOUSE.WAREHOUSE_ID`.

If you already kno…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_5`, `parent_chunk_data_dictionary.md_6`, `WORK_ORDER→WAREHOUSE`, `Work Order→WORK_ORDER`, `Warehouse Inventory Levels→INVENTORY`, `Warehouse Inventory Levels`, `parent_chunk_data_dictionary.md_8`, `parent_chunk_data_dictionary.md_7`

**Context previews (first 3):**

1. _## warehouse  Stores physical storage location information for inventory management.  | Column | Data Type | Constraints | Description | |--------|-----------|-------------|-------------| | warehouse_…_

2. _## work_order  Represents production jobs for manufacturing products with hierarchical work order support.  | Column | Data Type | Constraints | Description | |--------|-----------|-------------|-----…_

3. _Relationship: WORK_ORDER references WAREHOUSE via foreign key WAREHOUSE_ID -> WAREHOUSE.WAREHOUSE_ID.…_

---

### ✅ QA-017 — How can I find which components need reordering based on current inventory levels?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.5211 | **Gate:** `proceed`

**Expected answer:**
> Query the inventory table and filter where quantity_on_hand minus quantity_reserved is less than reorder_threshold. Join with the component table to get component names, categories, and standard costs. Join with the warehouse table for location information. Results identify which components are belo…

**System answer:**
> From the retrieved context, this can only be answered at the schema level, not with a fully defined business rule.

The relevant table is INVENTORY, which tracks stock levels for both components and products at specific warehouses. For components, use the INVENTORY records where COMPONENT_ID is populated; the context states COMPONENT_ID and PRODUCT_ID are exclusive, so a component inventory row is…

**Sources retrieved (12):** `Warehouse Inventory Levels→INVENTORY`, `Warehouse Inventory Levels`, `parent_chunk_data_dictionary.md_5`, `INVENTORY→COMPONENT`, `parent_chunk_data_dictionary.md_3`, `parent_chunk_data_dictionary.md_7`, `parent_chunk_data_dictionary.md_4`, `parent_chunk_business_glossary.md_1`

**Context previews (first 3):**

1. _Business concept 'Warehouse Inventory Levels' — The table stores stock by warehouse with references to either a component or product, plus on-hand, reserved, reorder, and last restock fields. This ali…_

2. _Warehouse Inventory Levels: The table stores stock by warehouse with references to either a component or product, plus on-hand, reserved, reorder, and last restock fields. This aligns closely with the…_

3. _## warehouse  Stores physical storage location information for inventory management.  | Column | Data Type | Constraints | Description | |--------|-----------|-------------|-------------| | warehouse_…_

---

### ✅ QA-018 — How do I determine the manufacturing route for a specific product?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.6300 | **Gate:** `proceed`

**Expected answer:**
> Query the route table filtering by product_id, ordered by sequence_number ascending. For each operation, retrieve operation_name, work_center, cycle_time_minutes, and setup_time_minutes. Join with the product table to get product details. The sequence of operations shows the complete manufacturing w…

**System answer:**
> To determine the manufacturing route for a specific product, use the ROUTE table, which is the physical implementation of the business concept “Route.” The route is defined per product through ROUTE.PRODUCT_ID, and ROUTE references PRODUCT via the foreign key ROUTE.PRODUCT_ID -> PRODUCT.PRODUCT_ID.

At the schema level, the procedure is: first identify the product in PRODUCT using PRODUCT.PRODUCT_…

**Sources retrieved (12):** `Route→ROUTE`, `parent_chunk_data_dictionary.md_6`, `ROUTE→PRODUCT`, `parent_chunk_data_dictionary.md_3`, `parent_chunk_data_dictionary.md_7`, `Work Order→WORK_ORDER`, `Route`, `parent_chunk_business_glossary.md_2`

**Context previews (first 3):**

1. _Business concept 'Route' — The table is explicitly labeled as the ROUTE table for manufacturing workflow steps and contains the expected route attributes: product_id, route_name, sequence_number, oper…_

2. _## work_order  Represents production jobs for manufacturing products with hierarchical work order support.  | Column | Data Type | Constraints | Description | |--------|-----------|-------------|-----…_

3. _Relationship: ROUTE references PRODUCT via foreign key PRODUCT_ID -> PRODUCT.PRODUCT_ID.…_

---

### ✅ QA-019 — How can I find which batches are stored at a specific warehouse and their QC status?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.7533 | **Gate:** `proceed`

**Expected answer:**
> Query the batch table filtering by warehouse_id. Join with the product table to get product names and types. Include production_date, quantity_produced, expiry_date, and qc_status (PENDING, PASSED, FAILED, QUARANTINED). Filter by qc_status to isolate batches requiring quality attention or ready for …

**System answer:**
> Use the BATCH table as the primary source. It already stores both the warehouse reference and the batch QC status: BATCH has BATCH_ID, PRODUCT_ID, PRODUCTION_DATE, QUANTITY_PRODUCED, WAREHOUSE_ID, EXPIRY_DATE, and QC_STATUS.

To find batches stored at a specific warehouse, filter BATCH on BATCH.WAREHOUSE_ID for that warehouse. The relationship is explicitly defined as BATCH.WAREHOUSE_ID → WAREHOUS…

**Sources retrieved (12):** `Production Batch→BATCH`, `parent_chunk_data_dictionary.md_5`, `Warehouse Inventory Levels→INVENTORY`, `Warehouse Inventory Levels`, `BATCH→WAREHOUSE`, `parent_chunk_data_dictionary.md_6`, `inspection and testing records for quality assurance→QUALITY_CONTROL`, `parent_chunk_data_dictionary.md_8`

**Context previews (first 3):**

1. _Business concept 'Production Batch' — The table is explicitly labeled as a BATCH table for production lots and contains batch-specific attributes such as product_id, production_date, quantity_produced…_

2. _## warehouse  Stores physical storage location information for inventory management.  | Column | Data Type | Constraints | Description | |--------|-----------|-------------|-------------| | warehouse_…_

3. _Business concept 'Warehouse Inventory Levels' — The table stores stock by warehouse with references to either a component or product, plus on-hand, reserved, reorder, and last restock fields. This ali…_

---

### ✅ QA-020 — How do I identify which specifications apply to specific components?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.3098 | **Gate:** `proceed`

**Expected answer:**
> Query the component table and join with the specification table via specification_id. Include component_name, component_category, and specification details (specification_name, spec_type, critical_parameter, min_value, max_value, unit_of_measure). This shows the technical requirements that each comp…

**System answer:**
> Use the `COMPONENT` table and its `SPECIFICATION_ID` column. The retrieved context explicitly maps the business concept `Component` to physical table `COMPONENT`, which includes `COMPONENT_ID`, `COMPONENT_NAME`, `STANDARD_COST`, `UNIT_OF_MEASURE`, and `SPECIFICATION_ID`.

To identify which specification applies to a specific component, follow the schema relationship from `COMPONENT.SPECIFICATION_I…

**Sources retrieved (12):** `Component→COMPONENT`, `parent_chunk_data_dictionary.md_5`, `parent_chunk_data_dictionary.md_7`, `parent_chunk_data_dictionary.md_3`, `Warehouse Inventory Levels→INVENTORY`, `Specification→SPECIFICATION`, `Warehouse Inventory Levels`, `Component`

**Context previews (first 3):**

1. _Business concept 'Component' — The table is explicitly labeled as a COMPONENT table and contains component_id, component_name, standard_cost, unit_of_measure, and specification_id, which aligns direct…_

2. _## warehouse  Stores physical storage location information for inventory management.  | Column | Data Type | Constraints | Description | |--------|-----------|-------------|-------------| | warehouse_…_

3. _## specification  Defines technical requirements and acceptance criteria for materials and products.  | Column | Data Type | Constraints | Description | |--------|-----------|-------------|-----------…_

---

### ✅ QA-021 — How can I perform a complete BOM explosion to find all components required for a finished product?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.3509 | **Gate:** `proceed`

**Expected answer:**
> Use a recursive query starting from the product_id of the finished good. At each level, join the bom table to find component_product_id entries. For each component, check if product_type is 'ASSEMBLY' or 'FINISHED_GOOD'. If so, recursively query bom again using that component_product_id as the new p…

**System answer:**
> To do a complete BOM explosion, use the `bom` table as the recursive structure and the `product` table to identify what each node is.

Start with the finished product in `product`, using `product.product_id` as the root and `product.product_type = 'FINISHED_GOOD'` if you want to restrict the starting item to finished goods. Then find its immediate BOM lines by joining `bom.parent_product_id = prod…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_4`, `parent_chunk_data_dictionary.md_3`, `Bill of Materials Entry→BOM`, `BOM→PRODUCT`, `Product→PRODUCT`, `parent_chunk_data_dictionary.md_5`, `parent_chunk_data_dictionary.md_7`, `parent_chunk_business_glossary.md_0`

**Context previews (first 3):**

1. _## bom  Bill of Materials defining product composition and hierarchical structure. Supports recursive relationships for multi-level assemblies.  | Column | Data Type | Constraints | Description | |---…_

2. _# Manufacturing Data Dictionary  This data dictionary documents the database schema for the manufacturing supply chain system. It includes all tables, columns, data types, constraints, and relationshi…_

3. _Business concept 'Bill of Materials Entry' — The table stores parent_product_id, component_product_id, quantity, unit_of_measure, and bom_level, which exactly matches a BOM line item/entry defining pr…_

---

### ✅ QA-022 — How do I calculate the total material cost for a product including all sub-assemblies?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.2332 | **Gate:** `proceed`

**Expected answer:**
> Perform a recursive BOM explosion to find all leaf-level components. For each leaf component, join with the component table to get standard_cost. Multiply standard_cost by the accumulated quantity from the BOM traversal. Sum all component costs to get total material cost. This calculation must trave…

**System answer:**
> Use the `BOM` table to recursively explode the product structure, and use `PRODUCT.BASE_COST` as the cost source for each referenced item.

At the schema level, the trace starts with the target product in `PRODUCT` using `PRODUCT.PRODUCT_ID`. Then join that product to `BOM` on `BOM.PARENT_PRODUCT_ID = PRODUCT.PRODUCT_ID` to get its direct components. For each BOM row, join `BOM.COMPONENT_PRODUCT_I…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_3`, `parent_chunk_data_dictionary.md_4`, `parent_chunk_data_dictionary.md_7`, `parent_chunk_data_dictionary.md_8`, `Bill of Materials Entry→BOM`, `Product→PRODUCT`, `parent_chunk_data_dictionary.md_6`, `parent_chunk_data_dictionary.md_5`

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
> Use the `bom` table recursively.

The key structure is that `bom.parent_product_id` and `bom.component_product_id` both reference `product.product_id`, and the context explicitly says this supports recursive, multi-level assemblies such as `Bicycle → Wheel → Spoke`. To find every parent product that contains a specific component anywhere in its BOM, start with BOM rows where `component_product_id`…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_4`, `parent_chunk_data_dictionary.md_3`, `Bill of Materials Entry→BOM`, `BOM→PRODUCT`, `Product→PRODUCT`, `PRODUCT→PRODUCT`, `parent_chunk_data_dictionary.md_6`, `parent_chunk_data_dictionary.md_8`

**Context previews (first 3):**

1. _## bom  Bill of Materials defining product composition and hierarchical structure. Supports recursive relationships for multi-level assemblies.  | Column | Data Type | Constraints | Description | |---…_

2. _# Manufacturing Data Dictionary  This data dictionary documents the database schema for the manufacturing supply chain system. It includes all tables, columns, data types, constraints, and relationshi…_

3. _Business concept 'Bill of Materials Entry' — The table stores parent_product_id, component_product_id, quantity, unit_of_measure, and bom_level, which exactly matches a BOM line item/entry defining pr…_

---

### ✅ QA-024 — How do I identify work orders that require a specific component, considering nested sub-assemblies?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.3651 | **Gate:** `proceed`

**Expected answer:**
> First, perform reverse BOM traversal to find all parent products that contain the target component at any level. Then query the work_order table where product_id is in the set of parent products found. This includes work orders for finished goods that contain the component indirectly through sub-ass…

**System answer:**
> Use the product BOM hierarchy, not just the immediate work order record.

A `WORK_ORDER` identifies the product being built through `WORK_ORDER.PRODUCT_ID -> PRODUCT.PRODUCT_ID`. To determine whether that work order requires a specific component when sub-assemblies are nested, you need to recursively explode the `BOM` starting from that work order’s `PRODUCT_ID`.

The schema path is:

`WORK_ORDER.…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_6`, `parent_chunk_data_dictionary.md_5`, `parent_chunk_data_dictionary.md_3`, `parent_chunk_data_dictionary.md_4`, `Work Order→WORK_ORDER`, `WORK_ORDER→WORK_ORDER`, `Component→COMPONENT`, `WORK_ORDER→PRODUCT`

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
> Use the `BOM` table, because it explicitly stores `BOM_LEVEL`, described as the depth in the product hierarchy, and both `PARENT_PRODUCT_ID` and `COMPONENT_PRODUCT_ID` link BOM entries to `PRODUCT.PRODUCT_ID`.

If you want the maximum BOM depth in the entire system, you would look for the highest value in `BOM.BOM_LEVEL`. That column exists specifically to track hierarchy depth and support hierarc…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_4`, `Bill of Materials Entry→BOM`, `parent_chunk_data_dictionary.md_3`, `BOM→PRODUCT`, `Product→PRODUCT`, `parent_chunk_data_dictionary.md_7`, `parent_chunk_data_dictionary.md_5`, `Bill of Materials Entry`

**Context previews (first 3):**

1. _## bom  Bill of Materials defining product composition and hierarchical structure. Supports recursive relationships for multi-level assemblies.  | Column | Data Type | Constraints | Description | |---…_

2. _Business concept 'Bill of Materials Entry' — The table stores parent_product_id, component_product_id, quantity, unit_of_measure, and bom_level, which exactly matches a BOM line item/entry defining pr…_

3. _# Manufacturing Data Dictionary  This data dictionary documents the database schema for the manufacturing supply chain system. It includes all tables, columns, data types, constraints, and relationshi…_

---

### ✅ QA-026 — How do I find all products that have a specific product as a sub-assembly at any level?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.2392 | **Gate:** `proceed`

**Expected answer:**
> Perform a recursive search starting with the target product_id as the initial component_product_id in the bom table. For each parent_product_id found, check if that parent appears as a component in other bom entries. Continue recursively until reaching products that are not used as components elsewh…

**System answer:**
> Use the BOM hierarchy, not just a single direct lookup.

The relevant structure is `BOM`, which models each bill-of-materials line item with `PARENT_PRODUCT_ID` and `COMPONENT_PRODUCT_ID`, both pointing to `PRODUCT(PRODUCT_ID)`. The context explicitly says this table “supports recursive relationships for multi-level assemblies” and enables multi-level structures such as “Bicycle → Wheel → Spoke.”
…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_3`, `parent_chunk_data_dictionary.md_4`, `parent_chunk_data_dictionary.md_5`, `Warehouse Inventory Levels`, `Warehouse Inventory Levels→INVENTORY`, `Bill of Materials Entry→BOM`, `parent_chunk_data_dictionary.md_7`, `parent_chunk_data_dictionary.md_6`

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
> The retrieved context does not define a calculation rule for a product’s “total lead time” across its full BOM. It only tells you where the relevant lead-time data and hierarchy are stored.

At the schema level, the direct lead time for any product is `product.lead_time_days`, described as the product’s “procurement or production lead time.” The product hierarchy/composition is modeled primarily t…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_3`, `Product→PRODUCT`, `Component-Supplier Relationship→COMPONENT_SUPPLIER`, `parent_chunk_data_dictionary.md_4`, `parent_chunk_data_dictionary.md_7`, `parent_chunk_data_dictionary.md_6`, `Component-Supplier Relationship`, `parent_chunk_data_dictionary.md_8`

**Context previews (first 3):**

1. _# Manufacturing Data Dictionary  This data dictionary documents the database schema for the manufacturing supply chain system. It includes all tables, columns, data types, constraints, and relationshi…_

2. _Business concept 'Product' — The table stores product_id, product_name, product_type, base_cost, and lead_time_days, which directly matches the business concept describing a product's identifier, name…_

3. _Business concept 'Component-Supplier Relationship' — The table is explicitly described as a many-to-many component-supplier junction and contains foreign keys to both component and supplier, plus rela…_

---

### ✅ QA-028 — How do I generate a complete indented BOM report showing the hierarchical structure?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.4180 | **Gate:** `proceed`

**Expected answer:**
> Use a recursive query on the bom table that tracks the current depth level. Start with the top-level product (parent_product_id where product has no parent_product_id). At each level, output component details indented by depth level. Include product_name, quantity, and unit_of_measure. Recursively p…

**System answer:**
> Use the `bom` table as the hierarchy driver and the `product` table for names and product attributes.

The hierarchy is defined in `bom` by `parent_product_id` and `component_product_id`, and both columns are foreign keys to `product(product_id)`. To build a complete indented BOM, start from the top-level assembly in `bom.parent_product_id`, then repeatedly follow this path:

`bom.parent_product_i…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_4`, `parent_chunk_data_dictionary.md_3`, `Product→PRODUCT`, `parent_chunk_data_dictionary.md_6`, `Bill of Materials Entry→BOM`, `parent_chunk_data_dictionary.md_8`, `BOM→PRODUCT`, `parent_chunk_business_glossary.md_0`

**Context previews (first 3):**

1. _## bom  Bill of Materials defining product composition and hierarchical structure. Supports recursive relationships for multi-level assemblies.  | Column | Data Type | Constraints | Description | |---…_

2. _# Manufacturing Data Dictionary  This data dictionary documents the database schema for the manufacturing supply chain system. It includes all tables, columns, data types, constraints, and relationshi…_

3. _Business concept 'Product' — The table stores product_id, product_name, product_type, base_cost, and lead_time_days, which directly matches the business concept describing a product's identifier, name…_

---

### ✅ QA-029 — How can I find which components appear most frequently across all product BOMs?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.1587 | **Gate:** `proceed_with_warning`

**Expected answer:**
> Perform BOM explosion for all products and aggregate occurrences of each leaf-level component. Count how many distinct product hierarchies contain each component. Join with component table for component names. Order by frequency descending to identify common components that should be prioritized for…

**System answer:**
> Use the `BOM` table, because it implements the business concept of a Bill of Materials Entry and stores one row per parent/component relationship.

To find the components that appear most frequently across all product BOMs, aggregate `BOM` by `component_product_id` and count the number of BOM rows for each component. Then sort that count descending. If you want readable component details, join `BO…

**Sources retrieved (12):** `Bill of Materials Entry→BOM`, `parent_chunk_data_dictionary.md_4`, `parent_chunk_data_dictionary.md_3`, `Product→PRODUCT`, `BOM→PRODUCT`, `parent_chunk_data_dictionary.md_5`, `Warehouse Inventory Levels→INVENTORY`, `Warehouse Inventory Levels`

**Context previews (first 3):**

1. _Business concept 'Bill of Materials Entry' — The table stores parent_product_id, component_product_id, quantity, unit_of_measure, and bom_level, which exactly matches a BOM line item/entry defining pr…_

2. _## bom  Bill of Materials defining product composition and hierarchical structure. Supports recursive relationships for multi-level assemblies.  | Column | Data Type | Constraints | Description | |---…_

3. _# Manufacturing Data Dictionary  This data dictionary documents the database schema for the manufacturing supply chain system. It includes all tables, columns, data types, constraints, and relationshi…_

---

### ✅ QA-030 — How do I detect circular references in the BOM structure to prevent infinite loops?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.1295 | **Gate:** `proceed_with_warning`

**Expected answer:**
> Use a recursive query with a cycle detection check. Track the path of visited product_ids at each recursion level. If a product_id appears twice in the same path, a circular reference exists. Alternatively, check if any bom record has parent_product_id = component_product_id (direct self-reference),…

**System answer:**
> The retrieved context does not define a method to detect circular references or prevent infinite loops in the BOM structure. It does not provide a cycle-detection algorithm, recursive SQL, trigger, stored procedure, or validation rule for identifying loops.

What the context does say is that the `bom` table is the structure used for hierarchical product composition. In `bom`, both `parent_product_…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_4`, `parent_chunk_data_dictionary.md_3`, `BOM→PRODUCT`, `Bill of Materials Entry→BOM`, `Product→PRODUCT`, `parent_chunk_data_dictionary.md_8`, `parent_chunk_data_dictionary.md_7`, `parent_chunk_business_glossary.md_0`

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
> At the schema level, you would determine the supplier chain by first exploding the finished product’s multi-level bill of materials, and then attaching supplier relationships to the component items found in that hierarchy.

The hierarchy starts in `product`, where a finished good is a `product` row with `product_type = FINISHED_GOOD`. The explicit multi-level structure is modeled in `bom`, where `…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_3`, `parent_chunk_data_dictionary.md_4`, `parent_chunk_data_dictionary.md_8`, `Component-Supplier Relationship→COMPONENT_SUPPLIER`, `parent_chunk_data_dictionary.md_6`, `Supplier→SUPPLIER`, `Component-Supplier Relationship`, `parent_chunk_data_dictionary.md_7`

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
> Use the `WORK_ORDER` and `INVENTORY` tables.

At the schema level, the check is:

1. Start from `WORK_ORDER`.
   For the target work order, use:
   `WORK_ORDER.WORK_ORDER_ID`,
   `WORK_ORDER.PRODUCT_ID`,
   `WORK_ORDER.QUANTITY_ORDERED`,
   `WORK_ORDER.QUANTITY_COMPLETED`,
   and optionally `WORK_ORDER.WAREHOUSE_ID`.

2. Join to `INVENTORY` on the product:
   `WORK_ORDER.PRODUCT_ID = INVENTORY.PRO…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_5`, `parent_chunk_data_dictionary.md_6`, `Warehouse Inventory Levels`, `Warehouse Inventory Levels→INVENTORY`, `INVENTORY→WAREHOUSE`, `WORK_ORDER→WAREHOUSE`, `Work Order→WORK_ORDER`, `parent_chunk_data_dictionary.md_8`

**Context previews (first 3):**

1. _## warehouse  Stores physical storage location information for inventory management.  | Column | Data Type | Constraints | Description | |--------|-----------|-------------|-------------| | warehouse_…_

2. _## work_order  Represents production jobs for manufacturing products with hierarchical work order support.  | Column | Data Type | Constraints | Description | |--------|-----------|-------------|-----…_

3. _Warehouse Inventory Levels: The table stores stock by warehouse with references to either a component or product, plus on-hand, reserved, reorder, and last restock fields. This aligns closely with the…_

---

### ✅ QA-033 — How can I find which quality control inspections failed for components from specific suppliers?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.4561 | **Gate:** `proceed`

**Expected answer:**
> Query the quality_control table filtering by result = 'FAIL'. Join with the batch table to get product_id and production_date. Join with the bom table recursively to trace which products contain failed components. Join with component_supplier and supplier tables to identify the source supplier. Filt…

**System answer:**
> From the retrieved context, the part you can answer directly is the “failed quality control inspections” portion:

Failed inspections are the individual QC log records in the physical table `QUALITY_CONTROL`, using these columns: `QC_ID`, `BATCH_ID`, `SPECIFICATION_ID`, `QC_DATE`, `QC_TYPE`, `INSPECTOR_ID`, `RESULT`, `DEFECT_COUNT`, and `NOTES`. A failed inspection is a row where `RESULT = 'FAIL'`…

**Sources retrieved (12):** `inspection and testing records for quality assurance→QUALITY_CONTROL`, `parent_chunk_data_dictionary.md_5`, `parent_chunk_data_dictionary.md_3`, `parent_chunk_data_dictionary.md_4`, `Component-Supplier Relationship→COMPONENT_SUPPLIER`, `Component-Supplier Relationship`, `COMPONENT_SUPPLIER→SUPPLIER`, `parent_chunk_data_dictionary.md_8`

**Context previews (first 3):**

1. _Business concept 'inspection and testing records for quality assurance' — The columns qc_date, qc_type, inspector_id, result, defect_count, and notes indicate individual inspection/test records rather…_

2. _## warehouse  Stores physical storage location information for inventory management.  | Column | Data Type | Constraints | Description | |--------|-----------|-------------|-------------| | warehouse_…_

3. _# Manufacturing Data Dictionary  This data dictionary documents the database schema for the manufacturing supply chain system. It includes all tables, columns, data types, constraints, and relationshi…_

---

### ✅ QA-034 — How do I calculate the total manufacturing time for a work order including all sub-assembly work orders?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.1599 | **Gate:** `proceed_with_warning`

**Expected answer:**
> Query the work_order table starting with the parent work_order. Find all child work_orders where parent_work_order matches the current work_order_id. For each work order (parent and children), join with the route table on product_id to get all operations. Sum (cycle_time_minutes * quantity) plus set…

**System answer:**
> From the retrieved context, you can trace the relevant records, but you cannot derive a definitive calculation formula for “total manufacturing time.”

What is known is this: `WORK_ORDER` represents production jobs and supports hierarchy through `PARENT_WORK_ORDER`, which references `WORK_ORDER.WORK_ORDER_ID`. That means a top-level work order can have child work orders for decomposition. Each wor…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_6`, `Work Order→WORK_ORDER`, `parent_chunk_data_dictionary.md_3`, `Route→ROUTE`, `parent_chunk_data_dictionary.md_7`, `parent_chunk_data_dictionary.md_5`, `parent_chunk_data_dictionary.md_4`, `parent_chunk_business_glossary.md_0`

**Context previews (first 3):**

1. _## work_order  Represents production jobs for manufacturing products with hierarchical work order support.  | Column | Data Type | Constraints | Description | |--------|-----------|-------------|-----…_

2. _Business concept 'Work Order' — The table stores production job records with a product reference, ordered and completed quantities, status, priority, planned dates, and an optional parent work order f…_

3. _# Manufacturing Data Dictionary  This data dictionary documents the database schema for the manufacturing supply chain system. It includes all tables, columns, data types, constraints, and relationshi…_

---

### ✅ QA-035 — How can I identify which shipments are overdue and their impact on work orders?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0719 | **Gate:** `proceed_with_warning`

**Expected answer:**
> Query the shipment table filtering for status = 'SHIPPED' where actual_arrival is NULL and estimated_arrival is in the past (overdue). Join with the component_supplier table via supplier_id and component_id to identify which components are delayed. Perform reverse BOM lookup to find which parent pro…

**System answer:**
> From the retrieved context alone, you cannot determine an exact overdue-shipment rule or exact work-order impact.

What is known is that `SHIPMENT` contains the timing and status fields you would need to assess lateness at a schema level: `SHIPMENT_ID`, `SHIPMENT_TYPE` (`INBOUND`, `OUTBOUND`, `INTERNAL`), `WAREHOUSE_ID`, `SUPPLIER_ID`, `CUSTOMER_ID`, `SHIP_DATE`, `ESTIMATED_ARRIVAL`, `ACTUAL_ARRIV…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_5`, `parent_chunk_data_dictionary.md_8`, `parent_chunk_data_dictionary.md_6`, `Work Order→WORK_ORDER`, `WORK_ORDER→PRODUCT`, `source and destination locations→SHIPMENT`, `WORK_ORDER→WAREHOUSE`, `SHIPMENT→WAREHOUSE`

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
> Based on the retrieved context, you can find batches that are approaching or past expiry from the BATCH table, which includes BATCH_ID, PRODUCT_ID, PRODUCTION_DATE, QUANTITY_PRODUCED, WAREHOUSE_ID, EXPIRY_DATE, and QC_STATUS. “Past expiry” would mean filtering on BATCH.EXPIRY_DATE before your reference date. “Approaching expiry” also depends on BATCH.EXPIRY_DATE, but the context does not define wh…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_5`, `Warehouse Inventory Levels→INVENTORY`, `Warehouse Inventory Levels`, `Production Batch→BATCH`, `parent_chunk_data_dictionary.md_7`, `parent_chunk_data_dictionary.md_3`, `Component-Supplier Relationship`, `Component-Supplier Relationship→COMPONENT_SUPPLIER`

**Context previews (first 3):**

1. _## warehouse  Stores physical storage location information for inventory management.  | Column | Data Type | Constraints | Description | |--------|-----------|-------------|-------------| | warehouse_…_

2. _Business concept 'Warehouse Inventory Levels' — The table stores stock by warehouse with references to either a component or product, plus on-hand, reserved, reorder, and last restock fields. This ali…_

3. _Warehouse Inventory Levels: The table stores stock by warehouse with references to either a component or product, plus on-hand, reserved, reorder, and last restock fields. This aligns closely with the…_

---

### ✅ QA-037 — How can I generate a material requirements plan showing when to order components based on work order schedules?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0433 | **Gate:** `proceed_with_warning`

**Expected answer:**
> Query all work_orders with status 'PENDING' ordered by planned_start_date. For each work_order, perform BOM explosion to get required components and quantities. For each component, query inventory for current available stock across warehouses. Calculate net requirements = (required quantity * work_o…

**System answer:**
> From the retrieved context, an MRP-style report can be built from the schema, but the context does not define a single official MRP rule. The documented join path is to start with `WORK_ORDER`, join `WORK_ORDER.PRODUCT_ID = BOM.PARENT_PRODUCT_ID` to explode each production job into required BOM items, then join `BOM.COMPONENT_PRODUCT_ID = PRODUCT.PRODUCT_ID` to identify the required item and bring…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_6`, `parent_chunk_data_dictionary.md_7`, `parent_chunk_data_dictionary.md_5`, `Work Order→WORK_ORDER`, `parent_chunk_data_dictionary.md_4`, `parent_chunk_data_dictionary.md_3`, `Bill of Materials Entry→BOM`, `parent_chunk_business_glossary.md_1`

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
> The retrieved context supports this only partially, and only at the schema level.

You can trace the supplier side of the genealogy with `COMPONENT_SUPPLIER`, which is the many-to-many junction between `COMPONENT` and `SUPPLIER`. The path is `SUPPLIER.SUPPLIER_ID -> COMPONENT_SUPPLIER.SUPPLIER_ID` and `COMPONENT.COMPONENT_ID -> COMPONENT_SUPPLIER.COMPONENT_ID`. That gives you the supplier linked t…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_3`, `parent_chunk_data_dictionary.md_7`, `parent_chunk_data_dictionary.md_5`, `parent_chunk_data_dictionary.md_8`, `Component-Supplier Relationship→COMPONENT_SUPPLIER`, `Component-Supplier Relationship`, `parent_chunk_data_dictionary.md_4`, `Component→COMPONENT`

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

What is known is that supplier options for a component are modeled through the many-to-many table `COMPONENT_SUPPLIER`, which implements the “Component-Supplier Relationship.” That table contains `COMPONENT_ID`, `SUPPLIER_ID`, `IS_PREFERRED`, `LEAD_TIME_DAYS`, and `UNIT_PRICE`, and it links to `SUPPLIER`, which c…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_4`, `Component-Supplier Relationship→COMPONENT_SUPPLIER`, `Component-Supplier Relationship`, `parent_chunk_data_dictionary.md_3`, `parent_chunk_data_dictionary.md_5`, `parent_chunk_data_dictionary.md_8`, `Supplier→SUPPLIER`, `parent_chunk_data_dictionary.md_7`

**Context previews (first 3):**

1. _## bom  Bill of Materials defining product composition and hierarchical structure. Supports recursive relationships for multi-level assemblies.  | Column | Data Type | Constraints | Description | |---…_

2. _Business concept 'Component-Supplier Relationship' — The table is explicitly described as a many-to-many component-supplier junction and contains foreign keys to both component and supplier, plus rela…_

3. _Component-Supplier Relationship: The table is explicitly described as a many-to-many component-supplier junction and contains foreign keys to both component and supplier, plus relationship attributes …_

---

### ✅ QA-040 — How do I calculate the total landed cost for a product including component costs, supplier lead times, and manufacturing operations?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.1922 | **Gate:** `proceed_with_warning`

**Expected answer:**
> Perform recursive BOM explosion to get all leaf components. For each component, query component_supplier to get unit_price from primary supplier. Multiply by accumulated BOM quantity for material cost. Add shipping costs (estimated from shipment history). Query route table for the product to get all…

**System answer:**
> From the retrieved context, you can only calculate this partially at the schema level.

The relevant structures are `PRODUCT`, `COMPONENT`, `COMPONENT_SUPPLIER`, and `ROUTE`.

For the product itself, `PRODUCT` gives you `PRODUCT_ID`, `PRODUCT_NAME`, `PRODUCT_TYPE`, `PARENT_PRODUCT_ID`, `BASE_COST`, and `LEAD_TIME_DAYS`. The `parent_product_id` self-reference supports a multi-level product hierarch…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_3`, `Component-Supplier Relationship`, `Component-Supplier Relationship→COMPONENT_SUPPLIER`, `Product→PRODUCT`, `Route→ROUTE`, `parent_chunk_data_dictionary.md_6`, `parent_chunk_data_dictionary.md_7`, `Component→COMPONENT`

**Context previews (first 3):**

1. _# Manufacturing Data Dictionary  This data dictionary documents the database schema for the manufacturing supply chain system. It includes all tables, columns, data types, constraints, and relationshi…_

2. _Component-Supplier Relationship: The table is explicitly described as a many-to-many component-supplier junction and contains foreign keys to both component and supplier, plus relationship attributes …_

3. _Business concept 'Component-Supplier Relationship' — The table is explicitly described as a many-to-many component-supplier junction and contains foreign keys to both component and supplier, plus rela…_

---

## Anomalies & Observations

No anomalies detected. All questions grounded with acceptable RAGAS scores.
