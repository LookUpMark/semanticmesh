-- ============================================================
-- RETAIL BANKING SCHEMA
-- Domain: Banking & Finance
-- Complexity: Intermediate
-- Tables: 8 (customers, accounts, customer_account, transactions,
--            loans, branches, atms, cards)
-- ============================================================

-- ============================================================
-- DROP TABLES (in correct dependency order)
-- ============================================================
DROP TABLE IF EXISTS cards;
DROP TABLE IF EXISTS transactions;
DROP TABLE IF EXISTS loans;
DROP TABLE IF EXISTS customer_account;
DROP TABLE IF EXISTS accounts;
DROP TABLE IF EXISTS atms;
DROP TABLE IF EXISTS branches;
DROP TABLE IF EXISTS customers;

-- ============================================================
-- TABLE: customers
-- Description: Core customer dimension with KYC and risk profiling
-- ============================================================
CREATE TABLE customers (
    customer_id INTEGER PRIMARY KEY AUTOINCREMENT,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    tax_id VARCHAR(11) NOT NULL UNIQUE,
    email VARCHAR(100) NOT NULL,
    phone VARCHAR(20),
    address VARCHAR(200) NOT NULL,
    city VARCHAR(50) NOT NULL,
    state VARCHAR(2) NOT NULL,
    zip_code VARCHAR(10) NOT NULL,
    kyc_status VARCHAR(20) NOT NULL DEFAULT 'Level1' CHECK (kyc_status IN ('Level1', 'Level2', 'Level3')),
    risk_profile VARCHAR(20) NOT NULL DEFAULT 'Moderate' CHECK (risk_profile IN ('Conservative', 'Moderate', 'Aggressive')),
    customer_since DATE NOT NULL DEFAULT CURRENT_DATE,
    is_preferred BOOLEAN NOT NULL DEFAULT 0,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_customers_tax_id ON customers(tax_id);
CREATE INDEX idx_customers_name ON customers(last_name, first_name);
CREATE INDEX idx_customers_kyc ON customers(kyc_status);

-- ============================================================
-- TABLE: branches
-- Description: Physical bank locations (branches and ATMs)
-- ============================================================
CREATE TABLE branches (
    branch_id INTEGER PRIMARY KEY AUTOINCREMENT,
    branch_code VARCHAR(4) NOT NULL UNIQUE,
    branch_name VARCHAR(100) NOT NULL,
    branch_type VARCHAR(20) NOT NULL CHECK (branch_type IN ('FullService', 'Satellite', 'ATMOnly')),
    address VARCHAR(200) NOT NULL,
    city VARCHAR(50) NOT NULL,
    state VARCHAR(2) NOT NULL,
    zip_code VARCHAR(10) NOT NULL,
    phone VARCHAR(20),
    hours VARCHAR(100),
    atm_count INTEGER NOT NULL DEFAULT 0,
    teller_count INTEGER NOT NULL DEFAULT 0,
    manager_name VARCHAR(100),
    opened_date DATE NOT NULL DEFAULT CURRENT_DATE,
    status VARCHAR(20) NOT NULL DEFAULT 'Active' CHECK (status IN ('Active', 'TemporarilyClosed', 'PermanentlyClosed')),
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_branches_code ON branches(branch_code);
CREATE INDEX idx_branches_type ON branches(branch_type);
CREATE INDEX idx_branches_city ON branches(city, state);

-- ============================================================
-- TABLE: atms
-- Description: ATM locations (standalone and branch ATMs)
-- ============================================================
CREATE TABLE atms (
    atm_id INTEGER PRIMARY KEY AUTOINCREMENT,
    atm_code VARCHAR(10) NOT NULL UNIQUE,
    branch_id INTEGER,
    location VARCHAR(200) NOT NULL,
    latitude DECIMAL(10,6),
    longitude DECIMAL(11,6),
    atm_type VARCHAR(20) NOT NULL CHECK (atm_type IN ('Standalone', 'Branch', 'DriveThrough')),
    status VARCHAR(20) NOT NULL DEFAULT 'Operational' CHECK (status IN ('Operational', 'OutOfService', 'OutOfCash')),
    cash_balance DECIMAL(12,2),
    last_replenished TIMESTAMP,
    supports_deposit BOOLEAN NOT NULL DEFAULT 1,
    supports_cardless BOOLEAN NOT NULL DEFAULT 0,
    installed_date DATE NOT NULL DEFAULT CURRENT_DATE,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (branch_id) REFERENCES branches(branch_id)
);

CREATE INDEX idx_atms_branch ON atms(branch_id);
CREATE INDEX idx_atms_status ON atms(status);
CREATE INDEX idx_atms_location ON atms(location);

-- ============================================================
-- TABLE: accounts
-- Description: Deposit accounts with hierarchy support
-- ============================================================
CREATE TABLE accounts (
    account_id INTEGER PRIMARY KEY AUTOINCREMENT,
    account_number VARCHAR(16) NOT NULL UNIQUE,
    account_type VARCHAR(20) NOT NULL CHECK (account_type IN ('Checking', 'Savings', 'MoneyMarket', 'CD', 'Investment')),
    account_subtype VARCHAR(30),
    parent_account_id INTEGER,
    branch_id INTEGER,
    status VARCHAR(20) NOT NULL DEFAULT 'Active' CHECK (status IN ('Active', 'Dormant', 'Frozen', 'Closed')),
    current_balance DECIMAL(15,2) NOT NULL DEFAULT 0.00,
    available_balance DECIMAL(15,2) NOT NULL DEFAULT 0.00,
    interest_rate DECIMAL(5,4),
    interest_earned DECIMAL(15,2) NOT NULL DEFAULT 0.00,
    minimum_balance DECIMAL(15,2) NOT NULL DEFAULT 0.00,
    monthly_fee DECIMAL(10,2) NOT NULL DEFAULT 0.00,
    opened_date DATE NOT NULL DEFAULT CURRENT_DATE,
    closed_date DATE,
    last_transaction_date TIMESTAMP,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (parent_account_id) REFERENCES accounts(account_id),
    FOREIGN KEY (branch_id) REFERENCES branches(branch_id),
    CHECK (parent_account_id != account_id)
);

CREATE INDEX idx_accounts_type ON accounts(account_type);
CREATE INDEX idx_accounts_status ON accounts(status);
CREATE INDEX idx_accounts_parent ON accounts(parent_account_id);
CREATE INDEX idx_accounts_branch ON accounts(branch_id);
CREATE INDEX idx_accounts_balance ON accounts(current_balance);

-- ============================================================
-- TABLE: customer_account (Junction Table)
-- Description: Many-to-many relationship between customers and accounts
-- ============================================================
CREATE TABLE customer_account (
    customer_id INTEGER NOT NULL,
    account_id INTEGER NOT NULL,
    relationship_type VARCHAR(20) NOT NULL DEFAULT 'Owner' CHECK (relationship_type IN ('Owner', 'JointOwner', 'AuthorizedSigner', 'Custodian')),
    is_primary BOOLEAN NOT NULL DEFAULT 0,
    ownership_percentage DECIMAL(5,2) NOT NULL DEFAULT 100.00,
    linked_date DATE NOT NULL DEFAULT CURRENT_DATE,
    unlinked_date DATE,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (customer_id, account_id),
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id),
    FOREIGN KEY (account_id) REFERENCES accounts(account_id)
);

CREATE INDEX idx_customer_account_customer ON customer_account(customer_id);
CREATE INDEX idx_customer_account_account ON customer_account(account_id);
CREATE INDEX idx_customer_account_role ON customer_account(relationship_type);
CREATE INDEX idx_customer_account_primary ON customer_account(is_primary, customer_id);

-- ============================================================
-- TABLE: transactions
-- Description: Transaction fact table for all account activity
-- ============================================================
CREATE TABLE transactions (
    transaction_id INTEGER PRIMARY KEY AUTOINCREMENT,
    account_id INTEGER NOT NULL,
    transaction_type VARCHAR(20) NOT NULL CHECK (transaction_type IN ('Debit', 'Credit', 'Transfer', 'Payment', 'Withdrawal', 'Deposit', 'Fee')),
    amount DECIMAL(15,2) NOT NULL,
    currency VARCHAR(3) NOT NULL DEFAULT 'USD',
    transaction_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    status VARCHAR(20) NOT NULL DEFAULT 'Pending' CHECK (status IN ('Pending', 'Posted', 'Failed', 'Cancelled', 'OnHold')),
    balance_after DECIMAL(15,2),
    description VARCHAR(200),
    reference_number VARCHAR(50),
    external_account VARCHAR(30),
    location VARCHAR(100),
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (account_id) REFERENCES accounts(account_id)
);

CREATE INDEX idx_transactions_account ON transactions(account_id);
CREATE INDEX idx_transactions_date ON transactions(transaction_date);
CREATE INDEX idx_transactions_type ON transactions(transaction_type);
CREATE INDEX idx_transactions_status ON transactions(status);
CREATE INDEX idx_transactions_account_date ON transactions(account_id, transaction_date DESC);

-- ============================================================
-- TABLE: loans
-- Description: Loan products with amortization tracking
-- ============================================================
CREATE TABLE loans (
    loan_id INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_id INTEGER NOT NULL,
    loan_type VARCHAR(20) NOT NULL CHECK (loan_type IN ('Mortgage', 'Personal', 'Auto', 'HELOC', 'CreditCard')),
    account_id INTEGER,
    principal_amount DECIMAL(15,2) NOT NULL,
    interest_rate DECIMAL(5,4) NOT NULL,
    term_months INTEGER NOT NULL,
    monthly_payment DECIMAL(10,2) NOT NULL,
    balance_due DECIMAL(15,2) NOT NULL,
    origination_date DATE NOT NULL,
    maturity_date DATE NOT NULL,
    status VARCHAR(20) NOT NULL DEFAULT 'Pending' CHECK (status IN ('Pending', 'Approved', 'Active', 'PaidOff', 'Defaulted')),
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id),
    FOREIGN KEY (account_id) REFERENCES accounts(account_id)
);

