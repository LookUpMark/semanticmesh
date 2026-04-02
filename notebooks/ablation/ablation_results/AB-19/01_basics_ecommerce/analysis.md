# AB-19 — 01_basics_ecommerce — Run Analysis

**Timestamp:** 2026-03-31 02:50:05  
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
| Triplets extracted | 249 |
| Entities resolved | 82 |
| Tables parsed | 7 |
| Tables completed | 7 |

## Query Evaluation Summary

| Metric | Value |
|--------|-------|
| Questions | 15 |
| Grounded | **15/15 (100%)** |
| Avg GT Coverage | 96% |
| Avg Top Score | 0.4742 |
| Avg Chunk Count | 12.0 |
| Abstained | 0 |

## RAGAS Metrics

RAGAS evaluation not enabled for this run.

## Per-Question Deep Dive

### ✅ Q001 — What information is stored for each customer?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.7610 | **Gate:** `proceed`

**Expected answer:**
> Each customer has a unique ID, full name, email address, geographic region code, creation date, and active status. The email must be unique across all customers.

**System answer:**
> For each customer, the physical table CUSTOMER_MASTER stores these fields: CUST_ID, FULL_NAME, EMAIL, REGION_CODE, CREATED_AT, and IS_ACTIVE.

From the data dictionary, these mean: CUST_ID is the unique customer identifier, FULL_NAME is the customer’s full name, EMAIL is the unique email address used for login, REGION_CODE is the geographic region for tax, CREATED_AT is the account creation timest…

**Sources retrieved (12):** `Master record for all registered platform customers→CUSTOMER_MASTER`, `Sales Order Header→SALES_ORDER_HDR`, `parent_chunk_data_dictionary.txt_3`, `parent_chunk_business_glossary.txt_0`, `parent_chunk_business_glossary.txt_1`, `SALES_ORDER_HDR→CUSTOMER_MASTER`, `Each line item`, `Monetary Transaction→PAYMENT`

**Context previews (first 3):**

1. _Business concept 'Master record for all registered platform customers' — The table stores a customer identifier, full name, unique email, region code, account creation timestamp, and active flag, whic…_

2. _Business concept 'Sales Order Header' — The table name and structure indicate a header-level order record with order ID, customer reference, order date, total amount, status, and fulfillment timestamp…_

3. _# Data Dictionary - E-Commerce Database (Simplified)  This document describes the physical database schema for the simplified e-commerce test dataset.  ────────────────────────────────────────────────…_

---

### ✅ Q002 — How are products categorized on the platform?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.1590 | **Gate:** `proceed_with_warning`

**Expected answer:**
> Products belong to categories which can have a parent category, forming a hierarchical tree structure. Each product references exactly one category through its CATEGORY_ID.

**System answer:**
> Products are categorized through the product master table TB_PRODUCT. Each product record includes a CATEGORY_ID, and that column is a foreign key to TB_CATEGORY.CATEGORY_ID. This means each product is assigned to a category stored in TB_CATEGORY.

The context also shows that TB_CATEGORY has a self-reference via PARENT_CATEGORY_ID → TB_CATEGORY.CATEGORY_ID, so the category structure can be hierarc…

**Sources retrieved (12):** `parent_chunk_business_glossary.txt_0`, `Product`, `parent_chunk_data_dictionary.txt_3`, `parent_chunk_business_glossary.txt_1`, `Product→TB_PRODUCT`, `Master record for all registered platform customers→CUSTOMER_MASTER`, `parent_chunk_data_dictionary.txt_4`, `parent_chunk_data_dictionary.txt_5`

**Context previews (first 3):**

1. _# Business Glossary - E-Commerce Domain (Simplified)  This document defines the core business concepts for the e-commerce platform test dataset.  ──────────────────────────────────────────────────────…_

2. _Product: The table contains a product master record with product ID, SKU, product name, category, unit price, and active status, which aligns directly with the Product concept. The foreign key to TB_C…_

