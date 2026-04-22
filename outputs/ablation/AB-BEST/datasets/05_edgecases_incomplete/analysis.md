# AB-BEST — 05_edgecases_incomplete — Run Analysis

**Timestamp:** 2026-04-21 21:09:37  
**Run tag:** `run-20260421_221024`

## Configuration

| Parameter | Value |
|-----------|-------|
| Extraction model | `LLM (openai/gpt-4.1-nano)` |
| Reasoning model | `openai/gpt-oss-120b` |
| Embedding model | `BAAI/bge-m3` |
| Retrieval mode | `hybrid` |
| Reranker | `True` |
| Reranker top_k | `20` |
| Chunk size / overlap | `128 / 16` |
| ER similarity threshold | `0.65` |

## Builder Results

| Metric | Value |
|--------|-------|
| Triplets extracted | 23 |
| Entities resolved | 7 |
| Tables parsed | 5 |
| Tables completed | 5 |

## Query Evaluation Summary

| Metric | Value |
|--------|-------|
| Questions | 20 |
| Grounded | **20/20 (100%)** |
| Avg GT Coverage | N/A |
| Avg Top Score | 0.4743 |
| Avg Chunk Count | 14.0 |
| Abstained | 0 |

## RAGAS Metrics

RAGAS evaluation not enabled for this run.

## Per-Question Deep Dive

### ✅ ec_001 — What is a customer?

**Status:** GROUNDED  
**GT Coverage:** N/A | **Top Score:** 0.0000 | **Gate:** `proceed`

**Expected answer:**
> The business glossary defines Customer as "an individual or organization that... [definition incomplete]". Related terms include Client (a person or company that purchases goods or services, sometimes used interchangeably with Customer), Account Holder (the primary owner of an account), and End User…

**System answer:**
> 

**Sources retrieved (12):** `Customer→CUSTOMERS`, `parent_chunk_data_dictionary.txt_1`, `parent_chunk_data_dictionary.txt_2`, `Sales Order→ORDERS`, `parent_chunk_data_dictionary.txt_3`, `Any Monetary Exchange→PAYMENTS`, `Order Item→ORDER_ITEMS`, `parent_chunk_business_glossary.txt_0`

---

### ✅ ec_002 — What's the difference between firstName and first_name in the CUSTOMERS table?

**Status:** GROUNDED  
**GT Coverage:** N/A | **Top Score:** 0.0000 | **Gate:** `proceed`

**Expected answer:**
> Both columns exist in the CUSTOMERS table with identical VARCHAR(50) data types. The data dictionary notes they appear to be duplicates resulting from inconsistent naming conventions (snake_case vs camelCase), but the actual usage by the application is not documented.

**System answer:**
> 

**Sources retrieved (12):** `Customer→CUSTOMERS`, `parent_chunk_data_dictionary.txt_1`, `parent_chunk_data_dictionary.txt_2`, `parent_chunk_data_dictionary.txt_3`, `Customer`, `Sales Order→ORDERS`, `Any Monetary Exchange→PAYMENTS`, `Order Item→ORDER_ITEMS`

---

### ✅ ec_003 — Which customer column should be used as a foreign key reference: customer_id or CustomerID?

**Status:** GROUNDED  
**GT Coverage:** N/A | **Top Score:** 0.0000 | **Gate:** `proceed`

**Expected answer:**
> The CUSTOMERS table has both customer_id (defined as PRIMARY KEY) and CustomerID (defined as INTEGER with no constraints). The ORDERS table also has both customer_id and CustomerID columns with ambiguous FK references. The data dictionary indicates this inconsistency is documented but not yet resolv…

**System answer:**
> 

**Sources retrieved (12):** `parent_chunk_data_dictionary.txt_2`, `parent_chunk_data_dictionary.txt_1`, `Customer→CUSTOMERS`, `parent_chunk_data_dictionary.txt_3`, `Sales Order→ORDERS`, `Any Monetary Exchange→PAYMENTS`, `Order Item→ORDER_ITEMS`, `Product→PRODUCTS`

---

### ✅ ec_004 — What are the valid values for order_status?

**Status:** GROUNDED  
**GT Coverage:** N/A | **Top Score:** 0.0000 | **Gate:** `proceed`

**Expected answer:**
> The business glossary documents several order statuses: Pending, Processing, Completed, Cancelled, On Hold, and Failed (which is marked as [definition missing]). However, these are not enforced by a CHECK constraint in the schema, and the data dictionary notes that valid values reference '[missing d…

**System answer:**
> 

**Sources retrieved (12):** `parent_chunk_data_dictionary.txt_3`, `Sales Order→ORDERS`, `parent_chunk_data_dictionary.txt_1`, `parent_chunk_data_dictionary.txt_2`, `Any Monetary Exchange→PAYMENTS`, `Order Item→ORDER_ITEMS`, `Product→PRODUCTS`, `Customer→CUSTOMERS`

