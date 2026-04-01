# AB-09 — 06_edgecases_legacy — Run Analysis

**Timestamp:** 2026-03-31 22:39:46  
**Run tag:** `v5`

## Configuration

| Parameter | Value |
|-----------|-------|
| Extraction model | `LLM (gpt-5.4-nano-2026-03-17)` |
| Reasoning model | `gpt-5.4-2026-03-05` |
| Embedding model | `BAAI/bge-m3` |
| Retrieval mode | `hybrid` |
| Reranker | `True` |
| Reranker top_k | `12` |
| Chunk size / overlap | `256 / 32` |
| ER similarity threshold | `0.75` |

## Builder Results

| Metric | Value |
|--------|-------|
| Triplets extracted | 332 |
| Entities resolved | 213 |
| Tables parsed | 10 |
| Tables completed | 10 |

## Query Evaluation Summary

| Metric | Value |
|--------|-------|
| Questions | 25 |
| Grounded | **25/25 (100%)** |
| Avg GT Coverage | 100% |
| Avg Top Score | 0.6459 |
| Avg Chunk Count | 12.0 |
| Abstained | 0 |

## RAGAS Metrics

RAGAS evaluation not enabled for this run.

## Per-Question Deep Dive

### ✅ 1 — What is the purpose of the tblCustomer table?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.9921 | **Gate:** `proceed`

