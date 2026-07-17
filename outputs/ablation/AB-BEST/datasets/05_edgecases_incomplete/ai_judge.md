# AI-Judge Evaluation: AB-BEST/05_edgecases_incomplete
**Evaluator:** (`gpt-5.4-nano-2026-03-17`) using `docs/AI_JUDGE_PROMPT.md`  
**Date:** 2026-07-17

---

# Ablation Study Evaluation: AB-BEST — 05_edgecases_incomplete

## Executive Summary
AB-BEST shows a **healthy end-to-end pipeline**: all 5 parsed tables were completed in the builder, no Cypher or ingestion failures occurred, and the query layer **answered every question without abstaining** while achieving **high grounding (grounded_rate=1.0)**. The main concern is that several “edgecase” questions revolve around *unknown/undefined* semantics (enums, constraints, cardinality), and the system consistently chose **proceed** even when some answers should arguably remain uncertain; additionally, a few queries show **lower retrieval quality signals** despite correct grounding.

## Scores

| Dimension | Score (1-5) | Weight | Weighted |
|---|---:|---:|---:|
| Builder Quality | 5 | 25% | 1.25 |
| Retrieval Effectiveness | 4 | 25% | 1.00 |
| Answer Quality | 4 | 30% | 1.20 |
| Pipeline Health | 5 | 10% | 0.50 |
| Ablation Impact | 5 | 10% | 0.50 |
| **Overall** |  |  | **4.45** |

## Dimension Analysis

### 1. Builder Quality (5/5)
- **tables_parsed=5, tables_completed=5, all_tables_completed=true**
- **cypher_failed=false**, **failed_mappings=[]**, **ingestion_errors=[]**
- Triplet density is strong for the small corpus: **triplets_extracted=86** and **entities_resolved=85** suggests solid extraction + entity resolution (no evidence of over/under-extraction).
- Builder time is reported as **elapsed_s=0**, but no functional failures are indicated.

### 2. Retrieval Effectiveness (4/5)
Signals from the bundle:
- **avg_gt_coverage=0.789** (good; not consistently ≥0.8 across the set)
- **avg_top_score=0.783** (healthy; strong reranker confidence overall)
- **No gate abstentions** (**abstained_count=0**), and **gate_decision="proceed"** for all examples (including cases where context was arguably incomplete/ambiguous).
- A few individual questions have notably weaker retrieval signals (even though grounded answers were still correct), e.g.:
  - **ec_007** (covered_sources empty, **gt_coverage=0.0**)
  - **ec_004** (**retrieval_quality_score_raw=0.55**, adjusted 0.7)
  - **ec_005/ec_006/ec_013** show retrieval gating “with warning” behavior via pool_confidence or raw scores.

Given the rubric emphasis on gt coverage and top-score, this earns **4** rather than 5 because **ec_007** shows complete retrieval miss by the provided coverage metric, yet the system still produced an answer.

### 3. Answer Quality (4/5)
- System reports **grounded_count=20 / grounded_rate=1.0**, with **0 factually wrong** items detected by the grader (no grader rejections that indicate hallucination).
- The quality is strong in semantic correctness, including correctly stating inability-to-determine in several “missing_*” / negative-like situations:
  - **ec_004**: “I cannot find this information…” for valid order_status values.
  - **ec_009**: “cannot confirm accepted payment methods.”
  - **ec_012**: correctly notes Failed definition missing.
  - **ec_015**: correctly states invoice timing cannot be determined from context.
- Why not 5: the pipeline never abstains and frequently uses “unclear/needs verification” language instead of abstention even when the rubric’s known limitation (“Negative questions test abstention ability”) would suggest a stricter “abstain_early” behavior for unanswerable items. In this ablation, the model’s answers remain *grounded*, but the gating strategy appears permissive for edgecases.

**Best/worst examples (semantic judgment)**
- **Best**: **ec_004** (CORRECTLY_ABSTAINED-style answer, but marked as proceed). It clearly distinguishes absence of enum values from existing status mentions.
- **Best**: **ec_012** (CORRECT) — explicitly states only that Failed is present and its definition is missing.
- **Worst**: **ec_007** (still grounded per flag, but **gt_coverage=0.0**) — answer is plausible given the glossary cross-references, yet the provided coverage metric suggests retrieval didn’t align to expected sources (“covered_sources empty”). This is likely an artifact of source alignment rather than wrong semantics, but it prevents a 5.

