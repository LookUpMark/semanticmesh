# AB-00 — 05_edgecases_incomplete — Run Analysis

**Timestamp:** 2026-03-30 19:24:26  
**Run tag:** `post-fix-v5`

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
| Triplets extracted | 210 |
| Entities resolved | 93 |
| Tables parsed | 5 |
| Tables completed | 5 |

## Query Evaluation Summary

| Metric | Value |
|--------|-------|
| Questions | 20 |
| Grounded | **20/20 (100%)** |
| Avg GT Coverage | 100% |
| Avg Top Score | 0.4747 |
| Avg Chunk Count | 11.0 |
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
> From the retrieved context, a Customer is a business concept in the “CUSTOMER MANAGEMENT” glossary, but its formal definition is incomplete: “An individual or organization that...” The context also says “Client” may be used interchangeably with Customer in some contexts and defines Client as “a person or company that purchases goods or services.”

At the schema level, the business concept CUSTOMER…

**Sources retrieved (11):** `CUSTOMERS→CUSTOMERS`, `parent_chunk_data_dictionary.txt_1`, `parent_chunk_data_dictionary.txt_2`, `parent_chunk_data_dictionary.txt_3`, `ORDER_ITEMS vs ORDER_PRODUCTS vs ORDER_DETAILS→ORDERS`, `payment_method→PAYMENTS`, `parent_chunk_business_glossary.txt_0`, `Order Item→ORDER_ITEMS`

**Context previews (first 3):**

