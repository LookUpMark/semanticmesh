# AI-Judge Evaluation: AB-05/01_basics_ecommerce
**Evaluator:** (`gpt-5.4-nano-2026-03-17`) using `docs/AI_JUDGE_PROMPT.md`  
**Date:** 2026-07-17

---

# Ablation Study Evaluation: AB-05 — 01_basics_ecommerce

## Executive Summary
AB-05 shows excellent end-to-end performance on the E-Commerce basics dataset: all 7 builder tables completed successfully with no Cypher failures or ingestion errors, and all 15 questions were answered with full grounded coverage (grounded_rate=1.0) and perfect ground-truth source retrieval (avg_gt_coverage=1.0). Retrieval confidence is consistently strong (avg_top_score≈0.78) and the pipeline exhibits perfect health signals (0 grader rejections, 0 abstentions, 0 inconsistencies). Overall, this run reflects a stable and semantically correct GraphRAG pipeline.

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
- `tables_completed=7`, `all_tables_completed=true`
- `cypher_failed=false`, `failed_mappings=[]`
- `ingestion_errors=[]`
- Triplet extraction: `triplets_extracted=112` (reasonable for 7 tables in a basics dataset)
- Overall: Builder Graph construction is fully successful with no recoverable or unrecoverable failures.

### 2. Retrieval Effectiveness (5/5)
- `grounded_rate=1.0`, `abstained_count=0`
- `avg_gt_coverage=1.0` across all questions (ground-truth sources are always retrieved)
- `avg_top_score=0.7798` (healthy confidence for cross-encoder reranking)
- `pipeline_health.questions_with_low_retrieval_score=0`
- No evidence of negative-question retrieval miss (there are negative queries, and they are handled correctly—see Q013, Q014).

### 3. Answer Quality (5/5)
- All 15 answers are semantically correct and grounded; `grounded_count=15` and `grader_rejection_count=0`.
- The generated answers correctly capture schema constraints and relationships (FKs, hierarchy, junction behavior, statuses, and monetary tracking fields).
- Negative questions are handled appropriately:
  - Q013 (“multiple categories”) correctly answers “No”
  - Q014 (“order without payment”) answers “Yes” with an explanation tied to nullable payment confirmation; this matches the expected answer logic in the bundle.

**Best and worst examples (representative):**
- **Best (high quality, schema-precise):** Q002, Q011, Q012, Q015 — exact field-level modeling with correct semantics.
- **Worst (still correct):** Q006 and Q014 are comparatively shorter/more summary-like, but remain fully correct vs expected answers and do not hallucinate.

### 4. Pipeline Health (5/5)
- `total_grader_rejections=0`
- `grader_inconsistencies=0`
- `gate_abstentions=0`
- `cypher_failed=false`, `failed_mappings_count=0`, `ingestion_errors_count=0`
- Latency is reported as 0s in bundle fields, but functionally there are no operational issues recorded.

### 5. Ablation Impact (N/A)
- This bundle is labeled AB-05, but it does not include any “changes_vs_baseline” context or explicit baseline (AB-00) comparison fields in the provided JSON. Therefore, ablation impact cannot be causally assessed per rubric.

## Per-Question Deep Dive

### Q001: What information is stored for each customer?
- **Type:** direct_mapping | **Difficulty:** easy
- **Verdict:** CORRECT
- **Expected:** ID, full name, unique email, region code, creation date, active status; email unique
- **Generated:** Full schema/field list from `CUSTOMER_MASTER` with correct meanings (CUST_ID, FULL_NAME, EMAIL, REGION_CODE, CREATED_AT, IS_ACTIVE) and uniqueness notion for email
- **Analysis:** Correct and field-accurate; no incorrect claims.
- **Retrieval:** gt_coverage=1.0, top_score=0.7209, gate=proceed

