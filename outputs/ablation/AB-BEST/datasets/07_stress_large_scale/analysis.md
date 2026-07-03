# AB-BEST — 07_stress_large_scale — Run Analysis

**Timestamp:** 2026-07-03 10:54:48  
**Run tag:** `run-20260703_110655`

## Configuration

| Parameter | Value |
|-----------|-------|
| Extraction model | `LLM (gpt-5-nano-2025-08-07)` |
| Reasoning model | `gpt-5.4-nano-2026-03-17` |
| Embedding model | `BAAI/bge-m3` |
| Retrieval mode | `hybrid` |
| Reranker | `True` |
| Reranker top_k | `5` |
| Chunk size / overlap | `256 / 32` |
| ER similarity threshold | `0.75` |

## Builder Results

| Metric | Value |
|--------|-------|
| Triplets extracted | 111 |
| Entities resolved | 84 |
| Tables parsed | 55 |
| Tables completed | 55 |

## Query Evaluation Summary

| Metric | Value |
|--------|-------|
| Questions | 55 |
| Grounded | **55/55 (100%)** |
| Avg GT Coverage | 85% |
| Avg Top Score | 0.7416 |
| Avg Chunk Count | 24.3 |
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

**Sources retrieved (8):** `customer.website`, `customer`, `Customer`, `customer_type`, `customer.tax_id`, `customer.credit_score`, `customer.customer_number`, `customer.industry_code`

---

### ✅ QA-002 — How does the schema classify different types of products?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0000 | **Gate:** `proceed`

**Expected answer:**
> Products are classified by product_type via CHECK constraint: FINISHED_GOOD, RAW_MATERIAL, SERVICE, or CONSUMABLE. They also belong to a hierarchical product_category (via category_id FK) where product_category has a self-referencing parent_category_id for nested categories. Products also track stat…

**System answer:**
> 

**Sources retrieved (10):** `parent_chunk_business_glossary.md_0`, `parent_chunk_business_glossary.md_2`, `product.product_type`, `parent_chunk_business_glossary.md_3`, `product`, `Product`, `product_category`, `product.unit_of_measure`

---

### ✅ QA-003 — What is the structure of the sales order and how does it link to customers and products?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0000 | **Gate:** `proceed`

**Expected answer:**
> The sales_order table links to customer via customer_id FK and to warehouse via warehouse_id. It tracks order_number (UNIQUE), order_date, required_date, promised_date, subtotal/tax_amount/freight_amount/total_amount, and status (DRAFT/CONFIRMED/PICKED/SHIPPED/INVOICED/CANCELLED via CHECK). Priority…

**System answer:**
> 

**Sources retrieved (10):** `Sales Order`, `sales_order.customer_id`, `sales_order_line.product_id`, `sales_order`, `sales_order.required_date`, `sales_order.tax_amount`, `sales_order.warehouse_id`, `sales_order.status`

---

### ✅ QA-004 — How does the schema represent supplier information and their classification?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0000 | **Gate:** `proceed`

**Expected answer:**
> The supplier table stores supplier_id (PK), supplier_number (UNIQUE), supplier_name, supplier_type (MANUFACTURER/DISTRIBUTOR/SERVICE_PROVIDER via CHECK), tax_id, registration_date, and status (ACTIVE/INACTIVE/ON_HOLD/BLACKLISTED). Performance metrics are tracked: credit_rating (A/B/C/D), lead_time_d…

**System answer:**
> 

**Sources retrieved (9):** `Supplier`, `supplier.supplier_type`, `supplier`, `supplier.lead_time_days`, `supplier.quality_rating`, `supplier.credit_rating`, `supplier.tax_id`, `supplier.registration_date`

---

### ✅ QA-005 — What types of warehouses does the system support and how is storage organized?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0000 | **Gate:** `proceed`

