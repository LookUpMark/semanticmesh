# AB-18 — 04_complex_manufacturing — Run Analysis

**Timestamp:** 2026-04-01 20:36:37  
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
| Triplets extracted | 353 |
| Entities resolved | 126 |
| Tables parsed | 13 |
| Tables completed | 13 |

## Query Evaluation Summary

| Metric | Value |
|--------|-------|
| Questions | 40 |
| Grounded | **40/40 (100%)** |
| Avg GT Coverage | 100% |
| Avg Top Score | 0.4239 |
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
> Products are stored in the `product` table, which represents all manufactured items in the system, including `FINISHED_GOOD`, `ASSEMBLY`, and `COMPONENT` products. For each product, the system stores the unique identifier (`product_id`), product name (`product_name`), type classification (`product_type`), parent product reference (`parent_product_id`), base manufacturing cost (`base_cost`), lead t…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_3`, `Work Order→WORK_ORDER`, `parent_chunk_data_dictionary.md_6`, `parent_chunk_data_dictionary.md_5`, `parent_chunk_data_dictionary.md_7`, `parent_chunk_business_glossary.md_0`, `parent_chunk_business_glossary.md_1`, `Work Order`

**Context previews (first 3):**

1. _# Manufacturing Data Dictionary  This data dictionary documents the database schema for the manufacturing supply chain system. It includes all tables, columns, data types, constraints, and relationshi…_

2. _Business concept 'Work Order' — The table is explicitly commented as WORK_ORDER and contains core manufacturing job fields such as product_id, quantities ordered/completed, status, priority, planned d…_

3. _## work_order  Represents production jobs for manufacturing products with hierarchical work order support.  | Column | Data Type | Constraints | Description | |--------|-----------|-------------|-----…_

---

### ✅ QA-002 — How are components defined in the manufacturing database?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.5910 | **Gate:** `proceed`

**Expected answer:**
> Components are defined with a unique identifier (component_id), descriptive name (component_name), category grouping (component_category), unit of measure (unit_of_measure), standard unit cost (standard_cost), and optional reference to technical specifications (specification_id). Components represen…

**System answer:**
> In the business glossary, a Component is defined as an atomic raw material or purchased part that cannot be further broken down into simpler manufactured items. Components are the building blocks used in manufacturing and are procured from external suppliers.

In the physical schema, components appear in multiple related ways. There is a `COMPONENT` table with the columns `component_id`, `componen…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_3`, `parent_chunk_data_dictionary.md_4`, `components they can provide through approved supplier relationships→COMPONENT_SUPPLIER`, `parent_chunk_data_dictionary.md_5`, `BOM entry→BOM`, `Inventory stock levels for components and products at specific warehouse locations→INVENTORY`, `parent_chunk_business_glossary.md_0`, `parent_chunk_business_glossary.md_1`

**Context previews (first 3):**

1. _# Manufacturing Data Dictionary  This data dictionary documents the database schema for the manufacturing supply chain system. It includes all tables, columns, data types, constraints, and relationshi…_

2. _## bom  Bill of Materials defining product composition and hierarchical structure. Supports recursive relationships for multi-level assemblies.  | Column | Data Type | Constraints | Description | |---…_

3. _Business concept 'components they can provide through approved supplier relationships' is implemented by physical table COMPONENT_SUPPLIER (columns: component_supplier_id, component_id, supplier_id, i…_

---

### ✅ QA-003 — What is the purpose of the Bill of Materials (BOM) table?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.9118 | **Gate:** `proceed`

**Expected answer:**
> The BOM table defines the hierarchical structure of products by specifying which components or sub-assemblies are required to manufacture each parent product. It records the unique BOM entry identifier (bom_id), parent product being built (parent_product_id), component or sub-assembly product (compo…

**System answer:**
> The Bill of Materials table, `bom`, defines product composition and hierarchical structure. Its purpose is to record which component products go into a parent product, along with the required quantity, unit of measure, hierarchy depth (`bom_level`), and whether a component is optional.

From the context, `bom` supports recursive, multi-level assemblies because both `parent_product_id` and `compone…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_4`, `BOM→PRODUCT`, `BOM entry→BOM`, `parent_chunk_data_dictionary.md_3`, `parent_chunk_data_dictionary.md_7`, `parent_chunk_data_dictionary.md_8`, `parent_chunk_business_glossary.md_0`, `parent_chunk_business_glossary.md_1`

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
> The system maintains supplier master data in the SUPPLIER table, which stores external vendor information for component procurement. From the retrieved context, the supplier attributes are supplier_id, supplier_name, contact_email, contact_phone, rating, and is_preferred.

It also maintains supplier-related relationship data in COMPONENT_SUPPLIER for “components they can provide through approved s…

**Sources retrieved (12):** `Preferred supplier for this component→SUPPLIER`, `parent_chunk_data_dictionary.md_4`, `SHIPMENT→SUPPLIER`, `components they can provide through approved supplier relationships→COMPONENT_SUPPLIER`, `Shipment`, `parent_chunk_data_dictionary.md_8`, `COMPONENT_SUPPLIER→SUPPLIER`, `Shipment→SHIPMENT`

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
> Warehouses are represented by the physical table `WAREHOUSE`, which implements the business concept of geographic location information and models a physical storage location for inventory management.

In the schema, `WAREHOUSE` has these columns: `warehouse_id` as the primary key and unique warehouse identifier, `warehouse_name` as a required warehouse name, `address`, `city`, `state`, `capacity` …

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
> The `INVENTORY` table tracks inventory stock levels for components and products at specific warehouse locations. It records, for each inventory record, the `warehouse_id`, either a `component_id` or a `product_id` (these are exclusive, so a record supports one or the other but not both), `quantity_on_hand`, `quantity_reserved`, `reorder_threshold`, and `last_restock_date`. The context also describ…

**Sources retrieved (12):** `INVENTORY→PRODUCT`, `INVENTORY→WAREHOUSE`, `INVENTORY→COMPONENT`, `Inventory stock levels for components and products at specific warehouse locations→INVENTORY`, `parent_chunk_data_dictionary.md_5`, `parent_chunk_data_dictionary.md_7`, `parent_chunk_data_dictionary.md_8`, `parent_chunk_business_glossary.md_1`

**Context previews (first 3):**

1. _Relationship: INVENTORY references PRODUCT via foreign key PRODUCT_ID -> PRODUCT.PRODUCT_ID.…_

2. _Relationship: INVENTORY references WAREHOUSE via foreign key WAREHOUSE_ID -> WAREHOUSE.WAREHOUSE_ID.…_

3. _Relationship: INVENTORY references COMPONENT via foreign key COMPONENT_ID -> COMPONENT.COMPONENT_ID.…_

---

### ✅ QA-007 — How are work orders structured in the manufacturing system?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.6242 | **Gate:** `proceed`

**Expected answer:**
> Work orders represent production jobs with a unique identifier (work_order_id), product to be manufactured (product_id), optional parent work order for nested hierarchies (parent_work_order), quantity to produce (quantity_ordered), quantity completed so far (quantity_completed), current status (PEND…

**System answer:**
> Work orders are represented by the business concept Work Order and are implemented by the physical table `WORK_ORDER`. They model production jobs for manufacturing products and include explicit support for hierarchy, so a large production job can be decomposed into child work orders.

Structurally, each work order has a unique identifier in `work_order_id` and references the product being manufact…

**Sources retrieved (12):** `Work Order→WORK_ORDER`, `parent_chunk_data_dictionary.md_6`, `WORK_ORDER→PRODUCT`, `WORK_ORDER→WORK_ORDER`, `parent_chunk_data_dictionary.md_3`, `WORK_ORDER→WAREHOUSE`, `parent_chunk_data_dictionary.md_8`, `Work Order`

**Context previews (first 3):**

1. _Business concept 'Work Order' — The table is explicitly commented as WORK_ORDER and contains core manufacturing job fields such as product_id, quantities ordered/completed, status, priority, planned d…_

2. _## work_order  Represents production jobs for manufacturing products with hierarchical work order support.  | Column | Data Type | Constraints | Description | |--------|-----------|-------------|-----…_

3. _Relationship: WORK_ORDER references PRODUCT via foreign key PRODUCT_ID -> PRODUCT.PRODUCT_ID.…_

---

### ✅ QA-008 — What information is captured in the shipment table?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.9810 | **Gate:** `proceed`

**Expected answer:**
> Shipments track material transfers with a unique identifier (shipment_id), shipment type (INBOUND from suppliers, OUTBOUND to customers, INTERNAL between warehouses), destination warehouse (warehouse_id), source supplier for inbound (supplier_id), destination customer for outbound (customer_id), shi…

**System answer:**
> The `SHIPMENT` table captures shipment records for material transfers between warehouses, suppliers, and customers. It stores:

`shipment_id`, the unique shipment identifier; `shipment_type`, which is required and can be `INBOUND`, `OUTBOUND`, or `INTERNAL`; `warehouse_id`, the warehouse reference; `supplier_id`, the supplier reference, used for inbound shipments only; `customer_id`, the customer …

**Sources retrieved (12):** `Shipment`, `Shipment→SHIPMENT`, `SHIPMENT→WAREHOUSE`, `SHIPMENT→SUPPLIER`, `parent_chunk_data_dictionary.md_8`, `parent_chunk_data_dictionary.md_5`, `parent_chunk_business_glossary.md_0`, `parent_chunk_business_glossary.md_1`

**Context previews (first 3):**

1. _Shipment: The table is explicitly labeled as SHIPMENT and contains shipment-specific attributes such as shipment_type, ship_date, estimated_arrival, actual_arrival, and status. The foreign keys to war…_

2. _Business concept 'Shipment' — The table is explicitly labeled as SHIPMENT and contains shipment-specific attributes such as shipment_type, ship_date, estimated_arrival, actual_arrival, and status. The…_

3. _Relationship: SHIPMENT references WAREHOUSE via foreign key WAREHOUSE_ID -> WAREHOUSE.WAREHOUSE_ID.…_

---

### ✅ QA-009 — How does the quality control system record inspections?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.9540 | **Gate:** `proceed`

**Expected answer:**
> Quality control records are stored with a unique identifier (qc_id), associated production batch (batch_id), applicable specification requirements (specification_id), inspection date (qc_date), inspection type (INCOMING for supplier materials, IN_PROCESS during manufacturing, FINAL for finished good…

**System answer:**
> The quality control system records inspections in the physical table QUALITY_CONTROL, which implements the business concept “Quality Control inspections.” The table stores these columns: qc_id, batch_id, specification_id, qc_date, qc_type, inspector_id, result, defect_count, and notes.

From the glossary, each QC record represents an inspection or testing activity performed on materials, in-proces…

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
> Specification records define the technical requirements, standards, and acceptance criteria for materials and products. In the `SPECIFICATION` table, they capture the specification name, version, effective date, specification type (`DIMENSIONAL`, `MATERIAL`, or `PERFORMANCE`), the critical parameter being tested, and the acceptable value range through `min_value`, `max_value`, and `unit_of_measure…