### Q002: How are products categorized on the platform?
- **Type:** direct_mapping | **Difficulty:** easy
- **Verdict:** CORRECT
- **Expected:** One category per product; hierarchical categories via parent pointer; product references exactly one CATEGORY_ID
- **Generated:** Correctly describes `TB_PRODUCT.CATEGORY_ID → TB_CATEGORY.CATEGORY_ID` and `TB_CATEGORY.PARENT_CATEGORY_ID`
- **Analysis:** Matches expected hierarchy and FK structure.
- **Retrieval:** gt_coverage=1.0, top_score=0.7000, gate=proceed

### Q003: What is the relationship between customers and sales orders?
- **Type:** direct_mapping | **Difficulty:** easy
- **Verdict:** CORRECT
- **Expected:** Each order references exactly one customer via CUST_ID; customer can have zero or more orders
- **Generated:** Explains FK and cardinality correctly
- **Analysis:** Semantically aligned with expected.
- **Retrieval:** gt_coverage=1.0, top_score=0.9847, gate=proceed

### Q004: What does an order line item contain?
- **Type:** direct_mapping | **Difficulty:** easy
- **Verdict:** CORRECT
- **Expected:** product, quantity, unit price at purchase time, extended amount; belongs to exactly one sales order
- **Generated:** Correctly describes `ORDER_LINE_ITEM` columns and semantics (QUANTITY, UNIT_PRICE, LINE_AMT) and order linkage via ORDER_ID
- **Analysis:** Fully correct.
- **Retrieval:** gt_coverage=1.0, top_score=0.9736, gate=proceed

### Q005: How are payments linked to orders?
- **Type:** direct_mapping | **Difficulty:** easy
- **Verdict:** CORRECT
- **Expected:** Payment has exactly one sales order via PAYMENT.ORDER_ID → SALES_ORDER_HDR.ORDER_ID; tracks method/amount/status/confirmation
- **Generated:** Correct FK mapping and relationship description
- **Analysis:** Correct.
- **Retrieval:** gt_coverage=1.0, top_score=0.9633, gate=proceed

### Q006: What statuses can an order have?
- **Type:** attribute_lookup | **Difficulty:** easy
- **Verdict:** CORRECT
- **Expected:** PENDING, CONFIRMED, SHIPPED, DELIVERED, CANCELLED (lifecycle)
- **Generated:** Provides same set via `SALES_ORDER_HDR.STATUS_CODE` and glossary alignment
- **Analysis:** Correct list; slight mismatch to “CHECK constraint” detail is not required because expected also centers lifecycle values.
- **Retrieval:** gt_coverage=1.0, top_score=0.7000, gate=proceed

### Q007: Which table stores the product SKU information?
- **Type:** direct_mapping | **Difficulty:** easy
- **Verdict:** CORRECT
- **Expected:** `TB_PRODUCT` stores SKU in `SKU` column
- **Generated:** “TB_PRODUCT.SKU” directly
- **Analysis:** Correct.
- **Retrieval:** gt_coverage=1.0, top_score=0.9868, gate=proceed

### Q008: How can I find all orders placed by a specific customer?
- **Type:** multi_hop | **Difficulty:** medium
- **Verdict:** CORRECT
- **Expected:** Filter `SALES_ORDER_HDR` by CUST_ID; join CUSTOMER_MASTER on CUST_ID to get details
- **Generated:** Correct query strategy and join key
- **Analysis:** Correct join and filter semantics.
- **Retrieval:** gt_coverage=1.0, top_score=0.7000, gate=proceed

### Q009: How does the schema link orders to their individual product line items?
- **Type:** multi_hop | **Difficulty:** medium
- **Verdict:** CORRECT
- **Expected:** `ORDER_LINE_ITEM` joins `SALES_ORDER_HDR` and `TB_PRODUCT` via ORDER_ID and PRODUCT_ID; includes QUANTITY/UNIT_PRICE/LINE_AMT
- **Generated:** Correct junction table explanation and join path
- **Analysis:** Correct.
- **Retrieval:** gt_coverage=1.0, top_score=0.7000, gate=proceed

