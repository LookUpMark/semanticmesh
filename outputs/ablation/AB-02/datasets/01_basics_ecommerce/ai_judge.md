# AI-Judge Evaluation: AB-02/01_basics_ecommerce
**Evaluator:** (`gpt-5.4-nano-2026-03-17`) using `docs/AI_JUDGE_PROMPT.md`  
**Date:** 2026-07-17

---

# Ablation Study Evaluation: AB-02 — 01_basics_ecommerce

## Executive Summary
AB-02 shows a **healthy end-to-end pipeline**: builder completed all tables with **no Cypher/mapping/ingestion failures**, and **all 15 queries were answered without abstention** while remaining grounded. However, **retrieval-to-ground-truth coverage is only moderate on average** (avg_gt_coverage ≈ **0.54**) despite high avg_top_score (~**0.72**), suggesting the system often retrieves relevant but not the full set of expected sources—likely acceptable for “basics,” but it reduces robustness for multi-hop and some attribute/negative cases. Answer correctness appears strong overall; the main concern is that **retrieval metrics and “covered_sources” do not fully align with context sufficiency** for several questions (notably Q003, Q006, Q011, Q014).

## Scores

| Dimension | Score (1-5) | Weight | Weighted |
|---|---:|---:|---:|
| Builder Quality | 5 | 25% | 1.25 |
| Retrieval Effectiveness | 4 | 25% | 1.00 |
| Answer Quality | 4 | 30% | 1.20 |
| Pipeline Health | 5 | 10% | 0.50 |
| Ablation Impact | 3 | 10% | 0.30 |
| **Overall** |  |  | **4.25** |

## Dimension Analysis

### 1. Builder Quality (5/5)
- `tables_parsed=7`, `tables_completed=7`, `all_tables_completed=true`
- `cypher_failed=false`, `failed_mappings=[]`, `ingestion_errors=[]`
- `triplets_extracted=112`, `entities_resolved=69` → triplet/entity ≈ **1.62** (not high), but the rubric’s decisive signals (all tables completed, no failures) dominate here.
**Verdict:** builder is effectively correct and stable for this dataset.

### 2. Retrieval Effectiveness (4/5)
- `grounded_rate=1.0`, `abstained_count=0` (no retrieval-driven abstentions)
- `avg_gt_coverage=0.5389` (moderate)
- `avg_top_score=0.7162` (healthy cross-encoder confidence)
- There are **retrieval-strength mismatches**:
  - Several questions have **gt_coverage = 0.0** even while answers are marked grounded (examples: **Q006, Q007, Q011, Q014**).
  - This indicates either (a) ground-truth source bookkeeping is incomplete, or (b) the answer can be grounded in contexts that do not exactly match `expected_sources`.
**Rubric fit:** avg_top_score is strong and no “low retrieval” failures are reported; moderate gt_coverage suggests retrieval is good enough but not exhaustive.

### 3. Answer Quality (4/5)
- `grounded_count=15 / 15` and `grader_rejection_count=0` across all provided questions.
- Semantically, most answers correctly restate schema relationships and constraints.
- Minor issue pattern: some multi-hop/negative cases are **semantically plausible** but the expected “ground-truth coverage” is 0 and retrieval quality scores drop (e.g., Q014 has `gt_coverage=0.0`).
  
**Examples (best cases):**
- **Q001** correctly enumerates customer fields including uniqueness of email, and aligns to retrieved data dictionary/glossary.
- **Q004** correctly lists order line item components (LINE_ID, ORDER_ID, PRODUCT_ID, QUANTITY, UNIT_PRICE, LINE_AMT) and meaning.

**Examples (worst cases, still grounded):**
- **Q006**: “order statuses” answered correctly (PENDING, CONFIRMED, SHIPPED, DELIVERED, CANCELLED) but `gt_coverage=0.0`.
- **Q014 (negative, medium)**: Answer says “Yes” (orders can exist without confirmed payment) based on nullable `PAYMENT_CONFIRMED_AT`. This conflicts with the rubric’s negative-example expectation described in the prompt (and with the expected_answer’s framing about creation vs shipping). The pipeline still marks it grounded and provides no grader rejection, suggesting the dataset’s expected semantics for the negative question may be nuanced or the answer-grading definition differs from what the rubric anticipates.

