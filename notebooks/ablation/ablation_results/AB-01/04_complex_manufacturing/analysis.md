# AB-01 — 04_complex_manufacturing — Run Analysis

**Timestamp:** 2026-03-31 00:09:32  
**Run tag:** `v5`

## Configuration

| Parameter | Value |
|-----------|-------|
| Extraction model | `LLM (gpt-5.4-nano-2026-03-17)` |
| Reasoning model | `gpt-5.4-2026-03-05` |
| Embedding model | `BAAI/bge-m3` |
| Retrieval mode | `vector` |
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
| Avg Top Score | 0.0915 |
| Avg Chunk Count | 6.0 |
| Abstained | 0 |

## RAGAS Metrics

RAGAS evaluation not enabled for this run.

## Per-Question Deep Dive

### ✅ QA-001 — What information is stored about products in the manufacturing system?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.5492 | **Gate:** `proceed`

**Expected answer:**
> Products are tracked with a unique identifier (product_id), descriptive name (product_name), classification as finished good, assembly, or component (product_type), optional parent product reference for hierarchical structures (parent_product_id), standard unit cost (base_cost), typical procurement …

**System answer:**
> The retrieved context explicitly says the manufacturing system stores product information in at least two ways.

In Manufacturing Routing, the data is keyed by route_id and product_id and stores the ordered steps for a product. The fields mentioned are route_name, sequence_number, operation_name, work_center, and timing fields. The context describes this as defining the full route structure for pr…

**Sources retrieved (6):** `Manufacturing Routing`, `Actual stock levels of components and products at specific warehouse locations`, `Component Supplier Relationship`, `inspection and testing records for quality assurance`, `Hierarchical production planning and tracking`, `Batches for traceability and inventory management`

**Context previews (first 3):**

1. _Manufacturing Routing: The table is keyed by route_id and product_id and stores the ordered steps for a product, including route_name, sequence_number, operation_name, work_center, and timing fields. …_

2. _Actual stock levels of components and products at specific warehouse locations…_

3. _Component Supplier Relationship: This table is a junction entity linking one component to one supplier, with a unique component_id/supplier_id pair and relationship attributes such as is_preferred, le…_

---

### ✅ QA-002 — How are components defined in the manufacturing database?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0060 | **Gate:** `proceed_with_warning`

**Expected answer:**
> Components are defined with a unique identifier (component_id), descriptive name (component_name), category grouping (component_category), unit of measure (unit_of_measure), standard unit cost (standard_cost), and optional reference to technical specifications (specification_id). Components represen…

**System answer:**
> In the provided context, components are shown only through their relationships and inventory presence.

The clearest definition is in the Component Supplier Relationship business concept, where a component is identified by component_id and linked to a supplier through a unique component_id/supplier_id pair. That relationship has attributes is_preferred, lead_time_days, and unit_price, so the conte…

**Sources retrieved (6):** `Manufacturing Routing`, `Actual stock levels of components and products at specific warehouse locations`, `Component Supplier Relationship`, `Hierarchical production planning and tracking`, `Batches for traceability and inventory management`, `inspection and testing records for quality assurance`

**Context previews (first 3):**

1. _Manufacturing Routing: The table is keyed by route_id and product_id and stores the ordered steps for a product, including route_name, sequence_number, operation_name, work_center, and timing fields. …_

2. _Actual stock levels of components and products at specific warehouse locations…_

3. _Component Supplier Relationship: This table is a junction entity linking one component to one supplier, with a unique component_id/supplier_id pair and relationship attributes such as is_preferred, le…_

---

### ✅ QA-003 — What is the purpose of the Bill of Materials (BOM) table?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0038 | **Gate:** `proceed_with_warning`

