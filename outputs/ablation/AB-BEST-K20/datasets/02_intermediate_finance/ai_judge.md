# AI-Judge Evaluation: AB-BEST-K20/02_intermediate_finance
**Evaluator:** (`gpt-5.4-nano-2026-03-17`) using `docs/AI_JUDGE_PROMPT.md`  
**Date:** 2026-07-17

---

# Ablation Study Evaluation: AB-BEST-K20 — 02_intermediate_finance

## Executive Summary
This run shows **excellent end-to-end pipeline performance**: the Builder successfully completed all 8 parsed tables with **no Cypher failures**, and the Query Graph achieved **grounded_rate=1.0** with **avg_gt_coverage=1.0** across all 25 questions. Retrieval confidence is generally healthy (avg_top_score ≈ **0.749**) and the system correctly handles both positive and negative/abstention-style queries (no abstentions; negatives answered by “not enough information” rather than fabricating). The main concern is **a few grader-rejection events (3 total)** despite high grounding—suggesting the grader may be enforcing stricter “completeness to expected” semantics on some items rather than hallucination.

## Scores

| Dimension | Score (1-5) | Weight | Weighted |
|---|---:|---:|---:|
| Builder Quality | 5 | 25% | 1.25 |
| Retrieval Effectiveness | 5 | 25% | 1.25 |
| Answer Quality | 4 | 30% | 1.20 |
| Pipeline Health | 4 | 10% | 0.40 |
| Ablation Impact | 5 | 10% | 0.50 |
| **Overall** |  |  | **4.60** |

## Dimension Analysis

### 1. Builder Quality (5/5)
- `tables_parsed=8`, `tables_completed=8`, `all_tables_completed=true`
- `cypher_failed=false`, `failed_mappings=[]`
- `ingestion_errors=[]`
- Triplet extraction is substantial (`triplets_extracted=240`, `entities_resolved=207`), consistent with a functioning extraction + ER + mapping pipeline.
**Conclusion:** No builder-side failures; graph construction is reliable.

### 2. Retrieval Effectiveness (5/5)
- `grounded_rate=1.0` and `avg_gt_coverage=1.0`
- `avg_top_score=0.7492` (consistent with a strong reranking stage for bge-reranker-v2-m3)
- No gate abstentions: `abstained_count=0`, `gate_abstention=0`
- No questions with low retrieval score: `questions_with_low_retrieval_score=0`
**Conclusion:** Ground-truth sources are consistently retrieved with strong reranker confidence.

### 3. Answer Quality (4/5)
- `grounded_rate=1.0` across all questions indicates **no verifiable hallucinations** relative to retrieved KG context.
- However, there are **grader rejections**:
  - `pipeline_health.total_grader_rejections=3`
  - Several per-question entries show `grader_rejection_count=1` (notably query_id **11** and **23**) while most others are 0.
- These rejections appear to be about **strict semantic alignment / completeness vs expected answer**, not about grounding correctness (since grounded is always true).

**Worst-case signal (examples):**
- **Query 23 (negative)**: expected “account cannot exist without any customer linked” (or business-rule enforced), while generated answer concludes it’s **not determinable from DDL** (“knowledge graph does not contain enough information”). That is reasonable given the provided KG, but may conflict with the expected answer’s assumption about business-rule enforcement.
- **Query 11**: expected answer is about how multiple ownership types are supported; generated answer correctly describes storing a single `relationship_type` per `(customer_id, account_id)` row, but may diverge from the expected framing (possibly treated as incomplete by the grader).

**Conclusion:** Answers are grounded and largely correct; small semantic mismatches caused grader rejections.

### 4. Pipeline Health (4/5)
- `cypher_failed=false`, `failed_mappings_count=0`, `ingestion_errors_count=0`
- `grader_inconsistencies=0`
- Some rejections occurred (**3 total**), but they did not trigger instability (no evidence of “forced pass after max retries” patterns; also no signs of generation collapse).
**Conclusion:** Stable pipeline with minor grader disagreement/completeness issues.

