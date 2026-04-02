# AB-12 — 01_basics_ecommerce — Run Analysis

**Timestamp:** 2026-04-01 01:44:30  
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
| ER similarity threshold | `0.85` |

## Builder Results

| Metric | Value |
|--------|-------|
| Triplets extracted | 280 |
| Entities resolved | 171 |
| Tables parsed | 7 |
| Tables completed | 7 |

## Query Evaluation Summary

| Metric | Value |
|--------|-------|
| Questions | 15 |
| Grounded | **15/15 (100%)** |
| Avg GT Coverage | 98% |
| Avg Top Score | 0.4445 |
| Avg Chunk Count | 12.0 |
| Abstained | 0 |

## RAGAS Metrics

RAGAS evaluation not enabled for this run.

## Per-Question Deep Dive

### ✅ Q001 — What information is stored for each customer?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.3478 | **Gate:** `proceed`

**Expected answer:**
> Each customer has a unique ID, full name, email address, geographic region code, creation date, and active status. The email must be unique across all customers.

**System answer:**
> For each customer, the physical table CUSTOMER_MASTER stores these fields: CUST_ID, FULL_NAME, EMAIL, REGION_CODE, CREATED_AT, and IS_ACTIVE. The data dictionary describes this as the master record for all registered platform customers, where CUST_ID is the unique customer identifier, FULL_NAME is the customer’s full name, EMAIL is the unique email address used for login, REGION_CODE is the geogra…

**Sources retrieved (12):** `Sales Order Header→SALES_ORDER_HDR`, `parent_chunk_data_dictionary.txt_3`, `Master record for all registered platform customers→CUSTOMER_MASTER`, `parent_chunk_business_glossary.txt_0`, `parent_chunk_business_glossary.txt_1`, `SALES_ORDER_HDR→CUSTOMER_MASTER`, `parent_chunk_business_glossary.txt_2`, `parent_chunk_data_dictionary.txt_4`

**Context previews (first 3):**

1. _Business concept 'Sales Order Header' — The table name and columns indicate a header-level order record: order id, customer id, order date, total amount, status, payment confirmation, and delivery tim…_

2. _# Data Dictionary - E-Commerce Database (Simplified)  This document describes the physical database schema for the simplified e-commerce test dataset.  ────────────────────────────────────────────────…_

3. _Business concept 'Master record for all registered platform customers' is implemented by physical table CUSTOMER_MASTER (columns: CUST_ID, FULL_NAME, EMAIL, REGION_CODE, CREATED_AT, IS_ACTIVE).…_

---

### ✅ Q002 — How are products categorized on the platform?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.1590 | **Gate:** `proceed_with_warning`

**Expected answer:**
> Products belong to categories which can have a parent category, forming a hierarchical tree structure. Each product references exactly one category through its CATEGORY_ID.

**System answer:**
> Products are categorized through the `TB_PRODUCT` and `TB_CATEGORY` tables. The business concept `Product` is implemented by `TB_PRODUCT`, which includes the column `CATEGORY_ID`. That column is a foreign key to `TB_CATEGORY.CATEGORY_ID`, so each product is assigned to a category record in `TB_CATEGORY`.

