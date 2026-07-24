# OWL Export/Import Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add OWL 2 DL export/import to the SemanticMesh Knowledge Graph, enabling interoperability with Protégé/Stardog/GraphDB and backup/restore of the full graph.

**Architecture:** Template-based mapping with `rdflib`. The OWL mapper translates between Neo4j node/edge dicts (the exact format `kg_registry._export_graph()` already produces) and RDF/OWL triples. Export: Neo4j → node/edge dicts → `rdflib.Graph` → 4 split `.owl` files. Import: `.owl` files → parse → node/edge dicts → Cypher MERGE (3 strategies).

**Tech Stack:** Python 3.11, `rdflib` (new dep), FastAPI, Pydantic v2, Neo4j 5.x (Community), pytest.

---

## Spec Refinements Discovered During Planning

These deviate from the approved spec but are forced by the real codebase. Flagged here so they are visible at review:

1. **No `owl_registry.py`.** `src/graph/kg_registry.py` already provides SQLite-backed snapshot versioning. The OWL layer reuses it instead of duplicating a registry. The spec's `owl_registry.py` is dropped.
2. **"Versioned" import ≠ Neo4j named graphs.** The project runs Docker `neo4j:5` (Community Edition); `CREATE DATABASE` / `db.createGraph` are Enterprise-only and will fail. Reimplemented as: snapshot the live graph via `kg_registry.save_snapshot()` (auto-backup for rollback) → then clear + rebuild. The external contract (`strategy: "versioned"`) is unchanged.
3. **`neo4j-rdf-ext` dropped.** Not needed — mapping goes Neo4j → Python dicts → RDF (and back), never RDF-native against Neo4j. One new dependency only: `rdflib`.
4. **Relationship coverage expanded.** Spec listed 4 relationship types; the real graph has 9 (`MAPPED_TO`, `HAS_ATTRIBUTE`, `REFERENCES`, `MENTIONS`, `DESCRIBED_BY`, `PART_OF`, `INSTANCE_OF`, `CONTAINS_CHUNK`, `CHILD_OF`). All known types map; unknown types are skipped with a warning (mirrors `kg_registry._ALLOWED_REL_TYPES`).

---

## Confirmed Graph Schema (ground truth from `kg_registry.py`)

**Node labels and business-identity keys:**

| Label | Key property | URI scheme |
|-------|-------------|-----------|
| `BusinessConcept` | `name` | `sm:concept/{name}` |
| `PhysicalTable` | `table_name` | `sm:table/{table_name}` |
| `Attribute` | `name` | `sm:attr/{name}` |
| `Chunk` | `chunk_index`, `source_doc` | `sm:chunk/{idx}/{source_doc}` |
| `ParentChunk` | `parent_chunk_index`, `source_doc` | `sm:pchunk/{idx}/{source_doc}` |
| `SourceFile` | `path` | `sm:file/{path}` |

**Relationship types:** `MAPPED_TO`, `HAS_ATTRIBUTE`, `REFERENCES`, `MENTIONS`, `DESCRIBED_BY`, `PART_OF`, `INSTANCE_OF`, `CONTAINS_CHUNK`, `CHILD_OF`.

**Node/edge dict format** (produced by `kg_registry._export_graph()`):

```python
node = {"eid": "...", "labels": ["BusinessConcept"], "props": {"name": "Customer", "definition": "...", "synonyms": ["Client"]}}
edge = {"eid": "...", "start_eid": "...", "end_eid": "...", "rel_type": "MAPPED_TO", "props": {"confidence": 0.9}}
```

**Note:** `embedding` vectors are dropped on export by default (mirror `kg_registry`); regenerated on query. `include_embeddings=False` is the safe default.

---

## File Structure

| File | Responsibility |
|------|---------------|
| **Create** `src/graph/owl_mapper.py` | Pure mapping: node/edge dict ↔ RDF triples. No Neo4j, no I/O. Most-tested unit. |
| **Create** `src/graph/owl_exporter.py` | Orchestrate: `_export_graph()` dicts → mapper → write 4 `.owl` files + `metadata.json`. |
| **Create** `src/graph/owl_importer.py` | Orchestrate: parse `.owl` → mapper → node/edge dicts → Cypher MERGE (clean/versioned/merge). |
| **Modify** `src/api/models.py` | Add `OwlExportRequest`, `OwlExportMeta`, `OwlImportRequest`, `OwlImportResult`. |
| **Modify** `src/api/demo_router.py` | Add 5 OWL endpoints under `/demo/kg/owl`. Auth inherited from router. |
| **Modify** `pyproject.toml` | Add `rdflib` dependency. |
| **Create** `tests/unit/test_owl_mapper.py` | Unit tests for mapper (no services). |
| **Create** `tests/unit/test_owl_exporter.py` | Unit tests for exporter (Neo4j mocked). |
| **Create** `tests/unit/test_owl_importer.py` | Unit tests for importer (Neo4j mocked). |
| **Create** `tests/integration/test_owl_flow.py` | Round-trip integration test (Neo4j required, `@pytest.mark.integration`). |

---

## Task 0: Add `rdflib` Dependency

**Files:**
- Modify: `pyproject.toml`

- [ ] **Step 1: Add rdflib to dependencies**

In `pyproject.toml`, add to the `dependencies` list (alphabetical-ish, after `ragas`):

```toml
    "rdflib>=7.0,<8.0",
```

- [ ] **Step 2: Install**

Run: `.venv/bin/pip install -e ".[dev]" 2>&1 | tail -5`
Expected: `Successfully installed ... rdflib-7.x ...`

- [ ] **Step 3: Verify import**

Run: `.venv/bin/python -c "import rdflib; print(rdflib.__version__)"`
Expected: `7.x.x`

- [ ] **Step 4: Commit**

```bash
git add pyproject.toml
git commit -m "chore: add rdflib dependency for OWL export/import"
```

---

## Task 1: OWL Mapper — Node → RDF

**Files:**
- Create: `src/graph/owl_mapper.py`
- Test: `tests/unit/test_owl_mapper.py`

- [ ] **Step 1: Write the failing tests**

Create `tests/unit/test_owl_mapper.py`:

```python
"""Unit tests for src.graph.owl_mapper — pure dict↔RDF mapping, no Neo4j."""

from __future__ import annotations

from rdflib import Graph, Literal, URIRef
from rdflib.namespace import RDF, RDFS, SKOS

from src.graph import owl_mapper


class TestNodeToRdf:
    def test_business_concept_mapped_to_sm_concept(self) -> None:
        node = {
            "eid": "1",
            "labels": ["BusinessConcept"],
            "props": {"name": "Customer", "definition": "A buyer", "synonyms": ["Client"]},
        }
        g = Graph()
        uri = owl_mapper.node_to_rdf(node, g)
        assert uri is not None
        assert uri == owl_mapper.SM["concept/Customer"]
        assert (uri, RDF.type, owl_mapper.SM.Concept) in g
        assert (uri, RDFS.label, Literal("Customer")) in g
        assert (uri, SKOS.definition, Literal("A buyer")) in g
        assert (uri, SKOS.altLabel, Literal("Client")) in g

    def test_physical_table_uses_table_name_key(self) -> None:
        node = {
            "eid": "2",
            "labels": ["PhysicalTable"],
            "props": {"table_name": "TB_CST", "ddl_source": "CREATE TABLE..."},
        }
        g = Graph()
        uri = owl_mapper.node_to_rdf(node, g)
        assert uri == owl_mapper.SM["table/TB_CST"]
        assert (uri, RDF.type, owl_mapper.SM.PhysicalTable) in g
        # unknown props land in the sm: namespace, lossless
        assert (uri, owl_mapper.SM["ddl_source"], Literal("CREATE TABLE...")) in g

    def test_compound_key_chunk_uri(self) -> None:
        node = {
            "eid": "3",
            "labels": ["Chunk"],
            "props": {"chunk_index": 4, "source_doc": "guide.pdf"},
        }
        g = Graph()
        uri = owl_mapper.node_to_rdf(node, g)
        assert uri == owl_mapper.SM["chunk/4/guide.pdf"]

    def test_embedding_dropped_by_default(self) -> None:
        node = {
            "eid": "4",
            "labels": ["BusinessConcept"],
            "props": {"name": "X", "embedding": [0.1, 0.2]},
        }
        g = Graph()
        owl_mapper.node_to_rdf(node, g)
        assert (None, owl_mapper.SM.embedding, None) not in g

    def test_embedding_kept_when_flag_set(self) -> None:
        node = {
            "eid": "4",
            "labels": ["BusinessConcept"],
            "props": {"name": "X", "embedding": [0.1, 0.2]},
        }
        g = Graph()
        owl_mapper.node_to_rdf(node, g, include_embeddings=True)
        assert (None, owl_mapper.SM["embedding"], None) in g

    def test_unknown_label_returns_none(self) -> None:
        node = {"eid": "5", "labels": ["Mystery"], "props": {"name": "X"}}
        g = Graph()
        assert owl_mapper.node_to_rdf(node, g) is None

    def test_missing_key_returns_none(self) -> None:
        node = {"eid": "6", "labels": ["BusinessConcept"], "props": {}}
        g = Graph()
        assert owl_mapper.node_to_rdf(node, g) is None
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `.venv/bin/python -m pytest tests/unit/test_owl_mapper.py -q`
Expected: FAIL — `ModuleNotFoundError: No module named 'src.graph.owl_mapper'`

- [ ] **Step 3: Implement the mapper (node part)**

Create `src/graph/owl_mapper.py`:

```python
"""Neo4j node/edge dicts ↔ RDF/OWL 2 DL triples.

Pure mapping layer — no Neo4j access, no filesystem I/O. Operates on the same
node/edge dict format produced by ``src.graph.kg_registry._export_graph()`` so
the exporter/importer can share it.

Design:
- Each node → an ``sm:`` URI derived from its business-identity key, typed as an
  ``sm:Concept``/``sm:PhysicalTable``/… class (subclass of owl:Thing).
- Well-known props use a standard vocab predicate (skos:definition, …) for
  tool interoperability; every other prop is emitted losslessly under the
  ``sm:`` namespace so round-trip restore is exact (modulo embeddings).
- Embedding vectors are dropped by default (mirror kg_registry); they are
  regenerated on query and would bloat the OWL file.
"""

from __future__ import annotations

import urllib.parse
from typing import Any

from rdflib import BNode, Graph, Literal, Namespace, URIRef
from rdflib.namespace import RDF, RDFS, SKOS

SM = Namespace("http://semanticmesh/graph/v1#")

# Neo4j label → (uri-segment, rdf-class, key-prop-or-tuple-of-props)
_LABEL_SCHEME: dict[str, tuple[str, URIRef, str | tuple[str, ...]]] = {
    "BusinessConcept": ("concept", SM.Concept, "name"),
    "PhysicalTable": ("table", SM.PhysicalTable, "table_name"),
    "Attribute": ("attr", SM.Attribute, "name"),
    "Chunk": ("chunk", SM.Chunk, ("chunk_index", "source_doc")),
    "ParentChunk": ("pchunk", SM.ParentChunk, ("parent_chunk_index", "source_doc")),
    "SourceFile": ("file", SM.SourceFile, "path"),
}

# Well-known props → standard-vocab predicates (literal-valued).
_SEMANTIC_PROPS: dict[str, URIRef] = {
    "definition": SKOS.definition,
    "synonyms": SKOS.altLabel,
    "comment": RDFS.comment,
}


def _quote(value: Any) -> str:
    return urllib.parse.quote(str(value), safe="")


def node_uri(label: str, props: dict[str, Any]) -> URIRef | None:
    """Return the stable ``sm:`` URI for a node, or None if not mappable."""
    scheme = _LABEL_SCHEME.get(label)
    if scheme is None:
        return None
    segment, _rdf_class, key = scheme
    if isinstance(key, tuple):
        parts = [props.get(k) for k in key]
        if any(p in (None, "") for p in parts):
            return None
        local = "/".join(_quote(p) for p in parts)
    else:
        val = props.get(key)
        if val in (None, ""):
            return None
        local = _quote(val)
    return SM[f"{segment}/{local}"]


def node_to_rdf(
    node: dict[str, Any],
    graph: Graph,
    *,
    include_embeddings: bool = False,
) -> URIRef | None:
    """Map a node dict to RDF triples in ``graph``. Return its URI, or None to skip."""
    labels: list[str] = list(node.get("labels", []))
    props: dict[str, Any] = dict(node.get("props", {}) or {})
    label = next((l for l in labels if l in _LABEL_SCHEME), None)
    if label is None:
        return None
    uri = node_uri(label, props)
    if uri is None:
        return None
    _, rdf_class, key = _LABEL_SCHEME[label]
    graph.add((uri, RDF.type, rdf_class))
    key_prop = key[0] if isinstance(key, tuple) else key
    if props.get(key_prop) is not None:
        graph.add((uri, RDFS.label, Literal(str(props[key_prop]))))
    for pname, pval in props.items():
        if pval is None or pname == key_prop:
            continue
        if pname == "embedding" and not include_embeddings:
            continue
        pred = _SEMANTIC_PROPS.get(pname, SM[pname])
        values = pval if isinstance(pval, list) else [pval]
        for v in values:
            graph.add((uri, pred, Literal(v)))
    return uri
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `.venv/bin/python -m pytest tests/unit/test_owl_mapper.py -q`
Expected: PASS (7 tests)

- [ ] **Step 5: Commit**

```bash
git add src/graph/owl_mapper.py tests/unit/test_owl_mapper.py
git commit -m "feat(owl): add node→RDF mapping in owl_mapper"
```

---

## Task 2: OWL Mapper — Edge → RDF

**Files:**
- Modify: `src/graph/owl_mapper.py`
- Test: `tests/unit/test_owl_mapper.py`

- [ ] **Step 1: Add failing tests** (append to `tests/unit/test_owl_mapper.py`)

