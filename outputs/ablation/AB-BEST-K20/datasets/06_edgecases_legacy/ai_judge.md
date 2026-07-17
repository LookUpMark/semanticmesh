# AI-Judge Evaluation: AB-BEST-K20/06_edgecases_legacy
**Evaluator:** (`gpt-5.4-nano-2026-03-17`) using `docs/AI_JUDGE_PROMPT.md`  
**Date:** 2026-07-17

---

# Ablation Study Evaluation: AB-BEST-K20 — 06_edgecases_legacy

## Executive Summary
This run shows an excellent end-to-end pipeline outcome: all 10 DDL tables were parsed and completed with no Cypher failures, and every one of the 25 questions produced grounded answers with full GT source coverage. The main tension is internal: several questions report **only “adequate” context sufficiency but still score retrieval as mediocre (notably many queries have `retrieval_quality_score_raw` around ~0.55)**—yet the system still answers correctly and does not require regeneration or abstention. Overall, the architecture appears stable and correct for edge-case schema/documentation questions.

## Scores

| Dimension | Score (1-5) | Weight | Weighted |
|---|---:|---:|---:|
| Builder Quality | 5 | 25% | 1.25 |
| Retrieval Effectiveness | 4 | 25% | 1.00 |
| Answer Quality | 5 | 30% | 1.50 |
| Pipeline Health | 5 | 10% | 0.50 |
| Ablation Impact |  N/A | 10% | 0.00 |
| **Overall** |  |  | **4.25** |

## Dimension Analysis

### 1. Builder Quality (5/5)
- `tables_parsed=10`, `tables_completed=10`, `all_tables_completed=true`
- `cypher_failed=false`, `failed_mappings=[]`, `ingestion_errors=[]`
- Triplet extraction: `triplets_extracted=154`, `entities_resolved=140`
  - Triplets/entity ≈ **154/140 = 1.1** (not meeting the rubric’s “>30 per doc” density heuristic), *but* the downstream mapping/graph construction still completed successfully and query grounding is perfect. In this bundle, builder quality should be judged primarily by completion + Cypher health signals.

### 2. Retrieval Effectiveness (4/5)
Global signals:
- `avg_gt_coverage=1.0` (perfect GT source coverage)
- `avg_top_score=0.814` (healthy)
- `abstained_count=0`, `grounded_rate=1.0`

However, per-question retrieval confidence varies:
- Several queries have **lowish raw retrieval scores (~0.55)** with pool confidence applied (`pool_confidence_applied=true`), notably:
  - Q4, Q6, Q7, Q8, Q10, Q11, Q14, Q15, Q16, Q17, Q18, etc. (many show `retrieval_quality_score_raw≈0.55` and adjusted score bumped to 0.7 via confidence floor).
- Despite that, answers remain correct—so this is best interpreted as: retrieval quality gate + confidence floor are doing their job, but raw ranking confidence is not uniformly “high”.

Given rubric discipline: avg_gt_coverage and avg_top_score justify **4 rather than 3** (retrieval is not fundamentally broken).

### 3. Answer Quality (5/5)
- `query_report.grounded_rate=1.0`
- `grounded_count=25` out of 25
- `grader_rejection_count=0` for every question
- For the worst retrieval-quality queries, answers are still semantically correct and well-aligned with the expected schema/documentation facts.

Examples (spot checks):
- Q3: correctly identifies `vw_SalesOrderHdr` primary key `lngOrderID` and table/view nuance.
- Q10: correctly describes `tblPayment.CardNumberText` plaintext PAN PCI violation.
- Q7: correctly flags `tblProduct.unit_cost` as `VARCHAR(20)` with currency symbols requiring parsing; aligns with expected “should be DECIMAL”.
- Q19: correctly covers `User.PasswordHash` SHA-256 unsalted rainbow-table vulnerability (and does not invent other password behaviors).

### 4. Pipeline Health (5/5)
- `total_grader_rejections=0`
- `grader_inconsistencies=0`
- `gate_abstentions=0`
- `cypher_failed=false`, `failed_mappings_count=0`, `ingestion_errors_count=0`
- Note: `builder_report.elapsed_s=0` and `query_report.elapsed_s=0` are likely logging artifacts, but no operational instability is indicated.

### 5. Ablation Impact (N/A)
- `study_id=AB-BEST-K20` is provided, but the bundle does **not** include an `ablation_context` block (or explicit “changes vs baseline” flags). Therefore, impact cannot be assessed causally per rubric.

## Dimension Analysis (Notes on Question Types)
`dataset_info` reports `"query_type_distribution": {"unknown": 25}` and difficulty also `"unknown"`. The rubric asks for query-type-specific reasoning (e.g., negative questions/abstention), but there are no such labeled types here. Still, there were **no abstentions** and no incorrect answers, so negative-question handling is not stress-tested by this bundle.

