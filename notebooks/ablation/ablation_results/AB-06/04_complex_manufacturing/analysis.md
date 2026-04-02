# AB-06 — 04_complex_manufacturing — Run Analysis

**Timestamp:** 2026-03-31 06:46:52  
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
| Chunk size / overlap | `128 / 16` |
| ER similarity threshold | `0.75` |

## Builder Results

| Metric | Value |
|--------|-------|
| Triplets extracted | 420 |
| Entities resolved | 129 |
| Tables parsed | 13 |
| Tables completed | 13 |

## Query Evaluation Summary

| Metric | Value |
|--------|-------|
| Questions | 40 |
| Grounded | **40/40 (100%)** |
| Avg GT Coverage | 100% |
| Avg Top Score | 0.4125 |
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
> In the manufacturing system, product information is stored in the PRODUCT table. A product represents any manufactured item, including finished goods, assemblies, and components.

The stored product attributes are: product_id, which is the unique product identifier; product_name, the product name; product_type, which classifies the product as FINISHED_GOOD, ASSEMBLY, or COMPONENT; parent_product_i…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_3`, `parent_chunk_data_dictionary.md_6`, `parent_chunk_data_dictionary.md_5`, `parent_chunk_data_dictionary.md_7`, `parent_chunk_business_glossary.md_0`, `parent_chunk_business_glossary.md_1`, `parent_chunk_business_glossary.md_2`, `Traceability Batches→BATCH`

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
> Components are defined in two related ways in the retrieved context.

As a business concept, a Component is “an atomic raw material or purchased part” that “cannot be further broken down into simpler manufactured items.” Components are the building blocks used in manufacturing and are procured from external suppliers.

At the schema level, the context shows that components are represented both wit…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_3`, `parent_chunk_data_dictionary.md_4`, `components they can provide through approved supplier relationships→COMPONENT_SUPPLIER`, `parent_chunk_data_dictionary.md_5`, `BOM entry→BOM`, `Inventory Records→INVENTORY`, `parent_chunk_business_glossary.md_0`, `parent_chunk_business_glossary.md_1`

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
> The Bill of Materials table, `bom`, defines product composition and hierarchical structure. It records which component products go into a parent product, including the required `quantity`, `unit_of_measure`, `bom_level`, and whether the component `is_optional`.

