# AI-Judge Evaluation: AB-12/01_basics_ecommerce
**Evaluator:** (`gpt-5.4-nano-2026-03-17`) using `docs/AI_JUDGE_PROMPT.md`  
**Date:** 2026-07-17

---

# Ablation Study Evaluation: AB-12 — 01_basics_ecommerce

## Executive Summary
AB-12 shows a healthy end-to-end pipeline on the e-commerce “basics” dataset: the builder completed all tables with no Cypher failures or ingestion errors, and the query graph achieved 100% grounded answers. The only clear concern is that several multi-hop queries (e.g., Q008) have noticeably lower `gt_coverage` despite still returning grounded answers, suggesting that retrieval relevance/tightness varies by question type even when answers remain correct.

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
- `tables_completed = 7`, `all_tables_completed = true`
- `cypher_failed = false`
- `failed_mappings = []`, `ingestion_errors = []`
- Triplets extracted: `triplets_extracted = 99` (strong density for a basics dataset)

This meets (and exceeds) the “all tables completed, no cypher failures, no failed mappings” criteria.

### 2. Retrieval Effectiveness (4/5)
Key signals:
- `avg_gt_coverage = 0.95` (strong; near the 0.8+ threshold for score 5)
- `avg_top_score = 0.778` (healthy for a cross-encoder reranker; comfortably above 0.5)
- `pipeline_health.gate_abstentions = 0` and `grounded_rate = 1.0`

However, multi-hop retrieval is not uniformly tight:
- Worst observed `gt_coverage` in the provided set:
  - **Q008** (multi-hop): `gt_coverage = 0.5` while the answer is still correct.
  - **Q010**: `gt_coverage = 0.75`
- `retrieval_quality_score_raw` is low for some multi-hop queries (many at/around **0.55**), indicating variability in the raw reranker confidence before the pipeline’s adjustments/pool-confidence handling.

Given correctness remains high, this looks like “retrieval is good but not perfectly recall-tight for multi-hop,” which aligns better with **4/5** than **5/5**.

### 3. Answer Quality (5/5)
- `query_report.grounded_rate = 1.0` (all 15 grounded)
- `grader_rejection_count = 0` and `grader_consistency_valid = true`

Selected per-question checks:
- **Best-case correctness (Q004, Q007, Q011, Q013, Q014):**
  - Q013 (negative): correctly answers “No” with schema-grounded reasoning.
  - Q014 (negative): correctly answers “Yes” and justifies it via nullable `PAYMENT_CONFIRMED_AT` and “shipping gated by payment confirmation” (not “payment required to create order”).
- **Multi-hop that still matches expected (Q009, Q012, Q015):**
  - Q009 and Q012 correctly describe relationship modeling/junction structure.
  - Q015 is a bit nuanced: the generated answer includes `PAYMENT.AMOUNT`, whereas the expected answer focuses on order header `TOTAL_AMT` plus line item `LINE_AMT/UNIT_PRICE/QUANTITY`. This is not wrong; it’s extra, but it also explicitly acknowledges that retrieved context didn’t provide the exact `SALES_ORDER_HDR` total column—consistent with groundedness.

Overall: the answers are semantically aligned with expected intents across direct and negative question types.

### 4. Pipeline Health (5/5)
- `total_grader_rejections = 0`
- `grader_inconsistencies = 0`
- `gate_abstentions = 0`
- `cypher_failed = false`, `failed_mappings_count = 0`, `ingestion_errors_count = 0`

With no failures and stable grader behavior, this meets the top tier.

### 5. Ablation Impact (N/A)
- This bundle is **AB-12**, but the provided JSON does not include an `ablation_context` field or a “changes vs baseline” specification, nor does it explicitly state which ablation flags differ from AB-00.
- Therefore, per rubric, Ablation Impact cannot be scored from the information available.

## Per-Question Deep Dive

### Q001: What information is stored for each customer?
- **Type:** direct_mapping | **Difficulty:** easy  
- **Verdict:** CORRECT  
- **Expected:** ID, full name, unique email, region code, creation date, active status; email unique  
- **Generated:** Uses `customer_master` to cover `CUST_ID`, `FULL_NAME`, `EMAIL` (via context), `REGION_CODE`, `CREATED_AT`, `IS_ACTIVE`/`is_active`  
- **Analysis:** Matches all required customer attributes; grounded in retrieved customer master context.  
- **Retrieval:** gt_coverage=1.0, top_score=0.7777517942119628, gate=proceed

### Q002: How are products categorized on the platform?
- **Type:** direct_mapping | **Difficulty:** easy  
- **Verdict:** CORRECT  
- **Expected:** single category per product; category hierarchy via parent category; `CATEGORY_ID` FK  
- **Generated:** `TB_PRODUCT.CATEGORY_ID` → `TB_CATEGORY(CATEGORY_ID)`; hierarchy via `PARENT_CATEGORY_ID`  
- **Analysis:** Captures both FK linkage and hierarchy.  
- **Retrieval:** gt_coverage=1.0, top_score=0.7777517942119628, gate=proceed

