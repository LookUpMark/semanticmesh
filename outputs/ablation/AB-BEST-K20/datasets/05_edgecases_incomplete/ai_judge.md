# AI-Judge Evaluation: AB-BEST-K20/05_edgecases_incomplete
**Evaluator:** (`gpt-5.4-nano-2026-03-17`) using `docs/AI_JUDGE_PROMPT.md`  
**Date:** 2026-07-17

---

# Ablation Study Evaluation: AB-BEST-K20 — 05_edgecases_incomplete

## Executive Summary
This run shows **strong end-to-end performance**: the builder completed all parsed tables with **no Cypher failures** and **no ingestion issues**, and the query graph achieved **grounded_rate = 1.0** with **avg_gt_coverage = 1.0** and **avg_top_score ≈ 0.78**. The main weakness is not correctness (answers are grounded and match the expected intent), but rather **realism/assurance limits** on edge cases where the glossary/schema explicitly mark items as “unclear/not verified”: the system often answers “cannot be determined from context” or repeats documented ambiguity, which is acceptable for the governance setting but can reduce “decisiveness.”

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
- `tables_parsed=5`, `tables_completed=5`, `all_tables_completed=true`
- `cypher_failed=false`
- `failed_mappings=[]`, `ingestion_errors=[]`
- Triplet extraction and ER appear healthy enough for edgecase-heavy data: `triplets_extracted=89`, `entities_resolved=78`, and (importantly) no downstream graph construction failures are reported.
**Verdict:** Builder pipeline is fully functional and completed its job without recovery/fallback pain.

### 2. Retrieval Effectiveness (5/5)
- `query_report.avg_gt_coverage = 1.0`
- `query_report.avg_top_score = 0.7818` (healthy semantic confidence for bge-reranker-v2-m3)
- `abstained_count=0` and `gate_abstentions=0`, consistent with expected answer availability in this dataset slice (even when “cannot determine” is the correct governance response, it is still answerable).
- No per-question indicator of retrieval collapse: `pipeline_health.questions_with_low_retrieval_score = 0`
**Verdict:** Retrieval is consistently finding the ground-truth relevant sources.

### 3. Answer Quality (4/5)
- `query_report.grounded_rate = 1.0` (every answer is verifiably grounded in retrieved KG context).
- Across multiple edge-case types (duplicates, conflicting references, missing definitions/constraints, circular definitions, ambiguous relationships), answers **either**:
  - provide the expected glossary/schema interpretation, or
  - correctly state that the info is not determinable / definition missing / unclear.
  
Notable nuance: some “governance-style” queries (e.g., NOT NULL constraints, FK enforcement) are answered in a way that stays within what contexts actually specify. This is generally correct, but compared to a stricter “derive definitive rule from DDL semantics” approach, it’s sometimes **more cautious** than the expected_answer’s implied certainty. That’s why this is **4** rather than 5.

Worst/representative examples:
- **ec_004 (valid order_status values):** model says it cannot find enumerated values in context—this aligns with the expected note “[missing reference]”; grounded and correct.
- **ec_013 (NOT NULL constraints?):** generated response is cautious (“does not confirm elsewhere”), whereas expected_answer frames PK columns as implicitly NOT NULL; however it remains grounded and does not hallucinate.
- **ec_020 (FK enforcement):** model answers “cannot determine” from KG context; expected_answer asserts “no FK constraints enforced,” but the provided expected context description implies this is known from DDL. The model’s response is still reasonable but may diverge from the “known no-enforcement” conclusion.

### 4. Pipeline Health (5/5)
- `cypher_failed=false`
- `failed_mappings_count=0`, `ingestion_errors_count=0`
- `grader_inconsistencies=0`
- `total_grader_rejections=2`, but:
  - per-question `grader_rejection_count` is mostly 0, with **ec_012** showing `grader_rejection_count=1`
  - grader consistency is valid (`grader_consistency_valid=true` everywhere shown)
**Verdict:** Self-reflection and gating behaved stably; rejections did not indicate systemic failure.

