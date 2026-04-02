# AB-17 — 05_edgecases_incomplete — Run Analysis

**Timestamp:** 2026-04-01 19:30:29  
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
| Triplets extracted | 220 |
| Entities resolved | 99 |
| Tables parsed | 5 |
| Tables completed | 5 |

## Query Evaluation Summary

| Metric | Value |
|--------|-------|
| Questions | 20 |
| Grounded | **20/20 (100%)** |
| Avg GT Coverage | 100% |
| Avg Top Score | 0.4786 |
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
> In the BUSINESS GLOSSARY under CUSTOMER MANAGEMENT, Customer is defined only partially as “An individual or organization that...” because the definition is incomplete in the retrieved context.

Related glossary terms clarify the meaning around it: Client is “a person or company that purchases goods or services” and may be used interchangeably with Customer in some contexts; Account Holder is simil…

**Sources retrieved (12):** `Customer's first name→CUSTOMERS`, `parent_chunk_data_dictionary.txt_1`, `parent_chunk_data_dictionary.txt_2`, `parent_chunk_data_dictionary.txt_3`, `ORDER_ITEMS vs ORDER_PRODUCTS vs ORDER_DETAILS→ORDERS`, `payment_method valid values not documented (credit_card, debit, paypal?)→PAYMENTS`, `parent_chunk_business_glossary.txt_0`, `Customer's first name`

**Context previews (first 3):**

1. _Business concept 'Customer's first name' is implemented by physical table CUSTOMERS (columns: customer_id, CustomerID, firstName, first_name, lastName, last_name, email, emailAddress, phone, phoneNumb…_

2. _DATA DICTIONARY - Enterprise Database Version: 2.1 (incomplete documentation) Last Updated: 2024-02-28 ========================================== CUSTOMERS ========================================== P…_

3. _Foreign Keys: - customer_id → CUSTOMERS(customer_id or CustomerID?) - [missing other FK definitions] ========================================== ORDER_ITEMS (or ORDER_DETAILS?) ========================…_

---

### ✅ ec_002 — What's the difference between firstName and first_name in the CUSTOMERS table?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.6176 | **Gate:** `proceed`

**Expected answer:**
> Both columns exist in the CUSTOMERS table with identical VARCHAR(50) data types. The data dictionary notes they appear to be duplicates resulting from inconsistent naming conventions (snake_case vs camelCase), but the actual usage by the application is not documented.

**System answer:**
> Based on the retrieved context, there is no documented business difference between `firstName` and `first_name` in `CUSTOMERS`.

The data dictionary shows both columns as `VARCHAR(50)`. `firstName` is described as “Customer's first name,” while `first_name` is marked as “[appears to be duplicate].” The business concept mapping for “Customer's first name” also points to the `CUSTOMERS` table and in…

**Sources retrieved (12):** `Customer's first name→CUSTOMERS`, `parent_chunk_data_dictionary.txt_1`, `parent_chunk_data_dictionary.txt_2`, `parent_chunk_data_dictionary.txt_3`, `Order Item`, `Order Item→ORDER_ITEMS`, `parent_chunk_business_glossary.txt_0`, `ORDER_ITEMS vs ORDER_PRODUCTS vs ORDER_DETAILS→ORDERS`

**Context previews (first 3):**

1. _Business concept 'Customer's first name' is implemented by physical table CUSTOMERS (columns: customer_id, CustomerID, firstName, first_name, lastName, last_name, email, emailAddress, phone, phoneNumb…_

2. _DATA DICTIONARY - Enterprise Database Version: 2.1 (incomplete documentation) Last Updated: 2024-02-28 ========================================== CUSTOMERS ========================================== P…_

3. _Foreign Keys: - customer_id → CUSTOMERS(customer_id or CustomerID?) - [missing other FK definitions] ========================================== ORDER_ITEMS (or ORDER_DETAILS?) ========================…_

---

### ✅ ec_003 — Which customer column should be used as a foreign key reference: customer_id or CustomerID?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.9258 | **Gate:** `proceed`

**Expected answer:**
> The CUSTOMERS table has both customer_id (defined as PRIMARY KEY) and CustomerID (defined as INTEGER with no constraints). The ORDERS table also has both customer_id and CustomerID columns with ambiguous FK references. The data dictionary indicates this inconsistency is documented but not yet resolv…

**System answer:**
> The context does not confirm this definitively. The strongest evidence points to using customer_id:

In CUSTOMERS, customer_id is labeled as the primary key, while CustomerID is marked as a possible duplicate and not confirmed. The documentation explicitly says “Primary Key: customer_id (or is it CustomerID? check with DBA),” so the schema is inconsistent and requires validation. The foreign key n…

