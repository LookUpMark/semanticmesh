# Run 02 — Full Fixtures Results

**Date:** 2026-03-13  
**Input:** Full fixtures (`sample_docs/business_glossary.txt` + `sample_docs/data_dictionary.txt`, `sample_ddl/simple_schema.sql`)  
**Models:** Reasoning `openai/gpt-oss-120b` → OpenRouter · Extraction `openai/gpt-oss-20b` → OpenRouter  
**Previous run (Run 01):** smoke fixtures (2 chunks, 42 triplets, 217s)

---

## Builder Graph Summary

| Metric | Value |
|--------|-------|
| **Total time** | 1212.2 s (~20 min 12 s) |
| **Chunks processed** | 18 (5 from business_glossary + 13 from data_dictionary) |
| **Triplets extracted** | 483 |
| **Entities resolved** | 170 |
| **Tables parsed** | 3 |
| **Tables enriched** | 3 / 3 |
| **Tables completed** | 3 / 3 |
| **Cypher failures** | False |

---

## Cell-by-Cell Analysis

### Cell 0 — Configuration Check ✅

```
Reasoning  : 'openai/gpt-oss-120b'  →  provider=openrouter  max_tokens=16384
Extraction : 'openai/gpt-oss-20b'   →  provider=openrouter  max_tokens=16384
Documents  : 2 file(s)
DDL files  : 1 file(s)
Neo4j      : bolt://localhost:7687
```

Both models correctly routed to OpenRouter. `detect_provider()` working as expected.

---

### Cell 1 — Environment Check ✅

```
Neo4j      : OK  (bolt://localhost:7687)
LM Studio  : skipped (extraction uses openrouter)
```

Neo4j reachable. LM Studio check correctly skipped because `openai/gpt-oss-20b` contains `/` → routed to OpenRouter.

---

### Cell 2 — Document Loading ✅

```
Loaded text file 'business_glossary.txt'   → 5 chunks (chunk_size=512, overlap=64)
Loaded text file 'data_dictionary.txt'     → 13 chunks (chunk_size=512, overlap=64)
Parsed 3 table(s) from DDL input.

Documents loaded : 2 file(s)  →  18 chunk(s)
DDL files loaded : 1 file(s)  →   3 table(s)
```

Chunking worked correctly. Full fixtures are significantly larger than smoke (2 chunks → 18 chunks).

---

### Cell 3 — Builder Graph Run

#### 3a. Triplet Extraction ⚠️ (1 chunk truncated)

| Chunk | Source | Triplets | Latency |
|-------|--------|----------|---------|
| 0 | business_glossary.txt | 23 | 30.2 s |
| 1 | business_glossary.txt | 22 | 20.9 s |
| 2 | business_glossary.txt | 25 | 54.0 s |
| 3 | business_glossary.txt | 35 | 64.9 s (429 retry) |
| 4 | business_glossary.txt | 24 | 14.4 s |
| 0 | data_dictionary.txt | 32 | 24.0 s |
| 1 | data_dictionary.txt | 24 | 52.5 s |
| 2 | data_dictionary.txt | 8 | 16.2 s |
| 3 | data_dictionary.txt | 30 | 95.3 s |
| 4 | data_dictionary.txt | 15 | 18.7 s |
| 5 | data_dictionary.txt | 39 | 151.2 s |
| **6** | **data_dictionary.txt** | **0** | **91.6 s (truncated)** |
| 7 | data_dictionary.txt | 24 | 53.9 s |
| 8 | data_dictionary.txt | 32 | 65.6 s |
| 9 | data_dictionary.txt | 43 | 86.2 s |
| 10 | data_dictionary.txt | 35 | 9.9 s |
| 11 | data_dictionary.txt | 50 | ~88 s |
| 12 | data_dictionary.txt | 22 | ~33 s |
| **Total** | | **483** | **~976 s** |

**Issue — Chunk 6 truncated:** `output_tokens=16384` (hit the cap) → empty content → non-JSON warning on attempt 1 → reflection prompt sent → reflection returned 0 triplets (chunk content was apparently too dense even for the reflection pass). Lost ~1 chunk worth of triplets. This is the same `max_tokens` cap trade-off: prevents empty content for most chunks but can still truncate the heaviest ones.

