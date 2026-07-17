# AI-Judge Evaluation: AB-08/01_basics_ecommerce
**Evaluator:** (`gpt-5.4-nano-2026-03-17`) using `docs/AI_JUDGE_PROMPT.md`  
**Date:** 2026-07-17

---

# Ablation Study Evaluation: AB-08 — 01_basics_ecommerce

## Executive Summary
AB-08 shows excellent end-to-end performance on this **basics** e-commerce dataset: builder completed all tables with **no Cypher failures/mapping failures**, and the query graph produced **grounded answers for all 15/15 questions** with very high average GT coverage (**0.983**) and strong average top reranker score (**0.779**). The only notable weakness is that some multi-hop answers (e.g., order-to-line-item/product hierarchy) retrieve sufficient sources but sometimes mix in extra context (payments/shipments) rather than staying tightly scoped—however, this does not translate into incorrectness.

## Scores

| Dimension | Score (1-5) | Weight | Weighted |
|---|---:|---:|---:|
| Builder Quality | 5 | 25% | 1.25 |
| Retrieval Effectiveness | 5 | 25% | 1.25 |
| Answer Quality | 5 | 30% | 1.50 |
| Pipeline Health | 5 | 10% | 0.50 |
| Ablation Impact | 3 | 10% | 0.30 |
| **Overall** |  |  | **4.80** |

## Dimension Analysis

### 1. Builder Quality (5/5)
- `tables_parsed=7`, `tables_completed=7`, `all_tables_completed=true`
- `cypher_failed=false`
- `failed_mappings=[]`
- `ingestion_errors=[]`
- Triplet extraction/ER appears healthy enough for these results (`triplets_extracted=100`, `entities_resolved=63`), and there are **no downstream graph construction failures**.

**Verdict:** Meets the rubric’s top-tier criteria (all tables completed, no cypher failures, no failed mappings).

### 2. Retrieval Effectiveness (5/5)
- `total_questions=15`, `grounded_rate=1.0`, `abstained_count=0`
- `avg_gt_coverage=0.9833` (very high)
- `avg_top_score=0.7794` (strong reranker confidence for bge-reranker-v2-m3)
- `pipeline_health.questions_with_low_retrieval_score=0`

**Verdict:** Retrieval quality is clearly sufficient across the board; even negative questions were answered correctly without triggering abstention issues.

### 3. Answer Quality (5/5)
- `grounded_count=15` and **no grader rejections** (`grader_rejection_count=0` for every shown question)
- For negative queries:
  - **Q013 (negative):** Correctly answers “No” and grounds it in “belongs to exactly one Category” + FK `CATEGORY_ID -> TB_CATEGORY`.
  - **Q014 (negative):** Correctly answers “Yes” and uses the nullability of `SALES_ORDER_HDR.PAYMENT_CONFIRMED_AT` to justify order existence without confirmed payment, while acknowledging shipping constraints.

**Per-question semantic check highlights:**
- Q001, Q002, Q003, Q004, Q005, Q006, Q007 all align with expected facts and schema relations.
- Multi-hop queries (Q008–Q012, Q015) provide correct join paths and key fields.
- Q010 shows some potential scope noise (retrieves shipment/payment contexts), but the **core hierarchy described is correct**, and the bundle reports grounding and no rejections.

**Verdict:** All answers are semantically correct and grounded; no evidence of wrong or fabricated claims.

### 4. Pipeline Health (5/5)
- `pipeline_health.cypher_failed=false`
- `total_grader_rejections=0`
- `grader_inconsistencies=0`
- `gate_abstentions=0`
- `failed_mappings_count=0`, `ingestion_errors_count=0`

**Verdict:** Stable pipeline, no error recovery artifacts needed.

### 5. Ablation Impact (3/5)
This bundle is **AB-08**, but the bundle provided does **not include `ablation_context`** nor a “changes_vs_baseline” field, so we cannot rigorously validate the intended ablation causal hypothesis.

What we *can* infer from config:
- `retrieval_mode=hybrid`, `enable_reranker=true`, `enable_cypher_healing`/`enable_critic_validation`/`enable_hallucination_grader` are not explicitly present here (so we cannot confirm which components were disabled/enabled vs baseline).
- Performance is excellent; without knowing the ablated components, it’s unclear whether AB-08 caused improvement/degradation.

**Verdict:** Quality is high, but ablation attribution is under-specified in the provided bundle → middle score.

## Per-Question Deep Dive

### Q001: What information is stored for each customer?
- **Type:** direct_mapping | **Difficulty:** easy  
- **Verdict:** CORRECT  
- **Expected:** CUST_ID, full name, email (unique), region code, created date, active status  
- **Generated:** Enumerates all those fields from `CUSTOMER_MASTER` and aligns with the schema columns  
- **Analysis:** Correct table/field mapping; includes email uniqueness indirectly via “email” attribute (expected says must be unique).  
- **Retrieval:** gt_coverage=1.0, top_score=0.7482, gate=proceed

