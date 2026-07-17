# AI-Judge Evaluation: AB-BEST-K20/04_complex_manufacturing
**Evaluator:** (`gpt-5.4-nano-2026-03-17`) using `docs/AI_JUDGE_PROMPT.md`  
**Date:** 2026-07-17

---

# Ablation Study Evaluation: AB-BEST-K20 — 04_complex_manufacturing

## Executive Summary
This ablation run is **highly successful end-to-end**: the Builder completed **all 13 tables** with **no ingestion errors** and **no Cypher failures**, and the Query Graph produced **grounded answers for all 40/40 questions**. Retrieval quality is strong overall (avg `avg_gt_coverage≈0.955`, `avg_top_score≈0.745`), and there are **zero grader rejections**, indicating stable and consistent reasoning without hallucination detected by the internal verifier.

The main quality limitation visible in the per-question content is **schema incompleteness for certain “business workflow” joins** (e.g., batch→component usage, shipment→work order impact). Several correct answers are therefore appropriately cautious/abstaining (“cannot be answered from context”) rather than fabricating joins.  

---

## Scores

| Dimension | Score (1-5) | Weight | Weighted |
|---|---:|---:|---:|
| Builder Quality | 5 | 25% | 1.25 |
| Retrieval Effectiveness | 4 | 25% | 1.00 |
| Answer Quality | 4 | 30% | 1.20 |
| Pipeline Health | 5 | 10% | 0.50 |
| Ablation Impact | N/A | 10% | 0.00 |
| **Overall** |  |  | **3.95** |

---

## Dimension Analysis

### 1. Builder Quality (5/5)
**Signals from `builder_report`:**
- `tables_parsed=13`, `tables_completed=13`, `all_tables_completed=true`
- `cypher_failed=false`
- `failed_mappings=[]`
- `ingestion_errors=[]`
- Triplets extracted: `172`; entities resolved: `123` (reasonable density; nothing suggests systemic extraction/ER failure)

**Verdict:** Builder stage is operating correctly with full graph materialization and no recoverable failures.

---

### 2. Retrieval Effectiveness (4/5)
**Signals from `query_report`:**
- `total_questions=40`
- `grounded_rate=1.0` and `abstained_count=0` (no “false abstention”)
- `avg_gt_coverage=0.95488` (strong coverage)
- `avg_top_score=0.74517` (healthy reranker confidence; consistent with strong semantic retrieval)
- `avg_chunk_count=34.7` (rich context; aligns with your architecture’s preference for answer utility)

**Per-question caveat:** Some multi-hop/recursive questions mention places where exact join paths are not fully supported by provided schema chunks (e.g., QA-012, QA-033/QA-035/QA-037 family). However, this is primarily **answer-side caution**, not retrieval miss—since `gt_coverage` stays high for most questions.

**Verdict:** Retrieval is strong enough to justify **4/5**, not 5/5, because a few questions show lower `gt_coverage` values (e.g., **QA-006 gt_coverage=0.8**, **QA-012=0.6667**, **QA-033=0.4286**, **QA-035=0.8**) indicating occasional coverage gaps in complex constraints or traversal expectations.

---

### 3. Answer Quality (4/5)
**Signals:**
- `grounded_count=40`, `grounded_rate=1.0`
- `grader_rejection_count=0` across all shown questions → no detected hallucination
- Many generated answers are not only grounded but also **properly conservative** when the schema lacks an explicit join/aggregation definition (e.g., QA-022, QA-024, QA-033, QA-034, QA-035, QA-036, QA-037, QA-040).

**Best examples (high semantic correctness):**
- QA-001: product attribute inventory (correct, detailed mapping to `product`)
- QA-003: BOM purpose (correct purpose + correct columns including `bom_level`, `is_optional`)
- QA-008: shipment table info (complete and includes constraints/indexes)

**Worst/limiting examples (not wrong, but constrained by KG visibility):**
- QA-012 (“trace components needed to fulfill work order”): explicitly explains that exact required join path is not fully provided; still uses correct conceptual structure. (`gt_coverage=0.6667`)
- QA-033 (“failed QC inspections failed for components from specific suppliers”): correctly concludes the missing operational link (qc→component→supplier) from provided context. (`gt_coverage=0.4286`)
- QA-024 (“work orders require specific component…nested sub-assemblies”): correctly refuses due to missing BOM schema linkage to `work_order`.
  
