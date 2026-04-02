# Complex Enterprise Scenarios for Stress Testing

This document describes complex business scenarios that require joining multiple tables across business units, testing entity resolution, and evaluating system performance under realistic enterprise conditions.

## Scenario 1: Order-to-Cash Cross-Business-Unit Analysis

**Business Question**: Analyze the complete order-to-cash cycle for high-value customers who purchase products from multiple categories, tracking from sales order through payment collection.

**Complexity Factors**:
- Joins 8 tables: Customer → Customer Type → Sales Order → Sales Order Line → Product → Product Category → Invoice → Payment
- Filters on customer credit score, order value, and product categories
- Aggregates payment collection metrics (days to pay, collection rate)
- Time-based analysis (orders in last 90 days)

**Expected Answer Format**:
```
Customer: Acme Corporation (Customer Type: Enterprise)
Credit Score: 85, Credit Limit: $1,000,000
Orders (Last 90 Days): 15 orders, Total Value: $1,250,000
Product Categories: Electronics (60%), Machinery (30%), Supplies (10%)

Order-to-Cash Metrics:
- Average Days to Pay: 35 days
- Payment Collection Rate: 93.3%
- Outstanding AR: $83,500
- Overdue Invoices: 2 invoices, $25,000

Top Purchased Products:
1. Industrial Control System - Category: Automation Electronics - 45 units, $450,000
2. Heavy Duty Motor Assembly - Category: Machinery Components - 20 units, $300,000
3. Precision Bearings Kit - Category: Industrial Supplies - 100 units, $75,000
```

**Key Relationships**:
- Customer.customer_type_id → Customer_Type
- Sales_Order.customer_id → Customer
- Sales_Order_Line.order_id → Sales_Order
- Sales_Order_Line.product_id → Product
- Product.category_id → Product_Category
- Invoice.order_id → Sales_Order
- Payment.invoice_id → Invoice

## Scenario 2: Procurement-to-Pay Performance Analysis

**Business Question**: Evaluate supplier performance across quality, delivery, and cost dimensions for critical raw materials sourced from multiple suppliers.

**Complexity Factors**:
- Joins 9 tables: Supplier → Supplier Contract → Purchase Order → Purchase Order Line → Product → Purchase Receipt → Purchase Receipt Line → Quality Inspection → Accounts Payable
- Filters on supplier rating, product types, and date ranges
- Aggregates on-time delivery rates, quality pass rates, and payment terms
- Compares actual vs. negotiated pricing from contracts

**Expected Answer Format**:
```
Supplier: Global Components Inc.
Supplier Type: Manufacturer
Credit Rating: A, Quality Rating: 4.8/5.0
Active Contracts: 3 contracts, Total Value: $5,000,000

Procurement Performance (Last 6 Months):
- Purchase Orders: 45 POs, Total Value: $2,100,000
- On-Time Delivery Rate: 91.1% (41 of 45 orders on time)
- Average Lead Time: 18 days (Contract: 15 days)
- Quality Pass Rate: 97.8% (44 of 45 inspections passed)

Top Purchased Products:
1. Steel Alloy Sheets - Product Type: Raw Material
   - Orders: 15, Quantity: 50,000 kg, Value: $750,000
   - Unit Price: $15.00/kg (Contract: $14.50/kg)
   - Quality Pass Rate: 100%, Lead Time: 16 days

2. Precision Machined Parts - Product Type: Component
   - Orders: 12, Quantity: 25,000 units, Value: $500,000
   - Unit Price: $20.00/unit (Contract: $19.50/unit)
   - Quality Pass Rate: 95.8%, Lead Time: 20 days

Payment Analysis:
- Total AP: $2,100,000
- Paid: $1,800,000 (85.7%)
- Outstanding: $300,000
- Average Payment Terms: Net 45 days
- Early Payment Discounts Captured: $18,000 (1.9% of paid amount)
```

**Key Relationships**:
- Supplier_Contract.supplier_id → Supplier
- Purchase_Order.supplier_id → Supplier
- Purchase_Order_Line.po_id → Purchase Order
- Purchase_Order_Line.product_id → Product
- Purchase_Receipt.po_id → Purchase Order
- Purchase_Receipt_Line.receipt_id → Purchase Receipt
- Quality_Inspection.reference_id → Purchase Receipt
- Accounts_Payable.supplier_id → Supplier

## Scenario 3: Multi-Warehouse Inventory Optimization

