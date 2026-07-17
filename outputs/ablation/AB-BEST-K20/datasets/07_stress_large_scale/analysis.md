# AB-BEST-K20 — 07_stress_large_scale — Run Analysis

**Timestamp:** 2026-07-17 15:13:34  
**Run tag:** `run-20260717_154008`

## Configuration

| Parameter | Value |
|-----------|-------|
| Extraction model | `LLM (gpt-5-nano-2025-08-07)` |
| Reasoning model | `gpt-5.4-nano-2026-03-17` |
| Embedding model | `BAAI/bge-m3` |
| Retrieval mode | `hybrid` |
| Reranker | `True` |
| Reranker top_k | `20` |
| Chunk size / overlap | `256 / 32` |
| ER similarity threshold | `0.75` |

## Builder Results

| Metric | Value |
|--------|-------|
| Triplets extracted | 104 |
| Entities resolved | 89 |
| Tables parsed | 55 |
| Tables completed | 55 |

## Query Evaluation Summary

| Metric | Value |
|--------|-------|
| Questions | 55 |
| Grounded | **55/55 (100%)** |
| Avg GT Coverage | 95% |
| Avg Top Score | 0.7579 |
| Avg Chunk Count | 39.7 |
| Abstained | 0 |

## RAGAS Metrics

RAGAS evaluation not enabled for this run.

## Per-Question Deep Dive

### ✅ QA-001 — What information does the customer table store and what constraints does it have?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0000 | **Gate:** `proceed`