### 5. Ablation Impact (5/5)
- Study is labeled **AB-BEST-K20**, and the run appears to be the “best/combined-optimal” configuration; however, the bundle does **not include** an `ablation_context` section describing what changed vs baseline (and `ragas` is null).
- Given the very strong objective results (builder completion, retrieval, grounding) and no failures, this ablation plausibly represents an intended “best” setting.
**Conclusion:** Observed behavior matches “best” expectations strongly.

## Per-Question Deep Dive

### 1: What is a checking account?
- **Type:** direct_mapping | **Difficulty:** Easy  
- **Verdict:** CORRECT  
- **Expected:** Checking is one of account types defined by accounts CHECK constraint; glossary definition of Account; tracks balances/fees/interest_rate nullable; subtype via account_subtype; related card rules.  
- **Generated:** Uses `accounts.account_type` and glossary definition; includes balances/status fields and mentions subtypes.  
- **Analysis:** Matches expected concept definition and schema constraints; grounded in retrieved `accounts` + glossary.  
- **Retrieval:** gt_coverage=1.0, top_score=0.7, gate=proceed

### 2: What is the difference between a savings account and a money market account?
- **Type:** direct_mapping | **Difficulty:** Easy  
- **Verdict:** PARTIALLY_CORRECT  
- **Expected:** Savings vs Money Market differ via glossary examples/rates; both are account types with interest_rate/minimum_balance/monthly_fee.  
- **Generated:** States context lacks explicit “difference” beyond both being account types; still cites example interest/APY behavior.  
- **Analysis:** Correctly identifies missing explicit behavioral rules, but expected answer assumes a clearer differentiation; grader likely considered it partial.  
- **Retrieval:** gt_coverage=1.0, top_score=0.7, gate=proceed

### 3: What is APR versus APY?
- **Type:** direct_mapping | **Difficulty:** Easy  
- **Verdict:** CORRECT  
- **Expected:** APR for loans, APY for deposits; APY reflects compounding and can be higher; examples provided.  
- **Generated:** Correct conceptual definitions and compounding distinction.  
- **Analysis:** Consistent with `Interest` glossary context.  
- **Retrieval:** gt_coverage=1.0, top_score=0.9607, gate=proceed

### 4: What is KYC Level 2?
- **Type:** direct_mapping | **Difficulty:** Easy  
- **Verdict:** CORRECT  
- **Expected:** Level1/2/3 constrained; glossary explains purpose/tiers; specific requirements not detailed beyond relative placement.  
- **Generated:** Defines as valid level; references constraint and default; mentions Level3 high-value.  
- **Analysis:** Matches expected “Level2 exists; specific docs not detailed” framing.  
- **Retrieval:** gt_coverage=1.0, top_score=0.7, gate=proceed

### 5: How does the schema support different account subtypes and their varying requirements?
- **Type:** direct_mapping | **Difficulty:** Easy  
- **Verdict:** CORRECT  
- **Expected:** `account_subtype` differentiates within account types; min_balance + monthly_fee govern requirements; glossary mentions fee triggers.  
- **Generated:** Describes subtype column and nullable fee/interest-related fields; discusses min_balance and monthly_fee defaults.  
- **Analysis:** Correctly grounded; slight emphasis on other fields but aligned with expected schema mechanisms.  
- **Retrieval:** gt_coverage=1.0, top_score=0.7, gate=proceed

### 6: What types of loan products does the bank offer?
- **Type:** direct_mapping | **Difficulty:** Easy  
- **Verdict:** CORRECT  
- **Expected:** Five loan types via CHECK on `loans.loan_type`; glossary notes collateral/rates/default behavior.  
- **Generated:** Lists the five types from `Loan`/`loans.loan_type`.  
- **Analysis:** Expected detail on rates/collateral not fully elaborated, but the core required facts are present and grounded.  
- **Retrieval:** gt_coverage=1.0, top_score=0.7, gate=proceed

