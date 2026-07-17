# AI-Judge Evaluation: AB-BEST/07_stress_large_scale
**Evaluator:** (`gpt-5.4-nano-2026-03-17`) using `docs/AI_JUDGE_PROMPT.md`  
**Date:** 2026-07-17

---

# Ablation Study Evaluation: AB-BEST — 07_stress_large_scale

## Executive Summary
This run shows **excellent end-to-end architecture health**: all **55/55 tables completed**, **no Cypher failures**, and **no pipeline errors/rejections**. Query-side performance is also strong (**grounded_rate=1.0**, **avg_gt_coverage≈0.85**, **avg_top_score≈0.74**), with most answers correctly reflecting what the KG exposes.  

However, there are several **semantic-mismatch cases** where the model **incorrectly abstains** on questions that are largely answerable from the expected schema details (or fails to include requested enumerations/constraints), despite retrieval quality being reported as adequate.

## Scores

| Dimension | Score (1-5) | Weight | Weighted |
|---|---:|---:|---:|
| Builder Quality | 5 | 25% | 1.25 |
| Retrieval Effectiveness | 5 | 25% | 1.25 |
| Answer Quality | 4 | 30% | 1.20 |
| Pipeline Health | 5 | 10% | 0.50 |
| Ablation Impact | N/A | 10% | N/A |
| **Overall** |  |  | **4.20** |

## Dimension Analysis

### 1. Builder Quality (5/5)
- `tables_parsed=55`, `tables_completed=55`, `all_tables_completed=true`
- `cypher_failed=false`, `failed_mappings=[]`, `ingestion_errors=[]`
- Triplet extraction appears healthy: `triplets_extracted=111`, `entities_resolved=84` (no strong sign of under/over extraction; ER not clearly pathological).
**Verdict:** Builder graph construction is fully successful with no recovery needed.

### 2. Retrieval Effectiveness (5/5)
- `query_report.grounded_count=55`, `grounded_rate=1.0`
- `avg_gt_coverage=0.8503` (high)
- `avg_top_score=0.7416` (strong reranker confidence for bge-reranker-v2-m3)
- `abstained_count=0` and `gate_abstentions=0` — no false abstentions.
- `questions_with_low_retrieval_score=0` in `pipeline_health`
**Verdict:** Retrieval is very effective and consistent with the ground-truth sources being retrieved.

### 3. Answer Quality (4/5)
Overall grounding is perfect, but there are **noticeable “missing required specifics” / “wrong abstain” / “doesn’t answer requested structure”** behaviors on some questions:

Key observation:
- Several answers say **“cannot find in KG”** even when `gt_coverage=1.0` and contexts include relevant schema pieces (e.g., QA-015, QA-022, QA-026, QA-028, QA-029, QA-040, QA-041 variants, QA-050/QA-054/QA-055 where question expects constraints/enumerations).
- Some multi-hop questions correctly explain linkages but omit requested **enum values, CHECK constraints, or polymorphic mechanics** that the expected answers include.

**Best examples (strong correctness/completeness):**
- QA-007, QA-008? (Several show coherent structure descriptions)
- QA-012 handles GL “how it works” by admitting insufficiency; that is aligned with context limitations.

**Worst examples (semantic incompleteness / mis-handled “what should be present”):**
- QA-022 (CHECK constraints across tables): ground-truth coverage is extremely low (`gt_coverage=0.1818`) but the system *still* proceeds; it abstains textually though it should have either extracted constraints or clearly matched which constraints were present.  
- QA-028 (CASCADE rules): model answers “cannot find” with `gt_coverage=0.0` but still marked grounded and proceeded; this appears to be a mismatch between expected and actual retrieval evidence or evaluation labeling.
- QA-026 (computed/generated columns): expected has 3 computed columns, but model says cannot find; `gt_coverage=0.3333` suggests some retrieval existed but answer omitted specifics.
- QA-050 (multi-currency negative): expected says **no exchange rate table**, multi-currency supported at document level; model answers “Yes” but its rationale is off-target (it overstates evidence and ignores the exchange-rate absence requirement). Still grounded, but semantically misaligned with the “negative” framing.

### 4. Pipeline Health (5/5)
- `total_grader_rejections=0`
- `grader_inconsistencies=0`
- `gate_abstentions=0`
- `cypher_failed=false`, `failed_mappings_count=0`, `ingestion_errors_count=0`
**Verdict:** No stability issues; self-check loops did not need to intervene.

