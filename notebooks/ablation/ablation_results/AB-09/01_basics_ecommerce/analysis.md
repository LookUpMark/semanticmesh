# AB-09 — 01_basics_ecommerce — Run Analysis

**Timestamp:** 2026-04-01 21:16:59  
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
| Triplets extracted | 229 |
| Entities resolved | 72 |
| Tables parsed | 7 |
| Tables completed | 7 |

## Query Evaluation Summary

| Metric | Value |
|--------|-------|
| Questions | 15 |
| Grounded | **15/15 (100%)** |
| Avg GT Coverage | 94% |
| Avg Top Score | 0.4348 |
| Avg Chunk Count | 12.0 |
| Abstained | 0 |

## RAGAS Metrics

RAGAS evaluation not enabled for this run.

## Per-Question Deep Dive

### ✅ Q001 — What information is stored for each customer?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.1578 | **Gate:** `proceed_with_warning`

**Expected answer:**
> Each customer has a unique ID, full name, email address, geographic region code, creation date, and active status. The email must be unique across all customers.

**System answer:**
> For each customer, the physical customer master record is stored in CUSTOMER_MASTER, which implements the Customer business concept. The context shows these fields: CUST_ID as the unique customer identifier, FULL_NAME as the customer’s full name, EMAIL as the unique email address used for login, REGION_CODE as the geographic region for tax, CREATED_AT as the account creation timestamp, and IS_ACTI…

**Sources retrieved (12):** `Sales Order Header`, `Sales Order Header→SALES_ORDER_HDR`, `parent_chunk_data_dictionary.txt_3`, `Master record for all registered platform customers→CUSTOMER_MASTER`, `parent_chunk_business_glossary.txt_0`, `Shipment→SHIPMENT`, `Shipment`, `parent_chunk_business_glossary.txt_1`

**Context previews (first 3):**

1. _Sales Order Header: The table name and structure clearly indicate a header-level sales order record: it has an order ID, customer foreign key, order date, total amount, status, and fulfillment/payment…_

2. _Business concept 'Sales Order Header' — The table name and structure clearly indicate a header-level sales order record: it has an order ID, customer foreign key, order date, total amount, status, and…_

3. _# Data Dictionary - E-Commerce Database (Simplified)  This document describes the physical database schema for the simplified e-commerce test dataset.  ────────────────────────────────────────────────…_

---

### ✅ Q002 — How are products categorized on the platform?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.1590 | **Gate:** `proceed_with_warning`

**Expected answer:**
> Products belong to categories which can have a parent category, forming a hierarchical tree structure. Each product references exactly one category through its CATEGORY_ID.

**System answer:**
> Products are categorized through a category hierarchy. The business concept is a “Hierarchical product category tree,” implemented by the table TB_CATEGORY. Products in TB_PRODUCT are assigned to a category through the column CATEGORY_ID, with a foreign key from TB_PRODUCT.CATEGORY_ID to TB_CATEGORY.CATEGORY_ID. The category structure is hierarchical because TB_CATEGORY also has a self-reference: …

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
> A sales order belongs to exactly one customer. In the schema, this is implemented by SALES_ORDER_HDR.CUST_ID as a foreign key to CUSTOMER_MASTER.CUST_ID.

Synthesizing the business and schema context, the relationship is customer-to-sales-order: customers place sales orders, and each sales order is the header record for one customer order. The glossary also says a Customer is someone who has made …

**Sources retrieved (12):** `parent_chunk_business_glossary.txt_2`, `parent_chunk_business_glossary.txt_0`, `Sales Order Header`, `parent_chunk_business_glossary.txt_1`, `Sales Order Header→SALES_ORDER_HDR`, `parent_chunk_data_dictionary.txt_4`, `SALES_ORDER_HDR→CUSTOMER_MASTER`, `parent_chunk_data_dictionary.txt_3`

**Context previews (first 3):**

1. _Sales Order Relationships: - A Sales Order is placed by exactly one Customer - A Sales Order has one or more Order Line Items - A Sales Order has one or more Payments - A Sales Order has one or more S…_

2. _# Business Glossary - E-Commerce Domain (Simplified)  This document defines the core business concepts for the e-commerce platform test dataset.  ──────────────────────────────────────────────────────…_

3. _Sales Order Header: The table name and structure clearly indicate a header-level sales order record: it has an order ID, customer foreign key, order date, total amount, status, and fulfillment/payment…_

---

### ✅ Q004 — What does an order line item contain?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.9835 | **Gate:** `proceed`

**Expected answer:**
> An order line item specifies a product, the quantity ordered, the unit price at time of purchase, and the calculated extended amount. Each line item belongs to exactly one sales order.

