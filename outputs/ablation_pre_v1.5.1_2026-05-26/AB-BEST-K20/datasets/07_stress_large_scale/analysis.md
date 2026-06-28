# AB-BEST-K20 — 07_stress_large_scale — Run Analysis

**Timestamp:** 2026-05-07 14:20:55  
**Run tag:** `run-20260507_152820`

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
| Triplets extracted | 138 |
| Entities resolved | 108 |
| Tables parsed | 58 |
| Tables completed | 58 |

## Query Evaluation Summary

| Metric | Value |
|--------|-------|
| Questions | 55 |
| Grounded | **55/55 (100%)** |
| Avg GT Coverage | 92% |
| Avg Top Score | 0.7274 |
| Avg Chunk Count | 40.9 |
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

**Sources retrieved (12):** `CUSTOMER.CREDIT_LIMIT`, `CUSTOMER.WEBSITE`, `CUSTOMER.CURRENCY`, `CUSTOMER.CUSTOMER_ID`, `CUSTOMER.CUSTOMER_TYPE_ID`, `parent_chunk_business_glossary.md_4`, `parent_chunk_business_glossary.md_1`, `parent_chunk_business_glossary.md_3`

---

### ✅ QA-002 — How does the schema classify different types of products?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0000 | **Gate:** `proceed`

**Expected answer:**
> Products are classified by product_type via CHECK constraint: FINISHED_GOOD, RAW_MATERIAL, SERVICE, or CONSUMABLE. They also belong to a hierarchical product_category (via category_id FK) where product_category has a self-referencing parent_category_id for nested categories. Products also track stat…

**System answer:**
> 

**Sources retrieved (12):** `parent_chunk_business_glossary.md_0`, `Product`, `Purchase Order`, `Commercial Document`, `parent_chunk_business_glossary.md_2`, `parent_chunk_business_glossary.md_4`, `PRODUCT.PRODUCT_TYPE`, `PRODUCT.COST`

---

### ✅ QA-003 — What is the structure of the sales order and how does it link to customers and products?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0000 | **Gate:** `proceed`

**Expected answer:**
> The sales_order table links to customer via customer_id FK and to warehouse via warehouse_id. It tracks order_number (UNIQUE), order_date, required_date, promised_date, subtotal/tax_amount/freight_amount/total_amount, and status (DRAFT/CONFIRMED/PICKED/SHIPPED/INVOICED/CANCELLED via CHECK). Priority…

**System answer:**
> 

**Sources retrieved (12):** `parent_chunk_business_glossary.md_0`, `parent_chunk_business_glossary.md_3`, `Commercial Document`, `parent_chunk_business_glossary.md_2`, `Sales Order`, `SALES_ORDER.CUSTOMER_ID`, `SALES_ORDER.ORDER_NUMBER`, `SALES_ORDER.SALES_REP_ID`

---

### ✅ QA-004 — How does the schema represent supplier information and their classification?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0000 | **Gate:** `proceed`

**Expected answer:**
> The supplier table stores supplier_id (PK), supplier_number (UNIQUE), supplier_name, supplier_type (MANUFACTURER/DISTRIBUTOR/SERVICE_PROVIDER via CHECK), tax_id, registration_date, and status (ACTIVE/INACTIVE/ON_HOLD/BLACKLISTED). Performance metrics are tracked: credit_rating (A/B/C/D), lead_time_d…

**System answer:**
> 

**Sources retrieved (12):** `Supplier Contract`, `parent_chunk_business_glossary.md_0`, `parent_chunk_business_glossary.md_4`, `SUPPLIER.SUPPLIER_TYPE`, `SUPPLIER.STATUS`, `SUPPLIER.SUPPLIER_NAME`, `SUPPLIER.SUPPLIER_ID`, `SUPPLIER.SUPPLIER_NUMBER`

---

### ✅ QA-005 — What types of warehouses does the system support and how is storage organized?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0000 | **Gate:** `proceed`

