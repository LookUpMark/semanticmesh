# Enterprise ERP Business Glossary

## Sales & Customer Management

### Customer
**Definition**: An individual or organization that purchases goods or services from the company. Customers can be classified as retail (B2C) or business (B2B) with different credit terms and pricing structures.

**Attributes**: customer_id, customer_name, customer_type, credit_limit, payment_terms, tax_id, registration_date, status

**Related Concepts**: Sales Order, Invoice, Payment, Customer Address, Credit Score

### Sales Order
**Definition**: A commercial document issued by a seller to a buyer indicating types, quantities, and agreed prices for products or services. Sales orders can be in draft, confirmed, shipped, or cancelled status.

**Attributes**: order_id, customer_id, order_date, delivery_date, total_amount, status, sales_rep_id, warehouse_id

**Related Concepts**: Customer, Order Line, Invoice, Shipment, Sales Representative

### Product
**Definition**: A tangible item or service that the company sells to customers. Products can be finished goods, raw materials, or services with different pricing and inventory tracking requirements.

**Attributes**: product_id, product_name, product_type, base_price, cost, weight, unit_of_measure, status, category_id

**Related Concepts**: Product Category, Bill of Materials, Inventory, Price List, Order Line

## Procurement & Supplier Management

### Supplier
**Definition**: An external entity that provides goods or services to the company. Suppliers are evaluated on quality, delivery performance, and cost. Each supplier has a credit rating and payment terms.

**Attributes**: supplier_id, supplier_name, supplier_type, payment_terms, credit_rating, currency, lead_time_days, status

**Related Concepts**: Purchase Order, Supplier Contract, Purchase Receipt, Quality Inspection

### Purchase Order
**Definition**: A commercial document issued by a buyer to a seller indicating types, quantities, and agreed prices for products or services. Purchase orders go through approval workflows before being sent to suppliers.

**Attributes**: po_id, supplier_id, order_date, required_date, total_amount, status, approved_by, approval_date, warehouse_id

**Related Concepts**: Supplier, Purchase Order Line, Purchase Receipt, Supplier Invoice, Approval Workflow

### Supplier Contract
**Definition**: A formal agreement between the company and a supplier defining terms, conditions, pricing, and service level agreements (SLAs). Contracts can be fixed-price, cost-plus, or rate-based.

**Attributes**: contract_id, supplier_id, contract_type, start_date, end_date, payment_terms, status, renewal_terms

**Related Concepts**: Supplier, Purchase Order, Contract Amendment, Performance Review

## Inventory & Warehousing

### Warehouse
**Definition**: A physical location where inventory is stored. Warehouses can be company-owned, third-party logistics (3PL) facilities, or virtual locations for transit inventory.

**Attributes**: warehouse_id, warehouse_name, warehouse_type, location_address, capacity_cubic_meters, manager_id, status

**Related Concepts**: Inventory Transaction, Bin Location, Warehouse Zone, Stock Transfer

### Inventory Transaction
**Definition**: A record of any movement or change in inventory quantity. Transactions include receipts, issues, transfers, adjustments, and cycle counts.

**Attributes**: transaction_id, product_id, warehouse_id, transaction_type, quantity, transaction_date, reference_type, reference_id, unit_cost

**Related Concepts**: Product, Warehouse, Bin Location, Purchase Receipt, Sales Shipment

### Bin Location
**Definition**: A specific storage location within a warehouse. Bin locations are organized into zones, aisles, shelves, and positions for efficient picking and put-away.

**Attributes**: bin_id, warehouse_id, zone_id, aisle, shelf, position, capacity_quantity, current_quantity, product_id

**Related Concepts**: Warehouse, Warehouse Zone, Product, Inventory Transaction

### Stock Transfer
**Definition**: The movement of inventory between warehouses or locations. Stock transfers can be planned (inter-warehouse transfers) or ad-hoc (emergency replenishment).

**Attributes**: transfer_id, from_warehouse_id, to_warehouse_id, transfer_date, status, shipment_method, tracking_number

**Related Concepts**: Warehouse, Product, Inventory Transaction, Shipment

## Finance & Accounting

### General Ledger Account
**Definition**: A chronological record of all financial transactions for a specific account type. Accounts are organized into a chart of accounts with hierarchies for balance sheet and income statement.

**Attributes**: account_id, account_number, account_name, account_type, parent_account_id, currency, balance_type, status

**Related Concepts**: Journal Entry, Account Hierarchy, Financial Statement, Budget

### Journal Entry
**Definition**: A recording of a financial transaction in double-entry bookkeeping. Each journal entry must balance with equal debits and credits.

