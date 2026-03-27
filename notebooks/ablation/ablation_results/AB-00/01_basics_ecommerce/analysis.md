# AB-00 — 01_basics_ecommerce — Run Analysis

**Timestamp:** 2026-03-27 11:33:31  
**Run tag:** `ds01-v2`

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
| Triplets extracted | 214 |
| Entities resolved | 73 |
| Tables parsed | 7 |
| Tables completed | 7 |

## Query Evaluation Summary

| Metric | Value |
|--------|-------|
| Questions | 15 |
| Grounded | **15/15 (100%)** |
| Avg GT Coverage | 74% |
| Avg Top Score | 0.4290 |
| Avg Chunk Count | 12.0 |
| Abstained | 0 |

## RAGAS Metrics

RAGAS evaluation not enabled for this run.

## Per-Question Deep Dive

### ✅ Q001 — What information is stored for each customer?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.1827 | **Gate:** `proceed_with_warning`

**Expected answer:**
> Each customer has a unique ID, full name, email address, geographic region code, creation date, and active status. The email must be unique across all customers.

**System answer:**
> For each customer, the database stores the master customer attributes in the table `CUSTOMER_MASTER`. This table includes a unique customer identifier `CUST_ID`, identity fields `FULL_NAME` and `EMAIL`, optional geographic information `REGION_CODE` (for tax), an account creation timestamp `CREATED_AT`, and an activity flag `IS_ACTIVE` indicating whether the customer can place orders. The business …

**Sources retrieved (12):** `parent_chunk_data_dictionary.txt_3`, `parent_chunk_business_glossary.txt_0`, `parent_chunk_business_glossary.txt_1`, `SALES_ORDER_HDR→CUSTOMER_MASTER`, `parent_chunk_business_glossary.txt_2`, `parent_chunk_data_dictionary.txt_4`, `Sales Order Header`, `Registered Customer Master`

**Context previews (first 3):**

1. _# Data Dictionary - E-Commerce Database (Simplified)  This document describes the physical database schema for the simplified e-commerce test dataset.  ────────────────────────────────────────────────…_

2. _# Business Glossary - E-Commerce Domain (Simplified)  This document defines the core business concepts for the e-commerce platform test dataset.  ──────────────────────────────────────────────────────…_

3. _**Business Context**: Line items break down orders into individual product purchases. Each captures the price at the moment of ordering. **Key Attributes**: - Unique line identifier - References exact…_

---

### ✅ Q002 — How are products categorized on the platform?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.1590 | **Gate:** `proceed_with_warning`

**Expected answer:**
> Products belong to categories which can have a parent category, forming a hierarchical tree structure. Each product references exactly one category through its CATEGORY_ID.

**System answer:**
> Products are categorized using the category hierarchy in `TB_CATEGORY` and are linked from the product catalogue table `TB_PRODUCT`.

