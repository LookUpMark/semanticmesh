# AB-10 — 05_edgecases_incomplete — Run Analysis

**Timestamp:** 2026-04-01 00:00:17  
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
| Triplets extracted | 216 |
| Entities resolved | 92 |
| Tables parsed | 5 |
| Tables completed | 5 |

## Query Evaluation Summary

| Metric | Value |
|--------|-------|
| Questions | 20 |
| Grounded | **20/20 (100%)** |
| Avg GT Coverage | 100% |
| Avg Top Score | 0.4668 |
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
> In the BUSINESS GLOSSARY, Customer is defined only partially as “An individual or organization that...” and the definition is marked incomplete.

From the same glossary, Client is “a person or company that purchases goods or services” and may be used interchangeably with Customer in some contexts. Related terms are distinguished as follows: Account Holder is the primary owner of an account and is …

**Sources retrieved (9):** `parent_chunk_data_dictionary.txt_1`, `parent_chunk_data_dictionary.txt_2`, `Sales→ORDERS`, `parent_chunk_data_dictionary.txt_3`, `payment_method→PAYMENTS`, `parent_chunk_business_glossary.txt_0`, `Order Items→ORDER_ITEMS`, `Inventory Item→PRODUCTS`

**Context previews (first 3):**

1. _DATA DICTIONARY - Enterprise Database Version: 2.1 (incomplete documentation) Last Updated: 2024-02-28 ========================================== CUSTOMERS ========================================== P…_

2. _Foreign Keys: - customer_id → CUSTOMERS(customer_id or CustomerID?) - [missing other FK definitions] ========================================== ORDER_ITEMS (or ORDER_DETAILS?) ========================…_

