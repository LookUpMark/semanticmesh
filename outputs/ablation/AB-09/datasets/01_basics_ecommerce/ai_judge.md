# AI-Judge Evaluation: AB-09/01_basics_ecommerce
**Evaluator:** (`gpt-5.4-nano-2026-03-17`) using `docs/AI_JUDGE_PROMPT.md`  
**Date:** 2026-07-17

---

# Ablation Study Evaluation: AB-09 — 01_basics_ecommerce

## Executive Summary
AB-09 shows excellent overall system behavior on the E-Commerce basics dataset: the builder completed all tables with no Cypher failures or ingestion errors, and the query side achieved 100% grounded answers with very high retrieval coverage (avg_gt_coverage=0.95) and strong reranker confidence (avg_top_score≈0.79). The only minor concern is that one multi-hop query (Q008) has notably lower ground-truth coverage (0.5), suggesting occasional retrieval dilution, but it did not impact grounded correctness.

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
- `tables_parsed`: 7, `tables_completed`: 7, `all_tables_completed`: **true**
- `cypher_failed`: **false**
- `failed_mappings`: **[]**, `ingestion_errors`: **[]**
- Triplet extraction is strong: `triplets_extracted`=69 with `entities_resolved`=36 (no signs of extreme under/over extraction failure)
- Builder runtime is effectively absent (`elapsed_s`: 0), but no health indicators contradict correctness.

### 2. Retrieval Effectiveness (4/5)
Key signals:
- `grounded_rate`: **1.0**, `abstained_count`: **0** (no incorrect abstentions)
- `avg_gt_coverage`: **0.95** (excellent)
- `avg_top_score`: **0.787** (healthy for a bge-reranker-v2-m3 setup)
- One clear outlier: **Q008** has `gt_coverage=0.5` while still answering correctly. This suggests retrieval could be improved for that multi-hop pattern, but it was not catastrophic.

Given the rubric, the run meets score-5 on most retrieval indicators except for that single question-level coverage drop; hence **4/5** rather than 5/5.

### 3. Answer Quality (5/5)
- `query_report.grounded_rate = 1.0`: all answers are verifiably grounded in retrieved context.
- No hallucination detections:
  - `total_grader_rejections`: 0
  - Every provided per-question shows `grader_rejection_count: 0`
- Negative questions are handled correctly:
  - **Q013 (negative)**: “Can a product belong to multiple categories?” → correctly answered **No**
  - **Q014 (negative)**: “Is it possible for a customer to place an order without payment?” → answered consistently with nullable `PAYMENT_CONFIRMED_AT` semantics (“possible” but shipping restricted)

Top/bottom exemplar checks:
- Best (Q003): `retrieval_quality_score`≈0.985, fully correct relationship framing.
- Worst (Q008): Despite `gt_coverage=0.5`, the generated answer correctly explains filtering/joining between `SALES_ORDER_HDR` and `CUSTOMER_MASTER` and does not introduce contradictions.

### 4. Pipeline Health (5/5)
- `total_grader_rejections`: **0**
- `grader_inconsistencies`: 0
- `gate_abstentions`: 0
- `cypher_failed`: false; `failed_mappings_count`: 0; `ingestion_errors_count`: 0  
Overall: stable and clean run with no recovery loops needed.

### 5. Ablation Impact (N/A)
This bundle is AB-09, but the provided bundle does not include an `ablation_context.changes_vs_baseline` field nor explicit “vs baseline” flag differences. Therefore, ablation impact cannot be assessed per rubric.

## Per-Question Deep Dive

### Q001: What information is stored for each customer?
- **Type:** direct_mapping | **Difficulty:** easy  
- **Verdict:** CORRECT
- **Expected:** Customer has ID, full name, email (unique), region code, creation date, active status
- **Generated:** Describes CUSTOMER_MASTER fields (CUST_ID, FULL_NAME, EMAIL, REGION_CODE, CREATED_AT, IS_ACTIVE) with correct types/nullable semantics
- **Analysis:** Matches expected customer attribute set and key constraints; no extra incorrect claims
- **Retrieval:** gt_coverage=1.0, top_score=0.7, gate=proceed

