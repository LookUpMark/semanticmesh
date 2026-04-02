# AB-10 — 04_complex_manufacturing — Run Analysis

**Timestamp:** 2026-03-31 23:50:07  
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
| Triplets extracted | 369 |
| Entities resolved | 127 |
| Tables parsed | 13 |
| Tables completed | 13 |

## Query Evaluation Summary

| Metric | Value |
|--------|-------|
| Questions | 40 |
| Grounded | **40/40 (100%)** |
| Avg GT Coverage | 100% |
| Avg Top Score | 0.4146 |
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
> The manufacturing system stores product master data in the `product` table for all manufactured items, including finished goods, assemblies, and components.

From the provided schema, the stored product information includes the unique product identifier in `product_id`, the product name in `product_name`, the product classification in `product_type`, the parent product in `parent_product_id`, the …

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_3`, `Work Order→WORK_ORDER`, `Actual stock levels of components and products stored in specific warehouses→WAREHOUSE`, `parent_chunk_data_dictionary.md_6`, `Route Step→ROUTE`, `parent_chunk_data_dictionary.md_5`, `parent_chunk_business_glossary.md_0`, `parent_chunk_business_glossary.md_1`

**Context previews (first 3):**

1. _# Manufacturing Data Dictionary  This data dictionary documents the database schema for the manufacturing supply chain system. It includes all tables, columns, data types, constraints, and relationshi…_

2. _Business concept 'Work Order' — The table name, comment, and columns such as product_id, parent_work_order, quantity_ordered, quantity_completed, status, priority, and planned dates all align with a m…_

3. _Business concept 'Actual stock levels of components and products stored in specific warehouses' is implemented by physical table WAREHOUSE (columns: warehouse_id, warehouse_name, address, city, state,…_

---

### ✅ QA-002 — How are components defined in the manufacturing database?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.5910 | **Gate:** `proceed`

**Expected answer:**
> Components are defined with a unique identifier (component_id), descriptive name (component_name), category grouping (component_category), unit of measure (unit_of_measure), standard unit cost (standard_cost), and optional reference to technical specifications (specification_id). Components represen…

**System answer:**
> Components are defined in two closely related ways in the manufacturing database.

At the business level, a Component is described as an atomic raw material or purchased part that cannot be further broken down into simpler manufactured items. Components are the building blocks used in manufacturing and are procured from external suppliers.

At the schema level, there is a physical table named COMP…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_3`, `a parent product, a component product (which can be either a component or sub-assembly), the required quantity, unit of measure, and hierarchical level in the product structure→COMPONENT`, `parent_chunk_data_dictionary.md_4`, `components they can provide through approved supplier relationships→COMPONENT_SUPPLIER`, `parent_chunk_data_dictionary.md_5`, `BOM entry→BOM`, `parent_chunk_business_glossary.md_0`, `parent_chunk_business_glossary.md_1`

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
> The Bill of Materials table, BOM, defines product composition and hierarchical structure. Its purpose is to represent what components go into a parent product and in what quantity, supporting multi-level assemblies through recursive relationships.

From the context, BOM implements the business concept of a “BOM entry” and is used to model assemblies such as a parent product containing component pr…

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
> The system maintains supplier master data in the SUPPLIER table and supplier relationship/transaction data in related tables.

In SUPPLIER, it stores external vendor information for component procurement, including supplier_id, supplier_name, contact_email, contact_phone, rating, and is_preferred. The business concept “Preferred supplier for this component” is mapped to SUPPLIER, so preferred stat…

**Sources retrieved (12):** `Preferred supplier for this component→SUPPLIER`, `parent_chunk_data_dictionary.md_4`, `SHIPMENT→SUPPLIER`, `components they can provide through approved supplier relationships→COMPONENT_SUPPLIER`, `One-to-many with shipment (inbound)→SHIPMENT`, `parent_chunk_data_dictionary.md_8`, `COMPONENT_SUPPLIER→SUPPLIER`, `parent_chunk_data_dictionary.md_3`

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
> Warehouses are represented by the `WAREHOUSE` table. In the schema, `warehouse` stores physical storage location information for inventory management and represents a physical storage location where materials, components, and finished goods are stored.

The `WAREHOUSE` table has these columns: `warehouse_id` as the primary key and unique warehouse identifier, `warehouse_name`, `address`, `city`, `…

**Sources retrieved (12):** `INVENTORY→WAREHOUSE`, `BATCH→WAREHOUSE`, `WORK_ORDER→WAREHOUSE`, `SHIPMENT→WAREHOUSE`, `parent_chunk_data_dictionary.md_6`, `Actual stock levels of components and products stored in specific warehouses→WAREHOUSE`, `parent_chunk_data_dictionary.md_5`, `parent_chunk_data_dictionary.md_8`

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
> The `inventory` table tracks stock levels of components and products at specific warehouse locations. It records the warehouse, either a `component_id` or a `product_id` for the item being stored, the `quantity_on_hand`, `quantity_reserved`, the `reorder_threshold`, and the `last_restock_date`.

From the context, each inventory record supports either a component or a product, but not both in the s…

**Sources retrieved (12):** `INVENTORY→PRODUCT`, `Batches for traceability and inventory management→INVENTORY`, `INVENTORY→WAREHOUSE`, `INVENTORY→COMPONENT`, `Work Order→WORK_ORDER`, `parent_chunk_data_dictionary.md_5`, `Batches for traceability and inventory management→BATCH`, `parent_chunk_data_dictionary.md_7`

**Context previews (first 3):**

1. _Relationship: INVENTORY references PRODUCT via foreign key PRODUCT_ID -> PRODUCT.PRODUCT_ID.…_

2. _Business concept 'Batches for traceability and inventory management' is implemented by physical table INVENTORY (columns: inventory_id, warehouse_id, component_id, product_id, quantity_on_hand, quanti…_

3. _Relationship: INVENTORY references WAREHOUSE via foreign key WAREHOUSE_ID -> WAREHOUSE.WAREHOUSE_ID.…_

---

### ✅ QA-007 — How are work orders structured in the manufacturing system?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.6406 | **Gate:** `proceed`

**Expected answer:**
> Work orders represent production jobs with a unique identifier (work_order_id), product to be manufactured (product_id), optional parent work order for nested hierarchies (parent_work_order), quantity to produce (quantity_ordered), quantity completed so far (quantity_completed), current status (PEND…

**System answer:**
> Work orders are implemented by the physical table `WORK_ORDER` and represent production jobs for manufacturing products. In the business model, a Work Order is a manufacturing production job tracking record, not inventory or product master data.

The structure of a work order includes these columns: `work_order_id` as the primary key and unique work order identifier; `product_id` as a required for…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_6`, `Work Order→WORK_ORDER`, `WORK_ORDER→PRODUCT`, `Route Step→ROUTE`, `WORK_ORDER→WORK_ORDER`, `parent_chunk_data_dictionary.md_3`, `WORK_ORDER→WAREHOUSE`, `Work Order`

