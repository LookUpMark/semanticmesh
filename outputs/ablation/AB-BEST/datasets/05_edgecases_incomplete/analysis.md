# AB-BEST — 05_edgecases_incomplete — Run Analysis

**Timestamp:** 2026-05-06 20:09:06  
**Run tag:** `run-20260506_210258`

## Configuration

| Parameter | Value |
|-----------|-------|
| Extraction model | `LLM (gpt-5-nano-2025-08-07)` |
| Reasoning model | `gpt-5.4-nano-2026-03-17` |
| Embedding model | `BAAI/bge-m3` |
| Retrieval mode | `hybrid` |
| Reranker | `True` |
| Reranker top_k | `5` |
| Chunk size / overlap | `256 / 32` |
| ER similarity threshold | `0.75` |

## Builder Results

| Metric | Value |
|--------|-------|
| Triplets extracted | 75 |
| Entities resolved | 70 |
| Tables parsed | 5 |
| Tables completed | 5 |

## Query Evaluation Summary

| Metric | Value |
|--------|-------|
| Questions | 20 |
| Grounded | **20/20 (100%)** |
| Avg GT Coverage | 82% |
| Avg Top Score | 0.7978 |
| Avg Chunk Count | 22.6 |
| Abstained | 0 |

## RAGAS Metrics

RAGAS evaluation not enabled for this run.

## Per-Question Deep Dive

### ✅ ec_001 — What is a customer?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0000 | **Gate:** `proceed`

**Expected answer:**
> The business glossary defines Customer as "an individual or organization that... [definition incomplete]". Related terms include Client (a person or company that purchases goods or services, sometimes used interchangeably with Customer), Account Holder (the primary owner of an account), and End User…

**System answer:**
> 

**Sources retrieved (12):** `parent_chunk_data_dictionary.txt_1`, `Customer`, `CUSTOMERS.FIRST_NAME`, `CUSTOMERS.FIRSTNAME`, `CUSTOMERS.LASTNAME`, `parent_chunk_business_glossary.txt_0`, `CUSTOMERS`, `CUSTOMERS.CREATEDDATE`

---

### ✅ ec_002 — What's the difference between firstName and first_name in the CUSTOMERS table?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0000 | **Gate:** `proceed`

**Expected answer:**
> Both columns exist in the CUSTOMERS table with identical VARCHAR(50) data types. The data dictionary notes they appear to be duplicates resulting from inconsistent naming conventions (snake_case vs camelCase), but the actual usage by the application is not documented.

**System answer:**
> 

**Sources retrieved (12):** `parent_chunk_data_dictionary.txt_1`, `CUSTOMERS.FIRST_NAME`, `CUSTOMERS.FIRSTNAME`, `CUSTOMERS.LAST_NAME`, `CUSTOMERS.LASTNAME`, `CUSTOMERS`, `CUSTOMERS.CREATEDDATE`, `CUSTOMERS.STATUS`

---

### ✅ ec_003 — Which customer column should be used as a foreign key reference: customer_id or CustomerID?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0000 | **Gate:** `proceed`

**Expected answer:**
> The CUSTOMERS table has both customer_id (defined as PRIMARY KEY) and CustomerID (defined as INTEGER with no constraints). The ORDERS table also has both customer_id and CustomerID columns with ambiguous FK references. The data dictionary indicates this inconsistency is documented but not yet resolv…

**System answer:**
> 

**Sources retrieved (12):** `parent_chunk_data_dictionary.txt_2`, `parent_chunk_data_dictionary.txt_1`, `ORDERS.CUSTOMER_ID`, `CUSTOMERS.CUSTOMER_ID`, `PAYMENTS.CUSTOMER_ID`, `CUSTOMERS.CUSTOMERID`, `ORDERS.CUSTOMERID`, `CUSTOMERS`

---

### ✅ ec_004 — What are the valid values for order_status?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0000 | **Gate:** `proceed`

**Expected answer:**
> The business glossary documents several order statuses: Pending, Processing, Completed, Cancelled, On Hold, and Failed (which is marked as [definition missing]). However, these are not enforced by a CHECK constraint in the schema, and the data dictionary notes that valid values reference '[missing d…

**System answer:**
> 

**Sources retrieved (12):** `parent_chunk_data_dictionary.txt_3`, `ORDERS.ORDER_STATUS`, `ORDERS.PAYMENT_STATUS`, `ORDERS.ORDER_ID`, `ORDERS.ORDERID`, `ORDERS`, `Sales Order`, `ORDERS.PAYMENT_METHOD`

---

