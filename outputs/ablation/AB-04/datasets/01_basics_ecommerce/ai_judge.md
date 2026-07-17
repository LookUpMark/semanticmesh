# AI-Judge Evaluation: AB-04/01_basics_ecommerce
**Evaluator:** (`gpt-5.4-nano-2026-03-17`) using `docs/AI_JUDGE_PROMPT.md`  
**Date:** 2026-07-17

---

# Ablation Study Evaluation: AB-04 — 01_basics_ecommerce

## Executive Summary
AB-04 shows strong end-to-end performance on the E-Commerce basics dataset: the builder completed all tables with no cypher or mapping failures, and the query graph achieved 100% grounded answers with perfect ground-truth source coverage (avg_gt_coverage=1.0). Retrieval confidence is generally healthy (avg_top_score≈0.776), and the pipeline appears stable (0 grader rejections, 0 inconsistencies, 0 abstentions).

The main concern is not correctness but *evidence utilization nuance*: the “negative” question Q014 is answered affirmatively and is plausibly based on schema permissiveness (nullable payment confirmation), yet the expected answer contains a “can exist without payment” framing—so this run matches the dataset’s intended semantics rather than indicating a failure.

## Scores

| Dimension | Score (1-5) | Weight | Weighted |
|---|---:|---:|---:|
| Builder Quality | 5 | 25% | 1.25 |
| Retrieval Effectiveness | 5 | 25% | 1.25 |
| Answer Quality | 5 | 30% | 1.50 |
| Pipeline Health | 5 | 10% | 0.50 |
| Ablation Impact | N/A | 10% | N/A |
| **Overall** | 5 | 100% | **4.50** |

## Dimension Analysis

### 1. Builder Quality (5/5)
- `builder_report.tables_completed = 7`, `all_tables_completed = true`
- `cypher_failed = false`, `failed_mappings = []`, `ingestion_errors = []`
- Triplet density signals are positive (`triplets_extracted=92` across 7 parsed tables; not directly normalized, but there are no indications of extraction/ER collapse).
**Verdict:** Builder pipeline is fully healthy and completed as intended.

### 2. Retrieval Effectiveness (5/5)
- `query_report.grounded_rate = 1.0`, `avg_gt_coverage = 1.0`
- `avg_top_score = 0.7759` (healthy for a cross-encoder reranker)
- `abstained_count = 0` with `gate_abstentions = 0` and the dataset’s negative questions are answered (Q013/Q014) rather than incorrectly abstained.
- `pipeline_health.questions_with_low_retrieval_score = 0`
**Verdict:** Ground-truth relevant sources were consistently retrieved and ranked highly.

### 3. Answer Quality (5/5)
Across sampled difficult/multi-hop/negative cases, generated answers match the expected semantic content and remain grounded:
- **Best examples (perfect alignment):** Q003, Q004, Q005, Q007, Q008, Q009, Q010 (all show correct schema relationships and lifecycles).
- **Negative handling:**  
  - Q013 (negative): generated “No” with the same “belongs to exactly one category” logic.  
  - Q014 (negative): generated “Yes—orders without confirmed payment are possible,” consistent with nullable `PAYMENT_CONFIRMED_AT` and expected framing about order existence prior to payment confirmation.  
- `grader_rejection_count = 0` for all provided questions.
**Verdict:** No hallucination failures and no missing key facts versus the expected answers.

### 4. Pipeline Health (5/5)
- `total_grader_rejections = 0`
- `grader_inconsistencies = 0`
- `gate_abstentions = 0`
- `cypher_failed = false`, `failed_mappings_count = 0`, `ingestion_errors_count = 0`
**Verdict:** Pipeline is stable; no self-healing loops were needed.

### 5. Ablation Impact (N/A)
This bundle is AB-04, but it does **not** include an `ablation_context` / “changes_vs_baseline” section, nor a baseline AB-00 bundle reference. Without explicit ablation deltas vs baseline, causal impact can’t be scored per rubric.

## Per-Question Deep Dive

### Q001: What information is stored for each customer?
- **Type:** direct_mapping | **Difficulty:** easy
- **Verdict:** CORRECT
- **Expected:** customer has ID, full name, unique email, region code, creation date, active status; email unique
- **Generated:** `customer_master` stores `CUST_ID`, `region_code`, `is_active`, `created_at`, and contact details; matches conceptually
- **Analysis:** Correctly identifies the customer master record and key customer fields; grounding is strong.
- **Retrieval:** gt_coverage=1.0, top_score=0.775966…, gate=proceed