**Context previews (first 3):**

1. _## work_order  Represents production jobs for manufacturing products with hierarchical work order support.  | Column | Data Type | Constraints | Description | |--------|-----------|-------------|-----…_

2. _Business concept 'Work Order' — The table name, comment, and columns such as product_id, parent_work_order, quantity_ordered, quantity_completed, status, priority, and planned dates all align with a m…_

3. _Relationship: WORK_ORDER references PRODUCT via foreign key PRODUCT_ID -> PRODUCT.PRODUCT_ID.…_

---

### ✅ QA-008 — What information is captured in the shipment table?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.8515 | **Gate:** `proceed`

**Expected answer:**
> Shipments track material transfers with a unique identifier (shipment_id), shipment type (INBOUND from suppliers, OUTBOUND to customers, INTERNAL between warehouses), destination warehouse (warehouse_id), source supplier for inbound (supplier_id), destination customer for outbound (customer_id), shi…

**System answer:**
> The `SHIPMENT` table captures material transfer information between warehouses, suppliers, and customers. It stores:

`shipment_id`, the unique shipment identifier; `shipment_type`, which is required and indicates whether the shipment is `INBOUND`, `OUTBOUND`, or `INTERNAL`; `warehouse_id`, the warehouse involved in the shipment; `supplier_id`, the supplier reference for inbound shipments; `custom…

**Sources retrieved (12):** `One-to-many with shipment (inbound)→SHIPMENT`, `SHIPMENT→WAREHOUSE`, `SHIPMENT→SUPPLIER`, `parent_chunk_data_dictionary.md_8`, `parent_chunk_data_dictionary.md_5`, `parent_chunk_business_glossary.md_0`, `parent_chunk_business_glossary.md_1`, `Batches for traceability and inventory management→INVENTORY`

**Context previews (first 3):**

1. _Business concept 'One-to-many with shipment (inbound)' is implemented by physical table SHIPMENT (columns: shipment_id, shipment_type, warehouse_id, supplier_id, customer_id, ship_date, estimated_arri…_

2. _Relationship: SHIPMENT references WAREHOUSE via foreign key WAREHOUSE_ID -> WAREHOUSE.WAREHOUSE_ID.…_

3. _Relationship: SHIPMENT references SUPPLIER via foreign key SUPPLIER_ID -> SUPPLIER.SUPPLIER_ID.…_

---

### ✅ QA-009 — How does the quality control system record inspections?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.9540 | **Gate:** `proceed`

**Expected answer:**
> Quality control records are stored with a unique identifier (qc_id), associated production batch (batch_id), applicable specification requirements (specification_id), inspection date (qc_date), inspection type (INCOMING for supplier materials, IN_PROCESS during manufacturing, FINAL for finished good…

**System answer:**
> The quality control system records inspections in the physical table QUALITY_CONTROL, which implements the business concept Quality Control (QC). Each inspection is stored as a QC record with these columns: qc_id, batch_id, specification_id, qc_date, qc_type, inspector_id, result, defect_count, and notes.

From the business definition, a QC record captures inspection and testing performed on mater…

**Sources retrieved (12):** `Quality Control (QC)→QUALITY_CONTROL`, `BOM→PRODUCT`, `parent_chunk_data_dictionary.md_3`, `BATCH→PRODUCT`, `BATCH→WAREHOUSE`, `parent_chunk_business_glossary.md_2`, `parent_chunk_business_glossary.md_0`, `Quality Control (QC)`

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
> Specification records define the technical requirements, standards, and acceptance criteria for materials and products. In the `SPECIFICATION` table, they capture the specification name and version, effective date, specification type (`DIMENSIONAL`, `MATERIAL`, or `PERFORMANCE`), the critical parameter being tested, and the acceptable minimum and maximum values with the unit of measure. These reco…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_7`, `specification types (dimensional, material, performance)→SPECIFICATION`, `Quality Control (QC)→QUALITY_CONTROL`, `a parent product, a component product (which can be either a component or sub-assembly), the required quantity, unit of measure, and hierarchical level in the product structure→COMPONENT`, `parent_chunk_data_dictionary.md_3`, `parent_chunk_business_glossary.md_2`, `parent_chunk_business_glossary.md_0`, `parent_chunk_business_glossary.md_1`

**Context previews (first 3):**

1. _## specification  Defines technical requirements and acceptance criteria for materials and products.  | Column | Data Type | Constraints | Description | |--------|-----------|-------------|-----------…_

