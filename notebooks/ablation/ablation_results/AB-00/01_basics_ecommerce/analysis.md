# AB-00 — 01_basics_ecommerce — Run Analysis

**Timestamp:** 2026-03-27 17:29:19  
**Run tag:** `post-fix-v3`

## Configuration

| Parameter | Value |
|-----------|-------|
| Extraction model | `LLM (gpt-5.4-nano-2026-03-17)` |
| Reasoning model | `gpt-5.4-nano-2026-03-17` |
| Embedding model | `BAAI/bge-m3` |
| Retrieval mode | `hybrid` |
| Reranker | `True` |
| Reranker top_k | `12` |
| Chunk size / overlap | `256 / 32` |
| ER similarity threshold | `0.75` |

## Builder Results

| Metric | Value |
|--------|-------|
| Triplets extracted | 233 |
| Entities resolved | 76 |
| Tables parsed | 7 |
| Tables completed | 7 |

## Query Evaluation Summary

| Metric | Value |
|--------|-------|
| Questions | 15 |
| Grounded | **15/15 (100%)** |
| Avg GT Coverage | 96% |
| Avg Top Score | 0.4775 |
| Avg Chunk Count | 12.0 |
| Abstained | 0 |

## RAGAS Metrics

RAGAS evaluation not enabled for this run.

## Per-Question Deep Dive

### ✅ Q001 — What information is stored for each customer?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.6060 | **Gate:** `proceed`

**Expected answer:**
> Each customer has a unique ID, full name, email address, geographic region code, creation date, and active status. The email must be unique across all customers.

**System answer:**
> For each customer, the **Customer Master Record** stored in the physical table **CUSTOMER_MASTER** includes core identifying attributes and lifecycle/eligibility fields: **CUST_ID**, **FULL_NAME**, **EMAIL** (unique login email), **REGION_CODE** (geographic region for tax), **CREATED_AT** (account creation timestamp), and **IS_ACTIVE** (whether the customer can place orders).  

The knowledge grap…

**Sources retrieved (12):** `Customer Master Record→CUSTOMER_MASTER`, `Header record for each customer sales order→SALES_ORDER_HDR`, `parent_chunk_data_dictionary.txt_3`, `parent_chunk_business_glossary.txt_0`, `Order Fulfillment Shipment→SHIPMENT`, `Product Catalogue→TB_PRODUCT`, `parent_chunk_business_glossary.txt_1`, `Customer Master Record`

**Context previews (first 3):**

1. _Business concept 'Customer Master Record' — The table stores core identifying attributes for registered customers (CUST_ID, FULL_NAME, unique EMAIL) along with customer lifecycle fields (CREATED_AT) a…_

