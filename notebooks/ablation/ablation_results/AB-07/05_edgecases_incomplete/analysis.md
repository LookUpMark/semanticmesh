# AB-07 — 05_edgecases_incomplete — Run Analysis

**Timestamp:** 2026-03-31 18:03:27  
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
| Chunk size / overlap | `384 / 48` |
| ER similarity threshold | `0.75` |

## Builder Results

| Metric | Value |
|--------|-------|
| Triplets extracted | 217 |
| Entities resolved | 77 |
| Tables parsed | 5 |
| Tables completed | 5 |

## Query Evaluation Summary

| Metric | Value |
|--------|-------|
| Questions | 20 |
| Grounded | **20/20 (100%)** |
| Avg GT Coverage | 100% |
| Avg Top Score | 0.4864 |
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
> In the retrieved context, “Customer” is a business glossary term under Customer Management, but its definition is incomplete: “An individual or organization that...” so the full formal definition is not available.

What can be stated from the context is that a customer is closely related to several nearby terms. “Client” is defined as “a person or company that purchases goods or services,” and the…

**Sources retrieved (12):** `customer_id→CUSTOMERS`, `parent_chunk_data_dictionary.txt_1`, `parent_chunk_data_dictionary.txt_2`, `Sales→ORDERS`, `parent_chunk_data_dictionary.txt_3`, `Payment gateway response→PAYMENTS`, `parent_chunk_business_glossary.txt_0`, `Order Items→ORDER_ITEMS`

**Context previews (first 3):**

