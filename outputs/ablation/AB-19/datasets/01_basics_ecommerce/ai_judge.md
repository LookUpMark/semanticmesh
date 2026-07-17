# AI-Judge Evaluation: AB-19/01_basics_ecommerce
**Evaluator:** (`gpt-5.4-nano-2026-03-17`) using `docs/AI_JUDGE_PROMPT.md`  
**Date:** 2026-07-17

---

# Ablation Study Evaluation: AB-19 — 01_basics_ecommerce

## Executive Summary
AB-19 shows **excellent end-to-end query behavior** on the 15 “basics” e-commerce questions: **100% grounded answers**, **no abstentions**, and **0 grader rejections/inconsistencies**. However, the **builder pipeline reports `cypher_failed: true` despite `all_tables_completed=true` and `failed_mappings/ingestion_errors` being zero**, which is internally inconsistent and suggests either (a) a recoverable Cypher error occurred during a non-critical sub-step, or (b) the flag is not accurately logged.

Overall, the pipeline’s *semantic retrieval + answer generation* looks very strong for this dataset, with the main concern being the **builder-health telemetry around Cypher failure**.

## Scores

| Dimension | Score (1-5) | Weight | Weighted |
|---|---:|---:|---:|
| Builder Quality | 4 | 25% | 1.00 |
| Retrieval Effectiveness | 4 | 25% | 1.00 |
| Answer Quality | 5 | 30% | 1.50 |
| Pipeline Health | 3 | 10% | 0.30 |
| Ablation Impact | N/A | 10% | 0.00 |
| **Overall** |  |  | **3.80** |

## Dimension Analysis

### 1. Builder Quality (4/5)
- **Tables parsed/completed:** `tables_parsed=7`, `tables_completed=7`, `all_tables_completed=true`
- **Mapping failures:** `failed_mappings=[]`, `ingestion_errors=[]`
- **Triplets/entities:** `triplets_extracted=109`, `entities_resolved=69` → ratio ≈ **1.58**
  - This is **not** “>30 per doc” as the rubric’s ideal signal, but the rubric also emphasizes correct completion/no failures. Here, mapping completed cleanly, so extraction density may be modest but not catastrophic.
- **Cypher flag:** `builder_report.cypher_failed=true` while still completing all tables and having no failed mappings.
  - Since healing/fallback isn’t described in the bundle fields, we can’t confirm how catastrophic this was; we must downgrade from a perfect score due to the **Cypher-failure telemetry**.

**Verdict:** Builder seems operational overall (all tables done, no mapping/ingestion failures), but the Cypher failure flag prevents a 5.

### 2. Retrieval Effectiveness (4/5)
- **Ground-truth retrieval:** `avg_gt_coverage=0.9833` (very high)
- **Reranker confidence:** `avg_top_score=0.7850` (healthy; rubric expects ~0.5+)
- **Low retrieval questions:** `questions_with_low_retrieval_score=0`
- **Abstentions:** `abstained_count=0`, and no negative questions were wrongfully answered (see Q013, Q014).

Raw retrieval quality behavior in samples:
- Many questions show `retrieval_quality_score_adjusted` around **0.7** or much higher (e.g., Q003 ≈ 0.985, Q004 ≈ 0.954).
- The only visible “weaker” multi-hop coverage is **Q010** with `gt_coverage=0.75`, but it is still grounded and answered correctly.

**Verdict:** Retrieval is strong across the board; minor deduction for the couple lower-coverage multi-hop cases (not severe enough to drop to 3).

### 3. Answer Quality (5/5)
- **Grounded rate:** `grounded_rate=1.0` with `grounded=true` for each shown question.
- **Semantic correctness vs expected:** For the listed queries, the generated answers match the expected facts (relationships, foreign keys, field meanings, status sets, and negative constraints).
- **Self-critique stability:** `grader_rejection_count=0` across questions and `grader_consistency_valid=true`.
- **Negative handling:**  
  - **Q013 (negative):** “Can a product belong to multiple categories?” → correctly answers **No**, grounded in “belongs to exactly one Category” and the FK.
  - **Q014 (negative):** “Is it possible for a customer to place an order without payment?” → answers **Yes** (order record exists with nullable `PAYMENT_CONFIRMED_AT`), and correctly distinguishes “can’t ship until payment confirmed.”

