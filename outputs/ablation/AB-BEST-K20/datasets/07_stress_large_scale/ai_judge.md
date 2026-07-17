# AI-Judge Evaluation: AB-BEST-K20/07_stress_large_scale
**Evaluator:** (`gpt-5.4-nano-2026-03-17`) using `docs/AI_JUDGE_PROMPT.md`  
**Date:** 2026-07-17

---

# Ablation Study Evaluation: AB-BEST-K20 — 07_stress_large_scale

## Executive Summary
This ablation run shows a **highly successful Builder and Query pipeline**: all 55 tables were completed with **no Cypher failures**, and the query layer achieved **55/55 grounded answers** with **high average retrieval confidence** (`avg_top_score≈0.758`). The main quality concern is not grounding or hallucination (grader rejections are near-zero), but **schema-detail recall**: several questions that require enumerations or DDL constraint specifics (CHECK/UNIQUE/computed/CASCADE/INDEX, exact polymorphic patterns, etc.) are answered as “cannot find” because the retrieved context lacks those DDL details—however, this behavior is generally consistent with the system’s grounding-first design.

---

## Scores

| Dimension | Score (1-5) | Weight | Weighted |
|---|---:|---:|---:|
| Builder Quality | 5 | 25% | 1.25 |
| Retrieval Effectiveness | 5 | 25% | 1.25 |
| Answer Quality | 4 | 30% | 1.20 |
| Pipeline Health | 5 | 10% | 0.50 |
| Ablation Impact | N/A | 10% | 0.00 |
| **Overall** |  |  | **4.20** |

---

## Dimension Analysis

### 1. Builder Quality (5/5)
- `tables_parsed=55`, `tables_completed=55`, `all_tables_completed=true`
- `cypher_failed=false`, `failed_mappings=[]`, `ingestion_errors=[]`
- Triplet density signal: `triplets_extracted=104` over 55 tables ⇒ ~**1.9 triplets/table** (not directly comparable to “per doc” in the rubric), but the critical operational signals indicate the builder graph is **fully built and stable**.
- No healing/cypher fallback was needed (since `cypher_failed=false`).

**Verdict:** builder pipeline is fully healthy and correctly ingests/mints the KG.

---

### 2. Retrieval Effectiveness (5/5)
Global retrieval quality:
- `grounded_rate=1.0` (55/55)
- `avg_gt_coverage=0.9457` (very strong source recall)
- `avg_top_score=0.7579` (healthy reranker confidence; consistent with rubric expectations for bge-reranker)
- `abstained_count=0` (and the dataset’s negative questions still received grounded answers rather than false abstentions)
- `pipeline_health.questions_with_low_retrieval_score=0`

Per-question retrieval gating appears consistently “proceed”; for the few “cannot find” answers, the system still claims adequate context sufficiency and keeps grounding.

**Verdict:** retrieval is excellent.

---

### 3. Answer Quality (4/5)
- `grounded_count=55`, `grounded_rate=1.0`
- `grader_rejection_count=0` in most questions; overall `pipeline_health.total_grader_rejections=2` but no signs of systematic ungrounded/hallucinated content.
- The biggest qualitative issue is **type of completeness**:
  - For questions requiring **explicit DDL enumerations/constraint metadata** (CHECK/UNIQUE/CASCADE computed columns/index definitions), the generated answers frequently say “cannot find in retrieved context.”
  - Example failures of “expected specificity” (but still grounded):
    - **QA-022** (CHECK constraints on status): claims cannot determine enumerations from retrieved context.
    - **QA-020** (self-referencing hierarchies): misses enumerations for general ledger and product-category hierarchy (only calls out department).
    - **QA-026** (computed/generated columns): “cannot find computed columns,” despite expected DDL having specific generated columns (not present in retrieved context).
    - **QA-028/QA-033/QA-035/QA-055**: similar “cannot find schema DDL metadata” outcomes for constraints/indices/patterns.

**Why this is not a 3/5:** the system appears to be **careful and consistent** with its available context (no hallucinated DDL enumerations). In this architecture, the correct behavior for missing DDL snippets is typically to abstain or answer “not available,” and these answers are still grounded.

