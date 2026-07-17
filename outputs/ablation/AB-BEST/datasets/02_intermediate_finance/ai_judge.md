# AI-Judge Evaluation: AB-BEST/02_intermediate_finance
**Evaluator:** (`gpt-5.4-nano-2026-03-17`) using `docs/AI_JUDGE_PROMPT.md`  
**Date:** 2026-07-17

---

# Ablation Study Evaluation: AB-BEST — 02_intermediate_finance

## Executive Summary
This run shows a **highly successful end-to-end pipeline**: the Builder completed **100% of tables** with **no Cypher failures or ingestion errors**, and the Query Graph answered **all 25/25 questions as grounded** with very high average retrieval/coverage (avg_gt_coverage **0.99**, avg_top_score **0.746**).  
The main concerns are **a few answer-level knowledge gaps/over-claims** in specific questions (notably one “negative” reasoning case and a couple of hard/multi-hop explanatory questions), despite strong grounding signals.

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
- `tables_parsed=8`, `tables_completed=8`, `all_tables_completed=true`
- `cypher_failed=false`
- `failed_mappings=[]`, `ingestion_errors=[]`
- Triplet extraction density appears healthy: `triplets_extracted=244` across `8` tables (strong enough signal that KG edge potential is good).
**Verdict:** Builder graph is functioning correctly with no observable structural failures.

### 2. Retrieval Effectiveness (4/5)
- `grounded_rate=1.0` for the whole set and `avg_gt_coverage=0.99` → ground-truth sources are almost always retrieved.
- `avg_top_score=0.7458` → strong reranker confidence overall.
- Minor concern: per-question retrieval-quality scores show some variability (e.g., a few entries at `retrieval_quality_score_raw≈0.55`), but none trigger the reported `pipeline_health.questions_with_low_retrieval_score=0`.
**Verdict:** Retrieval is excellent overall; score slightly below 5 because a few hard questions indicate that “retrieved context” was sometimes insufficient or not used to its full explanatory potential.

### 3. Answer Quality (4/5)
- `grounded_count=25` and `grounded_rate=1.0` suggest the grader considered all generated answers verifiable against retrieved contexts.
- However, expert semantic review finds **a few cases where the answer does not fully satisfy the expected *explanatory* requirement** (not just missing synonyms/wording), plus at least **one negative-question mismatch in reasoning**:
  - **Q2**: expected a difference between savings vs money market; generated answer abstains (“cannot find”) despite glossary/examples in the expected context. This is a major *task-fit* miss.
  - **Q21 (preferred status)**: generated answer says it cannot find preferred meaning, while expected includes glossary meaning and `customers.is_preferred`.
  - **Q23 (negative)**: expected “can’t exist without customer” is framed as business rule/application-level; generated answer argues more carefully about schema not forcing it. This is semantically plausible, but it contradicts the expected verdict framing and likely fails the dataset’s intended notion of the negative target.
  - **Q17 (interest rates across deposit & loan)**: generated answer says deposit interest storage isn’t shown; expected says accounts track interest via `interest_rate` and glossary clarifies APY/compounding. This is an under-specification relative to expected.
**Verdict:** Mostly correct and well-grounded, but **several notable misses reduce the score from 5** to 4.

### 4. Pipeline Health (5/5)
- `cypher_failed=false`, `failed_mappings_count=0`, `ingestion_errors_count=0`
- `grader_inconsistencies=0`
- `gate_abstentions=0`
- `pipeline_health.total_grader_rejections=5`, but per-question `grader_consistency_valid=true` and there are **no indications of unstable recovery** (no forced final “pass” after max retries is reported).
**Verdict:** Stable and healthy.

### 5. Ablation Impact (5/5)
- `study_id=AB-BEST` implies a combined/best configuration. In this bundle, there are **no ablation-induced flags indicating disabling** of core quality components (reranker enabled, hybrid retrieval, no evidence of turning off critic/grade loops).
- Observed behavior aligns with “best” expectations: near-perfect groundedness and high coverage.
**Verdict:** Outcomes match the “best” hypothesis.

---

## Per-Question Deep Dive

### 1: What is a checking account?
- **Type:** direct_mapping | **Difficulty:** Easy
- **Verdict:** CORRECT
- **Expected:** Checking is one of account types; defined by accounts CHECK constraint; glossary on account/management; includes balances/fees/interest_rate nullable; optional subtype; cards linked rule
- **Generated:** Matches accounts.account_type constraint and relevant columns; no extra wrong claims
- **Analysis:** Correct schema-based definition; properly contextualizes subtype and balances.
- **Retrieval:** gt_coverage=1.0, top_score=0.55, gate=proceed

