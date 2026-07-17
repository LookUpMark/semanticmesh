# AI-Judge Evaluation: AB-BEST-K20/02_intermediate_finance
**Evaluator:** (`gpt-5.4-nano-2026-03-17`) using `docs/AI_JUDGE_PROMPT.md`  
**Date:** 2026-07-17

---

# Ablation Study Evaluation: AB-BEST-K20 — 02_intermediate_finance

## Executive Summary
This ablation run shows an excellent end-to-end pipeline: all 8 schema tables completed successfully with no Cypher or ingestion failures, and query answering was consistently grounded (grounded_rate = 1.0) across all 25 questions. Retrieval quality is healthy overall (avg_gt_coverage = 1.0; avg_top_score ≈ 0.75) with no low-retrieval questions, and hallucination grading produced zero rejections for most questions (grader_rejection_count is small at the pipeline level). The main weakness is not factual accuracy, but that the system sometimes answers using only schema column definitions while under-specifying business-process nuance (e.g., loan lifecycle workflow) and includes at least one case where a grader rejection occurred despite a grounded answer.

## Scores

| Dimension | Score (1-5) | Weight | Weighted |
|---|---:|---:|---:|
| Builder Quality | 5 | 25% | 1.25 |
| Retrieval Effectiveness | 5 | 25% | 1.25 |
| Answer Quality | 4 | 30% | 1.20 |
| Pipeline Health | 4 | 10% | 0.40 |
| Ablation Impact | N/A | 10% | 0.00 |
| **Overall** |  |  | **4.10** |

## Dimension Analysis

### 1. Builder Quality (5/5)
- `tables_parsed=8`, `tables_completed=8`, `all_tables_completed=true`
- `cypher_failed=false`, `failed_mappings=[]`, `ingestion_errors=[]`
- Triplet/ER density looks strong for this dataset size: `triplets_extracted=240`, `entities_resolved=207` (no sign of weak extraction or over-merging failures)
- Builder latency shown as `elapsed_s: 0` (likely instrumentation artifact), but no operational failure signals exist.

### 2. Retrieval Effectiveness (5/5)
- `avg_gt_coverage = 1.0` (ground-truth sources retrieved for all questions)
- `avg_top_score = 0.7492` (healthy reranker confidence; well within expected range for `bge-reranker-v2-m3`)
- `abstained_count=0` and `gate_abstentions=0`: no evidence of false abstentions.
- `pipeline_health.questions_with_low_retrieval_score = 0` aligns with the per-question retrieval setup.

### 3. Answer Quality (4/5)
Signals:
- `query_report.grounded_rate = 1.0` and `grounded=true` per question where shown → no hallucination groundedness failures.
- `grader_rejection_count` is present at the pipeline level (`total_grader_rejections=3`) and per-question at least once (`query_id=11` and possibly `query_id=12`).
- The provided per-question answers are mostly semantically aligned with expectations, but a few show “schema-accurate but process-nuanced” gaps.

Notable examples:
- **Query 20 (Hard, loan lifecycle workflow)**: the generated answer correctly describes `loans.status` states but explicitly says the schema lacks step-by-step workflow states (application → disbursed → closed). That matches the “what is in the schema” interpretation, but it under-delivers vs the expected answer’s more process-like framing (still likely acceptable, hence 4 not 5).
- **Query 9 (Frozen meaning)**: generated answer says the business meaning of `Frozen` is not defined beyond being a status enum—whereas the expected answer implies “temporary/reversible suspension.” This is a semantic mismatch risk, though grounding is still true.

### 4. Pipeline Health (4/5)
- No builder or Cypher failures: `cypher_failed=false`, `failed_mappings_count=0`, `ingestion_errors_count=0`
- No gate issues: `gate_abstentions=0`
- Small but non-zero grader activity: `total_grader_rejections=3`, `grader_inconsistencies=0`
  - Zero inconsistencies suggests the self-reflection logic is stable.
  - The presence of grader rejections indicates the grader caught potential issues at least briefly, but recovery/validation appears successful since final outputs are grounded and no question failed.

### 5. Ablation Impact (N/A)
- The bundle is `AB-BEST-K20`, but the provided JSON does not include `ablation_context.changes_vs_baseline` or a baseline `study_id` reference.
- Therefore causal “impact vs baseline” cannot be validated with the rubric rules.

## Dimension Analysis: Key Supported Signals Across the Bundle
- **Builder**: perfect completion, no Cypher failures.
- **Retrieval**: perfect coverage, high reranker top score.
- **Grounding**: universally grounded (1.0).
- **Stability**: grader inconsistency = 0; only a few total grader rejections.

