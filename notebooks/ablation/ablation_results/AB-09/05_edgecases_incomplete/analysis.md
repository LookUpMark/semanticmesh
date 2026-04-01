# AB-09 — 05_edgecases_incomplete — Run Analysis

**Timestamp:** 2026-03-31 22:29:03  
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
| Triplets extracted | 139 |
| Entities resolved | 88 |
| Tables parsed | 5 |
| Tables completed | 5 |

## Query Evaluation Summary

| Metric | Value |
|--------|-------|
| Questions | 20 |
| Grounded | **20/20 (100%)** |
| Avg GT Coverage | 100% |
| Avg Top Score | 0.4682 |
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
> In the BUSINESS GLOSSARY under Customer Management, Customer is defined only partially as “An individual or organization that...” because the definition is incomplete in the retrieved context.

The same glossary provides related distinctions: Client is “a person or company that purchases goods or services” and may be used interchangeably with Customer in some contexts; Account Holder is similar to…

**Sources retrieved (12):** `CUSTOMERS(customer_id or CustomerID?)→CUSTOMERS`, `parent_chunk_data_dictionary.txt_1`, `parent_chunk_data_dictionary.txt_2`, `Sales→ORDERS`, `parent_chunk_data_dictionary.txt_3`, `Payment gateway response→PAYMENTS`, `parent_chunk_business_glossary.txt_0`, `CUSTOMERS(customer_id or CustomerID?)`

**Context previews (first 3):**