### ✅ ec_005 — Is there a difference between Product, Item, and SKU?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0000 | **Gate:** `proceed`

**Expected answer:**
> The glossary indicates these terms are related but distinct: Product is defined as "A thing that is... [definition needs clarification]"; Item is a synonym for Product used in inventory context; SKU (Stock Keeping Unit) is a unique identifier for a product variant; Inventory Item refers to physical …

**System answer:**
> 

**Sources retrieved (12):** `parent_chunk_data_dictionary.txt_3`, `parent_chunk_business_glossary.txt_0`, `PRODUCTS.SKU`, `PRODUCTS.PRODUCT_SKU`, `PRODUCTS.PRODUCTID`, `PRODUCTS.STOCK_QUANTITY`, `PRODUCTS`, `Inventory Item`

---

### ✅ ec_006 — Which table should ORDER_ITEMS.product_id reference: PRODUCTS or INVENTORY?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0000 | **Gate:** `proceed`

**Expected answer:**
> The data dictionary states the FK reference is to 'PRODUCTS (or INVENTORY?)' and notes it is 'not verified'. The schema provides two potential targets: PRODUCTS table (which has product_id) and an INVENTORY table that is referenced in documentation but not defined in the DDL. The actual relationship…

**System answer:**
> 

**Sources retrieved (12):** `parent_chunk_data_dictionary.txt_2`, `ORDER_ITEMS.PRODUCT_ID`, `ORDER_ITEMS.PRODUCTID`, `ORDER_ITEMS.ORDER_ITEM_ID`, `PRODUCTS.PRODUCTID`, `ORDER_ITEMS`, `Order Items`, `ORDER_ITEMS.ORDER_ID`

---

### ✅ ec_007 — What's the difference between Revenue and Sales?

**Status:** GROUNDED  
**GT Coverage:** 0% | **Top Score:** 0.0000 | **Gate:** `proceed`

**Expected answer:**
> Both terms show circular definitions: Revenue is defined as 'Income from sales. The same as... [definition circular, see Sales]', while Sales is defined as 'Revenue from selling products. See Revenue.' The glossary provides no clear distinction between these concepts.

**System answer:**
> 

**Sources retrieved (12):** `parent_chunk_data_dictionary.txt_3`, `parent_chunk_business_glossary.txt_0`, `Sales Order`, `parent_chunk_data_dictionary.txt_1`, `parent_chunk_data_dictionary.txt_2`, `ORDERS.TAXAMOUNT`, `ORDERS`, `ORDERS.PAYMENT_METHOD`

---

### ✅ ec_008 — Can one order have multiple payments?

**Status:** GROUNDED  
**GT Coverage:** 50% | **Top Score:** 0.0000 | **Gate:** `proceed`

**Expected answer:**
> The PAYMENTS table has an order_id column, suggesting a many-to-one relationship (multiple payments can reference a single order). However, the relationship section in the glossary asks 'Or is it one-to-one?' indicating uncertainty. The ORDERS table has both payment_status and payment_method columns…

**System answer:**
> 

**Sources retrieved (12):** `parent_chunk_data_dictionary.txt_3`, `parent_chunk_business_glossary.txt_0`, `PAYMENTS.ORDER_ID`, `PAYMENTS.PAYMENT_AMOUNT`, `PAYMENTS.PAYMENT_METHOD`, `Payment`, `PAYMENTS`, `PAYMENTS.PAYMENT_STATUS`

---

### ✅ ec_009 — What payment methods are accepted?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0000 | **Gate:** `proceed`

**Expected answer:**
> The PAYMENTS table has a payment_method column (VARCHAR(30)), but the data dictionary notes '[missing valid values]' and no CHECK constraint exists to enumerate acceptable methods. The schema does not document what values are valid (e.g., credit_card, debit, paypal, etc.).

**System answer:**
> 

**Sources retrieved (12):** `PAYMENTS.PAYMENT_METHOD`, `PAYMENTS.PAYMENT_STATUS`, `parent_chunk_business_glossary.txt_0`, `parent_chunk_data_dictionary.txt_3`, `ORDERS.PAYMENT_METHOD`, `ORDERS.PAYMENT_STATUS`, `PAYMENTS`, `Payment`

---

### ✅ ec_010 — What's the correct table name: ORDER_ITEMS or ORDER_DETAILS?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0000 | **Gate:** `proceed`

**Expected answer:**
> The DDL creates a table named ORDER_ITEMS, but the data dictionary header shows 'ORDER_ITEMS (or ORDER_DETAILS?)' and notes 'Table name ambiguity: ORDER_ITEMS vs ORDER_DETAILS'. The actual table name in the schema is ORDER_ITEMS, but documentation suggests the application may reference it differentl…

