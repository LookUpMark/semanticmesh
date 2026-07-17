# AI-Judge Evaluation: AB-08/01_basics_ecommerce
**Evaluator:** (`gpt-5.4-nano-2026-03-17`) using `docs/AI_JUDGE_PROMPT.md`  
**Date:** 2026-07-17

---

# Ablation Study Evaluation: AB-08 — 01_basics_ecommerce

## Executive Summary
AB-08 shows a **highly successful** end-to-end run on the E-Commerce basics dataset: the builder completed all tables with no Cypher failures or ingestion errors, and the query system achieved **15/15 grounded answers** with strong retrieval quality (avg_top_score ≈ **0.777**). There are no pipeline health issues (0 grader rejections, 0 abstentions), and across the provided samples the generated answers are semantically aligned with the expected schema/business constraints.

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
- Triplet extraction/ER scale appears healthy: `triplets_extracted=102`, `entities_resolved=68` (no sign of under-extraction or ER collapse).
**Conclusion:** The builder pipeline is functioning correctly and fully completed.

### 2. Retrieval Effectiveness (5/5)
- `grounded_rate=1.0` and `avg_gt_coverage=0.9167`
- `avg_top_score=0.7771` (consistent with a strong cross-encoder reranker confidence)
- `abstained_count=0` and `gate_abstentions=0`, with no evidence of false abstention on solvable questions.
- Per-question examples (e.g., Q003 and Q004) show strong raw retrieval confidence; even the lower retrieval-quality-looking case (e.g., Q006 has retrieval_quality_score_raw=0.55) still answered correctly and stayed grounded.

### 3. Answer Quality (5/5)
- `grounded_count=15` and `grounded=true` for all listed questions.
- Semantic checks on representative cases:
  - **Direct mapping correctness:** Q001–Q007 all correctly describe the schema/business rules (e.g., customer fields, category hierarchy, SKU storage, line item contents).
  - **Multi-hop correctness:** Q008–Q012 correctly explain joins/hierarchy traversal (customer→orders, orders→lines→products, shipments↔orders↔warehouse).
  - **Negative questions:** Q013 (negative) correctly answers “No” using “belongs to exactly one Category,” and Q014 correctly answers “Yes” with the nullable confirmation fields and the shipping constraint (“cannot be shipped until payment is confirmed”).
- No hallucination indicators: `grader_rejection_count=0` across the bundle.

### 4. Pipeline Health (5/5)
- `total_grader_rejections=0`, `grader_inconsistencies=0`
- `gate_abstentions=0`
- `cypher_failed=false`, `failed_mappings_count=0`, `ingestion_errors_count=0`
- No self-healing behavior is triggered, but that’s consistent with a stable run rather than failure.

### 5. Ablation Impact (N/A)
- The bundle is AB-08, but **no `ablation_context`** is provided in the input to specify changes vs baseline (AB-00) or an expected causal hypothesis. Therefore this dimension cannot be scored per rubric.

## Per-Question Deep Dive

### Q001: What information is stored for each customer?
- **Type:** direct_mapping | **Difficulty:** easy
- **Verdict:** CORRECT
- **Expected:** customer fields: unique ID, full name, unique email, region code, creation date, active status; email unique
- **Generated:** describes customer_master core fields (CUST_ID, full name, contact, region, created_at, active flag); grounded in retrieved context
- **Analysis:** Matches the schema/business concept content; does not introduce incorrect facts.
- **Retrieval:** gt_coverage=1.0, top_score=0.7771 (pool reported 0.7), gate=proceed

### Q002: How are products categorized on the platform?
- **Type:** direct_mapping | **Difficulty:** easy
- **Verdict:** CORRECT
- **Expected:** each product references exactly one category; categories can have parent category hierarchy
- **Generated:** accurately explains TB_PRODUCT.category_id FK to TB_CATEGORY and parent_category_id self-reference
- **Analysis:** Schema-level explanation aligns with expected hierarchy model.
- **Retrieval:** gt_coverage=1.0, top_score=0.7 (raw 0.55), gate=proceed