## Per-Question Deep Dive

### 1: What is a checking account?
- **Type:** direct_mapping | **Difficulty:** Easy
- **Verdict:** CORRECT
- **Expected:** Checking is an account type in `accounts` (CHECK constraint); glossary defines accounts; includes balance/fee/rates; account_subtype exists; debit card linkage mention.
- **Generated:** Defines Account + `accounts.account_type` includes `Checking`; describes related attributes.
- **Analysis:** Matches expected semantics using correct schema/glossary sources; extra attributes are fine.
- **Retrieval:** gt_coverage=1.0, top_score=0.7, gate=proceed

### 2: What is the difference between a savings account and a money market account?
- **Verdict:** PARTIALLY_CORRECT
- **Expected:** Interest/glossary examples show APY differences (Savings vs Money Market) and both are account types in `accounts`.
- **Generated:** Says explicit difference isn’t directly defined; uses glossary examples to describe interest examples but doesn’t clearly state “difference” beyond examples.
- **Analysis:** Semantically close but less direct than expected (still grounded).
- **Retrieval:** gt_coverage=1.0, top_score=0.3–0.7 (given retrieval_quality_score_adjusted=0.7), gate=proceed

### 3: What is APR versus APY?
- **Verdict:** CORRECT
- **Expected:** APR for loans, APY for deposits; APY reflects compounding; examples.
- **Generated:** Correctly states APR vs APY distinction and compounding/frequency concept.
- **Analysis:** Good semantic match.
- **Retrieval:** gt_coverage=1.0, top_score≈0.96, gate=proceed

### 4: What is KYC Level 2?
- **Verdict:** CORRECT
- **Expected:** `kyc_status` CHECK constraint includes Level1/2/3; Level1 min, Level3 for high-value/international; Level2 between but specific requirements not detailed.
- **Generated:** Correctly states valid Level2 and constraint; mentions defaults and glossary higher-level usage.
- **Analysis:** Matches “not detailed” expectation.
- **Retrieval:** gt_coverage=1.0, top_score=0.7, gate=proceed

### 5: How does the schema support different account subtypes and their varying requirements?
- **Verdict:** CORRECT
- **Expected:** `account_subtype` + subtype-dependent attributes; minimum balance can trigger fees.
- **Generated:** Correctly references `account_subtype` and explains related nullable fields/defaults; describes requirements at schema level.
- **Analysis:** Slight risk of overemphasis on interest_rate/status vs min_balance/monthly_fee but still aligned.
- **Retrieval:** gt_coverage=1.0, top_score=0.7, gate=proceed

### 6: What types of loan products does the bank offer?
- **Verdict:** CORRECT
- **Expected:** 5 loan types via CHECK constraint; brief collateral/KYC/defaulted notes.
- **Generated:** Lists all five types correctly; cites constraint.
- **Analysis:** Expected nuance present at least implicitly via schema description.
- **Retrieval:** gt_coverage=1.0, top_score=0.7, gate=proceed

### 7: What is the daily ATM withdrawal limit defined in the schema?
- **Verdict:** CORRECT
- **Expected:** `cards.atm_daily_limit` default 500.00; per-card limit.
- **Generated:** States `atm_daily_limit` = 500.00.
- **Analysis:** Doesn’t explicitly say “per-card” but schema context implies it; still correct.
- **Retrieval:** gt_coverage=1.0, top_score=0.7, gate=proceed

### 8: What is the difference between a parent account and a child account?
- **Verdict:** CORRECT
- **Expected:** `parent_account_id` self-reference; top-level NULL; hierarchy supports portfolio aggregation.
- **Generated:** Correctly explains parent/child definitions and constraint preventing self-reference.
- **Analysis:** Full semantic match.
- **Retrieval:** gt_coverage=1.0, top_score=0.7, gate=proceed

### 9: What does the status 'Frozen' mean for a card?
- **Verdict:** PARTIALLY_CORRECT
- **Expected:** Frozen vs Blocked distinguished; implies temporary restriction.
- **Generated:** Says business meaning of Frozen is not defined beyond being an enum value.
- **Analysis:** Under-specifies meaning compared to expected; but no hallucination.
- **Retrieval:** gt_coverage=1.0, top_score=0.7, gate=proceed

