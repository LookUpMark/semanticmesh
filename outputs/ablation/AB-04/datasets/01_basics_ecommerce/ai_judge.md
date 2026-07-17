# AI-Judge Evaluation: AB-04/01_basics_ecommerce
**Evaluator:** (`gpt-5.4-nano-2026-03-17`) using `docs/AI_JUDGE_PROMPT.md`  
**Date:** 2026-07-17

---

# Ablation Study Evaluation: AB-04 — 01_basics_ecommerce

## Executive Summary
AB-04 performs extremely well on the e-commerce “basics” dataset: all 7 builder tables completed successfully with no Cypher failures or ingestion errors, and all 15 query answers were grounded with perfect `grounded_count=15` and `avg_gt_coverage≈0.98`. Retrieval confidence is strong (`avg_top_score≈0.77`) with no low-retrieval questions flagged, though there is at least one negative-question that looks logically questionable against the provided schema/business rules (Q014) despite remaining “grounded.”

## Scores

| Dimension | Score (1-5) | Weight | Weighted |
|---|---:|---:|---:|
| Builder Quality | 5 | 25% | 1.25 |
| Retrieval Effectiveness | 5 | 25% | 1.25 |
| Answer Quality | 4 | 30% | 1.20 |
| Pipeline Health | 5 | 10% | 0.50 |
| Ablation Impact | N/A | 10% | 0.00 |
| **Overall** |  |  | **4.20** |

## Dimension Analysis

### 1. Builder Quality (5/5)
- `tables_parsed=7`, `tables_completed=7`, `all_tables_completed=true`
- `cypher_failed=false`, `failed_mappings=[]`, `ingestion_errors=[]`
- `triplets_extracted=105` with `entities_resolved=49` (ER appears reasonable; not obviously under/over-extracted)
- No evidence of builder instability (Cypher healing not needed; no failures)

### 2. Retrieval Effectiveness (5/5)
- Query-level retrieval:
  - `grounded_rate=1.0` (all answers grounded)
  - `avg_gt_coverage=0.9833` (ground-truth sources are consistently in the retrieved set)
  - `avg_top_score=0.7738` (healthy reranker confidence for bge-reranker-v2-m3)
- Negative questions:
  - `abstained_count=0`, and `gate_abstentions=0` with no retrieval-quality gate failures
  - On a “basics” dataset this is acceptable, and there were no flagged low-retrieval questions: `questions_with_low_retrieval_score=0`

### 3. Answer Quality (4/5)
Most answers are semantically correct and well-aligned with expected schema facts, including multi-hop relationship modeling and negative constraints.
However, at least one negative question appears to contradict the expected answer’s intended conclusion about “possibility” given business rules, even though the system marked it grounded and did not trigger grader rejection.

**Notable case: Q014**
- Expected: “Yes, an order can exist without payment” (and links this to `PAYMENT_CONFIRMED_AT` being nullable; also discusses shipping eligibility being gated by payment confirmation).
- Generated: “Yes—an order can exist without payment… nothing in physical schema metadata indicates each order must have at least one payment row.”
- This is actually consistent with the *structural* claim (“can exist without payment”), but the expected answer additionally frames it with business-rule context. The generator did not clearly reconcile the “business glossary says orders cannot be shipped until payment is confirmed” portion into an operational statement (i.e., *it can exist*, but *cannot be shipped/fulfilled* until payment is confirmed). This looks like a completeness/interpretation gap rather than a factual hallucination.

Because the rubric emphasizes correctness over wording and the system’s groundedness is perfect, this is best treated as minor completeness loss rather than a major failure—hence 4/5.

### 4. Pipeline Health (5/5)
- `pipeline_health`: `total_grader_rejections=0`, `grader_inconsistencies=0`, `gate_abstentions=0`
- `cypher_failed=false`, `failed_mappings_count=0`, `ingestion_errors_count=0`
- No self-healing or regeneration loops were exercised, but there’s no instability signal.

### 5. Ablation Impact (N/A)
- The bundle is AB-04, but the JSON does not include an `ablation_context` or a “changes_vs_baseline” record, so there’s no explicit causal hypothesis comparison to AB-00 within the provided data.
- Therefore, this dimension is scored as N/A per instructions.

---

## Per-Question Deep Dive

### Q001: What information is stored for each customer?
- **Type:** direct_mapping | **Difficulty:** easy  
- **Verdict:** CORRECT  
- **Expected:** CUST_ID, FULL_NAME, EMAIL (unique), REGION_CODE, CREATED_AT, IS_ACTIVE  
- **Generated:** Maps those CUSTOMER_MASTER / CUSTOMER fields and describes CREATED_AT and IS_ACTIVE; includes customer schema details.  
- **Analysis:** Correct and specific; matches retrieved customer master metadata.  
- **Retrieval:** gt_coverage=1.0, top_score=0.7, gate=proceed  

