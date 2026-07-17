# AI-Judge Evaluation: AB-10/01_basics_ecommerce
**Evaluator:** (`gpt-5.4-nano-2026-03-17`) using `docs/AI_JUDGE_PROMPT.md`  
**Date:** 2026-07-17

---

# Ablation Study Evaluation: AB-10 — 01_basics_ecommerce

## Executive Summary
AB-10 shows excellent end-to-end performance on the e-commerce “basics” dataset: builder completed all tables with no Cypher failures and the query system answered all 15 questions with grounded_rate = 1.0 and gt_coverage = 1.0. Retrieval confidence (avg_top_score ≈ 0.79) is healthy for a bge-reranker, and there are zero grader rejections and zero pipeline health anomalies, indicating stable generation and strong internal wiring between schema extraction → mapping → KG → retrieval.

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
- Triplet density looks reasonable for a small schema: `triplets_extracted=125`, `entities_resolved=62` (no sign of extraction failure; also ER didn’t destabilize the build)
- No healing/fallback triggered; builder graph construction is fully successful.

### 2. Retrieval Effectiveness (5/5)
- `grounded_rate=1.0` and `abstained_count=0` with `avg_gt_coverage=1.0`
- `avg_top_score=0.786` (strong reranker confidence for this architecture)
- `pipeline_health.questions_with_low_retrieval_score=0`
- For negative queries (Q013, Q014), the system did not abstain early; instead it produced correct content consistent with the expected “negative” semantics.

### 3. Answer Quality (5/5)
- All answers are semantically aligned with the expected answers (including schema-level relationships and business rules), and there are **no** grader rejections (`grader_rejection_count=0` across all listed questions).
- The generated answers sometimes include extra correct schema details (e.g., additional fields like timestamps), which is a positive sign rather than an error under the rubric.

**Best- and worst-case sampling (representative):**
- Best examples: Q003, Q004, Q011, Q015 — extremely precise schema relationship explanations with correct field usage.
- “Potential risk” questions: Q013 and Q014 (negative type). Both are handled correctly, with explicit “No” for multi-category membership and “Yes” for orders existing without payment confirmed, both consistent with the glossary/schema interpretation.

### 4. Pipeline Health (5/5)
- `total_grader_rejections=0`, `grader_inconsistencies=0`, `gate_abstentions=0`
- `cypher_failed=false`, `failed_mappings_count=0`, `ingestion_errors_count=0`
- The system appears fully stable for this run: no self-reflection loops were required to recover from errors.

### 5. Ablation Impact (N/A)
- Study AB-10 is not compared to a baseline bundle (no `ablation_context` provided; and `study_id` is not `AB-00`).
- Therefore, ablation impact cannot be causally evaluated per rubric.

## Per-Question Deep Dive

### Q001: What information is stored for each customer?
- **Type:** direct_mapping | **Difficulty:** easy
- **Verdict:** CORRECT
- **Expected:** Customer has unique ID, full name, email, region code, creation date, active status; email unique.
- **Generated:** Correctly identifies customer master core fields including identifier, contact details, regional reference, status, and `created_at` timestamp; includes PK semantics.
- **Analysis:** Matches expected schema content and relationships; no missing required facts observed.
- **Retrieval:** gt_coverage=1.0, top_score=0.786, gate=proceed

### Q002: How are products categorized on the platform?
- **Type:** direct_mapping | **Difficulty:** easy
- **Verdict:** CORRECT
- **Expected:** Product belongs to one category (`CATEGORY_ID`), categories support parent hierarchy.
- **Generated:** Correctly explains hierarchical `TB_CATEGORY` with `PARENT_CATEGORY_ID` and `TB_PRODUCT.CATEGORY_ID` FK.
- **Analysis:** Semantically complete; relationship and hierarchy structure both correct.
- **Retrieval:** gt_coverage=1.0, top_score=0.786, gate=proceed