From the schema and glossary context, its purpose is to support multi-level assemblies and recursive product structures. It does this by …

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_4`, `BOM→PRODUCT`, `BOM entry→BOM`, `parent_chunk_data_dictionary.md_3`, `parent_chunk_data_dictionary.md_8`, `parent_chunk_business_glossary.md_0`, `parent_chunk_business_glossary.md_1`, `a standard cost, unit of measure, and may be associated with technical specifications that define quality requirements→SPECIFICATION`

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
> The system maintains supplier master data in the `SUPPLIER` table, which stores external vendor information for component procurement. From the retrieved context, the supplier attributes are `supplier_id`, `supplier_name`, `contact_email`, `contact_phone`, `rating`, and `is_preferred`. The business concept “Preferred supplier for this component” is mapped to `SUPPLIER`, so preferred-status informa…

**Sources retrieved (12):** `Preferred supplier for this component→SUPPLIER`, `parent_chunk_data_dictionary.md_4`, `SHIPMENT→SUPPLIER`, `shipment type, source and destination locations, dates for ship, estimated arrival, and actual delivery, along with current status→SHIPMENT`, `components they can provide through approved supplier relationships→COMPONENT_SUPPLIER`, `parent_chunk_data_dictionary.md_8`, `COMPONENT_SUPPLIER→SUPPLIER`, `parent_chunk_data_dictionary.md_3`

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
> Warehouses are represented by the physical table `WAREHOUSE`, which models a physical storage location for materials, components, and finished goods.

In the schema, `WAREHOUSE` has these columns: `warehouse_id` as the primary key and unique warehouse identifier, `warehouse_name` as the required warehouse name, `address`, `city`, `state`, `capacity` as a required positive storage capacity with def…

**Sources retrieved (12):** `INVENTORY→WAREHOUSE`, `BATCH→WAREHOUSE`, `WORK_ORDER→WAREHOUSE`, `SHIPMENT→WAREHOUSE`, `parent_chunk_data_dictionary.md_6`, `parent_chunk_data_dictionary.md_5`, `geographic location information→WAREHOUSE`, `parent_chunk_data_dictionary.md_8`

**Context previews (first 3):**

1. _Relationship: INVENTORY references WAREHOUSE via foreign key WAREHOUSE_ID -> WAREHOUSE.WAREHOUSE_ID.…_

2. _Relationship: BATCH references WAREHOUSE via foreign key WAREHOUSE_ID -> WAREHOUSE.WAREHOUSE_ID.…_

3. _Relationship: WORK_ORDER references WAREHOUSE via foreign key WAREHOUSE_ID -> WAREHOUSE.WAREHOUSE_ID.…_

---

### ✅ QA-006 — What does the inventory table track?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.8179 | **Gate:** `proceed`

**Expected answer:**
> The inventory table tracks real-time stock levels including a unique record identifier (inventory_id), warehouse location (warehouse_id), component identifier for materials (component_id) or product identifier for finished goods (product_id), current physical stock quantity (quantity_on_hand), quant…

**System answer:**
> The `INVENTORY` table tracks stock levels of components and products at specific warehouse locations. It stores item-level inventory records tied to a `warehouse_id` and either a `component_id` or a `product_id`—these two are exclusive, so a record supports either a component or a product, not both.

From the context, it tracks:
- `quantity_on_hand`: available stock
- `quantity_reserved`: stock re…

**Sources retrieved (12):** `INVENTORY→PRODUCT`, `Inventory Records→INVENTORY`, `INVENTORY→WAREHOUSE`, `INVENTORY→COMPONENT`, `parent_chunk_data_dictionary.md_5`, `Traceability Batches→BATCH`, `parent_chunk_data_dictionary.md_7`, `parent_chunk_data_dictionary.md_8`

**Context previews (first 3):**

1. _Relationship: INVENTORY references PRODUCT via foreign key PRODUCT_ID -> PRODUCT.PRODUCT_ID.…_

2. _Business concept 'Inventory Records' — The table stores item-level inventory entries tied to a warehouse and either a component or product, with on-hand, reserved, reorder threshold, and restock date …_

3. _Relationship: INVENTORY references WAREHOUSE via foreign key WAREHOUSE_ID -> WAREHOUSE.WAREHOUSE_ID.…_

---

### ✅ QA-007 — How are work orders structured in the manufacturing system?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.5041 | **Gate:** `proceed`

**Expected answer:**
> Work orders represent production jobs with a unique identifier (work_order_id), product to be manufactured (product_id), optional parent work order for nested hierarchies (parent_work_order), quantity to produce (quantity_ordered), quantity completed so far (quantity_completed), current status (PEND…

**System answer:**
> Work orders are implemented by the physical table `WORK_ORDER` and represent production jobs for manufacturing products. The structure captures both the core job details and hierarchical relationships between jobs.

The table includes `work_order_id` as the primary key, `product_id` as a required foreign key to `PRODUCT.PRODUCT_ID`, and `warehouse_id` as a foreign key to `WAREHOUSE.WAREHOUSE_ID` t…

**Sources retrieved (12):** `Work Orders→WORK_ORDER`, `parent_chunk_data_dictionary.md_6`, `WORK_ORDER→PRODUCT`, `WORK_ORDER→WORK_ORDER`, `parent_chunk_data_dictionary.md_3`, `WORK_ORDER→WAREHOUSE`, `Route Steps→ROUTE`, `parent_chunk_data_dictionary.md_5`

**Context previews (first 3):**

1. _Business concept 'Work Orders' — The table is explicitly labeled as WORK_ORDER and contains core attributes of a production job: product, planned dates, quantities ordered/completed, status, priority,…_

2. _## work_order  Represents production jobs for manufacturing products with hierarchical work order support.  | Column | Data Type | Constraints | Description | |--------|-----------|-------------|-----…_

3. _Relationship: WORK_ORDER references PRODUCT via foreign key PRODUCT_ID -> PRODUCT.PRODUCT_ID.…_

---

### ✅ QA-008 — What information is captured in the shipment table?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.8695 | **Gate:** `proceed`

**Expected answer:**
> Shipments track material transfers with a unique identifier (shipment_id), shipment type (INBOUND from suppliers, OUTBOUND to customers, INTERNAL between warehouses), destination warehouse (warehouse_id), source supplier for inbound (supplier_id), destination customer for outbound (customer_id), shi…

**System answer:**
> The SHIPMENT table captures shipment type, source and destination location references, ship and delivery timing, and current shipment status. It is described as tracking material transfers between warehouses, suppliers, and customers.

Specifically, SHIPMENT stores:
shipment_id, the unique shipment identifier;
shipment_type, which can be INBOUND, OUTBOUND, or INTERNAL;
warehouse_id, a reference to…

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
> The quality control system records inspections in the `QUALITY_CONTROL` table, which implements the business concept “inspection and testing records for quality assurance.”

Each inspection record includes:
`qc_id`, `batch_id`, `specification_id`, `qc_date`, `qc_type`, `inspector_id`, `result`, `defect_count`, and `notes`.

From the glossary, these records capture inspection and testing activities…

**Sources retrieved (12):** `inspection and testing records for quality assurance→QUALITY_CONTROL`, `BOM→PRODUCT`, `Traceability Batches→BATCH`, `BATCH→PRODUCT`, `BATCH→WAREHOUSE`, `parent_chunk_business_glossary.md_2`, `inspection and testing records for quality assurance`, `parent_chunk_business_glossary.md_0`

**Context previews (first 3):**

1. _Business concept 'inspection and testing records for quality assurance' is implemented by physical table QUALITY_CONTROL (columns: qc_id, batch_id, specification_id, qc_date, qc_type, inspector_id, re…_

2. _Relationship: BOM references PRODUCT via foreign key COMPONENT_PRODUCT_ID -> PRODUCT.PRODUCT_ID.…_

3. _Business concept 'Traceability Batches' — The table stores production lot identifiers, product linkage, production date, quantity, warehouse, expiry date, and QC status, which matches batch-level trac…_

---

### ✅ QA-010 — What do specification records define?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.7558 | **Gate:** `proceed`

**Expected answer:**
> Specifications define technical requirements with a unique identifier (specification_id), descriptive name (specification_name), version number, effective date, specification type (DIMENSIONAL, MATERIAL, PERFORMANCE), critical parameter being measured (critical_parameter), acceptable minimum value (…

**System answer:**
> Specification records define the technical requirements, standards, and acceptance criteria for materials and products. In the `SPECIFICATION` table, they capture the specification name and version, effective date, specification type (`DIMENSIONAL`, `MATERIAL`, `PERFORMANCE`), the critical parameter being tested, acceptable minimum and maximum values, and the unit of measure. The context also stat…

**Sources retrieved (12):** `inspection and testing records for quality assurance→QUALITY_CONTROL`, `a standard cost, unit of measure, and may be associated with technical specifications that define quality requirements→SPECIFICATION`, `parent_chunk_data_dictionary.md_7`, `parent_chunk_data_dictionary.md_3`, `Inventory Records→INVENTORY`, `parent_chunk_business_glossary.md_2`, `parent_chunk_business_glossary.md_0`, `a standard cost, unit of measure, and may be associated with technical specifications that define quality requirements`

**Context previews (first 3):**

1. _Business concept 'inspection and testing records for quality assurance' is implemented by physical table QUALITY_CONTROL (columns: qc_id, batch_id, specification_id, qc_date, qc_type, inspector_id, re…_

2. _Business concept 'a standard cost, unit of measure, and may be associated with technical specifications that define quality requirements' is implemented by physical table SPECIFICATION (columns: speci…_

3. _## specification  Defines technical requirements and acceptance criteria for materials and products.  | Column | Data Type | Constraints | Description | |--------|-----------|-------------|-----------…_

---

### ✅ QA-011 — How can I find which suppliers provide specific components?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.3227 | **Gate:** `proceed`

**Expected answer:**
> Query the component_supplier table which links components to their approved suppliers. This table contains the component identifier (component_id), supplier identifier (supplier_id), preferred supplier flag (is_preferred), lead time in days (lead_time_days), and unit price (unit_price). Join with th…

**System answer:**
> Use the approved supplier relationship table `COMPONENT_SUPPLIER`.

The retrieved context says the business concept “components they can provide through approved supplier relationships” is implemented by `COMPONENT_SUPPLIER`, with columns `component_supplier_id`, `component_id`, `supplier_id`, `is_preferred`, `lead_time_days`, and `unit_price`.

To find which suppliers provide a specific component…

**Sources retrieved (12):** `components they can provide through approved supplier relationships→COMPONENT_SUPPLIER`, `parent_chunk_data_dictionary.md_5`, `parent_chunk_data_dictionary.md_4`, `parent_chunk_data_dictionary.md_3`, `parent_chunk_data_dictionary.md_8`, `components they can provide through approved supplier relationships`, `parent_chunk_business_glossary.md_0`, `parent_chunk_business_glossary.md_1`

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
> From the retrieved context, you can trace a work order to the product being manufactured, but you cannot fully determine the required components from the available schema details alone.

What is known is this: the `WORK_ORDER` table represents production jobs, and `work_order.product_id` is a foreign key to `product(product_id)`. So the first step is to identify the product on the work order throu…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_5`, `Work Orders→WORK_ORDER`, `parent_chunk_data_dictionary.md_6`, `parent_chunk_data_dictionary.md_3`, `components they can provide through approved supplier relationships→COMPONENT_SUPPLIER`, `parent_chunk_data_dictionary.md_8`, `parent_chunk_data_dictionary.md_7`, `parent_chunk_business_glossary.md_1`

