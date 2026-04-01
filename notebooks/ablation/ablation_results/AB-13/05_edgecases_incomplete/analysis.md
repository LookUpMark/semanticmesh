# AB-13 — 05_edgecases_incomplete — Run Analysis

**Timestamp:** 2026-04-01 04:30:46  
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
| Triplets extracted | 177 |
| Entities resolved | 80 |
| Tables parsed | 5 |
| Tables completed | 5 |

## Query Evaluation Summary

| Metric | Value |
|--------|-------|
| Questions | 20 |
| Grounded | **20/20 (100%)** |
| Avg GT Coverage | 100% |
| Avg Top Score | 0.4744 |
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
> In the BUSINESS GLOSSARY under CUSTOMER MANAGEMENT, “Customer” is only partially defined as “An individual or organization that...” and the definition is marked incomplete.

The related glossary context says “Client” is “a person or company that purchases goods or services” and may be used interchangeably with “Customer” in some contexts. It also says “Account Holder” is the primary owner of an ac…

**Sources retrieved (12):** `Customer's first name→CUSTOMERS`, `parent_chunk_data_dictionary.txt_1`, `Sales Order→ORDERS`, `parent_chunk_data_dictionary.txt_2`, `parent_chunk_data_dictionary.txt_3`, `payment_method→PAYMENTS`, `parent_chunk_business_glossary.txt_0`, `Customer's first name`

**Context previews (first 3):**

1. _Business concept 'Customer's first name' is implemented by physical table CUSTOMERS (columns: customer_id, CustomerID, firstName, first_name, lastName, last_name, email, emailAddress, phone, phoneNumb…_

2. _DATA DICTIONARY - Enterprise Database Version: 2.1 (incomplete documentation) Last Updated: 2024-02-28 ========================================== CUSTOMERS ========================================== P…_

3. _Business concept 'Sales Order' — The table contains a clear order header structure with order identifier, customer reference, order date, status, amounts, and payment fields, which aligns strongly wit…_

---

### ✅ ec_002 — What's the difference between firstName and first_name in the CUSTOMERS table?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.6176 | **Gate:** `proceed`

**Expected answer:**
> Both columns exist in the CUSTOMERS table with identical VARCHAR(50) data types. The data dictionary notes they appear to be duplicates resulting from inconsistent naming conventions (snake_case vs camelCase), but the actual usage by the application is not documented.

**System answer:**
> Based on the retrieved context, there is no documented business difference between `firstName` and `first_name` in `CUSTOMERS`.

The context shows that both columns are in the `CUSTOMERS` table, both are `VARCHAR(50)`, and `firstName` is explicitly described as “Customer's first name.” The `first_name` column is described as “[appears to be duplicate].” The business concept mapping for “Customer's…

**Sources retrieved (12):** `Customer's first name→CUSTOMERS`, `parent_chunk_data_dictionary.txt_1`, `parent_chunk_data_dictionary.txt_2`, `Sales Order→ORDERS`, `parent_chunk_data_dictionary.txt_3`, `Order Details→ORDER_ITEMS`, `parent_chunk_business_glossary.txt_0`, `Sales Order`

**Context previews (first 3):**

1. _Business concept 'Customer's first name' is implemented by physical table CUSTOMERS (columns: customer_id, CustomerID, firstName, first_name, lastName, last_name, email, emailAddress, phone, phoneNumb…_

2. _DATA DICTIONARY - Enterprise Database Version: 2.1 (incomplete documentation) Last Updated: 2024-02-28 ========================================== CUSTOMERS ========================================== P…_

3. _Foreign Keys: - customer_id → CUSTOMERS(customer_id or CustomerID?) - [missing other FK definitions] ========================================== ORDER_ITEMS (or ORDER_DETAILS?) ========================…_

---

### ✅ ec_003 — Which customer column should be used as a foreign key reference: customer_id or CustomerID?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.9258 | **Gate:** `proceed`

**Expected answer:**
> The CUSTOMERS table has both customer_id (defined as PRIMARY KEY) and CustomerID (defined as INTEGER with no constraints). The ORDERS table also has both customer_id and CustomerID columns with ambiguous FK references. The data dictionary indicates this inconsistency is documented but not yet resolv…