The category structure itself is hierarchical. `TB_CATEGORY` contains `CATEGORY_ID`, `CATEGOR…

**Sources retrieved (12):** `parent_chunk_business_glossary.txt_0`, `parent_chunk_data_dictionary.txt_3`, `parent_chunk_business_glossary.txt_1`, `Category→TB_CATEGORY`, `Master record for all registered platform customers→CUSTOMER_MASTER`, `parent_chunk_data_dictionary.txt_4`, `parent_chunk_data_dictionary.txt_5`, `Product→TB_PRODUCT`

**Context previews (first 3):**

1. _# Business Glossary - E-Commerce Domain (Simplified)  This document defines the core business concepts for the e-commerce platform test dataset.  ──────────────────────────────────────────────────────…_

2. _# Data Dictionary - E-Commerce Database (Simplified)  This document describes the physical database schema for the simplified e-commerce test dataset.  ────────────────────────────────────────────────…_

3. _**Business Context**: Line items break down orders into individual product purchases. Each captures the price at the moment of ordering. **Key Attributes**: - Unique line identifier - References exact…_

---

### ✅ Q003 — What is the relationship between customers and sales orders?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.9847 | **Gate:** `proceed`

**Expected answer:**
> Each sales order is placed by exactly one customer, referenced through the CUST_ID foreign key. A customer can place zero or more orders over time.

**System answer:**
> A customer places sales orders, and each Sales Order is placed by exactly one Customer.

In the physical schema, this is implemented by SALES_ORDER_HDR.CUST_ID referencing CUSTOMER_MASTER.CUST_ID. That means each sales order header record in SALES_ORDER_HDR is linked to one customer record in CUSTOMER_MASTER.

The business glossary also connects these concepts directly: Customer is related to Sale…

**Sources retrieved (12):** `parent_chunk_business_glossary.txt_2`, `parent_chunk_business_glossary.txt_0`, `parent_chunk_business_glossary.txt_1`, `Sales Order Header→SALES_ORDER_HDR`, `parent_chunk_data_dictionary.txt_4`, `SALES_ORDER_HDR→CUSTOMER_MASTER`, `parent_chunk_data_dictionary.txt_3`, `PAYMENT→SALES_ORDER_HDR`

**Context previews (first 3):**

1. _Sales Order Relationships: - A Sales Order is placed by exactly one Customer - A Sales Order has one or more Order Line Items - A Sales Order has one or more Payments - A Sales Order has one or more S…_

2. _# Business Glossary - E-Commerce Domain (Simplified)  This document defines the core business concepts for the e-commerce platform test dataset.  ──────────────────────────────────────────────────────…_

3. _**Business Context**: Line items break down orders into individual product purchases. Each captures the price at the moment of ordering. **Key Attributes**: - Unique line identifier - References exact…_

---

### ✅ Q004 — What does an order line item contain?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.9580 | **Gate:** `proceed`

**Expected answer:**
> An order line item specifies a product, the quantity ordered, the unit price at time of purchase, and the calculated extended amount. Each line item belongs to exactly one sales order.

**System answer:**
> An order line item contains the details of an individual product purchase within a sales order. In the business concept and the `ORDER_LINE_ITEM` table, it includes a unique line identifier (`LINE_ID`), the parent order (`ORDER_ID`), the product ordered (`PRODUCT_ID`), the quantity (`QUANTITY`), the unit price at the time of the order (`UNIT_PRICE`), and the extended line amount (`LINE_AMT`), whic…

**Sources retrieved (12):** `Must contain at least one Order Line Item→ORDER_LINE_ITEM`, `parent_chunk_business_glossary.txt_1`, `ORDER_LINE_ITEM→TB_PRODUCT`, `ORDER_LINE_ITEM→SALES_ORDER_HDR`, `parent_chunk_business_glossary.txt_2`, `parent_chunk_data_dictionary.txt_4`, `Sales Order Header→SALES_ORDER_HDR`, `parent_chunk_business_glossary.txt_0`

**Context previews (first 3):**

1. _Business concept 'Must contain at least one Order Line Item' is implemented by physical table ORDER_LINE_ITEM (columns: LINE_ID, ORDER_ID, PRODUCT_ID, QUANTITY, UNIT_PRICE, LINE_AMT).…_

2. _**Business Context**: Line items break down orders into individual product purchases. Each captures the price at the moment of ordering. **Key Attributes**: - Unique line identifier - References exact…_

3. _Relationship: ORDER_LINE_ITEM references TB_PRODUCT via foreign key PRODUCT_ID -> TB_PRODUCT.PRODUCT_ID.…_

---

### ✅ Q005 — How are payments linked to orders?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.9232 | **Gate:** `proceed`

**Expected answer:**
> Each payment is associated with exactly one sales order through the ORDER_ID foreign key. Payments track the payment method, amount, status, and confirmation timestamp.

**System answer:**
> Payments are linked to orders through the `PAYMENT.ORDER_ID` foreign key, which references `SALES_ORDER_HDR.ORDER_ID`.

From the context, this means:
A `PAYMENT` record is for exactly one Sales Order, and a `Sales Order` has one or more Payments. So the relationship is one-to-many from `SALES_ORDER_HDR` to `PAYMENT`.

At the schema level, you would join payments to orders as:
`PAYMENT.ORDER_ID = S…

