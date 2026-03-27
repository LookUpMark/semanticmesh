# AB-00 — 05_edgecases_incomplete — Run Analysis

**Timestamp:** 2026-03-27 15:42:58  
**Run tag:** `post-fix-v2`

## Configuration

| Parameter | Value |
|-----------|-------|
| Extraction model | `LLM (gpt-5.4-nano-2026-03-17)` |
| Reasoning model | `gpt-5.4-nano-2026-03-17` |
| Embedding model | `BAAI/bge-m3` |
| Retrieval mode | `hybrid` |
| Reranker | `True` |
| Reranker top_k | `12` |
| Chunk size / overlap | `256 / 32` |
| ER similarity threshold | `0.75` |

## Builder Results

| Metric | Value |
|--------|-------|
| Triplets extracted | 190 |
| Entities resolved | 87 |
| Tables parsed | 5 |
| Tables completed | 5 |

## Query Evaluation Summary

| Metric | Value |
|--------|-------|
| Questions | 20 |
| Grounded | **20/20 (100%)** |
| Avg GT Coverage | 100% |
| Avg Top Score | 0.4780 |
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
> In the business glossary (“BUSINESS GLOSSARY - Enterprise System”), a “Customer” is defined as “an individual or organization that…” but the definition is incomplete in the knowledge graph. The glossary also states that a “Client” is “a person or company that purchases goods or services,” and notes that “Client” may be used interchangeably with “Customer” in some contexts.

**Sources retrieved (12):** `Customer→CUSTOMERS`, `parent_chunk_data_dictionary.txt_1`, `parent_chunk_data_dictionary.txt_2`, `parent_chunk_data_dictionary.txt_3`, `Order and Transaction→ORDERS`, `Payment gateway response→PAYMENTS`, `parent_chunk_business_glossary.txt_0`, `Customer`

**Context previews (first 3):**

1. _Business concept 'Customer' — The table name and core identifiers/contact fields (customer_id, first/last name, email, phone) align directly to the business concept of a purchasing customer. Additiona…_

2. _DATA DICTIONARY - Enterprise Database Version: 2.1 (incomplete documentation) Last Updated: 2024-02-28 ========================================== CUSTOMERS ========================================== P…_

3. _Foreign Keys: - customer_id → CUSTOMERS(customer_id or CustomerID?) - [missing other FK definitions] ========================================== ORDER_ITEMS (or ORDER_DETAILS?) ========================…_

---

### ✅ ec_002 — What's the difference between firstName and first_name in the CUSTOMERS table?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.4278 | **Gate:** `proceed`

**Expected answer:**
> Both columns exist in the CUSTOMERS table with identical VARCHAR(50) data types. The data dictionary notes they appear to be duplicates resulting from inconsistent naming conventions (snake_case vs camelCase), but the actual usage by the application is not documented.

**System answer:**
> In the `CUSTOMERS` table, `firstName` and `first_name` are two separate columns that both represent the customer’s first name (both are `VARCHAR(50)` in the data dictionary). However, the available documentation distinguishes them only in their metadata notes: `first_name` is marked as “[appears to be duplicate]”, while the retrieved snippet does not attach any “[missing documentation]” note speci…

**Sources retrieved (12):** `Customer→CUSTOMERS`, `parent_chunk_data_dictionary.txt_1`, `parent_chunk_data_dictionary.txt_2`, `Order and Transaction→ORDERS`, `parent_chunk_data_dictionary.txt_3`, `Order Line Items→ORDER_ITEMS`, `Product Catalogue→PRODUCTS`, `Customer`

**Context previews (first 3):**

1. _Business concept 'Customer' — The table name and core identifiers/contact fields (customer_id, first/last name, email, phone) align directly to the business concept of a purchasing customer. Additiona…_

2. _DATA DICTIONARY - Enterprise Database Version: 2.1 (incomplete documentation) Last Updated: 2024-02-28 ========================================== CUSTOMERS ========================================== P…_

3. _Foreign Keys: - customer_id → CUSTOMERS(customer_id or CustomerID?) - [missing other FK definitions] ========================================== ORDER_ITEMS (or ORDER_DETAILS?) ========================…_

---

### ✅ ec_003 — Which customer column should be used as a foreign key reference: customer_id or CustomerID?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.9258 | **Gate:** `proceed`

