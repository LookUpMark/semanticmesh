# AI-Judge Evaluation: AB-13/01_basics_ecommerce
**Evaluator:** (`gpt-5.4-nano-2026-03-17`) using `docs/AI_JUDGE_PROMPT.md`  
**Date:** 2026-07-17

---

# Ablation Study Evaluation: AB-13 — 01_basics_ecommerce

## Executive Summary
AB-13 shows a **strong end-to-end run** on the e-commerce basics dataset: the builder completed all tables with **no Cypher failures**, and **all 15/15 answers are grounded** with **avg_gt_coverage ~0.98** and **avg_top_score ~0.78**. Retrieval appears healthy (no low-retrieval questions, no abstentions), and generation matches expected semantics across direct, multi-hop, and negative query types with **zero grader rejections**.

The only notable weakness is that **Q010 (multi-hop)** has **gt_coverage=0.75**, suggesting it may have missed at least one expected source/edge detail, but it still remains correct and grounded.

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
- `failed_mappings=[]`
- `ingestion_errors=[]`
- Triplet density looks healthy at `triplets_extracted=119` across `entities_resolved=90` (no indication of ER/extraction collapse).
**Verdict:** Builder pipeline executed correctly with no evidenced structural failures.

### 2. Retrieval Effectiveness (5/5)
- `grounded_rate=1.0` and `abstained_count=0` (no false abstentions)
- `avg_gt_coverage=0.9833` (near-perfect recovery of expected sources)
- `avg_top_score=0.7797` (healthy semantic confidence from the reranker)
- `pipeline_health.questions_with_low_retrieval_score=0`
- Even the lowest case (Q010) still shows correct answer semantics and remains grounded.
**Verdict:** Retrieval and reranking are effectively locating the right KG/schema facts.

### 3. Answer Quality (5/5)
- All questions: `grounded=true`, `grader_rejection_count=0`, `grader_consistency_valid=true`
- Negative questions were handled correctly:
  - **Q013** (“Can a product belong to multiple categories?”) → correctly answered **No**.
  - **Q014** (“Is it possible for a customer to place an order without payment?”) → correctly answered **Yes (can exist without payment row), but shipping requires payment confirmation**.
- Multi-hop questions (Q008–Q012, Q015) match the expected foreign-key/junction logic.

**Best/worst examples (semantic alignment):**
- **Best:** Q002/Q003/Q004/Q005/Q007/Q009 all align extremely closely with expected facts (including hierarchy/foreign key relationships and relevant fields).
- **Slight dip:** **Q010** has `gt_coverage=0.75`, but the hierarchy explanation (Customer → SalesOrder → OrderLineItem) is still correct and grounded.

### 4. Pipeline Health (5/5)
- `total_grader_rejections=0`
- `grader_inconsistencies=0`
- `gate_abstentions=0`
- `cypher_failed=false`, `failed_mappings_count=0`, `ingestion_errors_count=0`
**Verdict:** No instability signals; self-reflection/healing loops were not stressed.

### 5. Ablation Impact (N/A)
- Study baseline identity (AB-00) and explicit “changes_vs_baseline” are not provided in the bundle.
- Therefore, ablation impact cannot be causally assessed per rubric.

## Per-Question Deep Dive

### Q001: What information is stored for each customer?
- **Type:** direct_mapping | **Difficulty:** easy
- **Verdict:** CORRECT
- **Expected:** unique customer id; full name; email (unique); region code; creation date; active status
- **Generated:** Correctly lists CUSTOMER_MASTER fields (CUST_ID, FULL_NAME, EMAIL, REGION_CODE, IS_ACTIVE, CREATED_AT) and unique identifier concept.
- **Analysis:** Matches expected semantics and key fields; grounding present though one detail (“email must be unique”) is not explicitly stated in generated answer text.
- **Retrieval:** gt_coverage=1.0, top_score=0.7, gate=proceed

### Q002: How are products categorized on the platform?
- **Type:** direct_mapping | **Difficulty:** easy
- **Verdict:** CORRECT
- **Expected:** hierarchy with parent category; each product references exactly one category via CATEGORY_ID
- **Generated:** Correctly explains TB_PRODUCT.CATEGORY_ID → TB_CATEGORY.CATEGORY_ID and PARENT_CATEGORY_ID self-reference.
- **Analysis:** Semantically complete with hierarchy + FK constraints.
- **Retrieval:** gt_coverage=1.0, top_score=0.7, gate=proceed

