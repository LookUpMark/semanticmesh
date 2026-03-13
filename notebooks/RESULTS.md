# Pipeline Run Results — Smoke Test

**Date:** 2026-03-13  
**Dataset:** Smoke fixtures (2 docs + 1 DDL with 2 tables)  
**Reasoning model:** `openai/gpt-oss-120b` → OpenRouter  
**Extraction model:** `openai/gpt-oss-20b` → OpenRouter  
**Total elapsed:** 217.2 s

---

## Cell-by-Cell Analysis

### ✅ Cell 2 — Configuration
Both models detected as `provider=openrouter`, `max_tokens=16384`. LM Studio not involved.

```
Reasoning  : 'openai/gpt-oss-120b'  →  provider=openrouter  max_tokens=16384
Extraction : 'openai/gpt-oss-20b'   →  provider=openrouter  max_tokens=16384
Documents  : 2 file(s)
DDL files  : 1 file(s)
Neo4j      : bolt://localhost:7687
```

### ✅ Cell 4 — Environment Check
Neo4j OK. LM Studio check correctly skipped (`extraction uses openrouter`).

### ✅ Cell 6 — Data Loading
2 documents → 2 chunks, 1 DDL → 2 tables. Clean.

---

### ✅ Cell 8 — Builder Graph

| Metric | Value |
|--------|-------|
| Elapsed | **217.2 s** |
| Triplets extracted | **42** (up from 27 with local model) |
| Entities resolved | **38** (up from 23) |
| ER clusters | 11 |
| Tables enriched | 2/2 |
| CUST_MASTER mapping | `Customer` — confidence 95% ✅ |
| SALES_ORD mapping | `Sales Order` — confidence 95% ✅ |
| Critic approvals | Both approved on first attempt ✅ |
| Cypher failures | **False** ✅ |
| Completed tables | CUST_MASTER, SALES_ORD |

**Notable events:**
- 3 ER judge warnings (malformed JSON on attempt 1) → all resolved by reflection on attempt 2 — expected behaviour.
- SALES_ORD Cypher: single-quote syntax error on attempt 1 (`'PENDING'`) → healed on attempt 2 by the Cypher Healing loop.

### ✅ Cell 10 — Graph Inspection
```
PhysicalTable   : 2 nodes
BusinessConcept : 2 nodes

Sales Order → SALES_ORD  (95%)
Customer    → CUST_MASTER (95%)
```

### ✅ Cell 12 — Graph Visualization
No Neo4j deprecation warnings (fixed: `id()` → `elementId()`, removed non-existent `r.column` property). Graph saved to `kg_preview.html`.

### ✅ Cell 14 — Single Query
> *"Which table stores customer data and what columns does it have?"*

- Reranker loaded **without CUDA OOM** (fix: `CUDA_VISIBLE_DEVICES=""` during init).
- Answer generated on first attempt, graded `grounded=True`.

```
The **Customer** table stores the customer data. According to the context it
contains a **primary key**, **full name**, **email**, and **region code** columns.
```

---

### ✅ Cell 15 — Batch Queries (3/3 correct)

| # | Question | Grader result | Notes |
|---|----------|---------------|-------|
| 1 | What entities exist in the business domain? | ✅ `grounded=True` | Customer, Sales Order |
| 2 | Which table stores customer information? | ✅ `grounded=True` (after 1 regenerate) | Grader rejected first answer as too vague → regenerated with full column list |
| 3 | How are customers and orders related? | ✅ `grounded=True` (after 1 regenerate) | Grader rejected first answer (ungrounded FK claim) → regenerated with "customer reference column links each order to CUST_MASTER" |

**Final answers:**

**Q1:** The business domain includes the entities **Sales Order** and **Customer**.

**Q2:** The Customer table stores customer information, as it contains the primary key, full name, email, and region code and is described as the master record for every customer account.

**Q3:** The Sales Order table contains a "customer reference" column that links each order to a record in the Customer master table, indicating that every sales order is associated with a customer.

---

## Issues Fixed in This Run

| Issue | Fix | Status |
|-------|-----|--------|
| Extraction model hardcoded to LM Studio | `get_extraction_llm()` uses `detect_provider()` → routes `openai/gpt-oss-20b` to OpenRouter | ✅ |
| Reranker CUDA OOM (GPU occupied by LM Studio) | `CUDA_VISIBLE_DEVICES=""` during `FlagReranker` init | ✅ |
| Graph viz Neo4j `id()` deprecation warnings | `id()` → `elementId()` in pyvis Cypher queries | ✅ |
| Graph viz warning on non-existent `r.column` | Removed from `COALESCE`, kept only `r.confidence` | ✅ |

## Remaining Known Issues

| Issue | Severity | Notes |
|-------|----------|-------|
| Cypher single-quote syntax error on string values | Low | Consistently healed on attempt 2 by Cypher Healing loop |
| Grader JSON parse error on attempt 1 (occasional) | Low | Resolved by reflection on attempt 2 |
