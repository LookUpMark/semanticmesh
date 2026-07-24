# Changelog — v1.6.2

**Date:** 2026-07-24
**Type:** Patch — lossless edge round-trip via per-edge reification (found by DS07 stress test)

## Summary

The DS07 stress test (58 tables → ~815 nodes, ~922 edges) revealed that multiple relationships of the same type between the same node pair were silently collapsed on export. Fixed with per-edge `rdf:Statement` reification. DS07 now round-trips **exactly**: nodes and edges both 100% preserved.

## The bug

RDF triples are unique by `(subject, predicate, object)`. Two edges of the same type between the same pair — e.g. table `A` with two FK columns both referencing table `B` — serialize to the **same** triple, collapsing into one. DS07 lost 7 of 90 `REFERENCES` edges this way (multi-FK-to-same-table). The ontology structure (`A` references `B`) was preserved; only the secondary FK-column detail was lost.

## Fix

- **Export (`edge_to_rdf`):** every edge now emits a distinct reified `sm:Statement` blank node (carrying its own `subject`/`predicate`/`object`/props) **plus** the base triple (kept for graph visualization in Protégé).
- **Import (`from_owl_xml`):** edges are extracted from reified statements (one edge per statement), so duplicate-pair edges survive. A base-triple fallback handles OWL produced by external tools (Protégé/Stardog) that emit plain triples without reification.
- **Import MERGE:** the relationship pattern includes the edge's properties (`MERGE (a)-[r:T {column: $rp_column}]->(b)`) so duplicate-pair edges write as distinct relationships.

## Verification

Real DS07 build (58 tables, LLM-driven) → export 4 OWL files → wipe → import clean:

```
nodes  812 → 812   ✅  (BusinessConcept 41, PhysicalTable 55, Attribute 634, Chunk 63, ParentChunk 19)
edges  922 → 922   ✅  (CHILD_OF 63, HAS_COLUMN 634, MAPPED_TO 55, MENTIONS 80, REFERENCES 90)
```

`REFERENCES` 90→90 (was 90→83 in v1.6.1). Export 0.6s / 2.4 MB, import 2.7s.

- **Unit:** 31 OWL tests pass (added `test_duplicate_pair_edges_distinguished_by_props` regression guard).
- **Full suite:** 561 unit tests pass, zero regressions.
- **Lint:** ruff clean.

## Files

- `src/graph/owl_mapper.py` — `edge_to_rdf` always reifies; `from_owl_xml` extracts from statements + fallback
- `src/graph/owl_importer.py` — MERGE pattern includes edge props
- `tests/unit/test_owl_importer.py` — duplicate-pair regression test