### 10: How does the transactions table track the impact of each transaction on account balances?
- **Verdict:** CORRECT
- **Expected:** `balance_after` per transaction; debit/credit impact; statuses; glossary rules.
- **Generated:** Correctly identifies `balance_after` and ties to account.
- **Analysis:** Omits explicit “debit reduces / credit increases” linkage, but balance_after semantics cover the core asked point.
- **Retrieval:** gt_coverage=1.0, top_score=0.7, gate=proceed

### 11: How does the customer_account junction table support multiple ownership types?
- **Verdict:** PARTIALLY_CORRECT
- **Expected:** CHECK constraint on relationship_type; is_primary and ownership_percentage; composite PK; multiple role links possible.
- **Generated:** Correct design reasoning (role per customer-account pair).
- **Analysis:** Despite being conceptually correct, this question has `grader_rejection_count=1` in bundle → grader judged a mismatch at least once (final decision still grounded).
- **Retrieval:** gt_coverage=1.0, top_score=0.9866, gate=proceed

### 12: What is the difference between current_balance and available_balance in the accounts table?
- **Verdict:** CORRECT
- **Expected:** current includes pending; available excludes holds/pending; glossary confirms.
- **Generated:** Matches the column descriptions precisely.
- **Analysis:** Correct.
- **Retrieval:** gt_coverage=1.0, top_score=0.8537, gate=proceed

### 13: How are loans linked to both customers and accounts in the schema?
- **Verdict:** CORRECT
- **Expected:** `loans.customer_id` non-null FK; `loans.account_id` nullable FK; loan tracks other terms.
- **Generated:** Correctly explains nullability and FK relationships.
- **Analysis:** Full semantic match.
- **Retrieval:** gt_coverage=1.0, top_score≈0.81, gate=proceed

### 14: What types of transactions does the system support and how does their status lifecycle work?
- **Verdict:** CORRECT
- **Expected:** 7 transaction types; 5 status lifecycle states; default Pending.
- **Generated:** Lists both enums and default Pending; mentions balance_after.
- **Analysis:** Good semantic match.
- **Retrieval:** gt_coverage=1.0, top_score=0.7, gate=proceed

### 15: How does the schema support joint account ownership between multiple customers?
- **Verdict:** INCORRECT (or PARTIALLY_CORRECT depending on grader interpretation)
- **Expected:** Joint via `customer_account` many-to-many; relationship_type CHECK; ownership_percentage; is_primary; linkage dates; multiple customers per account with different roles.
- **Generated:** Correctly explains many-to-many and fields, but the run shows retrieval correctness and grounding; however multi-hop joint semantics should be compared with expected precisely—no explicit “multiple rows per account” statement is required but it’s implied via PK.
- **Analysis:** Likely correct design-wise; however based on rubric strictness, it’s missing one explicit piece: statement that same account_id appears in multiple rows for different customers (though it does describe composite PK and per-link fields).
- **Retrieval:** gt_coverage=1.0, top_score=0.7, gate=proceed

### 16: What information does the cards table track and how are cards linked to customers and accounts?
- **Verdict:** CORRECT
- **Expected:** card_type/network/number/name/exp/cvv; limits; security features; status lifecycle; FKs required.
- **Generated:** Thoroughly enumerates card columns and states required FKs.
- **Analysis:** Strong match.
- **Retrieval:** gt_coverage=1.0, top_score≈0.95, gate=proceed

### 17: How does the schema handle interest rates across deposit and loan products?
- **Verdict:** PARTIALLY_CORRECT
- **Expected:** APR for loans, APY/deposit; deposit interest credited monthly; promotional/penalty notes.
- **Generated:** Correctly explains APR in loans and interest_rate/interest_earned at account level; says APY column name not exposed.
- **Analysis:** Most concepts covered, but glossary nuance about APY vs APR mapping could be more explicit.
- **Retrieval:** gt_coverage=1.0, top_score=0.7, gate=proceed

### 18: What types of branches does the bank operate and how do they differ in capabilities?
- **Verdict:** PARTIALLY_CORRECT
- **Expected:** FullService vs Satellite vs ATMOnly capability differences including loan origination/advisors and 24/7.
- **Generated:** Explains the three types and capability reductions; focuses on what is in schema but doesn’t clearly include safe-deposit boxes/advisor details or 24/7 access.
- **Analysis:** Semantically close but missing some expected capability specifics.
- **Retrieval:** gt_coverage=1.0, top_score=0.7, gate=proceed

### 19: How are ATMs related to branches in the schema and what types of ATMs exist?
- **Verdict:** CORRECT
- **Expected:** Nullable branch_id means standalone; atm_type has Branch/DriveThrough/Standalone (and definition nuance).
- **Generated:** Correctly describes nullable FK and atm_type enum.
- **Analysis:** Good match; glossary-level notes about cash replenishment not emphasized but question asks types and relationship.
- **Retrieval:** gt_coverage=1.0, top_score=0.7, gate=proceed

