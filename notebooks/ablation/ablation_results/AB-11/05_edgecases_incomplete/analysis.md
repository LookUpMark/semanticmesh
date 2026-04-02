# AB-11 — 05_edgecases_incomplete — Run Analysis

**Timestamp:** 2026-04-01 01:25:18  
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
| ER similarity threshold | `0.65` |

## Builder Results

| Metric | Value |
|--------|-------|
| Triplets extracted | 190 |
| Entities resolved | 28 |
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
> In the BUSINESS GLOSSARY, a Customer is only partially defined as “An individual or organization that...”; the definition is incomplete in the retrieved context.

The same glossary says Client is “a person or company that purchases goods or services” and may be used interchangeably with Customer in some contexts. It also distinguishes Account Holder as similar to Customer but with an account-speci…

**Sources retrieved (12):** `parent_chunk_data_dictionary.txt_1`, `Multiple FK references (order_id, customer_id) - unclear relationship→CUSTOMERS`, `parent_chunk_data_dictionary.txt_2`, `Sales Order→ORDERS`, `parent_chunk_data_dictionary.txt_3`, `Multiple FK references (order_id, customer_id) - unclear relationship`, `parent_chunk_business_glossary.txt_0`, `Sales Order`

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

The data dictionary describes `firstName` as `VARCHAR(50)` with the description “Customer's first name,” while `first_name` is also `VARCHAR(50)` and is explicitly noted as “[appears to be duplicate].” Constraints for both are undocumented (`?`), and the overall `CUSTOME…

**Sources retrieved (12):** `Multiple FK references (order_id, customer_id) - unclear relationship→CUSTOMERS`, `parent_chunk_data_dictionary.txt_1`, `parent_chunk_data_dictionary.txt_2`, `Sales Order→ORDERS`, `parent_chunk_data_dictionary.txt_3`, `Inventory Item→PRODUCTS`, `Unknown→ORDER_ITEMS`, `parent_chunk_business_glossary.txt_0`

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
> From the retrieved context, customer_id is the best-supported foreign key reference, but the documentation is inconsistent and does not fully confirm it.

The strongest evidence is that the CUSTOMERS table lists its primary key as “customer_id (or is it CustomerID? check with DBA)”, and CustomerID is described as a “possible duplicate of customer_id.” Also, PAYMENTS defines customer_id as an FK re…

**Sources retrieved (12):** `parent_chunk_data_dictionary.txt_2`, `Multiple FK references (order_id, customer_id) - unclear relationship→CUSTOMERS`, `parent_chunk_data_dictionary.txt_1`, `parent_chunk_data_dictionary.txt_3`, `Sales Order→ORDERS`, `Multiple FK references (order_id, customer_id) - unclear relationship`, `Inventory Item→PRODUCTS`, `Unknown→ORDER_ITEMS`

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
> The retrieved context shows that order_status is a column on the ORDERS table, which implements the Sales Order business concept. The context also says the ORDERS table contains “order lifecycle data,” and the glossary defines an Order as “a request to purchase products or services” that “can be in various states.”

However, the context does not provide any enumerated or documented valid values fo…

**Sources retrieved (12):** `parent_chunk_data_dictionary.txt_3`, `Sales Order→ORDERS`, `parent_chunk_data_dictionary.txt_1`, `parent_chunk_data_dictionary.txt_2`, `parent_chunk_business_glossary.txt_0`, `Multiple FK references (order_id, customer_id) - unclear relationship→CUSTOMERS`, `Unknown→ORDER_ITEMS`, `Inventory Item→PRODUCTS`

**Context previews (first 3):**

1. _========================================== PAYMENTS ==========================================  Primary Key: payment_id (unverified) | Column Name | Data Type | Constraints | Description | |----------…_

2. _Business concept 'Sales Order' — The table centers on order identity, customer linkage, order date, totals, shipping, tax, and status fields, which aligns with an order record rather than payment or s…_

