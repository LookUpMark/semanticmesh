# AB-01 — 01_basics_ecommerce — Run Analysis

**Timestamp:** 2026-03-30 21:15:57  
**Run tag:** `v5`

## Configuration

| Parameter | Value |
|-----------|-------|
| Extraction model | `LLM (gpt-5.4-nano-2026-03-17)` |
| Reasoning model | `gpt-5.4-2026-03-05` |
| Embedding model | `BAAI/bge-m3` |
| Retrieval mode | `vector` |
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
| Avg GT Coverage | 68% |
| Avg Top Score | 0.1878 |
| Avg Chunk Count | 5.0 |
| Abstained | 0 |

## RAGAS Metrics

RAGAS evaluation not enabled for this run.

## Per-Question Deep Dive

### ✅ Q001 — What information is stored for each customer?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.5624 | **Gate:** `proceed`

**Expected answer:**
> Each customer has a unique ID, full name, email address, geographic region code, creation date, and active status. The email must be unique across all customers.

**System answer:**
> For each customer, the Customer Master stores the core customer identity attributes: full name, email, region, creation timestamp, and active status. It represents the master record for registered platform customers.

**Sources retrieved (5):** `Shipment`, `Customer Master`, `Sales Order Header`, `Order Payment`, `Hierarchical product category tree`

**Context previews (first 3):**

1. _Shipment: The table name, primary key, shipped timestamp, tracking number, warehouse code, and shipment status all align directly with the business concept of a shipment. The foreign key to SALES_ORDE…_

2. _Customer Master: The table stores core customer identity attributes such as full name, email, region, creation timestamp, and active status, which aligns directly with the master record for registered…_

3. _Sales Order Header: The table name and structure indicate it is the header-level record for an order, with order ID, customer ID, order date, total amount, and status timestamps. This aligns most dire…_

---

### ✅ Q002 — How are products categorized on the platform?

**Status:** GROUNDED  
**GT Coverage:** 50% | **Top Score:** 0.0116 | **Gate:** `proceed_with_warning`

**Expected answer:**
> Products belong to categories which can have a parent category, forming a hierarchical tree structure. Each product references exactly one category through its CATEGORY_ID.

**System answer:**
> Products are categorized through a hierarchical product category tree. The retrieved context does not provide further schema details such as the table name, category levels, parent-child columns, or how products link to categories, so only this high-level categorization approach is available.

**Sources retrieved (5):** `Shipment`, `Customer Master`, `Hierarchical product category tree`, `Sales Order Header`, `Order Payment`

**Context previews (first 3):**

1. _Shipment: The table name, primary key, shipped timestamp, tracking number, warehouse code, and shipment status all align directly with the business concept of a shipment. The foreign key to SALES_ORDE…_

2. _Customer Master: The table stores core customer identity attributes such as full name, email, region, creation timestamp, and active status, which aligns directly with the master record for registered…_

3. _Hierarchical product category tree…_

---

### ✅ Q003 — What is the relationship between customers and sales orders?

**Status:** GROUNDED  
**GT Coverage:** 75% | **Top Score:** 0.0645 | **Gate:** `proceed_with_warning`

**Expected answer:**
> Each sales order is placed by exactly one customer, referenced through the CUST_ID foreign key. A customer can place zero or more orders over time.

**System answer:**
> The relationship is that customers are represented by Customer Master, and sales orders are represented by Sales Order Header. The Sales Order Header includes CUSTOMER_ID, which ties each order header to a customer master record.

From the context, this means a sales order belongs to a customer via CUSTOMER_ID, with Customer Master holding the core customer identity attributes and Sales Order Head…

**Sources retrieved (5):** `Shipment`, `Sales Order Header`, `Order Payment`, `Customer Master`, `Hierarchical product category tree`

**Context previews (first 3):**

1. _Shipment: The table name, primary key, shipped timestamp, tracking number, warehouse code, and shipment status all align directly with the business concept of a shipment. The foreign key to SALES_ORDE…_

2. _Sales Order Header: The table name and structure indicate it is the header-level record for an order, with order ID, customer ID, order date, total amount, and status timestamps. This aligns most dire…_

3. _Order Payment: The table is explicitly scoped to a sales order through ORDER_ID and captures payment method, amount, status, and confirmation time, which matches an order-settlement record. This is mo…_

