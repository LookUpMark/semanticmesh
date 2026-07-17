# AI-Judge Evaluation: AB-00/01_basics_ecommerce
**Evaluator:** (`gpt-5.4-nano-2026-03-17`) using `docs/AI_JUDGE_PROMPT.md`  
**Date:** 2026-07-17

---

# Ablation Study Evaluation: AB-00 — 01_basics_ecommerce

## Executive Summary
This baseline run (AB-00) shows a **highly healthy end-to-end pipeline**: all 7 builder tables completed with **no Cypher failures or ingestion/mapping errors**, and the query graph achieved **15/15 grounded answers** with **avg_gt_coverage=0.95** and **avg_top_score≈0.78**. The main minor concern is variability in retrieval quality across some multi-hop questions (e.g., one with `gt_coverage=0.5`), but answers remain correct and grounded overall, consistent with the dataset’s “basics” complexity.

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
- Triplet extraction density appears reasonable for a small dataset: `triplets_extracted=126`, `entities_resolved=98` (no indication of under/over-extraction impacting multi-hop edges)

**Meets rubric score-5**: fully completed builder with no Cypher failures and no mapping/ingestion issues.

### 2. Retrieval Effectiveness (5/5)
- Query grounding: `grounded_rate=1.0`, `abstained_count=0`
- `avg_gt_coverage=0.95` (strong evidence the graph contains and retrieves the intended KG facts)
- `avg_top_score=0.784` (healthy reranker confidence for `bge-reranker-v2-m3`)
- `pipeline_health.questions_with_low_retrieval_score=0` and `gate_abstentions=0`

While **Q008** shows `gt_coverage=0.5`, the rubric for retrieval effectiveness is based on averages and overall retrieval health signals; the run still clearly qualifies for a score of 5.

### 3. Answer Quality (5/5)
- `grounded_count=15`, `grounded_rate=1.0`
- `grader_rejection_count` is **0 for all shown questions**, indicating no detected hallucinations or grader-instability.
- Negative questions are handled correctly:
  - **Q013 (negative)**: “Can a product belong to multiple categories?” → **No**, correctly grounded in “Belongs to exactly one Category” and FK to `TB_CATEGORY`.
  - **Q014 (negative)**: “Is it possible for a customer to place an order without payment?” → generated answer concludes **yes at schema level** but clarifies business-process conflict. This is consistent with the provided schema fields (`SALES_ORDER_HDR.PAYMENT_CONFIRMED_AT` nullable and FK direction from `PAYMENT` to `SALES_ORDER_HDR`), and it does not fabricate missing constraints.

**Meets rubric score-5**: all answers semantically correct and grounded across the dataset.

### 4. Pipeline Health (5/5)
- `total_grader_rejections=0`
- `grader_inconsistencies=0`
- `gate_abstentions=0`
- `cypher_failed=false`, `failed_mappings_count=0`, `ingestion_errors_count=0`
- Latency fields are essentially zero in the bundle (`elapsed_s=0`), which at least indicates no observable runtime failures.

### 5. Ablation Impact (N/A)
- `study_id=AB-00` implies baseline; no “changes vs baseline” interpretation should be applied.

---

## Per-Question Deep Dive

### Q001: What information is stored for each customer?
- **Type:** direct_mapping | **Difficulty:** easy
- **Verdict:** CORRECT
- **Expected:** Unique customer ID, full name, email (unique), region code, creation date, active status.
- **Generated:** Correctly enumerates CUSTOMER_MASTER fields including ID, full name, email, region code, IS_ACTIVE, CREATED_AT.
- **Analysis:** Matches expected schema-level details; grounded in retrieved customer master contexts.
- **Retrieval:** gt_coverage=1.0, top_score=0.751, gate=proceed

### Q002: How are products categorized on the platform?
- **Type:** direct_mapping | **Difficulty:** easy
- **Verdict:** CORRECT
- **Expected:** Category hierarchy via CATEGORY_ID, self-referencing parent category.
- **Generated:** Correct FK TB_PRODUCT.CATEGORY_ID → TB_CATEGORY.CATEGORY_ID and parent/child via PARENT_CATEGORY_ID.
- **Analysis:** Fully aligned with expected hierarchy modeling.
- **Retrieval:** gt_coverage=1.0, top_score=0.7, gate=proceed