**Sources retrieved (12):** `PAYMENT→SALES_ORDER_HDR`, `parent_chunk_business_glossary.txt_1`, `parent_chunk_business_glossary.txt_2`, `parent_chunk_data_dictionary.txt_4`, `SHIPMENT→SALES_ORDER_HDR`, `ORDER_LINE_ITEM→SALES_ORDER_HDR`, `SALES_ORDER_HDR→CUSTOMER_MASTER`, `parent_chunk_business_glossary.txt_0`

**Context previews (first 3):**

1. _Relationship: PAYMENT references SALES_ORDER_HDR via foreign key ORDER_ID -> SALES_ORDER_HDR.ORDER_ID.…_

2. _**Business Context**: Line items break down orders into individual product purchases. Each captures the price at the moment of ordering. **Key Attributes**: - Unique line identifier - References exact…_

3. _Sales Order Relationships: - A Sales Order is placed by exactly one Customer - A Sales Order has one or more Order Line Items - A Sales Order has one or more Payments - A Sales Order has one or more S…_

---

### ✅ Q006 — What statuses can an order have?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.2273 | **Gate:** `proceed`

**Expected answer:**
> Orders can have one of five statuses defined via CHECK constraint on SALES_ORDER_HDR.STATUS_CODE: PENDING (initial state when order is created), CONFIRMED (payment has been received), SHIPPED (dispatched to customer), DELIVERED (received by customer), or CANCELLED. The business glossary describes th…

**System answer:**
> The retrieved context shows that an order has a status field, STATUS_CODE, on SALES_ORDER_HDR, which implements the Sales Order Header concept. However, it does not provide the allowed order status values or enumerate what statuses an order can have.

Related schema facts from the context are:
SALES_ORDER_HDR contains ORDER_ID, CUST_ID, ORDER_DATE, TOTAL_AMT, STATUS_CODE, PAYMENT_CONFIRMED_AT, DEL…

**Sources retrieved (12):** `Sales Order Header→SALES_ORDER_HDR`, `parent_chunk_business_glossary.txt_0`, `parent_chunk_business_glossary.txt_1`, `Shipment→SHIPMENT`, `parent_chunk_business_glossary.txt_2`, `PAYMENT_CONFIRMED_AT→PAYMENT`, `parent_chunk_data_dictionary.txt_4`, `parent_chunk_data_dictionary.txt_3`

**Context previews (first 3):**

1. _Business concept 'Sales Order Header' — The table name and columns indicate a header-level order record: order id, customer id, order date, total amount, status, payment confirmation, and delivery tim…_

2. _# Business Glossary - E-Commerce Domain (Simplified)  This document defines the core business concepts for the e-commerce platform test dataset.  ──────────────────────────────────────────────────────…_

3. _**Business Context**: Line items break down orders into individual product purchases. Each captures the price at the moment of ordering. **Key Attributes**: - Unique line identifier - References exact…_

---

### ✅ Q007 — Which table stores the product SKU information?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.7968 | **Gate:** `proceed`

**Expected answer:**
> The TB_PRODUCT table stores the SKU (Stock Keeping Unit) code for each product, along with product name, category, price, and active status.

**System answer:**
> The product SKU is stored in TB_PRODUCT, in the SKU column. The context maps the business concept Product to physical table TB_PRODUCT with columns PRODUCT_ID, SKU, PRODUCT_NAME, CATEGORY_ID, UNIT_PRICE, and IS_ACTIVE.

