# AI-Judge Evaluation: AB-15/01_basics_ecommerce
**Evaluator:** (`gpt-5.4-nano-2026-03-17`) using `docs/AI_JUDGE_PROMPT.md`  
**Date:** 2026-07-17

---

# Ablation Study Evaluation: AB-15 — 01_basics_ecommerce

## Executive Summary
AB-15 shows a fully healthy end-to-end run on the e-commerce “basics” dataset: all 7 builder tables completed with no Cypher/mapping/ingestion failures, and all 15 queries were answered (0 abstentions) with perfect grounded rate (1.0). Retrieval and answer quality are strong overall (avg gt_coverage=0.85, avg_top_score≈0.75), with the main architectural concern being one clear retrieval miss (Q008: gt_coverage=0) where the system still produced a grounded answer.

## Scores

| Dimension | Score (1-5) | Weight | Weighted |
|---|---:|---:|---:|
| Builder Quality | 5 | 25% | 1.25 |
| Retrieval Effectiveness | 4 | 25% | 1.00 |
| Answer Quality | 5 | 30% | 1.50 |
| Pipeline Health | 5 | 10% | 0.50 |
| Ablation Impact | N/A | 10% | 0.00 |
| **Overall** |  |  | **4.25** |

## Dimension Analysis

### 1. Builder Quality (5/5)
- `tables_parsed=7`, `tables_completed=7`, `all_tables_completed=true`
- `cypher_failed=false`, `failed_mappings=[]`, `ingestion_errors=[]`
- Triplet extraction is substantial: `triplets_extracted=119`, and `entities_resolved=91` is plausible for basics (no ER blow-up signals).
- No evidence of builder degradation, fallback Cypher, or skipped work (`builder_skipped=false`).

### 2. Retrieval Effectiveness (4/5)
- `grounded_rate=1.0` and `abstained_count=0` (no false abstentions).
- `avg_gt_coverage=0.85` meets the rubric for a high-performing retrieval regime, though not perfect.
- `avg_top_score=0.747` is very strong for a cross-encoder reranker (right in the healthy band).
- **Key exception:** **Q008** has `gt_coverage=0.0` while the system still answered with `grounded=true`. This indicates either:
  - the answer relied on non-GT sources that were still correct/adequate, or
  - the ground-truth coverage calculation is strict to expected_sources/coverage labels.
  Either way, it prevents a 5/5 retrieval score. All other questions show `gt_coverage=1.0` (except Q010 at 0.75).

### 3. Answer Quality (5/5)
- `query_report.grounded_rate=1.0` across all 15 questions.
- No grader rejections and no consistency issues: `total_grader_rejections=0`.
- Negative questions were handled correctly:
  - **Q013** (negative): correctly states products belong to exactly one category.
  - **Q014** (negative): answers “Yes” with reasoning grounded in schema nullability/constraints about shipping vs ordering.
- For the worst retrieval case (Q008), the content is still semantically aligned with the expected query intent (orders filtered by `CUST_ID` join/relationship).

### 4. Pipeline Health (5/5)
- `total_grader_rejections=0`
- `grader_inconsistencies=0`
- `gate_abstentions=0`
- `cypher_failed=false`
- `failed_mappings_count=0`, `ingestion_errors_count=0`
- Latency fields are `0`/near-zero in the bundle, so no practical performance regression signals can be extracted—but importantly, there are no stability failures.

### 5. Ablation Impact (N/A)
- This bundle is labeled `AB-15`, but it does not include `ablation_context` or a `baseline` comparison in the provided JSON.
- Therefore, ablation causal impact cannot be assessed against AB-00 per rubric.

## Dimension 4/5 Notes on Specific Strengths
- Multi-hop questions (Q008–Q012, Q015) were answered coherently using the expected join paths and foreign-key semantics.
- The system maintained correctness even when `gt_coverage` dipped (Q010, Q008), suggesting the distilled contexts were sufficient and generation was not brittle.

---

## Per-Question Deep Dive

### Q001: What information is stored for each customer?
- **Type:** direct_mapping | **Difficulty:** easy
- **Verdict:** CORRECT
- **Expected:** customer has ID, full name, email (unique), region code, created_at, active status
- **Generated:** describes CUSTOMER_MASTER fields including `CUST_ID`, `FULL_NAME`, `EMAIL`, `REGION_CODE`, `CREATED_AT`, `IS_ACTIVE`; aligns with uniqueness of email (by attribute description)
- **Analysis:** Matches schema/glossary; correctly lists all key customer attributes.
- **Retrieval:** gt_coverage=1.0, top_score=0.7, gate=proceed

