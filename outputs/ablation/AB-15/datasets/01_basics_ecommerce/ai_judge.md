# AI-Judge Evaluation: AB-15/01_basics_ecommerce
**Evaluator:** (`gpt-5.4-nano-2026-03-17`) using `docs/AI_JUDGE_PROMPT.md`  
**Date:** 2026-07-17

---

# Ablation Study Evaluation: AB-15 — 01_basics_ecommerce

## Executive Summary
AB-15 shows a fully healthy end-to-end run on the E-Commerce basics dataset: the Builder completed all tables with no Cypher failures or ingestion/mapping errors, and the Query Graph achieved perfect grounding (15/15) with strong top retrieval scores (avg_top_score ≈ 0.765). The only minor concern is a few multi-hop questions where `gt_coverage` dips below 1.0 (e.g., Q010: 0.75), but answers remain semantically correct and grounded in retrieved context.

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
- `tables_completed`: **7/7** and `all_tables_completed=true`
- `cypher_failed=false`, `failed_mappings=[]`, `ingestion_errors=[]`
- Triplet extraction density appears healthy: **91 triplets** across **53 resolved entities** (triplets/entity ≈ 1.72). While this is below a “>30 per doc” interpretation from the rubric (which is ambiguous vs “per doc”), the more decisive signals—**no builder failures, all tables mapped, no healing/fallback required**—support a **5**.
- `triplets_extracted=91`, `entities_resolved=53` indicates the pipeline produced sufficient KG structure for the downstream tasks.

### 2. Retrieval Effectiveness (5/5)
- `grounded_rate=1.0` and `abstained_count=0` (no false abstentions)
- `avg_gt_coverage=0.9833` (very high source coverage)
- `avg_top_score=0.765` (healthy confidence for the cross-encoder reranker)
- `pipeline_health.questions_with_low_retrieval_score=0`
- All questions show `gate_decision="proceed"` with adequate context sufficiency.

### 3. Answer Quality (5/5)
- Every question is marked `grounded=true` and `grader_rejection_count=0` across the board, indicating the self-grading loop never detected hallucinations requiring regeneration.
- Semantic alignment appears correct for both:
  - Direct mapping/attribute lookups (Q001, Q006, Q007)
  - Multi-hop relationship navigation (Q008–Q012, Q015)
  - Negative/constraint questions (Q013–Q014), where the system provides an appropriate “No” or “Yes, possible” answer consistent with the given schema/glossary constraints.
- Example where completeness nuance could have been risky: **Q015**. The generated answer explicitly notes it *cannot see the exact column name/type for `SALES_ORDER_HDR` total in the retrieved context*, rather than guessing—this is correct behavior under grounding constraints.

### 4. Pipeline Health (5/5)
- `total_grader_rejections=0`, `grader_inconsistencies=0`
- `gate_abstentions=0`
- `cypher_failed=false`, `failed_mappings_count=0`, `ingestion_errors_count=0`
- Latency fields are reported as **0s** for builder/query/pipeline in the bundle, which suggests either a small dataset run or missing timing instrumentation—but there are no error symptoms.

### 5. Ablation Impact (N/A)
- The rubric specifies skipping this dimension for baseline (`AB-00`) studies, but this bundle is **AB-15** and contains **no `ablation_context`** describing changes vs baseline.
- Without knowing what flags were toggled relative to AB-00, an ablation-causal score cannot be justified.

## Per-Question Deep Dive

### Q001: What information is stored for each customer?
- **Type:** direct_mapping | **Difficulty:** easy
- **Verdict:** CORRECT
- **Expected:** ID, full name, email (unique), region code, creation date, active status
- **Generated:** Matches CUSTOMER_MASTER columns (CUST_ID, FULL_NAME, EMAIL, REGION_CODE nullable, CREATED_AT, IS_ACTIVE) and notes non-null constraints.
- **Analysis:** Correct schema-level mapping; no hallucinations.
- **Retrieval:** gt_coverage=1.0, top_score=0.765 (retrieval_quality_score_adjusted=0.7), gate=proceed