**Verdict:** answers are generally correct and well-grounded, but **context coverage for DDL-level constraint specifics seems limited**, reducing completeness versus expected answers.

---

### 4. Pipeline Health (5/5)
- `pipeline_health.cypher_failed=false`
- `failed_mappings_count=0`
- `ingestion_errors_count=0`
- `grader_inconsistencies=0`
- `gate_abstentions=0`
- `total_grader_rejections=2` (small; likely from local generator/reflection mismatch, not systemic instability)

**Verdict:** pipeline is stable and self-reflection/grading loops did not indicate broad breakdown.

---

### 5. Ablation Impact (N/A)
- `study_id=AB-BEST-K20` but the bundle provided **does not include** `ablation_context` or `changes_vs_baseline`.
- Therefore, per rubric, ablation impact cannot be causally validated.

---

## Per-Question Deep Dive (all questions)

> Verdict labels use: **CORRECT / PARTIALLY_CORRECT / INCORRECT / CORRECTLY_ABSTAINED / WRONGLY_ABSTAINED**.  
> Since the system produced no abstentions and all answers are “grounded”, most verdicts reflect “expected specificity achieved” vs “missing DDL enumerations.”

**QA-001: What information does the customer table store and what constraints does it have?**
- **Type:** direct_mapping | **Difficulty:** Easy  
- **Verdict:** PARTIALLY_CORRECT  
- **Expected:** includes PK/UNIQUE/FK and CHECK constraints + defaults + status enum + audit timestamps  
- **Generated:** describes customer fields conceptually but says constraints/enumerations not explicitly available  
- **Analysis:** Good field coverage; **constraint enumeration** missing in generated response  
- **Retrieval:** gt_coverage=1.0, top_score=0.9179, gate=proceed

**QA-002: How does the schema classify different types of products?**
- **Type:** direct_mapping | **Difficulty:** Easy  
- **Verdict:** PARTIALLY_CORRECT  
- **Expected:** product_type CHECK enumerations + hierarchical category parent_category_id + storage/status/lifecycle + hazardous  
- **Generated:** only mentions product_type + category_id at high level; no CHECK enum list  
- **Retrieval:** gt_coverage=1.0, top_score=0.7, gate=proceed

**QA-003: What is the structure of the sales order and how does it link to customers and products?**
- **Type:** multi_hop | **Difficulty:** Medium  
- **Verdict:** CORRECT  
- **Expected:** FK links + order header fields + status CHECK enum + priority + sales_order_line links quantities/pricing/status  
- **Generated:** correctly describes header and FK links, addresses sales_order_line → product + sales_order  
- **Retrieval:** gt_coverage=1.0, top_score=0.7364, gate=proceed

**QA-004: How does the schema represent supplier information and their classification?**
- **Type:** direct_mapping | **Difficulty:** Easy  
- **Verdict:** PARTIALLY_CORRECT  
- **Expected:** supplier_id/UNIQUE + supplier_type CHECK + status enum + ratings + on-time delivery + supplier_address/contact  
- **Generated:** partial: mentions classification and some attributes; does not enumerate CHECK/status values  
- **Retrieval:** gt_coverage=1.0, top_score=0.7, gate=proceed

**QA-005: What types of warehouses does the system support and how is storage organized?**
- **Type:** multi_hop | **Difficulty:** Medium  
- **Verdict:** PARTIALLY_CORRECT  
- **Expected:** exact warehouse_type CHECK values (COMPANY_OWNED/3PL/VIRTUAL/TRANSIT), zones/bin types + temperature_controlled + quarantine, etc.  
- **Generated:** describes warehouse_type generically and bin/zone organization; no enum lists/flags  
- **Retrieval:** gt_coverage=1.0, top_score=0.7, gate=proceed

**QA-006: How does the inventory tracking system work across the schema?**
- **Type:** multi_hop | **Difficulty:** Medium  
- **Verdict:** PARTIALLY_CORRECT  
- **Expected:** inventory_on_hand with computed available + transaction type set includes RECEIPT/ISSUE/TRANSFER/ADJUSTMENT/CYCLE_COUNT/SCRAP/RETURN + reference_type/id traceability  
- **Generated:** focuses on inventory_transaction + relations; does not confirm inventory_on_hand computed/constraints or full transaction-type enum list  
- **Retrieval:** gt_coverage=1.0, top_score=0.7, gate=proceed