2. _Business concept 'Header record for each customer sales order' is implemented by physical table SALES_ORDER_HDR (columns: ORDER_ID, CUST_ID, ORDER_DATE, TOTAL_AMT, STATUS_CODE, PAYMENT_CONFIRMED_AT, D…_

3. _# Data Dictionary - E-Commerce Database (Simplified)  This document describes the physical database schema for the simplified e-commerce test dataset.  ────────────────────────────────────────────────…_

---

### ✅ Q002 — How are products categorized on the platform?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.1590 | **Gate:** `proceed_with_warning`

**Expected answer:**
> Products belong to categories which can have a parent category, forming a hierarchical tree structure. Each product references exactly one category through its CATEGORY_ID.

**System answer:**
> Products are categorized using the hierarchical product category tree implemented by the physical table `TB_CATEGORY`. The product catalogue table `TB_PRODUCT` stores each product’s `CATEGORY_ID`, which references `TB_CATEGORY.CATEGORY_ID`, so each product belongs to a category (and categories can form a hierarchy via `TB_CATEGORY.PARENT_CATEGORY_ID`).

**Sources retrieved (12):** `parent_chunk_business_glossary.txt_0`, `parent_chunk_data_dictionary.txt_3`, `parent_chunk_business_glossary.txt_1`, `Product Catalogue→TB_PRODUCT`, `Customer Master Record→CUSTOMER_MASTER`, `Order Payment→PAYMENT`, `Product Catalogue`, `parent_chunk_data_dictionary.txt_5`

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
> In the e-commerce schema, a Sales Order is placed by exactly one Customer. This is implemented by the foreign key relationship where `SALES_ORDER_HDR` references `CUSTOMER_MASTER` via `CUST_ID -> CUSTOMER_MASTER.CUST_ID` (i.e., each row in `SALES_ORDER_HDR` is tied to exactly one customer in `CUSTOMER_MASTER`).

**Sources retrieved (12):** `parent_chunk_business_glossary.txt_2`, `parent_chunk_business_glossary.txt_0`, `parent_chunk_business_glossary.txt_1`, `Order Payment`, `Order Payment→PAYMENT`, `parent_chunk_data_dictionary.txt_4`, `Header record for each customer sales order→SALES_ORDER_HDR`, `Order Fulfillment Shipment→SHIPMENT`

**Context previews (first 3):**

1. _Sales Order Relationships: - A Sales Order is placed by exactly one Customer - A Sales Order has one or more Order Line Items - A Sales Order has one or more Payments - A Sales Order has one or more S…_

2. _# Business Glossary - E-Commerce Domain (Simplified)  This document defines the core business concepts for the e-commerce platform test dataset.  ──────────────────────────────────────────────────────…_

3. _**Business Context**: Line items break down orders into individual product purchases. Each captures the price at the moment of ordering. **Key Attributes**: - Unique line identifier - References exact…_

---

### ✅ Q004 — What does an order line item contain?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.9729 | **Gate:** `proceed`

**Expected answer:**
> An order line item specifies a product, the quantity ordered, the unit price at time of purchase, and the calculated extended amount. Each line item belongs to exactly one sales order.

**System answer:**
> An order line item contains the individual product purchase details within a sales order. In the schema for the physical table `ORDER_LINE_ITEM`, it stores `PRODUCT_ID` (the product ordered), `QUANTITY` (number of units ordered), `UNIT_PRICE` (the unit price at the moment the order was placed, fixed and historical), and `LINE_AMT` (the extended amount, calculated as quantity × unit price). It also…

**Sources retrieved (12):** `Order Line Item→ORDER_LINE_ITEM`, `parent_chunk_business_glossary.txt_1`, `ORDER_LINE_ITEM→TB_PRODUCT`, `ORDER_LINE_ITEM→SALES_ORDER_HDR`, `parent_chunk_business_glossary.txt_2`, `parent_chunk_data_dictionary.txt_4`, `Order Fulfillment Shipment→SHIPMENT`, `Order Payment`

**Context previews (first 3):**

1. _Business concept 'Order Line Item' — The table name and structure (ORDER_ID, PRODUCT_ID) indicate it stores individual product lines within a sales order. The presence of QUANTITY, UNIT_PRICE, and LIN…_

2. _**Business Context**: Line items break down orders into individual product purchases. Each captures the price at the moment of ordering. **Key Attributes**: - Unique line identifier - References exact…_

3. _Relationship: ORDER_LINE_ITEM references TB_PRODUCT via foreign key PRODUCT_ID -> TB_PRODUCT.PRODUCT_ID.…_

---

### ✅ Q005 — How are payments linked to orders?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.9768 | **Gate:** `proceed`

**Expected answer:**
> Each payment is associated with exactly one sales order through the ORDER_ID foreign key. Payments track the payment method, amount, status, and confirmation timestamp.

**System answer:**
> Payments are linked to orders through the `PAYMENT` table’s foreign key `ORDER_ID`, which references `SALES_ORDER_HDR.ORDER_ID` (i.e., each payment is for a specific sales order).

**Sources retrieved (12):** `Order Payment`, `PAYMENT→SALES_ORDER_HDR`, `Order Payment→PAYMENT`, `parent_chunk_business_glossary.txt_1`, `parent_chunk_business_glossary.txt_2`, `parent_chunk_data_dictionary.txt_4`, `SHIPMENT→SALES_ORDER_HDR`, `ORDER_LINE_ITEM→SALES_ORDER_HDR`

**Context previews (first 3):**

1. _Order Payment: The table represents discrete payment transactions linked to a specific sales order via ORDER_ID (foreign key to SALES_ORDER_HDR), with payment method, amount, and status/confirmation t…_

2. _Relationship: PAYMENT references SALES_ORDER_HDR via foreign key ORDER_ID -> SALES_ORDER_HDR.ORDER_ID.…_

3. _Business concept 'Order Payment' — The table represents discrete payment transactions linked to a specific sales order via ORDER_ID (foreign key to SALES_ORDER_HDR), with payment method, amount, and s…_

---

### ✅ Q006 — What statuses can an order have?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.2891 | **Gate:** `proceed`

**Expected answer:**
> Orders can have one of five statuses defined via CHECK constraint on SALES_ORDER_HDR.STATUS_CODE: PENDING (initial state when order is created), CONFIRMED (payment has been received), SHIPPED (dispatched to customer), DELIVERED (received by customer), or CANCELLED. The business glossary describes th…

**System answer:**
> The retrieved context only shows that a sales order has a `STATUS_CODE` column in `SALES_ORDER_HDR` (table “Header record for each customer sales order”). However, it does not provide the possible status code values/enumerations, so I cannot list what specific order statuses are allowed based on this context.

**Sources retrieved (12):** `Order Fulfillment Shipment→SHIPMENT`, `parent_chunk_business_glossary.txt_0`, `parent_chunk_business_glossary.txt_1`, `Order Payment`, `Header record for each customer sales order→SALES_ORDER_HDR`, `Order Payment→PAYMENT`, `parent_chunk_business_glossary.txt_2`, `parent_chunk_data_dictionary.txt_4`

**Context previews (first 3):**

1. _Business concept 'Order Fulfillment Shipment' — The SHIPMENT table is a header-level logistics record tied to a specific sales order (ORDER_ID) and captures when it was shipped (SHIPPED_AT), shipment …_

2. _# Business Glossary - E-Commerce Domain (Simplified)  This document defines the core business concepts for the e-commerce platform test dataset.  ──────────────────────────────────────────────────────…_

3. _**Business Context**: Line items break down orders into individual product purchases. Each captures the price at the moment of ordering. **Key Attributes**: - Unique line identifier - References exact…_

---

### ✅ Q007 — Which table stores the product SKU information?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.8246 | **Gate:** `proceed`

**Expected answer:**
> The TB_PRODUCT table stores the SKU (Stock Keeping Unit) code for each product, along with product name, category, price, and active status.

**System answer:**
> The table that stores product SKU information is `TB_PRODUCT` (from the business concept “Product Catalogue”, which includes the column `SKU`).

**Sources retrieved (12):** `Product Catalogue→TB_PRODUCT`, `Order Line Item→ORDER_LINE_ITEM`, `parent_chunk_data_dictionary.txt_3`, `Customer Master Record→CUSTOMER_MASTER`, `ORDER_LINE_ITEM→TB_PRODUCT`, `Hierarchical product category tree→TB_CATEGORY`, `Product Catalogue`, `Order Line Item`

**Context previews (first 3):**

1. _Business concept 'Product Catalogue' — TB_PRODUCT stores master data for sellable items, including a unique SKU, human-readable product name, category reference (CATEGORY_ID), unit price, and an activ…_

2. _Business concept 'Order Line Item' — The table name and structure (ORDER_ID, PRODUCT_ID) indicate it stores individual product lines within a sales order. The presence of QUANTITY, UNIT_PRICE, and LIN…_

3. _# Data Dictionary - E-Commerce Database (Simplified)  This document describes the physical database schema for the simplified e-commerce test dataset.  ────────────────────────────────────────────────…_

---

### ✅ Q008 — How can I find all orders placed by a specific customer?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.1428 | **Gate:** `proceed_with_warning`

**Expected answer:**
> Query the SALES_ORDER_HDR table filtering by CUST_ID. Each order has a foreign key reference to CUSTOMER_MASTER.CUST_ID, so joining these tables on CUST_ID will show all orders for a customer along with their details.

**System answer:**
> To find all orders placed by a specific customer, use the foreign-key relationship between the customer master table and the sales order header table.

First, identify the customer in `CUSTOMER_MASTER` by `CUST_ID` (or by `FULL_NAME` / `EMAIL`, since those columns exist in `CUSTOMER_MASTER`). Then retrieve their orders from `SALES_ORDER_HDR` by joining on `CUSTOMER_MASTER.CUST_ID = SALES_ORDER_HDR…

**Sources retrieved (12):** `parent_chunk_data_dictionary.txt_3`, `parent_chunk_business_glossary.txt_2`, `Order Fulfillment Shipment→SHIPMENT`, `Order Payment`, `parent_chunk_business_glossary.txt_0`, `Header record for each customer sales order→SALES_ORDER_HDR`, `parent_chunk_data_dictionary.txt_4`, `Order Payment→PAYMENT`

**Context previews (first 3):**

1. _# Data Dictionary - E-Commerce Database (Simplified)  This document describes the physical database schema for the simplified e-commerce test dataset.  ────────────────────────────────────────────────…_

2. _Sales Order Relationships: - A Sales Order is placed by exactly one Customer - A Sales Order has one or more Order Line Items - A Sales Order has one or more Payments - A Sales Order has one or more S…_

3. _Business concept 'Order Fulfillment Shipment' — The SHIPMENT table is a header-level logistics record tied to a specific sales order (ORDER_ID) and captures when it was shipped (SHIPPED_AT), shipment …_

---

### ✅ Q009 — What products were included in a specific order?

**Status:** GROUNDED  
**GT Coverage:** 67% | **Top Score:** 0.1178 | **Gate:** `proceed_with_warning`

**Expected answer:**
> Join ORDER_LINE_ITEM with TB_PRODUCT on PRODUCT_ID. For order ORDER_ID, the line items show which products were ordered, in what quantity, and at what price.

**System answer:**
> To determine what products were included in a specific order, use the business concept “Order Line Item” implemented by the physical table `ORDER_LINE_ITEM`. For a given `ORDER_ID`, the products in that order are identified by `ORDER_LINE_ITEM.PRODUCT_ID` (each row represents one product line within the sales order). The same `ORDER_LINE_ITEM` rows also provide `QUANTITY`, `UNIT_PRICE` (historical…

**Sources retrieved (12):** `Order Fulfillment Shipment→SHIPMENT`, `parent_chunk_data_dictionary.txt_4`, `parent_chunk_business_glossary.txt_1`, `Order Payment`, `ORDER_LINE_ITEM→TB_PRODUCT`, `Order Payment→PAYMENT`, `parent_chunk_business_glossary.txt_0`, `Order Line Item→ORDER_LINE_ITEM`

**Context previews (first 3):**

1. _Business concept 'Order Fulfillment Shipment' — The SHIPMENT table is a header-level logistics record tied to a specific sales order (ORDER_ID) and captures when it was shipped (SHIPPED_AT), shipment …_

2. _**Foreign Keys**: - CUST_ID → CUSTOMER_MASTER(CUST_ID) **Business Concept Mapping**: SalesOrder ──────────────────────────────────────────────────────────── ORDER_LINE_ITEM ───────────────────────────…_

3. _**Business Context**: Line items break down orders into individual product purchases. Each captures the price at the moment of ordering. **Key Attributes**: - Unique line identifier - References exact…_

---

### ✅ Q010 — Show me the order hierarchy from customer to line items.

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.3719 | **Gate:** `proceed`

**Expected answer:**
> The hierarchy is: Customer (CUSTOMER_MASTER) → SalesOrder (SALES_ORDER_HDR) → OrderLineItem (ORDER_LINE_ITEM) → Product (TB_PRODUCT). Each customer has orders, each order has line items, and each line item references a product.

**System answer:**
> From the retrieved context, the order hierarchy is: a Customer has Sales Orders, where each Sales Order is placed by exactly one Customer, and each Sales Order contains one or more Order Line Items. At the line level, an Order Line Item is part of exactly one Sales Order.

In terms of the mapped tables/business concepts: Customer is implemented by `CUSTOMER_MASTER`, Sales Order by `SALES_ORDER_HDR…

**Sources retrieved (12):** `parent_chunk_business_glossary.txt_2`, `parent_chunk_data_dictionary.txt_4`, `parent_chunk_business_glossary.txt_1`, `Order Line Item→ORDER_LINE_ITEM`, `ORDER_LINE_ITEM→TB_PRODUCT`, `ORDER_LINE_ITEM→SALES_ORDER_HDR`, `Header record for each customer sales order→SALES_ORDER_HDR`, `parent_chunk_business_glossary.txt_0`

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
> In this schema, confirming a payment means that the payment transaction’s confirmation timestamp and status are recorded. The payment is stored in the `PAYMENT` table, which includes `STATUS_CODE` and `CONFIRMED_AT` (along with `PAYMENT_ID`, `ORDER_ID`, `PAYMENT_METHOD`, and `AMOUNT`). The `PAYMENT.ORDER_ID` is a foreign key to the order header in `SALES_ORDER_HDR`.

At the order level, the corres…

**Sources retrieved (12):** `parent_chunk_business_glossary.txt_1`, `Order Payment`, `Order Payment→PAYMENT`, `Header record for each customer sales order→SALES_ORDER_HDR`, `PAYMENT→SALES_ORDER_HDR`, `parent_chunk_data_dictionary.txt_4`, `parent_chunk_business_glossary.txt_0`, `parent_chunk_business_glossary.txt_2`

**Context previews (first 3):**

1. _**Business Context**: Line items break down orders into individual product purchases. Each captures the price at the moment of ordering. **Key Attributes**: - Unique line identifier - References exact…_

2. _Order Payment: The table represents discrete payment transactions linked to a specific sales order via ORDER_ID (foreign key to SALES_ORDER_HDR), with payment method, amount, and status/confirmation t…_

3. _Business concept 'Order Payment' — The table represents discrete payment transactions linked to a specific sales order via ORDER_ID (foreign key to SALES_ORDER_HDR), with payment method, amount, and s…_

---

### ✅ Q012 — How are shipments related to orders and warehouses?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.8998 | **Gate:** `proceed`

**Expected answer:**
> Each shipment is for exactly one sales order (ORDER_ID in SHIPMENT references SALES_ORDER_HDR). The shipment also specifies the source warehouse code and includes tracking information and delivery status.

**System answer:**
> Shipments are related to orders via the `SHIPMENT` table’s `ORDER_ID`, which is a foreign key to `SALES_ORDER_HDR.ORDER_ID` (so each shipment is for exactly one sales order). Shipments are related to warehouses via `SHIPMENT.WAREHOUSE_CODE`, and the business rules state that each shipment comes from exactly one warehouse.

**Sources retrieved (12):** `Order Fulfillment Shipment→SHIPMENT`, `parent_chunk_business_glossary.txt_2`, `parent_chunk_business_glossary.txt_0`, `parent_chunk_business_glossary.txt_1`, `Order Payment→PAYMENT`, `parent_chunk_data_dictionary.txt_4`, `Order Payment`, `parent_chunk_data_dictionary.txt_3`

**Context previews (first 3):**

1. _Business concept 'Order Fulfillment Shipment' — The SHIPMENT table is a header-level logistics record tied to a specific sales order (ORDER_ID) and captures when it was shipped (SHIPPED_AT), shipment …_

2. _Sales Order Relationships: - A Sales Order is placed by exactly one Customer - A Sales Order has one or more Order Line Items - A Sales Order has one or more Payments - A Sales Order has one or more S…_

3. _# Business Glossary - E-Commerce Domain (Simplified)  This document defines the core business concepts for the e-commerce platform test dataset.  ──────────────────────────────────────────────────────…_

---

### ✅ Q013 — Can a product belong to multiple categories?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.3613 | **Gate:** `proceed`

**Expected answer:**
> No, each product belongs to exactly one category. The TB_PRODUCT table has a CATEGORY_ID foreign key referencing TB_CATEGORY, which stores a single category value per product.

**System answer:**
> Based on the schema in the retrieved context, a product belongs to only one category in the current model. `TB_PRODUCT` stores a single `CATEGORY_ID` column (a foreign key to `TB_CATEGORY.CATEGORY_ID`), so there is no indication that a single `TB_PRODUCT` record can reference multiple categories.

**Sources retrieved (12):** `parent_chunk_business_glossary.txt_0`, `TB_PRODUCT→TB_CATEGORY`, `parent_chunk_business_glossary.txt_1`, `Hierarchical product category tree→TB_CATEGORY`, `Product Catalogue→TB_PRODUCT`, `parent_chunk_data_dictionary.txt_3`, `parent_chunk_data_dictionary.txt_4`, `ORDER_LINE_ITEM→TB_PRODUCT`

**Context previews (first 3):**

1. _# Business Glossary - E-Commerce Domain (Simplified)  This document defines the core business concepts for the e-commerce platform test dataset.  ──────────────────────────────────────────────────────…_

2. _Relationship: TB_PRODUCT references TB_CATEGORY via foreign key CATEGORY_ID -> TB_CATEGORY.CATEGORY_ID.…_

3. _**Business Context**: Line items break down orders into individual product purchases. Each captures the price at the moment of ordering. **Key Attributes**: - Unique line identifier - References exact…_

---

### ✅ Q014 — Is it possible for a customer to place an order without payment?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0719 | **Gate:** `proceed_with_warning`

**Expected answer:**
> Yes, an order can exist without payment. SALES_ORDER_HDR has STATUS_CODE defaulting to PENDING and PAYMENT_CONFIRMED_AT is nullable (NULL when no payment yet). The PAYMENT table links via ORDER_ID foreign key but nothing prevents an order from existing without a payment row. However, the business gl…

**System answer:**
> Based on the business relationships in the retrieved context, a Sales Order must have one or more Payments. Specifically, the context states: “A Sales Order has one or more Payments” (Sales Order Relationships). Therefore, in this modeled dataset, it is not possible for a customer to place a Sales Order without having at least one payment record associated with that order.

**Sources retrieved (12):** `parent_chunk_data_dictionary.txt_3`, `parent_chunk_business_glossary.txt_1`, `parent_chunk_business_glossary.txt_2`, `Order Payment`, `Order Payment→PAYMENT`, `parent_chunk_business_glossary.txt_0`, `parent_chunk_data_dictionary.txt_4`, `Header record for each customer sales order→SALES_ORDER_HDR`

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
> In the provided schema, each sales order is represented by a row in **`SALES_ORDER_HDR`**, which includes a **`TOTAL_AMT`** column (the order’s total value) and a **`CUST_ID`** column that is linked to **`CUSTOMER_MASTER(CUST_ID)`**. 

However, the retrieved context does not explicitly define the business rule or method for computing “the total value of all orders placed by a customer” across mult…

**Sources retrieved (12):** `parent_chunk_business_glossary.txt_1`, `parent_chunk_business_glossary.txt_0`, `parent_chunk_data_dictionary.txt_3`, `parent_chunk_business_glossary.txt_2`, `parent_chunk_data_dictionary.txt_4`, `Header record for each customer sales order→SALES_ORDER_HDR`, `Order Payment→PAYMENT`, `Order Payment`

**Context previews (first 3):**

1. _**Business Context**: Line items break down orders into individual product purchases. Each captures the price at the moment of ordering. **Key Attributes**: - Unique line identifier - References exact…_

2. _# Business Glossary - E-Commerce Domain (Simplified)  This document defines the core business concepts for the e-commerce platform test dataset.  ──────────────────────────────────────────────────────…_

3. _# Data Dictionary - E-Commerce Database (Simplified)  This document describes the physical database schema for the simplified e-commerce test dataset.  ────────────────────────────────────────────────…_

---

## Anomalies & Observations

No anomalies detected. All questions grounded with acceptable RAGAS scores.