CREATE INDEX idx_loans_customer ON loans(customer_id);
CREATE INDEX idx_loans_account ON loans(account_id);
CREATE INDEX idx_loans_type ON loans(loan_type);
CREATE INDEX idx_loans_status ON loans(status);
CREATE INDEX idx_loans_maturity ON loans(maturity_date);

-- ============================================================
-- TABLE: cards
-- Description: Debit, credit, and ATM cards
-- ============================================================
CREATE TABLE cards (
    card_id INTEGER PRIMARY KEY AUTOINCREMENT,
    account_id INTEGER NOT NULL,
    customer_id INTEGER NOT NULL,
    card_number VARCHAR(20) NOT NULL UNIQUE,
    card_type VARCHAR(20) NOT NULL CHECK (card_type IN ('Debit', 'Credit', 'ATM')),
    card_network VARCHAR(20) NOT NULL CHECK (card_network IN ('Visa', 'Mastercard', 'Discover', 'AmericanExpress')),
    card_name VARCHAR(50) NOT NULL,
    expiration_date VARCHAR(5) NOT NULL,
    cvv VARCHAR(4) NOT NULL,
    credit_limit DECIMAL(12,2),
    daily_limit DECIMAL(10,2) NOT NULL DEFAULT 3000.00,
    atm_daily_limit DECIMAL(10,2) NOT NULL DEFAULT 500.00,
    pin_set BOOLEAN NOT NULL DEFAULT 0,
    has_chip BOOLEAN NOT NULL DEFAULT 1,
    contactless_enabled BOOLEAN NOT NULL DEFAULT 1,
    status VARCHAR(20) NOT NULL DEFAULT 'Active' CHECK (status IN ('Active', 'Frozen', 'Blocked', 'Expired')),
    issued_date DATE NOT NULL DEFAULT CURRENT_DATE,
    last_used_date TIMESTAMP,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (account_id) REFERENCES accounts(account_id),
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
);