**Business Question**: Optimize inventory distribution across warehouses by analyzing product demand, stock levels, transfer patterns, and holding costs.

**Complexity Factors**:
- Joins 10 tables: Product → Product Category → Inventory On Hand → Warehouse → Warehouse Zone → Bin Location → Inventory Transaction → Stock Transfer → Sales Order Line → Shipment
- Filters on product category, warehouse type, and stock status
- Aggregates inventory turnover, fill rates, and transfer costs
- Identifies stock imbalances and excess inventory

**Expected Answer Format**:
```
Product: Industrial Hydraulic Pump
Category: Fluid Power Systems
Product Type: Finished Good
Cost: $450.00, Base Price: $850.00

Network Inventory Status:
- Total On-Hand: 3,500 units across 5 warehouses
- Total Allocated: 1,200 units
- Total Available: 2,300 units
- Inventory Value: $1,575,000

Warehouse Breakdown:

1. Chicago Distribution Center (Company-Owned)
   - On-Hand: 1,500 units (Allocated: 400, Available: 1,100)
   - Zones: Bulk Storage (Zone A) - 1,200 units, Pick Area (Zone B) - 300 units
   - Last 90 Days Sales: 850 units from this warehouse
   - Fill Rate: 96.5%, Stock-Outs: 3 events
   - Inventory Turnover: 4.2 turns/year

2. Dallas Regional Hub (Company-Owned)
   - On-Hand: 800 units (Allocated: 350, Available: 450)
   - Zones: Bulk Storage (Zone C) - 600 units, Pick Area (Zone D) - 200 units
   - Last 90 Days Sales: 420 units from this warehouse
   - Fill Rate: 98.1%, Stock-Outs: 1 event
   - Inventory Turnover: 3.8 turns/year

3. Los Angeles 3PL Facility (Third-Party)
   - On-Hand: 600 units (Allocated: 250, Available: 350)
   - Last 90 Days Sales: 310 units from this warehouse
   - Fill Rate: 94.2%, Stock-Outs: 5 events
   - Storage Cost: $12.50/unit/month

Transfer Activity (Last 90 Days):
- Chicago → Dallas: 200 units, Cost: $3,500
- Dallas → Los Angeles: 150 units, Cost: $2,800
- Chicago → Los Angeles: 100 units, Cost: $2,200

Recommendations:
- Transfer 200 units from Chicago to Los Angeles to prevent stock-outs
- Chicago has excess stock (600 units above 30-day average)
- Los Angeles needs replenishment (stock-outs increasing)
- Estimated transfer cost: $2,200, potential lost sales prevented: $42,500
```

**Key Relationships**:
- Product.category_id → Product Category
- Inventory_On_Hand.product_id → Product
- Inventory_On_Hand.warehouse_id → Warehouse
- Inventory_On_Hand.bin_id → Bin Location
- Bin_Location.zone_id → Warehouse Zone
- Warehouse_Zone.warehouse_id → Warehouse
- Inventory_Transaction.product_id → Product
- Inventory_Transaction.warehouse_id → Warehouse
- Stock_Transfer.from_warehouse_id → Warehouse
- Stock_Transfer.to_warehouse_id → Warehouse
- Sales_Order_Line.product_id → Product
- Sales_Order.warehouse_id → Warehouse
- Shipment.origin_location_id → Warehouse
- Shipment.destination_location_id → Warehouse

## Scenario 4: Production Cost & Efficiency Analysis

**Business Question**: Analyze production costs, scrap rates, and efficiency across production lines for complex manufactured products with multi-level bills of materials.

**Complexity Factors**:
- Joins 8 tables: Product → Bill of Materials (self-join for multi-level) → Work Order → Work Order Material → Production Schedule → Production Line → Quality Inspection → Inventory Transaction
- Recursive BOM traversal (finished good → sub-assemblies → raw materials)
- Aggregates material usage, scrap rates, and cycle times
- Compares planned vs. actual production metrics

