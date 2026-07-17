# AI-Judge Evaluation: AB-BEST-K20/05_edgecases_incomplete
**Evaluator:** (`gpt-5.4-nano-2026-03-17`) using `docs/AI_JUDGE_PROMPT.md`  
**Date:** 2026-07-17

---

# Ablation Study Evaluation: AB-BEST-K20 — 05_edgecases_incomplete

## Executive Summary
This run completed all 5 parsed DDL tables successfully with no Cypher failures and no ingestion issues, indicating strong **Builder Graph** stability even under edge-case/incomplete documentation conditions. Retrieval and grounding are also excellent at the question level (**20/20 grounded**, **avg_gt_coverage=1.0**), though several “missing/ambiguous” questions show the system answering “cannot determine” rather than resolving nuanced schema semantics—this is acceptable given the dataset’s intentionally incomplete ground truth. The main concern is **semantic adequacy under edge-case constraints**: a few answers (notably around NOT NULL enforcement and uniqueness/nullable constraints) appear to over-rely on “unknown/undocumented” and may not fully align with the expected handling of implicit constraints.

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
- `tables_parsed=5`, `tables_completed=5`, `all_tables_completed=true`
- `cypher_failed=false`, `failed_mappings=[]`, `ingestion_errors=[]`
- Triplet extraction and entity resolution succeeded at meaningful scale (`triplets_extracted=89`, `entities_resolved=78`)
- Parent/child chunking shows `0` for both, but that does **not** imply failure; it just indicates the particular trace produced no parent/child chunk artifacts.

**Verdict:** No builder instability signals; the graph was constructed reliably.

### 2. Retrieval Effectiveness (4/5)
- `grounded_rate=1.0`, `avg_gt_coverage=1.0` (strong recall of expected sources)
- `avg_top_score=0.7818` (healthy reranker confidence overall)
- However, some specific queries show only borderline retrieval quality:
  - `ec_004` (order_status valid values) has `retrieval_quality_score=0.7` with raw score substantially lower.
  - Several “unknown”/negative-style questions still proceeded (no abstentions), which is fine for non-negative queries but can indicate the pipeline is conservative mainly via the answer content rather than the gating behavior.
- There were **no gate abstentions** and no low-retrieval questions flagged at the pipeline level.

**Verdict:** Retrieval is clearly effective, but the “always answer” behavior on uncertainty-heavy edge cases suggests the quality gate is not exercising abstention much (which would matter more if the rubric expected abstain on unanswerable cases).

### 3. Answer Quality (4/5)
Overall grounding is perfect (`grounded_count=20`), and most answers match the expected “what is known vs not documented” intent.

**But** at least one case likely fails expected semantics:
- **`ec_013`** (“Are there any NOT NULL constraints defined in the schema?”)  
  - Expected: “No explicit NOT NULL constraints written” but note that PKs are implicitly NOT NULL; therefore answer should acknowledge the distinction.
  - Generated: says NOT NULL constraints are “not documented/unknown,” which contradicts the expected nuance about implicit PK non-nullability.

Additionally, there is a mild systematic pattern:
- For “missing/uncertain” questions, the model often responds “cannot find/enumeration missing” (correct), but sometimes does not fully incorporate implicit SQL properties or glossary-vs-DDL interpretations that the expected answers rely on.

**Therefore:** high correctness, but not uniformly precise on the tricky edge semantics.

### 4. Pipeline Health (5/5)
- `pipeline_health.cypher_failed=false`, `ingestion_errors_count=0`, `failed_mappings_count=0`
- `grader_inconsistencies=0`
- `total_grader_rejections=2` and `grader_consistency_valid=true` across questions shown.
- `gate_abstentions=0` with no instability.

**Verdict:** Stable and self-reflection loops did not indicate critical failures.

### 5. Ablation Impact (N/A)
Study id is **AB-BEST-K20**, but the bundle **does not include** an `ablation_context` object describing changes vs baseline (AB-00). Therefore rubric comparison-by-causality cannot be applied fairly.

---

## Dimension 3: Answer Quality (X/5) — Per-question highlights (best/worst)

### Best 3 (strong matches to expected intent)
- **`ec_001`** (“What is a customer?”): Correctly uses glossary definition fragment and the Client interchangeability note; grounded and aligned.
- **`ec_002`** (firstName vs first_name): Correctly identifies they are described as duplicates and only naming differs; matches expected constraints about “no documented semantic difference.”
- **`ec_006`** (ORDER_ITEMS.product_id vs PRODUCTS/INVENTORY): Correctly concludes “cannot determine” because doc explicitly says unverified and INVENTORY target is not defined.

