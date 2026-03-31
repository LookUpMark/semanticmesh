# _REBUILD — 01_basics_ecommerce — Run Analysis

**Timestamp:** 2026-03-30 22:48:09  
**Run tag:** `v5-rebuild`

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
| Triplets extracted | 231 |
| Entities resolved | 76 |
| Tables parsed | 7 |
| Tables completed | 7 |

## Query Evaluation Summary

| Metric | Value |
|--------|-------|
| Questions | 1 |
| Grounded | **1/1 (100%)** |
| Avg GT Coverage | 100% |
| Avg Top Score | 0.2800 |
| Avg Chunk Count | 12.0 |
| Abstained | 0 |

## RAGAS Metrics

RAGAS evaluation not enabled for this run.

## Per-Question Deep Dive

### ✅ Q001 — What information is stored for each customer?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.2800 | **Gate:** `proceed`

**Expected answer:**
> Each customer has a unique ID, full name, email address, geographic region code, creation date, and active status. The email must be unique across all customers.

**System answer:**
> For each customer, the physical customer master record is stored in CUSTOMER_MASTER. It contains CUST_ID (unique customer identifier), FULL_NAME, EMAIL (unique email address used for login), REGION_CODE (geographic region for tax), CREATED_AT (account creation timestamp), and IS_ACTIVE (whether the customer can place orders).

From the business glossary, the customer concept also includes a valid …

**Sources retrieved (12):** `Sales Order Header→SALES_ORDER_HDR`, `Customer Master→CUSTOMER_MASTER`, `the customer, items, payment status, and delivery information→PAYMENT`, `parent_chunk_data_dictionary.txt_3`, `parent_chunk_business_glossary.txt_0`, `Shipment`, `parent_chunk_business_glossary.txt_1`, `Shipment→SHIPMENT`

**Context previews (first 3):**

1. _Business concept 'Sales Order Header' — The table name and columns match a sales order header record: it has order ID, customer reference, order date, total amount, status, and fulfillment/payment tim…_

2. _Business concept 'Customer Master' — The table is a customer master record: it contains a unique customer ID, full name, unique email, region, creation timestamp, and active flag. This aligns most dir…_

3. _Business concept 'the customer, items, payment status, and delivery information' is implemented by physical table PAYMENT (columns: PAYMENT_ID, ORDER_ID, PAYMENT_METHOD, AMOUNT, STATUS_CODE, CONFIRMED…_

---

## Anomalies & Observations

No anomalies detected. All questions grounded with acceptable RAGAS scores.
