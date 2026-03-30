# AB-00 — 01_basics_ecommerce — Run Analysis

**Timestamp:** 2026-03-30 18:03:55  
**Run tag:** `post-fix-v5`

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
| Triplets extracted | 241 |
| Entities resolved | 78 |
| Tables parsed | 7 |
| Tables completed | 7 |

## Query Evaluation Summary

| Metric | Value |
|--------|-------|
| Questions | 15 |
| Grounded | **15/15 (100%)** |
| Avg GT Coverage | 95% |
| Avg Top Score | 0.3776 |
| Avg Chunk Count | 12.0 |
| Abstained | 0 |

## RAGAS Metrics

RAGAS evaluation not enabled for this run.

## Per-Question Deep Dive

### ✅ Q001 — What information is stored for each customer?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.1461 | **Gate:** `proceed_with_warning`

**Expected answer:**
> Each customer has a unique ID, full name, email address, geographic region code, creation date, and active status. The email must be unique across all customers.

**System answer:**
> For each customer, the physical customer master record is stored in CUSTOMER_MASTER, which implements the Customer business concept. The schema stores these fields for each customer: CUST_ID as the unique customer identifier, FULL_NAME as the customer’s full name, EMAIL as the unique email address used for login, REGION_CODE as the geographic region used for tax, CREATED_AT as the account creation…

**Sources retrieved (12):** `Sales Order Header→SALES_ORDER_HDR`, `Sales Order Header`, `parent_chunk_data_dictionary.txt_3`, `Master record for all registered platform customers→CUSTOMER_MASTER`, `parent_chunk_business_glossary.txt_0`, `Shipment→SHIPMENT`, `parent_chunk_business_glossary.txt_1`, `SALES_ORDER_HDR→CUSTOMER_MASTER`

**Context previews (first 3):**

1. _Business concept 'Sales Order Header' — The table name, primary key, customer foreign key, order date, status, and fulfillment/payment timestamps all align with a header-level sales order record. The …_

2. _Sales Order Header: The table name, primary key, customer foreign key, order date, status, and fulfillment/payment timestamps all align with a header-level sales order record. The closest business def…_

3. _# Data Dictionary - E-Commerce Database (Simplified)  This document describes the physical database schema for the simplified e-commerce test dataset.  ────────────────────────────────────────────────…_

---

### ✅ Q002 — How are products categorized on the platform?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.1590 | **Gate:** `proceed_with_warning`

**Expected answer:**
> Products belong to categories which can have a parent category, forming a hierarchical tree structure. Each product references exactly one category through its CATEGORY_ID.

**System answer:**
> Products are categorized through a category hierarchy in the database. Each product in TB_PRODUCT carries a CATEGORY_ID, and that column is a foreign key to TB_CATEGORY.CATEGORY_ID. This means every product is assigned to a category record in TB_CATEGORY.

The category structure is hierarchical: TB_CATEGORY has a self-reference through PARENT_CATEGORY_ID → TB_CATEGORY(CATEGORY_ID). So categories c…

**Sources retrieved (12):** `parent_chunk_business_glossary.txt_0`, `parent_chunk_data_dictionary.txt_3`, `parent_chunk_business_glossary.txt_1`, `Master record for all registered platform customers→CUSTOMER_MASTER`, `parent_chunk_data_dictionary.txt_4`, `PARENT_CATEGORY_ID → TB_CATEGORY(CATEGORY_ID) [self-reference]→TB_CATEGORY`, `parent_chunk_data_dictionary.txt_5`, `Hierarchical product category tree→TB_PRODUCT`

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
> The retrieved context supports this relationship: a Sales Order is placed by exactly one Customer.

At the schema level, this is implemented by SALES_ORDER_HDR.CUST_ID as a foreign key to CUSTOMER_MASTER.CUST_ID. The business concept mapping also aligns SALES_ORDER_HDR to SalesOrder and CUSTOMER_MASTER to Customer.

The context also links Customer and SalesOrder in the business glossary and descri…

**Sources retrieved (12):** `parent_chunk_business_glossary.txt_2`, `parent_chunk_business_glossary.txt_0`, `Sales Order Header`, `parent_chunk_business_glossary.txt_1`, `Sales Order Header→SALES_ORDER_HDR`, `parent_chunk_data_dictionary.txt_4`, `SALES_ORDER_HDR→CUSTOMER_MASTER`, `parent_chunk_data_dictionary.txt_3`

