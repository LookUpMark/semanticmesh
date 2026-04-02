# AB-20 — 01_basics_ecommerce — Run Analysis

**Timestamp:** 2026-03-30 21:23:06  
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
| ER similarity threshold | `0.75` |

## Builder Results

Builder skipped (`--no-builder`).

## Query Evaluation Summary

| Metric | Value |
|--------|-------|
| Questions | 15 |
| Grounded | **15/15 (100%)** |
| Avg GT Coverage | 97% |
| Avg Top Score | 0.4197 |
| Avg Chunk Count | 12.0 |
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
> For each customer, the customer master record is stored in CUSTOMER_MASTER. It contains:

CUST_ID, the unique customer identifier; FULL_NAME, the customer’s full name; EMAIL, the unique email address used for login; REGION_CODE, the customer’s geographic region for tax; CREATED_AT, the account creation timestamp; and IS_ACTIVE, which indicates whether the customer can place orders.

The business g…

**Sources retrieved (12):** `Customer Master→CUSTOMER_MASTER`, `Sales Order Header→SALES_ORDER_HDR`, `parent_chunk_data_dictionary.txt_3`, `parent_chunk_business_glossary.txt_0`, `parent_chunk_business_glossary.txt_1`, `SALES_ORDER_HDR→CUSTOMER_MASTER`, `parent_chunk_business_glossary.txt_2`, `parent_chunk_data_dictionary.txt_4`

**Context previews (first 3):**

1. _Business concept 'Customer Master' — The table stores core customer identity attributes such as full name, email, region, creation timestamp, and active status, which aligns directly with the master r…_

2. _Business concept 'Sales Order Header' — The table name and structure indicate it is the header-level record for an order, with order ID, customer ID, order date, total amount, and status timestamps. T…_

3. _# Data Dictionary - E-Commerce Database (Simplified)  This document describes the physical database schema for the simplified e-commerce test dataset.  ────────────────────────────────────────────────…_

---

### ✅ Q002 — How are products categorized on the platform?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.1590 | **Gate:** `proceed_with_warning`

**Expected answer:**
> Products belong to categories which can have a parent category, forming a hierarchical tree structure. Each product references exactly one category through its CATEGORY_ID.

**System answer:**
> Products are categorized by linking each product in TB_PRODUCT to a category in TB_CATEGORY through TB_PRODUCT.CATEGORY_ID → TB_CATEGORY.CATEGORY_ID.

The category structure is hierarchical: TB_CATEGORY has a self-reference on PARENT_CATEGORY_ID → TB_CATEGORY.CATEGORY_ID, which means categories can be arranged in a parent/child tree. Combining these relationships, a product belongs to one category…

**Sources retrieved (12):** `parent_chunk_business_glossary.txt_0`, `parent_chunk_data_dictionary.txt_3`, `parent_chunk_business_glossary.txt_1`, `Customer Master→CUSTOMER_MASTER`, `parent_chunk_data_dictionary.txt_4`, `Customer Master`, `parent_chunk_data_dictionary.txt_5`, `Hierarchical product category tree→TB_PRODUCT`

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
> A customer-to-sales-order relationship is one-to-many based on the retrieved context: each Sales Order is placed by exactly one Customer, while a Customer can place orders.

At the schema level, this is implemented by SALES_ORDER_HDR.CUST_ID as a foreign key to CUSTOMER_MASTER.CUST_ID. That means each row in SALES_ORDER_HDR belongs to one customer record in CUSTOMER_MASTER.

The business glossary …

**Sources retrieved (12):** `parent_chunk_business_glossary.txt_2`, `parent_chunk_business_glossary.txt_0`, `parent_chunk_business_glossary.txt_1`, `Sales Order Header→SALES_ORDER_HDR`, `parent_chunk_data_dictionary.txt_4`, `SALES_ORDER_HDR→CUSTOMER_MASTER`, `parent_chunk_data_dictionary.txt_3`, `Order Payment→PAYMENT`

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
> An order line item, implemented by ORDER_LINE_ITEM, contains the details for one product purchase within a sales order. It includes LINE_ID as the unique line identifier, ORDER_ID as the parent sales order reference, PRODUCT_ID as the referenced product, QUANTITY as the number of units ordered, UNIT_PRICE as the price at the time of ordering, and LINE_AMT as the extended amount calculated as quant…

