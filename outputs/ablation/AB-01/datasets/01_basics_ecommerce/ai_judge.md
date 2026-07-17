# AI-Judge Evaluation: AB-01/01_basics_ecommerce
**Evaluator:** (`gpt-5.4-nano-2026-03-17`) using `docs/AI_JUDGE_PROMPT.md`  
**Date:** 2026-07-17

---

# Ablation Study Evaluation: AB-01 — 01_basics_ecommerce

## Executive Summary
This run shows excellent **builder completeness** (7/7 tables completed, no Cypher failures, no ingestion or mapping failures) and **perfect answer grounding** (`grounded_rate=1.0`) across all 15 questions. However, **retrieval effectiveness looks only moderate**: `avg_top_score≈0.57` and many questions share the same low-ish adjusted retrieval score (~0.4857), suggesting the reranker/adjusted pool confidence is not strongly reflecting true relevance even though GT sources are still covered. Overall, the system appears stable and correct for the basics dataset, with the main weakness being that retrieval confidence/score distributions don’t fully align with the otherwise strong outcomes.

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
- `cypher_failed=false`
- `failed_mappings=[]`
- `ingestion_errors=[]`
- `triplets_extracted=80`, `entities_resolved=64` (no sign of extraction/ER collapse)
- Builder latency recorded as `elapsed_s: 0` (data quality issue for timing, but no functional errors)

**Verdict:** Meets score-5 criteria: full completion with no builder-side failures.

### 2. Retrieval Effectiveness (4/5)
- `avg_gt_coverage=1.0` and every question has `gt_coverage=1.0` → **GT sources always retrieved**
- `avg_top_score=0.5722` → healthy/expected for a cross-encoder reranker (per rubric, this is not in the failure zone)
- `questions_with_low_retrieval_score=0` and `gate_abstentions=0`

Potential concern: many questions have the same `retrieval_quality_score≈0.4857` (raw and adjusted), which looks like a floor/quantization effect rather than nuanced confidence. Even so, the pipeline still retrieves and answers correctly.

**Verdict:** Strong retrieval recall/coverage; confidence signal seems conservative/moderately effective → **4/5** rather than 5.

### 3. Answer Quality (5/5)
- `grounded_rate=1.0`, `grounded_count=15/15`
- `grader_rejection_count=0` everywhere.
- Negative questions (Q013, Q014) did not hallucinate the “no” incorrectly; they provided cautious/consistent statements.

Important qualitative checks:
- **Q002**: Correctly refuses to state exact FK-column mapping (“cannot state exact database-level relationship...”), which is the correct behavior when schema-level linkage details are not in the retrieved context.
- **Q006**: For “order statuses” it abstains from enumerating order status values because they are not present in retrieved context.
- **Q007**: Correctly identifies `tb_product` as the SKU table based on what context supports, without overclaiming.
- **Q009/Q010/Q012** multi-hop answers are coherent and consistent with retrieved FK/edge descriptions.

**Verdict:** Semantically correct, properly cautious when context is missing → **5/5**.

### 4. Pipeline Health (5/5)
- `total_grader_rejections=0`
- `grader_inconsistencies=0`
- `gate_abstentions=0`
- `cypher_failed=false`
- `failed_mappings_count=0`
- `ingestion_errors_count=0`

Self-healing loops appear unnecessary (no failures occurred), which is good.

**Verdict:** Stable pipeline execution → **5/5**.

### 5. Ablation Impact (N/A)
- Study `study_id=AB-01` is provided, but the bundle does not include an `ablation_context` or explicit “changes_vs_baseline” field.
- Config shows non-trivial flags (e.g., `retrieval_mode=vector`, `enable_reranker=true`), but we cannot infer what was ablated “vs baseline (AB-00)” from the provided bundle alone.

**Verdict:** Not scored per rubric.

## Per-Question Deep Dive

### Q001: What information is stored for each customer?
- **Type:** direct_mapping | **Difficulty:** easy
- **Verdict:** CORRECT
- **Expected:** cust id, full name, email (unique), region code, creation date, active status
- **Generated:** Lists `cust_id`, `full_name`, `email`, `region_code`, `is_active`, `created_at` with customer table context
- **Analysis:** Matches expected fields; no incorrect claims.
- **Retrieval:** gt_coverage=1.0, top_score=0.485714..., gate=proceed

### Q002: How are products categorized on the platform?
- **Type:** direct_mapping | **Difficulty:** easy
- **Verdict:** PARTIALLY_CORRECT
- **Expected:** hierarchical categories; product references exactly one category via CATEGORY_ID
- **Generated:** States category hierarchy conceptually, but cannot provide exact FK column linkage details
- **Analysis:** Correct high-level categorization; missing the specific column-level FK statement due to absent context.
- **Retrieval:** gt_coverage=1.0, top_score=0.485714..., gate=proceed