**Sources retrieved (12):** `parent_chunk_data_dictionary.txt_2`, `parent_chunk_data_dictionary.txt_1`, `Customer's first name→CUSTOMERS`, `parent_chunk_data_dictionary.txt_3`, `ORDER_ITEMS vs ORDER_PRODUCTS vs ORDER_DETAILS→ORDERS`, `payment_method valid values not documented (credit_card, debit, paypal?)→PAYMENTS`, `Order Item→ORDER_ITEMS`, `ORDER_ITEMS vs ORDER_PRODUCTS vs ORDER_DETAILS→PRODUCTS`

**Context previews (first 3):**

1. _Foreign Keys: - customer_id → CUSTOMERS(customer_id or CustomerID?) - [missing other FK definitions] ========================================== ORDER_ITEMS (or ORDER_DETAILS?) ========================…_

2. _DATA DICTIONARY - Enterprise Database Version: 2.1 (incomplete documentation) Last Updated: 2024-02-28 ========================================== CUSTOMERS ========================================== P…_

3. _Business concept 'Customer's first name' is implemented by physical table CUSTOMERS (columns: customer_id, CustomerID, firstName, first_name, lastName, last_name, email, emailAddress, phone, phoneNumb…_

---

### ✅ ec_004 — What are the valid values for order_status?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.4798 | **Gate:** `proceed`

**Expected answer:**
> The business glossary documents several order statuses: Pending, Processing, Completed, Cancelled, On Hold, and Failed (which is marked as [definition missing]). However, these are not enforced by a CHECK constraint in the schema, and the data dictionary notes that valid values reference '[missing d…

**System answer:**
> The valid values for ORDERS.order_status are not documented in the provided context.

What the context does show is that the ORDERS table includes an order_status column, and the business glossary says an Order “can be in various states,” but no specific status values are listed anywhere in the retrieved context.

**Sources retrieved (12):** `payment_method valid values not documented (credit_card, debit, paypal?)→PAYMENTS`, `parent_chunk_data_dictionary.txt_3`, `ORDER_ITEMS vs ORDER_PRODUCTS vs ORDER_DETAILS→ORDERS`, `parent_chunk_data_dictionary.txt_1`, `parent_chunk_data_dictionary.txt_2`, `parent_chunk_business_glossary.txt_0`, `payment_method valid values not documented (credit_card, debit, paypal?)`, `Order Item→ORDER_ITEMS`

**Context previews (first 3):**

