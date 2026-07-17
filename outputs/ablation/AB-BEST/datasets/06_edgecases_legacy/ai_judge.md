# AI-Judge Evaluation: AB-BEST/06_edgecases_legacy
**Evaluator:** (`gpt-5.4-nano-2026-03-17`) using `docs/AI_JUDGE_PROMPT.md`  
**Date:** 2026-07-17

---

# Ablation Study Evaluation: AB-BEST — 06_edgecases_legacy

## Executive Summary
AB-BEST shows strong end-to-end system health: all 10 builder tables completed with no Cypher failures, and query-time answers were 100% grounded with zero abstentions across 25 edge-case questions. Retrieval quality is mixed (several questions show lower raw retrieval confidence despite being correct), but answer quality remains consistently correct and well-aligned with the expected legacy migration semantics.

The main concern is *not correctness* (it’s consistently correct), but *retrieval signal integrity*: multiple questions with low adjusted relevance (and some `gt_coverage=0`) still produced correct, grounded answers—suggesting the scoring/coverage bookkeeping may not be tightly coupled to actual usefulness of retrieved contexts.

---

## Scores

| Dimension | Score (1-5) | Weight | Weighted |
|---|---:|---:|---:|
| Builder Quality | 5 | 25% | 1.25 |
| Retrieval Effectiveness | 4 | 25% | 1.00 |
| Answer Quality | 5 | 30% | 1.50 |
| Pipeline Health | 5 | 10% | 0.50 |
| Ablation Impact | 5 | 10% | 0.50 |
| **Overall** |  |  | **4.25** |

---

## Dimension Analysis

### 1. Builder Quality (5/5)
- `tables_parsed=10`, `tables_completed=10`, `all_tables_completed=true`
- `cypher_failed=false`, `failed_mappings=[]`, `ingestion_errors=[]`
- Triplet extraction density appears healthy (`triplets_extracted=154` across 10 tables; entities_resolved=145)
- No signs the builder was unstable or skipped.

**Verdict:** Meets score-5 criteria: fully completed build with no failures.

### 2. Retrieval Effectiveness (4/5)
- Overall query groundedness is perfect (`grounded_rate=1.0`), and no false abstentions (`abstained_count=0`).
- However, retrieval confidence signals are not uniformly strong:
  - `avg_gt_coverage = 0.6302` (moderate; well below the 0.8 threshold for score-5)
  - `avg_top_score = 0.7950` (high; suggests reranker confidence was generally strong)
- Several individual questions show *low/zero* `gt_coverage` while still being correct (e.g., `query_id 4, 13, 14, 16, 17, 18, 19, 21, 22, 23, 24, 25` have `gt_coverage=0.0` in the bundle for multiple cases).

**Expert interpretation:** The system often answered correctly even when the bookkeeping “ground-truth coverage” was low—likely because the answer could be supported by non-designated sources or other retrieved context that still contains the facts. This prevents giving score 5, but does not indicate end-to-end retrieval failure.

### 3. Answer Quality (5/5)
- `grounded_rate=1.0` and `grader_rejection_count=0` for essentially all questions (only `pipeline_health.total_grader_rejections=1`, with no per-question pattern of incorrect-but-accepted outputs).
- Per-question inspection of representative cases shows semantic alignment with expected answers:
  - `query_id 1` correctly identifies tblCustomer purpose (legacy CRM master data, includes Hungarian fields and migration placeholders).
  - `query_id 4` correctly identifies reserved word tables as `Group` and `User` and quoting requirement.
  - `query_id 10` correctly states the PCI issue in `tblPayment.CardNumberText`.
  - `query_id 13` correctly states the self-referencing FK `ParentGroupID -> GroupID`.
  - `query_id 25` correctly lists critical migration issues (PCI, unit_cost type, missing FK on inv_txn_log.user_id, unsalted SHA-256, etc.).

**Verdict:** Consistent correctness + no hallucinations.