**Attributes**: entry_id, entry_date, period_id, source_document_type, source_document_id, created_by, approved_by, status, total_debit, total_credit

**Related Concepts**: Journal Entry Line, General Ledger Account, Accounting Period, User

### Accounts Receivable
**Definition**: Money owed to the company by customers for goods or services delivered on credit. AR aging tracks overdue payments and supports collections workflows.

**Attributes**: ar_id, customer_id, invoice_id, amount_due, due_date, days_overdue, status, collection_status, last_contact_date

**Related Concepts**: Customer, Invoice, Payment, Collections Note, Credit Memo

### Accounts Payable
**Definition**: Money owed by the company to suppliers for goods or services received on credit. AP aging tracks payment due dates and supports payment approval workflows.

**Attributes**: ap_id, supplier_id, invoice_id, amount_due, due_date, discount_available, discount_until, status, payment_priority

**Related Concepts**: Supplier, Supplier Invoice, Payment, Payment Term

### Budget
**Definition**: A financial plan that allocates resources to departments, projects, or accounts for a specific period. Budgets are compared to actual results for variance analysis.

**Attributes**: budget_id, budget_type, period_id, department_id, account_id, budgeted_amount, actual_amount, variance, status

**Related Concepts**: Department, Account, Accounting Period, Budget Version

## Human Resources

### Employee
**Definition**: An individual who works for the company under an employment contract. Employees can be full-time, part-time, contract, or temporary with different compensation and benefit structures.

**Attributes**: employee_id, first_name, last_name, employee_type, department_id, position_id, hire_date, status, salary, manager_id

**Related Concepts**: Department, Position, Employee Compensation, Time Entry, Performance Review

### Department
**Definition**: An organizational unit within the company responsible for specific business functions. Departments have budgets, managers, and reporting hierarchies.

**Attributes**: department_id, department_name, parent_department_id, manager_id, budget_code, location, status

**Related Concepts**: Employee, Position, Budget, Cost Center

### Position
**Definition**: A specific role within the organizational structure with defined responsibilities, qualifications, and compensation ranges. Positions belong to job families with career paths.

**Attributes**: position_id, position_title, job_family, grade_level, min_salary, max_salary, department_id, status, required_qualifications

**Related Concepts**: Employee, Department, Job Family, Employee Compensation

### Time Entry
**Definition**: A record of hours worked by an employee, used for payroll processing and project costing. Time entries can be billable or non-billable to projects.

**Attributes**: time_entry_id, employee_id, project_id, work_date, hours_worked, work_type, description, approval_status, submitted_date

**Related Concepts**: Employee, Project, Payroll Period, Invoice

## Production & Manufacturing

### Bill of Materials
**Definition**: A hierarchical list of raw materials, sub-assemblies, and quantities required to manufacture a finished product. BOMs can be single-level or multi-level with phantom items.

**Attributes**: bom_id, product_id, component_id, quantity, unit_of_measure, scrap_percentage, effective_start_date, effective_end_date

**Related Concepts**: Product, Work Order, Production Schedule, Material Requirement

### Work Order
**Definition**: A document authorizing the production of a specified quantity of product. Work orders track labor, materials, and overhead costs for job costing.

**Attributes**: work_order_id, product_id, quantity_ordered, quantity_completed, start_date, required_date, status, production_line_id, priority

**Related Concepts**: Product, Bill of Materials, Work Order Operation, Material Requirement, Production Schedule

### Production Schedule
**Definition**: A plan that allocates production resources (lines, machines, labor) to work orders over time. Schedules consider capacity constraints, material availability, and demand priorities.

**Attributes**: schedule_id, work_order_id, production_line_id, scheduled_start, scheduled_end, actual_start, actual_end, status, priority

**Related Concepts**: Work Order, Production Line, Product, Capacity Planning

### Production Line
**Definition**: A manufacturing resource consisting of equipment and personnel configured to produce products. Lines have capacity rates, changeover times, and maintenance schedules.

**Attributes**: line_id, line_name, line_type, capacity_per_hour, location_id, status, maintenance_schedule_id

**Related Concepts**: Production Schedule, Work Order, Location, Maintenance Schedule

## Quality & Compliance

### Quality Inspection
**Definition**: A systematic examination of materials or products to verify conformance to specifications. Inspections can be incoming (from suppliers), in-process (during production), or final (before shipping).

**Attributes**: inspection_id, inspection_type, reference_type, reference_id, product_id, inspection_date, inspector_id, result, defects_found, status

**Related Concepts**: Product, Supplier, Purchase Receipt, Work Order, Quality Standard

### Quality Standard
**Definition**: A documented specification defining acceptance criteria for products or processes. Standards can be internal (company-specific) or external (ISO, ASTM, FDA).