### 5. Ablation Impact (N/A)
- Study id is **AB-BEST**, but the bundle does not include an explicit `ablation_context` or a baseline (`AB-00`) diff in the provided JSON.
- Therefore causal “impact vs baseline” cannot be validated per rubric.

---

## Per-Question Deep Dive

### QA-001: What information does the customer table store and what constraints does it have?
- **Type:** direct_mapping | **Difficulty:** Easy
- **Verdict:** PARTIALLY_CORRECT
- **Expected:** PK customer_id; UNIQUE customer_number; FK customer_type_id; CHECK status values; defaults; CHECK credit_score 0-100; timestamps.
- **Generated:** Correct high-level attributes exist; **claims contexts do not provide explicit constraints** and lists only a few columns as evidence.
- **Analysis:** Good semantic coverage of what the table stores, but **fails the constraint enumeration** expected.
- **Retrieval:** gt_coverage=1.0, top_score=0.8968, gate=proceed

### QA-002: How does the schema classify different types of products?
- **Type:** direct_mapping | **Difficulty:** Easy
- **Verdict:** PARTIALLY_CORRECT
- **Expected:** CHECK enum product_type values; product_category hierarchy incl parent_category_id; other attributes (hazardous, temperature, shelf life).
- **Generated:** Mentions product_type classification via glossary; does not enumerate CHECK values or hierarchy details explicitly.
- **Retrieval:** gt_coverage=1.0, top_score=0.7000, gate=proceed

### QA-003: What is the structure of the sales order and how does it link to customers and products?
- **Type:** multi_hop | **Difficulty:** Medium
- **Verdict:** PARTIALLY_CORRECT
- **Expected:** Explicit FKs: sales_order.customer_id → customer; sales_order.warehouse_id; CHECK status lifecycle; sales_order_line.product_id → product; line qty/pricing/status fields.
- **Generated:** Correctly describes tables and attributes; **does not provide explicit join key details**.
- **Retrieval:** gt_coverage=1.0, top_score=0.7000, gate=proceed

### QA-004: How does the schema represent supplier information and their classification?
- **Type:** direct_mapping | **Difficulty:** Easy
- **Verdict:** PARTIALLY_CORRECT
- **Expected:** supplier_type CHECK enum values; supplier_number UNIQUE; status enum; performance metrics (credit_rating, lead_time_days, quality_rating, on_time_delivery_rate); address/contact tables.
- **Generated:** Mentions supplier_type, credit_rating/lead_time/quality_rating; **misses exact enum sets and many fields**.
- **Retrieval:** gt_coverage=1.0, top_score=0.7000, gate=proceed

### QA-005: What types of warehouses does the system support and how is storage organized?
- **Type:** multi_hop | **Difficulty:** Medium
- **Verdict:** PARTIALLY_CORRECT
- **Expected:** warehouse_type CHECK enum list; zones and bin types enums; temperature_controlled; bin status enum.
- **Generated:** Explains warehouse_type conceptually + bin location organization; **does not enumerate enum values / flags / unique-per-warehouse codes**.
- **Retrieval:** gt_coverage=1.0, top_score=0.7000, gate=proceed

### QA-006: How does the inventory tracking system work across the schema?
- **Type:** multi_hop | **Difficulty:** Medium
- **Verdict:** PARTIALLY_CORRECT
- **Expected:** inventory_on_hand with unique and computed quantity_available; inventory_transaction transaction_type enum list; source document ref pattern.
- **Generated:** Focuses mainly on inventory_transaction; **omits inventory_on_hand + computed quantity_available** and detailed transaction_type list.
- **Retrieval:** gt_coverage=1.0, top_score=0.7000, gate=proceed

### QA-007: BOM structure and multi-level product hierarchies
- **Type:** direct_mapping | **Difficulty:** Medium
- **Verdict:** CORRECT
- **Expected:** self-referencing parent/component via quantities & UOM; component_type enums; effective dates; unique composite.
- **Generated:** Explains BOM hierarchy and multi-level traversal; mentions scrap and effective date range/type broadly.
- **Retrieval:** gt_coverage=1.0, top_score=0.9732, gate=proceed