**Context previews (first 3):**

1. _## warehouse  Stores physical storage location information for inventory management.  | Column | Data Type | Constraints | Description | |--------|-----------|-------------|-------------| | warehouse_…_

2. _Business concept 'Work Orders' — The table is explicitly labeled as WORK_ORDER and contains core attributes of a production job: product, planned dates, quantities ordered/completed, status, priority,…_

3. _## work_order  Represents production jobs for manufacturing products with hierarchical work order support.  | Column | Data Type | Constraints | Description | |--------|-----------|-------------|-----…_

---

### ✅ QA-013 — How can I identify which warehouses have available inventory for specific components?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.8215 | **Gate:** `proceed`

**Expected answer:**
> Query the inventory table filtered by component_id, joining with the warehouse table to get warehouse names and locations. Calculate available quantity as quantity_on_hand minus quantity_reserved. Filter for records where available quantity is greater than zero. Results show warehouse names, locatio…

**System answer:**
> Use the `INVENTORY` table as the starting point, because the business concept “Inventory Records” is implemented by `INVENTORY`, and each record is tied to a specific `warehouse_id` and either a `component_id` or a `product_id`. For your case, look for inventory rows where `component_id` is populated, because `INVENTORY.COMPONENT_ID` is a foreign key to `COMPONENT.COMPONENT_ID`, and the schema sta…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_5`, `Inventory Records→INVENTORY`, `INVENTORY→WAREHOUSE`, `INVENTORY→COMPONENT`, `parent_chunk_data_dictionary.md_3`, `parent_chunk_data_dictionary.md_8`, `parent_chunk_data_dictionary.md_6`, `parent_chunk_business_glossary.md_1`

**Context previews (first 3):**

1. _## warehouse  Stores physical storage location information for inventory management.  | Column | Data Type | Constraints | Description | |--------|-----------|-------------|-------------| | warehouse_…_

2. _Business concept 'Inventory Records' — The table stores item-level inventory entries tied to a warehouse and either a component or product, with on-hand, reserved, reorder threshold, and restock date …_

3. _Relationship: INVENTORY references WAREHOUSE via foreign key WAREHOUSE_ID -> WAREHOUSE.WAREHOUSE_ID.…_

---

### ✅ QA-014 — How do I find which shipments delivered materials from a specific supplier?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.2401 | **Gate:** `proceed`

**Expected answer:**
> Query the shipment table filtering by supplier_id and shipment_type = 'INBOUND'. Join with the warehouse table to show destination warehouses. Filter for status = 'DELIVERED' and include actual_arrival date. Results can be ordered by ship_date descending to show most recent deliveries first.

**System answer:**
> Use the `SHIPMENT` table as the starting point. The relevant relationship is `SHIPMENT.SUPPLIER_ID -> SUPPLIER.SUPPLIER_ID`.

To find shipments delivered from a specific supplier, filter `SHIPMENT` by:
`shipment.supplier_id = <specific supplier>`
and, because supplier-linked shipments are inbound, `shipment.shipment_type = 'INBOUND'`.
Then restrict to delivered shipments with `shipment.status = 'D…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_8`, `SHIPMENT→SUPPLIER`, `shipment type, source and destination locations, dates for ship, estimated arrival, and actual delivery, along with current status→SHIPMENT`, `parent_chunk_data_dictionary.md_5`, `parent_chunk_data_dictionary.md_3`, `parent_chunk_data_dictionary.md_4`, `components they can provide through approved supplier relationships→COMPONENT_SUPPLIER`, `parent_chunk_business_glossary.md_1`

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
> The knowledge graph contains schema-level metadata only, not the actual inspection records for a specific batch. Based on the schema, you would determine this by looking in the `QUALITY_CONTROL` table and filtering on the target `batch_id`.