### Q003: What is the relationship between customers and sales orders?
- **Type:** direct_mapping | **Difficulty:** easy
- **Verdict:** CORRECT
- **Expected:** each order placed by exactly one customer (CUST_ID FK); customers can have zero or more orders
- **Generated:** states one-to-many and references FK sales_order_hdr.cust_id -> customer_master.cust_id
- **Analysis:** Correct relationship semantics.
- **Retrieval:** gt_coverage=1.0, top_score≈0.9847, gate=proceed

### Q004: What does an order line item contain?
- **Type:** direct_mapping | **Difficulty:** easy
- **Verdict:** CORRECT
- **Expected:** product, quantity, unit price at purchase time, extended amount; belongs to one sales order
- **Generated:** correctly lists product, quantity, unit_price, line amount; associates to sales order
- **Analysis:** Fully aligned.
- **Retrieval:** gt_coverage=1.0, top_score≈0.9821, gate=proceed

### Q005: How are payments linked to orders?
- **Type:** direct_mapping | **Difficulty:** easy
- **Verdict:** CORRECT
- **Expected:** each payment associated with exactly one sales order via ORDER_ID FK; tracks method/amount/status/confirmation
- **Generated:** accurately states “references exactly one sales order” and FK payment.order_id -> sales_order_hdr.order_id
- **Analysis:** Correct.
- **Retrieval:** gt_coverage=1.0, top_score≈0.9091, gate=proceed

### Q006: What statuses can an order have?
- **Type:** attribute_lookup | **Difficulty:** easy
- **Verdict:** CORRECT
- **Expected:** five statuses: PENDING, CONFIRMED, SHIPPED, DELIVERED, CANCELLED
- **Generated:** lists exactly those five
- **Analysis:** Matches expected enumeration.
- **Retrieval:** gt_coverage=1.0, top_score=0.7 (raw 0.55), gate=proceed

### Q007: Which table stores the product SKU information?
- **Type:** direct_mapping | **Difficulty:** easy
- **Verdict:** CORRECT
- **Expected:** TB_PRODUCT stores SKU and other product attributes
- **Generated:** identifies tb_product.sku (SKU field)
- **Analysis:** Correct mapping to physical table/attribute.
- **Retrieval:** gt_coverage=1.0, top_score≈0.9891, gate=proceed

### Q008: How can I find all orders placed by a specific customer?
- **Type:** multi_hop | **Difficulty:** medium
- **Verdict:** CORRECT
- **Expected:** filter SALES_ORDER_HDR by CUST_ID; join to CUSTOMER_MASTER on CUST_ID to retrieve customer orders
- **Generated:** correct FK-based filtering logic and key order fields
- **Analysis:** Correct multi-hop reasoning.
- **Retrieval:** gt_coverage=1.0, top_score=0.7 (raw 0.55), gate=proceed

### Q009: How does the schema link orders to their individual product line items?
- **Type:** multi_hop | **Difficulty:** medium
- **Verdict:** CORRECT
- **Expected:** ORDER_LINE_ITEM is junction between SALES_ORDER_HDR and TB_PRODUCT; includes ORDER_ID, PRODUCT_ID, quantity>0, UNIT_PRICE, LINE_AMT
- **Generated:** correct join path via order_line_item.order_id -> sales_order_hdr.order_id and order_line_item.product_id -> tb_product.product_id
- **Analysis:** Semantically matches; no contradictions seen.
- **Retrieval:** gt_coverage=1.0, top_score=0.7 (raw 0.5819), gate=proceed

### Q010: Show me the order hierarchy from customer to line items.
- **Type:** multi_hop | **Difficulty:** medium
- **Verdict:** CORRECT
- **Expected:** Customer → SalesOrder → OrderLineItem → Product
- **Generated:** matches the hierarchy and relationship logic to order_line_item
- **Analysis:** Correct and adequately grounded.
- **Retrieval:** gt_coverage=0.75, top_score=0.7, gate=proceed

