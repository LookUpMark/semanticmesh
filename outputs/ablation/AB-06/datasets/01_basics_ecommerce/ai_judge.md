# AI-Judge Evaluation: AB-06/01_basics_ecommerce
**Evaluator:** (`gpt-5.4-nano-2026-03-17`) using `docs/AI_JUDGE_PROMPT.md`  
**Date:** 2026-07-17

---

# Ablation Study Evaluation: AB-06 — 01_basics_ecommerce

## Executive Summary
AB-06 shows a fully healthy end-to-end run on the *basics e-commerce* dataset: the builder completed all tables with no Cypher failures and the query graph retrieved/verifiably grounded answers for all 15 questions. Retrieval confidence is consistently high (avg_top_score ≈ 0.79) and answer grounding is perfect (grounded_rate = 1.0, abstained_count = 0), including correct handling of negative questions.

The main “caveat” is not a failure of correctness, but metric interpretation: several per-question retrieval_quality_score_raw values are low-ish (e.g., ~0.55) while adjusted scores are ~0.7 due to the pool confidence floor; however, since grounding and semantic correctness are excellent, this does not materially indicate a retrieval problem.

## Scores

| Dimension | Score (1-5) | Weight | Weighted |
|---|---:|---:|---:|
| Builder Quality | 5 | 25% | 1.25 |
| Retrieval Effectiveness | 5 | 25% | 1.25 |
| Answer Quality | 5 | 30% | 1.50 |
| Pipeline Health | 5 | 10% | 0.50 |
| Ablation Impact | 3 | 10% | 0.30 |
| **Overall** |  |  | **4.80** |

## Dimension Analysis

### 1. Builder Quality (5/5)
- `tables_parsed=7`, `tables_completed=7`, `all_tables_completed=true`
- `cypher_failed=false`
- `failed_mappings=[]`, `ingestion_errors=[]`
- Triplet density signal: `triplets_extracted=106` across 7 tables is strong for this small dataset.
- No evidence of broken upstream steps (ER, mapping, Cypher healing) impacting the query KG quality.

### 2. Retrieval Effectiveness (5/5)
- `query_report.grounded_rate=1.0`
- `abstained_count=0` with a small “basics” dataset and no unanswerable/negative failures observed.
- `avg_gt_coverage=1.0` means expected sources were retrieved for every question.
- `avg_top_score=0.7899` is in the healthy band for a bge-reranker-v2-m3 style reranker.
- `pipeline_health.questions_with_low_retrieval_score=0`

### 3. Answer Quality (5/5)
Across the provided per-question records:
- Every answer is marked `grounded=true` with `grader_rejection_count=0`
- Negative questions are handled correctly:
  - **Q013 (negative)**: “Can a product belong to multiple categories?” → correctly says **No**, consistent with “belongs to exactly one Category” via CATEGORY_ID FK.
  - **Q014 (negative)**: “Is it possible for a customer to place an order without payment?” → correctly distinguishes *shipping rules* vs *existence of order header/payment confirmation field*, concluding **Yes** (order header can exist; payment confirmation is required before shipping).
- No hallucination signals: no grader rejections and “context_sufficiency=adequate” everywhere.

**Best examples (semantic match + completeness):**
- Q001 (customers fields): matches exactly expected fields (ID, full name, email, region code, creation date, active status, email uniqueness) using customer_master / glossary contexts.
- Q009/Q010 (multi-hop structural modeling): correctly describes junction/edges and hierarchy: SALES_ORDER_HDR → ORDER_LINE_ITEM → TB_PRODUCT, and Customer → SalesOrder → LineItems.

### 4. Pipeline Health (5/5)
- `pipeline_health.total_grader_rejections=0`
- `grader_inconsistencies=0`
- `gate_abstentions=0`
- `cypher_failed=false`
- `failed_mappings_count=0`, `ingestion_errors_count=0`
- Latency signals are trivial here (`elapsed_s=0` across builder/query), consistent with a small dataset; importantly, there are no stability/error indicators.

### 5. Ablation Impact (3/5)
Study AB-06 is not compared against a baseline via an explicit `ablation_context` object in the bundle, and the provided `config` does not clearly state which components were disabled/enabled relative to AB-00 (baseline). Therefore:
- We cannot attribute *causal* improvements/deteriorations to specific ablation flags.
- Given the build and query are near-perfect, the most reasonable interpretation is that AB-06 represents a “good configuration,” but we can’t validate the expected effect from a formal hypothesis.

If AB-06 corresponds to a single-flag change (e.g., turning a component off), that information is missing here—so the ablation-impact score is necessarily conservative.

## Per-Question Deep Dive

