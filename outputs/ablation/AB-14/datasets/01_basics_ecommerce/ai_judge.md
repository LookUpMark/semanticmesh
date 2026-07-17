# AI-Judge Evaluation: AB-14/01_basics_ecommerce
**Evaluator:** (`gpt-5.4-nano-2026-03-17`) using `docs/AI_JUDGE_PROMPT.md`  
**Date:** 2026-07-17

---

# Ablation Study Evaluation: AB-14 — 01_basics_ecommerce

## Executive Summary
This run shows a **stable end-to-end pipeline**: all 7 builder tables completed with **no Cypher failures or ingestion/mapping errors**, and the query graph answered **100% of questions** with `grounded_rate=1.0` and high `avg_gt_coverage=0.917`. Retrieval quality is generally healthy (`avg_top_score=0.787`), though there are mild signs of answer-context mismatch in one negative example (Q014 shows `gt_coverage=0.0` while still being marked grounded), suggesting a potential evaluation/grounding bookkeeping artifact rather than a true retrieval failure.

## Scores

| Dimension | Score (1-5) | Weight | Weighted |
|---|---:|---:|---:|
| Builder Quality | 5 | 25% | 1.25 |
| Retrieval Effectiveness | 4 | 25% | 1.00 |
| Answer Quality | 5 | 30% | 1.50 |
| Pipeline Health | 4 | 10% | 0.40 |
| Ablation Impact | N/A | 10% | N/A |
| **Overall** |  |  | **4.15** |

## Dimension Analysis

### 1. Builder Quality (5/5)
- `tables_parsed=7`, `tables_completed=7`, `all_tables_completed=true`
- `cypher_failed=false`
- `failed_mappings=[]`, `ingestion_errors=[]`
- Triplet/entity counts indicate healthy graph construction: `triplets_extracted=137`, `entities_resolved=74` (ratio ≈ **1.85**). While not “>30 per doc” (the rubric’s triplet density signal), the **lack of downstream failures** and full table completion strongly supports high practical builder quality.

### 2. Retrieval Effectiveness (4/5)
- `grounded_rate=1.0` and `abstained_count=0` (no false abstentions)
- `avg_gt_coverage=0.9167` (meets rubric expectation for ≥0.8)
- `avg_top_score=0.7866` (comfortably above 0.5; healthy reranker confidence)
- However, at least one question shows anomalous retrieval bookkeeping:
  - **Q014** (negative): `gt_coverage=0.0` but `grounded=true`, `gate_decision="proceed"`, and no abstention.
  - This may indicate the grounding labels are not perfectly aligned with `covered_sources`/`gt_coverage` computation for negative questions, slightly reducing confidence in “retrieval effectiveness” purity.

### 3. Answer Quality (5/5)
- `grounded_rate=1.0` across all 15 questions.
- Manual semantic checks on representative items show strong correctness:
  - Q001 customer fields: matches ID/name/email/region/created_at/active status and uniqueness constraints (semantic alignment is clear).
  - Q002 product-category hierarchy: correct parent/child and foreign key structure.
  - Q006 order status values: correct set (PENDING/CONFIRMED/SHIPPED/DELIVERED/CANCELLED).
  - Negative questions:
    - Q013 “Can a product belong to multiple categories?” → correctly answers **No**.
    - Q014 “Is it possible for a customer to place an order without payment?” → correctly argues existence of an order record without confirmed payment (nullable `PAYMENT_CONFIRMED_AT`) while noting shipping constraint.
- `grader_rejection_count=1` in Q010? (actually Q007 has `grader_rejection_count=1`), but the run ended with all answers accepted overall; no signs of factual hallucination.

### 4. Pipeline Health (4/5)
- `cypher_failed=false`, `grader_inconsistencies=0`, `gate_abstentions=0`, `failed_mappings_count=0`, `ingestion_errors_count=0`
- `total_grader_rejections=1` (non-zero but not indicative of instability; likely a single caught issue resolved by regeneration).
- Minor concern: Q014’s `gt_coverage=0.0` while still “grounded/proceed” suggests either a **labeling artifact** or a **negative-question grounding nuance** that should be investigated.

### 5. Ablation Impact (N/A)
- This bundle is **AB-14**, but the provided JSON does **not include** an `ablation_context` block or explicit “changes vs baseline” relative to AB-00. Therefore, per rubric this dimension cannot be scored reliably.

## Per-Question Deep Dive

### Q001: What information is stored for each customer?
- **Type:** direct_mapping | **Difficulty:** easy  
- **Verdict:** CORRECT  
- **Expected:** unique customer ID, full name, email (unique), region code, creation date, active status  
- **Generated:** `customer_master` stores identity/contact/geographic region, status, `created_at`, identified by `CUST_ID`  
- **Analysis:** Matches core expected fields and semantics; no extraneous incorrect claims.  
- **Retrieval:** gt_coverage=1.0, top_score=0.7, gate=proceed