### 4. Pipeline Health (5/5)
- **pipeline_health.total_grader_rejections=3**
- **grader_inconsistencies=0**
- **gate_abstentions=0**
- **cypher_failed=false**, **failed_mappings_count=0**, **ingestion_errors_count=0**
- Grader rejection count of 3 with consistency-valid suggests occasional internal correction needs, but no instability is visible.

### 5. Ablation Impact (5/5)
- Study id is **AB-BEST**, implying best/combined configuration; the bundle shows **high quality across the board** with no tradeoff failures.
- No explicit `ablation_context` is provided, so I can’t verify the exact deltas vs baseline flags. Still, the observed outcomes are consistent with an “optimal” ablation: strong reranker confidence (**avg_top_score≈0.783**) and fully successful builder (**all_tables_completed=true**, **cypher_failed=false**).

## Per-Question Deep Dive

### ec_001: What is a customer?
- **Type:** missing_definition | **Difficulty:** unknown  
- **Verdict:** CORRECT  
- **Expected:** Customer definition incomplete; related: Client interchangeable, Account Holder primary owner, End User actual user  
- **Generated:** Defines Customer as buyer; includes glossary distinctions for Client/Account Holder/End User  
- **Analysis:** Matches glossary semantics and correctly uses “may be used interchangeably” framing.  
- **Retrieval:** gt_coverage=1.0, top_score=0.9836598719063984, gate=proceed

### ec_002: What's the difference between firstName and first_name in the CUSTOMERS table?
- **Type:** duplicate_columns | **Difficulty:** unknown  
- **Verdict:** CORRECT  
- **Expected:** Same VARCHAR(50), duplicates from naming convention inconsistency; usage undocumented  
- **Generated:** States both represent same attribute; only naming/documentation inconsistency  
- **Analysis:** Correctly answers “difference unknown / none documented,” consistent with contexts.  
- **Retrieval:** gt_coverage=1.0, top_score=0.9007046022173545, gate=proceed

### ec_003: Which customer column should be used as a foreign key reference: customer_id or CustomerID?
- **Type:** conflicting_references | **Difficulty:** unknown  
- **Verdict:** CORRECT  
- **Expected:** Ambiguity documented; verify with DBA; customer_id is PK but doesn’t resolve which FK target  
- **Generated:** Concludes no definitive answer from context; prefers customer_id as more directly documented but notes ambiguity  
- **Analysis:** Correctly stays within “unclear/verification needed” without asserting a resolution.  
- **Retrieval:** gt_coverage=1.0, top_score=0.9254997409810218, gate=proceed

### ec_004: What are the valid values for order_status?
- **Type:** missing_constraint | **Difficulty:** unknown  
- **Verdict:** CORRECT  
- **Expected:** Glossary lists statuses (Failed definition missing) but schema/data dictionary doesn’t document allowed values/check constraint  
- **Generated:** “I cannot find this information…”; notes missing authoritative enum set  
- **Analysis:** Correctly distinguishes having *labels* from having *validated allowed values*.  
- **Retrieval:** gt_coverage=1.0, top_score=0.7, gate=proceed

### ec_005: Is there a difference between Product, Item, and SKU?
- **Type:** ambiguous_synonyms | **Difficulty:** unknown  
- **Verdict:** PARTIALLY_CORRECT  
- **Expected:** Product and Item related but distinct not clearly defined; SKU is identifier; boundaries unclear  
- **Generated:** Says Item is synonym; SKU is identifier; Product definition incomplete  
- **Analysis:** Semantics match the glossary direction; however, expected framing emphasizes “exact distinctions not clearly defined,” while answer asserts “essentially same concept” more strongly (still consistent with glossary).  
- **Retrieval:** gt_coverage=1.0, top_score=0.7, gate=proceed

### ec_006: Which table should ORDER_ITEMS.product_id reference: PRODUCTS or INVENTORY?
- **Type:** ambiguous_reference | **Difficulty:** unknown  
- **Verdict:** CORRECT  
- **Expected:** Docs say “PRODUCTS (or INVENTORY?)” and not verified; cannot determine  
- **Generated:** States cannot verify; repeats “not verified” note  
- **Analysis:** Correct abstention-like response but marked proceed.  
- **Retrieval:** gt_coverage=0.5, top_score=0.9608783531246672, gate=proceed