---

### ✅ Q004 — What does an order line item contain?

**Status:** GROUNDED  
**GT Coverage:** 50% | **Top Score:** 0.3072 | **Gate:** `proceed`

**Expected answer:**
> An order line item specifies a product, the quantity ordered, the unit price at time of purchase, and the calculated extended amount. Each line item belongs to exactly one sales order.

**System answer:**
> The retrieved context does not define an order line item or list any line-item columns.

What it does provide is the related distinction that Sales Order Header is the header-level record for each customer sales order, with order ID, customer ID, order date, total amount, and status timestamps, and that this concept is explicitly described as being the header record rather than line items. The con…

**Sources retrieved (5):** `Shipment`, `Sales Order Header`, `Order Payment`, `Customer Master`, `Hierarchical product category tree`

**Context previews (first 3):**

1. _Shipment: The table name, primary key, shipped timestamp, tracking number, warehouse code, and shipment status all align directly with the business concept of a shipment. The foreign key to SALES_ORDE…_

2. _Sales Order Header: The table name and structure indicate it is the header-level record for an order, with order ID, customer ID, order date, total amount, and status timestamps. This aligns most dire…_

3. _Order Payment: The table is explicitly scoped to a sales order through ORDER_ID and captures payment method, amount, status, and confirmation time, which matches an order-settlement record. This is mo…_

---

### ✅ Q005 — How are payments linked to orders?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.4721 | **Gate:** `proceed`

**Expected answer:**
> Each payment is associated with exactly one sales order through the ORDER_ID foreign key. Payments track the payment method, amount, status, and confirmation timestamp.

**System answer:**
> Payments are linked to orders through the Order Payment table’s ORDER_ID. The retrieved context says Order Payment is explicitly scoped to a sales order through ORDER_ID and stores payment method, amount, status, and confirmation time. The corresponding order record is the Sales Order Header, which is the header-level record for each customer sales order and includes the order ID. So, at the schem…

**Sources retrieved (5):** `Shipment`, `Order Payment`, `Sales Order Header`, `Customer Master`, `Hierarchical product category tree`

**Context previews (first 3):**

1. _Shipment: The table name, primary key, shipped timestamp, tracking number, warehouse code, and shipment status all align directly with the business concept of a shipment. The foreign key to SALES_ORDE…_

2. _Order Payment: The table is explicitly scoped to a sales order through ORDER_ID and captures payment method, amount, status, and confirmation time, which matches an order-settlement record. This is mo…_

3. _Sales Order Header: The table name and structure indicate it is the header-level record for an order, with order ID, customer ID, order date, total amount, and status timestamps. This aligns most dire…_

---

### ✅ Q006 — What statuses can an order have?

**Status:** GROUNDED  
**GT Coverage:** 50% | **Top Score:** 0.2355 | **Gate:** `proceed`

**Expected answer:**
> Orders can have one of five statuses defined via CHECK constraint on SALES_ORDER_HDR.STATUS_CODE: PENDING (initial state when order is created), CONFIRMED (payment has been received), SHIPPED (dispatched to customer), DELIVERED (received by customer), or CANCELLED. The business glossary describes th…

**System answer:**
> The retrieved context indicates that the Sales Order Header includes status-related timestamps, so an order does have status tracking at the header level. However, the specific order status values are not provided in the context.

Related status-bearing concepts in the context are:
The Sales Order Header, which has status timestamps.
The Order Payment, which captures a payment status.
The Shipment…

**Sources retrieved (5):** `Shipment`, `Sales Order Header`, `Order Payment`, `Customer Master`, `Hierarchical product category tree`

**Context previews (first 3):**

1. _Shipment: The table name, primary key, shipped timestamp, tracking number, warehouse code, and shipment status all align directly with the business concept of a shipment. The foreign key to SALES_ORDE…_

2. _Sales Order Header: The table name and structure indicate it is the header-level record for an order, with order ID, customer ID, order date, total amount, and status timestamps. This aligns most dire…_

3. _Order Payment: The table is explicitly scoped to a sales order through ORDER_ID and captures payment method, amount, status, and confirmation time, which matches an order-settlement record. This is mo…_

