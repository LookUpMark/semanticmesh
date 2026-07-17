# AI-Judge Evaluation: AB-00/01_basics_ecommerce
**Evaluator:** (`gpt-5.4-nano-2026-03-17`) using `docs/AI_JUDGE_PROMPT.md`  
**Date:** 2026-07-17

---

# Ablation Study Evaluation: AB-00 — 01_basics_ecommerce

## Executive Summary
This baseline run (AB-00) shows an excellent end-to-end pipeline on the e-commerce basics dataset: the builder completed all tables with no Cypher/mapping failures, and the query graph retrieved and generated answers that are grounded for **all 15/15 questions**. Retrieval confidence is consistently high (avg top reranker score **0.78**), and there are **zero** grader rejections or pipeline health issues.

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
- `tables_completed = 7`, `all_tables_completed = true`
- `cypher_failed = false`, `failed_mappings = []`, `ingestion_errors = []`
- Triplet extraction present (`triplets_extracted = 112`) with healthy entity resolution (`entities_resolved = 76`)
- Builder health indicators fully meet the rubric’s score-5 criteria.

### 2. Retrieval Effectiveness (5/5)
- `grounded_rate = 1.0` and `avg_gt_coverage = 0.9833`
- `avg_top_score = 0.7813` (strong reranker confidence)
- `gate_abstentions = 0` and there are `0` questions with low retrieval score
- Even the lowest-quality observed per-question raw retrieval score values still correspond to grounded answers and correct semantics (e.g., Q002 / Q006 / Q011 / Q015), indicating retrieval did not miss required facts.

### 3. Answer Quality (5/5)
- `grounded_count = 15` and `grounded_rate = 1.0`
- Across direct-mapping and multi-hop queries, generated answers match the expected semantic facts (foreign keys, cardinalities, and attribute meanings).
- Negative questions are handled correctly in spirit:
  - Q013 (“multiple categories”) → correctly abstains from the possibility (answers “No” with correct FK rationale).
  - Q014 (“order without payment”) → the answer asserts “Yes” based on nullable `PAYMENT_CONFIRMED_AT`, consistent with the provided expected reasoning that the system allows orders prior to payment confirmation (and payment is a prerequisite for shipping, not necessarily order creation).
- No grader rejections (`grader_rejection_count` is 0 for every shown question), supporting that the model did not hallucinate facts beyond grounded context.

### 4. Pipeline Health (5/5)
- `total_grader_rejections = 0`
- `grader_inconsistencies = 0`
- `gate_abstentions = 0`
- `cypher_failed = false`, `ingestion_errors_count = 0`
- This indicates stability: no self-healing loops were needed for Cypher, and generation passed hallucination grading every time.

### 5. Ablation Impact (N/A)
- `study_id = AB-00` implies baseline; no “changes vs baseline” are applicable.

## Per-Question Deep Dive

### Q001: What information is stored for each customer?
- **Type:** direct_mapping | **Difficulty:** easy  
- **Verdict:** CORRECT  
- **Expected:** customer ID, full name, email (unique), region code, creation date, active status  
- **Generated:** correctly identifies `CUSTOMER_MASTER` as the source; mentions primary key `CUST_ID` and fields like `created_at` and `region_code`, plus activation status and contact identity.  
- **Analysis:** Correct semantic coverage; grounded in retrieved glossary/table columns.  
- **Retrieval:** gt_coverage=1.0, top_score=0.7068, gate=proceed

### Q002: How are products categorized on the platform?
- **Type:** direct_mapping | **Difficulty:** easy  
- **Verdict:** CORRECT  
- **Expected:** hierarchy via `PARENT_CATEGORY_ID`; each product references exactly one category through `CATEGORY_ID`  
- **Generated:** matches hierarchy and FK semantics between `TB_PRODUCT` and `TB_CATEGORY`.  
- **Analysis:** Properly explains one-category-per-product and the self-referencing category tree.  
- **Retrieval:** gt_coverage=1.0, top_score=0.7, gate=proceed