**Expected Answer Format**:
```
Product: Industrial Assembly Robot ARM-500
Category: Automation Equipment
Product Type: Finished Good
Standard Cost: $12,500, Base Price: $25,000

Bill of Materials (Multi-Level):

Level 0: Industrial Assembly Robot ARM-500
├── Level 1: Robotic Arm Assembly (Sub-Assembly)
│   ├── Level 2: Servo Motor Controller Module (Raw Material) - 2 units @ $450 = $900
│   ├── Level 2: Precision Gearbox (Raw Material) - 1 unit @ $650 = $650
│   └── Level 2: Aluminum Arm Structure (Raw Material) - 1 unit @ $350 = $350
├── Level 1: Control System Unit (Sub-Assembly)
│   ├── Level 2: Industrial PLC Controller (Raw Material) - 1 unit @ $1,200 = $1,200
│   ├── Level 2: Sensor Array Kit (Raw Material) - 1 unit @ $800 = $800
│   └── Level 2: Power Supply Unit (Raw Material) - 1 unit @ $250 = $250
└── Level 1: Base Platform (Purchased Component)
    └── Level 2: Heavy Duty Base (Purchased) - 1 unit @ $1,500 = $1,500

Total Material Cost: $5,650
Estimated Labor & Overhead: $6,850
Total Standard Cost: $12,500

Production Performance (Last 6 Months):
- Work Orders: 25 orders, Total Quantity: 150 units
- Production Line: Line 1 (Assembly) - Capacity: 8 units/day
- Average Cycle Time: 4.2 hours (Standard: 4.0 hours)
- On-Time Delivery: 88% (22 of 25 orders on time)
- First Pass Quality Yield: 94.7%

Material Usage Analysis:
- Planned Material Cost: $847,500 (150 units × $5,650)
- Actual Material Cost: $892,500
- Material Variance: +$45,000 (+5.3%)
- Scrap Rate: 3.2% (normal: 2.0%)

Top Scrap Contributors:
1. Aluminum Arm Structure: 8% scrap (normal: 2%)
2. Precision Gearbox: 5% scrap (normal: 1%)
3. Servo Motor Controller: 4% scrap (normal: 2%)

Quality Inspection Results:
- Final Inspections: 150 units, 142 Passed, 8 Failed (5.3% failure rate)
- In-Process Inspections: 75 checks, 71 Passed, 4 Conditional Pass
- Common Defects: Dimensional tolerance (40%), Surface finish (30%), Assembly errors (30%)

Production Schedule Adherence:
- Scheduled Production Time: 600 hours (150 units × 4 hours)
- Actual Production Time: 630 hours
- Efficiency: 95.2%
- Downtime: 18 hours (3% of scheduled time)
  - Equipment Maintenance: 12 hours
  - Material Shortages: 4 hours
  - Other: 2 hours

Recommendations:
- Investigate aluminum arm structure machining process (8% scrap)
- Re-optimize work center scheduling to reduce downtime
- Negotiate volume pricing for servo motor controllers
```

**Key Relationships**:
- Product.product_id (parent) → Bill_of_Materials.parent_product_id
- Product.product_id (component) → Bill_of_Materials.component_product_id
- Bill_of_Materials (self-join for multi-level BOM)
- Work_Order.product_id → Product
- Work_Order.production_line_id → Production Line
- Work_Order.warehouse_id → Warehouse
- Work_Order_Material.work_order_id → Work Order
- Work_Order_Material.product_id → Product
- Work_Order_Material.bin_id → Bin Location
- Production_Schedule.work_order_id → Work Order
- Production_Schedule.production_line_id → Production Line
- Quality_Inspection.reference_id → Work Order
- Inventory_Transaction.reference_id → Work Order

## Scenario 5: Customer Entity Resolution & Deduplication

**Business Question**: Identify and merge duplicate customer records across the system, analyzing relationships with orders, invoices, and payments.

**Complexity Factors**:
- Tests entity resolution across Customer, Customer Address, Customer Contact
- Must detect duplicates based on name similarity, tax ID, address, phone, email
- Evaluates impact on related records (orders, invoices, payments, AR)
- Requires scoring confidence for merge decisions

