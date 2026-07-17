# AI-Judge Evaluation: AB-19/01_basics_ecommerce
**Evaluator:** (`gpt-5.4-nano-2026-03-17`) using `docs/AI_JUDGE_PROMPT.md`  
**Date:** 2026-07-17

---

# Ablation Study Evaluation: AB-19 — 01_basics_ecommerce

## Executive Summary
This run is **highly successful end-to-end** on the “basics” e-commerce dataset: all 15 answers are marked grounded with **grounded_rate = 1.0**, and average ground-truth retrieval coverage is very high (**avg_gt_coverage ≈ 0.98**) with healthy reranker confidence (**avg_top_score ≈ 0.77**).  
However, the bundle reports a serious builder-side issue: **`builder_report.cypher_failed = true` and `pipeline_health.cypher_failed = true`**, despite `tables_completed = 7`, `failed_mappings = []`, and `ingestion_errors = []`. This is internally inconsistent and should be investigated because it could mean either (a) Cypher healing failed but ingestion still succeeded, or (b) the flag is incorrectly recorded while the graph is actually usable.

## Scores

| Dimension | Score (1-5) | Weight | Weighted |
|---|---:|---:|---:|
| Builder Quality | 2 | 25% | 0.50 |
| Retrieval Effectiveness | 5 | 25% | 1.25 |
| Answer Quality | 5 | 30% | 1.50 |
| Pipeline Health | 2 | 10% | 0.20 |
| Ablation Impact | N/A | 10% | N/A |
| **Overall** |  |  | **3.45** |

## Dimension Analysis

### 1. Builder Quality (2/5)
- **Tables parsed/completed:** `tables_parsed=7`, `tables_completed=7`, `all_tables_completed=true` ✅
- **Cypher:** `builder_report.cypher_failed=true` ❌ (and `pipeline_health.cypher_failed=true` ❌)
- **Failed mappings:** `failed_mappings=[]` ✅
- **Triplets/extraction:** `triplets_extracted=134`, `entities_resolved=90` ⇒ triplets/entity ≈ **1.49**.
  - Rubric signal: “too low (<3) suggests weak extraction; too high (>20) suggests poor ER” → this is **below the ‘healthy’ extraction density** band, though answers still grounded well.
- **Ingestion:** `ingestion_errors=[]`, `builder_skipped=false` ✅

**Verdict:** Builder completion looks fine, but the explicit **Cypher failure flag** prevents a high score under the rubric.

### 2. Retrieval Effectiveness (5/5)
Strong retrieval signals:
- `query_report.grounded_rate = 1.0` ✅
- `avg_gt_coverage = 0.9833` (very high) ✅
- `avg_top_score = 0.7683` (healthy reranker confidence) ✅
- `abstained_count = 0`, `gate_abstentions = 0` ✅ (no false abstentions implied)
- `pipeline_health.questions_with_low_retrieval_score = 0` ✅

### 3. Answer Quality (5/5)
- `query_report.grounded_count = 15/15` and `grounded_rate = 1.0` ✅
- Per-question examples show correct semantic content for direct/multi-hop/negative questions:
  - **Q013 (negative):** correctly answers “No” and cites exactly-one-category constraint via `TB_PRODUCT.CATEGORY_ID` NOT NULL + FK.
  - **Q014 (negative/medium):** answers “Yes” (and argues the system allows an order row before payment confirmation because `PAYMENT_CONFIRMED_AT` is nullable). This matches the *schema-permitted* interpretation and remains grounded.

Also:
- `grader_rejection_count` is **0 for all shown questions**, consistent with stable generation.

### 4. Pipeline Health (2/5)
- `pipeline_health.cypher_failed=true` ❌
- `total_grader_rejections=0`, `grader_inconsistencies=0`, `gate_abstentions=0` ✅
- `ingestion_errors_count=0` ✅

**Main concern:** Cypher failure indicates instability or broken healing, even though downstream QA succeeds—this suggests an instrumentation/recording mismatch or that the graph was still produced via fallback despite the failure flag.

### 5. Ablation Impact (N/A)
- The rubric says to score this only when the study is compared to a baseline (e.g., AB-00) or when `ablation_context.changes_vs_baseline` is provided.  
- The bundle only identifies `study_id=AB-19` with config parameters, but **does not specify “changes vs baseline”**.

## Per-Question Deep Dive

### Q001: What information is stored for each customer?
- **Type:** direct_mapping | **Difficulty:** easy
- **Verdict:** CORRECT
- **Expected:** cust id, full name, email (unique), region code, creation date, active status
- **Generated:** Describes `CUSTOMER_MASTER` fields: `CUST_ID`, `FULL_NAME`, `EMAIL`, `REGION_CODE`, `CREATED_AT`, `IS_ACTIVE`; mentions linkage via `SALES_ORDER_HDR.CUST_ID`.
- **Analysis:** Matches customer attribute set and identifiers; grounded in retrieved dictionary/glossary + schema column descriptions.
- **Retrieval:** gt_coverage=1.0, top_score=0.7814, gate=proceed

