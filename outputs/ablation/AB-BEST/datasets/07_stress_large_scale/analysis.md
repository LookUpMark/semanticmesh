# AB-BEST — 07_stress_large_scale — Run Analysis

**Timestamp:** 2026-04-21 22:30:49  
**Run tag:** `run-20260421_221024`

## Configuration

| Parameter | Value |
|-----------|-------|
| Extraction model | `LLM (openai/gpt-4.1-nano)` |
| Reasoning model | `openai/gpt-oss-120b` |
| Embedding model | `BAAI/bge-m3` |
| Retrieval mode | `hybrid` |
| Reranker | `True` |
| Reranker top_k | `20` |
| Chunk size / overlap | `128 / 16` |
| ER similarity threshold | `0.65` |

## Builder Results

| Metric | Value |
|--------|-------|
| Triplets extracted | 21 |
| Entities resolved | 14 |
| Tables parsed | 58 |
| Tables completed | 58 |

## Query Evaluation Summary

| Metric | Value |
|--------|-------|
| Questions | 55 |
| Grounded | **55/55 (100%)** |
| Avg GT Coverage | 80% |
| Avg Top Score | 0.2688 |
| Avg Chunk Count | 20.0 |
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

**Sources retrieved (12):** `Customer→CUSTOMER`, `Customer Type→CUSTOMER_TYPE`, `Customer Address→CUSTOMER_ADDRESS`, `Customer Contact→CUSTOMER_CONTACT`, `Shipment`, `User Account→APP_USER`, `Customer`, `Customer Type`

---

### ✅ QA-002 — How does the schema classify different types of products?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0000 | **Gate:** `proceed`

**Expected answer:**
> Products are classified by product_type via CHECK constraint: FINISHED_GOOD, RAW_MATERIAL, SERVICE, or CONSUMABLE. They also belong to a hierarchical product_category (via category_id FK) where product_category has a self-referencing parent_category_id for nested categories. Products also track stat…

**System answer:**
> 

**Sources retrieved (12):** `Product Catalog→PRODUCT`, `Bill Of Materials→BILL_OF_MATERIALS`, `Customer Type→CUSTOMER_TYPE`, `Pricing→PRODUCT_PRICE`, `Manufacturing Line→PRODUCTION_LINE`, `Pricing→PRICE_LIST`, `Shipment`, `Bill Of Materials`

---

### ✅ QA-003 — What is the structure of the sales order and how does it link to customers and products?

**Status:** GROUNDED  
**GT Coverage:** 67% | **Top Score:** 0.0000 | **Gate:** `proceed`

**Expected answer:**
> The sales_order table links to customer via customer_id FK and to warehouse via warehouse_id. It tracks order_number (UNIQUE), order_date, required_date, promised_date, subtotal/tax_amount/freight_amount/total_amount, and status (DRAFT/CONFIRMED/PICKED/SHIPPED/INVOICED/CANCELLED via CHECK). Priority…

**System answer:**
> 

**Sources retrieved (12):** `Sales Order Line→SALES_ORDER_LINE`, `Receipts Issues Transfers→SALES_ORDER`, `Purchase Order Line→PURCHASE_ORDER_LINE`, `Purchase Order→PURCHASE_ORDER`, `Customer→CUSTOMER`, `Invoice Item→INVOICE_LINE`, `parent_chunk_business_glossary.md_0`, `Sales Order Line`

---

### ✅ QA-004 — How does the schema represent supplier information and their classification?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0000 | **Gate:** `proceed`

**Expected answer:**
> The supplier table stores supplier_id (PK), supplier_number (UNIQUE), supplier_name, supplier_type (MANUFACTURER/DISTRIBUTOR/SERVICE_PROVIDER via CHECK), tax_id, registration_date, and status (ACTIVE/INACTIVE/ON_HOLD/BLACKLISTED). Performance metrics are tracked: credit_rating (A/B/C/D), lead_time_d…

**System answer:**
> 

**Sources retrieved (12):** `Supplier→SUPPLIER_ADDRESS`, `Supplier→SUPPLIER`, `Supplier Contact→SUPPLIER_CONTACT`, `Purchase Order→PURCHASE_ORDER`, `User Account→APP_USER`, `Warehouse Receipt→PURCHASE_RECEIPT`, `Shipment`, `Supplier`

---

### ✅ QA-005 — What types of warehouses does the system support and how is storage organized?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0000 | **Gate:** `proceed`