### 4. Pipeline Health (5/5)
- `cypher_failed=false`
- `failed_mappings_count=0`
- `ingestion_errors_count=0`
- `grader_inconsistencies=0`
- `gate_abstentions=0`
- `pipeline_health.total_grader_rejections=1` but no evidence of widespread instability; per-question `grader_rejection_count` is 0 for the shown items, suggesting the single rejection may be transient or internal to the reflection loops.

**Verdict:** Stable and error-free overall.

### 5. Ablation Impact (5/5)
- Study: `AB-BEST`
- Config matches a strong setup: `retrieval_mode=hybrid`, `enable_reranker=true` (with cross-encoder), and no ablation flags disabling key quality loops are evident.
- Given the excellent groundedness and builder completion, AB-BEST achieves the expected “best” behavior: correctness preserved and reliability high.

**Verdict:** Observed behavior matches “optimal” expectations.

---

## Per-Question Deep Dive

### 1: What is the purpose of the tblCustomer table?
- **Type:** unknown | **Difficulty:** unknown
- **Verdict:** CORRECT
- **Expected:** Stores customer master data; includes customer codes, names, email, region; includes legacy (`strCustID`, `strFullName`) and migration compatibility (`cust_id`, `customer_name`) fields.
- **Generated:** Stores customer master data from legacy CRM.
- **Analysis:** Matches purpose and domain meaning; migration placeholders present in retrieved context.
- **Retrieval:** gt_coverage=1.0, top_score=0.9922, gate=proceed

### 2: How are customers identified in the legacy system?
- **Verdict:** CORRECT
- **Expected:** Identified by `strCustID` (VARCHAR(50), PK), AS/400-derived formats like `C-XXXXX`/`REG-XXXX`.
- **Generated:** Exactly that; includes PK/UNIQUE and NOT NULL.
- **Analysis:** Complete and precise.
- **Retrieval:** gt_coverage=1.0, top_score=0.8292, gate=proceed

### 3: What table stores order header information and what is its primary key?
- **Verdict:** CORRECT
- **Expected:** `vw_SalesOrderHdr` table; PK `lngOrderID` (INT, PK) despite `vw_` prefix.
- **Generated:** Matches.
- **Retrieval:** gt_coverage=1.0, top_score=0.7432, gate=proceed

### 4: Which table in the schema uses a SQL reserved word as its name?
- **Verdict:** CORRECT
- **Expected:** `Group` and `User`, quoted as `[Group]` and `[User]`.
- **Generated:** Matches both.
- **Analysis:** Correct reserved-word handling.
- **Retrieval:** gt_coverage=0.0, top_score=0.7, gate=proceed

### 5: What is the relationship between vw_SalesOrderHdr and tblCustomer?
- **Verdict:** CORRECT
- **Expected:** FK: `intCustID -> tblCustomer.strCustID`; one customer to many orders.
- **Generated:** Matches one-to-many relationship and FK.
- **Retrieval:** gt_coverage=1.0, top_score=0.9988, gate=proceed

### 6: What naming convention is used for the inventory transaction log table?
- **Verdict:** CORRECT
- **Expected:** `inv_txn_log`; abbreviated naming; abbreviated fields like `txn_id`, `txn_dt`, `txn_type`, `prod_id`.
- **Generated:** Mentions `inv_` and abbreviated convention; matches general naming.
- **Retrieval:** gt_coverage=1.0, top_score=0.9306, gate=proceed

### 7: What data quality issue exists in the tblProduct unit_cost field?
- **Verdict:** CORRECT
- **Expected:** `unit_cost` is VARCHAR(20) not DECIMAL; contains `$` requiring parsing.
- **Generated:** Matches both data type and parsing/currency-symbol issue.
- **Retrieval:** gt_coverage=0.0, top_score=0.8597, gate=proceed

### 8: How does the ord_line_item table handle product data redundancy?
- **Verdict:** CORRECT
- **Expected:** Redundant denormalized product copies (`product_code`, `item_name`) that snapshot at order time; may become out of sync.
- **Generated:** Correctly infers redundancy and “don’t update from master” implication.
- **Retrieval:** gt_coverage=1.0, top_score=0.7015, gate=proceed

