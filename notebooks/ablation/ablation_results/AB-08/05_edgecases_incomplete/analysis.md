# AB-08 — 05_edgecases_incomplete — Run Analysis

**Timestamp:** 2026-03-31 19:32:38  
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
| Chunk size / overlap | `512 / 64` |
| ER similarity threshold | `0.75` |

## Builder Results

| Metric | Value |
|--------|-------|
| Triplets extracted | 192 |
| Entities resolved | 77 |
| Tables parsed | 5 |
| Tables completed | 5 |

## Query Evaluation Summary

| Metric | Value |
|--------|-------|
| Questions | 20 |
| Grounded | **20/20 (100%)** |
| Avg GT Coverage | 100% |
| Avg Top Score | 0.4826 |
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
> In the business glossary, Customer is defined only partially as “An individual or organization that...” and the definition is marked incomplete.

Related glossary terms give additional context: “Client” is “a person or company that purchases goods or services” and may be used interchangeably with Customer in some contexts. “Account Holder” is the primary owner of an account and is similar to Custo…

**Sources retrieved (12):** `parent_chunk_data_dictionary.txt_1`, `Multiple FK references (order_id, customer_id) - unclear relationship→CUSTOMERS`, `parent_chunk_data_dictionary.txt_2`, `Sales Order→ORDERS`, `parent_chunk_data_dictionary.txt_3`, `payment_method→PAYMENTS`, `Multiple FK references (order_id, customer_id) - unclear relationship`, `parent_chunk_business_glossary.txt_0`

**Context previews (first 3):**

1. _DATA DICTIONARY - Enterprise Database Version: 2.1 (incomplete documentation) Last Updated: 2024-02-28 ========================================== CUSTOMERS ========================================== P…_