3. _# Data Dictionary - E-Commerce Database (Simplified)  This document describes the physical database schema for the simplified e-commerce test dataset.  ────────────────────────────────────────────────…_

---

### ✅ Q003 — What is the relationship between customers and sales orders?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.9847 | **Gate:** `proceed`

**Expected answer:**
> Each sales order is placed by exactly one customer, referenced through the CUST_ID foreign key. A customer can place zero or more orders over time.

**System answer:**
> A customer-to-sales-order relationship is modeled as follows: each Sales Order is placed by exactly one Customer. In the physical schema, this is implemented by SALES_ORDER_HDR.CUST_ID as a foreign key to CUSTOMER_MASTER.CUST_ID.

The context also describes Customer as the party who places orders, and lists SalesOrder as a related concept to Customer. At the business level, a customer is defined a…

**Sources retrieved (12):** `parent_chunk_business_glossary.txt_2`, `parent_chunk_business_glossary.txt_0`, `parent_chunk_business_glossary.txt_1`, `Sales Order Header→SALES_ORDER_HDR`, `parent_chunk_data_dictionary.txt_4`, `SALES_ORDER_HDR→CUSTOMER_MASTER`, `parent_chunk_data_dictionary.txt_3`, `Monetary Transaction→PAYMENT`

**Context previews (first 3):**

1. _Sales Order Relationships: - A Sales Order is placed by exactly one Customer - A Sales Order has one or more Order Line Items - A Sales Order has one or more Payments - A Sales Order has one or more S…_

2. _# Business Glossary - E-Commerce Domain (Simplified)  This document defines the core business concepts for the e-commerce platform test dataset.  ──────────────────────────────────────────────────────…_

3. _**Business Context**: Line items break down orders into individual product purchases. Each captures the price at the moment of ordering. **Key Attributes**: - Unique line identifier - References exact…_

---

### ✅ Q004 — What does an order line item contain?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.9888 | **Gate:** `proceed`

**Expected answer:**
> An order line item specifies a product, the quantity ordered, the unit price at time of purchase, and the calculated extended amount. Each line item belongs to exactly one sales order.

