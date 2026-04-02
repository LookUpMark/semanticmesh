# AB-06 — 06_edgecases_legacy — Run Analysis

**Timestamp:** 2026-03-31 07:10:03  
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
| Chunk size / overlap | `128 / 16` |
| ER similarity threshold | `0.75` |

## Builder Results

| Metric | Value |
|--------|-------|
| Triplets extracted | 509 |
| Entities resolved | 287 |
| Tables parsed | 10 |
| Tables completed | 10 |

## Query Evaluation Summary

| Metric | Value |
|--------|-------|
| Questions | 25 |
| Grounded | **25/25 (100%)** |
| Avg GT Coverage | 100% |
| Avg Top Score | 0.6344 |
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
> The `tblCustomer` table stores customer master data from the legacy CRM system. It is the customer master table for the `CustomerMaster` business concept and contains canonical customer attributes including customer ID, full name, email, region, country, active flag, and notes. In business terms, it stores customers defined as individuals or organizations that have purchased products or services f…

**Sources retrieved (12):** `parent_chunk_data_dictionary.txt_4`, `parent_chunk_business_glossary.md_0`, `Customer Master→TBLCUSTOMER`, `parent_chunk_data_dictionary.txt_5`, `parent_chunk_business_glossary.md_3`, `parent_chunk_data_dictionary.txt_7`, `VW_SALESORDERHDR→TBLCUSTOMER`, `parent_chunk_business_glossary.md_2`

**Context previews (first 3):**

1. _================================================================================ CUSTOMERMASTER DATABASE - DATA DICTIONARY =============================================================================…_

2. _# CustomerMaster E-Commerce System - Business Glossary  ## Document Overview **System**: CustomerMaster v3.2.1 (Legacy) **Last Updated**: March 2015 **Purpose**: Business terminology definitions for d…_

3. _Business concept 'Customer Master' — The table is explicitly described as a customer master table and contains canonical customer attributes such as customer ID, full name, email, region, country, act…_

---

### ✅ 2 — How are customers identified in the legacy system?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.8295 | **Gate:** `proceed`

**Expected answer:**
> Customers are identified by strCustID, which is a VARCHAR(50) field containing alphanumeric customer codes inherited from an AS/400 system. These codes follow formats like C-XXXXX or REG-XXXX and can contain letters, numbers, and hyphens.

**System answer:**
> In the legacy system, customers are identified primarily by `tblCustomer.strCustID`.

`strCustID` is the primary key of `tblCustomer` and is the unique customer code. It is an alphanumeric identifier inherited from the AS/400 system, stored as `VARCHAR(50)`, and its documented format is `C-XXXXX` or `REG-XXXX`. It can contain letters, numbers, and hyphens, and it is `NOT NULL` and `UNIQUE`.

The b…

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
> Order header information is stored in `VW_SALESORDERHDR`, described as the implementation of the business concept “Sales order header records.”

The context shows `lngOrderID` as the order identifier column, and other tables reference `VW_SALESORDERHDR.lngOrderID` via foreign keys (`ORD_LINE_ITEM.ORD_ID` and `TBLORDERSTATUSHISTORY.OrderID`, and also `TBLPAYMENT.ORDERID`). However, the retrieved co…

**Sources retrieved (12):** `Sales order header records→VW_SALESORDERHDR`, `parent_chunk_data_dictionary.txt_5`, `parent_chunk_data_dictionary.txt_7`, `parent_chunk_data_dictionary.txt_4`, `parent_chunk_business_glossary.md_3`, `parent_chunk_business_glossary.md_0`, `Order line items→ORD_LINE_ITEM`, `Audit log of order status changes→TBLORDERSTATUSHISTORY`

**Context previews (first 3):**