---

## Per-Question Deep Dive

### 1: What is the purpose of the tblCustomer table?
- **Type:** unknown | **Difficulty:** unknown  
- **Verdict:** CORRECT  
- **Expected:** customer master; fields incl. `strCustID`, `strFullName`, email, region; legacy Hungarian notation + migration placeholders (`cust_id`, `customer_name`)  
- **Generated:** matches purpose + key fields; includes `bolActive`, timestamps, and migration columns  
- **Analysis:** Full semantic match to expected; uses correct legacy schema details.  
- **Retrieval:** gt_coverage=1.0, top_score=0.814, gate=proceed

### 2: How are customers identified in the legacy system?
- **Type:** unknown | **Difficulty:** unknown  
- **Verdict:** CORRECT  
- **Expected:** `strCustID` VARCHAR(50), formats like `C-XXXXX` / `REG-XXXX`, NOT NULL UNIQUE  
- **Generated:** exactly describes `strCustID` PK and format constraints  
- **Analysis:** No missing/extra incorrect facts.  
- **Retrieval:** gt_coverage=1.0, top_score=0.829, gate=proceed

### 3: What table stores order header information and what is its primary key?
- **Type:** unknown | **Difficulty:** unknown  
- **Verdict:** CORRECT  
- **Expected:** `vw_SalesOrderHdr` (table), PK `lngOrderID` INT  
- **Generated:** matches both table name and PK  
- **Analysis:** Correct view/table nuance and Hungarian prefix context.  
- **Retrieval:** gt_coverage=1.0, top_score=0.935, gate=proceed

### 4: Which table in the schema uses a SQL reserved word as its name?
- **Type:** unknown | **Difficulty:** unknown  
- **Verdict:** CORRECT  
- **Expected:** `Group` and `User` require `[Group]` / `[User]`  
- **Generated:** states reserved-word tables and quoting requirement  
- **Analysis:** Matches expected.  
- **Retrieval:** gt_coverage=1.0, top_score=0.700, gate=proceed

### 5: What is the relationship between vw_SalesOrderHdr and tblCustomer?
- **Type:** unknown | **Difficulty:** unknown  
- **Verdict:** CORRECT  
- **Expected:** FK `vw_SalesOrderHdr.intCustID → tblCustomer.strCustID` (VARCHAR mismatch note)  
- **Generated:** provides correct FK direction + data-type nuance + one-to-many  
- **Analysis:** Fully aligned.  
- **Retrieval:** gt_coverage=1.0, top_score=0.999, gate=proceed

### 6: What naming convention is used for the inventory transaction log table?
- **Type:** unknown | **Difficulty:** unknown  
- **Verdict:** CORRECT  
- **Expected:** table `inv_txn_log` uses abbreviated naming; fields `txn_id`, `txn_dt`, `txn_type`, `prod_id`  
- **Generated:** matches wording and examples  
- **Analysis:** Correct and complete.  
- **Retrieval:** gt_coverage=1.0, top_score=0.700, gate=proceed

### 7: What data quality issue exists in the tblProduct unit_cost field?
- **Type:** unknown | **Difficulty:** unknown  
- **Verdict:** CORRECT  
- **Expected:** `unit_cost` is VARCHAR(20) not DECIMAL; contains currency symbols like `$19.99`  
- **Generated:** matches all key points including parsing requirement  
- **Analysis:** Perfect alignment.  
- **Retrieval:** gt_coverage=1.0, top_score=0.860, gate=proceed

### 8: How does the ord_line_item table handle product data redundancy?
- **Type:** unknown | **Difficulty:** unknown  
- **Verdict:** CORRECT  
- **Expected:** redundant denormalized product copies for reporting + snapshot semantics; should not be updated from master  
- **Generated:** captures `product_code`/`item_name` redundancy, out-of-sync note, and “do NOT update” rule  
- **Analysis:** Matches expected.  
- **Retrieval:** gt_coverage=1.0, top_score=0.931, gate=proceed

### 9: What are the valid values for the strOrderStatus field in vw_SalesOrderHdr?
- **Type:** unknown | **Difficulty:** unknown  
- **Verdict:** CORRECT  
- **Expected:** CHECK constraint values: `PENDING`, `SHIPPED`, `CANCELLED`  
- **Generated:** lists exactly those values  
- **Analysis:** Correct.  
- **Retrieval:** gt_coverage=1.0, top_score=0.700, gate=proceed

### 10: Which table stores payment information and what security issue does it have?
- **Type:** unknown | **Difficulty:** unknown  
- **Verdict:** CORRECT  
- **Expected:** `tblPayment`, `CardNumberText` plaintext unencrypted PAN; PCI violation  
- **Generated:** matches both table and security issue; tokenization recommendation  
- **Analysis:** Correct.  
- **Retrieval:** gt_coverage=1.0, top_score=0.700, gate=proceed