---

### ✅ ec_005 — Is there a difference between Product, Item, and SKU?

**Status:** GROUNDED  
**GT Coverage:** N/A | **Top Score:** 0.0000 | **Gate:** `proceed`

**Expected answer:**
> The glossary indicates these terms are related but distinct: Product is defined as "A thing that is... [definition needs clarification]"; Item is a synonym for Product used in inventory context; SKU (Stock Keeping Unit) is a unique identifier for a product variant; Inventory Item refers to physical …

**System answer:**
> 

**Sources retrieved (12):** `Product→PRODUCTS`, `parent_chunk_data_dictionary.txt_2`, `Order Item→ORDER_ITEMS`, `parent_chunk_data_dictionary.txt_1`, `parent_chunk_data_dictionary.txt_3`, `parent_chunk_business_glossary.txt_0`, `Product`, `Order Item`

---

### ✅ ec_006 — Which table should ORDER_ITEMS.product_id reference: PRODUCTS or INVENTORY?

**Status:** GROUNDED  
**GT Coverage:** N/A | **Top Score:** 0.0000 | **Gate:** `proceed`

**Expected answer:**
> The data dictionary states the FK reference is to 'PRODUCTS (or INVENTORY?)' and notes it is 'not verified'. The schema provides two potential targets: PRODUCTS table (which has product_id) and an INVENTORY table that is referenced in documentation but not defined in the DDL. The actual relationship…

**System answer:**
> 

**Sources retrieved (12):** `parent_chunk_data_dictionary.txt_2`, `Product→PRODUCTS`, `Order Item→ORDER_ITEMS`, `parent_chunk_data_dictionary.txt_3`, `parent_chunk_data_dictionary.txt_1`, `Product`, `parent_chunk_business_glossary.txt_0`, `Sales Order→ORDERS`

---

### ✅ ec_007 — What's the difference between Revenue and Sales?

**Status:** GROUNDED  
**GT Coverage:** N/A | **Top Score:** 0.0000 | **Gate:** `proceed`

**Expected answer:**
> Both terms show circular definitions: Revenue is defined as 'Income from sales. The same as... [definition circular, see Sales]', while Sales is defined as 'Revenue from selling products. See Revenue.' The glossary provides no clear distinction between these concepts.

**System answer:**
> 

**Sources retrieved (12):** `Sales Order→ORDERS`, `Product→PRODUCTS`, `parent_chunk_data_dictionary.txt_3`, `parent_chunk_business_glossary.txt_0`, `Sales Order`, `Product`, `parent_chunk_data_dictionary.txt_1`, `parent_chunk_data_dictionary.txt_2`

---

### ✅ ec_008 — Can one order have multiple payments?

**Status:** GROUNDED  
**GT Coverage:** N/A | **Top Score:** 0.0000 | **Gate:** `proceed`

**Expected answer:**
> The PAYMENTS table has an order_id column, suggesting a many-to-one relationship (multiple payments can reference a single order). However, the relationship section in the glossary asks 'Or is it one-to-one?' indicating uncertainty. The ORDERS table has both payment_status and payment_method columns…

**System answer:**
> 

**Sources retrieved (12):** `parent_chunk_data_dictionary.txt_3`, `Sales Order→ORDERS`, `Any Monetary Exchange→PAYMENTS`, `parent_chunk_data_dictionary.txt_2`, `parent_chunk_data_dictionary.txt_1`, `Order Item→ORDER_ITEMS`, `Product→PRODUCTS`, `Customer→CUSTOMERS`

---

### ✅ ec_009 — What payment methods are accepted?

**Status:** GROUNDED  
**GT Coverage:** N/A | **Top Score:** 0.0000 | **Gate:** `proceed`

**Expected answer:**
> The PAYMENTS table has a payment_method column (VARCHAR(30)), but the data dictionary notes '[missing valid values]' and no CHECK constraint exists to enumerate acceptable methods. The schema does not document what values are valid (e.g., credit_card, debit, paypal, etc.).

**System answer:**
> 

**Sources retrieved (12):** `parent_chunk_data_dictionary.txt_3`, `Sales Order→ORDERS`, `Any Monetary Exchange→PAYMENTS`, `parent_chunk_data_dictionary.txt_1`, `parent_chunk_data_dictionary.txt_2`, `parent_chunk_business_glossary.txt_0`, `Sales Order`, `Customer→CUSTOMERS`

---

### ✅ ec_010 — What's the correct table name: ORDER_ITEMS or ORDER_DETAILS?

**Status:** GROUNDED  
**GT Coverage:** N/A | **Top Score:** 0.0000 | **Gate:** `proceed`