**Expected Answer Format**:
```
Entity Resolution Analysis - Customer Duplicates

Detected Duplicate Group 1 (Confidence: 0.92):
- Record 1: Customer ID 1001
  Name: ACME Manufacturing Inc.
  Tax ID: 12-3456789
  Addresses:
    - 123 Industrial Blvd, Detroit, MI 48201 (Billing)
    - 123 Industrial Blvd, Detroit, MI 48201 (Shipping)
  Contacts: John Smith (Purchasing Manager), john.smith@acme-mfg.com
  Orders: 45 orders, Total Value: $2,350,000
  Invoices: 42 invoices, Balance Due: $125,000
  AR Records: 15 records, $280,000 outstanding

- Record 2: Customer ID 2847
  Name: ACME Manufacturing Company
  Tax ID: 12-3456789
  Addresses:
    - 123 Industrial Boulevard, Detroit, MI 48201 (Billing)
  Contacts: J. Smith (Purchasing), jsmith@acmemfg.com
  Orders: 12 orders, Total Value: $450,000
  Invoices: 11 invoices, Balance Due: $35,000
  AR Records: 5 records, $52,000 outstanding

Duplicate Detection Signals:
- Name Similarity: 0.87 (ACME Manufacturing Inc. vs ACME Manufacturing Company)
- Tax ID Match: EXACT (12-3456789)
- Address Match: 0.95 (123 Industrial Blvd vs 123 Industrial Boulevard)
- Phone Match: N/A (phone not provided in Record 2)
- Email Similarity: 0.72 (john.smith@acme-mfg.com vs jsmith@acmemfg.com)
- Combined Confidence Score: 0.92

Merge Recommendation: MERGE
Surviving Record: Customer ID 1001 (more complete data, more transaction history)

Impact Analysis:
- Total Orders After Merge: 57 orders ($2,800,000 total value)
- Total Invoices After Merge: 53 invoices ($160,000 balance due)
- Total AR Records After Merge: 20 records ($332,000 outstanding)
- No conflicts detected (no overlapping order numbers)
- Duplicate contact: "John Smith" and "J. Smith" - keep both as separate contacts

Related Records to Update:
- 57 Sales Orders (update customer_id from 2847 → 1001)
- 53 Invoices (update customer_id from 2847 → 1001)
- 20 Accounts Receivable records (update customer_id from 2847 → 1001)
- 12 Payments (update customer_id from 2847 → 1001)

Action Required:
- Review contact records for duplicate individuals
- Confirm merge with customer service team
- Update system master data
- Archive Record 2847 as merged into Record 1001
```

**Key Relationships**:
- Customer.customer_type_id → Customer_Type
- Customer_Address.customer_id → Customer
- Customer_Contact.customer_id → Customer
- Sales_Order.customer_id → Customer
- Invoice.customer_id → Customer
- Payment.customer_id → Customer
- Accounts_Receivable.customer_id → Customer
- Project.customer_id → Customer

## Scenario 6: Financial Statement Generation with Multi-Level Account Rollup

**Business Question**: Generate a trial balance and income statement for the accounting period, aggregating transactions across multiple account hierarchies and business units.

**Complexity Factors**:
- Joins 7 tables: Account Type → General Ledger Account (self-join for hierarchy) → Journal Entry → Journal Entry Line → Accounting Period → Budget → Department
- Recursive account hierarchy traversal (parent-child relationships)
- Aggregates debits and credits across multiple dimensions
- Compares actual vs. budget with variance analysis

