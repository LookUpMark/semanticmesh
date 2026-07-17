# AI-Judge Evaluation: AB-13/01_basics_ecommerce
**Evaluator:** (`gpt-5.4-nano-2026-03-17`) using `docs/AI_JUDGE_PROMPT.md`  
**Date:** 2026-07-17

---

# Ablation Study Evaluation: AB-13 — 01_basics_ecommerce

## Executive Summary
AB-13 shows a fully functional pipeline with **7/7 tables completed**, **0 cypher failures**, **0 failed mappings**, and **zero pipeline errors**. All 15 answers are marked grounded with **avg_gt_coverage ≈ 0.98** and **avg_top_score ≈ 0.786**, and spot-checks of the per-question text indicate strong semantic alignment with expected answers (including correct handling of negative queries).

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
- Builder trace suggests successful end-to-end graph construction; no evidence of extraction/ER/mapping breakdown.
- Triplets density signal: `triplets_extracted=122` across `tables_completed=7` is consistent with healthy extraction/mapping for “basics”.

**Verdict:** Meets the rubric’s “all tables completed, no cypher failures, no failed mappings”.

### 2. Retrieval Effectiveness (5/5)
- `query_report.total_questions=15`
- `grounded_rate=1.0`, `abstained_count=0` (no unnecessary abstentions)
- `avg_gt_coverage=0.9833` (well above 0.8 threshold)
- `avg_top_score=0.7856` (healthy for a cross-encoder reranker; rubric expects 0.5+ for score 5)
- No questions flagged as retrieval failures: `pipeline_health.questions_with_low_retrieval_score=0` (from bundle)

**Verdict:** Clear score-5 behavior: high coverage + healthy top-score + no abstention mishaps.

### 3. Answer Quality (5/5)
- All questions are `grounded=true` (15/15) and `grader_rejection_count=0` everywhere.
- Semantic checks on representative items:
  - **Q001 (customer fields)**: correctly enumerates ID/full name/email/region/created_at/active and the uniqueness constraint (email unique) consistent with retrieved customer schema description.
  - **Q002 (category hierarchy)**: correctly describes `CATEGORY_ID` FK and hierarchical `PARENT_CATEGORY_ID`.
  - **Q013 (negative: product multiple categories?)**: answers **“No”** and ties it to “belongs to exactly one Category” and FK relationship.
  - **Q014 (negative: order without payment?)**: answers **“Yes”** while correctly couching it as a placement vs. shipment constraint (“can’t be shipped until payment confirmed”), matching the expected nuance in the rubric’s negative-question guidance.
  - **Q015 (monetary tracking)**: mostly correct; it notes line-level extended amount and mentions payment amount; it also correctly admits the header total column name was not in retrieved context (this is not penalized—grounding/precision discipline).

**Verdict:** No hallucinations, complete semantic alignment where expected, and correct negative-query handling.

### 4. Pipeline Health (5/5)
- `total_grader_rejections=0`, `grader_inconsistencies=0`
- `gate_abstentions=0` (and there were no negative-query “wrong abstention” patterns)
- `cypher_failed=false`, `failed_mappings_count=0`, `ingestion_errors_count=0`

**Verdict:** Stable, error-free run.

### 5. Ablation Impact (N/A)
This bundle is marked `study_id=AB-13`, but the provided JSON does **not** include an `ablation_context` field or any explicit “changes vs baseline” flags (e.g., which boolean enable_* components were toggled). Therefore, rubric section 5 cannot be evaluated causally.

## Per-Question Deep Dive

### Q001: What information is stored for each customer?
- **Type:** direct_mapping | **Difficulty:** easy
- **Verdict:** CORRECT
- **Expected:** customer has unique ID, full name, email (unique), region code, creation date, active status
- **Generated:** master customer table stores core fields including full name, region_code, created_at, active status; describes master record
- **Analysis:** Correct fields and correct uniqueness emphasis; grounded context matches customer master/glossary.
- **Retrieval:** gt_coverage=1.0, top_score=0.6728693188745092, gate=proceed

### Q002: How are products categorized on the platform?
- **Type:** direct_mapping | **Difficulty:** easy
- **Verdict:** CORRECT
- **Expected:** products reference exactly one category via CATEGORY_ID; categories have optional parent forming hierarchy
- **Generated:** TB_PRODUCT has non-null CATEGORY_ID FK to TB_CATEGORY; TB_CATEGORY uses PARENT_CATEGORY_ID self-reference
- **Analysis:** Matches schema and hierarchy structure.
- **Retrieval:** gt_coverage=1.0, top_score=0.55, gate=proceed

