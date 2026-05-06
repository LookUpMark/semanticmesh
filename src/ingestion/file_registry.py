"""Incremental ingestion file registry — SHA-256 based change detection.

Tracks ingested source files in Neo4j as ``(:SourceFile)`` nodes.  On each
build run the pipeline can:

  1. **Skip** files whose SHA-256 hasn't changed since the last ingest.
  2. **Re-ingest** files whose content has been modified (purge old data first).
  3. **Purge** files that were present in the previous run but are absent now
     (user deleted or renamed the file).

Node schema::

    (:SourceFile {
        path:        str,       # canonical file path (UNIQUE key)
        sha256:      str,       # hex digest of file contents
        byte_size:   int,       # raw file size in bytes
        chunk_count: int,       # number of Chunk nodes created from this file
        ingested_at: datetime,  # timestamp of latest successful ingest
    })
"""

from __future__ import annotations

import hashlib
import logging
from pathlib import Path
from typing import TYPE_CHECKING, Literal

if TYPE_CHECKING:
    from src.graph.neo4j_client import Neo4jClient

from src.config.logging import get_logger

logger: logging.Logger = get_logger(__name__)

FileStatus = Literal["unchanged", "modified", "new"]

_CHUNK_SIZE = 65_536  # 64 KiB read buffer for streaming SHA computation


# ── Public API ────────────────────────────────────────────────────────────────


def compute_file_sha(path: str | Path) -> str:
    """Return the SHA-256 hex digest of *path* using streaming I/O.

    Streaming avoids loading large PDFs entirely into memory.

    Args:
        path: Absolute or relative file path.

    Returns:
        64-character lowercase hex string, e.g. ``"a3f4..."``.

    Raises:
        FileNotFoundError: If the file does not exist.
    """
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        while chunk := fh.read(_CHUNK_SIZE):
            h.update(chunk)
    return h.hexdigest()


def check_file_status(client: Neo4jClient, path: str, sha: str) -> FileStatus:
    """Compare *sha* against the stored digest for *path*.

    Args:
        client: Open Neo4jClient context.
        path:   Canonical source-doc identifier (same string used in Chunk nodes).
        sha:    Current SHA-256 hex digest of the file on disk.

    Returns:
        - ``"unchanged"``  — digest matches; no re-ingestion needed.
        - ``"modified"``   — file exists in registry but digest differs.
        - ``"new"``        — no SourceFile node found for this path.
    """
    rows = client.execute_cypher(
        "MATCH (sf:SourceFile {path: $path}) RETURN sf.sha256 AS sha",
        {"path": path},
    )
    if not rows:
        return "new"
    stored_sha = rows[0].get("sha") or ""
    return "unchanged" if stored_sha == sha else "modified"


def register_file(
    client: Neo4jClient,
    path: str,
    sha: str,
    chunk_count: int,
) -> None:
    """Upsert a ``SourceFile`` node after successful ingestion.

    Safe to call multiple times — uses ``MERGE`` so repeated calls are idempotent.

    Args:
        client:      Open Neo4jClient context.
        path:        Canonical source-doc identifier.
        sha:         SHA-256 hex digest written to the node.
        chunk_count: Number of Chunk (child) nodes created from this file.
    """
    client.execute_cypher(
        "MERGE (sf:SourceFile {path: $path}) "
        "ON CREATE SET sf.sha256 = $sha, "
        "              sf.byte_size = $byte_size, "
        "              sf.chunk_count = $chunk_count, "
        "              sf.ingested_at = datetime() "
        "ON MATCH SET  sf.sha256 = $sha, "
        "              sf.byte_size = $byte_size, "
        "              sf.chunk_count = $chunk_count, "
        "              sf.ingested_at = datetime()",
        {
            "path": path,
            "sha": sha,
            "byte_size": Path(path).stat().st_size if Path(path).exists() else -1,
            "chunk_count": chunk_count,
        },
    )
    logger.debug("SourceFile registered: path=%s sha=%s…", path, sha[:12])