**Best signals:** no hallucination interventions; answers consistently align with schema/glossary content.

### 4. Pipeline Health (3/5)
- `pipeline_health.total_grader_rejections=0`, `grader_inconsistencies=0`, `gate_abstentions=0` → good.
- **But** `cypher_failed=true` is present in both `builder_report` and `pipeline_health`.
- Yet, simultaneously:
  - `builder_report.all_tables_completed=true`
  - `failed_mappings=[]`
  - `ingestion_errors=[]`

This suggests one of:
1) Cypher healing failed but system recovered via deterministic fallback (but no explicit “heal_cypher” metadata is given), **or**
2) `cypher_failed` is a coarse boolean set during an intermediate attempt even though final ingestion succeeded, **or**
3) Logging mismatch.

Because we cannot verify recovery outcome from the provided bundle fields, we rate pipeline health as **moderate** rather than 5.

### 5. Ablation Impact (N/A)
- The bundle is **AB-19**, but the JSON provided does **not** include an `ablation_context` or “changes_vs_baseline” description.
- Therefore, per rubric, Ablation Impact cannot be scored.

## Per-Question Deep Dive

### Q001: What information is stored for each customer?
- **Type:** direct_mapping | **Difficulty:** easy
- **Verdict:** CORRECT
- **Expected:** unique customer ID, full name, unique email, region code, creation date, active status; email unique
- **Generated:** customer_master stores customer identity (CUST_ID), contact details, region_code, created_at, is_active
- **Analysis:** Correct mapping of customer fields; properly identifies PK/fields. Email uniqueness not explicitly restated, but schema description supports uniqueness intent and no contradiction appears.
- **Retrieval:** gt_coverage=1.0, top_score=0.6391731867145634, gate=proceed

### Q002: How are products categorized on the platform?
- **Type:** direct_mapping | **Difficulty:** easy
- **Verdict:** CORRECT
- **Expected:** each product references exactly one category; categories can have parents (hierarchy)
- **Generated:** product has non-null CATEGORY_ID FK to TB_CATEGORY; parent hierarchy via PARENT_CATEGORY_ID self-reference
- **Analysis:** Fully consistent with schema/glossary; includes hierarchy detail.
- **Retrieval:** gt_coverage=1.0, top_score=0.55, gate=proceed

### Q003: What is the relationship between customers and sales orders?
- **Type:** direct_mapping | **Difficulty:** easy
- **Verdict:** CORRECT
- **Expected:** each order placed by exactly one customer via CUST_ID FK; customer can have zero or more orders
- **Generated:** exactly-one customer per order; customer places zero-or-more orders; FK description matches
- **Analysis:** Correct directionality and cardinality.
- **Retrieval:** gt_coverage=1.0, top_score=0.9846936454393053, gate=proceed

### Q004: What does an order line item contain?
- **Type:** direct_mapping | **Difficulty:** easy
- **Verdict:** CORRECT
- **Expected:** product, quantity, unit price at purchase time, extended amount; belongs to exactly one order
- **Generated:** product, quantity, unit price, line amount/total amount; stored in order_line_item; line item belongs to exactly one order
- **Analysis:** Correct set of fields and FK-based belonging.
- **Retrieval:** gt_coverage=1.0, top_score=0.953621794005189, gate=proceed

### Q005: How are payments linked to orders?
- **Type:** direct_mapping | **Difficulty:** easy
- **Verdict:** CORRECT
- **Expected:** each payment associated with exactly one sales order via ORDER_ID; payment method/amount/status/timestamps
- **Generated:** payment.order_id → sales_order_hdr.order_id; payment references exactly one sales order; mentions confirmation timestamp/status/amount
- **Analysis:** Correct FK-based linkage.
- **Retrieval:** gt_coverage=1.0, top_score=0.909103245693355, gate=proceed