**Expected answer:**
> The customer table stores customer_id (PK), customer_number (UNIQUE), customer_name, customer_type_id (FK to customer_type), tax_id, registration_date, status (ACTIVE/INACTIVE/SUSPENDED via CHECK), credit_limit (default 0), currency (default USD), payment_terms (default 30 days), credit_score (CHECK…

**System answer:**
> 

**Sources retrieved (8):** `customer.website`, `parent_chunk_business_glossary.md_4`, `parent_chunk_business_glossary.md_1`, `parent_chunk_business_glossary.md_3`, `payment→customer`, `customer_contact→customer`, `customer→customer_type`, `sales_order→customer`

---

### ✅ QA-002 — How does the schema classify different types of products?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0000 | **Gate:** `proceed`

**Expected answer:**
> Products are classified by product_type via CHECK constraint: FINISHED_GOOD, RAW_MATERIAL, SERVICE, or CONSUMABLE. They also belong to a hierarchical product_category (via category_id FK) where product_category has a self-referencing parent_category_id for nested categories. Products also track stat…

**System answer:**
> 

**Sources retrieved (9):** `parent_chunk_business_glossary.md_0`, `parent_chunk_business_glossary.md_2`, `parent_chunk_business_glossary.md_4`, `product.product_type`, `parent_chunk_business_glossary.md_3`, `Production Line`, `Employee`, `work_order→product`

---

### ✅ QA-003 — What is the structure of the sales order and how does it link to customers and products?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0000 | **Gate:** `proceed`

**Expected answer:**
> The sales_order table links to customer via customer_id FK and to warehouse via warehouse_id. It tracks order_number (UNIQUE), order_date, required_date, promised_date, subtotal/tax_amount/freight_amount/total_amount, and status (DRAFT/CONFIRMED/PICKED/SHIPPED/INVOICED/CANCELLED via CHECK). Priority…

**System answer:**
> 

**Sources retrieved (8):** `sales_order→customer`, `sales_order_line→product`, `sales_order_line→sales_order`, `invoice→sales_order`, `invoice_line→sales_order_line`, `sales_order.customer_id`, `work_order→product`, `Sales Order`

---

### ✅ QA-004 — How does the schema represent supplier information and their classification?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0000 | **Gate:** `proceed`

**Expected answer:**
> The supplier table stores supplier_id (PK), supplier_number (UNIQUE), supplier_name, supplier_type (MANUFACTURER/DISTRIBUTOR/SERVICE_PROVIDER via CHECK), tax_id, registration_date, and status (ACTIVE/INACTIVE/ON_HOLD/BLACKLISTED). Performance metrics are tracked: credit_rating (A/B/C/D), lead_time_d…

**System answer:**
> 

**Sources retrieved (9):** `parent_chunk_business_glossary.md_0`, `parent_chunk_business_glossary.md_4`, `purchase_order→supplier`, `supplier_address→supplier`, `app_user→supplier`, `supplier_contract→supplier`, `supplier_contact→supplier`, `purchase_receipt→supplier`

---

### ✅ QA-005 — What types of warehouses does the system support and how is storage organized?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0000 | **Gate:** `proceed`

**Expected answer:**
> The warehouse table defines four types via CHECK: COMPANY_OWNED, 3PL (third-party logistics), VIRTUAL, and TRANSIT. Each warehouse has capacity_cubic_meters and status (ACTIVE/INACTIVE/UNDER_MAINTENANCE). Storage is organized hierarchically: warehouse → warehouse_zone (types: BULK/PICK/STAGING/RECEI…

**System answer:**
> 

**Sources retrieved (10):** `parent_chunk_business_glossary.md_1`, `parent_chunk_business_glossary.md_4`, `warehouse.warehouse_type`, `Bin Location`, `Warehouse`, `warehouse_zone.zone_type`, `parent_chunk_business_glossary.md_0`, `parent_chunk_business_glossary.md_3`

---

### ✅ QA-006 — How does the inventory tracking system work across the schema?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0000 | **Gate:** `proceed`

**Expected answer:**
> Inventory is tracked at two levels. The inventory_on_hand table records current stock per product/warehouse/bin/lot combination (UNIQUE constraint), with quantity_on_hand, quantity_allocated, and a computed quantity_available column (on_hand minus allocated). The inventory_transaction table logs all…

**System answer:**
> 

**Sources retrieved (10):** `parent_chunk_business_glossary.md_0`, `parent_chunk_business_glossary.md_1`, `parent_chunk_business_glossary.md_4`, `parent_chunk_business_glossary.md_3`, `Reference Data`, `inventory_transaction→warehouse`, `inventory_transaction→product`, `inventory_transaction→bin_location`

---

### ✅ QA-007 — What is the Bill of Materials structure and how does it support multi-level product hierarchies?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0000 | **Gate:** `proceed`

**Expected answer:**
> The bill_of_materials table implements a many-to-many self-referencing relationship on the product table: parent_product_id (FK to product) contains component_product_id (FK to product) with a specified quantity and unit_of_measure. Components are classified as COMPONENT, PHANTOM, BYPRODUCT, or CO_P…

**System answer:**
> 

**Sources retrieved (9):** `parent_chunk_business_glossary.md_2`, `Bill Of Materials`, `Purchase Receipt Line`, `parent_chunk_business_glossary.md_0`, `bill_of_materials→product`, `bill_of_materials.component_product_id`, `parent_chunk_business_glossary.md_1`, `bill_of_materials`

---

### ✅ QA-008 — How are work orders structured and what do they track?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0000 | **Gate:** `proceed`

**Expected answer:**
> The work_order table references product_id (what to produce), production_line_id (where), and warehouse_id (inventory location). It tracks quantity_ordered, quantity_completed, quantity_scrapped, planned dates (start_date, required_date), actual dates (actual_start_date, actual_finish_date), status …

**System answer:**
> 

**Sources retrieved (9):** `Work Order`, `Purchase Receipt Line`, `parent_chunk_business_glossary.md_2`, `parent_chunk_business_glossary.md_0`, `work_order.quantity_ordered`, `Project Task`, `parent_chunk_business_glossary.md_3`, `work_order→production_line`

---

### ✅ QA-009 — How does the quality management system work in the schema?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0000 | **Gate:** `proceed`

**Expected answer:**
> Quality is managed through three related tables. quality_inspection records inspections with types INCOMING/IN_PROCESS/FINAL/AUDIT, results PENDING/PASS/FAIL/CONDITIONAL_PASS, and links to quality_standard (types INTERNAL/ISO/ASTM/FDA/CE). Inspections track defects_found, sample_size, and batch_size…

**System answer:**
> 

**Sources retrieved (12):** `parent_chunk_business_glossary.md_3`, `parent_chunk_business_glossary.md_0`, `Quality Inspection`, `parent_chunk_business_glossary.md_4`, `quality_inspection.standard_id`, `quality_inspection→quality_standard`, `quality_inspection→product`, `quality_inspection→warehouse`

---

### ✅ QA-010 — What is the complete invoice lifecycle and how are invoices linked to orders and payments?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0000 | **Gate:** `proceed`

**Expected answer:**
> The invoice table supports four types via CHECK: SALES, PURCHASE, CREDIT_MEMO, and DEBIT_MEMO. Invoices link to customer_id and optionally order_id (FK to sales_order). They track subtotal/tax_amount/total_amount/amount_paid/balance_due and status (DRAFT/POSTED/PAID/OVERDUE/VOID). Each invoice has i…

**System answer:**
> 

**Sources retrieved (10):** `payment.invoice_id`, `invoice.order_id`, `accounts_payable.invoice_date`, `invoice→sales_order`, `payment→invoice`, `invoice_line→sales_order_line`, `invoice_line→invoice`, `invoice→customer`

---

### ✅ QA-011 — How does the procurement process flow from purchase order to receipt?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0000 | **Gate:** `proceed`

**Expected answer:**
> Purchase orders (purchase_order) link to supplier_id FK and warehouse_id, with status lifecycle DRAFT/SUBMITTED/ACKNOWLEDGED/PARTIAL/RECEIVED/CLOSED/CANCELLED. Each PO has purchase_order_line items referencing products with quantity tracking (ordered/received/invoiced) and supplier_part_number. When…

**System answer:**
> 

**Sources retrieved (10):** `parent_chunk_business_glossary.md_0`, `parent_chunk_business_glossary.md_3`, `purchase_receipt→purchase_order`, `purchase_receipt_line→purchase_order_line`, `purchase_receipt.po_id`, `purchase_receipt_line.po_line_id`, `Purchase Receipt`, `Purchase Receipt Line`

---

### ✅ QA-012 — How does the general ledger and accounting system work?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0000 | **Gate:** `proceed`

**Expected answer:**
> The GL is built on account_type (DEBIT or CREDIT balance_type), general_ledger_account (with hierarchical parent_account_id self-reference and status ACTIVE/INACTIVE), and accounting_period (with fiscal_year, start/end dates, and is_closed flag). Journal entries (journal_entry) reference a period, h…

**System answer:**
> 

**Sources retrieved (8):** `parent_chunk_business_glossary.md_1`, `general_ledger_account→account_type`, `general_ledger_account→general_ledger_account`, `journal_entry_line→general_ledger_account`, `General Ledger Account`, `general_ledger_account.account_number`, `general_ledger_account`, `general_ledger_account.parent_account_id`

---

### ✅ QA-013 — How are accounts receivable and accounts payable tracked?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0000 | **Gate:** `proceed`

**Expected answer:**
> Accounts receivable (accounts_receivable) links to customer_id and invoice_id, tracking amount_original, amount_due, due_date, and a computed days_overdue column. Status values are CURRENT/DUE/OVERDUE/COLLECTION/WRITE_OFF, with collection_status and next_action_date for collections workflow. Account…

**System answer:**
> 

**Sources retrieved (8):** `parent_chunk_business_glossary.md_1`, `accounts_payable.amount_due`, `accounts_payable→invoice`, `accounts_payable→supplier`, `Accounts Receivable`, `accounts_payable`, `payment→invoice`, `payment→customer`

---

### ✅ QA-014 — How is the employee and organizational structure represented?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0000 | **Gate:** `proceed`

**Expected answer:**
> The department table has hierarchical parent_department_id self-reference with status ACTIVE/INACTIVE. Positions (position table) belong to departments via department_id FK, with grade_level, salary range (min/max), and FLSA status (EXEMPT/NON_EXEMPT). Employees reference department_id, position_id,…

**System answer:**
> 

**Sources retrieved (9):** `parent_chunk_business_glossary.md_2`, `Employee`, `Position`, `parent_chunk_business_glossary.md_4`, `employee.employee_type`, `employee→employee`, `project→employee`, `employee→department`

---

### ✅ QA-015 — How does the shipment and logistics system work?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0000 | **Gate:** `proceed`

**Expected answer:**
> Carriers (carrier table) are classified by type: LTL/FTL/PARCEL/AIR/OCEAN/RAIL with rating (0-5). Shipping routes define paths between warehouses (origin_location_id, destination_location_id both FK to warehouse) with distance_km, estimated_hours, and cost_per_km. Shipments reference origin/destinat…

**System answer:**
> 

**Sources retrieved (12):** `parent_chunk_business_glossary.md_3`, `parent_chunk_business_glossary.md_1`, `parent_chunk_business_glossary.md_0`, `shipment_line.shipment_id`, `shipment→carrier`, `shipment→shipping_route`, `shipment→warehouse`, `shipment_line→shipment`

---

### ✅ QA-016 — How does the project management module work?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0000 | **Gate:** `proceed`

**Expected answer:**
> Projects link to customer_id (for customer-facing projects) and project_manager_id (FK to employee). Project types are CUSTOMER/INTERNAL/R&D/CAPITAL with status PLANNING/ACTIVE/ON_HOLD/COMPLETED/CANCELLED and priority levels. Projects track budget_amount vs actual_cost. Project tasks (project_task) …

**System answer:**
> 

**Sources retrieved (12):** `parent_chunk_business_glossary.md_3`, `Project Task`, `Time Entry`, `parent_chunk_business_glossary.md_2`, `parent_chunk_business_glossary.md_0`, `parent_chunk_business_glossary.md_1`, `project→employee`, `project_task→project`

---

### ✅ QA-017 — How does the system handle user authentication, roles, and permissions?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0000 | **Gate:** `proceed`

**Expected answer:**
> The app_user table links to employee_id, customer_id, or supplier_id depending on user_type (EMPLOYEE/CUSTOMER/SUPPLIER/ADMIN). Users have status ACTIVE/INACTIVE/LOCKED/PENDING with failed_login_attempts tracking. Roles (role table) are typed as SYSTEM/BUSINESS/CUSTOM with ACTIVE/INACTIVE status. Th…

**System answer:**
> 

**Sources retrieved (9):** `User`, `Role`, `parent_chunk_business_glossary.md_4`, `user_role.user_id`, `user_role→app_user`, `user_role→role`, `audit_log→app_user`, `app_user→employee`

---

### ✅ QA-018 — What is the complete path from a customer placing an order to the product being shipped?

**Status:** GROUNDED  
**GT Coverage:** 75% | **Top Score:** 0.0000 | **Gate:** `proceed`

**Expected answer:**
> The order-to-ship path traverses: customer → sales_order (via customer_id FK) → sales_order_line (via order_id FK) → product (via product_id FK). For fulfillment: sales_order references warehouse_id for the fulfillment location. Inventory is checked via inventory_on_hand (product_id + warehouse_id).…

**System answer:**
> 

**Sources retrieved (11):** `parent_chunk_business_glossary.md_0`, `parent_chunk_business_glossary.md_3`, `parent_chunk_business_glossary.md_2`, `sales_order_line.quantity_shipped`, `Purchase Receipt Line`, `sales_order→customer`, `purchase_order_line→product`, `sales_order_line→product`

---

### ✅ QA-019 — How does the schema support supplier contracts and their relationship to purchase orders?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0000 | **Gate:** `proceed`

**Expected answer:**
> The supplier_contract table links to supplier_id FK, with contract_type (FIXED_PRICE/COST_PLUS/RATE_BASED/FRAMEWORK), start/end dates, auto_renew flag, payment_terms, total_value, and status (DRAFT/ACTIVE/EXPIRED/TERMINATED). Purchase orders independently link to the same supplier via supplier_id FK…

**System answer:**
> 

**Sources retrieved (8):** `parent_chunk_business_glossary.md_0`, `purchase_order.supplier_reference`, `parent_chunk_business_glossary.md_4`, `purchase_order→supplier`, `purchase_receipt→supplier`, `parent_chunk_business_glossary.md_3`, `supplier_contract→supplier`, `purchase_order_line→purchase_order`

---

### ✅ QA-020 — What self-referencing hierarchies exist in the schema?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0000 | **Gate:** `proceed`

**Expected answer:**
> The schema has five self-referencing hierarchies: (1) product_category.parent_category_id → product_category.category_id for nested product classifications; (2) general_ledger_account.parent_account_id → general_ledger_account.account_id for chart of accounts hierarchy; (3) department.parent_departm…

**System answer:**
> 

**Sources retrieved (12):** `General Ledger Account`, `Department`, `parent_chunk_business_glossary.md_2`, `parent_chunk_business_glossary.md_1`, `work_order→production_line`, `work_order_material→work_order`, `payment→invoice`, `project→employee`

---

### ✅ QA-021 — How does the price list system work for products?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0000 | **Gate:** `proceed`

**Expected answer:**
> The price_list table defines named price lists with currency, effective_date, expiration_date, and status. The product_price junction table links products to price lists with price, minimum_quantity (for volume pricing), discount_percentage, and effective_date. A UNIQUE constraint on (product_id, pr…

**System answer:**
> 

**Sources retrieved (9):** `parent_chunk_business_glossary.md_0`, `product_price.price_list_id`, `price_list.price_list_id`, `Purchase Receipt Line`, `parent_chunk_business_glossary.md_2`, `parent_chunk_business_glossary.md_3`, `product_price→price_list`, `price_list`

---

### ✅ QA-022 — What CHECK constraints on status columns exist across the major tables?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0000 | **Gate:** `proceed`

**Expected answer:**
> Key status CHECK constraints include: customer (ACTIVE/INACTIVE/SUSPENDED), product (ACTIVE/DISCONTINUED/PHASE_OUT), sales_order (DRAFT/CONFIRMED/PICKED/SHIPPED/INVOICED/CANCELLED), purchase_order (DRAFT/SUBMITTED/ACKNOWLEDGED/PARTIAL/RECEIVED/CLOSED/CANCELLED), work_order (DRAFT/RELEASED/IN_PROGRES…

**System answer:**
> 

**Sources retrieved (12):** `parent_chunk_business_glossary.md_4`, `parent_chunk_business_glossary.md_2`, `quality_inspection.status`, `customer.status`, `department.status`, `role.status`, `general_ledger_account.status`, `Purchase Receipt Line`

---

### ✅ QA-023 — How does the stock transfer process work between warehouses?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0000 | **Gate:** `proceed`

**Expected answer:**
> Stock transfers use the stock_transfer table with from_warehouse_id and to_warehouse_id (both FK to warehouse), transfer_date, shipment_method, tracking_number, and status (DRAFT/PICKED/SHIPPED/RECEIVED/CANCELLED). Individual items are tracked via stock_transfer_line with from_bin_id and to_bin_id (…

**System answer:**
> 

**Sources retrieved (8):** `parent_chunk_business_glossary.md_1`, `parent_chunk_business_glossary.md_3`, `Stock Transfer`, `stock_transfer.to_warehouse_id`, `stock_transfer→warehouse`, `stock_transfer_line→bin_location`, `stock_transfer_line→stock_transfer`, `stock_transfer_line→product`

---

### ✅ QA-024 — How are production lines defined and what types exist?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0000 | **Gate:** `proceed`

**Expected answer:**
> The production_line table defines manufacturing resources with line_code (UNIQUE), line_name, line_type (ASSEMBLY/DISCRETE/PROCESS/MIXING via CHECK), location_id (FK to warehouse for the physical location), capacity_per_hour, setup_time_minutes, and status (ACTIVE/MAINTENANCE/INACTIVE). Production l…

**System answer:**
> 

**Sources retrieved (9):** `parent_chunk_business_glossary.md_2`, `parent_chunk_business_glossary.md_3`, `Production Line`, `Production Schedule`, `parent_chunk_business_glossary.md_4`, `work_order→production_line`, `production_line→warehouse`, `production_schedule→production_line`

---

### ✅ QA-025 — How does the budget system integrate with the financial accounts?

**Status:** GROUNDED  
**GT Coverage:** 50% | **Top Score:** 0.0000 | **Gate:** `proceed`

**Expected answer:**
> The budget table links to both department_id and account_id (FK to general_ledger_account). It tracks budget_type (OPERATING/CAPITAL/PROJECT), fiscal_year, budgeted_amount, actual_amount, and a computed variance column (budgeted minus actual). Budget status follows DRAFT/APPROVED/ACTIVE/CLOSED. This…

**System answer:**
> 

**Sources retrieved (10):** `parent_chunk_business_glossary.md_1`, `General Ledger Account`, `parent_chunk_business_glossary.md_4`, `parent_chunk_business_glossary.md_3`, `accounts_payable.payment_priority`, `accounts_payable→invoice`, `journal_entry_line.account_id`, `general_ledger_account.currency`

---

### ✅ QA-026 — What computed/generated columns exist in the schema?

**Status:** GROUNDED  
**GT Coverage:** 0% | **Top Score:** 0.0000 | **Gate:** `proceed`

**Expected answer:**
> The schema has three computed columns using GENERATED ALWAYS AS: (1) inventory_on_hand.quantity_available = quantity_on_hand - quantity_allocated; (2) accounts_receivable.days_overdue = DATEDIFF(CURRENT_DATE, due_date); (3) budget.variance = budgeted_amount - actual_amount. All are STORED (materiali…

**System answer:**
> 

**Sources retrieved (12):** `parent_chunk_business_glossary.md_4`, `work_order→production_line`, `payment→invoice`, `bill_of_materials→product`, `work_order_material→work_order`, `invoice_line→sales_order_line`, `shipping_route→warehouse`, `production_schedule.created_at`

---

### ✅ QA-027 — How are customer addresses and contacts structured?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0000 | **Gate:** `proceed`

**Expected answer:**
> Customer addresses are stored in customer_address with address_type (BILLING/SHIPPING/BOTH via CHECK), full address fields (line1, line2, city, state, postal_code, country_code), and is_default flag. The customer_id FK has ON DELETE CASCADE. Customer contacts are in customer_contact with contact_nam…

**System answer:**
> 

**Sources retrieved (9):** `customer_address.created_at`, `customer_address→customer`, `customer_contact→customer`, `project→customer`, `sales_order→customer`, `payment→customer`, `invoice→customer`, `customer_contact.is_primary`

---

### ✅ QA-028 — What CASCADE rules exist in the schema and what tables use them?

**Status:** GROUNDED  
**GT Coverage:** 75% | **Top Score:** 0.0000 | **Gate:** `proceed`

**Expected answer:**
> CASCADE rules (ON DELETE CASCADE, ON UPDATE CASCADE) are defined in foreign key constraint syntax within the DDL. These details are typically on child tables like customer_address, customer_contact, sales_order_line, and purchase_order_line. However, specific CASCADE declarations may not be surfaced…

**System answer:**
> 

**Sources retrieved (11):** `shipping_route→warehouse`, `inventory_transaction→warehouse`, `shipment→warehouse`, `quality_standard.standard_code`, `role.role_code`, `Reference Data`, `parent_chunk_business_glossary.md_2`, `parent_chunk_business_glossary.md_3`

---

### ✅ QA-029 — How does the schema link quality inspections to their source documents?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0000 | **Gate:** `proceed`

**Expected answer:**
> Quality inspections use a polymorphic reference pattern: reference_type (VARCHAR) identifies the source table (e.g., 'purchase_receipt', 'work_order') and reference_id (INT) stores the primary key of that source record. The inspection also directly references product_id and warehouse_id via foreign …

**System answer:**
> 

**Sources retrieved (8):** `quality_inspection.reference_type`, `quality_inspection→quality_standard`, `quality_inspection→product`, `quality_inspection→warehouse`, `Quality Inspection`, `non_conformance_report→product`, `supplier_contact→supplier`, `supplier_contract→supplier`

---

### ✅ QA-030 — How does the journal entry enforce double-entry bookkeeping?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0000 | **Gate:** `proceed`

**Expected answer:**
> The journal_entry table requires total_debit and total_credit columns to be present (both NOT NULL DECIMAL 15,2). Journal_entry_line items each reference a general_ledger_account and have a CHECK constraint ensuring exactly one of debit_amount or credit_amount is positive: CHECK ((debit_amount > 0 A…

**System answer:**
> 

**Sources retrieved (9):** `Journal Entry`, `Financial Transaction`, `parent_chunk_business_glossary.md_1`, `journal_entry→accounting_period`, `journal_entry_line→journal_entry`, `journal_entry_line→general_ledger_account`, `journal_entry.approved_by`, `journal_entry`

---

### ✅ QA-031 — What types of non-conformance reports exist and what is their lifecycle?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0000 | **Gate:** `proceed`

**Expected answer:**
> Non-conformance reports (NCRs) have four types via CHECK: PRODUCT, PROCESS, DOCUMENTATION, and SUPPLIER. Severity is classified as MINOR/MAJOR/CRITICAL. The status lifecycle is OPEN → IN_PROGRESS → CLOSED → VERIFIED. NCRs track root_cause, corrective_action, and preventive_action (all TEXT fields) f…

**System answer:**
> 

**Sources retrieved (8):** `parent_chunk_business_glossary.md_4`, `non_conformance_report.ncr_type`, `parent_chunk_business_glossary.md_3`, `parent_chunk_business_glossary.md_0`, `Non Conformance Report`, `Bill Of Materials`, `General Ledger Account`, `purchase_receipt_line`

---

### ✅ QA-032 — How does the purchase receipt track rejected quantities and lot information?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0000 | **Gate:** `proceed`

**Expected answer:**
> The purchase_receipt_line table tracks three quantity measures: quantity_ordered, quantity_received, and quantity_rejected. When quantity_rejected > 0, materials failed inspection. Each receipt line also records lot_number (for lot traceability), expiration_date (for perishable items), location_id (…

**System answer:**
> 

**Sources retrieved (8):** `purchase_receipt_line.quantity_rejected`, `Purchase Receipt Line`, `parent_chunk_business_glossary.md_0`, `parent_chunk_business_glossary.md_1`, `parent_chunk_business_glossary.md_3`, `purchase_receipt_line→purchase_receipt`, `purchase_receipt→purchase_order`, `purchase_receipt_line→purchase_order_line`

---

### ✅ QA-033 — What UNIQUE constraints exist across the schema and what do they enforce?

**Status:** GROUNDED  
**GT Coverage:** 75% | **Top Score:** 0.0000 | **Gate:** `proceed`

**Expected answer:**
> UNIQUE constraints exist on business identifier columns (customer.customer_number, product.product_number, supplier.supplier_number, invoice.invoice_number) and composite keys. However, constraint metadata (UNIQUE, CHECK, etc.) may not surface through chunk-based retrieval unless the constraint DDL …

**System answer:**
> 

**Sources retrieved (12):** `Production Schedule`, `Time Entry`, `Reference Data`, `Master Data`, `parent_chunk_business_glossary.md_4`, `parent_chunk_business_glossary.md_2`, `payment→invoice`, `shipment→warehouse`

---

### ✅ QA-034 — How does the schema handle the relationship between employees, departments, and projects?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0000 | **Gate:** `proceed`

**Expected answer:**
> Employees belong to departments via department_id FK and hold positions via position_id FK. Positions also reference department_id, creating a redundant but verifiable link. Employee.manager_id (self-referencing FK) creates reporting chains. Projects link to project_manager_id (FK to employee) and o…

**System answer:**
> 

**Sources retrieved (10):** `parent_chunk_business_glossary.md_2`, `parent_chunk_business_glossary.md_1`, `department.created_at`, `parent_chunk_business_glossary.md_3`, `Project`, `project.description`, `Department`, `parent_chunk_business_glossary.md_4`

---

### ✅ QA-035 — What is the relationship between sales orders, invoices, and payments?

**Status:** GROUNDED  
**GT Coverage:** 80% | **Top Score:** 0.0000 | **Gate:** `proceed`

**Expected answer:**
> Sales orders are invoiced by creating invoice records with order_id FK referencing sales_order. Invoice line items (invoice_line) can link back to specific sales_order_line items via order_line_id FK. Payments reference invoice_id FK to settle invoices. The invoice tracks amount_paid and balance_due…

**System answer:**
> 

**Sources retrieved (12):** `parent_chunk_business_glossary.md_0`, `parent_chunk_business_glossary.md_4`, `parent_chunk_business_glossary.md_1`, `sales_order.payment_terms`, `payment.invoice_id`, `sales_order_line.quantity_invoiced`, `parent_chunk_business_glossary.md_3`, `invoice→sales_order`

---

### ✅ QA-036 — What types of inventory transactions does the system track?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0000 | **Gate:** `proceed`

**Expected answer:**
> The inventory_transaction table supports seven transaction types via CHECK constraint: RECEIPT (goods received from suppliers), ISSUE (materials consumed by production or shipped to customers), TRANSFER (movement between warehouses/bins), ADJUSTMENT (corrections to inventory counts), CYCLE_COUNT (pe…

**System answer:**
> 

**Sources retrieved (9):** `parent_chunk_business_glossary.md_1`, `parent_chunk_business_glossary.md_0`, `parent_chunk_business_glossary.md_4`, `Inventory Transaction`, `parent_chunk_business_glossary.md_3`, `inventory_transaction→product`, `inventory_transaction→warehouse`, `inventory_transaction→bin_location`

---

### ✅ QA-037 — How does the BOM component type affect manufacturing?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0000 | **Gate:** `proceed`

**Expected answer:**
> The bill_of_materials table classifies components into four types via CHECK: COMPONENT (standard parts consumed in production), PHANTOM (sub-assemblies that are not stocked — their components are consumed directly), BYPRODUCT (secondary outputs of the production process), and CO_PRODUCT (additional …

**System answer:**
> 

**Sources retrieved (10):** `parent_chunk_business_glossary.md_2`, `Purchase Receipt Line`, `bill_of_materials.bom_id`, `bill_of_materials→product`, `Bill Of Materials`, `Production Line`, `parent_chunk_business_glossary.md_3`, `parent_chunk_business_glossary.md_4`

---

### ✅ QA-038 — How does the audit log track system events and changes?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0000 | **Gate:** `proceed`

**Expected answer:**
> The audit_log table records every significant system event with event_type, user_id (FK to app_user), entity_type (which table was affected), entity_id (which record), and action (CREATE/READ/UPDATE/DELETE/LOGIN/LOGOUT/EXPORT via CHECK). For data changes, old_value and new_value are stored as JSON. …

**System answer:**
> 

**Sources retrieved (8):** `Audit Log`, `parent_chunk_business_glossary.md_4`, `audit_log.log_id`, `parent_chunk_business_glossary.md_3`, `audit_log→app_user`, `parent_chunk_business_glossary.md_1`, `Reference Data`, `Warehouse`

---

### ✅ QA-039 — What are the different address types supported across the schema?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0000 | **Gate:** `proceed`

**Expected answer:**
> Customer addresses support three types: BILLING, SHIPPING, and BOTH. Supplier addresses support four types: MAIN, BILLING, SHIPPING, and RETURN. Both customer_address and supplier_address have is_default/is_primary flags and cascade delete from their parent. The warehouse table stores location_addre…

**System answer:**
> 

**Sources retrieved (9):** `parent_chunk_business_glossary.md_4`, `parent_chunk_business_glossary.md_0`, `supplier_address→supplier`, `customer_address→customer`, `customer_address.address_type`, `supplier_address.address_type`, `Reference Data`, `supplier_address.city`

---

### ✅ QA-040 — How would the schema support tracing a product from purchase receipt to customer shipment?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0000 | **Gate:** `proceed`

**Expected answer:**
> The full traceability path is: purchase_receipt (inbound from supplier) → purchase_receipt_line (with lot_number) → inventory_on_hand (lot_number at warehouse/bin) → inventory_transaction (RECEIPT type logs the inbound). For production: work_order_material records material consumption → work_order t…

**System answer:**
> 

**Sources retrieved (10):** `parent_chunk_business_glossary.md_1`, `parent_chunk_business_glossary.md_0`, `purchase_receipt_line→product`, `purchase_receipt.received_by`, `Purchase Receipt Line`, `purchase_receipt_line→purchase_receipt`, `purchase_receipt_line→purchase_order_line`, `purchase_receipt→purchase_order`

---

### ✅ QA-041 — How are supplier addresses and contacts structured compared to customer addresses?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0000 | **Gate:** `proceed`

**Expected answer:**
> Both follow the same pattern: parent entity → address table + contact table, both with ON DELETE CASCADE. Supplier_address has address_type MAIN/BILLING/SHIPPING/RETURN (vs customer's BILLING/SHIPPING/BOTH) and uses is_primary flag (vs customer_address's is_default). Supplier_contact mirrors custome…

**System answer:**
> 

**Sources retrieved (8):** `Master Data`, `parent_chunk_business_glossary.md_0`, `parent_chunk_business_glossary.md_4`, `parent_chunk_business_glossary.md_3`, `supplier_address→supplier`, `supplier_contact→supplier`, `customer_address→customer`, `supplier_address.address_id`

---

### ✅ QA-042 — Does the schema track employee compensation history?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0000 | **Gate:** `proceed`

**Expected answer:**
> The employee table has current annual_salary and hourly_rate columns and the position table defines min_salary and max_salary ranges. However, there is no compensation history table in the schema — salary changes would overwrite the current values without preserving history. The only historical trac…

**System answer:**
> 

**Sources retrieved (8):** `parent_chunk_business_glossary.md_2`, `employee.annual_salary`, `parent_chunk_business_glossary.md_3`, `project→employee`, `employee→employee`, `employee→position`, `time_entry→employee`, `employee→department`

---

### ✅ QA-043 — How does the shipping route connect two warehouses through a carrier?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0000 | **Gate:** `proceed`

**Expected answer:**
> The shipping_route table has origin_location_id and destination_location_id (both FK to warehouse), carrier_id (FK to carrier), plus route_code (UNIQUE), distance_km, estimated_hours, cost_per_km, and service_level. Shipments reference route_id FK to use a predefined route, plus independently refere…

**System answer:**
> 

**Sources retrieved (8):** `shipping_route.carrier_id`, `shipping_route→carrier`, `parent_chunk_business_glossary.md_3`, `shipping_route→warehouse`, `shipment→shipping_route`, `Shipping Route`, `shipping_route`, `shipping_route.estimated_hours`

---

### ✅ QA-044 — What is the production scheduling model and how does it relate to work orders?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0000 | **Gate:** `proceed`

**Expected answer:**
> The production_schedule table links work_order_id (FK to work_order) to production_line_id (FK to production_line) with scheduled_start and scheduled_end timestamps, plus actual_start and actual_end for tracking real execution. Status progresses SCHEDULED → RUNNING → COMPLETED (or CANCELLED). Priori…

**System answer:**
> 

**Sources retrieved (8):** `production_schedule.work_order_id`, `parent_chunk_business_glossary.md_2`, `Production Schedule`, `parent_chunk_business_glossary.md_3`, `parent_chunk_business_glossary.md_4`, `parent_chunk_business_glossary.md_0`, `production_schedule→work_order`, `work_order→production_line`

---

### ✅ QA-045 — How does the invoice line link back to both sales order lines and products?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0000 | **Gate:** `proceed`

**Expected answer:**
> Invoice_line references invoice_id FK (parent invoice), product_id FK (what was invoiced), and optionally order_line_id FK (back-reference to the specific sales_order_line). This three-way linkage supports: invoice → sales_order (via invoice.order_id), invoice_line → product (direct), and invoice_li…

**System answer:**
> 

**Sources retrieved (9):** `invoice_line→sales_order_line`, `invoice→sales_order`, `sales_order_line→product`, `sales_order_line→sales_order`, `sales_order_line.quantity_invoiced`, `invoice_line→product`, `invoice_line→invoice`, `invoice_line.product_id`

---

### ✅ QA-046 — Is there a returns or reverse logistics capability in the schema?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0000 | **Gate:** `proceed`

**Expected answer:**
> Returns are partially supported: payment_type includes REFUND, invoice_type includes CREDIT_MEMO, shipment_type includes RETURN, and inventory_transaction has a RETURN transaction type. However, there is no dedicated returns management table (e.g., return_authorization or RMA). Returns would be trac…

**System answer:**
> 

**Sources retrieved (12):** `Warehouse`, `parent_chunk_business_glossary.md_3`, `parent_chunk_business_glossary.md_1`, `sales_order.shipping_method`, `shipment→warehouse`, `shipping_route→warehouse`, `payment→invoice`, `work_order→warehouse`

---

### ✅ QA-047 — How many tables are in each business domain and what are they?

**Status:** GROUNDED  
**GT Coverage:** N/A | **Top Score:** 0.0000 | **Gate:** `proceed`

**Expected answer:**
> A complete table-by-domain breakdown requires schema-wide overview not available from individual chunk retrieval. From retrieved context, identifiable domains include Sales & Customer Management (customer, product, sales_order, etc.), Finance (invoice, payment, journal_entry, gl_account), HR (employ…

**System answer:**
> 

**Sources retrieved (11):** `sales_order.subtotal`, `accounts_payable.discount_available`, `stock_transfer→warehouse`, `supplier_contact→supplier`, `customer_address→customer`, `project→customer`, `work_order→warehouse`, `supplier_address→supplier`

---

### ✅ QA-048 — How does the accounting period system work?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0000 | **Gate:** `proceed`

**Expected answer:**
> The accounting_period table defines fiscal periods with period_code (UNIQUE), period_name, start_date, end_date, fiscal_year, and is_closed flag. A UNIQUE constraint on (fiscal_year, period_code) prevents duplicate periods within a year. Journal entries reference period_id FK to ensure postings land…

**System answer:**
> 

**Sources retrieved (8):** `parent_chunk_business_glossary.md_1`, `journal_entry→accounting_period`, `accounting_period.period_id`, `accounting_period`, `accounting_period.closed_at`, `accounting_period.is_closed`, `accounting_period.end_date`, `parent_chunk_business_glossary.md_2`

---

### ✅ QA-049 — How do work order materials track material consumption against BOM requirements?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0000 | **Gate:** `proceed`

**Expected answer:**
> The work_order_material table links work_order_id FK to product_id FK (the material), with quantity_required (from BOM calculation) and quantity_issued (actually consumed). Status tracks progress: PENDING/ISSUED/PARTIAL/COMPLETE. Materials are sourced from specific bins via bin_id FK to bin_location…

**System answer:**
> 

**Sources retrieved (9):** `Purchase Receipt Line`, `parent_chunk_business_glossary.md_2`, `parent_chunk_business_glossary.md_3`, `parent_chunk_business_glossary.md_0`, `Work Order`, `work_order_material.quantity_required`, `work_order_material→work_order`, `work_order_material→product`

---

### ✅ QA-050 — Does the schema support multi-currency transactions?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0000 | **Gate:** `proceed`

**Expected answer:**
> Multiple tables have currency columns defaulting to USD: customer.currency, sales_order.currency, invoice.currency, payment.currency, purchase_order.currency, supplier.currency, supplier_contract.currency, general_ledger_account.currency, and price_list.currency. However, there is no currency exchan…

**System answer:**
> 

**Sources retrieved (12):** `parent_chunk_business_glossary.md_1`, `Accounts Receivable`, `Inventory Transaction`, `parent_chunk_business_glossary.md_4`, `General Ledger Account`, `payment.currency`, `purchase_order.currency`, `sales_order.currency`

---

### ✅ QA-051 — How does the schema handle product storage requirements for hazardous or temperature-sensitive items?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0000 | **Gate:** `proceed`

**Expected answer:**
> Products have three relevant fields: hazardous (BOOLEAN, default FALSE), storage_temperature_min (DECIMAL), and storage_temperature_max (DECIMAL). Warehouse zones have a temperature_controlled (BOOLEAN) flag. When a product requires temperature control, it should be stored in bins within temperature…

**System answer:**
> 

**Sources retrieved (10):** `product.hazardous`, `Purchase Receipt Line`, `Bill Of Materials`, `parent_chunk_business_glossary.md_1`, `parent_chunk_business_glossary.md_0`, `parent_chunk_business_glossary.md_3`, `parent_chunk_business_glossary.md_2`, `parent_chunk_business_glossary.md_4`

---

### ✅ QA-052 — What polymorphic reference patterns exist in the schema?

**Status:** GROUNDED  
**GT Coverage:** 57% | **Top Score:** 0.0000 | **Gate:** `proceed`

**Expected answer:**
> The schema uses reference_type + reference_id polymorphic patterns in several tables: (1) quality_inspection — reference_type identifies the source (purchase_receipt, work_order) and reference_id stores the ID; (2) inventory_transaction — reference_type identifies the source document (sales_order, p…

**System answer:**
> 

**Sources retrieved (12):** `production_schedule→work_order`, `production_schedule→production_line`, `payment→invoice`, `shipment→warehouse`, `invoice→sales_order`, `purchase_order_line→purchase_order`, `Reference Data`, `inventory_transaction.reference_type`

---

### ✅ QA-053 — Is there a customer loyalty or rewards program in the schema?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0000 | **Gate:** `proceed`

**Expected answer:**
> No, the schema does not contain any tables or columns for customer loyalty programs, reward points, or promotional campaigns. Customer classification is limited to customer_type_id (FK to customer_type), credit_score, and is_preferred-style fields do not exist. The customer table focuses on commerci…

**System answer:**
> 

**Sources retrieved (11):** `project→customer`, `payment→customer`, `customer→customer_type`, `app_user→customer`, `invoice→customer`, `customer_contact→customer`, `customer.payment_terms`, `Customer`

---

### ✅ QA-054 — How does the schema support three-way matching in procurement?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0000 | **Gate:** `proceed`

**Expected answer:**
> Three-way matching (PO → receipt → invoice) is supported through linked tables: purchase_order_line tracks quantity_ordered, quantity_received, and quantity_invoiced. Purchase_receipt_line links back to po_line_id FK. Invoice can be linked to purchase activities via invoice_type = 'PURCHASE' and acc…

**System answer:**
> 

**Sources retrieved (8):** `parent_chunk_business_glossary.md_0`, `parent_chunk_business_glossary.md_4`, `parent_chunk_business_glossary.md_1`, `purchase_order.approved_by`, `purchase_order→supplier`, `purchase_order_line→purchase_order`, `purchase_receipt_line→purchase_order_line`, `purchase_receipt→purchase_order`

---

### ✅ QA-055 — What indexes exist for performance optimization and which tables have the most?

**Status:** GROUNDED  
**GT Coverage:** N/A | **Top Score:** 0.0000 | **Gate:** `proceed`

**Expected answer:**
> Index definitions (CREATE INDEX statements) are DDL metadata that may not surface through chunk-based retrieval unless explicitly included in retrieved context. The schema likely defines indexes on foreign key columns and frequently-queried fields, but specific index names, compositions, and per-tab…

**System answer:**
> 

**Sources retrieved (8):** `parent_chunk_business_glossary.md_4`, `parent_chunk_business_glossary.md_2`, `parent_chunk_business_glossary.md_3`, `parent_chunk_business_glossary.md_0`, `quality_inspection.standard_id`, `project_task→employee`, `time_entry→employee`, `inventory_transaction→warehouse`

---

## Anomalies & Observations

No anomalies detected. All questions grounded with acceptable RAGAS scores.