### Worst 3 (most concerning mismatches)
1. **`ec_013`** (“Are there any NOT NULL constraints defined in the schema?”)  
   - Likely **INCORRECT** vs expected nuance about implicit NOT NULL for PRIMARY KEYs.
2. **`ec_004`** (“valid values for order_status”)  
   - Generated correctly says “cannot find,” but retrieval quality is borderline and answer content may be too close to “I cannot find” even though expected answer references glossary statuses (Pending/Processing/Completed/Cancelled/On Hold/Failed). In the provided context, those glossary statuses exist, but the generated answer chose not to incorporate them.
3. **`ec_016`** (“Is the sku column in PRODUCTS unique?”)  
   - Generated hedges that uniqueness is “intended but not confirmed,” matching the “UNIQUE?” with partial documentation idea; this is plausible but may diverge from expected if expected answer asserts “not defined” more directly.

Given rubric discipline (“semantic correctness > string matching”), the run is still mostly correct—but `ec_013` is the clearest expected-vs-generated semantic mismatch.

---

## Per-Question Deep Dive (all questions)

### ec_001: What is a customer?
- **Type:** missing_definition | **Difficulty:** unknown
- **Verdict:** CORRECT
- **Expected:** Customer glossary definition fragment; Client interchangeability; related terms.
- **Generated:** Defines Customer from glossary fragment; notes Client may be used interchangeably.
- **Analysis:** Matches key expected facts and appropriately limits to documented content.
- **Retrieval:** gt_coverage=1.0, top_score=0.9837, gate=proceed

### ec_002: What's the difference between firstName and first_name in the CUSTOMERS table?
- **Type:** duplicate_columns | **Difficulty:** unknown
- **Verdict:** CORRECT
- **Expected:** Both exist, identical VARCHAR(50); duplicates due to naming conventions; usage not documented.
- **Generated:** Both store first name; described as duplicate; no semantic processing difference documented.
- **Analysis:** Aligns with expected “identical/duplicate; no authoritative usage.”
- **Retrieval:** gt_coverage=1.0, top_score=0.8862, gate=proceed

### ec_003: Which customer column should be used as a foreign key reference: customer_id or CustomerID?
- **Type:** conflicting_references | **Difficulty:** unknown
- **Verdict:** CORRECTLY_ABSTAINED *(via “cannot determine” within proceed)*
- **Expected:** Ambiguous FK; context says “pending verification with DBA.”
- **Generated:** Explains ambiguity; cannot definitively choose.
- **Analysis:** Correct “cannot confirm” handling.
- **Retrieval:** gt_coverage=1.0, top_score=0.9255, gate=proceed

### ec_004: What are the valid values for order_status?
- **Type:** missing_constraint | **Difficulty:** unknown
- **Verdict:** PARTIALLY_CORRECT
- **Expected:** Glossary lists statuses (Pending, Processing, Completed, Cancelled, On Hold, Failed w/ missing definition); not enforced via CHECK; data dictionary says missing reference.
- **Generated:** Says cannot find valid values; references missing reference in ORDERS context.
- **Analysis:** Likely under-utilizes glossary enumerations present in retrieved contexts; should include at least the named statuses.
- **Retrieval:** gt_coverage=1.0, top_score=0.7, gate=proceed

### ec_005: Is there a difference between Product, Item, and SKU?
- **Type:** ambiguous_synonyms | **Difficulty:** unknown
- **Verdict:** CORRECT
- **Expected:** Product vs Item related; SKU is unique identifier; exact distinctions unclear but these are distinct concepts.
- **Generated:** Item is synonym/inventory context; SKU is unique variant identifier; notes other glossary terms.
- **Analysis:** Captures expected boundaries.
- **Retrieval:** gt_coverage=1.0, top_score=0.7, gate=proceed

### ec_006: Which table should ORDER_ITEMS.product_id reference: PRODUCTS or INVENTORY?
- **Type:** ambiguous_reference | **Difficulty:** unknown
- **Verdict:** CORRECT
- **Expected:** “PRODUCTS (or INVENTORY?)” unverified; cannot determine from available docs.
- **Generated:** Concludes not determinable; describes both support product_id referencing but schema says unverified.
- **Analysis:** Matches expected “cannot determine.”
- **Retrieval:** gt_coverage=1.0, top_score=0.9609, gate=proceed