`QUALITY_CONTROL` is the table for the business concept “inspection and testing records for quality assurance,” and it includes these relevant columns: `qc_id…

**Sources retrieved (12):** `inspection and testing records for quality assurance→QUALITY_CONTROL`, `Traceability Batches→BATCH`, `parent_chunk_data_dictionary.md_7`, `BATCH→PRODUCT`, `parent_chunk_data_dictionary.md_5`, `parent_chunk_data_dictionary.md_6`, `BATCH→WAREHOUSE`, `parent_chunk_business_glossary.md_2`

**Context previews (first 3):**

1. _Business concept 'inspection and testing records for quality assurance' is implemented by physical table QUALITY_CONTROL (columns: qc_id, batch_id, specification_id, qc_date, qc_type, inspector_id, re…_

2. _Business concept 'Traceability Batches' — The table stores production lot identifiers, product linkage, production date, quantity, warehouse, expiry date, and QC status, which matches batch-level trac…_

3. _## specification  Defines technical requirements and acceptance criteria for materials and products.  | Column | Data Type | Constraints | Description | |--------|-----------|-------------|-----------…_

---

### ✅ QA-016 — How do I track which work orders are in progress at a specific warehouse?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.7311 | **Gate:** `proceed`

**Expected answer:**
> Query the work_order table filtering by warehouse_id and status = 'IN_PROGRESS'. Join with the product table to get product names and types. Include quantity_ordered, quantity_completed, priority, planned_end_date, and calculate progress percentage as (quantity_completed / quantity_ordered * 100). O…

**System answer:**
> Use the `work_order` table, because it represents production jobs and includes both the work order `status` and the `warehouse_id` production location.

To track work orders that are in progress at a specific warehouse, filter `work_order` on:
`status = 'IN_PROGRESS'`
and the target `warehouse_id`.

The key columns in `work_order` for this are:
`work_order_id` for the job,
`product_id` for what is…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_5`, `parent_chunk_data_dictionary.md_6`, `WORK_ORDER→WAREHOUSE`, `Work Orders→WORK_ORDER`, `parent_chunk_data_dictionary.md_8`, `parent_chunk_data_dictionary.md_7`, `Inventory Records→INVENTORY`, `parent_chunk_business_glossary.md_1`

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
> Use the `INVENTORY` table, which implements the business concept “Inventory Records.” To find components that need reordering, filter inventory records where `component_id` is populated, because an inventory row tracks either a component or a product, exclusively. Then compare the current stock fields to the reorder trigger field in that same table.

