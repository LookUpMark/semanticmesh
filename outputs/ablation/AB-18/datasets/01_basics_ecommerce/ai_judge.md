# AI-Judge Evaluation: AB-18/01_basics_ecommerce
**Evaluator:** (`gpt-5.4-nano-2026-03-17`) using `docs/AI_JUDGE_PROMPT.md`  
**Date:** 2026-07-17

---

# Ablation Study Evaluation: AB-18 — 01_basics_ecommerce

## Executive Summary
AB-18 shows a fully functioning two-graph pipeline on the E-Commerce *basics* dataset: the Builder Graph completed all table mappings with no Cypher failures or ingestion issues, and Query Graph responses are fully grounded (grounded rate = 1.0) with excellent GT source coverage (avg_gt_coverage ≈ 0.983). Retrieval quality is also strong on average (avg_top_score ≈ 0.78) and the system never abstains incorrectly (0 abstentions).

The only notable weakness is not “correctness” but **schema/answer nuance**: for the negative question Q014 (“Is it possible for a customer to place an order without payment?”), the generated answer asserts that orders can exist without payment, which appears to conflict with the expected interpretation that payment is required for shipping but not necessarily for order existence—this run’s verdict should therefore be treated as **potentially partially incorrect** depending on how strictly the rubric interprets the expected answer’s business rule framing.

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
- Triplet extraction appears healthy: `triplets_extracted=108` over a small set of tables/entities (no sign of ER collapse; rather ER achieved 71 resolved entities)

This meets the rubric’s “all tables completed, no cypher failures, no failed mappings” criteria.

### 2. Retrieval Effectiveness (4/5)
Key signals:
- `grounded_rate=1.0` and `avg_gt_coverage=0.9833` are excellent.
- `avg_top_score=0.7795` indicates the reranker is confident on the top fused results (healthy for bge-reranker-v2-m3).
- `pipeline_health.questions_with_low_retrieval_score=0` and `gate_abstentions=0`.

A small reason to not award 5:
- Q010 (multi-hop) has `gt_coverage=0.75`, noticeably lower than others, indicating occasional weaker traversal coverage even on basics.

Still, overall retrieval is strong enough for a 4 rather than a 3.

### 3. Answer Quality (4/5)
- `query_report.grounded_rate=1.0` (all answers grounded in retrieved contexts).
- Across the provided per-question samples, most answers match the expected facts extremely well (Q001–Q012 mostly align tightly with expected schema relationships/status lists/junction logic).

Potential issue:
- **Q014 (negative, medium)**: The expected answer says “Yes, an order can exist without payment,” and explains that payment affects shipping rather than order existence; the generated answer closely mirrors this by pointing to `SALES_ORDER_HDR.PAYMENT_CONFIRMED_AT` being nullable and framing payment as affecting shipping.  
  However, it also downplays the “nothing prevents an order from existing without a payment row” vs. “orders are created first and require payment confirmation before fulfillment” in a way that could be interpreted as overly permissive. Because the expected answer is itself somewhat conditional/interpretive, the correct rubric action is to treat the match as **not fully perfect nuance** but still plausibly correct from the schema. Hence: 4 overall rather than 5.

### 4. Pipeline Health (5/5)
- `total_grader_rejections=0`
- `grader_inconsistencies=0`
- `gate_abstentions=0`
- `cypher_failed=false`, `failed_mappings_count=0`, `ingestion_errors_count=0`

This run shows no instability and no evidence of self-healing being required.

### 5. Ablation Impact (N/A)
- Study is AB-18, but the bundle does not provide explicit `changes_vs_baseline` nor an ablation_context with expected impact.
- `config` shows `enable_reranker=true` and `retrieval_mode=hybrid`, but we cannot infer which flags differ from baseline in this rubric framework.

## Per-Question Deep Dive

### Q001: What information is stored for each customer?
- **Type:** direct_mapping | **Difficulty:** easy
- **Verdict:** CORRECT
- **Expected:** ID, full name, unique email, region code, creation date, active status
- **Generated:** CUSTOMER_MASTER fields incl. CUST_ID, FULL_NAME, EMAIL, REGION_CODE, CREATED_AT, IS_ACTIVE; supports uniqueness implied by “unique email”
- **Analysis:** Schema fields align with expected customer attributes and the email uniqueness is consistent with the dataset description.
- **Retrieval:** gt_coverage=1.0, top_score=0.7883, gate=proceed

