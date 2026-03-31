# AB-20 — 04_complex_manufacturing — Run Analysis

**Timestamp:** 2026-03-31 01:04:16  
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

Builder skipped (`--no-builder`).

## Query Evaluation Summary

| Metric | Value |
|--------|-------|
| Questions | 40 |
| Grounded | **40/40 (100%)** |
| Avg GT Coverage | 100% |
| Avg Top Score | 0.4283 |
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
> The manufacturing system stores product information primarily in the `product` table. A product represents any manufactured item in the system, including finished goods, assemblies, and components.

For each product, the system stores a unique identifier in `product_id`, the product name in `product_name`, the classification in `product_type`, the parent product in `parent_product_id`, the base ma…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_3`, `Manufacturing Routing→ROUTE`, `parent_chunk_data_dictionary.md_6`, `parent_chunk_data_dictionary.md_5`, `parent_chunk_data_dictionary.md_7`, `complex products→PRODUCT`, `parent_chunk_business_glossary.md_0`, `Manufacturing Routing`

**Context previews (first 3):**

1. _# Manufacturing Data Dictionary  This data dictionary documents the database schema for the manufacturing supply chain system. It includes all tables, columns, data types, constraints, and relationshi…_

2. _Business concept 'Manufacturing Routing' — The table is keyed by route_id and product_id and stores the ordered steps for a product, including route_name, sequence_number, operation_name, work_center,…_

3. _## work_order  Represents production jobs for manufacturing products with hierarchical work order support.  | Column | Data Type | Constraints | Description | |--------|-----------|-------------|-----…_

---

### ✅ QA-002 — How are components defined in the manufacturing database?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.5910 | **Gate:** `proceed`

**Expected answer:**
> Components are defined with a unique identifier (component_id), descriptive name (component_name), category grouping (component_category), unit of measure (unit_of_measure), standard unit cost (standard_cost), and optional reference to technical specifications (specification_id). Components represen…

**System answer:**
> In the provided context, components are defined at both the business-concept level and the schema level.

As a business concept, a Component is “an atomic raw material or purchased part” that cannot be further broken down into simpler manufactured items. Components are described as the building blocks used in manufacturing and are procured from external suppliers.

At the physical schema level, co…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_3`, `parent_chunk_data_dictionary.md_4`, `parent_chunk_data_dictionary.md_5`, `BOM entry→BOM`, `parent_chunk_business_glossary.md_0`, `parent_chunk_business_glossary.md_1`, `parent_chunk_business_glossary.md_2`, `Manufacturing Routing`

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
> The Bill of Materials table, `bom`, defines product composition and hierarchical structure. Its purpose is to represent what components go into a parent product and in what quantity, supporting multi-level assemblies through recursive relationships.

From the context, `bom` is the physical implementation of the business concept “BOM entry” and includes `parent_product_id` for the product being bui…

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
> The system maintains supplier master data in the `SUPPLIER` table, which stores external vendor information for component procurement. From the retrieved context, the supplier attributes are `supplier_id`, `supplier_name`, `contact_email`, `contact_phone`, `rating`, and `is_preferred`.

It also maintains supplier-related relationship data in other tables. In `COMPONENT_SUPPLIER`, a supplier is lin…

**Sources retrieved (12):** `Preferred supplier for this component→SUPPLIER`, `parent_chunk_data_dictionary.md_4`, `SHIPMENT→SUPPLIER`, `shipment type, source and destination locations, dates for ship, estimated arrival, and actual delivery, along with current status→SHIPMENT`, `parent_chunk_data_dictionary.md_8`, `COMPONENT_SUPPLIER→SUPPLIER`, `Component Supplier Relationship→COMPONENT_SUPPLIER`, `parent_chunk_data_dictionary.md_3`

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
> Warehouses are represented by the `warehouse` table (`WAREHOUSE`) as physical storage locations for inventory management. The table stores `warehouse_id` as the primary key, along with `warehouse_name`, `address`, `city`, `state`, `capacity`, and `manager_id`. In the business description, a Warehouse is a physical storage location where materials, components, and finished goods are stored, with de…

