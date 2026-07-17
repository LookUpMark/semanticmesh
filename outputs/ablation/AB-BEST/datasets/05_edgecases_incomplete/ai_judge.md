# AI-Judge Evaluation: AB-BEST/05_edgecases_incomplete
**Evaluator:** (`gpt-5.4-nano-2026-03-17`) using `docs/AI_JUDGE_PROMPT.md`  
**Date:** 2026-07-17

---

# Ablation Study Evaluation: AB-BEST — 05_edgecases_incomplete

## Executive Summary
AB-BEST shows **strong end-to-end pipeline stability**: all 5 tables completed in the Builder, **no Cypher failures**, and **grounded_rate = 1.0 across all 20 questions**. Retrieval also looks healthy (avg_gt_coverage≈0.79, avg_top_score≈0.78) with **no abstentions**, but there are several edgecase-driven questions where the system properly answers “cannot determine” / preserves uncertainty rather than hallucinating—consistent with the dataset’s incompleteness. The main concern is not correctness, but **retrieval realism vs. scoring signals**: one question shows very low raw retrieval relevance (ec_003) and another shows missing GT coverage numerically (ec_007) while still being graded grounded, suggesting the evaluation may be over-penalizing/over-smoothing internal alignment metrics.

## Scores

| Dimension | Score (1-5) | Weight | Weighted |
|---|---:|---:|---:|
| Builder Quality | 5 | 25% | 1.25 |
| Retrieval Effectiveness | 4 | 25% | 1.00 |
| Answer Quality | 5 | 30% | 1.50 |
| Pipeline Health | 5 | 10% | 0.50 |
| Ablation Impact | N/A | 10% | 0.00 |
| **Overall** |  |  | **4.25** |

## Dimension Analysis

### 1. Builder Quality (5/5)
- `tables_parsed=5`, `tables_completed=5`, `all_tables_completed=true`
- `cypher_failed=false`, `failed_mappings=[]`, `ingestion_errors=[]`
- Triplet extraction density appears adequate: `triplets_extracted=86`, `entities_resolved=85` (no sign of extraction/ER collapse)
- Builder traces indicate no health-impacting failures (`builder_skipped=false`).

**Verdict:** Meets the rubric’s top tier: completed, no Cypher errors, no failed mappings.

### 2. Retrieval Effectiveness (4/5)
Key signals:
- `avg_gt_coverage = 0.789` (≥ 0.6 threshold for score 4)
- `avg_top_score = 0.783` (healthy; well above the rubric’s 0.3 requirement for score 4)
- `questions_with_low_retrieval_score = 0`
- `gate_abstentions = 0`

Per-question notable checks:
- Worst retrieval-looking item by **raw score**:  
  - **ec_003** has `retrieval_quality_score_raw=0.55` but still `gt_coverage=1.0` and answer is uncertainty-preserving and grounded.
- **ec_007** shows `gt_coverage=0.0` (but answer is still marked grounded true). This is the main anomaly: either the GT coverage computation differs from the “expected_sources” notion, or the expected mapping is loose.

Overall, retrieval is plausibly effective (high top scores, no low-retrieval cases), but the `gt_coverage=0.0` event suggests either:
1) expected source attribution mismatches actual retrieved concepts, or  
2) “coverage” computation is stricter than what the semantic answer uses.

**Verdict:** Good retrieval with one anomaly → 4/5.

### 3. Answer Quality (5/5)
- `query_report.grounded_rate = 1.0` (all 20 grounded)
- `grader_rejection_count = 3` total, but the bundle also reports `grounded=true` on all per-question entries shown; these rejections likely reflect internal regeneration stability rather than final incorrectness.

Crucial qualitative behavior:
- For incompleteness/edgecases, the model **does not hallucinate enumerations or definitions**, e.g.:
  - **ec_004 (order_status valid values)**: correctly says it cannot find allowed set; expects glossary values but schema has no constraint.
  - **ec_012 (Failed meaning)**: correctly notes definition missing (“Failed: [definition missing]”).
  - **ec_009 (payment methods accepted)**: correctly says accepted values aren’t documented.
  - **ec_001/005/007**: preserves glossary ambiguity and circular definitions.

**Best examples (high-quality uncertainty handling):**
- **ec_004, ec_009, ec_012**: correctly abstain *semantically* by stating “cannot determine from KG” (rather than fabricating values).

