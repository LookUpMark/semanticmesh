# AB-00 — 07_stress_large_scale — Run Analysis

**Timestamp:** 2026-03-27 19:41:20  
**Run tag:** `post-fix-v3`

## Configuration

| Parameter | Value |
|-----------|-------|
| Extraction model | `LLM (gpt-5.4-nano-2026-03-17)` |
| Reasoning model | `gpt-5.4-nano-2026-03-17` |
| Embedding model | `BAAI/bge-m3` |
| Retrieval mode | `hybrid` |
| Reranker | `True` |
| Reranker top_k | `12` |
| Chunk size / overlap | `256 / 32` |
| ER similarity threshold | `0.75` |

## Builder Results

| Metric | Value |
|--------|-------|
| Triplets extracted | 785 |
| Entities resolved | 407 |
| Tables parsed | 58 |
| Tables completed | 58 |

## Query Evaluation Summary

| Metric | Value |
|--------|-------|
| Questions | 55 |
| Grounded | **29/55 (53%)** |
| Avg GT Coverage | 100% |
| Avg Top Score | 0.1520 |
| Avg Chunk Count | 6.3 |
| Abstained | 26 |

## RAGAS Metrics

RAGAS evaluation not enabled for this run.

## Per-Question Deep Dive

### ✅ QA-001 — What information does the customer table store and what constraints does it have?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.8229 | **Gate:** `proceed`