**Expected answer:**
> The BOM table defines the hierarchical structure of products by specifying which components or sub-assemblies are required to manufacture each parent product. It records the unique BOM entry identifier (bom_id), parent product being built (parent_product_id), component or sub-assembly product (compo…

**System answer:**
> The retrieved context does not explicitly describe a Bill of Materials (BOM) table, so I cannot state its purpose from the knowledge provided.

The closest related manufacturing concept in the context is “Hierarchical production planning and tracking,” but the context does not identify that concept as the BOM table or provide any BOM-specific definition, keys, columns, or business purpose.

**Sources retrieved (6):** `Manufacturing Routing`, `Component Supplier Relationship`, `Actual stock levels of components and products at specific warehouse locations`, `inspection and testing records for quality assurance`, `Batches for traceability and inventory management`, `Hierarchical production planning and tracking`

**Context previews (first 3):**

1. _Manufacturing Routing: The table is keyed by route_id and product_id and stores the ordered steps for a product, including route_name, sequence_number, operation_name, work_center, and timing fields. …_

2. _Component Supplier Relationship: This table is a junction entity linking one component to one supplier, with a unique component_id/supplier_id pair and relationship attributes such as is_preferred, le…_

3. _Actual stock levels of components and products at specific warehouse locations…_

---

### ✅ QA-004 — What supplier information does the system maintain?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0083 | **Gate:** `proceed_with_warning`

**Expected answer:**
> Suppliers are tracked with a unique identifier (supplier_id), legal business name (supplier_name), primary contact email (contact_email), primary contact phone number (contact_phone), performance rating from 1.0 to 5.0 (rating), and preferred supplier status flag (is_preferred).

**System answer:**
> From the retrieved context, the system maintains supplier information at the component-supplier relationship level in the Component Supplier Relationship table. This junction entity links one component to one supplier, with a unique component_id/supplier_id pair, and stores relationship-specific attributes including is_preferred, lead_time_days, and unit_price.

The context indicates that this mod…

**Sources retrieved (6):** `Component Supplier Relationship`, `Manufacturing Routing`, `inspection and testing records for quality assurance`, `Batches for traceability and inventory management`, `Actual stock levels of components and products at specific warehouse locations`, `Hierarchical production planning and tracking`

**Context previews (first 3):**

1. _Component Supplier Relationship: This table is a junction entity linking one component to one supplier, with a unique component_id/supplier_id pair and relationship attributes such as is_preferred, le…_

2. _Manufacturing Routing: The table is keyed by route_id and product_id and stores the ordered steps for a product, including route_name, sequence_number, operation_name, work_center, and timing fields. …_

3. _inspection and testing records for quality assurance…_

---

### ✅ QA-005 — How are warehouses represented in the schema?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0007 | **Gate:** `proceed_with_warning`

**Expected answer:**
> Warehouses are defined with a unique identifier (warehouse_id), descriptive name (warehouse_name), full street address (address), city location (city), state or province (state), total storage capacity in cubic meters (capacity), and optional manager identifier (manager_id).

**System answer:**
> From the retrieved context, warehouses are represented only indirectly as warehouse locations in the business concept “Actual stock levels of components and products at specific warehouse locations.”

So, the schema context shows that inventory is tracked at the level of a specific warehouse location for components and products. However, the retrieved context does not provide a warehouse table nam…

**Sources retrieved (6):** `Actual stock levels of components and products at specific warehouse locations`, `Manufacturing Routing`, `Batches for traceability and inventory management`, `Component Supplier Relationship`, `Hierarchical production planning and tracking`, `inspection and testing records for quality assurance`

**Context previews (first 3):**

1. _Actual stock levels of components and products at specific warehouse locations…_

2. _Manufacturing Routing: The table is keyed by route_id and product_id and stores the ordered steps for a product, including route_name, sequence_number, operation_name, work_center, and timing fields. …_

3. _Batches for traceability and inventory management…_

---

### ✅ QA-006 — What does the inventory table track?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0138 | **Gate:** `proceed_with_warning`

**Expected answer:**
> The inventory table tracks real-time stock levels including a unique record identifier (inventory_id), warehouse location (warehouse_id), component identifier for materials (component_id) or product identifier for finished goods (product_id), current physical stock quantity (quantity_on_hand), quant…

**System answer:**
> The inventory table tracks actual stock levels of components and products at specific warehouse locations.

**Sources retrieved (6):** `Batches for traceability and inventory management`, `Hierarchical production planning and tracking`, `Manufacturing Routing`, `Component Supplier Relationship`, `Actual stock levels of components and products at specific warehouse locations`, `inspection and testing records for quality assurance`

**Context previews (first 3):**

1. _Batches for traceability and inventory management…_

2. _Hierarchical production planning and tracking…_

3. _Manufacturing Routing: The table is keyed by route_id and product_id and stores the ordered steps for a product, including route_name, sequence_number, operation_name, work_center, and timing fields. …_

---

### ✅ QA-007 — How are work orders structured in the manufacturing system?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.2261 | **Gate:** `proceed`

**Expected answer:**
> Work orders represent production jobs with a unique identifier (work_order_id), product to be manufactured (product_id), optional parent work order for nested hierarchies (parent_work_order), quantity to produce (quantity_ordered), quantity completed so far (quantity_completed), current status (PEND…

**System answer:**
> The retrieved context does not explicitly define a work order table, work order keys, statuses, or direct work-order-to-other-table relationships, so I cannot describe the exact schema structure of work orders themselves from this knowledge graph.

What the context does show is the surrounding manufacturing structure that work orders would likely operate within. The clearest schema evidence is the…

**Sources retrieved (6):** `Manufacturing Routing`, `Actual stock levels of components and products at specific warehouse locations`, `Hierarchical production planning and tracking`, `Component Supplier Relationship`, `Batches for traceability and inventory management`, `inspection and testing records for quality assurance`

**Context previews (first 3):**

1. _Manufacturing Routing: The table is keyed by route_id and product_id and stores the ordered steps for a product, including route_name, sequence_number, operation_name, work_center, and timing fields. …_

2. _Actual stock levels of components and products at specific warehouse locations…_

3. _Hierarchical production planning and tracking…_

---

### ✅ QA-008 — What information is captured in the shipment table?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0388 | **Gate:** `proceed_with_warning`

**Expected answer:**
> Shipments track material transfers with a unique identifier (shipment_id), shipment type (INBOUND from suppliers, OUTBOUND to customers, INTERNAL between warehouses), destination warehouse (warehouse_id), source supplier for inbound (supplier_id), destination customer for outbound (customer_id), shi…

**System answer:**
> The retrieved context does not describe a shipment table, so I cannot determine what information it captures.

What is present in the context is limited to other business concepts: Manufacturing Routing, Component Supplier Relationship, inspection and testing records for quality assurance, batches for traceability and inventory management, actual stock levels at warehouse locations, and hierarchic…

**Sources retrieved (6):** `Manufacturing Routing`, `Component Supplier Relationship`, `inspection and testing records for quality assurance`, `Batches for traceability and inventory management`, `Actual stock levels of components and products at specific warehouse locations`, `Hierarchical production planning and tracking`

**Context previews (first 3):**

1. _Manufacturing Routing: The table is keyed by route_id and product_id and stores the ordered steps for a product, including route_name, sequence_number, operation_name, work_center, and timing fields. …_

2. _Component Supplier Relationship: This table is a junction entity linking one component to one supplier, with a unique component_id/supplier_id pair and relationship attributes such as is_preferred, le…_

3. _inspection and testing records for quality assurance…_

---

### ✅ QA-009 — How does the quality control system record inspections?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.4847 | **Gate:** `proceed`

**Expected answer:**
> Quality control records are stored with a unique identifier (qc_id), associated production batch (batch_id), applicable specification requirements (specification_id), inspection date (qc_date), inspection type (INCOMING for supplier materials, IN_PROCESS during manufacturing, FINAL for finished good…

**System answer:**
> The retrieved context indicates that the quality control system records inspections as inspection and testing records for quality assurance.

No additional schema details are provided in the context, so I cannot specify the table name, columns, workflow, or how individual inspection records are structured.

**Sources retrieved (6):** `inspection and testing records for quality assurance`, `Manufacturing Routing`, `Component Supplier Relationship`, `Batches for traceability and inventory management`, `Hierarchical production planning and tracking`, `Actual stock levels of components and products at specific warehouse locations`

**Context previews (first 3):**

1. _inspection and testing records for quality assurance…_

2. _Manufacturing Routing: The table is keyed by route_id and product_id and stores the ordered steps for a product, including route_name, sequence_number, operation_name, work_center, and timing fields. …_

3. _Component Supplier Relationship: This table is a junction entity linking one component to one supplier, with a unique component_id/supplier_id pair and relationship attributes such as is_preferred, le…_

---

### ✅ QA-010 — What do specification records define?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0031 | **Gate:** `proceed_with_warning`

**Expected answer:**
> Specifications define technical requirements with a unique identifier (specification_id), descriptive name (specification_name), version number, effective date, specification type (DIMENSIONAL, MATERIAL, PERFORMANCE), critical parameter being measured (critical_parameter), acceptable minimum value (…

**System answer:**
> The retrieved context does not mention specification records, so it cannot determine what specification records define.

What is present in the context is limited to these concepts: manufacturing routing, component-supplier relationships, batches for traceability and inventory management, actual stock levels at warehouse locations, hierarchical production planning and tracking, and inspection and …

**Sources retrieved (6):** `inspection and testing records for quality assurance`, `Manufacturing Routing`, `Component Supplier Relationship`, `Batches for traceability and inventory management`, `Actual stock levels of components and products at specific warehouse locations`, `Hierarchical production planning and tracking`

**Context previews (first 3):**

1. _inspection and testing records for quality assurance…_

2. _Manufacturing Routing: The table is keyed by route_id and product_id and stores the ordered steps for a product, including route_name, sequence_number, operation_name, work_center, and timing fields. …_

3. _Component Supplier Relationship: This table is a junction entity linking one component to one supplier, with a unique component_id/supplier_id pair and relationship attributes such as is_preferred, le…_

---

### ✅ QA-011 — How can I find which suppliers provide specific components?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.2385 | **Gate:** `proceed`

**Expected answer:**
> Query the component_supplier table which links components to their approved suppliers. This table contains the component identifier (component_id), supplier identifier (supplier_id), preferred supplier flag (is_preferred), lead time in days (lead_time_days), and unit price (unit_price). Join with th…

**System answer:**
> Use the Component Supplier Relationship concept. The retrieved context says this is a junction entity that links one component to one supplier, with a unique component_id/supplier_id pair.

So, to find which suppliers provide a specific component, you would look up rows in Component Supplier Relationship for the target component_id. Each matching row represents one supplier-component association. …

**Sources retrieved (6):** `Actual stock levels of components and products at specific warehouse locations`, `Component Supplier Relationship`, `Manufacturing Routing`, `inspection and testing records for quality assurance`, `Batches for traceability and inventory management`, `Hierarchical production planning and tracking`

**Context previews (first 3):**

1. _Actual stock levels of components and products at specific warehouse locations…_

2. _Component Supplier Relationship: This table is a junction entity linking one component to one supplier, with a unique component_id/supplier_id pair and relationship attributes such as is_preferred, le…_

3. _Manufacturing Routing: The table is keyed by route_id and product_id and stores the ordered steps for a product, including route_name, sequence_number, operation_name, work_center, and timing fields. …_

---

### ✅ QA-012 — How do I trace which components are needed to fulfill a work order?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0017 | **Gate:** `proceed_with_warning`

**Expected answer:**
> Start with the work_order table to get the product_id being manufactured. Join to the bom table using product_id as parent_product_id to find all direct components and sub-assemblies. For each component_product_id, if it is an ASSEMBLY type product, recursively query the bom table again to explode m…

**System answer:**
> I cannot determine how to trace which components are needed to fulfill a work order from the retrieved context.

What the context does show is only a partial manufacturing schema/business glossary: a Manufacturing Routing concept keyed by route_id and product_id that stores ordered production steps for a product, including route_name, sequence_number, operation_name, work_center, and timing fields…

**Sources retrieved (6):** `Manufacturing Routing`, `Batches for traceability and inventory management`, `Actual stock levels of components and products at specific warehouse locations`, `Component Supplier Relationship`, `Hierarchical production planning and tracking`, `inspection and testing records for quality assurance`

**Context previews (first 3):**

1. _Manufacturing Routing: The table is keyed by route_id and product_id and stores the ordered steps for a product, including route_name, sequence_number, operation_name, work_center, and timing fields. …_

2. _Batches for traceability and inventory management…_

3. _Actual stock levels of components and products at specific warehouse locations…_

---

### ✅ QA-013 — How can I identify which warehouses have available inventory for specific components?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.8727 | **Gate:** `proceed`

**Expected answer:**
> Query the inventory table filtered by component_id, joining with the warehouse table to get warehouse names and locations. Calculate available quantity as quantity_on_hand minus quantity_reserved. Filter for records where available quantity is greater than zero. Results show warehouse names, locatio…

**System answer:**
> Use the business concept “Actual stock levels of components and products at specific warehouse locations.” That is the context’s source for determining inventory by warehouse.

At a schema level, the way to answer your question is to look up the specific component in whatever structure implements that concept and check its stock level at each warehouse location. Warehouses that show a positive sto…

**Sources retrieved (6):** `Actual stock levels of components and products at specific warehouse locations`, `Batches for traceability and inventory management`, `Manufacturing Routing`, `inspection and testing records for quality assurance`, `Component Supplier Relationship`, `Hierarchical production planning and tracking`

**Context previews (first 3):**

1. _Actual stock levels of components and products at specific warehouse locations…_

2. _Batches for traceability and inventory management…_

3. _Manufacturing Routing: The table is keyed by route_id and product_id and stores the ordered steps for a product, including route_name, sequence_number, operation_name, work_center, and timing fields. …_

---

### ✅ QA-014 — How do I find which shipments delivered materials from a specific supplier?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0032 | **Gate:** `proceed_with_warning`

**Expected answer:**
> Query the shipment table filtering by supplier_id and shipment_type = 'INBOUND'. Join with the warehouse table to show destination warehouses. Filter for status = 'DELIVERED' and include actual_arrival date. Results can be ordered by ship_date descending to show most recent deliveries first.

**System answer:**
> I cannot determine which shipments delivered materials from a specific supplier from the retrieved context, because the context does not include any shipment, delivery, receipt, or other transaction-level entity.

What the context does provide is schema-level metadata for related business concepts. The closest supplier-related structure is Component Supplier Relationship, which links one component…

**Sources retrieved (6):** `Component Supplier Relationship`, `Actual stock levels of components and products at specific warehouse locations`, `Manufacturing Routing`, `Batches for traceability and inventory management`, `inspection and testing records for quality assurance`, `Hierarchical production planning and tracking`

**Context previews (first 3):**

1. _Component Supplier Relationship: This table is a junction entity linking one component to one supplier, with a unique component_id/supplier_id pair and relationship attributes such as is_preferred, le…_

2. _Actual stock levels of components and products at specific warehouse locations…_

3. _Manufacturing Routing: The table is keyed by route_id and product_id and stores the ordered steps for a product, including route_name, sequence_number, operation_name, work_center, and timing fields. …_

---

### ✅ QA-015 — How can I determine which quality control inspections were performed on a specific production batch?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0106 | **Gate:** `proceed_with_warning`

**Expected answer:**
> Query the quality_control table filtered by batch_id. Join with the specification table to get requirement details (specification_name, spec_type, acceptable ranges). Include qc_date, qc_type (INCOMING, IN_PROCESS, FINAL), result (PASS, FAIL, CONDITIONAL), and defect_count. This shows the complete i…

**System answer:**
> From the retrieved context, I cannot determine how to identify which quality control inspections were performed on a specific production batch.

The context only states that the knowledge graph includes the business concepts "inspection and testing records for quality assurance" and "Batches for traceability and inventory management." It does not provide any table names, column names, batch identi…

**Sources retrieved (6):** `inspection and testing records for quality assurance`, `Hierarchical production planning and tracking`, `Manufacturing Routing`, `Batches for traceability and inventory management`, `Actual stock levels of components and products at specific warehouse locations`, `Component Supplier Relationship`

**Context previews (first 3):**

1. _inspection and testing records for quality assurance…_

2. _Hierarchical production planning and tracking…_

3. _Manufacturing Routing: The table is keyed by route_id and product_id and stores the ordered steps for a product, including route_name, sequence_number, operation_name, work_center, and timing fields. …_

---

### ✅ QA-016 — How do I track which work orders are in progress at a specific warehouse?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0203 | **Gate:** `proceed_with_warning`

**Expected answer:**
> Query the work_order table filtering by warehouse_id and status = 'IN_PROGRESS'. Join with the product table to get product names and types. Include quantity_ordered, quantity_completed, priority, planned_end_date, and calculate progress percentage as (quantity_completed / quantity_ordered * 100). O…

**System answer:**
> From the retrieved context, I can only say that the knowledge graph includes these relevant concepts: “Hierarchical production planning and tracking,” “Manufacturing Routing,” and “Actual stock levels of components and products at specific warehouse locations.”

What is known:
“Manufacturing Routing” is keyed by route_id and product_id and stores ordered production steps, including route_name, seq…

**Sources retrieved (6):** `Actual stock levels of components and products at specific warehouse locations`, `Manufacturing Routing`, `Hierarchical production planning and tracking`, `Batches for traceability and inventory management`, `Component Supplier Relationship`, `inspection and testing records for quality assurance`

**Context previews (first 3):**

1. _Actual stock levels of components and products at specific warehouse locations…_

2. _Manufacturing Routing: The table is keyed by route_id and product_id and stores the ordered steps for a product, including route_name, sequence_number, operation_name, work_center, and timing fields. …_

3. _Hierarchical production planning and tracking…_

---

### ✅ QA-017 — How can I find which components need reordering based on current inventory levels?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.1682 | **Gate:** `proceed_with_warning`

**Expected answer:**
> Query the inventory table and filter where quantity_on_hand minus quantity_reserved is less than reorder_threshold. Join with the component table to get component names, categories, and standard costs. Join with the warehouse table for location information. Results identify which components are belo…

**System answer:**
> From the retrieved context, the relevant starting point is the business concept “Actual stock levels of components and products at specific warehouse locations,” which indicates that current on-hand inventory is tracked by component/product and warehouse location. That is the concept you would use to see present inventory.

To identify components that need reordering, the context only supports the…

**Sources retrieved (6):** `Actual stock levels of components and products at specific warehouse locations`, `Batches for traceability and inventory management`, `Component Supplier Relationship`, `Manufacturing Routing`, `Hierarchical production planning and tracking`, `inspection and testing records for quality assurance`

**Context previews (first 3):**

1. _Actual stock levels of components and products at specific warehouse locations…_

2. _Batches for traceability and inventory management…_

3. _Component Supplier Relationship: This table is a junction entity linking one component to one supplier, with a unique component_id/supplier_id pair and relationship attributes such as is_preferred, le…_

---

### ✅ QA-018 — How do I determine the manufacturing route for a specific product?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.8168 | **Gate:** `proceed`

**Expected answer:**
> Query the route table filtering by product_id, ordered by sequence_number ascending. For each operation, retrieve operation_name, work_center, cycle_time_minutes, and setup_time_minutes. Join with the product table to get product details. The sequence of operations shows the complete manufacturing w…

**System answer:**
> Use the Manufacturing Routing table. The retrieved context says it is keyed by route_id and product_id and stores the ordered steps for a product.

To determine the manufacturing route for a specific product, look up the rows in Manufacturing Routing for that product_id. From those rows, use route_id and route_name to identify the route, and sequence_number to order the steps. The route details ar…

**Sources retrieved (6):** `Manufacturing Routing`, `Hierarchical production planning and tracking`, `Actual stock levels of components and products at specific warehouse locations`, `Batches for traceability and inventory management`, `inspection and testing records for quality assurance`, `Component Supplier Relationship`

**Context previews (first 3):**

1. _Manufacturing Routing: The table is keyed by route_id and product_id and stores the ordered steps for a product, including route_name, sequence_number, operation_name, work_center, and timing fields. …_

2. _Hierarchical production planning and tracking…_

3. _Actual stock levels of components and products at specific warehouse locations…_

---

### ✅ QA-019 — How can I find which batches are stored at a specific warehouse and their QC status?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0991 | **Gate:** `proceed_with_warning`

**Expected answer:**
> Query the batch table filtering by warehouse_id. Join with the product table to get product names and types. Include production_date, quantity_produced, expiry_date, and qc_status (PENDING, PASSED, FAILED, QUARANTINED). Filter by qc_status to isolate batches requiring quality attention or ready for …

**System answer:**
> From the retrieved context, the relevant pieces are “Actual stock levels of components and products at specific warehouse locations,” “Batches for traceability and inventory management,” and “inspection and testing records for quality assurance.”

So, at a conceptual level, finding batches stored at a specific warehouse and their QC status would require combining:
the warehouse/location stock info…

**Sources retrieved (6):** `Actual stock levels of components and products at specific warehouse locations`, `Batches for traceability and inventory management`, `Manufacturing Routing`, `Component Supplier Relationship`, `inspection and testing records for quality assurance`, `Hierarchical production planning and tracking`

**Context previews (first 3):**

1. _Actual stock levels of components and products at specific warehouse locations…_

2. _Batches for traceability and inventory management…_

3. _Manufacturing Routing: The table is keyed by route_id and product_id and stores the ordered steps for a product, including route_name, sequence_number, operation_name, work_center, and timing fields. …_

---

### ✅ QA-020 — How do I identify which specifications apply to specific components?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0065 | **Gate:** `proceed_with_warning`

**Expected answer:**
> Query the component table and join with the specification table via specification_id. Include component_name, component_category, and specification details (specification_name, spec_type, critical_parameter, min_value, max_value, unit_of_measure). This shows the technical requirements that each comp…

**System answer:**
> From the retrieved context, this cannot be determined.

What is known is that there is a “Component Supplier Relationship” concept that links a component to a supplier using a unique component_id/supplier_id pair, with attributes is_preferred, lead_time_days, and unit_price. The context also mentions business concepts for actual stock levels, manufacturing routing, inspection and testing records, …

**Sources retrieved (6):** `Actual stock levels of components and products at specific warehouse locations`, `Component Supplier Relationship`, `Manufacturing Routing`, `inspection and testing records for quality assurance`, `Hierarchical production planning and tracking`, `Batches for traceability and inventory management`

**Context previews (first 3):**

1. _Actual stock levels of components and products at specific warehouse locations…_

2. _Component Supplier Relationship: This table is a junction entity linking one component to one supplier, with a unique component_id/supplier_id pair and relationship attributes such as is_preferred, le…_

3. _Manufacturing Routing: The table is keyed by route_id and product_id and stores the ordered steps for a product, including route_name, sequence_number, operation_name, work_center, and timing fields. …_

---

### ✅ QA-021 — How can I perform a complete BOM explosion to find all components required for a finished product?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0002 | **Gate:** `proceed_with_warning`

**Expected answer:**
> Use a recursive query starting from the product_id of the finished good. At each level, join the bom table to find component_product_id entries. For each component, check if product_type is 'ASSEMBLY' or 'FINISHED_GOOD'. If so, recursively query bom again using that component_product_id as the new p…

**System answer:**
> I cannot describe a complete BOM explosion from the retrieved context, because the context does not define any bill-of-materials structure, parent-child component relationships, quantities, levels, or traversal logic for a finished product.

What the context does provide is only related metadata around manufacturing and components:

The “Manufacturing Routing” concept is keyed by route_id and prod…

**Sources retrieved (6):** `Manufacturing Routing`, `Hierarchical production planning and tracking`, `Actual stock levels of components and products at specific warehouse locations`, `Batches for traceability and inventory management`, `inspection and testing records for quality assurance`, `Component Supplier Relationship`

**Context previews (first 3):**

1. _Manufacturing Routing: The table is keyed by route_id and product_id and stores the ordered steps for a product, including route_name, sequence_number, operation_name, work_center, and timing fields. …_

2. _Hierarchical production planning and tracking…_

3. _Actual stock levels of components and products at specific warehouse locations…_

---

### ✅ QA-022 — How do I calculate the total material cost for a product including all sub-assemblies?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0004 | **Gate:** `proceed_with_warning`

**Expected answer:**
> Perform a recursive BOM explosion to find all leaf-level components. For each leaf component, join with the component table to get standard_cost. Multiply standard_cost by the accumulated quantity from the BOM traversal. Sum all component costs to get total material cost. This calculation must trave…

**System answer:**
> From the retrieved context, only part of this can be answered.

What is known:
The context indicates there is a concept of hierarchical production planning and tracking, which suggests products and sub-assemblies may be organized in a hierarchy. It also defines a Component Supplier Relationship table, where each component_id/supplier_id pair is unique and includes attributes such as is_preferred, …

**Sources retrieved (6):** `Manufacturing Routing`, `Hierarchical production planning and tracking`, `Actual stock levels of components and products at specific warehouse locations`, `Batches for traceability and inventory management`, `inspection and testing records for quality assurance`, `Component Supplier Relationship`

**Context previews (first 3):**

1. _Manufacturing Routing: The table is keyed by route_id and product_id and stores the ordered steps for a product, including route_name, sequence_number, operation_name, work_center, and timing fields. …_

2. _Hierarchical production planning and tracking…_

3. _Actual stock levels of components and products at specific warehouse locations…_

---

### ✅ QA-023 — How can I find all parent products that contain a specific component anywhere in their BOM structure?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0003 | **Gate:** `proceed_with_warning`

**Expected answer:**
> Use a recursive reverse traversal of the BOM. Start with the component_id as the initial parent_product_id. Find all records where this product appears as component_product_id in the bom table. For each parent_product_id found, check if it appears as a component_product_id in other bom records (is a…

**System answer:**
> From the retrieved context, only one relevant fact is available: there is a business concept called “Hierarchical production planning and tracking.” That suggests the knowledge graph includes some notion of multi-level production structure.

However, the context does not provide the BOM table name, parent-child relationship columns, product/component keys, or any recursive hierarchy model. Because…

**Sources retrieved (6):** `Actual stock levels of components and products at specific warehouse locations`, `Component Supplier Relationship`, `Manufacturing Routing`, `Batches for traceability and inventory management`, `inspection and testing records for quality assurance`, `Hierarchical production planning and tracking`

**Context previews (first 3):**

1. _Actual stock levels of components and products at specific warehouse locations…_

2. _Component Supplier Relationship: This table is a junction entity linking one component to one supplier, with a unique component_id/supplier_id pair and relationship attributes such as is_preferred, le…_

3. _Manufacturing Routing: The table is keyed by route_id and product_id and stores the ordered steps for a product, including route_name, sequence_number, operation_name, work_center, and timing fields. …_

---

### ✅ QA-024 — How do I identify work orders that require a specific component, considering nested sub-assemblies?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0003 | **Gate:** `proceed_with_warning`

**Expected answer:**
> First, perform reverse BOM traversal to find all parent products that contain the target component at any level. Then query the work_order table where product_id is in the set of parent products found. This includes work orders for finished goods that contain the component indirectly through sub-ass…

**System answer:**
> From the retrieved context, the only relevant fact is that the knowledge graph includes a business concept for “Hierarchical production planning and tracking,” which suggests the model supports some form of multi-level production structure, and a separate concept for “Actual stock levels of components and products at specific warehouse locations.” It also includes “Manufacturing Routing,” but that…

**Sources retrieved (6):** `Component Supplier Relationship`, `Manufacturing Routing`, `Actual stock levels of components and products at specific warehouse locations`, `Hierarchical production planning and tracking`, `Batches for traceability and inventory management`, `inspection and testing records for quality assurance`

**Context previews (first 3):**

1. _Component Supplier Relationship: This table is a junction entity linking one component to one supplier, with a unique component_id/supplier_id pair and relationship attributes such as is_preferred, le…_

2. _Manufacturing Routing: The table is keyed by route_id and product_id and stores the ordered steps for a product, including route_name, sequence_number, operation_name, work_center, and timing fields. …_

3. _Actual stock levels of components and products at specific warehouse locations…_

---

### ✅ QA-025 — How can I determine the maximum BOM depth level for any product?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0001 | **Gate:** `proceed_with_warning`

**Expected answer:**
> Use a recursive query on the bom table, incrementing a level counter at each traversal. Start with bom_level = 0 and add 1 for each recursive step. Track the maximum level reached across all product hierarchies. This identifies the most complex product structures with the deepest nesting.

**System answer:**
> From the retrieved context, I cannot determine how to calculate the maximum BOM depth level for a product.

What is known is only that the knowledge graph includes the business concept "Hierarchical production planning and tracking." However, the context does not provide a BOM table, parent-child product/component relationships, a level/depth attribute, or any schema details for traversing a produ…

**Sources retrieved (6):** `Manufacturing Routing`, `Actual stock levels of components and products at specific warehouse locations`, `Batches for traceability and inventory management`, `Hierarchical production planning and tracking`, `inspection and testing records for quality assurance`, `Component Supplier Relationship`

**Context previews (first 3):**

1. _Manufacturing Routing: The table is keyed by route_id and product_id and stores the ordered steps for a product, including route_name, sequence_number, operation_name, work_center, and timing fields. …_

2. _Actual stock levels of components and products at specific warehouse locations…_

3. _Batches for traceability and inventory management…_

---

### ✅ QA-026 — How do I find all products that have a specific product as a sub-assembly at any level?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0027 | **Gate:** `proceed_with_warning`

**Expected answer:**
> Perform a recursive search starting with the target product_id as the initial component_product_id in the bom table. For each parent_product_id found, check if that parent appears as a component in other bom entries. Continue recursively until reaching products that are not used as components elsewh…

**System answer:**
> From the retrieved context, the only relevant information is the business concept “Hierarchical production planning and tracking.” That indicates the knowledge graph covers hierarchical manufacturing structures in principle.

However, the context does not provide the schema details needed to answer how to find all products that contain a specific product as a sub-assembly at any level. Specificall…

**Sources retrieved (6):** `Actual stock levels of components and products at specific warehouse locations`, `Manufacturing Routing`, `Hierarchical production planning and tracking`, `Component Supplier Relationship`, `Batches for traceability and inventory management`, `inspection and testing records for quality assurance`

**Context previews (first 3):**

1. _Actual stock levels of components and products at specific warehouse locations…_

2. _Manufacturing Routing: The table is keyed by route_id and product_id and stores the ordered steps for a product, including route_name, sequence_number, operation_name, work_center, and timing fields. …_

3. _Hierarchical production planning and tracking…_

---

### ✅ QA-027 — How can I calculate the total lead time for a product including all sub-assembly lead times?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0051 | **Gate:** `proceed_with_warning`

**Expected answer:**
> Perform a recursive BOM explosion to find all components and sub-assemblies. For each product_id in the hierarchy, retrieve lead_time_days from the product table. The total lead time is the maximum of all lead times in the hierarchy (representing the longest dependency chain), or optionally sum lead…

**System answer:**
> From the retrieved context, the calculable parts are only partial.

For the manufacturing portion, use Manufacturing Routing. It is keyed by route_id and product_id and stores the ordered production steps for a product, including sequence_number, operation_name, work_center, and timing fields. Based on that, the direct production lead time for a product would come from its routing timing fields ac…

**Sources retrieved (6):** `Component Supplier Relationship`, `Manufacturing Routing`, `Hierarchical production planning and tracking`, `Actual stock levels of components and products at specific warehouse locations`, `Batches for traceability and inventory management`, `inspection and testing records for quality assurance`

**Context previews (first 3):**

1. _Component Supplier Relationship: This table is a junction entity linking one component to one supplier, with a unique component_id/supplier_id pair and relationship attributes such as is_preferred, le…_

2. _Manufacturing Routing: The table is keyed by route_id and product_id and stores the ordered steps for a product, including route_name, sequence_number, operation_name, work_center, and timing fields. …_

3. _Hierarchical production planning and tracking…_

---

### ✅ QA-028 — How do I generate a complete indented BOM report showing the hierarchical structure?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0016 | **Gate:** `proceed_with_warning`

**Expected answer:**
> Use a recursive query on the bom table that tracks the current depth level. Start with the top-level product (parent_product_id where product has no parent_product_id). At each level, output component details indented by depth level. Include product_name, quantity, and unit_of_measure. Recursively p…

**System answer:**
> From the retrieved context, I cannot describe how to generate a complete indented BOM report at the schema level, because the context does not define any BOM table, parent/child product-component relationship, hierarchy column, level/depth field, or quantity structure.

What the context does support is only this: there is a business concept of “Hierarchical production planning and tracking.” That …

**Sources retrieved (6):** `Hierarchical production planning and tracking`, `Manufacturing Routing`, `Component Supplier Relationship`, `inspection and testing records for quality assurance`, `Batches for traceability and inventory management`, `Actual stock levels of components and products at specific warehouse locations`

**Context previews (first 3):**

1. _Hierarchical production planning and tracking…_

2. _Manufacturing Routing: The table is keyed by route_id and product_id and stores the ordered steps for a product, including route_name, sequence_number, operation_name, work_center, and timing fields. …_

3. _Component Supplier Relationship: This table is a junction entity linking one component to one supplier, with a unique component_id/supplier_id pair and relationship attributes such as is_preferred, le…_

---

### ✅ QA-029 — How can I find which components appear most frequently across all product BOMs?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0003 | **Gate:** `proceed_with_warning`

**Expected answer:**
> Perform BOM explosion for all products and aggregate occurrences of each leaf-level component. Count how many distinct product hierarchies contain each component. Join with component table for component names. Order by frequency descending to identify common components that should be prioritized for…

**System answer:**
> The retrieved context does not provide enough schema detail to answer this directly. It does not include any BOM table, any product-to-component relationship table, or columns that show which components belong to which products. Because of that, I cannot describe a supported query or calculation for “which components appear most frequently across all product BOMs.”

What the context does contain i…

**Sources retrieved (6):** `Manufacturing Routing`, `Actual stock levels of components and products at specific warehouse locations`, `Hierarchical production planning and tracking`, `Component Supplier Relationship`, `Batches for traceability and inventory management`, `inspection and testing records for quality assurance`

**Context previews (first 3):**

1. _Manufacturing Routing: The table is keyed by route_id and product_id and stores the ordered steps for a product, including route_name, sequence_number, operation_name, work_center, and timing fields. …_

2. _Actual stock levels of components and products at specific warehouse locations…_

3. _Hierarchical production planning and tracking…_

---

### ✅ QA-030 — How do I detect circular references in the BOM structure to prevent infinite loops?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0000 | **Gate:** `proceed_with_warning`

**Expected answer:**
> Use a recursive query with a cycle detection check. Track the path of visited product_ids at each recursion level. If a product_id appears twice in the same path, a circular reference exists. Alternatively, check if any bom record has parent_product_id = component_product_id (direct self-reference),…

**System answer:**
> The retrieved context does not provide enough information to answer this. It only mentions the broad business concept “Hierarchical production planning and tracking,” but it does not define any BOM table, BOM fields, hierarchy rules, or validation logic. Because of that, the context is insufficient to determine how circular references are detected or prevented.

**Sources retrieved (6):** `Manufacturing Routing`, `Hierarchical production planning and tracking`, `Component Supplier Relationship`, `Batches for traceability and inventory management`, `inspection and testing records for quality assurance`, `Actual stock levels of components and products at specific warehouse locations`

**Context previews (first 3):**

1. _Manufacturing Routing: The table is keyed by route_id and product_id and stores the ordered steps for a product, including route_name, sequence_number, operation_name, work_center, and timing fields. …_

2. _Hierarchical production planning and tracking…_

3. _Component Supplier Relationship: This table is a junction entity linking one component to one supplier, with a unique component_id/supplier_id pair and relationship attributes such as is_preferred, le…_

---

### ✅ QA-031 — How can I determine the complete supplier chain for a finished product, including suppliers for all sub-assemblies?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0018 | **Gate:** `proceed_with_warning`

**Expected answer:**
> First, perform recursive BOM explosion to find all leaf-level components in the product hierarchy. Then query the component_supplier table for each component_id to find approved suppliers. Join with the supplier table to get supplier names, ratings, and contact information. Include supplier-specific…

**System answer:**
> From the retrieved context, only part of this can be answered.

What is known is that supplier assignment exists at the component level through the Component Supplier Relationship table. That table links one component to one supplier using a unique component_id/supplier_id pair, and it stores relationship attributes including is_preferred, lead_time_days, and unit_price. So, if you already know a …

**Sources retrieved (6):** `Component Supplier Relationship`, `Manufacturing Routing`, `Hierarchical production planning and tracking`, `Batches for traceability and inventory management`, `Actual stock levels of components and products at specific warehouse locations`, `inspection and testing records for quality assurance`

**Context previews (first 3):**

1. _Component Supplier Relationship: This table is a junction entity linking one component to one supplier, with a unique component_id/supplier_id pair and relationship attributes such as is_preferred, le…_

2. _Manufacturing Routing: The table is keyed by route_id and product_id and stores the ordered steps for a product, including route_name, sequence_number, operation_name, work_center, and timing fields. …_

3. _Hierarchical production planning and tracking…_

---

### ✅ QA-032 — How do I check if sufficient inventory exists across all warehouses to fulfill a work order?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0188 | **Gate:** `proceed_with_warning`

**Expected answer:**
> For the work_order's product_id, perform recursive BOM explosion to get all required components with quantities. For each component, sum the available quantity (quantity_on_hand - quantity_reserved) across all warehouses from the inventory table. Compare aggregated available inventory against requir…

**System answer:**
> From the retrieved context, only part of this can be answered.

What is known is that the knowledge graph includes the business concept of “Actual stock levels of components and products at specific warehouse locations.” That indicates inventory is tracked by warehouse location, so checking availability “across all warehouses” would, at a conceptual level, require aggregating those stock levels ac…

**Sources retrieved (6):** `Batches for traceability and inventory management`, `Manufacturing Routing`, `Actual stock levels of components and products at specific warehouse locations`, `Hierarchical production planning and tracking`, `Component Supplier Relationship`, `inspection and testing records for quality assurance`

**Context previews (first 3):**

1. _Batches for traceability and inventory management…_

2. _Manufacturing Routing: The table is keyed by route_id and product_id and stores the ordered steps for a product, including route_name, sequence_number, operation_name, work_center, and timing fields. …_

3. _Actual stock levels of components and products at specific warehouse locations…_

---

### ✅ QA-033 — How can I find which quality control inspections failed for components from specific suppliers?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0029 | **Gate:** `proceed_with_warning`

**Expected answer:**
> Query the quality_control table filtering by result = 'FAIL'. Join with the batch table to get product_id and production_date. Join with the bom table recursively to trace which products contain failed components. Join with component_supplier and supplier tables to identify the source supplier. Filt…

**System answer:**
> From the retrieved context, I can only say this at a schema/concept level:

There is a business concept for “inspection and testing records for quality assurance,” and there is a defined “Component Supplier Relationship” entity that links components to suppliers through a unique component_id / supplier_id pair, with attributes including is_preferred, lead_time_days, and unit_price.

So, the part t…

**Sources retrieved (6):** `inspection and testing records for quality assurance`, `Actual stock levels of components and products at specific warehouse locations`, `Manufacturing Routing`, `Batches for traceability and inventory management`, `Component Supplier Relationship`, `Hierarchical production planning and tracking`

**Context previews (first 3):**

1. _inspection and testing records for quality assurance…_

2. _Actual stock levels of components and products at specific warehouse locations…_

3. _Manufacturing Routing: The table is keyed by route_id and product_id and stores the ordered steps for a product, including route_name, sequence_number, operation_name, work_center, and timing fields. …_

---

### ✅ QA-034 — How do I calculate the total manufacturing time for a work order including all sub-assembly work orders?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0052 | **Gate:** `proceed_with_warning`

**Expected answer:**
> Query the work_order table starting with the parent work_order. Find all child work_orders where parent_work_order matches the current work_order_id. For each work order (parent and children), join with the route table on product_id to get all operations. Sum (cycle_time_minutes * quantity) plus set…

**System answer:**
> From the retrieved context, only part of this can be answered.

What is known is that the “Manufacturing Routing” structure is keyed by route_id and product_id and stores the ordered production steps for a product, including sequence_number, operation_name, work_center, and timing fields. Based on that, the manufacturing time for a single product route would logically come from the routing data by…

**Sources retrieved (6):** `Manufacturing Routing`, `Component Supplier Relationship`, `Batches for traceability and inventory management`, `inspection and testing records for quality assurance`, `Hierarchical production planning and tracking`, `Actual stock levels of components and products at specific warehouse locations`

**Context previews (first 3):**

1. _Manufacturing Routing: The table is keyed by route_id and product_id and stores the ordered steps for a product, including route_name, sequence_number, operation_name, work_center, and timing fields. …_

2. _Component Supplier Relationship: This table is a junction entity linking one component to one supplier, with a unique component_id/supplier_id pair and relationship attributes such as is_preferred, le…_

3. _Batches for traceability and inventory management…_

---

### ✅ QA-035 — How can I identify which shipments are overdue and their impact on work orders?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0003 | **Gate:** `proceed_with_warning`

**Expected answer:**
> Query the shipment table filtering for status = 'SHIPPED' where actual_arrival is NULL and estimated_arrival is in the past (overdue). Join with the component_supplier table via supplier_id and component_id to identify which components are delayed. Perform reverse BOM lookup to find which parent pro…

**System answer:**
> I cannot determine which shipments are overdue or their impact on work orders from the retrieved context.

The context does not include any shipment entity, purchase order data, due dates, expected or actual receipt dates, work order tables, or delay-calculation rules. Because those concepts are absent, there is no supported way to define “overdue shipment” or trace a shipment’s effect on a work o…

**Sources retrieved (6):** `Manufacturing Routing`, `Component Supplier Relationship`, `Batches for traceability and inventory management`, `Hierarchical production planning and tracking`, `Actual stock levels of components and products at specific warehouse locations`, `inspection and testing records for quality assurance`

**Context previews (first 3):**

1. _Manufacturing Routing: The table is keyed by route_id and product_id and stores the ordered steps for a product, including route_name, sequence_number, operation_name, work_center, and timing fields. …_

2. _Component Supplier Relationship: This table is a junction entity linking one component to one supplier, with a unique component_id/supplier_id pair and relationship attributes such as is_preferred, le…_

3. _Batches for traceability and inventory management…_

---

### ✅ QA-036 — How do I find which batches are approaching or past expiry and contain components from specific suppliers?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0165 | **Gate:** `proceed_with_warning`

**Expected answer:**
> Query the batch table filtering for expiry_date within a warning window (e.g., next 30 days) or past expiry. Join with the bom table recursively on product_id to trace all components used in those batches. Join with component_supplier and supplier tables to filter by specific suppliers. Results iden…

**System answer:**
> From the retrieved context, I can only answer this partially.

What is known is that there is a business concept for Batches for traceability and inventory management, and there is a Component Supplier Relationship table that links one component to one supplier with a unique component_id/supplier_id pair. That relationship includes attributes such as is_preferred, lead_time_days, and unit_price.

…

**Sources retrieved (6):** `Actual stock levels of components and products at specific warehouse locations`, `Component Supplier Relationship`, `Batches for traceability and inventory management`, `Manufacturing Routing`, `Hierarchical production planning and tracking`, `inspection and testing records for quality assurance`

**Context previews (first 3):**

1. _Actual stock levels of components and products at specific warehouse locations…_

2. _Component Supplier Relationship: This table is a junction entity linking one component to one supplier, with a unique component_id/supplier_id pair and relationship attributes such as is_preferred, le…_

3. _Batches for traceability and inventory management…_

---

### ✅ QA-037 — How can I generate a material requirements plan showing when to order components based on work order schedules?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0006 | **Gate:** `proceed_with_warning`

**Expected answer:**
> Query all work_orders with status 'PENDING' ordered by planned_start_date. For each work_order, perform BOM explosion to get required components and quantities. For each component, query inventory for current available stock across warehouses. Calculate net requirements = (required quantity * work_o…

**System answer:**
> The retrieved context is not sufficient to define a full material requirements planning process based on work order schedules.

From the available context, the only planning-related structures are:

The “Manufacturing Routing” table, keyed by route_id and product_id, stores ordered production steps with route_name, sequence_number, operation_name, work_center, and timing fields. This describes the…

**Sources retrieved (6):** `Manufacturing Routing`, `Hierarchical production planning and tracking`, `Actual stock levels of components and products at specific warehouse locations`, `Component Supplier Relationship`, `Batches for traceability and inventory management`, `inspection and testing records for quality assurance`

**Context previews (first 3):**

1. _Manufacturing Routing: The table is keyed by route_id and product_id and stores the ordered steps for a product, including route_name, sequence_number, operation_name, work_center, and timing fields. …_

2. _Hierarchical production planning and tracking…_

3. _Actual stock levels of components and products at specific warehouse locations…_

---

### ✅ QA-038 — How do I trace the complete genealogy of a component from supplier through batch to finished goods?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0068 | **Gate:** `proceed_with_warning`

**Expected answer:**
> Start with a shipment from the supplier (shipment table with supplier_id and shipment_type = 'INBOUND'). Track to inventory updates via component_id and warehouse_id. Identify batches that consumed the component via reverse BOM lookup (batch.product_id → bom hierarchy → component_id). Query quality_…

**System answer:**
> From the retrieved context, I can only establish a partial schema-level starting point, not a complete genealogy path.

The only explicit supplier-to-component structure described is Component Supplier Relationship. It is a junction entity linking one component to one supplier, with a unique component_id/supplier_id pair, and attributes including is_preferred, lead_time_days, and unit_price. That …

**Sources retrieved (6):** `Component Supplier Relationship`, `Batches for traceability and inventory management`, `Actual stock levels of components and products at specific warehouse locations`, `Hierarchical production planning and tracking`, `Manufacturing Routing`, `inspection and testing records for quality assurance`

**Context previews (first 3):**

1. _Component Supplier Relationship: This table is a junction entity linking one component to one supplier, with a unique component_id/supplier_id pair and relationship attributes such as is_preferred, le…_

2. _Batches for traceability and inventory management…_

3. _Actual stock levels of components and products at specific warehouse locations…_

---

### ✅ QA-039 — How can I find alternative suppliers for components that are critical for multiple products?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0049 | **Gate:** `proceed_with_warning`

**Expected answer:**
> Perform BOM explosion for all active products and count component usage frequency. Identify high-frequency components. Query component_supplier table to find all suppliers for these components. Filter to suppliers with rating >= 4.0 (high quality) and is_preferred = 'Y'. For each component, list alt…

**System answer:**
> From the retrieved context, the only supported way to find alternative suppliers is through the Component Supplier Relationship business concept. It is a junction entity with a unique component_id/supplier_id pair and attributes including is_preferred, lead_time_days, and unit_price. For any component you already know, you would look up all Component Supplier Relationship records for that componen…

**Sources retrieved (6):** `Actual stock levels of components and products at specific warehouse locations`, `Manufacturing Routing`, `inspection and testing records for quality assurance`, `Batches for traceability and inventory management`, `Component Supplier Relationship`, `Hierarchical production planning and tracking`

**Context previews (first 3):**

1. _Actual stock levels of components and products at specific warehouse locations…_

2. _Manufacturing Routing: The table is keyed by route_id and product_id and stores the ordered steps for a product, including route_name, sequence_number, operation_name, work_center, and timing fields. …_

3. _inspection and testing records for quality assurance…_

---

### ✅ QA-040 — How do I calculate the total landed cost for a product including component costs, supplier lead times, and manufacturing operations?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0209 | **Gate:** `proceed_with_warning`

**Expected answer:**
> Perform recursive BOM explosion to get all leaf components. For each component, query component_supplier to get unit_price from primary supplier. Multiply by accumulated BOM quantity for material cost. Add shipping costs (estimated from shipment history). Query route table for the product to get all…

**System answer:**
> From the retrieved context, I can only state the pieces of data that appear to be relevant; I cannot determine a complete landed-cost calculation.

What is known from the context is that the Component Supplier Relationship table stores the supplier-component association and includes component_id, supplier_id, is_preferred, lead_time_days, and unit_price. This means the context supports identifying…

**Sources retrieved (6):** `Component Supplier Relationship`, `Manufacturing Routing`, `Hierarchical production planning and tracking`, `Actual stock levels of components and products at specific warehouse locations`, `Batches for traceability and inventory management`, `inspection and testing records for quality assurance`

**Context previews (first 3):**

1. _Component Supplier Relationship: This table is a junction entity linking one component to one supplier, with a unique component_id/supplier_id pair and relationship attributes such as is_preferred, le…_

2. _Manufacturing Routing: The table is keyed by route_id and product_id and stores the ordered steps for a product, including route_name, sequence_number, operation_name, work_center, and timing fields. …_

3. _Hierarchical production planning and tracking…_

---

## Anomalies & Observations

No anomalies detected. All questions grounded with acceptable RAGAS scores.
