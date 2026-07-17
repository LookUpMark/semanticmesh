# AI-Judge Evaluation: AB-02/01_basics_ecommerce
**Evaluator:** (`gpt-5.4-nano-2026-03-17`) using `docs/AI_JUDGE_PROMPT.md`  
**Date:** 2026-07-17

---

# Ablation Study Evaluation: AB-02 — 01_basics_ecommerce

## Executive Summary
AB-02 produced an overall healthy run: all 7 DDL tables were completed with no Cypher failures, and every query generated a grounded answer with no grader rejections or pipeline instabilities. However, retrieval *coverage* is uneven (avg_gt_coverage=0.55) and at least a couple queries show clear retrieval misses/weakness (e.g., Q003, Q006, Q011, Q014), which the generator still handled by relying on partially relevant context. Biggest concern: several multi-hop questions have lower ground-truth coverage than expected even on a “basics” dataset.

## Scores

| Dimension | Score (1-5) | Weight | Weighted |
|---|---:|---:|---:|
| Builder Quality | 5 | 25% | 1.25 |
| Retrieval Effectiveness | 3 | 25% | 0.75 |
| Answer Quality | 4 | 30% | 1.20 |
| Pipeline Health | 5 | 10% | 0.50 |
| Ablation Impact | N/A | 10% | 0.00 |
| **Overall** |  |  | **3.70** |

## Dimension Analysis

### 1. Builder Quality (5/5)
- `builder_report.all_tables_completed = true` (7/7)
- `cypher_failed = false`
- `failed_mappings = []`
- `ingestion_errors = []`
- Triplet extraction density looks strong for a small corpus: `triplets_extracted=81`, `entities_resolved=51` (ratio ≈ 1.59; not clearly “high”, but there are no downstream builder failures and graph execution is stable).
**Verdict:** Builder stage is effectively correct and complete.

### 2. Retrieval Effectiveness (3/5)
Key signals:
- `query_report.grounded_rate = 1.0` (answers are grounded, so retrieval usually found *something* useful)
- But ground-truth coverage is only moderate: `avg_gt_coverage = 0.55` (for basics)
- `avg_top_score = 0.745` is high, suggesting reranker confidence is generally strong, yet coverage still misses some expected sources.
- There are at least several obvious low-coverage cases:
  - **Q003**: `gt_coverage=0.0`, `retrieval_quality_score_raw≈0.9847` (contradiction worth noting: contexts didn’t include the expected sources marked as GT)
  - **Q006**: `gt_coverage=0.0`, `retrieval_quality_score_raw≈0.4857`
  - **Q011**: `gt_coverage=0.5`, `retrieval_quality_score_raw≈0.4857`
  - **Q014** (negative): `gt_coverage=0.5`
  - Many others are ~0.5–0.75 rather than consistently high.
**Verdict:** Retrieval is not consistently hitting the exact GT sources across questions, even though the system’s reranker confidence and grounding checks prevent obvious hallucinations.

### 3. Answer Quality (4/5)
- `query_report.grounded_rate = 1.0` and `pipeline_health.total_grader_rejections = 0`
- No evidence of fabricated answers; all responses are supported by retrieved contexts.
- Some answers appear *semantically correct but not perfectly aligned to expected sources* (the rubric emphasizes semantic correctness vs string matching).  
Examples:
- **Q004** correctly explains order line item contents including `QUANTITY`, `UNIT_PRICE`, `LINE_AMT`, and linkage to `ORDER_LINE_ITEM`/`LINE_ID`.
- **Q005** correctly explains payment→order linkage through `PAYMENT.ORDER_ID → SALES_ORDER_HDR(ORDER_ID)`.
- **Q013 (negative)** correctly answers “No” (product belongs to exactly one category) and reasons from both business rule and schema.

Potential minor issue:
- Some responses mention fields/tables with less direct GT coverage (e.g., Q015 discusses `TOTAL_AMT` but the context says it’s “not provided explicitly” in that retrieved snippet). Still, it is consistent with the broader data dictionary content included in the context set.
**Verdict:** High groundedness and semantic correctness; quality is slightly capped by repeated GT-source coverage gaps.