**Context previews (first 3):**

1. _Sales Order Relationships: - A Sales Order is placed by exactly one Customer - A Sales Order has one or more Order Line Items - A Sales Order has one or more Payments - A Sales Order has one or more S…_

2. _# Business Glossary - E-Commerce Domain (Simplified)  This document defines the core business concepts for the e-commerce platform test dataset.  ──────────────────────────────────────────────────────…_

3. _Sales Order Header: The table name, primary key, customer foreign key, order date, status, and fulfillment/payment timestamps all align with a header-level sales order record. The closest business def…_

---

### ✅ Q004 — What does an order line item contain?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.8739 | **Gate:** `proceed`

**Expected answer:**
> An order line item specifies a product, the quantity ordered, the unit price at time of purchase, and the calculated extended amount. Each line item belongs to exactly one sales order.

**System answer:**
> An order line item, implemented by the ORDER_LINE_ITEM table, contains the details for one product purchase within a sales order. It includes a unique line identifier (LINE_ID), the parent order reference (ORDER_ID), the referenced product (PRODUCT_ID), the quantity ordered (QUANTITY), the unit price at the time of order (UNIT_PRICE), and the extended line amount (LINE_AMT), which is quantity × un…

**Sources retrieved (12):** `parent_chunk_business_glossary.txt_1`, `ORDER_LINE_ITEM→TB_PRODUCT`, `item→ORDER_LINE_ITEM`, `ORDER_LINE_ITEM→SALES_ORDER_HDR`, `parent_chunk_business_glossary.txt_2`, `parent_chunk_data_dictionary.txt_4`, `Shipment→SHIPMENT`, `Sales Order Header`

**Context previews (first 3):**

1. _**Business Context**: Line items break down orders into individual product purchases. Each captures the price at the moment of ordering. **Key Attributes**: - Unique line identifier - References exact…_

2. _Relationship: ORDER_LINE_ITEM references TB_PRODUCT via foreign key PRODUCT_ID -> TB_PRODUCT.PRODUCT_ID.…_

3. _Business concept 'item' is implemented by physical table ORDER_LINE_ITEM (columns: LINE_ID, ORDER_ID, PRODUCT_ID, QUANTITY, UNIT_PRICE, LINE_AMT).…_

---

### ✅ Q005 — How are payments linked to orders?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.9232 | **Gate:** `proceed`

**Expected answer:**
> Each payment is associated with exactly one sales order through the ORDER_ID foreign key. Payments track the payment method, amount, status, and confirmation timestamp.

**System answer:**
> Payments are linked to orders through the PAYMENT.ORDER_ID foreign key, which references SALES_ORDER_HDR.ORDER_ID.

From the business relationships in the context, a Payment is for exactly one Sales Order, and a Sales Order has one or more Payments. At the schema level, this means you join PAYMENT to SALES_ORDER_HDR on PAYMENT.ORDER_ID = SALES_ORDER_HDR.ORDER_ID.

The PAYMENT table implements the …

**Sources retrieved (12):** `PAYMENT→SALES_ORDER_HDR`, `parent_chunk_business_glossary.txt_1`, `parent_chunk_business_glossary.txt_2`, `parent_chunk_data_dictionary.txt_4`, `SHIPMENT→SALES_ORDER_HDR`, `ORDER_LINE_ITEM→SALES_ORDER_HDR`, `SALES_ORDER_HDR→CUSTOMER_MASTER`, `parent_chunk_business_glossary.txt_0`

**Context previews (first 3):**

1. _Relationship: PAYMENT references SALES_ORDER_HDR via foreign key ORDER_ID -> SALES_ORDER_HDR.ORDER_ID.…_

2. _**Business Context**: Line items break down orders into individual product purchases. Each captures the price at the moment of ordering. **Key Attributes**: - Unique line identifier - References exact…_

3. _Sales Order Relationships: - A Sales Order is placed by exactly one Customer - A Sales Order has one or more Order Line Items - A Sales Order has one or more Payments - A Sales Order has one or more S…_

---

### ✅ Q006 — What statuses can an order have?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.1839 | **Gate:** `proceed_with_warning`

