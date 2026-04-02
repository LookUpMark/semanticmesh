# AB-04 — 01_basics_ecommerce — Run Analysis

**Timestamp:** 2026-03-30 21:25:39  
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
| Questions | 15 |
| Grounded | **15/15 (100%)** |
| Avg GT Coverage | 73% |
| Avg Top Score | 0.4197 |
| Avg Chunk Count | 5.0 |
| Abstained | 0 |

## RAGAS Metrics

RAGAS evaluation not enabled for this run.

## Per-Question Deep Dive

### ✅ Q001 — What information is stored for each customer?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.5625 | **Gate:** `proceed`

**Expected answer:**
> Each customer has a unique ID, full name, email address, geographic region code, creation date, and active status. The email must be unique across all customers.

**System answer:**
> For each customer, the Customer Master record is stored in the CUSTOMER_MASTER table. It contains:

CUST_ID, the unique customer identifier; FULL_NAME, the customer’s full name; EMAIL, the unique email address used for login; REGION_CODE, the customer’s geographic region for tax; CREATED_AT, the account creation timestamp; and IS_ACTIVE, which indicates whether the customer can place orders.

The …

**Sources retrieved (5):** `Customer Master→CUSTOMER_MASTER`, `Sales Order Header→SALES_ORDER_HDR`, `parent_chunk_data_dictionary.txt_3`, `Customer Master`, `Sales Order Header`

**Context previews (first 3):**

1. _Business concept 'Customer Master' — The table stores core customer identity attributes such as full name, email, region, creation timestamp, and active status, which aligns directly with the master r…_

2. _Business concept 'Sales Order Header' — The table name and structure indicate it is the header-level record for an order, with order ID, customer ID, order date, total amount, and status timestamps. T…_

3. _# Data Dictionary - E-Commerce Database (Simplified)  This document describes the physical database schema for the simplified e-commerce test dataset.  ────────────────────────────────────────────────…_

---

### ✅ Q002 — How are products categorized on the platform?

**Status:** GROUNDED  
**GT Coverage:** 75% | **Top Score:** 0.1590 | **Gate:** `proceed_with_warning`

**Expected answer:**
> Products belong to categories which can have a parent category, forming a hierarchical tree structure. Each product references exactly one category through its CATEGORY_ID.

**System answer:**
> Products are categorized through a hierarchical product category tree. In the physical schema, this is implemented in the TB_PRODUCT table, which includes the CATEGORY_ID column. Based on the context, TB_PRODUCT is the master catalogue of products, so each product record is assigned a category through CATEGORY_ID. The retrieved context does not provide the separate category table or the detailed h…

**Sources retrieved (5):** `parent_chunk_business_glossary.txt_0`, `parent_chunk_data_dictionary.txt_3`, `parent_chunk_business_glossary.txt_1`, `Customer Master`, `Hierarchical product category tree→TB_PRODUCT`

**Context previews (first 3):**

1. _# Business Glossary - E-Commerce Domain (Simplified)  This document defines the core business concepts for the e-commerce platform test dataset.  ──────────────────────────────────────────────────────…_

2. _# Data Dictionary - E-Commerce Database (Simplified)  This document describes the physical database schema for the simplified e-commerce test dataset.  ────────────────────────────────────────────────…_

3. _**Business Context**: Line items break down orders into individual product purchases. Each captures the price at the moment of ordering. **Key Attributes**: - Unique line identifier - References exact…_

---

### ✅ Q003 — What is the relationship between customers and sales orders?

**Status:** GROUNDED  
**GT Coverage:** 25% | **Top Score:** 0.9847 | **Gate:** `proceed`

**Expected answer:**
> Each sales order is placed by exactly one customer, referenced through the CUST_ID foreign key. A customer can place zero or more orders over time.

**System answer:**
> The retrieved context explicitly states that a Sales Order is placed by exactly one Customer. In the schema, this relationship is implemented by CUSTOMER_MASTER.CUST_ID linking to SALES_ORDER_HDR.CUST_ID.

The business glossary also connects these concepts by stating that customers place orders and listing SalesOrder as a related concept of Customer.

What the context does not explicitly state is …

**Sources retrieved (5):** `parent_chunk_business_glossary.txt_2`, `parent_chunk_business_glossary.txt_0`, `parent_chunk_business_glossary.txt_1`, `Sales Order Header`, `parent_chunk_data_dictionary.txt_5`

