# AB-18 — 05_edgecases_incomplete — Run Analysis

**Timestamp:** 2026-04-01 20:45:51  
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
| Triplets extracted | 231 |
| Entities resolved | 99 |
| Tables parsed | 5 |
| Tables completed | 5 |

## Query Evaluation Summary

| Metric | Value |
|--------|-------|
| Questions | 20 |
| Grounded | **20/20 (100%)** |
| Avg GT Coverage | 100% |
| Avg Top Score | 0.4623 |
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
> In the business glossary, Customer is defined only partially as “An individual or organization that...” because the definition is incomplete in the retrieved context. The glossary also notes that Client is “a person or company that purchases goods or services” and may be used interchangeably with Customer in some contexts.

At the schema level, the customer concept is represented by the CUSTOMERS …

**Sources retrieved (11):** `parent_chunk_data_dictionary.txt_1`, `parent_chunk_data_dictionary.txt_2`, `Sales Order→ORDERS`, `parent_chunk_data_dictionary.txt_3`, `Payment gateway response→PAYMENTS`, `parent_chunk_business_glossary.txt_0`, `Sales Order`, `Order Item→ORDER_ITEMS`

**Context previews (first 3):**

1. _DATA DICTIONARY - Enterprise Database Version: 2.1 (incomplete documentation) Last Updated: 2024-02-28 ========================================== CUSTOMERS ========================================== P…_

2. _Foreign Keys: - customer_id → CUSTOMERS(customer_id or CustomerID?) - [missing other FK definitions] ========================================== ORDER_ITEMS (or ORDER_DETAILS?) ========================…_

3. _Business concept 'Sales Order' — The table contains core order header fields such as order_id, customer_id, order_date, order_status, amounts, and payment/shipping totals, which align strongly with a …_

---

### ✅ ec_002 — What's the difference between firstName and first_name in the CUSTOMERS table?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.3978 | **Gate:** `proceed`

**Expected answer:**
> Both columns exist in the CUSTOMERS table with identical VARCHAR(50) data types. The data dictionary notes they appear to be duplicates resulting from inconsistent naming conventions (snake_case vs camelCase), but the actual usage by the application is not documented.

**System answer:**
> Based on the retrieved context, there is no documented business difference between `firstName` and `first_name` in `CUSTOMERS`.

The data dictionary shows both as `VARCHAR(50)`. `firstName` is described as “Customer's first name,” while `first_name` is marked as “[appears to be duplicate].” This suggests they are likely duplicate or legacy/inconsistently named versions of the same attribute, but t…

**Sources retrieved (11):** `parent_chunk_data_dictionary.txt_1`, `parent_chunk_data_dictionary.txt_2`, `Sales Order→ORDERS`, `parent_chunk_data_dictionary.txt_3`, `Order Item→ORDER_ITEMS`, `parent_chunk_business_glossary.txt_0`, `Sales Order`, `Order Item`

**Context previews (first 3):**

1. _DATA DICTIONARY - Enterprise Database Version: 2.1 (incomplete documentation) Last Updated: 2024-02-28 ========================================== CUSTOMERS ========================================== P…_

2. _Foreign Keys: - customer_id → CUSTOMERS(customer_id or CustomerID?) - [missing other FK definitions] ========================================== ORDER_ITEMS (or ORDER_DETAILS?) ========================…_

3. _Business concept 'Sales Order' — The table contains core order header fields such as order_id, customer_id, order_date, order_status, amounts, and payment/shipping totals, which align strongly with a …_

---

### ✅ ec_003 — Which customer column should be used as a foreign key reference: customer_id or CustomerID?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.9258 | **Gate:** `proceed`

**Expected answer:**
> The CUSTOMERS table has both customer_id (defined as PRIMARY KEY) and CustomerID (defined as INTEGER with no constraints). The ORDERS table also has both customer_id and CustomerID columns with ambiguous FK references. The data dictionary indicates this inconsistency is documented but not yet resolv…

**System answer:**
> The retrieved context does not resolve this definitively. In `CUSTOMERS`, the primary key is documented as `customer_id (or is it CustomerID? check with DBA)`, so the data dictionary explicitly flags the ambiguity. The foreign key note also says `customer_id → CUSTOMERS(customer_id or CustomerID?)`, which again leaves the target column unresolved.

From the specific tables shown, `customer_id` is …

