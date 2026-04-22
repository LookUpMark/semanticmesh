# AB-BEST — 06_edgecases_legacy — Run Analysis

**Timestamp:** 2026-04-21 21:24:05  
**Run tag:** `run-20260421_221024`

## Configuration

| Parameter | Value |
|-----------|-------|
| Extraction model | `LLM (openai/gpt-4.1-nano)` |
| Reasoning model | `openai/gpt-oss-120b` |
| Embedding model | `BAAI/bge-m3` |
| Retrieval mode | `hybrid` |
| Reranker | `True` |
| Reranker top_k | `20` |
| Chunk size / overlap | `128 / 16` |
| ER similarity threshold | `0.65` |

## Builder Results

| Metric | Value |
|--------|-------|
| Triplets extracted | 166 |
| Entities resolved | 46 |
| Tables parsed | 10 |
| Tables completed | 10 |

## Query Evaluation Summary

| Metric | Value |
|--------|-------|
| Questions | 25 |
| Grounded | **25/25 (100%)** |
| Avg GT Coverage | N/A |
| Avg Top Score | 0.6276 |
| Avg Chunk Count | 20.0 |
| Abstained | 0 |

## RAGAS Metrics

RAGAS evaluation not enabled for this run.

## Per-Question Deep Dive

### ✅ 1 — What is the purpose of the tblCustomer table?

**Status:** GROUNDED  
**GT Coverage:** N/A | **Top Score:** 0.0000 | **Gate:** `proceed`

