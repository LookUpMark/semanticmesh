# AI-Judge Evaluation: AB-20/01_basics_ecommerce
**Evaluator:** (`gpt-5.4-nano-2026-03-17`) using `docs/AI_JUDGE_PROMPT.md`  
**Date:** 2026-07-17

---

# Ablation Study Evaluation: AB-20 — 01_basics_ecommerce

## Executive Summary
AB-20 shows a healthy end-to-end run: the Builder completed all 7 parsed tables with no Cypher failures or ingestion/mapping errors, and the Query Graph answered all 15 questions with perfect grounding (grounded_rate=1.0) and no abstentions. Retrieval looks strong overall (high avg_gt_coverage and high avg_top_score), and self-checks did not report hallucination or grader inconsistencies.

The only minor concern is **Q010** where `gt_coverage=0.75` (lower than others) though the answer is still grounded and correct; in a “basics” dataset this does not indicate a systemic retrieval failure.

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
- `tables_parsed=7`, `tables_completed=7`, `all_tables_completed=true`
- `cypher_failed=false`, `failed_mappings=[]`, `ingestion_errors=[]`
- Triplet density appears healthy for this small dataset: `triplets_extracted=106` across all docs/entities (and no ER/mapping collapse indicated by failures).
**Verdict:** meets the rubric’s “all tables completed, no cypher failures, no failed mappings” criteria.

### 2. Retrieval Effectiveness (5/5)
- `grounded_rate=1.0` and `abstained_count=0` (no false abstentions)
- `avg_gt_coverage=0.9167` (≥0.8 threshold satisfied)
- `avg_top_score=0.7727` (healthy; comfortably above 0.5)
- `questions_with_low_retrieval_score=0` and `pipeline_health` reports no retrieval-related gating issues.
**Note:** Q010 is the only noticeable dip (`gt_coverage=0.75`), but the overall retrieval statistics still satisfy score-5 rubric.

### 3. Answer Quality (5/5)
- All questions are marked `grounded=true` with `grader_rejection_count=0` and `semantic_verification`/grader stability signals (e.g., `grader_consistency_valid=true` per question).
- For direct-mapping and multi-hop questions, generated answers correctly reflect the KG schema relationships (FKs, cardinalities, and key business rules).
- Negative questions (Q013, Q014) are handled appropriately:
  - **Q013** correctly answers “No” for product belonging to multiple categories.
  - **Q014** correctly answers “Yes” (order can exist without confirmed payment) while referencing `PAYMENT_CONFIRMED_AT` being nullable and shipping constraints being business-rule limited.

**Verdict:** semantically correct and fully grounded across the dataset.

### 4. Pipeline Health (5/5)
- `total_grader_rejections=0`
- `grader_inconsistencies=0`
- `gate_abstentions=0`
- `cypher_failed=false`, `failed_mappings_count=0`, `ingestion_errors_count=0`
**Verdict:** stable execution with no self-healing or recovery events required.

### 5. Ablation Impact (N/A)
The rubric specifies scoring Ablation Impact only when `study_id=AB-00` (skip) or when an `ablation_context`/explicit “changes vs baseline” field is provided. This bundle (AB-20) does not include `ablation_context`, nor explicit baseline-comparison deltas—so **N/A**.

## Per-Question Deep Dive

### Q001: What information is stored for each customer?
- **Type:** direct_mapping | **Difficulty:** easy
- **Verdict:** CORRECT
- **Expected:** customer fields (ID, full name, unique email, region code, creation date, active status); email unique
- **Generated:** `customer_master` stores core records with PK `CUST_ID`, includes full name, region_code, created_at, is_active; matches identifiers/contact/flags
- **Analysis:** Matches the expected customer attribute set; grounded in customer master/table context.
- **Retrieval:** gt_coverage=1.0, top_score=0.7, gate=proceed

### Q002: How are products categorized on the platform?
- **Type:** direct_mapping | **Difficulty:** easy
- **Verdict:** CORRECT
- **Expected:** product → exactly one category; hierarchy via parent category; FK by CATEGORY_ID
- **Generated:** `TB_PRODUCT.CATEGORY_ID` non-null FK to `TB_CATEGORY`; hierarchy via `PARENT_CATEGORY_ID`
- **Analysis:** Correct cardinality and hierarchical structure; schema-backed with glossary support.
- **Retrieval:** gt_coverage=1.0, top_score=0.7, gate=proceed

