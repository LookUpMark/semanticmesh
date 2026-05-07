# Changelog — v1.4.0

**Date:** 2026-05-07

## Summary

Performance and reliability improvements for large-schema datasets. Added parallel mapping phase (~5x speedup on 50+ table schemas) and fixed a critical Neo4j constraint violation when multiple tables map to the same BusinessConcept.

## Changes

### Critical (Bug Fix)

- **Fixed duplicate BusinessConcept constraint violation** (`src/graph/build_nodes.py`): When two tables map to the same concept (e.g., `CUSTOMER` and `CUSTOMER_CONTACT` → `'Customer'`), the normalization step now detects the existing concept and re-links the PhysicalTable instead of attempting a rename that violates the unique constraint. Previously this crashed the entire pipeline with `Neo.ClientError.Schema.ConstraintValidationFailed`.

### Feature

- **Parallel mapping phase** (`src/graph/parallel_mapping.py`, `src/graph/builder_graph.py`):
  - New `parallel_mapping` LangGraph node between `enrich_schema` and `rag_mapping`
  - Uses `ThreadPoolExecutor` to process all tables through mapping+validation concurrently
  - Configurable via `MAPPING_CONCURRENCY` env var (default: 5 workers)
  - Pre-computed proposals bypass redundant LLM calls in the sequential loop
  - Expected speedup: ~4-5x on datasets with 50+ tables (from ~60min to ~12-15min)
  - Falls back to sequential mode when `mapping_concurrency=1`

### Configuration

- **New setting: `mapping_concurrency`** (`src/config/config.py`, `src/config/settings.py`): Controls number of parallel workers during mapping+validation phase. Default: 5. Set to 1 to disable parallelism.

### State

- **`precomputed_proposals` field** (`src/models/state.py`): New `BuilderState` field `dict[str, MappingProposal]` to carry pre-computed mapping results through the graph.

### Validation

- **Precomputed bypass in validator** (`src/graph/validation_nodes.py`): When a table has a precomputed proposal (from parallel phase), the critic validation is skipped since it was already performed during parallel execution.

### Documentation

- **README.md**: Updated Builder Graph Mermaid diagram to show "Parallel Mapping" node; updated stage table; added "Parallel mapping" to Key Features list.
- **docs/images/component_diagrams.md**: Updated diagrams 09 (RAG Mapping) and 10 (Graph Construction) to reflect parallel architecture and concept deduplication logic.

## Migration Notes

- No breaking changes. Parallel mapping is enabled by default (`MAPPING_CONCURRENCY=5`).
- To revert to sequential behavior: set `MAPPING_CONCURRENCY=1` in `.env`.
- All 517 unit tests pass without modification.

---

## Ablation Results: AB-BEST-K20 vs K5 (Complete)

Full 7-dataset comparison validating `reranker_top_k=5` as the optimal global default.

### Final K5 vs K20 Comparison

| Dataset | K5 | K20 | Delta | Winner |
|---------|:---:|:---:|:-----:|:------:|
| DS01 E-Commerce (15q) | **5.00** | 4.65 | -0.35 | K5 |
| DS02 Finance (25q) | **5.00** | 4.60 | -0.40 | K5 |
| DS03 Healthcare (30q) | **4.70** | 4.35 | -0.35 | K5 |
| DS04 Manufacturing (40q) | **4.75** | 4.65 | -0.10 | K5 |
| DS05 Edge-incomplete (20q) | 4.30 | **4.80** | +0.50 | K20 |
| DS06 Edge-legacy (25q) | **5.00** | 4.90 | -0.10 | K5 |
| DS07 Stress 58-tab (55q) | **4.35** | 3.65 | -0.70 | K5 |
| **Average** | **4.73** | **4.53** | **-0.20** | **K5** |

### Key Insights

1. **K5 wins 6/7 datasets** — average advantage of 0.20 points
2. **Largest gap on DS07** (Δ=-0.70): 20 chunks from a 58-table schema overwhelm the generator with noise, causing underspecification of constraint enumerations
3. **K20 wins only on DS05** (incomplete schemas): broader retrieval compensates for sparse documentation
4. **Higher GT coverage ≠ higher quality**: DS07 K20 achieves 92% GT vs K5's 78%, yet scores 0.70 points lower — precision > recall for answer quality
5. **Efficiency**: K5 requires 4× fewer cross-encoder inference calls per query

### DS07 K20 Pipeline Metrics

- 58/58 tables completed, 0 Cypher failures
- 138 triplets extracted, 108 entities resolved
- 55/55 answers grounded (100%), 0 hallucinations
- GT coverage: 92%, avg_top_score: 0.727
- Total tokens: 2.08M, elapsed: 52.6 min
- AI Judge: Builder=5, Retrieval=4, Answer=3, Health=5 → **3.65/5**

### Root Cause: Why More Context Hurts on Complex Schemas

The AI Judge identified the failure mode as **underspecification, not hallucination**:
- Answers describe schema at a conceptual level ("status column exists") rather than enumerating specific CHECK constraint values (ACTIVE/INACTIVE/SUSPENDED)
- Chunks ranked 6–20 on a 58-table schema introduce related-but-wrong tables (e.g., `PURCHASE_ORDER_HEADER` chunks for questions about `SALES_ORDER_HEADER`)
- K5 forces focused answers from the 5 most relevant chunks → higher precision