CREATE INDEX idx_cards_account ON cards(account_id);
CREATE INDEX idx_cards_customer ON cards(customer_id);
CREATE INDEX idx_cards_number ON cards(card_number);
CREATE INDEX idx_cards_status ON cards(status);

-- ============================================================
-- SAMPLE DATA: branches
-- ============================================================
INSERT INTO branches (branch_id, branch_code, branch_name, branch_type, address, city, state, zip_code, phone, hours, atm_count, teller_count, manager_name, opened_date, status) VALUES
(1, '0001', 'Downtown Headquarters', 'FullService', '123 Main Street', 'New York', 'NY', '10001', '(212) 555-0001', 'Mon-Fri 9AM-5PM, Sat 9AM-1PM', 4, 5, 'John Davidson', '2010-01-15', 'Active'),
(2, '0002', 'Westside Branch', 'FullService', '456 Oak Avenue', 'Los Angeles', 'CA', '90001', '(310) 555-0002', 'Mon-Fri 9AM-6PM, Sat 9AM-2PM', 2, 3, 'Sarah Mitchell', '2015-03-20', 'Active'),
(3, '0003', 'Northtown Satellite', 'Satellite', '789 Pine Street', 'Chicago', 'IL', '60601', '(312) 555-0003', 'Mon-Fri 10AM-4PM', 1, 2, 'Michael Chen', '2018-07-10', 'Active'),
(4, '0004', 'South Station ATM', 'ATMOnly', '321 Elm Street', 'Houston', 'TX', '77001', NULL, '24/7', 2, 0, NULL, '2020-02-01', 'Active'),
(5, '0005', 'Eastside Branch', 'FullService', '654 Maple Drive', 'Phoenix', 'AZ', '85001', '(602) 555-0005', 'Mon-Fri 9AM-5PM, Sat 10AM-2PM', 3, 4, 'Lisa Rodriguez', '2012-09-15', 'Active');