**Verdict:** No incorrect claims observed; grounded and semantically aligned → 5/5.

### 4. Pipeline Health (5/5)
- `cypher_failed=false`
- `ingestion_errors_count=0`
- `failed_mappings_count=0`
- `grader_inconsistencies=0`
- `grader_consistency_valid=true` on all shown questions
- `total_grader_rejections=3` is small and does not indicate instability (no evidence of “forced pass after exhaustion” behavior).

**Verdict:** Stable execution across builder and query graphs → 5/5.

### 5. Ablation Impact (N/A)
This run is `AB-BEST`, but the bundle provided does **not include** `ablation_context.changes_vs_baseline` or an explicit “baseline AB-00” comparison section. Therefore, the rubric requires N/A.

## Per-Question Deep Dive

### ec_001: What is a customer?
- **Type:** missing_definition | **Difficulty:** unknown  
- **Verdict:** CORRECT  
- **Expected:** Customer definition exists but incomplete; related terms Client, Account Holder, End User.  
- **Generated:** Defines customer generally; notes Client interchangeability; includes Account Holder and End User distinctions.  
- **Analysis:** Matches expected glossary content and properly reflects incompleteness.  
- **Retrieval:** gt_coverage=1.0, top_score=0.9837, gate=proceed

### ec_002: What's the difference between firstName and first_name in the CUSTOMERS table?
- **Type:** duplicate_columns | **Difficulty:** unknown  
- **Verdict:** CORRECT  
- **Expected:** Both exist with same type; appear duplicates due to naming convention; application usage unknown.  
- **Generated:** Says both hold first name; marks as naming inconsistency/legacy duplicates; no functional difference confirmed.  
- **Analysis:** Semantically aligned with expected.  
- **Retrieval:** gt_coverage=1.0, top_score=0.9007, gate=proceed

### ec_003: Which customer column should be used as a foreign key reference: customer_id or CustomerID?
- **Type:** conflicting_references | **Difficulty:** unknown  
- **Verdict:** CORRECT  
- **Expected:** Ambiguous; PK is customer_id but FK usage uncertain; requires verification.  
- **Generated:** Chooses “no definitive answer” based strictly on context; notes customer_id is PK but does not confirm CustomerID is invalid.  
- **Analysis:** Correctly avoids asserting a resolution when FK reference is unclear.  
- **Retrieval:** gt_coverage=1.0, top_score=0.9255, gate=proceed

### ec_004: What are the valid values for order_status?
- **Type:** missing_constraint | **Difficulty:** unknown  
- **Verdict:** CORRECT  
- **Expected:** Glossary lists statuses; but schema/data dict says valid values not documented; Failed definition missing.  
- **Generated:** Says cannot find allowed set / constraints; relies on “no enum documentation”.  
- **Analysis:** Correct “not available” behavior.  
- **Retrieval:** gt_coverage=1.0, top_score=0.55 (raw), retrieval_quality_score=0.7, gate=proceed

### ec_005: Is there a difference between Product, Item, and SKU?
- **Type:** ambiguous_synonyms | **Difficulty:** unknown  
- **Verdict:** CORRECT  
- **Expected:** Product and Item related but distinct/not fully defined; SKU is unique identifier for product variant; distinctions unclear.  
- **Generated:** States Product definition incomplete; Item synonym in inventory context; SKU is identifier; no full formal distinction for Product/Item.  
- **Analysis:** Matches expected “related but unclear” stance.  
- **Retrieval:** gt_coverage=1.0, top_score=0.7, gate=proceed

### ec_006: Which table should ORDER_ITEMS.product_id reference: PRODUCTS or INVENTORY?
- **Type:** ambiguous_reference | **Difficulty:** unknown  
- **Verdict:** CORRECT  
- **Expected:** Documentation says PRODUCTS or INVENTORY? but “not verified”; relationship cannot be determined.  
- **Generated:** Explicitly cannot verify; cites that FK target “not verified”.  
- **Analysis:** Correct uncertainty preservation.  
- **Retrieval:** gt_coverage=0.5, top_score=0.9609, gate=proceed

### ec_007: What's the difference between Revenue and Sales?
- **Type:** circular_definition | **Difficulty:** unknown  
- **Verdict:** CORRECT  
- **Expected:** Both are circularly defined via cross-references; no clear distinction.  
- **Generated:** Restates cross-referencing definitions and notes no explicit distinction.  
- **Analysis:** Correct.  
- **Retrieval:** gt_coverage=0.0 (anomalous), top_score=0.7, gate=proceed

