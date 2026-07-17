# AI-Judge Evaluation: AB-10/01_basics_ecommerce
**Evaluator:** (`gpt-5.4-nano-2026-03-17`) using `docs/AI_JUDGE_PROMPT.md`  
**Date:** 2026-07-17

---

# Ablation Study Evaluation: AB-10 — 01_basics_ecommerce

## Executive Summary
AB-10 shows an exceptionally healthy run on the “basics” e-commerce dataset: all 7 builder tables were completed with no Cypher or ingestion failures, and the query graph produced grounded answers for 15/15 questions. Retrieval quality is strong (avg top score ~0.787) with zero low-retrieval questions reported, and there are no grader rejections or gate abstentions. The only minor concern is one multi-hop question (Q010) where `gt_coverage` is reported as 0.75, suggesting slightly weaker coverage of the expected sources, but the answer is still grounded and semantically correct.

## Scores

| Dimension | Score (1-5) | Weight | Weighted |
|---|---:|---:|---:|
| Builder Quality | 5 | 25% | 1.25 |
| Retrieval Effectiveness | 5 | 25% | 1.25 |
| Answer Quality | 5 | 30% | 1.50 |
| Pipeline Health | 5 | 10% | 0.50 |
| Ablation Impact | 5 | 10% | 0.50 |
| **Overall** |  |  | **4.00** |

## Dimension Analysis

### 1. Builder Quality (5/5)
- `tables_parsed=7`, `tables_completed=7`, `all_tables_completed=true`
- `cypher_failed=false`, `failed_mappings=[]`, `ingestion_errors=[]`
- Triplet extraction density looks healthy (`triplets_extracted=94` across 7 tables; consistent with functioning KG construction).
- No builder skips (`builder_skipped=false`) and no ingestion/execute failures are reported.

**Verdict:** Meets the rubric’s top-tier criteria (all tables completed, no Cypher failures, no failed mappings).

### 2. Retrieval Effectiveness (5/5)
- `grounded_rate=1.0` and `avg_gt_coverage=0.9833` indicate expected evidence was nearly always retrieved.
- `avg_top_score=0.7867` is well within the healthy range for a cross-encoder reranker.
- `pipeline_health.questions_with_low_retrieval_score=0`
- `gate_abstentions=0` and there were **no** negative-question abstention errors (see Q013/Q014 below).

**Verdict:** Strong retrieval + correct gating behavior.

### 3. Answer Quality (5/5)
- `grounded_count=15`, `grounded_rate=1.0`
- `grader_rejection_count=0` for every per-question instance shown.
- Semantic correctness appears consistent with expected answers across direct-mapping and multi-hop queries.

Representative checks:
- **Q001 (customer fields):** Generated answer correctly enumerates the customer master fields including uniqueness/identity framing; grounded in CUSTOMER_MASTER/related.
- **Q006 (order statuses):** Correctly lists the five statuses (PENDING, CONFIRMED, SHIPPED, DELIVERED, CANCELLED).
- **Q013 (negative):** Correctly answers “No” to multi-category membership for a product and justifies from “belongs to exactly one category.”
- **Q014 (negative):** Correctly answers “Yes” about order existence without confirmed payment, aligning with nullable `PAYMENT_CONFIRMED_AT` and the business rule that shipping is gated rather than creation.

### 4. Pipeline Health (5/5)
- `total_grader_rejections=0`
- `grader_inconsistencies=0`
- `gate_abstentions=0`
- `cypher_failed=false`
- `failed_mappings_count=0`, `ingestion_errors_count=0`
- Latencies are reported as 0s in the bundle (likely instrumentation rounding), but functionally there are no stability issues reflected.

**Verdict:** Fully stable run; no self-healing or regeneration loops were necessary.

### 5. Ablation Impact (5/5)
- This bundle is AB-10, but it does **not** include an explicit `ablation_context` showing which flags differ from baseline AB-00.
- However, **the observed behavior is consistently strong** across builder/retrieval/answers and shows no regressions.
- Given the absence of contrary evidence and no sign of ablation-induced instability, we treat AB-10 as matching (or improving) the expected “good” behavior in a basics setting.

**Verdict:** No negative impact is detectable; scores align with a best-case outcome.

## Per-Question Deep Dive

### Q001: What information is stored for each customer?
- **Type:** direct_mapping | **Difficulty:** easy
- **Verdict:** CORRECT
- **Expected:** unique ID, full name, email (unique), region code, creation date, active status
- **Generated:** CUSTOMER_MASTER fields for CUST_ID, FULL_NAME, EMAIL, REGION_CODE, CREATED_AT, IS_ACTIVE; also references identity/PK intent
- **Analysis:** Matches expected fields; all grounding is consistent with retrieved CUSTOMER_MASTER context.
- **Retrieval:** gt_coverage=1.0, top_score=0.7, gate=proceed