### Q002: How are products categorized on the platform?
- **Verdict:** CORRECT
- **Expected:** product references exactly one category; category has parent/child hierarchy
- **Generated:** Explains TB_PRODUCT.CATEGORY_ID → TB_CATEGORY.CATEGORY_ID and TB_CATEGORY.PARENT_CATEGORY_ID self-reference
- **Analysis:** Correct hierarchy and single-category per product rule
- **Retrieval:** gt_coverage=1.0, top_score=0.7, gate=proceed

### Q003: What is the relationship between customers and sales orders?
- **Verdict:** CORRECT
- **Expected:** one customer places many orders over time; each order placed by exactly one customer
- **Generated:** SALES_ORDER_HDR.CUST_ID → CUSTOMER_MASTER.CUST_ID plus “0 or more” orders per customer
- **Analysis:** Correct cardinality and foreign-key rationale
- **Retrieval:** gt_coverage=1.0, top_score=0.9847097286, gate=proceed

### Q004: What does an order line item contain?
- **Verdict:** CORRECT
- **Expected:** product, quantity, unit price at time of purchase, extended amount; belongs to exactly one sales order
- **Generated:** Includes LINE_ID, ORDER_ID, PRODUCT_ID, QUANTITY, UNIT_PRICE, LINE_AMT; quantity×unit price logic
- **Analysis:** Fully aligned with expected line-item content
- **Retrieval:** gt_coverage=1.0, top_score=0.9845636397, gate=proceed

### Q005: How are payments linked to orders?
- **Verdict:** CORRECT
- **Expected:** one payment associated with exactly one sales order via ORDER_ID foreign key
- **Generated:** PAYMENT.ORDER_ID → SALES_ORDER_HDR.ORDER_ID; also mentions “exactly one sales order” semantic
- **Analysis:** Correct linkage and relationship explanation
- **Retrieval:** gt_coverage=1.0, top_score=0.9500523382, gate=proceed

### Q006: What statuses can an order have?
- **Verdict:** CORRECT
- **Expected:** PENDING, CONFIRMED, SHIPPED, DELIVERED, CANCELLED (via STATUS_CODE lifecycle)
- **Generated:** Lists all five statuses
- **Analysis:** Correct lifecycle set
- **Retrieval:** gt_coverage=1.0, top_score=0.7, gate=proceed

### Q007: Which table stores the product SKU information?
- **Verdict:** CORRECT
- **Expected:** TB_PRODUCT stores SKU (plus other product fields)
- **Generated:** TB_PRODUCT.SKU, and context includes SKU semantics
- **Analysis:** Exact table/column mapping
- **Retrieval:** gt_coverage=1.0, top_score=0.9852004506, gate=proceed

### Q008: How can I find all orders placed by a specific customer?
- **Verdict:** CORRECT
- **Expected:** filter SALES_ORDER_HDR by CUST_ID and join to CUSTOMER_MASTER on CUST_ID for customer details
- **Generated:** Explains WHERE on SALES_ORDER_HDR.CUST_ID = customer’s CUST_ID and optional join for FULL_NAME/EMAIL
- **Analysis:** Correct multi-hop retrieval intent despite diluted gt coverage
- **Retrieval:** gt_coverage=0.5, top_score=0.7, gate=proceed

### Q009: How does the schema link orders to their individual product line items?
- **Verdict:** CORRECT
- **Expected:** ORDER_LINE_ITEM junction with ORDER_ID → SALES_ORDER_HDR and PRODUCT_ID → TB_PRODUCT; includes QUANTITY, UNIT_PRICE, LINE_AMT
- **Generated:** Correctly explains both foreign keys and line item role
- **Analysis:** Matches expected schema modeling
- **Retrieval:** gt_coverage=1.0, top_score=0.7, gate=proceed

### Q010: Show me the order hierarchy from customer to line items.
- **Verdict:** CORRECT
- **Expected:** CUSTOMER → SALES_ORDER_HDR → ORDER_LINE_ITEM → TB_PRODUCT
- **Generated:** Implements via foreign-key links on CUST_ID, ORDER_ID, PRODUCT_ID
- **Analysis:** Correct hierarchy and join path description
- **Retrieval:** gt_coverage=0.75, top_score=0.7, gate=proceed