**Attributes**: standard_id, standard_code, standard_name, standard_type, version, issue_date, status

**Related Concepts**: Quality Inspection, Test Procedure, Product Specification

### Non-Conformance Report
**Definition**: A document describing a quality deviation or defect that does not meet specifications. NCRs trigger root cause analysis and corrective/preventive actions (CAPA).

**Attributes**: ncr_id, ncr_type, reference_type, reference_id, product_id, issue_date, reported_by, severity, root_cause, status, resolution_date

**Related Concepts**: Quality Inspection, Product, Corrective Action, Supplier

## Logistics & Shipping

### Shipment
**Definition**: The physical transportation of goods from one location to another. Shipments can be outbound (to customers), inbound (from suppliers), or inter-warehouse transfers.

**Attributes**: shipment_id, shipment_type, origin_location_id, destination_location_id, ship_date, estimated_arrival, carrier_id, tracking_number, status

**Related Concepts**: Carrier, Shipment Line, Sales Order, Purchase Receipt, Stock Transfer

### Carrier
**Definition**: A company that provides transportation services for shipping goods. Carriers are rated on cost, transit time, and delivery performance.

**Attributes**: carrier_id, carrier_name, carrier_type, service_level, contact_phone, email, rating, status

**Related Concepts**: Shipment, Shipping Rate, Carrier Contract

### Shipping Route
**Definition**: A predefined path for moving goods between locations with specific transit times, costs, and handling requirements. Routes can include multiple stops and transshipments.

**Attributes**: route_id, route_name, origin_id, destination_id, distance_km, estimated_hours, carrier_id, service_level, status

**Related Concepts**: Shipment, Carrier, Location, Shipping Rate

## Project Management

### Project
**Definition**: A temporary endeavor with defined objectives, deliverables, timelines, and resources. Projects can be customer-facing (consulting, construction) or internal (R&D, process improvement).

**Attributes**: project_id, project_name, project_type, customer_id, project_manager_id, start_date, end_date, budget_amount, status, priority

**Related Concepts**: Customer, Employee, Project Task, Time Entry, Invoice

### Project Task
**Definition**: A specific work item within a project that must be completed. Tasks have dependencies, assignments, and progress tracking.

**Attributes**: task_id, project_id, task_name, parent_task_id, assigned_to, start_date, due_date, estimated_hours, actual_hours, status, completion_percentage

**Related Concepts**: Project, Employee, Time Entry, Task Dependency

## Reporting & Analytics

### Key Performance Indicator (KPI)
**Definition**: A quantifiable metric used to evaluate performance against strategic objectives. KPIs can be financial, operational, customer-facing, or employee-related.

**Common KPIs**: Order fulfillment rate, Inventory turnover, Supplier on-time delivery, Customer satisfaction, Employee productivity, Production yield

### Financial Statement
**Definition**: Formal reports summarizing financial performance and position. Primary statements include Balance Sheet, Income Statement, and Cash Flow Statement.

**Types**: Balance Sheet (assets, liabilities, equity), Income Statement (revenue, expenses, profit), Cash Flow Statement (operating, investing, financing activities)

## System Concepts

### User
**Definition**: A person who interacts with the ERP system with specific permissions and roles. Users can be employees, customers, suppliers, or system administrators.

**Attributes**: user_id, username, email, user_type, status, last_login_date, failed_login_attempts

**Related Concepts**: Employee, Role, Permission, Audit Log

### Role
**Definition**: A collection of permissions that grants access to specific system functions. Users can have multiple roles for different contexts (e.g., Buyer and Approver).

**Attributes**: role_id, role_name, role_type, description, status

**Related Concepts**: User, Permission, Role Hierarchy

### Audit Log
**Definition**: A chronological record of system events including logins, data changes, approvals, and errors. Audit logs support security monitoring and compliance requirements.

**Attributes**: log_id, event_type, user_id, entity_type, entity_id, timestamp, ip_address, action, old_value, new_value

**Related Concepts**: User, Entity, Security Incident

## Data Quality Concepts

### Master Data
**Definition**: Core business entities that are shared across multiple business processes. Examples include Customer, Product, Supplier, and Employee records.

**Challenge**: Maintaining consistency and accuracy across duplicate records, system integrations, and organizational changes.

### Reference Data
**Definition**: Standardized codes and classifications used across the system. Examples include currency codes, country codes, unit measures, and tax categories.

**Challenge**: Managing updates from external authorities (ISO, UN) while maintaining historical compatibility.

### Transactional Data
**Definition**: High-volume records generated by business operations such as orders, invoices, payments, and inventory movements.

**Challenge**: Query performance at scale while maintaining data integrity and auditability.
