# AB-01 — 06_edgecases_legacy — Run Analysis

**Timestamp:** 2026-03-31 02:22:24  
**Run tag:** `v5`

## Configuration

| Parameter | Value |
|-----------|-------|
| Extraction model | `LLM (gpt-5.4-nano-2026-03-17)` |
| Reasoning model | `gpt-5.4-2026-03-05` |
| Embedding model | `BAAI/bge-m3` |
| Retrieval mode | `vector` |
| Reranker | `True` |
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
| Avg Top Score | 0.0934 |
| Avg Chunk Count | 5.0 |
| Abstained | 0 |

## RAGAS Metrics

RAGAS evaluation not enabled for this run.

## Per-Question Deep Dive

### ✅ 1 — What is the purpose of the tblCustomer table?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0097 | **Gate:** `proceed_with_warning`

**Expected answer:**
> The tblCustomer table stores customer master data including customer codes, names, email addresses, and region information. It uses Hungarian notation with the str prefix for string fields and contains both legacy fields (strCustID, strFullName) and new migration compatibility fields (cust_id, custo…

**System answer:**
> I cannot determine the purpose of the tblCustomer table from the retrieved context. The only customer-related item present is the business concept name “CustomerMaster v3.2.1,” but it includes no description, columns, relationships, or explicit mapping to a table named tblCustomer.

**Sources retrieved (5):** `payment records`, `Order line items`, `Group Hierarchy`, `CustomerMaster v3.2.1`, `Shipping carrier master data`

**Context previews (first 3):**

1. _payment records: The table contains core payment transaction fields such as PaymentID, OrderID, PaymentMethod, PaymentDate, Amount, PaymentStatus, and authorization details, which strongly indicate a …_

2. _Order line items: The table is clearly an order-detail structure: it links a single order to a product and captures quantity, total amount, discount amount, and line status. The schema supports line-i…_

3. _Group Hierarchy: The table is a self-referencing group/category structure with ParentGroupID and contains only generic group attributes, which aligns most closely with a hierarchical group concept rat…_

---

### ✅ 2 — How are customers identified in the legacy system?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0000 | **Gate:** `proceed_with_warning`

**Expected answer:**
> Customers are identified by strCustID, which is a VARCHAR(50) field containing alphanumeric customer codes inherited from an AS/400 system. These codes follow formats like C-XXXXX or REG-XXXX and can contain letters, numbers, and hyphens.

**System answer:**
> From the retrieved context, the only customer-related information is the business concept name "CustomerMaster v3.2.1". There is no description of its fields, keys, identifiers, or any legacy-system-specific customer ID mechanism.

So, based on the available context, I cannot determine how customers are identified in the legacy system. What is known is only that a customer master concept exists; w…

**Sources retrieved (5):** `Group Hierarchy`, `payment records`, `Order line items`, `CustomerMaster v3.2.1`, `Shipping carrier master data`

**Context previews (first 3):**

1. _Group Hierarchy: The table is a self-referencing group/category structure with ParentGroupID and contains only generic group attributes, which aligns most closely with a hierarchical group concept rat…_

2. _payment records: The table contains core payment transaction fields such as PaymentID, OrderID, PaymentMethod, PaymentDate, Amount, PaymentStatus, and authorization details, which strongly indicate a …_

3. _Order line items: The table is clearly an order-detail structure: it links a single order to a product and captures quantity, total amount, discount amount, and line status. The schema supports line-i…_

---

### ✅ 3 — What table stores order header information and what is its primary key?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.5104 | **Gate:** `proceed`

**Expected answer:**
> Order header information is stored in the vw_SalesOrderHdr table despite the vw_ prefix suggesting it's a view. The primary key is lngOrderID, which is an INT field using the lng (long integer) Hungarian notation prefix.

**System answer:**
> The retrieved context does not identify the table that stores order header information or state its primary key.

The only related fact is from the payment records concept, which says the payment table “references an order header” and includes an OrderID field. That suggests OrderID is related to the order header entity, but the actual order header table name and its primary key are not provided i…

**Sources retrieved (5):** `payment records`, `Order line items`, `Group Hierarchy`, `Shipping carrier master data`, `CustomerMaster v3.2.1`

**Context previews (first 3):**

1. _payment records: The table contains core payment transaction fields such as PaymentID, OrderID, PaymentMethod, PaymentDate, Amount, PaymentStatus, and authorization details, which strongly indicate a …_

2. _Order line items: The table is clearly an order-detail structure: it links a single order to a product and captures quantity, total amount, discount amount, and line status. The schema supports line-i…_

3. _Group Hierarchy: The table is a self-referencing group/category structure with ParentGroupID and contains only generic group attributes, which aligns most closely with a hierarchical group concept rat…_

---

### ✅ 4 — Which table in the schema uses a SQL reserved word as its name?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0074 | **Gate:** `proceed_with_warning`

**Expected answer:**
> The schema includes two tables that use SQL reserved words: 'Group' (for product categories) and 'User' (for system users). These require square bracket quoting [Group] and [User] in SQL queries to avoid syntax errors.

**System answer:**
> The retrieved context does not identify any physical table name that is a SQL reserved word.

The closest related item is the business concept "Group Hierarchy", which describes a self-referencing Group → Group structure with ParentGroupID, but it does not explicitly state the actual schema table name. Because the context only provides business concept descriptions and not a confirmed physical tab…

**Sources retrieved (5):** `payment records`, `Order line items`, `Group Hierarchy`, `Shipping carrier master data`, `CustomerMaster v3.2.1`

**Context previews (first 3):**

1. _payment records: The table contains core payment transaction fields such as PaymentID, OrderID, PaymentMethod, PaymentDate, Amount, PaymentStatus, and authorization details, which strongly indicate a …_

2. _Order line items: The table is clearly an order-detail structure: it links a single order to a product and captures quantity, total amount, discount amount, and line status. The schema supports line-i…_

3. _Group Hierarchy: The table is a self-referencing group/category structure with ParentGroupID and contains only generic group attributes, which aligns most closely with a hierarchical group concept rat…_

---

### ✅ 5 — What is the relationship between vw_SalesOrderHdr and tblCustomer?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0002 | **Gate:** `proceed_with_warning`

**Expected answer:**
> vw_SalesOrderHdr has a foreign key relationship with tblCustomer through the intCustID field, which references strCustID. Despite the int prefix suggesting an integer, intCustID is actually a VARCHAR(50) field matching the strCustID data type.

**System answer:**
> I cannot determine the relationship between vw_SalesOrderHdr and tblCustomer from the retrieved context. The context does not mention vw_SalesOrderHdr, tblCustomer, or any foreign key, join path, or business rule connecting them.

What is present is only high-level metadata for payment records, order line items, group hierarchy, CustomerMaster v3.2.1, and shipping carrier master data. None of thos…

**Sources retrieved (5):** `payment records`, `Order line items`, `Group Hierarchy`, `CustomerMaster v3.2.1`, `Shipping carrier master data`

**Context previews (first 3):**

1. _payment records: The table contains core payment transaction fields such as PaymentID, OrderID, PaymentMethod, PaymentDate, Amount, PaymentStatus, and authorization details, which strongly indicate a …_

2. _Order line items: The table is clearly an order-detail structure: it links a single order to a product and captures quantity, total amount, discount amount, and line status. The schema supports line-i…_

3. _Group Hierarchy: The table is a self-referencing group/category structure with ParentGroupID and contains only generic group attributes, which aligns most closely with a hierarchical group concept rat…_

---

### ✅ 6 — What naming convention is used for the inventory transaction log table?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0031 | **Gate:** `proceed_with_warning`

**Expected answer:**
> The inventory transaction log table is named 'inv_txn_log' using abbreviated naming with underscore separators. Field names within this table are also heavily abbreviated: txn_id (transaction ID), txn_dt (transaction date), txn_type (transaction type), and prod_id (product ID).

**System answer:**
> The retrieved context does not provide any information about an inventory transaction log table, so the naming convention for that table cannot be determined.

What is known from the context is limited to these concepts: payment records, order line items, group hierarchy, shipping carrier master data, and CustomerMaster v3.2.1. None of those entries describes an inventory transaction log table or …

**Sources retrieved (5):** `payment records`, `Order line items`, `Group Hierarchy`, `Shipping carrier master data`, `CustomerMaster v3.2.1`

**Context previews (first 3):**

1. _payment records: The table contains core payment transaction fields such as PaymentID, OrderID, PaymentMethod, PaymentDate, Amount, PaymentStatus, and authorization details, which strongly indicate a …_

2. _Order line items: The table is clearly an order-detail structure: it links a single order to a product and captures quantity, total amount, discount amount, and line status. The schema supports line-i…_

3. _Group Hierarchy: The table is a self-referencing group/category structure with ParentGroupID and contains only generic group attributes, which aligns most closely with a hierarchical group concept rat…_

---

### ✅ 7 — What data quality issue exists in the tblProduct unit_cost field?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0108 | **Gate:** `proceed_with_warning`

**Expected answer:**
> The tblProduct.unit_cost field has an inappropriate data type - it's defined as VARCHAR(20) instead of DECIMAL. This field contains currency symbols like '$19.99' which require parsing before calculations can be performed, making it unusable for mathematical operations without transformation.

**System answer:**
> I cannot determine any data quality issue for the tblProduct unit_cost field from the retrieved context.

What the context does contain is only high-level business-concept information for payment records, shipping carrier master data, order line items, group hierarchy, and CustomerMaster v3.2.1. The only product-related detail mentioned is that the order line items concept lacks an explicit unit_p…

**Sources retrieved (5):** `payment records`, `Shipping carrier master data`, `Order line items`, `Group Hierarchy`, `CustomerMaster v3.2.1`

**Context previews (first 3):**

1. _payment records: The table contains core payment transaction fields such as PaymentID, OrderID, PaymentMethod, PaymentDate, Amount, PaymentStatus, and authorization details, which strongly indicate a …_

2. _Shipping carrier master data…_

3. _Order line items: The table is clearly an order-detail structure: it links a single order to a product and captures quantity, total amount, discount amount, and line status. The schema supports line-i…_

---

### ✅ 8 — How does the ord_line_item table handle product data redundancy?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.4886 | **Gate:** `proceed`

**Expected answer:**
> The ord_line_item table contains redundant copies of product data (product_code and item_name) that are denormalized for reporting performance and to snapshot product information at the time of order. These fields may become out of sync with the tblProduct master and should not be updated from produ…

**System answer:**
> From the retrieved context, only a limited schema-level description is available for the order line item concept: it “links a single order to a product and captures quantity, total amount, discount amount, and line status.”

Based on that, what is known is that the order-line-item structure associates an order with a product rather than describing broad product details in the context provided. How…

**Sources retrieved (5):** `payment records`, `Order line items`, `Group Hierarchy`, `Shipping carrier master data`, `CustomerMaster v3.2.1`

**Context previews (first 3):**

1. _payment records: The table contains core payment transaction fields such as PaymentID, OrderID, PaymentMethod, PaymentDate, Amount, PaymentStatus, and authorization details, which strongly indicate a …_

2. _Order line items: The table is clearly an order-detail structure: it links a single order to a product and captures quantity, total amount, discount amount, and line status. The schema supports line-i…_

3. _Group Hierarchy: The table is a self-referencing group/category structure with ParentGroupID and contains only generic group attributes, which aligns most closely with a hierarchical group concept rat…_

---

### ✅ 9 — What are the valid values for the strOrderStatus field in vw_SalesOrderHdr?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0013 | **Gate:** `proceed_with_warning`

**Expected answer:**
> The strOrderStatus field accepts three values enforced by a CHECK constraint: 'PENDING' (order received but not shipped), 'SHIPPED' (order has been shipped to customer), and 'CANCELLED' (order cancelled before shipping).

**System answer:**
> The retrieved context does not define vw_SalesOrderHdr or the strOrderStatus field, so the valid values for strOrderStatus cannot be determined from this knowledge graph.

What is known from the context is only that there is an Order line items concept with a line status, and a payment records concept with a PaymentStatus field. However, those are different status fields and do not provide the val…

**Sources retrieved (5):** `payment records`, `Order line items`, `Group Hierarchy`, `CustomerMaster v3.2.1`, `Shipping carrier master data`

**Context previews (first 3):**

1. _payment records: The table contains core payment transaction fields such as PaymentID, OrderID, PaymentMethod, PaymentDate, Amount, PaymentStatus, and authorization details, which strongly indicate a …_

2. _Order line items: The table is clearly an order-detail structure: it links a single order to a product and captures quantity, total amount, discount amount, and line status. The schema supports line-i…_

3. _Group Hierarchy: The table is a self-referencing group/category structure with ParentGroupID and contains only generic group attributes, which aligns most closely with a hierarchical group concept rat…_

---

### ✅ 10 — Which table stores payment information and what security issue does it have?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.3340 | **Gate:** `proceed`

**Expected answer:**
> Payment information is stored in the tblPayment table. The table has a critical security issue: the CardNumberText field stores full unencrypted credit card numbers as VARCHAR(100), which is a PCI compliance violation. The system also lacks proper tokenization and encryption at rest.

**System answer:**
> The table identified as payment records stores the payment information. It contains fields such as PaymentID, OrderID, PaymentMethod, PaymentDate, Amount, PaymentStatus, and authorization details, and it physically stores individual payment transactions.

The security issue called out in the context is that it includes sensitive card data.

**Sources retrieved (5):** `payment records`, `Order line items`, `Group Hierarchy`, `CustomerMaster v3.2.1`, `Shipping carrier master data`

**Context previews (first 3):**

1. _payment records: The table contains core payment transaction fields such as PaymentID, OrderID, PaymentMethod, PaymentDate, Amount, PaymentStatus, and authorization details, which strongly indicate a …_

2. _Order line items: The table is clearly an order-detail structure: it links a single order to a product and captures quantity, total amount, discount amount, and line status. The schema supports line-i…_

3. _Group Hierarchy: The table is a self-referencing group/category structure with ParentGroupID and contains only generic group attributes, which aligns most closely with a hierarchical group concept rat…_

---

### ✅ 11 — What is the purpose of the bolActive field in tblCustomer and tblProduct?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0015 | **Gate:** `proceed_with_warning`

**Expected answer:**
> The bolActive field (using Hungarian notation 'bol' for boolean/bit) is a flag indicating whether a record is active. In tblCustomer, it marks whether customers are included in marketing (1=active, 0=inactive). In tblProduct, it indicates product availability (1=available for sale, 0=discontinued).

**System answer:**
> I cannot determine the purpose of the bolActive field in tblCustomer or tblProduct from the retrieved context. The context only mentions the business concepts CustomerMaster v3.2.1, payment records, Order line items, Group Hierarchy, and Shipping carrier master data, and it does not provide any column definitions or table metadata for tblCustomer, tblProduct, or a field named bolActive.

**Sources retrieved (5):** `payment records`, `Order line items`, `Group Hierarchy`, `CustomerMaster v3.2.1`, `Shipping carrier master data`

**Context previews (first 3):**

1. _payment records: The table contains core payment transaction fields such as PaymentID, OrderID, PaymentMethod, PaymentDate, Amount, PaymentStatus, and authorization details, which strongly indicate a …_

2. _Order line items: The table is clearly an order-detail structure: it links a single order to a product and captures quantity, total amount, discount amount, and line status. The schema supports line-i…_

3. _Group Hierarchy: The table is a self-referencing group/category structure with ParentGroupID and contains only generic group attributes, which aligns most closely with a hierarchical group concept rat…_

---

### ✅ 12 — How are inventory transactions tracked in the system?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0017 | **Gate:** `proceed_with_warning`

**Expected answer:**
> Inventory transactions are tracked in the inv_txn_log table, which records all stock movements. Each transaction has a type (txn_type): 'IN' for receipts, 'OUT' for shipments, and 'ADJ' for corrections. The table uses heavily abbreviated field names and references products via prod_id.

**System answer:**
> The retrieved context does not describe any inventory transaction entity, stock movement table, or inventory-tracking process, so it is not possible to determine how inventory transactions are tracked in the system.

What is known from the context is limited to other areas of the schema: a payment record concept with fields such as PaymentID, OrderID, PaymentMethod, PaymentDate, Amount, PaymentSta…

**Sources retrieved (5):** `payment records`, `Group Hierarchy`, `Order line items`, `CustomerMaster v3.2.1`, `Shipping carrier master data`

**Context previews (first 3):**

1. _payment records: The table contains core payment transaction fields such as PaymentID, OrderID, PaymentMethod, PaymentDate, Amount, PaymentStatus, and authorization details, which strongly indicate a …_

2. _Group Hierarchy: The table is a self-referencing group/category structure with ParentGroupID and contains only generic group attributes, which aligns most closely with a hierarchical group concept rat…_

3. _Order line items: The table is clearly an order-detail structure: it links a single order to a product and captures quantity, total amount, discount amount, and line status. The schema supports line-i…_

---

### ✅ 13 — What is the self-referencing relationship in the Group table?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.8376 | **Gate:** `proceed`

**Expected answer:**
> The Group table has a self-referencing foreign key where ParentGroupID references GroupID, creating a hierarchical structure for product categories. A NULL ParentGroupID indicates a top-level group, while non-NULL values create nested category levels.

**System answer:**
> The Group table has a self-referencing hierarchy through ParentGroupID. This means one Group can act as the parent of many child Groups, forming a one-to-many Group → Group hierarchical/category structure.

**Sources retrieved (5):** `Group Hierarchy`, `payment records`, `Order line items`, `CustomerMaster v3.2.1`, `Shipping carrier master data`

**Context previews (first 3):**

1. _Group Hierarchy: The table is a self-referencing group/category structure with ParentGroupID and contains only generic group attributes, which aligns most closely with a hierarchical group concept rat…_

2. _payment records: The table contains core payment transaction fields such as PaymentID, OrderID, PaymentMethod, PaymentDate, Amount, PaymentStatus, and authorization details, which strongly indicate a …_

3. _Order line items: The table is clearly an order-detail structure: it links a single order to a product and captures quantity, total amount, discount amount, and line status. The schema supports line-i…_

---

### ✅ 14 — What migration compatibility columns exist in tblCustomer?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0001 | **Gate:** `proceed_with_warning`

**Expected answer:**
> The tblCustomer table includes cust_id (INT) and customer_name (VARCHAR 255) as migration compatibility columns alongside the legacy strCustID and strFullName fields. These are intended for the new ERP system that will use integer IDs and standardized naming conventions.

**System answer:**
> The retrieved context does not mention a table named tblCustomer, so I cannot verify any migration compatibility columns for it.

The only customer-related item in the context is the business concept name CustomerMaster v3.2.1, and it includes no column definitions or schema details. Because of that, the migration compatibility columns for tblCustomer cannot be determined from the provided context…

**Sources retrieved (5):** `payment records`, `Order line items`, `Group Hierarchy`, `CustomerMaster v3.2.1`, `Shipping carrier master data`

**Context previews (first 3):**

1. _payment records: The table contains core payment transaction fields such as PaymentID, OrderID, PaymentMethod, PaymentDate, Amount, PaymentStatus, and authorization details, which strongly indicate a …_

2. _Order line items: The table is clearly an order-detail structure: it links a single order to a product and captures quantity, total amount, discount amount, and line status. The schema supports line-i…_

3. _Group Hierarchy: The table is a self-referencing group/category structure with ParentGroupID and contains only generic group attributes, which aligns most closely with a hierarchical group concept rat…_

---

### ✅ 15 — How does the system handle order status history tracking?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0071 | **Gate:** `proceed_with_warning`

**Expected answer:**
> Order status changes are tracked in the tblOrderStatusHistory table, which creates an audit record for each status transition. Each history record includes OrderID, OldStatus, NewStatus, ChangedByUser, ChangedDate, and ChangeReason fields, providing a complete audit trail of order workflow.

**System answer:**
> The retrieved context does not describe how order status history is tracked.

What is known from the context is only that an “Order line items” table exists and it includes a line status, and that a “payment records” table includes a PaymentStatus for payment transactions. However, there is no table, column set, or business concept in the provided context for order status history, status-change ti…

**Sources retrieved (5):** `payment records`, `Order line items`, `CustomerMaster v3.2.1`, `Group Hierarchy`, `Shipping carrier master data`

**Context previews (first 3):**

1. _payment records: The table contains core payment transaction fields such as PaymentID, OrderID, PaymentMethod, PaymentDate, Amount, PaymentStatus, and authorization details, which strongly indicate a …_

2. _Order line items: The table is clearly an order-detail structure: it links a single order to a product and captures quantity, total amount, discount amount, and line status. The schema supports line-i…_

3. _CustomerMaster v3.2.1…_

---

### ✅ 16 — What is the inconsistent naming pattern between order tables?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0152 | **Gate:** `proceed_with_warning`

**Expected answer:**
> The schema shows inconsistent naming: order headers use 'vw_SalesOrderHdr' with Hungarian notation, while line items use 'ord_line_item' with abbreviated underscore notation. Additionally, the line item table references lngOrderID but names its foreign key 'ord_id' instead of 'order_id' or 'lngOrder…

**System answer:**
> From the retrieved context, the only inconsistency that can be inferred is conceptual: one order-related table is referred to as an order header (mentioned in payment records as “references an order header”), while another is described as an order-detail structure / Order line items. That suggests mixed naming around order tables using header/detail terminology versus line-item terminology.

The e…

**Sources retrieved (5):** `payment records`, `Order line items`, `Group Hierarchy`, `Shipping carrier master data`, `CustomerMaster v3.2.1`

**Context previews (first 3):**

1. _payment records: The table contains core payment transaction fields such as PaymentID, OrderID, PaymentMethod, PaymentDate, Amount, PaymentStatus, and authorization details, which strongly indicate a …_

2. _Order line items: The table is clearly an order-detail structure: it links a single order to a product and captures quantity, total amount, discount amount, and line status. The schema supports line-i…_

3. _Group Hierarchy: The table is a self-referencing group/category structure with ParentGroupID and contains only generic group attributes, which aligns most closely with a hierarchical group concept rat…_

---

### ✅ 17 — What deprecated fields exist in tblProduct and why should they be avoided?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0052 | **Gate:** `proceed_with_warning`

**Expected answer:**
> The tblProduct table contains three deprecated fields: prod_num (superseded by strSKU), item_desc (superseded by strDescription), and unit_cost (wrong data type with VARCHAR instead of DECIMAL). These fields should not be used in new code as they represent outdated design decisions.

**System answer:**
> The provided context does not include any definition of tblProduct, any column list for that table, or any indication of deprecated fields. Because of that, I cannot determine which fields in tblProduct are deprecated or why they should be avoided from the knowledge provided here.

**Sources retrieved (5):** `payment records`, `Order line items`, `Group Hierarchy`, `CustomerMaster v3.2.1`, `Shipping carrier master data`

**Context previews (first 3):**

1. _payment records: The table contains core payment transaction fields such as PaymentID, OrderID, PaymentMethod, PaymentDate, Amount, PaymentStatus, and authorization details, which strongly indicate a …_

2. _Order line items: The table is clearly an order-detail structure: it links a single order to a product and captures quantity, total amount, discount amount, and line status. The schema supports line-i…_

3. _Group Hierarchy: The table is a self-referencing group/category structure with ParentGroupID and contains only generic group attributes, which aligns most closely with a hierarchical group concept rat…_

---

### ✅ 18 — How are shipping carriers configured in the system?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0136 | **Gate:** `proceed_with_warning`

**Expected answer:**
> Shipping carriers are stored in the tblShippingCarrier table with CarrierID, CarrierName, CarrierCode (for API integration), TrackingURL (with {TRACKING_NUM} placeholder), and bolActive flag. Only carriers with bolActive=1 should be offered during checkout.

**System answer:**
> The retrieved context only identifies a business concept named “Shipping carrier master data.” From that, the most that can be said is that shipping carriers are represented as master data in the system.

The context does not provide the actual configuration details, such as the table name, columns, attributes, relationships, setup process, or how carrier options are linked to orders or shipments.…

**Sources retrieved (5):** `Shipping carrier master data`, `Group Hierarchy`, `payment records`, `Order line items`, `CustomerMaster v3.2.1`

**Context previews (first 3):**

1. _Shipping carrier master data…_

2. _Group Hierarchy: The table is a self-referencing group/category structure with ParentGroupID and contains only generic group attributes, which aligns most closely with a hierarchical group concept rat…_

3. _payment records: The table contains core payment transaction fields such as PaymentID, OrderID, PaymentMethod, PaymentDate, Amount, PaymentStatus, and authorization details, which strongly indicate a …_

---

### ✅ 19 — What is the relationship between User table passwords and security?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0006 | **Gate:** `proceed_with_warning`

**Expected answer:**
> The User table stores password hashes in the PasswordHash field, but uses SHA-256 without salt, making it vulnerable to rainbow table attacks. This is identified as a security issue in the data dictionary. Additionally, the table name 'User' is a SQL reserved word requiring square bracket quoting.

**System answer:**
> The retrieved context does not provide information about a User table, password fields, password handling, or security rules for user authentication.

What is present in the context is unrelated schema/business metadata for payment records, group hierarchy, order line items, a customer master concept name, and shipping carrier master data. The only security-related detail mentioned is that the pay…

**Sources retrieved (5):** `payment records`, `Group Hierarchy`, `Order line items`, `CustomerMaster v3.2.1`, `Shipping carrier master data`

**Context previews (first 3):**

1. _payment records: The table contains core payment transaction fields such as PaymentID, OrderID, PaymentMethod, PaymentDate, Amount, PaymentStatus, and authorization details, which strongly indicate a …_

2. _Group Hierarchy: The table is a self-referencing group/category structure with ParentGroupID and contains only generic group attributes, which aligns most closely with a hierarchical group concept rat…_

3. _Order line items: The table is clearly an order-detail structure: it links a single order to a product and captures quantity, total amount, discount amount, and line status. The schema supports line-i…_

---

### ✅ 20 — What fields in vw_SalesOrderHdr use the 'flt' Hungarian notation prefix and what do they store?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0370 | **Gate:** `proceed_with_warning`

**Expected answer:**
> The vw_SalesOrderHdr table uses the 'flt' (float) prefix for three monetary fields: fltSubTotal (line item subtotal before tax), fltTaxAmount (calculated tax), and fltTotalAmount (final total including tax and shipping). Despite the 'flt' prefix suggesting floating-point, these are defined as DECIMA…

**System answer:**
> I cannot determine this from the retrieved context. The context does not include the definition of vw_SalesOrderHdr or any column list for that view, so it does not show which fields use the flt Hungarian notation prefix or what those fields store. The available context only contains high-level business concepts for payment records, order line items, group hierarchy, customer master, and shipping …

**Sources retrieved (5):** `payment records`, `Order line items`, `Group Hierarchy`, `CustomerMaster v3.2.1`, `Shipping carrier master data`

**Context previews (first 3):**

1. _payment records: The table contains core payment transaction fields such as PaymentID, OrderID, PaymentMethod, PaymentDate, Amount, PaymentStatus, and authorization details, which strongly indicate a …_

2. _Order line items: The table is clearly an order-detail structure: it links a single order to a product and captures quantity, total amount, discount amount, and line status. The schema supports line-i…_

3. _Group Hierarchy: The table is a self-referencing group/category structure with ParentGroupID and contains only generic group attributes, which aligns most closely with a hierarchical group concept rat…_

---

### ✅ 21 — How does the schema handle the different date/time field naming conventions?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0062 | **Gate:** `proceed_with_warning`

**Expected answer:**
> The schema uses 'dtm' (datetime) Hungarian notation prefix consistently: dtmCreated and dtmLastModified in tblCustomer, dtmOrderDate/dtmShipDate/dtmRequiredDate in vw_SalesOrderHdr, dtmIntroduced/dtmDiscontinued in tblProduct, and txn_dt in inv_txn_log (abbreviated exception). The User table breaks …

**System answer:**
> The retrieved context does not provide enough information to explain how the schema handles different date/time field naming conventions at a schema-wide level.

What is known from the context is very limited: in the payment records concept, one date field is explicitly named PaymentDate. The same concept also lists fields such as PaymentID, OrderID, PaymentMethod, Amount, PaymentStatus, and autho…

**Sources retrieved (5):** `payment records`, `Order line items`, `Group Hierarchy`, `CustomerMaster v3.2.1`, `Shipping carrier master data`

**Context previews (first 3):**

1. _payment records: The table contains core payment transaction fields such as PaymentID, OrderID, PaymentMethod, PaymentDate, Amount, PaymentStatus, and authorization details, which strongly indicate a …_

2. _Order line items: The table is clearly an order-detail structure: it links a single order to a product and captures quantity, total amount, discount amount, and line status. The schema supports line-i…_

3. _Group Hierarchy: The table is a self-referencing group/category structure with ParentGroupID and contains only generic group attributes, which aligns most closely with a hierarchical group concept rat…_

---

### ✅ 22 — What table prefix patterns exist in the schema and what do they indicate?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0422 | **Gate:** `proceed_with_warning`

**Expected answer:**
> The schema uses multiple inconsistent table prefixes: 'tbl' for standard tables (tblCustomer, tblProduct, tblPayment, tblShippingCarrier, tblOrderStatusHistory), 'vw_' for a misnamed table (vw_SalesOrderHdr), and domain-specific prefixes 'ord_' (ord_line_item) and 'inv_' (inv_txn_log). Two tables (G…

**System answer:**
> The retrieved context does not provide enough information to identify schema-wide table prefix patterns or what such prefixes indicate.

What is known from the context is limited to a few business concepts:
payment records, Order line items, Group Hierarchy, Shipping carrier master data, and CustomerMaster v3.2.1. For three of these, the context gives semantic descriptions of the table content: pa…

**Sources retrieved (5):** `payment records`, `Order line items`, `Group Hierarchy`, `Shipping carrier master data`, `CustomerMaster v3.2.1`

**Context previews (first 3):**

1. _payment records: The table contains core payment transaction fields such as PaymentID, OrderID, PaymentMethod, PaymentDate, Amount, PaymentStatus, and authorization details, which strongly indicate a …_

2. _Order line items: The table is clearly an order-detail structure: it links a single order to a product and captures quantity, total amount, discount amount, and line status. The schema supports line-i…_

3. _Group Hierarchy: The table is a self-referencing group/category structure with ParentGroupID and contains only generic group attributes, which aligns most closely with a hierarchical group concept rat…_

---

### ✅ 23 — What foreign key relationships exist for the vw_SalesOrderHdr table?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0011 | **Gate:** `proceed_with_warning`

**Expected answer:**
> The vw_SalesOrderHdr table has one explicit foreign key constraint: intCustID references tblCustomer.strCustID. Implicit relationships (not enforced by FK constraints) include tblPayment.OrderID, tblOrderStatusHistory.OrderID, and ord_line_item.ord_id all referencing vw_SalesOrderHdr.lngOrderID.

**System answer:**
> I cannot determine the foreign key relationships for `vw_SalesOrderHdr` from the provided context.

The retrieved context does not mention `vw_SalesOrderHdr` or list any foreign key definitions for it. The closest related facts are that the payment records table “references an order header” and that the Order line items table “links a single order to a product,” which suggests other tables relate …

**Sources retrieved (5):** `payment records`, `Order line items`, `Group Hierarchy`, `Shipping carrier master data`, `CustomerMaster v3.2.1`

**Context previews (first 3):**

1. _payment records: The table contains core payment transaction fields such as PaymentID, OrderID, PaymentMethod, PaymentDate, Amount, PaymentStatus, and authorization details, which strongly indicate a …_

2. _Order line items: The table is clearly an order-detail structure: it links a single order to a product and captures quantity, total amount, discount amount, and line status. The schema supports line-i…_

3. _Group Hierarchy: The table is a self-referencing group/category structure with ParentGroupID and contains only generic group attributes, which aligns most closely with a hierarchical group concept rat…_

---

### ✅ 24 — How does the legacy system handle product SKU format and uniqueness?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0003 | **Gate:** `proceed_with_warning`

**Expected answer:**
> Product SKUs are stored in the strSKU field with a UNIQUE constraint. The format follows Category-Color-Size pattern (e.g., 'SHIRT-BLU-L'). The deprecated prod_num field also exists but should not be used. SKUs are used in foreign key references from ord_line_item through the denormalized product_co…

**System answer:**
> I cannot determine how the legacy system handles product SKU format or uniqueness from the retrieved context.

What is known from the context is limited to high-level business concepts: there is an Order line items concept that links an order to a product and stores quantity, total amount, discount amount, and line status; a Group Hierarchy concept with a self-referencing ParentGroupID; a payment …

**Sources retrieved (5):** `payment records`, `Order line items`, `Group Hierarchy`, `Shipping carrier master data`, `CustomerMaster v3.2.1`

**Context previews (first 3):**

1. _payment records: The table contains core payment transaction fields such as PaymentID, OrderID, PaymentMethod, PaymentDate, Amount, PaymentStatus, and authorization details, which strongly indicate a …_

2. _Order line items: The table is clearly an order-detail structure: it links a single order to a product and captures quantity, total amount, discount amount, and line status. The schema supports line-i…_

3. _Group Hierarchy: The table is a self-referencing group/category structure with ParentGroupID and contains only generic group attributes, which aligns most closely with a hierarchical group concept rat…_

---

### ✅ 25 — What are the critical data quality issues identified for migration?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0000 | **Gate:** `proceed_with_warning`

**Expected answer:**
> Critical issues include: (1) PCI compliance violation - unencrypted card numbers in tblPayment.CardNumberText, (2) inappropriate data types - unit_cost as VARCHAR instead of DECIMAL, (3) missing foreign key constraints - inv_txn_log.user_id has no FK to User table, (4) security vulnerability - User.…

**System answer:**
> I cannot determine the critical data quality issues identified for migration from the retrieved context.

What the context does provide is only high-level schema/business concept information: a payment records table, Shipping carrier master data, Order line items, Group Hierarchy, and CustomerMaster v3.2.1. It describes some structural characteristics, such as payment fields, order-detail semantic…

**Sources retrieved (5):** `payment records`, `Shipping carrier master data`, `Order line items`, `Group Hierarchy`, `CustomerMaster v3.2.1`

**Context previews (first 3):**

1. _payment records: The table contains core payment transaction fields such as PaymentID, OrderID, PaymentMethod, PaymentDate, Amount, PaymentStatus, and authorization details, which strongly indicate a …_

2. _Shipping carrier master data…_

3. _Order line items: The table is clearly an order-detail structure: it links a single order to a product and captures quantity, total amount, discount amount, and line status. The schema supports line-i…_

---

## Anomalies & Observations

No anomalies detected. All questions grounded with acceptable RAGAS scores.