### Q001: What information is stored for each customer?
- **Type:** direct_mapping | **Difficulty:** easy  
- **Verdict:** CORRECT  
- **Expected:** unique customer ID, full name, email, region code, creation date, active status; email unique  
- **Generated:** customer_master stores CUST_ID, full_name, EMAIL, region, created_at, IS_ACTIVE; describes account activation status  
- **Analysis:** Correct fields and intended meaning; grounded in retrieved Customer Master and column definitions.  
- **Retrieval:** gt_coverage=1.0, top_score=0.7027, gate=proceed

### Q002: How are products categorized on the platform?
- **Type:** direct_mapping | **Difficulty:** easy  
- **Verdict:** CORRECT  
- **Expected:** category hierarchy via parent category; each product references exactly one category via CATEGORY_ID  
- **Generated:** TB_CATEGORY defines hierarchy via PARENT_CATEGORY_ID; TB_PRODUCT has non-null CATEGORY_ID FK to TB_CATEGORY  
- **Analysis:** Correct hierarchical and one-to-many/one-to-one semantics, aligned with schema.  
- **Retrieval:** gt_coverage=1.0, top_score=0.7, gate=proceed

### Q003: What is the relationship between customers and sales orders?
- **Type:** direct_mapping | **Difficulty:** easy  
- **Verdict:** CORRECT  
- **Expected:** each order placed by exactly one customer (CUST_ID FK); customer can have zero or more orders  
- **Generated:** many-to-one: customer → zero or more sales orders; each sales order header tied to one customer  
- **Analysis:** Correct cardinalities and FK linkage.  
- **Retrieval:** gt_coverage=1.0, top_score=0.9847, gate=proceed

### Q004: What does an order line item contain?
- **Type:** direct_mapping | **Difficulty:** easy  
- **Verdict:** CORRECT  
- **Expected:** product, quantity, unit price at time of purchase, extended amount; belongs to exactly one sales order  
- **Generated:** product + quantity + unit price + total line amounts; aligns with order_line_item description  
- **Analysis:** Correct content; grounded in OrderLineItem and column glossary/definitions.  
- **Retrieval:** gt_coverage=1.0, top_score=0.9835, gate=proceed

### Q005: How are payments linked to orders?
- **Type:** direct_mapping | **Difficulty:** easy  
- **Verdict:** CORRECT  
- **Expected:** each payment associated with exactly one sales order via ORDER_ID FK; includes method/amount/status/timestamps  
- **Generated:** exactly that, using Payment → Sales Order relationship and payment columns  
- **Analysis:** Correct linkage and attribute coverage.  
- **Retrieval:** gt_coverage=1.0, top_score=0.9627, gate=proceed

### Q006: What statuses can an order have?
- **Type:** attribute_lookup | **Difficulty:** easy  
- **Verdict:** CORRECT  
- **Expected:** PENDING, CONFIRMED, SHIPPED, DELIVERED, CANCELLED; CHECK constraint / glossary lifecycle  
- **Generated:** lists the five statuses  
- **Analysis:** Matches expected lifecycle.  
- **Retrieval:** gt_coverage=1.0, top_score=0.7, gate=proceed

### Q007: Which table stores the product SKU information?
- **Type:** direct_mapping | **Difficulty:** easy  
- **Verdict:** CORRECT  
- **Expected:** TB_PRODUCT stores SKU (plus name/category/price/active)  
- **Generated:** tb_product.sku / SKU column description  
- **Analysis:** Correct table/column identification.  
- **Retrieval:** gt_coverage=1.0, top_score=0.9881, gate=proceed

### Q008: How can I find all orders placed by a specific customer?
- **Type:** multi_hop | **Difficulty:** medium  
- **Verdict:** CORRECT  
- **Expected:** filter SALES_ORDER_HDR by CUST_ID FK to CUSTOMER_MASTER; join shows orders + details  
- **Generated:** select from SALES_ORDER_HDR where CUST_ID = customer CUST_ID; mentions key order fields and timestamps  
- **Analysis:** Correct multi-hop reasoning and join key semantics.  
- **Retrieval:** gt_coverage=1.0, top_score=0.7, gate=proceed

### Q009: How does the schema link orders to their individual product line items?
- **Type:** multi_hop | **Difficulty:** medium  
- **Verdict:** CORRECT  
- **Expected:** ORDER_LINE_ITEM junction: ORDER_ID → SALES_ORDER_HDR; PRODUCT_ID → TB_PRODUCT; includes QUANTITY, UNIT_PRICE, LINE_AMT  
- **Generated:** describes ORDER_LINE_ITEM with FK order_id and product_id and correct containment  
- **Analysis:** Correct junction-model explanation.  
- **Retrieval:** gt_coverage=1.0, top_score=0.7, gate=proceed