**Sources retrieved (12):** `version numbers, effective dates, specification types (dimensional, material, performance), critical parameters to test, and acceptable value ranges with units of measure→SPECIFICATION`, `parent_chunk_data_dictionary.md_7`, `Quality Control inspections→QUALITY_CONTROL`, `parent_chunk_data_dictionary.md_3`, `Product classification: FINISHED_GOOD, ASSEMBLY, COMPONENT→COMPONENT`, `parent_chunk_business_glossary.md_2`, `parent_chunk_business_glossary.md_0`, `version numbers, effective dates, specification types (dimensional, material, performance), critical parameters to test, and acceptable value ranges with units of measure`

**Context previews (first 3):**

1. _Business concept 'version numbers, effective dates, specification types (dimensional, material, performance), critical parameters to test, and acceptable value ranges with units of measure' is impleme…_

2. _## specification  Defines technical requirements and acceptance criteria for materials and products.  | Column | Data Type | Constraints | Description | |--------|-----------|-------------|-----------…_

3. _Business concept 'Quality Control inspections' is implemented by physical table QUALITY_CONTROL (columns: qc_id, batch_id, specification_id, qc_date, qc_type, inspector_id, result, defect_count, notes…_

---

### ✅ QA-011 — How can I find which suppliers provide specific components?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.3227 | **Gate:** `proceed`

**Expected answer:**
> Query the component_supplier table which links components to their approved suppliers. This table contains the component identifier (component_id), supplier identifier (supplier_id), preferred supplier flag (is_preferred), lead time in days (lead_time_days), and unit price (unit_price). Join with th…

**System answer:**
> To find which suppliers provide specific components, use the approved supplier relationship table `COMPONENT_SUPPLIER`.

The relevant schema path is:

`COMPONENT` → `COMPONENT_SUPPLIER` → `SUPPLIER`

Specifically:
`COMPONENT_SUPPLIER.COMPONENT_ID` references `COMPONENT.COMPONENT_ID`
and
`COMPONENT_SUPPLIER.SUPPLIER_ID` references `SUPPLIER.SUPPLIER_ID`.

From the context, the business concept “com…

**Sources retrieved (12):** `components they can provide through approved supplier relationships→COMPONENT_SUPPLIER`, `parent_chunk_data_dictionary.md_5`, `parent_chunk_data_dictionary.md_4`, `parent_chunk_data_dictionary.md_3`, `Inventory stock levels for components and products at specific warehouse locations→INVENTORY`, `components they can provide through approved supplier relationships`, `parent_chunk_business_glossary.md_0`, `parent_chunk_business_glossary.md_1`

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
> Use `WORK_ORDER` as the starting point. For a given `work_order_id`, read `WORK_ORDER.product_id` to find the product being manufactured, by joining `WORK_ORDER.product_id = PRODUCT.product_id`.

From that product, trace the required lower-level items through the product structure. The retrieved context confirms two schema mechanisms for this: `PRODUCT.parent_product_id`, which supports a self-ref…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_5`, `parent_chunk_data_dictionary.md_6`, `Work Order→WORK_ORDER`, `parent_chunk_data_dictionary.md_3`, `components they can provide through approved supplier relationships→COMPONENT_SUPPLIER`, `Inventory stock levels for components and products at specific warehouse locations→INVENTORY`, `parent_chunk_data_dictionary.md_8`, `parent_chunk_data_dictionary.md_7`

**Context previews (first 3):**

1. _## warehouse  Stores physical storage location information for inventory management.  | Column | Data Type | Constraints | Description | |--------|-----------|-------------|-------------| | warehouse_…_

2. _## work_order  Represents production jobs for manufacturing products with hierarchical work order support.  | Column | Data Type | Constraints | Description | |--------|-----------|-------------|-----…_

3. _Business concept 'Work Order' — The table is explicitly commented as WORK_ORDER and contains core manufacturing job fields such as product_id, quantities ordered/completed, status, priority, planned d…_

---

### ✅ QA-013 — How can I identify which warehouses have available inventory for specific components?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.9737 | **Gate:** `proceed`

**Expected answer:**
> Query the inventory table filtered by component_id, joining with the warehouse table to get warehouse names and locations. Calculate available quantity as quantity_on_hand minus quantity_reserved. Filter for records where available quantity is greater than zero. Results show warehouse names, locatio…

**System answer:**
> Use the `INVENTORY` table as the starting point, because the business concept “Inventory stock levels for components and products at specific warehouse locations” is implemented there. To find warehouses for a specific component, filter `INVENTORY.component_id` to the component of interest and join to `WAREHOUSE` on `INVENTORY.warehouse_id = WAREHOUSE.warehouse_id`.

From the context, the relevant…

**Sources retrieved (12):** `Inventory stock levels for components and products at specific warehouse locations→INVENTORY`, `parent_chunk_data_dictionary.md_5`, `INVENTORY→WAREHOUSE`, `INVENTORY→COMPONENT`, `parent_chunk_data_dictionary.md_3`, `parent_chunk_data_dictionary.md_8`, `parent_chunk_data_dictionary.md_6`, `parent_chunk_data_dictionary.md_4`

**Context previews (first 3):**

1. _Business concept 'Inventory stock levels for components and products at specific warehouse locations' is implemented by physical table INVENTORY (columns: inventory_id, warehouse_id, component_id, pro…_

2. _## warehouse  Stores physical storage location information for inventory management.  | Column | Data Type | Constraints | Description | |--------|-----------|-------------|-------------| | warehouse_…_

3. _Relationship: INVENTORY references WAREHOUSE via foreign key WAREHOUSE_ID -> WAREHOUSE.WAREHOUSE_ID.…_

---

### ✅ QA-014 — How do I find which shipments delivered materials from a specific supplier?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.3860 | **Gate:** `proceed`

**Expected answer:**
> Query the shipment table filtering by supplier_id and shipment_type = 'INBOUND'. Join with the warehouse table to show destination warehouses. Filter for status = 'DELIVERED' and include actual_arrival date. Results can be ordered by ship_date descending to show most recent deliveries first.

**System answer:**
> Use the `shipment` table, because it tracks material transfers between warehouses, suppliers, and customers and includes `supplier_id`, `shipment_type`, `actual_arrival`, and `status`.

To find shipments that delivered materials from a specific supplier, filter `shipment` by:
`shipment.supplier_id = <specific supplier>`
and
`shipment.status = 'DELIVERED'`.

From the schema, supplier-linked shipmen…

**Sources retrieved (12):** `Shipment`, `parent_chunk_data_dictionary.md_8`, `Shipment→SHIPMENT`, `SHIPMENT→SUPPLIER`, `parent_chunk_data_dictionary.md_5`, `Inventory stock levels for components and products at specific warehouse locations→INVENTORY`, `parent_chunk_data_dictionary.md_7`, `parent_chunk_data_dictionary.md_3`

**Context previews (first 3):**

1. _Shipment: The table is explicitly labeled as SHIPMENT and contains shipment-specific attributes such as shipment_type, ship_date, estimated_arrival, actual_arrival, and status. The foreign keys to war…_

2. _## shipment  Tracks material transfers between warehouses, suppliers, and customers.  | Column | Data Type | Constraints | Description | |--------|-----------|-------------|-------------| | shipment_i…_

3. _Business concept 'Shipment' — The table is explicitly labeled as SHIPMENT and contains shipment-specific attributes such as shipment_type, ship_date, estimated_arrival, actual_arrival, and status. The…_

---

### ✅ QA-015 — How can I determine which quality control inspections were performed on a specific production batch?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.9779 | **Gate:** `proceed`

**Expected answer:**
> Query the quality_control table filtered by batch_id. Join with the specification table to get requirement details (specification_name, spec_type, acceptable ranges). Include qc_date, qc_type (INCOMING, IN_PROCESS, FINAL), result (PASS, FAIL, CONDITIONAL), and defect_count. This shows the complete i…

**System answer:**
> To determine which quality control inspections were performed on a specific production batch, use the QUALITY_CONTROL table, which implements the business concept “Quality Control inspections.” The key column is batch_id, because QC inspections are associated with specific production batches.

For a given batch, filter QUALITY_CONTROL where QUALITY_CONTROL.batch_id equals the target batch_id. Each…

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
> Use the `work_order` table, because it stores the production job, its `status`, and its `warehouse_id`.

To find work orders that are currently in progress at a specific warehouse, filter `work_order.status` to `IN_PROGRESS` and filter `work_order.warehouse_id` to the target warehouse. The key columns are `work_order_id`, `product_id`, `quantity_ordered`, `quantity_completed`, `priority`, `planned…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_5`, `parent_chunk_data_dictionary.md_6`, `WORK_ORDER→WAREHOUSE`, `Inventory stock levels for components and products at specific warehouse locations→INVENTORY`, `Work Order→WORK_ORDER`, `parent_chunk_data_dictionary.md_8`, `parent_chunk_data_dictionary.md_7`, `parent_chunk_business_glossary.md_1`

**Context previews (first 3):**

1. _## warehouse  Stores physical storage location information for inventory management.  | Column | Data Type | Constraints | Description | |--------|-----------|-------------|-------------| | warehouse_…_

2. _## work_order  Represents production jobs for manufacturing products with hierarchical work order support.  | Column | Data Type | Constraints | Description | |--------|-----------|-------------|-----…_

3. _Relationship: WORK_ORDER references WAREHOUSE via foreign key WAREHOUSE_ID -> WAREHOUSE.WAREHOUSE_ID.…_

---

### ✅ QA-017 — How can I find which components need reordering based on current inventory levels?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.5478 | **Gate:** `proceed`

**Expected answer:**
> Query the inventory table and filter where quantity_on_hand minus quantity_reserved is less than reorder_threshold. Join with the component table to get component names, categories, and standard costs. Join with the warehouse table for location information. Results identify which components are belo…

**System answer:**
> Use the `INVENTORY` table, which implements the business concept “Inventory stock levels for components and products at specific warehouse locations.”

At the schema level, the relevant columns are `component_id`, `product_id`, `warehouse_id`, `quantity_on_hand`, `quantity_reserved`, `reorder_threshold`, and `last_restock_date`. Because an inventory record is for either a component or a product, a…

**Sources retrieved (12):** `Inventory stock levels for components and products at specific warehouse locations→INVENTORY`, `parent_chunk_data_dictionary.md_5`, `INVENTORY→COMPONENT`, `parent_chunk_data_dictionary.md_3`, `parent_chunk_data_dictionary.md_7`, `parent_chunk_data_dictionary.md_4`, `parent_chunk_data_dictionary.md_6`, `components they can provide through approved supplier relationships→COMPONENT_SUPPLIER`

**Context previews (first 3):**

1. _Business concept 'Inventory stock levels for components and products at specific warehouse locations' is implemented by physical table INVENTORY (columns: inventory_id, warehouse_id, component_id, pro…_

2. _## warehouse  Stores physical storage location information for inventory management.  | Column | Data Type | Constraints | Description | |--------|-----------|-------------|-------------| | warehouse_…_

3. _Relationship: INVENTORY references COMPONENT via foreign key COMPONENT_ID -> COMPONENT.COMPONENT_ID.…_

---

### ✅ QA-018 — How do I determine the manufacturing route for a specific product?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0413 | **Gate:** `proceed_with_warning`

**Expected answer:**
> Query the route table filtering by product_id, ordered by sequence_number ascending. For each operation, retrieve operation_name, work_center, cycle_time_minutes, and setup_time_minutes. Join with the product table to get product details. The sequence of operations shows the complete manufacturing w…

**System answer:**
> To determine the manufacturing route for a specific product from the schema metadata in the knowledge graph, use the `ROUTE` table and match it to the product through `ROUTE.PRODUCT_ID -> PRODUCT.PRODUCT_ID`.

At the schema level, the route is represented as `Route Step`, and the context states that each row in `ROUTE` contains a single operation in a product’s routing. The relevant `ROUTE` column…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_6`, `ROUTE→PRODUCT`, `Route Step→ROUTE`, `parent_chunk_data_dictionary.md_3`, `Work Order→WORK_ORDER`, `parent_chunk_data_dictionary.md_7`, `the product produced, production date, quantity produced, warehouse location, expiry date (if applicable), and quality control status→PRODUCT`, `parent_chunk_business_glossary.md_2`

**Context previews (first 3):**

1. _## work_order  Represents production jobs for manufacturing products with hierarchical work order support.  | Column | Data Type | Constraints | Description | |--------|-----------|-------------|-----…_

2. _Relationship: ROUTE references PRODUCT via foreign key PRODUCT_ID -> PRODUCT.PRODUCT_ID.…_

3. _Business concept 'Route Step' — Each row contains a single operation in a product"s routing, with sequence number, operation name, work center, and timing fields that align with the route-step concept…_

---

### ✅ QA-019 — How can I find which batches are stored at a specific warehouse and their QC status?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.7533 | **Gate:** `proceed`

**Expected answer:**
> Query the batch table filtering by warehouse_id. Join with the product table to get product names and types. Include production_date, quantity_produced, expiry_date, and qc_status (PENDING, PASSED, FAILED, QUARANTINED). Filter by qc_status to isolate batches requiring quality attention or ready for …

**System answer:**
> Use the BATCH table as the starting point. The business concept “Production batch reference” is implemented by BATCH with columns batch_id, product_id, production_date, quantity_produced, warehouse_id, expiry_date, and qc_status. BATCH references WAREHOUSE through BATCH.warehouse_id -> WAREHOUSE.warehouse_id.

So, to find batches at a specific warehouse, filter BATCH by warehouse_id. If you need t…

**Sources retrieved (12):** `Production batch reference→BATCH`, `parent_chunk_data_dictionary.md_5`, `Inventory stock levels for components and products at specific warehouse locations→INVENTORY`, `BATCH→WAREHOUSE`, `Quality Control inspections→QUALITY_CONTROL`, `the product produced, production date, quantity produced, warehouse location, expiry date (if applicable), and quality control status→PRODUCT`, `parent_chunk_data_dictionary.md_6`, `parent_chunk_data_dictionary.md_8`

**Context previews (first 3):**

1. _Business concept 'Production batch reference' is implemented by physical table BATCH (columns: batch_id, product_id, production_date, quantity_produced, warehouse_id, expiry_date, qc_status).…_

2. _## warehouse  Stores physical storage location information for inventory management.  | Column | Data Type | Constraints | Description | |--------|-----------|-------------|-------------| | warehouse_…_

3. _Business concept 'Inventory stock levels for components and products at specific warehouse locations' is implemented by physical table INVENTORY (columns: inventory_id, warehouse_id, component_id, pro…_

---

### ✅ QA-020 — How do I identify which specifications apply to specific components?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.2550 | **Gate:** `proceed`

**Expected answer:**
> Query the component table and join with the specification table via specification_id. Include component_name, component_category, and specification details (specification_name, spec_type, critical_parameter, min_value, max_value, unit_of_measure). This shows the technical requirements that each comp…

**System answer:**
> Use the `COMPONENT` table to find the specification assigned to each component. The applicable join path is `COMPONENT.specification_id` → `SPECIFICATION.specification_id`.

From the context, `COMPONENT` includes these columns: `component_id`, `component_name`, `component_category`, `unit_of_measure`, `standard_cost`, and `specification_id`. The `SPECIFICATION` table defines the actual requirement…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_5`, `Product classification: FINISHED_GOOD, ASSEMBLY, COMPONENT→COMPONENT`, `parent_chunk_data_dictionary.md_7`, `parent_chunk_data_dictionary.md_3`, `Inventory stock levels for components and products at specific warehouse locations→INVENTORY`, `version numbers, effective dates, specification types (dimensional, material, performance), critical parameters to test, and acceptable value ranges with units of measure→SPECIFICATION`, `parent_chunk_data_dictionary.md_4`, `components they can provide through approved supplier relationships→COMPONENT_SUPPLIER`

**Context previews (first 3):**

1. _## warehouse  Stores physical storage location information for inventory management.  | Column | Data Type | Constraints | Description | |--------|-----------|-------------|-------------| | warehouse_…_

2. _Business concept 'Product classification: FINISHED_GOOD, ASSEMBLY, COMPONENT' — Product classification: FINISHED_GOOD, ASSEMBLY, COMPONENT is implemented by physical table COMPONENT (columns: componen…_

3. _## specification  Defines technical requirements and acceptance criteria for materials and products.  | Column | Data Type | Constraints | Description | |--------|-----------|-------------|-----------…_

---

### ✅ QA-021 — How can I perform a complete BOM explosion to find all components required for a finished product?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.3509 | **Gate:** `proceed`

**Expected answer:**
> Use a recursive query starting from the product_id of the finished good. At each level, join the bom table to find component_product_id entries. For each component, check if product_type is 'ASSEMBLY' or 'FINISHED_GOOD'. If so, recursively query bom again using that component_product_id as the new p…

**System answer:**
> To perform a complete BOM explosion for a finished product, use the `bom` table as the recursive structure and the `product` table to identify the product at each level.

Start with the finished product in `product`, using its `product_id`. The `product` table classifies products as `FINISHED_GOOD`, `ASSEMBLY`, or `COMPONENT`, so your root item is the `product.product_id` for the finished good.

T…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_4`, `parent_chunk_data_dictionary.md_3`, `BOM entry→BOM`, `BOM→PRODUCT`, `Product classification: FINISHED_GOOD, ASSEMBLY, COMPONENT→COMPONENT`, `parent_chunk_data_dictionary.md_5`, `parent_chunk_data_dictionary.md_7`, `parent_chunk_data_dictionary.md_6`

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
> Use the `bom` and `product` tables as a recursive cost rollup.

Start with the target row in `product` using `product.product_id`. Then traverse the BOM hierarchy through `bom.parent_product_id = product.product_id`. For each BOM row, follow `bom.component_product_id` back to `product.product_id` to get the child item, and keep recursing because the context says the `bom` table supports multi-leve…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_3`, `parent_chunk_data_dictionary.md_4`, `parent_chunk_data_dictionary.md_7`, `Product classification: FINISHED_GOOD, ASSEMBLY, COMPONENT→COMPONENT`, `parent_chunk_data_dictionary.md_8`, `parent_chunk_data_dictionary.md_6`, `the product produced, production date, quantity produced, warehouse location, expiry date (if applicable), and quality control status→PRODUCT`, `parent_chunk_data_dictionary.md_5`

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
> Use the `bom` table, because the business concept “BOM entry” is implemented by `BOM (bom_id, parent_product_id, component_product_id, quantity, unit_of_measure, bom_level, is_optional)`, and this table is explicitly defined to support recursive multi-level assemblies.

To find every parent product that contains a specific component anywhere in the structure, start with the target component’s `pro…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_4`, `parent_chunk_data_dictionary.md_3`, `BOM entry→BOM`, `BOM→PRODUCT`, `PRODUCT→PRODUCT`, `parent_chunk_data_dictionary.md_6`, `parent_chunk_data_dictionary.md_8`, `parent_chunk_data_dictionary.md_5`

**Context previews (first 3):**

1. _## bom  Bill of Materials defining product composition and hierarchical structure. Supports recursive relationships for multi-level assemblies.  | Column | Data Type | Constraints | Description | |---…_

2. _# Manufacturing Data Dictionary  This data dictionary documents the database schema for the manufacturing supply chain system. It includes all tables, columns, data types, constraints, and relationshi…_

3. _Business concept 'BOM entry' is implemented by physical table BOM (columns: bom_id, parent_product_id, component_product_id, quantity, unit_of_measure, bom_level, is_optional).…_

---

### ✅ QA-024 — How do I identify work orders that require a specific component, considering nested sub-assemblies?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.3651 | **Gate:** `proceed`

**Expected answer:**
> First, perform reverse BOM traversal to find all parent products that contain the target component at any level. Then query the work_order table where product_id is in the set of parent products found. This includes work orders for finished goods that contain the component indirectly through sub-ass…

**System answer:**
> Use the `WORK_ORDER` table together with the `BOM` table, and trace the BOM recursively.

At the schema level, the path is:

`WORK_ORDER.product_id -> PRODUCT.product_id -> BOM.parent_product_id`

From there, follow the BOM hierarchy through:

`BOM.component_product_id -> PRODUCT.product_id`

and, for nested sub-assemblies, treat that `component_product_id` as another `BOM.parent_product_id` and c…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_6`, `parent_chunk_data_dictionary.md_5`, `parent_chunk_data_dictionary.md_3`, `parent_chunk_data_dictionary.md_4`, `Work Order→WORK_ORDER`, `WORK_ORDER→WORK_ORDER`, `WORK_ORDER→PRODUCT`, `WORK_ORDER→WAREHOUSE`

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
> Use the `bom` table, because it is the physical implementation of the business concept “BOM entry,” and it includes the `bom_level` column, which is explicitly described as the “depth in product hierarchy” and “tracks depth for performance optimization.”

If you want the maximum BOM depth across the entire system, take the maximum value of `BOM.bom_level`.

If you want the maximum BOM depth for a …

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_4`, `parent_chunk_data_dictionary.md_3`, `BOM entry→BOM`, `BOM→PRODUCT`, `parent_chunk_data_dictionary.md_7`, `parent_chunk_data_dictionary.md_5`, `parent_chunk_data_dictionary.md_6`, `version numbers, effective dates, specification types (dimensional, material, performance), critical parameters to test, and acceptable value ranges with units of measure→SPECIFICATION`

**Context previews (first 3):**

1. _## bom  Bill of Materials defining product composition and hierarchical structure. Supports recursive relationships for multi-level assemblies.  | Column | Data Type | Constraints | Description | |---…_

2. _# Manufacturing Data Dictionary  This data dictionary documents the database schema for the manufacturing supply chain system. It includes all tables, columns, data types, constraints, and relationshi…_

3. _Business concept 'BOM entry' is implemented by physical table BOM (columns: bom_id, parent_product_id, component_product_id, quantity, unit_of_measure, bom_level, is_optional).…_

---

### ✅ QA-026 — How do I find all products that have a specific product as a sub-assembly at any level?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.2392 | **Gate:** `proceed`

**Expected answer:**
> Perform a recursive search starting with the target product_id as the initial component_product_id in the bom table. For each parent_product_id found, check if that parent appears as a component in other bom entries. Continue recursively until reaching products that are not used as components elsewh…

**System answer:**
> Use the `bom` table to traverse the product hierarchy recursively.

The relevant structure is:

`bom.component_product_id` → the product that is used as a component or sub-assembly  
`bom.parent_product_id` → the product that contains it  
Both columns are foreign keys to `product(product_id)`.

To find all products that contain a specific product at any level, start with the target product’s `pro…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_3`, `parent_chunk_data_dictionary.md_4`, `parent_chunk_data_dictionary.md_5`, `Inventory stock levels for components and products at specific warehouse locations→INVENTORY`, `Product classification: FINISHED_GOOD, ASSEMBLY, COMPONENT→COMPONENT`, `parent_chunk_data_dictionary.md_7`, `parent_chunk_data_dictionary.md_6`, `BOM entry→BOM`

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
> From the schema, the lead-time attribute is `product.lead_time_days`, described as the product’s “procurement or production lead time.” To include sub-assemblies, the correct structural path is to traverse the `bom` table recursively, because `bom` is the Bill of Materials that “defines product composition and hierarchical structure” and supports “multi-level assemblies.”

At the schema level, the…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_3`, `the product produced, production date, quantity produced, warehouse location, expiry date (if applicable), and quality control status→PRODUCT`, `components they can provide through approved supplier relationships→COMPONENT_SUPPLIER`, `parent_chunk_data_dictionary.md_4`, `parent_chunk_data_dictionary.md_7`, `parent_chunk_data_dictionary.md_6`, `parent_chunk_data_dictionary.md_8`, `parent_chunk_data_dictionary.md_5`

**Context previews (first 3):**

1. _# Manufacturing Data Dictionary  This data dictionary documents the database schema for the manufacturing supply chain system. It includes all tables, columns, data types, constraints, and relationshi…_

2. _Business concept 'the product produced, production date, quantity produced, warehouse location, expiry date (if applicable), and quality control status' is implemented by physical table PRODUCT (colum…_

3. _Business concept 'components they can provide through approved supplier relationships' is implemented by physical table COMPONENT_SUPPLIER (columns: component_supplier_id, component_id, supplier_id, i…_

---

### ✅ QA-028 — How do I generate a complete indented BOM report showing the hierarchical structure?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.4180 | **Gate:** `proceed`

**Expected answer:**
> Use a recursive query on the bom table that tracks the current depth level. Start with the top-level product (parent_product_id where product has no parent_product_id). At each level, output component details indented by depth level. Include product_name, quantity, and unit_of_measure. Recursively p…

**System answer:**
> Use the `bom` table as the source for the hierarchy, because it is the table that defines product composition and supports recursive multi-level assemblies. A complete indented BOM report is built by starting with a root product in `product`, then repeatedly following `bom.parent_product_id → bom.component_product_id` down through all levels.

The core join path is: `bom.parent_product_id → produc…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_4`, `parent_chunk_data_dictionary.md_3`, `parent_chunk_data_dictionary.md_6`, `parent_chunk_data_dictionary.md_8`, `BOM entry→BOM`, `Work Order→WORK_ORDER`, `BOM→PRODUCT`, `parent_chunk_business_glossary.md_0`

**Context previews (first 3):**

1. _## bom  Bill of Materials defining product composition and hierarchical structure. Supports recursive relationships for multi-level assemblies.  | Column | Data Type | Constraints | Description | |---…_

2. _# Manufacturing Data Dictionary  This data dictionary documents the database schema for the manufacturing supply chain system. It includes all tables, columns, data types, constraints, and relationshi…_

3. _## work_order  Represents production jobs for manufacturing products with hierarchical work order support.  | Column | Data Type | Constraints | Description | |--------|-----------|-------------|-----…_

---

### ✅ QA-029 — How can I find which components appear most frequently across all product BOMs?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.1587 | **Gate:** `proceed_with_warning`

**Expected answer:**
> Perform BOM explosion for all products and aggregate occurrences of each leaf-level component. Count how many distinct product hierarchies contain each component. Join with component table for component names. Order by frequency descending to identify common components that should be prioritized for…

**System answer:**
> Use the `bom` table as the primary source, because a BOM entry is implemented by `BOM(bom_id, parent_product_id, component_product_id, quantity, unit_of_measure, bom_level, is_optional)`.

At the schema level, the way to find the most frequently used components is to count how many BOM rows reference each `component_product_id`. The core logic is:

Join `bom.component_product_id` to `product.produ…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_4`, `parent_chunk_data_dictionary.md_3`, `BOM entry→BOM`, `BOM→PRODUCT`, `parent_chunk_data_dictionary.md_5`, `Inventory stock levels for components and products at specific warehouse locations→INVENTORY`, `Product classification: FINISHED_GOOD, ASSEMBLY, COMPONENT→COMPONENT`, `parent_chunk_data_dictionary.md_7`

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
> The retrieved context only gives the BOM structure, not a documented cycle-detection procedure.

What is known from the context is that `bom` models a recursive product hierarchy using `parent_product_id` and `component_product_id`, and both columns reference `product(product_id)`. The table is explicitly described as supporting multi-level assemblies, and `bom_level` is used to track depth for hi…

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
> From the retrieved context, you can determine the complete product structure for a finished product, but you cannot fully determine the complete supplier chain for each sub-assembly because the necessary supplier-to-item relationship is not present.

The part that is supported is the hierarchy traversal. Start with `product`, where the finished item is a `product` record and `product_type` can be …

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_3`, `Product classification: FINISHED_GOOD, ASSEMBLY, COMPONENT→COMPONENT`, `parent_chunk_data_dictionary.md_4`, `parent_chunk_data_dictionary.md_8`, `parent_chunk_data_dictionary.md_6`, `parent_chunk_data_dictionary.md_7`, `Shipment→SHIPMENT`, `parent_chunk_data_dictionary.md_5`

**Context previews (first 3):**

1. _# Manufacturing Data Dictionary  This data dictionary documents the database schema for the manufacturing supply chain system. It includes all tables, columns, data types, constraints, and relationshi…_

2. _Business concept 'Product classification: FINISHED_GOOD, ASSEMBLY, COMPONENT' — Product classification: FINISHED_GOOD, ASSEMBLY, COMPONENT is implemented by physical table COMPONENT (columns: componen…_

3. _## bom  Bill of Materials defining product composition and hierarchical structure. Supports recursive relationships for multi-level assemblies.  | Column | Data Type | Constraints | Description | |---…_

---

### ✅ QA-032 — How do I check if sufficient inventory exists across all warehouses to fulfill a work order?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.4035 | **Gate:** `proceed`

**Expected answer:**
> For the work_order's product_id, perform recursive BOM explosion to get all required components with quantities. For each component, sum the available quantity (quantity_on_hand - quantity_reserved) across all warehouses from the inventory table. Compare aggregated available inventory against requir…

**System answer:**
> From the retrieved context, the schema-level way to check this is to start with `WORK_ORDER` and then inspect matching `INVENTORY` records for the same product across all warehouses.

Use `WORK_ORDER.work_order_id` to retrieve the work order row, then take its `product_id`, `quantity_ordered`, `quantity_completed`, `status`, and `warehouse_id`. To find stock for that product, look in `INVENTORY` w…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_5`, `parent_chunk_data_dictionary.md_6`, `Inventory stock levels for components and products at specific warehouse locations→INVENTORY`, `INVENTORY→WAREHOUSE`, `Work Order→WORK_ORDER`, `WORK_ORDER→WAREHOUSE`, `parent_chunk_data_dictionary.md_8`, `parent_chunk_business_glossary.md_1`

**Context previews (first 3):**

1. _## warehouse  Stores physical storage location information for inventory management.  | Column | Data Type | Constraints | Description | |--------|-----------|-------------|-------------| | warehouse_…_

2. _## work_order  Represents production jobs for manufacturing products with hierarchical work order support.  | Column | Data Type | Constraints | Description | |--------|-----------|-------------|-----…_

3. _Business concept 'Inventory stock levels for components and products at specific warehouse locations' is implemented by physical table INVENTORY (columns: inventory_id, warehouse_id, component_id, pro…_

---

### ✅ QA-033 — How can I find which quality control inspections failed for components from specific suppliers?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.4561 | **Gate:** `proceed`

**Expected answer:**
> Query the quality_control table filtering by result = 'FAIL'. Join with the batch table to get product_id and production_date. Join with the bom table recursively to trace which products contain failed components. Join with component_supplier and supplier tables to identify the source supplier. Filt…

**System answer:**
> From the retrieved context, the part that can be answered clearly is how to identify failed QC inspections, and the part that is not fully answerable is how to tie those inspections to specific components and suppliers.

Quality Control inspections are implemented by the physical table QUALITY_CONTROL, with columns qc_id, batch_id, specification_id, qc_date, qc_type, inspector_id, result, defect_c…

**Sources retrieved (12):** `Quality Control inspections→QUALITY_CONTROL`, `parent_chunk_data_dictionary.md_5`, `parent_chunk_data_dictionary.md_3`, `components they can provide through approved supplier relationships→COMPONENT_SUPPLIER`, `parent_chunk_data_dictionary.md_4`, `Inventory stock levels for components and products at specific warehouse locations→INVENTORY`, `COMPONENT_SUPPLIER→SUPPLIER`, `parent_chunk_business_glossary.md_2`

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
> From the retrieved context, the supported way to calculate this at the schema level is through the `WORK_ORDER` hierarchy, not through `ROUTE`.

`WORK_ORDER` explicitly supports decomposition through the self-referential column `parent_work_order`, which is a foreign key to `WORK_ORDER(work_order_id)`. That means you can start with one root work order and recursively find all child and lower-level…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_6`, `Work Order→WORK_ORDER`, `parent_chunk_data_dictionary.md_3`, `parent_chunk_data_dictionary.md_7`, `parent_chunk_data_dictionary.md_5`, `parent_chunk_data_dictionary.md_4`, `Route Step→ROUTE`, `parent_chunk_business_glossary.md_0`

**Context previews (first 3):**

1. _## work_order  Represents production jobs for manufacturing products with hierarchical work order support.  | Column | Data Type | Constraints | Description | |--------|-----------|-------------|-----…_

2. _Business concept 'Work Order' — The table is explicitly commented as WORK_ORDER and contains core manufacturing job fields such as product_id, quantities ordered/completed, status, priority, planned d…_

3. _# Manufacturing Data Dictionary  This data dictionary documents the database schema for the manufacturing supply chain system. It includes all tables, columns, data types, constraints, and relationshi…_

---

### ✅ QA-035 — How can I identify which shipments are overdue and their impact on work orders?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0719 | **Gate:** `proceed_with_warning`

**Expected answer:**
> Query the shipment table filtering for status = 'SHIPPED' where actual_arrival is NULL and estimated_arrival is in the past (overdue). Join with the component_supplier table via supplier_id and component_id to identify which components are delayed. Perform reverse BOM lookup to find which parent pro…

**System answer:**
> The retrieved context does not define an “overdue shipment” rule, so I cannot tell you which shipments are overdue from the knowledge graph alone. What the context does provide for `SHIPMENT` is the schema needed to apply a rule if your organization already has one: `shipment_id`, `shipment_type` (`INBOUND`, `OUTBOUND`, `INTERNAL`), `warehouse_id`, `supplier_id`, `customer_id`, `ship_date`, `estim…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_5`, `parent_chunk_data_dictionary.md_8`, `parent_chunk_data_dictionary.md_6`, `Shipment`, `Shipment→SHIPMENT`, `Work Order→WORK_ORDER`, `WORK_ORDER→PRODUCT`, `WORK_ORDER→WAREHOUSE`

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
> Use `BATCH` to identify the expiry side of the problem, and then trace the batched product toward its component-supplier relationships as far as the schema allows.

`BATCH` is the production-lot table for this. It contains `batch_id`, `product_id`, `production_date`, `quantity_produced`, `warehouse_id`, `expiry_date`, and `qc_status`. To find expired batches, filter on `BATCH.expiry_date` being be…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_5`, `Inventory stock levels for components and products at specific warehouse locations→INVENTORY`, `parent_chunk_data_dictionary.md_7`, `parent_chunk_data_dictionary.md_3`, `Production batch reference→BATCH`, `parent_chunk_data_dictionary.md_8`, `components they can provide through approved supplier relationships→COMPONENT_SUPPLIER`, `parent_chunk_business_glossary.md_2`

**Context previews (first 3):**

1. _## warehouse  Stores physical storage location information for inventory management.  | Column | Data Type | Constraints | Description | |--------|-----------|-------------|-------------| | warehouse_…_

2. _Business concept 'Inventory stock levels for components and products at specific warehouse locations' is implemented by physical table INVENTORY (columns: inventory_id, warehouse_id, component_id, pro…_

3. _## specification  Defines technical requirements and acceptance criteria for materials and products.  | Column | Data Type | Constraints | Description | |--------|-----------|-------------|-----------…_

---

### ✅ QA-037 — How can I generate a material requirements plan showing when to order components based on work order schedules?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0433 | **Gate:** `proceed_with_warning`

**Expected answer:**
> Query all work_orders with status 'PENDING' ordered by planned_start_date. For each work_order, perform BOM explosion to get required components and quantities. For each component, query inventory for current available stock across warehouses. Calculate net requirements = (required quantity * work_o…

**System answer:**
> You can generate this at the schema level by using `WORK_ORDER` as the schedule source and joining it to `BOM`, `PRODUCT`, `INVENTORY`, and `WAREHOUSE`.

Start from `WORK_ORDER`, because it contains the production schedule and demand-driving fields: `work_order_id`, `product_id`, `quantity_ordered`, `quantity_completed`, `status`, `priority`, `planned_start_date`, `planned_end_date`, `warehouse_id…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_6`, `parent_chunk_data_dictionary.md_7`, `Work Order→WORK_ORDER`, `parent_chunk_data_dictionary.md_5`, `parent_chunk_data_dictionary.md_4`, `parent_chunk_data_dictionary.md_3`, `components they can provide through approved supplier relationships→COMPONENT_SUPPLIER`, `Inventory stock levels for components and products at specific warehouse locations→INVENTORY`

**Context previews (first 3):**

1. _## work_order  Represents production jobs for manufacturing products with hierarchical work order support.  | Column | Data Type | Constraints | Description | |--------|-----------|-------------|-----…_

2. _## specification  Defines technical requirements and acceptance criteria for materials and products.  | Column | Data Type | Constraints | Description | |--------|-----------|-------------|-----------…_

3. _Business concept 'Work Order' — The table is explicitly commented as WORK_ORDER and contains core manufacturing job fields such as product_id, quantities ordered/completed, status, priority, planned d…_

---

### ✅ QA-038 — How do I trace the complete genealogy of a component from supplier through batch to finished goods?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0748 | **Gate:** `proceed_with_warning`

**Expected answer:**
> Start with a shipment from the supplier (shipment table with supplier_id and shipment_type = 'INBOUND'). Track to inventory updates via component_id and warehouse_id. Identify batches that consumed the component via reverse BOM lookup (batch.product_id → bom hierarchy → component_id). Query quality_…

**System answer:**
> From the retrieved context, you can only trace this genealogy partially at the schema level.

The supplier side starts with `COMPONENT_SUPPLIER`, which stores approved supplier relationships for a component using `component_id`, `supplier_id`, `is_preferred`, `lead_time_days`, and `unit_price`. The supplier master is `supplier`, whose key is `supplier_id`. The component master is `component`, whos…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_3`, `Product classification: FINISHED_GOOD, ASSEMBLY, COMPONENT→COMPONENT`, `parent_chunk_data_dictionary.md_7`, `parent_chunk_data_dictionary.md_5`, `parent_chunk_data_dictionary.md_8`, `parent_chunk_data_dictionary.md_4`, `components they can provide through approved supplier relationships→COMPONENT_SUPPLIER`, `COMPONENT_SUPPLIER→COMPONENT`

**Context previews (first 3):**

1. _# Manufacturing Data Dictionary  This data dictionary documents the database schema for the manufacturing supply chain system. It includes all tables, columns, data types, constraints, and relationshi…_

2. _Business concept 'Product classification: FINISHED_GOOD, ASSEMBLY, COMPONENT' — Product classification: FINISHED_GOOD, ASSEMBLY, COMPONENT is implemented by physical table COMPONENT (columns: componen…_

3. _## specification  Defines technical requirements and acceptance criteria for materials and products.  | Column | Data Type | Constraints | Description | |--------|-----------|-------------|-----------…_

---

### ✅ QA-039 — How can I find alternative suppliers for components that are critical for multiple products?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0772 | **Gate:** `proceed_with_warning`

**Expected answer:**
> Perform BOM explosion for all active products and count component usage frequency. Identify high-frequency components. Query component_supplier table to find all suppliers for these components. Filter to suppliers with rating >= 4.0 (high quality) and is_preferred = 'Y'. For each component, list alt…

**System answer:**
> From the retrieved context, this can only be answered partially at the schema level.

What is known is that product-to-component usage across multiple products is modeled in `bom`. In that table, `parent_product_id` is the product being built, and `component_product_id` is the product used as a component. So, to identify items used in multiple products, you would use `bom` and look for the same `c…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_4`, `parent_chunk_data_dictionary.md_3`, `components they can provide through approved supplier relationships→COMPONENT_SUPPLIER`, `Preferred supplier for this component→SUPPLIER`, `parent_chunk_data_dictionary.md_5`, `parent_chunk_data_dictionary.md_8`, `parent_chunk_data_dictionary.md_7`, `parent_chunk_business_glossary.md_0`

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
> From the retrieved context, there is no explicit landed-cost formula or procedure, and there is no table that stores manufacturing operation costs, labor costs, overhead, freight, duties, or other standard landed-cost elements. But the context does provide the schema pieces you can use for a partial calculation at the schema level.

For the product itself, the `product` table contains `product_id`…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_3`, `components they can provide through approved supplier relationships→COMPONENT_SUPPLIER`, `the product produced, production date, quantity produced, warehouse location, expiry date (if applicable), and quality control status→PRODUCT`, `parent_chunk_data_dictionary.md_6`, `parent_chunk_data_dictionary.md_7`, `parent_chunk_data_dictionary.md_5`, `parent_chunk_data_dictionary.md_8`, `parent_chunk_data_dictionary.md_4`

**Context previews (first 3):**

1. _# Manufacturing Data Dictionary  This data dictionary documents the database schema for the manufacturing supply chain system. It includes all tables, columns, data types, constraints, and relationshi…_

2. _Business concept 'components they can provide through approved supplier relationships' is implemented by physical table COMPONENT_SUPPLIER (columns: component_supplier_id, component_id, supplier_id, i…_

3. _Business concept 'the product produced, production date, quantity produced, warehouse location, expiry date (if applicable), and quality control status' is implemented by physical table PRODUCT (colum…_

---

## Anomalies & Observations

No anomalies detected. All questions grounded with acceptable RAGAS scores.