**System answer:**
> An order line item is a single line within a sales order that specifies one product, the quantity ordered, and the unit price at the time of purchase. It also contains the extended line amount, defined as quantity × unit price.

In the schema, this is implemented by ORDER_LINE_ITEM, which contains:
LINE_ID as the unique line identifier, ORDER_ID as the parent sales order, PRODUCT_ID as the product…

**Sources retrieved (12):** `Order Line Item`, `Order Line Item→ORDER_LINE_ITEM`, `parent_chunk_business_glossary.txt_1`, `ORDER_LINE_ITEM→TB_PRODUCT`, `ORDER_LINE_ITEM→SALES_ORDER_HDR`, `parent_chunk_business_glossary.txt_2`, `parent_chunk_data_dictionary.txt_4`, `Sales Order Header`

**Context previews (first 3):**

1. _Order Line Item: The table structure matches a sales order line item exactly: it has foreign keys to the sales order and product, plus quantity, unit price, and extended line amount. The provided busi…_

2. _Business concept 'Order Line Item' — The table structure matches a sales order line item exactly: it has foreign keys to the sales order and product, plus quantity, unit price, and extended line amoun…_

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
A PAYMENT record is for exactly one Sales Order, and a Sales Order has one or more Payments.
The physical relationship is PAYMENT → SALES_ORDER_HDR on ORDER_ID.
To join payments to orders at the schema level, use PAYMENT.ORDER_ID = SALES_ORDER_HDR.ORDER_…

**Sources retrieved (12):** `PAYMENT→SALES_ORDER_HDR`, `parent_chunk_business_glossary.txt_1`, `parent_chunk_business_glossary.txt_2`, `parent_chunk_data_dictionary.txt_4`, `SHIPMENT→SALES_ORDER_HDR`, `ORDER_LINE_ITEM→SALES_ORDER_HDR`, `SALES_ORDER_HDR→CUSTOMER_MASTER`, `parent_chunk_data_dictionary.txt_5`

**Context previews (first 3):**

1. _Relationship: PAYMENT references SALES_ORDER_HDR via foreign key ORDER_ID -> SALES_ORDER_HDR.ORDER_ID.…_

2. _**Business Context**: Line items break down orders into individual product purchases. Each captures the price at the moment of ordering. **Key Attributes**: - Unique line identifier - References exact…_

3. _Sales Order Relationships: - A Sales Order is placed by exactly one Customer - A Sales Order has one or more Order Line Items - A Sales Order has one or more Payments - A Sales Order has one or more S…_

---

### ✅ Q006 — What statuses can an order have?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.3253 | **Gate:** `proceed`

**Expected answer:**
> Orders can have one of five statuses defined via CHECK constraint on SALES_ORDER_HDR.STATUS_CODE: PENDING (initial state when order is created), CONFIRMED (payment has been received), SHIPPED (dispatched to customer), DELIVERED (received by customer), or CANCELLED. The business glossary describes th…

**System answer:**
> The retrieved context shows that an order, implemented by SALES_ORDER_HDR, has a STATUS_CODE column, so orders do have a tracked status at the header level. The same table also includes PAYMENT_CONFIRMED_AT and DELIVERED_AT, which indicate payment and fulfillment milestones.

However, the context does not provide the allowed order status values or a status code list for SALES_ORDER_HDR, so I canno…

**Sources retrieved (12):** `Sales Order Header→SALES_ORDER_HDR`, `Sales Order Header`, `Sales Order Payment→PAYMENT`, `parent_chunk_business_glossary.txt_0`, `parent_chunk_business_glossary.txt_1`, `Shipment→SHIPMENT`, `Shipment`, `parent_chunk_business_glossary.txt_2`

**Context previews (first 3):**

1. _Business concept 'Sales Order Header' — The table name and structure clearly indicate a header-level sales order record: it has an order ID, customer foreign key, order date, total amount, status, and…_

2. _Sales Order Header: The table name and structure clearly indicate a header-level sales order record: it has an order ID, customer foreign key, order date, total amount, status, and fulfillment/payment…_

3. _Business concept 'Sales Order Payment' — The table records a payment tied to a specific sales order via ORDER_ID and includes payment-specific attributes such as method, amount, status, and confirmati…_

---

### ✅ Q007 — Which table stores the product SKU information?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.5995 | **Gate:** `proceed`

**Expected answer:**
> The TB_PRODUCT table stores the SKU (Stock Keeping Unit) code for each product, along with product name, category, price, and active status.

**System answer:**
> The product SKU is stored in TB_PRODUCT, in the column SKU.