### 7: What is the daily ATM withdrawal limit defined in the schema?
- **Type:** direct_mapping | **Difficulty:** Easy  
- **Verdict:** CORRECT  
- **Expected:** `cards.atm_daily_limit` default 500.00; per-card not per-customer.  
- **Generated:** States `cards.atm_daily_limit` default 500.00.  
- **Analysis:** Correct.  
- **Retrieval:** gt_coverage=1.0, top_score=0.7, gate=proceed

### 8: What is the difference between a parent account and a child account?
- **Type:** direct_mapping | **Difficulty:** Easy  
- **Verdict:** CORRECT  
- **Expected:** `parent_account_id` self-FK; CHECK prevents cycles; parent vs child via NULL vs reference.  
- **Generated:** Explains NULL top-level vs referenced parent; includes cycle prevention.  
- **Analysis:** Correct and grounded.  
- **Retrieval:** gt_coverage=1.0, top_score=0.7, gate=proceed

### 9: What does the status 'Frozen' mean for a card?
- **Type:** direct_mapping | **Difficulty:** Easy  
- **Verdict:** PARTIALLY_CORRECT  
- **Expected:** Frozen vs Blocked distinction implied by glossary; expected to provide meaning.  
- **Generated:** Says meaning of Frozen not defined beyond being a status value.  
- **Analysis:** Grounded but arguably under-answers expected semantics (“Frozen is temporary/reversible”).  
- **Retrieval:** gt_coverage=1.0, top_score=0.7, gate=proceed

### 10: How does the transactions table track the impact of each transaction on account balances?
- **Type:** direct_mapping | **Difficulty:** Easy  
- **Verdict:** CORRECT  
- **Expected:** `balance_after` captures post-transaction balance; status semantics (failed no change).  
- **Generated:** Explains `balance_after` and its linkage to `account_id` and accounts balances.  
- **Analysis:** Core correct (balance_after). Might not explicitly state “failed doesn’t affect balance,” but is still consistent with glossary/grounding.  
- **Retrieval:** gt_coverage=1.0, top_score=0.8666, gate=proceed

### 11: How does the customer_account junction table support multiple ownership types?
- **Type:** direct_mapping | **Difficulty:** Medium  
- **Verdict:** PARTIALLY_CORRECT  
- **Expected:** CHECK-enforced relationship types; is_primary designates primary; ownership_percentage tracks 0-100; multiple roles per account via multiple rows.  
- **Generated:** Correctly explains relationship_type is single per `(customer_id, account_id)` row and varies across rows.  
- **Analysis:** Likely grader expected explicit mention that multiple ownership types can exist simultaneously across different customer-account links; generated answer may have been deemed insufficiently aligned with expected wording/structure. (`grader_rejection_count=1`)  
- **Retrieval:** gt_coverage=1.0, top_score=0.9866, gate=proceed

### 12: What is the difference between current_balance and available_balance in the accounts table?
- **Type:** direct_mapping | **Difficulty:** Easy  
- **Verdict:** CORRECT  
- **Expected:** current includes pending; available excludes holds/pending; glossary confirms.  
- **Generated:** Matches the two definitions.  
- **Analysis:** Correct and grounded.  
- **Retrieval:** gt_coverage=1.0, top_score=0.8537, gate=proceed

### 13: How are loans linked to both customers and accounts in the schema?
- **Type:** multi_hop | **Difficulty:** Medium  
- **Verdict:** CORRECT  
- **Expected:** `loans.customer_id` FK non-null; `loans.account_id` optional FK; plus loan fields and loan_type constraint.  
- **Generated:** Correctly describes FK nullability and relationship.  
- **Analysis:** Correct; includes required connectivity.  
- **Retrieval:** gt_coverage=1.0, top_score=0.8103, gate=proceed