### Q002: How are products categorized on the platform?
- **Type:** direct_mapping | **Difficulty:** easy  
- **Verdict:** CORRECT  
- **Expected:** each product references exactly one category; categories have optional parent for hierarchy  
- **Generated:** Matches `TB_PRODUCT.CATEGORY_ID -> TB_CATEGORY.CATEGORY_ID` and `PARENT_CATEGORY_ID`  
- **Analysis:** Correct hierarchical category modeling  
- **Retrieval:** gt_coverage=1.0, top_score=0.7, gate=proceed

### Q003: What is the relationship between customers and sales orders?
- **Type:** direct_mapping | **Difficulty:** easy  
- **Verdict:** CORRECT  
- **Expected:** Sales order placed by exactly one customer (0..* orders per customer) via `CUST_ID` FK  
- **Generated:** States the relationship and FK path `SALES_ORDER_HDR.CUST_ID -> CUSTOMER_MASTER.CUST_ID`  
- **Analysis:** Correct cardinality and join key  
- **Retrieval:** gt_coverage=1.0, top_score=0.9847, gate=proceed

### Q004: What does an order line item contain?
- **Type:** direct_mapping | **Difficulty:** easy  
- **Verdict:** CORRECT  
- **Expected:** product, quantity, unit price at purchase time, extended amount; belongs to exactly one sales order  
- **Generated:** Includes line identifier and matches `LINE_AMT = quantity × unit price`  
- **Analysis:** Correct attributes; correctly grounded  
- **Retrieval:** gt_coverage=1.0, top_score=0.9885, gate=proceed

### Q005: How are payments linked to orders?
- **Type:** direct_mapping | **Difficulty:** easy  
- **Verdict:** CORRECT  
- **Expected:** Payment references exactly one sales order via ORDER_ID; stores method, amount, status, confirmation time  
- **Generated:** Correctly maps `PAYMENT.ORDER_ID -> SALES_ORDER_HDR.ORDER_ID` and mentions relevant fields  
- **Analysis:** Correct FK relationship and attribute set  
- **Retrieval:** gt_coverage=1.0, top_score=0.9501, gate=proceed

### Q006: What statuses can an order have?
- **Type:** attribute_lookup | **Difficulty:** easy  
- **Verdict:** CORRECT  
- **Expected:** PENDING, CONFIRMED, SHIPPED, DELIVERED, CANCELLED  
- **Generated:** Lists exactly those statuses from the glossary/business concept mapping  
- **Analysis:** Correct enumeration  
- **Retrieval:** gt_coverage=1.0, top_score=0.7, gate=proceed

### Q007: Which table stores the product SKU information?
- **Type:** direct_mapping | **Difficulty:** easy  
- **Verdict:** CORRECT  
- **Expected:** TB_PRODUCT.SKU  
- **Generated:** States `TB_PRODUCT` and `TB_PRODUCT.SKU`  
- **Analysis:** Precise and correct  
- **Retrieval:** gt_coverage=1.0, top_score=0.9892, gate=proceed

### Q008: How can I find all orders placed by a specific customer?
- **Type:** multi_hop | **Difficulty:** medium  
- **Verdict:** CORRECT  
- **Expected:** filter `SALES_ORDER_HDR` by `CUST_ID`, join to `CUSTOMER_MASTER` if desired  
- **Generated:** Exactly describes the filter/join strategy  
- **Analysis:** Correct join path and key column  
- **Retrieval:** gt_coverage=1.0, top_score=0.7, gate=proceed

### Q009: How does the schema link orders to their individual product line items?
- **Type:** multi_hop | **Difficulty:** medium  
- **Verdict:** CORRECT  
- **Expected:** ORDER_LINE_ITEM as junction: ORDER_ID FK to SALES_ORDER_HDR and PRODUCT_ID FK to TB_PRODUCT; includes quantity/unit_price/line_amt  
- **Generated:** Correctly explains the association via `ORDER_LINE_ITEM.ORDER_ID` and product via `ORDER_LINE_ITEM.PRODUCT_ID`  
- **Analysis:** Correct conceptual modeling; includes link semantics.  
- **Retrieval:** gt_coverage=1.0, top_score=0.7, gate=proceed

