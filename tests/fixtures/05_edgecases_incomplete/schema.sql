-- Enterprise Database Schema
-- Version: 2.1 (with known inconsistencies)
-- Last Updated: 2024-02-28
-- Status: Production (with documented issues)

-- ============================================================================
-- CUSTOMERS TABLE
-- ============================================================================
-- NOTE: Naming convention inconsistency - mix of snake_case and camelCase
-- NOTE: Some columns may be legacy duplicates

CREATE TABLE CUSTOMERS (
    customer_id INTEGER PRIMARY KEY,
    CustomerID INTEGER,  -- Possible duplicate - verify before cleanup
    firstName VARCHAR(50),
    first_name VARCHAR(50),  -- Appears to be duplicate
    lastName VARCHAR(50),
    last_name VARCHAR(100),  -- Appears to be duplicate
    email VARCHAR(255),
    emailAddress VARCHAR(255),  -- Possible duplicate
    phone VARCHAR(20),
    phoneNumber VARCHAR(20),  -- Possible duplicate
    created_at TIMESTAMP,
    CreatedDate DATETIME,  -- Different data type for same purpose?
    account_status VARCHAR(20),
    status VARCHAR(20),  -- Duplicate?
    customer_type VARCHAR(30),
    customer_region VARCHAR(50)
    -- NOTE: NOT NULL constraints not defined
    -- NOTE: No CHECK constraints on status values
);

-- ============================================================================
-- ORDERS TABLE
-- ============================================================================

CREATE TABLE ORDERS (
    order_id INTEGER PRIMARY KEY,
    OrderID INTEGER,  -- Possible duplicate
    customer_id INTEGER,  -- FK reference ambiguous
    CustomerID INTEGER,  -- FK reference ambiguous
    order_date DATE,
    OrderDate DATETIME,  -- Different precision
    order_status VARCHAR(25),
    orderAmount DECIMAL(10,2),  -- camelCase
    total_amount DECIMAL(12,2),  -- snake_case - duplicate?
    shippingAmount DECIMAL(10,2),
    tax_amount DECIMAL(10,2),
    TaxAmount DECIMAL(10,2),  -- Duplicate
    payment_status VARCHAR(20),
    payment_method VARCHAR(30),
    created_at TIMESTAMP,
    updated_at TIMESTAMP,
    notes TEXT,
    Notes TEXT  -- Duplicate
    -- NOTE: FK constraints not enforced (missing REFERENCES clause)
    -- NOTE: No CHECK constraint on order_status values
);

-- ============================================================================
-- ORDER_ITEMS TABLE (also referenced as ORDER_DETAILS in some docs)
-- ============================================================================

CREATE TABLE ORDER_ITEMS (
    order_item_id INTEGER PRIMARY KEY,
    order_id INTEGER,
    product_id INTEGER,  -- References PRODUCTS or INVENTORY?
    ProductID INTEGER,  -- Duplicate with inconsistent naming
    quantity INTEGER,
    unit_price DECIMAL(10,2),
    UnitPrice DECIMAL(10,2),  -- Duplicate
    discount_percent DECIMAL(5,2),
    discount_amount DECIMAL(10,2),
    line_total DECIMAL(12,2),
    LineTotal DECIMAL(12,2)  -- Duplicate
    -- NOTE: FK constraints missing
    -- NOTE: No CHECK on quantity > 0
);

-- ============================================================================
-- PRODUCTS TABLE (also referenced as INVENTORY_ITEMS)
-- ============================================================================

CREATE TABLE PRODUCTS (
    product_id INTEGER PRIMARY KEY,
    ProductID INTEGER,  -- Possible duplicate
    product_name VARCHAR(255),
    ProductName VARCHAR(255),  -- Duplicate
    product_sku VARCHAR(50),
    sku VARCHAR(50),  -- Duplicate, should be UNIQUE?
    product_category VARCHAR(100),
    category VARCHAR(100),  -- Duplicate
    unit_price DECIMAL(10,2),
    current_price DECIMAL(10,2),  -- Different from unit_price?
    cost_price DECIMAL(10,2),
    stock_quantity INTEGER,
    quantity_in_stock INTEGER,  -- Duplicate
    reorder_level INTEGER,
    is_active BOOLEAN,
    active_flag CHAR(1),  -- Duplicate - stores Y/N?
    created_at TIMESTAMP,
    updated_at TIMESTAMP,
    product_description TEXT
    -- NOTE: No UNIQUE constraint on sku
    -- NOTE: No CHECK on stock_quantity >= 0
);

-- ============================================================================
-- PAYMENTS TABLE
-- ============================================================================

CREATE TABLE PAYMENTS (
    payment_id INTEGER PRIMARY KEY,
    PaymentID INTEGER,  -- Possible duplicate
    order_id INTEGER,
    customer_id INTEGER,
    payment_date DATETIME,
    payment_amount DECIMAL(10,2),
    payment_method VARCHAR(30),
    payment_status VARCHAR(20),
    transaction_id VARCHAR(100),
    TransactionID VARCHAR(100),  -- Duplicate
    response_code VARCHAR(50),
    response_message TEXT,
    created_at TIMESTAMP
    -- NOTE: FK constraints missing
    -- NOTE: No UNIQUE constraint on transaction_id
    -- NOTE: No CHECK on payment_status values
);

-- ============================================================================
-- INDEXES (Partial documentation)
-- ============================================================================

-- Some indexes may exist - not fully documented
CREATE INDEX idx_orders_customer_id ON ORDERS(customer_id);
CREATE INDEX idx_orders_customer_id_duplicate ON ORDERS(CustomerID);
CREATE INDEX idx_order_items_order_id ON ORDER_ITEMS(order_id);
CREATE INDEX idx_order_items_product_id ON ORDER_ITEMS(product_id);
CREATE INDEX idx_payments_order_id ON PAYMENTS(order_id);

-- ============================================================================
-- KNOWN INCONSISTENCIES
-- ============================================================================
-- 1. FK constraints defined in data dictionary but not enforced in DDL
-- 2. Mix of snake_case and camelCase naming
-- 3. Duplicate columns with different names
-- 4. Missing NOT NULL constraints
-- 5. Missing CHECK constraints for status columns
-- 6. Missing UNIQUE constraints on natural keys
-- 7. Inconsistent data types (TIMESTAMP vs DATETIME)
-- 8. Table name ambiguity (ORDER_ITEMS vs ORDER_DETAILS)
-- 9. No documentation on which columns are actually used by application
-- 10. Conflicting FK references (customer_id vs CustomerID)
