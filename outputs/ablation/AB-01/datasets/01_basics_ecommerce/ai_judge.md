# AI-Judge Evaluation: AB-01/01_basics_ecommerce
**Evaluator:** (`gpt-5.4-nano-2026-03-17`) using `docs/AI_JUDGE_PROMPT.md`  
**Date:** 2026-07-17

---

# Ablation Study Evaluation: AB-01 — 01_basics_ecommerce

## Executive Summary
This run shows **strong end-to-end pipeline stability** (builder completed all tables, no Cypher failures, no ingestion errors, no gate abstentions) and **perfect grounding** (`grounded_rate=1.0`, `avg_gt_coverage=1.0`). However, several **answers are not actually correct w.r.t. expected schema rules**, despite being marked grounded—especially on **negative questions** and **attribute-listing** (e.g., order statuses). Overall, this indicates a **mismatch between the dataset-grounding signals and semantic correctness**, likely due to grading/gating relying heavily on retrieved conceptual context rather than verifying the specific expected constraints/values.

## Scores

| Dimension | Score (1-5) | Weight | Weighted |
|---|---:|---:|---:|
| Builder Quality | 5 | 25% | 1.25 |
| Retrieval Effectiveness | 4 | 25% | 1.00 |
| Answer Quality | 2 | 30% | 0.60 |
| Pipeline Health | 5 | 10% | 0.50 |
| Ablation Impact | 3 | 10% | 0.30 |
| **Overall** |  |  | **3.65** |

## Dimension Analysis

### 1. Builder Quality (5/5)
- `tables_completed=7`, `all_tables_completed=true`
- `cypher_failed=false`
- `failed_mappings=[]`
- `ingestion_errors=[]`
- Triplet density/ER cannot be computed precisely from the provided “per-doc” granularity, but the absolute ingestion/build health signals are excellent.

**Verdict:** Builder graph construction is fully successful for this dataset.

### 2. Retrieval Effectiveness (4/5)
- `grounded_rate=1.0`
- `abstained_count=0` (no false abstentions of unanswerable questions)
- `avg_gt_coverage=1.0` indicates the ground-truth sources are consistently retrieved.
- `avg_top_score=0.5725` is healthy for a cross-encoder reranker.
- Still, several questions where answers should use *specific expected constraints/values* do not—this points more to answer quality than retrieval (retrieval appears adequate).

**Verdict:** Retrieval is strong overall; slight downgrade vs. perfect because retrieval scores don’t reflect the semantic failures seen later.

### 3. Answer Quality (2/5)
Despite perfect grounding, multiple generated answers **do not match the expected facts/rules**:

- **Q006 (positive attribute lookup: order statuses)**  
  Expected: a specific set of five statuses from a CHECK constraint + lifecycle terms.  
  Generated: “I cannot find this information…” even though `gt_coverage=1.0` and the context includes `SALES_ORDER_HDR.STATUS_CODE`.  
  → This is a semantic incompleteness/failure.

- **Q008 (multi-hop orders by customer)**  
  Generated: correctly explains the filter/join *in principle*, but then says it can’t state exact join condition/columns.  
  Even so, for this basics dataset, the expected answer is explicit about joining on `CUST_ID`. The answer is “partially correct but hedged,” which should not be rated as fully correct in an expert semantic rubric.

- **Negative question failures:**
  - **Q013 (negative: can a product belong to multiple categories?)**  
    Expected: **No**, exactly one category per product (CATEGORY_ID FK).  
    Generated: cannot confirm; implies ambiguity.  
    → This is a direct failure on negative reasoning.
  - **Q014 (negative: possible to place an order without payment?)**  
    Expected: **Yes** can exist without payment (nullable PAYMENT_CONFIRMED_AT; default PENDING).  
    Generated: “Yes—” but the justification focuses on missing constraints; also doesn’t properly incorporate the glossary rule about shipping requiring confirmed payment (expected answer includes that business rule).  
    → Partially aligned but not confidently matching the expected business constraint set.

- `grader_rejection_count=1` overall (only one rejection), suggesting the semantic grader is **not catching** these misses consistently.