### Q003: What is the relationship between customers and sales orders?
- **Type:** direct_mapping | **Difficulty:** easy  
- **Verdict:** CORRECT  
- **Expected:** each sales order placed by exactly one customer; customer can have zero or more orders  
- **Generated:** matches “exactly one” via `sales_order_hdr.cust_id -> customer_master.cust_id` and “zero or more” at customer level.  
- **Analysis:** Correct cardinalities and FK mapping.  
- **Retrieval:** gt_coverage=1.0, top_score=0.9847, gate=proceed

### Q004: What does an order line item contain?
- **Type:** direct_mapping | **Difficulty:** easy  
- **Verdict:** CORRECT  
- **Expected:** product, quantity, unit price at time of purchase, and extended amount; belongs to exactly one sales order  
- **Generated:** covers product, quantity, unit_price, and extended amount; grounded in order line item concepts.  
- **Analysis:** Correct attribute set and extended amount rule.  
- **Retrieval:** gt_coverage=1.0, top_score=0.9933, gate=proceed

### Q005: How are payments linked to orders?
- **Type:** direct_mapping | **Difficulty:** easy  
- **Verdict:** CORRECT  
- **Expected:** each payment linked to exactly one sales order via `ORDER_ID`; includes method, amount, status, confirmation timestamp  
- **Generated:** correctly explains the FK relationship and references payment business concept fields.  
- **Analysis:** Semantically aligned with expected linkage.  
- **Retrieval:** gt_coverage=1.0, top_score=0.9333, gate=proceed

### Q006: What statuses can an order have?
- **Type:** attribute_lookup | **Difficulty:** easy  
- **Verdict:** CORRECT  
- **Expected:** PENDING, CONFIRMED, SHIPPED, DELIVERED, CANCELLED  
- **Generated:** lists exactly those five statuses from sales order concept context.  
- **Analysis:** Complete and correct enumerations.  
- **Retrieval:** gt_coverage=1.0, top_score=0.7, gate=proceed

### Q007: Which table stores the product SKU information?
- **Type:** direct_mapping | **Difficulty:** easy  
- **Verdict:** CORRECT  
- **Expected:** TB_PRODUCT stores SKU  
- **Generated:** states `tb_product` stores SKU and describes it as part of product catalog identifiers.  
- **Analysis:** Correct table-level mapping.  
- **Retrieval:** gt_coverage=1.0, top_score=0.9814, gate=proceed

### Q008: How can I find all orders placed by a specific customer?
- **Type:** multi_hop | **Difficulty:** medium  
- **Verdict:** CORRECT  
- **Expected:** filter/join SALES_ORDER_HDR on CUST_ID referencing CUSTOMER_MASTER.CUST_ID  
- **Generated:** explains filtering or joining by CUST_ID and lists key fields returned.  
- **Analysis:** Correct multi-hop join path and relevant attributes.  
- **Retrieval:** gt_coverage=1.0, top_score=0.7, gate=proceed

### Q009: How does the schema link orders to their individual product line items?
- **Type:** multi_hop | **Difficulty:** medium  
- **Verdict:** CORRECT  
- **Expected:** ORDER_LINE_ITEM links SALES_ORDER_HDR and TB_PRODUCT; contains ORDER_ID, PRODUCT_ID, quantity, unit_price, line_amt  
- **Generated:** correctly describes FK bridge using `order_line_item.ORDER_ID -> sales_order_hdr.ORDER_ID` and `PRODUCT_ID -> TB_PRODUCT.PRODUCT_ID`.  
- **Analysis:** Correct structural explanation (junction/bridge).  
- **Retrieval:** gt_coverage=1.0, top_score=0.7, gate=proceed

### Q010: Show me the order hierarchy from customer to line items.
- **Type:** multi_hop | **Difficulty:** medium  
- **Verdict:** CORRECT  
- **Expected:** CUSTOMER_MASTER → SALES_ORDER_HDR → ORDER_LINE_ITEM → TB_PRODUCT  
- **Generated:** matches hierarchy and FK directions; correctly identifies line-item fields.  
- **Analysis:** Proper hierarchy and column semantics.  
- **Retrieval:** gt_coverage=0.75, top_score=0.7, gate=proceed

