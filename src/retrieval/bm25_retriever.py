"""BM25 keyword retrieval module.

EP-12 / US-12-02: Implements BM25 keyword search over node text corpus
using rank-bm25 library. Provides index building and search functionality.
"""

from __future__ import annotations

import threading
from typing import TYPE_CHECKING, Any

from src.config.logging import get_logger
from src.config.settings import get_settings
from src.models.schemas import RetrievedChunk
from src.retrieval.node_utils import _node_to_text

if TYPE_CHECKING:
    import logging

logger: logging.Logger = get_logger(__name__)

# ── BM25 Object Cache ─────────────────────────────────────────────────────────
# Caches the BM25Okapi object alongside the node corpus to avoid rebuilding
# the tokenized index on every query. Invalidated together with the node-index.
_BM25_CACHE: Any = None  # BM25Okapi instance
_BM25_CORPUS_ID: int = 0  # id() of the all_nodes list used to build cache
_BM25_LOCK = threading.Lock()


def invalidate_bm25_cache() -> None:
    """Invalidate the in-memory BM25 node-index cache.

    Delegates to :func:`src.retrieval.hybrid_retriever.invalidate_bm25_cache`.
    This thin wrapper is imported by ``builder_graph`` to avoid a circular import
    (hybrid_retriever imports bm25_retriever; builder_graph imports bm25_retriever).
    """
    global _BM25_CACHE, _BM25_CORPUS_ID  # noqa: PLW0603
    with _BM25_LOCK:
        _BM25_CACHE = None
        _BM25_CORPUS_ID = 0
    from src.retrieval.hybrid_retriever import (  # local import breaks cycle
        invalidate_bm25_cache as _invalidate,
    )

    _invalidate()


# ── DDL Query Expansion ────────────────────────────────────────────────────────
# When a query mentions status/constraint-related terms, inject DDL keywords
# so BM25 can find chunks containing column definitions and CHECK constraints.

_DDL_EXPANSION_MAP: dict[str, list[str]] = {
    "status": ["status_code", "pending", "confirmed", "cancelled", "check"],
    "statuses": ["status_code", "pending", "confirmed", "cancelled", "check"],
    "constraint": ["check", "constraint", "unique", "foreign", "not"],
    "type": ["varchar", "integer", "decimal", "bigint", "boolean", "date"],
    "enum": ["check", "status_code", "type_code"],
    "values": ["check", "pending", "confirmed", "cancelled"],
    "nullable": ["null", "not", "nullable", "yes", "no"],
    "payment": ["payment_method", "amount", "status_code", "confirmed_at"],
    "confirmation": ["confirmed_at", "confirmed", "status_code", "pending"],
}


def _expand_query_tokens(tokens: list[str]) -> list[str]:
    """Expand BM25 query tokens with DDL-related synonyms for better recall."""
    expanded = list(tokens)
    for token in tokens:
        clean = token.strip("?.,!;:")
        if clean in _DDL_EXPANSION_MAP:
            expanded.extend(_DDL_EXPANSION_MAP[clean])
    return expanded


def bm25_search(
    query: str,
    all_nodes: list[dict[str, Any]],
    top_k: int | None = None,
) -> list[RetrievedChunk]:
    """Keyword retrieval using BM25Okapi over a pre-built node text corpus.

    Args:
        query: Natural language query string.
        all_nodes: Node dump from ``build_node_index``.
        top_k: Number of results; defaults to ``settings.retrieval_bm25_top_k``.

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

    # Use cached BM25 object if the node list hasn't changed (same id())
    global _BM25_CACHE, _BM25_CORPUS_ID  # noqa: PLW0603
    corpus_id = id(all_nodes)
    with _BM25_LOCK:
        if _BM25_CACHE is not None and corpus_id == _BM25_CORPUS_ID:
            bm25 = _BM25_CACHE
        else:
            corpus_texts: list[str] = [_node_to_text(node) for node in all_nodes]
            tokenised_corpus = [text.split() for text in corpus_texts]
            bm25 = BM25Okapi(tokenised_corpus)
            _BM25_CACHE = bm25
            _BM25_CORPUS_ID = corpus_id
            logger.debug("bm25_search: rebuilt BM25 index (%d docs).", len(all_nodes))

    tokenised_query = _expand_query_tokens(query.lower().split())
    scores: list[float] = bm25.get_scores(tokenised_query).tolist()

    indexed = sorted(enumerate(scores), key=lambda x: x[1], reverse=True)[:n]
    chunks: list[RetrievedChunk] = []
    for idx, score in indexed:
        node = all_nodes[idx]
        node_type = node.get("node_type", "BusinessConcept")
        # ParentChunk nodes carry raw text; other nodes use name + definition
        if node_type == "ParentChunk":
            raw_text = (node.get("text") or "").strip()
            if not raw_text:
                continue
            chunk_idx = node.get("chunk_index", 0)
            src = node.get("source_doc") or ""
            chunks.append(
                RetrievedChunk(
                    node_id=f"parent_chunk_{src}_{chunk_idx}",
                    node_type="ParentChunk",
                    text=raw_text,
                    score=score,
                    source_type="bm25",
                    metadata={"chunk_index": chunk_idx, "source_doc": src},
                )
            )
        else:
            name = (node.get("name") or "").strip()
            definition = node.get("definition") or ""
            if not name:
                continue
            text = f"{name}: {definition}" if definition else name
            chunks.append(
                RetrievedChunk(
                    node_id=name,
                    node_type=node_type,
                    text=text,
                    score=score,
                    source_type="bm25",
                    metadata={
                        key: val for key, val in node.items() if key not in ("name", "definition")
                    },
                )
            )
    logger.debug("bm25_search: %d results for query '%s'.", len(chunks), query[:60])
    return chunks
