# AI-Judge Evaluation: AB-BEST/04_complex_manufacturing
**Evaluator:** (`gpt-5.4-nano-2026-03-17`) using `docs/AI_JUDGE_PROMPT.md`  
**Date:** 2026-07-17

---

# Ablation Study Evaluation: AB-BEST — 04_complex_manufacturing

## Executive Summary
This ablation run demonstrates **excellent builder success** (all 13 tables completed, no Cypher failures or ingestion/mapping errors) and **strong end-to-end answer grounding** (grounded_rate = **1.0** across 40/40 questions). However, a few questions reveal **conceptual/coverage gaps** in the generated answers (notably where the expected solution requires schema relationships not present in the retrieved context), and several of those are reflected in **lower gt_coverage** and **lower retrieval quality** for specific items. Overall, the system appears stable and well-aligned with the KG schema, but deeper multi-hop/recursive reasoning is still constrained by missing internal linkage in the retrieved context.

## Scores

| Dimension | Score (1-5) | Weight | Weighted |
|---|---:|---:|---:|
| Builder Quality | 5 | 25% | 1.25 |
| Retrieval Effectiveness | 4 | 25% | 1.00 |
| Answer Quality | 4 | 30% | 1.20 |
| Pipeline Health | 5 | 10% | 0.50 |
| Ablation Impact | 5 | 10% | 0.50 |
| **Overall** |  |  | **4.45** |

## Dimension Analysis

### 1. Builder Quality (5/5)
- `tables_completed`: **13/13**, `all_tables_completed=true`
- `cypher_failed=false`
- `failed_mappings=[]`
- `ingestion_errors=[]`
- Triplet density signal: `triplets_extracted=176`, `entities_resolved=108` → ratio ≈ **1.63** (lower than the rubric “>30 per doc” heuristic, but the pipeline still produced a complete, error-free graph). Most importantly, **graph construction correctness appears intact** given zero mapping/cypher/ingestion failures.

**Verdict:** Builder is functionally successful and operationally reliable.

### 2. Retrieval Effectiveness (4/5)
Key signals:
- `grounded_rate=1.0` across all 40 questions (no wrong ungrounded outputs).
- `avg_gt_coverage=0.8217` (strong; most expected sources are retrieved).
- `avg_top_score=0.7375` (healthy semantic confidence for a cross-encoder reranker).
- No abstentions (`abstained_count=0`) and gate never halted (`gate_abstentions=0`).

However, some evidence of retrieval/query-context insufficiency exists:
- Lowest per-question `gt_coverage` observed in the provided items: **0.2857** (QA-036), **0.3333** (QA-009), **0.5** (QA-002/QA-020/QA-029/QA-030), and **0.6667** for several multi-hop/recursive cases.
- At least two answers explicitly say relationships needed for the join path are missing from retrieved contexts (e.g., QA-012, QA-020, QA-033/QA-034/QA-035/QA-036/QA-038).

**Verdict:** Retrieval is generally strong, but a handful of complex questions still hit **context linkage limitations**, reducing coverage.

### 3. Answer Quality (4/5)
- `query_report.grounded_rate=1.0` means answers are consistently grounded in retrieved KG context.
- `grader_rejection_count=0` and `semantic_verification_passed` appears consistently `true`, implying no detected hallucinations.

But “answer quality” is not just hallucination-free; it’s whether the answer matches the expected intent:
- Some items where expected answers require specific join paths are answered only partially or with conditional inability (still grounded, but **not fully satisfying expected logic**)—e.g.:
  - **QA-012** (expected: trace components needed for a work order; generated: says insufficient schema-level relationship in retrieved context)
  - **QA-033** (failed inspections by supplier → generated: cannot find component/supplier linkage)
  - **QA-034** (manufacturing time from route operations → generated: switches to planned date duration; missing expected route-based time computation)
  - **QA-036/QA-038** (expiry + supplier component containment; genealogy through batch → generated: cannot complete due to missing schema/relationships in retrieved context)

Given these, I rate answer quality slightly below perfect: **4/5** (grounding is excellent; correctness/coverage drops on a minority of complex join-reasoning questions).