**Expected answer:**
> Orders can have one of five statuses defined via CHECK constraint on SALES_ORDER_HDR.STATUS_CODE: PENDING (initial state when order is created), CONFIRMED (payment has been received), SHIPPED (dispatched to customer), DELIVERED (received by customer), or CANCELLED. The business glossary describes th…

**System answer:**
> The retrieved context shows that an order is represented by the business concept Sales Order Header, implemented by the table SALES_ORDER_HDR, and that it has a STATUS_CODE column. It also has related lifecycle timestamps such as PAYMENT_CONFIRMED_AT and DELIVERED_AT.

However, the context does not provide the actual allowed order status values or a status code enumeration, so I cannot state which…

**Sources retrieved (12):** `Sales Order Header`, `parent_chunk_business_glossary.txt_0`, `Sales Order Header→SALES_ORDER_HDR`, `parent_chunk_business_glossary.txt_1`, `Shipment→SHIPMENT`, `Monetary transaction that settles the total amount due for a Sales Order→PAYMENT`, `parent_chunk_business_glossary.txt_2`, `parent_chunk_data_dictionary.txt_4`

**Context previews (first 3):**

1. _Sales Order Header: The table name, primary key, customer foreign key, order date, status, and fulfillment/payment timestamps all align with a header-level sales order record. The closest business def…_

2. _# Business Glossary - E-Commerce Domain (Simplified)  This document defines the core business concepts for the e-commerce platform test dataset.  ──────────────────────────────────────────────────────…_

3. _Business concept 'Sales Order Header' — The table name, primary key, customer foreign key, order date, status, and fulfillment/payment timestamps all align with a header-level sales order record. The …_

---

### ✅ Q007 — Which table stores the product SKU information?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.5995 | **Gate:** `proceed`

**Expected answer:**
> The TB_PRODUCT table stores the SKU (Stock Keeping Unit) code for each product, along with product name, category, price, and active status.

**System answer:**
> The product SKU is stored in TB_PRODUCT, in the SKU column. The retrieved context explicitly maps the product-related concept to TB_PRODUCT with columns PRODUCT_ID, SKU, PRODUCT_NAME, CATEGORY_ID, UNIT_PRICE, and IS_ACTIVE.

**Sources retrieved (12):** `Hierarchical product category tree→TB_PRODUCT`, `item→ORDER_LINE_ITEM`, `parent_chunk_data_dictionary.txt_3`, `ORDER_LINE_ITEM→TB_PRODUCT`, `parent_chunk_business_glossary.txt_0`, `TB_PRODUCT→TB_CATEGORY`, `parent_chunk_data_dictionary.txt_5`, `Master record for all registered platform customers→CUSTOMER_MASTER`

**Context previews (first 3):**

1. _Business concept 'Hierarchical product category tree' is implemented by physical table TB_PRODUCT (columns: PRODUCT_ID, SKU, PRODUCT_NAME, CATEGORY_ID, UNIT_PRICE, IS_ACTIVE).…_

2. _Business concept 'item' is implemented by physical table ORDER_LINE_ITEM (columns: LINE_ID, ORDER_ID, PRODUCT_ID, QUANTITY, UNIT_PRICE, LINE_AMT).…_

3. _# Data Dictionary - E-Commerce Database (Simplified)  This document describes the physical database schema for the simplified e-commerce test dataset.  ────────────────────────────────────────────────…_

---

### ✅ Q008 — How can I find all orders placed by a specific customer?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.1428 | **Gate:** `proceed_with_warning`

**Expected answer:**
> Query the SALES_ORDER_HDR table filtering by CUST_ID. Each order has a foreign key reference to CUSTOMER_MASTER.CUST_ID, so joining these tables on CUST_ID will show all orders for a customer along with their details.

**System answer:**
> Use the sales order header table, because the business concept “Sales Order Header” is implemented by SALES_ORDER_HDR, and that table has the customer foreign key CUST_ID.

The join path is CUSTOMER_MASTER.CUST_ID = SALES_ORDER_HDR.CUST_ID. The context explicitly states that SALES_ORDER_HDR references CUSTOMER_MASTER via foreign key CUST_ID → CUSTOMER_MASTER(CUST_ID), and that a Sales Order is pla…

