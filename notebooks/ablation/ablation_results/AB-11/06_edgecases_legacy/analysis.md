# AB-11 — 06_edgecases_legacy — Run Analysis

**Timestamp:** 2026-04-01 01:36:52  
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
| ER similarity threshold | `0.65` |

## Builder Results

| Metric | Value |
|--------|-------|
| Triplets extracted | 484 |
| Entities resolved | 47 |
| Tables parsed | 10 |
| Tables completed | 10 |

## Query Evaluation Summary

| Metric | Value |
|--------|-------|
| Questions | 25 |
| Grounded | **25/25 (100%)** |
| Avg GT Coverage | 100% |
| Avg Top Score | 0.6149 |
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
> The `tblCustomer` table stores customer master data from the legacy CRM system. It represents the business entity “Customer,” meaning individuals or organizations that have purchased products or services from the company. The table holds the legacy AS/400 customer identifier (`strCustID`) and customer master attributes such as name, email, region, country, creation and modification dates, active s…

**Sources retrieved (12):** `parent_chunk_data_dictionary.txt_4`, `parent_chunk_business_glossary.md_0`, `parent_chunk_data_dictionary.txt_5`, `parent_chunk_business_glossary.md_3`, `Customer Master→TBLCUSTOMER`, `parent_chunk_data_dictionary.txt_7`, `VW_SALESORDERHDR→TBLCUSTOMER`, `parent_chunk_business_glossary.md_2`

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
> In the legacy CustomerMaster system, customers are identified by `strCustID` in `tblCustomer`. The context describes this as the primary key and the customer’s unique customer code, inherited from the AS/400 system. It is an alphanumeric identifier, stored as `VARCHAR(50)`, in formats such as `C-XXXXX` or `REG-XXXX`, and may contain letters, numbers, and hyphens. It is `NOT NULL` and `UNIQUE`.

Th…

**Sources retrieved (12):** `parent_chunk_business_glossary.md_0`, `parent_chunk_data_dictionary.txt_4`, `parent_chunk_business_glossary.md_2`, `Customer Master→TBLCUSTOMER`, `parent_chunk_data_dictionary.txt_5`, `parent_chunk_business_glossary.md_3`, `parent_chunk_data_dictionary.txt_8`, `parent_chunk_data_dictionary.txt_6`

**Context previews (first 3):**

1. _# CustomerMaster E-Commerce System - Business Glossary  ## Document Overview **System**: CustomerMaster v3.2.1 (Legacy) **Last Updated**: March 2015 **Purpose**: Business terminology definitions for d…_

2. _================================================================================ CUSTOMERMASTER DATABASE - DATA DICTIONARY =============================================================================…_

3. _## Legacy System Quirks  ### Hungarian Notation The legacy system uses Hungarian notation prefixes: - `str` = string (VARCHAR) - `int` = integer (INT) - `lng` = long integer (INT) - `flt` = float/mone…_

---

### ✅ 3 — What table stores order header information and what is its primary key?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.5240 | **Gate:** `proceed`

**Expected answer:**
> Order header information is stored in the vw_SalesOrderHdr table despite the vw_ prefix suggesting it's a view. The primary key is lngOrderID, which is an INT field using the lng (long integer) Hungarian notation prefix.

**System answer:**
> The order header information is stored in `VW_SALESORDERHDR`, which is identified as the sales order header table. Its key order identifier is `lngOrderID`, which is the column referenced by related tables such as `TBLPAYMENT.OrderID`, `TBLORDERSTATUSHISTORY.OrderID`, and `ORD_LINE_ITEM.ORD_ID`. The retrieved context does not explicitly label `lngOrderID` as the primary key, but it functions as th…

**Sources retrieved (12):** `Sales Order→VW_SALESORDERHDR`, `parent_chunk_data_dictionary.txt_5`, `parent_chunk_data_dictionary.txt_7`, `parent_chunk_data_dictionary.txt_4`, `Payment Transaction→TBLPAYMENT`, `parent_chunk_business_glossary.md_3`, `parent_chunk_business_glossary.md_0`, `ORD_LINE_ITEM→VW_SALESORDERHDR`

**Context previews (first 3):**

