# AI-Judge Evaluation: AB-14/01_basics_ecommerce
**Evaluator:** (`gpt-5.4-nano-2026-03-17`) using `docs/AI_JUDGE_PROMPT.md`  
**Date:** 2026-07-17

---

# Ablation Study Evaluation: AB-14 — 01_basics_ecommerce

## Executive Summary
AB-14 shows excellent end-to-end performance on the e-commerce “basics” dataset: builder completed all 7 tables with zero Cypher failures and the query stage grounded **all 15/15 answers**. The main quality exception is **Q008** (multi-hop) where ground-truth coverage drops to **0.5**, suggesting incomplete retrieval for that specific join/edge chain—however the generated answer remains grounded and correct. Overall, this run indicates the architecture (hybrid retrieval + reranking + KG-grounded generation) is functioning robustly.

## Scores

| Dimension | Score (1-5) | Weight | Weighted |
|---|---:|---:|---:|
| Builder Quality | 5 | 25% | 1.25 |
| Retrieval Effectiveness | 4 | 25% | 1.00 |
| Answer Quality | 5 | 30% | 1.50 |
| Pipeline Health | 5 | 10% | 0.50 |
| Ablation Impact |  N/A | 10% | 0.00 |
| **Overall** |  |  | **4.25** |

## Dimension Analysis

### 1. Builder Quality (5/5)
- `tables_parsed=7`, `tables_completed=7`, `all_tables_completed=true`
- `cypher_failed=false`
- `failed_mappings=[]`, `ingestion_errors=[]`
- Triplet density is healthy: `triplets_extracted=109` across 7 tables (no evidence of sparse extraction).
**Conclusion:** Builder graph construction fully succeeded with no operational issues.

### 2. Retrieval Effectiveness (4/5)
- `avg_gt_coverage=0.95` (strong)
- `avg_top_score=0.789` (healthy confidence for the reranker in this architecture)
- No abstentions: `abstained_count=0`, and all answers are grounded.
- One notable retrieval weakness: **Q008** has `gt_coverage=0.5` while still answering correctly.
**Conclusion:** Retrieval is consistently effective, with a localized multi-hop coverage drop.

### 3. Answer Quality (5/5)
- `query_report.grounded_rate=1.0` and `grounded_count=15`
- `grader_rejection_count=0` across all shown questions (no hallucination detections / no instability)
- Negative questions:
  - **Q013** (negative) correctly states a product belongs to exactly one category (supports “no” to multiple categories).
  - **Q014** (negative) correctly reasons that orders can exist without confirmed payment timestamp (and constrains shipping, not order creation).
**Conclusion:** Answers are semantically correct and properly aligned with KG schema/glossary.

### 4. Pipeline Health (5/5)
- `total_grader_rejections=0`
- `grader_inconsistencies=0`
- `gate_abstentions=0`
- `cypher_failed=false`, `failed_mappings_count=0`, `ingestion_errors_count=0`
**Conclusion:** No self-healing or stability problems observed.

### 5. Ablation Impact (N/A)
- The rubric specifies scoring this only when the bundle contains a comparison vs baseline (e.g., `ablation_context` or `study_id=AB-00`). This bundle includes `study_id=AB-14` but no explicit “changes vs baseline” context is provided.
**Therefore:** Ablation impact cannot be causally validated from the provided bundle alone.

## Per-Question Deep Dive

### Q001: What information is stored for each customer?
- **Type:** direct_mapping | **Difficulty:** easy
- **Verdict:** CORRECT
- **Expected:** customer has unique ID, full name, email (unique), region code, creation date, active status
- **Generated:** lists FULL_NAME, EMAIL, REGION_CODE, IS_ACTIVE, CREATED_AT and references CUSTOMER_MASTER primary key + schema columns
- **Analysis:** Matches the expected schema attributes; no hallucinated customer fields.
- **Retrieval:** gt_coverage=1.0, top_score=0.7, gate=proceed

### Q002: How are products categorized on the platform?
- **Type:** direct_mapping | **Difficulty:** easy
- **Verdict:** CORRECT
- **Expected:** product belongs to exactly one category; category supports parent hierarchy
- **Generated:** explains CATEGORY_ID FK and TB_CATEGORY parent linkage
- **Analysis:** Correct and complete, with hierarchy detail.
- **Retrieval:** gt_coverage=1.0, top_score=0.7, gate=proceed