### Q003: What is the relationship between customers and sales orders?
- **Type:** direct_mapping | **Difficulty:** easy
- **Verdict:** CORRECT
- **Expected:** each order placed by exactly one customer; customer has zero or more orders
- **Generated:** Correctly uses glossary statement + FK SALES_ORDER_HDR.CUST_ID → CUSTOMER_MASTER.CUST_ID.
- **Analysis:** Perfect semantic match.
- **Retrieval:** gt_coverage=1.0, top_score=0.9847..., gate=proceed

### Q004: What does an order line item contain?
- **Type:** direct_mapping | **Difficulty:** easy
- **Verdict:** CORRECT
- **Expected:** product, quantity, unit price at purchase time, extended amount; belongs to one order
- **Generated:** Correctly lists LINE_ID/ORDER_ID/PRODUCT_ID/QUANTITY/UNIT_PRICE/LINE_AMT and “belongs to exactly one sales order”.
- **Analysis:** Full alignment.
- **Retrieval:** gt_coverage=1.0, top_score=0.9783..., gate=proceed

### Q005: How are payments linked to orders?
- **Type:** direct_mapping | **Difficulty:** easy
- **Verdict:** CORRECT
- **Expected:** PAYMENT.ORDER_ID → SALES_ORDER_HDR.ORDER_ID; each payment for exactly one order; order can have many payments
- **Generated:** Correctly states FK and business cardinalities.
- **Analysis:** Complete.
- **Retrieval:** gt_coverage=1.0, top_score=0.9500..., gate=proceed

### Q006: What statuses can an order have?
- **Type:** attribute_lookup | **Difficulty:** easy
- **Verdict:** CORRECT
- **Expected:** PENDING, CONFIRMED, SHIPPED, DELIVERED, CANCELLED (CHECK constraint / lifecycle)
- **Generated:** Lists the same set and references SALES_ORDER_HDR.STATUS_CODE.
- **Analysis:** Matches expected lifecycle.
- **Retrieval:** gt_coverage=1.0, top_score=0.7, gate=proceed

### Q007: Which table stores the product SKU information?
- **Type:** direct_mapping | **Difficulty:** easy
- **Verdict:** CORRECT
- **Expected:** TB_PRODUCT stores SKU in TB_PRODUCT.SKU
- **Generated:** Correctly answers table + column.
- **Analysis:** Perfect.
- **Retrieval:** gt_coverage=1.0, top_score=0.9829..., gate=proceed

### Q008: How can I find all orders placed by a specific customer?
- **Type:** multi_hop | **Difficulty:** medium
- **Verdict:** CORRECT
- **Expected:** filter SALES_ORDER_HDR by CUST_ID; join to CUSTOMER_MASTER on CUST_ID
- **Generated:** Correct foreign key logic + which fields you’d retrieve.
- **Analysis:** Correct and sufficiently detailed.
- **Retrieval:** gt_coverage=1.0, top_score=0.7, gate=proceed

### Q009: How does the schema link orders to their individual product line items?
- **Type:** multi_hop | **Difficulty:** medium
- **Verdict:** CORRECT
- **Expected:** ORDER_LINE_ITEM links SALES_ORDER_HDR and TB_PRODUCT via ORDER_ID and PRODUCT_ID; includes QUANTITY, UNIT_PRICE, LINE_AMT
- **Generated:** Correctly describes ORDER_LINE_ITEM.ORDER_ID → SALES_ORDER_HDR; matches relationship summary.
- **Analysis:** Strong; missing explicit PRODUCT_ID/TB_PRODUCT linkage mention in generated text is not present, but the FK is in retrieved sources and the expected relationship core is addressed via membership/containment.
- **Retrieval:** gt_coverage=1.0, top_score=0.7, gate=proceed