**Sources retrieved (12):** `INVENTORY→WAREHOUSE`, `BATCH→WAREHOUSE`, `WORK_ORDER→WAREHOUSE`, `SHIPMENT→WAREHOUSE`, `parent_chunk_data_dictionary.md_6`, `parent_chunk_data_dictionary.md_5`, `Actual stock levels of components and products at specific warehouse locations→WAREHOUSE`, `parent_chunk_data_dictionary.md_8`

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
> The `INVENTORY` table tracks the actual stock levels of components and products at specific warehouse locations.

From the context, each inventory record represents stock in a `warehouse` and includes:
`inventory_id`, `warehouse_id`, `component_id`, `product_id`, `quantity_on_hand`, `quantity_reserved`, `reorder_threshold`, and `last_restock_date`.

It supports either a component or a product in a…

**Sources retrieved (12):** `INVENTORY→PRODUCT`, `INVENTORY→WAREHOUSE`, `INVENTORY→COMPONENT`, `Actual stock levels of components and products at specific warehouse locations→INVENTORY`, `parent_chunk_data_dictionary.md_5`, `Batches for traceability and inventory management→BATCH`, `parent_chunk_data_dictionary.md_7`, `parent_chunk_data_dictionary.md_8`

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
> Work orders are implemented by the `WORK_ORDER` table and represent production jobs for manufacturing products. The structure is explicitly hierarchical: each work order has a primary key `work_order_id`, and the optional `parent_work_order` foreign key points back to `WORK_ORDER.WORK_ORDER_ID`, allowing a large production job to be decomposed into child work orders for complex production planning…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_6`, `Manufacturing Routing→ROUTE`, `Hierarchical production planning and tracking→WORK_ORDER`, `WORK_ORDER→PRODUCT`, `WORK_ORDER→WORK_ORDER`, `parent_chunk_data_dictionary.md_3`, `WORK_ORDER→WAREHOUSE`, `parent_chunk_data_dictionary.md_8`

**Context previews (first 3):**

1. _## work_order  Represents production jobs for manufacturing products with hierarchical work order support.  | Column | Data Type | Constraints | Description | |--------|-----------|-------------|-----…_

2. _Business concept 'Manufacturing Routing' — The table is keyed by route_id and product_id and stores the ordered steps for a product, including route_name, sequence_number, operation_name, work_center,…_

3. _Business concept 'Hierarchical production planning and tracking' is implemented by physical table WORK_ORDER (columns: work_order_id, product_id, parent_work_order, quantity_ordered, quantity_complete…_

---

### ✅ QA-008 — What information is captured in the shipment table?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.8695 | **Gate:** `proceed`

**Expected answer:**
> Shipments track material transfers with a unique identifier (shipment_id), shipment type (INBOUND from suppliers, OUTBOUND to customers, INTERNAL between warehouses), destination warehouse (warehouse_id), source supplier for inbound (supplier_id), destination customer for outbound (customer_id), shi…

**System answer:**
> The `SHIPMENT` table captures material transfer information between warehouses, suppliers, and customers. It implements the business concept of shipment type, source and destination locations, ship date, estimated arrival date, actual delivery/arrival date, and current status.

Specifically, it stores:
`shipment_id` as the unique shipment identifier; `shipment_type` to indicate whether the shipmen…

**Sources retrieved (12):** `shipment type, source and destination locations, dates for ship, estimated arrival, and actual delivery, along with current status→SHIPMENT`, `SHIPMENT→WAREHOUSE`, `SHIPMENT→SUPPLIER`, `parent_chunk_data_dictionary.md_8`, `parent_chunk_data_dictionary.md_5`, `shipment type, source and destination locations, dates for ship, estimated arrival, and actual delivery, along with current status`, `parent_chunk_business_glossary.md_0`, `parent_chunk_business_glossary.md_1`

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

Each inspection is captured as a QC record with these columns: qc_id, batch_id, specification_id, qc_date, qc_type, inspector_id, result, defect_count, and notes. From the business description, this means the system rec…

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
> Specification records define the technical requirements, standards, and acceptance criteria for materials and products. The `SPECIFICATION` table captures the specification name, version, effective date, specification type (`DIMENSIONAL`, `MATERIAL`, `PERFORMANCE`), the critical parameter being tested, acceptable minimum and maximum values, and the unit of measure. These records serve as the refer…

**Sources retrieved (12):** `inspection and testing records for quality assurance→QUALITY_CONTROL`, `parent_chunk_data_dictionary.md_7`, `Technical specification reference→SPECIFICATION`, `parent_chunk_data_dictionary.md_3`, `Product classification: FINISHED_GOOD, ASSEMBLY, COMPONENT→COMPONENT`, `parent_chunk_business_glossary.md_2`, `parent_chunk_business_glossary.md_0`, `inspection and testing records for quality assurance`

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
> To find which suppliers provide specific components, use the Component Supplier Relationship implemented by the `COMPONENT_SUPPLIER` table. The context says this table is the junction entity linking one component to one supplier, and it has a unique `component_id` / `supplier_id` pair.

The schema path is:

`COMPONENT.component_id` → `COMPONENT_SUPPLIER.component_id` → `COMPONENT_SUPPLIER.supplier…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_5`, `parent_chunk_data_dictionary.md_4`, `parent_chunk_data_dictionary.md_3`, `Actual stock levels of components and products at specific warehouse locations→INVENTORY`, `parent_chunk_business_glossary.md_0`, `parent_chunk_business_glossary.md_1`, `Component Supplier Relationship→COMPONENT_SUPPLIER`, `Preferred supplier for this component→SUPPLIER`

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
> To trace which components are needed for a work order, start with `WORK_ORDER`. The key join is `WORK_ORDER.product_id -> PRODUCT.product_id`, because `WORK_ORDER` identifies the product being manufactured.

From that product, trace the product structure recursively. The context shows two mechanisms that support this:

`PRODUCT.parent_product_id -> PRODUCT.product_id`, which enables multi-level pr…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_5`, `Hierarchical production planning and tracking→WORK_ORDER`, `parent_chunk_data_dictionary.md_6`, `Actual stock levels of components and products at specific warehouse locations→INVENTORY`, `parent_chunk_data_dictionary.md_3`, `parent_chunk_data_dictionary.md_8`, `parent_chunk_data_dictionary.md_7`, `WORK_ORDER→PRODUCT`

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
> Use the `INVENTORY` table, which implements the business concept “Actual stock levels of components and products at specific warehouse locations,” and join it to `WAREHOUSE`.

