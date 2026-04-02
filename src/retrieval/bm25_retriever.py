"""BM25 keyword retrieval module.

EP-12 / US-12-02: Implements BM25 keyword search over node text corpus
using rank-bm25 library. Provides index building and search functionality.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from src.config.logging import get_logger
from src.config.settings import get_settings
from src.models.schemas import RetrievedChunk
from src.retrieval.node_utils import _node_to_text

if TYPE_CHECKING:
    import logging

logger: logging.Logger = get_logger(__name__)


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

    corpus_texts: list[str] = [_node_to_text(node) for node in all_nodes]
    tokenised_corpus = [text.split() for text in corpus_texts]
    bm25 = BM25Okapi(tokenised_corpus)

    tokenised_query = query.lower().split()
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
