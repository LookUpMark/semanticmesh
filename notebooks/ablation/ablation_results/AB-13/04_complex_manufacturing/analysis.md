# AB-13 — 04_complex_manufacturing — Run Analysis

**Timestamp:** 2026-04-01 04:20:15  
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
| Triplets extracted | 366 |
| Entities resolved | 123 |
| Tables parsed | 13 |
| Tables completed | 13 |

## Query Evaluation Summary

| Metric | Value |
|--------|-------|
| Questions | 40 |
| Grounded | **40/40 (100%)** |
| Avg GT Coverage | 100% |
| Avg Top Score | 0.4366 |
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
> In the manufacturing system, the physical `product` table stores core information about each manufactured item. A product can represent a `FINISHED_GOOD`, `ASSEMBLY`, or `COMPONENT`, and the table is used for finished goods, assemblies, and components in a hierarchical product structure.

For each product, the system stores `product_id` as the unique identifier, `product_name`, `product_type`, `pa…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_3`, `Production Route→ROUTE`, `parent_chunk_data_dictionary.md_6`, `parent_chunk_data_dictionary.md_5`, `parent_chunk_data_dictionary.md_7`, `parent_chunk_business_glossary.md_0`, `parent_chunk_business_glossary.md_1`, `Production Route`

**Context previews (first 3):**

1. _# Manufacturing Data Dictionary  This data dictionary documents the database schema for the manufacturing supply chain system. It includes all tables, columns, data types, constraints, and relationshi…_

2. _Business concept 'Production Route' — The table stores ordered manufacturing operations for a product, including operation name, work center, cycle time, setup time, and sequence number, which is char…_

3. _## work_order  Represents production jobs for manufacturing products with hierarchical work order support.  | Column | Data Type | Constraints | Description | |--------|-----------|-------------|-----…_

---

### ✅ QA-002 — How are components defined in the manufacturing database?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.5910 | **Gate:** `proceed`

**Expected answer:**
> Components are defined with a unique identifier (component_id), descriptive name (component_name), category grouping (component_category), unit of measure (unit_of_measure), standard unit cost (standard_cost), and optional reference to technical specifications (specification_id). Components represen…

**System answer:**
> Components are defined in two closely related ways in the retrieved context.

As a business concept, a Component is “an atomic raw material or purchased part that cannot be further broken down into simpler manufactured items.” Components are described as the building blocks used in manufacturing and are procured from external suppliers.

At the physical schema level, there is a COMPONENT table wit…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_3`, `parent_chunk_data_dictionary.md_4`, `parent_chunk_data_dictionary.md_5`, `Inventory Stock Levels→INVENTORY`, `BOM entry→BOM`, `parent_chunk_business_glossary.md_0`, `parent_chunk_business_glossary.md_1`, `parent_chunk_business_glossary.md_2`

**Context previews (first 3):**

1. _# Manufacturing Data Dictionary  This data dictionary documents the database schema for the manufacturing supply chain system. It includes all tables, columns, data types, constraints, and relationshi…_

2. _## bom  Bill of Materials defining product composition and hierarchical structure. Supports recursive relationships for multi-level assemblies.  | Column | Data Type | Constraints | Description | |---…_

3. _## warehouse  Stores physical storage location information for inventory management.  | Column | Data Type | Constraints | Description | |--------|-----------|-------------|-------------| | warehouse_…_

---

### ✅ QA-003 — What is the purpose of the Bill of Materials (BOM) table?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.9118 | **Gate:** `proceed`

**Expected answer:**
> The BOM table defines the hierarchical structure of products by specifying which components or sub-assemblies are required to manufacture each parent product. It records the unique BOM entry identifier (bom_id), parent product being built (parent_product_id), component or sub-assembly product (compo…

**System answer:**
> The Bill of Materials table, `bom`, is used to define product composition and hierarchical structure. It records which component products go into a parent product, along with the required quantity, unit of measure, BOM level, and whether a component is optional.

From the context, its purpose is specifically to support recursive, multi-level assemblies by linking `parent_product_id` and `component…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_4`, `BOM→PRODUCT`, `BOM entry→BOM`, `Material Transfer`, `parent_chunk_data_dictionary.md_3`, `Material Transfer→SHIPMENT`, `parent_chunk_data_dictionary.md_7`, `parent_chunk_data_dictionary.md_8`

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
> The system maintains supplier master data in the `SUPPLIER` table, which stores external vendor information for component procurement. From the retrieved context, the supplier information includes `supplier_id`, `supplier_name`, `contact_email`, `contact_phone`, `rating`, and `is_preferred`.

Supplier information is also used in related structures. The `SHIPMENT` table has a `supplier_id` foreign …

**Sources retrieved (12):** `Preferred supplier for this component→SUPPLIER`, `parent_chunk_data_dictionary.md_4`, `SHIPMENT→SUPPLIER`, `Preferred supplier for this component→COMPONENT_SUPPLIER`, `Material Transfer`, `parent_chunk_data_dictionary.md_8`, `COMPONENT_SUPPLIER→SUPPLIER`, `Material Transfer→SHIPMENT`

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
> Warehouses are represented by the `warehouse` table.

This table models a warehouse as a physical storage location where materials, components, and finished goods are stored, with capacity limits, geographic location details, and an assigned manager. Its columns are `warehouse_id` as the primary key, `warehouse_name` as a required name, `address`, `city`, `state`, `capacity` as a required integer …

**Sources retrieved (12):** `INVENTORY→WAREHOUSE`, `BATCH→WAREHOUSE`, `WORK_ORDER→WAREHOUSE`, `SHIPMENT→WAREHOUSE`, `parent_chunk_data_dictionary.md_6`, `parent_chunk_data_dictionary.md_5`, `Actual stock levels of components and products at specific warehouse locations→WAREHOUSE`, `Inventory Stock Levels`

**Context previews (first 3):**

1. _Relationship: INVENTORY references WAREHOUSE via foreign key WAREHOUSE_ID -> WAREHOUSE.WAREHOUSE_ID.…_

2. _Relationship: BATCH references WAREHOUSE via foreign key WAREHOUSE_ID -> WAREHOUSE.WAREHOUSE_ID.…_

3. _Relationship: WORK_ORDER references WAREHOUSE via foreign key WAREHOUSE_ID -> WAREHOUSE.WAREHOUSE_ID.…_

---

### ✅ QA-006 — What does the inventory table track?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.9949 | **Gate:** `proceed`

**Expected answer:**
> The inventory table tracks real-time stock levels including a unique record identifier (inventory_id), warehouse location (warehouse_id), component identifier for materials (component_id) or product identifier for finished goods (product_id), current physical stock quantity (quantity_on_hand), quant…

**System answer:**
> The `INVENTORY` table tracks stock levels for components and products at specific warehouse locations. It records the warehouse-linked quantity on hand, quantity reserved, reorder threshold, and last restock date. Each inventory record is tied to a `warehouse_id` and refers to either a `component_id` or a `product_id` exclusively, not both. This implements the business concept of “Inventory Stock …

**Sources retrieved (12):** `Inventory Stock Levels`, `Inventory Stock Levels→INVENTORY`, `INVENTORY→PRODUCT`, `INVENTORY→WAREHOUSE`, `INVENTORY→COMPONENT`, `parent_chunk_data_dictionary.md_5`, `Material Transfer`, `Material Transfer→SHIPMENT`

**Context previews (first 3):**

1. _Inventory Stock Levels: The table tracks warehouse-linked quantities on hand, quantities reserved, and reorder thresholds for either a component or product, which directly matches stock levels at spec…_

2. _Business concept 'Inventory Stock Levels' — The table tracks warehouse-linked quantities on hand, quantities reserved, and reorder thresholds for either a component or product, which directly matches …_

3. _Relationship: INVENTORY references PRODUCT via foreign key PRODUCT_ID -> PRODUCT.PRODUCT_ID.…_

---

### ✅ QA-007 — How are work orders structured in the manufacturing system?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.4854 | **Gate:** `proceed`

**Expected answer:**
> Work orders represent production jobs with a unique identifier (work_order_id), product to be manufactured (product_id), optional parent work order for nested hierarchies (parent_work_order), quantity to produce (quantity_ordered), quantity completed so far (quantity_completed), current status (PEND…

**System answer:**
> Work orders are implemented by the physical table WORK_ORDER and represent production jobs for manufacturing products. Each work order is uniquely identified by work_order_id and is structured around the core production planning and tracking fields: product_id, quantity_ordered, quantity_completed, status, priority, planned_start_date, planned_end_date, and warehouse_id.

The structure supports th…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_6`, `Work Order→WORK_ORDER`, `WORK_ORDER→PRODUCT`, `Production Route→ROUTE`, `WORK_ORDER→WORK_ORDER`, `parent_chunk_data_dictionary.md_3`, `WORK_ORDER→WAREHOUSE`, `parent_chunk_data_dictionary.md_8`