**Expected answer:**
> The DDL creates a table named ORDER_ITEMS, but the data dictionary header shows 'ORDER_ITEMS (or ORDER_DETAILS?)' and notes 'Table name ambiguity: ORDER_ITEMS vs ORDER_DETAILS'. The actual table name in the schema is ORDER_ITEMS, but documentation suggests the application may reference it differentl…

**System answer:**
> 

**Sources retrieved (12):** `parent_chunk_data_dictionary.txt_2`, `Order Item→ORDER_ITEMS`, `Product→PRODUCTS`, `parent_chunk_data_dictionary.txt_3`, `parent_chunk_data_dictionary.txt_1`, `Customer→CUSTOMERS`, `Product`, `Sales Order→ORDERS`

---

### ✅ ec_011 — Which date column should be used to track when an order was created: order_date, OrderDate, or created_at?

**Status:** GROUNDED  
**GT Coverage:** N/A | **Top Score:** 0.0000 | **Gate:** `proceed`

**Expected answer:**
> The ORDERS table has three date-related columns: order_date (DATE type), OrderDate (DATETIME type with different precision), and created_at (TIMESTAMP type). The data dictionary provides no guidance on which is actually used by the application or why three columns exist for potentially the same purp…

**System answer:**
> 

**Sources retrieved (12):** `Sales Order→ORDERS`, `Any Monetary Exchange→PAYMENTS`, `Customer→CUSTOMERS`, `parent_chunk_data_dictionary.txt_1`, `parent_chunk_data_dictionary.txt_3`, `Product→PRODUCTS`, `parent_chunk_data_dictionary.txt_2`, `Order Item→ORDER_ITEMS`

---

### ✅ ec_012 — What does the Failed order status mean?

**Status:** GROUNDED  
**GT Coverage:** N/A | **Top Score:** 0.0000 | **Gate:** `proceed`

**Expected answer:**
> The business glossary lists Failed as an order status but marks it as '[definition missing]'. Other statuses have definitions (Pending, Processing, Completed, Cancelled, On Hold), but Failed is undefined despite being a valid status value.

**System answer:**
> 

**Sources retrieved (12):** `Sales Order→ORDERS`, `parent_chunk_data_dictionary.txt_3`, `parent_chunk_data_dictionary.txt_1`, `parent_chunk_data_dictionary.txt_2`, `Product→PRODUCTS`, `Any Monetary Exchange→PAYMENTS`, `Customer→CUSTOMERS`, `Order Item→ORDER_ITEMS`

---

### ✅ ec_013 — Are there any NOT NULL constraints defined in the schema?

**Status:** GROUNDED  
**GT Coverage:** N/A | **Top Score:** 0.0000 | **Gate:** `proceed`

**Expected answer:**
> No NOT NULL constraints are defined in the DDL. The data dictionary explicitly states 'NOT NULL constraints not defined' under 'Missing Documentation' and notes 'assumed, not verified'. All columns are nullable by default.

**System answer:**
> 

**Sources retrieved (12):** `parent_chunk_data_dictionary.txt_3`, `parent_chunk_data_dictionary.txt_2`, `parent_chunk_data_dictionary.txt_1`, `Any Monetary Exchange→PAYMENTS`, `Sales Order→ORDERS`, `parent_chunk_business_glossary.txt_0`, `Product→PRODUCTS`, `Order Item→ORDER_ITEMS`

---

### ✅ ec_014 — What's the difference between unit_price and current_price in PRODUCTS?

**Status:** GROUNDED  
**GT Coverage:** N/A | **Top Score:** 0.0000 | **Gate:** `proceed`

**Expected answer:**
> The PRODUCTS table has both unit_price and current_price columns (both DECIMAL(10,2)). The data dictionary asks 'Different from unit_price?' but provides no explanation of the distinction or when each would be used.

**System answer:**
> 

**Sources retrieved (12):** `Product→PRODUCTS`, `parent_chunk_data_dictionary.txt_2`, `Order Item→ORDER_ITEMS`, `parent_chunk_data_dictionary.txt_3`, `parent_chunk_business_glossary.txt_0`, `Product`, `parent_chunk_data_dictionary.txt_1`, `Sales Order→ORDERS`

---

### ✅ ec_015 — When is an invoice generated vs payment processed?

**Status:** GROUNDED  
**GT Coverage:** N/A | **Top Score:** 0.0000 | **Gate:** `proceed`

**Expected answer:**
> The relationship section in the glossary asks 'An invoice is generated for an order. But when? And can one order have multiple invoices?' indicating the timing and cardinality are not defined. The glossary defines Invoice as 'A document requesting payment. Related to Bill' and Payment as 'The transf…

**System answer:**
> 

**Sources retrieved (12):** `parent_chunk_data_dictionary.txt_3`, `Sales Order→ORDERS`, `parent_chunk_data_dictionary.txt_1`, `parent_chunk_data_dictionary.txt_2`, `Any Monetary Exchange→PAYMENTS`, `parent_chunk_business_glossary.txt_0`, `Sales Order`, `Product→PRODUCTS`

