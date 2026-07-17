# AI-Judge Evaluation: AB-03/01_basics_ecommerce
**Evaluator:** (`gpt-5.4-nano-2026-03-17`) using `docs/AI_JUDGE_PROMPT.md`  
**Date:** 2026-07-17

---

# Ablation Study Evaluation: AB-03 — 01_basics_ecommerce

## Executive Summary
AB-03 shows a fully successful end-to-end run on a “basics” e-commerce dataset: all 7 builder tables completed with no Cypher or ingestion failures, and all 15 questions were answered with grounded outputs (grounded_rate = 1.0) with the retrieval gate always proceeding. The only notable weakness is a likely business-logic overreach on negative questions (Q014), where the system infers “order can exist without payment” without clearly demonstrating that this is explicitly allowed by schema constraints—though the run contains no grader rejections.

## Scores

| Dimension | Score (1-5) | Weight | Weighted |
|---|---:|---:|---:|
| Builder Quality | 5 | 25% | 1.25 |
| Retrieval Effectiveness | 5 | 25% | 1.25 |
| Answer Quality | 4 | 30% | 1.20 |
| Pipeline Health | 5 | 10% | 0.50 |
| Ablation Impact | 4 | 10% | 0.40 |
| **Overall** |  |  | **4.60** |

## Dimension Analysis

### 1. Builder Quality (5/5)
- `tables_parsed=7`, `tables_completed=7`, `all_tables_completed=true`
- `cypher_failed=false`
- `failed_mappings=[]`, `ingestion_errors=[]`
- Triplet extraction is healthy: `triplets_extracted=117` (for basics/ecommerce this is strong)
- No evidence of builder instability or missing graph construction components.

### 2. Retrieval Effectiveness (5/5)
- Query report is ideal:
  - `grounded_rate=1.0`, `abstained_count=0`
  - `avg_gt_coverage=1.0` across all questions
  - `avg_top_score≈0.70` (healthy confidence for a cross-encoder reranker; note reranker was disabled, but the top-score metric still looks strong)
- `pipeline_health.questions_with_low_retrieval_score=0`
- Negative questions were not abstained (gate always `proceed`), but that’s not penalized as retrieval effectiveness per se—only if answers were wrong (handled in Answer Quality).

### 3. Answer Quality (4/5)
Overall grounded and semantically aligned with expected answers for the majority of questions.
- **Strong performance:** All 15 questions are marked `grounded=true` and `grader_rejection_count=0`.
- **Main concern (negative logic / schema permissibility):**
  - **Q014** (“Is it possible for a customer to place an order without payment?”) is the only place where the system’s inference looks weaker than the expected answer.
    - Expected: acknowledges that payments may be absent before confirmation but frames it around `PAYMENT_CONFIRMED_AT` being nullable and schema allowing the order to exist prior to payment confirmation.
    - Generated: says “Yes” but argues that the schema/business context does *not explicitly* prevent order placement without a payment row, and it leans on the business flow (“has one or more Payments” as a “typical business flow” rather than a constraint). This is plausible, but less directly supported than the expected rationale.
- Even with that, there are no grader rejections, and the answer still matches the expected “Yes” outcome, so this is a mild downgrade rather than a failure.

### 4. Pipeline Health (5/5)
- `cypher_failed=false`
- `total_grader_rejections=0`
- `grader_inconsistencies=0`
- `gate_abstentions=0`
- `builder_report.ingestion_errors=[]`
- Latency indicators are effectively zero in the bundle (`elapsed_s: 0`)—not enough detail to assess performance, but no operational errors occurred.

### 5. Ablation Impact (4/5)
Study AB-03 indicates ablation settings versus baseline, but the bundle does **not** include an explicit `ablation_context.changes_vs_baseline`. From `config`:
- `enable_reranker=false` (reranker disabled)
- `retrieval_mode=hybrid`
- No explicit flags for critic validation / hallucination grader / cypher healing are provided here (so we cannot attribute improvements/declines to those specifically).
Observed effect: despite reranker being off, retrieval confidence (`avg_top_score≈0.70`) and GT coverage are perfect. This suggests either the dataset is sufficiently “easy/basics” or hybrid retrieval + graph structure is doing most of the work.
- Because causal attribution is incomplete (baseline unknown), score is not 5, but results are clearly not degraded.

## Per-Question Deep Dive

### Q001: What information is stored for each customer?
- **Type:** direct_mapping | **Difficulty:** easy
- **Verdict:** CORRECT
- **Expected:** ID, full name, email (unique), region code, creation date, active status
- **Generated:** Maps all those fields to `CUSTOMER_MASTER` columns; includes the “active” and created timestamp.
- **Analysis:** Correct semantic coverage; grounded in retrieved schema/glossary.
- **Retrieval:** gt_coverage=1.0, top_score=0.7, gate=proceed