### 2: What is the difference between a savings account and a money market account?
- **Type:** direct_mapping | **Difficulty:** Easy
- **Verdict:** INCORRECT
- **Expected:** Both are deposit product types in accounts.account_type; glossary examples: Savings APY examples (0.25/0.50) vs Money Market 0.75% tiered by balance; both share interest_rate/minimum_balance/monthly_fee
- **Generated:** Says cannot find differences; only notes they are different account_type values
- **Analysis:** Fails the key comparative part; despite contexts including account_type and interest glossary, it did not retrieve/synthesize the provided examples.
- **Retrieval:** gt_coverage=1.0, top_score=0.55, gate=proceed

### 3: What is APR versus APY?
- **Type:** direct_mapping | **Difficulty:** Easy
- **Verdict:** CORRECT
- **Expected:** APR for loans; APY for deposits; APY incorporates compounding and is higher when compounding > annually; examples
- **Generated:** Correct APR/APY roles and compounding implication; aligned with glossary rules
- **Analysis:** Strong semantic match.
- **Retrieval:** gt_coverage=1.0, top_score=0.96, gate=proceed

### 4: What is KYC Level 2?
- **Type:** direct_mapping | **Difficulty:** Easy
- **Verdict:** PARTIALLY_CORRECT
- **Expected:** Level1 minimum; Level3 for high-value/international; Level2 sits between, but specific criteria not detailed
- **Generated:** Correct about allowed level and that criteria beyond being an allowed level aren’t specified
- **Analysis:** Semantically aligns with expected; minor wording gaps only.  
- **Retrieval:** gt_coverage=1.0, top_score=0.61, gate=proceed

### 5: How does the schema support different account subtypes and their varying requirements?
- **Type:** direct_mapping | **Difficulty:** Easy
- **Verdict:** CORRECT
- **Expected:** account_subtype differentiates within account_type; linked to min balance & monthly_fee; interest_rate nullable for non-interest accounts
- **Generated:** Correctly describes account_subtype, interest_rate nullability, and related constraints/defaults
- **Analysis:** Correct and sufficiently complete.
- **Retrieval:** gt_coverage=1.0, top_score=0.55, gate=proceed

### 6: What types of loan products does the bank offer?
- **Type:** direct_mapping | **Difficulty:** Easy
- **Verdict:** CORRECT
- **Expected:** Mortgage, Personal, Auto, HELOC, CreditCard; loan_type CHECK and glossary examples/notes
- **Generated:** Lists all five types correctly
- **Analysis:** Complete for this question’s expected core list.
- **Retrieval:** gt_coverage=1.0, top_score=0.55, gate=proceed

### 7: What is the daily ATM withdrawal limit defined in the schema?
- **Type:** direct_mapping | **Difficulty:** Easy
- **Verdict:** CORRECT
- **Expected:** cards.atm_daily_limit default 500.00 per card; distinguish from daily_limit
- **Generated:** Correctly identifies atm_daily_limit and default value
- **Analysis:** Meets expected requirement.
- **Retrieval:** gt_coverage=1.0, top_score=0.55, gate=proceed

### 8: What is the difference between a parent account and a child account?
- **Type:** direct_mapping | **Difficulty:** Easy
- **Verdict:** CORRECT
- **Expected:** parent_account_id self-ref; prevents circularity; parent contains children for portfolio aggregation; top-level has NULL
- **Generated:** Correct hierarchy definition; mentions circularity check; no behavioral claims beyond hierarchy
- **Analysis:** Strong match.
- **Retrieval:** gt_coverage=1.0, top_score=0.55, gate=proceed

### 9: What does the status “Frozen” mean for a card?
- **Type:** direct_mapping | **Difficulty:** Easy
- **Verdict:** PARTIALLY_CORRECT
- **Expected:** glossary distinguishes statuses; Frozen vs Blocked implies temporary suspension vs immediate block; business meaning
- **Generated:** Only states Frozen is a valid allowed status; says no further business definition in context
- **Analysis:** Under-explains “meaning” relative to expected distinction.  
- **Retrieval:** gt_coverage=1.0, top_score=0.55, gate=proceed

### 10: How does the transactions table track the impact of each transaction on account balances?
- **Type:** direct_mapping | **Difficulty:** Easy
- **Verdict:** PARTIALLY_CORRECT
- **Expected:** balance_after tracks impact; plus debit reduces/credit increases; posted vs failed behavior
- **Generated:** Correctly highlights balance_after primarily; does not emphasize debit/credit sign/semantics and failure impact
- **Analysis:** Mostly right but misses part of expected explanatory mapping.
- **Retrieval:** gt_coverage=1.0, top_score=0.72, gate=proceed