### Q003: What is the relationship between customers and sales orders?
- **Type:** direct_mapping | **Difficulty:** easy
- **Verdict:** CORRECT
- **Expected:** sales order placed by exactly one customer; customer has zero or more orders
- **Generated:** cites glossary and FK `SALES_ORDER_HDR.CUST_ID -> CUSTOMER_MASTER.CUST_ID`
- **Analysis:** Correct relationship direction and multiplicity.
- **Retrieval:** gt_coverage=1.0, top_score=0.9847, gate=proceed

### Q004: What does an order line item contain?
- **Type:** direct_mapping | **Difficulty:** easy
- **Verdict:** CORRECT
- **Expected:** product, quantity, unit price at purchase time, extended amount; belongs to one sales order
- **Generated:** lists ORDER_LINE_ITEM fields including QUANTITY, UNIT_PRICE, LINE_AMT, plus belongs via ORDER_ID
- **Analysis:** Fully aligned.
- **Retrieval:** gt_coverage=1.0, top_score=0.9872, gate=proceed

### Q005: How are payments linked to orders?
- **Type:** direct_mapping | **Difficulty:** easy
- **Verdict:** CORRECT
- **Expected:** PAYMENT.ORDER_ID -> SALES_ORDER_HDR.ORDER_ID; tracks method, amount, status, confirmation timestamp
- **Generated:** correctly references FK and “for exactly one Sales Order”
- **Analysis:** Correct linking + attributes.
- **Retrieval:** gt_coverage=1.0, top_score=0.9501, gate=proceed

### Q006: What statuses can an order have?
- **Type:** attribute_lookup | **Difficulty:** easy
- **Verdict:** CORRECT
- **Expected:** PENDING, CONFIRMED, SHIPPED, DELIVERED, CANCELLED
- **Generated:** lists all five statuses
- **Analysis:** Correct list.
- **Retrieval:** gt_coverage=1.0, top_score=0.7, gate=proceed

### Q007: Which table stores the product SKU information?
- **Type:** direct_mapping | **Difficulty:** easy
- **Verdict:** CORRECT
- **Expected:** TB_PRODUCT stores SKU
- **Generated:** directly states `TB_PRODUCT.SKU`
- **Analysis:** Fully correct.
- **Retrieval:** gt_coverage=1.0, top_score=0.9886, gate=proceed

### Q008: How can I find all orders placed by a specific customer?
- **Type:** multi_hop | **Difficulty:** medium
- **Verdict:** CORRECT
- **Expected:** filter SALES_ORDER_HDR by CUST_ID; join to CUSTOMER_MASTER.CUST_ID
- **Generated:** explains FK and shows how to filter by `SALES_ORDER_HDR.CUST_ID`
- **Analysis:** Correct join/filter logic, but retrieval was incomplete (only partial GT sources counted).
- **Retrieval:** gt_coverage=0.5, top_score=0.7, gate=proceed

### Q009: How does the schema link orders to their individual product line items?
- **Type:** multi_hop | **Difficulty:** medium
- **Verdict:** CORRECT
- **Expected:** ORDER_LINE_ITEM is junction: ORDER_ID -> SALES_ORDER_HDR, PRODUCT_ID -> TB_PRODUCT; includes QUANTITY, UNIT_PRICE, LINE_AMT
- **Generated:** correctly describes ORDER_LINE_ITEM.ORDER_ID and ORDER_LINE_ITEM.PRODUCT_ID links
- **Analysis:** Correct schema modeling and junction role (quantity/amount conceptually supported).
- **Retrieval:** gt_coverage=1.0, top_score=0.7, gate=proceed

### Q010: Show me the order hierarchy from customer to line items.
- **Type:** multi_hop | **Difficulty:** medium
- **Verdict:** CORRECT
- **Expected:** CUSTOMER_MASTER → SALES_ORDER_HDR → ORDER_LINE_ITEM → TB_PRODUCT
- **Generated:** correctly describes FK path and hierarchy using business relationship summaries
- **Analysis:** Correct 4-level hierarchy.
- **Retrieval:** gt_coverage=0.75, top_score=0.7, gate=proceed

