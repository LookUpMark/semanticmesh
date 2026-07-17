# AI-Judge Evaluation: AB-11/01_basics_ecommerce
**Evaluator:** (`gpt-5.4-nano-2026-03-17`) using `docs/AI_JUDGE_PROMPT.md`  
**Date:** 2026-07-17

---

# Ablation Study Evaluation: AB-11 — 01_basics_ecommerce

## Executive Summary
AB-11 shows a fully functioning GraphRAG run on the e-commerce “basics” dataset: builder mapping completed for all tables with no Cypher failures or ingestion errors, and query answering achieved a 100% grounded rate across all 15 questions. Retrieval quality is consistently strong (avg `avg_top_score` ≈ 0.789, avg `avg_gt_coverage` ≈ 0.983), and there are zero grader rejections/inconsistencies and zero abstentions, indicating stable internal loops and reliable gating.

The only noteworthy weakness is minor: one multi-hop question (Q010) shows reduced `gt_coverage` (0.75), but the generated answer remains grounded and correct given the provided evidence.

## Scores

| Dimension | Score (1-5) | Weight | Weighted |
|---|---:|---:|---:|
| Builder Quality | 5 | 25% | 1.25 |
| Retrieval Effectiveness | 5 | 25% | 1.25 |
| Answer Quality | 5 | 30% | 1.50 |
| Pipeline Health | 5 | 10% | 0.50 |
| Ablation Impact | N/A | 10% | N/A |
| **Overall** |  |  | **4.50** |

## Dimension Analysis

### 1. Builder Quality (5/5)
- `tables_parsed=7`, `tables_completed=7`, `all_tables_completed=true`
- `cypher_failed=false`
- `failed_mappings=[]`
- `ingestion_errors=[]`
- Triplet extraction density is strong: `triplets_extracted=97` across a small number of docs/tables (no indication of weak extraction).
- No evidence of parent/child chunking issues (`parent_chunks=0`, `child_chunks=0`), and builder latency is effectively zero in the bundle (`elapsed_s=0`, likely artifact of instrumentation, but no failures).

**Judgment:** Meets rubric’s top-tier criteria (no builder failures).

### 2. Retrieval Effectiveness (5/5)
- `grounded_rate=1.0` (all answers have verifiable grounding)
- `avg_gt_coverage=0.9833` (near-complete retrieval of expected sources)
- `avg_top_score=0.7888` (healthy reranker confidence; well above the rubric thresholds)
- `pipeline_health.questions_with_low_retrieval_score=0`
- `gate_abstentions=0` (no incorrect abstention in this run)

**Conclusion:** Retrieval is effective and the quality gate behaves correctly for this dataset/difficulty mix.

### 3. Answer Quality (5/5)
Across the 15 provided per-question examples:
- Every `per_question.grounded=true`
- `grader_rejection_count=0` for all shown questions
- Negative questions are handled correctly:
  - Q013 (negative): correctly answers “No… belongs to exactly one category.”
  - Q014 (negative): correctly answers “Yes… orders can exist without confirmed payment,” while noting shipping requires confirmation.
- Multi-hop questions produce correct hierarchical/join logic (customer→order→line→product; order→line items; payments confirmation state; shipments→orders→warehouses).

**Judgment:** Matches rubric’s score-5 bar (verifiably grounded and semantically correct vs expected).

### 4. Pipeline Health (5/5)
- `pipeline_health.total_grader_rejections=0`
- `grader_inconsistencies=0`
- `gate_abstentions=0`
- `cypher_failed=false`
- `failed_mappings_count=0`
- `ingestion_errors_count=0`

Self-reflection loops appear stable (no retry storms visible, no max-retry exhaustion implied).

### 5. Ablation Impact (N/A)
This bundle is **AB-11**, but the input does not include an `ablation_context` or any “baseline vs changed flags” summary. Therefore, I cannot reliably attribute changes to a specific ablation hypothesis per rubric.

## Per-Question Deep Dive

### Q001: What information is stored for each customer?
- **Type:** direct_mapping | **Difficulty:** easy
- **Verdict:** CORRECT
- **Expected:** unique customer ID, full name, email (unique), region code, creation date, active status
- **Generated:** lists CUST_ID, FULL_NAME, EMAIL, REGION_CODE, IS_ACTIVE, CREATED_AT; explains CUSTOMER_MASTER as the source
- **Analysis:** Semantically matches expected; correct emphasis on fields.
- **Retrieval:** gt_coverage=1.0, top_score=0.7, gate=proceed

