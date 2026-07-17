# AI-Judge Evaluation: AB-16/01_basics_ecommerce
**Evaluator:** (`gpt-5.4-nano-2026-03-17`) using `docs/AI_JUDGE_PROMPT.md`  
**Date:** 2026-07-17

---

# Ablation Study Evaluation: AB-16 — 01_basics_ecommerce

## Executive Summary
This run shows an excellent end-to-end system behavior on the “basics” e-commerce dataset: all 7 tables were completed with no Cypher failures, retrieval consistently covered ground-truth sources (avg `gt_coverage`≈0.98, grounded_rate=1.0), and there were zero grader rejections or pipeline instabilities. The only notable concern is semantic/context precision around a potential schema mismatch in **Q011** (payment `STATUS` vs `STATUS_CODE`)—however it did not trigger hallucination rejection in the provided logs.

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
- Triplet extraction density looks healthy in aggregate (`triplets_extracted=106` across 7 tables).
**Conclusion:** Builder graph construction was fully successful with no recoveries needed.

### 2. Retrieval Effectiveness (5/5)
- `grounded_rate=1.0` and `abstained_count=0`
- `avg_gt_coverage=0.9833` (very high)
- `avg_top_score=0.7879` (strong reranker confidence)
- `pipeline_health.questions_with_low_retrieval_score=0`
**Conclusion:** Retrieval and context selection reliably brought in the ground-truth supporting sources for every question.

### 3. Answer Quality (5/5)
- All 15 answers are marked grounded: `grounded_count=15`, `grounded_rate=1.0`
- For representative questions:
  - **Q001** correctly enumerates customer fields (ID, full name, email, region code, created at, active flag) and notes email uniqueness.
  - **Q002–Q007** correctly describe category hierarchy, order/customer relationship, line-item composition, payment linking, order statuses, and SKU storage.
  - **Negative questions**:
    - **Q013** correctly answers “No” for product belonging to multiple categories.
    - **Q014** answers “Yes” that an order can exist without payment confirmation, reasoning from `PAYMENT_CONFIRMED_AT` being nullable and linking shipping constraints at a business-rule level.
- There are **zero grader rejections** (`grader_rejection_count=0` for all shown questions).
**Conclusion:** Semantically, answers align with expected facts and handle negative queries correctly.

### 4. Pipeline Health (5/5)
- `total_grader_rejections=0`
- `grader_inconsistencies=0`
- `gate_abstentions=0`
- `cypher_failed=false`, `failed_mappings_count=0`, `ingestion_errors_count=0`
**Conclusion:** No instability indicators; self-checks did not find hallucinations or contradictions.

### 5. Ablation Impact (N/A)
- Study is **AB-16**, but the bundle does not include explicit “changes_vs_baseline” or an ablation context field describing what differs from AB-00.
- Therefore ablation impact cannot be causally evaluated per rubric.

## Per-Question Deep Dive

### Q001: What information is stored for each customer?
- **Type:** direct_mapping | **Difficulty:** easy  
- **Verdict:** CORRECT  
- **Expected:** customer ID, full name, email (unique), region code, creation date, active status  
- **Generated:** lists `CUST_ID`, `FULL_NAME`, `EMAIL`, `REGION_CODE`, `CREATED_AT`, `IS_ACTIVE` and notes `EMAIL` uniqueness  
- **Analysis:** Correct field enumeration and uniqueness point; grounded in retrieved `CUSTOMER_MASTER`/schema contexts.  
- **Retrieval:** gt_coverage=1.0, top_score=0.7205, gate=proceed

### Q002: How are products categorized on the platform?
- **Type:** direct_mapping | **Difficulty:** easy  
- **Verdict:** CORRECT  
- **Expected:** product → exactly one category via `CATEGORY_ID`; categories support hierarchy via `PARENT_CATEGORY_ID`  
- **Generated:** matches FK and parent-child category structure  
- **Analysis:** Fully consistent with glossary + data dictionary contexts.  
- **Retrieval:** gt_coverage=1.0, top_score=0.7, gate=proceed