### ec_007: What's the difference between Revenue and Sales?
- **Type:** circular_definition | **Difficulty:** unknown
- **Verdict:** CORRECT
- **Expected:** Both circular; no clear distinction.
- **Generated:** Describes circularity and absence of non-circular distinction.
- **Analysis:** Fully aligned.
- **Retrieval:** gt_coverage=1.0, top_score=0.7, gate=proceed

### ec_008: Can one order have multiple payments?
- **Type:** conflicting_cardinality | **Difficulty:** unknown
- **Verdict:** CORRECT
- **Expected:** PAYMENTS.order_id suggests many payments; glossary relationship uncertain; ORDERS payment_method/status columns conflict.
- **Generated:** Says cannot be determined definitively from available context; notes unclear relationship and lack of uniqueness/cardi constraints.
- **Analysis:** Correctly avoids over-claiming.
- **Retrieval:** gt_coverage=1.0, top_score=0.7, gate=proceed

### ec_009: What payment methods are accepted?
- **Type:** missing_enum_values | **Difficulty:** unknown
- **Verdict:** CORRECT
- **Expected:** No documented valid values; examples not enumerated.
- **Generated:** States valid values are not documented; acknowledges example mention only.
- **Analysis:** Matches expected.
- **Retrieval:** gt_coverage=1.0, top_score=0.7, gate=proceed

### ec_010: What's the correct table name: ORDER_ITEMS or ORDER_DETAILS?
- **Type:** naming_ambiguity | **Difficulty:** unknown
- **Verdict:** CORRECTLY_ABSTAINED *(via “cannot definitively confirm” message)*
- **Expected:** DDL creates ORDER_ITEMS; dictionary shows ambiguity and notes app may reference differently.
- **Generated:** Says context cannot definitively confirm schema-level name; mentions business concept uses order_items.
- **Analysis:** Slightly conservative vs expected “DDL creates ORDER_ITEMS,” but still consistent with “documentation ambiguity” framing.
- **Retrieval:** gt_coverage=1.0, top_score=0.9627, gate=proceed

### ec_011: Which date column should be used to track when an order was created?
- **Type:** duplicate_columns | **Difficulty:** unknown
- **Verdict:** CORRECT
- **Expected:** order_date vs OrderDate vs created_at exist; no guidance on app usage.
- **Generated:** Chooses order_date as “order created” based on its description.
- **Analysis:** This is stronger than “no guidance,” but it is grounded in the provided description; acceptable given expected may treat descriptions as guidance.
- **Retrieval:** gt_coverage=1.0, top_score=0.9581, gate=proceed

### ec_012: What does the Failed order status mean?
- **Type:** missing_definition | **Difficulty:** unknown
- **Verdict:** CORRECT
- **Expected:** Failed exists but definition missing.
- **Generated:** States definition missing; no meaning found.
- **Analysis:** Perfect match.
- **Retrieval:** gt_coverage=1.0, top_score=0.7, gate=proceed

### ec_013: Are there any NOT NULL constraints defined in the schema?
- **Type:** missing_constraints | **Difficulty:** unknown
- **Verdict:** INCORRECT
- **Expected:** No explicit NOT NULL in DDL; PKs implicitly NOT NULL; non-PK columns nullable by default.
- **Generated:** Says NOT NULL is not documented / treated as unknown (based on “assumed, not verified” language).
- **Analysis:** Misses expected nuance about PRIMARY KEY implicit NOT NULL.
- **Retrieval:** gt_coverage=null, top_score=0.7628, gate=proceed

### ec_014: What's the difference between unit_price and current_price in PRODUCTS?
- **Type:** duplicate_columns | **Difficulty:** unknown
- **Verdict:** CORRECT
- **Expected:** Both exist; difference not explained beyond “different from unit_price.”
- **Generated:** Uses “Standard selling price” vs “different from unit_price” and notes lack of further detail.
- **Analysis:** Aligned.
- **Retrieval:** gt_coverage=1.0, top_score=0.7443, gate=proceed

### ec_015: When is an invoice generated vs payment processed?
- **Type:** missing_workflow | **Difficulty:** unknown
- **Verdict:** CORRECT
- **Expected:** Timing and sequence not defined; invoice definition exists but no workflow.
- **Generated:** States invoice timing relative to payment not specified; notes no invoice events in provided schema.
- **Analysis:** Correct “unavailable” answer.
- **Retrieval:** gt_coverage=1.0, top_score=0.7, gate=proceed