### Q010: Show me the order hierarchy from customer to line items.
- **Type:** multi_hop | **Difficulty:** medium  
- **Verdict:** CORRECT  
- **Expected:** Customer → SALES_ORDER_HDR → ORDER_LINE_ITEM → TB_PRODUCT  
- **Generated:** describes Customer via SALES_ORDER_HDR.CUST_ID; then order_line_item links to sales order and has product_id  
- **Analysis:** Correct hierarchy and edge directionality (customer → orders → line items → products).  
- **Retrieval:** gt_coverage=1.0, top_score=0.7, gate=proceed

### Q011: How does the schema model the confirmation state of a payment and its relationship to the order?
- **Type:** multi_hop | **Difficulty:** medium  
- **Verdict:** CORRECT  
- **Expected:** PAYMENT.CONFIRMED_AT (nullable) + PAYMENT.STATUS_CODE; order has PAYMENT_CONFIRMED_AT mirrored; order lifecycle/status constraint  
- **Generated:** correctly explains payment confirmation timestamp/status and payment→order linkage and shipping dependency  
- **Analysis:** Correct modeling of confirmation and relationship semantics (even though order-mirroring nuance is described at concept level).  
- **Retrieval:** gt_coverage=1.0, top_score=0.7, gate=proceed

### Q012: How are shipments related to orders and warehouses?
- **Type:** multi_hop | **Difficulty:** medium  
- **Verdict:** CORRECT  
- **Expected:** SHIPMENT.ORDER_ID → SALES_ORDER_HDR; shipment includes warehouse code, tracking, status  
- **Generated:** many shipments to one order; comes from exactly one warehouse; includes tracking/status fields  
- **Analysis:** Correct relationship and warehouse linkage.  
- **Retrieval:** gt_coverage=1.0, top_score=0.9268, gate=proceed

### Q013: Can a product belong to multiple categories?
- **Type:** negative | **Difficulty:** easy  
- **Verdict:** CORRECT  
- **Expected:** No; product belongs to exactly one category (CATEGORY_ID FK in TB_PRODUCT)  
- **Generated:** “No” with exact “belongs to exactly one Category” justification  
- **Analysis:** Correct negative handling without fabrication.  
- **Retrieval:** gt_coverage=1.0, top_score=0.7, gate=proceed

### Q014: Is it possible for a customer to place an order without payment?
- **Type:** negative | **Difficulty:** medium  
- **Verdict:** CORRECT  
- **Expected:** Yes, order can exist without payment confirmation (PAYMENT_CONFIRMED_AT nullable); shipping blocked until payment confirmed  
- **Generated:** answers Yes; explains PAYMENT_CONFIRMED_AT nullable and focuses on shipping/business rules  
- **Analysis:** Correctly interprets “order can exist” vs “order can be shipped.”  
- **Retrieval:** gt_coverage=1.0, top_score=0.7, gate=proceed

### Q015: What schema fields support monetary value tracking across orders and their line items?
- **Type:** multi_hop | **Difficulty:** easy  
- **Verdict:** CORRECT  
- **Expected:** header total in SALES_ORDER_HDR.TOTAL_AMT; line pricing via ORDER_LINE_ITEM.UNIT_PRICE, QUANTITY, LINE_AMT (= Q×UP); reconcile via ORDER_ID  
- **Generated:** discusses unit_price + line_amt + qty at line-item level; also mentions payment.AMOUNT (slightly broader than expected)  
- **Analysis:** Core expected mapping is correct; adding payment-level field is not a contradiction.  
- **Retrieval:** gt_coverage=1.0, top_score=0.7, gate=proceed

## Anomalies & Recommendations

### Red Flags
- **None affecting correctness.** No grader rejections, no abstentions, no Cypher failures.
- Minor metric nuance: Several questions show `retrieval_quality_score_raw` around **0.55** while `retrieval_quality_score_adjusted` becomes **~0.7** due to pooling confidence application. This looks like an intended gating/normalization effect, but it can mask marginal retrieval degradation in harder studies.

### Recommendations
- For future ablation reporting, include an explicit `ablation_context` (changes vs baseline + expected impact) so the “Ablation Impact” dimension can be evaluated causally.
- Add instrumentation to expose, per question and per source type (vector/bm25/graph), how much each contributed to final context—this would help diagnose issues when grounded_rate drops in advanced settings.
- Keep an eye on negative-question behavior in harder datasets; this run shows perfect handling, likely aided by correct schema grounding.

## Comparison Notes (if applicable)
- No AB-00 baseline comparison data is present in the bundle (no `ablation_context`), so changes vs baseline cannot be verified. Performance is excellent on the provided configuration.