At the schema level, the path is:
`INVENTORY.warehouse_id -> WAREHOUSE.warehouse_id`

To look for a specific component, filter `INVENTORY.component_id` to the component you care about. The context says `component_id` is the …

**Sources retrieved (12):** `Actual stock levels of components and products at specific warehouse locations→INVENTORY`, `parent_chunk_data_dictionary.md_5`, `Actual stock levels of components and products at specific warehouse locations→WAREHOUSE`, `INVENTORY→WAREHOUSE`, `INVENTORY→COMPONENT`, `parent_chunk_data_dictionary.md_3`, `parent_chunk_data_dictionary.md_8`, `parent_chunk_data_dictionary.md_6`

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
> To find shipments that delivered materials from a specific supplier, use the `SHIPMENT` table. It is the table that implements the business concept of shipment type, source and destination locations, ship date, estimated arrival, actual delivery, and current status.

At the schema level, the relevant logic is:

Filter `SHIPMENT.supplier_id` to the supplier you care about. If you need to validate o…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_8`, `SHIPMENT→SUPPLIER`, `shipment type, source and destination locations, dates for ship, estimated arrival, and actual delivery, along with current status→SHIPMENT`, `parent_chunk_data_dictionary.md_5`, `Actual stock levels of components and products at specific warehouse locations→INVENTORY`, `parent_chunk_data_dictionary.md_7`, `parent_chunk_business_glossary.md_1`, `parent_chunk_business_glossary.md_0`

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
> The knowledge graph contains schema metadata, not actual inspection records, so it cannot tell you which inspections were performed for a specific batch instance. It does show exactly how to determine that in the schema.

Use the `QUALITY_CONTROL` table, which implements the business concept “inspection and testing records for quality assurance.” The key column is `batch_id`, which associates each…

**Sources retrieved (12):** `inspection and testing records for quality assurance→QUALITY_CONTROL`, `parent_chunk_data_dictionary.md_7`, `Batches for traceability and inventory management→BATCH`, `BATCH→PRODUCT`, `parent_chunk_data_dictionary.md_5`, `parent_chunk_data_dictionary.md_6`, `parent_chunk_data_dictionary.md_3`, `parent_chunk_business_glossary.md_2`

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
> To track work orders that are in progress at a specific warehouse, use the `work_order` table and filter on its `status` and `warehouse_id` columns.

The key logic is:

`work_order.status = 'IN_PROGRESS'`
and
`work_order.warehouse_id = <specific warehouse>`

This works because `work_order` represents production jobs, its `status` column supports `PENDING, IN_PROGRESS, COMPLETED, CLOSED`, and `ware…

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
> Use the INVENTORY table, which implements the business concept “Actual stock levels of components and products at specific warehouse locations.”