### Q006: What statuses can an order have?
- **Type:** attribute_lookup | **Difficulty:** easy
- **Verdict:** CORRECT
- **Expected:** PENDING, CONFIRMED, SHIPPED, DELIVERED, CANCELLED
- **Generated:** lists exactly those five statuses
- **Analysis:** Matches expected lifecycle.
- **Retrieval:** gt_coverage=1.0, top_score=0.7, gate=proceed

### Q007: Which table stores the product SKU information?
- **Type:** direct_mapping | **Difficulty:** easy
- **Verdict:** CORRECT
- **Expected:** TB_PRODUCT stores SKU code (plus name/category/price/active)
- **Generated:** `tb_product` has SKU attribute
- **Analysis:** Correct table attribution.
- **Retrieval:** gt_coverage=1.0, top_score=0.9883577758353339, gate=proceed

### Q008: How can I find all orders placed by a specific customer?
- **Type:** multi_hop | **Difficulty:** medium
- **Verdict:** CORRECT
- **Expected:** filter SALES_ORDER_HDR by CUST_ID; join to CUSTOMER_MASTER on CUST_ID
- **Generated:** uses SALES_ORDER_HDR and filter on CUST_ID FK; mentions ORDER_ID and fields like ORDER_DATE/TOTAL_AMT/STATUS_CODE
- **Analysis:** Correct join/filter reasoning for multi-hop.
- **Retrieval:** gt_coverage=1.0, top_score=0.7, gate=proceed

### Q009: How does the schema link orders to their individual product line items?
- **Type:** multi_hop | **Difficulty:** medium
- **Verdict:** CORRECT
- **Expected:** junction via ORDER_LINE_ITEM; ORDER_ID FK to SALES_ORDER_HDR; PRODUCT_ID FK to TB_PRODUCT; includes quantity/unit_price/line_amt
- **Generated:** links via order_line_item.order_id ↔ sales_order_hdr.order_id and product_id ↔ tb_product.product_id; mentions line amount fields
- **Analysis:** Correct multi-hop junction entity explanation.
- **Retrieval:** gt_coverage=1.0, top_score=0.7, gate=proceed

### Q010: Show me the order hierarchy from customer to line items.
- **Type:** multi_hop | **Difficulty:** medium
- **Verdict:** CORRECT
- **Expected:** Customer → SalesOrder → OrderLineItem → Product
- **Generated:** CUSTOMER_MASTER → SALES_ORDER_HDR → ORDER_LINE_ITEM; includes product_id and line fields
- **Analysis:** Captures the hierarchy correctly despite `gt_coverage=0.75`.
- **Retrieval:** gt_coverage=0.75, top_score=0.7, gate=proceed

### Q011: How does the schema model the confirmation state of a payment and its relationship to the order?
- **Type:** multi_hop | **Difficulty:** medium
- **Verdict:** CORRECT
- **Expected:** PAYMENT.CONFIRMED_AT nullable and PAYMENT.STATUS_CODE values; SALES_ORDER_HDR.PAYMENT_CONFIRMED_AT mirrors; order lifecycle statuses defined
- **Generated:** explains PAYMENT confirmation via confirmed timestamp + status allowed values; explains Payment references exactly one Sales Order; includes sales_order_hdr.payment_confirmed_at and shipping restriction
- **Analysis:** Consistent with expected state modeling; does not contradict allowed statuses even if it doesn’t enumerate all order statuses in the excerpt.
- **Retrieval:** gt_coverage=1.0, top_score=0.7, gate=proceed