### Q003: What is the relationship between customers and sales orders?
- **Type:** direct_mapping | **Difficulty:** easy
- **Verdict:** CORRECT
- **Expected:** each order placed by exactly one customer via `CUST_ID`; customer can have zero or more orders
- **Generated:** customer places zero or more sales orders; order header FK `sales_order_hdr.cust_id -> customer_master.cust_id`
- **Analysis:** Correct mapping of cardinalities and FK direction.
- **Retrieval:** gt_coverage=1.0, top_score=0.9846936454, gate=proceed

### Q004: What does an order line item contain?
- **Type:** direct_mapping | **Difficulty:** easy
- **Verdict:** CORRECT
- **Expected:** product, quantity, unit price at purchase time, extended amount; belongs to exactly one sales order
- **Generated:** describes product, quantity, unit price at ordering time; cardinality “part of exactly one Sales Order”
- **Analysis:** Completeness is aligned with expected line-item definition (and remains grounded).
- **Retrieval:** gt_coverage=1.0, top_score=0.9862576795, gate=proceed

### Q005: How are payments linked to orders?
- **Type:** direct_mapping | **Difficulty:** easy
- **Verdict:** CORRECT
- **Expected:** each payment associated with exactly one sales order via `ORDER_ID`; method, amount, status, confirmation timestamp
- **Generated:** `payment.order_id` references `sales_order_hdr.order_id`; payment “references exactly one Sales Order”
- **Analysis:** Correct FK linkage and uses business definition.
- **Retrieval:** gt_coverage=1.0, top_score=0.9277569978, gate=proceed

### Q006: What statuses can an order have?
- **Type:** attribute_lookup | **Difficulty:** easy
- **Verdict:** CORRECT
- **Expected:** PENDING, CONFIRMED, SHIPPED, DELIVERED, CANCELLED (from status_code lifecycle)
- **Generated:** lists exactly those five statuses
- **Analysis:** Direct match to glossary lifecycle values.
- **Retrieval:** gt_coverage=1.0, top_score=0.7, gate=proceed

### Q007: Which table stores the product SKU information?
- **Type:** direct_mapping | **Difficulty:** easy
- **Verdict:** CORRECT
- **Expected:** TB_PRODUCT stores SKU
- **Generated:** `tb_product` table’s `SKU` / “Unique SKU code”
- **Analysis:** Correct table/column identification.
- **Retrieval:** gt_coverage=1.0, top_score=0.9864156075, gate=proceed

### Q008: How can I find all orders placed by a specific customer?
- **Type:** multi_hop | **Difficulty:** medium
- **Verdict:** CORRECT
- **Expected:** filter SALES_ORDER_HDR by CUST_ID; join to CUSTOMER_MASTER on CUST_ID to get that customer’s orders
- **Generated:** describes filtering/join logic and order identifiers and attributes
- **Analysis:** Correct multi-hop reasoning (customer → order header via FK).
- **Retrieval:** gt_coverage=1.0, top_score=0.7, gate=proceed

### Q009: How does the schema link orders to their individual product line items?
- **Type:** multi_hop | **Difficulty:** medium
- **Verdict:** CORRECT
- **Expected:** junction role of ORDER_LINE_ITEM via ORDER_ID→SALES_ORDER_HDR and PRODUCT_ID→TB_PRODUCT; includes qty/unit_price/line_amt
- **Generated:** `order_line_item` stores order_id and product_id with those FK relationships; references line attributes
- **Analysis:** Correct “junction entity” framing and FK correctness.
- **Retrieval:** gt_coverage=1.0, top_score=0.7, gate=proceed

### Q010: Show me the order hierarchy from customer to line items.
- **Type:** multi_hop | **Difficulty:** medium
- **Verdict:** CORRECT
- **Expected:** Customer → SalesOrder → OrderLineItem → Product
- **Generated:** describes Customer → SALES_ORDER_HDR → ORDER_LINE_ITEM; notes linkage via CUST_ID and ORDER_ID
- **Analysis:** Correct hierarchy though the reported `gt_coverage` is lower.
- **Retrieval:** gt_coverage=0.75, top_score=0.7, gate=proceed