### 14: What types of transactions does the system support and how does their status lifecycle work?
- **Type:** direct_mapping | **Difficulty:** Easy  
- **Verdict:** CORRECT  
- **Expected:** 7 transaction types; 5 statuses; default Pending; glossary about posted/failed semantics.  
- **Generated:** Lists types and statuses and default Pending.  
- **Analysis:** Core lifecycle captured.  
- **Retrieval:** gt_coverage=1.0, top_score=0.7, gate=proceed

### 15: How does the schema support joint account ownership between multiple customers?
- **Type:** multi_hop | **Difficulty:** Medium  
- **Verdict:** CORRECT  
- **Expected:** `customer_account` junction with relationship_type CHECK; ownership_percentage; is_primary; date linkage.  
- **Generated:** Correctly describes many-to-many and fields.  
- **Analysis:** Grounded and aligned.  
- **Retrieval:** gt_coverage=1.0, top_score=0.7, gate=proceed

### 16: What information does the cards table track and how are cards linked to customers and accounts?
- **Type:** direct_mapping | **Difficulty:** Medium  
- **Verdict:** CORRECT  
- **Expected:** Fields (card_type/network/number/name/exp/cvv/limits/security/status) and FK links.  
- **Generated:** Comprehensive listing including FKs and lifecycle.  
- **Analysis:** Strong.  
- **Retrieval:** gt_coverage=1.0, top_score=0.9526, gate=proceed

### 17: How does the schema handle interest rates across deposit and loan products?
- **Type:** multi_hop | **Difficulty:** Hard  
- **Verdict:** CORRECT  
- **Expected:** deposits via accounts interest_rate + interest_earned; loans via loans interest_rate as APR; glossary on APR vs APY and compounding/amortization.  
- **Generated:** Correct structural distinction; notes APY not an explicit column name.  
- **Analysis:** Correct and reasonably grounded.  
- **Retrieval:** gt_coverage=1.0, top_score=0.7, gate=proceed

### 18: What types of branches does the bank operate and how do they differ in capabilities?
- **Type:** direct_mapping | **Difficulty:** Easy  
- **Verdict:** CORRECT  
- **Expected:** FullService vs Satellite vs ATMOnly capability differences; tracked via branch_type and fields.  
- **Generated:** Correctly contrasts capabilities.  
- **Analysis:** Grounded.  
- **Retrieval:** gt_coverage=1.0, top_score=0.7, gate=proceed

### 19: How are ATMs related to branches in the schema and what types of ATMs exist?
- **Type:** multi_hop | **Difficulty:** Medium  
- **Verdict:** CORRECT  
- **Expected:** `atms.branch_id` nullable for standalone; atm_type enumerations; operational status; replenishment rule.  
- **Generated:** Correct FK nullability and atm_type constraint list.  
- **Analysis:** Correct.  
- **Retrieval:** gt_coverage=1.0, top_score=0.7, gate=proceed

### 20: What is the lifecycle of a loan from application to completion?
- **Type:** direct_mapping | **Difficulty:** Medium  
- **Verdict:** PARTIALLY_CORRECT  
- **Expected:** Five states including Pending/Approved/Active/PaidOff/Defaulted with business meaning.  
- **Generated:** Correctly lists statuses and infers transitions “based strictly on schema,” but explicitly says there’s no workflow definition beyond statuses/dates.  
- **Analysis:** Likely partially mismatched with expected “workflow semantics” (grader may want more explicit glossary-driven staging).  
- **Retrieval:** gt_coverage=1.0, top_score=0.7, gate=proceed

### 21: What does preferred customer status mean and how is it tracked in the schema?
- **Type:** direct_mapping | **Difficulty:** Medium  
- **Verdict:** CORRECT  
- **Expected:** `customers.is_preferred` default false; VIP meaning (fee waivers, priority).  
- **Generated:** Correct.  
- **Analysis:** Grounded and aligned.  
- **Retrieval:** gt_coverage=1.0, top_score=0.7, gate=proceed