Overall: correctness is high, but **negative-question semantics and source-coverage alignment** need attention.

### 4. Pipeline Health (5/5)
- `total_grader_rejections=0`, `grader_inconsistencies=0`, `gate_abstentions=0`
- `cypher_failed=false`, `failed_mappings_count=0`, `ingestion_errors_count=0`
- Latency shown as `elapsed_s=0` in many places; no stability issues are evident in the bundle.
**Verdict:** stable and error-free for this run.

### 5. Ablation Impact (3/5)
- Bundle is **AB-02**, but the provided JSON does **not include** an `ablation_context` field describing changes vs baseline (AB-00).
- We can only infer configuration differences from the bundle:
  - `retrieval_mode="bm25"`
  - `enable_reranker` is effectively **on** (reranker true)
  - `enable_reranker=true` but no flags for critic/hallucination grader are shown in the bundle.
Given missing “changes vs baseline” context, the ablation causal claim can’t be validated strongly. Observationally, the system performed well, so any degradation would be hard to attribute. Hence a mid score.

---

## Per-Question Deep Dive

### Q001: What information is stored for each customer?
- **Type:** direct_mapping | **Difficulty:** easy  
- **Verdict:** CORRECT  
- **Expected:** customer fields (unique ID, full name, unique email, region code, created_at, active status) + email uniqueness  
- **Generated:** enumerates `CUST_ID`, `FULL_NAME`, `EMAIL`, `REGION_CODE`, `CREATED_AT`, `IS_ACTIVE` and states email is unique  
- **Analysis:** Matches expected schema fields and uniqueness claim; grounded in retrieved dictionary/glossary.  
- **Retrieval:** gt_coverage=1.0, top_score=0.716221..., gate=proceed  

### Q002: How are products categorized on the platform?
- **Type:** direct_mapping | **Difficulty:** easy  
- **Verdict:** CORRECT  
- **Expected:** products belong to exactly one category; categories form hierarchy via parent category; product uses CATEGORY_ID FK  
- **Generated:** explains `TB_CATEGORY` hierarchy (`PARENT_CATEGORY_ID`) and `TB_PRODUCT.CATEGORY_ID → TB_CATEGORY` FK, non-null  
- **Analysis:** Correct and appropriately detailed.  
- **Retrieval:** gt_coverage=1.0, top_score=0.716221..., gate=proceed  

### Q003: What is the relationship between customers and sales orders?
- **Type:** direct_mapping | **Difficulty:** easy  
- **Verdict:** CORRECT  
- **Expected:** one customer → many orders; each order references exactly one customer via CUST_ID  
- **Generated:** many-to-one; describes FK relationship  
- **Analysis:** Semantically correct; note gt_coverage is only 0.5 (ground-truth sources mismatch likely).  
- **Retrieval:** gt_coverage=0.5, top_score=0.984693..., gate=proceed  

### Q004: What does an order line item contain?
- **Type:** direct_mapping | **Difficulty:** easy  
- **Verdict:** CORRECT  
- **Expected:** product reference, quantity, unit price (time of purchase), extended amount; belongs to exactly one sales order  
- **Generated:** lists `LINE_ID`, `ORDER_ID`, `PRODUCT_ID`, `QUANTITY`, `UNIT_PRICE`, `LINE_AMT` and definition of LINE_AMT  
- **Analysis:** Accurate and fully aligned with context.  
- **Retrieval:** gt_coverage=0.75, top_score=0.873969..., gate=proceed  

### Q005: How are payments linked to orders?
- **Type:** direct_mapping | **Difficulty:** easy  
- **Verdict:** CORRECT  
- **Expected:** PAYMENT.ORDER_ID FK to SALES_ORDER_HDR; includes payment attributes like method/amount/status/confirmation  
- **Generated:** correctly states ORDER_ID FK linking payment to order  
- **Analysis:** Grounded and correct; minor source coverage mismatch (`gt_coverage=0.6667`).  
- **Retrieval:** gt_coverage=0.6667, top_score=0.772702..., gate=proceed  