### Q002: How are products categorized on the platform?
- **Type:** direct_mapping | **Difficulty:** easy
- **Verdict:** CORRECT
- **Expected:** product references exactly one category; category has optional parent for hierarchy
- **Generated:** `TB_PRODUCT.CATEGORY_ID` FK to `TB_CATEGORY.CATEGORY_ID`; parent hierarchy via `PARENT_CATEGORY_ID`
- **Analysis:** Correctly captures both single-category assignment and hierarchical category tree.
- **Retrieval:** gt_coverage=1.0, top_score=0.7, gate=proceed

### Q003: What is the relationship between customers and sales orders?
- **Type:** direct_mapping | **Difficulty:** easy
- **Verdict:** CORRECT
- **Expected:** each order placed by one customer (CUST_ID FK); customer has zero or more orders
- **Generated:** Uses glossary relationship + FK `SALES_ORDER_HDR.CUST_ID -> CUSTOMER_MASTER.CUST_ID`
- **Analysis:** Correct one-to-many relationship.
- **Retrieval:** gt_coverage=1.0, top_score=0.9847, gate=proceed

### Q004: What does an order line item contain?
- **Type:** direct_mapping | **Difficulty:** easy
- **Verdict:** CORRECT
- **Expected:** product, quantity, unit price at purchase, extended amount; belongs to exactly one sales order
- **Generated:** `ORDER_LINE_ITEM` includes `LINE_ID`, `ORDER_ID`, `PRODUCT_ID`, `QUANTITY`, `UNIT_PRICE`, `LINE_AMT`
- **Analysis:** Correctly enumerates required components and ties to order.
- **Retrieval:** gt_coverage=1.0, top_score=0.9781, gate=proceed

### Q005: How are payments linked to orders?
- **Type:** direct_mapping | **Difficulty:** easy
- **Verdict:** CORRECT
- **Expected:** payment associated with exactly one sales order through `ORDER_ID`; includes method, amount, status, confirmation timestamp
- **Generated:** FK `PAYMENT.ORDER_ID -> SALES_ORDER_HDR.ORDER_ID` + describes payment attributes
- **Analysis:** Correct linkage and attribute framing.
- **Retrieval:** gt_coverage=1.0, top_score=0.9501, gate=proceed

### Q006: What statuses can an order have?
- **Type:** attribute_lookup | **Difficulty:** easy
- **Verdict:** CORRECT
- **Expected:** PENDING, CONFIRMED, SHIPPED, DELIVERED, CANCELLED (and lifecycle explanation)
- **Generated:** lists the five statuses
- **Analysis:** Correct enumeration; grounded on glossary/status code content.
- **Retrieval:** gt_coverage=1.0, top_score=0.7, gate=proceed

### Q007: Which table stores the product SKU information?
- **Type:** direct_mapping | **Difficulty:** easy
- **Verdict:** CORRECT
- **Expected:** `TB_PRODUCT` stores SKU in `SKU`
- **Generated:** `TB_PRODUCT.SKU`
- **Analysis:** Correct single-column answer.
- **Retrieval:** gt_coverage=1.0, top_score=0.7, gate=proceed

### Q008: How can I find all orders placed by a specific customer?
- **Type:** multi_hop | **Difficulty:** medium
- **Verdict:** CORRECT
- **Expected:** filter `SALES_ORDER_HDR` by `CUST_ID` and join to `CUSTOMER_MASTER` on `CUST_ID`
- **Generated:** describes filtering `SALES_ORDER_HDR.CUST_ID` and join logic; mentions key order fields
- **Analysis:** Correct multi-hop join/filter guidance.
- **Retrieval:** gt_coverage=1.0, top_score=0.7, gate=proceed

### Q009: How does the schema link orders to their individual product line items?
- **Type:** multi_hop | **Difficulty:** medium
- **Verdict:** CORRECT
- **Expected:** `ORDER_LINE_ITEM` is junction: `ORDER_ID` FK to `SALES_ORDER_HDR`, `PRODUCT_ID` FK to `TB_PRODUCT`; also QUANTITY/UNIT_PRICE/LINE_AMT
- **Generated:** correctly explains FK constraints for both sides
- **Analysis:** Correct junction-table modeling.
- **Retrieval:** gt_coverage=1.0, top_score=0.7, gate=proceed

### Q010: Show me the order hierarchy from customer to line items.
- **Type:** multi_hop | **Difficulty:** medium
- **Verdict:** CORRECT
- **Expected:** `CUSTOMER_MASTER -> SALES_ORDER_HDR -> ORDER_LINE_ITEM -> TB_PRODUCT`
- **Generated:** describes hierarchy and join path via FK fields
- **Analysis:** Matches expected path; note gt_coverage is lower than others (0.75) but answer remains grounded/correct.
- **Retrieval:** gt_coverage=0.75, top_score=0.7, gate=proceed

