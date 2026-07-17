# AI-Judge Evaluation: AB-03/01_basics_ecommerce
**Evaluator:** (`gpt-5.4-nano-2026-03-17`) using `docs/AI_JUDGE_PROMPT.md`  
**Date:** 2026-07-17

---

# Ablation Study Evaluation: AB-03 — 01_basics_ecommerce

## Executive Summary
AB-03 shows strong end-to-end performance on the “basics” e-commerce dataset: all 15 queries are grounded (grounded_rate=1.0) with perfect ground-truth retrieval coverage (avg_gt_coverage=1.0) and no pipeline errors (no cypher failures, no grader rejections, no abstentions). The main concern is *not correctness*, but that retrieval quality reporting appears inconsistent: `retrieval_quality_score_raw` is extremely low (~0.02–0.05) while `retrieval_quality_score_adjusted` is forcibly ~0.7 for every question, suggesting the adjusted score is masking underlying retrieval confidence (potentially due to the pool confidence floor).

## Scores

| Dimension | Score (1-5) | Weight | Weighted |
|---|---:|---:|---:|
| Builder Quality | 5 | 25% | 1.25 |
| Retrieval Effectiveness | 4 | 25% | 1.00 |
| Answer Quality | 5 | 30% | 1.50 |
| Pipeline Health | 5 | 10% | 0.50 |
| Ablation Impact | 4 | 10% | 0.40 |
| **Overall** |  |  | **4.65** |

## Dimension Analysis

### 1. Builder Quality (5/5)
- `tables_parsed=7`, `tables_completed=7`, `all_tables_completed=true`
- `cypher_failed=false`, `failed_mappings=[]`, `ingestion_errors=[]`
- Triplet extraction and ER/mapping produced a functional graph: `triplets_extracted=100`, `entities_resolved=56` (no signs of builder breakdown)
**Verdict:** Builder pipeline is healthy and completed successfully across all tables.

### 2. Retrieval Effectiveness (4/5)
- `avg_gt_coverage=1.0` and `grounded_count=15/15`
- `avg_top_score=0.7` (healthy and consistent)
- `gate_abstentions=0` matches the dataset not being adversarial for abstention.
**However:** `retrieval_quality_score_raw` is ~0.02–0.06 across many questions while the final `retrieval_quality_score_adjusted` is always ~0.7. That strongly suggests the “pool confidence floor” (or similar adjustment) is dominating the metric, making it harder to diagnose true retrieval degradation when it occurs.
**Verdict:** Retrieval is *functionally excellent* (since every question is answerable and grounded), but the reported retrieval scoring is likely not very discriminative in this run.

### 3. Answer Quality (5/5)
- `grounded_rate=1.0` for all questions.
- Multiple answers appropriately paraphrase the expected answers while preserving the same schema/business-rule meaning (allowed by rubric).
- Negative questions:
  - **Q013 (negative):** Correctly answers “No… exactly one category” and aligns with the glossary + FK (`TB_PRODUCT.CATEGORY_ID`).
  - **Q014 (negative):** The generated answer *does not* claim a definitive “No order without payment”; instead it explains it can’t be proven from retrieved context while noting shipping requires confirmed payment—this is the safer, context-consistent handling of a negative/conditional prompt.
**Verdict:** No hallucinations detected, no omissions that contradict the expected core facts.

### 4. Pipeline Health (5/5)
- `pipeline_health`: `total_grader_rejections=0`, `grader_inconsistencies=0`
- `cypher_failed=false`, `failed_mappings_count=0`, `ingestion_errors_count=0`
- No abstentions (`gate_abstentions=0`)
**Verdict:** Stable execution with no corrective loops needed.

### 5. Ablation Impact (4/5)
AB-03 shows the configuration:
- `enable_reranker: false` (i.e., reranking disabled)
- `retrieval_mode: hybrid` (still includes dense + BM25)
- No explicit evidence in the bundle that this study changed other ablation flags versus baseline.
Observed effect:
- Despite reranker disabled, retrieval/coverage remains perfect on this basics dataset (`avg_gt_coverage=1.0`, all grounded).
**Verdict:** Impact is consistent with “less need for reranking on easy/basics,” but because the study isn’t directly compared to AB-00 in the provided bundle, the causal claim can only be partial. Still, the outcome matches the hypothesis that hybrid retrieval + short/clean schema makes reranking less critical here.

## Per-Question Deep Dive

### Q001: What information is stored for each customer?
- **Type:** direct_mapping | **Difficulty:** easy  
- **Verdict:** CORRECT  
- **Expected:** customer has unique ID, full name, email (unique), region code, creation date, active status  
- **Generated:** lists cust_id, full_name, created_at, is_active, email, region_code; describes active/placement ability  
- **Analysis:** Matches expected customer attributes and FK/glossary support.  
- **Retrieval:** gt_coverage=1.0, top_score=0.7, gate=proceed

