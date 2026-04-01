# AB-08 — 01_basics_ecommerce — Run Analysis

**Timestamp:** 2026-03-31 18:19:55  
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
| Chunk size / overlap | `512 / 64` |
| ER similarity threshold | `0.75` |

## Builder Results

| Metric | Value |
|--------|-------|
| Triplets extracted | 248 |
| Entities resolved | 79 |
| Tables parsed | 7 |
| Tables completed | 7 |

## Query Evaluation Summary

| Metric | Value |
|--------|-------|
| Questions | 15 |
| Grounded | **15/15 (100%)** |
| Avg GT Coverage | 100% |
| Avg Top Score | 0.3892 |
| Avg Chunk Count | 12.0 |
| Abstained | 0 |

## RAGAS Metrics

RAGAS evaluation not enabled for this run.

## Per-Question Deep Dive

### ✅ Q001 — What information is stored for each customer?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.2895 | **Gate:** `proceed`

**Expected answer:**
> Each customer has a unique ID, full name, email address, geographic region code, creation date, and active status. The email must be unique across all customers.

**System answer:**
> For each customer, the physical customer master table `CUSTOMER_MASTER` stores: `CUST_ID` (unique customer identifier), `FULL_NAME`, `EMAIL` (unique email address used for login), `REGION_CODE` (geographic region for tax), `CREATED_AT` (account creation timestamp), and `IS_ACTIVE` (whether the customer can place orders).

At the business-concept level, the `Customer` concept also includes a unique…

**Sources retrieved (12):** `Sales Order Header`, `Sales Order Header→SALES_ORDER_HDR`, `the customer, items, payment status, and delivery information→PAYMENT`, `parent_chunk_data_dictionary.txt_3`, `Master record for all registered platform customers→CUSTOMER_MASTER`, `parent_chunk_business_glossary.txt_0`, `parent_chunk_business_glossary.txt_1`, `SALES_ORDER_HDR→CUSTOMER_MASTER`

**Context previews (first 3):**

1. _Sales Order Header: The table name, primary key, customer foreign key, order date, total amount, and status/delivery timestamps all align with a sales order header rather than line items or payments. …_

2. _Business concept 'Sales Order Header' — The table name, primary key, customer foreign key, order date, total amount, and status/delivery timestamps all align with a sales order header rather than line…_

