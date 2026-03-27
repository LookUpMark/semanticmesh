# AB-00 — 01_basics_ecommerce — Run Analysis

**Timestamp:** 2026-03-27 15:03:52  
**Run tag:** `post-fix-v2`

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
| Triplets extracted | 239 |
| Entities resolved | 82 |
| Tables parsed | 6 |
| Tables completed | 6 |

## Query Evaluation Summary

| Metric | Value |
|--------|-------|
| Questions | 15 |
| Grounded | **15/15 (100%)** |
| Avg GT Coverage | 96% |
| Avg Top Score | 0.4189 |
| Avg Chunk Count | 12.0 |
| Abstained | 0 |

## RAGAS Metrics

RAGAS evaluation not enabled for this run.

## Per-Question Deep Dive

### ✅ Q001 — What information is stored for each customer?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.1591 | **Gate:** `proceed_with_warning`

**Expected answer:**
> Each customer has a unique ID, full name, email address, geographic region code, creation date, and active status. The email must be unique across all customers.

**System answer:**
> For each customer, the physical table `CUSTOMER_MASTER` stores the customer’s identifier and account attributes: `CUST_ID`, `FULL_NAME`, `EMAIL`, `REGION_CODE` (nullable), `CREATED_AT`, and `IS_ACTIVE`. The business concept `CUSTOMER` also frames these as key attributes: unique customer ID, valid login email, geographic region for tax, and active/inactive status.

**Sources retrieved (12):** `Header record for each customer sales order→SALES_ORDER_HDR`, `parent_chunk_data_dictionary.txt_3`, `parent_chunk_business_glossary.txt_0`, `Shipment Record→SHIPMENT`, `Payment Transaction→PAYMENT`, `parent_chunk_business_glossary.txt_1`, `SALES_ORDER_HDR→CUSTOMER_MASTER`, `parent_chunk_business_glossary.txt_2`

**Context previews (first 3):**