-- ============================================================
-- SAMPLE DATA: atms
-- ============================================================
INSERT INTO atms (atm_id, atm_code, branch_id, location, latitude, longitude, atm_type, status, cash_balance, last_replenished, supports_deposit, supports_cardless, installed_date) VALUES
(1001, 'ATM-0001', 1, '123 Main Street - Bank Branch 0001', 40.712776, -74.005974, 'Branch', 'Operational', 85000.00, '2024-02-15 02:30:00', 1, 1, '2010-01-15'),
(1002, 'ATM-0002', 1, '123 Main Street - Drive Through', 40.712780, -74.005970, 'DriveThrough', 'Operational', 45000.00, '2024-02-15 02:30:00', 1, 1, '2010-01-15'),
(1003, 'ATM-0003', 2, '456 Oak Avenue - Bank Branch 0002', 34.052235, -118.243683, 'Branch', 'Operational', 62000.00, '2024-02-14 16:00:00', 1, 1, '2015-03-20'),
(1004, 'ATM-0004', 2, '456 Oak Avenue - Walk-up', 34.052230, -118.243680, 'Branch', 'OutOfCash', 0.00, '2024-02-14 08:00:00', 1, 0, '2015-03-20'),
(1005, 'ATM-0005', 3, '789 Pine Street - Bank Branch 0003', 41.878113, -87.629799, 'Branch', 'Operational', 38000.00, '2024-02-15 06:00:00', 1, 1, '2018-07-10'),
(1006, 'STANDALONE-001', NULL, '321 Elm Street - Shopping Mall', 29.760427, -95.369803, 'Standalone', 'Operational', 25000.00, '2024-02-13 14:00:00', 0, 1, '2020-02-01'),
(1007, 'STANDALONE-002', NULL, '987 Birch Road - Grocery Store', 33.448377, -112.074036, 'Standalone', 'OutOfService', 15000.00, '2024-02-12 10:00:00', 0, 0, '2021-06-15');

-- ============================================================
-- SAMPLE DATA: customers
-- ============================================================
INSERT INTO customers (customer_id, first_name, last_name, tax_id, email, phone, address, city, state, zip_code, kyc_status, risk_profile, customer_since, is_preferred) VALUES
(10001, 'James', 'Wilson', '123-45-6789', 'james.wilson@email.com', '(212) 555-1001', '123 Main Street, Apt 4B', 'New York', 'NY', '10001', 'Level2', 'Moderate', '2018-03-15', 1),
(10002, 'Mary', 'Johnson', '234-56-7890', 'mary.johnson@email.com', '(212) 555-1002', '456 Oak Avenue', 'New York', 'NY', '10002', 'Level3', 'Conservative', '2015-07-20', 1),
(10003, 'Robert', 'Chen', '345-67-8901', 'robert.chen@email.com', '(310) 555-2001', '789 Pine Street', 'Los Angeles', 'CA', '90001', 'Level2', 'Aggressive', '2020-01-10', 0),
(10004, 'Patricia', 'Davis', '456-78-9012', 'patricia.davis@email.com', '(312) 555-3001', '321 Elm Street', 'Chicago', 'IL', '60601', 'Level1', 'Moderate', '2021-05-25', 0),
(10005, 'Michael', 'Rodriguez', '567-89-0123', 'michael.rodriguez@email.com', '(602) 555-4001', '654 Maple Drive', 'Phoenix', 'AZ', '85001', 'Level2', 'Moderate', '2019-09-12', 1),
(10006, 'Jennifer', 'Martinez', '678-90-1234', 'jennifer.martinez@email.com', '(713) 555-5001', '987 Birch Road', 'Houston', 'TX', '77001', 'Level1', 'Conservative', '2022-02-18', 0),
(10007, 'David', 'Anderson', '789-01-2345', 'david.anderson@email.com', '(212) 555-1003', '159 Willow Lane', 'New York', 'NY', '10003', 'Level2', 'Aggressive', '2017-11-30', 1),
(10008, 'Linda', 'Thompson', '890-12-3456', 'linda.thompson@email.com', '(310) 555-2002', '753 Cedar Court', 'Los Angeles', 'CA', '90002', 'Level3', 'Moderate', '2016-04-08', 1),
(10009, 'William', ' Harris', '901-23-4567', 'william.harris@email.com', '(312) 555-3002', '357 Oak Street', 'Chicago', 'IL', '60602', 'Level1', 'Conservative', '2023-01-20', 0),
(10010, 'Elizabeth', 'Clark', '012-34-5678', 'elizabeth.clark@email.com', '(602) 555-4002', '951 Aspen Way', 'Phoenix', 'AZ', '85002', 'Level2', 'Moderate', '2014-06-15', 1);