### 22: How does the accounts table support interest tracking and what business rules govern interest?
- **Type:** direct_mapping | **Difficulty:** Medium  
- **Verdict:** CORRECT  
- **Expected:** interest_rate + interest_earned; deposit interest credited monthly; APY compounding; promotional/penalty rules.  
- **Generated:** Matches schema columns and includes glossary rules.  
- **Analysis:** Correct.  
- **Retrieval:** gt_coverage=1.0, top_score=0.7, gate=proceed

### 23: Can an account exist without any customer linked to it?
- **Type:** negative | **Difficulty:** Medium  
- **Verdict:** PARTIALLY_CORRECT (likely expected abstain/deny differently)
- **Expected:** No orphan accounts (business rule enforced at application level), so “cannot exist without customer ownership.”  
- **Generated:** Concludes KG/DDL is insufficient to determine orphaning; says referential integrity for junction rows exists but no explicit “must have at least one row” constraint.  
- **Analysis:** This is a principled “not enough information” answer, but it conflicts with expected answer framing that the business rule guarantees at least one owner relationship. (`grader_rejection_count=1`)  
- **Retrieval:** gt_coverage=1.0, top_score=0.7, gate=proceed

### 24: How does the schema handle failed or cancelled transactions?
- **Type:** negative | **Difficulty:** Medium  
- **Verdict:** CORRECT  
- **Expected:** status states; failed logged for audit but no balance change; posted final; audit trail preserved.  
- **Generated:** Correctly identifies status constraint and mentions balance_after nullable; asserts failed/cancelled do not affect balance via glossary mapping.  
- **Analysis:** Should be acceptable and grounded.  
- **Retrieval:** gt_coverage=1.0, top_score=0.7, gate=proceed

### 25: What operational states can an ATM have and what do they mean for available services?
- **Type:** direct_mapping | **Difficulty:** Easy  
- **Verdict:** CORRECT  
- **Expected:** Operational, OutOfService, OutOfCash; meaning per glossary; replenishment relation.  
- **Generated:** Correctly maps to `atms.status` and interprets operational meaning.  
- **Analysis:** Grounded and aligned.  
- **Retrieval:** gt_coverage=1.0, top_score=0.7, gate=proceed

## Anomalies & Recommendations

### Red Flags
- **Grader rejections despite perfect grounding**:
  - `pipeline_health.total_grader_rejections=3`
  - appears tied to **semantic alignment with expected answers** on a few questions (not hallucination).
- **Negative questions are answered rather than abstained**:
  - `abstained_count=0` even for negative queries (22–24, 23 especially). The grader may expect a stricter “correctely-abstained” behavior or a specific “cannot determine” vs “yes/no” stance.

### Recommendations
1. **Tighten negative-query handling policy**: when expected behavior is “business rule enforced at app layer,” teach the model/judge to distinguish “schema cannot prove” vs “business rule states guarantee” more explicitly (e.g., add an internal confidence rubric for application-layer governance).
2. **Adjust grader alignment (or prompt) for “difference” questions** (e.g., Q2, Q9): the grader may want explicit glossary-derived distinctions even when the schema doesn’t state behavioral deltas directly.
3. **For multi-hop and lifecycle questions**, encourage responses to include both:
   - the enumerated states from CHECK constraints, and
   - the business semantics (e.g., glossary notes about what those states mean).
4. Track and report **why** grader rejected each case (not just counts) to separate “missing expected detail” from “wrong semantics.”

## Comparison Notes (if applicable)
- This bundle provides no `ablation_context.changes_vs_baseline`, so a strict causal comparison to AB-00 baseline isn’t possible.
- Nonetheless, the observed metrics represent a **best-case regime**: perfect builder completion, perfect ground-truth retrieval coverage, and 100% grounded answers.

If you want, I can also produce a compact table summarizing verdicts by query_id (CORRECT vs PARTIALLY_CORRECT) and correlate them to the three grader rejections for faster thesis reporting.