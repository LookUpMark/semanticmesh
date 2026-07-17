# AI-Judge Evaluation: AB-05/01_basics_ecommerce
**Evaluator:** (`gpt-5.4-nano-2026-03-17`) using `docs/AI_JUDGE_PROMPT.md`  
**Date:** 2026-07-17

---

# Ablation Study Evaluation: AB-05 — 01_basics_ecommerce

## Executive Summary
AB-05 is a successful run on the **basics e-commerce** dataset: the Builder completed **all 7 parsed tables**, produced **112 triplets**, and had **zero Cypher/mapping/ingestion failures**. Query answering is consistently grounded (**grounded_rate = 1.0**, **gt_coverage = 1.0**) with healthy reranker confidence (avg_top_score ≈ **0.775**), and the pipeline shows **no grader/gate failures**.

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
- `failed_mappings=[]`
- `ingestion_errors=[]`
- High structural output: `triplets_extracted=112`, `entities_resolved=71`
- Builder health signals indicate the full Builder graph (including mapping + Cypher generation/healing) is functioning with no recovery fallbacks required.

### 2. Retrieval Effectiveness (5/5)
- `query_report.grounded_count=15`, `grounded_rate=1.0`
- `avg_gt_coverage=1.0` across all questions (retrieved contexts include the ground-truth sources)
- `avg_top_score=0.7747` (healthy for a bge-reranker-v2-m3 style reranker)
- `pipeline_health.gate_abstentions=0` and `abstained_count=0`, with no negatives showing missed abstention.
- `questions_with_low_retrieval_score=0` in `pipeline_health`.

### 3. Answer Quality (5/5)
- Every question is marked `grounded=true` with `grader_rejection_count=0`.
- Across the sample, generated answers accurately reflect schema constraints/relationships (e.g., CUST_ID FK to orders, STATUS_CODE lifecycle, order-line monetary fields, SKU in `TB_PRODUCT.SKU`, etc.).
- Negative questions are handled correctly (see Q013 and Q014):
  - Q013 (“Can a product belong to multiple categories?”) correctly answers **No**.
  - Q014 (“Is it possible for a customer to place an order without payment?”) correctly answers **Yes** *based on the nullable payment confirmation field*, without contradicting the glossary’s shipping rule.

### 4. Pipeline Health (5/5)
- `pipeline_health`: all critical counters are zero/false:
  - `total_grader_rejections=0`
  - `grader_inconsistencies=0`
  - `gate_abstentions=0`
  - `cypher_failed=false`
  - `failed_mappings_count=0`
  - `ingestion_errors_count=0`
- Per-question `grader_consistency_valid=true` and `context_sufficiency=adequate` throughout.

### 5. Ablation Impact (N/A)
- This bundle is **AB-05**, but no `ablation_context` (vs baseline AB-00) is provided in the input, so causal impact relative to a baseline cannot be scored per rubric.

---

## Per-Question Deep Dive

### Q001: What information is stored for each customer?
- **Type:** direct_mapping | **Difficulty:** easy
- **Verdict:** CORRECT
- **Expected:** ID, full name, unique email, region code, creation date, active status; email unique
- **Generated:** Correctly lists `CUST_ID`, `FULL_NAME`, unique `EMAIL`, `REGION_CODE`, `CREATED_AT`, `IS_ACTIVE`, with nullable region
- **Analysis:** Matches schema columns and business meaning; includes the “whether can place orders” interpretation.
- **Retrieval:** gt_coverage=1.0, top_score=0.7747, gate=proceed

### Q002: How are products categorized on the platform?
- **Type:** direct_mapping | **Difficulty:** easy
- **Verdict:** CORRECT
- **Expected:** product has exactly one category via `CATEGORY_ID`; categories hierarchical via `PARENT_CATEGORY_ID`
- **Generated:** Correctly describes `TB_PRODUCT.CATEGORY_ID → TB_CATEGORY.CATEGORY_ID` and parent hierarchy
- **Analysis:** Correct structural relationship and hierarchy
- **Retrieval:** gt_coverage=1.0, top_score=0.7000, gate=proceed