**Sources retrieved (12):** `Hierarchical product category tree→TB_PRODUCT`, `parent_chunk_data_dictionary.txt_3`, `Shipment→SHIPMENT`, `Order Line Item`, `Shipment`, `ORDER_LINE_ITEM→TB_PRODUCT`, `Hierarchical product category tree→TB_CATEGORY`, `Order Line Item→ORDER_LINE_ITEM`

**Context previews (first 3):**

1. _Business concept 'Hierarchical product category tree' is implemented by physical table TB_PRODUCT (columns: PRODUCT_ID, SKU, PRODUCT_NAME, CATEGORY_ID, UNIT_PRICE, IS_ACTIVE).…_

2. _# Data Dictionary - E-Commerce Database (Simplified)  This document describes the physical database schema for the simplified e-commerce test dataset.  ────────────────────────────────────────────────…_

3. _Business concept 'Shipment' — The table name, foreign key to SALES_ORDER_HDR, and attributes like shipped timestamp, tracking number, warehouse code, and status all align directly with the shipment co…_

---

### ✅ Q008 — How can I find all orders placed by a specific customer?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.1428 | **Gate:** `proceed_with_warning`

**Expected answer:**
> Query the SALES_ORDER_HDR table filtering by CUST_ID. Each order has a foreign key reference to CUSTOMER_MASTER.CUST_ID, so joining these tables on CUST_ID will show all orders for a customer along with their details.

**System answer:**
> Use the customer-to-order foreign key path between CUSTOMER_MASTER and SALES_ORDER_HDR.

At the schema level, all orders for a customer are stored in SALES_ORDER_HDR, and that table references the customer through SALES_ORDER_HDR.CUST_ID → CUSTOMER_MASTER.CUST_ID. The relevant order columns available in SALES_ORDER_HDR are ORDER_ID, CUST_ID, ORDER_DATE, TOTAL_AMT, STATUS_CODE, PAYMENT_CONFIRMED_AT…

**Sources retrieved (12):** `parent_chunk_data_dictionary.txt_3`, `parent_chunk_business_glossary.txt_2`, `Sales Order Header`, `parent_chunk_business_glossary.txt_0`, `Sales Order Header→SALES_ORDER_HDR`, `parent_chunk_data_dictionary.txt_4`, `Sales Order Payment→PAYMENT`, `SALES_ORDER_HDR→CUSTOMER_MASTER`

**Context previews (first 3):**

1. _# Data Dictionary - E-Commerce Database (Simplified)  This document describes the physical database schema for the simplified e-commerce test dataset.  ────────────────────────────────────────────────…_

2. _Sales Order Relationships: - A Sales Order is placed by exactly one Customer - A Sales Order has one or more Order Line Items - A Sales Order has one or more Payments - A Sales Order has one or more S…_

3. _Sales Order Header: The table name and structure clearly indicate a header-level sales order record: it has an order ID, customer foreign key, order date, total amount, status, and fulfillment/payment…_

---

### ✅ Q009 — What products were included in a specific order?

**Status:** GROUNDED  
**GT Coverage:** 83% | **Top Score:** 0.1555 | **Gate:** `proceed_with_warning`

**Expected answer:**
> Join ORDER_LINE_ITEM with TB_PRODUCT on PRODUCT_ID. For order ORDER_ID, the line items show which products were ordered, in what quantity, and at what price.

**System answer:**
> The knowledge graph does not contain instance-level order data, so it cannot tell me which products were included in a particular order number. It contains schema metadata only.

From the available context, the correct schema-level way to find the products in a specific order is to trace SALES_ORDER_HDR.ORDER_ID to ORDER_LINE_ITEM.ORDER_ID, then ORDER_LINE_ITEM.PRODUCT_ID to TB_PRODUCT.PRODUCT_ID.…

**Sources retrieved (12):** `parent_chunk_data_dictionary.txt_4`, `parent_chunk_business_glossary.txt_1`, `Sales Order Payment→PAYMENT`, `Order Line Item`, `ORDER_LINE_ITEM→TB_PRODUCT`, `Order Line Item→ORDER_LINE_ITEM`, `parent_chunk_business_glossary.txt_0`, `parent_chunk_data_dictionary.txt_3`

**Context previews (first 3):**

1. _**Foreign Keys**: - CUST_ID → CUSTOMER_MASTER(CUST_ID) **Business Concept Mapping**: SalesOrder ──────────────────────────────────────────────────────────── ORDER_LINE_ITEM ───────────────────────────…_

2. _**Business Context**: Line items break down orders into individual product purchases. Each captures the price at the moment of ordering. **Key Attributes**: - Unique line identifier - References exact…_