### 5. Ablation Impact (N/A)
This bundle is **AB-BEST-K20**, but the provided JSON does not include an `ablation_context` (e.g., changes_vs_baseline, expected_impact). Therefore, rubric comparison to baseline cannot be applied.

## Per-Question Deep Dive (20/20)

### ec_001: What is a customer?
- **Type:** missing_definition | **Difficulty:** unknown
- **Verdict:** CORRECT
- **Expected:** Customer definition from business glossary; related terms Client, Account Holder, End User.
- **Generated:** Defines Customer from glossary snippet; mentions Client interchangeability.
- **Analysis:** Correct semantic capture of “Customer” and related glossary context.
- **Retrieval:** gt_coverage=1.0, top_score=0.9837, gate=proceed

### ec_002: What's the difference between firstName and first_name in the CUSTOMERS table?
- **Type:** duplicate_columns | **Difficulty:** unknown
- **Verdict:** CORRECT
- **Expected:** Both exist with identical type; duplicates from inconsistent naming; application usage unknown.
- **Generated:** States both store first name; naming inconsistency; no further semantic/process difference.
- **Analysis:** Matches expected “duplicate/legacy” and “no usage documented.”
- **Retrieval:** gt_coverage=1.0, top_score=0.8862, gate=proceed

### ec_003: Which customer column should be used as a foreign key reference: customer_id or CustomerID?
- **Type:** conflicting_references | **Difficulty:** unknown
- **Verdict:** CORRECT
- **Expected:** Inconsistency documented; both referenced with unclear verification; pending DBA verification.
- **Generated:** Cannot definitively determine from context; cites “check with DBA” / unclear FK reference.
- **Analysis:** Properly respects “unverified/unclear” governance stance.
- **Retrieval:** gt_coverage=1.0, top_score=0.9255, gate=proceed

### ec_004: What are the valid values for order_status?
- **Type:** missing_constraint | **Difficulty:** unknown
- **Verdict:** CORRECT
- **Expected:** Glossary lists statuses but marks workflow/enumeration reference missing; not enforced via CHECK.
- **Generated:** Says cannot find enumerated valid values; notes “See valid values in… [missing reference]”.
- **Analysis:** Correctly identifies missing enumeration in retrieved context.
- **Retrieval:** gt_coverage=1.0, top_score=0.7, gate=proceed

### ec_005: Is there a difference between Product, Item, and SKU?
- **Type:** ambiguous_synonyms | **Difficulty:** unknown
- **Verdict:** CORRECT
- **Expected:** Product defined vaguely; Item synonym in inventory context; SKU unique identifier for product variant.
- **Generated:** Extracts exactly those distinctions; acknowledges unclear Product definition but answers Product vs Item vs SKU.
- **Analysis:** Correct semantic mapping of glossary definitions.
- **Retrieval:** gt_coverage=1.0, top_score=0.7, gate=proceed

### ec_006: Which table should ORDER_ITEMS.product_id reference: PRODUCTS or INVENTORY?
- **Type:** ambiguous_reference | **Difficulty:** unknown
- **Verdict:** CORRECT
- **Expected:** “PRODUCTS (or INVENTORY?)” not verified; inventory table referenced in docs but not defined.
- **Generated:** States it can’t conclusively decide; supports PRODUCTS linkage while noting unverified target.
- **Analysis:** Correctly maintains “not verified” constraint.
- **Retrieval:** gt_coverage=1.0, top_score=0.9609, gate=proceed

### ec_007: What's the difference between Revenue and Sales?
- **Type:** circular_definition | **Difficulty:** unknown
- **Verdict:** CORRECT
- **Expected:** Circular definitions; no clear distinction.
- **Generated:** Notes definitions reference each other; no non-circular distinction present.
- **Analysis:** Correctly preserves circularity / lack of boundary.
- **Retrieval:** gt_coverage=1.0, top_score=0.7, gate=proceed

