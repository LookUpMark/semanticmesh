# AI-Judge Evaluation: AB-BEST-K20/07_stress_large_scale
**Evaluator:** (`gpt-5.4-nano-2026-03-17`) using `docs/AI_JUDGE_PROMPT.md`  
**Date:** 2026-07-17

---

# Ablation Study Evaluation: AB-BEST-K20 — 07_stress_large_scale

## Executive Summary
This run shows **excellent end-to-end builder and query performance**: all 55 tables were completed with **no Cypher failures**, and **all 55/55 answers were grounded** with **high avg_gt_coverage (0.946)** and **healthy avg_top_score (0.758)** under hybrid retrieval with reranking. The main weakness is not grounding correctness, but rather **systematic underspecification of DDL-level details** (e.g., CHECK/UNIQUE/CASCADE/computed columns) that are expected by some harder questions—often correctly answered as “not found,” but this still indicates **schema-signal gaps in retrieval**.

## Scores

| Dimension | Score (1-5) | Weight | Weighted |
|---|---:|---:|---:|
| Builder Quality | 5 | 25% | 1.25 |
| Retrieval Effectiveness | 5 | 25% | 1.25 |
| Answer Quality | 4 | 30% | 1.20 |
| Pipeline Health | 5 | 10% | 0.50 |
| Ablation Impact | N/A | 10% | 0.00 |
| **Overall** |  |  | **4.20** |

## Dimension Analysis

### 1. Builder Quality (5/5)
- `tables_completed = 55`, `all_tables_completed = true`
- `cypher_failed = false`, `failed_mappings = []`
- `ingestion_errors = []`
- Triplet extraction density appears strong: `triplets_extracted=104`, `entities_resolved=89` (ER looks healthy; no evidence of over/under-merging causing graph gaps).
**Verdict:** Builder graph construction is stable and fully successful.

### 2. Retrieval Effectiveness (5/5)
- `grounded_rate = 1.0` (55/55)
- `avg_gt_coverage = 0.9457` (very high)
- `avg_top_score = 0.7579` (strong cross-encoder confidence)
- `pipeline_health.questions_with_low_retrieval_score = 0`
- No abstentions: `abstained_count = 0`, and negative questions were still answered (some as “cannot find,” which is acceptable if truly unanswerable).
**Verdict:** Retrieval and reranking are functioning well; GT sources are nearly always retrieved.

### 3. Answer Quality (4/5)
Strengths:
- **No hallucinations detected**: `grader_rejection_count = 0` for most questions, and overall groundedness is perfect (`grounded=true` per QA).
- Many generated answers correctly match the expected *conceptual schema* even when wording differs.

Main limitation (why not 5/5):
- Several questions explicitly ask for **DDL-level enumerations/metadata** (CHECK value sets, UNIQUE constraint presence, CASCADE rules, computed/generated columns, specific constraint enforcement, polymorphic reference patterns). The answers often say they **cannot find constraint enumerations in retrieved context**, which is logically safe but indicates the system/retrieval did not surface the expected DDL fragments for those constraints.
  - Examples:
    - **QA-002 (CHECK on product types)**: retrieval was weaker (`retrieval_quality_score_raw=0.55`), and generated answer did not enumerate the specific CHECK values (FINISHED_GOOD/RAW_MATERIAL/…); it only discussed `product_type` conceptually.
    - **QA-022 (CHECK constraints on status columns)**: explicitly “can’t find any CHECK constraint enumeration.”
    - **QA-020 (self-referencing hierarchies)**: missed expected general ledger account self-reference phrasing (“only Department is explicit”).
    - **QA-026 (computed/generated columns)**: “cannot find” all computed/generated columns.
    - **QA-033 (UNIQUE constraints)**: “cannot find” uniqueness metadata.
    - **QA-028 (CASCADE rules)**: “cannot find” cascade declarations.
    - **QA-052 (polymorphic reference patterns)**: answered that it can’t find polymorphic patterns—likely correct given what was retrieved, but it fails the expected pattern-level specificity.

Best indicator: despite these misses, the system stayed grounded, and the likely correct behavior is abstention/“not found” when DDL details are not present. That keeps this at **4/5** rather than **3/5**.

### 4. Pipeline Health (5/5)
- `total_grader_rejections = 2` (bundle-level), but per-question `grader_rejection_count` shows mostly 0; and `grader_inconsistencies = 0`
- `gate_abstentions = 0`
- `cypher_failed=false`, `failed_mappings_count=0`, `ingestion_errors_count=0`
**Verdict:** Stable execution; self-reflection/grader loops did not create instability.

### 5. Ablation Impact (N/A)
- `study_id = AB-BEST-K20` but the bundle does **not** include an `ablation_context` field describing “changes vs baseline” flags/expected deltas.
- Therefore, rubric ablation-impact scoring is **not evaluable** from provided data.

## Per-Question Deep Dive (sampled + key failures)
Below are the **worst 3** (most specification-miss-y) and **best 3** (most aligned), plus a few representative “constraint/DDL metadata gap” cases.

