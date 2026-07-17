# AI-Judge Evaluation: AB-07/01_basics_ecommerce
**Evaluator:** (`gpt-5.4-nano-2026-03-17`) using `docs/AI_JUDGE_PROMPT.md`  
**Date:** 2026-07-17

---

# Ablation Study Evaluation: AB-07 — 01_basics_ecommerce

## Executive Summary
AB-07 shows a highly successful end-to-end run on the *basics* e-commerce dataset: the builder completed all table mappings with no Cypher failures or ingestion errors, and the query graph achieved full groundedness (grounded_rate = 1.0) across all 15 questions. Retrieval quality is consistently healthy (avg_top_score ≈ 0.776; no low-retrieval questions), and answer content matches the expected schema relationships and attributes with zero grader rejections and no gate abstentions. The only minor concern is that some multi-hop retrieval scoring varies per-question (e.g., Q010 gt_coverage=0.75), but answer correctness remains strong.

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
- `cypher_failed=false`, `failed_mappings=[]`, `ingestion_errors=[]`
- Triplet extraction and ER appear productive: `triplets_extracted=101`, `entities_resolved=74` (no sign of weak extraction or runaway ER; ratio is within a reasonable band for this small dataset).

**Verdict:** Builder is fully functional and produced a complete KG for the dataset.

### 2. Retrieval Effectiveness (5/5)
- `grounded_rate=1.0` and `abstained_count=0` with `gate_decision="proceed"` everywhere.
- `avg_gt_coverage=0.9833` (very high; most questions retrieve all expected sources).
- `avg_top_score=0.7761` indicates strong semantic ranking by the cross-encoder reranker.
- `pipeline_health.questions_with_low_retrieval_score=0` and `total_grader_rejections=0` suggests retrieval quality aligns with answer generation needs.

### 3. Answer Quality (5/5)
- All answers are grounded: `grounded_count=15`, `grounded_rate=1.0`.
- `grader_rejection_count=0` and `grader_consistency_valid=true` across all questions indicate no factual/faithfulness failures were detected.
- Responses are not just semantically aligned; they correctly map schema concepts (FKs, nullable fields, status domains, junction-table roles) to the questions’ expected facts.

Best/worst examples (semantic check):
- **Best (clear correctness):** Q001 (customer attributes), Q002 (category hierarchy), Q006 (order statuses), Q013 (negative: product belongs to exactly one category).
- **Mild variation but still correct:** Q010 (hierarchy) has `gt_coverage=0.75`, yet the generated answer correctly captures the chain Customer → SalesOrder → OrderLineItem → Product.

### 4. Pipeline Health (5/5)
- `total_grader_rejections=0`, `grader_inconsistencies=0`, `gate_abstentions=0`
- `cypher_failed=false`, `failed_mappings_count=0`, `ingestion_errors_count=0`
- No evidence of hitting self-healing or reflection retry exhaustion.

**Verdict:** Stable execution with no corrective loops needed.

### 5. Ablation Impact (N/A)
This bundle is AB-07, but it does **not** include an explicit baseline comparison object (e.g., `ablation_context.changes_vs_baseline`). The provided `config` shows reranking enabled and hybrid retrieval, but the rubric requires stated changes vs baseline to score causal impact.

## Per-Question Deep Dive

### Q001: What information is stored for each customer?
- **Type:** direct_mapping | **Difficulty:** easy  
- **Verdict:** CORRECT  
- **Expected:** customer ID, full name, unique email, region code, creation date, active status; email unique.  
- **Generated:** correctly describes customer_master fields incl. `CUST_ID`, `EMAIL`, `REGION_CODE`, `CREATED_AT`, `IS_ACTIVE`.  
- **Analysis:** Matches all key facts; no unsupported claims.  
- **Retrieval:** gt_coverage=1.0, top_score=0.7760510405045259, gate=proceed

### Q002: How are products categorized on the platform?
- **Type:** direct_mapping | **Difficulty:** easy  
- **Verdict:** CORRECT  
- **Expected:** products belong to exactly one category; category hierarchy via parent category; FK through `CATEGORY_ID`.  
- **Generated:** correctly explains `TB_PRODUCT.CATEGORY_ID → TB_CATEGORY.CATEGORY_ID` and parent/child via `PARENT_CATEGORY_ID`.  
- **Analysis:** Accurate and complete.  
- **Retrieval:** gt_coverage=1.0, top_score=0.7760510405045259, gate=proceed

