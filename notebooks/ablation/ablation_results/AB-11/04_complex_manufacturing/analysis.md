# AB-11 — 04_complex_manufacturing — Run Analysis

**Timestamp:** 2026-04-01 01:15:10  
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
| ER similarity threshold | `0.65` |

## Builder Results

| Metric | Value |
|--------|-------|
| Triplets extracted | 445 |
| Entities resolved | 16 |
| Tables parsed | 13 |
| Tables completed | 13 |

## Query Evaluation Summary

| Metric | Value |
|--------|-------|
| Questions | 40 |
| Grounded | **40/40 (100%)** |
| Avg GT Coverage | 100% |
| Avg Top Score | 0.4353 |
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
> In the manufacturing system, the `product` table stores core master data about manufactured items. A product can represent a `FINISHED_GOOD`, `ASSEMBLY`, or `COMPONENT`, and the system explicitly says products include finished goods ready for sale, sub-assemblies used in production, and individual components.

The physical `product` table stores these attributes: `product_id` as the unique product…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_3`, `parent_chunk_data_dictionary.md_6`, `Manufacturing Work Order→WORK_ORDER`, `Manufacturing Work Order`, `Inventory→INVENTORY`, `parent_chunk_data_dictionary.md_5`, `parent_chunk_data_dictionary.md_7`, `parent_chunk_business_glossary.md_0`

**Context previews (first 3):**

1. _# Manufacturing Data Dictionary  This data dictionary documents the database schema for the manufacturing supply chain system. It includes all tables, columns, data types, constraints, and relationshi…_

2. _## work_order  Represents production jobs for manufacturing products with hierarchical work order support.  | Column | Data Type | Constraints | Description | |--------|-----------|-------------|-----…_

3. _Business concept 'Manufacturing Work Order' — The table is explicitly labeled as production jobs and includes product reference, parent work order hierarchy, planned dates, quantities ordered/complete…_

---

### ✅ QA-002 — How are components defined in the manufacturing database?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.5910 | **Gate:** `proceed`

**Expected answer:**
> Components are defined with a unique identifier (component_id), descriptive name (component_name), category grouping (component_category), unit of measure (unit_of_measure), standard unit cost (standard_cost), and optional reference to technical specifications (specification_id). Components represen…

**System answer:**
> In the business glossary, a Component is defined as an atomic raw material or purchased part that cannot be further broken down into simpler manufactured items. Components are the building blocks used in manufacturing and are procured from external suppliers.

In the physical schema, that business concept is implemented by the COMPONENT table, with these columns: component_id, component_name, comp…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_3`, `a parent product, a component product (which can be either a component or sub-assembly), the required quantity, unit of measure, and hierarchical level in the product structure→COMPONENT`, `parent_chunk_data_dictionary.md_4`, `The Bill of Materials (BOM)→BOM`, `parent_chunk_data_dictionary.md_5`, `Approved Supplier Relationship→COMPONENT_SUPPLIER`, `Inventory→INVENTORY`, `parent_chunk_business_glossary.md_0`

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
> The Bill of Materials (BOM) table exists to define product composition and hierarchical structure. It records which component products go into a parent product, along with the required quantity, unit of measure, hierarchy depth (`bom_level`), and whether a component is optional.

In schema terms, `BOM` implements the business concept “The Bill of Materials (BOM)” and links products through `parent…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_4`, `The Bill of Materials (BOM)→BOM`, `BOM→PRODUCT`, `Manufacturing Work Order`, `Manufacturing Work Order→WORK_ORDER`, `parent_chunk_data_dictionary.md_3`, `The Bill of Materials (BOM)`, `parent_chunk_business_glossary.md_0`

**Context previews (first 3):**

1. _## bom  Bill of Materials defining product composition and hierarchical structure. Supports recursive relationships for multi-level assemblies.  | Column | Data Type | Constraints | Description | |---…_

2. _Business concept 'The Bill of Materials (BOM)' is implemented by physical table BOM (columns: bom_id, parent_product_id, component_product_id, quantity, unit_of_measure, bom_level, is_optional).…_

3. _Relationship: BOM references PRODUCT via foreign key COMPONENT_PRODUCT_ID -> PRODUCT.PRODUCT_ID.…_

---

### ✅ QA-004 — What supplier information does the system maintain?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.5861 | **Gate:** `proceed`

**Expected answer:**
> Suppliers are tracked with a unique identifier (supplier_id), legal business name (supplier_name), primary contact email (contact_email), primary contact phone number (contact_phone), performance rating from 1.0 to 5.0 (rating), and preferred supplier status flag (is_preferred).

**System answer:**
> The system maintains supplier master data in the SUPPLIER table for external vendors used in procurement operations. Based on the context, the supplier-specific attributes are supplier_id, supplier_name, contact_email, contact_phone, rating, and is_preferred. The business description says suppliers are external vendors assessed by performance and maintained for procurement operations, which aligns…

**Sources retrieved (12):** `Suppliers→SUPPLIER`, `parent_chunk_data_dictionary.md_4`, `SHIPMENT→SUPPLIER`, `parent_chunk_data_dictionary.md_8`, `COMPONENT_SUPPLIER→SUPPLIER`, `Approved Supplier Relationship→COMPONENT_SUPPLIER`, `parent_chunk_data_dictionary.md_3`, `Shipment→SHIPMENT`

**Context previews (first 3):**

1. _Business concept 'Suppliers' — The table is explicitly labeled as the SUPPLIER table and contains supplier-specific attributes such as supplier_id, supplier_name, contact details, rating, and preferre…_

2. _## bom  Bill of Materials defining product composition and hierarchical structure. Supports recursive relationships for multi-level assemblies.  | Column | Data Type | Constraints | Description | |---…_

3. _Relationship: SHIPMENT references SUPPLIER via foreign key SUPPLIER_ID -> SUPPLIER.SUPPLIER_ID.…_

---

### ✅ QA-005 — How are warehouses represented in the schema?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.3381 | **Gate:** `proceed`

**Expected answer:**
> Warehouses are defined with a unique identifier (warehouse_id), descriptive name (warehouse_name), full street address (address), city location (city), state or province (state), total storage capacity in cubic meters (capacity), and optional manager identifier (manager_id).

**System answer:**
> Warehouses are represented by the physical table WAREHOUSE, which implements the business concept of a Warehouse as a physical storage location and supply chain node.

The WAREHOUSE table has primary key warehouse_id and the columns warehouse_name, address, city, state, capacity, and manager_id. From the schema and business description, a warehouse stores location information, has a defined storag…

**Sources retrieved (12):** `INVENTORY→WAREHOUSE`, `BATCH→WAREHOUSE`, `WORK_ORDER→WAREHOUSE`, `SHIPMENT→WAREHOUSE`, `parent_chunk_data_dictionary.md_6`, `Warehouse→WAREHOUSE`, `parent_chunk_data_dictionary.md_5`, `Manufacturing Work Order`

