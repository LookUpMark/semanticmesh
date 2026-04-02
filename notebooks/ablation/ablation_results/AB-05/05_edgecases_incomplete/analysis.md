# AB-05 — 05_edgecases_incomplete — Run Analysis

**Timestamp:** 2026-03-31 02:09:25  
**Run tag:** `v5`

## Configuration

| Parameter | Value |
|-----------|-------|
| Extraction model | `LLM (gpt-5.4-nano-2026-03-17)` |
| Reasoning model | `gpt-5.4-2026-03-05` |
| Embedding model | `BAAI/bge-m3` |
| Retrieval mode | `hybrid` |
| Reranker | `True` |
| Reranker top_k | `20` |
| Chunk size / overlap | `256 / 32` |
| ER similarity threshold | `0.75` |

## Builder Results

Builder skipped (`--no-builder`).

## Query Evaluation Summary

| Metric | Value |
|--------|-------|
| Questions | 20 |
| Grounded | **20/20 (100%)** |
| Avg GT Coverage | 100% |
| Avg Top Score | 0.4706 |
| Avg Chunk Count | 12.0 |
| Abstained | 0 |

## RAGAS Metrics

RAGAS evaluation not enabled for this run.

## Per-Question Deep Dive

### ✅ ec_001 — What is a customer?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.8714 | **Gate:** `proceed`

**Expected answer:**
> The business glossary defines Customer as "an individual or organization that... [definition incomplete]". Related terms include Client (a person or company that purchases goods or services, sometimes used interchangeably with Customer), Account Holder (the primary owner of an account), and End User…

**System answer:**
> In the business glossary, Customer is defined only partially as “An individual or organization that...” because the definition is incomplete in the retrieved context.

Related glossary context says Client is “a person or company that purchases goods or services” and may be used interchangeably with Customer in some contexts. It also distinguishes Account Holder as the primary owner of an account, …

**Sources retrieved (12):** `CUSTOMERS→CUSTOMERS`, `parent_chunk_data_dictionary.txt_1`, `Sales Order→ORDERS`, `parent_chunk_data_dictionary.txt_2`, `parent_chunk_data_dictionary.txt_3`, `Payment gateway response→PAYMENTS`, `parent_chunk_business_glossary.txt_0`, `Sales Order`

**Context previews (first 3):**

