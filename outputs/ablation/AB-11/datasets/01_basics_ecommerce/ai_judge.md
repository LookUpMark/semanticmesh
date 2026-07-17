# AI-Judge Evaluation: AB-11/01_basics_ecommerce
**Evaluator:** (`gpt-5.4-nano-2026-03-17`) using `docs/AI_JUDGE_PROMPT.md`  
**Date:** 2026-07-17

---

# Ablation Study Evaluation: AB-11 — 01_basics_ecommerce

## Executive Summary
For this **AB-11** run on the **e-commerce basics** dataset, the pipeline is highly functional: **all 7 builder tables completed successfully with no Cypher failures or ingestion errors**, and **all 15/15 queries were answered while remaining fully grounded**. Retrieval appears consistently effective (high avg GT coverage and strong reranker confidence), though one query shows a borderline low retrieval raw score pattern (consistent with a small “extra context” effect rather than a true miss). Overall, AB-11 demonstrates a **stable and correct end-to-end Builder → GraphRAG Query** behavior.

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
- `failed_mappings=[]`, `ingestion_errors=[]`
- Triplet extraction is substantial: `triplets_extracted=98` across `entities_resolved=62` (triplets/entity ≈ 1.58). For **basics**, this is acceptable given mapping correctness and zero downstream failures; the key outcome is that **the KG was built without error**.

### 2. Retrieval Effectiveness (5/5)
- `grounded_rate=1.0` with `avg_gt_coverage=0.9833` (very high)
- `avg_top_score=0.7843` (healthy for cross-encoder reranker; comfortably above the “healthy range” noted in rubric)
- No abstentions: `abstained_count=0` and `gate_abstentions=0` — consistent with “ground-truth available in KG” for basics.
- No questions with low retrieval: `pipeline_health.questions_with_low_retrieval_score=0`.

### 3. Answer Quality (5/5)
- `grounded_count=15` out of 15 and **every answer is semantically aligned with expected content**.
- Representative checks:
  - Q001 correctly enumerates customer fields (and notes account status semantics caveat appropriately).
  - Q002 correctly explains category hierarchy via `PARENT_CATEGORY_ID`.
  - Multi-hop examples (Q008–Q012, Q015) properly describe foreign-key traversal logic and schema relationships.
  - Negative questions:
    - Q013 (“Can a product belong to multiple categories?”) correctly answers **No**.
    - Q014 (“Is it possible for a customer to place an order without payment?”) correctly answers **Yes**, and correctly focuses on *order creation vs shipping/payment confirmation constraint*.
- `grader_rejection_count=1` overall in `pipeline_health`, which indicates the Self-RAG/Hallucination grading caught at least one issue during generation, but the system still reached correct grounded outputs with no instability.

### 4. Pipeline Health (5/5)
- `cypher_failed=false`, `failed_mappings_count=0`, `ingestion_errors_count=0`
- `grader_inconsistencies=0`
- `gate_abstentions=0` (no misfires leading to abstention)
- Only `total_grader_rejections=1`, and per-question grader consistency is valid across shown items (`grader_consistency_valid=true`).

### 5. Ablation Impact (N/A)
- The rubric specifies to use this dimension only if baseline identification is available (e.g., `AB-00`) or if `ablation_context` is provided. The bundle includes `study_id=AB-11`, but **no baseline diff context (`changes_vs_baseline`, `expected_impact`)** is present, so this dimension is **not scored**.

## Per-Question Deep Dive

### Q001: What information is stored for each customer?
- **Type:** direct_mapping | **Difficulty:** easy  
- **Verdict:** CORRECT  
- **Expected:** unique customer ID, full name, email (unique), region code, created date, active status  
- **Generated:** core customer info via `customer_master`, includes PK `CUST_ID`, `region_code`, and “account status” (with note on unclear value meanings)  
- **Analysis:** Correctly identifies the customer master attributes; minor wording/semantic granularity issue (“account status” meaning not enumerated) does not break correctness.  
- **Retrieval:** gt_coverage=1.0, top_score=0.7843, gate=proceed  

