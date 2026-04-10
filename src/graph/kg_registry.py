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
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from src.config.logging import get_logger

logger = get_logger(__name__)

_DATA_DIR = Path(__file__).parent.parent.parent / "data" / "memory"
_REGISTRY_DB = _DATA_DIR / "kg_registry.db"
_SNAPSHOTS_DIR = _DATA_DIR / "kg_snapshots"


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
    - ParentChunk      → ``parent_chunk_id`` (fallback: ``chunk_id``)
    - Chunk            → ``chunk_id``
    - SourceFile       → ``path``
    - anything else    → ``name`` if present, else skip
    """
    from src.graph.neo4j_client import Neo4jClient, setup_schema

    def _business_key(node: dict) -> tuple[str, str] | None:
        """Return (label, key_value) used as MERGE identity, or None to skip."""
        labels = node["labels"]
        props = node["props"]
        if "BusinessConcept" in labels:
            k = props.get("name")
            return ("BusinessConcept", k) if k else None
        if "PhysicalTable" in labels:
            k = props.get("table_name")
            return ("PhysicalTable", k) if k else None
        if "ParentChunk" in labels:
            k = props.get("parent_chunk_id") or props.get("chunk_id")
            return ("ParentChunk", k) if k else None
        if "Chunk" in labels:
            k = props.get("chunk_id")
            return ("Chunk", k) if k else None
        if "SourceFile" in labels:
            k = props.get("path")
            return ("SourceFile", k) if k else None
        return None

    with Neo4jClient() as client:
        # 1. Wipe existing graph
        client.execute_cypher("MATCH (n) DETACH DELETE n")

        # 2. Re-create schema
        setup_schema(client)

        # 2. Build a mapping original_eid → business_key for relationship reconstruction
        eid_to_key: dict[str, tuple[str, str]] = {}
        for node in nodes:
            bk = _business_key(node)
            if bk:
                eid_to_key[node["eid"]] = bk

        # 3. MERGE nodes
        stmts: list[tuple[str, dict]] = []
        for node in nodes:
            bk = _business_key(node)
            if not bk:
                continue
            label, key_val = bk
            key_prop = "name" if label in ("BusinessConcept", "SourceFile") else (
                "table_name" if label == "PhysicalTable" else (
                    "parent_chunk_id" if label == "ParentChunk" else "chunk_id"
                )
            )
            props_without_key = {k: v for k, v in node["props"].items() if k != key_prop}
            cypher = (
                f"MERGE (n:{label} {{{key_prop}: $key}}) "
                "SET n += $props"
            )
            stmts.append((cypher, {"key": key_val, "props": props_without_key}))

        # Execute in batches of 200
        for i in range(0, len(stmts), 200):
            client.execute_batch(stmts[i:i + 200])

        # 4. MERGE relationships
        rel_stmts: list[tuple[str, dict]] = []
        for edge in edges:
            src = eid_to_key.get(edge["start_eid"])
            tgt = eid_to_key.get(edge["end_eid"])
            if not src or not tgt:
                continue
            src_label, src_key = src
            tgt_label, tgt_key = tgt
            src_prop = "name" if src_label in ("BusinessConcept", "SourceFile") else (
                "table_name" if src_label == "PhysicalTable" else (
                    "parent_chunk_id" if src_label == "ParentChunk" else "chunk_id"
                )
            )
            tgt_prop = "name" if tgt_label in ("BusinessConcept", "SourceFile") else (
                "table_name" if tgt_label == "PhysicalTable" else (
                    "parent_chunk_id" if tgt_label == "ParentChunk" else "chunk_id"
                )
            )
            rel_type = edge["rel_type"]
            cypher = (
                f"MATCH (a:{src_label} {{{src_prop}: $src_key}}) "
                f"MATCH (b:{tgt_label} {{{tgt_prop}: $tgt_key}}) "
                f"MERGE (a)-[r:{rel_type}]->(b) "
                "SET r += $props"
            )
            rel_stmts.append((cypher, {
                "src_key": src_key,
                "tgt_key": tgt_key,
                "props": edge["props"],
            }))

        for i in range(0, len(rel_stmts), 200):
            client.execute_batch(rel_stmts[i:i + 200])

    logger.info(
        "KG import complete: %d nodes, %d edges merged.",
        len([n for n in nodes if _business_key(n)]),
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

    created_at = datetime.now(timezone.utc).isoformat()
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