**Expected answer:**
> The CUSTOMERS table has both customer_id (defined as PRIMARY KEY) and CustomerID (defined as INTEGER with no constraints). The ORDERS table also has both customer_id and CustomerID columns with ambiguous FK references. The data dictionary indicates this inconsistency is documented but not yet resolv…

**System answer:**
> The documentation is inconsistent about the CUSTOMER primary key name. In the `CUSTOMERS` section, the primary key is listed as `customer_id (or is it CustomerID? check with DBA)`, and there’s also a separate `CustomerID` column that “is possibly duplicate of customer_id”.

For foreign keys, the only explicit mapping note says `customer_id → CUSTOMERS(customer_id or CustomerID?)`, which means the …

**Sources retrieved (12):** `parent_chunk_data_dictionary.txt_2`, `parent_chunk_data_dictionary.txt_1`, `parent_chunk_data_dictionary.txt_3`, `Order and Transaction→ORDERS`, `Customer→CUSTOMERS`, `Payment gateway response→PAYMENTS`, `Order Line Items→ORDER_ITEMS`, `Product Catalogue→PRODUCTS`

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
> I cannot find this information in the knowledge graph.

**Sources retrieved (12):** `parent_chunk_data_dictionary.txt_3`, `Order and Transaction→ORDERS`, `parent_chunk_data_dictionary.txt_1`, `parent_chunk_data_dictionary.txt_2`, `Product Catalogue→PRODUCTS`, `parent_chunk_business_glossary.txt_0`, `Product Catalogue`, `Payment gateway response→PAYMENTS`

**Context previews (first 3):**

1. _========================================== PAYMENTS ==========================================  Primary Key: payment_id (unverified) | Column Name | Data Type | Constraints | Description | |----------…_