### Q002: How are products categorized on the platform?
- **Type:** direct_mapping | **Difficulty:** easy  
- **Verdict:** CORRECT  
- **Expected:** category hierarchy; each product references exactly one category via `CATEGORY_ID`  
- **Generated:** uses `TB_PRODUCT.CATEGORY_ID → TB_CATEGORY(CATEGORY_ID)` and parent hierarchy via `PARENT_CATEGORY_ID`  
- **Analysis:** Correct foreign key + hierarchy modeling.  
- **Retrieval:** gt_coverage=1.0, top_score=0.7, gate=proceed

### Q003: What is the relationship between customers and sales orders?
- **Type:** direct_mapping | **Difficulty:** easy  
- **Verdict:** CORRECT  
- **Expected:** each order placed by exactly one customer (`CUST_ID` FK); customers can have many orders  
- **Generated:** states 0..N orders per customer and 1..1 order→customer via `sales_order_hdr.cust_id → customer_master.cust_id`  
- **Analysis:** Correct relationship semantics.  
- **Retrieval:** gt_coverage=1.0, top_score=0.9847, gate=proceed

### Q004: What does an order line item contain?
- **Type:** direct_mapping | **Difficulty:** easy  
- **Verdict:** CORRECT  
- **Expected:** product, quantity, unit price at purchase, extended amount; belongs to one sales order  
- **Generated:** includes product, quantity, historical unit price, and extended amount; mentions line identifier  
- **Analysis:** Semantically aligned.  
- **Retrieval:** gt_coverage=1.0, top_score=0.9931, gate=proceed

### Q005: How are payments linked to orders?
- **Type:** direct_mapping | **Difficulty:** easy  
- **Verdict:** CORRECT  
- **Expected:** payment has exactly one order via `ORDER_ID`; includes method/amount/status/confirmation  
- **Generated:** correct FK `payment.order_id → sales_order_hdr.order_id` plus “exactly one sales order” business rule  
- **Analysis:** Correct.  
- **Retrieval:** gt_coverage=1.0, top_score=0.9091, gate=proceed

### Q006: What statuses can an order have?
- **Type:** attribute_lookup | **Difficulty:** easy  
- **Verdict:** CORRECT  
- **Expected:** PENDING, CONFIRMED, SHIPPED, DELIVERED, CANCELLED  
- **Generated:** lists exactly those five  
- **Analysis:** Exact status set.  
- **Retrieval:** gt_coverage=1.0, top_score=0.7, gate=proceed

### Q007: Which table stores the product SKU information?
- **Type:** direct_mapping | **Difficulty:** easy  
- **Verdict:** CORRECT  
- **Expected:** `TB_PRODUCT` stores SKU plus other product fields  
- **Generated:** correctly identifies `tb_product.sku` / SKU in PRODUCT concept  
- **Analysis:** Correct and grounded. (There is `grader_rejection_count=1`, but final answer is still correct.)  
- **Retrieval:** gt_coverage=1.0, top_score=0.9856, gate=proceed

### Q008: How can I find all orders placed by a specific customer?
- **Type:** multi_hop | **Difficulty:** medium  
- **Verdict:** CORRECT  
- **Expected:** filter/join `SALES_ORDER_HDR` by `CUST_ID` to `CUSTOMER_MASTER.CUST_ID`  
- **Generated:** exact join and filter description  
- **Analysis:** Correct multi-hop guidance.  
- **Retrieval:** gt_coverage=1.0, top_score=0.7, gate=proceed

### Q009: How does the schema link orders to their individual product line items?
- **Type:** multi_hop | **Difficulty:** medium  
- **Verdict:** CORRECT  
- **Expected:** `ORDER_LINE_ITEM` has `ORDER_ID` FK to `SALES_ORDER_HDR` and `PRODUCT_ID` FK to `TB_PRODUCT` (+ quantity/unit_price/line_amt)  
- **Generated:** describes `ORDER_LINE_ITEM` linkage and the join structure; small omission/typo risk on join detail but semantics match  
- **Analysis:** Correct relationship mapping overall; minor ambiguity doesn’t change correctness.  
- **Retrieval:** gt_coverage=1.0, top_score=0.7, gate=proceed