**Context previews (first 3):**

1. _Sales Order Relationships: - A Sales Order is placed by exactly one Customer - A Sales Order has one or more Order Line Items - A Sales Order has one or more Payments - A Sales Order has one or more S…_

2. _# Business Glossary - E-Commerce Domain (Simplified)  This document defines the core business concepts for the e-commerce platform test dataset.  ──────────────────────────────────────────────────────…_

3. _**Business Context**: Line items break down orders into individual product purchases. Each captures the price at the moment of ordering. **Key Attributes**: - Unique line identifier - References exact…_

---

### ✅ Q004 — What does an order line item contain?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.8739 | **Gate:** `proceed`

**Expected answer:**
> An order line item specifies a product, the quantity ordered, the unit price at time of purchase, and the calculated extended amount. Each line item belongs to exactly one sales order.

**System answer:**
> An order line item breaks an order into an individual product purchase. From the business definition, it contains a unique line identifier, a reference to exactly one product, the quantity ordered, the unit price at the time of ordering, and the extended amount calculated as quantity × unit price.

In the schema, this is implemented by the ORDER_LINE_ITEM table with columns LINE_ID, ORDER_ID, PROD…

**Sources retrieved (5):** `parent_chunk_business_glossary.txt_1`, `ORDER_LINE_ITEM→TB_PRODUCT`, `item→ORDER_LINE_ITEM`, `ORDER_LINE_ITEM→SALES_ORDER_HDR`, `parent_chunk_business_glossary.txt_2`

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
> Payments are linked to orders through the `PAYMENT` table’s `ORDER_ID`, which is a foreign key to `SALES_ORDER_HDR.ORDER_ID`. In schema terms, you join `PAYMENT.ORDER_ID = SALES_ORDER_HDR.ORDER_ID`.

The context also defines the business relationship this way: a Sales Order has one or more Payments, and a Payment is for exactly one Sales Order. The `PAYMENT` table is explicitly scoped to a sales o…

**Sources retrieved (5):** `PAYMENT→SALES_ORDER_HDR`, `parent_chunk_business_glossary.txt_1`, `parent_chunk_business_glossary.txt_2`, `Order Payment`, `Sales Order Header`

**Context previews (first 3):**

1. _Relationship: PAYMENT references SALES_ORDER_HDR via foreign key ORDER_ID -> SALES_ORDER_HDR.ORDER_ID.…_

2. _**Business Context**: Line items break down orders into individual product purchases. Each captures the price at the moment of ordering. **Key Attributes**: - Unique line identifier - References exact…_

3. _Sales Order Relationships: - A Sales Order is placed by exactly one Customer - A Sales Order has one or more Order Line Items - A Sales Order has one or more Payments - A Sales Order has one or more S…_

---

### ✅ Q006 — What statuses can an order have?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.2353 | **Gate:** `proceed`

**Expected answer:**
> Orders can have one of five statuses defined via CHECK constraint on SALES_ORDER_HDR.STATUS_CODE: PENDING (initial state when order is created), CONFIRMED (payment has been received), SHIPPED (dispatched to customer), DELIVERED (received by customer), or CANCELLED. The business glossary describes th…

**System answer:**
> The retrieved context shows that order status is stored on the Sales Order Header business concept, implemented by table SALES_ORDER_HDR, in column STATUS_CODE. It also includes lifecycle-related timestamps PAYMENT_CONFIRMED_AT and DELIVERED_AT.

However, the context does not provide the actual allowed order status values or a status code list, so I cannot say exactly which statuses an order can h…

**Sources retrieved (5):** `Shipment`, `Sales Order Header→SALES_ORDER_HDR`, `parent_chunk_business_glossary.txt_0`, `parent_chunk_business_glossary.txt_1`, `Sales Order Header`

**Context previews (first 3):**

1. _Shipment: The table name, primary key, shipped timestamp, tracking number, warehouse code, and shipment status all align directly with the business concept of a shipment. The foreign key to SALES_ORDE…_

2. _Business concept 'Sales Order Header' — The table name and structure indicate it is the header-level record for an order, with order ID, customer ID, order date, total amount, and status timestamps. T…_

