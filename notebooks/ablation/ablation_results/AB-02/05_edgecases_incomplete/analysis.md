# AB-02 — 05_edgecases_incomplete — Run Analysis

**Timestamp:** 2026-03-31 01:54:21  
**Run tag:** `v5`

## Configuration

| Parameter | Value |
|-----------|-------|
| Extraction model | `LLM (gpt-5.4-nano-2026-03-17)` |
| Reasoning model | `gpt-5.4-2026-03-05` |
| Embedding model | `BAAI/bge-m3` |
| Retrieval mode | `bm25` |
| Reranker | `True` |
| Reranker top_k | `12` |
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
| Avg Top Score | 0.4073 |
| Avg Chunk Count | 6.3 |
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
> From the BUSINESS GLOSSARY, a Customer is “an individual or organization that...” but the definition is incomplete in the retrieved context.

Related terms in the same glossary help clarify the concept:
Client is “a person or company that purchases goods or services” and may be used interchangeably with Customer in some contexts.
Account Holder is the primary owner of an account and is similar to …

**Sources retrieved (6):** `parent_chunk_data_dictionary.txt_1`, `parent_chunk_data_dictionary.txt_3`, `parent_chunk_business_glossary.txt_0`, `Sales Order`, `Order Items`, `Payment gateway response`

**Context previews (first 3):**

1. _DATA DICTIONARY - Enterprise Database Version: 2.1 (incomplete documentation) Last Updated: 2024-02-28 ========================================== CUSTOMERS ========================================== P…_

2. _========================================== PAYMENTS ==========================================  Primary Key: payment_id (unverified) | Column Name | Data Type | Constraints | Description | |----------…_

3. _BUSINESS GLOSSARY - Enterprise System Last Updated: 2024-03-15 Status: Partial (pending review) ========================================== CUSTOMER MANAGEMENT =========================================…_

---

### ✅ ec_002 — What's the difference between firstName and first_name in the CUSTOMERS table?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.3978 | **Gate:** `proceed`

**Expected answer:**
> Both columns exist in the CUSTOMERS table with identical VARCHAR(50) data types. The data dictionary notes they appear to be duplicates resulting from inconsistent naming conventions (snake_case vs camelCase), but the actual usage by the application is not documented.

**System answer:**
> Based on the retrieved context, there is no documented business difference between `firstName` and `first_name` in the `CUSTOMERS` table.

The data dictionary shows:

`firstName` is `VARCHAR(50)` and described as “Customer's first name.”
`first_name` is also `VARCHAR(50)` and is marked as “[appears to be duplicate].”

So, from the available documentation, both columns appear to represent the same …

**Sources retrieved (6):** `parent_chunk_data_dictionary.txt_1`, `parent_chunk_data_dictionary.txt_3`, `parent_chunk_business_glossary.txt_0`, `Sales Order`, `Order Items`, `Payment gateway response`

**Context previews (first 3):**

1. _DATA DICTIONARY - Enterprise Database Version: 2.1 (incomplete documentation) Last Updated: 2024-02-28 ========================================== CUSTOMERS ========================================== P…_

2. _========================================== PAYMENTS ==========================================  Primary Key: payment_id (unverified) | Column Name | Data Type | Constraints | Description | |----------…_

3. _BUSINESS GLOSSARY - Enterprise System Last Updated: 2024-03-15 Status: Partial (pending review) ========================================== CUSTOMER MANAGEMENT =========================================…_

---

### ✅ ec_003 — Which customer column should be used as a foreign key reference: customer_id or CustomerID?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.9258 | **Gate:** `proceed`

**Expected answer:**
> The CUSTOMERS table has both customer_id (defined as PRIMARY KEY) and CustomerID (defined as INTEGER with no constraints). The ORDERS table also has both customer_id and CustomerID columns with ambiguous FK references. The data dictionary indicates this inconsistency is documented but not yet resolv…

**System answer:**
> Based on the retrieved context, customer_id appears to be the intended foreign key reference, but it is not definitively confirmed.

