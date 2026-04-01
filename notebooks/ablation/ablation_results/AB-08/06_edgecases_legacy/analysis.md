# AB-08 — 06_edgecases_legacy — Run Analysis

**Timestamp:** 2026-03-31 19:44:23  
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
| Chunk size / overlap | `512 / 64` |
| ER similarity threshold | `0.75` |

## Builder Results

| Metric | Value |
|--------|-------|
| Triplets extracted | 473 |
| Entities resolved | 286 |
| Tables parsed | 10 |
| Tables completed | 10 |

## Query Evaluation Summary

| Metric | Value |
|--------|-------|
| Questions | 25 |
| Grounded | **25/25 (100%)** |
| Avg GT Coverage | 100% |
| Avg Top Score | 0.6087 |
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
> The `tblCustomer` table stores customer master data from the legacy CRM system. In the business glossary, this corresponds to the `Customer` entity: an individual or organization that has purchased products or services from the company. Customers in `tblCustomer` use legacy identifiers inherited from the AS/400 system.

**Sources retrieved (12):** `parent_chunk_data_dictionary.txt_4`, `parent_chunk_business_glossary.md_0`, `parent_chunk_data_dictionary.txt_5`, `parent_chunk_business_glossary.md_3`, `parent_chunk_data_dictionary.txt_7`, `VW_SALESORDERHDR→TBLCUSTOMER`, `parent_chunk_business_glossary.md_2`, `parent_chunk_data_dictionary.txt_6`

**Context previews (first 3):**

1. _================================================================================ CUSTOMERMASTER DATABASE - DATA DICTIONARY =============================================================================…_

2. _# CustomerMaster E-Commerce System - Business Glossary  ## Document Overview **System**: CustomerMaster v3.2.1 (Legacy) **Last Updated**: March 2015 **Purpose**: Business terminology definitions for d…_

3. _strCategory (VARCHAR 100)     - Product category     - Hierarchical: "Clothing > Shirts > Casual" strBrand (VARCHAR 100) - Brand or manufacturer name - Free text field dtmIntroduced (DATETIME) - Produ…_

---

### ✅ 2 — How are customers identified in the legacy system?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.8295 | **Gate:** `proceed`

**Expected answer:**
> Customers are identified by strCustID, which is a VARCHAR(50) field containing alphanumeric customer codes inherited from an AS/400 system. These codes follow formats like C-XXXXX or REG-XXXX and can contain letters, numbers, and hyphens.

**System answer:**
> In the legacy CustomerMaster system, customers are identified by `tblCustomer.strCustID`. This is the primary key and the business-defined unique customer code for a customer. The glossary says this identifier is a legacy identifier inherited from the AS/400 system, and the data dictionary defines it as `VARCHAR(50)`, `NOT NULL`, and `UNIQUE`.

The identifier is alphanumeric and uses formats such …

**Sources retrieved (12):** `parent_chunk_business_glossary.md_0`, `parent_chunk_data_dictionary.txt_4`, `parent_chunk_business_glossary.md_2`, `parent_chunk_data_dictionary.txt_5`, `parent_chunk_business_glossary.md_3`, `parent_chunk_data_dictionary.txt_8`, `parent_chunk_data_dictionary.txt_6`, `parent_chunk_data_dictionary.txt_7`

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
> Order header information is stored in VW_SALESORDERHDR, which implements the business concept Sales order header records.

The context does not explicitly label a primary key for VW_SALESORDERHDR, but lngOrderID is the order identifier column and is the key referenced by related tables:
ORD_LINE_ITEM.ORD_ID -> VW_SALESORDERHDR.LNGORDERID,
TBLPAYMENT.ORDERID -> VW_SALESORDERHDR.LNGORDERID,
and TBLO…

**Sources retrieved (12):** `Sales order header records→VW_SALESORDERHDR`, `parent_chunk_data_dictionary.txt_5`, `Order Line Item`, `parent_chunk_data_dictionary.txt_7`, `parent_chunk_data_dictionary.txt_4`, `parent_chunk_business_glossary.md_3`, `Order status→TBLORDERSTATUSHISTORY`, `Order Line Item→ORD_LINE_ITEM`

**Context previews (first 3):**

