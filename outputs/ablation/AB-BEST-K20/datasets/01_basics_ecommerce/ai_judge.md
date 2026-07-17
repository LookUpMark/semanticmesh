# AI-Judge Evaluation: AB-BEST-K20/01_basics_ecommerce
**Evaluator:** (`gpt-5.4-nano-2026-03-17`) using `docs/AI_JUDGE_PROMPT.md`  
**Date:** 2026-07-17

---

# Ablation Study Evaluation: AB-BEST-K20 — 01_basics_ecommerce

## Executive Summary
This run shows excellent end-to-end quality on the **basics e-commerce** dataset: the builder completed all table mappings with **no Cypher failures** or ingestion errors, and the query layer achieved **grounded_rate = 1.0** with **avg_gt_coverage = 1.0** across all 15 questions. Retrieval confidence appears consistently strong (avg_top_score ≈ **0.789**), and there were **zero grader rejections** or pipeline inconsistencies.  
The main caveat is that one “negative” question (Q014) is answered as **YES** rather than abstaining or explicitly stating a contradiction, which depends on whether the expected interpretation treats “order has one or more payments” as a hard constraint vs. only a business rule.

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
- `tables_completed = 7`, `all_tables_completed = true`
- `cypher_failed = false`
- `failed_mappings = []`, `ingestion_errors = []`
- Triplet density cannot be computed precisely from the provided fields, but triplets/entities look healthy (`triplets_extracted=132`, `entities_resolved=108`), indicating extraction + ER were not obviously broken.

### 2. Retrieval Effectiveness (5/5)
- `grounded_rate = 1.0`, `abstained_count = 0`
- `avg_gt_coverage = 1.0` (ground-truth sources always retrieved)
- `avg_top_score = 0.789` (healthy for a reranker like `bge-reranker-v2-m3`)
- `pipeline_health.questions_with_low_retrieval_score = 0`
- For negative questions, the gate behavior is “proceed” (no abstentions), but that’s not penalized by the rubric unless the negative logic is wrong in answer content.

### 3. Answer Quality (4/5)
Overall groundedness is perfect (`grounded_count=15` and `grounded_rate=1.0`), and answers are consistently semantically aligned with expected facts.

However, there is a likely **logical/interpretation issue** in the negative test:
- **Q014 (negative)**: Expected answers argue that orders should not exist without payment in practice (created first, but fulfillment requires payment confirmation; the expected phrasing leans toward “not without payment” in the business-rule sense).  
  The generated answer concludes **“Yes, possible at schema level for an order without payment records.”**  
  Even though this is plausible from FK directionality, it conflicts with the *expected* interpretation provided in the bundle.

Because the rubric prioritizes semantic correctness vs. string match, and because only this “negative” item is suspect, the run is still very strong, but not a clean 5.

### 4. Pipeline Health (5/5)
- `total_grader_rejections = 0`
- `grader_inconsistencies = 0`
- `gate_abstentions = 0`
- `cypher_failed = false`, `failed_mappings_count = 0`, `ingestion_errors_count = 0`
- Latency fields are shown as 0/blanked in builder/query reports, but there are no error indicators.

### 5. Ablation Impact (N/A)
- The rubric specifies scoring this dimension only for non-baseline studies with explicit `changes_vs_baseline` / `ablation_context`.
- This bundle (`AB-BEST-K20`) does not include an ablation context section, and we are not told which flags changed vs. AB-00 in a comparable machine-readable way.
- Therefore: **N/A**.

## Per-Question Deep Dive

### Q001: What information is stored for each customer?
- **Type:** direct_mapping | **Difficulty:** easy
- **Verdict:** CORRECT
- **Expected:** ID, full name, email (unique), region code, creation date, active status
- **Generated:** Matches schema columns in `CUSTOMER_MASTER` and describes uniqueness for email
- **Analysis:** Strong semantic match to expected schema attributes; correctly identifies key semantics like unique email.
- **Retrieval:** gt_coverage=1.0, top_score=0.7, gate=proceed