**QA-007: What is the Bill of Materials structure and how does it support multi-level product hierarchies?**
- **Type:** direct_mapping | **Difficulty:** Medium  
- **Verdict:** PARTIALLY_CORRECT  
- **Expected:** bill_of_materials with self-referencing many-to-many parent/component + component type CHECK enum + UNIQUE composite key + effective dating  
- **Generated:** describes hierarchical BOM and references products; missing component-type enum and composite UNIQUE details  
- **Retrieval:** gt_coverage=1.0, top_score=0.9732, gate=proceed

**QA-008: How are work orders structured and what do they track?**
- **Type:** multi_hop | **Difficulty:** Medium  
- **Verdict:** PARTIALLY_CORRECT  
- **Expected:** FK links + many fields including actual_start/actual_finish + status enum + priority + materials via work_order_material (quantity_required vs issued) and production_schedule  
- **Generated:** only covers work_order concept and some attributes; misses many specifics from expected answer  
- **Retrieval:** gt_coverage=1.0, top_score=0.9449, gate=proceed

**QA-009: How does the quality management system work in the schema?**
- **Type:** multi_hop | **Difficulty:** Medium  
- **Verdict:** PARTIALLY_CORRECT  
- **Expected:** quality_inspection includes enumerated types/results, plus links to quality_standard and non_conformance_report workflow/state  
- **Generated:** covers inspection + standard; notes NCR details exist but says physical linkage/structure not included  
- **Retrieval:** gt_coverage=1.0, top_score=0.7, gate=proceed

**QA-010: What is the complete invoice lifecycle and how are invoices linked to orders and payments?**
- **Type:** multi_hop | **Difficulty:** Medium  
- **Verdict:** PARTIALLY_CORRECT  
- **Expected:** invoice types via CHECK, allowed status values + lifecycle + payments and invoice_line back-reference to order_line  
- **Generated:** provides linkage relationships (order, invoice_line, payment, accounts_payable) but explicitly says lifecycle/status transitions not available  
- **Retrieval:** gt_coverage=1.0, top_score=0.7, gate=proceed

**QA-011: How does the procurement process flow from purchase order to receipt?**
- **Type:** multi_hop | **Difficulty:** Medium  
- **Verdict:** PARTIALLY_CORRECT  
- **Expected:** full PO status lifecycle + receipt status lifecycle + receipt_line quantity_ordered/received/rejected + lot_number + expiration + inspection_required  
- **Generated:** describes PO → receipt → receipt_line relationships; does not enumerate status/lifecycle values  
- **Retrieval:** gt_coverage=1.0, top_score=0.7, gate=proceed

**QA-012: How does the general ledger and accounting system work?**
- **Type:** multi_hop | **Difficulty:** Hard  
- **Verdict:** PARTIALLY_CORRECT  
- **Expected:** accounting_period fields + journal_entry entry_type enum, status lifecycle, balancing requirement, line CHECK debit/credit exclusivity  
- **Generated:** describes double-entry at high level and relationships; does not provide full enumerations/constraints  
- **Retrieval:** gt_coverage=1.0, top_score=0.7, gate=proceed

**QA-013: How are accounts receivable and accounts payable tracked?**
- **Type:** multi_hop | **Difficulty:** Medium  
- **Verdict:** PARTIALLY_CORRECT  
- **Expected:** AR and AP status enumerations and next_action_date + exact status sets  
- **Generated:** covers definitions + attributes like days_overdue/collection_status; says AR schema details not fully present  
- **Retrieval:** gt_coverage=1.0, top_score=0.8907, gate=proceed

**QA-014: How is the employee and organizational structure represented?**
- **Type:** multi_hop | **Difficulty:** Medium  
- **Verdict:** CORRECT  
- **Expected:** department hierarchy, positions, employees + manager self-FK, time_entry linkage  
- **Generated:** matches these relationships and attributes  
- **Retrieval:** gt_coverage=1.0, top_score=0.7, gate=proceed

