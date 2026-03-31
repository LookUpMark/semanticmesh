# _REBUILD — 04_complex_manufacturing — Run Analysis

**Timestamp:** 2026-03-30 23:54:42  
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
| Triplets extracted | 380 |
| Entities resolved | 123 |
| Tables parsed | 13 |
| Tables completed | 13 |

## Query Evaluation Summary

| Metric | Value |
|--------|-------|
| Questions | 1 |
| Grounded | **1/1 (100%)** |
| Avg GT Coverage | 100% |
| Avg Top Score | 0.8872 |
| Avg Chunk Count | 12.0 |
| Abstained | 0 |

## RAGAS Metrics

RAGAS evaluation not enabled for this run.

## Per-Question Deep Dive

### ✅ QA-001 — What information is stored about products in the manufacturing system?

**Status:** GROUNDED  
**GT Coverage:** 100% | **Top Score:** 0.8872 | **Gate:** `proceed`

**Expected answer:**
> Products are tracked with a unique identifier (product_id), descriptive name (product_name), classification as finished good, assembly, or component (product_type), optional parent product reference for hierarchical structures (parent_product_id), standard unit cost (base_cost), typical procurement …

**System answer:**
> The manufacturing system stores product master data in the `product` table. For each product, it stores a unique `product_id`, `product_name`, `product_type`, `parent_product_id`, `base_cost`, `lead_time_days`, and `is_active`.

From the retrieved schema and glossary, this means the system records:

A Product represents any manufactured item, including finished goods, assemblies, and components. T…

**Sources retrieved (12):** `parent_chunk_data_dictionary.md_3`, `Manufacturing Routing→ROUTE`, `parent_chunk_data_dictionary.md_6`, `parent_chunk_data_dictionary.md_5`, `parent_chunk_data_dictionary.md_7`, `complex products→PRODUCT`, `parent_chunk_business_glossary.md_0`, `Manufacturing Routing`

**Context previews (first 3):**

1. _# Manufacturing Data Dictionary  This data dictionary documents the database schema for the manufacturing supply chain system. It includes all tables, columns, data types, constraints, and relationshi…_

2. _Business concept 'Manufacturing Routing' — The table is keyed by route_id and product_id and stores the ordered steps for a product, including route_name, sequence_number, operation_name, work_center,…_

3. _## work_order  Represents production jobs for manufacturing products with hierarchical work order support.  | Column | Data Type | Constraints | Description | |--------|-----------|-------------|-----…_

---

## Anomalies & Observations

No anomalies detected. All questions grounded with acceptable RAGAS scores.
