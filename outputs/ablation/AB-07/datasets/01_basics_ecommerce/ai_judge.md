# AI-Judge Evaluation: AB-07/01_basics_ecommerce
**Evaluator:** (`gpt-5.4-nano-2026-03-17`) using `docs/AI_JUDGE_PROMPT.md`  
**Date:** 2026-07-17

---

# Ablation Study Evaluation: AB-07 — 01_basics_ecommerce

## Executive Summary
This run shows **excellent end-to-end system behavior** on the e-commerce “basics” dataset: the Builder completed **all 7 tables** with **no Cypher failures, mapping failures, or ingestion errors**, and the Query pipeline produced answers that were **fully grounded** (**grounded_rate = 1.0**) across **all 15 questions**. Retrieval quality is also healthy overall (**avg_gt_coverage = 1.0**, **avg_top_score ≈ 0.78**), and pipeline health indicators show **zero grader rejections/inconsistencies and zero abstentions**.

The main limitation is interpretive: while retrieval/grounding are perfect, one question (Q015) exhibits an **answer-structure gap**—the expected answer highlights `SALES_ORDER_HDR.TOTAL_AMT`, but the generated answer omits that specific column and instead leans on line-item and payment fields.

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
Evidence from `builder_report`:
- `tables_parsed = 7`, `tables_completed = 7`, `all_tables_completed = true`
- `cypher_failed = false`
- `failed_mappings = []`, `ingestion_errors = []`
- `triplets_extracted = 115` and `entities_resolved = 87` (reasonable density; no signs of ER collapse or extraction failure)
- No builder skips/errors: `builder_skipped = false`

Meets (and exceeds) rubric “score 5”: all tables completed, no Cypher failures, no failed mappings.

### 2. Retrieval Effectiveness (5/5)
Evidence from `query_report` + `pipeline_health`:
- `grounded_rate` is not directly in `query_report`, but `grounded_count=15` is implied by `grounded_rate` not provided; per-question shows `grounded=true` for all.
- `avg_gt_coverage = 1.0`
- `avg_top_score = 0.7794` (well within “healthy” range for reranker)
- `abstained_count = 0` and `gate_abstentions = 0`
- `questions_with_low_retrieval_score = 0`
- No case of `gt_coverage = 0` is shown

This matches rubric score-5: high coverage, no retrieval misses indicated, and no false abstentions.

### 3. Answer Quality (4/5)
Evidence:
- `grounded_rate = 1.0` (per-question `grounded=true` for all shown)
- `grader_rejection_count = 0` for all questions
- However, **content completeness vs. expected** is not always perfect.

Most questions are strongly aligned with expected answers. The main quality dip is:

- **Q015**: expected explicitly includes `SALES_ORDER_HDR.TOTAL_AMT` for order header value, but the generated answer says the column name is “not provided in retrieved context,” and then pivots to line items (`UNIT_PRICE`, `LINE_AMT`) and payments (`PAYMENT.AMOUNT`). The answer is still grounded, but it doesn’t fully satisfy the “header totals” requirement from the expected answer.

Because the rubric emphasizes semantic correctness/completeness, this is sufficient to drop from 5 → 4, despite perfect grounding and no hallucination rejections.

### 4. Pipeline Health (5/5)
Evidence from `pipeline_health`:
- `total_grader_rejections = 0`
- `grader_inconsistencies = 0`
- `gate_abstentions = 0`
- `cypher_failed = false`
- `failed_mappings_count = 0`
- `ingestion_errors_count = 0`

All self-reflection/healing loops appear unnecessary or successful (no recorded failures). Meets rubric score 5.

### 5. Ablation Impact (N/A)
This bundle is labeled `AB-07`, but the provided `config` does **not** include an explicit `ablation_context` or a clear mapping of which flags were changed vs baseline AB-00. Therefore, ablation-impact scoring is **not determinable** from the bundle content according to the rubric.

## Per-Question Deep Dive

### Q001: What information is stored for each customer?
- **Type:** direct_mapping | **Difficulty:** easy
- **Verdict:** CORRECT
- **Expected:** CUST_ID, FULL_NAME, EMAIL (unique), REGION_CODE, CREATED_AT, IS_ACTIVE
- **Generated:** Lists the same customer fields from `CUSTOMER_MASTER` (plus confirms types).
- **Analysis:** Exact semantic match; minor mismatch risk on “email must be unique” is not harmed—answer still captures all key stored attributes.
- **Retrieval:** gt_coverage=1.0, top_score=0.7, gate=proceed