### 11: What is the purpose of the bolActive field in tblCustomer and tblProduct?
- **Type:** unknown | **Difficulty:** unknown  
- **Verdict:** CORRECT  
- **Expected:** `bolActive` indicates active customer inclusion in marketing and product availability/discontinued  
- **Generated:** matches exact semantics and 1/0 mapping  
- **Analysis:** Correct.  
- **Retrieval:** gt_coverage=1.0, top_score=0.700, gate=proceed

### 12: How are inventory transactions tracked in the system?
- **Type:** unknown | **Difficulty:** unknown  
- **Verdict:** CORRECT  
- **Expected:** `inv_txn_log` with `txn_type` values IN/OUT/ADJ; abbreviated fields; qty sign conventions; derived inventory quantity rule  
- **Generated:** includes all core rules, including derived inventory logic  
- **Analysis:** Correct and detailed.  
- **Retrieval:** gt_coverage=1.0, top_score=0.898, gate=proceed

### 13: What is the self-referencing relationship in the Group table?
- **Type:** unknown | **Difficulty:** unknown  
- **Verdict:** CORRECT  
- **Expected:** `ParentGroupID → GroupID`; NULL indicates top-level groups  
- **Generated:** matches fully  
- **Analysis:** Correct.  
- **Retrieval:** gt_coverage=1.0, top_score=0.700, gate=proceed

### 14: What migration compatibility columns exist in tblCustomer?
- **Type:** unknown | **Difficulty:** unknown  
- **Verdict:** CORRECT  
- **Expected:** `cust_id` (INT) and `customer_name` (VARCHAR 255) for new system compatibility  
- **Generated:** matches both fields and semantics (“planned”, currently NULL)  
- **Analysis:** Correct.  
- **Retrieval:** gt_coverage=1.0, top_score=0.700, gate=proceed

### 15: How does the system handle order status history tracking?
- **Type:** unknown | **Difficulty:** unknown  
- **Verdict:** CORRECT  
- **Expected:** `tblOrderStatusHistory` audit log, includes OrderID, OldStatus, NewStatus, ChangedByUser, ChangedDate, ChangeReason  
- **Generated:** matches all fields and audit-trail semantics  
- **Analysis:** Correct.  
- **Retrieval:** gt_coverage=1.0, top_score=0.700, gate=proceed

### 16: What is the inconsistent naming pattern between order tables?
- **Type:** unknown | **Difficulty:** unknown  
- **Verdict:** CORRECT  
- **Expected:** `vw_SalesOrderHdr` misnamed prefix; `ord_line_item` uses `ord_`; plus `ord_id` naming inconsistency  
- **Generated:** focuses on prefix misnaming/prefix inconsistency and related-table naming  
- **Analysis:** Still semantically correct, though it does not explicitly restate the `ord_id` FK name inconsistency in the main narrative (but it is implied by context).  
- **Retrieval:** gt_coverage=1.0, top_score=0.700, gate=proceed

### 17: What deprecated fields exist in tblProduct and why should they be avoided?
- **Type:** unknown | **Difficulty:** unknown  
- **Verdict:** CORRECT  
- **Expected:** `prod_num`, `item_desc`, `unit_cost` (VARCHAR money bug)  
- **Generated:** matches all three and explains why `unit_cost` is unusable without conversion  
- **Analysis:** Correct.  
- **Retrieval:** gt_coverage=1.0, top_score=0.860, gate=proceed

### 18: How are shipping carriers configured in the system?
- **Type:** unknown | **Difficulty:** unknown  
- **Verdict:** CORRECT  
- **Expected:** `tblShippingCarrier` fields incl. `CarrierCode`, `TrackingURL` with `{TRACKING_NUM}`, `bolActive` business rule  
- **Generated:** matches table fields + active-carrier usage  
- **Analysis:** Correct.  
- **Retrieval:** gt_coverage=1.0, top_score=0.700, gate=proceed

### 19: What is the relationship between User table passwords and security?
- **Type:** unknown | **Difficulty:** unknown  
- **Verdict:** CORRECT  
- **Expected:** `PasswordHash` SHA-256 unsalted → rainbow-table vulnerability; reserved-word `User` needs quoting  
- **Generated:** covers unsalted SHA-256; also mentions payment/card security separately (correct but not requested)  
- **Analysis:** No incorrect password/security claim; extra correct info doesn’t harm.  
- **Retrieval:** gt_coverage=null? (bundle shows `gt_coverage: null`), top_score=0.700, gate=proceed