### Q003: What is the relationship between customers and sales orders?
- **Type:** direct_mapping | **Difficulty:** easy
- **Verdict:** CORRECT
- **Expected:** each order placed by exactly one customer; customer can have zero or more orders
- **Generated:** Correct FK `SALES_ORDER_HDR.CUST_ID → CUSTOMER_MASTER.CUST_ID` + multiplicity
- **Analysis:** Fully aligned with glossary and FK semantics
- **Retrieval:** gt_coverage=1.0, top_score=0.9847, gate=proceed

### Q004: What does an order line item contain?
- **Type:** direct_mapping | **Difficulty:** easy
- **Verdict:** CORRECT
- **Expected:** product, quantity, unit price at purchase, extended amount; belongs to one order
- **Generated:** Correct fields including historical unit price and `LINE_AMT = quantity × unit price`
- **Analysis:** Accurate
- **Retrieval:** gt_coverage=1.0, top_score=0.9856, gate=proceed

### Q005: How are payments linked to orders?
- **Type:** direct_mapping | **Difficulty:** easy
- **Verdict:** CORRECT
- **Expected:** each payment linked to exactly one order via `ORDER_ID` FK; tracks method/amount/status/confirmation time
- **Generated:** Correct FK `payment.order_id -> sales_order_hdr.order_id` and “references exactly one order”
- **Analysis:** Correct
- **Retrieval:** gt_coverage=1.0, top_score=0.9445, gate=proceed

### Q006: What statuses can an order have?
- **Type:** attribute_lookup | **Difficulty:** easy
- **Verdict:** CORRECT
- **Expected:** PENDING, CONFIRMED, SHIPPED, DELIVERED, CANCELLED
- **Generated:** Matches the five statuses from `SALES_ORDER_HDR.STATUS_CODE`
- **Analysis:** Correct enumeration
- **Retrieval:** gt_coverage=1.0, top_score not separately shown for Q006, overall consistent; gate=proceed

### Q007: Which table stores the product SKU information?
- **Type:** direct_mapping | **Difficulty:** easy
- **Verdict:** CORRECT
- **Expected:** `TB_PRODUCT` stores SKU in `SKU`
- **Generated:** Correct: `tb_product.SKU`
- **Analysis:** Correct mapping
- **Retrieval:** gt_coverage=1.0, top_score=0.9844, gate=proceed

### Q008: How can I find all orders placed by a specific customer?
- **Type:** multi_hop | **Difficulty:** medium
- **Verdict:** CORRECT
- **Expected:** query `SALES_ORDER_HDR` by `CUST_ID`, optionally join to `CUSTOMER_MASTER`
- **Generated:** Correct FK-based filtering and join strategy
- **Analysis:** Correct multi-hop reasoning, uses the nullable constraint accurately
- **Retrieval:** gt_coverage=1.0, top_score=0.7000, gate=proceed

### Q009: How does the schema link orders to their individual product line items?
- **Type:** multi_hop | **Difficulty:** medium
- **Verdict:** CORRECT
- **Expected:** `ORDER_LINE_ITEM` bridges `SALES_ORDER_HDR` and `TB_PRODUCT`; includes quantity/unit price/extended amount
- **Generated:** Correctly describes `ORDER_LINE_ITEM.ORDER_ID` FK and `PRODUCT_ID` FK, plus line attributes
- **Analysis:** Correct junction-table semantics
- **Retrieval:** gt_coverage=1.0, top_score=0.7000, gate=proceed

### Q010: Show me the order hierarchy from customer to line items.
- **Type:** multi_hop | **Difficulty:** medium
- **Verdict:** CORRECT
- **Expected:** CUSTOMER_MASTER → SALES_ORDER_HDR → ORDER_LINE_ITEM → TB_PRODUCT
- **Generated:** Correct hierarchy; describes FK directions
- **Analysis:** Correct chain
- **Retrieval:** gt_coverage=1.0, top_score not separately shown, but gate=proceed and grounded

