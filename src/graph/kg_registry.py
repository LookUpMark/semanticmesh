"""Knowledge-Graph snapshot registry.

Stores named KG snapshots to SQLite and exports/imports the live Neo4j graph
so users can save, load, and eject Knowledge Graphs at will — similar to
loading/unloading a model in LM Studio.

Storage layout::

    data/memory/kg_registry.db   ← SQLite with snapshot metadata + active pointer
    data/memory/kg_snapshots/    ← one JSON file per snapshot

Snapshot JSON schema::

    {
      "id":         "<uuid>",
      "name":       "E-Commerce v1",
      "nodes":  [ {"element_id": "...", "labels": [...], "props": {...}}, ... ],
      "edges":  [ {"element_id": "...", "start_id": "...", "end_id": "...",
                   "type": "MAPPED_TO", "props": {...}}, ... ]
    }

Because Neo4j element IDs are internal and change on import, nodes are keyed by
their *business identity* (``name`` for BusinessConcept, ``table_name`` for
PhysicalTable, ``chunk_id`` for Chunk/ParentChunk) so MERGE idempotency works.
"""

from __future__ import annotations

import json
import sqlite3
import uuid
from contextlib import contextmanager
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from src.config.logging import get_logger

logger = get_logger(__name__)

_DATA_DIR = Path(__file__).parent.parent.parent / "data" / "memory"
_REGISTRY_DB = _DATA_DIR / "kg_registry.db"
_SNAPSHOTS_DIR = _DATA_DIR / "kg_snapshots"

_ALLOWED_REL_TYPES = frozenset({
    "MAPPED_TO", "HAS_ATTRIBUTE", "REFERENCES", "MENTIONS",
    "DESCRIBED_BY", "PART_OF", "INSTANCE_OF", "CONTAINS_CHUNK",
})


# ─────────────────────────────────────────────────────────────────────────────
# DB bootstrap
# ─────────────────────────────────────────────────────────────────────────────

def _ensure_dirs() -> None:
    _DATA_DIR.mkdir(parents=True, exist_ok=True)
    _SNAPSHOTS_DIR.mkdir(parents=True, exist_ok=True)


@contextmanager
def _db():
    _ensure_dirs()
    conn = sqlite3.connect(str(_REGISTRY_DB))
    conn.row_factory = sqlite3.Row
    try:
        _bootstrap(conn)
        yield conn
        conn.commit()
    finally:
        conn.close()