### Q011: How does the schema model the confirmation state of a payment and its relationship to the order?
- **Type:** multi_hop | **Difficulty:** medium
- **Verdict:** CORRECT
- **Expected:** `PAYMENT.CONFIRMED_AT` + `PAYMENT.STATUS_CODE`; order mirrors via `SALES_ORDER_HDR.PAYMENT_CONFIRMED_AT`; payment linked via `PAYMENT.ORDER_ID`
- **Generated:** matches both timestamp/status fields and linkage
- **Analysis:** Correct modeling at both payment and order header levels.
- **Retrieval:** gt_coverage=1.0, top_score=0.7, gate=proceed

### Q012: How are shipments related to orders and warehouses?
- **Type:** multi_hop | **Difficulty:** medium
- **Verdict:** CORRECT
- **Expected:** `SHIPMENT.ORDER_ID -> SALES_ORDER_HDR`; source warehouse code + tracking/status
- **Generated:** explains order linkage via `SHIPMENT.ORDER_ID` and warehouse via `SHIPMENT.WAREHOUSE_CODE`
- **Analysis:** Correct two-hop relationship (order + warehouse).
- **Retrieval:** gt_coverage=1.0, top_score=0.8300, gate=proceed

### Q013: Can a product belong to multiple categories?
- **Type:** negative | **Difficulty:** easy
- **Verdict:** CORRECT
- **Expected:** No; each product belongs to exactly one category (`TB_PRODUCT.CATEGORY_ID` NOT NULL FK)
- **Generated:** “No” with exactly-one-category justification
- **Analysis:** Correct negative handling.
- **Retrieval:** gt_coverage=1.0, top_score=0.7, gate=proceed

### Q014: Is it possible for a customer to place an order without payment?
- **Type:** negative | **Difficulty:** medium
- **Verdict:** CORRECT
- **Expected:** “Yes” in the sense orders can exist without payment row/confirmation yet; shipping requires payment confirmation
- **Generated:** argues `SALES_ORDER_HDR.PAYMENT_CONFIRMED_AT` is nullable and shipping is constrained, not order creation
- **Analysis:** Correctly answers “Yes” and supports with nullable payment confirmation semantics.
- **Retrieval:** gt_coverage=1.0, top_score=0.7, gate=proceed

### Q015: What schema fields support monetary value tracking across orders and their line items?
- **Type:** multi_hop | **Difficulty:** easy
- **Verdict:** CORRECT
- **Expected:** `SALES_ORDER_HDR.TOTAL_AMT`; `ORDER_LINE_ITEM.UNIT_PRICE`, `QUANTITY`, `LINE_AMT`; link via `ORDER_ID`
- **Generated:** mentions line-level monetary fields and also introduces `PAYMENT.AMOUNT`
- **Analysis:** Core expected fields are correct; extra payment-level detail is additional correct info.
- **Retrieval:** gt_coverage=1.0, top_score=0.7, gate=proceed

## Anomalies & Recommendations

### Red Flags
1. **Builder/Cypher inconsistency**
   - `builder_report.cypher_failed = true`
   - `pipeline_health.cypher_failed = true`
   - Yet `tables_completed=7`, `all_tables_completed=true`, `failed_mappings=[]`, and **all query answers are grounded**.
   - This strongly suggests either:
     - Cypher healing failed but fallback/deterministic upsert succeeded (and flags were not cleared), or
     - Cypher failure is reported incorrectly, or
     - Graph build partially succeeded in a way still sufficient for this dataset.

2. **Low triplet density**
   - `triplets_extracted/entities_resolved ≈ 1.49` (below the rubric’s “healthy” ≥3 signal).
   - Despite that, retrieval/QA is excellent—likely because the dataset is small/basics and glossary/dictionary contexts were sufficient.

### Recommendations
- **Investigate cypher_failed flag semantics**
  - Confirm whether `cypher_failed` indicates “attempt failed then fallback succeeded” vs “final graph write failed”.
  - Add explicit metrics: number of Cypher statements executed successfully vs attempted; whether deterministic fallback path was taken.
- **Add builder artifact verification**
  - After `build_graph`, run a sanity query (e.g., count nodes/relationships for each ontology concept) to ensure KG is fully populated even if LLM Cypher healing reports failure.
- **Improve triplet extraction/ER instrumentation**
  - Log triplets per document chunk and extraction failure modes (JSON parse, truncation at token cap).
  - Consider adjusting ER thresholds or blocking settings only after validating KG coverage impact on multi-hop retrieval.

## Comparison Notes (if applicable)
- No AB-00 baseline bundle or `ablation_context.changes_vs_baseline` is provided, so a true causal ablation comparison cannot be scored.