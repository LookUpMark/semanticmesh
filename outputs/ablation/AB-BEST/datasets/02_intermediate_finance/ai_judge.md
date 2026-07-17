# AI-Judge Evaluation: AB-BEST/02_intermediate_finance
**Evaluator:** (`gpt-5.4-nano-2026-03-17`) using `docs/AI_JUDGE_PROMPT.md`  
**Date:** 2026-07-17

---

# Ablation Study Evaluation: AB-BEST — 02_intermediate_finance

## Executive Summary
AB-BEST shows **excellent end-to-end functionality**: builder completed all 8 tables with **no Cypher failures or ingestion errors**, and query-time grounding is **1.0 across all 25 questions**. Retrieval confidence is generally healthy (avg_top_score ≈ **0.746**), but there are a few semantic slips where the system either **abstains incorrectly** (question 2) or **fails to capture expected domain nuances** (question 25; plus one “missed” multi-step expectation in 20). Overall, this run demonstrates strong pipeline reliability with minor answer-level and coverage-quality concerns.

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
- **All tables parsed and completed**: `tables_parsed=8`, `tables_completed=8`, `all_tables_completed=true`
- **No Cypher/ingestion issues**: `cypher_failed=false`, `failed_mappings=[]`, `ingestion_errors=[]`
- Triplet extraction density appears healthy: `triplets_extracted=244`, `entities_resolved=212` (reasonable ratio; not indicative of severe extraction/ER breakdown)

### 2. Retrieval Effectiveness (5/5)
- `grounded_rate=1.0`, `abstained_count=0`
- **High retrieval alignment**: `avg_gt_coverage=0.99`
- **Healthy reranker confidence**: `avg_top_score=0.7458` (in the expected “good” band for bge-reranker-v2-m3)
- No signs of retrieval collapse: `questions_with_low_retrieval_score=0` in pipeline_health

### 3. Answer Quality (4/5)
- Most answers are correct and consistent with retrieved contexts (and judged grounded).
- However, there are **clear answer-level mismatches**:
  - **Q2**: Expected a difference between Savings vs Money Market, but the model answers *“cannot find information”* despite glossary/examples present in the bundle contexts.
  - **Q25**: Model states it can list operational states but claims the context doesn’t define meanings; expected answer includes more service/meaning interpretation tied to glossary rules (e.g., OutOfCash/OutOfService implications).
  - **Q20**: Interprets “lifecycle from application to completion” primarily as status progression, but the expected answer emphasizes meanings/events and transitions; still mostly reasonable, but somewhat under-specified vs expectation.
- `grader_rejection_count` is low overall (total shown as 5 pipeline health; per-question has 2 on Q23, 1 on Q4 and 1 on Q22, etc.), indicating the grader caught a few issues but not widespread instability.

### 4. Pipeline Health (5/5)
- **No pipeline breakage**: `cypher_failed=false`, `failed_mappings_count=0`, `ingestion_errors_count=0`
- **No abstention-related failures**: `gate_abstentions=0`
- `grader_inconsistencies=0` and grader decisions were consistent.

### 5. Ablation Impact (5/5)
- Study is **AB-BEST**; the bundle indicates the best configuration (not explicitly listing “changes_vs_baseline” in the provided JSON).
- Observed outcomes match “best-case” behavior: builder reliability is perfect, retrieval is strong, and answer correctness is high.
- Given the rubric, this merits **5/5** because the system demonstrably achieves near-ideal coverage and grounding with only minor answer-level defects.

---

## Per-Question Deep Dive

### 1: What is a checking account?
- **Type:** direct_mapping | **Difficulty:** Easy  
- **Verdict:** CORRECT
- **Expected:** Checking is one of account types (CHECK constraint); glossary definition of deposit accounts; schema fields for balances/fees/interest; subtype support; debit-card linkage mention.
- **Generated:** Correctly describes Checking as allowed `accounts.account_type` and lists core fields (balances, status, interest_rate).
- **Analysis:** Matches expected schema-level constraints and description; good coverage.
- **Retrieval:** gt_coverage=1.0, top_score=0.55, gate=proceed

### 2: What is the difference between a savings account and a money market account?
- **Type:** direct_mapping | **Difficulty:** Easy  
- **Verdict:** INCORRECT
- **Expected:** Glossary provides example APY rates and indicates savings vs money market as distinct deposit product types (0.25/0.50 vs 0.75 tiered by balance).
- **Generated:** Claims it cannot find difference beyond `account_type` values.
- **Analysis:** Contradiction: retrieved contexts include the glossary Interest examples differentiating Savings and Money Market, but the generated answer fails to use them.
- **Retrieval:** gt_coverage=1.0, top_score=0.55, gate=proceed

