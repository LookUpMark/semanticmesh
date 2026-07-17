# AI-Judge Evaluation: AB-BEST-K20/06_edgecases_legacy
**Evaluator:** (`gpt-5.4-nano-2026-03-17`) using `docs/AI_JUDGE_PROMPT.md`  
**Date:** 2026-07-17

---

# Ablation Study Evaluation: AB-BEST-K20 — 06_edgecases_legacy

## Executive Summary
This run shows **near-perfect end-to-end behavior** for the query graph: all 25 questions were answered with **grounded_rate = 1.0**, **gt_coverage = 1.0**, and **gate_decision = proceed** for every case. Builder ingestion and Cypher execution were also stable (**all_tables_completed = true**, **cypher_failed = false**, **ingestion_errors = []**), indicating the Builder Graph produced a usable KG for these legacy edge-case questions.

The main limitation is not incorrectness but **retrieval quality variability**: several questions have **low retrieval_quality_score_raw (~0.55–0.59) with pool_confidence_applied=true**, suggesting the reranker/top-pool confidence thresholding may have “let through” adequate contexts rather than strongly ranked ones.

---

## Scores

| Dimension | Score (1-5) | Weight | Weighted |
|---|---:|---:|---:|
| Builder Quality | 5 | 25% | 1.25 |
| Retrieval Effectiveness | 4 | 25% | 1.00 |
| Answer Quality | 5 | 30% | 1.50 |
| Pipeline Health | 5 | 10% | 0.50 |
| Ablation Impact | N/A | 10% | 0.00 |
| **Overall** |  |  | **4.25** |

---

## Dimension Analysis

### 1. Builder Quality (5/5)
Evidence from `builder_report`:
- `tables_parsed = 10`, `tables_completed = 10`, `all_tables_completed = true`
- `cypher_failed = false`
- `failed_mappings = []`
- `ingestion_errors = []`
- `triplets_extracted = 154`, `entities_resolved = 140` (no obvious ER collapse/explosion)
- Builder latency and trace fields are inconsistent/empty (`elapsed_s = 0`), but **no failure signals** appear.

**Conclusion:** Builder Graph is functioning correctly and produced a complete KG for the target schema.

---

### 2. Retrieval Effectiveness (4/5)
Evidence from `query_report` and `per_question`:
- `avg_gt_coverage = 1.0` and every question has `gt_coverage = 1.0` in the provided sample → **no ground-truth retrieval misses**
- `avg_top_score = 0.8139` (healthy; above typical “comfort” for cross-enc rerankers)
- However, there are cases where `retrieval_quality_score_raw` is notably lower, e.g.:
  - Query **4**: raw **0.55** (adjusted to **0.7** via `pool_confidence_applied=true`)
  - Query **5**: raw **0.55**
  - Query **6**: raw **0.55**
  - Query **7**: raw **0.55**
  - Query **8**: raw **0.55**
  - Query **11**: raw **0.55**
  - Query **14**: raw **0.55**
  - Query **15**: raw **0.55**
  - Many others show raw ≈0.55 while adjusted hits the **0.7** floor.

This indicates retrieval ranking is sometimes only “just sufficient,” but the system’s context gating/pool-confidence logic preserves final answer correctness.

**Conclusion:** Retrieval is effective in terms of coverage and final grounding, but the raw reranker confidence suggests **some fragility**.

---

### 3. Answer Quality (5/5)
Evidence:
- `query_report.grounded_rate = 1.0` (all questions grounded)
- `grader_rejection_count = 0` for all shown questions
- Negative/abstention behavior is not exercised here (`abstained_count = 0`), but for non-negative questions, answers match expected semantics.

Per-question highlights:
- **Query 1** (“purpose of tblCustomer”) correctly includes Hungarian notation, legacy + migration compatibility fields.
- **Query 2** (“How customers identified…”) correctly states `strCustID` as VARCHAR(50), alphanumeric AS/400-derived codes.
- **Query 3** (“order header table & PK”) correctly identifies `vw_SalesOrderHdr.lngOrderID` as INT PK despite `vw_` naming.
- **Query 4** (“reserved word table”) correctly identifies `Group` and `User` requiring bracket quoting.
- **Query 7** (“unit_cost issue”) correctly identifies VARCHAR type + `$` symbol parsing requirement.
- **Query 25** (“critical data quality issues”) correctly aggregates the major categories and includes PCI + FK + type + security concerns.

**Conclusion:** Outputs are semantically correct, comprehensive relative to expected answers, and consistently grounded.