```python
class TestEdgeToRdf:
    def test_known_edge_emits_predicate(self) -> None:
        eid_to_uri = {
            "1": owl_mapper.SM["concept/Customer"],
            "2": owl_mapper.SM["table/TB_CST"],
        }
        edge = {
            "eid": "r1",
            "start_eid": "1",
            "end_eid": "2",
            "rel_type": "MAPPED_TO",
            "props": {"confidence": 0.9},
        }
        g = Graph()
        ok = owl_mapper.edge_to_rdf(edge, g, eid_to_uri)
        assert ok is True
        assert (
            owl_mapper.SM["concept/Customer"],
            owl_mapper.SM.MAPPED_TO,
            owl_mapper.SM["table/TB_CST"],
        ) in g

    def test_unknown_rel_type_skipped(self) -> None:
        eid_to_uri = {"1": owl_mapper.SM["concept/A"], "2": owl_mapper.SM["table/B"]}
        edge = {"start_eid": "1", "end_eid": "2", "rel_type": "WEIRD", "props": {}}
        g = Graph()
        assert owl_mapper.edge_to_rdf(edge, g, eid_to_uri) is False
        assert len(g) == 0

    def test_missing_endpoint_skipped(self) -> None:
        eid_to_uri = {"1": owl_mapper.SM["concept/A"]}  # endpoint 2 unknown
        edge = {"start_eid": "1", "end_eid": "2", "rel_type": "MAPPED_TO", "props": {}}
        g = Graph()
        assert owl_mapper.edge_to_rdf(edge, g, eid_to_uri) is False

    def test_edge_props_attached_as_reification(self) -> None:
        eid_to_uri = {"1": owl_mapper.SM["concept/A"], "2": owl_mapper.SM["table/B"]}
        edge = {
            "start_eid": "1",
            "end_eid": "2",
            "rel_type": "MAPPED_TO",
            "props": {"confidence": 0.9},
        }
        g = Graph()
        owl_mapper.edge_to_rdf(edge, g, eid_to_uri)
        # confidence lives on the reified statement
        assert (None, owl_mapper.SM["confidence"], Literal(0.9)) in g
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `.venv/bin/python -m pytest tests/unit/test_owl_mapper.py::TestEdgeToRdf -q`
Expected: FAIL — `AttributeError: module ... has no attribute 'edge_to_rdf'`

- [ ] **Step 3: Implement edge mapping** (append to `src/graph/owl_mapper.py`)

```python
# Known relationship types → sm: object properties.
_REL_TYPES: frozenset[str] = frozenset(
    {
        "MAPPED_TO",
        "HAS_ATTRIBUTE",
        "REFERENCES",
        "MENTIONS",
        "DESCRIBED_BY",
        "PART_OF",
        "INSTANCE_OF",
        "CONTAINS_CHUNK",
        "CHILD_OF",
    }
)


def edge_to_rdf(
    edge: dict[str, Any],
    graph: Graph,
    eid_to_uri: dict[str, URIRef],
) -> bool:
    """Map an edge dict to an RDF triple (reified for props). Return False if skipped."""
    rel_type = edge.get("rel_type")
    if rel_type not in _REL_TYPES:
        return False
    src = eid_to_uri.get(edge.get("start_eid", ""))
    tgt = eid_to_uri.get(edge.get("end_eid", ""))
    if src is None or tgt is None:
        return False
    pred = SM[rel_type]
    graph.add((src, pred, tgt))
    # Attach edge properties via OWL reification so round-trip is lossless.
    props = edge.get("props", {}) or {}
    if props:
        stmt = BNode()
        graph.add((stmt, RDF.type, SM.Statement))
        graph.add((stmt, RDF.subject, src))
        graph.add((stmt, RDF.predicate, pred))
        graph.add((stmt, RDF.object, tgt))
        for pname, pval in props.items():
            if pval is None:
                continue
            values = pval if isinstance(pval, list) else [pval]
            for v in values:
                graph.add((stmt, SM[pname], Literal(v)))
    return True
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `.venv/bin/python -m pytest tests/unit/test_owl_mapper.py -q`
Expected: PASS (11 tests)

- [ ] **Step 5: Commit**

```bash
git add src/graph/owl_mapper.py tests/unit/test_owl_mapper.py
git commit -m "feat(owl): add edge→RDF mapping with reified properties"
```

---

## Task 3: OWL Mapper — Round-Trip Serialization + Parse

**Files:**
- Modify: `src/graph/owl_mapper.py`
- Test: `tests/unit/test_owl_mapper.py`

- [ ] **Step 1: Add failing tests** (append to `tests/unit/test_owl_mapper.py`)

```python
class TestRoundTrip:
    def test_serialize_and_parse_roundtrips_nodes(self) -> None:
        nodes = [
            {
                "eid": "1",
                "labels": ["BusinessConcept"],
                "props": {"name": "Customer", "definition": "A buyer", "synonyms": ["Client"]},
            },
            {
                "eid": "2",
                "labels": ["PhysicalTable"],
                "props": {"table_name": "TB_CST", "ddl_source": "CREATE TABLE TB_CST (id INT)"},
            },
        ]
        edges: list[dict] = []
        text = owl_mapper.to_owl_xml(nodes, edges)
        out_nodes, out_edges = owl_mapper.from_owl_xml(text)
        # identity preserved
        out_keys = {(tuple(n["labels"]),) + tuple(sorted(n["props"].items())) for n in out_nodes}
        assert len(out_nodes) == 2
        names = {n["props"].get("name") or n["props"].get("table_name") for n in out_nodes}
        assert names == {"Customer", "TB_CST"}

    def test_roundtrip_preserves_definition_and_synonyms(self) -> None:
        nodes = [
            {
                "eid": "1",
                "labels": ["BusinessConcept"],
                "props": {"name": "Order", "definition": "A purchase", "synonyms": ["Purchase", "Sale"]},
            }
        ]
        text = owl_mapper.to_owl_xml(nodes, edges=[])
        out_nodes, _ = owl_mapper.from_owl_xml(text)
        bc = [n for n in out_nodes if "BusinessConcept" in n["labels"]][0]
        assert bc["props"]["definition"] == "A purchase"
        assert set(bc["props"]["synonyms"]) == {"Purchase", "Sale"}

    def test_roundtrip_edges_with_props(self) -> None:
        nodes = [
            {"eid": "1", "labels": ["BusinessConcept"], "props": {"name": "Customer"}},
            {"eid": "2", "labels": ["PhysicalTable"], "props": {"table_name": "TB_CST"}},
        ]
        edges = [
            {"eid": "r1", "start_eid": "1", "end_eid": "2", "rel_type": "MAPPED_TO",
             "props": {"confidence": 0.9}},
        ]
        text = owl_mapper.to_owl_xml(nodes, edges)
        out_nodes, out_edges = owl_mapper.from_owl_xml(text)
        assert len(out_edges) == 1
        e = out_edges[0]
        assert e["rel_type"] == "MAPPED_TO"
        assert e["props"]["confidence"] == 0.9
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `.venv/bin/python -m pytest tests/unit/test_owl_mapper.py::TestRoundTrip -q`
Expected: FAIL — `AttributeError: ... has no attribute 'to_owl_xml'`

- [ ] **Step 3: Implement serialization + parse** (append to `src/graph/owl_mapper.py`)

```python
# Reverse of _LABEL_SCHEME: uri-segment → (label, key-prop-or-tuple).
_SEGMENT_TO_LABEL: dict[str, tuple[str, str | tuple[str, ...]]] = {
    seg: (label, scheme[2]) for label, scheme in _LABEL_SCHEME.items() for seg in [scheme[0]]
}

# Reverse of _SEMANTIC_PROPS: predicate local-name → prop name.
_PRED_TO_PROP: dict[str, str] = {
    "definition": "definition",
    "altLabel": "synonyms",
    "comment": "comment",
}


def _bind_namespaces(graph: Graph) -> None:
    graph.bind("sm", SM)
    graph.bind("skos", SKOS)
    graph.bind("rdfs", RDFS)


def build_graph(
    nodes: list[dict],
    edges: list[dict],
    *,
    include_embeddings: bool = False,
) -> tuple[Graph, dict[str, URIRef]]:
    """Map all nodes+edges into a fresh Graph. Return (graph, eid→uri)."""
    graph = Graph()
    _bind_namespaces(graph)
    eid_to_uri: dict[str, URIRef] = {}
    for node in nodes:
        uri = node_to_rdf(node, graph, include_embeddings=include_embeddings)
        if uri is not None:
            eid_to_uri[node.get("eid", "")] = uri
    for edge in edges:
        edge_to_rdf(edge, graph, eid_to_uri)
    return graph, eid_to_uri


def to_owl_xml(
    nodes: list[dict],
    edges: list[dict],
    *,
    include_embeddings: bool = False,
) -> str:
    """Serialize node/edge dicts to an OWL/RDF XML string."""
    graph, _ = build_graph(nodes, edges, include_embeddings=include_embeddings)
    return graph.serialize(format="xml")