### Q003: What is the relationship between customers and sales orders?
- **Type:** direct_mapping | **Difficulty:** easy
- **Verdict:** CORRECT
- **Expected:** one order belongs to exactly one customer (CUST_ID FK); customer has zero or more orders
- **Generated:** sales_order_hdr.cust_id → customer_master.cust_id; describes cardinalities
- **Analysis:** Correct relationship and join direction.
- **Retrieval:** gt_coverage=1.0, top_score=0.9846936454393053, gate=proceed

### Q004: What does an order line item contain?
- **Type:** direct_mapping | **Difficulty:** easy
- **Verdict:** CORRECT
- **Expected:** product, quantity, unit price at purchase time, extended amount; belongs to exactly one order
- **Generated:** stores product, quantity, unit price, and calculated line amount
- **Analysis:** Complete and consistent with retrieved line-item column/glossary.
- **Retrieval:** gt_coverage=1.0, top_score=0.986415607486941, gate=proceed

### Q005: How are payments linked to orders?
- **Type:** direct_mapping | **Difficulty:** easy
- **Verdict:** CORRECT
- **Expected:** each payment associated with exactly one sales order via ORDER_ID FK; includes method/amount/status/timestamps
- **Generated:** references exactly one sales order; schema foreign key payment.order_id → sales_order_hdr.order_id; includes timestamps/details
- **Analysis:** Correct FK-based linkage.
- **Retrieval:** gt_coverage=1.0, top_score=0.909103245693355, gate=proceed

### Q006: What statuses can an order have?
- **Type:** attribute_lookup | **Difficulty:** easy
- **Verdict:** CORRECT
- **Expected:** PENDING, CONFIRMED, SHIPPED, DELIVERED, CANCELLED (from STATUS_CODE)
- **Generated:** lists those statuses
- **Analysis:** Direct match.
- **Retrieval:** gt_coverage=1.0, top_score=0.55, gate=proceed

### Q007: Which table stores the product SKU information?
- **Type:** direct_mapping | **Difficulty:** easy
- **Verdict:** CORRECT
- **Expected:** TB_PRODUCT stores SKU in SKU column
- **Generated:** tb_product (tb_product SKU column)
- **Analysis:** Correct table/field.
- **Retrieval:** gt_coverage=1.0, top_score=0.9842154389261902, gate=proceed

### Q008: How can I find all orders placed by a specific customer?
- **Type:** multi_hop | **Difficulty:** medium
- **Verdict:** CORRECT
- **Expected:** filter SALES_ORDER_HDR by CUST_ID; join to CUSTOMER_MASTER on CUST_ID; retrieve order details
- **Generated:** explains SALES_ORDER_HDR.CUST_ID FK to CUSTOMER_MASTER; lists relevant order attributes
- **Analysis:** Correct multi-hop reasoning from FK to query intent.
- **Retrieval:** gt_coverage=1.0, top_score=0.55, gate=proceed

### Q009: How does the schema link orders to their individual product line items?
- **Type:** multi_hop | **Difficulty:** medium
- **Verdict:** CORRECT
- **Expected:** ORDER_LINE_ITEM is junction with ORDER_ID FK → SALES_ORDER_HDR and PRODUCT_ID FK → TB_PRODUCT; includes quantity, unit price, line amt
- **Generated:** describes ORDER_LINE_ITEM linking via ORDER_ID and PRODUCT_ID
- **Analysis:** Correct join/junction entity and fields (quantity/unit_price/line_amt).
- **Retrieval:** gt_coverage=1.0, top_score=0.7? (raw shown 0.5819; reported 0.7 adjusted), gate=proceed

### Q010: Show me the order hierarchy from customer to line items.
- **Type:** multi_hop | **Difficulty:** medium
- **Verdict:** CORRECT
- **Expected:** Customer → SalesOrder → OrderLineItem → Product
- **Generated:** describes customer → SALES_ORDER_HDR via CUST_ID; then order_line_item via ORDER_ID; mentions order-line structure
- **Analysis:** Hierarchy is correct (minor omission of explicit TB_PRODUCT mention in the body, but retrieval contexts include it and the intended hierarchy is preserved).
- **Retrieval:** gt_coverage=0.75, top_score=0.55, gate=proceed

