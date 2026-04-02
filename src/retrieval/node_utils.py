"""Node processing utilities for retrieval.

Provides text transformation and processing helpers for Neo4j nodes
used in BM25 indexing and result formatting.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    import logging

    from src.config.logging import get_logger

    logger: logging.Logger = get_logger(__name__)


def _node_to_text(node: dict[str, Any]) -> str:
    """Flatten a node dict to a searchable string for BM25 tokenisation.

    Combines name, definition, synonyms, and column names into a single
    lowercase string suitable for BM25 keyword search.

    Args:
        node: Node property dict with keys like ``name``, ``definition``,
            ``synonyms``, and optionally ``column_names``.

    Returns:
        Lowercase concatenated text string.
    """
    parts = [
        node.get("name") or node.get("text") or "",
        node.get("definition") or "",
        " ".join(node.get("synonyms") or []),
        " ".join(node.get("column_names") or []),
    ]
    return " ".join(p for p in parts if p).lower()