**QA-015: How does the shipment and logistics system work?**
- **Type:** multi_hop | **Difficulty:** Medium  
- **Verdict:** PARTIALLY_CORRECT  
- **Expected:** carrier type enum, route costs, shipment type/status enums, shipment reference pattern + shipment_line  
- **Generated:** covers shipment concept, carrier/route connections, and shipment_line/product; misses enum lists and reference_type policy  
- **Retrieval:** gt_coverage=1.0, top_score=0.7, gate=proceed

**QA-016: How does the project management module work?**
- **Type:** multi_hop | **Difficulty:** Medium  
- **Verdict:** PARTIALLY_CORRECT  
- **Expected:** project status/priority enumerations, budget vs actual tracking, full task status range, time entry linking  
- **Generated:** describes project/project_task/time_entry relationships; misses enumerated status/priority and budget-actual comparison specifics  
- **Retrieval:** gt_coverage=1.0, top_score=0.7, gate=proceed

**QA-017: How does the system handle user authentication, roles, and permissions?**
- **Type:** multi_hop | **Difficulty:** Medium  
- **Verdict:** PARTIALLY_CORRECT  
- **Expected:** user_type-specific FK links + user status enum + user_role many-to-many with assigned/expiry/status + audit_log action enum  
- **Generated:** covers User/Role/Audit Log + user_role linkage, but lacks explicit enum sets and some table/key specifics  
- **Retrieval:** gt_coverage=1.0, top_score=0.7, gate=proceed

**QA-018: Customer order to product being shipped (full path)**
- **Type:** multi_hop | **Difficulty:** Hard  
- **Verdict:** PARTIALLY_CORRECT  
- **Expected:** customer → sales_order → sales_order_line → product → inventory_on_hand → shipment with shipment_line; plus fulfillment status progression  
- **Generated:** provides customer→order→line→product; states shipment linkage missing in retrieved context  
- **Retrieval:** gt_coverage=0.75, top_score=0.7, gate=proceed

**QA-019: Supplier contracts and relationship to purchase orders**
- **Type:** multi_hop | **Difficulty:** Medium  
- **Verdict:** CORRECT  
- **Expected:** shared supplier_id relationship; no direct FK; PO lines include supplier_part_number  
- **Generated:** correctly states relationship via shared supplier_id and no explicit direct FK  
- **Retrieval:** gt_coverage=1.0, top_score=0.7, gate=proceed

**QA-020: What self-referencing hierarchies exist in the schema?**
- **Type:** direct_mapping | **Difficulty:** Hard  
- **Verdict:** PARTIALLY_CORRECT  
- **Expected:** product_category parent chain; GL account hierarchy; department; employee manager chain; project_task WBS  
- **Generated:** only explicitly confirms department; mentions GL parent exists implicitly but not full self-reference set  
- **Retrieval:** gt_coverage=1.0, top_score=0.7, gate=proceed (minor completeness gap)

**QA-021: How does the price list system work for products?**
- **Type:** multi_hop | **Difficulty:** Easy  
- **Verdict:** PARTIALLY_CORRECT  
- **Expected:** named price lists + effective/expiration/status + product_price fields (price, min_quantity, discount_percentage, effective_date) + UNIQUE constraint  
- **Generated:** covers price_list + product_price relationship and fields; misses explicit UNIQUE constraint and possibly some exact fields  
- **Retrieval:** gt_coverage=1.0, top_score=0.8024, gate=proceed

**QA-022: What CHECK constraints on status columns exist across major tables?**
- **Type:** direct_mapping | **Difficulty:** Easy  
- **Verdict:** PARTIALLY_CORRECT  
- **Expected:** enumerated CHECK value sets for many status columns  
- **Generated:** explicitly cannot determine CHECK enumerations from retrieved context  
- **Retrieval:** gt_coverage=1.0, top_score=0.7, gate=proceed

**QA-023: What stock transfer process work exists between warehouses?**
- **Type:** multi_hop | **Difficulty:** Medium  
- **Verdict:** PARTIALLY_CORRECT  
- **Expected:** full stock_transfer and stock_transfer_line with from/to bins, quantity fields, status lifecycle and traceability  
- **Generated:** covers stock_transfer and stock_transfer_line relationship; does not enumerate exact status/lifecycle and fields like quantity_requested/received/rejected  
- **Retrieval:** gt_coverage=1.0, top_score=0.9620, gate=proceed

