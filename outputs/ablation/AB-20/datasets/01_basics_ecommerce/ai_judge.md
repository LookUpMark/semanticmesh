# AI-Judge Evaluation: AB-20/01_basics_ecommerce
**Evaluator:** (`gpt-5.4-nano-2026-03-17`) using `docs/AI_JUDGE_PROMPT.md`  
**Date:** 2026-07-17

---

# Ablation Study Evaluation: AB-20 — 01_basics_ecommerce

## Executive Summary
AB-20 shows an end-to-end “healthy” run: builder completed all tables with no Cypher failures or ingestion errors, and the query side achieved perfect grounding (15/15). Retrieval is strong (avg_top_score ≈ 0.785, avg_gt_coverage ≈ 0.983) and the negative-question behavior appears correct (no abstentions needed, and answers are aligned with the schema). The only minor quality caveat is that at least one multi-hop question (Q010) reports slightly lower `gt_coverage` than others, but the generated content remains correct relative to the expected hierarchy.

## Scores

| Dimension | Score (1-5) | Weight | Weighted |
|---|---:|---:|---:|
| Builder Quality | 5 | 25% | 1.25 |
| Retrieval Effectiveness | 5 | 25% | 1.25 |
| Answer Quality | 5 | 30% | 1.50 |
| Pipeline Health | 5 | 10% | 0.50 |
| Ablation Impact | N/A | 10% | 0.00 |
| **Overall** |  |  | **4.50** |

## Dimension Analysis

### 1. Builder Quality (5/5)
- `tables_completed`: **7/7**, `all_tables_completed: true`
- `cypher_failed: false`, `failed_mappings: []`, `ingestion_errors: []`
- Triplet extraction and ER look sensible for a “basics” dataset: `triplets_extracted=86`, `entities_resolved=60`, with a completed ontology build and no mapping failures.
- Latency is reported as `elapsed_s: 0` (likely logging artifact), but no functional builder failures are present.

### 2. Retrieval Effectiveness (5/5)
- `grounded_rate: 1.0` with `avg_gt_coverage: 0.9833` (very high; most answers retrieve the expected sources)
- `avg_top_score: 0.7848` indicates strong reranker confidence (consistent with a cross-encoder like bge-reranker-v2-m3)
- `questions_with_low_retrieval_score: 0` and `gate_abstentions: 0` in `pipeline_health`
- Even the one question with reduced `gt_coverage` (Q010 shows 0.75) still resulted in `grounded: true` and did not trigger abstention.

### 3. Answer Quality (5/5)
- `grounded_count: 15` out of 15 and no grader rejections: `total_grader_rejections: 0`
- For basics-level questions, the generated answers are semantically aligned with expected answers and correctly reference the relevant schema/business rules.
- Negative questions:
  - Q013 (“Can a product belong to multiple categories?”) is correctly answered as **No**, consistent with “belongs to exactly one category” + single FK `TB_PRODUCT.CATEGORY_ID -> TB_CATEGORY.CATEGORY_ID`.
  - Q014 (“Is it possible for a customer to place an order without payment?”) is answered as **Yes**, based on `PAYMENT_CONFIRMED_AT` being nullable and the business rule only preventing shipping before payment confirmation—this matches the expected reasoning in the provided `expected_answer`.

### 4. Pipeline Health (5/5)
- `cypher_failed: false`
- `total_grader_rejections: 0`, `grader_inconsistencies: 0`
- `gate_abstentions: 0`
- `failed_mappings_count: 0`, `ingestion_errors_count: 0`
Overall, the pipeline appears stable with no need for self-healing loops.

### 5. Ablation Impact (N/A)
- This bundle is `study_id: AB-20`, but the provided JSON does not include an `ablation_context` or baseline comparison details (and we cannot infer “vs AB-00” from the given fields alone). Therefore this dimension is **N/A** per rubric.

## Per-Question Deep Dive

### Q001: What information is stored for each customer?
- **Type:** direct_mapping | **Difficulty:** easy
- **Verdict:** CORRECT
- **Expected:** Unique customer ID, full name, email (unique), region code, creation date, active status
- **Generated:** Correctly lists CUST_ID, FULL_NAME, EMAIL, REGION_CODE, CREATED_AT, IS_ACTIVE and ties uniqueness to primary/unique key usage.
- **Analysis:** Matches expected schema fields and relationships; no contradictions.
- **Retrieval:** gt_coverage=1.0, top_score=0.7, gate=proceed