1. _Business concept 'CUSTOMERS' is implemented by physical table CUSTOMERS (columns: customer_id, CustomerID, firstName, first_name, lastName, last_name, email, emailAddress, phone, phoneNumber, created_…_

2. _DATA DICTIONARY - Enterprise Database Version: 2.1 (incomplete documentation) Last Updated: 2024-02-28 ========================================== CUSTOMERS ========================================== P…_

3. _Foreign Keys: - customer_id → CUSTOMERS(customer_id or CustomerID?) - [missing other FK definitions] ========================================== ORDER_ITEMS (or ORDER_DETAILS?) ========================…_

---

### ✅ ec_002 — What's the difference between firstName and first_name in the CUSTOMERS table?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.5988 | **Gate:** `proceed`

**Expected answer:**
> Both columns exist in the CUSTOMERS table with identical VARCHAR(50) data types. The data dictionary notes they appear to be duplicates resulting from inconsistent naming conventions (snake_case vs camelCase), but the actual usage by the application is not documented.

**System answer:**
> From the retrieved context, there is no documented business difference between `firstName` and `first_name` in `CUSTOMERS`.

The data dictionary shows both columns as `VARCHAR(50)`. `firstName` is described as “Customer's first name,” while `first_name` is explicitly marked as “[appears to be duplicate].” The constraints for both are undocumented (`?`), and the overall `CUSTOMERS` documentation is…

**Sources retrieved (11):** `CUSTOMERS→CUSTOMERS`, `parent_chunk_data_dictionary.txt_1`, `parent_chunk_data_dictionary.txt_2`, `parent_chunk_data_dictionary.txt_3`, `Order Item→ORDER_ITEMS`, `parent_chunk_business_glossary.txt_0`, `Order Item`, `ORDER_ITEMS vs ORDER_PRODUCTS vs ORDER_DETAILS→ORDERS`

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
> The retrieved context does not definitively resolve this. It shows that the CUSTOMERS table’s primary key is documented as “customer_id (or is it CustomerID? check with DBA),” and it also lists CustomerID as a possible duplicate of customer_id. The foreign key note likewise says “customer_id → CUSTOMERS(customer_id or CustomerID?).”

So, based strictly on the context, customer_id is the more expli…

**Sources retrieved (11):** `parent_chunk_data_dictionary.txt_2`, `parent_chunk_data_dictionary.txt_1`, `CUSTOMERS→CUSTOMERS`, `parent_chunk_data_dictionary.txt_3`, `ORDER_ITEMS vs ORDER_PRODUCTS vs ORDER_DETAILS→ORDERS`, `payment_method→PAYMENTS`, `Order Item→ORDER_ITEMS`, `Inventory Item→PRODUCTS`

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
> The retrieved context shows that `order_status` is a column in `ORDERS`, but it does not provide any valid values for that field.

From the context, `ORDERS` includes `order_status`, and the glossary says an Order “can be in various states,” but those states are not enumerated anywhere in the retrieved context.

**Sources retrieved (11):** `parent_chunk_data_dictionary.txt_3`, `ORDER_ITEMS vs ORDER_PRODUCTS vs ORDER_DETAILS→ORDERS`, `parent_chunk_data_dictionary.txt_1`, `parent_chunk_data_dictionary.txt_2`, `Order Item→ORDER_ITEMS`, `parent_chunk_business_glossary.txt_0`, `Order Item`, `payment_method→PAYMENTS`

**Context previews (first 3):**

1. _========================================== PAYMENTS ==========================================  Primary Key: payment_id (unverified) | Column Name | Data Type | Constraints | Description | |----------…_

2. _Business concept 'ORDER_ITEMS vs ORDER_PRODUCTS vs ORDER_DETAILS' is implemented by physical table ORDERS (columns: order_id, OrderID, customer_id, CustomerID, order_date, OrderDate, order_status, ord…_

3. _DATA DICTIONARY - Enterprise Database Version: 2.1 (incomplete documentation) Last Updated: 2024-02-28 ========================================== CUSTOMERS ========================================== P…_

---

### ✅ ec_005 — Is there a difference between Product, Item, and SKU?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.5696 | **Gate:** `proceed`

**Expected answer:**
> The glossary indicates these terms are related but distinct: Product is defined as "A thing that is... [definition needs clarification]"; Item is a synonym for Product used in inventory context; SKU (Stock Keeping Unit) is a unique identifier for a product variant; Inventory Item refers to physical …

**System answer:**
> The retrieved context does not provide explicit glossary definitions that distinguish “Product,” “Item,” and “SKU” as separate business terms, so a definitive business-meaning difference is not available.

What the context does show is this:

“Inventory Item” is implemented by the physical table PRODUCTS. That table includes product identity and descriptive fields such as product_id/ProductID, pro…

**Sources retrieved (11):** `Inventory Item→PRODUCTS`, `parent_chunk_data_dictionary.txt_2`, `Order Item→ORDER_ITEMS`, `ORDER_ITEMS vs ORDER_PRODUCTS vs ORDER_DETAILS→ORDERS`, `parent_chunk_data_dictionary.txt_1`, `parent_chunk_data_dictionary.txt_3`, `parent_chunk_business_glossary.txt_0`, `Order Item`

**Context previews (first 3):**

1. _Business concept 'Inventory Item' is implemented by physical table PRODUCTS (columns: product_id, ProductID, product_name, ProductName, product_sku, sku, product_category, category, unit_price, curren…_

2. _Foreign Keys: - customer_id → CUSTOMERS(customer_id or CustomerID?) - [missing other FK definitions] ========================================== ORDER_ITEMS (or ORDER_DETAILS?) ========================…_

3. _Business concept 'Order Item' — The table is clearly line-level, with order_item_id, order_id, product_id, quantity, unit_price, discount fields, and line_total indicating individual order items rathe…_

---

### ✅ ec_006 — Which table should ORDER_ITEMS.product_id reference: PRODUCTS or INVENTORY?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.9608 | **Gate:** `proceed`

**Expected answer:**
> The data dictionary states the FK reference is to 'PRODUCTS (or INVENTORY?)' and notes it is 'not verified'. The schema provides two potential targets: PRODUCTS table (which has product_id) and an INVENTORY table that is referenced in documentation but not defined in the DDL. The actual relationship…

**System answer:**
> Based on the retrieved context, ORDER_ITEMS.product_id should reference PRODUCTS.

The strongest support is that the business concept “Inventory Item” is implemented by the physical table PRODUCTS, and PRODUCTS contains the product identifier columns product_id and ProductID. The ORDER_ITEMS table is described as the line-level “Order Item” table with product_id/ProductID representing the item bei…

**Sources retrieved (11):** `parent_chunk_data_dictionary.txt_2`, `Inventory Item→PRODUCTS`, `ORDER_ITEMS vs ORDER_PRODUCTS vs ORDER_DETAILS→ORDERS`, `Order Item→ORDER_ITEMS`, `parent_chunk_data_dictionary.txt_3`, `parent_chunk_data_dictionary.txt_1`, `Order Item`, `parent_chunk_business_glossary.txt_0`

**Context previews (first 3):**

1. _Foreign Keys: - customer_id → CUSTOMERS(customer_id or CustomerID?) - [missing other FK definitions] ========================================== ORDER_ITEMS (or ORDER_DETAILS?) ========================…_

2. _Business concept 'Inventory Item' is implemented by physical table PRODUCTS (columns: product_id, ProductID, product_name, ProductName, product_sku, sku, product_category, category, unit_price, curren…_

3. _Business concept 'ORDER_ITEMS vs ORDER_PRODUCTS vs ORDER_DETAILS' is implemented by physical table ORDERS (columns: order_id, OrderID, customer_id, CustomerID, order_date, OrderDate, order_status, ord…_

---

### ✅ ec_007 — What's the difference between Revenue and Sales?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.4224 | **Gate:** `proceed`

**Expected answer:**
> Both terms show circular definitions: Revenue is defined as 'Income from sales. The same as... [definition circular, see Sales]', while Sales is defined as 'Revenue from selling products. See Revenue.' The glossary provides no clear distinction between these concepts.

**System answer:**
> The retrieved context does not define either Revenue or Sales, so I cannot state their difference from the knowledge graph.

What the context does provide is only related order and payment metadata. In the business glossary, Order is defined as “A request to purchase products or services. Can be in various states,” and Transaction is described as similar to Order but more general. In the schema, m…

**Sources retrieved (11):** `parent_chunk_data_dictionary.txt_2`, `Order Item→ORDER_ITEMS`, `parent_chunk_data_dictionary.txt_3`, `parent_chunk_business_glossary.txt_0`, `Order Item`, `parent_chunk_data_dictionary.txt_1`, `ORDER_ITEMS vs ORDER_PRODUCTS vs ORDER_DETAILS→ORDERS`, `payment_method→PAYMENTS`

**Context previews (first 3):**

1. _Foreign Keys: - customer_id → CUSTOMERS(customer_id or CustomerID?) - [missing other FK definitions] ========================================== ORDER_ITEMS (or ORDER_DETAILS?) ========================…_

2. _Business concept 'Order Item' — The table is clearly line-level, with order_item_id, order_id, product_id, quantity, unit_price, discount fields, and line_total indicating individual order items rathe…_

3. _========================================== PAYMENTS ==========================================  Primary Key: payment_id (unverified) | Column Name | Data Type | Constraints | Description | |----------…_

---

### ✅ ec_008 — Can one order have multiple payments?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0981 | **Gate:** `proceed_with_warning`

**Expected answer:**
> The PAYMENTS table has an order_id column, suggesting a many-to-one relationship (multiple payments can reference a single order). However, the relationship section in the glossary asks 'Or is it one-to-one?' indicating uncertainty. The ORDERS table has both payment_status and payment_method columns…

**System answer:**
> Yes, based on the schema, one order can have multiple payments.

The retrieved context shows that PAYMENTS has payment_id as its primary key and order_id as a foreign key referencing ORDERS. Because payment_id is the unique row identifier, and there is no stated unique constraint on order_id in PAYMENTS, the table structure allows multiple PAYMENTS rows to reference the same ORDERS row.

This mean…

**Sources retrieved (11):** `parent_chunk_data_dictionary.txt_3`, `payment_method→PAYMENTS`, `ORDER_ITEMS vs ORDER_PRODUCTS vs ORDER_DETAILS→ORDERS`, `parent_chunk_data_dictionary.txt_2`, `Order Item→ORDER_ITEMS`, `parent_chunk_data_dictionary.txt_1`, `Inventory Item→PRODUCTS`, `CUSTOMERS→CUSTOMERS`

**Context previews (first 3):**

1. _========================================== PAYMENTS ==========================================  Primary Key: payment_id (unverified) | Column Name | Data Type | Constraints | Description | |----------…_

2. _Business concept 'payment_method' is implemented by physical table PAYMENTS (columns: payment_id, PaymentID, order_id, customer_id, payment_date, payment_amount, payment_method, payment_status, transa…_

3. _Business concept 'ORDER_ITEMS vs ORDER_PRODUCTS vs ORDER_DETAILS' is implemented by physical table ORDERS (columns: order_id, OrderID, customer_id, CustomerID, order_date, OrderDate, order_status, ord…_

---

### ✅ ec_009 — What payment methods are accepted?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.1791 | **Gate:** `proceed_with_warning`

**Expected answer:**
> The PAYMENTS table has a payment_method column (VARCHAR(30)), but the data dictionary notes '[missing valid values]' and no CHECK constraint exists to enumerate acceptable methods. The schema does not document what values are valid (e.g., credit_card, debit, paypal, etc.).

**System answer:**
> The retrieved context does not list the accepted payment methods. It only shows that payment method is captured in the PAYMENTS table as PAYMENTS.payment_method (VARCHAR(30)), and there is also a payment_method column on ORDERS, but both are documented with “[missing valid values]” or without enumerated allowed values. So the schema indicates where payment method is stored, but not which methods a…

**Sources retrieved (11):** `parent_chunk_data_dictionary.txt_3`, `payment_method→PAYMENTS`, `ORDER_ITEMS vs ORDER_PRODUCTS vs ORDER_DETAILS→ORDERS`, `parent_chunk_data_dictionary.txt_1`, `parent_chunk_data_dictionary.txt_2`, `parent_chunk_business_glossary.txt_0`, `Order Item→ORDER_ITEMS`, `CUSTOMERS→CUSTOMERS`

**Context previews (first 3):**

1. _========================================== PAYMENTS ==========================================  Primary Key: payment_id (unverified) | Column Name | Data Type | Constraints | Description | |----------…_

2. _Business concept 'payment_method' is implemented by physical table PAYMENTS (columns: payment_id, PaymentID, order_id, customer_id, payment_date, payment_amount, payment_method, payment_status, transa…_

3. _Business concept 'ORDER_ITEMS vs ORDER_PRODUCTS vs ORDER_DETAILS' is implemented by physical table ORDERS (columns: order_id, OrderID, customer_id, CustomerID, order_date, OrderDate, order_status, ord…_

---

### ✅ ec_010 — What's the correct table name: ORDER_ITEMS or ORDER_DETAILS?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.9778 | **Gate:** `proceed`

**Expected answer:**
> The DDL creates a table named ORDER_ITEMS, but the data dictionary header shows 'ORDER_ITEMS (or ORDER_DETAILS?)' and notes 'Table name ambiguity: ORDER_ITEMS vs ORDER_DETAILS'. The actual table name in the schema is ORDER_ITEMS, but documentation suggests the application may reference it differentl…

**System answer:**
> Based on the retrieved context, the physical table name is ORDER_ITEMS.

The context explicitly says the business concept “Order Item” is implemented by physical table ORDER_ITEMS, and also notes that ORDER_DETAILS is a documented alias for the same line-level table. So ORDER_DETAILS appears to be an alternate or legacy name, not the primary physical table name in the metadata provided.

There is …

**Sources retrieved (11):** `parent_chunk_data_dictionary.txt_2`, `Order Item→ORDER_ITEMS`, `ORDER_ITEMS vs ORDER_PRODUCTS vs ORDER_DETAILS→ORDERS`, `Inventory Item→PRODUCTS`, `parent_chunk_data_dictionary.txt_3`, `parent_chunk_data_dictionary.txt_1`, `CUSTOMERS→CUSTOMERS`, `Order Item`

**Context previews (first 3):**

1. _Foreign Keys: - customer_id → CUSTOMERS(customer_id or CustomerID?) - [missing other FK definitions] ========================================== ORDER_ITEMS (or ORDER_DETAILS?) ========================…_

2. _Business concept 'Order Item' — The table is clearly line-level, with order_item_id, order_id, product_id, quantity, unit_price, discount fields, and line_total indicating individual order items rathe…_

3. _Business concept 'ORDER_ITEMS vs ORDER_PRODUCTS vs ORDER_DETAILS' is implemented by physical table ORDERS (columns: order_id, OrderID, customer_id, CustomerID, order_date, OrderDate, order_status, ord…_

---

### ✅ ec_011 — Which date column should be used to track when an order was created: order_date, OrderDate, or created_at?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.8920 | **Gate:** `proceed`

**Expected answer:**
> The ORDERS table has three date-related columns: order_date (DATE type), OrderDate (DATETIME type with different precision), and created_at (TIMESTAMP type). The data dictionary provides no guidance on which is actually used by the application or why three columns exist for potentially the same purp…

**System answer:**
> From the retrieved context, this cannot be determined definitively.

The only information provided for `ORDERS` is that it contains `order_date`, `OrderDate`, and `created_at` (along with other columns). There is no column-level description in the retrieved context explaining which one is the authoritative “order created” timestamp.

Given the broader schema pattern shown elsewhere, fields like `o…

**Sources retrieved (11):** `ORDER_ITEMS vs ORDER_PRODUCTS vs ORDER_DETAILS→ORDERS`, `payment_method→PAYMENTS`, `parent_chunk_data_dictionary.txt_1`, `parent_chunk_data_dictionary.txt_3`, `CUSTOMERS→CUSTOMERS`, `Inventory Item→PRODUCTS`, `parent_chunk_data_dictionary.txt_2`, `Order Item→ORDER_ITEMS`

**Context previews (first 3):**

1. _Business concept 'ORDER_ITEMS vs ORDER_PRODUCTS vs ORDER_DETAILS' is implemented by physical table ORDERS (columns: order_id, OrderID, customer_id, CustomerID, order_date, OrderDate, order_status, ord…_

2. _Business concept 'payment_method' is implemented by physical table PAYMENTS (columns: payment_id, PaymentID, order_id, customer_id, payment_date, payment_amount, payment_method, payment_status, transa…_

3. _DATA DICTIONARY - Enterprise Database Version: 2.1 (incomplete documentation) Last Updated: 2024-02-28 ========================================== CUSTOMERS ========================================== P…_

---

### ✅ ec_012 — What does the Failed order status mean?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0031 | **Gate:** `proceed_with_warning`

**Expected answer:**
> The business glossary lists Failed as an order status but marks it as '[definition missing]'. Other statuses have definitions (Pending, Processing, Completed, Cancelled, On Hold), but Failed is undefined despite being a valid status value.

**System answer:**
> The retrieved context does not define a meaning for a “Failed” order status.

What the context does show is that the ORDERS table includes an order_status column, and both ORDERS and PAYMENTS include payment_status-related fields. However, the documentation explicitly says valid values are missing for PAYMENTS.payment_status, and it provides no documented value list or business definition for ORDE…

**Sources retrieved (11):** `parent_chunk_data_dictionary.txt_3`, `parent_chunk_data_dictionary.txt_1`, `ORDER_ITEMS vs ORDER_PRODUCTS vs ORDER_DETAILS→ORDERS`, `parent_chunk_data_dictionary.txt_2`, `Order Item→ORDER_ITEMS`, `payment_method→PAYMENTS`, `Inventory Item→PRODUCTS`, `CUSTOMERS→CUSTOMERS`

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
> No explicit NOT NULL constraints are documented in the retrieved context.

The schema excerpts shown for PAYMENTS, CUSTOMERS, and ORDER_ITEMS list constraints like PK, FK, and UNIQUE?, but none of the columns are explicitly marked NOT NULL. The documentation is also labeled incomplete, so the context does not confirm whether NOT NULL exists elsewhere; it only shows that no NOT NULL constraints are…

**Sources retrieved (11):** `parent_chunk_data_dictionary.txt_3`, `parent_chunk_data_dictionary.txt_2`, `Order Item→ORDER_ITEMS`, `parent_chunk_data_dictionary.txt_1`, `ORDER_ITEMS vs ORDER_PRODUCTS vs ORDER_DETAILS→ORDERS`, `Order Item`, `parent_chunk_business_glossary.txt_0`, `Inventory Item→PRODUCTS`

**Context previews (first 3):**

1. _========================================== PAYMENTS ==========================================  Primary Key: payment_id (unverified) | Column Name | Data Type | Constraints | Description | |----------…_

2. _Foreign Keys: - customer_id → CUSTOMERS(customer_id or CustomerID?) - [missing other FK definitions] ========================================== ORDER_ITEMS (or ORDER_DETAILS?) ========================…_

3. _Business concept 'Order Item' — The table is clearly line-level, with order_item_id, order_id, product_id, quantity, unit_price, discount fields, and line_total indicating individual order items rathe…_

---

### ✅ ec_014 — What's the difference between unit_price and current_price in PRODUCTS?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.4761 | **Gate:** `proceed`

**Expected answer:**
> The PRODUCTS table has both unit_price and current_price columns (both DECIMAL(10,2)). The data dictionary asks 'Different from unit_price?' but provides no explanation of the distinction or when each would be used.

**System answer:**
> The retrieved context shows that PRODUCTS, which implements the business concept Inventory Item, contains both unit_price and current_price. However, it does not provide column definitions or descriptions for those two PRODUCTS columns, so the difference between them is not documented in the available context.

The only related pricing description in the context is for ORDER_ITEMS.unit_price, whic…

**Sources retrieved (11):** `Inventory Item→PRODUCTS`, `parent_chunk_data_dictionary.txt_2`, `Order Item→ORDER_ITEMS`, `ORDER_ITEMS vs ORDER_PRODUCTS vs ORDER_DETAILS→ORDERS`, `parent_chunk_data_dictionary.txt_3`, `Order Item`, `parent_chunk_business_glossary.txt_0`, `ORDER_ITEMS vs ORDER_PRODUCTS vs ORDER_DETAILS`

**Context previews (first 3):**

1. _Business concept 'Inventory Item' is implemented by physical table PRODUCTS (columns: product_id, ProductID, product_name, ProductName, product_sku, sku, product_category, category, unit_price, curren…_

2. _Foreign Keys: - customer_id → CUSTOMERS(customer_id or CustomerID?) - [missing other FK definitions] ========================================== ORDER_ITEMS (or ORDER_DETAILS?) ========================…_

3. _Business concept 'Order Item' — The table is clearly line-level, with order_item_id, order_id, product_id, quantity, unit_price, discount fields, and line_total indicating individual order items rathe…_

---

### ✅ ec_015 — When is an invoice generated vs payment processed?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.6598 | **Gate:** `proceed`

**Expected answer:**
> The relationship section in the glossary asks 'An invoice is generated for an order. But when? And can one order have multiple invoices?' indicating the timing and cardinality are not defined. The glossary defines Invoice as 'A document requesting payment. Related to Bill' and Payment as 'The transf…

**System answer:**
> The retrieved context does not document any invoice entity, invoice table, invoice column, or business rule for invoice generation, so I cannot determine when an invoice is generated.

The payment side is partially documented. Payment processing is represented by the PAYMENTS table, which includes payment_date as a DATETIME field, so the context supports that the time a payment is processed is cap…

**Sources retrieved (11):** `parent_chunk_data_dictionary.txt_3`, `ORDER_ITEMS vs ORDER_PRODUCTS vs ORDER_DETAILS→ORDERS`, `parent_chunk_data_dictionary.txt_1`, `parent_chunk_data_dictionary.txt_2`, `payment_method→PAYMENTS`, `parent_chunk_business_glossary.txt_0`, `Order Item→ORDER_ITEMS`, `Inventory Item→PRODUCTS`

**Context previews (first 3):**

1. _========================================== PAYMENTS ==========================================  Primary Key: payment_id (unverified) | Column Name | Data Type | Constraints | Description | |----------…_

2. _Business concept 'ORDER_ITEMS vs ORDER_PRODUCTS vs ORDER_DETAILS' is implemented by physical table ORDERS (columns: order_id, OrderID, customer_id, CustomerID, order_date, OrderDate, order_status, ord…_

3. _DATA DICTIONARY - Enterprise Database Version: 2.1 (incomplete documentation) Last Updated: 2024-02-28 ========================================== CUSTOMERS ========================================== P…_

---

### ✅ ec_016 — Is the sku column in PRODUCTS unique?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.3824 | **Gate:** `proceed`

**Expected answer:**
> The PRODUCTS table has both product_sku and sku columns. The data dictionary notes sku 'should be UNIQUE?' but the DDL does not define a UNIQUE constraint on either column. No index is documented for these columns.

**System answer:**
> The retrieved context does not state that `sku` in `PRODUCTS` is unique. It only shows that `PRODUCTS` includes `product_sku` and `sku` as columns in the business concept "Inventory Item," but no uniqueness constraint is documented for either column.

**Sources retrieved (11):** `Inventory Item→PRODUCTS`, `parent_chunk_data_dictionary.txt_2`, `parent_chunk_data_dictionary.txt_3`, `Order Item→ORDER_ITEMS`, `ORDER_ITEMS vs ORDER_PRODUCTS vs ORDER_DETAILS→ORDERS`, `parent_chunk_data_dictionary.txt_1`, `CUSTOMERS→CUSTOMERS`, `payment_method→PAYMENTS`

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
> The retrieved context indicates that customers and orders are related through the ORDERS table. The physical table implementing the order concept is ORDERS, and it includes customer_id and CustomerID columns ([3]). The customer concept is implemented by the CUSTOMERS table, whose key is documented inconsistently as customer_id or CustomerID ([4], [6]).

So at the schema level, the relationship is …

**Sources retrieved (11):** `parent_chunk_data_dictionary.txt_3`, `parent_chunk_data_dictionary.txt_2`, `ORDER_ITEMS vs ORDER_PRODUCTS vs ORDER_DETAILS→ORDERS`, `parent_chunk_data_dictionary.txt_1`, `Order Item→ORDER_ITEMS`, `CUSTOMERS→CUSTOMERS`, `parent_chunk_business_glossary.txt_0`, `Order Item`

**Context previews (first 3):**

1. _========================================== PAYMENTS ==========================================  Primary Key: payment_id (unverified) | Column Name | Data Type | Constraints | Description | |----------…_

2. _Foreign Keys: - customer_id → CUSTOMERS(customer_id or CustomerID?) - [missing other FK definitions] ========================================== ORDER_ITEMS (or ORDER_DETAILS?) ========================…_

3. _Business concept 'ORDER_ITEMS vs ORDER_PRODUCTS vs ORDER_DETAILS' is implemented by physical table ORDERS (columns: order_id, OrderID, customer_id, CustomerID, order_date, OrderDate, order_status, ord…_

---

### ✅ ec_018 — Which price column represents what the customer actually pays?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0682 | **Gate:** `proceed_with_warning`

**Expected answer:**
> Multiple price columns exist across tables: ORDERS has orderAmount and total_amount; ORDER_ITEMS has unit_price and UnitPrice; PRODUCTS has unit_price, current_price, and cost_price. The data dictionary does not explain which represents the final customer price, whether discounts are applied, or how…

**System answer:**
> From the retrieved context, the column that most directly represents what the customer actually pays is ORDER_ITEMS.line_total for each order line, because the same table also contains quantity, unit_price, discount_percent, and discount_amount, which implies line_total is the final line-level amount after pricing and discounts.

Related price columns in the context mean different things:
ORDER_IT…

**Sources retrieved (11):** `payment_method→PAYMENTS`, `ORDER_ITEMS vs ORDER_PRODUCTS vs ORDER_DETAILS→ORDERS`, `parent_chunk_data_dictionary.txt_2`, `parent_chunk_data_dictionary.txt_3`, `Order Item→ORDER_ITEMS`, `CUSTOMERS→CUSTOMERS`, `parent_chunk_data_dictionary.txt_1`, `Inventory Item→PRODUCTS`

**Context previews (first 3):**

1. _Business concept 'payment_method' is implemented by physical table PAYMENTS (columns: payment_id, PaymentID, order_id, customer_id, payment_date, payment_amount, payment_method, payment_status, transa…_

2. _Business concept 'ORDER_ITEMS vs ORDER_PRODUCTS vs ORDER_DETAILS' is implemented by physical table ORDERS (columns: order_id, OrderID, customer_id, CustomerID, order_date, OrderDate, order_status, ord…_

3. _Foreign Keys: - customer_id → CUSTOMERS(customer_id or CustomerID?) - [missing other FK definitions] ========================================== ORDER_ITEMS (or ORDER_DETAILS?) ========================…_

---

### ✅ ec_019 — What's the difference between Shipment, Delivery, and Fulfillment?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0050 | **Gate:** `proceed_with_warning`

**Expected answer:**
> The glossary provides definitions but unclear boundaries: Shipment is 'The process of delivering goods to a customer'; Delivery is 'The completion of a Shipment when goods reach the customer'; Fulfillment is 'The process of preparing and delivering orders. Encompasses Shipment and Delivery.' The exa…

**System answer:**
> The retrieved context does not define or distinguish “Shipment,” “Delivery,” or “Fulfillment,” so their differences cannot be determined from the knowledge graph.

What is known from the context is that the business glossary is marked “Partial (pending review)” and includes some order-related terms such as “Order” (“A request to purchase products or services. Can be in various states.”) and “Trans…

**Sources retrieved (11):** `parent_chunk_data_dictionary.txt_2`, `parent_chunk_data_dictionary.txt_3`, `Order Item→ORDER_ITEMS`, `parent_chunk_business_glossary.txt_0`, `Order Item`, `ORDER_ITEMS vs ORDER_PRODUCTS vs ORDER_DETAILS→ORDERS`, `parent_chunk_data_dictionary.txt_1`, `payment_method→PAYMENTS`

**Context previews (first 3):**

1. _Foreign Keys: - customer_id → CUSTOMERS(customer_id or CustomerID?) - [missing other FK definitions] ========================================== ORDER_ITEMS (or ORDER_DETAILS?) ========================…_

2. _========================================== PAYMENTS ==========================================  Primary Key: payment_id (unverified) | Column Name | Data Type | Constraints | Description | |----------…_

3. _Business concept 'Order Item' — The table is clearly line-level, with order_item_id, order_id, product_id, quantity, unit_price, discount fields, and line_total indicating individual order items rathe…_

---

### ✅ ec_020 — Are foreign key constraints enforced in the schema?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.1603 | **Gate:** `proceed_with_warning`

**Expected answer:**
> No foreign key constraints are enforced in the DDL. While the data dictionary documents FK relationships (e.g., customer_id → CUSTOMERS, order_id → ORDERS), the actual CREATE TABLE statements omit the REFERENCES clauses. The schema explicitly notes 'FK constraints defined in data dictionary but not …

**System answer:**
> The retrieved context does not confirm that foreign key constraints are consistently enforced in the schema.

What it does show is that several columns are documented as foreign keys at the metadata level: ORDER_ITEMS.order_id references ORDERS, ORDER_ITEMS.product_id references PRODUCTS, PAYMENTS.order_id references ORDERS, PAYMENTS.customer_id references CUSTOMERS, and there is also a separate n…

**Sources retrieved (11):** `parent_chunk_data_dictionary.txt_2`, `parent_chunk_data_dictionary.txt_3`, `Order Item→ORDER_ITEMS`, `parent_chunk_data_dictionary.txt_1`, `Order Item`, `parent_chunk_business_glossary.txt_0`, `ORDER_ITEMS vs ORDER_PRODUCTS vs ORDER_DETAILS→ORDERS`, `Inventory Item→PRODUCTS`

**Context previews (first 3):**

1. _Foreign Keys: - customer_id → CUSTOMERS(customer_id or CustomerID?) - [missing other FK definitions] ========================================== ORDER_ITEMS (or ORDER_DETAILS?) ========================…_

2. _========================================== PAYMENTS ==========================================  Primary Key: payment_id (unverified) | Column Name | Data Type | Constraints | Description | |----------…_

3. _Business concept 'Order Item' — The table is clearly line-level, with order_item_id, order_id, product_id, quantity, unit_price, discount fields, and line_total indicating individual order items rathe…_

---

## Anomalies & Observations

No anomalies detected. All questions grounded with acceptable RAGAS scores.