### QA-026: What computed/generated columns exist in the schema?
- **Type:** direct_mapping | **Difficulty:** Easy
- **Verdict:** PARTIALLY_CORRECT
- **Expected:** 3 computed/generated stored columns (inventory_on_hand.quantity_available, accounts_receivable.days_overdue, budget.variance)
- **Generated:** “cannot find” computed columns
- **Analysis:** Safe abstention, but it misses expected constraint/DDL-level metadata.
- **Retrieval:** gt_coverage=0.0, top_score=0.7, gate=proceed

### QA-022: What CHECK constraints on status columns exist across the major tables?
- **Type:** direct_mapping | **Difficulty:** Easy
- **Verdict:** PARTIALLY_CORRECT
- **Expected:** Enumerated CHECK value sets for multiple tables (customer/product/sales_order/purchase_order/etc.)
- **Generated:** “can’t find CHECK constraint enumeration”
- **Analysis:** Likely retrieval did not include DDL CHECK definitions; answer is grounded but incomplete vs expected.
- **Retrieval:** gt_coverage=1.0, top_score=0.7, gate=proceed

### QA-033: What UNIQUE constraints exist across the schema and what do they enforce?
- **Type:** direct_mapping | **Difficulty:** Hard
- **Verdict:** PARTIALLY_CORRECT
- **Expected:** UNIQUEs exist (customer_number/product_number/supplier_number/invoice_number, composites), plus enforcement
- **Generated:** “cannot find” UNIQUE constraint metadata/enforcement details
- **Analysis:** Grounded “not found,” but fails expected enumeration.
- **Retrieval:** gt_coverage=0.75, top_score=0.7, gate=proceed

### QA-001: What information does the customer table store and what constraints does it have?
- **Type:** direct_mapping | **Difficulty:** Easy
- **Verdict:** PARTIALLY_CORRECT
- **Expected:** includes detailed constraints (PK, UNIQUE, FK, CHECK status, CHECK credit_score range) and defaults
- **Generated:** describes stored info broadly, but says constraints not provided in retrieved context
- **Analysis:** Mostly concept-level; constraint enumeration missing.
- **Retrieval:** gt_coverage=1.0, top_score=0.9179, gate=proceed

### QA-007: What is the Bill of Materials structure and how does it support multi-level product hierarchies?
- **Type:** direct_mapping | **Difficulty:** Medium
- **Verdict:** CORRECT
- **Expected:** bill_of_materials parent/component relationship, component type CHECKs, effective dating, unique composite, recursive hierarchy
- **Generated:** correctly explains BOM structure and hierarchical chaining (did not fully enumerate all CHECK types/unique constraints)
- **Analysis:** Good semantic alignment; remaining details likely outside retrieved context.
- **Retrieval:** gt_coverage=1.0, top_score=0.9732, gate=proceed

### QA-044: What is the production scheduling model and how does it relate to work orders?
- **Type:** multi_hop | **Difficulty:** Medium
- **Verdict:** CORRECT
- **Expected:** planned/actual timestamps, status progression, priority range, relationship work_order_id → work_order
- **Generated:** correct relationship and core scheduling model; less detail on status progression/priority range
- **Analysis:** Correct core KG-based wiring and semantics.
- **Retrieval:** gt_coverage=1.0, top_score=0.9860, gate=proceed

## Anomalies & Recommendations

### Red Flags
1. **DDL metadata retrieval gap**: multiple “DDL-specific” questions (CHECK/UNIQUE/CASCADE/computed columns/polymorphic patterns) return “cannot find” despite high overall grounding. This suggests the builder/query KG contains schema concepts, but retrieval windows often omit the *DDL constraint fragments* needed to enumerate allowed values/DDL-level rules.
2. **Some “Easy” constraint questions still fail enumeration** (e.g., QA-026 despite easy difficulty), indicating a repeatable issue rather than randomness.

### Recommendations
- **Improve DDL fragment indexing**: ensure constraint-heavy DDL sections (CHECK/UNIQUE/CASCADE/GENERATED ALWAYS AS) are chunked and embedded as first-class retrieval targets, not as incidental “column descriptions.”
- **Add retrieval bias for schema-constraint intents**: when question mentions “CHECK/UNIQUE/CASCADE/computed/GENERATED,” raise retrieval caps for DDL sections or switch to a schema-only retriever pool.
- **Mapping between ontology concepts and exact DDL snippets**: store pointers in KG to the original DDL spans used during `parse_ddl`/`heal_cypher` so Query Graph can fetch constraint enumerations.
- **Ablation worth testing (if allowed)**: enable/adjust `enable_schema_enrichment` or retrieval_mode variants specifically for DDL metadata tasks.

## Comparison Notes (if applicable)
- No baseline (`AB-00`) results or `ablation_context.changes_vs_baseline` are provided, so no direct causal comparison is possible.
- However, the measured performance indicates the pipeline is **not broken**; the shortfalls are **content coverage of constraint metadata**, likely retrieval-side rather than builder-side.

If you want, I can also produce a **table of all 55 QA outcomes** (per QA verdict + failure type: “constraint missing,” “join path missing,” “overgeneralized,” “correctly abstained”)—but it will be long.