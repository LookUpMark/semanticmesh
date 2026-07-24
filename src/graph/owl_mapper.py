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
    label = next((lbl for lbl in labels if lbl in _LABEL_SCHEME), None)
    if label is None:
        return None
    uri = node_uri(label, props)
    if uri is None:
        return None
    _, rdf_class, key = _LABEL_SCHEME[label]
    graph.add((uri, RDF.type, rdf_class))
    # Skip ALL identity props — they're encoded in the URI (node_uri), so emitting
    # them again as triples would collide on extraction (compound keys: chunk_index
    # AND source_doc). rdfs:label carries the primary key for human readers.
    key_props_skip = set(key) if isinstance(key, tuple) else {key}
    primary_key = key[0] if isinstance(key, tuple) else key
    if props.get(primary_key) is not None:
        graph.add((uri, RDFS.label, Literal(str(props[primary_key]))))
    for pname, pval in props.items():
        if pval is None or pname in key_props_skip:
            continue
        if pname == "embedding" and not include_embeddings:
            continue
        pred = _SEMANTIC_PROPS.get(pname, SM[pname])
        values = pval if isinstance(pval, list) else [pval]
        for v in values:
            graph.add((uri, pred, Literal(v)))
    return uri


# Known relationship types → sm: object properties.
_REL_TYPES: frozenset[str] = frozenset(
    {
        "MAPPED_TO",
        "HAS_ATTRIBUTE",
        "HAS_COLUMN",
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
    """Map an edge dict to RDF. Return False if skipped.

    Emits the base triple (src, pred, tgt) for graph visualization in tools
    like Protégé, PLUS a distinct reified ``sm:Statement`` per edge. RDF triples
    are unique by (s, p, o), so without per-edge reification two same-type edges
    between the same pair (e.g. two FK columns A→B) would collapse into one.
    The statement carries the edge's own properties and gives each edge a
    distinct identity for lossless round-trip.
    """
    rel_type = edge.get("rel_type")
    if rel_type not in _REL_TYPES:
        return False
    src = eid_to_uri.get(edge.get("start_eid", ""))
    tgt = eid_to_uri.get(edge.get("end_eid", ""))
    if src is None or tgt is None:
        return False
    pred = SM[rel_type]
    graph.add((src, pred, tgt))
    stmt = BNode()
    graph.add((stmt, RDF.type, SM.Statement))
    graph.add((stmt, RDF.subject, src))
    graph.add((stmt, RDF.predicate, pred))
    graph.add((stmt, RDF.object, tgt))
    for pname, pval in (edge.get("props", {}) or {}).items():
        if pval is None:
            continue
        values = pval if isinstance(pval, list) else [pval]
        for v in values:
            graph.add((stmt, SM[pname], Literal(v)))
    return True


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
        for kname, raw in zip(key, decoded, strict=True):
            props[kname] = int(raw) if kname.endswith("_index") else raw
        return label, props
    props = {key: decoded[0]}
    return label, props


def from_owl_xml(text: str) -> tuple[list[dict], list[dict]]:
    """Parse a single OWL/RDF XML document into (nodes, edges) dicts.

    Reverses to_owl_xml. Node props come from typed literals; edge props come
    from reified sm:Statement blank nodes.
    """
    graph = Graph()
    graph.parse(data=text, format="xml")
    return _extract_nodes_edges(graph)


def from_owl_documents(texts: list[str]) -> tuple[list[dict], list[dict]]:
    """Parse several OWL/RDF XML documents into one merged (nodes, edges) result.

    Each export produces multiple files (entities/tables/mappings/technical),
    each a complete XML document. Concatenating their text yields invalid XML,
    so parse each separately and union the triples before extracting. Duplicate
    nodes/edges (a node appears in its own file and again in mappings.owl)
    collapse on the union because they share the same sm: URI.
    """
    merged = Graph()
    for text in texts:
        single = Graph()
        single.parse(data=text, format="xml")
        merged += single
    return _extract_nodes_edges(merged)


def _extract_nodes_edges(graph: Graph) -> tuple[list[dict], list[dict]]:
    """Extract (nodes, edges) dicts from a parsed Graph (single or unioned)."""
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
            # Collect all values for this predicate; collapse to scalar below.
            # Generalizes the old synonyms-only special case — any list-typed
            # prop (current or future) round-trips losslessly.
            props.setdefault(prop_name, []).append(o.toPython())

    # Collapse single-value lists to scalars; keep multi-value as lists.
    # Identity key props (scalars from key_props) are untouched.
    for prop_map in node_props.values():
        for k, v in prop_map.items():
            if isinstance(v, list) and len(v) == 1:
                prop_map[k] = v[0]

    nodes = []
    uri_to_eid: dict[URIRef, str] = {}
    for i, (uri, labels) in enumerate(node_labels.items()):
        eid = str(i)
        uri_to_eid[uri] = eid
        nodes.append({"eid": eid, "labels": labels, "props": node_props.get(uri, {})})

    # Edges: one per reified sm:Statement (preserves props + duplicate-pair edges,
    # which a plain-triple scan could not). Plus a base-triple fallback for OWL
    # produced by external tools (Protégé/Stardog) that emit edges as plain
    # triples without sm:Statement reification.
    edges: list[dict] = []
    covered: set[tuple[Any, Any, Any]] = set()

    def _edge_props(stmt: Any) -> dict[str, Any]:
        props: dict[str, Any] = {}
        for pred in graph.predicates(stmt):
            if pred in (RDF.type, RDF.subject, RDF.predicate, RDF.object):
                continue
            pname = str(pred)[len(str(SM)) :]
            vals = [lit.toPython() for lit in graph.objects(stmt, pred)]
            props[pname] = vals[0] if len(vals) == 1 else vals
        return props

    for stmt in graph.subjects(RDF.type, SM.Statement):
        s = graph.value(stmt, RDF.subject)
        p = graph.value(stmt, RDF.predicate)
        o = graph.value(stmt, RDF.object)
        if s is None or p is None or o is None:
            continue
        rel_type = _local_name(p)
        if rel_type not in _REL_TYPES:
            continue
        edges.append(
            {
                "eid": f"r{len(edges)}",
                "start_eid": uri_to_eid.get(s, ""),
                "end_eid": uri_to_eid.get(o, ""),
                "rel_type": rel_type,
                "props": _edge_props(stmt),
            }
        )
        covered.add((s, p, o))

    # Fallback: plain triples of known rel types not already covered by a statement.
    for s, p, o in graph:
        if not str(p).startswith(str(SM)):
            continue
        rel_type = _local_name(p)
        if rel_type == "Statement" or rel_type not in _REL_TYPES:
            continue
        if (s, p, o) in covered:
            continue
        covered.add((s, p, o))
        edges.append(
            {
                "eid": f"r{len(edges)}",
                "start_eid": uri_to_eid.get(s, ""),
                "end_eid": uri_to_eid.get(o, ""),
                "rel_type": rel_type,
                "props": {},
            }
        )
    return nodes, edges


def _local_name(uri: Any) -> str:
    """Return the local name of a URI/namespace term (after the last # or /)."""
    text = str(uri)
    return text.rsplit("#", 1)[-1].rsplit("/", 1)[-1]
