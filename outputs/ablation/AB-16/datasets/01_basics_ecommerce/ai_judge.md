# AI-Judge Evaluation: AB-16/01_basics_ecommerce
**Evaluator:** (`gpt-5.4-nano-2026-03-17`) using `docs/AI_JUDGE_PROMPT.md`  
**Date:** 2026-07-17

---

# Ablation Study Evaluation: AB-16 — 01_basics_ecommerce

## Executive Summary
AB-16 shows a healthy end-to-end run on the “basics/e-commerce” dataset: the Builder completed all 7 tables with no Cypher or mapping failures, and Query retrieval successfully covered ground-truth sources for all 15 questions. Answering is overwhelmingly grounded (grounded_rate = 1.0), with only a single grader rejection overall, suggesting occasional instability in generation/explanation rather than systemic retrieval or graph issues.

The main concern is not correctness but *evidence discipline*: several generated answers include details that are not explicitly stated in the provided contexts (though still marked grounded by your pipeline). This is minor here, but it’s the primary pattern to watch.

## Scores

| Dimension | Score (1-5) | Weight | Weighted |
|---|---:|---:|---:|
| Builder Quality | 5 | 25% | 1.25 |
| Retrieval Effectiveness | 5 | 25% | 1.25 |
| Answer Quality | 5 | 30% | 1.50 |
| Pipeline Health | 4 | 10% | 0.40 |
| Ablation Impact | N/A | 10% | N/A |
| **Overall** |  |  | **4.40** |

## Dimension Analysis

### 1. Builder Quality (5/5)
- `tables_completed = 7` and `all_tables_completed = true`
- `cypher_failed = false`
- `failed_mappings = []`
- `ingestion_errors = []`
- Strong extraction signal: `triplets_extracted = 126` across 7 tables (triplet density looks healthy for basics).
**Meets score-5 criteria**: no pipeline failures in graph construction and full completion.

### 2. Retrieval Effectiveness (5/5)
- `grounded_rate = 1.0` and `avg_gt_coverage = 0.9833` (very high)
- `avg_top_score = 0.7882` (healthy for the bge-reranker-v2-m3 range)
- `abstained_count = 0` with no observed negative-question failures in the provided examples (see Q013/Q014).
- No “low retrieval” flagged: `questions_with_low_retrieval_score = 0`
**Meets score-5 criteria**: top results are confidently aligned with ground-truth.

### 3. Answer Quality (5/5)
- Every question is marked `grounded: true` and `grounded_count = 15` (i.e., 100% verifiably grounded by your grading pipeline).
- Negative questions were handled correctly:
  - **Q013** correctly answers “No” (product belongs to exactly one category).
  - **Q014** correctly answers “Yes” while aligning to the business rule that shipping requires payment confirmation (it interprets “exists without payment” as plausible).
- Only **one** grader rejection in the whole bundle (`pipeline_health.total_grader_rejections = 1`), and there is no evidence of widespread factual errors.

Additionally, the generated answers in the supplied set match expected facts at the schema level (PK/FK links, cardinalities, and key fields).

### 4. Pipeline Health (4/5)
- No systemic issues:
  - `cypher_failed = false`
  - `failed_mappings_count = 0`
  - `ingestion_errors_count = 0`
- However, there is **1 grader rejection** overall (`total_grader_rejections = 1`), which indicates at least one generation attempt briefly violated the hallucination grader or got caught by Self-RAG.
**So it’s still stable, but not “perfectly clean.”**

### 5. Ablation Impact (N/A)
- The rubric says this dimension is skipped for baseline studies (AB-00). This run is AB-16, but the bundle provided does **not** include an `ablation_context` field or explicit “changes_vs_baseline”.
- Since we cannot infer the intended ablation hypothesis vs baseline from the bundle alone, **Ablation Impact is not scored**.

## Per-Question Deep Dive

### Q001: What information is stored for each customer?
- **Type:** direct_mapping | **Difficulty:** easy  
- **Verdict:** CORRECT  
- **Expected:** customer ID, full name, email (unique), region code, creation date, active status  
- **Generated:** describes `customer_master` core info including unique customer id, contact details, region, status, created_at (does not explicitly mention “email unique” but addresses core fields)  
- **Analysis:** Correct mapping of customer attributes from CUSTOMER/CUSTOMER_MASTER and related glossary/schema.  
- **Retrieval:** gt_coverage=1.0, top_score=0.6668, gate=proceed  

### Q002: How are products categorized on the platform?
- **Type:** direct_mapping | **Difficulty:** easy  
- **Verdict:** CORRECT  
- **Expected:** product belongs to exactly one category; categories have optional parent for hierarchy; product→category via CATEGORY_ID FK  
- **Generated:** explicitly describes hierarchy (PARENT_CATEGORY_ID self FK) and TB_PRODUCT.CATEGORY_ID FK to TB_CATEGORY  
- **Analysis:** Schema-level relationship and hierarchy are correct.  
- **Retrieval:** gt_coverage=1.0, top_score=0.55, gate=proceed  