At the schema level, the key columns are in `IN…

**Sources retrieved (12):** `Inventory Records→INVENTORY`, `parent_chunk_data_dictionary.md_5`, `INVENTORY→COMPONENT`, `parent_chunk_data_dictionary.md_3`, `parent_chunk_data_dictionary.md_4`, `parent_chunk_data_dictionary.md_6`, `components they can provide through approved supplier relationships→COMPONENT_SUPPLIER`, `parent_chunk_business_glossary.md_1`

**Context previews (first 3):**

1. _Business concept 'Inventory Records' — The table stores item-level inventory entries tied to a warehouse and either a component or product, with on-hand, reserved, reorder threshold, and restock date …_

2. _## warehouse  Stores physical storage location information for inventory management.  | Column | Data Type | Constraints | Description | |--------|-----------|-------------|-------------| | warehouse_…_

3. _Relationship: INVENTORY references COMPONENT via foreign key COMPONENT_ID -> COMPONENT.COMPONENT_ID.…_

---

### ✅ QA-018 — How do I determine the manufacturing route for a specific product?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0781 | **Gate:** `proceed_with_warning`

**Expected answer:**
> Query the route table filtering by product_id, ordered by sequence_number ascending. For each operation, retrieve operation_name, work_center, cycle_time_minutes, and setup_time_minutes. Join with the product table to get product details. The sequence of operations shows the complete manufacturing w…

**System answer:**
> To determine the manufacturing route for a specific product, use the ROUTE table. In the retrieved context, the business concept “Route Steps” is implemented by physical table ROUTE, and ROUTE references PRODUCT through the foreign key ROUTE.product_id → PRODUCT.product_id.

The route is stored at the step level, not as a separate higher-level workflow header. That means you identify the product i…

**Sources retrieved (12):** `Route Steps→ROUTE`, `parent_chunk_data_dictionary.md_6`, `ROUTE→PRODUCT`, `parent_chunk_data_dictionary.md_3`, `parent_chunk_data_dictionary.md_7`, `a unique identifier, name, type classification, base cost, and lead time for procurement or production→PRODUCT`, `Traceability Batches→BATCH`, `Route Steps`

**Context previews (first 3):**

1. _Business concept 'Route Steps' — The table has one row per ordered operation step, identified by sequence_number and operation_name, with work_center, cycle time, and setup time for each step. The pro…_

2. _## work_order  Represents production jobs for manufacturing products with hierarchical work order support.  | Column | Data Type | Constraints | Description | |--------|-----------|-------------|-----…_

3. _Relationship: ROUTE references PRODUCT via foreign key PRODUCT_ID -> PRODUCT.PRODUCT_ID.…_

---

### ✅ QA-019 — How can I find which batches are stored at a specific warehouse and their QC status?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.7533 | **Gate:** `proceed`

**Expected answer:**
> Query the batch table filtering by warehouse_id. Join with the product table to get product names and types. Include production_date, quantity_produced, expiry_date, and qc_status (PENDING, PASSED, FAILED, QUARANTINED). Filter by qc_status to isolate batches requiring quality attention or ready for …

**System answer:**
> Use the BATCH table, because it stores both the warehouse linkage and the batch QC status. In this schema, BATCH has the columns batch_id, product_id, production_date, quantity_produced, warehouse_id, expiry_date, and qc_status, and BATCH.warehouse_id is a foreign key to WAREHOUSE.warehouse_id.

So, at the schema level, the way to find batches stored at a specific warehouse is to query BATCH and f…

**Sources retrieved (12):** `Traceability Batches→BATCH`, `parent_chunk_data_dictionary.md_5`, `BATCH→WAREHOUSE`, `inspection and testing records for quality assurance→QUALITY_CONTROL`, `parent_chunk_data_dictionary.md_6`, `parent_chunk_data_dictionary.md_8`, `Inventory Records→INVENTORY`, `parent_chunk_data_dictionary.md_7`

**Context previews (first 3):**

1. _Business concept 'Traceability Batches' — The table stores production lot identifiers, product linkage, production date, quantity, warehouse, expiry date, and QC status, which matches batch-level trac…_

2. _## warehouse  Stores physical storage location information for inventory management.  | Column | Data Type | Constraints | Description | |--------|-----------|-------------|-------------| | warehouse_…_

3. _Relationship: BATCH references WAREHOUSE via foreign key WAREHOUSE_ID -> WAREHOUSE.WAREHOUSE_ID.…_

---

### ✅ QA-020 — How do I identify which specifications apply to specific components?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.2550 | **Gate:** `proceed`

**Expected answer:**
> Query the component table and join with the specification table via specification_id. Include component_name, component_category, and specification details (specification_name, spec_type, critical_parameter, min_value, max_value, unit_of_measure). This shows the technical requirements that each comp…

**System answer:**
> To identify which specifications apply to specific components, use the component-to-specification link in the schema: the `COMPONENT` table includes a `specification_id`, and the `SPECIFICATION` table is keyed by `specification_id`.

The join path is:
`COMPONENT.specification_id = SPECIFICATION.specification_id`

From the context, `COMPONENT` has these relevant columns: `component_id`, `component_…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_5`, `parent_chunk_data_dictionary.md_7`, `Product classification: FINISHED_GOOD, ASSEMBLY, COMPONENT→COMPONENT`, `parent_chunk_data_dictionary.md_3`, `a standard cost, unit of measure, and may be associated with technical specifications that define quality requirements→SPECIFICATION`, `parent_chunk_data_dictionary.md_4`, `components they can provide through approved supplier relationships→COMPONENT_SUPPLIER`, `parent_chunk_business_glossary.md_0`

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
> Use the `bom` table as the recursive structure and the `product` table to identify the finished product and describe each returned item.

A complete BOM explosion, based strictly on the schema provided, means recursively traversing `bom` from a finished product down through all of its nested assemblies and components:

Start with the target finished product in `product`, where `product.product_id`…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_4`, `parent_chunk_data_dictionary.md_3`, `BOM entry→BOM`, `BOM→PRODUCT`, `Product classification: FINISHED_GOOD, ASSEMBLY, COMPONENT→COMPONENT`, `parent_chunk_data_dictionary.md_7`, `parent_chunk_data_dictionary.md_6`, `parent_chunk_data_dictionary.md_8`

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
> Use the `BOM` table as the primary roll-up structure, not just `PRODUCT.parent_product_id`, because `BOM` is the table that explicitly defines composition and quantities for multi-level assemblies.

The schema-supported calculation path is:

Start with the target product in `PRODUCT` using `PRODUCT.product_id`. Find its immediate children in `BOM` where `BOM.parent_product_id = PRODUCT.product_id`…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_3`, `parent_chunk_data_dictionary.md_4`, `Product classification: FINISHED_GOOD, ASSEMBLY, COMPONENT→COMPONENT`, `parent_chunk_data_dictionary.md_7`, `parent_chunk_data_dictionary.md_8`, `parent_chunk_data_dictionary.md_6`, `a unique identifier, name, type classification, base cost, and lead time for procurement or production→PRODUCT`, `Work Orders→WORK_ORDER`

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
> Use the `bom` table and traverse it recursively upward through `parent_product_id` and `component_product_id`.

The retrieved context says `bom` defines product composition and supports recursive relationships for multi-level assemblies. In `bom`, both `parent_product_id` and `component_product_id` reference `product(product_id)`, which enables structures such as `Bicycle → Wheel → Spoke`.

To fin…

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
> To identify work orders that require a specific component while accounting for nested sub-assemblies, use the `BOM` structure to resolve product composition and then join that result to `WORK_ORDER`.

The core path is `WORK_ORDER.PRODUCT_ID -> PRODUCT.PRODUCT_ID`, combined with recursive traversal of `BOM`, where both `BOM.PARENT_PRODUCT_ID` and `BOM.COMPONENT_PRODUCT_ID` reference `PRODUCT.PRODUC…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_6`, `parent_chunk_data_dictionary.md_5`, `parent_chunk_data_dictionary.md_3`, `Work Orders→WORK_ORDER`, `parent_chunk_data_dictionary.md_4`, `WORK_ORDER→WORK_ORDER`, `WORK_ORDER→PRODUCT`, `parent_chunk_business_glossary.md_1`

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
> Use the `bom` table. The context explicitly says `bom_level` is the “depth in product hierarchy,” is `NOT NULL`, defaults to `0`, and has a check `>= 0`. It also says `bom_level` “tracks depth for performance optimization,” and the `idx_bom_level` index exists for hierarchical queries.

To determine the maximum BOM depth:

For a specific product, use `BOM.parent_product_id` to identify the product…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_4`, `parent_chunk_data_dictionary.md_3`, `BOM entry→BOM`, `BOM→PRODUCT`, `parent_chunk_data_dictionary.md_7`, `parent_chunk_data_dictionary.md_5`, `parent_chunk_data_dictionary.md_6`, `parent_chunk_data_dictionary.md_8`

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
> To find all products that have a specific product as a sub-assembly at any level, use the `bom` table as the hierarchy path and recurse upward through it.