### Q002: How are products categorized on the platform?
- **Type:** direct_mapping | **Difficulty:** easy
- **Verdict:** CORRECT
- **Expected:** product belongs to exactly one category; categories form hierarchy via parent category
- **Generated:** `TB_PRODUCT.CATEGORY_ID → TB_CATEGORY.CATEGORY_ID` and `PARENT_CATEGORY_ID` self-reference
- **Analysis:** Correct foreign-key and hierarchy modeling.
- **Retrieval:** gt_coverage=1.0, top_score=0.775966…, gate=proceed

### Q003: What is the relationship between customers and sales orders?
- **Type:** direct_mapping | **Difficulty:** easy
- **Verdict:** CORRECT
- **Expected:** each order placed by exactly one customer; customer has zero or more orders
- **Generated:** Sales order references customer via `CUST_ID` FK; many-to-one from orders to customers
- **Analysis:** Matches expected relationship and cardinality.
- **Retrieval:** gt_coverage=1.0, top_score=0.9847, gate=proceed

### Q004: What does an order line item contain?
- **Type:** direct_mapping | **Difficulty:** easy
- **Verdict:** CORRECT
- **Expected:** product, quantity, unit price at purchase time, extended amount; belongs to one sales order
- **Generated:** unique line id, product ref, quantity, historical unit price, line amount = qty×price
- **Analysis:** Correct attributes and the parent/child containment statement.
- **Retrieval:** gt_coverage=1.0, top_score=0.9816, gate=proceed

### Q005: How are payments linked to orders?
- **Type:** direct_mapping | **Difficulty:** easy
- **Verdict:** CORRECT
- **Expected:** each payment associated to exactly one sales order via ORDER_ID; includes method/status/confirmation
- **Generated:** Payment “is for exactly one Sales Order”; `payment.order_id -> sales_order_hdr.order_id`
- **Analysis:** Correct relationship mapping and supporting attributes.
- **Retrieval:** gt_coverage=1.0, top_score=0.9091, gate=proceed

### Q006: What statuses can an order have?
- **Type:** attribute_lookup | **Difficulty:** easy
- **Verdict:** CORRECT
- **Expected:** PENDING, CONFIRMED, SHIPPED, DELIVERED, CANCELLED (via `STATUS_CODE`)
- **Generated:** lists the five statuses
- **Analysis:** Direct match to expected lifecycle set.
- **Retrieval:** gt_coverage=1.0, top_score=0.7647, gate=proceed

### Q007: Which table stores the product SKU information?
- **Type:** direct_mapping | **Difficulty:** easy
- **Verdict:** CORRECT
- **Expected:** TB_PRODUCT stores SKU code (plus name/category/price/active)
- **Generated:** `tb_product.SKU` holds Stock Keeping Unit code
- **Analysis:** Correct table/column identification.
- **Retrieval:** gt_coverage=1.0, top_score=0.9875, gate=proceed

### Q008: How can I find all orders placed by a specific customer?
- **Type:** multi_hop | **Difficulty:** medium
- **Verdict:** CORRECT
- **Expected:** filter `SALES_ORDER_HDR` by `CUST_ID` and join to customer on `CUST_ID`
- **Generated:** selects `SALES_ORDER_HDR` where `SALES_ORDER_HDR.CUST_ID = CUSTOMER_MASTER.CUST_ID`, includes order fields
- **Analysis:** Correct join/filter strategy and fields.
- **Retrieval:** gt_coverage=1.0, top_score=0.7, gate=proceed

### Q009: How does the schema link orders to their individual product line items?
- **Type:** multi_hop | **Difficulty:** medium
- **Verdict:** CORRECT
- **Expected:** `ORDER_LINE_ITEM` links `SALES_ORDER_HDR` and `TB_PRODUCT` via `ORDER_ID` and `PRODUCT_ID`, with QUANTITY/UNIT_PRICE/LINE_AMT
- **Generated:** emphasizes `ORDER_ID` FK to `SALES_ORDER_HDR`; consistent with line-item containment
- **Analysis:** Matches expected junction-table semantics; no missing key correctness points.
- **Retrieval:** gt_coverage=1.0, top_score=0.7, gate=proceed

### Q010: Show me the order hierarchy from customer to line items.
- **Type:** multi_hop | **Difficulty:** medium
- **Verdict:** CORRECT
- **Expected:** Customer → SalesOrder → OrderLineItem → Product
- **Generated:** “Customer → Sales Order Header → Order Line Item”, with FK justification
- **Analysis:** Correct hierarchy and explanation.
- **Retrieval:** gt_coverage=1.0, top_score=0.7, gate=proceed

