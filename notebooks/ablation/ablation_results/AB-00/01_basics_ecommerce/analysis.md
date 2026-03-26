# AB-00 — 01_basics_ecommerce — Run Analysis

**Timestamp:** 2026-03-26 18:34:38  
**Run tag:** `run-20260326_192305`

## Configuration

| Parameter | Value |
|-----------|-------|
| Extraction model | `LLM (gpt-5.4-nano)` |
| Reasoning model | `gpt-5.4-mini` |
| Embedding model | `BAAI/bge-m3` |
| Retrieval mode | `hybrid` |
| Reranker | `True` |
| Reranker top_k | `10` |
| Chunk size / overlap | `256 / 32` |
| ER similarity threshold | `0.75` |

## Builder Results

| Metric | Value |
|--------|-------|
| Triplets extracted | 319 |
| Entities resolved | 65 |
| Tables parsed | 7 |
| Tables completed | 7 |

## Query Evaluation Summary

| Metric | Value |
|--------|-------|
| Questions | 15 |
| Grounded | **15/15 (100%)** |
| Avg GT Coverage | 64% |
| Avg Top Score | 0.4792 |
| Avg Chunk Count | 10.0 |
| Abstained | 0 |

## RAGAS Metrics

| Metric | Value | Interpretation |
|--------|-------|----------------|
| Faithfulness | **1.0000** | Answers grounded in context |
| Answer Relevancy | **0.5298** | Answers relevant to question |
| Context Precision | **0.7062** | Retrieved chunks are on-topic |
| Context Recall | **0.8333** | All needed context retrieved |

## Per-Question Deep Dive

### ✅ Q001 — What information is stored for each customer?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.3616 | **Gate:** `proceed`

**Expected answer:**
> Each customer has a unique ID, full name, email address, geographic region code, creation date, and active status. The email must be unique across all customers.

**System answer:**
> The context only says that CUSTOMER_MASTER stores the master record for all registered platform customers, with CUST_ID as the primary key. It does not provide further details on what customer information is stored, so I cannot be more specific.

**RAGAS scores:**

| f | ar | cp | cr |
|---|----|----|-----|
| 1.00 | 0.00 | 0.12 | 0.00 |

**Sources retrieved (10):** `chunk_2`, `Sales Order`, `Shipment`, `chunk_5`, `chunk_4`, `SALES_ORDER_HDR→CUSTOMER_MASTER`, `the customer, items, payment status, and delivery information`, `chunk_0`

**Context previews (first 3):**

1. _**Foreign Keys**: - PARENT_CATEGORY_ID → TB_CATEGORY(CATEGORY_ID) [self-reference] **Business Concept Mapping**: Category ──────────────────────────────────────────────────────────── SALES_ORDER_HDR ─…_

2. _Sales Order: The table name, primary key ORDER_ID, customer foreign key, order date, total amount, and fulfillment/payment status fields align directly with a sales order header record. The business e…_

3. _Shipment: The table name, primary key SHIPMENT_ID, foreign key to SALES_ORDER_HDR, and shipping-related attributes (WAREHOUSE_CODE, SHIPPED_AT, TRACKING_NUMBER, STATUS_CODE) directly indicate a shipme…_

---

### ✅ Q002 — How are products categorized on the platform?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.3543 | **Gate:** `proceed`

**Expected answer:**
> Products belong to categories which can have a parent category, forming a hierarchical tree structure. Each product references exactly one category through its CATEGORY_ID.

**System answer:**
> Products are categorized using the TB_CATEGORY table. The context shows that TB_PRODUCT references TB_CATEGORY via CATEGORY_ID → TB_CATEGORY.CATEGORY_ID, and TB_CATEGORY also has a self-reference through PARENT_CATEGORY_ID → TB_CATEGORY(CATEGORY_ID), indicating a hierarchical product category tree.

**RAGAS scores:**

| f | ar | cp | cr |
|---|----|----|-----|
| 1.00 | 0.56 | 0.45 | 1.00 |

**Sources retrieved (10):** `chunk_3`, `chunk_2`, `chunk_1`, `chunk_0`, `chunk_6`, `TB_PRODUCT→TB_CATEGORY`, `ORDER_LINE_ITEM→TB_PRODUCT`, `Order Line Item`

**Context previews (first 3):**