---

### ✅ Q007 — Which table stores the product SKU information?

**Status:** GROUNDED  
**GT Coverage:** 50% | **Top Score:** 0.0856 | **Gate:** `proceed_with_warning`

**Expected answer:**
> The TB_PRODUCT table stores the SKU (Stock Keeping Unit) code for each product, along with product name, category, price, and active status.

**System answer:**
> From the retrieved context, this cannot be determined. The context only identifies tables or concepts for Customer Master, Shipment, Sales Order Header, and Order Payment, plus a business concept for a hierarchical product category tree. It does not mention any table or column for product SKU information, so no supported table name can be given.

**Sources retrieved (5):** `Customer Master`, `Hierarchical product category tree`, `Shipment`, `Sales Order Header`, `Order Payment`

**Context previews (first 3):**

1. _Customer Master: The table stores core customer identity attributes such as full name, email, region, creation timestamp, and active status, which aligns directly with the master record for registered…_

2. _Hierarchical product category tree…_

3. _Shipment: The table name, primary key, shipped timestamp, tracking number, warehouse code, and shipment status all align directly with the business concept of a shipment. The foreign key to SALES_ORDE…_

---

### ✅ Q008 — How can I find all orders placed by a specific customer?

**Status:** GROUNDED  
**GT Coverage:** 75% | **Top Score:** 0.0206 | **Gate:** `proceed_with_warning`

**Expected answer:**
> Query the SALES_ORDER_HDR table filtering by CUST_ID. Each order has a foreign key reference to CUSTOMER_MASTER.CUST_ID, so joining these tables on CUST_ID will show all orders for a customer along with their details.

**System answer:**
> Use Sales Order Header. The retrieved context says this table is the header-level record for each customer sales order and includes order ID, customer ID, order date, total amount, and status timestamps. So to find all orders placed by a specific customer, filter Sales Order Header by the customer ID for that customer.

If you need customer-identifying attributes to determine which customer to loo…

**Sources retrieved (5):** `Shipment`, `Sales Order Header`, `Customer Master`, `Order Payment`, `Hierarchical product category tree`

**Context previews (first 3):**

1. _Shipment: The table name, primary key, shipped timestamp, tracking number, warehouse code, and shipment status all align directly with the business concept of a shipment. The foreign key to SALES_ORDE…_

2. _Sales Order Header: The table name and structure indicate it is the header-level record for an order, with order ID, customer ID, order date, total amount, and status timestamps. This aligns most dire…_

3. _Customer Master: The table stores core customer identity attributes such as full name, email, region, creation timestamp, and active status, which aligns directly with the master record for registered…_

---

### ✅ Q009 — What products were included in a specific order?

**Status:** GROUNDED  
**GT Coverage:** 33% | **Top Score:** 0.0178 | **Gate:** `proceed_with_warning`

**Expected answer:**
> Join ORDER_LINE_ITEM with TB_PRODUCT on PRODUCT_ID. For order ORDER_ID, the line items show which products were ordered, in what quantity, and at what price.

**System answer:**
> I cannot determine what products were included in a specific order from the retrieved context.

The context contains schema-level business concepts only, not operational order records. It identifies Sales Order Header as the header record for each customer sales order, with order ID, customer ID, order date, total amount, and status timestamps, and it identifies related concepts such as Order Paym…

**Sources retrieved (5):** `Shipment`, `Order Payment`, `Sales Order Header`, `Customer Master`, `Hierarchical product category tree`

**Context previews (first 3):**

1. _Shipment: The table name, primary key, shipped timestamp, tracking number, warehouse code, and shipment status all align directly with the business concept of a shipment. The foreign key to SALES_ORDE…_

2. _Order Payment: The table is explicitly scoped to a sales order through ORDER_ID and captures payment method, amount, status, and confirmation time, which matches an order-settlement record. This is mo…_

3. _Sales Order Header: The table name and structure indicate it is the header-level record for an order, with order ID, customer ID, order date, total amount, and status timestamps. This aligns most dire…_

---

### ✅ Q010 — Show me the order hierarchy from customer to line items.

**Status:** GROUNDED  
**GT Coverage:** 75% | **Top Score:** 0.1188 | **Gate:** `proceed_with_warning`

