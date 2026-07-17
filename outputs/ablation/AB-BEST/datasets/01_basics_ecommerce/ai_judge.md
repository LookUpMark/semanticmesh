# AI-Judge Evaluation: AB-BEST/01_basics_ecommerce
**Evaluator:** (`gpt-5.4-nano-2026-03-17`) using `docs/AI_JUDGE_PROMPT.md`  
**Date:** 2026-07-17

---

# Ablation Study Evaluation: AB-BEST — 01_basics_ecommerce

## Executive Summary
AB-BEST on the e-commerce basics dataset shows an excellent end-to-end run: the builder completed all tables with no Cypher failures or ingestion errors, and the query stage achieved perfect grounding with `avg_gt_coverage = 1.0` across all 15 questions. Retrieval confidence is generally strong (`avg_top_score = 0.783`) and the system produced correct schema/graph answers for both positive and negative question types, with zero grader rejections and no pipeline health issues.

The main caveat is not a failure signal but a completeness mismatch in **Q015**: the generated answer correctly notes that the order-level total field wasn’t clearly evidenced in the retrieved snippet, while the expected answer asserts a specific field (`SALES_ORDER_HDR.TOTAL_AMT`). This appears to be a context-utilization/trace coverage artifact rather than a KG inconsistency.

## Scores

| Dimension | Score (1-5) | Weight | Weighted |
|---|---:|---:|---:|
| Builder Quality | 5 | 25% | 1.25 |
| Retrieval Effectiveness | 5 | 25% | 1.25 |
| Answer Quality | 4 | 30% | 1.20 |
| Pipeline Health | 5 | 10% | 0.50 |
| Ablation Impact | 5 | 10% | 0.50 |
| **Overall** |  |  | **4.70** |

## Dimension Analysis

### 1. Builder Quality (5/5)
- `tables_completed = 7`, `all_tables_completed = true`
- `cypher_failed = false`
- `failed_mappings = []`, `ingestion_errors = []`
- Strong extraction/graph construction signals: `triplets_extracted = 68`, `entities_resolved = 29`
- No builder skips or parent/child chunking artifacts impacting ingestion (`parent_chunks = 0`, `child_chunks = 0`)

### 2. Retrieval Effectiveness (5/5)
- `grounded_rate = 1.0`, `abstained_count = 0` (no false abstentions)
- `avg_gt_coverage = 1.0` for all questions
- `avg_top_score = 0.783` (healthy semantic confidence for the reranker)
- `pipeline_health.questions_with_low_retrieval_score = 0`
- Per-question retrieval_quality_score is consistently high (many at 0.7 floor-adjusted; several near ~0.95+), and no query shows `gt_coverage = 0`.

### 3. Answer Quality (4/5)
Overall, answers are semantically correct and grounded for essentially the entire set, but **Q015** shows a likely omission/field-identification mismatch:
- **Q015:** Expected specifically states `SALES_ORDER_HDR.TOTAL_AMT (DECIMAL(12,2) NOT NULL)`. Generated claims the order header “does not list any specific monetary total field/column name/type” in the retrieved excerpt, though later contexts include a “Total monetary value” mention in the glossary. This is the only notable deviation from the expected schema specificity.
- All other shown questions match expected facts (including negative constraints in **Q013** and **Q014**), and no hallucination failures are indicated.

### 4. Pipeline Health (5/5)
- `total_grader_rejections = 0`
- `grader_inconsistencies = 0`
- `gate_abstentions = 0`
- `cypher_failed = false`, `failed_mappings_count = 0`, `ingestion_errors_count = 0`
- End-to-end indicates stable operation with no self-reflection loops needing resolution.

### 5. Ablation Impact (5/5)
Study id is **AB-BEST**, and the run exhibits “best-case” behavior across all tracked components:
- Builder is perfect (all tables completed, no Cypher errors).
- Retrieval quality is perfect on GT coverage and high on reranker confidence.
- Answer generation passes all graders (0 rejections) with correct handling of both direct and negative question types.
Even without explicit “changes_vs_baseline” fields, the observed outcome corresponds to the expected “best/optimal configuration” pattern strongly enough to award a top score.

## Per-Question Deep Dive

### Q001: What information is stored for each customer?
- **Type:** direct_mapping | **Difficulty:** easy
- **Verdict:** CORRECT
- **Expected:** ID, full name, email (unique), region code, creation date, active status
- **Generated:** Describes customer_master storing identifiers/contact details/region/account status/created-at and CUST_ID + created_at; aligns with stored fields conceptually.
- **Analysis:** Correctly grounded in CUSTOMER/CUSTOMER_MASTER and key fields (ID and created_at); does not explicitly restate “email must be unique” but remains semantically consistent with customer identity fields.
- **Retrieval:** gt_coverage=1.0, top_score=0.783422826363825, gate=proceed

