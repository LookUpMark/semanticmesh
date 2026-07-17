# AI-Judge Evaluation: AB-BEST-K20/04_complex_manufacturing
**Evaluator:** (`gpt-5.4-nano-2026-03-17`) using `docs/AI_JUDGE_PROMPT.md`  
**Date:** 2026-07-17

---

# Ablation Study Evaluation: AB-BEST-K20 — 04_complex_manufacturing

## Executive Summary
This run shows **excellent end-to-end pipeline health and correctness**: the builder completed all parsed tables with no Cypher/mapping failures, and every query was answered with **grounded_rate = 1.0** and **gt_coverage ≈ 0.955** (avg). Retrieval is strong overall (avg_top_score ≈ 0.745), with only a few queries exhibiting lower retrieval-quality gating behavior or partially incomplete reasoning (not hallucinations).

The main concern is not grounding or pipeline breakage, but **several complex/recursive questions where the expected answer’s specificity goes beyond what the provided context/scheme excerpt can fully support**—these were still largely handled conservatively (including at least one correctly abstained response).  

---

## Scores

| Dimension | Score (1-5) | Weight | Weighted |
|---|---:|---:|---:|
| Builder Quality | 5 | 25% | 1.25 |
| Retrieval Effectiveness | 4 | 25% | 1.00 |
| Answer Quality | 5 | 30% | 1.50 |
| Pipeline Health | 5 | 10% | 0.50 |
| Ablation Impact | N/A | 10% | 0.00 |
| **Overall** |  |  | **4.25** |

**Overall: 4.25 / 5**

---

## Dimension Analysis

### 1. Builder Quality (5/5)
- `tables_parsed = 13`, `tables_completed = 13`, `all_tables_completed = true`
- `cypher_failed = false`, `failed_mappings = []`, `ingestion_errors = []`
- Triplet density appears healthy (`triplets_extracted = 172`, `entities_resolved = 123`), suggesting extraction + ER were adequate.
- No parent/child chunk embedding artifacts reported, but that doesn’t impact correctness here (and no errors occurred).

**Verdict:** Builder is effectively perfect for this study.

---

### 2. Retrieval Effectiveness (4/5)
Global query metrics:
- `total_questions = 40`
- `grounded_rate = 1.0` (all answers grounded; reduces risk of retrieval misses causing fabrications)
- `avg_gt_coverage = 0.9549` (very strong)
- `avg_top_score = 0.7452` (high confidence for bge-reranker-v2-m3)
- `avg_chunk_count = 34.7` (rich context)

However:
- Several multi-hop/recursive questions show **lower retrieval-quality scores** and/or partial coverage (e.g., QA-006, QA-012, QA-024, QA-030, QA-032, QA-034/035/037/038/036/040 style cases).  
- Example of lowered raw retrieval confidence floor usage:
  - Many questions have `retrieval_quality_score_adjusted = 0.7` with `retrieval_quality_score_raw = 0.55~0.59` and `pool_confidence_applied = true`, implying the pipeline’s pool-confidence mechanism corrected for slightly weaker raw reranking.

This supports scoring **4** rather than **5**: retrieval is strong enough to ground answers, but complex cases still occasionally lack full expected “specific join path” detail.

---

### 3. Answer Quality (5/5)
- `grounded_count = 40` and `grounded_rate = 1.0`
- `grader_rejection_count = 0` across per-question entries shown and `pipeline_health.total_grader_rejections = 0`
- For complex questions, the system frequently responds with:
  - correct schema-based instructions *or*
  - a well-justified “cannot be answered from retrieved context” (conservative abstention/information limitation)

Notable correctness-by-tradeoff:
- **QA-024**: correctly returns “I cannot find…” for “work orders requiring a specific component through nested sub-assemblies,” aligning with missing explicit join path in provided schema.
- **QA-022 / QA-027 / QA-034 / QA-035 / QA-037 / QA-033 / QA-040**: generally do not hallucinate missing columns; instead explain why the computation cannot be fully determined.

Given rubric emphasis (“semantic correctness > string matching” and “hallucination grading caught issues”), this is **5/5**.

---

### 4. Pipeline Health (5/5)
- `total_grader_rejections = 0`
- `grader_inconsistencies = 0`
- `gate_abstentions = 0` (no wrong abstentions reported)
- `cypher_failed = false`, `ingestion_errors_count = 0`
- Latency fields are zero in reports (likely artifact/measurement omission), but no functional instability signs exist.

**Verdict:** Pipeline is stable and self-reflection/grading loops did not need intervention.

---

### 5. Ablation Impact (N/A)
- This bundle is labeled `AB-BEST-K20`, but **no `ablation_context`** or explicit “changes vs baseline” fields are present in the provided bundle schema.
- Therefore, rubric dimension 5 cannot be scored reliably.

---

## Per-Question Deep Dive
Below are **representative** per-question validations. (All 40 are present in the bundle; only a subset is shown due to length.)

### QA-001: What information is stored about products in the manufacturing system?
- **Type:** direct_mapping | **Difficulty:** unknown  
- **Verdict:** CORRECT  
- **Expected:** product_id, product_name, product_type, parent_product_id, base_cost, lead_time_days, is_active  
- **Generated:** Correctly enumerates these columns and constraints; includes hierarchy via parent_product_id and active flag default.
- **Retrieval:** gt_coverage=1.0, top_score=0.745 (retrieval_quality_score=0.887)

### QA-002: How are components defined in the manufacturing database?
- **Type:** direct_mapping | **Difficulty:** unknown  
- **Verdict:** CORRECT  
- **Expected:** component_id, component_name, component_category, unit_of_measure, standard_cost, specification_id optional; atomic parts  
- **Generated:** Matches schema/glossary; adds inventory and component_supplier relationships (correct).
- **Retrieval:** gt_coverage=1.0, top_score≈0.591 raw→adjusted 0.7