**Expected answer:**
> The customer table stores customer_id (PK), customer_number (UNIQUE), customer_name, customer_type_id (FK to customer_type), tax_id, registration_date, status (ACTIVE/INACTIVE/SUSPENDED via CHECK), credit_limit (default 0), currency (default USD), payment_terms (default 30 days), credit_score (CHECK…

**System answer:**
> The knowledge graph describes the business concept “Customer Master” as being implemented by the physical table `CUSTOMER`. From the context, `CUSTOMER` stores core customer master data including `customer_id`, `customer_number`, `customer_name`, `customer_type_id`, `tax_id`, `registration_date`, and `status`. It also stores several customer attributes: `credit_limit`, `currency`, `payment_terms`,…

**Sources retrieved (12):** `User Account`, `Customer Address`, `Duplicate Contact Records→CUSTOMER_CONTACT`, `Customer Address→CUSTOMER_ADDRESS`, `Customer Address→SUPPLIER_ADDRESS`, `User Account→APP_USER`, `Customer Master→CUSTOMER`, `Duplicate Contact Records`

**Context previews (first 3):**

1. _User Account: The table stores core identity and authentication attributes such as username, email, user_type, status, last_login_date, and failed_login_attempts, which directly represent a user accou…_

2. _Customer Address: The table name and foreign key (customer_id → customer) indicate it stores address records belonging to customers. It includes standard address attributes (address_type, address_line…_

3. _Business concept 'Duplicate Contact Records' — The table stores customer contact attributes (name, role, email, phone) linked to customer_id, which can be used to review and reconcile potentially dupl…_

---

### ✅ QA-002 — How does the schema classify different types of products?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0142 | **Gate:** `proceed_with_warning`

**Expected answer:**
> Products are classified by product_type via CHECK constraint: FINISHED_GOOD, RAW_MATERIAL, SERVICE, or CONSUMABLE. They also belong to a hierarchical product_category (via category_id FK) where product_category has a self-referencing parent_category_id for nested categories. Products also track stat…

**System answer:**
> The schema classifies different types of products using the business concept “Finished goods raw materials services,” which states that the product catalog records include an explicit `product_type` supporting “finished goods, raw materials, and services.” This concept is implemented by the physical table `PRODUCT`, which includes the column `product_type` (along with other product attributes like…

**Sources retrieved (12):** `Finished goods raw materials services→PRODUCT`, `parent_chunk_business_glossary.md_0`, `Finished goods raw materials services`, `parent_chunk_complex_scenarios.md_5`, `parent_chunk_complex_scenarios.md_6`, `parent_chunk_complex_scenarios.md_13`, `parent_chunk_complex_scenarios.md_14`, `parent_chunk_business_glossary.md_3`

**Context previews (first 3):**

1. _Business concept 'Finished goods raw materials services' — The table is a master data record for sellable/managed items with an explicit product_type that supports finished goods, raw materials, and s…_

2. _# Enterprise ERP Business Glossary  ## Sales & Customer Management  ### Customer **Definition**: An individual or organization that purchases goods or services from the company. Customers can be class…_

3. _Finished goods raw materials services: The table is a master data record for sellable/managed items with an explicit product_type that supports finished goods, raw materials, and services, matching th…_

---

### ✅ QA-003 — What is the structure of the sales order and how does it link to customers and products?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.5556 | **Gate:** `proceed`

**Expected answer:**
> The sales_order table links to customer via customer_id FK and to warehouse via warehouse_id. It tracks order_number (UNIQUE), order_date, required_date, promised_date, subtotal/tax_amount/freight_amount/total_amount, and status (DRAFT/CONFIRMED/PICKED/SHIPPED/INVOICED/CANCELLED via CHECK). Priority…

**System answer:**
> The sales order is represented by the physical table SALES_ORDER, which stores order-level fields including order_id, order_number, customer_id, order_date, required_date, promised_date, warehouse_id, sales_rep_id, shipping_method, payment_terms, currency, subtotal, tax_amount, freight_amount, total_amount, status, priority, customer_po_number, created_at, and updated_at. It links directly to the …

**Sources retrieved (12):** `the complete order-to-cash cycle for high-value customers who purchase products from multiple categories, tracking from sales order through payment collection→SALES_ORDER`, `Sales Order Line→SALES_ORDER_LINE`, `Customer Invoice→INVOICE`, `User Account`, `Purchase Order Line`, `parent_chunk_business_glossary.md_0`, `parent_chunk_complex_scenarios.md_5`, `Sales Order Line`

**Context previews (first 3):**

1. _Business concept 'the complete order-to-cash cycle for high-value customers who purchase products from multiple categories, tracking from sales order through payment collection' is implemented by phys…_

2. _Business concept 'Sales Order Line' — The table contains order line identifiers (line_id, line_number) tied to a parent sales order (order_id) and captures product, ordered/shipped/invoiced quantities…_

3. _Business concept 'Customer Invoice' — The table is explicitly named invoice and contains standard invoice attributes such as invoice_number, invoice_type, invoice_date, due_date, currency, monetary to…_

---

### ✅ QA-004 — How does the schema represent supplier information and their classification?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0286 | **Gate:** `proceed_with_warning`

**Expected answer:**
> The supplier table stores supplier_id (PK), supplier_number (UNIQUE), supplier_name, supplier_type (MANUFACTURER/DISTRIBUTOR/SERVICE_PROVIDER via CHECK), tax_id, registration_date, and status (ACTIVE/INACTIVE/ON_HOLD/BLACKLISTED). Performance metrics are tracked: credit_rating (A/B/C/D), lead_time_d…

**System answer:**
> The schema represents supplier information using the business concept “Supplier Master,” implemented by the physical table SUPPLIER. SUPPLIER stores supplier identity and classification attributes including supplier_id, supplier_number, supplier_name, and supplier_type (along with tax_id, registration_date, and status). In addition, it stores commercial and performance profile information for the …

**Sources retrieved (12):** `Supplier Master→SUPPLIER`, `Each supplier→SUPPLIER_CONTACT`, `Employee Time Entry→TIME_ENTRY`, `User Account`, `Supplier Master`, `parent_chunk_business_glossary.md_0`, `Employee Time Entry`, `Supplier Contract`

**Context previews (first 3):**

1. _Business concept 'Supplier Master' — The table implements a supplier master record (supplier_id/number/name/type, tax_id, registration_date, status) along with commercial terms (payment_terms, currenc…_

2. _Business concept 'Each supplier' is implemented by physical table SUPPLIER_CONTACT (columns: contact_id, supplier_id, contact_name, contact_role, email, phone, is_primary, created_at).…_

3. _Business concept 'Employee Time Entry' — The table captures a per-employee, per-day record of hours worked (employee_id, work_date, hours_worked) with optional work categorization and an approval work…_

---

### ✅ QA-005 — What types of warehouses does the system support and how is storage organized?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.2585 | **Gate:** `proceed`

**Expected answer:**
> The warehouse table defines four types via CHECK: COMPANY_OWNED, 3PL (third-party logistics), VIRTUAL, and TRANSIT. Each warehouse has capacity_cubic_meters and status (ACTIVE/INACTIVE/UNDER_MAINTENANCE). Storage is organized hierarchically: warehouse → warehouse_zone (types: BULK/PICK/STAGING/RECEI…

**System answer:**
> The system supports multiple kinds of warehouses, as defined in the business concept “Warehouse”: warehouses can be company-owned, third-party logistics (3PL) facilities, or virtual locations for transit inventory (via the “warehouse_type” attribute).

Storage organization within those warehouses is supported through “Warehouse Zone” and its physical implementation “WAREHOUSE_ZONE”. “Warehouse Zon…

**Sources retrieved (12):** `Warehouse Zone→WAREHOUSE_ZONE`, `Finished goods raw materials services→PRODUCT`, `Inventory Quantity Change→INVENTORY_TRANSACTION`, `parent_chunk_business_glossary.md_1`, `Warehouse Zone`, `parent_chunk_complex_scenarios.md_7`, `parent_chunk_business_glossary.md_4`, `Inventory Quantity Change`

**Context previews (first 3):**

1. _Business concept 'Warehouse Zone' — The table explicitly models zones that belong to a warehouse via warehouse_id and includes zone identifiers (zone_code, zone_name) and classification attributes (zo…_

2. _Business concept 'Finished goods raw materials services' — The table is a master data record for sellable/managed items with an explicit product_type that supports finished goods, raw materials, and s…_

3. _Business concept 'Inventory Quantity Change' — The table stores item-level changes to inventory quantity (quantity, transaction_type, transaction_date) and relates them to the specific product and sto…_

---

### ✅ QA-006 — How does the inventory tracking system work across the schema?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0081 | **Gate:** `proceed_with_warning`

**Expected answer:**
> Inventory is tracked at two levels. The inventory_on_hand table records current stock per product/warehouse/bin/lot combination (UNIQUE constraint), with quantity_on_hand, quantity_allocated, and a computed quantity_available column (on_hand minus allocated). The inventory_transaction table logs all…

**System answer:**
> In the schema, inventory tracking works by recording every movement or change in inventory quantity in the `INVENTORY_TRANSACTION` table and by capturing specific inter-warehouse movements in the `STOCK_TRANSFER` table.

`INVENTORY_TRANSACTION` is the core tracking mechanism because it stores item-level quantity changes tied to both the product and the storage location. Each record includes identi…

**Sources retrieved (12):** `Stock Transfer→STOCK_TRANSFER`, `Inventory Quantity Change→INVENTORY_TRANSACTION`, `parent_chunk_complex_scenarios.md_7`, `parent_chunk_business_glossary.md_1`, `Inventory Quantity Change`, `Stock Transfer`, `parent_chunk_business_glossary.md_4`, `parent_chunk_complex_scenarios.md_15`

**Context previews (first 3):**

1. _Business concept 'Stock Transfer' — The table explicitly stores inter-warehouse movement details (from_warehouse_id, to_warehouse_id), along with transfer and required dates, shipment method, tracking…_

2. _Business concept 'Inventory Quantity Change' — The table stores item-level changes to inventory quantity (quantity, transaction_type, transaction_date) and relates them to the specific product and sto…_

3. _## Scenario 3: Multi-Warehouse Inventory Optimization **Business Question**: Optimize inventory distribution across warehouses by analyzing product demand, stock levels, transfer patterns, and holding…_

---

### ✅ QA-007 — What is the Bill of Materials structure and how does it support multi-level product hierarchies?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.5486 | **Gate:** `proceed`

**Expected answer:**
> The bill_of_materials table implements a many-to-many self-referencing relationship on the product table: parent_product_id (FK to product) contains component_product_id (FK to product) with a specified quantity and unit_of_measure. Components are classified as COMPONENT, PHANTOM, BYPRODUCT, or CO_P…

**System answer:**
> The Bill of Materials structure is implemented by the physical table `BILL_OF_MATERIALS`. In this design, each BOM record links a `parent_product_id` to a `component_product_id`, along with the `quantity` and `unit_of_measure` needed, plus attributes like `scrap_percentage`, `component_type`, and effective dating via `effective_start_date` and `effective_end_date`.

It supports multi-level product…

**Sources retrieved (12):** `Joins 8 tables: Product → Bill of Materials (self-join for multi-level) → Work Order → Work Order Material → Production Schedule → Production Line → Quality Inspection → Inventory Transaction→BILL_OF_MATERIALS`, `Joins 8 tables: Product → Bill of Materials (self-join for multi-level) → Work Order → Work Order Material → Production Schedule → Production Line → Quality Inspection → Inventory Transaction→QUALITY_INSPECTION`, `Joins 8 tables: Product → Bill of Materials (self-join for multi-level) → Work Order → Work Order Material → Production Schedule → Production Line → Quality Inspection → Inventory Transaction`, `Job costing materials→WORK_ORDER_MATERIAL`, `Finished goods raw materials services→PRODUCT`, `BOMs, account hierarchies, project task hierarchies→PROJECT_TASK`, `parent_chunk_complex_scenarios.md_8`, `parent_chunk_business_glossary.md_2`

**Context previews (first 3):**

1. _Business concept 'Joins 8 tables: Product → Bill of Materials (self-join for multi-level) → Work Order → Work Order Material → Production Schedule → Production Line → Quality Inspection → Inventory Tr…_

2. _Business concept 'Joins 8 tables: Product → Bill of Materials (self-join for multi-level) → Work Order → Work Order Material → Production Schedule → Production Line → Quality Inspection → Inventory Tr…_

3. _Joins 8 tables: Product → Bill of Materials (self-join for multi-level) → Work Order → Work Order Material → Production Schedule → Production Line → Quality Inspection → Inventory Transaction…_

---

### ✅ QA-008 — How are work orders structured and what do they track?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.1099 | **Gate:** `proceed_with_warning`

**Expected answer:**
> The work_order table references product_id (what to produce), production_line_id (where), and warehouse_id (inventory location). It tracks quantity_ordered, quantity_completed, quantity_scrapped, planned dates (start_date, required_date), actual dates (actual_start_date, actual_finish_date), status …

**System answer:**
> Work orders are represented by the physical table WORK_ORDER, which defines a “specific work item within a project that must be completed.” In WORK_ORDER, each work order is identified by work_order_id and work_order_number and is tied to a product (product_id), production line (production_line_id), and warehouse (warehouse_id). It tracks quantities including quantity_ordered, quantity_completed, …

**Sources retrieved (12):** `Job costing materials→WORK_ORDER_MATERIAL`, `A specific work item within a project that must be completed.→WORK_ORDER`, `Joins 8 tables: Product → Bill of Materials (self-join for multi-level) → Work Order → Work Order Material → Production Schedule → Production Line → Quality Inspection → Inventory Transaction→QUALITY_INSPECTION`, `Joins 8 tables: Product → Bill of Materials (self-join for multi-level) → Work Order → Work Order Material → Production Schedule → Production Line → Quality Inspection → Inventory Transaction→BILL_OF_MATERIALS`, `the complete order-to-cash cycle for high-value customers who purchase products from multiple categories, tracking from sales order through payment collection→SALES_ORDER`, `Scheduled Production Time→PRODUCTION_SCHEDULE`, `Joins 8 tables: Product → Bill of Materials (self-join for multi-level) → Work Order → Work Order Material → Production Schedule → Production Line → Quality Inspection → Inventory Transaction`, `Job costing materials`

**Context previews (first 3):**

1. _Business concept 'Job costing materials' — The table records per-work-order material quantities (quantity_required vs quantity_issued) and unit costs tied to a specific work_order_id, which aligns wit…_

2. _Business concept 'A specific work item within a project that must be completed.' — A specific work item within a project that must be completed. is implemented by physical table WORK_ORDER (columns: w…_

3. _Business concept 'Joins 8 tables: Product → Bill of Materials (self-join for multi-level) → Work Order → Work Order Material → Production Schedule → Production Line → Quality Inspection → Inventory Tr…_

---

### ✅ QA-009 — How does the quality management system work in the schema?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0049 | **Gate:** `proceed_with_warning`

**Expected answer:**
> Quality is managed through three related tables. quality_inspection records inspections with types INCOMING/IN_PROCESS/FINAL/AUDIT, results PENDING/PASS/FAIL/CONDITIONAL_PASS, and links to quality_standard (types INTERNAL/ISO/ASTM/FDA/CE). Inspections track defects_found, sample_size, and batch_size…

**System answer:**
> From the retrieved context, the quality management system is represented primarily by two related business concepts: “Quality Standard” and “Quality Inspection.”

“Quality Standard” is implemented by the physical table QUALITY_STANDARD with columns standard_id, standard_code, standard_name, standard_type, version, issue_date, status, and description. In business terms, a quality standard is a docu…

**Sources retrieved (12):** `Employee Time Entry→TIME_ENTRY`, `Quality Standard→QUALITY_STANDARD`, `parent_chunk_business_glossary.md_3`, `Employee Time Entry`, `parent_chunk_business_glossary.md_2`, `parent_chunk_complex_scenarios.md_16`, `parent_chunk_business_glossary.md_0`, `parent_chunk_complex_scenarios.md_13`

**Context previews (first 3):**

1. _Business concept 'Employee Time Entry' — The table captures a per-employee, per-day record of hours worked (employee_id, work_date, hours_worked) with optional work categorization and an approval work…_

2. _Business concept 'Quality Standard' is implemented by physical table QUALITY_STANDARD (columns: standard_id, standard_code, standard_name, standard_type, version, issue_date, status, description).…_

3. _## Quality & Compliance  ### Quality Inspection **Definition**: A systematic examination of materials or products to verify conformance to specifications. Inspections can be incoming (from suppliers),…_

---

### ✅ QA-010 — What is the complete invoice lifecycle and how are invoices linked to orders and payments?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.1852 | **Gate:** `proceed_with_warning`

**Expected answer:**
> The invoice table supports four types via CHECK: SALES, PURCHASE, CREDIT_MEMO, and DEBIT_MEMO. Invoices link to customer_id and optionally order_id (FK to sales_order). They track subtotal/tax_amount/total_amount/amount_paid/balance_due and status (DRAFT/POSTED/PAID/OVERDUE/VOID). Each invoice has i…

**System answer:**
> The retrieved context does not define an explicit ordered sequence of invoice lifecycle stages/transitions. What it does specify is that the **Business concept “Customer Invoice”** is represented by the physical table **INVOICE**, which includes lifecycle-relevant fields: `invoice_date`, `due_date`, payment progress via `amount_paid` and `balance_due`, and a lifecycle indicator via `status`.

Invo…

**Sources retrieved (12):** `Customer Invoice→INVOICE`, `the complete order-to-cash cycle for high-value customers who purchase products from multiple categories, tracking from sales order through payment collection→SALES_ORDER`, `Payment Record→PAYMENT`, `Invoice Line→INVOICE_LINE`, `parent_chunk_complex_scenarios.md_5`, `Customer Invoice`, `parent_chunk_complex_scenarios.md_10`, `the complete order-to-cash cycle for high-value customers who purchase products from multiple categories, tracking from sales order through payment collection`

**Context previews (first 3):**

1. _Business concept 'Customer Invoice' — The table is explicitly named invoice and contains standard invoice attributes such as invoice_number, invoice_type, invoice_date, due_date, currency, monetary to…_

2. _Business concept 'the complete order-to-cash cycle for high-value customers who purchase products from multiple categories, tracking from sales order through payment collection' is implemented by phys…_

3. _Business concept 'Payment Record' — The table contains core payment attributes (payment_id/payment_number, payment_type, payment_date, payment_method, amount/currency, status) and links directly to cu…_

---

### ✅ QA-011 — How does the procurement process flow from purchase order to receipt?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.6981 | **Gate:** `proceed`

**Expected answer:**
> Purchase orders (purchase_order) link to supplier_id FK and warehouse_id, with status lifecycle DRAFT/SUBMITTED/ACKNOWLEDGED/PARTIAL/RECEIVED/CLOSED/CANCELLED. Each PO has purchase_order_line items referencing products with quantity tracking (ordered/received/invoiced) and supplier_part_number. When…

**System answer:**
> In the procurement process flow modeled here, the Purchase Order is represented at two levels: `PURCHASE_ORDER` (purchase order header) and `PURCHASE_ORDER_LINE` (purchase order line items).

A purchase order header (`PURCHASE_ORDER`, keyed by `po_id`) provides the order-level reference information and status/amounts. The item-level details of that same purchase order are stored in `PURCHASE_ORDER…

**Sources retrieved (12):** `Purchase Receipt→PURCHASE_RECEIPT`, `Purchase Receipt Line→PURCHASE_RECEIPT_LINE`, `Purchase Order Line→PURCHASE_ORDER_LINE`, `Purchase Order Header→PURCHASE_ORDER`, `Purchase Order Line`, `parent_chunk_complex_scenarios.md_6`, `Purchase Receipt`, `parent_chunk_complex_scenarios.md_13`

**Context previews (first 3):**

1. _Business concept 'Purchase Receipt' — The table is explicitly named purchase_receipt and contains core receipt attributes such as receipt_id/receipt_number, receipt_date, po_id (purchase order referen…_

2. _Business concept 'Purchase Receipt Line' — The table is explicitly keyed by receipt_line_id and receipt_id (referencing purchase_receipt) and contains line-level receiving quantities (quantity_receive…_

3. _Business concept 'Purchase Order Line' — The table name and core columns (po_id, line_number, product_id, quantity_ordered/received/invoiced, unit_price, discounts, tax, line_total, promised_date, sta…_

---

### ✅ QA-012 — How does the general ledger and accounting system work?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.5276 | **Gate:** `proceed`

**Expected answer:**
> The GL is built on account_type (DEBIT or CREDIT balance_type), general_ledger_account (with hierarchical parent_account_id self-reference and status ACTIVE/INACTIVE), and accounting_period (with fiscal_year, start/end dates, and is_closed flag). Journal entries (journal_entry) reference a period, h…

**System answer:**
> Based on the retrieved context, the general ledger and accounting system works by linking journal activity to ledger accounts, accounting periods, budgets, and organizational departments, and then aggregating those amounts across an account hierarchy.

Journal activity is stored in `JOURNAL_ENTRY` (columns include `entry_id`, `entry_number`, `entry_date`, `period_id`, `entry_type`, `currency`, `to…

**Sources retrieved (12):** `Joins 7 tables: Account Type → General Ledger Account (self-join for hierarchy) → Journal Entry → Journal Entry Line → Accounting Period → Budget → Department→GENERAL_LEDGER_ACCOUNT`, `Joins 7 tables: Account Type → General Ledger Account (self-join for hierarchy) → Journal Entry → Journal Entry Line → Accounting Period → Budget → Department→JOURNAL_ENTRY_LINE`, `Joins 7 tables: Account Type → General Ledger Account (self-join for hierarchy) → Journal Entry → Journal Entry Line → Accounting Period → Budget → Department→JOURNAL_ENTRY`, `Joins 7 tables: Account Type → General Ledger Account (self-join for hierarchy) → Journal Entry → Journal Entry Line → Accounting Period → Budget → Department`, `parent_chunk_complex_scenarios.md_18`, `Accounting_Period→ACCOUNTING_PERIOD`, `parent_chunk_business_glossary.md_1`, `parent_chunk_complex_scenarios.md_12`

**Context previews (first 3):**

1. _Business concept 'Joins 7 tables: Account Type → General Ledger Account (self-join for hierarchy) → Journal Entry → Journal Entry Line → Accounting Period → Budget → Department' is implemented by phys…_

2. _Business concept 'Joins 7 tables: Account Type → General Ledger Account (self-join for hierarchy) → Journal Entry → Journal Entry Line → Accounting Period → Budget → Department' is implemented by phys…_

3. _Business concept 'Joins 7 tables: Account Type → General Ledger Account (self-join for hierarchy) → Journal Entry → Journal Entry Line → Accounting Period → Budget → Department' is implemented by phys…_

---

### ✅ QA-013 — How are accounts receivable and accounts payable tracked?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.1800 | **Gate:** `proceed_with_warning`

**Expected answer:**
> Accounts receivable (accounts_receivable) links to customer_id and invoice_id, tracking amount_original, amount_due, due_date, and a computed days_overdue column. Status values are CURRENT/DUE/OVERDUE/COLLECTION/WRITE_OFF, with collection_status and next_action_date for collections workflow. Account…

**System answer:**
> Accounts payable is explicitly tracked by the business concept “Accounts Payable”, implemented by the physical table `ACCOUNTS_PAYABLE` / `accounts_payable`. This table includes AP-specific attributes such as `supplier_id`, `invoice_id`, `amount_original`, `amount_due`, `invoice_date`, `due_date`, `discount_available`, `discount_until`, `payment_terms`, `status`, `payment_priority`, and `payment_d…

**Sources retrieved (12):** `Accounts Payable→ACCOUNTS_PAYABLE`, `Purchase Receipt Line→PURCHASE_RECEIPT_LINE`, `the complete order-to-cash cycle for high-value customers who purchase products from multiple categories, tracking from sales order through payment collection→SALES_ORDER`, `Purchase Receipt→PURCHASE_RECEIPT`, `Accounts Payable`, `parent_chunk_complex_scenarios.md_6`, `parent_chunk_complex_scenarios.md_11`, `parent_chunk_business_glossary.md_1`

**Context previews (first 3):**

1. _Business concept 'Accounts Payable' — The table is explicitly named accounts_payable and contains typical AP attributes such as supplier_id, invoice_id, amount_due, due_date, discount terms, and payme…_

2. _Business concept 'Purchase Receipt Line' — The table is explicitly keyed by receipt_line_id and receipt_id (referencing purchase_receipt) and contains line-level receiving quantities (quantity_receive…_

3. _Business concept 'the complete order-to-cash cycle for high-value customers who purchase products from multiple categories, tracking from sales order through payment collection' is implemented by phys…_

---

### ✅ QA-014 — How is the employee and organizational structure represented?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.2711 | **Gate:** `proceed`

**Expected answer:**
> The department table has hierarchical parent_department_id self-reference with status ACTIVE/INACTIVE. Positions (position table) belong to departments via department_id FK, with grade_level, salary range (min/max), and FLSA status (EXEMPT/NON_EXEMPT). Employees reference department_id, position_id,…

**System answer:**
> The employee and organizational structure is represented in the schema primarily through the EMPLOYEE table, which stores core employee master data and organizational relationship fields. Specifically, the EMPLOYEE table includes department_id, position_id, and manager_id to capture an employee’s Department, Position, and Manager relationships, along with employment details (e.g., hire_date, termi…

**Sources retrieved (12):** `Employee Record→EMPLOYEE`, `Job Position→POSITION`, `User Account`, `User Account→APP_USER`, `parent_chunk_business_glossary.md_2`, `Employee Record`, `Job Position`, `parent_chunk_business_glossary.md_3`

**Context previews (first 3):**

1. _Business concept 'Employee Record' — The table stores core employee master data (employee identifiers, personal details, employment dates, status) and organizational relationships (department, positio…_

2. _Business concept 'Job Position' — The table stores detailed attributes of a specific organizational position (position_id/code/title), including responsibilities/description and compensation range (mi…_

3. _User Account: The table stores core identity and authentication attributes such as username, email, user_type, status, last_login_date, and failed_login_attempts, which directly represent a user accou…_

---

### ✅ QA-015 — How does the shipment and logistics system work?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0860 | **Gate:** `proceed_with_warning`

**Expected answer:**
> Carriers (carrier table) are classified by type: LTL/FTL/PARCEL/AIR/OCEAN/RAIL with rating (0-5). Shipping routes define paths between warehouses (origin_location_id, destination_location_id both FK to warehouse) with distance_km, estimated_hours, and cost_per_km. Shipments reference origin/destinat…

**System answer:**
> From the available knowledge graph, the shipment and logistics portion is represented at two levels: shipment “headers” and shipment “lines,” plus inter-warehouse stock movement.

A shipment itself is stored in the physical table SHIPMENT, which includes logistics and routing/destination attributes such as origin_location_id and destination_location_id (the business concept “Shipment.destination_l…

**Sources retrieved (12):** `Shipment Line→SHIPMENT_LINE`, `Shipment.destination_location_id→SHIPMENT`, `Stock Transfer→STOCK_TRANSFER`, `parent_chunk_business_glossary.md_3`, `Shipment Line`, `parent_chunk_business_glossary.md_1`, `parent_chunk_business_glossary.md_0`, `parent_chunk_complex_scenarios.md_7`

**Context previews (first 3):**

1. _Business concept 'Shipment Line' — The table is keyed by shipment_line_id and links to shipment via shipment_id, with line_number, product_id, quantity, and unit_of_measure—typical attributes of indiv…_

2. _Business concept 'Shipment.destination_location_id' is implemented by physical table SHIPMENT (columns: shipment_id, shipment_number, shipment_type, origin_location_id, destination_location_id, refere…_

3. _Business concept 'Stock Transfer' — The table explicitly stores inter-warehouse movement details (from_warehouse_id, to_warehouse_id), along with transfer and required dates, shipment method, tracking…_

---

### ✅ QA-016 — How does the project management module work?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0070 | **Gate:** `proceed_with_warning`

**Expected answer:**
> Projects link to customer_id (for customer-facing projects) and project_manager_id (FK to employee). Project types are CUSTOMER/INTERNAL/R&D/CAPITAL with status PLANNING/ACTIVE/ON_HOLD/COMPLETED/CANCELLED and priority levels. Projects track budget_amount vs actual_cost. Project tasks (project_task) …

**System answer:**
> I cannot find this information in the knowledge graph.

**Sources retrieved (12):** `Prepare project status report for customer steering committee→PROJECT`, `BOMs, account hierarchies, project task hierarchies→PROJECT_TASK`, `Employee Time Entry→TIME_ENTRY`, `A specific work item within a project that must be completed.→WORK_ORDER`, `parent_chunk_complex_scenarios.md_18`, `parent_chunk_business_glossary.md_2`, `parent_chunk_complex_scenarios.md_15`, `parent_chunk_complex_scenarios.md_17`

**Context previews (first 3):**

1. _Business concept 'Prepare project status report for customer steering committee' is implemented by physical table PROJECT (columns: project_id, project_code, project_name, project_type, customer_id, p…_

2. _Business concept 'BOMs, account hierarchies, project task hierarchies' is implemented by physical table PROJECT_TASK (columns: task_id, project_id, task_number, task_name, parent_task_id, assigned_to,…_

3. _Business concept 'Employee Time Entry' — The table captures a per-employee, per-day record of hours worked (employee_id, work_date, hours_worked) with optional work categorization and an approval work…_

---

### ✅ QA-017 — How does the system handle user authentication, roles, and permissions?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.5034 | **Gate:** `proceed`

**Expected answer:**
> The app_user table links to employee_id, customer_id, or supplier_id depending on user_type (EMPLOYEE/CUSTOMER/SUPPLIER/ADMIN). Users have status ACTIVE/INACTIVE/LOCKED/PENDING with failed_login_attempts tracking. Roles (role table) are typed as SYSTEM/BUSINESS/CUSTOM with ACTIVE/INACTIVE status. Th…

**System answer:**
> User authentication is represented by the **APP_USER** table, which stores identity and authentication attributes such as **username**, **email**, **user_type**, **status**, **last_login_date**, **failed_login_attempts**, and **password_changed_date** (along with other profile fields).  

Roles and role hierarchy/assignments are represented by the **USER_ROLE** table, which links a user to a role …

**Sources retrieved (12):** `User, Permission, Role Hierarchy→USER_ROLE`, `User Account`, `User Account→APP_USER`, `Employee Record→EMPLOYEE`, `User, Permission, Role Hierarchy`, `parent_chunk_business_glossary.md_4`, `Employee Record`, `parent_chunk_complex_scenarios.md_15`

**Context previews (first 3):**

1. _Business concept 'User, Permission, Role Hierarchy' is implemented by physical table USER_ROLE (columns: user_role_id, user_id, role_id, assigned_date, assigned_by, expiry_date, status).…_

2. _User Account: The table stores core identity and authentication attributes such as username, email, user_type, status, last_login_date, and failed_login_attempts, which directly represent a user accou…_

3. _Business concept 'User Account' — The table stores core identity and authentication attributes such as username, email, user_type, status, last_login_date, and failed_login_attempts, which directly re…_

---

### ✅ QA-018 — What is the complete path from a customer placing an order to the product being shipped?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.3521 | **Gate:** `proceed`

**Expected answer:**
> The order-to-ship path traverses: customer → sales_order (via customer_id FK) → sales_order_line (via order_id FK) → product (via product_id FK). For fulfillment: sales_order references warehouse_id for the fulfillment location. Inventory is checked via inventory_on_hand (product_id + warehouse_id).…

**System answer:**
> From a customer placing an order, the available schema path is:

A customer is represented in the order-to-cash flow by `SALES_ORDER` via `SALES_ORDER.customer_id`. That order contains line items in `SALES_ORDER_LINE`, which are tied to the order by `SALES_ORDER_LINE.order_id` and identify the ordered product via `SALES_ORDER_LINE.product_id`. The shipped product is represented at the shipment ite…

**Sources retrieved (12):** `the complete order-to-cash cycle for high-value customers who purchase products from multiple categories, tracking from sales order through payment collection→SALES_ORDER`, `Sales Order Line→SALES_ORDER_LINE`, `Shipment Line→SHIPMENT_LINE`, `Customer Invoice→INVOICE`, `Joins 8 tables: Product → Bill of Materials (self-join for multi-level) → Work Order → Work Order Material → Production Schedule → Production Line → Quality Inspection → Inventory Transaction→QUALITY_INSPECTION`, `the complete order-to-cash cycle for high-value customers who purchase products from multiple categories, tracking from sales order through payment collection`, `parent_chunk_complex_scenarios.md_5`, `parent_chunk_business_glossary.md_0`

**Context previews (first 3):**

1. _Business concept 'the complete order-to-cash cycle for high-value customers who purchase products from multiple categories, tracking from sales order through payment collection' is implemented by phys…_

2. _Business concept 'Sales Order Line' — The table contains order line identifiers (line_id, line_number) tied to a parent sales order (order_id) and captures product, ordered/shipped/invoiced quantities…_

3. _Business concept 'Shipment Line' — The table is keyed by shipment_line_id and links to shipment via shipment_id, with line_number, product_id, quantity, and unit_of_measure—typical attributes of indiv…_

---

### ✅ QA-019 — How does the schema support supplier contracts and their relationship to purchase orders?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.5185 | **Gate:** `proceed`

**Expected answer:**
> The supplier_contract table links to supplier_id FK, with contract_type (FIXED_PRICE/COST_PLUS/RATE_BASED/FRAMEWORK), start/end dates, auto_renew flag, payment_terms, total_value, and status (DRAFT/ACTIVE/EXPIRED/TERMINATED). Purchase orders independently link to the same supplier via supplier_id FK…

**System answer:**
> The schema supports supplier contracts through the physical table **SUPPLIER_CONTRACT**, which implements the business concept **“Supplier Contract”** by storing contract-level identifiers and commercial terms such as **contract_number, supplier_id, contract_type, start_date/end_date, payment_terms, currency, total_value, status, and auto_renew** (plus **contract_id** and timestamps like **created…

**Sources retrieved (12):** `Supplier Contract→SUPPLIER_CONTRACT`, `Purchase Order Line`, `Purchase Order Line→PURCHASE_ORDER_LINE`, `Purchase Order Header→PURCHASE_ORDER`, `Purchase Receipt Line→PURCHASE_RECEIPT_LINE`, `parent_chunk_complex_scenarios.md_6`, `parent_chunk_complex_scenarios.md_13`, `Supplier Contract`

**Context previews (first 3):**

1. _Business concept 'Supplier Contract' — The table stores contract-level identifiers and commercial terms (contract_number, supplier_id, contract_type, start_date/end_date, payment_terms, currency, tota…_

2. _Purchase Order Line: The table name and core columns (po_id, line_number, product_id, quantity_ordered/received/invoiced, unit_price, discounts, tax, line_total, promised_date, status) directly model …_

3. _Business concept 'Purchase Order Line' — The table name and core columns (po_id, line_number, product_id, quantity_ordered/received/invoiced, unit_price, discounts, tax, line_total, promised_date, sta…_

---

### ✅ QA-020 — What self-referencing hierarchies exist in the schema?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0152 | **Gate:** `proceed_with_warning`

**Expected answer:**
> The schema has five self-referencing hierarchies: (1) product_category.parent_category_id → product_category.category_id for nested product classifications; (2) general_ledger_account.parent_account_id → general_ledger_account.account_id for chart of accounts hierarchy; (3) department.parent_departm…

**System answer:**
> The retrieved context shows these self-referencing (hierarchical) structures:

In the chart of accounts, the business concept “Joins 7 tables: Account Type → General Ledger Account (self-join for hierarchy) → …” indicates a self-join hierarchy for `GENERAL_LEDGER_ACCOUNT`, supported by the `parent_account_id` column in `GENERAL_LEDGER_ACCOUNT`.

For product structure, the business concept “Joins 8…

**Sources retrieved (12):** `Joins 7 tables: Account Type → General Ledger Account (self-join for hierarchy) → Journal Entry → Journal Entry Line → Accounting Period → Budget → Department→JOURNAL_ENTRY_LINE`, `parent_chunk_complex_scenarios.md_18`, `Joins 7 tables: Account Type → General Ledger Account (self-join for hierarchy) → Journal Entry → Journal Entry Line → Accounting Period → Budget → Department`, `Joins 7 tables: Account Type → General Ledger Account (self-join for hierarchy) → Journal Entry → Journal Entry Line → Accounting Period → Budget → Department→JOURNAL_ENTRY`, `Joins 7 tables: Account Type → General Ledger Account (self-join for hierarchy) → Journal Entry → Journal Entry Line → Accounting Period → Budget → Department→GENERAL_LEDGER_ACCOUNT`, `Joins 8 tables: Product → Bill of Materials (self-join for multi-level) → Work Order → Work Order Material → Production Schedule → Production Line → Quality Inspection → Inventory Transaction→QUALITY_INSPECTION`, `BOMs, account hierarchies, project task hierarchies→PROJECT_TASK`, `parent_chunk_business_glossary.md_2`

**Context previews (first 3):**

1. _Business concept 'Joins 7 tables: Account Type → General Ledger Account (self-join for hierarchy) → Journal Entry → Journal Entry Line → Accounting Period → Budget → Department' is implemented by phys…_

2. _## Performance Testing Considerations  These scenarios are designed to test the following aspects of a GraphRAG system: 1. **Multi-Hop Query Performance**: Each scenario requires 6-10 table joins 2. *…_

3. _Joins 7 tables: Account Type → General Ledger Account (self-join for hierarchy) → Journal Entry → Journal Entry Line → Accounting Period → Budget → Department…_

---

### ✅ QA-021 — How does the price list system work for products?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.5272 | **Gate:** `proceed`

**Expected answer:**
> The price_list table defines named price lists with currency, effective_date, expiration_date, and status. The product_price junction table links products to price lists with price, minimum_quantity (for volume pricing), discount_percentage, and effective_date. A UNIQUE constraint on (product_id, pr…

**System answer:**
> In this schema, product pricing is driven by two main structures: the price list itself and the product-specific rates assigned to it.

First, the table `PRICE_LIST` defines the “price list system” settings. It includes `price_list_id` (the identifier), `price_list_name`, `currency`, and the validity window fields `effective_date` and `expiration_date`, plus a `status`. This supports different cre…

**Sources retrieved (12):** `Fixed-price pricing model→PRODUCT_PRICE`, `different credit terms and pricing structures→PRICE_LIST`, `Finished goods raw materials services→PRODUCT`, `Purchase Order Line`, `Fixed-price pricing model`, `parent_chunk_business_glossary.md_0`, `Finished goods raw materials services`, `parent_chunk_complex_scenarios.md_5`

**Context previews (first 3):**

1. _Business concept 'Fixed-price pricing model' — product_price defines product-specific prices tied to a price_list_id, with effective_date validity windows, minimum_quantity breaks, and discount_percen…_

2. _Business concept 'different credit terms and pricing structures' is implemented by physical table PRICE_LIST (columns: price_list_id, price_list_name, currency, effective_date, expiration_date, status…_

3. _Business concept 'Finished goods raw materials services' — The table is a master data record for sellable/managed items with an explicit product_type that supports finished goods, raw materials, and s…_

---

### ✅ QA-022 — What CHECK constraints on status columns exist across the major tables?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0110 | **Gate:** `proceed_with_warning`

**Expected answer:**
> Key status CHECK constraints include: customer (ACTIVE/INACTIVE/SUSPENDED), product (ACTIVE/DISCONTINUED/PHASE_OUT), sales_order (DRAFT/CONFIRMED/PICKED/SHIPPED/INVOICED/CANCELLED), purchase_order (DRAFT/SUBMITTED/ACKNOWLEDGED/PARTIAL/RECEIVED/CLOSED/CANCELLED), work_order (DRAFT/RELEASED/IN_PROGRES…

**System answer:**
> I cannot find this information in the knowledge graph.

**Sources retrieved (12):** `Joins 8 tables: Product → Bill of Materials (self-join for multi-level) → Work Order → Work Order Material → Production Schedule → Production Line → Quality Inspection → Inventory Transaction→QUALITY_INSPECTION`, `Customer Master→CUSTOMER`, `Purchase Order Line→PURCHASE_ORDER_LINE`, `Job costing materials→WORK_ORDER_MATERIAL`, `Purchase Order Line`, `Purchase Order Header→PURCHASE_ORDER`, `Finished goods raw materials services→PRODUCT`, `Supplier Contract→SUPPLIER_CONTRACT`

**Context previews (first 3):**

1. _Business concept 'Joins 8 tables: Product → Bill of Materials (self-join for multi-level) → Work Order → Work Order Material → Production Schedule → Production Line → Quality Inspection → Inventory Tr…_

2. _Business concept 'Customer Master' — The table implements core customer master data via customer_id/customer_number, customer_name, tax_id, registration_date, status, and customer_type_id. Credit_limi…_

3. _Business concept 'Purchase Order Line' — The table name and core columns (po_id, line_number, product_id, quantity_ordered/received/invoiced, unit_price, discounts, tax, line_total, promised_date, sta…_

---

### ✅ QA-023 — How does the stock transfer process work between warehouses?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.9475 | **Gate:** `proceed`

**Expected answer:**
> Stock transfers use the stock_transfer table with from_warehouse_id and to_warehouse_id (both FK to warehouse), transfer_date, shipment_method, tracking_number, and status (DRAFT/PICKED/SHIPPED/RECEIVED/CANCELLED). Individual items are tracked via stock_transfer_line with from_bin_id and to_bin_id (…

**System answer:**
> The stock transfer between warehouses is represented in two related tables: `STOCK_TRANSFER` (the transfer “header”) and `STOCK_TRANSFER_LINE` (the per-product “lines”).

In `STOCK_TRANSFER`, the process is defined at the warehouse-to-warehouse level by `from_warehouse_id` and `to_warehouse_id`, plus scheduling and logistics details such as `transfer_date`, `required_date`, `shipment_method`, `tra…

**Sources retrieved (12):** `Stock Transfer→STOCK_TRANSFER`, `Stock Transfer Line→STOCK_TRANSFER_LINE`, `Joins 8 tables: Product → Bill of Materials (self-join for multi-level) → Work Order → Work Order Material → Production Schedule → Production Line → Quality Inspection → Inventory Transaction→QUALITY_INSPECTION`, `Warehouse Zone→WAREHOUSE_ZONE`, `Stock Transfer`, `parent_chunk_business_glossary.md_1`, `parent_chunk_complex_scenarios.md_7`, `Stock Transfer Line`

**Context previews (first 3):**

1. _Business concept 'Stock Transfer' — The table explicitly stores inter-warehouse movement details (from_warehouse_id, to_warehouse_id), along with transfer and required dates, shipment method, tracking…_

2. _Business concept 'Stock Transfer Line' — The table is explicitly line-level for an inventory transfer, linked to a transfer header via transfer_id and capturing movement quantities per product. It rec…_

3. _Business concept 'Joins 8 tables: Product → Bill of Materials (self-join for multi-level) → Work Order → Work Order Material → Production Schedule → Production Line → Quality Inspection → Inventory Tr…_

---

### ✅ QA-024 — How are production lines defined and what types exist?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.6110 | **Gate:** `proceed`

**Expected answer:**
> The production_line table defines manufacturing resources with line_code (UNIQUE), line_name, line_type (ASSEMBLY/DISCRETE/PROCESS/MIXING via CHECK), location_id (FK to warehouse for the physical location), capacity_per_hour, setup_time_minutes, and status (ACTIVE/MAINTENANCE/INACTIVE). Production l…

**System answer:**
> Production lines are defined by the business concept “Production Line,” implemented in the physical table `PRODUCTION_LINE` with columns `line_id`, `line_code`, `line_name`, `line_type`, `location_id`, `capacity_per_hour`, `setup_time_minutes`, `status`, and `created_at`.

The context indicates that “types” of production lines are represented by the `line_type` attribute in `PRODUCTION_LINE`, but …

**Sources retrieved (12):** `Production Line→PRODUCTION_LINE`, `Joins 8 tables: Product → Bill of Materials (self-join for multi-level) → Work Order → Work Order Material → Production Schedule → Production Line → Quality Inspection → Inventory Transaction→QUALITY_INSPECTION`, `A specific work item within a project that must be completed.→WORK_ORDER`, `Joins 8 tables: Product → Bill of Materials (self-join for multi-level) → Work Order → Work Order Material → Production Schedule → Production Line → Quality Inspection → Inventory Transaction→BILL_OF_MATERIALS`, `Joins 8 tables: Product → Bill of Materials (self-join for multi-level) → Work Order → Work Order Material → Production Schedule → Production Line → Quality Inspection → Inventory Transaction`, `Scheduled Production Time→PRODUCTION_SCHEDULE`, `parent_chunk_complex_scenarios.md_9`, `parent_chunk_complex_scenarios.md_8`

**Context previews (first 3):**

1. _Business concept 'Production Line' is implemented by physical table PRODUCTION_LINE (columns: line_id, line_code, line_name, line_type, location_id, capacity_per_hour, setup_time_minutes, status, crea…_

2. _Business concept 'Joins 8 tables: Product → Bill of Materials (self-join for multi-level) → Work Order → Work Order Material → Production Schedule → Production Line → Quality Inspection → Inventory Tr…_

3. _Business concept 'A specific work item within a project that must be completed.' — A specific work item within a project that must be completed. is implemented by physical table WORK_ORDER (columns: w…_

---

### ✅ QA-025 — How does the budget system integrate with the financial accounts?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0169 | **Gate:** `proceed_with_warning`

**Expected answer:**
> The budget table links to both department_id and account_id (FK to general_ledger_account). It tracks budget_type (OPERATING/CAPITAL/PROJECT), fiscal_year, budgeted_amount, actual_amount, and a computed variance column (budgeted minus actual). Budget status follows DRAFT/APPROVED/ACTIVE/CLOSED. This…

**System answer:**
> Within the knowledge graph, the integration points between the budget data and the financial-accounting data are shown at the schema level by shared fields and by the stated join path.

The business concept “Budget Variance Analysis - Q1 2024” is implemented by table BUDGET, which includes an `account_id` column (along with `budgeted_amount`, `actual_amount`, and `variance`). The financial-account…

**Sources retrieved (12):** `Budget Variance Analysis - Q1 2024→BUDGET`, `Joins 7 tables: Account Type → General Ledger Account (self-join for hierarchy) → Journal Entry → Journal Entry Line → Accounting Period → Budget → Department→JOURNAL_ENTRY`, `Joins 7 tables: Account Type → General Ledger Account (self-join for hierarchy) → Journal Entry → Journal Entry Line → Accounting Period → Budget → Department→JOURNAL_ENTRY_LINE`, `Joins 7 tables: Account Type → General Ledger Account (self-join for hierarchy) → Journal Entry → Journal Entry Line → Accounting Period → Budget → Department→GENERAL_LEDGER_ACCOUNT`, `parent_chunk_complex_scenarios.md_11`, `parent_chunk_business_glossary.md_2`, `parent_chunk_complex_scenarios.md_12`, `parent_chunk_complex_scenarios.md_16`

**Context previews (first 3):**

1. _Business concept 'Budget Variance Analysis - Q1 2024' is implemented by physical table BUDGET (columns: budget_id, budget_name, budget_type, fiscal_year, department_id, account_id, budgeted_amount, ac…_

2. _Business concept 'Joins 7 tables: Account Type → General Ledger Account (self-join for hierarchy) → Journal Entry → Journal Entry Line → Accounting Period → Budget → Department' is implemented by phys…_

3. _Business concept 'Joins 7 tables: Account Type → General Ledger Account (self-join for hierarchy) → Journal Entry → Journal Entry Line → Accounting Period → Budget → Department' is implemented by phys…_

---

### ✅ QA-026 — What computed/generated columns exist in the schema?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0105 | **Gate:** `proceed_with_warning`

**Expected answer:**
> The schema has three computed columns using GENERATED ALWAYS AS: (1) inventory_on_hand.quantity_available = quantity_on_hand - quantity_allocated; (2) accounts_receivable.days_overdue = DATEDIFF(CURRENT_DATE, due_date); (3) budget.variance = budgeted_amount - actual_amount. All are STORED (materiali…

**System answer:**
> I cannot find this information in the knowledge graph.

**Sources retrieved (12):** `Scheduled Production Time→PRODUCTION_SCHEDULE`, `Budget Variance Analysis - Q1 2024→BUDGET`, `Purchase Order Line`, `Recent NCRs: 3 non-conformance reports in last 6 months→NON_CONFORMANCE_REPORT`, `Joins 7 tables: Account Type → General Ledger Account (self-join for hierarchy) → Journal Entry → Journal Entry Line → Accounting Period → Budget → Department→JOURNAL_ENTRY_LINE`, `Payment Record→PAYMENT`, `the complete order-to-cash cycle for high-value customers who purchase products from multiple categories, tracking from sales order through payment collection→SALES_ORDER`, `Department→DEPARTMENT`

**Context previews (first 3):**

1. _Business concept 'Scheduled Production Time' is implemented by physical table PRODUCTION_SCHEDULE (columns: schedule_id, work_order_id, production_line_id, scheduled_start, scheduled_end, actual_start…_

2. _Business concept 'Budget Variance Analysis - Q1 2024' is implemented by physical table BUDGET (columns: budget_id, budget_name, budget_type, fiscal_year, department_id, account_id, budgeted_amount, ac…_

3. _Purchase Order Line: The table name and core columns (po_id, line_number, product_id, quantity_ordered/received/invoiced, unit_price, discounts, tax, line_total, promised_date, status) directly model …_

---

### ✅ QA-027 — How are customer addresses and contacts structured?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.4708 | **Gate:** `proceed`

**Expected answer:**
> Customer addresses are stored in customer_address with address_type (BILLING/SHIPPING/BOTH via CHECK), full address fields (line1, line2, city, state, postal_code, country_code), and is_default flag. The customer_id FK has ON DELETE CASCADE. Customer contacts are in customer_contact with contact_nam…

**System answer:**
> Customer addresses are structured as address records that belong to a customer via a `customer_id` foreign key to the `customer` entity. The address attributes include `address_type`, `address_line1`, `address_line2`, `city`, `state`, `postal_code`, and `country_code`, plus an `is_default` flag. In the physical schema, this is implemented by the table `CUSTOMER_ADDRESS` with columns `address_id, c…

**Sources retrieved (12):** `Customer Address`, `Customer Address→CUSTOMER_ADDRESS`, `Customer Address→SUPPLIER_ADDRESS`, `Duplicate Contact Records→CUSTOMER_CONTACT`, `Customer Master→CUSTOMER`, `User Account`, `Duplicate Contact Records`, `parent_chunk_complex_scenarios.md_10`

**Context previews (first 3):**

1. _Customer Address: The table name and foreign key (customer_id → customer) indicate it stores address records belonging to customers. It includes standard address attributes (address_type, address_line…_

2. _Business concept 'Customer Address' — The table name and foreign key (customer_id → customer) indicate it stores address records belonging to customers. It includes standard address attributes (addres…_

3. _Business concept 'Customer Address' — The table name and foreign key (customer_id → customer) indicate it stores address records belonging to customers. It includes standard address attributes (addres…_

---

### ✅ QA-028 — What CASCADE rules exist in the schema and what tables use them?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0102 | **Gate:** `proceed_with_warning`

**Expected answer:**
> ON DELETE CASCADE is used on child tables that should be automatically removed when the parent is deleted: customer_address and customer_contact (cascade from customer), supplier_address and supplier_contact (cascade from supplier), sales_order_line (cascade from sales_order), purchase_order_line (c…

**System answer:**
> I cannot find this information in the knowledge graph.

**Sources retrieved (12):** `Employee Time Entry→TIME_ENTRY`, `Joins 8 tables: Product → Bill of Materials (self-join for multi-level) → Work Order → Work Order Material → Production Schedule → Production Line → Quality Inspection → Inventory Transaction`, `User, Permission, Role Hierarchy→USER_ROLE`, `Joins 7 tables: Account Type → General Ledger Account (self-join for hierarchy) → Journal Entry → Journal Entry Line → Accounting Period → Budget → Department`, `User Account`, `Employee Time Entry`, `parent_chunk_complex_scenarios.md_15`, `parent_chunk_complex_scenarios.md_13`

**Context previews (first 3):**

1. _Business concept 'Employee Time Entry' — The table captures a per-employee, per-day record of hours worked (employee_id, work_date, hours_worked) with optional work categorization and an approval work…_

2. _Joins 8 tables: Product → Bill of Materials (self-join for multi-level) → Work Order → Work Order Material → Production Schedule → Production Line → Quality Inspection → Inventory Transaction…_

3. _Business concept 'User, Permission, Role Hierarchy' is implemented by physical table USER_ROLE (columns: user_role_id, user_id, role_id, assigned_date, assigned_by, expiry_date, status).…_

---

### ✅ QA-029 — How does the schema link quality inspections to their source documents?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0604 | **Gate:** `proceed_with_warning`

**Expected answer:**
> Quality inspections use a polymorphic reference pattern: reference_type (VARCHAR) identifies the source table (e.g., 'purchase_receipt', 'work_order') and reference_id (INT) stores the primary key of that source record. The inspection also directly references product_id and warehouse_id via foreign …

**System answer:**
> The retrieved context shows that the physical table `QUALITY_INSPECTION` includes the columns `reference_type` and `reference_id`, alongside `product_id` and other inspection attributes. This indicates that quality inspections are associated to some “referenced record” via these fields.

However, the context does not explicitly specify which specific source-document tables/keys `reference_type` an…

**Sources retrieved (12):** `Joins 8 tables: Product → Bill of Materials (self-join for multi-level) → Work Order → Work Order Material → Production Schedule → Production Line → Quality Inspection → Inventory Transaction→QUALITY_INSPECTION`, `Joins 8 tables: Product → Bill of Materials (self-join for multi-level) → Work Order → Work Order Material → Production Schedule → Production Line → Quality Inspection → Inventory Transaction`, `Joins 8 tables: Product → Bill of Materials (self-join for multi-level) → Work Order → Work Order Material → Production Schedule → Production Line → Quality Inspection → Inventory Transaction→BILL_OF_MATERIALS`, `Purchase Receipt Line→PURCHASE_RECEIPT_LINE`, `parent_chunk_business_glossary.md_3`, `parent_chunk_complex_scenarios.md_9`, `parent_chunk_complex_scenarios.md_13`, `parent_chunk_complex_scenarios.md_6`

**Context previews (first 3):**

1. _Business concept 'Joins 8 tables: Product → Bill of Materials (self-join for multi-level) → Work Order → Work Order Material → Production Schedule → Production Line → Quality Inspection → Inventory Tr…_

2. _Joins 8 tables: Product → Bill of Materials (self-join for multi-level) → Work Order → Work Order Material → Production Schedule → Production Line → Quality Inspection → Inventory Transaction…_

3. _Business concept 'Joins 8 tables: Product → Bill of Materials (self-join for multi-level) → Work Order → Work Order Material → Production Schedule → Production Line → Quality Inspection → Inventory Tr…_

---

### ⛔ QA-030 — How does the journal entry enforce double-entry bookkeeping?

**Status:** ABSTAINED  
**GT Coverage:** 100% | **Top Score:** 0.0000 | **Gate:** `abstain_early`

**Expected answer:**
> The journal_entry table requires total_debit and total_credit columns to be present (both NOT NULL DECIMAL 15,2). Journal_entry_line items each reference a general_ledger_account and have a CHECK constraint ensuring exactly one of debit_amount or credit_amount is positive: CHECK ((debit_amount > 0 A…

**System answer:**
> I cannot find this information in the knowledge graph.

---

### ⛔ QA-031 — What types of non-conformance reports exist and what is their lifecycle?

**Status:** ABSTAINED  
**GT Coverage:** 100% | **Top Score:** 0.0000 | **Gate:** `abstain_early`

**Expected answer:**
> Non-conformance reports (NCRs) have four types via CHECK: PRODUCT, PROCESS, DOCUMENTATION, and SUPPLIER. Severity is classified as MINOR/MAJOR/CRITICAL. The status lifecycle is OPEN → IN_PROGRESS → CLOSED → VERIFIED. NCRs track root_cause, corrective_action, and preventive_action (all TEXT fields) f…

**System answer:**
> I cannot find this information in the knowledge graph.

---

### ⛔ QA-032 — How does the purchase receipt track rejected quantities and lot information?

**Status:** ABSTAINED  
**GT Coverage:** 100% | **Top Score:** 0.0000 | **Gate:** `abstain_early`

**Expected answer:**
> The purchase_receipt_line table tracks three quantity measures: quantity_ordered, quantity_received, and quantity_rejected. When quantity_rejected > 0, materials failed inspection. Each receipt line also records lot_number (for lot traceability), expiration_date (for perishable items), location_id (…

**System answer:**
> I cannot find this information in the knowledge graph.

---

### ⛔ QA-033 — What UNIQUE constraints exist across the schema and what do they enforce?

**Status:** ABSTAINED  
**GT Coverage:** 100% | **Top Score:** 0.0000 | **Gate:** `abstain_early`

**Expected answer:**
> Key UNIQUE constraints include: customer.customer_number, product.product_number, supplier.supplier_number (business identifiers); invoice.invoice_number, payment.payment_number, shipment.shipment_number (document numbers); sales_order.order_number, purchase_order.po_number; warehouse.warehouse_code…

**System answer:**
> I cannot find this information in the knowledge graph.

---

### ⛔ QA-034 — How does the schema handle the relationship between employees, departments, and projects?

**Status:** ABSTAINED  
**GT Coverage:** 100% | **Top Score:** 0.0000 | **Gate:** `abstain_early`

**Expected answer:**
> Employees belong to departments via department_id FK and hold positions via position_id FK. Positions also reference department_id, creating a redundant but verifiable link. Employee.manager_id (self-referencing FK) creates reporting chains. Projects link to project_manager_id (FK to employee) and o…

**System answer:**
> I cannot find this information in the knowledge graph.

---

### ⛔ QA-035 — What is the relationship between sales orders, invoices, and payments?

**Status:** ABSTAINED  
**GT Coverage:** 100% | **Top Score:** 0.0000 | **Gate:** `abstain_early`

**Expected answer:**
> Sales orders are invoiced by creating invoice records with order_id FK referencing sales_order. Invoice line items (invoice_line) can link back to specific sales_order_line items via order_line_id FK. Payments reference invoice_id FK to settle invoices. The invoice tracks amount_paid and balance_due…

**System answer:**
> I cannot find this information in the knowledge graph.

---

### ⛔ QA-036 — What types of inventory transactions does the system track?

**Status:** ABSTAINED  
**GT Coverage:** 100% | **Top Score:** 0.0000 | **Gate:** `abstain_early`

**Expected answer:**
> The inventory_transaction table supports seven transaction types via CHECK constraint: RECEIPT (goods received from suppliers), ISSUE (materials consumed by production or shipped to customers), TRANSFER (movement between warehouses/bins), ADJUSTMENT (corrections to inventory counts), CYCLE_COUNT (pe…

**System answer:**
> I cannot find this information in the knowledge graph.

---

### ⛔ QA-037 — How does the BOM component type affect manufacturing?

**Status:** ABSTAINED  
**GT Coverage:** 100% | **Top Score:** 0.0000 | **Gate:** `abstain_early`

**Expected answer:**
> The bill_of_materials table classifies components into four types via CHECK: COMPONENT (standard parts consumed in production), PHANTOM (sub-assemblies that are not stocked — their components are consumed directly), BYPRODUCT (secondary outputs of the production process), and CO_PRODUCT (additional …

**System answer:**
> I cannot find this information in the knowledge graph.

---

### ⛔ QA-038 — How does the audit log track system events and changes?

**Status:** ABSTAINED  
**GT Coverage:** 100% | **Top Score:** 0.0000 | **Gate:** `abstain_early`

**Expected answer:**
> The audit_log table records every significant system event with event_type, user_id (FK to app_user), entity_type (which table was affected), entity_id (which record), and action (CREATE/READ/UPDATE/DELETE/LOGIN/LOGOUT/EXPORT via CHECK). For data changes, old_value and new_value are stored as JSON. …

**System answer:**
> I cannot find this information in the knowledge graph.

---

### ⛔ QA-039 — What are the different address types supported across the schema?

**Status:** ABSTAINED  
**GT Coverage:** 100% | **Top Score:** 0.0000 | **Gate:** `abstain_early`

**Expected answer:**
> Customer addresses support three types: BILLING, SHIPPING, and BOTH. Supplier addresses support four types: MAIN, BILLING, SHIPPING, and RETURN. Both customer_address and supplier_address have is_default/is_primary flags and cascade delete from their parent. The warehouse table stores location_addre…

**System answer:**
> I cannot find this information in the knowledge graph.

---

### ⛔ QA-040 — How would the schema support tracing a product from purchase receipt to customer shipment?

**Status:** ABSTAINED  
**GT Coverage:** 100% | **Top Score:** 0.0000 | **Gate:** `abstain_early`

**Expected answer:**
> The full traceability path is: purchase_receipt (inbound from supplier) → purchase_receipt_line (with lot_number) → inventory_on_hand (lot_number at warehouse/bin) → inventory_transaction (RECEIPT type logs the inbound). For production: work_order_material records material consumption → work_order t…

**System answer:**
> I cannot find this information in the knowledge graph.

---

### ⛔ QA-041 — How are supplier addresses and contacts structured compared to customer addresses?

**Status:** ABSTAINED  
**GT Coverage:** 100% | **Top Score:** 0.0000 | **Gate:** `abstain_early`

**Expected answer:**
> Both follow the same pattern: parent entity → address table + contact table, both with ON DELETE CASCADE. Supplier_address has address_type MAIN/BILLING/SHIPPING/RETURN (vs customer's BILLING/SHIPPING/BOTH) and uses is_primary flag (vs customer_address's is_default). Supplier_contact mirrors custome…

**System answer:**
> I cannot find this information in the knowledge graph.

---

### ⛔ QA-042 — Does the schema track employee compensation history?

**Status:** ABSTAINED  
**GT Coverage:** 100% | **Top Score:** 0.0000 | **Gate:** `abstain_early`

**Expected answer:**
> The employee table has current annual_salary and hourly_rate columns and the position table defines min_salary and max_salary ranges. However, there is no compensation history table in the schema — salary changes would overwrite the current values without preserving history. The only historical trac…

**System answer:**
> I cannot find this information in the knowledge graph.

---

### ⛔ QA-043 — How does the shipping route connect two warehouses through a carrier?

**Status:** ABSTAINED  
**GT Coverage:** 100% | **Top Score:** 0.0000 | **Gate:** `abstain_early`

**Expected answer:**
> The shipping_route table has origin_location_id and destination_location_id (both FK to warehouse), carrier_id (FK to carrier), plus route_code (UNIQUE), distance_km, estimated_hours, cost_per_km, and service_level. Shipments reference route_id FK to use a predefined route, plus independently refere…

**System answer:**
> I cannot find this information in the knowledge graph.

---

### ⛔ QA-044 — What is the production scheduling model and how does it relate to work orders?

**Status:** ABSTAINED  
**GT Coverage:** 100% | **Top Score:** 0.0000 | **Gate:** `abstain_early`

**Expected answer:**
> The production_schedule table links work_order_id (FK to work_order) to production_line_id (FK to production_line) with scheduled_start and scheduled_end timestamps, plus actual_start and actual_end for tracking real execution. Status progresses SCHEDULED → RUNNING → COMPLETED (or CANCELLED). Priori…

**System answer:**
> I cannot find this information in the knowledge graph.

---

### ⛔ QA-045 — How does the invoice line link back to both sales order lines and products?

**Status:** ABSTAINED  
**GT Coverage:** 100% | **Top Score:** 0.0000 | **Gate:** `abstain_early`

**Expected answer:**
> Invoice_line references invoice_id FK (parent invoice), product_id FK (what was invoiced), and optionally order_line_id FK (back-reference to the specific sales_order_line). This three-way linkage supports: invoice → sales_order (via invoice.order_id), invoice_line → product (direct), and invoice_li…

**System answer:**
> I cannot find this information in the knowledge graph.

---

### ⛔ QA-046 — Is there a returns or reverse logistics capability in the schema?

**Status:** ABSTAINED  
**GT Coverage:** 100% | **Top Score:** 0.0000 | **Gate:** `abstain_early`

**Expected answer:**
> Returns are partially supported: payment_type includes REFUND, invoice_type includes CREDIT_MEMO, shipment_type includes RETURN, and inventory_transaction has a RETURN transaction type. However, there is no dedicated returns management table (e.g., return_authorization or RMA). Returns would be trac…

**System answer:**
> I cannot find this information in the knowledge graph.

---

### ⛔ QA-047 — How many tables are in each business domain and what are they?

**Status:** ABSTAINED  
**GT Coverage:** 100% | **Top Score:** 0.0000 | **Gate:** `abstain_early`

**Expected answer:**
> The schema has 37 tables across 7+ domains: Sales & Customer (10: customer_type, customer, customer_address, customer_contact, product_category, product, price_list, product_price, sales_order, sales_order_line), Invoicing & Payment (4: invoice, invoice_line, payment, accounts_receivable), Procureme…

**System answer:**
> I cannot find this information in the knowledge graph.

---

### ⛔ QA-048 — How does the accounting period system work?

**Status:** ABSTAINED  
**GT Coverage:** 100% | **Top Score:** 0.0000 | **Gate:** `abstain_early`

**Expected answer:**
> The accounting_period table defines fiscal periods with period_code (UNIQUE), period_name, start_date, end_date, fiscal_year, and is_closed flag. A UNIQUE constraint on (fiscal_year, period_code) prevents duplicate periods within a year. Journal entries reference period_id FK to ensure postings land…

**System answer:**
> I cannot find this information in the knowledge graph.

---

### ⛔ QA-049 — How do work order materials track material consumption against BOM requirements?

**Status:** ABSTAINED  
**GT Coverage:** 100% | **Top Score:** 0.0000 | **Gate:** `abstain_early`

**Expected answer:**
> The work_order_material table links work_order_id FK to product_id FK (the material), with quantity_required (from BOM calculation) and quantity_issued (actually consumed). Status tracks progress: PENDING/ISSUED/PARTIAL/COMPLETE. Materials are sourced from specific bins via bin_id FK to bin_location…

**System answer:**
> I cannot find this information in the knowledge graph.

---

### ⛔ QA-050 — Does the schema support multi-currency transactions?

**Status:** ABSTAINED  
**GT Coverage:** 100% | **Top Score:** 0.0000 | **Gate:** `abstain_early`

**Expected answer:**
> Multiple tables have currency columns defaulting to USD: customer.currency, sales_order.currency, invoice.currency, payment.currency, purchase_order.currency, supplier.currency, supplier_contract.currency, general_ledger_account.currency, and price_list.currency. However, there is no currency exchan…

**System answer:**
> I cannot find this information in the knowledge graph.

---

### ⛔ QA-051 — How does the schema handle product storage requirements for hazardous or temperature-sensitive items?

**Status:** ABSTAINED  
**GT Coverage:** 100% | **Top Score:** 0.0000 | **Gate:** `abstain_early`

**Expected answer:**
> Products have three relevant fields: hazardous (BOOLEAN, default FALSE), storage_temperature_min (DECIMAL), and storage_temperature_max (DECIMAL). Warehouse zones have a temperature_controlled (BOOLEAN) flag. When a product requires temperature control, it should be stored in bins within temperature…

**System answer:**
> I cannot find this information in the knowledge graph.

---

### ⛔ QA-052 — What polymorphic reference patterns exist in the schema?

**Status:** ABSTAINED  
**GT Coverage:** 100% | **Top Score:** 0.0000 | **Gate:** `abstain_early`

**Expected answer:**
> The schema uses reference_type + reference_id polymorphic patterns in several tables: (1) quality_inspection — reference_type identifies the source (purchase_receipt, work_order) and reference_id stores the ID; (2) inventory_transaction — reference_type identifies the source document (sales_order, p…

**System answer:**
> I cannot find this information in the knowledge graph.

---

### ⛔ QA-053 — Is there a customer loyalty or rewards program in the schema?

**Status:** ABSTAINED  
**GT Coverage:** 100% | **Top Score:** 0.0000 | **Gate:** `abstain_early`

**Expected answer:**
> No, the schema does not contain any tables or columns for customer loyalty programs, reward points, or promotional campaigns. Customer classification is limited to customer_type_id (FK to customer_type), credit_score, and is_preferred-style fields do not exist. The customer table focuses on commerci…

**System answer:**
> I cannot find this information in the knowledge graph.

---

### ⛔ QA-054 — How does the schema support three-way matching in procurement?

**Status:** ABSTAINED  
**GT Coverage:** 100% | **Top Score:** 0.0000 | **Gate:** `abstain_early`

**Expected answer:**
> Three-way matching (PO → receipt → invoice) is supported through linked tables: purchase_order_line tracks quantity_ordered, quantity_received, and quantity_invoiced. Purchase_receipt_line links back to po_line_id FK. Invoice can be linked to purchase activities via invoice_type = 'PURCHASE' and acc…

**System answer:**
> I cannot find this information in the knowledge graph.

---

### ⛔ QA-055 — What indexes exist for performance optimization and which tables have the most?

**Status:** ABSTAINED  
**GT Coverage:** 100% | **Top Score:** 0.0000 | **Gate:** `abstain_early`

**Expected answer:**
> The schema defines explicit indexes beyond primary keys: customer has 3 indexes (on customer_type_id, status, customer_name), product has 4 (category, status, type, name), sales_order has 4 (customer, status, date, warehouse), purchase_order has 4 (supplier, status, date, warehouse), inventory has 5…

**System answer:**
> I cannot find this information in the knowledge graph.

---

## Anomalies & Observations

- **QA-030**: ABSTAINED early — retrieval quality gate rejected all chunks
- **QA-031**: ABSTAINED early — retrieval quality gate rejected all chunks
- **QA-032**: ABSTAINED early — retrieval quality gate rejected all chunks
- **QA-033**: ABSTAINED early — retrieval quality gate rejected all chunks
- **QA-034**: ABSTAINED early — retrieval quality gate rejected all chunks
- **QA-035**: ABSTAINED early — retrieval quality gate rejected all chunks
- **QA-036**: ABSTAINED early — retrieval quality gate rejected all chunks
- **QA-037**: ABSTAINED early — retrieval quality gate rejected all chunks
- **QA-038**: ABSTAINED early — retrieval quality gate rejected all chunks
- **QA-039**: ABSTAINED early — retrieval quality gate rejected all chunks
- **QA-040**: ABSTAINED early — retrieval quality gate rejected all chunks
- **QA-041**: ABSTAINED early — retrieval quality gate rejected all chunks
- **QA-042**: ABSTAINED early — retrieval quality gate rejected all chunks
- **QA-043**: ABSTAINED early — retrieval quality gate rejected all chunks
- **QA-044**: ABSTAINED early — retrieval quality gate rejected all chunks
- **QA-045**: ABSTAINED early — retrieval quality gate rejected all chunks
- **QA-046**: ABSTAINED early — retrieval quality gate rejected all chunks
- **QA-047**: ABSTAINED early — retrieval quality gate rejected all chunks
- **QA-048**: ABSTAINED early — retrieval quality gate rejected all chunks
- **QA-049**: ABSTAINED early — retrieval quality gate rejected all chunks
- **QA-050**: ABSTAINED early — retrieval quality gate rejected all chunks
- **QA-051**: ABSTAINED early — retrieval quality gate rejected all chunks
- **QA-052**: ABSTAINED early — retrieval quality gate rejected all chunks
- **QA-053**: ABSTAINED early — retrieval quality gate rejected all chunks
- **QA-054**: ABSTAINED early — retrieval quality gate rejected all chunks
- **QA-055**: ABSTAINED early — retrieval quality gate rejected all chunks
