# AB-04 — 04_complex_manufacturing — Run Analysis

**Timestamp:** 2026-03-31 01:20:15  
**Run tag:** `v5`

## Configuration

| Parameter | Value |
|-----------|-------|
| Extraction model | `LLM (gpt-5.4-nano-2026-03-17)` |
| Reasoning model | `gpt-5.4-2026-03-05` |
| Embedding model | `BAAI/bge-m3` |
| Retrieval mode | `hybrid` |
| Reranker | `True` |
| Reranker top_k | `5` |
| Chunk size / overlap | `256 / 32` |
| ER similarity threshold | `0.75` |

## Builder Results

Builder skipped (`--no-builder`).

## Query Evaluation Summary

| Metric | Value |
|--------|-------|
| Questions | 40 |
| Grounded | **40/40 (100%)** |
| Avg GT Coverage | 100% |
| Avg Top Score | 0.4283 |
| Avg Chunk Count | 5.0 |
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
> In the manufacturing system, a Product represents any manufactured item, including finished goods, assemblies/sub-assemblies, and components.

The provided schema shows that the `product` table stores these specific product attributes: `product_id` as the unique identifier, `product_name`, `product_type`, `parent_product_id`, `base_cost`, `lead_time_days`, and `is_active`. The `product_type` class…

**Sources retrieved (5):** `parent_chunk_data_dictionary.md_3`, `Manufacturing Routing→ROUTE`, `parent_chunk_business_glossary.md_0`, `Manufacturing Routing`, `parent_chunk_business_glossary.md_1`

**Context previews (first 3):**

1. _# Manufacturing Data Dictionary  This data dictionary documents the database schema for the manufacturing supply chain system. It includes all tables, columns, data types, constraints, and relationshi…_

2. _Business concept 'Manufacturing Routing' — The table is keyed by route_id and product_id and stores the ordered steps for a product, including route_name, sequence_number, operation_name, work_center,…_

3. _# Manufacturing Business Glossary  This glossary defines the core business concepts and terminology used in the manufacturing supply chain domain. It covers product structures, materials management, p…_

---

### ✅ QA-002 — How are components defined in the manufacturing database?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.5910 | **Gate:** `proceed`

**Expected answer:**
> Components are defined with a unique identifier (component_id), descriptive name (component_name), category grouping (component_category), unit of measure (unit_of_measure), standard unit cost (standard_cost), and optional reference to technical specifications (specification_id). Components represen…

**System answer:**
> In the retrieved context, components are defined primarily as a kind of Product. The `product` table stores finished goods, assemblies, and components, and uses `product_type` to classify them as `FINISHED_GOOD`, `ASSEMBLY`, or `COMPONENT`. So, in the database, a component is a product record whose `product_type` is `COMPONENT`.

The business glossary further defines a Component as an atomic raw m…

**Sources retrieved (5):** `parent_chunk_data_dictionary.md_3`, `parent_chunk_data_dictionary.md_4`, `parent_chunk_business_glossary.md_0`, `parent_chunk_business_glossary.md_1`, `parent_chunk_business_glossary.md_2`

**Context previews (first 3):**

1. _# Manufacturing Data Dictionary  This data dictionary documents the database schema for the manufacturing supply chain system. It includes all tables, columns, data types, constraints, and relationshi…_

2. _## bom  Bill of Materials defining product composition and hierarchical structure. Supports recursive relationships for multi-level assemblies.  | Column | Data Type | Constraints | Description | |---…_

3. _# Manufacturing Business Glossary  This glossary defines the core business concepts and terminology used in the manufacturing supply chain domain. It covers product structures, materials management, p…_

---

### ✅ QA-003 — What is the purpose of the Bill of Materials (BOM) table?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.9118 | **Gate:** `proceed`