**System answer:**
> The retrieved context does not definitively resolve this. In CUSTOMERS, the primary key is documented as “customer_id (or is it CustomerID? check with DBA),” so the source itself marks the choice as uncertain.

From the available schema metadata, customer_id is the stronger foreign key reference candidate because:
the foreign key note is written as “customer_id → CUSTOMERS(customer_id or CustomerI…

**Sources retrieved (12):** `parent_chunk_data_dictionary.txt_2`, `parent_chunk_data_dictionary.txt_1`, `Customer's first name→CUSTOMERS`, `parent_chunk_data_dictionary.txt_3`, `Sales Order→ORDERS`, `payment_method→PAYMENTS`, `Order Details→ORDER_ITEMS`, `Inventory Item→PRODUCTS`

**Context previews (first 3):**

1. _Foreign Keys: - customer_id → CUSTOMERS(customer_id or CustomerID?) - [missing other FK definitions] ========================================== ORDER_ITEMS (or ORDER_DETAILS?) ========================…_

2. _DATA DICTIONARY - Enterprise Database Version: 2.1 (incomplete documentation) Last Updated: 2024-02-28 ========================================== CUSTOMERS ========================================== P…_

3. _Business concept 'Customer's first name' is implemented by physical table CUSTOMERS (columns: customer_id, CustomerID, firstName, first_name, lastName, last_name, email, emailAddress, phone, phoneNumb…_

---

### ✅ ec_004 — What are the valid values for order_status?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.3951 | **Gate:** `proceed`

**Expected answer:**
> The business glossary documents several order statuses: Pending, Processing, Completed, Cancelled, On Hold, and Failed (which is marked as [definition missing]). However, these are not enforced by a CHECK constraint in the schema, and the data dictionary notes that valid values reference '[missing d…

**System answer:**
> The retrieved context shows that order_status is a column on the ORDERS table, which implements the business concept Sales Order. The business glossary also says an Order “can be in various states.” However, the context does not provide an enumerated domain, code list, or any documented valid values for order_status.

So, from the available context, the only supported answer is: order_status exist…

**Sources retrieved (12):** `parent_chunk_data_dictionary.txt_3`, `Sales Order→ORDERS`, `parent_chunk_data_dictionary.txt_1`, `parent_chunk_data_dictionary.txt_2`, `parent_chunk_business_glossary.txt_0`, `payment_method→PAYMENTS`, `Order Details→ORDER_ITEMS`, `Customer's first name→CUSTOMERS`

**Context previews (first 3):**

1. _========================================== PAYMENTS ==========================================  Primary Key: payment_id (unverified) | Column Name | Data Type | Constraints | Description | |----------…_

2. _Business concept 'Sales Order' — The table contains a clear order header structure with order identifier, customer reference, order date, status, amounts, and payment fields, which aligns strongly wit…_

3. _DATA DICTIONARY - Enterprise Database Version: 2.1 (incomplete documentation) Last Updated: 2024-02-28 ========================================== CUSTOMERS ========================================== P…_

---

### ✅ ec_005 — Is there a difference between Product, Item, and SKU?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.5696 | **Gate:** `proceed`

**Expected answer:**
> The glossary indicates these terms are related but distinct: Product is defined as "A thing that is... [definition needs clarification]"; Item is a synonym for Product used in inventory context; SKU (Stock Keeping Unit) is a unique identifier for a product variant; Inventory Item refers to physical …

**System answer:**
> From the retrieved context, there is no explicit business glossary definition that distinguishes “Product” from “Item.” What the schema does show is that the business concept “Inventory Item” is implemented by the physical table PRODUCTS, so in this knowledge graph the item/inventory concept is represented in the same table as product data.

The PRODUCTS table contains product-identifying and desc…

**Sources retrieved (12):** `Inventory Item→PRODUCTS`, `parent_chunk_data_dictionary.txt_2`, `Order Details→ORDER_ITEMS`, `parent_chunk_data_dictionary.txt_1`, `parent_chunk_data_dictionary.txt_3`, `Sales Order→ORDERS`, `parent_chunk_business_glossary.txt_0`, `Order Details`

**Context previews (first 3):**

1. _Business concept 'Inventory Item' is implemented by physical table PRODUCTS (columns: product_id, ProductID, product_name, ProductName, product_sku, sku, product_category, category, unit_price, curren…_

2. _Foreign Keys: - customer_id → CUSTOMERS(customer_id or CustomerID?) - [missing other FK definitions] ========================================== ORDER_ITEMS (or ORDER_DETAILS?) ========================…_

3. _Business concept 'Order Details' — The table is a line-item detail structure with order_id, product_id, quantity, pricing, discount, and line total fields, which aligns most closely with an order deta…_

---

### ✅ ec_006 — Which table should ORDER_ITEMS.product_id reference: PRODUCTS or INVENTORY?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.9608 | **Gate:** `proceed`

**Expected answer:**
> The data dictionary states the FK reference is to 'PRODUCTS (or INVENTORY?)' and notes it is 'not verified'. The schema provides two potential targets: PRODUCTS table (which has product_id) and an INVENTORY table that is referenced in documentation but not defined in the DDL. The actual relationship…

**System answer:**
> Based on the retrieved context, ORDER_ITEMS.product_id should reference PRODUCTS.

The strongest support is that the business concept "Inventory Item" is implemented by the physical table PRODUCTS, and ORDER_ITEMS / "Order Details" includes product_id as the line-item product reference. The ORDER_ITEMS documentation itself says product_id "References PRODUCTS (or INVENTORY?)", but no physical tabl…

**Sources retrieved (12):** `parent_chunk_data_dictionary.txt_2`, `Inventory Item→PRODUCTS`, `Order Details→ORDER_ITEMS`, `Sales Order→ORDERS`, `parent_chunk_data_dictionary.txt_3`, `parent_chunk_data_dictionary.txt_1`, `Order Details`, `parent_chunk_business_glossary.txt_0`

**Context previews (first 3):**

1. _Foreign Keys: - customer_id → CUSTOMERS(customer_id or CustomerID?) - [missing other FK definitions] ========================================== ORDER_ITEMS (or ORDER_DETAILS?) ========================…_

2. _Business concept 'Inventory Item' is implemented by physical table PRODUCTS (columns: product_id, ProductID, product_name, ProductName, product_sku, sku, product_category, category, unit_price, curren…_

3. _Business concept 'Order Details' — The table is a line-item detail structure with order_id, product_id, quantity, pricing, discount, and line total fields, which aligns most closely with an order deta…_

---

### ✅ ec_007 — What's the difference between Revenue and Sales?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.4224 | **Gate:** `proceed`

**Expected answer:**
> Both terms show circular definitions: Revenue is defined as 'Income from sales. The same as... [definition circular, see Sales]', while Sales is defined as 'Revenue from selling products. See Revenue.' The glossary provides no clear distinction between these concepts.

**System answer:**
> The retrieved context does not define “Revenue” at all, and it does not define “Sales” as a standalone financial concept, so I cannot state the conceptual difference between Revenue and Sales from this knowledge graph.

What the context does contain is the business concept “Sales Order.” It says “Sales Order” is implemented by the ORDERS table and represents an order header structure with an order…

**Sources retrieved (12):** `Sales Order→ORDERS`, `parent_chunk_data_dictionary.txt_2`, `Order Details→ORDER_ITEMS`, `parent_chunk_data_dictionary.txt_3`, `parent_chunk_business_glossary.txt_0`, `Sales Order`, `Order Details`, `parent_chunk_data_dictionary.txt_1`

**Context previews (first 3):**

1. _Business concept 'Sales Order' — The table contains a clear order header structure with order identifier, customer reference, order date, status, amounts, and payment fields, which aligns strongly wit…_

2. _Foreign Keys: - customer_id → CUSTOMERS(customer_id or CustomerID?) - [missing other FK definitions] ========================================== ORDER_ITEMS (or ORDER_DETAILS?) ========================…_

3. _Business concept 'Order Details' — The table is a line-item detail structure with order_id, product_id, quantity, pricing, discount, and line total fields, which aligns most closely with an order deta…_

---

### ✅ ec_008 — Can one order have multiple payments?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0981 | **Gate:** `proceed_with_warning`

**Expected answer:**
> The PAYMENTS table has an order_id column, suggesting a many-to-one relationship (multiple payments can reference a single order). However, the relationship section in the glossary asks 'Or is it one-to-one?' indicating uncertainty. The ORDERS table has both payment_status and payment_method columns…

**System answer:**
> From the retrieved context, it is known that `PAYMENTS.order_id` is a foreign key that references `ORDERS`, so each payment record is linked to an order.

What cannot be determined from the context is the cardinality of that relationship. The documentation does not state whether `PAYMENTS.order_id` is unique, and it does not define a one-to-one or one-to-many rule between `ORDERS` and `PAYMENTS`. …

**Sources retrieved (12):** `parent_chunk_data_dictionary.txt_3`, `Sales Order→ORDERS`, `payment_method→PAYMENTS`, `parent_chunk_data_dictionary.txt_2`, `Order Details→ORDER_ITEMS`, `parent_chunk_data_dictionary.txt_1`, `Inventory Item→PRODUCTS`, `Customer's first name→CUSTOMERS`

**Context previews (first 3):**

1. _========================================== PAYMENTS ==========================================  Primary Key: payment_id (unverified) | Column Name | Data Type | Constraints | Description | |----------…_

2. _Business concept 'Sales Order' — The table contains a clear order header structure with order identifier, customer reference, order date, status, amounts, and payment fields, which aligns strongly wit…_

3. _Business concept 'payment_method' is implemented by physical table PAYMENTS (columns: payment_id, PaymentID, order_id, customer_id, payment_date, payment_amount, payment_method, payment_status, transa…_

---

### ✅ ec_009 — What payment methods are accepted?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.1791 | **Gate:** `proceed_with_warning`

**Expected answer:**
> The PAYMENTS table has a payment_method column (VARCHAR(30)), but the data dictionary notes '[missing valid values]' and no CHECK constraint exists to enumerate acceptable methods. The schema does not document what values are valid (e.g., credit_card, debit, paypal, etc.).

**System answer:**
> The retrieved context does not list the accepted payment method values.

What it does show is that payment method is a tracked schema field in two places. In PAYMENTS, the column payment_method is defined as VARCHAR(30), but its documentation explicitly says “[missing valid values].” The business concept payment_method is mapped to the PAYMENTS table. In ORDERS, which is described as the Sales Ord…

**Sources retrieved (12):** `parent_chunk_data_dictionary.txt_3`, `payment_method→PAYMENTS`, `Sales Order→ORDERS`, `parent_chunk_data_dictionary.txt_1`, `parent_chunk_data_dictionary.txt_2`, `parent_chunk_business_glossary.txt_0`, `Sales Order`, `Customer's first name→CUSTOMERS`

**Context previews (first 3):**

1. _========================================== PAYMENTS ==========================================  Primary Key: payment_id (unverified) | Column Name | Data Type | Constraints | Description | |----------…_

2. _Business concept 'payment_method' is implemented by physical table PAYMENTS (columns: payment_id, PaymentID, order_id, customer_id, payment_date, payment_amount, payment_method, payment_status, transa…_

3. _Business concept 'Sales Order' — The table contains a clear order header structure with order identifier, customer reference, order date, status, amounts, and payment fields, which aligns strongly wit…_

---

### ✅ ec_010 — What's the correct table name: ORDER_ITEMS or ORDER_DETAILS?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.9953 | **Gate:** `proceed`

**Expected answer:**
> The DDL creates a table named ORDER_ITEMS, but the data dictionary header shows 'ORDER_ITEMS (or ORDER_DETAILS?)' and notes 'Table name ambiguity: ORDER_ITEMS vs ORDER_DETAILS'. The actual table name in the schema is ORDER_ITEMS, but documentation suggests the application may reference it differentl…

**System answer:**
> From the retrieved context, the physical table name is ORDER_ITEMS, but it is also explicitly referenced as ORDER_DETAILS.

The context says the structure is a line-item detail table and that ORDER_DETAILS is the better semantic/business name: “the DDL explicitly notes it is also referenced as ORDER_DETAILS, so that naming is the best semantic match.” It also states that the business concept “Orde…

**Sources retrieved (12):** `parent_chunk_data_dictionary.txt_2`, `Order Details→ORDER_ITEMS`, `Inventory Item→PRODUCTS`, `parent_chunk_data_dictionary.txt_3`, `parent_chunk_data_dictionary.txt_1`, `Customer's first name→CUSTOMERS`, `Order Details`, `Customer's first name`

**Context previews (first 3):**

1. _Foreign Keys: - customer_id → CUSTOMERS(customer_id or CustomerID?) - [missing other FK definitions] ========================================== ORDER_ITEMS (or ORDER_DETAILS?) ========================…_

2. _Business concept 'Order Details' — The table is a line-item detail structure with order_id, product_id, quantity, pricing, discount, and line total fields, which aligns most closely with an order deta…_

3. _Business concept 'Inventory Item' is implemented by physical table PRODUCTS (columns: product_id, ProductID, product_name, ProductName, product_sku, sku, product_category, category, unit_price, curren…_

---

### ✅ ec_011 — Which date column should be used to track when an order was created: order_date, OrderDate, or created_at?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.8495 | **Gate:** `proceed`

**Expected answer:**
> The ORDERS table has three date-related columns: order_date (DATE type), OrderDate (DATETIME type with different precision), and created_at (TIMESTAMP type). The data dictionary provides no guidance on which is actually used by the application or why three columns exist for potentially the same purp…

**System answer:**
> From the retrieved context, this cannot be determined definitively.

The ORDERS table for the business concept Sales Order includes all three columns: order_date, OrderDate, and created_at. The context says the table has a “clear order header structure with order identifier, customer reference, order date, status, amounts, and payment fields,” which supports order_date/OrderDate as order-related d…

**Sources retrieved (12):** `Sales Order→ORDERS`, `payment_method→PAYMENTS`, `parent_chunk_data_dictionary.txt_1`, `parent_chunk_data_dictionary.txt_3`, `Customer's first name→CUSTOMERS`, `Inventory Item→PRODUCTS`, `parent_chunk_data_dictionary.txt_2`, `Order Details→ORDER_ITEMS`

**Context previews (first 3):**

1. _Business concept 'Sales Order' — The table contains a clear order header structure with order identifier, customer reference, order date, status, amounts, and payment fields, which aligns strongly wit…_

2. _Business concept 'payment_method' is implemented by physical table PAYMENTS (columns: payment_id, PaymentID, order_id, customer_id, payment_date, payment_amount, payment_method, payment_status, transa…_

3. _DATA DICTIONARY - Enterprise Database Version: 2.1 (incomplete documentation) Last Updated: 2024-02-28 ========================================== CUSTOMERS ========================================== P…_

---

### ✅ ec_012 — What does the Failed order status mean?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0031 | **Gate:** `proceed_with_warning`

**Expected answer:**
> The business glossary lists Failed as an order status but marks it as '[definition missing]'. Other statuses have definitions (Pending, Processing, Completed, Cancelled, On Hold), but Failed is undefined despite being a valid status value.

**System answer:**
> From the retrieved context, I can only confirm that the Sales Order concept is implemented by the ORDERS table, and that this table includes an order_status column. The glossary also says an Order “can be in various states.”

However, the context does not define any specific order status values or their meanings, so the meaning of a Failed order status cannot be determined from the knowledge graph…

**Sources retrieved (12):** `Sales Order→ORDERS`, `parent_chunk_data_dictionary.txt_3`, `parent_chunk_data_dictionary.txt_1`, `parent_chunk_data_dictionary.txt_2`, `Order Details→ORDER_ITEMS`, `payment_method→PAYMENTS`, `Customer's first name→CUSTOMERS`, `Inventory Item→PRODUCTS`

**Context previews (first 3):**

1. _Business concept 'Sales Order' — The table contains a clear order header structure with order identifier, customer reference, order date, status, amounts, and payment fields, which aligns strongly wit…_

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

The schema excerpts shown for CUSTOMERS, PAYMENTS, ORDER_ITEMS, and the concept mappings list constraints such as PK, FK, and UNIQUE?, but they do not show any column marked NOT NULL. In many places the documentation is incomplete and the constraints are listed as “?” or “[missing documentation],” so the context does not confi…

**Sources retrieved (12):** `parent_chunk_data_dictionary.txt_3`, `Order Details→ORDER_ITEMS`, `parent_chunk_data_dictionary.txt_2`, `parent_chunk_data_dictionary.txt_1`, `Sales Order→ORDERS`, `Order Details`, `parent_chunk_business_glossary.txt_0`, `Sales Order`

**Context previews (first 3):**

1. _========================================== PAYMENTS ==========================================  Primary Key: payment_id (unverified) | Column Name | Data Type | Constraints | Description | |----------…_

2. _Business concept 'Order Details' — The table is a line-item detail structure with order_id, product_id, quantity, pricing, discount, and line total fields, which aligns most closely with an order deta…_

3. _Foreign Keys: - customer_id → CUSTOMERS(customer_id or CustomerID?) - [missing other FK definitions] ========================================== ORDER_ITEMS (or ORDER_DETAILS?) ========================…_

---

### ✅ ec_014 — What's the difference between unit_price and current_price in PRODUCTS?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.4761 | **Gate:** `proceed`

**Expected answer:**
> The PRODUCTS table has both unit_price and current_price columns (both DECIMAL(10,2)). The data dictionary asks 'Different from unit_price?' but provides no explanation of the distinction or when each would be used.

**System answer:**
> The retrieved context shows that PRODUCTS, which implements the business concept Inventory Item, contains both unit_price and current_price, but it does not provide any column descriptions or business rules for either field in PRODUCTS.

So, from the available context, the only supported answer is that both are separate columns in PRODUCTS, but the knowledge graph does not document how unit_price …

**Sources retrieved (12):** `Inventory Item→PRODUCTS`, `parent_chunk_data_dictionary.txt_2`, `Order Details→ORDER_ITEMS`, `Sales Order→ORDERS`, `parent_chunk_data_dictionary.txt_3`, `parent_chunk_business_glossary.txt_0`, `Order Details`, `Sales Order`

**Context previews (first 3):**

1. _Business concept 'Inventory Item' is implemented by physical table PRODUCTS (columns: product_id, ProductID, product_name, ProductName, product_sku, sku, product_category, category, unit_price, curren…_

2. _Foreign Keys: - customer_id → CUSTOMERS(customer_id or CustomerID?) - [missing other FK definitions] ========================================== ORDER_ITEMS (or ORDER_DETAILS?) ========================…_

3. _Business concept 'Order Details' — The table is a line-item detail structure with order_id, product_id, quantity, pricing, discount, and line total fields, which aligns most closely with an order deta…_

---

### ✅ ec_015 — When is an invoice generated vs payment processed?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.6598 | **Gate:** `proceed`

**Expected answer:**
> The relationship section in the glossary asks 'An invoice is generated for an order. But when? And can one order have multiple invoices?' indicating the timing and cardinality are not defined. The glossary defines Invoice as 'A document requesting payment. Related to Bill' and Payment as 'The transf…

**System answer:**
> The retrieved context does not define a business rule for when an invoice is generated versus when a payment is processed.

What can be answered from the context is this: there is no invoice entity, invoice table, invoice column, or glossary definition for “Invoice” in the provided material, so invoice generation timing is not available here.

Payment processing is partially documented at the sche…

**Sources retrieved (12):** `parent_chunk_data_dictionary.txt_3`, `Sales Order→ORDERS`, `parent_chunk_data_dictionary.txt_1`, `parent_chunk_data_dictionary.txt_2`, `payment_method→PAYMENTS`, `parent_chunk_business_glossary.txt_0`, `Sales Order`, `Order Details→ORDER_ITEMS`

**Context previews (first 3):**

1. _========================================== PAYMENTS ==========================================  Primary Key: payment_id (unverified) | Column Name | Data Type | Constraints | Description | |----------…_

2. _Business concept 'Sales Order' — The table contains a clear order header structure with order identifier, customer reference, order date, status, amounts, and payment fields, which aligns strongly wit…_

3. _DATA DICTIONARY - Enterprise Database Version: 2.1 (incomplete documentation) Last Updated: 2024-02-28 ========================================== CUSTOMERS ========================================== P…_

---

### ✅ ec_016 — Is the sku column in PRODUCTS unique?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.3824 | **Gate:** `proceed`

**Expected answer:**
> The PRODUCTS table has both product_sku and sku columns. The data dictionary notes sku 'should be UNIQUE?' but the DDL does not define a UNIQUE constraint on either column. No index is documented for these columns.

**System answer:**
> The retrieved context does not state that the PRODUCTS sku column is unique.

What the context does show is that the business concept Inventory Item maps to PRODUCTS, with columns including product_sku and sku, but no constraints such as UNIQUE are provided for either column. So, based on the available context, uniqueness for sku cannot be confirmed.

**Sources retrieved (12):** `Inventory Item→PRODUCTS`, `parent_chunk_data_dictionary.txt_2`, `parent_chunk_data_dictionary.txt_3`, `Order Details→ORDER_ITEMS`, `parent_chunk_data_dictionary.txt_1`, `Customer's first name→CUSTOMERS`, `Sales Order→ORDERS`, `payment_method→PAYMENTS`

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
> Customers and orders are related through the ORDERS table, which implements the business concept “Sales Order.” The ORDERS table includes a customer reference: customer_id and also CustomerID as a duplicate/legacy variant. The CUSTOMERS table has primary key customer_id, with CustomerID noted as a possible duplicate naming variant.

So, at the schema level, an order belongs to a customer by joinin…

**Sources retrieved (12):** `parent_chunk_data_dictionary.txt_3`, `parent_chunk_data_dictionary.txt_2`, `Sales Order→ORDERS`, `parent_chunk_data_dictionary.txt_1`, `Order Details→ORDER_ITEMS`, `Customer's first name→CUSTOMERS`, `parent_chunk_business_glossary.txt_0`, `Sales Order`

**Context previews (first 3):**

1. _========================================== PAYMENTS ==========================================  Primary Key: payment_id (unverified) | Column Name | Data Type | Constraints | Description | |----------…_

2. _Foreign Keys: - customer_id → CUSTOMERS(customer_id or CustomerID?) - [missing other FK definitions] ========================================== ORDER_ITEMS (or ORDER_DETAILS?) ========================…_

3. _Business concept 'Sales Order' — The table contains a clear order header structure with order identifier, customer reference, order date, status, amounts, and payment fields, which aligns strongly wit…_

---

### ✅ ec_018 — Which price column represents what the customer actually pays?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0682 | **Gate:** `proceed_with_warning`

**Expected answer:**
> Multiple price columns exist across tables: ORDERS has orderAmount and total_amount; ORDER_ITEMS has unit_price and UnitPrice; PRODUCTS has unit_price, current_price, and cost_price. The data dictionary does not explain which represents the final customer price, whether discounts are applied, or how…

**System answer:**
> The retrieved context does not explicitly identify a single price column as “what the customer actually pays,” so this cannot be determined definitively.

What is known from the context is:

In ORDER_ITEMS (the business concept “Order Details”), unit_price is the only column explicitly described as “Price per unit.” The same table also includes discount_percent, discount_amount, and line_total / L…

**Sources retrieved (12):** `payment_method→PAYMENTS`, `parent_chunk_data_dictionary.txt_2`, `parent_chunk_data_dictionary.txt_3`, `Sales Order→ORDERS`, `Customer's first name→CUSTOMERS`, `Order Details→ORDER_ITEMS`, `parent_chunk_data_dictionary.txt_1`, `Inventory Item→PRODUCTS`

**Context previews (first 3):**

1. _Business concept 'payment_method' is implemented by physical table PAYMENTS (columns: payment_id, PaymentID, order_id, customer_id, payment_date, payment_amount, payment_method, payment_status, transa…_

2. _Foreign Keys: - customer_id → CUSTOMERS(customer_id or CustomerID?) - [missing other FK definitions] ========================================== ORDER_ITEMS (or ORDER_DETAILS?) ========================…_

3. _========================================== PAYMENTS ==========================================  Primary Key: payment_id (unverified) | Column Name | Data Type | Constraints | Description | |----------…_

---

### ✅ ec_019 — What's the difference between Shipment, Delivery, and Fulfillment?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0050 | **Gate:** `proceed_with_warning`

**Expected answer:**
> The glossary provides definitions but unclear boundaries: Shipment is 'The process of delivering goods to a customer'; Delivery is 'The completion of a Shipment when goods reach the customer'; Fulfillment is 'The process of preparing and delivering orders. Encompasses Shipment and Delivery.' The exa…

**System answer:**
> I cannot determine the difference between Shipment, Delivery, and Fulfillment from the retrieved context. The provided context includes definitions and schema mappings for Sales Order, Order Details, Customers, Payments, Inventory Item, and a partial glossary entry for Order and Transaction, but it does not contain any business glossary definitions, table mappings, or schema metadata for Shipment,…

**Sources retrieved (12):** `Sales Order→ORDERS`, `parent_chunk_data_dictionary.txt_2`, `Order Details→ORDER_ITEMS`, `parent_chunk_data_dictionary.txt_3`, `parent_chunk_business_glossary.txt_0`, `Sales Order`, `Order Details`, `parent_chunk_data_dictionary.txt_1`

**Context previews (first 3):**

1. _Business concept 'Sales Order' — The table contains a clear order header structure with order identifier, customer reference, order date, status, amounts, and payment fields, which aligns strongly wit…_

2. _Foreign Keys: - customer_id → CUSTOMERS(customer_id or CustomerID?) - [missing other FK definitions] ========================================== ORDER_ITEMS (or ORDER_DETAILS?) ========================…_

3. _Business concept 'Order Details' — The table is a line-item detail structure with order_id, product_id, quantity, pricing, discount, and line total fields, which aligns most closely with an order deta…_

---

### ✅ ec_020 — Are foreign key constraints enforced in the schema?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.1603 | **Gate:** `proceed_with_warning`

**Expected answer:**
> No foreign key constraints are enforced in the DDL. While the data dictionary documents FK relationships (e.g., customer_id → CUSTOMERS, order_id → ORDERS), the actual CREATE TABLE statements omit the REFERENCES clauses. The schema explicitly notes 'FK constraints defined in data dictionary but not …

**System answer:**
> The retrieved context does not confirm that foreign key constraints are actually enforced in the schema. What it does show is schema documentation that labels some columns as foreign keys and identifies intended relationships, but the documentation is incomplete and in places explicitly uncertain.

From the context, the documented foreign key relationships include PAYMENTS.order_id referencing ORD…

**Sources retrieved (12):** `parent_chunk_data_dictionary.txt_2`, `parent_chunk_data_dictionary.txt_3`, `parent_chunk_data_dictionary.txt_1`, `Order Details→ORDER_ITEMS`, `Order Details`, `parent_chunk_business_glossary.txt_0`, `Customer's first name→CUSTOMERS`, `Sales Order→ORDERS`

**Context previews (first 3):**

1. _Foreign Keys: - customer_id → CUSTOMERS(customer_id or CustomerID?) - [missing other FK definitions] ========================================== ORDER_ITEMS (or ORDER_DETAILS?) ========================…_

2. _========================================== PAYMENTS ==========================================  Primary Key: payment_id (unverified) | Column Name | Data Type | Constraints | Description | |----------…_

3. _DATA DICTIONARY - Enterprise Database Version: 2.1 (incomplete documentation) Last Updated: 2024-02-28 ========================================== CUSTOMERS ========================================== P…_

---

## Anomalies & Observations

No anomalies detected. All questions grounded with acceptable RAGAS scores.