### Q002: How are products categorized on the platform?
- **Type:** direct_mapping | **Difficulty:** easy
- **Verdict:** CORRECT
- **Expected:** Product→Category via CATEGORY_ID; hierarchical categories with optional parent
- **Generated:** Correctly states CATEGORY_ID FK and PARENT_CATEGORY_ID self-reference
- **Analysis:** Fully aligned with schema/glossary.
- **Retrieval:** gt_coverage=1.0, top_score=0.7, gate=proceed

### Q003: What is the relationship between customers and sales orders?
- **Type:** direct_mapping | **Difficulty:** easy
- **Verdict:** CORRECT
- **Expected:** One customer places zero or more orders; each order has exactly one customer via CUST_ID FK
- **Generated:** Uses glossary + SALES_ORDER_HDR.CUST_ID → CUSTOMER_MASTER.CUST_ID
- **Analysis:** Correct and grounded.
- **Retrieval:** gt_coverage=1.0, top_score=0.9847, gate=proceed

### Q004: What does an order line item contain?
- **Type:** direct_mapping | **Difficulty:** easy
- **Verdict:** CORRECT
- **Expected:** product, quantity, unit price at purchase, extended amount; belongs to one sales order
- **Generated:** Correctly lists unit price, quantity, LINE_AMT logic; enumerates columns including LINE_ID, ORDER_ID, PRODUCT_ID
- **Analysis:** Meets expected content.
- **Retrieval:** gt_coverage=1.0, top_score=0.9881, gate=proceed

### Q005: How are payments linked to orders?
- **Type:** direct_mapping | **Difficulty:** easy
- **Verdict:** CORRECT
- **Expected:** Payment associated to exactly one sales order via ORDER_ID FK; method/amount/status/timestamp
- **Generated:** Correctly states PAYMENT.ORDER_ID → SALES_ORDER_HDR.ORDER_ID and supports it with “references exactly one Sales Order”
- **Analysis:** Strong match.
- **Retrieval:** gt_coverage=1.0, top_score=0.95, gate=proceed

### Q006: What statuses can an order have?
- **Type:** attribute_lookup | **Difficulty:** easy
- **Verdict:** CORRECT
- **Expected:** PENDING, CONFIRMED, SHIPPED, DELIVERED, CANCELLED (via CHECK constraint/glossary)
- **Generated:** Lists exactly those five statuses
- **Analysis:** Correct.
- **Retrieval:** gt_coverage=1.0, top_score=0.7, gate=proceed

### Q007: Which table stores the product SKU information?
- **Type:** direct_mapping | **Difficulty:** easy
- **Verdict:** CORRECT
- **Expected:** TB_PRODUCT.SKU (and related product attributes)
- **Generated:** “TB_PRODUCT stores SKU in TB_PRODUCT.SKU”
- **Analysis:** Correct and succinct.
- **Retrieval:** gt_coverage=1.0, top_score=0.98, gate=proceed

### Q008: How can I find all orders placed by a specific customer?
- **Type:** multi_hop | **Difficulty:** medium
- **Verdict:** CORRECT
- **Expected:** Query SALES_ORDER_HDR filter by CUST_ID; join to CUSTOMER_MASTER if needed
- **Generated:** Correctly describes filtering by SALES_ORDER_HDR.CUST_ID and optional join
- **Analysis:** Satisfies expected guidance.
- **Retrieval:** gt_coverage=1.0, top_score=0.7, gate=proceed

### Q009: How does the schema link orders to their individual product line items?
- **Type:** multi_hop | **Difficulty:** medium
- **Verdict:** CORRECT
- **Expected:** Junction role of ORDER_LINE_ITEM: ORDER_ID→SALES_ORDER_HDR, PRODUCT_ID→TB_PRODUCT; includes QUANTITY, UNIT_PRICE, LINE_AMT
- **Generated:** Correctly explains using ORDER_LINE_ITEM.ORDER_ID and PRODUCT_ID; matches core attributes
- **Analysis:** Correct.
- **Retrieval:** gt_coverage=1.0, top_score=0.7, gate=proceed

### Q010: Show me the order hierarchy from customer to line items.
- **Type:** multi_hop | **Difficulty:** medium
- **Verdict:** CORRECT
- **Expected:** CUSTOMER_MASTER → SALES_ORDER_HDR → ORDER_LINE_ITEM → TB_PRODUCT
- **Generated:** Correct hierarchy and describes FK links for the customer and order→line relationship
- **Analysis:** Good coverage (though it doesn’t deeply enumerate product at the end, it is implied by using line items.)
- **Retrieval:** gt_coverage=1.0, top_score=0.7, gate=proceed