def _parse_node_uri(uri: URIRef) -> tuple[str, dict[str, Any]] | None:
    """Inverse of node_uri: sm URI → (label, key-props). Return None if not a node URI."""
    if not str(uri).startswith(str(SM)):
        return None
    local = str(uri)[len(str(SM)) :]
    if "/" not in local:
        return None
    segment, _, rest = local.partition("/")
    entry = _SEGMENT_TO_LABEL.get(segment)
    if entry is None:
        return None
    label, key = entry
    decoded = [urllib.parse.unquote(p) for p in rest.split("/")]
    if isinstance(key, tuple):
        # coerce numeric index keys back to int
        props: dict[str, Any] = {}
        for kname, raw in zip(key, decoded):
            props[kname] = int(raw) if kname.endswith("_index") else raw
        return label, props
    props = {key: decoded[0]}
    return label, props


def from_owl_xml(text: str) -> tuple[list[dict], list[dict]]:
    """Parse an OWL/RDF XML string back into (nodes, edges) dicts.

    Reverses to_owl_xml. Node props come from typed literals; edge props come
    from reified sm:Statement blank nodes.
    """
    graph = Graph()
    graph.parse(data=text, format="xml")

    # Collect reified statements (edge props) first.
    reified: dict[tuple[URIRef, URIRef, Any], dict[str, Any]] = {}
    plain_edges: set[tuple[URIRef, URIRef, Any]] = set()
    for stmt in graph.subjects(RDF.type, SM.Statement):
        s = graph.value(stmt, RDF.subject)
        p = graph.value(stmt, RDF.predicate)
        o = graph.value(stmt, RDF.object)
        if s is None or p is None or o is None:
            continue
        key = (s, p, o)
        props: dict[str, Any] = {}
        for pred in graph.predicates(stmt):
            if pred in (RDF.type, RDF.subject, RDF.predicate, RDF.object):
                continue
            pname = str(pred)[len(str(SM)) :]
            vals = [lit.toPython() for lit in graph.objects(stmt, pred)]
            props[pname] = vals[0] if len(vals) == 1 else vals
        reified[key] = props
        plain_edges.add(key)

    # Nodes: group all typed-literal/uri triples by subject.
    node_props: dict[URIRef, dict[str, Any]] = {}
    node_labels: dict[URIRef, list[str]] = {}
    for s, p, o in graph:
        parsed = _parse_node_uri(s)
        if parsed is None:
            continue
        label, key_props = parsed
        node_labels.setdefault(s, [])
        if label not in node_labels[s]:
            node_labels[s].append(label)
        props = node_props.setdefault(s, {})
        props.update(key_props)
        local = _local_name(p)
        if p == RDF.type or p == RDFS.label:
            continue
        prop_name = _PRED_TO_PROP.get(local)
        if prop_name is None:
            if not str(p).startswith(str(SM)):
                continue
            prop_name = local
        if isinstance(o, Literal):
            val = o.toPython()
            if prop_name == "synonyms":
                props.setdefault(prop_name, []).append(val)
            else:
                props[prop_name] = val

    nodes = []
    uri_to_eid: dict[URIRef, str] = {}
    for i, (uri, labels) in enumerate(node_labels.items()):
        eid = str(i)
        uri_to_eid[uri] = eid
        nodes.append({"eid": eid, "labels": labels, "props": node_props.get(uri, {})})

    # Edges: every sm:-predicate triple that is not reified-only.
    rel_segments = {scheme[0] for scheme in _LABEL_SCHEME.values()}
    edges: list[dict] = []
    seen: set[tuple[URIRef, URIRef, Any]] = set()
    for s, p, o in graph:
        if not str(p).startswith(str(SM)):
            continue
        rel_type = str(p)[len(str(SM)) :]
        if rel_type in ("Statement",) or rel_type in rel_segments:
            continue
        if rel_type not in _REL_TYPES:
            continue
        key = (s, p, o)
        if key in seen:
            continue
        seen.add(key)
        edges.append(
            {
                "eid": f"r{len(edges)}",
                "start_eid": uri_to_eid.get(s, ""),
                "end_eid": uri_to_eid.get(o, ""),
                "rel_type": rel_type,
                "props": reified.get(key, {}),
            }
        )
    return nodes, edges


def _local_name(uri: Any) -> str:
    """Return the local name of a URI/namespace term (after the last # or /)."""
    text = str(uri)
    return text.rsplit("#", 1)[-1].rsplit("/", 1)[-1]
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `.venv/bin/python -m pytest tests/unit/test_owl_mapper.py -q`
Expected: PASS (14 tests)

- [ ] **Step 5: Commit**

```bash
git add src/graph/owl_mapper.py tests/unit/test_owl_mapper.py
git commit -m "feat(owl): add lossless OWL XML round-trip serialize/parse"
```

---

## Task 4: OWL Exporter — 4-File Split + Metadata

**Files:**
- Create: `src/graph/owl_exporter.py`
- Test: `tests/unit/test_owl_exporter.py`

- [ ] **Step 1: Write the failing tests**

Create `tests/unit/test_owl_exporter.py`:

```python
"""Unit tests for src.graph.owl_exporter — Neo4j mocked."""

from __future__ import annotations

import json
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from src.graph import owl_exporter


@pytest.fixture(autouse=True)
def _isolate_export_dir(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setattr(owl_exporter, "_EXPORT_DIR", tmp_path / "owl_exports")
    yield


def _fake_graph_dump():
    """Mirror kg_registry._export_graph() output without Neo4j."""
    nodes = [
        {"eid": "1", "labels": ["BusinessConcept"],
         "props": {"name": "Customer", "definition": "A buyer"}},
        {"eid": "2", "labels": ["PhysicalTable"],
         "props": {"table_name": "TB_CST", "ddl_source": "CREATE TABLE..."}},
    ]
    edges = [
        {"eid": "r1", "start_eid": "1", "end_eid": "2",
         "rel_type": "MAPPED_TO", "props": {"confidence": 0.9}},
    ]
    return nodes, edges


class TestExportToOwlFiles:
    def test_writes_four_owl_files_plus_metadata(self, tmp_path: Path) -> None:
        with patch.object(owl_exporter, "_dump_graph", return_value=_fake_graph_dump()):
            meta = owl_exporter.export_to_owl_files(include_embeddings=False)
        out_dir = tmp_path / "owl_exports" / meta["export_id"]
        assert (out_dir / "entities.owl").exists()
        assert (out_dir / "tables.owl").exists()
        assert (out_dir / "mappings.owl").exists()
        assert (out_dir / "technical.owl").exists()
        assert (out_dir / "metadata.json").exists()

    def test_metadata_records_counts_and_checksums(self) -> None:
        with patch.object(owl_exporter, "_dump_graph", return_value=_fake_graph_dump()):
            meta = owl_exporter.export_to_owl_files()
        assert meta["nodes_count"] == 2
        assert meta["relationships_count"] == 1
        assert set(meta["checksums"]) == {"entities.owl", "tables.owl", "mappings.owl", "technical.owl"}
        # checksum is a 64-char hex sha256
        assert all(len(h) == 64 for h in meta["checksums"].values())

    def test_metadata_json_round_trips(self, tmp_path: Path) -> None:
        with patch.object(owl_exporter, "_dump_graph", return_value=_fake_graph_dump()):
            meta = owl_exporter.export_to_owl_files()
        out_dir = tmp_path / "owl_exports" / meta["export_id"]
        loaded = json.loads((out_dir / "metadata.json").read_text())
        assert loaded["export_id"] == meta["export_id"]
        assert loaded["nodes_count"] == 2

    def test_empty_graph_raises(self) -> None:
        with patch.object(owl_exporter, "_dump_graph", return_value=([], [])):
            with pytest.raises(ValueError, match="no_data_to_export"):
                owl_exporter.export_to_owl_files()
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `.venv/bin/python -m pytest tests/unit/test_owl_exporter.py -q`
Expected: FAIL — `ModuleNotFoundError: ... owl_exporter`

- [ ] **Step 3: Implement the exporter**

Create `src/graph/owl_exporter.py`:

```python
"""Export the live Neo4j Knowledge Graph to split OWL 2 DL files.

Pipeline: ``kg_registry._export_graph()`` → node/edge dicts → ``owl_mapper``
→ 4 partitioned ``.owl`` files + a ``metadata.json`` with SHA-256 checksums.

File split (for tool-friendliness and partial import):
  entities.owl  — BusinessConcept nodes
  tables.owl    — PhysicalTable + Attribute nodes
  mappings.owl  — MAPPED_TO / REFERENCES / HAS_ATTRIBUTE edges (+ touched nodes)
  technical.owl — Chunk / ParentChunk / SourceFile nodes + remaining edges
"""