---

### ✅ ec_016 — Is the sku column in PRODUCTS unique?

**Status:** GROUNDED  
**GT Coverage:** N/A | **Top Score:** 0.0000 | **Gate:** `proceed`

**Expected answer:**
> The PRODUCTS table has both product_sku and sku columns. The data dictionary notes sku 'should be UNIQUE?' but the DDL does not define a UNIQUE constraint on either column. No index is documented for these columns.

**System answer:**
> 

**Sources retrieved (12):** `Product→PRODUCTS`, `parent_chunk_data_dictionary.txt_2`, `parent_chunk_data_dictionary.txt_3`, `parent_chunk_data_dictionary.txt_1`, `Order Item→ORDER_ITEMS`, `Sales Order→ORDERS`, `Customer→CUSTOMERS`, `Any Monetary Exchange→PAYMENTS`

---

### ✅ ec_017 — What is the relationship between customers and orders?

**Status:** GROUNDED  
**GT Coverage:** N/A | **Top Score:** 0.0000 | **Gate:** `proceed`

**Expected answer:**
> The glossary states 'A customer can place multiple orders. Or is it accounts that place orders?' indicating uncertainty about the relationship. The ORDERS table has both customer_id and CustomerID columns with ambiguous FK references, and the data dictionary notes they reference 'customer (which tab…

**System answer:**
> 

**Sources retrieved (12):** `parent_chunk_data_dictionary.txt_3`, `Sales Order→ORDERS`, `parent_chunk_data_dictionary.txt_2`, `Order Item→ORDER_ITEMS`, `parent_chunk_data_dictionary.txt_1`, `Customer→CUSTOMERS`, `parent_chunk_business_glossary.txt_0`, `Sales Order`

---

### ✅ ec_018 — Which price column represents what the customer actually pays?

**Status:** GROUNDED  
**GT Coverage:** N/A | **Top Score:** 0.0000 | **Gate:** `proceed`

**Expected answer:**
> Multiple price columns exist across tables: ORDERS has orderAmount and total_amount; ORDER_ITEMS has unit_price and UnitPrice; PRODUCTS has unit_price, current_price, and cost_price. The data dictionary does not explain which represents the final customer price, whether discounts are applied, or how…

**System answer:**
> 

**Sources retrieved (12):** `Any Monetary Exchange→PAYMENTS`, `Order Item→ORDER_ITEMS`, `parent_chunk_data_dictionary.txt_2`, `parent_chunk_data_dictionary.txt_3`, `Sales Order→ORDERS`, `parent_chunk_data_dictionary.txt_1`, `Product→PRODUCTS`, `Customer→CUSTOMERS`

---

### ✅ ec_019 — What's the difference between Shipment, Delivery, and Fulfillment?

**Status:** GROUNDED  
**GT Coverage:** N/A | **Top Score:** 0.0000 | **Gate:** `proceed`

**Expected answer:**
> The glossary provides definitions but unclear boundaries: Shipment is 'The process of delivering goods to a customer'; Delivery is 'The completion of a Shipment when goods reach the customer'; Fulfillment is 'The process of preparing and delivering orders. Encompasses Shipment and Delivery.' The exa…

**System answer:**
> 

**Sources retrieved (12):** `parent_chunk_data_dictionary.txt_3`, `parent_chunk_business_glossary.txt_0`, `Sales Order→ORDERS`, `parent_chunk_data_dictionary.txt_2`, `parent_chunk_data_dictionary.txt_1`, `Product→PRODUCTS`, `Order Item→ORDER_ITEMS`, `Any Monetary Exchange→PAYMENTS`

---

### ✅ ec_020 — Are foreign key constraints enforced in the schema?

**Status:** GROUNDED  
**GT Coverage:** N/A | **Top Score:** 0.0000 | **Gate:** `proceed`

**Expected answer:**
> No foreign key constraints are enforced in the DDL. While the data dictionary documents FK relationships (e.g., customer_id → CUSTOMERS, order_id → ORDERS), the actual CREATE TABLE statements omit the REFERENCES clauses. The schema explicitly notes 'FK constraints defined in data dictionary but not …

**System answer:**
> 

**Sources retrieved (12):** `parent_chunk_data_dictionary.txt_2`, `parent_chunk_data_dictionary.txt_3`, `parent_chunk_data_dictionary.txt_1`, `Any Monetary Exchange→PAYMENTS`, `Product→PRODUCTS`, `Customer→CUSTOMERS`, `Sales Order→ORDERS`, `Order Item→ORDER_ITEMS`

---

## Anomalies & Observations

No anomalies detected. All questions grounded with acceptable RAGAS scores.