---

### 4. Pipeline Health (5/5)
Evidence from `pipeline_health`:
- `total_grader_rejections = 0`
- `grader_inconsistencies = 0`
- `gate_abstentions = 0`
- `cypher_failed = false`
- `failed_mappings_count = 0`
- `ingestion_errors_count = 0`

This run shows **no instability** and no self-healing failures.

---

### 5. Ablation Impact (N/A)
This bundle is labeled `AB-BEST-K20`, but the provided JSON **does not include**:
- explicit comparison to baseline (`AB-00`)
- a `changes_vs_baseline` / `ablation_context` field
- toggles that changed vs baseline are not provided as an “ablation spec”

So this dimension is **not scorable** under the rubric.

---

## Per-Question Deep Dive

> Verdict mapping:
- **CORRECT** = expected facts covered and grounded
- **PARTIALLY_CORRECT** = missing key expected facts (not seen here)
- **INCORRECT** = wrong facts or ungrounded (not seen here)
- **CORRECTLY_ABSTAINED / WRONGLY_ABSTAINED** = not applicable (no abstentions)

### 1: What is the purpose of the tblCustomer table?
- **Type:** unknown | **Difficulty:** unknown
- **Verdict:** CORRECT
- **Expected:** tblCustomer stores customer master data; includes legacy codes/names/emails/region and migration fields (cust_id, customer_name)
- **Generated:** Correctly describes purpose, legacy AS/400 identifier, fields, and migration placeholders; mentions bolActive timestamps etc.
- **Analysis:** Matches expected intent and key fields; grounded in retrieved dictionary content.
- **Retrieval:** gt_coverage=1.0, top_score=0.8139919335890311, gate=proceed

### 2: How are customers identified in the legacy system?
- **Verdict:** CORRECT
- **Expected:** `strCustID` is VARCHAR(50), alphanumeric formats like C-XXXXX or REG-XXXX
- **Generated:** Correctly identifies `strCustID` and format examples; mentions PK/UNIQUE/NOT NULL.
- **Analysis:** Fully aligned with expected semantic content.
- **Retrieval:** gt_coverage=1.0, top_score=0.8139919335890311, gate=proceed

### 3: What table stores order header information and what is its primary key?
- **Verdict:** CORRECT
- **Expected:** `vw_SalesOrderHdr` table despite vw prefix; PK is `lngOrderID` INT with lng prefix
- **Generated:** Matches both table name and primary key.
- **Analysis:** Correct semantic handling of naming quirk.
- **Retrieval:** gt_coverage=1.0, top_score=0.9353465116437761, gate=proceed

### 4: Which table in the schema uses a SQL reserved word as its name?
- **Verdict:** CORRECT
- **Expected:** `Group` and `User` are reserved; require `[Group]` and `[User]`
- **Generated:** Identifies both and quotes the bracket rule.
- **Analysis:** Correct.
- **Retrieval:** gt_coverage=1.0, top_score=0.7, gate=proceed

### 5: What is the relationship between vw_SalesOrderHdr and tblCustomer?
- **Verdict:** CORRECT
- **Expected:** `vw_SalesOrderHdr.intCustID` (VARCHAR) → `tblCustomer.strCustID`
- **Generated:** Correctly states FK and one-to-many relationship.
- **Analysis:** Correct FK direction + datatype nuance.
- **Retrieval:** gt_coverage=1.0, top_score=0.8292155820981656, gate=proceed

### 6: What naming convention is used for the inventory transaction log table?
- **Verdict:** CORRECT
- **Expected:** `inv_txn_log` with abbreviated field names like txn_id, txn_dt, txn_type, prod_id
- **Generated:** Correctly describes heavily abbreviated convention.
- **Analysis:** Correct but relies on “naming convention” label; still grounded.
- **Retrieval:** gt_coverage=1.0, top_score=0.7, gate=proceed

### 7: What data quality issue exists in the tblProduct unit_cost field?
- **Verdict:** CORRECT
- **Expected:** `unit_cost` is VARCHAR(20) not DECIMAL; contains `$` requiring parsing
- **Generated:** Correctly describes VARCHAR(20), `$` symbols, should be DECIMAL.
- **Analysis:** Correct.
- **Retrieval:** gt_coverage=1.0, top_score=0.7, gate=proceed

### 8: How does the ord_line_item table handle product data redundancy?
- **Verdict:** CORRECT
- **Expected:** redundant `product_code` and `item_name` snapshot and should not be updated
- **Generated:** Correctly explains redundancy and “do not update from product master”.
- **Analysis:** Correct.
- **Retrieval:** gt_coverage=1.0, top_score=0.7, gate=proceed