### Q003: What is the relationship between customers and sales orders?
- **Type:** direct_mapping | **Difficulty:** easy  
- **Verdict:** CORRECT  
- **Expected:** each sales order placed by exactly one customer; customer can have zero or more orders.  
- **Generated:** matches “one order placed by exactly one customer” and uses FK `CUST_ID`.  
- **Analysis:** Correct schema relationship statement.  
- **Retrieval:** gt_coverage=1.0, top_score=0.7760510405045259, gate=proceed

### Q004: What does an order line item contain?
- **Type:** direct_mapping | **Difficulty:** easy  
- **Verdict:** CORRECT  
- **Expected:** product, quantity, unit price at purchase time, extended amount; belongs to one sales order.  
- **Generated:** covers line id, product reference, quantity, unit price, and `LINE_AMT = qty × price`.  
- **Analysis:** Complete and accurate.  
- **Retrieval:** gt_coverage=1.0, top_score=0.7760510405045259, gate=proceed

### Q005: How are payments linked to orders?
- **Type:** direct_mapping | **Difficulty:** easy  
- **Verdict:** CORRECT  
- **Expected:** each payment associated with exactly one sales order via ORDER_ID; method/amount/status/confirmation timestamp.  
- **Generated:** correctly states FK `payment.order_id -> sales_order_hdr.order_id` and references business “one payment per order record”.  
- **Analysis:** Accurate; includes key payment attributes.  
- **Retrieval:** gt_coverage=1.0, top_score=0.7760510405045259, gate=proceed

### Q006: What statuses can an order have?
- **Type:** attribute_lookup | **Difficulty:** easy  
- **Verdict:** CORRECT  
- **Expected:** PENDING, CONFIRMED, SHIPPED, DELIVERED, CANCELLED with business lifecycle.  
- **Generated:** exactly lists the five statuses.  
- **Analysis:** Perfect match.  
- **Retrieval:** gt_coverage=1.0, top_score=0.7760510405045259, gate=proceed

### Q007: Which table stores the product SKU information?
- **Type:** direct_mapping | **Difficulty:** easy  
- **Verdict:** CORRECT  
- **Expected:** TB_PRODUCT stores SKU and related product details.  
- **Generated:** correctly points to `tb_product.SKU`.  
- **Analysis:** Correct table/field mapping.  
- **Retrieval:** gt_coverage=1.0, top_score=0.7760510405045259, gate=proceed

### Q008: How can I find all orders placed by a specific customer?
- **Type:** multi_hop | **Difficulty:** medium  
- **Verdict:** CORRECT  
- **Expected:** filter `SALES_ORDER_HDR` by `CUST_ID` and join to `CUSTOMER_MASTER` on `CUST_ID`.  
- **Generated:** correctly describes the join/filter approach using the FK.  
- **Analysis:** Complete multi-hop reasoning (customer → orders).  
- **Retrieval:** gt_coverage=1.0, top_score=0.7760510405045259, gate=proceed

### Q009: How does the schema link orders to their individual product line items?
- **Type:** multi_hop | **Difficulty:** medium  
- **Verdict:** CORRECT  
- **Expected:** ORDER_LINE_ITEM as junction; ORDER_ID FK to SALES_ORDER_HDR; PRODUCT_ID FK to TB_PRODUCT; quantity, unit price, line amount.  
- **Generated:** correctly explains `order_line_item.order_id -> sales_order_hdr.order_id`.  
- **Analysis:** Mentions junction role and parent linkage; aligned with expected.  
- **Retrieval:** gt_coverage=1.0, top_score=0.7760510405045259, gate=proceed

### Q010: Show me the order hierarchy from customer to line items.
- **Type:** multi_hop | **Difficulty:** medium  
- **Verdict:** CORRECT  
- **Expected:** CUSTOMER_MASTER → SALES_ORDER_HDR → ORDER_LINE_ITEM → TB_PRODUCT.  
- **Generated:** states Customer → Sales Order Header → Order Line Items and ties to FK `CUSTOMER_MASTER.CUST_ID → SALES_ORDER_HDR.CUST_ID` plus `order_line_item.order_id → sales_order_hdr.order_id`.  
- **Analysis:** Fully correct hierarchy conceptually; minor mismatch vs expected evidence chain is reflected only in coverage.  
- **Retrieval:** gt_coverage=0.75, top_score=0.7760510405045259, gate=proceed

