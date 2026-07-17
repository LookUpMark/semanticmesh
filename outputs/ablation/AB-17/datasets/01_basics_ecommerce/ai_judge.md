# AI-Judge Evaluation: AB-17/01_basics_ecommerce
**Evaluator:** (`gpt-5.4-nano-2026-03-17`) using `docs/AI_JUDGE_PROMPT.md`  
**Date:** 2026-07-17

---

# Ablation Study Evaluation: AB-17 — 01_basics_ecommerce

## Executive Summary
AB-17 shows an excellent end-to-end run on the E-Commerce “basics” dataset: all 7 builder tables completed with no Cypher failures or ingestion errors, and the query layer achieved 100% grounded answers with high average GT source coverage (0.917) and strong reranker confidence (avg top score ≈ 0.786). The only notable concern is a **negative question** (Q014) where the pipeline answered “Yes” but the bundle’s own grading metadata marks it as grounded while `gt_coverage=0`, indicating a possible **retrieval/context mismatch** or **gap in negative-question handling logic**.

## Scores

| Dimension | Score (1-5) | Weight | Weighted |
|---|---:|---:|---:|
| Builder Quality | 5 | 25% | 1.25 |
| Retrieval Effectiveness | 4 | 25% | 1.00 |
| Answer Quality | 4 | 30% | 1.20 |
| Pipeline Health | 5 | 10% | 0.50 |
| Ablation Impact | N/A | 10% | 0.00 |
| **Overall** |  |  | **3.95** |

## Dimension Analysis

### 1. Builder Quality (5/5)
- `tables_parsed=7`, `tables_completed=7`, `all_tables_completed=true`
- `cypher_failed=false`, `failed_mappings=[]`, `ingestion_errors=[]`
- Triplet density looks healthy at a qualitative level: `triplets_extracted=91` over `entities_resolved=69` suggests reasonable extraction/ER balance for a small dataset.
**Conclusion:** Builder Graph was fully successful and produced a consistent KG.

### 2. Retrieval Effectiveness (4/5)
- `grounded_rate=1.0` and `avg_gt_coverage=0.9167` are strong.
- `avg_top_score=0.7863` indicates the reranker found semantically correct top results confidently (consistent with bge-reranker-v2 behavior).
- However, **Q014** has `gt_coverage=0.0` while still being marked `grounded=true` and `gate_decision="proceed"`. That combination is unusual: it implies either
  - the retrieved contexts did not actually include the expected sources for the answer, or
  - the “negative” expectation was not represented in retrieved contexts but the system still decided it could answer.
- Still, overall retrieval health is excellent: `questions_with_low_retrieval_score=0` and `pipeline_health.gate_abstentions=0`.

**Conclusion:** Retrieval is mostly very good, with one clear outlier affecting effectiveness for negative reasoning.

### 3. Answer Quality (4/5)
- `query_report.grounded_rate=1.0` across all 15 questions.
- For the *positive/direct/multi-hop* questions (e.g., Q001, Q002, Q003, Q004, Q005, Q006, Q007, Q008–Q012, Q015), generated answers precisely reflect the schema/glossary constraints and relationships. No grader rejections (`grader_rejection_count` is 0 for shown questions).
- **Q014 (negative)** is the main concern:
  - Expected: “Yes, an order can exist without payment” is essentially about whether the schema allows orders without payment rows; additionally, the expected explanation ties to nullable `PAYMENT_CONFIRMED_AT` and optional payment row presence.
  - Generated: “Yes—based on the schema, an order can exist without payment confirmation timestamp is nullable,” which is aligned with the *first part* of expected.
  - Yet Q014 has `gt_coverage=0.0` and `covered_sources=[]`, meaning the system’s explanation may not have used the expected grounding sources.
  
Given the rubric priority (“semantic correctness > string matching”) you might still rate Q014 as correct, but the retrieval metadata signals an internal inconsistency: the system shouldn’t be confident about a negative/conditional claim while retrieving nothing from the expected sources.

