-- Enterprise ERP Schema - Large Scale Stress Test
-- 37 tables, 150+ relationships, complex enterprise scenarios

-- ============================================
-- SALES & CUSTOMER MANAGEMENT
-- ============================================

CREATE TABLE customer_type (
    customer_type_id VARCHAR(20) PRIMARY KEY,
    type_name VARCHAR(100) NOT NULL,
    description VARCHAR(500),
    credit_check_required BOOLEAN DEFAULT TRUE,
    default_payment_terms INT DEFAULT 30
);

CREATE TABLE customer (
    customer_id INT PRIMARY KEY,
    customer_number VARCHAR(50) UNIQUE NOT NULL,
    customer_name VARCHAR(200) NOT NULL,
    customer_type_id VARCHAR(20) REFERENCES customer_type(customer_type_id),
    tax_id VARCHAR(50),
    registration_date DATE NOT NULL,
    status VARCHAR(20) NOT NULL CHECK (status IN ('ACTIVE', 'INACTIVE', 'SUSPENDED')),
    credit_limit DECIMAL(15,2) DEFAULT 0,
    currency VARCHAR(3) DEFAULT 'USD',
    payment_terms INT DEFAULT 30,
    credit_score INT CHECK (credit_score BETWEEN 0 AND 100),
    annual_revenue DECIMAL(18,2),
    industry_code VARCHAR(20),
    website VARCHAR(200),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE customer_address (
    address_id INT PRIMARY KEY,
    customer_id INT REFERENCES customer(customer_id) ON DELETE CASCADE,
    address_type VARCHAR(20) NOT NULL CHECK (address_type IN ('BILLING', 'SHIPPING', 'BOTH')),
    address_line1 VARCHAR(200) NOT NULL,
    address_line2 VARCHAR(200),
    city VARCHAR(100) NOT NULL,
    state VARCHAR(100),
    postal_code VARCHAR(20),
    country_code VARCHAR(2) NOT NULL,
    is_default BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE customer_contact (
    contact_id INT PRIMARY KEY,
    customer_id INT REFERENCES customer(customer_id) ON DELETE CASCADE,
    contact_name VARCHAR(200) NOT NULL,
    contact_role VARCHAR(100),
    email VARCHAR(200),
    phone VARCHAR(50),
    is_primary BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE product_category (
    category_id INT PRIMARY KEY,
    category_code VARCHAR(20) UNIQUE NOT NULL,
    category_name VARCHAR(200) NOT NULL,
    parent_category_id INT REFERENCES product_category(category_id),
    description VARCHAR(500),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE product (
    product_id INT PRIMARY KEY,
    product_number VARCHAR(50) UNIQUE NOT NULL,
    product_name VARCHAR(200) NOT NULL,
    category_id INT REFERENCES product_category(category_id),
    product_type VARCHAR(20) NOT NULL CHECK (product_type IN ('FINISHED_GOOD', 'RAW_MATERIAL', 'SERVICE', 'CONSUMABLE')),
    base_price DECIMAL(15,2) NOT NULL,
    cost DECIMAL(15,2),
    weight DECIMAL(10,3),
    weight_unit VARCHAR(10) DEFAULT 'KG',
    unit_of_measure VARCHAR(20) NOT NULL DEFAULT 'EACH',
    status VARCHAR(20) NOT NULL CHECK (status IN ('ACTIVE', 'DISCONTINUED', 'PHASE_OUT')),
    shelf_life_days INT,
    storage_temperature_min DECIMAL(5,2),
    storage_temperature_max DECIMAL(5,2),
    hazardous BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE price_list (
    price_list_id INT PRIMARY KEY,
    price_list_name VARCHAR(100) NOT NULL,
    currency VARCHAR(3) NOT NULL DEFAULT 'USD',
    effective_date DATE NOT NULL,
    expiration_date DATE,
    status VARCHAR(20) DEFAULT 'ACTIVE'
);

CREATE TABLE product_price (
    price_id INT PRIMARY KEY,
    product_id INT REFERENCES product(product_id),
    price_list_id INT REFERENCES price_list(price_list_id),
    price DECIMAL(15,2) NOT NULL,
    minimum_quantity INT DEFAULT 1,
    discount_percentage DECIMAL(5,2) DEFAULT 0,
    effective_date DATE NOT NULL,
    UNIQUE (product_id, price_list_id, effective_date)
);

CREATE TABLE sales_order (
    order_id INT PRIMARY KEY,
    order_number VARCHAR(50) UNIQUE NOT NULL,
    customer_id INT REFERENCES customer(customer_id),
    order_date DATE NOT NULL,
    required_date DATE,
    promised_date DATE,
    warehouse_id INT NOT NULL,
    sales_rep_id INT,
    shipping_method VARCHAR(50),
    payment_terms INT DEFAULT 30,
    currency VARCHAR(3) DEFAULT 'USD',
    subtotal DECIMAL(15,2) NOT NULL,
    tax_amount DECIMAL(15,2) DEFAULT 0,
    freight_amount DECIMAL(15,2) DEFAULT 0,
    total_amount DECIMAL(15,2) NOT NULL,
    status VARCHAR(20) NOT NULL CHECK (status IN ('DRAFT', 'CONFIRMED', 'PICKED', 'SHIPPED', 'INVOICED', 'CANCELLED')),
    priority VARCHAR(20) DEFAULT 'NORMAL' CHECK (priority IN ('LOW', 'NORMAL', 'HIGH', 'URGENT')),
    customer_po_number VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE sales_order_line (
    line_id INT PRIMARY KEY,
    order_id INT REFERENCES sales_order(order_id) ON DELETE CASCADE,
    line_number INT NOT NULL,
    product_id INT REFERENCES product(product_id),
    quantity_ordered DECIMAL(12,3) NOT NULL,
    quantity_shipped DECIMAL(12,3) DEFAULT 0,
    quantity_invoiced DECIMAL(12,3) DEFAULT 0,
    unit_price DECIMAL(15,2) NOT NULL,
    discount_percentage DECIMAL(5,2) DEFAULT 0,
    tax_percentage DECIMAL(5,2) DEFAULT 0,
    line_total DECIMAL(15,2) NOT NULL,
    status VARCHAR(20) DEFAULT 'OPEN' CHECK (status IN ('OPEN', 'PICKED', 'SHIPPED', 'INVOICED', 'CANCELLED')),
    requested_ship_date DATE,
    promised_ship_date DATE,
    UNIQUE (order_id, line_number)
);

CREATE TABLE invoice (
    invoice_id INT PRIMARY KEY,
    invoice_number VARCHAR(50) UNIQUE NOT NULL,
    invoice_type VARCHAR(20) NOT NULL CHECK (invoice_type IN ('SALES', 'PURCHASE', 'CREDIT_MEMO', 'DEBIT_MEMO')),
    customer_id INT REFERENCES customer(customer_id),
    order_id INT REFERENCES sales_order(order_id),
    invoice_date DATE NOT NULL,
    due_date DATE NOT NULL,
    currency VARCHAR(3) DEFAULT 'USD',
    subtotal DECIMAL(15,2) NOT NULL,
    tax_amount DECIMAL(15,2) DEFAULT 0,
    total_amount DECIMAL(15,2) NOT NULL,
    amount_paid DECIMAL(15,2) DEFAULT 0,
    balance_due DECIMAL(15,2) NOT NULL,
    status VARCHAR(20) NOT NULL CHECK (status IN ('DRAFT', 'POSTED', 'PAID', 'OVERDUE', 'VOID')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE invoice_line (
    invoice_line_id INT PRIMARY KEY,
    invoice_id INT REFERENCES invoice(invoice_id) ON DELETE CASCADE,
    line_number INT NOT NULL,
    product_id INT REFERENCES product(product_id),
    description VARCHAR(500),
    quantity DECIMAL(12,3) NOT NULL,
    unit_price DECIMAL(15,2) NOT NULL,
    tax_percentage DECIMAL(5,2) DEFAULT 0,
    line_total DECIMAL(15,2) NOT NULL,
    order_line_id INT REFERENCES sales_order_line(line_id),
    UNIQUE (invoice_id, line_number)
);

CREATE TABLE payment (
    payment_id INT PRIMARY KEY,
    payment_number VARCHAR(50) UNIQUE NOT NULL,
    payment_type VARCHAR(20) NOT NULL CHECK (payment_type IN ('RECEIPT', 'PAYMENT', 'REFUND')),
    customer_id INT REFERENCES customer(customer_id),
    invoice_id INT REFERENCES invoice(invoice_id),
    payment_date DATE NOT NULL,
    payment_method VARCHAR(20) NOT NULL CHECK (payment_method IN ('CASH', 'CREDIT_CARD', 'WIRE', 'CHECK', 'ACH')),
    amount DECIMAL(15,2) NOT NULL,
    currency VARCHAR(3) DEFAULT 'USD',
    reference_number VARCHAR(100),
    status VARCHAR(20) NOT NULL CHECK (status IN ('PENDING', 'COMPLETED', 'FAILED', 'REVERSED')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ============================================
-- PROCUREMENT & SUPPLIER MANAGEMENT
-- ============================================

CREATE TABLE supplier (
    supplier_id INT PRIMARY KEY,
    supplier_number VARCHAR(50) UNIQUE NOT NULL,
    supplier_name VARCHAR(200) NOT NULL,
    supplier_type VARCHAR(20) NOT NULL CHECK (supplier_type IN ('MANUFACTURER', 'DISTRIBUTOR', 'SERVICE_PROVIDER')),
    tax_id VARCHAR(50),
    registration_date DATE NOT NULL,
    status VARCHAR(20) NOT NULL CHECK (status IN ('ACTIVE', 'INACTIVE', 'ON_HOLD', 'BLACKLISTED')),
    payment_terms INT DEFAULT 30,
    currency VARCHAR(3) DEFAULT 'USD',
    credit_rating VARCHAR(10) CHECK (credit_rating IN ('A', 'B', 'C', 'D')),
    lead_time_days INT DEFAULT 0,
    quality_rating DECIMAL(3,2) CHECK (quality_rating BETWEEN 0 AND 5),
    on_time_delivery_rate DECIMAL(5,2) CHECK (on_time_delivery_rate BETWEEN 0 AND 100),
    website VARCHAR(200),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE supplier_address (
    address_id INT PRIMARY KEY,
    supplier_id INT REFERENCES supplier(supplier_id) ON DELETE CASCADE,
    address_type VARCHAR(20) NOT NULL CHECK (address_type IN ('MAIN', 'BILLING', 'SHIPPING', 'RETURN')),
    address_line1 VARCHAR(200) NOT NULL,
    address_line2 VARCHAR(200),
    city VARCHAR(100) NOT NULL,
    state VARCHAR(100),
    postal_code VARCHAR(20),
    country_code VARCHAR(2) NOT NULL,
    is_primary BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE supplier_contact (
    contact_id INT PRIMARY KEY,
    supplier_id INT REFERENCES supplier(supplier_id) ON DELETE CASCADE,
    contact_name VARCHAR(200) NOT NULL,
    contact_role VARCHAR(100),
    email VARCHAR(200),
    phone VARCHAR(50),
    is_primary BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE supplier_contract (
    contract_id INT PRIMARY KEY,
    contract_number VARCHAR(50) UNIQUE NOT NULL,
    supplier_id INT REFERENCES supplier(supplier_id),
    contract_type VARCHAR(20) NOT NULL CHECK (contract_type IN ('FIXED_PRICE', 'COST_PLUS', 'RATE_BASED', 'FRAMEWORK')),
    start_date DATE NOT NULL,
    end_date DATE,
    auto_renew BOOLEAN DEFAULT FALSE,
    payment_terms INT,
    currency VARCHAR(3) DEFAULT 'USD',
    total_value DECIMAL(18,2),
    status VARCHAR(20) NOT NULL CHECK (status IN ('DRAFT', 'ACTIVE', 'EXPIRED', 'TERMINATED')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE purchase_order (
    po_id INT PRIMARY KEY,
    po_number VARCHAR(50) UNIQUE NOT NULL,
    supplier_id INT REFERENCES supplier(supplier_id),
    order_date DATE NOT NULL,
    required_date DATE,
    promised_date DATE,
    warehouse_id INT NOT NULL,
    buyer_id INT,
    payment_terms INT DEFAULT 30,
    currency VARCHAR(3) DEFAULT 'USD',
    subtotal DECIMAL(15,2) NOT NULL,
    tax_amount DECIMAL(15,2) DEFAULT 0,
    freight_amount DECIMAL(15,2) DEFAULT 0,
    total_amount DECIMAL(15,2) NOT NULL,
    status VARCHAR(20) NOT NULL CHECK (status IN ('DRAFT', 'SUBMITTED', 'ACKNOWLEDGED', 'PARTIAL', 'RECEIVED', 'CLOSED', 'CANCELLED')),
    priority VARCHAR(20) DEFAULT 'NORMAL' CHECK (priority IN ('LOW', 'NORMAL', 'HIGH', 'URGENT')),
    approved_by INT,
    approval_date DATE,
    supplier_reference VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE purchase_order_line (
    line_id INT PRIMARY KEY,
    po_id INT REFERENCES purchase_order(po_id) ON DELETE CASCADE,
    line_number INT NOT NULL,
    product_id INT REFERENCES product(product_id),
    quantity_ordered DECIMAL(12,3) NOT NULL,
    quantity_received DECIMAL(12,3) DEFAULT 0,
    quantity_invoiced DECIMAL(12,3) DEFAULT 0,
    unit_price DECIMAL(15,2) NOT NULL,
    discount_percentage DECIMAL(5,2) DEFAULT 0,
    tax_percentage DECIMAL(5,2) DEFAULT 0,
    line_total DECIMAL(15,2) NOT NULL,
    promised_date DATE,
    status VARCHAR(20) DEFAULT 'OPEN' CHECK (status IN ('OPEN', 'PARTIAL', 'RECEIVED', 'CANCELLED')),
    supplier_part_number VARCHAR(100),
    UNIQUE (po_id, line_number)
);

CREATE TABLE purchase_receipt (
    receipt_id INT PRIMARY KEY,
    receipt_number VARCHAR(50) UNIQUE NOT NULL,
    po_id INT REFERENCES purchase_order(po_id),
    supplier_id INT REFERENCES supplier(supplier_id),
    warehouse_id INT NOT NULL,
    receipt_date DATE NOT NULL,
    received_by INT,
    carrier VARCHAR(100),
    tracking_number VARCHAR(100),
    status VARCHAR(20) NOT NULL CHECK (status IN ('RECEIVED', 'INSPECTED', 'PUT_AWAY', 'REJECTED')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE purchase_receipt_line (
    receipt_line_id INT PRIMARY KEY,
    receipt_id INT REFERENCES purchase_receipt(receipt_id) ON DELETE CASCADE,
    po_line_id INT REFERENCES purchase_order_line(line_id),
    product_id INT REFERENCES product(product_id),
    quantity_ordered DECIMAL(12,3) NOT NULL,
    quantity_received DECIMAL(12,3) NOT NULL,
    quantity_rejected DECIMAL(12,3) DEFAULT 0,
    unit_cost DECIMAL(15,2) NOT NULL,
    lot_number VARCHAR(50),
    expiration_date DATE,
    location_id INT,
    inspection_required BOOLEAN DEFAULT FALSE,
    UNIQUE (receipt_id, po_line_id)
);

-- ============================================
-- INVENTORY & WAREHOUSING
-- ============================================

CREATE TABLE warehouse (
    warehouse_id INT PRIMARY KEY,
    warehouse_code VARCHAR(20) UNIQUE NOT NULL,
    warehouse_name VARCHAR(100) NOT NULL,
    warehouse_type VARCHAR(20) NOT NULL CHECK (warehouse_type IN ('COMPANY_OWNED', '3PL', 'VIRTUAL', 'TRANSIT')),
    location_address VARCHAR(500),
    city VARCHAR(100),
    state VARCHAR(100),
    country_code VARCHAR(2) NOT NULL,
    capacity_cubic_meters DECIMAL(12,2),
    manager_id INT,
    status VARCHAR(20) NOT NULL CHECK (status IN ('ACTIVE', 'INACTIVE', 'UNDER_MAINTENANCE')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE warehouse_zone (
    zone_id INT PRIMARY KEY,
    warehouse_id INT REFERENCES warehouse(warehouse_id) ON DELETE CASCADE,
    zone_code VARCHAR(20) NOT NULL,
    zone_name VARCHAR(100) NOT NULL,
    zone_type VARCHAR(20) NOT NULL CHECK (zone_type IN ('BULK', 'PICK', 'STAGING', 'RECEIVING', 'SHIPPING')),
    temperature_controlled BOOLEAN DEFAULT FALSE,
    UNIQUE (warehouse_id, zone_code)
);

CREATE TABLE bin_location (
    bin_id INT PRIMARY KEY,
    warehouse_id INT REFERENCES warehouse(warehouse_id) ON DELETE CASCADE,
    zone_id INT REFERENCES warehouse_zone(zone_id),
    bin_code VARCHAR(50) NOT NULL,
    aisle VARCHAR(20),
    shelf VARCHAR(20),
    position VARCHAR(20),
    bin_type VARCHAR(20) NOT NULL CHECK (bin_type IN ('BULK', 'PICK', 'FLOW_RACK', 'CANTILEVER')),
    capacity_quantity DECIMAL(12,3),
    capacity_weight DECIMAL(10,3),
    status VARCHAR(20) NOT NULL CHECK (status IN ('ACTIVE', 'FULL', 'LOCKED', 'QUARANTINE')),
    UNIQUE (warehouse_id, bin_code)
);

CREATE TABLE inventory_on_hand (
    inventory_id INT PRIMARY KEY,
    product_id INT REFERENCES product(product_id),
    warehouse_id INT REFERENCES warehouse(warehouse_id),
    bin_id INT REFERENCES bin_location(bin_id),
    lot_number VARCHAR(50),
    quantity_on_hand DECIMAL(12,3) NOT NULL,
    quantity_allocated DECIMAL(12,3) DEFAULT 0,
    quantity_available DECIMAL(12,3) GENERATED ALWAYS AS (quantity_on_hand - quantity_allocated) STORED,
    unit_cost DECIMAL(15,2),
    last_received_date DATE,
    expiration_date DATE,
    UNIQUE (product_id, warehouse_id, bin_id, lot_number)
);

CREATE TABLE inventory_transaction (
    transaction_id INT PRIMARY KEY,
    transaction_number VARCHAR(50) UNIQUE NOT NULL,
    product_id INT REFERENCES product(product_id),
    warehouse_id INT REFERENCES warehouse(warehouse_id),
    bin_id INT REFERENCES bin_location(bin_id),
    transaction_type VARCHAR(20) NOT NULL CHECK (transaction_type IN ('RECEIPT', 'ISSUE', 'TRANSFER', 'ADJUSTMENT', 'CYCLE_COUNT', 'SCRAP', 'RETURN')),
    transaction_date DATE NOT NULL,
    quantity DECIMAL(12,3) NOT NULL,
    unit_cost DECIMAL(15,2),
    reference_type VARCHAR(50),
    reference_id INT,
    reason_code VARCHAR(20),
    created_by INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE stock_transfer (
    transfer_id INT PRIMARY KEY,
    transfer_number VARCHAR(50) UNIQUE NOT NULL,
    from_warehouse_id INT REFERENCES warehouse(warehouse_id),
    to_warehouse_id INT REFERENCES warehouse(warehouse_id),
    transfer_date DATE NOT NULL,
    required_date DATE,
    shipment_method VARCHAR(50),
    tracking_number VARCHAR(100),
    status VARCHAR(20) NOT NULL CHECK (status IN ('DRAFT', 'PICKED', 'SHIPPED', 'RECEIVED', 'CANCELLED')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE stock_transfer_line (
    transfer_line_id INT PRIMARY KEY,
    transfer_id INT REFERENCES stock_transfer(transfer_id) ON DELETE CASCADE,
    product_id INT REFERENCES product(product_id),
    from_bin_id INT REFERENCES bin_location(bin_id),
    to_bin_id INT REFERENCES bin_location(bin_id),
    quantity_requested DECIMAL(12,3) NOT NULL,
    quantity_shipped DECIMAL(12,3) DEFAULT 0,
    quantity_received DECIMAL(12,3) DEFAULT 0,
    status VARCHAR(20) DEFAULT 'PENDING' CHECK (status IN ('PENDING', 'PICKED', 'SHIPPED', 'RECEIVED', 'CANCELLED'))
);

-- ============================================
-- PRODUCTION & MANUFACTURING
-- ============================================

CREATE TABLE production_line (
    line_id INT PRIMARY KEY,
    line_code VARCHAR(20) UNIQUE NOT NULL,
    line_name VARCHAR(100) NOT NULL,
    line_type VARCHAR(20) NOT NULL CHECK (line_type IN ('ASSEMBLY', 'DISCRETE', 'PROCESS', 'MIXING')),
    location_id INT REFERENCES warehouse(warehouse_id),
    capacity_per_hour DECIMAL(10,2),
    setup_time_minutes INT DEFAULT 0,
    status VARCHAR(20) NOT NULL CHECK (status IN ('ACTIVE', 'MAINTENANCE', 'INACTIVE')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE bill_of_materials (
    bom_id INT PRIMARY KEY,
    parent_product_id INT REFERENCES product(product_id),
    component_product_id INT REFERENCES product(product_id),
    quantity DECIMAL(12,3) NOT NULL,
    unit_of_measure VARCHAR(20) NOT NULL,
    scrap_percentage DECIMAL(5,2) DEFAULT 0,
    effective_start_date DATE NOT NULL,
    effective_end_date DATE,
    component_type VARCHAR(20) DEFAULT 'COMPONENT' CHECK (component_type IN ('COMPONENT', 'PHANTOM', 'BYPRODUCT', 'CO_PRODUCT')),
    UNIQUE (parent_product_id, component_product_id, effective_start_date)
);

CREATE TABLE work_order (
    work_order_id INT PRIMARY KEY,
    work_order_number VARCHAR(50) UNIQUE NOT NULL,
    product_id INT REFERENCES product(product_id),
    production_line_id INT REFERENCES production_line(line_id),
    warehouse_id INT REFERENCES warehouse(warehouse_id),
    quantity_ordered DECIMAL(12,3) NOT NULL,
    quantity_completed DECIMAL(12,3) DEFAULT 0,
    quantity_scrapped DECIMAL(12,3) DEFAULT 0,
    start_date DATE NOT NULL,
    required_date DATE NOT NULL,
    actual_start_date DATE,
    actual_finish_date DATE,
    status VARCHAR(20) NOT NULL CHECK (status IN ('DRAFT', 'RELEASED', 'IN_PROGRESS', 'COMPLETED', 'CANCELLED')),
    priority VARCHAR(20) DEFAULT 'NORMAL' CHECK (priority IN ('LOW', 'NORMAL', 'HIGH', 'URGENT')),
    created_by INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE work_order_material (
    material_id INT PRIMARY KEY,
    work_order_id INT REFERENCES work_order(work_order_id) ON DELETE CASCADE,
    product_id INT REFERENCES product(product_id),
    quantity_required DECIMAL(12,3) NOT NULL,
    quantity_issued DECIMAL(12,3) DEFAULT 0,
    unit_cost DECIMAL(15,2),
    bin_id INT REFERENCES bin_location(bin_id),
    status VARCHAR(20) DEFAULT 'PENDING' CHECK (status IN ('PENDING', 'ISSUED', 'PARTIAL', 'COMPLETE'))
);

CREATE TABLE production_schedule (
    schedule_id INT PRIMARY KEY,
    work_order_id INT REFERENCES work_order(work_order_id),
    production_line_id INT REFERENCES production_line(line_id),
    scheduled_start TIMESTAMP NOT NULL,
    scheduled_end TIMESTAMP NOT NULL,
    actual_start TIMESTAMP,
    actual_end TIMESTAMP,
    status VARCHAR(20) NOT NULL CHECK (status IN ('SCHEDULED', 'RUNNING', 'COMPLETED', 'CANCELLED')),
    priority INT DEFAULT 5 CHECK (priority BETWEEN 1 AND 10),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ============================================
-- QUALITY & COMPLIANCE
-- ============================================

CREATE TABLE quality_standard (
    standard_id INT PRIMARY KEY,
    standard_code VARCHAR(20) UNIQUE NOT NULL,
    standard_name VARCHAR(200) NOT NULL,
    standard_type VARCHAR(20) NOT NULL CHECK (standard_type IN ('INTERNAL', 'ISO', 'ASTM', 'FDA', 'CE')),
    version VARCHAR(20),
    issue_date DATE,
    status VARCHAR(20) NOT NULL CHECK (status IN ('ACTIVE', 'SUPERSEDED', 'DRAFT')),
    description TEXT
);

CREATE TABLE quality_inspection (
    inspection_id INT PRIMARY KEY,
    inspection_number VARCHAR(50) UNIQUE NOT NULL,
    inspection_type VARCHAR(20) NOT NULL CHECK (inspection_type IN ('INCOMING', 'IN_PROCESS', 'FINAL', 'AUDIT')),
    reference_type VARCHAR(50),
    reference_id INT,
    product_id INT REFERENCES product(product_id),
    warehouse_id INT REFERENCES warehouse(warehouse_id),
    inspection_date DATE NOT NULL,
    inspector_id INT,
    result VARCHAR(20) NOT NULL CHECK (result IN ('PENDING', 'PASS', 'FAIL', 'CONDITIONAL_PASS')),
    defects_found INT DEFAULT 0,
    sample_size INT,
    batch_size INT,
    standard_id INT REFERENCES quality_standard(standard_id),
    notes TEXT,
    status VARCHAR(20) NOT NULL CHECK (status IN ('PENDING', 'COMPLETED', 'CANCELLED')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE non_conformance_report (
    ncr_id INT PRIMARY KEY,
    ncr_number VARCHAR(50) UNIQUE NOT NULL,
    ncr_type VARCHAR(20) NOT NULL CHECK (ncr_type IN ('PRODUCT', 'PROCESS', 'DOCUMENTATION', 'SUPPLIER')),
    reference_type VARCHAR(50),
    reference_id INT,
    product_id INT REFERENCES product(product_id),
    issue_date DATE NOT NULL,
    reported_by INT,
    severity VARCHAR(20) NOT NULL CHECK (severity IN ('MINOR', 'MAJOR', 'CRITICAL')),
    root_cause TEXT,
    corrective_action TEXT,
    preventive_action TEXT,
    status VARCHAR(20) NOT NULL CHECK (status IN ('OPEN', 'IN_PROGRESS', 'CLOSED', 'VERIFIED')),
    resolution_date DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ============================================
-- FINANCE & ACCOUNTING
-- ============================================

CREATE TABLE account_type (
    account_type_id INT PRIMARY KEY,
    type_code VARCHAR(10) UNIQUE NOT NULL,
    type_name VARCHAR(100) NOT NULL,
    balance_type VARCHAR(10) NOT NULL CHECK (balance_type IN ('DEBIT', 'CREDIT'))
);

CREATE TABLE general_ledger_account (
    account_id INT PRIMARY KEY,
    account_number VARCHAR(50) UNIQUE NOT NULL,
    account_name VARCHAR(200) NOT NULL,
    account_type_id INT REFERENCES account_type(account_type_id),
    parent_account_id INT REFERENCES general_ledger_account(account_id),
    currency VARCHAR(3) DEFAULT 'USD',
    description TEXT,
    status VARCHAR(20) NOT NULL CHECK (status IN ('ACTIVE', 'INACTIVE')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE accounting_period (
    period_id INT PRIMARY KEY,
    period_code VARCHAR(20) UNIQUE NOT NULL,
    period_name VARCHAR(50) NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    fiscal_year INT NOT NULL,
    is_closed BOOLEAN DEFAULT FALSE,
    closed_at TIMESTAMP,
    UNIQUE (fiscal_year, period_code)
);

CREATE TABLE journal_entry (
    entry_id INT PRIMARY KEY,
    entry_number VARCHAR(50) UNIQUE NOT NULL,
    entry_date DATE NOT NULL,
    period_id INT REFERENCES accounting_period(period_id),
    source_document_type VARCHAR(50),
    source_document_id INT,
    entry_type VARCHAR(20) NOT NULL CHECK (entry_type IN ('SALES', 'PURCHASE', 'PAYMENT', 'RECEIPT', 'ADJUSTMENT', 'REVERSAL')),
    currency VARCHAR(3) DEFAULT 'USD',
    description TEXT,
    created_by INT,
    approved_by INT,
    approval_date TIMESTAMP,
    total_debit DECIMAL(15,2) NOT NULL,
    total_credit DECIMAL(15,2) NOT NULL,
    status VARCHAR(20) NOT NULL CHECK (status IN ('DRAFT', 'SUBMITTED', 'APPROVED', 'POSTED', 'REVERSED')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE journal_entry_line (
    line_id INT PRIMARY KEY,
    entry_id INT REFERENCES journal_entry(entry_id) ON DELETE CASCADE,
    line_number INT NOT NULL,
    account_id INT REFERENCES general_ledger_account(account_id),
    debit_amount DECIMAL(15,2) DEFAULT 0,
    credit_amount DECIMAL(15,2) DEFAULT 0,
    description VARCHAR(500),
    cost_center_id INT,
    reference_type VARCHAR(50),
    reference_id INT,
    UNIQUE (entry_id, line_number),
    CHECK ((debit_amount > 0 AND credit_amount = 0) OR (credit_amount > 0 AND debit_amount = 0))
);

CREATE TABLE accounts_receivable (
    ar_id INT PRIMARY KEY,
    customer_id INT REFERENCES customer(customer_id),
    invoice_id INT REFERENCES invoice(invoice_id),
    amount_original DECIMAL(15,2) NOT NULL,
    amount_due DECIMAL(15,2) NOT NULL,
    invoice_date DATE NOT NULL,
    due_date DATE NOT NULL,
    days_overdue INT GENERATED ALWAYS AS (DATEDIFF(CURRENT_DATE, due_date)) STORED,
    status VARCHAR(20) NOT NULL CHECK (status IN ('CURRENT', 'DUE', 'OVERDUE', 'COLLECTION', 'WRITE_OFF')),
    collection_status VARCHAR(20),
    last_contact_date DATE,
    next_action_date DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE accounts_payable (
    ap_id INT PRIMARY KEY,
    supplier_id INT REFERENCES supplier(supplier_id),
    invoice_id INT REFERENCES invoice(invoice_id),
    amount_original DECIMAL(15,2) NOT NULL,
    amount_due DECIMAL(15,2) NOT NULL,
    invoice_date DATE NOT NULL,
    due_date DATE NOT NULL,
    discount_available DECIMAL(15,2) DEFAULT 0,
    discount_until DATE,
    payment_terms INT DEFAULT 30,
    status VARCHAR(20) NOT NULL CHECK (status IN ('NEW', 'APPROVED', 'PAID', 'OVERDUE', 'DISPUTED')),
    payment_priority INT DEFAULT 5 CHECK (payment_priority BETWEEN 1 AND 10),
    payment_date DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE budget (
    budget_id INT PRIMARY KEY,
    budget_name VARCHAR(200) NOT NULL,
    budget_type VARCHAR(20) NOT NULL CHECK (budget_type IN ('OPERATING', 'CAPITAL', 'PROJECT')),
    fiscal_year INT NOT NULL,
    department_id INT,
    account_id INT REFERENCES general_ledger_account(account_id),
    budgeted_amount DECIMAL(18,2) NOT NULL,
    actual_amount DECIMAL(18,2) DEFAULT 0,
    variance DECIMAL(18,2) GENERATED ALWAYS AS (budgeted_amount - actual_amount) STORED,
    currency VARCHAR(3) DEFAULT 'USD',
    status VARCHAR(20) NOT NULL CHECK (status IN ('DRAFT', 'APPROVED', 'ACTIVE', 'CLOSED')),
    version INT DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ============================================
-- HUMAN RESOURCES
-- ============================================

CREATE TABLE department (
    department_id INT PRIMARY KEY,
    department_code VARCHAR(20) UNIQUE NOT NULL,
    department_name VARCHAR(200) NOT NULL,
    parent_department_id INT REFERENCES department(department_id),
    manager_id INT,
    budget_code VARCHAR(20),
    location VARCHAR(200),
    status VARCHAR(20) NOT NULL CHECK (status IN ('ACTIVE', 'INACTIVE')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE position (
    position_id INT PRIMARY KEY,
    position_code VARCHAR(20) UNIQUE NOT NULL,
    position_title VARCHAR(200) NOT NULL,
    job_family VARCHAR(50),
    grade_level INT,
    department_id INT REFERENCES department(department_id),
    min_salary DECIMAL(15,2),
    max_salary DECIMAL(15,2),
    flsa_status VARCHAR(20) CHECK (flsa_status IN ('EXEMPT', 'NON_EXEMPT')),
    status VARCHAR(20) NOT NULL CHECK (status IN ('ACTIVE', 'INACTIVE')),
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE employee (
    employee_id INT PRIMARY KEY,
    employee_number VARCHAR(20) UNIQUE NOT NULL,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    employee_type VARCHAR(20) NOT NULL CHECK (employee_type IN ('FULL_TIME', 'PART_TIME', 'CONTRACT', 'TEMPORARY')),
    department_id INT REFERENCES department(department_id),
    position_id INT REFERENCES position(position_id),
    manager_id INT REFERENCES employee(employee_id),
    hire_date DATE NOT NULL,
    termination_date DATE,
    status VARCHAR(20) NOT NULL CHECK (status IN ('ACTIVE', 'ON_LEAVE', 'TERMINATED')),
    annual_salary DECIMAL(15,2),
    hourly_rate DECIMAL(10,2),
    email VARCHAR(200),
    phone VARCHAR(50),
    location VARCHAR(200),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE time_entry (
    time_entry_id INT PRIMARY KEY,
    employee_id INT REFERENCES employee(employee_id),
    project_id INT,
    work_date DATE NOT NULL,
    hours_worked DECIMAL(5,2) NOT NULL CHECK (hours_worked > 0),
    work_type VARCHAR(50),
    description TEXT,
    approval_status VARCHAR(20) NOT NULL CHECK (approval_status IN ('PENDING', 'APPROVED', 'REJECTED')),
    submitted_date DATE,
    approved_by INT REFERENCES employee(employee_id),
    approved_date DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ============================================
-- LOGISTICS & SHIPPING
-- ============================================

CREATE TABLE carrier (
    carrier_id INT PRIMARY KEY,
    carrier_code VARCHAR(20) UNIQUE NOT NULL,
    carrier_name VARCHAR(200) NOT NULL,
    carrier_type VARCHAR(20) NOT NULL CHECK (carrier_type IN ('LTL', 'FTL', 'PARCEL', 'AIR', 'OCEAN', 'RAIL')),
    service_level VARCHAR(50),
    contact_phone VARCHAR(50),
    contact_email VARCHAR(200),
    rating DECIMAL(3,2) CHECK (rating BETWEEN 0 AND 5),
    status VARCHAR(20) NOT NULL CHECK (status IN ('ACTIVE', 'INACTIVE')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE shipping_route (
    route_id INT PRIMARY KEY,
    route_code VARCHAR(20) UNIQUE NOT NULL,
    route_name VARCHAR(200) NOT NULL,
    origin_location_id INT REFERENCES warehouse(warehouse_id),
    destination_location_id INT REFERENCES warehouse(warehouse_id),
    distance_km DECIMAL(10,2),
    estimated_hours DECIMAL(8,2),
    carrier_id INT REFERENCES carrier(carrier_id),
    service_level VARCHAR(50),
    cost_per_km DECIMAL(10,2),
    status VARCHAR(20) NOT NULL CHECK (status IN ('ACTIVE', 'INACTIVE')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE shipment (
    shipment_id INT PRIMARY KEY,
    shipment_number VARCHAR(50) UNIQUE NOT NULL,
    shipment_type VARCHAR(20) NOT NULL CHECK (shipment_type IN ('OUTBOUND', 'INBOUND', 'TRANSFER', 'RETURN')),
    origin_location_id INT REFERENCES warehouse(warehouse_id),
    destination_location_id INT REFERENCES warehouse(warehouse_id),
    reference_type VARCHAR(50),
    reference_id INT,
    ship_date DATE NOT NULL,
    estimated_arrival DATE,
    actual_arrival DATE,
    carrier_id INT REFERENCES carrier(carrier_id),
    route_id INT REFERENCES shipping_route(route_id),
    tracking_number VARCHAR(100),
    freight_cost DECIMAL(15,2),
    weight DECIMAL(10,3),
    status VARCHAR(20) NOT NULL CHECK (status IN ('PENDING', 'PICKED', 'SHIPPED', 'IN_TRANSIT', 'DELIVERED', 'EXCEPTION', 'CANCELLED')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE shipment_line (
    shipment_line_id INT PRIMARY KEY,
    shipment_id INT REFERENCES shipment(shipment_id) ON DELETE CASCADE,
    line_number INT NOT NULL,
    product_id INT REFERENCES product(product_id),
    description VARCHAR(500),
    quantity DECIMAL(12,3) NOT NULL,
    unit_of_measure VARCHAR(20),
    weight DECIMAL(10,3),
    reference_line_id INT,
    UNIQUE (shipment_id, line_number)
);

-- ============================================
-- PROJECT MANAGEMENT
-- ============================================

CREATE TABLE project (
    project_id INT PRIMARY KEY,
    project_code VARCHAR(20) UNIQUE NOT NULL,
    project_name VARCHAR(200) NOT NULL,
    project_type VARCHAR(20) NOT NULL CHECK (project_type IN ('CUSTOMER', 'INTERNAL', 'R&D', 'CAPITAL')),
    customer_id INT REFERENCES customer(customer_id),
    project_manager_id INT REFERENCES employee(employee_id),
    start_date DATE NOT NULL,
    end_date DATE,
    budget_amount DECIMAL(18,2),
    actual_cost DECIMAL(18,2) DEFAULT 0,
    status VARCHAR(20) NOT NULL CHECK (status IN ('PLANNING', 'ACTIVE', 'ON_HOLD', 'COMPLETED', 'CANCELLED')),
    priority VARCHAR(20) DEFAULT 'NORMAL' CHECK (priority IN ('LOW', 'NORMAL', 'HIGH', 'URGENT')),
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE project_task (
    task_id INT PRIMARY KEY,
    project_id INT REFERENCES project(project_id) ON DELETE CASCADE,
    task_number VARCHAR(50) NOT NULL,
    task_name VARCHAR(200) NOT NULL,
    parent_task_id INT REFERENCES project_task(task_id),
    assigned_to INT REFERENCES employee(employee_id),
    start_date DATE NOT NULL,
    due_date DATE NOT NULL,
    actual_start_date DATE,
    actual_finish_date DATE,
    estimated_hours DECIMAL(10,2),
    actual_hours DECIMAL(10,2) DEFAULT 0,
    status VARCHAR(20) NOT NULL CHECK (status IN ('NOT_STARTED', 'IN_PROGRESS', 'COMPLETED', 'ON_HOLD', 'CANCELLED')),
    completion_percentage DECIMAL(5,2) DEFAULT 0 CHECK (completion_percentage BETWEEN 0 AND 100),
    priority VARCHAR(20) DEFAULT 'NORMAL' CHECK (priority IN ('LOW', 'NORMAL', 'HIGH', 'URGENT')),
    UNIQUE (project_id, task_number)
);

-- ============================================
-- SYSTEM & SECURITY
-- ============================================

CREATE TABLE app_user (
    user_id INT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(200) UNIQUE NOT NULL,
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    user_type VARCHAR(20) NOT NULL CHECK (user_type IN ('EMPLOYEE', 'CUSTOMER', 'SUPPLIER', 'ADMIN')),
    employee_id INT REFERENCES employee(employee_id),
    customer_id INT REFERENCES customer(customer_id),
    supplier_id INT REFERENCES supplier(supplier_id),
    status VARCHAR(20) NOT NULL CHECK (status IN ('ACTIVE', 'INACTIVE', 'LOCKED', 'PENDING')),
    failed_login_attempts INT DEFAULT 0,
    last_login_date TIMESTAMP,
    password_changed_date DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE role (
    role_id INT PRIMARY KEY,
    role_code VARCHAR(50) UNIQUE NOT NULL,
    role_name VARCHAR(100) NOT NULL,
    role_type VARCHAR(20) NOT NULL CHECK (role_type IN ('SYSTEM', 'BUSINESS', 'CUSTOM')),
    description TEXT,
    status VARCHAR(20) NOT NULL CHECK (status IN ('ACTIVE', 'INACTIVE')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE user_role (
    user_role_id INT PRIMARY KEY,
    user_id INT REFERENCES app_user(user_id) ON DELETE CASCADE,
    role_id INT REFERENCES role(role_id) ON DELETE CASCADE,
    assigned_date DATE NOT NULL,
    assigned_by INT REFERENCES app_user(user_id),
    expiry_date DATE,
    status VARCHAR(20) NOT NULL CHECK (status IN ('ACTIVE', 'EXPIRED', 'REVOKED')),
    UNIQUE (user_id, role_id)
);

CREATE TABLE audit_log (
    log_id BIGINT PRIMARY KEY,
    event_type VARCHAR(50) NOT NULL,
    user_id INT REFERENCES app_user(user_id),
    entity_type VARCHAR(50) NOT NULL,
    entity_id INT NOT NULL,
    action VARCHAR(20) NOT NULL CHECK (action IN ('CREATE', 'READ', 'UPDATE', 'DELETE', 'LOGIN', 'LOGOUT', 'EXPORT')),
    old_value JSON,
    new_value JSON,
    ip_address VARCHAR(50),
    user_agent VARCHAR(500),
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_audit_entity (entity_type, entity_id),
    INDEX idx_audit_user (user_id),
    INDEX idx_audit_timestamp (timestamp)
);

-- ============================================
-- INDEXES FOR PERFORMANCE
-- ============================================

-- Customer indexes
CREATE INDEX idx_customer_type ON customer(customer_type_id);
CREATE INDEX idx_customer_status ON customer(status);
CREATE INDEX idx_customer_name ON customer(customer_name);

-- Product indexes
CREATE INDEX idx_product_category ON product(category_id);
CREATE INDEX idx_product_status ON product(status);
CREATE INDEX idx_product_type ON product(product_type);
CREATE INDEX idx_product_name ON product(product_name);

-- Sales Order indexes
CREATE INDEX idx_sales_order_customer ON sales_order(customer_id);
CREATE INDEX idx_sales_order_status ON sales_order(status);
CREATE INDEX idx_sales_order_date ON sales_order(order_date);
CREATE INDEX idx_sales_order_warehouse ON sales_order(warehouse_id);

-- Purchase Order indexes
CREATE INDEX idx_purchase_order_supplier ON purchase_order(supplier_id);
CREATE INDEX idx_purchase_order_status ON purchase_order(status);
CREATE INDEX idx_purchase_order_date ON purchase_order(order_date);
CREATE INDEX idx_purchase_order_warehouse ON purchase_order(warehouse_id);

-- Inventory indexes
CREATE INDEX idx_inventory_product ON inventory_on_hand(product_id);
CREATE INDEX idx_inventory_warehouse ON inventory_on_hand(warehouse_id);
CREATE INDEX idx_inventory_bin ON inventory_on_hand(bin_id);
CREATE INDEX idx_inventory_transaction_product ON inventory_transaction(product_id);
CREATE INDEX idx_inventory_transaction_date ON inventory_transaction(transaction_date);

-- Work Order indexes
CREATE INDEX idx_work_order_product ON work_order(product_id);
CREATE INDEX idx_work_order_status ON work_order(status);
CREATE INDEX idx_work_order_dates ON work_order(start_date, required_date);

-- Invoice indexes
CREATE INDEX idx_invoice_customer ON invoice(customer_id);
CREATE INDEX idx_invoice_status ON invoice(status);
CREATE INDEX idx_invoice_due_date ON invoice(due_date);

-- Payment indexes
CREATE INDEX idx_payment_customer ON payment(customer_id);
CREATE INDEX idx_payment_status ON payment(status);
CREATE INDEX idx_payment_date ON payment(payment_date);

-- AP/AR indexes
CREATE INDEX idx_ar_customer ON accounts_receivable(customer_id);
CREATE INDEX idx_ar_status ON accounts_receivable(status);
CREATE INDEX idx_ar_due_date ON accounts_receivable(due_date);
CREATE INDEX idx_ap_supplier ON accounts_payable(supplier_id);
CREATE INDEX idx_ap_status ON accounts_payable(status);
CREATE INDEX idx_ap_due_date ON accounts_payable(due_date);

-- Employee indexes
CREATE INDEX idx_employee_department ON employee(department_id);
CREATE INDEX idx_employee_status ON employee(status);
CREATE INDEX idx_employee_manager ON employee(manager_id);

-- Project indexes
CREATE INDEX idx_project_customer ON project(customer_id);
CREATE INDEX idx_project_manager ON project(project_manager_id);
CREATE INDEX idx_project_status ON project(status);
CREATE INDEX idx_project_task_project ON project_task(project_id);
CREATE INDEX idx_project_task_assigned ON project_task(assigned_to);

-- Quality indexes
CREATE INDEX idx_inspection_product ON quality_inspection(product_id);
CREATE INDEX idx_inspection_status ON quality_inspection(status);
CREATE INDEX idx_inspection_date ON quality_inspection(inspection_date);

-- Shipment indexes
CREATE INDEX idx_shipment_origin ON shipment(origin_location_id);
CREATE INDEX idx_shipment_destination ON shipment(destination_location_id);
CREATE INDEX idx_shipment_status ON shipment(status);
CREATE INDEX idx_shipment_carrier ON shipment(carrier_id);