**Expected answer:**
> The warehouse table defines four types via CHECK: COMPANY_OWNED, 3PL (third-party logistics), VIRTUAL, and TRANSIT. Each warehouse has capacity_cubic_meters and status (ACTIVE/INACTIVE/UNDER_MAINTENANCE). Storage is organized hierarchically: warehouse → warehouse_zone (types: BULK/PICK/STAGING/RECEI…

**System answer:**
> 

**Sources retrieved (12):** `Bin Location→BIN_LOCATION`, `Warehouse→WAREHOUSE`, `Warehouse Zone→WAREHOUSE_ZONE`, `Inventory→INVENTORY_ON_HAND`, `Inventory Transaction→INVENTORY_TRANSACTION`, `Inventory Transaction→WORK_ORDER_MATERIAL`, `Inventory Transaction`, `parent_chunk_business_glossary.md_1`

---

### ✅ QA-006 — How does the inventory tracking system work across the schema?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0000 | **Gate:** `proceed`

**Expected answer:**
> Inventory is tracked at two levels. The inventory_on_hand table records current stock per product/warehouse/bin/lot combination (UNIQUE constraint), with quantity_on_hand, quantity_allocated, and a computed quantity_available column (on_hand minus allocated). The inventory_transaction table logs all…

**System answer:**
> 

**Sources retrieved (12):** `Inventory Transaction→WORK_ORDER_MATERIAL`, `Inventory Transaction→INVENTORY_TRANSACTION`, `Inventory Transaction`, `Inventory→INVENTORY_ON_HAND`, `Product Catalog→PRODUCT`, `Bin Location→BIN_LOCATION`, `Stock Transfer→STOCK_TRANSFER`, `Shipment`

---

### ✅ QA-007 — What is the Bill of Materials structure and how does it support multi-level product hierarchies?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0000 | **Gate:** `proceed`

**Expected answer:**
> The bill_of_materials table implements a many-to-many self-referencing relationship on the product table: parent_product_id (FK to product) contains component_product_id (FK to product) with a specified quantity and unit_of_measure. Components are classified as COMPONENT, PHANTOM, BYPRODUCT, or CO_P…

**System answer:**
> 

**Sources retrieved (12):** `Bill Of Materials→BILL_OF_MATERIALS`, `Product Category→PRODUCT_CATEGORY`, `Inventory Transaction→WORK_ORDER_MATERIAL`, `Product Catalog→PRODUCT`, `Invoice Item→INVOICE_LINE`, `Purchase Order Line→PURCHASE_ORDER_LINE`, `Bill Of Materials`, `parent_chunk_business_glossary.md_2`

---

### ✅ QA-008 — How are work orders structured and what do they track?

**Status:** GROUNDED  
**GT Coverage:** 50% | **Top Score:** 0.0000 | **Gate:** `proceed`

**Expected answer:**
> The work_order table references product_id (what to produce), production_line_id (where), and warehouse_id (inventory location). It tracks quantity_ordered, quantity_completed, quantity_scrapped, planned dates (start_date, required_date), actual dates (actual_start_date, actual_finish_date), status …

**System answer:**
> 

**Sources retrieved (12):** `Work Order→WORK_ORDER`, `Inventory Transaction→WORK_ORDER_MATERIAL`, `Work Order Schedule→PRODUCTION_SCHEDULE`, `Work Time→TIME_ENTRY`, `Sales Order Line→SALES_ORDER_LINE`, `Warehouse Receipt→PURCHASE_RECEIPT`, `Work Order`, `Work Order Schedule`

---

### ✅ QA-009 — How does the quality management system work in the schema?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0000 | **Gate:** `proceed`

**Expected answer:**
> Quality is managed through three related tables. quality_inspection records inspections with types INCOMING/IN_PROCESS/FINAL/AUDIT, results PENDING/PASS/FAIL/CONDITIONAL_PASS, and links to quality_standard (types INTERNAL/ISO/ASTM/FDA/CE). Inspections track defects_found, sample_size, and batch_size…

**System answer:**
> 

**Sources retrieved (12):** `Quality Standard→QUALITY_STANDARD`, `Quality Inspection→QUALITY_INSPECTION`, `Quality Issue→NON_CONFORMANCE_REPORT`, `Supplier→SUPPLIER`, `Organizational Unit→DEPARTMENT`, `Work Order Schedule→PRODUCTION_SCHEDULE`, `parent_chunk_business_glossary.md_3`, `parent_chunk_business_glossary.md_2`

---

### ✅ QA-010 — What is the complete invoice lifecycle and how are invoices linked to orders and payments?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0000 | **Gate:** `proceed`

**Expected answer:**
> The invoice table supports four types via CHECK: SALES, PURCHASE, CREDIT_MEMO, and DEBIT_MEMO. Invoices link to customer_id and optionally order_id (FK to sales_order). They track subtotal/tax_amount/total_amount/amount_paid/balance_due and status (DRAFT/POSTED/PAID/OVERDUE/VOID). Each invoice has i…

**System answer:**
> 

**Sources retrieved (12):** `Financial Transaction→INVOICE`, `Invoice Item→INVOICE_LINE`, `Money Owed To→ACCOUNTS_PAYABLE`, `Money Owed To→PAYMENT`, `Money Owed To→ACCOUNTS_RECEIVABLE`, `Purchase Order Line→PURCHASE_ORDER_LINE`, `parent_chunk_business_glossary.md_0`, `Financial Transaction`

---

### ✅ QA-011 — How does the procurement process flow from purchase order to receipt?

**Status:** GROUNDED  
**GT Coverage:** 60% | **Top Score:** 0.0000 | **Gate:** `proceed`

**Expected answer:**
> Purchase orders (purchase_order) link to supplier_id FK and warehouse_id, with status lifecycle DRAFT/SUBMITTED/ACKNOWLEDGED/PARTIAL/RECEIVED/CLOSED/CANCELLED. Each PO has purchase_order_line items referencing products with quantity tracking (ordered/received/invoiced) and supplier_part_number. When…

**System answer:**
> 

**Sources retrieved (12):** `Warehouse Receipt→PURCHASE_RECEIPT`, `Receipt Details→PURCHASE_RECEIPT_LINE`, `Purchase Order→PURCHASE_ORDER`, `Purchase Order Line→PURCHASE_ORDER_LINE`, `Receipts Issues Transfers→SALES_ORDER`, `Financial Transaction→INVOICE`, `parent_chunk_business_glossary.md_0`, `parent_chunk_business_glossary.md_3`

---

### ✅ QA-012 — How does the general ledger and accounting system work?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0000 | **Gate:** `proceed`

**Expected answer:**
> The GL is built on account_type (DEBIT or CREDIT balance_type), general_ledger_account (with hierarchical parent_account_id self-reference and status ACTIVE/INACTIVE), and accounting_period (with fiscal_year, start/end dates, and is_closed flag). Journal entries (journal_entry) reference a period, h…

**System answer:**
> 

**Sources retrieved (12):** `General Ledger Account→ACCOUNT_TYPE`, `General Ledger Account→GENERAL_LEDGER_ACCOUNT`, `Financial Period→ACCOUNTING_PERIOD`, `System Event Log→AUDIT_LOG`, `Inventory Transaction→WORK_ORDER_MATERIAL`, `General Ledger Account`, `parent_chunk_business_glossary.md_1`, `parent_chunk_business_glossary.md_4`

---

### ✅ QA-013 — How are accounts receivable and accounts payable tracked?

**Status:** GROUNDED  
**GT Coverage:** 33% | **Top Score:** 0.0000 | **Gate:** `proceed`

**Expected answer:**
> Accounts receivable (accounts_receivable) links to customer_id and invoice_id, tracking amount_original, amount_due, due_date, and a computed days_overdue column. Status values are CURRENT/DUE/OVERDUE/COLLECTION/WRITE_OFF, with collection_status and next_action_date for collections workflow. Account…

**System answer:**
> 

**Sources retrieved (12):** `Money Owed To→ACCOUNTS_RECEIVABLE`, `Money Owed To→ACCOUNTS_PAYABLE`, `Money Owed To→PAYMENT`, `Budget→BUDGET`, `Money Owed To`, `parent_chunk_business_glossary.md_1`, `General Ledger Account→ACCOUNT_TYPE`, `General Ledger Account→GENERAL_LEDGER_ACCOUNT`

---

### ✅ QA-014 — How is the employee and organizational structure represented?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0000 | **Gate:** `proceed`

**Expected answer:**
> The department table has hierarchical parent_department_id self-reference with status ACTIVE/INACTIVE. Positions (position table) belong to departments via department_id FK, with grade_level, salary range (min/max), and FLSA status (EXEMPT/NON_EXEMPT). Employees reference department_id, position_id,…

**System answer:**
> 

**Sources retrieved (12):** `Employee→EMPLOYEE`, `Organizational Unit→DEPARTMENT`, `User Account→APP_USER`, `Work Time→TIME_ENTRY`, `parent_chunk_business_glossary.md_2`, `Employee`, `Organizational Unit`, `parent_chunk_business_glossary.md_3`

---

### ✅ QA-015 — How does the shipment and logistics system work?

**Status:** GROUNDED  
**GT Coverage:** 67% | **Top Score:** 0.0000 | **Gate:** `proceed`

**Expected answer:**
> Carriers (carrier table) are classified by type: LTL/FTL/PARCEL/AIR/OCEAN/RAIL with rating (0-5). Shipping routes define paths between warehouses (origin_location_id, destination_location_id both FK to warehouse) with distance_km, estimated_hours, and cost_per_km. Shipments reference origin/destinat…

**System answer:**
> 

**Sources retrieved (12):** `Shipment→SHIPMENT`, `Shipment`, `Shipment Line→SHIPMENT_LINE`, `Stock Transfer→STOCK_TRANSFER_LINE`, `Stock Transfer→STOCK_TRANSFER`, `Logistics Carrier→CARRIER`, `parent_chunk_business_glossary.md_3`, `parent_chunk_business_glossary.md_1`

---

### ✅ QA-016 — How does the project management module work?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0000 | **Gate:** `proceed`

**Expected answer:**
> Projects link to customer_id (for customer-facing projects) and project_manager_id (FK to employee). Project types are CUSTOMER/INTERNAL/R&D/CAPITAL with status PLANNING/ACTIVE/ON_HOLD/COMPLETED/CANCELLED and priority levels. Projects track budget_amount vs actual_cost. Project tasks (project_task) …

**System answer:**
> 

**Sources retrieved (12):** `Project→PROJECT`, `Project Task→PROJECT_TASK`, `Work Time→TIME_ENTRY`, `Budget→BUDGET`, `Organizational Unit→DEPARTMENT`, `Work Order Schedule→PRODUCTION_SCHEDULE`, `parent_chunk_business_glossary.md_2`, `Project`

---

### ✅ QA-017 — How does the system handle user authentication, roles, and permissions?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0000 | **Gate:** `proceed`

**Expected answer:**
> The app_user table links to employee_id, customer_id, or supplier_id depending on user_type (EMPLOYEE/CUSTOMER/SUPPLIER/ADMIN). Users have status ACTIVE/INACTIVE/LOCKED/PENDING with failed_login_attempts tracking. Roles (role table) are typed as SYSTEM/BUSINESS/CUSTOM with ACTIVE/INACTIVE status. Th…

**System answer:**
> 

**Sources retrieved (12):** `User Account→APP_USER`, `User Role Assignments→USER_ROLE`, `System Event Log→AUDIT_LOG`, `Role→ROLE`, `General Ledger Account→GENERAL_LEDGER_ACCOUNT`, `Customer Contact→CUSTOMER_CONTACT`, `parent_chunk_business_glossary.md_4`, `User Account`

---

### ✅ QA-018 — What is the complete path from a customer placing an order to the product being shipped?

**Status:** GROUNDED  
**GT Coverage:** 29% | **Top Score:** 0.0000 | **Gate:** `proceed`

**Expected answer:**
> The order-to-ship path traverses: customer → sales_order (via customer_id FK) → sales_order_line (via order_id FK) → product (via product_id FK). For fulfillment: sales_order references warehouse_id for the fulfillment location. Inventory is checked via inventory_on_hand (product_id + warehouse_id).…

**System answer:**
> 

**Sources retrieved (12):** `Receipts Issues Transfers→SALES_ORDER`, `Sales Order Line→SALES_ORDER_LINE`, `Purchase Order Line→PURCHASE_ORDER_LINE`, `Stock Transfer→STOCK_TRANSFER_LINE`, `Purchase Order→PURCHASE_ORDER`, `Warehouse Receipt→PURCHASE_RECEIPT`, `parent_chunk_business_glossary.md_0`, `Receipts Issues Transfers`

---

### ✅ QA-019 — How does the schema support supplier contracts and their relationship to purchase orders?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0000 | **Gate:** `proceed`

**Expected answer:**
> The supplier_contract table links to supplier_id FK, with contract_type (FIXED_PRICE/COST_PLUS/RATE_BASED/FRAMEWORK), start/end dates, auto_renew flag, payment_terms, total_value, and status (DRAFT/ACTIVE/EXPIRED/TERMINATED). Purchase orders independently link to the same supplier via supplier_id FK…

**System answer:**
> 

**Sources retrieved (12):** `Purchase Order→PURCHASE_ORDER`, `Purchase Order Line→PURCHASE_ORDER_LINE`, `Contract→SUPPLIER_CONTRACT`, `Supplier→SUPPLIER_ADDRESS`, `Supplier→SUPPLIER`, `Warehouse Receipt→PURCHASE_RECEIPT`, `parent_chunk_business_glossary.md_0`, `Purchase Order`

---

### ✅ QA-020 — What self-referencing hierarchies exist in the schema?

**Status:** GROUNDED  
**GT Coverage:** 67% | **Top Score:** 0.0000 | **Gate:** `proceed`

**Expected answer:**
> The schema has five self-referencing hierarchies: (1) product_category.parent_category_id → product_category.category_id for nested product classifications; (2) general_ledger_account.parent_account_id → general_ledger_account.account_id for chart of accounts hierarchy; (3) department.parent_departm…

**System answer:**
> 

**Sources retrieved (12):** `parent_chunk_business_glossary.md_2`, `parent_chunk_business_glossary.md_1`, `Organizational Unit→DEPARTMENT`, `Product Category→PRODUCT_CATEGORY`, `Journal Entry→JOURNAL_ENTRY_LINE`, `Money Owed To→PAYMENT`, `Inventory Transaction→INVENTORY_TRANSACTION`, `Shipment→SHIPMENT`

---

### ✅ QA-021 — How does the price list system work for products?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0000 | **Gate:** `proceed`

**Expected answer:**
> The price_list table defines named price lists with currency, effective_date, expiration_date, and status. The product_price junction table links products to price lists with price, minimum_quantity (for volume pricing), discount_percentage, and effective_date. A UNIQUE constraint on (product_id, pr…

**System answer:**
> 

**Sources retrieved (12):** `Pricing→PRICE_LIST`, `Pricing→PRODUCT_PRICE`, `Product Catalog→PRODUCT`, `Purchase Order Line→PURCHASE_ORDER_LINE`, `Invoice Item→INVOICE_LINE`, `Sales Order Line→SALES_ORDER_LINE`, `Pricing`, `parent_chunk_business_glossary.md_0`

---

### ✅ QA-022 — What CHECK constraints on status columns exist across the major tables?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0000 | **Gate:** `proceed`

**Expected answer:**
> Key status CHECK constraints include: customer (ACTIVE/INACTIVE/SUSPENDED), product (ACTIVE/DISCONTINUED/PHASE_OUT), sales_order (DRAFT/CONFIRMED/PICKED/SHIPPED/INVOICED/CANCELLED), purchase_order (DRAFT/SUBMITTED/ACKNOWLEDGED/PARTIAL/RECEIVED/CLOSED/CANCELLED), work_order (DRAFT/RELEASED/IN_PROGRES…

**System answer:**
> 

**Sources retrieved (12):** `Inventory Transaction→WORK_ORDER_MATERIAL`, `Quality Issue→NON_CONFORMANCE_REPORT`, `User Account→APP_USER`, `Employee→EMPLOYEE`, `Financial Transaction→INVOICE`, `Receipts Issues Transfers→SALES_ORDER`, `Customer→CUSTOMER`, `Quality Standard→QUALITY_STANDARD`

---

### ✅ QA-023 — How does the stock transfer process work between warehouses?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0000 | **Gate:** `proceed`

**Expected answer:**
> Stock transfers use the stock_transfer table with from_warehouse_id and to_warehouse_id (both FK to warehouse), transfer_date, shipment_method, tracking_number, and status (DRAFT/PICKED/SHIPPED/RECEIVED/CANCELLED). Individual items are tracked via stock_transfer_line with from_bin_id and to_bin_id (…

**System answer:**
> 

**Sources retrieved (12):** `Stock Transfer→STOCK_TRANSFER`, `Stock Transfer→STOCK_TRANSFER_LINE`, `Inventory Transaction→INVENTORY_TRANSACTION`, `Receipts Issues Transfers→SALES_ORDER`, `Inventory Transaction→WORK_ORDER_MATERIAL`, `Inventory Transaction`, `Inventory→INVENTORY_ON_HAND`, `Stock Transfer`

---

### ✅ QA-024 — How are production lines defined and what types exist?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0000 | **Gate:** `proceed`

**Expected answer:**
> The production_line table defines manufacturing resources with line_code (UNIQUE), line_name, line_type (ASSEMBLY/DISCRETE/PROCESS/MIXING via CHECK), location_id (FK to warehouse for the physical location), capacity_per_hour, setup_time_minutes, and status (ACTIVE/MAINTENANCE/INACTIVE). Production l…

**System answer:**
> 

**Sources retrieved (12):** `Manufacturing Line→PRODUCTION_LINE`, `Work Order→WORK_ORDER`, `Work Order Schedule→PRODUCTION_SCHEDULE`, `Warehouse→WAREHOUSE`, `Manufacturing Line`, `Work Order`, `parent_chunk_business_glossary.md_3`, `parent_chunk_business_glossary.md_4`

---

### ✅ QA-025 — How does the budget system integrate with the financial accounts?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0000 | **Gate:** `proceed`

**Expected answer:**
> The budget table links to both department_id and account_id (FK to general_ledger_account). It tracks budget_type (OPERATING/CAPITAL/PROJECT), fiscal_year, budgeted_amount, actual_amount, and a computed variance column (budgeted minus actual). Budget status follows DRAFT/APPROVED/ACTIVE/CLOSED. This…

**System answer:**
> 

**Sources retrieved (12):** `Budget→BUDGET`, `General Ledger Account→ACCOUNT_TYPE`, `General Ledger Account→GENERAL_LEDGER_ACCOUNT`, `Financial Period→ACCOUNTING_PERIOD`, `Organizational Unit→DEPARTMENT`, `Journal Entry→JOURNAL_ENTRY_LINE`, `parent_chunk_business_glossary.md_2`, `Budget`

---

### ✅ QA-026 — What computed/generated columns exist in the schema?

**Status:** GROUNDED  
**GT Coverage:** 75% | **Top Score:** 0.0000 | **Gate:** `proceed`

**Expected answer:**
> The schema has three computed columns using GENERATED ALWAYS AS: (1) inventory_on_hand.quantity_available = quantity_on_hand - quantity_allocated; (2) accounts_receivable.days_overdue = DATEDIFF(CURRENT_DATE, due_date); (3) budget.variance = budgeted_amount - actual_amount. All are STORED (materiali…

**System answer:**
> 

**Sources retrieved (12):** `Budget→BUDGET`, `Route→SHIPPING_ROUTE`, `Work Order Schedule→PRODUCTION_SCHEDULE`, `Employee→EMPLOYEE`, `Journal Entry→JOURNAL_ENTRY`, `General Ledger Account→GENERAL_LEDGER_ACCOUNT`, `Money Owed To→PAYMENT`, `Journal Entry→JOURNAL_ENTRY_LINE`

---

### ✅ QA-027 — How are customer addresses and contacts structured?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0000 | **Gate:** `proceed`

**Expected answer:**
> Customer addresses are stored in customer_address with address_type (BILLING/SHIPPING/BOTH via CHECK), full address fields (line1, line2, city, state, postal_code, country_code), and is_default flag. The customer_id FK has ON DELETE CASCADE. Customer contacts are in customer_contact with contact_nam…

**System answer:**
> 

**Sources retrieved (12):** `Customer Address→CUSTOMER_ADDRESS`, `Customer Contact→CUSTOMER_CONTACT`, `Customer→CUSTOMER`, `User Account→APP_USER`, `Supplier Contact→SUPPLIER_CONTACT`, `Project→PROJECT`, `Customer Address`, `Customer Contact`

---

### ✅ QA-028 — What CASCADE rules exist in the schema and what tables use them?

**Status:** GROUNDED  
**GT Coverage:** 50% | **Top Score:** 0.0000 | **Gate:** `proceed`

**Expected answer:**
> ON DELETE CASCADE is used on child tables that should be automatically removed when the parent is deleted: customer_address and customer_contact (cascade from customer), supplier_address and supplier_contact (cascade from supplier), sales_order_line (cascade from sales_order), purchase_order_line (c…

**System answer:**
> 

**Sources retrieved (12):** `Inventory Transaction`, `Manufacturing Line→PRODUCTION_LINE`, `User Role Assignments→USER_ROLE`, `Manufacturing Line`, `Quality Standard`, `Role`, `Work Order`, `Quality Issue`

---

### ✅ QA-029 — How does the schema link quality inspections to their source documents?

**Status:** GROUNDED  
**GT Coverage:** 67% | **Top Score:** 0.0000 | **Gate:** `proceed`

**Expected answer:**
> Quality inspections use a polymorphic reference pattern: reference_type (VARCHAR) identifies the source table (e.g., 'purchase_receipt', 'work_order') and reference_id (INT) stores the primary key of that source record. The inspection also directly references product_id and warehouse_id via foreign …

**System answer:**
> 

**Sources retrieved (12):** `Quality Inspection→QUALITY_INSPECTION`, `Quality Standard→QUALITY_STANDARD`, `Journal Entry→JOURNAL_ENTRY`, `Quality Issue→NON_CONFORMANCE_REPORT`, `Supplier→SUPPLIER`, `Supplier→SUPPLIER_ADDRESS`, `parent_chunk_business_glossary.md_3`, `Quality Inspection`

---

### ✅ QA-030 — How does the journal entry enforce double-entry bookkeeping?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0000 | **Gate:** `proceed`

**Expected answer:**
> The journal_entry table requires total_debit and total_credit columns to be present (both NOT NULL DECIMAL 15,2). Journal_entry_line items each reference a general_ledger_account and have a CHECK constraint ensuring exactly one of debit_amount or credit_amount is positive: CHECK ((debit_amount > 0 A…

**System answer:**
> 

**Sources retrieved (12):** `Journal Entry→JOURNAL_ENTRY`, `Journal Entry→JOURNAL_ENTRY_LINE`, `Work Time→TIME_ENTRY`, `Work Order Schedule→PRODUCTION_SCHEDULE`, `Journal Entry`, `parent_chunk_business_glossary.md_2`, `parent_chunk_business_glossary.md_3`, `parent_chunk_business_glossary.md_1`

---

### ✅ QA-031 — What types of non-conformance reports exist and what is their lifecycle?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0000 | **Gate:** `proceed`

**Expected answer:**
> Non-conformance reports (NCRs) have four types via CHECK: PRODUCT, PROCESS, DOCUMENTATION, and SUPPLIER. Severity is classified as MINOR/MAJOR/CRITICAL. The status lifecycle is OPEN → IN_PROGRESS → CLOSED → VERIFIED. NCRs track root_cause, corrective_action, and preventive_action (all TEXT fields) f…

**System answer:**
> 

**Sources retrieved (12):** `Quality Issue→NON_CONFORMANCE_REPORT`, `Quality Standard→QUALITY_STANDARD`, `Customer→CUSTOMER`, `Supplier→SUPPLIER`, `Inventory Transaction`, `Quality Issue`, `parent_chunk_business_glossary.md_3`, `parent_chunk_business_glossary.md_4`

---

### ✅ QA-032 — How does the purchase receipt track rejected quantities and lot information?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0000 | **Gate:** `proceed`

**Expected answer:**
> The purchase_receipt_line table tracks three quantity measures: quantity_ordered, quantity_received, and quantity_rejected. When quantity_rejected > 0, materials failed inspection. Each receipt line also records lot_number (for lot traceability), expiration_date (for perishable items), location_id (…

**System answer:**
> 

**Sources retrieved (12):** `Receipt Details→PURCHASE_RECEIPT_LINE`, `Warehouse Receipt→PURCHASE_RECEIPT`, `Purchase Order Line→PURCHASE_ORDER_LINE`, `Inventory→INVENTORY_ON_HAND`, `Inventory Transaction→WORK_ORDER_MATERIAL`, `Inventory Transaction→INVENTORY_TRANSACTION`, `Inventory Transaction`, `Receipt Details`

---

### ✅ QA-033 — What UNIQUE constraints exist across the schema and what do they enforce?

**Status:** GROUNDED  
**GT Coverage:** 20% | **Top Score:** 0.0000 | **Gate:** `proceed`

**Expected answer:**
> Key UNIQUE constraints include: customer.customer_number, product.product_number, supplier.supplier_number (business identifiers); invoice.invoice_number, payment.payment_number, shipment.shipment_number (document numbers); sales_order.order_number, purchase_order.po_number; warehouse.warehouse_code…

**System answer:**
> 

**Sources retrieved (12):** `Inventory Transaction`, `Inventory Transaction→WORK_ORDER_MATERIAL`, `Inventory Transaction→INVENTORY_TRANSACTION`, `parent_chunk_business_glossary.md_4`, `parent_chunk_business_glossary.md_2`, `Role→ROLE`, `Organizational Unit→DEPARTMENT`, `Quality Standard→QUALITY_STANDARD`

---

### ✅ QA-034 — How does the schema handle the relationship between employees, departments, and projects?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0000 | **Gate:** `proceed`

**Expected answer:**
> Employees belong to departments via department_id FK and hold positions via position_id FK. Positions also reference department_id, creating a redundant but verifiable link. Employee.manager_id (self-referencing FK) creates reporting chains. Projects link to project_manager_id (FK to employee) and o…

**System answer:**
> 

**Sources retrieved (12):** `Employee→EMPLOYEE`, `Budget→BUDGET`, `Organizational Unit→DEPARTMENT`, `Work Time→TIME_ENTRY`, `Project→PROJECT`, `Project Task→PROJECT_TASK`, `Employee`, `Organizational Unit`

---

### ✅ QA-035 — What is the relationship between sales orders, invoices, and payments?

**Status:** GROUNDED  
**GT Coverage:** 57% | **Top Score:** 0.0000 | **Gate:** `proceed`

**Expected answer:**
> Sales orders are invoiced by creating invoice records with order_id FK referencing sales_order. Invoice line items (invoice_line) can link back to specific sales_order_line items via order_line_id FK. Payments reference invoice_id FK to settle invoices. The invoice tracks amount_paid and balance_due…

**System answer:**
> 

**Sources retrieved (12):** `Sales Order Line→SALES_ORDER_LINE`, `Financial Transaction→INVOICE`, `Receipts Issues Transfers→SALES_ORDER`, `Purchase Order Line→PURCHASE_ORDER_LINE`, `Purchase Order→PURCHASE_ORDER`, `Customer→CUSTOMER`, `parent_chunk_business_glossary.md_0`, `parent_chunk_business_glossary.md_3`

---

### ✅ QA-036 — What types of inventory transactions does the system track?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0000 | **Gate:** `proceed`

**Expected answer:**
> The inventory_transaction table supports seven transaction types via CHECK constraint: RECEIPT (goods received from suppliers), ISSUE (materials consumed by production or shipped to customers), TRANSFER (movement between warehouses/bins), ADJUSTMENT (corrections to inventory counts), CYCLE_COUNT (pe…

**System answer:**
> 

**Sources retrieved (12):** `Inventory Transaction→INVENTORY_TRANSACTION`, `Inventory Transaction`, `Inventory Transaction→WORK_ORDER_MATERIAL`, `Stock Transfer→STOCK_TRANSFER`, `Stock Transfer→STOCK_TRANSFER_LINE`, `Inventory→INVENTORY_ON_HAND`, `General Ledger Account→ACCOUNT_TYPE`, `parent_chunk_business_glossary.md_1`

---

### ✅ QA-037 — How does the BOM component type affect manufacturing?

**Status:** GROUNDED  
**GT Coverage:** 33% | **Top Score:** 0.0000 | **Gate:** `proceed`

**Expected answer:**
> The bill_of_materials table classifies components into four types via CHECK: COMPONENT (standard parts consumed in production), PHANTOM (sub-assemblies that are not stocked — their components are consumed directly), BYPRODUCT (secondary outputs of the production process), and CO_PRODUCT (additional …

**System answer:**
> 

**Sources retrieved (12):** `Bill Of Materials→BILL_OF_MATERIALS`, `Manufacturing Line→PRODUCTION_LINE`, `Work Order→WORK_ORDER`, `Bin Location→BIN_LOCATION`, `Quality Standard→QUALITY_STANDARD`, `Quality Issue→NON_CONFORMANCE_REPORT`, `parent_chunk_business_glossary.md_2`, `parent_chunk_business_glossary.md_3`

---

### ✅ QA-038 — How does the audit log track system events and changes?

**Status:** GROUNDED  
**GT Coverage:** 50% | **Top Score:** 0.0000 | **Gate:** `proceed`

**Expected answer:**
> The audit_log table records every significant system event with event_type, user_id (FK to app_user), entity_type (which table was affected), entity_id (which record), and action (CREATE/READ/UPDATE/DELETE/LOGIN/LOGOUT/EXPORT via CHECK). For data changes, old_value and new_value are stored as JSON. …

**System answer:**
> 

**Sources retrieved (12):** `System Event Log→AUDIT_LOG`, `Inventory Transaction→INVENTORY_TRANSACTION`, `Inventory Transaction`, `Inventory Transaction→WORK_ORDER_MATERIAL`, `Work Time→TIME_ENTRY`, `General Ledger Account→GENERAL_LEDGER_ACCOUNT`, `General Ledger Account→ACCOUNT_TYPE`, `System Event Log`

---

### ✅ QA-039 — What are the different address types supported across the schema?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0000 | **Gate:** `proceed`

**Expected answer:**
> Customer addresses support three types: BILLING, SHIPPING, and BOTH. Supplier addresses support four types: MAIN, BILLING, SHIPPING, and RETURN. Both customer_address and supplier_address have is_default/is_primary flags and cascade delete from their parent. The warehouse table stores location_addre…

**System answer:**
> 

**Sources retrieved (12):** `Customer Address→CUSTOMER_ADDRESS`, `Supplier→SUPPLIER_ADDRESS`, `System Event Log→AUDIT_LOG`, `Warehouse→WAREHOUSE`, `Customer Type→CUSTOMER_TYPE`, `Warehouse Zone→WAREHOUSE_ZONE`, `Shipment`, `Inventory Transaction`

---

### ✅ QA-040 — How would the schema support tracing a product from purchase receipt to customer shipment?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0000 | **Gate:** `proceed`

**Expected answer:**
> The full traceability path is: purchase_receipt (inbound from supplier) → purchase_receipt_line (with lot_number) → inventory_on_hand (lot_number at warehouse/bin) → inventory_transaction (RECEIPT type logs the inbound). For production: work_order_material records material consumption → work_order t…

**System answer:**
> 

**Sources retrieved (12):** `Warehouse Receipt→PURCHASE_RECEIPT`, `Receipt Details→PURCHASE_RECEIPT_LINE`, `Receipts Issues Transfers→SALES_ORDER`, `Shipment→SHIPMENT`, `Shipment Line→SHIPMENT_LINE`, `Stock Transfer→STOCK_TRANSFER`, `Shipment`, `parent_chunk_business_glossary.md_3`

---

### ✅ QA-041 — How are supplier addresses and contacts structured compared to customer addresses?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0000 | **Gate:** `proceed`

**Expected answer:**
> Both follow the same pattern: parent entity → address table + contact table, both with ON DELETE CASCADE. Supplier_address has address_type MAIN/BILLING/SHIPPING/RETURN (vs customer's BILLING/SHIPPING/BOTH) and uses is_primary flag (vs customer_address's is_default). Supplier_contact mirrors custome…

**System answer:**
> 

**Sources retrieved (12):** `Supplier→SUPPLIER_ADDRESS`, `Supplier Contact→SUPPLIER_CONTACT`, `Customer Address→CUSTOMER_ADDRESS`, `Supplier→SUPPLIER`, `User Account→APP_USER`, `Customer Contact→CUSTOMER_CONTACT`, `parent_chunk_business_glossary.md_0`, `Supplier Contact`

---

### ✅ QA-042 — Does the schema track employee compensation history?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0000 | **Gate:** `proceed`

**Expected answer:**
> The employee table has current annual_salary and hourly_rate columns and the position table defines min_salary and max_salary ranges. However, there is no compensation history table in the schema — salary changes would overwrite the current values without preserving history. The only historical trac…

**System answer:**
> 

**Sources retrieved (12):** `Employee→EMPLOYEE`, `Work Time→TIME_ENTRY`, `User Account→APP_USER`, `System Event Log→AUDIT_LOG`, `Employee`, `parent_chunk_business_glossary.md_2`, `Work Time`, `parent_chunk_business_glossary.md_4`

---

### ✅ QA-043 — How does the shipping route connect two warehouses through a carrier?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0000 | **Gate:** `proceed`

**Expected answer:**
> The shipping_route table has origin_location_id and destination_location_id (both FK to warehouse), carrier_id (FK to carrier), plus route_code (UNIQUE), distance_km, estimated_hours, cost_per_km, and service_level. Shipments reference route_id FK to use a predefined route, plus independently refere…

**System answer:**
> 

**Sources retrieved (12):** `Route→SHIPPING_ROUTE`, `Shipment→SHIPMENT`, `Warehouse Receipt→PURCHASE_RECEIPT`, `Stock Transfer→STOCK_TRANSFER`, `Stock Transfer→STOCK_TRANSFER_LINE`, `Shipment`, `Receipts Issues Transfers→SALES_ORDER`, `parent_chunk_business_glossary.md_3`

---

### ✅ QA-044 — What is the production scheduling model and how does it relate to work orders?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0000 | **Gate:** `proceed`

**Expected answer:**
> The production_schedule table links work_order_id (FK to work_order) to production_line_id (FK to production_line) with scheduled_start and scheduled_end timestamps, plus actual_start and actual_end for tracking real execution. Status progresses SCHEDULED → RUNNING → COMPLETED (or CANCELLED). Priori…

**System answer:**
> 

**Sources retrieved (12):** `Work Order Schedule→PRODUCTION_SCHEDULE`, `Work Order→WORK_ORDER`, `Inventory Transaction→WORK_ORDER_MATERIAL`, `Manufacturing Line→PRODUCTION_LINE`, `Project Task→PROJECT_TASK`, `Work Time→TIME_ENTRY`, `Work Order Schedule`, `Work Order`

---

### ✅ QA-045 — How does the invoice line link back to both sales order lines and products?

**Status:** GROUNDED  
**GT Coverage:** 67% | **Top Score:** 0.0000 | **Gate:** `proceed`

**Expected answer:**
> Invoice_line references invoice_id FK (parent invoice), product_id FK (what was invoiced), and optionally order_line_id FK (back-reference to the specific sales_order_line). This three-way linkage supports: invoice → sales_order (via invoice.order_id), invoice_line → product (direct), and invoice_li…

**System answer:**
> 

**Sources retrieved (12):** `Sales Order Line→SALES_ORDER_LINE`, `Invoice Item→INVOICE_LINE`, `Purchase Order Line→PURCHASE_ORDER_LINE`, `Financial Transaction→INVOICE`, `Receipts Issues Transfers→SALES_ORDER`, `Money Owed To→ACCOUNTS_RECEIVABLE`, `parent_chunk_business_glossary.md_0`, `Sales Order Line`

---

### ✅ QA-046 — Is there a returns or reverse logistics capability in the schema?

**Status:** GROUNDED  
**GT Coverage:** 50% | **Top Score:** 0.0000 | **Gate:** `proceed`

**Expected answer:**
> Returns are partially supported: payment_type includes REFUND, invoice_type includes CREDIT_MEMO, shipment_type includes RETURN, and inventory_transaction has a RETURN transaction type. However, there is no dedicated returns management table (e.g., return_authorization or RMA). Returns would be trac…

**System answer:**
> 

**Sources retrieved (12):** `Logistics Carrier→CARRIER`, `parent_chunk_business_glossary.md_3`, `parent_chunk_business_glossary.md_1`, `Logistics Carrier`, `Receipts Issues Transfers→SALES_ORDER`, `Warehouse→WAREHOUSE`, `Manufacturing Line→PRODUCTION_LINE`, `Shipment`

---

### ✅ QA-047 — How many tables are in each business domain and what are they?

**Status:** GROUNDED  
**GT Coverage:** 0% | **Top Score:** 0.0000 | **Gate:** `proceed`

**Expected answer:**
> The schema has 37 tables across 7+ domains: Sales & Customer (10: customer_type, customer, customer_address, customer_contact, product_category, product, price_list, product_price, sales_order, sales_order_line), Invoicing & Payment (4: invoice, invoice_line, payment, accounts_receivable), Procureme…

**System answer:**
> 

**Sources retrieved (12):** `Receipts Issues Transfers→SALES_ORDER`, `Money Owed To→ACCOUNTS_RECEIVABLE`, `Customer→CUSTOMER`, `Money Owed To→PAYMENT`, `Employee→EMPLOYEE`, `Supplier→SUPPLIER`, `Warehouse→WAREHOUSE`, `Journal Entry→JOURNAL_ENTRY`

---

### ✅ QA-048 — How does the accounting period system work?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0000 | **Gate:** `proceed`

**Expected answer:**
> The accounting_period table defines fiscal periods with period_code (UNIQUE), period_name, start_date, end_date, fiscal_year, and is_closed flag. A UNIQUE constraint on (fiscal_year, period_code) prevents duplicate periods within a year. Journal entries reference period_id FK to ensure postings land…

**System answer:**
> 

**Sources retrieved (12):** `Financial Period→ACCOUNTING_PERIOD`, `Budget→BUDGET`, `Journal Entry→JOURNAL_ENTRY`, `General Ledger Account→ACCOUNT_TYPE`, `General Ledger Account→GENERAL_LEDGER_ACCOUNT`, `Work Time→TIME_ENTRY`, `Financial Period`, `parent_chunk_business_glossary.md_4`

---

### ✅ QA-049 — How do work order materials track material consumption against BOM requirements?

**Status:** GROUNDED  
**GT Coverage:** 25% | **Top Score:** 0.0000 | **Gate:** `proceed`

**Expected answer:**
> The work_order_material table links work_order_id FK to product_id FK (the material), with quantity_required (from BOM calculation) and quantity_issued (actually consumed). Status tracks progress: PENDING/ISSUED/PARTIAL/COMPLETE. Materials are sourced from specific bins via bin_id FK to bin_location…

**System answer:**
> 

**Sources retrieved (12):** `Inventory Transaction→WORK_ORDER_MATERIAL`, `Bill Of Materials→BILL_OF_MATERIALS`, `Work Order→WORK_ORDER`, `Work Order Schedule→PRODUCTION_SCHEDULE`, `Inventory Transaction→INVENTORY_TRANSACTION`, `Receipt Details→PURCHASE_RECEIPT_LINE`, `parent_chunk_business_glossary.md_2`, `parent_chunk_business_glossary.md_3`

---

### ✅ QA-050 — Does the schema support multi-currency transactions?

**Status:** GROUNDED  
**GT Coverage:** 75% | **Top Score:** 0.0000 | **Gate:** `proceed`

**Expected answer:**
> Multiple tables have currency columns defaulting to USD: customer.currency, sales_order.currency, invoice.currency, payment.currency, purchase_order.currency, supplier.currency, supplier_contract.currency, general_ledger_account.currency, and price_list.currency. However, there is no currency exchan…

**System answer:**
> 

**Sources retrieved (12):** `Customer→CUSTOMER`, `General Ledger Account→GENERAL_LEDGER_ACCOUNT`, `Inventory Transaction→INVENTORY_TRANSACTION`, `Inventory Transaction→WORK_ORDER_MATERIAL`, `Stock Transfer→STOCK_TRANSFER_LINE`, `Stock Transfer→STOCK_TRANSFER`, `Inventory Transaction`, `General Ledger Account→ACCOUNT_TYPE`

---

### ✅ QA-051 — How does the schema handle product storage requirements for hazardous or temperature-sensitive items?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0000 | **Gate:** `proceed`

**Expected answer:**
> Products have three relevant fields: hazardous (BOOLEAN, default FALSE), storage_temperature_min (DECIMAL), and storage_temperature_max (DECIMAL). Warehouse zones have a temperature_controlled (BOOLEAN) flag. When a product requires temperature control, it should be stored in bins within temperature…

**System answer:**
> 

**Sources retrieved (12):** `Product Catalog→PRODUCT`, `Receipt Details→PURCHASE_RECEIPT_LINE`, `Bill Of Materials→BILL_OF_MATERIALS`, `Quality Inspection→QUALITY_INSPECTION`, `Bin Location→BIN_LOCATION`, `Shipment Line→SHIPMENT_LINE`, `parent_chunk_business_glossary.md_1`, `Product Catalog`

---

### ✅ QA-052 — What polymorphic reference patterns exist in the schema?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0000 | **Gate:** `proceed`

**Expected answer:**
> The schema uses reference_type + reference_id polymorphic patterns in several tables: (1) quality_inspection — reference_type identifies the source (purchase_receipt, work_order) and reference_id stores the ID; (2) inventory_transaction — reference_type identifies the source document (sales_order, p…

**System answer:**
> 

**Sources retrieved (12):** `Journal Entry→JOURNAL_ENTRY_LINE`, `Shipment`, `Shipment→SHIPMENT`, `Inventory Transaction→INVENTORY_TRANSACTION`, `Inventory Transaction`, `Inventory Transaction→WORK_ORDER_MATERIAL`, `parent_chunk_business_glossary.md_3`, `parent_chunk_business_glossary.md_1`

---

### ✅ QA-053 — Is there a customer loyalty or rewards program in the schema?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0000 | **Gate:** `proceed`

**Expected answer:**
> No, the schema does not contain any tables or columns for customer loyalty programs, reward points, or promotional campaigns. Customer classification is limited to customer_type_id (FK to customer_type), credit_score, and is_preferred-style fields do not exist. The customer table focuses on commerci…

**System answer:**
> 

**Sources retrieved (12):** `Customer→CUSTOMER`, `User Account→APP_USER`, `Receipts Issues Transfers→SALES_ORDER`, `Customer Type→CUSTOMER_TYPE`, `Money Owed To→PAYMENT`, `Money Owed To→ACCOUNTS_RECEIVABLE`, `parent_chunk_business_glossary.md_0`, `parent_chunk_business_glossary.md_4`

---

### ✅ QA-054 — How does the schema support three-way matching in procurement?

**Status:** GROUNDED  
**GT Coverage:** 50% | **Top Score:** 0.0000 | **Gate:** `proceed`

**Expected answer:**
> Three-way matching (PO → receipt → invoice) is supported through linked tables: purchase_order_line tracks quantity_ordered, quantity_received, and quantity_invoiced. Purchase_receipt_line links back to po_line_id FK. Invoice can be linked to purchase activities via invoice_type = 'PURCHASE' and acc…

**System answer:**
> 

**Sources retrieved (12):** `Customer→CUSTOMER`, `parent_chunk_business_glossary.md_0`, `parent_chunk_business_glossary.md_4`, `parent_chunk_business_glossary.md_1`, `Customer`, `Receipt Details→PURCHASE_RECEIPT_LINE`, `Receipts Issues Transfers→SALES_ORDER`, `Supplier→SUPPLIER_ADDRESS`

---

### ✅ QA-055 — What indexes exist for performance optimization and which tables have the most?

**Status:** GROUNDED  
**GT Coverage:** 0% | **Top Score:** 0.0000 | **Gate:** `proceed`

**Expected answer:**
> The schema defines explicit indexes beyond primary keys: customer has 3 indexes (on customer_type_id, status, customer_name), product has 4 (category, status, type, name), sales_order has 4 (customer, status, date, warehouse), purchase_order has 4 (supplier, status, date, warehouse), inventory has 5…

**System answer:**
> 

**Sources retrieved (12):** `Supplier→SUPPLIER`, `Supplier→SUPPLIER_ADDRESS`, `parent_chunk_business_glossary.md_4`, `parent_chunk_business_glossary.md_0`, `parent_chunk_business_glossary.md_2`, `Supplier`, `parent_chunk_business_glossary.md_3`, `Employee→EMPLOYEE`

---

## Anomalies & Observations

No anomalies detected. All questions grounded with acceptable RAGAS scores.