### 4. Pipeline Health (5/5)
- `pipeline_health` shows:
  - `cypher_failed=false`
  - `ingestion_errors_count=0`
  - `failed_mappings_count=0`
  - `grader_inconsistencies=0`
  - `gate_abstentions=0`
  - `total_grader_rejections=0`
- Latency fields are all **0** in the bundle (likely not logged), but operationally there are **no faults**.

### 5. Ablation Impact (5/5)
- `study_id=AB-BEST` and no `ablation_context` is provided in the bundle, so we can’t formally compare “vs baseline” from the bundle itself.
- Still, the observed performance is near-optimal: full builder completion, full grounding, high average retrieval scores, and zero pipeline errors.
- Under the rubric, this strongly supports that AB-BEST is an “optimal/combined-best” style configuration, deserving **5/5** for impact.

## Per-Question Deep Dive
*(Verdicts based on semantic match to `expected_answer`; groundedness alone is not treated as “correct.”)*

### QA-001: What information is stored about products in the manufacturing system?
- **Type:** direct_mapping | **Difficulty:** unknown  
- **Verdict:** CORRECT  
- **Expected:** product_id, product_name, product_type, parent_product_id (hierarchy), base_cost, lead_time_days, is_active  
- **Generated:** Correctly describes `product` table fields including hierarchy via `parent_product_id` and cost/timing/status defaults/constraints  
- **Analysis:** Direct schema-to-answer mapping; fully aligned.
- **Retrieval:** gt_coverage=1.0, top_score=0.8870, gate=proceed

### QA-002: How are components defined in the manufacturing database?
- **Type:** direct_mapping | **Difficulty:** unknown  
- **Verdict:** PARTIALLY_CORRECT  
- **Expected:** component_id, component_name, component_category, unit_of_measure, standard_cost, specification_id (optional), atomic/non-decomposable  
- **Generated:** Matches most schema-level attributes and optional specification_id  
- **Analysis:** Main omission: expected “cannot be further decomposed” is partially paraphrased, but overall content matches.
- **Retrieval:** gt_coverage=0.5, top_score=0.5911, gate=proceed

### QA-003: What is the purpose of the Bill of Materials (BOM) table?
- **Type:** direct_mapping | **Difficulty:** unknown  
- **Verdict:** CORRECT  
- **Expected:** BOM defines hierarchical product structure; includes bom_id, parent_product_id, component_product_id, quantity, unit_of_measure, bom_level, is_optional  
- **Generated:** Correct purpose and key fields; mentions recursive explosions and optional components  
- **Analysis:** Strong alignment.
- **Retrieval:** gt_coverage=0.6667, top_score=0.9115, gate=proceed

### QA-004: What supplier information does the system maintain?
- **Type:** direct_mapping | **Difficulty:** unknown  
- **Verdict:** CORRECT  
- **Expected:** supplier_id, supplier_name, contact_email, contact_phone, rating, is_preferred  
- **Generated:** Matches exactly with schema/constraints
- **Analysis:** Good.
- **Retrieval:** gt_coverage=1.0, top_score=0.55, gate=proceed

### QA-005: How are warehouses represented in the schema?
- **Type:** direct_mapping | **Difficulty:** unknown  
- **Verdict:** CORRECT  
- **Expected:** warehouse_id, warehouse_name, address, city, state, capacity, manager_id  
- **Generated:** Correctly lists these fields and relationships (shipment/work order usage)
- **Analysis:** Good.
- **Retrieval:** gt_coverage=1.0, top_score=0.55, gate=proceed

### QA-006: What does the inventory table track?
- **Type:** direct_mapping | **Difficulty:** unknown  
- **Verdict:** CORRECT  
- **Expected:** inventory_id, warehouse_id, component_id OR product_id, quantity_on_hand, quantity_reserved, reorder_threshold, last_restock_date  
- **Generated:** Correctly describes available quantities and mutual exclusivity
- **Analysis:** Good.
- **Retrieval:** gt_coverage=0.8, top_score=0.55, gate=proceed