**Sources retrieved (12):** `parent_chunk_data_dictionary.txt_3`, `parent_chunk_business_glossary.txt_2`, `Sales Order Header`, `parent_chunk_business_glossary.txt_0`, `Sales Order Header→SALES_ORDER_HDR`, `parent_chunk_data_dictionary.txt_4`, `SALES_ORDER_HDR→CUSTOMER_MASTER`, `parent_chunk_business_glossary.txt_1`

**Context previews (first 3):**

1. _# Data Dictionary - E-Commerce Database (Simplified)  This document describes the physical database schema for the simplified e-commerce test dataset.  ────────────────────────────────────────────────…_

2. _Sales Order Relationships: - A Sales Order is placed by exactly one Customer - A Sales Order has one or more Order Line Items - A Sales Order has one or more Payments - A Sales Order has one or more S…_

3. _Sales Order Header: The table name, primary key, customer foreign key, order date, status, and fulfillment/payment timestamps all align with a header-level sales order record. The closest business def…_

---

### ✅ Q009 — What products were included in a specific order?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0782 | **Gate:** `proceed_with_warning`

**Expected answer:**
> Join ORDER_LINE_ITEM with TB_PRODUCT on PRODUCT_ID. For order ORDER_ID, the line items show which products were ordered, in what quantity, and at what price.

**System answer:**
> From the retrieved context, I can explain how to find the products in an order, but I cannot list the products for a particular order because no specific order rows are provided.

The schema path is SALES_ORDER_HDR.ORDER_ID → ORDER_LINE_ITEM.ORDER_ID → TB_PRODUCT.PRODUCT_ID. A sales order is represented by SALES_ORDER_HDR, and its included products are stored at the line level in ORDER_LINE_ITEM. …

**Sources retrieved (12):** `parent_chunk_data_dictionary.txt_4`, `parent_chunk_business_glossary.txt_1`, `ORDER_LINE_ITEM→TB_PRODUCT`, `parent_chunk_business_glossary.txt_0`, `parent_chunk_data_dictionary.txt_3`, `item→ORDER_LINE_ITEM`, `parent_chunk_business_glossary.txt_2`, `Sales Order Header`

**Context previews (first 3):**

1. _**Foreign Keys**: - CUST_ID → CUSTOMER_MASTER(CUST_ID) **Business Concept Mapping**: SalesOrder ──────────────────────────────────────────────────────────── ORDER_LINE_ITEM ───────────────────────────…_

2. _**Business Context**: Line items break down orders into individual product purchases. Each captures the price at the moment of ordering. **Key Attributes**: - Unique line identifier - References exact…_

3. _Relationship: ORDER_LINE_ITEM references TB_PRODUCT via foreign key PRODUCT_ID -> TB_PRODUCT.PRODUCT_ID.…_

---

### ✅ Q010 — Show me the order hierarchy from customer to line items.

**Status:** GROUNDED  
**GT Coverage:** 75% | **Top Score:** 0.3719 | **Gate:** `proceed`

**Expected answer:**
> The hierarchy is: Customer (CUSTOMER_MASTER) → SalesOrder (SALES_ORDER_HDR) → OrderLineItem (ORDER_LINE_ITEM) → Product (TB_PRODUCT). Each customer has orders, each order has line items, and each line item references a product.

**System answer:**
> The order hierarchy from customer to line items is:

Customer → Sales Order → Order Line Item

In the physical schema, that is:

CUSTOMER_MASTER.CUST_ID → SALES_ORDER_HDR.CUST_ID → ORDER_LINE_ITEM.ORDER_ID

More specifically, the join path is:
CUSTOMER_MASTER.CUST_ID = SALES_ORDER_HDR.CUST_ID
and
SALES_ORDER_HDR.ORDER_ID = ORDER_LINE_ITEM.ORDER_ID

The business meaning across those tables is:
CUST…

**Sources retrieved (12):** `parent_chunk_business_glossary.txt_2`, `parent_chunk_data_dictionary.txt_4`, `parent_chunk_business_glossary.txt_1`, `item→ORDER_LINE_ITEM`, `ORDER_LINE_ITEM→TB_PRODUCT`, `ORDER_LINE_ITEM→SALES_ORDER_HDR`, `Sales Order Header`, `parent_chunk_business_glossary.txt_0`

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
> From the retrieved context, payment confirmation is recorded at both the payment level and the order-header level.