### QA-008: How are work orders structured and what do they track?
- **Type:** multi_hop | **Difficulty:** Medium
- **Verdict:** PARTIALLY_CORRECT
- **Expected:** explicit FKs (product_id, production_line_id, warehouse_id), qty fields (ordered/completed/scrapped), planned vs actual timestamps, priority enums, status enums; work_order_material linking.
- **Generated:** Describes work_order attributes partially; **omits explicit join to production_line and warehouse**, and omits work_order_material behavior.
- **Retrieval:** gt_coverage=1.0, top_score=0.7000, gate=proceed

### QA-009: How does the quality management system work in the schema?
- **Type:** multi_hop | **Difficulty:** Medium
- **Verdict:** PARTIALLY_CORRECT
- **Expected:** quality_inspection with inspection types enum + result enum; defect/sample/batch; NCR lifecycle/types and CAPA fields.
- **Generated:** Covers quality_standard + quality_inspection linkage to standard/product; **does not cover NCR lifecycle/types** and overclaims about supplier linkage not present.
- **Retrieval:** gt_coverage=0.6667, top_score=0.7000, gate=proceed

### QA-010: Invoice lifecycle and linkage
- **Type:** multi_hop | **Difficulty:** Medium
- **Verdict:** PARTIALLY_CORRECT
- **Expected:** invoice_type enum, full lifecycle statuses, order link via order_id FK, payment link, invoice_line optional order_line_id.
- **Generated:** Captures linkages + some attributes (status/collection status) but explicitly says lifecycle stages are missing.
- **Retrieval:** gt_coverage=1.0, top_score=0.7000, gate=proceed

### QA-011: Procurement flow from purchase order to receipt
- **Type:** multi_hop | **Difficulty:** Medium
- **Verdict:** PARTIALLY_CORRECT
- **Expected:** PO status lifecycle; PO lines with quantity tracking; purchase_receipt statuses; receipt_line lot/expiration and join keys.
- **Generated:** Correct PO → receipt at concept level; **does not provide join key column names** and misses status enumerations.
- **Retrieval:** gt_coverage=1.0, top_score=0.7000, gate=proceed

### QA-012: General ledger and accounting system
- **Type:** multi_hop | **Difficulty:** Hard
- **Verdict:** CORRECT
- **Expected:** GL built on account_type/balance_type, hierarchical parent accounts; accounting_period fields; journal_entry balancing + line debit/credit CHECK.
- **Generated:** Admits inability to explain workflow beyond schema metadata; provides accurate retrieved concepts.
- **Retrieval:** gt_coverage=1.0, top_score=0.8891, gate=proceed

### QA-013: AR and AP tracking
- **Type:** multi_hop | **Difficulty:** Medium
- **Verdict:** PARTIALLY_CORRECT
- **Expected:** AR status/collection workflow values + computed days_overdue; AP status enum + discount/terms fields; explicit both link back to invoice.
- **Generated:** Correctly describes AR concept and AP fields; includes invoice linkage; **misses detailed enum/status sets and computed column definition**.
- **Retrieval:** gt_coverage=1.0, top_score=0.7000, gate=proceed

### QA-014: Employee & org structure
- **Type:** multi_hop | **Difficulty:** Medium
- **Verdict:** PARTIALLY_CORRECT
- **Expected:** department hierarchy, position→department, employee→department/position/manager, time_entry approval status enum, FLSA and salary ranges enums.
- **Generated:** Correctly covers department/position/manager_id; mentions termination/hourly_rate; **misses required enum sets and many specific constraints**.
- **Retrieval:** gt_coverage=1.0, top_score=0.7000, gate=proceed

### QA-015: Shipment and logistics system works
- **Type:** multi_hop | **Difficulty:** Medium
- **Verdict:** PARTIALLY_CORRECT
- **Expected:** carrier types, route fields (distance, cost_per_km), shipment type/status lifecycle, shipment_line links to product and quantities/weights, reference_type+reference_id polymorphism.
- **Generated:** Says it can’t find end-to-end workflow; describes only some relationships/fields.
- **Retrieval:** gt_coverage=1.0, top_score=0.7000, gate=proceed