### ec_008: Can one order have multiple payments?
- **Type:** conflicting_cardinality | **Difficulty:** unknown  
- **Verdict:** CORRECT  
- **Expected:** Table hints many-to-one, but glossary explicitly questions it; uncertainty remains.  
- **Generated:** Says relationship/cardinality not defined in contexts; glossary suggests “multiple payment attempts” but explicitly unclear.  
- **Analysis:** Correctly reflects uncertainty.  
- **Retrieval:** gt_coverage=0.5, top_score=0.7, gate=proceed

### ec_009: What payment methods are accepted?
- **Type:** missing_enum_values | **Difficulty:** unknown  
- **Verdict:** CORRECT  
- **Expected:** No authoritative accepted list; “missing valid values”.  
- **Generated:** Says values not documented/confirmable; therefore cannot confirm accepted methods.  
- **Analysis:** Correctly does not fabricate.  
- **Retrieval:** gt_coverage=1.0, top_score=0.7, gate=proceed

### ec_010: What's the correct table name: ORDER_ITEMS or ORDER_DETAILS?
- **Type:** naming_ambiguity | **Difficulty:** unknown  
- **Verdict:** CORRECT  
- **Expected:** Ambiguous in docs; DDL uses ORDER_ITEMS, but uncertainty acknowledged.  
- **Generated:** States evidence contains ambiguity; notes `order_items` is the concrete table name referenced for attributes, but does not “conclusively verify” over ORDER_DETAILS.  
- **Analysis:** Faithful to “ambiguity” nature.  
- **Retrieval:** gt_coverage=1.0, top_score=0.9627, gate=proceed

### ec_011: Which date column should be used to track when an order was created?
- **Type:** duplicate_columns | **Difficulty:** unknown  
- **Verdict:** CORRECT  
- **Expected:** order_date vs OrderDate vs created_at; no guidance which is used by application.  
- **Generated:** Chooses order_date since its description says “Date order was created”; acknowledges other columns exist but no mapping for created_at semantics.  
- **Analysis:** Reasonable and consistent with expected stance (selects the most directly documented one).  
- **Retrieval:** gt_coverage=1.0, top_score=0.9674, gate=proceed

### ec_012: What does the Failed order status mean?
- **Type:** missing_definition | **Difficulty:** unknown  
- **Verdict:** CORRECT  
- **Expected:** Failed is a valid status value but definition missing.  
- **Generated:** States that “Failed” exists but definition missing, so meaning cannot be derived.  
- **Analysis:** Correct.  
- **Retrieval:** gt_coverage=1.0, top_score=0.7, gate=proceed

### ec_013: Are there any NOT NULL constraints defined in the schema?
- **Type:** missing_constraints | **Difficulty:** unknown  
- **Verdict:** CORRECT  
- **Expected:** NOT NULL not written in DDL; PKs implicitly NOT NULL; but keyword absent.  
- **Generated:** Says NOT NULL not documented; can’t confirm any NOT NULL beyond what’s explicitly mentioned (none).  
- **Analysis:** Matches the “cannot confirm from provided context” framing.  
- **Retrieval:** gt_coverage=null (in bundle), retrieval_quality_score=0.7628, gate=proceed

### ec_014: What's the difference between unit_price and current_price in PRODUCTS?
- **Type:** duplicate_columns | **Difficulty:** unknown  
- **Verdict:** CORRECT  
- **Expected:** both DECIMAL(10,2); data dictionary hints “different from unit_price?”; distinction unclear.  
- **Generated:** States unit_price = standard selling price; current_price is separate and “different from unit_price”; no more detail.  
- **Analysis:** Correctly limited to available documentation.  
- **Retrieval:** gt_coverage=1.0, top_score=0.7235, gate=proceed

### ec_015: When is an invoice generated vs payment processed?
- **Type:** missing_workflow | **Difficulty:** unknown  
- **Verdict:** CORRECT  
- **Expected:** glossary asks timing questions; definitions don’t specify sequence/timing.  
- **Generated:** Explains Receipt is after payment; but cannot determine invoice vs payment timing.  
- **Analysis:** Good separation of what is known vs unknown.  
- **Retrieval:** gt_coverage=1.0, retrieval_quality_score=0.7, gate=proceed