### Q002: How are products categorized on the platform?
- **Type:** direct_mapping | **Difficulty:** easy
- **Verdict:** CORRECT
- **Expected:** product → exactly one category; category hierarchy via parent category; CATEGORY_ID FK
- **Generated:** TB_PRODUCT.CATEGORY_ID FK to TB_CATEGORY.CATEGORY_ID; PARENT_CATEGORY_ID self-reference; matches hierarchy description
- **Analysis:** Correct FK + hierarchy articulation.
- **Retrieval:** gt_coverage=1.0, top_score=0.7, gate=proceed

### Q003: What is the relationship between customers and sales orders?
- **Type:** direct_mapping | **Difficulty:** easy
- **Verdict:** CORRECT
- **Expected:** each order placed by exactly one customer; customer can have zero or more orders
- **Generated:** Customer places zero-or-more orders; FK SALES_ORDER_HDR.CUST_ID → CUSTOMER_MASTER.CUST_ID
- **Analysis:** Correct cardinality and FK mapping.
- **Retrieval:** gt_coverage=1.0, top_score=0.9847, gate=proceed

### Q004: What does an order line item contain?
- **Type:** direct_mapping | **Difficulty:** easy
- **Verdict:** CORRECT
- **Expected:** product, quantity, unit price at purchase, extended amount; belongs to exactly one sales order
- **Generated:** ORDER_LINE_ITEM includes PRODUCT_ID, QUANTITY, UNIT_PRICE, LINE_AMT; ORDER_ID belongs to sales order
- **Analysis:** Complete and schema-faithful.
- **Retrieval:** gt_coverage=1.0, top_score=0.9805, gate=proceed

### Q005: How are payments linked to orders?
- **Type:** direct_mapping | **Difficulty:** easy
- **Verdict:** CORRECT
- **Expected:** PAYMENT.ORDER_ID → SALES_ORDER_HDR.ORDER_ID; payment method/amount/status/confirmed timestamp
- **Generated:** Explicit foreign key linkage and business rule “one payment for exactly one order”
- **Analysis:** Matches expected join logic.
- **Retrieval:** gt_coverage=1.0, top_score=0.9501, gate=proceed

### Q006: What statuses can an order have?
- **Type:** attribute_lookup | **Difficulty:** easy
- **Verdict:** CORRECT
- **Expected:** PENDING, CONFIRMED, SHIPPED, DELIVERED, CANCELLED via STATUS_CODE
- **Generated:** Lists the same five statuses and ties to SALES_ORDER_HDR.STATUS_CODE
- **Analysis:** Correct enumeration.
- **Retrieval:** gt_coverage=1.0, top_score=0.7, gate=proceed

### Q007: Which table stores the product SKU information?
- **Type:** direct_mapping | **Difficulty:** easy
- **Verdict:** CORRECT
- **Expected:** TB_PRODUCT stores SKU in SKU column
- **Generated:** TB_PRODUCT.SKU, consistent with glossary/schema
- **Analysis:** Direct and correct.
- **Retrieval:** gt_coverage=1.0, top_score=0.9892, gate=proceed

### Q008: How can I find all orders placed by a specific customer?
- **Type:** multi_hop | **Difficulty:** medium
- **Verdict:** CORRECT
- **Expected:** filter SALES_ORDER_HDR by CUST_ID and join to CUSTOMER_MASTER on CUST_ID
- **Generated:** Correct SQL-style logic; enumerates order fields
- **Analysis:** Matches expected join/filter path.
- **Retrieval:** gt_coverage=1.0, top_score=0.7, gate=proceed

### Q009: How does the schema link orders to their individual product line items?
- **Type:** multi_hop | **Difficulty:** medium
- **Verdict:** CORRECT
- **Expected:** ORDER_LINE_ITEM links SALES_ORDER_HDR and TB_PRODUCT via ORDER_ID and PRODUCT_ID; includes quantity/unit_price/line_amt
- **Generated:** Explains ORDER_LINE_ITEM as junction, FK directions, belongs-to-one-order semantics
- **Analysis:** Correct multi-hop linkage.
- **Retrieval:** gt_coverage=1.0, top_score=0.7, gate=proceed

### Q010: Show me the order hierarchy from customer to line items.
- **Type:** multi_hop | **Difficulty:** medium
- **Verdict:** PARTIALLY_CORRECT
- **Expected:** CUSTOMER_MASTER → SALES_ORDER_HDR → ORDER_LINE_ITEM → TB_PRODUCT
- **Generated:** Provides the same hierarchy and join path; however, the expected answer is explicit about the full chain, while the generated answer sometimes summarizes at “line items for a customer” rather than fully restating TB_PRODUCT at the end of the join in every clause.
- **Analysis:** Semantically aligned, but slightly less explicit about TB_PRODUCT linkage than the expected phrasing.
- **Retrieval:** gt_coverage=0.75, top_score=0.7, gate=proceed