**Conclusion:** Mostly correct and well-grounded, but the negative-question outlier suggests a need to tighten gate/grounding criteria when `expected_sources` are empty/not retrieved.

### 4. Pipeline Health (5/5)
- `total_grader_rejections=0`
- `grader_inconsistencies=0`
- `gate_abstentions=0`
- `cypher_failed=false`, `failed_mappings_count=0`, `ingestion_errors_count=0`
**Conclusion:** Stable run; self-reflection loops were not exercised because no errors were produced.

### 5. Ablation Impact (N/A)
- The provided bundle does not include an “AB-00 baseline” comparison block nor an `ablation_context.changes_vs_baseline`.
- So the ablation impact dimension cannot be validated as causal.

## Dimension Analysis (quick highlights by best/worst questions)

### Best questions (high-confidence, full coverage)
- **Q003**: `gt_coverage=1.0`, retrieval_quality_score_raw not shown but `retrieval_quality_score≈0.985`; answer mirrors FK relationship and cardinality.
- **Q006**: statuses list matches glossary; `gt_coverage=1.0`.
- **Q007**: SKU stored in `TB_PRODUCT.SKU`; `gt_coverage=1.0`.

### Worst / outlier questions
- **Q014** (negative): `gt_coverage=0.0`, `covered_sources=[]`, `gate_decision=proceed`, yet `grounded=true`.
  - This is the strongest red flag in the bundle because it indicates either:
    - the expected sources weren’t retrieved at all, or
    - the scoring/grading pipeline marked the answer grounded despite missing expected-context linkage.

## Per-Question Deep Dive

### Q001: What information is stored for each customer?
- **Type:** direct_mapping | **Difficulty:** easy
- **Verdict:** CORRECT
- **Expected:** unique customer ID, full name, email (unique), region code, creation date, active status
- **Generated:** matches fields and types in `CUSTOMER_MASTER` (CUST_ID, FULL_NAME, EMAIL, REGION_CODE, CREATED_AT, IS_ACTIVE) and notes uniqueness via PK
- **Analysis:** Perfect alignment with expected schema/glossary content.
- **Retrieval:** gt_coverage=1.0, top_score=0.7, gate=proceed

### Q002: How are products categorized on the platform?
- **Type:** direct_mapping | **Difficulty:** easy
- **Verdict:** CORRECT
- **Expected:** product → exactly one category via CATEGORY_ID; categories have parent for hierarchy
- **Generated:** includes CATEGORY_ID FK to TB_CATEGORY and hierarchy via PARENT_CATEGORY_ID
- **Analysis:** Correct cardinality and hierarchy.
- **Retrieval:** gt_coverage=1.0, top_score=0.7, gate=proceed

### Q003: What is the relationship between customers and sales orders?
- **Type:** direct_mapping | **Difficulty:** easy
- **Verdict:** CORRECT
- **Expected:** one customer places zero or more orders; each order belongs to exactly one customer
- **Generated:** matches FK `SALES_ORDER_HDR.CUST_ID -> CUSTOMER_MASTER.CUST_ID`
- **Analysis:** Correct.
- **Retrieval:** gt_coverage=1.0, top_score=0.9847, gate=proceed

### Q004: What does an order line item contain?
- **Type:** direct_mapping | **Difficulty:** easy
- **Verdict:** CORRECT
- **Expected:** product, quantity, unit price at purchase, extended/line amount; belongs to one order
- **Generated:** lists LINE_ID, ORDER_ID, PRODUCT_ID, QUANTITY, UNIT_PRICE, LINE_AMT
- **Analysis:** Correct.
- **Retrieval:** gt_coverage=1.0, top_score=0.9711, gate=proceed