**Expected answer:**
> The hierarchy is: Customer (CUSTOMER_MASTER) → SalesOrder (SALES_ORDER_HDR) → OrderLineItem (ORDER_LINE_ITEM) → Product (TB_PRODUCT). Each customer has orders, each order has line items, and each line item references a product.

**System answer:**
> From the retrieved context, I can only show the hierarchy partially.

The known customer-to-order portion is:

Customer Master → Sales Order Header

This is supported by the fact that Customer Master is the master record for registered customers, and Sales Order Header is the header-level record for each customer sales order and includes customer ID. So, at the schema/business-concept level, the o…

**Sources retrieved (5):** `Shipment`, `Sales Order Header`, `Customer Master`, `Order Payment`, `Hierarchical product category tree`

**Context previews (first 3):**

1. _Shipment: The table name, primary key, shipped timestamp, tracking number, warehouse code, and shipment status all align directly with the business concept of a shipment. The foreign key to SALES_ORDE…_

2. _Sales Order Header: The table name and structure indicate it is the header-level record for an order, with order ID, customer ID, order date, total amount, and status timestamps. This aligns most dire…_

3. _Customer Master: The table stores core customer identity attributes such as full name, email, region, creation timestamp, and active status, which aligns directly with the master record for registered…_

---

### ✅ Q011 — What happens when a payment is confirmed for an order?

**Status:** GROUNDED  
**GT Coverage:** 75% | **Top Score:** 0.3259 | **Gate:** `proceed`

**Expected answer:**
> When payment is confirmed, the PAYMENT record's STATUS_CODE becomes 'CONFIRMED', the CONFIRMED_AT timestamp is set, and the associated SALES_ORDER_HDR can progress from PENDING to CONFIRMED status.

**System answer:**
> From the retrieved context, when a payment is confirmed for an order, the confirmation is recorded in the Order Payment business concept for that specific sales order via ORDER_ID. That record captures the payment method, amount, status, and confirmation time, so a confirmed payment means the order-level payment record has an updated status and a populated confirmation timestamp.

The payment is t…

**Sources retrieved (5):** `Shipment`, `Order Payment`, `Sales Order Header`, `Customer Master`, `Hierarchical product category tree`

**Context previews (first 3):**

1. _Shipment: The table name, primary key, shipped timestamp, tracking number, warehouse code, and shipment status all align directly with the business concept of a shipment. The foreign key to SALES_ORDE…_

2. _Order Payment: The table is explicitly scoped to a sales order through ORDER_ID and captures payment method, amount, status, and confirmation time, which matches an order-settlement record. This is mo…_

3. _Sales Order Header: The table name and structure indicate it is the header-level record for an order, with order ID, customer ID, order date, total amount, and status timestamps. This aligns most dire…_

---

### ✅ Q012 — How are shipments related to orders and warehouses?

**Status:** GROUNDED  
**GT Coverage:** 75% | **Top Score:** 0.5485 | **Gate:** `proceed`

**Expected answer:**
> Each shipment is for exactly one sales order (ORDER_ID in SHIPMENT references SALES_ORDER_HDR). The shipment also specifies the source warehouse code and includes tracking information and delivery status.

**System answer:**
> Shipments are related to orders through the Shipment table’s foreign key to SALES_ORDER_HDR, which indicates that a shipment represents the logistics side of fulfilling a sales order.

For warehouses, the retrieved context only supports that Shipment includes a warehouse code. It does not mention a Warehouse table or any explicit relationship from Shipment to a warehouse entity, so no stronger war…

**Sources retrieved (5):** `Shipment`, `Sales Order Header`, `Order Payment`, `Customer Master`, `Hierarchical product category tree`

**Context previews (first 3):**

1. _Shipment: The table name, primary key, shipped timestamp, tracking number, warehouse code, and shipment status all align directly with the business concept of a shipment. The foreign key to SALES_ORDE…_

2. _Sales Order Header: The table name and structure indicate it is the header-level record for an order, with order ID, customer ID, order date, total amount, and status timestamps. This aligns most dire…_

3. _Order Payment: The table is explicitly scoped to a sales order through ORDER_ID and captures payment method, amount, status, and confirmation time, which matches an order-settlement record. This is mo…_

---

