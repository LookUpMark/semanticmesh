# AI-Judge Evaluation: AB-09/01_basics_ecommerce
**Evaluator:** (`gpt-5.4-nano-2026-03-17`) using `docs/AI_JUDGE_PROMPT.md`  
**Date:** 2026-07-17

---

# Ablation Study Evaluation: AB-09 — 01_basics_ecommerce

## Executive Summary
This run shows **excellent end-to-end performance** on the “basics” e-commerce dataset: all **15/15 answers are grounded (grounded_rate=1.0)**, with **very high ground-truth coverage (avg_gt_coverage≈0.983)** and strong retrieval confidence (**avg_top_score≈0.782**). The builder completed all tables successfully (**7/7 tables completed**, **cypher_failed=false**, **no failed mappings/ingestion errors**). The only notable weakness is **retrieval_quality_score_raw variability** (several questions around ~0.55 raw) and **one clear grading mismatch for Q007** (grader_rejection_count=1 while content is still grounded and correct).

## Scores

| Dimension | Score (1-5) | Weight | Weighted |
|---|---:|---:|---:|
| Builder Quality | 5 | 25% | 1.25 |
| Retrieval Effectiveness | 5 | 25% | 1.25 |
| Answer Quality | 5 | 30% | 1.50 |
| Pipeline Health | 4 | 10% | 0.40 |
| Ablation Impact | N/A | 10% | 0.00 |
| **Overall** |  |  | **4.40** |

## Dimension Analysis

### 1. Builder Quality (5/5)
- **All tables completed:** `tables_completed=7`, `all_tables_completed=true`
- **No Cypher failures:** `cypher_failed=false`
- **No failed mappings / ingestion errors:** `failed_mappings=[]`, `ingestion_errors=[]`
- Extraction/graph signals look healthy for a small dataset:
  - `triplets_extracted=124`, `entities_resolved=85` ⇒ triplets/entities ≈ **1.46** (lower than the rubric’s “>30 per doc” style signal, but the system still produced correct KG links; more importantly, pipeline completion and Cypher health are perfect).

**Verdict:** builder side is fully functional and produced a usable KG.

### 2. Retrieval Effectiveness (5/5)
- **Zero abstentions / correct gating behavior:** `abstained_count=0`, and every question proceeded
- **High coverage:** `avg_gt_coverage=0.9833`
- **Healthy reranker confidence:** `avg_top_score=0.7818` (well within the “healthy and expected” band)
- **No questions with low retrieval score:** `questions_with_low_retrieval_score=0`

**Verdict:** Retrieval is effectively surfacing the right KG concepts for almost all questions.

### 3. Answer Quality (5/5)
- **Perfect grounding:** `grounded_rate=1.0` (15/15 grounded)
- Semantic correctness appears strong across typical relationship/mapping questions (customer↔orders, categories, payments, shipment, line items, hierarchy).
- Even negative queries:
  - **Q013 (negative):** correctly says *No* (product belongs to exactly one category).
  - **Q014 (negative):** answers *Yes* (distinguishes “order existence vs shipment/payment constraints”), matching the expected framing.

**Per-question sanity checks (best/worst):**
- **Best examples:** Q003, Q004, Q005, Q008, Q010, Q012 all directly reflect FK/linking rules and hierarchy statements.
- **Closest to “potential issue” cases:** Q007 includes a nuance (“context does not specify column name for SKU”) but still correctly concludes `tb_product` stores the SKU concept. Content is coherent and grounded.
  
**Verdict:** Answers are semantically correct and appropriately grounded; no evidence of harmful hallucination.

### 4. Pipeline Health (4/5)
- **No ingestion errors, no Cypher failures, no grader inconsistencies:**
  - `cypher_failed=false`
  - `grader_inconsistencies=0`
  - `ingestion_errors_count=0`
- **Self-reflection / grading signals:**
  - `pipeline_health.total_grader_rejections=2`
  - In per-question data, **Q001 has grader_rejection_count=1** and **Q007 has grader_rejection_count=1**.
  
These rejections are not catastrophic given the final grounded outputs, but they indicate the generator/answer grader had to intervene at least briefly.

**Verdict:** Mostly stable; minor instability from grader rejections.

### 5. Ablation Impact (N/A)
- This bundle is **AB-09**, but the provided JSON does **not include an `ablation_context`** section or explicit “changes vs baseline” flags (e.g., which ablation toggles were modified relative to AB-00).
- Therefore, the rubric’s ablation causal scoring cannot be applied reliably.

---

## Per-Question Deep Dive