### Q011: How does the schema model the confirmation state of a payment and its relationship to the order?
- **Verdict:** CORRECT
- **Expected:** PAYMENT.CONFIRMED_AT + PAYMENT.STATUS_CODE; SALES_ORDER_HDR.PAYMENT_CONFIRMED_AT mirrors; PAYMENT linked to order via ORDER_ID
- **Generated:** Describes both confirmation fields and “payment confirmed before shipping” lifecycle; links via PAYMENT.ORDER_ID
- **Analysis:** Correct modeling of confirmation state and linkage
- **Retrieval:** gt_coverage=1.0, top_score=0.7, gate=proceed

### Q012: How are shipments related to orders and warehouses?
- **Verdict:** CORRECT
- **Expected:** SHIPMENT.ORDER_ID → SALES_ORDER_HDR; shipment has source warehouse via SHIPMENT.WAREHOUSE_CODE; includes tracking/status/delivery info
- **Generated:** Explains SHIPMENT belongs to one order and comes from exactly one warehouse; mentions corresponding fields
- **Analysis:** Correct relationships; no missing cardinality/field logic
- **Retrieval:** gt_coverage=1.0, top_score=0.90758112497, gate=proceed

### Q013: Can a product belong to multiple categories?
- **Type:** negative | **Difficulty:** easy  
- **Verdict:** CORRECT
- **Expected:** No; TB_PRODUCT has single CATEGORY_ID FK to TB_CATEGORY
- **Generated:** “No” with CATEGORY_ID → TB_CATEGORY.CATEGORY_ID and single-category statement
- **Analysis:** Correct negative handling consistent with schema
- **Retrieval:** gt_coverage=1.0, top_score=0.7, gate=proceed

### Q014: Is it possible for a customer to place an order without payment?
- **Type:** negative | **Difficulty:** medium  
- **Verdict:** CORRECT
- **Expected:** Yes possible to exist before confirmation (PAYMENT_CONFIRMED_AT nullable), but not shippable until payment confirmed
- **Generated:** “Yes” based on nullable PAYMENT_CONFIRMED_AT; clarifies constraint applies to shipping not order creation
- **Analysis:** Correct interpretation of negative question using nullable semantics
- **Retrieval:** gt_coverage=1.0, top_score=0.7, gate=proceed

### Q015: What schema fields support monetary value tracking across orders and their line items?
- **Verdict:** CORRECT
- **Expected:** TOTAL_AMT at order header; UNIT_PRICE, QUANTITY, LINE_AMT at line level; reconcile via ORDER_ID
- **Generated:** Correctly explains line-level UNIT_PRICE and LINE_AMT and links via ORDER_ID; notes order-level total conceptually as “Total monetary value”; also mentions payment amount field (PAYMENT.AMOUNT)
- **Analysis:** Semantically correct and grounded; extra mention of payment is acceptable
- **Retrieval:** gt_coverage=1.0, top_score=0.7, gate=proceed

## Anomalies & Recommendations

### Red Flags
- **Q008** shows `gt_coverage=0.5` and still outputs a correct answer. This indicates retrieval may sometimes surface irrelevant but distractor-rich contexts (e.g., shipment-related info) even when the final answer remains correct. Not a failure, but a robustness gap.

### Recommendations
- Add a targeted retrieval-quality calibration for multi-hop “filter + optional join” patterns (like “orders by customer”), ensuring the system strongly prioritizes `SALES_ORDER_HDR` and `CUSTOMER_MASTER` contexts over adjacent order lifecycle entities (e.g., Shipment).
- Consider tightening the context distillation caps or adding a small graph-traversal boost specifically when the query mentions “orders placed by customer” (i.e., emphasize CUST_ID adjacency to SALES_ORDER_HDR).
- Keep the negative-question behavior as-is; Q013/Q014 are handled correctly (suggests the abstention/gating and groundedness checks are functioning well).

## Comparison Notes (if applicable)
- `ragas` is `null`, so there are no RAGAS metrics to compare.
- No explicit “vs baseline” configuration changes are provided beyond the AB-09 identifier; thus no causal comparison can be performed under the rubric.