1. _Business concept 'Sales order header records' is implemented by physical table VW_SALESORDERHDR (columns: lngOrderID, intCustID, dtmOrderDate, dtmShipDate, dtmRequiredDate, strOrderStatus, fltSubTotal…_

2. _strCategory (VARCHAR 100)     - Product category     - Hierarchical: "Clothing > Shirts > Casual" strBrand (VARCHAR 100) - Brand or manufacturer name - Free text field dtmIntroduced (DATETIME) - Produ…_

3. _Order Line Item: The table structure matches an order line entity: it has a line identifier, foreign keys to an order and a product, plus quantity, amount, discount, and status fields. The redundant p…_

---

### ✅ 4 — Which table in the schema uses a SQL reserved word as its name?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.5119 | **Gate:** `proceed`

**Expected answer:**
> The schema includes two tables that use SQL reserved words: 'Group' (for product categories) and 'User' (for system users). These require square bracket quoting [Group] and [User] in SQL queries to avoid syntax errors.

**System answer:**
> The schema uses two tables with SQL reserved words as names: `Group` and `User`. The context says they must be quoted as `[Group]` and `[User]`.

**Sources retrieved (12):** `parent_chunk_business_glossary.md_2`, `parent_chunk_data_dictionary.txt_6`, `parent_chunk_data_dictionary.txt_8`, `parent_chunk_data_dictionary.txt_5`, `parent_chunk_data_dictionary.txt_7`, `parent_chunk_data_dictionary.txt_4`, `parent_chunk_business_glossary.md_0`, `parent_chunk_business_glossary.md_3`

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
> `vw_SalesOrderHdr` references `tblCustomer` through a foreign key from `vw_SalesOrderHdr.intCustID` to `tblCustomer.strCustID`.

From the context:
`VW_SALESORDERHDR` has column `intCustID`.
`tblCustomer` has primary key `strCustID`, which is the unique customer code.
The business glossary also states that customers are stored in `tblCustomer`, and migration guidance says `tblCustomer` is required …

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
> The inventory transaction log table is `inv_txn_log`, and its table-specific naming convention is explicitly described as “Heavily abbreviated.” The broader legacy convention also shows it uses the `inv_` prefix for inventory-related tables.

**Sources retrieved (12):** `parent_chunk_data_dictionary.txt_6`, `Product → Inventory Transactions→INV_TXN_LOG`, `parent_chunk_business_glossary.md_2`, `parent_chunk_data_dictionary.txt_7`, `parent_chunk_business_glossary.md_3`, `parent_chunk_data_dictionary.txt_4`, `INV_TXN_LOG→TBLPRODUCT`, `parent_chunk_data_dictionary.txt_8`

**Context previews (first 3):**

1. _qty (INT)     - Quantity ordered     - Must be positive integer  amt (DECIMAL 10,2)     - Line item total amount (qty * unit_price)     - At time of order (snapshotted, not current price)  disc_amt (D…_

2. _Business concept 'Product → Inventory Transactions' is implemented by physical table INV_TXN_LOG (columns: txn_id, prod_id, txn_type, qty, txn_dt, ref_num, user_id, notes).…_

3. _## Legacy System Quirks  ### Hungarian Notation The legacy system uses Hungarian notation prefixes: - `str` = string (VARCHAR) - `int` = integer (INT) - `lng` = long integer (INT) - `flt` = float/mone…_

---

### ✅ 7 — What data quality issue exists in the tblProduct unit_cost field?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.8594 | **Gate:** `proceed`

**Expected answer:**
> The tblProduct.unit_cost field has an inappropriate data type - it's defined as VARCHAR(20) instead of DECIMAL. This field contains currency symbols like '$19.99' which require parsing before calculations can be performed, making it unusable for mathematical operations without transformation.

**System answer:**
> The `tblProduct.unit_cost` field has an inappropriate data type and is identified as a bug. It is defined as `VARCHAR(20)` instead of a numeric type, stores cost as text, includes currency symbols such as `"$19.99"`, and therefore must be parsed before calculations. The context explicitly says it should be `DECIMAL`.

**Sources retrieved (12):** `parent_chunk_business_glossary.md_3`, `parent_chunk_business_glossary.md_2`, `parent_chunk_data_dictionary.txt_8`, `parent_chunk_data_dictionary.txt_6`, `parent_chunk_data_dictionary.txt_5`, `both active and discontinued products with the same SKU pattern→TBLPRODUCT`, `parent_chunk_data_dictionary.txt_7`, `ORD_LINE_ITEM→TBLPRODUCT`

**Context previews (first 3):**

1. _## Migration Priority Guidelines  ### Critical Path (Must Migrate First) 1. **tblCustomer** - Required for all orders 2. **tblProduct** - Required for line items and inventory 3. **vw_SalesOrderHdr** …_

2. _## Legacy System Quirks  ### Hungarian Notation The legacy system uses Hungarian notation prefixes: - `str` = string (VARCHAR) - `int` = integer (INT) - `lng` = long integer (INT) - `flt` = float/mone…_

3. _CardNumberText (VARCHAR 100)     - SECURITY ISSUE: Full card number stored as text! - Should be tokenized - Contains unencrypted PAN (Primary Account Number) CardHolderName (VARCHAR 100) - Cardholder …_

---

### ✅ 8 — How does the ord_line_item table handle product data redundancy?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.9047 | **Gate:** `proceed`

**Expected answer:**
> The ord_line_item table contains redundant copies of product data (product_code and item_name) that are denormalized for reporting performance and to snapshot product information at the time of order. These fields may become out of sync with the tblProduct master and should not be updated from produ…

**System answer:**
> `ord_line_item` stores product data both normalized and denormalized. It has `prod_id`, which is a foreign key to `TBLPRODUCT.INTPRODID`, but it also keeps redundant product attributes in the same row: `product_code` and `item_name`.

From the context, `product_code` is a redundant copy of `tblProduct.strSKU`. It is denormalized for reporting performance, but it may become out of sync with the mas…

**Sources retrieved (12):** `Order Line Item`, `Order Line Item→ORD_LINE_ITEM`, `ORD_LINE_ITEM→TBLPRODUCT`, `parent_chunk_business_glossary.md_3`, `ORD_LINE_ITEM→VW_SALESORDERHDR`, `parent_chunk_business_glossary.md_2`, `parent_chunk_data_dictionary.txt_8`, `parent_chunk_data_dictionary.txt_6`

**Context previews (first 3):**

1. _Order Line Item: The table structure matches an order line entity: it has a line identifier, foreign keys to an order and a product, plus quantity, amount, discount, and status fields. The redundant p…_

2. _Business concept 'Order Line Item' — The table structure matches an order line entity: it has a line identifier, foreign keys to an order and a product, plus quantity, amount, discount, and status fie…_

3. _Relationship: ORD_LINE_ITEM references TBLPRODUCT via foreign key PROD_ID -> TBLPRODUCT.INTPRODID.…_

---

### ✅ 9 — What are the valid values for the strOrderStatus field in vw_SalesOrderHdr?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.9131 | **Gate:** `proceed`

**Expected answer:**
> The strOrderStatus field accepts three values enforced by a CHECK constraint: 'PENDING' (order received but not shipped), 'SHIPPED' (order has been shipped to customer), and 'CANCELLED' (order cancelled before shipping).

**System answer:**
> The retrieved context shows that `vw_SalesOrderHdr` includes a `strOrderStatus` column, and `tblOrderStatusHistory` tracks status changes with `OldStatus` and `NewStatus` for `OrderID -> vw_SalesOrderHdr.lngOrderID`. However, the context does not provide an enumeration or list of valid `strOrderStatus` values.

The only related detail is that `tblOrderStatusHistory.ChangeReason` may contain free-t…

**Sources retrieved (12):** `parent_chunk_data_dictionary.txt_5`, `Sales order header records→VW_SALESORDERHDR`, `parent_chunk_data_dictionary.txt_7`, `parent_chunk_business_glossary.md_0`, `parent_chunk_business_glossary.md_3`, `parent_chunk_business_glossary.md_2`, `TBLORDERSTATUSHISTORY→VW_SALESORDERHDR`, `VW_SALESORDERHDR→TBLCUSTOMER`

**Context previews (first 3):**

1. _strCategory (VARCHAR 100)     - Product category     - Hierarchical: "Clothing > Shirts > Casual" strBrand (VARCHAR 100) - Brand or manufacturer name - Free text field dtmIntroduced (DATETIME) - Produ…_

2. _Business concept 'Sales order header records' is implemented by physical table VW_SALESORDERHDR (columns: lngOrderID, intCustID, dtmOrderDate, dtmShipDate, dtmRequiredDate, strOrderStatus, fltSubTotal…_

3. _Email (VARCHAR 150)     - User email address     - For notifications  LastLogin (DATETIME)     - Last successful login timestamp     - NULL for new users  CreatedDate (DATETIME)     - Account creation…_

---

### ✅ 10 — Which table stores payment information and what security issue does it have?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.2454 | **Gate:** `proceed`

**Expected answer:**
> Payment information is stored in the tblPayment table. The table has a critical security issue: the CardNumberText field stores full unencrypted credit card numbers as VARCHAR(100), which is a PCI compliance violation. The system also lacks proper tokenization and encryption at rest.

**System answer:**
> Payment information is stored in `tblPayment` (also shown as `TBLPAYMENT`). It contains fields such as `PaymentID`, `OrderID`, `PaymentMethod`, `PaymentDate`, `Amount`, `PaymentStatus`, `CardNumberText`, `CardHolderName`, and `AuthorizationCode`.

The security issue is that `tblPayment.CardNumberText` stores full card numbers in plaintext as unencrypted PAN data. The context flags this as a critic…

**Sources retrieved (12):** `Unknown→TBLPAYMENT`, `parent_chunk_business_glossary.md_3`, `parent_chunk_data_dictionary.txt_7`, `parent_chunk_data_dictionary.txt_8`, `parent_chunk_data_dictionary.txt_4`, `parent_chunk_business_glossary.md_0`, `TBLPAYMENT→VW_SALESORDERHDR`, `parent_chunk_business_glossary.md_2`

**Context previews (first 3):**

1. _Business concept 'Unknown' — The table is a payment transaction record with amount, date, status, method, and card details, but the business entities only define supporting concepts such as Authorizat…_

2. _## Migration Priority Guidelines  ### Critical Path (Must Migrate First) 1. **tblCustomer** - Required for all orders 2. **tblProduct** - Required for line items and inventory 3. **vw_SalesOrderHdr** …_

3. _Email (VARCHAR 150)     - User email address     - For notifications  LastLogin (DATETIME)     - Last successful login timestamp     - NULL for new users  CreatedDate (DATETIME)     - Account creation…_

---

### ✅ 11 — What is the purpose of the bolActive field in tblCustomer and tblProduct?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.9646 | **Gate:** `proceed`

**Expected answer:**
> The bolActive field (using Hungarian notation 'bol' for boolean/bit) is a flag indicating whether a record is active. In tblCustomer, it marks whether customers are included in marketing (1=active, 0=inactive). In tblProduct, it indicates product availability (1=available for sale, 0=discontinued).

**System answer:**
> For `tblCustomer`, the context does define the purpose of `bolActive`: customers “can be marked as inactive (`bolActive = 0`) but are never deleted.” So in `tblCustomer`, `bolActive` is used to indicate whether a customer is inactive versus active.

For `tblProduct`, the context only confirms that `bolActive` exists as a column in `TBLPRODUCT`, and that the table contains both active and discontin…

**Sources retrieved (12):** `parent_chunk_data_dictionary.txt_4`, `parent_chunk_data_dictionary.txt_7`, `parent_chunk_business_glossary.md_0`, `parent_chunk_business_glossary.md_3`, `both active and discontinued products with the same SKU pattern→TBLPRODUCT`, `parent_chunk_business_glossary.md_2`, `parent_chunk_data_dictionary.txt_5`, `parent_chunk_data_dictionary.txt_6`

**Context previews (first 3):**

1. _================================================================================ CUSTOMERMASTER DATABASE - DATA DICTIONARY =============================================================================…_

2. _Email (VARCHAR 150)     - User email address     - For notifications  LastLogin (DATETIME)     - Last successful login timestamp     - NULL for new users  CreatedDate (DATETIME)     - Account creation…_

3. _# CustomerMaster E-Commerce System - Business Glossary  ## Document Overview **System**: CustomerMaster v3.2.1 (Legacy) **Last Updated**: March 2015 **Purpose**: Business terminology definitions for d…_

---

### ✅ 12 — How are inventory transactions tracked in the system?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.4369 | **Gate:** `proceed`

**Expected answer:**
> Inventory transactions are tracked in the inv_txn_log table, which records all stock movements. Each transaction has a type (txn_type): 'IN' for receipts, 'OUT' for shipments, and 'ADJ' for corrections. The table uses heavily abbreviated field names and references products via prod_id.

**System answer:**
> Inventory transactions are tracked through the business concept Product → Inventory Transactions, which is implemented by the physical table `INV_TXN_LOG` / `inv_txn_log`.

This table’s stated purpose is an inventory transaction log, and it also appears in the migration guidance as the inventory audit trail. The tracked fields are `txn_id`, `prod_id`, `txn_type`, `qty`, `txn_dt`, `ref_num`, `user_…

**Sources retrieved (12):** `Product → Inventory Transactions→INV_TXN_LOG`, `parent_chunk_data_dictionary.txt_6`, `parent_chunk_business_glossary.md_3`, `Product → Inventory Transactions`, `parent_chunk_business_glossary.md_2`, `parent_chunk_business_glossary.md_0`, `parent_chunk_data_dictionary.txt_7`, `parent_chunk_data_dictionary.txt_4`

**Context previews (first 3):**

1. _Business concept 'Product → Inventory Transactions' is implemented by physical table INV_TXN_LOG (columns: txn_id, prod_id, txn_type, qty, txn_dt, ref_num, user_id, notes).…_

2. _qty (INT)     - Quantity ordered     - Must be positive integer  amt (DECIMAL 10,2)     - Line item total amount (qty * unit_price)     - At time of order (snapshotted, not current price)  disc_amt (D…_

3. _## Migration Priority Guidelines  ### Critical Path (Must Migrate First) 1. **tblCustomer** - Required for all orders 2. **tblProduct** - Required for line items and inventory 3. **vw_SalesOrderHdr** …_

---

### ✅ 13 — What is the self-referencing relationship in the Group table?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.3145 | **Gate:** `proceed`

**Expected answer:**
> The Group table has a self-referencing foreign key where ParentGroupID references GroupID, creating a hierarchical structure for product categories. A NULL ParentGroupID indicates a top-level group, while non-NULL values create nested category levels.

**System answer:**
> The `GROUP` table has a self-referencing foreign key: `PARENTGROUPID -> GROUP.GROUPID`. This means each group can reference another row in the same `GROUP` table as its parent, supporting the hierarchical category navigation structure described for `GROUP` (`GroupID`, `GroupName`, `ParentGroupID`, `Description`, `IsActive`).

**Sources retrieved (12):** `GROUP→GROUP`, `parent_chunk_data_dictionary.txt_6`, `parent_chunk_business_glossary.md_2`, `parent_chunk_business_glossary.md_3`, `category navigation→GROUP`, `parent_chunk_data_dictionary.txt_8`, `parent_chunk_data_dictionary.txt_7`, `parent_chunk_data_dictionary.txt_4`

**Context previews (first 3):**

1. _Relationship: GROUP references GROUP via foreign key PARENTGROUPID -> GROUP.GROUPID.…_

2. _qty (INT)     - Quantity ordered     - Must be positive integer  amt (DECIMAL 10,2)     - Line item total amount (qty * unit_price)     - At time of order (snapshotted, not current price)  disc_amt (D…_

3. _## Legacy System Quirks  ### Hungarian Notation The legacy system uses Hungarian notation prefixes: - `str` = string (VARCHAR) - `int` = integer (INT) - `lng` = long integer (INT) - `flt` = float/mone…_

---

### ✅ 14 — What migration compatibility columns exist in tblCustomer?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.6606 | **Gate:** `proceed`

**Expected answer:**
> The tblCustomer table includes cust_id (INT) and customer_name (VARCHAR 255) as migration compatibility columns alongside the legacy strCustID and strFullName fields. These are intended for the new ERP system that will use integer IDs and standardized naming conventions.

**System answer:**
> The retrieved context does not identify any `tblCustomer` fields as “migration compatibility columns.”

From the available `tblCustomer` metadata, I can only confirm these columns:
`strCustID` (the primary key, VARCHAR 50, legacy customer identifier) and `strFullName` (VARCHAR 255, customer full name).

The context also states that customers are stored in `tblCustomer`, use legacy AS/400 identifie…

**Sources retrieved (12):** `parent_chunk_business_glossary.md_3`, `parent_chunk_data_dictionary.txt_4`, `parent_chunk_business_glossary.md_0`, `parent_chunk_business_glossary.md_2`, `parent_chunk_data_dictionary.txt_5`, `VW_SALESORDERHDR→TBLCUSTOMER`, `parent_chunk_data_dictionary.txt_8`, `both active and discontinued products with the same SKU pattern→TBLPRODUCT`

**Context previews (first 3):**

1. _## Migration Priority Guidelines  ### Critical Path (Must Migrate First) 1. **tblCustomer** - Required for all orders 2. **tblProduct** - Required for line items and inventory 3. **vw_SalesOrderHdr** …_

2. _================================================================================ CUSTOMERMASTER DATABASE - DATA DICTIONARY =============================================================================…_

3. _# CustomerMaster E-Commerce System - Business Glossary  ## Document Overview **System**: CustomerMaster v3.2.1 (Legacy) **Last Updated**: March 2015 **Purpose**: Business terminology definitions for d…_

---

### ✅ 15 — How does the system handle order status history tracking?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.3658 | **Gate:** `proceed`

**Expected answer:**
> Order status changes are tracked in the tblOrderStatusHistory table, which creates an audit record for each status transition. Each history record includes OrderID, OldStatus, NewStatus, ChangedByUser, ChangedDate, and ChangeReason fields, providing a complete audit trail of order workflow.

**System answer:**
> The system tracks order status history with the physical table `TBLORDERSTATUSHISTORY` / `tblOrderStatusHistory`, which is the implementation of the business concept `Order status`. Its stated purpose is an audit log of order status changes.

Each status change is stored as one history record with:
`HistoryID` as the auto-increment primary key,
`OrderID` as the foreign key to `VW_SALESORDERHDR.LNG…

**Sources retrieved (12):** `Order status→TBLORDERSTATUSHISTORY`, `parent_chunk_data_dictionary.txt_7`, `parent_chunk_business_glossary.md_3`, `TBLORDERSTATUSHISTORY→VW_SALESORDERHDR`, `parent_chunk_business_glossary.md_0`, `parent_chunk_data_dictionary.txt_5`, `Sales order header records→VW_SALESORDERHDR`, `parent_chunk_data_dictionary.txt_6`

**Context previews (first 3):**

1. _Business concept 'Order status' is implemented by physical table TBLORDERSTATUSHISTORY (columns: HistoryID, OrderID, OldStatus, NewStatus, ChangedByUser, ChangedDate, ChangeReason).…_

2. _Email (VARCHAR 150)     - User email address     - For notifications  LastLogin (DATETIME)     - Last successful login timestamp     - NULL for new users  CreatedDate (DATETIME)     - Account creation…_

3. _## Migration Priority Guidelines  ### Critical Path (Must Migrate First) 1. **tblCustomer** - Required for all orders 2. **tblProduct** - Required for line items and inventory 3. **vw_SalesOrderHdr** …_

---

### ✅ 16 — What is the inconsistent naming pattern between order tables?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.2869 | **Gate:** `proceed`

**Expected answer:**
> The schema shows inconsistent naming: order headers use 'vw_SalesOrderHdr' with Hungarian notation, while line items use 'ord_line_item' with abbreviated underscore notation. Additionally, the line item table references lngOrderID but names its foreign key 'ord_id' instead of 'order_id' or 'lngOrder…

**System answer:**
> The order-related tables use inconsistent naming conventions: the order header is named `vw_SalesOrderHdr` with a `vw_` prefix even though it is actually a table, while the order detail table is named `ord_line_item` with an `ord_` prefix. This reflects the broader legacy inconsistency where different parts of the system use different table prefixes.

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
> In `tblProduct`, the legacy deprecated fields are `prod_num`, `item_desc`, and `unit_cost`.

`prod_num` (`VARCHAR 20`) is an old legacy product number. It has been superseded by `strSKU` and is retained only for historical reporting, so it should be avoided in new code.

`item_desc` (`VARCHAR 500`) is an old truncated description. It has been superseded by `strDescription`, and the data dictionary…

**Sources retrieved (12):** `parent_chunk_business_glossary.md_3`, `parent_chunk_data_dictionary.txt_5`, `both active and discontinued products with the same SKU pattern→TBLPRODUCT`, `parent_chunk_business_glossary.md_2`, `parent_chunk_data_dictionary.txt_6`, `parent_chunk_data_dictionary.txt_8`, `parent_chunk_data_dictionary.txt_7`, `ORD_LINE_ITEM→TBLPRODUCT`

**Context previews (first 3):**

1. _## Migration Priority Guidelines  ### Critical Path (Must Migrate First) 1. **tblCustomer** - Required for all orders 2. **tblProduct** - Required for line items and inventory 3. **vw_SalesOrderHdr** …_

2. _strCategory (VARCHAR 100)     - Product category     - Hierarchical: "Clothing > Shirts > Casual" strBrand (VARCHAR 100) - Brand or manufacturer name - Free text field dtmIntroduced (DATETIME) - Produ…_

3. _Business concept 'both active and discontinued products with the same SKU pattern' is implemented by physical table TBLPRODUCT (columns: intProdID, strSKU, strName, strDescription, fltPrice, intStockQ…_

---

### ✅ 18 — How are shipping carriers configured in the system?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.2613 | **Gate:** `proceed`

**Expected answer:**
> Shipping carriers are stored in the tblShippingCarrier table with CarrierID, CarrierName, CarrierCode (for API integration), TrackingURL (with {TRACKING_NUM} placeholder), and bolActive flag. Only carriers with bolActive=1 should be offered during checkout.

**System answer:**
> Shipping carriers are configured as master/reference data in the `tblShippingCarrier` table, which implements the business concept “Shipping carrier master data.”

From the retrieved context, the carrier configuration consists of these fields in `TBLSHIPPINGCARRIER`:
`CarrierID`, `CarrierName`, `CarrierCode`, `TrackingURL`, and `bolActive`.

The glossary also describes a shipping carrier as a thir…

**Sources retrieved (12):** `Shipping carrier master data→TBLSHIPPINGCARRIER`, `parent_chunk_data_dictionary.txt_7`, `parent_chunk_business_glossary.md_3`, `parent_chunk_business_glossary.md_2`, `parent_chunk_business_glossary.md_0`, `parent_chunk_data_dictionary.txt_4`, `parent_chunk_data_dictionary.txt_6`, `parent_chunk_data_dictionary.txt_5`

**Context previews (first 3):**

1. _Business concept 'Shipping carrier master data' is implemented by physical table TBLSHIPPINGCARRIER (columns: CarrierID, CarrierName, CarrierCode, TrackingURL, bolActive).…_

2. _Email (VARCHAR 150)     - User email address     - For notifications  LastLogin (DATETIME)     - Last successful login timestamp     - NULL for new users  CreatedDate (DATETIME)     - Account creation…_

3. _## Migration Priority Guidelines  ### Critical Path (Must Migrate First) 1. **tblCustomer** - Required for all orders 2. **tblProduct** - Required for line items and inventory 3. **vw_SalesOrderHdr** …_

---

### ✅ 19 — What is the relationship between User table passwords and security?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0401 | **Gate:** `proceed_with_warning`

**Expected answer:**
> The User table stores password hashes in the PasswordHash field, but uses SHA-256 without salt, making it vulnerable to rainbow table attacks. This is identified as a security issue in the data dictionary. Additionally, the table name 'User' is a SQL reserved word requiring square bracket quoting.

**System answer:**
> The `User` table, which implements the business concept “System users,” contains the `PasswordHash` column. The retrieved context identifies a critical security issue with this field: `User.PasswordHash` uses SHA-256 without salt, which is described as vulnerable to rainbow table attacks. The context also flags `User` as a reserved word table name that must be quoted as `[User]`, but the security-…

**Sources retrieved (12):** `parent_chunk_business_glossary.md_3`, `parent_chunk_data_dictionary.txt_7`, `System users→USER`, `parent_chunk_data_dictionary.txt_8`, `parent_chunk_business_glossary.md_2`, `Unknown→TBLPAYMENT`, `parent_chunk_data_dictionary.txt_6`, `parent_chunk_data_dictionary.txt_4`

**Context previews (first 3):**

1. _## Migration Priority Guidelines  ### Critical Path (Must Migrate First) 1. **tblCustomer** - Required for all orders 2. **tblProduct** - Required for line items and inventory 3. **vw_SalesOrderHdr** …_

2. _Email (VARCHAR 150)     - User email address     - For notifications  LastLogin (DATETIME)     - Last successful login timestamp     - NULL for new users  CreatedDate (DATETIME)     - Account creation…_

3. _Business concept 'System users' is implemented by physical table USER (columns: UserID, UserName, PasswordHash, UserRole, Email, LastLogin, CreatedDate).…_

---

### ✅ 20 — What fields in vw_SalesOrderHdr use the 'flt' Hungarian notation prefix and what do they store?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.9078 | **Gate:** `proceed`

**Expected answer:**
> The vw_SalesOrderHdr table uses the 'flt' (float) prefix for three monetary fields: fltSubTotal (line item subtotal before tax), fltTaxAmount (calculated tax), and fltTotalAmount (final total including tax and shipping). Despite the 'flt' prefix suggesting floating-point, these are defined as DECIMA…

**System answer:**
> In `vw_SalesOrderHdr`, the fields with the `flt` Hungarian notation prefix are `fltSubTotal`, `fltTaxAmount`, and `fltTotalAmount`.

The retrieved context says the `flt` prefix denotes `float/money (DECIMAL)`, so these are decimal or money-type fields by naming convention. However, the context does not explicitly define what each of those three columns stores beyond their column names. It also not…

**Sources retrieved (12):** `Sales order header records→VW_SALESORDERHDR`, `parent_chunk_business_glossary.md_3`, `parent_chunk_data_dictionary.txt_5`, `parent_chunk_business_glossary.md_2`, `parent_chunk_business_glossary.md_0`, `parent_chunk_data_dictionary.txt_7`, `parent_chunk_data_dictionary.txt_8`, `parent_chunk_data_dictionary.txt_4`

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
> The schema does not use one consistent date/time naming convention.

The legacy convention is Hungarian notation, where `dtm` means a `DATETIME` field. The context gives `dtmIntroduced (DATETIME)` and `dtmDiscontinued (DATETIME)` as examples, and also refers to `dtmRequiredDate` in fulfillment priority rules. However, the migration notes explicitly say these prefixes are inconsistent across the sy…

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
> The schema uses inconsistent table naming patterns.

The prefix patterns shown in the context are `tbl`, `vw_`, `ord_`, and `inv_`, plus some tables with no prefix at all.

`tbl` is the standard table prefix used for regular business tables such as `tblCustomer`, `tblProduct`, `tblPayment`, and `tblOrderStatusHistory`.

`vw_` looks like a view prefix, but in this legacy system it is explicitly use…

**Sources retrieved (12):** `parent_chunk_data_dictionary.txt_5`, `parent_chunk_data_dictionary.txt_8`, `parent_chunk_business_glossary.md_2`, `parent_chunk_data_dictionary.txt_7`, `both active and discontinued products with the same SKU pattern→TBLPRODUCT`, `parent_chunk_business_glossary.md_0`, `parent_chunk_business_glossary.md_3`, `parent_chunk_data_dictionary.txt_4`

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
> For `vw_SalesOrderHdr`, the retrieved context shows both one outbound foreign key and three inbound foreign keys.

`vw_SalesOrderHdr` references `TBLCUSTOMER` through `INTCUSTID -> TBLCUSTOMER.STRCUSTID`. The business concept mapping for `VW_SALESORDERHDR` identifies `intCustID` and `lngOrderID` as columns on this table, and the legacy notes add that `intCustID` is named like an integer but is act…

**Sources retrieved (12):** `VW_SALESORDERHDR→TBLCUSTOMER`, `ORD_LINE_ITEM→VW_SALESORDERHDR`, `TBLPAYMENT→VW_SALESORDERHDR`, `TBLORDERSTATUSHISTORY→VW_SALESORDERHDR`, `parent_chunk_data_dictionary.txt_5`, `parent_chunk_data_dictionary.txt_7`, `parent_chunk_business_glossary.md_3`, `parent_chunk_business_glossary.md_2`

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
> The retrieved context only answers this partially.

For SKU handling, the product master uses `tblProduct.strSKU` as the current product identifier field. The older field `prod_num` is marked as deprecated and “superseded by `strSKU`,” and is retained only for historical reporting. In `ord_line_item`, `product_code` is a redundant copy of `tblProduct.strSKU`, added for reporting performance, and i…

**Sources retrieved (12):** `parent_chunk_business_glossary.md_0`, `parent_chunk_business_glossary.md_2`, `parent_chunk_data_dictionary.txt_4`, `parent_chunk_data_dictionary.txt_5`, `parent_chunk_business_glossary.md_3`, `both active and discontinued products with the same SKU pattern→TBLPRODUCT`, `parent_chunk_data_dictionary.txt_6`, `parent_chunk_data_dictionary.txt_8`

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
> The migration documentation identifies critical issues in several areas.

For referential integrity, some `ord_line_item.prod_id` values point to non-existent products, some orders reference customers in `tblCustomer` who are marked inactive, and `inv_txn_log.user_id` has no foreign key constraint.

For data consistency, `tblProduct` contains both active and discontinued products using the same SK…

**Sources retrieved (12):** `parent_chunk_business_glossary.md_3`, `parent_chunk_data_dictionary.txt_8`, `parent_chunk_business_glossary.md_0`, `parent_chunk_business_glossary.md_2`, `parent_chunk_data_dictionary.txt_4`, `parent_chunk_data_dictionary.txt_5`, `parent_chunk_data_dictionary.txt_6`, `parent_chunk_data_dictionary.txt_7`

**Context previews (first 3):**

1. _## Migration Priority Guidelines  ### Critical Path (Must Migrate First) 1. **tblCustomer** - Required for all orders 2. **tblProduct** - Required for line items and inventory 3. **vw_SalesOrderHdr** …_

2. _CardNumberText (VARCHAR 100)     - SECURITY ISSUE: Full card number stored as text! - Should be tokenized - Contains unencrypted PAN (Primary Account Number) CardHolderName (VARCHAR 100) - Cardholder …_

3. _# CustomerMaster E-Commerce System - Business Glossary  ## Document Overview **System**: CustomerMaster v3.2.1 (Legacy) **Last Updated**: March 2015 **Purpose**: Business terminology definitions for d…_

---

## Anomalies & Observations

No anomalies detected. All questions grounded with acceptable RAGAS scores.