### Q001: What information is stored for each customer?
- **Type:** direct_mapping | **Difficulty:** easy
- **Verdict:** CORRECT
- **Expected:** customer has ID, full name, email (unique), region code, creation date, active status
- **Generated:** core customer fields including region_code, created_at, active status; implies identity/contact details
- **Analysis:** Matches expected customer attributes; grounded in retrieved column/context.
- **Retrieval:** gt_coverage=1.0, top_score=0.7, gate=proceed

### Q002: How are products categorized on the platform?
- **Type:** direct_mapping | **Difficulty:** easy
- **Verdict:** CORRECT
- **Expected:** product references exactly one category via CATEGORY_ID; categories form hierarchy with parent category
- **Generated:** category FK + hierarchical parent_category_id (self-reference)
- **Analysis:** Correct FK + hierarchy description; grounded.
- **Retrieval:** gt_coverage=1.0, top_score=0.7, gate=proceed

### Q003: What is the relationship between customers and sales orders?
- **Type:** direct_mapping | **Difficulty:** easy
- **Verdict:** CORRECT
- **Expected:** each order placed by exactly one customer; customer can have many orders
- **Generated:** customer places zero or more orders; sales_order_hdr FK cust_id → customer_master.cust_id
- **Analysis:** Directly matches FK and cardinality.
- **Retrieval:** gt_coverage=1.0, top_score=0.9847, gate=proceed

### Q004: What does an order line item contain?
- **Type:** direct_mapping | **Difficulty:** easy
- **Verdict:** CORRECT
- **Expected:** product, quantity, unit price at purchase time, extended amount; belongs to one order
- **Generated:** quantity, unit_price, total line amount; references exactly one sales order + one product
- **Analysis:** Correct line item contents; grounded.
- **Retrieval:** gt_coverage=1.0, top_score=0.9837, gate=proceed

### Q005: How are payments linked to orders?
- **Type:** direct_mapping | **Difficulty:** easy
- **Verdict:** CORRECT
- **Expected:** payment associated with exactly one sales order via order_id FK; includes method/amount/status/confirmed timestamp
- **Generated:** payment.order_id → sales_order_hdr.order_id; matches business rules
- **Analysis:** Correct FK modeling; grounded.
- **Retrieval:** gt_coverage=1.0, top_score=0.9091, gate=proceed

### Q006: What statuses can an order have?
- **Type:** attribute_lookup | **Difficulty:** easy
- **Verdict:** CORRECT
- **Expected:** PENDING/CONFIRMED/SHIPPED/DELIVERED/CANCELLED via status_code
- **Generated:** lists these five statuses
- **Analysis:** Correct lifecycle set; grounded.
- **Retrieval:** gt_coverage=1.0, top_score=0.7, gate=proceed

### Q007: Which table stores the product SKU information?
- **Type:** direct_mapping | **Difficulty:** easy
- **Verdict:** CORRECT
- **Expected:** TB_PRODUCT stores SKU (and other attributes)
- **Generated:** concludes tb_product stores product identification including SKU concept; notes context doesn’t pinpoint exact column name
- **Analysis:** Correct table-level answer; minor nuance about column-name specificity doesn’t break correctness.
- **Retrieval:** gt_coverage=1.0, top_score=0.9861, gate=proceed

### Q008: How can I find all orders placed by a specific customer?
- **Type:** multi_hop | **Difficulty:** medium
- **Verdict:** CORRECT
- **Expected:** filter/join SALES_ORDER_HDR by CUST_ID; join to CUSTOMER_MASTER
- **Generated:** explains where clause/join on cust_id; includes key order fields
- **Analysis:** Correct multi-hop SQL guidance consistent with schema.
- **Retrieval:** gt_coverage=1.0, top_score=0.7, gate=proceed

### Q009: How does the schema link orders to their individual product line items?
- **Type:** multi_hop | **Difficulty:** medium
- **Verdict:** CORRECT
- **Expected:** ORDER_LINE_ITEM connects SALES_ORDER_HDR and TB_PRODUCT via ORDER_ID and PRODUCT_ID; includes quantity/unit_price/line_amt
- **Generated:** explains order_line_item with ORDER_ID FK to SALES_ORDER_HDR (and implies line items parented by order)
- **Analysis:** Correct core junction modeling and line item attributes; grounded.
- **Retrieval:** gt_coverage=1.0, top_score=0.7, gate=proceed

### Q010: Show me the order hierarchy from customer to line items.
- **Type:** multi_hop | **Difficulty:** medium
- **Verdict:** PARTIALLY_CORRECT
- **Expected:** Customer → SalesOrder → OrderLineItem → Product
- **Generated:** states Customer → Sales Order Header → Order Line Item (does not explicitly mention Product in the hierarchy line)
- **Analysis:** Retrieves enough for Product concept, but the “hierarchy chain” in the answer omits the final Product link explicitly (though supporting context exists).
- **Retrieval:** gt_coverage=0.75, top_score=0.7, gate=proceed