### QA-016: Project management module
- **Type:** multi_hop | **Difficulty:** Medium
- **Verdict:** PARTIALLY_CORRECT
- **Expected:** project types/status/priority, tasks hierarchy assigned_to/status/completion %, time entries linking to cost, budget vs actuals.
- **Generated:** Describes project and project_task links; **omits enums and time_entry integration**.
- **Retrieval:** gt_coverage=1.0, top_score=0.7000, gate=proceed

### QA-017: Authentication, roles, permissions
- **Type:** multi_hop | **Difficulty:** Medium
- **Verdict:** PARTIALLY_CORRECT
- **Expected:** app_user user_type mapping; role types + statuses; user_role many-to-many with assigned/expiry/status; audit_log actions incl LOGIN/LOGOUT/CRUD.
- **Generated:** Covers user/role/audit log and user_role mapping; **does not confirm permission checks nor full action enum set**.
- **Retrieval:** gt_coverage=0.6667, top_score=0.7000, gate=proceed

### QA-018: Customer order to product shipped path (hard)
- **Type:** multi_hop | **Difficulty:** Hard
- **Verdict:** INCORRECT
- **Expected:** explicit traversal: customer → sales_order → sales_order_line → product; sales_order warehouse; inventory_on_hand; shipment + shipment_line; status progression; invoice/payment settlement.
- **Generated:** States context too limited to provide end-to-end join path; only partial existence of concepts.
- **Retrieval:** gt_coverage=0.75, top_score=0.7000, gate=proceed

### QA-019: Supplier contracts & relationship to purchase orders
- **Type:** multi_hop | **Difficulty:** Medium
- **Verdict:** PARTIALLY_CORRECT
- **Expected:** supplier_contract links to supplier_id; purchase orders also link to same supplier_id; compare terms via PO lines.
- **Generated:** Correct supplier_contract→supplier; correctly says no explicit contract↔PO FK, but does not fully articulate shared supplier_id and comparison idea.
- **Retrieval:** gt_coverage=1.0, top_score=0.7000, gate=proceed

### QA-020: Self-referencing hierarchies
- **Type:** direct_mapping | **Difficulty:** Hard
- **Verdict:** INCORRECT
- **Expected:** 5 hierarchies (product_category, general_ledger_account, department, employee, project_task).
- **Generated:** Only identifies department parent_department_id.
- **Retrieval:** gt_coverage=0.8, top_score=0.7000, gate=proceed

### QA-021: Price list system
- **Type:** multi_hop | **Difficulty:** Easy
- **Verdict:** PARTIALLY_CORRECT
- **Expected:** explicit uniqueness constraint on (product_id, price_list_id, effective_date); min_quantity/discount_percentage; base_price separate.
- **Generated:** Explains price_list + product_price and FK; **does not state uniqueness constraint and min_quantity/discount threshold details clearly**.
- **Retrieval:** gt_coverage=1.0, top_score=0.8154, gate=proceed

### QA-022: CHECK constraints on status columns across major tables
- **Type:** direct_mapping | **Difficulty:** Easy
- **Verdict:** INCORRECT
- **Expected:** enumerated CHECK enum values for many tables (customer/product/sales_order/purchase_order/work_order/invoice/payment/supplier/shipment/warehouse).
- **Generated:** Says cannot find CHECK constraints; provides unrelated attribute mentions.
- **Retrieval:** gt_coverage=0.1818, top_score=0.7000, gate=proceed

### QA-023: Stock transfer process between warehouses
- **Type:** multi_hop | **Difficulty:** Medium
- **Verdict:** PARTIALLY_CORRECT
- **Expected:** stock_transfer from/to warehouses, status lifecycle; stock_transfer_line with from_bin/to_bin, quantity measures, statuses.
- **Generated:** Covers stock_transfer high-level fields and from_warehouse relationship; **omits stock_transfer_line traceability details**.
- **Retrieval:** gt_coverage=1.0, top_score=0.9620, gate=proceed

### QA-024: Production lines types
- **Type:** direct_mapping | **Difficulty:** Easy
- **Verdict:** PARTIALLY_CORRECT
- **Expected:** line_type CHECK enum list; status enum; setup time; UNIQUE line_code.
- **Generated:** Describes production_line and line_type exists, **but does not enumerate values or confirm constraint list**.
- **Retrieval:** gt_coverage=1.0, top_score=0.7295, gate=proceed