### Q002: How are products categorized on the platform?
- **Type:** direct_mapping | **Difficulty:** easy
- **Verdict:** CORRECT
- **Expected:** Product → exactly one Category; categories form hierarchy via parent category
- **Generated:** PRODUCT has CATEGORY_ID FK to TB_CATEGORY; TB_CATEGORY has PARENT_CATEGORY_ID self-reference.
- **Analysis:** Fully matches schema + glossary hierarchy relationship.
- **Retrieval:** gt_coverage=1.0, top_score=0.783..., gate=proceed

### Q003: What is the relationship between customers and sales orders?
- **Type:** direct_mapping | **Difficulty:** easy
- **Verdict:** CORRECT
- **Expected:** SalesOrder placed by exactly one Customer; customer can have zero or more orders
- **Generated:** Uses glossary “zero or more” and schema FK cust_id -> customer_master.cust_id; clarifies direction not required by FK.
- **Analysis:** Correct relationship semantics and cardinality.
- **Retrieval:** gt_coverage=1.0, top_score=0.9846936454393053, gate=proceed

### Q004: What does an order line item contain?
- **Type:** direct_mapping | **Difficulty:** easy
- **Verdict:** CORRECT
- **Expected:** product, quantity, unit price at purchase time, extended amount; belongs to exactly one order
- **Generated:** States product/quantity/unit price/total line amount; includes membership to the order conceptually via relationships.
- **Analysis:** Matches glossary + line-item column definition.
- **Retrieval:** gt_coverage=1.0, top_score=0.9492946352021694, gate=proceed

### Q005: How are payments linked to orders?
- **Type:** direct_mapping | **Difficulty:** easy
- **Verdict:** CORRECT
- **Expected:** Payment → exactly one SalesOrder via ORDER_ID; includes method/amount/status/confirmation timestamp
- **Generated:** payment.order_id references sales_order_hdr.order_id; describes key payment attributes.
- **Analysis:** Correct FK and intent.
- **Retrieval:** gt_coverage=1.0, top_score=0.909103245693355, gate=proceed

### Q006: What statuses can an order have?
- **Type:** attribute_lookup | **Difficulty:** easy
- **Verdict:** CORRECT
- **Expected:** PENDING, CONFIRMED, SHIPPED, DELIVERED, CANCELLED
- **Generated:** Lists exactly those five statuses from glossary.
- **Analysis:** Perfect.
- **Retrieval:** gt_coverage=1.0, top_score=0.7, gate=proceed

### Q007: Which table stores the product SKU information?
- **Type:** direct_mapping | **Difficulty:** easy
- **Verdict:** CORRECT
- **Expected:** TB_PRODUCT stores SKU (and other product attributes)
- **Generated:** States tb_product contains the SKU field and describes it as “Unique SKU code”.
- **Analysis:** Correct table identification.
- **Retrieval:** gt_coverage=1.0, top_score=0.9900635812940538, gate=proceed

### Q008: How can I find all orders placed by a specific customer?
- **Type:** multi_hop | **Difficulty:** medium
- **Verdict:** CORRECT
- **Expected:** Filter SALES_ORDER_HDR by CUST_ID; join to CUSTOMER_MASTER on CUST_ID for customer identity
- **Generated:** Explains join via CUST_ID and filtering SALES_ORDER_HDR; notes schema doesn’t show mapping from email to CUST_ID in provided contexts.
- **Analysis:** Matches expected approach and appropriately limits what’s evidenced.
- **Retrieval:** gt_coverage=1.0, top_score=0.7, gate=proceed

### Q009: How does the schema link orders to their individual product line items?
- **Type:** multi_hop | **Difficulty:** medium
- **Verdict:** CORRECT
- **Expected:** Junction semantics via ORDER_LINE_ITEM with ORDER_ID -> SALES_ORDER_HDR and PRODUCT_ID -> TB_PRODUCT; includes quantity/unit_price/line_amt
- **Generated:** Correctly explains ORDER_ID FK and PRODUCT_ID FK plus line-level fields.
- **Analysis:** Correct join path and junction table role.
- **Retrieval:** gt_coverage=1.0, top_score=0.7, gate=proceed

### Q010: Show me the order hierarchy from customer to line items.
- **Type:** multi_hop | **Difficulty:** medium
- **Verdict:** CORRECT
- **Expected:** CUSTOMER_MASTER → SALES_ORDER_HDR → ORDER_LINE_ITEM → TB_PRODUCT
- **Generated:** Explains the foreign key join path customer -> order via CUST_ID and order -> lines via ORDER_ID; includes line fields.
- **Analysis:** Correct hierarchy and join keys.
- **Retrieval:** gt_coverage=1.0, top_score=0.7, gate=proceed

