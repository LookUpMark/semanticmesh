# AB-BEST-OPENROUTER — 01_basics_ecommerce — Run Analysis

**Timestamp:** 2026-04-15 16:44:00  
**Run tag:** `ds01-20260415`

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
| Triplets extracted | 88 |
| Entities resolved | 50 |
| Tables parsed | 7 |
| Tables completed | 7 |

## Query Evaluation Summary

| Metric | Value |
|--------|-------|
| Questions | 15 |
| Grounded | **15/15 (100%)** |
| Avg GT Coverage | 100% |
| Avg Top Score | 0.4272 |
| Avg Chunk Count | 12.0 |
| Abstained | 0 |

## RAGAS Metrics

RAGAS evaluation not enabled for this run.

## Per-Question Deep Dive

### ✅ Q001 — What information is stored for each customer?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0833 | **Gate:** `proceed_with_warning`

**Expected answer:**
> Each customer has a unique ID, full name, email address, geographic region code, creation date, and active status. The email must be unique across all customers.

**System answer:**
> The e‑commerce data model stores a single “customer” record in the **CUSTOMER_MASTER** table. For each customer the following fields are captured:

* **CUST_ID** – the unique, auto‑incremented identifier for the customer.  
* **FULL_NAME** – the customer’s full name.  
* **EMAIL** – the unique email address used for login.  
* **REGION_CODE** – the geographic region (used for tax calculation).  
*…

**Sources retrieved (12):** `Customer Items Payment→SALES_ORDER_HDR`, `Customer Items Payment→PAYMENT`, `parent_chunk_data_dictionary.txt_0`, `parent_chunk_business_glossary.txt_3`, `Customer→CUSTOMER_MASTER`, `Individual Product Lines→ORDER_LINE_ITEM`, `parent_chunk_business_glossary.txt_4`, `SALES_ORDER_HDR→CUSTOMER_MASTER`

**Context previews (first 3):**

1. _Business concept 'Customer Items Payment' — Orders are created when customers complete checkout. They track the customer, items, payment status, and delivery information. is implemented by physical ta…_

2. _Business concept 'Customer Items Payment' — Orders are created when customers complete checkout. They track the customer, items, payment status, and delivery information. is implemented by physical ta…_

3. _# Data Dictionary - E-Commerce Database (Simplified)  This document describes the physical database schema for the simplified e-commerce test dataset.  ────────────────────────────────────────────────…_

---

### ✅ Q002 — How are products categorized on the platform?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.1590 | **Gate:** `proceed_with_warning`

**Expected answer:**
> Products belong to categories which can have a parent category, forming a hierarchical tree structure. Each product references exactly one category through its CATEGORY_ID.

**System answer:**
> Products are linked to categories through the **CATEGORY_ID** column in the **TB_PRODUCT** table. The foreign‑key relationship `TB_PRODUCT.CATEGORY_ID → TB_CATEGORY.CATEGORY_ID` (see chunk [10]) assigns each product to a single category record.  

The **TB_CATEGORY** table (the “Hierarchical Product Category Tree” described in chunks [9] and [12]) stores categories and supports a hierarchy via its…

**Sources retrieved (12):** `parent_chunk_business_glossary.txt_3`, `parent_chunk_data_dictionary.txt_0`, `Individual Product Lines→ORDER_LINE_ITEM`, `parent_chunk_business_glossary.txt_4`, `Customer→CUSTOMER_MASTER`, `Individual Product Lines`, `parent_chunk_data_dictionary.txt_2`, `Customer`

**Context previews (first 3):**

1. _# Business Glossary - E-Commerce Domain (Simplified)  This document defines the core business concepts for the e-commerce platform test dataset.  ──────────────────────────────────────────────────────…_

2. _# Data Dictionary - E-Commerce Database (Simplified)  This document describes the physical database schema for the simplified e-commerce test dataset.  ────────────────────────────────────────────────…_

3. _Business concept 'Individual Product Lines' — A formal transaction document recording the agreement between the platform and a Customer to supply Products. is implemented by physical table ORDER_LINE_…_

---

### ✅ Q003 — What is the relationship between customers and sales orders?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.9847 | **Gate:** `proceed`

**Expected answer:**
> Each sales order is placed by exactly one customer, referenced through the CUST_ID foreign key. A customer can place zero or more orders over time.

**System answer:**
> The e‑commerce model defines the link between a customer and a sales order as follows:

- **Business rule** – “A Sales Order is placed by exactly one Customer” [1].  
- **Physical implementation** – The sales‑order header table `SALES_ORDER_HDR` contains the column `CUST_ID`, which is a foreign key that references `CUSTOMER_MASTER(CUST_ID)` [5][7][12].

Thus, every sales‑order record is associated…

**Sources retrieved (12):** `parent_chunk_business_glossary.txt_5`, `parent_chunk_business_glossary.txt_3`, `Customer Items Payment→SALES_ORDER_HDR`, `parent_chunk_business_glossary.txt_4`, `parent_chunk_data_dictionary.txt_1`, `Customer Items Payment→PAYMENT`, `SALES_ORDER_HDR→CUSTOMER_MASTER`, `parent_chunk_data_dictionary.txt_0`

**Context previews (first 3):**

1. _Sales Order Relationships: - A Sales Order is placed by exactly one Customer - A Sales Order has one or more Order Line Items - A Sales Order has one or more Payments - A Sales Order has one or more S…_

2. _# Business Glossary - E-Commerce Domain (Simplified)  This document defines the core business concepts for the e-commerce platform test dataset.  ──────────────────────────────────────────────────────…_

3. _Business concept 'Customer Items Payment' — Orders are created when customers complete checkout. They track the customer, items, payment status, and delivery information. is implemented by physical ta…_

---

### ✅ Q004 — What does an order line item contain?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.8739 | **Gate:** `proceed`

**Expected answer:**
> An order line item specifies a product, the quantity ordered, the unit price at time of purchase, and the calculated extended amount. Each line item belongs to exactly one sales order.

**System answer:**
> An **order line item** (the physical table **ORDER_LINE_ITEM**) records a single product purchase within a sales order.  
It contains the following fields:

* **LINE_ID** – the unique identifier for the line (primary key).  
* **ORDER_ID** – foreign‑key to the parent sales order (**SALES_ORDER_HDR.ORDER_ID**).  
* **PRODUCT_ID** – foreign‑key to the product being bought (**TB_PRODUCT.PRODUCT_ID**)…

**Sources retrieved (12):** `parent_chunk_business_glossary.txt_4`, `ORDER_LINE_ITEM→TB_PRODUCT`, `ORDER_LINE_ITEM→SALES_ORDER_HDR`, `parent_chunk_business_glossary.txt_5`, `Individual Product Lines→ORDER_LINE_ITEM`, `parent_chunk_data_dictionary.txt_1`, `Shipment→SHIPMENT`, `Customer Items Payment→SALES_ORDER_HDR`

**Context previews (first 3):**

1. _**Business Context**: Line items break down orders into individual product purchases. Each captures the price at the moment of ordering. **Key Attributes**: - Unique line identifier - References exact…_

2. _Relationship: ORDER_LINE_ITEM references TB_PRODUCT via foreign key PRODUCT_ID -> TB_PRODUCT.PRODUCT_ID.…_

3. _Relationship: ORDER_LINE_ITEM references SALES_ORDER_HDR via foreign key ORDER_ID -> SALES_ORDER_HDR.ORDER_ID.…_

---

### ✅ Q005 — How are payments linked to orders?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.9232 | **Gate:** `proceed`

**Expected answer:**
> Each payment is associated with exactly one sales order through the ORDER_ID foreign key. Payments track the payment method, amount, status, and confirmation timestamp.

**System answer:**
> Payments are linked to orders through a foreign‑key relationship.  
The **PAYMENT** table contains an **ORDER_ID** column, and this column is defined as a foreign key that references **SALES_ORDER_HDR.ORDER_ID** (the primary key of the sales‑order header). As a result:

* Each payment record points to exactly one sales order (the order for which the payment was made).  
* Conversely, a sales order…

**Sources retrieved (12):** `PAYMENT→SALES_ORDER_HDR`, `Customer Items Payment→PAYMENT`, `Customer Items Payment→SALES_ORDER_HDR`, `parent_chunk_business_glossary.txt_4`, `parent_chunk_business_glossary.txt_5`, `parent_chunk_data_dictionary.txt_1`, `SHIPMENT→SALES_ORDER_HDR`, `ORDER_LINE_ITEM→SALES_ORDER_HDR`

**Context previews (first 3):**

1. _Relationship: PAYMENT references SALES_ORDER_HDR via foreign key ORDER_ID -> SALES_ORDER_HDR.ORDER_ID.…_

2. _Business concept 'Customer Items Payment' — Orders are created when customers complete checkout. They track the customer, items, payment status, and delivery information. is implemented by physical ta…_

