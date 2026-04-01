# AB-12 — 05_edgecases_incomplete — Run Analysis

**Timestamp:** 2026-04-01 02:55:15  
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
| ER similarity threshold | `0.85` |

## Builder Results

| Metric | Value |
|--------|-------|
| Triplets extracted | 214 |
| Entities resolved | 156 |
| Tables parsed | 5 |
| Tables completed | 5 |

## Query Evaluation Summary

| Metric | Value |
|--------|-------|
| Questions | 20 |
| Grounded | **20/20 (100%)** |
| Avg GT Coverage | 100% |
| Avg Top Score | 0.4732 |
| Avg Chunk Count | 9.0 |
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
> In the business glossary, Customer is defined only partially as “An individual or organization that...”; the definition is marked incomplete. The glossary also notes that Client is “a person or company that purchases goods or services” and may be used interchangeably with Customer in some contexts. It distinguishes Account Holder as the primary owner of an account, similar to Customer but in an ac…

**Sources retrieved (9):** `Customer→CUSTOMERS`, `parent_chunk_data_dictionary.txt_1`, `parent_chunk_data_dictionary.txt_2`, `parent_chunk_data_dictionary.txt_3`, `Order→ORDERS`, `Payment→PAYMENTS`, `parent_chunk_business_glossary.txt_0`, `Order→ORDER_ITEMS`

**Context previews (first 3):**

