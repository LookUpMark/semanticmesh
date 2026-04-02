# AB-08 — 04_complex_manufacturing — Run Analysis

**Timestamp:** 2026-03-31 19:23:30  
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
| Chunk size / overlap | `512 / 64` |
| ER similarity threshold | `0.75` |

## Builder Results

| Metric | Value |
|--------|-------|
| Triplets extracted | 416 |
| Entities resolved | 129 |
| Tables parsed | 13 |
| Tables completed | 13 |

## Query Evaluation Summary

| Metric | Value |
|--------|-------|
| Questions | 40 |
| Grounded | **40/40 (100%)** |
| Avg GT Coverage | 100% |
| Avg Top Score | 0.4324 |
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
> In the manufacturing system, the `PRODUCT` table stores information about all manufactured items, including finished goods, assemblies, and components.

The retrieved schema shows these stored product attributes: `product_id`, which is the unique product identifier and primary key; `product_name`, the product name; `product_type`, the classification of the product with allowed values `FINISHED_GOO…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_3`, `Manufacturing Route→ROUTE`, `Actual stock levels of components and products stored in specific warehouses→INVENTORY`, `Work Order→WORK_ORDER`, `parent_chunk_data_dictionary.md_6`, `parent_chunk_business_glossary.md_0`, `Manufacturing Route`, `parent_chunk_business_glossary.md_1`

**Context previews (first 3):**

1. _# Manufacturing Data Dictionary  This data dictionary documents the database schema for the manufacturing supply chain system. It includes all tables, columns, data types, constraints, and relationshi…_

2. _Business concept 'Manufacturing Route' — The table stores ordered manufacturing steps for a product, including operation name, work center, cycle time, setup time, and sequence number, which aligns di…_