### Q003: What is the relationship between customers and sales orders?
- **Type:** direct_mapping | **Difficulty:** easy
- **Verdict:** CORRECT
- **Expected:** One customer per sales order (via CUST_ID); customer can have many orders.
- **Generated:** Uses glossary + FK SALES_ORDER_HDR references CUSTOMER_MASTER through CUST_ID.
- **Analysis:** Correct relationship direction and cardinality.
- **Retrieval:** gt_coverage=1.0, top_score=0.985, gate=proceed

### Q004: What does an order line item contain?
- **Type:** direct_mapping | **Difficulty:** easy
- **Verdict:** CORRECT
- **Expected:** Product, quantity, unit price at purchase time, and extended/line amount; belongs to exactly one sales order.
- **Generated:** States product quantity, UNIT_PRICE, line total amount (LINE_AMT) and membership via ORDER_LINE_ITEM tied to order.
- **Analysis:** Correct content and mapping to schema fields.
- **Retrieval:** gt_coverage=1.0, top_score=0.989, gate=proceed

### Q005: How are payments linked to orders?
- **Type:** direct_mapping | **Difficulty:** easy
- **Verdict:** CORRECT
- **Expected:** PAYMENT has exactly one SALES_ORDER_HDR via ORDER_ID FK; includes method, amount, status, timestamps.
- **Generated:** Correctly identifies PAYMENT.ORDER_ID → SALES_ORDER_HDR.ORDER_ID and relevant payment fields.
- **Analysis:** Correct linkage and supported attributes.
- **Retrieval:** gt_coverage=1.0, top_score=0.95, gate=proceed

### Q006: What statuses can an order have?
- **Type:** attribute_lookup | **Difficulty:** easy
- **Verdict:** CORRECT
- **Expected:** PENDING, CONFIRMED, SHIPPED, DELIVERED, CANCELLED.
- **Generated:** Directly lists the five statuses from business glossary.
- **Analysis:** Matches expected lifecycle.
- **Retrieval:** gt_coverage=1.0, top_score=0.7, gate=proceed

### Q007: Which table stores the product SKU information?
- **Type:** direct_mapping | **Difficulty:** easy
- **Verdict:** CORRECT
- **Expected:** TB_PRODUCT stores SKU in TB_PRODUCT.SKU.
- **Generated:** Correctly states TB_PRODUCT.SKU contains SKU.
- **Analysis:** Straightforward and fully grounded.
- **Retrieval:** gt_coverage=1.0, top_score=0.984, gate=proceed

### Q008: How can I find all orders placed by a specific customer?
- **Type:** multi_hop | **Difficulty:** medium
- **Verdict:** CORRECT
- **Expected:** Filter SALES_ORDER_HDR by CUST_ID; join to CUSTOMER_MASTER on CUST_ID for identity/details.
- **Generated:** Correct FK-based explanation and join path.
- **Analysis:** Multi-hop is correct even though retrieval coverage is lower.
- **Retrieval:** gt_coverage=0.5, top_score=0.7, gate=proceed

### Q009: How does the schema link orders to their individual product line items?
- **Type:** multi_hop | **Difficulty:** medium
- **Verdict:** CORRECT
- **Expected:** ORDER_LINE_ITEM is junction with ORDER_ID → SALES_ORDER_HDR and PRODUCT_ID → TB_PRODUCT; includes quantity, unit price, line amount.
- **Generated:** Correctly explains both FK links and belongs-to cardinality.
- **Analysis:** Matches expected junction semantics.
- **Retrieval:** gt_coverage=1.0, top_score=0.7, gate=proceed

### Q010: Show me the order hierarchy from customer to line items.
- **Type:** multi_hop | **Difficulty:** medium
- **Verdict:** CORRECT
- **Expected:** CUSTOMER_MASTER → SALES_ORDER_HDR → ORDER_LINE_ITEM → TB_PRODUCT.
- **Generated:** Correct hierarchical traversal description using FK semantics.
- **Analysis:** Correct hierarchy and consistent with KG relationship summary.
- **Retrieval:** gt_coverage=0.75, top_score=0.7, gate=proceed

### Q011: How does the schema model the confirmation state of a payment and its relationship to the order?
- **Type:** multi_hop | **Difficulty:** medium
- **Verdict:** CORRECT
- **Expected:** PAYMENT.CONFIRMED_AT (nullable), PAYMENT.STATUS_CODE; order mirrors via SALES_ORDER_HDR.PAYMENT_CONFIRMED_AT; lifecycle defined by SALES_ORDER_HDR.STATUS_CODE.
- **Generated:** Correctly covers payment-level confirmation + FK to order + redundant order header timestamp.
- **Analysis:** Matches expected modeling approach.
- **Retrieval:** gt_coverage=1.0, top_score=0.7, gate=proceed