In this schema, `bom.parent_product_id` is the product being built, and `bom.component_product_id` is the product that goes into it. Both columns reference `product(product_id)`, and the dictionary explicitly says this supports multi-level asse…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_3`, `parent_chunk_data_dictionary.md_4`, `parent_chunk_data_dictionary.md_5`, `Product classification: FINISHED_GOOD, ASSEMBLY, COMPONENT→COMPONENT`, `parent_chunk_data_dictionary.md_7`, `BOM entry→BOM`, `Inventory Records→INVENTORY`, `parent_chunk_data_dictionary.md_8`

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
> From the retrieved context, the schema supports this by traversing the product hierarchy and reading `lead_time_days` from `PRODUCT`.

The strongest schema path is through `BOM`, because `BOM` explicitly defines composition: `bom.parent_product_id` is the product being built, and `bom.component_product_id` is the product that goes into it. Both columns reference `PRODUCT(product_id)`, and `bom_lev…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_3`, `a unique identifier, name, type classification, base cost, and lead time for procurement or production→PRODUCT`, `components they can provide through approved supplier relationships→COMPONENT_SUPPLIER`, `parent_chunk_data_dictionary.md_4`, `parent_chunk_data_dictionary.md_7`, `parent_chunk_data_dictionary.md_6`, `parent_chunk_data_dictionary.md_8`, `Route Steps→ROUTE`

**Context previews (first 3):**

1. _# Manufacturing Data Dictionary  This data dictionary documents the database schema for the manufacturing supply chain system. It includes all tables, columns, data types, constraints, and relationshi…_

2. _Business concept 'a unique identifier, name, type classification, base cost, and lead time for procurement or production' is implemented by physical table PRODUCT (columns: product_id, product_name, p…_

3. _Business concept 'components they can provide through approved supplier relationships' is implemented by physical table COMPONENT_SUPPLIER (columns: component_supplier_id, component_id, supplier_id, i…_

---

### ✅ QA-028 — How do I generate a complete indented BOM report showing the hierarchical structure?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.4180 | **Gate:** `proceed`

**Expected answer:**
> Use a recursive query on the bom table that tracks the current depth level. Start with the top-level product (parent_product_id where product has no parent_product_id). At each level, output component details indented by depth level. Include product_name, quantity, and unit_of_measure. Recursively p…

**System answer:**
> Use the `bom` table as the backbone of the report, because it is the structure that “defines product composition and hierarchical structure” and “supports recursive relationships for multi-level assemblies.”

To generate a complete indented BOM report, start from a top-level product in `product.product_id` and then recursively traverse `bom` rows where `bom.parent_product_id` equals that product. …

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_4`, `parent_chunk_data_dictionary.md_3`, `parent_chunk_data_dictionary.md_6`, `parent_chunk_data_dictionary.md_8`, `BOM entry→BOM`, `BOM→PRODUCT`, `Work Orders→WORK_ORDER`, `Route Steps→ROUTE`

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
> Use the `bom` table as the source, because each BOM entry is one component used in one parent product. To find which components appear most frequently across all BOMs, count how many `bom` rows reference each `component_product_id`.

The core logic is:

`bom.component_product_id` → group by this column → count rows

That tells you how often a given product is used as a component in BOM structures.…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_4`, `parent_chunk_data_dictionary.md_3`, `BOM entry→BOM`, `BOM→PRODUCT`, `parent_chunk_data_dictionary.md_5`, `Product classification: FINISHED_GOOD, ASSEMBLY, COMPONENT→COMPONENT`, `Inventory Records→INVENTORY`, `parent_chunk_data_dictionary.md_7`

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
> The retrieved context does not define a circular-reference detection method or an infinite-loop prevention algorithm for the `bom` structure.

What it does say is that `bom` is the Bill of Materials table for product composition and hierarchical structure, and it “supports recursive relationships for multi-level assemblies.” The relevant columns are `parent_product_id` and `component_product_id`, …

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_4`, `parent_chunk_data_dictionary.md_3`, `BOM→PRODUCT`, `BOM entry→BOM`, `parent_chunk_data_dictionary.md_8`, `Route Steps→ROUTE`, `parent_chunk_data_dictionary.md_7`, `parent_chunk_data_dictionary.md_6`

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
> Use the product hierarchy and BOM recursion first, then attach supplier relationships where the exploded item is a component.

At the product-structure level, the complete sub-assembly chain is modeled in two places. The `product` table stores each item with `product_id`, `product_name`, `product_type`, `parent_product_id`, `base_cost`, `lead_time_days`, and `is_active`. Its self-reference on `par…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_3`, `Product classification: FINISHED_GOOD, ASSEMBLY, COMPONENT→COMPONENT`, `parent_chunk_data_dictionary.md_4`, `parent_chunk_data_dictionary.md_8`, `components they can provide through approved supplier relationships→COMPONENT_SUPPLIER`, `Route Steps→ROUTE`, `Preferred supplier for this component→SUPPLIER`, `a unique identifier, name, type classification, base cost, and lead time for procurement or production→PRODUCT`

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
> From the schema and business concepts provided, you can check this at the schema level by tracing a work order’s product into item-level inventory records and aggregating inventory across warehouses.