### Q002: How are products categorized on the platform?
- **Type:** direct_mapping | **Difficulty:** easy
- **Verdict:** CORRECT
- **Expected:** product references exactly one category via `CATEGORY_ID`; category hierarchy exists
- **Generated:** Explains category assignment via `TB_PRODUCT.CATEGORY_ID` and “belongs to exactly one Category”.
- **Analysis:** Matches expected category mechanism; no missing key constraint.
- **Retrieval:** gt_coverage=1.0, top_score=0.7, gate=proceed

### Q003: What is the relationship between customers and sales orders?
- **Type:** direct_mapping | **Difficulty:** easy
- **Verdict:** CORRECT
- **Expected:** one customer places zero or more orders; each order placed by exactly one customer via `CUST_ID`
- **Generated:** Uses glossary + FK `SALES_ORDER_HDR.CUST_ID` → `CUSTOMER_MASTER.CUST_ID`.
- **Analysis:** Correct.
- **Retrieval:** gt_coverage=1.0, top_score=0.7, gate=proceed

### Q004: What does an order line item contain?
- **Type:** direct_mapping | **Difficulty:** easy
- **Verdict:** CORRECT
- **Expected:** product, quantity, unit price at purchase time, extended amount; belongs to exactly one order
- **Generated:** Includes unique line id and extended amount = quantity × unit price; tied to `ORDER_LINE_ITEM`.
- **Analysis:** Correct and complete.
- **Retrieval:** gt_coverage=1.0, top_score=0.7, gate=proceed

### Q005: How are payments linked to orders?
- **Type:** direct_mapping | **Difficulty:** easy
- **Verdict:** CORRECT
- **Expected:** payment has exactly one sales order via `PAYMENT.ORDER_ID`; includes method/status/confirmed timestamp
- **Generated:** Links via FK on `PAYMENT.ORDER_ID`; mentions confirmation timestamp.
- **Analysis:** Correct.
- **Retrieval:** gt_coverage=1.0, top_score=0.7, gate=proceed

### Q006: What statuses can an order have?
- **Type:** attribute_lookup | **Difficulty:** easy
- **Verdict:** CORRECT
- **Expected:** PENDING, CONFIRMED, SHIPPED, DELIVERED, CANCELLED (from `SALES_ORDER_HDR.STATUS_CODE`)
- **Generated:** Lists exactly those statuses.
- **Analysis:** Correct.
- **Retrieval:** gt_coverage=1.0, top_score=0.7, gate=proceed

### Q007: Which table stores the product SKU information?
- **Type:** direct_mapping | **Difficulty:** easy
- **Verdict:** CORRECT
- **Expected:** `TB_PRODUCT` with `TB_PRODUCT.SKU`
- **Generated:** Correct.
- **Analysis:** Correct.
- **Retrieval:** gt_coverage=1.0, top_score=0.7, gate=proceed

### Q008: How can I find all orders placed by a specific customer?
- **Type:** multi_hop | **Difficulty:** medium
- **Verdict:** CORRECT
- **Expected:** query `SALES_ORDER_HDR` filtering by `CUST_ID`; join to `CUSTOMER_MASTER` as needed
- **Generated:** Explains `SALES_ORDER_HDR.CUST_ID` and optional join to identify customer attributes.
- **Analysis:** Correct join logic.
- **Retrieval:** gt_coverage=1.0, top_score=0.7, gate=proceed

### Q009: How does the schema link orders to their individual product line items?
- **Type:** multi_hop | **Difficulty:** medium
- **Verdict:** CORRECT
- **Expected:** junction `ORDER_LINE_ITEM` links `SALES_ORDER_HDR` and `TB_PRODUCT` via FK IDs; includes qty/unit price/line amt
- **Generated:** States `ORDER_LINE_ITEM` is within orders and references product via `ORDER_LINE_ITEM.PRODUCT_ID`; mentions qty and extended amount.
- **Analysis:** Correct.
- **Retrieval:** gt_coverage=1.0, top_score=0.7, gate=proceed

### Q010: Show me the order hierarchy from customer to line items.
- **Type:** multi_hop | **Difficulty:** medium
- **Verdict:** CORRECT
- **Expected:** Customer → SalesOrder → OrderLineItem → Product
- **Generated:** Correct foreign-key and membership explanation (`CUST_ID` then `ORDER_LINE_ITEM.ORDER_ID`).
- **Analysis:** Correct.
- **Retrieval:** gt_coverage=1.0, top_score=0.7, gate=proceed

