# AB-14 — 01_basics_ecommerce — Run Analysis

**Timestamp:** 2026-04-01 04:50:54  
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
| Triplets extracted | 243 |
| Entities resolved | 75 |
| Tables parsed | 7 |
| Tables completed | 7 |

## Query Evaluation Summary

| Metric | Value |
|--------|-------|
| Questions | 15 |
| Grounded | **15/15 (100%)** |
| Avg GT Coverage | 99% |
| Avg Top Score | 0.4063 |
| Avg Chunk Count | 12.0 |
| Abstained | 0 |

## RAGAS Metrics

RAGAS evaluation not enabled for this run.

## Per-Question Deep Dive

### ✅ Q001 — What information is stored for each customer?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.2979 | **Gate:** `proceed`

**Expected answer:**
> Each customer has a unique ID, full name, email address, geographic region code, creation date, and active status. The email must be unique across all customers.

**System answer:**
> For each customer, the physical table `CUSTOMER_MASTER` stores `CUST_ID` (unique customer identifier), `FULL_NAME` (customer’s full name), `EMAIL` (unique email address used for login), `REGION_CODE` (geographic region for tax), `CREATED_AT` (account creation timestamp), and `IS_ACTIVE` (whether the customer can place orders).

At the business-concept level, the `CUSTOMER` concept also includes a …

**Sources retrieved (12):** `Sales Order Header→SALES_ORDER_HDR`, `the customer, items, payment status, and delivery information→PAYMENT`, `parent_chunk_data_dictionary.txt_3`, `Master record for all registered platform customers→CUSTOMER_MASTER`, `parent_chunk_business_glossary.txt_0`, `parent_chunk_business_glossary.txt_1`, `SALES_ORDER_HDR→CUSTOMER_MASTER`, `parent_chunk_business_glossary.txt_2`

**Context previews (first 3):**

1. _Business concept 'Sales Order Header' — The table name and columns align strongly with an order header entity: it has order ID, customer reference, order date, total amount, status, and fulfillment/pa…_