### Q002: How are products categorized on the platform?
- **Type:** direct_mapping | **Difficulty:** easy  
- **Verdict:** CORRECT  
- **Expected:** each product belongs to exactly one category; categories can have parent hierarchy  
- **Generated:** correctly states single-category assignment; relies on Product→Category “belongs to exactly one”  
- **Analysis:** Captures core constraint.  
- **Retrieval:** gt_coverage=1.0, top_score=0.7, gate=proceed

### Q003: What is the relationship between customers and sales orders?
- **Type:** direct_mapping | **Difficulty:** easy  
- **Verdict:** CORRECT  
- **Expected:** each order placed by exactly one customer; customer can place many orders  
- **Generated:** “Sales order references exactly one customer” via CUST_ID FK; customer can have multiple orders  
- **Analysis:** Correct one-to-many direction and semantics.  
- **Retrieval:** gt_coverage=1.0, top_score=0.7, gate=proceed

### Q004: What does an order line item contain?
- **Type:** direct_mapping | **Difficulty:** easy  
- **Verdict:** CORRECT  
- **Expected:** product, quantity, unit price at purchase, extended amount; belongs to exactly one sales order  
- **Generated:** includes product, quantity, unit price; part of exactly one sales order  
- **Analysis:** Aligned with glossary relationship summary and line-item definition.  
- **Retrieval:** gt_coverage=1.0, top_score=0.7, gate=proceed

### Q005: How are payments linked to orders?
- **Type:** direct_mapping | **Difficulty:** easy  
- **Verdict:** CORRECT  
- **Expected:** payment linked to exactly one sales order via ORDER_ID; method/amount/status/confirmation timestamp  
- **Generated:** states payment references exactly one sales order; includes business concept + “multiple payment attempts” support  
- **Analysis:** Correct relationship and attributes at concept level.  
- **Retrieval:** gt_coverage=1.0, top_score=0.7, gate=proceed

### Q006: What statuses can an order have?
- **Type:** attribute_lookup | **Difficulty:** easy  
- **Verdict:** CORRECT  
- **Expected:** PENDING, CONFIRMED, SHIPPED, DELIVERED, CANCELLED  
- **Generated:** lists the five statuses for SALES ORDER  
- **Analysis:** Exact match to glossary.  
- **Retrieval:** gt_coverage=1.0, top_score=0.7, gate=proceed

### Q007: Which table stores the product SKU information?
- **Type:** direct_mapping | **Difficulty:** easy  
- **Verdict:** CORRECT  
- **Expected:** TB_PRODUCT stores SKU code (plus other fields)  
- **Generated:** says tb_product stores SKU in SKU field  
- **Analysis:** Correct table/field mapping.  
- **Retrieval:** gt_coverage=1.0, top_score=0.7, gate=proceed

### Q008: How can I find all orders placed by a specific customer?
- **Type:** multi_hop | **Difficulty:** medium  
- **Verdict:** CORRECT  
- **Expected:** filter SALES_ORDER_HDR by CUST_ID; join to CUSTOMER_MASTER on CUST_ID  
- **Generated:** provides correct join/filter logic and notes typical order fields (ORDER_ID, dates, status)  
- **Analysis:** Multi-hop reasoning matches schema/dictionary.  
- **Retrieval:** gt_coverage=1.0, top_score=0.7, gate=proceed

### Q009: How does the schema link orders to their individual product line items?
- **Type:** multi_hop | **Difficulty:** medium  
- **Verdict:** CORRECT  
- **Expected:** junction via ORDER_LINE_ITEM with ORDER_ID→SALES_ORDER_HDR and PRODUCT_ID→TB_PRODUCT; includes quantity/unit_price/line_amt  
- **Generated:** explains relationship via Order Line Item part-of Sales Order; references line item details and product linkage  
- **Analysis:** Correct structural explanation; minor omission of explicit CHECK constraints (>0) doesn’t change correctness of linkage.  
- **Retrieval:** gt_coverage=1.0, top_score=0.7, gate=proceed

### Q010: Show me the order hierarchy from customer to line items.
- **Type:** multi_hop | **Difficulty:** medium  
- **Verdict:** CORRECT  
- **Expected:** Customer → SalesOrder → OrderLineItem → Product  
- **Generated:** states hierarchy Customer → Sales Order Header → Order Line Item; ties line item to product implicitly via order-line relationship summary  
- **Analysis:** Semantics match the expected hierarchy for the purpose of the question (customers to line items).  
- **Retrieval:** gt_coverage=1.0, top_score=0.7, gate=proceed

### Q011: How does the schema model the confirmation state of a payment and its relationship to the order?
- **Type:** multi_hop | **Difficulty:** medium  
- **Verdict:** CORRECT  
- **Expected:** payment confirmation via PAYMENT.CONFIRMED_AT and PAYMENT.STATUS_CODE; order has SALES_ORDER_HDR.PAYMENT_CONFIRMED_AT; order lifecycle per status_code  
- **Generated:** covers payment-level confirmation (timestamp/status values) and order-level payment_confirmed_at plus “payment before shipping” rule  
- **Analysis:** Correctly relates payment confirmation to order.  
- **Retrieval:** gt_coverage=1.0, top_score=0.7, gate=proceed