2. _Business concept 'Order and Transaction' is implemented by physical table ORDERS (columns: order_id, OrderID, customer_id, CustomerID, order_date, OrderDate, order_status, orderAmount, total_amount, s…_

3. _DATA DICTIONARY - Enterprise Database Version: 2.1 (incomplete documentation) Last Updated: 2024-02-28 ========================================== CUSTOMERS ========================================== P…_

---

### ✅ ec_005 — Is there a difference between Product, Item, and SKU?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.5696 | **Gate:** `proceed`

**Expected answer:**
> The glossary indicates these terms are related but distinct: Product is defined as "A thing that is... [definition needs clarification]"; Item is a synonym for Product used in inventory context; SKU (Stock Keeping Unit) is a unique identifier for a product variant; Inventory Item refers to physical …

**System answer:**
> The retrieved context describes a “Product Catalogue” (the physical table `PRODUCTS`) as master data for sellable goods, including product identifiers, names, categories, and SKU fields (e.g., `product_sku` / `sku`), along with pricing and inventory attributes (`stock_quantity`, `reorder_level`, `is_active`). However, it does not define separate business concepts for “Item” or explicitly explain h…

**Sources retrieved (12):** `Product Catalogue→PRODUCTS`, `parent_chunk_data_dictionary.txt_2`, `Order Line Items→ORDER_ITEMS`, `parent_chunk_data_dictionary.txt_1`, `parent_chunk_data_dictionary.txt_3`, `Order and Transaction→ORDERS`, `Customer→CUSTOMERS`, `parent_chunk_business_glossary.txt_0`

**Context previews (first 3):**

1. _Business concept 'Product Catalogue' — The table defines master data for sellable goods, including product identifiers, names, categories, SKU, pricing (unit/current and cost), and inventory attribute…_

2. _Foreign Keys: - customer_id → CUSTOMERS(customer_id or CustomerID?) - [missing other FK definitions] ========================================== ORDER_ITEMS (or ORDER_DETAILS?) ========================…_

3. _Business concept 'Order Line Items' — ORDER_ITEMS contains the typical order line attributes (order_item_id, order_id, product_id, quantity, unit_price, discount_percent/amount, and line_total). Altho…_

---

### ✅ ec_006 — Which table should ORDER_ITEMS.product_id reference: PRODUCTS or INVENTORY?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.9608 | **Gate:** `proceed`

**Expected answer:**
> The data dictionary states the FK reference is to 'PRODUCTS (or INVENTORY?)' and notes it is 'not verified'. The schema provides two potential targets: PRODUCTS table (which has product_id) and an INVENTORY table that is referenced in documentation but not defined in the DDL. The actual relationship…

**System answer:**
> Based on the foreign key note for `ORDER_ITEMS.product_id`, it is intended to reference `PRODUCTS` (“References PRODUCTS (or INVENTORY?)”). And the business concept “Product Catalogue” is implemented by the physical table `PRODUCTS` (it describes the product catalogue/inventory item master).  

So, the expected reference is `PRODUCTS` (even though the documentation also mentions “INVENTORY?” as an…

**Sources retrieved (12):** `parent_chunk_data_dictionary.txt_2`, `Product Catalogue→PRODUCTS`, `Order Line Items→ORDER_ITEMS`, `parent_chunk_data_dictionary.txt_3`, `parent_chunk_data_dictionary.txt_1`, `Order Line Items`, `Product Catalogue`, `parent_chunk_business_glossary.txt_0`

**Context previews (first 3):**

1. _Foreign Keys: - customer_id → CUSTOMERS(customer_id or CustomerID?) - [missing other FK definitions] ========================================== ORDER_ITEMS (or ORDER_DETAILS?) ========================…_

2. _Business concept 'Product Catalogue' — The table defines master data for sellable goods, including product identifiers, names, categories, SKU, pricing (unit/current and cost), and inventory attribute…_

3. _Business concept 'Order Line Items' — ORDER_ITEMS contains the typical order line attributes (order_item_id, order_id, product_id, quantity, unit_price, discount_percent/amount, and line_total). Altho…_

---

### ✅ ec_007 — What's the difference between Revenue and Sales?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.4224 | **Gate:** `proceed`

**Expected answer:**
> Both terms show circular definitions: Revenue is defined as 'Income from sales. The same as... [definition circular, see Sales]', while Sales is defined as 'Revenue from selling products. See Revenue.' The glossary provides no clear distinction between these concepts.

**System answer:**
> I cannot find this information in the knowledge graph.

**Sources retrieved (12):** `parent_chunk_data_dictionary.txt_2`, `Order Line Items→ORDER_ITEMS`, `Product Catalogue→PRODUCTS`, `Customer→CUSTOMERS`, `Order and Transaction→ORDERS`, `parent_chunk_data_dictionary.txt_3`, `parent_chunk_business_glossary.txt_0`, `Product Catalogue`

**Context previews (first 3):**

1. _Foreign Keys: - customer_id → CUSTOMERS(customer_id or CustomerID?) - [missing other FK definitions] ========================================== ORDER_ITEMS (or ORDER_DETAILS?) ========================…_

2. _Business concept 'Order Line Items' — ORDER_ITEMS contains the typical order line attributes (order_item_id, order_id, product_id, quantity, unit_price, discount_percent/amount, and line_total). Altho…_

3. _Business concept 'Product Catalogue' — The table defines master data for sellable goods, including product identifiers, names, categories, SKU, pricing (unit/current and cost), and inventory attribute…_

---

### ✅ ec_008 — Can one order have multiple payments?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0981 | **Gate:** `proceed_with_warning`

**Expected answer:**
> The PAYMENTS table has an order_id column, suggesting a many-to-one relationship (multiple payments can reference a single order). However, the relationship section in the glossary asks 'Or is it one-to-one?' indicating uncertainty. The ORDERS table has both payment_status and payment_method columns…

**System answer:**
> The retrieved context for the `PAYMENTS` table states that `PAYMENTS.order_id` is a foreign key referencing `ORDERS`. However, it does not document any business rule or constraint about uniqueness or cardinality of `order_id` within `PAYMENTS` (it only shows `transaction_id` as “UNIQUE?”/“External transaction reference”). Therefore, based strictly on the knowledge graph provided, we cannot confirm…

**Sources retrieved (12):** `parent_chunk_data_dictionary.txt_3`, `Order and Transaction→ORDERS`, `Payment gateway response→PAYMENTS`, `parent_chunk_data_dictionary.txt_2`, `Order Line Items→ORDER_ITEMS`, `parent_chunk_data_dictionary.txt_1`, `Product Catalogue→PRODUCTS`, `Customer→CUSTOMERS`

**Context previews (first 3):**

1. _========================================== PAYMENTS ==========================================  Primary Key: payment_id (unverified) | Column Name | Data Type | Constraints | Description | |----------…_

2. _Business concept 'Order and Transaction' is implemented by physical table ORDERS (columns: order_id, OrderID, customer_id, CustomerID, order_date, OrderDate, order_status, orderAmount, total_amount, s…_

3. _Business concept 'Payment gateway response' is implemented by physical table PAYMENTS (columns: payment_id, PaymentID, order_id, customer_id, payment_date, payment_amount, payment_method, payment_stat…_

---

### ✅ ec_009 — What payment methods are accepted?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.1791 | **Gate:** `proceed_with_warning`

**Expected answer:**
> The PAYMENTS table has a payment_method column (VARCHAR(30)), but the data dictionary notes '[missing valid values]' and no CHECK constraint exists to enumerate acceptable methods. The schema does not document what values are valid (e.g., credit_card, debit, paypal, etc.).

**System answer:**
> The retrieved context does not list the accepted/valid values for `PAYMENTS.payment_method`. It only indicates that `payment_method` has the constraint “[missing valid values]”, so the set of accepted payment methods is not provided here.

**Sources retrieved (12):** `parent_chunk_data_dictionary.txt_3`, `Payment gateway response→PAYMENTS`, `Order and Transaction→ORDERS`, `parent_chunk_data_dictionary.txt_1`, `parent_chunk_data_dictionary.txt_2`, `parent_chunk_business_glossary.txt_0`, `Payment gateway response`, `Customer→CUSTOMERS`

**Context previews (first 3):**

1. _========================================== PAYMENTS ==========================================  Primary Key: payment_id (unverified) | Column Name | Data Type | Constraints | Description | |----------…_

2. _Business concept 'Payment gateway response' is implemented by physical table PAYMENTS (columns: payment_id, PaymentID, order_id, customer_id, payment_date, payment_amount, payment_method, payment_stat…_

3. _Business concept 'Order and Transaction' is implemented by physical table ORDERS (columns: order_id, OrderID, customer_id, CustomerID, order_date, OrderDate, order_status, orderAmount, total_amount, s…_

---

### ✅ ec_010 — What's the correct table name: ORDER_ITEMS or ORDER_DETAILS?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.9722 | **Gate:** `proceed`

**Expected answer:**
> The DDL creates a table named ORDER_ITEMS, but the data dictionary header shows 'ORDER_ITEMS (or ORDER_DETAILS?)' and notes 'Table name ambiguity: ORDER_ITEMS vs ORDER_DETAILS'. The actual table name in the schema is ORDER_ITEMS, but documentation suggests the application may reference it differentl…

**System answer:**
> Based on the retrieved context for the business concept “Order Line Items,” the physical table is implemented as ORDER_ITEMS. The context also says the table is “also referenced as ORDER_DETAILS,” but that does not change the implemented table name. So the correct table name is ORDER_ITEMS.

**Sources retrieved (12):** `parent_chunk_data_dictionary.txt_2`, `Order Line Items→ORDER_ITEMS`, `Product Catalogue→PRODUCTS`, `parent_chunk_data_dictionary.txt_3`, `parent_chunk_data_dictionary.txt_1`, `Order Line Items`, `Product Catalogue`, `Customer`

**Context previews (first 3):**

1. _Foreign Keys: - customer_id → CUSTOMERS(customer_id or CustomerID?) - [missing other FK definitions] ========================================== ORDER_ITEMS (or ORDER_DETAILS?) ========================…_

2. _Business concept 'Order Line Items' — ORDER_ITEMS contains the typical order line attributes (order_item_id, order_id, product_id, quantity, unit_price, discount_percent/amount, and line_total). Altho…_

3. _Business concept 'Product Catalogue' — The table defines master data for sellable goods, including product identifiers, names, categories, SKU, pricing (unit/current and cost), and inventory attribute…_

---

### ✅ ec_011 — Which date column should be used to track when an order was created: order_date, OrderDate, or created_at?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.9218 | **Gate:** `proceed`

**Expected answer:**
> The ORDERS table has three date-related columns: order_date (DATE type), OrderDate (DATETIME type with different precision), and created_at (TIMESTAMP type). The data dictionary provides no guidance on which is actually used by the application or why three columns exist for potentially the same purp…

**System answer:**
> In the `ORDERS` table (used for the business concept “Order and Transaction”), there are multiple date/timestamp columns: `order_date`, `OrderDate`, and `created_at` (also `updated_at`).

The retrieved context does not specify which one is intended to track “when an order was created,” nor does it state the semantic difference between `order_date` vs `OrderDate` vs `created_at`. Therefore, from th…

**Sources retrieved (12):** `Order and Transaction→ORDERS`, `Payment gateway response→PAYMENTS`, `parent_chunk_data_dictionary.txt_1`, `parent_chunk_data_dictionary.txt_3`, `Customer→CUSTOMERS`, `Product Catalogue→PRODUCTS`, `Order Line Items→ORDER_ITEMS`, `parent_chunk_data_dictionary.txt_2`

**Context previews (first 3):**

1. _Business concept 'Order and Transaction' is implemented by physical table ORDERS (columns: order_id, OrderID, customer_id, CustomerID, order_date, OrderDate, order_status, orderAmount, total_amount, s…_

2. _Business concept 'Payment gateway response' is implemented by physical table PAYMENTS (columns: payment_id, PaymentID, order_id, customer_id, payment_date, payment_amount, payment_method, payment_stat…_

3. _DATA DICTIONARY - Enterprise Database Version: 2.1 (incomplete documentation) Last Updated: 2024-02-28 ========================================== CUSTOMERS ========================================== P…_

---

### ✅ ec_012 — What does the Failed order status mean?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0031 | **Gate:** `proceed_with_warning`

**Expected answer:**
> The business glossary lists Failed as an order status but marks it as '[definition missing]'. Other statuses have definitions (Pending, Processing, Completed, Cancelled, On Hold), but Failed is undefined despite being a valid status value.

**System answer:**
> The retrieved context confirms that the business concept “Order and Transaction” is implemented by the physical table `ORDERS`, which includes an `order_status` (and also `payment_status` / `payment_method`). However, the context does not define the possible values for `order_status` or specify what a status value like “Failed” means. Therefore, the meaning of “Failed” for `ORDERS.order_status` ca…

**Sources retrieved (12):** `parent_chunk_data_dictionary.txt_3`, `parent_chunk_data_dictionary.txt_1`, `Order and Transaction→ORDERS`, `parent_chunk_data_dictionary.txt_2`, `Order Line Items→ORDER_ITEMS`, `Product Catalogue→PRODUCTS`, `Customer→CUSTOMERS`, `Payment gateway response→PAYMENTS`

**Context previews (first 3):**

1. _========================================== PAYMENTS ==========================================  Primary Key: payment_id (unverified) | Column Name | Data Type | Constraints | Description | |----------…_

2. _DATA DICTIONARY - Enterprise Database Version: 2.1 (incomplete documentation) Last Updated: 2024-02-28 ========================================== CUSTOMERS ========================================== P…_

3. _Business concept 'Order and Transaction' is implemented by physical table ORDERS (columns: order_id, OrderID, customer_id, CustomerID, order_date, OrderDate, order_status, orderAmount, total_amount, s…_

---

### ✅ ec_013 — Are there any NOT NULL constraints defined in the schema?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.7628 | **Gate:** `proceed`

**Expected answer:**
> No NOT NULL constraints are defined in the DDL. The data dictionary explicitly states 'NOT NULL constraints not defined' under 'Missing Documentation' and notes 'assumed, not verified'. All columns are nullable by default.

**System answer:**
> In the retrieved schema documentation for tables like `PAYMENTS`, `ORDER_ITEMS` (or `ORDER_DETAILS`), `CUSTOMERS`, and the conceptual mappings to `ORDERS`/`PRODUCTS`, the listed constraints mention primary keys (e.g., `payment_id` as PK), foreign keys, and possibly uniqueness (e.g., `transaction_id` as “UNIQUE?”), but there is no indication of any `NOT NULL` constraints.

**Sources retrieved (12):** `parent_chunk_data_dictionary.txt_3`, `parent_chunk_data_dictionary.txt_2`, `parent_chunk_data_dictionary.txt_1`, `Order Line Items→ORDER_ITEMS`, `Order and Transaction→ORDERS`, `parent_chunk_business_glossary.txt_0`, `Order Line Items`, `Product Catalogue→PRODUCTS`

**Context previews (first 3):**

1. _========================================== PAYMENTS ==========================================  Primary Key: payment_id (unverified) | Column Name | Data Type | Constraints | Description | |----------…_

2. _Foreign Keys: - customer_id → CUSTOMERS(customer_id or CustomerID?) - [missing other FK definitions] ========================================== ORDER_ITEMS (or ORDER_DETAILS?) ========================…_

3. _DATA DICTIONARY - Enterprise Database Version: 2.1 (incomplete documentation) Last Updated: 2024-02-28 ========================================== CUSTOMERS ========================================== P…_

---

### ✅ ec_014 — What's the difference between unit_price and current_price in PRODUCTS?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.6518 | **Gate:** `proceed`

**Expected answer:**
> The PRODUCTS table has both unit_price and current_price columns (both DECIMAL(10,2)). The data dictionary asks 'Different from unit_price?' but provides no explanation of the distinction or when each would be used.

**System answer:**
> In the `PRODUCTS` table (business concept `Product Catalogue`), `unit_price` and `current_price` are both pricing attributes for sellable goods, alongside `cost_price` and inventory fields like `stock_quantity` and `reorder_level`. The retrieved context does not define the specific business meaning or calculation difference between `unit_price` and `current_price`; it only states that the table in…

**Sources retrieved (12):** `Product Catalogue→PRODUCTS`, `Order Line Items→ORDER_ITEMS`, `parent_chunk_data_dictionary.txt_2`, `parent_chunk_data_dictionary.txt_3`, `Order and Transaction→ORDERS`, `Customer→CUSTOMERS`, `Product Catalogue`, `Order Line Items`

**Context previews (first 3):**

1. _Business concept 'Product Catalogue' — The table defines master data for sellable goods, including product identifiers, names, categories, SKU, pricing (unit/current and cost), and inventory attribute…_

2. _Business concept 'Order Line Items' — ORDER_ITEMS contains the typical order line attributes (order_item_id, order_id, product_id, quantity, unit_price, discount_percent/amount, and line_total). Altho…_

3. _Foreign Keys: - customer_id → CUSTOMERS(customer_id or CustomerID?) - [missing other FK definitions] ========================================== ORDER_ITEMS (or ORDER_DETAILS?) ========================…_

---

### ✅ ec_015 — When is an invoice generated vs payment processed?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.6598 | **Gate:** `proceed`

**Expected answer:**
> The relationship section in the glossary asks 'An invoice is generated for an order. But when? And can one order have multiple invoices?' indicating the timing and cardinality are not defined. The glossary defines Invoice as 'A document requesting payment. Related to Bill' and Payment as 'The transf…

**System answer:**
> The knowledge graph content you provided does not define any business concept or table for “invoice generation,” nor does it state when an invoice is generated.

What it does show is when a payment is processed in the physical table PAYMENTS (business concept “Payment gateway response” is implemented by PAYMENTS). In PAYMENTS, the “payment processed” timestamp would correspond to the column paymen…

**Sources retrieved (12):** `parent_chunk_data_dictionary.txt_3`, `parent_chunk_data_dictionary.txt_1`, `parent_chunk_data_dictionary.txt_2`, `Payment gateway response→PAYMENTS`, `Order and Transaction→ORDERS`, `parent_chunk_business_glossary.txt_0`, `Payment gateway response`, `Order Line Items→ORDER_ITEMS`

**Context previews (first 3):**

1. _========================================== PAYMENTS ==========================================  Primary Key: payment_id (unverified) | Column Name | Data Type | Constraints | Description | |----------…_

2. _DATA DICTIONARY - Enterprise Database Version: 2.1 (incomplete documentation) Last Updated: 2024-02-28 ========================================== CUSTOMERS ========================================== P…_

3. _Foreign Keys: - customer_id → CUSTOMERS(customer_id or CustomerID?) - [missing other FK definitions] ========================================== ORDER_ITEMS (or ORDER_DETAILS?) ========================…_

---

### ✅ ec_016 — Is the sku column in PRODUCTS unique?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.4300 | **Gate:** `proceed`

**Expected answer:**
> The PRODUCTS table has both product_sku and sku columns. The data dictionary notes sku 'should be UNIQUE?' but the DDL does not define a UNIQUE constraint on either column. No index is documented for these columns.

**System answer:**
> The retrieved context for the `PRODUCTS` table lists SKU-related columns (`product_sku` and `sku`) as part of the product catalogue master data, but it does not state any uniqueness constraint for `sku` (or `product_sku`). Therefore, the uniqueness of the `sku` column cannot be confirmed from the knowledge graph.

**Sources retrieved (12):** `Product Catalogue→PRODUCTS`, `parent_chunk_data_dictionary.txt_2`, `parent_chunk_data_dictionary.txt_3`, `Order Line Items→ORDER_ITEMS`, `parent_chunk_data_dictionary.txt_1`, `Customer→CUSTOMERS`, `Order and Transaction→ORDERS`, `Payment gateway response→PAYMENTS`

**Context previews (first 3):**

1. _Business concept 'Product Catalogue' — The table defines master data for sellable goods, including product identifiers, names, categories, SKU, pricing (unit/current and cost), and inventory attribute…_

2. _Foreign Keys: - customer_id → CUSTOMERS(customer_id or CustomerID?) - [missing other FK definitions] ========================================== ORDER_ITEMS (or ORDER_DETAILS?) ========================…_

3. _========================================== PAYMENTS ==========================================  Primary Key: payment_id (unverified) | Column Name | Data Type | Constraints | Description | |----------…_

---

### ✅ ec_017 — What is the relationship between customers and orders?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0859 | **Gate:** `proceed_with_warning`

**Expected answer:**
> The glossary states 'A customer can place multiple orders. Or is it accounts that place orders?' indicating uncertainty about the relationship. The ORDERS table has both customer_id and CustomerID columns with ambiguous FK references, and the data dictionary notes they reference 'customer (which tab…

**System answer:**
> In the retrieved context, the relationship between customers and orders is expressed via the `customer_id` foreign key in the `ORDERS` table. Specifically, the `ORDERS` table is implemented for the business concept “Order and Transaction” and includes `customer_id` / `CustomerID` as a customer identifier. The context also states that `customer_id` is a foreign key “→ CUSTOMERS(customer_id or Custo…

**Sources retrieved (12):** `parent_chunk_data_dictionary.txt_3`, `Order and Transaction→ORDERS`, `parent_chunk_data_dictionary.txt_2`, `parent_chunk_data_dictionary.txt_1`, `Customer→CUSTOMERS`, `Order Line Items→ORDER_ITEMS`, `Product Catalogue→PRODUCTS`, `parent_chunk_business_glossary.txt_0`

**Context previews (first 3):**

1. _========================================== PAYMENTS ==========================================  Primary Key: payment_id (unverified) | Column Name | Data Type | Constraints | Description | |----------…_

2. _Business concept 'Order and Transaction' is implemented by physical table ORDERS (columns: order_id, OrderID, customer_id, CustomerID, order_date, OrderDate, order_status, orderAmount, total_amount, s…_

3. _Foreign Keys: - customer_id → CUSTOMERS(customer_id or CustomerID?) - [missing other FK definitions] ========================================== ORDER_ITEMS (or ORDER_DETAILS?) ========================…_

---

### ✅ ec_018 — Which price column represents what the customer actually pays?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0581 | **Gate:** `proceed_with_warning`

**Expected answer:**
> Multiple price columns exist across tables: ORDERS has orderAmount and total_amount; ORDER_ITEMS has unit_price and UnitPrice; PRODUCTS has unit_price, current_price, and cost_price. The data dictionary does not explain which represents the final customer price, whether discounts are applied, or how…

**System answer:**
> The retrieved context does not explicitly state which specific column represents “what the customer actually pays,” nor does it define any comparison between `ORDERS` and `PAYMENTS` amounts.

What the knowledge graph *does* show is that the price-related columns present are:
`PAYMENTS.payment_amount` (in table `PAYMENTS`, described only with “[missing documentation]” and associated to the business…

**Sources retrieved (12):** `Payment gateway response→PAYMENTS`, `Order and Transaction→ORDERS`, `parent_chunk_data_dictionary.txt_2`, `parent_chunk_data_dictionary.txt_3`, `Order Line Items→ORDER_ITEMS`, `parent_chunk_data_dictionary.txt_1`, `Customer→CUSTOMERS`, `Product Catalogue→PRODUCTS`

**Context previews (first 3):**

1. _Business concept 'Payment gateway response' is implemented by physical table PAYMENTS (columns: payment_id, PaymentID, order_id, customer_id, payment_date, payment_amount, payment_method, payment_stat…_

2. _Business concept 'Order and Transaction' is implemented by physical table ORDERS (columns: order_id, OrderID, customer_id, CustomerID, order_date, OrderDate, order_status, orderAmount, total_amount, s…_

3. _Foreign Keys: - customer_id → CUSTOMERS(customer_id or CustomerID?) - [missing other FK definitions] ========================================== ORDER_ITEMS (or ORDER_DETAILS?) ========================…_

---

### ✅ ec_019 — What's the difference between Shipment, Delivery, and Fulfillment?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0050 | **Gate:** `proceed_with_warning`

**Expected answer:**
> The glossary provides definitions but unclear boundaries: Shipment is 'The process of delivering goods to a customer'; Delivery is 'The completion of a Shipment when goods reach the customer'; Fulfillment is 'The process of preparing and delivering orders. Encompasses Shipment and Delivery.' The exa…

**System answer:**
> I cannot find this information in the knowledge graph.

**Sources retrieved (12):** `parent_chunk_data_dictionary.txt_2`, `Order and Transaction→ORDERS`, `Order Line Items→ORDER_ITEMS`, `parent_chunk_data_dictionary.txt_3`, `Product Catalogue→PRODUCTS`, `Customer→CUSTOMERS`, `parent_chunk_business_glossary.txt_0`, `Order and Transaction`

**Context previews (first 3):**

1. _Foreign Keys: - customer_id → CUSTOMERS(customer_id or CustomerID?) - [missing other FK definitions] ========================================== ORDER_ITEMS (or ORDER_DETAILS?) ========================…_

2. _Business concept 'Order and Transaction' is implemented by physical table ORDERS (columns: order_id, OrderID, customer_id, CustomerID, order_date, OrderDate, order_status, orderAmount, total_amount, s…_

3. _Business concept 'Order Line Items' — ORDER_ITEMS contains the typical order line attributes (order_item_id, order_id, product_id, quantity, unit_price, discount_percent/amount, and line_total). Altho…_

---

### ✅ ec_020 — Are foreign key constraints enforced in the schema?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.1603 | **Gate:** `proceed_with_warning`

**Expected answer:**
> No foreign key constraints are enforced in the DDL. While the data dictionary documents FK relationships (e.g., customer_id → CUSTOMERS, order_id → ORDERS), the actual CREATE TABLE statements omit the REFERENCES clauses. The schema explicitly notes 'FK constraints defined in data dictionary but not …

**System answer:**
> The retrieved documentation shows foreign key definitions, but it does not state whether they are enforced as constraints in the schema.

For example, in `ORDER_ITEMS`, `order_id` is described as an FK referencing `ORDERS`, and `product_id` is described as an FK referencing `PRODUCTS` (with inconsistent naming also noted). In `PAYMENTS`, `order_id` is described as an FK referencing `ORDERS`, and `…

**Sources retrieved (12):** `parent_chunk_data_dictionary.txt_2`, `parent_chunk_data_dictionary.txt_3`, `parent_chunk_data_dictionary.txt_1`, `parent_chunk_business_glossary.txt_0`, `Payment gateway response→PAYMENTS`, `Order and Transaction→ORDERS`, `Customer→CUSTOMERS`, `Order Line Items→ORDER_ITEMS`

**Context previews (first 3):**

1. _Foreign Keys: - customer_id → CUSTOMERS(customer_id or CustomerID?) - [missing other FK definitions] ========================================== ORDER_ITEMS (or ORDER_DETAILS?) ========================…_

2. _========================================== PAYMENTS ==========================================  Primary Key: payment_id (unverified) | Column Name | Data Type | Constraints | Description | |----------…_

3. _DATA DICTIONARY - Enterprise Database Version: 2.1 (incomplete documentation) Last Updated: 2024-02-28 ========================================== CUSTOMERS ========================================== P…_

---

## Anomalies & Observations

No anomalies detected. All questions grounded with acceptable RAGAS scores.