**Sources retrieved (12):** `parent_chunk_business_glossary.txt_1`, `ORDER_LINE_ITEM→TB_PRODUCT`, `item→ORDER_LINE_ITEM`, `ORDER_LINE_ITEM→SALES_ORDER_HDR`, `parent_chunk_business_glossary.txt_2`, `parent_chunk_data_dictionary.txt_4`, `Sales Order Header→SALES_ORDER_HDR`, `Customer Master→CUSTOMER_MASTER`

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
> Payments are linked to orders through the `PAYMENT.ORDER_ID` foreign key, which references `SALES_ORDER_HDR.ORDER_ID`.

From the schema and business relationships:
`PAYMENT` implements the business concept “Order Payment” and is explicitly scoped to a sales order through `ORDER_ID`.
A payment is for exactly one sales order, while a sales order has one or more payments.
To join payments to orders a…

**Sources retrieved (12):** `PAYMENT→SALES_ORDER_HDR`, `parent_chunk_business_glossary.txt_1`, `parent_chunk_business_glossary.txt_2`, `parent_chunk_data_dictionary.txt_4`, `SHIPMENT→SALES_ORDER_HDR`, `ORDER_LINE_ITEM→SALES_ORDER_HDR`, `SALES_ORDER_HDR→CUSTOMER_MASTER`, `parent_chunk_data_dictionary.txt_5`

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
> The retrieved context shows that an order, implemented by SALES_ORDER_HDR, has a STATUS_CODE column. It also includes PAYMENT_CONFIRMED_AT and DELIVERED_AT timestamp columns, which indicate order lifecycle milestones such as payment confirmation and delivery.

However, the context does not provide the actual allowed STATUS_CODE values for an order, so I cannot list specific order statuses from the…

**Sources retrieved (12):** `Shipment`, `Sales Order Header→SALES_ORDER_HDR`, `parent_chunk_business_glossary.txt_0`, `parent_chunk_business_glossary.txt_1`, `Shipment→SHIPMENT`, `Order Payment→PAYMENT`, `Customer Master→CUSTOMER_MASTER`, `parent_chunk_business_glossary.txt_2`

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

**Sources retrieved (12):** `Hierarchical product category tree→TB_PRODUCT`, `item→ORDER_LINE_ITEM`, `parent_chunk_data_dictionary.txt_3`, `ORDER_LINE_ITEM→TB_PRODUCT`, `Customer Master→CUSTOMER_MASTER`, `Hierarchical product category tree→TB_CATEGORY`, `parent_chunk_business_glossary.txt_0`, `TB_PRODUCT→TB_CATEGORY`

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
> To find all orders placed by a specific customer, use the relationship between CUSTOMER_MASTER and SALES_ORDER_HDR.

The key path is SALES_ORDER_HDR.CUST_ID → CUSTOMER_MASTER.CUST_ID. A Sales Order is placed by exactly one Customer, and SALES_ORDER_HDR stores the order header for each customer order.

At the schema level, the simplest approach is:

If you already know the customer ID, query SALES_…

**Sources retrieved (12):** `parent_chunk_data_dictionary.txt_3`, `parent_chunk_business_glossary.txt_2`, `Sales Order Header→SALES_ORDER_HDR`, `parent_chunk_business_glossary.txt_0`, `parent_chunk_data_dictionary.txt_4`, `Customer Master→CUSTOMER_MASTER`, `SALES_ORDER_HDR→CUSTOMER_MASTER`, `parent_chunk_business_glossary.txt_1`

**Context previews (first 3):**

1. _# Data Dictionary - E-Commerce Database (Simplified)  This document describes the physical database schema for the simplified e-commerce test dataset.  ────────────────────────────────────────────────…_

2. _Sales Order Relationships: - A Sales Order is placed by exactly one Customer - A Sales Order has one or more Order Line Items - A Sales Order has one or more Payments - A Sales Order has one or more S…_

3. _Business concept 'Sales Order Header' — The table name and structure indicate it is the header-level record for an order, with order ID, customer ID, order date, total amount, and status timestamps. T…_

---

### ✅ Q009 — What products were included in a specific order?

