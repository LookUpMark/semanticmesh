# AB-04 — 06_edgecases_legacy — Run Analysis

**Timestamp:** 2026-03-31 02:38:34  
**Run tag:** `v5`

## Configuration

| Parameter | Value |
|-----------|-------|
| Extraction model | `LLM (gpt-5.4-nano-2026-03-17)` |
| Reasoning model | `gpt-5.4-2026-03-05` |
| Embedding model | `BAAI/bge-m3` |
| Retrieval mode | `hybrid` |
| Reranker | `True` |
| Reranker top_k | `5` |
| Chunk size / overlap | `256 / 32` |
| ER similarity threshold | `0.75` |

## Builder Results

Builder skipped (`--no-builder`).

## Query Evaluation Summary

| Metric | Value |
|--------|-------|
| Questions | 25 |
| Grounded | **25/25 (100%)** |
| Avg GT Coverage | 100% |
| Avg Top Score | 0.6102 |
| Avg Chunk Count | 5.0 |
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
> The `tblCustomer` table stores customer master data from the legacy CRM system. In the business glossary, a customer is defined as an individual or organization that has purchased products or services from the company, and customers are stored in `tblCustomer` with legacy identifiers inherited from the AS/400 system. It is a core entity required for all orders in the migration priority guidance.

**Sources retrieved (5):** `parent_chunk_data_dictionary.txt_4`, `parent_chunk_business_glossary.md_0`, `parent_chunk_data_dictionary.txt_5`, `parent_chunk_business_glossary.md_3`, `parent_chunk_data_dictionary.txt_7`

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
> In the legacy CustomerMaster system, customers are identified by `strCustID` in the `tblCustomer` table. This is the primary key and the required unique customer code for each customer. The context says it is an alphanumeric identifier inherited from the AS/400 system, stored as `VARCHAR(50)`, with formats such as `C-XXXXX` or `REG-XXXX`. It can contain letters, numbers, and hyphens, and it is `NO…

**Sources retrieved (5):** `parent_chunk_business_glossary.md_0`, `parent_chunk_data_dictionary.txt_4`, `parent_chunk_business_glossary.md_2`, `parent_chunk_data_dictionary.txt_5`, `parent_chunk_business_glossary.md_1`

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
> Order header information is stored in VW_SALESORDERHDR, which implements the business concept Sales order header records. The key column identified for that table is lngOrderID; the context also shows tblOrderStatusHistory.OrderID as a foreign key to vw_SalesOrderHdr.lngOrderID, indicating lngOrderID is the order header identifier. The context does not explicitly label it as the primary key, but l…

**Sources retrieved (5):** `Sales order header records→VW_SALESORDERHDR`, `payment records`, `parent_chunk_data_dictionary.txt_5`, `payment records→TBLPAYMENT`, `parent_chunk_data_dictionary.txt_7`

**Context previews (first 3):**

1. _Business concept 'Sales order header records' is implemented by physical table VW_SALESORDERHDR (columns: lngOrderID, intCustID, dtmOrderDate, dtmShipDate, dtmRequiredDate, strOrderStatus, fltSubTotal…_

2. _payment records: The table contains core payment transaction fields such as PaymentID, OrderID, PaymentMethod, PaymentDate, Amount, PaymentStatus, and authorization details, which strongly indicate a …_

3. _strCategory (VARCHAR 100)     - Product category     - Hierarchical: "Clothing > Shirts > Casual" strBrand (VARCHAR 100) - Brand or manufacturer name - Free text field dtmIntroduced (DATETIME) - Produ…_

---

### ✅ 4 — Which table in the schema uses a SQL reserved word as its name?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.5119 | **Gate:** `proceed`

**Expected answer:**
> The schema includes two tables that use SQL reserved words: 'Group' (for product categories) and 'User' (for system users). These require square bracket quoting [Group] and [User] in SQL queries to avoid syntax errors.

**System answer:**
> The schema uses two SQL reserved words as table names: `Group` and `User`. The context says they must be quoted as `[Group]` and `[User]`.

**Sources retrieved (5):** `parent_chunk_business_glossary.md_2`, `parent_chunk_data_dictionary.txt_6`, `parent_chunk_data_dictionary.txt_8`, `parent_chunk_data_dictionary.txt_5`, `Order line items`

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
> `vw_SalesOrderHdr` references `tblCustomer` through a foreign key from `vw_SalesOrderHdr.INTCUSTID` to `TBLCUSTOMER.STRCUSTID`. The context also states that `tblCustomer` is the customer master table, where customers are stored with a unique customer code `strCustID`, and that `vw_SalesOrderHdr` is core transactional order data. Together, this means each sales order header is linked to a customer …

**Sources retrieved (5):** `VW_SALESORDERHDR→TBLCUSTOMER`, `parent_chunk_business_glossary.md_0`, `TBLPAYMENT→VW_SALESORDERHDR`, `parent_chunk_data_dictionary.txt_5`, `parent_chunk_business_glossary.md_3`

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
> The inventory transaction log table `inv_txn_log` uses a heavily abbreviated naming convention. It also follows the `inv_` table prefix pattern shown in the legacy system naming conventions.

**Sources retrieved (5):** `parent_chunk_data_dictionary.txt_6`, `parent_chunk_business_glossary.md_2`, `parent_chunk_data_dictionary.txt_7`, `parent_chunk_business_glossary.md_3`, `inventory audit trail→INV_TXN_LOG`

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
> The `tblProduct.unit_cost` field has an inappropriate data type: it is stored as `VARCHAR(20)` instead of a numeric type like `DECIMAL`. The context explicitly calls this a bug, notes that it contains currency symbols such as `"$19.99"`, and says it must be parsed before calculations.

**Sources retrieved (5):** `parent_chunk_business_glossary.md_3`, `parent_chunk_business_glossary.md_2`, `parent_chunk_data_dictionary.txt_8`, `parent_chunk_data_dictionary.txt_6`, `parent_chunk_data_dictionary.txt_5`

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
> From the retrieved context, `ORD_LINE_ITEM` handles product-related data in a partially denormalized way: it references `TBLPRODUCT` through `prod_id -> TBLPRODUCT.INTPRODID`, but the table itself also contains `product_code` and `item_name` along with `prod_id`, `qty`, `amt`, `disc_amt`, and `line_status`.

The context explicitly states only one consequence of this design: denormalized fields in …

**Sources retrieved (5):** `ORD_LINE_ITEM→TBLPRODUCT`, `Order line items→ORD_LINE_ITEM`, `parent_chunk_business_glossary.md_3`, `ORD_LINE_ITEM→VW_SALESORDERHDR`, `Order line items`

**Context previews (first 3):**

1. _Relationship: ORD_LINE_ITEM references TBLPRODUCT via foreign key PROD_ID -> TBLPRODUCT.INTPRODID.…_

2. _Business concept 'Order line items' — The table is clearly an order-detail structure: it links a single order to a product and captures quantity, total amount, discount amount, and line status. The sc…_

3. _## Migration Priority Guidelines  ### Critical Path (Must Migrate First) 1. **tblCustomer** - Required for all orders 2. **tblProduct** - Required for line items and inventory 3. **vw_SalesOrderHdr** …_

---

### ✅ 9 — What are the valid values for the strOrderStatus field in vw_SalesOrderHdr?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.9131 | **Gate:** `proceed`

**Expected answer:**
> The strOrderStatus field accepts three values enforced by a CHECK constraint: 'PENDING' (order received but not shipped), 'SHIPPED' (order has been shipped to customer), and 'CANCELLED' (order cancelled before shipping).

**System answer:**
> The retrieved context does not enumerate the valid values for `vw_SalesOrderHdr.strOrderStatus`.

What the context does confirm is that `strOrderStatus` is a column on `VW_SALESORDERHDR`, which implements the business concept “Sales order header records.” It also shows a related audit table, `tblOrderStatusHistory`, where `OrderID` links to `vw_SalesOrderHdr.lngOrderID` and status changes are trac…

**Sources retrieved (5):** `parent_chunk_data_dictionary.txt_5`, `Sales order header records→VW_SALESORDERHDR`, `parent_chunk_data_dictionary.txt_7`, `parent_chunk_business_glossary.md_0`, `parent_chunk_business_glossary.md_1`

**Context previews (first 3):**

1. _strCategory (VARCHAR 100)     - Product category     - Hierarchical: "Clothing > Shirts > Casual" strBrand (VARCHAR 100) - Brand or manufacturer name - Free text field dtmIntroduced (DATETIME) - Produ…_

2. _Business concept 'Sales order header records' is implemented by physical table VW_SALESORDERHDR (columns: lngOrderID, intCustID, dtmOrderDate, dtmShipDate, dtmRequiredDate, strOrderStatus, fltSubTotal…_

3. _Email (VARCHAR 150)     - User email address     - For notifications  LastLogin (DATETIME)     - Last successful login timestamp     - NULL for new users  CreatedDate (DATETIME)     - Account creation…_

---

### ✅ 10 — Which table stores payment information and what security issue does it have?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.3347 | **Gate:** `proceed`

**Expected answer:**
> Payment information is stored in the tblPayment table. The table has a critical security issue: the CardNumberText field stores full unencrypted credit card numbers as VARCHAR(100), which is a PCI compliance violation. The system also lacks proper tokenization and encryption at rest.

**System answer:**
> Payment information is stored in the physical table TBLPAYMENT, also referred to as tblPayment. The context says it contains payment transaction fields including PaymentID, OrderID, PaymentMethod, PaymentDate, Amount, PaymentStatus, CardNumberText, CardHolderName, and AuthorizationCode.

The security issue is that TBLPAYMENT.CardNumberText stores full card numbers in plaintext as unencrypted text.…

**Sources retrieved (5):** `payment records`, `parent_chunk_business_glossary.md_3`, `parent_chunk_data_dictionary.txt_7`, `payment records→TBLPAYMENT`, `parent_chunk_data_dictionary.txt_8`

**Context previews (first 3):**

1. _payment records: The table contains core payment transaction fields such as PaymentID, OrderID, PaymentMethod, PaymentDate, Amount, PaymentStatus, and authorization details, which strongly indicate a …_

2. _## Migration Priority Guidelines  ### Critical Path (Must Migrate First) 1. **tblCustomer** - Required for all orders 2. **tblProduct** - Required for line items and inventory 3. **vw_SalesOrderHdr** …_

3. _Email (VARCHAR 150)     - User email address     - For notifications  LastLogin (DATETIME)     - Last successful login timestamp     - NULL for new users  CreatedDate (DATETIME)     - Account creation…_

---

### ✅ 11 — What is the purpose of the bolActive field in tblCustomer and tblProduct?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.9646 | **Gate:** `proceed`

**Expected answer:**
> The bolActive field (using Hungarian notation 'bol' for boolean/bit) is a flag indicating whether a record is active. In tblCustomer, it marks whether customers are included in marketing (1=active, 0=inactive). In tblProduct, it indicates product availability (1=available for sale, 0=discontinued).

**System answer:**
> In `tblCustomer`, the retrieved context explicitly shows that `bolActive` is used to mark whether a customer is active. The business rule says customers with `bolActive = 0` are inactive, and inactive customers are never deleted. This means the field supports customer status management while preserving legacy customer records.

For `tblProduct`, the retrieved context does not provide the actual fi…

**Sources retrieved (5):** `parent_chunk_data_dictionary.txt_4`, `parent_chunk_data_dictionary.txt_7`, `parent_chunk_business_glossary.md_0`, `parent_chunk_business_glossary.md_3`, `parent_chunk_business_glossary.md_1`

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
> Inventory transactions are tracked through the inventory audit trail, which is implemented by the physical table `INV_TXN_LOG` / `inv_txn_log`. Its stated purpose is “Inventory transaction log.”

The table records each inventory adjustment with these columns: `txn_id`, `prod_id`, `txn_type`, `qty`, `txn_dt`, `ref_num`, `user_id`, and `notes`. From the schema details available, `txn_id` is the auto…

**Sources retrieved (5):** `parent_chunk_data_dictionary.txt_6`, `parent_chunk_business_glossary.md_3`, `inventory audit trail→INV_TXN_LOG`, `inventory audit trail`, `parent_chunk_business_glossary.md_1`

**Context previews (first 3):**

1. _qty (INT)     - Quantity ordered     - Must be positive integer  amt (DECIMAL 10,2)     - Line item total amount (qty * unit_price)     - At time of order (snapshotted, not current price)  disc_amt (D…_

2. _## Migration Priority Guidelines  ### Critical Path (Must Migrate First) 1. **tblCustomer** - Required for all orders 2. **tblProduct** - Required for line items and inventory 3. **vw_SalesOrderHdr** …_

3. _Business concept 'inventory audit trail' is implemented by physical table INV_TXN_LOG (columns: txn_id, prod_id, txn_type, qty, txn_dt, ref_num, user_id, notes).…_

---

### ✅ 13 — What is the self-referencing relationship in the Group table?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.8372 | **Gate:** `proceed`

**Expected answer:**
> The Group table has a self-referencing foreign key where ParentGroupID references GroupID, creating a hierarchical structure for product categories. A NULL ParentGroupID indicates a top-level group, while non-NULL values create nested category levels.

**System answer:**
> The `GROUP` table has a self-referencing foreign key where `PARENTGROUPID` references `GROUP.GROUPID`. This implements a one-to-many Group → Group hierarchy, meaning each group can have a parent group and can also have multiple child groups. The relevant table is `GROUP` with columns `GroupID`, `GroupName`, `ParentGroupID`, `Description`, and `IsActive`.

**Sources retrieved (5):** `Group Hierarchy→GROUP`, `GROUP→GROUP`, `parent_chunk_data_dictionary.txt_6`, `parent_chunk_business_glossary.md_2`, `Group Hierarchy`

**Context previews (first 3):**

1. _Business concept 'Group Hierarchy' — The table is a self-referencing group/category structure with ParentGroupID and contains only generic group attributes, which aligns most closely with a hierarchic…_

2. _Relationship: GROUP references GROUP via foreign key PARENTGROUPID -> GROUP.GROUPID.…_

3. _qty (INT)     - Quantity ordered     - Must be positive integer  amt (DECIMAL 10,2)     - Line item total amount (qty * unit_price)     - At time of order (snapshotted, not current price)  disc_amt (D…_

---

### ✅ 14 — What migration compatibility columns exist in tblCustomer?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.6606 | **Gate:** `proceed`

**Expected answer:**
> The tblCustomer table includes cust_id (INT) and customer_name (VARCHAR 255) as migration compatibility columns alongside the legacy strCustID and strFullName fields. These are intended for the new ERP system that will use integer IDs and standardized naming conventions.

**System answer:**
> The retrieved context does not explicitly label any `tblCustomer` fields as “migration compatibility columns.” What it does show is that `TBLCUSTOMER` implements the `CustomerMaster v3.2.1` concept and contains both legacy Hungarian-notation columns and alternate-style column names.

From that evidence, the compatibility-style columns in `TBLCUSTOMER` appear to be `cust_id` and `customer_name`, be…

**Sources retrieved (5):** `parent_chunk_business_glossary.md_3`, `CustomerMaster v3.2.1→TBLCUSTOMER`, `parent_chunk_data_dictionary.txt_4`, `parent_chunk_business_glossary.md_0`, `parent_chunk_business_glossary.md_2`

**Context previews (first 3):**

1. _## Migration Priority Guidelines  ### Critical Path (Must Migrate First) 1. **tblCustomer** - Required for all orders 2. **tblProduct** - Required for line items and inventory 3. **vw_SalesOrderHdr** …_

2. _Business concept 'CustomerMaster v3.2.1' is implemented by physical table TBLCUSTOMER (columns: strCustID, strFullName, strEmail, strRegion, strCountry, dtmCreated, dtmLastModified, bolActive, cust_id…_

3. _================================================================================ CUSTOMERMASTER DATABASE - DATA DICTIONARY =============================================================================…_

---

### ✅ 15 — How does the system handle order status history tracking?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.3072 | **Gate:** `proceed`

**Expected answer:**
> Order status changes are tracked in the tblOrderStatusHistory table, which creates an audit record for each status transition. Each history record includes OrderID, OldStatus, NewStatus, ChangedByUser, ChangedDate, and ChangeReason fields, providing a complete audit trail of order workflow.

**System answer:**
> The system handles order status history tracking through the business concept Order status audit, which is implemented by the physical table TBLORDERSTATUSHISTORY / tblOrderStatusHistory.

This table is an audit log of order status changes. Each history row records:
HistoryID as the auto-increment primary key,
OrderID as the foreign key to vw_SalesOrderHdr.lngOrderID,
OldStatus as the previous sta…

**Sources retrieved (5):** `Order status audit→TBLORDERSTATUSHISTORY`, `parent_chunk_data_dictionary.txt_7`, `parent_chunk_business_glossary.md_3`, `parent_chunk_business_glossary.md_1`, `Order status audit`

**Context previews (first 3):**

1. _Business concept 'Order status audit' is implemented by physical table TBLORDERSTATUSHISTORY (columns: HistoryID, OrderID, OldStatus, NewStatus, ChangedByUser, ChangedDate, ChangeReason).…_

2. _Email (VARCHAR 150)     - User email address     - For notifications  LastLogin (DATETIME)     - Last successful login timestamp     - NULL for new users  CreatedDate (DATETIME)     - Account creation…_

3. _## Migration Priority Guidelines  ### Critical Path (Must Migrate First) 1. **tblCustomer** - Required for all orders 2. **tblProduct** - Required for line items and inventory 3. **vw_SalesOrderHdr** …_

---

### ✅ 16 — What is the inconsistent naming pattern between order tables?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.2869 | **Gate:** `proceed`

**Expected answer:**
> The schema shows inconsistent naming: order headers use 'vw_SalesOrderHdr' with Hungarian notation, while line items use 'ord_line_item' with abbreviated underscore notation. Additionally, the line item table references lngOrderID but names its foreign key 'ord_id' instead of 'order_id' or 'lngOrder…

**System answer:**
> The order-related tables use mixed naming conventions rather than one consistent pattern. In the context, the order header is named `vw_SalesOrderHdr` using a `vw_` prefix even though it is actually a table, while the order detail table is `ord_line_item` using an `ord_` prefix. Related order audit data also uses the `tbl` pattern in `tblOrderStatusHistory`. So the inconsistency is that order tabl…

**Sources retrieved (5):** `parent_chunk_business_glossary.md_2`, `parent_chunk_data_dictionary.txt_5`, `parent_chunk_data_dictionary.txt_8`, `parent_chunk_business_glossary.md_3`, `parent_chunk_data_dictionary.txt_7`

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
> In `tblProduct`, the deprecated fields are `prod_num`, `item_desc`, and `unit_cost`.

`prod_num` (`VARCHAR 20`) is the old legacy product number. It has been superseded by `strSKU` and is retained only for historical reporting, so it should not be used in new code.

`item_desc` (`VARCHAR 500`) is the old truncated description. It has been superseded by `strDescription`, and the context explicitly …

**Sources retrieved (5):** `parent_chunk_business_glossary.md_3`, `parent_chunk_data_dictionary.txt_5`, `both active and discontinued products with the same SKU pattern→TBLPRODUCT`, `parent_chunk_business_glossary.md_2`, `parent_chunk_data_dictionary.txt_6`

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
> Shipping carriers are configured as shipping carrier master data in the physical table `TBLSHIPPINGCARRIER` (also referred to in the terminology as `tblShippingCarrier`). This table stores carrier records with the columns `CarrierID`, `CarrierName`, `CarrierCode`, `TrackingURL`, and `bolActive`.

From the business terminology, a shipping carrier is a third-party logistics provider responsible for …

**Sources retrieved (5):** `Shipping carrier master data→TBLSHIPPINGCARRIER`, `parent_chunk_data_dictionary.txt_7`, `parent_chunk_business_glossary.md_3`, `parent_chunk_business_glossary.md_1`, `Shipping carrier master data`

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
> The `User` table, which implements the business concept “System users,” contains a `PasswordHash` column. The identified security issue is that `User.PasswordHash` uses SHA-256 without salt, which is described as vulnerable to rainbow table attacks. The context therefore links user passwords to a specific security weakness: password hashes are stored in a way that does not provide adequate protect…

**Sources retrieved (5):** `parent_chunk_business_glossary.md_3`, `parent_chunk_data_dictionary.txt_7`, `System users→USER`, `parent_chunk_data_dictionary.txt_8`, `parent_chunk_business_glossary.md_2`

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

From the legacy notation guidance, `flt` indicates a float/money value, stored as `DECIMAL`. Based on the column names, these store the order subtotal, the tax amount, and the total amount for the sales order. The context also notes a data quality issue that some `vw…