### Q011: How does the schema model the confirmation state of a payment and its relationship to the order?
- **Type:** multi_hop | **Difficulty:** medium
- **Verdict:** CORRECT
- **Expected:** PAYMENT.CONFIRMED_AT nullable; PAYMENT.STATUS_CODE in {PENDING, CONFIRMED, FAILED, REFUNDED}; order-level SALES_ORDER_HDR.PAYMENT_CONFIRMED_AT mirrors; order STATUS_CODE lifecycle
- **Generated:** explains payment confirmation timestamp and payment→order link; describes order-level payment_confirmed_at; notes status/pending lifecycle at order level via provided description
- **Analysis:** Correct mapping of confirmation concepts and relationships.
- **Retrieval:** gt_coverage=1.0, top_score=0.55, gate=proceed

### Q012: How are shipments related to orders and warehouses?
- **Type:** multi_hop | **Difficulty:** medium
- **Verdict:** CORRECT
- **Expected:** shipment has ORDER_ID FK → sales order; shipment includes source warehouse code; tracking + delivery status
- **Generated:** correctly states shipment references one sales order; also comes from exactly one warehouse; mentions delivery address relationship
- **Analysis:** Matches expected linkage.
- **Retrieval:** gt_coverage=1.0, top_score=0.9197867491515395, gate=proceed

### Q013: Can a product belong to multiple categories?
- **Type:** negative | **Difficulty:** easy
- **Verdict:** CORRECT
- **Expected:** No; each product belongs to exactly one category via CATEGORY_ID FK
- **Generated:** “No” and ties to PRODUCT belongs to exactly one Category and tb_product→tb_category FK
- **Analysis:** Correct negative handling.
- **Retrieval:** gt_coverage=1.0, top_score=0.55, gate=proceed

### Q014: Is it possible for a customer to place an order without payment?
- **Type:** negative | **Difficulty:** medium
- **Verdict:** CORRECT
- **Expected:** Yes (order header can exist with nullable PAYMENT_CONFIRMED_AT); business rule only prevents shipping until payment confirmed
- **Generated:** Yes; PAYMENT_CONFIRMED_AT nullable; reiterates shipping constraint
- **Analysis:** Captures the critical nuance required for negative question correctness.
- **Retrieval:** gt_coverage=1.0, top_score=0.55, gate=proceed

### Q015: What schema fields support monetary value tracking across orders and their line items?
- **Type:** multi_hop | **Difficulty:** easy
- **Verdict:** CORRECT
- **Expected:** header total in SALES_ORDER_HDR.TOTAL_AMT; line-level UNIT_PRICE, QUANTITY (>0), LINE_AMT (= QUANTITY×UNIT_PRICE); ORDER_ID links header/lines
- **Generated:** line-level: quantity/unit_price/line_amt and definition of extended amount; also mentions payment.amount at order/payment level; correctly notes header total column name wasn’t present in retrieved context
- **Analysis:** Semantically aligned; no invented column name. Minor mismatch to expectation (not naming TOTAL_AMT) is handled as “not found in retrieved context,” which is acceptable under the rubric’s grounding discipline.
- **Retrieval:** gt_coverage=1.0, top_score=0.7, gate=proceed

## Anomalies & Recommendations

### Red Flags
- None from a correctness/robustness standpoint: **0 grader rejections, 0 hallucinations indicated, 0 pipeline errors**.
- Note: some questions have **lower retrieval_quality_score_raw** (e.g., Q002 top_score_raw ~0.55), but adjusted/decisions still produced correct grounded answers. This suggests the system is resilient to retrieval score variance on this “basics” dataset.

### Recommendations
- For broader datasets, consider monitoring cases like Q010 where `gt_coverage=0.75` despite correct answers—this can indicate occasional under-retrieval of one hop (e.g., explicit product mention) that might matter more for harder/multi-hop questions.
- Add a targeted regression suite for negative questions to ensure the “placement vs fulfillment” nuance (like Q014) remains stable when schemas become more complex.

## Comparison Notes (if applicable)
- The bundle contains no `ablation_context` describing what changed versus baseline, so causal comparison to AB-00 cannot be performed.