### 9: What are the valid values for the strOrderStatus field in vw_SalesOrderHdr?
- **Verdict:** CORRECT
- **Expected:** PENDING, SHIPPED, CANCELLED (CHECK constraint)
- **Generated:** Lists exactly these values.
- **Analysis:** Correct.
- **Retrieval:** gt_coverage=1.0, top_score=0.7, gate=proceed

### 10: Which table stores payment information and what security issue does it have?
- **Verdict:** CORRECT
- **Expected:** tblPayment; CardNumberText stores plaintext PAN; PCI violation
- **Generated:** Correctly identifies table and summarizes PCI issue.
- **Analysis:** Correct.
- **Retrieval:** gt_coverage=1.0, top_score=0.7, gate=proceed

### 11: What is the purpose of the bolActive field in tblCustomer and tblProduct?
- **Verdict:** CORRECT
- **Expected:** Active flag; customers excluded from marketing when 0; products discontinued when 0
- **Generated:** Correctly states semantics for both tables.
- **Analysis:** Correct.
- **Retrieval:** gt_coverage=1.0, top_score=0.9645892699236761, gate=proceed

### 12: How are inventory transactions tracked in the system?
- **Verdict:** CORRECT
- **Expected:** inv_txn_log; txn_type IN/OUT/ADJ; abbreviated fields; prod_id references product
- **Generated:** Very complete; includes quantity sign logic and audit purpose.
- **Analysis:** Correct and even adds extra consistent detail.
- **Retrieval:** gt_coverage=1.0, top_score=0.9305845275935024, gate=proceed

### 13: What is the self-referencing relationship in the Group table?
- **Verdict:** CORRECT
- **Expected:** ParentGroupID → GroupID hierarchy; NULL = top-level
- **Generated:** Correct one-to-many self ref and NULL semantics.
- **Analysis:** Correct.
- **Retrieval:** gt_coverage=1.0, top_score=0.7, gate=proceed

### 14: What migration compatibility columns exist in tblCustomer?
- **Verdict:** CORRECT
- **Expected:** cust_id and customer_name
- **Generated:** Correctly describes both with intended migration meaning and NULL status.
- **Analysis:** Correct.
- **Retrieval:** gt_coverage=1.0, top_score=0.7, gate=proceed

### 15: How does the system handle order status history tracking?
- **Verdict:** CORRECT
- **Expected:** tblOrderStatusHistory audit trail for each status transition; includes OrderID, OldStatus, NewStatus, ChangedByUser, ChangedDate, ChangeReason
- **Generated:** Correctly enumerates fields and ties to glossary “every status change creates a history record”.
- **Analysis:** Correct.
- **Retrieval:** gt_coverage=1.0, top_score=0.7, gate=proceed

### 16: What is the inconsistent naming pattern between order tables?
- **Verdict:** CORRECT
- **Expected:** vw_SalesOrderHdr uses vw_ but is actually table; ord_line_item uses ord_ and references lngOrderID as ord_id
- **Generated:** Correctly explains naming inconsistency and cross-table prefix mismatch.
- **Analysis:** Correct.
- **Retrieval:** gt_coverage=1.0, top_score=0.7, gate=proceed

### 17: What deprecated fields exist in tblProduct and why should they be avoided?
- **Verdict:** CORRECT
- **Expected:** prod_num, item_desc, unit_cost—deprecated/bugs; shouldn’t be used for new code
- **Generated:** Correctly identifies and explains each deprecated field and “Only strSKU should be used”.
- **Analysis:** Correct.
- **Retrieval:** gt_coverage=1.0, top_score=0.7, gate=proceed

### 18: How are shipping carriers configured in the system?
- **Verdict:** CORRECT
- **Expected:** tblShippingCarrier with CarrierID/Name/Code/TrackingURL/bolActive; only bolActive=1 offered
- **Generated:** Correctly states fields and bolActive business rule.
- **Analysis:** Correct.
- **Retrieval:** gt_coverage=1.0, top_score=0.7, gate=proceed

### 19: What is the relationship between User table passwords and security?
- **Verdict:** CORRECT
- **Expected:** PasswordHash uses SHA-256 without salt → rainbow-table vulnerability
- **Generated:** Correctly points to unsalted SHA-256 and repeats the password security issue.
- **Analysis:** Correct (even though it also mentions other security issues; extra correct info is fine).
- **Retrieval:** gt_coverage=1.0, top_score=0.7, gate=proceed

