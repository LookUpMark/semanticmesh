# AB-19 — 05_edgecases_incomplete — Run Analysis

**Timestamp:** 2026-03-31 03:58:08  
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
| Triplets extracted | 203 |
| Entities resolved | 80 |
| Tables parsed | 5 |
| Tables completed | 5 |

## Query Evaluation Summary

| Metric | Value |
|--------|-------|
| Questions | 20 |
| Grounded | **20/20 (100%)** |
| Avg GT Coverage | 100% |
| Avg Top Score | 0.4588 |
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
> In the business glossary, Customer is defined only partially as “An individual or organization that...” so the full formal definition is incomplete in the retrieved context. The glossary also notes that Client is “a person or company that purchases goods or services” and may be used interchangeably with Customer in some contexts.

At the schema level, the Customer concept is implemented by the CUS…

**Sources retrieved (12):** `Customer→CUSTOMERS`, `parent_chunk_data_dictionary.txt_1`, `Order→ORDERS`, `parent_chunk_data_dictionary.txt_2`, `Payment→PAYMENTS`, `parent_chunk_data_dictionary.txt_3`, `parent_chunk_business_glossary.txt_0`, `Customer`

**Context previews (first 3):**

1. _Business concept 'Customer' — The table clearly models customer master data through its name and core attributes such as name, email, phone, status, type, and region. However, duplicate legacy columns…_

2. _DATA DICTIONARY - Enterprise Database Version: 2.1 (incomplete documentation) Last Updated: 2024-02-28 ========================================== CUSTOMERS ========================================== P…_

3. _Business concept 'Order' — The table clearly represents an order header with order identifiers, customer reference, order dates, statuses, payment fields, and monetary amounts. However, duplicate/conf…_

---

### ✅ ec_002 — What's the difference between firstName and first_name in the CUSTOMERS table?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.4967 | **Gate:** `proceed`

**Expected answer:**
> Both columns exist in the CUSTOMERS table with identical VARCHAR(50) data types. The data dictionary notes they appear to be duplicates resulting from inconsistent naming conventions (snake_case vs camelCase), but the actual usage by the application is not documented.

**System answer:**
> In the retrieved context, there is no documented business difference between `firstName` and `first_name` in `CUSTOMERS`.

The data dictionary shows both columns in the same table, both are `VARCHAR(50)`. `firstName` is described as “Customer's first name,” while `first_name` is explicitly noted as “[appears to be duplicate].” The business-concept mapping also flags duplicate legacy columns and in…

**Sources retrieved (12):** `Customer→CUSTOMERS`, `parent_chunk_data_dictionary.txt_1`, `parent_chunk_data_dictionary.txt_2`, `Order→ORDERS`, `parent_chunk_data_dictionary.txt_3`, `Payment→PAYMENTS`, `Order Items→ORDER_ITEMS`, `Inventory Item→PRODUCTS`

**Context previews (first 3):**

1. _Business concept 'Customer' — The table clearly models customer master data through its name and core attributes such as name, email, phone, status, type, and region. However, duplicate legacy columns…_

2. _DATA DICTIONARY - Enterprise Database Version: 2.1 (incomplete documentation) Last Updated: 2024-02-28 ========================================== CUSTOMERS ========================================== P…_

3. _Foreign Keys: - customer_id → CUSTOMERS(customer_id or CustomerID?) - [missing other FK definitions] ========================================== ORDER_ITEMS (or ORDER_DETAILS?) ========================…_

---

### ✅ ec_003 — Which customer column should be used as a foreign key reference: customer_id or CustomerID?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.9258 | **Gate:** `proceed`

**Expected answer:**
> The CUSTOMERS table has both customer_id (defined as PRIMARY KEY) and CustomerID (defined as INTEGER with no constraints). The ORDERS table also has both customer_id and CustomerID columns with ambiguous FK references. The data dictionary indicates this inconsistency is documented but not yet resolv…

**System answer:**
> From the retrieved context, this is not definitively resolved.

The strongest indication is that customer_id should be used, because:
the CUSTOMERS table lists its primary key as “customer_id (or is it CustomerID? check with DBA)”, and the documented foreign keys in other tables use customer_id, for example PAYMENTS.customer_id and the FK note “customer_id → CUSTOMERS(customer_id or CustomerID?)”.…

