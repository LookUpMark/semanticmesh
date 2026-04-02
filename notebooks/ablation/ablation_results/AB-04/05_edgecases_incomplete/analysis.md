# AB-04 — 05_edgecases_incomplete — Run Analysis

**Timestamp:** 2026-03-31 02:05:58  
**Run tag:** `v5`

## Configuration

| Parameter | Value |
|-----------|-------|
| Extraction model | `LLM (gpt-5.4-nano-2026-03-17)` |
| Reasoning model | `gpt-5.4-2026-03-05` |
| Embedding model | `BAAI/bge-m3` |
| Retrieval mode | `hybrid` |
| Reranker | `True` |
| Reranker top_k | `5` |
| Chunk size / overlap | `256 / 32` |
| ER similarity threshold | `0.75` |

## Builder Results

Builder skipped (`--no-builder`).

## Query Evaluation Summary

| Metric | Value |
|--------|-------|
| Questions | 20 |
| Grounded | **20/20 (100%)** |
| Avg GT Coverage | 100% |
| Avg Top Score | 0.4706 |
| Avg Chunk Count | 5.0 |
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
> In the retrieved context, Customer is defined only partially: “An individual or organization that...”, and the definition is marked incomplete in the business glossary.

Related context says Client is “a person or company that purchases goods or services” and may be used interchangeably with Customer in some contexts, but the glossary does not explicitly complete the Customer definition with that …

**Sources retrieved (5):** `CUSTOMERS→CUSTOMERS`, `parent_chunk_data_dictionary.txt_1`, `Sales Order→ORDERS`, `parent_chunk_business_glossary.txt_0`, `Sales Order`

**Context previews (first 3):**

