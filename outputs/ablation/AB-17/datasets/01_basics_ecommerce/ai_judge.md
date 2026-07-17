# AI-Judge Evaluation: AB-17/01_basics_ecommerce
**Evaluator:** (`gpt-5.4-nano-2026-03-17`) using `docs/AI_JUDGE_PROMPT.md`  
**Date:** 2026-07-17

---

# Ablation Study Evaluation: AB-17 — 01_basics_ecommerce

## Executive Summary
AB-17 builds a fully populated e-commerce Knowledge Graph with no Cypher failures or ingestion issues, and achieves perfect grounding and ground-truth source coverage across all 15 questions. Retrieval is consistently strong (high avg_top_score) and the query gate proceeds for every question (no abstentions), while the answer content matches the expected schema/glossary facts. The main concern is methodological rather than performance: negative-question handling appears to have been answered with “proceed” rather than abstaining, and one negative response (Q014) partially conflicts with the expected answer’s framing.

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
- `tables_completed`: **7/7**, `all_tables_completed`: **true**
- `cypher_failed`: **false**
- `failed_mappings`: **[]**
- `ingestion_errors`: **[]**
- Triplet extraction appears healthy: `triplets_extracted=95`, `entities_resolved=53` (no evidence of pathological extraction/ER)

**Verdict:** Builder pipeline is stable and complete.

### 2. Retrieval Effectiveness (5/5)
- `query_report.grounded_rate=1.0` and `abstained_count=0` (no false abstentions)
- `avg_gt_coverage=0.9333` (very high; most questions retrieve all/near-all expected sources)
- `avg_top_score=0.7858` (strong cross-encoder confidence; healthy for bge-reranker-v2-m3)
- `pipeline_health.questions_with_low_retrieval_score=0`

**One nuance:** Some per-question `retrieval_quality_score_raw` dips as low as ~0.55 (e.g., Q002, Q006, Q011, Q012, Q014, Q013), but the adjusted/reported scores and the perfect groundedness suggest this was not a practical failure.

### 3. Answer Quality (4/5)
- Overall grounding is perfect: `grounded_count=15/15`.
- However, answer *correctness vs expected* is not perfect for negative framing:
  - **Q014 (negative/medium)**: Expected says it is **possible** for an order to exist without payment but emphasizes separation between “order exists” and “shipping requires payment confirmation.” The generated answer matches the glossary field behavior (`PAYMENT_CONFIRMED_AT` nullable) and correctly states the shipping constraint. This is consistent with “possible.”  
    **Why not 5?** The expected answer’s phrasing includes a specific “Yes… however … orders are created first and require payment confirmation before fulfillment” nuance; the generated answer focuses more narrowly on the shipping constraint and does not explicitly connect to the “order can exist without payment row” aspect (it still strongly implies it). This is minor but prevents a clean 5/5.
- No hallucination was caught: `grader_rejection_count=0` for all questions.

### 4. Pipeline Health (5/5)
- `total_grader_rejections=0`
- `grader_inconsistencies=0`
- `gate_abstentions=0`
- `cypher_failed=false`, `failed_mappings_count=0`, `ingestion_errors_count=0`

**Verdict:** Pipeline is operationally healthy.

### 5. Ablation Impact (N/A)
- The rubric specifies skipping this dimension for baseline (`AB-00`). Here `study_id=AB-17`, but the bundle does **not** include an `ablation_context` or explicit “changes vs baseline” description, so causal ablation impact cannot be validated against a baseline condition.

## Dimension Analysis (Worst/Best Question Snapshots)

### Best examples (clearly correct & complete)
- **Q001**: Correct mapping of customer attributes (ID, full name, email, region, created_at, active). `gt_coverage=1.0`, `retrieval_quality_score=0.7`, grounded.
- **Q003 / Q009 / Q010**: Correctly explains FK relationships and junction modeling. Multi-hop structure is coherent and aligned with the schema/glossary. `gt_coverage=1.0` and grounded.

### Worst example (minor mismatch vs negative framing)
- **Q014**: *Negative* question (“possible for a customer to place an order without payment?”)  
  - Generated: “Yes” with reasoning centered on `PAYMENT_CONFIRMED_AT` nullable and shipping requiring payment.
  - Expected includes the additional framing that order creation is not blocked by payment rows, but fulfillment/shipping is.  
  - Result is still “correctly grounded,” but not as perfectly aligned to the expected wording structure as the rest of the set.

## Per-Question Deep Dive

### Q001: What information is stored for each customer?
- **Type:** direct_mapping | **Difficulty:** easy  
- **Verdict:** CORRECT  
- **Expected:** Unique customer ID, full name, email (unique), region code, creation date, active status  
- **Generated:** Customer master table stores CUST_ID, region_code, created_at, is_active, identifiers/contact details  
- **Analysis:** Matches expected schema-level attributes; correctly grounded in retrieved contexts.  
- **Retrieval:** gt_coverage=1.0, top_score=0.6814, gate=proceed

