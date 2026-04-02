# AB-03 — 04_complex_manufacturing — Run Analysis

**Timestamp:** 2026-03-31 00:53:25  
**Run tag:** `v5`

## Configuration

| Parameter | Value |
|-----------|-------|
| Extraction model | `LLM (gpt-5.4-nano-2026-03-17)` |
| Reasoning model | `gpt-5.4-2026-03-05` |
| Embedding model | `BAAI/bge-m3` |
| Retrieval mode | `hybrid` |
| Reranker | `False` |
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
| Avg Top Score | 5.5981 |
| Avg Chunk Count | 12.0 |
| Abstained | 0 |

## RAGAS Metrics

RAGAS evaluation not enabled for this run.

## Per-Question Deep Dive

### ✅ QA-001 — What information is stored about products in the manufacturing system?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 3.3566 | **Gate:** `proceed`

**Expected answer:**
> Products are tracked with a unique identifier (product_id), descriptive name (product_name), classification as finished good, assembly, or component (product_type), optional parent product reference for hierarchical structures (parent_product_id), standard unit cost (base_cost), typical procurement …

**System answer:**
> The manufacturing system stores products as manufactured items that can be finished goods, assemblies, or components. In the `product` table, each product has a `product_id` as the unique identifier, `product_name`, `product_type`, `parent_product_id`, `base_cost`, `lead_time_days`, and `is_active`.

From the schema and glossary together, the information captured about products includes their uniq…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_3`, `parent_chunk_data_dictionary.md_5`, `parent_chunk_data_dictionary.md_7`, `parent_chunk_data_dictionary.md_6`, `Actual stock levels of components and products at specific warehouse locations→INVENTORY`, `Actual stock levels of components and products at specific warehouse locations→WAREHOUSE`, `Manufacturing Routing→ROUTE`, `parent_chunk_business_glossary.md_0`

**Context previews (first 3):**

1. _# Manufacturing Data Dictionary  This data dictionary documents the database schema for the manufacturing supply chain system. It includes all tables, columns, data types, constraints, and relationshi…_

2. _## warehouse  Stores physical storage location information for inventory management.  | Column | Data Type | Constraints | Description | |--------|-----------|-------------|-------------| | warehouse_…_

3. _## specification  Defines technical requirements and acceptance criteria for materials and products.  | Column | Data Type | Constraints | Description | |--------|-----------|-------------|-----------…_

---

### ✅ QA-002 — How are components defined in the manufacturing database?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 3.9124 | **Gate:** `proceed`

**Expected answer:**
> Components are defined with a unique identifier (component_id), descriptive name (component_name), category grouping (component_category), unit of measure (unit_of_measure), standard unit cost (standard_cost), and optional reference to technical specifications (specification_id). Components represen…

**System answer:**
> Components are defined in two closely related ways in the retrieved context.

In the business glossary, a Component is defined as an atomic raw material or purchased part that cannot be further broken down into simpler manufactured items. Components are the building blocks used in manufacturing and are procured from external suppliers.

In the schema, components are also reflected through the Prod…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_3`, `parent_chunk_data_dictionary.md_4`, `parent_chunk_data_dictionary.md_7`, `parent_chunk_data_dictionary.md_5`, `parent_chunk_data_dictionary.md_6`, `Actual stock levels of components and products at specific warehouse locations→INVENTORY`, `Actual stock levels of components and products at specific warehouse locations→WAREHOUSE`, `parent_chunk_business_glossary.md_0`

**Context previews (first 3):**

1. _# Manufacturing Data Dictionary  This data dictionary documents the database schema for the manufacturing supply chain system. It includes all tables, columns, data types, constraints, and relationshi…_

2. _## bom  Bill of Materials defining product composition and hierarchical structure. Supports recursive relationships for multi-level assemblies.  | Column | Data Type | Constraints | Description | |---…_

3. _## specification  Defines technical requirements and acceptance criteria for materials and products.  | Column | Data Type | Constraints | Description | |--------|-----------|-------------|-----------…_

---

### ✅ QA-003 — What is the purpose of the Bill of Materials (BOM) table?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 5.4182 | **Gate:** `proceed`