from __future__ import annotations

import hashlib
import json
from datetime import datetime
from pathlib import Path
from typing import Any

from src.config.logging import get_logger
from src.graph.owl_mapper import build_graph

logger = get_logger(__name__)

_EXPORT_DIR = Path(__file__).parent.parent.parent / "data" / "memory" / "owl_exports"

_PARTITION_LABELS: dict[str, set[str]] = {
    "entities.owl": {"BusinessConcept"},
    "tables.owl": {"PhysicalTable", "Attribute"},
    "technical.owl": {"Chunk", "ParentChunk", "SourceFile"},
}
# Edge partition by rel_type; mappings.owl gets the schema edges.
_PARTITION_RELS: dict[str, set[str]] = {
    "mappings.owl": {"MAPPED_TO", "REFERENCES", "HAS_ATTRIBUTE"},
}


def _dump_graph(*, include_embeddings: bool = False) -> tuple[list[dict], list[dict]]:
    """Return (nodes, edges) dicts from Neo4j. Thin wrapper over kg_registry."""
    from src.graph.kg_registry import _export_graph

    nodes, edges = _export_graph()
    if not include_embeddings:
        for n in nodes:
            n["props"].pop("embedding", None)
    return nodes, edges


def _partition_nodes(nodes: list[dict]) -> dict[str, list[dict]]:
    buckets: dict[str, list[dict]] = {f: [] for f in (*_PARTITION_LABELS, "mappings.owl")}
    for node in nodes:
        labels = set(node.get("labels", []))
        placed = False
        for fname, lbls in _PARTITION_LABELS.items():
            if labels & lbls:
                buckets[fname].append(node)
                placed = True
                break
        if not placed:
            buckets["technical.owl"].append(node)  # catch-all
    return buckets


def _partition_edges(
    edges: list[dict],
    nodes: list[dict],
) -> tuple[dict[str, list[dict]], dict[str, list[dict]]]:
    """Partition edges, and gather the nodes each edge touches for its file."""
    eid_to_node = {n["eid"]: n for n in nodes}
    edge_buckets: dict[str, list[dict]] = {f: [] for f in _PARTITION_RELS}
    node_buckets: dict[str, list[dict]] = {f: [] for f in _PARTITION_RELS}
    for edge in edges:
        rel = edge.get("rel_type")
        for fname, rels in _PARTITION_RELS.items():
            if rel in rels:
                edge_buckets[fname].append(edge)
                for eid in (edge.get("start_eid"), edge.get("end_eid")):
                    n = eid_to_node.get(eid)
                    if n and n not in node_buckets[fname]:
                        node_buckets[fname].append(n)
                break
        else:
            edge_buckets.setdefault("technical.owl", []).append(edge)
    return edge_buckets, node_buckets


def _sha256(path: Path) -> str:
    h = hashlib.sha256()
    h.update(path.read_bytes())
    return h.hexdigest()


def export_to_owl_files(
    *,
    include_embeddings: bool = False,
) -> dict[str, Any]:
    """Export the live graph to 4 OWL files + metadata.json. Return metadata dict."""
    nodes, edges = _dump_graph(include_embeddings=include_embeddings)
    if not nodes and not edges:
        raise ValueError("no_data_to_export: the Knowledge Graph is empty")

    export_id = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    out_dir = _EXPORT_DIR / export_id
    out_dir.mkdir(parents=True, exist_ok=True)

    node_buckets = _partition_nodes(nodes)
    edge_buckets, edge_node_buckets = _partition_edges(edges, nodes)

    checksums: dict[str, str] = {}
    for fname in ("entities.owl", "tables.owl", "mappings.owl", "technical.owl"):
        part_nodes = node_buckets.get(fname, [])
        if fname in edge_node_buckets:
            # mappings.owl: include touched nodes so the file is self-contained.
            existing_eids = {n["eid"] for n in part_nodes}
            for n in edge_node_buckets[fname]:
                if n["eid"] not in existing_eids:
                    part_nodes.append(n)
                    existing_eids.add(n["eid"])
        part_edges = edge_buckets.get(fname, [])
        graph, _ = build_graph(part_nodes, part_edges, include_embeddings=include_embeddings)
        text = graph.serialize(format="xml")
        path = out_dir / fname
        path.write_text(text, encoding="utf-8")
        checksums[fname] = _sha256(path)

    metadata = {
        "export_id": export_id,
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "files": list(checksums),
        "checksums": checksums,
        "nodes_count": len(nodes),
        "relationships_count": len(edges),
        "include_embeddings": include_embeddings,
    }
    (out_dir / "metadata.json").write_text(json.dumps(metadata, indent=2), encoding="utf-8")
    logger.info("OWL export %s: %d nodes, %d edges → %s", export_id, len(nodes), len(edges), out_dir)
    return metadata


def export_dir(export_id: str) -> Path:
    """Return the directory path for a given export id (for download)."""
    return _EXPORT_DIR / export_id


def list_exports() -> list[dict[str, Any]]:
    """List all exports on disk (metadata only), newest first."""
    if not _EXPORT_DIR.exists():
        return []
    out: list[dict[str, Any]] = []
    for child in sorted(_EXPORT_DIR.iterdir(), reverse=True):
        meta_path = child / "metadata.json"
        if meta_path.exists():
            out.append(json.loads(meta_path.read_text()))
    return out
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `.venv/bin/python -m pytest tests/unit/test_owl_exporter.py -q`
Expected: PASS (4 tests)

- [ ] **Step 5: Commit**

```bash
git add src/graph/owl_exporter.py tests/unit/test_owl_exporter.py
git commit -m "feat(owl): add split-file exporter with metadata + checksums"
```

---

## Task 5: OWL Importer — Clean / Versioned / Merge Strategies

**Files:**
- Create: `src/graph/owl_importer.py`
- Test: `tests/unit/test_owl_importer.py`

- [ ] **Step 1: Write the failing tests**

Create `tests/unit/test_owl_importer.py`:

```python
"""Unit tests for src.graph.owl_importer — Neo4j mocked."""

from __future__ import annotations

from unittest.mock import MagicMock, patch

import pytest

from src.graph import owl_importer
from src.graph.owl_mapper import to_owl_xml


def _owl_text():
    nodes = [
        {"eid": "1", "labels": ["BusinessConcept"], "props": {"name": "Customer"}},
        {"eid": "2", "labels": ["PhysicalTable"], "props": {"table_name": "TB_CST"}},
    ]
    edges = [
        {"eid": "r1", "start_eid": "1", "end_eid": "2",
         "rel_type": "MAPPED_TO", "props": {"confidence": 0.9}},
    ]
    return to_owl_xml(nodes, edges)


class TestImportFromOwlText:
    def test_clean_strategy_clears_then_writes(self) -> None:
        client = MagicMock()
        with patch.object(owl_importer, "Neo4jClient") as N, \
             patch.object(owl_importer, "setup_schema") as setup:
            N.return_value.__enter__.return_value = client
            result = owl_importer.import_from_owl_text(_owl_text(), strategy="clean")
        # DELETE must run before any write
        calls = [c.args[0] for c in client.execute_cypher.call_args_list]
        assert any("DETACH DELETE" in c for c in calls)
        assert client.execute_batch.called
        assert result["nodes_merged"] == 2
        assert result["relationships_merged"] == 1

    def test_merge_strategy_does_not_clear(self) -> None:
        client = MagicMock()
        with patch.object(owl_importer, "Neo4jClient") as N, \
             patch.object(owl_importer, "setup_schema"):
            N.return_value.__enter__.return_value = client
            owl_importer.import_from_owl_text(_owl_text(), strategy="merge")
        calls = [c.args[0] for c in client.execute_cypher.call_args_list]
        assert not any("DETACH DELETE" in c for c in calls)

    def test_versioned_strategy_snapshots_first(self) -> None:
        # save_snapshot is late-imported from kg_registry inside import_from_owl_text,
        # so patch it at its source module.
        client = MagicMock()
        with patch.object(owl_importer, "Neo4jClient") as N, \
             patch.object(owl_importer, "setup_schema"), \
             patch("src.graph.kg_registry.save_snapshot",
                   return_value={"id": "snap-backup-1"}) as save:
            N.return_value.__enter__.return_value = client
            result = owl_importer.import_from_owl_text(_owl_text(), strategy="versioned")
        save.assert_called_once()
        assert result["backup_snapshot_id"] is not None
        # and it still cleared + wrote
        calls = [c.args[0] for c in client.execute_cypher.call_args_list]
        assert any("DETACH DELETE" in c for c in calls)

    def test_invalid_strategy_raises(self) -> None:
        with pytest.raises(ValueError, match="unsupported_strategy"):
            owl_importer.import_from_owl_text(_owl_text(), strategy="bogus")
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `.venv/bin/python -m pytest tests/unit/test_owl_importer.py -q`
Expected: FAIL — `ModuleNotFoundError: ... owl_importer`

- [ ] **Step 3: Implement the importer**

Create `src/graph/owl_importer.py`:

```python
"""Import OWL 2 DL files/text into the Neo4j Knowledge Graph.

Strategies:
  clean     — clear graph, then MERGE all nodes+edges (like kg_registry load).
  versioned — snapshot the live graph first (rollback backup via kg_registry),
              then clear + MERGE.
  merge     — MERGE only, no clear (incremental; MERGE is idempotent).

Note: Neo4j Community (Docker neo4j:5) has no named-graph/fabric support, so a
true "versioned graph" is impossible. The rollback safety the user wants is
delivered by an auto-snapshot instead — same external contract.
"""

from __future__ import annotations

from datetime import datetime
from typing import Any, Literal

from src.config.logging import get_logger
from src.graph.neo4j_client import Neo4jClient, setup_schema
from src.graph.owl_mapper import from_owl_xml

logger = get_logger(__name__)

Strategy = Literal["clean", "versioned", "merge"]

_ALLOWED_RELS = frozenset(
    {"MAPPED_TO", "HAS_ATTRIBUTE", "REFERENCES", "MENTIONS", "DESCRIBED_BY",
     "PART_OF", "INSTANCE_OF", "CONTAINS_CHUNK", "CHILD_OF"}
)

# ponytail: the node/edge → MERGE builders below mirror kg_registry._import_graph.
# A future refactor could extract a shared graph_merge() into kg_registry; left
# duplicated here to avoid coupling OWL import to kg_registry internals and to
# not disturb the 530 passing tests.


def _node_identity(node: dict) -> tuple[str, dict] | None:
    """Return (cypher_match_fragment, params) for MERGE, or None to skip."""
    labels = node.get("labels", [])
    props = node.get("props", {})
    if "BusinessConcept" in labels and props.get("name"):
        return "(n:BusinessConcept {name: $key})", {"key": props["name"]}
    if "PhysicalTable" in labels and props.get("table_name"):
        return "(n:PhysicalTable {table_name: $key})", {"key": props["table_name"]}
    if "Attribute" in labels and props.get("name"):
        return "(n:Attribute {name: $key})", {"key": props["name"]}
    if "Chunk" in labels and props.get("chunk_index") is not None:
        return ("(n:Chunk {chunk_index: $idx, source_doc: $src})",
                {"idx": props["chunk_index"], "src": props.get("source_doc", "")})
    if "ParentChunk" in labels and props.get("parent_chunk_index") is not None:
        return ("(n:ParentChunk {parent_chunk_index: $idx, source_doc: $src})",
                {"idx": props["parent_chunk_index"], "src": props.get("source_doc", "")})
    if "SourceFile" in labels and props.get("path"):
        return "(n:SourceFile {path: $key})", {"key": props["path"]}
    return None


def _node_label(node: dict) -> str | None:
    labels = node.get("labels", [])
    for primary in ("BusinessConcept", "PhysicalTable", "Attribute",
                    "ParentChunk", "Chunk", "SourceFile"):
        if primary in labels:
            return primary
    return None


def _build_node_statements(nodes: list[dict]) -> list[tuple[str, dict]]:
    stmts: list[tuple[str, dict]] = []
    for node in nodes:
        ident = _node_identity(node)
        if ident is None:
            continue
        match_frag, ident_params = ident
        props = {k: v for k, v in node["props"].items()
                 if k not in ident_params and k != "embedding"}
        stmts.append((f"MERGE {match_frag} SET n += $props",
                      {**ident_params, "props": props}))
    return stmts


def _merge_graph(
    client: Neo4jClient,
    nodes: list[dict],
    edges: list[dict],
    *,
    clear: bool,
) -> tuple[int, int]:
    """Write nodes+edges via MERGE. Returns (nodes_merged, rels_merged)."""
    if clear:
        client.execute_cypher("MATCH (n) DETACH DELETE n")
        setup_schema(client)

    node_stmts = _build_node_statements(nodes)
    for i in range(0, len(node_stmts), 200):
        client.execute_batch(node_stmts[i: i + 200])

    # eid → identity match fragment for relationship wiring
    eid_identity: dict[str, tuple[str, dict]] = {}
    for node in nodes:
        ident = _node_identity(node)
        if ident:
            eid_identity[node.get("eid", "")] = ident

    rel_stmts: list[tuple[str, dict]] = []
    for edge in edges:
        rel_type = edge.get("rel_type")
        if rel_type not in _ALLOWED_RELS:
            logger.warning("Skipping unknown relationship type '%s' on import.", rel_type)
            continue
        src = eid_identity.get(edge.get("start_eid", ""))
        tgt = eid_identity.get(edge.get("end_eid", ""))
        if not src or not tgt:
            continue
        src_frag, src_p = src
        tgt_frag, tgt_p = tgt
        # rewrite aliases a/b
        src_frag = src_frag.replace("n:", "a:").replace("(n", "(a")
        tgt_frag = tgt_frag.replace("n:", "b:").replace("(n", "(b")
        cypher = (f"MATCH {src_frag} MATCH {tgt_frag} "
                  f"MERGE (a)-[r:`{rel_type}`]->(b) SET r += $props")
        params = {**src_p, **tgt_p, "props": edge.get("props", {})}
        rel_stmts.append((cypher, params))

    for i in range(0, len(rel_stmts), 200):
        client.execute_batch(rel_stmts[i: i + 200])
    return len(node_stmts), len(rel_stmts)