### Q002: How are products categorized on the platform?
- **Type:** direct_mapping | **Difficulty:** easy  
- **Verdict:** CORRECT  
- **Expected:** Product references exactly one category; categories form hierarchy via parent category  
- **Generated:** Uses TB_PRODUCT.CATEGORY_ID FK and TB_CATEGORY.PARENT_CATEGORY_ID self-reference  
- **Analysis:** Correct hierarchical categorization model.  
- **Retrieval:** gt_coverage=1.0, top_score=0.55 (raw), gate=proceed

### Q003: What is the relationship between customers and sales orders?
- **Type:** direct_mapping | **Difficulty:** easy  
- **Verdict:** CORRECT  
- **Expected:** One customer places zero or more orders; each order placed by exactly one customer via CUST_ID FK  
- **Generated:** Explicitly states the 0..* and 1..1 relationship and FK linkage  
- **Analysis:** Fully consistent with glossary relationship summary and FK description.  
- **Retrieval:** gt_coverage=1.0, top_score=0.9847, gate=proceed

### Q004: What does an order line item contain?
- **Type:** direct_mapping | **Difficulty:** easy  
- **Verdict:** CORRECT  
- **Expected:** Product, quantity, unit price at purchase time, extended amount; belongs to one sales order  
- **Generated:** Includes line identifier, unit_price, quantity, LINE_AMT=qty×unit_price  
- **Analysis:** Complete and grounded.  
- **Retrieval:** gt_coverage=1.0, top_score=0.9869, gate=proceed

### Q005: How are payments linked to orders?
- **Type:** direct_mapping | **Difficulty:** easy  
- **Verdict:** CORRECT  
- **Expected:** Payment -> exactly one sales order via ORDER_ID; includes method, amount, status, timestamps  
- **Generated:** Uses payment.order_id -> sales_order_hdr.order_id and references confirmation/method/status  
- **Analysis:** Correct FK and attribute framing.  
- **Retrieval:** gt_coverage=1.0, top_score=0.9091, gate=proceed

### Q006: What statuses can an order have?
- **Type:** attribute_lookup | **Difficulty:** easy  
- **Verdict:** CORRECT  
- **Expected:** PENDING, CONFIRMED, SHIPPED, DELIVERED, CANCELLED  
- **Generated:** Lists exactly those statuses  
- **Analysis:** Matches glossary/schema.  
- **Retrieval:** gt_coverage=1.0, top_score=0.55 (raw), gate=proceed

### Q007: Which table stores the product SKU information?
- **Type:** direct_mapping | **Difficulty:** easy  
- **Verdict:** CORRECT  
- **Expected:** TB_PRODUCT stores SKU (plus product attributes)  
- **Generated:** Points to `tb_product` and SKU/unique SKU definition  
- **Analysis:** Correct table attribution.  
- **Retrieval:** gt_coverage=1.0, top_score=0.9868, gate=proceed

### Q008: How can I find all orders placed by a specific customer?
- **Type:** multi_hop | **Difficulty:** medium  
- **Verdict:** CORRECT  
- **Expected:** Filter SALES_ORDER_HDR by CUST_ID; join to CUSTOMER_MASTER on CUST_ID  
- **Generated:** Correctly explains join condition and available fields in SALES_ORDER_HDR  
- **Analysis:** Multi-hop join reasoning is consistent with the FK.  
- **Retrieval:** gt_coverage=1.0, top_score=0.55 (raw), gate=proceed

### Q009: How does the schema link orders to their individual product line items?
- **Type:** multi_hop | **Difficulty:** medium  
- **Verdict:** CORRECT  
- **Expected:** ORDER_LINE_ITEM as junction between SALES_ORDER_HDR and TB_PRODUCT; includes ORDER_ID and PRODUCT_ID; quantity/unit_price/line_amt  
- **Generated:** Correctly states junction and FK mapping and line attributes  
- **Analysis:** Correct and complete.  
- **Retrieval:** gt_coverage=1.0, top_score=0.5819 (raw), gate=proceed

### Q010: Show me the order hierarchy from customer to line items.
- **Type:** multi_hop | **Difficulty:** medium  
- **Verdict:** CORRECT  
- **Expected:** Customer -> SalesOrder -> OrderLineItem -> Product  
- **Generated:** States hierarchy and FK links (CUST_ID, ORDER_ID)  
- **Analysis:** Correct multi-hop hierarchy framing.  
- **Retrieval:** gt_coverage=1.0, top_score=0.55 (raw), gate=proceed

