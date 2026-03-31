# _REBUILD — 05_edgecases_incomplete — Run Analysis

**Timestamp:** 2026-03-31 01:48:24  
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
| Triplets extracted | 209 |
| Entities resolved | 81 |
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
> In the BUSINESS GLOSSARY under CUSTOMER MANAGEMENT, Customer is defined only partially as “An individual or organization that...” because the definition is incomplete in the retrieved context.

Related glossary terms help clarify the intended meaning: Client is “a person or company that purchases goods or services” and may be used interchangeably with Customer in some contexts; Account Holder is t…

**Sources retrieved (12):** `CUSTOMERS→CUSTOMERS`, `parent_chunk_data_dictionary.txt_1`, `Sales Order→ORDERS`, `parent_chunk_data_dictionary.txt_2`, `parent_chunk_data_dictionary.txt_3`, `Payment gateway response→PAYMENTS`, `parent_chunk_business_glossary.txt_0`, `Sales Order`

**Context previews (first 3):**

1. _Business concept 'CUSTOMERS' is implemented by physical table CUSTOMERS (columns: customer_id, CustomerID, firstName, first_name, lastName, last_name, email, emailAddress, phone, phoneNumber, created_…_

2. _DATA DICTIONARY - Enterprise Database Version: 2.1 (incomplete documentation) Last Updated: 2024-02-28 ========================================== CUSTOMERS ========================================== P…_

3. _Business concept 'Sales Order' — The table contains canonical order-header attributes such as order_id, customer_id, order_date, order_status, and financial totals (amount, shipping, tax), which align…_

---

## Anomalies & Observations

No anomalies detected. All questions grounded with acceptable RAGAS scores.