### ec_007: What's the difference between Revenue and Sales?
- **Type:** circular_definition | **Difficulty:** unknown  
- **Verdict:** CORRECT  
- **Expected:** Circular definitions with no clear distinction  
- **Generated:** Reports Revenue is “income from sales” and Sales is “revenue from selling products”; doesn’t claim they’re same/opposites  
- **Analysis:** Semantically correct; however, bundle’s alignment says **covered_sources empty / gt_coverage=0.0**, suggesting evaluation source-mapping mismatch rather than answer wrongness.  
- **Retrieval:** gt_coverage=0.0, top_score=0.7, gate=proceed

### ec_008: Can one order have multiple payments?
- **Type:** conflicting_cardinality | **Difficulty:** unknown  
- **Verdict:** CORRECT  
- **Expected:** PAYMENTS has order_id; glossary says “multiple payment attempts? or one-to-one?” uncertain  
- **Generated:** Says relationship not defined but glossary implies multiple attempts possible  
- **Analysis:** Correctly explains both ambiguity and design implication without definitive claim.  
- **Retrieval:** gt_coverage=0.5, top_score=0.7, gate=proceed

### ec_009: What payment methods are accepted?
- **Type:** missing_enum_values | **Difficulty:** unknown  
- **Verdict:** CORRECT  
- **Expected:** payment_method exists but valid set not documented; no CHECK/enum  
- **Generated:** Cannot confirm accepted methods; mentions only that values are not authoritative  
- **Analysis:** Correctly refuses to enumerate.  
- **Retrieval:** gt_coverage=1.0, top_score=0.7, gate=proceed

### ec_010: What's the correct table name: ORDER_ITEMS or ORDER_DETAILS?
- **Type:** naming_ambiguity | **Difficulty:** unknown  
- **Verdict:** CORRECT  
- **Expected:** Evidence notes ambiguity; actual table in DDL is ORDER_ITEMS; app may reference differently  
- **Generated:** Notes ambiguity persists but indicates evidence uses order_items as actual referenced table  
- **Analysis:** Reasonable within provided snippets; doesn’t overclaim ORDER_DETAILS.  
- **Retrieval:** gt_coverage=1.0, top_score=0.9626731126558706, gate=proceed

### ec_011: Which date column should be used to track when an order was created?
- **Type:** duplicate_columns | **Difficulty:** unknown  
- **Verdict:** CORRECT  
- **Expected:** order_date vs OrderDate vs created_at all exist; no guidance  
- **Generated:** Chooses order_date (DATE, “Date order was created”); acknowledges other columns exist but doesn’t equate them  
- **Analysis:** This is a best-supported choice from context; matches expected “no guidance” by partially selecting the only one explicitly labeled “created.”  
- **Retrieval:** gt_coverage=1.0, top_score=0.9674102552339746, gate=proceed

### ec_012: What does the Failed order status mean?
- **Type:** missing_definition | **Difficulty:** unknown  
- **Verdict:** CORRECT  
- **Expected:** Failed value exists; definition missing; other statuses have definitions  
- **Generated:** States only that definition is missing (“Failed: [definition missing]”)  
- **Analysis:** Correct “cannot determine meaning” answer.  
- **Retrieval:** gt_coverage=1.0, top_score=0.7, gate=proceed

### ec_013: Are there any NOT NULL constraints defined in the schema?
- **Type:** missing_constraints | **Difficulty:** unknown  
- **Verdict:** CORRECT  
- **Expected:** No explicit NOT NULL in DDL; PK implies non-null implicitly; others nullable by default  
- **Generated:** Says NOT NULL not documented; only confirms “assumed, not verified” from PAYMENTS  
- **Analysis:** Correct within provided evidence; doesn’t contradict PK implicit non-null.  
- **Retrieval:** gt_coverage=null (reported null), top_score=0.7627776615116516, gate=proceed

### ec_014: What's the difference between unit_price and current_price in PRODUCTS?
- **Type:** duplicate_columns | **Difficulty:** unknown  
- **Verdict:** CORRECT  
- **Expected:** Both DECIMAL; unit_price is standard selling price; current_price differs but distinction unclear  
- **Generated:** Explains unit_price as standard, current_price as potentially different; no further determination  
- **Analysis:** Correctly mirrors “different from unit_price?” note.  
- **Retrieval:** gt_coverage=1.0, top_score=0.723504868613798, gate=proceed

### ec_015: When is an invoice generated vs payment processed?
- **Type:** missing_workflow | **Difficulty:** unknown  
- **Verdict:** CORRECT  
- **Expected:** Glossary asks “when?”; Invoice defined generically; workflow timing not specified  
- **Generated:** States timing cannot be determined from context; notes receipt occurs after payment but no invoice timing  
- **Analysis:** Good separation; avoids inventing invoice timestamps.  
- **Retrieval:** gt_coverage=1.0, top_score=0.7, gate=proceed