1. _**Foreign Keys**: - CUST_ID → CUSTOMER_MASTER(CUST_ID) **Business Concept Mapping**: SalesOrder ──────────────────────────────────────────────────────────── ORDER_LINE_ITEM ───────────────────────────…_

2. _**Foreign Keys**: - PARENT_CATEGORY_ID → TB_CATEGORY(CATEGORY_ID) [self-reference] **Business Concept Mapping**: Category ──────────────────────────────────────────────────────────── SALES_ORDER_HDR ─…_

3. _**Examples**: - A new user registers and places their first order - An existing customer updates their shipping address ──────────────────────────────────────────────────────────── PRODUCT ───────────…_

---

### ✅ Q003 — What is the relationship between customers and sales orders?

**Status:** GROUNDED  
**GT Coverage:** 75% | **Top Score:** 0.9869 | **Gate:** `proceed`

**Expected answer:**
> Each sales order is placed by exactly one customer, referenced through the CUST_ID foreign key. A customer can place zero or more orders over time.

**System answer:**
> A Customer places zero or more Sales Orders. In the simplified schema, SALES_ORDER_HDR references CUSTOMER_MASTER via the foreign key CUST_ID.

**RAGAS scores:**

| f | ar | cp | cr |
|---|----|----|-----|
| 1.00 | 0.64 | 0.76 | 1.00 |

**Sources retrieved (10):** `chunk_6`, `chunk_5`, `chunk_2`, `Sales Order`, `chunk_4`, `chunk_3`, `SALES_ORDER_HDR→CUSTOMER_MASTER`, `chunk_0`

**Context previews (first 3):**

1. _Customer Relationships: - A Customer places zero or more Sales Orders - A Customer has one or more Customer Addresses (not in simplified schema) Product Relationships: - A Product belongs to exactly o…_

2. _**Business Context**: Shipments represent the logistics side of order fulfillment. They track what items were sent, when, and to whom. **Key Attributes**: - Unique Shipment ID - References exactly one…_

3. _──────────────────────────────────────────────────────────── SALES ORDER ──────────────────────────────────────────────────────────── **Definition**: A formal transaction document recording the agreem…_

---

### ✅ Q004 — What does an order line item contain?

**Status:** GROUNDED  
**GT Coverage:** 50% | **Top Score:** 0.9792 | **Gate:** `proceed`

**Expected answer:**
> An order line item specifies a product, the quantity ordered, the unit price at time of purchase, and the calculated extended amount. Each line item belongs to exactly one sales order.

**System answer:**
> An ORDER LINE ITEM contains a single product within a Sales Order, along with the quantity and unit price at the time of purchase. The context also indicates it has a line amount.

**RAGAS scores:**

| f | ar | cp | cr |
|---|----|----|-----|
| 1.00 | 0.87 | 1.00 | 1.00 |

**Sources retrieved (10):** `chunk_3`, `Order Line Item`, `ORDER_LINE_ITEM→TB_PRODUCT`, `ORDER_LINE_ITEM→SALES_ORDER_HDR`, `chunk_2`, `chunk_6`, `Sales Order`, `chunk_4`

**Context previews (first 3):**

1. _──────────────────────────────────────────────────────────── ORDER LINE ITEM ──────────────────────────────────────────────────────────── **Definition**: A single line within a Sales Order specifying …_

2. _Order Line Item: The table name and columns clearly represent individual product lines within a sales order, with foreign keys to SALES_ORDER_HDR and TB_PRODUCT. The presence of quantity, unit price, …_

3. _Relationship: ORDER_LINE_ITEM references TB_PRODUCT via foreign key PRODUCT_ID -> TB_PRODUCT.PRODUCT_ID.…_

---

### ✅ Q005 — How are payments linked to orders?

**Status:** GROUNDED  
**GT Coverage:** 67% | **Top Score:** 0.9232 | **Gate:** `proceed`

**Expected answer:**
> Each payment is associated with exactly one sales order through the ORDER_ID foreign key. Payments track the payment method, amount, status, and confirmation timestamp.

**System answer:**
> Payments are linked to orders through the PAYMENT table’s foreign key ORDER_ID, which references SALES_ORDER_HDR.ORDER_ID.

**RAGAS scores:**

| f | ar | cp | cr |
|---|----|----|-----|
| 1.00 | 0.91 | 0.74 | 0.50 |