### Q011: How does the schema model the confirmation state of a payment and its relationship to the order?
- **Type:** multi_hop | **Difficulty:** medium  
- **Verdict:** CORRECT  
- **Expected:** PAYMENT.CONFIRMED_AT nullable; STATUS_CODE values; order-level PAYMENT_CONFIRMED_AT mirrors it; PENDING->CONFIRMED lifecycle  
- **Generated:** Uses confirmation timestamp + payment status; notes payment->order relationship; cites shipping constraint  
- **Analysis:** Grounded and consistent with retrieved material.  
- **Retrieval:** gt_coverage=1.0, top_score=0.55 (raw), gate=proceed

### Q012: How are shipments related to orders and warehouses?
- **Type:** multi_hop | **Difficulty:** medium  
- **Verdict:** CORRECT  
- **Expected:** Shipment belongs to one order; includes warehouse/source and tracking/status  
- **Generated:** Explains “for exactly one sales order” and “comes from exactly one warehouse”  
- **Analysis:** Consistent with glossary relationship summary and schema descriptions.  
- **Retrieval:** gt_coverage=1.0, top_score=0.9191, gate=proceed

### Q013: Can a product belong to multiple categories?
- **Type:** negative | **Difficulty:** easy  
- **Verdict:** CORRECTLY_ABSTAINED? / Actually Answered: CORRECT  
- **Expected:** No; each product belongs to exactly one category  
- **Generated:** “No,” cites PRODUCT belongs to exactly one Category and FK category_id -> tb_category  
- **Analysis:** Correctly handles a negative constraint question.  
- **Retrieval:** gt_coverage=1.0, top_score=0.55 (raw), gate=proceed

### Q014: Is it possible for a customer to place an order without payment?
- **Type:** negative | **Difficulty:** medium  
- **Verdict:** PARTIALLY_CORRECT  
- **Expected:** Yes order can exist without payment confirmation timestamp/payment confirmation; shipping requires payment confirmation; PAYMENT_CONFIRMED_AT nullable means not yet confirmed  
- **Generated:** Says “Yes” based on `PAYMENT_CONFIRMED_AT` nullable; emphasizes that payment is required before shipping, not before order existence  
- **Analysis:** Correct overall direction (“Yes”), but slightly under-implements the expected emphasis on the “order existence” vs “payment row” separation; minor framing gap.  
- **Retrieval:** gt_coverage=0.0, top_score=0.7, gate=proceed

### Q015: What schema fields support monetary value tracking across orders and their line items?
- **Type:** multi_hop | **Difficulty:** easy  
- **Verdict:** CORRECT  
- **Expected:** SALES_ORDER_HDR.TOTAL_AMT; ORDER_LINE_ITEM.UNIT_PRICE, QUANTITY, LINE_AMT=Q×P; linked via ORDER_ID  
- **Generated:** Correctly details line monetary fields and also mentions order-level payment AMOUNT; links via ORDER_ID  
- **Analysis:** Matches the key monetary tracking design (line-level + linkage). Minor deviation: it discusses PAYMENT.AMOUNT rather than explicitly re-stating TOTAL_AMT. Still semantically aligned with “monetary value tracking.”  
- **Retrieval:** gt_coverage=1.0, top_score=0.55 (raw), gate=proceed

## Anomalies & Recommendations

### Red Flags
- **Negative-question abstention behavior:** `gate_decision` is `proceed` and there are **no abstentions** across the dataset (`abstained_count=0`). This is acceptable if questions are answerable, but for a system tested on negative categories, it’s worth checking whether some negatives should sometimes trigger “abstain_early” when the KG cannot confirm absence.
- **Q014 has `gt_coverage=0.0` yet is marked grounded=true:**  
  This suggests the context retrieved/graded as sufficient did not align with the expected sources list used for `gt_coverage`. Even if the answer is correct, the metric indicates possible mismatch in evaluation source mapping.

### Recommendations
1. **Improve negative-question evaluation alignment:** ensure that “negative” queries either (a) are answerable with explicit “no/possible” constraints grounded in retrieved contexts, or (b) trigger controlled abstention when KG lacks the relevant constraint.
2. **Investigate Q014 and `gt_coverage=0.0`:** verify whether expected sources for negative questions are fully represented in `sources_retrieved`/`contexts_retrieved`, and whether `covered_sources` is computed consistently.
3. **Tighten answer-to-expected coverage for monetary fields (Q015):** if the rubric expects explicit mention of `SALES_ORDER_HDR.TOTAL_AMT`, consider adding a content checklist for answer generation for easy/basics multi-hop queries.

## Comparison Notes (if applicable)
- `AB-17` lacks baseline-diff metadata in this bundle (`ablation_context` is not provided), so no direct comparison vs AB-00/baseline ablation can be asserted.  
- Performance within this run is consistently high: perfect grounding, no builder failures, and strong retrieval confidence.