3. _DATA DICTIONARY - Enterprise Database Version: 2.1 (incomplete documentation) Last Updated: 2024-02-28 ========================================== CUSTOMERS ========================================== P…_

---

### ✅ ec_005 — Is there a difference between Product, Item, and SKU?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.5696 | **Gate:** `proceed`

**Expected answer:**
> The glossary indicates these terms are related but distinct: Product is defined as "A thing that is... [definition needs clarification]"; Item is a synonym for Product used in inventory context; SKU (Stock Keeping Unit) is a unique identifier for a product variant; Inventory Item refers to physical …

**System answer:**
> The retrieved context only partially answers this.

It does not provide explicit glossary definitions for Product, Item, or SKU as separate business concepts, so I cannot give a formal enterprise distinction between all three from the knowledge graph.

What it does say is that the physical table PRODUCTS is mapped to the business concept Inventory Item, not to SKU or Product. The reason given is t…

**Sources retrieved (12):** `Inventory Item→PRODUCTS`, `parent_chunk_data_dictionary.txt_2`, `Unknown→ORDER_ITEMS`, `parent_chunk_data_dictionary.txt_1`, `parent_chunk_data_dictionary.txt_3`, `Sales Order→ORDERS`, `parent_chunk_business_glossary.txt_0`, `Inventory Item`

**Context previews (first 3):**

1. _Business concept 'Inventory Item' — The table includes core product identifiers and descriptors, but the explicit stock_quantity, quantity_in_stock, and reorder_level fields make it operational invent…_

2. _Foreign Keys: - customer_id → CUSTOMERS(customer_id or CustomerID?) - [missing other FK definitions] ========================================== ORDER_ITEMS (or ORDER_DETAILS?) ========================…_

3. _Business concept 'Unknown' — This table is a sales order line-item structure: order_item_id, order_id, product_id, quantity, unit_price, discount, and line_total describe individual order lines rather…_

---

### ✅ ec_006 — Which table should ORDER_ITEMS.product_id reference: PRODUCTS or INVENTORY?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.9608 | **Gate:** `proceed`

**Expected answer:**
> The data dictionary states the FK reference is to 'PRODUCTS (or INVENTORY?)' and notes it is 'not verified'. The schema provides two potential targets: PRODUCTS table (which has product_id) and an INVENTORY table that is referenced in documentation but not defined in the DDL. The actual relationship…

**System answer:**
> Based on the retrieved context, ORDER_ITEMS.product_id is documented as a foreign key that references “PRODUCTS (or INVENTORY?)”, so the source documentation is explicitly ambiguous.

However, the same context says the business concept “Inventory Item” is implemented by the physical table PRODUCTS, with columns including product_id, ProductID, stock_quantity, quantity_in_stock, and reorder_level. …

**Sources retrieved (12):** `parent_chunk_data_dictionary.txt_2`, `Inventory Item→PRODUCTS`, `Unknown→ORDER_ITEMS`, `Sales Order→ORDERS`, `Multiple FK references (order_id, customer_id) - unclear relationship→CUSTOMERS`, `Multiple FK references (order_id, customer_id) - unclear relationship`, `parent_chunk_data_dictionary.txt_3`, `parent_chunk_data_dictionary.txt_1`

**Context previews (first 3):**

1. _Foreign Keys: - customer_id → CUSTOMERS(customer_id or CustomerID?) - [missing other FK definitions] ========================================== ORDER_ITEMS (or ORDER_DETAILS?) ========================…_

2. _Business concept 'Inventory Item' — The table includes core product identifiers and descriptors, but the explicit stock_quantity, quantity_in_stock, and reorder_level fields make it operational invent…_

3. _Business concept 'Unknown' — This table is a sales order line-item structure: order_item_id, order_id, product_id, quantity, unit_price, discount, and line_total describe individual order lines rather…_

---

### ✅ ec_007 — What's the difference between Revenue and Sales?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.4224 | **Gate:** `proceed`