**Sources retrieved (10):** `PAYMENT→SALES_ORDER_HDR`, `chunk_4`, `chunk_2`, `chunk_6`, `SHIPMENT→SALES_ORDER_HDR`, `chunk_3`, `chunk_5`, `ORDER_LINE_ITEM→SALES_ORDER_HDR`

**Context previews (first 3):**

1. _Relationship: PAYMENT references SALES_ORDER_HDR via foreign key ORDER_ID -> SALES_ORDER_HDR.ORDER_ID.…_

2. _──────────────────────────────────────────────────────────── PAYMENT ──────────────────────────────────────────────────────────── **Definition**: The monetary transaction that settles the total amount…_

3. _──────────────────────────────────────────────────────────── SALES ORDER ──────────────────────────────────────────────────────────── **Definition**: A formal transaction document recording the agreem…_

---

### ✅ Q006 — What statuses can an order have?

**Status:** GROUNDED  
**GT Coverage:** 0% | **Top Score:** 0.7018 | **Gate:** `proceed`

**Expected answer:**
> Orders can have one of five statuses: PENDING (initial state), CONFIRMED (payment received), SHIPPED (sent to customer), DELIVERED (received by customer), or CANCELLED.

**System answer:**
> The retrieved context shows that a Sales Order tracks “fulfillment/payment status,” and another business concept description says it tracks “payment status and delivery information,” but it does not list the actual status values an order can have. So I can confirm that order status exists in the Sales Order concept, but the specific statuses are not provided in the context.

**RAGAS scores:**

| f | ar | cp | cr |
|---|----|----|-----|
| 1.00 | 0.00 | 0.00 | 0.00 |

**Sources retrieved (10):** `chunk_2`, `chunk_5`, `Sales Order`, `chunk_4`, `Shipment`, `chunk_6`, `chunk_3`, `chunk_0`

**Context previews (first 3):**

1. _──────────────────────────────────────────────────────────── SALES ORDER ──────────────────────────────────────────────────────────── **Definition**: A formal transaction document recording the agreem…_

2. _**Business Context**: Shipments represent the logistics side of order fulfillment. They track what items were sent, when, and to whom. **Key Attributes**: - Unique Shipment ID - References exactly one…_

3. _Sales Order: The table name, primary key ORDER_ID, customer foreign key, order date, total amount, and fulfillment/payment status fields align directly with a sales order header record. The business e…_

---

### ✅ Q007 — Which table stores the product SKU information?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0324 | **Gate:** `proceed_with_warning`

**Expected answer:**
> The TB_PRODUCT table stores the SKU (Stock Keeping Unit) code for each product, along with product name, category, price, and active status.

**System answer:**
> The SKU information is stored in the TB_PRODUCT table, in the SKU column.

**RAGAS scores:**

| f | ar | cp | cr |
|---|----|----|-----|
| 1.00 | 0.75 | 0.88 | 1.00 |

**Sources retrieved (10):** `Order Line Item`, `ORDER_LINE_ITEM→TB_PRODUCT`, `chunk_1`, `TB_PRODUCT→TB_CATEGORY`, `Shipment`, `chunk_6`, `chunk_7`, `chunk_0`

**Context previews (first 3):**

1. _Order Line Item: The table name and columns clearly represent individual product lines within a sales order, with foreign keys to SALES_ORDER_HDR and TB_PRODUCT. The presence of quantity, unit price, …_

2. _Relationship: ORDER_LINE_ITEM references TB_PRODUCT via foreign key PRODUCT_ID -> TB_PRODUCT.PRODUCT_ID.…_

3. _**Primary Key**: PRODUCT_ID (INT, auto-increment) **Column Details**: | Column | Type | Description | Nullable | |--------|------|-------------|----------| | PRODUCT_ID | INT | Unique product identifi…_

---

### ✅ Q008 — How can I find all orders placed by a specific customer?

**Status:** GROUNDED  
**GT Coverage:** 75% | **Top Score:** 0.3604 | **Gate:** `proceed`

**Expected answer:**
> Query the SALES_ORDER_HDR table filtering by CUST_ID. Each order has a foreign key reference to CUSTOMER_MASTER.CUST_ID, so joining these tables on CUST_ID will show all orders for a customer along with their details.