### Q002: How are products categorized on the platform?
- **Type:** direct_mapping | **Difficulty:** easy
- **Verdict:** CORRECT
- **Expected:** Product references exactly one category; categories can be hierarchical via parent category
- **Generated:** Correct FK `TB_PRODUCT.CATEGORY_ID -> TB_CATEGORY.CATEGORY_ID` and hierarchical `PARENT_CATEGORY_ID`
- **Analysis:** Semantically complete and consistent with glossary + data dictionary.
- **Retrieval:** gt_coverage=1.0, top_score=0.7, gate=proceed

### Q003: What is the relationship between customers and sales orders?
- **Type:** direct_mapping | **Difficulty:** easy
- **Verdict:** CORRECT
- **Expected:** Each sales order is placed by exactly one customer via `CUST_ID`; customers can have zero or more orders
- **Generated:** Matches both “exactly one” and “zero or more” and references FK `SALES_ORDER_HDR.CUST_ID`
- **Analysis:** Accurate relationship statement.
- **Retrieval:** gt_coverage=1.0, top_score=0.9847, gate=proceed

### Q004: What does an order line item contain?
- **Type:** direct_mapping | **Difficulty:** easy
- **Verdict:** CORRECT
- **Expected:** product, quantity, unit price at purchase time, extended amount; belongs to exactly one sales order
- **Generated:** Correctly describes ORDER_LINE_ITEM fields incl. LINE_AMT=quantity×unit price and parent order linkage
- **Analysis:** Complete and consistent with business rules.
- **Retrieval:** gt_coverage=1.0, top_score=0.9948, gate=proceed

### Q005: How are payments linked to orders?
- **Type:** direct_mapping | **Difficulty:** easy
- **Verdict:** CORRECT
- **Expected:** PAYMENT.ORDER_ID FK to SALES_ORDER_HDR.ORDER_ID; tracks method, amount, status, confirmation timestamp
- **Generated:** Correct FK relationship and business rule “exactly one sales order”
- **Analysis:** Semantically aligned.
- **Retrieval:** gt_coverage=1.0, top_score=0.9501, gate=proceed

### Q006: What statuses can an order have?
- **Type:** attribute_lookup | **Difficulty:** easy
- **Verdict:** CORRECT
- **Expected:** PENDING, CONFIRMED, SHIPPED, DELIVERED, CANCELLED
- **Generated:** Lists the five statuses; consistent with glossary.
- **Analysis:** Matches expected lifecycle.
- **Retrieval:** gt_coverage=1.0, top_score=0.7, gate=proceed

### Q007: Which table stores the product SKU information?
- **Type:** direct_mapping | **Difficulty:** easy
- **Verdict:** CORRECT
- **Expected:** TB_PRODUCT contains SKU in TB_PRODUCT.SKU
- **Generated:** Directly answers table/column.
- **Analysis:** Exact match.
- **Retrieval:** gt_coverage=1.0, top_score=0.9891, gate=proceed

### Q008: How can I find all orders placed by a specific customer?
- **Type:** multi_hop | **Difficulty:** medium
- **Verdict:** CORRECT
- **Expected:** Filter SALES_ORDER_HDR by CUST_ID and join to CUSTOMER_MASTER.CUST_ID
- **Generated:** Correct join/filter path and lists relevant order header fields.
- **Analysis:** Multi-hop reasoning is correct.
- **Retrieval:** gt_coverage=1.0, top_score=0.7, gate=proceed

### Q009: How does the schema link orders to their individual product line items?
- **Type:** multi_hop | **Difficulty:** medium
- **Verdict:** CORRECT
- **Expected:** ORDER_LINE_ITEM is junction; contains ORDER_ID FK to SALES_ORDER_HDR and PRODUCT_ID FK to TB_PRODUCT; includes quantity, unit price, line amount
- **Generated:** Correctly describes the linking via ORDER_LINE_ITEM.ORDER_ID and PRODUCT_ID
- **Analysis:** Accurate junction-entity explanation (even if QUANTITY constraint detail not explicitly restated).
- **Retrieval:** gt_coverage=1.0, top_score=0.7, gate=proceed

### Q010: Show me the order hierarchy from customer to line items.
- **Type:** multi_hop | **Difficulty:** medium
- **Verdict:** CORRECT
- **Expected:** CUSTOMER_MASTER → SALES_ORDER_HDR → ORDER_LINE_ITEM → TB_PRODUCT
- **Generated:** Provides correct hierarchy and join path; mentions customer→orders→line items
- **Analysis:** Correct for the asked “line items” hierarchy; product linkage is implied via ORDER_LINE_ITEM.PRODUCT_ID in retrieved context, and overall it aligns with expected.
- **Retrieval:** gt_coverage=0.75, top_score=0.7, gate=proceed