**Status:** GROUNDED  
**GT Coverage:** 83% | **Top Score:** 0.0782 | **Gate:** `proceed_with_warning`

**Expected answer:**
> Join ORDER_LINE_ITEM with TB_PRODUCT on PRODUCT_ID. For order ORDER_ID, the line items show which products were ordered, in what quantity, and at what price.

**System answer:**
> The knowledge graph contains schema-level metadata only, not actual order records, so it does not say which products were included in any specific order instance.

From the schema, products in an order are represented in ORDER_LINE_ITEM, which is the order detail table for individual product lines within a sales order. To find the products for a specific order, use the order’s ORDER_ID and look up…

**Sources retrieved (12):** `parent_chunk_data_dictionary.txt_4`, `parent_chunk_business_glossary.txt_1`, `ORDER_LINE_ITEM→TB_PRODUCT`, `parent_chunk_business_glossary.txt_0`, `Order Payment→PAYMENT`, `parent_chunk_data_dictionary.txt_3`, `item→ORDER_LINE_ITEM`, `Order Payment`

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
> The order hierarchy in the schema is Customer → Sales Order Header → Order Line Item.

At the business level, a Sales Order is placed by exactly one Customer, and a Sales Order has one or more Order Line Items. An Order Line Item is part of exactly one Sales Order.

At the table level, this is implemented as CUSTOMER_MASTER → SALES_ORDER_HDR → ORDER_LINE_ITEM. SALES_ORDER_HDR.CUST_ID is a foreign …

**Sources retrieved (12):** `parent_chunk_business_glossary.txt_2`, `parent_chunk_data_dictionary.txt_4`, `parent_chunk_business_glossary.txt_1`, `item→ORDER_LINE_ITEM`, `Sales Order Header→SALES_ORDER_HDR`, `ORDER_LINE_ITEM→TB_PRODUCT`, `ORDER_LINE_ITEM→SALES_ORDER_HDR`, `parent_chunk_business_glossary.txt_0`

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
> When a payment is confirmed, the confirmation is recorded against a specific sales order in the PAYMENT table, which is scoped to an order through PAYMENT.ORDER_ID → SALES_ORDER_HDR.ORDER_ID. The payment record captures the payment method, amount, status, and the confirmation time in PAYMENT.CONFIRMED_AT, along with PAYMENT.STATUS_CODE.

At the order-header level, SALES_ORDER_HDR also includes PAY…

**Sources retrieved (12):** `parent_chunk_business_glossary.txt_1`, `Order Payment→PAYMENT`, `Sales Order Header→SALES_ORDER_HDR`, `PAYMENT→SALES_ORDER_HDR`, `parent_chunk_data_dictionary.txt_4`, `parent_chunk_business_glossary.txt_0`, `parent_chunk_business_glossary.txt_2`, `parent_chunk_data_dictionary.txt_3`

**Context previews (first 3):**

1. _**Business Context**: Line items break down orders into individual product purchases. Each captures the price at the moment of ordering. **Key Attributes**: - Unique line identifier - References exact…_

2. _Business concept 'Order Payment' — The table is explicitly scoped to a sales order through ORDER_ID and captures payment method, amount, status, and confirmation time, which matches an order-settlemen…_

3. _Business concept 'Sales Order Header' — The table name and structure indicate it is the header-level record for an order, with order ID, customer ID, order date, total amount, and status timestamps. T…_

---

### ✅ Q012 — How are shipments related to orders and warehouses?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.5488 | **Gate:** `proceed`

**Expected answer:**
> Each shipment is for exactly one sales order (ORDER_ID in SHIPMENT references SALES_ORDER_HDR). The shipment also specifies the source warehouse code and includes tracking information and delivery status.

**System answer:**
> Shipments are modeled as the logistics fulfillment records for orders. The business concept Shipment is implemented by the SHIPMENT table, which contains SHIPMENT_ID, ORDER_ID, WAREHOUSE_CODE, SHIPPED_AT, TRACKING_NUMBER, and STATUS_CODE.

In relation to orders, a shipment is tied to a sales order through ORDER_ID. The context explicitly states that SHIPMENT references SALES_ORDER_HDR via the fore…