### ✅ Q013 — Can a product belong to multiple categories?

**Status:** GROUNDED  
**GT Coverage:** 67% | **Top Score:** 0.0093 | **Gate:** `proceed_with_warning`

**Expected answer:**
> No, each product belongs to exactly one category. The TB_PRODUCT table has a CATEGORY_ID foreign key referencing TB_CATEGORY, which stores a single category value per product.

**System answer:**
> The retrieved context does not say whether a product can belong to multiple categories.

It only mentions the business concept "Hierarchical product category tree," which indicates that categories are organized in a hierarchy, but it does not provide any rule or schema detail about product-to-category assignment cardinality, such as one product to one category or one product to many categories.

**Sources retrieved (5):** `Hierarchical product category tree`, `Customer Master`, `Shipment`, `Sales Order Header`, `Order Payment`

**Context previews (first 3):**

1. _Hierarchical product category tree…_

2. _Customer Master: The table stores core customer identity attributes such as full name, email, region, creation timestamp, and active status, which aligns directly with the master record for registered…_

3. _Shipment: The table name, primary key, shipped timestamp, tracking number, warehouse code, and shipment status all align directly with the business concept of a shipment. The foreign key to SALES_ORDE…_

---

### ✅ Q014 — Is it possible for a customer to place an order without payment?

**Status:** GROUNDED  
**GT Coverage:** 75% | **Top Score:** 0.0134 | **Gate:** `proceed_with_warning`

**Expected answer:**
> Yes, an order can exist without payment. SALES_ORDER_HDR has STATUS_CODE defaulting to PENDING and PAYMENT_CONFIRMED_AT is nullable (NULL when no payment yet). The PAYMENT table links via ORDER_ID foreign key but nothing prevents an order from existing without a payment row. However, the business gl…

**System answer:**
> The retrieved context does not provide enough information to determine whether a customer can place an order without payment.

What is known from the context is that Sales Order Header is the header-level record for each customer sales order and includes order ID, customer ID, order date, total amount, and status timestamps. It also shows that Order Payment is a separate order-scoped record linked…

**Sources retrieved (5):** `Shipment`, `Order Payment`, `Sales Order Header`, `Customer Master`, `Hierarchical product category tree`

**Context previews (first 3):**

1. _Shipment: The table name, primary key, shipped timestamp, tracking number, warehouse code, and shipment status all align directly with the business concept of a shipment. The foreign key to SALES_ORDE…_

2. _Order Payment: The table is explicitly scoped to a sales order through ORDER_ID and captures payment method, amount, status, and confirmation time, which matches an order-settlement record. This is mo…_

3. _Sales Order Header: The table name and structure indicate it is the header-level record for an order, with order ID, customer ID, order date, total amount, and status timestamps. This aligns most dire…_

---

### ✅ Q015 — What is the total value of all orders placed by a customer?

**Status:** GROUNDED  
**GT Coverage:** 75% | **Top Score:** 0.0236 | **Gate:** `proceed_with_warning`

**Expected answer:**
> Sum the TOTAL_AMT column from SALES_ORDER_HDR for all records where CUST_ID matches the customer's ID. This aggregates the monetary value of all orders placed by that customer.

**System answer:**
> The retrieved context does not provide actual order records or customer-specific values, so the total value of all orders placed by a customer cannot be determined from this knowledge graph.

What is known is the schema-level structure: the business concept Sales Order Header is the header-level record for each customer sales order and includes order ID, customer ID, order date, total amount, and …

**Sources retrieved (5):** `Shipment`, `Sales Order Header`, `Customer Master`, `Order Payment`, `Hierarchical product category tree`

**Context previews (first 3):**

1. _Shipment: The table name, primary key, shipped timestamp, tracking number, warehouse code, and shipment status all align directly with the business concept of a shipment. The foreign key to SALES_ORDE…_

2. _Sales Order Header: The table name and structure indicate it is the header-level record for an order, with order ID, customer ID, order date, total amount, and status timestamps. This aligns most dire…_

3. _Customer Master: The table stores core customer identity attributes such as full name, email, region, creation timestamp, and active status, which aligns directly with the master record for registered…_

---

## Anomalies & Observations

No anomalies detected. All questions grounded with acceptable RAGAS scores.