**Sources retrieved (11):** `parent_chunk_data_dictionary.txt_2`, `parent_chunk_data_dictionary.txt_1`, `parent_chunk_data_dictionary.txt_3`, `Sales Order→ORDERS`, `Payment gateway response→PAYMENTS`, `Order Item→ORDER_ITEMS`, `Inventory Item→PRODUCTS`, `Sales Order`

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
> The retrieved context does not provide the valid values for order_status.

It does show that order_status is a column in the ORDERS table, which implements the business concept Sales Order, and the glossary says an Order “can be in various states,” but no enumeration or allowed status list is documented in the provided context.

**Sources retrieved (11):** `parent_chunk_data_dictionary.txt_3`, `Sales Order→ORDERS`, `parent_chunk_data_dictionary.txt_1`, `parent_chunk_data_dictionary.txt_2`, `Sales Order`, `parent_chunk_business_glossary.txt_0`, `Payment gateway response→PAYMENTS`, `Order Item→ORDER_ITEMS`

**Context previews (first 3):**

1. _========================================== PAYMENTS ==========================================  Primary Key: payment_id (unverified) | Column Name | Data Type | Constraints | Description | |----------…_

2. _Business concept 'Sales Order' — The table contains core order header fields such as order_id, customer_id, order_date, order_status, amounts, and payment/shipping totals, which align strongly with a …_

3. _DATA DICTIONARY - Enterprise Database Version: 2.1 (incomplete documentation) Last Updated: 2024-02-28 ========================================== CUSTOMERS ========================================== P…_

---

### ✅ ec_005 — Is there a difference between Product, Item, and SKU?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.5696 | **Gate:** `proceed`

**Expected answer:**
> The glossary indicates these terms are related but distinct: Product is defined as "A thing that is... [definition needs clarification]"; Item is a synonym for Product used in inventory context; SKU (Stock Keeping Unit) is a unique identifier for a product variant; Inventory Item refers to physical …

**System answer:**
> From the retrieved context, there is a schema-level difference, but not a full glossary definition of all three terms.

“Item” is used in two different ways in the metadata. “Inventory Item” is implemented by the PRODUCTS table, so in that context an item appears to mean a product master/inventory record. The PRODUCTS table includes columns such as product_id, product_name, product_sku or sku, cat…

**Sources retrieved (11):** `Inventory Item→PRODUCTS`, `parent_chunk_data_dictionary.txt_2`, `Order Item→ORDER_ITEMS`, `parent_chunk_data_dictionary.txt_1`, `Sales Order→ORDERS`, `parent_chunk_data_dictionary.txt_3`, `parent_chunk_business_glossary.txt_0`, `Order Item`

**Context previews (first 3):**