### Q002: How are products categorized on the platform?
- **Type:** direct_mapping | **Difficulty:** easy  
- **Verdict:** CORRECT  
- **Expected:** TB_PRODUCT has CATEGORY_ID -> TB_CATEGORY; hierarchical via PARENT_CATEGORY_ID  
- **Generated:** CATEGORY_ID FK and TB_CATEGORY self-reference parent category.  
- **Analysis:** Semantically complete with hierarchy detail.  
- **Retrieval:** gt_coverage=1.0, top_score=0.7, gate=proceed  

### Q003: What is the relationship between customers and sales orders?
- **Type:** direct_mapping | **Difficulty:** easy  
- **Verdict:** CORRECT  
- **Expected:** SALES_ORDER_HDR.CUST_ID -> CUSTOMER_MASTER.CUST_ID; customer has zero or more orders  
- **Generated:** States both cardinality and FK relationship.  
- **Analysis:** Fully aligned.  
- **Retrieval:** gt_coverage=1.0, top_score=0.9847, gate=proceed  

### Q004: What does an order line item contain?
- **Type:** direct_mapping | **Difficulty:** easy  
- **Verdict:** CORRECT  
- **Expected:** product, quantity, unit price at time of purchase, extended amount; belongs to exactly one sales order  
- **Generated:** Mentions LINE_ID, ORDER_ID, PRODUCT_ID, QUANTITY, UNIT_PRICE, LINE_AMT.  
- **Analysis:** Matches expected content.  
- **Retrieval:** gt_coverage=1.0, top_score=0.9877, gate=proceed  

### Q005: How are payments linked to orders?
- **Type:** direct_mapping | **Difficulty:** easy  
- **Verdict:** CORRECT  
- **Expected:** PAYMENT.ORDER_ID -> SALES_ORDER_HDR.ORDER_ID; payment method/amount/status/timestamps  
- **Generated:** Explicit FK mapping and business rule.  
- **Analysis:** Correct.  
- **Retrieval:** gt_coverage=1.0, top_score=0.9501, gate=proceed  

### Q006: What statuses can an order have?
- **Type:** attribute_lookup | **Difficulty:** easy  
- **Verdict:** CORRECT  
- **Expected:** PENDING, CONFIRMED, SHIPPED, DELIVERED, CANCELLED  
- **Generated:** Lists exactly those states.  
- **Analysis:** Correct.  
- **Retrieval:** gt_coverage=1.0, top_score=0.7, gate=proceed  

### Q007: Which table stores the product SKU information?
- **Type:** direct_mapping | **Difficulty:** easy  
- **Verdict:** CORRECT  
- **Expected:** TB_PRODUCT.SKU  
- **Generated:** States TB_PRODUCT and TB_PRODUCT.SKU.  
- **Analysis:** Correct.  
- **Retrieval:** gt_coverage=1.0, top_score=0.9842, gate=proceed  

### Q008: How can I find all orders placed by a specific customer?
- **Type:** multi_hop | **Difficulty:** medium  
- **Verdict:** CORRECT  
- **Expected:** Filter SALES_ORDER_HDR by CUST_ID; join to CUSTOMER_MASTER on CUST_ID for customer attributes  
- **Generated:** Provides correct filtering and optional join.  
- **Analysis:** Semantically correct retrieval of join path.  
- **Retrieval:** gt_coverage=1.0, top_score=0.7, gate=proceed  

### Q009: How does the schema link orders to their individual product line items?
- **Type:** multi_hop | **Difficulty:** medium  
- **Verdict:** CORRECT  
- **Expected:** ORDER_LINE_ITEM is junction: ORDER_ID -> SALES_ORDER_HDR; PRODUCT_ID -> TB_PRODUCT; includes QUANTITY, UNIT_PRICE, LINE_AMT  
- **Generated:** Correctly describes ORDER_ID FK linkage and PRODUCT_ID FK.  
- **Analysis:** Correct despite not explicitly mentioning QUANTITY constraint/LINE_AMT constraint; still consistent.  
- **Retrieval:** gt_coverage=1.0, top_score=0.7, gate=proceed  

### Q010: Show me the order hierarchy from customer to line items.
- **Type:** multi_hop | **Difficulty:** medium  
- **Verdict:** CORRECT  
- **Expected:** CUSTOMER_MASTER -> SALES_ORDER_HDR -> ORDER_LINE_ITEM -> TB_PRODUCT  
- **Generated:** Correct hierarchy and FK reasoning; mentions PRODUCT via ORDER_LINE_ITEM.PRODUCT_ID  
- **Analysis:** Correct.  
- **Retrieval:** gt_coverage=0.75, top_score=0.7, gate=proceed  

