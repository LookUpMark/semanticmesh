# AI-Judge Evaluation: AB-BEST/06_edgecases_legacy
**Evaluator:** (`gpt-5.4-nano-2026-03-17`) using `docs/AI_JUDGE_PROMPT.md`  
**Date:** 2026-07-17

---

# Ablation Study Evaluation: AB-BEST — 06_edgecases_legacy

## Executive Summary
AB-BEST shows an overall healthy **end-to-end** migration pipeline run: all 10/10 tables were completed with **no Cypher failures** or ingestion errors, and **every question was grounded** (grounded_rate = 1.0) with **no abstentions**. The main concern is **retrieval effectiveness nuance**: some questions have **gt_coverage = 0.0** and multiple queries show **lower retrieval_quality_score (≈0.7 with raw ≈0.55)**, suggesting the system can still answer correctly, but sometimes relies on non-exact context matches rather than retrieving the exact ground-truth sources.

## Scores

| Dimension | Score (1-5) | Weight | Weighted |
|---|---:|---:|---:|
| Builder Quality | 5 | 25% | 1.25 |
| Retrieval Effectiveness | 3 | 25% | 0.75 |
| Answer Quality | 5 | 30% | 1.50 |
| Pipeline Health | 5 | 10% | 0.50 |
| Ablation Impact | N/A | 10% | 0.00 |
| **Overall** |  |  | **4.00** |

## Dimension Analysis

### 1. Builder Quality (5/5)
- `tables_parsed=10`, `tables_completed=10`, `all_tables_completed=true`
- `cypher_failed=false`, `failed_mappings=[]`, `ingestion_errors=[]`
- Triplet extraction looks healthy for migration semantics: `triplets_extracted=154`, `entities_resolved=145` (no sign of catastrophic ER).
**Meets score-5 criteria**: all tables completed + no Cypher/mapping/ingestion failures.

### 2. Retrieval Effectiveness (3/5)
Key signals:
- `query_report.avg_gt_coverage = 0.6302` (below the rubric’s 0.6 threshold for score-4 but not terrible; still indicates partial GT-source retrieval).
- `query_report.avg_top_score = 0.7949` which is **very high**, indicating the reranker is confident on the top results.
- However, there are **clear per-question retrieval misses**:
  - `query_id 4`: `gt_coverage=0.0`, raw retrieval quality 0.55
  - `query_id 6`: `gt_coverage=0.0`, raw 0.55
  - `query_id 7`: `gt_coverage=0.0`, raw ≈0.66–0.68? (shows `gt_coverage=0.0`)
  - `query_id 13`: `gt_coverage=0.0`, raw ≈0.68
  - `query_id 14`: `gt_coverage=0.0`, raw 0.66…
  - `query_id 15`: `gt_coverage=0.0`, raw 0.55
  - `query_id 16`: `gt_coverage=0.0`, raw 0.55
  - `query_id 17`: `gt_coverage=0.0`, raw 0.66…
  - `query_id 18`: `gt_coverage=0.0`, raw 0.55
  - `query_id 19`: `gt_coverage=null`
  - `query_id 20`: `gt_coverage=0.0`, raw 0.55
  - `query_id 21`: `gt_coverage=0.0`, raw 0.55
  - `query_id 22`: `gt_coverage=0.125`
  - `query_id 24`: `gt_coverage=0.0`, raw 0.55
  - `query_id 25`: `gt_coverage=0.0`, raw 0.55

Despite those, the system still answers correctly—so this run likely benefits from **broad context matches** or **non-GT-but-equivalent** chunks. That’s exactly why the rubric separates retrieval from answer quality: retrieval is not consistently hitting GT sources even when answers are correct.

**Result:** meets “partial retrieval” behavior → 3/5.

### 3. Answer Quality (5/5)
- `query_report.grounded_rate = 1.0` with `grader_rejection_count = 0` for almost all questions (only pipeline health shows 1 total rejection; see below).
- All generated answers are semantically aligned with expected answers across the shown set.
- Negative/abstention behavior: none needed; `abstained_count=0` and no evidence of fabrications.

**Result:** score-5 behavior (fully grounded + semantically correct), even if some answers use non-GT sources.

### 4. Pipeline Health (5/5)
- `pipeline_health.cypher_failed=false`
- `ingestion_errors_count=0`
- `grader_inconsistencies=0`, `gate_abstentions=0`
- `total_grader_rejections=1` but per-question `grader_rejection_count` is mostly 0 and `grader_consistency_valid=true`.
Overall, no evidence of instability or unrecovered failures.