**Context previews (first 3):**

1. _Relationship: INVENTORY references WAREHOUSE via foreign key WAREHOUSE_ID -> WAREHOUSE.WAREHOUSE_ID.…_

2. _Relationship: BATCH references WAREHOUSE via foreign key WAREHOUSE_ID -> WAREHOUSE.WAREHOUSE_ID.…_

3. _Relationship: WORK_ORDER references WAREHOUSE via foreign key WAREHOUSE_ID -> WAREHOUSE.WAREHOUSE_ID.…_

---

### ✅ QA-006 — What does the inventory table track?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.8141 | **Gate:** `proceed`

**Expected answer:**
> The inventory table tracks real-time stock levels including a unique record identifier (inventory_id), warehouse location (warehouse_id), component identifier for materials (component_id) or product identifier for finished goods (product_id), current physical stock quantity (quantity_on_hand), quant…

**System answer:**
> The `INVENTORY` table tracks stock levels for components and products stored at specific warehouse locations. It implements physical inventory records and includes the key measures `quantity_on_hand`, `quantity_reserved`, `reorder_threshold`, and `last_restock_date`. Through its foreign keys, each inventory record is tied to a `WAREHOUSE` and to either a `COMPONENT` or a `PRODUCT` (the context sta…

**Sources retrieved (12):** `Inventory`, `Inventory→INVENTORY`, `INVENTORY→PRODUCT`, `INVENTORY→WAREHOUSE`, `INVENTORY→COMPONENT`, `parent_chunk_data_dictionary.md_5`, `Batches→BATCH`, `Manufacturing Work Order`

**Context previews (first 3):**

1. _Inventory: The table is explicitly labeled as inventory stock levels and contains canonical inventory measures such as quantity_on_hand, quantity_reserved, reorder_threshold, and last_restock_date. It…_

2. _Business concept 'Inventory' — The table is explicitly labeled as inventory stock levels and contains canonical inventory measures such as quantity_on_hand, quantity_reserved, reorder_threshold, and l…_

3. _Relationship: INVENTORY references PRODUCT via foreign key PRODUCT_ID -> PRODUCT.PRODUCT_ID.…_

---

### ✅ QA-007 — How are work orders structured in the manufacturing system?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.8884 | **Gate:** `proceed`

**Expected answer:**
> Work orders represent production jobs with a unique identifier (work_order_id), product to be manufactured (product_id), optional parent work order for nested hierarchies (parent_work_order), quantity to produce (quantity_ordered), quantity completed so far (quantity_completed), current status (PEND…

**System answer:**
> Work orders in this manufacturing system are structured as production jobs, implemented by the `WORK_ORDER` table. They track the product being manufactured, the production hierarchy, planned schedule, quantities, execution status, priority, and production location.

The `WORK_ORDER` table contains `work_order_id` as the primary key and `product_id` as a required foreign key to `PRODUCT.PRODUCT_ID…

**Sources retrieved (12):** `Manufacturing Work Order`, `Manufacturing Work Order→WORK_ORDER`, `parent_chunk_data_dictionary.md_6`, `WORK_ORDER→PRODUCT`, `WORK_ORDER→WORK_ORDER`, `Route Steps→ROUTE`, `parent_chunk_data_dictionary.md_3`, `WORK_ORDER→WAREHOUSE`

**Context previews (first 3):**

1. _Manufacturing Work Order: The table is explicitly labeled as production jobs and includes product reference, parent work order hierarchy, planned dates, quantities ordered/completed, status, and prior…_

2. _Business concept 'Manufacturing Work Order' — The table is explicitly labeled as production jobs and includes product reference, parent work order hierarchy, planned dates, quantities ordered/complete…_

3. _## work_order  Represents production jobs for manufacturing products with hierarchical work order support.  | Column | Data Type | Constraints | Description | |--------|-----------|-------------|-----…_

---

### ✅ QA-008 — What information is captured in the shipment table?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.9085 | **Gate:** `proceed`

**Expected answer:**
> Shipments track material transfers with a unique identifier (shipment_id), shipment type (INBOUND from suppliers, OUTBOUND to customers, INTERNAL between warehouses), destination warehouse (warehouse_id), source supplier for inbound (supplier_id), destination customer for outbound (customer_id), shi…

**System answer:**
> The `SHIPMENT` table captures material transfer records between warehouses, suppliers, and customers. It implements the business concept `Shipment` and stores:

`shipment_id` as the unique shipment identifier and primary key; `shipment_type` as the shipment category with values `INBOUND`, `OUTBOUND`, or `INTERNAL`; `warehouse_id` as the warehouse reference; `supplier_id` as the supplier reference,…

**Sources retrieved (12):** `Shipment→SHIPMENT`, `Shipment`, `SHIPMENT→WAREHOUSE`, `SHIPMENT→SUPPLIER`, `parent_chunk_data_dictionary.md_8`, `parent_chunk_data_dictionary.md_5`, `parent_chunk_business_glossary.md_0`, `Inventory`

**Context previews (first 3):**

1. _Business concept 'Shipment' — The table name, primary key, and date/status fields align directly with the shipment concept, and the foreign keys to warehouse, supplier, and customer match the inbound/…_

2. _Shipment: The table name, primary key, and date/status fields align directly with the shipment concept, and the foreign keys to warehouse, supplier, and customer match the inbound/outbound material tr…_

3. _Relationship: SHIPMENT references WAREHOUSE via foreign key WAREHOUSE_ID -> WAREHOUSE.WAREHOUSE_ID.…_

---

### ✅ QA-009 — How does the quality control system record inspections?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.9540 | **Gate:** `proceed`

**Expected answer:**
> Quality control records are stored with a unique identifier (qc_id), associated production batch (batch_id), applicable specification requirements (specification_id), inspection date (qc_date), inspection type (INCOMING for supplier materials, IN_PROCESS during manufacturing, FINAL for finished good…

**System answer:**
> The quality control system records inspections in the physical table `QUALITY_CONTROL`, which implements the business concept `Quality Control`.

Each inspection is stored as a QC record with these columns: `qc_id`, `batch_id`, `specification_id`, `qc_date`, `qc_type`, `inspector_id`, `result`, `defect_count`, and `notes`.

From the business description, these records capture inspection and testin…

**Sources retrieved (12):** `Quality Control→QUALITY_CONTROL`, `BOM→PRODUCT`, `parent_chunk_data_dictionary.md_3`, `BATCH→PRODUCT`, `BATCH→WAREHOUSE`, `parent_chunk_business_glossary.md_2`, `Quality Control`, `parent_chunk_business_glossary.md_0`

**Context previews (first 3):**

1. _Business concept 'Quality Control' — The table name, comment, and columns (qc_date, qc_type, inspector_id, result, defect_count, notes) clearly indicate inspection and testing records for quality assu…_

2. _Relationship: BOM references PRODUCT via foreign key COMPONENT_PRODUCT_ID -> PRODUCT.PRODUCT_ID.…_

3. _# Manufacturing Data Dictionary  This data dictionary documents the database schema for the manufacturing supply chain system. It includes all tables, columns, data types, constraints, and relationshi…_

---

### ✅ QA-010 — What do specification records define?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.7558 | **Gate:** `proceed`

**Expected answer:**
> Specifications define technical requirements with a unique identifier (specification_id), descriptive name (specification_name), version number, effective date, specification type (DIMENSIONAL, MATERIAL, PERFORMANCE), critical parameter being measured (critical_parameter), acceptable minimum value (…

**System answer:**
> Specification records define the technical requirements, standards, and acceptance criteria for materials and products. In the `SPECIFICATION` table, they capture a unique specification identifier, specification name, version, effective date, specification type (`DIMENSIONAL`, `MATERIAL`, `PERFORMANCE`), the critical parameter being tested, the minimum and maximum acceptable values, and the unit o…

**Sources retrieved (12):** `Quality Control→QUALITY_CONTROL`, `Specification→SPECIFICATION`, `parent_chunk_data_dictionary.md_7`, `a parent product, a component product (which can be either a component or sub-assembly), the required quantity, unit of measure, and hierarchical level in the product structure→COMPONENT`, `parent_chunk_data_dictionary.md_3`, `parent_chunk_business_glossary.md_2`, `Specification`, `parent_chunk_business_glossary.md_0`

**Context previews (first 3):**

1. _Business concept 'Quality Control' — The table name, comment, and columns (qc_date, qc_type, inspector_id, result, defect_count, notes) clearly indicate inspection and testing records for quality assu…_

2. _Business concept 'Specification' — The table name and columns directly match the glossary concept for technical requirements/specifications, including identifier, name, version, effective date, type, …_

3. _## specification  Defines technical requirements and acceptance criteria for materials and products.  | Column | Data Type | Constraints | Description | |--------|-----------|-------------|-----------…_

---

### ✅ QA-011 — How can I find which suppliers provide specific components?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.1645 | **Gate:** `proceed_with_warning`

**Expected answer:**
> Query the component_supplier table which links components to their approved suppliers. This table contains the component identifier (component_id), supplier identifier (supplier_id), preferred supplier flag (is_preferred), lead time in days (lead_time_days), and unit price (unit_price). Join with th…

**System answer:**
> To find which suppliers provide specific components, use the `COMPONENT_SUPPLIER` table. The retrieved context defines it as the business concept “Approved Supplier Relationship,” and it explicitly links components to their approved suppliers through `component_id` and `supplier_id`.

The join path is:

`COMPONENT.COMPONENT_ID = COMPONENT_SUPPLIER.COMPONENT_ID`
and
`SUPPLIER.SUPPLIER_ID = COMPONEN…

**Sources retrieved (12):** `Approved Supplier Relationship→COMPONENT_SUPPLIER`, `parent_chunk_data_dictionary.md_5`, `parent_chunk_data_dictionary.md_4`, `Suppliers→SUPPLIER`, `parent_chunk_data_dictionary.md_3`, `parent_chunk_data_dictionary.md_8`, `parent_chunk_business_glossary.md_0`, `Approved Supplier Relationship`

**Context previews (first 3):**

1. _Business concept 'Approved Supplier Relationship' — The table is a junction entity linking component_id and supplier_id, and the comments explicitly say it links components to their approved suppliers…_

2. _## warehouse  Stores physical storage location information for inventory management.  | Column | Data Type | Constraints | Description | |--------|-----------|-------------|-------------| | warehouse_…_

3. _## bom  Bill of Materials defining product composition and hierarchical structure. Supports recursive relationships for multi-level assemblies.  | Column | Data Type | Constraints | Description | |---…_

---

### ✅ QA-012 — How do I trace which components are needed to fulfill a work order?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.2334 | **Gate:** `proceed`

**Expected answer:**
> Start with the work_order table to get the product_id being manufactured. Join to the bom table using product_id as parent_product_id to find all direct components and sub-assemblies. For each component_product_id, if it is an ASSEMBLY type product, recursively query the bom table again to explode m…

**System answer:**
> From the available schema, the trace starts at `WORK_ORDER`, which implements the Manufacturing Work Order concept.

To identify what a work order requires, first use `WORK_ORDER.product_id` to find the product being manufactured in `PRODUCT.product_id`. The `work_order` table tells you the production job, including `work_order_id`, `product_id`, `quantity_ordered`, `quantity_completed`, `status`,…

**Sources retrieved (12):** `Manufacturing Work Order`, `parent_chunk_data_dictionary.md_5`, `Manufacturing Work Order→WORK_ORDER`, `parent_chunk_data_dictionary.md_6`, `parent_chunk_data_dictionary.md_3`, `parent_chunk_data_dictionary.md_8`, `a parent product, a component product (which can be either a component or sub-assembly), the required quantity, unit of measure, and hierarchical level in the product structure→COMPONENT`, `Inventory→INVENTORY`

**Context previews (first 3):**

1. _Manufacturing Work Order: The table is explicitly labeled as production jobs and includes product reference, parent work order hierarchy, planned dates, quantities ordered/completed, status, and prior…_

2. _## warehouse  Stores physical storage location information for inventory management.  | Column | Data Type | Constraints | Description | |--------|-----------|-------------|-------------| | warehouse_…_

3. _Business concept 'Manufacturing Work Order' — The table is explicitly labeled as production jobs and includes product reference, parent work order hierarchy, planned dates, quantities ordered/complete…_

---

### ✅ QA-013 — How can I identify which warehouses have available inventory for specific components?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.8215 | **Gate:** `proceed`

**Expected answer:**
> Query the inventory table filtered by component_id, joining with the warehouse table to get warehouse names and locations. Calculate available quantity as quantity_on_hand minus quantity_reserved. Filter for records where available quantity is greater than zero. Results show warehouse names, locatio…

**System answer:**
> Use the INVENTORY table as the starting point, because Inventory is defined as the actual stock levels of components and products stored in specific warehouses, and it tracks quantity_on_hand and quantity_reserved.

To identify warehouses for a specific component, follow this schema path: INVENTORY.component_id -> COMPONENT.component_id and INVENTORY.warehouse_id -> WAREHOUSE.warehouse_id. The cri…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_5`, `Inventory`, `Inventory→INVENTORY`, `INVENTORY→WAREHOUSE`, `INVENTORY→COMPONENT`, `parent_chunk_data_dictionary.md_3`, `parent_chunk_data_dictionary.md_8`, `Batches→BATCH`

**Context previews (first 3):**

1. _## warehouse  Stores physical storage location information for inventory management.  | Column | Data Type | Constraints | Description | |--------|-----------|-------------|-------------| | warehouse_…_

2. _Inventory: The table is explicitly labeled as inventory stock levels and contains canonical inventory measures such as quantity_on_hand, quantity_reserved, reorder_threshold, and last_restock_date. It…_

3. _Business concept 'Inventory' — The table is explicitly labeled as inventory stock levels and contains canonical inventory measures such as quantity_on_hand, quantity_reserved, reorder_threshold, and l…_

---

### ✅ QA-014 — How do I find which shipments delivered materials from a specific supplier?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.2401 | **Gate:** `proceed`

**Expected answer:**
> Query the shipment table filtering by supplier_id and shipment_type = 'INBOUND'. Join with the warehouse table to show destination warehouses. Filter for status = 'DELIVERED' and include actual_arrival date. Results can be ordered by ship_date descending to show most recent deliveries first.

**System answer:**
> Use the SHIPMENT table as the starting point. To find shipments that delivered materials from a specific supplier, filter SHIPMENT on `supplier_id` and on the inbound/delivery fields that the schema defines.

The relevant logic from the context is:

`SHIPMENT.supplier_id` references `SUPPLIER.supplier_id`, and the `chk_supplier_inbound` constraint says `supplier_id` is only set for `INBOUND` shipm…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_8`, `SHIPMENT→SUPPLIER`, `Shipment→SHIPMENT`, `Shipment`, `parent_chunk_data_dictionary.md_5`, `Suppliers→SUPPLIER`, `parent_chunk_business_glossary.md_1`, `parent_chunk_business_glossary.md_0`

**Context previews (first 3):**

1. _## shipment  Tracks material transfers between warehouses, suppliers, and customers.  | Column | Data Type | Constraints | Description | |--------|-----------|-------------|-------------| | shipment_i…_

2. _Relationship: SHIPMENT references SUPPLIER via foreign key SUPPLIER_ID -> SUPPLIER.SUPPLIER_ID.…_

3. _Business concept 'Shipment' — The table name, primary key, and date/status fields align directly with the shipment concept, and the foreign keys to warehouse, supplier, and customer match the inbound/…_

---

### ✅ QA-015 — How can I determine which quality control inspections were performed on a specific production batch?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.9779 | **Gate:** `proceed`

**Expected answer:**
> Query the quality_control table filtered by batch_id. Join with the specification table to get requirement details (specification_name, spec_type, acceptable ranges). Include qc_date, qc_type (INCOMING, IN_PROCESS, FINAL), result (PASS, FAIL, CONDITIONAL), and defect_count. This shows the complete i…

**System answer:**
> Use the `QUALITY_CONTROL` table, because it stores the QC inspection records and includes `batch_id` to identify the production batch being inspected.

To determine which inspections were performed on a specific batch, filter `QUALITY_CONTROL.batch_id` to the target batch. The relevant inspection details in `QUALITY_CONTROL` are:
`qc_id`, `batch_id`, `specification_id`, `qc_date`, `qc_type`, `insp…

**Sources retrieved (12):** `Quality Control→QUALITY_CONTROL`, `Batches→BATCH`, `parent_chunk_data_dictionary.md_7`, `BATCH→PRODUCT`, `parent_chunk_data_dictionary.md_5`, `parent_chunk_data_dictionary.md_6`, `parent_chunk_data_dictionary.md_3`, `parent_chunk_business_glossary.md_2`

**Context previews (first 3):**

1. _Business concept 'Quality Control' — The table name, comment, and columns (qc_date, qc_type, inspector_id, result, defect_count, notes) clearly indicate inspection and testing records for quality assu…_

2. _Business concept 'Batches' — The table is explicitly labelled as a batch/production lots table and contains batch-specific identifiers, produced quantity, production date, expiry date, warehouse linka…_

3. _## specification  Defines technical requirements and acceptance criteria for materials and products.  | Column | Data Type | Constraints | Description | |--------|-----------|-------------|-----------…_

---

### ✅ QA-016 — How do I track which work orders are in progress at a specific warehouse?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.7311 | **Gate:** `proceed`

**Expected answer:**
> Query the work_order table filtering by warehouse_id and status = 'IN_PROGRESS'. Join with the product table to get product names and types. Include quantity_ordered, quantity_completed, priority, planned_end_date, and calculate progress percentage as (quantity_completed / quantity_ordered * 100). O…

**System answer:**
> Use the `WORK_ORDER` table. A work order is defined there as a manufacturing production job, and it includes both the warehouse link and the production status.

To find work orders that are currently in progress at a specific warehouse, filter `WORK_ORDER` on:
`status = 'IN_PROGRESS'`
and
`warehouse_id = <target warehouse_id>`

The key columns in `WORK_ORDER` for tracking are `work_order_id`, `pro…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_5`, `Manufacturing Work Order`, `parent_chunk_data_dictionary.md_6`, `Manufacturing Work Order→WORK_ORDER`, `WORK_ORDER→WAREHOUSE`, `parent_chunk_data_dictionary.md_8`, `parent_chunk_data_dictionary.md_7`, `Batches→BATCH`

**Context previews (first 3):**

1. _## warehouse  Stores physical storage location information for inventory management.  | Column | Data Type | Constraints | Description | |--------|-----------|-------------|-------------| | warehouse_…_

2. _Manufacturing Work Order: The table is explicitly labeled as production jobs and includes product reference, parent work order hierarchy, planned dates, quantities ordered/completed, status, and prior…_

3. _## work_order  Represents production jobs for manufacturing products with hierarchical work order support.  | Column | Data Type | Constraints | Description | |--------|-----------|-------------|-----…_

---

### ✅ QA-017 — How can I find which components need reordering based on current inventory levels?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.3023 | **Gate:** `proceed`

**Expected answer:**
> Query the inventory table and filter where quantity_on_hand minus quantity_reserved is less than reorder_threshold. Join with the component table to get component names, categories, and standard costs. Join with the warehouse table for location information. Results identify which components are belo…

**System answer:**
> Use the INVENTORY table, because it is the table that tracks stock levels and contains the relevant measures: quantity_on_hand, quantity_reserved, reorder_threshold, last_restock_date, warehouse_id, component_id, and product_id.

For components specifically, look for INVENTORY rows where component_id is populated, since the schema says an inventory record supports either a component or a product, …

**Sources retrieved (12):** `Inventory→INVENTORY`, `Inventory`, `parent_chunk_data_dictionary.md_5`, `INVENTORY→COMPONENT`, `parent_chunk_data_dictionary.md_3`, `parent_chunk_data_dictionary.md_7`, `parent_chunk_data_dictionary.md_4`, `a parent product, a component product (which can be either a component or sub-assembly), the required quantity, unit of measure, and hierarchical level in the product structure→COMPONENT`

**Context previews (first 3):**

1. _Business concept 'Inventory' — The table is explicitly labeled as inventory stock levels and contains canonical inventory measures such as quantity_on_hand, quantity_reserved, reorder_threshold, and l…_

2. _Inventory: The table is explicitly labeled as inventory stock levels and contains canonical inventory measures such as quantity_on_hand, quantity_reserved, reorder_threshold, and last_restock_date. It…_

3. _## warehouse  Stores physical storage location information for inventory management.  | Column | Data Type | Constraints | Description | |--------|-----------|-------------|-------------| | warehouse_…_

---

### ✅ QA-018 — How do I determine the manufacturing route for a specific product?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0442 | **Gate:** `proceed_with_warning`

**Expected answer:**
> Query the route table filtering by product_id, ordered by sequence_number ascending. For each operation, retrieve operation_name, work_center, cycle_time_minutes, and setup_time_minutes. Join with the product table to get product details. The sequence of operations shows the complete manufacturing w…

**System answer:**
> To determine the manufacturing route for a specific product, use the `ROUTE` table, which implements the business concept `Route Steps`. The documented relationship is `ROUTE.product_id -> PRODUCT.product_id`, so the route for a product is identified through that `product_id`.

If you already know the product ID, retrieve all rows from `ROUTE` where `ROUTE.product_id` equals that product’s `PRODUC…

**Sources retrieved (12):** `Route Steps→ROUTE`, `parent_chunk_data_dictionary.md_6`, `ROUTE→PRODUCT`, `Manufacturing Work Order`, `parent_chunk_data_dictionary.md_3`, `Manufacturing Work Order→WORK_ORDER`, `parent_chunk_data_dictionary.md_7`, `parent_chunk_data_dictionary.md_5`

**Context previews (first 3):**

1. _Business concept 'Route Steps' — The table explicitly represents manufacturing workflow steps, with sequence_number, operation_name, work_center, and per-step timing fields such as cycle and setup tim…_

2. _## work_order  Represents production jobs for manufacturing products with hierarchical work order support.  | Column | Data Type | Constraints | Description | |--------|-----------|-------------|-----…_

3. _Relationship: ROUTE references PRODUCT via foreign key PRODUCT_ID -> PRODUCT.PRODUCT_ID.…_

---

### ✅ QA-019 — How can I find which batches are stored at a specific warehouse and their QC status?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.7533 | **Gate:** `proceed`

**Expected answer:**
> Query the batch table filtering by warehouse_id. Join with the product table to get product names and types. Include production_date, quantity_produced, expiry_date, and qc_status (PENDING, PASSED, FAILED, QUARANTINED). Filter by qc_status to isolate batches requiring quality attention or ready for …

**System answer:**
> Use the `BATCH` table. It directly implements the business concept of production batches and contains both the warehouse link and the batch QC status:

`BATCH(batch_id, product_id, production_date, quantity_produced, warehouse_id, expiry_date, qc_status)`

To find batches stored at a specific warehouse, filter `BATCH.warehouse_id` for the warehouse you want. The QC status is already stored in `BAT…

**Sources retrieved (12):** `Batches→BATCH`, `parent_chunk_data_dictionary.md_5`, `BATCH→WAREHOUSE`, `Quality Control→QUALITY_CONTROL`, `parent_chunk_data_dictionary.md_6`, `parent_chunk_data_dictionary.md_8`, `Manufacturing Work Order→WORK_ORDER`, `Inventory→INVENTORY`

**Context previews (first 3):**

1. _Business concept 'Batches' — The table is explicitly labelled as a batch/production lots table and contains batch-specific identifiers, produced quantity, production date, expiry date, warehouse linka…_

2. _## warehouse  Stores physical storage location information for inventory management.  | Column | Data Type | Constraints | Description | |--------|-----------|-------------|-------------| | warehouse_…_

3. _Relationship: BATCH references WAREHOUSE via foreign key WAREHOUSE_ID -> WAREHOUSE.WAREHOUSE_ID.…_

---

### ✅ QA-020 — How do I identify which specifications apply to specific components?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.2550 | **Gate:** `proceed`

**Expected answer:**
> Query the component table and join with the specification table via specification_id. Include component_name, component_category, and specification details (specification_name, spec_type, critical_parameter, min_value, max_value, unit_of_measure). This shows the technical requirements that each comp…

**System answer:**
> To identify which specifications apply to specific components, use the link between COMPONENT and SPECIFICATION.

The COMPONENT table includes the column specification_id, and the SPECIFICATION table is keyed by specification_id. So the schema-level path is:

COMPONENT.specification_id = SPECIFICATION.specification_id

That lets you trace a component to its applicable specification and retrieve bo…

**Sources retrieved (12):** `a parent product, a component product (which can be either a component or sub-assembly), the required quantity, unit of measure, and hierarchical level in the product structure→COMPONENT`, `parent_chunk_data_dictionary.md_5`, `parent_chunk_data_dictionary.md_7`, `parent_chunk_data_dictionary.md_3`, `Specification→SPECIFICATION`, `parent_chunk_data_dictionary.md_4`, `Approved Supplier Relationship→COMPONENT_SUPPLIER`, `parent_chunk_business_glossary.md_0`

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
> Use the `BOM` table recursively, starting from the finished product in `PRODUCT`.

A complete BOM explosion is supported directly by the schema because `BOM` is defined as a hierarchical structure with:
`parent_product_id` → the product being built,
`component_product_id` → the product that goes into it,
`quantity`,
`unit_of_measure`,
`bom_level`,
and `is_optional`.

The join path is:

1. Identify…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_4`, `parent_chunk_data_dictionary.md_3`, `The Bill of Materials (BOM)→BOM`, `BOM→PRODUCT`, `Manufacturing Work Order→WORK_ORDER`, `Manufacturing Work Order`, `a parent product, a component product (which can be either a component or sub-assembly), the required quantity, unit of measure, and hierarchical level in the product structure→COMPONENT`, `parent_chunk_data_dictionary.md_5`

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
> From the retrieved context, the schema supports this as a recursive BOM roll-up, but it does not fully specify the costing policy.

Structurally, you calculate it by starting with the target `product.product_id`, finding all rows in `bom` where `bom.parent_product_id = product.product_id`, and joining each `bom.component_product_id` back to `product.product_id`. Because `bom` is recursive and supp…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_3`, `a parent product, a component product (which can be either a component or sub-assembly), the required quantity, unit of measure, and hierarchical level in the product structure→COMPONENT`, `parent_chunk_data_dictionary.md_4`, `parent_chunk_data_dictionary.md_7`, `parent_chunk_data_dictionary.md_8`, `The Bill of Materials (BOM)→BOM`, `parent_chunk_data_dictionary.md_6`, `parent_chunk_data_dictionary.md_5`

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
> Use the BOM table recursively.

The direct containment relationship is in `BOM`, where:
- `parent_product_id` is the product being built,
- `component_product_id` is the product that goes into it,
- both columns reference `PRODUCT.PRODUCT_ID`.

To find every parent product that contains a specific component anywhere in the structure, start with the target component in `BOM.component_product_id`, t…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_4`, `parent_chunk_data_dictionary.md_3`, `The Bill of Materials (BOM)→BOM`, `a parent product, a component product (which can be either a component or sub-assembly), the required quantity, unit of measure, and hierarchical level in the product structure→COMPONENT`, `BOM→PRODUCT`, `Manufacturing Work Order→WORK_ORDER`, `Manufacturing Work Order`, `PRODUCT→PRODUCT`

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
> Use `WORK_ORDER` together with the recursive `BOM` structure.

A work order is for the product in `WORK_ORDER.product_id`. A required component is represented through `BOM`, where:

- `BOM.parent_product_id` = the product being built
- `BOM.component_product_id` = a product that goes into it
- both columns reference `PRODUCT.product_id`
- `BOM` explicitly supports recursive, multi-level assemblies…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_6`, `parent_chunk_data_dictionary.md_5`, `a parent product, a component product (which can be either a component or sub-assembly), the required quantity, unit of measure, and hierarchical level in the product structure→COMPONENT`, `parent_chunk_data_dictionary.md_3`, `Manufacturing Work Order→WORK_ORDER`, `parent_chunk_data_dictionary.md_4`, `Manufacturing Work Order`, `WORK_ORDER→WORK_ORDER`

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
> Use the `bom` table’s `bom_level` column. In the schema, `bom_level` is defined as the “depth in product hierarchy,” is constrained to be `>= 0`, and is explicitly described as tracking depth for performance optimization. So the maximum BOM depth overall is the maximum value of `BOM.bom_level`.

If you need the maximum depth for a specific product, use `BOM.parent_product_id` to identify the produ…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_4`, `parent_chunk_data_dictionary.md_3`, `The Bill of Materials (BOM)→BOM`, `BOM→PRODUCT`, `parent_chunk_data_dictionary.md_7`, `Manufacturing Work Order→WORK_ORDER`, `Manufacturing Work Order`, `parent_chunk_data_dictionary.md_5`

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
> Use the `bom` table to trace upward through the product hierarchy.

The relevant structure is:

- `bom.parent_product_id` = the product being built
- `bom.component_product_id` = the product that goes into it
- `bom` supports recursive, multi-level assemblies
- The business concept explicitly says the component product can be either a component or a sub-assembly
- `bom_level` stores hierarchy dept…

**Sources retrieved (12):** `a parent product, a component product (which can be either a component or sub-assembly), the required quantity, unit of measure, and hierarchical level in the product structure→COMPONENT`, `parent_chunk_data_dictionary.md_3`, `parent_chunk_data_dictionary.md_4`, `parent_chunk_data_dictionary.md_5`, `parent_chunk_data_dictionary.md_7`, `The Bill of Materials (BOM)→BOM`, `parent_chunk_data_dictionary.md_6`, `Inventory→INVENTORY`

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
> The context provides the schema needed to trace all sub-assemblies, but it does not define an official business rule for how “total lead time” should be aggregated. Specifically, it tells you where the lead time is stored and how to traverse the hierarchy, but not whether total lead time should be the sum of all levels, the maximum path, or some other calculation.

From the schema, the core source…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_3`, `a parent product, a component product (which can be either a component or sub-assembly), the required quantity, unit of measure, and hierarchical level in the product structure→COMPONENT`, `Approved Supplier Relationship→COMPONENT_SUPPLIER`, `parent_chunk_data_dictionary.md_4`, `parent_chunk_data_dictionary.md_7`, `parent_chunk_data_dictionary.md_6`, `parent_chunk_data_dictionary.md_8`, `parent_chunk_business_glossary.md_0`

**Context previews (first 3):**

1. _# Manufacturing Data Dictionary  This data dictionary documents the database schema for the manufacturing supply chain system. It includes all tables, columns, data types, constraints, and relationshi…_

2. _Business concept 'a parent product, a component product (which can be either a component or sub-assembly), the required quantity, unit of measure, and hierarchical level in the product structure' is i…_

3. _Business concept 'Approved Supplier Relationship' — The table is a junction entity linking component_id and supplier_id, and the comments explicitly say it links components to their approved suppliers…_

---

### ✅ QA-028 — How do I generate a complete indented BOM report showing the hierarchical structure?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.4180 | **Gate:** `proceed`

**Expected answer:**
> Use a recursive query on the bom table that tracks the current depth level. Start with the top-level product (parent_product_id where product has no parent_product_id). At each level, output component details indented by depth level. Include product_name, quantity, and unit_of_measure. Recursively p…

**System answer:**
> Use the `bom` table as the report’s primary source. The retrieved context explicitly says `bom` defines product composition and hierarchical structure, supports recursive relationships for multi-level assemblies, and stores the hierarchical depth in `bom_level`.

At schema level, the report should be built from these columns in `bom`:

`bom_id`, `parent_product_id`, `component_product_id`, `quanti…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_4`, `parent_chunk_data_dictionary.md_3`, `a parent product, a component product (which can be either a component or sub-assembly), the required quantity, unit of measure, and hierarchical level in the product structure→COMPONENT`, `Manufacturing Work Order→WORK_ORDER`, `Manufacturing Work Order`, `parent_chunk_data_dictionary.md_6`, `parent_chunk_data_dictionary.md_8`, `The Bill of Materials (BOM)→BOM`

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
> Use the BOM table as the source, because the Bill of Materials is implemented by physical table BOM with the columns bom_id, parent_product_id, component_product_id, quantity, unit_of_measure, bom_level, and is_optional.

To find which components appear most frequently, aggregate BOM rows by component_product_id. The core join path is BOM.component_product_id → PRODUCT.product_id, because BOM refe…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_4`, `parent_chunk_data_dictionary.md_3`, `The Bill of Materials (BOM)→BOM`, `BOM→PRODUCT`, `Manufacturing Work Order`, `Manufacturing Work Order→WORK_ORDER`, `parent_chunk_data_dictionary.md_5`, `a parent product, a component product (which can be either a component or sub-assembly), the required quantity, unit of measure, and hierarchical level in the product structure→COMPONENT`

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
> From the retrieved context, the BOM structure is recursive because `BOM.parent_product_id` and `BOM.component_product_id` both reference `PRODUCT.product_id`. The `bom` table is described as supporting “recursive relationships for multi-level assemblies,” and `bom_level` is used to track hierarchy depth for performance optimization. The schema also includes a unique constraint, `uq_bom_structure` …

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_4`, `parent_chunk_data_dictionary.md_3`, `BOM→PRODUCT`, `Manufacturing Work Order`, `Manufacturing Work Order→WORK_ORDER`, `The Bill of Materials (BOM)→BOM`, `parent_chunk_data_dictionary.md_8`, `parent_chunk_data_dictionary.md_7`

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
> Based on the retrieved context, you can determine the full product structure for a finished product, but you cannot fully derive the complete end-to-end supplier chain from that finished product using only the documented relationships.

The product hierarchy is modeled through `bom` and `product`. To trace all sub-assemblies and lower-level parts, start from `product.product_id` for the finished g…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_3`, `a parent product, a component product (which can be either a component or sub-assembly), the required quantity, unit of measure, and hierarchical level in the product structure→COMPONENT`, `parent_chunk_data_dictionary.md_4`, `parent_chunk_data_dictionary.md_8`, `parent_chunk_data_dictionary.md_6`, `Approved Supplier Relationship→COMPONENT_SUPPLIER`, `Suppliers→SUPPLIER`, `parent_chunk_data_dictionary.md_7`

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
> Use `WORK_ORDER` and `INVENTORY`, with `WAREHOUSE` if you want warehouse-level detail.

At the schema level, start from `WORK_ORDER` using `work_order_id`. That table gives you the `product_id` for the item being produced, the `quantity_ordered`, the `quantity_completed`, and the production `warehouse_id`. If you want the remaining quantity still to be fulfilled, the relevant work-order quantities…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_5`, `parent_chunk_data_dictionary.md_6`, `Inventory`, `Inventory→INVENTORY`, `Manufacturing Work Order`, `Manufacturing Work Order→WORK_ORDER`, `INVENTORY→WAREHOUSE`, `WORK_ORDER→WAREHOUSE`

**Context previews (first 3):**

1. _## warehouse  Stores physical storage location information for inventory management.  | Column | Data Type | Constraints | Description | |--------|-----------|-------------|-------------| | warehouse_…_

2. _## work_order  Represents production jobs for manufacturing products with hierarchical work order support.  | Column | Data Type | Constraints | Description | |--------|-----------|-------------|-----…_

3. _Inventory: The table is explicitly labeled as inventory stock levels and contains canonical inventory measures such as quantity_on_hand, quantity_reserved, reorder_threshold, and last_restock_date. It…_

---

### ✅ QA-033 — How can I find which quality control inspections failed for components from specific suppliers?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.4561 | **Gate:** `proceed`

**Expected answer:**
> Query the quality_control table filtering by result = 'FAIL'. Join with the batch table to get product_id and production_date. Join with the bom table recursively to trace which products contain failed components. Join with component_supplier and supplier tables to identify the source supplier. Filt…

**System answer:**
> From the retrieved context, this can only be answered partially at the schema level.

Failed quality inspections are recorded in the `QUALITY_CONTROL` table, which implements the Quality Control concept. The relevant columns are `qc_id`, `batch_id`, `specification_id`, `qc_date`, `qc_type`, `inspector_id`, `result`, `defect_count`, and `notes`. To find failed inspections, the key filter is `result…

**Sources retrieved (12):** `Quality Control→QUALITY_CONTROL`, `parent_chunk_data_dictionary.md_5`, `parent_chunk_data_dictionary.md_3`, `Approved Supplier Relationship→COMPONENT_SUPPLIER`, `parent_chunk_data_dictionary.md_4`, `Suppliers→SUPPLIER`, `parent_chunk_business_glossary.md_2`, `parent_chunk_business_glossary.md_0`

**Context previews (first 3):**

1. _Business concept 'Quality Control' — The table name, comment, and columns (qc_date, qc_type, inspector_id, result, defect_count, notes) clearly indicate inspection and testing records for quality assu…_

2. _## warehouse  Stores physical storage location information for inventory management.  | Column | Data Type | Constraints | Description | |--------|-----------|-------------|-------------| | warehouse_…_

3. _# Manufacturing Data Dictionary  This data dictionary documents the database schema for the manufacturing supply chain system. It includes all tables, columns, data types, constraints, and relationshi…_

---

### ✅ QA-034 — How do I calculate the total manufacturing time for a work order including all sub-assembly work orders?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.1599 | **Gate:** `proceed_with_warning`

**Expected answer:**
> Query the work_order table starting with the parent work_order. Find all child work_orders where parent_work_order matches the current work_order_id. For each work order (parent and children), join with the route table on product_id to get all operations. Sum (cycle_time_minutes * quantity) plus set…

**System answer:**
> From the retrieved context, the supported way to calculate total manufacturing time for a work order including sub-assembly work orders is to use the work order hierarchy in `WORK_ORDER` and the per-step timing fields in `ROUTE`.

`WORK_ORDER` represents manufacturing production jobs and supports decomposition through the self-referential column `parent_work_order → work_order(work_order_id)`. Tha…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_6`, `Manufacturing Work Order→WORK_ORDER`, `Manufacturing Work Order`, `parent_chunk_data_dictionary.md_3`, `Route Steps→ROUTE`, `a parent product, a component product (which can be either a component or sub-assembly), the required quantity, unit of measure, and hierarchical level in the product structure→COMPONENT`, `parent_chunk_data_dictionary.md_7`, `parent_chunk_data_dictionary.md_5`

**Context previews (first 3):**

1. _## work_order  Represents production jobs for manufacturing products with hierarchical work order support.  | Column | Data Type | Constraints | Description | |--------|-----------|-------------|-----…_

2. _Business concept 'Manufacturing Work Order' — The table is explicitly labeled as production jobs and includes product reference, parent work order hierarchy, planned dates, quantities ordered/complete…_

3. _Manufacturing Work Order: The table is explicitly labeled as production jobs and includes product reference, parent work order hierarchy, planned dates, quantities ordered/completed, status, and prior…_

---

### ✅ QA-035 — How can I identify which shipments are overdue and their impact on work orders?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0719 | **Gate:** `proceed_with_warning`

**Expected answer:**
> Query the shipment table filtering for status = 'SHIPPED' where actual_arrival is NULL and estimated_arrival is in the past (overdue). Join with the component_supplier table via supplier_id and component_id to identify which components are delayed. Perform reverse BOM lookup to find which parent pro…

**System answer:**
> The knowledge graph provides schema-level metadata, not actual shipment or work order records, so it cannot tell you which specific shipments are overdue. It does, however, show how to identify them and how to trace likely impact on work orders.

Use the SHIPMENT table to detect overdue shipments. The relevant columns are SHIPMENT.shipment_id, shipment_type, warehouse_id, ship_date, estimated_arri…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_5`, `parent_chunk_data_dictionary.md_8`, `parent_chunk_data_dictionary.md_6`, `Manufacturing Work Order→WORK_ORDER`, `Shipment→SHIPMENT`, `Manufacturing Work Order`, `WORK_ORDER→PRODUCT`, `WORK_ORDER→WAREHOUSE`

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
> From the retrieved context, only part of this can be answered.

You can identify batches that are past expiry or nearing expiry from the `BATCH` table, because it contains `batch_id`, `product_id`, `production_date`, `quantity_produced`, `warehouse_id`, `expiry_date`, and `qc_status`. A past-expiry batch would be determined by comparing `BATCH.expiry_date` to a reference date. An “approaching expi…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_5`, `Batches→BATCH`, `parent_chunk_data_dictionary.md_7`, `parent_chunk_data_dictionary.md_3`, `Approved Supplier Relationship→COMPONENT_SUPPLIER`, `parent_chunk_data_dictionary.md_8`, `parent_chunk_business_glossary.md_2`, `parent_chunk_business_glossary.md_1`

**Context previews (first 3):**

1. _## warehouse  Stores physical storage location information for inventory management.  | Column | Data Type | Constraints | Description | |--------|-----------|-------------|-------------| | warehouse_…_

2. _Business concept 'Batches' — The table is explicitly labelled as a batch/production lots table and contains batch-specific identifiers, produced quantity, production date, expiry date, warehouse linka…_

3. _## specification  Defines technical requirements and acceptance criteria for materials and products.  | Column | Data Type | Constraints | Description | |--------|-----------|-------------|-----------…_

---

### ✅ QA-037 — How can I generate a material requirements plan showing when to order components based on work order schedules?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0433 | **Gate:** `proceed_with_warning`

**Expected answer:**
> Query all work_orders with status 'PENDING' ordered by planned_start_date. For each work_order, perform BOM explosion to get required components and quantities. For each component, query inventory for current available stock across warehouses. Calculate net requirements = (required quantity * work_o…

**System answer:**
> Based on the retrieved schema, you can build this plan from `WORK_ORDER`, `BOM`, `PRODUCT`, and `INVENTORY`.

`WORK_ORDER` is the schedule driver for manufacturing demand. It gives you the product being built (`product_id`), the scheduled dates (`planned_start_date`, `planned_end_date`), the quantities (`quantity_ordered`, `quantity_completed`), the production location (`warehouse_id`), and the hi…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_6`, `parent_chunk_data_dictionary.md_7`, `parent_chunk_data_dictionary.md_5`, `Manufacturing Work Order→WORK_ORDER`, `parent_chunk_data_dictionary.md_4`, `Manufacturing Work Order`, `parent_chunk_data_dictionary.md_3`, `The Bill of Materials (BOM)→BOM`

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
> The knowledge graph only provides schema-level metadata, not operational records, so you cannot trace a specific real-world component instance end-to-end here. But based on the available schema, the genealogy logic is:

Start with the approved sourcing relationship in `COMPONENT_SUPPLIER`. This table implements the “Approved Supplier Relationship” business concept and links `component_id` to `supp…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_3`, `parent_chunk_data_dictionary.md_7`, `parent_chunk_data_dictionary.md_5`, `parent_chunk_data_dictionary.md_8`, `parent_chunk_data_dictionary.md_4`, `Approved Supplier Relationship→COMPONENT_SUPPLIER`, `COMPONENT_SUPPLIER→COMPONENT`, `Shipment→SHIPMENT`

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
> Use the BOM structure to identify shared components, then use the approved supplier relationship to list sourcing options.

At the product-structure level, the `bom` table shows what goes into what: `parent_product_id` is the product being built and `component_product_id` is the product used as a component. Because both columns reference `product(product_id)`, and the BOM supports recursive multi-…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_4`, `Approved Supplier Relationship→COMPONENT_SUPPLIER`, `parent_chunk_data_dictionary.md_3`, `parent_chunk_data_dictionary.md_5`, `parent_chunk_data_dictionary.md_8`, `parent_chunk_data_dictionary.md_7`, `COMPONENT_SUPPLIER→COMPONENT`, `Suppliers→SUPPLIER`

**Context previews (first 3):**

1. _## bom  Bill of Materials defining product composition and hierarchical structure. Supports recursive relationships for multi-level assemblies.  | Column | Data Type | Constraints | Description | |---…_

2. _Business concept 'Approved Supplier Relationship' — The table is a junction entity linking component_id and supplier_id, and the comments explicitly say it links components to their approved suppliers…_

3. _# Manufacturing Data Dictionary  This data dictionary documents the database schema for the manufacturing supply chain system. It includes all tables, columns, data types, constraints, and relationshi…_

---

### ✅ QA-040 — How do I calculate the total landed cost for a product including component costs, supplier lead times, and manufacturing operations?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.1922 | **Gate:** `proceed_with_warning`

**Expected answer:**
> Perform recursive BOM explosion to get all leaf components. For each component, query component_supplier to get unit_price from primary supplier. Multiply by accumulated BOM quantity for material cost. Add shipping costs (estimated from shipment history). Query route table for the product to get all…

**System answer:**
> From the retrieved context, a full total landed cost calculation cannot be determined. The context gives you some cost- and lead-time-related fields, but it does not define a landed-cost formula, and it does not include manufacturing operation cost data.

What is known is this: a product is stored in `product`, where `product.base_cost` is the base manufacturing cost and `product.lead_time_days` i…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_3`, `Approved Supplier Relationship→COMPONENT_SUPPLIER`, `a parent product, a component product (which can be either a component or sub-assembly), the required quantity, unit of measure, and hierarchical level in the product structure→COMPONENT`, `parent_chunk_data_dictionary.md_6`, `parent_chunk_data_dictionary.md_7`, `parent_chunk_data_dictionary.md_5`, `parent_chunk_data_dictionary.md_8`, `parent_chunk_data_dictionary.md_4`

**Context previews (first 3):**

1. _# Manufacturing Data Dictionary  This data dictionary documents the database schema for the manufacturing supply chain system. It includes all tables, columns, data types, constraints, and relationshi…_

2. _Business concept 'Approved Supplier Relationship' — The table is a junction entity linking component_id and supplier_id, and the comments explicitly say it links components to their approved suppliers…_

3. _Business concept 'a parent product, a component product (which can be either a component or sub-assembly), the required quantity, unit of measure, and hierarchical level in the product structure' is i…_

---

## Anomalies & Observations

No anomalies detected. All questions grounded with acceptable RAGAS scores.