### Q011: How does the schema model the confirmation state of a payment and its relationship to the order?
- **Type:** multi_hop | **Difficulty:** medium
- **Verdict:** CORRECT
- **Expected:** PAYMENT.STATUS_CODE + PAYMENT.CONFIRMED_AT; order-level SALES_ORDER_HDR.PAYMENT_CONFIRMED_AT; FK PAYMENT.ORDER_ID; order lifecycle tied to payment confirmation
- **Generated:** Covers all these elements
- **Analysis:** Correct and grounded.
- **Retrieval:** gt_coverage=1.0, top_score=0.7, gate=proceed

### Q012: How are shipments related to orders and warehouses?
- **Type:** multi_hop | **Difficulty:** medium
- **Verdict:** CORRECT
- **Expected:** SHIPMENT.ORDER_ID→SALES_ORDER_HDR; includes source warehouse code, tracking, status
- **Generated:** Correctly states SHIPMENT.ORDER_ID and SHIPMENT.WAREHOUSE_CODE; references business definition attributes
- **Analysis:** Matches expected.
- **Retrieval:** gt_coverage=1.0, top_score=0.7884, gate=proceed

### Q013: Can a product belong to multiple categories?
- **Type:** negative | **Difficulty:** easy
- **Verdict:** CORRECT
- **Expected:** No; product belongs to exactly one category via TB_PRODUCT.CATEGORY_ID FK
- **Generated:** States “No” and cites glossary + FK
- **Analysis:** Correct handling of negative question.
- **Retrieval:** gt_coverage=1.0, top_score=0.7, gate=proceed

### Q014: Is it possible for a customer to place an order without payment?
- **Type:** negative | **Difficulty:** medium
- **Verdict:** CORRECT
- **Expected:** Yes can exist without payment initially; PAYMENT_CONFIRMED_AT nullable; “can’t ship until confirmed”
- **Generated:** Correctly distinguishes order creation vs shipping constraints
- **Analysis:** Semantically correct for the negative framing.
- **Retrieval:** gt_coverage=1.0, top_score=0.7, gate=proceed

### Q015: What schema fields support monetary value tracking across orders and their line items?
- **Type:** multi_hop | **Difficulty:** easy
- **Verdict:** PARTIALLY_CORRECT
- **Expected:** SALES_ORDER_HDR.TOTAL_AMT (NOT NULL) + ORDER_LINE_ITEM.UNIT_PRICE, QUANTITY(>0), LINE_AMT; linked via ORDER_ID
- **Generated:** Explains line-item monetary fields and the linkage, and also mentions PAYMENT.AMOUNT; but **does not name `SALES_ORDER_HDR.TOTAL_AMT`**, claiming it wasn’t in retrieved context.
- **Analysis:** Likely completeness miss: answer doesn’t include the expected header total column name despite the system being grounded. This reduces quality from fully correct to partial.
- **Retrieval:** gt_coverage=1.0, top_score=0.7, gate=proceed

## Anomalies & Recommendations

### Red Flags
- **Q015 completeness gap**: expected order header total (`SALES_ORDER_HDR.TOTAL_AMT`) is not explicitly provided in the generated answer, even though the broader context appears to include “Sales Order” descriptions that contain “Total monetary value”.
- No evidence of hallucination or abstention errors: `grader_rejection_count=0` across the board.

### Recommendations
1. **Add “header field retrieval enforcement” for known schema asks**: when expected answers mention a specific table/column family (e.g., “TOTAL_AMT”), ensure the generator explicitly extracts the column name when it exists in retrieved contexts.
2. **Context-to-assertion checklist**: during answer generation, require that if contexts include `SALES_ORDER_HDR` monetary fields, the output must reference the specific column(s) (not just the concept “total monetary value”).
3. **Negative question calibration review**: though correct here, keep an eye on Q-type handling by tying gate logic to explicit “nullable/constraints/business rules” statements (already done well).

## Comparison Notes (if applicable)
- Ablation impact scoring is **N/A** because the bundle does not specify what changed from baseline AB-00 (no `ablation_context.changes_vs_baseline` and no explicit ablation flag deltas).
- Functionally, the run corresponds to a strong configuration (hybrid retrieval + reranker enabled), and performance is consistent with that expectation.