3. _Business concept 'Customer Items Payment' — Orders are created when customers complete checkout. They track the customer, items, payment status, and delivery information. is implemented by physical ta…_

---

### ✅ Q006 — What statuses can an order have?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.2261 | **Gate:** `proceed`

**Expected answer:**
> Orders can have one of five statuses defined via CHECK constraint on SALES_ORDER_HDR.STATUS_CODE: PENDING (initial state when order is created), CONFIRMED (payment has been received), SHIPPED (dispatched to customer), DELIVERED (received by customer), or CANCELLED. The business glossary describes th…

**System answer:**
> The only information the retrieved context gives about an order’s status is that the **`SALES_ORDER_HDR`** table has a column named **`STATUS_CODE`** (along with timestamps such as `PAYMENT_CONFIRMED_AT` and `DELIVERED_AT`).  

The actual list of possible status values (e.g., “Pending”, “Confirmed”, “Delivered”, “Cancelled”, etc.) is **not provided** in the supplied context. Therefore, based on th…

**Sources retrieved (12):** `Customer Items Payment→SALES_ORDER_HDR`, `parent_chunk_business_glossary.txt_3`, `parent_chunk_business_glossary.txt_4`, `Customer Items Payment→PAYMENT`, `Shipment→SHIPMENT`, `parent_chunk_business_glossary.txt_5`, `parent_chunk_data_dictionary.txt_1`, `parent_chunk_data_dictionary.txt_0`

**Context previews (first 3):**

1. _Business concept 'Customer Items Payment' — Orders are created when customers complete checkout. They track the customer, items, payment status, and delivery information. is implemented by physical ta…_

2. _# Business Glossary - E-Commerce Domain (Simplified)  This document defines the core business concepts for the e-commerce platform test dataset.  ──────────────────────────────────────────────────────…_

3. _**Business Context**: Line items break down orders into individual product purchases. Each captures the price at the moment of ordering. **Key Attributes**: - Unique line identifier - References exact…_

---

### ✅ Q007 — Which table stores the product SKU information?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.6228 | **Gate:** `proceed`

**Expected answer:**
> The TB_PRODUCT table stores the SKU (Stock Keeping Unit) code for each product, along with product name, category, price, and active status.

**System answer:**
> The product SKU is stored in the **TB_PRODUCT** table (its columns include PRODUCT_ID, SKU, PRODUCT_NAME, CATEGORY_ID, UNIT_PRICE, IS_ACTIVE)【1】.

**Sources retrieved (12):** `Product→TB_PRODUCT`, `Individual Product Lines→ORDER_LINE_ITEM`, `parent_chunk_data_dictionary.txt_0`, `ORDER_LINE_ITEM→TB_PRODUCT`, `Customer→CUSTOMER_MASTER`, `parent_chunk_business_glossary.txt_3`, `TB_PRODUCT→TB_CATEGORY`, `Hierarchical Product Category Tree→TB_CATEGORY`

**Context previews (first 3):**

