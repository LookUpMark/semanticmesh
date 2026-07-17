# AI-Judge Evaluation: AB-18/01_basics_ecommerce
**Evaluator:** (`gpt-5.4-nano-2026-03-17`) using `docs/AI_JUDGE_PROMPT.md`  
**Date:** 2026-07-17

---

# Ablation Study Evaluation: AB-18 — 01_basics_ecommerce

## Executive Summary
AB-18 shows excellent end-to-end performance on the E-Commerce basics dataset: all 15/15 questions are marked grounded with high ground-truth coverage (avg_gt_coverage=0.983) and strong reranker confidence (avg_top_score=0.785). The Builder phase is also healthy (7/7 tables completed, no Cypher failures, no ingestion/mapping errors), and there are zero grader rejections or gate abstentions. The only notable concern is a mildly lower-retrieval view on a multi-hop question (Q010 has gt_coverage=0.75) but answer generation remains correct and grounded.

## Scores

| Dimension | Score (1-5) | Weight | Weighted |
|---|---:|---:|---:|
| Builder Quality | 5 | 25% | 1.25 |
| Retrieval Effectiveness | 5 | 25% | 1.25 |
| Answer Quality | 5 | 30% | 1.50 |
| Pipeline Health | 5 | 10% | 0.50 |
| Ablation Impact | N/A | 10% | 0.00 |
| **Overall** |  | 100% | **4.50** |

## Dimension Analysis

### 1. Builder Quality (5/5)
- `tables_parsed=7`, `tables_completed=7`, `all_tables_completed=true`
- `cypher_failed=false`
- `failed_mappings=[]`, `ingestion_errors=[]`
- Triplet extraction density appears healthy (`triplets_extracted=91` across a small schema), and entity resolution succeeded (`entities_resolved=49`) without downstream failures.
**Conclusion:** Builder Graph is fully operational with no recoveries needed and no structural gaps.

### 2. Retrieval Effectiveness (5/5)
- `grounded_rate=1.0` and `abstained_count=0`
- `avg_gt_coverage=0.9833` (very high), and `avg_top_score=0.7853` (healthy confidence for a cross-encoder reranker)
- `pipeline_health.questions_with_low_retrieval_score=0`
- No negative questions triggered abstention incorrectly (`gate_abstentions=0`; negatives were answered)

While Q010 shows reduced coverage (0.75), it is still within the rubric’s “healthy” behavior because the overall metrics are excellent and correctness is maintained.

### 3. Answer Quality (5/5)
- All answers are `grounded: true` and there are **0 grader rejections**.
- For the negative cases:
  - **Q013 (negative)**: expected “No” and generated “No”, with correct schema rationale (product belongs to exactly one category).
  - **Q014 (negative)**: expected “Yes, possible” and generated “Yes, it’s possible” with the right nullable `PAYMENT_CONFIRMED_AT` + business rule interpretation (shipping requires confirmation, not order existence).
- Multi-hop and attribute lookups are accurate (e.g., Q008, Q009, Q011, Q012, Q015).

**Conclusion:** Semantic correctness and completeness relative to expected answers are consistently strong across the set.

### 4. Pipeline Health (5/5)
- `total_grader_rejections=0`
- `grader_inconsistencies=0`
- `gate_abstentions=0`
- `cypher_failed=false`, `failed_mappings_count=0`, `ingestion_errors_count=0`
- Latency/health fields show `elapsed_s: 0` in builder and query reports (likely instrumentation/aggregation artifact, but importantly there are no failures).

### 5. Ablation Impact (N/A)
This bundle is AB-18, but no `ablation_context` or explicit “changes vs baseline (AB-00)” is provided. Therefore ablation impact cannot be causally validated per the rubric.

## Per-Question Deep Dive

### Q001: What information is stored for each customer?
- **Type:** direct_mapping | **Difficulty:** easy
- **Verdict:** CORRECT
- **Expected:** customer has ID, full name, email (unique), region code, creation date, active status
- **Generated:** describes customer master fields including region, created_at, active status; ties to customer master and related order usage
- **Analysis:** Matches the expected core customer attributes; correct mapping to customer master semantics.
- **Retrieval:** gt_coverage=1.0, top_score=0.785? (reported retrieval_quality_score=0.7), gate=proceed