**Sources retrieved (12):** `parent_chunk_data_dictionary.txt_2`, `parent_chunk_data_dictionary.txt_1`, `parent_chunk_data_dictionary.txt_3`, `Customer→CUSTOMERS`, `Order→ORDERS`, `Payment→PAYMENTS`, `Inventory Item→PRODUCTS`, `Order Items→ORDER_ITEMS`

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
> The retrieved context does not provide an enumerated list of valid values for ORDERS.ORDER_STATUS.

What it does show is that ORDER_STATUS exists on the ORDERS table: the Order concept is implemented by physical table ORDERS, which includes ORDER_STATUS among its columns. The business glossary also says an Order “can be in various states,” but it does not name those states.

So, from the available…

**Sources retrieved (12):** `parent_chunk_data_dictionary.txt_3`, `Order→ORDERS`, `parent_chunk_data_dictionary.txt_1`, `parent_chunk_data_dictionary.txt_2`, `parent_chunk_business_glossary.txt_0`, `Payment→PAYMENTS`, `Inventory Item→PRODUCTS`, `Order Items→ORDER_ITEMS`

**Context previews (first 3):**

1. _========================================== PAYMENTS ==========================================  Primary Key: payment_id (unverified) | Column Name | Data Type | Constraints | Description | |----------…_

2. _Business concept 'Order' — The table clearly represents an order header with order identifiers, customer reference, order dates, statuses, payment fields, and monetary amounts. However, duplicate/conf…_

3. _DATA DICTIONARY - Enterprise Database Version: 2.1 (incomplete documentation) Last Updated: 2024-02-28 ========================================== CUSTOMERS ========================================== P…_

---

### ✅ ec_005 — Is there a difference between Product, Item, and SKU?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.5696 | **Gate:** `proceed`

**Expected answer:**
> The glossary indicates these terms are related but distinct: Product is defined as "A thing that is... [definition needs clarification]"; Item is a synonym for Product used in inventory context; SKU (Stock Keeping Unit) is a unique identifier for a product variant; Inventory Item refers to physical …

**System answer:**
> From the retrieved context, I cannot confirm a defined business difference between “Product,” “Item,” and “SKU.”

What the context does show is this: the business concept explicitly defined is “Inventory Item,” and it is implemented by the physical table PRODUCTS. That table includes columns such as PRODUCT_ID, PRODUCTID, PRODUCT_NAME, PRODUCTNAME, PRODUCT_SKU, SKU, PRODUCT_CATEGORY, CATEGORY, UNI…

**Sources retrieved (12):** `Inventory Item→PRODUCTS`, `parent_chunk_data_dictionary.txt_2`, `Order Items→ORDER_ITEMS`, `parent_chunk_data_dictionary.txt_1`, `Customer→CUSTOMERS`, `Order→ORDERS`, `parent_chunk_data_dictionary.txt_3`, `parent_chunk_business_glossary.txt_0`

**Context previews (first 3):**

1. _Business concept 'Inventory Item' — The table centers on a stock-held item with identifiers, pricing, category, quantity on hand, reorder level, and active status, which fits the inventory-item concep…_

2. _Foreign Keys: - customer_id → CUSTOMERS(customer_id or CustomerID?) - [missing other FK definitions] ========================================== ORDER_ITEMS (or ORDER_DETAILS?) ========================…_