1. _Business concept 'Inventory Item' is implemented by physical table PRODUCTS (columns: product_id, ProductID, product_name, ProductName, product_sku, sku, product_category, category, unit_price, curren…_

2. _Foreign Keys: - customer_id → CUSTOMERS(customer_id or CustomerID?) - [missing other FK definitions] ========================================== ORDER_ITEMS (or ORDER_DETAILS?) ========================…_

3. _Business concept 'Order Item' — The table is explicitly named ORDER_ITEMS and contains classic line-item attributes such as order_id, product_id, quantity, unit_price, discount, and line_total, which …_

---

### ✅ ec_006 — Which table should ORDER_ITEMS.product_id reference: PRODUCTS or INVENTORY?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.9608 | **Gate:** `proceed`

**Expected answer:**
> The data dictionary states the FK reference is to 'PRODUCTS (or INVENTORY?)' and notes it is 'not verified'. The schema provides two potential targets: PRODUCTS table (which has product_id) and an INVENTORY table that is referenced in documentation but not defined in the DDL. The actual relationship…

**System answer:**
> Based on the retrieved context, ORDER_ITEMS.product_id should reference PRODUCTS.

The strongest support is:
The ORDER_ITEMS definition says product_id is an FK that references “PRODUCTS (or INVENTORY?)”, so the documentation itself is uncertain.
The business concept mapping for Inventory Item explicitly says the physical table is PRODUCTS, not INVENTORY.
The Order Item mapping also lists product_…

**Sources retrieved (11):** `parent_chunk_data_dictionary.txt_2`, `Inventory Item→PRODUCTS`, `Order Item→ORDER_ITEMS`, `parent_chunk_data_dictionary.txt_3`, `parent_chunk_data_dictionary.txt_1`, `Order Item`, `parent_chunk_business_glossary.txt_0`, `Sales Order→ORDERS`

**Context previews (first 3):**

1. _Foreign Keys: - customer_id → CUSTOMERS(customer_id or CustomerID?) - [missing other FK definitions] ========================================== ORDER_ITEMS (or ORDER_DETAILS?) ========================…_

2. _Business concept 'Inventory Item' is implemented by physical table PRODUCTS (columns: product_id, ProductID, product_name, ProductName, product_sku, sku, product_category, category, unit_price, curren…_

3. _Business concept 'Order Item' — The table is explicitly named ORDER_ITEMS and contains classic line-item attributes such as order_id, product_id, quantity, unit_price, discount, and line_total, which …_

---

### ✅ ec_007 — What's the difference between Revenue and Sales?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.4224 | **Gate:** `proceed`

**Expected answer:**
> Both terms show circular definitions: Revenue is defined as 'Income from sales. The same as... [definition circular, see Sales]', while Sales is defined as 'Revenue from selling products. See Revenue.' The glossary provides no clear distinction between these concepts.

**System answer:**
> The retrieved context does not define a business distinction between Revenue and Sales, so I cannot state their difference from this knowledge graph.

What the context does contain is sales-related schema and glossary evidence:

The only explicit sales-related concept is Sales Order. It is implemented by the ORDERS table, which contains order header fields including order_id, customer_id, order_da…

**Sources retrieved (11):** `Sales Order→ORDERS`, `parent_chunk_data_dictionary.txt_2`, `Order Item→ORDER_ITEMS`, `parent_chunk_data_dictionary.txt_3`, `parent_chunk_business_glossary.txt_0`, `Sales Order`, `Order Item`, `parent_chunk_data_dictionary.txt_1`

**Context previews (first 3):**

1. _Business concept 'Sales Order' — The table contains core order header fields such as order_id, customer_id, order_date, order_status, amounts, and payment/shipping totals, which align strongly with a …_

2. _Foreign Keys: - customer_id → CUSTOMERS(customer_id or CustomerID?) - [missing other FK definitions] ========================================== ORDER_ITEMS (or ORDER_DETAILS?) ========================…_

3. _Business concept 'Order Item' — The table is explicitly named ORDER_ITEMS and contains classic line-item attributes such as order_id, product_id, quantity, unit_price, discount, and line_total, which …_

---

### ✅ ec_008 — Can one order have multiple payments?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0981 | **Gate:** `proceed_with_warning`

**Expected answer:**
> The PAYMENTS table has an order_id column, suggesting a many-to-one relationship (multiple payments can reference a single order). However, the relationship section in the glossary asks 'Or is it one-to-one?' indicating uncertainty. The ORDERS table has both payment_status and payment_method columns…

**System answer:**
> Yes, based on the schema metadata, one order can have multiple payments.

The evidence is that PAYMENTS has its own primary key, payment_id, and includes order_id as a foreign key referencing ORDERS. That structure means PAYMENTS is modeled as a child table of ORDERS, with each payment row tied to an order through order_id. There is no indication in the retrieved context that order_id is unique in…

**Sources retrieved (11):** `parent_chunk_data_dictionary.txt_3`, `Sales Order→ORDERS`, `Payment gateway response→PAYMENTS`, `parent_chunk_data_dictionary.txt_2`, `parent_chunk_data_dictionary.txt_1`, `Order Item→ORDER_ITEMS`, `Inventory Item→PRODUCTS`, `parent_chunk_business_glossary.txt_0`

**Context previews (first 3):**

1. _========================================== PAYMENTS ==========================================  Primary Key: payment_id (unverified) | Column Name | Data Type | Constraints | Description | |----------…_

2. _Business concept 'Sales Order' — The table contains core order header fields such as order_id, customer_id, order_date, order_status, amounts, and payment/shipping totals, which align strongly with a …_

3. _Business concept 'Payment gateway response' is implemented by physical table PAYMENTS (columns: payment_id, PaymentID, order_id, customer_id, payment_date, payment_amount, payment_method, payment_stat…_

---

### ✅ ec_009 — What payment methods are accepted?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.1791 | **Gate:** `proceed_with_warning`

**Expected answer:**
> The PAYMENTS table has a payment_method column (VARCHAR(30)), but the data dictionary notes '[missing valid values]' and no CHECK constraint exists to enumerate acceptable methods. The schema does not document what values are valid (e.g., credit_card, debit, paypal, etc.).

**System answer:**
> The retrieved context does not specify which payment methods are accepted. It only shows that payment method is stored in two places: PAYMENTS.payment_method, which is a VARCHAR(30) with “[missing valid values],” and ORDERS.payment_method as an order header field in ORDERS. No allowed or accepted payment method values are documented in the retrieved context.

**Sources retrieved (11):** `parent_chunk_data_dictionary.txt_3`, `Sales Order→ORDERS`, `Payment gateway response→PAYMENTS`, `parent_chunk_data_dictionary.txt_1`, `parent_chunk_data_dictionary.txt_2`, `parent_chunk_business_glossary.txt_0`, `Payment gateway response`, `Sales Order`

**Context previews (first 3):**

1. _========================================== PAYMENTS ==========================================  Primary Key: payment_id (unverified) | Column Name | Data Type | Constraints | Description | |----------…_

2. _Business concept 'Sales Order' — The table contains core order header fields such as order_id, customer_id, order_date, order_status, amounts, and payment/shipping totals, which align strongly with a …_

3. _Business concept 'Payment gateway response' is implemented by physical table PAYMENTS (columns: payment_id, PaymentID, order_id, customer_id, payment_date, payment_amount, payment_method, payment_stat…_

---

### ✅ ec_010 — What's the correct table name: ORDER_ITEMS or ORDER_DETAILS?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.9982 | **Gate:** `proceed`

**Expected answer:**
> The DDL creates a table named ORDER_ITEMS, but the data dictionary header shows 'ORDER_ITEMS (or ORDER_DETAILS?)' and notes 'Table name ambiguity: ORDER_ITEMS vs ORDER_DETAILS'. The actual table name in the schema is ORDER_ITEMS, but documentation suggests the application may reference it differentl…

**System answer:**
> Based on the retrieved context, the correct table name is ORDER_ITEMS.

The strongest evidence is the business concept mapping, which explicitly says Business concept 'Order Item' is implemented by physical table ORDER_ITEMS, and it repeats that the table is explicitly named ORDER_ITEMS. ORDER_DETAILS appears only as an alternative in the concept family or as uncertainty in incomplete documentatio…

**Sources retrieved (11):** `Order Item→ORDER_ITEMS`, `parent_chunk_data_dictionary.txt_2`, `Inventory Item→PRODUCTS`, `parent_chunk_data_dictionary.txt_3`, `parent_chunk_data_dictionary.txt_1`, `Order Item`, `Sales Order→ORDERS`, `Payment gateway response→PAYMENTS`

**Context previews (first 3):**

1. _Business concept 'Order Item' — The table is explicitly named ORDER_ITEMS and contains classic line-item attributes such as order_id, product_id, quantity, unit_price, discount, and line_total, which …_

2. _Foreign Keys: - customer_id → CUSTOMERS(customer_id or CustomerID?) - [missing other FK definitions] ========================================== ORDER_ITEMS (or ORDER_DETAILS?) ========================…_

3. _Business concept 'Inventory Item' is implemented by physical table PRODUCTS (columns: product_id, ProductID, product_name, ProductName, product_sku, sku, product_category, category, unit_price, curren…_

---

### ✅ ec_011 — Which date column should be used to track when an order was created: order_date, OrderDate, or created_at?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.8238 | **Gate:** `proceed`

**Expected answer:**
> The ORDERS table has three date-related columns: order_date (DATE type), OrderDate (DATETIME type with different precision), and created_at (TIMESTAMP type). The data dictionary provides no guidance on which is actually used by the application or why three columns exist for potentially the same purp…

**System answer:**
> Based on the retrieved context, order_date is the best-supported column to use. In the ORDERS mapping for the business concept Sales Order, order_date is explicitly identified as one of the core order header fields.

The context also shows OrderDate and created_at as columns in ORDERS, but it does not define either of them. Because the documentation is incomplete and the table contains duplicate l…

**Sources retrieved (11):** `Sales Order→ORDERS`, `Payment gateway response→PAYMENTS`, `parent_chunk_data_dictionary.txt_1`, `parent_chunk_data_dictionary.txt_3`, `Inventory Item→PRODUCTS`, `Order Item→ORDER_ITEMS`, `parent_chunk_data_dictionary.txt_2`, `Sales Order`

**Context previews (first 3):**

1. _Business concept 'Sales Order' — The table contains core order header fields such as order_id, customer_id, order_date, order_status, amounts, and payment/shipping totals, which align strongly with a …_

2. _Business concept 'Payment gateway response' is implemented by physical table PAYMENTS (columns: payment_id, PaymentID, order_id, customer_id, payment_date, payment_amount, payment_method, payment_stat…_

3. _DATA DICTIONARY - Enterprise Database Version: 2.1 (incomplete documentation) Last Updated: 2024-02-28 ========================================== CUSTOMERS ========================================== P…_

---

### ✅ ec_012 — What does the Failed order status mean?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0032 | **Gate:** `proceed_with_warning`

**Expected answer:**
> The business glossary lists Failed as an order status but marks it as '[definition missing]'. Other statuses have definitions (Pending, Processing, Completed, Cancelled, On Hold), but Failed is undefined despite being a valid status value.

**System answer:**
> I cannot determine the meaning of the specific order status "Failed" from the retrieved context.

What the context does show is that the business concept Sales Order is implemented by the ORDERS table, which includes an order_status column, and the glossary says an Order "can be in various states." However, no valid values or definitions for order_status are provided, and "Failed" is not defined a…

**Sources retrieved (11):** `Sales Order→ORDERS`, `parent_chunk_data_dictionary.txt_3`, `parent_chunk_data_dictionary.txt_1`, `parent_chunk_data_dictionary.txt_2`, `Order Item→ORDER_ITEMS`, `Payment gateway response→PAYMENTS`, `Inventory Item→PRODUCTS`, `parent_chunk_business_glossary.txt_0`

**Context previews (first 3):**

1. _Business concept 'Sales Order' — The table contains core order header fields such as order_id, customer_id, order_date, order_status, amounts, and payment/shipping totals, which align strongly with a …_

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

Across the shown schema fragments for CUSTOMERS, PAYMENTS, ORDER_ITEMS, and the ORDERS column listing, the documented constraints include PK, FK, and a possible UNIQUE on PAYMENTS.transaction_id, but none of the columns are explicitly marked NOT NULL. In many places the constraint field is just “?” or the documentation is note…

**Sources retrieved (11):** `parent_chunk_data_dictionary.txt_3`, `parent_chunk_data_dictionary.txt_2`, `parent_chunk_data_dictionary.txt_1`, `Sales Order→ORDERS`, `parent_chunk_business_glossary.txt_0`, `Inventory Item→PRODUCTS`, `Payment gateway response→PAYMENTS`, `Order Item→ORDER_ITEMS`

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
> The retrieved context shows that PRODUCTS, which implements the business concept Inventory Item, contains both unit_price and current_price, but it does not provide column-level definitions for either field in PRODUCTS. So the knowledge graph does not define the difference between PRODUCTS.unit_price and PRODUCTS.current_price.

The only related pricing definition in the context is ORDER_ITEMS.uni…

**Sources retrieved (11):** `Inventory Item→PRODUCTS`, `parent_chunk_data_dictionary.txt_2`, `Order Item→ORDER_ITEMS`, `Sales Order→ORDERS`, `parent_chunk_data_dictionary.txt_3`, `Order Item`, `parent_chunk_business_glossary.txt_0`, `Sales Order`

**Context previews (first 3):**

1. _Business concept 'Inventory Item' is implemented by physical table PRODUCTS (columns: product_id, ProductID, product_name, ProductName, product_sku, sku, product_category, category, unit_price, curren…_

2. _Foreign Keys: - customer_id → CUSTOMERS(customer_id or CustomerID?) - [missing other FK definitions] ========================================== ORDER_ITEMS (or ORDER_DETAILS?) ========================…_

3. _Business concept 'Order Item' — The table is explicitly named ORDER_ITEMS and contains classic line-item attributes such as order_id, product_id, quantity, unit_price, discount, and line_total, which …_

---

### ✅ ec_015 — When is an invoice generated vs payment processed?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.6598 | **Gate:** `proceed`

**Expected answer:**
> The relationship section in the glossary asks 'An invoice is generated for an order. But when? And can one order have multiple invoices?' indicating the timing and cardinality are not defined. The glossary defines Invoice as 'A document requesting payment. Related to Bill' and Payment as 'The transf…

**System answer:**
> The retrieved context does not define a business rule for when an invoice is generated, and it does not include any invoice table, invoice column, or invoice lifecycle concept.

What it does show is how payment processing is represented in the schema. Payment processing is captured by the PAYMENTS table, which implements the business concept Payment gateway response. PAYMENTS includes order_id as …

**Sources retrieved (11):** `Sales Order→ORDERS`, `parent_chunk_data_dictionary.txt_3`, `parent_chunk_data_dictionary.txt_1`, `parent_chunk_data_dictionary.txt_2`, `Payment gateway response→PAYMENTS`, `parent_chunk_business_glossary.txt_0`, `Sales Order`, `Payment gateway response`

**Context previews (first 3):**

1. _Business concept 'Sales Order' — The table contains core order header fields such as order_id, customer_id, order_date, order_status, amounts, and payment/shipping totals, which align strongly with a …_

2. _========================================== PAYMENTS ==========================================  Primary Key: payment_id (unverified) | Column Name | Data Type | Constraints | Description | |----------…_

3. _DATA DICTIONARY - Enterprise Database Version: 2.1 (incomplete documentation) Last Updated: 2024-02-28 ========================================== CUSTOMERS ========================================== P…_

---

### ✅ ec_016 — Is the sku column in PRODUCTS unique?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.3824 | **Gate:** `proceed`

**Expected answer:**
> The PRODUCTS table has both product_sku and sku columns. The data dictionary notes sku 'should be UNIQUE?' but the DDL does not define a UNIQUE constraint on either column. No index is documented for these columns.

**System answer:**
> The retrieved context shows that PRODUCTS includes product_sku and sku as columns under the business concept Inventory Item, but it does not provide any uniqueness constraint for either column. So based on the available context, it cannot be determined whether sku in PRODUCTS is unique.

**Sources retrieved (11):** `Inventory Item→PRODUCTS`, `parent_chunk_data_dictionary.txt_2`, `parent_chunk_data_dictionary.txt_3`, `parent_chunk_data_dictionary.txt_1`, `Order Item→ORDER_ITEMS`, `Sales Order→ORDERS`, `Payment gateway response→PAYMENTS`, `parent_chunk_business_glossary.txt_0`

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
> The relationship is at the order-header level in ORDERS. The business concept Sales Order is implemented by ORDERS, and that table includes customer_id and CustomerID along with order_id, order_date, and order_status. The CUSTOMERS table uses customer_id (or possibly CustomerID) as its primary key, so the schema indicates that an order is tied to a customer through ORDERS.customer_id / ORDERS.Cust…

**Sources retrieved (11):** `parent_chunk_data_dictionary.txt_3`, `parent_chunk_data_dictionary.txt_2`, `Sales Order→ORDERS`, `parent_chunk_data_dictionary.txt_1`, `Order Item→ORDER_ITEMS`, `parent_chunk_business_glossary.txt_0`, `Sales Order`, `Order Item`

**Context previews (first 3):**

1. _========================================== PAYMENTS ==========================================  Primary Key: payment_id (unverified) | Column Name | Data Type | Constraints | Description | |----------…_

2. _Foreign Keys: - customer_id → CUSTOMERS(customer_id or CustomerID?) - [missing other FK definitions] ========================================== ORDER_ITEMS (or ORDER_DETAILS?) ========================…_

3. _Business concept 'Sales Order' — The table contains core order header fields such as order_id, customer_id, order_date, order_status, amounts, and payment/shipping totals, which align strongly with a …_

---

### ✅ ec_018 — Which price column represents what the customer actually pays?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0581 | **Gate:** `proceed_with_warning`

**Expected answer:**
> Multiple price columns exist across tables: ORDERS has orderAmount and total_amount; ORDER_ITEMS has unit_price and UnitPrice; PRODUCTS has unit_price, current_price, and cost_price. The data dictionary does not explain which represents the final customer price, whether discounts are applied, or how…

**System answer:**
> The context does not explicitly define a single column as “what the customer actually pays,” but the closest schema-level answers are:

For an actual payment transaction, PAYMENTS.payment_amount is the amount paid.

For an order line, ORDER_ITEMS.line_total is the strongest match for what the customer pays for that line, because ORDER_ITEMS also contains quantity, unit_price, discount_percent, and…

**Sources retrieved (11):** `Payment gateway response→PAYMENTS`, `Sales Order→ORDERS`, `parent_chunk_data_dictionary.txt_2`, `parent_chunk_data_dictionary.txt_3`, `Order Item→ORDER_ITEMS`, `parent_chunk_data_dictionary.txt_1`, `Inventory Item→PRODUCTS`, `Sales Order`

**Context previews (first 3):**

1. _Business concept 'Payment gateway response' is implemented by physical table PAYMENTS (columns: payment_id, PaymentID, order_id, customer_id, payment_date, payment_amount, payment_method, payment_stat…_

2. _Business concept 'Sales Order' — The table contains core order header fields such as order_id, customer_id, order_date, order_status, amounts, and payment/shipping totals, which align strongly with a …_

3. _Foreign Keys: - customer_id → CUSTOMERS(customer_id or CustomerID?) - [missing other FK definitions] ========================================== ORDER_ITEMS (or ORDER_DETAILS?) ========================…_

---

### ✅ ec_019 — What's the difference between Shipment, Delivery, and Fulfillment?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0156 | **Gate:** `proceed_with_warning`

**Expected answer:**
> The glossary provides definitions but unclear boundaries: Shipment is 'The process of delivering goods to a customer'; Delivery is 'The completion of a Shipment when goods reach the customer'; Fulfillment is 'The process of preparing and delivering orders. Encompasses Shipment and Delivery.' The exa…

**System answer:**
> The retrieved context does not define Shipment, Delivery, or Fulfillment, so I cannot state the difference between them from the available information.

The only closely related information is that the business concept Sales Order is described as an order header record and is “clearly an order captured at the header level rather than shipment, invoice, or payment,” implemented by ORDERS. The gloss…

**Sources retrieved (11):** `Sales Order→ORDERS`, `parent_chunk_data_dictionary.txt_2`, `Order Item→ORDER_ITEMS`, `parent_chunk_data_dictionary.txt_3`, `Sales Order`, `parent_chunk_business_glossary.txt_0`, `Order Item`, `parent_chunk_data_dictionary.txt_1`

**Context previews (first 3):**

1. _Business concept 'Sales Order' — The table contains core order header fields such as order_id, customer_id, order_date, order_status, amounts, and payment/shipping totals, which align strongly with a …_

2. _Foreign Keys: - customer_id → CUSTOMERS(customer_id or CustomerID?) - [missing other FK definitions] ========================================== ORDER_ITEMS (or ORDER_DETAILS?) ========================…_

3. _Business concept 'Order Item' — The table is explicitly named ORDER_ITEMS and contains classic line-item attributes such as order_id, product_id, quantity, unit_price, discount, and line_total, which …_

---

### ✅ ec_020 — Are foreign key constraints enforced in the schema?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.1603 | **Gate:** `proceed_with_warning`

**Expected answer:**
> No foreign key constraints are enforced in the DDL. While the data dictionary documents FK relationships (e.g., customer_id → CUSTOMERS, order_id → ORDERS), the actual CREATE TABLE statements omit the REFERENCES clauses. The schema explicitly notes 'FK constraints defined in data dictionary but not …

**System answer:**
> The retrieved context does not confirm that foreign key constraints are actually enforced by the database.

It does document foreign key relationships at the schema-description level: PAYMENTS.order_id references ORDERS, PAYMENTS.customer_id references CUSTOMERS, ORDER_ITEMS.order_id references ORDERS, and ORDER_ITEMS.product_id references PRODUCTS, plus a note showing customer_id → CUSTOMERS. How…

**Sources retrieved (11):** `parent_chunk_data_dictionary.txt_2`, `parent_chunk_data_dictionary.txt_3`, `parent_chunk_data_dictionary.txt_1`, `parent_chunk_business_glossary.txt_0`, `Payment gateway response→PAYMENTS`, `Sales Order→ORDERS`, `Order Item→ORDER_ITEMS`, `Inventory Item→PRODUCTS`

**Context previews (first 3):**

1. _Foreign Keys: - customer_id → CUSTOMERS(customer_id or CustomerID?) - [missing other FK definitions] ========================================== ORDER_ITEMS (or ORDER_DETAILS?) ========================…_

2. _========================================== PAYMENTS ==========================================  Primary Key: payment_id (unverified) | Column Name | Data Type | Constraints | Description | |----------…_

3. _DATA DICTIONARY - Enterprise Database Version: 2.1 (incomplete documentation) Last Updated: 2024-02-28 ========================================== CUSTOMERS ========================================== P…_

---

## Anomalies & Observations

No anomalies detected. All questions grounded with acceptable RAGAS scores.