1. _Business concept 'CUSTOMERS' is implemented by physical table CUSTOMERS (columns: customer_id, CustomerID, firstName, first_name, lastName, last_name, email, emailAddress, phone, phoneNumber, created_…_

2. _DATA DICTIONARY - Enterprise Database Version: 2.1 (incomplete documentation) Last Updated: 2024-02-28 ========================================== CUSTOMERS ========================================== P…_

3. _Business concept 'Sales Order' — The table contains canonical order-header attributes such as order_id, customer_id, order_date, order_status, and financial totals (amount, shipping, tax), which align…_

---

### ✅ ec_002 — What's the difference between firstName and first_name in the CUSTOMERS table?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.5988 | **Gate:** `proceed`

**Expected answer:**
> Both columns exist in the CUSTOMERS table with identical VARCHAR(50) data types. The data dictionary notes they appear to be duplicates resulting from inconsistent naming conventions (snake_case vs camelCase), but the actual usage by the application is not documented.

**System answer:**
> Based on the retrieved context, there is no documented business difference between `firstName` and `first_name` in `CUSTOMERS`.

The `CUSTOMERS` data dictionary shows both columns as `VARCHAR(50)`. `firstName` is described as “Customer's first name,” while `first_name` is explicitly noted as “[appears to be duplicate].” The concept-to-table mapping for `CUSTOMERS` also includes both names, which s…

**Sources retrieved (5):** `CUSTOMERS→CUSTOMERS`, `parent_chunk_data_dictionary.txt_1`, `parent_chunk_data_dictionary.txt_2`, `Sales Order→ORDERS`, `parent_chunk_business_glossary.txt_0`

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
> Based on the retrieved context, the strongest documented choice is customer_id.

The context says the CUSTOMERS table primary key is "customer_id (or is it CustomerID? check with DBA)," so customer_id is the primary key currently indicated, but the documentation is explicitly inconsistent. That is reinforced by other tables: PAYMENTS uses customer_id as an FK referencing CUSTOMERS, and the Sales O…

**Sources retrieved (5):** `parent_chunk_data_dictionary.txt_2`, `parent_chunk_data_dictionary.txt_1`, `CUSTOMERS→CUSTOMERS`, `parent_chunk_data_dictionary.txt_3`, `Sales Order→ORDERS`

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

What it does show is that order_status is an order-header attribute in the ORDERS table, which implements the business concept Sales Order. But no enumeration, code list, or allowed status values is included in the context.

**Sources retrieved (5):** `parent_chunk_data_dictionary.txt_3`, `Sales Order→ORDERS`, `Sales Order`, `Order Items`, `Payment gateway response→PAYMENTS`

**Context previews (first 3):**

1. _========================================== PAYMENTS ==========================================  Primary Key: payment_id (unverified) | Column Name | Data Type | Constraints | Description | |----------…_

2. _Business concept 'Sales Order' — The table contains canonical order-header attributes such as order_id, customer_id, order_date, order_status, and financial totals (amount, shipping, tax), which align…_

3. _Sales Order: The table contains canonical order-header attributes such as order_id, customer_id, order_date, order_status, and financial totals (amount, shipping, tax), which align strongly with a sal…_

---

### ✅ ec_005 — Is there a difference between Product, Item, and SKU?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.5696 | **Gate:** `proceed`

**Expected answer:**
> The glossary indicates these terms are related but distinct: Product is defined as "A thing that is... [definition needs clarification]"; Item is a synonym for Product used in inventory context; SKU (Stock Keeping Unit) is a unique identifier for a product variant; Inventory Item refers to physical …

**System answer:**
> From the retrieved context, only part of this can be answered.

The context does not define separate business concepts named “Product” or “SKU,” so it does not establish an explicit business difference among “Product,” “Item,” and “SKU.”

What it does show is this:

“Merchandise” is the business concept implemented by the PRODUCTS table. PRODUCTS contains columns such as product_id, product_name, …

**Sources retrieved (5):** `Merchandise→PRODUCTS`, `parent_chunk_data_dictionary.txt_2`, `Order Items→ORDER_ITEMS`, `parent_chunk_business_glossary.txt_0`, `Order Items`

**Context previews (first 3):**

1. _Business concept 'Merchandise' is implemented by physical table PRODUCTS (columns: product_id, ProductID, product_name, ProductName, product_sku, sku, product_category, category, unit_price, current_p…_

2. _Foreign Keys: - customer_id → CUSTOMERS(customer_id or CustomerID?) - [missing other FK definitions] ========================================== ORDER_ITEMS (or ORDER_DETAILS?) ========================…_

3. _Business concept 'Order Items' — The table is explicitly named ORDER_ITEMS and its columns form a classic order line structure with order_id, product_id, quantity, unit price, discounts, and line tota…_

---

### ✅ ec_006 — Which table should ORDER_ITEMS.product_id reference: PRODUCTS or INVENTORY?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.9608 | **Gate:** `proceed`

**Expected answer:**
> The data dictionary states the FK reference is to 'PRODUCTS (or INVENTORY?)' and notes it is 'not verified'. The schema provides two potential targets: PRODUCTS table (which has product_id) and an INVENTORY table that is referenced in documentation but not defined in the DDL. The actual relationship…

**System answer:**
> Based on the retrieved context, ORDER_ITEMS.product_id should most likely reference PRODUCTS, not INVENTORY.

The strongest support is that the business concept “Order Items” is implemented by ORDER_ITEMS with a classic order-line structure including product_id, and the business concept “Merchandise” is implemented by PRODUCTS, which contains product_id/ProductID and product attributes such as pro…

**Sources retrieved (5):** `parent_chunk_data_dictionary.txt_2`, `Order Items→ORDER_ITEMS`, `Merchandise→PRODUCTS`, `Order Items`, `parent_chunk_business_glossary.txt_0`

**Context previews (first 3):**

1. _Foreign Keys: - customer_id → CUSTOMERS(customer_id or CustomerID?) - [missing other FK definitions] ========================================== ORDER_ITEMS (or ORDER_DETAILS?) ========================…_

2. _Business concept 'Order Items' — The table is explicitly named ORDER_ITEMS and its columns form a classic order line structure with order_id, product_id, quantity, unit price, discounts, and line tota…_

3. _Business concept 'Merchandise' is implemented by physical table PRODUCTS (columns: product_id, ProductID, product_name, ProductName, product_sku, sku, product_category, category, unit_price, current_p…_

---

### ✅ ec_007 — What's the difference between Revenue and Sales?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.4224 | **Gate:** `proceed`

**Expected answer:**
> Both terms show circular definitions: Revenue is defined as 'Income from sales. The same as... [definition circular, see Sales]', while Sales is defined as 'Revenue from selling products. See Revenue.' The glossary provides no clear distinction between these concepts.

**System answer:**
> The retrieved context does not define Revenue or Sales as financial business terms, so I cannot state a supported difference between them from this knowledge graph.

What the context does show is only the order-related use of “Sales”: the business concept “Sales Order” is mapped to the physical table ORDERS, and it is described as clearly representing “an order placed by a customer.” The ORDERS ta…

**Sources retrieved (5):** `Sales Order→ORDERS`, `parent_chunk_data_dictionary.txt_2`, `parent_chunk_business_glossary.txt_0`, `Sales Order`, `parent_chunk_data_dictionary.txt_1`

**Context previews (first 3):**

1. _Business concept 'Sales Order' — The table contains canonical order-header attributes such as order_id, customer_id, order_date, order_status, and financial totals (amount, shipping, tax), which align…_

2. _Foreign Keys: - customer_id → CUSTOMERS(customer_id or CustomerID?) - [missing other FK definitions] ========================================== ORDER_ITEMS (or ORDER_DETAILS?) ========================…_

3. _BUSINESS GLOSSARY - Enterprise System Last Updated: 2024-03-15 Status: Partial (pending review) ========================================== CUSTOMER MANAGEMENT =========================================…_

---

### ✅ ec_008 — Can one order have multiple payments?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0981 | **Gate:** `proceed_with_warning`

**Expected answer:**
> The PAYMENTS table has an order_id column, suggesting a many-to-one relationship (multiple payments can reference a single order). However, the relationship section in the glossary asks 'Or is it one-to-one?' indicating uncertainty. The ORDERS table has both payment_status and payment_method columns…

**System answer:**
> The retrieved context does not explicitly say whether one order can have multiple payments.

What it does say is that PAYMENTS includes order_id as a foreign key that references ORDERS, and ORDERS is the physical table for the business concept “Sales Order.” That establishes that a payment row can be linked to an order through PAYMENTS.order_id → ORDERS.order_id. However, the context does not docu…

**Sources retrieved (5):** `parent_chunk_data_dictionary.txt_3`, `Sales Order→ORDERS`, `Payment gateway response→PAYMENTS`, `parent_chunk_data_dictionary.txt_2`, `parent_chunk_business_glossary.txt_0`

**Context previews (first 3):**

1. _========================================== PAYMENTS ==========================================  Primary Key: payment_id (unverified) | Column Name | Data Type | Constraints | Description | |----------…_

2. _Business concept 'Sales Order' — The table contains canonical order-header attributes such as order_id, customer_id, order_date, order_status, and financial totals (amount, shipping, tax), which align…_

3. _Business concept 'Payment gateway response' is implemented by physical table PAYMENTS (columns: payment_id, PaymentID, order_id, customer_id, payment_date, payment_amount, payment_method, payment_stat…_

---

### ✅ ec_009 — What payment methods are accepted?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.1791 | **Gate:** `proceed_with_warning`

**Expected answer:**
> The PAYMENTS table has a payment_method column (VARCHAR(30)), but the data dictionary notes '[missing valid values]' and no CHECK constraint exists to enumerate acceptable methods. The schema does not document what values are valid (e.g., credit_card, debit, paypal, etc.).

**System answer:**
> The retrieved context does not list the accepted payment methods.

It shows a `payment_method` column in both `PAYMENTS` and `ORDERS`, but for `PAYMENTS` the documentation explicitly says “[missing valid values],” and no enumerated values are provided anywhere in the context. So, from the available knowledge graph, I can only say that payment method is captured in `PAYMENTS.payment_method` and `OR…

**Sources retrieved (5):** `parent_chunk_data_dictionary.txt_3`, `Payment gateway response→PAYMENTS`, `Sales Order→ORDERS`, `parent_chunk_business_glossary.txt_0`, `Payment gateway response`

**Context previews (first 3):**

1. _========================================== PAYMENTS ==========================================  Primary Key: payment_id (unverified) | Column Name | Data Type | Constraints | Description | |----------…_

2. _Business concept 'Payment gateway response' is implemented by physical table PAYMENTS (columns: payment_id, PaymentID, order_id, customer_id, payment_date, payment_amount, payment_method, payment_stat…_

3. _Business concept 'Sales Order' — The table contains canonical order-header attributes such as order_id, customer_id, order_date, order_status, and financial totals (amount, shipping, tax), which align…_

---

### ✅ ec_010 — What's the correct table name: ORDER_ITEMS or ORDER_DETAILS?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.9938 | **Gate:** `proceed`

**Expected answer:**
> The DDL creates a table named ORDER_ITEMS, but the data dictionary header shows 'ORDER_ITEMS (or ORDER_DETAILS?)' and notes 'Table name ambiguity: ORDER_ITEMS vs ORDER_DETAILS'. The actual table name in the schema is ORDER_ITEMS, but documentation suggests the application may reference it differentl…

**System answer:**
> Based on the retrieved context, the correct table name is ORDER_ITEMS.

The strongest evidence is that the business concept "Order Items" is explicitly mapped to the physical table ORDER_ITEMS, and the context states that "the table is explicitly named ORDER_ITEMS." The mention of "ORDER_DETAILS?" appears only as an uncertainty in incomplete documentation, not as the confirmed physical table name.

**Sources retrieved (5):** `parent_chunk_data_dictionary.txt_2`, `Order Items→ORDER_ITEMS`, `Order Items`, `Sales Order→ORDERS`, `Sales Order`

**Context previews (first 3):**

1. _Foreign Keys: - customer_id → CUSTOMERS(customer_id or CustomerID?) - [missing other FK definitions] ========================================== ORDER_ITEMS (or ORDER_DETAILS?) ========================…_

2. _Business concept 'Order Items' — The table is explicitly named ORDER_ITEMS and its columns form a classic order line structure with order_id, product_id, quantity, unit price, discounts, and line tota…_

3. _Order Items: The table is explicitly named ORDER_ITEMS and its columns form a classic order line structure with order_id, product_id, quantity, unit price, discounts, and line total. Duplicate legacy …_

---

### ✅ ec_011 — Which date column should be used to track when an order was created: order_date, OrderDate, or created_at?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.7679 | **Gate:** `proceed`

**Expected answer:**
> The ORDERS table has three date-related columns: order_date (DATE type), OrderDate (DATETIME type with different precision), and created_at (TIMESTAMP type). The data dictionary provides no guidance on which is actually used by the application or why three columns exist for potentially the same purp…

**System answer:**
> From the retrieved context, `order_date` is the strongest candidate to track when the order was created/placed.

The reason is that the business concept “Sales Order” says the table contains canonical order-header attributes such as `order_id`, `customer_id`, `order_date`, `order_status`, and financial totals. That makes `order_date` the canonical business date for the order. `OrderDate` appears t…

**Sources retrieved (5):** `Sales Order→ORDERS`, `Payment gateway response→PAYMENTS`, `parent_chunk_data_dictionary.txt_1`, `parent_chunk_data_dictionary.txt_3`, `CUSTOMERS→CUSTOMERS`

**Context previews (first 3):**

1. _Business concept 'Sales Order' — The table contains canonical order-header attributes such as order_id, customer_id, order_date, order_status, and financial totals (amount, shipping, tax), which align…_

2. _Business concept 'Payment gateway response' is implemented by physical table PAYMENTS (columns: payment_id, PaymentID, order_id, customer_id, payment_date, payment_amount, payment_method, payment_stat…_

3. _DATA DICTIONARY - Enterprise Database Version: 2.1 (incomplete documentation) Last Updated: 2024-02-28 ========================================== CUSTOMERS ========================================== P…_

---

### ✅ ec_012 — What does the Failed order status mean?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0031 | **Gate:** `proceed_with_warning`

**Expected answer:**
> The business glossary lists Failed as an order status but marks it as '[definition missing]'. Other statuses have definitions (Pending, Processing, Completed, Cancelled, On Hold), but Failed is undefined despite being a valid status value.

**System answer:**
> The retrieved context does not define a “Failed” order status.

What it does show is that the business concept Sales Order is implemented by the ORDERS table, and that ORDERS includes an order_status column alongside order_id, customer_id, and order_date. The glossary also says an Order “can be in various states.” However, no valid values or meanings for order_status are documented in the retrieve…

**Sources retrieved (5):** `Sales Order→ORDERS`, `parent_chunk_data_dictionary.txt_3`, `parent_chunk_data_dictionary.txt_1`, `parent_chunk_business_glossary.txt_0`, `Sales Order`

**Context previews (first 3):**

1. _Business concept 'Sales Order' — The table contains canonical order-header attributes such as order_id, customer_id, order_date, order_status, and financial totals (amount, shipping, tax), which align…_

2. _========================================== PAYMENTS ==========================================  Primary Key: payment_id (unverified) | Column Name | Data Type | Constraints | Description | |----------…_

3. _DATA DICTIONARY - Enterprise Database Version: 2.1 (incomplete documentation) Last Updated: 2024-02-28 ========================================== CUSTOMERS ========================================== P…_

---

### ✅ ec_013 — Are there any NOT NULL constraints defined in the schema?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.7628 | **Gate:** `proceed`

**Expected answer:**
> No NOT NULL constraints are defined in the DDL. The data dictionary explicitly states 'NOT NULL constraints not defined' under 'Missing Documentation' and notes 'assumed, not verified'. All columns are nullable by default.

**System answer:**
> No explicit NOT NULL constraints are shown in the retrieved context.

The schema excerpts list constraints such as PK, FK, and possibly UNIQUE on some columns, but none of the displayed column definitions explicitly say NOT NULL. For example, in CUSTOMERS, PAYMENTS, and ORDER_ITEMS, many constraint entries are shown as ?, missing documentation, or inferred relationships, not NOT NULL.

The only nu…

**Sources retrieved (5):** `parent_chunk_data_dictionary.txt_3`, `parent_chunk_data_dictionary.txt_2`, `Order Items→ORDER_ITEMS`, `parent_chunk_data_dictionary.txt_1`, `Order Items`

**Context previews (first 3):**

1. _========================================== PAYMENTS ==========================================  Primary Key: payment_id (unverified) | Column Name | Data Type | Constraints | Description | |----------…_

2. _Foreign Keys: - customer_id → CUSTOMERS(customer_id or CustomerID?) - [missing other FK definitions] ========================================== ORDER_ITEMS (or ORDER_DETAILS?) ========================…_

3. _Business concept 'Order Items' — The table is explicitly named ORDER_ITEMS and its columns form a classic order line structure with order_id, product_id, quantity, unit price, discounts, and line tota…_

---

### ✅ ec_014 — What's the difference between unit_price and current_price in PRODUCTS?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.5008 | **Gate:** `proceed`

**Expected answer:**
> The PRODUCTS table has both unit_price and current_price columns (both DECIMAL(10,2)). The data dictionary asks 'Different from unit_price?' but provides no explanation of the distinction or when each would be used.

**System answer:**
> From the retrieved context, I can only say that the business concept “Merchandise” is implemented by the PRODUCTS table, and that PRODUCTS includes both unit_price and current_price as separate columns.

The context does not define the semantic difference between unit_price and current_price within PRODUCTS. There is no column description for either one in the PRODUCTS mapping.

The only related d…

**Sources retrieved (5):** `Merchandise→PRODUCTS`, `parent_chunk_data_dictionary.txt_2`, `Order Items→ORDER_ITEMS`, `Order Items`, `parent_chunk_business_glossary.txt_0`

**Context previews (first 3):**

1. _Business concept 'Merchandise' is implemented by physical table PRODUCTS (columns: product_id, ProductID, product_name, ProductName, product_sku, sku, product_category, category, unit_price, current_p…_

2. _Foreign Keys: - customer_id → CUSTOMERS(customer_id or CustomerID?) - [missing other FK definitions] ========================================== ORDER_ITEMS (or ORDER_DETAILS?) ========================…_

3. _Business concept 'Order Items' — The table is explicitly named ORDER_ITEMS and its columns form a classic order line structure with order_id, product_id, quantity, unit price, discounts, and line tota…_

---

### ✅ ec_015 — When is an invoice generated vs payment processed?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.6598 | **Gate:** `proceed`

**Expected answer:**
> The relationship section in the glossary asks 'An invoice is generated for an order. But when? And can one order have multiple invoices?' indicating the timing and cardinality are not defined. The glossary defines Invoice as 'A document requesting payment. Related to Bill' and Payment as 'The transf…

**System answer:**
> From the retrieved context, I cannot determine when an invoice is generated, because there is no invoice table, invoice column, or business glossary entry for “Invoice,” and no lifecycle rule describing invoice creation.

What the context does show is how payment processing is represented at the schema level. The `PAYMENTS` table contains `payment_id`, `order_id`, `customer_id`, `payment_date`, `p…

**Sources retrieved (5):** `parent_chunk_data_dictionary.txt_3`, `Sales Order→ORDERS`, `parent_chunk_data_dictionary.txt_1`, `parent_chunk_data_dictionary.txt_2`, `parent_chunk_business_glossary.txt_0`

**Context previews (first 3):**

1. _========================================== PAYMENTS ==========================================  Primary Key: payment_id (unverified) | Column Name | Data Type | Constraints | Description | |----------…_

2. _Business concept 'Sales Order' — The table contains canonical order-header attributes such as order_id, customer_id, order_date, order_status, and financial totals (amount, shipping, tax), which align…_

3. _DATA DICTIONARY - Enterprise Database Version: 2.1 (incomplete documentation) Last Updated: 2024-02-28 ========================================== CUSTOMERS ========================================== P…_

---

### ✅ ec_016 — Is the sku column in PRODUCTS unique?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.3933 | **Gate:** `proceed`

**Expected answer:**
> The PRODUCTS table has both product_sku and sku columns. The data dictionary notes sku 'should be UNIQUE?' but the DDL does not define a UNIQUE constraint on either column. No index is documented for these columns.

**System answer:**
> The retrieved context does not state that `sku` in `PRODUCTS` is unique. It only shows that the `PRODUCTS` table includes `product_sku` and `sku` as columns under the business concept `Merchandise`, but no uniqueness constraint is documented for either column.

**Sources retrieved (5):** `Merchandise→PRODUCTS`, `parent_chunk_data_dictionary.txt_2`, `parent_chunk_data_dictionary.txt_3`, `parent_chunk_business_glossary.txt_0`, `Order Items`

**Context previews (first 3):**

1. _Business concept 'Merchandise' is implemented by physical table PRODUCTS (columns: product_id, ProductID, product_name, ProductName, product_sku, sku, product_category, category, unit_price, current_p…_

2. _Foreign Keys: - customer_id → CUSTOMERS(customer_id or CustomerID?) - [missing other FK definitions] ========================================== ORDER_ITEMS (or ORDER_DETAILS?) ========================…_

3. _========================================== PAYMENTS ==========================================  Primary Key: payment_id (unverified) | Column Name | Data Type | Constraints | Description | |----------…_

---

### ✅ ec_017 — What is the relationship between customers and orders?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0859 | **Gate:** `proceed_with_warning`

**Expected answer:**
> The glossary states 'A customer can place multiple orders. Or is it accounts that place orders?' indicating uncertainty about the relationship. The ORDERS table has both customer_id and CustomerID columns with ambiguous FK references, and the data dictionary notes they reference 'customer (which tab…

**System answer:**
> The relationship is that ORDERS is linked to CUSTOMERS through the customer_id field. In the retrieved context, the Sales Order concept is implemented by the ORDERS table, which includes customer_id (and also a duplicate variant CustomerID). A foreign key definition also states customer_id → CUSTOMERS(customer_id or CustomerID?).

Based on that schema metadata, an order is associated with a custom…

**Sources retrieved (5):** `parent_chunk_data_dictionary.txt_3`, `Sales Order→ORDERS`, `parent_chunk_data_dictionary.txt_2`, `parent_chunk_business_glossary.txt_0`, `Sales Order`

**Context previews (first 3):**

1. _========================================== PAYMENTS ==========================================  Primary Key: payment_id (unverified) | Column Name | Data Type | Constraints | Description | |----------…_

2. _Business concept 'Sales Order' — The table contains canonical order-header attributes such as order_id, customer_id, order_date, order_status, and financial totals (amount, shipping, tax), which align…_

3. _Foreign Keys: - customer_id → CUSTOMERS(customer_id or CustomerID?) - [missing other FK definitions] ========================================== ORDER_ITEMS (or ORDER_DETAILS?) ========================…_

---

### ✅ ec_018 — Which price column represents what the customer actually pays?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0581 | **Gate:** `proceed_with_warning`

**Expected answer:**
> Multiple price columns exist across tables: ORDERS has orderAmount and total_amount; ORDER_ITEMS has unit_price and UnitPrice; PRODUCTS has unit_price, current_price, and cost_price. The data dictionary does not explain which represents the final customer price, whether discounts are applied, or how…

**System answer:**
> The retrieved context does not identify any single column as definitively “what the customer actually pays.”

What is known from the context is:

In ORDERS, the Sales Order table includes financial total fields: orderAmount, total_amount, shippingAmount, tax_amount, and TaxAmount. The business concept description says these are “financial totals (amount, shipping, tax),” but it does not define whi…

**Sources retrieved (5):** `Payment gateway response→PAYMENTS`, `Sales Order→ORDERS`, `parent_chunk_data_dictionary.txt_2`, `parent_chunk_business_glossary.txt_0`, `Sales Order`

**Context previews (first 3):**

1. _Business concept 'Payment gateway response' is implemented by physical table PAYMENTS (columns: payment_id, PaymentID, order_id, customer_id, payment_date, payment_amount, payment_method, payment_stat…_

2. _Business concept 'Sales Order' — The table contains canonical order-header attributes such as order_id, customer_id, order_date, order_status, and financial totals (amount, shipping, tax), which align…_

3. _Foreign Keys: - customer_id → CUSTOMERS(customer_id or CustomerID?) - [missing other FK definitions] ========================================== ORDER_ITEMS (or ORDER_DETAILS?) ========================…_

---

### ✅ ec_019 — What's the difference between Shipment, Delivery, and Fulfillment?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0050 | **Gate:** `proceed_with_warning`

**Expected answer:**
> The glossary provides definitions but unclear boundaries: Shipment is 'The process of delivering goods to a customer'; Delivery is 'The completion of a Shipment when goods reach the customer'; Fulfillment is 'The process of preparing and delivering orders. Encompasses Shipment and Delivery.' The exa…

**System answer:**
> The provided context does not define Shipment, Delivery, or Fulfillment, so their differences cannot be determined from the available information.

The only related concepts present are:
Order — “A request to purchase products or services. Can be in various states.”
Sales Order — represented by table ORDERS, with order-header attributes such as order_id, customer_id, order_date, order_status, and …

**Sources retrieved (5):** `Sales Order→ORDERS`, `parent_chunk_data_dictionary.txt_2`, `parent_chunk_business_glossary.txt_0`, `Sales Order`, `parent_chunk_data_dictionary.txt_1`

**Context previews (first 3):**

1. _Business concept 'Sales Order' — The table contains canonical order-header attributes such as order_id, customer_id, order_date, order_status, and financial totals (amount, shipping, tax), which align…_

2. _Foreign Keys: - customer_id → CUSTOMERS(customer_id or CustomerID?) - [missing other FK definitions] ========================================== ORDER_ITEMS (or ORDER_DETAILS?) ========================…_

3. _BUSINESS GLOSSARY - Enterprise System Last Updated: 2024-03-15 Status: Partial (pending review) ========================================== CUSTOMER MANAGEMENT =========================================…_

---

### ✅ ec_020 — Are foreign key constraints enforced in the schema?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.1603 | **Gate:** `proceed_with_warning`

**Expected answer:**
> No foreign key constraints are enforced in the DDL. While the data dictionary documents FK relationships (e.g., customer_id → CUSTOMERS, order_id → ORDERS), the actual CREATE TABLE statements omit the REFERENCES clauses. The schema explicitly notes 'FK constraints defined in data dictionary but not …

**System answer:**
> The retrieved context does not confirm that foreign key constraints are enforced at the database level.

It does show documented foreign key relationships in the schema metadata:
ORDER_ITEMS has order_id marked as FK to ORDERS and product_id marked as FK to PRODUCTS (with uncertainty noted as “or INVENTORY?”), and PAYMENTS has order_id marked as FK to ORDERS and customer_id marked as FK to CUSTOME…

**Sources retrieved (5):** `parent_chunk_data_dictionary.txt_2`, `parent_chunk_data_dictionary.txt_3`, `parent_chunk_data_dictionary.txt_1`, `Order Items→ORDER_ITEMS`, `Order Items`

**Context previews (first 3):**

1. _Foreign Keys: - customer_id → CUSTOMERS(customer_id or CustomerID?) - [missing other FK definitions] ========================================== ORDER_ITEMS (or ORDER_DETAILS?) ========================…_

2. _========================================== PAYMENTS ==========================================  Primary Key: payment_id (unverified) | Column Name | Data Type | Constraints | Description | |----------…_

3. _DATA DICTIONARY - Enterprise Database Version: 2.1 (incomplete documentation) Last Updated: 2024-02-28 ========================================== CUSTOMERS ========================================== P…_

---

## Anomalies & Observations

No anomalies detected. All questions grounded with acceptable RAGAS scores.