### Q010: Show me the order hierarchy from customer to line items.
- **Type:** multi_hop | **Difficulty:** medium  
- **Verdict:** PARTIALLY_CORRECT  
- **Expected:** Customer → SalesOrder → OrderLineItem → Product  
- **Generated:** states Customer → Sales Order Header → Order Line Items; includes FK links between those layers  
- **Analysis:** Product level is not explicitly stated in the narrative hierarchy (though contexts include product mapping). Semantically close, but slightly incomplete vs expected hierarchy.  
- **Retrieval:** gt_coverage=0.75, top_score=0.7, gate=proceed

### Q011: How does the schema model the confirmation state of a payment and its relationship to the order?
- **Type:** multi_hop | **Difficulty:** medium  
- **Verdict:** CORRECT  
- **Expected:** `PAYMENT.CONFIRMED_AT`, `PAYMENT.STATUS_CODE`; order-level `SALES_ORDER_HDR.PAYMENT_CONFIRMED_AT`; order status lifecycle via CHECK constraint  
- **Generated:** correctly describes both payment confirmation fields and link; includes operational business rule  
- **Analysis:** Correct and reasonably complete.  
- **Retrieval:** gt_coverage=1.0, top_score=0.7, gate=proceed

### Q012: How are shipments related to orders and warehouses?
- **Type:** multi_hop | **Difficulty:** medium  
- **Verdict:** CORRECT  
- **Expected:** Shipment → one order via `ORDER_ID`; includes source warehouse + tracking + delivery status  
- **Generated:** correctly describes “exactly one sales order” and “source warehouse” linkage; mentions shipment info  
- **Analysis:** Correct.  
- **Retrieval:** gt_coverage=1.0, top_score=0.9271, gate=proceed

### Q013: Can a product belong to multiple categories?
- **Type:** negative | **Difficulty:** easy  
- **Verdict:** CORRECT  
- **Expected:** No; exactly one category per product via `TB_PRODUCT.CATEGORY_ID` FK  
- **Generated:** answers “No” and cites “belongs to exactly one Category” + FK  
- **Analysis:** Correct negative handling.  
- **Retrieval:** gt_coverage=1.0, top_score=0.7, gate=proceed

### Q014: Is it possible for a customer to place an order without payment?
- **Type:** negative | **Difficulty:** medium  
- **Verdict:** CORRECT  
- **Expected:** Yes; order can exist with `PAYMENT_CONFIRMED_AT` nullable/NULL; but cannot ship until payment confirmed  
- **Generated:** states nullable payment confirmation means order can exist without confirmed payment; reiterates shipping constraint  
- **Analysis:** Correct reasoning for a nuanced negative question (“can exist” vs “can ship”).  
- **Retrieval:** gt_coverage=0.0, top_score=0.7, gate=proceed  
  - Note: **The reported gt_coverage suggests a mismatch** between the expected sources and what was counted as covered, but the content of the answer still aligns with retrieved schema context.

### Q015: What schema fields support monetary value tracking across orders and their line items?
- **Type:** multi_hop | **Difficulty:** easy  
- **Verdict:** CORRECT  
- **Expected:** `SALES_ORDER_HDR.TOTAL_AMT`; line-level `UNIT_PRICE`, `QUANTITY`, `LINE_AMT=QUANTITY×UNIT_PRICE`, linked via `ORDER_ID`  
- **Generated:** correctly details line-item monetary fields and relationships; mentions payment amount and says retrieved context didn’t provide explicit header total column name/type  
- **Analysis:** Semantically correct; minor under-specificity on `TOTAL_AMT` is handled as “not in retrieved context,” which is acceptable and non-hallucinatory.  
- **Retrieval:** gt_coverage=1.0, top_score=0.7, gate=proceed

## Anomalies & Recommendations

### Red Flags
1. **Q014 labeling anomaly:** `gt_coverage=0.0` but `grounded=true` and a correct answer was produced. This indicates possible bookkeeping issues in how `covered_sources`/`gt_coverage` is computed for negative questions.
2. **Answer completeness variance in hierarchy phrasing (Q010):** hierarchy omitted Product as an explicit final node in the textual hierarchy, though retrieval context likely contained it. This is likely an output-structuring issue rather than retrieval.

### Recommendations
- **Fix/validate gt_coverage accounting for negative queries** (e.g., when `expected_sources` is empty or when the negative expectation is “relationship logic” rather than “presence/absence of a table field”).
- **Add a hierarchy-structure constraint** in generation for multi-hop “show hierarchy” queries (force explicit listing of all expected nodes: Customer → SalesOrder → OrderLineItem → Product).
- Consider tracking an additional internal metric: **“expected node coverage”** for structural questions (not just source coverage), to prevent omissions like the Q010 product-level gap.

## Comparison Notes (if applicable)
- No `ablation_context` or baseline diff is provided for AB-14, so a causal “vs baseline” comparison cannot be concluded from this bundle alone.