-- Legacy E-commerce Schema Migration
-- Source: CustomerMaster database (c. 2008)
-- Notes: Hungarian notation, mixed case, reserved words, inappropriate types

-- Customer master table with legacy naming
CREATE TABLE tblCustomer (
    strCustID VARCHAR(50) NOT NULL PRIMARY KEY,
    strFullName VARCHAR(255) NOT NULL,
    strEmail VARCHAR(150),
    strRegion VARCHAR(100),
    strCountry VARCHAR(100),
    dtmCreated DATETIME,
    dtmLastModified DATETIME,
    bolActive BIT DEFAULT 1,
    -- Migration compatibility columns (old vs new)
    cust_id INT NULL,  -- New integer ID (future migration)
    customer_name VARCHAR(255) NULL,  -- New naming convention
    txtNotes TEXT NULL
);

-- Product catalog with mixed conventions
CREATE TABLE tblProduct (
    intProdID INT NOT NULL PRIMARY KEY,
    strSKU VARCHAR(50) NOT NULL UNIQUE,
    strName VARCHAR(255) NOT NULL,
    strDescription TEXT,
    fltPrice DECIMAL(10,2) NOT NULL,
    intStockQty INT DEFAULT 0,
    bolActive BIT DEFAULT 1,
    strCategory VARCHAR(100),
    strBrand VARCHAR(100),
    dtmIntroduced DATETIME,
    dtmDiscontinued DATETIME NULL,
    -- Legacy columns (deprecated but present)
    prod_num VARCHAR(20) NULL,
    item_desc VARCHAR(500) NULL,
    unit_cost VARCHAR(20) NULL  -- Wrong type!
);

-- Sales order header - VIEW treated as table
CREATE TABLE vw_SalesOrderHdr (
    lngOrderID INT NOT NULL PRIMARY KEY,
    intCustID VARCHAR(50) NOT NULL,
    dtmOrderDate DATETIME NOT NULL,
    dtmShipDate DATETIME,
    dtmRequiredDate DATETIME,
    strOrderStatus VARCHAR(20) CHECK (strOrderStatus IN ('PENDING', 'SHIPPED', 'CANCELLED')),
    fltSubTotal DECIMAL(12,2),
    fltTaxAmount DECIMAL(12,2),
    fltTotalAmount DECIMAL(12,2),
    strShippingMethod VARCHAR(50),
    strTrackingNumber VARCHAR(100),
    -- FK constraint would go here in modern schema
    FOREIGN KEY (intCustID) REFERENCES tblCustomer(strCustID)
);

-- Order line items - snake_case but inconsistent
CREATE TABLE ord_line_item (
    line_id INT NOT NULL PRIMARY KEY,
    ord_id INT NOT NULL,
    prod_id INT NOT NULL,
    qty INT DEFAULT 1,
    amt DECIMAL(10,2) NOT NULL,
    disc_amt DECIMAL(10,2) DEFAULT 0,
    line_status VARCHAR(20),
    -- Inconsistent naming convention
    product_code VARCHAR(50) NULL,
    item_name VARCHAR(255) NULL,
    FOREIGN KEY (ord_id) REFERENCES vw_SalesOrderHdr(lngOrderID),
    FOREIGN KEY (prod_id) REFERENCES tblProduct(intProdID)
);

-- Inventory transaction log - abbreviated names
CREATE TABLE inv_txn_log (
    txn_id INT NOT NULL PRIMARY KEY,
    prod_id INT NOT NULL,
    txn_type VARCHAR(10) CHECK (txn_type IN ('IN', 'OUT', 'ADJ')),
    qty INT NOT NULL,
    txn_dt DATETIME DEFAULT GETDATE(),
    ref_num VARCHAR(50),
    user_id VARCHAR(50),
    notes TEXT NULL,
    FOREIGN KEY (prod_id) REFERENCES tblProduct(intProdID)
);

-- Category/Group table - reserved word issues
CREATE TABLE [Group] (
    GroupID INT NOT NULL PRIMARY KEY,
    GroupName VARCHAR(100) NOT NULL,
    ParentGroupID INT NULL,
    Description VARCHAR(500),
    IsActive BIT DEFAULT 1,
    FOREIGN KEY (ParentGroupID) REFERENCES [Group](GroupID)
);

-- User table - reserved word, mixed case
CREATE TABLE [User] (
    UserID INT NOT NULL PRIMARY KEY,
    UserName VARCHAR(100) NOT NULL UNIQUE,
    PasswordHash VARCHAR(255) NOT NULL,
    UserRole VARCHAR(50) CHECK (UserRole IN ('ADMIN', 'MANAGER', 'CLERK')),
    Email VARCHAR(150),
    LastLogin DATETIME,
    CreatedDate DATETIME DEFAULT GETDATE()
);

-- Order status history - verbose naming
CREATE TABLE tblOrderStatusHistory (
    HistoryID INT NOT NULL PRIMARY KEY,
    OrderID INT NOT NULL,
    OldStatus VARCHAR(20),
    NewStatus VARCHAR(20) NOT NULL,
    ChangedByUser VARCHAR(100),
    ChangedDate DATETIME DEFAULT GETDATE(),
    ChangeReason TEXT NULL,
    FOREIGN KEY (OrderID) REFERENCES vw_SalesOrderHdr(lngOrderID)
);

-- Shipping carrier table
CREATE TABLE tblShippingCarrier (
    CarrierID INT NOT NULL PRIMARY KEY,
    CarrierName VARCHAR(100) NOT NULL,
    CarrierCode VARCHAR(20) NOT NULL UNIQUE,
    TrackingURL VARCHAR(500),
    bolActive BIT DEFAULT 1
);

-- Payment information - security concerns with types
CREATE TABLE tblPayment (
    PaymentID INT NOT NULL PRIMARY KEY,
    OrderID INT NOT NULL,
    PaymentMethod VARCHAR(50) CHECK (PaymentMethod IN ('CREDIT_CARD', 'DEBIT', 'PAYPAL', 'BANK_TRANSFER')),
    PaymentDate DATETIME NOT NULL,
    Amount DECIMAL(12,2) NOT NULL,
    PaymentStatus VARCHAR(20) CHECK (PaymentStatus IN ('PENDING', 'COMPLETED', 'FAILED', 'REFUNDED')),
    -- Security issue: storing sensitive data as text
    CardNumberText VARCHAR(100) NULL,
    CardHolderName VARCHAR(100) NULL,
    AuthorizationCode VARCHAR(50),
    FOREIGN KEY (OrderID) REFERENCES vw_SalesOrderHdr(lngOrderID)
);

-- Create indexes for performance (typical legacy approach)
CREATE INDEX idx_cust_email ON tblCustomer(strEmail);
CREATE INDEX idx_cust_region ON tblCustomer(strRegion);
CREATE INDEX idx_prod_sku ON tblProduct(strSKU);
CREATE INDEX idx_prod_category ON tblProduct(strCategory);
CREATE INDEX idx_order_cust ON vw_SalesOrderHdr(intCustID);
CREATE INDEX idx_order_date ON vw_SalesOrderHdr(dtmOrderDate);
CREATE INDEX idx_line_order ON ord_line_item(ord_id);
CREATE INDEX idx_line_prod ON ord_line_item(prod_id);
CREATE INDEX idx_inv_prod ON inv_txn_log(prod_id);
CREATE INDEX idx_inv_date ON inv_txn_log(txn_dt);