**Expected answer:**
> The tblCustomer table stores customer master data including customer codes, names, email addresses, and region information. It uses Hungarian notation with the str prefix for string fields and contains both legacy fields (strCustID, strFullName) and new migration compatibility fields (cust_id, custo…

**System answer:**
> 

**Sources retrieved (12):** `parent_chunk_data_dictionary.txt_4`, `Customer→TBLCUSTOMER`, `parent_chunk_business_glossary.md_0`, `parent_chunk_data_dictionary.txt_5`, `parent_chunk_business_glossary.md_3`, `parent_chunk_data_dictionary.txt_7`, `VW_SALESORDERHDR→TBLCUSTOMER`, `parent_chunk_business_glossary.md_2`

---

### ✅ 2 — How are customers identified in the legacy system?

**Status:** GROUNDED  
**GT Coverage:** N/A | **Top Score:** 0.0000 | **Gate:** `proceed`

**Expected answer:**
> Customers are identified by strCustID, which is a VARCHAR(50) field containing alphanumeric customer codes inherited from an AS/400 system. These codes follow formats like C-XXXXX or REG-XXXX and can contain letters, numbers, and hyphens.

**System answer:**
> 

**Sources retrieved (12):** `parent_chunk_business_glossary.md_0`, `parent_chunk_data_dictionary.txt_4`, `parent_chunk_business_glossary.md_2`, `parent_chunk_data_dictionary.txt_5`, `Customer→TBLCUSTOMER`, `Product Active Status Flags→TBLPRODUCT`, `parent_chunk_data_dictionary.txt_6`, `Customer`

---

### ✅ 3 — What table stores order header information and what is its primary key?

**Status:** GROUNDED  
**GT Coverage:** N/A | **Top Score:** 0.0000 | **Gate:** `proceed`

**Expected answer:**
> Order header information is stored in the vw_SalesOrderHdr table despite the vw_ prefix suggesting it's a view. The primary key is lngOrderID, which is an INT field using the lng (long integer) Hungarian notation prefix.

**System answer:**
> 

**Sources retrieved (12):** `Sales Order→VW_SALESORDERHDR`, `parent_chunk_data_dictionary.txt_5`, `Payment→TBLPAYMENT`, `parent_chunk_data_dictionary.txt_7`, `parent_chunk_data_dictionary.txt_4`, `parent_chunk_business_glossary.md_3`, `Tbl Order Status History→TBLORDERSTATUSHISTORY`, `parent_chunk_business_glossary.md_0`

---

### ✅ 4 — Which table in the schema uses a SQL reserved word as its name?

**Status:** GROUNDED  
**GT Coverage:** N/A | **Top Score:** 0.0000 | **Gate:** `proceed`

**Expected answer:**
> The schema includes two tables that use SQL reserved words: 'Group' (for product categories) and 'User' (for system users). These require square bracket quoting [Group] and [User] in SQL queries to avoid syntax errors.

**System answer:**
> 

**Sources retrieved (12):** `parent_chunk_business_glossary.md_2`, `parent_chunk_data_dictionary.txt_6`, `parent_chunk_data_dictionary.txt_8`, `parent_chunk_data_dictionary.txt_5`, `parent_chunk_data_dictionary.txt_4`, `In→ORD_LINE_ITEM`, `Customer→TBLCUSTOMER`, `Product Active Status Flags→TBLPRODUCT`

---

### ✅ 5 — What is the relationship between vw_SalesOrderHdr and tblCustomer?

**Status:** GROUNDED  
**GT Coverage:** N/A | **Top Score:** 0.0000 | **Gate:** `proceed`

**Expected answer:**
> vw_SalesOrderHdr has a foreign key relationship with tblCustomer through the intCustID field, which references strCustID. Despite the int prefix suggesting an integer, intCustID is actually a VARCHAR(50) field matching the strCustID data type.

**System answer:**
> 

**Sources retrieved (12):** `VW_SALESORDERHDR→TBLCUSTOMER`, `parent_chunk_business_glossary.md_0`, `TBLPAYMENT→VW_SALESORDERHDR`, `parent_chunk_data_dictionary.txt_5`, `parent_chunk_business_glossary.md_3`, `parent_chunk_business_glossary.md_2`, `TBLORDERSTATUSHISTORY→VW_SALESORDERHDR`, `ORD_LINE_ITEM→VW_SALESORDERHDR`

---

### ✅ 6 — What naming convention is used for the inventory transaction log table?

**Status:** GROUNDED  
**GT Coverage:** N/A | **Top Score:** 0.0000 | **Gate:** `proceed`

**Expected answer:**
> The inventory transaction log table is named 'inv_txn_log' using abbreviated naming with underscore separators. Field names within this table are also heavily abbreviated: txn_id (transaction ID), txn_dt (transaction date), txn_type (transaction type), and prod_id (product ID).

**System answer:**
> 

**Sources retrieved (12):** `parent_chunk_data_dictionary.txt_6`, `In→INV_TXN_LOG`, `parent_chunk_business_glossary.md_2`, `parent_chunk_data_dictionary.txt_7`, `parent_chunk_business_glossary.md_3`, `In→ORD_LINE_ITEM`, `INV_TXN_LOG→TBLPRODUCT`, `parent_chunk_data_dictionary.txt_5`

---

### ✅ 7 — What data quality issue exists in the tblProduct unit_cost field?

**Status:** GROUNDED  
**GT Coverage:** N/A | **Top Score:** 0.0000 | **Gate:** `proceed`

**Expected answer:**
> The tblProduct.unit_cost field has an inappropriate data type - it's defined as VARCHAR(20) instead of DECIMAL. This field contains currency symbols like '$19.99' which require parsing before calculations can be performed, making it unusable for mathematical operations without transformation.

**System answer:**
> 

**Sources retrieved (12):** `parent_chunk_business_glossary.md_3`, `parent_chunk_business_glossary.md_2`, `parent_chunk_data_dictionary.txt_8`, `parent_chunk_data_dictionary.txt_6`, `parent_chunk_data_dictionary.txt_5`, `Product Active Status Flags→TBLPRODUCT`, `parent_chunk_data_dictionary.txt_7`, `ORD_LINE_ITEM→TBLPRODUCT`

---

### ✅ 8 — How does the ord_line_item table handle product data redundancy?

**Status:** GROUNDED  
**GT Coverage:** N/A | **Top Score:** 0.0000 | **Gate:** `proceed`

**Expected answer:**
> The ord_line_item table contains redundant copies of product data (product_code and item_name) that are denormalized for reporting performance and to snapshot product information at the time of order. These fields may become out of sync with the tblProduct master and should not be updated from produ…

**System answer:**
> 

**Sources retrieved (12):** `ORD_LINE_ITEM→TBLPRODUCT`, `parent_chunk_business_glossary.md_3`, `ORD_LINE_ITEM→VW_SALESORDERHDR`, `parent_chunk_business_glossary.md_2`, `In→ORD_LINE_ITEM`, `parent_chunk_data_dictionary.txt_8`, `parent_chunk_data_dictionary.txt_6`, `Product Active Status Flags→TBLPRODUCT`

---

### ✅ 9 — What are the valid values for the strOrderStatus field in vw_SalesOrderHdr?

**Status:** GROUNDED  
**GT Coverage:** N/A | **Top Score:** 0.0000 | **Gate:** `proceed`

**Expected answer:**
> The strOrderStatus field accepts three values enforced by a CHECK constraint: 'PENDING' (order received but not shipped), 'SHIPPED' (order has been shipped to customer), and 'CANCELLED' (order cancelled before shipping).

**System answer:**
> 

**Sources retrieved (12):** `parent_chunk_data_dictionary.txt_5`, `Sales Order→VW_SALESORDERHDR`, `parent_chunk_data_dictionary.txt_7`, `parent_chunk_business_glossary.md_0`, `parent_chunk_business_glossary.md_3`, `TBLORDERSTATUSHISTORY→VW_SALESORDERHDR`, `VW_SALESORDERHDR→TBLCUSTOMER`, `ORD_LINE_ITEM→VW_SALESORDERHDR`

---

### ✅ 10 — Which table stores payment information and what security issue does it have?

**Status:** GROUNDED  
**GT Coverage:** N/A | **Top Score:** 0.0000 | **Gate:** `proceed`

**Expected answer:**
> Payment information is stored in the tblPayment table. The table has a critical security issue: the CardNumberText field stores full unencrypted credit card numbers as VARCHAR(100), which is a PCI compliance violation. The system also lacks proper tokenization and encryption at rest.

**System answer:**
> 

**Sources retrieved (12):** `Payment→TBLPAYMENT`, `parent_chunk_business_glossary.md_3`, `parent_chunk_data_dictionary.txt_7`, `parent_chunk_data_dictionary.txt_8`, `Customer→TBLCUSTOMER`, `User→USER`, `Parcel Service Carrier→TBLSHIPPINGCARRIER`, `parent_chunk_data_dictionary.txt_4`

---

### ✅ 11 — What is the purpose of the bolActive field in tblCustomer and tblProduct?

**Status:** GROUNDED  
**GT Coverage:** N/A | **Top Score:** 0.0000 | **Gate:** `proceed`

**Expected answer:**
> The bolActive field (using Hungarian notation 'bol' for boolean/bit) is a flag indicating whether a record is active. In tblCustomer, it marks whether customers are included in marketing (1=active, 0=inactive). In tblProduct, it indicates product availability (1=available for sale, 0=discontinued).

**System answer:**
> 

**Sources retrieved (12):** `parent_chunk_data_dictionary.txt_4`, `parent_chunk_data_dictionary.txt_7`, `Product Active Status Flags→TBLPRODUCT`, `parent_chunk_business_glossary.md_0`, `Customer→TBLCUSTOMER`, `parent_chunk_business_glossary.md_3`, `parent_chunk_business_glossary.md_2`, `parent_chunk_data_dictionary.txt_5`

---

### ✅ 12 — How are inventory transactions tracked in the system?

**Status:** GROUNDED  
**GT Coverage:** N/A | **Top Score:** 0.0000 | **Gate:** `proceed`

**Expected answer:**
> Inventory transactions are tracked in the inv_txn_log table, which records all stock movements. Each transaction has a type (txn_type): 'IN' for receipts, 'OUT' for shipments, and 'ADJ' for corrections. The table uses heavily abbreviated field names and references products via prod_id.

**System answer:**
> 

**Sources retrieved (12):** `In→INV_TXN_LOG`, `In→ORD_LINE_ITEM`, `parent_chunk_data_dictionary.txt_6`, `parent_chunk_business_glossary.md_3`, `parent_chunk_business_glossary.md_2`, `parent_chunk_business_glossary.md_0`, `Product Active Status Flags→TBLPRODUCT`, `parent_chunk_data_dictionary.txt_7`

---

### ✅ 13 — What is the self-referencing relationship in the Group table?

**Status:** GROUNDED  
**GT Coverage:** N/A | **Top Score:** 0.0000 | **Gate:** `proceed`

**Expected answer:**
> The Group table has a self-referencing foreign key where ParentGroupID references GroupID, creating a hierarchical structure for product categories. A NULL ParentGroupID indicates a top-level group, while non-NULL values create nested category levels.

**System answer:**
> 

**Sources retrieved (12):** `GROUP→GROUP`, `parent_chunk_data_dictionary.txt_6`, `parent_chunk_business_glossary.md_2`, `Product Group→GROUP`, `parent_chunk_business_glossary.md_3`, `parent_chunk_data_dictionary.txt_8`, `parent_chunk_data_dictionary.txt_7`, `parent_chunk_data_dictionary.txt_4`

---

### ✅ 14 — What migration compatibility columns exist in tblCustomer?

**Status:** GROUNDED  
**GT Coverage:** N/A | **Top Score:** 0.0000 | **Gate:** `proceed`

**Expected answer:**
> The tblCustomer table includes cust_id (INT) and customer_name (VARCHAR 255) as migration compatibility columns alongside the legacy strCustID and strFullName fields. These are intended for the new ERP system that will use integer IDs and standardized naming conventions.

**System answer:**
> 

**Sources retrieved (12):** `parent_chunk_business_glossary.md_3`, `Customer→TBLCUSTOMER`, `parent_chunk_data_dictionary.txt_4`, `parent_chunk_business_glossary.md_0`, `parent_chunk_business_glossary.md_2`, `parent_chunk_data_dictionary.txt_5`, `VW_SALESORDERHDR→TBLCUSTOMER`, `parent_chunk_data_dictionary.txt_8`

---

### ✅ 15 — How does the system handle order status history tracking?

**Status:** GROUNDED  
**GT Coverage:** N/A | **Top Score:** 0.0000 | **Gate:** `proceed`

**Expected answer:**
> Order status changes are tracked in the tblOrderStatusHistory table, which creates an audit record for each status transition. Each history record includes OrderID, OldStatus, NewStatus, ChangedByUser, ChangedDate, and ChangeReason fields, providing a complete audit trail of order workflow.

**System answer:**
> 

**Sources retrieved (12):** `Tbl Order Status History→TBLORDERSTATUSHISTORY`, `parent_chunk_data_dictionary.txt_7`, `parent_chunk_business_glossary.md_3`, `TBLORDERSTATUSHISTORY→VW_SALESORDERHDR`, `parent_chunk_business_glossary.md_0`, `parent_chunk_data_dictionary.txt_5`, `Sales Order→VW_SALESORDERHDR`, `Payment→TBLPAYMENT`

---

### ✅ 16 — What is the inconsistent naming pattern between order tables?

**Status:** GROUNDED  
**GT Coverage:** N/A | **Top Score:** 0.0000 | **Gate:** `proceed`

**Expected answer:**
> The schema shows inconsistent naming: order headers use 'vw_SalesOrderHdr' with Hungarian notation, while line items use 'ord_line_item' with abbreviated underscore notation. Additionally, the line item table references lngOrderID but names its foreign key 'ord_id' instead of 'order_id' or 'lngOrder…

**System answer:**
> 

**Sources retrieved (12):** `parent_chunk_business_glossary.md_2`, `parent_chunk_data_dictionary.txt_5`, `parent_chunk_data_dictionary.txt_8`, `parent_chunk_business_glossary.md_3`, `parent_chunk_data_dictionary.txt_4`, `ORD_LINE_ITEM→VW_SALESORDERHDR`, `Tbl Order Status History→TBLORDERSTATUSHISTORY`, `TBLPAYMENT→VW_SALESORDERHDR`

---

### ✅ 17 — What deprecated fields exist in tblProduct and why should they be avoided?

**Status:** GROUNDED  
**GT Coverage:** N/A | **Top Score:** 0.0000 | **Gate:** `proceed`

**Expected answer:**
> The tblProduct table contains three deprecated fields: prod_num (superseded by strSKU), item_desc (superseded by strDescription), and unit_cost (wrong data type with VARCHAR instead of DECIMAL). These fields should not be used in new code as they represent outdated design decisions.

**System answer:**
> 

**Sources retrieved (12):** `parent_chunk_business_glossary.md_3`, `parent_chunk_data_dictionary.txt_5`, `parent_chunk_business_glossary.md_2`, `Product Active Status Flags→TBLPRODUCT`, `parent_chunk_data_dictionary.txt_6`, `parent_chunk_data_dictionary.txt_8`, `ORD_LINE_ITEM→TBLPRODUCT`, `INV_TXN_LOG→TBLPRODUCT`

---

### ✅ 18 — How are shipping carriers configured in the system?

**Status:** GROUNDED  
**GT Coverage:** N/A | **Top Score:** 0.0000 | **Gate:** `proceed`

**Expected answer:**
> Shipping carriers are stored in the tblShippingCarrier table with CarrierID, CarrierName, CarrierCode (for API integration), TrackingURL (with {TRACKING_NUM} placeholder), and bolActive flag. Only carriers with bolActive=1 should be offered during checkout.

**System answer:**
> 

**Sources retrieved (12):** `Parcel Service Carrier→TBLSHIPPINGCARRIER`, `parent_chunk_data_dictionary.txt_7`, `parent_chunk_business_glossary.md_3`, `parent_chunk_business_glossary.md_2`, `parent_chunk_business_glossary.md_0`, `parent_chunk_data_dictionary.txt_5`, `Sales Order→VW_SALESORDERHDR`, `Product Active Status Flags→TBLPRODUCT`

---

### ✅ 19 — What is the relationship between User table passwords and security?

**Status:** GROUNDED  
**GT Coverage:** N/A | **Top Score:** 0.0000 | **Gate:** `proceed`

**Expected answer:**
> The User table stores password hashes in the PasswordHash field, but uses SHA-256 without salt, making it vulnerable to rainbow table attacks. This is identified as a security issue in the data dictionary. Additionally, the table name 'User' is a SQL reserved word requiring square bracket quoting.

**System answer:**
> 

**Sources retrieved (12):** `parent_chunk_business_glossary.md_3`, `User→USER`, `parent_chunk_data_dictionary.txt_7`, `parent_chunk_data_dictionary.txt_8`, `parent_chunk_business_glossary.md_2`, `parent_chunk_data_dictionary.txt_6`, `In→INV_TXN_LOG`, `User`

---

### ✅ 20 — What fields in vw_SalesOrderHdr use the 'flt' Hungarian notation prefix and what do they store?

**Status:** GROUNDED  
**GT Coverage:** N/A | **Top Score:** 0.0000 | **Gate:** `proceed`

**Expected answer:**
> The vw_SalesOrderHdr table uses the 'flt' (float) prefix for three monetary fields: fltSubTotal (line item subtotal before tax), fltTaxAmount (calculated tax), and fltTotalAmount (final total including tax and shipping). Despite the 'flt' prefix suggesting floating-point, these are defined as DECIMA…

**System answer:**
> 

**Sources retrieved (12):** `Sales Order→VW_SALESORDERHDR`, `parent_chunk_business_glossary.md_3`, `parent_chunk_data_dictionary.txt_5`, `parent_chunk_business_glossary.md_2`, `parent_chunk_business_glossary.md_0`, `parent_chunk_data_dictionary.txt_7`, `ORD_LINE_ITEM→VW_SALESORDERHDR`, `TBLPAYMENT→VW_SALESORDERHDR`

---

### ✅ 21 — How does the schema handle the different date/time field naming conventions?

**Status:** GROUNDED  
**GT Coverage:** N/A | **Top Score:** 0.0000 | **Gate:** `proceed`

**Expected answer:**
> The schema uses 'dtm' (datetime) Hungarian notation prefix consistently: dtmCreated and dtmLastModified in tblCustomer, dtmOrderDate/dtmShipDate/dtmRequiredDate in vw_SalesOrderHdr, dtmIntroduced/dtmDiscontinued in tblProduct, and txn_dt in inv_txn_log (abbreviated exception). The User table breaks …

**System answer:**
> 

**Sources retrieved (12):** `parent_chunk_data_dictionary.txt_5`, `parent_chunk_business_glossary.md_2`, `parent_chunk_data_dictionary.txt_4`, `parent_chunk_data_dictionary.txt_8`, `parent_chunk_data_dictionary.txt_7`, `Tbl Order Status History→TBLORDERSTATUSHISTORY`, `User→USER`, `Sales Order→VW_SALESORDERHDR`

---

### ✅ 22 — What table prefix patterns exist in the schema and what do they indicate?

**Status:** GROUNDED  
**GT Coverage:** N/A | **Top Score:** 0.0000 | **Gate:** `proceed`

**Expected answer:**
> The schema uses multiple inconsistent table prefixes: 'tbl' for standard tables (tblCustomer, tblProduct, tblPayment, tblShippingCarrier, tblOrderStatusHistory), 'vw_' for a misnamed table (vw_SalesOrderHdr), and domain-specific prefixes 'ord_' (ord_line_item) and 'inv_' (inv_txn_log). Two tables (G…

**System answer:**
> 

**Sources retrieved (12):** `parent_chunk_data_dictionary.txt_5`, `parent_chunk_data_dictionary.txt_8`, `parent_chunk_business_glossary.md_2`, `parent_chunk_data_dictionary.txt_7`, `parent_chunk_business_glossary.md_0`, `parent_chunk_business_glossary.md_3`, `parent_chunk_data_dictionary.txt_6`, `parent_chunk_data_dictionary.txt_4`

---

### ✅ 23 — What foreign key relationships exist for the vw_SalesOrderHdr table?

**Status:** GROUNDED  
**GT Coverage:** N/A | **Top Score:** 0.0000 | **Gate:** `proceed`

**Expected answer:**
> The vw_SalesOrderHdr table has one explicit foreign key constraint: intCustID references tblCustomer.strCustID. Implicit relationships (not enforced by FK constraints) include tblPayment.OrderID, tblOrderStatusHistory.OrderID, and ord_line_item.ord_id all referencing vw_SalesOrderHdr.lngOrderID.

**System answer:**
> 

**Sources retrieved (12):** `VW_SALESORDERHDR→TBLCUSTOMER`, `ORD_LINE_ITEM→VW_SALESORDERHDR`, `TBLPAYMENT→VW_SALESORDERHDR`, `TBLORDERSTATUSHISTORY→VW_SALESORDERHDR`, `parent_chunk_data_dictionary.txt_5`, `parent_chunk_data_dictionary.txt_7`, `parent_chunk_business_glossary.md_3`, `parent_chunk_business_glossary.md_2`

---

### ✅ 24 — How does the legacy system handle product SKU format and uniqueness?

**Status:** GROUNDED  
**GT Coverage:** N/A | **Top Score:** 0.0000 | **Gate:** `proceed`

**Expected answer:**
> Product SKUs are stored in the strSKU field with a UNIQUE constraint. The format follows Category-Color-Size pattern (e.g., 'SHIRT-BLU-L'). The deprecated prod_num field also exists but should not be used. SKUs are used in foreign key references from ord_line_item through the denormalized product_co…

**System answer:**
> 

**Sources retrieved (12):** `parent_chunk_business_glossary.md_0`, `parent_chunk_business_glossary.md_2`, `parent_chunk_data_dictionary.txt_4`, `parent_chunk_data_dictionary.txt_5`, `parent_chunk_business_glossary.md_3`, `Product Active Status Flags→TBLPRODUCT`, `In→ORD_LINE_ITEM`, `ORD_LINE_ITEM→TBLPRODUCT`

---

### ✅ 25 — What are the critical data quality issues identified for migration?

**Status:** GROUNDED  
**GT Coverage:** N/A | **Top Score:** 0.0000 | **Gate:** `proceed`

**Expected answer:**
> Critical issues include: (1) PCI compliance violation - unencrypted card numbers in tblPayment.CardNumberText, (2) inappropriate data types - unit_cost as VARCHAR instead of DECIMAL, (3) missing foreign key constraints - inv_txn_log.user_id has no FK to User table, (4) security vulnerability - User.…

**System answer:**
> 

**Sources retrieved (12):** `parent_chunk_business_glossary.md_3`, `parent_chunk_data_dictionary.txt_8`, `parent_chunk_business_glossary.md_0`, `parent_chunk_business_glossary.md_2`, `parent_chunk_data_dictionary.txt_5`, `parent_chunk_data_dictionary.txt_6`, `Customer→TBLCUSTOMER`, `Product Active Status Flags→TBLPRODUCT`

---

## Anomalies & Observations

No anomalies detected. All questions grounded with acceptable RAGAS scores.