3. _Business concept 'Actual stock levels of components and products stored in specific warehouses' is implemented by physical table INVENTORY (columns: inventory_id, warehouse_id, component_id, product_i…_

---

### ✅ QA-002 — How are components defined in the manufacturing database?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.5910 | **Gate:** `proceed`

**Expected answer:**
> Components are defined with a unique identifier (component_id), descriptive name (component_name), category grouping (component_category), unit of measure (unit_of_measure), standard unit cost (standard_cost), and optional reference to technical specifications (specification_id). Components represen…

**System answer:**
> In the business glossary, a Component is defined as an atomic raw material or purchased part that cannot be further broken down into simpler manufactured items. Components are the building blocks used in manufacturing and are procured from external suppliers.

In the schema, components are represented in multiple related ways. The `product` table explicitly says it stores all manufactured items, i…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_3`, `Bill of Materials Entry`, `Bill of Materials Entry→BOM`, `parent_chunk_data_dictionary.md_4`, `parent_chunk_data_dictionary.md_5`, `Junction table linking components to approved suppliers→COMPONENT_SUPPLIER`, `Actual stock levels of components and products stored in specific warehouses→INVENTORY`, `parent_chunk_business_glossary.md_0`

**Context previews (first 3):**

1. _# Manufacturing Data Dictionary  This data dictionary documents the database schema for the manufacturing supply chain system. It includes all tables, columns, data types, constraints, and relationshi…_

2. _Bill of Materials Entry: The table directly models BOM structure with parent_product_id, component_product_id, quantity, unit_of_measure, bom_level, and is_optional, and the DDL comment explicitly sta…_

3. _Business concept 'Bill of Materials Entry' — The table directly models BOM structure with parent_product_id, component_product_id, quantity, unit_of_measure, bom_level, and is_optional, and the DDL co…_

---

### ✅ QA-003 — What is the purpose of the Bill of Materials (BOM) table?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.9118 | **Gate:** `proceed`

**Expected answer:**
> The BOM table defines the hierarchical structure of products by specifying which components or sub-assemblies are required to manufacture each parent product. It records the unique BOM entry identifier (bom_id), parent product being built (parent_product_id), component or sub-assembly product (compo…

**System answer:**
> The Bill of Materials table, `bom`, exists to define product composition and hierarchical structure. It models BOM entries that specify what components go into a parent product and in what quantity and unit of measure. Specifically, it captures `parent_product_id`, `component_product_id`, `quantity`, `unit_of_measure`, `bom_level`, and `is_optional`.

From the context, its purpose includes represe…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_4`, `Bill of Materials Entry`, `Bill of Materials Entry→BOM`, `BOM→PRODUCT`, `parent_chunk_data_dictionary.md_3`, `parent_chunk_data_dictionary.md_7`, `parent_chunk_data_dictionary.md_8`, `parent_chunk_business_glossary.md_0`

**Context previews (first 3):**

1. _## bom  Bill of Materials defining product composition and hierarchical structure. Supports recursive relationships for multi-level assemblies.  | Column | Data Type | Constraints | Description | |---…_

2. _Bill of Materials Entry: The table directly models BOM structure with parent_product_id, component_product_id, quantity, unit_of_measure, bom_level, and is_optional, and the DDL comment explicitly sta…_

3. _Business concept 'Bill of Materials Entry' — The table directly models BOM structure with parent_product_id, component_product_id, quantity, unit_of_measure, bom_level, and is_optional, and the DDL co…_

---

### ✅ QA-004 — What supplier information does the system maintain?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0325 | **Gate:** `proceed_with_warning`

**Expected answer:**
> Suppliers are tracked with a unique identifier (supplier_id), legal business name (supplier_name), primary contact email (contact_email), primary contact phone number (contact_phone), performance rating from 1.0 to 5.0 (rating), and preferred supplier status flag (is_preferred).

**System answer:**
> The system maintains supplier master data in the SUPPLIER table. From the retrieved context, that includes supplier_id, supplier_name, contact_email, contact_phone, rating, and is_preferred. The supplier table is described as storing external vendor information for component procurement, with supplier_id as the unique supplier identifier and supplier_name as the supplier name.

It also maintains s…

**Sources retrieved (12):** `Preferred supplier for this component→SUPPLIER`, `parent_chunk_data_dictionary.md_4`, `Junction table linking components to approved suppliers`, `SHIPMENT→SUPPLIER`, `Junction table linking components to approved suppliers→COMPONENT_SUPPLIER`, `One-to-many with shipment (inbound)→SHIPMENT`, `parent_chunk_data_dictionary.md_8`, `COMPONENT_SUPPLIER→SUPPLIER`

**Context previews (first 3):**

1. _Business concept 'Preferred supplier for this component' is implemented by physical table SUPPLIER (columns: supplier_id, supplier_name, contact_email, contact_phone, rating, is_preferred).…_

2. _## bom  Bill of Materials defining product composition and hierarchical structure. Supports recursive relationships for multi-level assemblies.  | Column | Data Type | Constraints | Description | |---…_

3. _Junction table linking components to approved suppliers: The table has a composite uniqueness constraint on component_id and supplier_id and foreign keys to both component and supplier, which clearly …_

---

### ✅ QA-005 — How are warehouses represented in the schema?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.3381 | **Gate:** `proceed`

**Expected answer:**
> Warehouses are defined with a unique identifier (warehouse_id), descriptive name (warehouse_name), full street address (address), city location (city), state or province (state), total storage capacity in cubic meters (capacity), and optional manager identifier (manager_id).

**System answer:**
> Warehouses are represented by the physical table `WAREHOUSE`, which implements the business concept of a “Production location.” It is also described as a physical storage location for inventory management and as a supply chain node where materials, components, and finished goods are stored, shipments are received and sent, products are staged for production or distribution, and produced batches ar…

**Sources retrieved (12):** `INVENTORY→WAREHOUSE`, `BATCH→WAREHOUSE`, `WORK_ORDER→WAREHOUSE`, `SHIPMENT→WAREHOUSE`, `parent_chunk_data_dictionary.md_6`, `Production location→WAREHOUSE`, `parent_chunk_data_dictionary.md_5`, `parent_chunk_data_dictionary.md_8`

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
> The `INVENTORY` table tracks the actual stock levels of components and products stored in specific warehouses. It records inventory by warehouse and supports either a component or a product in a given record, but not both at the same time.

From the context, `INVENTORY` includes:
`inventory_id`, `warehouse_id`, `component_id`, `product_id`, `quantity_on_hand`, `quantity_reserved`, `reorder_thresho…

**Sources retrieved (12):** `INVENTORY→PRODUCT`, `INVENTORY→WAREHOUSE`, `INVENTORY→COMPONENT`, `Actual stock levels of components and products stored in specific warehouses→INVENTORY`, `parent_chunk_data_dictionary.md_5`, `parent_chunk_data_dictionary.md_7`, `parent_chunk_data_dictionary.md_8`, `parent_chunk_business_glossary.md_1`

**Context previews (first 3):**

1. _Relationship: INVENTORY references PRODUCT via foreign key PRODUCT_ID -> PRODUCT.PRODUCT_ID.…_

2. _Relationship: INVENTORY references WAREHOUSE via foreign key WAREHOUSE_ID -> WAREHOUSE.WAREHOUSE_ID.…_

3. _Relationship: INVENTORY references COMPONENT via foreign key COMPONENT_ID -> COMPONENT.COMPONENT_ID.…_

---

### ✅ QA-007 — How are work orders structured in the manufacturing system?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.6658 | **Gate:** `proceed`

**Expected answer:**
> Work orders represent production jobs with a unique identifier (work_order_id), product to be manufactured (product_id), optional parent work order for nested hierarchies (parent_work_order), quantity to produce (quantity_ordered), quantity completed so far (quantity_completed), current status (PEND…

**System answer:**
> Work orders are implemented by the WORK_ORDER table and represent production jobs for manufacturing products. The structure is explicitly hierarchical: each work order has a unique work_order_id, and the parent_work_order column is a self-referencing foreign key to WORK_ORDER.work_order_id. This allows a large production job to be decomposed into child work orders and supports complex production p…

**Sources retrieved (12):** `Work Order→WORK_ORDER`, `parent_chunk_data_dictionary.md_6`, `WORK_ORDER→PRODUCT`, `Manufacturing Route→ROUTE`, `WORK_ORDER→WORK_ORDER`, `parent_chunk_data_dictionary.md_3`, `WORK_ORDER→WAREHOUSE`, `parent_chunk_data_dictionary.md_5`

**Context previews (first 3):**

1. _Business concept 'Work Order' — The table is explicitly named WORK_ORDER and the comment says it stores production jobs. Its columns capture planned versus completed quantities, status, priority, date…_

2. _## work_order  Represents production jobs for manufacturing products with hierarchical work order support.  | Column | Data Type | Constraints | Description | |--------|-----------|-------------|-----…_

3. _Relationship: WORK_ORDER references PRODUCT via foreign key PRODUCT_ID -> PRODUCT.PRODUCT_ID.…_

---

### ✅ QA-008 — What information is captured in the shipment table?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.8515 | **Gate:** `proceed`

**Expected answer:**
> Shipments track material transfers with a unique identifier (shipment_id), shipment type (INBOUND from suppliers, OUTBOUND to customers, INTERNAL between warehouses), destination warehouse (warehouse_id), source supplier for inbound (supplier_id), destination customer for outbound (customer_id), shi…

**System answer:**
> The `SHIPMENT` table tracks material transfers between warehouses, suppliers, and customers. It captures the shipment’s unique identifier (`shipment_id`), the shipment type (`shipment_type`), the related warehouse (`warehouse_id`), supplier (`supplier_id`), and customer (`customer_id`), along with shipment timing fields: `ship_date`, `estimated_arrival`, and `actual_arrival`. It also stores the sh…

**Sources retrieved (12):** `One-to-many with shipment (inbound)→SHIPMENT`, `SHIPMENT→WAREHOUSE`, `SHIPMENT→SUPPLIER`, `parent_chunk_data_dictionary.md_8`, `parent_chunk_data_dictionary.md_5`, `parent_chunk_business_glossary.md_0`, `parent_chunk_business_glossary.md_1`, `Work Order→WORK_ORDER`

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
> Inspections are recorded in the physical table QUALITY_CONTROL, which implements the business concept “inspection and testing records for quality assurance.”

Each inspection record captures:
qc_id as the unique QC record identifier, batch_id as the production batch or lot being inspected, specification_id as the technical specification being tested, qc_date as the inspection date, qc_type as the …

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
> Specification records define technical requirements, standards, and acceptance criteria for materials or products. They capture the specification name and version, effective date, specification type, critical parameter being tested, acceptable minimum and maximum values, and unit of measure.

**Sources retrieved (12):** `inspection and testing records for quality assurance→QUALITY_CONTROL`, `parent_chunk_data_dictionary.md_7`, `Specifications for quality requirements→SPECIFICATION`, `parent_chunk_data_dictionary.md_3`, `parent_chunk_business_glossary.md_2`, `parent_chunk_business_glossary.md_0`, `inspection and testing records for quality assurance`, `parent_chunk_business_glossary.md_1`

**Context previews (first 3):**

1. _Business concept 'inspection and testing records for quality assurance' is implemented by physical table QUALITY_CONTROL (columns: qc_id, batch_id, specification_id, qc_date, qc_type, inspector_id, re…_

2. _## specification  Defines technical requirements and acceptance criteria for materials and products.  | Column | Data Type | Constraints | Description | |--------|-----------|-------------|-----------…_

3. _Business concept 'Specifications for quality requirements' is implemented by physical table SPECIFICATION (columns: specification_id, specification_name, version, effective_date, spec_type, critical_p…_

---

### ✅ QA-011 — How can I find which suppliers provide specific components?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.1645 | **Gate:** `proceed_with_warning`

**Expected answer:**
> Query the component_supplier table which links components to their approved suppliers. This table contains the component identifier (component_id), supplier identifier (supplier_id), preferred supplier flag (is_preferred), lead time in days (lead_time_days), and unit price (unit_price). Join with th…

**System answer:**
> Use the `COMPONENT_SUPPLIER` table. The retrieved context identifies it as the junction table linking components to approved suppliers, with foreign keys `component_id -> COMPONENT.component_id` and `supplier_id -> SUPPLIER.supplier_id`.

To find which suppliers provide a specific component, trace this path:

`COMPONENT.component_id` ← `COMPONENT_SUPPLIER.component_id`
and
`COMPONENT_SUPPLIER.supp…

**Sources retrieved (12):** `Junction table linking components to approved suppliers→COMPONENT_SUPPLIER`, `Junction table linking components to approved suppliers`, `parent_chunk_data_dictionary.md_5`, `parent_chunk_data_dictionary.md_4`, `Actual stock levels of components and products stored in specific warehouses→INVENTORY`, `parent_chunk_data_dictionary.md_3`, `parent_chunk_business_glossary.md_0`, `parent_chunk_business_glossary.md_1`

**Context previews (first 3):**

1. _Business concept 'Junction table linking components to approved suppliers' — The table has a composite uniqueness constraint on component_id and supplier_id and foreign keys to both component and supp…_

2. _Junction table linking components to approved suppliers: The table has a composite uniqueness constraint on component_id and supplier_id and foreign keys to both component and supplier, which clearly …_

3. _## warehouse  Stores physical storage location information for inventory management.  | Column | Data Type | Constraints | Description | |--------|-----------|-------------|-------------| | warehouse_…_

---

### ✅ QA-012 — How do I trace which components are needed to fulfill a work order?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.2334 | **Gate:** `proceed`

**Expected answer:**
> Start with the work_order table to get the product_id being manufactured. Join to the bom table using product_id as parent_product_id to find all direct components and sub-assemblies. For each component_product_id, if it is an ASSEMBLY type product, recursively query the bom table again to explode m…

**System answer:**
> From the retrieved context, you can only trace this partially.

What is known is that a work order is stored in `WORK_ORDER`, and `WORK_ORDER.PRODUCT_ID` is a foreign key to `PRODUCT.PRODUCT_ID`. So the first step is to identify the product being manufactured from the work order by following `WORK_ORDER.PRODUCT_ID -> PRODUCT.PRODUCT_ID`.

The context also says the `PRODUCT` table supports hierarch…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_5`, `parent_chunk_data_dictionary.md_6`, `Work Order→WORK_ORDER`, `Actual stock levels of components and products stored in specific warehouses→INVENTORY`, `parent_chunk_data_dictionary.md_3`, `parent_chunk_data_dictionary.md_8`, `parent_chunk_data_dictionary.md_7`, `WORK_ORDER→PRODUCT`

**Context previews (first 3):**

1. _## warehouse  Stores physical storage location information for inventory management.  | Column | Data Type | Constraints | Description | |--------|-----------|-------------|-------------| | warehouse_…_

2. _## work_order  Represents production jobs for manufacturing products with hierarchical work order support.  | Column | Data Type | Constraints | Description | |--------|-----------|-------------|-----…_

3. _Business concept 'Work Order' — The table is explicitly named WORK_ORDER and the comment says it stores production jobs. Its columns capture planned versus completed quantities, status, priority, date…_

---

### ✅ QA-013 — How can I identify which warehouses have available inventory for specific components?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.8876 | **Gate:** `proceed`

**Expected answer:**
> Query the inventory table filtered by component_id, joining with the warehouse table to get warehouse names and locations. Calculate available quantity as quantity_on_hand minus quantity_reserved. Filter for records where available quantity is greater than zero. Results show warehouse names, locatio…

**System answer:**
> Use the INVENTORY table, which implements the business concept “Actual stock levels of components and products stored in specific warehouses.”

At the schema level, the path is INVENTORY.warehouse_id → WAREHOUSE.warehouse_id, and INVENTORY.component_id → COMPONENT.component_id.

To identify warehouses for a specific component, look in INVENTORY for records where the target component is in INVENTOR…

**Sources retrieved (12):** `Actual stock levels of components and products stored in specific warehouses→INVENTORY`, `parent_chunk_data_dictionary.md_5`, `INVENTORY→WAREHOUSE`, `INVENTORY→COMPONENT`, `parent_chunk_data_dictionary.md_3`, `parent_chunk_data_dictionary.md_8`, `parent_chunk_data_dictionary.md_6`, `parent_chunk_data_dictionary.md_4`

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
> Use the `shipment` table as the starting point, because it tracks transfers between suppliers, warehouses, and customers.

To find shipments that delivered materials from a specific supplier, filter `shipment` on:
`shipment.supplier_id` = the supplier you want,
`shipment.shipment_type` = `INBOUND`,
and `shipment.status` = `DELIVERED`.

That combination is supported by the schema: `supplier_id` is …

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_8`, `SHIPMENT→SUPPLIER`, `One-to-many with shipment (inbound)→SHIPMENT`, `parent_chunk_data_dictionary.md_5`, `Actual stock levels of components and products stored in specific warehouses→INVENTORY`, `parent_chunk_data_dictionary.md_7`, `parent_chunk_data_dictionary.md_3`, `parent_chunk_data_dictionary.md_4`

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
> To determine which quality control inspections were performed on a specific production batch, use the `QUALITY_CONTROL` table, because the business concept “inspection and testing records for quality assurance” is implemented by `QUALITY_CONTROL`, and that table includes `batch_id` as the production batch reference.

At the schema level, the lookup is:

`QUALITY_CONTROL.batch_id = BATCH.batch_id`
…

**Sources retrieved (12):** `inspection and testing records for quality assurance→QUALITY_CONTROL`, `parent_chunk_data_dictionary.md_7`, `Production batch reference→BATCH`, `BATCH→PRODUCT`, `parent_chunk_data_dictionary.md_5`, `parent_chunk_data_dictionary.md_6`, `parent_chunk_data_dictionary.md_3`, `parent_chunk_business_glossary.md_2`

**Context previews (first 3):**

1. _Business concept 'inspection and testing records for quality assurance' is implemented by physical table QUALITY_CONTROL (columns: qc_id, batch_id, specification_id, qc_date, qc_type, inspector_id, re…_

2. _## specification  Defines technical requirements and acceptance criteria for materials and products.  | Column | Data Type | Constraints | Description | |--------|-----------|-------------|-----------…_

3. _Business concept 'Production batch reference' is implemented by physical table BATCH (columns: batch_id, product_id, production_date, quantity_produced, warehouse_id, expiry_date, qc_status).…_

---

### ✅ QA-016 — How do I track which work orders are in progress at a specific warehouse?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.7311 | **Gate:** `proceed`

**Expected answer:**
> Query the work_order table filtering by warehouse_id and status = 'IN_PROGRESS'. Join with the product table to get product names and types. Include quantity_ordered, quantity_completed, priority, planned_end_date, and calculate progress percentage as (quantity_completed / quantity_ordered * 100). O…

**System answer:**
> Use the `WORK_ORDER` table, because it stores production jobs and includes both the work order status and the production location. To find work orders in progress at a specific warehouse, filter `WORK_ORDER` on `warehouse_id` and on `status = 'IN_PROGRESS'`.

The key columns are `WORK_ORDER.work_order_id`, `product_id`, `quantity_ordered`, `quantity_completed`, `priority`, `planned_start_date`, `p…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_5`, `parent_chunk_data_dictionary.md_6`, `WORK_ORDER→WAREHOUSE`, `Work Order→WORK_ORDER`, `Actual stock levels of components and products stored in specific warehouses→INVENTORY`, `parent_chunk_data_dictionary.md_8`, `parent_chunk_data_dictionary.md_7`, `parent_chunk_business_glossary.md_1`

**Context previews (first 3):**

1. _## warehouse  Stores physical storage location information for inventory management.  | Column | Data Type | Constraints | Description | |--------|-----------|-------------|-------------| | warehouse_…_

2. _## work_order  Represents production jobs for manufacturing products with hierarchical work order support.  | Column | Data Type | Constraints | Description | |--------|-----------|-------------|-----…_

3. _Relationship: WORK_ORDER references WAREHOUSE via foreign key WAREHOUSE_ID -> WAREHOUSE.WAREHOUSE_ID.…_

---

### ✅ QA-017 — How can I find which components need reordering based on current inventory levels?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.5691 | **Gate:** `proceed`

**Expected answer:**
> Query the inventory table and filter where quantity_on_hand minus quantity_reserved is less than reorder_threshold. Join with the component table to get component names, categories, and standard costs. Join with the warehouse table for location information. Results identify which components are belo…

**System answer:**
> Use the INVENTORY table, which implements the business concept “Actual stock levels of components and products stored in specific warehouses.” To find components that may need reordering, focus on INVENTORY records where component_id is populated, because each inventory row supports either a component or a product, but not both.

The relevant columns in INVENTORY are component_id, warehouse_id, qu…

**Sources retrieved (12):** `Actual stock levels of components and products stored in specific warehouses→INVENTORY`, `parent_chunk_data_dictionary.md_5`, `INVENTORY→COMPONENT`, `parent_chunk_data_dictionary.md_3`, `parent_chunk_data_dictionary.md_7`, `parent_chunk_data_dictionary.md_4`, `parent_chunk_data_dictionary.md_6`, `parent_chunk_business_glossary.md_1`

**Context previews (first 3):**

1. _Business concept 'Actual stock levels of components and products stored in specific warehouses' is implemented by physical table INVENTORY (columns: inventory_id, warehouse_id, component_id, product_i…_

2. _## warehouse  Stores physical storage location information for inventory management.  | Column | Data Type | Constraints | Description | |--------|-----------|-------------|-------------| | warehouse_…_

3. _Relationship: INVENTORY references COMPONENT via foreign key COMPONENT_ID -> COMPONENT.COMPONENT_ID.…_

---

### ✅ QA-018 — How do I determine the manufacturing route for a specific product?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.8387 | **Gate:** `proceed`

**Expected answer:**
> Query the route table filtering by product_id, ordered by sequence_number ascending. For each operation, retrieve operation_name, work_center, cycle_time_minutes, and setup_time_minutes. Join with the product table to get product details. The sequence of operations shows the complete manufacturing w…

**System answer:**
> To determine the manufacturing route for a specific product, use the ROUTE table, which implements the “Manufacturing Route” concept. The key relationship is ROUTE.product_id → PRODUCT.product_id.

At the schema level, the route is determined by selecting rows from ROUTE for the target product_id. The ROUTE table stores the ordered manufacturing steps for a product, and its relevant columns are ro…

**Sources retrieved (12):** `Manufacturing Route→ROUTE`, `parent_chunk_data_dictionary.md_6`, `ROUTE→PRODUCT`, `parent_chunk_data_dictionary.md_3`, `parent_chunk_data_dictionary.md_7`, `a unique identifier, name, type classification, base cost, and lead time for procurement or production→PRODUCT`, `parent_chunk_data_dictionary.md_5`, `Work Order→WORK_ORDER`

**Context previews (first 3):**

1. _Business concept 'Manufacturing Route' — The table stores ordered manufacturing steps for a product, including operation name, work center, cycle time, setup time, and sequence number, which aligns di…_

2. _## work_order  Represents production jobs for manufacturing products with hierarchical work order support.  | Column | Data Type | Constraints | Description | |--------|-----------|-------------|-----…_

3. _Relationship: ROUTE references PRODUCT via foreign key PRODUCT_ID -> PRODUCT.PRODUCT_ID.…_

---

### ✅ QA-019 — How can I find which batches are stored at a specific warehouse and their QC status?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.7533 | **Gate:** `proceed`

**Expected answer:**
> Query the batch table filtering by warehouse_id. Join with the product table to get product names and types. Include production_date, quantity_produced, expiry_date, and qc_status (PENDING, PASSED, FAILED, QUARANTINED). Filter by qc_status to isolate batches requiring quality attention or ready for …

**System answer:**
> Use the `BATCH` table directly. The business concept “Production batch reference” is implemented by `BATCH`, and it contains both the storage location and the batch QC status: `batch_id`, `product_id`, `production_date`, `quantity_produced`, `warehouse_id`, `expiry_date`, and `qc_status`.

The lookup path is:

`WAREHOUSE.warehouse_id` → `BATCH.warehouse_id`

This relationship is explicit: `BATCH` …

**Sources retrieved (12):** `Production batch reference→BATCH`, `Actual stock levels of components and products stored in specific warehouses→INVENTORY`, `parent_chunk_data_dictionary.md_5`, `BATCH→WAREHOUSE`, `inspection and testing records for quality assurance→QUALITY_CONTROL`, `parent_chunk_data_dictionary.md_6`, `parent_chunk_data_dictionary.md_8`, `Work Order→WORK_ORDER`

**Context previews (first 3):**

1. _Business concept 'Production batch reference' is implemented by physical table BATCH (columns: batch_id, product_id, production_date, quantity_produced, warehouse_id, expiry_date, qc_status).…_

2. _Business concept 'Actual stock levels of components and products stored in specific warehouses' is implemented by physical table INVENTORY (columns: inventory_id, warehouse_id, component_id, product_i…_

3. _## warehouse  Stores physical storage location information for inventory management.  | Column | Data Type | Constraints | Description | |--------|-----------|-------------|-------------| | warehouse_…_

---

### ✅ QA-020 — How do I identify which specifications apply to specific components?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.2550 | **Gate:** `proceed`

**Expected answer:**
> Query the component table and join with the specification table via specification_id. Include component_name, component_category, and specification details (specification_name, spec_type, critical_parameter, min_value, max_value, unit_of_measure). This shows the technical requirements that each comp…

**System answer:**
> From the retrieved context, you cannot reliably identify which specifications apply to specific components from the physical schema alone.

What is available is this: the business concept “Specifications for quality requirements” is implemented by the `SPECIFICATION` table, which has only these columns: `specification_id`, `specification_name`, `version`, `effective_date`, `spec_type`, `critical_p…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_5`, `parent_chunk_data_dictionary.md_7`, `Actual stock levels of components and products stored in specific warehouses→INVENTORY`, `parent_chunk_data_dictionary.md_3`, `parent_chunk_data_dictionary.md_4`, `Specifications for quality requirements→SPECIFICATION`, `Junction table linking components to approved suppliers→COMPONENT_SUPPLIER`, `parent_chunk_business_glossary.md_0`

**Context previews (first 3):**

1. _## warehouse  Stores physical storage location information for inventory management.  | Column | Data Type | Constraints | Description | |--------|-----------|-------------|-------------| | warehouse_…_

2. _## specification  Defines technical requirements and acceptance criteria for materials and products.  | Column | Data Type | Constraints | Description | |--------|-----------|-------------|-----------…_

3. _Business concept 'Actual stock levels of components and products stored in specific warehouses' is implemented by physical table INVENTORY (columns: inventory_id, warehouse_id, component_id, product_i…_

---

### ✅ QA-021 — How can I perform a complete BOM explosion to find all components required for a finished product?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.3509 | **Gate:** `proceed`

**Expected answer:**
> Use a recursive query starting from the product_id of the finished good. At each level, join the bom table to find component_product_id entries. For each component, check if product_type is 'ASSEMBLY' or 'FINISHED_GOOD'. If so, recursively query bom again using that component_product_id as the new p…

**System answer:**
> Use the `bom` table as the recursive structure and the `product` table to identify the finished product and describe each returned item.

A complete BOM explosion starts from the finished product in `product`, typically a row whose `product_type` is `FINISHED_GOOD`. Use that product’s `product_id` as the starting value, then find all direct BOM rows in `bom` where `bom.parent_product_id = product.…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_4`, `parent_chunk_data_dictionary.md_3`, `Bill of Materials Entry→BOM`, `BOM→PRODUCT`, `Bill of Materials Entry`, `parent_chunk_data_dictionary.md_5`, `parent_chunk_data_dictionary.md_7`, `parent_chunk_data_dictionary.md_6`

**Context previews (first 3):**

1. _## bom  Bill of Materials defining product composition and hierarchical structure. Supports recursive relationships for multi-level assemblies.  | Column | Data Type | Constraints | Description | |---…_

2. _# Manufacturing Data Dictionary  This data dictionary documents the database schema for the manufacturing supply chain system. It includes all tables, columns, data types, constraints, and relationshi…_

3. _Business concept 'Bill of Materials Entry' — The table directly models BOM structure with parent_product_id, component_product_id, quantity, unit_of_measure, bom_level, and is_optional, and the DDL co…_

---

### ✅ QA-022 — How do I calculate the total material cost for a product including all sub-assemblies?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.2332 | **Gate:** `proceed`

**Expected answer:**
> Perform a recursive BOM explosion to find all leaf-level components. For each leaf component, join with the component table to get standard_cost. Multiply standard_cost by the accumulated quantity from the BOM traversal. Sum all component costs to get total material cost. This calculation must trave…

**System answer:**
> Use the `bom` table as the exploded structure and the `product` table for the unit cost.

The schema supports this through a recursive product composition model: `bom.parent_product_id` and `bom.component_product_id` both reference `product(product_id)`, and the data dictionary explicitly says `bom` supports multi-level assemblies. The `product` table provides `base_cost`, while `bom` provides the…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_3`, `parent_chunk_data_dictionary.md_4`, `parent_chunk_data_dictionary.md_7`, `parent_chunk_data_dictionary.md_8`, `Bill of Materials Entry→BOM`, `parent_chunk_data_dictionary.md_6`, `parent_chunk_data_dictionary.md_5`, `Bill of Materials Entry`

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
> Use the `bom` table as the traversal table. It is the table that “defines product composition and hierarchical structure,” and both `parent_product_id` and `component_product_id` are foreign keys to `product(product_id)`, which explicitly supports recursive, multi-level assemblies.

To find every parent product that contains a specific component anywhere in its BOM structure, start with BOM rows w…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_4`, `parent_chunk_data_dictionary.md_3`, `Bill of Materials Entry`, `Bill of Materials Entry→BOM`, `BOM→PRODUCT`, `PRODUCT→PRODUCT`, `parent_chunk_data_dictionary.md_6`, `parent_chunk_data_dictionary.md_8`

**Context previews (first 3):**

1. _## bom  Bill of Materials defining product composition and hierarchical structure. Supports recursive relationships for multi-level assemblies.  | Column | Data Type | Constraints | Description | |---…_

2. _# Manufacturing Data Dictionary  This data dictionary documents the database schema for the manufacturing supply chain system. It includes all tables, columns, data types, constraints, and relationshi…_

3. _Bill of Materials Entry: The table directly models BOM structure with parent_product_id, component_product_id, quantity, unit_of_measure, bom_level, and is_optional, and the DDL comment explicitly sta…_

---

### ✅ QA-024 — How do I identify work orders that require a specific component, considering nested sub-assemblies?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.3651 | **Gate:** `proceed`

**Expected answer:**
> First, perform reverse BOM traversal to find all parent products that contain the target component at any level. Then query the work_order table where product_id is in the set of parent products found. This includes work orders for finished goods that contain the component indirectly through sub-ass…

**System answer:**
> Use the `WORK_ORDER` → `PRODUCT` → `BOM` path, and traverse the `BOM` hierarchy recursively.

A work order identifies what is being built through `work_order.product_id`, which references `product.product_id`. The `BOM` table defines product composition, where `bom.parent_product_id` is the product being built and `bom.component_product_id` is a product used inside it. Because both columns referen…

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
> Use the `bom` table, because it is the table that directly models the Bill of Materials hierarchy and it includes `bom_level`, which is explicitly defined as the “depth in product hierarchy.”

To determine maximum BOM depth:

For a specific product, filter `bom.parent_product_id` to that product’s `product_id`, then take the maximum value of `bom.bom_level`. The join path is `product.product_id = …

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_4`, `parent_chunk_data_dictionary.md_3`, `Bill of Materials Entry→BOM`, `Bill of Materials Entry`, `BOM→PRODUCT`, `parent_chunk_data_dictionary.md_7`, `parent_chunk_data_dictionary.md_5`, `parent_chunk_data_dictionary.md_6`

**Context previews (first 3):**

1. _## bom  Bill of Materials defining product composition and hierarchical structure. Supports recursive relationships for multi-level assemblies.  | Column | Data Type | Constraints | Description | |---…_

2. _# Manufacturing Data Dictionary  This data dictionary documents the database schema for the manufacturing supply chain system. It includes all tables, columns, data types, constraints, and relationshi…_

3. _Business concept 'Bill of Materials Entry' — The table directly models BOM structure with parent_product_id, component_product_id, quantity, unit_of_measure, bom_level, and is_optional, and the DDL co…_

---

### ✅ QA-026 — How do I find all products that have a specific product as a sub-assembly at any level?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.2392 | **Gate:** `proceed`

**Expected answer:**
> Perform a recursive search starting with the target product_id as the initial component_product_id in the bom table. For each parent_product_id found, check if that parent appears as a component in other bom entries. Continue recursively until reaching products that are not used as components elsewh…

**System answer:**
> Use the `bom` table as the primary path, because it directly models product composition.

For a specific product, start with `bom.component_product_id = <target product_id>`. Those rows identify the immediate parent products through `bom.parent_product_id` — the products that directly use the target as a sub-assembly or component. To find products that contain it at any level, continue recursively…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_3`, `parent_chunk_data_dictionary.md_4`, `parent_chunk_data_dictionary.md_5`, `Actual stock levels of components and products stored in specific warehouses→INVENTORY`, `Bill of Materials Entry→BOM`, `parent_chunk_data_dictionary.md_7`, `parent_chunk_data_dictionary.md_6`, `Bill of Materials Entry`

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
> From the retrieved context, the schema supports calculating this at the hierarchy level, but it does not define a single mandated roll-up formula.

The relevant source is the `PRODUCT` table plus the `BOM` table. `PRODUCT.lead_time_days` is the lead time for procurement or production of that item, and `BOM` defines the multi-level product structure with `parent_product_id`, `component_product_id`,…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_3`, `a unique identifier, name, type classification, base cost, and lead time for procurement or production→PRODUCT`, `Junction table linking components to approved suppliers→COMPONENT_SUPPLIER`, `parent_chunk_data_dictionary.md_4`, `Manufacturing Route→ROUTE`, `Junction table linking components to approved suppliers`, `parent_chunk_data_dictionary.md_7`, `parent_chunk_data_dictionary.md_6`

**Context previews (first 3):**

1. _# Manufacturing Data Dictionary  This data dictionary documents the database schema for the manufacturing supply chain system. It includes all tables, columns, data types, constraints, and relationshi…_

2. _Business concept 'a unique identifier, name, type classification, base cost, and lead time for procurement or production' is implemented by physical table PRODUCT (columns: product_id, product_name, p…_

3. _Business concept 'Junction table linking components to approved suppliers' — The table has a composite uniqueness constraint on component_id and supplier_id and foreign keys to both component and supp…_

---

### ✅ QA-028 — How do I generate a complete indented BOM report showing the hierarchical structure?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.4180 | **Gate:** `proceed`

**Expected answer:**
> Use a recursive query on the bom table that tracks the current depth level. Start with the top-level product (parent_product_id where product has no parent_product_id). At each level, output component details indented by depth level. Include product_name, quantity, and unit_of_measure. Recursively p…

**System answer:**
> Use the `bom` table as the source for the report, because it is the table that “defines product composition and hierarchical structure” and directly models the BOM entry with `parent_product_id`, `component_product_id`, `quantity`, `unit_of_measure`, `bom_level`, and `is_optional`.

To make the report readable, join `bom` to `product` twice. Join `bom.parent_product_id` to `product.product_id` to …

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_4`, `parent_chunk_data_dictionary.md_3`, `Bill of Materials Entry→BOM`, `Bill of Materials Entry`, `parent_chunk_data_dictionary.md_6`, `parent_chunk_data_dictionary.md_8`, `Work Order→WORK_ORDER`, `BOM→PRODUCT`

**Context previews (first 3):**

1. _## bom  Bill of Materials defining product composition and hierarchical structure. Supports recursive relationships for multi-level assemblies.  | Column | Data Type | Constraints | Description | |---…_

2. _# Manufacturing Data Dictionary  This data dictionary documents the database schema for the manufacturing supply chain system. It includes all tables, columns, data types, constraints, and relationshi…_

3. _Business concept 'Bill of Materials Entry' — The table directly models BOM structure with parent_product_id, component_product_id, quantity, unit_of_measure, bom_level, and is_optional, and the DDL co…_

---

### ✅ QA-029 — How can I find which components appear most frequently across all product BOMs?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.1587 | **Gate:** `proceed_with_warning`

**Expected answer:**
> Perform BOM explosion for all products and aggregate occurrences of each leaf-level component. Count how many distinct product hierarchies contain each component. Join with component table for component names. Order by frequency descending to identify common components that should be prioritized for…

**System answer:**
> Use the `bom` table, because it is the table that “directly models BOM structure” and contains the component reference in `component_product_id`.

At the schema level, the calculation is: count how many `bom` rows exist for each `component_product_id`. That gives the frequency with which a component appears across BOM entries. To make the result readable, join `bom.component_product_id` to `produc…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_4`, `parent_chunk_data_dictionary.md_3`, `Bill of Materials Entry→BOM`, `Bill of Materials Entry`, `BOM→PRODUCT`, `parent_chunk_data_dictionary.md_5`, `Actual stock levels of components and products stored in specific warehouses→INVENTORY`, `parent_chunk_data_dictionary.md_7`

**Context previews (first 3):**

1. _## bom  Bill of Materials defining product composition and hierarchical structure. Supports recursive relationships for multi-level assemblies.  | Column | Data Type | Constraints | Description | |---…_

2. _# Manufacturing Data Dictionary  This data dictionary documents the database schema for the manufacturing supply chain system. It includes all tables, columns, data types, constraints, and relationshi…_

3. _Business concept 'Bill of Materials Entry' — The table directly models BOM structure with parent_product_id, component_product_id, quantity, unit_of_measure, bom_level, and is_optional, and the DDL co…_

---

### ✅ QA-030 — How do I detect circular references in the BOM structure to prevent infinite loops?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.1295 | **Gate:** `proceed_with_warning`

**Expected answer:**
> Use a recursive query with a cycle detection check. Track the path of visited product_ids at each recursion level. If a product_id appears twice in the same path, a circular reference exists. Alternatively, check if any bom record has parent_product_id = component_product_id (direct self-reference),…

**System answer:**
> From the retrieved context, I can identify the BOM structure you would need to inspect, but the context does not provide a documented rule, query, or procedure for detecting circular references.

What is known is that circularity would have to be analyzed in the `bom` table, because it is the table that defines product composition and hierarchical structure. Each BOM entry has `parent_product_id` …

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_4`, `parent_chunk_data_dictionary.md_3`, `BOM→PRODUCT`, `Bill of Materials Entry→BOM`, `Bill of Materials Entry`, `parent_chunk_data_dictionary.md_8`, `parent_chunk_data_dictionary.md_7`, `parent_chunk_business_glossary.md_0`

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
> Based on the retrieved context, the intended schema-level approach is:

Start with the finished product in `product`, where `product_type` can be `FINISHED_GOOD`. To expand everything that goes into it, use the `bom` table recursively. In `bom`, `parent_product_id` is “what is being built” and `component_product_id` is “what goes into it,” and both columns are foreign keys to `product(product_id)`…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_3`, `parent_chunk_data_dictionary.md_4`, `parent_chunk_data_dictionary.md_8`, `parent_chunk_data_dictionary.md_6`, `Junction table linking components to approved suppliers→COMPONENT_SUPPLIER`, `parent_chunk_data_dictionary.md_7`, `Junction table linking components to approved suppliers`, `Manufacturing Route→ROUTE`

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
> To check this from the schema provided, start with `WORK_ORDER` and match it to `INVENTORY` by product.

A `work_order` identifies the product to manufacture in `WORK_ORDER.product_id` and the required and completed amounts in `quantity_ordered` and `quantity_completed`. Inventory records track stock by warehouse in `INVENTORY`, with `product_id`, `warehouse_id`, `quantity_on_hand`, and `quantity_…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_5`, `parent_chunk_data_dictionary.md_6`, `Actual stock levels of components and products stored in specific warehouses→INVENTORY`, `INVENTORY→WAREHOUSE`, `WORK_ORDER→WAREHOUSE`, `Work Order→WORK_ORDER`, `parent_chunk_data_dictionary.md_8`, `parent_chunk_data_dictionary.md_7`

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
> From the retrieved context, you can identify the two relevant pieces separately, but the context does not provide a complete supported join path to connect them.

The failed quality inspections are in `QUALITY_CONTROL`, which has columns `qc_id`, `batch_id`, `specification_id`, `qc_date`, `qc_type`, `inspector_id`, `result`, `defect_count`, and `notes`. To find failed inspections, filter `QUALITY_…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_5`, `parent_chunk_data_dictionary.md_3`, `Junction table linking components to approved suppliers→COMPONENT_SUPPLIER`, `inspection and testing records for quality assurance→QUALITY_CONTROL`, `Actual stock levels of components and products stored in specific warehouses→INVENTORY`, `parent_chunk_data_dictionary.md_4`, `Junction table linking components to approved suppliers`, `COMPONENT_SUPPLIER→SUPPLIER`

**Context previews (first 3):**

1. _## warehouse  Stores physical storage location information for inventory management.  | Column | Data Type | Constraints | Description | |--------|-----------|-------------|-------------| | warehouse_…_

2. _# Manufacturing Data Dictionary  This data dictionary documents the database schema for the manufacturing supply chain system. It includes all tables, columns, data types, constraints, and relationshi…_

3. _Business concept 'Junction table linking components to approved suppliers' — The table has a composite uniqueness constraint on component_id and supplier_id and foreign keys to both component and supp…_

---

### ✅ QA-034 — How do I calculate the total manufacturing time for a work order including all sub-assembly work orders?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.1599 | **Gate:** `proceed_with_warning`

**Expected answer:**
> Query the work_order table starting with the parent work_order. Find all child work_orders where parent_work_order matches the current work_order_id. For each work order (parent and children), join with the route table on product_id to get all operations. Sum (cycle_time_minutes * quantity) plus set…

**System answer:**
> From the retrieved context alone, I cannot give a documented formula for “total manufacturing time” for a work order and all its sub-assembly work orders.

What the context does support is the hierarchy you would use to identify the full work-order tree. `WORK_ORDER` stores production jobs, and `parent_work_order` is a self-referencing foreign key to `WORK_ORDER(work_order_id)`. That means you can…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_6`, `Manufacturing Route→ROUTE`, `Work Order→WORK_ORDER`, `parent_chunk_data_dictionary.md_3`, `parent_chunk_data_dictionary.md_7`, `parent_chunk_data_dictionary.md_5`, `parent_chunk_data_dictionary.md_4`, `parent_chunk_business_glossary.md_0`

**Context previews (first 3):**

1. _## work_order  Represents production jobs for manufacturing products with hierarchical work order support.  | Column | Data Type | Constraints | Description | |--------|-----------|-------------|-----…_

2. _Business concept 'Manufacturing Route' — The table stores ordered manufacturing steps for a product, including operation name, work center, cycle time, setup time, and sequence number, which aligns di…_

3. _Business concept 'Work Order' — The table is explicitly named WORK_ORDER and the comment says it stores production jobs. Its columns capture planned versus completed quantities, status, priority, date…_

---

### ✅ QA-035 — How can I identify which shipments are overdue and their impact on work orders?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0719 | **Gate:** `proceed_with_warning`

**Expected answer:**
> Query the shipment table filtering for status = 'SHIPPED' where actual_arrival is NULL and estimated_arrival is in the past (overdue). Join with the component_supplier table via supplier_id and component_id to identify which components are delayed. Perform reverse BOM lookup to find which parent pro…

**System answer:**
> From the retrieved context, you can only identify and correlate the relevant records at the schema level; the context does not define a business rule for when a shipment is “overdue,” and it does not define any direct shipment-to-work-order dependency.

The `SHIPMENT` table contains the fields you would use to assess shipment timing: `shipment_id`, `shipment_type`, `warehouse_id`, `supplier_id`, `…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_5`, `parent_chunk_data_dictionary.md_8`, `parent_chunk_data_dictionary.md_6`, `Work Order→WORK_ORDER`, `WORK_ORDER→PRODUCT`, `WORK_ORDER→WAREHOUSE`, `SHIPMENT→WAREHOUSE`, `One-to-many with shipment (inbound)→SHIPMENT`

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
> Use the BATCH table to find the expiry side of the problem, and then trace from the batch’s produced product to supplier-linked components.

The expiry part is directly available in BATCH, which is the “Production batch reference” table with columns batch_id, product_id, production_date, quantity_produced, warehouse_id, expiry_date, and qc_status. To find batches that are past expiry, compare BATC…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_5`, `Actual stock levels of components and products stored in specific warehouses→INVENTORY`, `parent_chunk_data_dictionary.md_7`, `parent_chunk_data_dictionary.md_3`, `Production batch reference→BATCH`, `Junction table linking components to approved suppliers→COMPONENT_SUPPLIER`, `parent_chunk_data_dictionary.md_8`, `Junction table linking components to approved suppliers`

**Context previews (first 3):**

1. _## warehouse  Stores physical storage location information for inventory management.  | Column | Data Type | Constraints | Description | |--------|-----------|-------------|-------------| | warehouse_…_

2. _Business concept 'Actual stock levels of components and products stored in specific warehouses' is implemented by physical table INVENTORY (columns: inventory_id, warehouse_id, component_id, product_i…_

3. _## specification  Defines technical requirements and acceptance criteria for materials and products.  | Column | Data Type | Constraints | Description | |--------|-----------|-------------|-----------…_

---

### ✅ QA-037 — How can I generate a material requirements plan showing when to order components based on work order schedules?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0433 | **Gate:** `proceed_with_warning`

**Expected answer:**
> Query all work_orders with status 'PENDING' ordered by planned_start_date. For each work_order, perform BOM explosion to get required components and quantities. For each component, query inventory for current available stock across warehouses. Calculate net requirements = (required quantity * work_o…

**System answer:**
> From the retrieved context, you can build a schedule-based material requirements view from the schema, but the context does not define a complete MRP rule set. In particular, it does not specify which `work_order.status` values should be treated as demand, and it does not define a formula for converting `planned_start_date` and `lead_time_days` into an order date.

The core join path starts with `…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_6`, `parent_chunk_data_dictionary.md_7`, `parent_chunk_data_dictionary.md_5`, `Work Order→WORK_ORDER`, `parent_chunk_data_dictionary.md_4`, `parent_chunk_data_dictionary.md_3`, `Bill of Materials Entry→BOM`, `Manufacturing Route→ROUTE`

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
> From the retrieved context, you can trace this only partially at the schema level.

On the supplier/procurement side, the path starts with `COMPONENT_SUPPLIER`, which is the junction table linking approved components to suppliers. Join `COMPONENT_SUPPLIER.component_id` to `COMPONENT.component_id`, and join `COMPONENT_SUPPLIER.supplier_id` to `SUPPLIER.supplier_id`. That gives you the approved supp…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_3`, `parent_chunk_data_dictionary.md_7`, `parent_chunk_data_dictionary.md_5`, `parent_chunk_data_dictionary.md_8`, `parent_chunk_data_dictionary.md_4`, `Junction table linking components to approved suppliers→COMPONENT_SUPPLIER`, `Bill of Materials Entry→BOM`, `Junction table linking components to approved suppliers`

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
> Use the BOM structure first, then the approved-supplier junction.

From the retrieved schema, the part of the problem that is fully defined is how to identify shared required components in product structures. The `bom` table tells you which item is used in which product: `parent_product_id` is the product being built, `component_product_id` is the component used in it, `quantity` is the required a…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_4`, `Junction table linking components to approved suppliers→COMPONENT_SUPPLIER`, `parent_chunk_data_dictionary.md_3`, `Junction table linking components to approved suppliers`, `Preferred supplier for this component→SUPPLIER`, `parent_chunk_data_dictionary.md_5`, `parent_chunk_data_dictionary.md_8`, `parent_chunk_data_dictionary.md_7`

**Context previews (first 3):**

1. _## bom  Bill of Materials defining product composition and hierarchical structure. Supports recursive relationships for multi-level assemblies.  | Column | Data Type | Constraints | Description | |---…_

2. _Business concept 'Junction table linking components to approved suppliers' — The table has a composite uniqueness constraint on component_id and supplier_id and foreign keys to both component and supp…_

3. _# Manufacturing Data Dictionary  This data dictionary documents the database schema for the manufacturing supply chain system. It includes all tables, columns, data types, constraints, and relationshi…_

---

### ✅ QA-040 — How do I calculate the total landed cost for a product including component costs, supplier lead times, and manufacturing operations?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.1922 | **Gate:** `proceed_with_warning`

**Expected answer:**
> Perform recursive BOM explosion to get all leaf components. For each component, query component_supplier to get unit_price from primary supplier. Multiply by accumulated BOM quantity for material cost. Add shipping costs (estimated from shipment history). Query route table for the product to get all…

**System answer:**
> From the retrieved context, you can define only a partial, schema-level landed-cost calculation. The knowledge graph gives metadata about tables, columns, and relationships, not actual transactional values, and it does not provide a complete costing formula.

The product anchor is `PRODUCT`. It stores `product_id`, `product_name`, `product_type`, `parent_product_id`, `base_cost`, `lead_time_days`,…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_3`, `a unique identifier, name, type classification, base cost, and lead time for procurement or production→PRODUCT`, `Junction table linking components to approved suppliers→COMPONENT_SUPPLIER`, `Junction table linking components to approved suppliers`, `Manufacturing Route→ROUTE`, `parent_chunk_data_dictionary.md_6`, `parent_chunk_data_dictionary.md_7`, `parent_chunk_data_dictionary.md_5`

**Context previews (first 3):**

1. _# Manufacturing Data Dictionary  This data dictionary documents the database schema for the manufacturing supply chain system. It includes all tables, columns, data types, constraints, and relationshi…_

2. _Business concept 'a unique identifier, name, type classification, base cost, and lead time for procurement or production' is implemented by physical table PRODUCT (columns: product_id, product_name, p…_

3. _Business concept 'Junction table linking components to approved suppliers' — The table has a composite uniqueness constraint on component_id and supplier_id and foreign keys to both component and supp…_

---

## Anomalies & Observations

No anomalies detected. All questions grounded with acceptable RAGAS scores.