**Expected Answer Format**:
```
Trial Balance - Period: 2024-Q1 (Jan 1 - Mar 31, 2024)

ASSETS (Debit Balance Accounts):
├── Current Assets
│   ├── 1000 - Cash and Cash Equivalents
│   │   ├── 1001 - Petty Cash: $5,000 (Debit)
│   │   └── 1002 - Bank Accounts: $1,250,000 (Debit)
│   ├── 1100 - Accounts Receivable: $2,450,000 (Debit)
│   ├── 1200 - Inventory: $3,800,000 (Debit)
│   │   ├── 1210 - Raw Materials: $1,200,000
│   │   ├── 1220 - Work in Progress: $800,000
│   │   └── 1230 - Finished Goods: $1,800,000
│   └── 1300 - Prepaid Expenses: $150,000 (Debit)
└── Total Current Assets: $7,655,000

LIABILITIES (Credit Balance Accounts):
├── Current Liabilities
│   ├── 2000 - Accounts Payable: $1,850,000 (Credit)
│   ├── 2100 - Accrued Expenses: $320,000 (Credit)
│   └── 2200 - Short-Term Debt: $500,000 (Credit)
└── Total Current Liabilities: $2,670,000

EQUITY (Credit Balance Accounts):
├── 3000 - Common Stock: $2,000,000 (Credit)
├── 3100 - Retained Earnings: $2,850,000 (Credit)
└── Total Equity: $4,850,000

REVENUES (Credit Balance Accounts):
├── 4000 - Sales Revenue: $8,500,000 (Credit)
│   ├── Electronics Division: $5,100,000
│   ├── Machinery Division: $2,550,000
│   └── Supplies Division: $850,000
├── 4100 - Service Revenue: $450,000 (Credit)
└── Total Revenue: $8,950,000

EXPENSES (Debit Balance Accounts):
├── 5000 - Cost of Goods Sold: $5,100,000 (Debit)
├── 6000 - Operating Expenses: $2,200,000 (Debit)
│   ├── 6100 - Salaries and Wages: $1,200,000
│   │   ├── Sales Department: $350,000
│   │   ├── Operations Department: $600,000
│   │   └── Administrative Department: $250,000
│   ├── 6200 - Rent and Facilities: $450,000
│   ├── 6300 - Utilities: $180,000
│   └── 6400 - Other Expenses: $370,000
└── Total Expenses: $7,300,000

Net Income: $1,650,000 (Revenue $8,950,000 - Expenses $7,300,000)

Validation:
- Total Debits: $20,055,000
- Total Credits: $20,055,000
- Trial Balance: IN BALANCE ✓

Budget Variance Analysis - Q1 2024:

Revenue:
- Budgeted Revenue: $9,000,000
- Actual Revenue: $8,950,000
- Variance: -$50,000 (-0.6%) - Favorable variance is small

Expenses:
- Budgeted Expenses: $7,200,000
- Actual Expenses: $7,300,000
- Variance: +$100,000 (+1.4%) - Unfavorable, investigate
  - Salaries: +$50,000 (overtime and temporary labor)
  - Utilities: +$30,000 (higher energy costs)
  - Rent: -$10,000 (lease renegotiation savings)

Department Performance:
1. Electronics Division
   - Budget: $5,200,000, Actual: $5,100,000
   - Variance: -$100,000 (-1.9%) - Slightly below budget

2. Machinery Division
   - Budget: $2,500,000, Actual: $2,550,000
   - Variance: +$50,000 (+2.0%) - Above budget, good performance

3. Supplies Division
   - Budget: $900,000, Actual: $850,000
   - Variance: -$50,000 (-5.6%) - Below budget, needs attention
```

**Key Relationships**:
- General_Ledger_Account.account_type_id → Account_Type
- General_Ledger_Account.parent_account_id → General_Ledger_Account (self-join for hierarchy)
- Journal_Entry_Line.account_id → General_Ledger_Account
- Journal_Entry_Line.entry_id → Journal_Entry
- Journal_Entry.period_id → Accounting_Period
- Budget.account_id → General_Ledger_Account
- Budget.department_id → Department

## Scenario 7: Supply Chain Risk Assessment

**Business Question**: Assess supply chain risk by analyzing supplier dependency, quality issues, lead time variability, and financial health across the procurement network.

**Complexity Factors**:
- Joins 8 tables: Supplier → Supplier Contract → Purchase Order → Purchase Order Line → Product → Purchase Receipt → Quality Inspection → Non-Conformance Report
- Network analysis of supplier-product relationships
- Aggregates risk indicators across multiple dimensions
- Identifies single points of failure and concentration risk