1. _Business concept 'Customer' is implemented by physical table CUSTOMERS (columns: customer_id, CustomerID, firstName, first_name, lastName, last_name, email, emailAddress, phone, phoneNumber, created_a…_

2. _DATA DICTIONARY - Enterprise Database Version: 2.1 (incomplete documentation) Last Updated: 2024-02-28 ========================================== CUSTOMERS ========================================== P…_

3. _Foreign Keys: - customer_id → CUSTOMERS(customer_id or CustomerID?) - [missing other FK definitions] ========================================== ORDER_ITEMS (or ORDER_DETAILS?) ========================…_

---

### ✅ ec_002 — What's the difference between firstName and first_name in the CUSTOMERS table?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.5087 | **Gate:** `proceed`

**Expected answer:**
> Both columns exist in the CUSTOMERS table with identical VARCHAR(50) data types. The data dictionary notes they appear to be duplicates resulting from inconsistent naming conventions (snake_case vs camelCase), but the actual usage by the application is not documented.

**System answer:**
> From the retrieved context, there is no documented business difference between `firstName` and `first_name` in `CUSTOMERS`.

The data dictionary says:
`firstName` is `VARCHAR(50)` and described as “Customer's first name.”
`first_name` is also `VARCHAR(50)` and is noted as “[appears to be duplicate].”

So, based on the available metadata, both columns appear to represent the same attribute, with di…

**Sources retrieved (9):** `Customer→CUSTOMERS`, `parent_chunk_data_dictionary.txt_1`, `parent_chunk_data_dictionary.txt_2`, `parent_chunk_data_dictionary.txt_3`, `parent_chunk_business_glossary.txt_0`, `Order→ORDERS`, `Payment→PAYMENTS`, `Inventory Item→PRODUCTS`

**Context previews (first 3):**

1. _Business concept 'Customer' is implemented by physical table CUSTOMERS (columns: customer_id, CustomerID, firstName, first_name, lastName, last_name, email, emailAddress, phone, phoneNumber, created_a…_

2. _DATA DICTIONARY - Enterprise Database Version: 2.1 (incomplete documentation) Last Updated: 2024-02-28 ========================================== CUSTOMERS ========================================== P…_

3. _Foreign Keys: - customer_id → CUSTOMERS(customer_id or CustomerID?) - [missing other FK definitions] ========================================== ORDER_ITEMS (or ORDER_DETAILS?) ========================…_

---

### ✅ ec_003 — Which customer column should be used as a foreign key reference: customer_id or CustomerID?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.9258 | **Gate:** `proceed`

**Expected answer:**
> The CUSTOMERS table has both customer_id (defined as PRIMARY KEY) and CustomerID (defined as INTEGER with no constraints). The ORDERS table also has both customer_id and CustomerID columns with ambiguous FK references. The data dictionary indicates this inconsistency is documented but not yet resolv…

**System answer:**
> The retrieved context does not definitively resolve this. The documentation is inconsistent.

What the context shows is:
The `CUSTOMERS` table lists `customer_id` as the primary key, but with an explicit note: “`customer_id` (or is it `CustomerID`? check with DBA)”.
`CustomerID` is separately described as a “possible duplicate of `customer_id`”.
The foreign key notes also say `customer_id → CUSTOM…

**Sources retrieved (9):** `parent_chunk_data_dictionary.txt_2`, `parent_chunk_data_dictionary.txt_1`, `Customer→CUSTOMERS`, `parent_chunk_data_dictionary.txt_3`, `Order→ORDERS`, `Payment→PAYMENTS`, `Order→ORDER_ITEMS`, `Inventory Item→PRODUCTS`

**Context previews (first 3):**

1. _Foreign Keys: - customer_id → CUSTOMERS(customer_id or CustomerID?) - [missing other FK definitions] ========================================== ORDER_ITEMS (or ORDER_DETAILS?) ========================…_

2. _DATA DICTIONARY - Enterprise Database Version: 2.1 (incomplete documentation) Last Updated: 2024-02-28 ========================================== CUSTOMERS ========================================== P…_

3. _Business concept 'Customer' is implemented by physical table CUSTOMERS (columns: customer_id, CustomerID, firstName, first_name, lastName, last_name, email, emailAddress, phone, phoneNumber, created_a…_

---

### ✅ ec_004 — What are the valid values for order_status?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.3951 | **Gate:** `proceed`

**Expected answer:**
> The business glossary documents several order statuses: Pending, Processing, Completed, Cancelled, On Hold, and Failed (which is marked as [definition missing]). However, these are not enforced by a CHECK constraint in the schema, and the data dictionary notes that valid values reference '[missing d…

**System answer:**
> The retrieved context does not provide the valid values for `order_status`.

What it does confirm is that `order_status` is a column on the `ORDERS` table, and the business concept `Order` is implemented by `ORDERS`. The business glossary also says an Order “can be in various states,” but it does not enumerate those states.

So, from the available context:
`order_status` exists on `ORDERS`, but it…

**Sources retrieved (9):** `parent_chunk_data_dictionary.txt_3`, `Order→ORDERS`, `parent_chunk_data_dictionary.txt_1`, `parent_chunk_data_dictionary.txt_2`, `parent_chunk_business_glossary.txt_0`, `Payment→PAYMENTS`, `Order→ORDER_ITEMS`, `Customer→CUSTOMERS`

**Context previews (first 3):**

1. _========================================== PAYMENTS ==========================================  Primary Key: payment_id (unverified) | Column Name | Data Type | Constraints | Description | |----------…_

2. _Business concept 'Order' is implemented by physical table ORDERS (columns: order_id, OrderID, customer_id, CustomerID, order_date, OrderDate, order_status, orderAmount, total_amount, shippingAmount, t…_

3. _DATA DICTIONARY - Enterprise Database Version: 2.1 (incomplete documentation) Last Updated: 2024-02-28 ========================================== CUSTOMERS ========================================== P…_

---

### ✅ ec_005 — Is there a difference between Product, Item, and SKU?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.5696 | **Gate:** `proceed`

**Expected answer:**
> The glossary indicates these terms are related but distinct: Product is defined as "A thing that is... [definition needs clarification]"; Item is a synonym for Product used in inventory context; SKU (Stock Keeping Unit) is a unique identifier for a product variant; Inventory Item refers to physical …

**System answer:**
> From the retrieved context, there is no explicit glossary definition that distinguishes “Product,” “Item,” and “SKU” as three separate business concepts.

What the context does show is this:

The only explicit concept mapping here is “Inventory Item,” and it is implemented by the physical table PRODUCTS. That table contains product-level attributes such as product_id/ProductID, product_name/Produc…

**Sources retrieved (9):** `Inventory Item→PRODUCTS`, `parent_chunk_data_dictionary.txt_2`, `Order→ORDER_ITEMS`, `parent_chunk_data_dictionary.txt_1`, `parent_chunk_data_dictionary.txt_3`, `parent_chunk_business_glossary.txt_0`, `Order→ORDERS`, `Customer→CUSTOMERS`

**Context previews (first 3):**

1. _Business concept 'Inventory Item' is implemented by physical table PRODUCTS (columns: product_id, ProductID, product_name, ProductName, product_sku, sku, product_category, category, unit_price, curren…_

2. _Foreign Keys: - customer_id → CUSTOMERS(customer_id or CustomerID?) - [missing other FK definitions] ========================================== ORDER_ITEMS (or ORDER_DETAILS?) ========================…_

3. _Business concept 'Order' is implemented by physical table ORDER_ITEMS (columns: order_item_id, order_id, product_id, ProductID, quantity, unit_price, UnitPrice, discount_percent, discount_amount, line…_

---

### ✅ ec_006 — Which table should ORDER_ITEMS.product_id reference: PRODUCTS or INVENTORY?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.9608 | **Gate:** `proceed`

**Expected answer:**
> The data dictionary states the FK reference is to 'PRODUCTS (or INVENTORY?)' and notes it is 'not verified'. The schema provides two potential targets: PRODUCTS table (which has product_id) and an INVENTORY table that is referenced in documentation but not defined in the DDL. The actual relationship…

**System answer:**
> Based on the retrieved context, ORDER_ITEMS.product_id should reference PRODUCTS.

The evidence is:
ORDER_ITEMS documents product_id as an FK with the note “References PRODUCTS (or INVENTORY?)”.
The business concept “Inventory Item” is explicitly implemented by the physical table PRODUCTS, which contains product_id/ProductID and the product attributes.

There is no physical table named INVENTORY d…

**Sources retrieved (9):** `parent_chunk_data_dictionary.txt_2`, `Inventory Item→PRODUCTS`, `Order→ORDER_ITEMS`, `parent_chunk_data_dictionary.txt_3`, `parent_chunk_data_dictionary.txt_1`, `parent_chunk_business_glossary.txt_0`, `Order→ORDERS`, `Payment→PAYMENTS`

**Context previews (first 3):**

1. _Foreign Keys: - customer_id → CUSTOMERS(customer_id or CustomerID?) - [missing other FK definitions] ========================================== ORDER_ITEMS (or ORDER_DETAILS?) ========================…_

2. _Business concept 'Inventory Item' is implemented by physical table PRODUCTS (columns: product_id, ProductID, product_name, ProductName, product_sku, sku, product_category, category, unit_price, curren…_

3. _Business concept 'Order' is implemented by physical table ORDER_ITEMS (columns: order_item_id, order_id, product_id, ProductID, quantity, unit_price, UnitPrice, discount_percent, discount_amount, line…_

---

### ✅ ec_007 — What's the difference between Revenue and Sales?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.4224 | **Gate:** `proceed`

**Expected answer:**
> Both terms show circular definitions: Revenue is defined as 'Income from sales. The same as... [definition circular, see Sales]', while Sales is defined as 'Revenue from selling products. See Revenue.' The glossary provides no clear distinction between these concepts.

**System answer:**
> The retrieved context does not define the business concepts Revenue or Sales, so I cannot state their difference from the knowledge graph.

What the context does provide is related order/payment metadata:
Order is defined in the business glossary as “a request to purchase products or services” and is implemented by ORDERS.
Payment is implemented by PAYMENTS, which includes payment_amount, payment_…

**Sources retrieved (9):** `parent_chunk_data_dictionary.txt_2`, `parent_chunk_data_dictionary.txt_3`, `parent_chunk_business_glossary.txt_0`, `parent_chunk_data_dictionary.txt_1`, `Order→ORDERS`, `Payment→PAYMENTS`, `Order→ORDER_ITEMS`, `Customer→CUSTOMERS`

**Context previews (first 3):**

1. _Foreign Keys: - customer_id → CUSTOMERS(customer_id or CustomerID?) - [missing other FK definitions] ========================================== ORDER_ITEMS (or ORDER_DETAILS?) ========================…_

2. _========================================== PAYMENTS ==========================================  Primary Key: payment_id (unverified) | Column Name | Data Type | Constraints | Description | |----------…_

3. _BUSINESS GLOSSARY - Enterprise System Last Updated: 2024-03-15 Status: Partial (pending review) ========================================== CUSTOMER MANAGEMENT =========================================…_

---

### ✅ ec_008 — Can one order have multiple payments?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0981 | **Gate:** `proceed_with_warning`

**Expected answer:**
> The PAYMENTS table has an order_id column, suggesting a many-to-one relationship (multiple payments can reference a single order). However, the relationship section in the glossary asks 'Or is it one-to-one?' indicating uncertainty. The ORDERS table has both payment_status and payment_method columns…

**System answer:**
> Yes, based on the schema metadata, one order can have multiple payments.

The evidence is in the PAYMENTS table: it has its own primary key, payment_id, and a separate foreign key, order_id, that references ORDERS. Because order_id in PAYMENTS is documented only as a foreign key and there is no uniqueness constraint shown on order_id, the table structure allows multiple PAYMENTS rows to reference …

**Sources retrieved (9):** `parent_chunk_data_dictionary.txt_3`, `Payment→PAYMENTS`, `Order→ORDERS`, `parent_chunk_data_dictionary.txt_2`, `parent_chunk_data_dictionary.txt_1`, `Order→ORDER_ITEMS`, `Inventory Item→PRODUCTS`, `Customer→CUSTOMERS`

**Context previews (first 3):**

1. _========================================== PAYMENTS ==========================================  Primary Key: payment_id (unverified) | Column Name | Data Type | Constraints | Description | |----------…_

2. _Business concept 'Payment' is implemented by physical table PAYMENTS (columns: payment_id, PaymentID, order_id, customer_id, payment_date, payment_amount, payment_method, payment_status, transaction_i…_

3. _Business concept 'Order' is implemented by physical table ORDERS (columns: order_id, OrderID, customer_id, CustomerID, order_date, OrderDate, order_status, orderAmount, total_amount, shippingAmount, t…_

---

### ✅ ec_009 — What payment methods are accepted?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.1791 | **Gate:** `proceed_with_warning`

**Expected answer:**
> The PAYMENTS table has a payment_method column (VARCHAR(30)), but the data dictionary notes '[missing valid values]' and no CHECK constraint exists to enumerate acceptable methods. The schema does not document what values are valid (e.g., credit_card, debit, paypal, etc.).

**System answer:**
> The retrieved context shows a payment_method field in both PAYMENTS and ORDERS. In PAYMENTS, payment_method is defined as VARCHAR(30), but its description explicitly says “[missing valid values].” The ORDERS table also includes payment_method, but no accepted values are documented there either.

So, the knowledge graph indicates that payment methods are tracked, but it does not specify which payme…

**Sources retrieved (9):** `parent_chunk_data_dictionary.txt_3`, `Payment→PAYMENTS`, `Order→ORDERS`, `parent_chunk_data_dictionary.txt_1`, `parent_chunk_data_dictionary.txt_2`, `parent_chunk_business_glossary.txt_0`, `Customer→CUSTOMERS`, `Order→ORDER_ITEMS`

**Context previews (first 3):**

1. _========================================== PAYMENTS ==========================================  Primary Key: payment_id (unverified) | Column Name | Data Type | Constraints | Description | |----------…_

2. _Business concept 'Payment' is implemented by physical table PAYMENTS (columns: payment_id, PaymentID, order_id, customer_id, payment_date, payment_amount, payment_method, payment_status, transaction_i…_

3. _Business concept 'Order' is implemented by physical table ORDERS (columns: order_id, OrderID, customer_id, CustomerID, order_date, OrderDate, order_status, orderAmount, total_amount, shippingAmount, t…_

---

### ✅ ec_010 — What's the correct table name: ORDER_ITEMS or ORDER_DETAILS?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.9627 | **Gate:** `proceed`

**Expected answer:**
> The DDL creates a table named ORDER_ITEMS, but the data dictionary header shows 'ORDER_ITEMS (or ORDER_DETAILS?)' and notes 'Table name ambiguity: ORDER_ITEMS vs ORDER_DETAILS'. The actual table name in the schema is ORDER_ITEMS, but documentation suggests the application may reference it differentl…

**System answer:**
> The retrieved context does not confirm a definitive answer, but it supports ORDER_ITEMS more strongly than ORDER_DETAILS.

Here’s why: the schema excerpt labels the section as “ORDER_ITEMS (or ORDER_DETAILS?)”, which explicitly shows uncertainty in the documentation. However, the business concept mapping states that the business concept “Order” is implemented by physical table ORDER_ITEMS, and the…

**Sources retrieved (9):** `parent_chunk_data_dictionary.txt_2`, `Order→ORDER_ITEMS`, `Inventory Item→PRODUCTS`, `parent_chunk_data_dictionary.txt_3`, `parent_chunk_data_dictionary.txt_1`, `Customer→CUSTOMERS`, `Order→ORDERS`, `Payment→PAYMENTS`

**Context previews (first 3):**

1. _Foreign Keys: - customer_id → CUSTOMERS(customer_id or CustomerID?) - [missing other FK definitions] ========================================== ORDER_ITEMS (or ORDER_DETAILS?) ========================…_

2. _Business concept 'Order' is implemented by physical table ORDER_ITEMS (columns: order_item_id, order_id, product_id, ProductID, quantity, unit_price, UnitPrice, discount_percent, discount_amount, line…_

3. _Business concept 'Inventory Item' is implemented by physical table PRODUCTS (columns: product_id, ProductID, product_name, ProductName, product_sku, sku, product_category, category, unit_price, curren…_

---

### ✅ ec_011 — Which date column should be used to track when an order was created: order_date, OrderDate, or created_at?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.9395 | **Gate:** `proceed`

**Expected answer:**
> The ORDERS table has three date-related columns: order_date (DATE type), OrderDate (DATETIME type with different precision), and created_at (TIMESTAMP type). The data dictionary provides no guidance on which is actually used by the application or why three columns exist for potentially the same purp…

**System answer:**
> From the retrieved context, the business concept Order is implemented by the ORDERS table, and that table includes all three columns: order_date, OrderDate, and created_at.

The context does not explicitly document which one is the authoritative column for “when an order was created,” so this cannot be determined definitively from the knowledge graph alone. The strongest schema-level indication is…

**Sources retrieved (9):** `Order→ORDERS`, `Payment→PAYMENTS`, `parent_chunk_data_dictionary.txt_1`, `parent_chunk_data_dictionary.txt_3`, `Customer→CUSTOMERS`, `Inventory Item→PRODUCTS`, `Order→ORDER_ITEMS`, `parent_chunk_data_dictionary.txt_2`

**Context previews (first 3):**

1. _Business concept 'Order' is implemented by physical table ORDERS (columns: order_id, OrderID, customer_id, CustomerID, order_date, OrderDate, order_status, orderAmount, total_amount, shippingAmount, t…_

2. _Business concept 'Payment' is implemented by physical table PAYMENTS (columns: payment_id, PaymentID, order_id, customer_id, payment_date, payment_amount, payment_method, payment_status, transaction_i…_

3. _DATA DICTIONARY - Enterprise Database Version: 2.1 (incomplete documentation) Last Updated: 2024-02-28 ========================================== CUSTOMERS ========================================== P…_

---

### ✅ ec_012 — What does the Failed order status mean?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0031 | **Gate:** `proceed_with_warning`

**Expected answer:**
> The business glossary lists Failed as an order status but marks it as '[definition missing]'. Other statuses have definitions (Pending, Processing, Completed, Cancelled, On Hold), but Failed is undefined despite being a valid status value.

**System answer:**
> The retrieved context does not define a “Failed” value for `ORDERS.order_status`, so its meaning cannot be determined from the knowledge graph.

What the context does show is that the business concept `Order` is implemented by the `ORDERS` table, which includes an `order_status` column, and the glossary says an order “can be in various states.” However, no valid values, status definitions, or busi…

**Sources retrieved (9):** `parent_chunk_data_dictionary.txt_3`, `parent_chunk_data_dictionary.txt_1`, `Order→ORDERS`, `parent_chunk_data_dictionary.txt_2`, `Payment→PAYMENTS`, `Order→ORDER_ITEMS`, `Customer→CUSTOMERS`, `Inventory Item→PRODUCTS`

**Context previews (first 3):**

1. _========================================== PAYMENTS ==========================================  Primary Key: payment_id (unverified) | Column Name | Data Type | Constraints | Description | |----------…_

2. _DATA DICTIONARY - Enterprise Database Version: 2.1 (incomplete documentation) Last Updated: 2024-02-28 ========================================== CUSTOMERS ========================================== P…_

3. _Business concept 'Order' is implemented by physical table ORDERS (columns: order_id, OrderID, customer_id, CustomerID, order_date, OrderDate, order_status, orderAmount, total_amount, shippingAmount, t…_

---

### ✅ ec_013 — Are there any NOT NULL constraints defined in the schema?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.7628 | **Gate:** `proceed`

**Expected answer:**
> No NOT NULL constraints are defined in the DDL. The data dictionary explicitly states 'NOT NULL constraints not defined' under 'Missing Documentation' and notes 'assumed, not verified'. All columns are nullable by default.

**System answer:**
> No explicit NOT NULL constraints are defined in the retrieved schema context.

The only constraints shown in the provided table metadata are things like PK, FK, and a possible UNIQUE? on PAYMENTS.transaction_id. For example:
CUSTOMERS shows customer_id as PK.
PAYMENTS shows payment_id as PK, order_id and customer_id as FK, and transaction_id as UNIQUE?.
ORDER_ITEMS shows order_item_id as PK, and o…

**Sources retrieved (9):** `parent_chunk_data_dictionary.txt_3`, `parent_chunk_data_dictionary.txt_2`, `parent_chunk_data_dictionary.txt_1`, `Order→ORDERS`, `parent_chunk_business_glossary.txt_0`, `Inventory Item→PRODUCTS`, `Customer→CUSTOMERS`, `Order→ORDER_ITEMS`

**Context previews (first 3):**

1. _========================================== PAYMENTS ==========================================  Primary Key: payment_id (unverified) | Column Name | Data Type | Constraints | Description | |----------…_

2. _Foreign Keys: - customer_id → CUSTOMERS(customer_id or CustomerID?) - [missing other FK definitions] ========================================== ORDER_ITEMS (or ORDER_DETAILS?) ========================…_

3. _DATA DICTIONARY - Enterprise Database Version: 2.1 (incomplete documentation) Last Updated: 2024-02-28 ========================================== CUSTOMERS ========================================== P…_

---

### ✅ ec_014 — What's the difference between unit_price and current_price in PRODUCTS?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.4761 | **Gate:** `proceed`

**Expected answer:**
> The PRODUCTS table has both unit_price and current_price columns (both DECIMAL(10,2)). The data dictionary asks 'Different from unit_price?' but provides no explanation of the distinction or when each would be used.

**System answer:**
> From the retrieved context, both unit_price and current_price are columns on PRODUCTS, which implements the business concept Inventory Item.

What the context does support is this:
PRODUCTS includes unit_price, current_price, cost_price, stock_quantity, quantity_in_stock, reorder_level, and other item attributes.
Elsewhere, ORDER_ITEMS also has a unit_price column, and there it is explicitly descr…

**Sources retrieved (9):** `Inventory Item→PRODUCTS`, `parent_chunk_data_dictionary.txt_2`, `Order→ORDER_ITEMS`, `parent_chunk_data_dictionary.txt_3`, `parent_chunk_business_glossary.txt_0`, `parent_chunk_data_dictionary.txt_1`, `Order→ORDERS`, `Payment→PAYMENTS`

**Context previews (first 3):**

1. _Business concept 'Inventory Item' is implemented by physical table PRODUCTS (columns: product_id, ProductID, product_name, ProductName, product_sku, sku, product_category, category, unit_price, curren…_

2. _Foreign Keys: - customer_id → CUSTOMERS(customer_id or CustomerID?) - [missing other FK definitions] ========================================== ORDER_ITEMS (or ORDER_DETAILS?) ========================…_

3. _Business concept 'Order' is implemented by physical table ORDER_ITEMS (columns: order_item_id, order_id, product_id, ProductID, quantity, unit_price, UnitPrice, discount_percent, discount_amount, line…_

---

### ✅ ec_015 — When is an invoice generated vs payment processed?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.6598 | **Gate:** `proceed`

**Expected answer:**
> The relationship section in the glossary asks 'An invoice is generated for an order. But when? And can one order have multiple invoices?' indicating the timing and cardinality are not defined. The glossary defines Invoice as 'A document requesting payment. Related to Bill' and Payment as 'The transf…

**System answer:**
> The retrieved context does not define any invoice concept, invoice table, or rule for invoice generation, so it cannot determine when an invoice is generated.

For payment processing, the context only shows schema metadata for the `PAYMENTS` table and related concepts. It indicates that a payment is recorded in `PAYMENTS`, which includes `payment_date`, `payment_amount`, `payment_method`, `payment…

**Sources retrieved (9):** `parent_chunk_data_dictionary.txt_3`, `Payment→PAYMENTS`, `parent_chunk_data_dictionary.txt_1`, `parent_chunk_data_dictionary.txt_2`, `Order→ORDERS`, `parent_chunk_business_glossary.txt_0`, `Inventory Item→PRODUCTS`, `Order→ORDER_ITEMS`

**Context previews (first 3):**

1. _========================================== PAYMENTS ==========================================  Primary Key: payment_id (unverified) | Column Name | Data Type | Constraints | Description | |----------…_

2. _Business concept 'Payment' is implemented by physical table PAYMENTS (columns: payment_id, PaymentID, order_id, customer_id, payment_date, payment_amount, payment_method, payment_status, transaction_i…_

3. _DATA DICTIONARY - Enterprise Database Version: 2.1 (incomplete documentation) Last Updated: 2024-02-28 ========================================== CUSTOMERS ========================================== P…_

---

### ✅ ec_016 — Is the sku column in PRODUCTS unique?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.3824 | **Gate:** `proceed`

**Expected answer:**
> The PRODUCTS table has both product_sku and sku columns. The data dictionary notes sku 'should be UNIQUE?' but the DDL does not define a UNIQUE constraint on either column. No index is documented for these columns.

**System answer:**
> The retrieved context shows that PRODUCTS includes product_sku and sku as columns under the business concept Inventory Item, but it does not provide any uniqueness constraint for either column. So from the available context, it cannot be determined whether sku in PRODUCTS is unique.

**Sources retrieved (9):** `Inventory Item→PRODUCTS`, `parent_chunk_data_dictionary.txt_2`, `parent_chunk_data_dictionary.txt_3`, `Order→ORDER_ITEMS`, `parent_chunk_data_dictionary.txt_1`, `Order→ORDERS`, `Customer→CUSTOMERS`, `Payment→PAYMENTS`

**Context previews (first 3):**

1. _Business concept 'Inventory Item' is implemented by physical table PRODUCTS (columns: product_id, ProductID, product_name, ProductName, product_sku, sku, product_category, category, unit_price, curren…_

2. _Foreign Keys: - customer_id → CUSTOMERS(customer_id or CustomerID?) - [missing other FK definitions] ========================================== ORDER_ITEMS (or ORDER_DETAILS?) ========================…_

3. _========================================== PAYMENTS ==========================================  Primary Key: payment_id (unverified) | Column Name | Data Type | Constraints | Description | |----------…_

---

### ✅ ec_017 — What is the relationship between customers and orders?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0859 | **Gate:** `proceed_with_warning`

**Expected answer:**
> The glossary states 'A customer can place multiple orders. Or is it accounts that place orders?' indicating uncertainty about the relationship. The ORDERS table has both customer_id and CustomerID columns with ambiguous FK references, and the data dictionary notes they reference 'customer (which tab…

**System answer:**
> The business concept Customer is implemented by the CUSTOMERS table, and the business concept Order is implemented by the ORDERS table.

The relationship between them is that ORDERS contains a customer reference: the ORDERS table includes customer_id and CustomerID columns, and the retrieved schema notes a foreign key customer_id → CUSTOMERS(customer_id or CustomerID?). Based on that metadata, eac…

**Sources retrieved (9):** `parent_chunk_data_dictionary.txt_3`, `Order→ORDERS`, `parent_chunk_data_dictionary.txt_2`, `parent_chunk_data_dictionary.txt_1`, `Customer→CUSTOMERS`, `parent_chunk_business_glossary.txt_0`, `Payment→PAYMENTS`, `Order→ORDER_ITEMS`

**Context previews (first 3):**

1. _========================================== PAYMENTS ==========================================  Primary Key: payment_id (unverified) | Column Name | Data Type | Constraints | Description | |----------…_

2. _Business concept 'Order' is implemented by physical table ORDERS (columns: order_id, OrderID, customer_id, CustomerID, order_date, OrderDate, order_status, orderAmount, total_amount, shippingAmount, t…_

3. _Foreign Keys: - customer_id → CUSTOMERS(customer_id or CustomerID?) - [missing other FK definitions] ========================================== ORDER_ITEMS (or ORDER_DETAILS?) ========================…_

---

### ✅ ec_018 — Which price column represents what the customer actually pays?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0965 | **Gate:** `proceed_with_warning`

**Expected answer:**
> Multiple price columns exist across tables: ORDERS has orderAmount and total_amount; ORDER_ITEMS has unit_price and UnitPrice; PRODUCTS has unit_price, current_price, and cost_price. The data dictionary does not explain which represents the final customer price, whether discounts are applied, or how…

**System answer:**
> Based on the schema shown, the closest column to “what the customer actually pays” is PAYMENTS.payment_amount, because it is the amount recorded on a payment in the PAYMENTS table.

The other columns appear to represent related order pricing components, but the documentation does not explicitly define them:
ORDERS.orderAmount and ORDERS.total_amount are both order-level amount fields, but no descr…

**Sources retrieved (9):** `Payment→PAYMENTS`, `Order→ORDERS`, `parent_chunk_data_dictionary.txt_2`, `parent_chunk_data_dictionary.txt_3`, `Order→ORDER_ITEMS`, `Customer→CUSTOMERS`, `parent_chunk_data_dictionary.txt_1`, `Inventory Item→PRODUCTS`

**Context previews (first 3):**

1. _Business concept 'Payment' is implemented by physical table PAYMENTS (columns: payment_id, PaymentID, order_id, customer_id, payment_date, payment_amount, payment_method, payment_status, transaction_i…_

2. _Business concept 'Order' is implemented by physical table ORDERS (columns: order_id, OrderID, customer_id, CustomerID, order_date, OrderDate, order_status, orderAmount, total_amount, shippingAmount, t…_

3. _Foreign Keys: - customer_id → CUSTOMERS(customer_id or CustomerID?) - [missing other FK definitions] ========================================== ORDER_ITEMS (or ORDER_DETAILS?) ========================…_

---

### ✅ ec_019 — What's the difference between Shipment, Delivery, and Fulfillment?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0050 | **Gate:** `proceed_with_warning`

**Expected answer:**
> The glossary provides definitions but unclear boundaries: Shipment is 'The process of delivering goods to a customer'; Delivery is 'The completion of a Shipment when goods reach the customer'; Fulfillment is 'The process of preparing and delivering orders. Encompasses Shipment and Delivery.' The exa…

**System answer:**
> The retrieved context does not define the business concepts Shipment, Delivery, or Fulfillment, so I cannot state the difference between them from the knowledge graph.

What the context does include is glossary/schema information for Customer, Client, Account Holder, End User, Order, Transaction, Payment, Inventory Item, and the related physical tables ORDERS, ORDER_ITEMS, PAYMENTS, PRODUCTS, and …

**Sources retrieved (9):** `parent_chunk_data_dictionary.txt_2`, `parent_chunk_data_dictionary.txt_3`, `parent_chunk_business_glossary.txt_0`, `Order→ORDERS`, `parent_chunk_data_dictionary.txt_1`, `Payment→PAYMENTS`, `Order→ORDER_ITEMS`, `Inventory Item→PRODUCTS`

**Context previews (first 3):**

1. _Foreign Keys: - customer_id → CUSTOMERS(customer_id or CustomerID?) - [missing other FK definitions] ========================================== ORDER_ITEMS (or ORDER_DETAILS?) ========================…_

2. _========================================== PAYMENTS ==========================================  Primary Key: payment_id (unverified) | Column Name | Data Type | Constraints | Description | |----------…_

3. _BUSINESS GLOSSARY - Enterprise System Last Updated: 2024-03-15 Status: Partial (pending review) ========================================== CUSTOMER MANAGEMENT =========================================…_

---

### ✅ ec_020 — Are foreign key constraints enforced in the schema?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.1603 | **Gate:** `proceed_with_warning`

**Expected answer:**
> No foreign key constraints are enforced in the DDL. While the data dictionary documents FK relationships (e.g., customer_id → CUSTOMERS, order_id → ORDERS), the actual CREATE TABLE statements omit the REFERENCES clauses. The schema explicitly notes 'FK constraints defined in data dictionary but not …

**System answer:**
> The retrieved context shows intended foreign key relationships, but it does not confirm that foreign key constraints are actually enforced at the database level.

Specifically, the schema metadata labels these columns as FK/reference fields:
In ORDER_ITEMS, order_id references ORDERS and product_id references PRODUCTS (with a duplicate/inconsistent ProductID also shown as FK).
In PAYMENTS, order_i…

**Sources retrieved (9):** `parent_chunk_data_dictionary.txt_2`, `parent_chunk_data_dictionary.txt_3`, `parent_chunk_data_dictionary.txt_1`, `parent_chunk_business_glossary.txt_0`, `Order→ORDERS`, `Customer→CUSTOMERS`, `Payment→PAYMENTS`, `Inventory Item→PRODUCTS`

**Context previews (first 3):**

1. _Foreign Keys: - customer_id → CUSTOMERS(customer_id or CustomerID?) - [missing other FK definitions] ========================================== ORDER_ITEMS (or ORDER_DETAILS?) ========================…_

2. _========================================== PAYMENTS ==========================================  Primary Key: payment_id (unverified) | Column Name | Data Type | Constraints | Description | |----------…_

3. _DATA DICTIONARY - Enterprise Database Version: 2.1 (incomplete documentation) Last Updated: 2024-02-28 ========================================== CUSTOMERS ========================================== P…_

---

## Anomalies & Observations

No anomalies detected. All questions grounded with acceptable RAGAS scores.