**Expected answer:**
> Both terms show circular definitions: Revenue is defined as 'Income from sales. The same as... [definition circular, see Sales]', while Sales is defined as 'Revenue from selling products. See Revenue.' The glossary provides no clear distinction between these concepts.

**System answer:**
> The retrieved context does not provide a business glossary definition for either Revenue or Sales, so I cannot state a validated business difference between those two terms from this knowledge graph alone.

What the context does show is the sales-related side of the model. It defines Sales Order as an order with confirmed pricing and inventory allocation, implemented by ORDERS. That table contains…

**Sources retrieved (12):** `Sales Order→ORDERS`, `Unknown→ORDER_ITEMS`, `parent_chunk_data_dictionary.txt_2`, `Inventory Item→PRODUCTS`, `parent_chunk_data_dictionary.txt_3`, `parent_chunk_business_glossary.txt_0`, `Sales Order`, `Unknown`

**Context previews (first 3):**

1. _Business concept 'Sales Order' — The table centers on order identity, customer linkage, order date, totals, shipping, tax, and status fields, which aligns with an order record rather than payment or s…_

2. _Business concept 'Unknown' — This table is a sales order line-item structure: order_item_id, order_id, product_id, quantity, unit_price, discount, and line_total describe individual order lines rather…_

3. _Foreign Keys: - customer_id → CUSTOMERS(customer_id or CustomerID?) - [missing other FK definitions] ========================================== ORDER_ITEMS (or ORDER_DETAILS?) ========================…_

---

### ✅ ec_008 — Can one order have multiple payments?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0981 | **Gate:** `proceed_with_warning`

**Expected answer:**
> The PAYMENTS table has an order_id column, suggesting a many-to-one relationship (multiple payments can reference a single order). However, the relationship section in the glossary asks 'Or is it one-to-one?' indicating uncertainty. The ORDERS table has both payment_status and payment_method columns…

**System answer:**
> From the retrieved context, it is known that `PAYMENTS` has its own primary key (`payment_id`) and an `order_id` foreign key that references `ORDERS`. That means payments are linked to orders through `PAYMENTS.order_id -> ORDERS.order_id`.

However, the context does not explicitly define the relationship cardinality, and it does not document whether `PAYMENTS.order_id` is unique. Because of that, …

**Sources retrieved (12):** `parent_chunk_data_dictionary.txt_3`, `Sales Order→ORDERS`, `Multiple FK references (order_id, customer_id) - unclear relationship→CUSTOMERS`, `Multiple FK references (order_id, customer_id) - unclear relationship`, `parent_chunk_data_dictionary.txt_2`, `parent_chunk_data_dictionary.txt_1`, `Unknown→ORDER_ITEMS`, `Inventory Item→PRODUCTS`

**Context previews (first 3):**

1. _========================================== PAYMENTS ==========================================  Primary Key: payment_id (unverified) | Column Name | Data Type | Constraints | Description | |----------…_

2. _Business concept 'Sales Order' — The table centers on order identity, customer linkage, order date, totals, shipping, tax, and status fields, which aligns with an order record rather than payment or s…_