### ec_016: Is the sku column in PRODUCTS unique?
- **Type:** missing_uniqueness | **Difficulty:** unknown  
- **Verdict:** CORRECT  
- **Expected:** sku/product_sku uniqueness “should be UNIQUE?” but not defined; no index documented  
- **Generated:** Says no confirmed uniqueness; reflects uncertainty markers  
- **Analysis:** Correct refusal to assert uniqueness.  
- **Retrieval:** gt_coverage=1.0, top_score=0.7699462646231279, gate=proceed

### ec_017: What is the relationship between customers and orders?
- **Type:** ambiguous_relationship | **Difficulty:** unknown  
- **Verdict:** CORRECT  
- **Expected:** “A customer can place multiple orders. Or is it accounts…?” uncertainty; FK columns ambiguous  
- **Generated:** Reports relationship is unclear; repeats glossary and uncertainty  
- **Analysis:** Matches expected uncertainty characterization.  
- **Retrieval:** gt_coverage=0.5, top_score=0.7, gate=proceed

### ec_018: Which price column represents what the customer actually pays?
- **Type:** semantic_ambiguity | **Difficulty:** unknown  
- **Verdict:** PARTIALLY_CORRECT  
- **Expected:** Multiple price columns; no documentation tying “final customer price” with discounts  
- **Generated:** Suggests payment_amount is closest to what customer pays; notes not explicitly tied to other price fields  
- **Analysis:** Largely aligned, but “closest representation” is an inference; still reasonable and grounded in payment semantics.  
- **Retrieval:** gt_coverage=0.0, top_score=0.7, gate=proceed

### ec_019: What's the difference between Shipment, Delivery, and Fulfillment?
- **Type:** overlapping_concepts | **Difficulty:** unknown  
- **Verdict:** CORRECT  
- **Expected:** Delivery completes shipment; fulfillment encompasses both; boundaries unclear  
- **Generated:** Reproduces glossary definitions and “encompasses” relation  
- **Analysis:** Correct and complete.  
- **Retrieval:** gt_coverage=1.0, top_score=0.7, gate=proceed

### ec_020: Are foreign key constraints enforced in the schema?
- **Type:** missing_fk_enforcement | **Difficulty:** unknown  
- **Verdict:** CORRECT  
- **Expected:** No FK constraints enforced; DDL omits REFERENCES though dictionary documents intended relationships  
- **Generated:** Cannot confirm enforcement from retrieved context; notes ambiguity and missing constraint documentation  
- **Analysis:** Because provided snippets are about documentation/ambiguity rather than DDL enforcement evidence, refusal is appropriate.  
- **Retrieval:** gt_coverage=0.5, top_score=0.7, gate=proceed

## Anomalies & Recommendations

### Red Flags
- **No abstentions at all** despite edgecase-heavy dataset (20/20 answered with `gate_decision="proceed"`). This suggests the retrieval gate/threshold may be too permissive for “missing/unknown” scenarios.
- **Source-alignment metrics sometimes indicate misses** while answers remain grounded:
  - **ec_007 gt_coverage=0.0** and **covered_sources=[]**
  - **ec_018 gt_coverage=0.0**
  This likely points to evaluation bookkeeping/source attribution issues or retrieval mapping quality not captured by gt_coverage.
- Reported **builder_report.elapsed_s=0** and **query_report.elapsed_s=0** are suspicious (instrumentation artifact), though not directly harming correctness.

### Recommendations
- Tighten **retrieval_quality_gate** behavior for edgecases: if contexts explicitly say “definition missing / not documented / unverified,” consider **gate_abstain_early** or a stricter “must cite definition absence” mode.
- Improve **source attribution**: ensure `covered_sources` and `gt_coverage` properly align when glossary definitions are present but expected_sources are different granularity (e.g., expected “PRODUCTS” while glossary lives in business glossary chunks).
- Add a “strictness layer” for questions of the form **“valid values / accepted methods / uniqueness / FK enforcement”**: require explicit constraint evidence; otherwise output should be standardized as “not documented in KG” (already done, but should drive gating).
- Instrument latency properly (non-zero elapsed_s) for performance reporting.

## Comparison Notes (if applicable)
- Baseline comparisons aren’t available (`ablation_context` and AB-00 bundle not provided). However, AB-BEST exhibits the hallmark of a “best” configuration: **all tables completed**, **no Cypher failures**, and **grounded_rate=1.0** across an edgecases dataset.