3. _Business concept 'Sales Order Payment' — The table records a payment tied to a specific sales order via ORDER_ID and includes payment-specific attributes such as method, amount, status, and confirmati…_

---

### ✅ Q010 — Show me the order hierarchy from customer to line items.

**Status:** GROUNDED  
**GT Coverage:** 75% | **Top Score:** 0.3719 | **Gate:** `proceed`

**Expected answer:**
> The hierarchy is: Customer (CUSTOMER_MASTER) → SalesOrder (SALES_ORDER_HDR) → OrderLineItem (ORDER_LINE_ITEM) → Product (TB_PRODUCT). Each customer has orders, each order has line items, and each line item references a product.

**System answer:**
> The order hierarchy in the schema is:

Customer → Sales Order → Order Line Item

Physically, that is:

CUSTOMER_MASTER.CUST_ID → SALES_ORDER_HDR.CUST_ID → ORDER_LINE_ITEM.ORDER_ID

From the retrieved context, the hierarchy works like this: a Sales Order is placed by exactly one Customer, and a Sales Order has one or more Order Line Items. At the table level, CUSTOMER_MASTER is the Customer table, …

**Sources retrieved (12):** `parent_chunk_business_glossary.txt_2`, `parent_chunk_data_dictionary.txt_4`, `Order Line Item`, `Order Line Item→ORDER_LINE_ITEM`, `parent_chunk_business_glossary.txt_1`, `ORDER_LINE_ITEM→TB_PRODUCT`, `ORDER_LINE_ITEM→SALES_ORDER_HDR`, `Sales Order Header`

**Context previews (first 3):**

1. _Sales Order Relationships: - A Sales Order is placed by exactly one Customer - A Sales Order has one or more Order Line Items - A Sales Order has one or more Payments - A Sales Order has one or more S…_

2. _**Foreign Keys**: - CUST_ID → CUSTOMER_MASTER(CUST_ID) **Business Concept Mapping**: SalesOrder ──────────────────────────────────────────────────────────── ORDER_LINE_ITEM ───────────────────────────…_

3. _Order Line Item: The table structure matches a sales order line item exactly: it has foreign keys to the sales order and product, plus quantity, unit price, and extended line amount. The provided busi…_

---

### ✅ Q011 — What happens when a payment is confirmed for an order?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.3521 | **Gate:** `proceed`

**Expected answer:**
> When payment is confirmed, the PAYMENT record's STATUS_CODE becomes 'CONFIRMED', the CONFIRMED_AT timestamp is set, and the associated SALES_ORDER_HDR can progress from PENDING to CONFIRMED status.

**System answer:**
> From the retrieved context, payment confirmation is recorded at both the payment and order-header level for the same order.

A payment is stored in PAYMENT, which is tied to a specific sales order by PAYMENT.ORDER_ID → SALES_ORDER_HDR.ORDER_ID. When it is confirmed, the relevant payment record includes its STATUS_CODE and CONFIRMED_AT timestamp. The related order header in SALES_ORDER_HDR also has…

**Sources retrieved (12):** `parent_chunk_business_glossary.txt_1`, `Sales Order Payment→PAYMENT`, `Sales Order Header→SALES_ORDER_HDR`, `PAYMENT→SALES_ORDER_HDR`, `parent_chunk_data_dictionary.txt_4`, `Sales Order Header`, `parent_chunk_business_glossary.txt_0`, `parent_chunk_business_glossary.txt_2`

**Context previews (first 3):**

1. _**Business Context**: Line items break down orders into individual product purchases. Each captures the price at the moment of ordering. **Key Attributes**: - Unique line identifier - References exact…_

2. _Business concept 'Sales Order Payment' — The table records a payment tied to a specific sales order via ORDER_ID and includes payment-specific attributes such as method, amount, status, and confirmati…_

3. _Business concept 'Sales Order Header' — The table name and structure clearly indicate a header-level sales order record: it has an order ID, customer foreign key, order date, total amount, status, and…_

---

### ✅ Q012 — How are shipments related to orders and warehouses?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.9030 | **Gate:** `proceed`

**Expected answer:**
> Each shipment is for exactly one sales order (ORDER_ID in SHIPMENT references SALES_ORDER_HDR). The shipment also specifies the source warehouse code and includes tracking information and delivery status.

**System answer:**
> Shipments are tied to orders through the SHIPMENT table. The retrieved context states that SHIPMENT implements the business concept Shipment and includes ORDER_ID, WAREHOUSE_CODE, SHIPPED_AT, TRACKING_NUMBER, and STATUS_CODE. SHIPMENT references SALES_ORDER_HDR via the foreign key ORDER_ID → SALES_ORDER_HDR.ORDER_ID.