### Q010: Show me the order hierarchy from customer to line items.
- **Type:** multi_hop | **Difficulty:** medium
- **Verdict:** CORRECT
- **Expected:** CUSTOMER_MASTER → SALES_ORDER_HDR → ORDER_LINE_ITEM → TB_PRODUCT
- **Generated:** Correct hierarchy with FK direction.
- **Analysis:** Correct relationship chain.
- **Retrieval:** gt_coverage=1.0, top_score=0.7000, gate=proceed

### Q011: How does the schema model the confirmation state of a payment and its relationship to the order?
- **Type:** multi_hop | **Difficulty:** medium
- **Verdict:** CORRECT
- **Expected:** PAYMENT.CONFIRMED_AT and PAYMENT.STATUS_CODE; order has SALES_ORDER_HDR.PAYMENT_CONFIRMED_AT mirroring; order lifecycle via STATUS_CODE
- **Generated:** Correctly covers both confirmation fields and FK relationship to order
- **Analysis:** Fully aligned with expected.
- **Retrieval:** gt_coverage=1.0, top_score=0.7000, gate=proceed

### Q012: How are shipments related to orders and warehouses?
- **Type:** multi_hop | **Difficulty:** medium
- **Verdict:** CORRECT
- **Expected:** SHIPMENT.ORDER_ID → SALES_ORDER_HDR.ORDER_ID; SHIPMENT includes source warehouse code + tracking + delivery status
- **Generated:** Correct FK to orders and correct use of WAREHOUSE_CODE; acknowledges no separate warehouse table in retrieved context
- **Analysis:** Correct within dataset representation.
- **Retrieval:** gt_coverage=1.0, top_score=0.7672, gate=proceed

### Q013: Can a product belong to multiple categories?
- **Type:** negative | **Difficulty:** easy
- **Verdict:** CORRECT
- **Expected:** No—product has exactly one category via TB_PRODUCT.CATEGORY_ID → TB_CATEGORY
- **Generated:** “No” and explains single FK/category reference
- **Analysis:** Correct handling of negative question.
- **Retrieval:** gt_coverage=1.0, top_score=0.7000, gate=proceed

### Q014: Is it possible for a customer to place an order without payment?
- **Type:** negative | **Difficulty:** medium
- **Verdict:** CORRECT
- **Expected:** Yes, orders can exist without payment confirmation (PAYMENT_CONFIRMED_AT nullable); shipping constrained by business rule
- **Generated:** “Yes,” using nullable `SALES_ORDER_HDR.PAYMENT_CONFIRMED_AT` and shipping constraint logic
- **Analysis:** Matches expected answer rationale; no fabrication.
- **Retrieval:** gt_coverage=1.0, top_score=0.7000, gate=proceed

### Q015: What schema fields support monetary value tracking across orders and their line items?
- **Type:** multi_hop | **Difficulty:** easy
- **Verdict:** CORRECT
- **Expected:** SALES_ORDER_HDR.TOTAL_AMT; ORDER_LINE_ITEM UNIT_PRICE and LINE_AMT; join via ORDER_ID
- **Generated:** Correctly names header and line fields plus FK linkage
- **Analysis:** Correct schema-level money tracking.
- **Retrieval:** gt_coverage=1.0, top_score=0.7000, gate=proceed

## Anomalies & Recommendations

### Red Flags
- None in terms of correctness/grounding: `grader_rejection_count=0`, `grounded_rate=1.0`, perfect retrieval coverage.
- Minor observation: many questions report `retrieval_quality_score=0.7` exactly, suggesting a floor/plateau effect from the pipeline’s confidence adjustment logic (not necessarily a problem, but worth checking if this is masking variance).

### Recommendations
- Validate retrieval score calibration: inspect how `retrieval_quality_score` is computed from `retrieval_quality_score_raw` vs the “0.7 pool confidence floor” mentioned in the system prompt; ensure it doesn’t compress too much signal in basics runs.
- For later (harder/edgecase) datasets: add targeted checks for multi-hop negatives, since Q013/Q014 succeeded here—future runs should confirm the same stability.

## Comparison Notes (if applicable)
- No AB-00 baseline comparison data was provided in the JSON (no `ablation_context`), so a causal “impact vs baseline” comparison cannot be performed.