### Q002: How are products categorized on the platform?
- **Type:** direct_mapping | **Difficulty:** easy
- **Verdict:** CORRECT
- **Expected:** hierarchical categories (parent category); product has exactly one CATEGORY_ID
- **Generated:** PRODUCT→TB_PRODUCT.CATEGORY_ID→TB_CATEGORY.CATEGORY_ID; mentions PARENT_CATEGORY_ID
- **Analysis:** Correct structure and relationship.
- **Retrieval:** gt_coverage=1.0, top_score=0.7, gate=proceed

### Q003: What is the relationship between customers and sales orders?
- **Type:** direct_mapping | **Difficulty:** easy
- **Verdict:** CORRECT
- **Expected:** orders placed by exactly one customer; customer can have zero or more orders
- **Generated:** mirrors glossary rule + FK via SALES_ORDER_HDR.CUST_ID → CUSTOMER_MASTER.CUST_ID
- **Analysis:** Correct cardinality and join key.
- **Retrieval:** gt_coverage=1.0, top_score=0.9847, gate=proceed

### Q004: What does an order line item contain?
- **Type:** direct_mapping | **Difficulty:** easy
- **Verdict:** CORRECT
- **Expected:** product, quantity, unit price at purchase, extended/line amount; belongs to one sales order
- **Generated:** LINE_ID, ORDER_ID, PRODUCT_ID, QUANTITY, UNIT_PRICE, LINE_AMT; notes nullability
- **Analysis:** Matches expected content; no hallucinations.
- **Retrieval:** gt_coverage=1.0, top_score=0.9802, gate=proceed

### Q005: How are payments linked to orders?
- **Type:** direct_mapping | **Difficulty:** easy
- **Verdict:** CORRECT
- **Expected:** payment associated to one order via ORDER_ID; payment tracks method/amount/status/confirmation
- **Generated:** PAYMENT.ORDER_ID → SALES_ORDER_HDR.ORDER_ID
- **Analysis:** Correct FK linkage; mentions relevant attributes.
- **Retrieval:** gt_coverage=1.0, top_score=0.9501, gate=proceed

### Q006: What statuses can an order have?
- **Type:** attribute_lookup | **Difficulty:** easy
- **Verdict:** CORRECT
- **Expected:** PENDING, CONFIRMED, SHIPPED, DELIVERED, CANCELLED
- **Generated:** lists those statuses and points to SALES_ORDER_HDR.STATUS_CODE
- **Analysis:** Correct enumeration.
- **Retrieval:** gt_coverage=1.0, top_score=0.7, gate=proceed

### Q007: Which table stores the product SKU information?
- **Type:** direct_mapping | **Difficulty:** easy
- **Verdict:** CORRECT
- **Expected:** TB_PRODUCT stores SKU in TB_PRODUCT.SKU
- **Generated:** explicitly states TB_PRODUCT.SKU (and context about catalog fields)
- **Analysis:** Correct table/column.
- **Retrieval:** gt_coverage=1.0, top_score=0.9849, gate=proceed

### Q008: How can I find all orders placed by a specific customer?
- **Type:** multi_hop | **Difficulty:** medium
- **Verdict:** CORRECT
- **Expected:** filter SALES_ORDER_HDR by CUST_ID; join to CUSTOMER_MASTER for customer details
- **Generated:** explains WHERE SALES_ORDER_HDR.CUST_ID = CUSTOMER_MASTER.CUST_ID and optional join
- **Analysis:** Correct query logic at schema level.
- **Retrieval:** gt_coverage=1.0, top_score=0.7, gate=proceed

### Q009: How does the schema link orders to their individual product line items?
- **Type:** multi_hop | **Difficulty:** medium
- **Verdict:** CORRECT
- **Expected:** ORDER_LINE_ITEM as junction; ORDER_ID FK to SALES_ORDER_HDR and PRODUCT_ID FK to TB_PRODUCT; line stores quantity, unit price, line amount
- **Generated:** describes ORDER_LINE_ITEM.ORDER_ID and ORDER_LINE_ITEM.PRODUCT_ID relationships
- **Analysis:** Correct join/junction semantics.
- **Retrieval:** gt_coverage=1.0, top_score=0.7, gate=proceed

### Q010: Show me the order hierarchy from customer to line items.
- **Type:** multi_hop | **Difficulty:** medium
- **Verdict:** CORRECT
- **Expected:** CUSTOMER_MASTER → SALES_ORDER_HDR → ORDER_LINE_ITEM → TB_PRODUCT
- **Generated:** gives the same hierarchy and clarifies key FK steps; mentions line amount relationship
- **Analysis:** Correct hierarchy; minor retrieval shortfall doesn’t impact correctness.
- **Retrieval:** gt_coverage=0.75, top_score=0.7, gate=proceed

