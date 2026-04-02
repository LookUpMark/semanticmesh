# AB-14 — 05_edgecases_incomplete — Run Analysis

**Timestamp:** 2026-04-01 05:56:46  
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
| Triplets extracted | 157 |
| Entities resolved | 80 |
| Tables parsed | 5 |
| Tables completed | 5 |

## Query Evaluation Summary

| Metric | Value |
|--------|-------|
| Questions | 20 |
| Grounded | **20/20 (100%)** |
| Avg GT Coverage | 100% |
| Avg Top Score | 0.4793 |
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
> In the business glossary, a Customer is defined only partially as “An individual or organization that...” because the definition is incomplete in the retrieved context. The glossary also notes that Client is “a person or company that purchases goods or services” and may be used interchangeably with Customer in some contexts, while Account Holder is similar to Customer but with an account-specific …

**Sources retrieved (11):** `CUSTOMERS→CUSTOMERS`, `parent_chunk_data_dictionary.txt_1`, `parent_chunk_data_dictionary.txt_2`, `Sales→ORDERS`, `parent_chunk_data_dictionary.txt_3`, `payment_method→PAYMENTS`, `parent_chunk_business_glossary.txt_0`, `Order Items→ORDER_ITEMS`

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
> In the CUSTOMERS table, the retrieved context does not document a business difference between firstName and first_name. Both are listed as VARCHAR(50) columns. The data dictionary describes firstName as “Customer’s first name,” while first_name is marked as “[appears to be duplicate].” Combined with the concept-to-table mapping, this suggests they are likely duplicate or inconsistently named versi…

**Sources retrieved (11):** `CUSTOMERS→CUSTOMERS`, `parent_chunk_data_dictionary.txt_1`, `parent_chunk_data_dictionary.txt_2`, `parent_chunk_data_dictionary.txt_3`, `Order Items`, `Order Items→ORDER_ITEMS`, `parent_chunk_business_glossary.txt_0`, `Sales→ORDERS`

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
> From the retrieved context, the schema does not definitively resolve this. The strongest indication is that `customer_id` should be used: the `CUSTOMERS` table lists `customer_id` as the primary key candidate, and other tables such as `PAYMENTS` define `customer_id` as the foreign key referencing `CUSTOMERS`. The foreign key note also shows `customer_id → CUSTOMERS(customer_id or CustomerID?)`, wh…

**Sources retrieved (11):** `parent_chunk_data_dictionary.txt_2`, `parent_chunk_data_dictionary.txt_1`, `CUSTOMERS→CUSTOMERS`, `parent_chunk_data_dictionary.txt_3`, `Sales→ORDERS`, `payment_method→PAYMENTS`, `Order Items`, `Order Items→ORDER_ITEMS`

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
> The retrieved context does not provide the valid values for ORDERS.order_status.

What the context does confirm is that:
The business concept Sales is implemented by the physical table ORDERS, and ORDERS includes the column order_status.
The business glossary defines Order as “A request to purchase products or services” and says it “can be in various states.”

However, no enumeration, code list, a…

**Sources retrieved (11):** `parent_chunk_data_dictionary.txt_3`, `Sales→ORDERS`, `parent_chunk_data_dictionary.txt_1`, `parent_chunk_data_dictionary.txt_2`, `Order Items`, `Order Items→ORDER_ITEMS`, `parent_chunk_business_glossary.txt_0`, `payment_method→PAYMENTS`

**Context previews (first 3):**

1. _========================================== PAYMENTS ==========================================  Primary Key: payment_id (unverified) | Column Name | Data Type | Constraints | Description | |----------…_

