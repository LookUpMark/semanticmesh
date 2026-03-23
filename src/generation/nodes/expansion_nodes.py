"""Context distillation and lazy expansion nodes.

Nodes:
- _node_context_distillation: LLM-based chunk filtering for query relevance
- _node_lazy_expansion: On-demand FK relationship fetching
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from src.config.logging import get_logger
from src.config.settings import get_settings
from src.generation.context_distiller import distill_context_chunks
from src.generation.lazy_expander import (
    collect_seed_names_for_expansion,
)
from src.graph.neo4j_client import Neo4jClient
from src.models.schemas import RetrievedChunk
from src.models.state import QueryState
from src.retrieval.hybrid_retriever import fetch_fk_relationships, graph_traversal

if TYPE_CHECKING:
    import logging

logger: logging.Logger = get_logger(__name__)


# ── Helper Functions ──


def _extract_relation_tokens(query: str) -> set[str]:
    relation_keywords = {
        "related",
        "relationship",
        "linked",
        "link",
        "connect",
        "connection",
        "join",
        "reference",
        "foreign",
        "parent",
        "child",
    }
    query_lower = query.lower()
    return {word for word in relation_keywords if word in query_lower}


def _get_source_caps(target: int) -> dict[str, int]:
    return {
        "vector": min(4, target),
        "bm25": min(4, target),
        "graph": min(5, target),
    }


def _should_fetch_fk_edges(query: str, chunks: list[RetrievedChunk]) -> bool:
    relation_tokens = _extract_relation_tokens(query)
    has_explicit_relation_request = len(relation_tokens) > 0
    has_fk_evidence = any("→" in c.node_id for c in chunks)
    return has_explicit_relation_request and not has_fk_evidence


def _combine_chunks(*chunk_lists: list[RetrievedChunk]) -> list[RetrievedChunk]:
    seen: set[str] = set()
    combined: list[RetrievedChunk] = []
    for chunks in chunk_lists:
        for chunk in chunks:
            if chunk.node_id not in seen:
                seen.add(chunk.node_id)
                combined.append(chunk)
    return combined


# ── Node Implementations ──


def _node_context_distillation(state: QueryState) -> dict[str, Any]:
    """Distill context chunks to query-relevant subset using LLM.

    Reduces context window by filtering out chunks that don't contribute
    to answering the specific query, improving focus and reducing hallucination risk.
    """
    query: str = state["user_query"]
    chunks: list[RetrievedChunk] = state.get("reranked_chunks") or []

    from src.generation.nodes.generation_nodes import _compose_generation_chunks

    composed = _compose_generation_chunks(query, chunks)
    distilled = distill_context_chunks(query, composed, max_chunks=len(composed) or 0)
    if distilled:
        logger.info(
            "Context distillation: composed=%d -> distilled=%d chunk(s).",
            len(composed),
            len(distilled),
        )
    return {"generation_chunks": distilled or composed}


def _node_lazy_expansion(state: QueryState) -> dict[str, Any]:
    """Lazy expansion: fetch FK relationships on-demand when needed.

    Triggered when:
    1. Query contains relationship keywords
    2. Current chunks lack FK edge evidence
    3. Lazy expansion is enabled in settings
    """
    settings = get_settings()
    if not getattr(settings, "enable_lazy_expansion", False):
        return {}

    query: str = state["user_query"]
    chunks: list[RetrievedChunk] = state.get("reranked_chunks") or []

    if not _should_fetch_fk_edges(query, chunks):
        return {}

    logger.info("Lazy expansion triggered: fetching FK relationships for query.")
    with Neo4jClient() as client:
        seeds = collect_seed_names_for_expansion(chunks, limit=8)
        if not seeds:
            return {}

        fk_chunks = fetch_fk_relationships(client)

        expanded = graph_traversal(
            seed_names=seeds,
            client=client,
            depth=max(1, settings.retrieval_graph_depth + 1),
        )

        new_chunks = _combine_chunks(chunks, fk_chunks, expanded)

        logger.info(
            "Lazy expansion: added %d FK chunks + %d graph traversal chunks.",
            len(fk_chunks),
            len(expanded),
        )

        return {"reranked_chunks": new_chunks}