### Q011: How does the schema model the confirmation state of a payment and its relationship to the order?
- **Type:** multi_hop | **Difficulty:** medium
- **Verdict:** CORRECT
- **Expected:** `PAYMENT.CONFIRMED_AT` nullable + status codes; order mirrors via `SALES_ORDER_HDR.PAYMENT_CONFIRMED_AT`; order lifecycle via `STATUS_CODE`
- **Generated:** Explains payment status and confirmation timestamp; includes order-header `PAYMENT_CONFIRMED_AT` and relationship “payment for exactly one sales order”.
- **Analysis:** Correct.
- **Retrieval:** gt_coverage=1.0, top_score=0.7, gate=proceed

### Q012: How are shipments related to orders and warehouses?
- **Type:** multi_hop | **Difficulty:** medium
- **Verdict:** CORRECT
- **Expected:** `SHIPMENT.ORDER_ID` → `SALES_ORDER_HDR`; includes warehouse origin, tracking/status
- **Generated:** Correctly describes `SHIPMENT.ORDER_ID` and `SHIPMENT.WAREHOUSE_CODE` as source warehouse.
- **Analysis:** Correct.
- **Retrieval:** gt_coverage=1.0, top_score=0.7, gate=proceed

### Q013: Can a product belong to multiple categories?
- **Type:** negative | **Difficulty:** easy
- **Verdict:** CORRECT
- **Expected:** No; exactly one category; `TB_PRODUCT.CATEGORY_ID` is single NOT NULL FK
- **Generated:** “No” and cites single category FK + NOT NULL.
- **Analysis:** Correct negative handling.
- **Retrieval:** gt_coverage=1.0, top_score=0.7, gate=proceed

### Q014: Is it possible for a customer to place an order without payment?
- **Type:** negative | **Difficulty:** medium
- **Verdict:** PARTIALLY_CORRECT
- **Expected:** Yes—orders can exist before payment confirmation; `SALES_ORDER_HDR.PAYMENT_CONFIRMED_AT` is nullable; business rule delays shipping until payment confirmed
- **Generated:** Says “Yes” and cites that payment confirmation timestamp is nullable and that the context says payment must be confirmed before shipping. However, it also argues that “has one or more payments” is a typical flow rather than an explicit constraint, which is less directly schema-grounded than the expected rationale.
- **Analysis:** Final answer matches expected (“Yes”), but the justification is slightly more inferential than desired for a negative/constraint question.
- **Retrieval:** gt_coverage=1.0, top_score=0.7, gate=proceed

### Q015: What schema fields support monetary value tracking across orders and their line items?
- **Type:** multi_hop | **Difficulty:** easy
- **Verdict:** CORRECT
- **Expected:** `SALES_ORDER_HDR.TOTAL_AMT`; line-level `UNIT_PRICE`, `QUANTITY`, `LINE_AMT=QTY×UNIT_PRICE`; linked by `ORDER_ID`
- **Generated:** Correctly covers line-level fields (`UNIT_PRICE`, `QUANTITY`, `LINE_AMT`). For header total amount, it mentions “total amount” conceptually and does not explicitly cite `TOTAL_AMT` as the column name from contexts shown.
- **Analysis:** Largely correct; minor omission of explicit column name in the generated rationale, but consistent with overall intent and marked grounded.
- **Retrieval:** gt_coverage=1.0, top_score=0.7, gate=proceed

## Anomalies & Recommendations

### Red Flags
- **Negative-question justification weakness (Q014):** The answer is correct in conclusion, but reasoning leans on “not explicitly prevented” rather than clearly deriving it from constraints/nullable fields that map to the expected explanation.
- **Q015 minor specificity gap:** generated response does not explicitly name `SALES_ORDER_HDR.TOTAL_AMT` even though expected answer does—suggests the model may under-cite exact column names when the concept is present.

### Recommendations
1. **Tighten constraint-grounding for negative questions:** When `query_type=negative`, require explicit reference to (a) nullable indicators like `PAYMENT_CONFIRMED_AT` and (b) any absence/presence of NOT NULL or FK existence constraints for payment rows before asserting “order without payment is possible”.
2. **Add “exact-field citation” behavior for attribute lookup questions:** If expected sources include specific columns (e.g., `TOTAL_AMT`), encourage the generator to explicitly name the column in the response.
3. **Ablation tracking:** Include `ablation_context.changes_vs_baseline` in future bundles so Ablation Impact can be scored with stronger causal evidence.

## Comparison Notes (if applicable)
- AB-03 is not AB-00 and no baseline delta (`ablation_context`) is provided in the bundle, so direct comparison to baseline behavior cannot be quantitatively validated.
- Despite `enable_reranker=false`, retrieval and groundedness are excellent, indicating the hybrid + graph-derived signals are sufficient for this basics dataset.

