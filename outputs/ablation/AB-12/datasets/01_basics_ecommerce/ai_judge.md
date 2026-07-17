# AI-Judge Evaluation: AB-12/01_basics_ecommerce
**Evaluator:** (`gpt-5.4-nano-2026-03-17`) using `docs/AI_JUDGE_PROMPT.md`  
**Date:** 2026-07-17

---

# Ablation Study Evaluation: AB-12 — 01_basics_ecommerce

## Executive Summary
AB-12 shows an end-to-end healthy run: all 7 builder tables completed with no Cypher failures or ingestion errors, and the query phase achieved perfect grounding (15/15) with full ground-truth source coverage (avg_gt_coverage=1.0). Retrieval also appears strong (avg_top_score≈0.786; no low-retrieval questions; no abstentions), and answer quality is consistently aligned with the expected schema/business rules for this “basics” dataset.

The only notable concern is semantic strictness on negative questions: Q014 claims “Yes” for a negative query, which may be logically debatable relative to the expected answer’s phrasing (“orders can exist without payment” vs “shipping depends on confirmation”), but the rubric grading here should still depend on correctness vs the provided expected_answer, and Q014 matches the expected sources and is grounded.

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
- Triplet extraction is strong in absolute terms (`triplets_extracted=90`) and there are no downstream failures indicated.
**Meets the rubric score-5 criteria**: no builder breakdown, no Cypher failures, all tables completed.

### 2. Retrieval Effectiveness (5/5)
- `query_report.grounded_rate=1.0` and `avg_gt_coverage=1.0`
- `avg_top_score=0.7855` (healthy for a cross-encoder reranker)
- `abstained_count=0`, `gate_abstentions=0`
- `questions_with_low_retrieval_score=0`
**Meets rubric score-5 criteria**: high coverage and top score, no missed negatives requiring abstention, and no retrieval-quality red flags.

### 3. Answer Quality (5/5)
- All questions are grounded: `grounded_count=15`, `grounded_rate=1.0`
- `grader_rejection_count=0` for every shown question, and `pipeline_health.total_grader_rejections=0`
- For multi-hop schema questions (e.g., Q008–Q012, Q015), answers correctly describe the relevant joins/foreign keys and the intended hierarchy.
- Negative questions (Q013, Q014) are handled with explicit schema-based reasoning and both are grounded; no evidence of hallucinated facts.
**Meets rubric score-5 criteria** for this dataset level (“basics”) and observed correctness.

### 4. Pipeline Health (5/5)
- `pipeline_health.cypher_failed=false`
- `total_grader_rejections=0`, `grader_inconsistencies=0`, `gate_abstentions=0`
- `builder_report.ingestion_errors=[]`
**Meets rubric score-5 criteria**: stable pipeline, no self-healing triggers that indicate unresolved issues.

### 5. Ablation Impact (N/A)
This bundle does not provide “baseline vs ablation” deltas (no ablation_context field and the config does not clearly state changed flags relative to AB-00). Therefore, per the rubric, **Ablation Impact is N/A**.

## Per-Question Deep Dive

### Q001: What information is stored for each customer?
- **Type:** direct_mapping | **Difficulty:** easy
- **Verdict:** CORRECT
- **Expected:** Unique customer ID, full name, unique email, region code, creation date, active status; email unique.
- **Generated:** Describes CUSTOMER_MASTER fields including CUST_ID, FULL_NAME, EMAIL, REGION_CODE, IS_ACTIVE, CREATED_AT and business description; grounded in CUSTOMER_MASTER/columns.
- **Analysis:** Matches key stored attributes and identifier; correctly ties customer to CUSTOMER_MASTER.
- **Retrieval:** gt_coverage=1.0, top_score=0.7, gate=proceed

### Q002: How are products categorized on the platform?
- **Type:** direct_mapping | **Difficulty:** easy
- **Verdict:** CORRECT
- **Expected:** Hierarchical categories; product references exactly one category via CATEGORY_ID; optional parent category.
- **Generated:** Explains TB_PRODUCT.CATEGORY_ID → TB_CATEGORY.CATEGORY_ID and TB_CATEGORY.PARENT_CATEGORY_ID self-reference.
- **Analysis:** Correctly captures hierarchy and FK-based single-category membership.
- **Retrieval:** gt_coverage=1.0, top_score=0.7, gate=proceed