2. _Business concept 'the customer, items, payment status, and delivery information' is implemented by physical table PAYMENT (columns: PAYMENT_ID, ORDER_ID, PAYMENT_METHOD, AMOUNT, STATUS_CODE, CONFIRMED…_

3. _# Data Dictionary - E-Commerce Database (Simplified)  This document describes the physical database schema for the simplified e-commerce test dataset.  ────────────────────────────────────────────────…_

---

### ✅ Q002 — How are products categorized on the platform?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.1590 | **Gate:** `proceed_with_warning`

**Expected answer:**
> Products belong to categories which can have a parent category, forming a hierarchical tree structure. Each product references exactly one category through its CATEGORY_ID.

**System answer:**
> Products are categorized through a category hierarchy.

In the schema, `TB_PRODUCT` is the product master catalogue, and each product has a `CATEGORY_ID`. That column is a foreign key to `TB_CATEGORY.CATEGORY_ID`, so each product is assigned to a category record in `TB_CATEGORY`.

The category structure is hierarchical: `TB_CATEGORY.PARENT_CATEGORY_ID` is a self-reference back to `TB_CATEGORY.CATE…

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
> The retrieved context explicitly states that a Sales Order is placed by exactly one Customer. In the physical schema, this is implemented by SALES_ORDER_HDR.CUST_ID referencing CUSTOMER_MASTER(CUST_ID).

So, the supported relationship is: each sales order links to one customer through SALES_ORDER_HDR.CUST_ID. The context also describes Customer and SalesOrder as related concepts and says customers…

**Sources retrieved (12):** `parent_chunk_business_glossary.txt_2`, `parent_chunk_business_glossary.txt_0`, `parent_chunk_business_glossary.txt_1`, `Sales Order Header→SALES_ORDER_HDR`, `parent_chunk_data_dictionary.txt_4`, `SALES_ORDER_HDR→CUSTOMER_MASTER`, `parent_chunk_data_dictionary.txt_3`, `the customer, items, payment status, and delivery information→PAYMENT`

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
> An order line item contains the details of an individual product purchase within a sales order. In the business context, it includes a unique line identifier, a reference to exactly one product, the quantity ordered, the unit price at the time of ordering, and the extended amount calculated as quantity × unit price.

In the schema, this is implemented by the ORDER_LINE_ITEM table with columns LINE…

**Sources retrieved (12):** `parent_chunk_business_glossary.txt_1`, `ORDER_LINE_ITEM→TB_PRODUCT`, `item→ORDER_LINE_ITEM`, `ORDER_LINE_ITEM→SALES_ORDER_HDR`, `parent_chunk_business_glossary.txt_2`, `parent_chunk_data_dictionary.txt_4`, `Sales Order Header→SALES_ORDER_HDR`, `parent_chunk_business_glossary.txt_0`

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
> Payments are linked to orders through the `ORDER_ID` foreign key.

The physical relationship is `PAYMENT.ORDER_ID -> SALES_ORDER_HDR.ORDER_ID`, meaning each row in `PAYMENT` references one row in `SALES_ORDER_HDR`. The context also states the business rule that a Payment is for exactly one Sales Order, and a Sales Order has one or more Payments.

So, to connect payments to orders in the schema, jo…

**Sources retrieved (12):** `PAYMENT→SALES_ORDER_HDR`, `parent_chunk_business_glossary.txt_1`, `parent_chunk_business_glossary.txt_2`, `parent_chunk_data_dictionary.txt_4`, `SHIPMENT→SALES_ORDER_HDR`, `ORDER_LINE_ITEM→SALES_ORDER_HDR`, `SALES_ORDER_HDR→CUSTOMER_MASTER`, `parent_chunk_business_glossary.txt_0`

**Context previews (first 3):**

1. _Relationship: PAYMENT references SALES_ORDER_HDR via foreign key ORDER_ID -> SALES_ORDER_HDR.ORDER_ID.…_

2. _**Business Context**: Line items break down orders into individual product purchases. Each captures the price at the moment of ordering. **Key Attributes**: - Unique line identifier - References exact…_

3. _Sales Order Relationships: - A Sales Order is placed by exactly one Customer - A Sales Order has one or more Order Line Items - A Sales Order has one or more Payments - A Sales Order has one or more S…_

---

### ✅ Q006 — What statuses can an order have?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.3528 | **Gate:** `proceed`

**Expected answer:**
> Orders can have one of five statuses defined via CHECK constraint on SALES_ORDER_HDR.STATUS_CODE: PENDING (initial state when order is created), CONFIRMED (payment has been received), SHIPPED (dispatched to customer), DELIVERED (received by customer), or CANCELLED. The business glossary describes th…

**System answer:**
> The retrieved context shows that an order’s status is stored in SALES_ORDER_HDR.STATUS_CODE for the business concept Sales Order Header. However, it does not list or define the possible order status values.

Related status fields also exist in PAYMENT.STATUS_CODE and SHIPMENT.STATUS_CODE, but those are payment and shipment statuses, not the order status values themselves.

**Sources retrieved (12):** `Sales Order Header→SALES_ORDER_HDR`, `parent_chunk_business_glossary.txt_0`, `parent_chunk_business_glossary.txt_1`, `the customer, items, payment status, and delivery information→PAYMENT`, `Shipment→SHIPMENT`, `parent_chunk_business_glossary.txt_2`, `parent_chunk_data_dictionary.txt_4`, `parent_chunk_data_dictionary.txt_3`

**Context previews (first 3):**

1. _Business concept 'Sales Order Header' — The table name and columns align strongly with an order header entity: it has order ID, customer reference, order date, total amount, status, and fulfillment/pa…_

2. _# Business Glossary - E-Commerce Domain (Simplified)  This document defines the core business concepts for the e-commerce platform test dataset.  ──────────────────────────────────────────────────────…_

3. _**Business Context**: Line items break down orders into individual product purchases. Each captures the price at the moment of ordering. **Key Attributes**: - Unique line identifier - References exact…_

---

### ✅ Q007 — Which table stores the product SKU information?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.5995 | **Gate:** `proceed`

**Expected answer:**
> The TB_PRODUCT table stores the SKU (Stock Keeping Unit) code for each product, along with product name, category, price, and active status.

**System answer:**
> The product SKU is stored in TB_PRODUCT, in the column SKU.

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
> Use the relationship between CUSTOMER_MASTER and SALES_ORDER_HDR.

The retrieved context states that a Sales Order is placed by exactly one Customer, and SALES_ORDER_HDR references CUSTOMER_MASTER through the foreign key SALES_ORDER_HDR.CUST_ID → CUSTOMER_MASTER.CUST_ID.

So the schema-level path is:

CUSTOMER_MASTER.CUST_ID = SALES_ORDER_HDR.CUST_ID

To find all orders placed by a specific custom…

**Sources retrieved (12):** `parent_chunk_data_dictionary.txt_3`, `parent_chunk_business_glossary.txt_2`, `Sales Order Header→SALES_ORDER_HDR`, `parent_chunk_business_glossary.txt_0`, `parent_chunk_data_dictionary.txt_4`, `SALES_ORDER_HDR→CUSTOMER_MASTER`, `parent_chunk_business_glossary.txt_1`, `the customer, items, payment status, and delivery information→PAYMENT`

**Context previews (first 3):**

1. _# Data Dictionary - E-Commerce Database (Simplified)  This document describes the physical database schema for the simplified e-commerce test dataset.  ────────────────────────────────────────────────…_

2. _Sales Order Relationships: - A Sales Order is placed by exactly one Customer - A Sales Order has one or more Order Line Items - A Sales Order has one or more Payments - A Sales Order has one or more S…_

3. _Business concept 'Sales Order Header' — The table name and columns align strongly with an order header entity: it has order ID, customer reference, order date, total amount, status, and fulfillment/pa…_

---

### ✅ Q009 — What products were included in a specific order?

**Status:** GROUNDED  
**GT Coverage:** 83% | **Top Score:** 0.0782 | **Gate:** `proceed_with_warning`

**Expected answer:**
> Join ORDER_LINE_ITEM with TB_PRODUCT on PRODUCT_ID. For order ORDER_ID, the line items show which products were ordered, in what quantity, and at what price.

**System answer:**
> The retrieved context does not contain actual order records, so I cannot tell which products were included in a specific order. It contains schema-level metadata only.

From the schema, the products in an order are determined through ORDER_LINE_ITEM. A Sales Order has one or more Order Line Items, and each Order Line Item references exactly one Product. The join path is SALES_ORDER_HDR.ORDER_ID = …

**Sources retrieved (12):** `parent_chunk_data_dictionary.txt_4`, `parent_chunk_business_glossary.txt_1`, `ORDER_LINE_ITEM→TB_PRODUCT`, `parent_chunk_business_glossary.txt_0`, `parent_chunk_data_dictionary.txt_3`, `item→ORDER_LINE_ITEM`, `parent_chunk_business_glossary.txt_2`, `parent_chunk_data_dictionary.txt_5`

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
> The order hierarchy in the schema is Customer → Sales Order → Order Line Item.

At the table level, Customer is implemented by CUSTOMER_MASTER, with primary key CUST_ID. A Sales Order is implemented by SALES_ORDER_HDR, and SALES_ORDER_HDR.CUST_ID is a foreign key to CUSTOMER_MASTER.CUST_ID. The business rule says a Sales Order is placed by exactly one Customer, and a customer can therefore be trac…

**Sources retrieved (12):** `parent_chunk_business_glossary.txt_2`, `parent_chunk_data_dictionary.txt_4`, `parent_chunk_business_glossary.txt_1`, `item→ORDER_LINE_ITEM`, `ORDER_LINE_ITEM→TB_PRODUCT`, `ORDER_LINE_ITEM→SALES_ORDER_HDR`, `parent_chunk_business_glossary.txt_0`, `parent_chunk_data_dictionary.txt_3`

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
> From the retrieved context, a confirmed payment is represented at the schema level, not as a described business workflow.

A payment belongs to exactly one sales order through PAYMENT.ORDER_ID → SALES_ORDER_HDR.ORDER_ID, and a sales order has one or more payments. When a payment is confirmed, the PAYMENT table records that event with its STATUS_CODE and CONFIRMED_AT columns. At the order-header le…

**Sources retrieved (12):** `parent_chunk_business_glossary.txt_1`, `Sales Order Header→SALES_ORDER_HDR`, `the customer, items, payment status, and delivery information→PAYMENT`, `PAYMENT→SALES_ORDER_HDR`, `parent_chunk_data_dictionary.txt_4`, `parent_chunk_business_glossary.txt_0`, `parent_chunk_business_glossary.txt_2`, `parent_chunk_data_dictionary.txt_3`

**Context previews (first 3):**

1. _**Business Context**: Line items break down orders into individual product purchases. Each captures the price at the moment of ordering. **Key Attributes**: - Unique line identifier - References exact…_

2. _Business concept 'Sales Order Header' — The table name and columns align strongly with an order header entity: it has order ID, customer reference, order date, total amount, status, and fulfillment/pa…_

3. _Business concept 'the customer, items, payment status, and delivery information' is implemented by physical table PAYMENT (columns: PAYMENT_ID, ORDER_ID, PAYMENT_METHOD, AMOUNT, STATUS_CODE, CONFIRMED…_

---

### ✅ Q012 — How are shipments related to orders and warehouses?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.4940 | **Gate:** `proceed`

**Expected answer:**
> Each shipment is for exactly one sales order (ORDER_ID in SHIPMENT references SALES_ORDER_HDR). The shipment also specifies the source warehouse code and includes tracking information and delivery status.

**System answer:**
> A Shipment is related to orders and warehouses through the SHIPMENT table. The business concept “Shipment” is implemented by SHIPMENT with columns SHIPMENT_ID, ORDER_ID, WAREHOUSE_CODE, SHIPPED_AT, TRACKING_NUMBER, and STATUS_CODE.

For orders, the relationship is explicit: a Shipment is for exactly one Sales Order, and SALES_ORDER_HDR.ORDER_ID is the parent key for SHIPMENT.ORDER_ID. The context …

**Sources retrieved (12):** `Shipment→SHIPMENT`, `parent_chunk_business_glossary.txt_2`, `parent_chunk_business_glossary.txt_0`, `parent_chunk_business_glossary.txt_1`, `the customer, items, payment status, and delivery information→PAYMENT`, `parent_chunk_data_dictionary.txt_4`, `Sales Order Header→SALES_ORDER_HDR`, `parent_chunk_data_dictionary.txt_3`

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
> Based on the retrieved context, a product appears to belong to only one category.

The schema shows that TB_PRODUCT has a single column, CATEGORY_ID, and TB_PRODUCT references TB_CATEGORY through the foreign key CATEGORY_ID → TB_CATEGORY.CATEGORY_ID. There is no junction table or multiple-category relationship shown for products. The category hierarchy itself is handled within TB_CATEGORY through …

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
> No. In the retrieved context, a Sales Order is placed by exactly one Customer, and a Sales Order has one or more Payments. At the schema/relationship level, this is modeled as CUSTOMER_MASTER.CUST_ID → SALES_ORDER_HDR.CUST_ID and SALES_ORDER_HDR.ORDER_ID → PAYMENT.ORDER_ID.

So the data model/business rules shown do not allow a sales order with zero payments. The context does not say whether payme…

**Sources retrieved (12):** `parent_chunk_data_dictionary.txt_3`, `parent_chunk_business_glossary.txt_1`, `parent_chunk_business_glossary.txt_2`, `parent_chunk_business_glossary.txt_0`, `parent_chunk_data_dictionary.txt_4`, `the customer, items, payment status, and delivery information→PAYMENT`, `Sales Order Header→SALES_ORDER_HDR`, `PAYMENT→SALES_ORDER_HDR`

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
> The retrieved context does not provide any actual customer or order records, so the total value of all orders placed by a customer cannot be determined as a number from this knowledge graph.

What is known from the context is the schema-level method. The customer is stored in CUSTOMER_MASTER with key CUST_ID. Sales orders are stored in SALES_ORDER_HDR, which includes CUST_ID and TOTAL_AMT. Since C…

**Sources retrieved (12):** `parent_chunk_business_glossary.txt_1`, `parent_chunk_business_glossary.txt_0`, `Sales Order Header→SALES_ORDER_HDR`, `parent_chunk_data_dictionary.txt_3`, `parent_chunk_business_glossary.txt_2`, `parent_chunk_data_dictionary.txt_4`, `the customer, items, payment status, and delivery information→PAYMENT`, `Master record for all registered platform customers→CUSTOMER_MASTER`

**Context previews (first 3):**

1. _**Business Context**: Line items break down orders into individual product purchases. Each captures the price at the moment of ordering. **Key Attributes**: - Unique line identifier - References exact…_

2. _# Business Glossary - E-Commerce Domain (Simplified)  This document defines the core business concepts for the e-commerce platform test dataset.  ──────────────────────────────────────────────────────…_

3. _Business concept 'Sales Order Header' — The table name and columns align strongly with an order header entity: it has order ID, customer reference, order date, total amount, status, and fulfillment/pa…_

---

## Anomalies & Observations

No anomalies detected. All questions grounded with acceptable RAGAS scores.