**Context previews (first 3):**

1. _## work_order  Represents production jobs for manufacturing products with hierarchical work order support.  | Column | Data Type | Constraints | Description | |--------|-----------|-------------|-----…_

2. _Business concept 'Work Order' — The table is explicitly labeled as WORK_ORDER and contains the hallmark attributes of a production work order: planned versus completed quantities, status, priority, pl…_

3. _Relationship: WORK_ORDER references PRODUCT via foreign key PRODUCT_ID -> PRODUCT.PRODUCT_ID.…_

---

### ✅ QA-008 — What information is captured in the shipment table?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.7169 | **Gate:** `proceed`

**Expected answer:**
> Shipments track material transfers with a unique identifier (shipment_id), shipment type (INBOUND from suppliers, OUTBOUND to customers, INTERNAL between warehouses), destination warehouse (warehouse_id), source supplier for inbound (supplier_id), destination customer for outbound (customer_id), shi…

**System answer:**
> The `SHIPMENT` table captures material transfer records between warehouses, suppliers, and customers. It stores the shipment’s unique identifier (`shipment_id`), the shipment type (`shipment_type`), the warehouse involved (`warehouse_id`), the supplier reference for inbound shipments (`supplier_id`), the customer reference for outbound shipments (`customer_id`), the shipment date (`ship_date`), th…

**Sources retrieved (12):** `Material Transfer`, `Material Transfer→SHIPMENT`, `SHIPMENT→WAREHOUSE`, `SHIPMENT→SUPPLIER`, `parent_chunk_data_dictionary.md_8`, `parent_chunk_data_dictionary.md_5`, `parent_chunk_business_glossary.md_0`, `parent_chunk_business_glossary.md_1`

**Context previews (first 3):**

1. _Material Transfer: The table is explicitly labeled as a shipment/material-transfer record and its foreign keys point to warehouse, supplier, and customer, matching the movement of materials between in…_

2. _Business concept 'Material Transfer' — The table is explicitly labeled as a shipment/material-transfer record and its foreign keys point to warehouse, supplier, and customer, matching the movement of …_

3. _Relationship: SHIPMENT references WAREHOUSE via foreign key WAREHOUSE_ID -> WAREHOUSE.WAREHOUSE_ID.…_

---

### ✅ QA-009 — How does the quality control system record inspections?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.9540 | **Gate:** `proceed`