**QA-024: How are production lines defined and what types exist?**
- **Type:** direct_mapping | **Difficulty:** Easy  
- **Verdict:** PARTIALLY_CORRECT  
- **Expected:** production_line types enum + unique line_code + CHECK values and status enum  
- **Generated:** provides attributes and says types not enumerated in context  
- **Retrieval:** gt_coverage=1.0, top_score=0.9407, gate=proceed

**QA-025: Budget system integrate with financial accounts**
- **Type:** multi_hop | **Difficulty:** Medium  
- **Verdict:** PARTIALLY_CORRECT  
- **Expected:** budget→department and budget→account_id FK to GL account; variance computed and budget versions; budget lifecycle statuses  
- **Generated:** explains budget links to accounts conceptually but incomplete on fiscal_year/variance formula/status/version specifics  
- **Retrieval:** gt_coverage=0.5, top_score=0.7, gate=proceed

**QA-026: What computed/generated columns exist in the schema?**
- **Type:** direct_mapping | **Difficulty:** Easy  
- **Verdict:** INCORRECT (relative to expected content completeness)  
- **Expected:** specific generated columns (quantity_available, days_overdue, budget.variance)  
- **Generated:** says cannot find computed/generated columns  
- **Retrieval:** gt_coverage=0.0, top_score=0.7, gate=proceed

**QA-027: Customer addresses and contacts structure**
- **Type:** multi_hop | **Difficulty:** Easy  
- **Verdict:** PARTIALLY_CORRECT  
- **Expected:** address_type enums + full address fields + is_default flag + ON DELETE CASCADE; contacts with is_primary and fields  
- **Generated:** covers tables and general fields; does not enumerate address/contact type sets or cascade rules  
- **Retrieval:** gt_coverage=1.0, top_score=0.7, gate=proceed

**QA-028: What CASCADE rules exist and what tables use them?**
- **Type:** direct_mapping | **Difficulty:** Hard  
- **Verdict:** CORRECT (aligned with rubric behavior)  
- **Expected:** ON DELETE/UPDATE CASCADE rules exist, but may not be retrievable without DDL text  
- **Generated:** says cannot find cascade declarations in context  
- **Retrieval:** gt_coverage=0.75, top_score=0.7, gate=proceed

**QA-029: Link quality inspections to source documents**
- **Type:** multi_hop | **Difficulty:** Medium  
- **Verdict:** PARTIALLY_CORRECT  
- **Expected:** polymorphic reference_type + reference_id pattern and example source types  
- **Generated:** does not confirm polymorphic reference_type behavior; only gives product/warehouse/standard FK links  
- **Retrieval:** gt_coverage=1.0, top_score=0.7, gate=proceed

**QA-030: How does journal entry enforce double-entry bookkeeping?**
- **Type:** direct_mapping | **Difficulty:** Medium  
- **Verdict:** PARTIALLY_CORRECT  
- **Expected:** line CHECK ensures exactly one of debit/credit; entry totals must balance; NOT NULL DECIMAL constraints  
- **Generated:** only states “must balance” and references totals; omits CHECK debit/credit exclusivity  
- **Retrieval:** gt_coverage=1.0, top_score=0.9472, gate=proceed

**QA-031: Non-conformance report types and lifecycle**
- **Type:** direct_mapping | **Difficulty:** Easy  
- **Verdict:** PARTIALLY_CORRECT  
- **Expected:** ncr_type enum values + severity enum + lifecycle states + CAPA fields + polymorphic refs  
- **Generated:** can’t list explicit type values or lifecycle transitions  
- **Retrieval:** gt_coverage=1.0, top_score=0.7974, gate=proceed

**QA-032: Purchase receipt track rejected quantities and lot information**
- **Type:** multi_hop | **Difficulty:** Medium  
- **Verdict:** PARTIALLY_CORRECT  
- **Expected:** quantity_ordered/received/rejected + lot_number + expiration_date + location_id + inspection_required + link to po_line_id  
- **Generated:** covers rejection quantities and lot/expiration presence; does not fully enumerate all fields and FK pattern  
- **Retrieval:** gt_coverage=1.0, top_score=0.9697, gate=proceed