**Expected answer:**
> The warehouse table defines four types via CHECK: COMPANY_OWNED, 3PL (third-party logistics), VIRTUAL, and TRANSIT. Each warehouse has capacity_cubic_meters and status (ACTIVE/INACTIVE/UNDER_MAINTENANCE). Storage is organized hierarchically: warehouse → warehouse_zone (types: BULK/PICK/STAGING/RECEI…

**System answer:**
> 

**Sources retrieved (11):** `parent_chunk_business_glossary.md_1`, `parent_chunk_business_glossary.md_4`, `warehouse.warehouse_type`, `Bin Location`, `Warehouse`, `warehouse`, `warehouse.created_at`, `warehouse.warehouse_code`

---

### ✅ QA-006 — How does the inventory tracking system work across the schema?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0000 | **Gate:** `proceed`

**Expected answer:**
> Inventory is tracked at two levels. The inventory_on_hand table records current stock per product/warehouse/bin/lot combination (UNIQUE constraint), with quantity_on_hand, quantity_allocated, and a computed quantity_available column (on_hand minus allocated). The inventory_transaction table logs all…

**System answer:**
> 

**Sources retrieved (11):** `inventory_transaction.transaction_number`, `inventory_transaction.bin_id`, `inventory_transaction→warehouse`, `inventory_transaction→product`, `inventory_transaction`, `Inventory Transaction`, `inventory_transaction.transaction_id`, `inventory_transaction.product_id`

---

### ✅ QA-007 — What is the Bill of Materials structure and how does it support multi-level product hierarchies?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0000 | **Gate:** `proceed`

**Expected answer:**
> The bill_of_materials table implements a many-to-many self-referencing relationship on the product table: parent_product_id (FK to product) contains component_product_id (FK to product) with a specified quantity and unit_of_measure. Components are classified as COMPONENT, PHANTOM, BYPRODUCT, or CO_P…

**System answer:**
> 

**Sources retrieved (10):** `Bill Of Materials`, `bill_of_materials→product`, `bill_of_materials.parent_product_id`, `bill_of_materials`, `bill_of_materials.scrap_percentage`, `bill_of_materials.bom_id`, `bill_of_materials.effective_start_date`, `bill_of_materials.effective_end_date`

---

### ✅ QA-008 — How are work orders structured and what do they track?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0000 | **Gate:** `proceed`

**Expected answer:**
> The work_order table references product_id (what to produce), production_line_id (where), and warehouse_id (inventory location). It tracks quantity_ordered, quantity_completed, quantity_scrapped, planned dates (start_date, required_date), actual dates (actual_start_date, actual_finish_date), status …

**System answer:**
> 

**Sources retrieved (8):** `parent_chunk_business_glossary.md_2`, `work_order.quantity_ordered`, `work_order`, `work_order.quantity_completed`, `work_order.actual_finish_date`, `work_order.product_id`, `work_order.required_date`, `work_order.quantity_scrapped`

---

### ✅ QA-009 — How does the quality management system work in the schema?

**Status:** GROUNDED  
**GT Coverage:** 67% | **Top Score:** 0.0000 | **Gate:** `proceed`

**Expected answer:**
> Quality is managed through three related tables. quality_inspection records inspections with types INCOMING/IN_PROCESS/FINAL/AUDIT, results PENDING/PASS/FAIL/CONDITIONAL_PASS, and links to quality_standard (types INTERNAL/ISO/ASTM/FDA/CE). Inspections track defects_found, sample_size, and batch_size…

**System answer:**
> 

**Sources retrieved (11):** `quality_inspection→quality_standard`, `quality_inspection→product`, `quality_standard.status`, `supplier.quality_rating`, `quality_standard`, `Quality Standard`, `quality_standard.standard_id`, `quality_standard.standard_type`

---

### ✅ QA-010 — What is the complete invoice lifecycle and how are invoices linked to orders and payments?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0000 | **Gate:** `proceed`

**Expected answer:**
> The invoice table supports four types via CHECK: SALES, PURCHASE, CREDIT_MEMO, and DEBIT_MEMO. Invoices link to customer_id and optionally order_id (FK to sales_order). They track subtotal/tax_amount/total_amount/amount_paid/balance_due and status (DRAFT/POSTED/PAID/OVERDUE/VOID). Each invoice has i…

**System answer:**
> 

**Sources retrieved (11):** `invoice.order_id`, `payment.invoice_id`, `invoice_line.invoice_line_id`, `Invoice`, `invoice`, `invoice.invoice_id`, `invoice.due_date`, `invoice.tax_amount`

---

### ✅ QA-011 — How does the procurement process flow from purchase order to receipt?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0000 | **Gate:** `proceed`

**Expected answer:**
> Purchase orders (purchase_order) link to supplier_id FK and warehouse_id, with status lifecycle DRAFT/SUBMITTED/ACKNOWLEDGED/PARTIAL/RECEIVED/CLOSED/CANCELLED. Each PO has purchase_order_line items referencing products with quantity tracking (ordered/received/invoiced) and supplier_part_number. When…

**System answer:**
> 

**Sources retrieved (9):** `Purchase Receipt`, `purchase_receipt.po_id`, `purchase_receipt`, `purchase_order`, `purchase_receipt.receipt_date`, `purchase_receipt.warehouse_id`, `purchase_receipt.receipt_number`, `purchase_receipt.created_at`

---

### ✅ QA-012 — How does the general ledger and accounting system work?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0000 | **Gate:** `proceed`

**Expected answer:**
> The GL is built on account_type (DEBIT or CREDIT balance_type), general_ledger_account (with hierarchical parent_account_id self-reference and status ACTIVE/INACTIVE), and accounting_period (with fiscal_year, start/end dates, and is_closed flag). Journal entries (journal_entry) reference a period, h…

**System answer:**
> 

**Sources retrieved (11):** `General Ledger Account`, `general_ledger_account→account_type`, `general_ledger_account→general_ledger_account`, `general_ledger_account.account_number`, `general_ledger_account`, `general_ledger_account.status`, `general_ledger_account.created_at`, `general_ledger_account.account_id`

---

### ✅ QA-013 — How are accounts receivable and accounts payable tracked?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0000 | **Gate:** `proceed`

**Expected answer:**
> Accounts receivable (accounts_receivable) links to customer_id and invoice_id, tracking amount_original, amount_due, due_date, and a computed days_overdue column. Status values are CURRENT/DUE/OVERDUE/COLLECTION/WRITE_OFF, with collection_status and next_action_date for collections workflow. Account…

**System answer:**
> 

**Sources retrieved (10):** `parent_chunk_business_glossary.md_1`, `accounts_payable→invoice`, `Accounts Payable`, `accounts_payable.invoice_id`, `accounts_payable`, `accounts_payable.status`, `accounts_payable.payment_priority`, `accounts_payable.amount_original`

---

### ✅ QA-014 — How is the employee and organizational structure represented?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0000 | **Gate:** `proceed`

**Expected answer:**
> The department table has hierarchical parent_department_id self-reference with status ACTIVE/INACTIVE. Positions (position table) belong to departments via department_id FK, with grade_level, salary range (min/max), and FLSA status (EXEMPT/NON_EXEMPT). Employees reference department_id, position_id,…

**System answer:**
> 

**Sources retrieved (9):** `parent_chunk_business_glossary.md_2`, `employee.employee_type`, `Employee`, `employee`, `employee.first_name`, `employee.manager_id`, `employee.department_id`, `employee.termination_date`

---

### ✅ QA-015 — How does the shipment and logistics system work?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0000 | **Gate:** `proceed`

**Expected answer:**
> Carriers (carrier table) are classified by type: LTL/FTL/PARCEL/AIR/OCEAN/RAIL with rating (0-5). Shipping routes define paths between warehouses (origin_location_id, destination_location_id both FK to warehouse) with distance_km, estimated_hours, and cost_per_km. Shipments reference origin/destinat…

**System answer:**
> 

**Sources retrieved (10):** `shipment→shipping_route`, `shipment→warehouse`, `shipment_line.shipment_id`, `shipment_line`, `Order Line`, `shipment`, `shipment_line.description`, `shipment_line.shipment_line_id`

---

### ✅ QA-016 — How does the project management module work?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0000 | **Gate:** `proceed`

**Expected answer:**
> Projects link to customer_id (for customer-facing projects) and project_manager_id (FK to employee). Project types are CUSTOMER/INTERNAL/R&D/CAPITAL with status PLANNING/ACTIVE/ON_HOLD/COMPLETED/CANCELLED and priority levels. Projects track budget_amount vs actual_cost. Project tasks (project_task) …

**System answer:**
> 

**Sources retrieved (10):** `project→employee`, `project_task→project`, `project.project_manager_id`, `project`, `project.status`, `project.description`, `project.priority`, `project.start_date`

---

### ✅ QA-017 — How does the system handle user authentication, roles, and permissions?

**Status:** GROUNDED  
**GT Coverage:** 67% | **Top Score:** 0.0000 | **Gate:** `proceed`

**Expected answer:**
> The app_user table links to employee_id, customer_id, or supplier_id depending on user_type (EMPLOYEE/CUSTOMER/SUPPLIER/ADMIN). Users have status ACTIVE/INACTIVE/LOCKED/PENDING with failed_login_attempts tracking. Roles (role table) are typed as SYSTEM/BUSINESS/CUSTOM with ACTIVE/INACTIVE status. Th…

**System answer:**
> 

**Sources retrieved (9):** `parent_chunk_business_glossary.md_4`, `user_role.user_id`, `user_role`, `app_user`, `user_role.expiry_date`, `user_role.status`, `user_role.assigned_date`, `Unknown`

---

### ✅ QA-018 — What is the complete path from a customer placing an order to the product being shipped?

**Status:** GROUNDED  
**GT Coverage:** 75% | **Top Score:** 0.0000 | **Gate:** `proceed`

**Expected answer:**
> The order-to-ship path traverses: customer → sales_order (via customer_id FK) → sales_order_line (via order_id FK) → product (via product_id FK). For fulfillment: sales_order references warehouse_id for the fulfillment location. Inventory is checked via inventory_on_hand (product_id + warehouse_id).…

**System answer:**
> 

**Sources retrieved (12):** `sales_order_line.quantity_shipped`, `Order Line`, `Sales Order`, `purchase_order_line.product_id`, `Customer`, `product`, `shipment_line.product_id`, `customer`

---

### ✅ QA-019 — How does the schema support supplier contracts and their relationship to purchase orders?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0000 | **Gate:** `proceed`

**Expected answer:**
> The supplier_contract table links to supplier_id FK, with contract_type (FIXED_PRICE/COST_PLUS/RATE_BASED/FRAMEWORK), start/end dates, auto_renew flag, payment_terms, total_value, and status (DRAFT/ACTIVE/EXPIRED/TERMINATED). Purchase orders independently link to the same supplier via supplier_id FK…

**System answer:**
> 

**Sources retrieved (11):** `Purchase Order Line`, `supplier_contract.contract_type`, `Supplier`, `supplier_contract→supplier`, `Supplier Contract`, `supplier_contract`, `supplier`, `supplier_contract.created_at`

---

### ✅ QA-020 — What self-referencing hierarchies exist in the schema?

**Status:** GROUNDED  
**GT Coverage:** 80% | **Top Score:** 0.0000 | **Gate:** `proceed`

**Expected answer:**
> The schema has five self-referencing hierarchies: (1) product_category.parent_category_id → product_category.category_id for nested product classifications; (2) general_ledger_account.parent_account_id → general_ledger_account.account_id for chart of accounts hierarchy; (3) department.parent_departm…

**System answer:**
> 

**Sources retrieved (12):** `parent_chunk_business_glossary.md_2`, `parent_chunk_business_glossary.md_1`, `Department`, `Order Line`, `Invoice Line`, `department`, `department.department_name`, `department.manager_id`

---

### ✅ QA-021 — How does the price list system work for products?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0000 | **Gate:** `proceed`

**Expected answer:**
> The price_list table defines named price lists with currency, effective_date, expiration_date, and status. The product_price junction table links products to price lists with price, minimum_quantity (for volume pricing), discount_percentage, and effective_date. A UNIQUE constraint on (product_id, pr…

**System answer:**
> 

**Sources retrieved (11):** `Price List`, `product_price.price_list_id`, `product_price→price_list`, `price_list.price_list_id`, `price_list`, `Unknown`, `price_list.currency`, `price_list.expiration_date`

---

### ✅ QA-022 — What CHECK constraints on status columns exist across the major tables?

**Status:** GROUNDED  
**GT Coverage:** 18% | **Top Score:** 0.0000 | **Gate:** `proceed`

**Expected answer:**
> Key status CHECK constraints include: customer (ACTIVE/INACTIVE/SUSPENDED), product (ACTIVE/DISCONTINUED/PHASE_OUT), sales_order (DRAFT/CONFIRMED/PICKED/SHIPPED/INVOICED/CANCELLED), purchase_order (DRAFT/SUBMITTED/ACKNOWLEDGED/PARTIAL/RECEIVED/CLOSED/CANCELLED), work_order (DRAFT/RELEASED/IN_PROGRES…

**System answer:**
> 

**Sources retrieved (12):** `parent_chunk_business_glossary.md_4`, `quality_inspection.status`, `customer.status`, `quality_standard.status`, `position.status`, `customer_type.credit_check_required`, `position.flsa_status`, `position`

---

### ✅ QA-023 — How does the stock transfer process work between warehouses?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0000 | **Gate:** `proceed`

**Expected answer:**
> Stock transfers use the stock_transfer table with from_warehouse_id and to_warehouse_id (both FK to warehouse), transfer_date, shipment_method, tracking_number, and status (DRAFT/PICKED/SHIPPED/RECEIVED/CANCELLED). Individual items are tracked via stock_transfer_line with from_bin_id and to_bin_id (…

**System answer:**
> 

**Sources retrieved (10):** `Stock Transfer`, `stock_transfer.to_warehouse_id`, `stock_transfer→warehouse`, `stock_transfer`, `stock_transfer.transfer_number`, `stock_transfer.transfer_id`, `stock_transfer.required_date`, `stock_transfer.tracking_number`

---

### ✅ QA-024 — How are production lines defined and what types exist?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0000 | **Gate:** `proceed`

**Expected answer:**
> The production_line table defines manufacturing resources with line_code (UNIQUE), line_name, line_type (ASSEMBLY/DISCRETE/PROCESS/MIXING via CHECK), location_id (FK to warehouse for the physical location), capacity_per_hour, setup_time_minutes, and status (ACTIVE/MAINTENANCE/INACTIVE). Production l…

**System answer:**
> 

**Sources retrieved (8):** `parent_chunk_business_glossary.md_2`, `Production Resources`, `production_line.line_type`, `production_line`, `production_line.status`, `production_line.setup_time_minutes`, `production_line.location_id`, `production_line.capacity_per_hour`

---

### ✅ QA-025 — How does the budget system integrate with the financial accounts?

**Status:** GROUNDED  
**GT Coverage:** 50% | **Top Score:** 0.0000 | **Gate:** `proceed`

**Expected answer:**
> The budget table links to both department_id and account_id (FK to general_ledger_account). It tracks budget_type (OPERATING/CAPITAL/PROJECT), fiscal_year, budgeted_amount, actual_amount, and a computed variance column (budgeted minus actual). Budget status follows DRAFT/APPROVED/ACTIVE/CLOSED. This…

**System answer:**
> 

**Sources retrieved (12):** `parent_chunk_business_glossary.md_1`, `parent_chunk_business_glossary.md_4`, `General Ledger Account`, `accounting_period.fiscal_year`, `parent_chunk_business_glossary.md_2`, `Journal Entry`, `Accounts Payable`, `general_ledger_account`

---

### ✅ QA-026 — What computed/generated columns exist in the schema?

**Status:** GROUNDED  
**GT Coverage:** 33% | **Top Score:** 0.0000 | **Gate:** `proceed`

**Expected answer:**
> The schema has three computed columns using GENERATED ALWAYS AS: (1) inventory_on_hand.quantity_available = quantity_on_hand - quantity_allocated; (2) accounts_receivable.days_overdue = DATEDIFF(CURRENT_DATE, due_date); (3) budget.variance = budgeted_amount - actual_amount. All are STORED (materiali…

**System answer:**
> 

**Sources retrieved (12):** `parent_chunk_business_glossary.md_4`, `Invoice`, `Budgeted Amount`, `Invoice Line`, `Purchase Receipt`, `project`, `customer`, `employee`

---

### ✅ QA-027 — How are customer addresses and contacts structured?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0000 | **Gate:** `proceed`

**Expected answer:**
> Customer addresses are stored in customer_address with address_type (BILLING/SHIPPING/BOTH via CHECK), full address fields (line1, line2, city, state, postal_code, country_code), and is_default flag. The customer_id FK has ON DELETE CASCADE. Customer contacts are in customer_contact with contact_nam…

**System answer:**
> 

**Sources retrieved (10):** `customer_address.customer_id`, `customer_address→customer`, `customer_contact.is_primary`, `customer_address`, `customer`, `customer_address.address_id`, `customer_address.is_default`, `customer_address.postal_code`

---

### ✅ QA-028 — What CASCADE rules exist in the schema and what tables use them?

**Status:** GROUNDED  
**GT Coverage:** 0% | **Top Score:** 0.0000 | **Gate:** `proceed`

**Expected answer:**
> CASCADE rules (ON DELETE CASCADE, ON UPDATE CASCADE) are defined in foreign key constraint syntax within the DDL. These details are typically on child tables like customer_address, customer_contact, sales_order_line, and purchase_order_line. However, specific CASCADE declarations may not be surfaced…

**System answer:**
> 

**Sources retrieved (11):** `shipping_route→warehouse`, `inventory_transaction→warehouse`, `shipment→warehouse`, `quality_standard.standard_code`, `quality_standard`, `Quality Standard`, `quality_standard.standard_id`, `quality_standard.standard_type`

---

### ✅ QA-029 — How does the schema link quality inspections to their source documents?

**Status:** GROUNDED  
**GT Coverage:** 33% | **Top Score:** 0.0000 | **Gate:** `proceed`

**Expected answer:**
> Quality inspections use a polymorphic reference pattern: reference_type (VARCHAR) identifies the source table (e.g., 'purchase_receipt', 'work_order') and reference_id (INT) stores the primary key of that source record. The inspection also directly references product_id and warehouse_id via foreign …

**System answer:**
> 

**Sources retrieved (9):** `quality_inspection.reference_type`, `Quality Inspection`, `quality_inspection`, `quality_standard`, `quality_inspection.result`, `quality_inspection.created_at`, `quality_inspection.status`, `quality_inspection.inspection_id`

---

### ✅ QA-030 — How does the journal entry enforce double-entry bookkeeping?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0000 | **Gate:** `proceed`

**Expected answer:**
> The journal_entry table requires total_debit and total_credit columns to be present (both NOT NULL DECIMAL 15,2). Journal_entry_line items each reference a general_ledger_account and have a CHECK constraint ensuring exactly one of debit_amount or credit_amount is positive: CHECK ((debit_amount > 0 A…

**System answer:**
> 

**Sources retrieved (11):** `Journal Entry`, `parent_chunk_business_glossary.md_1`, `journal_entry→accounting_period`, `journal_entry_line→journal_entry`, `journal_entry.entry_type`, `journal_entry`, `journal_entry.created_by`, `journal_entry.entry_date`

---

### ✅ QA-031 — What types of non-conformance reports exist and what is their lifecycle?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0000 | **Gate:** `proceed`

**Expected answer:**
> Non-conformance reports (NCRs) have four types via CHECK: PRODUCT, PROCESS, DOCUMENTATION, and SUPPLIER. Severity is classified as MINOR/MAJOR/CRITICAL. The status lifecycle is OPEN → IN_PROGRESS → CLOSED → VERIFIED. NCRs track root_cause, corrective_action, and preventive_action (all TEXT fields) f…

**System answer:**
> 

**Sources retrieved (9):** `non_conformance_report.reference_type`, `parent_chunk_business_glossary.md_3`, `non_conformance_report`, `Non Conformance Report`, `product`, `non_conformance_report.root_cause`, `non_conformance_report.ncr_type`, `non_conformance_report.created_at`

---

### ✅ QA-032 — How does the purchase receipt track rejected quantities and lot information?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0000 | **Gate:** `proceed`

**Expected answer:**
> The purchase_receipt_line table tracks three quantity measures: quantity_ordered, quantity_received, and quantity_rejected. When quantity_rejected > 0, materials failed inspection. Each receipt line also records lot_number (for lot traceability), expiration_date (for perishable items), location_id (…

**System answer:**
> 

**Sources retrieved (10):** `purchase_receipt_line.quantity_rejected`, `parent_chunk_business_glossary.md_0`, `Purchase Receipt`, `purchase_receipt.received_by`, `purchase_receipt.tracking_number`, `purchase_receipt`, `purchase_receipt.receipt_date`, `purchase_receipt.receipt_id`

---

### ✅ QA-033 — What UNIQUE constraints exist across the schema and what do they enforce?

**Status:** GROUNDED  
**GT Coverage:** 25% | **Top Score:** 0.0000 | **Gate:** `proceed`

**Expected answer:**
> UNIQUE constraints exist on business identifier columns (customer.customer_number, product.product_number, supplier.supplier_number, invoice.invoice_number) and composite keys. However, constraint metadata (UNIQUE, CHECK, etc.) may not surface through chunk-based retrieval unless the constraint DDL …

**System answer:**
> 

**Sources retrieved (12):** `Production Schedule`, `production_schedule.actual_end`, `parent_chunk_business_glossary.md_4`, `parent_chunk_business_glossary.md_2`, `Unknown`, `production_schedule`, `production_line`, `work_order`

---

### ✅ QA-034 — How does the schema handle the relationship between employees, departments, and projects?

**Status:** GROUNDED  
**GT Coverage:** 50% | **Top Score:** 0.0000 | **Gate:** `proceed`

**Expected answer:**
> Employees belong to departments via department_id FK and hold positions via position_id FK. Positions also reference department_id, creating a redundant but verifiable link. Employee.manager_id (self-referencing FK) creates reporting chains. Projects link to project_manager_id (FK to employee) and o…

**System answer:**
> 

**Sources retrieved (12):** `parent_chunk_business_glossary.md_2`, `parent_chunk_business_glossary.md_3`, `project.description`, `parent_chunk_business_glossary.md_4`, `parent_chunk_business_glossary.md_0`, `project`, `Budgeted Amount`, `customer`

---

### ✅ QA-035 — What is the relationship between sales orders, invoices, and payments?

**Status:** GROUNDED  
**GT Coverage:** 80% | **Top Score:** 0.0000 | **Gate:** `proceed`

**Expected answer:**
> Sales orders are invoiced by creating invoice records with order_id FK referencing sales_order. Invoice line items (invoice_line) can link back to specific sales_order_line items via order_line_id FK. Payments reference invoice_id FK to settle invoices. The invoice tracks amount_paid and balance_due…

**System answer:**
> 

**Sources retrieved (12):** `parent_chunk_business_glossary.md_0`, `invoice→sales_order`, `invoice_line→sales_order_line`, `sales_order_line.quantity_invoiced`, `payment.invoice_id`, `sales_order_line`, `Sales Order`, `sales_order`

---

### ✅ QA-036 — What types of inventory transactions does the system track?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0000 | **Gate:** `proceed`

**Expected answer:**
> The inventory_transaction table supports seven transaction types via CHECK constraint: RECEIPT (goods received from suppliers), ISSUE (materials consumed by production or shipped to customers), TRANSFER (movement between warehouses/bins), ADJUSTMENT (corrections to inventory counts), CYCLE_COUNT (pe…

**System answer:**
> 

**Sources retrieved (10):** `parent_chunk_business_glossary.md_1`, `parent_chunk_business_glossary.md_4`, `Inventory Transaction`, `inventory_transaction.transaction_type`, `inventory_transaction`, `inventory_transaction.transaction_id`, `inventory_transaction.transaction_number`, `inventory_transaction.unit_cost`

---

### ✅ QA-037 — How does the BOM component type affect manufacturing?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0000 | **Gate:** `proceed`

**Expected answer:**
> The bill_of_materials table classifies components into four types via CHECK: COMPONENT (standard parts consumed in production), PHANTOM (sub-assemblies that are not stocked — their components are consumed directly), BYPRODUCT (secondary outputs of the production process), and CO_PRODUCT (additional …

**System answer:**
> 

**Sources retrieved (9):** `bill_of_materials.component_type`, `Bill Of Materials`, `Product`, `Production Resources`, `bill_of_materials`, `product`, `bill_of_materials.scrap_percentage`, `bill_of_materials.effective_start_date`

---

### ✅ QA-038 — How does the audit log track system events and changes?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0000 | **Gate:** `proceed`

**Expected answer:**
> The audit_log table records every significant system event with event_type, user_id (FK to app_user), entity_type (which table was affected), entity_id (which record), and action (CREATE/READ/UPDATE/DELETE/LOGIN/LOGOUT/EXPORT via CHECK). For data changes, old_value and new_value are stored as JSON. …

**System answer:**
> 

**Sources retrieved (9):** `audit_log.event_type`, `Audit Log`, `parent_chunk_business_glossary.md_4`, `audit_log`, `audit_log.new_value`, `audit_log.user_agent`, `audit_log.old_value`, `audit_log.action`

---

### ✅ QA-039 — What are the different address types supported across the schema?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0000 | **Gate:** `proceed`

**Expected answer:**
> Customer addresses support three types: BILLING, SHIPPING, and BOTH. Supplier addresses support four types: MAIN, BILLING, SHIPPING, and RETURN. Both customer_address and supplier_address have is_default/is_primary flags and cascade delete from their parent. The warehouse table stores location_addre…

**System answer:**
> 

**Sources retrieved (11):** `parent_chunk_business_glossary.md_4`, `supplier_address.address_type`, `customer_address.address_type`, `Location Address`, `customer_address`, `customer_address.address_id`, `customer_address.is_default`, `customer_address.postal_code`

---

### ✅ QA-040 — How would the schema support tracing a product from purchase receipt to customer shipment?

**Status:** GROUNDED  
**GT Coverage:** 50% | **Top Score:** 0.0000 | **Gate:** `proceed`

**Expected answer:**
> The full traceability path is: purchase_receipt (inbound from supplier) → purchase_receipt_line (with lot_number) → inventory_on_hand (lot_number at warehouse/bin) → inventory_transaction (RECEIPT type logs the inbound). For production: work_order_material records material consumption → work_order t…

**System answer:**
> 

**Sources retrieved (9):** `purchase_receipt.tracking_number`, `Purchase Receipt`, `purchase_receipt`, `purchase_receipt.receipt_date`, `purchase_receipt.receipt_id`, `purchase_receipt.warehouse_id`, `purchase_receipt.receipt_number`, `purchase_receipt.created_at`

---

### ✅ QA-041 — How are supplier addresses and contacts structured compared to customer addresses?

**Status:** GROUNDED  
**GT Coverage:** 50% | **Top Score:** 0.0000 | **Gate:** `proceed`

**Expected answer:**
> Both follow the same pattern: parent entity → address table + contact table, both with ON DELETE CASCADE. Supplier_address has address_type MAIN/BILLING/SHIPPING/RETURN (vs customer's BILLING/SHIPPING/BOTH) and uses is_primary flag (vs customer_address's is_default). Supplier_contact mirrors custome…

**System answer:**
> 

**Sources retrieved (8):** `Master Data`, `supplier_address.address_type`, `supplier_address`, `supplier`, `supplier_address.country_code`, `supplier_address.postal_code`, `supplier_address.city`, `supplier_address.address_line1`

---

### ✅ QA-042 — Does the schema track employee compensation history?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0000 | **Gate:** `proceed`

**Expected answer:**
> The employee table has current annual_salary and hourly_rate columns and the position table defines min_salary and max_salary ranges. However, there is no compensation history table in the schema — salary changes would overwrite the current values without preserving history. The only historical trac…

**System answer:**
> 

**Sources retrieved (9):** `parent_chunk_business_glossary.md_2`, `employee.annual_salary`, `Employee`, `employee`, `employee.first_name`, `employee.manager_id`, `employee.department_id`, `employee.position_id`

---

### ✅ QA-043 — How does the shipping route connect two warehouses through a carrier?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0000 | **Gate:** `proceed`

**Expected answer:**
> The shipping_route table has origin_location_id and destination_location_id (both FK to warehouse), carrier_id (FK to carrier), plus route_code (UNIQUE), distance_km, estimated_hours, cost_per_km, and service_level. Shipments reference route_id FK to use a predefined route, plus independently refere…

**System answer:**
> 

**Sources retrieved (5):** `shipping_route→carrier`, `parent_chunk_business_glossary.md_3`, `shipping_route→warehouse`, `shipment→shipping_route`, `shipment→carrier`

---

### ✅ QA-044 — What is the production scheduling model and how does it relate to work orders?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0000 | **Gate:** `proceed`

**Expected answer:**
> The production_schedule table links work_order_id (FK to work_order) to production_line_id (FK to production_line) with scheduled_start and scheduled_end timestamps, plus actual_start and actual_end for tracking real execution. Status progresses SCHEDULED → RUNNING → COMPLETED (or CANCELLED). Priori…

**System answer:**
> 

**Sources retrieved (10):** `production_schedule.work_order_id`, `parent_chunk_business_glossary.md_2`, `Production Schedule`, `production_schedule→work_order`, `production_schedule`, `production_line`, `work_order`, `production_schedule.priority`

---

### ✅ QA-045 — How does the invoice line link back to both sales order lines and products?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0000 | **Gate:** `proceed`

**Expected answer:**
> Invoice_line references invoice_id FK (parent invoice), product_id FK (what was invoiced), and optionally order_line_id FK (back-reference to the specific sales_order_line). This three-way linkage supports: invoice → sales_order (via invoice.order_id), invoice_line → product (direct), and invoice_li…

**System answer:**
> 

**Sources retrieved (9):** `invoice_line.product_id`, `sales_order_line.quantity_invoiced`, `sales_order_line`, `sales_order_line.line_id`, `sales_order_line.quantity_shipped`, `sales_order_line.discount_percentage`, `sales_order_line.quantity_ordered`, `sales_order_line.line_total`

---

### ✅ QA-046 — Is there a returns or reverse logistics capability in the schema?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0000 | **Gate:** `proceed`

**Expected answer:**
> Returns are partially supported: payment_type includes REFUND, invoice_type includes CREDIT_MEMO, shipment_type includes RETURN, and inventory_transaction has a RETURN transaction type. However, there is no dedicated returns management table (e.g., return_authorization or RMA). Returns would be trac…

**System answer:**
> 

**Sources retrieved (12):** `parent_chunk_business_glossary.md_3`, `parent_chunk_business_glossary.md_1`, `Purchase Receipt`, `Order Line`, `Warehouse Zone`, `shipment_line`, `product`, `shipment`

---

### ✅ QA-047 — How many tables are in each business domain and what are they?

**Status:** GROUNDED  
**GT Coverage:** N/A | **Top Score:** 0.0000 | **Gate:** `proceed`

**Expected answer:**
> A complete table-by-domain breakdown requires schema-wide overview not available from individual chunk retrieval. From retrieved context, identifiable domains include Sales & Customer Management (customer, product, sales_order, etc.), Finance (invoice, payment, journal_entry, gl_account), HR (employ…

**System answer:**
> 

**Sources retrieved (12):** `sales_order.tax_amount`, `Accounting Period`, `Sales Order`, `Warehouse Zone`, `Master Data`, `sales_order`, `customer`, `sales_order.required_date`

---

### ✅ QA-048 — How does the accounting period system work?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0000 | **Gate:** `proceed`

**Expected answer:**
> The accounting_period table defines fiscal periods with period_code (UNIQUE), period_name, start_date, end_date, fiscal_year, and is_closed flag. A UNIQUE constraint on (fiscal_year, period_code) prevents duplicate periods within a year. Journal entries reference period_id FK to ensure postings land…

**System answer:**
> 

**Sources retrieved (9):** `journal_entry→accounting_period`, `accounting_period.period_id`, `accounting_period`, `Accounting Period`, `accounting_period.is_closed`, `accounting_period.closed_at`, `accounting_period.period_code`, `accounting_period.end_date`

---

### ✅ QA-049 — How do work order materials track material consumption against BOM requirements?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0000 | **Gate:** `proceed`

**Expected answer:**
> The work_order_material table links work_order_id FK to product_id FK (the material), with quantity_required (from BOM calculation) and quantity_issued (actually consumed). Status tracks progress: PENDING/ISSUED/PARTIAL/COMPLETE. Materials are sourced from specific bins via bin_id FK to bin_location…

**System answer:**
> 

**Sources retrieved (8):** `work_order_material.quantity_required`, `work_order_material`, `Bill Of Materials`, `work_order_material.unit_cost`, `work_order_material.quantity_issued`, `work_order_material.status`, `work_order`, `product`

---

### ✅ QA-050 — Does the schema support multi-currency transactions?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0000 | **Gate:** `proceed`

**Expected answer:**
> Multiple tables have currency columns defaulting to USD: customer.currency, sales_order.currency, invoice.currency, payment.currency, purchase_order.currency, supplier.currency, supplier_contract.currency, general_ledger_account.currency, and price_list.currency. However, there is no currency exchan…

**System answer:**
> 

**Sources retrieved (12):** `parent_chunk_business_glossary.md_1`, `customer.currency`, `parent_chunk_business_glossary.md_4`, `General Ledger Account`, `payment.currency`, `customer`, `Customer`, `customer_type`

---

### ✅ QA-051 — How does the schema handle product storage requirements for hazardous or temperature-sensitive items?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0000 | **Gate:** `proceed`

**Expected answer:**
> Products have three relevant fields: hazardous (BOOLEAN, default FALSE), storage_temperature_min (DECIMAL), and storage_temperature_max (DECIMAL). Warehouse zones have a temperature_controlled (BOOLEAN) flag. When a product requires temperature control, it should be stored in bins within temperature…

**System answer:**
> 

**Sources retrieved (10):** `product.storage_temperature_max`, `Bin Location`, `product.hazardous`, `work_order_material.quantity_required`, `product`, `Product`, `product_category`, `product.unit_of_measure`

---

### ✅ QA-052 — What polymorphic reference patterns exist in the schema?

**Status:** GROUNDED  
**GT Coverage:** 29% | **Top Score:** 0.0000 | **Gate:** `proceed`

**Expected answer:**
> The schema uses reference_type + reference_id polymorphic patterns in several tables: (1) quality_inspection — reference_type identifies the source (purchase_receipt, work_order) and reference_id stores the ID; (2) inventory_transaction — reference_type identifies the source document (sales_order, p…

**System answer:**
> 

**Sources retrieved (5):** `department→department`, `employee→position`, `employee→department`, `position→department`, `shipment→warehouse`

---

### ✅ QA-053 — Is there a customer loyalty or rewards program in the schema?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0000 | **Gate:** `proceed`

**Expected answer:**
> No, the schema does not contain any tables or columns for customer loyalty programs, reward points, or promotional campaigns. Customer classification is limited to customer_type_id (FK to customer_type), credit_score, and is_preferred-style fields do not exist. The customer table focuses on commerci…

**System answer:**
> 

**Sources retrieved (12):** `project→customer`, `payment→customer`, `customer→customer_type`, `Customer`, `customer.currency`, `customer`, `customer_type`, `customer.tax_id`

---

### ✅ QA-054 — How does the schema support three-way matching in procurement?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0000 | **Gate:** `proceed`

**Expected answer:**
> Three-way matching (PO → receipt → invoice) is supported through linked tables: purchase_order_line tracks quantity_ordered, quantity_received, and quantity_invoiced. Purchase_receipt_line links back to po_line_id FK. Invoice can be linked to purchase activities via invoice_type = 'PURCHASE' and acc…

**System answer:**
> 

**Sources retrieved (12):** `Supplier`, `parent_chunk_business_glossary.md_0`, `parent_chunk_business_glossary.md_4`, `parent_chunk_business_glossary.md_1`, `Purchase Receipt`, `supplier`, `supplier.supplier_type`, `supplier.lead_time_days`

---

### ✅ QA-055 — What indexes exist for performance optimization and which tables have the most?

**Status:** GROUNDED  
**GT Coverage:** N/A | **Top Score:** 0.0000 | **Gate:** `proceed`

**Expected answer:**
> Index definitions (CREATE INDEX statements) are DDL metadata that may not surface through chunk-based retrieval unless explicitly included in retrieved context. The schema likely defines indexes on foreign key columns and frequently-queried fields, but specific index names, compositions, and per-tab…

**System answer:**
> 

**Sources retrieved (12):** `parent_chunk_business_glossary.md_4`, `parent_chunk_business_glossary.md_2`, `parent_chunk_business_glossary.md_3`, `parent_chunk_business_glossary.md_0`, `Master Data`, `supplier_address`, `supplier`, `supplier_address.country_code`

---

## Anomalies & Observations

No anomalies detected. All questions grounded with acceptable RAGAS scores.
