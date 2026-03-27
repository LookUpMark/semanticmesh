# AB-00 — 04_complex_manufacturing — Run Analysis

**Timestamp:** 2026-03-27 18:13:59  
**Run tag:** `post-fix-v3`

## Configuration

| Parameter | Value |
|-----------|-------|
| Extraction model | `LLM (gpt-5.4-nano-2026-03-17)` |
| Reasoning model | `gpt-5.4-nano-2026-03-17` |
| Embedding model | `BAAI/bge-m3` |
| Retrieval mode | `hybrid` |
| Reranker | `True` |
| Reranker top_k | `12` |
| Chunk size / overlap | `256 / 32` |
| ER similarity threshold | `0.75` |

## Builder Results

| Metric | Value |
|--------|-------|
| Triplets extracted | 389 |
| Entities resolved | 125 |
| Tables parsed | 13 |
| Tables completed | 13 |

## Query Evaluation Summary

| Metric | Value |
|--------|-------|
| Questions | 40 |
| Grounded | **40/40 (100%)** |
| Avg GT Coverage | 100% |
| Avg Top Score | 0.4461 |
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
> The manufacturing system stores information about products in the `product` table (and also describes it in the `Product` business concept).

In `product`, each manufactured item has a unique `product_id`, a `product_name`, and a `product_type` that classifies it as `FINISHED_GOOD`, `ASSEMBLY`, or `COMPONENT`. It also stores hierarchical structure via `parent_product_id` (a self-referencing foreig…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_3`, `Route Steps→ROUTE`, `Actual stock levels of components and products stored in specific warehouses→INVENTORY`, `parent_chunk_data_dictionary.md_6`, `parent_chunk_data_dictionary.md_5`, `parent_chunk_data_dictionary.md_7`, `parent_chunk_business_glossary.md_0`, `Route Steps`

**Context previews (first 3):**

1. _# Manufacturing Data Dictionary  This data dictionary documents the database schema for the manufacturing supply chain system. It includes all tables, columns, data types, constraints, and relationshi…_

2. _Business concept 'Route Steps' — The table stores ordered manufacturing operations for a product using product_id, sequence_number, operation_name, work_center, and per-unit processing time (cycle_tim…_

3. _Business concept 'Actual stock levels of components and products stored in specific warehouses' is implemented by physical table INVENTORY (columns: inventory_id, warehouse_id, component_id, product_i…_

---

### ✅ QA-002 — How are components defined in the manufacturing database?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.5910 | **Gate:** `proceed`

**Expected answer:**
> Components are defined with a unique identifier (component_id), descriptive name (component_name), category grouping (component_category), unit of measure (unit_of_measure), standard unit cost (standard_cost), and optional reference to technical specifications (specification_id). Components represen…

**System answer:**
> In the manufacturing database, components are defined as atomic raw materials or purchased parts that cannot be further broken down into simpler manufactured items. At the schema level, this is reflected by the business concept “Component Cost and Spec” and its implementation in the physical table `COMPONENT`, which includes the fields `component_id` and `component_name`, plus `component_category`…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_3`, `Component Cost and Spec→COMPONENT`, `Bill of Materials (BOM) entry (parent product and required components/sub-assemblies with quantity, unit of measure, and hierarchy level)→BOM`, `Component approved supplier junction→COMPONENT_SUPPLIER`, `parent_chunk_data_dictionary.md_4`, `parent_chunk_data_dictionary.md_5`, `parent_chunk_business_glossary.md_0`, `parent_chunk_business_glossary.md_1`

**Context previews (first 3):**

1. _# Manufacturing Data Dictionary  This data dictionary documents the database schema for the manufacturing supply chain system. It includes all tables, columns, data types, constraints, and relationshi…_

2. _Business concept 'Component Cost and Spec' — The table defines atomic material parts with component_id and component_name, plus component_category for type classification, and financial fields unit_of…_

3. _Business concept 'Bill of Materials (BOM) entry (parent product and required components/sub-assemblies with quantity, unit of measure, and hierarchy level)' is implemented by physical table BOM (colum…_

---

### ✅ QA-003 — What is the purpose of the Bill of Materials (BOM) table?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.9118 | **Gate:** `proceed`

**Expected answer:**
> The BOM table defines the hierarchical structure of products by specifying which components or sub-assemblies are required to manufacture each parent product. It records the unique BOM entry identifier (bom_id), parent product being built (parent_product_id), component or sub-assembly product (compo…

**System answer:**
> The purpose of the `bom` table is to define a product’s composition and its hierarchical structure by listing, for each parent product, the required component (or sub-assembly) products and the quantity needed to build the parent. It supports multi-level assemblies through a hierarchy depth (`bom_level`) and recursive relationships (both `parent_product_id` and `component_product_id` reference `pr…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_4`, `Bill of Materials (BOM) entry (parent product and required components/sub-assemblies with quantity, unit of measure, and hierarchy level)→BOM`, `BOM→PRODUCT`, `parent_chunk_data_dictionary.md_3`, `parent_chunk_business_glossary.md_0`, `Bill of Materials (BOM) entry (parent product and required components/sub-assemblies with quantity, unit of measure, and hierarchy level)`, `External Supplier`, `Production Lots`

**Context previews (first 3):**

1. _## bom  Bill of Materials defining product composition and hierarchical structure. Supports recursive relationships for multi-level assemblies.  | Column | Data Type | Constraints | Description | |---…_

2. _Business concept 'Bill of Materials (BOM) entry (parent product and required components/sub-assemblies with quantity, unit of measure, and hierarchy level)' is implemented by physical table BOM (colum…_

3. _Relationship: BOM references PRODUCT via foreign key COMPONENT_PRODUCT_ID -> PRODUCT.PRODUCT_ID.…_

---

### ✅ QA-004 — What supplier information does the system maintain?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.4194 | **Gate:** `proceed`

**Expected answer:**
> Suppliers are tracked with a unique identifier (supplier_id), legal business name (supplier_name), primary contact email (contact_email), primary contact phone number (contact_phone), performance rating from 1.0 to 5.0 (rating), and preferred supplier status flag (is_preferred).

**System answer:**
> The system maintains external supplier master data in the table **SUPPLIER**. It includes a unique **supplier_id** and **supplier_name**, procurement contact details **contact_email** and **contact_phone**, and supplier evaluation attributes **rating** and **is_preferred**.

**Sources retrieved (12):** `External Supplier→SUPPLIER`, `parent_chunk_data_dictionary.md_4`, `SHIPMENT→SUPPLIER`, `parent_chunk_data_dictionary.md_8`, `COMPONENT_SUPPLIER→SUPPLIER`, `Component approved supplier junction→COMPONENT_SUPPLIER`, `parent_chunk_data_dictionary.md_3`, `External Supplier`

**Context previews (first 3):**

1. _Business concept 'External Supplier' — The table stores core supplier master data (supplier_id, supplier_name) along with procurement contact details (contact_email, contact_phone) and supplier evalua…_

2. _## bom  Bill of Materials defining product composition and hierarchical structure. Supports recursive relationships for multi-level assemblies.  | Column | Data Type | Constraints | Description | |---…_

3. _Relationship: SHIPMENT references SUPPLIER via foreign key SUPPLIER_ID -> SUPPLIER.SUPPLIER_ID.…_

---

### ✅ QA-005 — How are warehouses represented in the schema?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.3381 | **Gate:** `proceed`

**Expected answer:**
> Warehouses are defined with a unique identifier (warehouse_id), descriptive name (warehouse_name), full street address (address), city location (city), state or province (state), total storage capacity in cubic meters (capacity), and optional manager identifier (manager_id).

**System answer:**
> Warehouses are represented by the physical table `warehouse` (see the table definition `## warehouse`), which stores physical storage location information for inventory management. It includes columns `warehouse_id` (primary key), `warehouse_name`, `address`, `city`, `state`, `capacity`, and `manager_id`.

In the schema, `warehouse` is referenced by other entities via foreign keys: `inventory` ref…

**Sources retrieved (12):** `INVENTORY→WAREHOUSE`, `BATCH→WAREHOUSE`, `WORK_ORDER→WAREHOUSE`, `SHIPMENT→WAREHOUSE`, `parent_chunk_data_dictionary.md_6`, `state→WAREHOUSE`, `parent_chunk_data_dictionary.md_5`, `parent_chunk_data_dictionary.md_8`

**Context previews (first 3):**

1. _Relationship: INVENTORY references WAREHOUSE via foreign key WAREHOUSE_ID -> WAREHOUSE.WAREHOUSE_ID.…_

2. _Relationship: BATCH references WAREHOUSE via foreign key WAREHOUSE_ID -> WAREHOUSE.WAREHOUSE_ID.…_

3. _Relationship: WORK_ORDER references WAREHOUSE via foreign key WAREHOUSE_ID -> WAREHOUSE.WAREHOUSE_ID.…_

---

### ✅ QA-006 — What does the inventory table track?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.7080 | **Gate:** `proceed`

**Expected answer:**
> The inventory table tracks real-time stock levels including a unique record identifier (inventory_id), warehouse location (warehouse_id), component identifier for materials (component_id) or product identifier for finished goods (product_id), current physical stock quantity (quantity_on_hand), quant…

**System answer:**
> The physical table **INVENTORY** tracks the actual stock levels of **components and products** stored in **specific warehouses**. Each **inventory** record includes **quantity_on_hand** (quantity available), **quantity_reserved** (quantity reserved for pending orders), **reorder_threshold** (to trigger procurement), and **last_restock_date** (timestamp of the last restock). It supports either **co…

**Sources retrieved (12):** `INVENTORY→PRODUCT`, `INVENTORY→WAREHOUSE`, `INVENTORY→COMPONENT`, `Production Lots→BATCH`, `Actual stock levels of components and products stored in specific warehouses→INVENTORY`, `parent_chunk_data_dictionary.md_5`, `parent_chunk_data_dictionary.md_7`, `parent_chunk_data_dictionary.md_8`

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
> Work orders are stored in the `work_order` table, which represents production jobs and supports hierarchical work order decomposition. Structurally, each work order has a unique `work_order_id`, is tied to a `product_id` (the product to manufacture), and can optionally reference a `parent_work_order` (a self-referential foreign key to `work_order.work_order_id`) to form parent/child work order rel…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_6`, `Hierarchical production planning and tracking→WORK_ORDER`, `WORK_ORDER→PRODUCT`, `Route Steps→ROUTE`, `WORK_ORDER→WORK_ORDER`, `parent_chunk_data_dictionary.md_3`, `WORK_ORDER→WAREHOUSE`, `parent_chunk_data_dictionary.md_8`

**Context previews (first 3):**

1. _## work_order  Represents production jobs for manufacturing products with hierarchical work order support.  | Column | Data Type | Constraints | Description | |--------|-----------|-------------|-----…_

2. _Business concept 'Hierarchical production planning and tracking' is implemented by physical table WORK_ORDER (columns: work_order_id, product_id, parent_work_order, quantity_ordered, quantity_complete…_

3. _Relationship: WORK_ORDER references PRODUCT via foreign key PRODUCT_ID -> PRODUCT.PRODUCT_ID.…_

---

### ✅ QA-008 — What information is captured in the shipment table?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.9266 | **Gate:** `proceed`

**Expected answer:**
> Shipments track material transfers with a unique identifier (shipment_id), shipment type (INBOUND from suppliers, OUTBOUND to customers, INTERNAL between warehouses), destination warehouse (warehouse_id), source supplier for inbound (supplier_id), destination customer for outbound (customer_id), shi…

**System answer:**
> The physical table **SHIPMENT** captures material transfer information, including:

Shipment identifiers and parties/locations: **shipment_id** (primary key), **shipment_type** (NOT NULL; INBOUND, OUTBOUND, INTERNAL), **warehouse_id** (FK to WAREHOUSE), **supplier_id** (FK to supplier; intended for INBOUND only via **chk_supplier_inbound**), and **customer_id** (customer reference for outbound).

…

**Sources retrieved (12):** `Shipment Dates→SHIPMENT`, `SHIPMENT→WAREHOUSE`, `SHIPMENT→SUPPLIER`, `parent_chunk_data_dictionary.md_8`, `parent_chunk_data_dictionary.md_5`, `Shipment Dates`, `parent_chunk_business_glossary.md_0`, `External Supplier→SUPPLIER`

**Context previews (first 3):**

1. _Business concept 'Shipment Dates' — The table is explicitly a SHIPMENT entity for material transfers and contains the core date fields ship_date, estimated_arrival, and actual_arrival (with constraint…_

2. _Relationship: SHIPMENT references WAREHOUSE via foreign key WAREHOUSE_ID -> WAREHOUSE.WAREHOUSE_ID.…_

3. _Relationship: SHIPMENT references SUPPLIER via foreign key SUPPLIER_ID -> SUPPLIER.SUPPLIER_ID.…_

---

### ✅ QA-009 — How does the quality control system record inspections?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.9833 | **Gate:** `proceed`

**Expected answer:**
> Quality control records are stored with a unique identifier (qc_id), associated production batch (batch_id), applicable specification requirements (specification_id), inspection date (qc_date), inspection type (INCOMING for supplier materials, IN_PROCESS during manufacturing, FINAL for finished good…

**System answer:**
> The quality control system records inspections using the physical table `QUALITY_CONTROL` under the business concept `Quality Control Records` / `QualityControl`.

Each QC inspection record stores inspection/testing attributes such as `qc_date` (inspection date), `qc_type` (inspection type), `inspector_id` (inspector), `result` (test result), `defect_count` (defect counts), and `notes`. It also li…

**Sources retrieved (12):** `Quality Control Records→QUALITY_CONTROL`, `BOM→PRODUCT`, `Production Lots→BATCH`, `Technical requirements and acceptance criteria→SPECIFICATION`, `parent_chunk_data_dictionary.md_3`, `Quality Control Records`, `parent_chunk_business_glossary.md_2`, `parent_chunk_business_glossary.md_0`

**Context previews (first 3):**

1. _Business concept 'Quality Control Records' — The table stores inspection/testing attributes for quality assurance, including inspection date (qc_date), inspection type (qc_type), inspector (inspector_…_

2. _Relationship: BOM references PRODUCT via foreign key COMPONENT_PRODUCT_ID -> PRODUCT.PRODUCT_ID.…_

3. _Business concept 'Production Lots' — The table stores lot-level production details such as batch_id, product_id, production_date, quantity_produced, warehouse_id, expiry_date, and qc_status, which dir…_

---

### ✅ QA-010 — What do specification records define?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.7558 | **Gate:** `proceed`

**Expected answer:**
> Specifications define technical requirements with a unique identifier (specification_id), descriptive name (specification_name), version number, effective date, specification type (DIMENSIONAL, MATERIAL, PERFORMANCE), critical parameter being measured (critical_parameter), acceptable minimum value (…

**System answer:**
> Specification records define technical requirements and acceptance criteria for materials and products.

Specifically, the physical table `SPECIFICATION` stores versioned, effective-dated specifications with a `spec_type` (DIMENSIONAL, MATERIAL, PERFORMANCE), a tested `critical_parameter`, and measurable acceptable limits via `min_value` and `max_value` with a `unit_of_measure` (with the constrain…

**Sources retrieved (12):** `Quality Control Records→QUALITY_CONTROL`, `Technical requirements and acceptance criteria→SPECIFICATION`, `parent_chunk_data_dictionary.md_7`, `Component Cost and Spec→COMPONENT`, `parent_chunk_data_dictionary.md_3`, `parent_chunk_business_glossary.md_2`, `Quality Control Records`, `Technical requirements and acceptance criteria`

**Context previews (first 3):**

1. _Business concept 'Quality Control Records' — The table stores inspection/testing attributes for quality assurance, including inspection date (qc_date), inspection type (qc_type), inspector (inspector_…_

2. _Business concept 'Technical requirements and acceptance criteria' — The table stores a versioned, effective-dated specification with a specification type (spec_type) and measurable acceptance limits (…_

3. _## specification  Defines technical requirements and acceptance criteria for materials and products.  | Column | Data Type | Constraints | Description | |--------|-----------|-------------|-----------…_

---

### ✅ QA-011 — How can I find which suppliers provide specific components?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.2417 | **Gate:** `proceed`

**Expected answer:**
> Query the component_supplier table which links components to their approved suppliers. This table contains the component identifier (component_id), supplier identifier (supplier_id), preferred supplier flag (is_preferred), lead time in days (lead_time_days), and unit price (unit_price). Join with th…

**System answer:**
> To find which suppliers provide a specific component, use the component–supplier many-to-many junction table `COMPONENT_SUPPLIER`, which links `component_id` to `supplier_id` (and includes relationship attributes like `is_preferred`, `unit_price`, and `lead_time_days`). Filter `COMPONENT_SUPPLIER` by the `component_id` you care about, then join to `SUPPLIER` on `COMPONENT_SUPPLIER.supplier_id = SU…

**Sources retrieved (12):** `Component approved supplier junction→COMPONENT_SUPPLIER`, `External Supplier→SUPPLIER`, `parent_chunk_data_dictionary.md_5`, `parent_chunk_data_dictionary.md_4`, `Actual stock levels of components and products stored in specific warehouses→INVENTORY`, `parent_chunk_data_dictionary.md_3`, `Component approved supplier junction`, `External Supplier`

**Context previews (first 3):**

1. _Business concept 'Component approved supplier junction' — The table is explicitly a many-to-many junction between components and suppliers, with the DDL comment stating it links components to their ap…_

2. _Business concept 'External Supplier' — The table stores core supplier master data (supplier_id, supplier_name) along with procurement contact details (contact_email, contact_phone) and supplier evalua…_

3. _## warehouse  Stores physical storage location information for inventory management.  | Column | Data Type | Constraints | Description | |--------|-----------|-------------|-------------| | warehouse_…_

---

### ✅ QA-012 — How do I trace which components are needed to fulfill a work order?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.2334 | **Gate:** `proceed`

**Expected answer:**
> Start with the work_order table to get the product_id being manufactured. Join to the bom table using product_id as parent_product_id to find all direct components and sub-assemblies. For each component_product_id, if it is an ASSEMBLY type product, recursively query the bom table again to explode m…

**System answer:**
> In this schema, a `work_order` identifies the manufactured item via `work_order.product_id` (the product to be manufactured) and can be decomposed via `work_order.parent_work_order`.  

Separately, the `BOM` table defines how products break down into required components: each `BOM` row ties a `parent_product_id` to a `component_product_id`, along with the `quantity`, `unit_of_measure`, `bom_level`…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_5`, `Hierarchical production planning and tracking→WORK_ORDER`, `parent_chunk_data_dictionary.md_6`, `Bill of Materials (BOM) entry (parent product and required components/sub-assemblies with quantity, unit of measure, and hierarchy level)→BOM`, `Component approved supplier junction→COMPONENT_SUPPLIER`, `Actual stock levels of components and products stored in specific warehouses→INVENTORY`, `parent_chunk_data_dictionary.md_3`, `parent_chunk_data_dictionary.md_8`

**Context previews (first 3):**

1. _## warehouse  Stores physical storage location information for inventory management.  | Column | Data Type | Constraints | Description | |--------|-----------|-------------|-------------| | warehouse_…_

2. _Business concept 'Hierarchical production planning and tracking' is implemented by physical table WORK_ORDER (columns: work_order_id, product_id, parent_work_order, quantity_ordered, quantity_complete…_

3. _## work_order  Represents production jobs for manufacturing products with hierarchical work order support.  | Column | Data Type | Constraints | Description | |--------|-----------|-------------|-----…_

---

### ✅ QA-013 — How can I identify which warehouses have available inventory for specific components?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.8876 | **Gate:** `proceed`

**Expected answer:**
> Query the inventory table filtered by component_id, joining with the warehouse table to get warehouse names and locations. Calculate available quantity as quantity_on_hand minus quantity_reserved. Filter for records where available quantity is greater than zero. Results show warehouse names, locatio…

**System answer:**
> Use the `INVENTORY` table to find stock by `component_id` and then group by `warehouse_id` (and optionally join to `warehouse` for names). Each `INVENTORY` row represents the stock level in a specific warehouse for either a component or a product (with `component_id` and `product_id` being mutually exclusive).

To determine whether a warehouse has “available” inventory for a specific component, us…

**Sources retrieved (12):** `Actual stock levels of components and products stored in specific warehouses→INVENTORY`, `parent_chunk_data_dictionary.md_5`, `INVENTORY→WAREHOUSE`, `INVENTORY→COMPONENT`, `parent_chunk_data_dictionary.md_3`, `parent_chunk_data_dictionary.md_8`, `parent_chunk_data_dictionary.md_6`, `Actual stock levels of components and products stored in specific warehouses`

**Context previews (first 3):**

1. _Business concept 'Actual stock levels of components and products stored in specific warehouses' is implemented by physical table INVENTORY (columns: inventory_id, warehouse_id, component_id, product_i…_

2. _## warehouse  Stores physical storage location information for inventory management.  | Column | Data Type | Constraints | Description | |--------|-----------|-------------|-------------| | warehouse_…_

3. _Relationship: INVENTORY references WAREHOUSE via foreign key WAREHOUSE_ID -> WAREHOUSE.WAREHOUSE_ID.…_

---

### ✅ QA-014 — How do I find which shipments delivered materials from a specific supplier?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.2401 | **Gate:** `proceed`

**Expected answer:**
> Query the shipment table filtering by supplier_id and shipment_type = 'INBOUND'. Join with the warehouse table to show destination warehouses. Filter for status = 'DELIVERED' and include actual_arrival date. Results can be ordered by ship_date descending to show most recent deliveries first.

**System answer:**
> Use the `shipment` table and filter on the supplier and the delivery status.

In the `shipment` entity (`shipment_id`, `shipment_type`, `supplier_id`, `status`, etc.), `supplier_id` is only set for inbound shipments (`chk_supplier_inbound`), and the delivery completion is represented by `status = 'DELIVERED'`.

So, to find delivered materials from a specific supplier, look for rows in `shipment` w…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_8`, `SHIPMENT→SUPPLIER`, `Shipment Dates→SHIPMENT`, `parent_chunk_data_dictionary.md_5`, `External Supplier→SUPPLIER`, `Actual stock levels of components and products stored in specific warehouses→INVENTORY`, `Component approved supplier junction→COMPONENT_SUPPLIER`, `Shipment Dates`

**Context previews (first 3):**

1. _## shipment  Tracks material transfers between warehouses, suppliers, and customers.  | Column | Data Type | Constraints | Description | |--------|-----------|-------------|-------------| | shipment_i…_

2. _Relationship: SHIPMENT references SUPPLIER via foreign key SUPPLIER_ID -> SUPPLIER.SUPPLIER_ID.…_

3. _Business concept 'Shipment Dates' — The table is explicitly a SHIPMENT entity for material transfers and contains the core date fields ship_date, estimated_arrival, and actual_arrival (with constraint…_

---

### ✅ QA-015 — How can I determine which quality control inspections were performed on a specific production batch?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.9779 | **Gate:** `proceed`

**Expected answer:**
> Query the quality_control table filtered by batch_id. Join with the specification table to get requirement details (specification_name, spec_type, acceptable ranges). Include qc_date, qc_type (INCOMING, IN_PROCESS, FINAL), result (PASS, FAIL, CONDITIONAL), and defect_count. This shows the complete i…

**System answer:**
> To determine which quality control inspections were performed on a specific production batch, use the `QUALITY_CONTROL` table (mapped from the business concept “Quality Control Records”). Each QC inspection record in `QUALITY_CONTROL` includes a `batch_id` that links it to a production lot in `BATCH`.

So, retrieve all rows from `QUALITY_CONTROL` where `QUALITY_CONTROL.batch_id` equals the `batch_…

**Sources retrieved (12):** `Quality Control Records→QUALITY_CONTROL`, `Production Lots→BATCH`, `parent_chunk_data_dictionary.md_7`, `BATCH→PRODUCT`, `parent_chunk_data_dictionary.md_5`, `parent_chunk_data_dictionary.md_6`, `parent_chunk_data_dictionary.md_3`, `parent_chunk_business_glossary.md_2`

**Context previews (first 3):**

1. _Business concept 'Quality Control Records' — The table stores inspection/testing attributes for quality assurance, including inspection date (qc_date), inspection type (qc_type), inspector (inspector_…_

2. _Business concept 'Production Lots' — The table stores lot-level production details such as batch_id, product_id, production_date, quantity_produced, warehouse_id, expiry_date, and qc_status, which dir…_

3. _## specification  Defines technical requirements and acceptance criteria for materials and products.  | Column | Data Type | Constraints | Description | |--------|-----------|-------------|-----------…_

---

### ✅ QA-016 — How do I track which work orders are in progress at a specific warehouse?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.7311 | **Gate:** `proceed`

**Expected answer:**
> Query the work_order table filtering by warehouse_id and status = 'IN_PROGRESS'. Join with the product table to get product names and types. Include quantity_ordered, quantity_completed, priority, planned_end_date, and calculate progress percentage as (quantity_completed / quantity_ordered * 100). O…

**System answer:**
> To track work orders that are currently in progress at a specific warehouse, use the `work_order` table and filter by the `warehouse_id` for that warehouse, and by `status`.

In `work_order`, the `status` column (type `status_t`) supports values including `IN_PROGRESS` (along with `PENDING`, `COMPLETED`, and `CLOSED`). The `warehouse_id` column is a foreign key to `warehouse(warehouse_id)`, repres…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_5`, `parent_chunk_data_dictionary.md_6`, `Hierarchical production planning and tracking→WORK_ORDER`, `WORK_ORDER→WAREHOUSE`, `Actual stock levels of components and products stored in specific warehouses→INVENTORY`, `parent_chunk_data_dictionary.md_8`, `parent_chunk_data_dictionary.md_7`, `parent_chunk_business_glossary.md_1`

**Context previews (first 3):**

1. _## warehouse  Stores physical storage location information for inventory management.  | Column | Data Type | Constraints | Description | |--------|-----------|-------------|-------------| | warehouse_…_

2. _## work_order  Represents production jobs for manufacturing products with hierarchical work order support.  | Column | Data Type | Constraints | Description | |--------|-----------|-------------|-----…_

3. _Business concept 'Hierarchical production planning and tracking' is implemented by physical table WORK_ORDER (columns: work_order_id, product_id, parent_work_order, quantity_ordered, quantity_complete…_

---

### ✅ QA-017 — How can I find which components need reordering based on current inventory levels?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.5691 | **Gate:** `proceed`

**Expected answer:**
> Query the inventory table and filter where quantity_on_hand minus quantity_reserved is less than reorder_threshold. Join with the component table to get component names, categories, and standard costs. Join with the warehouse table for location information. Results identify which components are belo…

**System answer:**
> To find which components need reordering, use the `INVENTORY` table, which is the implementation of the business concept “Actual stock levels of components and products stored in specific warehouses” and includes `quantity_on_hand`, `quantity_reserved`, and `reorder_threshold` (with `reorder_threshold` described as being used to “trigger procurement”).

In practice, you should query `INVENTORY` fo…

**Sources retrieved (12):** `Actual stock levels of components and products stored in specific warehouses→INVENTORY`, `parent_chunk_data_dictionary.md_5`, `INVENTORY→COMPONENT`, `parent_chunk_data_dictionary.md_3`, `Bill of Materials (BOM) entry (parent product and required components/sub-assemblies with quantity, unit of measure, and hierarchy level)→BOM`, `parent_chunk_data_dictionary.md_7`, `parent_chunk_data_dictionary.md_4`, `Component approved supplier junction→COMPONENT_SUPPLIER`

**Context previews (first 3):**

1. _Business concept 'Actual stock levels of components and products stored in specific warehouses' is implemented by physical table INVENTORY (columns: inventory_id, warehouse_id, component_id, product_i…_

2. _## warehouse  Stores physical storage location information for inventory management.  | Column | Data Type | Constraints | Description | |--------|-----------|-------------|-------------| | warehouse_…_

3. _Relationship: INVENTORY references COMPONENT via foreign key COMPONENT_ID -> COMPONENT.COMPONENT_ID.…_

---

### ✅ QA-018 — How do I determine the manufacturing route for a specific product?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.7341 | **Gate:** `proceed`

**Expected answer:**
> Query the route table filtering by product_id, ordered by sequence_number ascending. For each operation, retrieve operation_name, work_center, cycle_time_minutes, and setup_time_minutes. Join with the product table to get product details. The sequence of operations shows the complete manufacturing w…

**System answer:**
> To determine the manufacturing route for a specific product, use the table **ROUTE** (from the business concept **“Route Steps”**). The route is defined by the ordered set of operations in ROUTE for that product.

Concretely, select rows from **ROUTE** where **ROUTE.product_id** matches the product you’re interested in, and order the results by **ROUTE.sequence_number**. Each row describes one ste…

**Sources retrieved (12):** `Route Steps→ROUTE`, `parent_chunk_data_dictionary.md_6`, `ROUTE→PRODUCT`, `parent_chunk_data_dictionary.md_3`, `parent_chunk_data_dictionary.md_7`, `parent_chunk_data_dictionary.md_5`, `Production Lots→BATCH`, `Route Steps`

**Context previews (first 3):**

1. _Business concept 'Route Steps' — The table stores ordered manufacturing operations for a product using product_id, sequence_number, operation_name, work_center, and per-unit processing time (cycle_tim…_

2. _## work_order  Represents production jobs for manufacturing products with hierarchical work order support.  | Column | Data Type | Constraints | Description | |--------|-----------|-------------|-----…_

3. _Relationship: ROUTE references PRODUCT via foreign key PRODUCT_ID -> PRODUCT.PRODUCT_ID.…_

---

### ✅ QA-019 — How can I find which batches are stored at a specific warehouse and their QC status?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.7533 | **Gate:** `proceed`

**Expected answer:**
> Query the batch table filtering by warehouse_id. Join with the product table to get product names and types. Include production_date, quantity_produced, expiry_date, and qc_status (PENDING, PASSED, FAILED, QUARANTINED). Filter by qc_status to isolate batches requiring quality attention or ready for …

**System answer:**
> You can use the physical table **BATCH** to find batches by warehouse, because **BATCH** stores lot-level details including **warehouse_id** and **qc_status** (along with **batch_id**, **product_id**, **production_date**, etc.). Filter **BATCH** where **warehouse_id = <the warehouse you care about>**, and return **batch_id** and **qc_status** (and any other batch fields you need).

Optionally, you…

**Sources retrieved (12):** `Production Lots→BATCH`, `Actual stock levels of components and products stored in specific warehouses→INVENTORY`, `parent_chunk_data_dictionary.md_5`, `Quality Control Records→QUALITY_CONTROL`, `BATCH→WAREHOUSE`, `parent_chunk_data_dictionary.md_6`, `parent_chunk_data_dictionary.md_8`, `parent_chunk_business_glossary.md_2`

**Context previews (first 3):**

1. _Business concept 'Production Lots' — The table stores lot-level production details such as batch_id, product_id, production_date, quantity_produced, warehouse_id, expiry_date, and qc_status, which dir…_

2. _Business concept 'Actual stock levels of components and products stored in specific warehouses' is implemented by physical table INVENTORY (columns: inventory_id, warehouse_id, component_id, product_i…_

3. _## warehouse  Stores physical storage location information for inventory management.  | Column | Data Type | Constraints | Description | |--------|-----------|-------------|-------------| | warehouse_…_

---

### ✅ QA-020 — How do I identify which specifications apply to specific components?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.2613 | **Gate:** `proceed`

**Expected answer:**
> Query the component table and join with the specification table via specification_id. Include component_name, component_category, and specification details (specification_name, spec_type, critical_parameter, min_value, max_value, unit_of_measure). This shows the technical requirements that each comp…

**System answer:**
> You can identify the specifications that apply to specific components by using the optional link from the component record to the specification record.

In the schema, the business concept “Component Cost and Spec” is implemented by the physical table `COMPONENT`, which includes an optional `specification_id` column. This aligns with the concept that components can optionally be linked to technica…

**Sources retrieved (12):** `Component Cost and Spec→COMPONENT`, `parent_chunk_data_dictionary.md_5`, `parent_chunk_data_dictionary.md_7`, `Actual stock levels of components and products stored in specific warehouses→INVENTORY`, `parent_chunk_data_dictionary.md_3`, `Technical requirements and acceptance criteria→SPECIFICATION`, `parent_chunk_data_dictionary.md_4`, `Component approved supplier junction→COMPONENT_SUPPLIER`

**Context previews (first 3):**

1. _Business concept 'Component Cost and Spec' — The table defines atomic material parts with component_id and component_name, plus component_category for type classification, and financial fields unit_of…_

2. _## warehouse  Stores physical storage location information for inventory management.  | Column | Data Type | Constraints | Description | |--------|-----------|-------------|-------------| | warehouse_…_

3. _## specification  Defines technical requirements and acceptance criteria for materials and products.  | Column | Data Type | Constraints | Description | |--------|-----------|-------------|-----------…_

---

### ✅ QA-021 — How can I perform a complete BOM explosion to find all components required for a finished product?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.3509 | **Gate:** `proceed`

**Expected answer:**
> Use a recursive query starting from the product_id of the finished good. At each level, join the bom table to find component_product_id entries. For each component, check if product_type is 'ASSEMBLY' or 'FINISHED_GOOD'. If so, recursively query bom again using that component_product_id as the new p…

**System answer:**
> To perform a complete BOM explosion (i.e., find all components/sub-assemblies at all hierarchy levels) for a finished product, use the recursive product structure defined by the `bom` table.

The `bom` table models each BOM entry with `parent_product_id` (the item being built) and `component_product_id` (the required component/sub-assembly), and it supports multi-level assemblies through repeated …

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_4`, `parent_chunk_data_dictionary.md_3`, `Bill of Materials (BOM) entry (parent product and required components/sub-assemblies with quantity, unit of measure, and hierarchy level)→BOM`, `BOM→PRODUCT`, `parent_chunk_data_dictionary.md_5`, `parent_chunk_data_dictionary.md_7`, `parent_chunk_data_dictionary.md_6`, `Route Steps→ROUTE`

**Context previews (first 3):**

1. _## bom  Bill of Materials defining product composition and hierarchical structure. Supports recursive relationships for multi-level assemblies.  | Column | Data Type | Constraints | Description | |---…_

2. _# Manufacturing Data Dictionary  This data dictionary documents the database schema for the manufacturing supply chain system. It includes all tables, columns, data types, constraints, and relationshi…_

3. _Business concept 'Bill of Materials (BOM) entry (parent product and required components/sub-assemblies with quantity, unit of measure, and hierarchy level)' is implemented by physical table BOM (colum…_

---

### ✅ QA-022 — How do I calculate the total material cost for a product including all sub-assemblies?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.2332 | **Gate:** `proceed`

**Expected answer:**
> Perform a recursive BOM explosion to find all leaf-level components. For each leaf component, join with the component table to get standard_cost. Multiply standard_cost by the accumulated quantity from the BOM traversal. Sum all component costs to get total material cost. This calculation must trave…

**System answer:**
> The retrieved knowledge graph does not define an explicit “total material cost” costing rule (for example, how to identify which BOM rows count as materials versus sub-assemblies, how to treat `bom_level`, or how to incorporate `is_optional`)—so the exact end-to-end formula is not determinable from the context.

What the context does provide is the structure and the available cost inputs needed to…

**Sources retrieved (12):** `Bill of Materials (BOM) entry (parent product and required components/sub-assemblies with quantity, unit of measure, and hierarchy level)→BOM`, `parent_chunk_data_dictionary.md_3`, `parent_chunk_data_dictionary.md_4`, `parent_chunk_data_dictionary.md_7`, `parent_chunk_data_dictionary.md_8`, `Component Cost and Spec→COMPONENT`, `parent_chunk_data_dictionary.md_6`, `parent_chunk_business_glossary.md_0`

**Context previews (first 3):**

1. _Business concept 'Bill of Materials (BOM) entry (parent product and required components/sub-assemblies with quantity, unit of measure, and hierarchy level)' is implemented by physical table BOM (colum…_

2. _# Manufacturing Data Dictionary  This data dictionary documents the database schema for the manufacturing supply chain system. It includes all tables, columns, data types, constraints, and relationshi…_

3. _## bom  Bill of Materials defining product composition and hierarchical structure. Supports recursive relationships for multi-level assemblies.  | Column | Data Type | Constraints | Description | |---…_

---

### ✅ QA-023 — How can I find all parent products that contain a specific component anywhere in their BOM structure?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.5213 | **Gate:** `proceed`

**Expected answer:**
> Use a recursive reverse traversal of the BOM. Start with the component_id as the initial parent_product_id. Find all records where this product appears as component_product_id in the bom table. For each parent_product_id found, check if it appears as a component_product_id in other bom records (is a…

**System answer:**
> Use the recursive structure of the `bom` table to walk the hierarchy.

Start with the `bom` rows where `bom.component_product_id` equals the specific product/component you care about. In those rows, the `bom.parent_product_id` values are the immediate parent products that contain it.

To find parent products “anywhere” in the BOM (including indirect containment), repeatedly move upward from those …

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_4`, `Bill of Materials (BOM) entry (parent product and required components/sub-assemblies with quantity, unit of measure, and hierarchy level)→BOM`, `parent_chunk_data_dictionary.md_3`, `BOM→PRODUCT`, `PRODUCT→PRODUCT`, `parent_chunk_data_dictionary.md_6`, `parent_chunk_data_dictionary.md_8`, `parent_chunk_data_dictionary.md_5`

**Context previews (first 3):**

1. _## bom  Bill of Materials defining product composition and hierarchical structure. Supports recursive relationships for multi-level assemblies.  | Column | Data Type | Constraints | Description | |---…_

2. _Business concept 'Bill of Materials (BOM) entry (parent product and required components/sub-assemblies with quantity, unit of measure, and hierarchy level)' is implemented by physical table BOM (colum…_

3. _# Manufacturing Data Dictionary  This data dictionary documents the database schema for the manufacturing supply chain system. It includes all tables, columns, data types, constraints, and relationshi…_

---

### ✅ QA-024 — How do I identify work orders that require a specific component, considering nested sub-assemblies?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.3651 | **Gate:** `proceed`

**Expected answer:**
> First, perform reverse BOM traversal to find all parent products that contain the target component at any level. Then query the work_order table where product_id is in the set of parent products found. This includes work orders for finished goods that contain the component indirectly through sub-ass…

**System answer:**
> From the retrieved context, we can say the following pieces exist, but the exact procedure to identify which `work_order` records require a given component through nested sub-assemblies is not explicitly defined.

`Bill of Materials (BOM)` is implemented by the `bom` table, where `parent_product_id` represents the product being built and `component_product_id` represents a component/product that g…

**Sources retrieved (12):** `Bill of Materials (BOM) entry (parent product and required components/sub-assemblies with quantity, unit of measure, and hierarchy level)→BOM`, `parent_chunk_data_dictionary.md_6`, `parent_chunk_data_dictionary.md_5`, `parent_chunk_data_dictionary.md_3`, `parent_chunk_data_dictionary.md_4`, `Hierarchical production planning and tracking→WORK_ORDER`, `WORK_ORDER→WORK_ORDER`, `WORK_ORDER→PRODUCT`

**Context previews (first 3):**

1. _Business concept 'Bill of Materials (BOM) entry (parent product and required components/sub-assemblies with quantity, unit of measure, and hierarchy level)' is implemented by physical table BOM (colum…_

2. _## work_order  Represents production jobs for manufacturing products with hierarchical work order support.  | Column | Data Type | Constraints | Description | |--------|-----------|-------------|-----…_

3. _## warehouse  Stores physical storage location information for inventory management.  | Column | Data Type | Constraints | Description | |--------|-----------|-------------|-------------| | warehouse_…_

---

### ✅ QA-025 — How can I determine the maximum BOM depth level for any product?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.2424 | **Gate:** `proceed`

**Expected answer:**
> Use a recursive query on the bom table, incrementing a level counter at each traversal. Start with bom_level = 0 and add 1 for each recursive step. Track the maximum level reached across all product hierarchies. This identifies the most complex product structures with the deepest nesting.

**System answer:**
> You can use the `bom` table’s `bom_level` column, which “tracks depth in product hierarchy.” To determine the maximum BOM depth level for each product, compute `MAX(bom.bom_level)` grouped by the product being built, i.e., `bom.parent_product_id` (since `parent_product_id` is the “Parent product (what is being built)” in `bom`).

This gives, for each `product_id` appearing as a `parent_product_id`…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_4`, `parent_chunk_data_dictionary.md_3`, `Bill of Materials (BOM) entry (parent product and required components/sub-assemblies with quantity, unit of measure, and hierarchy level)→BOM`, `BOM→PRODUCT`, `parent_chunk_data_dictionary.md_7`, `parent_chunk_data_dictionary.md_5`, `parent_chunk_data_dictionary.md_6`, `Actual stock levels of components and products stored in specific warehouses→INVENTORY`

**Context previews (first 3):**

1. _## bom  Bill of Materials defining product composition and hierarchical structure. Supports recursive relationships for multi-level assemblies.  | Column | Data Type | Constraints | Description | |---…_

2. _# Manufacturing Data Dictionary  This data dictionary documents the database schema for the manufacturing supply chain system. It includes all tables, columns, data types, constraints, and relationshi…_

3. _Business concept 'Bill of Materials (BOM) entry (parent product and required components/sub-assemblies with quantity, unit of measure, and hierarchy level)' is implemented by physical table BOM (colum…_

---

### ✅ QA-026 — How do I find all products that have a specific product as a sub-assembly at any level?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.3223 | **Gate:** `proceed`

**Expected answer:**
> Perform a recursive search starting with the target product_id as the initial component_product_id in the bom table. For each parent_product_id found, check if that parent appears as a component in other bom entries. Continue recursively until reaching products that are not used as components elsewh…

**System answer:**
> Use the `bom` table (schema: `bom_id, parent_product_id, component_product_id, quantity, unit_of_measure, bom_level, is_optional`) to find products that include a given product anywhere in their multi-level bill of materials.

Because `bom` represents the hierarchical composition and has recursive relationships (both `parent_product_id` and `component_product_id` reference `product(product_id)`), …

**Sources retrieved (12):** `Bill of Materials (BOM) entry (parent product and required components/sub-assemblies with quantity, unit of measure, and hierarchy level)→BOM`, `parent_chunk_data_dictionary.md_3`, `parent_chunk_data_dictionary.md_4`, `parent_chunk_data_dictionary.md_5`, `Actual stock levels of components and products stored in specific warehouses→INVENTORY`, `parent_chunk_data_dictionary.md_7`, `parent_chunk_data_dictionary.md_6`, `parent_chunk_data_dictionary.md_8`

**Context previews (first 3):**

1. _Business concept 'Bill of Materials (BOM) entry (parent product and required components/sub-assemblies with quantity, unit of measure, and hierarchy level)' is implemented by physical table BOM (colum…_

2. _# Manufacturing Data Dictionary  This data dictionary documents the database schema for the manufacturing supply chain system. It includes all tables, columns, data types, constraints, and relationshi…_

3. _## bom  Bill of Materials defining product composition and hierarchical structure. Supports recursive relationships for multi-level assemblies.  | Column | Data Type | Constraints | Description | |---…_

---

### ✅ QA-027 — How can I calculate the total lead time for a product including all sub-assembly lead times?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.3462 | **Gate:** `proceed`

**Expected answer:**
> Perform a recursive BOM explosion to find all components and sub-assemblies. For each product_id in the hierarchy, retrieve lead_time_days from the product table. The total lead time is the maximum of all lead times in the hierarchy (representing the longest dependency chain), or optionally sum lead…

**System answer:**
> From the schema, you can retrieve the lead time values you need, but the knowledge graph does not define a specific “total lead time” calculation rule (for example, whether to sum, take the maximum, or use any critical-path logic) across a BOM hierarchy.

To get the data required for a product’s sub-assemblies, you can use these definitions:

1) The per-product lead time is stored on `product.lead…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_3`, `product_id, sequence_number→PRODUCT`, `Component approved supplier junction→COMPONENT_SUPPLIER`, `Bill of Materials (BOM) entry (parent product and required components/sub-assemblies with quantity, unit of measure, and hierarchy level)→BOM`, `parent_chunk_data_dictionary.md_4`, `Route Steps→ROUTE`, `parent_chunk_data_dictionary.md_7`, `parent_chunk_business_glossary.md_0`

**Context previews (first 3):**

1. _# Manufacturing Data Dictionary  This data dictionary documents the database schema for the manufacturing supply chain system. It includes all tables, columns, data types, constraints, and relationshi…_

2. _Business concept 'product_id, sequence_number' is implemented by physical table PRODUCT (columns: product_id, product_name, product_type, parent_product_id, base_cost, lead_time_days, is_active).…_

3. _Business concept 'Component approved supplier junction' — The table is explicitly a many-to-many junction between components and suppliers, with the DDL comment stating it links components to their ap…_

---

### ✅ QA-028 — How do I generate a complete indented BOM report showing the hierarchical structure?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.4180 | **Gate:** `proceed`

**Expected answer:**
> Use a recursive query on the bom table that tracks the current depth level. Start with the top-level product (parent_product_id where product has no parent_product_id). At each level, output component details indented by depth level. Include product_name, quantity, and unit_of_measure. Recursively p…

**System answer:**
> To generate a complete indented BOM report from this schema, you use the recursive structure captured in the `bom` table (business concept “Bill of Materials (BOM) entry … with quantity … unit of measure, and hierarchy level” implemented by `bom`).

Start by choosing a top-level product (the schema supports “Level 0” finished goods as the root of the hierarchy). Then recursively expand the hierarc…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_4`, `parent_chunk_data_dictionary.md_3`, `Bill of Materials (BOM) entry (parent product and required components/sub-assemblies with quantity, unit of measure, and hierarchy level)→BOM`, `parent_chunk_data_dictionary.md_6`, `parent_chunk_data_dictionary.md_8`, `Hierarchical production planning and tracking→WORK_ORDER`, `BOM→PRODUCT`, `parent_chunk_business_glossary.md_0`

**Context previews (first 3):**

1. _## bom  Bill of Materials defining product composition and hierarchical structure. Supports recursive relationships for multi-level assemblies.  | Column | Data Type | Constraints | Description | |---…_

2. _# Manufacturing Data Dictionary  This data dictionary documents the database schema for the manufacturing supply chain system. It includes all tables, columns, data types, constraints, and relationshi…_

3. _Business concept 'Bill of Materials (BOM) entry (parent product and required components/sub-assemblies with quantity, unit of measure, and hierarchy level)' is implemented by physical table BOM (colum…_

---

### ✅ QA-029 — How can I find which components appear most frequently across all product BOMs?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.1587 | **Gate:** `proceed_with_warning`

**Expected answer:**
> Perform BOM explosion for all products and aggregate occurrences of each leaf-level component. Count how many distinct product hierarchies contain each component. Join with component table for component names. Order by frequency descending to identify common components that should be prioritized for…

**System answer:**
> You can use the BOM table `bom` to aggregate by `component_product_id` and rank by frequency.

In `bom` (columns include `component_product_id` and `parent_product_id`), each row represents a required component in a parent product’s Bill of Materials. So to find the most frequently used components across all product BOMs, count how many `bom` rows exist per `component_product_id` and sort descendi…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_4`, `Bill of Materials (BOM) entry (parent product and required components/sub-assemblies with quantity, unit of measure, and hierarchy level)→BOM`, `parent_chunk_data_dictionary.md_3`, `BOM→PRODUCT`, `parent_chunk_data_dictionary.md_5`, `Actual stock levels of components and products stored in specific warehouses→INVENTORY`, `parent_chunk_data_dictionary.md_7`, `Component approved supplier junction→COMPONENT_SUPPLIER`

**Context previews (first 3):**

1. _## bom  Bill of Materials defining product composition and hierarchical structure. Supports recursive relationships for multi-level assemblies.  | Column | Data Type | Constraints | Description | |---…_

2. _Business concept 'Bill of Materials (BOM) entry (parent product and required components/sub-assemblies with quantity, unit of measure, and hierarchy level)' is implemented by physical table BOM (colum…_

3. _# Manufacturing Data Dictionary  This data dictionary documents the database schema for the manufacturing supply chain system. It includes all tables, columns, data types, constraints, and relationshi…_

---

### ✅ QA-030 — How do I detect circular references in the BOM structure to prevent infinite loops?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.1295 | **Gate:** `proceed_with_warning`

**Expected answer:**
> Use a recursive query with a cycle detection check. Track the path of visited product_ids at each recursion level. If a product_id appears twice in the same path, a circular reference exists. Alternatively, check if any bom record has parent_product_id = component_product_id (direct self-reference),…

**System answer:**
> I cannot find this information in the knowledge graph.

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_4`, `parent_chunk_data_dictionary.md_3`, `BOM→PRODUCT`, `Bill of Materials (BOM) entry (parent product and required components/sub-assemblies with quantity, unit of measure, and hierarchy level)→BOM`, `parent_chunk_data_dictionary.md_8`, `parent_chunk_data_dictionary.md_7`, `Technical requirements and acceptance criteria→SPECIFICATION`, `parent_chunk_business_glossary.md_0`

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
> To determine the complete supplier chain for a finished product (including suppliers for all sub-assemblies), you can combine the BOM recursion with the component-to-supplier junction defined in the schema.

First, start from the finished product in the `product` table (where `product_type` identifies it as `FINISHED_GOOD`, and the hierarchy is supported by `parent_product_id`). Then use the `bom`…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_3`, `Bill of Materials (BOM) entry (parent product and required components/sub-assemblies with quantity, unit of measure, and hierarchy level)→BOM`, `parent_chunk_data_dictionary.md_4`, `parent_chunk_data_dictionary.md_8`, `Component approved supplier junction→COMPONENT_SUPPLIER`, `parent_chunk_data_dictionary.md_6`, `External Supplier→SUPPLIER`, `parent_chunk_business_glossary.md_0`

**Context previews (first 3):**

1. _# Manufacturing Data Dictionary  This data dictionary documents the database schema for the manufacturing supply chain system. It includes all tables, columns, data types, constraints, and relationshi…_

2. _Business concept 'Bill of Materials (BOM) entry (parent product and required components/sub-assemblies with quantity, unit of measure, and hierarchy level)' is implemented by physical table BOM (colum…_

3. _## bom  Bill of Materials defining product composition and hierarchical structure. Supports recursive relationships for multi-level assemblies.  | Column | Data Type | Constraints | Description | |---…_

---

### ✅ QA-032 — How do I check if sufficient inventory exists across all warehouses to fulfill a work order?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.4035 | **Gate:** `proceed`

**Expected answer:**
> For the work_order's product_id, perform recursive BOM explosion to get all required components with quantities. For each component, sum the available quantity (quantity_on_hand - quantity_reserved) across all warehouses from the inventory table. Compare aggregated available inventory against requir…

**System answer:**
> From the retrieved context, you can identify what data would be needed, but the knowledge graph does not define the rule for how inventory sufficiency for a `work_order` should be computed.

What the context does provide:

`work_order` includes `product_id` (the product to manufacture) and `quantity_ordered`, plus a `warehouse_id` indicating the production location and a `status`.  
`inventory` st…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_5`, `parent_chunk_data_dictionary.md_6`, `Actual stock levels of components and products stored in specific warehouses→INVENTORY`, `INVENTORY→WAREHOUSE`, `WORK_ORDER→WAREHOUSE`, `Hierarchical production planning and tracking→WORK_ORDER`, `parent_chunk_data_dictionary.md_8`, `parent_chunk_business_glossary.md_1`

**Context previews (first 3):**

1. _## warehouse  Stores physical storage location information for inventory management.  | Column | Data Type | Constraints | Description | |--------|-----------|-------------|-------------| | warehouse_…_

2. _## work_order  Represents production jobs for manufacturing products with hierarchical work order support.  | Column | Data Type | Constraints | Description | |--------|-----------|-------------|-----…_

3. _Business concept 'Actual stock levels of components and products stored in specific warehouses' is implemented by physical table INVENTORY (columns: inventory_id, warehouse_id, component_id, product_i…_

---

### ✅ QA-033 — How can I find which quality control inspections failed for components from specific suppliers?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.4561 | **Gate:** `proceed`

**Expected answer:**
> Query the quality_control table filtering by result = 'FAIL'. Join with the batch table to get product_id and production_date. Join with the bom table recursively to trace which products contain failed components. Join with component_supplier and supplier tables to identify the source supplier. Filt…

**System answer:**
> From the context, you can identify failed quality control inspections using the quality control tables/concepts alone, but you cannot determine which failures are specifically “for components from specific suppliers” because the knowledge graph does not show any join/relationship connecting QC records (or their batches/specifications) to suppliers.

For failed inspections, the business concept **“…

**Sources retrieved (12):** `Quality Control Records→QUALITY_CONTROL`, `Component approved supplier junction→COMPONENT_SUPPLIER`, `parent_chunk_data_dictionary.md_5`, `parent_chunk_data_dictionary.md_3`, `Actual stock levels of components and products stored in specific warehouses→INVENTORY`, `External Supplier→SUPPLIER`, `parent_chunk_business_glossary.md_2`, `parent_chunk_business_glossary.md_0`

**Context previews (first 3):**

1. _Business concept 'Quality Control Records' — The table stores inspection/testing attributes for quality assurance, including inspection date (qc_date), inspection type (qc_type), inspector (inspector_…_

2. _Business concept 'Component approved supplier junction' — The table is explicitly a many-to-many junction between components and suppliers, with the DDL comment stating it links components to their ap…_

3. _## warehouse  Stores physical storage location information for inventory management.  | Column | Data Type | Constraints | Description | |--------|-----------|-------------|-------------| | warehouse_…_

---

### ✅ QA-034 — How do I calculate the total manufacturing time for a work order including all sub-assembly work orders?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.1599 | **Gate:** `proceed_with_warning`

**Expected answer:**
> Query the work_order table starting with the parent work_order. Find all child work_orders where parent_work_order matches the current work_order_id. For each work order (parent and children), join with the route table on product_id to get all operations. Sum (cycle_time_minutes * quantity) plus set…

**System answer:**
> I cannot find this information in the knowledge graph.  

The context defines `WORK_ORDER` (including hierarchical decomposition via `parent_work_order`) and separately defines `ROUTE` “Route Steps” time fields (`cycle_time_minutes`, `setup_time_minutes`), but it does not describe how a `work_order` is tied to a `ROUTE`, nor does it provide any method or formula for computing a work order’s per-un…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_6`, `Route Steps→ROUTE`, `parent_chunk_data_dictionary.md_3`, `Bill of Materials (BOM) entry (parent product and required components/sub-assemblies with quantity, unit of measure, and hierarchy level)→BOM`, `Hierarchical production planning and tracking→WORK_ORDER`, `parent_chunk_data_dictionary.md_7`, `parent_chunk_data_dictionary.md_5`, `parent_chunk_data_dictionary.md_4`

**Context previews (first 3):**

1. _## work_order  Represents production jobs for manufacturing products with hierarchical work order support.  | Column | Data Type | Constraints | Description | |--------|-----------|-------------|-----…_

2. _Business concept 'Route Steps' — The table stores ordered manufacturing operations for a product using product_id, sequence_number, operation_name, work_center, and per-unit processing time (cycle_tim…_

3. _# Manufacturing Data Dictionary  This data dictionary documents the database schema for the manufacturing supply chain system. It includes all tables, columns, data types, constraints, and relationshi…_

---

### ✅ QA-035 — How can I identify which shipments are overdue and their impact on work orders?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0719 | **Gate:** `proceed_with_warning`

**Expected answer:**
> Query the shipment table filtering for status = 'SHIPPED' where actual_arrival is NULL and estimated_arrival is in the past (overdue). Join with the component_supplier table via supplier_id and component_id to identify which components are delayed. Perform reverse BOM lookup to find which parent pro…

**System answer:**
> I cannot find an explicit business rule in the retrieved context for what “overdue” means for shipments, so overdue shipments cannot be identified purely from the schema without an additional definition (for example, what cutoff date to use and which shipment states count as “not overdue”).

What the context does provide to support an overdue definition is the shipment date and status data in tabl…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_5`, `parent_chunk_data_dictionary.md_8`, `parent_chunk_data_dictionary.md_6`, `Shipment Dates→SHIPMENT`, `WORK_ORDER→PRODUCT`, `WORK_ORDER→WAREHOUSE`, `Hierarchical production planning and tracking→WORK_ORDER`, `SHIPMENT→WAREHOUSE`

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
> From the retrieved context, you can identify expiry at the batch level using the `BATCH` table’s `expiry_date` column (there is no other expiry-specific field shown). However, the context does not define any “approaching” expiry window or threshold logic (e.g., a specific number of days before expiry), so you’d need an explicit rule that is not present in the provided schema metadata.

For “compon…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_5`, `Actual stock levels of components and products stored in specific warehouses→INVENTORY`, `Production Lots→BATCH`, `parent_chunk_data_dictionary.md_7`, `parent_chunk_data_dictionary.md_3`, `Component approved supplier junction→COMPONENT_SUPPLIER`, `parent_chunk_business_glossary.md_2`, `parent_chunk_business_glossary.md_1`

**Context previews (first 3):**

1. _## warehouse  Stores physical storage location information for inventory management.  | Column | Data Type | Constraints | Description | |--------|-----------|-------------|-------------| | warehouse_…_

2. _Business concept 'Actual stock levels of components and products stored in specific warehouses' is implemented by physical table INVENTORY (columns: inventory_id, warehouse_id, component_id, product_i…_

3. _Business concept 'Production Lots' — The table stores lot-level production details such as batch_id, product_id, production_date, quantity_produced, warehouse_id, expiry_date, and qc_status, which dir…_

---

### ✅ QA-037 — How can I generate a material requirements plan showing when to order components based on work order schedules?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0433 | **Gate:** `proceed_with_warning`

**Expected answer:**
> Query all work_orders with status 'PENDING' ordered by planned_start_date. For each work_order, perform BOM explosion to get required components and quantities. For each component, query inventory for current available stock across warehouses. Calculate net requirements = (required quantity * work_o…

**System answer:**
> To generate a material requirements plan (MRP) from the available schema, you can drive the calculation from work schedules, expand required components through the BOM, and then incorporate lead time from the component’s product record.

First, use `work_order` as the production schedule source. The table provides `planned_start_date` and `planned_end_date` along with `quantity_ordered`, `quantity…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_6`, `Bill of Materials (BOM) entry (parent product and required components/sub-assemblies with quantity, unit of measure, and hierarchy level)→BOM`, `parent_chunk_data_dictionary.md_7`, `Component Cost and Spec→COMPONENT`, `parent_chunk_data_dictionary.md_5`, `parent_chunk_data_dictionary.md_4`, `Hierarchical production planning and tracking→WORK_ORDER`, `parent_chunk_data_dictionary.md_3`

**Context previews (first 3):**

1. _## work_order  Represents production jobs for manufacturing products with hierarchical work order support.  | Column | Data Type | Constraints | Description | |--------|-----------|-------------|-----…_

2. _Business concept 'Bill of Materials (BOM) entry (parent product and required components/sub-assemblies with quantity, unit of measure, and hierarchy level)' is implemented by physical table BOM (colum…_

3. _## specification  Defines technical requirements and acceptance criteria for materials and products.  | Column | Data Type | Constraints | Description | |--------|-----------|-------------|-----------…_

---

### ✅ QA-038 — How do I trace the complete genealogy of a component from supplier through batch to finished goods?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0748 | **Gate:** `proceed_with_warning`

**Expected answer:**
> Start with a shipment from the supplier (shipment table with supplier_id and shipment_type = 'INBOUND'). Track to inventory updates via component_id and warehouse_id. Identify batches that consumed the component via reverse BOM lookup (batch.product_id → bom hierarchy → component_id). Query quality_…

**System answer:**
> From the retrieved schema and concepts, you can trace parts of the genealogy, but the context does not provide enough explicit relationships to trace a *complete* supplier → component → batch (consumed) → finished-goods genealogy end to end.

What you can determine from the context:

1) Supplier → Component (approved sourcing)
The table concept/component “Component approved supplier junction” is i…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_3`, `parent_chunk_data_dictionary.md_7`, `parent_chunk_data_dictionary.md_5`, `parent_chunk_data_dictionary.md_8`, `Production Lots→BATCH`, `parent_chunk_data_dictionary.md_4`, `Component approved supplier junction→COMPONENT_SUPPLIER`, `parent_chunk_business_glossary.md_2`

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
> The knowledge graph does not define what the business phrase “critical for multiple products” means. However, you can derive a reasonable proxy from the schema by treating a component as “critical for multiple products” when it appears in the `bom` table as the same `component_product_id` under multiple distinct `parent_product_id` values.

Once you identify those components from `bom`, you can fi…

**Sources retrieved (12):** `Component approved supplier junction→COMPONENT_SUPPLIER`, `parent_chunk_data_dictionary.md_4`, `parent_chunk_data_dictionary.md_3`, `External Supplier→SUPPLIER`, `parent_chunk_data_dictionary.md_5`, `parent_chunk_data_dictionary.md_8`, `parent_chunk_data_dictionary.md_7`, `parent_chunk_business_glossary.md_0`

**Context previews (first 3):**

1. _Business concept 'Component approved supplier junction' — The table is explicitly a many-to-many junction between components and suppliers, with the DDL comment stating it links components to their ap…_

2. _## bom  Bill of Materials defining product composition and hierarchical structure. Supports recursive relationships for multi-level assemblies.  | Column | Data Type | Constraints | Description | |---…_

3. _# Manufacturing Data Dictionary  This data dictionary documents the database schema for the manufacturing supply chain system. It includes all tables, columns, data types, constraints, and relationshi…_

---

### ✅ QA-040 — How do I calculate the total landed cost for a product including component costs, supplier lead times, and manufacturing operations?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.1922 | **Gate:** `proceed_with_warning`

**Expected answer:**
> Perform recursive BOM explosion to get all leaf components. For each component, query component_supplier to get unit_price from primary supplier. Multiply by accumulated BOM quantity for material cost. Add shipping costs (estimated from shipment history). Query route table for the product to get all…

**System answer:**
> The knowledge graph provides the data elements you would need to *start* such a calculation, but it does not define any “landed cost” concept or an explicit formula/algorithm to compute it.

From the available schema/business concepts:

1) Component cost inputs  
Components have financial fields like `standard_cost` and `unit_of_measure` in the physical table `COMPONENT` (mapped from the business …

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_3`, `Component approved supplier junction→COMPONENT_SUPPLIER`, `product_id, sequence_number→PRODUCT`, `Route Steps→ROUTE`, `parent_chunk_data_dictionary.md_6`, `parent_chunk_data_dictionary.md_7`, `Component Cost and Spec→COMPONENT`, `parent_chunk_data_dictionary.md_5`

**Context previews (first 3):**

1. _# Manufacturing Data Dictionary  This data dictionary documents the database schema for the manufacturing supply chain system. It includes all tables, columns, data types, constraints, and relationshi…_

2. _Business concept 'Component approved supplier junction' — The table is explicitly a many-to-many junction between components and suppliers, with the DDL comment stating it links components to their ap…_

3. _Business concept 'product_id, sequence_number' is implemented by physical table PRODUCT (columns: product_id, product_name, product_type, parent_product_id, base_cost, lead_time_days, is_active).…_

---

## Anomalies & Observations

No anomalies detected. All questions grounded with acceptable RAGAS scores.