**Sources retrieved (5):** `Sales order header records→VW_SALESORDERHDR`, `parent_chunk_business_glossary.md_3`, `parent_chunk_data_dictionary.txt_5`, `parent_chunk_business_glossary.md_2`, `parent_chunk_business_glossary.md_0`

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
> The schema does not use one uniform date/time naming style; it uses multiple conventions in different parts of the legacy system.

In the Hungarian notation pattern, the `dtm` prefix indicates a `DATETIME` field. The context gives `dtmIntroduced` and `dtmDiscontinued` as examples, and `tblCustomer` explicitly states the naming convention includes `dtm = datetime`.

However, the schema is inconsist…

**Sources retrieved (5):** `parent_chunk_data_dictionary.txt_5`, `parent_chunk_business_glossary.md_2`, `parent_chunk_data_dictionary.txt_4`, `parent_chunk_data_dictionary.txt_8`, `parent_chunk_data_dictionary.txt_7`

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
> The schema uses inconsistent table prefix patterns across different parts of the system. According to the “Table Naming Inconsistency” description, the patterns are `tbl`, as in `tblCustomer`, `tblProduct`, and `tblPayment`; `vw_`, as in `vw_SalesOrderHdr`, although these are described as actually being tables rather than true views; `ord_`, as in `ord_line_item`; and `inv_`, as in `inv_txn_log`. …