1. _Business concept 'CUSTOMERS(customer_id or CustomerID?)' is implemented by physical table CUSTOMERS (columns: customer_id, CustomerID, firstName, first_name, lastName, last_name, email, emailAddress, …_

2. _DATA DICTIONARY - Enterprise Database Version: 2.1 (incomplete documentation) Last Updated: 2024-02-28 ========================================== CUSTOMERS ========================================== P…_

3. _Foreign Keys: - customer_id → CUSTOMERS(customer_id or CustomerID?) - [missing other FK definitions] ========================================== ORDER_ITEMS (or ORDER_DETAILS?) ========================…_

---

### ✅ ec_002 — What's the difference between firstName and first_name in the CUSTOMERS table?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.5954 | **Gate:** `proceed`

**Expected answer:**
> Both columns exist in the CUSTOMERS table with identical VARCHAR(50) data types. The data dictionary notes they appear to be duplicates resulting from inconsistent naming conventions (snake_case vs camelCase), but the actual usage by the application is not documented.

**System answer:**
> In the retrieved context, both `firstName` and `first_name` exist in the `CUSTOMERS` table. The documented difference is only that `firstName` is described as “Customer’s first name,” while `first_name` is labeled “[appears to be duplicate].” Both are `VARCHAR(50)`, and the documentation marks their constraints as `?`.

So, based on the available context, no confirmed business or functional differ…

**Sources retrieved (12):** `CUSTOMERS(customer_id or CustomerID?)→CUSTOMERS`, `parent_chunk_data_dictionary.txt_1`, `parent_chunk_data_dictionary.txt_2`, `parent_chunk_data_dictionary.txt_3`, `Order Items→ORDER_ITEMS`, `Order Items`, `Inventory Item→PRODUCTS`, `CUSTOMERS(customer_id or CustomerID?)`

**Context previews (first 3):**

1. _Business concept 'CUSTOMERS(customer_id or CustomerID?)' is implemented by physical table CUSTOMERS (columns: customer_id, CustomerID, firstName, first_name, lastName, last_name, email, emailAddress, …_

2. _DATA DICTIONARY - Enterprise Database Version: 2.1 (incomplete documentation) Last Updated: 2024-02-28 ========================================== CUSTOMERS ========================================== P…_

3. _Foreign Keys: - customer_id → CUSTOMERS(customer_id or CustomerID?) - [missing other FK definitions] ========================================== ORDER_ITEMS (or ORDER_DETAILS?) ========================…_

---

### ✅ ec_003 — Which customer column should be used as a foreign key reference: customer_id or CustomerID?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.9258 | **Gate:** `proceed`

**Expected answer:**
> The CUSTOMERS table has both customer_id (defined as PRIMARY KEY) and CustomerID (defined as INTEGER with no constraints). The ORDERS table also has both customer_id and CustomerID columns with ambiguous FK references. The data dictionary indicates this inconsistency is documented but not yet resolv…

**System answer:**
> The context does not definitively resolve this. The strongest evidence points to using CUSTOMERS.customer_id, because the CUSTOMERS table lists customer_id as the primary key, while CustomerID is described as a possible duplicate, and foreign key examples use customer_id. However, the documentation explicitly flags uncertainty: “customer_id (or is it CustomerID? check with DBA)” and even shows a f…

**Sources retrieved (12):** `parent_chunk_data_dictionary.txt_2`, `CUSTOMERS(customer_id or CustomerID?)→CUSTOMERS`, `parent_chunk_data_dictionary.txt_1`, `parent_chunk_data_dictionary.txt_3`, `Sales→ORDERS`, `Payment gateway response→PAYMENTS`, `Order Items→ORDER_ITEMS`, `Order Items`

**Context previews (first 3):**

1. _Foreign Keys: - customer_id → CUSTOMERS(customer_id or CustomerID?) - [missing other FK definitions] ========================================== ORDER_ITEMS (or ORDER_DETAILS?) ========================…_

2. _Business concept 'CUSTOMERS(customer_id or CustomerID?)' is implemented by physical table CUSTOMERS (columns: customer_id, CustomerID, firstName, first_name, lastName, last_name, email, emailAddress, …_

3. _DATA DICTIONARY - Enterprise Database Version: 2.1 (incomplete documentation) Last Updated: 2024-02-28 ========================================== CUSTOMERS ========================================== P…_

---

### ✅ ec_004 — What are the valid values for order_status?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.3951 | **Gate:** `proceed`

**Expected answer:**
> The business glossary documents several order statuses: Pending, Processing, Completed, Cancelled, On Hold, and Failed (which is marked as [definition missing]). However, these are not enforced by a CHECK constraint in the schema, and the data dictionary notes that valid values reference '[missing d…

**System answer:**
> The retrieved context does not provide an enumeration of valid values for `order_status`.

What it does show is that `order_status` is a column on the `ORDERS` table, and the business concept `Sales` is implemented by `ORDERS` with columns including `order_id`, `customer_id`, `order_date`, `order_status`, `orderAmount`, `total_amount`, `shippingAmount`, `tax_amount`, `payment_status`, and `payment…

**Sources retrieved (12):** `parent_chunk_data_dictionary.txt_3`, `Sales→ORDERS`, `parent_chunk_data_dictionary.txt_1`, `parent_chunk_data_dictionary.txt_2`, `parent_chunk_business_glossary.txt_0`, `Payment gateway response→PAYMENTS`, `Order Items`, `Order Items→ORDER_ITEMS`

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
> The retrieved context does not provide an explicit glossary definition that distinguishes “Product,” “Item,” and “SKU” as business terms, so I cannot state a formal semantic difference from the knowledge graph alone.

What the context does show is this:

The closest match to “Product” is the physical table PRODUCTS. However, the business concept mapped to that table is not called “Product”; it is …

**Sources retrieved (12):** `Inventory Item→PRODUCTS`, `parent_chunk_data_dictionary.txt_2`, `Order Items→ORDER_ITEMS`, `Order Items`, `parent_chunk_data_dictionary.txt_1`, `parent_chunk_data_dictionary.txt_3`, `parent_chunk_business_glossary.txt_0`, `Inventory Item`

**Context previews (first 3):**

1. _Business concept 'Inventory Item' — The table stores physical stock and replenishment attributes such as stock_quantity, quantity_in_stock, and reorder_level, alongside product identifiers and pricing…_

2. _Foreign Keys: - customer_id → CUSTOMERS(customer_id or CustomerID?) - [missing other FK definitions] ========================================== ORDER_ITEMS (or ORDER_DETAILS?) ========================…_

3. _Business concept 'Order Items' — The table is explicitly named ORDER_ITEMS and contains core line-item attributes such as order_id, product_id, quantity, unit_price, discounts, and line_total, which s…_

---

### ✅ ec_006 — Which table should ORDER_ITEMS.product_id reference: PRODUCTS or INVENTORY?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.9775 | **Gate:** `proceed`

**Expected answer:**
> The data dictionary states the FK reference is to 'PRODUCTS (or INVENTORY?)' and notes it is 'not verified'. The schema provides two potential targets: PRODUCTS table (which has product_id) and an INVENTORY table that is referenced in documentation but not defined in the DDL. The actual relationship…

**System answer:**
> Based on the retrieved context, ORDER_ITEMS.product_id should reference PRODUCTS.

The strongest support is in the ORDER_ITEMS documentation, which says product_id is an FK that “References PRODUCTS,” and the concept mapping for Order Items maps ORDER_ITEMS as the physical table containing product_id. Separately, the “Inventory Item” business concept is implemented by the physical table PRODUCTS, …

**Sources retrieved (12):** `Inventory Item→PRODUCTS`, `parent_chunk_data_dictionary.txt_2`, `Order Items`, `Order Items→ORDER_ITEMS`, `parent_chunk_data_dictionary.txt_3`, `parent_chunk_data_dictionary.txt_1`, `Inventory Item`, `parent_chunk_business_glossary.txt_0`

**Context previews (first 3):**

1. _Business concept 'Inventory Item' — The table stores physical stock and replenishment attributes such as stock_quantity, quantity_in_stock, and reorder_level, alongside product identifiers and pricing…_

2. _Foreign Keys: - customer_id → CUSTOMERS(customer_id or CustomerID?) - [missing other FK definitions] ========================================== ORDER_ITEMS (or ORDER_DETAILS?) ========================…_

3. _Order Items: The table is explicitly named ORDER_ITEMS and contains core line-item attributes such as order_id, product_id, quantity, unit_price, discounts, and line_total, which strongly indicate ord…_

---

### ✅ ec_007 — What's the difference between Revenue and Sales?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.4224 | **Gate:** `proceed`

**Expected answer:**
> Both terms show circular definitions: Revenue is defined as 'Income from sales. The same as... [definition circular, see Sales]', while Sales is defined as 'Revenue from selling products. See Revenue.' The glossary provides no clear distinction between these concepts.

**System answer:**
> From the retrieved context, only Sales is described; Revenue is not defined anywhere in the available glossary or schema metadata, so the difference between the two cannot be fully answered from this knowledge graph.

What the context does show is that the business concept Sales is implemented by the physical table ORDERS. That table includes order identifiers and customer links plus monetary and …

**Sources retrieved (12):** `Sales→ORDERS`, `parent_chunk_data_dictionary.txt_2`, `Inventory Item→PRODUCTS`, `parent_chunk_data_dictionary.txt_3`, `Order Items→ORDER_ITEMS`, `Order Items`, `parent_chunk_business_glossary.txt_0`, `Inventory Item`

**Context previews (first 3):**

1. _Business concept 'Sales' is implemented by physical table ORDERS (columns: order_id, OrderID, customer_id, CustomerID, order_date, OrderDate, order_status, orderAmount, total_amount, shippingAmount, t…_

2. _Foreign Keys: - customer_id → CUSTOMERS(customer_id or CustomerID?) - [missing other FK definitions] ========================================== ORDER_ITEMS (or ORDER_DETAILS?) ========================…_

3. _Business concept 'Inventory Item' — The table stores physical stock and replenishment attributes such as stock_quantity, quantity_in_stock, and reorder_level, alongside product identifiers and pricing…_

---

### ✅ ec_008 — Can one order have multiple payments?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0981 | **Gate:** `proceed_with_warning`

**Expected answer:**
> The PAYMENTS table has an order_id column, suggesting a many-to-one relationship (multiple payments can reference a single order). However, the relationship section in the glossary asks 'Or is it one-to-one?' indicating uncertainty. The ORDERS table has both payment_status and payment_method columns…

**System answer:**
> The context suggests that multiple payments per order may be possible, but it does not prove the business rule definitively.

What is known from the context is that PAYMENTS has payment_id as the primary key and order_id as a foreign key referencing ORDERS. That structure means payments are stored as separate rows and linked back to an order through order_id. The context does not document any uniq…

**Sources retrieved (12):** `parent_chunk_data_dictionary.txt_3`, `Payment gateway response→PAYMENTS`, `Sales→ORDERS`, `parent_chunk_data_dictionary.txt_2`, `parent_chunk_data_dictionary.txt_1`, `Order Items→ORDER_ITEMS`, `Order Items`, `Inventory Item→PRODUCTS`

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

What it does show is that payment method is captured in two tables:
PAYMENTS.payment_method, where the documentation explicitly says “[missing valid values],” and
ORDERS.payment_method, listed as a column in the ORDERS table mapping.

So the schema indicates payment methods are stored, but the knowledge graph does not provide the a…

**Sources retrieved (12):** `parent_chunk_data_dictionary.txt_3`, `Payment gateway response→PAYMENTS`, `Sales→ORDERS`, `parent_chunk_data_dictionary.txt_1`, `parent_chunk_data_dictionary.txt_2`, `parent_chunk_business_glossary.txt_0`, `Payment gateway response`, `CUSTOMERS(customer_id or CustomerID?)→CUSTOMERS`

**Context previews (first 3):**

1. _========================================== PAYMENTS ==========================================  Primary Key: payment_id (unverified) | Column Name | Data Type | Constraints | Description | |----------…_

2. _Business concept 'Payment gateway response' is implemented by physical table PAYMENTS (columns: payment_id, PaymentID, order_id, customer_id, payment_date, payment_amount, payment_method, payment_stat…_

3. _Business concept 'Sales' is implemented by physical table ORDERS (columns: order_id, OrderID, customer_id, CustomerID, order_date, OrderDate, order_status, orderAmount, total_amount, shippingAmount, t…_

---

### ✅ ec_010 — What's the correct table name: ORDER_ITEMS or ORDER_DETAILS?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.9863 | **Gate:** `proceed`

**Expected answer:**
> The DDL creates a table named ORDER_ITEMS, but the data dictionary header shows 'ORDER_ITEMS (or ORDER_DETAILS?)' and notes 'Table name ambiguity: ORDER_ITEMS vs ORDER_DETAILS'. The actual table name in the schema is ORDER_ITEMS, but documentation suggests the application may reference it differentl…

**System answer:**
> Based on the retrieved context, the table name is most strongly supported as ORDER_ITEMS.

The evidence is:
The Business Concept says “The table is explicitly named ORDER_ITEMS.”
The ConceptTableMapping says the business concept “Order Items” is implemented by physical table ORDER_ITEMS.
One schema chunk does mention “ORDER_ITEMS (or ORDER_DETAILS?)”, which indicates some documentation uncertainty…

**Sources retrieved (12):** `Order Items`, `parent_chunk_data_dictionary.txt_2`, `Order Items→ORDER_ITEMS`, `Inventory Item→PRODUCTS`, `parent_chunk_data_dictionary.txt_3`, `parent_chunk_data_dictionary.txt_1`, `CUSTOMERS(customer_id or CustomerID?)→CUSTOMERS`, `Sales→ORDERS`

**Context previews (first 3):**

1. _Order Items: The table is explicitly named ORDER_ITEMS and contains core line-item attributes such as order_id, product_id, quantity, unit_price, discounts, and line_total, which strongly indicate ord…_

2. _Foreign Keys: - customer_id → CUSTOMERS(customer_id or CustomerID?) - [missing other FK definitions] ========================================== ORDER_ITEMS (or ORDER_DETAILS?) ========================…_

3. _Business concept 'Order Items' — The table is explicitly named ORDER_ITEMS and contains core line-item attributes such as order_id, product_id, quantity, unit_price, discounts, and line_total, which s…_

---

### ✅ ec_011 — Which date column should be used to track when an order was created: order_date, OrderDate, or created_at?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.9218 | **Gate:** `proceed`

**Expected answer:**
> The ORDERS table has three date-related columns: order_date (DATE type), OrderDate (DATETIME type with different precision), and created_at (TIMESTAMP type). The data dictionary provides no guidance on which is actually used by the application or why three columns exist for potentially the same purp…

**System answer:**
> From the retrieved context alone, this cannot be determined with confidence.

What is known is that the ORDERS table for the Sales concept contains all three columns: order_date, OrderDate, and created_at. However, the retrieved context does not provide a data dictionary entry or column descriptions for ORDERS that define the meaning of those fields. The only explicit duplicate notes in the contex…

**Sources retrieved (12):** `Sales→ORDERS`, `Payment gateway response→PAYMENTS`, `CUSTOMERS(customer_id or CustomerID?)→CUSTOMERS`, `parent_chunk_data_dictionary.txt_1`, `parent_chunk_data_dictionary.txt_3`, `Inventory Item→PRODUCTS`, `parent_chunk_data_dictionary.txt_2`, `Order Items→ORDER_ITEMS`

**Context previews (first 3):**

1. _Business concept 'Sales' is implemented by physical table ORDERS (columns: order_id, OrderID, customer_id, CustomerID, order_date, OrderDate, order_status, orderAmount, total_amount, shippingAmount, t…_

2. _Business concept 'Payment gateway response' is implemented by physical table PAYMENTS (columns: payment_id, PaymentID, order_id, customer_id, payment_date, payment_amount, payment_method, payment_stat…_

3. _Business concept 'CUSTOMERS(customer_id or CustomerID?)' is implemented by physical table CUSTOMERS (columns: customer_id, CustomerID, firstName, first_name, lastName, last_name, email, emailAddress, …_

---

### ✅ ec_012 — What does the Failed order status mean?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0031 | **Gate:** `proceed_with_warning`

**Expected answer:**
> The business glossary lists Failed as an order status but marks it as '[definition missing]'. Other statuses have definitions (Pending, Processing, Completed, Cancelled, On Hold), but Failed is undefined despite being a valid status value.

**System answer:**
> The meaning of a Failed order status cannot be determined from the provided context.

The retrieved context shows that ORDERS has an order_status column in the Sales/ORDERS mapping, and the business glossary says an Order “can be in various states,” but it does not list any valid order_status values or define a value named Failed. So there is no supported definition of Failed as an order status in…

**Sources retrieved (12):** `parent_chunk_data_dictionary.txt_3`, `parent_chunk_data_dictionary.txt_1`, `Sales→ORDERS`, `parent_chunk_data_dictionary.txt_2`, `Inventory Item→PRODUCTS`, `Order Items→ORDER_ITEMS`, `Payment gateway response→PAYMENTS`, `Order Items`

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

The schema metadata shown for CUSTOMERS, PAYMENTS, and ORDER_ITEMS lists constraints such as PK, FK, and one UNIQUE? note, but no column is marked NOT NULL. Much of the documentation is also flagged as incomplete or missing, so the context does not provide any confirmed NOT NULL definitions.

**Sources retrieved (12):** `parent_chunk_data_dictionary.txt_3`, `parent_chunk_data_dictionary.txt_2`, `parent_chunk_data_dictionary.txt_1`, `Sales→ORDERS`, `Inventory Item→PRODUCTS`, `parent_chunk_business_glossary.txt_0`, `Inventory Item`, `Order Items`

**Context previews (first 3):**

1. _========================================== PAYMENTS ==========================================  Primary Key: payment_id (unverified) | Column Name | Data Type | Constraints | Description | |----------…_

2. _Foreign Keys: - customer_id → CUSTOMERS(customer_id or CustomerID?) - [missing other FK definitions] ========================================== ORDER_ITEMS (or ORDER_DETAILS?) ========================…_

3. _DATA DICTIONARY - Enterprise Database Version: 2.1 (incomplete documentation) Last Updated: 2024-02-28 ========================================== CUSTOMERS ========================================== P…_

---

### ✅ ec_014 — What's the difference between unit_price and current_price in PRODUCTS?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.4059 | **Gate:** `proceed`

**Expected answer:**
> The PRODUCTS table has both unit_price and current_price columns (both DECIMAL(10,2)). The data dictionary asks 'Different from unit_price?' but provides no explanation of the distinction or when each would be used.

**System answer:**
> From the retrieved context, I cannot determine an explicit documented difference between unit_price and current_price in PRODUCTS.

What the context does say is:

The business concept Inventory Item is implemented by the physical table PRODUCTS, and that table includes both unit_price and current_price, along with cost_price, product identifiers, and stock-related fields such as stock_quantity, qu…

**Sources retrieved (12):** `Inventory Item→PRODUCTS`, `parent_chunk_data_dictionary.txt_2`, `Order Items→ORDER_ITEMS`, `Order Items`, `parent_chunk_data_dictionary.txt_3`, `parent_chunk_business_glossary.txt_0`, `Inventory Item`, `parent_chunk_data_dictionary.txt_1`

**Context previews (first 3):**

1. _Business concept 'Inventory Item' — The table stores physical stock and replenishment attributes such as stock_quantity, quantity_in_stock, and reorder_level, alongside product identifiers and pricing…_

2. _Foreign Keys: - customer_id → CUSTOMERS(customer_id or CustomerID?) - [missing other FK definitions] ========================================== ORDER_ITEMS (or ORDER_DETAILS?) ========================…_

3. _Business concept 'Order Items' — The table is explicitly named ORDER_ITEMS and contains core line-item attributes such as order_id, product_id, quantity, unit_price, discounts, and line_total, which s…_

---

### ✅ ec_015 — When is an invoice generated vs payment processed?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.6598 | **Gate:** `proceed`

**Expected answer:**
> The relationship section in the glossary asks 'An invoice is generated for an order. But when? And can one order have multiple invoices?' indicating the timing and cardinality are not defined. The glossary defines Invoice as 'A document requesting payment. Related to Bill' and Payment as 'The transf…

**System answer:**
> The retrieved context does not define any invoice concept, invoice table, or rule for when an invoice is generated. So I cannot say when an invoice is generated from this knowledge graph.

What the context does support is the schema-level representation of payment processing. Payment processing is represented by the PAYMENTS table, which implements the business concept “Payment gateway response.” …

**Sources retrieved (12):** `parent_chunk_data_dictionary.txt_3`, `parent_chunk_data_dictionary.txt_1`, `parent_chunk_data_dictionary.txt_2`, `Payment gateway response→PAYMENTS`, `Sales→ORDERS`, `parent_chunk_business_glossary.txt_0`, `Payment gateway response`, `Inventory Item→PRODUCTS`

**Context previews (first 3):**

1. _========================================== PAYMENTS ==========================================  Primary Key: payment_id (unverified) | Column Name | Data Type | Constraints | Description | |----------…_

2. _DATA DICTIONARY - Enterprise Database Version: 2.1 (incomplete documentation) Last Updated: 2024-02-28 ========================================== CUSTOMERS ========================================== P…_

3. _Foreign Keys: - customer_id → CUSTOMERS(customer_id or CustomerID?) - [missing other FK definitions] ========================================== ORDER_ITEMS (or ORDER_DETAILS?) ========================…_

---

### ✅ ec_016 — Is the sku column in PRODUCTS unique?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.2814 | **Gate:** `proceed`

**Expected answer:**
> The PRODUCTS table has both product_sku and sku columns. The data dictionary notes sku 'should be UNIQUE?' but the DDL does not define a UNIQUE constraint on either column. No index is documented for these columns.

**System answer:**
> The retrieved context shows that PRODUCTS includes product_sku and sku, but it does not provide any constraint indicating that sku is unique. So based on the available context, uniqueness of the sku column cannot be confirmed.

**Sources retrieved (12):** `Inventory Item→PRODUCTS`, `parent_chunk_data_dictionary.txt_2`, `parent_chunk_data_dictionary.txt_3`, `Order Items`, `Order Items→ORDER_ITEMS`, `parent_chunk_data_dictionary.txt_1`, `CUSTOMERS(customer_id or CustomerID?)→CUSTOMERS`, `Sales→ORDERS`

**Context previews (first 3):**

1. _Business concept 'Inventory Item' — The table stores physical stock and replenishment attributes such as stock_quantity, quantity_in_stock, and reorder_level, alongside product identifiers and pricing…_

2. _Foreign Keys: - customer_id → CUSTOMERS(customer_id or CustomerID?) - [missing other FK definitions] ========================================== ORDER_ITEMS (or ORDER_DETAILS?) ========================…_

3. _========================================== PAYMENTS ==========================================  Primary Key: payment_id (unverified) | Column Name | Data Type | Constraints | Description | |----------…_

---

### ✅ ec_017 — What is the relationship between customers and orders?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0859 | **Gate:** `proceed_with_warning`

**Expected answer:**
> The glossary states 'A customer can place multiple orders. Or is it accounts that place orders?' indicating uncertainty about the relationship. The ORDERS table has both customer_id and CustomerID columns with ambiguous FK references, and the data dictionary notes they reference 'customer (which tab…

**System answer:**
> In the retrieved context, the relationship is a schema-level link between the `ORDERS` table and the `CUSTOMERS` table through customer identifier columns.

`ORDERS` (the physical table implementing the business concept “Sales”) contains `customer_id` and `CustomerID`. `CUSTOMERS` has primary key documentation for `customer_id` and a possible duplicate `CustomerID`. Taken together, this indicates …

**Sources retrieved (12):** `parent_chunk_data_dictionary.txt_3`, `parent_chunk_data_dictionary.txt_2`, `Sales→ORDERS`, `parent_chunk_data_dictionary.txt_1`, `Order Items→ORDER_ITEMS`, `CUSTOMERS(customer_id or CustomerID?)→CUSTOMERS`, `Order Items`, `Inventory Item→PRODUCTS`

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
> The retrieved context does not explicitly identify any single column as “what the customer actually pays.”

It shows several monetary columns, but their business meaning is not fully documented:
ORDERS has orderAmount, total_amount, shippingAmount, and tax_amount.
ORDER_ITEMS has unit_price, discount_percent, discount_amount, and line_total.
PAYMENTS has payment_amount.
PRODUCTS has unit_price, cu…

**Sources retrieved (12):** `Payment gateway response→PAYMENTS`, `Sales→ORDERS`, `parent_chunk_data_dictionary.txt_2`, `parent_chunk_data_dictionary.txt_3`, `Order Items→ORDER_ITEMS`, `CUSTOMERS(customer_id or CustomerID?)→CUSTOMERS`, `parent_chunk_data_dictionary.txt_1`, `Inventory Item→PRODUCTS`

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
> I cannot determine the difference between Shipment, Delivery, and Fulfillment from the retrieved context. The only glossary content provided covers terms such as Customer, Client, Account Holder, End User, Order, and Transaction, and the glossary itself is marked “Partial (pending review).” There are no definitions or table mappings in the context for Shipment, Delivery, or Fulfillment.

**Sources retrieved (12):** `parent_chunk_data_dictionary.txt_2`, `parent_chunk_data_dictionary.txt_3`, `Order Items→ORDER_ITEMS`, `Inventory Item→PRODUCTS`, `Order Items`, `parent_chunk_business_glossary.txt_0`, `Inventory Item`, `parent_chunk_data_dictionary.txt_1`

**Context previews (first 3):**

1. _Foreign Keys: - customer_id → CUSTOMERS(customer_id or CustomerID?) - [missing other FK definitions] ========================================== ORDER_ITEMS (or ORDER_DETAILS?) ========================…_

2. _========================================== PAYMENTS ==========================================  Primary Key: payment_id (unverified) | Column Name | Data Type | Constraints | Description | |----------…_

3. _Business concept 'Order Items' — The table is explicitly named ORDER_ITEMS and contains core line-item attributes such as order_id, product_id, quantity, unit_price, discounts, and line_total, which s…_

---

### ✅ ec_020 — Are foreign key constraints enforced in the schema?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.1603 | **Gate:** `proceed_with_warning`

**Expected answer:**
> No foreign key constraints are enforced in the DDL. While the data dictionary documents FK relationships (e.g., customer_id → CUSTOMERS, order_id → ORDERS), the actual CREATE TABLE statements omit the REFERENCES clauses. The schema explicitly notes 'FK constraints defined in data dictionary but not …

**System answer:**
> The retrieved context does not establish whether foreign key constraints are actually enforced at the database level.

What is documented is schema metadata that labels certain columns as FK and describes intended references: ORDER_ITEMS.order_id references ORDERS, ORDER_ITEMS.product_id references PRODUCTS (with ambiguity noted as “PRODUCTS (or INVENTORY?)”), PAYMENTS.order_id references ORDERS, …

**Sources retrieved (12):** `parent_chunk_data_dictionary.txt_2`, `parent_chunk_data_dictionary.txt_3`, `parent_chunk_data_dictionary.txt_1`, `parent_chunk_business_glossary.txt_0`, `Order Items`, `Payment gateway response→PAYMENTS`, `Order Items→ORDER_ITEMS`, `Sales→ORDERS`

**Context previews (first 3):**

1. _Foreign Keys: - customer_id → CUSTOMERS(customer_id or CustomerID?) - [missing other FK definitions] ========================================== ORDER_ITEMS (or ORDER_DETAILS?) ========================…_

2. _========================================== PAYMENTS ==========================================  Primary Key: payment_id (unverified) | Column Name | Data Type | Constraints | Description | |----------…_

3. _DATA DICTIONARY - Enterprise Database Version: 2.1 (incomplete documentation) Last Updated: 2024-02-28 ========================================== CUSTOMERS ========================================== P…_

---

## Anomalies & Observations

No anomalies detected. All questions grounded with acceptable RAGAS scores.