**Best explanation:** The system is able to produce context-grounded statements, but its final semantic mapping to “expected constraints/allowed values/cardinalities” is inconsistent—especially for negative questions and enumerations.

### 4. Pipeline Health (5/5)
- `cypher_failed=false`
- `grader_inconsistencies=0`
- `gate_abstentions=0`
- `total_grader_rejections=1` (minor and not catastrophic)
- Latency fields are all `0` here; not enough signal, but no failures are reported.

**Verdict:** Operationally healthy.

### 5. Ablation Impact (3/5)
This is **AB-01 (not baseline AB-00)**, but the bundle does not include `ablation_context` with “changes vs baseline” fields, so causality is hard to establish. What we can observe:
- `retrieval_mode="vector"` and `enable_reranker=true` are explicitly set.
- Despite vector-only mode, retrieval coverage is still perfect (`avg_gt_coverage=1.0`), so ablation impact on retrieval appears limited in this basics dataset.

Given missing baseline-comparison metadata, I award a middle score.

## Per-Question Deep Dive

### Q001: What information is stored for each customer?
- **Type:** direct_mapping | **Difficulty:** easy
- **Verdict:** CORRECT
- **Expected:** unique ID, full name, email (unique), region code, creation date, active status
- **Generated:** lists CUST_ID, FULL_NAME, EMAIL, REGION_CODE, CREATED_AT, IS_ACTIVE; identifies CUSTOMER_MASTER as table
- **Analysis:** Matches expected customer attribute set; email uniqueness is not asserted explicitly but overall field coverage is correct.
- **Retrieval:** gt_coverage=1.0, top_score=0.4857, gate=proceed

### Q002: How are products categorized on the platform?
- **Type:** direct_mapping | **Difficulty:** easy
- **Verdict:** CORRECT
- **Expected:** one category per product; categories form hierarchy (parent-child)
- **Generated:** CATEGORY_ID in TB_PRODUCT references TB_CATEGORY; TB_CATEGORY has PARENT_CATEGORY_ID
- **Analysis:** Captures the hierarchy and single-valued category reference.
- **Retrieval:** gt_coverage=1.0, top_score=0.4857, gate=proceed

### Q003: What is the relationship between customers and sales orders?
- **Type:** direct_mapping | **Difficulty:** easy
- **Verdict:** CORRECT
- **Expected:** each sales order placed by exactly one customer; customer can place zero+ orders
- **Generated:** SALES_ORDER_HDR has CUST_ID FK; CUSTOMER_MASTER.CUST_ID is PK
- **Analysis:** Correct cardinality phrasing is consistent with expected business relationship.
- **Retrieval:** gt_coverage=1.0, top_score=0.4857, gate=proceed

### Q004: What does an order line item contain?
- **Type:** direct_mapping | **Difficulty:** easy
- **Verdict:** CORRECT
- **Expected:** product, quantity, unit price, extended amount; belongs to one sales order
- **Generated:** mentions QUANTITY, UNIT_PRICE, LINE_AMT=qty*unit_price; lists columns from ORDER_LINE_ITEM
- **Analysis:** Correct and sufficiently specific.
- **Retrieval:** gt_coverage=1.0, top_score=0.9869, gate=proceed

### Q005: How are payments linked to orders?
- **Type:** direct_mapping | **Difficulty:** easy
- **Verdict:** PARTIALLY_CORRECT
- **Expected:** payment associated with exactly one order via ORDER_ID; method, amount, status, confirmed timestamp
- **Generated:** says payment settles exactly one sales order; but states it doesn’t include physical FK/column mapping and partially hedges about linkage fields
- **Analysis:** Grounded conceptual linkage is right, but the expected answer asks for ORDER_ID FK and confirmation timestamp; those are not clearly delivered.
- **Retrieval:** gt_coverage=1.0, top_score=0.9439, gate=proceed