**Mitigation options:** reduce `CHUNK_SIZE`, or increase `LLM_MAX_TOKENS_EXTRACTION` beyond 16384.

**Chunk 3 business_glossary:** 429 rate-limit hit mid-stream, recovered automatically.

**Per-source totals:**
- `business_glossary.txt` (5 chunks): 23+22+25+35+24 = **129 triplets**
- `data_dictionary.txt` (13 chunks): 32+24+8+30+15+39+0+24+32+43+35+50+22 = **354 triplets**

---

#### 3b. Entity Resolution ⚠️ (2 non-JSON, both auto-recovered)

- **Blocking:** extracted unique entities from 483 triplets, formed clusters (threshold=0.75)
- **Entities resolved:** 170
- **ER judge warning 1:** cluster `'DESCRIPTION'` — non-JSON on attempt 1, recovered on attempt 2
- **ER judge warning 2:** cluster `'product navigation and search filters'` — non-JSON on attempt 1, recovered on attempt 2

Both recovered via the self-reflection loop. The reflection prompt correctly triggered the model to emit valid JSON on the second attempt.

---

#### 3c. Schema Enrichment ✅

All 3 tables enriched:
- `CUSTOMER_MASTER` → `Customer Master`
- `TB_PRODUCT` → `Product`
- `SALES_ORDER_HDR` → `Sales Order Header`

---

#### 3d. Schema-to-Ontology Mapping ✅

| Table | Mapped To | Confidence | Critic |
|-------|-----------|------------|--------|
| CUSTOMER_MASTER | Customer Master | **95%** | approved ✅ |
| TB_PRODUCT | Product | **95%** | approved ✅ |
| SALES_ORDER_HDR | Sales Order | **96%** | approved ✅ |

All 3 mappings approved by the Actor-Critic validator on the first attempt. No HITL interrupt triggered.

---

#### 3e. Cypher Generation & Healing ⚠️ (1 healing required)

- **CUSTOMER_MASTER:** generated and executed cleanly ✅
- **TB_PRODUCT:** generated and executed cleanly ✅
- **SALES_ORDER_HDR:** ⚠️ Cypher syntax error on attempt 1
  - **Root cause:** LLM embedded the SQL default value `'PENDING'` as `''PENDING''` inside the `ddl_source` string literal, producing an unescaped single-quote inside a Cypher string
  - **Healed on attempt 2** ✅ — `cypher_healer` injected the error message as reflection context, model fixed the quoting
  - **FK edge created:** `SALES_ORDER_HDR.CUST_ID → CUSTOMER_MASTER` ✅

This is the same recurring single-quote bug documented in Run 01. The healing loop reliably resolves it on attempt 2.

---

#### 3f. Builder Graph Summary Block ✅

```
Elapsed             : 1212.2 s
Triplets extracted  : 483
Entities resolved   : 170
Tables parsed       : 3
Tables enriched     : 3
Tables completed    : 3
Cypher failures     : False

Completed tables:
  - CUSTOMER_MASTER
  - TB_PRODUCT
  - SALES_ORDER_HDR
```

`cypher_failed=False` — all 3 tables successfully upserted via LLM-generated (or healed) Cypher.

---

### Cell 4 — Knowledge Graph Inspection ✅

```
Node counts
  ['PhysicalTable']   : 3
  ['BusinessConcept'] : 3

Business Concepts
  Product
  Sales Order
  Customer Master

Concept → Table Mappings
  Sales Order     → SALES_ORDER_HDR   (96.0%)
  Customer Master → CUSTOMER_MASTER   (95.0%)
  Product         → TB_PRODUCT        (95.0%)
```

Graph correctly reflects 3 business concepts, 3 physical tables, and 3 mapping edges. FK edge `SALES_ORDER_HDR -[:REFERENCES]→ CUSTOMER_MASTER` also present.

---

### Cell 5 — Knowledge Graph Visualization ✅

PyVis graph rendered and saved to `notebooks/kg_preview.html`. No Neo4j deprecation warnings (fixed in prior session: `id()` → `elementId()`).

---

### Cell 6 — Single Query ✅

**Query:** "Which table stores customer data and what columns does it have?"