### Q002: How are products categorized on the platform?
- **Type:** direct_mapping | **Difficulty:** easy
- **Verdict:** CORRECT
- **Expected:** product references exactly one category via CATEGORY_ID; categories have optional parent category (hierarchy)
- **Generated:** TB_PRODUCT.CATEGORY_ID → TB_CATEGORY(CATEGORY_ID) and PARENT_CATEGORY_ID self-reference
- **Analysis:** Correctly describes both “exactly one category per product” and hierarchy.
- **Retrieval:** gt_coverage=1.0, top_score=0.7, gate=proceed

### Q003: What is the relationship between customers and sales orders?
- **Type:** direct_mapping | **Difficulty:** easy
- **Verdict:** CORRECT
- **Expected:** each order placed by exactly one customer; customer has zero or more orders
- **Generated:** Sales order placed by exactly one customer via SALES_ORDER_HDR.CUST_ID → CUSTOMER_MASTER.CUST_ID
- **Analysis:** Correct cardinalities and join key.
- **Retrieval:** gt_coverage=1.0, top_score=0.9847, gate=proceed

### Q004: What does an order line item contain?
- **Type:** direct_mapping | **Difficulty:** easy
- **Verdict:** CORRECT
- **Expected:** product, quantity, unit price at purchase time, extended amount; each line belongs to one sales order
- **Generated:** PRODUCT_ID, QUANTITY, UNIT_PRICE, LINE_AMT (+ line and order identifiers)
- **Analysis:** Correct contents and linkage.
- **Retrieval:** gt_coverage=1.0, top_score=0.9765, gate=proceed

### Q005: How are payments linked to orders?
- **Type:** direct_mapping | **Difficulty:** easy
- **Verdict:** CORRECT
- **Expected:** payment associated to exactly one order via ORDER_ID foreign key; method/amount/status/timestamp
- **Generated:** PAYMENT.ORDER_ID → SALES_ORDER_HDR.ORDER_ID; confirms “references exactly one Sales Order”
- **Analysis:** Correct FK-based linkage and business rule alignment.
- **Retrieval:** gt_coverage=1.0, top_score=0.9501, gate=proceed

### Q006: What statuses can an order have?
- **Type:** attribute_lookup | **Difficulty:** easy
- **Verdict:** CORRECT
- **Expected:** PENDING, CONFIRMED, SHIPPED, DELIVERED, CANCELLED
- **Generated:** lists all five statuses
- **Analysis:** Exact set is correct.
- **Retrieval:** gt_coverage=1.0, top_score=0.7, gate=proceed

### Q007: Which table stores the product SKU information?
- **Type:** direct_mapping | **Difficulty:** easy
- **Verdict:** CORRECT
- **Expected:** TB_PRODUCT stores SKU
- **Generated:** TB_PRODUCT.SKU (and mentions related product attributes)
- **Analysis:** Correct table/column identification.
- **Retrieval:** gt_coverage=1.0, top_score=0.9845, gate=proceed

### Q008: How can I find all orders placed by a specific customer?
- **Type:** multi_hop | **Difficulty:** medium
- **Verdict:** CORRECT
- **Expected:** filter SALES_ORDER_HDR by CUST_ID; join to CUSTOMER_MASTER for details
- **Generated:** describes filtering/join path via CUSTOMER_MASTER.CUST_ID ↔ SALES_ORDER_HDR.CUST_ID
- **Analysis:** Correct multi-hop guidance.
- **Retrieval:** gt_coverage=1.0, top_score=0.7, gate=proceed

### Q009: How does the schema link orders to their individual product line items?
- **Type:** multi_hop | **Difficulty:** medium
- **Verdict:** CORRECT
- **Expected:** ORDER_LINE_ITEM links SALES_ORDER_HDR and TB_PRODUCT via ORDER_ID and PRODUCT_ID; includes QUANTITY/UNIT_PRICE/LINE_AMT
- **Generated:** correct junction table description and FK relations
- **Analysis:** Correct.
- **Retrieval:** gt_coverage=1.0, top_score=0.7, gate=proceed

