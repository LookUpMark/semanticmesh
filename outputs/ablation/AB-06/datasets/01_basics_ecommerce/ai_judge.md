# AI-Judge Evaluation: AB-06/01_basics_ecommerce
**Evaluator:** (`gpt-5.4-nano-2026-03-17`) using `docs/AI_JUDGE_PROMPT.md`  
**Date:** 2026-07-17

---

# Ablation Study Evaluation: AB-06 — 01_basics_ecommerce

## Executive Summary
AB-06 shows excellent end-to-end behavior on the “basics/ecommerce” dataset: builder completed all 7 tables with no Cypher failures or ingestion/mapping errors, and the query stage produced grounded answers for all 15 questions (grounded_rate=1.0) with strong retrieval confidence (avg_top_score≈0.789). No grader rejections or gate abstentions occurred, so the run is very stable; the main “concern” is that the retrieval quality gate did not surface any low-retrieval situations at all (which is consistent with the dataset being easy).

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
- `cypher_failed=false`
- `failed_mappings=[]`, `ingestion_errors=[]`
- Triplet extraction is healthy (`triplets_extracted=116`) for a small dataset; ER count is reasonable (`entities_resolved=89`).

### 2. Retrieval Effectiveness (5/5)
- `grounded_rate=1.0`, `avg_gt_coverage=1.0`
- `avg_top_score=0.789` (well within “healthy” range for cross-encoder reranker confidence)
- `questions_with_low_retrieval_score=0` and `gate_abstentions=0`
- Negative questions (Q013, Q014) were handled correctly via explicit “No”/“Yes” content rather than false abstention.

### 3. Answer Quality (5/5)
- All questions are marked grounded (`grounded=true` for each shown item) and there are **zero** hallucination rejections (`grader_rejection_count=0` everywhere).
- The generated answers closely match the expected semantics, including:
  - Customer field list (Q001)
  - Product category hierarchy (Q002)
  - Customer↔orders relationship (Q003)
  - Order line item composition including extended amount (Q004)
  - Payment→order linkage (Q005)
  - Order status lifecycle (Q006)
  - Product SKU stored in TB_PRODUCT.SKU (Q007)
  - Multi-hop join guidance customer→orders (Q008)
  - Order hierarchy (Q010)
  - Payment confirmation logic and related order timestamp (Q011)
  - Shipment→order and shipment→warehouse aspects (Q012)
  - Negative: product belongs to exactly one category (Q013)
  - Negative: whether orders can exist without payment (Q014) — answered correctly with the glossary constraint about shipping vs payment confirmation
  - Monetary fields across header/lines (Q015)

### 4. Pipeline Health (5/5)
- `pipeline_health.total_grader_rejections=0`
- `grader_inconsistencies=0`, `gate_abstentions=0`
- `cypher_failed=false`, `failed_mappings_count=0`, `ingestion_errors_count=0`
- Latency fields are effectively zero in the bundle (`elapsed_s=0` for builder/query), which suggests a controlled/small run; importantly, there are no operational failures recorded.

### 5. Ablation Impact (N/A)
- The rubric instructs to use this dimension only when the study is not baseline (`AB-00`) **and** meaningful baseline-vs-ablation deltas are provided (e.g., `ablation_context.changes_vs_baseline`).  
- This bundle does not include `ablation_context`, nor does it clearly specify which flags were changed relative to AB-00. Therefore: **N/A**.

## Per-Question Deep Dive

### Q001: What information is stored for each customer?
- **Type:** direct_mapping | **Difficulty:** easy
- **Verdict:** CORRECT
- **Expected:** unique ID, full name, email (unique), region code, creation date, active status
- **Generated:** lists CUST_ID, FULL_NAME, EMAIL, REGION_CODE, IS_ACTIVE, CREATED_AT; notes CUSTOMER_MASTER fields in schema
- **Analysis:** Matches expected customer attribute set and aligns with schema descriptions.
- **Retrieval:** gt_coverage=1.0, top_score=0.7, gate=proceed