**Expected answer:**
> The BOM table defines the hierarchical structure of products by specifying which components or sub-assemblies are required to manufacture each parent product. It records the unique BOM entry identifier (bom_id), parent product being built (parent_product_id), component or sub-assembly product (compo…

**System answer:**
> The Bill of Materials (`bom`) table defines product composition and hierarchical structure. It records which component products go into a parent product, including the required quantity, unit of measure, hierarchy depth (`bom_level`), and whether a component is optional. Because both `parent_product_id` and `component_product_id` reference `product(product_id)`, it supports recursive, multi-level …

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_4`, `parent_chunk_data_dictionary.md_8`, `parent_chunk_data_dictionary.md_3`, `parent_chunk_data_dictionary.md_7`, `BOM entry→BOM`, `BOM→PRODUCT`, `parent_chunk_business_glossary.md_0`, `parent_chunk_business_glossary.md_2`

**Context previews (first 3):**

1. _## bom  Bill of Materials defining product composition and hierarchical structure. Supports recursive relationships for multi-level assemblies.  | Column | Data Type | Constraints | Description | |---…_

2. _## shipment  Tracks material transfers between warehouses, suppliers, and customers.  | Column | Data Type | Constraints | Description | |--------|-----------|-------------|-------------| | shipment_i…_

3. _# Manufacturing Data Dictionary  This data dictionary documents the database schema for the manufacturing supply chain system. It includes all tables, columns, data types, constraints, and relationshi…_

---

### ✅ QA-004 — What supplier information does the system maintain?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 3.4034 | **Gate:** `proceed`

**Expected answer:**
> Suppliers are tracked with a unique identifier (supplier_id), legal business name (supplier_name), primary contact email (contact_email), primary contact phone number (contact_phone), performance rating from 1.0 to 5.0 (rating), and preferred supplier status flag (is_preferred).

**System answer:**
> The system maintains supplier master data in the `SUPPLIER` table and supplier-related associations in other tables.

At the supplier master level, `SUPPLIER` stores external vendor information for component procurement. From the retrieved context, the maintained supplier attributes are `supplier_id`, `supplier_name`, `contact_email`, `contact_phone`, `rating`, and `is_preferred`. `supplier_id` is…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_8`, `parent_chunk_data_dictionary.md_4`, `parent_chunk_data_dictionary.md_3`, `Preferred supplier for this component→SUPPLIER`, `shipment type, source and destination locations, dates for ship, estimated arrival, and actual delivery, along with current status→SHIPMENT`, `Component Supplier Relationship→COMPONENT_SUPPLIER`, `SHIPMENT→SUPPLIER`, `COMPONENT_SUPPLIER→SUPPLIER`

**Context previews (first 3):**

1. _## shipment  Tracks material transfers between warehouses, suppliers, and customers.  | Column | Data Type | Constraints | Description | |--------|-----------|-------------|-------------| | shipment_i…_

2. _## bom  Bill of Materials defining product composition and hierarchical structure. Supports recursive relationships for multi-level assemblies.  | Column | Data Type | Constraints | Description | |---…_

3. _# Manufacturing Data Dictionary  This data dictionary documents the database schema for the manufacturing supply chain system. It includes all tables, columns, data types, constraints, and relationshi…_

---

### ✅ QA-005 — How are warehouses represented in the schema?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 1.9095 | **Gate:** `proceed`

**Expected answer:**
> Warehouses are defined with a unique identifier (warehouse_id), descriptive name (warehouse_name), full street address (address), city location (city), state or province (state), total storage capacity in cubic meters (capacity), and optional manager identifier (manager_id).

**System answer:**
> Warehouses are represented as a `warehouse` entity/table identified by `warehouse_id`. The retrieved context does not include the full `warehouse` table column definition, but it does show that `shipment.warehouse_id` is a foreign key to `warehouse(warehouse_id)`, which confirms the table exists in the schema and that `warehouse_id` is its key.

From the business glossary/context, a Warehouse is a…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_8`, `parent_chunk_data_dictionary.md_3`, `parent_chunk_data_dictionary.md_4`, `parent_chunk_business_glossary.md_1`, `Actual stock levels of components and products at specific warehouse locations`, `parent_chunk_business_glossary.md_0`, `parent_chunk_business_glossary.md_2`, `Manufacturing Routing`

**Context previews (first 3):**

1. _## shipment  Tracks material transfers between warehouses, suppliers, and customers.  | Column | Data Type | Constraints | Description | |--------|-----------|-------------|-------------| | shipment_i…_

2. _# Manufacturing Data Dictionary  This data dictionary documents the database schema for the manufacturing supply chain system. It includes all tables, columns, data types, constraints, and relationshi…_

3. _## bom  Bill of Materials defining product composition and hierarchical structure. Supports recursive relationships for multi-level assemblies.  | Column | Data Type | Constraints | Description | |---…_

---

### ✅ QA-006 — What does the inventory table track?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 3.6966 | **Gate:** `proceed`

**Expected answer:**
> The inventory table tracks real-time stock levels including a unique record identifier (inventory_id), warehouse location (warehouse_id), component identifier for materials (component_id) or product identifier for finished goods (product_id), current physical stock quantity (quantity_on_hand), quant…

**System answer:**
> The `inventory` table tracks stock levels of components and products at specific warehouse locations. It records the warehouse via `warehouse_id` and then references either a component through `component_id` or a product through `product_id`—the context states these are exclusive, so a single inventory record supports either a component or a product, not both.

It specifically tracks the actual st…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_8`, `parent_chunk_data_dictionary.md_3`, `parent_chunk_data_dictionary.md_4`, `parent_chunk_data_dictionary.md_5`, `parent_chunk_data_dictionary.md_7`, `parent_chunk_data_dictionary.md_6`, `Actual stock levels of components and products at specific warehouse locations→INVENTORY`, `parent_chunk_business_glossary.md_1`

**Context previews (first 3):**

1. _## shipment  Tracks material transfers between warehouses, suppliers, and customers.  | Column | Data Type | Constraints | Description | |--------|-----------|-------------|-------------| | shipment_i…_

2. _# Manufacturing Data Dictionary  This data dictionary documents the database schema for the manufacturing supply chain system. It includes all tables, columns, data types, constraints, and relationshi…_

3. _## bom  Bill of Materials defining product composition and hierarchical structure. Supports recursive relationships for multi-level assemblies.  | Column | Data Type | Constraints | Description | |---…_

---

### ✅ QA-007 — How are work orders structured in the manufacturing system?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 4.4898 | **Gate:** `proceed`

**Expected answer:**
> Work orders represent production jobs with a unique identifier (work_order_id), product to be manufactured (product_id), optional parent work order for nested hierarchies (parent_work_order), quantity to produce (quantity_ordered), quantity completed so far (quantity_completed), current status (PEND…

**System answer:**
> Work orders are represented by the `work_order` table and are used for hierarchical production planning and tracking. Each work order is a production job for manufacturing a specific product, identified by `work_order_id` as the primary key.

A work order is structured around these fields: `product_id`, which is required and references `product(product_id)` to identify the product to manufacture; …

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_8`, `parent_chunk_data_dictionary.md_6`, `parent_chunk_data_dictionary.md_3`, `parent_chunk_data_dictionary.md_7`, `Hierarchical production planning and tracking→WORK_ORDER`, `Manufacturing Routing→ROUTE`, `WORK_ORDER→WAREHOUSE`, `WORK_ORDER→WORK_ORDER`

**Context previews (first 3):**

1. _## shipment  Tracks material transfers between warehouses, suppliers, and customers.  | Column | Data Type | Constraints | Description | |--------|-----------|-------------|-------------| | shipment_i…_

2. _## work_order  Represents production jobs for manufacturing products with hierarchical work order support.  | Column | Data Type | Constraints | Description | |--------|-----------|-------------|-----…_

3. _# Manufacturing Data Dictionary  This data dictionary documents the database schema for the manufacturing supply chain system. It includes all tables, columns, data types, constraints, and relationshi…_

---

### ✅ QA-008 — What information is captured in the shipment table?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 5.7939 | **Gate:** `proceed`

**Expected answer:**
> Shipments track material transfers with a unique identifier (shipment_id), shipment type (INBOUND from suppliers, OUTBOUND to customers, INTERNAL between warehouses), destination warehouse (warehouse_id), source supplier for inbound (supplier_id), destination customer for outbound (customer_id), shi…

**System answer:**
> The `shipment` table captures material transfer information for movements between warehouses, suppliers, and customers. It implements the business concept of “shipment type, source and destination locations, dates for ship, estimated arrival, and actual delivery, along with current status.”

Specifically, it stores `shipment_id` as the unique shipment identifier; `shipment_type` as the shipment ca…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_8`, `parent_chunk_data_dictionary.md_4`, `parent_chunk_data_dictionary.md_5`, `shipment type, source and destination locations, dates for ship, estimated arrival, and actual delivery, along with current status→SHIPMENT`, `SHIPMENT→SUPPLIER`, `SHIPMENT→WAREHOUSE`, `parent_chunk_business_glossary.md_1`, `parent_chunk_business_glossary.md_0`

**Context previews (first 3):**

1. _## shipment  Tracks material transfers between warehouses, suppliers, and customers.  | Column | Data Type | Constraints | Description | |--------|-----------|-------------|-------------| | shipment_i…_

2. _## bom  Bill of Materials defining product composition and hierarchical structure. Supports recursive relationships for multi-level assemblies.  | Column | Data Type | Constraints | Description | |---…_

3. _## warehouse  Stores physical storage location information for inventory management.  | Column | Data Type | Constraints | Description | |--------|-----------|-------------|-------------| | warehouse_…_

---

### ✅ QA-009 — How does the quality control system record inspections?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 8.5086 | **Gate:** `proceed`

**Expected answer:**
> Quality control records are stored with a unique identifier (qc_id), associated production batch (batch_id), applicable specification requirements (specification_id), inspection date (qc_date), inspection type (INCOMING for supplier materials, IN_PROCESS during manufacturing, FINAL for finished good…

**System answer:**
> The quality control system records inspections in the physical table QUALITY_CONTROL, which implements the business concept “inspection and testing records for quality assurance.”

An inspection record includes these columns: qc_id, batch_id, specification_id, qc_date, qc_type, inspector_id, result, defect_count, and notes. From the business description, this means each QC record captures a unique…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_6`, `parent_chunk_data_dictionary.md_3`, `inspection and testing records for quality assurance→QUALITY_CONTROL`, `BOM→PRODUCT`, `INVENTORY→PRODUCT`, `INVENTORY→COMPONENT`, `INVENTORY→WAREHOUSE`, `WORK_ORDER→WAREHOUSE`

**Context previews (first 3):**

1. _## work_order  Represents production jobs for manufacturing products with hierarchical work order support.  | Column | Data Type | Constraints | Description | |--------|-----------|-------------|-----…_

2. _# Manufacturing Data Dictionary  This data dictionary documents the database schema for the manufacturing supply chain system. It includes all tables, columns, data types, constraints, and relationshi…_

3. _Business concept 'inspection and testing records for quality assurance' is implemented by physical table QUALITY_CONTROL (columns: qc_id, batch_id, specification_id, qc_date, qc_type, inspector_id, re…_

---

### ✅ QA-010 — What do specification records define?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 1.4606 | **Gate:** `proceed`

**Expected answer:**
> Specifications define technical requirements with a unique identifier (specification_id), descriptive name (specification_name), version number, effective date, specification type (DIMENSIONAL, MATERIAL, PERFORMANCE), critical parameter being measured (critical_parameter), acceptable minimum value (…

**System answer:**
> Specification records define the technical requirements and acceptance criteria for materials and products. In the `SPECIFICATION` table, they include the specification name and version, effective date, specification type (`DIMENSIONAL`, `MATERIAL`, `PERFORMANCE`), the critical parameter being tested, acceptable minimum and maximum values, and the unit of measure. These records serve as the techni…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_6`, `parent_chunk_data_dictionary.md_7`, `parent_chunk_data_dictionary.md_3`, `inspection and testing records for quality assurance→QUALITY_CONTROL`, `Technical specification reference→SPECIFICATION`, `Manufacturing Routing→ROUTE`, `inspection and testing records for quality assurance`, `parent_chunk_business_glossary.md_2`

**Context previews (first 3):**

1. _## work_order  Represents production jobs for manufacturing products with hierarchical work order support.  | Column | Data Type | Constraints | Description | |--------|-----------|-------------|-----…_

2. _## specification  Defines technical requirements and acceptance criteria for materials and products.  | Column | Data Type | Constraints | Description | |--------|-----------|-------------|-----------…_

3. _# Manufacturing Data Dictionary  This data dictionary documents the database schema for the manufacturing supply chain system. It includes all tables, columns, data types, constraints, and relationshi…_

---

### ✅ QA-011 — How can I find which suppliers provide specific components?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 1.1881 | **Gate:** `proceed`

**Expected answer:**
> Query the component_supplier table which links components to their approved suppliers. This table contains the component identifier (component_id), supplier identifier (supplier_id), preferred supplier flag (is_preferred), lead time in days (lead_time_days), and unit price (unit_price). Join with th…

**System answer:**
> From the retrieved context, the schema does not show a direct supplier-to-component relationship table, so you cannot definitively identify “which suppliers provide specific components” from the provided tables alone.

What the context does show is this:

The `supplier` table stores external vendor information “for component procurement.” The `shipment` table links suppliers through `shipment.supp…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_5`, `parent_chunk_data_dictionary.md_4`, `parent_chunk_data_dictionary.md_3`, `parent_chunk_data_dictionary.md_8`, `parent_chunk_data_dictionary.md_6`, `Actual stock levels of components and products at specific warehouse locations→INVENTORY`, `Actual stock levels of components and products at specific warehouse locations→WAREHOUSE`, `inspection and testing records for quality assurance→QUALITY_CONTROL`

**Context previews (first 3):**

1. _## warehouse  Stores physical storage location information for inventory management.  | Column | Data Type | Constraints | Description | |--------|-----------|-------------|-------------| | warehouse_…_

2. _## bom  Bill of Materials defining product composition and hierarchical structure. Supports recursive relationships for multi-level assemblies.  | Column | Data Type | Constraints | Description | |---…_

3. _# Manufacturing Data Dictionary  This data dictionary documents the database schema for the manufacturing supply chain system. It includes all tables, columns, data types, constraints, and relationshi…_

---

### ✅ QA-012 — How do I trace which components are needed to fulfill a work order?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 3.6608 | **Gate:** `proceed`

**Expected answer:**
> Start with the work_order table to get the product_id being manufactured. Join to the bom table using product_id as parent_product_id to find all direct components and sub-assemblies. For each component_product_id, if it is an ASSEMBLY type product, recursively query the bom table again to explode m…

**System answer:**
> To trace the components needed for a work order, start from `work_order.product_id`, because the `work_order` table identifies the product being manufactured.

The schema path is:

`work_order.product_id` → `product.product_id` → `bom.parent_product_id`

From `bom`, the needed components are listed in `component_product_id`, along with:
`quantity` as the required amount,
`unit_of_measure`,
`bom_le…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_6`, `parent_chunk_data_dictionary.md_8`, `parent_chunk_data_dictionary.md_3`, `parent_chunk_data_dictionary.md_7`, `parent_chunk_data_dictionary.md_5`, `parent_chunk_data_dictionary.md_4`, `parent_chunk_business_glossary.md_1`, `parent_chunk_business_glossary.md_0`

**Context previews (first 3):**

1. _## work_order  Represents production jobs for manufacturing products with hierarchical work order support.  | Column | Data Type | Constraints | Description | |--------|-----------|-------------|-----…_

2. _## shipment  Tracks material transfers between warehouses, suppliers, and customers.  | Column | Data Type | Constraints | Description | |--------|-----------|-------------|-------------| | shipment_i…_

3. _# Manufacturing Data Dictionary  This data dictionary documents the database schema for the manufacturing supply chain system. It includes all tables, columns, data types, constraints, and relationshi…_

---

### ✅ QA-013 — How can I identify which warehouses have available inventory for specific components?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 4.9632 | **Gate:** `proceed`

**Expected answer:**
> Query the inventory table filtered by component_id, joining with the warehouse table to get warehouse names and locations. Calculate available quantity as quantity_on_hand minus quantity_reserved. Filter for records where available quantity is greater than zero. Results show warehouse names, locatio…

**System answer:**
> Use the `inventory` table as the starting point. The retrieved context explicitly maps the business concept “Actual stock levels of components and products at specific warehouse locations” to `INVENTORY`, with columns `inventory_id`, `warehouse_id`, `component_id`, `product_id`, `quantity_on_hand`, `quantity_reserved`, `reorder_threshold`, and `last_restock_date`.

To identify which warehouses hol…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_5`, `parent_chunk_data_dictionary.md_3`, `parent_chunk_data_dictionary.md_8`, `parent_chunk_data_dictionary.md_6`, `parent_chunk_data_dictionary.md_4`, `parent_chunk_data_dictionary.md_7`, `Actual stock levels of components and products at specific warehouse locations→INVENTORY`, `parent_chunk_business_glossary.md_1`

**Context previews (first 3):**

1. _## warehouse  Stores physical storage location information for inventory management.  | Column | Data Type | Constraints | Description | |--------|-----------|-------------|-------------| | warehouse_…_

2. _# Manufacturing Data Dictionary  This data dictionary documents the database schema for the manufacturing supply chain system. It includes all tables, columns, data types, constraints, and relationshi…_

3. _## shipment  Tracks material transfers between warehouses, suppliers, and customers.  | Column | Data Type | Constraints | Description | |--------|-----------|-------------|-------------| | shipment_i…_

---

### ✅ QA-014 — How do I find which shipments delivered materials from a specific supplier?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 2.6639 | **Gate:** `proceed`

**Expected answer:**
> Query the shipment table filtering by supplier_id and shipment_type = 'INBOUND'. Join with the warehouse table to show destination warehouses. Filter for status = 'DELIVERED' and include actual_arrival date. Results can be ordered by ship_date descending to show most recent deliveries first.

**System answer:**
> Use the `shipment` table. It is the table that “tracks material transfers between warehouses, suppliers, and customers,” and it contains the fields needed to identify shipments from a supplier and whether they were delivered.

To find shipments delivered from a specific supplier, use this schema logic:

Join/filter on `shipment.supplier_id` for the supplier you want. The `shipment` table has `supp…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_3`, `parent_chunk_data_dictionary.md_8`, `parent_chunk_data_dictionary.md_5`, `parent_chunk_data_dictionary.md_4`, `parent_chunk_data_dictionary.md_7`, `parent_chunk_data_dictionary.md_6`, `Preferred supplier for this component→SUPPLIER`, `parent_chunk_business_glossary.md_1`

**Context previews (first 3):**

1. _# Manufacturing Data Dictionary  This data dictionary documents the database schema for the manufacturing supply chain system. It includes all tables, columns, data types, constraints, and relationshi…_

2. _## shipment  Tracks material transfers between warehouses, suppliers, and customers.  | Column | Data Type | Constraints | Description | |--------|-----------|-------------|-------------| | shipment_i…_

3. _## warehouse  Stores physical storage location information for inventory management.  | Column | Data Type | Constraints | Description | |--------|-----------|-------------|-------------| | warehouse_…_

---

### ✅ QA-015 — How can I determine which quality control inspections were performed on a specific production batch?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 5.4013 | **Gate:** `proceed`

**Expected answer:**
> Query the quality_control table filtered by batch_id. Join with the specification table to get requirement details (specification_name, spec_type, acceptable ranges). Include qc_date, qc_type (INCOMING, IN_PROCESS, FINAL), result (PASS, FAIL, CONDITIONAL), and defect_count. This shows the complete i…

**System answer:**
> Use the `quality_control` records for that batch. In the retrieved context, QC inspections are associated with specific production batches, and the `quality_control` table includes `qc_id` as the unique inspection identifier and `batch_id` as the batch reference.

So, schema-wise, you determine the inspections performed on a specific production batch by filtering `quality_control.batch_id` to the …

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_6`, `parent_chunk_data_dictionary.md_8`, `parent_chunk_data_dictionary.md_3`, `parent_chunk_data_dictionary.md_5`, `parent_chunk_business_glossary.md_2`, `parent_chunk_business_glossary.md_0`, `parent_chunk_business_glossary.md_1`, `Batches for traceability and inventory management`

**Context previews (first 3):**

1. _## work_order  Represents production jobs for manufacturing products with hierarchical work order support.  | Column | Data Type | Constraints | Description | |--------|-----------|-------------|-----…_

2. _## shipment  Tracks material transfers between warehouses, suppliers, and customers.  | Column | Data Type | Constraints | Description | |--------|-----------|-------------|-------------| | shipment_i…_

3. _# Manufacturing Data Dictionary  This data dictionary documents the database schema for the manufacturing supply chain system. It includes all tables, columns, data types, constraints, and relationshi…_

---

### ✅ QA-016 — How do I track which work orders are in progress at a specific warehouse?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 4.3892 | **Gate:** `proceed`

**Expected answer:**
> Query the work_order table filtering by warehouse_id and status = 'IN_PROGRESS'. Join with the product table to get product names and types. Include quantity_ordered, quantity_completed, priority, planned_end_date, and calculate progress percentage as (quantity_completed / quantity_ordered * 100). O…

**System answer:**
> Use the `work_order` table as the primary source. It represents production jobs and includes both the work order status and the production location.

To identify work orders that are currently in progress at a specific warehouse, filter `work_order` on:
`status = 'IN_PROGRESS'`
and
`warehouse_id = <specific warehouse_id>`.

The relevant columns in `work_order` are:
`work_order_id` for the job iden…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_8`, `parent_chunk_data_dictionary.md_6`, `parent_chunk_data_dictionary.md_5`, `parent_chunk_data_dictionary.md_3`, `parent_chunk_data_dictionary.md_7`, `Actual stock levels of components and products at specific warehouse locations→INVENTORY`, `parent_chunk_business_glossary.md_1`, `Actual stock levels of components and products at specific warehouse locations`

**Context previews (first 3):**

1. _## shipment  Tracks material transfers between warehouses, suppliers, and customers.  | Column | Data Type | Constraints | Description | |--------|-----------|-------------|-------------| | shipment_i…_

2. _## work_order  Represents production jobs for manufacturing products with hierarchical work order support.  | Column | Data Type | Constraints | Description | |--------|-----------|-------------|-----…_

3. _## warehouse  Stores physical storage location information for inventory management.  | Column | Data Type | Constraints | Description | |--------|-----------|-------------|-------------| | warehouse_…_

---

### ✅ QA-017 — How can I find which components need reordering based on current inventory levels?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 3.6537 | **Gate:** `proceed`

**Expected answer:**
> Query the inventory table and filter where quantity_on_hand minus quantity_reserved is less than reorder_threshold. Join with the component table to get component names, categories, and standard costs. Join with the warehouse table for location information. Results identify which components are belo…

**System answer:**
> Use the `inventory` table, which implements the business concept “Actual stock levels of components and products at specific warehouse locations.” For component reordering, look only at inventory records where `component_id` is populated, because the schema says each inventory row supports either a `component_id` or a `product_id` record, not both.

The relevant columns are `component_id`, `wareho…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_5`, `parent_chunk_data_dictionary.md_3`, `parent_chunk_data_dictionary.md_6`, `parent_chunk_data_dictionary.md_8`, `parent_chunk_data_dictionary.md_7`, `parent_chunk_data_dictionary.md_4`, `Actual stock levels of components and products at specific warehouse locations→INVENTORY`, `parent_chunk_business_glossary.md_0`

**Context previews (first 3):**

1. _## warehouse  Stores physical storage location information for inventory management.  | Column | Data Type | Constraints | Description | |--------|-----------|-------------|-------------| | warehouse_…_

2. _# Manufacturing Data Dictionary  This data dictionary documents the database schema for the manufacturing supply chain system. It includes all tables, columns, data types, constraints, and relationshi…_

3. _## work_order  Represents production jobs for manufacturing products with hierarchical work order support.  | Column | Data Type | Constraints | Description | |--------|-----------|-------------|-----…_

---

### ✅ QA-018 — How do I determine the manufacturing route for a specific product?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 3.1571 | **Gate:** `proceed`

**Expected answer:**
> Query the route table filtering by product_id, ordered by sequence_number ascending. For each operation, retrieve operation_name, work_center, cycle_time_minutes, and setup_time_minutes. Join with the product table to get product details. The sequence of operations shows the complete manufacturing w…

**System answer:**
> To determine the manufacturing route for a specific product, use the product’s `product_id` as the key. The retrieved context says the manufacturing routing table is keyed by `route_id` and `product_id`, and it stores the ordered production steps for a product, including `route_name`, `sequence_number`, `operation_name`, `work_center`, and timing fields.

At the schema level, the path is:

`produc…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_3`, `parent_chunk_data_dictionary.md_7`, `parent_chunk_data_dictionary.md_8`, `parent_chunk_data_dictionary.md_6`, `parent_chunk_data_dictionary.md_4`, `Actual stock levels of components and products at specific warehouse locations→INVENTORY`, `parent_chunk_business_glossary.md_2`, `Manufacturing Routing`

**Context previews (first 3):**

1. _# Manufacturing Data Dictionary  This data dictionary documents the database schema for the manufacturing supply chain system. It includes all tables, columns, data types, constraints, and relationshi…_

2. _## specification  Defines technical requirements and acceptance criteria for materials and products.  | Column | Data Type | Constraints | Description | |--------|-----------|-------------|-----------…_

3. _## shipment  Tracks material transfers between warehouses, suppliers, and customers.  | Column | Data Type | Constraints | Description | |--------|-----------|-------------|-------------| | shipment_i…_

---

### ✅ QA-019 — How can I find which batches are stored at a specific warehouse and their QC status?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 5.3079 | **Gate:** `proceed`

**Expected answer:**
> Query the batch table filtering by warehouse_id. Join with the product table to get product names and types. Include production_date, quantity_produced, expiry_date, and qc_status (PENDING, PASSED, FAILED, QUARANTINED). Filter by qc_status to isolate batches requiring quality attention or ready for …

**System answer:**
> Use the `batch` table as the starting point, because it stores both the warehouse reference and the batch-level QC status.

At the schema level, the path is:
`warehouse.warehouse_id` → `batch.warehouse_id`

The `batch` table includes:
`batch_id` as the batch identifier,
`product_id` for the produced product,
`production_date`,
`quantity_produced`,
`warehouse_id` as the storage location,
`expiry_da…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_5`, `parent_chunk_data_dictionary.md_6`, `parent_chunk_data_dictionary.md_8`, `parent_chunk_data_dictionary.md_3`, `parent_chunk_data_dictionary.md_7`, `parent_chunk_data_dictionary.md_4`, `parent_chunk_business_glossary.md_2`, `Actual stock levels of components and products at specific warehouse locations`

**Context previews (first 3):**

1. _## warehouse  Stores physical storage location information for inventory management.  | Column | Data Type | Constraints | Description | |--------|-----------|-------------|-------------| | warehouse_…_

2. _## work_order  Represents production jobs for manufacturing products with hierarchical work order support.  | Column | Data Type | Constraints | Description | |--------|-----------|-------------|-----…_

3. _## shipment  Tracks material transfers between warehouses, suppliers, and customers.  | Column | Data Type | Constraints | Description | |--------|-----------|-------------|-------------| | shipment_i…_

---

### ✅ QA-020 — How do I identify which specifications apply to specific components?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 1.1881 | **Gate:** `proceed`

**Expected answer:**
> Query the component table and join with the specification table via specification_id. Include component_name, component_category, and specification details (specification_name, spec_type, critical_parameter, min_value, max_value, unit_of_measure). This shows the technical requirements that each comp…

**System answer:**
> From the provided context, there is no direct schema relationship that links a specification to a component.

What the context does show is this path: `specification.specification_id` is referenced by `quality_control.specification_id`, and `quality_control.batch_id` is associated with `batch.batch_id`. Then `batch.product_id` links the batch to `product.product_id`. So, from the available schema,…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_5`, `parent_chunk_data_dictionary.md_6`, `parent_chunk_data_dictionary.md_7`, `parent_chunk_data_dictionary.md_3`, `parent_chunk_data_dictionary.md_4`, `Actual stock levels of components and products at specific warehouse locations→INVENTORY`, `Actual stock levels of components and products at specific warehouse locations→WAREHOUSE`, `inspection and testing records for quality assurance→QUALITY_CONTROL`

**Context previews (first 3):**

1. _## warehouse  Stores physical storage location information for inventory management.  | Column | Data Type | Constraints | Description | |--------|-----------|-------------|-------------| | warehouse_…_

2. _## work_order  Represents production jobs for manufacturing products with hierarchical work order support.  | Column | Data Type | Constraints | Description | |--------|-----------|-------------|-----…_

3. _## specification  Defines technical requirements and acceptance criteria for materials and products.  | Column | Data Type | Constraints | Description | |--------|-----------|-------------|-----------…_

---

### ✅ QA-021 — How can I perform a complete BOM explosion to find all components required for a finished product?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 7.8744 | **Gate:** `proceed`

**Expected answer:**
> Use a recursive query starting from the product_id of the finished good. At each level, join the bom table to find component_product_id entries. For each component, check if product_type is 'ASSEMBLY' or 'FINISHED_GOOD'. If so, recursively query bom again using that component_product_id as the new p…

**System answer:**
> To perform a complete BOM explosion for a finished product, use the `bom` table as the recursive structure and the `product` table for product details.

Start with the finished product in `product`, using `product.product_id` and, if needed, `product_type = 'FINISHED_GOOD'`. Then recursively traverse `bom` by matching the current product to `bom.parent_product_id`. Each matching row gives you a di…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_3`, `parent_chunk_data_dictionary.md_8`, `parent_chunk_data_dictionary.md_4`, `parent_chunk_data_dictionary.md_6`, `parent_chunk_data_dictionary.md_7`, `parent_chunk_data_dictionary.md_5`, `parent_chunk_business_glossary.md_0`, `parent_chunk_business_glossary.md_1`

**Context previews (first 3):**

1. _# Manufacturing Data Dictionary  This data dictionary documents the database schema for the manufacturing supply chain system. It includes all tables, columns, data types, constraints, and relationshi…_

2. _## shipment  Tracks material transfers between warehouses, suppliers, and customers.  | Column | Data Type | Constraints | Description | |--------|-----------|-------------|-------------| | shipment_i…_

3. _## bom  Bill of Materials defining product composition and hierarchical structure. Supports recursive relationships for multi-level assemblies.  | Column | Data Type | Constraints | Description | |---…_

---

### ✅ QA-022 — How do I calculate the total material cost for a product including all sub-assemblies?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 8.4791 | **Gate:** `proceed`

**Expected answer:**
> Perform a recursive BOM explosion to find all leaf-level components. For each leaf component, join with the component table to get standard_cost. Multiply standard_cost by the accumulated quantity from the BOM traversal. Sum all component costs to get total material cost. This calculation must trave…

**System answer:**
> The context does not define a prebuilt formula for “total material cost,” but it does provide the schema needed to calculate it.

Use the `bom` table to recursively explode the product structure, and use `product.base_cost` as the available cost field for each item.

At schema level, the calculation path is:

`product.product_id`
→ `bom.parent_product_id`
→ `bom.component_product_id`
→ `product.pr…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_3`, `parent_chunk_data_dictionary.md_8`, `parent_chunk_data_dictionary.md_4`, `parent_chunk_data_dictionary.md_6`, `parent_chunk_data_dictionary.md_7`, `parent_chunk_business_glossary.md_0`, `Manufacturing Routing`, `parent_chunk_business_glossary.md_2`

**Context previews (first 3):**

1. _# Manufacturing Data Dictionary  This data dictionary documents the database schema for the manufacturing supply chain system. It includes all tables, columns, data types, constraints, and relationshi…_

2. _## shipment  Tracks material transfers between warehouses, suppliers, and customers.  | Column | Data Type | Constraints | Description | |--------|-----------|-------------|-------------| | shipment_i…_

3. _## bom  Bill of Materials defining product composition and hierarchical structure. Supports recursive relationships for multi-level assemblies.  | Column | Data Type | Constraints | Description | |---…_

---

### ✅ QA-023 — How can I find all parent products that contain a specific component anywhere in their BOM structure?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 11.0575 | **Gate:** `proceed`

**Expected answer:**
> Use a recursive reverse traversal of the BOM. Start with the component_id as the initial parent_product_id. Find all records where this product appears as component_product_id in the bom table. For each parent_product_id found, check if it appears as a component_product_id in other bom records (is a…

**System answer:**
> Use the `bom` table as the primary traversal path, because it explicitly models product composition: `bom.parent_product_id` is the product being built, and `bom.component_product_id` is the product that goes into it. Both columns are foreign keys to `product(product_id)`, and the context states this supports recursive multi-level assemblies.

To find every parent product that contains a specific …

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_3`, `parent_chunk_data_dictionary.md_8`, `parent_chunk_data_dictionary.md_4`, `parent_chunk_data_dictionary.md_6`, `parent_chunk_data_dictionary.md_5`, `parent_chunk_data_dictionary.md_7`, `parent_chunk_business_glossary.md_0`, `parent_chunk_business_glossary.md_1`

**Context previews (first 3):**

1. _# Manufacturing Data Dictionary  This data dictionary documents the database schema for the manufacturing supply chain system. It includes all tables, columns, data types, constraints, and relationshi…_

2. _## shipment  Tracks material transfers between warehouses, suppliers, and customers.  | Column | Data Type | Constraints | Description | |--------|-----------|-------------|-------------| | shipment_i…_

3. _## bom  Bill of Materials defining product composition and hierarchical structure. Supports recursive relationships for multi-level assemblies.  | Column | Data Type | Constraints | Description | |---…_

---

### ✅ QA-024 — How do I identify work orders that require a specific component, considering nested sub-assemblies?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 3.5906 | **Gate:** `proceed`

**Expected answer:**
> First, perform reverse BOM traversal to find all parent products that contain the target component at any level. Then query the work_order table where product_id is in the set of parent products found. This includes work orders for finished goods that contain the component indirectly through sub-ass…

**System answer:**
> Use the `bom` table as the recursive structure, then join the resolved parent products to `work_order`.

The schema path is:

`bom.component_product_id` → `bom.parent_product_id` → `work_order.product_id`

Because `bom` is recursive through the `product` table, this lets you handle nested sub-assemblies. The relevant facts are:

The `work_order` table identifies what is being manufactured through …

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_8`, `parent_chunk_data_dictionary.md_6`, `parent_chunk_data_dictionary.md_3`, `parent_chunk_data_dictionary.md_5`, `parent_chunk_data_dictionary.md_4`, `parent_chunk_data_dictionary.md_7`, `parent_chunk_business_glossary.md_1`, `parent_chunk_business_glossary.md_2`

**Context previews (first 3):**

1. _## shipment  Tracks material transfers between warehouses, suppliers, and customers.  | Column | Data Type | Constraints | Description | |--------|-----------|-------------|-------------| | shipment_i…_

2. _## work_order  Represents production jobs for manufacturing products with hierarchical work order support.  | Column | Data Type | Constraints | Description | |--------|-----------|-------------|-----…_

3. _# Manufacturing Data Dictionary  This data dictionary documents the database schema for the manufacturing supply chain system. It includes all tables, columns, data types, constraints, and relationshi…_

---

### ✅ QA-025 — How can I determine the maximum BOM depth level for any product?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 6.4376 | **Gate:** `proceed`

**Expected answer:**
> Use a recursive query on the bom table, incrementing a level counter at each traversal. Start with bom_level = 0 and add 1 for each recursive step. Track the maximum level reached across all product hierarchies. This identifies the most complex product structures with the deepest nesting.

**System answer:**
> Use the `bom` table. It is the Bill of Materials table for hierarchical product composition, and it has a `bom_level` column defined as the “depth in product hierarchy,” with the note that it “tracks depth for performance optimization.”

To determine the maximum BOM depth, take the maximum value of `bom.bom_level`.

If you want the maximum depth across the entire system, use the maximum of `bom_le…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_8`, `parent_chunk_data_dictionary.md_3`, `parent_chunk_data_dictionary.md_4`, `parent_chunk_data_dictionary.md_7`, `parent_chunk_data_dictionary.md_6`, `parent_chunk_data_dictionary.md_5`, `parent_chunk_business_glossary.md_0`, `parent_chunk_business_glossary.md_2`

**Context previews (first 3):**

1. _## shipment  Tracks material transfers between warehouses, suppliers, and customers.  | Column | Data Type | Constraints | Description | |--------|-----------|-------------|-------------| | shipment_i…_

2. _# Manufacturing Data Dictionary  This data dictionary documents the database schema for the manufacturing supply chain system. It includes all tables, columns, data types, constraints, and relationshi…_

3. _## bom  Bill of Materials defining product composition and hierarchical structure. Supports recursive relationships for multi-level assemblies.  | Column | Data Type | Constraints | Description | |---…_

---

### ✅ QA-026 — How do I find all products that have a specific product as a sub-assembly at any level?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 8.7992 | **Gate:** `proceed`

**Expected answer:**
> Perform a recursive search starting with the target product_id as the initial component_product_id in the bom table. For each parent_product_id found, check if that parent appears as a component in other bom entries. Continue recursively until reaching products that are not used as components elsewh…

**System answer:**
> Use the `bom` table as the primary hierarchy source. It is the Bill of Materials table for product composition, and both `bom.parent_product_id` and `bom.component_product_id` reference `product(product_id)`. The context explicitly says this structure supports recursive, multi-level assemblies such as Bicycle → Wheel → Spoke.

To find every product that contains a specific product as a sub-assembl…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_3`, `parent_chunk_data_dictionary.md_5`, `parent_chunk_data_dictionary.md_8`, `parent_chunk_data_dictionary.md_6`, `parent_chunk_data_dictionary.md_4`, `parent_chunk_data_dictionary.md_7`, `parent_chunk_business_glossary.md_0`, `Actual stock levels of components and products at specific warehouse locations`

**Context previews (first 3):**

1. _# Manufacturing Data Dictionary  This data dictionary documents the database schema for the manufacturing supply chain system. It includes all tables, columns, data types, constraints, and relationshi…_

2. _## warehouse  Stores physical storage location information for inventory management.  | Column | Data Type | Constraints | Description | |--------|-----------|-------------|-------------| | warehouse_…_

3. _## shipment  Tracks material transfers between warehouses, suppliers, and customers.  | Column | Data Type | Constraints | Description | |--------|-----------|-------------|-------------| | shipment_i…_

---

### ✅ QA-027 — How can I calculate the total lead time for a product including all sub-assembly lead times?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 10.7796 | **Gate:** `proceed`

**Expected answer:**
> Perform a recursive BOM explosion to find all components and sub-assemblies. For each product_id in the hierarchy, retrieve lead_time_days from the product table. The total lead time is the maximum of all lead times in the hierarchy (representing the longest dependency chain), or optionally sum lead…

**System answer:**
> Use the product structure in the schema to recursively explode the product’s hierarchy and retrieve `lead_time_days` from every related `product` row.

The relevant fields are in `product` and `bom`:

`product.product_id` is the product key, and `product.lead_time_days` is the procurement or production lead time for that product. The `product` table also has a self-reference through `parent_produc…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_3`, `parent_chunk_data_dictionary.md_4`, `parent_chunk_data_dictionary.md_8`, `parent_chunk_data_dictionary.md_7`, `parent_chunk_data_dictionary.md_6`, `parent_chunk_business_glossary.md_0`, `parent_chunk_business_glossary.md_2`, `Manufacturing Routing`

**Context previews (first 3):**

1. _# Manufacturing Data Dictionary  This data dictionary documents the database schema for the manufacturing supply chain system. It includes all tables, columns, data types, constraints, and relationshi…_

2. _## bom  Bill of Materials defining product composition and hierarchical structure. Supports recursive relationships for multi-level assemblies.  | Column | Data Type | Constraints | Description | |---…_

3. _## shipment  Tracks material transfers between warehouses, suppliers, and customers.  | Column | Data Type | Constraints | Description | |--------|-----------|-------------|-------------| | shipment_i…_

---

### ✅ QA-028 — How do I generate a complete indented BOM report showing the hierarchical structure?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 5.8818 | **Gate:** `proceed`

**Expected answer:**
> Use a recursive query on the bom table that tracks the current depth level. Start with the top-level product (parent_product_id where product has no parent_product_id). At each level, output component details indented by depth level. Include product_name, quantity, and unit_of_measure. Recursively p…

**System answer:**
> To generate a complete indented BOM report, use the `BOM` table as the primary source, because it is the table that “defines product composition and hierarchical structure” and explicitly supports recursive relationships for multi-level assemblies.

The schema path is:

`BOM.parent_product_id -> PRODUCT.product_id`
and
`BOM.component_product_id -> PRODUCT.product_id`

So for each BOM row, the pare…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_8`, `parent_chunk_data_dictionary.md_3`, `parent_chunk_data_dictionary.md_4`, `parent_chunk_data_dictionary.md_6`, `Hierarchical production planning and tracking→WORK_ORDER`, `Manufacturing Routing→ROUTE`, `BOM entry→BOM`, `BOM→PRODUCT`

**Context previews (first 3):**

1. _## shipment  Tracks material transfers between warehouses, suppliers, and customers.  | Column | Data Type | Constraints | Description | |--------|-----------|-------------|-------------| | shipment_i…_

2. _# Manufacturing Data Dictionary  This data dictionary documents the database schema for the manufacturing supply chain system. It includes all tables, columns, data types, constraints, and relationshi…_

3. _## bom  Bill of Materials defining product composition and hierarchical structure. Supports recursive relationships for multi-level assemblies.  | Column | Data Type | Constraints | Description | |---…_

---

### ✅ QA-029 — How can I find which components appear most frequently across all product BOMs?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 5.2586 | **Gate:** `proceed`

**Expected answer:**
> Perform BOM explosion for all products and aggregate occurrences of each leaf-level component. Count how many distinct product hierarchies contain each component. Join with component table for component names. Order by frequency descending to identify common components that should be prioritized for…

**System answer:**
> Use the `bom` table as the primary source, because it defines product composition with one row per parent/component relationship through `parent_product_id` and `component_product_id`.

To find which components appear most frequently across all BOMs, group BOM rows by `bom.component_product_id` and count how many times each value occurs. Because `bom` has the constraint `uq_bom_structure UNIQUE (p…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_3`, `parent_chunk_data_dictionary.md_8`, `parent_chunk_data_dictionary.md_4`, `parent_chunk_data_dictionary.md_5`, `parent_chunk_data_dictionary.md_6`, `parent_chunk_data_dictionary.md_7`, `parent_chunk_business_glossary.md_0`, `parent_chunk_business_glossary.md_1`

**Context previews (first 3):**

1. _# Manufacturing Data Dictionary  This data dictionary documents the database schema for the manufacturing supply chain system. It includes all tables, columns, data types, constraints, and relationshi…_

2. _## shipment  Tracks material transfers between warehouses, suppliers, and customers.  | Column | Data Type | Constraints | Description | |--------|-----------|-------------|-------------| | shipment_i…_

3. _## bom  Bill of Materials defining product composition and hierarchical structure. Supports recursive relationships for multi-level assemblies.  | Column | Data Type | Constraints | Description | |---…_

---

### ✅ QA-030 — How do I detect circular references in the BOM structure to prevent infinite loops?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 6.1489 | **Gate:** `proceed`

**Expected answer:**
> Use a recursive query with a cycle detection check. Track the path of visited product_ids at each recursion level. If a product_id appears twice in the same path, a circular reference exists. Alternatively, check if any bom record has parent_product_id = component_product_id (direct self-reference),…

**System answer:**
> The context does not define a built-in cycle-prevention rule, trigger, or stored procedure for circular BOM detection. But it does provide the schema structure needed to detect it.

In this schema, circular-reference risk exists because `bom` is explicitly recursive: `BOM.parent_product_id` and `BOM.component_product_id` both reference `PRODUCT.product_id`. The data dictionary says this “supports …

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_8`, `parent_chunk_data_dictionary.md_3`, `parent_chunk_data_dictionary.md_4`, `parent_chunk_data_dictionary.md_7`, `parent_chunk_data_dictionary.md_6`, `Manufacturing Routing→ROUTE`, `BOM entry→BOM`, `BOM→PRODUCT`

**Context previews (first 3):**

1. _## shipment  Tracks material transfers between warehouses, suppliers, and customers.  | Column | Data Type | Constraints | Description | |--------|-----------|-------------|-------------| | shipment_i…_

2. _# Manufacturing Data Dictionary  This data dictionary documents the database schema for the manufacturing supply chain system. It includes all tables, columns, data types, constraints, and relationshi…_

3. _## bom  Bill of Materials defining product composition and hierarchical structure. Supports recursive relationships for multi-level assemblies.  | Column | Data Type | Constraints | Description | |---…_

---

### ✅ QA-031 — How can I determine the complete supplier chain for a finished product, including suppliers for all sub-assemblies?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 9.1723 | **Gate:** `proceed`

**Expected answer:**
> First, perform recursive BOM explosion to find all leaf-level components in the product hierarchy. Then query the component_supplier table for each component_id to find approved suppliers. Join with the supplier table to get supplier names, ratings, and contact information. Include supplier-specific…

**System answer:**
> Use the product and BOM hierarchy to explode the finished good into every nested assembly and component, and then attach suppliers at the component level.

From the retrieved schema, the structural path is: start in `product` for the target finished good using `product.product_id`, where `product_type` can be `FINISHED_GOOD`. Then recursively traverse `bom`, joining `bom.parent_product_id` to the …

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_3`, `parent_chunk_data_dictionary.md_8`, `parent_chunk_data_dictionary.md_4`, `parent_chunk_data_dictionary.md_7`, `parent_chunk_business_glossary.md_0`, `Manufacturing Routing`, `parent_chunk_business_glossary.md_2`, `parent_chunk_business_glossary.md_1`

**Context previews (first 3):**

1. _# Manufacturing Data Dictionary  This data dictionary documents the database schema for the manufacturing supply chain system. It includes all tables, columns, data types, constraints, and relationshi…_

2. _## shipment  Tracks material transfers between warehouses, suppliers, and customers.  | Column | Data Type | Constraints | Description | |--------|-----------|-------------|-------------| | shipment_i…_

3. _## bom  Bill of Materials defining product composition and hierarchical structure. Supports recursive relationships for multi-level assemblies.  | Column | Data Type | Constraints | Description | |---…_

---

### ✅ QA-032 — How do I check if sufficient inventory exists across all warehouses to fulfill a work order?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 6.1464 | **Gate:** `proceed`

**Expected answer:**
> For the work_order's product_id, perform recursive BOM explosion to get all required components with quantities. For each component, sum the available quantity (quantity_on_hand - quantity_reserved) across all warehouses from the inventory table. Compare aggregated available inventory against requir…

**System answer:**
> From the retrieved context, the schema-level way to check this is to use `WORK_ORDER` and `INVENTORY`.

`WORK_ORDER` tells you what product is being manufactured and how much is needed:
`work_order.work_order_id`, `product_id`, `quantity_ordered`, `quantity_completed`, `status`, and `warehouse_id`.

`INVENTORY` stores stock by warehouse for either a product or a component:
`inventory.warehouse_id`…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_3`, `parent_chunk_data_dictionary.md_6`, `parent_chunk_data_dictionary.md_5`, `parent_chunk_data_dictionary.md_8`, `parent_chunk_data_dictionary.md_7`, `Actual stock levels of components and products at specific warehouse locations→INVENTORY`, `Hierarchical production planning and tracking→WORK_ORDER`, `parent_chunk_business_glossary.md_1`

**Context previews (first 3):**

1. _# Manufacturing Data Dictionary  This data dictionary documents the database schema for the manufacturing supply chain system. It includes all tables, columns, data types, constraints, and relationshi…_

2. _## work_order  Represents production jobs for manufacturing products with hierarchical work order support.  | Column | Data Type | Constraints | Description | |--------|-----------|-------------|-----…_

3. _## warehouse  Stores physical storage location information for inventory management.  | Column | Data Type | Constraints | Description | |--------|-----------|-------------|-------------| | warehouse_…_

---

### ✅ QA-033 — How can I find which quality control inspections failed for components from specific suppliers?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 3.1295 | **Gate:** `proceed`

**Expected answer:**
> Query the quality_control table filtering by result = 'FAIL'. Join with the batch table to get product_id and production_date. Join with the bom table recursively to trace which products contain failed components. Join with component_supplier and supplier tables to identify the source supplier. Filt…

**System answer:**
> From the retrieved context, this can only be answered partially at the schema level.

You can trace failed quality inspections to the inspected manufactured item through the QC and batch structures. The `quality_control` / `QualityControl` concept is associated with a production `batch` through `batch_id`, and the `batch` table links to the inspected item through `batch.product_id → product.produc…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_3`, `parent_chunk_data_dictionary.md_5`, `parent_chunk_data_dictionary.md_6`, `parent_chunk_data_dictionary.md_4`, `parent_chunk_data_dictionary.md_8`, `parent_chunk_data_dictionary.md_7`, `Actual stock levels of components and products at specific warehouse locations→INVENTORY`, `parent_chunk_business_glossary.md_2`

**Context previews (first 3):**

1. _# Manufacturing Data Dictionary  This data dictionary documents the database schema for the manufacturing supply chain system. It includes all tables, columns, data types, constraints, and relationshi…_

2. _## warehouse  Stores physical storage location information for inventory management.  | Column | Data Type | Constraints | Description | |--------|-----------|-------------|-------------| | warehouse_…_

3. _## work_order  Represents production jobs for manufacturing products with hierarchical work order support.  | Column | Data Type | Constraints | Description | |--------|-----------|-------------|-----…_

---

### ✅ QA-034 — How do I calculate the total manufacturing time for a work order including all sub-assembly work orders?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 8.5142 | **Gate:** `proceed`

**Expected answer:**
> Query the work_order table starting with the parent work_order. Find all child work_orders where parent_work_order matches the current work_order_id. For each work order (parent and children), join with the route table on product_id to get all operations. Sum (cycle_time_minutes * quantity) plus set…

**System answer:**
> The retrieved context does not define a calculation rule for “total manufacturing time” across a work order and its sub-assembly work orders, so I cannot state an exact formula.

What the context does provide is the schema you would use to trace the hierarchy. In `work_order`, `parent_work_order` is a self-referential foreign key to `work_order(work_order_id)`. That means a top-level work order ca…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_6`, `parent_chunk_data_dictionary.md_8`, `parent_chunk_data_dictionary.md_3`, `parent_chunk_data_dictionary.md_7`, `parent_chunk_data_dictionary.md_4`, `parent_chunk_data_dictionary.md_5`, `Actual stock levels of components and products at specific warehouse locations→INVENTORY`, `parent_chunk_business_glossary.md_1`

**Context previews (first 3):**

1. _## work_order  Represents production jobs for manufacturing products with hierarchical work order support.  | Column | Data Type | Constraints | Description | |--------|-----------|-------------|-----…_

2. _## shipment  Tracks material transfers between warehouses, suppliers, and customers.  | Column | Data Type | Constraints | Description | |--------|-----------|-------------|-------------| | shipment_i…_

3. _# Manufacturing Data Dictionary  This data dictionary documents the database schema for the manufacturing supply chain system. It includes all tables, columns, data types, constraints, and relationshi…_

---

### ✅ QA-035 — How can I identify which shipments are overdue and their impact on work orders?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 5.1636 | **Gate:** `proceed`

**Expected answer:**
> Query the shipment table filtering for status = 'SHIPPED' where actual_arrival is NULL and estimated_arrival is in the past (overdue). Join with the component_supplier table via supplier_id and component_id to identify which components are delayed. Perform reverse BOM lookup to find which parent pro…

**System answer:**
> From the retrieved context, you can identify overdue shipments only at a schema level, and you can assess their possible impact on work orders through the shared warehouse relationship.

The relevant shipment fields are in `shipment`: `shipment_id`, `shipment_type`, `warehouse_id`, `supplier_id`, `customer_id`, `ship_date`, `estimated_arrival`, `actual_arrival`, and `status`. Shipment status value…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_8`, `parent_chunk_data_dictionary.md_6`, `parent_chunk_data_dictionary.md_7`, `parent_chunk_data_dictionary.md_4`, `parent_chunk_data_dictionary.md_3`, `parent_chunk_data_dictionary.md_5`, `Hierarchical production planning and tracking→WORK_ORDER`, `Manufacturing Routing→ROUTE`

**Context previews (first 3):**

1. _## shipment  Tracks material transfers between warehouses, suppliers, and customers.  | Column | Data Type | Constraints | Description | |--------|-----------|-------------|-------------| | shipment_i…_

2. _## work_order  Represents production jobs for manufacturing products with hierarchical work order support.  | Column | Data Type | Constraints | Description | |--------|-----------|-------------|-----…_

3. _## specification  Defines technical requirements and acceptance criteria for materials and products.  | Column | Data Type | Constraints | Description | |--------|-----------|-------------|-----------…_

---

### ✅ QA-036 — How do I find which batches are approaching or past expiry and contain components from specific suppliers?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 4.8426 | **Gate:** `proceed`

**Expected answer:**
> Query the batch table filtering for expiry_date within a warning window (e.g., next 30 days) or past expiry. Join with the bom table recursively on product_id to trace all components used in those batches. Join with component_supplier and supplier tables to filter by specific suppliers. Results iden…

**System answer:**
> From the retrieved context, you can identify batches that are approaching or past expiry from the `batch` table, and you can identify the product structure of those batches through `bom` and `product`. However, the context does not define a complete relationship that ties batch contents or BOM components to specific suppliers, so that supplier-specific part cannot be fully answered from the availa…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_3`, `parent_chunk_data_dictionary.md_5`, `parent_chunk_data_dictionary.md_7`, `parent_chunk_data_dictionary.md_8`, `parent_chunk_data_dictionary.md_6`, `parent_chunk_data_dictionary.md_4`, `Actual stock levels of components and products at specific warehouse locations→INVENTORY`, `parent_chunk_business_glossary.md_2`

**Context previews (first 3):**

1. _# Manufacturing Data Dictionary  This data dictionary documents the database schema for the manufacturing supply chain system. It includes all tables, columns, data types, constraints, and relationshi…_

2. _## warehouse  Stores physical storage location information for inventory management.  | Column | Data Type | Constraints | Description | |--------|-----------|-------------|-------------| | warehouse_…_

3. _## specification  Defines technical requirements and acceptance criteria for materials and products.  | Column | Data Type | Constraints | Description | |--------|-----------|-------------|-----------…_

---

### ✅ QA-037 — How can I generate a material requirements plan showing when to order components based on work order schedules?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 11.8210 | **Gate:** `proceed`

**Expected answer:**
> Query all work_orders with status 'PENDING' ordered by planned_start_date. For each work_order, perform BOM explosion to get required components and quantities. For each component, query inventory for current available stock across warehouses. Calculate net requirements = (required quantity * work_o…

**System answer:**
> From the retrieved schema, you can derive an MRP-style plan by using the work order schedule as demand, exploding the BOM to component requirements, checking inventory, and offsetting need dates by each component’s lead time.

The join path is: `work_order.product_id -> bom.parent_product_id` to find what each scheduled work order consumes; then `bom.component_product_id -> product.product_id` to …

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_6`, `parent_chunk_data_dictionary.md_8`, `parent_chunk_data_dictionary.md_3`, `parent_chunk_data_dictionary.md_7`, `parent_chunk_data_dictionary.md_4`, `parent_chunk_data_dictionary.md_5`, `parent_chunk_business_glossary.md_1`, `parent_chunk_business_glossary.md_0`

**Context previews (first 3):**

1. _## work_order  Represents production jobs for manufacturing products with hierarchical work order support.  | Column | Data Type | Constraints | Description | |--------|-----------|-------------|-----…_

2. _## shipment  Tracks material transfers between warehouses, suppliers, and customers.  | Column | Data Type | Constraints | Description | |--------|-----------|-------------|-------------| | shipment_i…_

3. _# Manufacturing Data Dictionary  This data dictionary documents the database schema for the manufacturing supply chain system. It includes all tables, columns, data types, constraints, and relationshi…_

---

### ✅ QA-038 — How do I trace the complete genealogy of a component from supplier through batch to finished goods?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 6.7981 | **Gate:** `proceed`

**Expected answer:**
> Start with a shipment from the supplier (shipment table with supplier_id and shipment_type = 'INBOUND'). Track to inventory updates via component_id and warehouse_id. Identify batches that consumed the component via reverse BOM lookup (batch.product_id → bom hierarchy → component_id). Query quality_…

**System answer:**
> From the retrieved context, you can describe the genealogy at the schema level, but you cannot fully execute a complete end-to-end trace because some required links are not provided.

For the supplier side, the procurement relationship starts with `supplier.supplier_id` and the component-supplier junction entity described as the “Component Supplier Relationship.” That junction links one `component…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_3`, `parent_chunk_data_dictionary.md_8`, `parent_chunk_data_dictionary.md_4`, `parent_chunk_data_dictionary.md_5`, `parent_chunk_business_glossary.md_0`, `parent_chunk_business_glossary.md_1`, `Component Supplier Relationship`, `parent_chunk_business_glossary.md_2`

**Context previews (first 3):**

1. _# Manufacturing Data Dictionary  This data dictionary documents the database schema for the manufacturing supply chain system. It includes all tables, columns, data types, constraints, and relationshi…_

2. _## shipment  Tracks material transfers between warehouses, suppliers, and customers.  | Column | Data Type | Constraints | Description | |--------|-----------|-------------|-------------| | shipment_i…_

3. _## bom  Bill of Materials defining product composition and hierarchical structure. Supports recursive relationships for multi-level assemblies.  | Column | Data Type | Constraints | Description | |---…_

---

### ✅ QA-039 — How can I find alternative suppliers for components that are critical for multiple products?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 5.4321 | **Gate:** `proceed`

**Expected answer:**
> Perform BOM explosion for all active products and count component usage frequency. Identify high-frequency components. Query component_supplier table to find all suppliers for these components. Filter to suppliers with rating >= 4.0 (high quality) and is_preferred = 'Y'. For each component, list alt…

**System answer:**
> You can answer this only partially from the retrieved context.

To find components that matter to multiple products, the key table is `bom`. It defines product composition with `parent_product_id` as the product being built and `component_product_id` as the product that goes into it. Both columns reference `product(product_id)`, so the schema supports tracing shared components across assemblies. T…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_3`, `parent_chunk_data_dictionary.md_4`, `parent_chunk_data_dictionary.md_8`, `parent_chunk_data_dictionary.md_6`, `parent_chunk_data_dictionary.md_5`, `parent_chunk_data_dictionary.md_7`, `Actual stock levels of components and products at specific warehouse locations→INVENTORY`, `Actual stock levels of components and products at specific warehouse locations→WAREHOUSE`

**Context previews (first 3):**

1. _# Manufacturing Data Dictionary  This data dictionary documents the database schema for the manufacturing supply chain system. It includes all tables, columns, data types, constraints, and relationshi…_

2. _## bom  Bill of Materials defining product composition and hierarchical structure. Supports recursive relationships for multi-level assemblies.  | Column | Data Type | Constraints | Description | |---…_

3. _## shipment  Tracks material transfers between warehouses, suppliers, and customers.  | Column | Data Type | Constraints | Description | |--------|-----------|-------------|-------------| | shipment_i…_

---

### ✅ QA-040 — How do I calculate the total landed cost for a product including component costs, supplier lead times, and manufacturing operations?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 11.0763 | **Gate:** `proceed`

**Expected answer:**
> Perform recursive BOM explosion to get all leaf components. For each component, query component_supplier to get unit_price from primary supplier. Multiply by accumulated BOM quantity for material cost. Add shipping costs (estimated from shipment history). Query route table for the product to get all…

**System answer:**
> The retrieved context does not define a formal “total landed cost” calculation, so I cannot give a complete supported formula. In particular, the context does not provide freight, duty, overhead, or operation cost-rate fields, and it does not define a method for converting routing timing fields into monetary cost.

What the context does provide is the structure of the inputs you can trace.

At the…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_3`, `parent_chunk_data_dictionary.md_4`, `parent_chunk_data_dictionary.md_8`, `parent_chunk_business_glossary.md_0`, `Manufacturing Routing`, `Component Supplier Relationship`, `parent_chunk_business_glossary.md_2`, `parent_chunk_business_glossary.md_1`

**Context previews (first 3):**

1. _# Manufacturing Data Dictionary  This data dictionary documents the database schema for the manufacturing supply chain system. It includes all tables, columns, data types, constraints, and relationshi…_

2. _## bom  Bill of Materials defining product composition and hierarchical structure. Supports recursive relationships for multi-level assemblies.  | Column | Data Type | Constraints | Description | |---…_

3. _## shipment  Tracks material transfers between warehouses, suppliers, and customers.  | Column | Data Type | Constraints | Description | |--------|-----------|-------------|-------------| | shipment_i…_

---

## Anomalies & Observations

No anomalies detected. All questions grounded with acceptable RAGAS scores.