From the relationship definitions, a Sales Order has one or more Shipments, and …

**Sources retrieved (12):** `Shipment`, `Shipment→SHIPMENT`, `parent_chunk_business_glossary.txt_2`, `parent_chunk_business_glossary.txt_0`, `parent_chunk_business_glossary.txt_1`, `parent_chunk_data_dictionary.txt_4`, `Sales Order Payment→PAYMENT`, `Order Line Item`

**Context previews (first 3):**

1. _Shipment: The table name, foreign key to SALES_ORDER_HDR, and attributes like shipped timestamp, tracking number, warehouse code, and status all align directly with the shipment concept. The business …_

2. _Business concept 'Shipment' — The table name, foreign key to SALES_ORDER_HDR, and attributes like shipped timestamp, tracking number, warehouse code, and status all align directly with the shipment co…_

3. _Sales Order Relationships: - A Sales Order is placed by exactly one Customer - A Sales Order has one or more Order Line Items - A Sales Order has one or more Payments - A Sales Order has one or more S…_

---

### ✅ Q013 — Can a product belong to multiple categories?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.3613 | **Gate:** `proceed`

**Expected answer:**
> No, each product belongs to exactly one category. The TB_PRODUCT table has a CATEGORY_ID foreign key referencing TB_CATEGORY, which stores a single category value per product.

**System answer:**
> Based on the provided schema, no: a product appears to belong to one direct category.

The context shows that TB_PRODUCT has a single CATEGORY_ID column, and TB_PRODUCT references TB_CATEGORY via the foreign key CATEGORY_ID → TB_CATEGORY.CATEGORY_ID. There is no junction table or additional category-assignment structure shown that would allow one product to be linked to multiple categories.

The c…

**Sources retrieved (12):** `parent_chunk_business_glossary.txt_0`, `TB_PRODUCT→TB_CATEGORY`, `Hierarchical product category tree→TB_PRODUCT`, `parent_chunk_business_glossary.txt_1`, `Hierarchical product category tree→TB_CATEGORY`, `parent_chunk_data_dictionary.txt_3`, `parent_chunk_data_dictionary.txt_4`, `Order Line Item`

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
> Based on the retrieved context, not as a persisted sales order without any payment record.

A Customer places a Sales Order through SALES_ORDER_HDR, linked by SALES_ORDER_HDR.CUST_ID → CUSTOMER_MASTER.CUST_ID. The business relationships state that a Sales Order has one or more Payments, and PAYMENT is linked to the order by PAYMENT.ORDER_ID → SALES_ORDER_HDR.ORDER_ID.

So the data model requires e…

**Sources retrieved (12):** `parent_chunk_data_dictionary.txt_3`, `parent_chunk_business_glossary.txt_1`, `parent_chunk_business_glossary.txt_2`, `parent_chunk_business_glossary.txt_0`, `parent_chunk_data_dictionary.txt_4`, `Sales Order Payment→PAYMENT`, `Sales Order Header→SALES_ORDER_HDR`, `Sales Order Header`

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
> The retrieved context does not provide actual customer order totals, only schema and business metadata.

From that schema, the total value of all orders placed by a customer can be derived by summing SALES_ORDER_HDR.TOTAL_AMT for all sales orders with the same SALES_ORDER_HDR.CUST_ID. This is supported by the facts that SALES_ORDER_HDR contains ORDER_ID, CUST_ID, and TOTAL_AMT, and that SALES_ORDE…

**Sources retrieved (12):** `parent_chunk_business_glossary.txt_1`, `parent_chunk_business_glossary.txt_0`, `Sales Order Header→SALES_ORDER_HDR`, `Sales Order Header`, `parent_chunk_data_dictionary.txt_3`, `parent_chunk_business_glossary.txt_2`, `parent_chunk_data_dictionary.txt_4`, `Sales Order Payment→PAYMENT`

**Context previews (first 3):**

1. _**Business Context**: Line items break down orders into individual product purchases. Each captures the price at the moment of ordering. **Key Attributes**: - Unique line identifier - References exact…_

2. _# Business Glossary - E-Commerce Domain (Simplified)  This document defines the core business concepts for the e-commerce platform test dataset.  ──────────────────────────────────────────────────────…_

3. _Business concept 'Sales Order Header' — The table name and structure clearly indicate a header-level sales order record: it has an order ID, customer foreign key, order date, total amount, status, and…_

---

## Anomalies & Observations

No anomalies detected. All questions grounded with acceptable RAGAS scores.