**System answer:**
> You can find a customer’s orders by using the `SALES_ORDER_HDR` table and filtering on the foreign key `CUST_ID`, which references `CUSTOMER_MASTER(CUST_ID)`. The context says `SALES_ORDER_HDR` stores the sales order header and is linked to the customer through `CUST_ID -> CUSTOMER_MASTER.CUST_ID`.

**RAGAS scores:**

| f | ar | cp | cr |
|---|----|----|-----|
| 1.00 | 0.62 | 0.96 | 1.00 |

**Sources retrieved (10):** `chunk_2`, `chunk_6`, `Sales Order`, `chunk_3`, `SALES_ORDER_HDR→CUSTOMER_MASTER`, `chunk_4`, `chunk_5`, `chunk_0`

**Context previews (first 3):**

1. _**Foreign Keys**: - PARENT_CATEGORY_ID → TB_CATEGORY(CATEGORY_ID) [self-reference] **Business Concept Mapping**: Category ──────────────────────────────────────────────────────────── SALES_ORDER_HDR ─…_

2. _Customer Relationships: - A Customer places zero or more Sales Orders - A Customer has one or more Customer Addresses (not in simplified schema) Product Relationships: - A Product belongs to exactly o…_

3. _Sales Order: The table name, primary key ORDER_ID, customer foreign key, order date, total amount, and fulfillment/payment status fields align directly with a sales order header record. The business e…_

---

### ✅ Q009 — What products were included in a specific order?

**Status:** GROUNDED  
**GT Coverage:** 50% | **Top Score:** 0.0798 | **Gate:** `proceed_with_warning`

**Expected answer:**
> Join ORDER_LINE_ITEM with TB_PRODUCT on PRODUCT_ID. For order ORDER_ID, the line items show which products were ordered, in what quantity, and at what price.

**System answer:**
> The products included in a specific order are captured in the ORDER_LINE_ITEM table. It records each product line within a Sales Order, with a foreign key to TB_PRODUCT via PRODUCT_ID, along with quantity and unit price.

**RAGAS scores:**

| f | ar | cp | cr |
|---|----|----|-----|
| 1.00 | 0.71 | 0.83 | 1.00 |

**Sources retrieved (10):** `chunk_3`, `Order Line Item`, `chunk_2`, `ORDER_LINE_ITEM→TB_PRODUCT`, `Shipment`, `chunk_4`, `chunk_6`, `chunk_1`

**Context previews (first 3):**

1. _──────────────────────────────────────────────────────────── ORDER LINE ITEM ──────────────────────────────────────────────────────────── **Definition**: A single line within a Sales Order specifying …_

2. _Order Line Item: The table name and columns clearly represent individual product lines within a sales order, with foreign keys to SALES_ORDER_HDR and TB_PRODUCT. The presence of quantity, unit price, …_

3. _──────────────────────────────────────────────────────────── SALES ORDER ──────────────────────────────────────────────────────────── **Definition**: A formal transaction document recording the agreem…_

---

### ✅ Q010 — Show me the order hierarchy from customer to line items.

**Status:** GROUNDED  
**GT Coverage:** 25% | **Top Score:** 0.3215 | **Gate:** `proceed`

**Expected answer:**
> The hierarchy is: Customer (CUSTOMER_MASTER) → SalesOrder (SALES_ORDER_HDR) → OrderLineItem (ORDER_LINE_ITEM) → Product (TB_PRODUCT). Each customer has orders, each order has line items, and each line item references a product.

**System answer:**
> The order hierarchy is CUSTOMER_MASTER → SALES_ORDER_HDR → ORDER_LINE_ITEM.

From the retrieved context, CUSTOMER_MASTER.CUST_ID maps to SALES_ORDER_HDR.CUST_ID, and SALES_ORDER_HDR.ORDER_ID maps to ORDER_LINE_ITEM.ORDER_ID.

**RAGAS scores:**

| f | ar | cp | cr |
|---|----|----|-----|
| 1.00 | 0.67 | 0.55 | 1.00 |

**Sources retrieved (10):** `chunk_3`, `Order Line Item`, `ORDER_LINE_ITEM→TB_PRODUCT`, `chunk_2`, `ORDER_LINE_ITEM→SALES_ORDER_HDR`, `chunk_1`, `Sales Order`, `chunk_6`

**Context previews (first 3):**

1. _**Foreign Keys**: - CUST_ID → CUSTOMER_MASTER(CUST_ID) **Business Concept Mapping**: SalesOrder ──────────────────────────────────────────────────────────── ORDER_LINE_ITEM ───────────────────────────…_