**Expected answer:**
> The tblCustomer table stores customer master data including customer codes, names, email addresses, and region information. It uses Hungarian notation with the str prefix for string fields and contains both legacy fields (strCustID, strFullName) and new migration compatibility fields (cust_id, custo…

**System answer:**
> The `tblCustomer` table stores customer master data from the legacy CRM system. It is the physical implementation of the business concept “Customer Master” / “Customer,” and contains core customer attributes including customer ID, full name, email, region, country, active flag, notes, and audit timestamps such as created and last modified dates.

The context also states that customers in this tabl…

**Sources retrieved (12):** `parent_chunk_data_dictionary.txt_4`, `parent_chunk_business_glossary.md_0`, `Customer Master→TBLCUSTOMER`, `parent_chunk_data_dictionary.txt_5`, `parent_chunk_business_glossary.md_3`, `parent_chunk_data_dictionary.txt_7`, `VW_SALESORDERHDR→TBLCUSTOMER`, `parent_chunk_business_glossary.md_2`

**Context previews (first 3):**

1. _================================================================================ CUSTOMERMASTER DATABASE - DATA DICTIONARY =============================================================================…_

2. _# CustomerMaster E-Commerce System - Business Glossary  ## Document Overview **System**: CustomerMaster v3.2.1 (Legacy) **Last Updated**: March 2015 **Purpose**: Business terminology definitions for d…_

3. _Business concept 'Customer Master' — The table contains core customer master attributes such as customer ID, full name, email, region, country, active flag, and audit timestamps, indicating it physica…_

---

### ✅ 2 — How are customers identified in the legacy system?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.8295 | **Gate:** `proceed`

**Expected answer:**
> Customers are identified by strCustID, which is a VARCHAR(50) field containing alphanumeric customer codes inherited from an AS/400 system. These codes follow formats like C-XXXXX or REG-XXXX and can contain letters, numbers, and hyphens.

**System answer:**
> In the legacy CustomerMaster system, customers are identified primarily by `tblCustomer.strCustID`. This is the primary key for `tblCustomer` and is described as an alphanumeric customer code inherited from the AS/400 system. It is a `VARCHAR(50)`, `NOT NULL`, and `UNIQUE`, and its documented formats are `C-XXXXX` or `REG-XXXX`, containing letters, numbers, and hyphens.

The business glossary also…

**Sources retrieved (12):** `parent_chunk_business_glossary.md_0`, `parent_chunk_data_dictionary.txt_4`, `parent_chunk_business_glossary.md_2`, `Customer Master→TBLCUSTOMER`, `parent_chunk_data_dictionary.txt_5`, `parent_chunk_business_glossary.md_3`, `parent_chunk_data_dictionary.txt_8`, `parent_chunk_data_dictionary.txt_6`

**Context previews (first 3):**

1. _# CustomerMaster E-Commerce System - Business Glossary  ## Document Overview **System**: CustomerMaster v3.2.1 (Legacy) **Last Updated**: March 2015 **Purpose**: Business terminology definitions for d…_

2. _================================================================================ CUSTOMERMASTER DATABASE - DATA DICTIONARY =============================================================================…_

3. _## Legacy System Quirks  ### Hungarian Notation The legacy system uses Hungarian notation prefixes: - `str` = string (VARCHAR) - `int` = integer (INT) - `lng` = long integer (INT) - `flt` = float/mone…_

---

### ✅ 3 — What table stores order header information and what is its primary key?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.5852 | **Gate:** `proceed`

**Expected answer:**
> Order header information is stored in the vw_SalesOrderHdr table despite the vw_ prefix suggesting it's a view. The primary key is lngOrderID, which is an INT field using the lng (long integer) Hungarian notation prefix.

**System answer:**
> Order header information is stored in VW_SALESORDERHDR, which implements the business concept “Sales order header records.” The order identifier column is lngOrderID. The retrieved context does not explicitly label it as the primary key, but it is the column referenced by related tables: tblOrderStatusHistory.OrderID and ORD_LINE_ITEM.ord_id both point to VW_SALESORDERHDR.lngOrderID.

**Sources retrieved (12):** `Sales order header records→VW_SALESORDERHDR`, `parent_chunk_data_dictionary.txt_5`, `Order Line Item`, `parent_chunk_data_dictionary.txt_7`, `parent_chunk_data_dictionary.txt_4`, `Payment transaction records`, `Order Line Item→ORD_LINE_ITEM`, `parent_chunk_business_glossary.md_3`

**Context previews (first 3):**

1. _Business concept 'Sales order header records' is implemented by physical table VW_SALESORDERHDR (columns: lngOrderID, intCustID, dtmOrderDate, dtmShipDate, dtmRequiredDate, strOrderStatus, fltSubTotal…_

2. _strCategory (VARCHAR 100)     - Product category     - Hierarchical: "Clothing > Shirts > Casual" strBrand (VARCHAR 100) - Brand or manufacturer name - Free text field dtmIntroduced (DATETIME) - Produ…_

3. _Order Line Item: The table is clearly the order-detail/line-item fact: it has one row per ordered product with ord_id, prod_id, qty, amount, discount, and line status. The foreign keys to SalesOrderHd…_

---

### ✅ 4 — Which table in the schema uses a SQL reserved word as its name?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.5119 | **Gate:** `proceed`

**Expected answer:**
> The schema includes two tables that use SQL reserved words: 'Group' (for product categories) and 'User' (for system users). These require square bracket quoting [Group] and [User] in SQL queries to avoid syntax errors.

**System answer:**
> The schema uses two SQL reserved words as table names: `Group` and `User`. The context explicitly says these are reserved words and must be quoted as `[Group]` and `[User]`.

**Sources retrieved (12):** `parent_chunk_business_glossary.md_2`, `parent_chunk_data_dictionary.txt_6`, `parent_chunk_data_dictionary.txt_8`, `Group Hierarchy→GROUP`, `parent_chunk_data_dictionary.txt_5`, `parent_chunk_data_dictionary.txt_7`, `parent_chunk_data_dictionary.txt_4`, `parent_chunk_business_glossary.md_0`

**Context previews (first 3):**

1. _## Legacy System Quirks  ### Hungarian Notation The legacy system uses Hungarian notation prefixes: - `str` = string (VARCHAR) - `int` = integer (INT) - `lng` = long integer (INT) - `flt` = float/mone…_

2. _qty (INT)     - Quantity ordered     - Must be positive integer  amt (DECIMAL 10,2)     - Line item total amount (qty * unit_price)     - At time of order (snapshotted, not current price)  disc_amt (D…_

3. _CardNumberText (VARCHAR 100)     - SECURITY ISSUE: Full card number stored as text! - Should be tokenized - Contains unencrypted PAN (Primary Account Number) CardHolderName (VARCHAR 100) - Cardholder …_

---

### ✅ 5 — What is the relationship between vw_SalesOrderHdr and tblCustomer?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.9940 | **Gate:** `proceed`

**Expected answer:**
> vw_SalesOrderHdr has a foreign key relationship with tblCustomer through the intCustID field, which references strCustID. Despite the int prefix suggesting an integer, intCustID is actually a VARCHAR(50) field matching the strCustID data type.

**System answer:**
> `vw_SalesOrderHdr` is related to `tblCustomer` by a foreign key: `vw_SalesOrderHdr.intCustID` references `tblCustomer.strCustID`.

From the context, this means each sales order header record is linked to a customer master record. `tblCustomer` stores customer master data, and its primary key is `strCustID`, which is the unique customer code. In `vw_SalesOrderHdr`, the customer link is stored in `i…

**Sources retrieved (12):** `VW_SALESORDERHDR→TBLCUSTOMER`, `parent_chunk_business_glossary.md_0`, `TBLPAYMENT→VW_SALESORDERHDR`, `parent_chunk_data_dictionary.txt_5`, `parent_chunk_business_glossary.md_3`, `parent_chunk_business_glossary.md_2`, `TBLORDERSTATUSHISTORY→VW_SALESORDERHDR`, `ORD_LINE_ITEM→VW_SALESORDERHDR`

**Context previews (first 3):**

1. _Relationship: VW_SALESORDERHDR references TBLCUSTOMER via foreign key INTCUSTID -> TBLCUSTOMER.STRCUSTID.…_

2. _# CustomerMaster E-Commerce System - Business Glossary  ## Document Overview **System**: CustomerMaster v3.2.1 (Legacy) **Last Updated**: March 2015 **Purpose**: Business terminology definitions for d…_

3. _Relationship: TBLPAYMENT references VW_SALESORDERHDR via foreign key ORDERID -> VW_SALESORDERHDR.LNGORDERID.…_

---

### ✅ 6 — What naming convention is used for the inventory transaction log table?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.9306 | **Gate:** `proceed`

**Expected answer:**
> The inventory transaction log table is named 'inv_txn_log' using abbreviated naming with underscore separators. Field names within this table are also heavily abbreviated: txn_id (transaction ID), txn_dt (transaction date), txn_type (transaction type), and prod_id (product ID).

**System answer:**
> The inventory transaction log table, `inv_txn_log`, uses a heavily abbreviated naming convention. It also follows the `inv_` table prefix pattern noted in the legacy system’s inconsistent table naming conventions.

**Sources retrieved (12):** `parent_chunk_data_dictionary.txt_6`, `Product Inventory Transactions`, `Product Inventory Transactions→INV_TXN_LOG`, `parent_chunk_business_glossary.md_2`, `parent_chunk_data_dictionary.txt_7`, `parent_chunk_business_glossary.md_3`, `parent_chunk_data_dictionary.txt_4`, `INV_TXN_LOG→TBLPRODUCT`

**Context previews (first 3):**

1. _qty (INT)     - Quantity ordered     - Must be positive integer  amt (DECIMAL 10,2)     - Line item total amount (qty * unit_price)     - At time of order (snapshotted, not current price)  disc_amt (D…_

2. _Product Inventory Transactions: The table name, foreign key to `tblProduct`, and quantity/transaction date fields clearly indicate an audit log of stock changes for a product. This matches the busines…_

3. _Business concept 'Product Inventory Transactions' — The table name, foreign key to `tblProduct`, and quantity/transaction date fields clearly indicate an audit log of stock changes for a product. This…_

---

### ✅ 7 — What data quality issue exists in the tblProduct unit_cost field?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.8594 | **Gate:** `proceed`

**Expected answer:**
> The tblProduct.unit_cost field has an inappropriate data type - it's defined as VARCHAR(20) instead of DECIMAL. This field contains currency symbols like '$19.99' which require parsing before calculations can be performed, making it unusable for mathematical operations without transformation.

**System answer:**
> In `tblProduct`, the `unit_cost` field has an inappropriate data type: it is stored as `VARCHAR(20)` instead of a numeric type like `DECIMAL`. The context describes this as a bug, notes that it contains currency symbols such as `"$19.99"`, and says it must be parsed before calculations.

**Sources retrieved (12):** `parent_chunk_business_glossary.md_3`, `parent_chunk_business_glossary.md_2`, `parent_chunk_data_dictionary.txt_8`, `parent_chunk_data_dictionary.txt_6`, `parent_chunk_data_dictionary.txt_5`, `both active and discontinued products with the same SKU pattern→TBLPRODUCT`, `Product Inventory Transactions`, `Product Inventory Transactions→INV_TXN_LOG`

**Context previews (first 3):**

1. _## Migration Priority Guidelines  ### Critical Path (Must Migrate First) 1. **tblCustomer** - Required for all orders 2. **tblProduct** - Required for line items and inventory 3. **vw_SalesOrderHdr** …_

2. _## Legacy System Quirks  ### Hungarian Notation The legacy system uses Hungarian notation prefixes: - `str` = string (VARCHAR) - `int` = integer (INT) - `lng` = long integer (INT) - `flt` = float/mone…_

3. _CardNumberText (VARCHAR 100)     - SECURITY ISSUE: Full card number stored as text! - Should be tokenized - Contains unencrypted PAN (Primary Account Number) CardHolderName (VARCHAR 100) - Cardholder …_

---

### ✅ 8 — How does the ord_line_item table handle product data redundancy?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.6603 | **Gate:** `proceed`

**Expected answer:**
> The ord_line_item table contains redundant copies of product data (product_code and item_name) that are denormalized for reporting performance and to snapshot product information at the time of order. These fields may become out of sync with the tblProduct master and should not be updated from produ…

**System answer:**
> `ord_line_item` handles product data redundancy by combining a normalized product reference with denormalized product snapshot fields.

It stores `prod_id`, which is a foreign key to `TBLPRODUCT.INTPRODID`, so the line item is linked to the master product record. At the same time, it also stores redundant product fields directly on the line item: `product_code` and `item_name`.

From the data dict…

**Sources retrieved (12):** `ORD_LINE_ITEM→TBLPRODUCT`, `Order Line Item`, `Order Line Item→ORD_LINE_ITEM`, `parent_chunk_business_glossary.md_3`, `ORD_LINE_ITEM→VW_SALESORDERHDR`, `parent_chunk_business_glossary.md_2`, `parent_chunk_data_dictionary.txt_6`, `parent_chunk_business_glossary.md_0`

**Context previews (first 3):**

1. _Relationship: ORD_LINE_ITEM references TBLPRODUCT via foreign key PROD_ID -> TBLPRODUCT.INTPRODID.…_

2. _Order Line Item: The table is clearly the order-detail/line-item fact: it has one row per ordered product with ord_id, prod_id, qty, amount, discount, and line status. The foreign keys to SalesOrderHd…_

3. _Business concept 'Order Line Item' — The table is clearly the order-detail/line-item fact: it has one row per ordered product with ord_id, prod_id, qty, amount, discount, and line status. The foreign …_

---

### ✅ 9 — What are the valid values for the strOrderStatus field in vw_SalesOrderHdr?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.9131 | **Gate:** `proceed`

**Expected answer:**
> The strOrderStatus field accepts three values enforced by a CHECK constraint: 'PENDING' (order received but not shipped), 'SHIPPED' (order has been shipped to customer), and 'CANCELLED' (order cancelled before shipping).

**System answer:**
> The retrieved context does not list any valid or enumerated values for `vw_SalesOrderHdr.strOrderStatus`.

What the context does show is that `strOrderStatus` is a column on `VW_SALESORDERHDR`, and order status changes are audited in `tblOrderStatusHistory` through `OldStatus` and `NewStatus`, both defined as `VARCHAR(20)`. `tblOrderStatusHistory.OrderID` links to `vw_SalesOrderHdr.lngOrderID`. Ho…

**Sources retrieved (12):** `parent_chunk_data_dictionary.txt_5`, `Sales order header records→VW_SALESORDERHDR`, `parent_chunk_data_dictionary.txt_7`, `parent_chunk_business_glossary.md_0`, `parent_chunk_business_glossary.md_3`, `parent_chunk_business_glossary.md_2`, `TBLORDERSTATUSHISTORY→VW_SALESORDERHDR`, `Order Line Item`

**Context previews (first 3):**

1. _strCategory (VARCHAR 100)     - Product category     - Hierarchical: "Clothing > Shirts > Casual" strBrand (VARCHAR 100) - Brand or manufacturer name - Free text field dtmIntroduced (DATETIME) - Produ…_

2. _Business concept 'Sales order header records' is implemented by physical table VW_SALESORDERHDR (columns: lngOrderID, intCustID, dtmOrderDate, dtmShipDate, dtmRequiredDate, strOrderStatus, fltSubTotal…_

3. _Email (VARCHAR 150)     - User email address     - For notifications  LastLogin (DATETIME)     - Last successful login timestamp     - NULL for new users  CreatedDate (DATETIME)     - Account creation…_

---

### ✅ 10 — Which table stores payment information and what security issue does it have?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.4097 | **Gate:** `proceed`

**Expected answer:**
> Payment information is stored in the tblPayment table. The table has a critical security issue: the CardNumberText field stores full unencrypted credit card numbers as VARCHAR(100), which is a PCI compliance violation. The system also lacks proper tokenization and encryption at rest.

**System answer:**
> The payment information is stored in the physical table TBLPAYMENT, which implements the business concept Payment transaction records. Its columns include PaymentID, OrderID, PaymentMethod, PaymentDate, Amount, PaymentStatus, CardNumberText, CardHolderName, and AuthorizationCode.

The security issue is that TBLPAYMENT.CardNumberText stores card numbers in plaintext/unencrypted form. The context ex…

**Sources retrieved (12):** `Payment transaction records`, `Payment transaction records→TBLPAYMENT`, `parent_chunk_business_glossary.md_3`, `parent_chunk_data_dictionary.txt_7`, `parent_chunk_data_dictionary.txt_8`, `parent_chunk_data_dictionary.txt_4`, `parent_chunk_business_glossary.md_0`, `TBLPAYMENT→VW_SALESORDERHDR`

**Context previews (first 3):**

1. _Payment transaction records: The table stores one payment event per row with payment-specific fields such as PaymentID, OrderID, PaymentDate, Amount, PaymentStatus, and AuthorizationCode. It also incl…_

2. _Business concept 'Payment transaction records' — The table stores one payment event per row with payment-specific fields such as PaymentID, OrderID, PaymentDate, Amount, PaymentStatus, and Authorizati…_

3. _## Migration Priority Guidelines  ### Critical Path (Must Migrate First) 1. **tblCustomer** - Required for all orders 2. **tblProduct** - Required for line items and inventory 3. **vw_SalesOrderHdr** …_

---

### ✅ 11 — What is the purpose of the bolActive field in tblCustomer and tblProduct?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.9646 | **Gate:** `proceed`

**Expected answer:**
> The bolActive field (using Hungarian notation 'bol' for boolean/bit) is a flag indicating whether a record is active. In tblCustomer, it marks whether customers are included in marketing (1=active, 0=inactive). In tblProduct, it indicates product availability (1=available for sale, 0=discontinued).

**System answer:**
> In `tblCustomer`, `bolActive` is the customer active flag. The glossary states that customers “can be marked as inactive (`bolActive = 0`) but are never deleted,” so its purpose is to indicate whether a customer is active or inactive in the customer master.

For `tblProduct`, the retrieved context shows that `TBLPRODUCT` includes a `bolActive` column, and it also states that the table contains bot…

**Sources retrieved (12):** `parent_chunk_data_dictionary.txt_4`, `parent_chunk_data_dictionary.txt_7`, `parent_chunk_business_glossary.md_0`, `parent_chunk_business_glossary.md_3`, `Customer Master→TBLCUSTOMER`, `both active and discontinued products with the same SKU pattern→TBLPRODUCT`, `parent_chunk_business_glossary.md_2`, `parent_chunk_data_dictionary.txt_5`

**Context previews (first 3):**

1. _================================================================================ CUSTOMERMASTER DATABASE - DATA DICTIONARY =============================================================================…_

2. _Email (VARCHAR 150)     - User email address     - For notifications  LastLogin (DATETIME)     - Last successful login timestamp     - NULL for new users  CreatedDate (DATETIME)     - Account creation…_

3. _# CustomerMaster E-Commerce System - Business Glossary  ## Document Overview **System**: CustomerMaster v3.2.1 (Legacy) **Last Updated**: March 2015 **Purpose**: Business terminology definitions for d…_

---

### ✅ 12 — How are inventory transactions tracked in the system?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.5834 | **Gate:** `proceed`

**Expected answer:**
> Inventory transactions are tracked in the inv_txn_log table, which records all stock movements. Each transaction has a type (txn_type): 'IN' for receipts, 'OUT' for shipments, and 'ADJ' for corrections. The table uses heavily abbreviated field names and references products via prod_id.

**System answer:**
> Inventory transactions are tracked as an audit log of stock changes in the `INV_TXN_LOG` / `inv_txn_log` table, which implements the business concept “Product Inventory Transactions.”

From the retrieved context, this log is one-to-many from product to inventory transactions and is tied to products through `prod_id`, which is a foreign key to `tblProduct.intProdID`. The table stores these fields: …

**Sources retrieved (12):** `Product Inventory Transactions`, `Product Inventory Transactions→INV_TXN_LOG`, `parent_chunk_data_dictionary.txt_6`, `parent_chunk_business_glossary.md_3`, `parent_chunk_business_glossary.md_2`, `parent_chunk_business_glossary.md_0`, `parent_chunk_data_dictionary.txt_7`, `parent_chunk_data_dictionary.txt_4`

**Context previews (first 3):**

1. _Product Inventory Transactions: The table name, foreign key to `tblProduct`, and quantity/transaction date fields clearly indicate an audit log of stock changes for a product. This matches the busines…_

2. _Business concept 'Product Inventory Transactions' — The table name, foreign key to `tblProduct`, and quantity/transaction date fields clearly indicate an audit log of stock changes for a product. This…_

3. _qty (INT)     - Quantity ordered     - Must be positive integer  amt (DECIMAL 10,2)     - Line item total amount (qty * unit_price)     - At time of order (snapshotted, not current price)  disc_amt (D…_

---

### ✅ 13 — What is the self-referencing relationship in the Group table?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.9058 | **Gate:** `proceed`

**Expected answer:**
> The Group table has a self-referencing foreign key where ParentGroupID references GroupID, creating a hierarchical structure for product categories. A NULL ParentGroupID indicates a top-level group, while non-NULL values create nested category levels.

**System answer:**
> The `Group` table is self-referencing through `ParentGroupID -> Group.GroupID`. This means each group row can point to another row in the same `Group` table as its parent, implementing a hierarchical Group structure rather than a flat list. The relevant columns are `GroupID`, `GroupName`, `ParentGroupID`, `Description`, and `IsActive`. Because `Group` is a reserved word, it must be quoted as `[Gro…

**Sources retrieved (12):** `Group Hierarchy→GROUP`, `GROUP→GROUP`, `parent_chunk_data_dictionary.txt_6`, `parent_chunk_business_glossary.md_2`, `parent_chunk_business_glossary.md_3`, `parent_chunk_data_dictionary.txt_8`, `Group Hierarchy`, `parent_chunk_data_dictionary.txt_7`

**Context previews (first 3):**

1. _Business concept 'Group Hierarchy' — The table is a self-referencing `Group` structure via `ParentGroupID`, so it physically implements a hierarchical group entity rather than a flat master record. Th…_

2. _Relationship: GROUP references GROUP via foreign key PARENTGROUPID -> GROUP.GROUPID.…_

3. _qty (INT)     - Quantity ordered     - Must be positive integer  amt (DECIMAL 10,2)     - Line item total amount (qty * unit_price)     - At time of order (snapshotted, not current price)  disc_amt (D…_

---

### ✅ 14 — What migration compatibility columns exist in tblCustomer?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.9053 | **Gate:** `proceed`

**Expected answer:**
> The tblCustomer table includes cust_id (INT) and customer_name (VARCHAR 255) as migration compatibility columns alongside the legacy strCustID and strFullName fields. These are intended for the new ERP system that will use integer IDs and standardized naming conventions.

**System answer:**
> In the retrieved context, `tblCustomer` / `TBLCUSTOMER` is listed with these columns: `strCustID`, `strFullName`, `strEmail`, `strRegion`, `strCountry`, `dtmCreated`, `dtmLastModified`, `bolActive`, `cust_id`, `customer_name`, and `txtNotes`.

The columns that most clearly look like migration/compatibility columns are `cust_id` and `customer_name`, because they coexist with the legacy Hungarian-no…

**Sources retrieved (12):** `Customer Master→TBLCUSTOMER`, `parent_chunk_business_glossary.md_3`, `parent_chunk_data_dictionary.txt_4`, `parent_chunk_business_glossary.md_0`, `parent_chunk_business_glossary.md_2`, `parent_chunk_data_dictionary.txt_5`, `VW_SALESORDERHDR→TBLCUSTOMER`, `parent_chunk_data_dictionary.txt_8`

**Context previews (first 3):**

1. _Business concept 'Customer Master' — The table contains core customer master attributes such as customer ID, full name, email, region, country, active flag, and audit timestamps, indicating it physica…_

2. _## Migration Priority Guidelines  ### Critical Path (Must Migrate First) 1. **tblCustomer** - Required for all orders 2. **tblProduct** - Required for line items and inventory 3. **vw_SalesOrderHdr** …_

3. _================================================================================ CUSTOMERMASTER DATABASE - DATA DICTIONARY =============================================================================…_

---

### ✅ 15 — How does the system handle order status history tracking?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.3202 | **Gate:** `proceed`

**Expected answer:**
> Order status changes are tracked in the tblOrderStatusHistory table, which creates an audit record for each status transition. Each history record includes OrderID, OldStatus, NewStatus, ChangedByUser, ChangedDate, and ChangeReason fields, providing a complete audit trail of order workflow.

**System answer:**
> The system tracks order status history through the business concept Audit log of order status changes, implemented by the physical table TBLORDERSTATUSHISTORY / tblOrderStatusHistory.

This table is specifically described as the audit log of order status changes. Each history row records:
HistoryID as the unique auto-increment history record identifier,
OrderID as the foreign key to VW_SALESORDERH…

**Sources retrieved (12):** `Audit log of order status changes→TBLORDERSTATUSHISTORY`, `parent_chunk_data_dictionary.txt_7`, `parent_chunk_business_glossary.md_3`, `TBLORDERSTATUSHISTORY→VW_SALESORDERHDR`, `parent_chunk_business_glossary.md_0`, `parent_chunk_data_dictionary.txt_5`, `Sales order header records→VW_SALESORDERHDR`, `parent_chunk_data_dictionary.txt_6`

**Context previews (first 3):**

1. _Business concept 'Audit log of order status changes' is implemented by physical table TBLORDERSTATUSHISTORY (columns: HistoryID, OrderID, OldStatus, NewStatus, ChangedByUser, ChangedDate, ChangeReason…_

2. _Email (VARCHAR 150)     - User email address     - For notifications  LastLogin (DATETIME)     - Last successful login timestamp     - NULL for new users  CreatedDate (DATETIME)     - Account creation…_

3. _## Migration Priority Guidelines  ### Critical Path (Must Migrate First) 1. **tblCustomer** - Required for all orders 2. **tblProduct** - Required for line items and inventory 3. **vw_SalesOrderHdr** …_

---

### ✅ 16 — What is the inconsistent naming pattern between order tables?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.2869 | **Gate:** `proceed`

**Expected answer:**
> The schema shows inconsistent naming: order headers use 'vw_SalesOrderHdr' with Hungarian notation, while line items use 'ord_line_item' with abbreviated underscore notation. Additionally, the line item table references lngOrderID but names its foreign key 'ord_id' instead of 'order_id' or 'lngOrder…

**System answer:**
> The order-related tables use mixed naming conventions rather than one consistent pattern. In the context, the order header is named `vw_SalesOrderHdr`, which uses a `vw_` prefix even though it is actually a table, while the line-item table is `ord_line_item`, which uses an `ord_` prefix. There is also `tblOrderStatusHistory`, which uses the `tbl` prefix. So the inconsistency is that order tables a…

**Sources retrieved (12):** `parent_chunk_business_glossary.md_2`, `parent_chunk_data_dictionary.txt_5`, `parent_chunk_data_dictionary.txt_8`, `parent_chunk_business_glossary.md_3`, `parent_chunk_data_dictionary.txt_7`, `Order Line Item`, `parent_chunk_data_dictionary.txt_6`, `parent_chunk_business_glossary.md_0`

**Context previews (first 3):**

1. _## Legacy System Quirks  ### Hungarian Notation The legacy system uses Hungarian notation prefixes: - `str` = string (VARCHAR) - `int` = integer (INT) - `lng` = long integer (INT) - `flt` = float/mone…_

2. _strCategory (VARCHAR 100)     - Product category     - Hierarchical: "Clothing > Shirts > Casual" strBrand (VARCHAR 100) - Brand or manufacturer name - Free text field dtmIntroduced (DATETIME) - Produ…_

3. _CardNumberText (VARCHAR 100)     - SECURITY ISSUE: Full card number stored as text! - Should be tokenized - Contains unencrypted PAN (Primary Account Number) CardHolderName (VARCHAR 100) - Cardholder …_

---

### ✅ 17 — What deprecated fields exist in tblProduct and why should they be avoided?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.6637 | **Gate:** `proceed`

**Expected answer:**
> The tblProduct table contains three deprecated fields: prod_num (superseded by strSKU), item_desc (superseded by strDescription), and unit_cost (wrong data type with VARCHAR instead of DECIMAL). These fields should not be used in new code as they represent outdated design decisions.

**System answer:**
> In `tblProduct`, the deprecated legacy fields are `prod_num`, `item_desc`, and `unit_cost`.

`prod_num` (`VARCHAR 20`) is an old legacy product number. It has been superseded by `strSKU` and is retained only for historical reporting, so it should not be used for current logic.

`item_desc` (`VARCHAR 500`) is an old truncated description. It has been superseded by `strDescription`, and the context …

**Sources retrieved (12):** `parent_chunk_business_glossary.md_3`, `parent_chunk_data_dictionary.txt_5`, `Product Inventory Transactions→INV_TXN_LOG`, `Product Inventory Transactions`, `both active and discontinued products with the same SKU pattern→TBLPRODUCT`, `parent_chunk_business_glossary.md_2`, `parent_chunk_data_dictionary.txt_6`, `parent_chunk_data_dictionary.txt_8`

**Context previews (first 3):**

1. _## Migration Priority Guidelines  ### Critical Path (Must Migrate First) 1. **tblCustomer** - Required for all orders 2. **tblProduct** - Required for line items and inventory 3. **vw_SalesOrderHdr** …_

2. _strCategory (VARCHAR 100)     - Product category     - Hierarchical: "Clothing > Shirts > Casual" strBrand (VARCHAR 100) - Brand or manufacturer name - Free text field dtmIntroduced (DATETIME) - Produ…_

3. _Business concept 'Product Inventory Transactions' — The table name, foreign key to `tblProduct`, and quantity/transaction date fields clearly indicate an audit log of stock changes for a product. This…_

---

### ✅ 18 — How are shipping carriers configured in the system?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.2613 | **Gate:** `proceed`

**Expected answer:**
> Shipping carriers are stored in the tblShippingCarrier table with CarrierID, CarrierName, CarrierCode (for API integration), TrackingURL (with {TRACKING_NUM} placeholder), and bolActive flag. Only carriers with bolActive=1 should be offered during checkout.

**System answer:**
> Shipping carriers are configured as master/reference data in the `tblShippingCarrier` table, mapped in the glossary as the business concept “Shipping carrier master data” and physically implemented by `TBLSHIPPINGCARRIER`.

From the retrieved context, the carrier configuration includes these fields: `CarrierID`, `CarrierName`, `CarrierCode`, `TrackingURL`, and `bolActive`. This means the system st…

**Sources retrieved (12):** `Shipping carrier master data→TBLSHIPPINGCARRIER`, `parent_chunk_data_dictionary.txt_7`, `parent_chunk_business_glossary.md_3`, `parent_chunk_business_glossary.md_2`, `parent_chunk_business_glossary.md_0`, `parent_chunk_data_dictionary.txt_4`, `parent_chunk_data_dictionary.txt_6`, `parent_chunk_data_dictionary.txt_5`

**Context previews (first 3):**

1. _Business concept 'Shipping carrier master data' is implemented by physical table TBLSHIPPINGCARRIER (columns: CarrierID, CarrierName, CarrierCode, TrackingURL, bolActive).…_

2. _Email (VARCHAR 150)     - User email address     - For notifications  LastLogin (DATETIME)     - Last successful login timestamp     - NULL for new users  CreatedDate (DATETIME)     - Account creation…_

3. _## Migration Priority Guidelines  ### Critical Path (Must Migrate First) 1. **tblCustomer** - Required for all orders 2. **tblProduct** - Required for line items and inventory 3. **vw_SalesOrderHdr** …_

---

### ✅ 19 — What is the relationship between User table passwords and security?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.1144 | **Gate:** `proceed_with_warning`

**Expected answer:**
> The User table stores password hashes in the PasswordHash field, but uses SHA-256 without salt, making it vulnerable to rainbow table attacks. This is identified as a security issue in the data dictionary. Additionally, the table name 'User' is a SQL reserved word requiring square bracket quoting.

**System answer:**
> The `User` table, which implements the “User Account” business concept, stores password data in the `PasswordHash` column as part of the account’s core credentials (`UserID`, `UserName`, `PasswordHash`, `UserRole`, `Email`, `LastLogin`, `CreatedDate`).

The security issue identified is that `User.PasswordHash` uses SHA-256 without a salt. According to the migration notes, this is considered vulner…

**Sources retrieved (12):** `parent_chunk_business_glossary.md_3`, `User Account→USER`, `parent_chunk_data_dictionary.txt_7`, `parent_chunk_data_dictionary.txt_8`, `parent_chunk_business_glossary.md_2`, `parent_chunk_data_dictionary.txt_6`, `parent_chunk_data_dictionary.txt_4`, `parent_chunk_data_dictionary.txt_5`

**Context previews (first 3):**

1. _## Migration Priority Guidelines  ### Critical Path (Must Migrate First) 1. **tblCustomer** - Required for all orders 2. **tblProduct** - Required for line items and inventory 3. **vw_SalesOrderHdr** …_

2. _Business concept 'User Account' — The table stores the core credentials and lifecycle attributes of an account record, including username, password hash, role, email, last login, and creation date. Th…_

3. _Email (VARCHAR 150)     - User email address     - For notifications  LastLogin (DATETIME)     - Last successful login timestamp     - NULL for new users  CreatedDate (DATETIME)     - Account creation…_

---

### ✅ 20 — What fields in vw_SalesOrderHdr use the 'flt' Hungarian notation prefix and what do they store?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.9078 | **Gate:** `proceed`

**Expected answer:**
> The vw_SalesOrderHdr table uses the 'flt' (float) prefix for three monetary fields: fltSubTotal (line item subtotal before tax), fltTaxAmount (calculated tax), and fltTotalAmount (final total including tax and shipping). Despite the 'flt' prefix suggesting floating-point, these are defined as DECIMA…

**System answer:**
> In `VW_SALESORDERHDR`, the fields with the `flt` Hungarian notation prefix are `fltSubTotal`, `fltTaxAmount`, and `fltTotalAmount`. From the legacy notation guidelines, `flt` indicates a float/money field, i.e. a `DECIMAL`-type amount field.

Based on the column names, they store the order subtotal, the tax amount, and the total order amount, respectively. The retrieved context also notes a data q…

**Sources retrieved (12):** `Sales order header records→VW_SALESORDERHDR`, `parent_chunk_business_glossary.md_3`, `parent_chunk_data_dictionary.txt_5`, `parent_chunk_business_glossary.md_2`, `parent_chunk_business_glossary.md_0`, `Order Line Item`, `parent_chunk_data_dictionary.txt_7`, `Order Line Item→ORD_LINE_ITEM`

**Context previews (first 3):**

1. _Business concept 'Sales order header records' is implemented by physical table VW_SALESORDERHDR (columns: lngOrderID, intCustID, dtmOrderDate, dtmShipDate, dtmRequiredDate, strOrderStatus, fltSubTotal…_

2. _## Migration Priority Guidelines  ### Critical Path (Must Migrate First) 1. **tblCustomer** - Required for all orders 2. **tblProduct** - Required for line items and inventory 3. **vw_SalesOrderHdr** …_

3. _strCategory (VARCHAR 100)     - Product category     - Hierarchical: "Clothing > Shirts > Casual" strBrand (VARCHAR 100) - Brand or manufacturer name - Free text field dtmIntroduced (DATETIME) - Produ…_

---

### ✅ 21 — How does the schema handle the different date/time field naming conventions?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.1757 | **Gate:** `proceed_with_warning`

**Expected answer:**
> The schema uses 'dtm' (datetime) Hungarian notation prefix consistently: dtmCreated and dtmLastModified in tblCustomer, dtmOrderDate/dtmShipDate/dtmRequiredDate in vw_SalesOrderHdr, dtmIntroduced/dtmDiscontinued in tblProduct, and txn_dt in inv_txn_log (abbreviated exception). The User table breaks …

**System answer:**
> The schema does not use a single consistent date/time naming standard. The retrieved context shows that date/time fields are handled through multiple naming conventions depending on the table or subsystem.

In the legacy Hungarian notation pattern, `dtm` denotes a `DATETIME` field. The context explicitly says `dtm = datetime (DATETIME)`. Examples include `tblProduct.dtmIntroduced` and `tblProduct.…

**Sources retrieved (12):** `parent_chunk_data_dictionary.txt_5`, `parent_chunk_business_glossary.md_2`, `parent_chunk_data_dictionary.txt_4`, `parent_chunk_data_dictionary.txt_8`, `parent_chunk_data_dictionary.txt_7`, `parent_chunk_data_dictionary.txt_6`, `parent_chunk_business_glossary.md_3`, `parent_chunk_business_glossary.md_0`

**Context previews (first 3):**

1. _strCategory (VARCHAR 100)     - Product category     - Hierarchical: "Clothing > Shirts > Casual" strBrand (VARCHAR 100) - Brand or manufacturer name - Free text field dtmIntroduced (DATETIME) - Produ…_

2. _## Legacy System Quirks  ### Hungarian Notation The legacy system uses Hungarian notation prefixes: - `str` = string (VARCHAR) - `int` = integer (INT) - `lng` = long integer (INT) - `flt` = float/mone…_

3. _================================================================================ CUSTOMERMASTER DATABASE - DATA DICTIONARY =============================================================================…_

---

### ✅ 22 — What table prefix patterns exist in the schema and what do they indicate?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0907 | **Gate:** `proceed_with_warning`

**Expected answer:**
> The schema uses multiple inconsistent table prefixes: 'tbl' for standard tables (tblCustomer, tblProduct, tblPayment, tblShippingCarrier, tblOrderStatusHistory), 'vw_' for a misnamed table (vw_SalesOrderHdr), and domain-specific prefixes 'ord_' (ord_line_item) and 'inv_' (inv_txn_log). Two tables (G…

**System answer:**
> The schema uses inconsistent table prefix patterns.

The `tbl` prefix appears on tables such as `tblCustomer`, `tblProduct`, `tblPayment`, and `tblOrderStatusHistory`. The context identifies this as one naming convention used in the legacy system; these are regular tables and tend to use more verbose names.

The `vw_` prefix appears in `vw_SalesOrderHdr`, but the context explicitly says these are …

**Sources retrieved (12):** `parent_chunk_data_dictionary.txt_5`, `parent_chunk_data_dictionary.txt_8`, `parent_chunk_business_glossary.md_2`, `parent_chunk_data_dictionary.txt_7`, `both active and discontinued products with the same SKU pattern→TBLPRODUCT`, `parent_chunk_business_glossary.md_0`, `Product Inventory Transactions`, `parent_chunk_business_glossary.md_3`

**Context previews (first 3):**

1. _strCategory (VARCHAR 100)     - Product category     - Hierarchical: "Clothing > Shirts > Casual" strBrand (VARCHAR 100) - Brand or manufacturer name - Free text field dtmIntroduced (DATETIME) - Produ…_

2. _CardNumberText (VARCHAR 100)     - SECURITY ISSUE: Full card number stored as text! - Should be tokenized - Contains unencrypted PAN (Primary Account Number) CardHolderName (VARCHAR 100) - Cardholder …_

3. _## Legacy System Quirks  ### Hungarian Notation The legacy system uses Hungarian notation prefixes: - `str` = string (VARCHAR) - `int` = integer (INT) - `lng` = long integer (INT) - `flt` = float/mone…_

---

### ✅ 23 — What foreign key relationships exist for the vw_SalesOrderHdr table?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.9902 | **Gate:** `proceed`

**Expected answer:**
> The vw_SalesOrderHdr table has one explicit foreign key constraint: intCustID references tblCustomer.strCustID. Implicit relationships (not enforced by FK constraints) include tblPayment.OrderID, tblOrderStatusHistory.OrderID, and ord_line_item.ord_id all referencing vw_SalesOrderHdr.lngOrderID.

**System answer:**
> The `VW_SALESORDERHDR` table has one outgoing foreign key and three incoming foreign key relationships in the retrieved context.

It references `TBLCUSTOMER` through `INTCUSTID -> TBLCUSTOMER.STRCUSTID`. The `VW_SALESORDERHDR` columns shown include `lngOrderID` and `intCustID`; the legacy notation notes that `intCustID` is actually a `VARCHAR` despite its `int` prefix.

Three tables reference `VW_…

**Sources retrieved (12):** `VW_SALESORDERHDR→TBLCUSTOMER`, `ORD_LINE_ITEM→VW_SALESORDERHDR`, `TBLPAYMENT→VW_SALESORDERHDR`, `TBLORDERSTATUSHISTORY→VW_SALESORDERHDR`, `Order Line Item`, `Order Line Item→ORD_LINE_ITEM`, `parent_chunk_data_dictionary.txt_5`, `parent_chunk_data_dictionary.txt_7`

**Context previews (first 3):**

1. _Relationship: VW_SALESORDERHDR references TBLCUSTOMER via foreign key INTCUSTID -> TBLCUSTOMER.STRCUSTID.…_

2. _Relationship: ORD_LINE_ITEM references VW_SALESORDERHDR via foreign key ORD_ID -> VW_SALESORDERHDR.LNGORDERID.…_

3. _Relationship: TBLPAYMENT references VW_SALESORDERHDR via foreign key ORDERID -> VW_SALESORDERHDR.LNGORDERID.…_

---

### ✅ 24 — How does the legacy system handle product SKU format and uniqueness?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.3256 | **Gate:** `proceed`

**Expected answer:**
> Product SKUs are stored in the strSKU field with a UNIQUE constraint. The format follows Category-Color-Size pattern (e.g., 'SHIRT-BLU-L'). The deprecated prod_num field also exists but should not be used. SKUs are used in foreign key references from ord_line_item through the denormalized product_co…

**System answer:**
> The legacy system uses `tblProduct.strSKU` as the current product identifier, and the older `prod_num` field is deprecated and explicitly “superseded by `strSKU`” but retained for historical reporting.

From the available context, the system does not provide a documented formal SKU format rule or a stated uniqueness constraint for `strSKU`. What the context does say is that `tblProduct` has a data…

**Sources retrieved (12):** `parent_chunk_business_glossary.md_0`, `parent_chunk_business_glossary.md_2`, `parent_chunk_data_dictionary.txt_4`, `parent_chunk_data_dictionary.txt_5`, `parent_chunk_business_glossary.md_3`, `both active and discontinued products with the same SKU pattern→TBLPRODUCT`, `parent_chunk_data_dictionary.txt_6`, `Customer Master→TBLCUSTOMER`

**Context previews (first 3):**

1. _# CustomerMaster E-Commerce System - Business Glossary  ## Document Overview **System**: CustomerMaster v3.2.1 (Legacy) **Last Updated**: March 2015 **Purpose**: Business terminology definitions for d…_

2. _## Legacy System Quirks  ### Hungarian Notation The legacy system uses Hungarian notation prefixes: - `str` = string (VARCHAR) - `int` = integer (INT) - `lng` = long integer (INT) - `flt` = float/mone…_

3. _================================================================================ CUSTOMERMASTER DATABASE - DATA DICTIONARY =============================================================================…_

---

### ✅ 25 — What are the critical data quality issues identified for migration?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.9662 | **Gate:** `proceed`

**Expected answer:**
> Critical issues include: (1) PCI compliance violation - unencrypted card numbers in tblPayment.CardNumberText, (2) inappropriate data types - unit_cost as VARCHAR instead of DECIMAL, (3) missing foreign key constraints - inv_txn_log.user_id has no FK to User table, (4) security vulnerability - User.…

**System answer:**
> The migration issues identified are:

Referential integrity gaps: some `ord_line_item.prod_id` values point to non-existent or deleted products, some orders reference customers that are marked inactive, and `inv_txn_log.user_id` has no foreign key constraint.

Data inconsistencies: `tblProduct` contains both active and discontinued products using the same SKU pattern, some `vw_SalesOrderHdr` rows …

**Sources retrieved (12):** `parent_chunk_business_glossary.md_3`, `parent_chunk_data_dictionary.txt_8`, `parent_chunk_business_glossary.md_0`, `parent_chunk_business_glossary.md_2`, `parent_chunk_data_dictionary.txt_4`, `Customer Master→TBLCUSTOMER`, `parent_chunk_data_dictionary.txt_6`, `parent_chunk_data_dictionary.txt_7`

**Context previews (first 3):**

1. _## Migration Priority Guidelines  ### Critical Path (Must Migrate First) 1. **tblCustomer** - Required for all orders 2. **tblProduct** - Required for line items and inventory 3. **vw_SalesOrderHdr** …_

2. _CardNumberText (VARCHAR 100)     - SECURITY ISSUE: Full card number stored as text! - Should be tokenized - Contains unencrypted PAN (Primary Account Number) CardHolderName (VARCHAR 100) - Cardholder …_

3. _# CustomerMaster E-Commerce System - Business Glossary  ## Document Overview **System**: CustomerMaster v3.2.1 (Legacy) **Last Updated**: March 2015 **Purpose**: Business terminology definitions for d…_

---

## Anomalies & Observations

No anomalies detected. All questions grounded with acceptable RAGAS scores.