### QA-025: Budget integrates with financial accounts
- **Type:** multi_hop | **Difficulty:** Medium
- **Verdict:** PARTIALLY_CORRECT
- **Expected:** budget_id links to department_id and account_id (general_ledger_account); budgeted/actual/variance; status lifecycle; budget versions.
- **Generated:** Explains conceptual Budget→Account via account_id and variance fields; **does not cover status lifecycle and versioning explicitly**.
- **Retrieval:** gt_coverage=0.5, top_score=0.7000, gate=proceed

### QA-026: Computed/generated columns exist
- **Type:** direct_mapping | **Difficulty:** Easy
- **Verdict:** INCORRECT
- **Expected:** 3 generated stored columns: quantity_available, days_overdue, budget.variance.
- **Generated:** “cannot find this information”.
- **Retrieval:** gt_coverage=0.3333, top_score=0.7000, gate=proceed

### QA-027: Customer addresses and contacts
- **Type:** multi_hop | **Difficulty:** Easy
- **Verdict:** PARTIALLY_CORRECT
- **Expected:** address_type enum with defaults + ON DELETE CASCADE; customer_contact fields + primary + ON DELETE CASCADE.
- **Generated:** Captures tables and some attributes and FK to customer; **does not enumerate address/contact value constraints or ON DELETE CASCADE**.
- **Retrieval:** gt_coverage=1.0, top_score=0.7000, gate=proceed

### QA-028: CASCADE rules exist & tables using them
- **Type:** direct_mapping | **Difficulty:** Hard
- **Verdict:** PARTIALLY_CORRECT
- **Expected:** cascade declarations may not be surfaced; correct behavior is to not guess if not in DDL text.
- **Generated:** Says cannot find; points to missing cascade text. This is directionally correct, but the expected answer implies a more nuanced “likely tables” view.
- **Retrieval:** gt_coverage=0.0, top_score=0.7000, gate=proceed

### QA-029: Link quality inspections to source documents (polymorphic)
- **Type:** multi_hop | **Difficulty:** Medium
- **Verdict:** INCORRECT
- **Expected:** polymorphic reference_type+reference_id pattern (purchase_receipt, work_order).
- **Generated:** Says cannot find; does not extract reference_type linkage mechanism.
- **Retrieval:** gt_coverage=0.3333, top_score=0.7000, gate=proceed

### QA-030: Journal entry enforces double-entry
- **Type:** direct_mapping | **Difficulty:** Medium
- **Verdict:** PARTIALLY_CORRECT
- **Expected:** line-level CHECK debit_amount>0 XOR credit_amount>0; entry totals equal.
- **Generated:** States entry totals balance; **does not confirm line-level CHECK**.
- **Retrieval:** gt_coverage=1.0, top_score=0.9472, gate=proceed

### QA-031: NCR types and lifecycle
- **Type:** direct_mapping | **Difficulty:** Easy
- **Verdict:** PARTIALLY_CORRECT
- **Expected:** types enum (PRODUCT/PROCESS/DOCUMENTATION/SUPPLIER), severities enum, status lifecycle OPEN→IN_PROGRESS→CLOSED→VERIFIED; CAPA fields; polymorphic reference_type+reference_id.
- **Generated:** Confirms lifecycle existence but **does not enumerate types or transitions**; still describes fields generally.
- **Retrieval:** gt_coverage=1.0, top_score=0.7000, gate=proceed

### QA-032: Purchase receipt rejected quantities & lot info
- **Type:** multi_hop | **Difficulty:** Medium
- **Verdict:** PARTIALLY_CORRECT
- **Expected:** purchase_receipt_line tracks quantity_received vs quantity_rejected; lot_number, expiration_date, inspection_required flag; po_line linkage.
- **Generated:** Mentions lot/inspection_required, but **fails to explain rejected-quantity mechanism**.
- **Retrieval:** gt_coverage=1.0, top_score=0.9649, gate=proceed

### QA-033: UNIQUE constraints exist & what they enforce
- **Type:** direct_mapping | **Difficulty:** Hard
- **Verdict:** CORRECT
- **Expected:** acknowledge uniqueness exists but not surfaced unless DDL text present.
- **Generated:** Correctly says cannot find UNIQUE constraint metadata from retrieved context; avoids guessing.
- **Retrieval:** gt_coverage=0.25, top_score=0.7000, gate=proceed

