# AB-13 — 01_basics_ecommerce — Run Analysis

**Timestamp:** 2026-07-17 19:18:46  
**Run tag:** `run-20260717_195424`

## Configuration

| Parameter | Value |
|-----------|-------|
| Extraction model | `LLM (gpt-5-nano-2025-08-07)` |
| Reasoning model | `gpt-5.4-nano-2026-03-17` |
| Embedding model | `BAAI/bge-m3` |
| Retrieval mode | `hybrid` |
| Reranker | `True` |
| Reranker top_k | `5` |
| Chunk size / overlap | `256 / 32` |
| ER similarity threshold | `0.75` |

## Builder Results

| Metric | Value |
|--------|-------|
| Triplets extracted | 122 |
| Entities resolved | 65 |
| Tables parsed | 7 |
| Tables completed | 7 |

## Query Evaluation Summary

| Metric | Value |
|--------|-------|
| Questions | 15 |
| Grounded | **15/15 (100%)** |
| Avg GT Coverage | 98% |
| Avg Top Score | 0.7856 |
| Avg Chunk Count | 15.1 |
| Abstained | 0 |

## RAGAS Metrics

RAGAS evaluation not enabled for this run.

## Per-Question Deep Dive

### ✅ Q001 — What information is stored for each customer?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0000 | **Gate:** `proceed`

**Expected answer:**
> Each customer has a unique ID, full name, email address, geographic region code, creation date, and active status. The email must be unique across all customers.

**System answer:**
> 

**Sources retrieved (6):** `parent_chunk_business_glossary.txt_1`, `customer_master.full_name`, `customer_master`, `Customer Master`, `customer_master.created_at`, `sales_order_hdr`

---

### ✅ Q002 — How are products categorized on the platform?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0000 | **Gate:** `proceed`

**Expected answer:**
> Products belong to categories which can have a parent category, forming a hierarchical tree structure. Each product references exactly one category through its CATEGORY_ID.

**System answer:**
> 

**Sources retrieved (12):** `parent_chunk_business_glossary.txt_0`, `parent_chunk_data_dictionary.txt_4`, `parent_chunk_business_glossary.txt_1`, `tb_product→tb_category`, `tb_product.category_id`, `tb_product`, `Tb Product`, `tb_category`

---

### ✅ Q003 — What is the relationship between customers and sales orders?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0000 | **Gate:** `proceed`

**Expected answer:**
> Each sales order is placed by exactly one customer, referenced through the CUST_ID foreign key. A customer can place zero or more orders over time.

**System answer:**
> 

**Sources retrieved (12):** `parent_chunk_business_glossary.txt_0`, `parent_chunk_business_glossary.txt_1`, `parent_chunk_business_glossary.txt_2`, `sales_order_hdr→customer_master`, `Shipment`, `sales_order_hdr`, `Payment`, `Order Line Item`

---

### ✅ Q004 — What does an order line item contain?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0000 | **Gate:** `proceed`

**Expected answer:**
> An order line item specifies a product, the quantity ordered, the unit price at time of purchase, and the calculated extended amount. Each line item belongs to exactly one sales order.

**System answer:**
> 

**Sources retrieved (9):** `parent_chunk_business_glossary.txt_2`, `Order Line Item`, `order_line_item.line_id`, `order_line_item`, `order_line_item.quantity`, `order_line_item.unit_price`, `sales_order_hdr`, `Payment`

---

### ✅ Q005 — How are payments linked to orders?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0000 | **Gate:** `proceed`

**Expected answer:**
> Each payment is associated with exactly one sales order through the ORDER_ID foreign key. Payments track the payment method, amount, status, and confirmation timestamp.

**System answer:**
> 

**Sources retrieved (11):** `parent_chunk_business_glossary.txt_1`, `payment.payment_method`, `payment→sales_order_hdr`, `Shipment`, `Payment`, `payment`, `sales_order_hdr`, `payment.confirmed_at`

---

### ✅ Q006 — What statuses can an order have?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0000 | **Gate:** `proceed`

**Expected answer:**
> Orders can have one of five statuses defined via CHECK constraint on SALES_ORDER_HDR.STATUS_CODE: PENDING (initial state when order is created), CONFIRMED (payment has been received), SHIPPED (dispatched to customer), DELIVERED (received by customer), or CANCELLED. The business glossary describes th…

**System answer:**
> 

**Sources retrieved (12):** `parent_chunk_business_glossary.txt_0`, `parent_chunk_business_glossary.txt_1`, `sales_order_hdr.status_code`, `Shipment`, `Payment`, `sales_order_hdr`, `Sales Order Hdr`, `sales_order_hdr.cust_id`

---

### ✅ Q007 — Which table stores the product SKU information?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0000 | **Gate:** `proceed`

**Expected answer:**
> The TB_PRODUCT table stores the SKU (Stock Keeping Unit) code for each product, along with product name, category, price, and active status.

**System answer:**
> 

**Sources retrieved (10):** `tb_product.sku`, `parent_chunk_business_glossary.txt_0`, `Tb Product`, `sales_order_hdr.cust_id`, `tb_product`, `tb_product.unit_price`, `tb_product.is_active`, `tb_product.product_name`

---

### ✅ Q008 — How can I find all orders placed by a specific customer?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0000 | **Gate:** `proceed`

**Expected answer:**
> Query the SALES_ORDER_HDR table filtering by CUST_ID. Each order has a foreign key reference to CUSTOMER_MASTER.CUST_ID, so joining these tables on CUST_ID will show all orders for a customer along with their details.

**System answer:**
> 