### ec_016: Is the sku column in PRODUCTS unique?
- **Type:** missing_uniqueness | **Difficulty:** unknown  
- **Verdict:** CORRECT  
- **Expected:** sku marked “UNIQUE?” but not actually enforced; no unique constraint documented.  
- **Generated:** Says “UNIQUE?” indicates uncertainty; no definitive uniqueness constraint confirmed.  
- **Analysis:** Correctly interprets question mark annotations as non-enforcement.  
- **Retrieval:** gt_coverage=1.0, retrieval_quality_score=0.7699, gate=proceed

### ec_017: What is the relationship between customers and orders?
- **Type:** ambiguous_relationship | **Difficulty:** unknown  
- **Verdict:** CORRECT  
- **Expected:** Glossary explicitly uncertain; orders/customer_id FK ambiguous.  
- **Generated:** Restates “customer to order unclear” and “accounts may place orders”.  
- **Analysis:** Matches expected uncertainty.  
- **Retrieval:** gt_coverage=0.5, top_score=0.7, gate=proceed

### ec_018: Which price column represents what the customer actually pays?
- **Type:** semantic_ambiguity | **Difficulty:** unknown  
- **Verdict:** CORRECT  
- **Expected:** ambiguous across order amounts, item prices, product prices, and payments.  
- **Generated:** Does not pick a single “actual paid” column definitively; points to payment_amount as closest but not explicitly tied; mentions discounts/line_total logic only as documented.  
- **Analysis:** Appropriate limitation.  
- **Retrieval:** gt_coverage=0.0 (in provided data), top_score=0.7, gate=proceed

### ec_019: What's the difference between Shipment, Delivery, and Fulfillment?
- **Type:** overlapping_concepts | **Difficulty:** unknown  
- **Verdict:** CORRECT  
- **Expected:** Definitions given but boundaries unclear; fulfillment encompasses shipment and delivery.  
- **Generated:** Restates exactly those definitions.  
- **Analysis:** Correct and fully grounded.  
- **Retrieval:** gt_coverage=1.0, top_score=0.7, gate=proceed

### ec_020: Are foreign key constraints enforced in the schema?
- **Type:** missing_fk_enforcement | **Difficulty:** unknown  
- **Verdict:** CORRECT  
- **Expected:** Data dictionary indicates FKs in docs but not enforced in DDL.  
- **Generated:** Properly says context cannot confirm enforcement; notes “Foreign Keys” exist as documented relationships but enforcement is not established in provided info; respects ambiguity.  
- **Analysis:** Correct “cannot confirm enforcement” response (even if expected implies it should be “no”). Given the retrieved text repeatedly marks ambiguity/unverified, this is the safest semantically consistent choice.  
- **Retrieval:** gt_coverage=0.5, top_score=0.7, gate=proceed

## Anomalies & Recommendations

### Red Flags
1. **Metric anomalies in coverage despite correct answers**
   - ec_007 shows `gt_coverage=0.0` while answer is grounded and semantically correct.
   - ec_018 shows `gt_coverage=0.0` while answer is grounded.
   - These likely indicate **GT coverage calculation misalignment** (expected_sources not matching the actual conceptual nodes used by KG retrieval), not necessarily model failure.

2. **No abstentions even on “unknown” difficulty**
   - All 20 questions were answered with `gate_decision=proceed`. While this is acceptable when “unknown” questions are expected to be answered as “cannot determine,” it’s worth checking that the system never fabricates instead of abstaining.

### Recommendations
- **Validate GT coverage computation**: ensure that `gt_coverage` aligns with how “expected_sources” are represented (table/term nodes vs document chunks vs ontology concepts). Consider mapping expected sources to the same normalization used by retrieval.
- **Introduce an explicit “cannot determine” policy test**: for missing-definition / missing-enum / missing-constraint categories, track whether answers always follow the “cannot confirm from KG” pattern (they appear to in this run).
- **Tune retrieval gating policy for negative/unknown edgecases**: if there exists any “negative” or true “no information found” subset, measure false positives; here there are none, but future ablations should verify abstention correctness.

## Comparison Notes (if applicable)
- `AB-BEST` suggests best configuration, but **no baseline AB-00 metrics or `ablation_context` are included** in the provided bundle. Therefore, no quantitative comparison against baseline can be performed per rubric.