To find components that need reordering, look at INVENTORY records where the row is for a component: INVENTORY.component_id is populated, because inventory supports either a component or a product in a record, exclusively. The key columns are INVENTORY.q…

**Sources retrieved (12):** `Actual stock levels of components and products at specific warehouse locations→INVENTORY`, `parent_chunk_data_dictionary.md_5`, `Actual stock levels of components and products at specific warehouse locations→WAREHOUSE`, `INVENTORY→COMPONENT`, `parent_chunk_data_dictionary.md_3`, `parent_chunk_data_dictionary.md_7`, `parent_chunk_data_dictionary.md_4`, `parent_chunk_data_dictionary.md_6`

**Context previews (first 3):**

1. _Business concept 'Actual stock levels of components and products at specific warehouse locations' is implemented by physical table INVENTORY (columns: inventory_id, warehouse_id, component_id, product…_

2. _## warehouse  Stores physical storage location information for inventory management.  | Column | Data Type | Constraints | Description | |--------|-----------|-------------|-------------| | warehouse_…_

3. _Business concept 'Actual stock levels of components and products at specific warehouse locations' is implemented by physical table WAREHOUSE (columns: warehouse_id, warehouse_name, address, city, stat…_

---

### ✅ QA-018 — How do I determine the manufacturing route for a specific product?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.8174 | **Gate:** `proceed`

**Expected answer:**
> Query the route table filtering by product_id, ordered by sequence_number ascending. For each operation, retrieve operation_name, work_center, cycle_time_minutes, and setup_time_minutes. Join with the product table to get product details. The sequence of operations shows the complete manufacturing w…

**System answer:**
> Use the `ROUTE` table, which implements the business concept “Manufacturing Routing.” It stores the full manufacturing route for a product and is keyed by `route_id` and `product_id`. The `ROUTE.product_id` column is a foreign key to `PRODUCT.product_id`, so the route is determined through that product relationship.

If you already know the product ID, retrieve rows from `ROUTE` where `product_id`…

**Sources retrieved (12):** `Manufacturing Routing→ROUTE`, `parent_chunk_data_dictionary.md_6`, `ROUTE→PRODUCT`, `parent_chunk_data_dictionary.md_3`, `parent_chunk_data_dictionary.md_7`, `parent_chunk_data_dictionary.md_8`, `Hierarchical production planning and tracking→WORK_ORDER`, `parent_chunk_data_dictionary.md_4`

**Context previews (first 3):**

1. _Business concept 'Manufacturing Routing' — The table is keyed by route_id and product_id and stores the ordered steps for a product, including route_name, sequence_number, operation_name, work_center,…_

2. _## work_order  Represents production jobs for manufacturing products with hierarchical work order support.  | Column | Data Type | Constraints | Description | |--------|-----------|-------------|-----…_

3. _Relationship: ROUTE references PRODUCT via foreign key PRODUCT_ID -> PRODUCT.PRODUCT_ID.…_

---

### ✅ QA-019 — How can I find which batches are stored at a specific warehouse and their QC status?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.7533 | **Gate:** `proceed`

**Expected answer:**
> Query the batch table filtering by warehouse_id. Join with the product table to get product names and types. Include production_date, quantity_produced, expiry_date, and qc_status (PENDING, PASSED, FAILED, QUARANTINED). Filter by qc_status to isolate batches requiring quality attention or ready for …

**System answer:**
> Use the BATCH table. The business concept “Batches for traceability and inventory management” is implemented by BATCH with columns batch_id, product_id, production_date, quantity_produced, warehouse_id, expiry_date, and qc_status. BATCH references WAREHOUSE through BATCH.WAREHOUSE_ID → WAREHOUSE.WAREHOUSE_ID.

So, schema-wise, to find batches stored at a specific warehouse and their QC status, you…

**Sources retrieved (12):** `Batches for traceability and inventory management→BATCH`, `parent_chunk_data_dictionary.md_5`, `Actual stock levels of components and products at specific warehouse locations→INVENTORY`, `Actual stock levels of components and products at specific warehouse locations→WAREHOUSE`, `BATCH→WAREHOUSE`, `inspection and testing records for quality assurance→QUALITY_CONTROL`, `parent_chunk_data_dictionary.md_6`, `parent_chunk_data_dictionary.md_8`

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
> To identify which specifications apply to specific components, use the `COMPONENT` table and its `specification_id` column, then join it to the `SPECIFICATION` table on `specification_id`.

The schema-level path is:

`COMPONENT.specification_id = SPECIFICATION.specification_id`

From the context, the `COMPONENT` table contains these relevant columns: `component_id`, `component_name`, `component_ca…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_5`, `parent_chunk_data_dictionary.md_7`, `Product classification: FINISHED_GOOD, ASSEMBLY, COMPONENT→COMPONENT`, `Actual stock levels of components and products at specific warehouse locations→INVENTORY`, `parent_chunk_data_dictionary.md_3`, `Actual stock levels of components and products at specific warehouse locations→WAREHOUSE`, `parent_chunk_data_dictionary.md_4`, `parent_chunk_business_glossary.md_0`

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
> To perform a complete BOM explosion for a finished product, use the `bom` table recursively, starting from the target row in `product`.

The core path is: start with `product.product_id` for the finished product, then join to `bom.parent_product_id`, then follow `bom.component_product_id` back to `product.product_id` to identify each child item. For deeper levels, repeat the same step recursively:…

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
> Based on the schema provided, the supported way to calculate total material cost for a product including all sub-assemblies is to recursively explode the `bom` structure and sum the cost contribution of every descendant product.

Start with the finished product in `product.product_id`. Join that product to `bom` on `bom.parent_product_id = product.product_id` to get its immediate components. Then …

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_3`, `parent_chunk_data_dictionary.md_4`, `Product classification: FINISHED_GOOD, ASSEMBLY, COMPONENT→COMPONENT`, `parent_chunk_data_dictionary.md_7`, `parent_chunk_data_dictionary.md_8`, `parent_chunk_data_dictionary.md_6`, `complex products→PRODUCT`, `parent_chunk_data_dictionary.md_5`

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
> Use the `bom` table as the primary path, because `BOM` is the business concept for product composition and multi-level assemblies.

To find all parent products that contain a specific component anywhere in the BOM structure, start with `bom.component_product_id` equal to the target component’s `product_id`. That gives you the direct parents from `bom.parent_product_id`.

Then recurse upward throug…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_4`, `parent_chunk_data_dictionary.md_3`, `BOM entry→BOM`, `BOM→PRODUCT`, `complex products→PRODUCT`, `PRODUCT→PRODUCT`, `parent_chunk_data_dictionary.md_6`, `parent_chunk_data_dictionary.md_8`

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
> Use the product structure, not operational inventory records. The knowledge graph contains schema metadata only, so it can tell you how to trace this, not which specific work orders currently match.

To identify work orders that require a specific component, the main join path is:

WORK_ORDER.PRODUCT_ID -> PRODUCT.PRODUCT_ID -> BOM.PARENT_PRODUCT_ID

Then recursively follow the BOM structure throu…

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
> Use the `bom` table’s `bom_level` column. The context explicitly says `bom_level` is the “Depth in product hierarchy,” is `NOT NULL`, defaults to `0`, and is indexed for hierarchical queries.

To determine the maximum BOM depth:

For the overall deepest BOM in the system, take the maximum value of `BOM.bom_level`.

For the maximum depth for a specific product, use the `bom` rows for that product a…

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
> Use the `bom` hierarchy to trace upward from the specific product to every product that contains it.

The relevant path is `bom.component_product_id → bom.parent_product_id`, with both columns referencing `product(product_id)`. In the `bom` table, `component_product_id` is “what goes into it,” and `parent_product_id` is “what is being built.” Because the BOM supports recursive, multi-level assembl…

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
> The context does not define a prebuilt “total lead time” metric or an official business rule for how to aggregate lead times across a hierarchy. But the schema shows how to derive it from the PRODUCT and BOM structures.

Each product’s own lead time is stored in PRODUCT.lead_time_days, described as the procurement or production lead time. To include sub-assemblies, you would start with the target …

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_3`, `complex products→PRODUCT`, `parent_chunk_data_dictionary.md_4`, `Component Supplier Relationship→COMPONENT_SUPPLIER`, `Manufacturing Routing→ROUTE`, `parent_chunk_data_dictionary.md_7`, `parent_chunk_data_dictionary.md_6`, `parent_chunk_data_dictionary.md_8`

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
> To generate a complete indented BOM report, use the `bom` table as the core hierarchy and join it to `product` twice: once through `bom.parent_product_id -> product.product_id` to get the parent product, and once through `bom.component_product_id -> product.product_id` to get the component product. The `bom` table is the business concept “BOM entry” and is specifically designed for recursive, mult…

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
> Use the BOM table as the primary source, because a “BOM entry” is implemented by BOM and each row represents one parent-product/component relationship. To find which components appear most frequently across all product BOMs, count BOM rows by BOM.component_product_id.

The core schema path is BOM.component_product_id → PRODUCT.product_id. If you also want to know which parent products use the comp…

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
> The context does not describe a built-in cycle-detection rule for the `bom` table, but it gives the schema needed to detect circular references.

A BOM hierarchy is represented in `bom` by `parent_product_id` → `component_product_id`, and both columns are foreign keys to `product(product_id)`. Because the table “supports recursive relationships for multi-level assemblies” and “supports unlimited n…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_4`, `parent_chunk_data_dictionary.md_3`, `BOM→PRODUCT`, `BOM entry→BOM`, `parent_chunk_data_dictionary.md_8`, `Manufacturing Routing→ROUTE`, `parent_chunk_data_dictionary.md_7`, `parent_chunk_data_dictionary.md_6`

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
> At the schema level, you would determine the supplier chain by combining the product hierarchy with the supplier-component relationship. Start from the finished product in `product`, using `product.product_id` and `product.product_type = FINISHED_GOOD`. Then recursively explode its structure through `bom`, joining `bom.parent_product_id` to the current `product.product_id` and following `bom.compo…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_3`, `Product classification: FINISHED_GOOD, ASSEMBLY, COMPONENT→COMPONENT`, `parent_chunk_data_dictionary.md_4`, `parent_chunk_data_dictionary.md_8`, `parent_chunk_data_dictionary.md_6`, `Component Supplier Relationship→COMPONENT_SUPPLIER`, `Manufacturing Routing→ROUTE`, `parent_chunk_business_glossary.md_0`

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
> From the available schema, you can answer this only at the metadata/process level, not by returning actual stock records.

The relevant tables are `WORK_ORDER`, `INVENTORY`, and `WAREHOUSE`.

`WORK_ORDER` gives you the demand side:
`work_order_id`, `product_id`, `quantity_ordered`, `quantity_completed`, `status`, and `warehouse_id`.

`INVENTORY` gives you the supply side:
`inventory_id`, `warehous…

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
> From the retrieved context, the part you can answer directly is the quality-control side: failed inspections are stored in the physical table `QUALITY_CONTROL`, which implements the business concept “inspection and testing records for quality assurance.” The relevant columns are `qc_id`, `batch_id`, `specification_id`, `qc_date`, `qc_type`, `inspector_id`, `result`, `defect_count`, and `notes`. To…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_5`, `parent_chunk_data_dictionary.md_3`, `inspection and testing records for quality assurance→QUALITY_CONTROL`, `parent_chunk_data_dictionary.md_4`, `Actual stock levels of components and products at specific warehouse locations→INVENTORY`, `Actual stock levels of components and products at specific warehouse locations→WAREHOUSE`, `COMPONENT_SUPPLIER→SUPPLIER`, `parent_chunk_business_glossary.md_2`

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
> Use the hierarchical structure in `WORK_ORDER` and the timing data in `ROUTE`.

At the schema level, the calculation path is:

Start with the root `WORK_ORDER.work_order_id`. Use the self-referential relationship `WORK_ORDER.parent_work_order → WORK_ORDER.work_order_id` to recursively collect all descendant work orders, because the table explicitly supports decomposition of a large production job …

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_6`, `parent_chunk_data_dictionary.md_3`, `Manufacturing Routing→ROUTE`, `Hierarchical production planning and tracking→WORK_ORDER`, `parent_chunk_data_dictionary.md_7`, `parent_chunk_data_dictionary.md_5`, `parent_chunk_data_dictionary.md_4`, `parent_chunk_business_glossary.md_0`

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
> The retrieved context supports only a schema-level answer, not actual record-level identification. There is no operational data here showing which specific shipments or work orders currently exist.

From the schema, the closest way to identify overdue shipments is in `SHIPMENT` using its date and status fields: `ship_date`, `estimated_arrival`, `actual_arrival`, and `status` (`PENDING`, `SHIPPED`,…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_5`, `parent_chunk_data_dictionary.md_8`, `parent_chunk_data_dictionary.md_6`, `WORK_ORDER→PRODUCT`, `WORK_ORDER→WAREHOUSE`, `Hierarchical production planning and tracking→WORK_ORDER`, `shipment type, source and destination locations, dates for ship, estimated arrival, and actual delivery, along with current status→SHIPMENT`, `SHIPMENT→WAREHOUSE`

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
> From the retrieved context, you can answer the expiry part at the schema level, but the supplier-component trace is only partially supported.

For expiry, the relevant table is `BATCH`, which implements “Batches for traceability and inventory management.” It has `batch_id`, `product_id`, `production_date`, `quantity_produced`, `warehouse_id`, `expiry_date`, and `qc_status`. To find batches that ar…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_5`, `Actual stock levels of components and products at specific warehouse locations→INVENTORY`, `Batches for traceability and inventory management→BATCH`, `Actual stock levels of components and products at specific warehouse locations→WAREHOUSE`, `parent_chunk_data_dictionary.md_7`, `parent_chunk_data_dictionary.md_3`, `parent_chunk_data_dictionary.md_8`, `parent_chunk_business_glossary.md_2`

**Context previews (first 3):**

1. _## warehouse  Stores physical storage location information for inventory management.  | Column | Data Type | Constraints | Description | |--------|-----------|-------------|-------------| | warehouse_…_

2. _Business concept 'Actual stock levels of components and products at specific warehouse locations' is implemented by physical table INVENTORY (columns: inventory_id, warehouse_id, component_id, product…_

3. _Business concept 'Batches for traceability and inventory management' is implemented by physical table BATCH (columns: batch_id, product_id, production_date, quantity_produced, warehouse_id, expiry_dat…_

---

### ✅ QA-037 — How can I generate a material requirements plan showing when to order components based on work order schedules?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0433 | **Gate:** `proceed_with_warning`

**Expected answer:**
> Query all work_orders with status 'PENDING' ordered by planned_start_date. For each work_order, perform BOM explosion to get required components and quantities. For each component, query inventory for current available stock across warehouses. Calculate net requirements = (required quantity * work_o…

**System answer:**
> Use `WORK_ORDER` as the driver, because it is the table for hierarchical production planning and tracking and it contains the schedule fields `planned_start_date`, `planned_end_date`, `status`, `quantity_ordered`, `quantity_completed`, `product_id`, and `warehouse_id`. For an MRP view, take open work orders with statuses such as `PENDING` or `IN_PROGRESS` rather than `COMPLETED` or `CLOSED`, and b…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_6`, `parent_chunk_data_dictionary.md_7`, `parent_chunk_data_dictionary.md_5`, `parent_chunk_data_dictionary.md_4`, `Hierarchical production planning and tracking→WORK_ORDER`, `parent_chunk_data_dictionary.md_3`, `Actual stock levels of components and products at specific warehouse locations→INVENTORY`, `WORK_ORDER→WORK_ORDER`

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
> At the schema level, the retrieved context supports only a partial genealogy, not a true lot-by-lot operational trace. The available metadata lets you trace supplier relationships, product structure, and produced batches, but it does not show a table that records which specific component receipt, inventory lot, or component batch was consumed by which production batch.

The supplier side starts wi…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_3`, `Product classification: FINISHED_GOOD, ASSEMBLY, COMPONENT→COMPONENT`, `parent_chunk_data_dictionary.md_7`, `parent_chunk_data_dictionary.md_5`, `parent_chunk_data_dictionary.md_8`, `parent_chunk_data_dictionary.md_4`, `Component Supplier Relationship→COMPONENT_SUPPLIER`, `parent_chunk_business_glossary.md_2`

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
> Use the BOM structure to identify components that are shared across multiple products, then use the component-to-supplier relationship to list supplier options for those components.

At the product-structure level, the relevant table is `bom`. Its `parent_product_id` is the product being built, and its `component_product_id` is the product used as a component. A component is “critical for multiple…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_4`, `parent_chunk_data_dictionary.md_3`, `Preferred supplier for this component→SUPPLIER`, `parent_chunk_data_dictionary.md_5`, `parent_chunk_data_dictionary.md_8`, `parent_chunk_data_dictionary.md_7`, `parent_chunk_business_glossary.md_0`, `parent_chunk_business_glossary.md_1`

**Context previews (first 3):**

1. _## bom  Bill of Materials defining product composition and hierarchical structure. Supports recursive relationships for multi-level assemblies.  | Column | Data Type | Constraints | Description | |---…_

2. _# Manufacturing Data Dictionary  This data dictionary documents the database schema for the manufacturing supply chain system. It includes all tables, columns, data types, constraints, and relationshi…_

3. _Business concept 'Preferred supplier for this component' is implemented by physical table SUPPLIER (columns: supplier_id, supplier_name, contact_email, contact_phone, rating, is_preferred).…_

---

### ✅ QA-040 — How do I calculate the total landed cost for a product including component costs, supplier lead times, and manufacturing operations?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.1922 | **Gate:** `proceed_with_warning`

**Expected answer:**
> Perform recursive BOM explosion to get all leaf components. For each component, query component_supplier to get unit_price from primary supplier. Multiply by accumulated BOM quantity for material cost. Add shipping costs (estimated from shipment history). Query route table for the product to get all…

**System answer:**
> The retrieved context does not define a formal “total landed cost” calculation, so an exact formula cannot be derived from the knowledge graph alone. However, the schema does support a partial, schema-level approach using `PRODUCT`, `COMPONENT_SUPPLIER`, and `ROUTE`, with important gaps.

For the finished or assembled item, start from `PRODUCT`. The target product is identified by `PRODUCT.product…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_3`, `Component Supplier Relationship→COMPONENT_SUPPLIER`, `complex products→PRODUCT`, `parent_chunk_data_dictionary.md_6`, `parent_chunk_data_dictionary.md_7`, `Manufacturing Routing→ROUTE`, `parent_chunk_data_dictionary.md_5`, `parent_chunk_data_dictionary.md_8`

**Context previews (first 3):**

1. _# Manufacturing Data Dictionary  This data dictionary documents the database schema for the manufacturing supply chain system. It includes all tables, columns, data types, constraints, and relationshi…_

2. _Business concept 'Component Supplier Relationship' — This table is a junction entity linking one component to one supplier, with a unique component_id/supplier_id pair and relationship attributes such…_

3. _Business concept 'complex products' is implemented by physical table PRODUCT (columns: product_id, product_name, product_type, parent_product_id, base_cost, lead_time_days, is_active).…_

---

## Anomalies & Observations

No anomalies detected. All questions grounded with acceptable RAGAS scores.