### Q011: How does the schema model the confirmation state of a payment and its relationship to the order?
- **Type:** multi_hop | **Difficulty:** medium
- **Verdict:** CORRECT
- **Expected:** PAYMENT.CONFIRMED_AT nullable; PAYMENT.STATUS_CODE constrained; SALES_ORDER_HDR.PAYMENT_CONFIRMED_AT mirrors; order STATUS_CODE lifecycle
- **Generated:** correctly discusses confirmed timestamp at Payment level and payment_confirmed_at at order level; relationship to shipping constraint
- **Analysis:** Correct modeling of confirmation at both levels.
- **Retrieval:** gt_coverage=1.0, top_score=0.7 (raw 0.55), gate=proceed

### Q012: How are shipments related to orders and warehouses?
- **Type:** multi_hop | **Difficulty:** medium
- **Verdict:** CORRECT
- **Expected:** Shipment references one sales order; includes source warehouse and tracking/status
- **Generated:** correctly states one-to-many from order to shipments; mentions shipment table fields and warehouse/timing/tracking semantics
- **Analysis:** Correct.
- **Retrieval:** gt_coverage=1.0, top_score≈0.7917, gate=proceed

### Q013: Can a product belong to multiple categories?
- **Type:** negative | **Difficulty:** easy
- **Verdict:** CORRECTLY_ABSTAINED? → **(Not abstained)** but **CORRECT**
- **Expected:** No; each product belongs to exactly one category (FK category_id)
- **Generated:** answers “No” and supports via “belongs to exactly one Category” and FK category_id -> tb_category
- **Analysis:** Correct handling of negative question (returns explicit “No,” not a fabricated positive).
- **Retrieval:** gt_coverage=1.0, top_score=0.7 (raw 0.55), gate=proceed

### Q014: Is it possible for a customer to place an order without payment?
- **Type:** negative | **Difficulty:** medium
- **Verdict:** CORRECT
- **Expected:** Yes—order can exist before payment confirmation; PAYMENT_CONFIRMED_AT nullable and status lifecycle; shipping requires confirmation
- **Generated:** answers “Yes” and references PAYMENT_CONFIRMED_AT nullable and shipping/payment constraint
- **Analysis:** Correct negative-question interpretation.
- **Retrieval:** gt_coverage=0.0 (note), top_score=0.7 (raw 0.55), gate=proceed  
  *Comment:* Even with reported `gt_coverage=0.0`, the answer remains consistent with the provided contexts and expected reasoning; this suggests GT-source coverage labeling may be incomplete rather than retrieval truly failing.

### Q015: What schema fields support monetary value tracking across orders and their line items?
- **Type:** multi_hop | **Difficulty:** easy
- **Verdict:** CORRECT
- **Expected:** ORDER header: TOTAL_AMT; line item: QUANTITY, UNIT_PRICE, LINE_AMT (= quantity×unit_price); linked via ORDER_ID FK
- **Generated:** correctly details LINE_AMT composition and mentions payment.amount as settlement field (in addition to expected)
- **Analysis:** Includes extra correct info (payment amount) without contradicting expected requirements.
- **Retrieval:** gt_coverage=1.0, top_score=0.7 (raw 0.55), gate=proceed

## Anomalies & Recommendations

### Red Flags
- **Q014 reports `gt_coverage=0.0`** while still being correct and grounded. This indicates a **possible annotation/ground-truth source mapping mismatch** rather than retrieval failure.
- Many questions show `retrieval_quality_score_raw=0.55` with adjusted score clamped to 0.7 due to the pool confidence floor—this can mask weaker raw retrieval on some queries, though correctness remained perfect in this run.

### Recommendations
- Re-check the **GT source coverage labeling** pipeline for negative questions (especially Q014) to ensure `gt_coverage` aligns with how “expected_sources” are defined.
- Add a report that separately flags cases where:
  - `gt_coverage=0` but `grounded=true`, and
  - generated answer is correct,
  to distinguish “retrieval actually missing GT sources” from “GT source bookkeeping mismatch.”

## Comparison Notes (if applicable)
- No baseline comparison (AB-00 or `ablation_context`) was provided, so a causal comparison cannot be made. However, the run itself is consistent with an “optimal/near-perfect” configuration on the basics dataset: complete builder ingestion/mapping and fully accurate query answering without hallucination rejections or abstentions.