**Result:** 5/5.

### 5. Ablation Impact (N/A)
This bundle is `study_id=AB-BEST`, but the provided JSON does **not** include an `ablation_context` or “changes_vs_baseline” to compare against AB-00. Therefore, ablation impact cannot be causally assessed per rubric.

---

## Dimension 3: Answer Quality (Per-question highlights)

**Best-case examples (clearly correct + direct mapping):**
- **Q1** (tblCustomer purpose): Correctly captures master-data purpose and includes migration compatibility fields present in context.
- **Q3** (vw_SalesOrderHdr primary key): Correct (`lngOrderID`, INT/PK).
- **Q10** (tblPayment security issue): Correctly states plaintext PAN in `CardNumberText`.

**Worst retrieval cases still answered correctly (shows decoupling between GT coverage and correctness):**
- **Q4** (reserved word table names): `gt_coverage=0.0` but answer is correct: `Group` and `User` with quoting requirement.
- **Q6** (inventory transaction naming convention): `gt_coverage=0.0` but answer correctly identifies `inv_txn_log` and abbreviated fields.
- **Q16** (inconsistent naming pattern): `gt_coverage=0.0` but answer accurately describes prefix inconsistencies and FK naming (`ord_id` → `lngOrderID`).

**Conclusion:** Answer quality remains excellent even when GT-source retrieval is imperfect.

---

## Per-Question Deep Dive

### 1: What is the purpose of the tblCustomer table?
- **Type:** unknown | **Difficulty:** unknown
- **Verdict:** CORRECT
- **Expected:** Customer master data; legacy + migration compatibility fields (strCustID, strFullName, strEmail, strRegion, cust_id, customer_name)
- **Generated:** Stores customer master data from legacy CRM
- **Analysis:** Correct purpose and consistent with retrieved dictionary (including migration placeholder fields in context).
- **Retrieval:** gt_coverage=1.0, top_score=0.9922, gate=proceed

### 2: How are customers identified in the legacy system?
- **Verdict:** CORRECT
- **Expected:** `strCustID` (VARCHAR50), formats like C-XXXXX / REG-XXXX, PK/unique
- **Generated:** Identified by `strCustID` PK/unique; formats match
- **Analysis:** Fully aligned.
- **Retrieval:** gt_coverage=1.0, top_score=0.8292, gate=proceed

### 3: What table stores order header information and what is its primary key?
- **Verdict:** CORRECT
- **Expected:** `vw_SalesOrderHdr` table; PK `lngOrderID` INT
- **Generated:** `vw_SalesOrderHdr`; PK `lngOrderID`
- **Analysis:** Direct match.
- **Retrieval:** gt_coverage=1.0, top_score=0.7432, gate=proceed

### 4: Which table in the schema uses a SQL reserved word as its name?
- **Verdict:** CORRECT
- **Expected:** `Group` and `User` are reserved words; must be bracket-quoted
- **Generated:** `Group` and `User` (quoted as `[Group]`, `[User]`)
- **Analysis:** Correct despite `gt_coverage=0.0` indicating GT-source retrieval mismatch.
- **Retrieval:** gt_coverage=0.0, top_score=0.7, gate=proceed

### 5: What is the relationship between vw_SalesOrderHdr and tblCustomer?
- **Verdict:** CORRECT
- **Expected:** `intCustID` → `tblCustomer.strCustID`; one customer to many orders
- **Generated:** Same FK + one-to-many
- **Analysis:** Correct.
- **Retrieval:** gt_coverage=1.0, top_score=0.9988, gate=proceed

### 6: What naming convention is used for the inventory transaction log table?
- **Verdict:** CORRECT
- **Expected:** `inv_txn_log`; abbreviated names (`txn_id`, `txn_dt`, `txn_type`, `prod_id`)
- **Generated:** Notes `inv_txn_log` and `inv_` prefix (but overall intent matches)
- **Analysis:** Semantically correct, even though GT coverage is 0.0.
- **Retrieval:** gt_coverage=0.0, top_score=0.93, gate=proceed

### 7: What data quality issue exists in the tblProduct unit_cost field?
- **Verdict:** CORRECT
- **Expected:** `unit_cost` is VARCHAR(20) not DECIMAL; contains `$19.99`-style symbols requiring parsing
- **Generated:** `unit_cost` VARCHAR(20) and contains `$`; parsing needed
- **Analysis:** Correct.
- **Retrieval:** gt_coverage=0.0, top_score=0.8597, gate=proceed