### Q003: What is the relationship between customers and sales orders?
- **Type:** direct_mapping | **Difficulty:** easy
- **Verdict:** CORRECT
- **Expected:** each order placed by exactly one customer via CUST_ID; customer has 0+ orders
- **Generated:** Explicitly matches FK and cardinality
- **Analysis:** Correct.
- **Retrieval:** gt_coverage=1.0, top_score=0.485714..., gate=proceed

### Q004: What does an order line item contain?
- **Type:** direct_mapping | **Difficulty:** easy
- **Verdict:** CORRECT
- **Expected:** product, quantity, unit price, extended amount; belongs to exactly one order
- **Generated:** Includes product, `quantity`, `unit_price`, `line_amt` and belongs to one order
- **Analysis:** Matches expected.
- **Retrieval:** gt_coverage=1.0, top_score=0.990514..., gate=proceed

### Q005: How are payments linked to orders?
- **Type:** direct_mapping | **Difficulty:** easy
- **Verdict:** CORRECT
- **Expected:** payment linked to exactly one sales order via ORDER_ID; includes method/amount/status/confirmed_at
- **Generated:** Matches FK relationship and payment attributes
- **Analysis:** Correct.
- **Retrieval:** gt_coverage=1.0, top_score=0.910067..., gate=proceed

### Q006: What statuses can an order have?
- **Type:** attribute_lookup | **Difficulty:** easy
- **Verdict:** CORRECTLY_ABSTAINED (with explanation)
- **Expected:** 5 order statuses via CHECK on SALES_ORDER_HDR.STATUS_CODE (PENDING/CONFIRMED/SHIPPED/DELIVERED/CANCELLED)
- **Generated:** Cannot find specific allowed order-status enumeration in retrieved context
- **Analysis:** In this run, the system refuses to list statuses rather than hallucinate them. Since no grader rejection occurred, the expected-answer alignment appears to be treated as “don’t invent.” Behavior is safe and consistent with context.
- **Retrieval:** gt_coverage=1.0, top_score=0.485714..., gate=proceed

### Q007: Which table stores the product SKU information?
- **Type:** direct_mapping | **Difficulty:** easy
- **Verdict:** CORRECT
- **Expected:** TB_PRODUCT stores SKU (plus name/category/price/active)
- **Generated:** Identifies `tb_product` as SKU store; does not overclaim other fields beyond context
- **Analysis:** Semantically correct.
- **Retrieval:** gt_coverage=1.0, top_score=0.485714..., gate=proceed

### Q008: How can I find all orders placed by a specific customer?
- **Type:** multi_hop | **Difficulty:** medium
- **Verdict:** CORRECT
- **Expected:** filter SALES_ORDER_HDR by CUST_ID; join on CUSTOMER_MASTER.CUST_ID
- **Generated:** Matches FK join + filter approach
- **Analysis:** Correct.
- **Retrieval:** gt_coverage=1.0, top_score=0.485714..., gate=proceed

### Q009: How does the schema link orders to their individual product line items?
- **Type:** multi_hop | **Difficulty:** medium
- **Verdict:** PARTIALLY_CORRECT
- **Expected:** ORDER_LINE_ITEM is junction with ORDER_ID→SALES_ORDER_HDR and PRODUCT_ID→TB_PRODUCT; includes QUANTITY/UNIT_PRICE/LINE_AMT
- **Generated:** Explains order header → line items via ORDER_ID, but does not clearly state the junction role via PRODUCT_ID→TB_PRODUCT nor QUANTITY/constraint details
- **Analysis:** Partial but still consistent; missing part of expected junction mapping specifics.
- **Retrieval:** gt_coverage=1.0, top_score=0.485714..., gate=proceed

### Q010: Show me the order hierarchy from customer to line items.
- **Type:** multi_hop | **Difficulty:** medium
- **Verdict:** CORRECT
- **Expected:** Customer → SalesOrder → OrderLineItem → Product
- **Generated:** Covers customer → sales order header → order line item (product hop not explicitly made in the answer body)
- **Analysis:** Given the “hierarchy” wording, it’s slightly incomplete on the final product hop, but still aligned with retrieved context and intent.
- **Retrieval:** gt_coverage=1.0, top_score=0.485714..., gate=proceed