### Q011: How does the schema model the confirmation state of a payment and its relationship to the order?
- **Type:** multi_hop | **Difficulty:** medium
- **Verdict:** CORRECT
- **Expected:** `PAYMENT.CONFIRMED_AT` + `PAYMENT.STATUS_CODE`; mirrors at order via `SALES_ORDER_HDR.PAYMENT_CONFIRMED_AT`
- **Generated:** Correctly explains both tables/fields and FK relation
- **Analysis:** Accurate modeling of confirmation state
- **Retrieval:** gt_coverage=1.0, top_score=0.7000, gate=proceed

### Q012: How are shipments related to orders and warehouses?
- **Type:** multi_hop | **Difficulty:** medium
- **Verdict:** CORRECT
- **Expected:** shipment “for” exactly one sales order via `SHIPMENT.ORDER_ID` → `SALES_ORDER_HDR.ORDER_ID`; includes warehouse code and tracking/status
- **Generated:** Correctly describes FK and warehouse-source semantics
- **Analysis:** Correct multi-hop relationship reasoning
- **Retrieval:** gt_coverage=1.0, top_score=0.7000, gate=proceed

### Q013: Can a product belong to multiple categories?
- **Type:** negative | **Difficulty:** easy
- **Verdict:** CORRECTLY_ABSTAINED / CORRECT (answer is explicit and correct)
- **Expected:** No; each product belongs to exactly one category via `TB_PRODUCT.CATEGORY_ID` FK
- **Generated:** “No” with correct justification (non-null FK, belongs-to-one-category semantics)
- **Analysis:** Correct negative handling (does not hallucinate multi-category)
- **Retrieval:** gt_coverage=1.0, top_score=0.7000, gate=proceed

### Q014: Is it possible for a customer to place an order without payment?
- **Type:** negative | **Difficulty:** medium
- **Verdict:** CORRECT
- **Expected:** Yes can exist without payment confirmation because `PAYMENT_CONFIRMED_AT` is nullable; shipping requires payment confirmation
- **Generated:** Correct interpretation of nullable `SALES_ORDER_HDR.PAYMENT_CONFIRMED_AT`
- **Analysis:** Correct distinction between “order exists” and “ship eligibility”
- **Retrieval:** gt_coverage=1.0, top_score=0.7000, gate=proceed

### Q015: What schema fields support monetary value tracking across orders and their line items?
- **Type:** multi_hop | **Difficulty:** easy
- **Verdict:** CORRECT
- **Expected:** `SALES_ORDER_HDR.TOTAL_AMT` and `ORDER_LINE_ITEM`’s `UNIT_PRICE`, `QUANTITY`, `LINE_AMT (= QUANTITY×UNIT_PRICE)`; linked by `ORDER_ID`
- **Generated:** Correctly covers header total, line components, extended line amount formula, and payment amount relation
- **Analysis:** Accurate and complete; extra mention of payment amount is not penalized and is consistent with contexts
- **Retrieval:** gt_coverage=1.0, top_score=0.7000, gate=proceed

---

## Anomalies & Recommendations

### Red Flags
- None observed. Key failure modes from the rubric (Cypher failures, mapping failures, retrieval miss leading to abstention errors, grounded but wrong answers, grader inconsistencies) are all absent.

### Recommendations
- Since this run is near-perfect, focus ablation/engineering effort elsewhere:
  - Evaluate under **advanced/hard** datasets where multi-hop extraction/ER and traversal become more fragile.
  - Specifically test the known limitation: **aggressive entity resolution (threshold=0.75)** by running adversarial near-duplicate entity names and measuring multi-hop edge correctness.

## Comparison Notes (if applicable)
- `ragas=null` and no explicit “baseline vs AB-05” diff is provided, so no AB-00 comparison can be made.
- The observed results indicate the configured hybrid retrieval + reranker + full self-reflection loops yield maximum correctness on this basics dataset.