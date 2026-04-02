# AB-13 — 01_basics_ecommerce — Run Analysis

**Timestamp:** 2026-04-01 03:14:57  
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

| Metric | Value |
|--------|-------|
| Triplets extracted | 228 |
| Entities resolved | 69 |
| Tables parsed | 7 |
| Tables completed | 7 |

## Query Evaluation Summary

| Metric | Value |
|--------|-------|
| Questions | 15 |
| Grounded | **15/15 (100%)** |
| Avg GT Coverage | 96% |
| Avg Top Score | 0.3934 |
| Avg Chunk Count | 12.0 |
| Abstained | 0 |

## RAGAS Metrics

RAGAS evaluation not enabled for this run.

## Per-Question Deep Dive

### ✅ Q001 — What information is stored for each customer?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.2800 | **Gate:** `proceed`

**Expected answer:**
> Each customer has a unique ID, full name, email address, geographic region code, creation date, and active status. The email must be unique across all customers.

**System answer:**
> For each customer, the physical table CUSTOMER_MASTER stores the customer’s unique identifier (CUST_ID), full name (FULL_NAME), unique email address used for login (EMAIL), geographic region for tax (REGION_CODE), account creation timestamp (CREATED_AT), and whether the customer is active and can place orders (IS_ACTIVE).

From the business glossary, the customer concept also includes a valid emai…

**Sources retrieved (12):** `the customer, items, payment status, and delivery information→CUSTOMER_MASTER`, `Header record for each customer sales order→SALES_ORDER_HDR`, `the customer, items, payment status, and delivery information→PAYMENT`, `parent_chunk_data_dictionary.txt_3`, `parent_chunk_business_glossary.txt_0`, `parent_chunk_business_glossary.txt_1`, `SALES_ORDER_HDR→CUSTOMER_MASTER`, `parent_chunk_business_glossary.txt_2`

**Context previews (first 3):**

