# Changelog — v1.6.0

**Date:** 2026-07-24
**Type:** Minor — new OWL 2 DL export/import feature (first new runtime capability since v1.5.1)

## Summary

Adds **OWL 2 DL export/import** for the SemanticMesh Knowledge Graph, enabling interoperability with external ontology tools (Protégé, Stardog, GraphDB) and portable backup/restore of the full graph. Template-based mapping with `rdflib` — deterministic, zero LLM cost. Reuses the existing `kg_registry` node/edge dump and snapshot system rather than duplicating graph I/O.

**559 unit tests pass** (530 baseline + 29 new), zero regressions. Neo4j integration round-trip test green.

## New Components

| File | Responsibility |
|------|---------------|
| `src/graph/owl_mapper.py` | Pure dict↔RDF mapping — node/edge → OWL triples, lossless round-trip serialize/parse |
| `src/graph/owl_exporter.py` | Neo4j → 4 split `.owl` files + `metadata.json` with SHA-256 checksums |
| `src/graph/owl_importer.py` | Parse `.owl` → dicts → Cypher MERGE (clean / versioned / merge strategies) |
| `src/api/demo_router.py` | 4 endpoints under `/api/v1/demo/kg/owl` |
| `src/api/models.py` | `OwlExportRequest`/`OwlExportMeta`, `OwlImportRequest`/`OwlImportResult` |

## API

| Method | Path | Purpose |
|--------|------|---------|
| `POST` | `/api/v1/demo/kg/owl/export` | Export live KG → 4 OWL files |
| `GET` | `/api/v1/demo/kg/owl/export/{export_id}` | Download export as `.tar.gz` |
| `GET` | `/api/v1/demo/kg/owl/export` | List exports |
| `POST` | `/api/v1/demo/kg/owl/import` | Import OWL documents (strategy: clean \| versioned \| merge) |

## Design decisions

- **"Versioned" import = auto-snapshot backup**, NOT Neo4j named graphs. Docker `neo4j:5` is Community Edition — `CREATE DATABASE`/fabric unavailable. Rollback safety delivered via existing `kg_registry.save_snapshot` before clear+rebuild. Same external contract.
- **Reified edge properties** (`rdf:Statement` blank nodes) for lossless edge-prop round-trip (e.g. mapping confidence).
- **Multi-document import** — exporter emits 4 complete XML files; `from_owl_documents()` parses each and unions RDF triples (concatenating XML is invalid).
- **`embedding` vectors dropped** on export/import (regenerated on query), mirroring `kg_registry`.
- **URL-quoted URIs** (`safe=""`) so `SourceFile` paths and `Chunk` source_doc containing `/` round-trip unambiguously.

## Security

- `export_id` validated as `YYYYMMDD_HHMMSS` with path-containment check in `export_dir` — blocks traversal via the download endpoint.
- Import accepts inline OWL content only (no server file-read path).
- Generic error messages + `logger.exception` (no exception-text leakage).

## Bugs caught during development

- Multi-document XML concatenation → invalid XML ("junk after document element"). Fixed via per-document parse + triple union.
- Relationship param collision when both edge endpoints are single-key nodes using `$key`. Fixed via namespaced params (`a_key`/`b_key`).
- `node_to_rdf` only skipped `key[0]` for compound keys → `source_doc` double-encoded (URI + triple). Fixed: skip all identity key props.
- Path traversal in download endpoint (final review). Fixed.

## Verification

- **Unit:** 559 passed (530 baseline + 29 new OWL tests). `.venv/bin/python -m pytest tests/unit/ -m "not slow" -q`
- **Integration:** Neo4j round-trip — seed KG → export 4 files → wipe → import clean → verify nodes + edge preserved. `.venv/bin/python -m pytest tests/integration/test_owl_flow.py -m integration`
- **Lint:** `ruff check` clean on all new files.
- **HTTP layer:** TestClient confirms traversal `..` blocked (404), malformed id → 400, valid-but-absent → 404.

## Dependencies

- Added `rdflib>=7.0,<8.0` (pure-Python RDF library). No Neo4j RDF plugin required.