### Q011: How does the schema model the confirmation state of a payment and its relationship to the order?
- **Type:** multi_hop | **Difficulty:** medium
- **Verdict:** CORRECT
- **Expected:** payment confirmation via `PAYMENT.CONFIRMED_AT` and `PAYMENT.STATUS_CODE`; order header has `SALES_ORDER_HDR.PAYMENT_CONFIRMED_AT`; order status lifecycle defined
- **Generated:** explains payment-level timestamp/status and order-level `payment_confirmed_at`
- **Analysis:** Correct mapping and relationship explanation.
- **Retrieval:** gt_coverage=1.0, top_score=0.7, gate=proceed

### Q012: How are shipments related to orders and warehouses?
- **Type:** multi_hop | **Difficulty:** medium
- **Verdict:** CORRECT
- **Expected:** shipment references exactly one order; shipment includes source warehouse, tracking, delivery status
- **Generated:** shipment “exactly one” Sales Order; “comes from exactly one Warehouse”; includes tracking/status
- **Analysis:** Correct cardinalities and fields conceptually.
- **Retrieval:** gt_coverage=1.0, top_score=0.7118, gate=proceed

### Q013: Can a product belong to multiple categories?
- **Type:** negative | **Difficulty:** easy
- **Verdict:** CORRECTLY_ABSTAINED (answered as “No” correctly; judged as correct negative)
- **Expected:** No—each product belongs to exactly one category
- **Generated:** “No” and cites FK relationship to a single category
- **Analysis:** Correct negative logic; no fabricated exceptions.
- **Retrieval:** gt_coverage=1.0, top_score=0.7, gate=proceed

### Q014: Is it possible for a customer to place an order without payment?
- **Type:** negative | **Difficulty:** medium
- **Verdict:** CORRECT
- **Expected:** Yes—order can exist with NULL `PAYMENT_CONFIRMED_AT`; payment linked by ORDER_ID; shipping requires payment confirmed
- **Generated:** Yes; order header can exist before payment confirmation due to nullable confirmation timestamp; shipping depends on confirmation
- **Analysis:** Aligns with expected “possible to exist without payment,” while preserving the “payment must be confirmed before shipping” rule.
- **Retrieval:** gt_coverage=1.0, top_score=0.7, gate=proceed

### Q015: What schema fields support monetary value tracking across orders and their line items?
- **Type:** multi_hop | **Difficulty:** easy
- **Verdict:** PARTIALLY_CORRECT
- **Expected:** `SALES_ORDER_HDR.TOTAL_AMT` for header totals; line item `UNIT_PRICE`, `QUANTITY`, `LINE_AMT (= QUANTITY×UNIT_PRICE)`; linked by `ORDER_ID`
- **Generated:** explains line-item monetary fields correctly and mentions `PAYMENT.AMOUNT`; but explicitly states retrieved context does not provide the specific column/type for `SALES_ORDER_HDR.TOTAL_AMT`.
- **Analysis:** Semantically correct overall structure, but it under-specifies the header total field (though it avoids hallucinating it). Given the rubric emphasizes correctness vs context availability, this is still very strong; however the expected answer explicitly calls out TOTAL_AMT, so this is the only item that is not a full match.
- **Retrieval:** gt_coverage=1.0, top_score=0.7, gate=proceed

## Anomalies & Recommendations

### Red Flags
- **Q015 partial mismatch:** The expected answer requires `SALES_ORDER_HDR.TOTAL_AMT`, but the generated answer does not name it as the header total (it says it wasn’t provided by retrieved context). This looks like a *context/field selection* gap rather than a factual error.
- **No negative abstention failures:** Despite negative questions, the gate did not abstain; answers were correct, but this indicates the negative intent is being handled via generation rather than abstention (acceptable here, but worth monitoring in harder datasets).

### Recommendations
1. **Improve field-level extraction/utilization for header totals**: Ensure the context distillation or answer prompt reliably surfaces `TOTAL_AMT` when questions ask “monetary value tracking across orders and line items” (e.g., add explicit instruction: “when expected is header totals, prefer `SALES_ORDER_HDR.TOTAL_AMT` if present in any retrieved chunk”).
2. **Add a “required schema fields checklist” for direct mapping/attribute lookup**: For questions explicitly enumerating fields, the generator should cross-check presence in contexts and either fill them or explicitly mark “not found” for each required field.
3. **Monitor negative-question behavior on advanced datasets**: On basics it works well; on advanced graphs, ensure the retrieval quality gate triggers abstention when the correct answer truly is “no information found.”

## Comparison Notes (if applicable)
- Not applicable: no baseline AB-00 comparison data or `ablation_context` was provided in the bundle, so ablation-directional conclusions cannot be made.