The strongest evidence is:
The CUSTOMERS table lists “Primary Key: customer_id (or is it CustomerID? check with DBA)”, which suggests customer_id is the primary/canonical key and CustomerID is a possible duplicate naming variant.
The foreign key notes show “customer_…

**Sources retrieved (6):** `parent_chunk_data_dictionary.txt_2`, `parent_chunk_data_dictionary.txt_1`, `parent_chunk_data_dictionary.txt_3`, `Sales Order`, `parent_chunk_business_glossary.txt_0`, `Order Items`

**Context previews (first 3):**

1. _Foreign Keys: - customer_id → CUSTOMERS(customer_id or CustomerID?) - [missing other FK definitions] ========================================== ORDER_ITEMS (or ORDER_DETAILS?) ========================…_

2. _DATA DICTIONARY - Enterprise Database Version: 2.1 (incomplete documentation) Last Updated: 2024-02-28 ========================================== CUSTOMERS ========================================== P…_

3. _========================================== PAYMENTS ==========================================  Primary Key: payment_id (unverified) | Column Name | Data Type | Constraints | Description | |----------…_

---

### ✅ ec_004 — What are the valid values for order_status?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.3954 | **Gate:** `proceed`

**Expected answer:**
> The business glossary documents several order statuses: Pending, Processing, Completed, Cancelled, On Hold, and Failed (which is marked as [definition missing]). However, these are not enforced by a CHECK constraint in the schema, and the data dictionary notes that valid values reference '[missing d…

**System answer:**
> The retrieved context does not list any valid values for `order_status`.

What the context does show is that `order_status` is a canonical attribute of the sales order header: the “Sales Order” concept says the table contains `order_id`, `customer_id`, `order_date`, `order_status`, and financial totals, and the business glossary says an Order “can be in various states.” However, no specific status…

**Sources retrieved (7):** `parent_chunk_data_dictionary.txt_3`, `parent_chunk_data_dictionary.txt_1`, `parent_chunk_data_dictionary.txt_2`, `Sales Order`, `Order Items`, `parent_chunk_business_glossary.txt_0`, `Payment gateway response`

**Context previews (first 3):**

1. _========================================== PAYMENTS ==========================================  Primary Key: payment_id (unverified) | Column Name | Data Type | Constraints | Description | |----------…_

2. _DATA DICTIONARY - Enterprise Database Version: 2.1 (incomplete documentation) Last Updated: 2024-02-28 ========================================== CUSTOMERS ========================================== P…_

3. _Foreign Keys: - customer_id → CUSTOMERS(customer_id or CustomerID?) - [missing other FK definitions] ========================================== ORDER_ITEMS (or ORDER_DETAILS?) ========================…_

---

### ✅ ec_005 — Is there a difference between Product, Item, and SKU?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.5696 | **Gate:** `proceed`

**Expected answer:**
> The glossary indicates these terms are related but distinct: Product is defined as "A thing that is... [definition needs clarification]"; Item is a synonym for Product used in inventory context; SKU (Stock Keeping Unit) is a unique identifier for a product variant; Inventory Item refers to physical …

**System answer:**
> The retrieved context does not provide explicit business definitions that distinguish Product, Item, and SKU.

What it does show is this: in the ORDER_ITEMS concept, the table is described as a classic order line structure with order_id, product_id, quantity, unit price, discounts, and line total. That supports only a limited schema-level interpretation: a product is something referenced on an ord…

**Sources retrieved (6):** `parent_chunk_data_dictionary.txt_1`, `parent_chunk_data_dictionary.txt_3`, `parent_chunk_business_glossary.txt_0`, `Order Items`, `Sales Order`, `Payment gateway response`

**Context previews (first 3):**

1. _DATA DICTIONARY - Enterprise Database Version: 2.1 (incomplete documentation) Last Updated: 2024-02-28 ========================================== CUSTOMERS ========================================== P…_

2. _========================================== PAYMENTS ==========================================  Primary Key: payment_id (unverified) | Column Name | Data Type | Constraints | Description | |----------…_