### Q002: How are products categorized on the platform?
- **Type:** direct_mapping | **Difficulty:** easy
- **Verdict:** CORRECT
- **Expected:** product references exactly one category via CATEGORY_ID; category hierarchy via parent category
- **Generated:** explains FK `TB_PRODUCT.CATEGORY_ID → TB_CATEGORY.CATEGORY_ID` and self-referential `PARENT_CATEGORY_ID`
- **Analysis:** Correctly captures hierarchy and “exactly one category” constraint.
- **Retrieval:** gt_coverage=1.0, top_score=0.7, gate=proceed

### Q003: What is the relationship between customers and sales orders?
- **Type:** direct_mapping | **Difficulty:** easy
- **Verdict:** CORRECT
- **Expected:** each sales order is placed by exactly one customer; customer can have zero or more orders
- **Generated:** states 1-to-many with FK `SALES_ORDER_HDR.CUST_ID → CUSTOMER_MASTER.CUST_ID`
- **Analysis:** Correct relationship direction and multiplicity.
- **Retrieval:** gt_coverage=1.0, top_score=0.9847, gate=proceed

### Q004: What does an order line item contain?
- **Type:** direct_mapping | **Difficulty:** easy
- **Verdict:** CORRECT
- **Expected:** product, quantity, unit price at time of purchase, extended amount; belongs to one sales order
- **Generated:** lists `LINE_ID`, `ORDER_ID`, `PRODUCT_ID`, `QUANTITY`, `UNIT_PRICE`, `LINE_AMT`
- **Analysis:** Fully consistent with glossary/schema.
- **Retrieval:** gt_coverage=1.0, top_score=0.8740, gate=proceed

### Q005: How are payments linked to orders?
- **Type:** direct_mapping | **Difficulty:** easy
- **Verdict:** CORRECT
- **Expected:** PAYMENT.ORDER_ID → SALES_ORDER_HDR.ORDER_ID; payment includes method, amount, status, confirmation timestamp
- **Generated:** describes exact FK and business rule “for exactly one sales order”
- **Analysis:** Correct linking and attribute coverage.
- **Retrieval:** gt_coverage=1.0, top_score=0.9501, gate=proceed

### Q006: What statuses can an order have?
- **Type:** attribute_lookup | **Difficulty:** easy
- **Verdict:** CORRECT
- **Expected:** PENDING, CONFIRMED, SHIPPED, DELIVERED, CANCELLED
- **Generated:** lists same five statuses; references `SALES_ORDER_HDR.STATUS_CODE`
- **Analysis:** Exact match.
- **Retrieval:** gt_coverage=1.0, top_score=0.7, gate=proceed

### Q007: Which table stores the product SKU information?
- **Type:** direct_mapping | **Difficulty:** easy
- **Verdict:** CORRECT
- **Expected:** TB_PRODUCT.SKU
- **Generated:** explicitly states SKU is stored in `TB_PRODUCT.SKU`
- **Analysis:** Precise table/column answer.
- **Retrieval:** gt_coverage=1.0, top_score=0.7, gate=proceed

### Q008: How can I find all orders placed by a specific customer?
- **Type:** multi_hop | **Difficulty:** medium
- **Verdict:** CORRECT
- **Expected:** query SALES_ORDER_HDR filtered by CUST_ID; join on CUSTOMER_MASTER.CUST_ID
- **Generated:** explains filtering `SALES_ORDER_HDR` by `CUST_ID` and optional join to CUSTOMER_MASTER
- **Analysis:** Semantically correct join path, though **coverage metric** says gt_coverage=0.
- **Retrieval:** gt_coverage=0.0, top_score=0.7, gate=proceed

### Q009: How does the schema link orders to their individual product line items?
- **Type:** multi_hop | **Difficulty:** medium
- **Verdict:** CORRECT
- **Expected:** ORDER_LINE_ITEM is junction: ORDER_ID → SALES_ORDER_HDR, PRODUCT_ID → TB_PRODUCT; includes qty/unit_price/line_amt
- **Generated:** explains linkage via `ORDER_LINE_ITEM.ORDER_ID → SALES_ORDER_HDR(ORDER_ID)`
- **Analysis:** Correct relationship; does not explicitly mention PRODUCT_ID in the final statement, but the schema sources include it; overall intent is met.
- **Retrieval:** gt_coverage=1.0, top_score=0.7, gate=proceed

### Q010: Show me the order hierarchy from customer to line items.
- **Type:** multi_hop | **Difficulty:** medium
- **Verdict:** CORRECT
- **Expected:** CUSTOMER_MASTER → SALES_ORDER_HDR → ORDER_LINE_ITEM → TB_PRODUCT
- **Generated:** provides the stepwise traversal via CUST_ID and ORDER_ID; describes line items and links to products
- **Analysis:** Correct hierarchy and traversal description.
- **Retrieval:** gt_coverage=0.75, top_score=0.7, gate=proceed

