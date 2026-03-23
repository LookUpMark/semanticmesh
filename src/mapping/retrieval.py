"""Retrieval utilities for semantic mapping.

This module provides embedding-based retrieval functions for finding relevant
business entities (concepts) during the RAG mapping process. It separates
the pure retrieval logic from the LLM-based mapping logic.
"""

from __future__ import annotations

from typing import Any

import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

from src.config.logging import get_logger
from src.config.settings import get_settings
from src.models.schemas import EnrichedTableSchema, Entity
from src.retrieval.embeddings import embed_text, embed_texts

_settings = get_settings()
logger = get_logger(__name__)


def build_retrieval_query(table: EnrichedTableSchema) -> str:
    """Construct a dense retrieval query from enriched table metadata.

    Priority order for metadata:
    1. enriched_table_name + table_description (if available)
    2. Fallback to original table_name + column names

    The richer this query, the better the embedding similarity with business
    concepts defined in natural language.

    Args:
        table: EnrichedTableSchema (may have enrichment fields as None if
               enrichment failed — graceful degradation).

    Returns:
        A plain-text query string for embedding.
    """
    parts: list[str] = []

    # Prefer enriched name + description
    if table.enriched_table_name:
        parts.append(table.enriched_table_name)
    else:
        parts.append(table.table_name)

    if table.table_description:
        parts.append(table.table_description)

    # Add enriched column names if available
    if table.enriched_columns:
        col_names = [ec.enriched_name for ec in table.enriched_columns]
    else:
        col_names = [c.name for c in table.columns if not c.is_primary_key]

    parts.append(", ".join(col_names[:10]))  # cap at 10 columns
    return " | ".join(parts)


def retrieve_top_entities(
    query: str,
    entities: list[Entity],
    embeddings: Any,
    top_k: int | None = None,
) -> list[Entity]:
    """Retrieve the most semantically relevant entities for a given table query.

    Constructs embedding text for each entity as ``"{name}: {definition}"``.
    Uses cosine similarity against the query embedding.

    Args:
        query: Plain-text retrieval query (from ``build_retrieval_query``).
        entities: All canonical entities from entity resolution.
        embeddings: Embedding model (BGE-M3).
        top_k: Maximum number of entities to return.
               Defaults to ``settings.retrieval_vector_top_k``.

    Returns:
        Top-k most similar ``Entity`` objects, sorted by descending similarity.
    """
    k = top_k if top_k is not None else _settings.retrieval_vector_top_k
    if not entities:
        return []

    query_vec = np.array(embed_text(query, model=embeddings), dtype=np.float32).reshape(1, -1)

    entity_texts = [f"{e.name}: {e.definition}" if e.definition else e.name for e in entities]
    entity_vecs = np.array(embed_texts(entity_texts, model=embeddings), dtype=np.float32)

    sims = cosine_similarity(query_vec, entity_vecs)[0]
    top_indices = np.argsort(sims)[::-1][:k]

    return [entities[i] for i in top_indices]