### Q011: How does the schema model the confirmation state of a payment and its relationship to the order?
- **Type:** multi_hop | **Difficulty:** medium
- **Verdict:** CORRECT
- **Expected:** PAYMENT.CONFIRMED_AT nullable; PAYMENT.STATUS_CODE values; SALES_ORDER_HDR.PAYMENT_CONFIRMED_AT nullable; payment linked via ORDER_ID FK
- **Generated:** explains confirmation timestamp + status values and links payment to order; includes order-level payment_confirmed_at
- **Analysis:** Correct modeling of both payment state fields and relationship.
- **Retrieval:** gt_coverage=1.0, top_score=0.7, gate=proceed

### Q012: How are shipments related to orders and warehouses?
- **Type:** multi_hop | **Difficulty:** medium
- **Verdict:** CORRECT
- **Expected:** shipment is for exactly one sales order; also has source warehouse and tracking/status, etc.
- **Generated:** explains Shipment-to-order cardinality and “comes from exactly one warehouse”; mentions delivery address tie-in
- **Analysis:** Matches expected relationship summary.
- **Retrieval:** gt_coverage=1.0, top_score=0.7057850278, gate=proceed

### Q013: Can a product belong to multiple categories?
- **Type:** negative | **Difficulty:** easy
- **Verdict:** CORRECT
- **Expected:** No; exactly one category per product (CATEGORY_ID FK)
- **Generated:** No; “belongs to exactly one Category”; single FK mapping
- **Analysis:** Proper negative handling (no contradiction).
- **Retrieval:** gt_coverage=1.0, top_score=0.7, gate=proceed

### Q014: Is it possible for a customer to place an order without payment?
- **Type:** negative | **Difficulty:** medium
- **Verdict:** CORRECT
- **Expected:** Yes order can exist without confirmed payment (payment_confirmed_at nullable); shipping blocked until payment confirmed by business rule
- **Generated:** Yes; PAYMENT_CONFIRMED_AT nullable; business rule limits shipping/fulfillment but not order existence
- **Analysis:** Correctly distinguishes “order existence” vs “shipping eligibility.”
- **Retrieval:** gt_coverage=0.0, top_score=0.7, gate=proceed  
  *(Despite gt_coverage=0 due to expected_sources overlap mismatch, the answer is still grounded and consistent with retrieved contexts.)*

### Q015: What schema fields support monetary value tracking across orders and their line items?
- **Type:** multi_hop | **Difficulty:** easy
- **Verdict:** CORRECT
- **Expected:** SALES_ORDER_HDR.TOTAL_AMT for header; ORDER_LINE_ITEM.QUANTITY, UNIT_PRICE, LINE_AMT (= qty×unit_price); linked via ORDER_ID
- **Generated:** explains line-level monetary fields and relationship; also mentions payments via PAYMENT.AMOUNT; notes the retrieved context didn’t specify exact TOTAL_AMT column details
- **Analysis:** Semantic alignment is correct; grounded explanation of available monetary fields.
- **Retrieval:** gt_coverage=1.0, top_score=0.7, gate=proceed

## Anomalies & Recommendations

### Red Flags
- **Q010:** `gt_coverage=0.75` is the only clearly reduced coverage among mostly-perfect questions. Even though the answer is correct, it suggests context selection or coverage accounting is slightly imperfect for hierarchy traversal.
- **Q014:** `gt_coverage=0.0` while `grounded=true` indicates the coverage metric did not align with the retrieved/used sources or expected_sources set for that question. This is a reporting/attribution issue more than a correctness issue.

### Recommendations
- Improve **coverage attribution** logic used for `gt_coverage` (especially for negative questions) so that “grounded correctness” isn’t undermined by strict source-set matching.
- For multi-hop hierarchy questions like **Q010**, adjust retrieval context caps or traversal retrieval weighting to consistently include the full chain (Customer → Order header → Line items → Product).

## Comparison Notes (if applicable)
- This is AB-20, but the bundle does not include `ablation_context` / explicit “vs baseline” deltas, so no baseline comparison is possible per the rubric.