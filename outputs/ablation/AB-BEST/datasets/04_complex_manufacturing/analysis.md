# AB-BEST — 04_complex_manufacturing — Run Analysis

**Timestamp:** 2026-04-21 21:03:08  
**Run tag:** `run-20260421_221024`

## Configuration

| Parameter | Value |
|-----------|-------|
| Extraction model | `LLM (openai/gpt-4.1-nano)` |
| Reasoning model | `openai/gpt-oss-120b` |
| Embedding model | `BAAI/bge-m3` |
| Retrieval mode | `hybrid` |
| Reranker | `True` |
| Reranker top_k | `20` |
| Chunk size / overlap | `128 / 16` |
| ER similarity threshold | `0.65` |

## Builder Results

| Metric | Value |
|--------|-------|
| Triplets extracted | 80 |
| Entities resolved | 22 |
| Tables parsed | 13 |
| Tables completed | 13 |

## Query Evaluation Summary

| Metric | Value |
|--------|-------|
| Questions | 40 |
| Grounded | **40/40 (100%)** |
| Avg GT Coverage | N/A |
| Avg Top Score | 0.4547 |
| Avg Chunk Count | 20.0 |
| Abstained | 0 |

## RAGAS Metrics

RAGAS evaluation not enabled for this run.

## Per-Question Deep Dive

### ✅ QA-001 — What information is stored about products in the manufacturing system?

**Status:** GROUNDED  
**GT Coverage:** N/A | **Top Score:** 0.0000 | **Gate:** `proceed`

**Expected answer:**
> Products are tracked with a unique identifier (product_id), descriptive name (product_name), classification as finished good, assembly, or component (product_type), optional parent product reference for hierarchical structures (parent_product_id), standard unit cost (base_cost), typical procurement …

**System answer:**
> 

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_3`, `Component→COMPONENT`, `Production Batch→BATCH`, `parent_chunk_data_dictionary.md_6`, `Stock Levels→INVENTORY`, `Manufacturing Route→ROUTE`, `parent_chunk_data_dictionary.md_5`, `Warehouse→WAREHOUSE`

---

### ✅ QA-002 — How are components defined in the manufacturing database?

**Status:** GROUNDED  
**GT Coverage:** N/A | **Top Score:** 0.0000 | **Gate:** `proceed`

**Expected answer:**
> Components are defined with a unique identifier (component_id), descriptive name (component_name), category grouping (component_category), unit of measure (unit_of_measure), standard unit cost (standard_cost), and optional reference to technical specifications (specification_id). Components represen…

**System answer:**
> 

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_3`, `Component→COMPONENT`, `Bill Of Materials (Bom)→BOM`, `parent_chunk_data_dictionary.md_4`, `parent_chunk_data_dictionary.md_5`, `Production Batch→BATCH`, `Manufacturing Route→ROUTE`, `parent_chunk_business_glossary.md_0`

---

### ✅ QA-003 — What is the purpose of the Bill of Materials (BOM) table?

**Status:** GROUNDED  
**GT Coverage:** N/A | **Top Score:** 0.0000 | **Gate:** `proceed`