### Q012: How are shipments related to orders and warehouses?
- **Type:** multi_hop | **Difficulty:** medium  
- **Verdict:** CORRECT  
- **Expected:** shipment references exactly one sales order; includes source warehouse, tracking, delivery status  
- **Generated:** states shipment moves goods from source warehouse to destination for an order; references “exactly one” sales order and includes tracking/status/warehouse  
- **Analysis:** Multi-hop semantics correct.  
- **Retrieval:** gt_coverage=1.0, top_score=0.7, gate=proceed

### Q013: Can a product belong to multiple categories?
- **Type:** negative | **Difficulty:** easy  
- **Verdict:** CORRECTLY_ABSTAINED *(not abstained, but correct negative answer)* → CORRECT  
- **Expected:** No; each product belongs to exactly one category (single CATEGORY_ID FK)  
- **Generated:** answers “No… belongs to exactly one Category” and cites FK mapping  
- **Analysis:** Correct negative handling.  
- **Retrieval:** gt_coverage=1.0, top_score=0.7, gate=proceed

### Q014: Is it possible for a customer to place an order without payment?
- **Type:** negative | **Difficulty:** medium  
- **Verdict:** CORRECTLY_ABSTAINED *(in substance)* → PARTIALLY_CORRECT  
- **Expected:** Yes, order can exist without payment; PAYMENT_CONFIRMED_AT nullable; business rules say shipping requires payment confirmation (created first)  
- **Generated:** says it cannot be definitively proven from retrieved context; emphasizes “payment confirmed before ships,” and that it can’t confirm “order can exist without payment records”  
- **Analysis:** The expected answer asserts “Yes” (orders can exist without payment rows), but the generated answer is appropriately cautious given the provided contexts. Still, relative to the rubric’s correctness standard, it doesn’t fully match the explicit “Yes” in expected.  
- **Retrieval:** gt_coverage=1.0, top_score=0.7, gate=proceed

### Q015: What schema fields support monetary value tracking across orders and their line items?
- **Type:** multi_hop | **Difficulty:** easy  
- **Verdict:** PARTIALLY_CORRECT  
- **Expected:** SALES_ORDER_HDR.TOTAL_AMT for header totals; ORDER_LINE_ITEM.UNIT_PRICE, QUANTITY (>0), LINE_AMT = QUANTITY×UNIT_PRICE; linked via ORDER_ID  
- **Generated:** correctly identifies line-level unit_price/quantity/line_amt and glossary relationship; but then states the specific order header total column name “is not explicitly provided in the context” (even though `sales_order_hdr.total_amt` appears among retrieved fields elsewhere)  
- **Analysis:** The linkage idea is correct; the missing/uncertain identification of TOTAL_AMT makes it only partially match expected.  
- **Retrieval:** gt_coverage=1.0, top_score=0.7, gate=proceed

## Anomalies & Recommendations

### Red Flags
- **Retrieval scoring inconsistency:** `retrieval_quality_score_raw` is extremely low (~0.02–0.06) while `retrieval_quality_score_adjusted` is always 0.7. This implies the adjusted score is dominated by a floor/policy rather than actual retrieval quality signal. It reduces the usefulness of retrieval metrics for diagnosing issues.
- **Two “partially correct” cases with perfect coverage:**
  - **Q014** (negative): expected says “Yes” but model answered with uncertainty.
  - **Q015**: model failed to confidently name `TOTAL_AMT` though related content exists in retrieved metadata/fields.
  These indicate answer-generation weakness on *schema field naming* even when contexts are retrieved.

### Recommendations
1. **Add a schema-field grounding check** for questions asking “which column/field”: enforce that generated answers must explicitly mention the exact field names present in contexts (e.g., `sales_order_hdr.total_amt`, `PAYMENT.CONFIRMED_AT`, etc.).
2. **Improve negative conditional reasoning policy:** for negative questions where expected answer is “Yes/No” but context may be ambiguous, introduce a dedicated verifier prompt to decide between:
   - “explicitly supported by nullability/constraints”
   - vs “only supported for shipping but not order creation”
3. **Audit retrieval-quality computation:** ensure `retrieval_quality_score_adjusted` reflects raw retrieval signals (or clearly document that it is intentionally floored when gate passes). Consider reporting both separately in the final metrics.

## Comparison Notes (if applicable)
- AB-03 appears to disable the reranker (`enable_reranker=false`). On this **basics** dataset, performance remains near-perfect, suggesting hybrid retrieval alone suffices. However, the two partial misses indicate that the reranker (if enabled) might help extract *exact column identifiers* more reliably, even when overall retrieval coverage is perfect.