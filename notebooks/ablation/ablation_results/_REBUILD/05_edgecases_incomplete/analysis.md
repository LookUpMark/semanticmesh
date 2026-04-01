# _REBUILD — 05_edgecases_incomplete — Run Analysis

**Timestamp:** 2026-03-31 16:55:49  
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
| Triplets extracted | 226 |
| Entities resolved | 82 |
| Tables parsed | 5 |
| Tables completed | 5 |

## Query Evaluation Summary

| Metric | Value |
|--------|-------|
| Questions | 1 |
| Grounded | **1/1 (100%)** |
| Avg GT Coverage | 100% |
| Avg Top Score | 0.8714 |
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
> In the business glossary, Customer is defined only partially as “An individual or organization that...” and the definition is marked incomplete. The same glossary says Client is “A person or company that purchases goods or services,” and notes that Client may be used interchangeably with Customer in some contexts.

The glossary also distinguishes related terms: Account Holder is the primary owner …

**Sources retrieved (12):** `parent_chunk_data_dictionary.txt_1`, `Multiple FK references (order_id, customer_id) - unclear relationship→CUSTOMERS`, `parent_chunk_data_dictionary.txt_2`, `parent_chunk_data_dictionary.txt_3`, `Table naming: ORDER_ITEMS vs ORDER_PRODUCTS vs ORDER_DETAILS→ORDERS`, `payment_method→PAYMENTS`, `Multiple FK references (order_id, customer_id) - unclear relationship`, `parent_chunk_business_glossary.txt_0`

**Context previews (first 3):**

1. _DATA DICTIONARY - Enterprise Database Version: 2.1 (incomplete documentation) Last Updated: 2024-02-28 ========================================== CUSTOMERS ========================================== P…_

2. _Business concept 'Multiple FK references (order_id, customer_id) - unclear relationship' is implemented by physical table CUSTOMERS (columns: customer_id, CustomerID, firstName, first_name, lastName, …_

3. _Foreign Keys: - customer_id → CUSTOMERS(customer_id or CustomerID?) - [missing other FK definitions] ========================================== ORDER_ITEMS (or ORDER_DETAILS?) ========================…_

---

## Anomalies & Observations

No anomalies detected. All questions grounded with acceptable RAGAS scores.
