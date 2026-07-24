# Changelog — v1.6.1

**Date:** 2026-07-24
**Type:** Patch — fixes two OWL round-trip bugs found by a real DS01 end-to-end run

## Summary

A real `run_builder` (AB-BEST config) → export → import cycle on DS01 exposed two round-trip bugs that the synthetic unit/integration tests missed. Both fixed. DS01 now round-trips **exactly**: 82 nodes → 82, 87 edges → 87 across every relationship type.

## Fixes

### 1. Cross-partition edges dropped (MENTIONS 11→0)

`MENTIONS` edges (Chunk → BusinessConcept) were lost on round-trip. Root cause: the exporter partitions nodes AND edges into separate `.owl` files, and each file's RDF build only knew the nodes in its own partition. An edge crossing label partitions (Chunk in `technical.owl`, BusinessConcept in `entities.owl`) lost its endpoint → dropped.

**Fix:** `_partition_edges` now carries BOTH endpoint nodes into each edge's partition file, so every file is self-contained and cross-partition edges resolve.

### 2. Wrong relationship type (HAS_COLUMN 42→0)

The mapper's known-relationship list had `HAS_ATTRIBUTE`, but the builder actually creates `HAS_COLUMN` (PhysicalTable → Attribute). 42 edges silently dropped on export.

**Fix:** added `HAS_COLUMN` to the known relationship types (mapper + importer + exporter partition). `HAS_ATTRIBUTE` kept for safety.

## Verification

Real DS01 build (7 tables, LLM-driven extraction/mapping/Cypher healing) → export 4 OWL files → wipe → import clean:

```
nodes  82 → 82   (BusinessConcept 7, PhysicalTable 7, Attribute 42, Chunk 19, ParentChunk 7)
edges  87 → 87   (CHILD_OF 19, HAS_COLUMN 42, MAPPED_TO 7, MENTIONS 12, REFERENCES 7)
```

- **Unit:** 30 OWL tests pass (added `test_cross_partition_edges_survive_file_split` regression guard, no Neo4j).
- **Full suite:** 560 unit tests pass, zero regressions.
- **Lint:** ruff clean.

## Files

- `src/graph/owl_exporter.py` — `_partition_edges` rewrite + `HAS_COLUMN` in partition
- `src/graph/owl_mapper.py` — `HAS_COLUMN` in `_REL_TYPES`
- `src/graph/owl_importer.py` — `HAS_COLUMN` in `_ALLOWED_RELS`
- `tests/unit/test_owl_exporter.py` — cross-partition regression test