Start with `WORK_ORDER`, because it identifies what is being produced and in what quantity. The relevant columns are `work_order_id`, `product_id`, `quantity_ordered`, `quantity_completed`, `status`,…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_5`, `parent_chunk_data_dictionary.md_6`, `Inventory Records→INVENTORY`, `INVENTORY→WAREHOUSE`, `Work Orders→WORK_ORDER`, `WORK_ORDER→WAREHOUSE`, `parent_chunk_data_dictionary.md_8`, `parent_chunk_business_glossary.md_1`

**Context previews (first 3):**

1. _## warehouse  Stores physical storage location information for inventory management.  | Column | Data Type | Constraints | Description | |--------|-----------|-------------|-------------| | warehouse_…_

2. _## work_order  Represents production jobs for manufacturing products with hierarchical work order support.  | Column | Data Type | Constraints | Description | |--------|-----------|-------------|-----…_

3. _Business concept 'Inventory Records' — The table stores item-level inventory entries tied to a warehouse and either a component or product, with on-hand, reserved, reorder threshold, and restock date …_

---

### ✅ QA-033 — How can I find which quality control inspections failed for components from specific suppliers?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.4561 | **Gate:** `proceed`

**Expected answer:**
> Query the quality_control table filtering by result = 'FAIL'. Join with the batch table to get product_id and production_date. Join with the bom table recursively to trace which products contain failed components. Join with component_supplier and supplier tables to identify the source supplier. Filt…

**System answer:**
> From the retrieved context, you can identify failed quality inspections at the batch level, but you can only partially connect them to suppliers.

The failure records are stored in `QUALITY_CONTROL`, which has `qc_id`, `batch_id`, `specification_id`, `qc_date`, `qc_type`, `inspector_id`, `result`, `defect_count`, and `notes`. The business meaning confirms that QC results can be `PASS`, `FAIL`, or …

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_5`, `parent_chunk_data_dictionary.md_3`, `inspection and testing records for quality assurance→QUALITY_CONTROL`, `components they can provide through approved supplier relationships→COMPONENT_SUPPLIER`, `parent_chunk_data_dictionary.md_4`, `COMPONENT_SUPPLIER→SUPPLIER`, `parent_chunk_data_dictionary.md_8`, `parent_chunk_data_dictionary.md_7`

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
> To calculate total manufacturing time for a work order including all sub-assembly work orders, the retrieved context supports a schema-level approach based on the WORK_ORDER hierarchy and the ROUTE step times.

Use WORK_ORDER as the starting point. The root work order is identified by WORK_ORDER.work_order_id. To include sub-assembly work orders, recursively traverse WORK_ORDER.parent_work_order →…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_6`, `parent_chunk_data_dictionary.md_3`, `Work Orders→WORK_ORDER`, `Route Steps→ROUTE`, `parent_chunk_data_dictionary.md_7`, `parent_chunk_data_dictionary.md_4`, `WORK_ORDER→PRODUCT`, `parent_chunk_business_glossary.md_0`

**Context previews (first 3):**

1. _## work_order  Represents production jobs for manufacturing products with hierarchical work order support.  | Column | Data Type | Constraints | Description | |--------|-----------|-------------|-----…_

2. _# Manufacturing Data Dictionary  This data dictionary documents the database schema for the manufacturing supply chain system. It includes all tables, columns, data types, constraints, and relationshi…_

3. _Business concept 'Work Orders' — The table is explicitly labeled as WORK_ORDER and contains core attributes of a production job: product, planned dates, quantities ordered/completed, status, priority,…_

---

### ✅ QA-035 — How can I identify which shipments are overdue and their impact on work orders?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0719 | **Gate:** `proceed_with_warning`

**Expected answer:**
> Query the shipment table filtering for status = 'SHIPPED' where actual_arrival is NULL and estimated_arrival is in the past (overdue). Join with the component_supplier table via supplier_id and component_id to identify which components are delayed. Perform reverse BOM lookup to find which parent pro…

**System answer:**
> Based on the retrieved context alone, I cannot determine which shipments are “overdue,” because no overdue definition is provided.

What the context does provide is the `SHIPMENT` schema: `shipment_id`, `shipment_type`, `warehouse_id`, `supplier_id`, `customer_id`, `ship_date`, `estimated_arrival`, `actual_arrival`, and `status`. The allowed `status` values are `PENDING`, `SHIPPED`, `DELIVERED`, a…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_5`, `parent_chunk_data_dictionary.md_8`, `parent_chunk_data_dictionary.md_6`, `Work Orders→WORK_ORDER`, `WORK_ORDER→PRODUCT`, `WORK_ORDER→WAREHOUSE`, `shipment type, source and destination locations, dates for ship, estimated arrival, and actual delivery, along with current status→SHIPMENT`, `SHIPMENT→WAREHOUSE`

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
> Use the `BATCH` table for the expiry side of the question. `BATCH` implements the traceability batch concept and includes `batch_id`, `product_id`, `production_date`, `quantity_produced`, `warehouse_id`, `expiry_date`, and `qc_status`. To find batches approaching or past expiry, filter on `BATCH.expiry_date`; the context does not define what time window counts as “approaching,” so that cutoff has …

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_5`, `Traceability Batches→BATCH`, `parent_chunk_data_dictionary.md_7`, `parent_chunk_data_dictionary.md_3`, `parent_chunk_data_dictionary.md_8`, `components they can provide through approved supplier relationships→COMPONENT_SUPPLIER`, `parent_chunk_data_dictionary.md_4`, `parent_chunk_business_glossary.md_2`

**Context previews (first 3):**

1. _## warehouse  Stores physical storage location information for inventory management.  | Column | Data Type | Constraints | Description | |--------|-----------|-------------|-------------| | warehouse_…_

2. _Business concept 'Traceability Batches' — The table stores production lot identifiers, product linkage, production date, quantity, warehouse, expiry date, and QC status, which matches batch-level trac…_

3. _## specification  Defines technical requirements and acceptance criteria for materials and products.  | Column | Data Type | Constraints | Description | |--------|-----------|-------------|-----------…_

---

### ✅ QA-037 — How can I generate a material requirements plan showing when to order components based on work order schedules?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0433 | **Gate:** `proceed_with_warning`

**Expected answer:**
> Query all work_orders with status 'PENDING' ordered by planned_start_date. For each work_order, perform BOM explosion to get required components and quantities. For each component, query inventory for current available stock across warehouses. Calculate net requirements = (required quantity * work_o…

**System answer:**
> Use `WORK_ORDER` as the driver for the plan. The core join path supported by the retrieved context is `WORK_ORDER.product_id -> BOM.parent_product_id` to explode each scheduled production job into its required component products, and then `BOM.component_product_id -> PRODUCT.product_id` to get the component item attributes, especially `PRODUCT.lead_time_days`.

A practical schema-level approach is…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_6`, `parent_chunk_data_dictionary.md_7`, `Work Orders→WORK_ORDER`, `parent_chunk_data_dictionary.md_5`, `parent_chunk_data_dictionary.md_4`, `parent_chunk_data_dictionary.md_3`, `components they can provide through approved supplier relationships→COMPONENT_SUPPLIER`, `WORK_ORDER→WORK_ORDER`