1. _Business concept 'Header record for each customer sales order' is implemented by physical table SALES_ORDER_HDR (columns: ORDER_ID, CUST_ID, ORDER_DATE, TOTAL_AMT, STATUS_CODE, PAYMENT_CONFIRMED_AT, D…_

2. _# Data Dictionary - E-Commerce Database (Simplified)  This document describes the physical database schema for the simplified e-commerce test dataset.  ────────────────────────────────────────────────…_

3. _# Business Glossary - E-Commerce Domain (Simplified)  This document defines the core business concepts for the e-commerce platform test dataset.  ──────────────────────────────────────────────────────…_

---

### ✅ Q002 — How are products categorized on the platform?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.1590 | **Gate:** `proceed_with_warning`

**Expected answer:**
> Products belong to categories which can have a parent category, forming a hierarchical tree structure. Each product references exactly one category through its CATEGORY_ID.

**System answer:**
> Products are categorized using a hierarchical product category tree. In the schema, the business concept “Hierarchical product category tree” is implemented by the physical table TB_CATEGORY, with products stored in TB_PRODUCT and linked to categories via the foreign key relationship TB_PRODUCT.CATEGORY_ID → TB_CATEGORY.CATEGORY_ID. TB_CATEGORY also includes a self-referencing parent category rela…

**Sources retrieved (12):** `parent_chunk_business_glossary.txt_0`, `parent_chunk_data_dictionary.txt_3`, `parent_chunk_business_glossary.txt_1`, `Master catalogue of all products available for sale→TB_PRODUCT`, `parent_chunk_data_dictionary.txt_4`, `Payment Transaction→PAYMENT`, `parent_chunk_data_dictionary.txt_5`, `Master catalogue of all products available for sale`

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
> In the schema and business rules, a Sales Order is placed by exactly one Customer. This is implemented by the foreign key relationship where `SALES_ORDER_HDR.CUST_ID` references `CUSTOMER_MASTER.CUST_ID`, meaning each sales order header belongs to one customer.

**Sources retrieved (12):** `parent_chunk_business_glossary.txt_2`, `parent_chunk_business_glossary.txt_0`, `parent_chunk_business_glossary.txt_1`, `parent_chunk_data_dictionary.txt_4`, `Header record for each customer sales order→SALES_ORDER_HDR`, `SALES_ORDER_HDR→CUSTOMER_MASTER`, `parent_chunk_data_dictionary.txt_3`, `Order Line Item`

**Context previews (first 3):**

1. _Sales Order Relationships: - A Sales Order is placed by exactly one Customer - A Sales Order has one or more Order Line Items - A Sales Order has one or more Payments - A Sales Order has one or more S…_

2. _# Business Glossary - E-Commerce Domain (Simplified)  This document defines the core business concepts for the e-commerce platform test dataset.  ──────────────────────────────────────────────────────…_

3. _**Business Context**: Line items break down orders into individual product purchases. Each captures the price at the moment of ordering. **Key Attributes**: - Unique line identifier - References exact…_

---

### ✅ Q004 — What does an order line item contain?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.9963 | **Gate:** `proceed`

**Expected answer:**
> An order line item specifies a product, the quantity ordered, the unit price at time of purchase, and the calculated extended amount. Each line item belongs to exactly one sales order.

**System answer:**
> An order line item (business concept “Order Line Item” implemented by table `ORDER_LINE_ITEM`) contains the specific product purchase details within a sales order: a unique line identifier (`LINE_ID`), the parent order (`ORDER_ID`), the ordered product (`PRODUCT_ID`), the quantity ordered (`QUANTITY`), the unit price at the time of ordering (`UNIT_PRICE`), and the extended amount (`LINE_AMT`, defi…

**Sources retrieved (12):** `Order Line Item`, `Order Line Item→ORDER_LINE_ITEM`, `parent_chunk_business_glossary.txt_1`, `ORDER_LINE_ITEM→TB_PRODUCT`, `ORDER_LINE_ITEM→SALES_ORDER_HDR`, `parent_chunk_business_glossary.txt_2`, `parent_chunk_data_dictionary.txt_4`, `Shipment Record→SHIPMENT`

**Context previews (first 3):**

1. _Order Line Item: The table contains LINE_ID, ORDER_ID, PRODUCT_ID, QUANTITY, UNIT_PRICE, and LINE_AMT, which exactly match the business concept of a single line within a sales order specifying a produ…_

2. _Business concept 'Order Line Item' — The table contains LINE_ID, ORDER_ID, PRODUCT_ID, QUANTITY, UNIT_PRICE, and LINE_AMT, which exactly match the business concept of a single line within a sales orde…_

3. _**Business Context**: Line items break down orders into individual product purchases. Each captures the price at the moment of ordering. **Key Attributes**: - Unique line identifier - References exact…_

---

### ✅ Q005 — How are payments linked to orders?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.9232 | **Gate:** `proceed`

**Expected answer:**
> Each payment is associated with exactly one sales order through the ORDER_ID foreign key. Payments track the payment method, amount, status, and confirmation timestamp.

**System answer:**
> Payments are linked to orders through the foreign key in the PAYMENT table: PAYMENT has ORDER_ID that references SALES_ORDER_HDR.ORDER_ID (“PAYMENT references SALES_ORDER_HDR via foreign key ORDER_ID -> SALES_ORDER_HDR.ORDER_ID”). This matches the relationship statement that a Sales Order has one or more Payments, and that each Payment is for exactly one Sales Order.

**Sources retrieved (12):** `PAYMENT→SALES_ORDER_HDR`, `parent_chunk_business_glossary.txt_1`, `parent_chunk_business_glossary.txt_2`, `parent_chunk_data_dictionary.txt_4`, `SHIPMENT→SALES_ORDER_HDR`, `ORDER_LINE_ITEM→SALES_ORDER_HDR`, `SALES_ORDER_HDR→CUSTOMER_MASTER`, `parent_chunk_business_glossary.txt_0`

**Context previews (first 3):**

1. _Relationship: PAYMENT references SALES_ORDER_HDR via foreign key ORDER_ID -> SALES_ORDER_HDR.ORDER_ID.…_

2. _**Business Context**: Line items break down orders into individual product purchases. Each captures the price at the moment of ordering. **Key Attributes**: - Unique line identifier - References exact…_

3. _Sales Order Relationships: - A Sales Order is placed by exactly one Customer - A Sales Order has one or more Order Line Items - A Sales Order has one or more Payments - A Sales Order has one or more S…_

---

### ✅ Q006 — What statuses can an order have?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.4377 | **Gate:** `proceed`

**Expected answer:**
> Orders can have one of five statuses defined via CHECK constraint on SALES_ORDER_HDR.STATUS_CODE: PENDING (initial state when order is created), CONFIRMED (payment has been received), SHIPPED (dispatched to customer), DELIVERED (received by customer), or CANCELLED. The business glossary describes th…

**System answer:**
> An order’s status is represented by the `STATUS_CODE` column in `SALES_ORDER_HDR` (the “Header record for each customer sales order”). The retrieved context does not enumerate the specific possible values (e.g., which exact statuses `STATUS_CODE` can take), so those status codes themselves remain unavailable here.

**Sources retrieved (12):** `Payment Transaction→PAYMENT`, `parent_chunk_business_glossary.txt_0`, `parent_chunk_business_glossary.txt_1`, `Header record for each customer sales order→SALES_ORDER_HDR`, `Shipment Record→SHIPMENT`, `parent_chunk_business_glossary.txt_2`, `Order Line Item`, `parent_chunk_data_dictionary.txt_4`

**Context previews (first 3):**

1. _Business concept 'Payment Transaction' — The PAYMENT table records an individual monetary transaction for a specific order, including payment method, amount, and a lifecycle status with confirmation/c…_

2. _# Business Glossary - E-Commerce Domain (Simplified)  This document defines the core business concepts for the e-commerce platform test dataset.  ──────────────────────────────────────────────────────…_

3. _**Business Context**: Line items break down orders into individual product purchases. Each captures the price at the moment of ordering. **Key Attributes**: - Unique line identifier - References exact…_

---

### ✅ Q007 — Which table stores the product SKU information?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.7768 | **Gate:** `proceed`

**Expected answer:**
> The TB_PRODUCT table stores the SKU (Stock Keeping Unit) code for each product, along with product name, category, price, and active status.

**System answer:**
> The product SKU information is stored in the physical table TB_PRODUCT, which includes the column SKU.

**Sources retrieved (12):** `Master catalogue of all products available for sale→TB_PRODUCT`, `Order Line Item`, `parent_chunk_data_dictionary.txt_3`, `Shipment Record→SHIPMENT`, `Order Line Item→ORDER_LINE_ITEM`, `ORDER_LINE_ITEM→TB_PRODUCT`, `Hierarchical product category tree→TB_CATEGORY`, `parent_chunk_business_glossary.txt_0`

**Context previews (first 3):**

1. _Business concept 'Master catalogue of all products available for sale' is implemented by physical table TB_PRODUCT (columns: PRODUCT_ID, SKU, PRODUCT_NAME, CATEGORY_ID, UNIT_PRICE, IS_ACTIVE).…_

2. _Order Line Item: The table contains LINE_ID, ORDER_ID, PRODUCT_ID, QUANTITY, UNIT_PRICE, and LINE_AMT, which exactly match the business concept of a single line within a sales order specifying a produ…_

3. _# Data Dictionary - E-Commerce Database (Simplified)  This document describes the physical database schema for the simplified e-commerce test dataset.  ────────────────────────────────────────────────…_

---

### ✅ Q008 — How can I find all orders placed by a specific customer?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.1428 | **Gate:** `proceed_with_warning`

**Expected answer:**
> Query the SALES_ORDER_HDR table filtering by CUST_ID. Each order has a foreign key reference to CUSTOMER_MASTER.CUST_ID, so joining these tables on CUST_ID will show all orders for a customer along with their details.

**System answer:**
> To find all orders placed by a specific customer, use the customer-to-order foreign key relationship between `CUSTOMER_MASTER` and `SALES_ORDER_HDR`.

First identify the customer in `CUSTOMER_MASTER` (for example by matching `EMAIL`, since `CUSTOMER_MASTER` has `CUST_ID` and `EMAIL`). Then retrieve all sales orders from `SALES_ORDER_HDR` where `SALES_ORDER_HDR.CUST_ID` equals that customer’s `CUST…

**Sources retrieved (12):** `parent_chunk_data_dictionary.txt_3`, `parent_chunk_business_glossary.txt_2`, `Payment Transaction→PAYMENT`, `parent_chunk_business_glossary.txt_0`, `Header record for each customer sales order→SALES_ORDER_HDR`, `parent_chunk_data_dictionary.txt_4`, `SALES_ORDER_HDR→CUSTOMER_MASTER`, `parent_chunk_business_glossary.txt_1`

**Context previews (first 3):**

1. _# Data Dictionary - E-Commerce Database (Simplified)  This document describes the physical database schema for the simplified e-commerce test dataset.  ────────────────────────────────────────────────…_

2. _Sales Order Relationships: - A Sales Order is placed by exactly one Customer - A Sales Order has one or more Order Line Items - A Sales Order has one or more Payments - A Sales Order has one or more S…_

3. _Business concept 'Payment Transaction' — The PAYMENT table records an individual monetary transaction for a specific order, including payment method, amount, and a lifecycle status with confirmation/c…_

---

### ✅ Q009 — What products were included in a specific order?

**Status:** GROUNDED  
**GT Coverage:** 67% | **Top Score:** 0.1103 | **Gate:** `proceed_with_warning`

**Expected answer:**
> Join ORDER_LINE_ITEM with TB_PRODUCT on PRODUCT_ID. For order ORDER_ID, the line items show which products were ordered, in what quantity, and at what price.

**System answer:**
> The retrieved context does not include any actual order records, so it cannot tell which products were included in a specific order.

What the schema indicates is that the products included in an order are determined by the order’s line items: for a given `ORDER_ID`, the `ORDER_LINE_ITEM` table lists the `PRODUCT_ID` values (via `ORDER_LINE_ITEM.PRODUCT_ID` → `TB_PRODUCT.PRODUCT_ID`), along with `…

**Sources retrieved (12):** `parent_chunk_data_dictionary.txt_4`, `parent_chunk_business_glossary.txt_1`, `Payment Transaction→PAYMENT`, `Order Line Item`, `ORDER_LINE_ITEM→TB_PRODUCT`, `Order Line Item→ORDER_LINE_ITEM`, `parent_chunk_business_glossary.txt_0`, `parent_chunk_data_dictionary.txt_3`

**Context previews (first 3):**

1. _**Foreign Keys**: - CUST_ID → CUSTOMER_MASTER(CUST_ID) **Business Concept Mapping**: SalesOrder ──────────────────────────────────────────────────────────── ORDER_LINE_ITEM ───────────────────────────…_

2. _**Business Context**: Line items break down orders into individual product purchases. Each captures the price at the moment of ordering. **Key Attributes**: - Unique line identifier - References exact…_

3. _Business concept 'Payment Transaction' — The PAYMENT table records an individual monetary transaction for a specific order, including payment method, amount, and a lifecycle status with confirmation/c…_

---

### ✅ Q010 — Show me the order hierarchy from customer to line items.

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.3719 | **Gate:** `proceed`

**Expected answer:**
> The hierarchy is: Customer (CUSTOMER_MASTER) → SalesOrder (SALES_ORDER_HDR) → OrderLineItem (ORDER_LINE_ITEM) → Product (TB_PRODUCT). Each customer has orders, each order has line items, and each line item references a product.

**System answer:**
> Customer → Sales Order → Order Line Items

A Sales Order is placed by exactly one Customer (implemented via `SALES_ORDER_HDR.CUST_ID` foreign key `CUST_ID → CUSTOMER_MASTER(CUST_ID)`). Each Sales Order has one or more Order Line Items (implemented via `ORDER_LINE_ITEM.ORDER_ID` foreign key `ORDER_ID → SALES_ORDER_HDR(ORDER_ID)`), where each `ORDER_LINE_ITEM` belongs to exactly one Sales Order. The…

**Sources retrieved (12):** `parent_chunk_business_glossary.txt_2`, `parent_chunk_data_dictionary.txt_4`, `Order Line Item`, `parent_chunk_business_glossary.txt_1`, `Order Line Item→ORDER_LINE_ITEM`, `ORDER_LINE_ITEM→TB_PRODUCT`, `ORDER_LINE_ITEM→SALES_ORDER_HDR`, `Header record for each customer sales order→SALES_ORDER_HDR`

**Context previews (first 3):**

1. _Sales Order Relationships: - A Sales Order is placed by exactly one Customer - A Sales Order has one or more Order Line Items - A Sales Order has one or more Payments - A Sales Order has one or more S…_

2. _**Foreign Keys**: - CUST_ID → CUSTOMER_MASTER(CUST_ID) **Business Concept Mapping**: SalesOrder ──────────────────────────────────────────────────────────── ORDER_LINE_ITEM ───────────────────────────…_

3. _Order Line Item: The table contains LINE_ID, ORDER_ID, PRODUCT_ID, QUANTITY, UNIT_PRICE, and LINE_AMT, which exactly match the business concept of a single line within a sales order specifying a produ…_

---

### ✅ Q011 — What happens when a payment is confirmed for an order?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.3521 | **Gate:** `proceed`

**Expected answer:**
> When payment is confirmed, the PAYMENT record's STATUS_CODE becomes 'CONFIRMED', the CONFIRMED_AT timestamp is set, and the associated SALES_ORDER_HDR can progress from PENDING to CONFIRMED status.

**System answer:**
> When a payment is confirmed for an order, the schema provides timestamp fields to record that event: `PAYMENT.CONFIRMED_AT` (on the `PAYMENT` table for the specific payment transaction) and `SALES_ORDER_HDR.PAYMENT_CONFIRMED_AT` (on the `SALES_ORDER_HDR` header for the order). The `PAYMENT` record is linked to the corresponding order header via the foreign key `PAYMENT.ORDER_ID -> SALES_ORDER_HDR.…

**Sources retrieved (12):** `parent_chunk_business_glossary.txt_1`, `Payment Transaction→PAYMENT`, `Header record for each customer sales order→SALES_ORDER_HDR`, `PAYMENT→SALES_ORDER_HDR`, `parent_chunk_data_dictionary.txt_4`, `parent_chunk_business_glossary.txt_0`, `parent_chunk_business_glossary.txt_2`, `parent_chunk_data_dictionary.txt_3`

**Context previews (first 3):**

1. _**Business Context**: Line items break down orders into individual product purchases. Each captures the price at the moment of ordering. **Key Attributes**: - Unique line identifier - References exact…_

2. _Business concept 'Payment Transaction' — The PAYMENT table records an individual monetary transaction for a specific order, including payment method, amount, and a lifecycle status with confirmation/c…_

3. _Business concept 'Header record for each customer sales order' is implemented by physical table SALES_ORDER_HDR (columns: ORDER_ID, CUST_ID, ORDER_DATE, TOTAL_AMT, STATUS_CODE, PAYMENT_CONFIRMED_AT, D…_

---

### ✅ Q012 — How are shipments related to orders and warehouses?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.4051 | **Gate:** `proceed`

**Expected answer:**
> Each shipment is for exactly one sales order (ORDER_ID in SHIPMENT references SALES_ORDER_HDR). The shipment also specifies the source warehouse code and includes tracking information and delivery status.

**System answer:**
> Shipments are related to orders through the `SHIPMENT` table’s `ORDER_ID`, which references `SALES_ORDER_HDR(ORDER_ID)` (so each shipment is for exactly one sales order). Shipments are related to warehouses through `SHIPMENT.WAREHOUSE_CODE`, and the business relationship states that a shipment comes from exactly one warehouse.

**Sources retrieved (12):** `parent_chunk_business_glossary.txt_2`, `Shipment Record→SHIPMENT`, `parent_chunk_business_glossary.txt_0`, `parent_chunk_business_glossary.txt_1`, `parent_chunk_data_dictionary.txt_4`, `parent_chunk_data_dictionary.txt_3`, `Payment Transaction→PAYMENT`, `Order Line Item`

**Context previews (first 3):**

1. _Sales Order Relationships: - A Sales Order is placed by exactly one Customer - A Sales Order has one or more Order Line Items - A Sales Order has one or more Payments - A Sales Order has one or more S…_

2. _Business concept 'Shipment Record' — The SHIPMENT table stores shipment-level execution attributes—SHIPMENT_ID, ORDER_ID, SHIPPED_AT, WAREHOUSE_CODE, TRACKING_NUMBER, and STATUS_CODE—matching the busi…_

3. _# Business Glossary - E-Commerce Domain (Simplified)  This document defines the core business concepts for the e-commerce platform test dataset.  ──────────────────────────────────────────────────────…_

---

### ✅ Q013 — Can a product belong to multiple categories?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.3613 | **Gate:** `proceed`

**Expected answer:**
> No, each product belongs to exactly one category. The TB_PRODUCT table has a CATEGORY_ID foreign key referencing TB_CATEGORY, which stores a single category value per product.

**System answer:**
> Based on the schema mapping for products, a product is associated with a single category only. The table `TB_PRODUCT` implements the “Master catalogue of all products available for sale” business concept and includes a single column `CATEGORY_ID`, which is a foreign key to `TB_CATEGORY.CATEGORY_ID`. There is no indication in the retrieved context of any structure (e.g., a join table) that would al…

**Sources retrieved (12):** `parent_chunk_business_glossary.txt_0`, `TB_PRODUCT→TB_CATEGORY`, `parent_chunk_business_glossary.txt_1`, `Hierarchical product category tree→TB_CATEGORY`, `parent_chunk_data_dictionary.txt_3`, `Master catalogue of all products available for sale→TB_PRODUCT`, `parent_chunk_data_dictionary.txt_4`, `Order Line Item→ORDER_LINE_ITEM`

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
> No. The business relationship states that a Sales Order “has one or more Payments” (see “Sales Order Relationships” in the retrieved context). Therefore, an order cannot be placed without at least one payment.

**Sources retrieved (12):** `parent_chunk_data_dictionary.txt_3`, `parent_chunk_business_glossary.txt_1`, `parent_chunk_business_glossary.txt_2`, `parent_chunk_business_glossary.txt_0`, `Payment Transaction→PAYMENT`, `parent_chunk_data_dictionary.txt_4`, `Header record for each customer sales order→SALES_ORDER_HDR`, `PAYMENT→SALES_ORDER_HDR`

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
> The knowledge graph identifies **“Header record for each customer sales order”** as implemented by **`SALES_ORDER_HDR`**, which includes a column **`TOTAL_AMT`** (along with `ORDER_ID`, `CUST_ID`, `ORDER_DATE`, `STATUS_CODE`, `PAYMENT_CONFIRMED_AT`, `DELIVERED_AT`, `CREATED_AT`). It also defines a foreign key relationship **`SALES_ORDER_HDR.CUST_ID → CUSTOMER_MASTER.CUST_ID`**, so you can select t…

**Sources retrieved (12):** `parent_chunk_business_glossary.txt_1`, `parent_chunk_business_glossary.txt_0`, `parent_chunk_data_dictionary.txt_3`, `parent_chunk_business_glossary.txt_2`, `parent_chunk_data_dictionary.txt_4`, `Payment Transaction→PAYMENT`, `Header record for each customer sales order→SALES_ORDER_HDR`, `Shipment Record→SHIPMENT`

**Context previews (first 3):**

1. _**Business Context**: Line items break down orders into individual product purchases. Each captures the price at the moment of ordering. **Key Attributes**: - Unique line identifier - References exact…_

2. _# Business Glossary - E-Commerce Domain (Simplified)  This document defines the core business concepts for the e-commerce platform test dataset.  ──────────────────────────────────────────────────────…_

3. _# Data Dictionary - E-Commerce Database (Simplified)  This document describes the physical database schema for the simplified e-commerce test dataset.  ────────────────────────────────────────────────…_

---

## Anomalies & Observations

No anomalies detected. All questions grounded with acceptable RAGAS scores.