### Q003: What is the relationship between customers and sales orders?
- **Type:** direct_mapping | **Difficulty:** easy  
- **Verdict:** CORRECT  
- **Expected:** each order placed by one customer (`CUST_ID` FK); customer can have many orders  
- **Generated:** cites “customer places zero or more orders” + FK `sales_order_hdr.cust_id` → `customer_master.cust_id`  
- **Analysis:** Relationship direction and cardinality align with expected.  
- **Retrieval:** gt_coverage=1.0, top_score=0.7777517942119628, gate=proceed

### Q004: What does an order line item contain?
- **Type:** direct_mapping | **Difficulty:** easy  
- **Verdict:** CORRECT  
- **Expected:** product, quantity, unit price at purchase time, extended/line amount; belongs to exactly one order  
- **Generated:** product + quantity + unit price + `quantity × unit price` extended amount  
- **Analysis:** Correctly covers the line-item monetary model.  
- **Retrieval:** gt_coverage=1.0, top_score=0.7777517942119628, gate=proceed

### Q005: How are payments linked to orders?
- **Type:** direct_mapping | **Difficulty:** easy  
- **Verdict:** CORRECT  
- **Expected:** `payment.order_id` → `sales_order_hdr.order_id`; payment method/status/amount/timestamps  
- **Generated:** Exactly that FK plus business rule “one payment per order” (and order can have many payments)  
- **Analysis:** Correct linkage and intent.  
- **Retrieval:** gt_coverage=1.0, top_score=0.7777517942119628, gate=proceed

### Q006: What statuses can an order have?
- **Type:** attribute_lookup | **Difficulty:** easy  
- **Verdict:** CORRECT  
- **Expected:** PENDING, CONFIRMED, SHIPPED, DELIVERED, CANCELLED  
- **Generated:** Lists those five statuses for `sales_order_hdr` / `sales_order_hdr.status_code`  
- **Analysis:** Direct match to expected lifecycle states.  
- **Retrieval:** gt_coverage=1.0, top_score=0.7777517942119628, gate=proceed

### Q007: Which table stores the product SKU information?
- **Type:** direct_mapping | **Difficulty:** easy  
- **Verdict:** CORRECT  
- **Expected:** `TB_PRODUCT` stores SKU code (`SKU`), plus other product attributes  
- **Generated:** `tb_product` and `SKU` column  
- **Analysis:** Correct table/column mapping.  
- **Retrieval:** gt_coverage=1.0, top_score=0.7777517942119628, gate=proceed

### Q008: How can I find all orders placed by a specific customer?
- **Type:** multi_hop | **Difficulty:** medium  
- **Verdict:** CORRECT  
- **Expected:** filter `SALES_ORDER_HDR` by `CUST_ID`; join on `CUSTOMER_MASTER.CUST_ID`  
- **Generated:** describes selecting orders from `SALES_ORDER_HDR` where `SALES_ORDER_HDR.CUST_ID` equals a customer’s `CUSTOMER_MASTER.CUST_ID`  
- **Analysis:** Correct query intent despite weaker GT source coverage.  
- **Retrieval:** gt_coverage=0.5, top_score=0.7777517942119628, gate=proceed

### Q009: How does the schema link orders to their individual product line items?
- **Type:** multi_hop | **Difficulty:** medium  
- **Verdict:** CORRECT  
- **Expected:** junction `ORDER_LINE_ITEM` with `ORDER_ID` → `SALES_ORDER_HDR` and `PRODUCT_ID` → `TB_PRODUCT`; includes quantity/unit price/line amount  
- **Generated:** joins via `ORDER_LINE_ITEM` on `ORDER_ID` and references `PRODUCT_ID` → `TB_PRODUCT`  
- **Analysis:** Correct junction modeling and linkage.  
- **Retrieval:** gt_coverage=1.0, top_score=0.7777517942119628, gate=proceed

### Q010: Show me the order hierarchy from customer to line items.
- **Type:** multi_hop | **Difficulty:** medium  
- **Verdict:** CORRECT  
- **Expected:** Customer → SALES_ORDER_HDR → ORDER_LINE_ITEM → TB_PRODUCT  
- **Generated:** describes hierarchy via `SALES_ORDER_HDR.CUST_ID` and `ORDER_LINE_ITEM.ORDER_ID` + product via `ORDER_LINE_ITEM`  
- **Analysis:** Structure matches expected; no contradiction observed.  
- **Retrieval:** gt_coverage=0.75, top_score=0.7777517942119628, gate=proceed