**Sources retrieved (5):** `parent_chunk_data_dictionary.txt_5`, `parent_chunk_data_dictionary.txt_8`, `parent_chunk_business_glossary.md_2`, `parent_chunk_data_dictionary.txt_7`, `Order line items`

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
> For vw_SalesOrderHdr, the retrieved context shows four foreign key relationships.

vw_SalesOrderHdr references TBLCUSTOMER through INTCUSTID -> TBLCUSTOMER.STRCUSTID.

Three other tables reference vw_SalesOrderHdr through its LNGORDERID key:
ORD_LINE_ITEM.ORD_ID -> VW_SALESORDERHDR.LNGORDERID,
TBLPAYMENT.ORDERID -> VW_SALESORDERHDR.LNGORDERID,
and TBLORDERSTATUSHISTORY.ORDERID -> VW_SALESORDERHDR.…

**Sources retrieved (5):** `VW_SALESORDERHDR→TBLCUSTOMER`, `ORD_LINE_ITEM→VW_SALESORDERHDR`, `TBLPAYMENT→VW_SALESORDERHDR`, `TBLORDERSTATUSHISTORY→VW_SALESORDERHDR`, `parent_chunk_data_dictionary.txt_5`

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
> From the retrieved context, the legacy product identifier is `strSKU`, and the old field `prod_num` is deprecated. The data dictionary says `prod_num` is an old legacy product number, was superseded by `strSKU`, and is retained only for historical reporting. The naming-convention note also indicates that the `str` prefix means a string/VARCHAR field, so `strSKU` is handled as a string-style identi…