### Q003: What is the relationship between customers and sales orders?
- **Type:** direct_mapping | **Difficulty:** easy
- **Verdict:** CORRECT
- **Expected:** Each sales order is placed by exactly one customer via `CUST_ID`; customer can have zero or more orders.
- **Generated:** Correctly states cardinality and FK (`sales_order_hdr.cust_id -> customer_master.cust_id`).
- **Analysis:** Accurate schema and cardinality.
- **Retrieval:** gt_coverage=1.0, top_score=0.985, gate=proceed

### Q004: What does an order line item contain?
- **Type:** direct_mapping | **Difficulty:** easy
- **Verdict:** CORRECT
- **Expected:** Product, quantity, unit price (historical), extended amount, belongs to exactly one sales order.
- **Generated:** Correctly covers quantity/unit_price and `extended amount = qty × unit_price`.
- **Analysis:** Complete and aligned.
- **Retrieval:** gt_coverage=1.0, top_score=0.979, gate=proceed

### Q005: How are payments linked to orders?
- **Type:** direct_mapping | **Difficulty:** easy
- **Verdict:** CORRECT
- **Expected:** Each payment associated with exactly one order via `ORDER_ID`; tracks method/amount/status/timestamp.
- **Generated:** Correct FK explanation and business meaning.
- **Analysis:** Correctly ties per-payment to single order.
- **Retrieval:** gt_coverage=1.0, top_score=0.921, gate=proceed

### Q006: What statuses can an order have?
- **Type:** attribute_lookup | **Difficulty:** easy
- **Verdict:** CORRECT
- **Expected:** PENDING, CONFIRMED, SHIPPED, DELIVERED, CANCELLED (CHECK constraint / glossary).
- **Generated:** Lists exactly those five statuses.
- **Analysis:** Correct enumeration.
- **Retrieval:** gt_coverage=1.0, top_score=0.700, gate=proceed

### Q007: Which table stores the product SKU information?
- **Type:** direct_mapping | **Difficulty:** easy
- **Verdict:** CORRECT
- **Expected:** `TB_PRODUCT.SKU` (and mentions product catalog fields).
- **Generated:** Correctly identifies `tb_product.sku` as SKU column.
- **Analysis:** Semantically correct.
- **Retrieval:** gt_coverage=1.0, top_score=0.984, gate=proceed

### Q008: How can I find all orders placed by a specific customer?
- **Type:** multi_hop | **Difficulty:** medium
- **Verdict:** CORRECT
- **Expected:** Filter `SALES_ORDER_HDR` by `CUST_ID` referencing `CUSTOMER_MASTER.CUST_ID`; join shows all orders.
- **Generated:** Correct join/filter logic and includes key order fields.
- **Analysis:** Correct multi-hop reasoning.
- **Retrieval:** gt_coverage=1.0, top_score=0.700, gate=proceed

### Q009: How does the schema link orders to their individual product line items?
- **Type:** multi_hop | **Difficulty:** medium
- **Verdict:** CORRECT
- **Expected:** `ORDER_LINE_ITEM` is junction with `ORDER_ID` and `PRODUCT_ID`, supports multiple line items per order.
- **Generated:** Correctly states linkage via `ORDER_LINE_ITEM` and `ORDER_ID -> SALES_ORDER_HDR`.
- **Analysis:** Correctly captures junction role for order ↔ lines.
- **Retrieval:** gt_coverage=1.0, top_score=0.700, gate=proceed

### Q010: Show me the order hierarchy from customer to line items.
- **Type:** multi_hop | **Difficulty:** medium
- **Verdict:** CORRECT
- **Expected:** Customer → SalesOrder → OrderLineItem → Product.
- **Generated:** Correctly presents customer via `SALES_ORDER_HDR.CUST_ID` and line linkage via `ORDER_LINE_ITEM.ORDER_ID`.
- **Analysis:** Correct hierarchy and parent-child structure.
- **Retrieval:** gt_coverage=1.0, top_score=0.700, gate=proceed