3. _# Business Glossary - E-Commerce Domain (Simplified)  This document defines the core business concepts for the e-commerce platform test dataset.  ──────────────────────────────────────────────────────…_

---

### ✅ Q007 — Which table stores the product SKU information?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.5995 | **Gate:** `proceed`

**Expected answer:**
> The TB_PRODUCT table stores the SKU (Stock Keeping Unit) code for each product, along with product name, category, price, and active status.

**System answer:**
> The product SKU is stored in the TB_PRODUCT table, in the SKU column.

**Sources retrieved (5):** `Hierarchical product category tree→TB_PRODUCT`, `item→ORDER_LINE_ITEM`, `parent_chunk_data_dictionary.txt_3`, `Customer Master`, `parent_chunk_data_dictionary.txt_5`

**Context previews (first 3):**

1. _Business concept 'Hierarchical product category tree' is implemented by physical table TB_PRODUCT (columns: PRODUCT_ID, SKU, PRODUCT_NAME, CATEGORY_ID, UNIT_PRICE, IS_ACTIVE).…_

2. _Business concept 'item' is implemented by physical table ORDER_LINE_ITEM (columns: LINE_ID, ORDER_ID, PRODUCT_ID, QUANTITY, UNIT_PRICE, LINE_AMT).…_

3. _# Data Dictionary - E-Commerce Database (Simplified)  This document describes the physical database schema for the simplified e-commerce test dataset.  ────────────────────────────────────────────────…_

---

### ✅ Q008 — How can I find all orders placed by a specific customer?

**Status:** GROUNDED  
**GT Coverage:** 50% | **Top Score:** 0.1428 | **Gate:** `proceed_with_warning`

**Expected answer:**
> Query the SALES_ORDER_HDR table filtering by CUST_ID. Each order has a foreign key reference to CUSTOMER_MASTER.CUST_ID, so joining these tables on CUST_ID will show all orders for a customer along with their details.

**System answer:**
> Use the Sales Order Header table, SALES_ORDER_HDR, because it is the header-level record for each customer sales order and includes ORDER_ID, CUST_ID, ORDER_DATE, TOTAL_AMT, STATUS_CODE, PAYMENT_CONFIRMED_AT, DELIVERED_AT, and CREATED_AT.

The key join path is CUSTOMER_MASTER.CUST_ID = SALES_ORDER_HDR.CUST_ID. This is supported by both the schema and the relationship rule that a Sales Order is pla…

**Sources retrieved (5):** `parent_chunk_data_dictionary.txt_3`, `parent_chunk_business_glossary.txt_2`, `Sales Order Header→SALES_ORDER_HDR`, `parent_chunk_business_glossary.txt_0`, `Sales Order Header`

**Context previews (first 3):**

1. _# Data Dictionary - E-Commerce Database (Simplified)  This document describes the physical database schema for the simplified e-commerce test dataset.  ────────────────────────────────────────────────…_

2. _Sales Order Relationships: - A Sales Order is placed by exactly one Customer - A Sales Order has one or more Order Line Items - A Sales Order has one or more Payments - A Sales Order has one or more S…_

3. _Business concept 'Sales Order Header' — The table name and structure indicate it is the header-level record for an order, with order ID, customer ID, order date, total amount, and status timestamps. T…_

---

### ✅ Q009 — What products were included in a specific order?

**Status:** GROUNDED  
**GT Coverage:** 67% | **Top Score:** 0.0782 | **Gate:** `proceed_with_warning`

**Expected answer:**
> Join ORDER_LINE_ITEM with TB_PRODUCT on PRODUCT_ID. For order ORDER_ID, the line items show which products were ordered, in what quantity, and at what price.

**System answer:**
> The retrieved context does not contain actual order records, a specific ORDER_ID, or product values for any individual order, so it cannot determine which products were included in a specific order.

What is known from the context is the schema-level relationship used to answer that question: SALES_ORDER_HDR.ORDER_ID links to ORDER_LINE_ITEM.ORDER_ID, and each ORDER_LINE_ITEM row identifies a prod…

**Sources retrieved (5):** `parent_chunk_data_dictionary.txt_4`, `parent_chunk_business_glossary.txt_1`, `ORDER_LINE_ITEM→TB_PRODUCT`, `Order Payment`, `parent_chunk_data_dictionary.txt_5`

**Context previews (first 3):**