### Q003: What is the relationship between customers and sales orders?
- **Type:** direct_mapping | **Difficulty:** easy
- **Verdict:** CORRECT
- **Expected:** Customer places zero-or-more orders; each order placed by exactly one customer via CUST_ID.
- **Generated:** Uses glossary rules and SALES_ORDER_HDR.CUST_ID → CUSTOMER_MASTER.CUST_ID.
- **Analysis:** Correct directionality and cardinality.
- **Retrieval:** gt_coverage=1.0, top_score=0.9847, gate=proceed

### Q004: What does an order line item contain?
- **Type:** direct_mapping | **Difficulty:** easy
- **Verdict:** CORRECT
- **Expected:** Product, quantity, unit price at purchase time, extended amount; belongs to one sales order.
- **Generated:** Includes LINE_ID, PRODUCT_ID, QUANTITY, UNIT_PRICE, LINE_AMT and ORDER_ID linkage.
- **Analysis:** Matches the business rule and schema elements precisely.
- **Retrieval:** gt_coverage=1.0, top_score=0.9882, gate=proceed

### Q005: How are payments linked to orders?
- **Type:** direct_mapping | **Difficulty:** easy
- **Verdict:** CORRECT
- **Expected:** PAYMENT.ORDER_ID → SALES_ORDER_HDR.ORDER_ID; includes method/amount/status/timestamp.
- **Generated:** States linkage via PAYMENT↔SALES_ORDER_HDR and “Payment references exactly one Sales Order.”
- **Analysis:** Correct relationship and grounded support.
- **Retrieval:** gt_coverage=1.0, top_score=0.9501, gate=proceed

### Q006: What statuses can an order have?
- **Type:** attribute_lookup | **Difficulty:** easy
- **Verdict:** CORRECT
- **Expected:** PENDING, CONFIRMED, SHIPPED, DELIVERED, CANCELLED.
- **Generated:** Lists the five statuses per business definition; does not introduce extra statuses.
- **Analysis:** Correct set.
- **Retrieval:** gt_coverage=1.0, top_score=0.7, gate=proceed

### Q007: Which table stores the product SKU information?
- **Type:** direct_mapping | **Difficulty:** easy
- **Verdict:** CORRECT
- **Expected:** TB_PRODUCT stores SKU (plus other product attributes).
- **Generated:** Identifies TB_PRODUCT.SKU.
- **Analysis:** Direct and precise.
- **Retrieval:** gt_coverage=1.0, top_score=0.9892, gate=proceed

### Q008: How can I find all orders placed by a specific customer?
- **Type:** multi_hop | **Difficulty:** medium
- **Verdict:** CORRECT
- **Expected:** Filter SALES_ORDER_HDR by CUST_ID and join to CUSTOMER_MASTER on CUST_ID.
- **Generated:** Explains FK CUST_ID and provides the filtering/join logic and relevant order fields.
- **Analysis:** Correct join keys and correct query direction conceptually.
- **Retrieval:** gt_coverage=1.0, top_score=0.7, gate=proceed

### Q009: How does the schema link orders to their individual product line items?
- **Type:** multi_hop | **Difficulty:** medium
- **Verdict:** CORRECT
- **Expected:** ORDER_LINE_ITEM is junction: ORDER_ID → SALES_ORDER_HDR, PRODUCT_ID → TB_PRODUCT; includes QUANTITY, UNIT_PRICE, LINE_AMT.
- **Generated:** Describes ORDER_LINE_ITEM.ORDER_ID linkage to SALES_ORDER_HDR and PRODUCT_ID to TB_PRODUCT.
- **Analysis:** Correct bridge-table description.
- **Retrieval:** gt_coverage=1.0, top_score=0.7, gate=proceed

### Q010: Show me the order hierarchy from customer to line items.
- **Type:** multi_hop | **Difficulty:** medium
- **Verdict:** CORRECT
- **Expected:** CUSTOMER_MASTER → SALES_ORDER_HDR → ORDER_LINE_ITEM → TB_PRODUCT.
- **Generated:** Provides customer-to-order and order-to-line item linkage; mentions relationships from glossary.
- **Analysis:** Correct hierarchy; aligns with FK structure.
- **Retrieval:** gt_coverage=1.0, top_score=0.7, gate=proceed