### ec_008: Can one order have multiple payments?
- **Type:** conflicting_cardinality | **Difficulty:** unknown
- **Verdict:** CORRECT
- **Expected:** PAYMENTS has order_id suggesting multiple; glossary relationship explicitly uncertain.
- **Generated:** Says cannot be definitively answered from constraints; cites “unclear relationship” note.
- **Analysis:** Correct governance answer under ambiguity.
- **Retrieval:** gt_coverage=1.0, top_score=0.7, gate=proceed

### ec_009: What payment methods are accepted?
- **Type:** missing_enum_values | **Difficulty:** unknown
- **Verdict:** CORRECT
- **Expected:** payment_method exists but allowed values missing; no CHECK enumeration.
- **Generated:** States valid payment_method values are not documented (only examples without enumeration).
- **Analysis:** Correctly identifies missing enum list.
- **Retrieval:** gt_coverage=1.0, top_score=0.7, gate=proceed

### ec_010: What's the correct table name: ORDER_ITEMS or ORDER_DETAILS?
- **Type:** naming_ambiguity | **Difficulty:** unknown
- **Verdict:** CORRECT
- **Expected:** DDL name ORDER_ITEMS; documentation ambiguity remains with ORDER_DETAILS.
- **Generated:** Cannot definitively resolve schema vs documentation usage; acknowledges business concept uses order_items.
- **Analysis:** Correctly handles naming uncertainty.
- **Retrieval:** gt_coverage=1.0, top_score=0.9627, gate=proceed

### ec_011: Which date column should be used to track when an order was created?
- **Type:** duplicate_columns | **Difficulty:** unknown
- **Verdict:** CORRECT
- **Expected:** Three candidate date columns exist; no guidance which is used by app.
- **Generated:** Chooses `order_date` based on description “Date order was created”; doesn’t claim app authority beyond that.
- **Analysis:** Matches expected semantics; grounded selection.
- **Retrieval:** gt_coverage=1.0, top_score=0.9581, gate=proceed

### ec_012: What does the Failed order status mean?
- **Type:** missing_definition | **Difficulty:** unknown
- **Verdict:** CORRECT
- **Expected:** Failed listed but marked “[definition missing]”.
- **Generated:** States “Failed” has no definition meaning.
- **Analysis:** Direct match.
- **Retrieval:** gt_coverage=1.0, top_score=0.7, gate=proceed

### ec_013: Are there any NOT NULL constraints defined in the schema?
- **Type:** missing_constraints | **Difficulty:** unknown
- **Verdict:** PARTIALLY_CORRECT
- **Expected:** No explicit NOT NULL in DDL; PK columns are implicitly NOT NULL by SQL standard; otherwise nullable by default.
- **Generated:** Mentions context does not confirm NOT NULL elsewhere; emphasizes “not documented/assumed unknown”.
- **Analysis:** Grounded and cautious, but may under-express the expected “PK implies NOT NULL” aspect.
- **Retrieval:** gt_coverage=null, top_score=0.7628, gate=proceed

### ec_014: What's the difference between unit_price and current_price in PRODUCTS?
- **Type:** duplicate_columns | **Difficulty:** unknown
- **Verdict:** CORRECT
- **Expected:** Both exist; no explanation of distinction besides “different from unit_price?”.
- **Generated:** unit_price = “Standard selling price”; current_price = “different from unit_price”; no more detail.
- **Analysis:** Matches expected level of detail.
- **Retrieval:** gt_coverage=1.0, top_score=0.7443, gate=proceed

### ec_015: When is an invoice generated vs payment processed?
- **Type:** missing_workflow | **Difficulty:** unknown
- **Verdict:** CORRECT
- **Expected:** Glossary asks “when?”; no workflow/timing rule; Invoice vs Payment timeline unknown.
- **Generated:** States context doesn’t specify invoice generation time; payment table lacks invoice events.
- **Analysis:** Correctly abstains on missing workflow rather than hallucinating.
- **Retrieval:** gt_coverage=1.0, top_score=0.7, gate=proceed