### Q010: Show me the order hierarchy from customer to line items.
- **Type:** multi_hop | **Difficulty:** medium
- **Verdict:** CORRECT
- **Expected:** CUSTOMER_MASTER → SALES_ORDER_HDR → ORDER_LINE_ITEM → TB_PRODUCT
- **Generated:** describes customer→orders→line items via CUST_ID and ORDER_ID; mentions line-item reachability
- **Analysis:** Conceptually correct hierarchy; note that it focuses less on explicitly naming TB_PRODUCT in the join path, but expected key facts (line items connected to customer via order) are present. This aligns with `gt_coverage=0.75` yet remains semantically correct.
- **Retrieval:** gt_coverage=0.75, top_score=0.7, gate=proceed

### Q011: How does the schema model the confirmation state of a payment and its relationship to the order?
- **Type:** multi_hop | **Difficulty:** medium
- **Verdict:** CORRECT
- **Expected:** PAYMENT.CONFIRMED_AT + PAYMENT.STATUS_CODE; SALES_ORDER_HDR.PAYMENT_CONFIRMED_AT; order lifecycle via STATUS_CODE with CHECK constraint
- **Generated:** accurately describes PAYMENT.CONFIRMED_AT/STATUS_CODE and relationship via PAYMENT.ORDER_ID and also includes SALES_ORDER_HDR.PAYMENT_CONFIRMED_AT
- **Analysis:** Correct.
- **Retrieval:** gt_coverage=1.0, top_score=0.7, gate=proceed

### Q012: How are shipments related to orders and warehouses?
- **Type:** multi_hop | **Difficulty:** medium
- **Verdict:** CORRECT
- **Expected:** SHIPMENT.ORDER_ID → SALES_ORDER_HDR.ORDER_ID; includes warehouse code, tracking, status
- **Generated:** correct order association + warehouse association via SHIPMENT.WAREHOUSE_CODE; covers tracking/status conceptually
- **Analysis:** Correct.
- **Retrieval:** gt_coverage=1.0, top_score=0.9053, gate=proceed

### Q013: Can a product belong to multiple categories?
- **Type:** negative | **Difficulty:** easy
- **Verdict:** CORRECT
- **Expected:** No—belongs to exactly one category (CATEGORY_ID FK)
- **Generated:** “No,” cites product business rule and FK structure; notes absence of multi-category/junction mechanism
- **Analysis:** Correct handling of negative question; no fabrication.
- **Retrieval:** gt_coverage=1.0, top_score=0.7, gate=proceed

### Q014: Is it possible for a customer to place an order without payment?
- **Type:** negative | **Difficulty:** medium
- **Verdict:** CORRECT
- **Expected:** Yes; PAYMENT_CONFIRMED_AT nullable; order can exist pending payment, but shipping is blocked until payment confirmed
- **Generated:** “Yes,” explains nullable confirmation timestamp and clarifies that the business rule constrains shipping rather than order creation
- **Analysis:** Correct negative reasoning.
- **Retrieval:** gt_coverage=1.0, top_score=0.7, gate=proceed

### Q015: What schema fields support monetary value tracking across orders and their line items?
- **Type:** multi_hop | **Difficulty:** easy
- **Verdict:** CORRECT
- **Expected:** SALES_ORDER_HDR.TOTAL_AMT; ORDER_LINE_ITEM.UNIT_PRICE, QUANTITY, LINE_AMT (= qty×unit_price); linked by ORDER_ID
- **Generated:** correctly lists line-level monetary fields and notes linkage; also references PAYMENT.AMOUNT as settlement tracking
- **Analysis:** Expected parts are correct; extra correct info (payment settlement) is a plus.
- **Retrieval:** gt_coverage=1.0, top_score=0.7, gate=proceed

## Anomalies & Recommendations

### Red Flags
- None major. Specifically:
  - `grader_rejection_count=0` everywhere shown
  - `gate_abstentions=0`
  - `cypher_failed=false`, no ingestion issues
- The only mild anomaly is **Q010** where `gt_coverage=0.75` (notably lower than others), though the verdict remains correct.

### Recommendations
- For Q010-like queries, improve the query-time traversal/context distillation strategy so that **all expected hierarchy levels** (including TB_PRODUCT) are more consistently included when the question asks for a full hierarchy. This likely involves:
  - slightly increasing graph context allowance for multi-hop “hierarchy” questions, or
  - ensuring the context compressor preserves the final hop entities (product) when intermediate hops are already present.

## Comparison Notes (if applicable)
- The bundle does not include an `ablation_context` field or explicit “changes vs baseline AB-00,” so direct causal comparison to AB-00 isn’t possible from the provided JSON.
- Despite that, AB-10 exhibits best-case behavior on this basics dataset: full builder completion, strong retrieval scores, and perfect groundedness with zero grader rejections.