**Sources retrieved (12):** `parent_chunk_data_dictionary.txt_4`, `parent_chunk_business_glossary.txt_0`, `parent_chunk_business_glossary.txt_2`, `Sales Order Hdr`, `sales_order_hdr.cust_id`, `customer_master`, `sales_order_hdr`, `sales_order_hdr.order_date`

---

### ✅ Q009 — How does the schema link orders to their individual product line items?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0000 | **Gate:** `proceed`

**Expected answer:**
> The ORDER_LINE_ITEM table is the junction entity between SALES_ORDER_HDR and TB_PRODUCT. It contains ORDER_ID (foreign key to SALES_ORDER_HDR) and PRODUCT_ID (foreign key to TB_PRODUCT), allowing a single order to have multiple line items. Each line item also records QUANTITY (constrained to be > 0)…

**System answer:**
> 

**Sources retrieved (12):** `parent_chunk_business_glossary.txt_1`, `order_line_item→tb_product`, `parent_chunk_data_dictionary.txt_5`, `order_line_item.product_id`, `order_line_item→sales_order_hdr`, `Order Line Item`, `order_line_item`, `tb_product`

---

### ✅ Q010 — Show me the order hierarchy from customer to line items.

**Status:** GROUNDED  
**GT Coverage:** 75% | **Top Score:** 0.0000 | **Gate:** `proceed`

**Expected answer:**
> The hierarchy is: Customer (CUSTOMER_MASTER) → SalesOrder (SALES_ORDER_HDR) → OrderLineItem (ORDER_LINE_ITEM) → Product (TB_PRODUCT). Each customer has orders, each order has line items, and each line item references a product.

**System answer:**
> 

**Sources retrieved (12):** `parent_chunk_business_glossary.txt_2`, `parent_chunk_business_glossary.txt_1`, `parent_chunk_data_dictionary.txt_5`, `order_line_item→sales_order_hdr`, `Order Line Item`, `order_line_item`, `order_line_item.order_id`, `order_line_item.quantity`

---

### ✅ Q011 — How does the schema model the confirmation state of a payment and its relationship to the order?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0000 | **Gate:** `proceed`

**Expected answer:**
> Payment confirmation is tracked through two schema fields: PAYMENT.CONFIRMED_AT (nullable DATETIME — NULL means not yet confirmed) and PAYMENT.STATUS_CODE constrained to PENDING, CONFIRMED, FAILED, or REFUNDED. At the order level, SALES_ORDER_HDR.PAYMENT_CONFIRMED_AT is a nullable datetime that mirr…

**System answer:**
> 

**Sources retrieved (10):** `parent_chunk_business_glossary.txt_1`, `payment.confirmed_at`, `sales_order_hdr.payment_confirmed_at`, `Payment`, `payment.order_id`, `sales_order_hdr`, `Sales Order Hdr`, `sales_order_hdr.cust_id`

---

### ✅ Q012 — How are shipments related to orders and warehouses?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0000 | **Gate:** `proceed`

**Expected answer:**
> Each shipment is for exactly one sales order (ORDER_ID in SHIPMENT references SALES_ORDER_HDR). The shipment also specifies the source warehouse code and includes tracking information and delivery status.

**System answer:**
> 

**Sources retrieved (10):** `parent_chunk_business_glossary.txt_1`, `shipment.warehouse_code`, `parent_chunk_business_glossary.txt_2`, `Shipment`, `shipment`, `sales_order_hdr`, `shipment.shipped_at`, `shipment.status_code`

---

### ✅ Q013 — Can a product belong to multiple categories?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0000 | **Gate:** `proceed`

**Expected answer:**
> No, each product belongs to exactly one category. The TB_PRODUCT table has a CATEGORY_ID foreign key referencing TB_CATEGORY, which stores a single category value per product.

**System answer:**
> 

**Sources retrieved (8):** `parent_chunk_business_glossary.txt_0`, `tb_product→tb_category`, `tb_category.category_name`, `parent_chunk_data_dictionary.txt_6`, `tb_product`, `tb_category`, `Tb Category`, `tb_category.category_id`

---

### ✅ Q014 — Is it possible for a customer to place an order without payment?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0000 | **Gate:** `proceed`

**Expected answer:**
> Yes, an order can exist without payment. SALES_ORDER_HDR has STATUS_CODE defaulting to PENDING and PAYMENT_CONFIRMED_AT is nullable (NULL when no payment yet). The PAYMENT table links via ORDER_ID foreign key but nothing prevents an order from existing without a payment row. However, the business gl…

**System answer:**
> 

**Sources retrieved (12):** `parent_chunk_data_dictionary.txt_4`, `parent_chunk_business_glossary.txt_1`, `parent_chunk_business_glossary.txt_2`, `parent_chunk_business_glossary.txt_0`, `Payment`, `payment.order_id`, `Shipment`, `payment`

---

### ✅ Q015 — What schema fields support monetary value tracking across orders and their line items?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0000 | **Gate:** `proceed`

**Expected answer:**
> SALES_ORDER_HDR stores the header-level order amount in TOTAL_AMT (DECIMAL(12,2) NOT NULL). ORDER_LINE_ITEM provides the per-product breakdown: UNIT_PRICE (price locked at time of order, not updated with future changes), QUANTITY (constrained to > 0), and LINE_AMT (= QUANTITY × UNIT_PRICE). Both tab…

**System answer:**
> 

**Sources retrieved (11):** `parent_chunk_business_glossary.txt_0`, `parent_chunk_business_glossary.txt_1`, `parent_chunk_data_dictionary.txt_5`, `order_line_item.line_amt`, `Order Line Item`, `order_line_item`, `order_line_item.order_id`, `order_line_item.quantity`

---

## Anomalies & Observations

No anomalies detected. All questions grounded with acceptable RAGAS scores.