- **Reranker:** loaded on CPU (no CUDA OOM), top chunk `'Customer Master'` (score=0.5884, pool=7, top_k=5)
- **Answer:** *"The customer data is stored in the **Customer Master** table (physical table `CUSTOMER_MASTER`). It contains the columns **ID**, **name**, **email**, **region** and **status**.【1】"*
- **Grader:** `grounded=True, action=pass` ✅

Correct answer, grounded on first attempt.

---

### Cell 7 — Batch Queries ✅

| # | Question | Top Chunk (score) | Grader | Notes |
|---|----------|-------------------|--------|-------|
| 1/3 | What entities exist in the business domain? | Sales Order (0.0049) | pass ✅ | ⚠️ Answer mentions only SalesOrder — incomplete |
| 2/3 | Which table stores customer information? | Customer Master (0.6665) | pass ✅ | Correct ✅ |
| 3/3 | How are customers and orders related? | Sales Order (0.0070) | pass ✅ | Correct ✅ |

**Answers:**

**[1/3]** *"The business domain includes the **SalesOrder** entity, which is mapped to the SALES_ORDER_HDR table."*  
⚠️ **Incomplete** — answer only cites SalesOrder. The reranker top chunk had score=0.0049 (very low), suggesting poor retrieval for this broad query. The model only had context about Sales Order in the top-k retrieved chunks. Customer Master and Product were not represented in the top results.

**[2/3]** *"The customer information is stored in the **Customer Master** table (CUSTOMER_MASTER).【1†source】"*  
✅ Correct and grounded.

**[3/3]** *"Customers are stored in the **Customer Master** table (the master record for all registered platform customers). Each sales order record in **SALES_ORDER_HDR** (the Sales Order header) includes a **customer reference** that links an order to the corresponding customer in Customer Master."*  
✅ Correct, well-structured, cites the FK relationship.

No `regenerate` loops triggered — all 4 answers (including Cell 6) passed grading on the first attempt.

---

### Cell 8 — Cleanup ✅

Cleanup cell left commented, as expected.

---

### Cell 9 — Graph Clear ✅

`Knowledge Graph cleared.` — ran successfully (development utility).

---

## Issues Found

| # | Severity | Description | Status |
|---|----------|-------------|--------|
| 1 | Medium | Chunk 6 of data_dictionary.txt hit `max_tokens=16384` cap → 0 triplets extracted (content lost) | Known — workaround: reduce `CHUNK_SIZE` or raise token cap |
| 2 | Low | ER judge non-JSON on attempts 1/3 for 2 clusters (`DESCRIPTION`, `product navigation and search filters`) | Auto-recovered via self-reflection ✅ |
| 3 | Low | Cypher single-quote bug on `SALES_ORDER_HDR` (`DEFAULT 'PENDING'`) | Auto-healed on attempt 2 ✅ |
| 4 | Low | Q1 "What entities exist?" only cited SalesOrder (low reranker score 0.0049) | Retrieval gap — broad queries need improved vector coverage or multi-hop graph traversal |

---

## Comparison with Run 01 (Smoke Fixtures)

| Metric | Run 01 (smoke) | Run 02 (full) | Δ |
|--------|---------------|---------------|---|
| Chunks | 2 | 18 | +16 |
| Triplets | 42 | 483 | +441 (+1050%) |
| Entities resolved | 38 | 170 | +132 |
| Tables completed | 2/2 | 3/3 | +1 |
| Elapsed | 217 s | 1212 s | +995 s |
| Cypher healings | 0 | 1 | +1 |
| Grader regenerate loops | 0 | 0 | = |
| Q&A pass rate | 3/3 ✅ | 4/4 ✅ | = |
| Chunk truncations | 0 | 1 | +1 |

---

## Notes

- **Scale:** 11× more triplets than smoke run, 5.6× longer — linear scaling as expected for sequential extraction.
- **Chunk 11 was the richest:** 50 triplets from a single 512-token chunk of `data_dictionary.txt` — very dense structured content.
- **All hallucination checks passed on first attempt** — the richer knowledge graph provides better grounding context.
- **Retrieval quality degrades on broad queries** (Q1) — with 170 entities in the graph, a broad open-ended query like "what entities exist?" may benefit from graph-traversal retrieval over pure vector similarity.
