# AB-00 — 05_edgecases_incomplete — Run Analysis

**Timestamp:** 2026-03-27 18:21:52  
**Run tag:** `post-fix-v3`

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
| Triplets extracted | 168 |
| Entities resolved | 82 |
| Tables parsed | 5 |
| Tables completed | 5 |

## Query Evaluation Summary

| Metric | Value |
|--------|-------|
| Questions | 20 |
| Grounded | **20/20 (100%)** |
| Avg GT Coverage | 100% |
| Avg Top Score | 0.4803 |
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
> In the business glossary (“BUSINESS GLOSSARY - Enterprise System”), a Customer is defined as “An individual or organization that...”, but the definition is incomplete in the retrieved context. The glossary also defines a “Client” as “a person or company that purchases goods or services” and notes that Client may be used interchangeably with Customer in some contexts.

**Sources retrieved (12):** `parent_chunk_data_dictionary.txt_1`, `parent_chunk_data_dictionary.txt_2`, `Sales Order→ORDERS`, `parent_chunk_data_dictionary.txt_3`, `Receipt→PAYMENTS`, `parent_chunk_business_glossary.txt_0`, `Inventory Items→PRODUCTS`, `BusinessConcept→PhysicalTable`

**Context previews (first 3):**

1. _DATA DICTIONARY - Enterprise Database Version: 2.1 (incomplete documentation) Last Updated: 2024-02-28 ========================================== CUSTOMERS ========================================== P…_

2. _Foreign Keys: - customer_id → CUSTOMERS(customer_id or CustomerID?) - [missing other FK definitions] ========================================== ORDER_ITEMS (or ORDER_DETAILS?) ========================…_