**Expected answer:**
> The BOM table defines the hierarchical structure of products by specifying which components or sub-assemblies are required to manufacture each parent product. It records the unique BOM entry identifier (bom_id), parent product being built (parent_product_id), component or sub-assembly product (compo…

**System answer:**
> 

**Sources retrieved (12):** `Bill Of Materials (Bom)→BOM`, `parent_chunk_data_dictionary.md_4`, `BOM→PRODUCT`, `parent_chunk_data_dictionary.md_3`, `parent_chunk_data_dictionary.md_8`, `Bill Of Materials (Bom)`, `Component→COMPONENT`, `Supplier→SUPPLIER`

---

### ✅ QA-004 — What supplier information does the system maintain?

**Status:** GROUNDED  
**GT Coverage:** N/A | **Top Score:** 0.0000 | **Gate:** `proceed`

**Expected answer:**
> Suppliers are tracked with a unique identifier (supplier_id), legal business name (supplier_name), primary contact email (contact_email), primary contact phone number (contact_phone), performance rating from 1.0 to 5.0 (rating), and preferred supplier status flag (is_preferred).

**System answer:**
> 

**Sources retrieved (12):** `Supplier→SUPPLIER`, `Component Supplier→COMPONENT_SUPPLIER`, `Physical Transfer→SHIPMENT`, `parent_chunk_data_dictionary.md_4`, `SHIPMENT→SUPPLIER`, `parent_chunk_data_dictionary.md_8`, `COMPONENT_SUPPLIER→SUPPLIER`, `parent_chunk_data_dictionary.md_3`

---

### ✅ QA-005 — How are warehouses represented in the schema?

**Status:** GROUNDED  
**GT Coverage:** N/A | **Top Score:** 0.0000 | **Gate:** `proceed`

**Expected answer:**
> Warehouses are defined with a unique identifier (warehouse_id), descriptive name (warehouse_name), full street address (address), city location (city), state or province (state), total storage capacity in cubic meters (capacity), and optional manager identifier (manager_id).

**System answer:**
> 

**Sources retrieved (12):** `Physical Transfer→SHIPMENT`, `parent_chunk_data_dictionary.md_8`, `Stock Levels→INVENTORY`, `parent_chunk_business_glossary.md_1`, `Physical Transfer`, `parent_chunk_business_glossary.md_2`, `Stock Levels`, `INVENTORY→WAREHOUSE`

---

### ✅ QA-006 — What does the inventory table track?

**Status:** GROUNDED  
**GT Coverage:** N/A | **Top Score:** 0.0000 | **Gate:** `proceed`

**Expected answer:**
> The inventory table tracks real-time stock levels including a unique record identifier (inventory_id), warehouse location (warehouse_id), component identifier for materials (component_id) or product identifier for finished goods (product_id), current physical stock quantity (quantity_on_hand), quant…

**System answer:**
> 

**Sources retrieved (12):** `Stock Levels→INVENTORY`, `INVENTORY→PRODUCT`, `INVENTORY→WAREHOUSE`, `INVENTORY→COMPONENT`, `parent_chunk_data_dictionary.md_5`, `Production Batch→BATCH`, `parent_chunk_data_dictionary.md_7`, `parent_chunk_data_dictionary.md_8`

---

### ✅ QA-007 — How are work orders structured in the manufacturing system?

**Status:** GROUNDED  
**GT Coverage:** N/A | **Top Score:** 0.0000 | **Gate:** `proceed`

**Expected answer:**
> Work orders represent production jobs with a unique identifier (work_order_id), product to be manufactured (product_id), optional parent work order for nested hierarchies (parent_work_order), quantity to produce (quantity_ordered), quantity completed so far (quantity_completed), current status (PEND…

**System answer:**
> 

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_6`, `Operation Name Work→WORK_ORDER`, `WORK_ORDER→PRODUCT`, `WORK_ORDER→WORK_ORDER`, `parent_chunk_data_dictionary.md_3`, `WORK_ORDER→WAREHOUSE`, `Manufacturing Route→ROUTE`, `parent_chunk_data_dictionary.md_5`

---

### ✅ QA-008 — What information is captured in the shipment table?

**Status:** GROUNDED  
**GT Coverage:** N/A | **Top Score:** 0.0000 | **Gate:** `proceed`

**Expected answer:**
> Shipments track material transfers with a unique identifier (shipment_id), shipment type (INBOUND from suppliers, OUTBOUND to customers, INTERNAL between warehouses), destination warehouse (warehouse_id), source supplier for inbound (supplier_id), destination customer for outbound (customer_id), shi…

**System answer:**
> 

**Sources retrieved (12):** `Physical Transfer→SHIPMENT`, `SHIPMENT→WAREHOUSE`, `SHIPMENT→SUPPLIER`, `parent_chunk_data_dictionary.md_8`, `parent_chunk_data_dictionary.md_5`, `Physical Transfer`, `parent_chunk_business_glossary.md_0`, `parent_chunk_business_glossary.md_1`

---

### ✅ QA-009 — How does the quality control system record inspections?

**Status:** GROUNDED  
**GT Coverage:** N/A | **Top Score:** 0.0000 | **Gate:** `proceed`

**Expected answer:**
> Quality control records are stored with a unique identifier (qc_id), associated production batch (batch_id), applicable specification requirements (specification_id), inspection date (qc_date), inspection type (INCOMING for supplier materials, IN_PROCESS during manufacturing, FINAL for finished good…

**System answer:**
> 

**Sources retrieved (12):** `Quality Control (Qc)→QUALITY_CONTROL`, `BOM→PRODUCT`, `Production Batch→BATCH`, `BATCH→PRODUCT`, `BATCH→WAREHOUSE`, `PRODUCT→PRODUCT`, `parent_chunk_data_dictionary.md_6`, `parent_chunk_business_glossary.md_2`

---

### ✅ QA-010 — What do specification records define?

**Status:** GROUNDED  
**GT Coverage:** N/A | **Top Score:** 0.0000 | **Gate:** `proceed`

**Expected answer:**
> Specifications define technical requirements with a unique identifier (specification_id), descriptive name (specification_name), version number, effective date, specification type (DIMENSIONAL, MATERIAL, PERFORMANCE), critical parameter being measured (critical_parameter), acceptable minimum value (…

**System answer:**
> 

**Sources retrieved (12):** `Specification→SPECIFICATION`, `parent_chunk_data_dictionary.md_7`, `Quality Control (Qc)→QUALITY_CONTROL`, `Component→COMPONENT`, `Physical Transfer→SHIPMENT`, `parent_chunk_data_dictionary.md_3`, `parent_chunk_business_glossary.md_2`, `Specification`

---

### ✅ QA-011 — How can I find which suppliers provide specific components?

**Status:** GROUNDED  
**GT Coverage:** N/A | **Top Score:** 0.0000 | **Gate:** `proceed`

**Expected answer:**
> Query the component_supplier table which links components to their approved suppliers. This table contains the component identifier (component_id), supplier identifier (supplier_id), preferred supplier flag (is_preferred), lead time in days (lead_time_days), and unit price (unit_price). Join with th…

**System answer:**
> 

**Sources retrieved (12):** `Component Supplier→COMPONENT_SUPPLIER`, `Supplier→SUPPLIER`, `parent_chunk_data_dictionary.md_5`, `parent_chunk_data_dictionary.md_4`, `parent_chunk_data_dictionary.md_3`, `Bill Of Materials (Bom)→BOM`, `Component→COMPONENT`, `parent_chunk_data_dictionary.md_8`

---

### ✅ QA-012 — How do I trace which components are needed to fulfill a work order?

**Status:** GROUNDED  
**GT Coverage:** N/A | **Top Score:** 0.0000 | **Gate:** `proceed`

**Expected answer:**
> Start with the work_order table to get the product_id being manufactured. Join to the bom table using product_id as parent_product_id to find all direct components and sub-assemblies. For each component_product_id, if it is an ASSEMBLY type product, recursively query the bom table again to explode m…

**System answer:**
> 

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_5`, `parent_chunk_data_dictionary.md_6`, `Operation Name Work→WORK_ORDER`, `Bill Of Materials (Bom)→BOM`, `Component→COMPONENT`, `Stock Levels→INVENTORY`, `parent_chunk_data_dictionary.md_3`, `parent_chunk_data_dictionary.md_8`

---

### ✅ QA-013 — How can I identify which warehouses have available inventory for specific components?

**Status:** GROUNDED  
**GT Coverage:** N/A | **Top Score:** 0.0000 | **Gate:** `proceed`

**Expected answer:**
> Query the inventory table filtered by component_id, joining with the warehouse table to get warehouse names and locations. Calculate available quantity as quantity_on_hand minus quantity_reserved. Filter for records where available quantity is greater than zero. Results show warehouse names, locatio…

**System answer:**
> 

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_5`, `Stock Levels→INVENTORY`, `INVENTORY→WAREHOUSE`, `INVENTORY→COMPONENT`, `parent_chunk_data_dictionary.md_3`, `parent_chunk_data_dictionary.md_8`, `parent_chunk_data_dictionary.md_6`, `Production Batch→BATCH`

---

### ✅ QA-014 — How do I find which shipments delivered materials from a specific supplier?

**Status:** GROUNDED  
**GT Coverage:** N/A | **Top Score:** 0.0000 | **Gate:** `proceed`

**Expected answer:**
> Query the shipment table filtering by supplier_id and shipment_type = 'INBOUND'. Join with the warehouse table to show destination warehouses. Filter for status = 'DELIVERED' and include actual_arrival date. Results can be ordered by ship_date descending to show most recent deliveries first.

**System answer:**
> 

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_8`, `SHIPMENT→SUPPLIER`, `Physical Transfer→SHIPMENT`, `parent_chunk_data_dictionary.md_5`, `Component Supplier→COMPONENT_SUPPLIER`, `Supplier→SUPPLIER`, `parent_chunk_data_dictionary.md_7`, `parent_chunk_data_dictionary.md_3`

---

### ✅ QA-015 — How can I determine which quality control inspections were performed on a specific production batch?

**Status:** GROUNDED  
**GT Coverage:** N/A | **Top Score:** 0.0000 | **Gate:** `proceed`

**Expected answer:**
> Query the quality_control table filtered by batch_id. Join with the specification table to get requirement details (specification_name, spec_type, acceptable ranges). Include qc_date, qc_type (INCOMING, IN_PROCESS, FINAL), result (PASS, FAIL, CONDITIONAL), and defect_count. This shows the complete i…

**System answer:**
> 

**Sources retrieved (12):** `Quality Control (Qc)→QUALITY_CONTROL`, `Production Batch→BATCH`, `parent_chunk_data_dictionary.md_7`, `BATCH→PRODUCT`, `parent_chunk_data_dictionary.md_5`, `parent_chunk_data_dictionary.md_6`, `parent_chunk_data_dictionary.md_3`, `BATCH→WAREHOUSE`

---

### ✅ QA-016 — How do I track which work orders are in progress at a specific warehouse?

**Status:** GROUNDED  
**GT Coverage:** N/A | **Top Score:** 0.0000 | **Gate:** `proceed`

**Expected answer:**
> Query the work_order table filtering by warehouse_id and status = 'IN_PROGRESS'. Join with the product table to get product names and types. Include quantity_ordered, quantity_completed, priority, planned_end_date, and calculate progress percentage as (quantity_completed / quantity_ordered * 100). O…

**System answer:**
> 

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_5`, `parent_chunk_data_dictionary.md_6`, `WORK_ORDER→WAREHOUSE`, `Operation Name Work→WORK_ORDER`, `Stock Levels→INVENTORY`, `parent_chunk_data_dictionary.md_8`, `Production Batch→BATCH`, `parent_chunk_data_dictionary.md_7`

---

### ✅ QA-017 — How can I find which components need reordering based on current inventory levels?

**Status:** GROUNDED  
**GT Coverage:** N/A | **Top Score:** 0.0000 | **Gate:** `proceed`

**Expected answer:**
> Query the inventory table and filter where quantity_on_hand minus quantity_reserved is less than reorder_threshold. Join with the component table to get component names, categories, and standard costs. Join with the warehouse table for location information. Results identify which components are belo…

**System answer:**
> 

**Sources retrieved (12):** `Stock Levels→INVENTORY`, `parent_chunk_data_dictionary.md_5`, `INVENTORY→COMPONENT`, `parent_chunk_data_dictionary.md_3`, `Bill Of Materials (Bom)→BOM`, `parent_chunk_data_dictionary.md_7`, `parent_chunk_data_dictionary.md_4`, `Component→COMPONENT`

---

### ✅ QA-018 — How do I determine the manufacturing route for a specific product?

**Status:** GROUNDED  
**GT Coverage:** N/A | **Top Score:** 0.0000 | **Gate:** `proceed`

**Expected answer:**
> Query the route table filtering by product_id, ordered by sequence_number ascending. For each operation, retrieve operation_name, work_center, cycle_time_minutes, and setup_time_minutes. Join with the product table to get product details. The sequence of operations shows the complete manufacturing w…

**System answer:**
> 

**Sources retrieved (12):** `Manufacturing Route→ROUTE`, `parent_chunk_data_dictionary.md_6`, `ROUTE→PRODUCT`, `Bill Of Materials (Bom)→BOM`, `parent_chunk_data_dictionary.md_3`, `Operation Name Work→WORK_ORDER`, `parent_chunk_data_dictionary.md_7`, `Production Batch→BATCH`

---

### ✅ QA-019 — How can I find which batches are stored at a specific warehouse and their QC status?

**Status:** GROUNDED  
**GT Coverage:** N/A | **Top Score:** 0.0000 | **Gate:** `proceed`

**Expected answer:**
> Query the batch table filtering by warehouse_id. Join with the product table to get product names and types. Include production_date, quantity_produced, expiry_date, and qc_status (PENDING, PASSED, FAILED, QUARANTINED). Filter by qc_status to isolate batches requiring quality attention or ready for …

**System answer:**
> 

**Sources retrieved (12):** `Production Batch→BATCH`, `parent_chunk_data_dictionary.md_5`, `BATCH→WAREHOUSE`, `Quality Control (Qc)→QUALITY_CONTROL`, `parent_chunk_data_dictionary.md_6`, `Stock Levels→INVENTORY`, `parent_chunk_data_dictionary.md_8`, `Operation Name Work→WORK_ORDER`

---

### ✅ QA-020 — How do I identify which specifications apply to specific components?

**Status:** GROUNDED  
**GT Coverage:** N/A | **Top Score:** 0.0000 | **Gate:** `proceed`

**Expected answer:**
> Query the component table and join with the specification table via specification_id. Include component_name, component_category, and specification details (specification_name, spec_type, critical_parameter, min_value, max_value, unit_of_measure). This shows the technical requirements that each comp…

**System answer:**
> 

**Sources retrieved (12):** `Component→COMPONENT`, `parent_chunk_data_dictionary.md_5`, `parent_chunk_data_dictionary.md_7`, `Bill Of Materials (Bom)→BOM`, `parent_chunk_data_dictionary.md_3`, `Specification→SPECIFICATION`, `parent_chunk_data_dictionary.md_4`, `Quality Control (Qc)→QUALITY_CONTROL`

---

### ✅ QA-021 — How can I perform a complete BOM explosion to find all components required for a finished product?

**Status:** GROUNDED  
**GT Coverage:** N/A | **Top Score:** 0.0000 | **Gate:** `proceed`

**Expected answer:**
> Use a recursive query starting from the product_id of the finished good. At each level, join the bom table to find component_product_id entries. For each component, check if product_type is 'ASSEMBLY' or 'FINISHED_GOOD'. If so, recursively query bom again using that component_product_id as the new p…

**System answer:**
> 

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_4`, `Bill Of Materials (Bom)→BOM`, `parent_chunk_data_dictionary.md_3`, `BOM→PRODUCT`, `parent_chunk_data_dictionary.md_7`, `parent_chunk_data_dictionary.md_6`, `Quality Control (Qc)→QUALITY_CONTROL`, `parent_chunk_data_dictionary.md_8`

---

### ✅ QA-022 — How do I calculate the total material cost for a product including all sub-assemblies?

**Status:** GROUNDED  
**GT Coverage:** N/A | **Top Score:** 0.0000 | **Gate:** `proceed`

**Expected answer:**
> Perform a recursive BOM explosion to find all leaf-level components. For each leaf component, join with the component table to get standard_cost. Multiply standard_cost by the accumulated quantity from the BOM traversal. Sum all component costs to get total material cost. This calculation must trave…

**System answer:**
> 

**Sources retrieved (12):** `Bill Of Materials (Bom)→BOM`, `parent_chunk_data_dictionary.md_3`, `parent_chunk_data_dictionary.md_4`, `parent_chunk_data_dictionary.md_7`, `parent_chunk_data_dictionary.md_8`, `Component→COMPONENT`, `parent_chunk_data_dictionary.md_6`, `Hierarchical Product Relationships→PRODUCT`

---

### ✅ QA-023 — How can I find all parent products that contain a specific component anywhere in their BOM structure?

**Status:** GROUNDED  
**GT Coverage:** N/A | **Top Score:** 0.0000 | **Gate:** `proceed`

**Expected answer:**
> Use a recursive reverse traversal of the BOM. Start with the component_id as the initial parent_product_id. Find all records where this product appears as component_product_id in the bom table. For each parent_product_id found, check if it appears as a component_product_id in other bom records (is a…

**System answer:**
> 

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_4`, `parent_chunk_data_dictionary.md_3`, `Bill Of Materials (Bom)→BOM`, `BOM→PRODUCT`, `PRODUCT→PRODUCT`, `parent_chunk_data_dictionary.md_6`, `parent_chunk_data_dictionary.md_8`, `parent_chunk_data_dictionary.md_5`

---

### ✅ QA-024 — How do I identify work orders that require a specific component, considering nested sub-assemblies?

**Status:** GROUNDED  
**GT Coverage:** N/A | **Top Score:** 0.0000 | **Gate:** `proceed`

**Expected answer:**
> First, perform reverse BOM traversal to find all parent products that contain the target component at any level. Then query the work_order table where product_id is in the set of parent products found. This includes work orders for finished goods that contain the component indirectly through sub-ass…

**System answer:**
> 

**Sources retrieved (12):** `Bill Of Materials (Bom)→BOM`, `parent_chunk_data_dictionary.md_6`, `parent_chunk_data_dictionary.md_5`, `parent_chunk_data_dictionary.md_3`, `parent_chunk_data_dictionary.md_4`, `Operation Name Work→WORK_ORDER`, `WORK_ORDER→WORK_ORDER`, `Component→COMPONENT`

---

### ✅ QA-025 — How can I determine the maximum BOM depth level for any product?

**Status:** GROUNDED  
**GT Coverage:** N/A | **Top Score:** 0.0000 | **Gate:** `proceed`

**Expected answer:**
> Use a recursive query on the bom table, incrementing a level counter at each traversal. Start with bom_level = 0 and add 1 for each recursive step. Track the maximum level reached across all product hierarchies. This identifies the most complex product structures with the deepest nesting.

**System answer:**
> 

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_4`, `parent_chunk_data_dictionary.md_3`, `Bill Of Materials (Bom)→BOM`, `BOM→PRODUCT`, `parent_chunk_data_dictionary.md_7`, `parent_chunk_data_dictionary.md_5`, `parent_chunk_data_dictionary.md_6`, `Specification→SPECIFICATION`

---

### ✅ QA-026 — How do I find all products that have a specific product as a sub-assembly at any level?

**Status:** GROUNDED  
**GT Coverage:** N/A | **Top Score:** 0.0000 | **Gate:** `proceed`

**Expected answer:**
> Perform a recursive search starting with the target product_id as the initial component_product_id in the bom table. For each parent_product_id found, check if that parent appears as a component in other bom entries. Continue recursively until reaching products that are not used as components elsewh…

**System answer:**
> 

**Sources retrieved (12):** `Bill Of Materials (Bom)→BOM`, `parent_chunk_data_dictionary.md_3`, `parent_chunk_data_dictionary.md_4`, `parent_chunk_data_dictionary.md_5`, `parent_chunk_data_dictionary.md_7`, `Stock Levels→INVENTORY`, `parent_chunk_data_dictionary.md_8`, `Hierarchical Product Relationships→PRODUCT`

---

### ✅ QA-027 — How can I calculate the total lead time for a product including all sub-assembly lead times?

**Status:** GROUNDED  
**GT Coverage:** N/A | **Top Score:** 0.0000 | **Gate:** `proceed`

**Expected answer:**
> Perform a recursive BOM explosion to find all components and sub-assemblies. For each product_id in the hierarchy, retrieve lead_time_days from the product table. The total lead time is the maximum of all lead times in the hierarchy (representing the longest dependency chain), or optionally sum lead…

**System answer:**
> 

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_3`, `Component Supplier→COMPONENT_SUPPLIER`, `Hierarchical Product Relationships→PRODUCT`, `Bill Of Materials (Bom)→BOM`, `parent_chunk_data_dictionary.md_4`, `parent_chunk_data_dictionary.md_7`, `parent_chunk_data_dictionary.md_6`, `parent_chunk_data_dictionary.md_8`

---

### ✅ QA-028 — How do I generate a complete indented BOM report showing the hierarchical structure?

**Status:** GROUNDED  
**GT Coverage:** N/A | **Top Score:** 0.0000 | **Gate:** `proceed`

**Expected answer:**
> Use a recursive query on the bom table that tracks the current depth level. Start with the top-level product (parent_product_id where product has no parent_product_id). At each level, output component details indented by depth level. Include product_name, quantity, and unit_of_measure. Recursively p…

**System answer:**
> 

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_4`, `parent_chunk_data_dictionary.md_3`, `Bill Of Materials (Bom)→BOM`, `parent_chunk_data_dictionary.md_6`, `parent_chunk_data_dictionary.md_8`, `Hierarchical Product Relationships→PRODUCT`, `BOM→PRODUCT`, `Hierarchical Product Relationships`

---

### ✅ QA-029 — How can I find which components appear most frequently across all product BOMs?

**Status:** GROUNDED  
**GT Coverage:** N/A | **Top Score:** 0.0000 | **Gate:** `proceed`

**Expected answer:**
> Perform BOM explosion for all products and aggregate occurrences of each leaf-level component. Count how many distinct product hierarchies contain each component. Join with component table for component names. Order by frequency descending to identify common components that should be prioritized for…

**System answer:**
> 

**Sources retrieved (12):** `Bill Of Materials (Bom)→BOM`, `parent_chunk_data_dictionary.md_4`, `parent_chunk_data_dictionary.md_3`, `BOM→PRODUCT`, `parent_chunk_data_dictionary.md_5`, `Stock Levels→INVENTORY`, `Component→COMPONENT`, `parent_chunk_data_dictionary.md_8`

---

### ✅ QA-030 — How do I detect circular references in the BOM structure to prevent infinite loops?

**Status:** GROUNDED  
**GT Coverage:** N/A | **Top Score:** 0.0000 | **Gate:** `proceed`

**Expected answer:**
> Use a recursive query with a cycle detection check. Track the path of visited product_ids at each recursion level. If a product_id appears twice in the same path, a circular reference exists. Alternatively, check if any bom record has parent_product_id = component_product_id (direct self-reference),…

**System answer:**
> 

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_4`, `parent_chunk_data_dictionary.md_3`, `BOM→PRODUCT`, `Bill Of Materials (Bom)→BOM`, `parent_chunk_data_dictionary.md_8`, `parent_chunk_data_dictionary.md_7`, `parent_chunk_data_dictionary.md_6`, `INVENTORY→COMPONENT`

---

### ✅ QA-031 — How can I determine the complete supplier chain for a finished product, including suppliers for all sub-assemblies?

**Status:** GROUNDED  
**GT Coverage:** N/A | **Top Score:** 0.0000 | **Gate:** `proceed`

**Expected answer:**
> First, perform recursive BOM explosion to find all leaf-level components in the product hierarchy. Then query the component_supplier table for each component_id to find approved suppliers. Join with the supplier table to get supplier names, ratings, and contact information. Include supplier-specific…

**System answer:**
> 

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_3`, `Bill Of Materials (Bom)→BOM`, `parent_chunk_data_dictionary.md_4`, `parent_chunk_data_dictionary.md_8`, `Quality Control (Qc)→QUALITY_CONTROL`, `Component Supplier→COMPONENT_SUPPLIER`, `Manufacturing Route→ROUTE`, `Supplier→SUPPLIER`

---

### ✅ QA-032 — How do I check if sufficient inventory exists across all warehouses to fulfill a work order?

**Status:** GROUNDED  
**GT Coverage:** N/A | **Top Score:** 0.0000 | **Gate:** `proceed`

**Expected answer:**
> For the work_order's product_id, perform recursive BOM explosion to get all required components with quantities. For each component, sum the available quantity (quantity_on_hand - quantity_reserved) across all warehouses from the inventory table. Compare aggregated available inventory against requir…

**System answer:**
> 

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_5`, `Stock Levels→INVENTORY`, `parent_chunk_data_dictionary.md_6`, `INVENTORY→WAREHOUSE`, `WORK_ORDER→WAREHOUSE`, `Operation Name Work→WORK_ORDER`, `parent_chunk_data_dictionary.md_8`, `parent_chunk_data_dictionary.md_7`

---

### ✅ QA-033 — How can I find which quality control inspections failed for components from specific suppliers?

**Status:** GROUNDED  
**GT Coverage:** N/A | **Top Score:** 0.0000 | **Gate:** `proceed`

**Expected answer:**
> Query the quality_control table filtering by result = 'FAIL'. Join with the batch table to get product_id and production_date. Join with the bom table recursively to trace which products contain failed components. Join with component_supplier and supplier tables to identify the source supplier. Filt…

**System answer:**
> 

**Sources retrieved (12):** `Quality Control (Qc)→QUALITY_CONTROL`, `parent_chunk_data_dictionary.md_5`, `parent_chunk_data_dictionary.md_3`, `Component Supplier→COMPONENT_SUPPLIER`, `parent_chunk_data_dictionary.md_4`, `parent_chunk_data_dictionary.md_8`, `parent_chunk_data_dictionary.md_7`, `Component→COMPONENT`

---

### ✅ QA-034 — How do I calculate the total manufacturing time for a work order including all sub-assembly work orders?

**Status:** GROUNDED  
**GT Coverage:** N/A | **Top Score:** 0.0000 | **Gate:** `proceed`

**Expected answer:**
> Query the work_order table starting with the parent work_order. Find all child work_orders where parent_work_order matches the current work_order_id. For each work order (parent and children), join with the route table on product_id to get all operations. Sum (cycle_time_minutes * quantity) plus set…

**System answer:**
> 

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_6`, `parent_chunk_data_dictionary.md_3`, `Bill Of Materials (Bom)→BOM`, `Operation Name Work→WORK_ORDER`, `Manufacturing Route→ROUTE`, `parent_chunk_data_dictionary.md_7`, `Production Batch→BATCH`, `parent_chunk_data_dictionary.md_4`

---

### ✅ QA-035 — How can I identify which shipments are overdue and their impact on work orders?

**Status:** GROUNDED  
**GT Coverage:** N/A | **Top Score:** 0.0000 | **Gate:** `proceed`

**Expected answer:**
> Query the shipment table filtering for status = 'SHIPPED' where actual_arrival is NULL and estimated_arrival is in the past (overdue). Join with the component_supplier table via supplier_id and component_id to identify which components are delayed. Perform reverse BOM lookup to find which parent pro…

**System answer:**
> 

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_5`, `parent_chunk_data_dictionary.md_8`, `parent_chunk_data_dictionary.md_6`, `Physical Transfer→SHIPMENT`, `WORK_ORDER→PRODUCT`, `Operation Name Work→WORK_ORDER`, `WORK_ORDER→WAREHOUSE`, `WORK_ORDER→WORK_ORDER`

---

### ✅ QA-036 — How do I find which batches are approaching or past expiry and contain components from specific suppliers?

**Status:** GROUNDED  
**GT Coverage:** N/A | **Top Score:** 0.0000 | **Gate:** `proceed`

**Expected answer:**
> Query the batch table filtering for expiry_date within a warning window (e.g., next 30 days) or past expiry. Join with the bom table recursively on product_id to trace all components used in those batches. Join with component_supplier and supplier tables to filter by specific suppliers. Results iden…

**System answer:**
> 

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_5`, `Component Supplier→COMPONENT_SUPPLIER`, `parent_chunk_data_dictionary.md_7`, `Production Batch→BATCH`, `parent_chunk_data_dictionary.md_3`, `parent_chunk_data_dictionary.md_8`, `parent_chunk_data_dictionary.md_4`, `Quality Control (Qc)→QUALITY_CONTROL`

---

### ✅ QA-037 — How can I generate a material requirements plan showing when to order components based on work order schedules?

**Status:** GROUNDED  
**GT Coverage:** N/A | **Top Score:** 0.0000 | **Gate:** `proceed`

**Expected answer:**
> Query all work_orders with status 'PENDING' ordered by planned_start_date. For each work_order, perform BOM explosion to get required components and quantities. For each component, query inventory for current available stock across warehouses. Calculate net requirements = (required quantity * work_o…

**System answer:**
> 

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_6`, `parent_chunk_data_dictionary.md_7`, `Bill Of Materials (Bom)→BOM`, `parent_chunk_data_dictionary.md_5`, `parent_chunk_data_dictionary.md_4`, `Operation Name Work→WORK_ORDER`, `parent_chunk_data_dictionary.md_3`, `WORK_ORDER→WORK_ORDER`

---

### ✅ QA-038 — How do I trace the complete genealogy of a component from supplier through batch to finished goods?

**Status:** GROUNDED  
**GT Coverage:** N/A | **Top Score:** 0.0000 | **Gate:** `proceed`

**Expected answer:**
> Start with a shipment from the supplier (shipment table with supplier_id and shipment_type = 'INBOUND'). Track to inventory updates via component_id and warehouse_id. Identify batches that consumed the component via reverse BOM lookup (batch.product_id → bom hierarchy → component_id). Query quality_…

**System answer:**
> 

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_3`, `parent_chunk_data_dictionary.md_5`, `Quality Control (Qc)→QUALITY_CONTROL`, `parent_chunk_data_dictionary.md_8`, `parent_chunk_data_dictionary.md_4`, `Bill Of Materials (Bom)→BOM`, `Component Supplier→COMPONENT_SUPPLIER`, `COMPONENT_SUPPLIER→COMPONENT`

---

### ✅ QA-039 — How can I find alternative suppliers for components that are critical for multiple products?

**Status:** GROUNDED  
**GT Coverage:** N/A | **Top Score:** 0.0000 | **Gate:** `proceed`

**Expected answer:**
> Perform BOM explosion for all active products and count component usage frequency. Identify high-frequency components. Query component_supplier table to find all suppliers for these components. Filter to suppliers with rating >= 4.0 (high quality) and is_preferred = 'Y'. For each component, list alt…

**System answer:**
> 

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_4`, `Component Supplier→COMPONENT_SUPPLIER`, `parent_chunk_data_dictionary.md_3`, `parent_chunk_data_dictionary.md_5`, `parent_chunk_data_dictionary.md_8`, `Bill Of Materials (Bom)→BOM`, `Specification→SPECIFICATION`, `Component→COMPONENT`

---

### ✅ QA-040 — How do I calculate the total landed cost for a product including component costs, supplier lead times, and manufacturing operations?

**Status:** GROUNDED  
**GT Coverage:** N/A | **Top Score:** 0.0000 | **Gate:** `proceed`

**Expected answer:**
> Perform recursive BOM explosion to get all leaf components. For each component, query component_supplier to get unit_price from primary supplier. Multiply by accumulated BOM quantity for material cost. Add shipping costs (estimated from shipment history). Query route table for the product to get all…

**System answer:**
> 

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_3`, `Component Supplier→COMPONENT_SUPPLIER`, `Manufacturing Route→ROUTE`, `Hierarchical Product Relationships→PRODUCT`, `parent_chunk_data_dictionary.md_6`, `Component→COMPONENT`, `parent_chunk_data_dictionary.md_7`, `Bill Of Materials (Bom)→BOM`

---

## Anomalies & Observations

No anomalies detected. All questions grounded with acceptable RAGAS scores.