### Q011: How does the schema model the confirmation state of a payment and its relationship to the order?
- **Type:** multi_hop | **Difficulty:** medium  
- **Verdict:** CORRECT  
- **Expected:** PAYMENT.CONFIRMED_AT and PAYMENT.STATUS_CODE; plus SALES_ORDER_HDR.PAYMENT_CONFIRMED_AT; relationship through PAYMENT.ORDER_ID  
- **Generated:** Covers both timestamp and status code plus order-level confirmation field and “payment must be confirmed before shipment” logic.  
- **Analysis:** Good completeness.  
- **Retrieval:** gt_coverage=1.0, top_score=0.7, gate=proceed  

### Q012: How are shipments related to orders and warehouses?
- **Type:** multi_hop | **Difficulty:** medium  
- **Verdict:** CORRECT  
- **Expected:** SHIPMENT.ORDER_ID -> SALES_ORDER_HDR; warehouse code, tracking, delivery status  
- **Generated:** Explains order linkage and warehouse code/origin concept.  
- **Analysis:** Correct for relational structure; generator mentions shipment origin attribute though not deeply enumerating tracking fields.  
- **Retrieval:** gt_coverage=1.0, top_score=0.7, gate=proceed  

### Q013: Can a product belong to multiple categories?
- **Type:** negative | **Difficulty:** easy  
- **Verdict:** CORRECT  
- **Expected:** No; TB_PRODUCT has single CATEGORY_ID FK to TB_CATEGORY  
- **Generated:** “No” with FK justification and “Belongs to exactly one Category” business rule.  
- **Analysis:** Correct negative handling.  
- **Retrieval:** gt_coverage=1.0, top_score=0.7, gate=proceed  

### Q014: Is it possible for a customer to place an order without payment?
- **Type:** negative | **Difficulty:** medium  
- **Verdict:** PARTIALLY_CORRECT  
- **Expected:** Yes, order can exist without payment because PAYMENT_CONFIRMED_AT is nullable and PAYMENT rows aren’t structurally mandatory; but business rules prevent shipping until payment confirmed.  
- **Generated:** States “Yes—an order can exist without payment” based on nullable PAYMENT_CONFIRMED_AT and absence of “must have payment row” constraint in physical schema metadata; mentions payment-order linkage but does not clearly restate the “cannot ship until payment confirmed” operational consequence.  
- **Analysis:** Structural “can exist” portion matches; missing stronger reconciliation of the business rule consequence reduces completeness for the expected answer’s intent.  
- **Retrieval:** gt_coverage=1.0, top_score=0.7, gate=proceed  

### Q015: What schema fields support monetary value tracking across orders and their line items?
- **Type:** multi_hop | **Difficulty:** easy  
- **Verdict:** CORRECT  
- **Expected:** SALES_ORDER_HDR.TOTAL_AMT; ORDER_LINE_ITEM.UNIT_PRICE, QUANTITY, LINE_AMT; join via ORDER_ID  
- **Generated:** Covers line-level extended amount and also mentions payments and linkage.  
- **Analysis:** Correct; may add extra payment linkage beyond expected, which is not a penalty if grounded.  
- **Retrieval:** gt_coverage=1.0, top_score=0.7, gate=proceed  

---

## Anomalies & Recommendations

### Red Flags
- **Negative-question completeness risk (Q014):** Even with perfect grounding and no grader rejections, the generated response can miss “operational implications” embedded in business rules (e.g., “can’t ship until payment confirmed”). This suggests the hallucination grader is likely checking grounding/claims presence rather than “must include all expected reasoning steps.”

### Recommendations
1. **Tighten negative-question rubric in the grader prompt**: require explicit mention of the business-rule consequence whenever the expected answer includes it (like “no shipping without confirmed payment”).
2. **Add a “business-rule reconciliation” check** for multi-hop negatives: when the generator reasons from nullability/absence of constraints, also require mapping to the relevant business glossary rule(s).
3. **For query-type detection confidence**, consider logging whether the system recognized “negative” and enforced abstain/constraint-consistency more strictly—currently it never abstained in this run (`abstained_count=0`), which can be fine, but for negatives you want explicit correctness on “should be impossible vs possible.”

## Comparison Notes (if applicable)
- No `ablation_context.changes_vs_baseline` was provided, so AB-04 cannot be quantitatively compared to AB-00 within the given bundle.