**Sources retrieved (5):** `parent_chunk_business_glossary.md_0`, `parent_chunk_business_glossary.md_2`, `parent_chunk_data_dictionary.txt_4`, `parent_chunk_data_dictionary.txt_5`, `parent_chunk_business_glossary.md_1`

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
> The migration-related data quality issues identified are:

There are referential integrity gaps: some `ord_line_item.prod_id` values point to non-existent products because the products were deleted; some orders reference customers who are marked inactive; and `inv_txn_log.user_id` has no foreign key constraint.

There are data inconsistencies: `tblProduct` contains both active and discontinued pro…

**Sources retrieved (5):** `parent_chunk_business_glossary.md_3`, `parent_chunk_data_dictionary.txt_8`, `parent_chunk_business_glossary.md_0`, `parent_chunk_business_glossary.md_2`, `parent_chunk_business_glossary.md_1`

**Context previews (first 3):**

1. _## Migration Priority Guidelines  ### Critical Path (Must Migrate First) 1. **tblCustomer** - Required for all orders 2. **tblProduct** - Required for line items and inventory 3. **vw_SalesOrderHdr** …_

2. _CardNumberText (VARCHAR 100)     - SECURITY ISSUE: Full card number stored as text! - Should be tokenized - Contains unencrypted PAN (Primary Account Number) CardHolderName (VARCHAR 100) - Cardholder …_

3. _# CustomerMaster E-Commerce System - Business Glossary  ## Document Overview **System**: CustomerMaster v3.2.1 (Legacy) **Last Updated**: March 2015 **Purpose**: Business terminology definitions for d…_

---

## Anomalies & Observations

No anomalies detected. All questions grounded with acceptable RAGAS scores.