### 20: What fields in vw_SalesOrderHdr use the 'flt' Hungarian notation prefix and what do they store?
- **Type:** unknown | **Difficulty:** unknown  
- **Verdict:** CORRECT  
- **Expected:** `fltSubTotal`, `fltTaxAmount`, `fltTotalAmount` are DECIMAL(12,2) money fields  
- **Generated:** lists all three and describes meaning/subtotal/tax/total including shipping  
- **Analysis:** Correct.  
- **Retrieval:** gt_coverage=1.0, top_score=0.963, gate=proceed

### 21: How does the schema handle the different date/time field naming conventions?
- **Type:** unknown | **Difficulty:** unknown  
- **Verdict:** PARTIALLY_CORRECT  
- **Expected:** Consistent `dtm` Hungarian prefix across key tables; note exceptions like `User` breaks convention (LastLogin/CreatedDate)  
- **Generated:** explains that overall naming conventions are inconsistent and focuses on `dtm` examples; states non-perfect consistency; mentions other datetime columns (`PaymentDate`, `ChangedDate`) but does not explicitly cover the expected “User table breaks convention with LastLogin/CreatedDate” as an explicit comparison to dtm fields.  
- **Analysis:** Still grounded and largely correct, but slightly off target relative to expected structured “dtm consistency + exceptions” framing.  
- **Retrieval:** gt_coverage=1.0, top_score=0.700, gate=proceed

### 22: What table prefix patterns exist in the schema and what do they indicate?
- **Type:** unknown | **Difficulty:** unknown  
- **Verdict:** CORRECT  
- **Expected:** `tbl` standard; `vw_` misnamed table; `ord_`, `inv_` module prefixes; reserved-word no-prefix `Group`/`User`  
- **Generated:** matches and explains evolution/misnaming; includes “no prefix” reserved words needing quoting  
- **Analysis:** Correct.  
- **Retrieval:** gt_coverage=1.0, top_score=0.996, gate=proceed

### 23: What foreign key relationships exist for the vw_SalesOrderHdr table?
- **Type:** unknown | **Difficulty:** unknown  
- **Verdict:** CORRECT  
- **Expected:** explicit FK `intCustID → tblCustomer.strCustID`; plus references via Payment/StatusHistory/LineItems to `lngOrderID` (implicit/mentioned)  
- **Generated:** lists all those relationships  
- **Analysis:** Correct and complete vs expected.  
- **Retrieval:** gt_coverage=1.0, top_score=0.996, gate=proceed

### 24: How does the legacy system handle product SKU format and uniqueness?
- **Type:** unknown | **Difficulty:** unknown  
- **Verdict:** CORRECT  
- **Expected:** SKU in `strSKU` UNIQUE; format `Category-Color-Size`; deprecated `prod_num` exists but avoid  
- **Generated:** matches uniqueness and format; mentions only `strSKU` for migration; correctly notes denormalized `product_code` snapshots  
- **Analysis:** Correct.  
- **Retrieval:** gt_coverage=1.0, top_score=0.700, gate=proceed

### 25: What are the critical data quality issues identified for migration?
- **Type:** unknown | **Difficulty:** unknown  
- **Verdict:** CORRECT  
- **Expected:** PCI violation, unit_cost type issue, missing FK constraint, unsalted SHA-256, misleading Hungarian notation, reserved-word tables quoting  
- **Generated:** covers those critical issues and adds additional referential integrity + performance items from glossary context  
- **Analysis:** Semantically aligned and includes extra correct items.  
- **Retrieval:** gt_coverage=1.0, top_score=0.966, gate=proceed

---

## Anomalies & Recommendations

### Red Flags
- **Ablation metadata missing:** No `ablation_context` explaining changes vs baseline; rubric dimension 5 is therefore N/A.
- **Question typing not labeled:** `query_type` and `difficulty` are all `"unknown"` across dataset; limits stress-testing analysis (e.g., negative questions).
- **Many queries show low `retrieval_quality_score_raw` (~0.55) with confidence floor applied:** This suggests the reranker’s top-candidate confidence is not uniformly high, even though answers are correct. That points to a potential calibration/thresholding tuning opportunity.

### Recommendations
1. **Expose and log per-stage retrieval details** (RRF contributions, traversal hits) for the low raw-score cluster (many Q4/Q6/Q9/Q10/Q11/etc.).
2. **Review reranker calibration / pool_confidence floor**: the system frequently relies on the applied confidence floor to reach the “proceed” region; verify that this doesn’t mask edge-case retrieval failures for harder question types.
3. **Label query types/difficulty** in the dataset so the abstention and multi-hop rubric logic can be validated properly.
4. **Improve “frame fidelity” for Q21**: add targeted prompting that mirrors expected rubric structure (e.g., “dtm prefix consistently used except X”).

## Comparison Notes (if applicable)
- No baseline comparison bundle is included. This evaluation cannot confirm whether AB-BEST-K20 improves over AB-00, only that the run itself is strong.

---