def import_from_owl_text(text: str, strategy: Strategy) -> dict[str, Any]:
    """Parse OWL XML text and import into Neo4j with the given strategy."""
    if strategy not in ("clean", "versioned", "merge"):
        raise ValueError("unsupported_strategy: use one of clean|versioned|merge")

    nodes, edges = from_owl_xml(text)
    backup_id: str | None = None

    if strategy == "versioned":
        from src.graph.kg_registry import save_snapshot
        ts = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
        snap = save_snapshot(name=f"pre-owl-import-{ts}",
                             description="auto-backup before OWL import")
        backup_id = snap["id"]

    with Neo4jClient() as client:
        nodes_merged, rels_merged = _merge_graph(
            client, nodes, edges, clear=(strategy != "merge")
        )

    result: dict[str, Any] = {
        "strategy": strategy,
        "nodes_merged": nodes_merged,
        "relationships_merged": rels_merged,
        "backup_snapshot_id": backup_id,
    }
    logger.info("OWL import (%s): %d nodes, %d rels.", strategy, nodes_merged, rels_merged)
    return result
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `.venv/bin/python -m pytest tests/unit/test_owl_importer.py -q`
Expected: PASS (4 tests)

- [ ] **Step 5: Commit**

```bash
git add src/graph/owl_importer.py tests/unit/test_owl_importer.py
git commit -m "feat(owl): add importer with clean/versioned/merge strategies"
```

---

## Task 6: API Models

**Files:**
- Modify: `src/api/models.py` (append after `RenameSnapshotRequest`, ~line 776)

- [ ] **Step 1: Add models**

Append to `src/api/models.py` (after the `RenameSnapshotRequest` class, before the Conversation section):

```python


# ── OWL export/import models ──────────────────────────────────────────────────


class OwlExportRequest(BaseModel):
    """Request to export the live KG to OWL 2 DL files."""

    model_config = ConfigDict(extra="forbid")

    include_embeddings: bool = Field(
        default=False,
        description="Include BGE-M3 embedding vectors (large; omitted by default).",
    )


class OwlExportMeta(BaseModel):
    """Metadata for an OWL export."""

    export_id: str = Field(description="Timestamp-based export id, e.g. '20260724_143022'.")
    timestamp: str = Field(description="ISO-8601 UTC creation timestamp.")
    files: list[str] = Field(description="OWL file names in this export.")
    checksums: dict[str, str] = Field(description="SHA-256 hex digest per file.")
    nodes_count: int = Field(description="Number of nodes exported.")
    relationships_count: int = Field(description="Number of relationships exported.")
    include_embeddings: bool = Field(default=False)


class OwlImportRequest(BaseModel):
    """Request to import OWL into the KG."""

    model_config = ConfigDict(extra="forbid")

    strategy: Literal["clean", "versioned", "merge"] = Field(
        default="clean",
        description=(
            "'clean' clears and rebuilds; 'versioned' snapshots first then "
            "clear+rebuild; 'merge' MERGEs without clearing."
        ),
    )
    files: list[str] = Field(
        description="OWL file paths or contents to import (union-parsed).",
    )


class OwlImportResult(BaseModel):
    """Result of an OWL import."""

    strategy: str
    nodes_merged: int
    relationships_merged: int
    backup_snapshot_id: str | None = Field(
        default=None,
        description="Set only for strategy='versioned' — the auto-backup snapshot id.",
    )
```

- [ ] **Step 2: Verify models import**

Run: `.venv/bin/python -c "from src.api.models import OwlExportRequest, OwlExportMeta, OwlImportRequest, OwlImportResult; print('ok')"`
Expected: `ok`

- [ ] **Step 3: Commit**

```bash
git add src/api/models.py
git commit -m "feat(owl): add API request/response models"
```

---

## Task 7: API Endpoints

**Files:**
- Modify: `src/api/demo_router.py` (append after the snapshot block, ~line 910)

- [ ] **Step 1: Add endpoints**

Append to `src/api/demo_router.py` (after the last snapshot endpoint):

```python


# ── OWL export/import ─────────────────────────────────────────────────────────


@router.post(
    "/kg/owl/export",
    response_model=OwlExportMeta,
    summary="Export the live KG to OWL 2 DL files",
    description=(
        "Exports the current Neo4j Knowledge Graph to four OWL files "
        "(entities, tables, mappings, technical) plus a metadata.json with "
        "SHA-256 checksums. Returns export metadata; download via "
        "**GET /demo/kg/owl/export/{export_id}**."
    ),
)
def export_owl(req: OwlExportRequest) -> OwlExportMeta:
    try:
        from src.graph.owl_exporter import export_to_owl_files
        meta = export_to_owl_files(include_embeddings=req.include_embeddings)
        return OwlExportMeta(**meta)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc))
    except Exception as exc:  # noqa: BLE001
        raise HTTPException(status_code=503, detail=f"neo4j_unavailable: {exc}")


@router.get(
    "/kg/owl/export/{export_id}",
    summary="Download an OWL export as a tarball",
    description="Streams a .tar.gz of the export directory (4 .owl files + metadata.json).",
)
def download_owl_export(export_id: str):
    import io
    import tarfile

    from fastapi.responses import StreamingResponse

    from src.graph.owl_exporter import export_dir

    try:
        directory = export_dir(export_id)
    except Exception as exc:  # noqa: BLE001
        raise HTTPException(status_code=400, detail=f"invalid_export_id: {exc}")
    if not directory.exists():
        raise HTTPException(status_code=404, detail=f"export '{export_id}' not found")

    def _tar_stream():
        buf = io.BytesIO()
        with tarfile.open(fileobj=buf, mode="w:gz") as tar:
            for path in sorted(directory.iterdir()):
                tar.add(path, arcname=path.name)
        buf.seek(0)
        yield buf.read()

    return StreamingResponse(
        _tar_stream(),
        media_type="application/gzip",
        headers={"Content-Disposition": f'attachment; filename="owl_export_{export_id}.tar.gz"'},
    )


@router.get(
    "/kg/owl/export",
    response_model=list[OwlExportMeta],
    summary="List all OWL exports",
)
def list_owl_exports() -> list[OwlExportMeta]:
    from src.graph.owl_exporter import list_exports
    return [OwlExportMeta(**m) for m in list_exports()]


@router.post(
    "/kg/owl/import",
    response_model=OwlImportResult,
    summary="Import OWL files into the KG",
    description=(
        "Parses the given OWL files (union) and imports them into Neo4j. "
        "strategy: 'clean' | 'versioned' | 'merge'."
    ),
)
def import_owl(req: OwlImportRequest) -> OwlImportResult:
    import pathlib

    from src.graph.owl_importer import import_from_owl_text

    texts: list[str] = []
    for f in req.files:
        p = pathlib.Path(f)
        if p.exists():
            texts.append(p.read_text(encoding="utf-8"))
        else:
            # treat as inline OWL XML content
            texts.append(f)
    if not texts:
        raise HTTPException(status_code=400, detail="no_owl_files_provided")

    try:
        result = import_from_owl_text("\n".join(texts), strategy=req.strategy)
        return OwlImportResult(**result)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))
    except Exception as exc:  # noqa: BLE001
        raise HTTPException(status_code=500, detail=f"import_failed: {exc}")
```

- [ ] **Step 2: Ensure imports resolve**