### Q011: How does the schema model the confirmation state of a payment and its relationship to the order?
- **Type:** multi_hop | **Difficulty:** medium
- **Verdict:** CORRECT
- **Expected:** PAYMENT.CONFIRMED_AT + PAYMENT.STATUS_CODE; SALES_ORDER_HDR.PAYMENT_CONFIRMED_AT mirrors; PAYMENT.ORDER_ID links to order; order ships only after confirmed payment
- **Generated:** correctly explains both confirmation fields and link
- **Analysis:** Complete and schema-faithful.
- **Retrieval:** gt_coverage=1.0, top_score=0.7, gate=proceed

### Q012: How are shipments related to orders and warehouses?
- **Type:** multi_hop | **Difficulty:** medium
- **Verdict:** CORRECT
- **Expected:** SHIPMENT.ORDER_ID -> SALES_ORDER_HDR; SHIPMENT.WAREHOUSE_CODE; includes tracking + delivery status
- **Generated:** correctly describes linkage to orders and warehouse code; references “one order may have multiple partial shipments”
- **Analysis:** Correct and complete.
- **Retrieval:** gt_coverage=1.0, top_score=0.9283, gate=proceed

### Q013: Can a product belong to multiple categories?
- **Type:** negative | **Difficulty:** easy
- **Verdict:** CORRECT
- **Expected:** No; TB_PRODUCT has single CATEGORY_ID FK to TB_CATEGORY
- **Generated:** “No” with glossary + schema justification
- **Analysis:** Proper negative handling; no fabrication.
- **Retrieval:** gt_coverage=1.0, top_score=0.7, gate=proceed

### Q014: Is it possible for a customer to place an order without payment?
- **Type:** negative | **Difficulty:** medium
- **Verdict:** CORRECT
- **Expected:** order can exist with STATUS_CODE default PENDING; PAYMENT_CONFIRMED_AT nullable; shipping requires confirmed payment
- **Generated:** states PAYMENT_CONFIRMED_AT nullable implies order can exist without confirmation; payment constraints apply to shipping
- **Analysis:** Correct nuance for negative question (it answers “possible” while respecting business rule about shipping).
- **Retrieval:** gt_coverage=1.0, top_score=0.7, gate=proceed

### Q015: What schema fields support monetary value tracking across orders and their line items?
- **Type:** multi_hop | **Difficulty:** easy
- **Verdict:** CORRECT
- **Expected:** SALES_ORDER_HDR.TOTAL_AMT; ORDER_LINE_ITEM.UNIT_PRICE + QUANTITY + LINE_AMT; linked by ORDER_ID
- **Generated:** mentions per-line UNIT_PRICE/LINE_AMT and ties PAYMENT.AMOUNT to order; describes ORDER_ID linkage
- **Analysis:** Slightly different from expected (uses PAYMENT amount for order-level settlement rather than emphasizing TOTAL_AMT), but still consistent with monetary tracking across order/payment/line levels and remains grounded.
- **Retrieval:** gt_coverage=1.0, top_score=0.7, gate=proceed

## Anomalies & Recommendations

### Red Flags
- **Localized retrieval miss:** **Q008** shows `gt_coverage=0.5` even though the final answer is correct. This suggests the retriever may not always fetch the minimal “customer-to-orders” chain consistently, relying instead on glossary-generalization.
- Retrieval quality scores for several “easy/direct” questions are clipped at **0.7** (likely due to the pipeline’s pool-confidence floor). This can mask underlying retrieval variance.

### Recommendations
1. **Investigate Q008 retrieval sources:** confirm whether the traversal/graph retrieval missed `CUSTOMER_MASTER → SALES_ORDER_HDR` or only partially retrieved it; improve entity resolution / traversal weights specifically for `CUST_ID`-based joins.
2. **Report both adjusted and raw retriever confidence distribution:** since many questions share `retrieval_quality_score=0.7`, add diagnostics for cases where raw reranker confidence differs but is masked by thresholding.
3. **For negative questions, keep an explicit “constraint vs existence” template:** Q014 handled this well; codify it to prevent future regressions (e.g., confusion between “order exists” vs “order can ship”).

## Comparison Notes (if applicable)
- Not applicable: the bundle does not include a baseline comparison artifact (e.g., `ablation_context.changes_vs_baseline`). Therefore, causal statements about AB-14 vs AB-00 cannot be made from the provided JSON.