def get_orphaned_files(client: Neo4jClient, current_paths: set[str]) -> list[str]:
    """Return paths of SourceFile nodes **not** in *current_paths*.

    These represent files that were ingested in a previous run but are no longer
    present in the current input set (deleted, renamed, or removed from scope).

    Args:
        client:        Open Neo4jClient context.
        current_paths: Set of canonical paths for files being processed this run.

    Returns:
        List of ``path`` strings for orphaned SourceFile nodes.
    """
    if not current_paths:
        return []
    rows = client.execute_cypher(
        "MATCH (sf:SourceFile) WHERE NOT sf.path IN $paths RETURN sf.path AS path",
        {"paths": list(current_paths)},
    )
    orphans = [r["path"] for r in rows if r.get("path")]
    if orphans:
        logger.info("Found %d orphaned SourceFile(s): %s", len(orphans), orphans)
    return orphans


def purge_file_data(client: Neo4jClient, source_doc: str) -> int:
    """Delete all Neo4j data derived from *source_doc*.

    Removes, in order:
    1. ``Chunk`` nodes (with all relationships, including CHILD_OF and MENTIONS).
    2. ``ParentChunk`` nodes (with remaining relationships).
    3. ``PhysicalTable`` nodes whose ``source_file`` matches (DDL-derived;
       cascades MAPPED_TO + REFERENCES edges).
    4. The ``SourceFile`` registry node itself.
    5. Orphan ``BusinessConcept`` cleanup — concepts with no remaining
       MENTIONS edges and no MAPPED_TO edges are deleted since they are
       no longer grounded in any source material.

    Args:
        client:     Open Neo4jClient context.
        source_doc: Canonical source-doc identifier (the ``path`` field).

    Returns:
        Total number of nodes deleted.
    """
    # Build a deduplicated list of identifiers (full path + basename if different)
    basename = source_doc.rsplit("/", 1)[-1] if "/" in source_doc else source_doc
    src_variants = list(dict.fromkeys([source_doc, basename]))  # preserves order, deduplicates

    # 1. Delete child Chunk nodes (cascades CHILD_OF + MENTIONS edges)
    rows_c = client.execute_cypher(
        "MATCH (c:Chunk) WHERE c.source_doc IN $srcs DETACH DELETE c RETURN count(c) AS n",
        {"srcs": src_variants},
    )
    n_chunks = (rows_c[0].get("n") or 0) if rows_c else 0

    # 2. Delete parent ParentChunk nodes
    rows_p = client.execute_cypher(
        "MATCH (pc:ParentChunk) WHERE pc.source_doc IN $srcs "
        "DETACH DELETE pc RETURN count(pc) AS n",
        {"srcs": src_variants},
    )
    n_parents = (rows_p[0].get("n") or 0) if rows_p else 0

    # 3. Delete PhysicalTable nodes whose source_file matches this DDL path
    rows_t = client.execute_cypher(
        "MATCH (pt:PhysicalTable) WHERE pt.source_file IN $srcs "
        "DETACH DELETE pt RETURN count(pt) AS n",
        {"srcs": src_variants},
    )
    n_tables = (rows_t[0].get("n") or 0) if rows_t else 0

    # 4. Remove the SourceFile registry node
    client.execute_cypher(
        "MATCH (sf:SourceFile {path: $src}) DELETE sf",
        {"src": source_doc},
    )

    # 5. Clean up orphan BusinessConcepts — nodes with no remaining edges
    #    A concept is orphaned when all its MENTIONS edges (from deleted Chunks)
    #    and all its MAPPED_TO edges (from deleted PhysicalTables) are gone.
    rows_bc = client.execute_cypher(
        "MATCH (bc:BusinessConcept) "
        "WHERE NOT (bc)<-[:MENTIONS]-() AND NOT (bc)-[:MAPPED_TO]->() "
        "DETACH DELETE bc RETURN count(bc) AS n"
    )
    n_orphan_bc = (rows_bc[0].get("n") or 0) if rows_bc else 0

    total = n_chunks + n_parents + n_tables + n_orphan_bc
    logger.info(
        "Purged source_doc='%s': %d Chunk(s), %d ParentChunk(s), "
        "%d PhysicalTable(s), %d orphan BusinessConcept(s) deleted.",
        source_doc,
        n_chunks,
        n_parents,
        n_tables,
        n_orphan_bc,
    )
    return total