### Q003: What is the relationship between customers and sales orders?
- **Type:** direct_mapping | **Difficulty:** easy  
- **Verdict:** CORRECT  
- **Expected:** orders placed by exactly one customer; customer can have many orders  
- **Generated:** “zero or more orders” and FK `SALES_ORDER_HDR.CUST_ID -> CUSTOMER_MASTER.CUST_ID`  
- **Analysis:** Correct one-to-many relationship and FK grounding.  
- **Retrieval:** gt_coverage=1.0, top_score=0.9847, gate=proceed

### Q004: What does an order line item contain?
- **Type:** direct_mapping | **Difficulty:** easy  
- **Verdict:** CORRECT  
- **Expected:** product, quantity, unit price at purchase time, extended amount; line belongs to exactly one order  
- **Generated:** describes product, quantity, unit price, and includes `LINE_AMT`; mentions line belongs to sales order  
- **Analysis:** Correct and complete.  
- **Retrieval:** gt_coverage=1.0, top_score=0.9872, gate=proceed

### Q005: How are payments linked to orders?
- **Type:** direct_mapping | **Difficulty:** easy  
- **Verdict:** CORRECT  
- **Expected:** each payment linked to exactly one order via `PAYMENT.ORDER_ID -> SALES_ORDER_HDR.ORDER_ID` and includes method/amount/status/timestamps  
- **Generated:** matches FK and “for exactly one sales order”; aligns with business rules  
- **Analysis:** Correct FK-based linkage.  
- **Retrieval:** gt_coverage=1.0, top_score=0.9501, gate=proceed

### Q006: What statuses can an order have?
- **Type:** attribute_lookup | **Difficulty:** easy  
- **Verdict:** CORRECT  
- **Expected:** PENDING, CONFIRMED, SHIPPED, DELIVERED, CANCELLED  
- **Generated:** lists exactly those statuses via `SALES_ORDER_HDR.STATUS_CODE`  
- **Analysis:** Correct enumeration.  
- **Retrieval:** gt_coverage=1.0, top_score=0.7, gate=proceed

### Q007: Which table stores the product SKU information?
- **Type:** direct_mapping | **Difficulty:** easy  
- **Verdict:** CORRECT  
- **Expected:** `TB_PRODUCT` stores SKU (and other product fields)  
- **Generated:** states `TB_PRODUCT.SKU`  
- **Analysis:** Correct column/table identification.  
- **Retrieval:** gt_coverage=1.0, top_score=0.9747, gate=proceed

### Q008: How can I find all orders placed by a specific customer?
- **Type:** multi_hop | **Difficulty:** medium  
- **Verdict:** CORRECT  
- **Expected:** filter `SALES_ORDER_HDR` by `CUST_ID`; join on `CUSTOMER_MASTER.CUST_ID`  
- **Generated:** explains filtering `SALES_ORDER_HDR.CUST_ID` and selecting order fields  
- **Analysis:** Matches expected join logic.  
- **Retrieval:** gt_coverage=1.0, top_score=0.7, gate=proceed

### Q009: How does the schema link orders to their individual product line items?
- **Type:** multi_hop | **Difficulty:** medium  
- **Verdict:** CORRECT  
- **Expected:** `ORDER_LINE_ITEM` as junction; `ORDER_ID` FK to order header and `PRODUCT_ID` FK to product; includes quantity/unit price/line amount  
- **Generated:** correctly states linkage via `ORDER_LINE_ITEM.ORDER_ID -> SALES_ORDER_HDR(ORDER_ID)` and `ORDER_LINE_ITEM.PRODUCT_ID -> TB_PRODUCT(PRODUCT_ID)`  
- **Analysis:** Correct junction modeling.  
- **Retrieval:** gt_coverage=1.0, top_score=0.7, gate=proceed

### Q010: Show me the order hierarchy from customer to line items.
- **Type:** multi_hop | **Difficulty:** medium  
- **Verdict:** CORRECT  
- **Expected:** CUSTOMER → SalesOrder → OrderLineItem → Product  
- **Generated:** describes traversal and required foreign keys (`CUST_ID`, then `ORDER_ID`)  
- **Analysis:** Correct hierarchy and join path explanation.  
- **Retrieval:** gt_coverage=0.75, top_score=0.7, gate=proceed