### Q002: How are products categorized on the platform?
- **Type:** direct_mapping | **Difficulty:** easy  
- **Verdict:** CORRECT  
- **Expected:** hierarchical category tree; product references exactly one category via `CATEGORY_ID`  
- **Generated:** `TB_CATEGORY` with `PARENT_CATEGORY_ID` and `TB_PRODUCT.CATEGORY_ID` FK  
- **Analysis:** Fully matches expected hierarchy + single-category membership.  
- **Retrieval:** gt_coverage=1.0, top_score=0.7, gate=proceed  

### Q003: What is the relationship between customers and sales orders?
- **Type:** direct_mapping | **Difficulty:** easy  
- **Verdict:** CORRECT  
- **Expected:** each order belongs to exactly one customer; customer has zero or more orders  
- **Generated:** many-to-one (customer→orders), order linked via `sales_order_hdr.cust_id -> customer_master.cust_id`  
- **Analysis:** Directly correct relational cardinality and key linkage.  
- **Retrieval:** gt_coverage=1.0, top_score=0.9847, gate=proceed  

### Q004: What does an order line item contain?
- **Type:** direct_mapping | **Difficulty:** easy  
- **Verdict:** CORRECT  
- **Expected:** product, quantity, unit price at purchase time, extended amount; belongs to one sales order  
- **Generated:** includes product, quantity, unit price, extended line amount; references `order_line_item`  
- **Analysis:** Correct schema semantics and content.  
- **Retrieval:** gt_coverage=1.0, top_score=0.9574, gate=proceed  

### Q005: How are payments linked to orders?
- **Type:** direct_mapping | **Difficulty:** easy  
- **Verdict:** CORRECT  
- **Expected:** one payment belongs to exactly one sales order via `ORDER_ID`  
- **Generated:** `payment.order_id -> sales_order_hdr.order_id`, plus business concept “one order has one or more payments”  
- **Analysis:** Correct FK linkage + cardinality.  
- **Retrieval:** gt_coverage=1.0, top_score=0.9548, gate=proceed  

### Q006: What statuses can an order have?
- **Type:** attribute_lookup | **Difficulty:** easy  
- **Verdict:** CORRECT  
- **Expected:** PENDING, CONFIRMED, SHIPPED, DELIVERED, CANCELLED  
- **Generated:** exactly those five statuses  
- **Analysis:** Matches glossary lifecycle and status constraint.  
- **Retrieval:** gt_coverage=1.0, top_score=0.7, gate=proceed  

### Q007: Which table stores the product SKU information?
- **Type:** direct_mapping | **Difficulty:** easy  
- **Verdict:** CORRECT  
- **Expected:** `TB_PRODUCT` stores SKU code  
- **Generated:** `tb_product.sku` / “Unique SKU code” in PRODUCT concept  
- **Analysis:** Correct table/attribute mapping.  
- **Retrieval:** gt_coverage=1.0, top_score=0.9822, gate=proceed  

### Q008: How can I find all orders placed by a specific customer?
- **Type:** multi_hop | **Difficulty:** medium  
- **Verdict:** CORRECT  
- **Expected:** filter `SALES_ORDER_HDR` by `CUST_ID`; join on CUST_ID to CUSTOMER_MASTER for details  
- **Generated:** describes filtering `SALES_ORDER_HDR.CUST_ID` and FK join to `CUSTOMER_MASTER.CUST_ID` and includes key order fields  
- **Analysis:** Correct multi-hop join logic and attribute mentions.  
- **Retrieval:** gt_coverage=1.0, top_score=0.7, gate=proceed  

### Q009: How does the schema link orders to their individual product line items?
- **Type:** multi_hop | **Difficulty:** medium  
- **Verdict:** CORRECT  
- **Expected:** `ORDER_LINE_ITEM` links `SALES_ORDER_HDR` and `TB_PRODUCT` via ORDER_ID and PRODUCT_ID; includes QUANTITY, UNIT_PRICE, LINE_AMT  
- **Generated:** explains join via `ORDER_LINE_ITEM.order_id -> SALES_ORDER_HDR.order_id` and `product_id -> TB_PRODUCT.product_id` and mentions line fields implicitly  
- **Analysis:** Correct relationship and junction-table semantics.  
- **Retrieval:** gt_coverage=1.0, top_score=0.7, gate=proceed  