3. _BUSINESS GLOSSARY - Enterprise System Last Updated: 2024-03-15 Status: Partial (pending review) ========================================== CUSTOMER MANAGEMENT =========================================…_

---

### ✅ ec_006 — Which table should ORDER_ITEMS.product_id reference: PRODUCTS or INVENTORY?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.9609 | **Gate:** `proceed`

**Expected answer:**
> The data dictionary states the FK reference is to 'PRODUCTS (or INVENTORY?)' and notes it is 'not verified'. The schema provides two potential targets: PRODUCTS table (which has product_id) and an INVENTORY table that is referenced in documentation but not defined in the DDL. The actual relationship…

**System answer:**
> The retrieved context does not determine this definitively.

What it does say is that in `ORDER_ITEMS`, the column `product_id` is documented as `INTEGER | FK | References PRODUCTS (or INVENTORY?)`, and there is also a second column `ProductID` marked as `INTEGER | FK | [inconsistent naming]`. The same context also says `ORDER_ITEMS` is explicitly a line-item table with `order_id`, `product_id`, `…

**Sources retrieved (7):** `parent_chunk_data_dictionary.txt_2`, `parent_chunk_data_dictionary.txt_3`, `parent_chunk_data_dictionary.txt_1`, `Order Items`, `parent_chunk_business_glossary.txt_0`, `Sales Order`, `Payment gateway response`

**Context previews (first 3):**

1. _Foreign Keys: - customer_id → CUSTOMERS(customer_id or CustomerID?) - [missing other FK definitions] ========================================== ORDER_ITEMS (or ORDER_DETAILS?) ========================…_

2. _========================================== PAYMENTS ==========================================  Primary Key: payment_id (unverified) | Column Name | Data Type | Constraints | Description | |----------…_

3. _DATA DICTIONARY - Enterprise Database Version: 2.1 (incomplete documentation) Last Updated: 2024-02-28 ========================================== CUSTOMERS ========================================== P…_

---

### ✅ ec_007 — What's the difference between Revenue and Sales?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.4224 | **Gate:** `proceed`

**Expected answer:**
> Both terms show circular definitions: Revenue is defined as 'Income from sales. The same as... [definition circular, see Sales]', while Sales is defined as 'Revenue from selling products. See Revenue.' The glossary provides no clear distinction between these concepts.

**System answer:**
> The retrieved context does not define either Revenue or Sales as business concepts, so I cannot state a factual difference between them from this knowledge graph alone.

What the context does contain is only sales-related schema and glossary evidence:
The Business Glossary defines Order as “a request to purchase products or services” and says it “can be in various states.” It also says Transaction…

**Sources retrieved (5):** `parent_chunk_data_dictionary.txt_3`, `parent_chunk_business_glossary.txt_0`, `Sales Order`, `Order Items`, `Payment gateway response`

**Context previews (first 3):**

1. _========================================== PAYMENTS ==========================================  Primary Key: payment_id (unverified) | Column Name | Data Type | Constraints | Description | |----------…_

2. _BUSINESS GLOSSARY - Enterprise System Last Updated: 2024-03-15 Status: Partial (pending review) ========================================== CUSTOMER MANAGEMENT =========================================…_

3. _Sales Order: The table contains canonical order-header attributes such as order_id, customer_id, order_date, order_status, and financial totals (amount, shipping, tax), which align strongly with a sal…_

---

### ✅ ec_008 — Can one order have multiple payments?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0981 | **Gate:** `proceed_with_warning`

**Expected answer:**
> The PAYMENTS table has an order_id column, suggesting a many-to-one relationship (multiple payments can reference a single order). However, the relationship section in the glossary asks 'Or is it one-to-one?' indicating uncertainty. The ORDERS table has both payment_status and payment_method columns…

**System answer:**
> Based on the retrieved schema, yes, an order can likely have multiple payments.

The evidence is in PAYMENTS: it has payment_id as the primary key and order_id as a foreign key referencing ORDERS. Because the primary key is on payment_id, not on order_id, the structure allows multiple PAYMENTS rows to point to the same order_id. That implies a one-to-many relationship from ORDERS to PAYMENTS.

How…

**Sources retrieved (6):** `parent_chunk_data_dictionary.txt_3`, `parent_chunk_data_dictionary.txt_1`, `parent_chunk_business_glossary.txt_0`, `Sales Order`, `Order Items`, `Payment gateway response`

**Context previews (first 3):**

1. _========================================== PAYMENTS ==========================================  Primary Key: payment_id (unverified) | Column Name | Data Type | Constraints | Description | |----------…_

2. _DATA DICTIONARY - Enterprise Database Version: 2.1 (incomplete documentation) Last Updated: 2024-02-28 ========================================== CUSTOMERS ========================================== P…_

3. _BUSINESS GLOSSARY - Enterprise System Last Updated: 2024-03-15 Status: Partial (pending review) ========================================== CUSTOMER MANAGEMENT =========================================…_

---

### ✅ ec_009 — What payment methods are accepted?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.1791 | **Gate:** `proceed_with_warning`

**Expected answer:**
> The PAYMENTS table has a payment_method column (VARCHAR(30)), but the data dictionary notes '[missing valid values]' and no CHECK constraint exists to enumerate acceptable methods. The schema does not document what values are valid (e.g., credit_card, debit, paypal, etc.).

**System answer:**
> The retrieved context does not specify which payment methods are accepted.

What it does show is that the `PAYMENTS` table includes a `payment_method` column defined as `VARCHAR(30)`, but its documentation explicitly says the valid values are missing. So, from the available schema metadata, I can say that the system records a payment method for each payment, but I cannot enumerate the accepted met…

**Sources retrieved (5):** `parent_chunk_data_dictionary.txt_3`, `parent_chunk_business_glossary.txt_0`, `Payment gateway response`, `Sales Order`, `Order Items`

**Context previews (first 3):**

1. _========================================== PAYMENTS ==========================================  Primary Key: payment_id (unverified) | Column Name | Data Type | Constraints | Description | |----------…_

2. _BUSINESS GLOSSARY - Enterprise System Last Updated: 2024-03-15 Status: Partial (pending review) ========================================== CUSTOMER MANAGEMENT =========================================…_

3. _Payment gateway response…_

---

### ✅ ec_010 — What's the correct table name: ORDER_ITEMS or ORDER_DETAILS?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.9938 | **Gate:** `proceed`

**Expected answer:**
> The DDL creates a table named ORDER_ITEMS, but the data dictionary header shows 'ORDER_ITEMS (or ORDER_DETAILS?)' and notes 'Table name ambiguity: ORDER_ITEMS vs ORDER_DETAILS'. The actual table name in the schema is ORDER_ITEMS, but documentation suggests the application may reference it differentl…

**System answer:**
> The retrieved context indicates the correct table name is ORDER_ITEMS.

The strongest evidence is the business concept entry stating: “The table is explicitly named ORDER_ITEMS.” The schema snippet also labels the section as “ORDER_ITEMS (or ORDER_DETAILS?)”, which shows there was some documentation uncertainty, but the explicit naming in the business concept resolves that uncertainty in favor of …

**Sources retrieved (7):** `parent_chunk_data_dictionary.txt_2`, `parent_chunk_data_dictionary.txt_3`, `parent_chunk_data_dictionary.txt_1`, `Order Items`, `Sales Order`, `parent_chunk_business_glossary.txt_0`, `Payment gateway response`

**Context previews (first 3):**

1. _Foreign Keys: - customer_id → CUSTOMERS(customer_id or CustomerID?) - [missing other FK definitions] ========================================== ORDER_ITEMS (or ORDER_DETAILS?) ========================…_

2. _========================================== PAYMENTS ==========================================  Primary Key: payment_id (unverified) | Column Name | Data Type | Constraints | Description | |----------…_

3. _DATA DICTIONARY - Enterprise Database Version: 2.1 (incomplete documentation) Last Updated: 2024-02-28 ========================================== CUSTOMERS ========================================== P…_

---

### ✅ ec_011 — Which date column should be used to track when an order was created: order_date, OrderDate, or created_at?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.3562 | **Gate:** `proceed`

**Expected answer:**
> The ORDERS table has three date-related columns: order_date (DATE type), OrderDate (DATETIME type with different precision), and created_at (TIMESTAMP type). The data dictionary provides no guidance on which is actually used by the application or why three columns exist for potentially the same purp…

**System answer:**
> Based on the retrieved context, the only order creation-related date column explicitly identified for the sales order entity is order_date. The “Sales Order” concept says the table contains canonical order-header attributes such as order_id, customer_id, order_date, order_status, and financial totals, which indicates order_date is the documented column to track when an order was created.

I cannot…

**Sources retrieved (7):** `parent_chunk_data_dictionary.txt_1`, `parent_chunk_data_dictionary.txt_3`, `parent_chunk_data_dictionary.txt_2`, `Sales Order`, `Order Items`, `parent_chunk_business_glossary.txt_0`, `Payment gateway response`

**Context previews (first 3):**

1. _DATA DICTIONARY - Enterprise Database Version: 2.1 (incomplete documentation) Last Updated: 2024-02-28 ========================================== CUSTOMERS ========================================== P…_

2. _========================================== PAYMENTS ==========================================  Primary Key: payment_id (unverified) | Column Name | Data Type | Constraints | Description | |----------…_

3. _Foreign Keys: - customer_id → CUSTOMERS(customer_id or CustomerID?) - [missing other FK definitions] ========================================== ORDER_ITEMS (or ORDER_DETAILS?) ========================…_

---

### ✅ ec_012 — What does the Failed order status mean?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0031 | **Gate:** `proceed_with_warning`

**Expected answer:**
> The business glossary lists Failed as an order status but marks it as '[definition missing]'. Other statuses have definitions (Pending, Processing, Completed, Cancelled, On Hold), but Failed is undefined despite being a valid status value.

**System answer:**
> The retrieved context does not define the meaning of a specific Failed order status.

What it does show is that a Sales Order is the order-header entity and includes an order_status column, and the glossary says an Order is “a request to purchase products or services” that “can be in various states.” However, no list of order status values is provided, and there is no business definition for Faile…

**Sources retrieved (6):** `parent_chunk_data_dictionary.txt_3`, `parent_chunk_data_dictionary.txt_1`, `parent_chunk_business_glossary.txt_0`, `Sales Order`, `Order Items`, `Payment gateway response`

**Context previews (first 3):**

1. _========================================== PAYMENTS ==========================================  Primary Key: payment_id (unverified) | Column Name | Data Type | Constraints | Description | |----------…_

2. _DATA DICTIONARY - Enterprise Database Version: 2.1 (incomplete documentation) Last Updated: 2024-02-28 ========================================== CUSTOMERS ========================================== P…_

3. _BUSINESS GLOSSARY - Enterprise System Last Updated: 2024-03-15 Status: Partial (pending review) ========================================== CUSTOMER MANAGEMENT =========================================…_

---

### ✅ ec_013 — Are there any NOT NULL constraints defined in the schema?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.7628 | **Gate:** `proceed`

**Expected answer:**
> No NOT NULL constraints are defined in the DDL. The data dictionary explicitly states 'NOT NULL constraints not defined' under 'Missing Documentation' and notes 'assumed, not verified'. All columns are nullable by default.

**System answer:**
> No explicit NOT NULL constraints are defined in the retrieved schema context.

The context shows constraint information such as PK, FK, and possible UNIQUE on columns like PAYMENTS.payment_id, PAYMENTS.order_id, PAYMENTS.customer_id, PAYMENTS.transaction_id, ORDER_ITEMS.order_item_id, ORDER_ITEMS.order_id, ORDER_ITEMS.product_id, and CUSTOMERS.customer_id, but it does not list any column as NOT NU…

**Sources retrieved (7):** `parent_chunk_data_dictionary.txt_3`, `parent_chunk_data_dictionary.txt_2`, `parent_chunk_data_dictionary.txt_1`, `Order Items`, `parent_chunk_business_glossary.txt_0`, `Sales Order`, `Payment gateway response`

**Context previews (first 3):**

1. _========================================== PAYMENTS ==========================================  Primary Key: payment_id (unverified) | Column Name | Data Type | Constraints | Description | |----------…_

2. _Foreign Keys: - customer_id → CUSTOMERS(customer_id or CustomerID?) - [missing other FK definitions] ========================================== ORDER_ITEMS (or ORDER_DETAILS?) ========================…_

3. _DATA DICTIONARY - Enterprise Database Version: 2.1 (incomplete documentation) Last Updated: 2024-02-28 ========================================== CUSTOMERS ========================================== P…_

---

### ✅ ec_014 — What's the difference between unit_price and current_price in PRODUCTS?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0895 | **Gate:** `proceed_with_warning`

**Expected answer:**
> The PRODUCTS table has both unit_price and current_price columns (both DECIMAL(10,2)). The data dictionary asks 'Different from unit_price?' but provides no explanation of the distinction or when each would be used.

**System answer:**
> From the retrieved context, I cannot determine the difference between `unit_price` and `current_price` in `PRODUCTS` because the `PRODUCTS` table definition is not provided, and `current_price` does not appear anywhere in the context.

What is known from the context is only this:
`unit_price` appears in `ORDER_ITEMS` and is described as “Price per unit.”
`ORDER_ITEMS.product_id` is marked as an FK…

**Sources retrieved (6):** `parent_chunk_data_dictionary.txt_2`, `parent_chunk_data_dictionary.txt_3`, `Order Items`, `parent_chunk_business_glossary.txt_0`, `Sales Order`, `Payment gateway response`

**Context previews (first 3):**

1. _Foreign Keys: - customer_id → CUSTOMERS(customer_id or CustomerID?) - [missing other FK definitions] ========================================== ORDER_ITEMS (or ORDER_DETAILS?) ========================…_

2. _========================================== PAYMENTS ==========================================  Primary Key: payment_id (unverified) | Column Name | Data Type | Constraints | Description | |----------…_

3. _Order Items: The table is explicitly named ORDER_ITEMS and its columns form a classic order line structure with order_id, product_id, quantity, unit price, discounts, and line total. Duplicate legacy …_

---

### ✅ ec_015 — When is an invoice generated vs payment processed?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.6604 | **Gate:** `proceed`

**Expected answer:**
> The relationship section in the glossary asks 'An invoice is generated for an order. But when? And can one order have multiple invoices?' indicating the timing and cardinality are not defined. The glossary defines Invoice as 'A document requesting payment. Related to Bill' and Payment as 'The transf…

**System answer:**
> The retrieved context does not define when an invoice is generated. There is no invoice table, invoice business concept, or lifecycle rule in the provided material that states any invoice timing.

The context does provide schema evidence for payment processing. The `PAYMENTS` table represents payments against an order and a customer: `order_id` is an FK to `ORDERS`, and `customer_id` is an FK to `…

