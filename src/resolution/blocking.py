"""Stage 1 of Agentic Entity Resolution: Vector Blocking.

EP-04-US-04-01: Embeds all unique entity strings with BGE-M3, then uses
cosine similarity to group near-duplicate pairs into EntityCluster objects.
Only clusters with >= 2 variants proceed to the LLM judge (Stage 2).
"""

from __future__ import annotations

from collections import defaultdict
from typing import TYPE_CHECKING, Any

import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

from src.config.logging import get_logger
from src.config.settings import get_settings
from src.models.schemas import EntityCluster, Triplet
from src.retrieval.embeddings import embed_texts

if TYPE_CHECKING:
    import logging

logger: logging.Logger = get_logger(__name__)
_settings = get_settings()


def extract_unique_entities(triplets: list[Triplet]) -> list[str]:
    """Extract all unique entity strings (subjects + objects) from triplets.

    Args:
        triplets: All triplets extracted by the SLM across all chunks.

    Returns:
        Sorted list of unique, non-empty entity strings.
    """
    entities: set[str] = set()
    for t in triplets:
        if t.subject.strip():
            entities.add(t.subject.strip())
        if t.object.strip():
            entities.add(t.object.strip())
    unique = sorted(entities)
    logger.info("Extracted %d unique entities from %d triplets.", len(unique), len(triplets))
    return unique


def block_entities(
    entities: list[str],
    embeddings: Any,
    threshold: float | None = None,
    top_k: int | None = None,
) -> list[EntityCluster]:
    """Group semantically similar entity strings into candidate clusters.

    Uses Union-Find clustering on cosine similarity matrix to merge
    near-duplicate variants. Only clusters with >= 2 variants are returned.

    Args:
        entities: Unique entity strings (from ``extract_unique_entities``).
        embeddings: Any ``Embeddings`` instance (BGE-M3 recommended).
        threshold: Minimum cosine similarity to form a cluster pair.
                   Defaults to ``settings.er_similarity_threshold``.
        top_k: Maximum number of candidates per entity for initial pruning.
               Defaults to ``settings.er_blocking_top_k``.

    Returns:
        List of ``EntityCluster`` objects (only clusters with >= 2 variants).
    """
    if not entities:
        return []

    sim_threshold = threshold if threshold is not None else _settings.er_similarity_threshold
    k = top_k if top_k is not None else _settings.er_blocking_top_k

    logger.info("Embedding %d entities for blocking...", len(entities))
    vectors = np.array(embed_texts(entities, model=embeddings), dtype=np.float32)

    sim_matrix = cosine_similarity(vectors)

    parent = list(range(len(entities)))

    def find(i: int) -> int:
        while parent[i] != i:
            parent[i] = parent[parent[i]]
            i = parent[i]
        return i

    def union(i: int, j: int) -> None:
        ri, rj = find(i), find(j)
        if ri != rj:
            parent[ri] = rj

    n = len(entities)
    for i in range(n):
        sims = sim_matrix[i]
        candidate_indices = np.argsort(sims)[::-1][:k]
        for j in candidate_indices:
            if i != j and sims[j] >= sim_threshold:
                union(i, j)

    groups: dict[int, list[int]] = defaultdict(list)
    for i in range(n):
        groups[find(i)].append(i)

    clusters: list[EntityCluster] = []
    for member_indices in groups.values():
        if len(member_indices) < 2:
            continue

        variants = [entities[i] for i in member_indices]

        canonical = max(variants, key=len)

        idx_arr = np.array(member_indices)
        sub_matrix = sim_matrix[np.ix_(idx_arr, idx_arr)]
        n_members = len(member_indices)
        if n_members > 1:
            mask = ~np.eye(n_members, dtype=bool)
            avg_sim = float(sub_matrix[mask].mean())
        else:
            avg_sim = 1.0

        clusters.append(
            EntityCluster(
                canonical_candidate=canonical,
                variants=variants,
                avg_similarity=round(avg_sim, 4),
            )
        )

    logger.info(
        "Blocking complete: %d clusters from %d entities (threshold=%.2f).",
        len(clusters),
        len(entities),
        sim_threshold,
    )
    return clusters