### Q011: How does the schema model the confirmation state of a payment and its relationship to the order?
- **Type:** multi_hop | **Difficulty:** medium  
- **Verdict:** CORRECT  
- **Expected:** PAYMENT.CONFIRMED_AT nullable; PAYMENT.STATUS_CODE lifecycle; order has SALES_ORDER_HDR.PAYMENT_CONFIRMED_AT; order status lifecycle too  
- **Generated:** explains confirmation timestamp/status in payment context and order-level `payment_confirmed_at` mirror; preserves “payment belongs to exactly one sales order.”  
- **Analysis:** Correct modeling of dual confirmation representations.  
- **Retrieval:** gt_coverage=1.0, top_score=0.7, gate=proceed

### Q012: How are shipments related to orders and warehouses?
- **Type:** multi_hop | **Difficulty:** medium  
- **Verdict:** CORRECT  
- **Expected:** SHIPMENT.ORDER_ID → SALES_ORDER_HDR.ORDER_ID; includes warehouse source, tracking, status  
- **Generated:** correctly states shipment-to-order cardinality and describes warehouse source + tracking/status fields.  
- **Analysis:** Correct multi-hop semantics based on shipment business definition.  
- **Retrieval:** gt_coverage=1.0, top_score=0.8203, gate=proceed

### Q013: Can a product belong to multiple categories?
- **Type:** negative | **Difficulty:** easy  
- **Verdict:** CORRECT  
- **Expected:** No; product has exactly one category via CATEGORY_ID FK to TB_CATEGORY  
- **Generated:** answers “No” and correctly cites “belongs to exactly one category” + FK rationale.  
- **Analysis:** Correct negative handling and alignment with expected.  
- **Retrieval:** gt_coverage=1.0, top_score=0.7, gate=proceed

### Q014: Is it possible for a customer to place an order without payment?
- **Type:** negative | **Difficulty:** medium  
- **Verdict:** CORRECT  
- **Expected:** Yes; PAYMENT_CONFIRMED_AT nullable; business rule is payment must be confirmed before shipping (not necessarily before order record exists)  
- **Generated:** argues “Yes” using nullable `SALES_ORDER_HDR.PAYMENT_CONFIRMED_AT` and foreign-key non-requirement for immediate payment row existence; ties to “payment before ships.”  
- **Analysis:** Correct interpretation consistent with expected answer’s logic.  
- **Retrieval:** gt_coverage=1.0, top_score=0.7, gate=proceed

### Q015: What schema fields support monetary value tracking across orders and their line items?
- **Type:** multi_hop | **Difficulty:** easy  
- **Verdict:** CORRECT  
- **Expected:** SALES_ORDER_HDR.TOTAL_AMT for header; ORDER_LINE_ITEM UNIT_PRICE, QUANTITY, LINE_AMT (= QUANTITY×UNIT_PRICE) for line items; join via ORDER_ID  
- **Generated:** correctly describes LINE_AMT/UNIT_PRICE/QUANTITY logic and links conceptually to order totals; mentions PAYMENT.amount for reconciliation as extra.  
- **Analysis:** Correctly covers core expected fields for order vs line items; extra payment linkage is not harmful.  
- **Retrieval:** gt_coverage=1.0, top_score=0.7, gate=proceed

## Anomalies & Recommendations

### Red Flags
- None. No abstentions, no grader rejections, and no builder failures.

### Recommendations
- Since this is baseline-perfect on basics, focus next ablations on regimes that stress weaknesses noted in the system prompt (e.g., multi-hop with paraphrase-heavy queries, negative questions requiring abstention, and ER edge cases that can over-merge similar entity names).
- Track whether retrieval_quality_score_raw consistently aligns with adjusted values; in this run, some raw scores appear lower than adjusted (pool-confidence application), so validating that the quality gate thresholding remains robust under ablations would be useful.

## Comparison Notes (if applicable)
- Baseline AB-00: no ablation changes to compare against. The run meets or exceeds score-5 rubric thresholds across all major dimensions.