### Q011: How does the schema model the confirmation state of a payment and its relationship to the order?
- **Type:** multi_hop | **Difficulty:** medium
- **Verdict:** CORRECT
- **Expected:** PAYMENT.CONFIRMED_AT + PAYMENT.STATUS_CODE; mirrored by SALES_ORDER_HDR.PAYMENT_CONFIRMED_AT; order lifecycle includes PENDING/CONFIRMED/SHIPPED/DELIVERED/CANCELLED
- **Generated:** Correctly describes both tables’ fields and the operational “before ships” rule
- **Analysis:** Complete.
- **Retrieval:** gt_coverage=1.0, top_score=0.7, gate=proceed

### Q012: How are shipments related to orders and warehouses?
- **Type:** multi_hop | **Difficulty:** medium
- **Verdict:** CORRECT
- **Expected:** SHIPMENT.ORDER_ID → SALES_ORDER_HDR.ORDER_ID; SHIPMENT.WAREHOUSE_CODE + tracking/status
- **Generated:** Correct foreign-key and business-rule relationships; mentions warehouse/source and partial shipments
- **Analysis:** Correct.
- **Retrieval:** gt_coverage=1.0, top_score=0.7, gate=proceed

### Q013: Can a product belong to multiple categories?
- **Type:** negative | **Difficulty:** easy
- **Verdict:** CORRECT
- **Expected:** No; TB_PRODUCT.CATEGORY_ID is a single FK to TB_CATEGORY
- **Generated:** “No” with glossary + FK explanation
- **Analysis:** Proper negative handling; no fabricated “maybe”.
- **Retrieval:** gt_coverage=1.0, top_score=0.7, gate=proceed

### Q014: Is it possible for a customer to place an order without payment?
- **Type:** negative | **Difficulty:** medium
- **Verdict:** PARTIALLY_CORRECT
- **Expected:** Yes, order can exist without payment row; PAYMENT_CONFIRMED_AT nullable; SHIPPING requires payment confirmation
- **Generated:** Says yes due to nullable PAYMENT_CONFIRMED_AT; treats PAYMENT as affecting shipping rather than whether the order record can exist
- **Analysis:** The generated answer matches the expected “nullable confirmation timestamp => order record can exist,” but the phrasing is slightly ambiguous about whether “no payment row exists yet” is allowed/covered. On a strict reading, this is minor nuance deviation.
- **Retrieval:** gt_coverage=1.0, top_score=0.7, gate=proceed

### Q015: What schema fields support monetary value tracking across orders and their line items?
- **Type:** multi_hop | **Difficulty:** easy
- **Verdict:** CORRECT
- **Expected:** SALES_ORDER_HDR.TOTAL_AMT; ORDER_LINE_ITEM UNIT_PRICE, QUANTITY (>0), LINE_AMT=QUANTITY×UNIT_PRICE; join via ORDER_ID
- **Generated:** Correctly describes unit_price/line_amt and mentions payment AMOUNT; notes foreign-key ties
- **Analysis:** Strong alignment. (One nuance: expected says QUANTITY constrained >0; generated doesn’t explicitly state the constraint, but this does not contradict other facts.)
- **Retrieval:** gt_coverage=1.0, top_score=0.7, gate=proceed

## Anomalies & Recommendations

### Red Flags
- **Minor nuance risk in negative logic (Q014)**: negative questions are sensitive to business-rule interpretation. Even when grounded, small phrasing differences can cause rubric-level mismatch.
- **Lower GT coverage in multi-hop (Q010: 0.75)**: suggests traversal/context distillation sometimes omits the final hop details (e.g., TB_PRODUCT articulation).

### Recommendations
1. **Tighten negative-question answer templates**: require explicit mapping from expected condition → specific nullable field(s) / constraint(s) and avoid over-general statements.
2. **For multi-hop chains, enforce “full path inclusion” in generation**: when the question asks for hierarchy, include every node in the path (Customer → SalesOrder → LineItem → Product) even if earlier hops already imply it.
3. **Use reranker-driven context budgeting more assertively for hard multi-hop**: increase effective graph/context contribution when `query_type=multi_hop` and `gt_coverage<0.8` is observed (here, Q010).

## Comparison Notes (if applicable)
- This run appears to be effectively “best case” for the basics dataset: Builder is perfect and retrieval/grounding is near-universal. No ablation-vs-baseline comparison is available because the bundle does not include `ablation_context` or explicit changed flags relative to AB-00.