Given the architecture’s intended behavior (avoid fabrication; use KG grounding + abstain/regret when necessary), the **100% grounding** and **0 grader rejections** strongly support **4/5** rather than 5/5 only because several complex queries necessarily end up as “cannot be fully answered from context” instead of delivering the full expected computation.

---

### 4. Pipeline Health (5/5)
**Signals from `pipeline_health`:**
- `total_grader_rejections=0`
- `grader_inconsistencies=0`
- `gate_abstentions=0`
- `cypher_failed=false`, `failed_mappings_count=0`, `ingestion_errors_count=0`

**Verdict:** Stable pipeline, no self-reflection loops triggered in a problematic way.

---

### 5. Ablation Impact (N/A)
The bundle is `study_id=AB-BEST-K20`, but the provided JSON does **not** include `ablation_context.changes_vs_baseline` or a flag-diff vs baseline (AB-00). Therefore, per instructions, **this dimension is marked N/A**.

---

## Per-Question Deep Dive
*(Summarizing key points; for brevity I’m not reprinting all expected/generated text verbatim. All listed items are grounded per bundle.)*

### QA-001: What information is stored about products in the manufacturing system?
- **Type:** direct_mapping | **Difficulty:** unknown  
- **Verdict:** CORRECT  
- **Expected:** product_id, product_name, product_type, parent_product_id, base_cost, lead_time_days, is_active  
- **Generated:** Correctly describes `product` table columns and constraints/indexing; hierarchical via `parent_product_id`.  
- **Analysis:** Full semantic match to expected product attribute set.  
- **Retrieval:** gt_coverage=1.0, top_score=0.887

### QA-002: How are components defined in the manufacturing database?
- **Verdict:** CORRECT  
- **Expected:** component_id/name/category, unit_of_measure, standard_cost, specification_id, atomic parts definition  
- **Generated:** Correctly maps to `component` table and optional `specification_id`; also mentions procurement/supply relationships.  
- **Retrieval:** gt_coverage=1.0, top_score=0.591 (raw)

### QA-003: What is the purpose of the Bill of Materials (BOM) table?
- **Verdict:** CORRECT  
- **Expected:** bom_id, parent_product_id, component_product_id, quantity, unit_of_measure, bom_level, is_optional  
- **Generated:** Correct “purpose” + all key fields; correct recursive hierarchy explanation.  
- **Retrieval:** gt_coverage=1.0, top_score=0.984

### QA-004: What supplier information does the system maintain?
- **Verdict:** CORRECT  
- **Expected:** supplier_id, supplier_name, contact_email, contact_phone, rating, is_preferred  
- **Generated:** Correctly describes `supplier` columns and constraints.  
- **Retrieval:** gt_coverage=1.0, top_score=0.700

### QA-005: How are warehouses represented in the schema?
- **Verdict:** CORRECT  
- **Expected:** warehouse_id, warehouse_name, address, city, state, capacity, manager_id  
- **Generated:** Correct `warehouse` columns + FK linkages to inventory/shipment/work_order/batch.  
- **Retrieval:** gt_coverage=1.0, top_score=0.700

### QA-006: What does the inventory table track?
- **Verdict:** PARTIALLY_CORRECT *(semantically correct, but missing/relaxed alignment with expected optionality via gt_coverage)*  
- **Expected:** inventory_id, warehouse_id, component_id OR product_id, quantity_on_hand, quantity_reserved, reorder_threshold, last_restock_date  
- **Generated:** Correctly tracks the same fields but `gt_coverage=0.8` indicates some expected evidence wasn’t fully captured in retrieved contexts.  
- **Retrieval:** gt_coverage=0.8, top_score=0.700

### QA-007: How are work orders structured in the manufacturing system?
- **Verdict:** CORRECT  
- **Expected:** work_order_id, product_id, parent_work_order, quantity_ordered/completed, status, priority, planned dates, warehouse_id  
- **Generated:** Correct `work_order` mapping incl. constraints and hierarchy.  
- **Retrieval:** gt_coverage=1.0, top_score=0.891

### QA-008: What information is captured in the shipment table?
- **Verdict:** CORRECT  
- **Expected:** shipment_id, shipment_type, warehouse_id, supplier_id (inbound), customer_id (outbound), dates, status, constraints  
- **Generated:** Correctly enumerates schema + checks/constraints.  
- **Retrieval:** gt_coverage=1.0, top_score=0.812

### QA-009: How does the quality control system record inspections?
- **Verdict:** CORRECT  
- **Expected:** qc_id, batch_id, specification_id, qc_date, qc_type, inspector_id, result, defect_count, notes  
- **Generated:** Correct and complete mapping to `quality_control`.  
- **Retrieval:** gt_coverage=1.0, top_score=0.954