2. _Order Line Item: The table name and columns clearly represent individual product lines within a sales order, with foreign keys to SALES_ORDER_HDR and TB_PRODUCT. The presence of quantity, unit price, …_

3. _Relationship: ORDER_LINE_ITEM references TB_PRODUCT via foreign key PRODUCT_ID -> TB_PRODUCT.PRODUCT_ID.…_

---

### ✅ Q011 — What happens when a payment is confirmed for an order?

**Status:** GROUNDED  
**GT Coverage:** 75% | **Top Score:** 0.5020 | **Gate:** `proceed`

**Expected answer:**
> When payment is confirmed, the PAYMENT record's STATUS_CODE becomes 'CONFIRMED', the CONFIRMED_AT timestamp is set, and the associated SALES_ORDER_HDR can progress from PENDING to CONFIRMED status.

**System answer:**
> When a payment is confirmed, the PAYMENT concept indicates that the monetary transaction settles the total amount due for the Sales Order, authorizing and transferring funds from the customer to the platform. The context also suggests it affects the order’s payment status, but that part is only partially stated in the retrieved text.

**RAGAS scores:**

| f | ar | cp | cr |
|---|----|----|-----|
| 1.00 | 0.67 | 0.83 | 1.00 |

**Sources retrieved (10):** `chunk_4`, `chunk_2`, `Sales Order`, `PAYMENT→SALES_ORDER_HDR`, `chunk_3`, `chunk_6`, `chunk_5`, `the customer, items, payment status, and delivery information`

**Context previews (first 3):**

1. _──────────────────────────────────────────────────────────── PAYMENT ──────────────────────────────────────────────────────────── **Definition**: The monetary transaction that settles the total amount…_

2. _──────────────────────────────────────────────────────────── SALES ORDER ──────────────────────────────────────────────────────────── **Definition**: A formal transaction document recording the agreem…_

3. _Sales Order: The table name, primary key ORDER_ID, customer foreign key, order date, total amount, and fulfillment/payment status fields align directly with a sales order header record. The business e…_

---

### ✅ Q012 — How are shipments related to orders and warehouses?

**Status:** GROUNDED  
**GT Coverage:** 75% | **Top Score:** 0.9047 | **Gate:** `proceed`

**Expected answer:**
> Each shipment is for exactly one sales order (ORDER_ID in SHIPMENT references SALES_ORDER_HDR). The shipment also specifies the source warehouse code and includes tracking information and delivery status.

**System answer:**
> Shipments are tied to orders through the Shipment entity/table: each shipment references exactly one Sales Order, via the SHIPMENT table and its foreign key to SALES_ORDER_HDR. Shipments also include a warehouse-related attribute, WAREHOUSE_CODE, which indicates the source warehouse.

**RAGAS scores:**

| f | ar | cp | cr |
|---|----|----|-----|
| 1.00 | 0.76 | 0.78 | 1.00 |

**Sources retrieved (10):** `chunk_5`, `Shipment`, `chunk_6`, `chunk_4`, `chunk_2`, `chunk_1`, `chunk_0`, `the customer, items, payment status, and delivery information`

**Context previews (first 3):**

1. _**Business Context**: Shipments represent the logistics side of order fulfillment. They track what items were sent, when, and to whom. **Key Attributes**: - Unique Shipment ID - References exactly one…_

2. _Shipment: The table name, primary key SHIPMENT_ID, foreign key to SALES_ORDER_HDR, and shipping-related attributes (WAREHOUSE_CODE, SHIPPED_AT, TRACKING_NUMBER, STATUS_CODE) directly indicate a shipme…_

3. _Customer Relationships: - A Customer places zero or more Sales Orders - A Customer has one or more Customer Addresses (not in simplified schema) Product Relationships: - A Product belongs to exactly o…_

---

### ✅ Q013 — Can a product belong to multiple categories?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.5380 | **Gate:** `proceed`

**Expected answer:**
> No, each product belongs to exactly one category. The TB_PRODUCT table has a CATEGORY_ID foreign key referencing TB_CATEGORY, which stores a single category value per product.

**System answer:**
> No. In the retrieved context, the Product relationship states that a product belongs to exactly one Category.

**RAGAS scores:**