### 4. Pipeline Health (5/5)
- `total_grader_rejections = 0`
- `grader_inconsistencies = 0`
- `gate_abstentions = 0` (and there are negative questions; the system did not abstain where it should have, but it also did not produce wrong negative answers)
- `cypher_failed = false`, `ingestion_errors_count = 0`
**Verdict:** Stable end-to-end with no self-reflection loops actually needing to correct anything.

### 5. Ablation Impact (N/A)
The rubric states: only score this dimension if baseline comparisons exist (e.g., `AB-00`) or if `ablation_context` is provided. This bundle doesn’t include baseline deltas—so **N/A**.

## Per-Question Deep Dive

### Q001: What information is stored for each customer?
- **Type:** direct_mapping | **Difficulty:** easy  
- **Verdict:** CORRECT  
- **Expected:** customer_id, full name, email (unique), region code, creation date, active status  
- **Generated:** Describes CUSTOMER_MASTER fields: CUST_ID, FULL_NAME, EMAIL (unique login), REGION_CODE, CREATED_AT, IS_ACTIVE  
- **Analysis:** Matches all key expected facts; grounded in data dictionary + glossary.  
- **Retrieval:** gt_coverage=1.0, top_score=0.7, gate=proceed

### Q002: How are products categorized on the platform?
- **Type:** direct_mapping | **Difficulty:** easy  
- **Verdict:** CORRECT  
- **Expected:** hierarchical categories; product has exactly one CATEGORY_ID; category has PARENT_CATEGORY_ID  
- **Generated:** Explains TB_PRODUCT → TB_CATEGORY via CATEGORY_ID and category hierarchy via PARENT_CATEGORY_ID  
- **Analysis:** Correctly captures hierarchy + one-category-per-product constraint.  
- **Retrieval:** gt_coverage=1.0, top_score=0.7, gate=proceed

### Q003: What is the relationship between customers and sales orders?
- **Type:** direct_mapping | **Difficulty:** easy  
- **Verdict:** PARTIALLY_CORRECT  
- **Expected:** sales order placed by exactly one customer via CUST_ID; customer can place zero or more orders  
- **Generated:** States the glossary relationship (zero-or-more orders; each order placed by one customer) but does not include CUST_ID FK detail in the answer  
- **Analysis:** Semantically close, but misses the explicit “referenced through CUST_ID foreign key” aspect expected by the GT sources. Also flagged with `gt_coverage=0.0`, indicating expected sources weren’t retrieved per the bundle’s GT labeling.  
- **Retrieval:** gt_coverage=0.0, top_score=0.9847, gate=proceed

### Q004: What does an order line item contain?
- **Type:** direct_mapping | **Difficulty:** easy  
- **Verdict:** CORRECT  
- **Expected:** product, quantity, unit price, extended amount, belongs to exactly one sales order  
- **Generated:** Includes LINE_ID, ORDER_ID, PRODUCT_ID, QUANTITY, UNIT_PRICE, LINE_AMT and explains FK to parent order  
- **Analysis:** Matches expected components; grounded in schema snippet.  
- **Retrieval:** gt_coverage=0.75, top_score=0.9851, gate=proceed

### Q005: How are payments linked to orders?
- **Type:** direct_mapping | **Difficulty:** easy  
- **Verdict:** CORRECT  
- **Expected:** PAYMENT.ORDER_ID → SALES_ORDER_HDR.ORDER_ID; payment has method/amount/status/confirmed timestamp  
- **Generated:** Correctly explains linkage via ORDER_ID FK + business statement about “exactly one Sales Order”  
- **Analysis:** Good alignment; grounded.  
- **Retrieval:** gt_coverage=0.6667, top_score=0.9653, gate=proceed