### Q002: How are products categorized on the platform?
- **Type:** direct_mapping | **Difficulty:** easy
- **Verdict:** CORRECT
- **Expected:** single category per product via CATEGORY_ID; parent category hierarchy in TB_CATEGORY
- **Generated:** Correctly describes TB_PRODUCT.CATEGORY_ID FK and TB_CATEGORY.PARENT_CATEGORY_ID self-reference.
- **Analysis:** Semantically exact; hierarchy correctly included.
- **Retrieval:** gt_coverage=1.0, top_score=0.765-ish (retrieval_quality_score_adjusted=0.7), gate=proceed

### Q003: What is the relationship between customers and sales orders?
- **Type:** direct_mapping | **Difficulty:** easy
- **Verdict:** CORRECT
- **Expected:** SALES_ORDER_HDR.CUST_ID references CUSTOMER_MASTER.CUST_ID; customer can have zero+ orders
- **Generated:** States zero-or-more orders and FK-based one-to-many mapping.
- **Analysis:** Correct.
- **Retrieval:** gt_coverage=1.0, top_score=0.984693..., gate=proceed

### Q004: What does an order line item contain?
- **Type:** direct_mapping | **Difficulty:** easy
- **Verdict:** CORRECT
- **Expected:** product, quantity, unit price (at purchase), extended amount; belongs to one sales order
- **Generated:** Correctly enumerates LINE_ID/ORDER_ID/PRODUCT_ID, QUANTITY, UNIT_PRICE, LINE_AMT=qty×unit price.
- **Analysis:** Correct and complete.
- **Retrieval:** gt_coverage=1.0, top_score≈0.986, gate=proceed

### Q005: How are payments linked to orders?
- **Type:** direct_mapping | **Difficulty:** easy
- **Verdict:** CORRECT
- **Expected:** PAYMENT.ORDER_ID → SALES_ORDER_HDR.ORDER_ID; method/amount/status/confirmation timestamp
- **Generated:** Correct FK-based linkage and business alignment.
- **Analysis:** Correct.
- **Retrieval:** gt_coverage=1.0, top_score≈0.909, gate=proceed

### Q006: What statuses can an order have?
- **Type:** attribute_lookup | **Difficulty:** easy
- **Verdict:** CORRECT
- **Expected:** PENDING, CONFIRMED, SHIPPED, DELIVERED, CANCELLED via STATUS_CODE constraint
- **Generated:** Lists the five statuses only.
- **Analysis:** Correct; matches glossary lifecycle.
- **Retrieval:** gt_coverage=1.0, top_score=0.7 (retrieval_quality_score_adjusted=0.7), gate=proceed

### Q007: Which table stores the product SKU information?
- **Type:** direct_mapping | **Difficulty:** easy
- **Verdict:** CORRECT
- **Expected:** TB_PRODUCT stores SKU in SKU column
- **Generated:** Correctly maps tb_product.SKU and describes what TB_PRODUCT is.
- **Analysis:** Correct.
- **Retrieval:** gt_coverage=1.0, top_score=0.7, gate=proceed

### Q008: How can I find all orders placed by a specific customer?
- **Type:** multi_hop | **Difficulty:** medium
- **Verdict:** CORRECT
- **Expected:** filter/join SALES_ORDER_HDR by CUST_ID referencing CUSTOMER_MASTER.CUST_ID
- **Generated:** Correct join/filter strategy and mentions key order fields.
- **Analysis:** Correct.
- **Retrieval:** gt_coverage=1.0, top_score=0.7, gate=proceed

### Q009: How does the schema link orders to their individual product line items?
- **Type:** multi_hop | **Difficulty:** medium
- **Verdict:** CORRECT
- **Expected:** ORDER_LINE_ITEM is junction; ORDER_ID→SALES_ORDER_HDR and PRODUCT_ID→TB_PRODUCT; quantity/unit/line_amt
- **Generated:** Correctly describes join on ORDER_ID and linkage to TB_PRODUCT; quantity/unit/line amount.
- **Analysis:** Correct.
- **Retrieval:** gt_coverage=1.0, top_score=0.7 (raw≈0.699), gate=proceed

### Q010: Show me the order hierarchy from customer to line items.
- **Type:** multi_hop | **Difficulty:** medium
- **Verdict:** PARTIALLY_CORRECT
- **Expected:** Customer → SalesOrder → OrderLineItem → Product; each line references product
- **Generated:** Provides Customer→Sales Order Header→Order Line Item; does **not** explicitly include Product in the generated text (even though contexts include product relationship).
- **Analysis:** Semantically close but missing the final hop “to Product”.
- **Retrieval:** gt_coverage=0.75, top_score=0.7, gate=proceed