1. _Business concept 'the customer, items, payment status, and delivery information' is implemented by physical table CUSTOMER_MASTER (columns: CUST_ID, FULL_NAME, EMAIL, REGION_CODE, CREATED_AT, IS_ACTIV…_

2. _Business concept 'Header record for each customer sales order' is implemented by physical table SALES_ORDER_HDR (columns: ORDER_ID, CUST_ID, ORDER_DATE, TOTAL_AMT, STATUS_CODE, PAYMENT_CONFIRMED_AT, D…_

3. _Business concept 'the customer, items, payment status, and delivery information' is implemented by physical table PAYMENT (columns: PAYMENT_ID, ORDER_ID, PAYMENT_METHOD, AMOUNT, STATUS_CODE, CONFIRMED…_

---

### ✅ Q002 — How are products categorized on the platform?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.1590 | **Gate:** `proceed_with_warning`

**Expected answer:**
> Products belong to categories which can have a parent category, forming a hierarchical tree structure. Each product references exactly one category through its CATEGORY_ID.

**System answer:**
> Products are categorized through a category structure centered on TB_CATEGORY and linked from TB_PRODUCT. Each product record in TB_PRODUCT has a CATEGORY_ID column, and that column is a foreign key to TB_CATEGORY.CATEGORY_ID. This means every product is assigned to a category through TB_PRODUCT.CATEGORY_ID → TB_CATEGORY.CATEGORY_ID.

The category model is hierarchical. The context explicitly refe…

**Sources retrieved (12):** `parent_chunk_business_glossary.txt_0`, `parent_chunk_data_dictionary.txt_3`, `parent_chunk_business_glossary.txt_1`, `parent_chunk_data_dictionary.txt_4`, `parent_chunk_data_dictionary.txt_5`, `Hierarchical product category tree→TB_PRODUCT`, `TB_PRODUCT→TB_CATEGORY`, `Hierarchical product category tree→TB_CATEGORY`

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
> A Sales Order is placed by exactly one Customer. In the physical schema, this relationship is implemented by SALES_ORDER_HDR.CUST_ID as a foreign key to CUSTOMER_MASTER.CUST_ID.

So, CUSTOMER_MASTER is the customer parent table, and SALES_ORDER_HDR stores the sales orders linked to customers through CUST_ID. The glossary also says Customer is related to SalesOrder, and that a customer is someone w…

**Sources retrieved (12):** `parent_chunk_business_glossary.txt_2`, `parent_chunk_business_glossary.txt_0`, `parent_chunk_business_glossary.txt_1`, `parent_chunk_data_dictionary.txt_4`, `Header record for each customer sales order→SALES_ORDER_HDR`, `SALES_ORDER_HDR→CUSTOMER_MASTER`, `parent_chunk_data_dictionary.txt_3`, `the customer, items, payment status, and delivery information→PAYMENT`

**Context previews (first 3):**

1. _Sales Order Relationships: - A Sales Order is placed by exactly one Customer - A Sales Order has one or more Order Line Items - A Sales Order has one or more Payments - A Sales Order has one or more S…_

2. _# Business Glossary - E-Commerce Domain (Simplified)  This document defines the core business concepts for the e-commerce platform test dataset.  ──────────────────────────────────────────────────────…_

3. _**Business Context**: Line items break down orders into individual product purchases. Each captures the price at the moment of ordering. **Key Attributes**: - Unique line identifier - References exact…_

---

### ✅ Q004 — What does an order line item contain?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.9804 | **Gate:** `proceed`

**Expected answer:**
> An order line item specifies a product, the quantity ordered, the unit price at time of purchase, and the calculated extended amount. Each line item belongs to exactly one sales order.

**System answer:**
> An order line item contains the details of one product purchase within a sales order. In the business concept “Order Line Item,” it includes a unique line identifier, a reference to exactly one sales order, a reference to exactly one product, the quantity ordered, the unit price at the time of ordering, and the extended line amount calculated as quantity × unit price.

In the physical table ORDER_…

**Sources retrieved (12):** `Order Line Item`, `Order Line Item→ORDER_LINE_ITEM`, `parent_chunk_business_glossary.txt_1`, `ORDER_LINE_ITEM→TB_PRODUCT`, `ORDER_LINE_ITEM→SALES_ORDER_HDR`, `parent_chunk_business_glossary.txt_2`, `parent_chunk_data_dictionary.txt_4`, `parent_chunk_business_glossary.txt_0`

**Context previews (first 3):**

1. _Order Line Item: The table structure matches an order line item entity: it has its own line identifier, foreign keys to SALES_ORDER_HDR and TB_PRODUCT, plus quantity, unit price, and line amount. The …_

2. _Business concept 'Order Line Item' — The table structure matches an order line item entity: it has its own line identifier, foreign keys to SALES_ORDER_HDR and TB_PRODUCT, plus quantity, unit price, a…_

3. _**Business Context**: Line items break down orders into individual product purchases. Each captures the price at the moment of ordering. **Key Attributes**: - Unique line identifier - References exact…_

---

### ✅ Q005 — How are payments linked to orders?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.9232 | **Gate:** `proceed`

**Expected answer:**
> Each payment is associated with exactly one sales order through the ORDER_ID foreign key. Payments track the payment method, amount, status, and confirmation timestamp.

**System answer:**
> Payments are linked to orders through the PAYMENT.ORDER_ID foreign key, which references SALES_ORDER_HDR.ORDER_ID.

From the context, this means:
The physical relationship is PAYMENT → SALES_ORDER_HDR on ORDER_ID.
A Payment is for exactly one Sales Order.
A Sales Order has one or more Payments.

The relevant tables and columns shown are:
PAYMENT: PAYMENT_ID, ORDER_ID, PAYMENT_METHOD, AMOUNT, STATU…

**Sources retrieved (12):** `PAYMENT→SALES_ORDER_HDR`, `parent_chunk_business_glossary.txt_1`, `parent_chunk_business_glossary.txt_2`, `parent_chunk_data_dictionary.txt_4`, `SHIPMENT→SALES_ORDER_HDR`, `ORDER_LINE_ITEM→SALES_ORDER_HDR`, `SALES_ORDER_HDR→CUSTOMER_MASTER`, `parent_chunk_business_glossary.txt_0`

**Context previews (first 3):**

1. _Relationship: PAYMENT references SALES_ORDER_HDR via foreign key ORDER_ID -> SALES_ORDER_HDR.ORDER_ID.…_

2. _**Business Context**: Line items break down orders into individual product purchases. Each captures the price at the moment of ordering. **Key Attributes**: - Unique line identifier - References exact…_

3. _Sales Order Relationships: - A Sales Order is placed by exactly one Customer - A Sales Order has one or more Order Line Items - A Sales Order has one or more Payments - A Sales Order has one or more S…_

---

### ✅ Q006 — What statuses can an order have?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.1803 | **Gate:** `proceed_with_warning`

**Expected answer:**
> Orders can have one of five statuses defined via CHECK constraint on SALES_ORDER_HDR.STATUS_CODE: PENDING (initial state when order is created), CONFIRMED (payment has been received), SHIPPED (dispatched to customer), DELIVERED (received by customer), or CANCELLED. The business glossary describes th…

**System answer:**
> The retrieved context does not list the allowed order status values.

What it does show is that order status is stored in SALES_ORDER_HDR.STATUS_CODE for the business concept “Header record for each customer sales order.” The same table also includes PAYMENT_CONFIRMED_AT and DELIVERED_AT, which indicates the order tracks at least payment confirmation and delivery milestones, but the actual STATUS_…

**Sources retrieved (12):** `parent_chunk_business_glossary.txt_0`, `parent_chunk_business_glossary.txt_1`, `Header record for each customer sales order→SALES_ORDER_HDR`, `the customer, items, payment status, and delivery information→PAYMENT`, `SHIPMENT_ID (BIGINT, auto-increment)→SHIPMENT`, `parent_chunk_business_glossary.txt_2`, `Order Line Item`, `Order Line Item→ORDER_LINE_ITEM`

**Context previews (first 3):**

1. _# Business Glossary - E-Commerce Domain (Simplified)  This document defines the core business concepts for the e-commerce platform test dataset.  ──────────────────────────────────────────────────────…_

2. _**Business Context**: Line items break down orders into individual product purchases. Each captures the price at the moment of ordering. **Key Attributes**: - Unique line identifier - References exact…_

3. _Business concept 'Header record for each customer sales order' is implemented by physical table SALES_ORDER_HDR (columns: ORDER_ID, CUST_ID, ORDER_DATE, TOTAL_AMT, STATUS_CODE, PAYMENT_CONFIRMED_AT, D…_

---

### ✅ Q007 — Which table stores the product SKU information?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.5995 | **Gate:** `proceed`

**Expected answer:**
> The TB_PRODUCT table stores the SKU (Stock Keeping Unit) code for each product, along with product name, category, price, and active status.

**System answer:**
> The product SKU is stored in the TB_PRODUCT table, in the SKU column.

**Sources retrieved (12):** `Hierarchical product category tree→TB_PRODUCT`, `Order Line Item→ORDER_LINE_ITEM`, `parent_chunk_data_dictionary.txt_3`, `Order Line Item`, `ORDER_LINE_ITEM→TB_PRODUCT`, `Hierarchical product category tree→TB_CATEGORY`, `parent_chunk_business_glossary.txt_0`, `TB_PRODUCT→TB_CATEGORY`

**Context previews (first 3):**

1. _Business concept 'Hierarchical product category tree' is implemented by physical table TB_PRODUCT (columns: PRODUCT_ID, SKU, PRODUCT_NAME, CATEGORY_ID, UNIT_PRICE, IS_ACTIVE).…_

2. _Business concept 'Order Line Item' — The table structure matches an order line item entity: it has its own line identifier, foreign keys to SALES_ORDER_HDR and TB_PRODUCT, plus quantity, unit price, a…_

3. _# Data Dictionary - E-Commerce Database (Simplified)  This document describes the physical database schema for the simplified e-commerce test dataset.  ────────────────────────────────────────────────…_

---

### ✅ Q008 — How can I find all orders placed by a specific customer?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.1428 | **Gate:** `proceed_with_warning`

**Expected answer:**
> Query the SALES_ORDER_HDR table filtering by CUST_ID. Each order has a foreign key reference to CUSTOMER_MASTER.CUST_ID, so joining these tables on CUST_ID will show all orders for a customer along with their details.

**System answer:**
> Use the relationship between CUSTOMER_MASTER and SALES_ORDER_HDR.

At the schema level, all customer orders are stored in SALES_ORDER_HDR, and that table references the customer in CUSTOMER_MASTER through the foreign key SALES_ORDER_HDR.CUST_ID → CUSTOMER_MASTER.CUST_ID. The context explicitly states that a Sales Order is placed by exactly one Customer.

So to find all orders for a specific custom…

**Sources retrieved (12):** `parent_chunk_data_dictionary.txt_3`, `parent_chunk_business_glossary.txt_2`, `parent_chunk_business_glossary.txt_0`, `Header record for each customer sales order→SALES_ORDER_HDR`, `parent_chunk_data_dictionary.txt_4`, `SALES_ORDER_HDR→CUSTOMER_MASTER`, `parent_chunk_business_glossary.txt_1`, `the customer, items, payment status, and delivery information→PAYMENT`

**Context previews (first 3):**

1. _# Data Dictionary - E-Commerce Database (Simplified)  This document describes the physical database schema for the simplified e-commerce test dataset.  ────────────────────────────────────────────────…_

2. _Sales Order Relationships: - A Sales Order is placed by exactly one Customer - A Sales Order has one or more Order Line Items - A Sales Order has one or more Payments - A Sales Order has one or more S…_

3. _# Business Glossary - E-Commerce Domain (Simplified)  This document defines the core business concepts for the e-commerce platform test dataset.  ──────────────────────────────────────────────────────…_

---

### ✅ Q009 — What products were included in a specific order?

**Status:** GROUNDED  
**GT Coverage:** 67% | **Top Score:** 0.0782 | **Gate:** `proceed_with_warning`

**Expected answer:**
> Join ORDER_LINE_ITEM with TB_PRODUCT on PRODUCT_ID. For order ORDER_ID, the line items show which products were ordered, in what quantity, and at what price.

**System answer:**
> The knowledge graph contains schema-level metadata only, not actual order records, so it does not say which products were included in any specific order instance.

From the schema, products in a specific order are traced through ORDER_LINE_ITEM. The relevant path is SALES_ORDER_HDR.ORDER_ID → ORDER_LINE_ITEM.ORDER_ID, then ORDER_LINE_ITEM.PRODUCT_ID → TB_PRODUCT.PRODUCT_ID. ORDER_LINE_ITEM stores …

**Sources retrieved (12):** `parent_chunk_data_dictionary.txt_4`, `parent_chunk_business_glossary.txt_1`, `Order Line Item`, `ORDER_LINE_ITEM→TB_PRODUCT`, `Order Line Item→ORDER_LINE_ITEM`, `parent_chunk_business_glossary.txt_0`, `parent_chunk_data_dictionary.txt_3`, `parent_chunk_business_glossary.txt_2`

**Context previews (first 3):**

1. _**Foreign Keys**: - CUST_ID → CUSTOMER_MASTER(CUST_ID) **Business Concept Mapping**: SalesOrder ──────────────────────────────────────────────────────────── ORDER_LINE_ITEM ───────────────────────────…_

2. _**Business Context**: Line items break down orders into individual product purchases. Each captures the price at the moment of ordering. **Key Attributes**: - Unique line identifier - References exact…_

3. _Order Line Item: The table structure matches an order line item entity: it has its own line identifier, foreign keys to SALES_ORDER_HDR and TB_PRODUCT, plus quantity, unit price, and line amount. The …_

---

### ✅ Q010 — Show me the order hierarchy from customer to line items.

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.3719 | **Gate:** `proceed`

**Expected answer:**
> The hierarchy is: Customer (CUSTOMER_MASTER) → SalesOrder (SALES_ORDER_HDR) → OrderLineItem (ORDER_LINE_ITEM) → Product (TB_PRODUCT). Each customer has orders, each order has line items, and each line item references a product.

**System answer:**
> The order hierarchy in the schema is:

Customer → Sales Order → Order Line Item

At the table level, that path is:

CUSTOMER_MASTER.CUST_ID → SALES_ORDER_HDR.CUST_ID → ORDER_LINE_ITEM.ORDER_ID via SALES_ORDER_HDR.ORDER_ID

From the retrieved context, the hierarchy works as follows:

A Sales Order is placed by exactly one Customer, and a Sales Order has one or more Order Line Items. Each Order Line…

**Sources retrieved (12):** `parent_chunk_business_glossary.txt_2`, `parent_chunk_data_dictionary.txt_4`, `Order Line Item`, `parent_chunk_business_glossary.txt_1`, `Order Line Item→ORDER_LINE_ITEM`, `ORDER_LINE_ITEM→TB_PRODUCT`, `ORDER_LINE_ITEM→SALES_ORDER_HDR`, `Header record for each customer sales order→SALES_ORDER_HDR`

**Context previews (first 3):**

1. _Sales Order Relationships: - A Sales Order is placed by exactly one Customer - A Sales Order has one or more Order Line Items - A Sales Order has one or more Payments - A Sales Order has one or more S…_

2. _**Foreign Keys**: - CUST_ID → CUSTOMER_MASTER(CUST_ID) **Business Concept Mapping**: SalesOrder ──────────────────────────────────────────────────────────── ORDER_LINE_ITEM ───────────────────────────…_

3. _Order Line Item: The table structure matches an order line item entity: it has its own line identifier, foreign keys to SALES_ORDER_HDR and TB_PRODUCT, plus quantity, unit price, and line amount. The …_

---

### ✅ Q011 — What happens when a payment is confirmed for an order?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.3521 | **Gate:** `proceed`

**Expected answer:**
> When payment is confirmed, the PAYMENT record's STATUS_CODE becomes 'CONFIRMED', the CONFIRMED_AT timestamp is set, and the associated SALES_ORDER_HDR can progress from PENDING to CONFIRMED status.

**System answer:**
> When a payment is confirmed, the schema shows that confirmation is recorded at both the payment and order-header level. In the PAYMENT table, the relevant fields are STATUS_CODE and CONFIRMED_AT for that specific payment record, and each PAYMENT belongs to exactly one sales order through PAYMENT.ORDER_ID → SALES_ORDER_HDR.ORDER_ID. In the SALES_ORDER_HDR table, the order also has a PAYMENT_CONFIRM…

**Sources retrieved (12):** `parent_chunk_business_glossary.txt_1`, `Header record for each customer sales order→SALES_ORDER_HDR`, `the customer, items, payment status, and delivery information→PAYMENT`, `PAYMENT→SALES_ORDER_HDR`, `parent_chunk_data_dictionary.txt_4`, `parent_chunk_business_glossary.txt_0`, `parent_chunk_business_glossary.txt_2`, `parent_chunk_data_dictionary.txt_3`

**Context previews (first 3):**

1. _**Business Context**: Line items break down orders into individual product purchases. Each captures the price at the moment of ordering. **Key Attributes**: - Unique line identifier - References exact…_

2. _Business concept 'Header record for each customer sales order' is implemented by physical table SALES_ORDER_HDR (columns: ORDER_ID, CUST_ID, ORDER_DATE, TOTAL_AMT, STATUS_CODE, PAYMENT_CONFIRMED_AT, D…_

3. _Business concept 'the customer, items, payment status, and delivery information' is implemented by physical table PAYMENT (columns: PAYMENT_ID, ORDER_ID, PAYMENT_METHOD, AMOUNT, STATUS_CODE, CONFIRMED…_

---

### ✅ Q012 — How are shipments related to orders and warehouses?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.3848 | **Gate:** `proceed`

**Expected answer:**
> Each shipment is for exactly one sales order (ORDER_ID in SHIPMENT references SALES_ORDER_HDR). The shipment also specifies the source warehouse code and includes tracking information and delivery status.

**System answer:**
> Shipments are related to orders at both the business and schema level. The business relationship states that a Shipment is for exactly one Sales Order. In the physical schema, SHIPMENT has an ORDER_ID column, and the retrieved foreign key definition says SHIPMENT references SALES_ORDER_HDR via ORDER_ID -> SALES_ORDER_HDR.ORDER_ID.

For warehouses, the business relationship states that a Shipment c…

**Sources retrieved (12):** `parent_chunk_business_glossary.txt_2`, `SHIPMENT_ID (BIGINT, auto-increment)→SHIPMENT`, `parent_chunk_business_glossary.txt_0`, `parent_chunk_business_glossary.txt_1`, `the customer, items, payment status, and delivery information→PAYMENT`, `parent_chunk_data_dictionary.txt_4`, `parent_chunk_data_dictionary.txt_3`, `the customer, items, payment status, and delivery information→CUSTOMER_MASTER`

**Context previews (first 3):**

1. _Sales Order Relationships: - A Sales Order is placed by exactly one Customer - A Sales Order has one or more Order Line Items - A Sales Order has one or more Payments - A Sales Order has one or more S…_

2. _Business concept 'SHIPMENT_ID (BIGINT, auto-increment)' is implemented by physical table SHIPMENT (columns: SHIPMENT_ID, ORDER_ID, WAREHOUSE_CODE, SHIPPED_AT, TRACKING_NUMBER, STATUS_CODE).…_

3. _# Business Glossary - E-Commerce Domain (Simplified)  This document defines the core business concepts for the e-commerce platform test dataset.  ──────────────────────────────────────────────────────…_

---

### ✅ Q013 — Can a product belong to multiple categories?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.3613 | **Gate:** `proceed`

**Expected answer:**
> No, each product belongs to exactly one category. The TB_PRODUCT table has a CATEGORY_ID foreign key referencing TB_CATEGORY, which stores a single category value per product.

**System answer:**
> Based on the retrieved schema, a product has one documented direct category assignment: TB_PRODUCT.CATEGORY_ID is a foreign key to TB_CATEGORY.CATEGORY_ID.

The context does not show any additional table or second category key that would allow multiple direct categories per product. So, from the documented model, a product belongs to one category in TB_PRODUCT.

TB_CATEGORY is hierarchical because…

**Sources retrieved (12):** `parent_chunk_business_glossary.txt_0`, `TB_PRODUCT→TB_CATEGORY`, `Hierarchical product category tree→TB_PRODUCT`, `parent_chunk_business_glossary.txt_1`, `Hierarchical product category tree→TB_CATEGORY`, `parent_chunk_data_dictionary.txt_3`, `parent_chunk_data_dictionary.txt_4`, `Order Line Item→ORDER_LINE_ITEM`

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
> Based on the retrieved context, the model does not represent a customer order without payment. A Sales Order is placed by exactly one Customer, and a Sales Order has one or more Payments. This is implemented by PAYMENT.ORDER_ID referencing SALES_ORDER_HDR.ORDER_ID, and SALES_ORDER_HDR referencing CUSTOMER_MASTER via CUST_ID.

So, at the schema/business-relationship level, an order is expected to h…

**Sources retrieved (12):** `parent_chunk_data_dictionary.txt_3`, `parent_chunk_business_glossary.txt_1`, `parent_chunk_business_glossary.txt_2`, `parent_chunk_business_glossary.txt_0`, `parent_chunk_data_dictionary.txt_4`, `the customer, items, payment status, and delivery information→PAYMENT`, `Header record for each customer sales order→SALES_ORDER_HDR`, `the customer, items, payment status, and delivery information→CUSTOMER_MASTER`

**Context previews (first 3):**

1. _# Data Dictionary - E-Commerce Database (Simplified)  This document describes the physical database schema for the simplified e-commerce test dataset.  ────────────────────────────────────────────────…_

2. _**Business Context**: Line items break down orders into individual product purchases. Each captures the price at the moment of ordering. **Key Attributes**: - Unique line identifier - References exact…_

3. _Sales Order Relationships: - A Sales Order is placed by exactly one Customer - A Sales Order has one or more Order Line Items - A Sales Order has one or more Payments - A Sales Order has one or more S…_

---

### ✅ Q015 — What is the total value of all orders placed by a customer?

**Status:** GROUNDED  
**GT Coverage:** 75% | **Top Score:** 0.0311 | **Gate:** `proceed_with_warning`

**Expected answer:**
> Sum the TOTAL_AMT column from SALES_ORDER_HDR for all records where CUST_ID matches the customer's ID. This aggregates the monetary value of all orders placed by that customer.

**System answer:**
> The retrieved context does not contain actual customer or order records, so I cannot give a numeric total for any specific customer. It contains schema-level metadata only.

From the schema, the total value of all orders placed by a customer would be traced through CUSTOMER_MASTER and SALES_ORDER_HDR using CUSTOMER_MASTER.CUST_ID = SALES_ORDER_HDR.CUST_ID, because a Sales Order is placed by exactl…

**Sources retrieved (12):** `parent_chunk_business_glossary.txt_1`, `parent_chunk_business_glossary.txt_0`, `parent_chunk_data_dictionary.txt_3`, `parent_chunk_business_glossary.txt_2`, `parent_chunk_data_dictionary.txt_4`, `Header record for each customer sales order→SALES_ORDER_HDR`, `the customer, items, payment status, and delivery information→PAYMENT`, `Header record for each customer sales order`

**Context previews (first 3):**

1. _**Business Context**: Line items break down orders into individual product purchases. Each captures the price at the moment of ordering. **Key Attributes**: - Unique line identifier - References exact…_

2. _# Business Glossary - E-Commerce Domain (Simplified)  This document defines the core business concepts for the e-commerce platform test dataset.  ──────────────────────────────────────────────────────…_

3. _# Data Dictionary - E-Commerce Database (Simplified)  This document describes the physical database schema for the simplified e-commerce test dataset.  ────────────────────────────────────────────────…_

---

## Anomalies & Observations

No anomalies detected. All questions grounded with acceptable RAGAS scores.