2. _Business concept 'Sales' is implemented by physical table ORDERS (columns: order_id, OrderID, customer_id, CustomerID, order_date, OrderDate, order_status, orderAmount, total_amount, shippingAmount, t…_

3. _DATA DICTIONARY - Enterprise Database Version: 2.1 (incomplete documentation) Last Updated: 2024-02-28 ========================================== CUSTOMERS ========================================== P…_

---

### ✅ ec_005 — Is there a difference between Product, Item, and SKU?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.5696 | **Gate:** `proceed`

**Expected answer:**
> The glossary indicates these terms are related but distinct: Product is defined as "A thing that is... [definition needs clarification]"; Item is a synonym for Product used in inventory context; SKU (Stock Keeping Unit) is a unique identifier for a product variant; Inventory Item refers to physical …

**System answer:**
> The retrieved context does not provide formal glossary definitions for Product, Item, or SKU, so it does not explicitly state the business difference between them. But at the schema level, they are used differently.

A Product is represented by the physical table PRODUCTS. That table holds product master data such as product_id/ProductID, product_name/ProductName, product_sku/sku, product_category…

**Sources retrieved (11):** `Table naming: ORDER_ITEMS vs ORDER_PRODUCTS vs ORDER_DETAILS→PRODUCTS`, `parent_chunk_data_dictionary.txt_2`, `Order Items`, `Order Items→ORDER_ITEMS`, `parent_chunk_data_dictionary.txt_1`, `parent_chunk_data_dictionary.txt_3`, `parent_chunk_business_glossary.txt_0`, `Table naming: ORDER_ITEMS vs ORDER_PRODUCTS vs ORDER_DETAILS`

**Context previews (first 3):**

1. _Business concept 'Table naming: ORDER_ITEMS vs ORDER_PRODUCTS vs ORDER_DETAILS' is implemented by physical table PRODUCTS (columns: product_id, ProductID, product_name, ProductName, product_sku, sku, …_

2. _Foreign Keys: - customer_id → CUSTOMERS(customer_id or CustomerID?) - [missing other FK definitions] ========================================== ORDER_ITEMS (or ORDER_DETAILS?) ========================…_

3. _Order Items: The table is clearly a line-item structure keyed by order_item_id and carrying order_id, product_id, quantity, pricing, discount, and line total fields, which aligns with Order Items rath…_

---

### ✅ ec_006 — Which table should ORDER_ITEMS.product_id reference: PRODUCTS or INVENTORY?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.9608 | **Gate:** `proceed`

**Expected answer:**
> The data dictionary states the FK reference is to 'PRODUCTS (or INVENTORY?)' and notes it is 'not verified'. The schema provides two potential targets: PRODUCTS table (which has product_id) and an INVENTORY table that is referenced in documentation but not defined in the DDL. The actual relationship…

**System answer:**
> The retrieved context does not confirm this definitively. In the `ORDER_ITEMS` definition, `product_id` is described as `FK | References PRODUCTS (or INVENTORY?)`, so the source documentation itself is ambiguous.

From the available context, `PRODUCTS` is the stronger match because:
`ORDER_ITEMS` is described as a line-item table with `product_id`, quantity, price, discount, and line total, and
th…

**Sources retrieved (11):** `parent_chunk_data_dictionary.txt_2`, `Table naming: ORDER_ITEMS vs ORDER_PRODUCTS vs ORDER_DETAILS→PRODUCTS`, `Order Items`, `Order Items→ORDER_ITEMS`, `parent_chunk_data_dictionary.txt_3`, `parent_chunk_data_dictionary.txt_1`, `parent_chunk_business_glossary.txt_0`, `Table naming: ORDER_ITEMS vs ORDER_PRODUCTS vs ORDER_DETAILS`

**Context previews (first 3):**

1. _Foreign Keys: - customer_id → CUSTOMERS(customer_id or CustomerID?) - [missing other FK definitions] ========================================== ORDER_ITEMS (or ORDER_DETAILS?) ========================…_

2. _Business concept 'Table naming: ORDER_ITEMS vs ORDER_PRODUCTS vs ORDER_DETAILS' is implemented by physical table PRODUCTS (columns: product_id, ProductID, product_name, ProductName, product_sku, sku, …_

3. _Order Items: The table is clearly a line-item structure keyed by order_item_id and carrying order_id, product_id, quantity, pricing, discount, and line total fields, which aligns with Order Items rath…_

---

### ✅ ec_007 — What's the difference between Revenue and Sales?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.4224 | **Gate:** `proceed`

**Expected answer:**
> Both terms show circular definitions: Revenue is defined as 'Income from sales. The same as... [definition circular, see Sales]', while Sales is defined as 'Revenue from selling products. See Revenue.' The glossary provides no clear distinction between these concepts.

**System answer:**
> From the retrieved context, only Sales is documented.

Sales is explicitly mapped to the physical table ORDERS. That table contains order-level fields such as order_id / OrderID, customer_id / CustomerID, order_date / OrderDate, order_status, orderAmount, total_amount, shippingAmount, tax_amount / TaxAmount, payment_status, payment_method, created_at, updated_at, notes / Notes. The glossary also d…

**Sources retrieved (11):** `Sales→ORDERS`, `parent_chunk_data_dictionary.txt_2`, `parent_chunk_data_dictionary.txt_3`, `Order Items→ORDER_ITEMS`, `Order Items`, `parent_chunk_business_glossary.txt_0`, `parent_chunk_data_dictionary.txt_1`, `Table naming: ORDER_ITEMS vs ORDER_PRODUCTS vs ORDER_DETAILS→PRODUCTS`

**Context previews (first 3):**

1. _Business concept 'Sales' is implemented by physical table ORDERS (columns: order_id, OrderID, customer_id, CustomerID, order_date, OrderDate, order_status, orderAmount, total_amount, shippingAmount, t…_

2. _Foreign Keys: - customer_id → CUSTOMERS(customer_id or CustomerID?) - [missing other FK definitions] ========================================== ORDER_ITEMS (or ORDER_DETAILS?) ========================…_

3. _========================================== PAYMENTS ==========================================  Primary Key: payment_id (unverified) | Column Name | Data Type | Constraints | Description | |----------…_

---

### ✅ ec_008 — Can one order have multiple payments?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0981 | **Gate:** `proceed_with_warning`

**Expected answer:**
> The PAYMENTS table has an order_id column, suggesting a many-to-one relationship (multiple payments can reference a single order). However, the relationship section in the glossary asks 'Or is it one-to-one?' indicating uncertainty. The ORDERS table has both payment_status and payment_method columns…

**System answer:**
> From the retrieved context, it is known that the PAYMENTS table contains an order_id foreign key that references ORDERS, so payments are linked to orders at the schema level.

However, the context does not state the cardinality between ORDERS and PAYMENTS. There is no documented uniqueness constraint on PAYMENTS.order_id and no explicit business rule saying whether an order can have only one payme…

**Sources retrieved (11):** `parent_chunk_data_dictionary.txt_3`, `payment_method→PAYMENTS`, `Sales→ORDERS`, `parent_chunk_data_dictionary.txt_2`, `parent_chunk_data_dictionary.txt_1`, `Order Items→ORDER_ITEMS`, `Order Items`, `Table naming: ORDER_ITEMS vs ORDER_PRODUCTS vs ORDER_DETAILS→PRODUCTS`

**Context previews (first 3):**

1. _========================================== PAYMENTS ==========================================  Primary Key: payment_id (unverified) | Column Name | Data Type | Constraints | Description | |----------…_

2. _Business concept 'payment_method' is implemented by physical table PAYMENTS (columns: payment_id, PaymentID, order_id, customer_id, payment_date, payment_amount, payment_method, payment_status, transa…_

3. _Business concept 'Sales' is implemented by physical table ORDERS (columns: order_id, OrderID, customer_id, CustomerID, order_date, OrderDate, order_status, orderAmount, total_amount, shippingAmount, t…_

---

### ✅ ec_009 — What payment methods are accepted?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.1791 | **Gate:** `proceed_with_warning`

**Expected answer:**
> The PAYMENTS table has a payment_method column (VARCHAR(30)), but the data dictionary notes '[missing valid values]' and no CHECK constraint exists to enumerate acceptable methods. The schema does not document what values are valid (e.g., credit_card, debit, paypal, etc.).

**System answer:**
> The retrieved context shows that payment methods are tracked, but it does not list the accepted values.

Specifically, the business concept payment_method is implemented in the PAYMENTS table, which includes the column payment_method, and the documentation for that column explicitly says “[missing valid values].” The ORDERS table also includes a payment_method column under the Sales concept, which…

**Sources retrieved (11):** `parent_chunk_data_dictionary.txt_3`, `payment_method→PAYMENTS`, `Sales→ORDERS`, `parent_chunk_data_dictionary.txt_1`, `parent_chunk_data_dictionary.txt_2`, `parent_chunk_business_glossary.txt_0`, `CUSTOMERS→CUSTOMERS`, `Order Items→ORDER_ITEMS`

**Context previews (first 3):**

1. _========================================== PAYMENTS ==========================================  Primary Key: payment_id (unverified) | Column Name | Data Type | Constraints | Description | |----------…_

2. _Business concept 'payment_method' is implemented by physical table PAYMENTS (columns: payment_id, PaymentID, order_id, customer_id, payment_date, payment_amount, payment_method, payment_status, transa…_

3. _Business concept 'Sales' is implemented by physical table ORDERS (columns: order_id, OrderID, customer_id, CustomerID, order_date, OrderDate, order_status, orderAmount, total_amount, shippingAmount, t…_

---

### ✅ ec_010 — What's the correct table name: ORDER_ITEMS or ORDER_DETAILS?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.9980 | **Gate:** `proceed`

**Expected answer:**
> The DDL creates a table named ORDER_ITEMS, but the data dictionary header shows 'ORDER_ITEMS (or ORDER_DETAILS?)' and notes 'Table name ambiguity: ORDER_ITEMS vs ORDER_DETAILS'. The actual table name in the schema is ORDER_ITEMS, but documentation suggests the application may reference it differentl…

**System answer:**
> Based on the retrieved context, ORDER_ITEMS is the better-supported and more correct table name.

The strongest evidence is the concept mapping that says the business concept “Order Items” is implemented by the physical table ORDER_ITEMS, with columns such as order_item_id, order_id, product_id, quantity, unit_price, discount_percent, discount_amount, and line_total. The context also explicitly sa…

**Sources retrieved (11):** `Table naming: ORDER_ITEMS vs ORDER_PRODUCTS vs ORDER_DETAILS→PRODUCTS`, `parent_chunk_data_dictionary.txt_2`, `Order Items→ORDER_ITEMS`, `parent_chunk_data_dictionary.txt_3`, `parent_chunk_data_dictionary.txt_1`, `CUSTOMERS→CUSTOMERS`, `Table naming: ORDER_ITEMS vs ORDER_PRODUCTS vs ORDER_DETAILS`, `Order Items`

**Context previews (first 3):**

1. _Business concept 'Table naming: ORDER_ITEMS vs ORDER_PRODUCTS vs ORDER_DETAILS' is implemented by physical table PRODUCTS (columns: product_id, ProductID, product_name, ProductName, product_sku, sku, …_

2. _Foreign Keys: - customer_id → CUSTOMERS(customer_id or CustomerID?) - [missing other FK definitions] ========================================== ORDER_ITEMS (or ORDER_DETAILS?) ========================…_

3. _Business concept 'Order Items' — The table is clearly a line-item structure keyed by order_item_id and carrying order_id, product_id, quantity, pricing, discount, and line total fields, which aligns w…_

---

### ✅ ec_011 — Which date column should be used to track when an order was created: order_date, OrderDate, or created_at?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.9218 | **Gate:** `proceed`

**Expected answer:**
> The ORDERS table has three date-related columns: order_date (DATE type), OrderDate (DATETIME type with different precision), and created_at (TIMESTAMP type). The data dictionary provides no guidance on which is actually used by the application or why three columns exist for potentially the same purp…

**System answer:**
> The retrieved context shows that the ORDERS table for the business concept Sales contains all three columns: order_date, OrderDate, and created_at. However, it does not define their meanings or indicate which one is the authoritative “order created” timestamp.

So, from the context, it cannot be determined whether order_date, OrderDate, or created_at should be used to track when an order was creat…

**Sources retrieved (11):** `Sales→ORDERS`, `payment_method→PAYMENTS`, `Table naming: ORDER_ITEMS vs ORDER_PRODUCTS vs ORDER_DETAILS→PRODUCTS`, `parent_chunk_data_dictionary.txt_1`, `parent_chunk_data_dictionary.txt_3`, `CUSTOMERS→CUSTOMERS`, `parent_chunk_data_dictionary.txt_2`, `Order Items→ORDER_ITEMS`

**Context previews (first 3):**

1. _Business concept 'Sales' is implemented by physical table ORDERS (columns: order_id, OrderID, customer_id, CustomerID, order_date, OrderDate, order_status, orderAmount, total_amount, shippingAmount, t…_

2. _Business concept 'payment_method' is implemented by physical table PAYMENTS (columns: payment_id, PaymentID, order_id, customer_id, payment_date, payment_amount, payment_method, payment_status, transa…_

3. _Business concept 'Table naming: ORDER_ITEMS vs ORDER_PRODUCTS vs ORDER_DETAILS' is implemented by physical table PRODUCTS (columns: product_id, ProductID, product_name, ProductName, product_sku, sku, …_

---

### ✅ ec_012 — What does the Failed order status mean?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0031 | **Gate:** `proceed_with_warning`

**Expected answer:**
> The business glossary lists Failed as an order status but marks it as '[definition missing]'. Other statuses have definitions (Pending, Processing, Completed, Cancelled, On Hold), but Failed is undefined despite being a valid status value.

**System answer:**
> The retrieved context does not define a Failed order status.

It only confirms that ORDERS includes an order_status column in the mapping for the business concept Sales, and the glossary says an Order “can be in various states.” However, the context does not provide the valid values for ORDERS.order_status or any business meaning for a specific value such as Failed.

So, from the available context…

**Sources retrieved (11):** `parent_chunk_data_dictionary.txt_3`, `parent_chunk_data_dictionary.txt_1`, `Sales→ORDERS`, `parent_chunk_data_dictionary.txt_2`, `Order Items→ORDER_ITEMS`, `Order Items`, `payment_method→PAYMENTS`, `Table naming: ORDER_ITEMS vs ORDER_PRODUCTS vs ORDER_DETAILS→PRODUCTS`

**Context previews (first 3):**

1. _========================================== PAYMENTS ==========================================  Primary Key: payment_id (unverified) | Column Name | Data Type | Constraints | Description | |----------…_

2. _DATA DICTIONARY - Enterprise Database Version: 2.1 (incomplete documentation) Last Updated: 2024-02-28 ========================================== CUSTOMERS ========================================== P…_

3. _Business concept 'Sales' is implemented by physical table ORDERS (columns: order_id, OrderID, customer_id, CustomerID, order_date, OrderDate, order_status, orderAmount, total_amount, shippingAmount, t…_

---

### ✅ ec_013 — Are there any NOT NULL constraints defined in the schema?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.7628 | **Gate:** `proceed`

**Expected answer:**
> No NOT NULL constraints are defined in the DDL. The data dictionary explicitly states 'NOT NULL constraints not defined' under 'Missing Documentation' and notes 'assumed, not verified'. All columns are nullable by default.

**System answer:**
> No explicit NOT NULL constraints are defined in the retrieved schema context.

The context shows constraints such as PK on fields like CUSTOMERS.customer_id, PAYMENTS.payment_id, and ORDER_ITEMS.order_item_id, FK on fields like PAYMENTS.order_id, PAYMENTS.customer_id, and ORDER_ITEMS.order_id/product_id, and a possible UNIQUE on PAYMENTS.transaction_id, but no column is explicitly marked NOT NULL.…

**Sources retrieved (11):** `parent_chunk_data_dictionary.txt_3`, `parent_chunk_data_dictionary.txt_2`, `parent_chunk_data_dictionary.txt_1`, `Sales→ORDERS`, `parent_chunk_business_glossary.txt_0`, `Order Items`, `Order Items→ORDER_ITEMS`, `Table naming: ORDER_ITEMS vs ORDER_PRODUCTS vs ORDER_DETAILS→PRODUCTS`

**Context previews (first 3):**

1. _========================================== PAYMENTS ==========================================  Primary Key: payment_id (unverified) | Column Name | Data Type | Constraints | Description | |----------…_

2. _Foreign Keys: - customer_id → CUSTOMERS(customer_id or CustomerID?) - [missing other FK definitions] ========================================== ORDER_ITEMS (or ORDER_DETAILS?) ========================…_

3. _DATA DICTIONARY - Enterprise Database Version: 2.1 (incomplete documentation) Last Updated: 2024-02-28 ========================================== CUSTOMERS ========================================== P…_

---

### ✅ ec_014 — What's the difference between unit_price and current_price in PRODUCTS?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.5557 | **Gate:** `proceed`

**Expected answer:**
> The PRODUCTS table has both unit_price and current_price columns (both DECIMAL(10,2)). The data dictionary asks 'Different from unit_price?' but provides no explanation of the distinction or when each would be used.

**System answer:**
> The retrieved context shows that PRODUCTS contains both unit_price and current_price, along with cost_price, but it does not define either column or explain how they differ in the PRODUCTS table.

The only explicit meaning available for a similarly named field is ORDER_ITEMS.unit_price, which is described there as “Price per unit.” However, the context does not say whether PRODUCTS.unit_price has …

**Sources retrieved (11):** `Table naming: ORDER_ITEMS vs ORDER_PRODUCTS vs ORDER_DETAILS→PRODUCTS`, `parent_chunk_data_dictionary.txt_2`, `Order Items→ORDER_ITEMS`, `Order Items`, `parent_chunk_data_dictionary.txt_3`, `parent_chunk_business_glossary.txt_0`, `Table naming: ORDER_ITEMS vs ORDER_PRODUCTS vs ORDER_DETAILS`, `parent_chunk_data_dictionary.txt_1`

**Context previews (first 3):**

1. _Business concept 'Table naming: ORDER_ITEMS vs ORDER_PRODUCTS vs ORDER_DETAILS' is implemented by physical table PRODUCTS (columns: product_id, ProductID, product_name, ProductName, product_sku, sku, …_

2. _Foreign Keys: - customer_id → CUSTOMERS(customer_id or CustomerID?) - [missing other FK definitions] ========================================== ORDER_ITEMS (or ORDER_DETAILS?) ========================…_

3. _Business concept 'Order Items' — The table is clearly a line-item structure keyed by order_item_id and carrying order_id, product_id, quantity, pricing, discount, and line total fields, which aligns w…_

---

### ✅ ec_015 — When is an invoice generated vs payment processed?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.6598 | **Gate:** `proceed`

**Expected answer:**
> The relationship section in the glossary asks 'An invoice is generated for an order. But when? And can one order have multiple invoices?' indicating the timing and cardinality are not defined. The glossary defines Invoice as 'A document requesting payment. Related to Bill' and Payment as 'The transf…

**System answer:**
> The retrieved context does not define any invoice entity, invoice table, or business rule for invoice generation, so it cannot answer when an invoice is generated.

For payment processing, the context does provide schema-level evidence. Payment processing is represented by the PAYMENTS table, which includes payment_date, payment_amount, payment_method, payment_status, transaction_id, response_code…

**Sources retrieved (11):** `parent_chunk_data_dictionary.txt_3`, `parent_chunk_data_dictionary.txt_1`, `parent_chunk_data_dictionary.txt_2`, `payment_method→PAYMENTS`, `Sales→ORDERS`, `parent_chunk_business_glossary.txt_0`, `Table naming: ORDER_ITEMS vs ORDER_PRODUCTS vs ORDER_DETAILS→PRODUCTS`, `Order Items→ORDER_ITEMS`

**Context previews (first 3):**

1. _========================================== PAYMENTS ==========================================  Primary Key: payment_id (unverified) | Column Name | Data Type | Constraints | Description | |----------…_

2. _DATA DICTIONARY - Enterprise Database Version: 2.1 (incomplete documentation) Last Updated: 2024-02-28 ========================================== CUSTOMERS ========================================== P…_

3. _Foreign Keys: - customer_id → CUSTOMERS(customer_id or CustomerID?) - [missing other FK definitions] ========================================== ORDER_ITEMS (or ORDER_DETAILS?) ========================…_

---

### ✅ ec_016 — Is the sku column in PRODUCTS unique?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.3450 | **Gate:** `proceed`

**Expected answer:**
> The PRODUCTS table has both product_sku and sku columns. The data dictionary notes sku 'should be UNIQUE?' but the DDL does not define a UNIQUE constraint on either column. No index is documented for these columns.

**System answer:**
> The context shows that PRODUCTS includes both `sku` and `product_sku` columns. It does not provide any constraint or description indicating that `sku` is unique, so uniqueness for `sku` cannot be confirmed from the provided context.

**Sources retrieved (11):** `Table naming: ORDER_ITEMS vs ORDER_PRODUCTS vs ORDER_DETAILS→PRODUCTS`, `parent_chunk_data_dictionary.txt_2`, `parent_chunk_data_dictionary.txt_3`, `Order Items`, `Order Items→ORDER_ITEMS`, `parent_chunk_data_dictionary.txt_1`, `Sales→ORDERS`, `CUSTOMERS→CUSTOMERS`

**Context previews (first 3):**

1. _Business concept 'Table naming: ORDER_ITEMS vs ORDER_PRODUCTS vs ORDER_DETAILS' is implemented by physical table PRODUCTS (columns: product_id, ProductID, product_name, ProductName, product_sku, sku, …_

2. _Foreign Keys: - customer_id → CUSTOMERS(customer_id or CustomerID?) - [missing other FK definitions] ========================================== ORDER_ITEMS (or ORDER_DETAILS?) ========================…_

3. _========================================== PAYMENTS ==========================================  Primary Key: payment_id (unverified) | Column Name | Data Type | Constraints | Description | |----------…_

---

### ✅ ec_017 — What is the relationship between customers and orders?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0859 | **Gate:** `proceed_with_warning`

**Expected answer:**
> The glossary states 'A customer can place multiple orders. Or is it accounts that place orders?' indicating uncertainty about the relationship. The ORDERS table has both customer_id and CustomerID columns with ambiguous FK references, and the data dictionary notes they reference 'customer (which tab…

**System answer:**
> In the schema metadata provided, customers and orders are related through the ORDERS table.

The business concept “Sales” is implemented by the physical table ORDERS, and that table includes customer_id and CustomerID alongside order_id/OrderID. The CUSTOMERS table has primary key documentation pointing to customer_id, with CustomerID noted as a possible duplicate/inconsistent alternative. Taken t…

**Sources retrieved (11):** `parent_chunk_data_dictionary.txt_3`, `parent_chunk_data_dictionary.txt_2`, `Sales→ORDERS`, `parent_chunk_data_dictionary.txt_1`, `Order Items→ORDER_ITEMS`, `CUSTOMERS→CUSTOMERS`, `Order Items`, `parent_chunk_business_glossary.txt_0`

**Context previews (first 3):**

1. _========================================== PAYMENTS ==========================================  Primary Key: payment_id (unverified) | Column Name | Data Type | Constraints | Description | |----------…_

2. _Foreign Keys: - customer_id → CUSTOMERS(customer_id or CustomerID?) - [missing other FK definitions] ========================================== ORDER_ITEMS (or ORDER_DETAILS?) ========================…_

3. _Business concept 'Sales' is implemented by physical table ORDERS (columns: order_id, OrderID, customer_id, CustomerID, order_date, OrderDate, order_status, orderAmount, total_amount, shippingAmount, t…_

---

### ✅ ec_018 — Which price column represents what the customer actually pays?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0682 | **Gate:** `proceed_with_warning`

**Expected answer:**
> Multiple price columns exist across tables: ORDERS has orderAmount and total_amount; ORDER_ITEMS has unit_price and UnitPrice; PRODUCTS has unit_price, current_price, and cost_price. The data dictionary does not explain which represents the final customer price, whether discounts are applied, or how…

**System answer:**
> The retrieved context does not explicitly define a single canonical column for “what the customer actually pays.”

From the schema, the only supported likely candidates are PAYMENTS.payment_amount, ORDER_ITEMS.line_total, and ORDERS.total_amount. PAYMENTS.payment_amount is the amount on a payment record in PAYMENTS; ORDER_ITEMS.line_total is the amount at the individual line-item level in ORDER_IT…

**Sources retrieved (11):** `payment_method→PAYMENTS`, `Sales→ORDERS`, `parent_chunk_data_dictionary.txt_2`, `parent_chunk_data_dictionary.txt_3`, `Order Items→ORDER_ITEMS`, `Table naming: ORDER_ITEMS vs ORDER_PRODUCTS vs ORDER_DETAILS→PRODUCTS`, `CUSTOMERS→CUSTOMERS`, `parent_chunk_data_dictionary.txt_1`

**Context previews (first 3):**

1. _Business concept 'payment_method' is implemented by physical table PAYMENTS (columns: payment_id, PaymentID, order_id, customer_id, payment_date, payment_amount, payment_method, payment_status, transa…_

2. _Business concept 'Sales' is implemented by physical table ORDERS (columns: order_id, OrderID, customer_id, CustomerID, order_date, OrderDate, order_status, orderAmount, total_amount, shippingAmount, t…_

3. _Foreign Keys: - customer_id → CUSTOMERS(customer_id or CustomerID?) - [missing other FK definitions] ========================================== ORDER_ITEMS (or ORDER_DETAILS?) ========================…_

---

### ✅ ec_019 — What's the difference between Shipment, Delivery, and Fulfillment?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0050 | **Gate:** `proceed_with_warning`

**Expected answer:**
> The glossary provides definitions but unclear boundaries: Shipment is 'The process of delivering goods to a customer'; Delivery is 'The completion of a Shipment when goods reach the customer'; Fulfillment is 'The process of preparing and delivering orders. Encompasses Shipment and Delivery.' The exa…

**System answer:**
> The retrieved context does not define Shipment, Delivery, or Fulfillment, so their difference cannot be determined from the knowledge graph.

What is known from the context is only that the business glossary is partial and includes some order-related terms such as Order, defined as “a request to purchase products or services” that “can be in various states,” and Transaction, described as similar t…

**Sources retrieved (11):** `parent_chunk_data_dictionary.txt_2`, `Order Items→ORDER_ITEMS`, `parent_chunk_data_dictionary.txt_3`, `Order Items`, `parent_chunk_business_glossary.txt_0`, `parent_chunk_data_dictionary.txt_1`, `Sales→ORDERS`, `Table naming: ORDER_ITEMS vs ORDER_PRODUCTS vs ORDER_DETAILS→PRODUCTS`

**Context previews (first 3):**

1. _Foreign Keys: - customer_id → CUSTOMERS(customer_id or CustomerID?) - [missing other FK definitions] ========================================== ORDER_ITEMS (or ORDER_DETAILS?) ========================…_

2. _Business concept 'Order Items' — The table is clearly a line-item structure keyed by order_item_id and carrying order_id, product_id, quantity, pricing, discount, and line total fields, which aligns w…_

3. _========================================== PAYMENTS ==========================================  Primary Key: payment_id (unverified) | Column Name | Data Type | Constraints | Description | |----------…_

---

### ✅ ec_020 — Are foreign key constraints enforced in the schema?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.1603 | **Gate:** `proceed_with_warning`

**Expected answer:**
> No foreign key constraints are enforced in the DDL. While the data dictionary documents FK relationships (e.g., customer_id → CUSTOMERS, order_id → ORDERS), the actual CREATE TABLE statements omit the REFERENCES clauses. The schema explicitly notes 'FK constraints defined in data dictionary but not …

**System answer:**
> The retrieved context does not confirm that foreign key constraints are actually enforced by the database.

It does show intended foreign key relationships in the schema documentation:
ORDER_ITEMS.order_id is marked FK to ORDERS, ORDER_ITEMS.product_id is marked FK to PRODUCTS (with uncertainty: “or INVENTORY?”), PAYMENTS.order_id is marked FK to ORDERS, PAYMENTS.customer_id is marked FK to CUSTOM…

**Sources retrieved (11):** `parent_chunk_data_dictionary.txt_2`, `Order Items`, `Order Items→ORDER_ITEMS`, `parent_chunk_data_dictionary.txt_3`, `parent_chunk_data_dictionary.txt_1`, `parent_chunk_business_glossary.txt_0`, `Sales→ORDERS`, `Table naming: ORDER_ITEMS vs ORDER_PRODUCTS vs ORDER_DETAILS→PRODUCTS`

**Context previews (first 3):**

1. _Foreign Keys: - customer_id → CUSTOMERS(customer_id or CustomerID?) - [missing other FK definitions] ========================================== ORDER_ITEMS (or ORDER_DETAILS?) ========================…_

2. _Order Items: The table is clearly a line-item structure keyed by order_item_id and carrying order_id, product_id, quantity, pricing, discount, and line total fields, which aligns with Order Items rath…_

3. _Business concept 'Order Items' — The table is clearly a line-item structure keyed by order_item_id and carrying order_id, product_id, quantity, pricing, discount, and line total fields, which aligns w…_

---

## Anomalies & Observations

No anomalies detected. All questions grounded with acceptable RAGAS scores.