### 8: How does the ord_line_item table handle product data redundancy?
- **Verdict:** CORRECT
- **Expected:** redundant denormalized `product_code`/`item_name` snapshot; may drift from `tblProduct`
- **Generated:** Correctly infers redundancy conceptually
- **Analysis:** Correct; though one context chunk shown is about payment security, the semantic claim matches glossary known issue.
- **Retrieval:** gt_coverage=1.0, top_score=0.7015, gate=proceed

### 9: What are the valid values for the strOrderStatus field in vw_SalesOrderHdr?
- **Verdict:** CORRECT
- **Expected:** `PENDING`, `SHIPPED`, `CANCELLED` (CHECK enforced)
- **Generated:** Same set
- **Analysis:** Correct.
- **Retrieval:** gt_coverage=1.0, top_score=0.9126, gate=proceed

### 10: Which table stores payment information and what security issue does it have?
- **Verdict:** CORRECT
- **Expected:** `tblPayment`; PCI issue: plaintext full PAN in `CardNumberText`
- **Generated:** `tblpayment`; plaintext PAN noted
- **Analysis:** Correct.
- **Retrieval:** gt_coverage=1.0, top_score=0.7, gate=proceed

### 11: What is the purpose of the bolActive field in tblCustomer and tblProduct?
- **Verdict:** CORRECT
- **Expected:** Customer marketing inclusion flag; product availability/discontinued flag
- **Generated:** Correct semantics for both tables
- **Analysis:** Correct.
- **Retrieval:** gt_coverage=1.0, top_score=0.9646, gate=proceed

### 12: How are inventory transactions tracked in the system?
- **Verdict:** CORRECT
- **Expected:** `inv_txn_log`; txn_type IN/OUT/ADJ + abbreviated fields + prod_id FK
- **Generated:** Detailed explanation with signs and fields
- **Analysis:** Correct.
- **Retrieval:** gt_coverage=1.0, top_score=0.7, gate=proceed

### 13: What is the self-referencing relationship in the Group table?
- **Verdict:** CORRECT
- **Expected:** `ParentGroupID` → `GroupID` creating hierarchy; NULL is top level
- **Generated:** Same relationship
- **Analysis:** Correct though GT coverage is 0.0.
- **Retrieval:** gt_coverage=0.0, top_score=0.7, gate=proceed

### 14: What migration compatibility columns exist in tblCustomer?
- **Verdict:** CORRECT
- **Expected:** `cust_id`, `customer_name`
- **Generated:** Same columns + meaning
- **Analysis:** Correct despite retrieval score being capped style (gt_coverage=0.0).
- **Retrieval:** gt_coverage=0.0, top_score=0.7, gate=proceed

### 15: How does the system handle order status history tracking?
- **Verdict:** CORRECT
- **Expected:** `tblOrderStatusHistory` audit trail fields (OrderID, OldStatus, NewStatus, etc.)
- **Generated:** Enumerates all fields and one-to-many audit pattern
- **Analysis:** Correct.
- **Retrieval:** gt_coverage=0.0, top_score=0.7, gate=proceed

### 16: What is the inconsistent naming pattern between order tables?
- **Verdict:** CORRECT
- **Expected:** inconsistent table prefixes; FK naming mismatch `ord_id` vs `lngOrderID`
- **Generated:** Same two inconsistencies
- **Analysis:** Correct despite gt_coverage=0.0.
- **Retrieval:** gt_coverage=0.0, top_score=0.7, gate=proceed

### 17: What deprecated fields exist in tblProduct and why should they be avoided?
- **Verdict:** CORRECT
- **Expected:** `prod_num`, `item_desc`, `unit_cost` (and why avoid)
- **Generated:** Same three and rationale
- **Analysis:** Correct.
- **Retrieval:** gt_coverage=0.0, top_score=0.7, gate=proceed

### 18: How are shipping carriers configured in the system?
- **Verdict:** CORRECT
- **Expected:** `tblShippingCarrier` with CarrierID/Name/Code/TrackingURL/bolActive; only bolActive=1 offered
- **Generated:** Correct.
- **Analysis:** Correct, even with gt_coverage=0.0.
- **Retrieval:** gt_coverage=0.0, top_score=0.7, gate=proceed

### 19: What is the relationship between User table passwords and security?
- **Verdict:** CORRECT
- **Expected:** unsalted SHA-256 in `PasswordHash`; security weakness; also reserved-word table
- **Generated:** Correctly ties PasswordHash → SHA-256 without salt → vulnerability
- **Analysis:** Correct; gt_coverage is null (unscored) but semantics match.
- **Retrieval:** gt_coverage=null, top_score=0.7, gate=proceed