1. _**Foreign Keys**: - CUST_ID → CUSTOMER_MASTER(CUST_ID) **Business Concept Mapping**: SalesOrder ──────────────────────────────────────────────────────────── ORDER_LINE_ITEM ───────────────────────────…_

2. _**Business Context**: Line items break down orders into individual product purchases. Each captures the price at the moment of ordering. **Key Attributes**: - Unique line identifier - References exact…_

3. _Relationship: ORDER_LINE_ITEM references TB_PRODUCT via foreign key PRODUCT_ID -> TB_PRODUCT.PRODUCT_ID.…_

---

### ✅ Q010 — Show me the order hierarchy from customer to line items.

**Status:** GROUNDED  
**GT Coverage:** 25% | **Top Score:** 0.3719 | **Gate:** `proceed`

**Expected answer:**
> The hierarchy is: Customer (CUSTOMER_MASTER) → SalesOrder (SALES_ORDER_HDR) → OrderLineItem (ORDER_LINE_ITEM) → Product (TB_PRODUCT). Each customer has orders, each order has line items, and each line item references a product.

**System answer:**
> The order hierarchy from customer to line items is:

Customer maps to CUSTOMER_MASTER. A customer is linked to sales orders through CUSTOMER_MASTER.CUST_ID → SALES_ORDER_HDR.CUST_ID, so each Sales Order in SALES_ORDER_HDR is placed by exactly one Customer.

SalesOrder maps to SALES_ORDER_HDR. This is the header-level order record, with order ID, customer ID, order date, total amount, and status ti…

**Sources retrieved (5):** `parent_chunk_business_glossary.txt_2`, `parent_chunk_data_dictionary.txt_4`, `parent_chunk_business_glossary.txt_1`, `parent_chunk_data_dictionary.txt_5`, `Sales Order Header`

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
> From the retrieved context, a confirmed payment is represented at the schema level in two places tied to the same order.

The payment itself is stored in the PAYMENT table as an Order Payment record, which is linked to the order by PAYMENT.ORDER_ID -> SALES_ORDER_HDR.ORDER_ID. That payment record captures the payment method, amount, status, and a confirmation timestamp in PAYMENT.CONFIRMED_AT.

At…

**Sources retrieved (5):** `parent_chunk_business_glossary.txt_1`, `Order Payment→PAYMENT`, `Sales Order Header→SALES_ORDER_HDR`, `PAYMENT→SALES_ORDER_HDR`, `Order Payment`

**Context previews (first 3):**

1. _**Business Context**: Line items break down orders into individual product purchases. Each captures the price at the moment of ordering. **Key Attributes**: - Unique line identifier - References exact…_

2. _Business concept 'Order Payment' — The table is explicitly scoped to a sales order through ORDER_ID and captures payment method, amount, status, and confirmation time, which matches an order-settlemen…_

3. _Business concept 'Sales Order Header' — The table name and structure indicate it is the header-level record for an order, with order ID, customer ID, order date, total amount, and status timestamps. T…_

---

### ✅ Q012 — How are shipments related to orders and warehouses?

**Status:** GROUNDED  
**GT Coverage:** 50% | **Top Score:** 0.5488 | **Gate:** `proceed`

**Expected answer:**
> Each shipment is for exactly one sales order (ORDER_ID in SHIPMENT references SALES_ORDER_HDR). The shipment also specifies the source warehouse code and includes tracking information and delivery status.

**System answer:**
> Shipments are tied to orders and warehouses in two ways.

A Shipment is for exactly one Sales Order, and a Sales Order has one or more Shipments. In the physical schema, the business concept Shipment is implemented by the SHIPMENT table, where ORDER_ID links the shipment to the order. The retrieved context also states that the foreign key to SALES_ORDER_HDR shows Shipment represents the logistics …

**Sources retrieved (5):** `Shipment`, `Shipment→SHIPMENT`, `parent_chunk_business_glossary.txt_2`, `parent_chunk_business_glossary.txt_0`, `parent_chunk_business_glossary.txt_1`

**Context previews (first 3):**

1. _Shipment: The table name, primary key, shipped timestamp, tracking number, warehouse code, and shipment status all align directly with the business concept of a shipment. The foreign key to SALES_ORDE…_

2. _Business concept 'Shipment' — The table name, primary key, shipped timestamp, tracking number, warehouse code, and shipment status all align directly with the business concept of a shipment. The forei…_