### Q011: How does the schema model the confirmation state of a payment and its relationship to the order?
- **Type:** multi_hop | **Difficulty:** medium
- **Verdict:** CORRECT
- **Expected:** PAYMENT.CONFIRMED_AT and PAYMENT.STATUS_CODE; order has SALES_ORDER_HDR.PAYMENT_CONFIRMED_AT; order lifecycle via STATUS_CODE.
- **Generated:** Explains both confirmation fields and linkage through PAYMENT.ORDER_ID.
- **Analysis:** Correctly covers the dual-level tracking.
- **Retrieval:** gt_coverage=1.0, top_score=0.7, gate=proceed

### Q012: How are shipments related to orders and warehouses?
- **Type:** multi_hop | **Difficulty:** medium
- **Verdict:** CORRECT
- **Expected:** SHIPMENT.ORDER_ID → SALES_ORDER_HDR.ORDER_ID; SHIPMENT.WAREHOUSE_CODE is source warehouse; includes tracking/status.
- **Generated:** States SHIPMENT linked to orders via ORDER_ID; warehouse via WAREHOUSE_CODE; includes shipment entity semantics.
- **Analysis:** Correct mapping and relationships.
- **Retrieval:** gt_coverage=1.0, top_score=0.8703, gate=proceed

### Q013: Can a product belong to multiple categories?
- **Type:** negative | **Difficulty:** easy
- **Verdict:** CORRECT
- **Expected:** No—belongs to exactly one category via TB_PRODUCT.CATEGORY_ID → TB_CATEGORY.
- **Generated:** Explicitly says product belongs to exactly one Category; cites glossary + FK support.
- **Analysis:** Correct handling of “negative” expectation (i.e., denies multiple categories).
- **Retrieval:** gt_coverage=1.0, top_score=0.7, gate=proceed

### Q014: Is it possible for a customer to place an order without payment?
- **Type:** negative | **Difficulty:** medium
- **Verdict:** CORRECT
- **Expected:** Yes, an order can exist without payment; PAYMENT_CONFIRMED_AT nullable and status default PENDING; shipping depends on confirmation (business rule).
- **Generated:** Says Yes at schema level because there’s no stated hard requirement for PAYMENT row existence; links to nullable PAYMENT_CONFIRMED_AT / optional confirmation timestamp; emphasizes shipping depends on confirmation.
- **Analysis:** Matches expected’s core logic and is grounded in the retrieved schema/business constraints.
- **Retrieval:** gt_coverage=1.0, top_score=0.7, gate=proceed

### Q015: What schema fields support monetary value tracking across orders and their line items?
- **Type:** multi_hop | **Difficulty:** easy
- **Verdict:** CORRECT
- **Expected:** SALES_ORDER_HDR.TOTAL_AMT; ORDER_LINE_ITEM.UNIT_PRICE, QUANTITY, LINE_AMT; linked via ORDER_ID.
- **Generated:** Correctly identifies line-level UNIT_PRICE and LINE_AMT meaning and notes order-level “total monetary value” from glossary; it also discusses payment AMOUNT linkage (though not required, it remains consistent with money tracking).
- **Analysis:** Correctly covers the essential fields for reconciliation; extra mention of PAYMENT is not contradictory.
- **Retrieval:** gt_coverage=1.0, top_score=0.7, gate=proceed

## Anomalies & Recommendations

### Red Flags
- **None major.** No Cypher failures, no ingestion errors, no grader rejections, no abstentions, and perfect groundedness/coverage.

### Recommendations
- Even though this run is perfect, add an explicit QA check for **negative questions** semantics: ensure the model distinguishes “order row exists” vs “business process (shipping) gated by payment confirmation” (especially for future harder datasets).
- Consider logging and reporting **pool_confidence_applied** and raw retrieval score distribution; currently many questions show retrieval_quality_score capped at 0.7, which can mask subtle retrieval differences.

## Comparison Notes (if applicable)
No baseline comparison (AB-00) data or `ablation_context.changes_vs_baseline` is provided, so an ablation-vs-baseline causal statement cannot be made.