**Expected answer:**
> The BOM table defines the hierarchical structure of products by specifying which components or sub-assemblies are required to manufacture each parent product. It records the unique BOM entry identifier (bom_id), parent product being built (parent_product_id), component or sub-assembly product (compo…

**System answer:**
> The Bill of Materials table, `bom`, defines product composition and hierarchical structure. Its purpose is to represent what components go into a parent product, including the required quantity, unit of measure, hierarchy depth (`bom_level`), and whether a component is optional.

From the context, `bom` supports recursive, multi-level assemblies because both `parent_product_id` and `component_prod…

**Sources retrieved (5):** `parent_chunk_data_dictionary.md_4`, `BOM→PRODUCT`, `BOM entry→BOM`, `parent_chunk_data_dictionary.md_3`, `parent_chunk_business_glossary.md_0`

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
> The system maintains supplier information in the SUPPLIER table, which stores external vendor information for component procurement. From the retrieved context, the supplier data includes supplier_id, supplier_name, contact_email, contact_phone, rating, and is_preferred.

Specifically, supplier_id is the unique supplier identifier and primary key, and supplier_name is required (NOT NULL). The is_p…

**Sources retrieved (5):** `Preferred supplier for this component→SUPPLIER`, `parent_chunk_data_dictionary.md_4`, `SHIPMENT→SUPPLIER`, `shipment type, source and destination locations, dates for ship, estimated arrival, and actual delivery, along with current status→SHIPMENT`, `parent_chunk_business_glossary.md_0`

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
> Warehouses are represented by the physical table `warehouse` (also referred to as the business concept `Warehouse`). It stores physical storage location information for inventory management and represents a physical storage location where materials, components, and finished goods are stored.

The `warehouse` table has these columns: `warehouse_id` as the primary key and unique warehouse identifier…

**Sources retrieved (5):** `parent_chunk_data_dictionary.md_6`, `parent_chunk_data_dictionary.md_5`, `Actual stock levels of components and products at specific warehouse locations→WAREHOUSE`, `parent_chunk_data_dictionary.md_8`, `parent_chunk_business_glossary.md_1`

**Context previews (first 3):**

1. _## work_order  Represents production jobs for manufacturing products with hierarchical work order support.  | Column | Data Type | Constraints | Description | |--------|-----------|-------------|-----…_

2. _## warehouse  Stores physical storage location information for inventory management.  | Column | Data Type | Constraints | Description | |--------|-----------|-------------|-------------| | warehouse_…_

3. _Business concept 'Actual stock levels of components and products at specific warehouse locations' is implemented by physical table WAREHOUSE (columns: warehouse_id, warehouse_name, address, city, stat…_

---

### ✅ QA-006 — What does the inventory table track?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.5349 | **Gate:** `proceed`

**Expected answer:**
> The inventory table tracks real-time stock levels including a unique record identifier (inventory_id), warehouse location (warehouse_id), component identifier for materials (component_id) or product identifier for finished goods (product_id), current physical stock quantity (quantity_on_hand), quant…

**System answer:**
> The INVENTORY table tracks the actual stock levels of components and products stored in specific warehouses. It records, for each inventory entry, the warehouse, either a component or a product (but not both in the same record), the quantity on hand, the quantity reserved for pending orders, the reorder threshold, and the last restock date.

From the context, INVENTORY is the physical table implem…

**Sources retrieved (5):** `INVENTORY→PRODUCT`, `INVENTORY→WAREHOUSE`, `INVENTORY→COMPONENT`, `Actual stock levels of components and products at specific warehouse locations→INVENTORY`, `parent_chunk_business_glossary.md_1`

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
> Work orders are structured as production jobs in the `work_order` table, with support for both single jobs and hierarchical decomposition.

Each work order is uniquely identified by `work_order_id` (primary key) and is tied to a product through `product_id`, which is a required foreign key to `product(product_id)`. This means work orders are used to manufacture products defined in the product stru…

**Sources retrieved (5):** `parent_chunk_data_dictionary.md_6`, `Manufacturing Routing→ROUTE`, `parent_chunk_business_glossary.md_0`, `parent_chunk_business_glossary.md_1`, `Manufacturing Routing`

**Context previews (first 3):**

1. _## work_order  Represents production jobs for manufacturing products with hierarchical work order support.  | Column | Data Type | Constraints | Description | |--------|-----------|-------------|-----…_

2. _Business concept 'Manufacturing Routing' — The table is keyed by route_id and product_id and stores the ordered steps for a product, including route_name, sequence_number, operation_name, work_center,…_

3. _# Manufacturing Business Glossary  This glossary defines the core business concepts and terminology used in the manufacturing supply chain domain. It covers product structures, materials management, p…_

---

### ✅ QA-008 — What information is captured in the shipment table?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.8695 | **Gate:** `proceed`

**Expected answer:**
> Shipments track material transfers with a unique identifier (shipment_id), shipment type (INBOUND from suppliers, OUTBOUND to customers, INTERNAL between warehouses), destination warehouse (warehouse_id), source supplier for inbound (supplier_id), destination customer for outbound (customer_id), shi…

**System answer:**
> The `SHIPMENT` table captures information about material transfers between warehouses, suppliers, and customers. It implements the business concept of shipment type, source and destination locations, shipping and arrival dates, and current status.

Specifically, it stores:

`shipment_id`: the unique shipment identifier.

`shipment_type`: the type of shipment, with allowed values `INBOUND`, `OUTBOU…

**Sources retrieved (5):** `shipment type, source and destination locations, dates for ship, estimated arrival, and actual delivery, along with current status→SHIPMENT`, `SHIPMENT→WAREHOUSE`, `SHIPMENT→SUPPLIER`, `parent_chunk_data_dictionary.md_8`, `shipment type, source and destination locations, dates for ship, estimated arrival, and actual delivery, along with current status`

**Context previews (first 3):**

1. _Business concept 'shipment type, source and destination locations, dates for ship, estimated arrival, and actual delivery, along with current status' is implemented by physical table SHIPMENT (columns…_

2. _Relationship: SHIPMENT references WAREHOUSE via foreign key WAREHOUSE_ID -> WAREHOUSE.WAREHOUSE_ID.…_

3. _Relationship: SHIPMENT references SUPPLIER via foreign key SUPPLIER_ID -> SUPPLIER.SUPPLIER_ID.…_

---

### ✅ QA-009 — How does the quality control system record inspections?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.9540 | **Gate:** `proceed`

**Expected answer:**
> Quality control records are stored with a unique identifier (qc_id), associated production batch (batch_id), applicable specification requirements (specification_id), inspection date (qc_date), inspection type (INCOMING for supplier materials, IN_PROCESS during manufacturing, FINAL for finished good…

**System answer:**
> The quality control system records inspections in the physical table QUALITY_CONTROL, which implements the business concept “inspection and testing records for quality assurance.”

Inspections are recorded as QC records with these columns: qc_id, batch_id, specification_id, qc_date, qc_type, inspector_id, result, defect_count, and notes.

From the QualityControl concept, this means each inspection…

**Sources retrieved (5):** `inspection and testing records for quality assurance→QUALITY_CONTROL`, `BOM→PRODUCT`, `parent_chunk_business_glossary.md_2`, `inspection and testing records for quality assurance`, `parent_chunk_business_glossary.md_0`

**Context previews (first 3):**

1. _Business concept 'inspection and testing records for quality assurance' is implemented by physical table QUALITY_CONTROL (columns: qc_id, batch_id, specification_id, qc_date, qc_type, inspector_id, re…_

2. _Relationship: BOM references PRODUCT via foreign key COMPONENT_PRODUCT_ID -> PRODUCT.PRODUCT_ID.…_

3. _## QualityControl  Quality Control (QC) represents inspection and testing activities performed on materials, in-process production, or finished goods. QC records track the type of inspection (incoming…_

---

### ✅ QA-010 — What do specification records define?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.7558 | **Gate:** `proceed`

**Expected answer:**
> Specifications define technical requirements with a unique identifier (specification_id), descriptive name (specification_name), version number, effective date, specification type (DIMENSIONAL, MATERIAL, PERFORMANCE), critical parameter being measured (critical_parameter), acceptable minimum value (…

**System answer:**
> Specification records define the technical requirements, standards, and acceptance criteria for materials or products. In the `SPECIFICATION` table, they capture the specification name and version, effective date, specification type (`DIMENSIONAL`, `MATERIAL`, or `PERFORMANCE`), the critical parameter being tested, acceptable minimum and maximum values, and the unit of measure. These records serve…

**Sources retrieved (5):** `inspection and testing records for quality assurance→QUALITY_CONTROL`, `parent_chunk_data_dictionary.md_7`, `Technical specification reference→SPECIFICATION`, `parent_chunk_business_glossary.md_2`, `parent_chunk_business_glossary.md_0`

**Context previews (first 3):**

1. _Business concept 'inspection and testing records for quality assurance' is implemented by physical table QUALITY_CONTROL (columns: qc_id, batch_id, specification_id, qc_date, qc_type, inspector_id, re…_

2. _## specification  Defines technical requirements and acceptance criteria for materials and products.  | Column | Data Type | Constraints | Description | |--------|-----------|-------------|-----------…_

3. _Business concept 'Technical specification reference' is implemented by physical table SPECIFICATION (columns: specification_id, specification_name, version, effective_date, spec_type, critical_paramet…_

---

### ✅ QA-011 — How can I find which suppliers provide specific components?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.2379 | **Gate:** `proceed`

**Expected answer:**
> Query the component_supplier table which links components to their approved suppliers. This table contains the component identifier (component_id), supplier identifier (supplier_id), preferred supplier flag (is_preferred), lead time in days (lead_time_days), and unit price (unit_price). Join with th…

**System answer:**
> Use the Component Supplier Relationship table. The retrieved context defines it as a junction entity that links one component to one supplier through a unique component_id / supplier_id pair.

To find which suppliers provide a specific component, trace the relationship by component_id:
join the target component on Component Supplier Relationship.component_id, then join Component Supplier Relations…

**Sources retrieved (5):** `parent_chunk_data_dictionary.md_5`, `parent_chunk_data_dictionary.md_4`, `parent_chunk_business_glossary.md_0`, `parent_chunk_business_glossary.md_1`, `Component Supplier Relationship`

**Context previews (first 3):**

1. _## warehouse  Stores physical storage location information for inventory management.  | Column | Data Type | Constraints | Description | |--------|-----------|-------------|-------------| | warehouse_…_

2. _## bom  Bill of Materials defining product composition and hierarchical structure. Supports recursive relationships for multi-level assemblies.  | Column | Data Type | Constraints | Description | |---…_

3. _# Manufacturing Business Glossary  This glossary defines the core business concepts and terminology used in the manufacturing supply chain domain. It covers product structures, materials management, p…_

---

### ✅ QA-012 — How do I trace which components are needed to fulfill a work order?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.2334 | **Gate:** `proceed`

**Expected answer:**
> Start with the work_order table to get the product_id being manufactured. Join to the bom table using product_id as parent_product_id to find all direct components and sub-assemblies. For each component_product_id, if it is an ASSEMBLY type product, recursively query the bom table again to explode m…

**System answer:**
> From the retrieved context, you can trace a work order to the product being built and to the warehouse where production is staged, but you cannot derive the exact required component list or component quantities because the context does not include a physical bill-of-materials table or any explicit product-to-component relationship.

The schema-level trace that is supported is this: start in WORK_O…

**Sources retrieved (5):** `parent_chunk_data_dictionary.md_5`, `Hierarchical production planning and tracking→WORK_ORDER`, `parent_chunk_data_dictionary.md_6`, `parent_chunk_business_glossary.md_1`, `parent_chunk_business_glossary.md_0`

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
> Use the INVENTORY table, joined to WAREHOUSE by warehouse_id.

The relevant path is INVENTORY.warehouse_id → WAREHOUSE.warehouse_id. To identify warehouses for a specific component, filter INVENTORY.component_id to the component you care about. The schema indicates that inventory records support either components or products, but not both in the same record, so component-based inventory is represe…

**Sources retrieved (5):** `Actual stock levels of components and products at specific warehouse locations→INVENTORY`, `parent_chunk_data_dictionary.md_5`, `Actual stock levels of components and products at specific warehouse locations→WAREHOUSE`, `Actual stock levels of components and products at specific warehouse locations`, `parent_chunk_business_glossary.md_1`

**Context previews (first 3):**

1. _Business concept 'Actual stock levels of components and products at specific warehouse locations' is implemented by physical table INVENTORY (columns: inventory_id, warehouse_id, component_id, product…_

2. _## warehouse  Stores physical storage location information for inventory management.  | Column | Data Type | Constraints | Description | |--------|-----------|-------------|-------------| | warehouse_…_

3. _Business concept 'Actual stock levels of components and products at specific warehouse locations' is implemented by physical table WAREHOUSE (columns: warehouse_id, warehouse_name, address, city, stat…_

---

### ✅ QA-014 — How do I find which shipments delivered materials from a specific supplier?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.2401 | **Gate:** `proceed`

**Expected answer:**
> Query the shipment table filtering by supplier_id and shipment_type = 'INBOUND'. Join with the warehouse table to show destination warehouses. Filter for status = 'DELIVERED' and include actual_arrival date. Results can be ordered by ship_date descending to show most recent deliveries first.

**System answer:**
> Use the `SHIPMENT` table. A shipment delivered from a supplier is represented there by combining these facts from the context:

`SHIPMENT.supplier_id` is a foreign key to `SUPPLIER.supplier_id`.
The constraint `chk_supplier_inbound` says `supplier_id` is only set for `INBOUND` shipments.
The `status` column includes `DELIVERED`.
The table also stores `ship_date`, `estimated_arrival`, and `actual_a…

**Sources retrieved (5):** `parent_chunk_data_dictionary.md_8`, `SHIPMENT→SUPPLIER`, `shipment type, source and destination locations, dates for ship, estimated arrival, and actual delivery, along with current status→SHIPMENT`, `parent_chunk_business_glossary.md_1`, `parent_chunk_business_glossary.md_0`

**Context previews (first 3):**

1. _## shipment  Tracks material transfers between warehouses, suppliers, and customers.  | Column | Data Type | Constraints | Description | |--------|-----------|-------------|-------------| | shipment_i…_

2. _Relationship: SHIPMENT references SUPPLIER via foreign key SUPPLIER_ID -> SUPPLIER.SUPPLIER_ID.…_

3. _Business concept 'shipment type, source and destination locations, dates for ship, estimated arrival, and actual delivery, along with current status' is implemented by physical table SHIPMENT (columns…_

---

### ✅ QA-015 — How can I determine which quality control inspections were performed on a specific production batch?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.9779 | **Gate:** `proceed`

**Expected answer:**
> Query the quality_control table filtered by batch_id. Join with the specification table to get requirement details (specification_name, spec_type, acceptable ranges). Include qc_date, qc_type (INCOMING, IN_PROCESS, FINAL), result (PASS, FAIL, CONDITIONAL), and defect_count. This shows the complete i…

**System answer:**
> Use the `QUALITY_CONTROL` table, which implements the business concept “inspection and testing records for quality assurance.” It contains the batch reference and the inspection details.

To determine which inspections were performed on a specific production batch, look up all rows in `QUALITY_CONTROL` where `batch_id` matches the target batch. The relevant columns are `qc_id`, `batch_id`, `specif…

**Sources retrieved (5):** `inspection and testing records for quality assurance→QUALITY_CONTROL`, `parent_chunk_data_dictionary.md_7`, `Batches for traceability and inventory management→BATCH`, `parent_chunk_business_glossary.md_2`, `parent_chunk_business_glossary.md_1`

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
> Use the `work_order` table. It directly stores both the production location and the work order status, so to find work orders in progress at a specific warehouse, filter `work_order.status = 'IN_PROGRESS'` and `work_order.warehouse_id` to the target warehouse.

The relevant columns in `work_order` are `work_order_id`, `product_id`, `parent_work_order`, `quantity_ordered`, `quantity_completed`, `st…

**Sources retrieved (5):** `parent_chunk_data_dictionary.md_5`, `parent_chunk_data_dictionary.md_6`, `Hierarchical production planning and tracking→WORK_ORDER`, `Actual stock levels of components and products at specific warehouse locations→INVENTORY`, `parent_chunk_business_glossary.md_1`

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
> Use the `INVENTORY` table, which implements the business concept “Actual stock levels of components and products at specific warehouse locations.”

At the schema level, components that need reordering are the `INVENTORY` records where the record is for a component and the current stock is at or below the reorder trigger. From the context, that means:

- `component_id` is populated and `product_id`…

**Sources retrieved (5):** `Actual stock levels of components and products at specific warehouse locations→INVENTORY`, `parent_chunk_data_dictionary.md_5`, `parent_chunk_business_glossary.md_1`, `Actual stock levels of components and products at specific warehouse locations`, `parent_chunk_business_glossary.md_0`

**Context previews (first 3):**

1. _Business concept 'Actual stock levels of components and products at specific warehouse locations' is implemented by physical table INVENTORY (columns: inventory_id, warehouse_id, component_id, product…_

2. _## warehouse  Stores physical storage location information for inventory management.  | Column | Data Type | Constraints | Description | |--------|-----------|-------------|-------------| | warehouse_…_

3. _## Warehouse  A Warehouse represents a physical storage location where materials, components, and finished goods are stored. Warehouses have defined capacity limits, geographic location information, a…_

---

### ✅ QA-018 — How do I determine the manufacturing route for a specific product?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.8174 | **Gate:** `proceed`

**Expected answer:**
> Query the route table filtering by product_id, ordered by sequence_number ascending. For each operation, retrieve operation_name, work_center, cycle_time_minutes, and setup_time_minutes. Join with the product table to get product details. The sequence of operations shows the complete manufacturing w…

**System answer:**
> To determine the manufacturing route for a specific product, use the physical table ROUTE, which implements the business concept Manufacturing Routing.

At the schema level, the route is identified by product_id together with route_id, and the table stores the full ordered production path for that product. For the target product, filter ROUTE by product_id, then order the results by sequence_numbe…

**Sources retrieved (5):** `Manufacturing Routing→ROUTE`, `parent_chunk_data_dictionary.md_6`, `Manufacturing Routing`, `parent_chunk_business_glossary.md_2`, `parent_chunk_business_glossary.md_0`

**Context previews (first 3):**

1. _Business concept 'Manufacturing Routing' — The table is keyed by route_id and product_id and stores the ordered steps for a product, including route_name, sequence_number, operation_name, work_center,…_

2. _## work_order  Represents production jobs for manufacturing products with hierarchical work order support.  | Column | Data Type | Constraints | Description | |--------|-----------|-------------|-----…_

3. _Manufacturing Routing: The table is keyed by route_id and product_id and stores the ordered steps for a product, including route_name, sequence_number, operation_name, work_center, and timing fields. …_

---

### ✅ QA-019 — How can I find which batches are stored at a specific warehouse and their QC status?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.7533 | **Gate:** `proceed`

**Expected answer:**
> Query the batch table filtering by warehouse_id. Join with the product table to get product names and types. Include production_date, quantity_produced, expiry_date, and qc_status (PENDING, PASSED, FAILED, QUARANTINED). Filter by qc_status to isolate batches requiring quality attention or ready for …

**System answer:**
> Use the BATCH table directly. The business concept “Batches for traceability and inventory management” is implemented by BATCH, and it includes both warehouse_id and qc_status, so the warehouse location and current batch QC status are stored together on the batch record.

To find batches stored at a specific warehouse, filter BATCH by BATCH.warehouse_id for the warehouse you want. The main columns…

**Sources retrieved (5):** `Batches for traceability and inventory management→BATCH`, `parent_chunk_data_dictionary.md_5`, `Actual stock levels of components and products at specific warehouse locations→INVENTORY`, `parent_chunk_business_glossary.md_2`, `parent_chunk_business_glossary.md_1`

**Context previews (first 3):**

1. _Business concept 'Batches for traceability and inventory management' is implemented by physical table BATCH (columns: batch_id, product_id, production_date, quantity_produced, warehouse_id, expiry_dat…_

2. _## warehouse  Stores physical storage location information for inventory management.  | Column | Data Type | Constraints | Description | |--------|-----------|-------------|-------------| | warehouse_…_

3. _Business concept 'Actual stock levels of components and products at specific warehouse locations' is implemented by physical table INVENTORY (columns: inventory_id, warehouse_id, component_id, product…_

---

### ✅ QA-020 — How do I identify which specifications apply to specific components?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.2550 | **Gate:** `proceed`

**Expected answer:**
> Query the component table and join with the specification table via specification_id. Include component_name, component_category, and specification details (specification_name, spec_type, critical_parameter, min_value, max_value, unit_of_measure). This shows the technical requirements that each comp…

**System answer:**
> From the retrieved context, you cannot directly identify which specification applies to a specific component through a defined schema relationship, because no direct Component-to-Specification link is shown.

What the context does show is this:

The `specification` entity defines technical requirements and acceptance criteria for materials and products. Its identifying column is `specification_id`…

**Sources retrieved (5):** `parent_chunk_data_dictionary.md_5`, `parent_chunk_data_dictionary.md_7`, `parent_chunk_business_glossary.md_0`, `parent_chunk_business_glossary.md_2`, `parent_chunk_business_glossary.md_1`

**Context previews (first 3):**

1. _## warehouse  Stores physical storage location information for inventory management.  | Column | Data Type | Constraints | Description | |--------|-----------|-------------|-------------| | warehouse_…_

2. _## specification  Defines technical requirements and acceptance criteria for materials and products.  | Column | Data Type | Constraints | Description | |--------|-----------|-------------|-----------…_

3. _# Manufacturing Business Glossary  This glossary defines the core business concepts and terminology used in the manufacturing supply chain domain. It covers product structures, materials management, p…_

---

### ✅ QA-021 — How can I perform a complete BOM explosion to find all components required for a finished product?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.3509 | **Gate:** `proceed`

**Expected answer:**
> Use a recursive query starting from the product_id of the finished good. At each level, join the bom table to find component_product_id entries. For each component, check if product_type is 'ASSEMBLY' or 'FINISHED_GOOD'. If so, recursively query bom again using that component_product_id as the new p…

**System answer:**
> To perform a complete BOM explosion for a finished product, use the `product` and `bom` tables recursively.

Start with the finished product in `product`, using `product.product_id` as the root item. The context says `product.product_type` can be `FINISHED_GOOD`, `ASSEMBLY`, or `COMPONENT`, so the starting product should be the finished good you want to build.

Then join to `bom` on:

`bom.parent_…

**Sources retrieved (5):** `parent_chunk_data_dictionary.md_4`, `parent_chunk_data_dictionary.md_3`, `BOM entry→BOM`, `parent_chunk_business_glossary.md_0`, `parent_chunk_business_glossary.md_1`

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
> To calculate total material cost for a product including all sub-assemblies, the retrieved context supports a recursive BOM explosion over the `bom` and `product` tables.

Start from the target product in `product.product_id`. Traverse `bom` using `bom.parent_product_id = product.product_id` to find its direct components in `bom.component_product_id`. Then join `bom.component_product_id` back to `…

**Sources retrieved (5):** `parent_chunk_data_dictionary.md_3`, `parent_chunk_data_dictionary.md_4`, `Product classification: FINISHED_GOOD, ASSEMBLY, COMPONENT→COMPONENT`, `parent_chunk_business_glossary.md_0`, `parent_chunk_business_glossary.md_1`

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
> Use the `bom` table recursively.

In this schema, `bom.parent_product_id` is the product being built, and `bom.component_product_id` is the product that goes into it. Because both columns reference `product(product_id)`, and the BOM supports multi-level assemblies, you can trace containment upward through the hierarchy.

The join path is:

1. Start with the specific component’s `product_id`.
2. Fi…

**Sources retrieved (5):** `parent_chunk_data_dictionary.md_4`, `parent_chunk_data_dictionary.md_3`, `parent_chunk_data_dictionary.md_6`, `parent_chunk_business_glossary.md_0`, `parent_chunk_business_glossary.md_1`

**Context previews (first 3):**

1. _## bom  Bill of Materials defining product composition and hierarchical structure. Supports recursive relationships for multi-level assemblies.  | Column | Data Type | Constraints | Description | |---…_

2. _# Manufacturing Data Dictionary  This data dictionary documents the database schema for the manufacturing supply chain system. It includes all tables, columns, data types, constraints, and relationshi…_

3. _## work_order  Represents production jobs for manufacturing products with hierarchical work order support.  | Column | Data Type | Constraints | Description | |--------|-----------|-------------|-----…_

---

### ✅ QA-024 — How do I identify work orders that require a specific component, considering nested sub-assemblies?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.3651 | **Gate:** `proceed`

**Expected answer:**
> First, perform reverse BOM traversal to find all parent products that contain the target component at any level. Then query the work_order table where product_id is in the set of parent products found. This includes work orders for finished goods that contain the component indirectly through sub-ass…

**System answer:**
> Use the `work_order` table together with the self-referential hierarchy in `product`.

A `work_order` directly identifies what is being manufactured through `work_order.product_id → product.product_id`. The `product` table supports nested assemblies through `product.parent_product_id → product.product_id`, and the dictionary explicitly says this enables multi-level product assemblies, unlimited ne…

**Sources retrieved (5):** `parent_chunk_data_dictionary.md_6`, `parent_chunk_data_dictionary.md_5`, `parent_chunk_data_dictionary.md_3`, `parent_chunk_business_glossary.md_1`, `parent_chunk_business_glossary.md_0`

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
> Use the `bom` table’s `bom_level` column. The context explicitly says `bom_level` is the “Depth in product hierarchy,” and the table supports recursive, multi-level assemblies through `parent_product_id` and `component_product_id`, both of which reference `product(product_id)`.

If you want the maximum BOM depth in the whole system, take the maximum value of `bom.bom_level`.

If you want the maxim…

**Sources retrieved (5):** `parent_chunk_data_dictionary.md_4`, `parent_chunk_data_dictionary.md_3`, `BOM entry→BOM`, `parent_chunk_data_dictionary.md_7`, `parent_chunk_business_glossary.md_0`

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
> Use the hierarchical product relationships in the schema and traverse upward recursively from the target product.

At the BOM level, the path is:

`product.product_id` → `bom.component_product_id` → `bom.parent_product_id` → `product.product_id`

To find all products that contain a specific product as a sub-assembly at any depth, start with the target product’s `product_id` and find all `bom` rows…

**Sources retrieved (5):** `parent_chunk_data_dictionary.md_3`, `parent_chunk_data_dictionary.md_4`, `parent_chunk_data_dictionary.md_5`, `parent_chunk_business_glossary.md_0`, `parent_chunk_business_glossary.md_1`

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
> The retrieved context supports how to trace the lead times through the product structure, but it does not define the exact business rule for turning those values into a single “total lead time.”

At the schema level, the relevant source is `product.lead_time_days`, described as the procurement or production lead time for a product. To include sub-assemblies, you would start with the target row in …

**Sources retrieved (5):** `parent_chunk_data_dictionary.md_3`, `complex products→PRODUCT`, `parent_chunk_data_dictionary.md_4`, `parent_chunk_business_glossary.md_0`, `parent_chunk_business_glossary.md_1`

**Context previews (first 3):**

1. _# Manufacturing Data Dictionary  This data dictionary documents the database schema for the manufacturing supply chain system. It includes all tables, columns, data types, constraints, and relationshi…_

2. _Business concept 'complex products' is implemented by physical table PRODUCT (columns: product_id, product_name, product_type, parent_product_id, base_cost, lead_time_days, is_active).…_

3. _## bom  Bill of Materials defining product composition and hierarchical structure. Supports recursive relationships for multi-level assemblies.  | Column | Data Type | Constraints | Description | |---…_

---

### ✅ QA-028 — How do I generate a complete indented BOM report showing the hierarchical structure?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.4180 | **Gate:** `proceed`

**Expected answer:**
> Use a recursive query on the bom table that tracks the current depth level. Start with the top-level product (parent_product_id where product has no parent_product_id). At each level, output component details indented by depth level. Include product_name, quantity, and unit_of_measure. Recursively p…

**System answer:**
> Use the `bom` table as the hierarchy driver and join it to `product` twice: once for the parent item and once for the component item.

A complete indented BOM report is based on this traversal path: start with a root `product.product_id`, find its direct children in `bom` where `bom.parent_product_id = product.product_id`, then join `bom.component_product_id` back to `product(product_id)` to get t…

**Sources retrieved (5):** `parent_chunk_data_dictionary.md_4`, `parent_chunk_data_dictionary.md_3`, `parent_chunk_data_dictionary.md_6`, `parent_chunk_data_dictionary.md_8`, `parent_chunk_business_glossary.md_0`

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
> The knowledge graph only provides schema metadata, not actual BOM records, so it cannot tell you which specific components are most frequent. But the schema shows exactly how to calculate it.

Use the BOM table, which implements the business concept “BOM entry.” The relevant table is BOM with columns bom_id, parent_product_id, component_product_id, quantity, unit_of_measure, bom_level, and is_opti…

**Sources retrieved (5):** `parent_chunk_data_dictionary.md_4`, `parent_chunk_data_dictionary.md_3`, `BOM entry→BOM`, `parent_chunk_data_dictionary.md_5`, `parent_chunk_business_glossary.md_0`

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
> The context shows that the `bom` table models the hierarchy through `parent_product_id` and `component_product_id`, with each BOM row representing a parent product and one of its component products. To trace the structure across multiple levels, you would follow one BOM row’s `component_product_id` to another BOM row’s `parent_product_id`. The relevant BOM columns are `bom_id`, `parent_product_id`…

**Sources retrieved (5):** `parent_chunk_data_dictionary.md_4`, `parent_chunk_data_dictionary.md_3`, `BOM→PRODUCT`, `BOM entry→BOM`, `parent_chunk_business_glossary.md_0`

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
> From the retrieved context, you can determine the complete product structure for a finished product, but you cannot fully determine the supplier chain for each sub-assembly from the available schema metadata.

The part that is supported is the hierarchical explosion of the finished product. The `bom` table is the main structure for this. Start with the finished product in `product`, where `product…

**Sources retrieved (5):** `parent_chunk_data_dictionary.md_3`, `parent_chunk_data_dictionary.md_4`, `parent_chunk_data_dictionary.md_8`, `parent_chunk_business_glossary.md_0`, `parent_chunk_business_glossary.md_1`

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
> From the schema provided, the check is done at the product-inventory level by linking `work_order` to `inventory` through `product_id`.

Use this join path: `work_order.product_id = inventory.product_id`. If you want warehouse names or locations in the result, also join `inventory.warehouse_id = warehouse.warehouse_id`.

The relevant columns are:
`work_order.work_order_id`, `work_order.product_id`…

**Sources retrieved (5):** `parent_chunk_data_dictionary.md_5`, `parent_chunk_data_dictionary.md_6`, `Actual stock levels of components and products at specific warehouse locations→INVENTORY`, `parent_chunk_business_glossary.md_1`, `parent_chunk_business_glossary.md_0`

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
> From the retrieved context, you can only answer this partially at the schema/business-concept level.

The context says that QualityControl records include a result with values PASS, FAIL, or CONDITIONAL, and that QC inspections are associated with specific Batches and may reference Specifications. So, at a minimum, failed inspections would be the QualityControl records where the QC result is FAIL.…

**Sources retrieved (5):** `parent_chunk_data_dictionary.md_5`, `parent_chunk_data_dictionary.md_3`, `parent_chunk_business_glossary.md_2`, `parent_chunk_business_glossary.md_0`, `parent_chunk_business_glossary.md_1`

**Context previews (first 3):**

1. _## warehouse  Stores physical storage location information for inventory management.  | Column | Data Type | Constraints | Description | |--------|-----------|-------------|-------------| | warehouse_…_

2. _# Manufacturing Data Dictionary  This data dictionary documents the database schema for the manufacturing supply chain system. It includes all tables, columns, data types, constraints, and relationshi…_

3. _## QualityControl  Quality Control (QC) represents inspection and testing activities performed on materials, in-process production, or finished goods. QC records track the type of inspection (incoming…_

---

### ✅ QA-034 — How do I calculate the total manufacturing time for a work order including all sub-assembly work orders?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.1599 | **Gate:** `proceed_with_warning`

**Expected answer:**
> Query the work_order table starting with the parent work_order. Find all child work_orders where parent_work_order matches the current work_order_id. For each work order (parent and children), join with the route table on product_id to get all operations. Sum (cycle_time_minutes * quantity) plus set…

**System answer:**
> From the retrieved context, I can only describe the schema elements you would use to trace the relevant data, not a definitive calculation rule.

What is known is that `work_order` represents production jobs and supports hierarchy through `parent_work_order`, which is a self-reference to `work_order(work_order_id)`. The context explicitly says this enables work order decomposition, so a parent wor…

**Sources retrieved (5):** `parent_chunk_data_dictionary.md_6`, `parent_chunk_data_dictionary.md_3`, `Manufacturing Routing→ROUTE`, `parent_chunk_business_glossary.md_0`, `parent_chunk_business_glossary.md_1`

**Context previews (first 3):**

1. _## work_order  Represents production jobs for manufacturing products with hierarchical work order support.  | Column | Data Type | Constraints | Description | |--------|-----------|-------------|-----…_

2. _# Manufacturing Data Dictionary  This data dictionary documents the database schema for the manufacturing supply chain system. It includes all tables, columns, data types, constraints, and relationshi…_

3. _Business concept 'Manufacturing Routing' — The table is keyed by route_id and product_id and stores the ordered steps for a product, including route_name, sequence_number, operation_name, work_center,…_

---

### ✅ QA-035 — How can I identify which shipments are overdue and their impact on work orders?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0719 | **Gate:** `proceed_with_warning`

**Expected answer:**
> Query the shipment table filtering for status = 'SHIPPED' where actual_arrival is NULL and estimated_arrival is in the past (overdue). Join with the component_supplier table via supplier_id and component_id to identify which components are delayed. Perform reverse BOM lookup to find which parent pro…

**System answer:**
> From the retrieved context, this can only be answered partially.

What is known is that `shipment` contains the fields needed to evaluate delivery timing at a schema level: `shipment_id`, `ship_date`, `estimated_arrival`, `actual_arrival`, `status`, and `warehouse_id`. The allowed `status` values are `PENDING`, `SHIPPED`, `DELIVERED`, and `CANCELLED`, and there is a constraint that `actual_arrival…

**Sources retrieved (5):** `parent_chunk_data_dictionary.md_5`, `parent_chunk_data_dictionary.md_8`, `parent_chunk_data_dictionary.md_6`, `parent_chunk_business_glossary.md_1`, `parent_chunk_business_glossary.md_0`

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
> Based on the retrieved context, I can only answer this partially at the schema/business-concept level.

The context shows that Batch is a real business entity, because QualityControl records are “performed on Batches,” QC has a batch reference, QC results determine Batch status, and Warehouses “store produced Batches.” It also shows that components exist and are procured from external suppliers, a…

**Sources retrieved (5):** `parent_chunk_data_dictionary.md_5`, `Actual stock levels of components and products at specific warehouse locations→INVENTORY`, `parent_chunk_business_glossary.md_2`, `parent_chunk_business_glossary.md_1`, `parent_chunk_business_glossary.md_0`

**Context previews (first 3):**

1. _## warehouse  Stores physical storage location information for inventory management.  | Column | Data Type | Constraints | Description | |--------|-----------|-------------|-------------| | warehouse_…_

2. _Business concept 'Actual stock levels of components and products at specific warehouse locations' is implemented by physical table INVENTORY (columns: inventory_id, warehouse_id, component_id, product…_

3. _## QualityControl  Quality Control (QC) represents inspection and testing activities performed on materials, in-process production, or finished goods. QC records track the type of inspection (incoming…_

---

### ✅ QA-037 — How can I generate a material requirements plan showing when to order components based on work order schedules?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0433 | **Gate:** `proceed_with_warning`

**Expected answer:**
> Query all work_orders with status 'PENDING' ordered by planned_start_date. For each work_order, perform BOM explosion to get required components and quantities. For each component, query inventory for current available stock across warehouses. Calculate net requirements = (required quantity * work_o…

**System answer:**
> From the retrieved context, you can only build a partial, schedule-aligned material requirements view; you cannot fully determine actual component order dates.

The available schema supports this approach: start with `work_order`, because it contains the production demand and schedule fields: `work_order_id`, `product_id`, `quantity_ordered`, `quantity_completed`, `status`, `priority`, `planned_st…

**Sources retrieved (5):** `parent_chunk_data_dictionary.md_6`, `parent_chunk_data_dictionary.md_7`, `parent_chunk_data_dictionary.md_5`, `parent_chunk_business_glossary.md_1`, `parent_chunk_business_glossary.md_0`

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
> From the retrieved context, I cannot describe a complete end-to-end genealogy from supplier through batch to finished goods, because the necessary links are only partially present.

What is known from the context is this: the `product` table is the core structure for manufactured items, including finished goods, assemblies, and components. It supports hierarchical relationships through `product.pa…

**Sources retrieved (5):** `parent_chunk_data_dictionary.md_3`, `parent_chunk_data_dictionary.md_7`, `parent_chunk_business_glossary.md_2`, `parent_chunk_business_glossary.md_0`, `parent_chunk_business_glossary.md_1`

**Context previews (first 3):**

1. _# Manufacturing Data Dictionary  This data dictionary documents the database schema for the manufacturing supply chain system. It includes all tables, columns, data types, constraints, and relationshi…_

2. _## specification  Defines technical requirements and acceptance criteria for materials and products.  | Column | Data Type | Constraints | Description | |--------|-----------|-------------|-----------…_

3. _## QualityControl  Quality Control (QC) represents inspection and testing activities performed on materials, in-process production, or finished goods. QC records track the type of inspection (incoming…_

---

### ✅ QA-039 — How can I find alternative suppliers for components that are critical for multiple products?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0772 | **Gate:** `proceed_with_warning`

**Expected answer:**
> Perform BOM explosion for all active products and count component usage frequency. Identify high-frequency components. Query component_supplier table to find all suppliers for these components. Filter to suppliers with rating >= 4.0 (high quality) and is_preferred = 'Y'. For each component, list alt…

**System answer:**
> From the retrieved context, you can answer this only at a partial, schema-metadata level.

To identify components that are critical for multiple products, the clearest documented source is `bom`. That table records product composition with `parent_product_id` as the product being built and `component_product_id` as the product used as a component. Because `bom` supports recursive, multi-level asse…

**Sources retrieved (5):** `parent_chunk_data_dictionary.md_4`, `parent_chunk_data_dictionary.md_3`, `parent_chunk_business_glossary.md_0`, `parent_chunk_business_glossary.md_1`, `Component Supplier Relationship`

**Context previews (first 3):**

1. _## bom  Bill of Materials defining product composition and hierarchical structure. Supports recursive relationships for multi-level assemblies.  | Column | Data Type | Constraints | Description | |---…_

2. _# Manufacturing Data Dictionary  This data dictionary documents the database schema for the manufacturing supply chain system. It includes all tables, columns, data types, constraints, and relationshi…_

3. _# Manufacturing Business Glossary  This glossary defines the core business concepts and terminology used in the manufacturing supply chain domain. It covers product structures, materials management, p…_

---

### ✅ QA-040 — How do I calculate the total landed cost for a product including component costs, supplier lead times, and manufacturing operations?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.1922 | **Gate:** `proceed_with_warning`

**Expected answer:**
> Perform recursive BOM explosion to get all leaf components. For each component, query component_supplier to get unit_price from primary supplier. Multiply by accumulated BOM quantity for material cost. Add shipping costs (estimated from shipment history). Query route table for the product to get all…

**System answer:**
> From the retrieved context, you can only calculate this partially.

The schema gives you three relevant cost/lead-time elements:

The `product` table stores `base_cost` and `lead_time_days`. For any product, `base_cost` is the only explicit product-level manufacturing cost shown, and `lead_time_days` is the product’s procurement or production lead time. The `product` table also supports a hierarch…

**Sources retrieved (5):** `parent_chunk_data_dictionary.md_3`, `parent_chunk_data_dictionary.md_6`, `parent_chunk_business_glossary.md_0`, `Component Supplier Relationship`, `parent_chunk_business_glossary.md_1`

**Context previews (first 3):**

1. _# Manufacturing Data Dictionary  This data dictionary documents the database schema for the manufacturing supply chain system. It includes all tables, columns, data types, constraints, and relationshi…_

2. _## work_order  Represents production jobs for manufacturing products with hierarchical work order support.  | Column | Data Type | Constraints | Description | |--------|-----------|-------------|-----…_

3. _# Manufacturing Business Glossary  This glossary defines the core business concepts and terminology used in the manufacturing supply chain domain. It covers product structures, materials management, p…_

---

## Anomalies & Observations

No anomalies detected. All questions grounded with acceptable RAGAS scores.