**System answer:**
> 

**Sources retrieved (12):** `parent_chunk_data_dictionary.txt_2`, `Order Items`, `ORDER_ITEMS.PRODUCT_ID`, `ORDER_ITEMS.QUANTITY`, `ORDER_ITEMS.PRODUCTID`, `ORDER_ITEMS`, `ORDER_ITEMS.ORDER_ID`, `ORDER_ITEMS.UNITPRICE`

---

### ✅ ec_011 — Which date column should be used to track when an order was created: order_date, OrderDate, or created_at?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0000 | **Gate:** `proceed`

**Expected answer:**
> The ORDERS table has three date-related columns: order_date (DATE type), OrderDate (DATETIME type with different precision), and created_at (TIMESTAMP type). The data dictionary provides no guidance on which is actually used by the application or why three columns exist for potentially the same purp…

**System answer:**
> 

**Sources retrieved (12):** `parent_chunk_data_dictionary.txt_1`, `ORDERS.CREATED_AT`, `ORDERS.ORDER_DATE`, `ORDERS.ORDERDATE`, `PAYMENTS.CREATED_AT`, `ORDERS.UPDATED_AT`, `ORDERS`, `Sales Order`

---

### ✅ ec_012 — What does the Failed order status mean?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0000 | **Gate:** `proceed`

**Expected answer:**
> The business glossary lists Failed as an order status but marks it as '[definition missing]'. Other statuses have definitions (Pending, Processing, Completed, Cancelled, On Hold), but Failed is undefined despite being a valid status value.

**System answer:**
> 

**Sources retrieved (12):** `parent_chunk_business_glossary.txt_0`, `parent_chunk_data_dictionary.txt_3`, `parent_chunk_data_dictionary.txt_1`, `ORDERS.ORDER_STATUS`, `ORDERS.PAYMENT_STATUS`, `ORDERS`, `Sales Order`, `ORDERS.PAYMENT_METHOD`

---

### ✅ ec_013 — Are there any NOT NULL constraints defined in the schema?

**Status:** GROUNDED  
**GT Coverage:** N/A | **Top Score:** 0.0000 | **Gate:** `proceed`

**Expected answer:**
> No explicit NOT NULL constraints are written in the DDL. The schema comment states 'NOT NULL constraints not defined' and the data dictionary notes them as 'assumed, not verified'. However, PRIMARY KEY columns (e.g., ORDER_ID, CUSTOMER_ID) are implicitly NOT NULL per SQL standard, even though the ke…

**System answer:**
> 

**Sources retrieved (12):** `parent_chunk_data_dictionary.txt_3`, `parent_chunk_data_dictionary.txt_2`, `parent_chunk_data_dictionary.txt_1`, `ORDERS.TAXAMOUNT`, `parent_chunk_business_glossary.txt_0`, `ORDERS.NOTES`, `ORDERS`, `Sales Order`

---

### ✅ ec_014 — What's the difference between unit_price and current_price in PRODUCTS?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0000 | **Gate:** `proceed`

**Expected answer:**
> The PRODUCTS table has both unit_price and current_price columns (both DECIMAL(10,2)). The data dictionary asks 'Different from unit_price?' but provides no explanation of the distinction or when each would be used.

**System answer:**
> 

**Sources retrieved (12):** `parent_chunk_data_dictionary.txt_2`, `parent_chunk_data_dictionary.txt_3`, `PRODUCTS.CURRENT_PRICE`, `PRODUCTS.UNIT_PRICE`, `PRODUCTS.COST_PRICE`, `PRODUCTS.UPDATED_AT`, `PRODUCTS`, `PRODUCTS.PRODUCTID`

---

### ✅ ec_015 — When is an invoice generated vs payment processed?

**Status:** GROUNDED  
**GT Coverage:** 50% | **Top Score:** 0.0000 | **Gate:** `proceed`

**Expected answer:**
> The relationship section in the glossary asks 'An invoice is generated for an order. But when? And can one order have multiple invoices?' indicating the timing and cardinality are not defined. The glossary defines Invoice as 'A document requesting payment. Related to Bill' and Payment as 'The transf…

**System answer:**
> 

**Sources retrieved (12):** `parent_chunk_data_dictionary.txt_3`, `parent_chunk_business_glossary.txt_0`, `PAYMENTS.PAYMENT_DATE`, `PAYMENTS.PAYMENT_METHOD`, `PAYMENTS.CREATED_AT`, `PAYMENTS.PAYMENT_STATUS`, `PAYMENTS`, `Payment`