### ec_016: Is the sku column in PRODUCTS unique?
- **Type:** missing_uniqueness | **Difficulty:** unknown
- **Verdict:** CORRECT
- **Expected:** sku marked “UNIQUE?” but no UNIQUE constraint in DDL; no index documented.
- **Generated:** Says uniqueness intention appears but not confirmed; does not claim uniqueness guarantee.
- **Analysis:** Matches expected “not proven/enumerated.”
- **Retrieval:** gt_coverage=1.0, top_score=0.7516, gate=proceed

### ec_017: What is the relationship between customers and orders?
- **Type:** ambiguous_relationship | **Difficulty:** unknown
- **Verdict:** CORRECT
- **Expected:** One customer can place multiple orders but unclear whether “accounts” place orders; FK ambiguity noted.
- **Generated:** States no precise DB relationship can be determined; uses glossary conceptual rule with explicit uncertainty.
- **Analysis:** Correctly preserves “unclear” boundary.
- **Retrieval:** gt_coverage=1.0, top_score=0.7, gate=proceed

### ec_018: Which price column represents what the customer actually pays?
- **Type:** semantic_ambiguity | **Difficulty:** unknown
- **Verdict:** CORRECT
- **Expected:** Multiple price columns; no explanation of which represents actual paid amount with discounts/timing.
- **Generated:** States context does not define which column equals what customer actually pays.
- **Analysis:** Correct uncertainty handling.
- **Retrieval:** gt_coverage=1.0, top_score=0.7, gate=proceed

### ec_019: What's the difference between Shipment, Delivery, and Fulfillment?
- **Type:** overlapping_concepts | **Difficulty:** unknown
- **Verdict:** CORRECT
- **Expected:** Shipment -> delivering goods; Delivery -> completion when goods reach customer; Fulfillment -> preparing & delivering, encompasses both; boundaries unclear but superset.
- **Generated:** Repeats the glossary definitions directly.
- **Analysis:** Aligned.
- **Retrieval:** gt_coverage=1.0, top_score=0.7, gate=proceed

### ec_020: Are foreign key constraints enforced in the schema?
- **Type:** missing_fk_enforcement | **Difficulty:** unknown
- **Verdict:** CORRECT
- **Expected:** No FK enforced in DDL; data dictionary documents relationships.
- **Generated:** Says context shows FK relationships but doesn’t confirm actual enforcement; cannot determine.
- **Analysis:** Matches the expected “not confirmed/enforcement not established” framing.
- **Retrieval:** gt_coverage=1.0, top_score=0.7, gate=proceed

---

## Anomalies & Recommendations

### Red Flags
- **`ec_013` semantics mismatch**: likely failure to incorporate **implicit SQL NOT NULL for PRIMARY KEYs**, while expected answer explicitly requires that nuance.
- Several **“missing_constraint / missing_enum / missing_workflow”** tasks are answered correctly as “not documented,” but **`ec_004`** suggests the model may under-use glossary enumerations even when they are present in retrieved context.
- `avg_gt_coverage=1.0` is strong, but **`ec_013` has `gt_coverage=null`**, suggesting some ground-truth linkage or source accounting inconsistency for constraints-type questions.

### Recommendations
1. **Add an implicit-constraint reasoning layer** for DDL/SQL correctness:
   - Treat PRIMARY KEY columns as implicitly `NOT NULL` even when DDL doesn’t explicitly include it.
   - When the question asks “are NOT NULL constraints defined,” separate:
     - explicit `NOT NULL` keyword usage
     - implicit `PRIMARY KEY` non-nullability
2. **Improve glossary-vs-DDL answer composition**:
   - For enum-like questions (e.g., `order_status valid values`), if glossary enumerations exist, prefer listing them and then note enforcement absence.
3. **Consider abstention tuning for edgecases**:
   - Even though grounding is perfect, if the intent is governance, distinguishing “cannot determine” vs “documented uncertainty” could be made more explicit in outputs (or abstain when the expected answer is explicitly “no information found”).
4. **Validate expected-vs-generated equivalence on “cannot determine” questions**:
   - Ensure the system doesn’t over-generalize uncertainty when glossary contains the needed mapping.

---

## Comparison Notes (if applicable)
- **Ablation Impact scoring is N/A** because the bundle lacks explicit `ablation_context` describing changes vs baseline AB-00.