### 20: What fields in vw_SalesOrderHdr use the 'flt' Hungarian notation prefix and what do they store?
- **Verdict:** CORRECT
- **Expected:** fltSubTotal, fltTaxAmount, fltTotalAmount are monetary fields (DECIMAL(12,2))
- **Generated:** Correctly lists all three and explains stored meaning.
- **Analysis:** Correct.
- **Retrieval:** gt_coverage=1.0, top_score=0.9628830911922404, gate=proceed

### 21: How does the schema handle the different date/time field naming conventions?
- **Verdict:** CORRECT
- **Expected:** dtm prefix for datetime fields; also notes exceptions (User table uses LastLogin/CreatedDate)
- **Generated:** Correctly states general dtm usage but also points out inconsistent overall conventions and exceptions. This is aligned with expected intent.
- **Analysis:** Correct semantic coverage.
- **Retrieval:** gt_coverage=1.0, top_score=0.7, gate=proceed

### 22: What table prefix patterns exist in the schema and what do they indicate?
- **Verdict:** CORRECT
- **Expected:** tbl, vw_ (misnamed), ord_, inv_, plus reserved-word no-prefix Group/User
- **Generated:** Correctly enumerates prefix patterns and indicates vw_ is misleading; explains ord_/inv_ purpose.
- **Analysis:** Correct.
- **Retrieval:** gt_coverage=1.0, top_score=0.9955662347993564, gate=proceed

### 23: What foreign key relationships exist for the vw_SalesOrderHdr table?
- **Verdict:** CORRECT
- **Expected:** Explicit FK: intCustID→tblCustomer.strCustID; implicit refs from Payment/OrderStatusHistory/LineItems to lngOrderID
- **Generated:** Correctly lists those relationships.
- **Analysis:** Correct.
- **Retrieval:** gt_coverage=1.0, top_score=0.9955662347993564, gate=proceed

### 24: How does the legacy system handle product SKU format and uniqueness?
- **Verdict:** CORRECT
- **Expected:** strSKU has UNIQUE and format Category-Color-Size; prod_num deprecated
- **Generated:** Correct.
- **Analysis:** Correct.
- **Retrieval:** gt_coverage=1.0, top_score=0.9662197710315901, gate=proceed

### 25: What are the critical data quality issues identified for migration?
- **Verdict:** CORRECT
- **Expected:** PCI plaintext card numbers; unit_cost type; missing FK inv_txn_log.user_id; unsalted SHA-256 password hash; misleading Hungarian notation; reserved words quoting requirement
- **Generated:** Correctly aggregates multiple critical categories (FK gaps, security/privacy, data inconsistencies). It emphasizes referential integrity gaps as well, which is consistent with the provided glossary.
- **Analysis:** Semantically correct and grounded; includes all major expected themes.
- **Retrieval:** gt_coverage=1.0, top_score=0.9662197710315901, gate=proceed

---

## Anomalies & Recommendations

### Red Flags
1. **Retrieval confidence floor masking variability**
   - Many questions show `retrieval_quality_score_raw ≈ 0.55` while `retrieval_quality_score_adjusted = 0.7` due to `pool_confidence_applied = true`.
   - This suggests the reranker’s top candidates weren’t always very confident, but the system’s gating/pool mechanism still recovered sufficient contexts.

2. **No abstention coverage**
   - `abstained_count = 0` and `gate_abstentions = 0`. If negative questions exist in the real use-case, this ablation run doesn’t test the abstention mechanism.

3. **Dataset_info complexity/difficulty fields are empty**
   - `dataset_info.complexity = ""`, `difficulty_distribution` keys are “unknown”, so difficulty-aware tuning cannot be validated from this bundle alone.

### Recommendations
- **Instrument retrieval diagnostics beyond top-score**: log distribution of reranker scores (mean/std) and how often the adjusted floor triggers. Consider a policy to increase `pool_size` or relax noise filtering only when raw < threshold but gt coverage is still 1.0.
- **Add explicit negative/abstention test cases** in future bundles (even if expected answer is “not found”), to validate `retrieval_quality_gate` behavior.
- **Use `elapsed_s` correctly** for builder/query reports; currently builder/query `elapsed_s` is `0`, limiting latency regression detection.

---

## Comparison Notes (if applicable)
No baseline (`AB-00`) results or `ablation_context.changes_vs_baseline` were provided, so a causal comparison to the baseline cannot be performed under the rubric.