3. _Business concept 'Multiple FK references (order_id, customer_id) - unclear relationship' is implemented by physical table CUSTOMERS (columns: customer_id, CustomerID, firstName, first_name, lastName, …_

---

### ✅ ec_009 — What payment methods are accepted?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.1791 | **Gate:** `proceed_with_warning`

**Expected answer:**
> The PAYMENTS table has a payment_method column (VARCHAR(30)), but the data dictionary notes '[missing valid values]' and no CHECK constraint exists to enumerate acceptable methods. The schema does not document what values are valid (e.g., credit_card, debit, paypal, etc.).

**System answer:**
> The retrieved context does not document the accepted payment methods.

It only shows that both PAYMENTS and ORDERS contain a payment_method column:
PAYMENTS.payment_method is VARCHAR(30) with “[missing valid values]”.
ORDERS includes a payment_method column, but no allowed values are listed there either.

So from the knowledge graph, the system tracks payment method, but the accepted methods thems…

**Sources retrieved (12):** `parent_chunk_data_dictionary.txt_3`, `Sales Order→ORDERS`, `parent_chunk_data_dictionary.txt_1`, `parent_chunk_data_dictionary.txt_2`, `parent_chunk_business_glossary.txt_0`, `Sales Order`, `Multiple FK references (order_id, customer_id) - unclear relationship→CUSTOMERS`, `Unknown→ORDER_ITEMS`

**Context previews (first 3):**

1. _========================================== PAYMENTS ==========================================  Primary Key: payment_id (unverified) | Column Name | Data Type | Constraints | Description | |----------…_

2. _Business concept 'Sales Order' — The table centers on order identity, customer linkage, order date, totals, shipping, tax, and status fields, which aligns with an order record rather than payment or s…_

3. _DATA DICTIONARY - Enterprise Database Version: 2.1 (incomplete documentation) Last Updated: 2024-02-28 ========================================== CUSTOMERS ========================================== P…_

---

### ✅ ec_010 — What's the correct table name: ORDER_ITEMS or ORDER_DETAILS?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.9627 | **Gate:** `proceed`

**Expected answer:**
> The DDL creates a table named ORDER_ITEMS, but the data dictionary header shows 'ORDER_ITEMS (or ORDER_DETAILS?)' and notes 'Table name ambiguity: ORDER_ITEMS vs ORDER_DETAILS'. The actual table name in the schema is ORDER_ITEMS, but documentation suggests the application may reference it differentl…

**System answer:**
> Based on the retrieved context, the table name is ORDER_ITEMS.

The strongest evidence is the concept-to-table mapping, which states that the sales order line-item structure “is implemented by physical table ORDER_ITEMS” and lists its columns: order_item_id, order_id, product_id, quantity, unit_price, discount_percent, discount_amount, and line_total. The reference to “ORDER_ITEMS (or ORDER_DETAIL…

**Sources retrieved (12):** `parent_chunk_data_dictionary.txt_2`, `Unknown→ORDER_ITEMS`, `Inventory Item→PRODUCTS`, `parent_chunk_data_dictionary.txt_3`, `Multiple FK references (order_id, customer_id) - unclear relationship→CUSTOMERS`, `parent_chunk_data_dictionary.txt_1`, `Sales Order→ORDERS`, `Multiple FK references (order_id, customer_id) - unclear relationship`

**Context previews (first 3):**

1. _Foreign Keys: - customer_id → CUSTOMERS(customer_id or CustomerID?) - [missing other FK definitions] ========================================== ORDER_ITEMS (or ORDER_DETAILS?) ========================…_

2. _Business concept 'Unknown' — This table is a sales order line-item structure: order_item_id, order_id, product_id, quantity, unit_price, discount, and line_total describe individual order lines rather…_

3. _Business concept 'Inventory Item' — The table includes core product identifiers and descriptors, but the explicit stock_quantity, quantity_in_stock, and reorder_level fields make it operational invent…_

---

### ✅ ec_011 — Which date column should be used to track when an order was created: order_date, OrderDate, or created_at?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.8016 | **Gate:** `proceed`

**Expected answer:**
> The ORDERS table has three date-related columns: order_date (DATE type), OrderDate (DATETIME type with different precision), and created_at (TIMESTAMP type). The data dictionary provides no guidance on which is actually used by the application or why three columns exist for potentially the same purp…

**System answer:**
> From the retrieved context alone, this cannot be determined definitively.

What is known is that the `ORDERS` table contains all three columns: `order_date`, `OrderDate`, and `created_at`. The `Sales Order` concept says the table includes “order date” and other lifecycle fields, but the context does not provide a data dictionary entry for `ORDERS` that defines these columns individually. It also s…

**Sources retrieved (12):** `Sales Order→ORDERS`, `Multiple FK references (order_id, customer_id) - unclear relationship→CUSTOMERS`, `parent_chunk_data_dictionary.txt_1`, `parent_chunk_data_dictionary.txt_3`, `Inventory Item→PRODUCTS`, `parent_chunk_data_dictionary.txt_2`, `Unknown→ORDER_ITEMS`, `Multiple FK references (order_id, customer_id) - unclear relationship`

**Context previews (first 3):**

1. _Business concept 'Sales Order' — The table centers on order identity, customer linkage, order date, totals, shipping, tax, and status fields, which aligns with an order record rather than payment or s…_

2. _Business concept 'Multiple FK references (order_id, customer_id) - unclear relationship' is implemented by physical table CUSTOMERS (columns: customer_id, CustomerID, firstName, first_name, lastName, …_

3. _DATA DICTIONARY - Enterprise Database Version: 2.1 (incomplete documentation) Last Updated: 2024-02-28 ========================================== CUSTOMERS ========================================== P…_

---

### ✅ ec_012 — What does the Failed order status mean?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0033 | **Gate:** `proceed_with_warning`

**Expected answer:**
> The business glossary lists Failed as an order status but marks it as '[definition missing]'. Other statuses have definitions (Pending, Processing, Completed, Cancelled, On Hold), but Failed is undefined despite being a valid status value.

**System answer:**
> The retrieved context does not define a specific meaning for the order status value "Failed."

What the context does show is that the Sales Order concept is implemented by the ORDERS table, which includes an order_status column along with order lifecycle fields, and the glossary says an Order is "a request to purchase products or services" that "can be in various states." However, no valid values …

**Sources retrieved (12):** `Sales Order→ORDERS`, `parent_chunk_data_dictionary.txt_3`, `parent_chunk_data_dictionary.txt_1`, `parent_chunk_data_dictionary.txt_2`, `Multiple FK references (order_id, customer_id) - unclear relationship→CUSTOMERS`, `Inventory Item→PRODUCTS`, `Unknown→ORDER_ITEMS`, `Multiple FK references (order_id, customer_id) - unclear relationship`

**Context previews (first 3):**

1. _Business concept 'Sales Order' — The table centers on order identity, customer linkage, order date, totals, shipping, tax, and status fields, which aligns with an order record rather than payment or s…_

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

The schema excerpts show constraints such as PK, FK, and UNIQUE?, and many columns are marked with ?, but none of the provided table definitions for CUSTOMERS, PAYMENTS, ORDER_ITEMS, ORDERS, or PRODUCTS explicitly list a NOT NULL constraint. The documentation is also marked as incomplete, so the context does not confirm whethe…

**Sources retrieved (12):** `parent_chunk_data_dictionary.txt_3`, `parent_chunk_data_dictionary.txt_2`, `parent_chunk_data_dictionary.txt_1`, `Sales Order→ORDERS`, `parent_chunk_business_glossary.txt_0`, `Unknown→ORDER_ITEMS`, `Multiple FK references (order_id, customer_id) - unclear relationship→CUSTOMERS`, `Inventory Item→PRODUCTS`

**Context previews (first 3):**

1. _========================================== PAYMENTS ==========================================  Primary Key: payment_id (unverified) | Column Name | Data Type | Constraints | Description | |----------…_

2. _Foreign Keys: - customer_id → CUSTOMERS(customer_id or CustomerID?) - [missing other FK definitions] ========================================== ORDER_ITEMS (or ORDER_DETAILS?) ========================…_

3. _DATA DICTIONARY - Enterprise Database Version: 2.1 (incomplete documentation) Last Updated: 2024-02-28 ========================================== CUSTOMERS ========================================== P…_

---

### ✅ ec_014 — What's the difference between unit_price and current_price in PRODUCTS?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.5268 | **Gate:** `proceed`

**Expected answer:**
> The PRODUCTS table has both unit_price and current_price columns (both DECIMAL(10,2)). The data dictionary asks 'Different from unit_price?' but provides no explanation of the distinction or when each would be used.

**System answer:**
> The retrieved context does not define any semantic difference between PRODUCTS.unit_price and PRODUCTS.current_price.

What the context does say is only that the PRODUCTS table includes both columns as part of the physical table implementing the business concept Inventory Item: product_id, ProductID, product_name, ProductName, product_sku, sku, product_category, category, unit_price, current_price…

**Sources retrieved (12):** `Inventory Item→PRODUCTS`, `parent_chunk_data_dictionary.txt_2`, `Unknown→ORDER_ITEMS`, `Sales Order→ORDERS`, `parent_chunk_data_dictionary.txt_3`, `Unknown`, `parent_chunk_business_glossary.txt_0`, `Inventory Item`

**Context previews (first 3):**

1. _Business concept 'Inventory Item' — The table includes core product identifiers and descriptors, but the explicit stock_quantity, quantity_in_stock, and reorder_level fields make it operational invent…_

2. _Foreign Keys: - customer_id → CUSTOMERS(customer_id or CustomerID?) - [missing other FK definitions] ========================================== ORDER_ITEMS (or ORDER_DETAILS?) ========================…_

3. _Business concept 'Unknown' — This table is a sales order line-item structure: order_item_id, order_id, product_id, quantity, unit_price, discount, and line_total describe individual order lines rather…_

---

### ✅ ec_015 — When is an invoice generated vs payment processed?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.6598 | **Gate:** `proceed`

**Expected answer:**
> The relationship section in the glossary asks 'An invoice is generated for an order. But when? And can one order have multiple invoices?' indicating the timing and cardinality are not defined. The glossary defines Invoice as 'A document requesting payment. Related to Bill' and Payment as 'The transf…

**System answer:**
> The retrieved context does not document invoice generation at all. There is no invoice table, no invoice business concept, and no lifecycle rule that says when an invoice is created relative to an order or a payment. So that part cannot be answered from the available knowledge graph.

What the context does cover is payment processing at a schema level. The PAYMENTS table is the payment record stru…

**Sources retrieved (12):** `parent_chunk_data_dictionary.txt_3`, `Sales Order→ORDERS`, `parent_chunk_data_dictionary.txt_1`, `parent_chunk_data_dictionary.txt_2`, `parent_chunk_business_glossary.txt_0`, `Sales Order`, `Inventory Item→PRODUCTS`, `Unknown→ORDER_ITEMS`

**Context previews (first 3):**

1. _========================================== PAYMENTS ==========================================  Primary Key: payment_id (unverified) | Column Name | Data Type | Constraints | Description | |----------…_

2. _Business concept 'Sales Order' — The table centers on order identity, customer linkage, order date, totals, shipping, tax, and status fields, which aligns with an order record rather than payment or s…_

3. _DATA DICTIONARY - Enterprise Database Version: 2.1 (incomplete documentation) Last Updated: 2024-02-28 ========================================== CUSTOMERS ========================================== P…_

---

### ✅ ec_016 — Is the sku column in PRODUCTS unique?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.4929 | **Gate:** `proceed`

**Expected answer:**
> The PRODUCTS table has both product_sku and sku columns. The data dictionary notes sku 'should be UNIQUE?' but the DDL does not define a UNIQUE constraint on either column. No index is documented for these columns.

**System answer:**
> The retrieved context does not state that PRODUCTS.sku or PRODUCTS.product_sku is unique. The PRODUCTS table is described only with its column list in the Inventory Item mapping, and no uniqueness constraint is provided for either sku column. So from the available context, this cannot be confirmed.

**Sources retrieved (12):** `Inventory Item→PRODUCTS`, `parent_chunk_data_dictionary.txt_2`, `parent_chunk_data_dictionary.txt_3`, `Unknown→ORDER_ITEMS`, `parent_chunk_data_dictionary.txt_1`, `Multiple FK references (order_id, customer_id) - unclear relationship→CUSTOMERS`, `Sales Order→ORDERS`, `Inventory Item`

**Context previews (first 3):**

1. _Business concept 'Inventory Item' — The table includes core product identifiers and descriptors, but the explicit stock_quantity, quantity_in_stock, and reorder_level fields make it operational invent…_

2. _Foreign Keys: - customer_id → CUSTOMERS(customer_id or CustomerID?) - [missing other FK definitions] ========================================== ORDER_ITEMS (or ORDER_DETAILS?) ========================…_

3. _========================================== PAYMENTS ==========================================  Primary Key: payment_id (unverified) | Column Name | Data Type | Constraints | Description | |----------…_

---

### ✅ ec_017 — What is the relationship between customers and orders?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0859 | **Gate:** `proceed_with_warning`

**Expected answer:**
> The glossary states 'A customer can place multiple orders. Or is it accounts that place orders?' indicating uncertainty about the relationship. The ORDERS table has both customer_id and CustomerID columns with ambiguous FK references, and the data dictionary notes they reference 'customer (which tab…

**System answer:**
> The retrieved context shows a schema-level link between orders and customers through a customer identifier, but the documentation is ambiguous.

ORDERS, which is mapped to the business concept “Sales Order,” includes customer linkage fields: customer_id and CustomerID. Separately, the documented foreign key says customer_id → CUSTOMERS(customer_id or CustomerID?), which indicates that an order is …

**Sources retrieved (12):** `Multiple FK references (order_id, customer_id) - unclear relationship→CUSTOMERS`, `parent_chunk_data_dictionary.txt_3`, `Sales Order→ORDERS`, `parent_chunk_data_dictionary.txt_2`, `Multiple FK references (order_id, customer_id) - unclear relationship`, `parent_chunk_data_dictionary.txt_1`, `Unknown→ORDER_ITEMS`, `Inventory Item→PRODUCTS`

**Context previews (first 3):**

1. _Business concept 'Multiple FK references (order_id, customer_id) - unclear relationship' is implemented by physical table CUSTOMERS (columns: customer_id, CustomerID, firstName, first_name, lastName, …_

2. _========================================== PAYMENTS ==========================================  Primary Key: payment_id (unverified) | Column Name | Data Type | Constraints | Description | |----------…_

3. _Business concept 'Sales Order' — The table centers on order identity, customer linkage, order date, totals, shipping, tax, and status fields, which aligns with an order record rather than payment or s…_

---

### ✅ ec_018 — Which price column represents what the customer actually pays?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0143 | **Gate:** `proceed_with_warning`

**Expected answer:**
> Multiple price columns exist across tables: ORDERS has orderAmount and total_amount; ORDER_ITEMS has unit_price and UnitPrice; PRODUCTS has unit_price, current_price, and cost_price. The data dictionary does not explain which represents the final customer price, whether discounts are applied, or how…

**System answer:**
> The retrieved context does not explicitly identify a single column as “what the customer actually pays.”

What the context does show is:

ORDERS contains order-level amount fields: orderAmount, total_amount, shippingAmount, tax_amount, and TaxAmount. The Sales Order mapping says this table covers “order amounts and order lifecycle data,” but it does not define which of orderAmount or total_amount …

**Sources retrieved (12):** `Sales Order→ORDERS`, `parent_chunk_data_dictionary.txt_2`, `parent_chunk_data_dictionary.txt_3`, `Unknown→ORDER_ITEMS`, `parent_chunk_data_dictionary.txt_1`, `Multiple FK references (order_id, customer_id) - unclear relationship→CUSTOMERS`, `Inventory Item→PRODUCTS`, `Multiple FK references (order_id, customer_id) - unclear relationship`

**Context previews (first 3):**

1. _Business concept 'Sales Order' — The table centers on order identity, customer linkage, order date, totals, shipping, tax, and status fields, which aligns with an order record rather than payment or s…_

2. _Foreign Keys: - customer_id → CUSTOMERS(customer_id or CustomerID?) - [missing other FK definitions] ========================================== ORDER_ITEMS (or ORDER_DETAILS?) ========================…_

3. _========================================== PAYMENTS ==========================================  Primary Key: payment_id (unverified) | Column Name | Data Type | Constraints | Description | |----------…_

---

### ✅ ec_019 — What's the difference between Shipment, Delivery, and Fulfillment?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0067 | **Gate:** `proceed_with_warning`

**Expected answer:**
> The glossary provides definitions but unclear boundaries: Shipment is 'The process of delivering goods to a customer'; Delivery is 'The completion of a Shipment when goods reach the customer'; Fulfillment is 'The process of preparing and delivering orders. Encompasses Shipment and Delivery.' The exa…

**System answer:**
> The retrieved context does not define Shipment, Delivery, or Fulfillment, so I cannot distinguish those terms from the knowledge graph.

What the context does define is related order terminology:
Order is defined in the business glossary as “a request to purchase products or services” and “can be in various states.”
Sales Order is represented by table ORDERS and includes order identity, customer l…

**Sources retrieved (12):** `Sales Order→ORDERS`, `parent_chunk_data_dictionary.txt_2`, `Unknown→ORDER_ITEMS`, `parent_chunk_data_dictionary.txt_3`, `Inventory Item→PRODUCTS`, `Sales Order`, `parent_chunk_business_glossary.txt_0`, `Unknown`

**Context previews (first 3):**

1. _Business concept 'Sales Order' — The table centers on order identity, customer linkage, order date, totals, shipping, tax, and status fields, which aligns with an order record rather than payment or s…_

2. _Foreign Keys: - customer_id → CUSTOMERS(customer_id or CustomerID?) - [missing other FK definitions] ========================================== ORDER_ITEMS (or ORDER_DETAILS?) ========================…_

3. _Business concept 'Unknown' — This table is a sales order line-item structure: order_item_id, order_id, product_id, quantity, unit_price, discount, and line_total describe individual order lines rather…_

---

### ✅ ec_020 — Are foreign key constraints enforced in the schema?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.1603 | **Gate:** `proceed_with_warning`

**Expected answer:**
> No foreign key constraints are enforced in the DDL. While the data dictionary documents FK relationships (e.g., customer_id → CUSTOMERS, order_id → ORDERS), the actual CREATE TABLE statements omit the REFERENCES clauses. The schema explicitly notes 'FK constraints defined in data dictionary but not …

**System answer:**
> The retrieved context shows that some columns are documented as foreign keys, but it does not confirm that foreign key constraints are actually enforced by the database.

Specifically, the schema metadata labels ORDER_ITEMS.order_id as an FK referencing ORDERS, ORDER_ITEMS.product_id as an FK referencing PRODUCTS (with uncertainty: “or INVENTORY?”), PAYMENTS.order_id as an FK referencing ORDERS, a…

**Sources retrieved (12):** `parent_chunk_data_dictionary.txt_2`, `parent_chunk_data_dictionary.txt_3`, `parent_chunk_data_dictionary.txt_1`, `parent_chunk_business_glossary.txt_0`, `Multiple FK references (order_id, customer_id) - unclear relationship→CUSTOMERS`, `Multiple FK references (order_id, customer_id) - unclear relationship`, `Unknown→ORDER_ITEMS`, `Inventory Item→PRODUCTS`

**Context previews (first 3):**

1. _Foreign Keys: - customer_id → CUSTOMERS(customer_id or CustomerID?) - [missing other FK definitions] ========================================== ORDER_ITEMS (or ORDER_DETAILS?) ========================…_

2. _========================================== PAYMENTS ==========================================  Primary Key: payment_id (unverified) | Column Name | Data Type | Constraints | Description | |----------…_

3. _DATA DICTIONARY - Enterprise Database Version: 2.1 (incomplete documentation) Last Updated: 2024-02-28 ========================================== CUSTOMERS ========================================== P…_

---

## Anomalies & Observations

No anomalies detected. All questions grounded with acceptable RAGAS scores.
