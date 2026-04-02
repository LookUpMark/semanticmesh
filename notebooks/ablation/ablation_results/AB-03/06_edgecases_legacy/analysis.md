# AB-03 — 06_edgecases_legacy — Run Analysis

**Timestamp:** 2026-03-31 02:31:19  
**Run tag:** `v5`

## Configuration

| Parameter | Value |
|-----------|-------|
| Extraction model | `LLM (gpt-5.4-nano-2026-03-17)` |
| Reasoning model | `gpt-5.4-2026-03-05` |
| Embedding model | `BAAI/bge-m3` |
| Retrieval mode | `hybrid` |
| Reranker | `False` |
| Reranker top_k | `12` |
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
| Avg Top Score | 7.1757 |
| Avg Chunk Count | 12.0 |
| Abstained | 0 |

## RAGAS Metrics

RAGAS evaluation not enabled for this run.

## Per-Question Deep Dive

### ✅ 1 — What is the purpose of the tblCustomer table?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 3.9026 | **Gate:** `proceed`

**Expected answer:**
> The tblCustomer table stores customer master data including customer codes, names, email addresses, and region information. It uses Hungarian notation with the str prefix for string fields and contains both legacy fields (strCustID, strFullName) and new migration compatibility fields (cust_id, custo…

**System answer:**
> The `tblCustomer` table stores customer master data from the legacy CRM system. In business terms, it represents a customer: an individual or organization that has purchased products or services from the company. It holds customer records using legacy identifiers inherited from the AS/400 system, with `strCustID` as the primary key/customer code.

**Sources retrieved (12):** `parent_chunk_business_glossary.md_0`, `parent_chunk_business_glossary.md_2`, `parent_chunk_data_dictionary.txt_4`, `parent_chunk_data_dictionary.txt_7`, `parent_chunk_data_dictionary.txt_5`, `parent_chunk_business_glossary.md_3`, `parent_chunk_data_dictionary.txt_6`, `CustomerMaster v3.2.1→TBLCUSTOMER`

**Context previews (first 3):**

1. _# CustomerMaster E-Commerce System - Business Glossary  ## Document Overview **System**: CustomerMaster v3.2.1 (Legacy) **Last Updated**: March 2015 **Purpose**: Business terminology definitions for d…_

2. _## Legacy System Quirks  ### Hungarian Notation The legacy system uses Hungarian notation prefixes: - `str` = string (VARCHAR) - `int` = integer (INT) - `lng` = long integer (INT) - `flt` = float/mone…_

3. _================================================================================ CUSTOMERMASTER DATABASE - DATA DICTIONARY =============================================================================…_

---

### ✅ 2 — How are customers identified in the legacy system?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 8.4965 | **Gate:** `proceed`

**Expected answer:**
> Customers are identified by strCustID, which is a VARCHAR(50) field containing alphanumeric customer codes inherited from an AS/400 system. These codes follow formats like C-XXXXX or REG-XXXX and can contain letters, numbers, and hyphens.

**System answer:**
> In the legacy CustomerMaster system, customers are identified by the `strCustID` field in `tblCustomer`. This is the primary key and the required unique customer code for each customer. The context describes it as an alphanumeric customer identifier inherited from the AS/400 legacy system, stored as `VARCHAR(50)`, with formats such as `C-XXXXX` or `REG-XXXX`. It can contain letters, numbers, and h…

**Sources retrieved (12):** `parent_chunk_business_glossary.md_0`, `parent_chunk_business_glossary.md_2`, `parent_chunk_business_glossary.md_3`, `parent_chunk_data_dictionary.txt_4`, `parent_chunk_data_dictionary.txt_5`, `parent_chunk_data_dictionary.txt_8`, `parent_chunk_data_dictionary.txt_6`, `System users→USER`

**Context previews (first 3):**

1. _# CustomerMaster E-Commerce System - Business Glossary  ## Document Overview **System**: CustomerMaster v3.2.1 (Legacy) **Last Updated**: March 2015 **Purpose**: Business terminology definitions for d…_

2. _## Legacy System Quirks  ### Hungarian Notation The legacy system uses Hungarian notation prefixes: - `str` = string (VARCHAR) - `int` = integer (INT) - `lng` = long integer (INT) - `flt` = float/mone…_

3. _## Migration Priority Guidelines  ### Critical Path (Must Migrate First) 1. **tblCustomer** - Required for all orders 2. **tblProduct** - Required for line items and inventory 3. **vw_SalesOrderHdr** …_

---

### ✅ 3 — What table stores order header information and what is its primary key?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 9.0033 | **Gate:** `proceed`

**Expected answer:**
> Order header information is stored in the vw_SalesOrderHdr table despite the vw_ prefix suggesting it's a view. The primary key is lngOrderID, which is an INT field using the lng (long integer) Hungarian notation prefix.

**System answer:**
> The order header information is stored in `vw_SalesOrderHdr`. The retrieved context does not explicitly state the primary key for `vw_SalesOrderHdr`, so I cannot confirm it. The only related detail provided is that `tblOrderStatusHistory.OrderID` is a foreign key to `vw_SalesOrderHdr.lngOrderID`, which shows `lngOrderID` is a referenced column in the order header table, but not that it is the prim…

**Sources retrieved (12):** `payment records`, `parent_chunk_business_glossary.md_0`, `parent_chunk_business_glossary.md_2`, `parent_chunk_data_dictionary.txt_4`, `parent_chunk_data_dictionary.txt_5`, `parent_chunk_business_glossary.md_3`, `parent_chunk_data_dictionary.txt_7`, `parent_chunk_data_dictionary.txt_6`

**Context previews (first 3):**

1. _payment records: The table contains core payment transaction fields such as PaymentID, OrderID, PaymentMethod, PaymentDate, Amount, PaymentStatus, and authorization details, which strongly indicate a …_

2. _# CustomerMaster E-Commerce System - Business Glossary  ## Document Overview **System**: CustomerMaster v3.2.1 (Legacy) **Last Updated**: March 2015 **Purpose**: Business terminology definitions for d…_

3. _## Legacy System Quirks  ### Hungarian Notation The legacy system uses Hungarian notation prefixes: - `str` = string (VARCHAR) - `int` = integer (INT) - `lng` = long integer (INT) - `flt` = float/mone…_

---

### ✅ 4 — Which table in the schema uses a SQL reserved word as its name?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 9.5952 | **Gate:** `proceed`

**Expected answer:**
> The schema includes two tables that use SQL reserved words: 'Group' (for product categories) and 'User' (for system users). These require square bracket quoting [Group] and [User] in SQL queries to avoid syntax errors.

**System answer:**
> The schema uses two SQL reserved words as table names: `Group` and `User`. The context says both are reserved words and must be quoted as `[Group]` and `[User]`.

**Sources retrieved (12):** `parent_chunk_business_glossary.md_2`, `parent_chunk_business_glossary.md_0`, `parent_chunk_data_dictionary.txt_8`, `parent_chunk_data_dictionary.txt_5`, `parent_chunk_data_dictionary.txt_6`, `parent_chunk_business_glossary.md_3`, `parent_chunk_data_dictionary.txt_4`, `parent_chunk_data_dictionary.txt_7`

**Context previews (first 3):**

1. _## Legacy System Quirks  ### Hungarian Notation The legacy system uses Hungarian notation prefixes: - `str` = string (VARCHAR) - `int` = integer (INT) - `lng` = long integer (INT) - `flt` = float/mone…_

2. _# CustomerMaster E-Commerce System - Business Glossary  ## Document Overview **System**: CustomerMaster v3.2.1 (Legacy) **Last Updated**: March 2015 **Purpose**: Business terminology definitions for d…_

3. _CardNumberText (VARCHAR 100)     - SECURITY ISSUE: Full card number stored as text! - Should be tokenized - Contains unencrypted PAN (Primary Account Number) CardHolderName (VARCHAR 100) - Cardholder …_

---

### ✅ 5 — What is the relationship between vw_SalesOrderHdr and tblCustomer?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 3.9416 | **Gate:** `proceed`

**Expected answer:**
> vw_SalesOrderHdr has a foreign key relationship with tblCustomer through the intCustID field, which references strCustID. Despite the int prefix suggesting an integer, intCustID is actually a VARCHAR(50) field matching the strCustID data type.

**System answer:**
> `vw_SalesOrderHdr` references `tblCustomer` through the customer identifier: `vw_SalesOrderHdr.intCustID -> tblCustomer.strCustID`.

From the context, `tblCustomer` stores customer master data, and `vw_SalesOrderHdr` stores sales order header records, so each sales order header is associated with a customer record. This means `tblCustomer` is the parent table for customers, and `vw_SalesOrderHdr` …

**Sources retrieved (12):** `parent_chunk_business_glossary.md_2`, `parent_chunk_business_glossary.md_0`, `parent_chunk_business_glossary.md_3`, `parent_chunk_data_dictionary.txt_5`, `parent_chunk_data_dictionary.txt_7`, `parent_chunk_data_dictionary.txt_4`, `CustomerMaster v3.2.1→TBLCUSTOMER`, `Sales order header records→VW_SALESORDERHDR`

**Context previews (first 3):**

1. _## Legacy System Quirks  ### Hungarian Notation The legacy system uses Hungarian notation prefixes: - `str` = string (VARCHAR) - `int` = integer (INT) - `lng` = long integer (INT) - `flt` = float/mone…_

2. _# CustomerMaster E-Commerce System - Business Glossary  ## Document Overview **System**: CustomerMaster v3.2.1 (Legacy) **Last Updated**: March 2015 **Purpose**: Business terminology definitions for d…_

3. _## Migration Priority Guidelines  ### Critical Path (Must Migrate First) 1. **tblCustomer** - Required for all orders 2. **tblProduct** - Required for line items and inventory 3. **vw_SalesOrderHdr** …_

---

### ✅ 6 — What naming convention is used for the inventory transaction log table?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 8.5707 | **Gate:** `proceed`

**Expected answer:**
> The inventory transaction log table is named 'inv_txn_log' using abbreviated naming with underscore separators. Field names within this table are also heavily abbreviated: txn_id (transaction ID), txn_dt (transaction date), txn_type (transaction type), and prod_id (product ID).

**System answer:**
> The inventory transaction log table, `inv_txn_log`, uses a heavily abbreviated naming convention. In the broader table naming scheme, it also follows the `inv_` prefix pattern.

**Sources retrieved (12):** `parent_chunk_data_dictionary.txt_6`, `parent_chunk_business_glossary.md_0`, `parent_chunk_data_dictionary.txt_4`, `parent_chunk_data_dictionary.txt_8`, `parent_chunk_data_dictionary.txt_7`, `parent_chunk_business_glossary.md_2`, `parent_chunk_business_glossary.md_3`, `parent_chunk_data_dictionary.txt_5`

**Context previews (first 3):**

1. _qty (INT)     - Quantity ordered     - Must be positive integer  amt (DECIMAL 10,2)     - Line item total amount (qty * unit_price)     - At time of order (snapshotted, not current price)  disc_amt (D…_

2. _# CustomerMaster E-Commerce System - Business Glossary  ## Document Overview **System**: CustomerMaster v3.2.1 (Legacy) **Last Updated**: March 2015 **Purpose**: Business terminology definitions for d…_

3. _================================================================================ CUSTOMERMASTER DATABASE - DATA DICTIONARY =============================================================================…_

---

### ✅ 7 — What data quality issue exists in the tblProduct unit_cost field?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 5.5314 | **Gate:** `proceed`

**Expected answer:**
> The tblProduct.unit_cost field has an inappropriate data type - it's defined as VARCHAR(20) instead of DECIMAL. This field contains currency symbols like '$19.99' which require parsing before calculations can be performed, making it unusable for mathematical operations without transformation.

**System answer:**
> The `tblProduct.unit_cost` field has an inappropriate data type: it is stored as `VARCHAR 20` instead of a numeric type like `DECIMAL`. The context explicitly describes this as a bug, notes that it can contain currency symbols such as `"$19.99"`, and says it requires parsing before calculations.

**Sources retrieved (12):** `parent_chunk_business_glossary.md_3`, `parent_chunk_business_glossary.md_0`, `parent_chunk_data_dictionary.txt_8`, `parent_chunk_data_dictionary.txt_4`, `parent_chunk_business_glossary.md_2`, `parent_chunk_data_dictionary.txt_5`, `parent_chunk_data_dictionary.txt_7`, `parent_chunk_data_dictionary.txt_6`

**Context previews (first 3):**

1. _## Migration Priority Guidelines  ### Critical Path (Must Migrate First) 1. **tblCustomer** - Required for all orders 2. **tblProduct** - Required for line items and inventory 3. **vw_SalesOrderHdr** …_

2. _# CustomerMaster E-Commerce System - Business Glossary  ## Document Overview **System**: CustomerMaster v3.2.1 (Legacy) **Last Updated**: March 2015 **Purpose**: Business terminology definitions for d…_

3. _CardNumberText (VARCHAR 100)     - SECURITY ISSUE: Full card number stored as text! - Should be tokenized - Contains unencrypted PAN (Primary Account Number) CardHolderName (VARCHAR 100) - Cardholder …_

---

### ✅ 8 — How does the ord_line_item table handle product data redundancy?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 4.6227 | **Gate:** `proceed`

**Expected answer:**
> The ord_line_item table contains redundant copies of product data (product_code and item_name) that are denormalized for reporting performance and to snapshot product information at the time of order. These fields may become out of sync with the tblProduct master and should not be updated from produ…

**System answer:**
> The `ord_line_item` table handles product data redundancy by storing both a product reference and duplicate product attributes on the line itself.

It includes `prod_id`, which links the line item to `tblProduct.intProdID`, but it also stores `product_code` and `item_name` as redundant product data. `product_code` is a denormalized copy of `tblProduct.strSKU`, kept for reporting performance, and i…

**Sources retrieved (12):** `parent_chunk_business_glossary.md_2`, `parent_chunk_business_glossary.md_0`, `parent_chunk_data_dictionary.txt_5`, `parent_chunk_business_glossary.md_3`, `payment records`, `parent_chunk_data_dictionary.txt_4`, `parent_chunk_data_dictionary.txt_6`, `parent_chunk_data_dictionary.txt_7`

**Context previews (first 3):**

1. _## Legacy System Quirks  ### Hungarian Notation The legacy system uses Hungarian notation prefixes: - `str` = string (VARCHAR) - `int` = integer (INT) - `lng` = long integer (INT) - `flt` = float/mone…_

2. _# CustomerMaster E-Commerce System - Business Glossary  ## Document Overview **System**: CustomerMaster v3.2.1 (Legacy) **Last Updated**: March 2015 **Purpose**: Business terminology definitions for d…_

3. _strCategory (VARCHAR 100)     - Product category     - Hierarchical: "Clothing > Shirts > Casual" strBrand (VARCHAR 100) - Brand or manufacturer name - Free text field dtmIntroduced (DATETIME) - Produ…_

---

### ✅ 9 — What are the valid values for the strOrderStatus field in vw_SalesOrderHdr?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 9.0512 | **Gate:** `proceed`

**Expected answer:**
> The strOrderStatus field accepts three values enforced by a CHECK constraint: 'PENDING' (order received but not shipped), 'SHIPPED' (order has been shipped to customer), and 'CANCELLED' (order cancelled before shipping).

**System answer:**
> The retrieved context does not list the valid values for `vw_SalesOrderHdr.strOrderStatus`.

What the context does confirm is that:
`strOrderStatus` is a column in `vw_SalesOrderHdr` (the sales order header table), and order status changes are audited in `tblOrderStatusHistory` through `OldStatus` and `NewStatus`. However, no enumeration of allowed order header status values is provided.

The only…

**Sources retrieved (12):** `parent_chunk_business_glossary.md_0`, `parent_chunk_business_glossary.md_2`, `parent_chunk_business_glossary.md_3`, `parent_chunk_data_dictionary.txt_4`, `parent_chunk_data_dictionary.txt_5`, `parent_chunk_data_dictionary.txt_8`, `parent_chunk_data_dictionary.txt_7`, `parent_chunk_data_dictionary.txt_6`

**Context previews (first 3):**

1. _# CustomerMaster E-Commerce System - Business Glossary  ## Document Overview **System**: CustomerMaster v3.2.1 (Legacy) **Last Updated**: March 2015 **Purpose**: Business terminology definitions for d…_

2. _## Legacy System Quirks  ### Hungarian Notation The legacy system uses Hungarian notation prefixes: - `str` = string (VARCHAR) - `int` = integer (INT) - `lng` = long integer (INT) - `flt` = float/mone…_

3. _## Migration Priority Guidelines  ### Critical Path (Must Migrate First) 1. **tblCustomer** - Required for all orders 2. **tblProduct** - Required for line items and inventory 3. **vw_SalesOrderHdr** …_

---

### ✅ 10 — Which table stores payment information and what security issue does it have?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 14.7582 | **Gate:** `proceed`

**Expected answer:**
> Payment information is stored in the tblPayment table. The table has a critical security issue: the CardNumberText field stores full unencrypted credit card numbers as VARCHAR(100), which is a PCI compliance violation. The system also lacks proper tokenization and encryption at rest.

**System answer:**
> The payment information is stored in `tblPayment` (also shown as `TBLPAYMENT`). The context describes it as the physical table implementing the business concept “payment records,” with columns including `PaymentID`, `OrderID`, `PaymentMethod`, `PaymentDate`, `Amount`, `PaymentStatus`, `CardNumberText`, `CardHolderName`, and `AuthorizationCode`.

The security issue is that `tblPayment.CardNumberTex…

**Sources retrieved (12):** `payment records`, `parent_chunk_data_dictionary.txt_8`, `parent_chunk_business_glossary.md_3`, `parent_chunk_data_dictionary.txt_7`, `parent_chunk_data_dictionary.txt_6`, `parent_chunk_business_glossary.md_0`, `parent_chunk_business_glossary.md_2`, `parent_chunk_data_dictionary.txt_4`

**Context previews (first 3):**

1. _payment records: The table contains core payment transaction fields such as PaymentID, OrderID, PaymentMethod, PaymentDate, Amount, PaymentStatus, and authorization details, which strongly indicate a …_

2. _CardNumberText (VARCHAR 100)     - SECURITY ISSUE: Full card number stored as text! - Should be tokenized - Contains unencrypted PAN (Primary Account Number) CardHolderName (VARCHAR 100) - Cardholder …_

3. _## Migration Priority Guidelines  ### Critical Path (Must Migrate First) 1. **tblCustomer** - Required for all orders 2. **tblProduct** - Required for line items and inventory 3. **vw_SalesOrderHdr** …_

---

### ✅ 11 — What is the purpose of the bolActive field in tblCustomer and tblProduct?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 6.8504 | **Gate:** `proceed`

**Expected answer:**
> The bolActive field (using Hungarian notation 'bol' for boolean/bit) is a flag indicating whether a record is active. In tblCustomer, it marks whether customers are included in marketing (1=active, 0=inactive). In tblProduct, it indicates product availability (1=available for sale, 0=discontinued).

**System answer:**
> In `tblCustomer`, `bolActive` is used to mark whether a customer is active or inactive. The business glossary states that customers can be marked as inactive (`bolActive = 0`) but are never deleted.

For `tblProduct`, the retrieved context does not explicitly define a `bolActive` column. However, it does show the same business purpose at the product level: products are tracked as active versus dis…

**Sources retrieved (12):** `parent_chunk_business_glossary.md_0`, `parent_chunk_data_dictionary.txt_4`, `parent_chunk_business_glossary.md_2`, `parent_chunk_data_dictionary.txt_8`, `parent_chunk_data_dictionary.txt_7`, `parent_chunk_business_glossary.md_3`, `parent_chunk_data_dictionary.txt_6`, `parent_chunk_data_dictionary.txt_5`

**Context previews (first 3):**

1. _# CustomerMaster E-Commerce System - Business Glossary  ## Document Overview **System**: CustomerMaster v3.2.1 (Legacy) **Last Updated**: March 2015 **Purpose**: Business terminology definitions for d…_

2. _================================================================================ CUSTOMERMASTER DATABASE - DATA DICTIONARY =============================================================================…_

3. _## Legacy System Quirks  ### Hungarian Notation The legacy system uses Hungarian notation prefixes: - `str` = string (VARCHAR) - `int` = integer (INT) - `lng` = long integer (INT) - `flt` = float/mone…_

---

### ✅ 12 — How are inventory transactions tracked in the system?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 7.8223 | **Gate:** `proceed`

**Expected answer:**
> Inventory transactions are tracked in the inv_txn_log table, which records all stock movements. Each transaction has a type (txn_type): 'IN' for receipts, 'OUT' for shipments, and 'ADJ' for corrections. The table uses heavily abbreviated field names and references products via prod_id.

**System answer:**
> Inventory transactions are tracked in the `inv_txn_log` table. In the context, this table is explicitly described as the implementation of the business concept “inventory audit trail” and its purpose is “Inventory transaction log.”

The table records inventory activity at the transaction level using these fields: `txn_id`, `prod_id`, `txn_type`, `qty`, `txn_dt`, `ref_num`, `user_id`, and `notes`. …

**Sources retrieved (12):** `parent_chunk_business_glossary.md_0`, `parent_chunk_business_glossary.md_2`, `payment records`, `parent_chunk_business_glossary.md_3`, `parent_chunk_data_dictionary.txt_4`, `parent_chunk_data_dictionary.txt_8`, `parent_chunk_data_dictionary.txt_6`, `inventory audit trail→INV_TXN_LOG`

**Context previews (first 3):**

1. _# CustomerMaster E-Commerce System - Business Glossary  ## Document Overview **System**: CustomerMaster v3.2.1 (Legacy) **Last Updated**: March 2015 **Purpose**: Business terminology definitions for d…_

2. _## Legacy System Quirks  ### Hungarian Notation The legacy system uses Hungarian notation prefixes: - `str` = string (VARCHAR) - `int` = integer (INT) - `lng` = long integer (INT) - `flt` = float/mone…_

3. _payment records: The table contains core payment transaction fields such as PaymentID, OrderID, PaymentMethod, PaymentDate, Amount, PaymentStatus, and authorization details, which strongly indicate a …_

---

### ✅ 13 — What is the self-referencing relationship in the Group table?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 6.3195 | **Gate:** `proceed`

**Expected answer:**
> The Group table has a self-referencing foreign key where ParentGroupID references GroupID, creating a hierarchical structure for product categories. A NULL ParentGroupID indicates a top-level group, while non-NULL values create nested category levels.

**System answer:**
> The `Group` table has a self-referencing foreign key: `ParentGroupID -> Group.GroupID`. This implements a one-to-many group hierarchy, where one group can have many child groups. Because `Group` is a reserved word in the legacy system, it must be quoted as `[Group]` in SQL.

**Sources retrieved (12):** `parent_chunk_business_glossary.md_2`, `parent_chunk_data_dictionary.txt_6`, `parent_chunk_data_dictionary.txt_8`, `parent_chunk_business_glossary.md_3`, `Group Hierarchy→GROUP`, `GROUP→GROUP`, `Group Hierarchy`, `parent_chunk_business_glossary.md_0`

**Context previews (first 3):**

1. _## Legacy System Quirks  ### Hungarian Notation The legacy system uses Hungarian notation prefixes: - `str` = string (VARCHAR) - `int` = integer (INT) - `lng` = long integer (INT) - `flt` = float/mone…_

2. _qty (INT)     - Quantity ordered     - Must be positive integer  amt (DECIMAL 10,2)     - Line item total amount (qty * unit_price)     - At time of order (snapshotted, not current price)  disc_amt (D…_

3. _CardNumberText (VARCHAR 100)     - SECURITY ISSUE: Full card number stored as text! - Should be tokenized - Contains unencrypted PAN (Primary Account Number) CardHolderName (VARCHAR 100) - Cardholder …_

---

### ✅ 14 — What migration compatibility columns exist in tblCustomer?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 7.5426 | **Gate:** `proceed`

**Expected answer:**
> The tblCustomer table includes cust_id (INT) and customer_name (VARCHAR 255) as migration compatibility columns alongside the legacy strCustID and strFullName fields. These are intended for the new ERP system that will use integer IDs and standardized naming conventions.

**System answer:**
> From the retrieved context, the only explicitly identifiable migration-compatibility / legacy identifier column in `tblCustomer` is `strCustID`.

`strCustID` is defined as `VARCHAR 50` and the primary key of `tblCustomer`. It is described as:
- an alphanumeric customer code inherited from the AS/400 system,
- a legacy AS/400 customer number,
- formatted like `C-XXXXX` or `REG-XXXX`,
- containing l…

**Sources retrieved (12):** `parent_chunk_data_dictionary.txt_8`, `parent_chunk_data_dictionary.txt_4`, `parent_chunk_business_glossary.md_3`, `parent_chunk_business_glossary.md_0`, `parent_chunk_business_glossary.md_2`, `parent_chunk_data_dictionary.txt_5`, `inventory audit trail→INV_TXN_LOG`, `Group Hierarchy→GROUP`

**Context previews (first 3):**

1. _CardNumberText (VARCHAR 100)     - SECURITY ISSUE: Full card number stored as text! - Should be tokenized - Contains unencrypted PAN (Primary Account Number) CardHolderName (VARCHAR 100) - Cardholder …_

2. _================================================================================ CUSTOMERMASTER DATABASE - DATA DICTIONARY =============================================================================…_

3. _## Migration Priority Guidelines  ### Critical Path (Must Migrate First) 1. **tblCustomer** - Required for all orders 2. **tblProduct** - Required for line items and inventory 3. **vw_SalesOrderHdr** …_

---

### ✅ 15 — How does the system handle order status history tracking?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 5.4913 | **Gate:** `proceed`

**Expected answer:**
> Order status changes are tracked in the tblOrderStatusHistory table, which creates an audit record for each status transition. Each history record includes OrderID, OldStatus, NewStatus, ChangedByUser, ChangedDate, and ChangeReason fields, providing a complete audit trail of order workflow.

**System answer:**
> The system tracks order status history in the `tblOrderStatusHistory` table, whose stated purpose is an audit log of order status changes. Each history row represents one status transition for an order.

The tracking structure is as follows: `HistoryID` is the auto-increment primary key for the history record. `OrderID` is a foreign key to `vw_SalesOrderHdr.lngOrderID`, so each status change is ti…

**Sources retrieved (12):** `parent_chunk_business_glossary.md_2`, `parent_chunk_business_glossary.md_0`, `parent_chunk_data_dictionary.txt_7`, `parent_chunk_data_dictionary.txt_6`, `parent_chunk_business_glossary.md_3`, `payment records`, `parent_chunk_data_dictionary.txt_4`, `parent_chunk_data_dictionary.txt_5`

**Context previews (first 3):**

1. _## Legacy System Quirks  ### Hungarian Notation The legacy system uses Hungarian notation prefixes: - `str` = string (VARCHAR) - `int` = integer (INT) - `lng` = long integer (INT) - `flt` = float/mone…_

2. _# CustomerMaster E-Commerce System - Business Glossary  ## Document Overview **System**: CustomerMaster v3.2.1 (Legacy) **Last Updated**: March 2015 **Purpose**: Business terminology definitions for d…_

3. _Email (VARCHAR 150)     - User email address     - For notifications  LastLogin (DATETIME)     - Last successful login timestamp     - NULL for new users  CreatedDate (DATETIME)     - Account creation…_

---

### ✅ 16 — What is the inconsistent naming pattern between order tables?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 4.6274 | **Gate:** `proceed`

**Expected answer:**
> The schema shows inconsistent naming: order headers use 'vw_SalesOrderHdr' with Hungarian notation, while line items use 'ord_line_item' with abbreviated underscore notation. Additionally, the line item table references lngOrderID but names its foreign key 'ord_id' instead of 'order_id' or 'lngOrder…

**System answer:**
> The order-related tables use inconsistent prefixes rather than one naming convention. In the retrieved context, the order header is `vw_SalesOrderHdr`, which uses the `vw_` prefix even though it is actually a table; the order detail table is `ord_line_item`, which uses the `ord_` prefix; and the order status audit table is `tblOrderStatusHistory`, which uses the `tbl` prefix. So the documented inc…

**Sources retrieved (12):** `parent_chunk_data_dictionary.txt_8`, `parent_chunk_business_glossary.md_2`, `parent_chunk_data_dictionary.txt_5`, `parent_chunk_business_glossary.md_0`, `parent_chunk_business_glossary.md_3`, `parent_chunk_data_dictionary.txt_6`, `parent_chunk_data_dictionary.txt_4`, `parent_chunk_data_dictionary.txt_7`

**Context previews (first 3):**

1. _CardNumberText (VARCHAR 100)     - SECURITY ISSUE: Full card number stored as text! - Should be tokenized - Contains unencrypted PAN (Primary Account Number) CardHolderName (VARCHAR 100) - Cardholder …_

2. _## Legacy System Quirks  ### Hungarian Notation The legacy system uses Hungarian notation prefixes: - `str` = string (VARCHAR) - `int` = integer (INT) - `lng` = long integer (INT) - `flt` = float/mone…_

3. _strCategory (VARCHAR 100)     - Product category     - Hierarchical: "Clothing > Shirts > Casual" strBrand (VARCHAR 100) - Brand or manufacturer name - Free text field dtmIntroduced (DATETIME) - Produ…_

---

### ✅ 17 — What deprecated fields exist in tblProduct and why should they be avoided?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 7.5562 | **Gate:** `proceed`

**Expected answer:**
> The tblProduct table contains three deprecated fields: prod_num (superseded by strSKU), item_desc (superseded by strDescription), and unit_cost (wrong data type with VARCHAR instead of DECIMAL). These fields should not be used in new code as they represent outdated design decisions.

**System answer:**
> In `tblProduct`, the deprecated fields are `prod_num`, `item_desc`, and `unit_cost`.

`prod_num` (`VARCHAR 20`) is an old legacy product number. It has been superseded by `strSKU` and is retained only for historical reporting, so it should be avoided in new code.

`item_desc` (`VARCHAR 500`) is an old truncated description field. It has been superseded by `strDescription`, and the dictionary expli…

**Sources retrieved (12):** `parent_chunk_data_dictionary.txt_8`, `parent_chunk_business_glossary.md_3`, `parent_chunk_business_glossary.md_0`, `payment records`, `parent_chunk_data_dictionary.txt_5`, `parent_chunk_data_dictionary.txt_4`, `parent_chunk_business_glossary.md_2`, `parent_chunk_data_dictionary.txt_6`

**Context previews (first 3):**

1. _CardNumberText (VARCHAR 100)     - SECURITY ISSUE: Full card number stored as text! - Should be tokenized - Contains unencrypted PAN (Primary Account Number) CardHolderName (VARCHAR 100) - Cardholder …_

2. _## Migration Priority Guidelines  ### Critical Path (Must Migrate First) 1. **tblCustomer** - Required for all orders 2. **tblProduct** - Required for line items and inventory 3. **vw_SalesOrderHdr** …_

3. _# CustomerMaster E-Commerce System - Business Glossary  ## Document Overview **System**: CustomerMaster v3.2.1 (Legacy) **Last Updated**: March 2015 **Purpose**: Business terminology definitions for d…_

---

### ✅ 18 — How are shipping carriers configured in the system?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 5.4059 | **Gate:** `proceed`

**Expected answer:**
> Shipping carriers are stored in the tblShippingCarrier table with CarrierID, CarrierName, CarrierCode (for API integration), TrackingURL (with {TRACKING_NUM} placeholder), and bolActive flag. Only carriers with bolActive=1 should be offered during checkout.

**System answer:**
> Shipping carriers are configured as shipping carrier master data in the physical table `TBLSHIPPINGCARRIER` / `tblShippingCarrier`. The available schema fields shown are `CarrierID`, `CarrierName`, `CarrierCode`, `TrackingURL`, and `bolActive`. The glossary defines a shipping carrier as a third-party logistics provider responsible for delivering packages to customers, and says carriers are stored …

**Sources retrieved (12):** `parent_chunk_business_glossary.md_0`, `parent_chunk_business_glossary.md_2`, `parent_chunk_data_dictionary.txt_7`, `parent_chunk_data_dictionary.txt_5`, `parent_chunk_business_glossary.md_3`, `parent_chunk_data_dictionary.txt_4`, `parent_chunk_data_dictionary.txt_6`, `System users→USER`

**Context previews (first 3):**

1. _# CustomerMaster E-Commerce System - Business Glossary  ## Document Overview **System**: CustomerMaster v3.2.1 (Legacy) **Last Updated**: March 2015 **Purpose**: Business terminology definitions for d…_

2. _## Legacy System Quirks  ### Hungarian Notation The legacy system uses Hungarian notation prefixes: - `str` = string (VARCHAR) - `int` = integer (INT) - `lng` = long integer (INT) - `flt` = float/mone…_

3. _Email (VARCHAR 150)     - User email address     - For notifications  LastLogin (DATETIME)     - Last successful login timestamp     - NULL for new users  CreatedDate (DATETIME)     - Account creation…_

---

### ✅ 19 — What is the relationship between User table passwords and security?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 4.3685 | **Gate:** `proceed`

**Expected answer:**
> The User table stores password hashes in the PasswordHash field, but uses SHA-256 without salt, making it vulnerable to rainbow table attacks. This is identified as a security issue in the data dictionary. Additionally, the table name 'User' is a SQL reserved word requiring square bracket quoting.

**System answer:**
> The `User` table, which stores system users (`UserID`, `UserName`, `PasswordHash`, `UserRole`, `Email`, `LastLogin`, `CreatedDate`), has an identified security weakness: `User.PasswordHash` uses SHA-256 without salt. The context explicitly flags this as a critical security issue because it is vulnerable to rainbow table attacks. Also, because the table name is `User`, it is a reserved word and mus…

**Sources retrieved (12):** `parent_chunk_business_glossary.md_2`, `parent_chunk_business_glossary.md_0`, `payment records`, `parent_chunk_data_dictionary.txt_6`, `parent_chunk_data_dictionary.txt_8`, `parent_chunk_business_glossary.md_3`, `parent_chunk_data_dictionary.txt_7`, `inventory audit trail→INV_TXN_LOG`

**Context previews (first 3):**

1. _## Legacy System Quirks  ### Hungarian Notation The legacy system uses Hungarian notation prefixes: - `str` = string (VARCHAR) - `int` = integer (INT) - `lng` = long integer (INT) - `flt` = float/mone…_

2. _# CustomerMaster E-Commerce System - Business Glossary  ## Document Overview **System**: CustomerMaster v3.2.1 (Legacy) **Last Updated**: March 2015 **Purpose**: Business terminology definitions for d…_

3. _payment records: The table contains core payment transaction fields such as PaymentID, OrderID, PaymentMethod, PaymentDate, Amount, PaymentStatus, and authorization details, which strongly indicate a …_

---

### ✅ 20 — What fields in vw_SalesOrderHdr use the 'flt' Hungarian notation prefix and what do they store?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 11.7491 | **Gate:** `proceed`

**Expected answer:**
> The vw_SalesOrderHdr table uses the 'flt' (float) prefix for three monetary fields: fltSubTotal (line item subtotal before tax), fltTaxAmount (calculated tax), and fltTotalAmount (final total including tax and shipping). Despite the 'flt' prefix suggesting floating-point, these are defined as DECIMA…

**System answer:**
> From the retrieved context, the only `vw_SalesOrderHdr` field explicitly shown with the `flt` Hungarian notation prefix is `fltTotalAmount`. The notation guide says `flt` means a float/money field stored as `DECIMAL`, and the field name indicates it stores the order’s total amount.

The context does not include the full `vw_SalesOrderHdr` column list, so I cannot confirm whether there are addition…

**Sources retrieved (12):** `parent_chunk_data_dictionary.txt_8`, `parent_chunk_business_glossary.md_2`, `parent_chunk_business_glossary.md_3`, `parent_chunk_business_glossary.md_0`, `parent_chunk_data_dictionary.txt_5`, `payment records`, `parent_chunk_data_dictionary.txt_4`, `parent_chunk_data_dictionary.txt_7`

**Context previews (first 3):**

1. _CardNumberText (VARCHAR 100)     - SECURITY ISSUE: Full card number stored as text! - Should be tokenized - Contains unencrypted PAN (Primary Account Number) CardHolderName (VARCHAR 100) - Cardholder …_

2. _## Legacy System Quirks  ### Hungarian Notation The legacy system uses Hungarian notation prefixes: - `str` = string (VARCHAR) - `int` = integer (INT) - `lng` = long integer (INT) - `flt` = float/mone…_

3. _## Migration Priority Guidelines  ### Critical Path (Must Migrate First) 1. **tblCustomer** - Required for all orders 2. **tblProduct** - Required for line items and inventory 3. **vw_SalesOrderHdr** …_

---

### ✅ 21 — How does the schema handle the different date/time field naming conventions?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 5.5040 | **Gate:** `proceed`

**Expected answer:**
> The schema uses 'dtm' (datetime) Hungarian notation prefix consistently: dtmCreated and dtmLastModified in tblCustomer, dtmOrderDate/dtmShipDate/dtmRequiredDate in vw_SalesOrderHdr, dtmIntroduced/dtmDiscontinued in tblProduct, and txn_dt in inv_txn_log (abbreviated exception). The User table breaks …

**System answer:**
> The schema handles date/time field names inconsistently across modules.

In the legacy Hungarian notation pattern, `dtm` indicates a `DATETIME` field. The context explicitly defines `dtm = datetime (DATETIME)`, and examples include `dtmIntroduced`, `dtmDiscontinued`, and the business term `dtmRequiredDate`. The `tblCustomer` area is also described as using Hungarian notation.

But other parts of t…

**Sources retrieved (12):** `parent_chunk_business_glossary.md_2`, `parent_chunk_data_dictionary.txt_5`, `parent_chunk_data_dictionary.txt_6`, `parent_chunk_data_dictionary.txt_4`, `parent_chunk_data_dictionary.txt_7`, `parent_chunk_business_glossary.md_0`, `parent_chunk_data_dictionary.txt_8`, `parent_chunk_business_glossary.md_3`

**Context previews (first 3):**

1. _## Legacy System Quirks  ### Hungarian Notation The legacy system uses Hungarian notation prefixes: - `str` = string (VARCHAR) - `int` = integer (INT) - `lng` = long integer (INT) - `flt` = float/mone…_

2. _strCategory (VARCHAR 100)     - Product category     - Hierarchical: "Clothing > Shirts > Casual" strBrand (VARCHAR 100) - Brand or manufacturer name - Free text field dtmIntroduced (DATETIME) - Produ…_

3. _qty (INT)     - Quantity ordered     - Must be positive integer  amt (DECIMAL 10,2)     - Line item total amount (qty * unit_price)     - At time of order (snapshotted, not current price)  disc_amt (D…_

---

### ✅ 22 — What table prefix patterns exist in the schema and what do they indicate?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 5.6543 | **Gate:** `proceed`

**Expected answer:**
> The schema uses multiple inconsistent table prefixes: 'tbl' for standard tables (tblCustomer, tblProduct, tblPayment, tblShippingCarrier, tblOrderStatusHistory), 'vw_' for a misnamed table (vw_SalesOrderHdr), and domain-specific prefixes 'ord_' (ord_line_item) and 'inv_' (inv_txn_log). Two tables (G…

**System answer:**
> The schema uses inconsistent table naming patterns.

The explicit table prefix patterns are `tbl`, `vw_`, `ord_`, and `inv_`, plus some tables with no prefix at all.

`tbl` is used for tables such as `tblCustomer`, `tblProduct`, `tblPayment`, `tblOrderStatusHistory`, and `tblShippingCarrier`. It indicates the conventional “table” naming style.

`vw_` appears in names such as `vw_SalesOrderHdr`, bu…

**Sources retrieved (12):** `parent_chunk_business_glossary.md_0`, `parent_chunk_data_dictionary.txt_5`, `parent_chunk_business_glossary.md_2`, `payment records`, `parent_chunk_data_dictionary.txt_8`, `parent_chunk_business_glossary.md_3`, `parent_chunk_data_dictionary.txt_6`, `parent_chunk_data_dictionary.txt_7`

**Context previews (first 3):**

1. _# CustomerMaster E-Commerce System - Business Glossary  ## Document Overview **System**: CustomerMaster v3.2.1 (Legacy) **Last Updated**: March 2015 **Purpose**: Business terminology definitions for d…_

2. _strCategory (VARCHAR 100)     - Product category     - Hierarchical: "Clothing > Shirts > Casual" strBrand (VARCHAR 100) - Brand or manufacturer name - Free text field dtmIntroduced (DATETIME) - Produ…_

3. _## Legacy System Quirks  ### Hungarian Notation The legacy system uses Hungarian notation prefixes: - `str` = string (VARCHAR) - `int` = integer (INT) - `lng` = long integer (INT) - `flt` = float/mone…_

---

### ✅ 23 — What foreign key relationships exist for the vw_SalesOrderHdr table?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 4.4242 | **Gate:** `proceed`

**Expected answer:**
> The vw_SalesOrderHdr table has one explicit foreign key constraint: intCustID references tblCustomer.strCustID. Implicit relationships (not enforced by FK constraints) include tblPayment.OrderID, tblOrderStatusHistory.OrderID, and ord_line_item.ord_id all referencing vw_SalesOrderHdr.lngOrderID.

**System answer:**
> For `vw_SalesOrderHdr`, the retrieved context shows these foreign key relationships:

`vw_SalesOrderHdr` has an outgoing foreign key to `tblCustomer`: `vw_SalesOrderHdr.intCustID` -> `tblCustomer.strCustID`.

It also has incoming foreign keys from other tables:
`ord_line_item.ord_id` -> `vw_SalesOrderHdr.lngOrderID`.
`tblOrderStatusHistory.OrderID` -> `vw_SalesOrderHdr.lngOrderID`.

The mapped col…

**Sources retrieved (12):** `parent_chunk_data_dictionary.txt_5`, `parent_chunk_data_dictionary.txt_7`, `parent_chunk_data_dictionary.txt_6`, `parent_chunk_business_glossary.md_3`, `parent_chunk_data_dictionary.txt_8`, `parent_chunk_data_dictionary.txt_4`, `parent_chunk_business_glossary.md_2`, `parent_chunk_business_glossary.md_0`

**Context previews (first 3):**

1. _strCategory (VARCHAR 100)     - Product category     - Hierarchical: "Clothing > Shirts > Casual" strBrand (VARCHAR 100) - Brand or manufacturer name - Free text field dtmIntroduced (DATETIME) - Produ…_

2. _Email (VARCHAR 150)     - User email address     - For notifications  LastLogin (DATETIME)     - Last successful login timestamp     - NULL for new users  CreatedDate (DATETIME)     - Account creation…_

3. _qty (INT)     - Quantity ordered     - Must be positive integer  amt (DECIMAL 10,2)     - Line item total amount (qty * unit_price)     - At time of order (snapshotted, not current price)  disc_amt (D…_

---

### ✅ 24 — How does the legacy system handle product SKU format and uniqueness?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 7.1977 | **Gate:** `proceed`

**Expected answer:**
> Product SKUs are stored in the strSKU field with a UNIQUE constraint. The format follows Category-Color-Size pattern (e.g., 'SHIRT-BLU-L'). The deprecated prod_num field also exists but should not be used. SKUs are used in foreign key references from ord_line_item through the denormalized product_co…

**System answer:**
> From the retrieved context, the legacy product identifier is `tblProduct.strSKU`. The older field `prod_num` is marked as deprecated and “superseded by `strSKU`,” but retained for historical reporting.

On format and uniqueness, the context is only partial. It does state a data inconsistency: `tblProduct` contains both active and discontinued products with the same SKU pattern. That means SKU patt…

**Sources retrieved (12):** `parent_chunk_business_glossary.md_0`, `parent_chunk_data_dictionary.txt_4`, `parent_chunk_business_glossary.md_2`, `parent_chunk_business_glossary.md_3`, `parent_chunk_data_dictionary.txt_6`, `parent_chunk_data_dictionary.txt_5`, `Group Hierarchy→GROUP`, `System users→USER`

**Context previews (first 3):**

1. _# CustomerMaster E-Commerce System - Business Glossary  ## Document Overview **System**: CustomerMaster v3.2.1 (Legacy) **Last Updated**: March 2015 **Purpose**: Business terminology definitions for d…_

2. _================================================================================ CUSTOMERMASTER DATABASE - DATA DICTIONARY =============================================================================…_

3. _## Legacy System Quirks  ### Hungarian Notation The legacy system uses Hungarian notation prefixes: - `str` = string (VARCHAR) - `int` = integer (INT) - `lng` = long integer (INT) - `flt` = float/mone…_

---

### ✅ 25 — What are the critical data quality issues identified for migration?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 11.4062 | **Gate:** `proceed`

**Expected answer:**
> Critical issues include: (1) PCI compliance violation - unencrypted card numbers in tblPayment.CardNumberText, (2) inappropriate data types - unit_cost as VARCHAR instead of DECIMAL, (3) missing foreign key constraints - inv_txn_log.user_id has no FK to User table, (4) security vulnerability - User.…

**System answer:**
> The migration assessment identifies these data quality issues:

Referential integrity gaps: some `ord_line_item.prod_id` values reference non-existent products because the products were deleted; some orders reference customers marked as inactive; and `inv_txn_log.user_id` has no foreign key constraint.

Data inconsistencies: `tblProduct` contains both active and discontinued products with the same…

**Sources retrieved (12):** `parent_chunk_business_glossary.md_3`, `parent_chunk_business_glossary.md_0`, `parent_chunk_business_glossary.md_2`, `parent_chunk_data_dictionary.txt_8`, `parent_chunk_data_dictionary.txt_7`, `parent_chunk_data_dictionary.txt_4`, `parent_chunk_data_dictionary.txt_6`, `payment records`

**Context previews (first 3):**

1. _## Migration Priority Guidelines  ### Critical Path (Must Migrate First) 1. **tblCustomer** - Required for all orders 2. **tblProduct** - Required for line items and inventory 3. **vw_SalesOrderHdr** …_

2. _# CustomerMaster E-Commerce System - Business Glossary  ## Document Overview **System**: CustomerMaster v3.2.1 (Legacy) **Last Updated**: March 2015 **Purpose**: Business terminology definitions for d…_

3. _## Legacy System Quirks  ### Hungarian Notation The legacy system uses Hungarian notation prefixes: - `str` = string (VARCHAR) - `int` = integer (INT) - `lng` = long integer (INT) - `flt` = float/mone…_

---

## Anomalies & Observations

No anomalies detected. All questions grounded with acceptable RAGAS scores.