### Q011: How does the schema model the confirmation state of a payment and its relationship to the order?
- **Type:** multi_hop | **Difficulty:** medium
- **Verdict:** CORRECT
- **Expected:** PAYMENT.CONFIRMED_AT + PAYMENT.STATUS_CODE; order header PAYMENT_CONFIRMED_AT; payment linked via ORDER_ID; status lifecycle defined
- **Generated:** explains PAYMENT.STATUS_CODE and PAYMENT.CONFIRMED_AT nullable; includes order-level PAYMENT_CONFIRMED_AT; links PAYMENT to order by PAYMENT.ORDER_ID
- **Analysis:** Correct modeling of both payment- and order-level confirmation.
- **Retrieval:** gt_coverage=1.0, top_score=0.7, gate=proceed

### Q012: How are shipments related to orders and warehouses?
- **Type:** multi_hop | **Difficulty:** medium
- **Verdict:** CORRECT
- **Expected:** SHIPMENT.ORDER_ID → SALES_ORDER_HDR.ORDER_ID; shipment includes source warehouse, tracking, delivery status
- **Generated:** states SHIPMENT references exactly one sales order; uses SHIPMENT.WAREHOUSE_CODE; implies origin/warehouse link
- **Analysis:** Correct order+warehouse relationship.
- **Retrieval:** gt_coverage=1.0, top_score=0.9317, gate=proceed

### Q013: Can a product belong to multiple categories?
- **Type:** negative | **Difficulty:** easy
- **Verdict:** CORRECT
- **Expected:** No; each product belongs to exactly one category (TB_PRODUCT.CATEGORY_ID FK)
- **Generated:** “No” + cites business rule “Belongs to exactly one Category”
- **Analysis:** Correct abstention behavior is *not* used here; an explicit correct negative answer is produced.
- **Retrieval:** gt_coverage=1.0, top_score=0.7, gate=proceed

### Q014: Is it possible for a customer to place an order without payment?
- **Type:** negative | **Difficulty:** medium
- **Verdict:** CORRECT
- **Expected:** Yes, order can exist with payment unconfirmed (PENDING; PAYMENT_CONFIRMED_AT nullable); business rule only prevents shipping before payment confirmation
- **Generated:** “Yes”; points to nullable PAYMENT_CONFIRMED_AT and shipping restriction wording
- **Analysis:** Correct handling of a nuanced negative question.
- **Retrieval:** gt_coverage=1.0, top_score=0.7, gate=proceed

### Q015: What schema fields support monetary value tracking across orders and their line items?
- **Type:** multi_hop | **Difficulty:** easy
- **Verdict:** CORRECT
- **Expected:** SALES_ORDER_HDR.TOTAL_AMT; ORDER_LINE_ITEM.UNIT_PRICE, QUANTITY, LINE_AMT = QUANTITY×UNIT_PRICE; linked via ORDER_ID
- **Generated:** mentions ORDER_LINE_ITEM.UNIT_PRICE and LINE_AMT, tied to ORDER_ID; additionally notes PAYMENT.AMOUNT for order-level payment tracking
- **Analysis:** Correct and adds extra relevant info (payment amount linkage) without contradicting expected answer.
- **Retrieval:** gt_coverage=1.0, top_score=0.7, gate=proceed

## Anomalies & Recommendations

### Red Flags
- **Mild:** Q010 has `gt_coverage=0.75` while remaining correct. This suggests the retrieval layer sometimes doesn’t fetch all expected sources, but the generator compensates using other retrieved context. Not necessarily harmful, but worth monitoring for scaling to more complex datasets.

### Recommendations
1. **Track “coverage-but-not-needed” vs “coverage-missing” cases:** For Q010, assess whether missing expected sources were purely redundant or were about hierarchy semantics; adjust retrieval caps if multi-hop joins become brittle.
2. **Add an explicit check for negative questions:** Currently negative Q013/Q014 are correct. For future datasets, ensure the gate/retrieval quality gate doesn’t let weak evidence leak into explicit “yes/no” answers.
3. **Consider relationship-property enrichment impact:** Builder mapping success is perfect here, but ablation studies that disable cypher healing/reranking should be tested for FK edge correctness and MENTIONS coverage—those are likely the failure points in advanced datasets.

## Comparison Notes (if applicable)
- `ragas` is `null`, so no RAGAS-vs-judge discrepancy can be discussed for this run.
- No baseline AB-00 bundle is provided in the prompt, so I cannot compare directly.

If you can share the baseline configuration/bundle (e.g., AB-00) or an `ablation_context` field for AB-11, I can fill in the **Ablation Impact** dimension per the rubric.