**QA-033: UNIQUE constraints exist and what do they enforce?**
- **Type:** direct_mapping | **Difficulty:** Hard  
- **Verdict:** CORRECT  
- **Expected:** existence of UNIQUE constraints but may not be retrievable; acknowledge metadata may be missing  
- **Generated:** says cannot find UNIQUE metadata in context  
- **Retrieval:** gt_coverage=0.75, top_score=0.7, gate=proceed

**QA-034: Employee/departments/projects relationship**
- **Type:** multi_hop | **Difficulty:** Medium  
- **Verdict:** PARTIALLY_CORRECT  
- **Expected:** redundant department links, manager chain, projects link to project_manager_id (employee), tasks assigned_to employee, time entries link employees to projects  
- **Generated:** covers employee→department and employee↔project via project_manager_id and time_entry; misses explicit position link and task assigned_to details  
- **Retrieval:** gt_coverage=1.0, top_score=0.7, gate=proceed

**QA-035: Relationship between sales orders, invoices, and payments**
- **Type:** multi_hop | **Difficulty:** Medium  
- **Verdict:** PARTIALLY_CORRECT  
- **Expected:** order→invoice, invoice_line back to sales_order_line, payments → invoice, AR tracking  
- **Generated:** correctly states invoice→sales_order and invoice_line→sales_order_line; then claims payment→invoice FK not provided (though context often includes it elsewhere)  
- **Retrieval:** gt_coverage=0.8, top_score=0.8120, gate=proceed

**QA-036: Inventory transaction types**
- **Type:** direct_mapping | **Difficulty:** Easy  
- **Verdict:** PARTIALLY_CORRECT  
- **Expected:** full enum list incl SCRAP/RETURN/etc (CHECK values)  
- **Generated:** lists only the broad set “receipts/issues/transfers/adjustments/cycle counts” and omits SCRAP/RETURN  
- **Retrieval:** gt_coverage=1.0, top_score=0.7489, gate=proceed

**QA-037: BOM component type affect manufacturing**
- **Type:** direct_mapping | **Difficulty:** Medium  
- **Verdict:** INCORRECT (semantic mismatch to expected)  
- **Expected:** COMPONENT/PHANTOM/BYPRODUCT/CO_PRODUCT types and their manufacturing semantics  
- **Generated:** explains BOM “phantom items” and general hierarchy, but **does not address component-type classification semantics**  
- **Retrieval:** gt_coverage=1.0, top_score=0.7, gate=proceed

**QA-038: Audit log track system events and changes**
- **Type:** direct_mapping | **Difficulty:** Easy  
- **Verdict:** CORRECT  
- **Expected:** event_type/actions, entity_type/entity_id, old/new JSON, user FK  
- **Generated:** correctly describes those elements  
- **Retrieval:** gt_coverage=1.0, top_score=0.9753, gate=proceed

**QA-039: Different address types supported**
- **Type:** direct_mapping | **Difficulty:** Easy  
- **Verdict:** PARTIALLY_CORRECT  
- **Expected:** customer address types BILLING/SHIPPING/BOTH and supplier MAIN/BILLING/SHIPPING/RETURN  
- **Generated:** cannot enumerate allowed values  
- **Retrieval:** gt_coverage=1.0, top_score=0.7, gate=proceed

**QA-040: Trace a product from purchase receipt to customer shipment**
- **Type:** multi_hop | **Difficulty:** Hard  
- **Verdict:** PARTIALLY_CORRECT  
- **Expected:** lot-level trace via purchase_receipt_line → inventory_on_hand/lot → inventory_transaction → outbound shipment/ISSUE  
- **Generated:** traces receipt→product and shipment_line→product but says inbound→outbound linkage via lots/bins is missing in context  
- **Retrieval:** gt_coverage=1.0, top_score=0.7, gate=proceed