### QA-034: Relationship between employees, departments, and projects
- **Type:** multi_hop | **Difficulty:** Medium
- **Verdict:** PARTIALLY_CORRECT
- **Expected:** employee.department_id and position_id; employee.manager_id; project.project_manager_id; project_task.assigned_to; time_entry links employee↔project.
- **Generated:** Correctly describes employee↔department and indirect via time_entry→project_id; **omits explicit links via project_manager_id / tasks**.
- **Retrieval:** gt_coverage=0.5, top_score=0.7000, gate=proceed

### QA-035: Relationship sales orders, invoices, payments
- **Type:** multi_hop | **Difficulty:** Medium
- **Verdict:** PARTIALLY_CORRECT
- **Expected:** invoice.order_id FK; invoice_line back-reference order_line_id; payments settle invoice; AR tracking.
- **Generated:** Explains invoice→sales_order and invoice_line→sales_order_line; payments linked to customer+invoice. **Missing explicit AR linkage and/or order_line_id naming precision**.
- **Retrieval:** gt_coverage=0.8, top_score=0.8120, gate=proceed

### QA-036: Types of inventory transactions tracked
- **Type:** direct_mapping | **Difficulty:** Easy
- **Verdict:** PARTIALLY_CORRECT
- **Expected:** explicit enum list includes RECEIPT, ISSUE, TRANSFER, ADJUSTMENT, CYCLE_COUNT, SCRAP, RETURN.
- **Generated:** Mentions receipts/issues/transfers/adjustments/cycle counts but **omits SCRAP and RETURN** (and source document reference pattern).
- **Retrieval:** gt_coverage=1.0, top_score=0.7000, gate=proceed

### QA-037: BOM component type affect manufacturing
- **Type:** direct_mapping | **Difficulty:** Medium
- **Verdict:** INCORRECT
- **Expected:** component type semantics: COMPONENT vs PHANTOM vs BYPRODUCT vs CO_PRODUCT; scrap_percentage; effective dates enable substitution.
- **Generated:** Says cannot find semantics; only repeats BOM definition (contradicts expected deeper semantics).
- **Retrieval:** gt_coverage=1.0, top_score=0.7000, gate=proceed

### QA-038: Audit log track system events and changes
- **Type:** direct_mapping | **Difficulty:** Easy
- **Verdict:** CORRECT
- **Expected:** event_type, user_id, entity_type/id, action enum, old_value/new_value JSON, ip_address,user_agent,timestamp and indexing.
- **Generated:** Covers user/entity/timestamp/ip/old/new/action; **does not mention indexes** but otherwise matches.
- **Retrieval:** gt_coverage=1.0, top_score=0.9753, gate=proceed

### QA-039: Address types supported
- **Type:** direct_mapping | **Difficulty:** Easy
- **Verdict:** INCORRECT
- **Expected:** customer address types BILLING/SHIPPING/BOTH; supplier types MAIN/BILLING/SHIPPING/RETURN; default/primary flags; cascade.
- **Generated:** Cannot enumerate address type values; fails comparison.
- **Retrieval:** gt_coverage=1.0, top_score=0.7000, gate=proceed

### QA-040: Trace product from purchase receipt to customer shipment
- **Type:** multi_hop | **Difficulty:** Hard
- **Verdict:** INCORRECT
- **Expected:** trace via receipt_line→inventory_on_hand (lot/bin)→inventory_transaction→work_order_material→inventory_transaction→sales_order→shipment→shipment_line→inventory_transaction ISSUES; lot-level trace.
- **Generated:** Stops early; claims no product linkage and no shipment linkage in context.
- **Retrieval:** gt_coverage=0.5, top_score=0.7000, gate=proceed

### QA-041: Supplier addresses and contacts vs customer
- **Type:** direct_mapping | **Difficulty:** Easy
- **Verdict:** PARTIALLY_CORRECT
- **Expected:** supplier has RETURN type; customer has BOTH; both have ON DELETE CASCADE; contact tables mirror.
- **Generated:** Claims cannot find customer-address schema; provides partial supplier address attributes.
- **Retrieval:** gt_coverage=0.5, top_score=0.7000, gate=proceed