1. _Business concept 'Product' — The price per unit of a product at the moment the order is placed. is implemented by physical table TB_PRODUCT (columns: PRODUCT_ID, SKU, PRODUCT_NAME, CATEGORY_ID, UNIT_P…_

2. _Business concept 'Individual Product Lines' — A formal transaction document recording the agreement between the platform and a Customer to supply Products. is implemented by physical table ORDER_LINE_…_

3. _# Data Dictionary - E-Commerce Database (Simplified)  This document describes the physical database schema for the simplified e-commerce test dataset.  ────────────────────────────────────────────────…_

---

### ✅ Q008 — How can I find all orders placed by a specific customer?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.1428 | **Gate:** `proceed_with_warning`

**Expected answer:**
> Query the SALES_ORDER_HDR table filtering by CUST_ID. Each order has a foreign key reference to CUSTOMER_MASTER.CUST_ID, so joining these tables on CUST_ID will show all orders for a customer along with their details.

**System answer:**
> To retrieve every order that belongs to a given customer you use the foreign‑key link between **CUSTOMER_MASTER** and **SALES_ORDER_HDR**.

* **CUSTOMER_MASTER** holds the master record for each customer; its primary key is **CUST_ID**.  
* **SALES_ORDER_HDR** stores one row per sales order and contains the column **CUST_ID**, which is defined as a foreign key that references **CUSTOMER_MASTER(CUS…

**Sources retrieved (12):** `parent_chunk_data_dictionary.txt_0`, `parent_chunk_business_glossary.txt_5`, `parent_chunk_business_glossary.txt_3`, `parent_chunk_data_dictionary.txt_1`, `Customer Items Payment→SALES_ORDER_HDR`, `Customer Items Payment→PAYMENT`, `SALES_ORDER_HDR→CUSTOMER_MASTER`, `parent_chunk_business_glossary.txt_4`

**Context previews (first 3):**

1. _# Data Dictionary - E-Commerce Database (Simplified)  This document describes the physical database schema for the simplified e-commerce test dataset.  ────────────────────────────────────────────────…_

2. _Sales Order Relationships: - A Sales Order is placed by exactly one Customer - A Sales Order has one or more Order Line Items - A Sales Order has one or more Payments - A Sales Order has one or more S…_

3. _# Business Glossary - E-Commerce Domain (Simplified)  This document defines the core business concepts for the e-commerce platform test dataset.  ──────────────────────────────────────────────────────…_

---

### ✅ Q009 — How does the schema link orders to their individual product line items?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.7434 | **Gate:** `proceed`

**Expected answer:**
> The ORDER_LINE_ITEM table is the junction entity between SALES_ORDER_HDR and TB_PRODUCT. It contains ORDER_ID (foreign key to SALES_ORDER_HDR) and PRODUCT_ID (foreign key to TB_PRODUCT), allowing a single order to have multiple line items. Each line item also records QUANTITY (constrained to be > 0)…

**System answer:**
> The link is made through the **ORDER_LINE_ITEM** table:

* ORDER_LINE_ITEM has a column **ORDER_ID** that is defined as a foreign‑key to **SALES_ORDER_HDR.ORDER_ID** ([4], [5], [12]).  
* Because SALES_ORDER_HDR.ORDER_ID is the primary key of the sales‑order header, each row in ORDER_LINE_ITEM points to exactly one sales order, while a sales order can be referenced by many ORDER_LINE_ITEM rows ([6…

**Sources retrieved (12):** `ORDER_LINE_ITEM→TB_PRODUCT`, `Individual Product Lines→ORDER_LINE_ITEM`, `parent_chunk_business_glossary.txt_4`, `ORDER_LINE_ITEM→SALES_ORDER_HDR`, `parent_chunk_data_dictionary.txt_1`, `parent_chunk_business_glossary.txt_5`, `parent_chunk_data_dictionary.txt_0`, `parent_chunk_business_glossary.txt_3`

**Context previews (first 3):**

1. _Relationship: ORDER_LINE_ITEM references TB_PRODUCT via foreign key PRODUCT_ID -> TB_PRODUCT.PRODUCT_ID.…_

2. _Business concept 'Individual Product Lines' — A formal transaction document recording the agreement between the platform and a Customer to supply Products. is implemented by physical table ORDER_LINE_…_

3. _**Business Context**: Line items break down orders into individual product purchases. Each captures the price at the moment of ordering. **Key Attributes**: - Unique line identifier - References exact…_

---

### ✅ Q010 — Show me the order hierarchy from customer to line items.

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.3719 | **Gate:** `proceed`

**Expected answer:**
> The hierarchy is: Customer (CUSTOMER_MASTER) → SalesOrder (SALES_ORDER_HDR) → OrderLineItem (ORDER_LINE_ITEM) → Product (TB_PRODUCT). Each customer has orders, each order has line items, and each line item references a product.

**System answer:**
> **Hierarchy**

1. **Customer** – stored in **`CUSTOMER_MASTER`** (primary key `CUST_ID`).  
2. **Sales Order** – stored in **`SALES_ORDER_HDR`**; each row has a foreign‑key **`CUST_ID`** that points to `CUSTOMER_MASTER.CUST_ID` (see chunk [11] and the foreign‑key note in chunk [1]).  
3. **Order Line Items** – stored in **`ORDER_LINE_ITEM`**; each row has a foreign‑key **`ORDER_ID`** that points t…

**Sources retrieved (12):** `parent_chunk_business_glossary.txt_5`, `parent_chunk_data_dictionary.txt_1`, `parent_chunk_business_glossary.txt_4`, `Individual Product Lines→ORDER_LINE_ITEM`, `ORDER_LINE_ITEM→TB_PRODUCT`, `ORDER_LINE_ITEM→SALES_ORDER_HDR`, `Customer Items Payment→SALES_ORDER_HDR`, `Customer Items Payment→PAYMENT`

**Context previews (first 3):**

1. _Sales Order Relationships: - A Sales Order is placed by exactly one Customer - A Sales Order has one or more Order Line Items - A Sales Order has one or more Payments - A Sales Order has one or more S…_

2. _**Foreign Keys**: - CUST_ID → CUSTOMER_MASTER(CUST_ID) **Business Concept Mapping**: SalesOrder ──────────────────────────────────────────────────────────── ORDER_LINE_ITEM ───────────────────────────…_

3. _**Business Context**: Line items break down orders into individual product purchases. Each captures the price at the moment of ordering. **Key Attributes**: - Unique line identifier - References exact…_

---

### ✅ Q011 — How does the schema model the confirmation state of a payment and its relationship to the order?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.1128 | **Gate:** `proceed_with_warning`

**Expected answer:**
> Payment confirmation is tracked through two schema fields: PAYMENT.CONFIRMED_AT (nullable DATETIME — NULL means not yet confirmed) and PAYMENT.STATUS_CODE constrained to PENDING, CONFIRMED, FAILED, or REFUNDED. At the order level, SALES_ORDER_HDR.PAYMENT_CONFIRMED_AT is a nullable datetime that mirr…

**System answer:**
> The schema records the confirmation of a payment in the **PAYMENT** table.  
- The table includes a **STATUS_CODE** column that holds the current payment status (e.g., pending, confirmed, failed).  
- It also has a **CONFIRMED_AT** datetime column that stores the timestamp when the payment was marked as confirmed.  

The payment is tied to its order through a foreign‑key relationship: **PAYMENT.OR…

**Sources retrieved (12):** `parent_chunk_business_glossary.txt_4`, `Customer Items Payment→PAYMENT`, `Customer Items Payment→SALES_ORDER_HDR`, `parent_chunk_data_dictionary.txt_1`, `parent_chunk_data_dictionary.txt_0`, `parent_chunk_business_glossary.txt_5`, `PAYMENT→SALES_ORDER_HDR`, `parent_chunk_business_glossary.txt_3`

**Context previews (first 3):**

1. _**Business Context**: Line items break down orders into individual product purchases. Each captures the price at the moment of ordering. **Key Attributes**: - Unique line identifier - References exact…_

2. _Business concept 'Customer Items Payment' — Orders are created when customers complete checkout. They track the customer, items, payment status, and delivery information. is implemented by physical ta…_

3. _Business concept 'Customer Items Payment' — Orders are created when customers complete checkout. They track the customer, items, payment status, and delivery information. is implemented by physical ta…_

---

### ✅ Q012 — How are shipments related to orders and warehouses?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.6447 | **Gate:** `proceed`

**Expected answer:**
> Each shipment is for exactly one sales order (ORDER_ID in SHIPMENT references SALES_ORDER_HDR). The shipment also specifies the source warehouse code and includes tracking information and delivery status.

**System answer:**
> Shipments are tied to a single sales order and to a single source warehouse.

* **Order relationship** – The physical **SHIPMENT** table contains the column **ORDER_ID**. According to the foreign‑key definition (chunk 12) **SHIPMENT.ORDER_ID → SALES_ORDER_HDR.ORDER_ID**, so each shipment record points to exactly one sales‑order header row. This is also described in the business‑relationship summar…

**Sources retrieved (12):** `Shipment→SHIPMENT`, `parent_chunk_business_glossary.txt_5`, `parent_chunk_business_glossary.txt_3`, `parent_chunk_business_glossary.txt_4`, `Customer Items Payment→PAYMENT`, `Customer Items Payment→SALES_ORDER_HDR`, `parent_chunk_data_dictionary.txt_1`, `parent_chunk_data_dictionary.txt_0`

**Context previews (first 3):**

1. _Business concept 'Shipment' — A specific shipment identified by its unique shipment number, containing items and associated with a tracking number and order. is implemented by physical table SHIPMENT …_

2. _Sales Order Relationships: - A Sales Order is placed by exactly one Customer - A Sales Order has one or more Order Line Items - A Sales Order has one or more Payments - A Sales Order has one or more S…_

3. _# Business Glossary - E-Commerce Domain (Simplified)  This document defines the core business concepts for the e-commerce platform test dataset.  ──────────────────────────────────────────────────────…_

---

### ✅ Q013 — Can a product belong to multiple categories?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.3613 | **Gate:** `proceed`

**Expected answer:**
> No, each product belongs to exactly one category. The TB_PRODUCT table has a CATEGORY_ID foreign key referencing TB_CATEGORY, which stores a single category value per product.

**System answer:**
> No. In this data model a product can belong to only **one** category.

The schema shows that the **TB_PRODUCT** table has a single column **CATEGORY_ID** that references **TB_CATEGORY.CATEGORY_ID** (see the foreign‑key relationship in the retrieved context). Because there is just one foreign‑key column, each product row can point to only one category row, meaning a product is assigned to a single …

**Sources retrieved (12):** `parent_chunk_business_glossary.txt_3`, `TB_PRODUCT→TB_CATEGORY`, `parent_chunk_business_glossary.txt_4`, `Hierarchical Product Category Tree→TB_CATEGORY`, `Product→TB_PRODUCT`, `parent_chunk_data_dictionary.txt_0`, `parent_chunk_data_dictionary.txt_1`, `ORDER_LINE_ITEM→TB_PRODUCT`

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
> The business rules (see chunk 3) state that **“A Sales Order has one or more Payments.”** This indicates that, in the intended e‑commerce process, an order is expected to be accompanied by at least one payment record.

From the schema side, the only structural link is the foreign‑key relationship shown in chunk 8: **PAYMENT.ORDER_ID → SALES_ORDER_HDR.ORDER_ID.** A foreign key from PAYMENT to SALES…

**Sources retrieved (12):** `parent_chunk_data_dictionary.txt_0`, `parent_chunk_business_glossary.txt_4`, `parent_chunk_business_glossary.txt_5`, `Customer Items Payment→PAYMENT`, `Customer Items Payment→SALES_ORDER_HDR`, `parent_chunk_business_glossary.txt_3`, `parent_chunk_data_dictionary.txt_1`, `PAYMENT→SALES_ORDER_HDR`

**Context previews (first 3):**

1. _# Data Dictionary - E-Commerce Database (Simplified)  This document describes the physical database schema for the simplified e-commerce test dataset.  ────────────────────────────────────────────────…_

2. _**Business Context**: Line items break down orders into individual product purchases. Each captures the price at the moment of ordering. **Key Attributes**: - Unique line identifier - References exact…_

3. _Sales Order Relationships: - A Sales Order is placed by exactly one Customer - A Sales Order has one or more Order Line Items - A Sales Order has one or more Payments - A Sales Order has one or more S…_

---

### ✅ Q015 — What schema fields support monetary value tracking across orders and their line items?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0862 | **Gate:** `proceed_with_warning`

**Expected answer:**
> SALES_ORDER_HDR stores the header-level order amount in TOTAL_AMT (DECIMAL(12,2) NOT NULL). ORDER_LINE_ITEM provides the per-product breakdown: UNIT_PRICE (price locked at time of order, not updated with future changes), QUANTITY (constrained to > 0), and LINE_AMT (= QUANTITY × UNIT_PRICE). Both tab…

**System answer:**
> The database records monetary values in two places:

* At the order‑header level, the **SALES_ORDER_HDR** table includes the column **TOTAL_AMT** (the total amount for the sales order).  
* At the line‑item level, the **ORDER_LINE_ITEM** table includes **UNIT_PRICE** (the price of a single unit at the time the order is placed) and **LINE_AMT** (the extended amount calculated as quantity × unit pri…

**Sources retrieved (12):** `parent_chunk_business_glossary.txt_4`, `parent_chunk_data_dictionary.txt_1`, `ORDER_LINE_ITEM→TB_PRODUCT`, `Individual Product Lines→ORDER_LINE_ITEM`, `ORDER_LINE_ITEM→SALES_ORDER_HDR`, `Customer Items Payment→PAYMENT`, `parent_chunk_business_glossary.txt_5`, `Customer Items Payment→SALES_ORDER_HDR`

**Context previews (first 3):**

1. _**Business Context**: Line items break down orders into individual product purchases. Each captures the price at the moment of ordering. **Key Attributes**: - Unique line identifier - References exact…_

2. _**Foreign Keys**: - CUST_ID → CUSTOMER_MASTER(CUST_ID) **Business Concept Mapping**: SalesOrder ──────────────────────────────────────────────────────────── ORDER_LINE_ITEM ───────────────────────────…_

3. _Relationship: ORDER_LINE_ITEM references TB_PRODUCT via foreign key PRODUCT_ID -> TB_PRODUCT.PRODUCT_ID.…_

---

## Anomalies & Observations

No anomalies detected. All questions grounded with acceptable RAGAS scores.