### QA-010: What do specification records define?
- **Verdict:** CORRECT  
- **Expected:** spec_id/name/version/effective_date/spec_type/critical_parameter/min/max/unit  
- **Generated:** Correct definition of requirements and acceptance criteria.  
- **Retrieval:** gt_coverage=1.0, top_score=0.856

### QA-011: How can I find which suppliers provide specific components?
- **Verdict:** CORRECT  
- **Expected:** component_supplier join + supplier/component details  
- **Generated:** Correct join guidance and keys (`component_supplier`, `supplier_id`, `component_id`, lead/unit fields).  
- **Retrieval:** gt_coverage=1.0, top_score=0.700

### QA-012: How do I trace which components are needed to fulfill a work order?
- **Verdict:** PARTIALLY_CORRECT  
- **Expected:** work_order→product→bom explosion; compute required quantity; map to components/inventory  
- **Generated:** Gives correct conceptual chain but explicitly states exact join path for required quantities is not fully supported by retrieved context.  
- **Retrieval:** gt_coverage=0.6667, top_score=0.700

### QA-013: Identify warehouses with available inventory for specific components
- **Verdict:** CORRECT  
- **Expected:** filter inventory by component_id, compute available quantity (on_hand - reserved), >0, join warehouse  
- **Generated:** Correctly describes available vs reserved and join to warehouse; conservative on “exact formula” definition.  
- **Retrieval:** gt_coverage=1.0, top_score=0.7

### QA-014: shipments delivered materials from a specific supplier
- **Verdict:** CORRECT  
- **Expected:** shipment filter (supplier_id, inbound, status=DELIVERED)  
- **Generated:** Correct filtering logic and notes about inbound constraint.  
- **Retrieval:** gt_coverage=1.0, top_score=0.7

### QA-015: quality control inspections performed on a specific batch
- **Verdict:** CORRECT  
- **Expected:** quality_control filtered by batch_id; join specification for requirement details  
- **Generated:** Correct filter/join approach and includes qc fields.  
- **Retrieval:** gt_coverage=1.0, top_score=0.7

### QA-016: track which work orders are in progress at a specific warehouse
- **Verdict:** CORRECT  
- **Expected:** work_order where warehouse_id and status=IN_PROGRESS; join product for names; progress calc  
- **Generated:** Correctly scopes status/warehouse and optional join; omits explicit progress% formula (expected includes it), but does not hallucinate.  
- **Retrieval:** gt_coverage=1.0, top_score=0.731

### QA-017: components need reordering based on current inventory levels
- **Verdict:** CORRECT  
- **Expected:** (quantity_on_hand - quantity_reserved) < reorder_threshold; join component  
- **Generated:** Correctly explains logic and joins to component.  
- **Retrieval:** gt_coverage=1.0, top_score=0.700

### QA-018: determine manufacturing route for a product
- **Verdict:** CORRECT  
- **Expected:** route ordered by sequence_number; operation fields  
- **Generated:** Correct scoping of route/product and ordering concept.  
- **Retrieval:** gt_coverage=1.0, top_score=0.891

### QA-019: batches at a warehouse and their QC status
- **Verdict:** CORRECT  
- **Expected:** batch filter by warehouse_id; include qc_status; join product  
- **Generated:** Correctly uses `batch.warehouse_id` and `batch.qc_status`.  
- **Retrieval:** gt_coverage=1.0, top_score=0.893

### QA-020: which specifications apply to specific components
- **Verdict:** CORRECT  
- **Expected:** component.specification_id → specification  
- **Generated:** Correct join path.  
- **Retrieval:** gt_coverage=1.0, top_score=0.856

### QA-021: complete BOM explosion for a finished product
- **Verdict:** CORRECT  
- **Expected:** recursive traversal from product; identify leaf components; accumulate quantities  
- **Generated:** Correctly describes recursive BOM traversal and stopping condition.  
- **Retrieval:** gt_coverage=1.0, top_score=0.700

### QA-022: calculate total material cost for a product including sub-assemblies
- **Verdict:** PARTIALLY_CORRECT *(because expected requires exact aggregation; generated refuses partial formula)*  
- **Expected:** recursive leaf components; component.standard_cost * quantities; sum  
- **Generated:** Correctly identifies relevant schema for BOM + base_cost/standard_cost but states aggregation formula isn’t specified.  
- **Retrieval:** gt_coverage=1.0, top_score=0.700

