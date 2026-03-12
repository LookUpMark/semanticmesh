"""Hybrid retriever — dense vector + BM25 + graph traversal.

EP-12 / US-12-01 to US-12-04:
Retrieves candidate nodes from Neo4j for a given natural-language query,
then merges and deduplicates results before passing to the reranker.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from src.config.logging import get_logger
from src.config.settings import get_settings
from src.models.schemas import RetrievedChunk
from src.retrieval.embeddings import embed_text

if TYPE_CHECKING:
    import logging

    from src.graph.neo4j_client import Neo4jClient

logger: logging.Logger = get_logger(__name__)


# ── Node Dump ──────────────────────────────────────────────────────────────────

def build_node_index(client: Neo4jClient) -> list[dict[str, Any]]:
    """Fetch all BusinessConcept and PhysicalTable nodes as plain dicts.

    This snapshot is kept in memory and used to build the BM25 token index at
    query-graph startup. It must be refreshed after each ingestion run.

    Args:
        client: Active ``Neo4jClient`` context.

    Returns:
        List of node property dicts with ``name``, ``node_type``, and other fields.
    """
    concept_records = client.execute_cypher(
        "MATCH (n:BusinessConcept) RETURN n.name AS name, "
        "n.definition AS definition, 'BusinessConcept' AS node_type, "
        "n.synonyms AS synonyms, n.source_doc AS source_doc"
    )
    table_records = client.execute_cypher(
        "MATCH (n:PhysicalTable) RETURN n.table_name AS name, "
        "'' AS definition, 'PhysicalTable' AS node_type, "
        "[] AS synonyms, n.source_doc AS source_doc, "
        "n.column_names AS column_names"
    )
    all_nodes = concept_records + table_records
    logger.debug("build_node_index: %d nodes fetched.", len(all_nodes))
    return all_nodes


# ── Dense Vector Search ────────────────────────────────────────────────────────

def vector_search(
    query: str,
    client: Neo4jClient,
    top_k: int | None = None,
    model=None,
) -> list[RetrievedChunk]:
    """Embed the query and run Neo4j vector index search on BusinessConcept nodes.

    Args:
        query:  Natural language query string.
        client: Active ``Neo4jClient``.
        top_k:  Number of results; defaults to ``settings.retrieval_vector_top_k``.
        model:  Optional pre-loaded FlagModel; passed to ``embed_text``.

    Returns:
        Sorted list of ``RetrievedChunk`` with ``source_type="vector"``.
    """
    settings = get_settings()
    n = top_k or settings.retrieval_vector_top_k
    query_vector: list[float] = embed_text(query, model=model)

    cypher = (
        "CALL db.index.vector.queryNodes('businessconcept_embedding', $k, $embedding) "
        "YIELD node, score "
        "RETURN node.name AS name, node.definition AS definition, "
        "score, 'BusinessConcept' AS node_type, "
        "node.source_doc AS source_doc, node.synonyms AS synonyms"
    )
    records = client.execute_cypher(cypher, {"k": n, "embedding": query_vector})

    chunks: list[RetrievedChunk] = []
    for rec in records:
        name = rec.get("name") or ""
        definition = rec.get("definition") or ""
        chunks.append(
            RetrievedChunk(
                node_id=name,
                node_type=rec.get("node_type", "BusinessConcept"),
                text=f"{name}: {definition}",
                score=float(rec.get("score", 0.0)),
                source_type="vector",
                metadata={
                    key: val for key, val in rec.items()
                    if key not in ("name", "definition", "score", "node_type")
                },
            )
        )
    logger.debug("vector_search: %d results for query '%s'.", len(chunks), query[:60])
    return chunks


# ── BM25 Keyword Search ────────────────────────────────────────────────────────

def _node_to_text(node: dict[str, Any]) -> str:
    """Flatten a node dict to a searchable string for BM25 tokenisation."""
    parts = [
        node.get("name") or "",
        node.get("definition") or "",
        " ".join(node.get("synonyms") or []),
        " ".join(node.get("column_names") or []),
    ]
    return " ".join(p for p in parts if p).lower()


def bm25_search(
    query: str,
    all_nodes: list[dict[str, Any]],
    top_k: int | None = None,
) -> list[RetrievedChunk]:
    """Keyword retrieval using BM25Okapi over a pre-built node text corpus.

    Args:
        query:     Natural language query string.
        all_nodes: Node dump from ``build_node_index``.
        top_k:     Number of results; defaults to ``settings.retrieval_bm25_top_k``.

    Returns:
        Sorted list of ``RetrievedChunk`` with ``source_type="bm25"``.
    """
    try:
        from rank_bm25 import BM25Okapi
    except ImportError as exc:
        raise ImportError("Install rank-bm25: pip install rank-bm25") from exc

    settings = get_settings()
    n = top_k or settings.retrieval_bm25_top_k

    if not all_nodes:
        return []

    corpus_texts: list[str] = [_node_to_text(node) for node in all_nodes]
    tokenised_corpus = [text.split() for text in corpus_texts]
    bm25 = BM25Okapi(tokenised_corpus)

    tokenised_query = query.lower().split()
    scores: list[float] = bm25.get_scores(tokenised_query).tolist()

    indexed = sorted(enumerate(scores), key=lambda x: x[1], reverse=True)[:n]
    chunks: list[RetrievedChunk] = []
    for idx, score in indexed:
        node = all_nodes[idx]
        name = node.get("name") or ""
        definition = node.get("definition") or ""
        chunks.append(
            RetrievedChunk(
                node_id=name,
                node_type=node.get("node_type", "BusinessConcept"),
                text=f"{name}: {definition}",
                score=score,
                source_type="bm25",
                metadata={
                    key: val for key, val in node.items()
                    if key not in ("name", "definition")
                },
            )
        )
    logger.debug("bm25_search: %d results for query '%s'.", len(chunks), query[:60])
    return chunks


# ── Graph Traversal ────────────────────────────────────────────────────────────

def graph_traversal(
    seed_names: list[str],
    client: Neo4jClient,
    depth: int | None = None,
) -> list[RetrievedChunk]:
    """Expand seed node names to their graph neighbours via Cypher traversal.

    Args:
        seed_names: Node names to start traversal from.
        client:     Active ``Neo4jClient``.
        depth:      Hop depth; defaults to ``settings.retrieval_graph_depth`` (2).

    Returns:
        List of ``RetrievedChunk`` with ``source_type="graph"``.
    """
    settings = get_settings()
    d = depth or settings.retrieval_graph_depth

    if not seed_names:
        return []

    cypher = (
        f"MATCH (start)-[r*1..{d}]-(neighbor) "
        "WHERE start.name IN $seed_names "
        "RETURN neighbor.name AS name, "
        "COALESCE(neighbor.definition, neighbor.table_name, '') AS definition, "
        "labels(neighbor)[0] AS node_type, type(r[0]) AS rel_type "
        "LIMIT 20"
    )
    records = client.execute_cypher(cypher, {"seed_names": seed_names})

    seen: set[str] = set()
    chunks: list[RetrievedChunk] = []
    for rec in records:
        name = rec.get("name") or ""
        if name in seen or name in seed_names:
            continue
        seen.add(name)
        definition = rec.get("definition") or ""
        chunks.append(
            RetrievedChunk(
                node_id=name,
                node_type=rec.get("node_type", "Unknown"),
                text=f"{name}: {definition}",
                score=0.5,  # graph neighbours get a neutral baseline score
                source_type="graph",
                metadata={"rel_type": rec.get("rel_type")},
            )
        )
    logger.debug("graph_traversal: %d neighbours found.", len(chunks))
    return chunks


# ── Result Merging ─────────────────────────────────────────────────────────────

def merge_results(
    vector: list[RetrievedChunk],
    bm25: list[RetrievedChunk],
    graph: list[RetrievedChunk],
) -> list[RetrievedChunk]:
    """Deduplicate and merge retrieval results from all three strategies.

    Deduplication by ``node_id`` — keep the highest score per node across
    all sources. Graph traversal results are included even at lower scores.

    Args:
        vector: Results from ``vector_search``.
        bm25:   Results from ``bm25_search``.
        graph:  Results from ``graph_traversal``.

    Returns:
        Deduplicated list sorted by score descending.
    """
    best: dict[str, RetrievedChunk] = {}
    for chunk in vector + bm25 + graph:
        nid = chunk.node_id
        if nid not in best or chunk.score > best[nid].score:
            best[nid] = chunk
    merged = sorted(best.values(), key=lambda c: c.score, reverse=True)
    logger.debug("merge_results: %d unique nodes.", len(merged))
    return merged
