# CustomerMaster E-Commerce System - Business Glossary

## Document Overview
**System**: CustomerMaster v3.2.1 (Legacy)
**Last Updated**: March 2015
**Purpose**: Business terminology definitions for data migration project
**Target System**: New ERP Platform (Migration Q4 2015)

---

## Core Business Entities

### Customer
**Definition**: An individual or organization that has purchased products or services from the company. Customers are stored in the `tblCustomer` table with legacy identifiers inherited from the AS/400 system.

**Business Rules**:
- A customer must have a unique customer code (strCustID)
- Customers can be marked as inactive (bolActive = 0) but are never deleted
- Email addresses are optional but strongly recommended for order notifications
- Customer region determines sales territory assignment and tax calculation

**Related Terms**: Client, Account, Buyer

**Data Migration Notes**: The new system will use integer customer IDs (cust_id) instead of alphanumeric strCustID codes. A mapping table will be maintained during the transition period.

---

### Order (Sales Order)
**Definition**: A commercial transaction request from a customer for one or more products. Orders represent the legal commitment to purchase and are stored in `vw_SalesOrderHdr` (despite the "vw_" prefix, this is a table, not a view).

**Business Rules**:
- Orders must have a valid customer reference
- Orders move through statuses: PENDING → SHIPPED (or CANCELLED)
- Order totals are calculated from line items plus tax
- Once shipped, orders cannot be cancelled (must process return instead)

**Related Terms**: Purchase Order, Sales Transaction, Customer Order

**Data Migration Notes**: The `lngOrderID` uses long integer format. The new system will continue using integer order IDs but may change the prefix convention.

---

### Product (SKU)
**Definition**: A sellable item in the company's catalog. Products are identified by SKU (Stock Keeping Unit) and stored in `tblProduct`.

**Business Rules**:
- Every product must have a unique SKU code
- SKUs follow the format: Category-Color-Size (e.g., SHIRT-BLU-L)
- Products can be discontinued but remain in the system for historical orders
- Prices can change over time; order line items snapshot the price at time of sale

**Related Terms**: Item, SKU, Merchandise, Inventory Item

**Data Migration Notes**: Legacy system has both `strSKU` and deprecated `prod_num` fields. Only `strSKU` should be used for migration.

---

### Line Item
**Definition**: An individual product within an order, specifying quantity and price. Stored in `ord_line_item` table.

**Business Rules**:
- Each line item references exactly one product
- Each line item belongs to exactly one order
- Line items have independent status (can be backordered while others ship)
- Amount is calculated as quantity × unit price at time of order

**Related Terms**: Order Line, Order Detail, Cart Item

**Data Migration Notes**: The `ord_line_item` table contains redundant copies of product data (`product_code`, `item_name`) for historical accuracy. These should NOT be updated from the product master.

---

### Inventory Transaction
**Definition**: A record of stock quantity changes for audit purposes. Stored in `inv_txn_log` table.

**Business Rules**:
- All stock movements must be logged
- Transaction types: IN (receipts), OUT (shipments), ADJ (corrections)
- Inventory quantity is the sum of all IN transactions minus all OUT transactions
- Manual adjustments require supervisor approval

**Related Terms**: Stock Movement, Inventory Adjustment, Warehouse Transaction

**Data Migration Notes**: The `inv_txn_log` table uses abbreviated field names (txn_id, txn_dt). New system should use full names for clarity.

---

## Domain-Specific Terminology

### Backorder
**Definition**: A situation where a customer orders a product that is out of stock. The order is accepted, but the line item is marked as BACKORDERED until inventory arrives.

**Business Impact**: Backorders are allowed even with negative stock quantities. This is intentional to support pre-orders and special orders.

---

### Fulfillment
**Definition**: The process of picking, packing, and shipping orders to customers. Managed by the warehouse team.

**Metrics**: Orders are typically fulfilled within 1-2 business days. Priority given to orders with earlier `dtmRequiredDate`.

---

### Shipping Carrier
**Definition**: Third-party logistics provider responsible for delivering packages to customers. Stored in `tblShippingCarrier`.

**Active Carriers**: UPS, FedEx, USPS

**Business Rules**: Only active carriers (bolActive = 1) should be offered to customers during checkout.

---

### Payment Authorization
**Definition**: The process of verifying that a customer's payment method is valid and has sufficient funds. Successful authorizations receive an authorization code from the payment gateway.

**Security Note**: The legacy system stores full card numbers in `CardNumberText` field. This is a PCI compliance violation and must be addressed in the migration.

---

## Status Workflows

### Order Status (strOrderStatus)
| Status | Description | Business Meaning |
|--------|-------------|------------------|
| PENDING | Order received but not yet shipped | Awaiting fulfillment |
| SHIPPED | Order has been shipped to customer | In transit |
| CANCELLED | Order cancelled before shipping | No longer valid |

**Transitions**:
- PENDING → SHIPPED (normal flow)
- PENDING → CANCELLED (customer request or fraud check)
- SHIPPED → (no transitions, final state)

### Line Item Status (line_status)
| Status | Description | Business Meaning |
|--------|-------------|------------------|
| PENDING | Not yet picked from warehouse | Awaiting fulfillment |
| PICKED | Picked but not yet shipped | Staged for shipping |
| SHIPPED | Included in shipment | Delivered to customer |
| BACKORDERED | Awaiting inventory | Will ship when available |

**Note**: Line items can have different statuses within the same order.