-- ============================================================
-- SAMPLE DATA: accounts (with parent-child hierarchy)
-- ============================================================
INSERT INTO accounts (account_id, account_number, account_type, account_subtype, parent_account_id, branch_id, status, current_balance, available_balance, interest_rate, interest_earned, minimum_balance, monthly_fee, opened_date, last_transaction_date) VALUES
-- Parent accounts (portfolio aggregators)
(50001, 'PORT-001', 'Investment', 'Portfolio', NULL, 1, 'Active', 0.00, 0.00, NULL, 0.00, 0.00, 0.00, '2018-03-15', '2024-02-15 10:30:00'),
(50002, 'PORT-002', 'Investment', 'Portfolio', NULL, 2, 'Active', 0.00, 0.00, NULL, 0.00, 0.00, 0.00, '2020-01-10', '2024-02-14 16:45:00'),

-- Child accounts under PORT-001 (James Wilson)
(50011, 'CHK-001001', 'Checking', 'Premium', 50001, 1, 'Active', 5240.35, 5200.00, NULL, 0.00, 2500.00, 0.00, '2018-03-15', '2024-02-15 10:30:00'),
(50012, 'SAV-001001', 'Savings', 'Standard', 50001, 1, 'Active', 15250.75, 15250.75, 0.0025, 38.12, 100.00, 5.00, '2018-03-15', '2024-02-14 09:00:00'),
(50013, 'CD-001001', 'CD', '12-Month', 50001, 1, 'Active', 50000.00, 50000.00, 0.0450, 2250.00, 1000.00, 0.00, '2023-02-15', '2024-02-01 00:00:00'),

-- Child accounts under PORT-002 (Robert Chen)
(50021, 'CHK-002001', 'Checking', 'Student', 50002, 2, 'Active', 850.50, 830.50, NULL, 0.00, 0.00, 0.00, '2020-01-10', '2024-02-15 08:15:00'),
(50022, 'SAV-002001', 'Savings', 'Standard', 50002, 2, 'Active', 3500.25, 3500.25, 0.0010, 3.50, 100.00, 5.00, '2020-01-10', '2024-02-10 14:30:00'),

-- Standalone accounts (no parent)
(50031, 'CHK-003001', 'Checking', 'Standard', NULL, 1, 'Active', 2150.00, 2100.00, NULL, 0.00, 100.00, 12.00, '2015-07-20', '2024-02-14 11:20:00'),
(50032, 'SAV-003001', 'Savings', 'Premium', NULL, 1, 'Active', 48750.50, 48750.50, 0.0050, 243.75, 2500.00, 0.00, '2015-07-20', '2024-02-15 09:00:00'),
(50033, 'MM-003001', 'MoneyMarket', 'Standard', NULL, 1, 'Active', 25000.00, 25000.00, 0.0075, 187.50, 2500.00, 10.00, '2020-06-15', '2024-02-14 16:00:00'),
(50034, 'CHK-004001', 'Checking', 'Standard', NULL, 3, 'Active', 1750.25, 1700.25, NULL, 0.00, 100.00, 12.00, '2021-05-25', '2024-02-13 15:45:00'),
(50035, 'SAV-004001', 'Savings', 'Standard', NULL, 3, 'Active', 5200.00, 5200.00, 0.0015, 7.80, 100.00, 5.00, '2021-05-25', '2024-02-12 10:00:00'),
(50036, 'CHK-005001', 'Checking', 'Premium', NULL, 5, 'Active', 12500.75, 12450.75, NULL, 0.00, 2500.00, 0.00, '2019-09-12', '2024-02-15 12:30:00'),
(50037, 'SAV-005001', 'Savings', 'Standard', NULL, 5, 'Active', 8350.00, 8350.00, 0.0020, 16.70, 100.00, 5.00, '2019-09-12', '2024-02-14 14:15:00'),
(50038, 'CHK-006001', 'Checking', 'Basic', NULL, 4, 'Active', 525.50, 500.00, NULL, 0.00, 0.00, 5.00, '2022-02-18', '2024-02-15 07:00:00'),
(50039, 'CD-004001', 'CD', '24-Month', NULL, 1, 'Active', 75000.00, 75000.00, 0.0475, 3562.50, 1000.00, 0.00, '2022-03-01', '2024-02-01 00:00:00'),
(50040, 'SAV-006001', 'Savings', 'Standard', NULL, 2, 'Active', 18500.00, 18500.00, 0.0030, 55.50, 100.00, 5.00, '2023-01-20', '2024-02-13 11:00:00');