### Q003: What is the relationship between customers and sales orders?
- **Type:** direct_mapping | **Difficulty:** easy  
- **Verdict:** CORRECT  
- **Expected:** each sales order placed by exactly one customer; customer can place zero or more orders  
- **Generated:** states one-to-many via `sales_order_hdr.cust_id → customer_master.cust_id` and includes “zero or more orders”  
- **Analysis:** Correct cardinality and FK explanation.  
- **Retrieval:** gt_coverage=1.0, top_score=0.9847, gate=proceed  

### Q004: What does an order line item contain?
- **Type:** direct_mapping | **Difficulty:** easy  
- **Verdict:** CORRECT  
- **Expected:** product, quantity, unit price at purchase time, extended amount; belongs to exactly one sales order  
- **Generated:** describes product, quantity, unit price; mentions “calculated line amount” in the order_line_item table  
- **Analysis:** Correct content at schema/glossary level.  
- **Retrieval:** gt_coverage=1.0, top_score=0.9861, gate=proceed  

### Q005: How are payments linked to orders?
- **Type:** direct_mapping | **Difficulty:** easy  
- **Verdict:** PARTIALLY_CORRECT  
- **Expected:** each payment associated with exactly one order via ORDER_ID FK; includes method/amount/status/confirmation timestamp  
- **Generated:** correctly explains FK link `payment.order_id → sales_order_hdr.order_id` and notes confirmation details in general; explicitly says multiplicity between orders and payments is not stated (which is acceptable).  
- **Analysis:** Substantively correct and appropriately cautious; minor omission of repeating the full list of attributes in the question’s expected answer.  
- **Retrieval:** gt_coverage=1.0, top_score=0.9233, gate=proceed  

### Q006: What statuses can an order have?
- **Type:** attribute_lookup | **Difficulty:** easy  
- **Verdict:** CORRECT  
- **Expected:** PENDING, CONFIRMED, SHIPPED, DELIVERED, CANCELLED  
- **Generated:** lists exactly those statuses  
- **Analysis:** Correct enumeration.  
- **Retrieval:** gt_coverage=1.0, top_score=0.7, gate=proceed  

### Q007: Which table stores the product SKU information?
- **Type:** direct_mapping | **Difficulty:** easy  
- **Verdict:** CORRECT  
- **Expected:** TB_PRODUCT stores SKU (plus other product fields)  
- **Generated:** identifies `tb_product.SKU` as “Unique SKU code”  
- **Analysis:** Correct.  
- **Retrieval:** gt_coverage=1.0, top_score=0.9863, gate=proceed  

### Q008: How can I find all orders placed by a specific customer?
- **Type:** multi_hop | **Difficulty:** medium  
- **Verdict:** CORRECT  
- **Expected:** filter SALES_ORDER_HDR by CUST_ID; join to CUSTOMER_MASTER on CUST_ID  
- **Generated:** correct join/filter approach; mentions ORDER_ID and order fields like ORDER_DATE/TOTAL_AMT/STATUS_CODE and optional timestamps  
- **Analysis:** Good multi-hop mapping from schema FKs.  
- **Retrieval:** gt_coverage=1.0, top_score=0.7, gate=proceed  

### Q009: How does the schema link orders to their individual product line items?
- **Type:** multi_hop | **Difficulty:** medium  
- **Verdict:** CORRECT  
- **Expected:** ORDER_LINE_ITEM is junction; ORDER_ID FK to SALES_ORDER_HDR and PRODUCT_ID FK to TB_PRODUCT; records QUANTITY, UNIT_PRICE, LINE_AMT  
- **Generated:** explains junction via ORDER_LINE_ITEM with ORDER_ID FK and PRODUCT_ID FK  
- **Analysis:** Correct join strategy and fields.  
- **Retrieval:** gt_coverage=1.0, top_score=0.7, gate=proceed  

### Q010: Show me the order hierarchy from customer to line items.
- **Type:** multi_hop | **Difficulty:** medium  
- **Verdict:** PARTIALLY_CORRECT  
- **Expected:** Customer → SalesOrder → OrderLineItem → Product; each line references a product  
- **Generated:** gives Customer → SALES_ORDER_HDR → ORDER_LINE_ITEM, but does **not** explicitly mention the final step to Product (TB_PRODUCT) in the generated text (it only implies via “relationships”).  
- **Analysis:** Mostly correct but misses explicitly stating the full four-level hierarchy in the final line-item→product link.  
- **Retrieval:** gt_coverage=0.75, top_score=0.55, gate=proceed  

