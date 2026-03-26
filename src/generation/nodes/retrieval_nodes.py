"""Retrieval and reranking nodes for the query pipeline.

Nodes:
- _node_retrieve: Hybrid retrieval combining vector, BM25, and graph traversal
- _node_rerank: Cross-encoder reranking with quality filtering
"""

from __future__ import annotations

import re
from typing import TYPE_CHECKING, Any

from src.config.logging import get_logger
from src.config.settings import get_settings
from src.graph.neo4j_client import Neo4jClient
from src.models.schemas import RetrievedChunk
from src.models.state import QueryState
from src.retrieval.embeddings import get_embeddings
from src.retrieval.hybrid_retriever import (
    bm25_search,
    build_node_index,
    fetch_all_concepts,
    fetch_fk_relationships,
    graph_traversal,
    merge_results,
    vector_search,
)
from src.retrieval.reranker import rerank

if TYPE_CHECKING:
    import logging

logger: logging.Logger = get_logger(__name__)

_TOKEN_RE = re.compile(r"[a-zA-Z0-9_]+")
_NOISE_MARKERS = (
    "heuristic embedding mapping score=",
    "adjusted_confidence=",
    "best_candidate=",
)
_RELATION_TOKENS = ("references", "foreign key", "fk ", " fk", "joins", "join ")
_PRIORITY_STRUCTURE_TOKENS = ("references", "foreign key")


# ── Helper Functions ──


def _has_relation_tokens(text: str) -> bool:
    return any(token in text for token in _RELATION_TOKENS)


def _has_priority_structure_tokens(text: str) -> bool:
    return any(token in text for token in _PRIORITY_STRUCTURE_TOKENS)


def _active_chunks(state: QueryState) -> list[RetrievedChunk]:
    return state.get("generation_chunks") or state.get("reranked_chunks") or []


def _has_structural_relationship_evidence(chunks: list[RetrievedChunk]) -> bool:
    for chunk in chunks:
        node_id = chunk.node_id.strip().lower()
        text = chunk.text.strip().lower()
        if "→" in node_id:
            return True
        if _has_relation_tokens(text):
            return True
    return False


def _query_terms(query: str) -> set[str]:
    stop = {
        "what",
        "which",
        "where",
        "when",
        "how",
        "does",
        "the",
        "this",
        "that",
        "with",
        "into",
        "from",
        "each",
        "for",
        "and",
        "are",
        "table",
        "database",
        "business",
        "concept",
        "information",
        "schema",
        "knowledge",
        "graph",
    }
    return {t.lower() for t in _TOKEN_RE.findall(query) if len(t) > 2 and t.lower() not in stop}


def _is_noise_chunk(chunk: RetrievedChunk) -> bool:
    text = chunk.text.lower()
    if any(marker in text for marker in _NOISE_MARKERS):
        return True
    if len(chunk.text.strip()) < 18 and "→" not in chunk.node_id:
        return True
    return False


def _pre_filter_rerank_pool(
    chunks: list[RetrievedChunk],
    query: str,
    max_candidates: int,
) -> list[RetrievedChunk]:
    """Filter and prioritize chunks before reranking.

    Removes noise chunks and prioritizes by:
    1. Structural evidence (FK edges)
    2. Query keyword matches
    3. Source type (graph > vector/bm25)
    4. Relevance score
    """
    if not chunks:
        return []

    terms = _query_terms(query)

    def _chunk_priority(chunk: RetrievedChunk) -> tuple[int, int, int, float]:
        text_l = chunk.text.lower()
        nid_l = chunk.node_id.lower()
        has_structure = int("→" in chunk.node_id or _has_priority_structure_tokens(text_l))
        keyword_hits = int(any(term in text_l or term in nid_l for term in terms))
        # source_rank before has_structure: ensures high-quality vector/BM25 entity hits
        # are not displaced by FK-edge graph chunks when keyword relevance is equal.
        source_rank = 2 if chunk.source_type in {"vector", "bm25"} else 1
        return (keyword_hits, source_rank, has_structure, float(chunk.score))

    selected: list[RetrievedChunk] = []
    dropped_noise = 0
    for chunk in chunks:
        if not chunk.node_id.strip() or not chunk.text.strip():
            continue
        if _is_noise_chunk(chunk):
            dropped_noise += 1
            continue
        selected.append(chunk)

    if not selected:
        selected = [c for c in chunks if c.node_id.strip() and c.text.strip()]

    selected.sort(key=_chunk_priority, reverse=True)
    limited = selected[:max_candidates]
    if dropped_noise:
        logger.info(
            "Pre-rerank quality filter dropped %d noisy chunk(s); kept %d/%d candidates.",
            dropped_noise,
            len(limited),
            len(chunks),
        )
    return limited