3. _Business concept 'Sales' is implemented by physical table ORDERS (columns: order_id, OrderID, customer_id, CustomerID, order_date, OrderDate, order_status, orderAmount, total_amount, shippingAmount, t…_

---

### ✅ ec_002 — What's the difference between firstName and first_name in the CUSTOMERS table?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.3978 | **Gate:** `proceed`

**Expected answer:**
> Both columns exist in the CUSTOMERS table with identical VARCHAR(50) data types. The data dictionary notes they appear to be duplicates resulting from inconsistent naming conventions (snake_case vs camelCase), but the actual usage by the application is not documented.

**System answer:**
> In the provided CUSTOMERS table documentation, there is no confirmed business difference between firstName and first_name.

The context shows that both columns are VARCHAR(50). firstName is described as "Customer's first name," while first_name is explicitly noted as "[appears to be duplicate]." Because the data dictionary is marked incomplete, the actual distinction—if any—cannot be confirmed fro…

**Sources retrieved (9):** `parent_chunk_data_dictionary.txt_1`, `parent_chunk_data_dictionary.txt_2`, `parent_chunk_data_dictionary.txt_3`, `Order Items→ORDER_ITEMS`, `parent_chunk_business_glossary.txt_0`, `Order Items`, `Sales→ORDERS`, `payment_method→PAYMENTS`

**Context previews (first 3):**

1. _DATA DICTIONARY - Enterprise Database Version: 2.1 (incomplete documentation) Last Updated: 2024-02-28 ========================================== CUSTOMERS ========================================== P…_

2. _Foreign Keys: - customer_id → CUSTOMERS(customer_id or CustomerID?) - [missing other FK definitions] ========================================== ORDER_ITEMS (or ORDER_DETAILS?) ========================…_

3. _========================================== PAYMENTS ==========================================  Primary Key: payment_id (unverified) | Column Name | Data Type | Constraints | Description | |----------…_

---

### ✅ ec_003 — Which customer column should be used as a foreign key reference: customer_id or CustomerID?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.9258 | **Gate:** `proceed`

**Expected answer:**
> The CUSTOMERS table has both customer_id (defined as PRIMARY KEY) and CustomerID (defined as INTEGER with no constraints). The ORDERS table also has both customer_id and CustomerID columns with ambiguous FK references. The data dictionary indicates this inconsistency is documented but not yet resolv…

**System answer:**
> The retrieved context does not establish this definitively because the schema documentation is inconsistent.

From the available metadata, the strongest indication is to use `customer_id`:
` table, the documented primary key is `customer_id`, but it is explicitly qualified with “or is it `CustomerID`? check with DBA”.
- In the foreign key notes, the relationship is written as `customer_id → CUSTOM…

**Sources retrieved (9):** `parent_chunk_data_dictionary.txt_2`, `parent_chunk_data_dictionary.txt_1`, `parent_chunk_data_dictionary.txt_3`, `Sales→ORDERS`, `payment_method→PAYMENTS`, `Order Items→ORDER_ITEMS`, `Inventory Item→PRODUCTS`, `parent_chunk_business_glossary.txt_0`

**Context previews (first 3):**

1. _Foreign Keys: - customer_id → CUSTOMERS(customer_id or CustomerID?) - [missing other FK definitions] ========================================== ORDER_ITEMS (or ORDER_DETAILS?) ========================…_

2. _DATA DICTIONARY - Enterprise Database Version: 2.1 (incomplete documentation) Last Updated: 2024-02-28 ========================================== CUSTOMERS ========================================== P…_

3. _========================================== PAYMENTS ==========================================  Primary Key: payment_id (unverified) | Column Name | Data Type | Constraints | Description | |----------…_

---

### ✅ ec_004 — What are the valid values for order_status?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.3951 | **Gate:** `proceed`

**Expected answer:**
> The business glossary documents several order statuses: Pending, Processing, Completed, Cancelled, On Hold, and Failed (which is marked as [definition missing]). However, these are not enforced by a CHECK constraint in the schema, and the data dictionary notes that valid values reference '[missing d…

**System answer:**
> The retrieved context shows that `order_status` is a column on the `ORDERS` table, which implements the business concept `Sales`. The `ORDERS` columns listed are `order_id`, `OrderID`, `customer_id`, `CustomerID`, `order_date`, `OrderDate`, `order_status`, `orderAmount`, `total_amount`, `shippingAmount`, `tax_amount`, `TaxAmount`, `payment_status`, `payment_method`, `created_at`, `updated_at`, `no…

**Sources retrieved (9):** `parent_chunk_data_dictionary.txt_3`, `Sales→ORDERS`, `parent_chunk_data_dictionary.txt_1`, `parent_chunk_data_dictionary.txt_2`, `parent_chunk_business_glossary.txt_0`, `payment_method→PAYMENTS`, `Order Items→ORDER_ITEMS`, `Inventory Item→PRODUCTS`

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
> From the retrieved context, the only clearly documented distinction is this:

“Inventory Item” is a business concept implemented by the PRODUCTS table. That table holds the product master/inventory attributes, including product_id, product_name, product_sku or sku, category, pricing, stock quantity, reorder level, active flags, timestamps, and description.

“Order Items” is a different business co…

**Sources retrieved (9):** `Inventory Item→PRODUCTS`, `parent_chunk_data_dictionary.txt_2`, `Order Items→ORDER_ITEMS`, `parent_chunk_data_dictionary.txt_1`, `parent_chunk_data_dictionary.txt_3`, `parent_chunk_business_glossary.txt_0`, `Order Items`, `Sales→ORDERS`

**Context previews (first 3):**

1. _Business concept 'Inventory Item' is implemented by physical table PRODUCTS (columns: product_id, ProductID, product_name, ProductName, product_sku, sku, product_category, category, unit_price, curren…_

2. _Foreign Keys: - customer_id → CUSTOMERS(customer_id or CustomerID?) - [missing other FK definitions] ========================================== ORDER_ITEMS (or ORDER_DETAILS?) ========================…_

3. _Business concept 'Order Items' — The table stores per-line order data such as product_id, quantity, unit_price, discount, and line_total, which strongly indicates order line items. The provided busine…_

---

### ✅ ec_006 — Which table should ORDER_ITEMS.product_id reference: PRODUCTS or INVENTORY?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.9608 | **Gate:** `proceed`

**Expected answer:**
> The data dictionary states the FK reference is to 'PRODUCTS (or INVENTORY?)' and notes it is 'not verified'. The schema provides two potential targets: PRODUCTS table (which has product_id) and an INVENTORY table that is referenced in documentation but not defined in the DDL. The actual relationship…

**System answer:**
> Based on the retrieved context, ORDER_ITEMS.product_id should reference PRODUCTS.

The evidence is:

The ORDER_ITEMS schema note says product_id is an FK and lists “References PRODUCTS (or INVENTORY?)”, so the raw FK documentation is ambiguous.

But the business concept mapping resolves that ambiguity: the business concept “Inventory Item” is implemented by the physical table PRODUCTS, not a table…

**Sources retrieved (9):** `parent_chunk_data_dictionary.txt_2`, `Inventory Item→PRODUCTS`, `Order Items→ORDER_ITEMS`, `parent_chunk_data_dictionary.txt_3`, `parent_chunk_data_dictionary.txt_1`, `Order Items`, `parent_chunk_business_glossary.txt_0`, `Sales→ORDERS`

**Context previews (first 3):**

1. _Foreign Keys: - customer_id → CUSTOMERS(customer_id or CustomerID?) - [missing other FK definitions] ========================================== ORDER_ITEMS (or ORDER_DETAILS?) ========================…_

2. _Business concept 'Inventory Item' is implemented by physical table PRODUCTS (columns: product_id, ProductID, product_name, ProductName, product_sku, sku, product_category, category, unit_price, curren…_

3. _Business concept 'Order Items' — The table stores per-line order data such as product_id, quantity, unit_price, discount, and line_total, which strongly indicates order line items. The provided busine…_

---

### ✅ ec_007 — What's the difference between Revenue and Sales?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.4224 | **Gate:** `proceed`

**Expected answer:**
> Both terms show circular definitions: Revenue is defined as 'Income from sales. The same as... [definition circular, see Sales]', while Sales is defined as 'Revenue from selling products. See Revenue.' The glossary provides no clear distinction between these concepts.

**System answer:**
> From the retrieved context, only Sales is described; Revenue is not defined anywhere in the provided material, so a direct difference between the two cannot be established from this knowledge graph.

What the context does say about Sales is that the business concept Sales is implemented by the physical table ORDERS. The ORDERS table includes these columns: order_id, OrderID, customer_id, CustomerI…

**Sources retrieved (9):** `Sales→ORDERS`, `parent_chunk_data_dictionary.txt_2`, `parent_chunk_data_dictionary.txt_3`, `Order Items→ORDER_ITEMS`, `parent_chunk_business_glossary.txt_0`, `Order Items`, `parent_chunk_data_dictionary.txt_1`, `payment_method→PAYMENTS`

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
> Based on the schema metadata provided, yes: one order appears able to have multiple payments.

The evidence is that PAYMENTS has its own primary key, payment_id, and also contains order_id as a foreign key referencing ORDERS. That structure indicates PAYMENTS is a child table of ORDERS, so multiple PAYMENTS rows can point to the same ORDERS row through order_id. There is no uniqueness constraint s…

**Sources retrieved (9):** `parent_chunk_data_dictionary.txt_3`, `payment_method→PAYMENTS`, `Sales→ORDERS`, `parent_chunk_data_dictionary.txt_2`, `parent_chunk_data_dictionary.txt_1`, `Order Items→ORDER_ITEMS`, `Inventory Item→PRODUCTS`, `parent_chunk_business_glossary.txt_0`

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
> The retrieved context does not specify which payment methods are accepted.

It only shows that payment method is stored in two places:
PAYMENTS.payment_method, defined as VARCHAR(30) with “[missing valid values],” and ORDERS.payment_method, listed as a column in ORDERS.

No allowed or enumerated payment_method values are provided in the context.

**Sources retrieved (9):** `parent_chunk_data_dictionary.txt_3`, `payment_method→PAYMENTS`, `Sales→ORDERS`, `parent_chunk_data_dictionary.txt_1`, `parent_chunk_data_dictionary.txt_2`, `parent_chunk_business_glossary.txt_0`, `Order Items→ORDER_ITEMS`, `Inventory Item→PRODUCTS`

**Context previews (first 3):**

1. _========================================== PAYMENTS ==========================================  Primary Key: payment_id (unverified) | Column Name | Data Type | Constraints | Description | |----------…_

2. _Business concept 'payment_method' is implemented by physical table PAYMENTS (columns: payment_id, PaymentID, order_id, customer_id, payment_date, payment_amount, payment_method, payment_status, transa…_

3. _Business concept 'Sales' is implemented by physical table ORDERS (columns: order_id, OrderID, customer_id, CustomerID, order_date, OrderDate, order_status, orderAmount, total_amount, shippingAmount, t…_

---

### ✅ ec_010 — What's the correct table name: ORDER_ITEMS or ORDER_DETAILS?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.9905 | **Gate:** `proceed`

**Expected answer:**
> The DDL creates a table named ORDER_ITEMS, but the data dictionary header shows 'ORDER_ITEMS (or ORDER_DETAILS?)' and notes 'Table name ambiguity: ORDER_ITEMS vs ORDER_DETAILS'. The actual table name in the schema is ORDER_ITEMS, but documentation suggests the application may reference it differentl…

**System answer:**
> Based on the retrieved context, the physical table name is ORDER_ITEMS.

The context explicitly says the business concept “Order Items” is implemented by physical table ORDER_ITEMS, and that ORDER_ITEMS is synonymous with ORDER_DETAILS. So ORDER_DETAILS appears to be an alternate name or synonym in the documentation, but the mapped table name is ORDER_ITEMS. The source also shows some documentatio…

**Sources retrieved (9):** `parent_chunk_data_dictionary.txt_2`, `Order Items→ORDER_ITEMS`, `Inventory Item→PRODUCTS`, `parent_chunk_data_dictionary.txt_3`, `parent_chunk_data_dictionary.txt_1`, `Order Items`, `Sales→ORDERS`, `payment_method→PAYMENTS`

**Context previews (first 3):**

1. _Foreign Keys: - customer_id → CUSTOMERS(customer_id or CustomerID?) - [missing other FK definitions] ========================================== ORDER_ITEMS (or ORDER_DETAILS?) ========================…_

2. _Business concept 'Order Items' — The table stores per-line order data such as product_id, quantity, unit_price, discount, and line_total, which strongly indicates order line items. The provided busine…_

3. _Business concept 'Inventory Item' is implemented by physical table PRODUCTS (columns: product_id, ProductID, product_name, ProductName, product_sku, sku, product_category, category, unit_price, curren…_

---

### ✅ ec_011 — Which date column should be used to track when an order was created: order_date, OrderDate, or created_at?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.9218 | **Gate:** `proceed`

**Expected answer:**
> The ORDERS table has three date-related columns: order_date (DATE type), OrderDate (DATETIME type with different precision), and created_at (TIMESTAMP type). The data dictionary provides no guidance on which is actually used by the application or why three columns exist for potentially the same purp…

**System answer:**
> From the retrieved context alone, this cannot be determined definitively.

The ORDERS table for the business concept Sales includes all three columns: order_date, OrderDate, and created_at. However, the context provides only the column list for ORDERS and does not define the meaning of those fields or distinguish whether order_date and OrderDate are duplicates, variants, or separate attributes. It…

**Sources retrieved (9):** `Sales→ORDERS`, `payment_method→PAYMENTS`, `parent_chunk_data_dictionary.txt_1`, `parent_chunk_data_dictionary.txt_3`, `Inventory Item→PRODUCTS`, `Order Items→ORDER_ITEMS`, `parent_chunk_data_dictionary.txt_2`, `Order Items`

**Context previews (first 3):**

1. _Business concept 'Sales' is implemented by physical table ORDERS (columns: order_id, OrderID, customer_id, CustomerID, order_date, OrderDate, order_status, orderAmount, total_amount, shippingAmount, t…_

2. _Business concept 'payment_method' is implemented by physical table PAYMENTS (columns: payment_id, PaymentID, order_id, customer_id, payment_date, payment_amount, payment_method, payment_status, transa…_

3. _DATA DICTIONARY - Enterprise Database Version: 2.1 (incomplete documentation) Last Updated: 2024-02-28 ========================================== CUSTOMERS ========================================== P…_

---

### ✅ ec_012 — What does the Failed order status mean?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0031 | **Gate:** `proceed_with_warning`

**Expected answer:**
> The business glossary lists Failed as an order status but marks it as '[definition missing]'. Other statuses have definitions (Pending, Processing, Completed, Cancelled, On Hold), but Failed is undefined despite being a valid status value.

**System answer:**
> I cannot determine the meaning of the Failed order status from the retrieved context.

What the context does show is that the Sales concept is implemented by the ORDERS table, and that ORDERS includes an order_status column. The business glossary also says an Order “can be in various states.” However, no valid order status values or definitions are provided, and Failed is not described anywhere in…

**Sources retrieved (9):** `parent_chunk_data_dictionary.txt_3`, `parent_chunk_data_dictionary.txt_1`, `Sales→ORDERS`, `parent_chunk_data_dictionary.txt_2`, `Order Items→ORDER_ITEMS`, `payment_method→PAYMENTS`, `Inventory Item→PRODUCTS`, `parent_chunk_business_glossary.txt_0`

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
> No explicit NOT NULL constraints are defined in the provided schema context.

In the shown table metadata for CUSTOMERS, PAYMENTS, ORDER_ITEMS, and the ORDERS/PRODUCTS concept mappings, the documented constraints include PK, FK, and a possible UNIQUE on PAYMENTS.transaction_id, but no column is explicitly labeled NOT NULL. Many constraint entries are marked as "?" or described as missing/incomplet…

**Sources retrieved (9):** `parent_chunk_data_dictionary.txt_3`, `parent_chunk_data_dictionary.txt_2`, `parent_chunk_data_dictionary.txt_1`, `Sales→ORDERS`, `parent_chunk_business_glossary.txt_0`, `Inventory Item→PRODUCTS`, `payment_method→PAYMENTS`, `Order Items→ORDER_ITEMS`

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
> The retrieved context shows that PRODUCTS, which implements the business concept Inventory Item, contains both unit_price and current_price columns, along with cost_price.

However, the context does not define the difference between unit_price and current_price within PRODUCTS. There are no column descriptions, calculation rules, or business glossary entries explaining how those two PRODUCTS field…

**Sources retrieved (9):** `Inventory Item→PRODUCTS`, `parent_chunk_data_dictionary.txt_2`, `Order Items→ORDER_ITEMS`, `parent_chunk_data_dictionary.txt_3`, `Order Items`, `parent_chunk_business_glossary.txt_0`, `parent_chunk_data_dictionary.txt_1`, `Sales→ORDERS`

**Context previews (first 3):**

1. _Business concept 'Inventory Item' is implemented by physical table PRODUCTS (columns: product_id, ProductID, product_name, ProductName, product_sku, sku, product_category, category, unit_price, curren…_

2. _Foreign Keys: - customer_id → CUSTOMERS(customer_id or CustomerID?) - [missing other FK definitions] ========================================== ORDER_ITEMS (or ORDER_DETAILS?) ========================…_

3. _Business concept 'Order Items' — The table stores per-line order data such as product_id, quantity, unit_price, discount, and line_total, which strongly indicates order line items. The provided busine…_

---

### ✅ ec_015 — When is an invoice generated vs payment processed?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.6598 | **Gate:** `proceed`

**Expected answer:**
> The relationship section in the glossary asks 'An invoice is generated for an order. But when? And can one order have multiple invoices?' indicating the timing and cardinality are not defined. The glossary defines Invoice as 'A document requesting payment. Related to Bill' and Payment as 'The transf…

**System answer:**
> The retrieved context does not define an invoice or invoice-generation event at all. There is no invoice business concept, no invoice table, and no invoice-related columns in the provided schema excerpts, so I cannot say when an invoice is generated from this context.

For payment processed, the context does show the schema used to capture payments. The business concept `payment_method` is impleme…

**Sources retrieved (9):** `parent_chunk_data_dictionary.txt_3`, `parent_chunk_data_dictionary.txt_1`, `parent_chunk_data_dictionary.txt_2`, `payment_method→PAYMENTS`, `Sales→ORDERS`, `parent_chunk_business_glossary.txt_0`, `Inventory Item→PRODUCTS`, `Order Items→ORDER_ITEMS`

**Context previews (first 3):**

1. _========================================== PAYMENTS ==========================================  Primary Key: payment_id (unverified) | Column Name | Data Type | Constraints | Description | |----------…_

2. _DATA DICTIONARY - Enterprise Database Version: 2.1 (incomplete documentation) Last Updated: 2024-02-28 ========================================== CUSTOMERS ========================================== P…_

3. _Foreign Keys: - customer_id → CUSTOMERS(customer_id or CustomerID?) - [missing other FK definitions] ========================================== ORDER_ITEMS (or ORDER_DETAILS?) ========================…_

---

### ✅ ec_016 — Is the sku column in PRODUCTS unique?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.3824 | **Gate:** `proceed`

**Expected answer:**
> The PRODUCTS table has both product_sku and sku columns. The data dictionary notes sku 'should be UNIQUE?' but the DDL does not define a UNIQUE constraint on either column. No index is documented for these columns.

**System answer:**
> The retrieved context does not state that `sku` in `PRODUCTS` is unique.

What the context does say is that the business concept "Inventory Item" maps to `PRODUCTS`, which includes `product_sku` and `sku` as columns, but no uniqueness constraint is provided for either column. The documentation shown is incomplete, so from this context alone, uniqueness cannot be confirmed.

**Sources retrieved (9):** `Inventory Item→PRODUCTS`, `parent_chunk_data_dictionary.txt_2`, `parent_chunk_data_dictionary.txt_3`, `parent_chunk_data_dictionary.txt_1`, `Order Items→ORDER_ITEMS`, `Sales→ORDERS`, `payment_method→PAYMENTS`, `parent_chunk_business_glossary.txt_0`

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
> Customers and orders are related through the customer identifier stored on ORDERS.

From the context, the physical table ORDERS (mapped to the business concept “Sales”) includes customer_id and CustomerID. The CUSTOMERS table has customer_id as its primary key, with CustomerID noted as a possible duplicate/inconsistent variant. Based on that schema, the relationship is:

CUSTOMERS.customer_id (or …

**Sources retrieved (9):** `parent_chunk_data_dictionary.txt_3`, `parent_chunk_data_dictionary.txt_2`, `Sales→ORDERS`, `parent_chunk_data_dictionary.txt_1`, `Order Items→ORDER_ITEMS`, `parent_chunk_business_glossary.txt_0`, `Order Items`, `payment_method→PAYMENTS`

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
> The retrieved context does not define a single price column as “the amount the customer actually pays,” so this cannot be determined definitively.

What is known from the context is:

In PAYMENTS, the column payment_amount exists and is the payment-level amount recorded for a payment transaction.

In ORDER_ITEMS, the table contains unit_price, discount_percent, discount_amount, and line_total, so …

**Sources retrieved (9):** `payment_method→PAYMENTS`, `Sales→ORDERS`, `parent_chunk_data_dictionary.txt_2`, `parent_chunk_data_dictionary.txt_3`, `Order Items→ORDER_ITEMS`, `parent_chunk_data_dictionary.txt_1`, `Inventory Item→PRODUCTS`, `parent_chunk_business_glossary.txt_0`

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
> The retrieved context does not define the business terms Shipment, Delivery, or Fulfillment, so I cannot distinguish them from one another based on the knowledge graph.

The only related information present is in the ORDER & TRANSACTION glossary area, where Order is defined as “a request to purchase products or services” and may be in various states, and Transaction is described as a more general …

**Sources retrieved (9):** `parent_chunk_data_dictionary.txt_2`, `parent_chunk_data_dictionary.txt_3`, `Order Items→ORDER_ITEMS`, `parent_chunk_business_glossary.txt_0`, `Order Items`, `parent_chunk_data_dictionary.txt_1`, `Sales→ORDERS`, `payment_method→PAYMENTS`

**Context previews (first 3):**

1. _Foreign Keys: - customer_id → CUSTOMERS(customer_id or CustomerID?) - [missing other FK definitions] ========================================== ORDER_ITEMS (or ORDER_DETAILS?) ========================…_

2. _========================================== PAYMENTS ==========================================  Primary Key: payment_id (unverified) | Column Name | Data Type | Constraints | Description | |----------…_

3. _Business concept 'Order Items' — The table stores per-line order data such as product_id, quantity, unit_price, discount, and line_total, which strongly indicates order line items. The provided busine…_

---

### ✅ ec_020 — Are foreign key constraints enforced in the schema?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.1603 | **Gate:** `proceed_with_warning`

**Expected answer:**
> No foreign key constraints are enforced in the DDL. While the data dictionary documents FK relationships (e.g., customer_id → CUSTOMERS, order_id → ORDERS), the actual CREATE TABLE statements omit the REFERENCES clauses. The schema explicitly notes 'FK constraints defined in data dictionary but not …

**System answer:**
> The retrieved context shows that foreign key relationships are documented, but it does not confirm that they are actually enforced by the database.

What is present in the context is schema metadata marking several columns as FK:
in ORDER_ITEMS, order_id is marked as an FK referencing ORDERS, and product_id is marked as an FK referencing PRODUCTS (with uncertainty noted as “or INVENTORY?”). There …

**Sources retrieved (9):** `parent_chunk_data_dictionary.txt_2`, `parent_chunk_data_dictionary.txt_3`, `parent_chunk_data_dictionary.txt_1`, `parent_chunk_business_glossary.txt_0`, `Sales→ORDERS`, `Inventory Item→PRODUCTS`, `payment_method→PAYMENTS`, `Order Items→ORDER_ITEMS`

**Context previews (first 3):**

1. _Foreign Keys: - customer_id → CUSTOMERS(customer_id or CustomerID?) - [missing other FK definitions] ========================================== ORDER_ITEMS (or ORDER_DETAILS?) ========================…_

2. _========================================== PAYMENTS ==========================================  Primary Key: payment_id (unverified) | Column Name | Data Type | Constraints | Description | |----------…_

3. _DATA DICTIONARY - Enterprise Database Version: 2.1 (incomplete documentation) Last Updated: 2024-02-28 ========================================== CUSTOMERS ========================================== P…_

---

## Anomalies & Observations

No anomalies detected. All questions grounded with acceptable RAGAS scores.
