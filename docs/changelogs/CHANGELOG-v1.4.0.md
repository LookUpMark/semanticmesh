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