### Q010: Show me the order hierarchy from customer to line items.
- **Type:** multi_hop | **Difficulty:** medium  
- **Verdict:** CORRECT  
- **Expected:** Customer → SalesOrder → OrderLineItem → Product  
- **Generated:** describes Customer→SalesOrder Header→Order Line Items; FK logic for order/lines  
- **Analysis:** Correct hierarchy framing (minor: doesn’t explicitly enumerate Product in the short hierarchy statement, but FK evidence and contexts support Product linkage).  
- **Retrieval:** gt_coverage=0.75, top_score=0.7, gate=proceed  

### Q011: How does the schema model the confirmation state of a payment and its relationship to the order?
- **Type:** multi_hop | **Difficulty:** medium  
- **Verdict:** CORRECT  
- **Expected:** `PAYMENT.CONFIRMED_AT` nullable + `PAYMENT.STATUS_CODE` lifecycle; order-level `SALES_ORDER_HDR.PAYMENT_CONFIRMED_AT` mirrors; order status lifecycle via CHECK  
- **Generated:** correctly explains both payment-level and order-level timestamps/statuses; payment linked to order via FK  
- **Analysis:** Proper confirmation modeling and relationship description.  
- **Retrieval:** gt_coverage=1.0, top_score=0.7, gate=proceed  

### Q012: How are shipments related to orders and warehouses?
- **Type:** multi_hop | **Difficulty:** medium  
- **Verdict:** CORRECT  
- **Expected:** shipment references one order; shipment specifies source warehouse + tracking/status/delivery  
- **Generated:** correctly states shipment→order cardinality and “comes from exactly one warehouse”  
- **Analysis:** Multi-hop relationship is accurate; warehouse and customer delivery logic covered.  
- **Retrieval:** gt_coverage=1.0, top_score=0.8860, gate=proceed  

### Q013: Can a product belong to multiple categories?
- **Type:** negative | **Difficulty:** easy  
- **Verdict:** CORRECT  
- **Expected:** No; product belongs to exactly one category (`TB_PRODUCT.CATEGORY_ID` FK)  
- **Generated:** “No” grounded in business rule “belongs to exactly one Category”  
- **Analysis:** Correct negative handling (no invented counterfactuals).  
- **Retrieval:** gt_coverage=1.0, top_score=0.7, gate=proceed  

### Q014: Is it possible for a customer to place an order without payment?
- **Type:** negative | **Difficulty:** medium  
- **Verdict:** CORRECT  
- **Expected:** Yes; order can exist with nullable `PAYMENT_CONFIRMED_AT` / payment not yet confirmed, but shipping is blocked until payment confirmed  
- **Generated:** correctly distinguishes order existence vs shipping constraint; uses nullable `PAYMENT_CONFIRMED_AT` as basis  
- **Analysis:** Correctly answers negative question with nuanced schema-grounded reasoning.  
- **Retrieval:** gt_coverage=1.0, top_score=0.7, gate=proceed  

### Q015: What schema fields support monetary value tracking across orders and their line items?
- **Type:** multi_hop | **Difficulty:** easy  
- **Verdict:** CORRECT  
- **Expected:** order-level `TOTAL_AMT` in `SALES_ORDER_HDR`; line-level `UNIT_PRICE`, `QUANTITY`, `LINE_AMT=QUANTITY×UNIT_PRICE`; FK via ORDER_ID  
- **Generated:** correctly explains `ORDER_LINE_ITEM` monetary fields; notes that order-level exact column name wasn’t retrieved (does not hallucinate)  
- **Analysis:** This is strong behavior: it **doesn’t invent the missing header column name** and stays grounded.  
- **Retrieval:** gt_coverage=1.0, top_score=0.7, gate=proceed  

## Anomalies & Recommendations

### Red Flags
- **None major.** All answers are grounded and correct; no Cypher/ingestion/mapping failures.
- Minor signal: Q010 has lower `gt_coverage=0.75` even though the answer is correct. This likely reflects **coverage scoring sensitivity** (not a correctness issue).

### Recommendations
- For better schema-field naming fidelity (e.g., Q015): ensure retrieval surfaces the **exact `SALES_ORDER_HDR` column name** for totals (`TOTAL_AMT`) more reliably, possibly by:
  - increasing graph traversal contribution when questions ask for “fields” (schema-level precision),
  - tightening context distillation caps if they ever truncate key dictionary snippets (here it still worked, but naming precision could improve).

## Comparison Notes (if applicable)
- No baseline (`AB-00`) diff context is provided in the bundle, so no direct “vs baseline” comparison is possible.