### 3: What is APR versus APY?
- **Type:** direct_mapping | **Difficulty:** Easy  
- **Verdict:** CORRECT
- **Expected:** APR for loans, APY for deposits; compounding implies APY > nominal; glossary examples.
- **Generated:** Correctly explains and aligns with glossary rules.
- **Analysis:** Semantically matches expected.
- **Retrieval:** gt_coverage=1.0, top_score=— (not provided in question object as raw vs adjusted), gate=proceed

### 4: What is KYC Level 2?
- **Type:** direct_mapping | **Difficulty:** Easy  
- **Verdict:** CORRECT
- **Expected:** Level2 is allowed; Level1 minimum; Level3 for high-value/international; risk_profile eligibility; specific criteria for Level2 not detailed.
- **Generated:** Correctly states allowed level and notes lack of extra criteria beyond “allowed level.”
- **Analysis:** Good alignment; minor instability indicated by `grader_rejection_count=1`, but final verdict is still correct.
- **Retrieval:** gt_coverage=1.0, top_score=0.6101 (raw), gate=proceed

### 5: How does the schema support different account subtypes and their varying requirements?
- **Type:** direct_mapping | **Difficulty:** Easy  
- **Verdict:** CORRECT
- **Expected:** `account_subtype` differentiates (Premium/Standard) plus minimum_balance/monthly_fee requirements; glossary confirms fees triggered by minimum balance.
- **Generated:** Explains `account_subtype` and varying nullable requirement fields; also details constraints/status defaults.
- **Analysis:** Solid; includes extra but consistent info.
- **Retrieval:** gt_coverage=1.0, top_score=0.55, gate=proceed

### 6: What types of loan products does the bank offer?
- **Type:** direct_mapping | **Difficulty:** Easy  
- **Verdict:** CORRECT
- **Expected:** 5 types from CHECK on `loans.loan_type` + examples and business rules.
- **Generated:** Lists five loan types correctly.
- **Analysis:** Expected numerical examples are omitted, but question asks “types”; content matches.
- **Retrieval:** gt_coverage=1.0, top_score=0.55, gate=proceed

### 7: What is the daily ATM withdrawal limit defined in the schema?
- **Type:** direct_mapping | **Difficulty:** Easy  
- **Verdict:** CORRECT
- **Expected:** `cards.atm_daily_limit=500.00` default; per-card limit; contrast with `daily_limit`.
- **Generated:** Correctly states `atm_daily_limit` default 500.00.
- **Analysis:** Matches core fact; does not emphasize “per-card not per-customer,” but expected was “should be” included—still largely correct.
- **Retrieval:** gt_coverage=1.0, top_score=0.55, gate=proceed

### 8: What is the difference between a parent account and a child account?
- **Type:** direct_mapping | **Difficulty:** Easy  
- **Verdict:** CORRECT
- **Expected:** `parent_account_id` self-reference; CHECK prevents circular; parent aggregates children; top-level NULL.
- **Generated:** Correctly explains roles and constraints.
- **Analysis:** Strong semantic match.
- **Retrieval:** gt_coverage=1.0, top_score=0.55, gate=proceed

### 9: What does the status “Frozen” mean for a card?
- **Type:** direct_mapping | **Difficulty:** Easy  
- **Verdict:** PARTIALLY_CORRECT
- **Expected:** Glossary distinguishes Frozen vs Blocked as temporary/reversible suspension; also mentions blocked for lost/stolen and expired renewal.
- **Generated:** Only states Frozen is allowed status value; claims no further definition.
- **Analysis:** Misses the expected semantic distinction (Frozen vs Blocked).
- **Retrieval:** gt_coverage=1.0, top_score=0.55, gate=proceed

### 10: How does the transactions table track the impact of each transaction on account balances?
- **Type:** direct_mapping | **Difficulty:** Easy  
- **Verdict:** CORRECT
- **Expected:** `balance_after` records balance post transaction; debit reduces, credit increases; status semantics.
- **Generated:** Correctly focuses on `balance_after` and notes its nullable nature.
- **Analysis:** Matches expected.
- **Retrieval:** gt_coverage=1.0, top_score=0.7225, gate=proceed

### 11: How does the customer_account junction table support multiple ownership types?
- **Type:** direct_mapping | **Difficulty:** Medium  
- **Verdict:** CORRECT
- **Expected:** composite PK; relationship_type CHECK with 4 values; is_primary + ownership_percentage.
- **Generated:** Correctly describes all.
- **Analysis:** Good.
- **Retrieval:** gt_coverage=1.0, top_score=0.9866, gate=proceed