| f | ar | cp | cr |
|---|----|----|-----|
| 1.00 | 0.79 | 1.00 | 1.00 |

**Sources retrieved (10):** `chunk_6`, `TB_PRODUCT→TB_CATEGORY`, `chunk_2`, `chunk_5`, `chunk_3`, `chunk_1`, `Hierarchical product category tree`, `chunk_7`

**Context previews (first 3):**

1. _Customer Relationships: - A Customer places zero or more Sales Orders - A Customer has one or more Customer Addresses (not in simplified schema) Product Relationships: - A Product belongs to exactly o…_

2. _Relationship: TB_PRODUCT references TB_CATEGORY via foreign key CATEGORY_ID -> TB_CATEGORY.CATEGORY_ID.…_

3. _**Foreign Keys**: - PARENT_CATEGORY_ID → TB_CATEGORY(CATEGORY_ID) [self-reference] **Business Concept Mapping**: Category ──────────────────────────────────────────────────────────── SALES_ORDER_HDR ─…_

---

### ✅ Q014 — Is it possible for a customer to place an order without payment?

**Status:** GROUNDED  
**GT Coverage:** 50% | **Top Score:** 0.0768 | **Gate:** `proceed_with_warning`

**Expected answer:**
> Technically yes, an order can be created in PENDING status without immediate payment. However, the order cannot be shipped until payment is confirmed (PAYMENT_CONFIRMED_AT is set). The business workflow requires payment confirmation before fulfillment.

**System answer:**
> The context does not say whether a customer can place an order without payment. It only states that a Customer can place zero or more Sales Orders, that Sales Orders are created when customers complete checkout, and that PAYMENT settles the total amount due for a Sales Order. So, from the provided context, it cannot be determined whether payment is required at the time an order is placed.

**RAGAS scores:**

| f | ar | cp | cr |
|---|----|----|-----|
| 1.00 | 0.00 | 0.77 | 1.00 |

**Sources retrieved (10):** `chunk_4`, `chunk_6`, `chunk_2`, `Sales Order`, `chunk_3`, `chunk_5`, `chunk_0`, `the customer, items, payment status, and delivery information`

**Context previews (first 3):**

1. _──────────────────────────────────────────────────────────── PAYMENT ──────────────────────────────────────────────────────────── **Definition**: The monetary transaction that settles the total amount…_

2. _Customer Relationships: - A Customer places zero or more Sales Orders - A Customer has one or more Customer Addresses (not in simplified schema) Product Relationships: - A Product belongs to exactly o…_

3. _──────────────────────────────────────────────────────────── SALES ORDER ──────────────────────────────────────────────────────────── **Definition**: A formal transaction document recording the agreem…_

---

### ✅ Q015 — What is the total value of all orders placed by a customer?

**Status:** GROUNDED  
**GT Coverage:** 25% | **Top Score:** 0.0654 | **Gate:** `proceed_with_warning`

**Expected answer:**
> Sum the TOTAL_AMT column from SALES_ORDER_HDR for all records where CUST_ID matches the customer's ID. This aggregates the monetary value of all orders placed by that customer.

**System answer:**
> The closest grounded concept in the context is Sales Order, which has a total amount field. The context does not explicitly define a customer-level aggregate for the total value of all orders, so I cannot confirm the exact term from the knowledge graph.

**RAGAS scores:**

| f | ar | cp | cr |
|---|----|----|-----|
| 1.00 | 0.00 | 0.92 | 1.00 |

**Sources retrieved (10):** `chunk_2`, `chunk_4`, `Sales Order`, `chunk_6`, `chunk_5`, `chunk_3`, `chunk_0`, `chunk_1`

**Context previews (first 3):**

1. _──────────────────────────────────────────────────────────── SALES ORDER ──────────────────────────────────────────────────────────── **Definition**: A formal transaction document recording the agreem…_

2. _──────────────────────────────────────────────────────────── PAYMENT ──────────────────────────────────────────────────────────── **Definition**: The monetary transaction that settles the total amount…_

3. _Sales Order: The table name, primary key ORDER_ID, customer foreign key, order date, total amount, and fulfillment/payment status fields align directly with a sales order header record. The business e…_

---

## Anomalies & Observations

- **Q001**: Very low context precision (0.12) — many off-topic chunks retrieved
- **Q006**: Very low context precision (0.00) — many off-topic chunks retrieved