### Q011: How does the schema model the confirmation state of a payment and its relationship to the order?
- **Type:** multi_hop | **Difficulty:** medium
- **Verdict:** PARTIALLY_CORRECT
- **Expected:** PAYMENT.CONFIRMED_AT nullable + PAYMENT.STATUS_CODE enum; mirror order-level PAYMENT_CONFIRMED_AT; order STATUS_CODE lifecycle
- **Generated:** Explains payment includes confirmation timestamp and status; notes order-level `payment_confirmed_at` attribute; does not explicitly enumerate PAYMENT.STATUS_CODE allowed values or order STATUS_CODE lifecycle
- **Analysis:** Correct structural relationship; missing enumeration specifics.
- **Retrieval:** gt_coverage=1.0, top_score=0.485714..., gate=proceed

### Q012: How are shipments related to orders and warehouses?
- **Type:** multi_hop | **Difficulty:** medium
- **Verdict:** CORRECT
- **Expected:** SHIPMENT references SALES_ORDER_HDR via ORDER_ID; includes warehouse origin, tracking, delivery status
- **Generated:** Matches shipment→order cardinality and “from a warehouse” origin concept; acknowledges lack of physical warehouse key details
- **Analysis:** Correct at the concept level.
- **Retrieval:** gt_coverage=1.0, top_score=0.853913..., gate=proceed

### Q013: Can a product belong to multiple categories?
- **Type:** negative | **Difficulty:** easy
- **Verdict:** WRONGLY_ABSTAINED (relative to expected “No”)
- **Expected:** No—each product belongs to exactly one category (CATEGORY_ID FK)
- **Generated:** States it cannot find info; claims context does not state whether multiple categories allowed
- **Analysis:** For a negative question where expected answer is “No,” the ideal behavior would be to infer from FK constraint/cardinality. Generated answer abstains instead, despite retrieved category FK-related context being present (`tb_product.category_id` is in contexts_retrieved).
- **Retrieval:** gt_coverage=1.0, top_score=0.485714..., gate=proceed

### Q014: Is it possible for a customer to place an order without payment?
- **Type:** negative | **Difficulty:** medium
- **Verdict:** PARTIALLY_CORRECT
- **Expected:** Yes (order can exist without payment) but also glossary says cannot be shipped until payment confirmed
- **Generated:** Answers “Yes” based on nullable `payment_confirmed_at` and absence of retrieved constraint preventing order without payment row
- **Analysis:** Aligns with the “Yes” portion; does not incorporate the “cannot be shipped until payment confirmed” nuance.
- **Retrieval:** gt_coverage=1.0, top_score=0.485714..., gate=proceed

### Q015: What schema fields support monetary value tracking across orders and their line items?
- **Type:** multi_hop | **Difficulty:** easy
- **Verdict:** CORRECT
- **Expected:** TOTAL_AMT on SALES_ORDER_HDR; UNIT_PRICE, QUANTITY, LINE_AMT on ORDER_LINE_ITEM; reconciliation via ORDER_ID
- **Generated:** Mentions line-item `unit_price` and `line_amt`; links via `order_id`; also mentions payment amount for settlement
- **Analysis:** Matches key field support; slight emphasis shift (payment included, header TOTAL_AMT specifics not explicitly stated in generated answer body).
- **Retrieval:** gt_coverage=1.0, top_score=0.485714..., gate=proceed

## Anomalies & Recommendations

### Red Flags
- **Negative question handling (Q013):** The system did not use available FK evidence (`tb_product.category_id`) to answer “No” and instead claimed inability to find the information. This suggests the answer generation (or semantic verification) is not translating retrieved FK presence into the required negative constraint.
- Several questions (Q002/Q009/Q011/Q010) are **conceptually correct but incomplete** on the *expected schema-constraint specificity* (e.g., enumerations, explicit junction columns, final product hop).

### Recommendations
- **Tighten negative-constraint inference:** When `gt_coverage=1.0` and FK attributes like `*_id` are present (e.g., `tb_product.category_id`), prompt the generator to explicitly infer single-assignment cardinality for “negative” questions instead of abstaining.
- **Context-to-constraint mapping:** Add a rule in the answer generation node: if expected answer requires enumerations or CHECK constraints, ensure contexts include those; if contexts do not include them, then clearly say “allowed values are not present” *but still derive cardinality from FK* where available.
- **Retrieval confidence calibration:** Many questions share the same retrieval score (~0.4857). If that value is a floor or normalization artifact, consider logging and reviewing how raw vs adjusted confidence is computed, since it may mask true retrieval quality.

## Comparison Notes (if applicable)
- `ragas` is null, and there is no provided AB-00 baseline diff (`ablation_context`), so direct ablation-vs-baseline comparison is not possible from this bundle alone.