-- ============================================================
-- SAMPLE DATA: customer_account (Junction Table)
-- ============================================================
INSERT INTO customer_account (customer_id, account_id, relationship_type, is_primary, ownership_percentage, linked_date) VALUES
-- James Wilson accounts (primary owner)
(10001, 50001, 'Owner', 1, 100.00, '2018-03-15'),
(10001, 50011, 'Owner', 1, 100.00, '2018-03-15'),
(10001, 50012, 'Owner', 1, 100.00, '2018-03-15'),
(10001, 50013, 'Owner', 1, 100.00, '2023-02-15'),

-- Mary Johnson accounts
(10002, 50031, 'Owner', 1, 100.00, '2015-07-20'),
(10002, 50032, 'Owner', 1, 100.00, '2015-07-20'),
(10002, 50033, 'Owner', 1, 100.00, '2020-06-15'),
(10002, 50039, 'Owner', 1, 100.00, '2022-03-01'),

-- Robert Chen accounts (primary owner)
(10003, 50002, 'Owner', 1, 100.00, '2020-01-10'),
(10003, 50021, 'Owner', 1, 100.00, '2020-01-10'),
(10003, 50022, 'Owner', 1, 100.00, '2020-01-10'),
(10003, 50040, 'JointOwner', 0, 50.00, '2023-01-20'),

-- Patricia Davis accounts
(10004, 50034, 'Owner', 1, 100.00, '2021-05-25'),
(10004, 50035, 'Owner', 1, 100.00, '2021-05-25'),

-- Michael Rodriguez accounts
(10005, 50036, 'Owner', 1, 100.00, '2019-09-12'),
(10005, 50037, 'Owner', 1, 100.00, '2019-09-12'),

-- Jennifer Martinez account
(10006, 50038, 'Owner', 1, 100.00, '2022-02-18'),

-- David Anderson accounts
(10007, 50031, 'JointOwner', 0, 50.00, '2017-11-30'),
(10007, 50032, 'JointOwner', 0, 50.00, '2017-11-30'),

-- Linda Thompson accounts
(10008, 50021, 'JointOwner', 0, 50.00, '2020-01-10'),
(10008, 50022, 'JointOwner', 0, 50.00, '2020-01-10'),

-- William Harris joint ownership with Linda
(10009, 50040, 'Owner', 1, 50.00, '2023-01-20'),

-- Elizabeth Clark accounts
(10010, 50036, 'JointOwner', 0, 50.00, '2014-06-15'),
(10010, 50037, 'JointOwner', 0, 50.00, '2014-06-15');

-- ============================================================
-- SAMPLE DATA: transactions
-- ============================================================
INSERT INTO transactions (transaction_id, account_id, transaction_type, amount, transaction_date, status, balance_after, description, reference_number, external_account, location) VALUES
-- Checking account transactions
(900001, 50011, 'Debit', 85.50, '2024-02-15 10:30:00', 'Posted', 5154.85, 'POS DEBIT - WHOLE FOODS MARKET #1234', NULL, 'XXXX-XXXX-XXXX-3456', 'WHOLE FOODS MARKET #1234 - NEW YORK, NY'),
(900002, 50011, 'Credit', 2500.00, '2024-02-15 09:00:00', 'Posted', 5240.35, 'ACH - PAYROLL DIRECT DEPOSIT', 'ACH123456789', NULL, NULL),
(900003, 50011, 'Debit', 1200.00, '2024-02-14 16:00:00', 'Posted', 2740.35, 'ONLINE BILL PAY - CON EDISON', 'PAY-987654321', NULL, NULL),
(900004, 50021, 'Debit', 45.25, '2024-02-15 08:15:00', 'Posted', 805.25, 'POS DEBIT - STARBUCKS COFFEE', NULL, 'XXXX-XXXX-XXXX-7890', 'STARBUCKS COFFEE - LOS ANGELES, CA'),
(900005, 50021, 'Withdrawal', 100.00, '2024-02-14 14:30:00', 'Posted', 850.50, 'ATM WITHDRAWAL - ATM-0003', NULL, NULL, '456 Oak Avenue - Bank Branch 0002'),
(900006, 50031, 'Debit', 250.00, '2024-02-14 11:20:00', 'Posted', 1900.00, 'CHECK #1001 - RENT PAYMENT', 'CHECK-0001001', NULL, NULL),
(900007, 50031, 'Credit', 500.00, '2024-02-13 10:00:00', 'Posted', 2150.00, 'TRANSFER FROM SAVINGS SAV-003001', NULL, 'SAV-003001', NULL),
(900008, 50034, 'Debit', 75.50, '2024-02-13 15:45:00', 'Posted', 1675.75, 'POS DEBIT - TARGET STORE #4567', NULL, 'XXXX-XXXX-XXXX-2345', 'TARGET STORE #4567 - CHICAGO, IL'),
(900009, 50034, 'Credit', 1500.00, '2024-02-12 09:30:00', 'Posted', 1751.25, 'MOBILE CHECK DEPOSIT - APP DEPOSIT', 'MOB-987654321', NULL, NULL),
(900010, 50036, 'Debit', 850.00, '2024-02-15 12:30:00', 'Posted', 11650.75, 'POS DEBIT - APPLE STORE', NULL, 'XXXX-XXXX-XXXX-9876', 'APPLE STORE - PHOENIX, AZ'),
(900011, 50036, 'Credit', 3200.00, '2024-02-14 16:00:00', 'Posted', 12500.75, 'ACH - TAX REFUND DIRECT DEPOSIT', 'ACH987654321', NULL, NULL),
(900012, 50036, 'Debit', 150.00, '2024-02-13 11:00:00', 'Posted', 9300.75, 'TELLER WITHDRAWAL - BRANCH 0005', NULL, NULL, '654 Maple Drive - PHOENIX, AZ'),
(900013, 50038, 'Withdrawal', 200.00, '2024-02-15 07:00:00', 'Posted', 325.50, 'ATM WITHDRAWAL - STANDALONE-001', NULL, NULL, '321 Elm Street - Shopping Mall'),
(900014, 50038, 'Credit', 400.00, '2024-02-14 08:30:00', 'Posted', 525.50, 'ACH - FREELANCE INCOME', 'ACH456789123', NULL, NULL),
(900015, 50038, 'Debit', 25.00, '2024-02-13 15:00:00', 'Failed', 525.50, 'POS DEBIT - INSUFFICIENT FUNDS', NULL, 'XXXX-XXXX-XXXX-5432', 'GAS STATION - HOUSTON, TX'),