### Q002: How are products categorized on the platform?
- **Type:** direct_mapping | **Difficulty:** easy
- **Verdict:** CORRECT
- **Expected:** each product references exactly one category; category can have parent for hierarchy
- **Generated:** TB_PRODUCT.CATEGORY_ID FK to TB_CATEGORY; self-referencing parent via PARENT_CATEGORY_ID
- **Analysis:** Correctly captures “exactly one” and hierarchy mechanism.
- **Retrieval:** gt_coverage=1.0, top_score=0.7, gate=proceed

### Q003: What is the relationship between customers and sales orders?
- **Type:** direct_mapping | **Difficulty:** easy
- **Verdict:** CORRECT
- **Expected:** sales orders placed by exactly one customer via CUST_ID FK; customer can have zero or more orders
- **Generated:** states 0..* orders per customer; explicit FK SALES_ORDER_HDR.CUST_ID → CUSTOMER_MASTER.CUST_ID
- **Analysis:** Correct relational semantics.
- **Retrieval:** gt_coverage=1.0, top_score=0.9847, gate=proceed

### Q004: What does an order line item contain?
- **Type:** direct_mapping | **Difficulty:** easy
- **Verdict:** CORRECT
- **Expected:** product, quantity, unit price at purchase time, extended amount; belongs to exactly one order
- **Generated:** specifies product, QUANTITY, UNIT_PRICE, LINE_AMT; includes ORDER_LINE_ITEM belongs to a Sales Order
- **Analysis:** Correct composition; extended amount included via LINE_AMT.
- **Retrieval:** gt_coverage=1.0, top_score=0.9943, gate=proceed

### Q005: How are payments linked to orders?
- **Type:** direct_mapping | **Difficulty:** easy
- **Verdict:** CORRECT
- **Expected:** Payment references exactly one sales order via ORDER_ID FK; includes method/amount/status/confirmation
- **Generated:** states PAYMENT.ORDER_ID FK to SALES_ORDER_HDR.ORDER_ID; includes status/method timestamps context
- **Analysis:** Correct linkage and attributes.
- **Retrieval:** gt_coverage=1.0, top_score=0.9501, gate=proceed

### Q006: What statuses can an order have?
- **Type:** attribute_lookup | **Difficulty:** easy
- **Verdict:** CORRECT
- **Expected:** PENDING, CONFIRMED, SHIPPED, DELIVERED, CANCELLED
- **Generated:** lists exactly those five.
- **Analysis:** Exact match to expected lifecycle.
- **Retrieval:** gt_coverage=1.0, top_score=0.7, gate=proceed

### Q007: Which table stores the product SKU information?
- **Type:** direct_mapping | **Difficulty:** easy
- **Verdict:** CORRECT
- **Expected:** TB_PRODUCT stores SKU in SKU column
- **Generated:** “TB_PRODUCT.SKU” correct
- **Analysis:** Direct and correct.
- **Retrieval:** gt_coverage=1.0, top_score=0.9890, gate=proceed

### Q008: How can I find all orders placed by a specific customer?
- **Type:** multi_hop | **Difficulty:** medium
- **Verdict:** CORRECT
- **Expected:** filter SALES_ORDER_HDR by CUST_ID; join to CUSTOMER_MASTER on CUST_ID
- **Generated:** explains filtering SALES_ORDER_HDR.CUST_ID and optional join to CUSTOMER_MASTER
- **Analysis:** Correct join path and intent.
- **Retrieval:** gt_coverage=1.0, top_score=0.7, gate=proceed

### Q009: How does the schema link orders to their individual product line items?
- **Type:** multi_hop | **Difficulty:** medium
- **Verdict:** CORRECT
- **Expected:** ORDER_LINE_ITEM is junction; contains ORDER_ID and PRODUCT_ID; includes QUANTITY/UNIT_PRICE/LINE_AMT
- **Generated:** describes ORDER_LINE_ITEM and both FKs (ORDER_ID→SALES_ORDER_HDR, PRODUCT_ID→TB_PRODUCT)
- **Analysis:** Correct junction model.
- **Retrieval:** gt_coverage=1.0, top_score=0.7, gate=proceed