**System answer:**
> An order line item, implemented by the ORDER_LINE_ITEM table, contains the detail for one individual product purchase within a sales order. It includes LINE_ID (unique line identifier), ORDER_ID (the parent sales order), PRODUCT_ID (the product ordered), QUANTITY (number of units), UNIT_PRICE (the price at the time of ordering), and LINE_AMT (the extended amount, calculated as quantity × unit pric…

**Sources retrieved (12):** `Each line item`, `Each line item→ORDER_LINE_ITEM`, `parent_chunk_business_glossary.txt_1`, `ORDER_LINE_ITEM→TB_PRODUCT`, `ORDER_LINE_ITEM→SALES_ORDER_HDR`, `parent_chunk_business_glossary.txt_2`, `parent_chunk_data_dictionary.txt_4`, `Product`

**Context previews (first 3):**

1. _Each line item: The table contains line-level order detail fields such as ORDER_ID, PRODUCT_ID, QUANTITY, UNIT_PRICE, and LINE_AMT, which match the business concept describing individual product purch…_

2. _Business concept 'Each line item' — The table contains line-level order detail fields such as ORDER_ID, PRODUCT_ID, QUANTITY, UNIT_PRICE, and LINE_AMT, which match the business concept describing indi…_

3. _**Business Context**: Line items break down orders into individual product purchases. Each captures the price at the moment of ordering. **Key Attributes**: - Unique line identifier - References exact…_

---

### ✅ Q005 — How are payments linked to orders?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.9232 | **Gate:** `proceed`

**Expected answer:**
> Each payment is associated with exactly one sales order through the ORDER_ID foreign key. Payments track the payment method, amount, status, and confirmation timestamp.

**System answer:**
> Payments are linked to orders through the `ORDER_ID` foreign key. Specifically, `PAYMENT.ORDER_ID` references `SALES_ORDER_HDR.ORDER_ID`.

From the schema and business context:
`PAYMENT` is the physical table for the payment/monetary transaction concept, with columns `PAYMENT_ID, ORDER_ID, PAYMENT_METHOD, AMOUNT, STATUS_CODE, CONFIRMED_AT, CREATED_AT`.
`SALES_ORDER_HDR` is the order header table, …

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
> The retrieved context shows that a sales order has a status field, specifically SALES_ORDER_HDR.STATUS_CODE, and describes the order as having “status” at the header level. However, it does not enumerate the possible order status values.

Related lifecycle fields on the order header are PAYMENT_CONFIRMED_AT and DELIVERED_AT in SALES_ORDER_HDR, but these are timestamps, not status codes. Payment an…

**Sources retrieved (12):** `parent_chunk_business_glossary.txt_0`, `parent_chunk_business_glossary.txt_1`, `Monetary Transaction→PAYMENT`, `Sales Order Header→SALES_ORDER_HDR`, `Product`, `Shipment→SHIPMENT`, `Product→TB_PRODUCT`, `parent_chunk_business_glossary.txt_2`

**Context previews (first 3):**

1. _# Business Glossary - E-Commerce Domain (Simplified)  This document defines the core business concepts for the e-commerce platform test dataset.  ──────────────────────────────────────────────────────…_

2. _**Business Context**: Line items break down orders into individual product purchases. Each captures the price at the moment of ordering. **Key Attributes**: - Unique line identifier - References exact…_

3. _Business concept 'Monetary Transaction' — The table records a payment tied to a sales order via ORDER_ID, with amount, method, status, and confirmation timestamp, which matches the concept of the mone…_

---

### ✅ Q007 — Which table stores the product SKU information?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.8316 | **Gate:** `proceed`

**Expected answer:**
> The TB_PRODUCT table stores the SKU (Stock Keeping Unit) code for each product, along with product name, category, price, and active status.

**System answer:**
> The product SKU is stored in TB_PRODUCT, in the SKU column. The context maps the Product business concept to physical table TB_PRODUCT with columns PRODUCT_ID, SKU, PRODUCT_NAME, CATEGORY_ID, UNIT_PRICE, and IS_ACTIVE.

**Sources retrieved (12):** `Product`, `Product→TB_PRODUCT`, `Each line item`, `parent_chunk_data_dictionary.txt_3`, `Each line item→ORDER_LINE_ITEM`, `ORDER_LINE_ITEM→TB_PRODUCT`, `parent_chunk_business_glossary.txt_0`, `TB_PRODUCT→TB_CATEGORY`

**Context previews (first 3):**

1. _Product: The table contains a product master record with product ID, SKU, product name, category, unit price, and active status, which aligns directly with the Product concept. The foreign key to TB_C…_

2. _Business concept 'Product' — The table contains a product master record with product ID, SKU, product name, category, unit price, and active status, which aligns directly with the Product concept. The…_

3. _Each line item: The table contains line-level order detail fields such as ORDER_ID, PRODUCT_ID, QUANTITY, UNIT_PRICE, and LINE_AMT, which match the business concept describing individual product purch…_

---

### ✅ Q008 — How can I find all orders placed by a specific customer?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.1428 | **Gate:** `proceed_with_warning`

**Expected answer:**
> Query the SALES_ORDER_HDR table filtering by CUST_ID. Each order has a foreign key reference to CUSTOMER_MASTER.CUST_ID, so joining these tables on CUST_ID will show all orders for a customer along with their details.

**System answer:**
> The retrieved context describes database schema metadata, not live order records, so it cannot show the actual orders for a specific customer. It does show exactly how to find them.

Use SALES_ORDER_HDR as the order table. It implements the SalesOrder concept and contains ORDER_ID, CUST_ID, ORDER_DATE, TOTAL_AMT, STATUS_CODE, PAYMENT_CONFIRMED_AT, DELIVERED_AT, and CREATED_AT.

To find all orders …

**Sources retrieved (12):** `parent_chunk_data_dictionary.txt_3`, `parent_chunk_business_glossary.txt_2`, `parent_chunk_business_glossary.txt_0`, `Sales Order Header→SALES_ORDER_HDR`, `parent_chunk_data_dictionary.txt_4`, `SALES_ORDER_HDR→CUSTOMER_MASTER`, `parent_chunk_business_glossary.txt_1`, `Master record for all registered platform customers→CUSTOMER_MASTER`

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
> The provided context does not contain actual order records, so it cannot determine which products were included in any specific order.

What is known from the context is the schema needed to answer that question if data were available: ORDER_LINE_ITEM stores the line-level products for an order, with ORDER_ID, PRODUCT_ID, QUANTITY, UNIT_PRICE, and LINE_AMT. ORDER_LINE_ITEM belongs to exactly one s…

**Sources retrieved (12):** `parent_chunk_data_dictionary.txt_4`, `parent_chunk_business_glossary.txt_1`, `Each line item`, `Product`, `ORDER_LINE_ITEM→TB_PRODUCT`, `Each line item→ORDER_LINE_ITEM`, `parent_chunk_business_glossary.txt_0`, `parent_chunk_data_dictionary.txt_3`

**Context previews (first 3):**

1. _**Foreign Keys**: - CUST_ID → CUSTOMER_MASTER(CUST_ID) **Business Concept Mapping**: SalesOrder ──────────────────────────────────────────────────────────── ORDER_LINE_ITEM ───────────────────────────…_

2. _**Business Context**: Line items break down orders into individual product purchases. Each captures the price at the moment of ordering. **Key Attributes**: - Unique line identifier - References exact…_

3. _Each line item: The table contains line-level order detail fields such as ORDER_ID, PRODUCT_ID, QUANTITY, UNIT_PRICE, and LINE_AMT, which match the business concept describing individual product purch…_

---

### ✅ Q010 — Show me the order hierarchy from customer to line items.

**Status:** GROUNDED  
**GT Coverage:** 75% | **Top Score:** 0.3719 | **Gate:** `proceed`

**Expected answer:**
> The hierarchy is: Customer (CUSTOMER_MASTER) → SalesOrder (SALES_ORDER_HDR) → OrderLineItem (ORDER_LINE_ITEM) → Product (TB_PRODUCT). Each customer has orders, each order has line items, and each line item references a product.

**System answer:**
> The order hierarchy is:

Customer → Sales Order → Order Line Item.

In the physical schema, that is CUSTOMER_MASTER → SALES_ORDER_HDR → ORDER_LINE_ITEM.

The join path is:
CUSTOMER_MASTER.CUST_ID = SALES_ORDER_HDR.CUST_ID
and
SALES_ORDER_HDR.ORDER_ID = ORDER_LINE_ITEM.ORDER_ID.

From the business relationships in the context, a Sales Order is placed by exactly one Customer, and a Sales Order has o…

**Sources retrieved (12):** `parent_chunk_business_glossary.txt_2`, `parent_chunk_data_dictionary.txt_4`, `Each line item`, `parent_chunk_business_glossary.txt_1`, `ORDER_LINE_ITEM→TB_PRODUCT`, `ORDER_LINE_ITEM→SALES_ORDER_HDR`, `parent_chunk_business_glossary.txt_0`, `parent_chunk_data_dictionary.txt_3`

**Context previews (first 3):**

1. _Sales Order Relationships: - A Sales Order is placed by exactly one Customer - A Sales Order has one or more Order Line Items - A Sales Order has one or more Payments - A Sales Order has one or more S…_

2. _**Foreign Keys**: - CUST_ID → CUSTOMER_MASTER(CUST_ID) **Business Concept Mapping**: SalesOrder ──────────────────────────────────────────────────────────── ORDER_LINE_ITEM ───────────────────────────…_

3. _Each line item: The table contains line-level order detail fields such as ORDER_ID, PRODUCT_ID, QUANTITY, UNIT_PRICE, and LINE_AMT, which match the business concept describing individual product purch…_

---

### ✅ Q011 — What happens when a payment is confirmed for an order?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.3521 | **Gate:** `proceed`

**Expected answer:**
> When payment is confirmed, the PAYMENT record's STATUS_CODE becomes 'CONFIRMED', the CONFIRMED_AT timestamp is set, and the associated SALES_ORDER_HDR can progress from PENDING to CONFIRMED status.

**System answer:**
> When a payment is confirmed, the confirmation is represented in the schema by the payment’s lifecycle fields in PAYMENT: the payment has a STATUS_CODE and a CONFIRMED_AT timestamp, and it is tied to the order through PAYMENT.ORDER_ID = SALES_ORDER_HDR.ORDER_ID.

At the order level, SALES_ORDER_HDR also contains a PAYMENT_CONFIRMED_AT column, so the order header can store when payment was confirmed…

**Sources retrieved (12):** `parent_chunk_business_glossary.txt_1`, `Monetary Transaction→PAYMENT`, `Sales Order Header→SALES_ORDER_HDR`, `PAYMENT→SALES_ORDER_HDR`, `parent_chunk_data_dictionary.txt_4`, `parent_chunk_business_glossary.txt_0`, `parent_chunk_business_glossary.txt_2`, `parent_chunk_data_dictionary.txt_3`

**Context previews (first 3):**

1. _**Business Context**: Line items break down orders into individual product purchases. Each captures the price at the moment of ordering. **Key Attributes**: - Unique line identifier - References exact…_

2. _Business concept 'Monetary Transaction' — The table records a payment tied to a sales order via ORDER_ID, with amount, method, status, and confirmation timestamp, which matches the concept of the mone…_

3. _Business concept 'Sales Order Header' — The table name and structure indicate a header-level order record with order ID, customer reference, order date, total amount, status, and fulfillment timestamp…_

---

### ✅ Q012 — How are shipments related to orders and warehouses?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.8749 | **Gate:** `proceed`

**Expected answer:**
> Each shipment is for exactly one sales order (ORDER_ID in SHIPMENT references SALES_ORDER_HDR). The shipment also specifies the source warehouse code and includes tracking information and delivery status.

**System answer:**
> Shipments are related to orders and warehouses through the Shipment concept implemented by the SHIPMENT table.

A shipment is for exactly one Sales Order, and a Sales Order has one or more Shipments. At the schema level, this is represented by SHIPMENT.ORDER_ID referencing SALES_ORDER_HDR.ORDER_ID.

A shipment also comes from exactly one Warehouse. In the SHIPMENT table, the warehouse linkage is r…

**Sources retrieved (12):** `Shipment→SHIPMENT`, `parent_chunk_business_glossary.txt_2`, `parent_chunk_business_glossary.txt_0`, `parent_chunk_business_glossary.txt_1`, `parent_chunk_data_dictionary.txt_4`, `Product`, `Monetary Transaction→PAYMENT`, `Shipment`

**Context previews (first 3):**

1. _Business concept 'Shipment' — The table name, primary key SHIPMENT_ID, and shipment-specific columns like ORDER_ID, WAREHOUSE_CODE, SHIPPED_AT, TRACKING_NUMBER, and STATUS_CODE align directly with the…_

2. _Sales Order Relationships: - A Sales Order is placed by exactly one Customer - A Sales Order has one or more Order Line Items - A Sales Order has one or more Payments - A Sales Order has one or more S…_

3. _# Business Glossary - E-Commerce Domain (Simplified)  This document defines the core business concepts for the e-commerce platform test dataset.  ──────────────────────────────────────────────────────…_

---

### ✅ Q013 — Can a product belong to multiple categories?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.3613 | **Gate:** `proceed`

**Expected answer:**
> No, each product belongs to exactly one category. The TB_PRODUCT table has a CATEGORY_ID foreign key referencing TB_CATEGORY, which stores a single category value per product.

**System answer:**
> Based on the retrieved context, no: in this schema a product belongs to one category, not multiple categories.

The evidence is that TB_PRODUCT is defined with a single CATEGORY_ID column, and there is a foreign key relationship TB_PRODUCT.CATEGORY_ID → TB_CATEGORY.CATEGORY_ID. There is no junction table or additional category-mapping structure shown that would allow one product to be assigned to …

**Sources retrieved (12):** `parent_chunk_business_glossary.txt_0`, `Product`, `TB_PRODUCT→TB_CATEGORY`, `Product→TB_PRODUCT`, `parent_chunk_business_glossary.txt_1`, `parent_chunk_data_dictionary.txt_3`, `parent_chunk_data_dictionary.txt_4`, `Each line item→ORDER_LINE_ITEM`

**Context previews (first 3):**

1. _# Business Glossary - E-Commerce Domain (Simplified)  This document defines the core business concepts for the e-commerce platform test dataset.  ──────────────────────────────────────────────────────…_

2. _Product: The table contains a product master record with product ID, SKU, product name, category, unit price, and active status, which aligns directly with the Product concept. The foreign key to TB_C…_

3. _Relationship: TB_PRODUCT references TB_CATEGORY via foreign key CATEGORY_ID -> TB_CATEGORY.CATEGORY_ID.…_

---

### ✅ Q014 — Is it possible for a customer to place an order without payment?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0719 | **Gate:** `proceed_with_warning`

**Expected answer:**
> Yes, an order can exist without payment. SALES_ORDER_HDR has STATUS_CODE defaulting to PENDING and PAYMENT_CONFIRMED_AT is nullable (NULL when no payment yet). The PAYMENT table links via ORDER_ID foreign key but nothing prevents an order from existing without a payment row. However, the business gl…

**System answer:**
> Based on the retrieved context, no: the model does not allow a sales order to exist without payment.

The key rule is in the Sales Order relationships: a Sales Order “has one or more Payments,” and the Payment relationship says “A Payment is for exactly one Sales Order.” At the schema level, this is implemented through PAYMENT.ORDER_ID → SALES_ORDER_HDR.ORDER_ID.

So, in this data model, if a cust…

**Sources retrieved (12):** `parent_chunk_data_dictionary.txt_3`, `parent_chunk_business_glossary.txt_1`, `parent_chunk_business_glossary.txt_2`, `parent_chunk_business_glossary.txt_0`, `parent_chunk_data_dictionary.txt_4`, `Monetary Transaction→PAYMENT`, `Sales Order Header→SALES_ORDER_HDR`, `PAYMENT→SALES_ORDER_HDR`

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
> The retrieved context does not provide actual order records or customer-specific amounts, so the total value of all orders placed by a customer cannot be determined from the knowledge graph.

What is known from the context is the schema needed to calculate it. The header-level order table is SALES_ORDER_HDR, which contains ORDER_ID, CUST_ID, and TOTAL_AMT. A customer is stored in CUSTOMER_MASTER w…

**Sources retrieved (12):** `parent_chunk_business_glossary.txt_1`, `parent_chunk_business_glossary.txt_0`, `Sales Order Header→SALES_ORDER_HDR`, `parent_chunk_data_dictionary.txt_3`, `parent_chunk_business_glossary.txt_2`, `parent_chunk_data_dictionary.txt_4`, `Monetary Transaction→PAYMENT`, `Master record for all registered platform customers→CUSTOMER_MASTER`

**Context previews (first 3):**

1. _**Business Context**: Line items break down orders into individual product purchases. Each captures the price at the moment of ordering. **Key Attributes**: - Unique line identifier - References exact…_

2. _# Business Glossary - E-Commerce Domain (Simplified)  This document defines the core business concepts for the e-commerce platform test dataset.  ──────────────────────────────────────────────────────…_

3. _Business concept 'Sales Order Header' — The table name and structure indicate a header-level order record with order ID, customer reference, order date, total amount, status, and fulfillment timestamp…_

---

## Anomalies & Observations

No anomalies detected. All questions grounded with acceptable RAGAS scores.