3. _Business concept 'the customer, items, payment status, and delivery information' is implemented by physical table PAYMENT (columns: PAYMENT_ID, ORDER_ID, PAYMENT_METHOD, AMOUNT, STATUS_CODE, CONFIRMED…_

---

### ✅ Q002 — How are products categorized on the platform?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.1590 | **Gate:** `proceed_with_warning`

**Expected answer:**
> Products belong to categories which can have a parent category, forming a hierarchical tree structure. Each product references exactly one category through its CATEGORY_ID.

**System answer:**
> Products are categorized by linking each product in TB_PRODUCT to a category in TB_CATEGORY through TB_PRODUCT.CATEGORY_ID → TB_CATEGORY.CATEGORY_ID.

The category model is a hierarchical product category tree. That hierarchy is stored in TB_CATEGORY, and TB_CATEGORY also has a self-reference through TB_CATEGORY.PARENT_CATEGORY_ID, which means categories can have parent categories and subcategorie…

**Sources retrieved (12):** `parent_chunk_business_glossary.txt_0`, `parent_chunk_data_dictionary.txt_3`, `parent_chunk_business_glossary.txt_1`, `Master record for all registered platform customers→CUSTOMER_MASTER`, `parent_chunk_data_dictionary.txt_4`, `parent_chunk_data_dictionary.txt_5`, `Hierarchical product category tree→TB_PRODUCT`, `TB_PRODUCT→TB_CATEGORY`

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
> The relationship is that each Sales Order belongs to exactly one Customer.

In the schema, the SalesOrder business concept is implemented by SALES_ORDER_HDR, and that table has CUST_ID as a foreign key to CUSTOMER_MASTER(CUST_ID). The context explicitly states: “A Sales Order is placed by exactly one Customer,” and also notes the FK relationship SALES_ORDER_HDR.CUST_ID → CUSTOMER_MASTER.CUST_ID.

…

**Sources retrieved (12):** `parent_chunk_business_glossary.txt_2`, `parent_chunk_business_glossary.txt_0`, `Sales Order Header`, `parent_chunk_business_glossary.txt_1`, `Sales Order Header→SALES_ORDER_HDR`, `parent_chunk_data_dictionary.txt_4`, `SALES_ORDER_HDR→CUSTOMER_MASTER`, `parent_chunk_data_dictionary.txt_3`

**Context previews (first 3):**

1. _Sales Order Relationships: - A Sales Order is placed by exactly one Customer - A Sales Order has one or more Order Line Items - A Sales Order has one or more Payments - A Sales Order has one or more S…_

2. _# Business Glossary - E-Commerce Domain (Simplified)  This document defines the core business concepts for the e-commerce platform test dataset.  ──────────────────────────────────────────────────────…_

3. _Sales Order Header: The table name, primary key, customer foreign key, order date, total amount, and status/delivery timestamps all align with a sales order header rather than line items or payments. …_

---

### ✅ Q004 — What does an order line item contain?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.8739 | **Gate:** `proceed`

**Expected answer:**
> An order line item specifies a product, the quantity ordered, the unit price at time of purchase, and the calculated extended amount. Each line item belongs to exactly one sales order.

**System answer:**
> An order line item represents an individual product purchase within a sales order. In the business context, it contains a unique line identifier, a reference to exactly one product, the quantity ordered, the unit price at the time of ordering, and the extended amount calculated as quantity × unit price.

In the schema, this is implemented by the ORDER_LINE_ITEM table, which contains the columns LI…

**Sources retrieved (12):** `parent_chunk_business_glossary.txt_1`, `ORDER_LINE_ITEM→TB_PRODUCT`, `item→ORDER_LINE_ITEM`, `ORDER_LINE_ITEM→SALES_ORDER_HDR`, `parent_chunk_business_glossary.txt_2`, `parent_chunk_data_dictionary.txt_4`, `Sales Order Header`, `Sales Order Header→SALES_ORDER_HDR`

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
> Payments are linked to orders through the `ORDER_ID` foreign key. The context states that `PAYMENT` references `SALES_ORDER_HDR` via `PAYMENT.ORDER_ID -> SALES_ORDER_HDR.ORDER_ID`.

At the business level, this means a Payment is for exactly one Sales Order, and a Sales Order has one or more Payments.

At the schema level, you link them by joining `PAYMENT.ORDER_ID` to `SALES_ORDER_HDR.ORDER_ID`. T…

**Sources retrieved (12):** `PAYMENT→SALES_ORDER_HDR`, `parent_chunk_business_glossary.txt_1`, `parent_chunk_business_glossary.txt_2`, `Sales Order Header→SALES_ORDER_HDR`, `Sales Order Header`, `parent_chunk_data_dictionary.txt_4`, `SHIPMENT→SALES_ORDER_HDR`, `ORDER_LINE_ITEM→SALES_ORDER_HDR`

**Context previews (first 3):**

1. _Relationship: PAYMENT references SALES_ORDER_HDR via foreign key ORDER_ID -> SALES_ORDER_HDR.ORDER_ID.…_

2. _**Business Context**: Line items break down orders into individual product purchases. Each captures the price at the moment of ordering. **Key Attributes**: - Unique line identifier - References exact…_

3. _Sales Order Relationships: - A Sales Order is placed by exactly one Customer - A Sales Order has one or more Order Line Items - A Sales Order has one or more Payments - A Sales Order has one or more S…_

---

### ✅ Q006 — What statuses can an order have?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.2111 | **Gate:** `proceed`

**Expected answer:**
> Orders can have one of five statuses defined via CHECK constraint on SALES_ORDER_HDR.STATUS_CODE: PENDING (initial state when order is created), CONFIRMED (payment has been received), SHIPPED (dispatched to customer), DELIVERED (received by customer), or CANCELLED. The business glossary describes th…

**System answer:**
> The retrieved context does not list the allowed order status values themselves, so I cannot name specific statuses like exact codes or labels.

What it does show is that order status is captured on the sales order header in SALES_ORDER_HDR.STATUS_CODE. The same table also includes PAYMENT_CONFIRMED_AT and DELIVERED_AT, which indicates the order header tracks payment-confirmation and delivery lifec…

**Sources retrieved (12):** `Sales Order Header`, `parent_chunk_business_glossary.txt_0`, `Sales Order Header→SALES_ORDER_HDR`, `parent_chunk_business_glossary.txt_1`, `the customer, items, payment status, and delivery information→PAYMENT`, `Shipment #S-001→SHIPMENT`, `parent_chunk_business_glossary.txt_2`, `parent_chunk_data_dictionary.txt_4`

**Context previews (first 3):**

1. _Sales Order Header: The table name, primary key, customer foreign key, order date, total amount, and status/delivery timestamps all align with a sales order header rather than line items or payments. …_

2. _# Business Glossary - E-Commerce Domain (Simplified)  This document defines the core business concepts for the e-commerce platform test dataset.  ──────────────────────────────────────────────────────…_

3. _Business concept 'Sales Order Header' — The table name, primary key, customer foreign key, order date, total amount, and status/delivery timestamps all align with a sales order header rather than line…_

---

### ✅ Q007 — Which table stores the product SKU information?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.5995 | **Gate:** `proceed`

**Expected answer:**
> The TB_PRODUCT table stores the SKU (Stock Keeping Unit) code for each product, along with product name, category, price, and active status.

**System answer:**
> The product SKU is stored in TB_PRODUCT, in the SKU column. The retrieved context shows TB_PRODUCT with columns PRODUCT_ID, SKU, PRODUCT_NAME, CATEGORY_ID, UNIT_PRICE, and IS_ACTIVE.

**Sources retrieved (12):** `Hierarchical product category tree→TB_PRODUCT`, `item→ORDER_LINE_ITEM`, `parent_chunk_data_dictionary.txt_3`, `ORDER_LINE_ITEM→TB_PRODUCT`, `Hierarchical product category tree→TB_CATEGORY`, `parent_chunk_business_glossary.txt_0`, `TB_PRODUCT→TB_CATEGORY`, `parent_chunk_data_dictionary.txt_5`

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
> To find all orders placed by a specific customer, use the relationship between CUSTOMER_MASTER and SALES_ORDER_HDR. The foreign key is SALES_ORDER_HDR.CUST_ID → CUSTOMER_MASTER.CUST_ID, and the business relationship states that a Sales Order is placed by exactly one Customer.

If you already know the customer’s CUST_ID, query SALES_ORDER_HDR and filter on CUST_ID. The order header table contains t…

**Sources retrieved (12):** `parent_chunk_data_dictionary.txt_3`, `parent_chunk_business_glossary.txt_2`, `parent_chunk_business_glossary.txt_0`, `Sales Order Header`, `Sales Order Header→SALES_ORDER_HDR`, `parent_chunk_data_dictionary.txt_4`, `SALES_ORDER_HDR→CUSTOMER_MASTER`, `parent_chunk_business_glossary.txt_1`

**Context previews (first 3):**

1. _# Data Dictionary - E-Commerce Database (Simplified)  This document describes the physical database schema for the simplified e-commerce test dataset.  ────────────────────────────────────────────────…_

2. _Sales Order Relationships: - A Sales Order is placed by exactly one Customer - A Sales Order has one or more Order Line Items - A Sales Order has one or more Payments - A Sales Order has one or more S…_

3. _# Business Glossary - E-Commerce Domain (Simplified)  This document defines the core business concepts for the e-commerce platform test dataset.  ──────────────────────────────────────────────────────…_

---

### ✅ Q009 — What products were included in a specific order?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0782 | **Gate:** `proceed_with_warning`

**Expected answer:**
> Join ORDER_LINE_ITEM with TB_PRODUCT on PRODUCT_ID. For order ORDER_ID, the line items show which products were ordered, in what quantity, and at what price.

**System answer:**
> The retrieved context does not contain actual order records, so I cannot tell which products were in a particular order instance. It contains schema-level metadata only.

From the schema, the products included in a specific order are stored in ORDER_LINE_ITEM, which represents the individual product lines within a sales order. To find them, use the order’s ORDER_ID and trace:

SALES_ORDER_HDR.ORDE…

**Sources retrieved (12):** `parent_chunk_data_dictionary.txt_4`, `parent_chunk_business_glossary.txt_1`, `ORDER_LINE_ITEM→TB_PRODUCT`, `parent_chunk_business_glossary.txt_0`, `parent_chunk_data_dictionary.txt_3`, `item→ORDER_LINE_ITEM`, `Sales Order Header`, `parent_chunk_business_glossary.txt_2`

**Context previews (first 3):**

1. _**Foreign Keys**: - CUST_ID → CUSTOMER_MASTER(CUST_ID) **Business Concept Mapping**: SalesOrder ──────────────────────────────────────────────────────────── ORDER_LINE_ITEM ───────────────────────────…_

2. _**Business Context**: Line items break down orders into individual product purchases. Each captures the price at the moment of ordering. **Key Attributes**: - Unique line identifier - References exact…_

3. _Relationship: ORDER_LINE_ITEM references TB_PRODUCT via foreign key PRODUCT_ID -> TB_PRODUCT.PRODUCT_ID.…_

---

### ✅ Q010 — Show me the order hierarchy from customer to line items.

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.3719 | **Gate:** `proceed`

**Expected answer:**
> The hierarchy is: Customer (CUSTOMER_MASTER) → SalesOrder (SALES_ORDER_HDR) → OrderLineItem (ORDER_LINE_ITEM) → Product (TB_PRODUCT). Each customer has orders, each order has line items, and each line item references a product.

**System answer:**
> The order hierarchy from customer to line items is:

Customer → Sales Order Header → Order Line Item

In the physical schema, that path is CUSTOMER_MASTER → SALES_ORDER_HDR → ORDER_LINE_ITEM.

The joins are:
CUSTOMER_MASTER.CUST_ID = SALES_ORDER_HDR.CUST_ID
SALES_ORDER_HDR.ORDER_ID = ORDER_LINE_ITEM.ORDER_ID

From the business relationships:
A Sales Order is placed by exactly one Customer.
A Sales…

**Sources retrieved (12):** `parent_chunk_business_glossary.txt_2`, `parent_chunk_data_dictionary.txt_4`, `Sales Order Header`, `Sales Order Header→SALES_ORDER_HDR`, `parent_chunk_business_glossary.txt_1`, `item→ORDER_LINE_ITEM`, `ORDER_LINE_ITEM→TB_PRODUCT`, `ORDER_LINE_ITEM→SALES_ORDER_HDR`

**Context previews (first 3):**

1. _Sales Order Relationships: - A Sales Order is placed by exactly one Customer - A Sales Order has one or more Order Line Items - A Sales Order has one or more Payments - A Sales Order has one or more S…_

2. _**Foreign Keys**: - CUST_ID → CUSTOMER_MASTER(CUST_ID) **Business Concept Mapping**: SalesOrder ──────────────────────────────────────────────────────────── ORDER_LINE_ITEM ───────────────────────────…_

3. _Sales Order Header: The table name, primary key, customer foreign key, order date, total amount, and status/delivery timestamps all align with a sales order header rather than line items or payments. …_

---

### ✅ Q011 — What happens when a payment is confirmed for an order?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.3521 | **Gate:** `proceed`

**Expected answer:**
> When payment is confirmed, the PAYMENT record's STATUS_CODE becomes 'CONFIRMED', the CONFIRMED_AT timestamp is set, and the associated SALES_ORDER_HDR can progress from PENDING to CONFIRMED status.

**System answer:**
> From the retrieved context, payment confirmation for an order is captured at the schema level, not described as a full business workflow.

A payment belongs to exactly one sales order, and a sales order has one or more payments. Physically, the PAYMENT table is linked to the order header through PAYMENT.ORDER_ID → SALES_ORDER_HDR.ORDER_ID.

When a payment is confirmed, the context shows these rele…

**Sources retrieved (12):** `parent_chunk_business_glossary.txt_1`, `Sales Order Header→SALES_ORDER_HDR`, `the customer, items, payment status, and delivery information→PAYMENT`, `PAYMENT→SALES_ORDER_HDR`, `parent_chunk_data_dictionary.txt_4`, `Sales Order Header`, `parent_chunk_business_glossary.txt_0`, `parent_chunk_business_glossary.txt_2`

**Context previews (first 3):**

1. _**Business Context**: Line items break down orders into individual product purchases. Each captures the price at the moment of ordering. **Key Attributes**: - Unique line identifier - References exact…_

2. _Business concept 'Sales Order Header' — The table name, primary key, customer foreign key, order date, total amount, and status/delivery timestamps all align with a sales order header rather than line…_

3. _Business concept 'the customer, items, payment status, and delivery information' is implemented by physical table PAYMENT (columns: PAYMENT_ID, ORDER_ID, PAYMENT_METHOD, AMOUNT, STATUS_CODE, CONFIRMED…_

---

### ✅ Q012 — How are shipments related to orders and warehouses?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.3848 | **Gate:** `proceed`

**Expected answer:**
> Each shipment is for exactly one sales order (ORDER_ID in SHIPMENT references SALES_ORDER_HDR). The shipment also specifies the source warehouse code and includes tracking information and delivery status.

**System answer:**
> A Shipment is related to orders by being for exactly one Sales Order. In the physical schema, the SHIPMENT table implements Shipment and contains ORDER_ID, and SHIPMENT.ORDER_ID references SALES_ORDER_HDR.ORDER_ID.

A Shipment is related to warehouses by coming from exactly one Warehouse. In the SHIPMENT table, this is represented by the WAREHOUSE_CODE column. The context does not provide a wareho…

**Sources retrieved (12):** `parent_chunk_business_glossary.txt_2`, `Shipment #S-001→SHIPMENT`, `parent_chunk_business_glossary.txt_0`, `parent_chunk_business_glossary.txt_1`, `the customer, items, payment status, and delivery information→PAYMENT`, `parent_chunk_data_dictionary.txt_4`, `Sales Order Header`, `Sales Order Header→SALES_ORDER_HDR`

**Context previews (first 3):**

1. _Sales Order Relationships: - A Sales Order is placed by exactly one Customer - A Sales Order has one or more Order Line Items - A Sales Order has one or more Payments - A Sales Order has one or more S…_

2. _Business concept 'Shipment #S-001' is implemented by physical table SHIPMENT (columns: SHIPMENT_ID, ORDER_ID, WAREHOUSE_CODE, SHIPPED_AT, TRACKING_NUMBER, STATUS_CODE).…_

3. _# Business Glossary - E-Commerce Domain (Simplified)  This document defines the core business concepts for the e-commerce platform test dataset.  ──────────────────────────────────────────────────────…_

---

### ✅ Q013 — Can a product belong to multiple categories?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.3613 | **Gate:** `proceed`

**Expected answer:**
> No, each product belongs to exactly one category. The TB_PRODUCT table has a CATEGORY_ID foreign key referencing TB_CATEGORY, which stores a single category value per product.

**System answer:**
> Based on the retrieved context, a product has one documented direct category assignment: `TB_PRODUCT.CATEGORY_ID` references `TB_CATEGORY.CATEGORY_ID`.

So, in the documented schema, each `TB_PRODUCT` row carries a single `CATEGORY_ID` value, which indicates one directly assigned category per product record.

The category structure itself is hierarchical, because `TB_CATEGORY.PARENT_CATEGORY_ID` r…

**Sources retrieved (12):** `parent_chunk_business_glossary.txt_0`, `TB_PRODUCT→TB_CATEGORY`, `Hierarchical product category tree→TB_PRODUCT`, `parent_chunk_business_glossary.txt_1`, `Hierarchical product category tree→TB_CATEGORY`, `parent_chunk_data_dictionary.txt_3`, `parent_chunk_data_dictionary.txt_4`, `ORDER_LINE_ITEM→TB_PRODUCT`

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
> Based on the retrieved context, no: a customer is not modeled as placing an order without payment.

The context states that a Sales Order is placed by exactly one Customer, and that a Sales Order has one or more Payments. In the schema, that is represented by CUSTOMER_MASTER.CUST_ID → SALES_ORDER_HDR.CUST_ID and PAYMENT.ORDER_ID → SALES_ORDER_HDR.ORDER_ID. So every order belongs to a customer and …

**Sources retrieved (12):** `parent_chunk_data_dictionary.txt_3`, `parent_chunk_business_glossary.txt_1`, `parent_chunk_business_glossary.txt_2`, `parent_chunk_business_glossary.txt_0`, `Sales Order Header`, `Sales Order Header→SALES_ORDER_HDR`, `parent_chunk_data_dictionary.txt_4`, `the customer, items, payment status, and delivery information→PAYMENT`

**Context previews (first 3):**

1. _# Data Dictionary - E-Commerce Database (Simplified)  This document describes the physical database schema for the simplified e-commerce test dataset.  ────────────────────────────────────────────────…_

2. _**Business Context**: Line items break down orders into individual product purchases. Each captures the price at the moment of ordering. **Key Attributes**: - Unique line identifier - References exact…_

3. _Sales Order Relationships: - A Sales Order is placed by exactly one Customer - A Sales Order has one or more Order Line Items - A Sales Order has one or more Payments - A Sales Order has one or more S…_

---

### ✅ Q015 — What is the total value of all orders placed by a customer?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0346 | **Gate:** `proceed_with_warning`

**Expected answer:**
> Sum the TOTAL_AMT column from SALES_ORDER_HDR for all records where CUST_ID matches the customer's ID. This aggregates the monetary value of all orders placed by that customer.

**System answer:**
> The retrieved context does not provide any customer-level order totals or operational records, so the actual total value of all orders placed by a specific customer cannot be determined from the knowledge graph.

What is known from the context is the schema needed to calculate it. The business concept “Sales Order Header” is implemented by SALES_ORDER_HDR, which contains ORDER_ID, CUST_ID, ORDER_D…

**Sources retrieved (12):** `Sales Order Header`, `parent_chunk_business_glossary.txt_1`, `Sales Order Header→SALES_ORDER_HDR`, `parent_chunk_business_glossary.txt_0`, `parent_chunk_data_dictionary.txt_3`, `parent_chunk_business_glossary.txt_2`, `parent_chunk_data_dictionary.txt_4`, `the customer, items, payment status, and delivery information→PAYMENT`

**Context previews (first 3):**

1. _Sales Order Header: The table name, primary key, customer foreign key, order date, total amount, and status/delivery timestamps all align with a sales order header rather than line items or payments. …_

2. _**Business Context**: Line items break down orders into individual product purchases. Each captures the price at the moment of ordering. **Key Attributes**: - Unique line identifier - References exact…_

3. _Business concept 'Sales Order Header' — The table name, primary key, customer foreign key, order date, total amount, and status/delivery timestamps all align with a sales order header rather than line…_

---

## Anomalies & Observations

No anomalies detected. All questions grounded with acceptable RAGAS scores.