**Expected Answer Format**:
```
Supply Chain Risk Assessment - Product Category: Critical Components

Category Overview:
- Total Products in Category: 85 products
- Total Suppliers: 12 suppliers
- Annual Spend: $15,800,000
- Strategic Importance: HIGH (used in 70% of finished goods)

Supplier Dependency Analysis:

HIGH RISK - Single Source Suppliers:

1. Supplier: PrecisionTech Components
   - Products Supplied: 8 critical components
   - Annual Spend: $3,200,000 (20.3% of category spend)
   - Risk Score: 9.2/10 (CRITICAL)
   - Dependency: 6 products are single-source (no alternative suppliers)
   - Contract Status: Expires in 3 months, not renewed
   - Financial Health: Credit Rating B (declining from A last year)
   - Quality Performance: 94.5% pass rate (below 98% threshold)
   - On-Time Delivery: 87% (below 95% threshold)
   - Lead Time: 28 days average (high variability: ±10 days)
   - Recent NCRs: 3 non-conformance reports in last 6 months
     - NCR-001: Dimensional defects on precision gears (Major)
     - NCR-002: Material certification missing (Major)
     - NCR-003: Packaging damage causing 15% scrap (Minor)

   Risk Factors:
   - Single source dependency on 6 critical products
   - Contract expiring, renewal uncertain
   - Declining financial health (credit rating downgrade)
   - Quality and delivery below acceptable thresholds
   - Lead time variability impacting production schedules

   Recommendations:
   - IMMEDIATE: Qualify alternate suppliers for 6 single-source products
   - HIGH: Increase safety stock for critical items (4 weeks → 8 weeks)
   - MEDIUM: Engage supplier on quality improvement plan
   - MEDIUM: Monitor financial health monthly

2. Supplier: Global Motors Ltd.
   - Products Supplied: 5 motor assemblies
   - Annual Spend: $2,800,000 (17.7% of category spend)
   - Risk Score: 7.8/10 (HIGH)
   - Dependency: 3 products are single-source
   - Contract Status: Active, expires in 18 months
   - Financial Health: Credit Rating A (stable)
   - Quality Performance: 98.2% pass rate (meets threshold)
   - On-Time Delivery: 92% (below 95% threshold)
   - Lead Time: 35 days average (consistent, ±3 days)

Product-Level Risk Analysis:

CRITICAL RISK PRODUCTS:

1. Product: Servo Motor Assembly SMA-2500
   - Category: Automation Components
   - Used In: 12 finished goods (40% of production volume)
   - Annual Usage: 5,000 units
   - Unit Cost: $450, Annual Spend: $2,250,000
   - Suppliers: 1 supplier (PrecisionTech Components)
   - Lead Time: 28 days
   - Quality Pass Rate: 94.5%
   - Current Stock: 450 units (9 days of inventory)
   - Risk Score: 9.5/10 (CRITICAL)

   Impact if Supply Disrupted:
   - Production halt on 12 finished goods
   - Potential revenue loss: $850,000 per week
   - Customer backlog: 45 orders affected

2. Product: Precision Gearbox PGB-800
   - Category: Power Transmission
   - Used In: 8 finished goods (25% of production volume)
   - Annual Usage: 3,000 units
   - Unit Cost: $650, Annual Spend: $1,950,000
   - Suppliers: 1 supplier (PrecisionTech Components)
   - Lead Time: 35 days
   - Quality Pass Rate: 92.0% (below threshold)
   - Current Stock: 180 units (18 days of inventory)
   - Risk Score: 8.8/10 (HIGH)

   Recent Quality Issues:
   - NCR-001: 15% scrap rate due to dimensional defects
   - 100% inspection implemented, increasing receiving time
   - Supplier corrective action pending

Network Visualization:
```
PrecisionTech (High Risk)
├── Servo Motor Assembly (Single Source) ─→ 12 FG products
├── Precision Gearbox (Single Source) ─→ 8 FG products
├── Linear Actuator (Single Source) ─→ 5 FG products
├── Ball Screw Assembly (Single Source) ─→ 4 FG products
├── Coupling Kit (Single Source) ─→ 3 FG products
└── Bearing Assembly (Alternative Available) ─→ 6 FG products

Global Motors (Medium Risk)
├── DC Motor M1 (Single Source) ─→ 6 FG products
├── DC Motor M2 (Single Source) ─→ 4 FG products
├── AC Motor A1 (Alternative Available) ─→ 5 FG products
└── Gear Motor GM1 (Alternative Available) ─→ 3 FG products
```

Overall Risk Assessment:
- Critical Risk Products: 8 products (9.4% of category)
- High Risk Products: 15 products (17.6% of category)
- Medium Risk Products: 25 products (29.4% of category)
- Low Risk Products: 37 products (43.5% of category)

Recommended Actions:
1. IMMEDIATE (This Week):
   - Approve emergency budget for alternate supplier qualification
   - Order 8-week safety stock for critical single-source items
   - Schedule executive review with PrecisionTech management

2. SHORT-TERM (Next 30 Days):
   - Launch RFQ for 6 single-source products from PrecisionTech
   - Implement 100% incoming inspection for PrecisionTech shipments
   - Update production schedules to account for longer lead times

3. MEDIUM-TERM (Next 90 Days):
   - Qualify 2 alternative suppliers for critical components
   - Negotiate improved quality and delivery terms with PrecisionTech
   - Implement supplier scorecard with monthly performance reviews
```

**Key Relationships**:
- Supplier_Contract.supplier_id → Supplier
- Purchase_Order.supplier_id → Supplier
- Purchase_Order_Line.po_id → Purchase Order
- Purchase_Order_Line.product_id → Product
- Purchase_Receipt.po_id → Purchase Order
- Quality_Inspection.reference_id → Purchase Receipt
- Non_Conformance_Report.product_id → Product

## Scenario 8: Project Profitability & Resource Utilization

**Business Question**: Analyze project profitability, resource utilization, and time tracking across customer projects with cross-departmental teams.