# ── Node Implementations ──


def _node_retrieve(state: QueryState) -> dict[str, Any]:
    """Execute hybrid retrieval: vector + BM25 + graph traversal with RRF fusion.

    Supports three retrieval modes via settings.retrieval_mode:
    - "vector": Dense vector search only
    - "bm25": Keyword search only
    - "hybrid" (default): Vector + BM25 + graph traversal with lazy expansion
    """
    settings = get_settings()
    query: str = state["user_query"]
    model = get_embeddings()

    retrieval_mode = (settings.retrieval_mode or "hybrid").lower()
    with Neo4jClient() as client:
        all_nodes = build_node_index(client)
        if retrieval_mode == "vector":
            vec_results = vector_search(
                query, client, top_k=settings.retrieval_vector_top_k, model=model
            )
            merged = vec_results
        elif retrieval_mode == "bm25":
            bm25_results = bm25_search(query, all_nodes, top_k=settings.retrieval_bm25_top_k)
            merged = bm25_results
        else:
            vec_results = vector_search(
                query, client, top_k=settings.retrieval_vector_top_k, model=model
            )
            trav_results = graph_traversal(
                seed_names=[c.node_id for c in vec_results[:5]],
                client=client,
                depth=settings.retrieval_graph_depth,
            )
            all_concepts = fetch_all_concepts(client)
            fk_chunks = fetch_fk_relationships(client)
            bm25_results = bm25_search(query, all_nodes, top_k=settings.retrieval_bm25_top_k)
            merged = merge_results(
                vec_results, bm25_results, trav_results + all_concepts + fk_chunks
            )

            if getattr(settings, "enable_lazy_expansion", False):
                from src.generation.lazy_expander import (
                    collect_seed_names_for_expansion,
                    should_trigger_lazy_expansion,
                )

                top_score = float(merged[0].score) if merged else 0.0
                if should_trigger_lazy_expansion(
                    top_score,
                    len(merged),
                    float(getattr(settings, "lazy_expansion_confidence_threshold", 0.40)),
                ):
                    seeds = collect_seed_names_for_expansion(merged, limit=8)
                    extra = graph_traversal(
                        seed_names=seeds,
                        client=client,
                        depth=max(1, settings.retrieval_graph_depth + 1),
                    )
                    merged = merge_results(
                        vec_results, bm25_results, trav_results + extra + all_concepts + fk_chunks
                    )
    logger.info(
        "Retrieval complete: %d merged chunks (mode=%s).",
        len(merged),
        retrieval_mode,
    )
    if not merged:
        logger.warning("Retrieval returned 0 chunks for query: %.80s", query)

    return {"retrieved_chunks": merged}


def _node_rerank(state: QueryState) -> dict[str, Any]:
    """Rerank retrieved chunks using cross-encoder with quality filtering.

    Applies pre-filtering to remove noise and prioritize structural evidence,
    then optionally applies cross-encoder reranking (bge-reranker-large).
    """
    settings = get_settings()
    query: str = state["user_query"]
    chunks: list[RetrievedChunk] = state.get("retrieved_chunks") or []
    max_pool = max(settings.reranker_top_k * 4, settings.reranker_top_k)
    pool = _pre_filter_rerank_pool(chunks, query=query, max_candidates=max_pool)

    if not settings.enable_reranker:
        candidates = pool[: settings.reranker_top_k]
    else:
        candidates = rerank(query, pool, top_k=settings.reranker_top_k)

    valid = [c for c in candidates if c.node_id.strip() and c.text.strip()]
    if not valid:
        logger.warning(
            "Rerank produced 0 valid chunks (pool=%d, candidates=%d) for query: %.80s",
            len(pool),
            len(candidates),
            query,
        )
        return {
            "reranked_chunks": [],
            "retrieval_quality_score": 0.0,
            "retrieval_chunk_count": 0,
            "retrieval_filtered_by_threshold": False,
            "context_sufficiency": "insufficient",
        }

    top_score = float(valid[0].score)
    if len(valid) == 1:
        sufficiency = "sparse"
    else:
        sufficiency = "adequate"

    return {
        "reranked_chunks": valid,
        "retrieval_quality_score": top_score,
        "retrieval_chunk_count": len(valid),
        "retrieval_filtered_by_threshold": False,
        "context_sufficiency": sufficiency,
    }
