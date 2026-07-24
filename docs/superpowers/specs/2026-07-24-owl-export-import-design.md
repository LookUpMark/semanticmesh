# OWL Export/Import Feature — Design Specification

**Project:** SemanticMesh GraphRAG
**Date:** 2026-07-24
**Author:** Marc'Antonio Lopez
**Status:** Design Approved — Pending Implementation Plan

---

## Overview

Add OWL 2 DL export/import capability to SemanticMesh Knowledge Graph, enabling:

1. **Interoperability** with external ontology tools (Protégé, Stardog, GraphDB)
2. **Backup/restore** of complete Knowledge Graph state
3. **Exchange** with other Data Governance systems (Collibra, Alation)

**Approach:** Template-based mapping (rdflib) — deterministic, zero LLM costs, fast.

---

## Architecture

### New Components

```python
src/graph/
  owl_exporter.py      # Neo4j → RDF (rdflib) → OWL files
  owl_importer.py      # OWL files → rdflib → Cypher MERGE
  owl_mapper.py        # Neo4j schema ↔ OWL 2 DL mapping rules
  owl_registry.py      # Export versioning (timestamp, checksums)

src/api/
  (new endpoints in existing FastAPI app)

src/models/schemas.py
  (new Pydantic models: OwlExportRequest, OwlExportMetadata, OwlImportRequest)
```

### API Endpoints

```python
POST /api/v1/kg/export/owl       # Export split (entities.owl + tables.owl + ...)
GET  /api/v1/kg/export/{id}      # Download export by ID
GET  /api/v1/kg/export/list      # List exports

POST /api/v1/kg/import/owl       # Import with strategy param
GET  /api/v1/kg/import/{id}      # Import status
```

### Dependencies

- `rdflib` (add to `pyproject.toml` if not present)
- `neo4j-rdf-ext` (optional, for direct RDF from Neo4j)

---

## OWL 2 DL Mapping Schema

### Neo4j → OWL Class Mapping

| Neo4j Node | OWL Type | Notes |
|------------|----------|-------|
| `BusinessConcept` | `owl:Class` + `skos:Concept` | Entity with definition |
| `PhysicalTable` | `owl:Class` + `skos:Concept` | Table schema |
| `Attribute` | `owl:DatatypeProperty` | Column metadata |
| `Document` | `dct:Source` + `prov:Entity` | Provenance |
| `Chunk` | `prov:Entity` | Text provenance |

### Neo4j → OWL Property Mapping

| Neo4j Relationship | OWL Property | Domain | Range |
|--------------------|--------------|--------|-------|
| `MAPPED_TO` | `owl:ObjectProperty` | `BusinessConcept` | `PhysicalTable` |
| `REFERENCES` | `owl:ObjectProperty` | `PhysicalTable` | `PhysicalTable` |
| `HAS_ATTRIBUTE` | `owl:ObjectProperty` | `PhysicalTable` | `Attribute` |
| `DESCRIBED_BY` | `owl:ObjectProperty` | `BusinessConcept` | `Chunk` |

### Neo4j Properties → OWL Annotations

| Neo4j Property | OWL Annotation |
|----------------|----------------|
| `Entity.name` | `rdfs:label` |
| `Entity.definition` | `skos:definition` |
| `Entity.synonyms` | `skos:altLabel` |
| `Entity.provenance_text` | `prov:wasGeneratedBy` |
| `TableSchema.ddl_source` | `dct:source` |
| `TableSchema.comment` | `rdfs:comment` |
| `ColumnSchema.data_type` | `rdfs:range` |

### OWL Prefixes

```turtle
@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix skos: <http://www.w3.org/2004/02/skos/core#> .
@prefix prov: <http://www.w3.org/ns/prov#> .
@prefix dct: <http://purl.org/dc/terms/> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .
@prefix sm: <http://semanticmesh/graph/v1#> .
```

---

## Export Flow

### Pipeline

```python
def export_kg_to_owl(
    include_embeddings: bool = False,
    include_chunks: bool = False,
) -> OwlExportMetadata:
    """
    1. Query Neo4j for all nodes/relationships
    2. Separate by type (entities, tables, mappings, technical)
    3. Convert each group → RDF triples (rdflib)
    4. Write .owl files to export/ directory
    5. Generate metadata.json + checksums
    6. Return export_id for download
    """
```

### Cypher Queries