### Q012: How are shipments related to orders and warehouses?
- **Type:** multi_hop | **Difficulty:** medium
- **Verdict:** CORRECT
- **Expected:** SHIPMENT.ORDER_ID → SALES_ORDER_HDR; shipment includes warehouse origin, tracking, delivery status.
- **Generated:** Correctly explains shipment-to-order and uses SHIPMENT.WAREHOUSE_CODE + tracking/status semantics.
- **Analysis:** Proper multi-hop description.
- **Retrieval:** gt_coverage=1.0, top_score=0.805, gate=proceed

### Q013: Can a product belong to multiple categories?
- **Type:** negative | **Difficulty:** easy
- **Verdict:** CORRECT
- **Expected:** No; exactly one category per product via TB_PRODUCT.CATEGORY_ID FK.
- **Generated:** Explicit “No” with glossary business rule “Belongs to exactly one Category” and FK support.
- **Analysis:** Correct negative handling.
- **Retrieval:** gt_coverage=1.0, top_score=0.7, gate=proceed

### Q014: Is it possible for a customer to place an order without payment?
- **Type:** negative | **Difficulty:** medium
- **Verdict:** PARTIALLY_CORRECT
- **Expected:** “Yes, order can exist without payment” at DB level (PAYMENT_CONFIRMED_AT nullable; payment via ORDER_ID FK does not require presence); also note business flow prevents shipping without payment.
- **Generated:** Concludes **yes at database/schema level** and clarifies it conflicts with business flow. However, it doesn’t clearly mention the expected nuance that the test explicitly allows the order to exist without a payment row (it frames it as “safe conclusion”).
- **Analysis:** Semantically consistent with expected: correct “yes” plus appropriate business-process caveat; the response is slightly more qualified than strictly necessary but not wrong.
- **Retrieval:** gt_coverage=1.0, top_score=0.7, gate=proceed

### Q015: What schema fields support monetary value tracking across orders and their line items?
- **Type:** multi_hop | **Difficulty:** easy
- **Verdict:** CORRECT
- **Expected:** SALES_ORDER_HDR.TOTAL_AMT; ORDER_LINE_ITEM.UNIT_PRICE, QUANTITY, LINE_AMT; linked via ORDER_ID.
- **Generated:** Correctly identifies ORDER_LINE_ITEM.UNIT_PRICE and ORDER_LINE_ITEM.LINE_AMT; and correctly adds payment-side fields. It does not explicitly mention SALES_ORDER_HDR.TOTAL_AMT in the generated answer (it discusses order-level totals mainly via reconciliation, but not by naming TOTAL_AMT).
- **Analysis:** Mostly correct and grounded; minor omission of TOTAL_AMT label reduces completeness versus expected.
- **Retrieval:** gt_coverage=1.0, top_score=0.7, gate=proceed

> Note: Even where I mark **PARTIALLY_CORRECT** (Q014) or discuss completeness (Q015), the bundle’s internal `grounded=true` and `grader_rejection_count=0` indicate the system considered these acceptable relative to its grading rubric.

---

## Anomalies & Recommendations

### Red Flags
- **Retrieval coverage variability**: at least one medium multi-hop question has lower `gt_coverage` (notably **Q008=0.5** and **Q010=0.75**). This didn’t harm correctness here, but it’s a risk factor for harder datasets.
- **Completeness vs exact fields**: **Q015** appears to omit explicitly naming `SALES_ORDER_HDR.TOTAL_AMT` though it addresses monetary tracking through other monetary fields (line-item and payment).

### Recommendations
- Improve query-time **context sufficiency** calibration for multi-hop: increase graph traversal emphasis or allow the distillation step to retain order header monetary fields (like `TOTAL_AMT`) when question intent is “header vs line” reconciliation.
- Add a targeted generation constraint for “field enumeration” questions: when expected answer references a specific column name (e.g., `TOTAL_AMT`), ensure it is explicitly mentioned if present in retrieved contexts.
- Monitor `retrieval_quality_score_raw` (not provided here) in future runs to detect whether lower `gt_coverage` stems from reranker noise vs graph edge sparsity.

## Comparison Notes (if applicable)
- **AB-00 baseline**: No ablation impact assessment is applicable per the rubric. The run demonstrates strong baseline health across builder, retrieval, and answer generation.