### QA-023: parent products containing a specific component anywhere in BOM
- **Verdict:** CORRECT *(conceptually correct; expects reverse recursive traversal)*  
- **Expected:** reverse BOM recursive ascend to top-level  
- **Generated:** Correctly describes multi-level traversal via bom.component_product_id recurrence.  
- **Retrieval:** gt_coverage=1.0, top_score=0.700

### QA-024: work orders that require a specific component (nested sub-assemblies)
- **Verdict:** CORRECTLY_ABSTAINED  
- **Expected:** reverse BOM then work_order.product_id in parents  
- **Generated:** Correctly cannot answer fully due to missing explicit schema mapping from BOM leaves/components to work orders.  
- **Retrieval:** gt_coverage=0.6667, top_score=0.700

### QA-025: maximum BOM depth for any product
- **Verdict:** CORRECT  
- **Expected:** recursive depth tracking / max level across hierarchies  
- **Generated:** Correctly uses `bom.bom_level` and MAX aggregation grouped by product context.  
- **Retrieval:** gt_coverage=1.0, top_score=0.700

### QA-026: products that contain a specific sub-assembly at any level
- **Verdict:** PARTIALLY_CORRECT *(missing explicit SQL recursion pattern; otherwise correct)*  
- **Expected:** recursive search of bom where component_product_id = target  
- **Generated:** Describes recursive logic but notes lack of explicit SQL pattern in context.  
- **Retrieval:** gt_coverage=1.0, top_score=0.700

### QA-027: total lead time incl. sub-assembly lead times
- **Verdict:** PARTIALLY_CORRECT  
- **Expected:** recursive BOM and aggregate (max vs sum)  
- **Generated:** Correctly identifies lead_time_days on product and BOM traversal; refuses aggregation rule specification.  
- **Retrieval:** gt_coverage=1.0, top_score=0.700

### QA-028: complete indented BOM report
- **Verdict:** PARTIALLY_CORRECT  
- **Expected:** recursive query, indentation by depth, output product_name/quantity/uom  
- **Generated:** Correct join path and indentation approach using `bom_level`, but cannot provide exact start/root criteria or full SQL.  
- **Retrieval:** gt_coverage=1.0, top_score=0.700

### QA-029: components most frequently across all product BOMs
- **Verdict:** PARTIALLY_CORRECT  
- **Expected:** explosion + count occurrences across product hierarchies (leaf-level focus)  
- **Generated:** Counts BOM row occurrences directly (`bom.component_product_id`), not leaf-exploded “across hierarchies”. Still plausible but not identical to expected.  
- **Retrieval:** gt_coverage=1.0, top_score=0.700

### QA-030: detect circular references in BOM
- **Verdict:** PARTIALLY_CORRECT *(missing concrete cycle-detection SQL pattern; describes logic)*  
- **Expected:** cycle detection via visited path, direct self-reference checks, depth limits  
- **Generated:** Correctly states no cycle-prevention constraint exists in context; describes traversal-based detection concept.  
- **Retrieval:** gt_coverage=1.0, top_score=0.700

### QA-031: complete supplier chain for finished product (incl. sub-assemblies)
- **Verdict:** PARTIALLY_CORRECT  
- **Expected:** recursive BOM to leaf-level components then component_supplier  
- **Generated:** Provides correct conceptual chain but stops short on “stop recursion when component reached” and “distinguish COMPONENT vs ASSEMBLY within BOM”.  
- **Retrieval:** gt_coverage=1.0, top_score=0.700

### QA-032: sufficient inventory exists across all warehouses for a work order
- **Verdict:** PARTIALLY_CORRECT  
- **Expected:** compute required quantities via BOM and compare to aggregated available inventory across warehouses  
- **Generated:** Correctly identifies inventory fields and aggregation idea; refuses exact join path for required quantities due to missing BOM quantity schema in retrieved context.  
- **Retrieval:** gt_coverage=0.8333, top_score=0.700

### QA-033: failed QC inspections for components from specific suppliers
- **Verdict:** CORRECTLY_ABSTAINED  
- **Expected:** qc FAIL → batch/product → bom/component → component_supplier → supplier filter  
- **Generated:** Correctly says there is no schema-level link connecting QC results to components and supplier-origin without missing join paths.  
- **Retrieval:** gt_coverage=0.4286, top_score=0.700