### QA-043: shipping route connect warehouses through carrier
- **Type:** multi_hop | **Difficulty:** Medium
- **Verdict:** PARTIALLY_CORRECT
- **Expected:** shipping_route includes both warehouse FKs, carrier_id, unique route_code and cost/distance/service fields; shipment references route and optionally carrier.
- **Generated:** Covers origin/destination and carrier relationships; **omits route_code/cost_per_km/distance fields and uniqueness**.
- **Retrieval:** gt_coverage=1.0, top_score=0.7000, gate=proceed

### QA-044: production scheduling model relates to work orders
- **Type:** multi_hop | **Difficulty:** Medium
- **Verdict:** PARTIALLY_CORRECT
- **Expected:** status progression values, priority 1-10 constraint, one-to-many schedule entries.
- **Generated:** Explains linkage and timing fields, **does not include status progression or priority constraint range**.
- **Retrieval:** gt_coverage=1.0, top_score=0.9860, gate=proceed

### QA-045: invoice line links back to both sales order lines and products
- **Type:** multi_hop | **Difficulty:** Medium
- **Verdict:** PARTIALLY_CORRECT
- **Expected:** invoice_line has invoice_id + product_id + optional order_line_id; sales_order_line links to product_id.
- **Generated:** Confirms conceptual linkage but does not provide column-level specifics.
- **Retrieval:** gt_coverage=1.0, top_score=0.7370, gate=proceed

### QA-046: returns/reverse logistics capability
- **Type:** negative | **Difficulty:** Medium
- **Verdict:** INCORRECT
- **Expected:** returns partially supported (REFUND/CREDIT_MEMO/RETURN transaction and shipment_type), but no centralized RMA table.
- **Generated:** “cannot find” returns/reverse logistics.
- **Retrieval:** gt_coverage=1.0, top_score=0.7000, gate=proceed

### QA-050: multi-currency transactions (negative)
- **Type:** negative | **Difficulty:** Medium
- **Verdict:** INCORRECT
- **Expected:** no exchange rate table; multi-currency per document level exists; conversions external.
- **Generated:** Says “Yes supports multi-currency” and points at currency fields but **does not address missing exchange-rate table**, and overgeneralizes.
- **Retrieval:** gt_coverage=1.0, top_score=0.7000, gate=proceed

---

## Anomalies & Recommendations

### Red Flags
1. **“Cannot find in KG” despite high `gt_coverage`** appears in multiple items (e.g., QA-015, QA-026, QA-029, QA-046, QA-050, QA-040/QA-043 partial). This suggests the generator is either:
   - not using retrieved contexts effectively, or
   - contexts_retrieved are not actually corresponding to the expected constraint details (possible KG context compression mismatch), or
   - the evaluation labeling’s `gt_coverage` may not reflect whether the specific enum/constraint text was retrieved.
2. **Enum-heavy schema questions** (CHECK constraints, status lifecycles, unique constraint catalogs, address type enumerations, component type semantics) are frequently **incompletely answered** even when retrieval quality is high.
3. **Negative questions** sometimes fail to handle the “absence/presence” boundary correctly (notably QA-046 and QA-050).

### Recommendations
- **Add an “enumeration extraction mode”** in the query answer node when the expected answer asks for CHECK/status/value lists (e.g., parse candidate contexts for enum/check/value patterns explicitly before generating).
- **Tighten context sufficiency gating for schema-constraint questions**: if the retrieved contexts lack explicit enum/value text, the system should abstain or explicitly state “enum values not present,” but not claim coverage of lifecycle/status lists.
- **Improve negative-question prompting**: enforce templates like:
  - “Supported because X tables/columns exist; not supported because no Y table exists.”
- **Align retrieval distillation caps to constraint-bearing sources**: ensure contexts that include DDL-derived constraints or glossary enums are not dropped by compression caps.
- **Add targeted regression tests** for: CHECK enums, polymorphic reference_type+reference_id, CASCADE/ON DELETE/UPDATE visibility, computed/generated columns, and polymorphic/logical “reverse logistics” cues.

## Comparison Notes (if applicable)
- No baseline comparison data is provided beyond `study_id=AB-BEST`; therefore ablation causal claims cannot be validated.

If you want, I can also provide a concise “error taxonomy” (enum-missing vs join-key-missing vs negative-boundary vs polymorphic-mechanism) aggregated across the 55 questions from the `per_question` list.