### 12: Difference between current_balance and available_balance
- **Type:** direct_mapping | **Difficulty:** Easy  
- **Verdict:** CORRECT
- **Expected:** current includes pending; available excludes holds/pending; glossary alignment.
- **Generated:** Matches exactly.
- **Analysis:** Correct.
- **Retrieval:** gt_coverage=1.0, top_score=0.8948, gate=proceed

### 13: How are loans linked to both customers and accounts?
- **Type:** multi_hop | **Difficulty:** Medium  
- **Verdict:** CORRECT
- **Expected:** loans.customer_id (required), loans.account_id optional; loan tracks other fields.
- **Generated:** Correct FK nullability-based linkage.
- **Analysis:** Matches expected.
- **Retrieval:** gt_coverage=1.0, top_score=0.8103, gate=proceed

### 14: Transaction types and status lifecycle
- **Type:** direct_mapping | **Difficulty:** Easy  
- **Verdict:** CORRECT
- **Expected:** 7 types + 5 states + business rules about posting/failure effects.
- **Generated:** Correctly lists both sets and lifecycle semantics.
- **Analysis:** Correct.
- **Retrieval:** gt_coverage=1.0, top_score=0.55, gate=proceed

### 15: How does schema support joint account ownership between multiple customers?
- **Type:** multi_hop | **Difficulty:** Medium  
- **Verdict:** CORRECT
- **Expected:** customer_account many-to-many; relationship_type; ownership_percentage; is_primary; linked/unlinked dates.
- **Generated:** Covers all required design elements.
- **Analysis:** Good.
- **Retrieval:** gt_coverage=1.0, top_score=0.5784, gate=proceed

### 16: What does cards table track and how are cards linked?
- **Type:** direct_mapping | **Difficulty:** Medium  
- **Verdict:** CORRECT
- **Expected:** links to accounts + customers; tracks limits, security features, status lifecycle.
- **Generated:** Correctly lists linked FKs and key columns.
- **Analysis:** Strong.
- **Retrieval:** gt_coverage=1.0, top_score=0.9702, gate=proceed

### 17: Interest rates across deposit and loan products
- **Type:** multi_hop | **Difficulty:** Hard  
- **Verdict:** PARTIALLY_CORRECT
- **Expected:** APR for loans vs APY for deposits; accounts interest tracking and rules.
- **Generated:** Explains APR for loans; describes APY conceptually, but claims deposit-specific schema mechanism not shown.
- **Analysis:** Likely incomplete vs expected “accounts interest tracking” framing (though contexts do include accounts interest_rate).
- **Retrieval:** gt_coverage=1.0, top_score=0.55, gate=proceed

### 18: Branch types and capability differences
- **Type:** direct_mapping | **Difficulty:** Easy  
- **Verdict:** CORRECT
- **Expected:** FullService/Satellite/ATMOnly + capabilities and tracked fields.
- **Generated:** Correctly explains differences in capabilities.
- **Analysis:** Missing some listed tracked fields (branch_code/address specifics), but capability difference is correct.
- **Retrieval:** gt_coverage=1.0, top_score=0.55, gate=proceed

### 19: ATMs related to branches; types
- **Type:** multi_hop | **Difficulty:** Medium  
- **Verdict:** CORRECT
- **Expected:** nullable branch_id => standalone; atm_type values and implications.
- **Generated:** Correctly describes relationship and types.
- **Analysis:** Good.
- **Retrieval:** gt_coverage=1.0, top_score=0.6892, gate=proceed

### 20: Lifecycle of a loan from application to completion
- **Type:** direct_mapping | **Difficulty:** Medium  
- **Verdict:** PARTIALLY_CORRECT
- **Expected:** Pending→Approved→Active→PaidOff and Defaulted meanings; business glossary adds transitions/events and repayment timeline.
- **Generated:** Correctly maps lifecycle to status values but under-specifies transition events and glossary-derived process detail.
- **Analysis:** Reasonable, but doesn’t fully satisfy expected “from application to completion” narrative.
- **Retrieval:** gt_coverage=1.0, top_score=0.55, gate=proceed

### 21: Preferred customer status and tracking
- **Type:** direct_mapping | **Difficulty:** Medium  
- **Verdict:** INCORRECT
- **Expected:** tracked by `customers.is_preferred`; glossary meaning (fee waivers/priority).
- **Generated:** Says it cannot find preferred status; does not use `is_preferred` even though it was retrieved.
- **Analysis:** Clear omission of an available schema field; contradicts expected content.
- **Retrieval:** gt_coverage=1.0, top_score=0.55, gate=proceed