### Q002: How are products categorized on the platform?
- **Type:** direct_mapping | **Difficulty:** easy
- **Verdict:** CORRECT
- **Expected:** product→category via CATEGORY_ID; category has hierarchical parent via PARENT_CATEGORY_ID
- **Generated:** Matches both FK structure and hierarchy semantics
- **Analysis:** Fully aligned with expected relational model.
- **Retrieval:** gt_coverage=1.0, top_score=0.7, gate=proceed

### Q003: What is the relationship between customers and sales orders?
- **Type:** direct_mapping | **Difficulty:** easy
- **Verdict:** CORRECT
- **Expected:** one customer places zero-or-more orders; orders reference customer via CUST_ID FK
- **Generated:** Matches FK and glossary statement
- **Analysis:** Correct relationship direction and cardinality.
- **Retrieval:** gt_coverage=1.0, top_score=0.9846936454, gate=proceed

### Q004: What does an order line item contain?
- **Type:** direct_mapping | **Difficulty:** easy
- **Verdict:** CORRECT
- **Expected:** product, quantity, unit price, extended amount; belongs to exactly one order
- **Generated:** Matches UNIT_PRICE, QUANTITY, LINE_AMT and membership via ORDER_ID
- **Analysis:** Complete and semantically correct.
- **Retrieval:** gt_coverage=1.0, top_score=0.9870296136, gate=proceed

### Q005: How are payments linked to orders?
- **Type:** direct_mapping | **Difficulty:** easy
- **Verdict:** CORRECT
- **Expected:** PAYMENT.ORDER_ID FK → SALES_ORDER_HDR.ORDER_ID; tracks method/amount/status/timestamps
- **Generated:** Matches FK and relationship summary
- **Analysis:** Correct.
- **Retrieval:** gt_coverage=1.0, top_score=0.9091032457, gate=proceed

### Q006: What statuses can an order have?
- **Type:** attribute_lookup | **Difficulty:** easy
- **Verdict:** CORRECT
- **Expected:** PENDING, CONFIRMED, SHIPPED, DELIVERED, CANCELLED
- **Generated:** Same list, aligned with business glossary and SALES_ORDER_HDR.STATUS_CODE
- **Analysis:** Correct lifecycle values.
- **Retrieval:** gt_coverage=1.0, top_score=0.7, gate=proceed

### Q007: Which table stores the product SKU information?
- **Type:** direct_mapping | **Difficulty:** easy
- **Verdict:** CORRECT
- **Expected:** TB_PRODUCT.SKU
- **Generated:** TB_PRODUCT and SKU column
- **Analysis:** Exact semantic match.
- **Retrieval:** gt_coverage=1.0, top_score=0.9824231167, gate=proceed

### Q008: How can I find all orders placed by a specific customer?
- **Type:** multi_hop | **Difficulty:** medium
- **Verdict:** CORRECT
- **Expected:** filter SALES_ORDER_HDR by CUST_ID; join via CUST_ID to CUSTOMER_MASTER
- **Generated:** Correct join path and filtering logic
- **Analysis:** Correct.
- **Retrieval:** gt_coverage=1.0, top_score=0.7, gate=proceed

### Q009: How does the schema link orders to their individual product line items?
- **Type:** multi_hop | **Difficulty:** medium
- **Verdict:** CORRECT
- **Expected:** ORDER_LINE_ITEM is junction with ORDER_ID FK to SALES_ORDER_HDR and PRODUCT_ID FK to TB_PRODUCT
- **Generated:** Matches chain and line-level fields
- **Analysis:** Correct multi-hop relational explanation.
- **Retrieval:** gt_coverage=1.0, top_score=0.7, gate=proceed

### Q010: Show me the order hierarchy from customer to line items.
- **Type:** multi_hop | **Difficulty:** medium
- **Verdict:** CORRECT
- **Expected:** CUSTOMER_MASTER → SALES_ORDER_HDR → ORDER_LINE_ITEM → TB_PRODUCT
- **Generated:** Correct hierarchy and FK steps; includes ORDER_ID linkage to line items
- **Analysis:** Semantically correct.
- **Retrieval:** gt_coverage=1.0, top_score=0.7, gate=proceed