1. _Business concept 'customer_id' is implemented by physical table CUSTOMERS (columns: customer_id, CustomerID, firstName, first_name, lastName, last_name, email, emailAddress, phone, phoneNumber, create…_

2. _DATA DICTIONARY - Enterprise Database Version: 2.1 (incomplete documentation) Last Updated: 2024-02-28 ========================================== CUSTOMERS ========================================== P…_

3. _Foreign Keys: - customer_id → CUSTOMERS(customer_id or CustomerID?) - [missing other FK definitions] ========================================== ORDER_ITEMS (or ORDER_DETAILS?) ========================…_

---

### ✅ ec_002 — What's the difference between firstName and first_name in the CUSTOMERS table?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.4883 | **Gate:** `proceed`

**Expected answer:**
> Both columns exist in the CUSTOMERS table with identical VARCHAR(50) data types. The data dictionary notes they appear to be duplicates resulting from inconsistent naming conventions (snake_case vs camelCase), but the actual usage by the application is not documented.

**System answer:**
> Based on the retrieved context, there is no documented business difference between `firstName` and `first_name` in `CUSTOMERS`.

The data dictionary says `firstName` is `VARCHAR(50)` and described as “Customer's first name,” while `first_name` is also `VARCHAR(50)` and is explicitly noted as “[appears to be duplicate].” The broader documentation also warns of inconsistent/duplicate naming in the s…

**Sources retrieved (12):** `customer_id→CUSTOMERS`, `parent_chunk_data_dictionary.txt_1`, `parent_chunk_data_dictionary.txt_2`, `parent_chunk_data_dictionary.txt_3`, `Order Items→ORDER_ITEMS`, `parent_chunk_business_glossary.txt_0`, `Order Items`, `Sales→ORDERS`

**Context previews (first 3):**

1. _Business concept 'customer_id' is implemented by physical table CUSTOMERS (columns: customer_id, CustomerID, firstName, first_name, lastName, last_name, email, emailAddress, phone, phoneNumber, create…_

2. _DATA DICTIONARY - Enterprise Database Version: 2.1 (incomplete documentation) Last Updated: 2024-02-28 ========================================== CUSTOMERS ========================================== P…_

3. _Foreign Keys: - customer_id → CUSTOMERS(customer_id or CustomerID?) - [missing other FK definitions] ========================================== ORDER_ITEMS (or ORDER_DETAILS?) ========================…_

---

### ✅ ec_003 — Which customer column should be used as a foreign key reference: customer_id or CustomerID?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.9258 | **Gate:** `proceed`

**Expected answer:**
> The CUSTOMERS table has both customer_id (defined as PRIMARY KEY) and CustomerID (defined as INTEGER with no constraints). The ORDERS table also has both customer_id and CustomerID columns with ambiguous FK references. The data dictionary indicates this inconsistency is documented but not yet resolv…

**System answer:**
> The retrieved context does not definitively resolve this, but it points more strongly to customer_id.

The strongest evidence is:
The CUSTOMERS table lists its primary key as “customer_id (or is it CustomerID? check with DBA)”, while CustomerID is described as a “Possible duplicate of customer_id”.
The foreign key documentation shows customer_id as the FK column name, with the note “customer_id → …

**Sources retrieved (12):** `parent_chunk_data_dictionary.txt_2`, `customer_id→CUSTOMERS`, `parent_chunk_data_dictionary.txt_1`, `parent_chunk_data_dictionary.txt_3`, `Sales→ORDERS`, `Payment gateway response→PAYMENTS`, `Order Items→ORDER_ITEMS`, `PRODUCTS (or INVENTORY?)→PRODUCTS`

**Context previews (first 3):**

1. _Foreign Keys: - customer_id → CUSTOMERS(customer_id or CustomerID?) - [missing other FK definitions] ========================================== ORDER_ITEMS (or ORDER_DETAILS?) ========================…_

2. _Business concept 'customer_id' is implemented by physical table CUSTOMERS (columns: customer_id, CustomerID, firstName, first_name, lastName, last_name, email, emailAddress, phone, phoneNumber, create…_

3. _DATA DICTIONARY - Enterprise Database Version: 2.1 (incomplete documentation) Last Updated: 2024-02-28 ========================================== CUSTOMERS ========================================== P…_

---

### ✅ ec_004 — What are the valid values for order_status?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.3951 | **Gate:** `proceed`

**Expected answer:**
> The business glossary documents several order statuses: Pending, Processing, Completed, Cancelled, On Hold, and Failed (which is marked as [definition missing]). However, these are not enforced by a CHECK constraint in the schema, and the data dictionary notes that valid values reference '[missing d…

**System answer:**
> The retrieved context does not list any valid values for ORDERS.order_status.

What the context does show is that the business concept Sales is implemented by the ORDERS table, and ORDERS includes the column order_status. The business glossary also says an Order “can be in various states.” However, no enumeration, code set, or allowed status values for order_status is provided anywhere in the retr…

**Sources retrieved (12):** `parent_chunk_data_dictionary.txt_3`, `Sales→ORDERS`, `parent_chunk_data_dictionary.txt_1`, `parent_chunk_data_dictionary.txt_2`, `Order Items→ORDER_ITEMS`, `parent_chunk_business_glossary.txt_0`, `Order Items`, `Payment gateway response→PAYMENTS`

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
> Yes, the retrieved context distinguishes them at the schema level, but only partially.

“Product” is represented by the business concept `PRODUCTS (or INVENTORY?)`, implemented by the `PRODUCTS` table. That table includes columns such as `product_id`/`ProductID`, `product_name`/`ProductName`, and `product_sku`/`sku`, along with category, price, stock, and status-related columns.

“Item” appears as…

**Sources retrieved (12):** `PRODUCTS (or INVENTORY?)→PRODUCTS`, `parent_chunk_data_dictionary.txt_2`, `Order Items→ORDER_ITEMS`, `parent_chunk_data_dictionary.txt_1`, `parent_chunk_data_dictionary.txt_3`, `parent_chunk_business_glossary.txt_0`, `Order Items`, `PRODUCTS (or INVENTORY?)`

**Context previews (first 3):**

1. _Business concept 'PRODUCTS (or INVENTORY?)' is implemented by physical table PRODUCTS (columns: product_id, ProductID, product_name, ProductName, product_sku, sku, product_category, category, unit_pri…_

2. _Foreign Keys: - customer_id → CUSTOMERS(customer_id or CustomerID?) - [missing other FK definitions] ========================================== ORDER_ITEMS (or ORDER_DETAILS?) ========================…_

3. _Business concept 'Order Items' — The table is explicitly named ORDER_ITEMS and documented as also referenced as ORDER_DETAILS, and its columns are characteristic of order line items (order_id, product…_

---

### ✅ ec_006 — Which table should ORDER_ITEMS.product_id reference: PRODUCTS or INVENTORY?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.9610 | **Gate:** `proceed`

**Expected answer:**
> The data dictionary states the FK reference is to 'PRODUCTS (or INVENTORY?)' and notes it is 'not verified'. The schema provides two potential targets: PRODUCTS table (which has product_id) and an INVENTORY table that is referenced in documentation but not defined in the DDL. The actual relationship…

**System answer:**
> Based on the retrieved context, ORDER_ITEMS.product_id should reference PRODUCTS.

The strongest evidence is that the business concept labeled "PRODUCTS (or INVENTORY?)" is explicitly implemented by the physical table PRODUCTS, and ORDER_ITEMS.product_id is documented as an FK to that same product entity. The context does show naming ambiguity in the documentation ("PRODUCTS or INVENTORY?"), but i…

**Sources retrieved (12):** `PRODUCTS (or INVENTORY?)→PRODUCTS`, `parent_chunk_data_dictionary.txt_2`, `Order Items→ORDER_ITEMS`, `parent_chunk_data_dictionary.txt_3`, `parent_chunk_data_dictionary.txt_1`, `PRODUCTS (or INVENTORY?)`, `Order Items`, `parent_chunk_business_glossary.txt_0`

**Context previews (first 3):**

1. _Business concept 'PRODUCTS (or INVENTORY?)' is implemented by physical table PRODUCTS (columns: product_id, ProductID, product_name, ProductName, product_sku, sku, product_category, category, unit_pri…_

2. _Foreign Keys: - customer_id → CUSTOMERS(customer_id or CustomerID?) - [missing other FK definitions] ========================================== ORDER_ITEMS (or ORDER_DETAILS?) ========================…_

3. _Business concept 'Order Items' — The table is explicitly named ORDER_ITEMS and documented as also referenced as ORDER_DETAILS, and its columns are characteristic of order line items (order_id, product…_

---

### ✅ ec_007 — What's the difference between Revenue and Sales?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.4224 | **Gate:** `proceed`

**Expected answer:**
> Both terms show circular definitions: Revenue is defined as 'Income from sales. The same as... [definition circular, see Sales]', while Sales is defined as 'Revenue from selling products. See Revenue.' The glossary provides no clear distinction between these concepts.

**System answer:**
> From the retrieved context, only Sales is defined; Revenue is not defined anywhere in the provided glossary, business concepts, or table mappings.

What the context does say about Sales is that the business concept “Sales” is implemented by the physical table ORDERS. The ORDERS table includes order-level fields such as order_id / OrderID, customer_id / CustomerID, order_date / OrderDate, order_sta…

**Sources retrieved (12):** `Sales→ORDERS`, `parent_chunk_data_dictionary.txt_2`, `Order Items→ORDER_ITEMS`, `parent_chunk_data_dictionary.txt_3`, `parent_chunk_business_glossary.txt_0`, `Order Items`, `parent_chunk_data_dictionary.txt_1`, `PRODUCTS (or INVENTORY?)→PRODUCTS`

**Context previews (first 3):**

1. _Business concept 'Sales' is implemented by physical table ORDERS (columns: order_id, OrderID, customer_id, CustomerID, order_date, OrderDate, order_status, orderAmount, total_amount, shippingAmount, t…_

2. _Foreign Keys: - customer_id → CUSTOMERS(customer_id or CustomerID?) - [missing other FK definitions] ========================================== ORDER_ITEMS (or ORDER_DETAILS?) ========================…_

3. _Business concept 'Order Items' — The table is explicitly named ORDER_ITEMS and documented as also referenced as ORDER_DETAILS, and its columns are characteristic of order line items (order_id, product…_

---

### ✅ ec_008 — Can one order have multiple payments?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0981 | **Gate:** `proceed_with_warning`

**Expected answer:**
> The PAYMENTS table has an order_id column, suggesting a many-to-one relationship (multiple payments can reference a single order). However, the relationship section in the glossary asks 'Or is it one-to-one?' indicating uncertainty. The ORDERS table has both payment_status and payment_method columns…

**System answer:**
> Based on the schema metadata, yes—the structure suggests one order can have multiple payments.

The evidence is in PAYMENTS: it has its own primary key, payment_id, and a separate foreign key, order_id, that references ORDERS. Because order_id is documented as an FK and not as unique, the schema allows multiple PAYMENTS rows to point to the same ORDERS row.

So the implied relationship is ORDERS 1…

**Sources retrieved (12):** `parent_chunk_data_dictionary.txt_3`, `Payment gateway response→PAYMENTS`, `Sales→ORDERS`, `parent_chunk_data_dictionary.txt_2`, `Order Items→ORDER_ITEMS`, `parent_chunk_data_dictionary.txt_1`, `PRODUCTS (or INVENTORY?)→PRODUCTS`, `customer_id→CUSTOMERS`

**Context previews (first 3):**

1. _========================================== PAYMENTS ==========================================  Primary Key: payment_id (unverified) | Column Name | Data Type | Constraints | Description | |----------…_

2. _Business concept 'Payment gateway response' is implemented by physical table PAYMENTS (columns: payment_id, PaymentID, order_id, customer_id, payment_date, payment_amount, payment_method, payment_stat…_

3. _Business concept 'Sales' is implemented by physical table ORDERS (columns: order_id, OrderID, customer_id, CustomerID, order_date, OrderDate, order_status, orderAmount, total_amount, shippingAmount, t…_

---

### ✅ ec_009 — What payment methods are accepted?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.1791 | **Gate:** `proceed_with_warning`

**Expected answer:**
> The PAYMENTS table has a payment_method column (VARCHAR(30)), but the data dictionary notes '[missing valid values]' and no CHECK constraint exists to enumerate acceptable methods. The schema does not document what values are valid (e.g., credit_card, debit, paypal, etc.).

**System answer:**
> The retrieved context does not list the accepted payment methods.

It only shows that payment method is captured in two places: PAYMENTS.payment_method and ORDERS.payment_method. For PAYMENTS.payment_method, the documentation explicitly says “[missing valid values],” and no allowed values are provided for ORDERS.payment_method either. So the schema indicates payment methods are stored, but the acc…

**Sources retrieved (12):** `parent_chunk_data_dictionary.txt_3`, `Payment gateway response→PAYMENTS`, `Sales→ORDERS`, `parent_chunk_data_dictionary.txt_1`, `parent_chunk_data_dictionary.txt_2`, `Order Items→ORDER_ITEMS`, `parent_chunk_business_glossary.txt_0`, `Payment gateway response`

**Context previews (first 3):**

1. _========================================== PAYMENTS ==========================================  Primary Key: payment_id (unverified) | Column Name | Data Type | Constraints | Description | |----------…_

2. _Business concept 'Payment gateway response' is implemented by physical table PAYMENTS (columns: payment_id, PaymentID, order_id, customer_id, payment_date, payment_amount, payment_method, payment_stat…_

3. _Business concept 'Sales' is implemented by physical table ORDERS (columns: order_id, OrderID, customer_id, CustomerID, order_date, OrderDate, order_status, orderAmount, total_amount, shippingAmount, t…_

---

### ✅ ec_010 — What's the correct table name: ORDER_ITEMS or ORDER_DETAILS?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.9982 | **Gate:** `proceed`

**Expected answer:**
> The DDL creates a table named ORDER_ITEMS, but the data dictionary header shows 'ORDER_ITEMS (or ORDER_DETAILS?)' and notes 'Table name ambiguity: ORDER_ITEMS vs ORDER_DETAILS'. The actual table name in the schema is ORDER_ITEMS, but documentation suggests the application may reference it differentl…

**System answer:**
> The retrieved context indicates that the correct physical table name is ORDER_ITEMS.

It is explicitly documented as “the table is explicitly named ORDER_ITEMS and documented as also referenced as ORDER_DETAILS.” So ORDER_DETAILS appears to be an alternate or inconsistent reference in documentation, but the implemented physical table is ORDER_ITEMS.

**Sources retrieved (12):** `Order Items→ORDER_ITEMS`, `parent_chunk_data_dictionary.txt_2`, `PRODUCTS (or INVENTORY?)→PRODUCTS`, `parent_chunk_data_dictionary.txt_3`, `parent_chunk_data_dictionary.txt_1`, `customer_id→CUSTOMERS`, `Order Items`, `Sales→ORDERS`

**Context previews (first 3):**

1. _Business concept 'Order Items' — The table is explicitly named ORDER_ITEMS and documented as also referenced as ORDER_DETAILS, and its columns are characteristic of order line items (order_id, product…_

2. _Foreign Keys: - customer_id → CUSTOMERS(customer_id or CustomerID?) - [missing other FK definitions] ========================================== ORDER_ITEMS (or ORDER_DETAILS?) ========================…_

3. _Business concept 'PRODUCTS (or INVENTORY?)' is implemented by physical table PRODUCTS (columns: product_id, ProductID, product_name, ProductName, product_sku, sku, product_category, category, unit_pri…_

---

### ✅ ec_011 — Which date column should be used to track when an order was created: order_date, OrderDate, or created_at?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.9218 | **Gate:** `proceed`

**Expected answer:**
> The ORDERS table has three date-related columns: order_date (DATE type), OrderDate (DATETIME type with different precision), and created_at (TIMESTAMP type). The data dictionary provides no guidance on which is actually used by the application or why three columns exist for potentially the same purp…

**System answer:**
> The retrieved context does not definitively specify which ORDERS column should be used as the authoritative “order created” date.

What the context does show is that the Sales/ORDERS table contains all three columns: order_date, OrderDate, and created_at. However, no ORDERS data dictionary entry is provided with descriptions for those columns.

There is also evidence elsewhere in the schema of dup…

**Sources retrieved (12):** `Sales→ORDERS`, `Payment gateway response→PAYMENTS`, `parent_chunk_data_dictionary.txt_1`, `parent_chunk_data_dictionary.txt_3`, `customer_id→CUSTOMERS`, `PRODUCTS (or INVENTORY?)→PRODUCTS`, `parent_chunk_data_dictionary.txt_2`, `Order Items→ORDER_ITEMS`

**Context previews (first 3):**

1. _Business concept 'Sales' is implemented by physical table ORDERS (columns: order_id, OrderID, customer_id, CustomerID, order_date, OrderDate, order_status, orderAmount, total_amount, shippingAmount, t…_

2. _Business concept 'Payment gateway response' is implemented by physical table PAYMENTS (columns: payment_id, PaymentID, order_id, customer_id, payment_date, payment_amount, payment_method, payment_stat…_

3. _DATA DICTIONARY - Enterprise Database Version: 2.1 (incomplete documentation) Last Updated: 2024-02-28 ========================================== CUSTOMERS ========================================== P…_

---

### ✅ ec_012 — What does the Failed order status mean?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0031 | **Gate:** `proceed_with_warning`

**Expected answer:**
> The business glossary lists Failed as an order status but marks it as '[definition missing]'. Other statuses have definitions (Pending, Processing, Completed, Cancelled, On Hold), but Failed is undefined despite being a valid status value.

**System answer:**
> I cannot find a documented meaning for the specific order status Failed in the retrieved context.

What the context does show is that the business concept Sales is implemented by the ORDERS table, and ORDERS includes an order_status column. The business glossary also says an Order is “a request to purchase products or services” and that it “can be in various states.” However, no valid values or de…

**Sources retrieved (12):** `parent_chunk_data_dictionary.txt_3`, `parent_chunk_data_dictionary.txt_1`, `Sales→ORDERS`, `parent_chunk_data_dictionary.txt_2`, `Order Items→ORDER_ITEMS`, `Payment gateway response→PAYMENTS`, `PRODUCTS (or INVENTORY?)→PRODUCTS`, `customer_id→CUSTOMERS`

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
> No explicit NOT NULL constraints are defined in the retrieved context.

The schema excerpts show constraints such as PK, FK, and possibly UNIQUE? or ?, but none of the listed columns in CUSTOMERS, PAYMENTS, or ORDER_ITEMS are documented with a NOT NULL constraint. The documentation is also marked as incomplete, so the context does not confirm whether NOT NULL exists in the actual database.

**Sources retrieved (12):** `parent_chunk_data_dictionary.txt_3`, `parent_chunk_data_dictionary.txt_2`, `parent_chunk_data_dictionary.txt_1`, `Order Items→ORDER_ITEMS`, `Sales→ORDERS`, `parent_chunk_business_glossary.txt_0`, `Order Items`, `PRODUCTS (or INVENTORY?)→PRODUCTS`

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
> From the retrieved context, both unit_price and current_price are columns on the PRODUCTS table, which implements the business concept "PRODUCTS (or INVENTORY?)". The same table also includes cost_price, so the schema clearly distinguishes multiple price-related fields at the product level.

However, the context does not define the semantic difference between PRODUCTS.unit_price and PRODUCTS.curre…

**Sources retrieved (12):** `PRODUCTS (or INVENTORY?)→PRODUCTS`, `parent_chunk_data_dictionary.txt_2`, `Order Items→ORDER_ITEMS`, `parent_chunk_data_dictionary.txt_3`, `Order Items`, `parent_chunk_business_glossary.txt_0`, `PRODUCTS (or INVENTORY?)`, `parent_chunk_data_dictionary.txt_1`

**Context previews (first 3):**

1. _Business concept 'PRODUCTS (or INVENTORY?)' is implemented by physical table PRODUCTS (columns: product_id, ProductID, product_name, ProductName, product_sku, sku, product_category, category, unit_pri…_

2. _Foreign Keys: - customer_id → CUSTOMERS(customer_id or CustomerID?) - [missing other FK definitions] ========================================== ORDER_ITEMS (or ORDER_DETAILS?) ========================…_

3. _Business concept 'Order Items' — The table is explicitly named ORDER_ITEMS and documented as also referenced as ORDER_DETAILS, and its columns are characteristic of order line items (order_id, product…_

---

### ✅ ec_015 — When is an invoice generated vs payment processed?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.6598 | **Gate:** `proceed`

**Expected answer:**
> The relationship section in the glossary asks 'An invoice is generated for an order. But when? And can one order have multiple invoices?' indicating the timing and cardinality are not defined. The glossary defines Invoice as 'A document requesting payment. Related to Bill' and Payment as 'The transf…

**System answer:**
> From the retrieved context, only the payment side is documented.

A payment is processed in the schema through the PAYMENTS table, which implements the business concept “Payment gateway response.” The available fields show that payment processing is recorded with payment_date, payment_amount, payment_method, payment_status, transaction_id, response_code, response_message, and created_at, and each …

**Sources retrieved (12):** `parent_chunk_data_dictionary.txt_3`, `parent_chunk_data_dictionary.txt_1`, `parent_chunk_data_dictionary.txt_2`, `Payment gateway response→PAYMENTS`, `Sales→ORDERS`, `parent_chunk_business_glossary.txt_0`, `Payment gateway response`, `Order Items→ORDER_ITEMS`

**Context previews (first 3):**

1. _========================================== PAYMENTS ==========================================  Primary Key: payment_id (unverified) | Column Name | Data Type | Constraints | Description | |----------…_

2. _DATA DICTIONARY - Enterprise Database Version: 2.1 (incomplete documentation) Last Updated: 2024-02-28 ========================================== CUSTOMERS ========================================== P…_

3. _Foreign Keys: - customer_id → CUSTOMERS(customer_id or CustomerID?) - [missing other FK definitions] ========================================== ORDER_ITEMS (or ORDER_DETAILS?) ========================…_

---

### ✅ ec_016 — Is the sku column in PRODUCTS unique?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.5549 | **Gate:** `proceed`

**Expected answer:**
> The PRODUCTS table has both product_sku and sku columns. The data dictionary notes sku 'should be UNIQUE?' but the DDL does not define a UNIQUE constraint on either column. No index is documented for these columns.

**System answer:**
> The retrieved context does not state that the `sku` column in `PRODUCTS` is unique. It only shows that `PRODUCTS` includes `product_sku` and `sku` as columns in the business concept mapping, but no uniqueness constraint is documented for either column. So, based on the available context, uniqueness cannot be confirmed.

**Sources retrieved (12):** `PRODUCTS (or INVENTORY?)→PRODUCTS`, `parent_chunk_data_dictionary.txt_2`, `parent_chunk_data_dictionary.txt_3`, `Order Items→ORDER_ITEMS`, `parent_chunk_data_dictionary.txt_1`, `customer_id→CUSTOMERS`, `Sales→ORDERS`, `Payment gateway response→PAYMENTS`

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
> From the retrieved context, the relationship between customers and orders is only partially documented.

The ORDERS table, which implements the business concept “Sales,” contains customer identifier columns: customer_id and CustomerID, along with order-level fields such as order_id, order_date, order_status, payment_status, and payment_method. The CUSTOMERS table contains customer_id and CustomerI…

**Sources retrieved (12):** `parent_chunk_data_dictionary.txt_3`, `parent_chunk_data_dictionary.txt_2`, `Sales→ORDERS`, `parent_chunk_data_dictionary.txt_1`, `Order Items→ORDER_ITEMS`, `customer_id→CUSTOMERS`, `parent_chunk_business_glossary.txt_0`, `Order Items`

**Context previews (first 3):**

1. _========================================== PAYMENTS ==========================================  Primary Key: payment_id (unverified) | Column Name | Data Type | Constraints | Description | |----------…_

2. _Foreign Keys: - customer_id → CUSTOMERS(customer_id or CustomerID?) - [missing other FK definitions] ========================================== ORDER_ITEMS (or ORDER_DETAILS?) ========================…_

3. _Business concept 'Sales' is implemented by physical table ORDERS (columns: order_id, OrderID, customer_id, CustomerID, order_date, OrderDate, order_status, orderAmount, total_amount, shippingAmount, t…_

---

### ✅ ec_018 — Which price column represents what the customer actually pays?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0581 | **Gate:** `proceed_with_warning`

**Expected answer:**
> Multiple price columns exist across tables: ORDERS has orderAmount and total_amount; ORDER_ITEMS has unit_price and UnitPrice; PRODUCTS has unit_price, current_price, and cost_price. The data dictionary does not explain which represents the final customer price, whether discounts are applied, or how…

**System answer:**
> The retrieved context does not explicitly identify any price column as “what the customer actually pays,” so that cannot be determined from the knowledge graph.

What the context does document is this: in ORDER_ITEMS, unit_price is described as “Price per unit.” ORDER_ITEMS also contains discount_percent, discount_amount, and line_total, but no definition is provided saying that line_total is the …

**Sources retrieved (12):** `Payment gateway response→PAYMENTS`, `Sales→ORDERS`, `parent_chunk_data_dictionary.txt_2`, `parent_chunk_data_dictionary.txt_3`, `PRODUCTS (or INVENTORY?)→PRODUCTS`, `Order Items→ORDER_ITEMS`, `parent_chunk_data_dictionary.txt_1`, `customer_id→CUSTOMERS`

**Context previews (first 3):**

1. _Business concept 'Payment gateway response' is implemented by physical table PAYMENTS (columns: payment_id, PaymentID, order_id, customer_id, payment_date, payment_amount, payment_method, payment_stat…_

2. _Business concept 'Sales' is implemented by physical table ORDERS (columns: order_id, OrderID, customer_id, CustomerID, order_date, OrderDate, order_status, orderAmount, total_amount, shippingAmount, t…_

3. _Foreign Keys: - customer_id → CUSTOMERS(customer_id or CustomerID?) - [missing other FK definitions] ========================================== ORDER_ITEMS (or ORDER_DETAILS?) ========================…_

---

### ✅ ec_019 — What's the difference between Shipment, Delivery, and Fulfillment?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0050 | **Gate:** `proceed_with_warning`

**Expected answer:**
> The glossary provides definitions but unclear boundaries: Shipment is 'The process of delivering goods to a customer'; Delivery is 'The completion of a Shipment when goods reach the customer'; Fulfillment is 'The process of preparing and delivering orders. Encompasses Shipment and Delivery.' The exa…

**System answer:**
> I cannot determine the difference between Shipment, Delivery, and Fulfillment from the retrieved context.

What is known from the context is limited to a partial business glossary and some schema metadata. The glossary includes entries such as Order, defined as “a request to purchase products or services” that “can be in various states,” and Transaction, described as similar to Order but more gene…

**Sources retrieved (12):** `parent_chunk_data_dictionary.txt_2`, `Order Items→ORDER_ITEMS`, `parent_chunk_data_dictionary.txt_3`, `parent_chunk_business_glossary.txt_0`, `Order Items`, `parent_chunk_data_dictionary.txt_1`, `Sales→ORDERS`, `Payment gateway response→PAYMENTS`

**Context previews (first 3):**

1. _Foreign Keys: - customer_id → CUSTOMERS(customer_id or CustomerID?) - [missing other FK definitions] ========================================== ORDER_ITEMS (or ORDER_DETAILS?) ========================…_

2. _Business concept 'Order Items' — The table is explicitly named ORDER_ITEMS and documented as also referenced as ORDER_DETAILS, and its columns are characteristic of order line items (order_id, product…_

3. _========================================== PAYMENTS ==========================================  Primary Key: payment_id (unverified) | Column Name | Data Type | Constraints | Description | |----------…_

---

### ✅ ec_020 — Are foreign key constraints enforced in the schema?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.1603 | **Gate:** `proceed_with_warning`

**Expected answer:**
> No foreign key constraints are enforced in the DDL. While the data dictionary documents FK relationships (e.g., customer_id → CUSTOMERS, order_id → ORDERS), the actual CREATE TABLE statements omit the REFERENCES clauses. The schema explicitly notes 'FK constraints defined in data dictionary but not …

**System answer:**
> The retrieved context documents foreign key relationships, but it does not confirm that foreign key constraints are actually enforced by the database.

What is shown is schema-level metadata such as ORDER_ITEMS.order_id marked as FK referencing ORDERS, ORDER_ITEMS.product_id referencing PRODUCTS, PAYMENTS.order_id referencing ORDERS, PAYMENTS.customer_id referencing CUSTOMERS, and a separate note …

**Sources retrieved (12):** `parent_chunk_data_dictionary.txt_2`, `parent_chunk_data_dictionary.txt_3`, `parent_chunk_data_dictionary.txt_1`, `Order Items→ORDER_ITEMS`, `parent_chunk_business_glossary.txt_0`, `Order Items`, `Payment gateway response→PAYMENTS`, `Sales→ORDERS`

**Context previews (first 3):**

1. _Foreign Keys: - customer_id → CUSTOMERS(customer_id or CustomerID?) - [missing other FK definitions] ========================================== ORDER_ITEMS (or ORDER_DETAILS?) ========================…_

2. _========================================== PAYMENTS ==========================================  Primary Key: payment_id (unverified) | Column Name | Data Type | Constraints | Description | |----------…_

3. _DATA DICTIONARY - Enterprise Database Version: 2.1 (incomplete documentation) Last Updated: 2024-02-28 ========================================== CUSTOMERS ========================================== P…_

---

## Anomalies & Observations

No anomalies detected. All questions grounded with acceptable RAGAS scores.