**Sources retrieved (12):** `Product→TB_PRODUCT`, `Must contain at least one Order Line Item→ORDER_LINE_ITEM`, `parent_chunk_data_dictionary.txt_3`, `ORDER_LINE_ITEM→TB_PRODUCT`, `Sales Order Header→SALES_ORDER_HDR`, `parent_chunk_business_glossary.txt_0`, `TB_PRODUCT→TB_CATEGORY`, `Sales Order Header`

**Context previews (first 3):**

1. _Business concept 'Product' is implemented by physical table TB_PRODUCT (columns: PRODUCT_ID, SKU, PRODUCT_NAME, CATEGORY_ID, UNIT_PRICE, IS_ACTIVE).…_

2. _Business concept 'Must contain at least one Order Line Item' is implemented by physical table ORDER_LINE_ITEM (columns: LINE_ID, ORDER_ID, PRODUCT_ID, QUANTITY, UNIT_PRICE, LINE_AMT).…_

3. _# Data Dictionary - E-Commerce Database (Simplified)  This document describes the physical database schema for the simplified e-commerce test dataset.  ────────────────────────────────────────────────…_

---

### ✅ Q008 — How can I find all orders placed by a specific customer?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.1428 | **Gate:** `proceed_with_warning`

**Expected answer:**
> Query the SALES_ORDER_HDR table filtering by CUST_ID. Each order has a foreign key reference to CUSTOMER_MASTER.CUST_ID, so joining these tables on CUST_ID will show all orders for a customer along with their details.

**System answer:**
> Use the customer-to-order relationship between CUSTOMER_MASTER and SALES_ORDER_HDR.

At the schema level, all orders for a customer are stored in SALES_ORDER_HDR, and that table references the customer through the foreign key SALES_ORDER_HDR.CUST_ID → CUSTOMER_MASTER.CUST_ID. A Sales Order is placed by exactly one Customer.

So the lookup path is:

CUSTOMER_MASTER.CUST_ID = SALES_ORDER_HDR.CUST_ID…

**Sources retrieved (12):** `parent_chunk_data_dictionary.txt_3`, `parent_chunk_business_glossary.txt_2`, `Sales Order Header→SALES_ORDER_HDR`, `parent_chunk_business_glossary.txt_0`, `parent_chunk_data_dictionary.txt_4`, `SALES_ORDER_HDR→CUSTOMER_MASTER`, `parent_chunk_business_glossary.txt_1`, `Master record for all registered platform customers→CUSTOMER_MASTER`

**Context previews (first 3):**

1. _# Data Dictionary - E-Commerce Database (Simplified)  This document describes the physical database schema for the simplified e-commerce test dataset.  ────────────────────────────────────────────────…_

2. _Sales Order Relationships: - A Sales Order is placed by exactly one Customer - A Sales Order has one or more Order Line Items - A Sales Order has one or more Payments - A Sales Order has one or more S…_

3. _Business concept 'Sales Order Header' — The table name and columns indicate a header-level order record: order id, customer id, order date, total amount, status, payment confirmation, and delivery tim…_

---

### ✅ Q009 — What products were included in a specific order?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0782 | **Gate:** `proceed_with_warning`

**Expected answer:**
> Join ORDER_LINE_ITEM with TB_PRODUCT on PRODUCT_ID. For order ORDER_ID, the line items show which products were ordered, in what quantity, and at what price.

**System answer:**
> The retrieved context does not contain order-level data, so it cannot tell which products were included in any specific order.

What is known from the context is the schema needed to answer that question. A specific order’s products would be found through ORDER_LINE_ITEM, which stores the line records for each sales order with LINE_ID, ORDER_ID, PRODUCT_ID, QUANTITY, UNIT_PRICE, and LINE_AMT. ORDE…

**Sources retrieved (12):** `parent_chunk_data_dictionary.txt_4`, `parent_chunk_business_glossary.txt_1`, `ORDER_LINE_ITEM→TB_PRODUCT`, `Must contain at least one Order Line Item→ORDER_LINE_ITEM`, `parent_chunk_business_glossary.txt_0`, `parent_chunk_data_dictionary.txt_3`, `Sales Order Header→SALES_ORDER_HDR`, `parent_chunk_business_glossary.txt_2`

**Context previews (first 3):**