**Complexity Factors**:
- Joins 7 tables: Project → Customer → Employee → Department → Project Task → Time Entry → Invoice
- Hierarchical project structure (parent-child tasks)
- Aggregates time, costs, and revenue across multiple dimensions
- Compares budgeted vs. actual costs and revenue

**Expected Answer Format**:
```
Project Profitability Analysis

Project: Enterprise Automation System Implementation
Project ID: PRJ-2024-015
Customer: Global Manufacturing Corp. (Customer Type: Enterprise)
Project Type: Customer Project
Project Manager: Sarah Chen (Employee ID: E1023)
Status: IN PROGRESS
Duration: Jan 15, 2024 - Jun 30, 2024 (current: Mar 23, 2024)

Financial Summary:
- Budgeted Revenue: $850,000
- Actual Revenue to Date: $425,000 (50% of budget)
- Budgeted Cost: $550,000
- Actual Cost to Date: $287,500 (52.3% of budget)
- Projected Profit: $300,000 (35.3% margin)
- Current Profit: $137,500 (32.4% margin to date)
- Status: ON TRACK (margin within ±5% of target)

Cost Breakdown by Department:

1. Engineering Department
   - Budget: $350,000 (63.6% of total budget)
   - Actual: $185,000 (52.9% of budget, 52.9% consumed)
   - Variance: -$165,000 remaining
   - Employees: 8 engineers assigned
   - Hours Logged: 2,450 hours @ average $75.50/hour
   - Top Resource: David Kim (Senior Engineer) - 320 hours, $26,400

2. Software Development Department
   - Budget: $120,000 (21.8% of total budget)
   - Actual: $68,500 (57.1% of budget, 57.1% consumed)
   - Variance: -$51,500 remaining
   - Employees: 5 developers assigned
   - Hours Logged: 1,150 hours @ average $59.60/hour
   - Top Resource: Maria Rodriguez (Lead Developer) - 280 hours, $18,200

3. Project Management Department
   - Budget: $50,000 (9.1% of total budget)
   - Actual: $22,000 (44.0% of budget, 44.0% consumed)
   - Variance: -$28,000 remaining
   - Employees: 2 project managers assigned
   - Hours Logged: 285 hours @ average $77.20/hour
   - Top Resource: Sarah Chen (Project Manager) - 180 hours, $14,400

4. Quality Assurance Department
   - Budget: $30,000 (5.5% of total budget)
   - Actual: $12,000 (40.0% of budget, 40.0% consumed)
   - Variance: -$18,000 remaining
   - Employees: 2 QA engineers assigned
   - Hours Logged: 150 hours @ average $80.00/hour

Task Progress & Budget Consumption:

Task Hierarchy:
PRJ-2024-015: Enterprise Automation System Implementation
├── Task 1: Requirements Analysis (COMPLETED)
│   ├── Budget: $30,000, Actual: $28,500 (95% consumed)
│   ├── Planned: 80 hours, Actual: 92 hours (+15% over)
│   ├── Assigned To: Sarah Chen (PM)
│   └── Status: COMPLETED (0.5 weeks late)
├── Task 2: System Design (COMPLETED)
│   ├── Budget: $75,000, Actual: $82,000 (109% consumed - over budget!)
│   ├── Planned: 250 hours, Actual: 295 hours (+18% over)
│   ├── Assigned To: Engineering (5 engineers)
│   └── Status: COMPLETED (1 week late)
├── Task 3: Software Development (IN PROGRESS - 60% complete)
│   ├── Budget: $250,000, Actual: $145,000 (58% consumed)
│   ├── Planned: 1,200 hours, Actual: 780 hours (65% consumed)
│   ├── Assigned To: Software Development (5 developers)
│   ├── Status: IN PROGRESS (on schedule)
│   └── Subtasks:
│       ├── Task 3.1: Backend API (COMPLETED) - $45,000 / $42,000
│       ├── Task 3.2: Frontend UI (IN PROGRESS - 70%) - $80,000 / $52,000
│       └── Task 3.3: Database Integration (NOT STARTED) - $60,000 / $0
├── Task 4: Hardware Integration (IN PROGRESS - 40% complete)
│   ├── Budget: $120,000, Actual: $42,000 (35% consumed)
│   ├── Planned: 500 hours, Actual: 195 hours (39% consumed)
│   ├── Assigned To: Engineering (4 engineers)
│   └── Status: SLIGHTLY BEHIND (blocked by hardware delivery)
└── Task 5: Testing & QA (NOT STARTED)
    ├── Budget: $75,000, Actual: $0 (0% consumed)
    ├── Planned: 400 hours, Actual: 0 hours
    ├── Assigned To: QA (2 engineers)
    └── Status: NOT STARTED (starts after Task 3 & 4 complete)

Resource Utilization Analysis:

Top 5 Resources by Hours Logged:
1. David Kim (Senior Engineer, Engineering)
   - Hours: 320 (39% of total engineering hours)
   - Cost: $26,400
   - Tasks: System Design (200h), Hardware Integration (120h)
   - Utilization: 85% (high utilization, risk of burnout)

2. Maria Rodriguez (Lead Developer, Software Development)
   - Hours: 280 (32% of total development hours)
   - Cost: $18,200
   - Tasks: Backend API (180h), Frontend UI (100h)
   - Utilization: 92% (very high, consider resource augmentation)

3. Sarah Chen (Project Manager, PM)
   - Hours: 180 (63% of total PM hours)
   - Cost: $14,400
   - Tasks: Requirements Analysis (80h), Overall Coordination (100h)
   - Utilization: 70% (appropriate for PM role)

4. James Wilson (Systems Engineer, Engineering)
   - Hours: 260 (32% of total engineering hours)
   - Cost: $19,500
   - Tasks: System Design (150h), Hardware Integration (110h)
   - Utilization: 78%

5. Lisa Park (Developer, Software Development)
   - Hours: 240 (28% of total development hours)
   - Cost: $14,160
   - Tasks: Frontend UI (240h)
   - Utilization: 82%

Billing & Revenue Recognition:
- Billing Type: Milestone-based (5 milestones)
- Milestones Completed: 2 of 5
- Revenue Recognized: $425,000 (50% of contract value)
- Invoices Issued: 2 invoices, $425,000 total
- Invoices Paid: 1 invoice, $200,000 paid
- Outstanding AR: $225,000 (within payment terms)

Risks & Issues:
1. CRITICAL: System Design task exceeded budget by $7,000 (+9%)
   - Impact: Reduces contingency budget for testing phase
   - Mitigation: Compressed schedule for Software Development to recover time

2. HIGH: Hardware Integration task is behind schedule
   - Cause: Hardware delivery delayed by supplier
   - Impact: May delay Testing & QA start by 1 week
   - Mitigation: Expedited hardware shipping ordered

3. MEDIUM: Two resources (Kim, Rodriguez) at >90% utilization
   - Risk: Burnout and quality issues
   - Mitigation: Consider adding backup resources for routine tasks

4. LOW: Customer approval pending on design specifications
   - Impact: Potential rework if changes requested
   - Mitigation: Regular check-ins with customer stakeholders

Recommendations:
1. Rebaseline project budget to account for System Design overage
2. Add contingency buffer for Hardware Integration delays
3. Monitor resource utilization weekly for top 3 resources
4. Schedule customer design review meeting to lock in requirements
5. Prepare project status report for customer steering committee
```