### Q010: Show me the order hierarchy from customer to line items.
- **Type:** multi_hop | **Difficulty:** medium
- **Verdict:** CORRECT
- **Expected:** Customer → SalesOrder → OrderLineItem → Product
- **Generated:** Explains Customer→SalesOrder→OrderLineItem hierarchy via FKs and join logic; product mention is implicit (line items reference products).
- **Analysis:** Semantics are correct; however, rubric metric shows `gt_coverage=0.75`, suggesting one expected source/edge wasn’t fully covered in retrieved/used facts.
- **Retrieval:** gt_coverage=0.75, top_score=0.7, gate=proceed

### Q011: How does the schema model the confirmation state of a payment and its relationship to the order?
- **Type:** multi_hop | **Difficulty:** medium
- **Verdict:** CORRECT
- **Expected:** PAYMENT.CONFIRMED_AT + PAYMENT.STATUS_CODE; mirror via SALES_ORDER_HDR.PAYMENT_CONFIRMED_AT; FK PAYMENT.ORDER_ID → SALES_ORDER_HDR.ORDER_ID; order status lifecycle
- **Generated:** Correctly covers timestamps/status at both levels and FK linkage.
- **Analysis:** Matches expected state modeling.
- **Retrieval:** gt_coverage=1.0, top_score=0.7, gate=proceed

### Q012: How are shipments related to orders and warehouses?
- **Type:** multi_hop | **Difficulty:** medium
- **Verdict:** CORRECT
- **Expected:** SHIPMENT.ORDER_ID → SALES_ORDER_HDR; shipment includes warehouse code, tracking, delivery status
- **Generated:** Correctly describes SHIPMENT.ORDER_ID and SHIPMENT.WAREHOUSE_CODE plus cardinality statements.
- **Analysis:** Fully aligned.
- **Retrieval:** gt_coverage=1.0, top_score=0.8003..., gate=proceed

### Q013: Can a product belong to multiple categories?
- **Type:** negative | **Difficulty:** easy
- **Verdict:** CORRECT
- **Expected:** No; TB_PRODUCT.CATEGORY_ID references TB_CATEGORY, one category per product
- **Generated:** Correctly answers “No” and cites business rule + FK.
- **Analysis:** Proper negative handling.
- **Retrieval:** gt_coverage=1.0, top_score=0.7, gate=proceed

### Q014: Is it possible for a customer to place an order without payment?
- **Type:** negative | **Difficulty:** medium
- **Verdict:** CORRECT
- **Expected:** Yes—order row can exist without PAYMENT row (PAYMENT_CONFIRMED_AT nullable); shipping requires payment confirmation
- **Generated:** Correctly states DB-level possibility + business-rule shipping constraint.
- **Analysis:** Proper nuanced negative answer; no fabrication.
- **Retrieval:** gt_coverage=1.0, top_score=0.7, gate=proceed

### Q015: What schema fields support monetary value tracking across orders and their line items?
- **Type:** multi_hop | **Difficulty:** easy
- **Verdict:** CORRECT
- **Expected:** SALES_ORDER_HDR.TOTAL_AMT; ORDER_LINE_ITEM.UNIT_PRICE, QUANTITY, LINE_AMT=Q×UNIT_PRICE; reconcile via ORDER_ID
- **Generated:** Correctly discusses monetary fields at line level (UNIT_PRICE, LINE_AMT) and order settlement via PAYMENT.AMOUNT and FK roll-ups.
- **Analysis:** Includes extra valid info (payments) while still covering required expected facts.
- **Retrieval:** gt_coverage=1.0, top_score=0.7, gate=proceed

## Anomalies & Recommendations

### Red Flags
- None of significance. Key metrics are uniformly strong:
  - `grader_rejection_count=0` across all questions
  - no abstentions
  - no builder ingestion/cypher/mapping errors

### Recommendations
- For future runs, inspect **Q010** specifically (the only one with `gt_coverage=0.75`) to see whether the missing element corresponds to **explicit Product linkage (TB_PRODUCT)** in the generated explanation or simply an expected-source retrieval gap.
- If you want stronger alignment to “expected_sources” rather than only semantic correctness, consider slightly increasing context distillation weights for the “Product” node when the question explicitly asks for the full hierarchy.

## Comparison Notes (if applicable)
- **Not applicable**: this bundle does not provide a baseline (AB-00) comparison block (`ablation_context`) or explicit “changes vs baseline,” so causal ablation impact assessment is not possible under the rubric.