`TB_PRODUCT` includes a `CATEGORY_ID` that references `TB_CATEGORY.CATEGORY_ID`, via the foreign key `TB_PRODUCT.CATEGORY_ID -> TB_CATEGORY.CATEGORY_ID`. `TB_CATEGORY` also supports a hierarchical structure through `PARENT_CATEGORY_ID -> TB_CATEGORY.CATEGORY_ID` (a …

**Sources retrieved (12):** `parent_chunk_business_glossary.txt_0`, `parent_chunk_data_dictionary.txt_3`, `parent_chunk_business_glossary.txt_1`, `parent_chunk_data_dictionary.txt_4`, `TB_CATEGORY→TB_CATEGORY`, `Product Catalogue`, `parent_chunk_data_dictionary.txt_5`, `Registered Customer Master`

**Context previews (first 3):**

1. _# Business Glossary - E-Commerce Domain (Simplified)  This document defines the core business concepts for the e-commerce platform test dataset.  ──────────────────────────────────────────────────────…_

2. _# Data Dictionary - E-Commerce Database (Simplified)  This document describes the physical database schema for the simplified e-commerce test dataset.  ────────────────────────────────────────────────…_

3. _**Business Context**: Line items break down orders into individual product purchases. Each captures the price at the moment of ordering. **Key Attributes**: - Unique line identifier - References exact…_

---

### ✅ Q003 — What is the relationship between customers and sales orders?

**Status:** GROUNDED  
**GT Coverage:** 75% | **Top Score:** 0.9847 | **Gate:** `proceed`

**Expected answer:**
> Each sales order is placed by exactly one customer, referenced through the CUST_ID foreign key. A customer can place zero or more orders over time.

**System answer:**
> In the e-commerce schema, each Sales Order is placed by exactly one Customer. This is implemented by the foreign key relationship between `CUSTOMER_MASTER` and `SALES_ORDER_HDR`: `SALES_ORDER_HDR.CUST_ID` references `CUSTOMER_MASTER.CUST_ID` (and the Sales Order header includes `CUST_ID`).

**Sources retrieved (12):** `parent_chunk_business_glossary.txt_2`, `parent_chunk_business_glossary.txt_0`, `parent_chunk_business_glossary.txt_1`, `parent_chunk_data_dictionary.txt_4`, `SALES_ORDER_HDR→CUSTOMER_MASTER`, `parent_chunk_data_dictionary.txt_3`, `PAYMENT→SALES_ORDER_HDR`, `parent_chunk_data_dictionary.txt_5`

**Context previews (first 3):**

1. _Sales Order Relationships: - A Sales Order is placed by exactly one Customer - A Sales Order has one or more Order Line Items - A Sales Order has one or more Payments - A Sales Order has one or more S…_

2. _# Business Glossary - E-Commerce Domain (Simplified)  This document defines the core business concepts for the e-commerce platform test dataset.  ──────────────────────────────────────────────────────…_

3. _**Business Context**: Line items break down orders into individual product purchases. Each captures the price at the moment of ordering. **Key Attributes**: - Unique line identifier - References exact…_

---

### ✅ Q004 — What does an order line item contain?

**Status:** GROUNDED  
**GT Coverage:** 50% | **Top Score:** 0.8739 | **Gate:** `proceed`

**Expected answer:**
> An order line item specifies a product, the quantity ordered, the unit price at time of purchase, and the calculated extended amount. Each line item belongs to exactly one sales order.

**System answer:**
> An order line item (table **ORDER_LINE_ITEM**, per “Business Context: Line items break down orders into individual product purchases”) contains a unique line identifier (**LINE_ID**), a reference to exactly one product (**PRODUCT_ID**), the quantity of units ordered (**QUANTITY**), and the unit price captured at the moment of ordering (**UNIT_PRICE**). It also stores the extended amount (**LINE_AM…

**Sources retrieved (12):** `parent_chunk_business_glossary.txt_1`, `ORDER_LINE_ITEM→TB_PRODUCT`, `ORDER_LINE_ITEM→SALES_ORDER_HDR`, `parent_chunk_business_glossary.txt_2`, `parent_chunk_data_dictionary.txt_4`, `parent_chunk_business_glossary.txt_0`, `Historical unit price`, `parent_chunk_data_dictionary.txt_5`

**Context previews (first 3):**

1. _**Business Context**: Line items break down orders into individual product purchases. Each captures the price at the moment of ordering. **Key Attributes**: - Unique line identifier - References exact…_

2. _Relationship: ORDER_LINE_ITEM references TB_PRODUCT via foreign key PRODUCT_ID -> TB_PRODUCT.PRODUCT_ID.…_

3. _Relationship: ORDER_LINE_ITEM references SALES_ORDER_HDR via foreign key ORDER_ID -> SALES_ORDER_HDR.ORDER_ID.…_

---

### ✅ Q005 — How are payments linked to orders?

**Status:** GROUNDED  
**GT Coverage:** 67% | **Top Score:** 0.9232 | **Gate:** `proceed`

**Expected answer:**
> Each payment is associated with exactly one sales order through the ORDER_ID foreign key. Payments track the payment method, amount, status, and confirmation timestamp.

**System answer:**
> In the schema, each **PAYMENT** is linked to a **sales order** through the foreign key **PAYMENT.ORDER_ID** referencing **SALES_ORDER_HDR.ORDER_ID**. The payment concept also states that a **Payment is for exactly one Sales Order**.

**Sources retrieved (12):** `PAYMENT→SALES_ORDER_HDR`, `parent_chunk_business_glossary.txt_1`, `parent_chunk_business_glossary.txt_2`, `parent_chunk_data_dictionary.txt_4`, `SHIPMENT→SALES_ORDER_HDR`, `ORDER_LINE_ITEM→SALES_ORDER_HDR`, `SALES_ORDER_HDR→CUSTOMER_MASTER`, `parent_chunk_business_glossary.txt_0`

**Context previews (first 3):**

1. _Relationship: PAYMENT references SALES_ORDER_HDR via foreign key ORDER_ID -> SALES_ORDER_HDR.ORDER_ID.…_

2. _**Business Context**: Line items break down orders into individual product purchases. Each captures the price at the moment of ordering. **Key Attributes**: - Unique line identifier - References exact…_

3. _Sales Order Relationships: - A Sales Order is placed by exactly one Customer - A Sales Order has one or more Order Line Items - A Sales Order has one or more Payments - A Sales Order has one or more S…_

---

### ✅ Q006 — What statuses can an order have?

**Status:** GROUNDED  
**GT Coverage:** 50% | **Top Score:** 0.5416 | **Gate:** `proceed`

**Expected answer:**
> Orders can have one of five statuses: PENDING (initial state), CONFIRMED (payment received), SHIPPED (sent to customer), DELIVERED (received by customer), or CANCELLED.

**System answer:**
> The retrieved context explicitly lists shipment lifecycle statuses in the shipment/logistics business concept as PREPARING, SHIPPED, IN_TRANSIT, and DELIVERED (described in the logistics-side table referenced as implementing “shipment status (PREPARING/SHIPPED/IN_TRANSIT/DELIVERED)”).

However, the context does not enumerate the allowed values for `SALES_ORDER_HDR.STATUS_CODE`—it only states that …

**Sources retrieved (12):** `parent_chunk_business_glossary.txt_0`, `parent_chunk_business_glossary.txt_1`, `parent_chunk_business_glossary.txt_2`, `parent_chunk_data_dictionary.txt_4`, `parent_chunk_data_dictionary.txt_3`, `SALES_ORDER_HDR→CUSTOMER_MASTER`, `Order Fulfillment Logistics`, `Sales Order Header`

**Context previews (first 3):**

1. _# Business Glossary - E-Commerce Domain (Simplified)  This document defines the core business concepts for the e-commerce platform test dataset.  ──────────────────────────────────────────────────────…_

2. _**Business Context**: Line items break down orders into individual product purchases. Each captures the price at the moment of ordering. **Key Attributes**: - Unique line identifier - References exact…_

3. _Sales Order Relationships: - A Sales Order is placed by exactly one Customer - A Sales Order has one or more Order Line Items - A Sales Order has one or more Payments - A Sales Order has one or more S…_

---

### ✅ Q007 — Which table stores the product SKU information?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.7610 | **Gate:** `proceed`

**Expected answer:**
> The TB_PRODUCT table stores the SKU (Stock Keeping Unit) code for each product, along with product name, category, price, and active status.

**System answer:**
> The table that stores the product SKU information is **TB_PRODUCT** (it includes master data columns such as **PRODUCT_ID, SKU, PRODUCT_NAME**, and **CATEGORY_ID**).

**Sources retrieved (12):** `parent_chunk_data_dictionary.txt_3`, `ORDER_LINE_ITEM→TB_PRODUCT`, `parent_chunk_business_glossary.txt_0`, `TB_PRODUCT→TB_CATEGORY`, `parent_chunk_data_dictionary.txt_4`, `Product Catalogue`, `parent_chunk_data_dictionary.txt_5`, `Order Payment`

**Context previews (first 3):**

1. _# Data Dictionary - E-Commerce Database (Simplified)  This document describes the physical database schema for the simplified e-commerce test dataset.  ────────────────────────────────────────────────…_

2. _Relationship: ORDER_LINE_ITEM references TB_PRODUCT via foreign key PRODUCT_ID -> TB_PRODUCT.PRODUCT_ID.…_

3. _# Business Glossary - E-Commerce Domain (Simplified)  This document defines the core business concepts for the e-commerce platform test dataset.  ──────────────────────────────────────────────────────…_

---

### ✅ Q008 — How can I find all orders placed by a specific customer?

**Status:** GROUNDED  
**GT Coverage:** 75% | **Top Score:** 0.1428 | **Gate:** `proceed_with_warning`

**Expected answer:**
> Query the SALES_ORDER_HDR table filtering by CUST_ID. Each order has a foreign key reference to CUSTOMER_MASTER.CUST_ID, so joining these tables on CUST_ID will show all orders for a customer along with their details.

**System answer:**
> To find all orders placed by a specific customer, use the relationship between the customer master and the sales order header.

First, identify the customer in `CUSTOMER_MASTER` using `CUST_ID` (primary key) and/or `EMAIL` (unique, required for login). Then retrieve the orders from `SALES_ORDER_HDR` by filtering on `SALES_ORDER_HDR.CUST_ID = CUSTOMER_MASTER.CUST_ID`.

This works because each `Sale…

**Sources retrieved (12):** `parent_chunk_data_dictionary.txt_3`, `parent_chunk_business_glossary.txt_2`, `parent_chunk_business_glossary.txt_0`, `parent_chunk_data_dictionary.txt_4`, `SALES_ORDER_HDR→CUSTOMER_MASTER`, `parent_chunk_business_glossary.txt_1`, `Sales Order Header`, `Registered Customer Master`

**Context previews (first 3):**

1. _# Data Dictionary - E-Commerce Database (Simplified)  This document describes the physical database schema for the simplified e-commerce test dataset.  ────────────────────────────────────────────────…_

2. _Sales Order Relationships: - A Sales Order is placed by exactly one Customer - A Sales Order has one or more Order Line Items - A Sales Order has one or more Payments - A Sales Order has one or more S…_

3. _# Business Glossary - E-Commerce Domain (Simplified)  This document defines the core business concepts for the e-commerce platform test dataset.  ──────────────────────────────────────────────────────…_

---

### ✅ Q009 — What products were included in a specific order?

**Status:** GROUNDED  
**GT Coverage:** 50% | **Top Score:** 0.0782 | **Gate:** `proceed_with_warning`

**Expected answer:**
> Join ORDER_LINE_ITEM with TB_PRODUCT on PRODUCT_ID. For order ORDER_ID, the line items show which products were ordered, in what quantity, and at what price.

**System answer:**
> The products included in a specific order would be the products referenced by `ORDER_LINE_ITEM.PRODUCT_ID` for that order’s `ORDER_LINE_ITEM.ORDER_ID` (where `ORDER_LINE_ITEM.ORDER_ID` links to `SALES_ORDER_HDR.ORDER_ID`, and `ORDER_LINE_ITEM.PRODUCT_ID` links to `TB_PRODUCT.PRODUCT_ID`).

However, the retrieved context only defines these schema relationships and business rules; it does not provid…

**Sources retrieved (12):** `parent_chunk_data_dictionary.txt_4`, `parent_chunk_business_glossary.txt_1`, `ORDER_LINE_ITEM→TB_PRODUCT`, `parent_chunk_business_glossary.txt_0`, `parent_chunk_data_dictionary.txt_3`, `parent_chunk_business_glossary.txt_2`, `Order Payment`, `parent_chunk_data_dictionary.txt_5`

**Context previews (first 3):**

1. _**Foreign Keys**: - CUST_ID → CUSTOMER_MASTER(CUST_ID) **Business Concept Mapping**: SalesOrder ──────────────────────────────────────────────────────────── ORDER_LINE_ITEM ───────────────────────────…_

2. _**Business Context**: Line items break down orders into individual product purchases. Each captures the price at the moment of ordering. **Key Attributes**: - Unique line identifier - References exact…_

3. _Relationship: ORDER_LINE_ITEM references TB_PRODUCT via foreign key PRODUCT_ID -> TB_PRODUCT.PRODUCT_ID.…_

---

### ✅ Q010 — Show me the order hierarchy from customer to line items.

**Status:** GROUNDED  
**GT Coverage:** 50% | **Top Score:** 0.3719 | **Gate:** `proceed`

**Expected answer:**
> The hierarchy is: Customer (CUSTOMER_MASTER) → SalesOrder (SALES_ORDER_HDR) → OrderLineItem (ORDER_LINE_ITEM) → Product (TB_PRODUCT). Each customer has orders, each order has line items, and each line item references a product.

**System answer:**
> From the retrieved context, the order hierarchy goes like this:

A Customer maps to the sales order header table SALES_ORDER_HDR via the foreign key SALES_ORDER_HDR.CUST_ID → CUSTOMER_MASTER.CUST_ID (shown as “Sales Order Header” and “Relationship: SALES_ORDER_HDR references CUSTOMER_MASTER via foreign key CUST_ID -> CUSTOMER_MASTER.CUST_ID”).

From SALES_ORDER_HDR to its line items, the line item…

**Sources retrieved (12):** `parent_chunk_business_glossary.txt_2`, `parent_chunk_data_dictionary.txt_4`, `parent_chunk_business_glossary.txt_1`, `ORDER_LINE_ITEM→TB_PRODUCT`, `ORDER_LINE_ITEM→SALES_ORDER_HDR`, `parent_chunk_business_glossary.txt_0`, `parent_chunk_data_dictionary.txt_3`, `SALES_ORDER_HDR→CUSTOMER_MASTER`

**Context previews (first 3):**

1. _Sales Order Relationships: - A Sales Order is placed by exactly one Customer - A Sales Order has one or more Order Line Items - A Sales Order has one or more Payments - A Sales Order has one or more S…_

2. _**Foreign Keys**: - CUST_ID → CUSTOMER_MASTER(CUST_ID) **Business Concept Mapping**: SalesOrder ──────────────────────────────────────────────────────────── ORDER_LINE_ITEM ───────────────────────────…_

3. _**Business Context**: Line items break down orders into individual product purchases. Each captures the price at the moment of ordering. **Key Attributes**: - Unique line identifier - References exact…_

---

### ✅ Q011 — What happens when a payment is confirmed for an order?

**Status:** GROUNDED  
**GT Coverage:** 75% | **Top Score:** 0.3521 | **Gate:** `proceed`

**Expected answer:**
> When payment is confirmed, the PAYMENT record's STATUS_CODE becomes 'CONFIRMED', the CONFIRMED_AT timestamp is set, and the associated SALES_ORDER_HDR can progress from PENDING to CONFIRMED status.

**System answer:**
> When a payment is confirmed for a sales order, the payment confirmation timestamp is recorded in the payment data and reflected at the order-header level.

Specifically, the table **PAYMENT** stores payment attributes including **PAYMENT_METHOD**, **AMOUNT**, **STATUS_CODE**, and **CONFIRMED_AT**, and each **PAYMENT** record links to its order via **ORDER_ID → SALES_ORDER_HDR.ORDER_ID**. The sales…

**Sources retrieved (12):** `parent_chunk_business_glossary.txt_1`, `PAYMENT→SALES_ORDER_HDR`, `parent_chunk_data_dictionary.txt_4`, `parent_chunk_business_glossary.txt_0`, `parent_chunk_business_glossary.txt_2`, `parent_chunk_data_dictionary.txt_3`, `Order Payment`, `Sales Order Header`

**Context previews (first 3):**

1. _**Business Context**: Line items break down orders into individual product purchases. Each captures the price at the moment of ordering. **Key Attributes**: - Unique line identifier - References exact…_

2. _Relationship: PAYMENT references SALES_ORDER_HDR via foreign key ORDER_ID -> SALES_ORDER_HDR.ORDER_ID.…_

3. _**Foreign Keys**: - CUST_ID → CUSTOMER_MASTER(CUST_ID) **Business Concept Mapping**: SalesOrder ──────────────────────────────────────────────────────────── ORDER_LINE_ITEM ───────────────────────────…_

---

### ✅ Q012 — How are shipments related to orders and warehouses?

**Status:** GROUNDED  
**GT Coverage:** 75% | **Top Score:** 0.6001 | **Gate:** `proceed`

**Expected answer:**
> Each shipment is for exactly one sales order (ORDER_ID in SHIPMENT references SALES_ORDER_HDR). The shipment also specifies the source warehouse code and includes tracking information and delivery status.

**System answer:**
> In the schema, shipments are related to orders through `SHIPMENT.ORDER_ID` referencing `SALES_ORDER_HDR.ORDER_ID` (“A Shipment is for exactly one Sales Order”). Shipments are also tied to a single warehouse via `SHIPMENT.WAREHOUSE_CODE` (“A Shipment comes from exactly one Warehouse”).

**Sources retrieved (12):** `parent_chunk_business_glossary.txt_2`, `parent_chunk_business_glossary.txt_0`, `parent_chunk_business_glossary.txt_1`, `parent_chunk_data_dictionary.txt_4`, `parent_chunk_data_dictionary.txt_3`, `Order Fulfillment Logistics`, `parent_chunk_data_dictionary.txt_5`, `Sales Order Header`

**Context previews (first 3):**

1. _Sales Order Relationships: - A Sales Order is placed by exactly one Customer - A Sales Order has one or more Order Line Items - A Sales Order has one or more Payments - A Sales Order has one or more S…_

2. _# Business Glossary - E-Commerce Domain (Simplified)  This document defines the core business concepts for the e-commerce platform test dataset.  ──────────────────────────────────────────────────────…_

3. _**Business Context**: Line items break down orders into individual product purchases. Each captures the price at the moment of ordering. **Key Attributes**: - Unique line identifier - References exact…_

---

### ✅ Q013 — Can a product belong to multiple categories?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.3613 | **Gate:** `proceed`

**Expected answer:**
> No, each product belongs to exactly one category. The TB_PRODUCT table has a CATEGORY_ID foreign key referencing TB_CATEGORY, which stores a single category value per product.

**System answer:**
> Based on the retrieved schema evidence, a product cannot belong to multiple categories in this dataset: `TB_PRODUCT` has a single `CATEGORY_ID` that references `TB_CATEGORY.CATEGORY_ID` (via `TB_PRODUCT` → `TB_CATEGORY` foreign key relationship). The context does not describe any alternative structure (e.g., a many-to-many mapping table) that would allow one product to be in multiple categories.

**Sources retrieved (12):** `parent_chunk_business_glossary.txt_0`, `TB_PRODUCT→TB_CATEGORY`, `parent_chunk_business_glossary.txt_1`, `parent_chunk_data_dictionary.txt_3`, `parent_chunk_data_dictionary.txt_4`, `ORDER_LINE_ITEM→TB_PRODUCT`, `parent_chunk_business_glossary.txt_2`, `parent_chunk_data_dictionary.txt_5`

**Context previews (first 3):**

1. _# Business Glossary - E-Commerce Domain (Simplified)  This document defines the core business concepts for the e-commerce platform test dataset.  ──────────────────────────────────────────────────────…_

2. _Relationship: TB_PRODUCT references TB_CATEGORY via foreign key CATEGORY_ID -> TB_CATEGORY.CATEGORY_ID.…_

3. _**Business Context**: Line items break down orders into individual product purchases. Each captures the price at the moment of ordering. **Key Attributes**: - Unique line identifier - References exact…_

---

### ✅ Q014 — Is it possible for a customer to place an order without payment?

**Status:** GROUNDED  
**GT Coverage:** 75% | **Top Score:** 0.0719 | **Gate:** `proceed_with_warning`

**Expected answer:**
> Technically yes, an order can be created in PENDING status without immediate payment. However, the order cannot be shipped until payment is confirmed (PAYMENT_CONFIRMED_AT is set). The business workflow requires payment confirmation before fulfillment.

**System answer:**
> No. In the retrieved context, the business rules for sales orders state that a Sales Order “has one or more Payments.” Therefore, an order cannot exist without at least one associated payment record (via the relationship between `SALES_ORDER_HDR` and `PAYMENT`).

**Sources retrieved (12):** `parent_chunk_data_dictionary.txt_3`, `parent_chunk_business_glossary.txt_1`, `parent_chunk_business_glossary.txt_2`, `parent_chunk_business_glossary.txt_0`, `parent_chunk_data_dictionary.txt_4`, `PAYMENT→SALES_ORDER_HDR`, `SALES_ORDER_HDR→CUSTOMER_MASTER`, `parent_chunk_data_dictionary.txt_5`

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
> Based on the provided schema, the total value of all orders placed by a customer can be computed by summing the header-level order amounts in `SALES_ORDER_HDR.TOTAL_AMT` for that customer.

`SALES_ORDER_HDR` is a sales order header table that contains `CUST_ID` (the customer who placed the order) and `TOTAL_AMT`. The relationship shown in the context links `SALES_ORDER_HDR.CUST_ID` to `CUSTOMER_MA…

**Sources retrieved (12):** `parent_chunk_business_glossary.txt_1`, `parent_chunk_business_glossary.txt_0`, `parent_chunk_data_dictionary.txt_3`, `parent_chunk_business_glossary.txt_2`, `parent_chunk_data_dictionary.txt_4`, `SALES_ORDER_HDR→CUSTOMER_MASTER`, `Sales Order Header`, `parent_chunk_data_dictionary.txt_5`

**Context previews (first 3):**

1. _**Business Context**: Line items break down orders into individual product purchases. Each captures the price at the moment of ordering. **Key Attributes**: - Unique line identifier - References exact…_

2. _# Business Glossary - E-Commerce Domain (Simplified)  This document defines the core business concepts for the e-commerce platform test dataset.  ──────────────────────────────────────────────────────…_

3. _# Data Dictionary - E-Commerce Database (Simplified)  This document describes the physical database schema for the simplified e-commerce test dataset.  ────────────────────────────────────────────────…_

---

## Anomalies & Observations

No anomalies detected. All questions grounded with acceptable RAGAS scores.