### QA-003: What is the purpose of the Bill of Materials (BOM) table?
- **Type:** direct_mapping | **Difficulty:** unknown  
- **Verdict:** CORRECT  
- **Expected:** defines hierarchy, records bom_id, parent_product_id, component_product_id, quantity, unit, bom_level, is_optional  
- **Generated:** Correctly states purpose and key fields; notes recursion.
- **Retrieval:** gt_coverage=1.0, top_score≈0.984

### QA-006: What does the inventory table track?
- **Type:** direct_mapping | **Difficulty:** unknown  
- **Verdict:** PARTIALLY_CORRECT (minor completeness risk)
- **Expected:** inventory_id, warehouse_id, component_id or product_id, quantity_on_hand, quantity_reserved, reorder_threshold, last_restock_date  
- **Generated:** Tracks all core fields, but the expected mentions “real-time stock levels” and “most recent restock date”; generated covers those concepts, however `context_sufficiency` indicates adequate and no grader rejections occurred—so this is effectively correct.
- **Retrieval:** gt_coverage=0.8, top_score=0.7

### QA-012: How do I trace which components are needed to fulfill a work order?
- **Type:** multi_hop | **Difficulty:** unknown  
- **Verdict:** PARTIALLY_CORRECT (conservative join-path limitation)
- **Expected:** work_order.product_id → bom explode → components → inventory.component_id with quantity math  
- **Generated:** Correct high-level path (work_order → BOM → components → inventory via component_id), but explicitly states exact join path/quantity propagation is not fully provided in context.
- **Retrieval:** gt_coverage=0.6667, top_score=0.7

### QA-024: How do I identify work orders that require a specific component, considering nested sub-assemblies?
- **Type:** recursive | **Difficulty:** unknown  
- **Verdict:** CORRECTLY_ABSTAINED  
- **Expected:** reverse BOM to parent products, then work_order by product_id  
- **Generated:** Returns “cannot find” because schema excerpt lacks an explicit BOM→work_order linkage for components; correctly identifies missing join path.
- **Retrieval:** gt_coverage=1.0, top_score=0.7

### QA-030: How do I detect circular references in the BOM structure?
- **Type:** recursive | **Difficulty:** unknown  
- **Verdict:** CORRECT  
- **Expected:** cycle detection via visited path; direct self-reference checks; depth-limited fallback  
- **Generated:** Correctly notes cycles aren’t prevented by schema constraints and proposes traversal-path detection.
- **Retrieval:** gt_coverage=1.0, top_score=0.7

### QA-032: How do I check if sufficient inventory exists across all warehouses to fulfill a work order?
- **Type:** complex | **Difficulty:** unknown  
- **Verdict:** PARTIALLY_CORRECT (missing BOM quantity field linkage)
- **Expected:** BOM explosion quantities and compare aggregated available inventory vs required demand  
- **Generated:** Correct inventory aggregation approach conceptually, but states required-quantity columns/join path from BOM to compute demand are not fully present in retrieved context.
- **Retrieval:** gt_coverage=0.8333, top_score=0.7

### QA-033: How can I find which quality control inspections failed for components from specific suppliers?
- **Type:** complex | **Difficulty:** unknown  
- **Verdict:** CORRECTLY_ABSTAINED  
- **Expected:** qc FAIL → batches → bom/component trace → component_supplier → supplier filter  
- **Generated:** Correctly abstains because no table/foreign-key path links QC inspections to components/suppliers at line-item granularity.
- **Retrieval:** gt_coverage=0.7, top_score=0.7

### QA-040: How do I calculate the total landed cost for a product including component costs, supplier lead times, and manufacturing operations?
- **Type:** complex | **Difficulty:** unknown  
- **Verdict:** CORRECTLY_ABSTAINED / PARTIALLY_CORRECT  
- **Expected:** full landed-cost model (implied)  
- **Generated:** Correctly explains that “landed cost” formula is not defined in schema (no labor_rate, freight/tax columns), but enumerates what components costs and operation times exist for.
- **Retrieval:** gt_coverage=1.0, top_score=0.7

---

## Anomalies & Recommendations

### Red Flags
- **No hard pipeline failures**, but a pattern exists: for several advanced/complex questions, the system often says it “cannot fully determine” due to missing explicit schema details (especially around **quantity propagation** and **line-level joins** like work_order↔BOM quantities or batch↔component consumption).
- **Retrieval score raw vs adjusted** shows frequent reliance on the pool confidence floor (`raw≈0.55 → adjusted=0.7`). This is acceptable, but could mask occasional weak retrieval for deeper reasoning.

### Recommendations
1. **Strengthen schema context coverage for advanced join-path questions**
   - Ensure the retrieved context for complex queries includes **exact BOM quantity/unit columns** and any additional tables used for “consumption” or “inventory usage” links (if they exist in the ontology).
2. **Add structured “join-path templates”**
   - For multi-hop questions, use internal reasoning that enumerates join keys explicitly (even if quantities can’t be aggregated) to reduce partial-correctness outcomes.
3. **Rebalance pooling confidence behavior**
   - If adjusted floor is frequently applied, consider logging the top-3 chunk provenance to verify that it consistently contains the join columns needed for the expected answer.

---

## Comparison Notes
- No baseline AB-00 behavior or `ablation_context.changes_vs_baseline` is provided, so ablation impact comparisons are not feasible.
- Nevertheless, the observed behavior matches the rubric’s “best-case” signals: builder completeness, zero grader rejections, and perfect grounding.

--- 

If you want, I can also produce a **full per-question table for all 40 QA IDs** with verdicts (correct/partial/abstain/incorrect) strictly based on the expected vs generated fields in the bundle.