### Q011: How does the schema model the confirmation state of a payment and its relationship to the order?
- **Type:** multi_hop | **Difficulty:** medium
- **Verdict:** CORRECT
- **Expected:** PAYMENT.CONFIRMED_AT + STATUS_CODE; SALES_ORDER_HDR.PAYMENT_CONFIRMED_AT mirrors; order STATUS_CODE lifecycle
- **Generated:** Covers both payment-level and order-level timestamps; links via payment.order_id and status semantics.
- **Analysis:** Correct modeling description.
- **Retrieval:** gt_coverage=1.0, top_score=0.7, gate=proceed

### Q012: How are shipments related to orders and warehouses?
- **Type:** multi_hop | **Difficulty:** medium
- **Verdict:** CORRECT
- **Expected:** SHIPMENT.ORDER_ID -> SALES_ORDER_HDR; shipment includes source warehouse, tracking, status
- **Generated:** Explains single order linkage and warehouse source relationship; describes tracking/status fields.
- **Analysis:** Correct.
- **Retrieval:** gt_coverage=1.0, top_score=0.9181872878284922, gate=proceed

### Q013: Can a product belong to multiple categories?
- **Type:** negative | **Difficulty:** easy
- **Verdict:** CORRECT
- **Expected:** No; belongs to exactly one category; tb_product.CATEGORY_ID FK to tb_category
- **Generated:** Says “No” and cites glossary + FK relationship category_id -> tb_category.category_id.
- **Analysis:** Correct negative handling.
- **Retrieval:** gt_coverage=1.0, top_score=0.7, gate=proceed

### Q014: Is it possible for a customer to place an order without payment?
- **Type:** negative | **Difficulty:** medium
- **Verdict:** PARTIALLY_CORRECT
- **Expected:** Yes, orders can exist without payment because PAYMENT_CONFIRMED_AT is nullable and no constraint prevents order row existence; shipping constrained by “payment must be confirmed”
- **Generated:** Answers “Yes” and argues constraints only restrict shipping; payment confirmation timestamp/delivery timestamp nullable indicates orders can exist before payments.
- **Analysis:** Substantively matches expected; could be slightly more explicit about “order created first” framing, but still aligns with the provided expected logic.
- **Retrieval:** gt_coverage=1.0, top_score=0.7, gate=proceed

### Q015: What schema fields support monetary value tracking across orders and their line items?
- **Type:** multi_hop | **Difficulty:** easy
- **Verdict:** PARTIALLY_CORRECT
- **Expected:** SALES_ORDER_HDR.TOTAL_AMT for header totals; ORDER_LINE_ITEM.UNIT_PRICE, QUANTITY, LINE_AMT for lines; join via ORDER_ID
- **Generated:** Correctly states line-item monetary fields (UNIT_PRICE, LINE_AMT, QUANTITY). However, it claims the knowledge graph excerpt “does not list any specific monetary total field” for SALES_ORDER_HDR, and does not name TOTAL_AMT, while later sources do indicate “Total monetary value” exists.
- **Analysis:** Missing one key expected field name/type at the order header level; everything else is correct.
- **Retrieval:** gt_coverage=1.0, top_score=0.7, gate=proceed

## Anomalies & Recommendations

### Red Flags
- **Q015 field identification lapse:** Expected `SALES_ORDER_HDR.TOTAL_AMT` is not explicitly used in the generated answer, despite the glossary describing “Total monetary value” and earlier structured schema text in the overall bundle that includes TOTAL_AMT. This suggests either:
  1) the retrieved context for Q015 did not include the specific `TOTAL_AMT` row from the data dictionary snippet, or  
  2) the model failed to extract and commit the exact column name/type from available context.

### Recommendations
1. **Tighten “schema field naming” in generation prompts** for attribute-specific questions (TOTAL_AMT vs generic “total value”). A simple rule: if expected answer requests a concrete column name, the generator should only respond with a column name that appears verbatim (or unambiguously) in retrieved contexts.
2. **Improve context selection for order-level monetary fields**: ensure retrieval caps and source diversification always include the `SALES_ORDER_HDR` column details, not only glossary fragments, for questions containing “monetary value” or “total”.
3. Add a **post-generation consistency check**: if the question contains “field(s)” and expected includes a specific identifier (like `TOTAL_AMT`), verify the identifier exists in `contexts_retrieved` or explicitly state “not found in retrieved context”—rather than implying absence.

## Comparison Notes (if applicable)
- This is AB-BEST; no `changes_vs_baseline` object is provided. However, the observed metrics indicate best-case performance across builder, retrieval, and validation: perfect grounding, no abstentions, no grader rejections, and full table completion.