**Key Relationships**:
- Project.customer_id → Customer
- Project.project_manager_id → Employee
- Employee.department_id → Department
- Project_Task.project_id → Project
- Project_Task.assigned_to → Employee
- Project_Task.parent_task_id → Project_Task (self-join for hierarchy)
- Time_Entry.employee_id → Employee
- Time_Entry.project_id → Project
- Invoice.customer_id → Customer
- Department.manager_id → Employee

## Performance Testing Considerations

These scenarios are designed to test the following aspects of a GraphRAG system:

1. **Multi-Hop Query Performance**: Each scenario requires 6-10 table joins
2. **Relationship Traversal**: Complex foreign key networks with many-to-many relationships
3. **Hierarchical Data**: BOMs, account hierarchies, project task hierarchies
4. **Aggregation Complexity**: Grouping and aggregating across multiple dimensions
5. **Entity Resolution**: Duplicate detection and merge recommendations
6. **Temporal Analysis**: Date range filtering and time-based aggregations
7. **Network Analysis**: Supplier dependency, supply chain risk visualization
8. **Variance Analysis**: Comparing planned vs. actual, budget vs. forecast

Expected query execution times for reference:
- Simple retrieval (2-3 tables): < 1 second
- Medium complexity (4-5 tables): 1-3 seconds
- High complexity (6-8 tables): 3-8 seconds
- Very high complexity (9+ tables, aggregations): 8-15 seconds
- Entity resolution batch (100 records): 10-30 seconds