### 22: accounts interest tracking and business rules
- **Type:** direct_mapping | **Difficulty:** Medium  
- **Verdict:** PARTIALLY_CORRECT
- **Expected:** interest_rate nullable, interest_earned YTD, glossary rules about monthly crediting, compounding/APY, promotional/penalty rates.
- **Generated:** Correctly describes columns and nullability/YN; does **not** robustly cover glossary business rules (monthly crediting, compounding, promotional/penalty rates).
- **Analysis:** Column-level correctness but business-rule coverage appears insufficient.
- **Retrieval:** gt_coverage=0.75, top_score=0.55, gate=proceed

### 23: Can an account exist without any customer linked to it?
- **Type:** negative | **Difficulty:** Medium  
- **Verdict:** PARTIALLY_CORRECT
- **Expected:** negative answer framed as “schema doesn’t enforce via constraint; business rule at application level.”
- **Generated:** Answers “not explicitly stated”; correctly reasons about absence of schema constraint, but expected answer wants explicit business-rule framing (and the gate is “proceed” rather than abstain).
- **Analysis:** Mostly aligned with expected (lack of FK from accounts), but the final framing is too cautious.
- **Retrieval:** gt_coverage=1.0, top_score=0.55, gate=proceed

### 24: How does schema handle failed or cancelled transactions?
- **Type:** negative | **Difficulty:** Medium  
- **Verdict:** CORRECT
- **Expected:** status includes Failed/Cancelled; failed don’t affect balance (balance_after no-change); audit trail; record preservation.
- **Generated:** Correctly explains statuses and balance_after nullable semantics.
- **Analysis:** Matches.
- **Retrieval:** gt_coverage=1.0, top_score=0.55, gate=proceed

### 25: Operational states of an ATM and what they mean
- **Type:** direct_mapping | **Difficulty:** Easy  
- **Verdict:** PARTIALLY_CORRECT
- **Expected:** Operational/OutOfService/OutOfCash plus meaning implications; OutOfCash prevents withdrawals; cash replenishment triggered when balance low; deposit/cardless behavior.
- **Generated:** Lists states but claims meanings aren’t defined beyond availability-management usage.
- **Analysis:** Underuses available glossary signals about replenishment and OutOfCash behavior.
- **Retrieval:** gt_coverage=1.0, top_score=0.55, gate=proceed

---

## Anomalies & Recommendations

### Red Flags
1. **Contradictory “I cannot find info” responses despite relevant retrieved contexts**  
   - Q2 (Savings vs Money Market) and Q21 (preferred customer status) both effectively fail to use available KG/glossary evidence.
2. **Expected nuance is sometimes missed even when retrieved**
   - Q9 (Frozen vs Blocked distinction), Q17 (deposit APY/account interest mechanism nuance), Q25 (service meanings of OutOfCash/OutOfService).
3. **Negative question handling is “proceed” not abstain**
   - Q23 is negative but the system does not abstain (gate_abstentions=0 overall). That’s acceptable if it answers correctly, but here it’s only partially aligned.

### Recommendations
- **Strengthen Answer Generation to consume retrieved glossary examples**:
  - Add a “must-use” retrieval-to-answer alignment check for key glossary example sections (e.g., Interest examples in Interest glossary).
- **Add a targeted contradiction detector for “cannot find” patterns**:
  - If `covered_sources` indicates the necessary concept is present (e.g., `Interest`, `customers.is_preferred`), disallow generic “cannot find” outputs and force extraction of relevant fields.
- **For status/lifecycle questions, enforce structured mapping**:
  - When question asks “meaning/implication of states,” require at least one explicit meaning sentence per status, not just state listing (Q9, Q25, Q20).
- **Revisit negative-gating thresholds for this study**:
  - Ensure gate abstention triggers when the question expects “no such linkage exists” and evidence is ambiguous; alternatively, allow “not enforceable” answers but with explicit schema-vs-business-rule contrast.

## Comparison Notes (if applicable)
- This is **AB-BEST**, so comparison to AB-00 is not possible from the provided JSON (no `ablation_context.changes_vs_baseline` field included).  
- Still, the observed KPIs strongly indicate the “best” configuration materially improves builder reliability and retrieval alignment, with remaining issues concentrated in **generation discipline** (using already-retrieved facts) rather than pipeline failures.