1. _Business concept 'Sales order header records' is implemented by physical table VW_SALESORDERHDR (columns: lngOrderID, intCustID, dtmOrderDate, dtmShipDate, dtmRequiredDate, strOrderStatus, fltSubTotal…_

2. _strCategory (VARCHAR 100)     - Product category     - Hierarchical: "Clothing > Shirts > Casual" strBrand (VARCHAR 100) - Brand or manufacturer name - Free text field dtmIntroduced (DATETIME) - Produ…_

3. _Email (VARCHAR 150)     - User email address     - For notifications  LastLogin (DATETIME)     - Last successful login timestamp     - NULL for new users  CreatedDate (DATETIME)     - Account creation…_

---

### ✅ 4 — Which table in the schema uses a SQL reserved word as its name?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.5119 | **Gate:** `proceed`

**Expected answer:**
> The schema includes two tables that use SQL reserved words: 'Group' (for product categories) and 'User' (for system users). These require square bracket quoting [Group] and [User] in SQL queries to avoid syntax errors.

**System answer:**
> The schema uses two SQL reserved words as table names: `Group` and `User`. The context says both are reserved words and must be quoted as `[Group]` and `[User]`.

**Sources retrieved (12):** `parent_chunk_business_glossary.md_2`, `parent_chunk_data_dictionary.txt_6`, `parent_chunk_data_dictionary.txt_8`, `parent_chunk_data_dictionary.txt_5`, `parent_chunk_data_dictionary.txt_4`, `Category Hierarchy→GROUP`, `parent_chunk_business_glossary.md_0`, `parent_chunk_business_glossary.md_3`

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
> `vw_SalesOrderHdr` references `tblCustomer` through a foreign key relationship: `vw_SalesOrderHdr.intCustID` -> `tblCustomer.strCustID`.

From the context, this means each sales order header record is linked to a customer master record in `tblCustomer`. The `vw_SalesOrderHdr` table contains the sales order header data, including `lngOrderID`, `intCustID`, order dates, status, and amounts, while `t…

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
> The inventory transaction log table `inv_txn_log` uses a heavily abbreviated naming convention. It also follows the `inv_` table prefix pattern used in the legacy system.

**Sources retrieved (12):** `parent_chunk_data_dictionary.txt_6`, `Inventory Transaction Log→INV_TXN_LOG`, `parent_chunk_business_glossary.md_2`, `parent_chunk_data_dictionary.txt_7`, `parent_chunk_business_glossary.md_3`, `parent_chunk_data_dictionary.txt_4`, `INV_TXN_LOG→TBLPRODUCT`, `parent_chunk_data_dictionary.txt_8`

**Context previews (first 3):**

1. _qty (INT)     - Quantity ordered     - Must be positive integer  amt (DECIMAL 10,2)     - Line item total amount (qty * unit_price)     - At time of order (snapshotted, not current price)  disc_amt (D…_

2. _Business concept 'Inventory Transaction Log' — The table name, primary fields, and provenance all indicate an inventory transaction log with transaction type, quantity, timestamp, product reference, a…_

3. _## Legacy System Quirks  ### Hungarian Notation The legacy system uses Hungarian notation prefixes: - `str` = string (VARCHAR) - `int` = integer (INT) - `lng` = long integer (INT) - `flt` = float/mone…_

---

### ✅ 7 — What data quality issue exists in the tblProduct unit_cost field?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.8594 | **Gate:** `proceed`

**Expected answer:**
> The tblProduct.unit_cost field has an inappropriate data type - it's defined as VARCHAR(20) instead of DECIMAL. This field contains currency symbols like '$19.99' which require parsing before calculations can be performed, making it unusable for mathematical operations without transformation.

**System answer:**
> The `tblProduct.unit_cost` field has a data quality issue because it is stored as `VARCHAR 20` instead of a numeric type. The context describes it as an old deprecated field where cost is stored as a string, marked as a bug, and says it should be `DECIMAL`. It also contains currency symbols such as `"$19.99"`, so the values must be parsed before calculations.

**Sources retrieved (12):** `parent_chunk_business_glossary.md_3`, `parent_chunk_business_glossary.md_2`, `parent_chunk_data_dictionary.txt_8`, `parent_chunk_data_dictionary.txt_6`, `parent_chunk_data_dictionary.txt_5`, `Copy of tblProduct.strSKU→TBLPRODUCT`, `parent_chunk_data_dictionary.txt_7`, `ORD_LINE_ITEM→TBLPRODUCT`

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
> `ord_line_item` handles product data redundancy by storing both the normalized product reference and denormalized product attributes in the same row.

It has `prod_id`, which is a foreign key to `TBLPRODUCT.INTPRODID`, so each line item still links to the master product record. But it also stores `product_code` and `item_name` directly in `ORD_LINE_ITEM`. The context describes these as redundant/d…

**Sources retrieved (12):** `ORD_LINE_ITEM→TBLPRODUCT`, `Order line items→ORD_LINE_ITEM`, `parent_chunk_business_glossary.md_3`, `ORD_LINE_ITEM→VW_SALESORDERHDR`, `parent_chunk_business_glossary.md_2`, `parent_chunk_data_dictionary.txt_8`, `parent_chunk_data_dictionary.txt_6`, `parent_chunk_business_glossary.md_0`

**Context previews (first 3):**

1. _Relationship: ORD_LINE_ITEM references TBLPRODUCT via foreign key PROD_ID -> TBLPRODUCT.INTPRODID.…_

2. _Business concept 'Order line items' — The table is the physical implementation of order line items: it links exactly one order to exactly one product per row and stores quantity, line amount, discount…_

3. _## Migration Priority Guidelines  ### Critical Path (Must Migrate First) 1. **tblCustomer** - Required for all orders 2. **tblProduct** - Required for line items and inventory 3. **vw_SalesOrderHdr** …_

---

### ✅ 9 — What are the valid values for the strOrderStatus field in vw_SalesOrderHdr?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.9131 | **Gate:** `proceed`

**Expected answer:**
> The strOrderStatus field accepts three values enforced by a CHECK constraint: 'PENDING' (order received but not shipped), 'SHIPPED' (order has been shipped to customer), and 'CANCELLED' (order cancelled before shipping).

**System answer:**
> The retrieved context does not provide an enumerated list of valid values for `vw_SalesOrderHdr.strOrderStatus`.

What the context does confirm is that `strOrderStatus` is a column in `VW_SALESORDERHDR`, and order status changes are tracked in `tblOrderStatusHistory` through `OldStatus` and `NewStatus`, both defined as `VARCHAR(20)`. It also states that `OldStatus` is `NULL` for the initial status…

**Sources retrieved (12):** `parent_chunk_data_dictionary.txt_5`, `Sales order header records→VW_SALESORDERHDR`, `parent_chunk_data_dictionary.txt_7`, `parent_chunk_business_glossary.md_0`, `parent_chunk_business_glossary.md_3`, `parent_chunk_business_glossary.md_2`, `TBLORDERSTATUSHISTORY→VW_SALESORDERHDR`, `VW_SALESORDERHDR→TBLCUSTOMER`

**Context previews (first 3):**

1. _strCategory (VARCHAR 100)     - Product category     - Hierarchical: "Clothing > Shirts > Casual" strBrand (VARCHAR 100) - Brand or manufacturer name - Free text field dtmIntroduced (DATETIME) - Produ…_

2. _Business concept 'Sales order header records' is implemented by physical table VW_SALESORDERHDR (columns: lngOrderID, intCustID, dtmOrderDate, dtmShipDate, dtmRequiredDate, strOrderStatus, fltSubTotal…_

3. _Email (VARCHAR 150)     - User email address     - For notifications  LastLogin (DATETIME)     - Last successful login timestamp     - NULL for new users  CreatedDate (DATETIME)     - Account creation…_

---

### ✅ 10 — Which table stores payment information and what security issue does it have?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0845 | **Gate:** `proceed_with_warning`

**Expected answer:**
> Payment information is stored in the tblPayment table. The table has a critical security issue: the CardNumberText field stores full unencrypted credit card numbers as VARCHAR(100), which is a PCI compliance violation. The system also lacks proper tokenization and encryption at rest.

**System answer:**
> Payment information is stored in `tblPayment` (`TBLPAYMENT`). The key security issue is that its `CardNumberText` column stores full payment card numbers as unencrypted text/plaintext PAN, when it should be tokenized. The context also notes this as a critical security violation and says the payment data lacks PCI-DSS-required protections such as tokenization and encryption at rest.

**Sources retrieved (12):** `parent_chunk_business_glossary.md_3`, `parent_chunk_data_dictionary.txt_7`, `parent_chunk_data_dictionary.txt_8`, `Payment gateway auth code→TBLPAYMENT`, `parent_chunk_data_dictionary.txt_4`, `parent_chunk_business_glossary.md_0`, `TBLPAYMENT→VW_SALESORDERHDR`, `parent_chunk_business_glossary.md_2`

**Context previews (first 3):**

1. _## Migration Priority Guidelines  ### Critical Path (Must Migrate First) 1. **tblCustomer** - Required for all orders 2. **tblProduct** - Required for line items and inventory 3. **vw_SalesOrderHdr** …_

2. _Email (VARCHAR 150)     - User email address     - For notifications  LastLogin (DATETIME)     - Last successful login timestamp     - NULL for new users  CreatedDate (DATETIME)     - Account creation…_

3. _CardNumberText (VARCHAR 100)     - SECURITY ISSUE: Full card number stored as text! - Should be tokenized - Contains unencrypted PAN (Primary Account Number) CardHolderName (VARCHAR 100) - Cardholder …_

---

### ✅ 11 — What is the purpose of the bolActive field in tblCustomer and tblProduct?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.9646 | **Gate:** `proceed`

**Expected answer:**
> The bolActive field (using Hungarian notation 'bol' for boolean/bit) is a flag indicating whether a record is active. In tblCustomer, it marks whether customers are included in marketing (1=active, 0=inactive). In tblProduct, it indicates product availability (1=available for sale, 0=discontinued).

**System answer:**
> For `tblCustomer`, `bolActive` is the customer active/inactive flag. The glossary states that customers “can be marked as inactive (`bolActive = 0`) but are never deleted,” and the `Customer Master` concept also lists an “active flag” among the canonical customer attributes.

For `tblProduct`, the retrieved context does not explicitly define the purpose of `bolActive`. It only shows that `tblProdu…

**Sources retrieved (12):** `parent_chunk_data_dictionary.txt_4`, `parent_chunk_data_dictionary.txt_7`, `parent_chunk_business_glossary.md_0`, `parent_chunk_business_glossary.md_3`, `Customer Master→TBLCUSTOMER`, `parent_chunk_business_glossary.md_2`, `parent_chunk_data_dictionary.txt_5`, `Copy of tblProduct.strSKU→TBLPRODUCT`

**Context previews (first 3):**

1. _================================================================================ CUSTOMERMASTER DATABASE - DATA DICTIONARY =============================================================================…_

2. _Email (VARCHAR 150)     - User email address     - For notifications  LastLogin (DATETIME)     - Last successful login timestamp     - NULL for new users  CreatedDate (DATETIME)     - Account creation…_

3. _# CustomerMaster E-Commerce System - Business Glossary  ## Document Overview **System**: CustomerMaster v3.2.1 (Legacy) **Last Updated**: March 2015 **Purpose**: Business terminology definitions for d…_

---

### ✅ 12 — How are inventory transactions tracked in the system?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.8263 | **Gate:** `proceed`

**Expected answer:**
> Inventory transactions are tracked in the inv_txn_log table, which records all stock movements. Each transaction has a type (txn_type): 'IN' for receipts, 'OUT' for shipments, and 'ADJ' for corrections. The table uses heavily abbreviated field names and references products via prod_id.

**System answer:**
> Inventory transactions are tracked through the `INV_TXN_LOG` / `inv_txn_log` table, which implements the business concept of the “Inventory Transaction Log.” The context describes this table as the inventory audit trail for product-related inventory transactions.

At the schema level, each inventory transaction is recorded as one row with these fields: `txn_id`, `prod_id`, `txn_type`, `qty`, `txn_…

**Sources retrieved (12):** `Inventory Transaction Log→INV_TXN_LOG`, `parent_chunk_data_dictionary.txt_6`, `parent_chunk_business_glossary.md_3`, `parent_chunk_business_glossary.md_2`, `parent_chunk_business_glossary.md_0`, `parent_chunk_data_dictionary.txt_7`, `parent_chunk_data_dictionary.txt_4`, `parent_chunk_data_dictionary.txt_5`

**Context previews (first 3):**

1. _Business concept 'Inventory Transaction Log' — The table name, primary fields, and provenance all indicate an inventory transaction log with transaction type, quantity, timestamp, product reference, a…_

2. _qty (INT)     - Quantity ordered     - Must be positive integer  amt (DECIMAL 10,2)     - Line item total amount (qty * unit_price)     - At time of order (snapshotted, not current price)  disc_amt (D…_

3. _## Migration Priority Guidelines  ### Critical Path (Must Migrate First) 1. **tblCustomer** - Required for all orders 2. **tblProduct** - Required for line items and inventory 3. **vw_SalesOrderHdr** …_

---

### ✅ 13 — What is the self-referencing relationship in the Group table?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.7294 | **Gate:** `proceed`

**Expected answer:**
> The Group table has a self-referencing foreign key where ParentGroupID references GroupID, creating a hierarchical structure for product categories. A NULL ParentGroupID indicates a top-level group, while non-NULL values create nested category levels.

**System answer:**
> The `GROUP` table is self-referencing through `ParentGroupID`. Specifically, `GROUP.PARENTGROUPID` is a foreign key to `GROUP.GROUPID`, creating a parent-child hierarchy. This is the relationship that implements the `Category Hierarchy` concept, where each group/category can have another group as its parent.

**Sources retrieved (12):** `Category Hierarchy→GROUP`, `GROUP→GROUP`, `parent_chunk_data_dictionary.txt_6`, `parent_chunk_business_glossary.md_2`, `parent_chunk_business_glossary.md_3`, `parent_chunk_data_dictionary.txt_8`, `Category Hierarchy`, `parent_chunk_data_dictionary.txt_7`

**Context previews (first 3):**

1. _Business concept 'Category Hierarchy' — The table is a self-referencing hierarchy with GroupID, ParentGroupID, GroupName, and IsActive, which aligns strongly with a navigable category/group structure.…_

2. _Relationship: GROUP references GROUP via foreign key PARENTGROUPID -> GROUP.GROUPID.…_

3. _qty (INT)     - Quantity ordered     - Must be positive integer  amt (DECIMAL 10,2)     - Line item total amount (qty * unit_price)     - At time of order (snapshotted, not current price)  disc_amt (D…_

---

### ✅ 14 — What migration compatibility columns exist in tblCustomer?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.9031 | **Gate:** `proceed`

**Expected answer:**
> The tblCustomer table includes cust_id (INT) and customer_name (VARCHAR 255) as migration compatibility columns alongside the legacy strCustID and strFullName fields. These are intended for the new ERP system that will use integer IDs and standardized naming conventions.

**System answer:**
> The retrieved context does not explicitly identify any `tblCustomer` columns as migration compatibility columns.

What the context does say is that `tblCustomer` / `TBLCUSTOMER` is the customer master table and includes these columns: `strCustID`, `strFullName`, `strEmail`, `strRegion`, `strCountry`, `dtmCreated`, `dtmLastModified`, `bolActive`, `cust_id`, `customer_name`, and `txtNotes`. It also …

**Sources retrieved (12):** `Customer Master→TBLCUSTOMER`, `parent_chunk_business_glossary.md_3`, `parent_chunk_data_dictionary.txt_4`, `parent_chunk_business_glossary.md_0`, `parent_chunk_business_glossary.md_2`, `parent_chunk_data_dictionary.txt_5`, `VW_SALESORDERHDR→TBLCUSTOMER`, `parent_chunk_data_dictionary.txt_8`

**Context previews (first 3):**

1. _Business concept 'Customer Master' — The table is explicitly described as a customer master table and contains canonical customer attributes such as customer ID, full name, email, region, country, act…_

2. _## Migration Priority Guidelines  ### Critical Path (Must Migrate First) 1. **tblCustomer** - Required for all orders 2. **tblProduct** - Required for line items and inventory 3. **vw_SalesOrderHdr** …_

3. _================================================================================ CUSTOMERMASTER DATABASE - DATA DICTIONARY =============================================================================…_

---

### ✅ 15 — How does the system handle order status history tracking?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.3202 | **Gate:** `proceed`

**Expected answer:**
> Order status changes are tracked in the tblOrderStatusHistory table, which creates an audit record for each status transition. Each history record includes OrderID, OldStatus, NewStatus, ChangedByUser, ChangedDate, and ChangeReason fields, providing a complete audit trail of order workflow.

**System answer:**
> The system tracks order status history with the physical table `TBLORDERSTATUSHISTORY` / `tblOrderStatusHistory`, which implements the business concept “Audit log of order status changes.” Its purpose is to store an audit trail of every status change for an order.

Each history row contains:
`HistoryID` as the auto-increment primary key,
`OrderID` as the foreign key to `VW_SALESORDERHDR.lngOrderID…

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
> The inconsistency is that the order-related tables use different prefixes. `vw_SalesOrderHdr` uses a `vw_` prefix even though the context says it is actually a table, while `ord_line_item` uses an `ord_` prefix. The context identifies this as part of the system’s table naming inconsistency.

**Sources retrieved (12):** `parent_chunk_business_glossary.md_2`, `parent_chunk_data_dictionary.txt_5`, `parent_chunk_data_dictionary.txt_8`, `parent_chunk_business_glossary.md_3`, `parent_chunk_data_dictionary.txt_6`, `parent_chunk_business_glossary.md_0`, `parent_chunk_data_dictionary.txt_4`, `Order line items→ORD_LINE_ITEM`

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

`prod_num` (`VARCHAR 20`) is an old legacy product number. It has been superseded by `strSKU` and is retained only for historical reporting, so it should not be used for new code.

`item_desc` (`VARCHAR 500`) is an old truncated description. It has been superseded by `strDescription`, so it should also be …

**Sources retrieved (12):** `parent_chunk_business_glossary.md_3`, `parent_chunk_data_dictionary.txt_5`, `Copy of tblProduct.strSKU→TBLPRODUCT`, `parent_chunk_business_glossary.md_2`, `parent_chunk_data_dictionary.txt_6`, `parent_chunk_data_dictionary.txt_8`, `ORD_LINE_ITEM→TBLPRODUCT`, `Customer Master→TBLCUSTOMER`

**Context previews (first 3):**

1. _## Migration Priority Guidelines  ### Critical Path (Must Migrate First) 1. **tblCustomer** - Required for all orders 2. **tblProduct** - Required for line items and inventory 3. **vw_SalesOrderHdr** …_

2. _strCategory (VARCHAR 100)     - Product category     - Hierarchical: "Clothing > Shirts > Casual" strBrand (VARCHAR 100) - Brand or manufacturer name - Free text field dtmIntroduced (DATETIME) - Produ…_

3. _Business concept 'Copy of tblProduct.strSKU' is implemented by physical table TBLPRODUCT (columns: intProdID, strSKU, strName, strDescription, fltPrice, intStockQty, bolActive, strCategory, strBrand, …_

---

### ✅ 18 — How are shipping carriers configured in the system?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.2613 | **Gate:** `proceed`

**Expected answer:**
> Shipping carriers are stored in the tblShippingCarrier table with CarrierID, CarrierName, CarrierCode (for API integration), TrackingURL (with {TRACKING_NUM} placeholder), and bolActive flag. Only carriers with bolActive=1 should be offered during checkout.

**System answer:**
> Shipping carriers are configured as reference/master data in the physical table `TBLSHIPPINGCARRIER` / `tblShippingCarrier`, which implements the business concept “Shipping carrier master data.”

The carrier configuration consists of these columns:
`CarrierID`, `CarrierName`, `CarrierCode`, `TrackingURL`, and `bolActive`.

From the glossary, a shipping carrier is a third-party logistics provider r…

**Sources retrieved (12):** `Shipping carrier master data→TBLSHIPPINGCARRIER`, `parent_chunk_data_dictionary.txt_7`, `parent_chunk_business_glossary.md_3`, `parent_chunk_business_glossary.md_2`, `parent_chunk_business_glossary.md_0`, `parent_chunk_data_dictionary.txt_5`, `Sales order header records→VW_SALESORDERHDR`, `System users→USER`

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
> The `User` table, which implements the business concept of system users, stores passwords in the `PasswordHash` column. The retrieved context identifies this as a security issue: `User.PasswordHash` uses SHA-256 without salt, which makes it vulnerable to rainbow table attacks. The context also notes that `User` is a reserved word and must be quoted as `[User]`, but the security-relevant fact is sp…

**Sources retrieved (12):** `parent_chunk_business_glossary.md_3`, `parent_chunk_data_dictionary.txt_7`, `System users→USER`, `parent_chunk_data_dictionary.txt_8`, `parent_chunk_business_glossary.md_2`, `parent_chunk_data_dictionary.txt_6`, `parent_chunk_data_dictionary.txt_4`, `parent_chunk_business_glossary.md_0`

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
> In `VW_SALESORDERHDR`, the fields with the `flt` Hungarian notation prefix are `fltSubTotal`, `fltTaxAmount`, and `fltTotalAmount`.

From the notation guidance, `flt` denotes a float/money field stored as `DECIMAL`, so these columns store monetary values. Based on their names, they store the order subtotal, tax amount, and total amount respectively. The context also notes a data quality issue spec…

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
> The schema does not use a single consistent date/time naming convention. The retrieved context shows at least two patterns.

In the legacy Hungarian notation style, datetime fields use the `dtm` prefix, where `dtm` means `DATETIME`. Examples include `dtmIntroduced`, `dtmDiscontinued`, and the glossary’s reference to `dtmRequiredDate`. The data dictionary for `tblCustomer` also states that the lega…

**Sources retrieved (12):** `parent_chunk_data_dictionary.txt_5`, `parent_chunk_business_glossary.md_2`, `parent_chunk_data_dictionary.txt_4`, `parent_chunk_data_dictionary.txt_8`, `parent_chunk_data_dictionary.txt_7`, `parent_chunk_data_dictionary.txt_6`, `parent_chunk_business_glossary.md_0`, `Inventory Transaction Log→INV_TXN_LOG`

**Context previews (first 3):**

1. _strCategory (VARCHAR 100)     - Product category     - Hierarchical: "Clothing > Shirts > Casual" strBrand (VARCHAR 100) - Brand or manufacturer name - Free text field dtmIntroduced (DATETIME) - Produ…_

2. _## Legacy System Quirks  ### Hungarian Notation The legacy system uses Hungarian notation prefixes: - `str` = string (VARCHAR) - `int` = integer (INT) - `lng` = long integer (INT) - `flt` = float/mone…_

3. _================================================================================ CUSTOMERMASTER DATABASE - DATA DICTIONARY =============================================================================…_

---

### ✅ 22 — What table prefix patterns exist in the schema and what do they indicate?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.1376 | **Gate:** `proceed_with_warning`

**Expected answer:**
> The schema uses multiple inconsistent table prefixes: 'tbl' for standard tables (tblCustomer, tblProduct, tblPayment, tblShippingCarrier, tblOrderStatusHistory), 'vw_' for a misnamed table (vw_SalesOrderHdr), and domain-specific prefixes 'ord_' (ord_line_item) and 'inv_' (inv_txn_log). Two tables (G…

**System answer:**
> The schema uses inconsistent table naming patterns. The documented table prefix patterns are `tbl`, `vw_`, `ord_`, and `inv_`, plus some tables with no prefix at all.

`tbl` appears to be the standard verbose table prefix, as seen in names like `tblCustomer`, `tblProduct`, `tblPayment`, and `tblOrderStatusHistory`. `vw_` appears in `vw_SalesOrderHdr`, but the context explicitly says these are actu…

**Sources retrieved (12):** `parent_chunk_data_dictionary.txt_5`, `Category Hierarchy→GROUP`, `parent_chunk_data_dictionary.txt_8`, `parent_chunk_business_glossary.md_2`, `parent_chunk_data_dictionary.txt_7`, `parent_chunk_business_glossary.md_0`, `parent_chunk_business_glossary.md_3`, `parent_chunk_data_dictionary.txt_4`

**Context previews (first 3):**

1. _strCategory (VARCHAR 100)     - Product category     - Hierarchical: "Clothing > Shirts > Casual" strBrand (VARCHAR 100) - Brand or manufacturer name - Free text field dtmIntroduced (DATETIME) - Produ…_

2. _Business concept 'Category Hierarchy' — The table is a self-referencing hierarchy with GroupID, ParentGroupID, GroupName, and IsActive, which aligns strongly with a navigable category/group structure.…_

3. _CardNumberText (VARCHAR 100)     - SECURITY ISSUE: Full card number stored as text! - Should be tokenized - Contains unencrypted PAN (Primary Account Number) CardHolderName (VARCHAR 100) - Cardholder …_

---

### ✅ 23 — What foreign key relationships exist for the vw_SalesOrderHdr table?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.9902 | **Gate:** `proceed`

**Expected answer:**
> The vw_SalesOrderHdr table has one explicit foreign key constraint: intCustID references tblCustomer.strCustID. Implicit relationships (not enforced by FK constraints) include tblPayment.OrderID, tblOrderStatusHistory.OrderID, and ord_line_item.ord_id all referencing vw_SalesOrderHdr.lngOrderID.

**System answer:**
> For `vw_SalesOrderHdr`, the retrieved context shows one outgoing foreign key and three incoming foreign keys.

`vw_SalesOrderHdr` references `tblCustomer` through `intCustID -> tblCustomer.strCustID`. The glossary also notes that customer records are stored in `tblCustomer`, and the migration notes say the Hungarian notation is inconsistent, so `intCustID` is actually a `VARCHAR` even though its n…

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
> In the retrieved context, the current product SKU is `tblProduct.strSKU`. The older field `prod_num` is explicitly marked as deprecated and “superseded by `strSKU`,” and `ord_line_item.product_code` is described as a redundant copy of `tblProduct.strSKU` kept for reporting performance and noted as potentially out of sync with the master product record.

For SKU format, the context does not give a …

**Sources retrieved (12):** `parent_chunk_business_glossary.md_0`, `parent_chunk_business_glossary.md_2`, `parent_chunk_data_dictionary.txt_4`, `parent_chunk_data_dictionary.txt_5`, `parent_chunk_business_glossary.md_3`, `parent_chunk_data_dictionary.txt_6`, `Customer Master→TBLCUSTOMER`, `Copy of tblProduct.strSKU→TBLPRODUCT`

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
> The migration review identified several critical issues.

Under referential integrity, some `ord_line_item.prod_id` values point to non-existent products in `tblProduct`, some orders reference customers in `tblCustomer` who are marked inactive, and `inv_txn_log.user_id` has no foreign key constraint.

Under data consistency, `tblProduct` contains both active and discontinued products using the sam…

**Sources retrieved (12):** `parent_chunk_business_glossary.md_3`, `parent_chunk_data_dictionary.txt_8`, `parent_chunk_business_glossary.md_0`, `parent_chunk_business_glossary.md_2`, `parent_chunk_data_dictionary.txt_4`, `parent_chunk_data_dictionary.txt_5`, `Customer Master→TBLCUSTOMER`, `parent_chunk_data_dictionary.txt_6`

**Context previews (first 3):**

1. _## Migration Priority Guidelines  ### Critical Path (Must Migrate First) 1. **tblCustomer** - Required for all orders 2. **tblProduct** - Required for line items and inventory 3. **vw_SalesOrderHdr** …_

2. _CardNumberText (VARCHAR 100)     - SECURITY ISSUE: Full card number stored as text! - Should be tokenized - Contains unencrypted PAN (Primary Account Number) CardHolderName (VARCHAR 100) - Cardholder …_

3. _# CustomerMaster E-Commerce System - Business Glossary  ## Document Overview **System**: CustomerMaster v3.2.1 (Legacy) **Last Updated**: March 2015 **Purpose**: Business terminology definitions for d…_

---

## Anomalies & Observations

No anomalies detected. All questions grounded with acceptable RAGAS scores.