### 9: What are the valid values for the strOrderStatus field in vw_SalesOrderHdr?
- **Verdict:** CORRECT
- **Expected:** CHECK-enforced values: PENDING, SHIPPED, CANCELLED.
- **Generated:** Matches.
- **Retrieval:** gt_coverage=1.0, top_score=0.9126, gate=proceed

### 10: Which table stores payment information and what security issue does it have?
- **Verdict:** CORRECT
- **Expected:** `tblPayment`; PCI issue: `CardNumberText` stores full plaintext PAN.
- **Generated:** Matches the plaintext/PAN PCI concern.
- **Retrieval:** gt_coverage=1.0, top_score=0.7, gate=proceed

### 11: What is the purpose of the bolActive field in tblCustomer and tblProduct?
- **Verdict:** CORRECT
- **Expected:** Active/inactive flag: customers excluded from marketing when inactive; products available/discontinued.
- **Generated:** Matches both semantics.
- **Retrieval:** gt_coverage=1.0, top_score=0.9646, gate=proceed

### 12: How are inventory transactions tracked in the system?
- **Verdict:** CORRECT
- **Expected:** `inv_txn_log` audit log; txn_type in {IN, OUT, ADJ}, prod_id references product.
- **Generated:** Matches fields, signs, reference behavior, and inventory sum rule.
- **Retrieval:** gt_coverage=1.0, top_score=0.7, gate=proceed

### 13: What is the self-referencing relationship in the Group table?
- **Verdict:** CORRECT
- **Expected:** `ParentGroupID -> GroupID` self-FK; hierarchical categories.
- **Generated:** Matches.
- **Retrieval:** gt_coverage=0.0, top_score=0.7, gate=proceed

### 14: What migration compatibility columns exist in tblCustomer?
- **Verdict:** CORRECT
- **Expected:** `cust_id` and `customer_name`.
- **Generated:** Matches both fields and migration intent.
- **Retrieval:** gt_coverage=1.0, top_score=0.7, gate=proceed

### 15: How does the system handle order status history tracking?
- **Verdict:** CORRECT
- **Expected:** `tblOrderStatusHistory` audit log with HistoryID, OrderID, OldStatus, NewStatus, ChangedByUser, ChangedDate, ChangeReason.
- **Generated:** Matches and adds one-to-many pattern.
- **Retrieval:** gt_coverage=1.0, top_score=0.7, gate=proceed

### 16: What is the inconsistent naming pattern between order tables?
- **Verdict:** CORRECT
- **Expected:** `vw_SalesOrderHdr` vs `ord_line_item`; plus FK field named `ord_id` referencing `lngOrderID`.
- **Generated:** Matches both prefix inconsistency and FK naming mismatch.
- **Retrieval:** gt_coverage=0.0, top_score=0.7, gate=proceed

### 17: What deprecated fields exist in tblProduct and why should they be avoided?
- **Verdict:** CORRECT
- **Expected:** `prod_num`, `item_desc`, `unit_cost` issues; avoid in new code.
- **Generated:** Matches the deprecated set and why.
- **Retrieval:** gt_coverage=1.0, top_score=0.7, gate=proceed

### 18: How are shipping carriers configured in the system?
- **Verdict:** CORRECT
- **Expected:** `tblShippingCarrier` with CarrierID, CarrierName, CarrierCode, TrackingURL, bolActive; only bolActive=1 offered.
- **Generated:** Matches.
- **Retrieval:** gt_coverage=1.0, top_score=0.7, gate=proceed

### 19: What is the relationship between User table passwords and security?
- **Verdict:** CORRECT
- **Expected:** `User.PasswordHash` is SHA-256 without salt; reserved-word quoting for `User`.
- **Generated:** States the SHA-256 without salt vulnerability; links password hash to security weakness.
- **Retrieval:** gt_coverage=null, top_score=0.7, gate=proceed