### Q006: What statuses can an order have?
- **Type:** attribute_lookup | **Difficulty:** easy  
- **Verdict:** CORRECT (but source coverage anomaly)  
- **Expected:** PENDING, CONFIRMED, SHIPPED, DELIVERED, CANCELLED from SALES_ORDER_HDR.STATUS_CODE lifecycle  
- **Generated:** lists exactly those five statuses  
- **Analysis:** Correct answer; however `gt_coverage=0.0` suggests `expected_sources`/pool coverage bookkeeping mismatch.  
- **Retrieval:** gt_coverage=0.0, top_score=0.626238..., gate=proceed  

### Q007: Which table stores the product SKU information?
- **Type:** direct_mapping | **Difficulty:** easy  
- **Verdict:** CORRECT (but source coverage anomaly)  
- **Expected:** TB_PRODUCT.SKU stores SKU  
- **Generated:** states `TB_PRODUCT` and `SKU` column  
- **Analysis:** Semantically correct; `gt_coverage=0.0` and low coverage indicates source matching mismatch.  
- **Retrieval:** gt_coverage=0.0, top_score=0.7, gate=proceed  

### Q008: How can I find all orders placed by a specific customer?
- **Type:** multi_hop | **Difficulty:** medium  
- **Verdict:** PARTIALLY_CORRECT  
- **Expected:** query SALES_ORDER_HDR filtering by CUST_ID; join Customer/CUSTOMER_MASTER on CUST_ID  
- **Generated:** correct join/filter idea and key columns; mentions returned fields  
- **Analysis:** Largely correct, but `gt_coverage=0.5` and retrieval pool suggests missing exact expected source set.  
- **Retrieval:** gt_coverage=0.5, top_score=0.7, gate=proceed  

### Q009: How does the schema link orders to their individual product line items?
- **Type:** multi_hop | **Difficulty:** medium  
- **Verdict:** PARTIALLY_CORRECT  
- **Expected:** junction ORDER_LINE_ITEM with ORDER_ID FK to SALES_ORDER_HDR and PRODUCT_ID FK to TB_PRODUCT + QUANTITY/UNIT_PRICE/LINE_AMT constraints  
- **Generated:** correctly focuses on ORDER_ID FK and that each line item belongs to one order  
- **Analysis:** Missing emphasis on PRODUCT_ID linkage and junction role; still grounded.  
- **Retrieval:** gt_coverage=0.6667, top_score=0.7, gate=proceed  

### Q010: Show me the order hierarchy from customer to line items.
- **Type:** multi_hop | **Difficulty:** medium  
- **Verdict:** PARTIALLY_CORRECT  
- **Expected:** CUSTOMER_MASTER → SALES_ORDER_HDR → ORDER_LINE_ITEM → TB_PRODUCT  
- **Generated:** gives hierarchy up to line items; does not clearly complete the final “line item → product” in the narrated answer  
- **Analysis:** Partially matches expected hierarchy.  
- **Retrieval:** gt_coverage=0.5, top_score=0.7, gate=proceed  

### Q011: Payment confirmation state and relationship to the order
- **Type:** multi_hop | **Difficulty:** medium  
- **Verdict:** PARTIALLY_CORRECT  
- **Expected:** PAYMENT.CONFIRMED_AT nullable + PAYMENT.STATUS_CODE lifecycle; also order-level PAYMENT_CONFIRMED_AT mirrors event; order STATUS_CODE lifecycle  
- **Generated:** correctly explains PAYMENT.STATUS_CODE and CONFIRMED_AT (nullable) and PAYMENT.ORDER_ID FK; mentions order-level PAYMENT_CONFIRMED_AT (nullable)  
- **Analysis:** Missing/unclear mapping to order-level STATUS_CODE lifecycle (or not tied explicitly), and `gt_coverage=0.0` indicates source mismatch.  
- **Retrieval:** gt_coverage=0.0, top_score=0.4857..., gate=proceed  

### Q012: How are shipments related to orders and warehouses?
- **Type:** multi_hop | **Difficulty:** medium  
- **Verdict:** PARTIALLY_CORRECT  
- **Expected:** SHIPMENT.ORDER_ID → SALES_ORDER_HDR.ORDER_ID; shipment has source warehouse, tracking, status  
- **Generated:** correctly describes shipment→order (ORDER_ID) and comes-from-one-warehouse (A Shipment comes from exactly one Warehouse)  
- **Analysis:** Might be light on tracking/status specifics; `gt_coverage=0.5`.  
- **Retrieval:** gt_coverage=0.5, top_score=0.7, gate=proceed  