### Payment Status (PaymentStatus)
| Status | Description | Business Meaning |
|--------|-------------|------------------|
| PENDING | Authorization initiated but not completed | Awaiting confirmation |
| COMPLETED | Payment successfully captured | Funds received |
| FAILED | Authorization declined or error | Payment did not succeed |
| REFUNDED | Payment returned to customer | After return/cancellation |

---

## Legacy System Quirks

### Hungarian Notation
The legacy system uses Hungarian notation prefixes:
- `str` = string (VARCHAR)
- `int` = integer (INT)
- `lng` = long integer (INT)
- `flt` = float/money (DECIMAL)
- `bol` = boolean (BIT)
- `dtm` = datetime (DATETIME)

**Migration Note**: These prefixes are inconsistent. For example, `intCustID` is actually a VARCHAR, and `lngOrderID` is a regular INT.

### Table Naming Inconsistency
Different parts of the system use different naming conventions:
- `tbl` prefix: tblCustomer, tblProduct, tblPayment
- `vw_` prefix (but actually tables): vw_SalesOrderHdr
- `ord_` prefix: ord_line_item
- `inv_` prefix: inv_txn_log
- No prefix: Group, User (reserved words!)

### Reserved Words as Names
Several tables use SQL reserved words as names:
- `Group` (product categories) - must be quoted as `[Group]`
- `User` (system users) - must be quoted as `[User]`

### Data Type Issues
- `tblProduct.unit_cost` is VARCHAR(20) instead of DECIMAL - contains "$" symbols
- `tblCustomer.strCustID` is VARCHAR(50) instead of INT - legacy AS/400 codes
- Foreign keys mix data types (intCustID is VARCHAR referencing strCustID)

### Abbreviated Names
Reports and queries use abbreviated column names:
- `cust_nm` → Customer Name (strFullName)
- `ord_dt` → Order Date (dtmOrderDate)
- `prod_desc` → Product Description (strDescription)
- `ship_meth` → Shipping Method (strShippingMethod)

These abbreviations are NOT in the schema but appear in ad-hoc queries and reports.

---

## Cross-Reference Tables

### Customer → Orders
**Relationship**: One-to-Many
**Foreign Key**: `vw_SalesOrderHdr.intCustID` → `tblCustomer.strCustID`
**Business Rule**: A customer can have many orders over time

### Order → Line Items
**Relationship**: One-to-Many
**Foreign Key**: `ord_line_item.ord_id` → `vw_SalesOrderHdr.lngOrderID`
**Business Rule**: An order must have at least one line item

### Product → Line Items
**Relationship**: One-to-Many
**Foreign Key**: `ord_line_item.prod_id` → `tblProduct.intProdID`
**Business Rule**: A product can appear in many orders over time

### Product → Inventory Transactions
**Relationship**: One-to-Many
**Foreign Key**: `inv_txn_log.prod_id` → `tblProduct.intProdID`
**Business Rule**: All stock movements are logged against products

### Group → Group (Hierarchy)
**Relationship**: Self-referencing One-to-Many
**Foreign Key**: `Group.ParentGroupID` → `Group.GroupID`
**Business Rule**: Product categories form a tree structure

### Order → Payments
**Relationship**: One-to-One (typically)
**Foreign Key**: `tblPayment.OrderID` → `vw_SalesOrderHdr.lngOrderID`
**Business Rule**: Most orders have one payment, but refunds create additional payment records

### Order → Status History
**Relationship**: One-to-Many
**Foreign Key**: `tblOrderStatusHistory.OrderID` → `vw_SalesOrderHdr.lngOrderID`
**Business Rule**: Every status change creates a history record

---

## Migration Priority Guidelines

### Critical Path (Must Migrate First)
1. **tblCustomer** - Required for all orders
2. **tblProduct** - Required for line items and inventory
3. **vw_SalesOrderHdr** - Core transactional data
4. **ord_line_item** - Order details

### Secondary (Can Migrate in Parallel)
5. **inv_txn_log** - Inventory audit trail
6. **tblPayment** - Payment records
7. **tblOrderStatusHistory** - Order status audit

### Low Priority (Migrate Last)
8. **tblShippingCarrier** - Reference data, can be manually recreated
9. **Group** - Product categories, can be reorganized
10. **User** - System users, can be recreated in new system

---

## Data Quality Issues Identified

### Referential Integrity Gaps
- Some `ord_line_item.prod_id` values reference non-existent products (deleted products)
- Some orders reference customers marked as inactive
- No foreign key constraint on `inv_txn_log.user_id`

### Data Inconsistencies
- `tblProduct` has both active and discontinued products with the same SKU pattern
- Some `vw_SalesOrderHdr` records have `fltTotalAmount = 0` (likely failed calculations)
- `tblPayment.CardNumberText` contains both full numbers and tokens (inconsistent)

### Security and Compliance
- **CRITICAL**: `tblPayment.CardNumberText` stores unencrypted card numbers
- **CRITICAL**: `User.PasswordHash` uses SHA-256 without salt (vulnerable to rainbow tables)
- Payment data lacks PCI-DSS required fields (tokenization, encryption at rest)

### Performance Issues
- No indexes on frequently queried fields (customer email, order date range)
- TEXT fields used for variable-length data (should use VARCHAR(MAX))
- Denormalized fields in `ord_line_item` create update overhead

---

## Glossary Maintenance

**Owner**: Data Migration Team
**Review Frequency**: Weekly during migration project
**Change Process**: Submit glossary update request to migration lead for approval

**Last Review**: March 15, 2015
**Next Review**: March 22, 2015