### Q011: How does the schema model the confirmation state of a payment and its relationship to the order?
- **Type:** multi_hop | **Difficulty:** medium
- **Verdict:** CORRECT
- **Expected:** PAYMENT.CONFIRMED_AT + PAYMENT.STATUS_CODE; order mirrors via SALES_ORDER_HDR.PAYMENT_CONFIRMED_AT; FK PAYMENT.ORDER_ID → SALES_ORDER_HDR.ORDER_ID
- **Generated:** Correctly describes both timestamp/status fields and FK link
- **Analysis:** Correct.
- **Retrieval:** gt_coverage=1.0, top_score=0.7, gate=proceed

### Q012: How are shipments related to orders and warehouses?
- **Type:** multi_hop | **Difficulty:** medium
- **Verdict:** CORRECT
- **Expected:** SHIPMENT.ORDER_ID FK → SALES_ORDER_HDR; SHIPMENT.WAREHOUSE_CODE as source warehouse; includes tracking/status
- **Generated:** Matches FK and source warehouse presence
- **Analysis:** Correct.
- **Retrieval:** gt_coverage=1.0, top_score=0.9737446992, gate=proceed

### Q013: Can a product belong to multiple categories?
- **Type:** negative | **Difficulty:** easy
- **Verdict:** CORRECT
- **Expected:** No; TB_PRODUCT.CATEGORY_ID FK implies exactly one category per product
- **Generated:** “No” and explains single-category constraint via FK and glossary rule
- **Analysis:** Correct handling of negative question.
- **Retrieval:** gt_coverage=1.0, top_score=0.7, gate=proceed

### Q014: Is it possible for a customer to place an order without payment?
- **Type:** negative | **Difficulty:** medium
- **Verdict:** INCORRECT
- **Expected:** The business rule implies orders cannot be shipped until payment confirmed; expected framing suggests “no payment required” is not allowed as a valid state (or at least not supported as a business-accepted order state).
- **Generated:** “Yes” at schema level: says payments are only enforced directionally (payment→order FK) and that there is no FK back requiring payment row; concludes payments are optional.
- **Analysis:** Generated answer is plausible from FK directionality, but it conflicts with the *expected* business-interpretation in the bundle (and the negative test’s intention). This is the only notable mismatch.
- **Retrieval:** gt_coverage=1.0, top_score=0.7, gate=proceed

### Q015: What schema fields support monetary value tracking across orders and their line items?
- **Type:** multi_hop | **Difficulty:** easy
- **Verdict:** CORRECT
- **Expected:** TOTAL_AMT at order header; UNIT_PRICE/QUANTITY/LINE_AMT at line level; linked by ORDER_ID FK
- **Generated:** Discusses TOTAL_AMT and line-level unit/extended amount; also mentions payment.amount
- **Analysis:** Semantically aligned; extra mention of payment fields is acceptable.
- **Retrieval:** gt_coverage=1.0, top_score=0.7, gate=proceed

## Anomalies & Recommendations

### Red Flags
- **Negative-question semantic conflict (Q014):** The system answered “Yes” to a negative question, likely interpreting schema constraints more literally than the expected business-rule interpretation. This suggests the negative handling may need a stronger “business rule vs. pure schema” distinction.
- No other failures are apparent: groundedness is perfect and there are no grader rejections.

### Recommendations
1. **Improve negative-question policy:** When `query_type="negative"`, require the answer to either:
   - cite an explicit constraint that prevents the negative condition, or
   - clearly state “schema allows but business rule disallows fulfillment,” matching the expected phrasing intent.
2. **Distinguish “schema constraints” vs “business rules” in generation prompts:** e.g., explicitly label: “DDL/FK constraints” vs “business lifecycle rules.”
3. **Add a targeted contradiction check for “can X exist without Y” questions:** ensure the answer reflects whether the system interprets “exist” as “row exists” or “business-valid state.”

## Comparison Notes (if applicable)
- No baseline diff (`AB-00`) or `ablation_context.changes_vs_baseline` is present in the bundle, so no causal comparison is provided.
- Nonetheless, performance is uniformly excellent: builder completeness, retrieval coverage, and grounding are all at their maxima for this run.