### Q013: Can a product belong to multiple categories? (negative)
- **Type:** negative | **Difficulty:** easy  
- **Verdict:** CORRECTLY_ABSTAINED (answered correctly as negative)  
- **Expected:** No; product belongs to exactly one category  
- **Generated:** says “No” and cites “belongs to exactly one Category”  
- **Analysis:** Correct handling of negative constraint.  
- **Retrieval:** gt_coverage=1.0, top_score=0.7, gate=proceed  

### Q014: Is it possible for a customer to place an order without payment? (negative)
- **Type:** negative | **Difficulty:** medium  
- **Verdict:** PARTIALLY_CORRECT  
- **Expected:** Yes, order can exist without payment confirmation (PENDING/nullable PAYMENT_CONFIRMED_AT), but business rule says cannot be shipped until payment confirmed  
- **Generated:** Answers “Yes” because PAYMENT_CONFIRMED_AT is nullable; emphasizes schema doesn’t require a payment row to exist for order header creation  
- **Analysis:** Core “can exist without confirmed payment” matches; however it arguably underplays the **business lifecycle constraint** (“cannot be shipped until payment is confirmed”) emphasized in expected_answer. Also `gt_coverage=0.0` suggests expected-source mismatch.  
- **Retrieval:** gt_coverage=0.0, top_score=0.7, gate=proceed  

### Q015: Monetary value tracking across orders and their line items
- **Type:** multi_hop | **Difficulty:** easy  
- **Verdict:** CORRECT  
- **Expected:** TOTAL_AMT in SALES_ORDER_HDR; line-level UNIT_PRICE/QUANTITY/LINE_AMT; linked via ORDER_ID  
- **Generated:** correctly explains LINE_AMT=quantity×unit_price and components; correctly describes PAYMENT.AMOUNT; and notes it can’t extract exact SALES_ORDER_HDR total column name but acknowledges “Total monetary value”  
- **Analysis:** Matches expected logic; minor uncertainty on exact TOTAL_AMT field name is consistent with the produced response. Grounded and correct in principle.  
- **Retrieval:** gt_coverage=1.0, top_score=0.7, gate=proceed  

---

## Anomalies & Recommendations

### Red Flags
1. **Ground-truth coverage anomalies despite grounded correctness**
   - Multiple questions have `gt_coverage=0.0` (Q006, Q007, Q011, Q014) while `grounded=true` and answers are clearly correct.
   - This likely points to **expected_sources/covered_sources labeling issues** or retrieval context mapping not aligning with the bundle’s `expected_sources` schema.

2. **Negative/semantic nuance not consistently reflected**
   - Q014 is a negative/multi-hop lifecycle question. The answer is mostly aligned but may not fully capture the business constraint about shipping (expected includes that lifecycle emphasis).

3. **Some multi-hop answers omit the final junction/edge**
   - Q009 and Q010 focus on order→header or order→lines but under-communicate the full traversal to product (and/or junction semantics).

### Recommendations
- **Fix ground-truth source bookkeeping:** ensure `expected_sources` entries correspond to the same naming/ontology concepts that `sources_retrieved` uses (e.g., “SalesOrder” vs “SALES_ORDER_HDR”, “Product” vs “TB_PRODUCT”).
- **Add negative-question rubric checks to hallucination grader:** explicitly score whether the answer incorporates the *business lifecycle* constraint (e.g., “cannot be shipped until payment confirmed”) when relevant.
- **Improve context selection for multi-hop:**
  - Increase emphasis in the retrieval distillation step for “junction entity” and “target table” mentions (ORDER_LINE_ITEM → TB_PRODUCT for Q009/Q010).
- **Track alignment metrics beyond gt_coverage:** add a “concept coverage” metric (ontology nodes hit) so correctness isn’t penalized when the expected source labels differ.

---

## Comparison Notes (if applicable)
- Since this bundle does **not** include `ablation_context.changes_vs_baseline`, a strict AB-02 vs AB-00 causal comparison cannot be performed.
- Observed performance is strong: **0 pipeline errors**, **100% grounded**, and **no grader rejections**, indicating AB-02 is at least as stable as baseline for this dataset.