### Q011: How does the schema model the confirmation state of a payment and its relationship to the order?
- **Type:** multi_hop | **Difficulty:** medium
- **Verdict:** CORRECT
- **Expected:** Payment confirmation via `PAYMENT.CONFIRMED_AT` and `PAYMENT.STATUS_CODE`; also mirrors at order level with `SALES_ORDER_HDR.PAYMENT_CONFIRMED_AT`; order lifecycle statuses.
- **Generated:** Correctly explains both payment-level and order-level confirmation timestamps and linkage.
- **Analysis:** Complete and consistent.
- **Retrieval:** gt_coverage=1.0, top_score=0.700, gate=proceed

### Q012: How are shipments related to orders and warehouses?
- **Type:** multi_hop | **Difficulty:** medium
- **Verdict:** CORRECT
- **Expected:** Shipment belongs to one order; includes source warehouse and tracking/status.
- **Generated:** Correctly states shipment ↔ sales order cardinality and shipment ↔ warehouse “comes from exactly one warehouse”.
- **Analysis:** Correct relationships.
- **Retrieval:** gt_coverage=1.0, top_score=0.924, gate=proceed

### Q013: Can a product belong to multiple categories?
- **Type:** negative | **Difficulty:** easy
- **Verdict:** CORRECT
- **Expected:** No; each product has exactly one category via `TB_PRODUCT.CATEGORY_ID` FK.
- **Generated:** “No” and correctly cites “belongs to exactly one Category” and single FK.
- **Analysis:** Correct negative handling; no contradiction.
- **Retrieval:** gt_coverage=1.0, top_score=0.700, gate=proceed

### Q014: Is it possible for a customer to place an order without payment?
- **Type:** negative | **Difficulty:** medium
- **Verdict:** CORRECT
- **Expected:** Yes, orders can exist with `PAYMENT_CONFIRMED_AT` NULL; business rule constrains shipping, not order existence.
- **Generated:** “Yes” and explains `PAYMENT_CONFIRMED_AT` nullable and rule about shipping only after confirmation.
- **Analysis:** Correct interpretation of “possible” vs “shipped”.
- **Retrieval:** gt_coverage=1.0, top_score=0.700, gate=proceed

### Q015: What schema fields support monetary value tracking across orders and their line items?
- **Type:** multi_hop | **Difficulty:** easy
- **Verdict:** CORRECT
- **Expected:** `SALES_ORDER_HDR.TOTAL_AMT`, `ORDER_LINE_ITEM.UNIT_PRICE`, `QUANTITY`, `LINE_AMT`, reconciliation via `ORDER_ID` link; also payment amount fields.
- **Generated:** Correctly explains line-level `LINE_AMT` composition and links via `ORDER_ID`; also correctly describes payment `AMOUNT` and `CONFIRMED_AT`.
- **Analysis:** Complete schema-field coverage.
- **Retrieval:** gt_coverage=1.0, top_score=0.700, gate=proceed

## Anomalies & Recommendations

### Red Flags
- None observed. Key pipeline safety indicators are clean:
  - `cypher_failed=false`, `ingestion_errors=[]`
  - `total_grader_rejections=0`, `grader_inconsistencies=0`
  - `gt_coverage=1.0` and `grounded_rate=1.0` across all 15 questions

### Recommendations
- Since AB-10 is clean, improvements should focus on **robustness beyond “basics”**:
  - Run the same ablation with `dataset_info.complexity = advanced/edgecases` to stress entity resolution, traversal retrieval, and negative-query abstention behavior.
  - Track whether the system continues to avoid false positives for negative questions when gt_coverage drops.

## Comparison Notes (if applicable)
- No baseline comparison bundle (`AB-00`) or `ablation_context` was provided, so causal “vs baseline” claims are not possible here.