1. _Business concept 'Sales Order' — The table is explicitly labeled as a sales order header and contains core order lifecycle fields such as order date, ship date, required date, status, and monetary tot…_

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
> `vw_SalesOrderHdr` is related to `tblCustomer` through a foreign key from `vw_SalesOrderHdr.intCustID` to `tblCustomer.strCustID`. This means each sales order header is associated with a customer record in `tblCustomer`.

From the context, `tblCustomer.strCustID` is the primary key and unique customer code, and `vw_SalesOrderHdr` is the sales order header table for core order data. The glossary al…

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
> The inventory transaction log table, `inv_txn_log`, uses a heavily abbreviated naming convention. The broader legacy system also identifies it under the `inv_` table prefix convention.

**Sources retrieved (12):** `parent_chunk_data_dictionary.txt_6`, `parent_chunk_business_glossary.md_2`, `parent_chunk_data_dictionary.txt_7`, `parent_chunk_business_glossary.md_3`, `parent_chunk_data_dictionary.txt_4`, `INV_TXN_LOG→TBLPRODUCT`, `parent_chunk_data_dictionary.txt_8`, `Unknown→INV_TXN_LOG`

**Context previews (first 3):**

1. _qty (INT)     - Quantity ordered     - Must be positive integer  amt (DECIMAL 10,2)     - Line item total amount (qty * unit_price)     - At time of order (snapshotted, not current price)  disc_amt (D…_

2. _## Legacy System Quirks  ### Hungarian Notation The legacy system uses Hungarian notation prefixes: - `str` = string (VARCHAR) - `int` = integer (INT) - `lng` = long integer (INT) - `flt` = float/mone…_

3. _Email (VARCHAR 150)     - User email address     - For notifications  LastLogin (DATETIME)     - Last successful login timestamp     - NULL for new users  CreatedDate (DATETIME)     - Account creation…_

---

### ✅ 7 — What data quality issue exists in the tblProduct unit_cost field?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.8594 | **Gate:** `proceed`

**Expected answer:**
> The tblProduct.unit_cost field has an inappropriate data type - it's defined as VARCHAR(20) instead of DECIMAL. This field contains currency symbols like '$19.99' which require parsing before calculations can be performed, making it unusable for mathematical operations without transformation.

**System answer:**
> The `tblProduct.unit_cost` field has an inappropriate data type issue: it is defined as `VARCHAR 20` even though it represents cost. The context labels this as a bug, says it should be `DECIMAL`, and notes that it contains currency-formatted text such as `"$19.99"`, so it must be parsed before calculations. This is also called out in the migration notes as an example of inappropriate data types.

**Sources retrieved (12):** `parent_chunk_business_glossary.md_3`, `parent_chunk_business_glossary.md_2`, `parent_chunk_data_dictionary.txt_8`, `Unknown→TBLPRODUCT`, `parent_chunk_data_dictionary.txt_6`, `parent_chunk_data_dictionary.txt_5`, `parent_chunk_data_dictionary.txt_7`, `ORD_LINE_ITEM→TBLPRODUCT`

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
> `ord_line_item` stores both the normalized product reference and redundant product attributes.

It links to the product master through `prod_id`, which is a foreign key to `tblProduct.INTPRODID`. In addition, it duplicates product information in two denormalized columns: `product_code` and `item_name`.

`product_code` is a redundant copy of `tblProduct.strSKU`. It exists for reporting performance,…

**Sources retrieved (12):** `ORD_LINE_ITEM→TBLPRODUCT`, `parent_chunk_business_glossary.md_3`, `ORD_LINE_ITEM→VW_SALESORDERHDR`, `parent_chunk_business_glossary.md_2`, `Unknown→ORD_LINE_ITEM`, `parent_chunk_data_dictionary.txt_8`, `parent_chunk_data_dictionary.txt_6`, `parent_chunk_business_glossary.md_0`

**Context previews (first 3):**

1. _Relationship: ORD_LINE_ITEM references TBLPRODUCT via foreign key PROD_ID -> TBLPRODUCT.INTPRODID.…_

2. _## Migration Priority Guidelines  ### Critical Path (Must Migrate First) 1. **tblCustomer** - Required for all orders 2. **tblProduct** - Required for line items and inventory 3. **vw_SalesOrderHdr** …_

3. _Relationship: ORD_LINE_ITEM references VW_SALESORDERHDR via foreign key ORD_ID -> VW_SALESORDERHDR.LNGORDERID.…_

---

### ✅ 9 — What are the valid values for the strOrderStatus field in vw_SalesOrderHdr?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.9131 | **Gate:** `proceed`

**Expected answer:**
> The strOrderStatus field accepts three values enforced by a CHECK constraint: 'PENDING' (order received but not shipped), 'SHIPPED' (order has been shipped to customer), and 'CANCELLED' (order cancelled before shipping).

**System answer:**
> The retrieved context does not provide an enumerated list of valid values for `vw_SalesOrderHdr.strOrderStatus`.

What the context does confirm is:
`strOrderStatus` is a column on `VW_SALESORDERHDR`, described as one of the core order lifecycle fields alongside `dtmOrderDate`, `dtmShipDate`, `dtmRequiredDate`, and the monetary totals.
Order status changes are tracked in `tblOrderStatusHistory`, wh…

**Sources retrieved (12):** `parent_chunk_data_dictionary.txt_5`, `Sales Order→VW_SALESORDERHDR`, `parent_chunk_data_dictionary.txt_7`, `parent_chunk_business_glossary.md_0`, `parent_chunk_business_glossary.md_3`, `parent_chunk_business_glossary.md_2`, `TBLORDERSTATUSHISTORY→VW_SALESORDERHDR`, `VW_SALESORDERHDR→TBLCUSTOMER`

**Context previews (first 3):**

1. _strCategory (VARCHAR 100)     - Product category     - Hierarchical: "Clothing > Shirts > Casual" strBrand (VARCHAR 100) - Brand or manufacturer name - Free text field dtmIntroduced (DATETIME) - Produ…_

2. _Business concept 'Sales Order' — The table is explicitly labeled as a sales order header and contains core order lifecycle fields such as order date, ship date, required date, status, and monetary tot…_

3. _Email (VARCHAR 150)     - User email address     - For notifications  LastLogin (DATETIME)     - Last successful login timestamp     - NULL for new users  CreatedDate (DATETIME)     - Account creation…_

---

### ✅ 10 — Which table stores payment information and what security issue does it have?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.5070 | **Gate:** `proceed`

**Expected answer:**
> Payment information is stored in the tblPayment table. The table has a critical security issue: the CardNumberText field stores full unencrypted credit card numbers as VARCHAR(100), which is a PCI compliance violation. The system also lacks proper tokenization and encryption at rest.

**System answer:**
> Payment information is stored in the `TBLPAYMENT` / `tblPayment` table, which implements the business concept “Payment Transaction.” It contains fields such as `PaymentID`, `OrderID`, `PaymentMethod`, `PaymentDate`, `Amount`, `PaymentStatus`, `CardNumberText`, `CardHolderName`, and `AuthorizationCode`.

The security issue is that `CardNumberText` stores card numbers in plaintext/unencrypted form. …

**Sources retrieved (12):** `Payment Transaction→TBLPAYMENT`, `parent_chunk_business_glossary.md_3`, `parent_chunk_data_dictionary.txt_7`, `parent_chunk_data_dictionary.txt_8`, `parent_chunk_data_dictionary.txt_4`, `parent_chunk_business_glossary.md_0`, `TBLPAYMENT→VW_SALESORDERHDR`, `parent_chunk_business_glossary.md_2`

**Context previews (first 3):**

1. _Business concept 'Payment Transaction' — The table stores one record per payment with identifiers, order linkage, amount, date, method, status, and authorization code, which matches a payment transact…_

2. _## Migration Priority Guidelines  ### Critical Path (Must Migrate First) 1. **tblCustomer** - Required for all orders 2. **tblProduct** - Required for line items and inventory 3. **vw_SalesOrderHdr** …_

3. _Email (VARCHAR 150)     - User email address     - For notifications  LastLogin (DATETIME)     - Last successful login timestamp     - NULL for new users  CreatedDate (DATETIME)     - Account creation…_

---

### ✅ 11 — What is the purpose of the bolActive field in tblCustomer and tblProduct?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.9646 | **Gate:** `proceed`

**Expected answer:**
> The bolActive field (using Hungarian notation 'bol' for boolean/bit) is a flag indicating whether a record is active. In tblCustomer, it marks whether customers are included in marketing (1=active, 0=inactive). In tblProduct, it indicates product availability (1=available for sale, 0=discontinued).

**System answer:**
> In `tblCustomer`, `bolActive` is used to mark whether a customer is active or inactive. The business glossary states that customers “can be marked as inactive (`bolActive = 0`) but are never deleted,” so its purpose is to preserve customer records while indicating inactive status.

For `tblProduct`, the retrieved context shows that `TBLPRODUCT` includes a `bolActive` column, and it also says the p…

**Sources retrieved (12):** `parent_chunk_data_dictionary.txt_4`, `parent_chunk_data_dictionary.txt_7`, `parent_chunk_business_glossary.md_0`, `parent_chunk_business_glossary.md_3`, `Customer Master→TBLCUSTOMER`, `Unknown→TBLPRODUCT`, `parent_chunk_business_glossary.md_2`, `Unknown→TBLSHIPPINGCARRIER`

**Context previews (first 3):**

1. _================================================================================ CUSTOMERMASTER DATABASE - DATA DICTIONARY =============================================================================…_

2. _Email (VARCHAR 150)     - User email address     - For notifications  LastLogin (DATETIME)     - Last successful login timestamp     - NULL for new users  CreatedDate (DATETIME)     - Account creation…_

3. _# CustomerMaster E-Commerce System - Business Glossary  ## Document Overview **System**: CustomerMaster v3.2.1 (Legacy) **Last Updated**: March 2015 **Purpose**: Business terminology definitions for d…_

---

### ✅ 12 — How are inventory transactions tracked in the system?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.1660 | **Gate:** `proceed_with_warning`

**Expected answer:**
> Inventory transactions are tracked in the inv_txn_log table, which records all stock movements. Each transaction has a type (txn_type): 'IN' for receipts, 'OUT' for shipments, and 'ADJ' for corrections. The table uses heavily abbreviated field names and references products via prod_id.

**System answer:**
> Inventory transactions are tracked in the `inv_txn_log` table. The retrieved context describes this table as the system’s “Inventory transaction log” and also classifies it as the inventory audit trail.

From the available schema metadata, `inv_txn_log` contains these columns: `txn_id`, `prod_id`, `txn_type`, `qty`, `txn_dt`, `ref_num`, `user_id`, and `notes`. The context gives these specific deta…

**Sources retrieved (12):** `parent_chunk_data_dictionary.txt_6`, `parent_chunk_business_glossary.md_3`, `parent_chunk_business_glossary.md_2`, `parent_chunk_business_glossary.md_0`, `parent_chunk_data_dictionary.txt_7`, `parent_chunk_data_dictionary.txt_4`, `parent_chunk_data_dictionary.txt_5`, `Unknown→INV_TXN_LOG`

**Context previews (first 3):**

1. _qty (INT)     - Quantity ordered     - Must be positive integer  amt (DECIMAL 10,2)     - Line item total amount (qty * unit_price)     - At time of order (snapshotted, not current price)  disc_amt (D…_

2. _## Migration Priority Guidelines  ### Critical Path (Must Migrate First) 1. **tblCustomer** - Required for all orders 2. **tblProduct** - Required for line items and inventory 3. **vw_SalesOrderHdr** …_

3. _## Legacy System Quirks  ### Hungarian Notation The legacy system uses Hungarian notation prefixes: - `str` = string (VARCHAR) - `int` = integer (INT) - `lng` = long integer (INT) - `flt` = float/mone…_

---

### ✅ 13 — What is the self-referencing relationship in the Group table?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.3145 | **Gate:** `proceed`

**Expected answer:**
> The Group table has a self-referencing foreign key where ParentGroupID references GroupID, creating a hierarchical structure for product categories. A NULL ParentGroupID indicates a top-level group, while non-NULL values create nested category levels.

**System answer:**
> The `Group` table has a self-referencing foreign key: `PARENTGROUPID -> GROUP.GROUPID`. This means each group can point to another row in the same `GROUP` table as its parent, creating a hierarchy of product categories. The table’s relevant columns are `GroupID`, `GroupName`, `ParentGroupID`, `Description`, and `IsActive`. Because `Group` is a reserved word, it must be quoted as `[Group]`.

**Sources retrieved (12):** `GROUP→GROUP`, `parent_chunk_data_dictionary.txt_6`, `parent_chunk_business_glossary.md_2`, `Unknown→GROUP`, `parent_chunk_business_glossary.md_3`, `parent_chunk_data_dictionary.txt_8`, `parent_chunk_data_dictionary.txt_7`, `parent_chunk_data_dictionary.txt_4`

**Context previews (first 3):**

1. _Relationship: GROUP references GROUP via foreign key PARENTGROUPID -> GROUP.GROUPID.…_

2. _qty (INT)     - Quantity ordered     - Must be positive integer  amt (DECIMAL 10,2)     - Line item total amount (qty * unit_price)     - At time of order (snapshotted, not current price)  disc_amt (D…_

3. _## Legacy System Quirks  ### Hungarian Notation The legacy system uses Hungarian notation prefixes: - `str` = string (VARCHAR) - `int` = integer (INT) - `lng` = long integer (INT) - `flt` = float/mone…_

---

### ✅ 14 — What migration compatibility columns exist in tblCustomer?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.9903 | **Gate:** `proceed`

**Expected answer:**
> The tblCustomer table includes cust_id (INT) and customer_name (VARCHAR 255) as migration compatibility columns alongside the legacy strCustID and strFullName fields. These are intended for the new ERP system that will use integer IDs and standardized naming conventions.

**System answer:**
> The retrieved context says `tblCustomer` includes migration compatibility fields, but it does not explicitly identify which specific columns those are.

The full column list given for `TBLCUSTOMER` is: `strCustID`, `strFullName`, `strEmail`, `strRegion`, `strCountry`, `dtmCreated`, `dtmLastModified`, `bolActive`, `cust_id`, `customer_name`, `txtNotes`.

From the context alone, I can confirm that m…

**Sources retrieved (12):** `Customer Master→TBLCUSTOMER`, `parent_chunk_business_glossary.md_3`, `parent_chunk_data_dictionary.txt_4`, `parent_chunk_business_glossary.md_0`, `parent_chunk_business_glossary.md_2`, `parent_chunk_data_dictionary.txt_5`, `VW_SALESORDERHDR→TBLCUSTOMER`, `parent_chunk_data_dictionary.txt_8`

**Context previews (first 3):**

1. _Business concept 'Customer Master' — The DDL explicitly labels this as a legacy CustomerMaster source and the columns capture master customer attributes such as name, email, region, country, and activ…_

2. _## Migration Priority Guidelines  ### Critical Path (Must Migrate First) 1. **tblCustomer** - Required for all orders 2. **tblProduct** - Required for line items and inventory 3. **vw_SalesOrderHdr** …_

3. _================================================================================ CUSTOMERMASTER DATABASE - DATA DICTIONARY =============================================================================…_

---

### ✅ 15 — How does the system handle order status history tracking?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.4313 | **Gate:** `proceed`

**Expected answer:**
> Order status changes are tracked in the tblOrderStatusHistory table, which creates an audit record for each status transition. Each history record includes OrderID, OldStatus, NewStatus, ChangedByUser, ChangedDate, and ChangeReason fields, providing a complete audit trail of order workflow.

**System answer:**
> The system tracks order status changes in the `tblOrderStatusHistory` table, which is explicitly described as an audit log of order status changes.

Each status transition is recorded as one history row with:
`HistoryID` as the auto-increment primary key,
`OrderID` as the foreign key to `vw_SalesOrderHdr.lngOrderID`,
`OldStatus` as the previous status value,
`NewStatus` as the new/current status v…

**Sources retrieved (12):** `Unknown→TBLSHIPPINGCARRIER`, `Unknown→GROUP`, `parent_chunk_data_dictionary.txt_7`, `Unknown→USER`, `Unknown→TBLORDERSTATUSHISTORY`, `Unknown→TBLPRODUCT`, `Unknown→INV_TXN_LOG`, `Unknown→ORD_LINE_ITEM`

**Context previews (first 3):**

1. _Business concept 'Unknown' — The table implements an order status history log, with HistoryID, OrderID, OldStatus, NewStatus, ChangedByUser, and ChangedDate capturing status transition events for sale…_

2. _Business concept 'Unknown' — The table implements an order status history log, with HistoryID, OrderID, OldStatus, NewStatus, ChangedByUser, and ChangedDate capturing status transition events for sale…_

3. _Email (VARCHAR 150)     - User email address     - For notifications  LastLogin (DATETIME)     - Last successful login timestamp     - NULL for new users  CreatedDate (DATETIME)     - Account creation…_

---

### ✅ 16 — What is the inconsistent naming pattern between order tables?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.2869 | **Gate:** `proceed`

**Expected answer:**
> The schema shows inconsistent naming: order headers use 'vw_SalesOrderHdr' with Hungarian notation, while line items use 'ord_line_item' with abbreviated underscore notation. Additionally, the line item table references lngOrderID but names its foreign key 'ord_id' instead of 'order_id' or 'lngOrder…

**System answer:**
> The order-related tables use mixed naming conventions instead of one consistent pattern. `vw_SalesOrderHdr` uses a `vw_` prefix even though it is actually a table, `ord_line_item` uses an `ord_` prefix, and `tblOrderStatusHistory` uses the `tbl` prefix. So the inconsistency is that order tables are split across `vw_`, `ord_`, and `tbl` naming styles.

**Sources retrieved (12):** `parent_chunk_business_glossary.md_2`, `parent_chunk_data_dictionary.txt_5`, `parent_chunk_data_dictionary.txt_8`, `parent_chunk_business_glossary.md_3`, `parent_chunk_data_dictionary.txt_7`, `parent_chunk_data_dictionary.txt_6`, `parent_chunk_business_glossary.md_0`, `parent_chunk_data_dictionary.txt_4`

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
> In `tblProduct` (`TBLPRODUCT`), the deprecated legacy fields are `prod_num`, `item_desc`, and `unit_cost`.

`prod_num` is an old legacy product number field (`VARCHAR 20`). It has been superseded by `strSKU` and is retained only for historical reporting, so it should be avoided in new code.

`item_desc` is an old truncated description field (`VARCHAR 500`). It has been superseded by `strDescriptio…

**Sources retrieved (12):** `parent_chunk_business_glossary.md_3`, `parent_chunk_data_dictionary.txt_5`, `Unknown→TBLPRODUCT`, `parent_chunk_business_glossary.md_2`, `parent_chunk_data_dictionary.txt_6`, `parent_chunk_data_dictionary.txt_8`, `Customer Master→TBLCUSTOMER`, `parent_chunk_data_dictionary.txt_7`

**Context previews (first 3):**

1. _## Migration Priority Guidelines  ### Critical Path (Must Migrate First) 1. **tblCustomer** - Required for all orders 2. **tblProduct** - Required for line items and inventory 3. **vw_SalesOrderHdr** …_

2. _strCategory (VARCHAR 100)     - Product category     - Hierarchical: "Clothing > Shirts > Casual" strBrand (VARCHAR 100) - Brand or manufacturer name - Free text field dtmIntroduced (DATETIME) - Produ…_

3. _Business concept 'Unknown' — The table implements an order status history log, with HistoryID, OrderID, OldStatus, NewStatus, ChangedByUser, and ChangedDate capturing status transition events for sale…_

---

### ✅ 18 — How are shipping carriers configured in the system?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.2613 | **Gate:** `proceed`

**Expected answer:**
> Shipping carriers are stored in the tblShippingCarrier table with CarrierID, CarrierName, CarrierCode (for API integration), TrackingURL (with {TRACKING_NUM} placeholder), and bolActive flag. Only carriers with bolActive=1 should be offered during checkout.

**System answer:**
> Shipping carriers are configured as reference data in `tblShippingCarrier`. From the retrieved context, that table contains these fields: `CarrierID`, `CarrierName`, `CarrierCode`, `TrackingURL`, and `bolActive`.

The glossary describes a shipping carrier as a third-party logistics provider responsible for delivering packages to customers, and says carriers are stored in `tblShippingCarrier`. The …

**Sources retrieved (12):** `parent_chunk_data_dictionary.txt_7`, `parent_chunk_business_glossary.md_3`, `Unknown→TBLSHIPPINGCARRIER`, `parent_chunk_business_glossary.md_2`, `parent_chunk_business_glossary.md_0`, `parent_chunk_data_dictionary.txt_4`, `parent_chunk_data_dictionary.txt_6`, `parent_chunk_data_dictionary.txt_5`

**Context previews (first 3):**

1. _Email (VARCHAR 150)     - User email address     - For notifications  LastLogin (DATETIME)     - Last successful login timestamp     - NULL for new users  CreatedDate (DATETIME)     - Account creation…_

2. _## Migration Priority Guidelines  ### Critical Path (Must Migrate First) 1. **tblCustomer** - Required for all orders 2. **tblProduct** - Required for line items and inventory 3. **vw_SalesOrderHdr** …_

3. _Business concept 'Unknown' — The table implements an order status history log, with HistoryID, OrderID, OldStatus, NewStatus, ChangedByUser, and ChangedDate capturing status transition events for sale…_

---

### ✅ 19 — What is the relationship between User table passwords and security?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0401 | **Gate:** `proceed_with_warning`

**Expected answer:**
> The User table stores password hashes in the PasswordHash field, but uses SHA-256 without salt, making it vulnerable to rainbow table attacks. This is identified as a security issue in the data dictionary. Additionally, the table name 'User' is a SQL reserved word requiring square bracket quoting.

**System answer:**
> The `User` table has a direct security weakness: `User.PasswordHash` uses SHA-256 without a salt, which the context identifies as vulnerable to rainbow table attacks. The context also notes that `User` is a reserved word and must be quoted as `[User]`, but the actual password-related security issue is specifically the unsalted SHA-256 hashing approach. The `User` table stores system user records w…

**Sources retrieved (12):** `parent_chunk_business_glossary.md_3`, `parent_chunk_data_dictionary.txt_7`, `Unknown→USER`, `parent_chunk_data_dictionary.txt_8`, `parent_chunk_business_glossary.md_2`, `parent_chunk_data_dictionary.txt_6`, `parent_chunk_data_dictionary.txt_4`, `parent_chunk_data_dictionary.txt_5`

**Context previews (first 3):**

1. _## Migration Priority Guidelines  ### Critical Path (Must Migrate First) 1. **tblCustomer** - Required for all orders 2. **tblProduct** - Required for line items and inventory 3. **vw_SalesOrderHdr** …_

2. _Email (VARCHAR 150)     - User email address     - For notifications  LastLogin (DATETIME)     - Last successful login timestamp     - NULL for new users  CreatedDate (DATETIME)     - Account creation…_

3. _Business concept 'Unknown' — The table implements an order status history log, with HistoryID, OrderID, OldStatus, NewStatus, ChangedByUser, and ChangedDate capturing status transition events for sale…_

---

### ✅ 20 — What fields in vw_SalesOrderHdr use the 'flt' Hungarian notation prefix and what do they store?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.9841 | **Gate:** `proceed`

**Expected answer:**
> The vw_SalesOrderHdr table uses the 'flt' (float) prefix for three monetary fields: fltSubTotal (line item subtotal before tax), fltTaxAmount (calculated tax), and fltTotalAmount (final total including tax and shipping). Despite the 'flt' prefix suggesting floating-point, these are defined as DECIMA…

**System answer:**
> In `VW_SALESORDERHDR`, the fields with the `flt` Hungarian notation prefix are `fltSubTotal`, `fltTaxAmount`, and `fltTotalAmount`. Based on the glossary entry for the `Sales Order` concept, these are the order’s monetary total fields. The notation guide says `flt` is used for float/money values (`DECIMAL`).

So these fields store:
`fltSubTotal` — the order subtotal,
`fltTaxAmount` — the tax amoun…

**Sources retrieved (12):** `Sales Order→VW_SALESORDERHDR`, `parent_chunk_business_glossary.md_3`, `parent_chunk_data_dictionary.txt_5`, `parent_chunk_business_glossary.md_2`, `parent_chunk_business_glossary.md_0`, `parent_chunk_data_dictionary.txt_7`, `parent_chunk_data_dictionary.txt_8`, `parent_chunk_data_dictionary.txt_4`

**Context previews (first 3):**

1. _Business concept 'Sales Order' — The table is explicitly labeled as a sales order header and contains core order lifecycle fields such as order date, ship date, required date, status, and monetary tot…_

2. _## Migration Priority Guidelines  ### Critical Path (Must Migrate First) 1. **tblCustomer** - Required for all orders 2. **tblProduct** - Required for line items and inventory 3. **vw_SalesOrderHdr** …_

3. _strCategory (VARCHAR 100)     - Product category     - Hierarchical: "Clothing > Shirts > Casual" strBrand (VARCHAR 100) - Brand or manufacturer name - Free text field dtmIntroduced (DATETIME) - Produ…_

---

### ✅ 21 — How does the schema handle the different date/time field naming conventions?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.1757 | **Gate:** `proceed_with_warning`

**Expected answer:**
> The schema uses 'dtm' (datetime) Hungarian notation prefix consistently: dtmCreated and dtmLastModified in tblCustomer, dtmOrderDate/dtmShipDate/dtmRequiredDate in vw_SalesOrderHdr, dtmIntroduced/dtmDiscontinued in tblProduct, and txn_dt in inv_txn_log (abbreviated exception). The User table breaks …

**System answer:**
> The schema does not use a single consistent date/time naming convention.

In the legacy Hungarian notation pattern, `dtm` denotes a `DATETIME` field. Examples in the context include `dtmIntroduced`, `dtmDiscontinued`, `dtmOrderDate`, `dtmShipDate`, and `dtmRequiredDate`. The data dictionary explicitly says `dtm = datetime (DATETIME)`.

However, the context also says naming is inconsistent across t…

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
> The schema uses several table naming prefix patterns, and the context explicitly says they are inconsistent across the system.

The patterns shown are `tbl`, `vw_`, `ord_`, and `inv_`, plus some tables with no prefix at all. `tbl` appears on tables such as `tblCustomer`, `tblProduct`, `tblPayment`, and `tblOrderStatusHistory`; in one table definition (`tblOrderStatusHistory`) this is described as …

**Sources retrieved (12):** `parent_chunk_data_dictionary.txt_5`, `parent_chunk_data_dictionary.txt_8`, `parent_chunk_business_glossary.md_2`, `parent_chunk_data_dictionary.txt_7`, `parent_chunk_business_glossary.md_0`, `parent_chunk_business_glossary.md_3`, `parent_chunk_data_dictionary.txt_4`, `parent_chunk_data_dictionary.txt_6`

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
> For `vw_SalesOrderHdr`, the retrieved context shows one outbound foreign key and three inbound foreign key relationships.

`vw_SalesOrderHdr` references `tblCustomer` through `intCustID -> tblCustomer.strCustID`. The context also notes a legacy naming inconsistency: `intCustID` is actually a `VARCHAR`, even though the name suggests an integer.

Three other tables reference `vw_SalesOrderHdr.lngOrd…

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
> From the retrieved context, the legacy product identifier is `tblProduct.strSKU`. It is the current SKU field, and the older `prod_num` field is explicitly marked as deprecated and “superseded by `strSKU`.” The order line table `ord_line_item` also stores `product_code` as a redundant copy of `tblProduct.strSKU` for reporting, and that copy may be out of sync with the product master.

For SKU form…

**Sources retrieved (12):** `parent_chunk_business_glossary.md_0`, `parent_chunk_business_glossary.md_2`, `parent_chunk_data_dictionary.txt_4`, `parent_chunk_data_dictionary.txt_5`, `parent_chunk_business_glossary.md_3`, `parent_chunk_data_dictionary.txt_6`, `Customer Master→TBLCUSTOMER`, `Unknown→TBLPRODUCT`

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
> The migration review identified several critical data quality and related migration issues.

Under referential integrity gaps, some `ord_line_item.prod_id` values reference non-existent products in `tblProduct`, some orders reference customers in `tblCustomer` who are marked inactive, and `inv_txn_log.user_id` has no foreign key constraint.

Under data inconsistencies, `tblProduct` contains both a…

**Sources retrieved (12):** `parent_chunk_business_glossary.md_3`, `parent_chunk_data_dictionary.txt_8`, `parent_chunk_business_glossary.md_0`, `parent_chunk_business_glossary.md_2`, `parent_chunk_data_dictionary.txt_4`, `Customer Master→TBLCUSTOMER`, `parent_chunk_data_dictionary.txt_6`, `parent_chunk_data_dictionary.txt_7`

**Context previews (first 3):**

1. _## Migration Priority Guidelines  ### Critical Path (Must Migrate First) 1. **tblCustomer** - Required for all orders 2. **tblProduct** - Required for line items and inventory 3. **vw_SalesOrderHdr** …_

2. _CardNumberText (VARCHAR 100)     - SECURITY ISSUE: Full card number stored as text! - Should be tokenized - Contains unencrypted PAN (Primary Account Number) CardHolderName (VARCHAR 100) - Cardholder …_

3. _# CustomerMaster E-Commerce System - Business Glossary  ## Document Overview **System**: CustomerMaster v3.2.1 (Legacy) **Last Updated**: March 2015 **Purpose**: Business terminology definitions for d…_

---

## Anomalies & Observations

No anomalies detected. All questions grounded with acceptable RAGAS scores.