2. _Business concept 'Multiple FK references (order_id, customer_id) - unclear relationship' is implemented by physical table CUSTOMERS (columns: customer_id, CustomerID, firstName, first_name, lastName, …_

3. _Foreign Keys: - customer_id → CUSTOMERS(customer_id or CustomerID?) - [missing other FK definitions] ========================================== ORDER_ITEMS (or ORDER_DETAILS?) ========================…_

---

### ✅ ec_002 — What's the difference between firstName and first_name in the CUSTOMERS table?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.4652 | **Gate:** `proceed`

**Expected answer:**
> Both columns exist in the CUSTOMERS table with identical VARCHAR(50) data types. The data dictionary notes they appear to be duplicates resulting from inconsistent naming conventions (snake_case vs camelCase), but the actual usage by the application is not documented.

**System answer:**
> Based on the retrieved context, there is no documented business difference between `firstName` and `first_name` in `CUSTOMERS`.

The data dictionary shows both columns as `VARCHAR(50)`. `firstName` is described as "Customer's first name," while `first_name` is explicitly noted as "[appears to be duplicate]." The documentation is incomplete, and constraints for both are unknown, so the context sugg…

**Sources retrieved (12):** `Multiple FK references (order_id, customer_id) - unclear relationship→CUSTOMERS`, `parent_chunk_data_dictionary.txt_1`, `parent_chunk_data_dictionary.txt_2`, `Sales Order→ORDERS`, `parent_chunk_data_dictionary.txt_3`, `Order Items→ORDER_ITEMS`, `Order Items`, `Sales Order`

**Context previews (first 3):**

1. _Business concept 'Multiple FK references (order_id, customer_id) - unclear relationship' is implemented by physical table CUSTOMERS (columns: customer_id, CustomerID, firstName, first_name, lastName, …_

2. _DATA DICTIONARY - Enterprise Database Version: 2.1 (incomplete documentation) Last Updated: 2024-02-28 ========================================== CUSTOMERS ========================================== P…_

3. _Foreign Keys: - customer_id → CUSTOMERS(customer_id or CustomerID?) - [missing other FK definitions] ========================================== ORDER_ITEMS (or ORDER_DETAILS?) ========================…_

---

### ✅ ec_003 — Which customer column should be used as a foreign key reference: customer_id or CustomerID?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.9258 | **Gate:** `proceed`

**Expected answer:**
> The CUSTOMERS table has both customer_id (defined as PRIMARY KEY) and CustomerID (defined as INTEGER with no constraints). The ORDERS table also has both customer_id and CustomerID columns with ambiguous FK references. The data dictionary indicates this inconsistency is documented but not yet resolv…

**System answer:**
> The retrieved context does not definitively resolve this. In CUSTOMERS, customer_id is marked as the primary key, while CustomerID is described as a possible duplicate and the dictionary explicitly says “customer_id (or is it CustomerID? check with DBA).”

So, based strictly on the available context, customer_id is the stronger foreign key reference candidate, because it is the only column explici…

**Sources retrieved (12):** `parent_chunk_data_dictionary.txt_2`, `Multiple FK references (order_id, customer_id) - unclear relationship→CUSTOMERS`, `parent_chunk_data_dictionary.txt_1`, `parent_chunk_data_dictionary.txt_3`, `Sales Order→ORDERS`, `Multiple FK references (order_id, customer_id) - unclear relationship`, `payment_method→PAYMENTS`, `Order Items→ORDER_ITEMS`

**Context previews (first 3):**

1. _Foreign Keys: - customer_id → CUSTOMERS(customer_id or CustomerID?) - [missing other FK definitions] ========================================== ORDER_ITEMS (or ORDER_DETAILS?) ========================…_

2. _Business concept 'Multiple FK references (order_id, customer_id) - unclear relationship' is implemented by physical table CUSTOMERS (columns: customer_id, CustomerID, firstName, first_name, lastName, …_

3. _DATA DICTIONARY - Enterprise Database Version: 2.1 (incomplete documentation) Last Updated: 2024-02-28 ========================================== CUSTOMERS ========================================== P…_

---

### ✅ ec_004 — What are the valid values for order_status?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.3951 | **Gate:** `proceed`

**Expected answer:**
> The business glossary documents several order statuses: Pending, Processing, Completed, Cancelled, On Hold, and Failed (which is marked as [definition missing]). However, these are not enforced by a CHECK constraint in the schema, and the data dictionary notes that valid values reference '[missing d…

**System answer:**
> The retrieved context does not provide the valid values for `order_status`.

What it does show is that `order_status` is a column in the `ORDERS` table, which implements the business concept `Sales Order`. That table contains order header information such as `order_id`, `customer_id`, order dates, pricing totals, `payment_status`, and `payment_method`. The business glossary also says an `Order` is…

**Sources retrieved (12):** `parent_chunk_data_dictionary.txt_3`, `Sales Order→ORDERS`, `parent_chunk_data_dictionary.txt_1`, `parent_chunk_data_dictionary.txt_2`, `parent_chunk_business_glossary.txt_0`, `Multiple FK references (order_id, customer_id) - unclear relationship→CUSTOMERS`, `payment_method→PAYMENTS`, `Order Items`

**Context previews (first 3):**

1. _========================================== PAYMENTS ==========================================  Primary Key: payment_id (unverified) | Column Name | Data Type | Constraints | Description | |----------…_

2. _Business concept 'Sales Order' — The table centers on an order header with order/customer identifiers, order dates, status, and pricing totals, which aligns best with a sales order rather than line it…_

3. _DATA DICTIONARY - Enterprise Database Version: 2.1 (incomplete documentation) Last Updated: 2024-02-28 ========================================== CUSTOMERS ========================================== P…_

---

### ✅ ec_005 — Is there a difference between Product, Item, and SKU?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.5696 | **Gate:** `proceed`

**Expected answer:**
> The glossary indicates these terms are related but distinct: Product is defined as "A thing that is... [definition needs clarification]"; Item is a synonym for Product used in inventory context; SKU (Stock Keeping Unit) is a unique identifier for a product variant; Inventory Item refers to physical …

**System answer:**
> From the retrieved context, there is a partial distinction, but it is not fully defined in business terms.

“Product” is represented by the PRODUCTS table. That table contains product-level attributes such as product_id, product_name, product_category, unit_price/current_price, cost_price, stock_quantity, reorder_level, is_active, and also product_sku / sku. This suggests that a Product is the mas…

**Sources retrieved (12):** `PRODUCTS (or INVENTORY?)→PRODUCTS`, `parent_chunk_data_dictionary.txt_2`, `Order Items`, `Order Items→ORDER_ITEMS`, `parent_chunk_data_dictionary.txt_1`, `Sales Order→ORDERS`, `parent_chunk_data_dictionary.txt_3`, `parent_chunk_business_glossary.txt_0`

**Context previews (first 3):**

1. _Business concept 'PRODUCTS (or INVENTORY?)' is implemented by physical table PRODUCTS (columns: product_id, ProductID, product_name, ProductName, product_sku, sku, product_category, category, unit_pri…_

2. _Foreign Keys: - customer_id → CUSTOMERS(customer_id or CustomerID?) - [missing other FK definitions] ========================================== ORDER_ITEMS (or ORDER_DETAILS?) ========================…_

3. _Order Items: The table is explicitly named ORDER_ITEMS and contains line-level attributes such as order_id, product_id, quantity, unit_price, discounts, and line_total, which match an order detail/ite…_

---

### ✅ ec_006 — Which table should ORDER_ITEMS.product_id reference: PRODUCTS or INVENTORY?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.9610 | **Gate:** `proceed`

**Expected answer:**
> The data dictionary states the FK reference is to 'PRODUCTS (or INVENTORY?)' and notes it is 'not verified'. The schema provides two potential targets: PRODUCTS table (which has product_id) and an INVENTORY table that is referenced in documentation but not defined in the DDL. The actual relationship…

**System answer:**
> Based on the retrieved context, ORDER_ITEMS.product_id should reference PRODUCTS.

The strongest evidence is that the ORDER_ITEMS schema explicitly says product_id “References PRODUCTS (or INVENTORY?)”, and the only physical table actually mapped for that product/inventory concept is PRODUCTS. The context shows the business concept “PRODUCTS (or INVENTORY?)” is implemented by physical table PRODUC…

**Sources retrieved (12):** `PRODUCTS (or INVENTORY?)→PRODUCTS`, `parent_chunk_data_dictionary.txt_2`, `Order Items`, `Order Items→ORDER_ITEMS`, `Multiple FK references (order_id, customer_id) - unclear relationship→CUSTOMERS`, `Multiple FK references (order_id, customer_id) - unclear relationship`, `parent_chunk_data_dictionary.txt_3`, `PRODUCTS (or INVENTORY?)`

**Context previews (first 3):**

1. _Business concept 'PRODUCTS (or INVENTORY?)' is implemented by physical table PRODUCTS (columns: product_id, ProductID, product_name, ProductName, product_sku, sku, product_category, category, unit_pri…_

2. _Foreign Keys: - customer_id → CUSTOMERS(customer_id or CustomerID?) - [missing other FK definitions] ========================================== ORDER_ITEMS (or ORDER_DETAILS?) ========================…_

3. _Order Items: The table is explicitly named ORDER_ITEMS and contains line-level attributes such as order_id, product_id, quantity, unit_price, discounts, and line_total, which match an order detail/ite…_

---

### ✅ ec_007 — What's the difference between Revenue and Sales?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.4224 | **Gate:** `proceed`

**Expected answer:**
> Both terms show circular definitions: Revenue is defined as 'Income from sales. The same as... [definition circular, see Sales]', while Sales is defined as 'Revenue from selling products. See Revenue.' The glossary provides no clear distinction between these concepts.

**System answer:**
> The retrieved context does not define Revenue, and it also does not define Sales as a standalone business term, so I cannot state the difference between Revenue and Sales from this knowledge graph.

What the context does contain is sales-related schema metadata. It defines Order in the business glossary as “a request to purchase products or services” that “can be in various states,” and Transactio…

**Sources retrieved (12):** `Sales Order→ORDERS`, `parent_chunk_data_dictionary.txt_2`, `Order Items→ORDER_ITEMS`, `parent_chunk_data_dictionary.txt_3`, `Order Items`, `parent_chunk_business_glossary.txt_0`, `Sales Order`, `parent_chunk_data_dictionary.txt_1`

**Context previews (first 3):**

1. _Business concept 'Sales Order' — The table centers on an order header with order/customer identifiers, order dates, status, and pricing totals, which aligns best with a sales order rather than line it…_

2. _Foreign Keys: - customer_id → CUSTOMERS(customer_id or CustomerID?) - [missing other FK definitions] ========================================== ORDER_ITEMS (or ORDER_DETAILS?) ========================…_

3. _Business concept 'Order Items' — The table is explicitly named ORDER_ITEMS and contains line-level attributes such as order_id, product_id, quantity, unit_price, discounts, and line_total, which match…_

---

### ✅ ec_008 — Can one order have multiple payments?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0981 | **Gate:** `proceed_with_warning`

**Expected answer:**
> The PAYMENTS table has an order_id column, suggesting a many-to-one relationship (multiple payments can reference a single order). However, the relationship section in the glossary asks 'Or is it one-to-one?' indicating uncertainty. The ORDERS table has both payment_status and payment_method columns…

**System answer:**
> Based on the schema metadata, it appears that one order can have multiple payments.

The evidence is that PAYMENTS has its own primary key, payment_id, and a separate foreign key, order_id, that references ORDERS. That structure means multiple PAYMENTS rows could point to the same ORDERS.order_id unless a unique constraint existed on PAYMENTS.order_id, and no such unique constraint is documented i…

**Sources retrieved (12):** `parent_chunk_data_dictionary.txt_3`, `Sales Order→ORDERS`, `Multiple FK references (order_id, customer_id) - unclear relationship→CUSTOMERS`, `payment_method→PAYMENTS`, `Multiple FK references (order_id, customer_id) - unclear relationship`, `parent_chunk_data_dictionary.txt_2`, `parent_chunk_data_dictionary.txt_1`, `Order Items→ORDER_ITEMS`

**Context previews (first 3):**

1. _========================================== PAYMENTS ==========================================  Primary Key: payment_id (unverified) | Column Name | Data Type | Constraints | Description | |----------…_

2. _Business concept 'Sales Order' — The table centers on an order header with order/customer identifiers, order dates, status, and pricing totals, which aligns best with a sales order rather than line it…_

3. _Business concept 'Multiple FK references (order_id, customer_id) - unclear relationship' is implemented by physical table CUSTOMERS (columns: customer_id, CustomerID, firstName, first_name, lastName, …_

---

### ✅ ec_009 — What payment methods are accepted?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.1791 | **Gate:** `proceed_with_warning`

**Expected answer:**
> The PAYMENTS table has a payment_method column (VARCHAR(30)), but the data dictionary notes '[missing valid values]' and no CHECK constraint exists to enumerate acceptable methods. The schema does not document what values are valid (e.g., credit_card, debit, paypal, etc.).

**System answer:**
> The retrieved context shows that payment method is tracked, but it does not document which payment methods are accepted.

Specifically, the business concept payment_method is implemented in the PAYMENTS table, which includes the column payment_method as VARCHAR(30), and its description explicitly says the valid values are missing. The PAYMENTS table also stores related payment attributes such as p…

**Sources retrieved (12):** `parent_chunk_data_dictionary.txt_3`, `payment_method→PAYMENTS`, `Sales Order→ORDERS`, `parent_chunk_data_dictionary.txt_1`, `parent_chunk_data_dictionary.txt_2`, `parent_chunk_business_glossary.txt_0`, `Sales Order`, `Multiple FK references (order_id, customer_id) - unclear relationship→CUSTOMERS`

**Context previews (first 3):**

1. _========================================== PAYMENTS ==========================================  Primary Key: payment_id (unverified) | Column Name | Data Type | Constraints | Description | |----------…_

2. _Business concept 'payment_method' is implemented by physical table PAYMENTS (columns: payment_id, PaymentID, order_id, customer_id, payment_date, payment_amount, payment_method, payment_status, transa…_

3. _Business concept 'Sales Order' — The table centers on an order header with order/customer identifiers, order dates, status, and pricing totals, which aligns best with a sales order rather than line it…_

---

### ✅ ec_010 — What's the correct table name: ORDER_ITEMS or ORDER_DETAILS?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.9958 | **Gate:** `proceed`

**Expected answer:**
> The DDL creates a table named ORDER_ITEMS, but the data dictionary header shows 'ORDER_ITEMS (or ORDER_DETAILS?)' and notes 'Table name ambiguity: ORDER_ITEMS vs ORDER_DETAILS'. The actual table name in the schema is ORDER_ITEMS, but documentation suggests the application may reference it differentl…

**System answer:**
> Based on the retrieved context, the correct table name is ORDER_ITEMS.

The strongest evidence is that the business concept "Order Items" is described as "explicitly named ORDER_ITEMS," and the concept-to-table mapping says it is implemented by physical table ORDER_ITEMS. One schema fragment shows a heading "ORDER_ITEMS (or ORDER_DETAILS?)", but that same fragment is marked as incomplete/undocumen…

**Sources retrieved (12):** `Order Items`, `Order Items→ORDER_ITEMS`, `parent_chunk_data_dictionary.txt_2`, `PRODUCTS (or INVENTORY?)→PRODUCTS`, `parent_chunk_data_dictionary.txt_3`, `Multiple FK references (order_id, customer_id) - unclear relationship→CUSTOMERS`, `parent_chunk_data_dictionary.txt_1`, `Sales Order→ORDERS`

**Context previews (first 3):**

1. _Order Items: The table is explicitly named ORDER_ITEMS and contains line-level attributes such as order_id, product_id, quantity, unit_price, discounts, and line_total, which match an order detail/ite…_

2. _Business concept 'Order Items' — The table is explicitly named ORDER_ITEMS and contains line-level attributes such as order_id, product_id, quantity, unit_price, discounts, and line_total, which match…_

3. _Foreign Keys: - customer_id → CUSTOMERS(customer_id or CustomerID?) - [missing other FK definitions] ========================================== ORDER_ITEMS (or ORDER_DETAILS?) ========================…_

---

### ✅ ec_011 — Which date column should be used to track when an order was created: order_date, OrderDate, or created_at?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.8621 | **Gate:** `proceed`

**Expected answer:**
> The ORDERS table has three date-related columns: order_date (DATE type), OrderDate (DATETIME type with different precision), and created_at (TIMESTAMP type). The data dictionary provides no guidance on which is actually used by the application or why three columns exist for potentially the same purp…

**System answer:**
> The retrieved context does not explicitly identify a single authoritative “order created” column for ORDERS.

From the context, ORDERS contains all three: order_date, OrderDate, and created_at. The Sales Order description says the table includes “order dates,” which supports order_date/OrderDate as order-related dates, and the table also has created_at as a separate timestamp-style column. The bro…

**Sources retrieved (12):** `Sales Order→ORDERS`, `Multiple FK references (order_id, customer_id) - unclear relationship→CUSTOMERS`, `payment_method→PAYMENTS`, `parent_chunk_data_dictionary.txt_1`, `parent_chunk_data_dictionary.txt_3`, `PRODUCTS (or INVENTORY?)→PRODUCTS`, `parent_chunk_data_dictionary.txt_2`, `Order Items→ORDER_ITEMS`

**Context previews (first 3):**

1. _Business concept 'Sales Order' — The table centers on an order header with order/customer identifiers, order dates, status, and pricing totals, which aligns best with a sales order rather than line it…_

2. _Business concept 'Multiple FK references (order_id, customer_id) - unclear relationship' is implemented by physical table CUSTOMERS (columns: customer_id, CustomerID, firstName, first_name, lastName, …_

3. _Business concept 'payment_method' is implemented by physical table PAYMENTS (columns: payment_id, PaymentID, order_id, customer_id, payment_date, payment_amount, payment_method, payment_status, transa…_

---

### ✅ ec_012 — What does the Failed order status mean?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0031 | **Gate:** `proceed_with_warning`

**Expected answer:**
> The business glossary lists Failed as an order status but marks it as '[definition missing]'. Other statuses have definitions (Pending, Processing, Completed, Cancelled, On Hold), but Failed is undefined despite being a valid status value.

**System answer:**
> The retrieved context does not document a specific order status value called "Failed" or define its meaning.

What the context does show is that the ORDERS table for the Sales Order concept includes an order_status column, and the glossary says an Order "can be in various states." However, no retrieved chunk lists the allowed order_status values or explains what "Failed" would mean. The context al…

**Sources retrieved (12):** `Sales Order→ORDERS`, `parent_chunk_data_dictionary.txt_3`, `parent_chunk_data_dictionary.txt_1`, `parent_chunk_data_dictionary.txt_2`, `Multiple FK references (order_id, customer_id) - unclear relationship→CUSTOMERS`, `Order Items→ORDER_ITEMS`, `Order Items`, `payment_method→PAYMENTS`

**Context previews (first 3):**

1. _Business concept 'Sales Order' — The table centers on an order header with order/customer identifiers, order dates, status, and pricing totals, which aligns best with a sales order rather than line it…_

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

The schema excerpts for CUSTOMERS, PAYMENTS, ORDER_ITEMS, and the ORDERS/PRODUCTS concept-to-table mappings show constraints such as PK, FK, and a possible UNIQUE on PAYMENTS.transaction_id, but none of the provided columns are marked NOT NULL. The documentation is also noted as incomplete, so the context does not confirm whet…

**Sources retrieved (12):** `parent_chunk_data_dictionary.txt_3`, `parent_chunk_data_dictionary.txt_2`, `parent_chunk_data_dictionary.txt_1`, `Sales Order→ORDERS`, `parent_chunk_business_glossary.txt_0`, `Order Items`, `PRODUCTS (or INVENTORY?)→PRODUCTS`, `Multiple FK references (order_id, customer_id) - unclear relationship→CUSTOMERS`

**Context previews (first 3):**

1. _========================================== PAYMENTS ==========================================  Primary Key: payment_id (unverified) | Column Name | Data Type | Constraints | Description | |----------…_

2. _Foreign Keys: - customer_id → CUSTOMERS(customer_id or CustomerID?) - [missing other FK definitions] ========================================== ORDER_ITEMS (or ORDER_DETAILS?) ========================…_

3. _DATA DICTIONARY - Enterprise Database Version: 2.1 (incomplete documentation) Last Updated: 2024-02-28 ========================================== CUSTOMERS ========================================== P…_

---

### ✅ ec_014 — What's the difference between unit_price and current_price in PRODUCTS?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.6065 | **Gate:** `proceed`

**Expected answer:**
> The PRODUCTS table has both unit_price and current_price columns (both DECIMAL(10,2)). The data dictionary asks 'Different from unit_price?' but provides no explanation of the distinction or when each would be used.

**System answer:**
> From the retrieved context, the PRODUCTS table includes both unit_price and current_price as separate columns, but the knowledge graph does not define the difference between them.

What can be stated from the context is this: the business concept “PRODUCTS (or INVENTORY?)” is implemented by physical table PRODUCTS, and that table contains product_id/ProductID, product_name/ProductName, product_sku…

**Sources retrieved (12):** `PRODUCTS (or INVENTORY?)→PRODUCTS`, `parent_chunk_data_dictionary.txt_2`, `Order Items→ORDER_ITEMS`, `Order Items`, `Sales Order→ORDERS`, `parent_chunk_data_dictionary.txt_3`, `parent_chunk_business_glossary.txt_0`, `PRODUCTS (or INVENTORY?)`

**Context previews (first 3):**

1. _Business concept 'PRODUCTS (or INVENTORY?)' is implemented by physical table PRODUCTS (columns: product_id, ProductID, product_name, ProductName, product_sku, sku, product_category, category, unit_pri…_

2. _Foreign Keys: - customer_id → CUSTOMERS(customer_id or CustomerID?) - [missing other FK definitions] ========================================== ORDER_ITEMS (or ORDER_DETAILS?) ========================…_

3. _Business concept 'Order Items' — The table is explicitly named ORDER_ITEMS and contains line-level attributes such as order_id, product_id, quantity, unit_price, discounts, and line_total, which match…_

---

### ✅ ec_015 — When is an invoice generated vs payment processed?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.6598 | **Gate:** `proceed`

**Expected answer:**
> The relationship section in the glossary asks 'An invoice is generated for an order. But when? And can one order have multiple invoices?' indicating the timing and cardinality are not defined. The glossary defines Invoice as 'A document requesting payment. Related to Bill' and Payment as 'The transf…

**System answer:**
> The retrieved context does not define any invoice concept, invoice table, or business rule for when an invoice is generated, so that part cannot be answered from the knowledge graph.

For payment processing, the context does show how it is modeled, but not the rule for exactly when processing occurs in the business lifecycle. Payment processing is represented primarily by the PAYMENTS table, which…

**Sources retrieved (12):** `parent_chunk_data_dictionary.txt_3`, `Sales Order→ORDERS`, `parent_chunk_data_dictionary.txt_1`, `parent_chunk_data_dictionary.txt_2`, `payment_method→PAYMENTS`, `parent_chunk_business_glossary.txt_0`, `Sales Order`, `Order Items→ORDER_ITEMS`

**Context previews (first 3):**

1. _========================================== PAYMENTS ==========================================  Primary Key: payment_id (unverified) | Column Name | Data Type | Constraints | Description | |----------…_

2. _Business concept 'Sales Order' — The table centers on an order header with order/customer identifiers, order dates, status, and pricing totals, which aligns best with a sales order rather than line it…_

3. _DATA DICTIONARY - Enterprise Database Version: 2.1 (incomplete documentation) Last Updated: 2024-02-28 ========================================== CUSTOMERS ========================================== P…_

---

### ✅ ec_016 — Is the sku column in PRODUCTS unique?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.5549 | **Gate:** `proceed`

**Expected answer:**
> The PRODUCTS table has both product_sku and sku columns. The data dictionary notes sku 'should be UNIQUE?' but the DDL does not define a UNIQUE constraint on either column. No index is documented for these columns.

**System answer:**
> The retrieved context does not state that `sku` in `PRODUCTS` is unique, so I cannot confirm uniqueness.

What the context does show is that the `PRODUCTS` table includes both `product_sku` and `sku` columns as part of the business concept mapped to `PRODUCTS`, but no constraint information such as `UNIQUE` is provided for either column.

**Sources retrieved (12):** `PRODUCTS (or INVENTORY?)→PRODUCTS`, `parent_chunk_data_dictionary.txt_2`, `parent_chunk_data_dictionary.txt_3`, `Order Items`, `Order Items→ORDER_ITEMS`, `parent_chunk_data_dictionary.txt_1`, `Multiple FK references (order_id, customer_id) - unclear relationship→CUSTOMERS`, `Sales Order→ORDERS`

**Context previews (first 3):**

1. _Business concept 'PRODUCTS (or INVENTORY?)' is implemented by physical table PRODUCTS (columns: product_id, ProductID, product_name, ProductName, product_sku, sku, product_category, category, unit_pri…_

2. _Foreign Keys: - customer_id → CUSTOMERS(customer_id or CustomerID?) - [missing other FK definitions] ========================================== ORDER_ITEMS (or ORDER_DETAILS?) ========================…_

3. _========================================== PAYMENTS ==========================================  Primary Key: payment_id (unverified) | Column Name | Data Type | Constraints | Description | |----------…_

---

### ✅ ec_017 — What is the relationship between customers and orders?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0859 | **Gate:** `proceed_with_warning`

**Expected answer:**
> The glossary states 'A customer can place multiple orders. Or is it accounts that place orders?' indicating uncertainty about the relationship. The ORDERS table has both customer_id and CustomerID columns with ambiguous FK references, and the data dictionary notes they reference 'customer (which tab…

**System answer:**
> In the schema, customers and orders are related through the ORDERS table. The business concept “Sales Order” is implemented by physical table ORDERS, which includes customer_id and CustomerID alongside order identifiers and order details. The foreign key metadata states customer_id → CUSTOMERS(customer_id or CustomerID?), so an order is linked to a customer through that customer identifier.

Based…

**Sources retrieved (12):** `Multiple FK references (order_id, customer_id) - unclear relationship→CUSTOMERS`, `parent_chunk_data_dictionary.txt_3`, `Sales Order→ORDERS`, `parent_chunk_data_dictionary.txt_2`, `Multiple FK references (order_id, customer_id) - unclear relationship`, `parent_chunk_data_dictionary.txt_1`, `Order Items→ORDER_ITEMS`, `Order Items`

**Context previews (first 3):**

1. _Business concept 'Multiple FK references (order_id, customer_id) - unclear relationship' is implemented by physical table CUSTOMERS (columns: customer_id, CustomerID, firstName, first_name, lastName, …_

2. _========================================== PAYMENTS ==========================================  Primary Key: payment_id (unverified) | Column Name | Data Type | Constraints | Description | |----------…_

3. _Business concept 'Sales Order' — The table centers on an order header with order/customer identifiers, order dates, status, and pricing totals, which aligns best with a sales order rather than line it…_

---

### ✅ ec_018 — Which price column represents what the customer actually pays?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0682 | **Gate:** `proceed_with_warning`

**Expected answer:**
> Multiple price columns exist across tables: ORDERS has orderAmount and total_amount; ORDER_ITEMS has unit_price and UnitPrice; PRODUCTS has unit_price, current_price, and cost_price. The data dictionary does not explain which represents the final customer price, whether discounts are applied, or how…

**System answer:**
> The retrieved context does not identify a single canonical “price column” that is explicitly defined as “what the customer actually pays.”

What is known from the context is:

In PAYMENTS, there is a `payment_amount` column. That is the clearest amount tied to an actual payment record, but the context does not explicitly state whether it is always the final amount paid for the full order.

In ORDE…

**Sources retrieved (12):** `payment_method→PAYMENTS`, `Sales Order→ORDERS`, `parent_chunk_data_dictionary.txt_2`, `parent_chunk_data_dictionary.txt_3`, `PRODUCTS (or INVENTORY?)→PRODUCTS`, `Order Items→ORDER_ITEMS`, `parent_chunk_data_dictionary.txt_1`, `Multiple FK references (order_id, customer_id) - unclear relationship→CUSTOMERS`

**Context previews (first 3):**

1. _Business concept 'payment_method' is implemented by physical table PAYMENTS (columns: payment_id, PaymentID, order_id, customer_id, payment_date, payment_amount, payment_method, payment_status, transa…_

2. _Business concept 'Sales Order' — The table centers on an order header with order/customer identifiers, order dates, status, and pricing totals, which aligns best with a sales order rather than line it…_

3. _Foreign Keys: - customer_id → CUSTOMERS(customer_id or CustomerID?) - [missing other FK definitions] ========================================== ORDER_ITEMS (or ORDER_DETAILS?) ========================…_

---

### ✅ ec_019 — What's the difference between Shipment, Delivery, and Fulfillment?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0050 | **Gate:** `proceed_with_warning`

**Expected answer:**
> The glossary provides definitions but unclear boundaries: Shipment is 'The process of delivering goods to a customer'; Delivery is 'The completion of a Shipment when goods reach the customer'; Fulfillment is 'The process of preparing and delivering orders. Encompasses Shipment and Delivery.' The exa…

**System answer:**
> The retrieved context does not define Shipment, Delivery, or Fulfillment, so I cannot state the difference between them from this knowledge graph.

What the context does cover is Order-related concepts such as Order, Sales Order, Order Items, Transaction, and schema tables like ORDERS, ORDER_ITEMS, PAYMENTS, CUSTOMERS, and PRODUCTS. There are no glossary entries, business concept definitions, or t…

**Sources retrieved (12):** `Sales Order→ORDERS`, `parent_chunk_data_dictionary.txt_2`, `parent_chunk_data_dictionary.txt_3`, `Order Items→ORDER_ITEMS`, `Order Items`, `parent_chunk_business_glossary.txt_0`, `Sales Order`, `parent_chunk_data_dictionary.txt_1`

**Context previews (first 3):**

1. _Business concept 'Sales Order' — The table centers on an order header with order/customer identifiers, order dates, status, and pricing totals, which aligns best with a sales order rather than line it…_

2. _Foreign Keys: - customer_id → CUSTOMERS(customer_id or CustomerID?) - [missing other FK definitions] ========================================== ORDER_ITEMS (or ORDER_DETAILS?) ========================…_

3. _========================================== PAYMENTS ==========================================  Primary Key: payment_id (unverified) | Column Name | Data Type | Constraints | Description | |----------…_

---

### ✅ ec_020 — Are foreign key constraints enforced in the schema?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.1603 | **Gate:** `proceed_with_warning`

**Expected answer:**
> No foreign key constraints are enforced in the DDL. While the data dictionary documents FK relationships (e.g., customer_id → CUSTOMERS, order_id → ORDERS), the actual CREATE TABLE statements omit the REFERENCES clauses. The schema explicitly notes 'FK constraints defined in data dictionary but not …

**System answer:**
> The retrieved context does not establish that foreign key constraints are actually enforced in the schema.

What is known from the context is that the data dictionary/documentation labels several columns as foreign keys or intended references: in ORDER_ITEMS, order_id is marked as FK to ORDERS, and product_id/ProductID is marked as FK to PRODUCTS (with ambiguity noted as “PRODUCTS (or INVENTORY?)”…

**Sources retrieved (12):** `parent_chunk_data_dictionary.txt_2`, `parent_chunk_data_dictionary.txt_3`, `parent_chunk_data_dictionary.txt_1`, `parent_chunk_business_glossary.txt_0`, `Order Items`, `Multiple FK references (order_id, customer_id) - unclear relationship→CUSTOMERS`, `Multiple FK references (order_id, customer_id) - unclear relationship`, `Order Items→ORDER_ITEMS`

**Context previews (first 3):**

1. _Foreign Keys: - customer_id → CUSTOMERS(customer_id or CustomerID?) - [missing other FK definitions] ========================================== ORDER_ITEMS (or ORDER_DETAILS?) ========================…_

2. _========================================== PAYMENTS ==========================================  Primary Key: payment_id (unverified) | Column Name | Data Type | Constraints | Description | |----------…_

3. _DATA DICTIONARY - Enterprise Database Version: 2.1 (incomplete documentation) Last Updated: 2024-02-28 ========================================== CUSTOMERS ========================================== P…_

---

## Anomalies & Observations

No anomalies detected. All questions grounded with acceptable RAGAS scores.