### Q010: Show me the order hierarchy from customer to line items.
- **Type:** multi_hop | **Difficulty:** medium
- **Verdict:** CORRECT
- **Expected:** CUSTOMER_MASTER → SALES_ORDER_HDR → ORDER_LINE_ITEM → TB_PRODUCT
- **Generated:** describes same hierarchy and key FK steps
- **Analysis:** Correct multi-hop hierarchy.
- **Retrieval:** gt_coverage=1.0, top_score=0.7, gate=proceed

### Q011: How does the schema model the confirmation state of a payment and its relationship to the order?
- **Type:** multi_hop | **Difficulty:** medium
- **Verdict:** CORRECT
- **Expected:** PAYMENT.CONFIRMED_AT nullable; PAYMENT.STATUS_CODE values; order-level SALES_ORDER_HDR.PAYMENT_CONFIRMED_AT mirrors; order lifecycle includes PENDING/CONFIRMED/SHIPPED/DELIVERED/CANCELLED
- **Generated:** covers PAYMENT.STATUS_CODE + CONFIRMED_AT and PAYMENT.ORDER_ID→SALES_ORDER_HDR.ORDER_ID; includes SALES_ORDER_HDR.PAYMENT_CONFIRMED_AT
- **Analysis:** Matches expected modeling intent.
- **Retrieval:** gt_coverage=1.0, top_score=0.7, gate=proceed

### Q012: How are shipments related to orders and warehouses?
- **Type:** multi_hop | **Difficulty:** medium
- **Verdict:** CORRECT
- **Expected:** SHIPMENT.ORDER_ID → SALES_ORDER_HDR; shipment includes warehouse code, tracking, status
- **Generated:** explains SHIPMENT.ORDER_ID linkage and SHIPMENT.WAREHOUSE_CODE/source warehouse notion
- **Analysis:** Correct order and warehouse relationship.
- **Retrieval:** gt_coverage=1.0, top_score=0.9179, gate=proceed

### Q013: Can a product belong to multiple categories?
- **Type:** negative | **Difficulty:** easy
- **Verdict:** CORRECT
- **Expected:** No; TB_PRODUCT has single CATEGORY_ID FK to TB_CATEGORY
- **Generated:** “No” with exactly-one-category rule via CATEGORY_ID FK
- **Analysis:** Correct negative handling and reasoning.
- **Retrieval:** gt_coverage=1.0, top_score=0.7, gate=proceed

### Q014: Is it possible for a customer to place an order without payment?
- **Type:** negative | **Difficulty:** medium
- **Verdict:** CORRECT
- **Expected:** Yes order can exist; PAYMENT_CONFIRMED_AT nullable; shipping requires confirmation
- **Generated:** “Yes” and distinguishes order creation vs shipping constraint
- **Analysis:** Correct nuance for negative question.
- **Retrieval:** gt_coverage=1.0, top_score=0.7, gate=proceed

### Q015: What schema fields support monetary value tracking across orders and their line items?
- **Type:** multi_hop | **Difficulty:** easy
- **Verdict:** CORRECT
- **Expected:** header TOTAL_AMT plus line UNIT_PRICE/QUANTITY/LINE_AMT; linked via ORDER_ID
- **Generated:** discusses line UNIT_PRICE and LINE_AMT and ties via ORDER_ID→order; also discusses payment AMOUNT (relevant but not contradicting)
- **Analysis:** Uses correct monetary fields at line level and maintains schema linkage; extra mention of PAYMENT.AMOUNT is not harmful.
- **Retrieval:** gt_coverage=1.0, top_score=0.7, gate=proceed

## Anomalies & Recommendations

### Red Flags
- **None major.** Key risk signals (ungrounded answers, hallucination grader rejections, gate abstentions, Cypher failures) are all zero.

### Recommendations
- Even though this run is flawless, consider adding/using more “harder” datasets or paraphrase-stressing queries to ensure the retrieval quality gate and multi-hop traversal remain robust under lower top-score conditions (this bundle shows no degradation scenario).
- For negative questions, you’re already correct; to further validate abstention policy, introduce negative queries where the KG truly lacks the answer (so the system must abstain or explicitly state absence).

## Comparison Notes (if applicable)
- No baseline (AB-00) bundle or `ablation_context` was provided, so no causal comparison can be made.