### 20: What fields in vw_SalesOrderHdr use the 'flt' Hungarian notation prefix and what do they store?
- **Verdict:** CORRECT
- **Expected:** fltSubTotal, fltTaxAmount, fltTotalAmount; DECIMAL money fields
- **Generated:** Same and explains DECIMAL(12,2)
- **Analysis:** Correct.
- **Retrieval:** gt_coverage=0.0, top_score=0.8799, gate=proceed

### 21: How does the schema handle the different date/time field naming conventions?
- **Verdict:** CORRECT
- **Expected:** dtm-prefixed fields for datetime; exceptions in User table (LastLogin, CreatedDate)
- **Generated:** Correctly describes dtm-prefixed fields and non-prefixed audit fields; mentions mixing due to inconsistency
- **Analysis:** Correct.
- **Retrieval:** gt_coverage=0.0, top_score=0.7, gate=proceed

### 22: What table prefix patterns exist in the schema and what do they indicate?
- **Verdict:** CORRECT
- **Expected:** prefixes: `tbl`, misnamed `vw_`, `ord_`, `inv_`, and no-prefix reserved words `Group`, `User`
- **Generated:** Correctly enumerates patterns and what they indicate
- **Analysis:** Correct.
- **Retrieval:** gt_coverage=0.125, top_score=0.7, gate=proceed

### 23: What foreign key relationships exist for the vw_SalesOrderHdr table?
- **Verdict:** CORRECT
- **Expected:** explicit FK `intCustID → tblCustomer.strCustID`; plus relationships where other tables reference `vw_SalesOrderHdr.lngOrderID`
- **Generated:** Correctly lists tblPayment, ord_line_item, and the inbound FK to tblCustomer
- **Analysis:** Correct.
- **Retrieval:** gt_coverage=1.0, top_score=0.9956, gate=proceed

### 24: How does the legacy system handle product SKU format and uniqueness?
- **Verdict:** CORRECT
- **Expected:** unique `strSKU`, format Category-Color-Size; deprecated `prod_num` avoided
- **Generated:** Correctly states uniqueness + format; doesn’t over-claim about denormalized product_code usage
- **Analysis:** Still correct relative to key facts.
- **Retrieval:** gt_coverage=0.0, top_score=0.7, gate=proceed

### 25: What are the critical data quality issues identified for migration?
- **Verdict:** CORRECT
- **Expected:** PCI issue, unit_cost type issue, missing inv_txn_log FK, unsalted SHA-256, misleading intCustID type, reserved-word tables quoting
- **Generated:** Mostly matches expected; includes referential integrity gaps too and performance issues in addition
- **Analysis:** Semantically correct; extra issues are not penalized.
- **Retrieval:** gt_coverage=0.0, top_score=0.9662, gate=proceed

---

## Anomalies & Recommendations

### Red Flags
1. **Many questions have `gt_coverage=0.0` while still producing correct grounded answers.**
   - This indicates GT-source labels may be overly strict, or retrieval is finding *equivalent* context but not the labeled GT chunk(s).
2. **Some retrieval scores are capped by pool confidence / adjusted behavior**:
   - Several questions show `retrieval_quality_score_raw=0.55` with adjusted/forced score 0.7 and `pool_confidence_applied=true`.

### Recommendations
1. **Audit GT source alignment strategy**: ensure GT chunk attribution matches how contexts are actually stored/merged (parent vs child chunks, schema expansion, synonyms).
2. **Add a secondary metric for “semantic GT coverage”**: instead of exact GT chunk overlap, compute whether retrieved contexts contain the expected facts (already approximated by grounding/semantic correctness).
3. **Investigate why specific tables/sections yield gt_coverage=0** (e.g., `Group/User`, date/time naming, SKU/deprecated fields). Likely caused by:
   - different chunk naming granularity,
   - glossary migration notes being used instead of exact schema chunks,
   - retrieval pulling “Migration Priority Guidelines / Legacy System Quirks” rather than field-level dictionary sections.
4. **Keep hallucination grader enabled** (it looks stable here); consider tightening retrieval quality gating thresholds only for cases where grounded_rate drops (not observed in this run).

## Comparison Notes (if applicable)
- No baseline (AB-00) changes were provided in the bundle, so direct ablation-vs-baseline comparison is not possible.