### Q012: How are shipments related to orders and warehouses?
- **Type:** multi_hop | **Difficulty:** medium
- **Verdict:** CORRECT
- **Expected:** SHIPMENT.ORDER_ID → SALES_ORDER_HDR; shipment includes warehouse code, tracking, delivery status
- **Generated:** shipments reference one sales order; shipments include source warehouse/warehouse code as part of shipment record
- **Analysis:** Correct linkage and warehouse association.
- **Retrieval:** gt_coverage=1.0, top_score=0.9386884633979415, gate=proceed

### Q013: Can a product belong to multiple categories?
- **Type:** negative | **Difficulty:** easy
- **Verdict:** CORRECTLY_ABSTAINED? (No — it answered correctly)
- **Expected:** No; product belongs to exactly one category (FK)
- **Generated:** “No”; references “belongs to exactly one Category” and single FK category_id
- **Analysis:** Correct negative constraint response (not abstaining, but correct).
- **Retrieval:** gt_coverage=1.0, top_score=0.7, gate=proceed

### Q014: Is it possible for a customer to place an order without payment?
- **Type:** negative | **Difficulty:** medium
- **Verdict:** CORRECT
- **Expected:** Yes, order can exist with nullable PAYMENT_CONFIRMED_AT; payment links via ORDER_ID, but shipping requires payment confirmation
- **Generated:** Yes; emphasizes nullable payment confirmation at order header; shipping restricted by business rules
- **Analysis:** Matches expected nuance: order record vs shipping eligibility.
- **Retrieval:** gt_coverage=1.0, top_score=0.7, gate=proceed

### Q015: What schema fields support monetary value tracking across orders and their line items?
- **Type:** multi_hop | **Difficulty:** easy
- **Verdict:** CORRECT
- **Expected:** TOTAL_AMT in SALES_ORDER_HDR; UNIT_PRICE + LINE_AMT in ORDER_LINE_ITEM; linked via ORDER_ID
- **Generated:** explains line-level UNIT_PRICE and LINE_AMT=QUANTITY×UNIT_PRICE; notes ORDER_ID linkage; also mentions PAYMENT.AMOUNT for order-level money applied
- **Analysis:** Correct for expected fields; extra mention of PAYMENT.AMOUNT is acceptable and likely grounded.
- **Retrieval:** gt_coverage=1.0, top_score=0.7, gate=proceed

## Anomalies & Recommendations

### Red Flags
- **Internal inconsistency / logging concern:** `builder_report.cypher_failed=true` and `pipeline_health.cypher_failed=true`, yet:
  - `builder_report.all_tables_completed=true`
  - `failed_mappings=[]`
  - `ingestion_errors=[]`
  This is the only meaningful warning sign in an otherwise strong run.
- **Extraction density signal:** `triplets_extracted=109` with `entities_resolved=69` gives a ratio ~1.58, which is far below the rubric’s “triplet density > 30 per doc” ideal indicator. Despite that, retrieval still worked well—suggesting the small dataset may not stress extraction much.

### Recommendations
1. **Clarify Cypher failure semantics**
   - Log both: “cypher attempted/failed” vs “final upsert succeeded”.
   - Record whether healing loop succeeded and whether deterministic fallback was used.
2. **Improve builder telemetry granularity**
   - Include counts for: cypher_heal_success, cypher_fallback_success, deterministic_builder_used.
3. **Re-check extraction yield thresholds**
   - If triplet/ER density is truly low due to extraction truncation, consider raising extraction max triplets or tuning extraction prompt to yield more structured triplets.
4. **Multi-hop retrieval robustness**
   - Q010 has `gt_coverage=0.75`; if multi-hop is targeted in future datasets (advanced complexity), consider monitoring graph traversal retrieval contribution and MENTIONS edge quality.

## Comparison Notes (if applicable)
- **No baseline comparison data provided** (no `ablation_context` or changes-vs-baseline), so this evaluation cannot attribute effects to specific ablation flag changes beyond what’s shown in `config`.

If you want, I can also compute an explicit per-type summary (direct_mapping vs multi_hop vs negative) from the bundle, but the provided results already indicate uniformly high correctness.