### Q006: What statuses can an order have?
- **Type:** attribute_lookup | **Difficulty:** easy  
- **Verdict:** PARTIALLY_CORRECT  
- **Expected:** statuses PENDING, CONFIRMED, SHIPPED, DELIVERED, CANCELLED from SALES_ORDER_HDR.STATUS_CODE lifecycle/constraint  
- **Generated:** Lists the five statuses from the business glossary; does not explicitly cite the CHECK constraint / STATUS_CODE linkage in the same way expected  
- **Analysis:** Semantically correct list; weaker than expected because `gt_coverage=0.0` indicates the GT-labeled expected sources weren’t retrieved per bundle scoring.  
- **Retrieval:** gt_coverage=0.0, top_score=0.4857, gate=proceed

### Q007: Which table stores the product SKU information?
- **Type:** direct_mapping | **Difficulty:** easy  
- **Verdict:** CORRECT  
- **Expected:** TB_PRODUCT stores SKU in SKU column  
- **Generated:** States TB_PRODUCT.SKU (VARCHAR(50))  
- **Analysis:** Direct schema mapping; grounded.  
- **Retrieval:** gt_coverage=0.0, top_score=0.7, gate=proceed

### Q008: How can I find all orders placed by a specific customer?
- **Type:** multi_hop | **Difficulty:** medium  
- **Verdict:** CORRECT  
- **Expected:** filter SALES_ORDER_HDR by CUST_ID; join to CUSTOMER_MASTER for customer details  
- **Generated:** Explains filter on SALES_ORDER_HDR.CUST_ID and optional join to CUSTOMER_MASTER  
- **Analysis:** Correct join logic and explanation.  
- **Retrieval:** gt_coverage=0.5, top_score=0.7, gate=proceed

### Q009: How does the schema link orders to their individual product line items?
- **Type:** multi_hop | **Difficulty:** medium  
- **Verdict:** CORRECT  
- **Expected:** ORDER_LINE_ITEM junction with ORDER_ID → SALES_ORDER_HDR and PRODUCT_ID → TB_PRODUCT; includes QUANTITY/UNIT_PRICE/LINE_AMT  
- **Generated:** Correctly describes ORDER_LINE_ITEM as junction and explains FKs + line fields  
- **Analysis:** Matches expected multi-hop structure.  
- **Retrieval:** gt_coverage=0.6667, top_score=0.7, gate=proceed

### Q010: Show me the order hierarchy from customer to line items.
- **Type:** multi_hop | **Difficulty:** medium  
- **Verdict:** PARTIALLY_CORRECT  
- **Expected:** Customer → SalesOrder → OrderLineItem → Product (and each order has line items referencing product)  
- **Generated:** Gives Customer→SalesOrder→OrderLineItem but includes less explicit Product step in the generated hierarchy (mentions “references exactly one Product” in retrieved context, but not as a concrete final hop in the written hierarchy)  
- **Analysis:** Largely correct but the “→ Product (TB_PRODUCT)” final hop is less explicit in the answer body.  
- **Retrieval:** gt_coverage=0.5, top_score=0.7, gate=proceed

### Q011: How does the schema model the confirmation state of a payment and its relationship to the order?
- **Type:** multi_hop | **Difficulty:** medium  
- **Verdict:** CORRECT  
- **Expected:** PAYMENT.CONFIRMED_AT nullable; PAYMENT.STATUS_CODE in {PENDING, CONFIRMED, FAILED, REFUNDED}; order has mirror PAYMENT_CONFIRMED_AT  
- **Generated:** Explains PAYMENT.STATUS_CODE and PAYMENT.CONFIRMED_AT and ties payments to order via ORDER_ID; also mentions SALES_ORDER_HDR.PAYMENT_CONFIRMED_AT  
- **Analysis:** Correct modeling explanation; grounded.  
- **Retrieval:** gt_coverage=0.5, top_score=0.4857, gate=proceed