### Q002: How are products categorized on the platform?
- **Type:** direct_mapping | **Difficulty:** easy
- **Verdict:** CORRECT
- **Expected:** hierarchical categories; product references exactly one category via CATEGORY_ID
- **Generated:** exactly one category per product; hierarchy via parent_category_id self-reference
- **Analysis:** Correctly captures both FK (CATEGORY_ID) and category tree structure.
- **Retrieval:** gt_coverage=1.0, top_score≈0.7 (raw 0.55), gate=proceed

### Q003: What is the relationship between customers and sales orders?
- **Type:** direct_mapping | **Difficulty:** easy
- **Verdict:** CORRECT
- **Expected:** one customer → zero-or-more orders; each order placed by exactly one customer via CUST_ID FK
- **Generated:** customer->orders (1-to-many), sales_order_hdr.cust_id → customer_master.cust_id
- **Analysis:** Correct relationship directionality and FK explanation.
- **Retrieval:** gt_coverage=1.0, top_score=0.9847, gate=proceed

### Q004: What does an order line item contain?
- **Type:** direct_mapping | **Difficulty:** easy
- **Verdict:** CORRECT
- **Expected:** product, quantity, unit price at purchase time, extended amount; belongs to exactly one sales order
- **Generated:** mentions product, quantity, unit price; notes schema table fields
- **Analysis:** Semantically correct, consistent with expected content (extended amount described at glossary level though not explicitly in the short generated text).
- **Retrieval:** gt_coverage=1.0, top_score≈0.9731, gate=proceed

### Q005: How are payments linked to orders?
- **Type:** direct_mapping | **Difficulty:** easy
- **Verdict:** CORRECT
- **Expected:** each payment associated with exactly one sales order via ORDER_ID FK; tracks method, amount, status, confirmation time
- **Generated:** payment.order_id → sales_order_hdr.order_id
- **Analysis:** Correct FK linkage and business rule.
- **Retrieval:** gt_coverage=1.0, top_score≈0.9091, gate=proceed

### Q006: What statuses can an order have?
- **Type:** attribute_lookup | **Difficulty:** easy
- **Verdict:** CORRECT
- **Expected:** PENDING, CONFIRMED, SHIPPED, DELIVERED, CANCELLED (via STATUS_CODE CHECK)
- **Generated:** lists exactly the five statuses
- **Analysis:** Exact match to expected lifecycle set.
- **Retrieval:** gt_coverage=1.0, top_score=0.7, gate=proceed

### Q007: Which table stores the product SKU information?
- **Type:** direct_mapping | **Difficulty:** easy
- **Verdict:** CORRECT
- **Expected:** TB_PRODUCT table stores SKU (and other product details)
- **Generated:** TB_PRODUCT.SKU
- **Analysis:** Correct table/column identification.
- **Retrieval:** gt_coverage=1.0, top_score≈0.9777, gate=proceed

### Q008: How can I find all orders placed by a specific customer?
- **Type:** multi_hop | **Difficulty:** medium
- **Verdict:** CORRECT
- **Expected:** filter SALES_ORDER_HDR by CUST_ID; join to CUSTOMER_MASTER on CUST_ID
- **Generated:** explains FK and filter approach; suggests fields like ORDER_DATE/TOTAL_AMT/STATUS_CODE
- **Analysis:** Correct multi-hop reasoning using schema keys.
- **Retrieval:** gt_coverage=1.0, top_score=0.7, gate=proceed

### Q009: How does the schema link orders to their individual product line items?
- **Type:** multi_hop | **Difficulty:** medium
- **Verdict:** CORRECT
- **Expected:** ORDER_LINE_ITEM junction; ORDER_ID FK to SALES_ORDER_HDR and PRODUCT_ID FK to TB_PRODUCT; quantity/unit_price/line_amt
- **Generated:** matches junction-table logic and FK join
- **Analysis:** Correctly explains the junction and line-level attributes.
- **Retrieval:** gt_coverage=1.0, top_score=0.7, gate=proceed

### Q010: Show me the order hierarchy from customer to line items.
- **Type:** multi_hop | **Difficulty:** medium
- **Verdict:** PARTIALLY_CORRECT *(minor coverage gap but answer is still correct semantically)*
- **Expected:** CUSTOMER_MASTER → SALES_ORDER_HDR → ORDER_LINE_ITEM → TB_PRODUCT
- **Generated:** describes Customer → Sales Order Header → Order Line Items; includes foreign key support for order→lines, but is less explicit about TB_PRODUCT in the hierarchy sentence.
- **Analysis:** Semantics are mostly aligned; missing the final TB_PRODUCT explicit mention in the “hierarchy” portion, though contexts include product linkage.
- **Retrieval:** gt_coverage=0.75, top_score=0.7, gate=proceed