```cypher
// BusinessConcepts
MATCH (bc:BusinessConcept) RETURN bc

// PhysicalTables
MATCH (pt:PhysicalTable) RETURN pt

// Mappings
MATCH (bc:BusinessConcept)-[r:MAPPED_TO]->(pt:PhysicalTable)
RETURN bc, r, pt

// Attributes
MATCH (pt:PhysicalTable)-[:HAS_ATTRIBUTE]->(a:Attribute)
RETURN pt, a
```

### RDF Conversion

```python
# Example: BusinessConcept → owl:Class
uri = URIRef(f"sm:concept/{entity.name}")
graph.add((uri, rdf.type, owl.Class))
graph.add((uri, rdfs.label, Literal(entity.name)))
graph.add((uri, skos.definition, Literal(entity.definition)))
for synonym in entity.synonyms:
    graph.add((uri, skos.altLabel, Literal(synonym)))
```

### File Structure

```
export_{timestamp}/
  ├── metadata.json          # timestamp, version, checksums
  ├── entities.owl           # BusinessConcept + Triplet
  ├── tables.owl             # PhysicalTable + Attribute
  ├── mappings.owl           # MAPPED_TO, REFERENCES relationships
  └── technical.owl          # Chunk, Document, embeddings (optional)
```

### API Contract

**Request:**
```python
POST /api/v1/kg/export/owl
{
  "include_embeddings": false,
  "include_chunks": false
}
```

**Response:**
```python
202 Accepted
{
  "export_id": "20250124_143022",
  "status": "processing",
  "estimated_seconds": 10
}
```

**Download:**
```python
GET /api/v1/kg/export/{id}
→ 200 OK (application/x-tar) tarball stream
```

---

## Import Flow

### Pipeline

```python
def import_owl_to_kg(
    owl_files: list[str],
    strategy: Literal["clean", "versioned", "merge"],
) -> str:
    """
    1. Parse .owl files → rdflib Graph
    2. Convert RDF triples → Cypher MERGE statements
    3. Execute on Neo4j with chosen strategy
    4. Return import_id
    """
```

### RDF Parsing

```python
graph = rdflib.Graph()
for owl_file in owl_files:
    graph.parse(owl_file, format="xml")
```

### RDF → Cypher Conversion

```python
for subj, pred, obj in graph:
    if pred == rdf.type and obj == owl.Class:
        concept_name = extract_local_name(subj)
        cypher = build_merge_cypher("BusinessConcept", concept_name)
        # Example MERGE:
        # MERGE (bc:BusinessConcept {name: 'Customer'})
        # SET bc.definition = '...', bc.synonyms = [...]
```

### Import Strategies

| Strategy | Behavior | Use Case |
|----------|----------|----------|
| `clean` | `MATCH (n) DETACH DELETE n` then import | Full rebuild, migration |
| `versioned` | Create new graph `graph_{timestamp}` | A/B testing, rollback |
| `merge` | MERGE statements only, no delete | Incremental updates |

### API Contract

**Request:**
```python
POST /api/v1/kg/import/owl
{
  "strategy": "versioned",
  "files": ["entities.owl", "tables.owl", "mappings.owl"]
}
```

**Response:**
```python
202 Accepted
{
  "import_id": "imp_20250124_143055",
  "status": "processing"
}
```

**Status Check:**
```python
GET /api/v1/kg/import/{id}
→ 200 OK
{
  "status": "completed",
  "nodes_created": 150,
  "relationships_created": 80,
  "duration_seconds": 12
}
```

---

## Pydantic Models

```python
class OwlExportRequest(BaseModel):
    include_embeddings: bool = False
    include_chunks: bool = False

class OwlExportMetadata(BaseModel):
    export_id: str
    timestamp: datetime
    files: list[str]
    checksums: dict[str, str]
    nodes_count: int
    relationships_count: int

class OwlImportRequest(BaseModel):
    strategy: Literal["clean", "versioned", "merge"]
    files: list[str]
    target_version: str | None = None

class OwlImportStatus(BaseModel):
    import_id: str
    status: Literal["pending", "processing", "completed", "failed"]
    nodes_created: int = 0
    nodes_merged: int = 0
    relationships_created: int = 0
    errors: list[str] = []
```

---

## Error Handling

### Export Errors

| Error | HTTP Status | Response |
|-------|-------------|----------|
| Neo4j connection failure | 503 | `{"error": "neo4j_unavailable"}` |
| Empty graph | 404 | `{"error": "no_data_to_export"}` |
| File write failure | 500 | `{"error": "file_write_failed", "path": "..."}` |
| RDF serialization error | 500 | `{"error": "rdf_serialization_failed", "detail": "..."}` |