### 20: What is the lifecycle of a loan from application to completion?
- **Verdict:** PARTIALLY_CORRECT
- **Expected:** Five status states plus process explanation from application to approval/active/paid/defaulted.
- **Generated:** Says explicit step-by-step workflow isn’t defined; correctly describes `loans.status` states and timelines (origination/maturity).
- **Analysis:** The expectation includes process-like lifecycle; the system stayed strictly schema-based, which is defensible but under-delivers.
- **Retrieval:** gt_coverage=1.0, top_score=0.7, gate=proceed

### 21: What does preferred customer status mean and how is it tracked in the schema?
- **Verdict:** CORRECT
- **Expected:** `customers.is_preferred` default false; glossary says fee waivers/priority.
- **Generated:** Correctly identifies VIP flag and default.
- **Analysis:** Good match.
- **Retrieval:** gt_coverage=1.0, top_score=0.7, gate=proceed

### 22: How does the accounts table support interest tracking and what business rules govern interest?
- **Verdict:** CORRECT
- **Expected:** interest_rate and interest_earned; glossary rules including monthly crediting; promotional/penalty notes.
- **Generated:** Explains interest_rate nullable, interest_earned defaults, and glossary monthly crediting/compounding/promotional/penalty behaviors.
- **Analysis:** Good alignment.
- **Retrieval:** gt_coverage=1.0, top_score=0.7, gate=proceed

### 23: Can an account exist without any customer linked to it?
- **Verdict:** CORRECTLY_ABSTAINED
- **Expected:** Negative question: should abstain or answer “cannot determine / not enough info” based on schema-level constraints + app/business rule.
- **Generated:** Correctly argues insufficient explicit DDL constraint to decide orphaning; avoids fabrication.
- **Analysis:** Correct negative-handling behavior.
- **Retrieval:** gt_coverage=1.0, top_score=0.7, gate=proceed

### 24: How does the schema handle failed or cancelled transactions?
- **Verdict:** CORRECT
- **Expected:** status enum includes Failed/Cancelled; glossary says failed logged for audit but no balance impact; posted is final.
- **Generated:** Discusses status constraint, balance_after nullable, and glossary business rules.
- **Analysis:** Grounded and aligned.
- **Retrieval:** gt_coverage=1.0, top_score=0.7, gate=proceed

### 25: What operational states can an ATM have and what do they mean for available services?
- **Verdict:** CORRECT
- **Expected:** Operational / OutOfService / OutOfCash; meanings including what services are blocked.
- **Generated:** Correctly maps to `atms.status` and describes meaning.
- **Analysis:** Good match.
- **Retrieval:** gt_coverage=1.0, top_score=0.7, gate=proceed

## Anomalies & Recommendations

### Red Flags
- **Grader rejections despite grounding**: `pipeline_health.total_grader_rejections=3` and `query_id=11` shows `grader_rejection_count=1`. This suggests occasional semantic interpretation mismatches (likely around modeling details like “multiple ownership types” wording or precision of how relationships are represented).
- **Process-knowledge gaps on “lifecycle workflow” questions**: for **Query 20**, the system correctly admits lack of explicit step workflow states, but the expected answer frames a business lifecycle narrative. If the evaluation expects richer narrative, you may need a pattern: “schema states correspond to business stages” even when not explicitly labeled as such.

### Recommendations
1. **Tighten mapping from enum states to business lifecycle narrative**  
   For lifecycle-style questions (loan lifecycle, card lifecycle distinctions like Frozen vs Blocked), add a post-processing step that explicitly links glossary phrasing to schema enums (when glossary is present), rather than relying on the model to infer missing meaning.
2. **Handle “difference between X and Y” by extracting differential attributes**  
   Query 2 and Query 17 show tendencies to answer “not explicitly defined” unless prompted to list the differential fields (e.g., APY tiers by balance vs compounding frequency). Add an instruction to always summarize “key differentiators present in sources” when both entities are defined in the same table/glossary section.
3. **Investigate grader rejection causes in Query 11**  
   Since grounding is true, the rejection is likely about completeness/overstatement (e.g., default values or nullability wording). Review the critic/grader prompt alignment for relationship modeling questions.

## Comparison Notes (if applicable)
- No baseline (`AB-00`) comparison data or `ablation_context` was included in the bundle, so differences vs baseline cannot be attributed causally per rubric requirements.