### 11: How does the customer_account junction table support multiple ownership types?
- **Type:** direct_mapping | **Difficulty:** Medium
- **Verdict:** CORRECT
- **Expected:** relationship_type values; composite PK; is_primary and ownership_percentage
- **Generated:** Correctly describes relationship_type, composite PK, and ownership metadata
- **Analysis:** Complete.
- **Retrieval:** gt_coverage=1.0, top_score=0.99, gate=proceed

### 12: Difference between current_balance and available_balance
- **Type:** direct_mapping | **Difficulty:** Easy
- **Verdict:** CORRECT
- **Expected:** current includes pending; available excludes holds/pending; glossary confirms
- **Generated:** Matches both definitions and glossary rule
- **Analysis:** Correct.
- **Retrieval:** gt_coverage=1.0, top_score=0.89, gate=proceed

### 13: How are loans linked to both customers and accounts in the schema?
- **Type:** multi_hop | **Difficulty:** Medium
- **Verdict:** CORRECT
- **Expected:** loans.customer_id FK to customers (required); loans.account_id optional FK to accounts
- **Generated:** Matches required/non-required foreign keys and optionality
- **Analysis:** Correct multi-hop.
- **Retrieval:** gt_coverage=1.0, top_score=0.81, gate=proceed

### 14: Transaction types and status lifecycle
- **Type:** direct_mapping | **Difficulty:** Easy
- **Verdict:** CORRECT
- **Expected:** 7 types; 5 status states; glossary behavior for posted/failed
- **Generated:** Correctly enumerates both sets and lifecycle behavior
- **Analysis:** Matches expected.
- **Retrieval:** gt_coverage=1.0, top_score=0.55, gate=proceed

### 15: Joint account ownership between multiple customers
- **Type:** multi_hop | **Difficulty:** Medium
- **Verdict:** CORRECT
- **Expected:** customer_account many-to-many; relationship_type includes JointOwner; ownership_percentage and is_primary
- **Generated:** Correctly describes role types and key ownership fields
- **Analysis:** Complete.
- **Retrieval:** gt_coverage=1.0, top_score=0.58, gate=proceed

### 16: What information does cards track and how are cards linked?
- **Type:** direct_mapping | **Difficulty:** Medium
- **Verdict:** CORRECT
- **Expected:** FK links to account_id and customer_id; core card attributes, limits, security features, status lifecycle
- **Generated:** Correct and detailed; aligns with schema constraints and column semantics
- **Analysis:** Complete.
- **Retrieval:** gt_coverage=1.0, top_score=0.97, gate=proceed

### 17: How does the schema handle interest rates across deposit and loan products?
- **Type:** multi_hop | **Difficulty:** Hard
- **Verdict:** PARTIALLY_CORRECT
- **Expected:** accounts has interest_rate + interest_earned; loans has interest_rate (APR); glossary maps APR to loans, APY to deposits and crediting/compounding rules
- **Generated:** Correctly covers loans APR storage, but claims deposit interest storage is not directly shown (only conceptual mapping)
- **Analysis:** Understates deposit-side storage because accounts.interest_rate is present; misses that portion of expected answer.
- **Retrieval:** gt_coverage=1.0, top_score=0.55, gate=proceed

### 18: Branch types and capabilities
- **Type:** direct_mapping | **Difficulty:** Easy
- **Verdict:** CORRECT
- **Expected:** FullService/Satellite/ATMOnly with capability differences per glossary and branch attributes
- **Generated:** Correctly explains capability differences aligned with glossary
- **Analysis:** Complete enough.
- **Retrieval:** gt_coverage=1.0, top_score=0.55, gate=proceed

### 19: ATM relation to branches and types of ATMs
- **Type:** multi_hop | **Difficulty:** Medium
- **Verdict:** CORRECT
- **Expected:** atms.branch_id nullable (standalone); atm_type supports Standalone/Branch/DriveThrough; operational status meaning
- **Generated:** Correct on branch_id nullable and atm_type set; matches glossary definitions
- **Analysis:** Correct multi-hop.
- **Retrieval:** gt_coverage=1.0, top_score=0.69, gate=proceed

### 20: Lifecycle of a loan from application to completion
- **Type:** direct_mapping | **Difficulty:** Medium
- **Verdict:** PARTIALLY_CORRECT
- **Expected:** status lifecycle (Pending/Approved/Active/PaidOff/Defaulted) plus description of what maps to application→completion; glossary notes about transitions/events
- **Generated:** Correctly maps lifecycle to status progression but explicitly says transitions/events aren’t specified
- **Analysis:** Meets status listing but misses the “application→completion” narrative the expected answer wants.
- **Retrieval:** gt_coverage=1.0, top_score=0.55, gate=proceed