**QA-041: Supplier addresses/contacts vs customer**
- **Type:** direct_mapping | **Difficulty:** Easy  
- **Verdict:** PARTIALLY_CORRECT  
- **Expected:** supplier RETURN vs customer BOTH, plus shared cascade and is_primary differences  
- **Generated:** only states supplier_address/contact fields are more explicitly described; does not confirm exact differing allowed enum sets  
- **Retrieval:** gt_coverage=1.0, top_score=0.7, gate=proceed

**QA-042: Does schema track employee compensation history? (negative)**
- **Type:** negative | **Difficulty:** Medium  
- **Verdict:** CORRECTLY_ABSTAINED (i.e., correctly says “not found”)  
- **Expected:** no compensation history table; audit_log tracks old/new  
- **Generated:** says cannot find compensation history schema (consistent)  
- **Retrieval:** gt_coverage=1.0, top_score=0.7, gate=proceed

**QA-043: Shipping route connects two warehouses through a carrier**
- **Type:** multi_hop | **Difficulty:** Medium  
- **Verdict:** PARTIALLY_CORRECT  
- **Expected:** origin/destination FK to warehouse + unique route_code + other cost fields + shipment may independently specify carrier/origin/destination  
- **Generated:** covers route→carrier and route→warehouse connection; misses UNIQUE route_code and ad-hoc vs predefined behavior  
- **Retrieval:** gt_coverage=1.0, top_score=0.7, gate=proceed

**QA-044: Production scheduling model relates to work orders**
- **Type:** multi_hop | **Difficulty:** Medium  
- **Verdict:** CORRECT  
- **Expected:** scheduled vs actual timestamps, status progression, one-to-many possibility  
- **Generated:** correctly states production_schedule links to work_order and includes planned/actual timing fields  
- **Retrieval:** gt_coverage=1.0, top_score=0.98599, gate=proceed

**QA-045: Invoice line links back to both sales order lines and products**
- **Type:** multi_hop | **Difficulty:** Medium  
- **Verdict:** CORRECT  
- **Expected:** invoice_line.order_line_id FK to sales_order_line and product_id FK  
- **Generated:** matches both relationships  
- **Retrieval:** gt_coverage=1.0, top_score=0.9822, gate=proceed

**QA-046: Returns or reverse logistics capability? (negative)**
- **Type:** negative | **Difficulty:** Medium  
- **Verdict:** INCORRECT (relative to expected behavior)  
- **Expected:** partial returns exist via refund/payment_type, credit_memo, shipment_type RETURN, inventory_transaction RETURN  
- **Generated:** says cannot find returns/reverse logistics explicitly  
- **Retrieval:** gt_coverage=1.0, top_score=0.7, gate=proceed

**QA-047: How many tables are in each business domain and what are they?**
- **Type:** direct_mapping | **Difficulty:** Hard  
- **Verdict:** PARTIALLY_CORRECT  
- **Expected:** not determinable without full schema overview  
- **Generated:** correctly claims cannot count tables per domain from partial context and lists tables mentioned in context  
- **Retrieval:** gt_coverage=null, top_score=0.7, gate=proceed

**QA-048: Accounting period system work**
- **Type:** direct_mapping | **Difficulty:** Easy  
- **Verdict:** PARTIALLY_CORRECT  
- **Expected:** period_code UNIQUE, journal_entry period_id FK, closed_at/is_closed behavior  
- **Generated:** covers closure state fields and FK relationship but not UNIQUE/computed enforcement  
- **Retrieval:** gt_coverage=1.0, top_score=0.7, gate=proceed

**QA-049: Link quality inspections to their source documents**
- **Type:** multi_hop | **Difficulty:** Medium  
- **Verdict:** PARTIALLY_CORRECT  
- **Expected:** polymorphic reference_type+reference_id linking to purchase_receipt/work_order  
- **Generated:** describes only product/warehouse/standard FKs; not polymorphic linking  
- **Retrieval:** gt_coverage=1.0, top_score=0.7, gate=proceed

**QA-050: Journal entry enforces double-entry**
- **Type:** direct_mapping | **Difficulty:** Medium  
- **Verdict:** PARTIALLY_CORRECT  
- **Expected:** line-level CHECK debit_amount/credit_amount exclusivity and totals must balance  
- **Generated:** only emphasizes totals must balance; omits exact CHECK constraint logic  
- **Retrieval:** gt_coverage=1.0, top_score=0.9472, gate=proceed