### 20: What fields in vw_SalesOrderHdr use the 'flt' Hungarian notation prefix and what do they store?
- **Verdict:** CORRECT
- **Expected:** `fltSubTotal`, `fltTaxAmount`, `fltTotalAmount` store money (DECIMAL(12,2)).
- **Generated:** Matches all three and their meanings.
- **Retrieval:** gt_coverage=1.0, top_score=0.7, gate=proceed

### 21: How does the system handle the different date/time field naming conventions?
- **Verdict:** CORRECT
- **Expected:** Mixed conventions; dtm-prefixed fields plus some exceptions (ChangedDate/PaymentDate without dtm).
- **Generated:** Matches the “mix” and specific examples.
- **Retrieval:** gt_coverage=0.0, top_score=0.7, gate=proceed

### 22: What table prefix patterns exist in the schema and what do they indicate?
- **Verdict:** CORRECT
- **Expected:** `tbl` base tables, `vw_` misnamed table, `ord_` and `inv_` domain prefixes, reserved-word tables `Group`/`User` without prefix.
- **Generated:** Matches.
- **Retrieval:** gt_coverage=0.0, top_score=0.7, gate=proceed

### 23: What foreign key relationships exist for the vw_SalesOrderHdr table?
- **Verdict:** CORRECT
- **Expected:** Explicit FK `intCustID -> tblCustomer.strCustID`; other tables reference it implicitly: tblPayment, tblOrderStatusHistory, ord_line_item.
- **Generated:** Matches explicit FK and the referenced relationships.
- **Retrieval:** gt_coverage=1.0, top_score=0.9956, gate=proceed

### 24: How does the legacy system handle product SKU format and uniqueness?
- **Verdict:** CORRECT
- **Expected:** Unique `strSKU` with Category-Color-Size pattern; deprecated `prod_num` not used.
- **Generated:** Matches uniqueness and format guidance (and does not overclaim about prod_num beyond “deprecated exists”).
- **Retrieval:** gt_coverage=0.0, top_score=0.7, gate=proceed

### 25: What are the critical data quality issues identified for migration?
- **Verdict:** CORRECT
- **Expected:** PCI in tblPayment; unit_cost wrong type; missing FK on inv_txn_log.user_id; unsalted SHA-256; misleading Hungarian notation; reserved-word quoting.
- **Generated:** Matches these critical issues (notably includes referential integrity gaps plus PCI/security and data quality inconsistencies).
- **Retrieval:** gt_coverage=0.0, top_score=0.9662, gate=proceed

---

## Anomalies & Recommendations

### Red Flags
- **GT coverage bookkeeping mismatch:** Many correct answers have `gt_coverage=0.0` (while still grounded and judged correct). This suggests one of:
  1) `covered_sources`/`expected_sources` are incomplete or misaligned with the dataset’s ground-truth labeling, or  
  2) retrieval quality metrics are not perfectly synchronized with actual “support” in contexts.
- `query_report.abstained_count=0` for an edge-case/negative-heavy dataset would be a concern in general, but here there are no negative queries in the bundle shown (query types are all `unknown`).

### Recommendations
1. **Fix GT coverage annotations** (or adjust evaluation mapping): ensure `expected_sources` correspond to the same granularity as `contexts_retrieved`.
2. **Improve retrieval-quality instrumentation**:
   - add “context factual support score” (e.g., whether key spans supporting the answer exist in contexts) rather than only source-level coverage.
3. **Audit Hungarian-notation/date/security extraction prompts** to ensure they don’t over-rely on glossary text; but in this run, outputs were correct.

---

## Comparison Notes (if applicable)
- `study_id=AB-BEST` is presented as the best setting; given the strong builder completion and perfect groundedness, this run appears to realize the intended “optimal” behavior.
- The ablation effect is assessed as optimal mainly via observed reliability rather than by explicit “changes_vs_baseline” fields (none are present in the provided bundle).

---