### 21: Preferred customer status and how tracked
- **Type:** direct_mapping | **Difficulty:** Medium
- **Verdict:** INCORRECT
- **Expected:** customers.is_preferred flag (default false) and glossary meaning (waived fees/priority); plus relation to risk/kyc eligibility
- **Generated:** Says it cannot find preferred meaning/tracking; claims glossary/schema do not define it
- **Analysis:** Contradicts schema context: `customers.is_preferred` is explicitly referenced in sources_retrieved.
- **Retrieval:** gt_coverage=1.0, top_score=0.55, gate=proceed

### 22: accounts interest tracking and governing business rules
- **Type:** direct_mapping | **Difficulty:** Medium
- **Verdict:** PARTIALLY_CORRECT
- **Expected:** accounts.interest_rate (nullable) + interest_earned (YTD) and glossary about monthly crediting/APY/compounding, promo/penalty rules
- **Generated:** Correctly describes interest_rate nullability and interest_earned; does not properly incorporate glossary promo/penalty and APY/compounding governing rules into the accounts table explanation (instead frames more generally)
- **Analysis:** Some expected content omitted.
- **Retrieval:** gt_coverage=0.75, top_score=0.55, gate=proceed

### 23: Can an account exist without any customer linked to it? (negative)
- **Type:** negative | **Difficulty:** Medium
- **Verdict:** PARTIALLY_CORRECT
- **Expected:** No schema constraint forces at least one customer; business glossary says accounts cannot exist without customer ownership but it’s application-level; thus “yes, it could exist” at DB level, but the dataset expects careful “negative” handling
- **Generated:** Says context does not explicitly state accounts must have customer_account rows; argues junction constraints don’t guarantee at least one link
- **Analysis:** Reasoning is aligned with expected DB-level interpretation, but it may conflict with the dataset’s intended framing of the negative condition (the expected answer explicitly mixes “no schema-level constraint” with “business rule enforced”). This looks like an answer that is *technically correct* but not *semantically aligned with the dataset target wording*.
- **Retrieval:** gt_coverage=1.0, top_score=0.55, gate=proceed

### 24: How does the schema handle failed or cancelled transactions?
- **Type:** negative | **Difficulty:** Medium
- **Verdict:** CORRECT
- **Expected:** status includes Failed/Cancelled; glossary: failed doesn’t affect balance; posted final; audit trail preserved
- **Generated:** Correctly describes transaction.status constraints and balance_after nullability logic
- **Analysis:** Matches expected semantics.
- **Retrieval:** gt_coverage=1.0, top_score=0.55, gate=proceed

### 25: ATM operational states and what they mean
- **Type:** direct_mapping | **Difficulty:** Easy
- **Verdict:** PARTIALLY_CORRECT
- **Expected:** Operational/OutOfService/OutOfCash meanings including deposit behavior and constraints from glossary
- **Generated:** Correctly lists allowed states but says context doesn’t define meaning beyond being part of status set
- **Analysis:** Misses expected “what it means” nuance.
- **Retrieval:** gt_coverage=1.0, top_score=0.55, gate=proceed

---

## Anomalies & Recommendations

### Red Flags
- **Task-fit failures despite high grounding**:  
  - Q2 (savings vs money market) and Q21 (preferred status) both return “cannot find” style answers even though retrieved sources include the relevant glossary/schema fields.
- **Under-explained “meaning” questions**: Q9 (Frozen meaning), Q25 (ATM state meanings) and parts of Q10/Q20 show correct enumerations but missing glossary-level operational semantics.
- **Hard reasoning omission**: Q17 fails to incorporate that deposit interest storage exists in `accounts.interest_rate` despite high coverage.

### Recommendations
1. **Add a “use retrieved examples/rules” synthesis constraint** for questions asking *differences* or *business-rule meaning* (comparative/interpretive question templates).
2. **Improve query-to-context selection inside generation**:
   - When `sources_retrieved` includes a decisive glossary section (e.g., Interest examples or “VIP/preferred” glossary text), forbid generic abstention (“cannot find”) unless retrieval contexts truly lack that material.
3. **Tighten negative-question target alignment**:
   - For negative queries, align generation to the dataset’s expected framing (DB constraint vs business rule) and require explicit statement in the expected polarity.
4. **For “state meaning” questions**, add a post-retrieval check: if the glossary defines semantics for each status, require them to be present in the final answer (otherwise flag for regeneration).

## Comparison Notes (if applicable)
- Since this is **AB-BEST**, no baseline (AB-00) bundle was provided for direct numeric comparison. Nonetheless, the observed metrics (builder success, grounded_rate=1.0, avg_gt_coverage=0.99, avg_top_score≈0.746, no pipeline errors) strongly indicate an overall best-case configuration in this study.

