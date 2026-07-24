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
import re
from datetime import UTC, datetime
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


def _dump_graph() -> tuple[list[dict], list[dict]]:
    """Return (nodes, edges) dicts from Neo4j. Thin wrapper over kg_registry.

    kg_registry._export_graph already strips embedding vectors (regenerated on
    query), so embeddings are never exported — matching the backup design.
    """
    from src.graph.kg_registry import _export_graph

    return _export_graph()


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


def export_to_owl_files() -> dict[str, Any]:
    """Export the live graph to 4 OWL files + metadata.json. Return metadata dict."""
    nodes, edges = _dump_graph()
    if not nodes and not edges:
        raise ValueError("no_data_to_export: the Knowledge Graph is empty")

    export_id = datetime.now(UTC).strftime("%Y%m%d_%H%M%S")
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
        graph, _ = build_graph(part_nodes, part_edges)
        text = graph.serialize(format="xml")
        path = out_dir / fname
        path.write_text(text, encoding="utf-8")
        checksums[fname] = _sha256(path)

    metadata = {
        "export_id": export_id,
        "timestamp": datetime.now(UTC).isoformat(),
        "nodes_count": len(nodes),
        "relationships_count": len(edges),
        "files": list(checksums),
        "checksums": checksums,
    }
    (out_dir / "metadata.json").write_text(json.dumps(metadata, indent=2), encoding="utf-8")
    logger.info(
        "OWL export %s: %d nodes, %d edges → %s",
        export_id,
        len(nodes),
        len(edges),
        out_dir,
    )
    return metadata


# Export ids are timestamps (YYYYMMDD_HHMMSS). Validate format + path containment
# to prevent traversal via the download endpoint (e.g. /export/..).
_EXPORT_ID_RE = re.compile(r"\d{8}_\d{6}")


def export_dir(export_id: str) -> Path:
    """Return the resolved directory path for a validated export id.

    Raises ValueError if the id is malformed or resolves outside _EXPORT_DIR.
    """
    if not _EXPORT_ID_RE.fullmatch(export_id):
        raise ValueError(f"invalid_export_id: {export_id!r}")
    directory = (_EXPORT_DIR / export_id).resolve()
    if not directory.is_relative_to(_EXPORT_DIR.resolve()):
        raise ValueError(f"invalid_export_id: {export_id!r}")
    return directory


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
