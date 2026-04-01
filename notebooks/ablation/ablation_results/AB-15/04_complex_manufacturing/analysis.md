# AB-15 — 04_complex_manufacturing — Run Analysis

**Timestamp:** 2026-03-31 20:54:56  
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
| Triplets extracted | 390 |
| Entities resolved | 129 |
| Tables parsed | 13 |
| Tables completed | 13 |

## Query Evaluation Summary

| Metric | Value |
|--------|-------|
| Questions | 40 |
| Grounded | **40/40 (100%)** |
| Avg GT Coverage | 100% |
| Avg Top Score | 0.4512 |
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
> The manufacturing system stores products in the `product` table. A product represents any manufactured item, including finished goods, assemblies or sub-assemblies, and components.

For each product, the system stores the product’s unique identifier in `product_id` (`VARCHAR(20)`, primary key), its name in `product_name` (`VARCHAR(100)`, not null), its classification in `product_type` (default `FI…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_3`, `Actual stock levels of components and products stored in specific warehouses→WAREHOUSE`, `Route→ROUTE`, `parent_chunk_data_dictionary.md_6`, `Work Order→WORK_ORDER`, `parent_chunk_data_dictionary.md_5`, `parent_chunk_business_glossary.md_0`, `parent_chunk_business_glossary.md_1`

**Context previews (first 3):**

1. _# Manufacturing Data Dictionary  This data dictionary documents the database schema for the manufacturing supply chain system. It includes all tables, columns, data types, constraints, and relationshi…_

2. _Business concept 'Actual stock levels of components and products stored in specific warehouses' is implemented by physical table WAREHOUSE (columns: warehouse_id, warehouse_name, address, city, state,…_

3. _Business concept 'Route' — The table is explicitly labeled as a ROUTE table for manufacturing workflow steps, and its columns capture operation sequence, work center, cycle time, and setup time for a …_

---

### ✅ QA-002 — How are components defined in the manufacturing database?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.5910 | **Gate:** `proceed`

**Expected answer:**
> Components are defined with a unique identifier (component_id), descriptive name (component_name), category grouping (component_category), unit of measure (unit_of_measure), standard unit cost (standard_cost), and optional reference to technical specifications (specification_id). Components represen…

**System answer:**
> In the manufacturing database, a component is defined as an atomic raw material or purchased part that cannot be further broken down into simpler manufactured items. The business glossary says components are the building blocks used in manufacturing and are procured from external suppliers.

At the schema level, components appear in multiple related structures:

The physical table COMPONENT is ide…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_3`, `a parent product, a component product (which can be either a component or sub-assembly), the required quantity, unit of measure, and hierarchical level in the product structure→COMPONENT`, `parent_chunk_data_dictionary.md_4`, `a parent product, a component product (which can be either a component or sub-assembly), the required quantity, unit of measure, and hierarchical level in the product structure→PRODUCT`, `The Bill of Materials (BOM)→BOM`, `parent_chunk_data_dictionary.md_5`, `parent_chunk_business_glossary.md_0`, `parent_chunk_business_glossary.md_1`

**Context previews (first 3):**

1. _# Manufacturing Data Dictionary  This data dictionary documents the database schema for the manufacturing supply chain system. It includes all tables, columns, data types, constraints, and relationshi…_

2. _Business concept 'a parent product, a component product (which can be either a component or sub-assembly), the required quantity, unit of measure, and hierarchical level in the product structure' is i…_

3. _## bom  Bill of Materials defining product composition and hierarchical structure. Supports recursive relationships for multi-level assemblies.  | Column | Data Type | Constraints | Description | |---…_

---

### ✅ QA-003 — What is the purpose of the Bill of Materials (BOM) table?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.9858 | **Gate:** `proceed`

**Expected answer:**
> The BOM table defines the hierarchical structure of products by specifying which components or sub-assemblies are required to manufacture each parent product. It records the unique BOM entry identifier (bom_id), parent product being built (parent_product_id), component or sub-assembly product (compo…

**System answer:**
> The Bill of Materials (BOM) table defines product composition and hierarchical structure. In the context, the business concept “The Bill of Materials (BOM)” is implemented by the physical table BOM, which stores how a parent product is built from component products.

Its purpose is to represent multi-level assemblies through recursive relationships: both `parent_product_id` and `component_product_…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_4`, `The Bill of Materials (BOM)→BOM`, `BOM→PRODUCT`, `parent_chunk_data_dictionary.md_3`, `Shipment`, `parent_chunk_data_dictionary.md_7`, `parent_chunk_data_dictionary.md_8`, `Shipment→SHIPMENT`

**Context previews (first 3):**

1. _## bom  Bill of Materials defining product composition and hierarchical structure. Supports recursive relationships for multi-level assemblies.  | Column | Data Type | Constraints | Description | |---…_

2. _Business concept 'The Bill of Materials (BOM)' is implemented by physical table BOM (columns: bom_id, parent_product_id, component_product_id, quantity, unit_of_measure, bom_level, is_optional).…_

3. _Relationship: BOM references PRODUCT via foreign key COMPONENT_PRODUCT_ID -> PRODUCT.PRODUCT_ID.…_

---

### ✅ QA-004 — What supplier information does the system maintain?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0318 | **Gate:** `proceed_with_warning`

**Expected answer:**
> Suppliers are tracked with a unique identifier (supplier_id), legal business name (supplier_name), primary contact email (contact_email), primary contact phone number (contact_phone), performance rating from 1.0 to 5.0 (rating), and preferred supplier status flag (is_preferred).

**System answer:**
> The system maintains supplier master data in the `supplier` table, but in the retrieved context only two supplier attributes are explicitly shown: `supplier_id` as the unique supplier identifier and `supplier_name` as the supplier name.

Beyond the core supplier record, the schema also stores supplier-related procurement and logistics information through relationships. In `component_supplier`, a s…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_4`, `SHIPMENT→SUPPLIER`, `Shipment`, `parent_chunk_data_dictionary.md_8`, `COMPONENT_SUPPLIER→SUPPLIER`, `Component-Supplier Link→COMPONENT_SUPPLIER`, `Shipment→SHIPMENT`, `parent_chunk_data_dictionary.md_3`

**Context previews (first 3):**

1. _## bom  Bill of Materials defining product composition and hierarchical structure. Supports recursive relationships for multi-level assemblies.  | Column | Data Type | Constraints | Description | |---…_

2. _Relationship: SHIPMENT references SUPPLIER via foreign key SUPPLIER_ID -> SUPPLIER.SUPPLIER_ID.…_

3. _Shipment: The table is explicitly labeled as SHIPMENT and contains shipment-specific attributes such as shipment type, ship/arrival dates, and status. Foreign keys to warehouse, supplier, and customer…_

---

### ✅ QA-005 — How are warehouses represented in the schema?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.3381 | **Gate:** `proceed`

**Expected answer:**
> Warehouses are defined with a unique identifier (warehouse_id), descriptive name (warehouse_name), full street address (address), city location (city), state or province (state), total storage capacity in cubic meters (capacity), and optional manager identifier (manager_id).

**System answer:**
> Warehouses are represented by the physical table `warehouse`, which stores physical storage location information for inventory management.

The `warehouse` table has these columns: `warehouse_id` as the primary key and unique warehouse identifier, `warehouse_name` as the required warehouse name, `address`, `city`, `state`, `capacity` as a required integer with default 0 and a check constraint `> 0…

**Sources retrieved (12):** `INVENTORY→WAREHOUSE`, `BATCH→WAREHOUSE`, `WORK_ORDER→WAREHOUSE`, `SHIPMENT→WAREHOUSE`, `parent_chunk_data_dictionary.md_6`, `Actual stock levels of components and products stored in specific warehouses→WAREHOUSE`, `parent_chunk_data_dictionary.md_5`, `Shipment`

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
> The `inventory` table tracks stock levels of components and products at specific warehouse locations. It records the warehouse, either a `component_id` or a `product_id` for the item being stocked, `quantity_on_hand`, `quantity_reserved` for pending orders, `reorder_threshold` to support replenishment, and `last_restock_date` as the restock timestamp. The context also states that each inventory re…

**Sources retrieved (12):** `INVENTORY→PRODUCT`, `Batches for traceability and inventory management→INVENTORY`, `INVENTORY→WAREHOUSE`, `Shipment`, `INVENTORY→COMPONENT`, `parent_chunk_data_dictionary.md_5`, `Batches for traceability and inventory management→BATCH`, `Shipment→SHIPMENT`

**Context previews (first 3):**

1. _Relationship: INVENTORY references PRODUCT via foreign key PRODUCT_ID -> PRODUCT.PRODUCT_ID.…_

2. _Business concept 'Batches for traceability and inventory management' is implemented by physical table INVENTORY (columns: inventory_id, warehouse_id, component_id, product_id, quantity_on_hand, quanti…_

3. _Relationship: INVENTORY references WAREHOUSE via foreign key WAREHOUSE_ID -> WAREHOUSE.WAREHOUSE_ID.…_

---

### ✅ QA-007 — How are work orders structured in the manufacturing system?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.7465 | **Gate:** `proceed`

**Expected answer:**
> Work orders represent production jobs with a unique identifier (work_order_id), product to be manufactured (product_id), optional parent work order for nested hierarchies (parent_work_order), quantity to produce (quantity_ordered), quantity completed so far (quantity_completed), current status (PEND…

**System answer:**
> Work orders are represented by the physical table WORK_ORDER and correspond to the business concept of a production job or manufacturing run. The structure is centered on work_order_id, which is the primary key and uniquely identifies each work order.

A work order is tied to the product being manufactured through product_id, which is required and is a foreign key to PRODUCT.PRODUCT_ID. This conne…

**Sources retrieved (12):** `Work Order→WORK_ORDER`, `parent_chunk_data_dictionary.md_6`, `WORK_ORDER→PRODUCT`, `WORK_ORDER→WORK_ORDER`, `parent_chunk_data_dictionary.md_3`, `WORK_ORDER→WAREHOUSE`, `Route→ROUTE`, `a parent product, a component product (which can be either a component or sub-assembly), the required quantity, unit of measure, and hierarchical level in the product structure→PRODUCT`

**Context previews (first 3):**

1. _Business concept 'Work Order' — The table name, primary key, and columns like product_id, parent_work_order, quantity_ordered, quantity_completed, status, priority, and planned dates align directly wi…_

2. _## work_order  Represents production jobs for manufacturing products with hierarchical work order support.  | Column | Data Type | Constraints | Description | |--------|-----------|-------------|-----…_

3. _Relationship: WORK_ORDER references PRODUCT via foreign key PRODUCT_ID -> PRODUCT.PRODUCT_ID.…_

---

### ✅ QA-008 — What information is captured in the shipment table?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.9839 | **Gate:** `proceed`

**Expected answer:**
> Shipments track material transfers with a unique identifier (shipment_id), shipment type (INBOUND from suppliers, OUTBOUND to customers, INTERNAL between warehouses), destination warehouse (warehouse_id), source supplier for inbound (supplier_id), destination customer for outbound (customer_id), shi…

**System answer:**
> The `SHIPMENT` table captures material transfers between warehouses, suppliers, and customers. It stores:

`shipment_id`, the unique shipment identifier; `shipment_type`, which is required and indicates whether the shipment is `INBOUND`, `OUTBOUND`, or `INTERNAL`; `warehouse_id`, a warehouse reference; `supplier_id`, a supplier reference used for inbound shipments; `customer_id`, a customer refere…

**Sources retrieved (12):** `Shipment`, `Shipment→SHIPMENT`, `SHIPMENT→WAREHOUSE`, `SHIPMENT→SUPPLIER`, `parent_chunk_data_dictionary.md_8`, `parent_chunk_data_dictionary.md_5`, `parent_chunk_business_glossary.md_0`, `parent_chunk_business_glossary.md_1`

**Context previews (first 3):**

1. _Shipment: The table is explicitly labeled as SHIPMENT and contains shipment-specific attributes such as shipment type, ship/arrival dates, and status. Foreign keys to warehouse, supplier, and customer…_

2. _Business concept 'Shipment' — The table is explicitly labeled as SHIPMENT and contains shipment-specific attributes such as shipment type, ship/arrival dates, and status. Foreign keys to warehouse, su…_

3. _Relationship: SHIPMENT references WAREHOUSE via foreign key WAREHOUSE_ID -> WAREHOUSE.WAREHOUSE_ID.…_

---

### ✅ QA-009 — How does the quality control system record inspections?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.9540 | **Gate:** `proceed`

**Expected answer:**
> Quality control records are stored with a unique identifier (qc_id), associated production batch (batch_id), applicable specification requirements (specification_id), inspection date (qc_date), inspection type (INCOMING for supplier materials, IN_PROCESS during manufacturing, FINAL for finished good…

**System answer:**
> The quality control system records inspections in the physical table QUALITY_CONTROL, which implements the business concept inspection and testing records for quality assurance.

Each inspection is stored as a QC record with these columns: qc_id, batch_id, specification_id, qc_date, qc_type, inspector_id, result, defect_count, and notes.

From the glossary and concept definition, this means an ins…

**Sources retrieved (12):** `inspection and testing records for quality assurance→QUALITY_CONTROL`, `BOM→PRODUCT`, `parent_chunk_data_dictionary.md_3`, `BATCH→PRODUCT`, `BATCH→WAREHOUSE`, `Specifications for quality requirements→SPECIFICATION`, `parent_chunk_business_glossary.md_2`, `inspection and testing records for quality assurance`

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
> Specification records define the technical requirements, standards, and acceptance criteria for materials and products. In the schema, the `SPECIFICATION` table captures the specification name and version, effective date, specification type (`DIMENSIONAL`, `MATERIAL`, `PERFORMANCE`), the critical parameter being tested, acceptable minimum and maximum values, and the unit of measure. These records …

**Sources retrieved (12):** `inspection and testing records for quality assurance→QUALITY_CONTROL`, `parent_chunk_data_dictionary.md_7`, `Specifications for quality requirements→SPECIFICATION`, `a parent product, a component product (which can be either a component or sub-assembly), the required quantity, unit of measure, and hierarchical level in the product structure→COMPONENT`, `parent_chunk_data_dictionary.md_3`, `parent_chunk_business_glossary.md_2`, `parent_chunk_business_glossary.md_0`, `inspection and testing records for quality assurance`

**Context previews (first 3):**

1. _Business concept 'inspection and testing records for quality assurance' is implemented by physical table QUALITY_CONTROL (columns: qc_id, batch_id, specification_id, qc_date, qc_type, inspector_id, re…_

2. _## specification  Defines technical requirements and acceptance criteria for materials and products.  | Column | Data Type | Constraints | Description | |--------|-----------|-------------|-----------…_

3. _Business concept 'Specifications for quality requirements' is implemented by physical table SPECIFICATION (columns: specification_id, specification_name, version, effective_date, spec_type, critical_p…_

---

### ✅ QA-011 — How can I find which suppliers provide specific components?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.5595 | **Gate:** `proceed`

**Expected answer:**
> Query the component_supplier table which links components to their approved suppliers. This table contains the component identifier (component_id), supplier identifier (supplier_id), preferred supplier flag (is_preferred), lead time in days (lead_time_days), and unit price (unit_price). Join with th…

**System answer:**
> Use the `COMPONENT_SUPPLIER` table. In the context, it is explicitly the many-to-many junction that links components to approved suppliers, and it also stores supplier-specific procurement terms.

To find which suppliers provide a specific component, follow this schema path: `COMPONENT.component_id` → `COMPONENT_SUPPLIER.component_id` → `COMPONENT_SUPPLIER.supplier_id` → `SUPPLIER.supplier_id`.

F…

**Sources retrieved (12):** `Component-Supplier Link→COMPONENT_SUPPLIER`, `parent_chunk_data_dictionary.md_5`, `parent_chunk_data_dictionary.md_4`, `Actual stock levels of components and products stored in specific warehouses→WAREHOUSE`, `parent_chunk_data_dictionary.md_3`, `parent_chunk_data_dictionary.md_8`, `Component-Supplier Link`, `parent_chunk_business_glossary.md_0`

**Context previews (first 3):**

1. _Business concept 'Component-Supplier Link' — The table is explicitly described as a many-to-many relationship linking components to approved suppliers, and its columns carry supplier-specific pricing,…_

2. _## warehouse  Stores physical storage location information for inventory management.  | Column | Data Type | Constraints | Description | |--------|-----------|-------------|-------------| | warehouse_…_

3. _## bom  Bill of Materials defining product composition and hierarchical structure. Supports recursive relationships for multi-level assemblies.  | Column | Data Type | Constraints | Description | |---…_

---

### ✅ QA-012 — How do I trace which components are needed to fulfill a work order?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.2334 | **Gate:** `proceed`

**Expected answer:**
> Start with the work_order table to get the product_id being manufactured. Join to the bom table using product_id as parent_product_id to find all direct components and sub-assemblies. For each component_product_id, if it is an ASSEMBLY type product, recursively query the bom table again to explode m…

**System answer:**
> To trace component needs for a work order from the retrieved schema, start with `WORK_ORDER`. Use `work_order_id` to get the manufacturing job, then read at least `product_id` and `warehouse_id`. `WORK_ORDER.product_id` identifies the product being manufactured, and `WORK_ORDER.warehouse_id` gives the production location. If the job is decomposed, `WORK_ORDER.parent_work_order` lets you recursivel…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_5`, `Work Order→WORK_ORDER`, `parent_chunk_data_dictionary.md_6`, `Batches for traceability and inventory management→INVENTORY`, `parent_chunk_data_dictionary.md_3`, `parent_chunk_data_dictionary.md_8`, `a parent product, a component product (which can be either a component or sub-assembly), the required quantity, unit of measure, and hierarchical level in the product structure→COMPONENT`, `parent_chunk_business_glossary.md_1`

**Context previews (first 3):**

1. _## warehouse  Stores physical storage location information for inventory management.  | Column | Data Type | Constraints | Description | |--------|-----------|-------------|-------------| | warehouse_…_

2. _Business concept 'Work Order' — The table name, primary key, and columns like product_id, parent_work_order, quantity_ordered, quantity_completed, status, priority, and planned dates align directly wi…_

3. _## work_order  Represents production jobs for manufacturing products with hierarchical work order support.  | Column | Data Type | Constraints | Description | |--------|-----------|-------------|-----…_

---

### ✅ QA-013 — How can I identify which warehouses have available inventory for specific components?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.8876 | **Gate:** `proceed`

**Expected answer:**
> Query the inventory table filtered by component_id, joining with the warehouse table to get warehouse names and locations. Calculate available quantity as quantity_on_hand minus quantity_reserved. Filter for records where available quantity is greater than zero. Results show warehouse names, locatio…

**System answer:**
> Use the `inventory` table to find component-specific stock records, and join it to `warehouse` to identify the warehouse details.

From the retrieved context, the relevant path is `INVENTORY.WAREHOUSE_ID -> WAREHOUSE.WAREHOUSE_ID`, and `INVENTORY.COMPONENT_ID -> COMPONENT.COMPONENT_ID`.

For a specific component, look in `inventory` for rows where `component_id` matches that component, then join t…

**Sources retrieved (12):** `Actual stock levels of components and products stored in specific warehouses→WAREHOUSE`, `parent_chunk_data_dictionary.md_5`, `INVENTORY→WAREHOUSE`, `Batches for traceability and inventory management→INVENTORY`, `INVENTORY→COMPONENT`, `parent_chunk_data_dictionary.md_3`, `parent_chunk_data_dictionary.md_8`, `parent_chunk_data_dictionary.md_6`

**Context previews (first 3):**

1. _Business concept 'Actual stock levels of components and products stored in specific warehouses' is implemented by physical table WAREHOUSE (columns: warehouse_id, warehouse_name, address, city, state,…_

2. _## warehouse  Stores physical storage location information for inventory management.  | Column | Data Type | Constraints | Description | |--------|-----------|-------------|-------------| | warehouse_…_

3. _Relationship: INVENTORY references WAREHOUSE via foreign key WAREHOUSE_ID -> WAREHOUSE.WAREHOUSE_ID.…_

---

### ✅ QA-014 — How do I find which shipments delivered materials from a specific supplier?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.4954 | **Gate:** `proceed`

**Expected answer:**
> Query the shipment table filtering by supplier_id and shipment_type = 'INBOUND'. Join with the warehouse table to show destination warehouses. Filter for status = 'DELIVERED' and include actual_arrival date. Results can be ordered by ship_date descending to show most recent deliveries first.

**System answer:**
> Use the `shipment` table. It is the table that “tracks material transfers between warehouses, suppliers, and customers,” and it contains the fields you need: `shipment_id`, `shipment_type`, `supplier_id`, `warehouse_id`, `ship_date`, `estimated_arrival`, `actual_arrival`, and `status`.

To find shipments delivered from a specific supplier, filter `shipment` by:
`shipment.supplier_id = <specific su…

**Sources retrieved (12):** `Shipment`, `parent_chunk_data_dictionary.md_8`, `Shipment→SHIPMENT`, `SHIPMENT→SUPPLIER`, `parent_chunk_data_dictionary.md_5`, `Component-Supplier Link→COMPONENT_SUPPLIER`, `parent_chunk_data_dictionary.md_7`, `parent_chunk_business_glossary.md_1`

**Context previews (first 3):**

1. _Shipment: The table is explicitly labeled as SHIPMENT and contains shipment-specific attributes such as shipment type, ship/arrival dates, and status. Foreign keys to warehouse, supplier, and customer…_

2. _## shipment  Tracks material transfers between warehouses, suppliers, and customers.  | Column | Data Type | Constraints | Description | |--------|-----------|-------------|-------------| | shipment_i…_

3. _Business concept 'Shipment' — The table is explicitly labeled as SHIPMENT and contains shipment-specific attributes such as shipment type, ship/arrival dates, and status. Foreign keys to warehouse, su…_

---

### ✅ QA-015 — How can I determine which quality control inspections were performed on a specific production batch?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.9779 | **Gate:** `proceed`

**Expected answer:**
> Query the quality_control table filtered by batch_id. Join with the specification table to get requirement details (specification_name, spec_type, acceptable ranges). Include qc_date, qc_type (INCOMING, IN_PROCESS, FINAL), result (PASS, FAIL, CONDITIONAL), and defect_count. This shows the complete i…

**System answer:**
> Use the `QUALITY_CONTROL` table, because the business concept “inspection and testing records for quality assurance” is implemented by `QUALITY_CONTROL`, and that table includes `batch_id` specifically to associate QC records with production batches.

To determine which inspections were performed on a specific batch, filter `QUALITY_CONTROL` by the target `batch_id`. The relevant inspection detail…

**Sources retrieved (12):** `inspection and testing records for quality assurance→QUALITY_CONTROL`, `parent_chunk_data_dictionary.md_7`, `Batches for traceability and inventory management→BATCH`, `BATCH→PRODUCT`, `parent_chunk_data_dictionary.md_5`, `parent_chunk_data_dictionary.md_6`, `parent_chunk_data_dictionary.md_3`, `BATCH→WAREHOUSE`

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
> To track which work orders are in progress at a specific warehouse, use the `WORK_ORDER` table and filter on its `warehouse_id` and `status` columns.

From the retrieved context, `WORK_ORDER` represents production jobs and includes:
`work_order_id`, `product_id`, `parent_work_order`, `quantity_ordered`, `quantity_completed`, `status`, `priority`, `planned_start_date`, `planned_end_date`, and `ware…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_5`, `parent_chunk_data_dictionary.md_6`, `WORK_ORDER→WAREHOUSE`, `Work Order→WORK_ORDER`, `Actual stock levels of components and products stored in specific warehouses→WAREHOUSE`, `parent_chunk_data_dictionary.md_8`, `Shipment→SHIPMENT`, `parent_chunk_business_glossary.md_1`

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
> Based on the retrieved context, the relevant schema is the INVENTORY table. It tracks stock for both components and products at specific warehouses and includes the fields inventory_id, warehouse_id, component_id, product_id, quantity_on_hand, quantity_reserved, reorder_threshold, and last_restock_date. The context also states that inventory records support either components or products, but not b…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_5`, `Batches for traceability and inventory management→INVENTORY`, `Actual stock levels of components and products stored in specific warehouses→WAREHOUSE`, `INVENTORY→COMPONENT`, `parent_chunk_data_dictionary.md_3`, `parent_chunk_data_dictionary.md_7`, `parent_chunk_data_dictionary.md_4`, `a parent product, a component product (which can be either a component or sub-assembly), the required quantity, unit of measure, and hierarchical level in the product structure→COMPONENT`

**Context previews (first 3):**

1. _## warehouse  Stores physical storage location information for inventory management.  | Column | Data Type | Constraints | Description | |--------|-----------|-------------|-------------| | warehouse_…_

2. _Business concept 'Batches for traceability and inventory management' is implemented by physical table INVENTORY (columns: inventory_id, warehouse_id, component_id, product_id, quantity_on_hand, quanti…_

3. _Business concept 'Actual stock levels of components and products stored in specific warehouses' is implemented by physical table WAREHOUSE (columns: warehouse_id, warehouse_name, address, city, state,…_

---

### ✅ QA-018 — How do I determine the manufacturing route for a specific product?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.8652 | **Gate:** `proceed`

**Expected answer:**
> Query the route table filtering by product_id, ordered by sequence_number ascending. For each operation, retrieve operation_name, work_center, cycle_time_minutes, and setup_time_minutes. Join with the product table to get product details. The sequence of operations shows the complete manufacturing w…

**System answer:**
> To determine the manufacturing route for a specific product, use the ROUTE table, which is the table for manufacturing workflow steps. The route is product-specific through the foreign key ROUTE.PRODUCT_ID → PRODUCT.PRODUCT_ID.

If you already know the product_id, look up rows in ROUTE where ROUTE.product_id equals that product_id. The route details are stored in these ROUTE columns: route_id, rou…

**Sources retrieved (12):** `Route→ROUTE`, `parent_chunk_data_dictionary.md_6`, `ROUTE→PRODUCT`, `parent_chunk_data_dictionary.md_3`, `Work Order→WORK_ORDER`, `parent_chunk_data_dictionary.md_7`, `parent_chunk_data_dictionary.md_8`, `Route`

**Context previews (first 3):**

1. _Business concept 'Route' — The table is explicitly labeled as a ROUTE table for manufacturing workflow steps, and its columns capture operation sequence, work center, cycle time, and setup time for a …_

2. _## work_order  Represents production jobs for manufacturing products with hierarchical work order support.  | Column | Data Type | Constraints | Description | |--------|-----------|-------------|-----…_

3. _Relationship: ROUTE references PRODUCT via foreign key PRODUCT_ID -> PRODUCT.PRODUCT_ID.…_

---

### ✅ QA-019 — How can I find which batches are stored at a specific warehouse and their QC status?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.7533 | **Gate:** `proceed`

**Expected answer:**
> Query the batch table filtering by warehouse_id. Join with the product table to get product names and types. Include production_date, quantity_produced, expiry_date, and qc_status (PENDING, PASSED, FAILED, QUARANTINED). Filter by qc_status to isolate batches requiring quality attention or ready for …

**System answer:**
> Use the `BATCH` table. It directly stores both the warehouse reference and the batch QC status:

`BATCH.batch_id`, `product_id`, `production_date`, `quantity_produced`, `warehouse_id`, `expiry_date`, `qc_status`.

To find which batches are stored at a specific warehouse, filter `BATCH.warehouse_id` for that warehouse. The foreign key relationship is `BATCH.WAREHOUSE_ID -> WAREHOUSE.WAREHOUSE_ID`, …

**Sources retrieved (12):** `Batches for traceability and inventory management→BATCH`, `parent_chunk_data_dictionary.md_5`, `Actual stock levels of components and products stored in specific warehouses→WAREHOUSE`, `BATCH→WAREHOUSE`, `inspection and testing records for quality assurance→QUALITY_CONTROL`, `parent_chunk_data_dictionary.md_6`, `Batches for traceability and inventory management→INVENTORY`, `parent_chunk_data_dictionary.md_8`

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
> To identify which specifications apply to specific components, use the `COMPONENT` table’s `specification_id` column and join it to `SPECIFICATION.specification_id`.

From the retrieved context, `COMPONENT` includes these relevant columns: `component_id`, `component_name`, `component_category`, `unit_of_measure`, `standard_cost`, and `specification_id`. The `SPECIFICATION` table contains `specific…

**Sources retrieved (12):** `a parent product, a component product (which can be either a component or sub-assembly), the required quantity, unit of measure, and hierarchical level in the product structure→COMPONENT`, `parent_chunk_data_dictionary.md_5`, `parent_chunk_data_dictionary.md_7`, `parent_chunk_data_dictionary.md_3`, `Actual stock levels of components and products stored in specific warehouses→WAREHOUSE`, `Component-Supplier Link→COMPONENT_SUPPLIER`, `parent_chunk_data_dictionary.md_4`, `parent_chunk_business_glossary.md_0`

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
> To perform a complete BOM explosion for a finished product, use the `bom` table as the recursive structure and the `product` table to identify and label the products involved.

Start with the finished product in `product`, using `product.product_id` as the root item. If you specifically want finished goods, the `product` table defines `product_type`, and one of its documented values is `FINISHED_G…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_4`, `parent_chunk_data_dictionary.md_3`, `The Bill of Materials (BOM)→BOM`, `BOM→PRODUCT`, `a parent product, a component product (which can be either a component or sub-assembly), the required quantity, unit of measure, and hierarchical level in the product structure→COMPONENT`, `a parent product, a component product (which can be either a component or sub-assembly), the required quantity, unit of measure, and hierarchical level in the product structure→PRODUCT`, `parent_chunk_data_dictionary.md_5`, `parent_chunk_data_dictionary.md_7`

**Context previews (first 3):**

1. _## bom  Bill of Materials defining product composition and hierarchical structure. Supports recursive relationships for multi-level assemblies.  | Column | Data Type | Constraints | Description | |---…_

2. _# Manufacturing Data Dictionary  This data dictionary documents the database schema for the manufacturing supply chain system. It includes all tables, columns, data types, constraints, and relationshi…_

3. _Business concept 'The Bill of Materials (BOM)' is implemented by physical table BOM (columns: bom_id, parent_product_id, component_product_id, quantity, unit_of_measure, bom_level, is_optional).…_

---

### ✅ QA-022 — How do I calculate the total material cost for a product including all sub-assemblies?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.2332 | **Gate:** `proceed`

**Expected answer:**
> Perform a recursive BOM explosion to find all leaf-level components. For each leaf component, join with the component table to get standard_cost. Multiply standard_cost by the accumulated quantity from the BOM traversal. Sum all component costs to get total material cost. This calculation must trave…

**System answer:**
> Use the `bom` table to explode the product structure recursively, and join each BOM row to the component’s record in `product` to get cost.

From the context, the relevant schema is:

- `bom.parent_product_id` → the product being built
- `bom.component_product_id` → the product that goes into it
- `bom.quantity` → required quantity of that component
- `bom.bom_level` → hierarchy depth
- `product.p…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_3`, `a parent product, a component product (which can be either a component or sub-assembly), the required quantity, unit of measure, and hierarchical level in the product structure→COMPONENT`, `a parent product, a component product (which can be either a component or sub-assembly), the required quantity, unit of measure, and hierarchical level in the product structure→PRODUCT`, `parent_chunk_data_dictionary.md_4`, `parent_chunk_data_dictionary.md_7`, `parent_chunk_data_dictionary.md_8`, `The Bill of Materials (BOM)→BOM`, `parent_chunk_data_dictionary.md_6`

**Context previews (first 3):**

1. _# Manufacturing Data Dictionary  This data dictionary documents the database schema for the manufacturing supply chain system. It includes all tables, columns, data types, constraints, and relationshi…_

2. _Business concept 'a parent product, a component product (which can be either a component or sub-assembly), the required quantity, unit of measure, and hierarchical level in the product structure' is i…_

3. _Business concept 'a parent product, a component product (which can be either a component or sub-assembly), the required quantity, unit of measure, and hierarchical level in the product structure' is i…_

---

### ✅ QA-023 — How can I find all parent products that contain a specific component anywhere in their BOM structure?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.5213 | **Gate:** `proceed`

**Expected answer:**
> Use a recursive reverse traversal of the BOM. Start with the component_id as the initial parent_product_id. Find all records where this product appears as component_product_id in the bom table. For each parent_product_id found, check if it appears as a component_product_id in other bom records (is a…

**System answer:**
> Use the `bom` table as the primary traversal structure, because it is explicitly defined to support recursive, multi-level assemblies. The key columns are `bom.component_product_id` and `bom.parent_product_id`, and both reference `product.product_id`.

To find all parent products that contain a specific component anywhere in the BOM, start with BOM rows where `component_product_id` equals the targ…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_4`, `parent_chunk_data_dictionary.md_3`, `The Bill of Materials (BOM)→BOM`, `a parent product, a component product (which can be either a component or sub-assembly), the required quantity, unit of measure, and hierarchical level in the product structure→COMPONENT`, `a parent product, a component product (which can be either a component or sub-assembly), the required quantity, unit of measure, and hierarchical level in the product structure→PRODUCT`, `BOM→PRODUCT`, `PRODUCT→PRODUCT`, `parent_chunk_data_dictionary.md_6`

**Context previews (first 3):**

1. _## bom  Bill of Materials defining product composition and hierarchical structure. Supports recursive relationships for multi-level assemblies.  | Column | Data Type | Constraints | Description | |---…_

2. _# Manufacturing Data Dictionary  This data dictionary documents the database schema for the manufacturing supply chain system. It includes all tables, columns, data types, constraints, and relationshi…_

3. _Business concept 'The Bill of Materials (BOM)' is implemented by physical table BOM (columns: bom_id, parent_product_id, component_product_id, quantity, unit_of_measure, bom_level, is_optional).…_

---

### ✅ QA-024 — How do I identify work orders that require a specific component, considering nested sub-assemblies?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.3651 | **Gate:** `proceed`

**Expected answer:**
> First, perform reverse BOM traversal to find all parent products that contain the target component at any level. Then query the work_order table where product_id is in the set of parent products found. This includes work orders for finished goods that contain the component indirectly through sub-ass…

**System answer:**
> Use the `WORK_ORDER` product and the recursive `BOM` structure.

At the schema level, the path is `WORK_ORDER.product_id -> PRODUCT.product_id -> BOM.parent_product_id`, then recursively follow `BOM.component_product_id` through additional `BOM.parent_product_id` rows until you reach all nested sub-assemblies and leaf components. A work order requires the specific component if the BOM explosion fo…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_6`, `parent_chunk_data_dictionary.md_5`, `a parent product, a component product (which can be either a component or sub-assembly), the required quantity, unit of measure, and hierarchical level in the product structure→COMPONENT`, `parent_chunk_data_dictionary.md_3`, `parent_chunk_data_dictionary.md_4`, `Work Order→WORK_ORDER`, `a parent product, a component product (which can be either a component or sub-assembly), the required quantity, unit of measure, and hierarchical level in the product structure→PRODUCT`, `WORK_ORDER→WORK_ORDER`

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
> Use the `bom` table. It already contains a `bom_level` column, described as the “depth in product hierarchy,” and the schema notes that `bom_level` is used to track hierarchy depth for performance optimization.

At the schema level:

If you want the maximum BOM depth in the whole system, take the maximum value of `bom.bom_level`.

If you want the maximum BOM depth for a specific product, use `bom.…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_4`, `parent_chunk_data_dictionary.md_3`, `The Bill of Materials (BOM)→BOM`, `BOM→PRODUCT`, `parent_chunk_data_dictionary.md_7`, `parent_chunk_data_dictionary.md_5`, `parent_chunk_data_dictionary.md_6`, `a parent product, a component product (which can be either a component or sub-assembly), the required quantity, unit of measure, and hierarchical level in the product structure→COMPONENT`

**Context previews (first 3):**

1. _## bom  Bill of Materials defining product composition and hierarchical structure. Supports recursive relationships for multi-level assemblies.  | Column | Data Type | Constraints | Description | |---…_

2. _# Manufacturing Data Dictionary  This data dictionary documents the database schema for the manufacturing supply chain system. It includes all tables, columns, data types, constraints, and relationshi…_

3. _Business concept 'The Bill of Materials (BOM)' is implemented by physical table BOM (columns: bom_id, parent_product_id, component_product_id, quantity, unit_of_measure, bom_level, is_optional).…_

---

### ✅ QA-026 — How do I find all products that have a specific product as a sub-assembly at any level?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.2948 | **Gate:** `proceed`

**Expected answer:**
> Perform a recursive search starting with the target product_id as the initial component_product_id in the bom table. For each parent_product_id found, check if that parent appears as a component in other bom entries. Continue recursively until reaching products that are not used as components elsewh…

**System answer:**
> Use the BOM hierarchy, because `bom` is the table that explicitly stores “a parent product, a component product … the required quantity, unit of measure, and hierarchical level in the product structure.”

To find all products that contain a specific product as a sub-assembly at any level, start with `bom.component_product_id = <target product_id>`. Those rows give the immediate parents in `bom.par…

**Sources retrieved (12):** `a parent product, a component product (which can be either a component or sub-assembly), the required quantity, unit of measure, and hierarchical level in the product structure→COMPONENT`, `a parent product, a component product (which can be either a component or sub-assembly), the required quantity, unit of measure, and hierarchical level in the product structure→PRODUCT`, `parent_chunk_data_dictionary.md_3`, `parent_chunk_data_dictionary.md_4`, `parent_chunk_data_dictionary.md_5`, `parent_chunk_data_dictionary.md_7`, `Actual stock levels of components and products stored in specific warehouses→WAREHOUSE`, `The Bill of Materials (BOM)→BOM`

**Context previews (first 3):**

1. _Business concept 'a parent product, a component product (which can be either a component or sub-assembly), the required quantity, unit of measure, and hierarchical level in the product structure' is i…_

2. _Business concept 'a parent product, a component product (which can be either a component or sub-assembly), the required quantity, unit of measure, and hierarchical level in the product structure' is i…_

3. _# Manufacturing Data Dictionary  This data dictionary documents the database schema for the manufacturing supply chain system. It includes all tables, columns, data types, constraints, and relationshi…_

---

### ✅ QA-027 — How can I calculate the total lead time for a product including all sub-assembly lead times?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.3462 | **Gate:** `proceed`

**Expected answer:**
> Perform a recursive BOM explosion to find all components and sub-assemblies. For each product_id in the hierarchy, retrieve lead_time_days from the product table. The total lead time is the maximum of all lead times in the hierarchy (representing the longest dependency chain), or optionally sum lead…

**System answer:**
> From the retrieved context, the schema supports tracing all sub-assemblies needed for a product, but it does not define a single business rule for how “total lead time” must be aggregated.

What the context does provide is the join path and the relevant columns. The target product is in `product`, where `product.product_id` identifies the item and `product.lead_time_days` stores its procurement or…

**Sources retrieved (12):** `a parent product, a component product (which can be either a component or sub-assembly), the required quantity, unit of measure, and hierarchical level in the product structure→PRODUCT`, `parent_chunk_data_dictionary.md_3`, `Component-Supplier Link→COMPONENT_SUPPLIER`, `a parent product, a component product (which can be either a component or sub-assembly), the required quantity, unit of measure, and hierarchical level in the product structure→COMPONENT`, `parent_chunk_data_dictionary.md_4`, `parent_chunk_data_dictionary.md_7`, `parent_chunk_data_dictionary.md_6`, `Route→ROUTE`

**Context previews (first 3):**

1. _Business concept 'a parent product, a component product (which can be either a component or sub-assembly), the required quantity, unit of measure, and hierarchical level in the product structure' is i…_

2. _# Manufacturing Data Dictionary  This data dictionary documents the database schema for the manufacturing supply chain system. It includes all tables, columns, data types, constraints, and relationshi…_

3. _Business concept 'Component-Supplier Link' — The table is explicitly described as a many-to-many relationship linking components to approved suppliers, and its columns carry supplier-specific pricing,…_

---

### ✅ QA-028 — How do I generate a complete indented BOM report showing the hierarchical structure?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.4180 | **Gate:** `proceed`

**Expected answer:**
> Use a recursive query on the bom table that tracks the current depth level. Start with the top-level product (parent_product_id where product has no parent_product_id). At each level, output component details indented by depth level. Include product_name, quantity, and unit_of_measure. Recursively p…

**System answer:**
> To generate a complete indented BOM report, use the `bom` table as the primary hierarchy source and join it to `product` twice.

The relevant structure is:

`bom.parent_product_id` → `product.product_id` to identify the assembly being built, and  
`bom.component_product_id` → `product.product_id` to identify the component or sub-assembly used inside it.

The `bom` table is specifically designed fo…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_4`, `parent_chunk_data_dictionary.md_3`, `a parent product, a component product (which can be either a component or sub-assembly), the required quantity, unit of measure, and hierarchical level in the product structure→COMPONENT`, `a parent product, a component product (which can be either a component or sub-assembly), the required quantity, unit of measure, and hierarchical level in the product structure→PRODUCT`, `parent_chunk_data_dictionary.md_6`, `parent_chunk_data_dictionary.md_8`, `The Bill of Materials (BOM)→BOM`, `parent_chunk_business_glossary.md_0`

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
> Use the BOM table as the primary source, because it defines product composition with `parent_product_id` for the product being built and `component_product_id` for what goes into it.

To find which components appear most frequently across all BOMs, aggregate `BOM.component_product_id` and count how many BOM rows reference each one. The basic path is `BOM.component_product_id -> PRODUCT.product_id`…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_4`, `parent_chunk_data_dictionary.md_3`, `The Bill of Materials (BOM)→BOM`, `BOM→PRODUCT`, `parent_chunk_data_dictionary.md_5`, `a parent product, a component product (which can be either a component or sub-assembly), the required quantity, unit of measure, and hierarchical level in the product structure→PRODUCT`, `a parent product, a component product (which can be either a component or sub-assembly), the required quantity, unit of measure, and hierarchical level in the product structure→COMPONENT`, `Actual stock levels of components and products stored in specific warehouses→WAREHOUSE`

**Context previews (first 3):**

1. _## bom  Bill of Materials defining product composition and hierarchical structure. Supports recursive relationships for multi-level assemblies.  | Column | Data Type | Constraints | Description | |---…_

2. _# Manufacturing Data Dictionary  This data dictionary documents the database schema for the manufacturing supply chain system. It includes all tables, columns, data types, constraints, and relationshi…_

3. _Business concept 'The Bill of Materials (BOM)' is implemented by physical table BOM (columns: bom_id, parent_product_id, component_product_id, quantity, unit_of_measure, bom_level, is_optional).…_

---

### ✅ QA-030 — How do I detect circular references in the BOM structure to prevent infinite loops?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.1295 | **Gate:** `proceed_with_warning`

**Expected answer:**
> Use a recursive query with a cycle detection check. Track the path of visited product_ids at each recursion level. If a product_id appears twice in the same path, a circular reference exists. Alternatively, check if any bom record has parent_product_id = component_product_id (direct self-reference),…

**System answer:**
> The retrieved context does not describe any explicit circular-reference detection rule or algorithm for the `bom` table, so I cannot tell you a supported method for detecting loops from this knowledge graph alone.

What the schema does show is:

The `bom` table is recursive because both `parent_product_id` and `component_product_id` are foreign keys to `product(product_id)`. That means BOM structu…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_4`, `parent_chunk_data_dictionary.md_3`, `BOM→PRODUCT`, `The Bill of Materials (BOM)→BOM`, `parent_chunk_data_dictionary.md_8`, `parent_chunk_data_dictionary.md_7`, `parent_chunk_data_dictionary.md_6`, `parent_chunk_business_glossary.md_0`

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
> From the retrieved context, you can determine the product structure completely, but the supplier chain is only partially derivable.

To get all sub-assemblies and lower-level parts for a finished product, start in `product` with the finished item, using `product.product_id` and `product_type = 'FINISHED_GOOD'`. Then traverse `bom` recursively, joining `bom.parent_product_id` to `product.product_id…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_3`, `a parent product, a component product (which can be either a component or sub-assembly), the required quantity, unit of measure, and hierarchical level in the product structure→PRODUCT`, `a parent product, a component product (which can be either a component or sub-assembly), the required quantity, unit of measure, and hierarchical level in the product structure→COMPONENT`, `parent_chunk_data_dictionary.md_4`, `parent_chunk_data_dictionary.md_8`, `parent_chunk_data_dictionary.md_6`, `Component-Supplier Link→COMPONENT_SUPPLIER`, `parent_chunk_data_dictionary.md_7`

**Context previews (first 3):**

1. _# Manufacturing Data Dictionary  This data dictionary documents the database schema for the manufacturing supply chain system. It includes all tables, columns, data types, constraints, and relationshi…_

2. _Business concept 'a parent product, a component product (which can be either a component or sub-assembly), the required quantity, unit of measure, and hierarchical level in the product structure' is i…_

3. _Business concept 'a parent product, a component product (which can be either a component or sub-assembly), the required quantity, unit of measure, and hierarchical level in the product structure' is i…_

---

### ✅ QA-032 — How do I check if sufficient inventory exists across all warehouses to fulfill a work order?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.4035 | **Gate:** `proceed`

**Expected answer:**
> For the work_order's product_id, perform recursive BOM explosion to get all required components with quantities. For each component, sum the available quantity (quantity_on_hand - quantity_reserved) across all warehouses from the inventory table. Compare aggregated available inventory against requir…

**System answer:**
> To check this from the available schema, use the `work_order` and `inventory` tables.

A `work_order` tells you what product is being manufactured and in what quantity through `work_order.product_id`, `quantity_ordered`, and `quantity_completed` [2]. The `inventory` table stores stock for either a `product_id` or a `component_id` at a specific `warehouse_id`, and the schema excerpt explicitly show…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_5`, `parent_chunk_data_dictionary.md_6`, `INVENTORY→WAREHOUSE`, `Actual stock levels of components and products stored in specific warehouses→WAREHOUSE`, `Work Order→WORK_ORDER`, `WORK_ORDER→WAREHOUSE`, `Batches for traceability and inventory management→INVENTORY`, `parent_chunk_data_dictionary.md_8`

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
> From the retrieved context, you can identify failed quality inspections in `QUALITY_CONTROL`, but you cannot fully trace them to components from specific suppliers because the required linking path is not provided.

The part that is supported is this: `QUALITY_CONTROL` stores QC inspections with columns `qc_id`, `batch_id`, `specification_id`, `qc_date`, `qc_type`, `inspector_id`, `result`, `defec…

**Sources retrieved (12):** `Component-Supplier Link→COMPONENT_SUPPLIER`, `parent_chunk_data_dictionary.md_5`, `parent_chunk_data_dictionary.md_3`, `inspection and testing records for quality assurance→QUALITY_CONTROL`, `parent_chunk_data_dictionary.md_4`, `Actual stock levels of components and products stored in specific warehouses→WAREHOUSE`, `COMPONENT_SUPPLIER→SUPPLIER`, `parent_chunk_data_dictionary.md_8`

**Context previews (first 3):**

1. _Business concept 'Component-Supplier Link' — The table is explicitly described as a many-to-many relationship linking components to approved suppliers, and its columns carry supplier-specific pricing,…_

2. _## warehouse  Stores physical storage location information for inventory management.  | Column | Data Type | Constraints | Description | |--------|-----------|-------------|-------------| | warehouse_…_

3. _# Manufacturing Data Dictionary  This data dictionary documents the database schema for the manufacturing supply chain system. It includes all tables, columns, data types, constraints, and relationshi…_

---

### ✅ QA-034 — How do I calculate the total manufacturing time for a work order including all sub-assembly work orders?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.1599 | **Gate:** `proceed_with_warning`

**Expected answer:**
> Query the work_order table starting with the parent work_order. Find all child work_orders where parent_work_order matches the current work_order_id. For each work order (parent and children), join with the route table on product_id to get all operations. Sum (cycle_time_minutes * quantity) plus set…

**System answer:**
> From the retrieved context, the schema-level way to calculate total manufacturing time for a work order and all of its sub-assembly work orders is to combine the hierarchical structure in WORK_ORDER with the product-specific operation times in ROUTE.

WORK_ORDER supports hierarchy through the self-referential column parent_work_order → work_order.work_order_id. That means a large production job ca…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_6`, `Work Order→WORK_ORDER`, `parent_chunk_data_dictionary.md_3`, `Route→ROUTE`, `a parent product, a component product (which can be either a component or sub-assembly), the required quantity, unit of measure, and hierarchical level in the product structure→PRODUCT`, `a parent product, a component product (which can be either a component or sub-assembly), the required quantity, unit of measure, and hierarchical level in the product structure→COMPONENT`, `parent_chunk_data_dictionary.md_7`, `parent_chunk_business_glossary.md_0`

**Context previews (first 3):**

1. _## work_order  Represents production jobs for manufacturing products with hierarchical work order support.  | Column | Data Type | Constraints | Description | |--------|-----------|-------------|-----…_

2. _Business concept 'Work Order' — The table name, primary key, and columns like product_id, parent_work_order, quantity_ordered, quantity_completed, status, priority, and planned dates align directly wi…_

3. _# Manufacturing Data Dictionary  This data dictionary documents the database schema for the manufacturing supply chain system. It includes all tables, columns, data types, constraints, and relationshi…_

---

### ✅ QA-035 — How can I identify which shipments are overdue and their impact on work orders?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0719 | **Gate:** `proceed_with_warning`

**Expected answer:**
> Query the shipment table filtering for status = 'SHIPPED' where actual_arrival is NULL and estimated_arrival is in the past (overdue). Join with the component_supplier table via supplier_id and component_id to identify which components are delayed. Perform reverse BOM lookup to find which parent pro…

**System answer:**
> From the retrieved context, you can identify overdue shipments from `SHIPMENT` and assess only a warehouse-level potential impact on `WORK_ORDER`.

A shipment is in `SHIPMENT` and has these relevant fields: `shipment_id`, `shipment_type`, `warehouse_id`, `ship_date`, `estimated_arrival`, `actual_arrival`, and `status`. The available shipment statuses are `PENDING`, `SHIPPED`, `DELIVERED`, and `CAN…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_5`, `parent_chunk_data_dictionary.md_8`, `parent_chunk_data_dictionary.md_6`, `Shipment`, `Work Order→WORK_ORDER`, `Shipment→SHIPMENT`, `WORK_ORDER→PRODUCT`, `WORK_ORDER→WAREHOUSE`

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
> From the retrieved context, you can only answer this partially.

What is known is that batch expiry is tracked in the `BATCH` table. The available batch fields include `batch_id`, `product_id`, `production_date`, `quantity_produced`, `warehouse_id`, and `expiry_date`, with `warehouse_id` linking to `WAREHOUSE(warehouse_id)`. So, at the schema level, batches that are past expiry or approaching expi…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_5`, `Component-Supplier Link→COMPONENT_SUPPLIER`, `Actual stock levels of components and products stored in specific warehouses→WAREHOUSE`, `Batches for traceability and inventory management→BATCH`, `parent_chunk_data_dictionary.md_7`, `Batches for traceability and inventory management→INVENTORY`, `parent_chunk_data_dictionary.md_3`, `parent_chunk_business_glossary.md_2`

**Context previews (first 3):**

1. _## warehouse  Stores physical storage location information for inventory management.  | Column | Data Type | Constraints | Description | |--------|-----------|-------------|-------------| | warehouse_…_

2. _Business concept 'Component-Supplier Link' — The table is explicitly described as a many-to-many relationship linking components to approved suppliers, and its columns carry supplier-specific pricing,…_

3. _Business concept 'Actual stock levels of components and products stored in specific warehouses' is implemented by physical table WAREHOUSE (columns: warehouse_id, warehouse_name, address, city, state,…_

---

### ✅ QA-037 — How can I generate a material requirements plan showing when to order components based on work order schedules?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0433 | **Gate:** `proceed_with_warning`

**Expected answer:**
> Query all work_orders with status 'PENDING' ordered by planned_start_date. For each work_order, perform BOM explosion to get required components and quantities. For each component, query inventory for current available stock across warehouses. Calculate net requirements = (required quantity * work_o…

**System answer:**
> From the retrieved context, I can only give a partial, schema-level approach. The knowledge graph does not contain a documented MRP procedure or enough business rules to determine an exact “when to order” calculation.

What is supported by the context is this:

The demand side comes from `WORK_ORDER`. It gives the product being built (`product_id`), the scheduled timing (`planned_start_date`, `pla…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_6`, `parent_chunk_data_dictionary.md_7`, `parent_chunk_data_dictionary.md_5`, `Work Order→WORK_ORDER`, `parent_chunk_data_dictionary.md_4`, `parent_chunk_data_dictionary.md_3`, `Component-Supplier Link→COMPONENT_SUPPLIER`, `The Bill of Materials (BOM)→BOM`

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
> The retrieved context does not contain enough information to trace a complete component genealogy from supplier through batch to finished goods end to end. What can be determined is the partial schema path, and what cannot be determined is the specific transactional linkage between those stages.

From the context, the supplier-to-component relationship is represented by `COMPONENT_SUPPLIER`, which…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_3`, `parent_chunk_data_dictionary.md_7`, `parent_chunk_data_dictionary.md_5`, `parent_chunk_data_dictionary.md_8`, `Batches for traceability and inventory management→INVENTORY`, `parent_chunk_data_dictionary.md_4`, `Component-Supplier Link→COMPONENT_SUPPLIER`, `Batches for traceability and inventory management→BATCH`

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
> Use the `bom` table to identify components that are used by more than one product, and use `COMPONENT_SUPPLIER` plus `supplier` to see the approved alternatives for those components.

At the product-structure level, `bom.parent_product_id` is the product being built and `bom.component_product_id` is the component or sub-assembly used in it. Because `bom` supports recursive relationships and multi-…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_4`, `Component-Supplier Link→COMPONENT_SUPPLIER`, `parent_chunk_data_dictionary.md_3`, `parent_chunk_data_dictionary.md_5`, `parent_chunk_data_dictionary.md_8`, `parent_chunk_data_dictionary.md_7`, `COMPONENT_SUPPLIER→COMPONENT`, `a parent product, a component product (which can be either a component or sub-assembly), the required quantity, unit of measure, and hierarchical level in the product structure→COMPONENT`

**Context previews (first 3):**

1. _## bom  Bill of Materials defining product composition and hierarchical structure. Supports recursive relationships for multi-level assemblies.  | Column | Data Type | Constraints | Description | |---…_

2. _Business concept 'Component-Supplier Link' — The table is explicitly described as a many-to-many relationship linking components to approved suppliers, and its columns carry supplier-specific pricing,…_

3. _# Manufacturing Data Dictionary  This data dictionary documents the database schema for the manufacturing supply chain system. It includes all tables, columns, data types, constraints, and relationshi…_

---

### ✅ QA-040 — How do I calculate the total landed cost for a product including component costs, supplier lead times, and manufacturing operations?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.1922 | **Gate:** `proceed_with_warning`

**Expected answer:**
> Perform recursive BOM explosion to get all leaf components. For each component, query component_supplier to get unit_price from primary supplier. Multiply by accumulated BOM quantity for material cost. Add shipping costs (estimated from shipment history). Query route table for the product to get all…

**System answer:**
> From the retrieved context, you can only define this at the schema level, not produce a complete numeric landed-cost formula.

The available join path is: start with `PRODUCT` for the target `product_id`; use `PRODUCT.parent_product_id` to traverse the hierarchical product structure because the `product` table explicitly supports multi-level assemblies and BOM-style nesting; use `ROUTE.product_id …

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_3`, `a parent product, a component product (which can be either a component or sub-assembly), the required quantity, unit of measure, and hierarchical level in the product structure→PRODUCT`, `Component-Supplier Link→COMPONENT_SUPPLIER`, `Route→ROUTE`, `a parent product, a component product (which can be either a component or sub-assembly), the required quantity, unit of measure, and hierarchical level in the product structure→COMPONENT`, `parent_chunk_data_dictionary.md_6`, `parent_chunk_data_dictionary.md_7`, `parent_chunk_data_dictionary.md_5`

**Context previews (first 3):**

1. _# Manufacturing Data Dictionary  This data dictionary documents the database schema for the manufacturing supply chain system. It includes all tables, columns, data types, constraints, and relationshi…_

2. _Business concept 'a parent product, a component product (which can be either a component or sub-assembly), the required quantity, unit of measure, and hierarchical level in the product structure' is i…_

3. _Business concept 'Component-Supplier Link' — The table is explicitly described as a many-to-many relationship linking components to approved suppliers, and its columns carry supplier-specific pricing,…_

---

## Anomalies & Observations

No anomalies detected. All questions grounded with acceptable RAGAS scores.
