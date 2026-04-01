# AB-14 — 04_complex_manufacturing — Run Analysis

**Timestamp:** 2026-04-01 05:47:32  
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
| Triplets extracted | 360 |
| Entities resolved | 121 |
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
> In the manufacturing system, the `product` table stores core information about manufactured items. A product represents any manufactured item in the system, including finished goods, sub-assemblies, and components.

The stored product attributes are:
`product_id`, the unique product identifier; `product_name`, the product name; `product_type`, which classifies the product as `FINISHED_GOOD`, `ASSE…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_3`, `parent_chunk_data_dictionary.md_6`, `parent_chunk_data_dictionary.md_5`, `parent_chunk_data_dictionary.md_7`, `parent_chunk_business_glossary.md_0`, `parent_chunk_business_glossary.md_1`, `parent_chunk_business_glossary.md_2`, `Production Batches→BATCH`

**Context previews (first 3):**

1. _# Manufacturing Data Dictionary  This data dictionary documents the database schema for the manufacturing supply chain system. It includes all tables, columns, data types, constraints, and relationshi…_

2. _## work_order  Represents production jobs for manufacturing products with hierarchical work order support.  | Column | Data Type | Constraints | Description | |--------|-----------|-------------|-----…_

3. _## warehouse  Stores physical storage location information for inventory management.  | Column | Data Type | Constraints | Description | |--------|-----------|-------------|-------------| | warehouse_…_

---

### ✅ QA-002 — How are components defined in the manufacturing database?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.5910 | **Gate:** `proceed`

**Expected answer:**
> Components are defined with a unique identifier (component_id), descriptive name (component_name), category grouping (component_category), unit of measure (unit_of_measure), standard unit cost (standard_cost), and optional reference to technical specifications (specification_id). Components represen…

**System answer:**
> Components are defined in the business glossary as atomic raw materials or purchased parts that cannot be further broken down into simpler manufactured items. They are the building blocks used in manufacturing and are procured from external suppliers.

In the database metadata provided, components are represented in several related ways:

The physical table COMPONENT is shown with columns componen…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_3`, `parent_chunk_data_dictionary.md_4`, `components they can provide through approved supplier relationships→COMPONENT_SUPPLIER`, `parent_chunk_data_dictionary.md_5`, `BOM entry→BOM`, `Actual stock levels of components and products at specific warehouse locations→INVENTORY`, `parent_chunk_business_glossary.md_0`, `parent_chunk_business_glossary.md_1`

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
> The Bill of Materials (`bom`) table defines product composition and hierarchical structure. It records which component products go into a parent product, including the required quantity, unit of measure, hierarchy depth (`bom_level`), and whether a component is optional.

Its purpose is to support multi-level assemblies through recursive product relationships: both `parent_product_id` and `compone…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_4`, `BOM→PRODUCT`, `BOM entry→BOM`, `parent_chunk_data_dictionary.md_3`, `parent_chunk_data_dictionary.md_7`, `parent_chunk_data_dictionary.md_8`, `parent_chunk_business_glossary.md_0`, `parent_chunk_business_glossary.md_1`

**Context previews (first 3):**

1. _## bom  Bill of Materials defining product composition and hierarchical structure. Supports recursive relationships for multi-level assemblies.  | Column | Data Type | Constraints | Description | |---…_

2. _Relationship: BOM references PRODUCT via foreign key COMPONENT_PRODUCT_ID -> PRODUCT.PRODUCT_ID.…_

3. _Business concept 'BOM entry' is implemented by physical table BOM (columns: bom_id, parent_product_id, component_product_id, quantity, unit_of_measure, bom_level, is_optional).…_

---

### ✅ QA-004 — What supplier information does the system maintain?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.2801 | **Gate:** `proceed`

**Expected answer:**
> Suppliers are tracked with a unique identifier (supplier_id), legal business name (supplier_name), primary contact email (contact_email), primary contact phone number (contact_phone), performance rating from 1.0 to 5.0 (rating), and preferred supplier status flag (is_preferred).

**System answer:**
> The system maintains supplier master data in the `SUPPLIER` table. Based on the `Supplier Evaluation Profile` concept, this includes supplier identity, procurement contact details, and evaluation attributes. The recorded fields are `supplier_id`, `supplier_name`, `contact_email`, `contact_phone`, `rating`, and `is_preferred`.

The context also shows supplier-related relationship data in other tabl…

**Sources retrieved (12):** `Supplier Evaluation Profile→SUPPLIER`, `parent_chunk_data_dictionary.md_4`, `SHIPMENT→SUPPLIER`, `components they can provide through approved supplier relationships→COMPONENT_SUPPLIER`, `Shipment`, `parent_chunk_data_dictionary.md_8`, `COMPONENT_SUPPLIER→SUPPLIER`, `Shipment→SHIPMENT`

**Context previews (first 3):**

1. _Business concept 'Supplier Evaluation Profile' — The table stores supplier master identity data plus evaluation attributes, specifically a performance rating and preferred status, along with procureme…_

2. _## bom  Bill of Materials defining product composition and hierarchical structure. Supports recursive relationships for multi-level assemblies.  | Column | Data Type | Constraints | Description | |---…_

3. _Relationship: SHIPMENT references SUPPLIER via foreign key SUPPLIER_ID -> SUPPLIER.SUPPLIER_ID.…_

---

### ✅ QA-005 — How are warehouses represented in the schema?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.3381 | **Gate:** `proceed`

**Expected answer:**
> Warehouses are defined with a unique identifier (warehouse_id), descriptive name (warehouse_name), full street address (address), city location (city), state or province (state), total storage capacity in cubic meters (capacity), and optional manager identifier (manager_id).

**System answer:**
> Warehouses are represented by the physical table `warehouse`.

In the schema, `warehouse` stores physical storage location information for inventory management and represents a physical location where materials, components, and finished goods are stored. It serves as a supply chain node where inventory is held, shipments are received, and products are staged for production or distribution.

The `w…

**Sources retrieved (12):** `INVENTORY→WAREHOUSE`, `BATCH→WAREHOUSE`, `WORK_ORDER→WAREHOUSE`, `SHIPMENT→WAREHOUSE`, `parent_chunk_data_dictionary.md_6`, `parent_chunk_data_dictionary.md_5`, `Shipment`, `Actual stock levels of components and products at specific warehouse locations→WAREHOUSE`

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
> The INVENTORY table tracks the actual stock levels of components and products at specific warehouse locations.