### Q011: How does the schema model the confirmation state of a payment and its relationship to the order?
- **Type:** multi_hop | **Difficulty:** medium  
- **Verdict:** CORRECT  
- **Expected:** `PAYMENT.CONFIRMED_AT` (nullable) + `PAYMENT.STATUS_CODE`; order-level `SALES_ORDER_HDR.PAYMENT_CONFIRMED_AT` nullable; order lifecycle statuses via constraint  
- **Generated:** payment status/timestamp + FK payment→order + order header payment confirmation timestamp  
- **Analysis:** Captures confirmation state split across payment and order.  
- **Retrieval:** gt_coverage=1.0, top_score=0.7777517942119628, gate=proceed

### Q012: How are shipments related to orders and warehouses?
- **Type:** multi_hop | **Difficulty:** medium  
- **Verdict:** CORRECT  
- **Expected:** shipment belongs to one order (`ORDER_ID`), includes source warehouse and tracking/status  
- **Generated:** “shipment references exactly one sales order” + “comes from exactly one warehouse” + shipment attributes  
- **Analysis:** Correct cardinality and attribute intent.  
- **Retrieval:** gt_coverage=1.0, top_score=0.7777517942119628, gate=proceed

### Q013: Can a product belong to multiple categories?
- **Type:** negative | **Difficulty:** easy  
- **Verdict:** CORRECTLY_ABSTAINED (Answer is correct negative)  
- **Expected:** No; product has exactly one category via FK `CATEGORY_ID`  
- **Generated:** “No” with explanation of single FK relationship  
- **Analysis:** Correct handling of negative constraint question.  
- **Retrieval:** gt_coverage=1.0, top_score=0.7777517942119628, gate=proceed

### Q014: Is it possible for a customer to place an order without payment?
- **Type:** negative | **Difficulty:** medium  
- **Verdict:** CORRECT  
- **Expected:** Yes; payment confirmation timestamp nullable; shipping requires confirmation but order creation can precede payment  
- **Generated:** Yes; `PAYMENT_CONFIRMED_AT` nullable; shipping gated by payment confirmation  
- **Analysis:** Correctly interprets the negative scenario (distinguishes “no confirmed payment” vs “no payment row required”).  
- **Retrieval:** gt_coverage=1.0, top_score=0.7777517942119628, gate=proceed

### Q015: What schema fields support monetary value tracking across orders and their line items?
- **Type:** multi_hop | **Difficulty:** easy  
- **Verdict:** PARTIALLY_CORRECT (still grounded and mostly matches)  
- **Expected:** `SALES_ORDER_HDR.TOTAL_AMT` (header total) + `ORDER_LINE_ITEM.UNIT_PRICE`, `QUANTITY`, `LINE_AMT = QUANTITY × UNIT_PRICE`; linked by `ORDER_ID`  
- **Generated:** Correctly covers line-level `LINE_AMT`, `QUANTITY`, `UNIT_PRICE` and link to `ORDER_ID`, and adds `PAYMENT.AMOUNT`; explicitly notes missing exact `SALES_ORDER_HDR` total column from retrieved context.  
- **Analysis:** Slight mismatch in scope (adds payment amount) and may not explicitly name `TOTAL_AMT`—but no incorrect claims are introduced; groundedness is maintained.  
- **Retrieval:** gt_coverage=1.0, top_score=0.7777517942119628, gate=proceed

## Anomalies & Recommendations

### Red Flags
- **Multi-hop retrieval tightness varies** even when answers are correct:
  - Q008 `gt_coverage=0.5` (retrieval did not strongly recover all ground-truth sources, yet generation stayed correct).
  - Q010 `gt_coverage=0.75`.
- **Extra-scope risk**: Q015 introduces `PAYMENT.AMOUNT` though the expected answer emphasizes `SALES_ORDER_HDR.TOTAL_AMT` + line amounts. This is not “wrong,” but indicates the model may over-generalize monetary tracking when context includes payments.

### Recommendations
1. **Strengthen multi-hop context selection**: adjust context distillation caps or retrieval fusion weights specifically for multi-hop questions to improve GT source recall (reduce cases like Q008).
2. **Constrain answer scope to question intent**: in `answer_generation`, add a lightweight “target entity/table” constraint using `query_type` (e.g., for Q015, emphasize `SALES_ORDER_HDR` total field rather than payment-level amount unless explicitly asked).
3. **Improve explicitness on header totals**: when the question asks for order-level monetary tracking, ensure the generator searches/uses `SALES_ORDER_HDR` total column descriptions (e.g., `TOTAL_AMT`) if present in contexts, even if payment contexts are also retrieved.

## Comparison Notes (if applicable)
- `ragas` is `null`, so no metric comparison is possible from this bundle.
- No baseline-vs-ablation change log (`changes_vs_baseline` / `ablation_context`) is provided, so AB-12’s causal impact cannot be asserted by the rubric.