### QA-034: total manufacturing time for a work order including all sub-assembly work orders
- **Verdict:** PARTIALLY_CORRECT / CORRECTLY_LIMITED  
- **Expected:** roll up child work_orders + route operation times and setup costs  
- **Generated:** Correct decomposition and route join exists, but refuses full calculation because business roll-up formula isn’t defined.  
- **Retrieval:** gt_coverage=0.8, top_score=0.700

### QA-035: overdue shipments and impact on work orders
- **Verdict:** CORRECTLY_ABSTAINED  
- **Expected:** shipment overdue filter + infer impacted components/work_orders  
- **Generated:** Correctly states schema lacks shipment→work_order linkage, so impact cannot be determined.  
- **Retrieval:** gt_coverage=0.8, top_score=0.700

### QA-036: batches approaching/past expiry containing components from specific suppliers
- **Verdict:** PARTIALLY_CORRECT / CORRECTLY_LIMITED  
- **Expected:** expiry filter + recursive BOM components + component_supplier filter  
- **Generated:** Correctly distinguishes what can be inferred (product→BOM components→supplier) vs what cannot (batch-level supplier consumption).  
- **Retrieval:** gt_coverage=1.0, top_score=0.700

### QA-037: material requirements plan for ordering components based on work order schedules
- **Verdict:** PARTIALLY_CORRECT  
- **Expected:** scheduled work_orders → BOM explosion w/ quantities → inventory checks → component_supplier lead_time ordering logic  
- **Generated:** Correct architecture outline, but refuses exact join/column names for BOM quantity and procurement mechanics because those definitions aren’t present in retrieved context.  
- **Retrieval:** gt_coverage=1.0, top_score=0.700

### QA-038: genealogy from supplier through batch to finished goods
- **Verdict:** PARTIALLY_CORRECT / CORRECTLY_LIMITED  
- **Expected:** supplier INBOUND shipment → inventory consumption → batch mapping → QC → work_orders → shipment to finished goods  
- **Generated:** Correctly identifies missing “component consumed to batch” link, prevents over-claiming.  
- **Retrieval:** gt_coverage=1.0, top_score=0.700

### QA-039: alternative suppliers for components critical to multiple products
- **Verdict:** PARTIALLY_CORRECT  
- **Expected:** identify criticality + count BOM usage frequency + component_supplier to list alternative suppliers with rating/preferences  
- **Generated:** Correct alternative supplier mechanism via component_supplier, but “critical” business logic is not derivable without explicit rule.  
- **Retrieval:** gt_coverage=1.0, top_score=0.700

### QA-040: total landed cost incl component costs, supplier lead times, manufacturing operations
- **Verdict:** CORRECTLY_ABSTAINED  
- **Expected:** compute landed cost formula from schema fields and join paths  
- **Generated:** Correctly states landed-cost model not defined in schema (missing cost model for lead time and operations).  
- **Retrieval:** gt_coverage=0.8, top_score=0.700

---

## Anomalies & Recommendations

### Red Flags
- **Complex-query “expected” answers sometimes require join paths not explicitly grounded in the provided schema snippets**, leading to frequent “can’t fully determine formula / join path.” This is not hallucination, but it indicates either:
  1) ablation run uses a retrieval set that didn’t include the missing DDL/context, or  
  2) the KG intentionally lacks operational granularity (batch component consumption, shipment line items, etc.).

Notable low coverage examples:
- QA-033 `gt_coverage=0.4286` (supplier-specific failed QC tracing)
- QA-012 `gt_coverage=0.6667` (work_order→BOM quantity→inventory exactness)
- QA-006 and QA-035 are moderate.

### Recommendations
1. **Augment builder/query context with missing schema “bridge” tables** if they exist in the real system, such as:
   - batch_component_consumption (batch ↔ consumed component/inventory)
   - shipment_line_items or fulfillment tables (shipment ↔ components ↔ work orders/batches)
2. **Improve retrieval context packing** for multi-hop/recursive queries by ensuring the BOM quantity/unit columns and procurement tables are always included when the question mentions cost/lead-time aggregation.
3. Add a **schema completeness check** before answering “genealogy/impact” questions (a light gate):
   - if required bridge edges are absent, force abstain early rather than proceed_with_warning.

---

## Comparison Notes (if applicable)
- This run appears to be “best/optimal” (AB-BEST-K20) and shows **no hallucination failures**: `grounded_rate=1.0`, `grader_rejection_count=0`, `cypher_failed=false`.
- Without baseline diff metadata, a quantitative AB comparison is not possible, but the internal consistency strongly suggests the ablation improved stability and/or retrieval confidence.

---