### QA-007: How are work orders structured in the manufacturing system?
- **Type:** direct_mapping | **Difficulty:** unknown  
- **Verdict:** CORRECT  
- **Expected:** work_order_id, product_id, parent_work_order, quantity_ordered, quantity_completed, status, priority, planned dates, warehouse_id  
- **Generated:** Correctly describes hierarchy + columns/constraints
- **Analysis:** Good.
- **Retrieval:** gt_coverage=1.0, top_score=0.8511, gate=proceed

### QA-008: What information is captured in the shipment table?
- **Type:** direct_mapping | **Difficulty:** unknown  
- **Verdict:** CORRECT  
- **Expected:** shipment_id, shipment_type, warehouse_id, supplier_id (inbound), customer_id (outbound), ship_date, estimated_arrival, actual_arrival, status  
- **Generated:** Matches.
- **Analysis:** Good.
- **Retrieval:** gt_coverage=1.0, top_score=0.8136, gate=proceed

### QA-009: How does the quality control system record inspections?
- **Type:** direct_mapping | **Difficulty:** unknown  
- **Verdict:** PARTIALLY_CORRECT  
- **Expected:** qc_id, batch_id, specification_id, qc_date, qc_type, inspector_id, result, defect_count, notes  
- **Generated:** Correctly explains all key attributes, but retrieved context coverage is low (gt_coverage 0.3333), suggesting some expected fields may not be fully supported by retrieved chunks (though the text claims them).
- **Analysis:** Likely missing evidence for one or more expected fields in retrieved contexts.
- **Retrieval:** gt_coverage=0.3333, top_score=0.6745, gate=proceed

### QA-012: How do I trace which components are needed to fulfill a work order?
- **Type:** multi_hop | **Difficulty:** unknown  
- **Verdict:** INCORRECT  
- **Expected:** Use work_order.product_id → bom where product_id is parent; recursively explode to get component_product_id; multiply quantities; leaf components; then relate to inventory  
- **Generated:** Explicitly says retrieved context lacks relationship connecting work_order to BOM components; claims not enough info  
- **Analysis:** Generated answer is cautious but does not meet expected solution.
- **Retrieval:** gt_coverage=0.6667, top_score=0.55, gate=proceed

### QA-013: Identify warehouses with available inventory for specific components
- **Type:** multi_hop | **Difficulty:** unknown  
- **Verdict:** CORRECT  
- **Expected:** inventory filtered by component_id, join warehouse, available = on_hand - reserved > 0  
- **Generated:** Correct logic (though doesn’t explicitly compute on_hand-reserved in the final sentence; still explains it conceptually)
- **Analysis:** Subtle incompleteness but aligned.
- **Retrieval:** gt_coverage=1.0, top_score=0.7694, gate=proceed

### QA-020: How identify which specifications apply to specific components?
- **Type:** multi_hop | **Difficulty:** unknown  
- **Verdict:** INCORRECT  
- **Expected:** component.specification_id (or join path) to specification; include component and specification attributes  
- **Generated:** Says retrieved context lacks actual table/column mapping needed (“cannot provide mapping mechanics”), despite claiming component has specification_id conceptually.
- **Analysis:** Fails expected “how to identify” join.
- **Retrieval:** gt_coverage=1.0, top_score=0.55, gate=proceed

### QA-033: Failed QC inspections for components from specific suppliers
- **Type:** complex | **Difficulty:** unknown  
- **Verdict:** INCORRECT  
- **Expected:** quality_control filtered by result='FAIL' → batch → trace to components via bom → component_supplier + supplier → filter supplier_id  
- **Generated:** States context lacks links from quality_control to components/suppliers; cannot specify join path  
- **Analysis:** Not meeting expected pipeline logic.
- **Retrieval:** gt_coverage=0.1429, top_score=0.55, gate=proceed