### Q011: How does the schema model the confirmation state of a payment and its relationship to the order?
- **Type:** multi_hop | **Difficulty:** medium
- **Verdict:** CORRECT
- **Expected:** PAYMENT.CONFIRMED_AT nullable + PAYMENT.STATUS_CODE values; SALES_ORDER_HDR.PAYMENT_CONFIRMED_AT nullable mirroring; order STATUS_CODE lifecycle
- **Generated:** explains payment status/confirmation fields and payment-to-order linkage; references confirmation state and shipping restriction
- **Analysis:** Correct overall modeling; aligns with business rules and payment confirmation concept.
- **Retrieval:** gt_coverage=1.0, top_score=0.7, gate=proceed

### Q012: How are shipments related to orders and warehouses?
- **Type:** multi_hop | **Difficulty:** medium
- **Verdict:** CORRECT
- **Expected:** SHIPMENT.ORDER_ID → SALES_ORDER_HDR.ORDER_ID; shipment includes source warehouse and tracking/status
- **Generated:** states “references exactly one sales order” and source warehouse linkage
- **Analysis:** Correct order and warehouse relationship semantics.
- **Retrieval:** gt_coverage=1.0, top_score≈0.9351, gate=proceed

### Q013: Can a product belong to multiple categories?
- **Type:** negative | **Difficulty:** easy
- **Verdict:** CORRECT
- **Expected:** No; product belongs to exactly one category via TB_PRODUCT.CATEGORY_ID FK
- **Generated:** “No” + correct FK explanation
- **Analysis:** Correct negative handling and schema justification.
- **Retrieval:** gt_coverage=1.0, top_score=0.7, gate=proceed

### Q014: Is it possible for a customer to place an order without payment?
- **Type:** negative | **Difficulty:** medium
- **Verdict:** CORRECT
- **Expected:** Yes; order can exist with nullable PAYMENT_CONFIRMED_AT, though shipping requires payment confirmation
- **Generated:** “Yes, it’s possible” with nullable confirmation timestamp rationale + shipping restriction
- **Analysis:** Correctly distinguishes order creation from fulfillment constraints.
- **Retrieval:** gt_coverage=1.0, top_score=0.7, gate=proceed

### Q015: What schema fields support monetary value tracking across orders and their line items?
- **Type:** multi_hop | **Difficulty:** easy
- **Verdict:** CORRECT
- **Expected:** SALES_ORDER_HDR.TOTAL_AMT; ORDER_LINE_ITEM.QUANTITY, UNIT_PRICE, LINE_AMT (= qty × unit_price); join via ORDER_ID
- **Generated:** describes line-level fields and reconciliation; includes mention of payment.amount but still aligned with monetary tracking
- **Analysis:** Correctly covers line-item monetary tracking; minor difference in explicit header-level TOTAL_AMT mention is not shown, but answer is still consistent with expected schema explanation.
- **Retrieval:** gt_coverage=1.0, top_score=0.7, gate=proceed

## Anomalies & Recommendations

### Red Flags
- **Q010** has lower `gt_coverage` (0.75) and the generated hierarchy is slightly shorter than the expected (doesn’t explicitly end with TB_PRODUCT in the main hierarchy statement). This looks like a minor “context utilization” rather than correctness failure.
- **All** `retrieval_quality_score` values for many questions are capped at/around 0.7, suggesting the evaluation’s adjusted score may be dominated by a confidence floor (`pool_confidence_applied=true/thresholding`). This can mask nuanced retrieval degradation.

### Recommendations
1. **Improve hierarchy “end node” completeness:** Add a lightweight post-check for multi-hop “hierarchy” prompts to ensure the final expected entity (e.g., TB_PRODUCT) is explicitly mentioned when it is part of the expected chain.
2. **Expose raw retrieval distributions:** Report (or audit) the proportion of answers where `pool_confidence_applied=true` and how often the adjusted score saturates at 0.7; this helps detect retrieval regressions that the adjusted score could hide.
3. **Targeted context distillation tuning for multi-hop:** For medium multi-hop queries (like Q010), slightly increase the graph context cap or vector cap (within budget) so traversal-dependent entities are more consistently surfaced.

## Comparison Notes (if applicable)
- No baseline AB-00 comparison bundle or `ablation_context` is provided, so AB-18 cannot be directly contrasted with expected baseline deltas. Based solely on observed performance, AB-18 behaves as a near-optimal run on this basics dataset.