### Q012: How are shipments related to orders and warehouses?
- **Type:** multi_hop | **Difficulty:** medium  
- **Verdict:** CORRECT  
- **Expected:** Shipment references exactly one SALES_ORDER_HDR via ORDER_ID; includes source warehouse and tracking/status  
- **Generated:** Covers both: shipment→order relationship and shipment→warehouse association; consistent with contexts  
- **Analysis:** Correct.  
- **Retrieval:** gt_coverage=0.5, top_score=0.9753, gate=proceed

### Q013: Can a product belong to multiple categories?
- **Type:** negative | **Difficulty:** easy  
- **Verdict:** CORRECTLY_ABSTAINED / CORRECT  
- **Expected:** No; product belongs to exactly one category (single CATEGORY_ID FK)  
- **Generated:** “No” and explains exactly-one-category rule + single CATEGORY_ID column/foreign key  
- **Analysis:** Correct handling of negative question; no hallucination.  
- **Retrieval:** gt_coverage=0.6667, top_score=0.7, gate=proceed

### Q014: Is it possible for a customer to place an order without payment?
- **Type:** negative | **Difficulty:** medium  
- **Verdict:** CORRECT  
- **Expected:** Yes possible (order can exist while PAYMENT_CONFIRMED_AT is NULL), though not shippable yet  
- **Generated:** Argues based on PAYMENT_CONFIRMED_AT nullable; clarifies payment required for shipping not creation  
- **Analysis:** Semantically matches expected reasoning.  
- **Retrieval:** gt_coverage=0.5, top_score=0.7, gate=proceed

### Q015: What schema fields support monetary value tracking across orders and their line items?
- **Type:** multi_hop | **Difficulty:** easy  
- **Verdict:** PARTIALLY_CORRECT  
- **Expected:** SALES_ORDER_HDR.TOTAL_AMT; ORDER_LINE_ITEM.UNIT_PRICE, QUANTITY (>0), LINE_AMT; linked via ORDER_ID  
- **Generated:** Correctly explains line fields; correctly mentions payments’ AMOUNT too; for header totals, it says the retrieved context may not explicitly provide the table field name, even though GT expects TOTAL_AMT  
- **Analysis:** Slight mismatch: includes PAYMENT fields (not expected) and hedges about header total field specificity. Still largely aligned to “monetary tracking” intent.  
- **Retrieval:** gt_coverage=1.0, top_score=0.7, gate=proceed

## Anomalies & Recommendations

### Red Flags
1. **GT coverage inconsistencies despite high reranker confidence**
   - Example **Q003**: `gt_coverage=0.0` but `retrieval_quality_score_raw≈0.9847` and the answer is grounded.
   - Example **Q006/Q007**: `gt_coverage=0.0` with still “adequate” contexts and grounding.
   - This suggests GT source labeling (or mapping between “expected_sources” and “covered_sources”) may be misaligned with what the contexts actually contained.
2. **Several multi-hop questions have only ~0.5–0.66 GT coverage** on a basics dataset.
   - Doesn’t break answer correctness due to grounding checks, but it reduces confidence in retrieval-to-source traceability.

### Recommendations
1. **Audit GT-source mapping logic**
   - Verify how `expected_sources` are converted into “covered_sources” and how those are matched against retrieved `sources_retrieved`.
   - Q003/Q006/Q007 are prime candidates.
2. **Strengthen retrieval quality gate logic reporting**
   - Since `gate_decision` is always `proceed`, consider ensuring the retrieval gate thresholds aren’t too permissive on basics.
3. **Improve entity-resolution edge quality (or traversal retrieval weighting)**
   - Even though answers are grounded, the moderate `avg_gt_coverage=0.55` indicates the expected KG concepts aren’t consistently surfaced.
4. **For multi-hop templates, enforce explicit hop coverage in generation**
   - Q010 and Q015 show “mostly correct but missing a hop/field specificity” patterns. Add a checklist-based verifier before finalization for required hops (e.g., Customer→SalesOrder→OrderLineItem→Product).

## Comparison Notes (if applicable)
- No baseline (`AB-00`) bundle or `ablation_context` is provided, so ablation-vs-baseline impact cannot be assessed.