### Q005: How are payments linked to orders?
- **Type:** direct_mapping | **Difficulty:** easy
- **Verdict:** CORRECT
- **Expected:** payment linked via ORDER_ID FK to SALES_ORDER_HDR; payment captures method/amount/status/timestamps
- **Generated:** matches FK and relationship summary
- **Analysis:** Correct.
- **Retrieval:** gt_coverage=1.0, top_score=0.9588, gate=proceed

### Q006: What statuses can an order have?
- **Type:** attribute_lookup | **Difficulty:** easy
- **Verdict:** CORRECT
- **Expected:** PENDING, CONFIRMED, SHIPPED, DELIVERED, CANCELLED (CHECK constraint + glossary)
- **Generated:** lists exactly those statuses
- **Analysis:** Correct.
- **Retrieval:** gt_coverage=1.0, top_score=0.7, gate=proceed

### Q007: Which table stores the product SKU information?
- **Type:** direct_mapping | **Difficulty:** easy
- **Verdict:** CORRECT
- **Expected:** TB_PRODUCT stores SKU in TB_PRODUCT.SKU
- **Generated:** states TB_PRODUCT.SKU; mentions additional column context
- **Analysis:** Correct.
- **Retrieval:** gt_coverage=1.0, top_score=0.9747, gate=proceed

### Q008: How can I find all orders placed by a specific customer?
- **Type:** multi_hop | **Difficulty:** medium
- **Verdict:** CORRECT
- **Expected:** filter SALES_ORDER_HDR by CUST_ID and join on CUSTOMER_MASTER.CUST_ID
- **Generated:** matches join and lists order attributes
- **Analysis:** Correct multi-hop logic.
- **Retrieval:** gt_coverage=1.0, top_score=0.7, gate=proceed

### Q009: How does the schema link orders to their individual product line items?
- **Type:** multi_hop | **Difficulty:** medium
- **Verdict:** CORRECT
- **Expected:** ORDER_LINE_ITEM is junction; has ORDER_ID FK to SALES_ORDER_HDR and PRODUCT_ID FK to TB_PRODUCT; also QUANTITY, UNIT_PRICE, LINE_AMT
- **Generated:** focuses on ORDER_ID foreign key to SALES_ORDER_HDR (does not explicitly mention PRODUCT_ID FK in the shown generated answer)
- **Analysis:** Still consistent with expected relationship, though slightly under-specified on PRODUCT_ID/line economics in the response text; overall grounded by contexts.
- **Retrieval:** gt_coverage=1.0, top_score=0.7, gate=proceed

### Q010: Show me the order hierarchy from customer to line items.
- **Type:** multi_hop | **Difficulty:** medium
- **Verdict:** CORRECT
- **Expected:** CUSTOMER_MASTER → SALES_ORDER_HDR → ORDER_LINE_ITEM → TB_PRODUCT
- **Generated:** describes join chain via CUST_ID and ORDER_ID and notes line item belongs to product
- **Analysis:** Correct hierarchy description.
- **Retrieval:** gt_coverage=0.75, top_score=0.7, gate=proceed

### Q011: How does the schema model the confirmation state of a payment and its relationship to the order?
- **Type:** multi_hop | **Difficulty:** medium
- **Verdict:** CORRECT
- **Expected:** PAYMENT.CONFIRMED_AT nullable + PAYMENT.STATUS_CODE lifecycle; SALES_ORDER_HDR.PAYMENT_CONFIRMED_AT mirrors; order lifecycle via STATUS_CODE
- **Generated:** captures PAYMENT.CONFIRMED_AT, PAYMENT.STATUS_CODE values, and links PAYMENT.ORDER_ID to SALES_ORDER_HDR
- **Analysis:** Correct, though expected explicitly mentions mirrored order-level field; generated response focuses on payment fields + link.
- **Retrieval:** gt_coverage=1.0, top_score=0.7, gate=proceed