3. _Business concept 'Order Items' — The table name, key structure, and line-level pricing/quantity columns clearly indicate an order line-item implementation. The provided business entity ORDER_ITEMS (or…_

---

### ✅ ec_006 — Which table should ORDER_ITEMS.product_id reference: PRODUCTS or INVENTORY?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.9608 | **Gate:** `proceed`

**Expected answer:**
> The data dictionary states the FK reference is to 'PRODUCTS (or INVENTORY?)' and notes it is 'not verified'. The schema provides two potential targets: PRODUCTS table (which has product_id) and an INVENTORY table that is referenced in documentation but not defined in the DDL. The actual relationship…

**System answer:**
> Based on the retrieved context, ORDER_ITEMS.product_id should reference PRODUCTS.

The strongest support is that the ORDER_ITEMS definition says product_id is an FK that “References PRODUCTS (or INVENTORY?)”, while the business concept “Inventory Item” is explicitly implemented by the physical table PRODUCTS, not by a separate INVENTORY table. The PRODUCTS table includes PRODUCT_ID and PRODUCTID, …

**Sources retrieved (12):** `parent_chunk_data_dictionary.txt_2`, `Inventory Item→PRODUCTS`, `Order Items→ORDER_ITEMS`, `Order→ORDERS`, `parent_chunk_data_dictionary.txt_3`, `parent_chunk_data_dictionary.txt_1`, `Inventory Item`, `parent_chunk_business_glossary.txt_0`

**Context previews (first 3):**

1. _Foreign Keys: - customer_id → CUSTOMERS(customer_id or CustomerID?) - [missing other FK definitions] ========================================== ORDER_ITEMS (or ORDER_DETAILS?) ========================…_

2. _Business concept 'Inventory Item' — The table centers on a stock-held item with identifiers, pricing, category, quantity on hand, reorder level, and active status, which fits the inventory-item concep…_

3. _Business concept 'Order Items' — The table name, key structure, and line-level pricing/quantity columns clearly indicate an order line-item implementation. The provided business entity ORDER_ITEMS (or…_

---

### ✅ ec_007 — What's the difference between Revenue and Sales?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.4224 | **Gate:** `proceed`

**Expected answer:**
> Both terms show circular definitions: Revenue is defined as 'Income from sales. The same as... [definition circular, see Sales]', while Sales is defined as 'Revenue from selling products. See Revenue.' The glossary provides no clear distinction between these concepts.

**System answer:**
> The retrieved context does not define either business concept “Revenue” or “Sales,” so it does not provide a direct difference between them.

What the context does provide is the surrounding order and payment structure that might be used in such a distinction, but without any rule connecting those structures to “Revenue” or “Sales.” Specifically, the glossary defines Order as “a request to purchas…

**Sources retrieved (12):** `Order→ORDERS`, `Inventory Item→PRODUCTS`, `parent_chunk_data_dictionary.txt_2`, `Order Items→ORDER_ITEMS`, `Customer→CUSTOMERS`, `Payment→PAYMENTS`, `parent_chunk_data_dictionary.txt_3`, `parent_chunk_business_glossary.txt_0`

**Context previews (first 3):**

1. _Business concept 'Order' — The table clearly represents an order header with order identifiers, customer reference, order dates, statuses, payment fields, and monetary amounts. However, duplicate/conf…_

2. _Business concept 'Inventory Item' — The table centers on a stock-held item with identifiers, pricing, category, quantity on hand, reorder level, and active status, which fits the inventory-item concep…_

3. _Foreign Keys: - customer_id → CUSTOMERS(customer_id or CustomerID?) - [missing other FK definitions] ========================================== ORDER_ITEMS (or ORDER_DETAILS?) ========================…_

---

### ✅ ec_008 — Can one order have multiple payments?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0981 | **Gate:** `proceed_with_warning`

**Expected answer:**
> The PAYMENTS table has an order_id column, suggesting a many-to-one relationship (multiple payments can reference a single order). However, the relationship section in the glossary asks 'Or is it one-to-one?' indicating uncertainty. The ORDERS table has both payment_status and payment_method columns…

**System answer:**
> Based on the retrieved schema metadata, yes, one order appears able to have multiple payments.

The evidence is that PAYMENTS has its own primary key, payment_id, and includes order_id as a foreign key referencing ORDERS. That structure implies PAYMENTS is a child table of ORDERS, so multiple payment records could point to the same order_id. There is no documented unique constraint on PAYMENTS.ord…

**Sources retrieved (12):** `parent_chunk_data_dictionary.txt_3`, `Order→ORDERS`, `Payment→PAYMENTS`, `parent_chunk_data_dictionary.txt_2`, `parent_chunk_data_dictionary.txt_1`, `Order Items→ORDER_ITEMS`, `Customer→CUSTOMERS`, `Inventory Item→PRODUCTS`

**Context previews (first 3):**

1. _========================================== PAYMENTS ==========================================  Primary Key: payment_id (unverified) | Column Name | Data Type | Constraints | Description | |----------…_

2. _Business concept 'Order' — The table clearly represents an order header with order identifiers, customer reference, order dates, statuses, payment fields, and monetary amounts. However, duplicate/conf…_

3. _Business concept 'Payment' — The table is explicitly named PAYMENTS and includes core payment attributes such as payment_date, payment_amount, payment_method, payment_status, and gateway response deta…_

---

### ✅ ec_009 — What payment methods are accepted?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.1791 | **Gate:** `proceed_with_warning`

**Expected answer:**
> The PAYMENTS table has a payment_method column (VARCHAR(30)), but the data dictionary notes '[missing valid values]' and no CHECK constraint exists to enumerate acceptable methods. The schema does not document what values are valid (e.g., credit_card, debit, paypal, etc.).

**System answer:**
> The retrieved context does not list any accepted payment method values.

What it does show is that payment method is modeled in two places: the PAYMENTS table includes a `payment_method` column of type `VARCHAR(30)`, and its documentation explicitly says the valid values are missing; the ORDERS table also includes a `PAYMENT_METHOD` column as part of the order header’s payment fields. The business…

**Sources retrieved (12):** `parent_chunk_data_dictionary.txt_3`, `Payment→PAYMENTS`, `Order→ORDERS`, `parent_chunk_data_dictionary.txt_1`, `parent_chunk_data_dictionary.txt_2`, `Payment`, `parent_chunk_business_glossary.txt_0`, `Order`

**Context previews (first 3):**

1. _========================================== PAYMENTS ==========================================  Primary Key: payment_id (unverified) | Column Name | Data Type | Constraints | Description | |----------…_

2. _Business concept 'Payment' — The table is explicitly named PAYMENTS and includes core payment attributes such as payment_date, payment_amount, payment_method, payment_status, and gateway response deta…_

3. _Business concept 'Order' — The table clearly represents an order header with order identifiers, customer reference, order dates, statuses, payment fields, and monetary amounts. However, duplicate/conf…_

---

### ✅ ec_010 — What's the correct table name: ORDER_ITEMS or ORDER_DETAILS?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.9811 | **Gate:** `proceed`

**Expected answer:**
> The DDL creates a table named ORDER_ITEMS, but the data dictionary header shows 'ORDER_ITEMS (or ORDER_DETAILS?)' and notes 'Table name ambiguity: ORDER_ITEMS vs ORDER_DETAILS'. The actual table name in the schema is ORDER_ITEMS, but documentation suggests the application may reference it differentl…

**System answer:**
> Based on the retrieved context, the physical table is identified as ORDER_ITEMS. The strongest evidence is the concept-to-table mapping, which says the business concept “Order Items” is implemented by physical table ORDER_ITEMS.

That said, the documentation is inconsistent: some chunks label it as “ORDER_ITEMS (or ORDER_DETAILS?)”, so ORDER_DETAILS appears as an undocumented alternate name or sou…

**Sources retrieved (12):** `parent_chunk_data_dictionary.txt_2`, `Order Items→ORDER_ITEMS`, `Inventory Item→PRODUCTS`, `Payment→PAYMENTS`, `parent_chunk_data_dictionary.txt_3`, `parent_chunk_data_dictionary.txt_1`, `Order Items`, `Payment`

**Context previews (first 3):**

1. _Foreign Keys: - customer_id → CUSTOMERS(customer_id or CustomerID?) - [missing other FK definitions] ========================================== ORDER_ITEMS (or ORDER_DETAILS?) ========================…_

2. _Business concept 'Order Items' — The table name, key structure, and line-level pricing/quantity columns clearly indicate an order line-item implementation. The provided business entity ORDER_ITEMS (or…_

3. _Business concept 'Inventory Item' — The table centers on a stock-held item with identifiers, pricing, category, quantity on hand, reorder level, and active status, which fits the inventory-item concep…_

---

### ✅ ec_011 — Which date column should be used to track when an order was created: order_date, OrderDate, or created_at?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.7551 | **Gate:** `proceed`

**Expected answer:**
> The ORDERS table has three date-related columns: order_date (DATE type), OrderDate (DATETIME type with different precision), and created_at (TIMESTAMP type). The data dictionary provides no guidance on which is actually used by the application or why three columns exist for potentially the same purp…

**System answer:**
> The retrieved context does not identify a single authoritative column.

For ORDERS, the available columns include ORDER_DATE, ORDERDATE, and CREATED_AT. But the context also says the table has duplicate/conflicting columns and incomplete documentation, so it is treated only as a generic Order record rather than a cleanly defined canonical structure.

Based on the context alone, I cannot confirm wh…

**Sources retrieved (12):** `Order→ORDERS`, `parent_chunk_data_dictionary.txt_1`, `parent_chunk_data_dictionary.txt_3`, `Payment→PAYMENTS`, `Customer→CUSTOMERS`, `Inventory Item→PRODUCTS`, `parent_chunk_data_dictionary.txt_2`, `Order Items→ORDER_ITEMS`

**Context previews (first 3):**

1. _Business concept 'Order' — The table clearly represents an order header with order identifiers, customer reference, order dates, statuses, payment fields, and monetary amounts. However, duplicate/conf…_

2. _DATA DICTIONARY - Enterprise Database Version: 2.1 (incomplete documentation) Last Updated: 2024-02-28 ========================================== CUSTOMERS ========================================== P…_

3. _========================================== PAYMENTS ==========================================  Primary Key: payment_id (unverified) | Column Name | Data Type | Constraints | Description | |----------…_

---

### ✅ ec_012 — What does the Failed order status mean?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0046 | **Gate:** `proceed_with_warning`

**Expected answer:**
> The business glossary lists Failed as an order status but marks it as '[definition missing]'. Other statuses have definitions (Pending, Processing, Completed, Cancelled, On Hold), but Failed is undefined despite being a valid status value.

**System answer:**
> The retrieved context does not define what the specific order status value “Failed” means.

What it does show is that the business concept Order is implemented by the ORDERS table, which includes an ORDER_STATUS column, and the glossary says an Order is “a request to purchase products or services” that “can be in various states.” But no valid values, status definitions, or lifecycle rules are prov…

**Sources retrieved (12):** `Order→ORDERS`, `parent_chunk_data_dictionary.txt_3`, `parent_chunk_data_dictionary.txt_1`, `Payment→PAYMENTS`, `Inventory Item→PRODUCTS`, `parent_chunk_data_dictionary.txt_2`, `Customer→CUSTOMERS`, `parent_chunk_business_glossary.txt_0`

**Context previews (first 3):**

1. _Business concept 'Order' — The table clearly represents an order header with order identifiers, customer reference, order dates, statuses, payment fields, and monetary amounts. However, duplicate/conf…_

2. _========================================== PAYMENTS ==========================================  Primary Key: payment_id (unverified) | Column Name | Data Type | Constraints | Description | |----------…_

3. _DATA DICTIONARY - Enterprise Database Version: 2.1 (incomplete documentation) Last Updated: 2024-02-28 ========================================== CUSTOMERS ========================================== P…_

---

### ✅ ec_013 — Are there any NOT NULL constraints defined in the schema?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.7628 | **Gate:** `proceed`

**Expected answer:**
> No NOT NULL constraints are defined in the DDL. The data dictionary explicitly states 'NOT NULL constraints not defined' under 'Missing Documentation' and notes 'assumed, not verified'. All columns are nullable by default.

**System answer:**
> Based on the retrieved context, no explicit NOT NULL constraints are defined in the provided schema excerpts.

The schema snippets show constraints such as PK, FK, and a possible UNIQUE on PAYMENTS.transaction_id, but the constraint field for most columns is either ? or missing documentation. For example, the CUSTOMERS, PAYMENTS, and ORDER_ITEMS definitions do not list any column as NOT NULL.

So,…

**Sources retrieved (12):** `parent_chunk_data_dictionary.txt_3`, `Payment→PAYMENTS`, `parent_chunk_data_dictionary.txt_2`, `parent_chunk_data_dictionary.txt_1`, `Order→ORDERS`, `Payment`, `Order`, `parent_chunk_business_glossary.txt_0`

**Context previews (first 3):**

1. _========================================== PAYMENTS ==========================================  Primary Key: payment_id (unverified) | Column Name | Data Type | Constraints | Description | |----------…_

2. _Business concept 'Payment' — The table is explicitly named PAYMENTS and includes core payment attributes such as payment_date, payment_amount, payment_method, payment_status, and gateway response deta…_

3. _Foreign Keys: - customer_id → CUSTOMERS(customer_id or CustomerID?) - [missing other FK definitions] ========================================== ORDER_ITEMS (or ORDER_DETAILS?) ========================…_

---

### ✅ ec_014 — What's the difference between unit_price and current_price in PRODUCTS?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.4514 | **Gate:** `proceed`

**Expected answer:**
> The PRODUCTS table has both unit_price and current_price columns (both DECIMAL(10,2)). The data dictionary asks 'Different from unit_price?' but provides no explanation of the distinction or when each would be used.

**System answer:**
> In the retrieved context, PRODUCTS includes both UNIT_PRICE and CURRENT_PRICE as columns on the Inventory Item/product master record, but the context does not provide column-level definitions that distinguish them.

So, based strictly on the available information, the only supported answer is: both are pricing-related fields in PRODUCTS, but the knowledge graph does not document what specific diff…

**Sources retrieved (12):** `Inventory Item→PRODUCTS`, `parent_chunk_data_dictionary.txt_2`, `Order Items→ORDER_ITEMS`, `Order→ORDERS`, `parent_chunk_data_dictionary.txt_3`, `Payment→PAYMENTS`, `parent_chunk_business_glossary.txt_0`, `Inventory Item`

**Context previews (first 3):**

1. _Business concept 'Inventory Item' — The table centers on a stock-held item with identifiers, pricing, category, quantity on hand, reorder level, and active status, which fits the inventory-item concep…_

2. _Foreign Keys: - customer_id → CUSTOMERS(customer_id or CustomerID?) - [missing other FK definitions] ========================================== ORDER_ITEMS (or ORDER_DETAILS?) ========================…_

3. _Business concept 'Order Items' — The table name, key structure, and line-level pricing/quantity columns clearly indicate an order line-item implementation. The provided business entity ORDER_ITEMS (or…_

---

### ✅ ec_015 — When is an invoice generated vs payment processed?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.6598 | **Gate:** `proceed`

**Expected answer:**
> The relationship section in the glossary asks 'An invoice is generated for an order. But when? And can one order have multiple invoices?' indicating the timing and cardinality are not defined. The glossary defines Invoice as 'A document requesting payment. Related to Bill' and Payment as 'The transf…

**System answer:**
> The retrieved context does not define when an invoice is generated. There is no Invoice business concept, table, column, or lifecycle rule in the provided material, so the invoice side of your question cannot be answered from this context.

What the context does show is how payment processing is represented at the schema level. A processed payment is modeled by the PAYMENTS table, which implements…

**Sources retrieved (12):** `parent_chunk_data_dictionary.txt_3`, `Payment→PAYMENTS`, `Order→ORDERS`, `parent_chunk_data_dictionary.txt_1`, `parent_chunk_data_dictionary.txt_2`, `parent_chunk_business_glossary.txt_0`, `Payment`, `Order`

**Context previews (first 3):**

1. _========================================== PAYMENTS ==========================================  Primary Key: payment_id (unverified) | Column Name | Data Type | Constraints | Description | |----------…_

2. _Business concept 'Payment' — The table is explicitly named PAYMENTS and includes core payment attributes such as payment_date, payment_amount, payment_method, payment_status, and gateway response deta…_

3. _Business concept 'Order' — The table clearly represents an order header with order identifiers, customer reference, order dates, statuses, payment fields, and monetary amounts. However, duplicate/conf…_

---

### ✅ ec_016 — Is the sku column in PRODUCTS unique?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.3660 | **Gate:** `proceed`

**Expected answer:**
> The PRODUCTS table has both product_sku and sku columns. The data dictionary notes sku 'should be UNIQUE?' but the DDL does not define a UNIQUE constraint on either column. No index is documented for these columns.

**System answer:**
> The retrieved context shows that PRODUCTS includes PRODUCT_SKU and SKU as columns under the business concept Inventory Item, but it does not specify any uniqueness constraint for either column. Based on the available context, I cannot confirm that SKU in PRODUCTS is unique.

**Sources retrieved (12):** `Inventory Item→PRODUCTS`, `parent_chunk_data_dictionary.txt_2`, `parent_chunk_data_dictionary.txt_3`, `Payment→PAYMENTS`, `Order Items→ORDER_ITEMS`, `parent_chunk_data_dictionary.txt_1`, `Order→ORDERS`, `parent_chunk_business_glossary.txt_0`

**Context previews (first 3):**

1. _Business concept 'Inventory Item' — The table centers on a stock-held item with identifiers, pricing, category, quantity on hand, reorder level, and active status, which fits the inventory-item concep…_

2. _Foreign Keys: - customer_id → CUSTOMERS(customer_id or CustomerID?) - [missing other FK definitions] ========================================== ORDER_ITEMS (or ORDER_DETAILS?) ========================…_

3. _========================================== PAYMENTS ==========================================  Primary Key: payment_id (unverified) | Column Name | Data Type | Constraints | Description | |----------…_

---

### ✅ ec_017 — What is the relationship between customers and orders?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0859 | **Gate:** `proceed_with_warning`

**Expected answer:**
> The glossary states 'A customer can place multiple orders. Or is it accounts that place orders?' indicating uncertainty about the relationship. The ORDERS table has both customer_id and CustomerID columns with ambiguous FK references, and the data dictionary notes they reference 'customer (which tab…

**System answer:**
> Customers and orders are related through the ORDERS table’s customer reference columns. The business concept mapping for Order says physical table ORDERS includes CUSTOMER_ID and CUSTOMERID, and the Customer concept is implemented by CUSTOMERS with CUSTOMER_ID and CUSTOMERID.

So, at the schema level, an order belongs to a customer by linking ORDERS.CUSTOMER_ID or ORDERS.CUSTOMERID to CUSTOMERS.CU…

**Sources retrieved (12):** `parent_chunk_data_dictionary.txt_3`, `parent_chunk_data_dictionary.txt_2`, `Order→ORDERS`, `parent_chunk_data_dictionary.txt_1`, `Payment→PAYMENTS`, `Customer→CUSTOMERS`, `Order Items→ORDER_ITEMS`, `Inventory Item→PRODUCTS`

**Context previews (first 3):**

1. _========================================== PAYMENTS ==========================================  Primary Key: payment_id (unverified) | Column Name | Data Type | Constraints | Description | |----------…_

2. _Foreign Keys: - customer_id → CUSTOMERS(customer_id or CustomerID?) - [missing other FK definitions] ========================================== ORDER_ITEMS (or ORDER_DETAILS?) ========================…_

3. _Business concept 'Order' — The table clearly represents an order header with order identifiers, customer reference, order dates, statuses, payment fields, and monetary amounts. However, duplicate/conf…_

---

### ✅ ec_018 — Which price column represents what the customer actually pays?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0251 | **Gate:** `proceed_with_warning`

**Expected answer:**
> Multiple price columns exist across tables: ORDERS has orderAmount and total_amount; ORDER_ITEMS has unit_price and UnitPrice; PRODUCTS has unit_price, current_price, and cost_price. The data dictionary does not explain which represents the final customer price, whether discounts are applied, or how…

**System answer:**
> From the retrieved context alone, this cannot be determined definitively.

What is known is that several price-related columns exist, but the documentation does not define which one is the final customer-paid amount:

In ORDER_ITEMS, unit_price is explicitly described as “Price per unit.” The same table also has discount_percent, discount_amount, and line_total, which suggests the customer-paid li…

**Sources retrieved (12):** `Order→ORDERS`, `Payment→PAYMENTS`, `parent_chunk_data_dictionary.txt_2`, `parent_chunk_data_dictionary.txt_3`, `Order Items→ORDER_ITEMS`, `parent_chunk_data_dictionary.txt_1`, `Inventory Item→PRODUCTS`, `Order`

**Context previews (first 3):**

1. _Business concept 'Order' — The table clearly represents an order header with order identifiers, customer reference, order dates, statuses, payment fields, and monetary amounts. However, duplicate/conf…_

2. _Business concept 'Payment' — The table is explicitly named PAYMENTS and includes core payment attributes such as payment_date, payment_amount, payment_method, payment_status, and gateway response deta…_

3. _Foreign Keys: - customer_id → CUSTOMERS(customer_id or CustomerID?) - [missing other FK definitions] ========================================== ORDER_ITEMS (or ORDER_DETAILS?) ========================…_

---

### ✅ ec_019 — What's the difference between Shipment, Delivery, and Fulfillment?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0050 | **Gate:** `proceed_with_warning`

**Expected answer:**
> The glossary provides definitions but unclear boundaries: Shipment is 'The process of delivering goods to a customer'; Delivery is 'The completion of a Shipment when goods reach the customer'; Fulfillment is 'The process of preparing and delivering orders. Encompasses Shipment and Delivery.' The exa…

**System answer:**
> The retrieved context does not define Shipment, Delivery, or Fulfillment, so their differences cannot be determined from this knowledge graph.

What is known from the context is that it covers related order-processing metadata such as the business concept Order, implemented by ORDERS, line items in ORDER_ITEMS, payments in PAYMENTS, inventory items in PRODUCTS, and customer data in CUSTOMERS. The …

**Sources retrieved (12):** `Order→ORDERS`, `parent_chunk_data_dictionary.txt_2`, `parent_chunk_data_dictionary.txt_3`, `Payment→PAYMENTS`, `Inventory Item→PRODUCTS`, `Order Items→ORDER_ITEMS`, `parent_chunk_business_glossary.txt_0`, `Order`

**Context previews (first 3):**

1. _Business concept 'Order' — The table clearly represents an order header with order identifiers, customer reference, order dates, statuses, payment fields, and monetary amounts. However, duplicate/conf…_

2. _Foreign Keys: - customer_id → CUSTOMERS(customer_id or CustomerID?) - [missing other FK definitions] ========================================== ORDER_ITEMS (or ORDER_DETAILS?) ========================…_

3. _========================================== PAYMENTS ==========================================  Primary Key: payment_id (unverified) | Column Name | Data Type | Constraints | Description | |----------…_

---

### ✅ ec_020 — Are foreign key constraints enforced in the schema?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.1603 | **Gate:** `proceed_with_warning`

**Expected answer:**
> No foreign key constraints are enforced in the DDL. While the data dictionary documents FK relationships (e.g., customer_id → CUSTOMERS, order_id → ORDERS), the actual CREATE TABLE statements omit the REFERENCES clauses. The schema explicitly notes 'FK constraints defined in data dictionary but not …

**System answer:**
> The retrieved context does not confirm that foreign key constraints are actually enforced in the schema.

It only shows schema documentation that marks some columns as foreign keys or intended references, for example PAYMENTS.order_id → ORDERS, PAYMENTS.customer_id → CUSTOMERS, and ORDER_ITEMS.order_id → ORDERS. ORDER_ITEMS.product_id is also described as referencing PRODUCTS, with uncertainty not…

**Sources retrieved (12):** `parent_chunk_data_dictionary.txt_2`, `Payment→PAYMENTS`, `parent_chunk_data_dictionary.txt_3`, `parent_chunk_data_dictionary.txt_1`, `Order→ORDERS`, `Order Items→ORDER_ITEMS`, `Payment`, `Order`

**Context previews (first 3):**

1. _Foreign Keys: - customer_id → CUSTOMERS(customer_id or CustomerID?) - [missing other FK definitions] ========================================== ORDER_ITEMS (or ORDER_DETAILS?) ========================…_

2. _Business concept 'Payment' — The table is explicitly named PAYMENTS and includes core payment attributes such as payment_date, payment_amount, payment_method, payment_status, and gateway response deta…_

3. _========================================== PAYMENTS ==========================================  Primary Key: payment_id (unverified) | Column Name | Data Type | Constraints | Description | |----------…_

---

## Anomalies & Observations

No anomalies detected. All questions grounded with acceptable RAGAS scores.