-- Savings account transactions (interest credits)
(900016, 50012, 'Credit', 38.12, '2024-02-01 00:00:00', 'Posted', 15250.75, 'INTEREST CREDIT - JANUARY 2024', NULL, NULL, NULL),
(900017, 50022, 'Credit', 3.50, '2024-02-01 00:00:00', 'Posted', 3500.25, 'INTEREST CREDIT - JANUARY 2024', NULL, NULL, NULL),
(900018, 50032, 'Credit', 243.75, '2024-02-01 00:00:00', 'Posted', 48750.50, 'INTEREST CREDIT - JANUARY 2024', NULL, NULL, NULL),
(900019, 50035, 'Credit', 7.80, '2024-02-01 00:00:00', 'Posted', 5200.00, 'INTEREST CREDIT - JANUARY 2024', NULL, NULL, NULL),
(900020, 50037, 'Credit', 16.70, '2024-02-01 00:00:00', 'Posted', 8350.00, 'INTEREST CREDIT - JANUARY 2024', NULL, NULL, NULL),

-- Transfer between accounts
(900021, 50032, 'Debit', 500.00, '2024-02-13 09:00:00', 'Posted', 48250.50, 'TRANSFER TO CHECKING CHK-003001', NULL, 'CHK-003001', NULL),

-- Fees
(900022, 50034, 'Debit', 12.00, '2024-01-31 23:59:59', 'Posted', 1751.25, 'MONTHLY MAINTENANCE FEE - JANUARY 2024', NULL, NULL, NULL),
(900023, 50035, 'Debit', 5.00, '2024-01-31 23:59:59', 'Posted', 5192.20, 'MONTHLY MAINTENANCE FEE - JANUARY 2024', NULL, NULL, NULL),
(900024, 50038, 'Debit', 5.00, '2024-01-31 23:59:59', 'Posted', 125.50, 'MONTHLY MAINTENANCE FEE - JANUARY 2024', NULL, NULL, NULL);

-- ============================================================
-- SAMPLE DATA: loans
-- ============================================================
INSERT INTO loans (loan_id, customer_id, loan_type, account_id, principal_amount, interest_rate, term_months, monthly_payment, balance_due, origination_date, maturity_date, status) VALUES
(70001, 10002, 'Mortgage', 50031, 350000.00, 0.0550, 360, 1987.57, 345250.00, '2020-03-15', '2055-03-15', 'Active'),
(70002, 10001, 'Personal', 50011, 15000.00, 0.0850, 48, 368.22, 8200.50, '2023-06-01', '2027-06-01', 'Active'),
(70003, 10005, 'Auto', 50036, 35000.00, 0.0650, 60, 684.57, 28000.00, '2022-08-15', '2027-08-15', 'Active'),
(70004, 10007, 'HELOC', 50032, 50000.00, 0.0850, 240, 450.00, 48000.00, '2021-04-01', '2041-04-01', 'Active'),
(70005, 10003, 'Personal', 50021, 8000.00, 0.0950, 36, 257.50, 3200.00, '2023-11-15', '2026-11-15', 'Active'),
(70006, 10010, 'Mortgage', 50036, 425000.00, 0.0600, 360, 2547.72, 418750.00, '2019-05-20', '2054-05-20', 'Active'),
(70007, 10004, 'Auto', 50034, 28000.00, 0.0700, 72, 478.92, 24500.00, '2023-02-10', '2029-02-10', 'Active'),
(70008, 10008, 'CreditCard', 50022, 10000.00, 0.1850, 0, 250.00, 7500.00, '2022-09-01', '2027-09-01', 'Active'),
(70009, 10002, 'Personal', NULL, 25000.00, 0.0750, 60, 500.48, 0.00, '2020-01-15', '2025-01-15', 'PaidOff'),
(70010, 10006, 'Personal', 50038, 5000.00, 0.1200, 24, 235.37, 4200.00, '2024-01-05', '2026-01-05', 'Active');