### Q012: How are shipments related to orders and warehouses?
- **Type:** multi_hop | **Difficulty:** medium
- **Verdict:** CORRECT
- **Expected:** shipment has ORDER_ID FK to sales order; includes warehouse code, tracking, status
- **Generated:** matches ORDER_ID relation and SHIPMENT.WAREHOUSE_CODE linkage and “comes from exactly one Warehouse”
- **Analysis:** Correct.
- **Retrieval:** gt_coverage=1.0, top_score=0.9059, gate=proceed

### Q013: Can a product belong to multiple categories?
- **Type:** negative | **Difficulty:** easy
- **Verdict:** CORRECT
- **Expected:** No; TB_PRODUCT has single CATEGORY_ID FK to TB_CATEGORY
- **Generated:** explicitly says “No” with glossary + FK support
- **Analysis:** Correct negative handling.
- **Retrieval:** gt_coverage=1.0, top_score=0.7, gate=proceed

### Q014: Is it possible for a customer to place an order without payment?
- **Type:** negative | **Difficulty:** medium
- **Verdict:** PARTIALLY_CORRECT (metadata inconsistency)
- **Expected:** order can exist without payment confirmation because PAYMENT_CONFIRMED_AT is nullable; payment links via ORDER_ID; shipping requires payment confirmation
- **Generated:** says “Yes” because PAYMENT_CONFIRMED_AT nullable; discusses shipping rules as about shipping, not order creation
- **Analysis:** Semantically aligned with the “can exist without payment confirmation” premise, but **bundle shows `gt_coverage=0` and `covered_sources=[]`**, meaning the expected supporting sources were not retrieved/credited. This undermines confidence in the grounding mechanism for negative questions.
- **Retrieval:** gt_coverage=0.0, top_score=0.7, gate=proceed

### Q015: What schema fields support monetary value tracking across orders and their line items?
- **Type:** multi_hop | **Difficulty:** easy
- **Verdict:** CORRECT
- **Expected:** SALES_ORDER_HDR.TOTAL_AMT; ORDER_LINE_ITEM UNIT_PRICE, QUANTITY, LINE_AMT; linked via ORDER_ID
- **Generated:** mentions line-level UNIT_PRICE and LINE_AMT, and order-level payment amount via PAYMENT.AMOUNT; describes key FKs connecting line items to orders
- **Analysis:** Correct about line-level economics; includes an extra (and possibly different) monetary source (PAYMENT.AMOUNT). That’s not wrong, but the expected asked specifically about TOTAL_AMT and reconciliation with header totals—generated answer may be slightly off-target there.
- **Retrieval:** gt_coverage=1.0, top_score=0.7, gate=proceed

## Anomalies & Recommendations

### Red Flags
1. **Q014 (negative) has `gt_coverage=0.0` and empty `covered_sources`, yet `grounded=true` and `gate_decision=proceed`.**
   - This suggests the grounding checker (or GT coverage calculation) is not tightly coupled to “expected sources” for negative questions.
2. **Q010 has `gt_coverage=0.75`** despite being judged correct—likely acceptable, but indicates some hierarchy evidence wasn’t fully captured by GT matching.

### Recommendations
- **Tighten negative-question grounding:** for `query_type="negative"`, require retrieval coverage overlap with expected sources or require explicit “negation-safe” justification templates (e.g., cite nullable fields/constraints and their meaning, not just business rules).
- **Audit grounding vs GT coverage mismatch:** ensure that `grounded=true` implies verifiable claims appear in the retrieved contexts that map to `expected_sources` (or revise the notion of groundedness to align with the system’s KG-grounding objective).
- **Improve response targeting (Q015):** align answer with expected “TOTAL_AMT + line economics” instead of emphasizing PAYMENT.AMOUNT unless asked.
- **Expand multi-hop coverage in text (Q009/Q011):** include both sides of junction links (e.g., ORDER_LINE_ITEM to TB_PRODUCT via PRODUCT_ID) when the question asks for full linkage.

## Comparison Notes (if applicable)
- Not applicable: AB-17 bundle does not include `changes_vs_baseline` or indicate which ablation flags differ from AB-00, so causal comparison cannot be performed per rubric.