**Expected answer:**
> The warehouse table defines four types via CHECK: COMPANY_OWNED, 3PL (third-party logistics), VIRTUAL, and TRANSIT. Each warehouse has capacity_cubic_meters and status (ACTIVE/INACTIVE/UNDER_MAINTENANCE). Storage is organized hierarchically: warehouse → warehouse_zone (types: BULK/PICK/STAGING/RECEI…

**System answer:**
> 

**Sources retrieved (12):** `parent_chunk_business_glossary.md_1`, `parent_chunk_business_glossary.md_4`, `WAREHOUSE.WAREHOUSE_TYPE`, `Bin Location`, `WAREHOUSE.STATUS`, `WAREHOUSE.STATE`, `BIN_LOCATION.BIN_TYPE`, `BIN_LOCATION.STATUS`

---

### ✅ QA-006 — How does the inventory tracking system work across the schema?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0000 | **Gate:** `proceed`

**Expected answer:**
> Inventory is tracked at two levels. The inventory_on_hand table records current stock per product/warehouse/bin/lot combination (UNIQUE constraint), with quantity_on_hand, quantity_allocated, and a computed quantity_available column (on_hand minus allocated). The inventory_transaction table logs all…

**System answer:**
> 

**Sources retrieved (12):** `parent_chunk_business_glossary.md_0`, `parent_chunk_business_glossary.md_1`, `parent_chunk_business_glossary.md_4`, `parent_chunk_business_glossary.md_3`, `Product`, `INVENTORY_TRANSACTION.PRODUCT_ID`, `INVENTORY_TRANSACTION.BIN_ID`, `INVENTORY_TRANSACTION.REASON_CODE`

---

### ✅ QA-007 — What is the Bill of Materials structure and how does it support multi-level product hierarchies?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0000 | **Gate:** `proceed`

**Expected answer:**
> The bill_of_materials table implements a many-to-many self-referencing relationship on the product table: parent_product_id (FK to product) contains component_product_id (FK to product) with a specified quantity and unit_of_measure. Components are classified as COMPONENT, PHANTOM, BYPRODUCT, or CO_P…

**System answer:**
> 

**Sources retrieved (12):** `parent_chunk_business_glossary.md_2`, `parent_chunk_business_glossary.md_0`, `BILL_OF_MATERIALS.PARENT_PRODUCT_ID`, `BILL_OF_MATERIALS.COMPONENT_PRODUCT_ID`, `BILL_OF_MATERIALS.COMPONENT_TYPE`, `BILL_OF_MATERIALS.QUANTITY`, `BILL_OF_MATERIALS.BOM_ID`, `parent_chunk_business_glossary.md_1`

---

### ✅ QA-008 — How are work orders structured and what do they track?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0000 | **Gate:** `proceed`

**Expected answer:**
> The work_order table references product_id (what to produce), production_line_id (where), and warehouse_id (inventory location). It tracks quantity_ordered, quantity_completed, quantity_scrapped, planned dates (start_date, required_date), actual dates (actual_start_date, actual_finish_date), status …

**System answer:**
> 

**Sources retrieved (12):** `parent_chunk_business_glossary.md_2`, `parent_chunk_business_glossary.md_0`, `WORK_ORDER.QUANTITY_ORDERED`, `WORK_ORDER.WORK_ORDER_NUMBER`, `WORK_ORDER.WORK_ORDER_ID`, `WORK_ORDER.PRIORITY`, `WORK_ORDER.ACTUAL_START_DATE`, `Commercial Document`

---

### ✅ QA-009 — How does the quality management system work in the schema?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0000 | **Gate:** `proceed`

**Expected answer:**
> Quality is managed through three related tables. quality_inspection records inspections with types INCOMING/IN_PROCESS/FINAL/AUDIT, results PENDING/PASS/FAIL/CONDITIONAL_PASS, and links to quality_standard (types INTERNAL/ISO/ASTM/FDA/CE). Inspections track defects_found, sample_size, and batch_size…

**System answer:**
> 

**Sources retrieved (12):** `parent_chunk_business_glossary.md_3`, `parent_chunk_business_glossary.md_0`, `Quality Inspection`, `parent_chunk_business_glossary.md_4`, `QUALITY_INSPECTION.BATCH_SIZE`, `QUALITY_INSPECTION.SAMPLE_SIZE`, `QUALITY_INSPECTION.CREATED_AT`, `QUALITY_STANDARD.DESCRIPTION`

---

### ✅ QA-010 — What is the complete invoice lifecycle and how are invoices linked to orders and payments?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0000 | **Gate:** `proceed`

**Expected answer:**
> The invoice table supports four types via CHECK: SALES, PURCHASE, CREDIT_MEMO, and DEBIT_MEMO. Invoices link to customer_id and optionally order_id (FK to sales_order). They track subtotal/tax_amount/total_amount/amount_paid/balance_due and status (DRAFT/POSTED/PAID/OVERDUE/VOID). Each invoice has i…

**System answer:**
> 

**Sources retrieved (12):** `Invoices`, `parent_chunk_business_glossary.md_4`, `parent_chunk_business_glossary.md_2`, `INVOICE.ORDER_ID`, `INVOICE.STATUS`, `INVOICE.INVOICE_NUMBER`, `INVOICE.DUE_DATE`, `INVOICE.BALANCE_DUE`

---

### ✅ QA-011 — How does the procurement process flow from purchase order to receipt?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0000 | **Gate:** `proceed`

**Expected answer:**
> Purchase orders (purchase_order) link to supplier_id FK and warehouse_id, with status lifecycle DRAFT/SUBMITTED/ACKNOWLEDGED/PARTIAL/RECEIVED/CLOSED/CANCELLED. Each PO has purchase_order_line items referencing products with quantity tracking (ordered/received/invoiced) and supplier_part_number. When…

**System answer:**
> 

**Sources retrieved (12):** `parent_chunk_business_glossary.md_0`, `parent_chunk_business_glossary.md_3`, `Purchase Order`, `PURCHASE_RECEIPT.PO_ID`, `PURCHASE_RECEIPT.RECEIVED_BY`, `PURCHASE_RECEIPT_LINE.QUANTITY_ORDERED`, `Commercial Document`, `parent_chunk_business_glossary.md_1`

---

### ✅ QA-012 — How does the general ledger and accounting system work?

**Status:** GROUNDED  
**GT Coverage:** 67% | **Top Score:** 0.0000 | **Gate:** `proceed`

**Expected answer:**
> The GL is built on account_type (DEBIT or CREDIT balance_type), general_ledger_account (with hierarchical parent_account_id self-reference and status ACTIVE/INACTIVE), and accounting_period (with fiscal_year, start/end dates, and is_closed flag). Journal entries (journal_entry) reference a period, h…

**System answer:**
> 

**Sources retrieved (12):** `parent_chunk_business_glossary.md_1`, `General Ledger Account`, `GENERAL_LEDGER_ACCOUNT.ACCOUNT_NUMBER`, `GENERAL_LEDGER_ACCOUNT.ACCOUNT_NAME`, `GENERAL_LEDGER_ACCOUNT.STATUS`, `GENERAL_LEDGER_ACCOUNT.ACCOUNT_TYPE_ID`, `GENERAL_LEDGER_ACCOUNT.CURRENCY`, `GENERAL_LEDGER_ACCOUNT`

---

### ✅ QA-013 — How are accounts receivable and accounts payable tracked?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0000 | **Gate:** `proceed`

**Expected answer:**
> Accounts receivable (accounts_receivable) links to customer_id and invoice_id, tracking amount_original, amount_due, due_date, and a computed days_overdue column. Status values are CURRENT/DUE/OVERDUE/COLLECTION/WRITE_OFF, with collection_status and next_action_date for collections workflow. Account…

**System answer:**
> 

**Sources retrieved (12):** `parent_chunk_business_glossary.md_1`, `Accounts Payable`, `ACCOUNTS_PAYABLE.AP_ID`, `ACCOUNTS_PAYABLE.INVOICE_ID`, `ACCOUNTS_PAYABLE.AMOUNT_DUE`, `ACCOUNTS_RECEIVABLE.INVOICE_ID`, `ACCOUNTS_RECEIVABLE.AMOUNT_DUE`, `INVOICE`

---

### ✅ QA-014 — How is the employee and organizational structure represented?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0000 | **Gate:** `proceed`

**Expected answer:**
> The department table has hierarchical parent_department_id self-reference with status ACTIVE/INACTIVE. Positions (position table) belong to departments via department_id FK, with grade_level, salary range (min/max), and FLSA status (EXEMPT/NON_EXEMPT). Employees reference department_id, position_id,…

**System answer:**
> 

**Sources retrieved (12):** `parent_chunk_business_glossary.md_2`, `Employee`, `Customer`, `parent_chunk_business_glossary.md_4`, `Department Entity`, `EMPLOYEE.EMPLOYEE_TYPE`, `EMPLOYEE.EMPLOYEE_ID`, `EMPLOYEE.EMPLOYEE_NUMBER`

---

### ✅ QA-015 — How does the shipment and logistics system work?

**Status:** GROUNDED  
**GT Coverage:** 50% | **Top Score:** 0.0000 | **Gate:** `proceed`

**Expected answer:**
> Carriers (carrier table) are classified by type: LTL/FTL/PARCEL/AIR/OCEAN/RAIL with rating (0-5). Shipping routes define paths between warehouses (origin_location_id, destination_location_id both FK to warehouse) with distance_km, estimated_hours, and cost_per_km. Shipments reference origin/destinat…

**System answer:**
> 

**Sources retrieved (12):** `parent_chunk_business_glossary.md_3`, `parent_chunk_business_glossary.md_1`, `parent_chunk_business_glossary.md_0`, `SHIPMENT.WEIGHT`, `Shipment Method`, `SHIPMENT.STATUS`, `SHIPMENT.SHIPMENT_TYPE`, `SHIPMENT.SHIP_DATE`

---

### ✅ QA-016 — How does the project management module work?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0000 | **Gate:** `proceed`

**Expected answer:**
> Projects link to customer_id (for customer-facing projects) and project_manager_id (FK to employee). Project types are CUSTOMER/INTERNAL/R&D/CAPITAL with status PLANNING/ACTIVE/ON_HOLD/COMPLETED/CANCELLED and priority levels. Projects track budget_amount vs actual_cost. Project tasks (project_task) …

**System answer:**
> 

**Sources retrieved (12):** `parent_chunk_business_glossary.md_3`, `Project Task`, `parent_chunk_business_glossary.md_2`, `parent_chunk_business_glossary.md_0`, `parent_chunk_business_glossary.md_1`, `PROJECT.PROJECT_NAME`, `PROJECT.PROJECT_ID`, `PROJECT_TASK.STATUS`

---

### ✅ QA-017 — How does the system handle user authentication, roles, and permissions?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0000 | **Gate:** `proceed`

**Expected answer:**
> The app_user table links to employee_id, customer_id, or supplier_id depending on user_type (EMPLOYEE/CUSTOMER/SUPPLIER/ADMIN). Users have status ACTIVE/INACTIVE/LOCKED/PENDING with failed_login_attempts tracking. Roles (role table) are typed as SYSTEM/BUSINESS/CUSTOM with ACTIVE/INACTIVE status. Th…

**System answer:**
> 

**Sources retrieved (12):** `Role`, `User`, `parent_chunk_business_glossary.md_4`, `USER_ROLE.USER_ID`, `USER_ROLE.USER_ROLE_ID`, `USER_ROLE.STATUS`, `USER_ROLE.ROLE_ID`, `APP_USER.CUSTOMER_ID`

---

### ✅ QA-018 — What is the complete path from a customer placing an order to the product being shipped?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0000 | **Gate:** `proceed`

**Expected answer:**
> The order-to-ship path traverses: customer → sales_order (via customer_id FK) → sales_order_line (via order_id FK) → product (via product_id FK). For fulfillment: sales_order references warehouse_id for the fulfillment location. Inventory is checked via inventory_on_hand (product_id + warehouse_id).…

**System answer:**
> 

**Sources retrieved (12):** `parent_chunk_business_glossary.md_0`, `parent_chunk_business_glossary.md_3`, `Commercial Document`, `parent_chunk_business_glossary.md_2`, `SALES_ORDER_LINE.QUANTITY_SHIPPED`, `parent_chunk_business_glossary.md_4`, `SALES_ORDER.SHIPPING_METHOD`, `Purchase Order`

---

### ✅ QA-019 — How does the schema support supplier contracts and their relationship to purchase orders?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0000 | **Gate:** `proceed`

**Expected answer:**
> The supplier_contract table links to supplier_id FK, with contract_type (FIXED_PRICE/COST_PLUS/RATE_BASED/FRAMEWORK), start/end dates, auto_renew flag, payment_terms, total_value, and status (DRAFT/ACTIVE/EXPIRED/TERMINATED). Purchase orders independently link to the same supplier via supplier_id FK…

**System answer:**
> 

**Sources retrieved (12):** `parent_chunk_business_glossary.md_0`, `Supplier Contract`, `PURCHASE_ORDER.SUPPLIER_REFERENCE`, `PURCHASE_ORDER.SUPPLIER_ID`, `PURCHASE_ORDER_LINE.SUPPLIER_PART_NUMBER`, `Commercial Document`, `parent_chunk_business_glossary.md_4`, `parent_chunk_business_glossary.md_1`

---

### ✅ QA-020 — What self-referencing hierarchies exist in the schema?

**Status:** GROUNDED  
**GT Coverage:** 80% | **Top Score:** 0.0000 | **Gate:** `proceed`

**Expected answer:**
> The schema has five self-referencing hierarchies: (1) product_category.parent_category_id → product_category.category_id for nested product classifications; (2) general_ledger_account.parent_account_id → general_ledger_account.account_id for chart of accounts hierarchy; (3) department.parent_departm…

**System answer:**
> 

**Sources retrieved (12):** `General Ledger Account`, `parent_chunk_business_glossary.md_2`, `parent_chunk_business_glossary.md_1`, `JOURNAL_ENTRY_LINE.REFERENCE_ID`, `JOURNAL_ENTRY_LINE.REFERENCE_TYPE`, `QUALITY_INSPECTION.REFERENCE_TYPE`, `Department Entity`, `Work Order Material`

---

### ✅ QA-021 — How does the price list system work for products?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0000 | **Gate:** `proceed`

**Expected answer:**
> The price_list table defines named price lists with currency, effective_date, expiration_date, and status. The product_price junction table links products to price lists with price, minimum_quantity (for volume pricing), discount_percentage, and effective_date. A UNIQUE constraint on (product_id, pr…

**System answer:**
> 

**Sources retrieved (12):** `parent_chunk_business_glossary.md_0`, `PRODUCT_PRICE.PRICE_LIST_ID`, `Purchase Order`, `Commercial Document`, `parent_chunk_business_glossary.md_2`, `parent_chunk_business_glossary.md_3`, `PRICE_LIST.PRICE_LIST_ID`, `PRICE_LIST.PRICE_LIST_NAME`

---

### ✅ QA-022 — What CHECK constraints on status columns exist across the major tables?

**Status:** GROUNDED  
**GT Coverage:** 82% | **Top Score:** 0.0000 | **Gate:** `proceed`

**Expected answer:**
> Key status CHECK constraints include: customer (ACTIVE/INACTIVE/SUSPENDED), product (ACTIVE/DISCONTINUED/PHASE_OUT), sales_order (DRAFT/CONFIRMED/PICKED/SHIPPED/INVOICED/CANCELLED), purchase_order (DRAFT/SUBMITTED/ACKNOWLEDGED/PARTIAL/RECEIVED/CLOSED/CANCELLED), work_order (DRAFT/RELEASED/IN_PROGRES…

**System answer:**
> 

**Sources retrieved (12):** `parent_chunk_business_glossary.md_4`, `parent_chunk_business_glossary.md_2`, `QUALITY_INSPECTION.STATUS`, `POSITION.STATUS`, `SALES_ORDER.STATUS`, `GENERAL_LEDGER_ACCOUNT.STATUS`, `POSITION.FLSA_STATUS`, `Accounting Period`

---

### ✅ QA-023 — How does the stock transfer process work between warehouses?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0000 | **Gate:** `proceed`

**Expected answer:**
> Stock transfers use the stock_transfer table with from_warehouse_id and to_warehouse_id (both FK to warehouse), transfer_date, shipment_method, tracking_number, and status (DRAFT/PICKED/SHIPPED/RECEIVED/CANCELLED). Individual items are tracked via stock_transfer_line with from_bin_id and to_bin_id (…

**System answer:**
> 

**Sources retrieved (12):** `parent_chunk_business_glossary.md_1`, `parent_chunk_business_glossary.md_3`, `Stock Transfer`, `STOCK_TRANSFER.SHIPMENT_METHOD`, `STOCK_TRANSFER.TO_WAREHOUSE_ID`, `STOCK_TRANSFER.FROM_WAREHOUSE_ID`, `STOCK_TRANSFER.STATUS`, `STOCK_TRANSFER.TRANSFER_DATE`

---

### ✅ QA-024 — How are production lines defined and what types exist?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0000 | **Gate:** `proceed`

**Expected answer:**
> The production_line table defines manufacturing resources with line_code (UNIQUE), line_name, line_type (ASSEMBLY/DISCRETE/PROCESS/MIXING via CHECK), location_id (FK to warehouse for the physical location), capacity_per_hour, setup_time_minutes, and status (ACTIVE/MAINTENANCE/INACTIVE). Production l…

**System answer:**
> 

**Sources retrieved (12):** `parent_chunk_business_glossary.md_2`, `parent_chunk_business_glossary.md_3`, `parent_chunk_business_glossary.md_4`, `PRODUCTION_LINE.LINE_TYPE`, `PRODUCTION_LINE.LINE_NAME`, `PRODUCTION_LINE.LINE_CODE`, `PRODUCTION_LINE.LINE_ID`, `PRODUCTION_LINE.CREATED_AT`

---

### ✅ QA-025 — How does the budget system integrate with the financial accounts?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0000 | **Gate:** `proceed`

**Expected answer:**
> The budget table links to both department_id and account_id (FK to general_ledger_account). It tracks budget_type (OPERATING/CAPITAL/PROJECT), fiscal_year, budgeted_amount, actual_amount, and a computed variance column (budgeted minus actual). Budget status follows DRAFT/APPROVED/ACTIVE/CLOSED. This…

**System answer:**
> 

**Sources retrieved (12):** `BUDGET.ACCOUNT_ID`, `BUDGET.VERSION`, `BUDGET.FISCAL_YEAR`, `Budget`, `BUDGET.DEPARTMENT_ID`, `BUDGET.CURRENCY`, `parent_chunk_business_glossary.md_1`, `parent_chunk_business_glossary.md_4`

---

### ✅ QA-026 — What computed/generated columns exist in the schema?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0000 | **Gate:** `proceed`

**Expected answer:**
> The schema has three computed columns using GENERATED ALWAYS AS: (1) inventory_on_hand.quantity_available = quantity_on_hand - quantity_allocated; (2) accounts_receivable.days_overdue = DATEDIFF(CURRENT_DATE, due_date); (3) budget.variance = budgeted_amount - actual_amount. All are STORED (materiali…

**System answer:**
> 

**Sources retrieved (12):** `parent_chunk_business_glossary.md_4`, `PRODUCTION_SCHEDULE.CREATED_AT`, `Work Order Material`, `PRODUCTION_LINE.CREATED_AT`, `Accounting Period`, `Inventory Transaction`, `Time Entry`, `Shipment Method`

---

### ✅ QA-027 — How are customer addresses and contacts structured?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0000 | **Gate:** `proceed`

**Expected answer:**
> Customer addresses are stored in customer_address with address_type (BILLING/SHIPPING/BOTH via CHECK), full address fields (line1, line2, city, state, postal_code, country_code), and is_default flag. The customer_id FK has ON DELETE CASCADE. Customer contacts are in customer_contact with contact_nam…

**System answer:**
> 

**Sources retrieved (12):** `CUSTOMER_CONTACT.EMAIL`, `CUSTOMER_CONTACT.IS_PRIMARY`, `CUSTOMER_CONTACT.CREATED_AT`, `CUSTOMER_CONTACT.PHONE`, `CUSTOMER_CONTACT.CONTACT_NAME`, `Customer`, `parent_chunk_business_glossary.md_0`, `CUSTOMER_TYPE`

---

### ✅ QA-028 — What CASCADE rules exist in the schema and what tables use them?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0000 | **Gate:** `proceed`

**Expected answer:**
> CASCADE rules (ON DELETE CASCADE, ON UPDATE CASCADE) are defined in foreign key constraint syntax within the DDL. These details are typically on child tables like customer_address, customer_contact, sales_order_line, and purchase_order_line. However, specific CASCADE declarations may not be surfaced…

**System answer:**
> 

**Sources retrieved (12):** `INVENTORY_TRANSACTION.REASON_CODE`, `Work Order Material`, `Inventory Transaction`, `Shipment Method`, `parent_chunk_business_glossary.md_2`, `parent_chunk_business_glossary.md_3`, `parent_chunk_business_glossary.md_4`, `parent_chunk_business_glossary.md_0`

---

### ✅ QA-029 — How does the schema link quality inspections to their source documents?

**Status:** GROUNDED  
**GT Coverage:** 33% | **Top Score:** 0.0000 | **Gate:** `proceed`

**Expected answer:**
> Quality inspections use a polymorphic reference pattern: reference_type (VARCHAR) identifies the source table (e.g., 'purchase_receipt', 'work_order') and reference_id (INT) stores the primary key of that source record. The inspection also directly references product_id and warehouse_id via foreign …

**System answer:**
> 

**Sources retrieved (12):** `parent_chunk_business_glossary.md_3`, `QUALITY_INSPECTION.DEFECTS_FOUND`, `QUALITY_INSPECTION.CREATED_AT`, `QUALITY_INSPECTION.REFERENCE_TYPE`, `QUALITY_INSPECTION.STANDARD_ID`, `QUALITY_INSPECTION.REFERENCE_ID`, `Quality Inspection`, `parent_chunk_business_glossary.md_0`

---

### ✅ QA-030 — How does the journal entry enforce double-entry bookkeeping?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0000 | **Gate:** `proceed`

**Expected answer:**
> The journal_entry table requires total_debit and total_credit columns to be present (both NOT NULL DECIMAL 15,2). Journal_entry_line items each reference a general_ledger_account and have a CHECK constraint ensuring exactly one of debit_amount or credit_amount is positive: CHECK ((debit_amount > 0 A…

**System answer:**
> 

**Sources retrieved (12):** `Journal Entry`, `parent_chunk_business_glossary.md_1`, `JOURNAL_ENTRY.ENTRY_TYPE`, `JOURNAL_ENTRY.ENTRY_ID`, `JOURNAL_ENTRY.STATUS`, `JOURNAL_ENTRY.ENTRY_DATE`, `JOURNAL_ENTRY.ENTRY_NUMBER`, `parent_chunk_business_glossary.md_2`

---

### ✅ QA-031 — What types of non-conformance reports exist and what is their lifecycle?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0000 | **Gate:** `proceed`

**Expected answer:**
> Non-conformance reports (NCRs) have four types via CHECK: PRODUCT, PROCESS, DOCUMENTATION, and SUPPLIER. Severity is classified as MINOR/MAJOR/CRITICAL. The status lifecycle is OPEN → IN_PROGRESS → CLOSED → VERIFIED. NCRs track root_cause, corrective_action, and preventive_action (all TEXT fields) f…

**System answer:**
> 

**Sources retrieved (12):** `parent_chunk_business_glossary.md_4`, `NON_CONFORMANCE_REPORT.REFERENCE_TYPE`, `NON_CONFORMANCE_REPORT.NCR_TYPE`, `NON_CONFORMANCE_REPORT.STATUS`, `NON_CONFORMANCE_REPORT.REPORTED_BY`, `NON_CONFORMANCE_REPORT.SEVERITY`, `parent_chunk_business_glossary.md_3`, `parent_chunk_business_glossary.md_0`

---

### ✅ QA-032 — How does the purchase receipt track rejected quantities and lot information?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0000 | **Gate:** `proceed`

**Expected answer:**
> The purchase_receipt_line table tracks three quantity measures: quantity_ordered, quantity_received, and quantity_rejected. When quantity_rejected > 0, materials failed inspection. Each receipt line also records lot_number (for lot traceability), expiration_date (for perishable items), location_id (…

**System answer:**
> 

**Sources retrieved (12):** `PURCHASE_RECEIPT_LINE.QUANTITY_REJECTED`, `PURCHASE_RECEIPT_LINE.QUANTITY_RECEIVED`, `PURCHASE_RECEIPT_LINE.LOT_NUMBER`, `PURCHASE_RECEIPT_LINE.QUANTITY_ORDERED`, `parent_chunk_business_glossary.md_0`, `parent_chunk_business_glossary.md_1`, `parent_chunk_business_glossary.md_3`, `PURCHASE_RECEIPT.RECEIVED_BY`

---

### ✅ QA-033 — What UNIQUE constraints exist across the schema and what do they enforce?

**Status:** GROUNDED  
**GT Coverage:** 75% | **Top Score:** 0.0000 | **Gate:** `proceed`

**Expected answer:**
> UNIQUE constraints exist on business identifier columns (customer.customer_number, product.product_number, supplier.supplier_number, invoice.invoice_number) and composite keys. However, constraint metadata (UNIQUE, CHECK, etc.) may not surface through chunk-based retrieval unless the constraint DDL …

**System answer:**
> 

**Sources retrieved (12):** `parent_chunk_business_glossary.md_4`, `parent_chunk_business_glossary.md_2`, `Sales Order`, `Department Entity`, `Work Order Material`, `PROJECT_TASK.ASSIGNED_TO`, `Time Entry`, `Supplier`

---

### ✅ QA-034 — How does the schema handle the relationship between employees, departments, and projects?

**Status:** GROUNDED  
**GT Coverage:** 50% | **Top Score:** 0.0000 | **Gate:** `proceed`

**Expected answer:**
> Employees belong to departments via department_id FK and hold positions via position_id FK. Positions also reference department_id, creating a redundant but verifiable link. Employee.manager_id (self-referencing FK) creates reporting chains. Projects link to project_manager_id (FK to employee) and o…

**System answer:**
> 

**Sources retrieved (12):** `parent_chunk_business_glossary.md_2`, `parent_chunk_business_glossary.md_1`, `Budget`, `parent_chunk_business_glossary.md_3`, `PROJECT_TASK.ASSIGNED_TO`, `PROJECT_TASK.ESTIMATED_HOURS`, `Department Entity`, `PROJECT.DESCRIPTION`

---

### ✅ QA-035 — What is the relationship between sales orders, invoices, and payments?

**Status:** GROUNDED  
**GT Coverage:** 80% | **Top Score:** 0.0000 | **Gate:** `proceed`

**Expected answer:**
> Sales orders are invoiced by creating invoice records with order_id FK referencing sales_order. Invoice line items (invoice_line) can link back to specific sales_order_line items via order_line_id FK. Payments reference invoice_id FK to settle invoices. The invoice tracks amount_paid and balance_due…

**System answer:**
> 

**Sources retrieved (12):** `Invoices`, `parent_chunk_business_glossary.md_0`, `SALES_ORDER.PAYMENT_TERMS`, `PAYMENT.INVOICE_ID`, `SALES_ORDER.CURRENCY`, `Commercial Document`, `parent_chunk_business_glossary.md_3`, `INVOICE.ORDER_ID`

---

### ✅ QA-036 — What types of inventory transactions does the system track?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0000 | **Gate:** `proceed`

**Expected answer:**
> The inventory_transaction table supports seven transaction types via CHECK constraint: RECEIPT (goods received from suppliers), ISSUE (materials consumed by production or shipped to customers), TRANSFER (movement between warehouses/bins), ADJUSTMENT (corrections to inventory counts), CYCLE_COUNT (pe…

**System answer:**
> 

**Sources retrieved (12):** `parent_chunk_business_glossary.md_1`, `parent_chunk_business_glossary.md_0`, `parent_chunk_business_glossary.md_4`, `Inventory Transaction`, `INVENTORY_TRANSACTION.TRANSACTION_TYPE`, `INVENTORY_TRANSACTION.TRANSACTION_ID`, `INVENTORY_TRANSACTION.PRODUCT_ID`, `INVENTORY_TRANSACTION.BIN_ID`

---

### ✅ QA-037 — How does the BOM component type affect manufacturing?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0000 | **Gate:** `proceed`

**Expected answer:**
> The bill_of_materials table classifies components into four types via CHECK: COMPONENT (standard parts consumed in production), PHANTOM (sub-assemblies that are not stocked — their components are consumed directly), BYPRODUCT (secondary outputs of the production process), and CO_PRODUCT (additional …

**System answer:**
> 

**Sources retrieved (12):** `parent_chunk_business_glossary.md_2`, `BILL_OF_MATERIALS.COMPONENT_TYPE`, `BILL_OF_MATERIALS.BOM_ID`, `BILL_OF_MATERIALS.QUANTITY`, `BILL_OF_MATERIALS.COMPONENT_PRODUCT_ID`, `BILL_OF_MATERIALS.PARENT_PRODUCT_ID`, `Work Order Material`, `BIN_LOCATION.BIN_TYPE`

---

### ✅ QA-038 — How does the audit log track system events and changes?

**Status:** GROUNDED  
**GT Coverage:** 50% | **Top Score:** 0.0000 | **Gate:** `proceed`

**Expected answer:**
> The audit_log table records every significant system event with event_type, user_id (FK to app_user), entity_type (which table was affected), entity_id (which record), and action (CREATE/READ/UPDATE/DELETE/LOGIN/LOGOUT/EXPORT via CHECK). For data changes, old_value and new_value are stored as JSON. …

**System answer:**
> 

**Sources retrieved (12):** `Audit Log`, `parent_chunk_business_glossary.md_4`, `AUDIT_LOG.EVENT_TYPE`, `AUDIT_LOG.LOG_ID`, `AUDIT_LOG.ACTION`, `AUDIT_LOG.TIMESTAMP`, `AUDIT_LOG.ENTITY_ID`, `parent_chunk_business_glossary.md_3`

---

### ✅ QA-039 — What are the different address types supported across the schema?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0000 | **Gate:** `proceed`

**Expected answer:**
> Customer addresses support three types: BILLING, SHIPPING, and BOTH. Supplier addresses support four types: MAIN, BILLING, SHIPPING, and RETURN. Both customer_address and supplier_address have is_default/is_primary flags and cascade delete from their parent. The warehouse table stores location_addre…

**System answer:**
> 

**Sources retrieved (12):** `parent_chunk_business_glossary.md_4`, `parent_chunk_business_glossary.md_0`, `SUPPLIER_ADDRESS.ADDRESS_TYPE`, `CUSTOMER_ADDRESS.ADDRESS_TYPE`, `SUPPLIER_ADDRESS.ADDRESS_LINE2`, `SUPPLIER_ADDRESS.ADDRESS_LINE1`, `SUPPLIER_ADDRESS.ADDRESS_ID`, `Warehouse Zone`

---

### ✅ QA-040 — How would the schema support tracing a product from purchase receipt to customer shipment?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0000 | **Gate:** `proceed`

**Expected answer:**
> The full traceability path is: purchase_receipt (inbound from supplier) → purchase_receipt_line (with lot_number) → inventory_on_hand (lot_number at warehouse/bin) → inventory_transaction (RECEIPT type logs the inbound). For production: work_order_material records material consumption → work_order t…

**System answer:**
> 

**Sources retrieved (12):** `parent_chunk_business_glossary.md_1`, `parent_chunk_business_glossary.md_3`, `parent_chunk_business_glossary.md_0`, `Customer`, `parent_chunk_business_glossary.md_4`, `PURCHASE_RECEIPT.RECEIVED_BY`, `PURCHASE_RECEIPT.STATUS`, `PURCHASE_RECEIPT.PO_ID`

---

### ✅ QA-041 — How are supplier addresses and contacts structured compared to customer addresses?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0000 | **Gate:** `proceed`

**Expected answer:**
> Both follow the same pattern: parent entity → address table + contact table, both with ON DELETE CASCADE. Supplier_address has address_type MAIN/BILLING/SHIPPING/RETURN (vs customer's BILLING/SHIPPING/BOTH) and uses is_primary flag (vs customer_address's is_default). Supplier_contact mirrors custome…

**System answer:**
> 

**Sources retrieved (12):** `parent_chunk_business_glossary.md_1`, `SUPPLIER_ADDRESS.IS_PRIMARY`, `SUPPLIER_ADDRESS.ADDRESS_ID`, `SUPPLIER_ADDRESS.ADDRESS_TYPE`, `SUPPLIER_ADDRESS.CITY`, `SUPPLIER_ADDRESS.CREATED_AT`, `Customer`, `parent_chunk_business_glossary.md_0`

---

### ✅ QA-042 — Does the schema track employee compensation history?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0000 | **Gate:** `proceed`

**Expected answer:**
> The employee table has current annual_salary and hourly_rate columns and the position table defines min_salary and max_salary ranges. However, there is no compensation history table in the schema — salary changes would overwrite the current values without preserving history. The only historical trac…

**System answer:**
> 

**Sources retrieved (12):** `parent_chunk_business_glossary.md_2`, `EMPLOYEE.CREATED_AT`, `parent_chunk_business_glossary.md_3`, `TIME_ENTRY.DESCRIPTION`, `TIME_ENTRY.EMPLOYEE_ID`, `Master Data`, `parent_chunk_business_glossary.md_4`, `parent_chunk_business_glossary.md_0`

---

### ✅ QA-043 — How does the shipping route connect two warehouses through a carrier?

**Status:** GROUNDED  
**GT Coverage:** 33% | **Top Score:** 0.0000 | **Gate:** `proceed`

**Expected answer:**
> The shipping_route table has origin_location_id and destination_location_id (both FK to warehouse), carrier_id (FK to carrier), plus route_code (UNIQUE), distance_km, estimated_hours, cost_per_km, and service_level. Shipments reference route_id FK to use a predefined route, plus independently refere…

**System answer:**
> 

**Sources retrieved (12):** `Shipping Route`, `SHIPPING_ROUTE.ROUTE_NAME`, `SHIPPING_ROUTE.SERVICE_LEVEL`, `SHIPPING_ROUTE.STATUS`, `SHIPPING_ROUTE.ROUTE_CODE`, `parent_chunk_business_glossary.md_3`, `SHIPPING_ROUTE.CARRIER_ID`, `Shipment Method`

---

### ✅ QA-044 — What is the production scheduling model and how does it relate to work orders?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0000 | **Gate:** `proceed`

**Expected answer:**
> The production_schedule table links work_order_id (FK to work_order) to production_line_id (FK to production_line) with scheduled_start and scheduled_end timestamps, plus actual_start and actual_end for tracking real execution. Status progresses SCHEDULED → RUNNING → COMPLETED (or CANCELLED). Priori…

**System answer:**
> 

**Sources retrieved (12):** `PRODUCTION_SCHEDULE.SCHEDULED_END`, `PRODUCTION_SCHEDULE.WORK_ORDER_ID`, `PRODUCTION_SCHEDULE.PRIORITY`, `PRODUCTION_SCHEDULE.STATUS`, `PRODUCTION_SCHEDULE.SCHEDULE_ID`, `parent_chunk_business_glossary.md_2`, `parent_chunk_business_glossary.md_3`, `parent_chunk_business_glossary.md_4`

---

### ✅ QA-045 — How does the invoice line link back to both sales order lines and products?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0000 | **Gate:** `proceed`

**Expected answer:**
> Invoice_line references invoice_id FK (parent invoice), product_id FK (what was invoiced), and optionally order_line_id FK (back-reference to the specific sales_order_line). This three-way linkage supports: invoice → sales_order (via invoice.order_id), invoice_line → product (direct), and invoice_li…

**System answer:**
> 

**Sources retrieved (12):** `parent_chunk_business_glossary.md_3`, `parent_chunk_business_glossary.md_0`, `parent_chunk_business_glossary.md_2`, `SALES_ORDER_LINE.QUANTITY_INVOICED`, `INVOICE_LINE.ORDER_LINE_ID`, `Sales Order`, `SALES_ORDER_LINE.DISCOUNT_PERCENTAGE`, `SALES_ORDER_LINE.REQUESTED_SHIP_DATE`

---

### ✅ QA-046 — Is there a returns or reverse logistics capability in the schema?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0000 | **Gate:** `proceed`

**Expected answer:**
> Returns are partially supported: payment_type includes REFUND, invoice_type includes CREDIT_MEMO, shipment_type includes RETURN, and inventory_transaction has a RETURN transaction type. However, there is no dedicated returns management table (e.g., return_authorization or RMA). Returns would be trac…

**System answer:**
> 

**Sources retrieved (12):** `parent_chunk_business_glossary.md_3`, `parent_chunk_business_glossary.md_1`, `Sales Order`, `PRODUCTION_SCHEDULE.STATUS`, `Work Order Material`, `SALES_ORDER.SHIPPING_METHOD`, `Inventory Transaction`, `Shipment Method`

---

### ✅ QA-047 — How many tables are in each business domain and what are they?

**Status:** GROUNDED  
**GT Coverage:** N/A | **Top Score:** 0.0000 | **Gate:** `proceed`

**Expected answer:**
> A complete table-by-domain breakdown requires schema-wide overview not available from individual chunk retrieval. From retrieved context, identifiable domains include Sales & Customer Management (customer, product, sales_order, etc.), Finance (invoice, payment, journal_entry, gl_account), HR (employ…

**System answer:**
> 

**Sources retrieved (12):** `INVOICE.TAX_AMOUNT`, `Accounting Period`, `Time Entry`, `SALES_ORDER.TAX_AMOUNT`, `PURCHASE_ORDER.TAX_AMOUNT`, `Sales Order`, `General Ledger Account`, `parent_chunk_business_glossary.md_0`

---

### ✅ QA-048 — How does the accounting period system work?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0000 | **Gate:** `proceed`

**Expected answer:**
> The accounting_period table defines fiscal periods with period_code (UNIQUE), period_name, start_date, end_date, fiscal_year, and is_closed flag. A UNIQUE constraint on (fiscal_year, period_code) prevents duplicate periods within a year. Journal entries reference period_id FK to ensure postings land…

**System answer:**
> 

**Sources retrieved (12):** `parent_chunk_business_glossary.md_1`, `ACCOUNTING_PERIOD.PERIOD_ID`, `ACCOUNTING_PERIOD.PERIOD_NAME`, `ACCOUNTING_PERIOD.START_DATE`, `ACCOUNTING_PERIOD.FISCAL_YEAR`, `ACCOUNTING_PERIOD.PERIOD_CODE`, `Accounting Period`, `ACCOUNTING_PERIOD`

---

### ✅ QA-049 — How do work order materials track material consumption against BOM requirements?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0000 | **Gate:** `proceed`

**Expected answer:**
> The work_order_material table links work_order_id FK to product_id FK (the material), with quantity_required (from BOM calculation) and quantity_issued (actually consumed). Status tracks progress: PENDING/ISSUED/PARTIAL/COMPLETE. Materials are sourced from specific bins via bin_id FK to bin_location…

**System answer:**
> 

**Sources retrieved (12):** `parent_chunk_business_glossary.md_2`, `parent_chunk_business_glossary.md_3`, `parent_chunk_business_glossary.md_0`, `WORK_ORDER_MATERIAL.QUANTITY_REQUIRED`, `WORK_ORDER_MATERIAL.MATERIAL_ID`, `WORK_ORDER_MATERIAL.PRODUCT_ID`, `WORK_ORDER_MATERIAL.WORK_ORDER_ID`, `WORK_ORDER_MATERIAL.BIN_ID`

---

### ✅ QA-050 — Does the schema support multi-currency transactions?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0000 | **Gate:** `proceed`

**Expected answer:**
> Multiple tables have currency columns defaulting to USD: customer.currency, sales_order.currency, invoice.currency, payment.currency, purchase_order.currency, supplier.currency, supplier_contract.currency, general_ledger_account.currency, and price_list.currency. However, there is no currency exchan…

**System answer:**
> 

**Sources retrieved (12):** `parent_chunk_business_glossary.md_1`, `Inventory Transaction`, `Sales Order`, `General Ledger Account`, `parent_chunk_business_glossary.md_4`, `SALES_ORDER.CURRENCY`, `PAYMENT.CURRENCY`, `BUDGET.CURRENCY`

---

### ✅ QA-051 — How does the schema handle product storage requirements for hazardous or temperature-sensitive items?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0000 | **Gate:** `proceed`

**Expected answer:**
> Products have three relevant fields: hazardous (BOOLEAN, default FALSE), storage_temperature_min (DECIMAL), and storage_temperature_max (DECIMAL). Warehouse zones have a temperature_controlled (BOOLEAN) flag. When a product requires temperature control, it should be stored in bins within temperature…

**System answer:**
> 

**Sources retrieved (12):** `PRODUCT.HAZARDOUS`, `PRODUCT.STORAGE_TEMPERATURE_MAX`, `PRODUCT.STORAGE_TEMPERATURE_MIN`, `PRODUCT.SHELF_LIFE_DAYS`, `PRODUCT.UPDATED_AT`, `Bin Location`, `parent_chunk_business_glossary.md_0`, `parent_chunk_business_glossary.md_1`

---

### ✅ QA-052 — What polymorphic reference patterns exist in the schema?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0000 | **Gate:** `proceed`

**Expected answer:**
> The schema uses reference_type + reference_id polymorphic patterns in several tables: (1) quality_inspection — reference_type identifies the source (purchase_receipt, work_order) and reference_id stores the ID; (2) inventory_transaction — reference_type identifies the source document (sales_order, p…

**System answer:**
> 

**Sources retrieved (12):** `JOURNAL_ENTRY_LINE.REFERENCE_TYPE`, `QUALITY_INSPECTION.REFERENCE_TYPE`, `JOURNAL_ENTRY_LINE.REFERENCE_ID`, `Work Order Material`, `SHIPMENT_LINE.REFERENCE_LINE_ID`, `NON_CONFORMANCE_REPORT.REFERENCE_TYPE`, `parent_chunk_business_glossary.md_3`, `parent_chunk_business_glossary.md_1`

---

### ✅ QA-053 — Is there a customer loyalty or rewards program in the schema?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0000 | **Gate:** `proceed`

**Expected answer:**
> No, the schema does not contain any tables or columns for customer loyalty programs, reward points, or promotional campaigns. Customer classification is limited to customer_type_id (FK to customer_type), credit_score, and is_preferred-style fields do not exist. The customer table focuses on commerci…

**System answer:**
> 

**Sources retrieved (12):** `Customer`, `parent_chunk_business_glossary.md_0`, `parent_chunk_business_glossary.md_4`, `parent_chunk_business_glossary.md_3`, `parent_chunk_business_glossary.md_1`, `CUSTOMER.CREDIT_LIMIT`, `CUSTOMER.CUSTOMER_NUMBER`, `CUSTOMER.PAYMENT_TERMS`

---

### ✅ QA-054 — How does the schema support three-way matching in procurement?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0000 | **Gate:** `proceed`

**Expected answer:**
> Three-way matching (PO → receipt → invoice) is supported through linked tables: purchase_order_line tracks quantity_ordered, quantity_received, and quantity_invoiced. Purchase_receipt_line links back to po_line_id FK. Invoice can be linked to purchase activities via invoice_type = 'PURCHASE' and acc…

**System answer:**
> 

**Sources retrieved (12):** `Sales Order`, `parent_chunk_business_glossary.md_0`, `parent_chunk_business_glossary.md_4`, `parent_chunk_business_glossary.md_1`, `PURCHASE_ORDER.APPROVED_BY`, `PURCHASE_ORDER.SUPPLIER_ID`, `Purchase Order`, `PURCHASE_ORDER.UPDATED_AT`

---

### ✅ QA-055 — What indexes exist for performance optimization and which tables have the most?

**Status:** GROUNDED  
**GT Coverage:** N/A | **Top Score:** 0.0000 | **Gate:** `proceed`

**Expected answer:**
> Index definitions (CREATE INDEX statements) are DDL metadata that may not surface through chunk-based retrieval unless explicitly included in retrieved context. The schema likely defines indexes on foreign key columns and frequently-queried fields, but specific index names, compositions, and per-tab…

**System answer:**
> 

**Sources retrieved (12):** `parent_chunk_business_glossary.md_4`, `parent_chunk_business_glossary.md_2`, `parent_chunk_business_glossary.md_3`, `parent_chunk_business_glossary.md_0`, `QUALITY_INSPECTION.DEFECTS_FOUND`, `QUALITY_INSPECTION.REFERENCE_ID`, `PRODUCTION_SCHEDULE.PRIORITY`, `POSITION.MAX_SALARY`

---

## Anomalies & Observations

No anomalies detected. All questions grounded with acceptable RAGAS scores.