def _bootstrap(conn: sqlite3.Connection) -> None:
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS kg_snapshots (
            id            TEXT PRIMARY KEY,
            name          TEXT NOT NULL,
            description   TEXT NOT NULL DEFAULT '',
            created_at    TEXT NOT NULL,
            node_count    INTEGER NOT NULL DEFAULT 0,
            edge_count    INTEGER NOT NULL DEFAULT 0,
            snapshot_path TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS kg_active (
            singleton     INTEGER PRIMARY KEY DEFAULT 1 CHECK (singleton = 1),
            snapshot_id   TEXT REFERENCES kg_snapshots(id) ON DELETE SET NULL
        );

        INSERT OR IGNORE INTO kg_active (singleton, snapshot_id) VALUES (1, NULL);
    """)


# ─────────────────────────────────────────────────────────────────────────────
# Neo4j export helpers
# ─────────────────────────────────────────────────────────────────────────────

def _export_graph() -> tuple[list[dict], list[dict]]:
    """Dump all nodes and edges from Neo4j as plain dicts (no embeddings)."""
    from src.graph.neo4j_client import Neo4jClient

    nodes_cypher = """
    MATCH (n)
    RETURN
        elementId(n)    AS eid,
        labels(n)       AS labels,
        properties(n)   AS props
    """

    edges_cypher = """
    MATCH (a)-[r]->(b)
    RETURN
        elementId(r)    AS eid,
        elementId(a)    AS start_eid,
        elementId(b)    AS end_eid,
        type(r)         AS rel_type,
        properties(r)   AS props
    """

    with Neo4jClient() as client:
        raw_nodes = client.execute_cypher(nodes_cypher)
        raw_edges = client.execute_cypher(edges_cypher)

    nodes = []
    for row in raw_nodes:
        props = dict(row["props"] or {})
        props.pop("embedding", None)  # omit large vectors — they'll be regenerated on load
        nodes.append({
            "eid": row["eid"],
            "labels": list(row["labels"]),
            "props": props,
        })

    edges = [
        {
            "eid": row["eid"],
            "start_eid": row["start_eid"],
            "end_eid": row["end_eid"],
            "rel_type": row["rel_type"],
            "props": dict(row["props"] or {}),
        }
        for row in raw_edges
    ]

    return nodes, edges


# ─────────────────────────────────────────────────────────────────────────────
# Neo4j import helpers
# ─────────────────────────────────────────────────────────────────────────────

def _import_graph(nodes: list[dict], edges: list[dict]) -> None:
    """Restore a snapshot into Neo4j (clear first, then MERGE all nodes+edges).

    Node identity for MERGE:
    - BusinessConcept  → ``name``
    - PhysicalTable    → ``table_name``
    - ParentChunk      → compound key: ``{parent_chunk_index, source_doc}``
    - Chunk            → compound key: ``{chunk_index, source_doc}``
    - SourceFile       → ``path``
    - anything else    → ``name`` if present, else skip
    """
    from src.graph.neo4j_client import Neo4jClient, setup_schema

    # Returns a stable string fingerprint for an eid, used to wire relationships.
    def _node_fingerprint(node: dict) -> str | None:
        labels = node["labels"]
        props = node["props"]
        if "BusinessConcept" in labels:
            k = props.get("name")
            return f"BusinessConcept::{k}" if k else None
        if "PhysicalTable" in labels:
            k = props.get("table_name")
            return f"PhysicalTable::{k}" if k else None
        if "ParentChunk" in labels:
            idx = props.get("parent_chunk_index")
            src = props.get("source_doc", "")
            return f"ParentChunk::{idx}::{src}" if idx is not None else None
        if "Chunk" in labels:
            idx = props.get("chunk_index")
            src = props.get("source_doc", "")
            return f"Chunk::{idx}::{src}" if idx is not None else None
        if "SourceFile" in labels:
            k = props.get("path")
            return f"SourceFile::{k}" if k else None
        return None

    def _merge_cypher_and_params(node: dict) -> tuple[str, dict] | None:
        """Return (cypher, params) for MERGE of this node, or None to skip."""
        labels = node["labels"]
        props = node["props"]
        if "BusinessConcept" in labels:
            name = props.get("name")
            if not name:
                return None
            rest = {k: v for k, v in props.items() if k != "name"}
            return (
                "MERGE (n:BusinessConcept {name: $key}) SET n += $props",
                {"key": name, "props": rest},
            )
        if "PhysicalTable" in labels:
            tn = props.get("table_name")
            if not tn:
                return None
            rest = {k: v for k, v in props.items() if k != "table_name"}
            return (
                "MERGE (n:PhysicalTable {table_name: $key}) SET n += $props",
                {"key": tn, "props": rest},
            )
        if "ParentChunk" in labels:
            idx = props.get("parent_chunk_index")
            src = props.get("source_doc", "")
            if idx is None:
                return None
            rest = {k: v for k, v in props.items() if k not in ("parent_chunk_index", "source_doc")}
            return (
                "MERGE (n:ParentChunk {parent_chunk_index: $idx, source_doc: $src}) SET n += $props",
                {"idx": idx, "src": src, "props": rest},
            )
        if "Chunk" in labels:
            idx = props.get("chunk_index")
            src = props.get("source_doc", "")
            if idx is None:
                return None
            rest = {k: v for k, v in props.items() if k not in ("chunk_index", "source_doc")}
            return (
                "MERGE (n:Chunk {chunk_index: $idx, source_doc: $src}) SET n += $props",
                {"idx": idx, "src": src, "props": rest},
            )
        if "SourceFile" in labels:
            path = props.get("path")
            if not path:
                return None
            rest = {k: v for k, v in props.items() if k != "path"}
            return (
                "MERGE (n:SourceFile {path: $key}) SET n += $props",
                {"key": path, "props": rest},
            )
        return None

    def _match_clause(fingerprint: str) -> tuple[str, str, dict]:
        """Return (alias_cypher_fragment, alias_letter, params) for a MATCH by fingerprint."""
        parts = fingerprint.split("::", 2)
        label = parts[0]
        if label == "BusinessConcept":
            return "({a}:BusinessConcept {name: ${a}_key})", "a", {"{a}_key": parts[1]}
        if label == "PhysicalTable":
            return "({a}:PhysicalTable {table_name: ${a}_key})", "a", {"{a}_key": parts[1]}
        if label == "ParentChunk":
            return (
                "({a}:ParentChunk {parent_chunk_index: ${a}_idx, source_doc: ${a}_src})",
                "a",
                {"{a}_idx": int(parts[1]), "{a}_src": parts[2]},
            )
        if label == "Chunk":
            return (
                "({a}:Chunk {chunk_index: ${a}_idx, source_doc: ${a}_src})",
                "a",
                {"{a}_idx": int(parts[1]), "{a}_src": parts[2]},
            )
        if label == "SourceFile":
            return "({a}:SourceFile {path: ${a}_key})", "a", {"{a}_key": parts[1]}
        return "", "a", {}

    with Neo4jClient() as client:
        # 1. Wipe existing graph
        client.execute_cypher("MATCH (n) DETACH DELETE n")

        # 2. Re-create schema constraints/indexes
        setup_schema(client)

        # 3. Build eid → fingerprint map for relationship reconstruction
        eid_to_fp: dict[str, str] = {}
        for node in nodes:
            fp = _node_fingerprint(node)
            if fp:
                eid_to_fp[node["eid"]] = fp

        # 4. MERGE nodes
        node_stmts: list[tuple[str, dict]] = []
        for node in nodes:
            mc = _merge_cypher_and_params(node)
            if mc:
                node_stmts.append(mc)

        for i in range(0, len(node_stmts), 200):
            client.execute_batch(node_stmts[i:i + 200])

        # 5. MERGE relationships — build per-relationship MATCH+MERGE statements
        rel_stmts: list[tuple[str, dict]] = []
        for edge in edges:
            src_fp = eid_to_fp.get(edge["start_eid"])
            tgt_fp = eid_to_fp.get(edge["end_eid"])
            if not src_fp or not tgt_fp:
                continue

            # Build MATCH fragments with distinct aliases (a, b)
            def _match_frag(fp: str, alias: str) -> tuple[str, dict]:
                parts = fp.split("::", 2)
                label = parts[0]
                if label in ("BusinessConcept", "SourceFile"):
                    prop = "name" if label == "BusinessConcept" else "path"
                    return (
                        f"MATCH ({alias}:{label} {{{prop}: ${alias}_key}})",
                        {f"{alias}_key": parts[1]},
                    )
                if label == "PhysicalTable":
                    return (
                        f"MATCH ({alias}:PhysicalTable {{table_name: ${alias}_key}})",
                        {f"{alias}_key": parts[1]},
                    )
                if label == "ParentChunk":
                    return (
                        f"MATCH ({alias}:ParentChunk {{parent_chunk_index: ${alias}_idx, source_doc: ${alias}_src}})",
                        {f"{alias}_idx": int(parts[1]), f"{alias}_src": parts[2]},
                    )
                if label == "Chunk":
                    return (
                        f"MATCH ({alias}:Chunk {{chunk_index: ${alias}_idx, source_doc: ${alias}_src}})",
                        {f"{alias}_idx": int(parts[1]), f"{alias}_src": parts[2]},
                    )
                return "", {}

            src_match, src_params = _match_frag(src_fp, "a")
            tgt_match, tgt_params = _match_frag(tgt_fp, "b")
            if not src_match or not tgt_match:
                continue

            rel_type = edge["rel_type"]
            if rel_type not in _ALLOWED_REL_TYPES:
                logger.warning("Skipping unknown relationship type '%s' during import.", rel_type)
                continue
            cypher = f"{src_match} {tgt_match} MERGE (a)-[r:`{rel_type}`]->(b) SET r += $props"
            params = {**src_params, **tgt_params, "props": edge["props"]}
            rel_stmts.append((cypher, params))

        for i in range(0, len(rel_stmts), 200):
            client.execute_batch(rel_stmts[i:i + 200])

    logger.info(
        "KG import complete: %d nodes, %d edges merged.",
        len(node_stmts),
        len(rel_stmts),
    )


# ─────────────────────────────────────────────────────────────────────────────
# Public API
# ─────────────────────────────────────────────────────────────────────────────

def list_snapshots() -> list[dict[str, Any]]:
    """Return all saved KG snapshots (metadata only, no graph data)."""
    with _db() as conn:
        active_row = conn.execute("SELECT snapshot_id FROM kg_active WHERE singleton=1").fetchone()
        active_id = active_row["snapshot_id"] if active_row else None
        rows = conn.execute(
            "SELECT id, name, description, created_at, node_count, edge_count "
            "FROM kg_snapshots ORDER BY created_at DESC"
        ).fetchall()
    return [
        {
            "id": r["id"],
            "name": r["name"],
            "description": r["description"],
            "created_at": r["created_at"],
            "node_count": r["node_count"],
            "edge_count": r["edge_count"],
            "is_active": r["id"] == active_id,
        }
        for r in rows
    ]


def get_active_snapshot() -> dict[str, Any] | None:
    """Return metadata of the currently loaded KG snapshot, or None."""
    with _db() as conn:
        row = conn.execute("""
            SELECT s.id, s.name, s.description, s.created_at, s.node_count, s.edge_count
            FROM kg_active a
            LEFT JOIN kg_snapshots s ON s.id = a.snapshot_id
            WHERE a.singleton = 1 AND a.snapshot_id IS NOT NULL
        """).fetchone()
    if row is None:
        return None
    result = dict(row)
    result["is_active"] = True
    return result


def save_snapshot(name: str, description: str = "") -> dict[str, Any]:
    """Export the current Neo4j graph and register it as a named snapshot.

    Returns the snapshot metadata dict.
    """
    snap_id = str(uuid.uuid4())
    snapshot_path = _SNAPSHOTS_DIR / f"{snap_id}.json"

    logger.info("Exporting KG snapshot '%s' …", name)
    nodes, edges = _export_graph()

    payload = {"id": snap_id, "name": name, "nodes": nodes, "edges": edges}
    _ensure_dirs()
    snapshot_path.write_text(json.dumps(payload, default=str), encoding="utf-8")

    created_at = datetime.now(UTC).isoformat()
    with _db() as conn:
        conn.execute(
            "INSERT INTO kg_snapshots (id, name, description, created_at, node_count, edge_count, snapshot_path) "
            "VALUES (?, ?, ?, ?, ?, ?, ?)",
            (snap_id, name, description, created_at, len(nodes), len(edges), str(snapshot_path)),
        )

    logger.info(
        "Snapshot '%s' saved: %d nodes, %d edges → %s",
        name, len(nodes), len(edges), snapshot_path,
    )
    return {
        "id": snap_id,
        "name": name,
        "description": description,
        "created_at": created_at,
        "node_count": len(nodes),
        "edge_count": len(edges),
        "is_active": False,
    }


def load_snapshot(snapshot_id: str) -> dict[str, Any]:
    """Clear Neo4j, restore the given snapshot, and mark it as active.

    Returns the snapshot metadata dict.
    """
    with _db() as conn:
        row = conn.execute(
            "SELECT id, name, description, created_at, node_count, edge_count, snapshot_path "
            "FROM kg_snapshots WHERE id = ?",
            (snapshot_id,),
        ).fetchone()
    if row is None:
        raise ValueError(f"Snapshot '{snapshot_id}' not found.")

    snapshot_path = Path(row["snapshot_path"])
    if not snapshot_path.exists():
        raise FileNotFoundError(f"Snapshot file missing: {snapshot_path}")

    payload = json.loads(snapshot_path.read_text(encoding="utf-8"))
    nodes = payload["nodes"]
    edges = payload["edges"]

    logger.info("Loading KG snapshot '%s' (%d nodes, %d edges) …", row["name"], len(nodes), len(edges))
    _import_graph(nodes, edges)

    with _db() as conn:
        conn.execute(
            "UPDATE kg_active SET snapshot_id = ? WHERE singleton = 1",
            (snapshot_id,),
        )

    logger.info("Snapshot '%s' loaded and set as active.", row["name"])
    return {
        "id": row["id"],
        "name": row["name"],
        "description": row["description"],
        "created_at": row["created_at"],
        "node_count": len(nodes),
        "edge_count": len(edges),
        "is_active": True,
    }


def eject_snapshot() -> None:
    """Clear the active pointer (the Neo4j data is NOT modified).

    Use this to mark that no named snapshot is currently loaded —
    the live graph may differ from any saved snapshot.
    """
    with _db() as conn:
        conn.execute("UPDATE kg_active SET snapshot_id = NULL WHERE singleton = 1")
    logger.info("Active KG snapshot ejected.")


def delete_snapshot(snapshot_id: str) -> None:
    """Delete a snapshot file and its registry entry.

    If it was the active snapshot, the active pointer is cleared.
    Raises ValueError if not found.
    """
    with _db() as conn:
        row = conn.execute(
            "SELECT snapshot_path FROM kg_snapshots WHERE id = ?",
            (snapshot_id,),
        ).fetchone()
        if row is None:
            raise ValueError(f"Snapshot '{snapshot_id}' not found.")
        conn.execute("DELETE FROM kg_snapshots WHERE id = ?", (snapshot_id,))
        conn.execute(
            "UPDATE kg_active SET snapshot_id = NULL WHERE singleton = 1 AND snapshot_id = ?",
            (snapshot_id,),
        )

    path = Path(row["snapshot_path"])
    if path.exists():
        path.unlink()
    logger.info("Snapshot '%s' deleted.", snapshot_id)


def rename_snapshot(
    snapshot_id: str,
    name: str,
    description: str | None = None,
) -> dict[str, Any]:
    """Update the name and optionally the description of an existing snapshot.

    Args:
        snapshot_id: UUID of the snapshot to rename.
        name: New human-readable name.
        description: New description. If ``None``, the existing value is kept.

    Returns:
        Updated snapshot metadata dict.

    Raises:
        ValueError: If the snapshot does not exist.
    """
    with _db() as conn:
        row = conn.execute(
            "SELECT id, name, description, created_at, node_count, edge_count "
            "FROM kg_snapshots WHERE id = ?",
            (snapshot_id,),
        ).fetchone()
        if row is None:
            raise ValueError(f"Snapshot '{snapshot_id}' not found.")

        new_desc = description if description is not None else row["description"]
        conn.execute(
            "UPDATE kg_snapshots SET name = ?, description = ? WHERE id = ?",
            (name, new_desc, snapshot_id),
        )

        active_row = conn.execute("SELECT snapshot_id FROM kg_active WHERE singleton=1").fetchone()
        active_id = active_row["snapshot_id"] if active_row else None

    logger.info("Snapshot '%s' renamed to '%s'.", snapshot_id, name)
    return {
        "id": snapshot_id,
        "name": name,
        "description": new_desc,
        "created_at": row["created_at"],
        "node_count": row["node_count"],
        "edge_count": row["edge_count"],
        "is_active": snapshot_id == active_id,
    }