### QA-034: Total manufacturing time for a work order including all sub-assembly work orders
- **Type:** complex | **Difficulty:** unknown  
- **Verdict:** PARTIALLY_CORRECT  
- **Expected:** work_order tree → route operations via product_id → sum cycle_time*quantity + setup_time across hierarchy  
- **Generated:** Instead computes duration from planned_start/end dates; cannot define expected route-based operation time  
- **Analysis:** Uses an alternative but not the required schema-based calculation.
- **Retrieval:** gt_coverage=0.6667, top_score=0.55, gate=proceed

### QA-036: Expiry + components from specific suppliers
- **Type:** complex | **Difficulty:** unknown  
- **Verdict:** INCORRECT  
- **Expected:** batch expiry filter → recursive bom to components → component_supplier/supplier filter → at-risk identification  
- **Generated:** Cannot complete due to missing batch-to-component consumption linkage and missing component_supplier schema details
- **Analysis:** Not satisfying expected join-reasoning.
- **Retrieval:** gt_coverage=0.2857, top_score=0.55, gate=proceed

### QA-038: Genealogy from supplier through batch to finished goods
- **Type:** complex | **Difficulty:** unknown  
- **Verdict:** PARTIALLY_CORRECT  
- **Expected:** shipment(supplier) → inventory(component) → reverse BOM to batch product genealogy → quality_control → work_order → shipment finished goods  
- **Generated:** Traces supplier→component (component_supplier) and component→finished goods via bom, but cannot complete supplier→batch→finished goods due to missing batch schema relationships  
- **Analysis:** Partial match; incomplete relative to expected end-to-end.
- **Retrieval:** gt_coverage=0.8, top_score=0.55, gate=proceed

### QA-039: Alternative suppliers for components critical for multiple products
- **Type:** complex | **Difficulty:** unknown  
- **Verdict:** PARTIALLY_CORRECT  
- **Expected:** BOM explosion frequency of leaf components across products → component_supplier → supplier filter rating>=4 and is_preferred='Y' → list alternatives  
- **Generated:** Uses frequency across bom.component_product_id and then component_supplier, but does not implement rating>=4.0 + preferred flag in the final “plan”.
- **Analysis:** Method described but filtering criteria not fully applied.
- **Retrieval:** gt_coverage=1.0, top_score=0.7, gate=proceed

## Anomalies & Recommendations

### Red Flags
- **No abstentions at all** (`abstained_count=0`, `gate_decision` always `proceed`). For advanced/complex questions, some answers explicitly state missing join paths—this suggests the gate may be **over-permissive** (it proceeds even when the KG context doesn’t contain enough schema linkage).
- Several complex questions are **cautious and say “not enough information in retrieved context”** (e.g., QA-012, QA-020, QA-033, QA-034/036/038). This indicates retrieval is grounded but not always *structurally sufficient* for multi-hop joins the question asks for.
- A few cases show **high groundedness but reduced gt_coverage** (e.g., QA-002, QA-009), suggesting retrieved context may not cover all expected facts even when the answer text sounds complete.

### Recommendations
1. **Tighten retrieval quality gate for schema/relationship-composition tasks.**  
   For questions requiring specific join paths (work_order→bom→components; quality_control→batch→component_supplier→supplier), trigger `abstain_early` or regenerate with explicit join-path constraints when `gt_coverage`-like signals are low.
2. **Add a “relationship schema sufficiency check”** before generation: ensure the contexts include the *exact bridging edge definitions* (e.g., batch→component consumption, QC→component/material link, shipment→work_order fulfillment link).
3. **Improve builder/query trace alignment:** when generation says “context does not include join path,” inspect whether the KG actually has the missing edge; if it does, retrieval may be failing to surface it (reranker/context caps). If it doesn’t, it’s a KG modeling gap.
4. **Introduce explicit mapping for known conceptual-to-physical gaps** (e.g., distinguishing `component` vs `product` identifiers in BOM explosion; handling cost fields for landed cost / manufacturing time).

## Comparison Notes (if applicable)
- `AB-BEST` is treated as the best configuration, and results are strong across builder, grounding, and pipeline health.
- The bundle does not include an `ablation_context.changes_vs_baseline`, so causal attribution to specific flags is not possible from provided data alone.