A payment is the “monetary transaction that settles the total amount due for a Sales Order,” implemented by the PAYMENT table. When a payment is confirmed, the payment record can store that event in PAYMENT.CONFIRMED_AT, and the same order-level event is also represented in SALES_ORD…

**Sources retrieved (12):** `parent_chunk_business_glossary.txt_1`, `Monetary transaction that settles the total amount due for a Sales Order→PAYMENT`, `Sales Order Header→SALES_ORDER_HDR`, `PAYMENT→SALES_ORDER_HDR`, `Sales Order Header`, `parent_chunk_data_dictionary.txt_4`, `parent_chunk_business_glossary.txt_0`, `parent_chunk_business_glossary.txt_2`

**Context previews (first 3):**

1. _**Business Context**: Line items break down orders into individual product purchases. Each captures the price at the moment of ordering. **Key Attributes**: - Unique line identifier - References exact…_

2. _Business concept 'Monetary transaction that settles the total amount due for a Sales Order' is implemented by physical table PAYMENT (columns: PAYMENT_ID, ORDER_ID, PAYMENT_METHOD, AMOUNT, STATUS_CODE…_

3. _Business concept 'Sales Order Header' — The table name, primary key, customer foreign key, order date, status, and fulfillment/payment timestamps all align with a header-level sales order record. The …_

---

### ✅ Q012 — How are shipments related to orders and warehouses?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.3848 | **Gate:** `proceed`

**Expected answer:**
> Each shipment is for exactly one sales order (ORDER_ID in SHIPMENT references SALES_ORDER_HDR). The shipment also specifies the source warehouse code and includes tracking information and delivery status.

**System answer:**
> Shipments are related to orders through the SHIPMENT table. A shipment is for exactly one Sales Order, and physically this is implemented by SHIPMENT.ORDER_ID referencing SALES_ORDER_HDR.ORDER_ID. The relationship is one-to-many from order to shipment: a Sales Order has one or more Shipments, while each Shipment belongs to exactly one order.

Shipments are related to warehouses as the origin of fu…

**Sources retrieved (12):** `parent_chunk_business_glossary.txt_2`, `Shipment→SHIPMENT`, `parent_chunk_business_glossary.txt_0`, `parent_chunk_business_glossary.txt_1`, `parent_chunk_data_dictionary.txt_4`, `Sales Order Header`, `Sales Order Header→SALES_ORDER_HDR`, `parent_chunk_data_dictionary.txt_3`

**Context previews (first 3):**

1. _Sales Order Relationships: - A Sales Order is placed by exactly one Customer - A Sales Order has one or more Order Line Items - A Sales Order has one or more Payments - A Sales Order has one or more S…_

2. _Business concept 'Shipment' — The table contains shipment-level logistics attributes such as ORDER_ID, WAREHOUSE_CODE, SHIPPED_AT, TRACKING_NUMBER, and STATUS_CODE, which align with a shipment record …_

3. _# Business Glossary - E-Commerce Domain (Simplified)  This document defines the core business concepts for the e-commerce platform test dataset.  ──────────────────────────────────────────────────────…_

---

### ✅ Q013 — Can a product belong to multiple categories?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.3613 | **Gate:** `proceed`

**Expected answer:**
> No, each product belongs to exactly one category. The TB_PRODUCT table has a CATEGORY_ID foreign key referencing TB_CATEGORY, which stores a single category value per product.

**System answer:**
> Based on the schema in the retrieved context, no: a product appears to belong to exactly one category.

The evidence is that `TB_PRODUCT` has a single column, `CATEGORY_ID`, and `TB_PRODUCT` references `TB_CATEGORY` through the foreign key `CATEGORY_ID -> TB_CATEGORY.CATEGORY_ID`. The context does not show any bridge or mapping table that would allow one product to be linked to multiple categories…

**Sources retrieved (12):** `parent_chunk_business_glossary.txt_0`, `TB_PRODUCT→TB_CATEGORY`, `Hierarchical product category tree→TB_PRODUCT`, `parent_chunk_business_glossary.txt_1`, `parent_chunk_data_dictionary.txt_3`, `parent_chunk_data_dictionary.txt_4`, `ORDER_LINE_ITEM→TB_PRODUCT`, `parent_chunk_business_glossary.txt_2`

**Context previews (first 3):**

1. _# Business Glossary - E-Commerce Domain (Simplified)  This document defines the core business concepts for the e-commerce platform test dataset.  ──────────────────────────────────────────────────────…_

2. _Relationship: TB_PRODUCT references TB_CATEGORY via foreign key CATEGORY_ID -> TB_CATEGORY.CATEGORY_ID.…_

3. _Business concept 'Hierarchical product category tree' is implemented by physical table TB_PRODUCT (columns: PRODUCT_ID, SKU, PRODUCT_NAME, CATEGORY_ID, UNIT_PRICE, IS_ACTIVE).…_

---

### ✅ Q014 — Is it possible for a customer to place an order without payment?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0719 | **Gate:** `proceed_with_warning`

**Expected answer:**
> Yes, an order can exist without payment. SALES_ORDER_HDR has STATUS_CODE defaulting to PENDING and PAYMENT_CONFIRMED_AT is nullable (NULL when no payment yet). The PAYMENT table links via ORDER_ID foreign key but nothing prevents an order from existing without a payment row. However, the business gl…

**System answer:**
> Based on the retrieved context, the model does not describe a Sales Order as existing without payment association. It states that a Sales Order is placed by exactly one Customer and that a Sales Order has one or more Payments, while each Payment is for exactly one Sales Order. In the schema, this is represented by SALES_ORDER_HDR linked to PAYMENT through ORDER_ID, and SALES_ORDER_HDR linked to CU…

**Sources retrieved (12):** `parent_chunk_data_dictionary.txt_3`, `parent_chunk_business_glossary.txt_1`, `parent_chunk_business_glossary.txt_2`, `parent_chunk_business_glossary.txt_0`, `parent_chunk_data_dictionary.txt_4`, `Sales Order Header→SALES_ORDER_HDR`, `Sales Order Header`, `Monetary transaction that settles the total amount due for a Sales Order→PAYMENT`

**Context previews (first 3):**

1. _# Data Dictionary - E-Commerce Database (Simplified)  This document describes the physical database schema for the simplified e-commerce test dataset.  ────────────────────────────────────────────────…_

2. _**Business Context**: Line items break down orders into individual product purchases. Each captures the price at the moment of ordering. **Key Attributes**: - Unique line identifier - References exact…_

3. _Sales Order Relationships: - A Sales Order is placed by exactly one Customer - A Sales Order has one or more Order Line Items - A Sales Order has one or more Payments - A Sales Order has one or more S…_

---

### ✅ Q015 — What is the total value of all orders placed by a customer?

**Status:** GROUNDED  
**GT Coverage:** 50% | **Top Score:** 0.0311 | **Gate:** `proceed_with_warning`

**Expected answer:**
> Sum the TOTAL_AMT column from SALES_ORDER_HDR for all records where CUST_ID matches the customer's ID. This aggregates the monetary value of all orders placed by that customer.

**System answer:**
> The knowledge graph does not contain instance-level order records, so it cannot return the numeric total for a specific customer. It only provides schema metadata.

From the schema, the customer-to-order path is CUSTOMER_MASTER.CUST_ID → SALES_ORDER_HDR.CUST_ID. The table SALES_ORDER_HDR represents the sales order header and includes ORDER_ID, CUST_ID, and TOTAL_AMT. So, at the schema level, the t…

**Sources retrieved (12):** `parent_chunk_business_glossary.txt_1`, `parent_chunk_business_glossary.txt_0`, `parent_chunk_data_dictionary.txt_3`, `parent_chunk_business_glossary.txt_2`, `Sales Order Header→SALES_ORDER_HDR`, `parent_chunk_data_dictionary.txt_4`, `Monetary transaction that settles the total amount due for a Sales Order→PAYMENT`, `Sales Order Header`

**Context previews (first 3):**

1. _**Business Context**: Line items break down orders into individual product purchases. Each captures the price at the moment of ordering. **Key Attributes**: - Unique line identifier - References exact…_

2. _# Business Glossary - E-Commerce Domain (Simplified)  This document defines the core business concepts for the e-commerce platform test dataset.  ──────────────────────────────────────────────────────…_

3. _# Data Dictionary - E-Commerce Database (Simplified)  This document describes the physical database schema for the simplified e-commerce test dataset.  ────────────────────────────────────────────────…_

---

## Anomalies & Observations

No anomalies detected. All questions grounded with acceptable RAGAS scores.