-- ============================================================
-- SAMPLE DATA: cards
-- ============================================================
INSERT INTO cards (card_id, account_id, customer_id, card_number, card_type, card_network, card_name, expiration_date, cvv, credit_limit, daily_limit, atm_daily_limit, pin_set, has_chip, contactless_enabled, status, issued_date, last_used_date) VALUES
-- Debit cards
(300001, 50011, 10001, '4532015112830366', 'Debit', 'Visa', 'JAMES WILSON', '12/25', '123', NULL, 3000.00, 500.00, 1, 1, 1, 'Active', '2023-12-01', '2024-02-15 10:30:00'),
(300002, 50021, 10003, '5425233430109903', 'Debit', 'Mastercard', 'ROBERT CHEN', '06/26', '789', NULL, 3000.00, 500.00, 1, 1, 1, 'Active', '2023-06-01', '2024-02-15 08:15:00'),
(300003, 50031, 10002, '4532015112840517', 'Debit', 'Visa', 'MARY JOHNSON', '09/25', '456', NULL, 5000.00, 1000.00, 1, 1, 1, 'Active', '2022-09-01', '2024-02-14 11:20:00'),
(300004, 50031, 10007, '5425233430111011', 'Debit', 'Mastercard', 'DAVID ANDERSON', '09/25', '234', NULL, 5000.00, 1000.00, 1, 1, 1, 'Active', '2022-09-01', '2024-02-10 14:30:00'),
(300005, 50034, 10004, '4532015112850628', 'Debit', 'Visa', 'PATRICIA DAVIS', '03/26', '567', NULL, 3000.00, 500.00, 1, 1, 1, 'Active', '2024-01-15', '2024-02-13 15:45:00'),
(300006, 50036, 10005, '5425233430112125', 'Debit', 'Mastercard', 'MICHAEL RODRIGUEZ', '11/25', '890', NULL, 5000.00, 2000.00, 1, 1, 1, 'Active', '2023-11-01', '2024-02-15 12:30:00'),
(300007, 50036, 10010, '5425233430113139', 'Debit', 'Mastercard', 'ELIZABETH CLARK', '11/25', '321', NULL, 5000.00, 2000.00, 1, 1, 1, 'Active', '2023-11-01', '2024-02-14 16:00:00'),
(300008, 50038, 10006, '4532015112860739', 'Debit', 'Visa', 'JENNIFER MARTINEZ', '07/26', '234', NULL, 2000.00, 400.00, 1, 1, 1, 'Active', '2024-02-01', '2024-02-15 07:00:00'),

-- ATM card (no point-of-sale)
(300009, 50022, 10003, '6011023430109903', 'ATM', 'Visa', 'ROBERT CHEN', '06/26', '789', NULL, 0.00, 500.00, 1, 0, 0, 'Active', '2023-06-01', '2024-02-14 14:30:00'),

-- Credit cards
(300010, 50032, 10002, '4532015112870840', 'Credit', 'Visa', 'MARY JOHNSON', '01/27', '567', 25000.00, 5000.00, 500.00, 1, 1, 1, 'Active', '2024-01-15', '2024-02-13 10:00:00'),
(300011, 50032, 10007, '5425233430114242', 'Credit', 'Mastercard', 'DAVID ANDERSON', '02/27', '890', 15000.00, 3000.00, 500.00, 1, 1, 1, 'Active', '2024-01-15', '2024-02-12 15:30:00'),
(300012, 50022, 10008, '3742453430115356', 'Credit', 'AmericanExpress', 'LINDA THOMPSON', '05/26', '1234', 10000.00, 3000.00, 500.00, 1, 1, 1, 'Active', '2023-05-01', '2024-02-10 09:45:00');

-- ============================================================
-- END OF SCHEMA
-- ============================================================
