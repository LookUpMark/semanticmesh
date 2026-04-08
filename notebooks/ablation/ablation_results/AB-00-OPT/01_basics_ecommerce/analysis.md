# AB-00-OPT — 01_basics_ecommerce — Run Analysis

**Timestamp:** 2026-04-08 12:00:24  
**Run tag:** `opt-v1-20260408`

## Configuration

| Parameter | Value |
|-----------|-------|
| Extraction model | `LLM (openai/gpt-4.1-nano)` |
| Reasoning model | `openai/gpt-oss-120b` |
| Embedding model | `BAAI/bge-m3` |
| Retrieval mode | `hybrid` |
| Reranker | `True` |
| Reranker top_k | `12` |
| Chunk size / overlap | `256 / 32` |
| ER similarity threshold | `0.75` |

## Builder Results

| Metric | Value |
|--------|-------|
| Triplets extracted | 99 |
| Entities resolved | 52 |
| Tables parsed | 7 |
| Tables completed | 7 |

## Query Evaluation Summary

| Metric | Value |
|--------|-------|
| Questions | 15 |
| Grounded | **15/15 (100%)** |
| Avg GT Coverage | 100% |
| Avg Top Score | 0.4614 |
| Avg Chunk Count | 12.0 |
| Abstained | 0 |

## RAGAS Metrics

RAGAS evaluation not enabled for this run.

## Per-Question Deep Dive

### ✅ Q001 — What information is stored for each customer?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.4860 | **Gate:** `proceed`

**Expected answer:**
> Each customer has a unique ID, full name, email address, geographic region code, creation date, and active status. The email must be unique across all customers.

**System answer:**
> The **CUSTOMER_MASTER** table holds the core record for every customer. For each customer it stores the following columns:

* **CUST_ID** – the unique, auto‑incremented customer identifier (primary key).  
* **FULL_NAME** – the customer’s full name.  
* **EMAIL** – the unique email address used for login.  
* **REGION_CODE** – the geographic region (used for tax calculations).  
* **CREATED_AT** –…

**Sources retrieved (12):** `CUSTOMER_MASTER→CUSTOMER_MASTER`, `the customer, items, payment status, and delivery information→PAYMENT`, `parent_chunk_data_dictionary.txt_0`, `parent_chunk_business_glossary.txt_3`, `references exactly one Sales Order`, `references exactly one Sales Order→SALES_ORDER_HDR`, `parent_chunk_business_glossary.txt_4`, `SALES_ORDER_HDR→CUSTOMER_MASTER`

**Context previews (first 3):**