From the context, each inventory record represents stock in a warehouse and includes:
inventory_id as the unique inventory record identifier, warehouse_id for the warehouse location, component_id or product_id as the item being stocked, quantity_on_hand, quantity_reserved, reorder_thresh…

**Sources retrieved (12):** `INVENTORY→PRODUCT`, `INVENTORY→WAREHOUSE`, `INVENTORY→COMPONENT`, `Actual stock levels of components and products at specific warehouse locations→INVENTORY`, `parent_chunk_data_dictionary.md_5`, `Production Batches→BATCH`, `parent_chunk_data_dictionary.md_7`, `parent_chunk_data_dictionary.md_8`

**Context previews (first 3):**

1. _Relationship: INVENTORY references PRODUCT via foreign key PRODUCT_ID -> PRODUCT.PRODUCT_ID.…_

2. _Relationship: INVENTORY references WAREHOUSE via foreign key WAREHOUSE_ID -> WAREHOUSE.WAREHOUSE_ID.…_

3. _Relationship: INVENTORY references COMPONENT via foreign key COMPONENT_ID -> COMPONENT.COMPONENT_ID.…_

---

### ✅ QA-007 — How are work orders structured in the manufacturing system?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.4854 | **Gate:** `proceed`

**Expected answer:**
> Work orders represent production jobs with a unique identifier (work_order_id), product to be manufactured (product_id), optional parent work order for nested hierarchies (parent_work_order), quantity to produce (quantity_ordered), quantity completed so far (quantity_completed), current status (PEND…

**System answer:**
> Work orders are structured through the `WORK_ORDER` table, which represents production jobs for manufacturing products and explicitly supports hierarchical production planning and tracking.

Each work order is identified by `work_order_id` as the primary key. A work order is tied to the product being manufactured through `product_id`, which is required and references `PRODUCT.PRODUCT_ID`. It can a…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_6`, `Hierarchical production planning and tracking→WORK_ORDER`, `WORK_ORDER→PRODUCT`, `WORK_ORDER→WORK_ORDER`, `parent_chunk_data_dictionary.md_3`, `WORK_ORDER→WAREHOUSE`, `parent_chunk_data_dictionary.md_8`, `parent_chunk_data_dictionary.md_7`

**Context previews (first 3):**

1. _## work_order  Represents production jobs for manufacturing products with hierarchical work order support.  | Column | Data Type | Constraints | Description | |--------|-----------|-------------|-----…_

2. _Business concept 'Hierarchical production planning and tracking' is implemented by physical table WORK_ORDER (columns: work_order_id, product_id, parent_work_order, quantity_ordered, quantity_complete…_

3. _Relationship: WORK_ORDER references PRODUCT via foreign key PRODUCT_ID -> PRODUCT.PRODUCT_ID.…_

---

### ✅ QA-008 — What information is captured in the shipment table?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.9788 | **Gate:** `proceed`

**Expected answer:**
> Shipments track material transfers with a unique identifier (shipment_id), shipment type (INBOUND from suppliers, OUTBOUND to customers, INTERNAL between warehouses), destination warehouse (warehouse_id), source supplier for inbound (supplier_id), destination customer for outbound (customer_id), shi…

**System answer:**
> The `shipment` table captures material transfer information between warehouses, suppliers, and customers. In `SHIPMENT`, it stores `shipment_id` as the unique identifier; `shipment_type`, which is `INBOUND`, `OUTBOUND`, or `INTERNAL`; `warehouse_id` as the warehouse reference; `supplier_id` as the supplier reference for inbound shipments; `customer_id` as the customer reference for outbound shipme…

**Sources retrieved (12):** `Shipment`, `Shipment→SHIPMENT`, `SHIPMENT→WAREHOUSE`, `SHIPMENT→SUPPLIER`, `parent_chunk_data_dictionary.md_8`, `parent_chunk_data_dictionary.md_5`, `parent_chunk_business_glossary.md_0`, `parent_chunk_business_glossary.md_1`

**Context previews (first 3):**

1. _Shipment: The table is explicitly labeled as SHIPMENT and contains shipment-specific fields such as shipment_type, ship_date, estimated_arrival, actual_arrival, and status. Foreign keys to warehouse a…_

2. _Business concept 'Shipment' — The table is explicitly labeled as SHIPMENT and contains shipment-specific fields such as shipment_type, ship_date, estimated_arrival, actual_arrival, and status. Foreign…_

3. _Relationship: SHIPMENT references WAREHOUSE via foreign key WAREHOUSE_ID -> WAREHOUSE.WAREHOUSE_ID.…_

---

### ✅ QA-009 — How does the quality control system record inspections?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.9540 | **Gate:** `proceed`

**Expected answer:**
> Quality control records are stored with a unique identifier (qc_id), associated production batch (batch_id), applicable specification requirements (specification_id), inspection date (qc_date), inspection type (INCOMING for supplier materials, IN_PROCESS during manufacturing, FINAL for finished good…

**System answer:**
> The quality control system records inspections in the physical table QUALITY_CONTROL, which implements the business concept “inspection and testing records for quality assurance.”

Each inspection is stored as a QC record with these columns: qc_id, batch_id, specification_id, qc_date, qc_type, inspector_id, result, defect_count, and notes. From the business description, this means the system captu…

**Sources retrieved (12):** `inspection and testing records for quality assurance→QUALITY_CONTROL`, `BOM→PRODUCT`, `parent_chunk_data_dictionary.md_3`, `BATCH→PRODUCT`, `parent_chunk_business_glossary.md_2`, `inspection and testing records for quality assurance`, `parent_chunk_business_glossary.md_0`, `parent_chunk_business_glossary.md_1`

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
> Specification records define technical requirements and acceptance criteria for materials and products.

From the Specification concept and table metadata, they include the specification name, version, effective date, specification type, the critical parameter being tested, minimum and maximum acceptable values, and the unit of measure. The specification type values are DIMENSIONAL, MATERIAL, and …

**Sources retrieved (12):** `inspection and testing records for quality assurance→QUALITY_CONTROL`, `parent_chunk_data_dictionary.md_7`, `Specifications for quality requirements→SPECIFICATION`, `parent_chunk_data_dictionary.md_3`, `Product classification: FINISHED_GOOD, ASSEMBLY, COMPONENT→COMPONENT`, `parent_chunk_business_glossary.md_2`, `parent_chunk_business_glossary.md_0`, `inspection and testing records for quality assurance`

**Context previews (first 3):**

1. _Business concept 'inspection and testing records for quality assurance' is implemented by physical table QUALITY_CONTROL (columns: qc_id, batch_id, specification_id, qc_date, qc_type, inspector_id, re…_

2. _## specification  Defines technical requirements and acceptance criteria for materials and products.  | Column | Data Type | Constraints | Description | |--------|-----------|-------------|-----------…_

3. _Business concept 'Specifications for quality requirements' is implemented by physical table SPECIFICATION (columns: specification_id, specification_name, version, effective_date, spec_type, critical_p…_

---

### ✅ QA-011 — How can I find which suppliers provide specific components?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.3227 | **Gate:** `proceed`

**Expected answer:**
> Query the component_supplier table which links components to their approved suppliers. This table contains the component identifier (component_id), supplier identifier (supplier_id), preferred supplier flag (is_preferred), lead time in days (lead_time_days), and unit price (unit_price). Join with th…

**System answer:**
> Use the `COMPONENT_SUPPLIER` table. The business concept “components they can provide through approved supplier relationships” is implemented by `COMPONENT_SUPPLIER`, which contains `component_id`, `supplier_id`, `is_preferred`, `lead_time_days`, and `unit_price`.

Schema path:
`COMPONENT` → `COMPONENT_SUPPLIER` → `SUPPLIER`

The relationships are:
`COMPONENT_SUPPLIER.COMPONENT_ID` → `COMPONENT.CO…

**Sources retrieved (12):** `components they can provide through approved supplier relationships→COMPONENT_SUPPLIER`, `parent_chunk_data_dictionary.md_5`, `parent_chunk_data_dictionary.md_4`, `parent_chunk_data_dictionary.md_3`, `Actual stock levels of components and products at specific warehouse locations→INVENTORY`, `Actual stock levels of components and products at specific warehouse locations→WAREHOUSE`, `parent_chunk_data_dictionary.md_8`, `components they can provide through approved supplier relationships`

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
> To trace which components are needed for a work order, start with `WORK_ORDER`. The key link is `WORK_ORDER.product_id -> PRODUCT.product_id`, because `work_order` stores the product to manufacture. From that product, trace downward through the product structure. The retrieved context shows two mechanisms for this decomposition: `PRODUCT.parent_product_id -> PRODUCT.product_id`, which supports mul…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_5`, `Hierarchical production planning and tracking→WORK_ORDER`, `parent_chunk_data_dictionary.md_6`, `Actual stock levels of components and products at specific warehouse locations→INVENTORY`, `parent_chunk_data_dictionary.md_3`, `components they can provide through approved supplier relationships→COMPONENT_SUPPLIER`, `parent_chunk_data_dictionary.md_8`, `parent_chunk_data_dictionary.md_7`

**Context previews (first 3):**

1. _## warehouse  Stores physical storage location information for inventory management.  | Column | Data Type | Constraints | Description | |--------|-----------|-------------|-------------| | warehouse_…_

2. _Business concept 'Hierarchical production planning and tracking' is implemented by physical table WORK_ORDER (columns: work_order_id, product_id, parent_work_order, quantity_ordered, quantity_complete…_

3. _## work_order  Represents production jobs for manufacturing products with hierarchical work order support.  | Column | Data Type | Constraints | Description | |--------|-----------|-------------|-----…_

---

### ✅ QA-013 — How can I identify which warehouses have available inventory for specific components?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.8728 | **Gate:** `proceed`

**Expected answer:**
> Query the inventory table filtered by component_id, joining with the warehouse table to get warehouse names and locations. Calculate available quantity as quantity_on_hand minus quantity_reserved. Filter for records where available quantity is greater than zero. Results show warehouse names, locatio…

**System answer:**
> At the schema level, you would use the INVENTORY table to find the warehouse locations associated with a specific component. INVENTORY tracks stock levels of components and products at specific warehouse locations, and it links those entities through these keys: INVENTORY.component_id → COMPONENT.component_id and INVENTORY.warehouse_id → WAREHOUSE.warehouse_id.

So the trace is: filter INVENTORY b…

**Sources retrieved (12):** `Actual stock levels of components and products at specific warehouse locations→INVENTORY`, `parent_chunk_data_dictionary.md_5`, `Actual stock levels of components and products at specific warehouse locations→WAREHOUSE`, `INVENTORY→WAREHOUSE`, `INVENTORY→COMPONENT`, `parent_chunk_data_dictionary.md_3`, `parent_chunk_data_dictionary.md_8`, `parent_chunk_data_dictionary.md_6`

**Context previews (first 3):**

1. _Business concept 'Actual stock levels of components and products at specific warehouse locations' is implemented by physical table INVENTORY (columns: inventory_id, warehouse_id, component_id, product…_

2. _## warehouse  Stores physical storage location information for inventory management.  | Column | Data Type | Constraints | Description | |--------|-----------|-------------|-------------| | warehouse_…_

3. _Business concept 'Actual stock levels of components and products at specific warehouse locations' is implemented by physical table WAREHOUSE (columns: warehouse_id, warehouse_name, address, city, stat…_

---

### ✅ QA-014 — How do I find which shipments delivered materials from a specific supplier?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.3983 | **Gate:** `proceed`

**Expected answer:**
> Query the shipment table filtering by supplier_id and shipment_type = 'INBOUND'. Join with the warehouse table to show destination warehouses. Filter for status = 'DELIVERED' and include actual_arrival date. Results can be ordered by ship_date descending to show most recent deliveries first.

**System answer:**
> Use the `shipment` table, because it tracks material transfers between warehouses, suppliers, and customers.

To find shipments that delivered materials from a specific supplier, the schema-level logic is:

Join/filter on `shipment.supplier_id`, since `SHIPMENT` references `SUPPLIER` via `SUPPLIER_ID -> SUPPLIER.SUPPLIER_ID`.

Then restrict to shipments that are:
- from a supplier: `shipment_type …

**Sources retrieved (12):** `Shipment`, `parent_chunk_data_dictionary.md_8`, `Shipment→SHIPMENT`, `SHIPMENT→SUPPLIER`, `parent_chunk_data_dictionary.md_5`, `Actual stock levels of components and products at specific warehouse locations→INVENTORY`, `parent_chunk_data_dictionary.md_7`, `parent_chunk_data_dictionary.md_3`

**Context previews (first 3):**

1. _Shipment: The table is explicitly labeled as SHIPMENT and contains shipment-specific fields such as shipment_type, ship_date, estimated_arrival, actual_arrival, and status. Foreign keys to warehouse a…_

2. _## shipment  Tracks material transfers between warehouses, suppliers, and customers.  | Column | Data Type | Constraints | Description | |--------|-----------|-------------|-------------| | shipment_i…_

3. _Business concept 'Shipment' — The table is explicitly labeled as SHIPMENT and contains shipment-specific fields such as shipment_type, ship_date, estimated_arrival, actual_arrival, and status. Foreign…_

---

### ✅ QA-015 — How can I determine which quality control inspections were performed on a specific production batch?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.9779 | **Gate:** `proceed`

**Expected answer:**
> Query the quality_control table filtered by batch_id. Join with the specification table to get requirement details (specification_name, spec_type, acceptable ranges). Include qc_date, qc_type (INCOMING, IN_PROCESS, FINAL), result (PASS, FAIL, CONDITIONAL), and defect_count. This shows the complete i…

**System answer:**
> Use the `QUALITY_CONTROL` table, which implements the business concept “inspection and testing records for quality assurance” and is described as storing inspection and testing records for quality assurance.

To find the inspections for a specific production batch, match the target batch’s `BATCH.batch_id` to `QUALITY_CONTROL.batch_id`. The direct schema path is:

`BATCH.batch_id` → `QUALITY_CONTR…

**Sources retrieved (12):** `inspection and testing records for quality assurance→QUALITY_CONTROL`, `Production Batches→BATCH`, `parent_chunk_data_dictionary.md_7`, `BATCH→PRODUCT`, `parent_chunk_data_dictionary.md_5`, `parent_chunk_data_dictionary.md_6`, `parent_chunk_data_dictionary.md_3`, `parent_chunk_business_glossary.md_2`

**Context previews (first 3):**

1. _Business concept 'inspection and testing records for quality assurance' is implemented by physical table QUALITY_CONTROL (columns: qc_id, batch_id, specification_id, qc_date, qc_type, inspector_id, re…_

2. _Business concept 'Production Batches' — The table is explicitly labeled as a batch/production lots entity and includes batch_id, product_id, production_date, quantity_produced, warehouse_id, expiry_da…_

3. _## specification  Defines technical requirements and acceptance criteria for materials and products.  | Column | Data Type | Constraints | Description | |--------|-----------|-------------|-----------…_

---

### ✅ QA-016 — How do I track which work orders are in progress at a specific warehouse?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.7311 | **Gate:** `proceed`

**Expected answer:**
> Query the work_order table filtering by warehouse_id and status = 'IN_PROGRESS'. Join with the product table to get product names and types. Include quantity_ordered, quantity_completed, priority, planned_end_date, and calculate progress percentage as (quantity_completed / quantity_ordered * 100). O…

**System answer:**
> Use the `WORK_ORDER` table, because it stores the production job, its current `status`, and its `warehouse_id` production location.

To find work orders that are currently in progress at a specific warehouse, filter `WORK_ORDER` where:
`status = 'IN_PROGRESS'`
and `warehouse_id = <target warehouse_id>`.

If you also want warehouse details, join:
`WORK_ORDER.warehouse_id -> WAREHOUSE.warehouse_id`.…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_5`, `parent_chunk_data_dictionary.md_6`, `Hierarchical production planning and tracking→WORK_ORDER`, `WORK_ORDER→WAREHOUSE`, `Actual stock levels of components and products at specific warehouse locations→INVENTORY`, `Actual stock levels of components and products at specific warehouse locations→WAREHOUSE`, `parent_chunk_data_dictionary.md_8`, `parent_chunk_data_dictionary.md_7`

**Context previews (first 3):**

1. _## warehouse  Stores physical storage location information for inventory management.  | Column | Data Type | Constraints | Description | |--------|-----------|-------------|-------------| | warehouse_…_

2. _## work_order  Represents production jobs for manufacturing products with hierarchical work order support.  | Column | Data Type | Constraints | Description | |--------|-----------|-------------|-----…_

3. _Business concept 'Hierarchical production planning and tracking' is implemented by physical table WORK_ORDER (columns: work_order_id, product_id, parent_work_order, quantity_ordered, quantity_complete…_

---

### ✅ QA-017 — How can I find which components need reordering based on current inventory levels?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.5270 | **Gate:** `proceed`

**Expected answer:**
> Query the inventory table and filter where quantity_on_hand minus quantity_reserved is less than reorder_threshold. Join with the component table to get component names, categories, and standard costs. Join with the warehouse table for location information. Results identify which components are belo…

**System answer:**
> Use the INVENTORY table, because the business concept “Actual stock levels of components and products at specific warehouse locations” is implemented there. For reordering components specifically, look at INVENTORY records where component_id is populated, since the schema states that an inventory record supports either a component or a product, but not both.

The relevant INVENTORY columns are com…

**Sources retrieved (12):** `Actual stock levels of components and products at specific warehouse locations→INVENTORY`, `parent_chunk_data_dictionary.md_5`, `Actual stock levels of components and products at specific warehouse locations→WAREHOUSE`, `INVENTORY→COMPONENT`, `parent_chunk_data_dictionary.md_3`, `parent_chunk_data_dictionary.md_7`, `parent_chunk_data_dictionary.md_4`, `parent_chunk_data_dictionary.md_6`

**Context previews (first 3):**

1. _Business concept 'Actual stock levels of components and products at specific warehouse locations' is implemented by physical table INVENTORY (columns: inventory_id, warehouse_id, component_id, product…_

2. _## warehouse  Stores physical storage location information for inventory management.  | Column | Data Type | Constraints | Description | |--------|-----------|-------------|-------------| | warehouse_…_

3. _Business concept 'Actual stock levels of components and products at specific warehouse locations' is implemented by physical table WAREHOUSE (columns: warehouse_id, warehouse_name, address, city, stat…_

---

### ✅ QA-018 — How do I determine the manufacturing route for a specific product?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0413 | **Gate:** `proceed_with_warning`

**Expected answer:**
> Query the route table filtering by product_id, ordered by sequence_number ascending. For each operation, retrieve operation_name, work_center, cycle_time_minutes, and setup_time_minutes. Join with the product table to get product details. The sequence of operations shows the complete manufacturing w…

**System answer:**
> To determine the manufacturing route for a specific product, use the `ROUTE` table linked to `PRODUCT` by `product_id`.

The retrieved context states that `ROUTE` references `PRODUCT` via the foreign key `PRODUCT_ID -> PRODUCT.PRODUCT_ID`. It also defines `ROUTE` as the implementation of the business concept “Routing Step,” with columns `route_id`, `product_id`, `route_name`, `sequence_number`, `o…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_6`, `ROUTE→PRODUCT`, `parent_chunk_data_dictionary.md_3`, `parent_chunk_data_dictionary.md_7`, `Routing Step→ROUTE`, `parent_chunk_data_dictionary.md_8`, `Hierarchical production planning and tracking→WORK_ORDER`, `parent_chunk_data_dictionary.md_4`

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
> Use the BATCH table directly. The retrieved context shows that BATCH includes batch_id, product_id, production_date, quantity_produced, warehouse_id, expiry_date, and qc_status, and that BATCH references WAREHOUSE through warehouse_id → WAREHOUSE.warehouse_id.

So to find which batches are stored at a specific warehouse and their QC status, filter BATCH by the target warehouse_id and return at lea…

**Sources retrieved (12):** `Production Batches→BATCH`, `parent_chunk_data_dictionary.md_5`, `Actual stock levels of components and products at specific warehouse locations→INVENTORY`, `Actual stock levels of components and products at specific warehouse locations→WAREHOUSE`, `BATCH→WAREHOUSE`, `inspection and testing records for quality assurance→QUALITY_CONTROL`, `parent_chunk_data_dictionary.md_6`, `parent_chunk_data_dictionary.md_8`

**Context previews (first 3):**

1. _Business concept 'Production Batches' — The table is explicitly labeled as a batch/production lots entity and includes batch_id, product_id, production_date, quantity_produced, warehouse_id, expiry_da…_

2. _## warehouse  Stores physical storage location information for inventory management.  | Column | Data Type | Constraints | Description | |--------|-----------|-------------|-------------| | warehouse_…_

3. _Business concept 'Actual stock levels of components and products at specific warehouse locations' is implemented by physical table INVENTORY (columns: inventory_id, warehouse_id, component_id, product…_

---

### ✅ QA-020 — How do I identify which specifications apply to specific components?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.2550 | **Gate:** `proceed`

**Expected answer:**
> Query the component table and join with the specification table via specification_id. Include component_name, component_category, and specification details (specification_name, spec_type, critical_parameter, min_value, max_value, unit_of_measure). This shows the technical requirements that each comp…

**System answer:**
> To identify which specifications apply to specific components, use the `COMPONENT` table’s `specification_id` column and join it to `SPECIFICATION.specification_id`.

The schema-level path is:

`COMPONENT.specification_id` → `SPECIFICATION.specification_id`

From the retrieved context, the `COMPONENT` table includes these relevant columns: `component_id`, `component_name`, `component_category`, `u…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_5`, `parent_chunk_data_dictionary.md_7`, `Product classification: FINISHED_GOOD, ASSEMBLY, COMPONENT→COMPONENT`, `Actual stock levels of components and products at specific warehouse locations→INVENTORY`, `parent_chunk_data_dictionary.md_3`, `Actual stock levels of components and products at specific warehouse locations→WAREHOUSE`, `parent_chunk_data_dictionary.md_4`, `Specifications for quality requirements→SPECIFICATION`

**Context previews (first 3):**

1. _## warehouse  Stores physical storage location information for inventory management.  | Column | Data Type | Constraints | Description | |--------|-----------|-------------|-------------| | warehouse_…_

2. _## specification  Defines technical requirements and acceptance criteria for materials and products.  | Column | Data Type | Constraints | Description | |--------|-----------|-------------|-----------…_

3. _Business concept 'Product classification: FINISHED_GOOD, ASSEMBLY, COMPONENT' is implemented by physical table COMPONENT (columns: component_id, component_name, component_category, unit_of_measure, st…_

---

### ✅ QA-021 — How can I perform a complete BOM explosion to find all components required for a finished product?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.3509 | **Gate:** `proceed`

**Expected answer:**
> Use a recursive query starting from the product_id of the finished good. At each level, join the bom table to find component_product_id entries. For each component, check if product_type is 'ASSEMBLY' or 'FINISHED_GOOD'. If so, recursively query bom again using that component_product_id as the new p…

**System answer:**
> To perform a complete BOM explosion for a finished product, use the `bom` table recursively starting from the finished product’s `product.product_id`.

The core schema path is:

`product.product_id` → `bom.parent_product_id` → `bom.component_product_id` → `product.product_id`

This works because the `bom` table stores each parent-child material relationship, and both `parent_product_id` and `compo…

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
> From the retrieved schema, the supported way to calculate a rolled-up material cost is to explode the product structure through `bom` and join each BOM component back to `product` for cost.

Use this path: start with the target row in `product` using `product.product_id`. Find its direct components in `bom` with `bom.parent_product_id = product.product_id`. For each BOM row, join `bom.component_pr…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_3`, `parent_chunk_data_dictionary.md_4`, `Product classification: FINISHED_GOOD, ASSEMBLY, COMPONENT→COMPONENT`, `parent_chunk_data_dictionary.md_7`, `parent_chunk_data_dictionary.md_8`, `parent_chunk_data_dictionary.md_6`, `parent_chunk_data_dictionary.md_5`, `(product_id, sequence_number)→PRODUCT`

**Context previews (first 3):**

1. _# Manufacturing Data Dictionary  This data dictionary documents the database schema for the manufacturing supply chain system. It includes all tables, columns, data types, constraints, and relationshi…_

2. _## bom  Bill of Materials defining product composition and hierarchical structure. Supports recursive relationships for multi-level assemblies.  | Column | Data Type | Constraints | Description | |---…_

3. _Business concept 'Product classification: FINISHED_GOOD, ASSEMBLY, COMPONENT' is implemented by physical table COMPONENT (columns: component_id, component_name, component_category, unit_of_measure, st…_

---

### ✅ QA-023 — How can I find all parent products that contain a specific component anywhere in their BOM structure?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.5213 | **Gate:** `proceed`

**Expected answer:**
> Use a recursive reverse traversal of the BOM. Start with the component_id as the initial parent_product_id. Find all records where this product appears as component_product_id in the bom table. For each parent_product_id found, check if it appears as a component_product_id in other bom records (is a…

**System answer:**
> Use the `bom` table as the traversal table. In this schema, a BOM entry is implemented by `BOM(bom_id, parent_product_id, component_product_id, quantity, unit_of_measure, bom_level, is_optional)`, and both `parent_product_id` and `component_product_id` reference `PRODUCT.product_id`. The context explicitly says this supports recursive, multi-level assemblies such as `Bicycle → Wheel → Spoke`.

So …

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
> Use the BOM hierarchy, then link the resulting products to `WORK_ORDER`.

From the provided schema, a work order is for a product via `WORK_ORDER.PRODUCT_ID -> PRODUCT.PRODUCT_ID`. Component requirements across nested sub-assemblies are modeled in `BOM`, where `BOM.PARENT_PRODUCT_ID` is the product being built and `BOM.COMPONENT_PRODUCT_ID` is a product used inside it. Because both columns referen…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_6`, `parent_chunk_data_dictionary.md_5`, `parent_chunk_data_dictionary.md_3`, `parent_chunk_data_dictionary.md_4`, `Hierarchical production planning and tracking→WORK_ORDER`, `WORK_ORDER→WORK_ORDER`, `WORK_ORDER→PRODUCT`, `WORK_ORDER→WAREHOUSE`

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
> Use the `bom` table. The business concept “BOM entry” is implemented by physical table `BOM`, and its `bom_level` column is explicitly defined as the depth in the product hierarchy. It is `NOT NULL`, defaults to `0`, and has a `CHECK >= 0`.

So, at the schema level, the maximum BOM depth is determined by taking the highest value in `BOM.bom_level`. There is no fixed upper bound defined in the sche…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_4`, `parent_chunk_data_dictionary.md_3`, `BOM entry→BOM`, `BOM→PRODUCT`, `parent_chunk_data_dictionary.md_7`, `parent_chunk_data_dictionary.md_5`, `parent_chunk_data_dictionary.md_6`, `Actual stock levels of components and products at specific warehouse locations→INVENTORY`

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
> Use the `bom` table as the primary structure for this search, because it explicitly models product composition and supports multi-level assemblies.

To find all products that contain a specific product as a sub-assembly at any level, start with the target product in `bom.component_product_id`, then recursively walk upward through `bom.parent_product_id`. Each step answers “what product is this use…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_3`, `parent_chunk_data_dictionary.md_4`, `parent_chunk_data_dictionary.md_5`, `Actual stock levels of components and products at specific warehouse locations→INVENTORY`, `Product classification: FINISHED_GOOD, ASSEMBLY, COMPONENT→COMPONENT`, `parent_chunk_data_dictionary.md_7`, `Actual stock levels of components and products at specific warehouse locations→WAREHOUSE`, `parent_chunk_data_dictionary.md_6`

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
> The retrieved context does not define a single official formula for “total lead time.” It tells you where the lead-time data lives and how to traverse the product structure, but it does not say whether total lead time should be calculated as a sum of all levels, the maximum/critical path, or some other planning rule.

What the context does support is the schema-level tracing method:

Start with th…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_3`, `(product_id, sequence_number)→PRODUCT`, `components they can provide through approved supplier relationships→COMPONENT_SUPPLIER`, `parent_chunk_data_dictionary.md_4`, `parent_chunk_data_dictionary.md_7`, `parent_chunk_data_dictionary.md_6`, `parent_chunk_data_dictionary.md_8`, `parent_chunk_data_dictionary.md_5`

**Context previews (first 3):**

1. _# Manufacturing Data Dictionary  This data dictionary documents the database schema for the manufacturing supply chain system. It includes all tables, columns, data types, constraints, and relationshi…_

2. _Business concept '(product_id, sequence_number)' is implemented by physical table PRODUCT (columns: product_id, product_name, product_type, parent_product_id, base_cost, lead_time_days, is_active).…_

3. _Business concept 'components they can provide through approved supplier relationships' is implemented by physical table COMPONENT_SUPPLIER (columns: component_supplier_id, component_id, supplier_id, i…_

---

### ✅ QA-028 — How do I generate a complete indented BOM report showing the hierarchical structure?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.4180 | **Gate:** `proceed`

**Expected answer:**
> Use a recursive query on the bom table that tracks the current depth level. Start with the top-level product (parent_product_id where product has no parent_product_id). At each level, output component details indented by depth level. Include product_name, quantity, and unit_of_measure. Recursively p…

**System answer:**
> Use the `bom` table as the primary source for the hierarchy and join it to `product` twice to resolve names for both the assembly and the component.

A complete indented BOM report is built from these schema relationships:

`bom.parent_product_id -> product.product_id` gives the parent assembly.
`bom.component_product_id -> product.product_id` gives the component under that parent.

The relevant `…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_4`, `parent_chunk_data_dictionary.md_3`, `parent_chunk_data_dictionary.md_6`, `parent_chunk_data_dictionary.md_8`, `BOM entry→BOM`, `Hierarchical production planning and tracking→WORK_ORDER`, `BOM→PRODUCT`, `parent_chunk_business_glossary.md_0`

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
> Use the BOM table as the primary source. The business concept “BOM entry” is implemented by `BOM(bom_id, parent_product_id, component_product_id, quantity, unit_of_measure, bom_level, is_optional)`, and `component_product_id` is a foreign key to `PRODUCT.product_id`.

To find which components appear most frequently across all product BOMs, count BOM rows grouped by `BOM.component_product_id`. If y…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_4`, `parent_chunk_data_dictionary.md_3`, `BOM entry→BOM`, `BOM→PRODUCT`, `parent_chunk_data_dictionary.md_5`, `Actual stock levels of components and products at specific warehouse locations→INVENTORY`, `Product classification: FINISHED_GOOD, ASSEMBLY, COMPONENT→COMPONENT`, `Actual stock levels of components and products at specific warehouse locations→WAREHOUSE`

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
> From the retrieved context, the BOM structure is recursive because `bom.parent_product_id` and `bom.component_product_id` both reference `product(product_id)`. The `bom` table is specifically described as supporting “recursive relationships for multi-level assemblies,” and the `product` hierarchy supports “unlimited nesting depth for complex assemblies.” That means any circular-reference check wou…

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
> From the retrieved context, you can determine the complete product structure for a finished product, but you cannot fully determine the complete supplier chain for that structure because the provided schema does not include a direct relationship from a supplier to a specific product, component, or BOM line.

What you can determine is the full sub-assembly/component hierarchy. Start with `product`,…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_3`, `Product classification: FINISHED_GOOD, ASSEMBLY, COMPONENT→COMPONENT`, `parent_chunk_data_dictionary.md_4`, `parent_chunk_data_dictionary.md_8`, `parent_chunk_data_dictionary.md_6`, `Shipment→SHIPMENT`, `parent_chunk_data_dictionary.md_7`, `parent_chunk_business_glossary.md_0`

**Context previews (first 3):**

1. _# Manufacturing Data Dictionary  This data dictionary documents the database schema for the manufacturing supply chain system. It includes all tables, columns, data types, constraints, and relationshi…_

2. _Business concept 'Product classification: FINISHED_GOOD, ASSEMBLY, COMPONENT' is implemented by physical table COMPONENT (columns: component_id, component_name, component_category, unit_of_measure, st…_

3. _## bom  Bill of Materials defining product composition and hierarchical structure. Supports recursive relationships for multi-level assemblies.  | Column | Data Type | Constraints | Description | |---…_

---

### ✅ QA-032 — How do I check if sufficient inventory exists across all warehouses to fulfill a work order?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.4035 | **Gate:** `proceed`

**Expected answer:**
> For the work_order's product_id, perform recursive BOM explosion to get all required components with quantities. For each component, sum the available quantity (quantity_on_hand - quantity_reserved) across all warehouses from the inventory table. Compare aggregated available inventory against requir…

**System answer:**
> The knowledge graph contains schema metadata only, so it cannot tell you whether a specific work order is currently fulfillable from actual records. At the schema level, the relevant fields are in `WORK_ORDER` and `INVENTORY`.

`WORK_ORDER` tells you what is being produced and in what amount: `work_order_id`, `product_id`, `quantity_ordered`, `quantity_completed`, `status`, and `warehouse_id`. `IN…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_5`, `parent_chunk_data_dictionary.md_6`, `Actual stock levels of components and products at specific warehouse locations→INVENTORY`, `INVENTORY→WAREHOUSE`, `WORK_ORDER→WAREHOUSE`, `Hierarchical production planning and tracking→WORK_ORDER`, `parent_chunk_data_dictionary.md_8`, `parent_chunk_business_glossary.md_1`

**Context previews (first 3):**

1. _## warehouse  Stores physical storage location information for inventory management.  | Column | Data Type | Constraints | Description | |--------|-----------|-------------|-------------| | warehouse_…_

2. _## work_order  Represents production jobs for manufacturing products with hierarchical work order support.  | Column | Data Type | Constraints | Description | |--------|-----------|-------------|-----…_

3. _Business concept 'Actual stock levels of components and products at specific warehouse locations' is implemented by physical table INVENTORY (columns: inventory_id, warehouse_id, component_id, product…_

---

### ✅ QA-033 — How can I find which quality control inspections failed for components from specific suppliers?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.4561 | **Gate:** `proceed`

**Expected answer:**
> Query the quality_control table filtering by result = 'FAIL'. Join with the batch table to get product_id and production_date. Join with the bom table recursively to trace which products contain failed components. Join with component_supplier and supplier tables to identify the source supplier. Filt…

**System answer:**
> From the retrieved context, the part you can identify directly is the failed inspection itself: use the `QUALITY_CONTROL` table and filter `result = 'FAIL'`. The available QC fields are `qc_id`, `batch_id`, `specification_id`, `qc_date`, `qc_type`, `inspector_id`, `result`, `defect_count`, and `notes`. QC is defined as inspection/testing on materials, in-process production, or finished goods, and …

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_5`, `parent_chunk_data_dictionary.md_3`, `inspection and testing records for quality assurance→QUALITY_CONTROL`, `components they can provide through approved supplier relationships→COMPONENT_SUPPLIER`, `parent_chunk_data_dictionary.md_4`, `Actual stock levels of components and products at specific warehouse locations→INVENTORY`, `Actual stock levels of components and products at specific warehouse locations→WAREHOUSE`, `COMPONENT_SUPPLIER→SUPPLIER`

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
> The retrieved context does not define an official calculation for “total manufacturing time” of a work order, so this cannot be determined precisely from the knowledge graph.

What is known from the context is this:

The table `WORK_ORDER` supports hierarchical production through `parent_work_order`, which is a self-reference to `work_order.work_order_id`. That means a top-level work order can be …

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_6`, `parent_chunk_data_dictionary.md_3`, `Hierarchical production planning and tracking→WORK_ORDER`, `parent_chunk_data_dictionary.md_7`, `parent_chunk_data_dictionary.md_5`, `parent_chunk_data_dictionary.md_4`, `Production Batches→BATCH`, `Routing Step→ROUTE`

**Context previews (first 3):**

1. _## work_order  Represents production jobs for manufacturing products with hierarchical work order support.  | Column | Data Type | Constraints | Description | |--------|-----------|-------------|-----…_

2. _# Manufacturing Data Dictionary  This data dictionary documents the database schema for the manufacturing supply chain system. It includes all tables, columns, data types, constraints, and relationshi…_

3. _Business concept 'Hierarchical production planning and tracking' is implemented by physical table WORK_ORDER (columns: work_order_id, product_id, parent_work_order, quantity_ordered, quantity_complete…_

---

### ✅ QA-035 — How can I identify which shipments are overdue and their impact on work orders?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0719 | **Gate:** `proceed_with_warning`

**Expected answer:**
> Query the shipment table filtering for status = 'SHIPPED' where actual_arrival is NULL and estimated_arrival is in the past (overdue). Join with the component_supplier table via supplier_id and component_id to identify which components are delayed. Perform reverse BOM lookup to find which parent pro…

**System answer:**
> Use the `shipment` table to evaluate shipment timing, and connect it to `work_order` through the shared `warehouse` relationship.

At the shipment level, the relevant fields are `shipment_id`, `shipment_type`, `warehouse_id`, `ship_date`, `estimated_arrival`, `actual_arrival`, and `status`. The context does not define a formal “overdue” flag, but it does provide the dates needed to assess lateness…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_5`, `parent_chunk_data_dictionary.md_8`, `parent_chunk_data_dictionary.md_6`, `Shipment`, `Shipment→SHIPMENT`, `WORK_ORDER→PRODUCT`, `WORK_ORDER→WAREHOUSE`, `Hierarchical production planning and tracking→WORK_ORDER`

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
> From the available schema, you can identify batches that are approaching or past expiry only from the `BATCH` table. The relevant columns are `batch_id`, `product_id`, `production_date`, `quantity_produced`, `warehouse_id`, `expiry_date`, and `qc_status`. To add location context, join `BATCH.warehouse_id` to `WAREHOUSE.warehouse_id`. To add the produced item, join `BATCH.product_id` to `PRODUCT.pr…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_5`, `Actual stock levels of components and products at specific warehouse locations→INVENTORY`, `Production Batches→BATCH`, `Actual stock levels of components and products at specific warehouse locations→WAREHOUSE`, `parent_chunk_data_dictionary.md_7`, `parent_chunk_data_dictionary.md_3`, `parent_chunk_business_glossary.md_2`, `parent_chunk_business_glossary.md_1`

**Context previews (first 3):**

1. _## warehouse  Stores physical storage location information for inventory management.  | Column | Data Type | Constraints | Description | |--------|-----------|-------------|-------------| | warehouse_…_

2. _Business concept 'Actual stock levels of components and products at specific warehouse locations' is implemented by physical table INVENTORY (columns: inventory_id, warehouse_id, component_id, product…_

3. _Business concept 'Production Batches' — The table is explicitly labeled as a batch/production lots entity and includes batch_id, product_id, production_date, quantity_produced, warehouse_id, expiry_da…_

---

### ✅ QA-037 — How can I generate a material requirements plan showing when to order components based on work order schedules?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0433 | **Gate:** `proceed_with_warning`

**Expected answer:**
> Query all work_orders with status 'PENDING' ordered by planned_start_date. For each work_order, perform BOM explosion to get required components and quantities. For each component, query inventory for current available stock across warehouses. Calculate net requirements = (required quantity * work_o…

**System answer:**
> Use `WORK_ORDER` as the driver, because it contains the production schedule in `product_id`, `quantity_ordered`, `quantity_completed`, `status`, `planned_start_date`, `planned_end_date`, and `warehouse_id`. For an MRP-style plan, focus on open work orders such as `PENDING` and `IN_PROGRESS`. If production is decomposed into sub-jobs, include the self-referential relationship `WORK_ORDER.parent_wor…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_6`, `parent_chunk_data_dictionary.md_7`, `parent_chunk_data_dictionary.md_5`, `parent_chunk_data_dictionary.md_4`, `Hierarchical production planning and tracking→WORK_ORDER`, `parent_chunk_data_dictionary.md_3`, `components they can provide through approved supplier relationships→COMPONENT_SUPPLIER`, `Actual stock levels of components and products at specific warehouse locations→INVENTORY`

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
> From the retrieved context, you cannot trace a fully continuous genealogy for a physical `COMPONENT` record all the way from `supplier` through `batch` to specific finished goods, because the provided schema metadata does not define the missing bridge points. In particular, there is no explicit relationship between `COMPONENT` and `PRODUCT`, `batch.product_id` links only to `product(product_id)`, …

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_3`, `Product classification: FINISHED_GOOD, ASSEMBLY, COMPONENT→COMPONENT`, `parent_chunk_data_dictionary.md_7`, `parent_chunk_data_dictionary.md_5`, `parent_chunk_data_dictionary.md_8`, `parent_chunk_data_dictionary.md_4`, `components they can provide through approved supplier relationships→COMPONENT_SUPPLIER`, `parent_chunk_business_glossary.md_2`

**Context previews (first 3):**

1. _# Manufacturing Data Dictionary  This data dictionary documents the database schema for the manufacturing supply chain system. It includes all tables, columns, data types, constraints, and relationshi…_

2. _Business concept 'Product classification: FINISHED_GOOD, ASSEMBLY, COMPONENT' is implemented by physical table COMPONENT (columns: component_id, component_name, component_category, unit_of_measure, st…_

3. _## specification  Defines technical requirements and acceptance criteria for materials and products.  | Column | Data Type | Constraints | Description | |--------|-----------|-------------|-----------…_

---

### ✅ QA-039 — How can I find alternative suppliers for components that are critical for multiple products?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0772 | **Gate:** `proceed_with_warning`

**Expected answer:**
> Perform BOM explosion for all active products and count component usage frequency. Identify high-frequency components. Query component_supplier table to find all suppliers for these components. Filter to suppliers with rating >= 4.0 (high quality) and is_preferred = 'Y'. For each component, list alt…

**System answer:**
> From the available schema, this is only partially traceable end to end.

To identify components that are critical for multiple products, the closest supported method is to use the `bom` table. `bom.parent_product_id` is the product being built, and `bom.component_product_id` is the product used as a component. Because `bom` supports recursive product structures and multi-level assemblies, you can …

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_4`, `parent_chunk_data_dictionary.md_3`, `components they can provide through approved supplier relationships→COMPONENT_SUPPLIER`, `parent_chunk_data_dictionary.md_5`, `parent_chunk_data_dictionary.md_8`, `parent_chunk_data_dictionary.md_7`, `COMPONENT_SUPPLIER→COMPONENT`, `COMPONENT_SUPPLIER→SUPPLIER`

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
> From the retrieved context, you can only calculate a partial, schema-driven version of landed cost.

The starting point is `PRODUCT`. For the finished product, use `PRODUCT.product_id` to find its own `base_cost` and `lead_time_days`. To include lower-level material content, recursively explode the `BOM` by joining `BOM.parent_product_id = PRODUCT.product_id`, then following each `BOM.component_pr…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_3`, `components they can provide through approved supplier relationships→COMPONENT_SUPPLIER`, `(product_id, sequence_number)→PRODUCT`, `parent_chunk_data_dictionary.md_6`, `parent_chunk_data_dictionary.md_7`, `parent_chunk_data_dictionary.md_5`, `parent_chunk_data_dictionary.md_8`, `Product classification: FINISHED_GOOD, ASSEMBLY, COMPONENT→COMPONENT`

**Context previews (first 3):**

1. _# Manufacturing Data Dictionary  This data dictionary documents the database schema for the manufacturing supply chain system. It includes all tables, columns, data types, constraints, and relationshi…_

2. _Business concept 'components they can provide through approved supplier relationships' is implemented by physical table COMPONENT_SUPPLIER (columns: component_supplier_id, component_id, supplier_id, i…_

3. _Business concept '(product_id, sequence_number)' is implemented by physical table PRODUCT (columns: product_id, product_name, product_type, parent_product_id, base_cost, lead_time_days, is_active).…_

---

## Anomalies & Observations

No anomalies detected. All questions grounded with acceptable RAGAS scores.