3. _Business concept 'Sales Order' — The table models the core header of an order with a unique order identifier, order date, order status, pricing totals (orderAmount/total_amount, shippingAmount, tax_am…_

---

### ✅ ec_002 — What's the difference between firstName and first_name in the CUSTOMERS table?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.3978 | **Gate:** `proceed`

**Expected answer:**
> Both columns exist in the CUSTOMERS table with identical VARCHAR(50) data types. The data dictionary notes they appear to be duplicates resulting from inconsistent naming conventions (snake_case vs camelCase), but the actual usage by the application is not documented.

**System answer:**
> In the `CUSTOMERS` table, `firstName` and `first_name` both exist and are both defined as `VARCHAR(50)`. 

`firstName` is described as “Customer’s first name.” For `first_name`, the documentation is missing/unclear and it is marked as “appears to be duplicate” (i.e., possibly an alternate or redundant representation of the same value). The retrieved context does not specify any authoritative rule …

**Sources retrieved (12):** `parent_chunk_data_dictionary.txt_1`, `parent_chunk_data_dictionary.txt_2`, `Sales Order→ORDERS`, `parent_chunk_data_dictionary.txt_3`, `Inventory Items→PRODUCTS`, `Order Line Items→ORDER_ITEMS`, `parent_chunk_business_glossary.txt_0`, `Sales Order`

**Context previews (first 3):**

1. _DATA DICTIONARY - Enterprise Database Version: 2.1 (incomplete documentation) Last Updated: 2024-02-28 ========================================== CUSTOMERS ========================================== P…_

2. _Foreign Keys: - customer_id → CUSTOMERS(customer_id or CustomerID?) - [missing other FK definitions] ========================================== ORDER_ITEMS (or ORDER_DETAILS?) ========================…_

3. _Business concept 'Sales Order' — The table models the core header of an order with a unique order identifier, order date, order status, pricing totals (orderAmount/total_amount, shippingAmount, tax_am…_

---

### ✅ ec_003 — Which customer column should be used as a foreign key reference: customer_id or CustomerID?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.9258 | **Gate:** `proceed`

**Expected answer:**
> The CUSTOMERS table has both customer_id (defined as PRIMARY KEY) and CustomerID (defined as INTEGER with no constraints). The ORDERS table also has both customer_id and CustomerID columns with ambiguous FK references. The data dictionary indicates this inconsistency is documented but not yet resolv…

**System answer:**
> The retrieved context is ambiguous about which `CUSTOMERS` key column is referenced. In the “Foreign Keys” section, it only states `customer_id → CUSTOMERS(customer_id or CustomerID?)`, and in the “CUSTOMERS” table it says the primary key is `customer_id (or is it CustomerID? check with DBA)`. Therefore, based on the knowledge graph alone, you cannot confirm whether the FK should reference `CUSTOM…

**Sources retrieved (12):** `parent_chunk_data_dictionary.txt_2`, `parent_chunk_data_dictionary.txt_1`, `parent_chunk_data_dictionary.txt_3`, `Sales Order→ORDERS`, `Receipt→PAYMENTS`, `Inventory Items→PRODUCTS`, `Order Line Items→ORDER_ITEMS`, `parent_chunk_business_glossary.txt_0`

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

**Sources retrieved (12):** `parent_chunk_data_dictionary.txt_3`, `Sales Order→ORDERS`, `parent_chunk_data_dictionary.txt_1`, `parent_chunk_data_dictionary.txt_2`, `Inventory Items→PRODUCTS`, `parent_chunk_business_glossary.txt_0`, `Inventory Items`, `Receipt→PAYMENTS`

**Context previews (first 3):**

1. _========================================== PAYMENTS ==========================================  Primary Key: payment_id (unverified) | Column Name | Data Type | Constraints | Description | |----------…_

2. _Business concept 'Sales Order' — The table models the core header of an order with a unique order identifier, order date, order status, pricing totals (orderAmount/total_amount, shippingAmount, tax_am…_

3. _DATA DICTIONARY - Enterprise Database Version: 2.1 (incomplete documentation) Last Updated: 2024-02-28 ========================================== CUSTOMERS ========================================== P…_

---

### ✅ ec_005 — Is there a difference between Product, Item, and SKU?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.5696 | **Gate:** `proceed`

**Expected answer:**
> The glossary indicates these terms are related but distinct: Product is defined as "A thing that is... [definition needs clarification]"; Item is a synonym for Product used in inventory context; SKU (Stock Keeping Unit) is a unique identifier for a product variant; Inventory Item refers to physical …

**System answer:**
> The retrieved context does not define separate business meanings for “Product” versus “Item” versus “SKU” in a way that lets me state a clear, formal difference between all three.

What it does show is:

“Inventory Items” is described as product/master data used for sale and inventory control, and it is implemented by the physical table PRODUCTS. That mapping includes multiple product identifiers …

**Sources retrieved (12):** `Inventory Items→PRODUCTS`, `parent_chunk_data_dictionary.txt_2`, `Order Line Items→ORDER_ITEMS`, `parent_chunk_data_dictionary.txt_1`, `parent_chunk_data_dictionary.txt_3`, `Sales Order→ORDERS`, `parent_chunk_business_glossary.txt_0`, `Inventory Items`

**Context previews (first 3):**

1. _Business concept 'Inventory Items' — The table stores product/master data used for sale and inventory control, including product identifiers (product_id), SKU, pricing (unit_price/current_price/cost_p…_

2. _Foreign Keys: - customer_id → CUSTOMERS(customer_id or CustomerID?) - [missing other FK definitions] ========================================== ORDER_ITEMS (or ORDER_DETAILS?) ========================…_

3. _Business concept 'Order Line Items' — The table name and structure (order_item_id, order_id, product_id, quantity, unit_price, discount, line_total) align directly with storing individual items/lines …_

---

### ✅ ec_006 — Which table should ORDER_ITEMS.product_id reference: PRODUCTS or INVENTORY?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.9608 | **Gate:** `proceed`

**Expected answer:**
> The data dictionary states the FK reference is to 'PRODUCTS (or INVENTORY?)' and notes it is 'not verified'. The schema provides two potential targets: PRODUCTS table (which has product_id) and an INVENTORY table that is referenced in documentation but not defined in the DDL. The actual relationship…

**System answer:**
> In the retrieved context for `ORDER_ITEMS`, the foreign key note on `product_id` is not definitive: it states `product_id → References PRODUCTS (or INVENTORY?)`. So from the schema metadata provided, the referenced table for `ORDER_ITEMS.product_id` is ambiguous between `PRODUCTS` and `INVENTORY`.

What we can say from the business-concept mapping is that the business concept “Inventory Items” is …

**Sources retrieved (12):** `parent_chunk_data_dictionary.txt_2`, `Inventory Items→PRODUCTS`, `Order Line Items→ORDER_ITEMS`, `parent_chunk_data_dictionary.txt_3`, `parent_chunk_data_dictionary.txt_1`, `Inventory Items`, `Order Line Items`, `parent_chunk_business_glossary.txt_0`

**Context previews (first 3):**

1. _Foreign Keys: - customer_id → CUSTOMERS(customer_id or CustomerID?) - [missing other FK definitions] ========================================== ORDER_ITEMS (or ORDER_DETAILS?) ========================…_

2. _Business concept 'Inventory Items' — The table stores product/master data used for sale and inventory control, including product identifiers (product_id), SKU, pricing (unit_price/current_price/cost_p…_

3. _Business concept 'Order Line Items' — The table name and structure (order_item_id, order_id, product_id, quantity, unit_price, discount, line_total) align directly with storing individual items/lines …_

---

### ✅ ec_007 — What's the difference between Revenue and Sales?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.4224 | **Gate:** `proceed`

**Expected answer:**
> Both terms show circular definitions: Revenue is defined as 'Income from sales. The same as... [definition circular, see Sales]', while Sales is defined as 'Revenue from selling products. See Revenue.' The glossary provides no clear distinction between these concepts.

**System answer:**
> The retrieved context does not include any definitions, attributes, or business glossary entries for “Revenue” versus “Sales,” nor does it describe how they differ. What is available are schema/concept mappings for “Sales Order” (table `ORDERS`) and “Order Line Items” (table `ORDER_ITEMS`), but there is no information in the provided context that explicitly defines or compares Revenue to Sales.

**Sources retrieved (12):** `Inventory Items→PRODUCTS`, `Sales Order→ORDERS`, `parent_chunk_data_dictionary.txt_2`, `Order Line Items→ORDER_ITEMS`, `parent_chunk_data_dictionary.txt_3`, `parent_chunk_business_glossary.txt_0`, `Sales Order`, `Inventory Items`

**Context previews (first 3):**

1. _Business concept 'Inventory Items' — The table stores product/master data used for sale and inventory control, including product identifiers (product_id), SKU, pricing (unit_price/current_price/cost_p…_

2. _Business concept 'Sales Order' — The table models the core header of an order with a unique order identifier, order date, order status, pricing totals (orderAmount/total_amount, shippingAmount, tax_am…_

3. _Foreign Keys: - customer_id → CUSTOMERS(customer_id or CustomerID?) - [missing other FK definitions] ========================================== ORDER_ITEMS (or ORDER_DETAILS?) ========================…_

---

### ✅ ec_008 — Can one order have multiple payments?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0981 | **Gate:** `proceed_with_warning`

**Expected answer:**
> The PAYMENTS table has an order_id column, suggesting a many-to-one relationship (multiple payments can reference a single order). However, the relationship section in the glossary asks 'Or is it one-to-one?' indicating uncertainty. The ORDERS table has both payment_status and payment_method columns…

**System answer:**
> The retrieved context shows that the `PAYMENTS` table includes `order_id` as a foreign key referencing `ORDERS`, but it does not specify the relationship cardinality between `ORDERS` and `PAYMENTS` (for example, whether `order_id` is unique in `PAYMENTS` or whether multiple `PAYMENTS` rows can share the same `order_id`).

So, based strictly on the knowledge graph provided, it is uncertain whether …

**Sources retrieved (12):** `parent_chunk_data_dictionary.txt_3`, `Sales Order→ORDERS`, `Receipt→PAYMENTS`, `parent_chunk_data_dictionary.txt_2`, `Order Line Items→ORDER_ITEMS`, `parent_chunk_data_dictionary.txt_1`, `Inventory Items→PRODUCTS`, `parent_chunk_business_glossary.txt_0`

**Context previews (first 3):**

1. _========================================== PAYMENTS ==========================================  Primary Key: payment_id (unverified) | Column Name | Data Type | Constraints | Description | |----------…_

2. _Business concept 'Sales Order' — The table models the core header of an order with a unique order identifier, order date, order status, pricing totals (orderAmount/total_amount, shippingAmount, tax_am…_

3. _Business concept 'Receipt' is implemented by physical table PAYMENTS (columns: payment_id, PaymentID, order_id, customer_id, payment_date, payment_amount, payment_method, payment_status, transaction_i…_

---

### ✅ ec_009 — What payment methods are accepted?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.1791 | **Gate:** `proceed_with_warning`

**Expected answer:**
> The PAYMENTS table has a payment_method column (VARCHAR(30)), but the data dictionary notes '[missing valid values]' and no CHECK constraint exists to enumerate acceptable methods. The schema does not document what values are valid (e.g., credit_card, debit, paypal, etc.).

**System answer:**
> I cannot find this information in the knowledge graph.

**Sources retrieved (12):** `parent_chunk_data_dictionary.txt_3`, `Sales Order→ORDERS`, `Receipt→PAYMENTS`, `parent_chunk_data_dictionary.txt_1`, `parent_chunk_data_dictionary.txt_2`, `Sales Order`, `parent_chunk_business_glossary.txt_0`, `Order Line Items→ORDER_ITEMS`

**Context previews (first 3):**

1. _========================================== PAYMENTS ==========================================  Primary Key: payment_id (unverified) | Column Name | Data Type | Constraints | Description | |----------…_

2. _Business concept 'Sales Order' — The table models the core header of an order with a unique order identifier, order date, order status, pricing totals (orderAmount/total_amount, shippingAmount, tax_am…_

3. _Business concept 'Receipt' is implemented by physical table PAYMENTS (columns: payment_id, PaymentID, order_id, customer_id, payment_date, payment_amount, payment_method, payment_status, transaction_i…_

---

### ✅ ec_010 — What's the correct table name: ORDER_ITEMS or ORDER_DETAILS?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.9627 | **Gate:** `proceed`

**Expected answer:**
> The DDL creates a table named ORDER_ITEMS, but the data dictionary header shows 'ORDER_ITEMS (or ORDER_DETAILS?)' and notes 'Table name ambiguity: ORDER_ITEMS vs ORDER_DETAILS'. The actual table name in the schema is ORDER_ITEMS, but documentation suggests the application may reference it differentl…

**System answer:**
> The retrieved data dictionary indicates the physical table for the “Order Line Items” concept is primarily implemented as `ORDER_ITEMS` (see Business concept mapping in context [2], which states “is implemented by physical table ORDER_ITEMS”). 

However, one schema section also labels it as “`ORDER_ITEMS` (or `ORDER_DETAILS`?)” (context [1]), which means `ORDER_DETAILS` is mentioned only as a poss…

**Sources retrieved (12):** `parent_chunk_data_dictionary.txt_2`, `Order Line Items→ORDER_ITEMS`, `Inventory Items→PRODUCTS`, `parent_chunk_data_dictionary.txt_3`, `parent_chunk_data_dictionary.txt_1`, `Order Line Items`, `Sales Order→ORDERS`, `Receipt→PAYMENTS`

**Context previews (first 3):**

1. _Foreign Keys: - customer_id → CUSTOMERS(customer_id or CustomerID?) - [missing other FK definitions] ========================================== ORDER_ITEMS (or ORDER_DETAILS?) ========================…_

2. _Business concept 'Order Line Items' — The table name and structure (order_item_id, order_id, product_id, quantity, unit_price, discount, line_total) align directly with storing individual items/lines …_

3. _Business concept 'Inventory Items' — The table stores product/master data used for sale and inventory control, including product identifiers (product_id), SKU, pricing (unit_price/current_price/cost_p…_

---

### ✅ ec_011 — Which date column should be used to track when an order was created: order_date, OrderDate, or created_at?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.7889 | **Gate:** `proceed`

**Expected answer:**
> The ORDERS table has three date-related columns: order_date (DATE type), OrderDate (DATETIME type with different precision), and created_at (TIMESTAMP type). The data dictionary provides no guidance on which is actually used by the application or why three columns exist for potentially the same purp…

**System answer:**
> For the business concept “Sales Order” in table **ORDERS**, the context explicitly documents **order_date / OrderDate** as the order’s “order date” attribute. The context also shows a **created_at** column in **ORDERS**, but it does not define what **created_at** represents (e.g., whether it means the moment the order record was created in the system).  

Because the meaning of **created_at** is n…

**Sources retrieved (12):** `Sales Order→ORDERS`, `Receipt→PAYMENTS`, `parent_chunk_data_dictionary.txt_1`, `parent_chunk_data_dictionary.txt_3`, `Inventory Items→PRODUCTS`, `Order Line Items→ORDER_ITEMS`, `parent_chunk_data_dictionary.txt_2`, `Sales Order`

**Context previews (first 3):**

1. _Business concept 'Sales Order' — The table models the core header of an order with a unique order identifier, order date, order status, pricing totals (orderAmount/total_amount, shippingAmount, tax_am…_

2. _Business concept 'Receipt' is implemented by physical table PAYMENTS (columns: payment_id, PaymentID, order_id, customer_id, payment_date, payment_amount, payment_method, payment_status, transaction_i…_

3. _DATA DICTIONARY - Enterprise Database Version: 2.1 (incomplete documentation) Last Updated: 2024-02-28 ========================================== CUSTOMERS ========================================== P…_

---

### ✅ ec_012 — What does the Failed order status mean?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0031 | **Gate:** `proceed_with_warning`

**Expected answer:**
> The business glossary lists Failed as an order status but marks it as '[definition missing]'. Other statuses have definitions (Pending, Processing, Completed, Cancelled, On Hold), but Failed is undefined despite being a valid status value.

**System answer:**
> The context provided states that the **Sales Order** concept is implemented by the physical table **ORDERS**, which includes an **order_status** column. However, it does not list any possible **order_status** values or define what a value like **“Failed”** would mean. Therefore, the meaning of a **Failed** order status is not specified in the available information.

**Sources retrieved (12):** `Sales Order→ORDERS`, `parent_chunk_data_dictionary.txt_3`, `parent_chunk_data_dictionary.txt_1`, `parent_chunk_data_dictionary.txt_2`, `Inventory Items→PRODUCTS`, `Order Line Items→ORDER_ITEMS`, `Receipt→PAYMENTS`, `parent_chunk_business_glossary.txt_0`

**Context previews (first 3):**

1. _Business concept 'Sales Order' — The table models the core header of an order with a unique order identifier, order date, order status, pricing totals (orderAmount/total_amount, shippingAmount, tax_am…_

2. _========================================== PAYMENTS ==========================================  Primary Key: payment_id (unverified) | Column Name | Data Type | Constraints | Description | |----------…_

3. _DATA DICTIONARY - Enterprise Database Version: 2.1 (incomplete documentation) Last Updated: 2024-02-28 ========================================== CUSTOMERS ========================================== P…_

---

### ✅ ec_013 — Are there any NOT NULL constraints defined in the schema?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.7628 | **Gate:** `proceed`

**Expected answer:**
> No NOT NULL constraints are defined in the DDL. The data dictionary explicitly states 'NOT NULL constraints not defined' under 'Missing Documentation' and notes 'assumed, not verified'. All columns are nullable by default.

**System answer:**
> The retrieved context does not define any explicit `NOT NULL` constraints for any schema elements. For the tables shown (notably `PAYMENTS`, `ORDER_ITEMS` / `ORDER_DETAILS?`, `CUSTOMERS`, and `ORDERS` via concept mapping), the “Constraints” information is marked as “[missing documentation]” or uses “?” placeholders (and for some fields it notes things like “PK”, “FK”, or “UNIQUE?”), but there is n…

**Sources retrieved (12):** `parent_chunk_data_dictionary.txt_3`, `parent_chunk_data_dictionary.txt_2`, `parent_chunk_data_dictionary.txt_1`, `Sales Order→ORDERS`, `parent_chunk_business_glossary.txt_0`, `Inventory Items→PRODUCTS`, `Order Line Items→ORDER_ITEMS`, `Receipt→PAYMENTS`

**Context previews (first 3):**

1. _========================================== PAYMENTS ==========================================  Primary Key: payment_id (unverified) | Column Name | Data Type | Constraints | Description | |----------…_

2. _Foreign Keys: - customer_id → CUSTOMERS(customer_id or CustomerID?) - [missing other FK definitions] ========================================== ORDER_ITEMS (or ORDER_DETAILS?) ========================…_

3. _DATA DICTIONARY - Enterprise Database Version: 2.1 (incomplete documentation) Last Updated: 2024-02-28 ========================================== CUSTOMERS ========================================== P…_

---

### ✅ ec_014 — What's the difference between unit_price and current_price in PRODUCTS?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.8065 | **Gate:** `proceed`

**Expected answer:**
> The PRODUCTS table has both unit_price and current_price columns (both DECIMAL(10,2)). The data dictionary asks 'Different from unit_price?' but provides no explanation of the distinction or when each would be used.

**System answer:**
> In the retrieved context for the business concept “Inventory Items” (implemented by physical table `PRODUCTS`), both `unit_price` and `current_price` are present as separate pricing columns alongside `cost_price`, but the context does not explain what distinguishes `unit_price` from `current_price` (e.g., whether one is historical/base price and the other is the latest price).

So, the only facts …

**Sources retrieved (12):** `Inventory Items→PRODUCTS`, `parent_chunk_data_dictionary.txt_2`, `Order Line Items→ORDER_ITEMS`, `Sales Order→ORDERS`, `parent_chunk_data_dictionary.txt_3`, `Inventory Items`, `Order Line Items`, `parent_chunk_business_glossary.txt_0`

**Context previews (first 3):**

1. _Business concept 'Inventory Items' — The table stores product/master data used for sale and inventory control, including product identifiers (product_id), SKU, pricing (unit_price/current_price/cost_p…_

2. _Foreign Keys: - customer_id → CUSTOMERS(customer_id or CustomerID?) - [missing other FK definitions] ========================================== ORDER_ITEMS (or ORDER_DETAILS?) ========================…_

3. _Business concept 'Order Line Items' — The table name and structure (order_item_id, order_id, product_id, quantity, unit_price, discount, line_total) align directly with storing individual items/lines …_

---

### ✅ ec_015 — When is an invoice generated vs payment processed?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.6598 | **Gate:** `proceed`

**Expected answer:**
> The relationship section in the glossary asks 'An invoice is generated for an order. But when? And can one order have multiple invoices?' indicating the timing and cardinality are not defined. The glossary defines Invoice as 'A document requesting payment. Related to Bill' and Payment as 'The transf…

**System answer:**
> In the retrieved context, there is no business concept or rule that describes “invoice generation,” nor any table labeled for invoices. The retrieved context does define payment/receipt-related concepts instead: “Business concept ‘Receipt’ is implemented by physical table PAYMENTS,” and PAYMENTS includes fields such as payment_date, payment_status, payment_method, and transaction_id (plus response…

**Sources retrieved (12):** `Order Line Items→ORDER_ITEMS`, `parent_chunk_data_dictionary.txt_3`, `Sales Order→ORDERS`, `parent_chunk_data_dictionary.txt_1`, `parent_chunk_data_dictionary.txt_2`, `Receipt→PAYMENTS`, `parent_chunk_business_glossary.txt_0`, `Order Line Items`

**Context previews (first 3):**

1. _Business concept 'Order Line Items' — The table name and structure (order_item_id, order_id, product_id, quantity, unit_price, discount, line_total) align directly with storing individual items/lines …_

2. _========================================== PAYMENTS ==========================================  Primary Key: payment_id (unverified) | Column Name | Data Type | Constraints | Description | |----------…_

3. _Business concept 'Sales Order' — The table models the core header of an order with a unique order identifier, order date, order status, pricing totals (orderAmount/total_amount, shippingAmount, tax_am…_

---

### ✅ ec_016 — Is the sku column in PRODUCTS unique?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.4820 | **Gate:** `proceed`

**Expected answer:**
> The PRODUCTS table has both product_sku and sku columns. The data dictionary notes sku 'should be UNIQUE?' but the DDL does not define a UNIQUE constraint on either column. No index is documented for these columns.

**System answer:**
> The retrieved context about `PRODUCTS` (via “Inventory Items” / physical table `PRODUCTS`) lists the `sku` (and also `product_sku` / `sku` as column variants), but it does not state any uniqueness constraint or index/constraint details for `sku`. Therefore, it is not documented here whether `PRODUCTS.sku` is unique.

**Sources retrieved (12):** `Inventory Items→PRODUCTS`, `parent_chunk_data_dictionary.txt_2`, `parent_chunk_data_dictionary.txt_3`, `Sales Order→ORDERS`, `parent_chunk_data_dictionary.txt_1`, `Order Line Items→ORDER_ITEMS`, `Receipt→PAYMENTS`, `parent_chunk_business_glossary.txt_0`

**Context previews (first 3):**

1. _Business concept 'Inventory Items' — The table stores product/master data used for sale and inventory control, including product identifiers (product_id), SKU, pricing (unit_price/current_price/cost_p…_

2. _Foreign Keys: - customer_id → CUSTOMERS(customer_id or CustomerID?) - [missing other FK definitions] ========================================== ORDER_ITEMS (or ORDER_DETAILS?) ========================…_

3. _========================================== PAYMENTS ==========================================  Primary Key: payment_id (unverified) | Column Name | Data Type | Constraints | Description | |----------…_

---

### ✅ ec_017 — What is the relationship between customers and orders?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0859 | **Gate:** `proceed_with_warning`

**Expected answer:**
> The glossary states 'A customer can place multiple orders. Or is it accounts that place orders?' indicating uncertainty about the relationship. The ORDERS table has both customer_id and CustomerID columns with ambiguous FK references, and the data dictionary notes they reference 'customer (which tab…

**System answer:**
> In the schema, the business concept “Sales Order” is implemented by the table `ORDERS`, which includes a `customer_id` / `CustomerID` column. The `CUSTOMERS` table has `customer_id` / `CustomerID` as its primary key. 

The retrieved context does not explicitly state a foreign key constraint from `ORDERS.customer_id` to `CUSTOMERS`, so I can only confirm that `ORDERS` contains a `customer_id` field…

**Sources retrieved (12):** `parent_chunk_data_dictionary.txt_3`, `parent_chunk_data_dictionary.txt_2`, `Sales Order→ORDERS`, `parent_chunk_data_dictionary.txt_1`, `Inventory Items→PRODUCTS`, `Order Line Items→ORDER_ITEMS`, `parent_chunk_business_glossary.txt_0`, `Sales Order`

**Context previews (first 3):**

1. _========================================== PAYMENTS ==========================================  Primary Key: payment_id (unverified) | Column Name | Data Type | Constraints | Description | |----------…_

2. _Foreign Keys: - customer_id → CUSTOMERS(customer_id or CustomerID?) - [missing other FK definitions] ========================================== ORDER_ITEMS (or ORDER_DETAILS?) ========================…_

3. _Business concept 'Sales Order' — The table models the core header of an order with a unique order identifier, order date, order status, pricing totals (orderAmount/total_amount, shippingAmount, tax_am…_

---

### ✅ ec_018 — Which price column represents what the customer actually pays?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0688 | **Gate:** `proceed_with_warning`

**Expected answer:**
> Multiple price columns exist across tables: ORDERS has orderAmount and total_amount; ORDER_ITEMS has unit_price and UnitPrice; PRODUCTS has unit_price, current_price, and cost_price. The data dictionary does not explain which represents the final customer price, whether discounts are applied, or how…

**System answer:**
> In the schema, the amount the customer actually pays is represented by `PAYMENTS.payment_amount` in the physical table `PAYMENTS` (used to implement the business concept `Receipt`). This is the only explicit “paid” amount column described in the retrieved context.  

What’s uncertain: the context does not explicitly define how `ORDERS.orderAmount` / `ORDERS.total_amount` relate to the final amount…

**Sources retrieved (12):** `Receipt→PAYMENTS`, `Sales Order→ORDERS`, `parent_chunk_data_dictionary.txt_2`, `parent_chunk_data_dictionary.txt_3`, `Order Line Items→ORDER_ITEMS`, `Inventory Items→PRODUCTS`, `parent_chunk_data_dictionary.txt_1`, `parent_chunk_business_glossary.txt_0`

**Context previews (first 3):**

1. _Business concept 'Receipt' is implemented by physical table PAYMENTS (columns: payment_id, PaymentID, order_id, customer_id, payment_date, payment_amount, payment_method, payment_status, transaction_i…_

2. _Business concept 'Sales Order' — The table models the core header of an order with a unique order identifier, order date, order status, pricing totals (orderAmount/total_amount, shippingAmount, tax_am…_

3. _Foreign Keys: - customer_id → CUSTOMERS(customer_id or CustomerID?) - [missing other FK definitions] ========================================== ORDER_ITEMS (or ORDER_DETAILS?) ========================…_

---

### ✅ ec_019 — What's the difference between Shipment, Delivery, and Fulfillment?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0050 | **Gate:** `proceed_with_warning`

**Expected answer:**
> The glossary provides definitions but unclear boundaries: Shipment is 'The process of delivering goods to a customer'; Delivery is 'The completion of a Shipment when goods reach the customer'; Fulfillment is 'The process of preparing and delivering orders. Encompasses Shipment and Delivery.' The exa…

**System answer:**
> I cannot find this information in the knowledge graph. The retrieved context only defines order-related and payment/inventory concepts and mappings (for example, “Sales Order” in table `ORDERS`, “Order Line Items” in table `ORDER_ITEMS`, “Inventory Items” in table `PRODUCTS`, and “Receipt” in table `PAYMENTS`). It does not mention or define “Shipment,” “Delivery,” or “Fulfillment,” so I can’t dete…

**Sources retrieved (12):** `Sales Order→ORDERS`, `parent_chunk_data_dictionary.txt_2`, `parent_chunk_data_dictionary.txt_3`, `Order Line Items→ORDER_ITEMS`, `Inventory Items→PRODUCTS`, `parent_chunk_business_glossary.txt_0`, `Sales Order`, `Order Line Items`

**Context previews (first 3):**

1. _Business concept 'Sales Order' — The table models the core header of an order with a unique order identifier, order date, order status, pricing totals (orderAmount/total_amount, shippingAmount, tax_am…_

2. _Foreign Keys: - customer_id → CUSTOMERS(customer_id or CustomerID?) - [missing other FK definitions] ========================================== ORDER_ITEMS (or ORDER_DETAILS?) ========================…_

3. _========================================== PAYMENTS ==========================================  Primary Key: payment_id (unverified) | Column Name | Data Type | Constraints | Description | |----------…_

---

### ✅ ec_020 — Are foreign key constraints enforced in the schema?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.1603 | **Gate:** `proceed_with_warning`

**Expected answer:**
> No foreign key constraints are enforced in the DDL. While the data dictionary documents FK relationships (e.g., customer_id → CUSTOMERS, order_id → ORDERS), the actual CREATE TABLE statements omit the REFERENCES clauses. The schema explicitly notes 'FK constraints defined in data dictionary but not …

**System answer:**
> The retrieved context shows that foreign key relationships are defined at the schema metadata level (e.g., in `ORDER_ITEMS`: `order_id → ORDERS(...)` and `product_id → PRODUCTS(...)`; in `PAYMENTS`: `order_id → ORDERS`, `customer_id → CUSTOMERS`), but it does not state whether those foreign key constraints are actually enforced in the database (for example, no information is provided about constra…

**Sources retrieved (12):** `parent_chunk_data_dictionary.txt_2`, `parent_chunk_data_dictionary.txt_3`, `parent_chunk_data_dictionary.txt_1`, `parent_chunk_business_glossary.txt_0`, `Inventory Items→PRODUCTS`, `Receipt→PAYMENTS`, `Order Line Items→ORDER_ITEMS`, `Sales Order→ORDERS`

**Context previews (first 3):**

1. _Foreign Keys: - customer_id → CUSTOMERS(customer_id or CustomerID?) - [missing other FK definitions] ========================================== ORDER_ITEMS (or ORDER_DETAILS?) ========================…_

2. _========================================== PAYMENTS ==========================================  Primary Key: payment_id (unverified) | Column Name | Data Type | Constraints | Description | |----------…_

3. _DATA DICTIONARY - Enterprise Database Version: 2.1 (incomplete documentation) Last Updated: 2024-02-28 ========================================== CUSTOMERS ========================================== P…_

---

## Anomalies & Observations

No anomalies detected. All questions grounded with acceptable RAGAS scores.