1. _**Foreign Keys**: - CUST_ID → CUSTOMER_MASTER(CUST_ID) **Business Concept Mapping**: SalesOrder ──────────────────────────────────────────────────────────── ORDER_LINE_ITEM ───────────────────────────…_

2. _**Business Context**: Line items break down orders into individual product purchases. Each captures the price at the moment of ordering. **Key Attributes**: - Unique line identifier - References exact…_

3. _Relationship: ORDER_LINE_ITEM references TB_PRODUCT via foreign key PRODUCT_ID -> TB_PRODUCT.PRODUCT_ID.…_

---

### ✅ Q010 — Show me the order hierarchy from customer to line items.

**Status:** GROUNDED  
**GT Coverage:** 75% | **Top Score:** 0.7370 | **Gate:** `proceed`

**Expected answer:**
> The hierarchy is: Customer (CUSTOMER_MASTER) → SalesOrder (SALES_ORDER_HDR) → OrderLineItem (ORDER_LINE_ITEM) → Product (TB_PRODUCT). Each customer has orders, each order has line items, and each line item references a product.

**System answer:**
> The order hierarchy in the schema is:

Customer → Sales Order Header → Order Line Item

Using the physical tables, the path is:

CUSTOMER_MASTER.CUST_ID = SALES_ORDER_HDR.CUST_ID  
SALES_ORDER_HDR.ORDER_ID = ORDER_LINE_ITEM.ORDER_ID

So to trace from a customer to the line items on their orders, you join CUSTOMER_MASTER to SALES_ORDER_HDR on CUST_ID, then join SALES_ORDER_HDR to ORDER_LINE_ITEM on…

**Sources retrieved (12):** `parent_chunk_business_glossary.txt_2`, `parent_chunk_data_dictionary.txt_4`, `parent_chunk_business_glossary.txt_1`, `Must contain at least one Order Line Item→ORDER_LINE_ITEM`, `ORDER_LINE_ITEM→TB_PRODUCT`, `ORDER_LINE_ITEM→SALES_ORDER_HDR`, `parent_chunk_business_glossary.txt_0`, `parent_chunk_data_dictionary.txt_3`

**Context previews (first 3):**

1. _Sales Order Relationships: - A Sales Order is placed by exactly one Customer - A Sales Order has one or more Order Line Items - A Sales Order has one or more Payments - A Sales Order has one or more S…_

2. _**Foreign Keys**: - CUST_ID → CUSTOMER_MASTER(CUST_ID) **Business Concept Mapping**: SalesOrder ──────────────────────────────────────────────────────────── ORDER_LINE_ITEM ───────────────────────────…_

3. _**Business Context**: Line items break down orders into individual product purchases. Each captures the price at the moment of ordering. **Key Attributes**: - Unique line identifier - References exact…_

---

### ✅ Q011 — What happens when a payment is confirmed for an order?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.3521 | **Gate:** `proceed`

**Expected answer:**
> When payment is confirmed, the PAYMENT record's STATUS_CODE becomes 'CONFIRMED', the CONFIRMED_AT timestamp is set, and the associated SALES_ORDER_HDR can progress from PENDING to CONFIRMED status.

**System answer:**
> When a payment is confirmed for an order, the confirmation is represented in the schema by a timestamp.

The business concept PAYMENT_CONFIRMED_AT is implemented by the PAYMENT table, specifically PAYMENT.CONFIRMED_AT. The PAYMENT table stores PAYMENT_ID, ORDER_ID, PAYMENT_METHOD, AMOUNT, STATUS_CODE, CONFIRMED_AT, and CREATED_AT, and each payment belongs to exactly one sales order through PAYMENT…

**Sources retrieved (12):** `parent_chunk_business_glossary.txt_1`, `PAYMENT_CONFIRMED_AT→PAYMENT`, `Sales Order Header→SALES_ORDER_HDR`, `PAYMENT→SALES_ORDER_HDR`, `parent_chunk_data_dictionary.txt_4`, `parent_chunk_business_glossary.txt_0`, `parent_chunk_business_glossary.txt_2`, `parent_chunk_data_dictionary.txt_3`