1. _Business concept 'CUSTOMER_MASTER' — CUSTOMER_MASTER is a database table or entity that stores customer information, with CUST_ID as its primary key. is implemented by physical table CUSTOMER_MASTER (…_

2. _Business concept 'the customer, items, payment status, and delivery information' — They track the customer, items, payment status, and delivery information. is implemented by physical table PAYMENT (c…_

3. _# Data Dictionary - E-Commerce Database (Simplified)  This document describes the physical database schema for the simplified e-commerce test dataset.  ────────────────────────────────────────────────…_

---

### ✅ Q002 — How are products categorized on the platform?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.1589 | **Gate:** `proceed_with_warning`

**Expected answer:**
> Products belong to categories which can have a parent category, forming a hierarchical tree structure. Each product references exactly one category through its CATEGORY_ID.

**System answer:**
> Products are categorized through a foreign‑key link between the product table and the category table.  

The physical table that implements the **Product** concept is **TB_PRODUCT** (columns include PRODUCT_ID, SKU, PRODUCT_NAME, **CATEGORY_ID**, UNIT_PRICE, IS_ACTIVE). As described in the schema, **TB_PRODUCT** has a foreign‑key **CATEGORY_ID → TB_CATEGORY.CATEGORY_ID** (retrieved context [8]), w…

**Sources retrieved (12):** `parent_chunk_business_glossary.txt_3`, `parent_chunk_data_dictionary.txt_0`, `parent_chunk_business_glossary.txt_4`, `parent_chunk_data_dictionary.txt_1`, `TB_CATEGORY→TB_CATEGORY`, `parent_chunk_data_dictionary.txt_2`, `Product Catalogue→TB_PRODUCT`, `TB_PRODUCT→TB_CATEGORY`

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
> The model defines a **one‑to‑many** relationship between customers and sales orders:

* **Each Sales Order is placed by exactly one Customer** – the sales‑order record contains a `CUST_ID` that points to the customer who created the order. (Chunk [1] – “A Sales Order is placed by exactly one Customer”)

* The `CUST_ID` column in the physical table **SALES_ORDER_HDR** is a foreign key that referenc…

**Sources retrieved (12):** `parent_chunk_business_glossary.txt_5`, `references exactly one Sales Order`, `parent_chunk_business_glossary.txt_3`, `references exactly one Sales Order→SALES_ORDER_HDR`, `parent_chunk_business_glossary.txt_4`, `parent_chunk_data_dictionary.txt_1`, `SALES_ORDER_HDR→CUSTOMER_MASTER`, `parent_chunk_data_dictionary.txt_0`

**Context previews (first 3):**

1. _Sales Order Relationships: - A Sales Order is placed by exactly one Customer - A Sales Order has one or more Order Line Items - A Sales Order has one or more Payments - A Sales Order has one or more S…_

2. _references exactly one Sales Order: An Order is a formal transaction document recording a customer"s request to purchase products, including associated line items, payments, and shipment details.…_

3. _# Business Glossary - E-Commerce Domain (Simplified)  This document defines the core business concepts for the e-commerce platform test dataset.  ──────────────────────────────────────────────────────…_

---

### ✅ Q004 — What does an order line item contain?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.9172 | **Gate:** `proceed`

**Expected answer:**
> An order line item specifies a product, the quantity ordered, the unit price at time of purchase, and the calculated extended amount. Each line item belongs to exactly one sales order.

**System answer:**
> An **Order Line Item** is the record that represents a single product purchase inside a sales order.  
According to the schema and business description it contains the following fields (columns) in the physical table **ORDER_LINE_ITEM**:

* **LINE_ID** – the unique identifier for the line item.  
* **ORDER_ID** – the identifier of the parent sales order (foreign‑key to SALES_ORDER_HDR).  
* **PROD…

**Sources retrieved (12):** `Order Line Item→ORDER_LINE_ITEM`, `parent_chunk_business_glossary.txt_4`, `ORDER_LINE_ITEM→TB_PRODUCT`, `references exactly one Sales Order`, `ORDER_LINE_ITEM→SALES_ORDER_HDR`, `parent_chunk_business_glossary.txt_5`, `references exactly one Sales Order→SALES_ORDER_HDR`, `parent_chunk_data_dictionary.txt_1`

**Context previews (first 3):**

1. _Business concept 'Order Line Item' is implemented by physical table ORDER_LINE_ITEM (columns: LINE_ID, ORDER_ID, PRODUCT_ID, QUANTITY, UNIT_PRICE, LINE_AMT).…_

2. _**Business Context**: Line items break down orders into individual product purchases. Each captures the price at the moment of ordering. **Key Attributes**: - Unique line identifier - References exact…_

3. _Relationship: ORDER_LINE_ITEM references TB_PRODUCT via foreign key PRODUCT_ID -> TB_PRODUCT.PRODUCT_ID.…_

---

### ✅ Q005 — How are payments linked to orders?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.9235 | **Gate:** `proceed`

**Expected answer:**
> Each payment is associated with exactly one sales order through the ORDER_ID foreign key. Payments track the payment method, amount, status, and confirmation timestamp.

**System answer:**
> Payments are linked to orders through a foreign‑key relationship.  
The **PAYMENT** table contains an **ORDER_ID** column (PAYMENT.ORDER_ID) that references the primary key **ORDER_ID** of the **SALES_ORDER_HDR** table (the order header). This is expressed in the schema as:

* “PAYMENT references SALES_ORDER_HDR via foreign key ORDER_ID → SALES_ORDER_HDR.ORDER_ID” ([1]).  
* The business rule stat…

**Sources retrieved (12):** `PAYMENT→SALES_ORDER_HDR`, `parent_chunk_business_glossary.txt_4`, `references exactly one Sales Order→SALES_ORDER_HDR`, `references exactly one Sales Order`, `parent_chunk_business_glossary.txt_5`, `parent_chunk_data_dictionary.txt_1`, `SHIPMENT→SALES_ORDER_HDR`, `ORDER_LINE_ITEM→SALES_ORDER_HDR`

**Context previews (first 3):**

1. _Relationship: PAYMENT references SALES_ORDER_HDR via foreign key ORDER_ID -> SALES_ORDER_HDR.ORDER_ID.…_

2. _**Business Context**: Line items break down orders into individual product purchases. Each captures the price at the moment of ordering. **Key Attributes**: - Unique line identifier - References exact…_

3. _Business concept 'references exactly one Sales Order' — An Order is a formal transaction document recording a customer"s request to purchase products, including associated line items, payments, and sh…_

---

### ✅ Q006 — What statuses can an order have?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.2654 | **Gate:** `proceed`

**Expected answer:**
> Orders can have one of five statuses defined via CHECK constraint on SALES_ORDER_HDR.STATUS_CODE: PENDING (initial state when order is created), CONFIRMED (payment has been received), SHIPPED (dispatched to customer), DELIVERED (received by customer), or CANCELLED. The business glossary describes th…

**System answer:**
> The schema defines a **STATUS_CODE** column for orders in the `SALES_ORDER_HDR` table (columns: ORDER_ID, CUST_ID, ORDER_DATE, TOTAL_AMT, **STATUS_CODE**, PAYMENT_CONFIRMED_AT, DELIVERED_AT, CREATED_AT). However, the retrieved context does not enumerate the specific status values that can appear in this column. Therefore, while we know that an order’s status is stored in the `STATUS_CODE` field, t…

**Sources retrieved (12):** `references exactly one Sales Order→SALES_ORDER_HDR`, `parent_chunk_business_glossary.txt_3`, `parent_chunk_business_glossary.txt_4`, `the customer, items, payment status, and delivery information→PAYMENT`, `references exactly one Sales Order`, `Shipment→SHIPMENT`, `parent_chunk_business_glossary.txt_5`, `parent_chunk_data_dictionary.txt_1`

**Context previews (first 3):**

1. _Business concept 'references exactly one Sales Order' — An Order is a formal transaction document recording a customer"s request to purchase products, including associated line items, payments, and sh…_

2. _# Business Glossary - E-Commerce Domain (Simplified)  This document defines the core business concepts for the e-commerce platform test dataset.  ──────────────────────────────────────────────────────…_

3. _**Business Context**: Line items break down orders into individual product purchases. Each captures the price at the moment of ordering. **Key Attributes**: - Unique line identifier - References exact…_

---

### ✅ Q007 — Which table stores the product SKU information?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.7909 | **Gate:** `proceed`

**Expected answer:**
> The TB_PRODUCT table stores the SKU (Stock Keeping Unit) code for each product, along with product name, category, price, and active status.

**System answer:**
> The product SKU is stored in the **TB_PRODUCT** table (its columns include PRODUCT_ID, SKU, PRODUCT_NAME, CATEGORY_ID, UNIT_PRICE, IS_ACTIVE).

**Sources retrieved (12):** `Product Catalogue→TB_PRODUCT`, `Order Line Item→ORDER_LINE_ITEM`, `references exactly one Sales Order→SALES_ORDER_HDR`, `parent_chunk_data_dictionary.txt_0`, `CUSTOMER_MASTER→CUSTOMER_MASTER`, `ORDER_LINE_ITEM→TB_PRODUCT`, `parent_chunk_business_glossary.txt_3`, `Hierarchical product category tree→TB_CATEGORY`

**Context previews (first 3):**

1. _Business concept 'Product Catalogue' is implemented by physical table TB_PRODUCT (columns: PRODUCT_ID, SKU, PRODUCT_NAME, CATEGORY_ID, UNIT_PRICE, IS_ACTIVE).…_

2. _Business concept 'Order Line Item' is implemented by physical table ORDER_LINE_ITEM (columns: LINE_ID, ORDER_ID, PRODUCT_ID, QUANTITY, UNIT_PRICE, LINE_AMT).…_

3. _Business concept 'references exactly one Sales Order' — An Order is a formal transaction document recording a customer"s request to purchase products, including associated line items, payments, and sh…_

---

### ✅ Q008 — How can I find all orders placed by a specific customer?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.1429 | **Gate:** `proceed_with_warning`

**Expected answer:**
> Query the SALES_ORDER_HDR table filtering by CUST_ID. Each order has a foreign key reference to CUSTOMER_MASTER.CUST_ID, so joining these tables on CUST_ID will show all orders for a customer along with their details.

**System answer:**
> To retrieve every sales order that belongs to one customer you use the link between **CUSTOMER_MASTER** and **SALES_ORDER_HDR**:

* **CUSTOMER_MASTER** holds the master record for each customer (primary key `CUST_ID`).
* **SALES_ORDER_HDR** stores each order and contains the foreign‑key column `CUST_ID` that points to `CUSTOMER_MASTER.CUST_ID` (see chunk 7).

The query therefore filters `SALES_ORD…

**Sources retrieved (12):** `parent_chunk_data_dictionary.txt_0`, `parent_chunk_business_glossary.txt_5`, `parent_chunk_business_glossary.txt_3`, `parent_chunk_data_dictionary.txt_1`, `references exactly one Sales Order→SALES_ORDER_HDR`, `the customer, items, payment status, and delivery information→PAYMENT`, `SALES_ORDER_HDR→CUSTOMER_MASTER`, `parent_chunk_business_glossary.txt_4`

**Context previews (first 3):**

1. _# Data Dictionary - E-Commerce Database (Simplified)  This document describes the physical database schema for the simplified e-commerce test dataset.  ────────────────────────────────────────────────…_

2. _Sales Order Relationships: - A Sales Order is placed by exactly one Customer - A Sales Order has one or more Order Line Items - A Sales Order has one or more Payments - A Sales Order has one or more S…_

3. _# Business Glossary - E-Commerce Domain (Simplified)  This document defines the core business concepts for the e-commerce platform test dataset.  ──────────────────────────────────────────────────────…_

---

### ✅ Q009 — How does the schema link orders to their individual product line items?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.7431 | **Gate:** `proceed`

**Expected answer:**
> The ORDER_LINE_ITEM table is the junction entity between SALES_ORDER_HDR and TB_PRODUCT. It contains ORDER_ID (foreign key to SALES_ORDER_HDR) and PRODUCT_ID (foreign key to TB_PRODUCT), allowing a single order to have multiple line items. Each line item also records QUANTITY (constrained to be > 0)…

**System answer:**
> The schema connects a sales order to its product‑level details through a foreign‑key relationship between the **SALES_ORDER_HDR** table (the order header) and the **ORDER_LINE_ITEM** table (the line‑item detail).

* **SALES_ORDER_HDR** – primary key **ORDER_ID** (BIGINT).  
* **ORDER_LINE_ITEM** – column **ORDER_ID** (BIGINT) that is defined as a foreign key pointing to **SALES_ORDER_HDR.ORDER_ID*…

**Sources retrieved (12):** `ORDER_LINE_ITEM→TB_PRODUCT`, `parent_chunk_business_glossary.txt_4`, `ORDER_LINE_ITEM→SALES_ORDER_HDR`, `parent_chunk_data_dictionary.txt_1`, `Order Line Item→ORDER_LINE_ITEM`, `references exactly one Sales Order→SALES_ORDER_HDR`, `references exactly one Sales Order`, `parent_chunk_business_glossary.txt_5`

**Context previews (first 3):**

1. _Relationship: ORDER_LINE_ITEM references TB_PRODUCT via foreign key PRODUCT_ID -> TB_PRODUCT.PRODUCT_ID.…_

2. _**Business Context**: Line items break down orders into individual product purchases. Each captures the price at the moment of ordering. **Key Attributes**: - Unique line identifier - References exact…_

3. _Relationship: ORDER_LINE_ITEM references SALES_ORDER_HDR via foreign key ORDER_ID -> SALES_ORDER_HDR.ORDER_ID.…_

---

### ✅ Q010 — Show me the order hierarchy from customer to line items.

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.3712 | **Gate:** `proceed`

**Expected answer:**
> The hierarchy is: Customer (CUSTOMER_MASTER) → SalesOrder (SALES_ORDER_HDR) → OrderLineItem (ORDER_LINE_ITEM) → Product (TB_PRODUCT). Each customer has orders, each order has line items, and each line item references a product.

**System answer:**
> The hierarchy is built from three tables that are linked by foreign‑key relationships:

1. **Customer** – the master record is stored in **CUSTOMER_MASTER** (primary key CUST_ID).  
2. **Sales Order** – each order is stored in **SALES_ORDER_HDR**; it contains a column CUST_ID that references CUSTOMER_MASTER(CUST_ID) ([2] and [12]). This implements the rule “a Sales Order is placed by exactly one C…

**Sources retrieved (12):** `parent_chunk_business_glossary.txt_5`, `parent_chunk_data_dictionary.txt_1`, `Order Line Item→ORDER_LINE_ITEM`, `references exactly one Sales Order→SALES_ORDER_HDR`, `parent_chunk_business_glossary.txt_4`, `references exactly one Sales Order`, `ORDER_LINE_ITEM→TB_PRODUCT`, `ORDER_LINE_ITEM→SALES_ORDER_HDR`

**Context previews (first 3):**

1. _Sales Order Relationships: - A Sales Order is placed by exactly one Customer - A Sales Order has one or more Order Line Items - A Sales Order has one or more Payments - A Sales Order has one or more S…_

2. _**Foreign Keys**: - CUST_ID → CUSTOMER_MASTER(CUST_ID) **Business Concept Mapping**: SalesOrder ──────────────────────────────────────────────────────────── ORDER_LINE_ITEM ───────────────────────────…_

3. _Business concept 'Order Line Item' is implemented by physical table ORDER_LINE_ITEM (columns: LINE_ID, ORDER_ID, PRODUCT_ID, QUANTITY, UNIT_PRICE, LINE_AMT).…_

---

### ✅ Q011 — How does the schema model the confirmation state of a payment and its relationship to the order?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.1133 | **Gate:** `proceed_with_warning`

**Expected answer:**
> Payment confirmation is tracked through two schema fields: PAYMENT.CONFIRMED_AT (nullable DATETIME — NULL means not yet confirmed) and PAYMENT.STATUS_CODE constrained to PENDING, CONFIRMED, FAILED, or REFUNDED. At the order level, SALES_ORDER_HDR.PAYMENT_CONFIRMED_AT is a nullable datetime that mirr…

**System answer:**
> **What the retrieved schema tells us**

1. **Payment table** – The physical table **PAYMENT** is defined with the columns  
   `PAYMENT_ID, ORDER_ID, PAYMENT_METHOD, AMOUNT, STATUS_CODE, CONFIRMED_AT, CREATED_AT`【2】.  

2. **Order (sales‑order) table** – The table **SALES_ORDER_HDR** contains, among others, the columns  
   `ORDER_ID, CUST_ID, ORDER_DATE, TOTAL_AMT, STATUS_CODE, PAYMENT_CONFIRMED_…

**Sources retrieved (12):** `parent_chunk_business_glossary.txt_4`, `the customer, items, payment status, and delivery information→PAYMENT`, `references exactly one Sales Order→SALES_ORDER_HDR`, `parent_chunk_data_dictionary.txt_1`, `parent_chunk_data_dictionary.txt_0`, `references exactly one Sales Order`, `parent_chunk_business_glossary.txt_5`, `PAYMENT→SALES_ORDER_HDR`

**Context previews (first 3):**

1. _**Business Context**: Line items break down orders into individual product purchases. Each captures the price at the moment of ordering. **Key Attributes**: - Unique line identifier - References exact…_

2. _Business concept 'the customer, items, payment status, and delivery information' — They track the customer, items, payment status, and delivery information. is implemented by physical table PAYMENT (c…_

3. _Business concept 'references exactly one Sales Order' — An Order is a formal transaction document recording a customer"s request to purchase products, including associated line items, payments, and sh…_

---

### ✅ Q012 — How are shipments related to orders and warehouses?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.4940 | **Gate:** `proceed`

**Expected answer:**
> Each shipment is for exactly one sales order (ORDER_ID in SHIPMENT references SALES_ORDER_HDR). The shipment also specifies the source warehouse code and includes tracking information and delivery status.

**System answer:**
> In the model the **SHIPMENT** table connects to orders and warehouses as follows:

* **Order relationship** – The column **ORDER_ID** in SHIPMENT stores the identifier of the sales order to which the shipment belongs. Chunk 12 confirms a foreign‑key relationship `SHIPMENT.ORDER_ID → SALES_ORDER_HDR.ORDER_ID`. The business rules (Chunk 2) state that *“A Shipment is for exactly one Sales Order,”* so…

**Sources retrieved (12):** `Shipment→SHIPMENT`, `parent_chunk_business_glossary.txt_5`, `parent_chunk_business_glossary.txt_3`, `references exactly one Sales Order`, `references exactly one Sales Order→SALES_ORDER_HDR`, `parent_chunk_business_glossary.txt_4`, `the customer, items, payment status, and delivery information→PAYMENT`, `parent_chunk_data_dictionary.txt_1`

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
> The schema defines a **single‑column foreign key** from the product table to the category table:

- **TB_PRODUCT** contains the column **CATEGORY_ID**.  
- The relationship is described as “TB_PRODUCT references TB_CATEGORY via foreign key **CATEGORY_ID → TB_CATEGORY.CATEGORY_ID**” (see chunk [2] and the mapping in chunk [10]).

Because the foreign‑key is a single column, each row in **TB_PRODUCT*…

**Sources retrieved (12):** `parent_chunk_business_glossary.txt_3`, `TB_PRODUCT→TB_CATEGORY`, `parent_chunk_business_glossary.txt_4`, `Product Catalogue→TB_PRODUCT`, `Hierarchical product category tree→TB_CATEGORY`, `parent_chunk_data_dictionary.txt_0`, `parent_chunk_data_dictionary.txt_1`, `ORDER_LINE_ITEM→TB_PRODUCT`

**Context previews (first 3):**

1. _# Business Glossary - E-Commerce Domain (Simplified)  This document defines the core business concepts for the e-commerce platform test dataset.  ──────────────────────────────────────────────────────…_

2. _Relationship: TB_PRODUCT references TB_CATEGORY via foreign key CATEGORY_ID -> TB_CATEGORY.CATEGORY_ID.…_

3. _**Business Context**: Line items break down orders into individual product purchases. Each captures the price at the moment of ordering. **Key Attributes**: - Unique line identifier - References exact…_

---

### ✅ Q014 — Is it possible for a customer to place an order without payment?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0721 | **Gate:** `proceed_with_warning`

**Expected answer:**
> Yes, an order can exist without payment. SALES_ORDER_HDR has STATUS_CODE defaulting to PENDING and PAYMENT_CONFIRMED_AT is nullable (NULL when no payment yet). The PAYMENT table links via ORDER_ID foreign key but nothing prevents an order from existing without a payment row. However, the business gl…

**System answer:**
> The retrieved context contains two relevant pieces of information:

1. **Business rule** – In chunk [3] the relationships for a Sales Order are described as:  
   “A Sales Order has one or more Payments.” This rule states that, according to the business model, every sales order must be associated with at least one payment record.

2. **Schema relationship** – In chunks [5], [8] and [9] the physica…

**Sources retrieved (12):** `parent_chunk_data_dictionary.txt_0`, `parent_chunk_business_glossary.txt_4`, `parent_chunk_business_glossary.txt_5`, `references exactly one Sales Order`, `references exactly one Sales Order→SALES_ORDER_HDR`, `parent_chunk_business_glossary.txt_3`, `parent_chunk_data_dictionary.txt_1`, `the customer, items, payment status, and delivery information→PAYMENT`

**Context previews (first 3):**

1. _# Data Dictionary - E-Commerce Database (Simplified)  This document describes the physical database schema for the simplified e-commerce test dataset.  ────────────────────────────────────────────────…_

2. _**Business Context**: Line items break down orders into individual product purchases. Each captures the price at the moment of ordering. **Key Attributes**: - Unique line identifier - References exact…_

3. _Sales Order Relationships: - A Sales Order is placed by exactly one Customer - A Sales Order has one or more Order Line Items - A Sales Order has one or more Payments - A Sales Order has one or more S…_

---

### ✅ Q015 — What schema fields support monetary value tracking across orders and their line items?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0970 | **Gate:** `proceed_with_warning`

**Expected answer:**
> SALES_ORDER_HDR stores the header-level order amount in TOTAL_AMT (DECIMAL(12,2) NOT NULL). ORDER_LINE_ITEM provides the per-product breakdown: UNIT_PRICE (price locked at time of order, not updated with future changes), QUANTITY (constrained to > 0), and LINE_AMT (= QUANTITY × UNIT_PRICE). Both tab…

**System answer:**
> The schema records monetary values in two places:

1. **SALES_ORDER_HDR** – the column **TOTAL_AMT** holds the total monetary amount for the whole sales order.

2. **ORDER_LINE_ITEM** – the columns that capture money for each line are:
   * **UNIT_PRICE** (DECIMAL 10,2) – the price of a single unit at the time the order is placed.
   * **LINE_AMT** (DECIMAL 12,2) – the extended amount for the line…

**Sources retrieved (12):** `Order Line Item→ORDER_LINE_ITEM`, `parent_chunk_business_glossary.txt_4`, `parent_chunk_data_dictionary.txt_1`, `references exactly one Sales Order→SALES_ORDER_HDR`, `ORDER_LINE_ITEM→TB_PRODUCT`, `references exactly one Sales Order`, `ORDER_LINE_ITEM→SALES_ORDER_HDR`, `the customer, items, payment status, and delivery information→PAYMENT`

**Context previews (first 3):**

1. _Business concept 'Order Line Item' is implemented by physical table ORDER_LINE_ITEM (columns: LINE_ID, ORDER_ID, PRODUCT_ID, QUANTITY, UNIT_PRICE, LINE_AMT).…_

2. _**Business Context**: Line items break down orders into individual product purchases. Each captures the price at the moment of ordering. **Key Attributes**: - Unique line identifier - References exact…_

3. _**Foreign Keys**: - CUST_ID → CUSTOMER_MASTER(CUST_ID) **Business Concept Mapping**: SalesOrder ──────────────────────────────────────────────────────────── ORDER_LINE_ITEM ───────────────────────────…_

---

## Anomalies & Observations

No anomalies detected. All questions grounded with acceptable RAGAS scores.