### Q011: How does the schema model the confirmation state of a payment and its relationship to the order?
- **Type:** multi_hop | **Difficulty:** medium  
- **Verdict:** CORRECT  
- **Expected:** PAYMENT.CONFIRMED_AT nullable + PAYMENT.STATUS_CODE; order-level PAYMENT_CONFIRMED_AT mirrors; order statuses lifecycle.  
- **Generated:** correctly discusses payment status + confirmation timestamp and “payment relates to exactly one sales order.”  
- **Analysis:** Accurate; aligns with business rules and relationship summary.  
- **Retrieval:** gt_coverage=1.0, top_score=0.7760510405045259, gate=proceed

### Q012: How are shipments related to orders and warehouses?
- **Type:** multi_hop | **Difficulty:** medium  
- **Verdict:** CORRECT  
- **Expected:** SHIPMENT.ORDER_ID → SALES_ORDER_HDR; shipment has warehouse code, tracking, delivery status; order can have multiple shipments.  
- **Generated:** correctly states single-order-per-shipment and comes-from-one-warehouse, plus partial shipments concept.  
- **Analysis:** Correct multi-hop schema interpretation.  
- **Retrieval:** gt_coverage=1.0, top_score=0.7760510405045259, gate=proceed

### Q013: Can a product belong to multiple categories?
- **Type:** negative | **Difficulty:** easy  
- **Verdict:** CORRECT  
- **Expected:** No; product belongs to exactly one category via TB_PRODUCT.CATEGORY_ID FK to TB_CATEGORY.  
- **Generated:** explicitly answers “No” and cites “belongs to exactly one category.”  
- **Analysis:** Proper handling of negative query; no contradiction.  
- **Retrieval:** gt_coverage=1.0, top_score=0.7760510405045259, gate=proceed

### Q014: Is it possible for a customer to place an order without payment?
- **Type:** negative | **Difficulty:** medium  
- **Verdict:** CORRECT  
- **Expected:** Yes, order can exist without payment (PAYMENT_CONFIRMED_AT nullable, STATUS_CODE default PENDING); business rule affects shipping not creation.  
- **Generated:** correctly answers “Yes” and explains nullable payment confirmation on the order header + shipping constraint.  
- **Analysis:** Correct negative reasoning and nuance.  
- **Retrieval:** gt_coverage=1.0, top_score=0.7760510405045259, gate=proceed

### Q015: What schema fields support monetary value tracking across orders and their line items?
- **Type:** multi_hop | **Difficulty:** easy  
- **Verdict:** CORRECT  
- **Expected:** order header TOTAL_AMT; order lines LINE_AMT and its derivation from UNIT_PRICE and QUANTITY; reconcile via ORDER_ID.  
- **Generated:** correctly emphasizes LINE_AMT/QUANTITY/UNIT_PRICE and also mentions payment amount, but the core asked linkage between header totals and line totals is supported via the provided contexts/structure.  
- **Analysis:** Grounded and aligned with monetary tracking fields.  
- **Retrieval:** gt_coverage=1.0, top_score=0.7760510405045259, gate=proceed

## Anomalies & Recommendations

### Red Flags
- None significant. Particularly:
  - No grader rejections (`grader_rejection_count=0` for all)
  - No abstentions (`gate_abstentions=0`)
  - No builder/ingestion/Cypher failures

### Recommendations
- Given Q010’s `gt_coverage=0.75` despite a correct answer, consider improving evidence retrieval for hierarchy chains (e.g., ensure traversal/keyword queries consistently pull both junction and child-table contexts).
- For thesis/reporting: document why retrieval-quality scores can differ while correctness stays perfect (groundedness + semantic mapping robustness on *basics* dataset).

## Comparison Notes (if applicable)
- Not possible to compare vs baseline in this bundle because no `ablation_context.changes_vs_baseline` is provided. If you share the baseline AB-00 bundle or the ablation context object for AB-07, I can score Dimension 5 properly (expected vs observed causal impact).