Add `OwlExportRequest, OwlExportMeta, OwlImportRequest, OwlImportResult` to the existing `from src.api.models import (...)` block at the top of `demo_router.py` (keep alphabetical-ish within the import).

Run: `.venv/bin/python -c "from src.api.demo_router import router; print(len(router.routes))"`
Expected: a number (no ImportError).

- [ ] **Step 3: Commit**

```bash
git add src/api/demo_router.py
git commit -m "feat(owl): add export/import/list/download endpoints"
```

---

## Task 8: Integration Round-Trip Test (Neo4j)

**Files:**
- Create: `tests/integration/test_owl_flow.py`

- [ ] **Step 1: Write the test**

Create `tests/integration/test_owl_flow.py`:

```python
"""Integration test: build a tiny KG, export to OWL, re-import losslessly.

Requires a live Neo4j. Skipped unless run with -m integration.
"""

from __future__ import annotations

import pytest

pytestmark = pytest.mark.integration


@pytest.fixture()
def clean_graph():
    from src.graph.neo4j_client import Neo4jClient
    with Neo4jClient() as client:
        client.execute_cypher("MATCH (n) DETACH DELETE n")
        yield client
        client.execute_cypher("MATCH (n) DETACH DELETE n")


def test_export_then_import_roundtrip(clean_graph) -> None:
    from src.graph.neo4j_client import Neo4jClient, setup_schema

    # Seed: one BusinessConcept + one PhysicalTable + MAPPED_TO edge.
    with Neo4jClient() as client:
        setup_schema(client)
        client.execute_batch([
            ("MERGE (bc:BusinessConcept {name: $name}) "
             "SET bc.definition = $def, bc.synonyms = $syn",
             {"name": "Customer", "def": "A buyer", "syn": ["Client"]}),
            ("MERGE (pt:PhysicalTable {table_name: $tn}) "
             "SET pt.ddl_source = $ddl",
             {"tn": "TB_CST", "ddl": "CREATE TABLE TB_CST (id INT)"}),
            ("MATCH (bc:BusinessConcept {name: 'Customer'}), "
             "(pt:PhysicalTable {table_name: 'TB_CST'}) "
             "MERGE (bc)-[:MAPPED_TO]->(pt)",
             {}),
        ])

    # Export
    from src.graph.owl_exporter import export_to_owl_files, export_dir
    meta = export_to_owl_files()
    assert meta["nodes_count"] >= 2
    assert meta["relationships_count"] >= 1

    # Read exported OWL, wipe graph, re-import clean.
    directory = export_dir(meta["export_id"])
    owl_text = "\n".join(p.read_text() for p in directory.glob("*.owl"))

    from src.graph.owl_importer import import_from_owl_text
    result = import_from_owl_text(owl_text, strategy="clean")
    assert result["nodes_merged"] >= 2
    assert result["relationships_merged"] >= 1

    # Verify restored nodes.
    from src.graph.neo4j_client import Neo4jClient as N
    with N() as client:
        bc = client.execute_cypher(
            "MATCH (bc:BusinessConcept {name: 'Customer'}) RETURN bc.definition AS d"
        )
        assert bc and bc[0]["d"] == "A buyer"
        rel = client.execute_cypher(
            "MATCH (:BusinessConcept {name: 'Customer'})-[:MAPPED_TO]->"
            "(pt:PhysicalTable {table_name: 'TB_CST'}) RETURN count(*) AS c"
        )
        assert rel[0]["c"] == 1
```

- [ ] **Step 2: Register the marker**

Check `pyproject.toml` / `tests/conftest.py` for a `integration` marker. If none exists, add to `pyproject.toml` under `[tool.pytest.ini_options]`:

```toml
markers = [
    "integration: requires a live Neo4j instance",
]
```

- [ ] **Step 3: Run unit suite (must stay green, integration skipped)**

Run: `.venv/bin/python -m pytest tests/unit/ -m "not slow" -q`
Expected: PASS — all previously-passing tests + new OWL unit tests (25 new).

- [ ] **Step 4: Run integration test (requires Neo4j up)**

Run: `.venv/bin/python -m pytest tests/integration/test_owl_flow.py -m integration -q`
Expected: PASS (1 test). If Neo4j is down, start it: `docker start thesis-neo4j` (or `--auto-neo4j` per project convention), then re-run.

- [ ] **Step 5: Commit**

```bash
git add tests/integration/test_owl_flow.py pyproject.toml
git commit -m "test(owl): add Neo4j round-trip integration test"
```

---

## Task 9: User Documentation

**Files:**
- Modify: `README.md` (API Endpoints Summary table)

- [ ] **Step 1: Document endpoints**

In `README.md`, add a row to the **API Endpoints Summary** table:

```markdown
| **OWL** | `POST /demo/kg/owl/export`, `GET /demo/kg/owl/export/{id}`, `POST /demo/kg/owl/import` | Export/import KG as OWL 2 DL (Protégé/Stardog/GraphDB compatible) |
```

- [ ] **Step 2: Add a short usage section**

After the REST API section in `README.md`, add:

```markdown
### OWL Export / Import

Export the live Knowledge Graph to OWL 2 DL for use in Protégé, Stardog, or
GraphDB, or as a backup:

```bash
# Export → returns export_id; download is a .tar.gz of 4 .owl files + metadata.json
curl -X POST -H "X-API-Key: $KEY" -H "Content-Type: application/json" \
  -d '{"include_embeddings": false}' \
  http://localhost:8000/api/v1/demo/kg/owl/export

curl -H "X-API-Key: $KEY" \
  http://localhost:8000/api/v1/demo/kg/owl/export/20260724_143022 -o export.tar.gz

# Import (strategy: clean | versioned | merge)
curl -X POST -H "X-API-Key: $KEY" -H "Content-Type: application/json" \
  -d '{"strategy": "versioned", "files": ["entities.owl", "tables.owl", "mappings.owl"]}' \
  http://localhost:8000/api/v1/demo/kg/owl/import
```
```

- [ ] **Step 3: Commit**

```bash
git add README.md
git commit -m "docs: document OWL export/import API"
```

---

## Final Verification

- [ ] **Full unit suite green**

Run: `.venv/bin/python -m pytest tests/unit/ -m "not slow" -q`
Expected: PASS (530 baseline + 25 new = ~555).

- [ ] **Lint clean**

Run: `.venv/bin/python -m ruff check src/graph/owl_mapper.py src/graph/owl_exporter.py src/graph/owl_importer.py src/api/demo_router.py src/api/models.py`
Expected: no errors.

- [ ] **API smoke (server up)**

Run: `.venv/bin/python -m scripts.serve_api --reload` then in another shell:

```bash
curl -H "X-API-Key: $KEY" http://localhost:8000/api/v1/demo/kg/owl/export
```

Expected: `[]` (no exports yet) or a JSON list.

---

## Notes for the Implementer

- **execute_cypher rejects `;`.** Never concatenate statements with semicolons. Use `execute_batch([(cypher, params), ...])` for multi-writes (transactional).
- **Neo4jClient is a context manager.** Always `with Neo4jClient() as client:`. The driver is a shared singleton — do not close it.
- **`from_owl_xml` parse fidelity:** lists (e.g. `synonyms`) are reconstructed by collecting all `skos:altLabel` literals for a subject. Numeric `*_index` keys are coerced back to `int`. Everything else round-trips as-is.
- **`versioned` is an auto-snapshot, not a Neo4j named graph** (Community Edition limitation). Roll back via `POST /demo/kg/snapshots/{backup_id}/load`.
- **`embedding` dropped by default** on both export and import, matching `kg_registry`. Re-enabled on export only via `include_embeddings=True`; import always ignores embeddings (regenerated on query).