1. _Business concept 'CUSTOMERS' is implemented by physical table CUSTOMERS (columns: customer_id, CustomerID, firstName, first_name, lastName, last_name, email, emailAddress, phone, phoneNumber, created_…_

2. _DATA DICTIONARY - Enterprise Database Version: 2.1 (incomplete documentation) Last Updated: 2024-02-28 ========================================== CUSTOMERS ========================================== P…_

3. _Business concept 'Sales Order' — The table contains canonical order-header attributes such as order_id, customer_id, order_date, order_status, and financial totals (amount, shipping, tax), which align…_

---

### ✅ ec_002 — What's the difference between firstName and first_name in the CUSTOMERS table?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.5988 | **Gate:** `proceed`

**Expected answer:**
> Both columns exist in the CUSTOMERS table with identical VARCHAR(50) data types. The data dictionary notes they appear to be duplicates resulting from inconsistent naming conventions (snake_case vs camelCase), but the actual usage by the application is not documented.

**System answer:**
> Based on the retrieved context, there is no documented business difference between `firstName` and `first_name` in `CUSTOMERS`.

The data dictionary says:

`firstName` is `VARCHAR(50)` and described as “Customer's first name.”
`first_name` is also `VARCHAR(50)` and is noted as “[appears to be duplicate].”

The concept-to-table mapping for `CUSTOMERS` also includes both columns, which reinforces th…

**Sources retrieved (12):** `CUSTOMERS→CUSTOMERS`, `parent_chunk_data_dictionary.txt_1`, `parent_chunk_data_dictionary.txt_2`, `Sales Order→ORDERS`, `parent_chunk_data_dictionary.txt_3`, `Order Items→ORDER_ITEMS`, `Merchandise→PRODUCTS`, `parent_chunk_business_glossary.txt_0`

**Context previews (first 3):**

1. _Business concept 'CUSTOMERS' is implemented by physical table CUSTOMERS (columns: customer_id, CustomerID, firstName, first_name, lastName, last_name, email, emailAddress, phone, phoneNumber, created_…_

2. _DATA DICTIONARY - Enterprise Database Version: 2.1 (incomplete documentation) Last Updated: 2024-02-28 ========================================== CUSTOMERS ========================================== P…_

3. _Foreign Keys: - customer_id → CUSTOMERS(customer_id or CustomerID?) - [missing other FK definitions] ========================================== ORDER_ITEMS (or ORDER_DETAILS?) ========================…_

---

### ✅ ec_003 — Which customer column should be used as a foreign key reference: customer_id or CustomerID?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.9258 | **Gate:** `proceed`

**Expected answer:**
> The CUSTOMERS table has both customer_id (defined as PRIMARY KEY) and CustomerID (defined as INTEGER with no constraints). The ORDERS table also has both customer_id and CustomerID columns with ambiguous FK references. The data dictionary indicates this inconsistency is documented but not yet resolv…

**System answer:**
> The retrieved context does not definitively resolve this. It is explicitly ambiguous.

In CUSTOMERS, the primary key is documented as “customer_id (or is it CustomerID? check with DBA),” so even the PK is marked as uncertain. The foreign key note likewise says “customer_id → CUSTOMERS(customer_id or CustomerID?),” which repeats that ambiguity rather than resolving it.

What the context does show i…

**Sources retrieved (12):** `parent_chunk_data_dictionary.txt_2`, `parent_chunk_data_dictionary.txt_1`, `CUSTOMERS→CUSTOMERS`, `parent_chunk_data_dictionary.txt_3`, `Sales Order→ORDERS`, `Payment gateway response→PAYMENTS`, `Order Items→ORDER_ITEMS`, `Merchandise→PRODUCTS`

**Context previews (first 3):**

1. _Foreign Keys: - customer_id → CUSTOMERS(customer_id or CustomerID?) - [missing other FK definitions] ========================================== ORDER_ITEMS (or ORDER_DETAILS?) ========================…_

2. _DATA DICTIONARY - Enterprise Database Version: 2.1 (incomplete documentation) Last Updated: 2024-02-28 ========================================== CUSTOMERS ========================================== P…_

3. _Business concept 'CUSTOMERS' is implemented by physical table CUSTOMERS (columns: customer_id, CustomerID, firstName, first_name, lastName, last_name, email, emailAddress, phone, phoneNumber, created_…_

---

### ✅ ec_004 — What are the valid values for order_status?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.3951 | **Gate:** `proceed`

**Expected answer:**
> The business glossary documents several order statuses: Pending, Processing, Completed, Cancelled, On Hold, and Failed (which is marked as [definition missing]). However, these are not enforced by a CHECK constraint in the schema, and the data dictionary notes that valid values reference '[missing d…

**System answer:**
> The retrieved context does not provide the valid values for `order_status`.

What the context does show is that `order_status` is a column on the `ORDERS` table, which implements the business concept “Sales Order.” That concept is described as an order placed by a customer, and the glossary says an “Order” is “a request to purchase products or services” and “can be in various states.” However, no …

**Sources retrieved (12):** `parent_chunk_data_dictionary.txt_3`, `Sales Order→ORDERS`, `parent_chunk_data_dictionary.txt_1`, `parent_chunk_data_dictionary.txt_2`, `Order Items→ORDER_ITEMS`, `Sales Order`, `Order Items`, `parent_chunk_business_glossary.txt_0`

**Context previews (first 3):**

1. _========================================== PAYMENTS ==========================================  Primary Key: payment_id (unverified) | Column Name | Data Type | Constraints | Description | |----------…_

2. _Business concept 'Sales Order' — The table contains canonical order-header attributes such as order_id, customer_id, order_date, order_status, and financial totals (amount, shipping, tax), which align…_

3. _DATA DICTIONARY - Enterprise Database Version: 2.1 (incomplete documentation) Last Updated: 2024-02-28 ========================================== CUSTOMERS ========================================== P…_

---

### ✅ ec_005 — Is there a difference between Product, Item, and SKU?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.5696 | **Gate:** `proceed`

**Expected answer:**
> The glossary indicates these terms are related but distinct: Product is defined as "A thing that is... [definition needs clarification]"; Item is a synonym for Product used in inventory context; SKU (Stock Keeping Unit) is a unique identifier for a product variant; Inventory Item refers to physical …

**System answer:**
> From the retrieved context, there is a schema-level difference between Product and Item, but SKU is not defined well enough to compare semantically.

A Product is represented by the business concept Merchandise, implemented by the PRODUCTS table. PRODUCTS contains master-style attributes such as product_id, product_name/ProductName, product_sku/sku, product_category/category, unit_price/current_pr…

**Sources retrieved (12):** `Merchandise→PRODUCTS`, `parent_chunk_data_dictionary.txt_2`, `Order Items→ORDER_ITEMS`, `parent_chunk_data_dictionary.txt_1`, `Sales Order→ORDERS`, `parent_chunk_data_dictionary.txt_3`, `parent_chunk_business_glossary.txt_0`, `Order Items`

**Context previews (first 3):**

1. _Business concept 'Merchandise' is implemented by physical table PRODUCTS (columns: product_id, ProductID, product_name, ProductName, product_sku, sku, product_category, category, unit_price, current_p…_

2. _Foreign Keys: - customer_id → CUSTOMERS(customer_id or CustomerID?) - [missing other FK definitions] ========================================== ORDER_ITEMS (or ORDER_DETAILS?) ========================…_

3. _Business concept 'Order Items' — The table is explicitly named ORDER_ITEMS and its columns form a classic order line structure with order_id, product_id, quantity, unit price, discounts, and line tota…_

---

### ✅ ec_006 — Which table should ORDER_ITEMS.product_id reference: PRODUCTS or INVENTORY?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.9608 | **Gate:** `proceed`

**Expected answer:**
> The data dictionary states the FK reference is to 'PRODUCTS (or INVENTORY?)' and notes it is 'not verified'. The schema provides two potential targets: PRODUCTS table (which has product_id) and an INVENTORY table that is referenced in documentation but not defined in the DDL. The actual relationship…

**System answer:**
> Based on the retrieved context, ORDER_ITEMS.product_id should most likely reference PRODUCTS, not INVENTORY.

The strongest support is:
ORDER_ITEMS is described as order line detail with product_id, quantity, unit price, discounts, and line total, and the business concept maps ORDER_ITEMS to line items.
PRODUCTS is explicitly defined as the physical table for the business concept “Merchandise” and…

**Sources retrieved (12):** `parent_chunk_data_dictionary.txt_2`, `Order Items→ORDER_ITEMS`, `Merchandise→PRODUCTS`, `parent_chunk_data_dictionary.txt_3`, `parent_chunk_data_dictionary.txt_1`, `Order Items`, `parent_chunk_business_glossary.txt_0`, `Sales Order→ORDERS`

**Context previews (first 3):**

1. _Foreign Keys: - customer_id → CUSTOMERS(customer_id or CustomerID?) - [missing other FK definitions] ========================================== ORDER_ITEMS (or ORDER_DETAILS?) ========================…_

2. _Business concept 'Order Items' — The table is explicitly named ORDER_ITEMS and its columns form a classic order line structure with order_id, product_id, quantity, unit price, discounts, and line tota…_

3. _Business concept 'Merchandise' is implemented by physical table PRODUCTS (columns: product_id, ProductID, product_name, ProductName, product_sku, sku, product_category, category, unit_price, current_p…_

---

### ✅ ec_007 — What's the difference between Revenue and Sales?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.4224 | **Gate:** `proceed`

**Expected answer:**
> Both terms show circular definitions: Revenue is defined as 'Income from sales. The same as... [definition circular, see Sales]', while Sales is defined as 'Revenue from selling products. See Revenue.' The glossary provides no clear distinction between these concepts.

**System answer:**
> The retrieved context does not define “Revenue” or “Sales” as standalone business concepts, so it does not provide enough information to state the difference between them.

The closest related information is:
The business concept “Sales Order” maps to table ORDERS, which represents an order placed by a customer and includes order-header fields such as order_id, customer_id, order_date, order_statu…

**Sources retrieved (12):** `Sales Order→ORDERS`, `parent_chunk_data_dictionary.txt_2`, `Order Items→ORDER_ITEMS`, `parent_chunk_data_dictionary.txt_3`, `Merchandise→PRODUCTS`, `parent_chunk_business_glossary.txt_0`, `Sales Order`, `Order Items`

**Context previews (first 3):**

1. _Business concept 'Sales Order' — The table contains canonical order-header attributes such as order_id, customer_id, order_date, order_status, and financial totals (amount, shipping, tax), which align…_

2. _Foreign Keys: - customer_id → CUSTOMERS(customer_id or CustomerID?) - [missing other FK definitions] ========================================== ORDER_ITEMS (or ORDER_DETAILS?) ========================…_

3. _Business concept 'Order Items' — The table is explicitly named ORDER_ITEMS and its columns form a classic order line structure with order_id, product_id, quantity, unit price, discounts, and line tota…_

---

### ✅ ec_008 — Can one order have multiple payments?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0981 | **Gate:** `proceed_with_warning`

**Expected answer:**
> The PAYMENTS table has an order_id column, suggesting a many-to-one relationship (multiple payments can reference a single order). However, the relationship section in the glossary asks 'Or is it one-to-one?' indicating uncertainty. The ORDERS table has both payment_status and payment_method columns…

**System answer:**
> Yes, the schema suggests that one order can have multiple payments.

From the PAYMENTS table, each payment has its own primary key, payment_id, and also carries order_id as a foreign key referencing ORDERS. Because order_id in PAYMENTS is documented as an FK rather than a PK or unique column, the retrieved context does not show any constraint limiting an order to a single payment row. That implies…

**Sources retrieved (12):** `parent_chunk_data_dictionary.txt_3`, `Sales Order→ORDERS`, `Payment gateway response→PAYMENTS`, `parent_chunk_data_dictionary.txt_2`, `parent_chunk_data_dictionary.txt_1`, `Order Items→ORDER_ITEMS`, `Merchandise→PRODUCTS`, `CUSTOMERS→CUSTOMERS`

**Context previews (first 3):**

1. _========================================== PAYMENTS ==========================================  Primary Key: payment_id (unverified) | Column Name | Data Type | Constraints | Description | |----------…_

2. _Business concept 'Sales Order' — The table contains canonical order-header attributes such as order_id, customer_id, order_date, order_status, and financial totals (amount, shipping, tax), which align…_

3. _Business concept 'Payment gateway response' is implemented by physical table PAYMENTS (columns: payment_id, PaymentID, order_id, customer_id, payment_date, payment_amount, payment_method, payment_stat…_

---

### ✅ ec_009 — What payment methods are accepted?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.1791 | **Gate:** `proceed_with_warning`

**Expected answer:**
> The PAYMENTS table has a payment_method column (VARCHAR(30)), but the data dictionary notes '[missing valid values]' and no CHECK constraint exists to enumerate acceptable methods. The schema does not document what values are valid (e.g., credit_card, debit, paypal, etc.).

**System answer:**
> The retrieved context does not list the accepted payment methods.

What it does show is that payment method is stored in both PAYMENTS.payment_method and ORDERS.payment_method, but in the PAYMENTS data dictionary the documentation explicitly says the column has “[missing valid values].” No enumeration of allowed or accepted methods is provided in the context.

**Sources retrieved (12):** `parent_chunk_data_dictionary.txt_3`, `Payment gateway response→PAYMENTS`, `Sales Order→ORDERS`, `parent_chunk_data_dictionary.txt_1`, `parent_chunk_data_dictionary.txt_2`, `parent_chunk_business_glossary.txt_0`, `Payment gateway response`, `CUSTOMERS→CUSTOMERS`

**Context previews (first 3):**

1. _========================================== PAYMENTS ==========================================  Primary Key: payment_id (unverified) | Column Name | Data Type | Constraints | Description | |----------…_

2. _Business concept 'Payment gateway response' is implemented by physical table PAYMENTS (columns: payment_id, PaymentID, order_id, customer_id, payment_date, payment_amount, payment_method, payment_stat…_

3. _Business concept 'Sales Order' — The table contains canonical order-header attributes such as order_id, customer_id, order_date, order_status, and financial totals (amount, shipping, tax), which align…_

---

### ✅ ec_010 — What's the correct table name: ORDER_ITEMS or ORDER_DETAILS?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.9938 | **Gate:** `proceed`

**Expected answer:**
> The DDL creates a table named ORDER_ITEMS, but the data dictionary header shows 'ORDER_ITEMS (or ORDER_DETAILS?)' and notes 'Table name ambiguity: ORDER_ITEMS vs ORDER_DETAILS'. The actual table name in the schema is ORDER_ITEMS, but documentation suggests the application may reference it differentl…

**System answer:**
> Based on the retrieved context, the correct table name is ORDER_ITEMS.

The strongest evidence is that the business concept "Order Items" is explicitly mapped to the physical table ORDER_ITEMS in the concept mapping, and another context chunk states, "The table is explicitly named ORDER_ITEMS." The reference to "ORDER_ITEMS (or ORDER_DETAILS?)" appears only in incomplete or uncertain documentation…

**Sources retrieved (12):** `parent_chunk_data_dictionary.txt_2`, `Order Items→ORDER_ITEMS`, `parent_chunk_data_dictionary.txt_3`, `Merchandise→PRODUCTS`, `parent_chunk_data_dictionary.txt_1`, `CUSTOMERS→CUSTOMERS`, `Order Items`, `Sales Order→ORDERS`

**Context previews (first 3):**

1. _Foreign Keys: - customer_id → CUSTOMERS(customer_id or CustomerID?) - [missing other FK definitions] ========================================== ORDER_ITEMS (or ORDER_DETAILS?) ========================…_

2. _Business concept 'Order Items' — The table is explicitly named ORDER_ITEMS and its columns form a classic order line structure with order_id, product_id, quantity, unit price, discounts, and line tota…_

3. _========================================== PAYMENTS ==========================================  Primary Key: payment_id (unverified) | Column Name | Data Type | Constraints | Description | |----------…_

---

### ✅ ec_011 — Which date column should be used to track when an order was created: order_date, OrderDate, or created_at?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.7679 | **Gate:** `proceed`

**Expected answer:**
> The ORDERS table has three date-related columns: order_date (DATE type), OrderDate (DATETIME type with different precision), and created_at (TIMESTAMP type). The data dictionary provides no guidance on which is actually used by the application or why three columns exist for potentially the same purp…

**System answer:**
> From the retrieved context, the strongest documented choice for tracking when an order was created is `order_date` in `ORDERS`.

The reason is that the business concept mapping for `Sales Order` explicitly calls out `order_date` as one of the “canonical order-header attributes” for the order entity. `OrderDate` also exists in the same table and appears to be a duplicate naming variant, since the c…

**Sources retrieved (12):** `Sales Order→ORDERS`, `Payment gateway response→PAYMENTS`, `parent_chunk_data_dictionary.txt_1`, `parent_chunk_data_dictionary.txt_3`, `CUSTOMERS→CUSTOMERS`, `Merchandise→PRODUCTS`, `Order Items→ORDER_ITEMS`, `parent_chunk_data_dictionary.txt_2`

**Context previews (first 3):**

1. _Business concept 'Sales Order' — The table contains canonical order-header attributes such as order_id, customer_id, order_date, order_status, and financial totals (amount, shipping, tax), which align…_

2. _Business concept 'Payment gateway response' is implemented by physical table PAYMENTS (columns: payment_id, PaymentID, order_id, customer_id, payment_date, payment_amount, payment_method, payment_stat…_

3. _DATA DICTIONARY - Enterprise Database Version: 2.1 (incomplete documentation) Last Updated: 2024-02-28 ========================================== CUSTOMERS ========================================== P…_

---

### ✅ ec_012 — What does the Failed order status mean?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0031 | **Gate:** `proceed_with_warning`

**Expected answer:**
> The business glossary lists Failed as an order status but marks it as '[definition missing]'. Other statuses have definitions (Pending, Processing, Completed, Cancelled, On Hold), but Failed is undefined despite being a valid status value.

**System answer:**
> I cannot find a definition of the specific order status value "Failed" in the retrieved context.

What the context does show is that the business concept Sales Order is implemented by the ORDERS table, which includes an order_status column, and the glossary says an Order is "a request to purchase products or services" that "can be in various states." However, no valid values or meanings for order_…

**Sources retrieved (12):** `Sales Order→ORDERS`, `parent_chunk_data_dictionary.txt_3`, `parent_chunk_data_dictionary.txt_1`, `parent_chunk_data_dictionary.txt_2`, `Order Items→ORDER_ITEMS`, `Payment gateway response→PAYMENTS`, `Merchandise→PRODUCTS`, `CUSTOMERS→CUSTOMERS`

**Context previews (first 3):**

1. _Business concept 'Sales Order' — The table contains canonical order-header attributes such as order_id, customer_id, order_date, order_status, and financial totals (amount, shipping, tax), which align…_

2. _========================================== PAYMENTS ==========================================  Primary Key: payment_id (unverified) | Column Name | Data Type | Constraints | Description | |----------…_

3. _DATA DICTIONARY - Enterprise Database Version: 2.1 (incomplete documentation) Last Updated: 2024-02-28 ========================================== CUSTOMERS ========================================== P…_

---

### ✅ ec_013 — Are there any NOT NULL constraints defined in the schema?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.7628 | **Gate:** `proceed`

**Expected answer:**
> No NOT NULL constraints are defined in the DDL. The data dictionary explicitly states 'NOT NULL constraints not defined' under 'Missing Documentation' and notes 'assumed, not verified'. All columns are nullable by default.

**System answer:**
> No explicit NOT NULL constraints are defined in the retrieved context.

The schema metadata shown for CUSTOMERS, PAYMENTS, ORDER_ITEMS, and the concept mappings documents PK, FK, and one possible UNIQUE constraint, but the non-key columns are mostly marked with “?” or “[missing documentation].” Even where primary keys are identified, the context does not explicitly state NOT NULL for any column. S…

**Sources retrieved (12):** `parent_chunk_data_dictionary.txt_3`, `parent_chunk_data_dictionary.txt_2`, `Order Items→ORDER_ITEMS`, `parent_chunk_data_dictionary.txt_1`, `Sales Order→ORDERS`, `Order Items`, `parent_chunk_business_glossary.txt_0`, `Merchandise→PRODUCTS`

**Context previews (first 3):**

1. _========================================== PAYMENTS ==========================================  Primary Key: payment_id (unverified) | Column Name | Data Type | Constraints | Description | |----------…_

2. _Foreign Keys: - customer_id → CUSTOMERS(customer_id or CustomerID?) - [missing other FK definitions] ========================================== ORDER_ITEMS (or ORDER_DETAILS?) ========================…_

3. _Business concept 'Order Items' — The table is explicitly named ORDER_ITEMS and its columns form a classic order line structure with order_id, product_id, quantity, unit price, discounts, and line tota…_

---

### ✅ ec_014 — What's the difference between unit_price and current_price in PRODUCTS?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.5008 | **Gate:** `proceed`

**Expected answer:**
> The PRODUCTS table has both unit_price and current_price columns (both DECIMAL(10,2)). The data dictionary asks 'Different from unit_price?' but provides no explanation of the distinction or when each would be used.

**System answer:**
> The retrieved context only shows that PRODUCTS includes both unit_price and current_price as columns in the business concept Merchandise. It does not provide any column descriptions, business rules, or calculation logic for either field in PRODUCTS, so the difference between them is not documented in the available context.

From the context, we can say only this:
PRODUCTS has columns including uni…

**Sources retrieved (12):** `Merchandise→PRODUCTS`, `parent_chunk_data_dictionary.txt_2`, `Order Items→ORDER_ITEMS`, `Sales Order→ORDERS`, `parent_chunk_data_dictionary.txt_3`, `Order Items`, `parent_chunk_business_glossary.txt_0`, `Sales Order`

**Context previews (first 3):**

1. _Business concept 'Merchandise' is implemented by physical table PRODUCTS (columns: product_id, ProductID, product_name, ProductName, product_sku, sku, product_category, category, unit_price, current_p…_

2. _Foreign Keys: - customer_id → CUSTOMERS(customer_id or CustomerID?) - [missing other FK definitions] ========================================== ORDER_ITEMS (or ORDER_DETAILS?) ========================…_

3. _Business concept 'Order Items' — The table is explicitly named ORDER_ITEMS and its columns form a classic order line structure with order_id, product_id, quantity, unit price, discounts, and line tota…_

---

### ✅ ec_015 — When is an invoice generated vs payment processed?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.6598 | **Gate:** `proceed`

**Expected answer:**
> The relationship section in the glossary asks 'An invoice is generated for an order. But when? And can one order have multiple invoices?' indicating the timing and cardinality are not defined. The glossary defines Invoice as 'A document requesting payment. Related to Bill' and Payment as 'The transf…

**System answer:**
> The retrieved context does not contain enough information to say when an invoice is generated versus when a payment is processed.

What is supported by the context is this: payment processing is represented by the PAYMENTS table, which is mapped to the business concept Payment gateway response. That table includes order_id, customer_id, payment_date, payment_amount, payment_method, payment_status,…

**Sources retrieved (12):** `parent_chunk_data_dictionary.txt_3`, `Sales Order→ORDERS`, `parent_chunk_data_dictionary.txt_1`, `parent_chunk_data_dictionary.txt_2`, `Payment gateway response→PAYMENTS`, `parent_chunk_business_glossary.txt_0`, `Payment gateway response`, `Order Items→ORDER_ITEMS`

**Context previews (first 3):**

1. _========================================== PAYMENTS ==========================================  Primary Key: payment_id (unverified) | Column Name | Data Type | Constraints | Description | |----------…_

2. _Business concept 'Sales Order' — The table contains canonical order-header attributes such as order_id, customer_id, order_date, order_status, and financial totals (amount, shipping, tax), which align…_

3. _DATA DICTIONARY - Enterprise Database Version: 2.1 (incomplete documentation) Last Updated: 2024-02-28 ========================================== CUSTOMERS ========================================== P…_

---

### ✅ ec_016 — Is the sku column in PRODUCTS unique?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.3933 | **Gate:** `proceed`

**Expected answer:**
> The PRODUCTS table has both product_sku and sku columns. The data dictionary notes sku 'should be UNIQUE?' but the DDL does not define a UNIQUE constraint on either column. No index is documented for these columns.

**System answer:**
> The context shows that PRODUCTS includes both product_sku and sku as columns under the business concept Merchandise, but it does not document any uniqueness constraint for sku or product_sku.

So, based strictly on the retrieved context, uniqueness of sku in PRODUCTS cannot be confirmed. The available context only establishes that the column exists; it does not state UNIQUE, PK, or any other const…

**Sources retrieved (12):** `Merchandise→PRODUCTS`, `parent_chunk_data_dictionary.txt_2`, `parent_chunk_data_dictionary.txt_3`, `Order Items→ORDER_ITEMS`, `parent_chunk_data_dictionary.txt_1`, `CUSTOMERS→CUSTOMERS`, `Sales Order→ORDERS`, `Payment gateway response→PAYMENTS`

**Context previews (first 3):**

1. _Business concept 'Merchandise' is implemented by physical table PRODUCTS (columns: product_id, ProductID, product_name, ProductName, product_sku, sku, product_category, category, unit_price, current_p…_

2. _Foreign Keys: - customer_id → CUSTOMERS(customer_id or CustomerID?) - [missing other FK definitions] ========================================== ORDER_ITEMS (or ORDER_DETAILS?) ========================…_

3. _========================================== PAYMENTS ==========================================  Primary Key: payment_id (unverified) | Column Name | Data Type | Constraints | Description | |----------…_

---

### ✅ ec_017 — What is the relationship between customers and orders?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0859 | **Gate:** `proceed_with_warning`

**Expected answer:**
> The glossary states 'A customer can place multiple orders. Or is it accounts that place orders?' indicating uncertainty about the relationship. The ORDERS table has both customer_id and CustomerID columns with ambiguous FK references, and the data dictionary notes they reference 'customer (which tab…

**System answer:**
> The relationship is that orders are linked to customers through the customer identifier on the order header.

From the context, the physical table ORDERS, which implements the business concept Sales Order, contains customer_id (and also a duplicate-style variant CustomerID). The CUSTOMERS table uses customer_id as its primary key, with a possible duplicate variant CustomerID. The documented foreig…

**Sources retrieved (12):** `parent_chunk_data_dictionary.txt_3`, `Sales Order→ORDERS`, `parent_chunk_data_dictionary.txt_2`, `parent_chunk_data_dictionary.txt_1`, `Order Items→ORDER_ITEMS`, `CUSTOMERS→CUSTOMERS`, `Merchandise→PRODUCTS`, `parent_chunk_business_glossary.txt_0`

**Context previews (first 3):**

1. _========================================== PAYMENTS ==========================================  Primary Key: payment_id (unverified) | Column Name | Data Type | Constraints | Description | |----------…_

2. _Business concept 'Sales Order' — The table contains canonical order-header attributes such as order_id, customer_id, order_date, order_status, and financial totals (amount, shipping, tax), which align…_

3. _Foreign Keys: - customer_id → CUSTOMERS(customer_id or CustomerID?) - [missing other FK definitions] ========================================== ORDER_ITEMS (or ORDER_DETAILS?) ========================…_

---

### ✅ ec_018 — Which price column represents what the customer actually pays?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0581 | **Gate:** `proceed_with_warning`

**Expected answer:**
> Multiple price columns exist across tables: ORDERS has orderAmount and total_amount; ORDER_ITEMS has unit_price and UnitPrice; PRODUCTS has unit_price, current_price, and cost_price. The data dictionary does not explain which represents the final customer price, whether discounts are applied, or how…

**System answer:**
> The retrieved context does not identify a single column that is explicitly defined as “what the customer actually pays,” so this cannot be determined definitively.

What is known from the context is:

In PRODUCTS, there are price-related columns unit_price, current_price, and cost_price, but the context does not define which of those is customer-facing.

In ORDER_ITEMS, unit_price is described as …

**Sources retrieved (12):** `Payment gateway response→PAYMENTS`, `Sales Order→ORDERS`, `parent_chunk_data_dictionary.txt_2`, `Order Items→ORDER_ITEMS`, `Merchandise→PRODUCTS`, `parent_chunk_data_dictionary.txt_3`, `CUSTOMERS→CUSTOMERS`, `parent_chunk_data_dictionary.txt_1`

**Context previews (first 3):**

1. _Business concept 'Payment gateway response' is implemented by physical table PAYMENTS (columns: payment_id, PaymentID, order_id, customer_id, payment_date, payment_amount, payment_method, payment_stat…_

2. _Business concept 'Sales Order' — The table contains canonical order-header attributes such as order_id, customer_id, order_date, order_status, and financial totals (amount, shipping, tax), which align…_

3. _Foreign Keys: - customer_id → CUSTOMERS(customer_id or CustomerID?) - [missing other FK definitions] ========================================== ORDER_ITEMS (or ORDER_DETAILS?) ========================…_

---

### ✅ ec_019 — What's the difference between Shipment, Delivery, and Fulfillment?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0050 | **Gate:** `proceed_with_warning`

**Expected answer:**
> The glossary provides definitions but unclear boundaries: Shipment is 'The process of delivering goods to a customer'; Delivery is 'The completion of a Shipment when goods reach the customer'; Fulfillment is 'The process of preparing and delivering orders. Encompasses Shipment and Delivery.' The exa…

**System answer:**
> I cannot find definitions or distinctions for Shipment, Delivery, or Fulfillment in the retrieved context.

The only related glossary content in the context is:
Order: “A request to purchase products or services. Can be in various states.”
Transaction: “Similar to Order but more general.”

The retrieved context also includes schema/business concepts for Sales Order, Order Items, Products, Customer…

**Sources retrieved (12):** `Sales Order→ORDERS`, `parent_chunk_data_dictionary.txt_2`, `parent_chunk_data_dictionary.txt_3`, `Order Items→ORDER_ITEMS`, `Merchandise→PRODUCTS`, `parent_chunk_business_glossary.txt_0`, `Sales Order`, `Order Items`

**Context previews (first 3):**

1. _Business concept 'Sales Order' — The table contains canonical order-header attributes such as order_id, customer_id, order_date, order_status, and financial totals (amount, shipping, tax), which align…_

2. _Foreign Keys: - customer_id → CUSTOMERS(customer_id or CustomerID?) - [missing other FK definitions] ========================================== ORDER_ITEMS (or ORDER_DETAILS?) ========================…_

3. _========================================== PAYMENTS ==========================================  Primary Key: payment_id (unverified) | Column Name | Data Type | Constraints | Description | |----------…_

---

### ✅ ec_020 — Are foreign key constraints enforced in the schema?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.1603 | **Gate:** `proceed_with_warning`

**Expected answer:**
> No foreign key constraints are enforced in the DDL. While the data dictionary documents FK relationships (e.g., customer_id → CUSTOMERS, order_id → ORDERS), the actual CREATE TABLE statements omit the REFERENCES clauses. The schema explicitly notes 'FK constraints defined in data dictionary but not …

**System answer:**
> The retrieved context does not confirm that foreign key constraints are actually enforced by the database schema.

What it does show is schema documentation that marks some columns as foreign keys, for example:
ORDER_ITEMS.order_id references ORDERS, and ORDER_ITEMS.product_id references PRODUCTS, although that reference is noted as uncertain with “PRODUCTS (or INVENTORY?)” and there are inconsist…

**Sources retrieved (12):** `parent_chunk_data_dictionary.txt_2`, `parent_chunk_data_dictionary.txt_3`, `parent_chunk_data_dictionary.txt_1`, `Order Items→ORDER_ITEMS`, `Order Items`, `parent_chunk_business_glossary.txt_0`, `Payment gateway response→PAYMENTS`, `Sales Order→ORDERS`

**Context previews (first 3):**

1. _Foreign Keys: - customer_id → CUSTOMERS(customer_id or CustomerID?) - [missing other FK definitions] ========================================== ORDER_ITEMS (or ORDER_DETAILS?) ========================…_

2. _========================================== PAYMENTS ==========================================  Primary Key: payment_id (unverified) | Column Name | Data Type | Constraints | Description | |----------…_

3. _DATA DICTIONARY - Enterprise Database Version: 2.1 (incomplete documentation) Last Updated: 2024-02-28 ========================================== CUSTOMERS ========================================== P…_

---

## Anomalies & Observations

No anomalies detected. All questions grounded with acceptable RAGAS scores.