**Sources retrieved (7):** `parent_chunk_data_dictionary.txt_3`, `parent_chunk_data_dictionary.txt_1`, `parent_chunk_data_dictionary.txt_2`, `parent_chunk_business_glossary.txt_0`, `Payment gateway response`, `Sales Order`, `Order Items`

**Context previews (first 3):**

1. _========================================== PAYMENTS ==========================================  Primary Key: payment_id (unverified) | Column Name | Data Type | Constraints | Description | |----------…_

2. _DATA DICTIONARY - Enterprise Database Version: 2.1 (incomplete documentation) Last Updated: 2024-02-28 ========================================== CUSTOMERS ========================================== P…_

3. _Foreign Keys: - customer_id → CUSTOMERS(customer_id or CustomerID?) - [missing other FK definitions] ========================================== ORDER_ITEMS (or ORDER_DETAILS?) ========================…_

---

### ✅ ec_016 — Is the sku column in PRODUCTS unique?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.1967 | **Gate:** `proceed_with_warning`

**Expected answer:**
> The PRODUCTS table has both product_sku and sku columns. The data dictionary notes sku 'should be UNIQUE?' but the DDL does not define a UNIQUE constraint on either column. No index is documented for these columns.

**System answer:**
> I cannot determine from the retrieved context whether `PRODUCTS.sku` is unique.