### Q006: What statuses can an order have?
- **Type:** attribute_lookup | **Difficulty:** easy
- **Verdict:** INCORRECT
- **Expected:** PENDING, CONFIRMED, SHIPPED, DELIVERED, CANCELLED (CHECK on SALES_ORDER_HDR.STATUS_CODE) + glossary lifecycle
- **Generated:** “I cannot find this information…” and only repeats that STATUS_CODE exists
- **Analysis:** Fails to provide the enumerated allowed values despite strong grounding signals.
- **Retrieval:** gt_coverage=1.0, top_score=0.4857, gate=proceed

### Q007: Which table stores the product SKU information?
- **Type:** direct_mapping | **Difficulty:** easy
- **Verdict:** CORRECT
- **Expected:** TB_PRODUCT stores SKU in TB_PRODUCT.SKU
- **Generated:** explicitly states TB_PRODUCT.SKU
- **Analysis:** Correct.
- **Retrieval:** gt_coverage=1.0, top_score=0.4857, gate=proceed

### Q008: How can I find all orders placed by a specific customer?
- **Type:** multi_hop | **Difficulty:** medium
- **Verdict:** PARTIALLY_CORRECT
- **Expected:** filter SALES_ORDER_HDR by CUST_ID; join CUSTOMER_MASTER on CUST_ID to show orders
- **Generated:** describes filtering/join on CUSTOMER_MASTER.CUST_ID in principle, but claims it can’t state exact join condition/columns
- **Analysis:** Conceptually right but unnecessarily denies the specific join key expected.
- **Retrieval:** gt_coverage=1.0, top_score=0.4857, gate=proceed

### Q009: How does the schema link orders to their individual product line items?
- **Type:** multi_hop | **Difficulty:** medium
- **Verdict:** INCORRECT
- **Expected:** ORDER_LINE_ITEM junction between SALES_ORDER_HDR and TB_PRODUCT via ORDER_ID and PRODUCT_ID, plus quantity/unit_price/line_amt
- **Generated:** can’t identify physical table/schema mechanism or FK linkage; only describes the business meaning of “Order Line Item”
- **Analysis:** Misses the core required mechanism (junction + FK columns).
- **Retrieval:** gt_coverage=1.0, top_score=0.4857, gate=proceed

### Q010: Show me the order hierarchy from customer to line items.
- **Type:** multi_hop | **Difficulty:** medium
- **Verdict:** PARTIALLY_CORRECT
- **Expected:** CUSTOMER_MASTER → SALES_ORDER_HDR → ORDER_LINE_ITEM → TB_PRODUCT
- **Generated:** provides narrative at concept level (customer, sales order header, line item) but denies schema-level join path/foreign keys
- **Analysis:** Hierarchy is implied correctly but lacks the “show me” specificity expected.
- **Retrieval:** gt_coverage=1.0, top_score=0.4857, gate=proceed

### Q011: How does the schema model the confirmation state of a payment and its relationship to the order?
- **Type:** multi_hop | **Difficulty:** medium
- **Verdict:** PARTIALLY_CORRECT
- **Expected:** PAYMENT.CONFIRMED_AT + PAYMENT.STATUS_CODE enum (PENDING/CONFIRMED/FAILED/REFUNDED) and SALES_ORDER_HDR.PAYMENT_CONFIRMED_AT mirrors; order lifecycle statuses
- **Generated:** correctly points to PAYMENT status/timestamp and mentions SALES_ORDER_HDR.PAYMENT_CONFIRMED_AT exists
- **Analysis:** But does not enumerate payment statuses nor clearly connect all expected fields/constraints.
- **Retrieval:** gt_coverage=1.0, top_score=0.4857, gate=proceed

### Q012: How are shipments related to orders and warehouses?
- **Type:** multi_hop | **Difficulty:** medium
- **Verdict:** PARTIALLY_CORRECT
- **Expected:** SHIPMENT has ORDER_ID FK to SALES_ORDER_HDR; includes source warehouse code + tracking + delivery status
- **Generated:** correct on “linked to exactly one sales order” and “moved from a source warehouse,” but hedges on physical join keys/warehouse field naming
- **Analysis:** Good concept coverage; misses expected schema specificity (ORDER_ID FK and warehouse code field naming).
- **Retrieval:** gt_coverage=1.0, top_score=0.8283, gate=proceed