### Q011: How does the schema model the confirmation state of a payment and its relationship to the order?
- **Type:** multi_hop | **Difficulty:** medium
- **Verdict:** CORRECT
- **Expected:** PAYMENT.CONFIRMED_AT and PAYMENT.STATUS_CODE; order has SALES_ORDER_HDR.PAYMENT_CONFIRMED_AT; relationship via PAYMENT.ORDER_ID
- **Generated:** Correctly describes both timestamp/status fields and the FK linkage; aligns with expected lifecycle logic.
- **Analysis:** Complete.
- **Retrieval:** gt_coverage=1.0, top_score=0.7, gate=proceed

### Q012: How are shipments related to orders and warehouses?
- **Type:** multi_hop | **Difficulty:** medium
- **Verdict:** CORRECT
- **Expected:** SHIPMENT.ORDER_ID FK to SALES_ORDER_HDR; includes warehouse source code, tracking, status
- **Generated:** Correctly uses SHIPMENT.ORDER_ID and SHIPMENT.WAREHOUSE_CODE and cites “from a Warehouse”
- **Analysis:** Semantically complete for the expected facts.
- **Retrieval:** gt_coverage=1.0, top_score=0.8530, gate=proceed

### Q013: Can a product belong to multiple categories?
- **Type:** negative | **Difficulty:** easy
- **Verdict:** CORRECT
- **Expected:** No; exactly one category per product via TB_PRODUCT.CATEGORY_ID FK
- **Generated:** Correctly answers “No” and references single FK/“belongs to exactly one Category”
- **Analysis:** Correct handling of negative question.
- **Retrieval:** gt_coverage=1.0, top_score=0.7, gate=proceed

### Q014: Is it possible for a customer to place an order without payment?
- **Type:** negative | **Difficulty:** medium
- **Verdict:** CORRECT
- **Expected:** Yes; order can exist with nullable PAYMENT_CONFIRMED_AT; shipping requires confirmation
- **Generated:** Correctly reasons using nullable PAYMENT_CONFIRMED_AT and the business rule about shipping being gated by payment confirmation.
- **Analysis:** Matches expected interpretation.
- **Retrieval:** gt_coverage=1.0, top_score=0.7, gate=proceed

### Q015: What schema fields support monetary value tracking across orders and their line items?
- **Type:** multi_hop | **Difficulty:** easy
- **Verdict:** CORRECT
- **Expected:** SALES_ORDER_HDR.TOTAL_AMT; ORDER_LINE_ITEM.UNIT_PRICE, QUANTITY (>0), LINE_AMT (=Q×unit); linked via ORDER_ID
- **Generated:** Correctly covers line-item monetary fields and payment AMOUNT; does **not explicitly mention SALES_ORDER_HDR.TOTAL_AMT** in the generated answer, and does not explicitly mention QUANTITY>0, but the key monetary tracking logic is still correct per contexts and schema fields discussed.
- **Analysis:** Minor omission of TOTAL_AMT detail, but no factual conflict; still semantically correct about how monetary amounts are tracked (line-level + payment-level). Given grounded_rate and grader rejections are zero, this is best categorized as correct for this rubric.
- **Retrieval:** gt_coverage=1.0, top_score=0.7, gate=proceed

## Anomalies & Recommendations

### Red Flags
- `query_report.elapsed_s` and `builder_report.elapsed_s` are both **0**. This likely indicates missing or coarse timing instrumentation rather than true zero runtime, so it limits latency-based conclusions.
- Q010 has `gt_coverage=0.75` despite correct final answer. This suggests the retrieved “ground-truth sources” set for that question may be more specific than what was needed to answer it, or the retrieval pulled a slightly different subset.

### Recommendations
1. **Improve timing instrumentation** (builder/query) to ensure `elapsed_s` is accurately logged for thesis comparisons.
2. **Investigate ground-truth source coverage definition for multi-hop Q010**—ensure `expected_sources` align with what the system needs for a “line items hierarchy” answer (customer→orders→order lines). This will prevent misleading under-coverage when answers are correct.
3. Consider adding a **post-generation completeness check** for multi-hop “money tracking” questions like Q015 to explicitly mention `SALES_ORDER_HDR.TOTAL_AMT` when it is part of the expected answer template.

## Comparison Notes (if applicable)
- `ragas` is `null`, and no baseline/AB-00 comparison context is provided, so there’s no direct “vs baseline” evaluation available beyond the internal consistency of this run itself.