What the context does provide is only indirect evidence about `PRODUCTS`: `ORDER_ITEMS` is explicitly described as the order line table, and it contains `product_id` plus a duplicate legacy-style `ProductID`, with notes saying `product_id` references `PRODUCTS` (or possibly `INVENTORY`, with some documentation uncerta…

**Sources retrieved (7):** `parent_chunk_data_dictionary.txt_2`, `parent_chunk_data_dictionary.txt_3`, `parent_chunk_data_dictionary.txt_1`, `parent_chunk_business_glossary.txt_0`, `Order Items`, `Sales Order`, `Payment gateway response`

**Context previews (first 3):**

1. _Foreign Keys: - customer_id → CUSTOMERS(customer_id or CustomerID?) - [missing other FK definitions] ========================================== ORDER_ITEMS (or ORDER_DETAILS?) ========================…_

2. _========================================== PAYMENTS ==========================================  Primary Key: payment_id (unverified) | Column Name | Data Type | Constraints | Description | |----------…_

3. _DATA DICTIONARY - Enterprise Database Version: 2.1 (incomplete documentation) Last Updated: 2024-02-28 ========================================== CUSTOMERS ========================================== P…_

---

### ✅ ec_017 — What is the relationship between customers and orders?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0859 | **Gate:** `proceed_with_warning`

**Expected answer:**
> The glossary states 'A customer can place multiple orders. Or is it accounts that place orders?' indicating uncertainty about the relationship. The ORDERS table has both customer_id and CustomerID columns with ambiguous FK references, and the data dictionary notes they reference 'customer (which tab…

**System answer:**
> A customer-to-order relationship is indicated directly in the order structure: the Sales Order table contains both order_id and customer_id, and it is described as “an order placed by a customer.” This implies that orders are associated to customers through customer_id in the order header, linking the order to the CUSTOMERS entity.

The CUSTOMERS table has customer_id as the primary key, although …

**Sources retrieved (6):** `parent_chunk_data_dictionary.txt_3`, `parent_chunk_data_dictionary.txt_1`, `parent_chunk_business_glossary.txt_0`, `Sales Order`, `Order Items`, `Payment gateway response`

**Context previews (first 3):**

1. _========================================== PAYMENTS ==========================================  Primary Key: payment_id (unverified) | Column Name | Data Type | Constraints | Description | |----------…_

2. _DATA DICTIONARY - Enterprise Database Version: 2.1 (incomplete documentation) Last Updated: 2024-02-28 ========================================== CUSTOMERS ========================================== P…_

3. _BUSINESS GLOSSARY - Enterprise System Last Updated: 2024-03-15 Status: Partial (pending review) ========================================== CUSTOMER MANAGEMENT =========================================…_

---

### ✅ ec_018 — Which price column represents what the customer actually pays?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0122 | **Gate:** `proceed_with_warning`

**Expected answer:**
> Multiple price columns exist across tables: ORDERS has orderAmount and total_amount; ORDER_ITEMS has unit_price and UnitPrice; PRODUCTS has unit_price, current_price, and cost_price. The data dictionary does not explain which represents the final customer price, whether discounts are applied, or how…

**System answer:**
> From the retrieved context, `unit_price` in `ORDER_ITEMS` is explicitly described as “Price per unit,” so it does not by itself represent what the customer actually pays if discounts apply.

Because `ORDER_ITEMS` also has `discount_percent`, and the business concept says the table includes “quantity, unit price, discounts, and line total,” the column that would most closely represent what the cust…

**Sources retrieved (7):** `parent_chunk_data_dictionary.txt_2`, `parent_chunk_data_dictionary.txt_3`, `parent_chunk_data_dictionary.txt_1`, `parent_chunk_business_glossary.txt_0`, `Sales Order`, `Order Items`, `Payment gateway response`

**Context previews (first 3):**

1. _Foreign Keys: - customer_id → CUSTOMERS(customer_id or CustomerID?) - [missing other FK definitions] ========================================== ORDER_ITEMS (or ORDER_DETAILS?) ========================…_

2. _========================================== PAYMENTS ==========================================  Primary Key: payment_id (unverified) | Column Name | Data Type | Constraints | Description | |----------…_

3. _DATA DICTIONARY - Enterprise Database Version: 2.1 (incomplete documentation) Last Updated: 2024-02-28 ========================================== CUSTOMERS ========================================== P…_

---

### ✅ ec_019 — What's the difference between Shipment, Delivery, and Fulfillment?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0050 | **Gate:** `proceed_with_warning`

**Expected answer:**
> The glossary provides definitions but unclear boundaries: Shipment is 'The process of delivering goods to a customer'; Delivery is 'The completion of a Shipment when goods reach the customer'; Fulfillment is 'The process of preparing and delivering orders. Encompasses Shipment and Delivery.' The exa…

**System answer:**
> The retrieved context does not define Shipment, Delivery, or Fulfillment, so I cannot determine the difference between those terms from the knowledge graph. The available glossary and schema content covers Customer, Client, Account Holder, End User, Order, Transaction, Sales Order, Order Items, and Payments, but not those three concepts.

**Sources retrieved (5):** `parent_chunk_data_dictionary.txt_3`, `parent_chunk_business_glossary.txt_0`, `Sales Order`, `Order Items`, `Payment gateway response`

**Context previews (first 3):**

1. _========================================== PAYMENTS ==========================================  Primary Key: payment_id (unverified) | Column Name | Data Type | Constraints | Description | |----------…_

2. _BUSINESS GLOSSARY - Enterprise System Last Updated: 2024-03-15 Status: Partial (pending review) ========================================== CUSTOMER MANAGEMENT =========================================…_

3. _Sales Order: The table contains canonical order-header attributes such as order_id, customer_id, order_date, order_status, and financial totals (amount, shipping, tax), which align strongly with a sal…_

---

### ✅ ec_020 — Are foreign key constraints enforced in the schema?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.1605 | **Gate:** `proceed_with_warning`

**Expected answer:**
> No foreign key constraints are enforced in the DDL. While the data dictionary documents FK relationships (e.g., customer_id → CUSTOMERS, order_id → ORDERS), the actual CREATE TABLE statements omit the REFERENCES clauses. The schema explicitly notes 'FK constraints defined in data dictionary but not …

**System answer:**
> The retrieved context shows that foreign key relationships are identified in the schema metadata, but it does not confirm that foreign key constraints are actually enforced at the database level.

From the context:
CUSTOMERS is referenced by customer_id in at least one foreign key note.
ORDER_ITEMS includes order_id marked as FK referencing ORDERS, and product_id marked as FK referencing PRODUCTS …

**Sources retrieved (7):** `parent_chunk_data_dictionary.txt_2`, `parent_chunk_data_dictionary.txt_3`, `parent_chunk_data_dictionary.txt_1`, `Order Items`, `parent_chunk_business_glossary.txt_0`, `Sales Order`, `Payment gateway response`

**Context previews (first 3):**

1. _Foreign Keys: - customer_id → CUSTOMERS(customer_id or CustomerID?) - [missing other FK definitions] ========================================== ORDER_ITEMS (or ORDER_DETAILS?) ========================…_

2. _========================================== PAYMENTS ==========================================  Primary Key: payment_id (unverified) | Column Name | Data Type | Constraints | Description | |----------…_

3. _DATA DICTIONARY - Enterprise Database Version: 2.1 (incomplete documentation) Last Updated: 2024-02-28 ========================================== CUSTOMERS ========================================== P…_

---

## Anomalies & Observations

No anomalies detected. All questions grounded with acceptable RAGAS scores.