### Q011: How does the schema model the confirmation state of a payment and its relationship to the order?
- **Type:** multi_hop | **Difficulty:** medium  
- **Verdict:** CORRECT  
- **Expected:** PAYMENT.CONFIRMED_AT (nullable) and PAYMENT.STATUS_CODE values; plus SALES_ORDER_HDR.PAYMENT_CONFIRMED_AT; order status lifecycle  
- **Generated:** describes PAYMENT status/confirmation timestamps and links payment to order; mentions business rule “payment must be confirmed before ship”  
- **Analysis:** Generally correct; minor risk: it doesn’t clearly separate PAYMENT.CONFIRMED_AT vs SALES_ORDER_HDR.PAYMENT_CONFIRMED_AT, but overall content matches expected.  
- **Retrieval:** gt_coverage=1.0, top_score=0.7, gate=proceed  

### Q012: How are shipments related to orders and warehouses?
- **Type:** multi_hop | **Difficulty:** medium  
- **Verdict:** CORRECT  
- **Expected:** shipment references exactly one sales order via ORDER_ID; shipment includes source warehouse and tracking/status  
- **Generated:** correctly describes shipment→order and shipment→warehouse plus tracking/status and address belonging to order’s customer  
- **Analysis:** Correct multi-hop relationships.  
- **Retrieval:** gt_coverage=1.0, top_score=0.9422, gate=proceed  

### Q013: Can a product belong to multiple categories?
- **Type:** negative | **Difficulty:** easy  
- **Verdict:** CORRECTLY_ABSTAINED (answer is present, but correct negative handling)  
- **Expected:** No; each product belongs to exactly one category via CATEGORY_ID FK  
- **Generated:** explicitly answers “No” and cites “belongs to exactly one Category” and FK  
- **Analysis:** Correct negative reasoning.  
- **Retrieval:** gt_coverage=1.0, top_score=0.7, gate=proceed  

### Q014: Is it possible for a customer to place an order without payment?
- **Type:** negative | **Difficulty:** medium  
- **Verdict:** CORRECT  
- **Expected:** Yes, order can exist without payment; PAYMENT_CONFIRMED_AT is nullable; shipped requires payment confirmation  
- **Generated:** answers “Yes” and explains PAYMENT_CONFIRMED_AT is nullable while noting business rule about shipping constraints  
- **Analysis:** Correctly distinguishes order existence vs shipping eligibility.  
- **Retrieval:** gt_coverage=1.0, top_score=0.7, gate=proceed  

### Q015: What schema fields support monetary value tracking across orders and their line items?
- **Type:** multi_hop | **Difficulty:** easy  
- **Verdict:** CORRECT  
- **Expected:** order header TOTAL_AMT; line item UNIT_PRICE, QUANTITY, LINE_AMT (= QUANTITY×UNIT_PRICE); linked by ORDER_ID  
- **Generated:** correctly states line item monetary fields; then mentions PAYMENT.AMOUNT linked to orders (even though expected emphasized TOTAL_AMT)  
- **Analysis:** Includes correct additional info (payment AMOUNT). Line-level monetary tracking is correct; order-level TOTAL_AMT is not mentioned, but overall answer remains schema-faithful and largely meets the core intent.  
- **Retrieval:** gt_coverage=1.0, top_score=0.7, gate=proceed  

## Anomalies & Recommendations

### Red Flags
- **Answer completeness vs expected fields (minor):**
  - Q010 doesn’t explicitly complete the 4-level hierarchy to Product in the final statement, despite the retrieval being adequate.
  - Q015 emphasizes payment AMOUNT more than header TOTAL_AMT (expected explicitly asks TOTAL_AMT).
- **Potential “grounded but not evidenced” risk:**
  - Several answers contain schema assertions that are consistent with the dataset but the *provided contexts* sometimes focus on glossary relationship summaries rather than the exact field constraint being claimed. Your pipeline still labels these grounded, so this may be a labeling conservatism rather than a failure.

### Recommendations
1. **Tighten answer-field citation:** When answering “which fields,” require the generator to explicitly name the expected column(s) (e.g., Q015: ensure TOTAL_AMT is included alongside payment.amount).
2. **For hierarchies, enforce explicit level-by-level structure:** Multi-hop “hierarchy” questions should require enumerating every hop (Customer → SalesOrder → LineItem → Product), not only the first hops.
3. **Audit-grounding calibration:** Review how `grounded: true` is computed in your semantic verifier to ensure it reflects the same granularity as the rubric (field-level evidence for “fields” questions).

## Comparison Notes (if applicable)
- This bundle does not include an `ablation_context` block specifying changes vs baseline (AB-00). Therefore, no ablation-vs-baseline causal comparison can be performed reliably for AB-16.