### Q011: How does the schema model the confirmation state of a payment and its relationship to the order?
- **Type:** multi_hop | **Difficulty:** medium  
- **Verdict:** CORRECT  
- **Expected:** `PAYMENT.CONFIRMED_AT` + `PAYMENT.STATUS_CODE`; order-level `SALES_ORDER_HDR.PAYMENT_CONFIRMED_AT`; order lifecycle/status_code constraints  
- **Generated:** uses `PAYMENT.CONFIRMED_AT` and ties via `PAYMENT.ORDER_ID`; also references `SALES_ORDER_HDR.PAYMENT_CONFIRMED_AT`  
- **Analysis:** Minor naming slip risk: generated text says `PAYMENT.STATUS` while schema contexts show `PAYMENT.STATUS_CODE`, but the answer still captures the correct modeling intent; no hallucination rejection occurred.  
- **Retrieval:** gt_coverage=1.0, top_score=0.7, gate=proceed

### Q012: How are shipments related to orders and warehouses?
- **Type:** multi_hop | **Difficulty:** medium  
- **Verdict:** CORRECT  
- **Expected:** `SHIPMENT.ORDER_ID -> SALES_ORDER_HDR`; shipment includes warehouse code and tracking/status  
- **Generated:** matches `SHIPMENT.ORDER_ID` linkage and `SHIPMENT.WAREHOUSE_CODE` and delivery logistics context  
- **Analysis:** Correct relationship and attributes.  
- **Retrieval:** gt_coverage=1.0, top_score=0.9012, gate=proceed

### Q013: Can a product belong to multiple categories?
- **Type:** negative | **Difficulty:** easy  
- **Verdict:** CORRECTLY_ABSTAINED (effectively correct negative response)  
- **Expected:** No; product belongs to exactly one category via `TB_PRODUCT.CATEGORY_ID`  
- **Generated:** “No” with glossary + FK justification  
- **Analysis:** Correct handling of negative constraint; not an abstention, but a correct negative answer.  
- **Retrieval:** gt_coverage=1.0, top_score=0.7, gate=proceed

### Q014: Is it possible for a customer to place an order without payment?
- **Type:** negative | **Difficulty:** medium  
- **Verdict:** CORRECT  
- **Expected:** Yes; `PAYMENT_CONFIRMED_AT` nullable indicates order record can exist before payment; shipping constrained until payment confirmed  
- **Generated:** “Yes” because `SALES_ORDER_HDR.PAYMENT_CONFIRMED_AT` is nullable; correctly contrasts creation vs shipping  
- **Analysis:** Correct negative-query reasoning grounded in nullable payment-confirmation field and business rule about shipping.  
- **Retrieval:** gt_coverage=1.0, top_score=0.7, gate=proceed

### Q015: What schema fields support monetary value tracking across orders and their line items?
- **Type:** multi_hop | **Difficulty:** easy  
- **Verdict:** CORRECT  
- **Expected:** `SALES_ORDER_HDR.TOTAL_AMT`; `ORDER_LINE_ITEM.UNIT_PRICE`, `ORDER_LINE_ITEM.LINE_AMT` with reconciliation via `ORDER_ID`; note qty constrained >0  
- **Generated:** correctly covers `UNIT_PRICE`, `LINE_AMT`, and links them via `ORDER_ID`; includes `PAYMENT.AMOUNT` and FK relations; does not explicitly mention `SALES_ORDER_HDR.TOTAL_AMT` in the generation text, but still addresses monetary tracking (line-level + payment-level reconciliation) and remains grounded.  
- **Analysis:** Strongly aligned; slight omission of `TOTAL_AMT` detail in the narrative, but still semantically correct for the question’s intent.  
- **Retrieval:** gt_coverage=1.0, top_score=0.7, gate=proceed

## Anomalies & Recommendations

### Red Flags
- **Q011**: The generated answer references “`PAYMENT.STATUS`” while the retrieved context and schema fields suggest “`PAYMENT.STATUS_CODE`”. This did not trigger a rejection, but it’s a naming inconsistency that could matter for downstream users performing strict schema mapping.

### Recommendations
- Add/strengthen a **schema-field name exactness check** in the hallucination grader: when the answer claims a specific column, require matching the exact column identifier (e.g., `STATUS_CODE` vs `STATUS`).
- Track per-question **schema-token accuracy** (column identifiers) separately from semantic correctness, especially for multi-hop attribute questions.

## Comparison Notes (if applicable)
- No baseline comparison artifacts (e.g., “AB-00” metrics or explicit `ablation_context`) were provided, so comparison-based conclusions are not possible.