3. _Sales Order Relationships: - A Sales Order is placed by exactly one Customer - A Sales Order has one or more Order Line Items - A Sales Order has one or more Payments - A Sales Order has one or more S…_

---

### ✅ Q013 — Can a product belong to multiple categories?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.3613 | **Gate:** `proceed`

**Expected answer:**
> No, each product belongs to exactly one category. The TB_PRODUCT table has a CATEGORY_ID foreign key referencing TB_CATEGORY, which stores a single category value per product.

**System answer:**
> Based on the retrieved context, a product is modeled as belonging to a single category, not multiple categories. The physical table TB_PRODUCT has one CATEGORY_ID column, and that column is a foreign key to TB_CATEGORY.CATEGORY_ID. The context does not show any separate mapping or junction table that would allow one product to be assigned to multiple categories.

The category structure itself is h…

**Sources retrieved (5):** `parent_chunk_business_glossary.txt_0`, `TB_PRODUCT→TB_CATEGORY`, `Hierarchical product category tree→TB_PRODUCT`, `parent_chunk_data_dictionary.txt_5`, `Hierarchical product category tree`

**Context previews (first 3):**

1. _# Business Glossary - E-Commerce Domain (Simplified)  This document defines the core business concepts for the e-commerce platform test dataset.  ──────────────────────────────────────────────────────…_

2. _Relationship: TB_PRODUCT references TB_CATEGORY via foreign key CATEGORY_ID -> TB_CATEGORY.CATEGORY_ID.…_

3. _Business concept 'Hierarchical product category tree' is implemented by physical table TB_PRODUCT (columns: PRODUCT_ID, SKU, PRODUCT_NAME, CATEGORY_ID, UNIT_PRICE, IS_ACTIVE).…_

---

### ✅ Q014 — Is it possible for a customer to place an order without payment?

**Status:** GROUNDED  
**GT Coverage:** 50% | **Top Score:** 0.0719 | **Gate:** `proceed_with_warning`

**Expected answer:**
> Yes, an order can exist without payment. SALES_ORDER_HDR has STATUS_CODE defaulting to PENDING and PAYMENT_CONFIRMED_AT is nullable (NULL when no payment yet). The PAYMENT table links via ORDER_ID foreign key but nothing prevents an order from existing without a payment row. However, the business gl…

**System answer:**
> Based on the retrieved context, no: the model does not allow a Sales Order without payment.

The relevant facts are that a Sales Order is placed by exactly one Customer, and a Sales Order has one or more Payments. The Payment relationship also states that a Payment is for exactly one Sales Order. Together, this means any order a customer places is modeled as having at least one associated payment.…

**Sources retrieved (5):** `parent_chunk_data_dictionary.txt_3`, `parent_chunk_business_glossary.txt_1`, `parent_chunk_business_glossary.txt_2`, `parent_chunk_business_glossary.txt_0`, `Sales Order Header→SALES_ORDER_HDR`

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
> From the retrieved context, this cannot be answered as an actual numeric value because the knowledge graph provides schema and business metadata only, not customer order records.

What is known is the relevant structure:
The business concept “Sales Order Header” is implemented by table SALES_ORDER_HDR, which contains ORDER_ID, CUST_ID, ORDER_DATE, TOTAL_AMT, STATUS_CODE, PAYMENT_CONFIRMED_AT, DELI…

**Sources retrieved (5):** `parent_chunk_business_glossary.txt_1`, `Sales Order Header→SALES_ORDER_HDR`, `parent_chunk_business_glossary.txt_0`, `parent_chunk_data_dictionary.txt_3`, `Sales Order Header`

**Context previews (first 3):**

1. _**Business Context**: Line items break down orders into individual product purchases. Each captures the price at the moment of ordering. **Key Attributes**: - Unique line identifier - References exact…_

2. _Business concept 'Sales Order Header' — The table name and structure indicate it is the header-level record for an order, with order ID, customer ID, order date, total amount, and status timestamps. T…_

3. _# Business Glossary - E-Commerce Domain (Simplified)  This document defines the core business concepts for the e-commerce platform test dataset.  ──────────────────────────────────────────────────────…_

---

## Anomalies & Observations

No anomalies detected. All questions grounded with acceptable RAGAS scores.