1. _Business concept 'payment_method valid values not documented (credit_card, debit, paypal?)' is implemented by physical table PAYMENTS (columns: payment_id, PaymentID, order_id, customer_id, payment_da…_

2. _========================================== PAYMENTS ==========================================  Primary Key: payment_id (unverified) | Column Name | Data Type | Constraints | Description | |----------…_

3. _Business concept 'ORDER_ITEMS vs ORDER_PRODUCTS vs ORDER_DETAILS' is implemented by physical table ORDERS (columns: order_id, OrderID, customer_id, CustomerID, order_date, OrderDate, order_status, ord…_

---

### ✅ ec_005 — Is there a difference between Product, Item, and SKU?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.5696 | **Gate:** `proceed`

**Expected answer:**
> The glossary indicates these terms are related but distinct: Product is defined as "A thing that is... [definition needs clarification]"; Item is a synonym for Product used in inventory context; SKU (Stock Keeping Unit) is a unique identifier for a product variant; Inventory Item refers to physical …

**System answer:**
> Yes, the retrieved context distinguishes Product and Item at the schema level, but it does not fully define SKU as a separate business concept.

A Product is represented by the physical table PRODUCTS. That table includes product-level attributes such as product_id/ProductID, product_name/ProductName, product_sku/sku, product_category/category, unit_price/current_price, cost_price, stock_quantity/…

**Sources retrieved (12):** `ORDER_ITEMS vs ORDER_PRODUCTS vs ORDER_DETAILS→PRODUCTS`, `parent_chunk_data_dictionary.txt_2`, `Order Item`, `Order Item→ORDER_ITEMS`, `ORDER_ITEMS vs ORDER_PRODUCTS vs ORDER_DETAILS→ORDERS`, `parent_chunk_data_dictionary.txt_1`, `parent_chunk_data_dictionary.txt_3`, `parent_chunk_business_glossary.txt_0`

**Context previews (first 3):**

1. _Business concept 'ORDER_ITEMS vs ORDER_PRODUCTS vs ORDER_DETAILS' is implemented by physical table PRODUCTS (columns: product_id, ProductID, product_name, ProductName, product_sku, sku, product_catego…_

2. _Foreign Keys: - customer_id → CUSTOMERS(customer_id or CustomerID?) - [missing other FK definitions] ========================================== ORDER_ITEMS (or ORDER_DETAILS?) ========================…_

3. _Order Item: The table stores line-level order attributes such as order_id, product_id, quantity, unit_price, discount, and line_total, which is characteristic of an order item/line item structure. The…_

---

### ✅ ec_006 — Which table should ORDER_ITEMS.product_id reference: PRODUCTS or INVENTORY?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.9608 | **Gate:** `proceed`

**Expected answer:**
> The data dictionary states the FK reference is to 'PRODUCTS (or INVENTORY?)' and notes it is 'not verified'. The schema provides two potential targets: PRODUCTS table (which has product_id) and an INVENTORY table that is referenced in documentation but not defined in the DDL. The actual relationship…

**System answer:**
> The retrieved context indicates that ORDER_ITEMS.product_id should most likely reference PRODUCTS, but the documentation is inconsistent.

In the ORDER_ITEMS definition, product_id is described as an FK that “References PRODUCTS (or INVENTORY?),” so the source itself flags uncertainty. However, the strongest supporting context points to PRODUCTS:

The business concept “Order Item” is implemented b…

**Sources retrieved (12):** `parent_chunk_data_dictionary.txt_2`, `ORDER_ITEMS vs ORDER_PRODUCTS vs ORDER_DETAILS→PRODUCTS`, `Order Item`, `Order Item→ORDER_ITEMS`, `ORDER_ITEMS vs ORDER_PRODUCTS vs ORDER_DETAILS→ORDERS`, `parent_chunk_data_dictionary.txt_3`, `parent_chunk_data_dictionary.txt_1`, `parent_chunk_business_glossary.txt_0`

**Context previews (first 3):**

1. _Foreign Keys: - customer_id → CUSTOMERS(customer_id or CustomerID?) - [missing other FK definitions] ========================================== ORDER_ITEMS (or ORDER_DETAILS?) ========================…_

2. _Business concept 'ORDER_ITEMS vs ORDER_PRODUCTS vs ORDER_DETAILS' is implemented by physical table PRODUCTS (columns: product_id, ProductID, product_name, ProductName, product_sku, sku, product_catego…_

3. _Order Item: The table stores line-level order attributes such as order_id, product_id, quantity, unit_price, discount, and line_total, which is characteristic of an order item/line item structure. The…_

---

### ✅ ec_007 — What's the difference between Revenue and Sales?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.4224 | **Gate:** `proceed`

**Expected answer:**
> Both terms show circular definitions: Revenue is defined as 'Income from sales. The same as... [definition circular, see Sales]', while Sales is defined as 'Revenue from selling products. See Revenue.' The glossary provides no clear distinction between these concepts.

**System answer:**
> I cannot determine the difference between Revenue and Sales from the provided context.

The retrieved context includes a partial business glossary and schema metadata for concepts such as Customer, Client, Account Holder, End User, Order, Transaction, Order Item, CUSTOMERS, ORDER_ITEMS, ORDERS, PRODUCTS, and PAYMENTS. However, it does not provide any glossary entry, table comment, or definition fo…

**Sources retrieved (12):** `parent_chunk_data_dictionary.txt_2`, `parent_chunk_data_dictionary.txt_3`, `Order Item→ORDER_ITEMS`, `Order Item`, `parent_chunk_business_glossary.txt_0`, `parent_chunk_data_dictionary.txt_1`, `ORDER_ITEMS vs ORDER_PRODUCTS vs ORDER_DETAILS→ORDERS`, `ORDER_ITEMS vs ORDER_PRODUCTS vs ORDER_DETAILS→PRODUCTS`

**Context previews (first 3):**

1. _Foreign Keys: - customer_id → CUSTOMERS(customer_id or CustomerID?) - [missing other FK definitions] ========================================== ORDER_ITEMS (or ORDER_DETAILS?) ========================…_

2. _========================================== PAYMENTS ==========================================  Primary Key: payment_id (unverified) | Column Name | Data Type | Constraints | Description | |----------…_

3. _Business concept 'Order Item' — The table stores line-level order attributes such as order_id, product_id, quantity, unit_price, discount, and line_total, which is characteristic of an order item/line…_

---

### ✅ ec_008 — Can one order have multiple payments?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0981 | **Gate:** `proceed_with_warning`

**Expected answer:**
> The PAYMENTS table has an order_id column, suggesting a many-to-one relationship (multiple payments can reference a single order). However, the relationship section in the glossary asks 'Or is it one-to-one?' indicating uncertainty. The ORDERS table has both payment_status and payment_method columns…

**System answer:**
> Based on the retrieved schema metadata, yes, the design suggests one order can have multiple payments.

The reason is that PAYMENTS has its own primary key, payment_id, and also contains order_id as a foreign key referencing ORDERS. That structure means PAYMENTS is a separate child table linked to ORDERS through order_id. There is no documented unique constraint on PAYMENTS.order_id in the provide…

**Sources retrieved (12):** `parent_chunk_data_dictionary.txt_3`, `ORDER_ITEMS vs ORDER_PRODUCTS vs ORDER_DETAILS→ORDERS`, `parent_chunk_data_dictionary.txt_2`, `payment_method valid values not documented (credit_card, debit, paypal?)→PAYMENTS`, `parent_chunk_data_dictionary.txt_1`, `Order Item→ORDER_ITEMS`, `Order Item`, `ORDER_ITEMS vs ORDER_PRODUCTS vs ORDER_DETAILS→PRODUCTS`

**Context previews (first 3):**

1. _========================================== PAYMENTS ==========================================  Primary Key: payment_id (unverified) | Column Name | Data Type | Constraints | Description | |----------…_

2. _Business concept 'ORDER_ITEMS vs ORDER_PRODUCTS vs ORDER_DETAILS' is implemented by physical table ORDERS (columns: order_id, OrderID, customer_id, CustomerID, order_date, OrderDate, order_status, ord…_

3. _Foreign Keys: - customer_id → CUSTOMERS(customer_id or CustomerID?) - [missing other FK definitions] ========================================== ORDER_ITEMS (or ORDER_DETAILS?) ========================…_

---

### ✅ ec_009 — What payment methods are accepted?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.2140 | **Gate:** `proceed`

**Expected answer:**
> The PAYMENTS table has a payment_method column (VARCHAR(30)), but the data dictionary notes '[missing valid values]' and no CHECK constraint exists to enumerate acceptable methods. The schema does not document what values are valid (e.g., credit_card, debit, paypal, etc.).

**System answer:**
> The accepted payment methods are not documented in the retrieved context.

What the context does show is that payment method is captured in PAYMENTS.payment_method, and ORDERS also includes a payment_method column. For PAYMENTS, the business concept explicitly says “payment_method valid values not documented (credit_card, debit, paypal?)”, and the data dictionary marks PAYMENTS.payment_method as V…

**Sources retrieved (12):** `payment_method valid values not documented (credit_card, debit, paypal?)→PAYMENTS`, `parent_chunk_data_dictionary.txt_3`, `ORDER_ITEMS vs ORDER_PRODUCTS vs ORDER_DETAILS→ORDERS`, `parent_chunk_data_dictionary.txt_1`, `parent_chunk_data_dictionary.txt_2`, `payment_method valid values not documented (credit_card, debit, paypal?)`, `parent_chunk_business_glossary.txt_0`, `Customer's first name→CUSTOMERS`

**Context previews (first 3):**

1. _Business concept 'payment_method valid values not documented (credit_card, debit, paypal?)' is implemented by physical table PAYMENTS (columns: payment_id, PaymentID, order_id, customer_id, payment_da…_

2. _========================================== PAYMENTS ==========================================  Primary Key: payment_id (unverified) | Column Name | Data Type | Constraints | Description | |----------…_

3. _Business concept 'ORDER_ITEMS vs ORDER_PRODUCTS vs ORDER_DETAILS' is implemented by physical table ORDERS (columns: order_id, OrderID, customer_id, CustomerID, order_date, OrderDate, order_status, ord…_

---

### ✅ ec_010 — What's the correct table name: ORDER_ITEMS or ORDER_DETAILS?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.9861 | **Gate:** `proceed`

**Expected answer:**
> The DDL creates a table named ORDER_ITEMS, but the data dictionary header shows 'ORDER_ITEMS (or ORDER_DETAILS?)' and notes 'Table name ambiguity: ORDER_ITEMS vs ORDER_DETAILS'. The actual table name in the schema is ORDER_ITEMS, but documentation suggests the application may reference it differentl…

**System answer:**
> Based on the retrieved context, the physical table name is ORDER_ITEMS.

The strongest support is the mapping: the business concept “Order Item” is implemented by physical table ORDER_ITEMS, with columns such as order_item_id, order_id, product_id, quantity, unit_price, discount_percent, discount_amount, and line_total. The context also says the table comment explicitly names ORDER_ITEMS and refer…

**Sources retrieved (12):** `Order Item`, `parent_chunk_data_dictionary.txt_2`, `ORDER_ITEMS vs ORDER_PRODUCTS vs ORDER_DETAILS→PRODUCTS`, `Order Item→ORDER_ITEMS`, `ORDER_ITEMS vs ORDER_PRODUCTS vs ORDER_DETAILS→ORDERS`, `parent_chunk_data_dictionary.txt_3`, `parent_chunk_data_dictionary.txt_1`, `Customer's first name→CUSTOMERS`

**Context previews (first 3):**

1. _Order Item: The table stores line-level order attributes such as order_id, product_id, quantity, unit_price, discount, and line_total, which is characteristic of an order item/line item structure. The…_

2. _Foreign Keys: - customer_id → CUSTOMERS(customer_id or CustomerID?) - [missing other FK definitions] ========================================== ORDER_ITEMS (or ORDER_DETAILS?) ========================…_

3. _Business concept 'ORDER_ITEMS vs ORDER_PRODUCTS vs ORDER_DETAILS' is implemented by physical table PRODUCTS (columns: product_id, ProductID, product_name, ProductName, product_sku, sku, product_catego…_

---

### ✅ ec_011 — Which date column should be used to track when an order was created: order_date, OrderDate, or created_at?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.8920 | **Gate:** `proceed`

**Expected answer:**
> The ORDERS table has three date-related columns: order_date (DATE type), OrderDate (DATETIME type with different precision), and created_at (TIMESTAMP type). The data dictionary provides no guidance on which is actually used by the application or why three columns exist for potentially the same purp…

**System answer:**
> From the retrieved context alone, I cannot determine a single authoritative choice between order_date, OrderDate, and created_at for “when an order was created.”

What the context does show is that the physical table ORDERS contains all of these columns: order_date, OrderDate, created_at, and updated_at. However, there is no ORDERS data dictionary entry in the provided context that defines the mea…

**Sources retrieved (12):** `ORDER_ITEMS vs ORDER_PRODUCTS vs ORDER_DETAILS→ORDERS`, `payment_method valid values not documented (credit_card, debit, paypal?)→PAYMENTS`, `parent_chunk_data_dictionary.txt_1`, `ORDER_ITEMS vs ORDER_PRODUCTS vs ORDER_DETAILS→PRODUCTS`, `parent_chunk_data_dictionary.txt_3`, `Customer's first name→CUSTOMERS`, `Order Item→ORDER_ITEMS`, `parent_chunk_data_dictionary.txt_2`

**Context previews (first 3):**

1. _Business concept 'ORDER_ITEMS vs ORDER_PRODUCTS vs ORDER_DETAILS' is implemented by physical table ORDERS (columns: order_id, OrderID, customer_id, CustomerID, order_date, OrderDate, order_status, ord…_

2. _Business concept 'payment_method valid values not documented (credit_card, debit, paypal?)' is implemented by physical table PAYMENTS (columns: payment_id, PaymentID, order_id, customer_id, payment_da…_

3. _DATA DICTIONARY - Enterprise Database Version: 2.1 (incomplete documentation) Last Updated: 2024-02-28 ========================================== CUSTOMERS ========================================== P…_

---

### ✅ ec_012 — What does the Failed order status mean?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0031 | **Gate:** `proceed_with_warning`

**Expected answer:**
> The business glossary lists Failed as an order status but marks it as '[definition missing]'. Other statuses have definitions (Pending, Processing, Completed, Cancelled, On Hold), but Failed is undefined despite being a valid status value.

**System answer:**
> The retrieved context does not define what a Failed order status means.

What is known from the context is that the ORDERS table includes an order_status column, and also a payment_status column. The PAYMENTS table also includes payment_status, along with response_code and response_message from the payment gateway. The business glossary says only that an Order “can be in various states,” but it do…

**Sources retrieved (12):** `parent_chunk_data_dictionary.txt_3`, `parent_chunk_data_dictionary.txt_1`, `ORDER_ITEMS vs ORDER_PRODUCTS vs ORDER_DETAILS→ORDERS`, `parent_chunk_data_dictionary.txt_2`, `Order Item→ORDER_ITEMS`, `Order Item`, `payment_method valid values not documented (credit_card, debit, paypal?)→PAYMENTS`, `ORDER_ITEMS vs ORDER_PRODUCTS vs ORDER_DETAILS→PRODUCTS`

**Context previews (first 3):**

1. _========================================== PAYMENTS ==========================================  Primary Key: payment_id (unverified) | Column Name | Data Type | Constraints | Description | |----------…_

2. _DATA DICTIONARY - Enterprise Database Version: 2.1 (incomplete documentation) Last Updated: 2024-02-28 ========================================== CUSTOMERS ========================================== P…_

3. _Business concept 'ORDER_ITEMS vs ORDER_PRODUCTS vs ORDER_DETAILS' is implemented by physical table ORDERS (columns: order_id, OrderID, customer_id, CustomerID, order_date, OrderDate, order_status, ord…_

---

### ✅ ec_013 — Are there any NOT NULL constraints defined in the schema?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.7628 | **Gate:** `proceed`

**Expected answer:**
> No NOT NULL constraints are defined in the DDL. The data dictionary explicitly states 'NOT NULL constraints not defined' under 'Missing Documentation' and notes 'assumed, not verified'. All columns are nullable by default.

**System answer:**
> No explicit NOT NULL constraints are defined in the retrieved context.

In the schema excerpts shown for CUSTOMERS, PAYMENTS, ORDER_ITEMS, and the ORDERS/PRODUCTS concept mappings, the documented constraints are things like PK, FK, UNIQUE?, or unknown indicated by ?. There is no column in the provided context whose constraint is stated as NOT NULL.

The closest available information is that some c…

**Sources retrieved (12):** `parent_chunk_data_dictionary.txt_3`, `parent_chunk_data_dictionary.txt_2`, `parent_chunk_data_dictionary.txt_1`, `ORDER_ITEMS vs ORDER_PRODUCTS vs ORDER_DETAILS→ORDERS`, `payment_method valid values not documented (credit_card, debit, paypal?)→PAYMENTS`, `parent_chunk_business_glossary.txt_0`, `payment_method valid values not documented (credit_card, debit, paypal?)`, `ORDER_ITEMS vs ORDER_PRODUCTS vs ORDER_DETAILS→PRODUCTS`

**Context previews (first 3):**

1. _========================================== PAYMENTS ==========================================  Primary Key: payment_id (unverified) | Column Name | Data Type | Constraints | Description | |----------…_

2. _Foreign Keys: - customer_id → CUSTOMERS(customer_id or CustomerID?) - [missing other FK definitions] ========================================== ORDER_ITEMS (or ORDER_DETAILS?) ========================…_

3. _DATA DICTIONARY - Enterprise Database Version: 2.1 (incomplete documentation) Last Updated: 2024-02-28 ========================================== CUSTOMERS ========================================== P…_

---

### ✅ ec_014 — What's the difference between unit_price and current_price in PRODUCTS?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.5348 | **Gate:** `proceed`

**Expected answer:**
> The PRODUCTS table has both unit_price and current_price columns (both DECIMAL(10,2)). The data dictionary asks 'Different from unit_price?' but provides no explanation of the distinction or when each would be used.

**System answer:**
> The retrieved context does not document a defined difference between unit_price and current_price in PRODUCTS.

What the context does show is that PRODUCTS includes both columns: unit_price and current_price, along with cost_price and other product attributes. However, no descriptions, business rules, or calculation logic are provided for either PRODUCTS.unit_price or PRODUCTS.current_price.

A re…

**Sources retrieved (12):** `ORDER_ITEMS vs ORDER_PRODUCTS vs ORDER_DETAILS→PRODUCTS`, `parent_chunk_data_dictionary.txt_2`, `Order Item→ORDER_ITEMS`, `Order Item`, `ORDER_ITEMS vs ORDER_PRODUCTS vs ORDER_DETAILS→ORDERS`, `parent_chunk_data_dictionary.txt_3`, `parent_chunk_business_glossary.txt_0`, `ORDER_ITEMS vs ORDER_PRODUCTS vs ORDER_DETAILS`

**Context previews (first 3):**

1. _Business concept 'ORDER_ITEMS vs ORDER_PRODUCTS vs ORDER_DETAILS' is implemented by physical table PRODUCTS (columns: product_id, ProductID, product_name, ProductName, product_sku, sku, product_catego…_

2. _Foreign Keys: - customer_id → CUSTOMERS(customer_id or CustomerID?) - [missing other FK definitions] ========================================== ORDER_ITEMS (or ORDER_DETAILS?) ========================…_

3. _Business concept 'Order Item' — The table stores line-level order attributes such as order_id, product_id, quantity, unit_price, discount, and line_total, which is characteristic of an order item/line…_

---

### ✅ ec_015 — When is an invoice generated vs payment processed?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.6598 | **Gate:** `proceed`

**Expected answer:**
> The relationship section in the glossary asks 'An invoice is generated for an order. But when? And can one order have multiple invoices?' indicating the timing and cardinality are not defined. The glossary defines Invoice as 'A document requesting payment. Related to Bill' and Payment as 'The transf…

**System answer:**
> The retrieved context does not contain enough information to say when an invoice is generated versus when a payment is processed.

What is known from the context is only schema-level metadata for payments and orders. The `PAYMENTS` table includes `order_id`, `customer_id`, `payment_date`, `payment_amount`, `payment_method`, `payment_status`, `transaction_id`, `response_code`, `response_message`, a…

**Sources retrieved (12):** `parent_chunk_data_dictionary.txt_3`, `ORDER_ITEMS vs ORDER_PRODUCTS vs ORDER_DETAILS→ORDERS`, `parent_chunk_data_dictionary.txt_1`, `parent_chunk_data_dictionary.txt_2`, `payment_method valid values not documented (credit_card, debit, paypal?)→PAYMENTS`, `parent_chunk_business_glossary.txt_0`, `payment_method valid values not documented (credit_card, debit, paypal?)`, `ORDER_ITEMS vs ORDER_PRODUCTS vs ORDER_DETAILS→PRODUCTS`

**Context previews (first 3):**

1. _========================================== PAYMENTS ==========================================  Primary Key: payment_id (unverified) | Column Name | Data Type | Constraints | Description | |----------…_

2. _Business concept 'ORDER_ITEMS vs ORDER_PRODUCTS vs ORDER_DETAILS' is implemented by physical table ORDERS (columns: order_id, OrderID, customer_id, CustomerID, order_date, OrderDate, order_status, ord…_

3. _DATA DICTIONARY - Enterprise Database Version: 2.1 (incomplete documentation) Last Updated: 2024-02-28 ========================================== CUSTOMERS ========================================== P…_

---

### ✅ ec_016 — Is the sku column in PRODUCTS unique?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.2798 | **Gate:** `proceed`

**Expected answer:**
> The PRODUCTS table has both product_sku and sku columns. The data dictionary notes sku 'should be UNIQUE?' but the DDL does not define a UNIQUE constraint on either column. No index is documented for these columns.

**System answer:**
> The retrieved context shows that PRODUCTS includes product_sku and sku, but it does not document any uniqueness constraint for sku.

So, based on the available context, I cannot confirm that the sku column in PRODUCTS is unique.

**Sources retrieved (12):** `ORDER_ITEMS vs ORDER_PRODUCTS vs ORDER_DETAILS→PRODUCTS`, `parent_chunk_data_dictionary.txt_2`, `parent_chunk_data_dictionary.txt_3`, `ORDER_ITEMS vs ORDER_PRODUCTS vs ORDER_DETAILS→ORDERS`, `parent_chunk_data_dictionary.txt_1`, `Order Item→ORDER_ITEMS`, `Customer's first name→CUSTOMERS`, `payment_method valid values not documented (credit_card, debit, paypal?)→PAYMENTS`

**Context previews (first 3):**

1. _Business concept 'ORDER_ITEMS vs ORDER_PRODUCTS vs ORDER_DETAILS' is implemented by physical table PRODUCTS (columns: product_id, ProductID, product_name, ProductName, product_sku, sku, product_catego…_

2. _Foreign Keys: - customer_id → CUSTOMERS(customer_id or CustomerID?) - [missing other FK definitions] ========================================== ORDER_ITEMS (or ORDER_DETAILS?) ========================…_

3. _========================================== PAYMENTS ==========================================  Primary Key: payment_id (unverified) | Column Name | Data Type | Constraints | Description | |----------…_

---

### ✅ ec_017 — What is the relationship between customers and orders?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0859 | **Gate:** `proceed_with_warning`

**Expected answer:**
> The glossary states 'A customer can place multiple orders. Or is it accounts that place orders?' indicating uncertainty about the relationship. The ORDERS table has both customer_id and CustomerID columns with ambiguous FK references, and the data dictionary notes they reference 'customer (which tab…

**System answer:**
> The retrieved context indicates that customers and orders are related through the ORDERS table’s customer identifier. The physical table mapped to the business concept includes ORDERS columns customer_id and CustomerID, while the CUSTOMERS table has customer_id and CustomerID as the customer key fields. So, at the schema level, an order is associated to a customer via ORDERS.customer_id or ORDERS.…

**Sources retrieved (12):** `parent_chunk_data_dictionary.txt_3`, `parent_chunk_data_dictionary.txt_2`, `ORDER_ITEMS vs ORDER_PRODUCTS vs ORDER_DETAILS→ORDERS`, `parent_chunk_data_dictionary.txt_1`, `Customer's first name→CUSTOMERS`, `Order Item→ORDER_ITEMS`, `Order Item`, `parent_chunk_business_glossary.txt_0`

**Context previews (first 3):**

1. _========================================== PAYMENTS ==========================================  Primary Key: payment_id (unverified) | Column Name | Data Type | Constraints | Description | |----------…_

2. _Foreign Keys: - customer_id → CUSTOMERS(customer_id or CustomerID?) - [missing other FK definitions] ========================================== ORDER_ITEMS (or ORDER_DETAILS?) ========================…_

3. _Business concept 'ORDER_ITEMS vs ORDER_PRODUCTS vs ORDER_DETAILS' is implemented by physical table ORDERS (columns: order_id, OrderID, customer_id, CustomerID, order_date, OrderDate, order_status, ord…_

---

### ✅ ec_018 — Which price column represents what the customer actually pays?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0426 | **Gate:** `proceed_with_warning`

**Expected answer:**
> Multiple price columns exist across tables: ORDERS has orderAmount and total_amount; ORDER_ITEMS has unit_price and UnitPrice; PRODUCTS has unit_price, current_price, and cost_price. The data dictionary does not explain which represents the final customer price, whether discounts are applied, or how…

**System answer:**
> The retrieved context does not identify a single canonical column as “what the customer actually pays.”

What it does show is that ORDER_ITEMS contains unit_price, discount_percent, discount_amount, and line_total at the line-item level; ORDERS contains orderAmount and total_amount at the order level, along with shippingAmount and tax_amount; and PAYMENTS contains payment_amount for recorded payme…

**Sources retrieved (12):** `payment_method valid values not documented (credit_card, debit, paypal?)→PAYMENTS`, `ORDER_ITEMS vs ORDER_PRODUCTS vs ORDER_DETAILS→ORDERS`, `parent_chunk_data_dictionary.txt_2`, `parent_chunk_data_dictionary.txt_3`, `ORDER_ITEMS vs ORDER_PRODUCTS vs ORDER_DETAILS→PRODUCTS`, `Customer's first name→CUSTOMERS`, `parent_chunk_data_dictionary.txt_1`, `Order Item→ORDER_ITEMS`

**Context previews (first 3):**

1. _Business concept 'payment_method valid values not documented (credit_card, debit, paypal?)' is implemented by physical table PAYMENTS (columns: payment_id, PaymentID, order_id, customer_id, payment_da…_

2. _Business concept 'ORDER_ITEMS vs ORDER_PRODUCTS vs ORDER_DETAILS' is implemented by physical table ORDERS (columns: order_id, OrderID, customer_id, CustomerID, order_date, OrderDate, order_status, ord…_

3. _Foreign Keys: - customer_id → CUSTOMERS(customer_id or CustomerID?) - [missing other FK definitions] ========================================== ORDER_ITEMS (or ORDER_DETAILS?) ========================…_

---

### ✅ ec_019 — What's the difference between Shipment, Delivery, and Fulfillment?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0050 | **Gate:** `proceed_with_warning`

**Expected answer:**
> The glossary provides definitions but unclear boundaries: Shipment is 'The process of delivering goods to a customer'; Delivery is 'The completion of a Shipment when goods reach the customer'; Fulfillment is 'The process of preparing and delivering orders. Encompasses Shipment and Delivery.' The exa…

**System answer:**
> I cannot determine the difference between Shipment, Delivery, and Fulfillment from the retrieved context.

What is known is that the context includes a partial business glossary for an enterprise system, with some entries under Customer Management and Order & Transaction, such as Customer, Client, Account Holder, End User, Order, and Transaction. However, there are no glossary definitions or schem…

**Sources retrieved (12):** `parent_chunk_data_dictionary.txt_2`, `parent_chunk_data_dictionary.txt_3`, `Order Item→ORDER_ITEMS`, `Order Item`, `parent_chunk_business_glossary.txt_0`, `ORDER_ITEMS vs ORDER_PRODUCTS vs ORDER_DETAILS→ORDERS`, `parent_chunk_data_dictionary.txt_1`, `ORDER_ITEMS vs ORDER_PRODUCTS vs ORDER_DETAILS→PRODUCTS`

**Context previews (first 3):**

1. _Foreign Keys: - customer_id → CUSTOMERS(customer_id or CustomerID?) - [missing other FK definitions] ========================================== ORDER_ITEMS (or ORDER_DETAILS?) ========================…_

2. _========================================== PAYMENTS ==========================================  Primary Key: payment_id (unverified) | Column Name | Data Type | Constraints | Description | |----------…_

3. _Business concept 'Order Item' — The table stores line-level order attributes such as order_id, product_id, quantity, unit_price, discount, and line_total, which is characteristic of an order item/line…_

---

### ✅ ec_020 — Are foreign key constraints enforced in the schema?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.1603 | **Gate:** `proceed_with_warning`

**Expected answer:**
> No foreign key constraints are enforced in the DDL. While the data dictionary documents FK relationships (e.g., customer_id → CUSTOMERS, order_id → ORDERS), the actual CREATE TABLE statements omit the REFERENCES clauses. The schema explicitly notes 'FK constraints defined in data dictionary but not …

**System answer:**
> The retrieved context does not confirm that foreign key constraints are actually enforced by the database.

What the context does show is schema metadata that labels some columns as foreign keys or says they reference other tables:
ORDER_ITEMS.order_id is marked FK and “References ORDERS,” ORDER_ITEMS.product_id is marked FK and “References PRODUCTS (or INVENTORY?),” PAYMENTS.order_id is marked FK…

**Sources retrieved (12):** `parent_chunk_data_dictionary.txt_2`, `parent_chunk_data_dictionary.txt_3`, `parent_chunk_data_dictionary.txt_1`, `parent_chunk_business_glossary.txt_0`, `Order Item`, `payment_method valid values not documented (credit_card, debit, paypal?)→PAYMENTS`, `ORDER_ITEMS vs ORDER_PRODUCTS vs ORDER_DETAILS→ORDERS`, `Customer's first name→CUSTOMERS`

**Context previews (first 3):**

1. _Foreign Keys: - customer_id → CUSTOMERS(customer_id or CustomerID?) - [missing other FK definitions] ========================================== ORDER_ITEMS (or ORDER_DETAILS?) ========================…_

2. _========================================== PAYMENTS ==========================================  Primary Key: payment_id (unverified) | Column Name | Data Type | Constraints | Description | |----------…_

3. _DATA DICTIONARY - Enterprise Database Version: 2.1 (incomplete documentation) Last Updated: 2024-02-28 ========================================== CUSTOMERS ========================================== P…_

---

## Anomalies & Observations

No anomalies detected. All questions grounded with acceptable RAGAS scores.