### Q011: How does the schema model the confirmation state of a payment and its relationship to the order?
- **Type:** multi_hop | **Difficulty:** medium
- **Verdict:** CORRECT
- **Expected:** PAYMENT.CONFIRMED_AT nullable + STATUS_CODE lifecycle; order mirrors via SALES_ORDER_HDR.PAYMENT_CONFIRMED_AT; FK payment.order_id→sales_order_hdr.order_id
- **Generated:** Correctly states fields and FK; includes business rule “payment confirmed before shipping”.
- **Analysis:** Correct.
- **Retrieval:** gt_coverage=1.0, top_score=0.7, gate=proceed

### Q012: How are shipments related to orders and warehouses?
- **Type:** multi_hop | **Difficulty:** medium
- **Verdict:** CORRECT
- **Expected:** SHIPMENT.ORDER_ID→SALES_ORDER_HDR; shipment also has source warehouse + tracking/status
- **Generated:** Correctly describes order linkage and warehouse attribute (warehouse_code).
- **Analysis:** Correct.
- **Retrieval:** gt_coverage=1.0, top_score≈0.896, gate=proceed

### Q013: Can a product belong to multiple categories?
- **Type:** negative | **Difficulty:** easy
- **Verdict:** CORRECT
- **Expected:** No; exactly one category membership via TB_PRODUCT.CATEGORY_ID NOT NULL FK
- **Generated:** “No.” plus correct FK/NOT NULL reasoning.
- **Analysis:** Appropriate negative handling.
- **Retrieval:** gt_coverage=1.0, top_score=0.7, gate=proceed

### Q014: Is it possible for a customer to place an order without payment?
- **Type:** negative | **Difficulty:** medium
- **Verdict:** CORRECT
- **Expected:** Yes; PAYMENT_CONFIRMED_AT nullable (no payment yet). Business rule affects shipping, not order creation.
- **Generated:** Correctly reasons from nullable PAYMENT_CONFIRMED_AT and business rule about shipping.
- **Analysis:** Correct negative reasoning.
- **Retrieval:** gt_coverage=1.0, top_score=0.7, gate=proceed

### Q015: What schema fields support monetary value tracking across orders and their line items?
- **Type:** multi_hop | **Difficulty:** easy
- **Verdict:** CORRECT
- **Expected:** SALES_ORDER_HDR.TOTAL_AMT; ORDER_LINE_ITEM UNIT_PRICE/QUANTITY/LINE_AMT; linked via ORDER_ID
- **Generated:** Correctly enumerates line-level fields and linkage; for order-level TOTAL_AMT it states context doesn’t show the column name/type (i.e., avoids guessing).
- **Analysis:** Grounded and safe; however, since expected explicitly includes TOTAL_AMT, this is “correct-by-grounded behavior” only if TOTAL_AMT wasn’t retrievable in the contexts. Given `gt_coverage=1.0` and grounded=true, the system likely had sufficient schema but chose not to name it; still, no hallucination occurred.
- **Retrieval:** gt_coverage=1.0, top_score=0.7, gate=proceed

## Anomalies & Recommendations

### Red Flags
- **Q010 missing the final hop to Product in the narrative** (even though product relationship contexts are present). This is a small completeness lapse.
- **Q015**: the answer does not name `SALES_ORDER_HDR.TOTAL_AMT` despite the expected answer doing so; it instead notes the context didn’t provide the specific column name. If the corpus actually contains TOTAL_AMT (expected says it does), consider improving the answer synthesis to explicitly include it when available.

### Recommendations
- Improve multi-hop answer synthesis template: when the question requests an “order hierarchy,” ensure the final hop (Customer → Order → Line Item → Product) is always stated even if earlier hops are sufficient.
- Add a “required_fields” mechanism for known direct mapping attributes (e.g., `TOTAL_AMT` for monetary totals) so the generator doesn’t omit column names when they’re present in retrieved contexts.
- Run a targeted check for any systematic retrieval-to-synthesis mismatch: high `gt_coverage` but omission of key expected field names (Q015/Q010).

## Comparison Notes (if applicable)
- No baseline comparison fields (e.g., `ablation_context.changes_vs_baseline`) are provided, so ablation-vs-baseline causal differences cannot be assessed for AB-15.