2. _Business concept 'specification types (dimensional, material, performance)' is implemented by physical table SPECIFICATION (columns: specification_id, specification_name, version, effective_date, spec…_

3. _Business concept 'Quality Control (QC)' is implemented by physical table QUALITY_CONTROL (columns: qc_id, batch_id, specification_id, qc_date, qc_type, inspector_id, result, defect_count, notes).…_

---

### ✅ QA-011 — How can I find which suppliers provide specific components?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.3227 | **Gate:** `proceed`

**Expected answer:**
> Query the component_supplier table which links components to their approved suppliers. This table contains the component identifier (component_id), supplier identifier (supplier_id), preferred supplier flag (is_preferred), lead time in days (lead_time_days), and unit price (unit_price). Join with th…

**System answer:**
> Use the `COMPONENT_SUPPLIER` table. The business concept “components they can provide through approved supplier relationships” is implemented by `COMPONENT_SUPPLIER`, which has these columns: `component_supplier_id`, `component_id`, `supplier_id`, `is_preferred`, `lead_time_days`, and `unit_price`.

To find which suppliers provide a specific component, follow this join path:
`COMPONENT_SUPPLIER.co…

**Sources retrieved (12):** `components they can provide through approved supplier relationships→COMPONENT_SUPPLIER`, `parent_chunk_data_dictionary.md_5`, `parent_chunk_data_dictionary.md_4`, `Actual stock levels of components and products stored in specific warehouses→WAREHOUSE`, `parent_chunk_data_dictionary.md_3`, `components they can provide through approved supplier relationships`, `parent_chunk_business_glossary.md_0`, `parent_chunk_business_glossary.md_1`

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
> From the retrieved context, you can only trace this at the schema level indirectly.

A `WORK_ORDER` tells you which product is being manufactured through `WORK_ORDER.product_id`, and where it is being produced through `WORK_ORDER.warehouse_id`. The starting join is therefore `WORK_ORDER.product_id -> PRODUCT.product_id`.

From `PRODUCT`, the schema gives you a self-referential hierarchy through `P…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_5`, `Work Order→WORK_ORDER`, `parent_chunk_data_dictionary.md_6`, `Batches for traceability and inventory management→INVENTORY`, `parent_chunk_data_dictionary.md_3`, `components they can provide through approved supplier relationships→COMPONENT_SUPPLIER`, `parent_chunk_data_dictionary.md_8`, `a parent product, a component product (which can be either a component or sub-assembly), the required quantity, unit of measure, and hierarchical level in the product structure→COMPONENT`

**Context previews (first 3):**

1. _## warehouse  Stores physical storage location information for inventory management.  | Column | Data Type | Constraints | Description | |--------|-----------|-------------|-------------| | warehouse_…_

2. _Business concept 'Work Order' — The table name, comment, and columns such as product_id, parent_work_order, quantity_ordered, quantity_completed, status, priority, and planned dates all align with a m…_

3. _## work_order  Represents production jobs for manufacturing products with hierarchical work order support.  | Column | Data Type | Constraints | Description | |--------|-----------|-------------|-----…_

---

### ✅ QA-013 — How can I identify which warehouses have available inventory for specific components?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.8876 | **Gate:** `proceed`

**Expected answer:**
> Query the inventory table filtered by component_id, joining with the warehouse table to get warehouse names and locations. Calculate available quantity as quantity_on_hand minus quantity_reserved. Filter for records where available quantity is greater than zero. Results show warehouse names, locatio…

**System answer:**
> Use the INVENTORY table joined to WAREHOUSE.

The relevant path is INVENTORY.warehouse_id -> WAREHOUSE.warehouse_id. INVENTORY also references the component through INVENTORY.component_id -> COMPONENT.component_id.

To identify warehouses that have inventory for a specific component, filter INVENTORY to the target component_id, then join to WAREHOUSE to return warehouse details such as warehouse_i…

**Sources retrieved (12):** `Actual stock levels of components and products stored in specific warehouses→WAREHOUSE`, `parent_chunk_data_dictionary.md_5`, `INVENTORY→WAREHOUSE`, `Batches for traceability and inventory management→INVENTORY`, `INVENTORY→COMPONENT`, `parent_chunk_data_dictionary.md_3`, `parent_chunk_data_dictionary.md_8`, `Actual stock levels of components and products stored in specific warehouses`

**Context previews (first 3):**

1. _Business concept 'Actual stock levels of components and products stored in specific warehouses' is implemented by physical table WAREHOUSE (columns: warehouse_id, warehouse_name, address, city, state,…_

2. _## warehouse  Stores physical storage location information for inventory management.  | Column | Data Type | Constraints | Description | |--------|-----------|-------------|-------------| | warehouse_…_

3. _Relationship: INVENTORY references WAREHOUSE via foreign key WAREHOUSE_ID -> WAREHOUSE.WAREHOUSE_ID.…_

---

### ✅ QA-014 — How do I find which shipments delivered materials from a specific supplier?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.2401 | **Gate:** `proceed`

**Expected answer:**
> Query the shipment table filtering by supplier_id and shipment_type = 'INBOUND'. Join with the warehouse table to show destination warehouses. Filter for status = 'DELIVERED' and include actual_arrival date. Results can be ordered by ship_date descending to show most recent deliveries first.

**System answer:**
> Use the `SHIPMENT` table as the primary source. Based on the schema, shipments from suppliers are inbound shipments, because `shipment.supplier_id` is “Supplier (inbound only)” and the constraint `chk_supplier_inbound` ensures `supplier_id` is only set for `INBOUND` shipments.

To find shipments delivered from a specific supplier, filter `SHIPMENT` on:
`shipment_type = 'INBOUND'`,
`supplier_id = <…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_8`, `SHIPMENT→SUPPLIER`, `One-to-many with shipment (inbound)→SHIPMENT`, `parent_chunk_data_dictionary.md_5`, `parent_chunk_data_dictionary.md_7`, `parent_chunk_data_dictionary.md_3`, `parent_chunk_data_dictionary.md_4`, `components they can provide through approved supplier relationships→COMPONENT_SUPPLIER`

**Context previews (first 3):**

1. _## shipment  Tracks material transfers between warehouses, suppliers, and customers.  | Column | Data Type | Constraints | Description | |--------|-----------|-------------|-------------| | shipment_i…_

2. _Relationship: SHIPMENT references SUPPLIER via foreign key SUPPLIER_ID -> SUPPLIER.SUPPLIER_ID.…_

3. _Business concept 'One-to-many with shipment (inbound)' is implemented by physical table SHIPMENT (columns: shipment_id, shipment_type, warehouse_id, supplier_id, customer_id, ship_date, estimated_arri…_

---

### ✅ QA-015 — How can I determine which quality control inspections were performed on a specific production batch?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.9779 | **Gate:** `proceed`

**Expected answer:**
> Query the quality_control table filtered by batch_id. Join with the specification table to get requirement details (specification_name, spec_type, acceptable ranges). Include qc_date, qc_type (INCOMING, IN_PROCESS, FINAL), result (PASS, FAIL, CONDITIONAL), and defect_count. This shows the complete i…

**System answer:**
> To determine which quality control inspections were performed on a specific production batch, use the direct relationship between BATCH and QUALITY_CONTROL through batch_id.

The relevant path is BATCH.batch_id = QUALITY_CONTROL.batch_id. Start with the target batch in BATCH, then find all rows in QUALITY_CONTROL whose batch_id matches that batch. The QUALITY_CONTROL table implements the Quality C…

**Sources retrieved (12):** `Quality Control (QC)→QUALITY_CONTROL`, `parent_chunk_data_dictionary.md_7`, `Batches for traceability and inventory management→BATCH`, `BATCH→PRODUCT`, `parent_chunk_data_dictionary.md_5`, `parent_chunk_data_dictionary.md_6`, `parent_chunk_data_dictionary.md_3`, `parent_chunk_business_glossary.md_2`

**Context previews (first 3):**

1. _Business concept 'Quality Control (QC)' is implemented by physical table QUALITY_CONTROL (columns: qc_id, batch_id, specification_id, qc_date, qc_type, inspector_id, result, defect_count, notes).…_

2. _## specification  Defines technical requirements and acceptance criteria for materials and products.  | Column | Data Type | Constraints | Description | |--------|-----------|-------------|-----------…_

3. _Business concept 'Batches for traceability and inventory management' is implemented by physical table BATCH (columns: batch_id, product_id, production_date, quantity_produced, warehouse_id, expiry_dat…_

---

### ✅ QA-016 — How do I track which work orders are in progress at a specific warehouse?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.7311 | **Gate:** `proceed`

**Expected answer:**
> Query the work_order table filtering by warehouse_id and status = 'IN_PROGRESS'. Join with the product table to get product names and types. Include quantity_ordered, quantity_completed, priority, planned_end_date, and calculate progress percentage as (quantity_completed / quantity_ordered * 100). O…

**System answer:**
> Use the `work_order` table and filter on its `status` and `warehouse_id` columns. In the retrieved context, `work_order.status` can be `PENDING`, `IN_PROGRESS`, `COMPLETED`, or `CLOSED`, and `work_order.warehouse_id` is a foreign key to `warehouse.warehouse_id`. So the work orders that are currently in progress at a given warehouse are the rows where `status = 'IN_PROGRESS'` and `warehouse_id` mat…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_5`, `parent_chunk_data_dictionary.md_6`, `WORK_ORDER→WAREHOUSE`, `Work Order→WORK_ORDER`, `Actual stock levels of components and products stored in specific warehouses→WAREHOUSE`, `parent_chunk_data_dictionary.md_8`, `parent_chunk_data_dictionary.md_7`, `parent_chunk_business_glossary.md_1`

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
> Use the `INVENTORY` table as the starting point, because it tracks the actual stock levels of components and products stored in specific warehouses and includes the fields `quantity_on_hand`, `quantity_reserved`, `reorder_threshold`, and `last_restock_date`.

To focus on components, look at `INVENTORY` records where `component_id` is populated, since `INVENTORY.component_id` is a foreign key to `C…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_5`, `Batches for traceability and inventory management→INVENTORY`, `Actual stock levels of components and products stored in specific warehouses→WAREHOUSE`, `INVENTORY→COMPONENT`, `parent_chunk_data_dictionary.md_3`, `parent_chunk_data_dictionary.md_7`, `parent_chunk_data_dictionary.md_4`, `Work Order→WORK_ORDER`

**Context previews (first 3):**

1. _## warehouse  Stores physical storage location information for inventory management.  | Column | Data Type | Constraints | Description | |--------|-----------|-------------|-------------| | warehouse_…_

2. _Business concept 'Batches for traceability and inventory management' is implemented by physical table INVENTORY (columns: inventory_id, warehouse_id, component_id, product_id, quantity_on_hand, quanti…_

3. _Business concept 'Actual stock levels of components and products stored in specific warehouses' is implemented by physical table WAREHOUSE (columns: warehouse_id, warehouse_name, address, city, state,…_

---

### ✅ QA-018 — How do I determine the manufacturing route for a specific product?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.2047 | **Gate:** `proceed`

**Expected answer:**
> Query the route table filtering by product_id, ordered by sequence_number ascending. For each operation, retrieve operation_name, work_center, cycle_time_minutes, and setup_time_minutes. Join with the product table to get product details. The sequence of operations shows the complete manufacturing w…

**System answer:**
> To determine the manufacturing route for a specific product, use the `ROUTE` table, because the business concept `Route Step` is physically implemented there. The route is stored at the step level, not as a separate route header: each row represents an individual manufacturing operation for a product.

The join path is `PRODUCT.product_id` → `ROUTE.product_id`, since `ROUTE` references `PRODUCT` t…

**Sources retrieved (12):** `Route Step→ROUTE`, `parent_chunk_data_dictionary.md_6`, `ROUTE→PRODUCT`, `parent_chunk_data_dictionary.md_3`, `parent_chunk_data_dictionary.md_7`, `Work Order→WORK_ORDER`, `parent_chunk_data_dictionary.md_8`, `Route Step`

**Context previews (first 3):**

1. _Business concept 'Route Step' — The table is row-level by product and sequence_number, with operation_name, work_center, cycle_time_minutes, and setup_time_minutes describing individual manufacturing …_

2. _## work_order  Represents production jobs for manufacturing products with hierarchical work order support.  | Column | Data Type | Constraints | Description | |--------|-----------|-------------|-----…_

3. _Relationship: ROUTE references PRODUCT via foreign key PRODUCT_ID -> PRODUCT.PRODUCT_ID.…_

---

### ✅ QA-019 — How can I find which batches are stored at a specific warehouse and their QC status?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.7533 | **Gate:** `proceed`

**Expected answer:**
> Query the batch table filtering by warehouse_id. Join with the product table to get product names and types. Include production_date, quantity_produced, expiry_date, and qc_status (PENDING, PASSED, FAILED, QUARANTINED). Filter by qc_status to isolate batches requiring quality attention or ready for …

**System answer:**
> Use the BATCH table as the primary source. The business concept “Batches for traceability and inventory management” is implemented by BATCH, which includes batch_id, product_id, production_date, quantity_produced, warehouse_id, expiry_date, and qc_status.

To find batches stored at a specific warehouse, filter BATCH by BATCH.warehouse_id. The retrieved context also states that BATCH references WAR…

**Sources retrieved (12):** `Batches for traceability and inventory management→BATCH`, `parent_chunk_data_dictionary.md_5`, `Actual stock levels of components and products stored in specific warehouses→WAREHOUSE`, `BATCH→WAREHOUSE`, `Quality Control (QC)→QUALITY_CONTROL`, `parent_chunk_data_dictionary.md_6`, `Batches for traceability and inventory management→INVENTORY`, `parent_chunk_data_dictionary.md_8`

**Context previews (first 3):**

1. _Business concept 'Batches for traceability and inventory management' is implemented by physical table BATCH (columns: batch_id, product_id, production_date, quantity_produced, warehouse_id, expiry_dat…_

2. _## warehouse  Stores physical storage location information for inventory management.  | Column | Data Type | Constraints | Description | |--------|-----------|-------------|-------------| | warehouse_…_

3. _Business concept 'Actual stock levels of components and products stored in specific warehouses' is implemented by physical table WAREHOUSE (columns: warehouse_id, warehouse_name, address, city, state,…_

---

### ✅ QA-020 — How do I identify which specifications apply to specific components?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.2550 | **Gate:** `proceed`

**Expected answer:**
> Query the component table and join with the specification table via specification_id. Include component_name, component_category, and specification details (specification_name, spec_type, critical_parameter, min_value, max_value, unit_of_measure). This shows the technical requirements that each comp…

**System answer:**
> To identify which specifications apply to specific components, use the direct link from `COMPONENT.specification_id` to `SPECIFICATION.specification_id`.

The retrieved context shows that the physical table `COMPONENT` includes these columns: `component_id`, `component_name`, `component_category`, `unit_of_measure`, `standard_cost`, and `specification_id`. The `SPECIFICATION` table defines the spe…

**Sources retrieved (12):** `a parent product, a component product (which can be either a component or sub-assembly), the required quantity, unit of measure, and hierarchical level in the product structure→COMPONENT`, `parent_chunk_data_dictionary.md_5`, `parent_chunk_data_dictionary.md_7`, `parent_chunk_data_dictionary.md_3`, `Actual stock levels of components and products stored in specific warehouses→WAREHOUSE`, `specification types (dimensional, material, performance)→SPECIFICATION`, `parent_chunk_data_dictionary.md_4`, `components they can provide through approved supplier relationships→COMPONENT_SUPPLIER`

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
> To do a complete BOM explosion for a finished product, use the `product` and `bom` tables recursively.

Start with the finished product in `product`, using `product.product_id` as the root item. If you want to restrict the starting item to a finished product, `product.product_type` includes `FINISHED_GOOD`, `ASSEMBLY`, and `COMPONENT`, so the root can be identified as a `FINISHED_GOOD` when that c…

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
> From the retrieved context, the schema supports this as a recursive bill-of-materials calculation.

Use the `bom` table to explode the product structure starting from the target product. The join path is `product.product_id` → `bom.parent_product_id`, then for each BOM row `bom.component_product_id` → `product.product_id` again to get the child product. Because both `bom.parent_product_id` and `bo…

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
> Use the `bom` table as the primary structure, because `BOM` is the table that stores “a parent product, a component product … and hierarchical level in the product structure,” with `parent_product_id` and `component_product_id` both pointing to `product(product_id)`.

At the schema level, the trace is:

1. Start in `bom` with the specific component you care about in `component_product_id`.
2. The …

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
> Use the `work_order` and `bom` tables together, with recursive traversal of the BOM hierarchy.

At the schema level, the direct path is `work_order.product_id → bom.parent_product_id`. A work order requires a component when the product being built on the work order has that component somewhere in its BOM structure. Because `bom` supports multi-level assemblies, you cannot stop at the first level: …

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
> Use the `bom` table, because it stores the hierarchy and includes `bom_level`, described as the “depth in product hierarchy” and “tracks depth for performance optimization.”

At the schema level, the simplest way to determine the maximum BOM depth is to take the highest `bom.bom_level` value.

For a specific product, use `bom.parent_product_id` to identify the product being built, then compute the…

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
> Use the BOM hierarchy, not just the `product` row alone.

The relevant table is `bom`, which defines product composition with:

`parent_product_id` = the product being built  
`component_product_id` = the product used inside it  
`bom_level` = depth in the hierarchy

To find all products that contain a specific product as a sub-assembly at any level, start with `bom.component_product_id = <target …

**Sources retrieved (12):** `a parent product, a component product (which can be either a component or sub-assembly), the required quantity, unit of measure, and hierarchical level in the product structure→COMPONENT`, `parent_chunk_data_dictionary.md_3`, `parent_chunk_data_dictionary.md_4`, `parent_chunk_data_dictionary.md_5`, `parent_chunk_data_dictionary.md_7`, `Actual stock levels of components and products stored in specific warehouses→WAREHOUSE`, `parent_chunk_data_dictionary.md_6`, `BOM entry→BOM`

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
> The retrieved context supports tracing the lead times across a product’s full assembly structure, but it does not define a single official business formula for “total lead time.”

At the schema level, the most direct way is to start from the target product in `product`, then traverse the `bom` table recursively. The join path is:

`product.product_id` → `bom.parent_product_id`  
then `bom.componen…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_3`, `(product_id, sequence_number)→PRODUCT`, `a parent product, a component product (which can be either a component or sub-assembly), the required quantity, unit of measure, and hierarchical level in the product structure→COMPONENT`, `components they can provide through approved supplier relationships→COMPONENT_SUPPLIER`, `parent_chunk_data_dictionary.md_4`, `parent_chunk_data_dictionary.md_7`, `parent_chunk_data_dictionary.md_6`, `Route Step→ROUTE`

**Context previews (first 3):**

1. _# Manufacturing Data Dictionary  This data dictionary documents the database schema for the manufacturing supply chain system. It includes all tables, columns, data types, constraints, and relationshi…_

2. _Business concept '(product_id, sequence_number)' is implemented by physical table PRODUCT (columns: product_id, product_name, product_type, parent_product_id, base_cost, lead_time_days, is_active).…_

3. _Business concept 'a parent product, a component product (which can be either a component or sub-assembly), the required quantity, unit of measure, and hierarchical level in the product structure' is i…_

---

### ✅ QA-028 — How do I generate a complete indented BOM report showing the hierarchical structure?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.4180 | **Gate:** `proceed`

**Expected answer:**
> Use a recursive query on the bom table that tracks the current depth level. Start with the top-level product (parent_product_id where product has no parent_product_id). At each level, output component details indented by depth level. Include product_name, quantity, and unit_of_measure. Recursively p…

**System answer:**
> To generate a complete indented BOM report, use the `bom` table as the hierarchy source and the `product` table twice to resolve product details.

The core structure is in `bom`, which represents a BOM entry with:
`bom_id`, `parent_product_id`, `component_product_id`, `quantity`, `unit_of_measure`, `bom_level`, and `is_optional`.

The required join path is:
`bom.parent_product_id -> product.produc…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_4`, `parent_chunk_data_dictionary.md_3`, `a parent product, a component product (which can be either a component or sub-assembly), the required quantity, unit of measure, and hierarchical level in the product structure→COMPONENT`, `parent_chunk_data_dictionary.md_6`, `parent_chunk_data_dictionary.md_8`, `BOM entry→BOM`, `BOM→PRODUCT`, `parent_chunk_business_glossary.md_0`

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
> Use the `bom` table as the primary source, because each BOM entry is one parent-product/component-product relationship and is implemented by `BOM(bom_id, parent_product_id, component_product_id, quantity, unit_of_measure, bom_level, is_optional)`.

To find which components appear most frequently across all product BOMs, group BOM rows by `bom.component_product_id` and count how many BOM entries re…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_4`, `parent_chunk_data_dictionary.md_3`, `BOM entry→BOM`, `BOM→PRODUCT`, `parent_chunk_data_dictionary.md_5`, `a parent product, a component product (which can be either a component or sub-assembly), the required quantity, unit of measure, and hierarchical level in the product structure→COMPONENT`, `Actual stock levels of components and products stored in specific warehouses→WAREHOUSE`, `parent_chunk_data_dictionary.md_7`

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
> From the retrieved context, the BOM structure is recursive: `bom.parent_product_id` and `bom.component_product_id` both reference `product.product_id`, and the `bom` table is explicitly described as supporting multi-level assemblies. That means the schema allows you to trace a hierarchy by repeatedly following `bom.parent_product_id -> bom.component_product_id`.

At a schema level, a circular refe…

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
> From the provided context, you can determine the complete product structure for a finished product, but you cannot fully determine the complete supplier chain for that structure because the retrieved schema does not show a direct relationship between suppliers and specific products, components, or BOM lines.

What you can do from the schema is this:

Start with the finished product in `product`, w…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_3`, `a parent product, a component product (which can be either a component or sub-assembly), the required quantity, unit of measure, and hierarchical level in the product structure→COMPONENT`, `parent_chunk_data_dictionary.md_4`, `parent_chunk_data_dictionary.md_8`, `parent_chunk_data_dictionary.md_6`, `parent_chunk_data_dictionary.md_7`, `Route Step→ROUTE`, `parent_chunk_data_dictionary.md_5`

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
> The retrieved context does not define a business rule for “sufficient inventory” or a formula for fulfillment. It also does not define any work-order material requirement structure, so it cannot tell you how much stock is required to satisfy a work order.

What the schema does support is tracing the relevant records.

Start from `WORK_ORDER`, using `work_order_id` to get the work order’s `product_…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_5`, `parent_chunk_data_dictionary.md_6`, `Work Order→WORK_ORDER`, `INVENTORY→WAREHOUSE`, `Actual stock levels of components and products stored in specific warehouses→WAREHOUSE`, `WORK_ORDER→WAREHOUSE`, `Batches for traceability and inventory management→INVENTORY`, `parent_chunk_business_glossary.md_1`

**Context previews (first 3):**

1. _## warehouse  Stores physical storage location information for inventory management.  | Column | Data Type | Constraints | Description | |--------|-----------|-------------|-------------| | warehouse_…_

2. _## work_order  Represents production jobs for manufacturing products with hierarchical work order support.  | Column | Data Type | Constraints | Description | |--------|-----------|-------------|-----…_

3. _Business concept 'Work Order' — The table name, comment, and columns such as product_id, parent_work_order, quantity_ordered, quantity_completed, status, priority, and planned dates all align with a m…_

---

### ✅ QA-033 — How can I find which quality control inspections failed for components from specific suppliers?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.4561 | **Gate:** `proceed`

**Expected answer:**
> Query the quality_control table filtering by result = 'FAIL'. Join with the batch table to get product_id and production_date. Join with the bom table recursively to trace which products contain failed components. Join with component_supplier and supplier tables to identify the source supplier. Filt…

**System answer:**
> From the retrieved context, the identifiable “failed quality control inspections” are in `QUALITY_CONTROL`, using:

- `qc_id`
- `batch_id`
- `specification_id`
- `qc_date`
- `qc_type`
- `inspector_id`
- `result`
- `defect_count`
- `notes`

To isolate failures, filter `QUALITY_CONTROL.result = 'FAIL'`. If you specifically mean inspections of incoming supplied material, the QC concept also defines `…

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
> From the retrieved context, the schema-supported way to calculate total manufacturing time for a work order including all sub-assembly work orders is to use the `WORK_ORDER` hierarchy together with the product-level `ROUTE` steps.

`WORK_ORDER` is explicitly hierarchical: `parent_work_order` is a self-referencing foreign key to `work_order.work_order_id`, and the description says this “enables wor…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_6`, `Work Order→WORK_ORDER`, `parent_chunk_data_dictionary.md_3`, `Route Step→ROUTE`, `a parent product, a component product (which can be either a component or sub-assembly), the required quantity, unit of measure, and hierarchical level in the product structure→COMPONENT`, `parent_chunk_data_dictionary.md_7`, `parent_chunk_data_dictionary.md_5`, `parent_chunk_business_glossary.md_0`

**Context previews (first 3):**

1. _## work_order  Represents production jobs for manufacturing products with hierarchical work order support.  | Column | Data Type | Constraints | Description | |--------|-----------|-------------|-----…_

2. _Business concept 'Work Order' — The table name, comment, and columns such as product_id, parent_work_order, quantity_ordered, quantity_completed, status, priority, and planned dates all align with a m…_

3. _# Manufacturing Data Dictionary  This data dictionary documents the database schema for the manufacturing supply chain system. It includes all tables, columns, data types, constraints, and relationshi…_

---

### ✅ QA-035 — How can I identify which shipments are overdue and their impact on work orders?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0719 | **Gate:** `proceed_with_warning`

**Expected answer:**
> Query the shipment table filtering for status = 'SHIPPED' where actual_arrival is NULL and estimated_arrival is in the past (overdue). Join with the component_supplier table via supplier_id and component_id to identify which components are delayed. Perform reverse BOM lookup to find which parent pro…

**System answer:**
> From the retrieved schema, you can identify overdue shipments at the schema level from `SHIPMENT` using its date and status fields, and then assess possible work-order impact only through the shared warehouse.

An overdue shipment can be evaluated from `shipment.estimated_arrival`, `shipment.actual_arrival`, and `shipment.status`. The table provides these relevant fields: `shipment_id`, `shipment_…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_5`, `parent_chunk_data_dictionary.md_8`, `Work Order→WORK_ORDER`, `parent_chunk_data_dictionary.md_6`, `WORK_ORDER→PRODUCT`, `WORK_ORDER→WAREHOUSE`, `SHIPMENT→WAREHOUSE`, `One-to-many with shipment (inbound)→SHIPMENT`

**Context previews (first 3):**

1. _## warehouse  Stores physical storage location information for inventory management.  | Column | Data Type | Constraints | Description | |--------|-----------|-------------|-------------| | warehouse_…_

2. _## shipment  Tracks material transfers between warehouses, suppliers, and customers.  | Column | Data Type | Constraints | Description | |--------|-----------|-------------|-------------| | shipment_i…_

3. _Business concept 'Work Order' — The table name, comment, and columns such as product_id, parent_work_order, quantity_ordered, quantity_completed, status, priority, and planned dates all align with a m…_

---

### ✅ QA-036 — How do I find which batches are approaching or past expiry and contain components from specific suppliers?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.1479 | **Gate:** `proceed_with_warning`

**Expected answer:**
> Query the batch table filtering for expiry_date within a warning window (e.g., next 30 days) or past expiry. Join with the bom table recursively on product_id to trace all components used in those batches. Join with component_supplier and supplier tables to filter by specific suppliers. Results iden…

**System answer:**
> From the retrieved context, you can identify batches that are approaching or past expiry from the `batch` table, but you cannot fully determine which of those batches contain components from specific suppliers because the retrieved context does not include the table definition or join columns for the product-to-component structure or the approved supplier-to-component relationship.

What is availa…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_5`, `Actual stock levels of components and products stored in specific warehouses→WAREHOUSE`, `Batches for traceability and inventory management→BATCH`, `parent_chunk_data_dictionary.md_7`, `Batches for traceability and inventory management→INVENTORY`, `parent_chunk_data_dictionary.md_3`, `parent_chunk_data_dictionary.md_8`, `parent_chunk_business_glossary.md_2`

**Context previews (first 3):**

1. _## warehouse  Stores physical storage location information for inventory management.  | Column | Data Type | Constraints | Description | |--------|-----------|-------------|-------------| | warehouse_…_

2. _Business concept 'Actual stock levels of components and products stored in specific warehouses' is implemented by physical table WAREHOUSE (columns: warehouse_id, warehouse_name, address, city, state,…_

3. _Business concept 'Batches for traceability and inventory management' is implemented by physical table BATCH (columns: batch_id, product_id, production_date, quantity_produced, warehouse_id, expiry_dat…_

---

### ✅ QA-037 — How can I generate a material requirements plan showing when to order components based on work order schedules?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0433 | **Gate:** `proceed_with_warning`

**Expected answer:**
> Query all work_orders with status 'PENDING' ordered by planned_start_date. For each work_order, perform BOM explosion to get required components and quantities. For each component, query inventory for current available stock across warehouses. Calculate net requirements = (required quantity * work_o…

**System answer:**
> From the retrieved schema, you can generate a material requirements plan by exploding each `WORK_ORDER` into its bill of materials and then attaching schedule and lead-time data.

The core join path is `WORK_ORDER.product_id -> BOM.parent_product_id`. `WORK_ORDER` gives the production job and schedule fields: `work_order_id`, `product_id`, `quantity_ordered`, `quantity_completed`, `status`, `plann…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_6`, `parent_chunk_data_dictionary.md_7`, `Work Order→WORK_ORDER`, `parent_chunk_data_dictionary.md_5`, `parent_chunk_data_dictionary.md_4`, `parent_chunk_data_dictionary.md_3`, `components they can provide through approved supplier relationships→COMPONENT_SUPPLIER`, `WORK_ORDER→WORK_ORDER`

**Context previews (first 3):**

1. _## work_order  Represents production jobs for manufacturing products with hierarchical work order support.  | Column | Data Type | Constraints | Description | |--------|-----------|-------------|-----…_

2. _## specification  Defines technical requirements and acceptance criteria for materials and products.  | Column | Data Type | Constraints | Description | |--------|-----------|-------------|-----------…_

3. _Business concept 'Work Order' — The table name, comment, and columns such as product_id, parent_work_order, quantity_ordered, quantity_completed, status, priority, and planned dates all align with a m…_

---

### ✅ QA-038 — How do I trace the complete genealogy of a component from supplier through batch to finished goods?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0748 | **Gate:** `proceed_with_warning`

**Expected answer:**
> Start with a shipment from the supplier (shipment table with supplier_id and shipment_type = 'INBOUND'). Track to inventory updates via component_id and warehouse_id. Identify batches that consumed the component via reverse BOM lookup (batch.product_id → bom hierarchy → component_id). Query quality_…

**System answer:**
> From the retrieved schema, you can trace this only partially at the schema level.

The supplier end starts with `SUPPLIER` and the approved sourcing relationship is `COMPONENT_SUPPLIER(component_id, supplier_id, is_preferred, lead_time_days, unit_price)`. That lets you identify which suppliers are approved to provide a given `component_id`, and with what preferred flag, lead time, and unit price.
…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_3`, `parent_chunk_data_dictionary.md_7`, `parent_chunk_data_dictionary.md_5`, `parent_chunk_data_dictionary.md_8`, `Batches for traceability and inventory management→INVENTORY`, `parent_chunk_data_dictionary.md_4`, `components they can provide through approved supplier relationships→COMPONENT_SUPPLIER`, `Batches for traceability and inventory management→BATCH`

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
> From the retrieved context, I can only answer this partially at the schema level.

What is known:
The context shows that supplier relationships for components are represented by the physical table `COMPONENT_SUPPLIER`, with columns `component_supplier_id`, `component_id`, `supplier_id`, `is_preferred`, `lead_time_days`, and `unit_price`. This is the table you would use to find multiple suppliers f…

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
> The retrieved context does not define an exact “total landed cost” formula, so you cannot compute a fully specified landed cost from the knowledge graph alone. In particular, the context does not provide freight, duty, tax, labor rates, overhead rates, or warehouse handling cost data. It also does not expose a clean, fully defined bill-of-material quantity table that would let you reliably multipl…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_3`, `components they can provide through approved supplier relationships→COMPONENT_SUPPLIER`, `(product_id, sequence_number)→PRODUCT`, `a parent product, a component product (which can be either a component or sub-assembly), the required quantity, unit of measure, and hierarchical level in the product structure→COMPONENT`, `parent_chunk_data_dictionary.md_6`, `parent_chunk_data_dictionary.md_7`, `Route Step→ROUTE`, `parent_chunk_data_dictionary.md_5`

**Context previews (first 3):**

1. _# Manufacturing Data Dictionary  This data dictionary documents the database schema for the manufacturing supply chain system. It includes all tables, columns, data types, constraints, and relationshi…_

2. _Business concept 'components they can provide through approved supplier relationships' is implemented by physical table COMPONENT_SUPPLIER (columns: component_supplier_id, component_id, supplier_id, i…_

3. _Business concept '(product_id, sequence_number)' is implemented by physical table PRODUCT (columns: product_id, product_name, product_type, parent_product_id, base_cost, lead_time_days, is_active).…_

---

## Anomalies & Observations

No anomalies detected. All questions grounded with acceptable RAGAS scores.