### ec_016: Is the sku column in PRODUCTS unique?
- **Type:** missing_uniqueness | **Difficulty:** unknown
- **Verdict:** CORRECT
- **Expected:** sku marked “UNIQUE?” but no UNIQUE constraint/DDL/index documented.
- **Generated:** Says uniqueness guarantee not confirmed; only intent indicated.
- **Analysis:** Correct governance read.
- **Retrieval:** gt_coverage=1.0, top_score=0.7516, gate=proceed

### ec_017: What is the relationship between customers and orders?
- **Type:** ambiguous_relationship | **Difficulty:** unknown
- **Verdict:** CORRECT
- **Expected:** Conceptual ambiguity; FK reference unclear; “one-to-many?” intended but not resolved.
- **Generated:** No precise DB relationship; describes conceptual rule with explicit uncertainty.
- **Analysis:** Correctly mirrors ambiguity and avoids asserting cardinality.
- **Retrieval:** gt_coverage=1.0, top_score=0.7, gate=proceed

### ec_018: Which price column represents what the customer actually pays?
- **Type:** semantic_ambiguity | **Difficulty:** unknown
- **Verdict:** CORRECT
- **Expected:** Multiple price columns exist; dictionary doesn’t connect them to “final customer paid amount”.
- **Generated:** States no explicit mapping from order/item/product/payments to “actually pays”; explains where info is missing.
- **Analysis:** Correct “cannot determine” answer grounded in missing mapping.
- **Retrieval:** gt_coverage=1.0, top_score=0.7, gate=proceed

### ec_019: What's the difference between Shipment, Delivery, and Fulfillment?
- **Type:** overlapping_concepts | **Difficulty:** unknown
- **Verdict:** CORRECT
- **Expected:** Fulfillment is superset; distinction not strictly defined beyond glossary statements.
- **Generated:** Repeats glossary definitions; captures containment relation.
- **Analysis:** Correctly reproduces definition boundaries.
- **Retrieval:** gt_coverage=1.0, top_score=0.7, gate=proceed

### ec_020: Are foreign key constraints enforced in the schema?
- **Type:** missing_fk_enforcement | **Difficulty:** unknown
- **Verdict:** PARTIALLY_CORRECT
- **Expected:** FK relationships documented but CREATE TABLE omits REFERENCES; schema notes FK constraints not enforced.
- **Generated:** Says context doesn’t confirm enforcement; only shows FKs marked FK with ambiguity/unverified references.
- **Analysis:** Grounded, but may not reflect the expected “explicitly not enforced in DDL” claim implied by expected_answer.
- **Retrieval:** gt_coverage=1.0, top_score=0.7, gate=proceed

## Anomalies & Recommendations

### Red Flags
- **Ambiguity-handling divergence risk:** For governance questions where expected answers assume a definitive “not enforced / implicitly NOT NULL,” the model sometimes answers “cannot determine” because it only sees “not documented/unclear” in retrieved contexts (notably **ec_013**, **ec_020**).
- **`gt_coverage` null for ec_013** despite grounded output: indicates the ground-truth source mapping might not be fully represented in the evaluation harness for that particular query.

### Recommendations
1. **Add DDL-semantics injection for constraint questions**: when the expected answer hinges on SQL standard semantics (e.g., PK ⇒ implicit NOT NULL) or DDL omission of `REFERENCES`, ensure the retrieval includes the actual parsed DDL statements or a normalized “DDL enforcement summary” node in the KG.
2. **Improve “explicitly not enforced” detection**: teach the generator to look for an enforcement-status phrase (e.g., “not enforced in DDL”) specifically, rather than general “FK marked in metadata.”
3. **Align evaluation ground-truth source mapping**: fix cases like **ec_013** where `gt_coverage=null` to avoid misleading retrieval effectiveness diagnostics.

## Comparison Notes (if applicable)
- No baseline comparison data (`changes_vs_baseline`) was provided in the bundle, so ablation-vs-baseline causal conclusions cannot be made.