**Sources retrieved (12):** `Shipment`, `Shipment→SHIPMENT`, `parent_chunk_business_glossary.txt_2`, `parent_chunk_business_glossary.txt_0`, `parent_chunk_business_glossary.txt_1`, `Sales Order Header→SALES_ORDER_HDR`, `parent_chunk_data_dictionary.txt_4`, `Order Payment→PAYMENT`

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
> Based on the retrieved schema, no: a product is modeled as belonging to a single category.

The evidence is that TB_PRODUCT has one CATEGORY_ID column, and there is a foreign key from TB_PRODUCT.CATEGORY_ID to TB_CATEGORY.CATEGORY_ID. The context does not show any junction table or repeating category structure that would allow one product to be linked to multiple categories.

What the schema does …

**Sources retrieved (12):** `parent_chunk_business_glossary.txt_0`, `TB_PRODUCT→TB_CATEGORY`, `Hierarchical product category tree→TB_PRODUCT`, `parent_chunk_business_glossary.txt_1`, `Hierarchical product category tree→TB_CATEGORY`, `parent_chunk_data_dictionary.txt_3`, `parent_chunk_data_dictionary.txt_4`, `Customer Master→CUSTOMER_MASTER`

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
> Based on the provided context, a customer is not modeled as having an order without payment at the business/schema level.

The context states that a Sales Order is placed by exactly one Customer, and that a Sales Order has one or more Payments. It also states that a Payment is for exactly one Sales Order, and the PAYMENT table is linked to SALES_ORDER_HDR through ORDER_ID. So in the defined relati…

**Sources retrieved (12):** `parent_chunk_data_dictionary.txt_3`, `parent_chunk_business_glossary.txt_1`, `parent_chunk_business_glossary.txt_2`, `parent_chunk_business_glossary.txt_0`, `Sales Order Header→SALES_ORDER_HDR`, `Order Payment→PAYMENT`, `parent_chunk_data_dictionary.txt_4`, `Customer Master→CUSTOMER_MASTER`

**Context previews (first 3):**

1. _# Data Dictionary - E-Commerce Database (Simplified)  This document describes the physical database schema for the simplified e-commerce test dataset.  ────────────────────────────────────────────────…_

2. _**Business Context**: Line items break down orders into individual product purchases. Each captures the price at the moment of ordering. **Key Attributes**: - Unique line identifier - References exact…_

3. _Sales Order Relationships: - A Sales Order is placed by exactly one Customer - A Sales Order has one or more Order Line Items - A Sales Order has one or more Payments - A Sales Order has one or more S…_

---

### ✅ Q015 — What is the total value of all orders placed by a customer?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0311 | **Gate:** `proceed_with_warning`

**Expected answer:**
> Sum the TOTAL_AMT column from SALES_ORDER_HDR for all records where CUST_ID matches the customer's ID. This aggregates the monetary value of all orders placed by that customer.

**System answer:**
> The knowledge graph contains schema-level metadata only, not actual order records, so it does not provide a numeric total for any specific customer.

From the schema, the total value of all orders placed by a customer would be calculated from SALES_ORDER_HDR, which is the Sales Order header table. SALES_ORDER_HDR contains ORDER_ID, CUST_ID, ORDER_DATE, TOTAL_AMT, STATUS_CODE, PAYMENT_CONFIRMED_AT,…

**Sources retrieved (12):** `parent_chunk_business_glossary.txt_1`, `Sales Order Header→SALES_ORDER_HDR`, `parent_chunk_business_glossary.txt_0`, `parent_chunk_data_dictionary.txt_3`, `parent_chunk_business_glossary.txt_2`, `parent_chunk_data_dictionary.txt_4`, `Customer Master→CUSTOMER_MASTER`, `Sales Order Header`

**Context previews (first 3):**

1. _**Business Context**: Line items break down orders into individual product purchases. Each captures the price at the moment of ordering. **Key Attributes**: - Unique line identifier - References exact…_

2. _Business concept 'Sales Order Header' — The table name and structure indicate it is the header-level record for an order, with order ID, customer ID, order date, total amount, and status timestamps. T…_

3. _# Business Glossary - E-Commerce Domain (Simplified)  This document defines the core business concepts for the e-commerce platform test dataset.  ──────────────────────────────────────────────────────…_

---

## Anomalies & Observations

No anomalies detected. All questions grounded with acceptable RAGAS scores.