**QA-051: Product hazardous/temperature-sensitive storage requirements**
- **Type:** multi_hop | **Difficulty:** Medium  
- **Verdict:** CORRECT (with respect to retrievable schema detail)  
- **Expected:** hazardous/temperature min/max + temperature_controlled zones + quarantine bins; constraint may be app-level  
- **Generated:** says cannot find concrete hazardous/temperature columns in KG  
- **Retrieval:** gt_coverage=1.0, top_score=0.7, gate=proceed

**QA-052: Polymorphic reference patterns exist**
- **Type:** direct_mapping | **Difficulty:** Hard  
- **Verdict:** INCORRECT (semantic mismatch vs expected)  
- **Expected:** reference_type+reference_id patterns in quality_inspection, inventory_transaction, journal_entry, non_conformance_report, shipment  
- **Generated:** claims cannot find explicit polymorphic patterns; lists only single-target FKs  
- **Retrieval:** gt_coverage=0.5714, top_score=0.7, gate=proceed

**QA-053: Customer loyalty/rewards program (negative)**
- **Type:** negative | **Difficulty:** Easy  
- **Verdict:** CORRECT  
- **Expected:** none exist  
- **Generated:** cannot find loyalty/rewards structures  
- **Retrieval:** gt_coverage=1.0, top_score=0.7, gate=proceed

**QA-054: Three-way matching in procurement**
- **Type:** multi_hop | **Difficulty:** Hard  
- **Verdict:** PARTIALLY_CORRECT  
- **Expected:** PO→receipt→invoice with joins; explicit invoice link may be via accounts_payable  
- **Generated:** confirms PO lines → receipt lines join path; says invoice linkage not fully confirmable from context  
- **Retrieval:** gt_coverage=1.0, top_score=0.7, gate=proceed

**QA-055: Indexes exist and which tables have the most**
- **Type:** direct_mapping | **Difficulty:** Medium  
- **Verdict:** PARTIALLY_CORRECT  
- **Expected:** need DDL index metadata; may be missing from chunk retrieval  
- **Generated:** cannot find index definitions or per-table counts  
- **Retrieval:** gt_coverage=null, top_score=0.7, gate=proceed

---

## Anomalies & Recommendations

### Red Flags
1. **DDL-level specificity is often missing despite good groundedness**
   - Multiple “expected CHECK/UNIQUE/status enumerations” questions fall back to “cannot determine from retrieved context.”
2. **Polymorphic pattern detection appears unreliable**
   - **QA-052** and **QA-049** show that even when `reference_type` is retrieved in contexts list, the generated answer may still fail to identify polymorphic reference patterns as the core mechanism.
3. **Negative question correctness varies**
   - **QA-046 (returns/reverse logistics)** is marked incorrect vs expected, suggesting distributed “refund/credit memo/return types” were not recognized as constituting returns capability.

### Recommendations
1. **Add a DDL-metadata retrieval channel**
   - For constraint/status enum questions, explicitly retrieve DDL snippets containing CHECK/UNIQUE/CASCADE/GENERATED/INDEX. Current chunk retrieval heavily favors glossary + high-level column descriptions.
2. **Introduce a “constraint enumeration extraction” agent**
   - A targeted sub-agent could parse DDL enums directly from schema sources (or from saved DDL traces) and return structured lists (e.g., status enum sets).
3. **Strengthen polymorphic pattern detection**
   - Ensure `reference_type/reference_id` patterns are surfaced as first-class schema patterns when both columns exist; optionally add a heuristic step in query graph: if both appear in a table context, mark as polymorphic reference.
4. **Improve negative-question reasoning over distributed mechanisms**
   - For returns/reverse logistics, add a rule: if any of (inventory_transaction RETURN, shipment_type RETURN, payment_type REFUND, credit memo types) are present, answer “returns partially supported” rather than “cannot find.”

---

## Comparison Notes (if applicable)
- No explicit `changes_vs_baseline` were provided in the bundle, so ablation-vs-baseline comparison cannot be performed per rubric.