---

### ✅ ec_016 — Is the sku column in PRODUCTS unique?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0000 | **Gate:** `proceed`

**Expected answer:**
> The PRODUCTS table has both product_sku and sku columns. The data dictionary notes sku 'should be UNIQUE?' but the DDL does not define a UNIQUE constraint on either column. No index is documented for these columns.

**System answer:**
> 

**Sources retrieved (12):** `parent_chunk_data_dictionary.txt_2`, `PRODUCTS.SKU`, `PRODUCTS.PRODUCT_SKU`, `PRODUCTS.PRODUCT_CATEGORY`, `PRODUCTS.PRODUCTID`, `PRODUCTS.PRODUCT_ID`, `PRODUCTS`, `PRODUCTS.PRODUCT_NAME`

---

### ✅ ec_017 — What is the relationship between customers and orders?

**Status:** GROUNDED  
**GT Coverage:** 50% | **Top Score:** 0.0000 | **Gate:** `proceed`

**Expected answer:**
> The glossary states 'A customer can place multiple orders. Or is it accounts that place orders?' indicating uncertainty about the relationship. The ORDERS table has both customer_id and CustomerID columns with ambiguous FK references, and the data dictionary notes they reference 'customer (which tab…

**System answer:**
> 

**Sources retrieved (12):** `parent_chunk_data_dictionary.txt_3`, `parent_chunk_business_glossary.txt_0`, `ORDERS.CUSTOMER_ID`, `ORDERS.CUSTOMERID`, `ORDERS.NOTES`, `ORDERS`, `ORDERS.PAYMENT_METHOD`, `ORDERS.CREATED_AT`

---

### ✅ ec_018 — Which price column represents what the customer actually pays?

**Status:** GROUNDED  
**GT Coverage:** 67% | **Top Score:** 0.0000 | **Gate:** `proceed`

**Expected answer:**
> Multiple price columns exist across tables: ORDERS has orderAmount and total_amount; ORDER_ITEMS has unit_price and UnitPrice; PRODUCTS has unit_price, current_price, and cost_price. The data dictionary does not explain which represents the final customer price, whether discounts are applied, or how…

**System answer:**
> 

**Sources retrieved (12):** `parent_chunk_data_dictionary.txt_2`, `PAYMENTS.CUSTOMER_ID`, `PAYMENTS.PAYMENT_AMOUNT`, `PRODUCTS.COST_PRICE`, `parent_chunk_business_glossary.txt_0`, `PRODUCTS.UNIT_PRICE`, `PRODUCTS.CURRENT_PRICE`, `PRODUCTS`

---

### ✅ ec_019 — What's the difference between Shipment, Delivery, and Fulfillment?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.0000 | **Gate:** `proceed`

**Expected answer:**
> The glossary provides definitions but unclear boundaries: Shipment is 'The process of delivering goods to a customer'; Delivery is 'The completion of a Shipment when goods reach the customer'; Fulfillment is 'The process of preparing and delivering orders. Encompasses Shipment and Delivery.' The exa…

**System answer:**
> 

**Sources retrieved (12):** `parent_chunk_data_dictionary.txt_3`, `ORDERS.UPDATED_AT`, `ORDERS.NOTES`, `ORDERS.PAYMENT_METHOD`, `ORDERS.PAYMENT_STATUS`, `ORDERS.SHIPPINGAMOUNT`, `ORDERS`, `Sales Order`

---

### ✅ ec_020 — Are foreign key constraints enforced in the schema?

**Status:** GROUNDED  
**GT Coverage:** 50% | **Top Score:** 0.0000 | **Gate:** `proceed`

**Expected answer:**
> No foreign key constraints are enforced in the DDL. While the data dictionary documents FK relationships (e.g., customer_id → CUSTOMERS, order_id → ORDERS), the actual CREATE TABLE statements omit the REFERENCES clauses. The schema explicitly notes 'FK constraints defined in data dictionary but not …

**System answer:**
> 

**Sources retrieved (12):** `parent_chunk_data_dictionary.txt_2`, `parent_chunk_data_dictionary.txt_1`, `parent_chunk_data_dictionary.txt_3`, `ORDERS.NOTES`, `parent_chunk_business_glossary.txt_0`, `ORDERS`, `Sales Order`, `ORDERS.PAYMENT_METHOD`

---

## Anomalies & Observations

No anomalies detected. All questions grounded with acceptable RAGAS scores.