**Context previews (first 3):**

1. _**Business Context**: Line items break down orders into individual product purchases. Each captures the price at the moment of ordering. **Key Attributes**: - Unique line identifier - References exact…_

2. _Business concept 'PAYMENT_CONFIRMED_AT' is implemented by physical table PAYMENT (columns: PAYMENT_ID, ORDER_ID, PAYMENT_METHOD, AMOUNT, STATUS_CODE, CONFIRMED_AT, CREATED_AT).…_

3. _Business concept 'Sales Order Header' — The table name and columns indicate a header-level order record: order id, customer id, order date, total amount, status, payment confirmation, and delivery tim…_

---

### ✅ Q012 — How are shipments related to orders and warehouses?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.4940 | **Gate:** `proceed`

**Expected answer:**
> Each shipment is for exactly one sales order (ORDER_ID in SHIPMENT references SALES_ORDER_HDR). The shipment also specifies the source warehouse code and includes tracking information and delivery status.

**System answer:**
> Shipments are tied to orders at both the business and schema levels. In the business relationships, a Sales Order has one or more Shipments, and each Shipment is for exactly one Sales Order. In the physical schema, the business concept Shipment is implemented by the SHIPMENT table, which includes ORDER_ID and WAREHOUSE_CODE, and SHIPMENT.ORDER_ID references SALES_ORDER_HDR.ORDER_ID.

For warehouse…

**Sources retrieved (12):** `Shipment→SHIPMENT`, `parent_chunk_business_glossary.txt_2`, `parent_chunk_business_glossary.txt_0`, `parent_chunk_business_glossary.txt_1`, `parent_chunk_data_dictionary.txt_4`, `Sales Order Header→SALES_ORDER_HDR`, `parent_chunk_data_dictionary.txt_3`, `parent_chunk_data_dictionary.txt_5`

**Context previews (first 3):**

1. _Business concept 'Shipment' is implemented by physical table SHIPMENT (columns: SHIPMENT_ID, ORDER_ID, WAREHOUSE_CODE, SHIPPED_AT, TRACKING_NUMBER, STATUS_CODE).…_

2. _Sales Order Relationships: - A Sales Order is placed by exactly one Customer - A Sales Order has one or more Order Line Items - A Sales Order has one or more Payments - A Sales Order has one or more S…_

3. _# Business Glossary - E-Commerce Domain (Simplified)  This document defines the core business concepts for the e-commerce platform test dataset.  ──────────────────────────────────────────────────────…_

---

### ✅ Q013 — Can a product belong to multiple categories?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.3613 | **Gate:** `proceed`

**Expected answer:**
> No, each product belongs to exactly one category. The TB_PRODUCT table has a CATEGORY_ID foreign key referencing TB_CATEGORY, which stores a single category value per product.

**System answer:**
> From the retrieved context, I can only say that TB_PRODUCT has a CATEGORY_ID column, and TB_PRODUCT references TB_CATEGORY via CATEGORY_ID -> TB_CATEGORY.CATEGORY_ID. So the schema shown includes a single category reference on each TB_PRODUCT record.

However, the context does not explicitly state whether products are restricted to one category overall, or whether another mechanism could allow mul…

**Sources retrieved (12):** `parent_chunk_business_glossary.txt_0`, `TB_PRODUCT→TB_CATEGORY`, `Product→TB_PRODUCT`, `parent_chunk_business_glossary.txt_1`, `parent_chunk_data_dictionary.txt_3`, `parent_chunk_data_dictionary.txt_4`, `Sales Order Header→SALES_ORDER_HDR`, `ORDER_LINE_ITEM→TB_PRODUCT`

**Context previews (first 3):**

1. _# Business Glossary - E-Commerce Domain (Simplified)  This document defines the core business concepts for the e-commerce platform test dataset.  ──────────────────────────────────────────────────────…_

2. _Relationship: TB_PRODUCT references TB_CATEGORY via foreign key CATEGORY_ID -> TB_CATEGORY.CATEGORY_ID.…_