### Q013: Can a product belong to multiple categories?
- **Type:** negative | **Difficulty:** easy
- **Verdict:** INCORRECT
- **Expected:** No—each product belongs to exactly one category; CATEGORY_ID FK on TB_PRODUCT
- **Generated:** cannot confirm; only notes TB_PRODUCT has CATEGORY_ID field
- **Analysis:** Negative question handling is wrong: should conclude single-category constraint, not ambiguity.
- **Retrieval:** gt_coverage=1.0, top_score=0.4857, gate=proceed

### Q014: Is it possible for a customer to place an order without payment?
- **Type:** negative | **Difficulty:** medium
- **Verdict:** PARTIALLY_CORRECT
- **Expected:** Yes possible; PAYMENT_CONFIRMED_AT nullable; status default PENDING; but shipping requires confirmed payment
- **Generated:** answers “Yes” based on lack of explicit constraint preventing order creation without Payment row; does not clearly incorporate the shipping/fulfillment constraint emphasized in expected answer
- **Analysis:** Correct polarity (Yes), weak alignment to the expected business-rule nuance.
- **Retrieval:** gt_coverage=1.0, top_score=0.4857, gate=proceed

### Q015: What schema fields support monetary value tracking across orders and their line items?
- **Type:** multi_hop | **Difficulty:** easy
- **Verdict:** PARTIALLY_CORRECT
- **Expected:** SALES_ORDER_HDR.TOTAL_AMT; ORDER_LINE_ITEM.UNIT_PRICE, QUANTITY (>0), LINE_AMT (=qty*unit_price); join via ORDER_ID
- **Generated:** covers line-item monetary fields and linkage to order via ORDER_ID; mentions Payment.amount but does not provide TOTAL_AMT or QUANTITY constraint detail
- **Analysis:** Misses header-level TOTAL_AMT and quantity constraint; includes extra (payment.amount) but lacks expected fields.
- **Retrieval:** gt_coverage=1.0, top_score=0.4857, gate=proceed

## Anomalies & Recommendations

### Red Flags
- **Perfect grounding doesn’t imply correctness:** multiple answers are semantically wrong/incomplete (notably **Q006, Q009, Q013**).
- **Negative questions are mishandled:** Q013 should be a clear “No” but the model hedges.
- **Enumerations/constraints are often missing:** order/payment status lists and schema constraints aren’t reliably extracted into the final answer.
- **Grader seems permissive:** `grader_rejection_count=1` despite clear expected-answer mismatches (especially negative and enumeration cases).

### Recommendations
1. **Tighten semantic verification for expected enumerations and cardinality constraints**  
   Add explicit checks in the hallucination grader/self-RAG step for:  
   - allowed-value lists (status codes)  
   - cardinality rules (exactly one / no multiple categories)  
   - junction-table mechanisms (FKs between entities)
2. **Improve negative-question handling policy**  
   For `query_type="negative"`, require either:
   - explicit evidence of rule enforcement (FK/cardinality/constraint) in contexts, or
   - abstain (or state “cannot determine”) consistently with expected.
3. **Ensure “context sufficiency” maps to answer sufficiency**  
   Several outputs claim inability to provide exact joins/columns despite `gt_coverage=1.0`. Add a guard: if `gt_coverage=1.0` and required sources are present, the generator must provide the key fields (e.g., ORDER_ID, TOTAL_AMT) rather than disclaiming.
4. **Add a dataset-aware expected-source to answer-field constraint**  
   When `expected_sources` include specific tables/columns, enforce that at least the primary required field names appear in the final answer (or justify why they are unavailable).

## Comparison Notes (if applicable)
- Bundle metadata doesn’t provide baseline (`AB-00`) diffs via `ablation_context`, so a strict causal ablation comparison isn’t possible.
- Even with `retrieval_mode=vector`, retrieval coverage and top-score are strong—semantic failures likely stem from **generation/grading and constraint extraction**, not retrieval recall.