**Expected answer:**
> Quality control records are stored with a unique identifier (qc_id), associated production batch (batch_id), applicable specification requirements (specification_id), inspection date (qc_date), inspection type (INCOMING for supplier materials, IN_PROCESS during manufacturing, FINAL for finished good…

**System answer:**
> The quality control system records inspections in the physical table `QUALITY_CONTROL`, which implements the business concept “Quality Control inspections.” Each inspection is stored as a QC record with these columns: `qc_id`, `batch_id`, `specification_id`, `qc_date`, `qc_type`, `inspector_id`, `result`, `defect_count`, and `notes`.

From the business definition, a QC record captures inspection a…

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
> Specification records define the technical requirements, standards, and acceptance criteria for materials and products. In the `SPECIFICATION` table, they capture the specification name and version, effective date, specification type (`DIMENSIONAL`, `MATERIAL`, `PERFORMANCE`), the critical parameter being tested, and the acceptable value range through `min_value`, `max_value`, and `unit_of_measure…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_7`, `Specifications for quality requirements→SPECIFICATION`, `Quality Control inspections→QUALITY_CONTROL`, `parent_chunk_data_dictionary.md_3`, `parent_chunk_business_glossary.md_2`, `parent_chunk_business_glossary.md_0`, `parent_chunk_business_glossary.md_1`, `Specifications for quality requirements`

**Context previews (first 3):**

1. _## specification  Defines technical requirements and acceptance criteria for materials and products.  | Column | Data Type | Constraints | Description | |--------|-----------|-------------|-----------…_

2. _Business concept 'Specifications for quality requirements' is implemented by physical table SPECIFICATION (columns: specification_id, specification_name, version, effective_date, spec_type, critical_p…_

3. _Business concept 'Quality Control inspections' is implemented by physical table QUALITY_CONTROL (columns: qc_id, batch_id, specification_id, qc_date, qc_type, inspector_id, result, defect_count, notes…_

---

### ✅ QA-011 — How can I find which suppliers provide specific components?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.1645 | **Gate:** `proceed_with_warning`

**Expected answer:**
> Query the component_supplier table which links components to their approved suppliers. This table contains the component identifier (component_id), supplier identifier (supplier_id), preferred supplier flag (is_preferred), lead time in days (lead_time_days), and unit price (unit_price). Join with th…

**System answer:**
> To find which suppliers provide specific components, follow the schema path through `COMPONENT_SUPPLIER`. The retrieved context shows these foreign key relationships: `COMPONENT_SUPPLIER.COMPONENT_ID -> COMPONENT.COMPONENT_ID` and `COMPONENT_SUPPLIER.SUPPLIER_ID -> SUPPLIER.SUPPLIER_ID`.

That means the lookup path is: start with the component in `COMPONENT`, match it to `COMPONENT_SUPPLIER` on `c…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_5`, `parent_chunk_data_dictionary.md_4`, `parent_chunk_data_dictionary.md_3`, `Inventory Stock Levels`, `Actual stock levels of components and products at specific warehouse locations→WAREHOUSE`, `parent_chunk_business_glossary.md_0`, `parent_chunk_business_glossary.md_1`, `Preferred supplier for this component→COMPONENT_SUPPLIER`

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
> Start with `work_order` and use the work order’s `product_id`, because `work_order.product_id` is the product to manufacture. The schema path in the retrieved context is:

`work_order.work_order_id` → `work_order.product_id` → `product.product_id`

From there, trace the product structure. The context says the `product` table supports hierarchical assemblies through `parent_product_id`, and it also…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_5`, `Inventory Stock Levels`, `Work Order→WORK_ORDER`, `Inventory Stock Levels→INVENTORY`, `parent_chunk_data_dictionary.md_6`, `parent_chunk_data_dictionary.md_3`, `parent_chunk_data_dictionary.md_8`, `parent_chunk_data_dictionary.md_7`

**Context previews (first 3):**

1. _## warehouse  Stores physical storage location information for inventory management.  | Column | Data Type | Constraints | Description | |--------|-----------|-------------|-------------| | warehouse_…_

2. _Inventory Stock Levels: The table tracks warehouse-linked quantities on hand, quantities reserved, and reorder thresholds for either a component or product, which directly matches stock levels at spec…_

3. _Business concept 'Work Order' — The table is explicitly labeled as WORK_ORDER and contains the hallmark attributes of a production work order: planned versus completed quantities, status, priority, pl…_

---

### ✅ QA-013 — How can I identify which warehouses have available inventory for specific components?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.8728 | **Gate:** `proceed`

**Expected answer:**
> Query the inventory table filtered by component_id, joining with the warehouse table to get warehouse names and locations. Calculate available quantity as quantity_on_hand minus quantity_reserved. Filter for records where available quantity is greater than zero. Results show warehouse names, locatio…

**System answer:**
> The knowledge graph contains schema metadata, not live inventory records, so it cannot tell you which specific warehouses currently have stock. It does show exactly how to identify them in the schema.

Use the INVENTORY table, which implements the business concept Inventory Stock Levels and tracks stock for either a component or a product at a specific warehouse. For components, use these columns …

**Sources retrieved (12):** `Inventory Stock Levels`, `parent_chunk_data_dictionary.md_5`, `Actual stock levels of components and products at specific warehouse locations→WAREHOUSE`, `Inventory Stock Levels→INVENTORY`, `INVENTORY→WAREHOUSE`, `INVENTORY→COMPONENT`, `parent_chunk_data_dictionary.md_3`, `parent_chunk_data_dictionary.md_8`

**Context previews (first 3):**

1. _Inventory Stock Levels: The table tracks warehouse-linked quantities on hand, quantities reserved, and reorder thresholds for either a component or product, which directly matches stock levels at spec…_

2. _## warehouse  Stores physical storage location information for inventory management.  | Column | Data Type | Constraints | Description | |--------|-----------|-------------|-------------| | warehouse_…_

3. _Business concept 'Actual stock levels of components and products at specific warehouse locations' is implemented by physical table WAREHOUSE (columns: warehouse_id, warehouse_name, address, city, stat…_

---

### ✅ QA-014 — How do I find which shipments delivered materials from a specific supplier?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.2401 | **Gate:** `proceed`

**Expected answer:**
> Query the shipment table filtering by supplier_id and shipment_type = 'INBOUND'. Join with the warehouse table to show destination warehouses. Filter for status = 'DELIVERED' and include actual_arrival date. Results can be ordered by ship_date descending to show most recent deliveries first.

**System answer:**
> Use the `SHIPMENT` table, because it is the table that tracks material transfers between warehouses, suppliers, and customers.

To find shipments that delivered materials from a specific supplier, filter `SHIPMENT` on:
`shipment_type = 'INBOUND'`, because the schema states `supplier_id` is only set for inbound shipments (`chk_supplier_inbound`);
`supplier_id = <specific supplier id>`, because `SHI…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_8`, `Material Transfer`, `Material Transfer→SHIPMENT`, `SHIPMENT→SUPPLIER`, `parent_chunk_data_dictionary.md_5`, `parent_chunk_data_dictionary.md_7`, `parent_chunk_data_dictionary.md_3`, `parent_chunk_data_dictionary.md_4`

**Context previews (first 3):**

1. _## shipment  Tracks material transfers between warehouses, suppliers, and customers.  | Column | Data Type | Constraints | Description | |--------|-----------|-------------|-------------| | shipment_i…_

2. _Material Transfer: The table is explicitly labeled as a shipment/material-transfer record and its foreign keys point to warehouse, supplier, and customer, matching the movement of materials between in…_

3. _Business concept 'Material Transfer' — The table is explicitly labeled as a shipment/material-transfer record and its foreign keys point to warehouse, supplier, and customer, matching the movement of …_

---

### ✅ QA-015 — How can I determine which quality control inspections were performed on a specific production batch?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.9779 | **Gate:** `proceed`

**Expected answer:**
> Query the quality_control table filtered by batch_id. Join with the specification table to get requirement details (specification_name, spec_type, acceptable ranges). Include qc_date, qc_type (INCOMING, IN_PROCESS, FINAL), result (PASS, FAIL, CONDITIONAL), and defect_count. This shows the complete i…

**System answer:**
> Use the `QUALITY_CONTROL` table, which implements the business concept “Quality Control inspections.” The key link is `QUALITY_CONTROL.batch_id`, because QC inspections are associated with specific production batches.

To find the inspections for a specific batch, filter `QUALITY_CONTROL` by the target `batch_id`. The relevant inspection details available there are:

`qc_id`, `batch_id`, `specific…

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
> Use the `WORK_ORDER` table and filter it by both the warehouse and the work order status.

The relevant relationship is `WORK_ORDER.WAREHOUSE_ID -> WAREHOUSE.WAREHOUSE_ID`, so to track work orders at a specific warehouse you identify the warehouse in `WAREHOUSE`, then retrieve the matching rows in `WORK_ORDER` where `warehouse_id` equals that warehouse and `status = 'IN_PROGRESS'`.

The key column…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_5`, `Inventory Stock Levels`, `parent_chunk_data_dictionary.md_6`, `Inventory Stock Levels→INVENTORY`, `WORK_ORDER→WAREHOUSE`, `Work Order→WORK_ORDER`, `Actual stock levels of components and products at specific warehouse locations→WAREHOUSE`, `parent_chunk_data_dictionary.md_8`

**Context previews (first 3):**

1. _## warehouse  Stores physical storage location information for inventory management.  | Column | Data Type | Constraints | Description | |--------|-----------|-------------|-------------| | warehouse_…_

2. _Inventory Stock Levels: The table tracks warehouse-linked quantities on hand, quantities reserved, and reorder thresholds for either a component or product, which directly matches stock levels at spec…_

3. _## work_order  Represents production jobs for manufacturing products with hierarchical work order support.  | Column | Data Type | Constraints | Description | |--------|-----------|-------------|-----…_

---

### ✅ QA-017 — How can I find which components need reordering based on current inventory levels?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.6287 | **Gate:** `proceed`

**Expected answer:**
> Query the inventory table and filter where quantity_on_hand minus quantity_reserved is less than reorder_threshold. Join with the component table to get component names, categories, and standard costs. Join with the warehouse table for location information. Results identify which components are belo…

**System answer:**
> Use the INVENTORY table, which implements the business concept Inventory Stock Levels. It tracks stock at specific warehouse locations and includes the columns inventory_id, warehouse_id, component_id, product_id, quantity_on_hand, quantity_reserved, reorder_threshold, and last_restock_date.

To find component records relevant to reordering, look at INVENTORY rows where component_id is populated, …

**Sources retrieved (12):** `Inventory Stock Levels→INVENTORY`, `Inventory Stock Levels`, `parent_chunk_data_dictionary.md_5`, `Actual stock levels of components and products at specific warehouse locations→WAREHOUSE`, `INVENTORY→COMPONENT`, `parent_chunk_data_dictionary.md_3`, `parent_chunk_data_dictionary.md_7`, `parent_chunk_data_dictionary.md_4`

**Context previews (first 3):**

1. _Business concept 'Inventory Stock Levels' — The table tracks warehouse-linked quantities on hand, quantities reserved, and reorder thresholds for either a component or product, which directly matches …_

2. _Inventory Stock Levels: The table tracks warehouse-linked quantities on hand, quantities reserved, and reorder thresholds for either a component or product, which directly matches stock levels at spec…_

3. _## warehouse  Stores physical storage location information for inventory management.  | Column | Data Type | Constraints | Description | |--------|-----------|-------------|-------------| | warehouse_…_

---

### ✅ QA-018 — How do I determine the manufacturing route for a specific product?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.8164 | **Gate:** `proceed`

**Expected answer:**
> Query the route table filtering by product_id, ordered by sequence_number ascending. For each operation, retrieve operation_name, work_center, cycle_time_minutes, and setup_time_minutes. Join with the product table to get product details. The sequence of operations shows the complete manufacturing w…

**System answer:**
> To determine the manufacturing route for a specific product, use the `ROUTE` table, which implements the business concept `Production Route`. The route is linked directly to a product through `ROUTE.product_id`, which is a foreign key to `PRODUCT.product_id`.

At the schema level, the lookup is:

`PRODUCT.product_id` → `ROUTE.product_id`

If you already know the product ID, retrieve rows from `ROU…

**Sources retrieved (12):** `Production Route→ROUTE`, `parent_chunk_data_dictionary.md_6`, `ROUTE→PRODUCT`, `parent_chunk_data_dictionary.md_3`, `parent_chunk_data_dictionary.md_7`, `the product produced, production date, quantity produced, warehouse location, expiry date (if applicable), and quality control status→PRODUCT`, `Inventory Stock Levels→INVENTORY`, `parent_chunk_data_dictionary.md_8`

**Context previews (first 3):**

1. _Business concept 'Production Route' — The table stores ordered manufacturing operations for a product, including operation name, work center, cycle time, setup time, and sequence number, which is char…_

2. _## work_order  Represents production jobs for manufacturing products with hierarchical work order support.  | Column | Data Type | Constraints | Description | |--------|-----------|-------------|-----…_

3. _Relationship: ROUTE references PRODUCT via foreign key PRODUCT_ID -> PRODUCT.PRODUCT_ID.…_

---

### ✅ QA-019 — How can I find which batches are stored at a specific warehouse and their QC status?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.7533 | **Gate:** `proceed`

**Expected answer:**
> Query the batch table filtering by warehouse_id. Join with the product table to get product names and types. Include production_date, quantity_produced, expiry_date, and qc_status (PENDING, PASSED, FAILED, QUARANTINED). Filter by qc_status to isolate batches requiring quality attention or ready for …

**System answer:**
> Use the `BATCH` table, because the business concept “Production batch reference” is implemented there and it includes both `warehouse_id` and `qc_status`.

To find batches stored at a specific warehouse, use the relationship `BATCH.WAREHOUSE_ID -> WAREHOUSE.WAREHOUSE_ID`. The basic path is `WAREHOUSE` joined to `BATCH` on `warehouse_id`, then filter for the warehouse you want. The relevant batch c…

**Sources retrieved (12):** `Production batch reference→BATCH`, `parent_chunk_data_dictionary.md_5`, `Actual stock levels of components and products at specific warehouse locations→WAREHOUSE`, `Inventory Stock Levels`, `BATCH→WAREHOUSE`, `Inventory Stock Levels→INVENTORY`, `Quality Control inspections→QUALITY_CONTROL`, `the product produced, production date, quantity produced, warehouse location, expiry date (if applicable), and quality control status→PRODUCT`

**Context previews (first 3):**

1. _Business concept 'Production batch reference' is implemented by physical table BATCH (columns: batch_id, product_id, production_date, quantity_produced, warehouse_id, expiry_date, qc_status).…_

2. _## warehouse  Stores physical storage location information for inventory management.  | Column | Data Type | Constraints | Description | |--------|-----------|-------------|-------------| | warehouse_…_

3. _Business concept 'Actual stock levels of components and products at specific warehouse locations' is implemented by physical table WAREHOUSE (columns: warehouse_id, warehouse_name, address, city, stat…_

---

### ✅ QA-020 — How do I identify which specifications apply to specific components?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.2550 | **Gate:** `proceed`

**Expected answer:**
> Query the component table and join with the specification table via specification_id. Include component_name, component_category, and specification details (specification_name, spec_type, critical_parameter, min_value, max_value, unit_of_measure). This shows the technical requirements that each comp…

**System answer:**
> To identify which specifications apply to specific components, use the direct link between `COMPONENT.specification_id` and `SPECIFICATION.specification_id`.

The documented path is:

`COMPONENT.specification_id` → `SPECIFICATION.specification_id`

From the retrieved context, the `COMPONENT` table includes these columns: `component_id`, `component_name`, `component_category`, `unit_of_measure`, `s…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_5`, `parent_chunk_data_dictionary.md_7`, `Product classification: FINISHED_GOOD, ASSEMBLY, COMPONENT→COMPONENT`, `parent_chunk_data_dictionary.md_3`, `Inventory Stock Levels`, `Inventory Stock Levels→INVENTORY`, `Actual stock levels of components and products at specific warehouse locations→WAREHOUSE`, `parent_chunk_data_dictionary.md_4`

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
> To perform a complete BOM explosion from the schema shown here, use the `bom` table as the primary structure and traverse it recursively through `product`.

A finished product is stored in `product`, where `product.product_type` can be `FINISHED_GOOD`, `ASSEMBLY`, or `COMPONENT`. The BOM itself is stored in `bom`, which is defined as the “Bill of Materials defining product composition and hierarch…

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
> Use the `bom` and `product` tables to do a recursive BOM explosion.

The context shows that `bom` defines the product structure, with `bom.parent_product_id` as the item being built and `bom.component_product_id` as the item that goes into it. Both columns reference `product(product_id)`, and the design explicitly supports multi-level assemblies. That means to calculate total material cost for one…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_3`, `parent_chunk_data_dictionary.md_4`, `Product classification: FINISHED_GOOD, ASSEMBLY, COMPONENT→COMPONENT`, `parent_chunk_data_dictionary.md_7`, `parent_chunk_data_dictionary.md_8`, `Production Route→ROUTE`, `parent_chunk_data_dictionary.md_6`, `the product produced, production date, quantity produced, warehouse location, expiry date (if applicable), and quality control status→PRODUCT`

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
> Use the `bom` table recursively. In this schema, a BOM entry is in `BOM(bom_id, parent_product_id, component_product_id, quantity, unit_of_measure, bom_level, is_optional)`, and both `parent_product_id` and `component_product_id` are foreign keys to `PRODUCT.product_id`. That is what enables multi-level assemblies.

To find every parent product that contains a specific component anywhere in its BO…

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
> Use the product structure, not just the work order hierarchy.

A work order is in `WORK_ORDER`, and the product being manufactured is `WORK_ORDER.PRODUCT_ID -> PRODUCT.PRODUCT_ID`. To find work orders that require a specific component, you would start from each work order’s `product_id` and traverse the `BOM` table recursively through its parent/component links:

`WORK_ORDER.PRODUCT_ID -> BOM.PARE…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_6`, `parent_chunk_data_dictionary.md_5`, `parent_chunk_data_dictionary.md_3`, `parent_chunk_data_dictionary.md_4`, `Work Order→WORK_ORDER`, `WORK_ORDER→WORK_ORDER`, `WORK_ORDER→PRODUCT`, `Inventory Stock Levels`

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
> Use the `bom` table’s `bom_level` column. In the retrieved context, `bom_level` is explicitly described as the “depth in product hierarchy” and “tracks depth for performance optimization.”

For a specific product, use `bom.parent_product_id` to identify the product being built, and then take the highest `bom.bom_level` value for that product’s BOM rows. If you want the product details, join `bom.p…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_4`, `parent_chunk_data_dictionary.md_3`, `BOM entry→BOM`, `BOM→PRODUCT`, `parent_chunk_data_dictionary.md_7`, `parent_chunk_data_dictionary.md_5`, `Inventory Stock Levels→INVENTORY`, `parent_chunk_data_dictionary.md_6`

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
> Use the `bom` table recursively.

The `bom` table is the schema object that defines product composition and “supports recursive relationships for multi-level assemblies.” Its key columns are `parent_product_id` for the product being built and `component_product_id` for the product that goes into it. Both columns reference `product(product_id)`, so you can traverse the hierarchy upward through as m…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_3`, `parent_chunk_data_dictionary.md_4`, `parent_chunk_data_dictionary.md_5`, `Inventory Stock Levels`, `Inventory Stock Levels→INVENTORY`, `Product classification: FINISHED_GOOD, ASSEMBLY, COMPONENT→COMPONENT`, `parent_chunk_data_dictionary.md_7`, `Actual stock levels of components and products at specific warehouse locations→WAREHOUSE`

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
> From the retrieved context, the schema supports this at the hierarchy level, but it does not define a single official business formula for “total lead time.” What is available is the structure needed to compute it.

The relevant source for lead time is the `product` table, which stores `lead_time_days` for each product and supports hierarchy through `parent_product_id`. For product composition, th…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_3`, `the product produced, production date, quantity produced, warehouse location, expiry date (if applicable), and quality control status→PRODUCT`, `parent_chunk_data_dictionary.md_4`, `Preferred supplier for this component→COMPONENT_SUPPLIER`, `Production Route→ROUTE`, `parent_chunk_data_dictionary.md_7`, `parent_chunk_data_dictionary.md_6`, `parent_chunk_data_dictionary.md_8`

**Context previews (first 3):**

1. _# Manufacturing Data Dictionary  This data dictionary documents the database schema for the manufacturing supply chain system. It includes all tables, columns, data types, constraints, and relationshi…_

2. _Business concept 'the product produced, production date, quantity produced, warehouse location, expiry date (if applicable), and quality control status' is implemented by physical table PRODUCT (colum…_

3. _## bom  Bill of Materials defining product composition and hierarchical structure. Supports recursive relationships for multi-level assemblies.  | Column | Data Type | Constraints | Description | |---…_

---

### ✅ QA-028 — How do I generate a complete indented BOM report showing the hierarchical structure?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.4180 | **Gate:** `proceed`

**Expected answer:**
> Use a recursive query on the bom table that tracks the current depth level. Start with the top-level product (parent_product_id where product has no parent_product_id). At each level, output component details indented by depth level. Include product_name, quantity, and unit_of_measure. Recursively p…

**System answer:**
> Use the `bom` table as the driving table for the report, because it is the business concept “BOM entry” and is explicitly described as supporting recursive relationships for multi-level assemblies.

To produce a complete indented BOM report, start from the top-level product you want to explode, using `bom.parent_product_id` as the assembly being built. Then recursively follow the hierarchy by trea…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_4`, `parent_chunk_data_dictionary.md_3`, `parent_chunk_data_dictionary.md_6`, `parent_chunk_data_dictionary.md_8`, `BOM entry→BOM`, `BOM→PRODUCT`, `Work Order→WORK_ORDER`, `parent_chunk_business_glossary.md_0`

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
> Use the `BOM` table, because the business concept “BOM entry” is implemented by `BOM (bom_id, parent_product_id, component_product_id, quantity, unit_of_measure, bom_level, is_optional)`.

At the schema level, the basic approach is to count how often each `component_product_id` appears in `BOM`. Since `BOM.component_product_id` is a foreign key to `PRODUCT.product_id`, you can join `BOM` to `PRODU…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_4`, `parent_chunk_data_dictionary.md_3`, `BOM entry→BOM`, `BOM→PRODUCT`, `parent_chunk_data_dictionary.md_5`, `Inventory Stock Levels`, `Product classification: FINISHED_GOOD, ASSEMBLY, COMPONENT→COMPONENT`, `Inventory Stock Levels→INVENTORY`

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
> From the retrieved context, I can only say this at the schema level: circular references would have to be investigated within the `bom` table, because `bom` is the structure that defines parent-child product composition. The relevant columns are `bom.parent_product_id` and `bom.component_product_id`, and both are foreign keys to `product.product_id`. The context also states that this design suppor…

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
> From the retrieved context, you can determine the complete product structure for a finished product, but you cannot fully determine the supplier chain for that product and all sub-assemblies because the schema shown does not include a direct relationship from a product or BOM component to a supplier.

At the product-structure level, the correct trace starts with `product` and `bom`. Use the finish…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_3`, `Product classification: FINISHED_GOOD, ASSEMBLY, COMPONENT→COMPONENT`, `parent_chunk_data_dictionary.md_4`, `parent_chunk_data_dictionary.md_8`, `parent_chunk_data_dictionary.md_6`, `parent_chunk_data_dictionary.md_7`, `Material Transfer→SHIPMENT`, `Production Route→ROUTE`

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
> From the schema metadata, you can do this at the product-stock level by linking `WORK_ORDER` to `INVENTORY` through the product being produced.

`WORK_ORDER.product_id` identifies the product to manufacture, and `INVENTORY.product_id` identifies stock records for products stored in warehouses. `INVENTORY.warehouse_id` links each stock record to `WAREHOUSE.warehouse_id`, so checking “across all war…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_5`, `parent_chunk_data_dictionary.md_6`, `Inventory Stock Levels`, `Inventory Stock Levels→INVENTORY`, `INVENTORY→WAREHOUSE`, `Work Order→WORK_ORDER`, `WORK_ORDER→WAREHOUSE`, `parent_chunk_business_glossary.md_1`

**Context previews (first 3):**

1. _## warehouse  Stores physical storage location information for inventory management.  | Column | Data Type | Constraints | Description | |--------|-----------|-------------|-------------| | warehouse_…_

2. _## work_order  Represents production jobs for manufacturing products with hierarchical work order support.  | Column | Data Type | Constraints | Description | |--------|-----------|-------------|-----…_

3. _Inventory Stock Levels: The table tracks warehouse-linked quantities on hand, quantities reserved, and reorder thresholds for either a component or product, which directly matches stock levels at spec…_

---

### ✅ QA-033 — How can I find which quality control inspections failed for components from specific suppliers?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.4561 | **Gate:** `proceed`

**Expected answer:**
> Query the quality_control table filtering by result = 'FAIL'. Join with the batch table to get product_id and production_date. Join with the bom table recursively to trace which products contain failed components. Join with component_supplier and supplier tables to identify the source supplier. Filt…

**System answer:**
> From the retrieved context, you can answer this only partially at the schema level.

The part that is directly supported is how to find failed quality control inspections themselves. The business concept “Quality Control inspections” is implemented by the physical table `QUALITY_CONTROL`, with columns `qc_id`, `batch_id`, `specification_id`, `qc_date`, `qc_type`, `inspector_id`, `result`, `defect_…

**Sources retrieved (12):** `Quality Control inspections→QUALITY_CONTROL`, `parent_chunk_data_dictionary.md_5`, `parent_chunk_data_dictionary.md_3`, `parent_chunk_data_dictionary.md_4`, `Actual stock levels of components and products at specific warehouse locations→WAREHOUSE`, `COMPONENT_SUPPLIER→SUPPLIER`, `parent_chunk_data_dictionary.md_8`, `Inventory Stock Levels`

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
> From the available context, the schema-level way to calculate total manufacturing time for a work order and all its sub-assembly work orders is to combine the hierarchical `WORK_ORDER` structure with the product-level `ROUTE` definition.

A `WORK_ORDER` represents a production job and supports hierarchy through `parent_work_order → work_order(work_order_id)`. The context states this “enables work …

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_6`, `Production Route→ROUTE`, `parent_chunk_data_dictionary.md_3`, `Work Order→WORK_ORDER`, `parent_chunk_data_dictionary.md_7`, `parent_chunk_data_dictionary.md_5`, `parent_chunk_data_dictionary.md_4`, `parent_chunk_business_glossary.md_0`

**Context previews (first 3):**

1. _## work_order  Represents production jobs for manufacturing products with hierarchical work order support.  | Column | Data Type | Constraints | Description | |--------|-----------|-------------|-----…_

2. _Business concept 'Production Route' — The table stores ordered manufacturing operations for a product, including operation name, work center, cycle time, setup time, and sequence number, which is char…_

3. _# Manufacturing Data Dictionary  This data dictionary documents the database schema for the manufacturing supply chain system. It includes all tables, columns, data types, constraints, and relationshi…_

---

### ✅ QA-035 — How can I identify which shipments are overdue and their impact on work orders?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0719 | **Gate:** `proceed_with_warning`

**Expected answer:**
> Query the shipment table filtering for status = 'SHIPPED' where actual_arrival is NULL and estimated_arrival is in the past (overdue). Join with the component_supplier table via supplier_id and component_id to identify which components are delayed. Perform reverse BOM lookup to find which parent pro…

**System answer:**
> The retrieved context does not define an “overdue shipment” rule, so I cannot determine from the knowledge graph how a shipment is formally classified as overdue.

What the context does provide for `SHIPMENT` is the available tracking fields: `shipment_id`, `shipment_type` (`INBOUND`, `OUTBOUND`, `INTERNAL`), `warehouse_id`, `supplier_id`, `customer_id`, `ship_date`, `estimated_arrival`, `actual_a…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_5`, `parent_chunk_data_dictionary.md_8`, `Work Order→WORK_ORDER`, `parent_chunk_data_dictionary.md_6`, `Material Transfer→SHIPMENT`, `WORK_ORDER→PRODUCT`, `Material Transfer`, `WORK_ORDER→WAREHOUSE`

**Context previews (first 3):**

1. _## warehouse  Stores physical storage location information for inventory management.  | Column | Data Type | Constraints | Description | |--------|-----------|-------------|-------------| | warehouse_…_

2. _## shipment  Tracks material transfers between warehouses, suppliers, and customers.  | Column | Data Type | Constraints | Description | |--------|-----------|-------------|-------------| | shipment_i…_

3. _Business concept 'Work Order' — The table is explicitly labeled as WORK_ORDER and contains the hallmark attributes of a production work order: planned versus completed quantities, status, priority, pl…_

---

### ✅ QA-036 — How do I find which batches are approaching or past expiry and contain components from specific suppliers?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.1479 | **Gate:** `proceed_with_warning`

**Expected answer:**
> Query the batch table filtering for expiry_date within a warning window (e.g., next 30 days) or past expiry. Join with the bom table recursively on product_id to trace all components used in those batches. Join with component_supplier and supplier tables to filter by specific suppliers. Results iden…

**System answer:**
> From the retrieved context, you can only answer this partially at the schema level.

For expiry, the relevant table is `BATCH`, which implements the business concept “Production batch reference” and includes `batch_id`, `product_id`, `production_date`, `quantity_produced`, `warehouse_id`, `expiry_date`, and `qc_status`. This means you can identify batches that are past expiry by checking `BATCH.ex…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_5`, `Inventory Stock Levels`, `Inventory Stock Levels→INVENTORY`, `Actual stock levels of components and products at specific warehouse locations→WAREHOUSE`, `parent_chunk_data_dictionary.md_7`, `parent_chunk_data_dictionary.md_3`, `Production batch reference→BATCH`, `parent_chunk_data_dictionary.md_8`

**Context previews (first 3):**

1. _## warehouse  Stores physical storage location information for inventory management.  | Column | Data Type | Constraints | Description | |--------|-----------|-------------|-------------| | warehouse_…_

2. _Inventory Stock Levels: The table tracks warehouse-linked quantities on hand, quantities reserved, and reorder thresholds for either a component or product, which directly matches stock levels at spec…_

3. _Business concept 'Inventory Stock Levels' — The table tracks warehouse-linked quantities on hand, quantities reserved, and reorder thresholds for either a component or product, which directly matches …_

---

### ✅ QA-037 — How can I generate a material requirements plan showing when to order components based on work order schedules?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0433 | **Gate:** `proceed_with_warning`

**Expected answer:**
> Query all work_orders with status 'PENDING' ordered by planned_start_date. For each work_order, perform BOM explosion to get required components and quantities. For each component, query inventory for current available stock across warehouses. Calculate net requirements = (required quantity * work_o…

**System answer:**
> From the retrieved schema, you can build this as a schema-level MRP view by using `WORK_ORDER` as the demand source, exploding the `BOM`, enriching with `PRODUCT`, and comparing against `INVENTORY` at the same `warehouse_id`.

The core join path is `WORK_ORDER.product_id -> BOM.parent_product_id`. That gives the components required for each work order through `BOM.component_product_id`, along with…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_6`, `parent_chunk_data_dictionary.md_7`, `parent_chunk_data_dictionary.md_5`, `Work Order→WORK_ORDER`, `parent_chunk_data_dictionary.md_4`, `parent_chunk_data_dictionary.md_3`, `Inventory Stock Levels`, `Inventory Stock Levels→INVENTORY`

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
> From the retrieved context, you can only trace this genealogy partially at the schema level.

The documented trace starts with the supplier-side movement in `shipment`. For supplier receipts, use `shipment.shipment_type = 'INBOUND'`, then read `shipment.supplier_id`, `shipment.warehouse_id`, `ship_date`, `estimated_arrival`, `actual_arrival`, and `status` (`PENDING`, `SHIPPED`, `DELIVERED`, `CANCE…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_3`, `Product classification: FINISHED_GOOD, ASSEMBLY, COMPONENT→COMPONENT`, `parent_chunk_data_dictionary.md_7`, `parent_chunk_data_dictionary.md_5`, `parent_chunk_data_dictionary.md_8`, `Material Transfer→SHIPMENT`, `parent_chunk_data_dictionary.md_4`, `Material Transfer`

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
> From the available schema, the clearest way is to treat “critical” components as BOM components where `bom.is_optional = 'N'`, then find which of those are used by more than one product through the `bom` table.

At the product-structure level, use `bom.parent_product_id` as the product being built and `bom.component_product_id` as the component used in it. Because `bom` supports recursive multi-le…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_4`, `parent_chunk_data_dictionary.md_3`, `Preferred supplier for this component→COMPONENT_SUPPLIER`, `Preferred supplier for this component→SUPPLIER`, `parent_chunk_data_dictionary.md_5`, `parent_chunk_data_dictionary.md_8`, `parent_chunk_data_dictionary.md_7`, `Inventory Stock Levels→INVENTORY`

**Context previews (first 3):**

1. _## bom  Bill of Materials defining product composition and hierarchical structure. Supports recursive relationships for multi-level assemblies.  | Column | Data Type | Constraints | Description | |---…_

2. _# Manufacturing Data Dictionary  This data dictionary documents the database schema for the manufacturing supply chain system. It includes all tables, columns, data types, constraints, and relationshi…_

3. _Business concept 'Preferred supplier for this component' is implemented by physical table COMPONENT_SUPPLIER (columns: component_supplier_id, component_id, supplier_id, is_preferred, lead_time_days, u…_

---

### ✅ QA-040 — How do I calculate the total landed cost for a product including component costs, supplier lead times, and manufacturing operations?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.1922 | **Gate:** `proceed_with_warning`

**Expected answer:**
> Perform recursive BOM explosion to get all leaf components. For each component, query component_supplier to get unit_price from primary supplier. Multiply by accumulated BOM quantity for material cost. Add shipping costs (estimated from shipment history). Query route table for the product to get all…

**System answer:**
> The knowledge graph does not define a single built-in “total landed cost” formula, but it does show the schema pieces you would combine to build one at the schema level.

Start with the finished product in `product`. The core product-level fields available are `product.product_id`, `product.base_cost`, and `product.lead_time_days`. If you want the product’s own stored manufacturing cost baseline, …

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_3`, `Production Route→ROUTE`, `the product produced, production date, quantity produced, warehouse location, expiry date (if applicable), and quality control status→PRODUCT`, `Preferred supplier for this component→COMPONENT_SUPPLIER`, `parent_chunk_data_dictionary.md_6`, `parent_chunk_data_dictionary.md_7`, `parent_chunk_data_dictionary.md_5`, `parent_chunk_data_dictionary.md_8`

**Context previews (first 3):**

1. _# Manufacturing Data Dictionary  This data dictionary documents the database schema for the manufacturing supply chain system. It includes all tables, columns, data types, constraints, and relationshi…_

2. _Business concept 'Production Route' — The table stores ordered manufacturing operations for a product, including operation name, work center, cycle time, setup time, and sequence number, which is char…_

3. _Business concept 'the product produced, production date, quantity produced, warehouse location, expiry date (if applicable), and quality control status' is implemented by physical table PRODUCT (colum…_

---

## Anomalies & Observations

No anomalies detected. All questions grounded with acceptable RAGAS scores.
