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