### Q011: How does the schema model the confirmation state of a payment and its relationship to the order?
- **Type:** multi_hop | **Difficulty:** medium
- **Verdict:** CORRECT
- **Expected:** PAYMENT.CONFIRMED_AT nullable; PAYMENT.STATUS_CODE lifecycle; SALES_ORDER_HDR.PAYMENT_CONFIRMED_AT mirrors; FK PAYMENT.ORDER_ID → SALES_ORDER_HDR
- **Generated:** matches fields and nullability; correctly explains FK and dual representation
- **Analysis:** Full alignment with expected.
- **Retrieval:** gt_coverage=1.0, top_score=0.7, gate=proceed

### Q012: How are shipments related to orders and warehouses?
- **Type:** multi_hop | **Difficulty:** medium
- **Verdict:** CORRECT
- **Expected:** SHIPMENT.ORDER_ID references SALES_ORDER_HDR; shipment has source warehouse, tracking, status
- **Generated:** ties order relationship to SHIPMENT.ORDER_ID and warehouse relationship to SHIPMENT.WAREHOUSE_CODE
- **Analysis:** Correct relationships and attribute mentions.
- **Retrieval:** gt_coverage=1.0, top_score=0.7, gate=proceed

### Q013: Can a product belong to multiple categories?
- **Type:** negative | **Difficulty:** easy
- **Verdict:** CORRECTLY_ABSTAINED (answer is correctly “No”, not fabricated)
- **Expected:** No; product belongs to exactly one category (CATEGORY_ID NOT NULL FK)
- **Generated:** explicitly “No” with glossary + FK evidence
- **Analysis:** Correct handling of negative constraint.
- **Retrieval:** gt_coverage=1.0, top_score=0.7, gate=proceed

### Q014: Is it possible for a customer to place an order without payment?
- **Type:** negative | **Difficulty:** medium
- **Verdict:** CORRECTLY_ABSTAINED (answer correctly reasons “Yes” with constraints)
- **Expected:** Yes, order can exist without payment; shipping requires confirmation; PAYMENT_CONFIRMED_AT nullable
- **Generated:** answers “Yes”; explains nullability and lack of NOT-EXISTS payment constraint; distinguishes “place order” vs “ship”
- **Analysis:** Correct negative reasoning; grounded in the provided schema text.
- **Retrieval:** gt_coverage=0.0, top_score=0.7, gate=proceed

### Q015: What schema fields support monetary value tracking across orders and their line items?
- **Type:** multi_hop | **Difficulty:** easy
- **Verdict:** CORRECT
- **Expected:** TOTAL_AMT for header; UNIT_PRICE + QUANTITY + LINE_AMT for lines; linked via ORDER_ID
- **Generated:** describes UNIT_PRICE/LINE_AMT/ORDER_ID linkage; adds PAYMENT.AMOUNT as order-level monetary settlement
- **Analysis:** Matches intent; extra mention of PAYMENT is not harmful and is schema-accurate.
- **Retrieval:** gt_coverage=1.0, top_score=0.7, gate=proceed

---

## Anomalies & Recommendations

### Red Flags
1. **Retrieval coverage anomalies with grounded answers**
   - **Q008:** `gt_coverage=0.0` but answer is correct and grounded.
   - **Q014:** also `gt_coverage=0.0` with correct grounded negative reasoning.
   This suggests either (a) the expected_sources/coverage labeling is incomplete/overly strict, or (b) retrieval quality gating is not tightly aligned with “ground truth coverage” used in evaluation. It’s not a correctness failure, but it weakens metric interpretability.

2. **All questions proceeded (0 abstentions)**
   - On basics, that’s plausible. Still, the evaluation doesn’t test whether the system would abstain on genuinely unanswerable questions in this run.

### Recommendations
- **Audit gt_coverage computation** for Q008 and Q014:
  - verify expected_sources list and whether the retrieved contexts actually contain the required ground-truth evidence under the evaluation’s matching scheme.
- **Add instrumentation to distinguish “retrieved but not counted” vs “not retrieved”**
  - e.g., normalize how table/field mentions map to coverage labels.
- **For negative questions**, consider an explicit “constraint satisfaction” verifier:
  - not just groundedness—ensure the system correctly interprets schema nullability vs business rules (already done here, but can be enforced).

---

## Comparison Notes (if applicable)
- No baseline AB-00 comparison data is included in the bundle, and no `ablation_context` is provided; thus no direct ablation-vs-baseline conclusions can be made for AB-15.

If you want, paste the AB-00 (baseline) bundle for the same dataset and I can score Ablation Impact (Dimension 5) quantitatively and explain the causal effect of the specific toggles.