### Q010: Show me the order hierarchy from customer to line items.
- **Type:** multi_hop | **Difficulty:** medium  
- **Verdict:** PARTIALLY_CORRECT  
- **Expected:** Customer → SalesOrder → OrderLineItem → Product  
- **Generated:** Correctly states Customer → Sales Order → Order Line Items and points to FK chain via `CUSTOMER_MASTER.CUST_ID` and `SALES_ORDER_HDR.ORDER_ID -> ORDER_LINE_ITEM.ORDER_ID`.  
- **Analysis:** The FK path to **Product** is not as explicit as expected (it mentions `ORDER_LINE_ITEM.PRODUCT_ID` in retrieved contexts, but the answer’s main chain stops at line items). Still grounded and not wrong about hierarchy direction/cardinality.  
- **Retrieval:** gt_coverage=0.75, top_score=0.7, gate=proceed

### Q011: How does the schema model the confirmation state of a payment and its relationship to the order?
- **Type:** multi_hop | **Difficulty:** medium  
- **Verdict:** CORRECT  
- **Expected:** PAYMENT.CONFIRMED_AT + PAYMENT.STATUS_CODE, and order-level PAYMENT_CONFIRMED_AT mirror; FK PAYMENT.ORDER_ID -> SALES_ORDER_HDR  
- **Generated:** Correctly explains nullable confirmed-at and status code, plus FK and order timestamp  
- **Analysis:** Matches expected modeling  
- **Retrieval:** gt_coverage=1.0, top_score=0.7, gate=proceed

### Q012: How are shipments related to orders and warehouses?
- **Type:** multi_hop | **Difficulty:** medium  
- **Verdict:** CORRECT  
- **Expected:** SHIPMENT.ORDER_ID FK to SALES_ORDER_HDR; warehouse code + tracking/status  
- **Generated:** Correctly states SHIPMENT references one order and links to warehouse via SHIPMENT.WAREHOUSE_CODE; mentions partial shipments  
- **Analysis:** Correct relationship summary  
- **Retrieval:** gt_coverage=1.0, top_score=0.7310, gate=proceed

### Q013: Can a product belong to multiple categories?
- **Type:** negative | **Difficulty:** easy  
- **Verdict:** CORRECTLY_ABSTAINED? → (Answered) CORRECT  
- **Expected:** No; belongs to exactly one category via TB_PRODUCT.CATEGORY_ID -> TB_CATEGORY  
- **Generated:** “No” and explains single FK + NOT NULL  
- **Analysis:** Correct negative handling and grounded justification  
- **Retrieval:** gt_coverage=1.0, top_score=0.7, gate=proceed

### Q014: Is it possible for a customer to place an order without payment?
- **Type:** negative | **Difficulty:** medium  
- **Verdict:** CORRECT  
- **Expected:** Yes—orders can exist without payment row; shipping requires payment confirmation  
- **Generated:** “Yes” using nullability of `SALES_ORDER_HDR.PAYMENT_CONFIRMED_AT`, while stating shipping restriction  
- **Analysis:** Correct separation between “order exists” vs “can ship”  
- **Retrieval:** gt_coverage=1.0, top_score=0.7, gate=proceed

### Q015: What schema fields support monetary value tracking across orders and their line items?
- **Type:** multi_hop | **Difficulty:** easy  
- **Verdict:** CORRECT  
- **Expected:** Order total in SALES_ORDER_HDR.TOTAL_AMT; line-level UNIT_PRICE, QUANTITY, LINE_AMT; reconciliation via ORDER_ID  
- **Generated:** Correctly explains line and order/payment monetary fields; notes line/unit price history and line amount computation  
- **Analysis:** Correct fields and join logic; answer also discusses PAYMENT.AMOUNT as amount tracking.  
- **Retrieval:** gt_coverage=1.0, top_score=0.7, gate=proceed

## Anomalies & Recommendations

### Red Flags
- **Q010** shows reduced GT coverage (`gt_coverage=0.75`) and slightly under-specifies the Product link in the main hierarchy chain. This is minor but indicates multi-hop traversal isn’t always “fully expressed” even when concepts are available.
- Some multi-hop answers retrieve extra concept contexts (e.g., payment/shipment) that are not strictly necessary; this didn’t harm correctness here, but could reduce answer tightness in harder datasets.

### Recommendations
- For multi-hop generation, add a lightweight **“required path checklist”** prompt keyed by the expected entity sequence (e.g., Customer→Order→LineItem→Product) to ensure the final hop (PRODUCT_ID) is explicitly verbalized.
- Add a small retrieval distillation rule: if a query asks for a strict hierarchy, cap retrieval to only sources contributing to the specified hop chain (reduces noise from payments/shipments).
- If negative questions exist in more complex datasets, consider a stricter correlation between “negative query_type” and **abstain vs explicit answer** policy, even though AB-08 handled negatives perfectly.

## Comparison Notes (if applicable)
- No baseline (AB-00) configuration or `ablation_context` is provided in the bundle, so quantitative “vs baseline” comparison cannot be made. Overall performance is excellent, but the lack of explicit ablation diffs limits causal interpretation.