### Import Errors

| Error | HTTP Status | Response |
|-------|-------------|----------|
| Malformed OWL file | 400 | `{"error": "invalid_owl", "parser_error": "..."}` |
| Unsupported strategy | 400 | `{"error": "unsupported_strategy", "hint": "use clean|versioned|merge"}` |
| Cypher execution error | 500 | `{"error": "cypher_failed", "query": "...", "detail": "..."}` |
| Transaction rollback | 500 | `{"error": "transaction_rolled_back", "reason": "..."}` |

### Monitoring (Langfuse/LangSmith)

```python
# Export events
export_event = {
    "export_id": export_id,
    "nodes_count": nodes,
    "rels_count": rels,
    "duration_ms": elapsed,
    "file_size_mb": total_size,
    "include_embeddings": include_embeddings,
}

# Import events
import_event = {
    "import_id": import_id,
    "strategy": strategy,
    "nodes_created": created,
    "nodes_merged": merged,
    "errors": error_count,
    "duration_ms": elapsed,
}
```

---

## Testing Strategy

### Unit Tests (No Services)

```python
tests/unit/test_owl_mapper.py
- test_business_concept_to_owl_class()
- test_physical_table_to_owl_class()
- test_attribute_to_datatype_property()
- test_relationships_to_object_properties()

tests/unit/test_owl_exporter.py
- test_rdf_graph_generation()
- test_cypher_to_rdf_conversion()
- test_file_splitting_logic()
- test_metadata_generation()

tests/unit/test_owl_importer.py
- test_owl_parser()
- test_rdf_to_cypher_conversion()
- test_merge_cypher_generation()
- test_strategy_validation()
```

### Integration Tests (Neo4j Required)

```python
tests/integration/test_owl_export_flow.py
- test_export_small_dataset()          # 1-2 tables
- test_export_large_dataset()          # 50+ tables (DS07)
- test_export_with_embeddings()
- test_export_tarball_creation()

tests/integration/test_owl_import_flow.py
- test_import_clean_strategy()
- test_import_versioned_strategy()
- test_import_merge_strategy()
- test_roundtrip_export_import()       # Critical path
```

### Property-Based Tests (Hypothesis)

```python
- test_roundtrip_preserves_all_data()
- test_cypher_merging_idempotent()
- test_checksums_consistent()
- test_concurrent_exports_idempotent()
```

### Coverage Targets

- Overall: 85%+
- Critical paths (export/import flow): 95%+
- Error paths: 80%+

---

## Performance Considerations

### Export Performance

| Dataset Size | Tables | Estimated Time | File Size |
|--------------|--------|----------------|-----------|
| Small (DS01) | 7 | ~5s | ~2MB |
| Medium (DS04) | 13 | ~8s | ~5MB |
| Large (DS07) | 58 | ~15s | ~20MB |
| Stress | 100+ | ~30s | ~50MB |

### Import Performance

| Dataset Size | Tables | Estimated Time (merge) | Estimated Time (clean) |
|--------------|--------|------------------------|------------------------|
| Small | 7 | ~6s | ~8s |
| Medium | 13 | ~10s | ~12s |
| Large | 58 | ~18s | ~22s |
| Stress | 100+ | ~35s | ~40s |

### Optimization Notes

- Use UNWIND batch for Cypher (1000 nodes/batch)
- Streaming tarball generation (no intermediate full file)
- Parallel RDF parsing for multiple .owl files
- Embedding vectors lazy load (only if `include_embeddings=True`)

---

## Implementation Phases

1. **Phase 1: Core mapping** — `owl_mapper.py`, Neo4j→OWL schema
2. **Phase 2: Export pipeline** — `owl_exporter.py`, API endpoints
3. **Phase 3: Import pipeline** — `owl_importer.py`, strategies
4. **Phase 4: Testing** — Unit + integration + property-based tests
5. **Phase 5: Documentation** — User guide, API docs, examples

---

## Open Questions

None at design time.

---

## References

- OWL 2 DL Specification: https://www.w3.org/TR/owl2-syntax/
- rdflib Documentation: https://rdflib.readthedocs.io/
- Neo4j RDF Extension: https://github.com/neo4j-contrib/neo4j-rdf-ext
- SemanticMesh Architecture: `docs/draft/SPECS.md`