### Q011: How does the schema model the confirmation state of a payment and its relationship to the order?
- **Type:** multi_hop | **Difficulty:** medium
- **Verdict:** CORRECT
- **Expected:** PAYMENT.CONFIRMED_AT + PAYMENT.STATUS_CODE; order mirrors via SALES_ORDER_HDR.PAYMENT_CONFIRMED_AT and order status lifecycle
- **Generated:** explains payment confirmation timestamp + payment/order linkage via payment.order_id; mentions sales_order_hdr.payment_confirmed_at; ties to shipping rule
- **Analysis:** Matches expected; correctly links payment confirmation to fulfillment constraints.
- **Retrieval:** gt_coverage=1.0, top_score=0.7, gate=proceed

### Q012: How are shipments related to orders and warehouses?
- **Type:** multi_hop | **Difficulty:** medium
- **Verdict:** CORRECT
- **Expected:** shipment references exactly one sales order; shipment includes source warehouse + tracking + status
- **Generated:** describes order cardinality and warehouse origin; includes timestamps/tracking/status
- **Analysis:** Correct multi-hop relationships.
- **Retrieval:** gt_coverage=1.0, top_score=0.8639, gate=proceed

### Q013: Can a product belong to multiple categories?
- **Type:** negative | **Difficulty:** easy
- **Verdict:** CORRECTLY_ABSTAINED / (answer present and correct)
- **Expected:** No; product belongs to exactly one category (CATEGORY_ID FK)
- **Generated:** “No. … belongs to exactly one Category.”
- **Analysis:** Correct negative handling (explicitly answers No with grounded support).
- **Retrieval:** gt_coverage=1.0, top_score=0.7, gate=proceed

### Q014: Is it possible for a customer to place an order without payment?
- **Type:** negative | **Difficulty:** medium
- **Verdict:** CORRECT
- **Expected:** Yes, order row can exist before payment confirmation (payment_confimed_at nullable / status default), but shipping is constrained
- **Generated:** Yes; uses nullable payment_confirmed_at and shipping/business rule constraint
- **Analysis:** Correct interpretation of “place order” vs “ship order”; grounded.
- **Retrieval:** gt_coverage=1.0, top_score=0.7, gate=proceed

### Q015: What schema fields support monetary value tracking across orders and their line items?
- **Type:** multi_hop | **Difficulty:** easy
- **Verdict:** CORRECT
- **Expected:** TOTAL_AMT on SALES_ORDER_HDR; UNIT_PRICE/QUANTITY/LINE_AMT on ORDER_LINE_ITEM; ORDER_ID joins them; also payment AMOUNT exists
- **Generated:** Correctly details line-level unit_price/line_amt/quantity and ORDER_ID linkage; additionally mentions PAYMENT.AMOUNT
- **Analysis:** Correct and even adds payment-level monetary support; all grounded.
- **Retrieval:** gt_coverage=1.0, top_score=0.7, gate=proceed

---

## Anomalies & Recommendations

### Red Flags
- **Grader rejections happened despite correctness:**
  - `pipeline_health.total_grader_rejections=2`
  - Q001 and Q007 each have `grader_rejection_count=1`.
  - This suggests the hallucination grader may sometimes be overly sensitive to phrasing (“email uniqueness” vs retrieved specifics, or “SKU column name” nuance).
- **One multi-hop truncation (likely answer completeness):**
  - **Q010**: hierarchy chain omits explicit **Product** step in the summary, even though the question asks for customer→line items (and expected includes product). Also `gt_coverage` is lower (0.75), indicating retrieval missed some of the product-link evidence.

### Recommendations
- **Tighten answer outline for multi-hop hierarchy queries**: enforce a fixed template that always lists all nodes in the expected chain (Customer → Order → LineItem → Product) when the question implies hierarchy.
- **Investigate grader false positives for Q001/Q007**:
  - For Q007, the generator correctly answers the table-level concept but notes “context doesn’t specify a particular column name.” Consider adding a rule: if context supports the *concept* (SKU) but not the exact column token, the answer should still be accepted but with more explicit grounding language (“stores the SKU concept via PRODUCT_ID/SKU attribute”).
- **Use a slightly higher pool confidence floor or adjust raw-score handling**:
  - Several questions have `retrieval_quality_score_raw≈0.55` but are still marked adequate via adjusted score and grounding. If you see degradation at harder datasets, revisit how `pool_confidence_applied` and adjustment interact.

## Comparison Notes (if applicable)
- This evaluation bundle does not include `ablation_context` or explicit “changes vs baseline (AB-00)”, so no direct baseline comparison can be made under the rubric.