3. _Business concept 'Product' is implemented by physical table TB_PRODUCT (columns: PRODUCT_ID, SKU, PRODUCT_NAME, CATEGORY_ID, UNIT_PRICE, IS_ACTIVE).…_

---

### ✅ Q014 — Is it possible for a customer to place an order without payment?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0719 | **Gate:** `proceed_with_warning`

**Expected answer:**
> Yes, an order can exist without payment. SALES_ORDER_HDR has STATUS_CODE defaulting to PENDING and PAYMENT_CONFIRMED_AT is nullable (NULL when no payment yet). The PAYMENT table links via ORDER_ID foreign key but nothing prevents an order from existing without a payment row. However, the business gl…

**System answer:**
> No. In the business relationships provided, a Sales Order is placed by exactly one Customer and has one or more Payments. The schema supports this through CUSTOMER_MASTER.CUST_ID → SALES_ORDER_HDR.CUST_ID and PAYMENT.ORDER_ID → SALES_ORDER_HDR.ORDER_ID. So, in this model, an order cannot exist without at least one associated payment.

The context also shows payment confirmation is tracked at both …

**Sources retrieved (12):** `parent_chunk_data_dictionary.txt_3`, `parent_chunk_business_glossary.txt_1`, `parent_chunk_business_glossary.txt_2`, `parent_chunk_business_glossary.txt_0`, `Sales Order Header→SALES_ORDER_HDR`, `parent_chunk_data_dictionary.txt_4`, `PAYMENT→SALES_ORDER_HDR`, `PAYMENT_CONFIRMED_AT→PAYMENT`

**Context previews (first 3):**

1. _# Data Dictionary - E-Commerce Database (Simplified)  This document describes the physical database schema for the simplified e-commerce test dataset.  ────────────────────────────────────────────────…_

2. _**Business Context**: Line items break down orders into individual product purchases. Each captures the price at the moment of ordering. **Key Attributes**: - Unique line identifier - References exact…_

3. _Sales Order Relationships: - A Sales Order is placed by exactly one Customer - A Sales Order has one or more Order Line Items - A Sales Order has one or more Payments - A Sales Order has one or more S…_

---

### ✅ Q015 — What is the total value of all orders placed by a customer?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0330 | **Gate:** `proceed_with_warning`

**Expected answer:**
> Sum the TOTAL_AMT column from SALES_ORDER_HDR for all records where CUST_ID matches the customer's ID. This aggregates the monetary value of all orders placed by that customer.

**System answer:**
> The retrieved context does not contain actual customer or order records, so I cannot give a numeric total for a specific customer.

At the schema level, the total value of all orders placed by a customer would be calculated from SALES_ORDER_HDR, which is the Sales Order Header table. SALES_ORDER_HDR is linked to CUSTOMER_MASTER by SALES_ORDER_HDR.CUST_ID → CUSTOMER_MASTER.CUST_ID, and it contains …

**Sources retrieved (12):** `parent_chunk_business_glossary.txt_1`, `Sales Order Header→SALES_ORDER_HDR`, `parent_chunk_business_glossary.txt_0`, `parent_chunk_data_dictionary.txt_3`, `parent_chunk_business_glossary.txt_2`, `parent_chunk_data_dictionary.txt_4`, `Master record for all registered platform customers→CUSTOMER_MASTER`, `SALES_ORDER_HDR→CUSTOMER_MASTER`

**Context previews (first 3):**

1. _**Business Context**: Line items break down orders into individual product purchases. Each captures the price at the moment of ordering. **Key Attributes**: - Unique line identifier - References exact…_

2. _Business concept 'Sales Order Header' — The table name and columns indicate a header-level order record: order id, customer id, order date, total amount, status, payment confirmation, and delivery tim…_

3. _# Business Glossary - E-Commerce Domain (Simplified)  This document defines the core business concepts for the e-commerce platform test dataset.  ──────────────────────────────────────────────────────…_

---

## Anomalies & Observations

No anomalies detected. All questions grounded with acceptable RAGAS scores.
