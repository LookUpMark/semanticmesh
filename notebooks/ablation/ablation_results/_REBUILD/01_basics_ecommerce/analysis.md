# _REBUILD — 01_basics_ecommerce — Run Analysis

**Timestamp:** 2026-03-31 16:30:08  
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
| Triplets extracted | 252 |
| Entities resolved | 84 |
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
> The retrieved context shows two different customer implementations, so the answer depends on which schema you mean.

In the simplified e-commerce schema, each customer is stored in CUSTOMER_MASTER with these fields: CUST_ID, FULL_NAME, EMAIL, REGION_CODE, CREATED_AT, and IS_ACTIVE. The related business glossary also describes customer information at the concept level as including a unique customer…

**Sources retrieved (12):** `the customer, items, payment status, and delivery information→CUSTOMER_MASTER`, `An individual or corporate entity that maintains a banking relationship with the institution, having completed Know Your Customer (KYC) verification→CUSTOMERS`, `Sales Order Header→SALES_ORDER_HDR`, `the customer, items, payment status, and delivery information→PAYMENT`, `CUSTOMER_ACCOUNT→CUSTOMERS`, `parent_chunk_data_dictionary.txt_3`, `parent_chunk_business_glossary.txt_0`, `LOANS→CUSTOMERS`

**Context previews (first 3):**

1. _Business concept 'the customer, items, payment status, and delivery information' is implemented by physical table CUSTOMER_MASTER (columns: CUST_ID, FULL_NAME, EMAIL, REGION_CODE, CREATED_AT, IS_ACTIV…_

2. _Business concept 'An individual or corporate entity that maintains a banking relationship with the institution, having completed Know Your Customer (KYC) verification' is implemented by physical table…_

3. _Business concept 'Sales Order Header' — The table name and structure strongly indicate a header-level sales order record: it has a unique order ID, customer reference, order date, total amount, and li…_

---

## Anomalies & Observations

No anomalies detected. All questions grounded with acceptable RAGAS scores.