**Context previews (first 3):**

1. _## work_order  Represents production jobs for manufacturing products with hierarchical work order support.  | Column | Data Type | Constraints | Description | |--------|-----------|-------------|-----…_

2. _## specification  Defines technical requirements and acceptance criteria for materials and products.  | Column | Data Type | Constraints | Description | |--------|-----------|-------------|-----------…_

3. _Business concept 'Work Orders' — The table is explicitly labeled as WORK_ORDER and contains core attributes of a production job: product, planned dates, quantities ordered/completed, status, priority,…_

---

### ✅ QA-038 — How do I trace the complete genealogy of a component from supplier through batch to finished goods?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0748 | **Gate:** `proceed_with_warning`

**Expected answer:**
> Start with a shipment from the supplier (shipment table with supplier_id and shipment_type = 'INBOUND'). Track to inventory updates via component_id and warehouse_id. Identify batches that consumed the component via reverse BOM lookup (batch.product_id → bom hierarchy → component_id). Query quality_…

**System answer:**
> The retrieved context supports this only partially, and only at the schema level, not with actual record-level genealogy data.

To trace from supplier to the sourced part, the starting point is the approved supplier relationship in `COMPONENT_SUPPLIER`, which has `component_id`, `supplier_id`, `is_preferred`, `lead_time_days`, and `unit_price`. You would join `COMPONENT_SUPPLIER.component_id` to `…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_3`, `Product classification: FINISHED_GOOD, ASSEMBLY, COMPONENT→COMPONENT`, `parent_chunk_data_dictionary.md_5`, `parent_chunk_data_dictionary.md_8`, `parent_chunk_data_dictionary.md_4`, `Traceability Batches→BATCH`, `components they can provide through approved supplier relationships→COMPONENT_SUPPLIER`, `parent_chunk_business_glossary.md_2`

**Context previews (first 3):**

1. _# Manufacturing Data Dictionary  This data dictionary documents the database schema for the manufacturing supply chain system. It includes all tables, columns, data types, constraints, and relationshi…_

2. _Business concept 'Product classification: FINISHED_GOOD, ASSEMBLY, COMPONENT' is implemented by physical table COMPONENT (columns: component_id, component_name, component_category, unit_of_measure, st…_

3. _## warehouse  Stores physical storage location information for inventory management.  | Column | Data Type | Constraints | Description | |--------|-----------|-------------|-------------| | warehouse_…_

---

### ✅ QA-039 — How can I find alternative suppliers for components that are critical for multiple products?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0772 | **Gate:** `proceed_with_warning`

**Expected answer:**
> Perform BOM explosion for all active products and count component usage frequency. Identify high-frequency components. Query component_supplier table to find all suppliers for these components. Filter to suppliers with rating >= 4.0 (high quality) and is_preferred = 'Y'. For each component, list alt…

**System answer:**
> This is only partially answerable from the retrieved context.

To identify components that are used by multiple products, the explicitly documented path is through `bom` and `product`. In `bom`, both `parent_product_id` and `component_product_id` are foreign keys to `product(product_id)`, and `product.product_type` can be `FINISHED_GOOD`, `ASSEMBLY`, or `COMPONENT`. So, at the product-structure le…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_4`, `parent_chunk_data_dictionary.md_3`, `components they can provide through approved supplier relationships→COMPONENT_SUPPLIER`, `Preferred supplier for this component→SUPPLIER`, `parent_chunk_data_dictionary.md_5`, `parent_chunk_data_dictionary.md_8`, `COMPONENT_SUPPLIER→COMPONENT`, `parent_chunk_business_glossary.md_0`

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
> The retrieved context does not define a “total landed cost” formula, so it is not possible to give a complete calculation for landed cost including manufacturing operations from the knowledge graph alone.

What is known from the context is this: product cost can be partially modeled from the `product` and `bom` tables. `product` contains `product_id`, `product_name`, `product_type`, `base_cost`, a…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_3`, `a unique identifier, name, type classification, base cost, and lead time for procurement or production→PRODUCT`, `components they can provide through approved supplier relationships→COMPONENT_SUPPLIER`, `parent_chunk_data_dictionary.md_6`, `parent_chunk_data_dictionary.md_7`, `parent_chunk_data_dictionary.md_8`, `Product classification: FINISHED_GOOD, ASSEMBLY, COMPONENT→COMPONENT`, `parent_chunk_data_dictionary.md_4`

**Context previews (first 3):**

1. _# Manufacturing Data Dictionary  This data dictionary documents the database schema for the manufacturing supply chain system. It includes all tables, columns, data types, constraints, and relationshi…_

2. _Business concept 'a unique identifier, name, type classification, base cost, and lead time for procurement or production' is implemented by physical table PRODUCT (columns: product_id, product_name, p…_

3. _Business concept 'components they can provide through approved supplier relationships' is implemented by physical table COMPONENT_SUPPLIER (columns: component_supplier_id, component_id, supplier_id, i…_

---

## Anomalies & Observations

No anomalies detected. All questions grounded with acceptable RAGAS scores.
