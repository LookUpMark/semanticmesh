"""Stage 1 of Agentic Entity Resolution: Vector Blocking.

EP-04-US-04-01: Embeds all unique entity strings with BGE-M3, then uses
cosine similarity to group near-duplicate pairs into EntityCluster objects.
Only clusters with >= 2 variants proceed to the LLM judge (Stage 2).
"""

from __future__ import annotations

from collections import defaultdict
from typing import TYPE_CHECKING, Any

import numpy as np

from src.config.logging import get_logger
from src.config.settings import get_settings
from src.models.schemas import EntityCluster, Triplet
from src.retrieval.embeddings import embed_texts
from src.utils.text_utils import is_valid_entity_name

if TYPE_CHECKING:
    import logging

logger: logging.Logger = get_logger(__name__)
_settings = get_settings()


def extract_unique_entities(triplets: list[Triplet]) -> list[str]:
    """Extract all unique entity strings (subjects + objects) from triplets.

    Applies ``is_valid_entity_name`` to reject obvious noise (stopwords-only,
    sentence fragments, purely numeric values) before expensive downstream steps.

    Args:
        triplets: All triplets extracted by the SLM across all chunks.

    Returns:
        Sorted list of unique, non-empty, quality-filtered entity strings.
    """
    entities: set[str] = set()
    rejected: int = 0
    for t in triplets:
        if t.subject.strip():
            if is_valid_entity_name(t.subject):
                entities.add(t.subject.strip())
            else:
                rejected += 1
        if t.object.strip():
            if is_valid_entity_name(t.object):
                entities.add(t.object.strip())
            else:
                rejected += 1
    unique = sorted(entities)
    if rejected:
        logger.info(
            "Filtered %d low-quality entity names before blocking.", rejected
        )
    logger.info("Extracted %d unique entities from %d triplets.", len(unique), len(triplets))
    return unique


def _split_oversized_cluster(
    member_indices: list[int],
    entities: list[str],
    local_sim: np.ndarray,
    max_size: int,
    base_threshold: float,
) -> list[EntityCluster]:
    """Split an oversized Union-Find component into tighter sub-clusters.

    Uses progressively higher similarity thresholds to re-cluster the members
    until all sub-clusters are within ``max_size``. Members that don't fit
    into any tight sub-cluster are promoted to singletons (dropped).

    Args:
        member_indices: Indices of entities in the oversized component.
        entities: Full entity list (for name lookup).
        sim_matrix: Pre-computed cosine similarity matrix.
        max_size: Maximum allowed cluster size.
        base_threshold: Original similarity threshold used in blocking.

    Returns:
        List of ``EntityCluster`` objects, each within ``max_size``.
    """
    idx_arr = np.array(member_indices)
    sub_sim = local_sim
    n_sub = len(member_indices)

    # Re-cluster with a tighter threshold (step up by 0.05 each iteration)
    threshold = base_threshold + get_settings().er_threshold_step
    max_iterations = get_settings().er_recluster_max_iterations

    for _ in range(max_iterations):
        # Fresh Union-Find on sub-matrix
        parent = list(range(n_sub))

        def find(i: int) -> int:
            while parent[i] != i:
                parent[i] = parent[parent[i]]
                i = parent[i]
            return i

        def union(i: int, j: int) -> None:
            ri, rj = find(i), find(j)
            if ri != rj:
                parent[ri] = rj

        for i in range(n_sub):
            for j in range(i + 1, n_sub):
                if sub_sim[i, j] >= threshold:
                    union(i, j)

        sub_groups: dict[int, list[int]] = defaultdict(list)
        for i in range(n_sub):
            sub_groups[find(i)].append(i)

        # Check if all groups are within max_size
        all_ok = all(len(g) <= max_size for g in sub_groups.values())
        if all_ok:
            break
        threshold += get_settings().er_threshold_step

    # Build EntityCluster objects from the sub-groups
    result: list[EntityCluster] = []
    for local_indices in sub_groups.values():
        if len(local_indices) < 2:
            continue
        # Cap at max_size: take the top-N most mutually similar
        if len(local_indices) > max_size:
            # Pick the `max_size` members with highest average pairwise sim
            local_arr = np.array(local_indices)
            cap_sim = sub_sim[np.ix_(local_arr, local_arr)]
            avg_sims = cap_sim.mean(axis=1)
            top_local = np.argsort(avg_sims)[::-1][:max_size]
            local_indices = [local_indices[i] for i in top_local]

        global_indices = [member_indices[li] for li in local_indices]
        variants = [entities[gi] for gi in global_indices]
        canonical = max(variants, key=len)

        l_arr = np.array(local_indices)
        g_sub = sub_sim[np.ix_(l_arr, l_arr)]
        n_m = len(local_indices)
        if n_m > 1:
            mask = ~np.eye(n_m, dtype=bool)
            avg_sim = float(g_sub[mask].mean())
        else:
            avg_sim = 1.0

        result.append(
            EntityCluster(
                canonical_candidate=canonical,
                variants=variants,
                avg_similarity=round(avg_sim, 4),
            )
        )

    logger.info(
        "Split oversized cluster (%d members) → %d sub-clusters (threshold=%.2f).",
        len(member_indices),
        len(result),
        threshold,
    )
    return result


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

    # Normalize for efficient cosine via dot product
    norms = np.linalg.norm(vectors, axis=1, keepdims=True)
    norms[norms == 0] = 1.0
    vectors_normed = vectors / norms

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

    # Batched top-k: process in chunks to limit peak memory
    n = len(entities)
    effective_k = min(k, n - 1)  # can't select more neighbors than exist
    batch_size = min(256, n)
    for start in range(0, n, batch_size):
        end = min(start + batch_size, n)
        # (batch, dim) @ (dim, n) → (batch, n) similarities
        sims_batch = vectors_normed[start:end] @ vectors_normed.T
        for local_i in range(end - start):
            i = start + local_i
            row = sims_batch[local_i]
            row[i] = -1.0  # exclude self
            candidate_indices = np.argpartition(row, -effective_k)[-effective_k:]
            for j in candidate_indices:
                if row[j] >= sim_threshold:
                    union(i, j)

    groups: dict[int, list[int]] = defaultdict(list)
    for i in range(n):
        groups[find(i)].append(i)

    max_cluster_size: int = _settings.er_max_cluster_size

    clusters: list[EntityCluster] = []
    for member_indices in groups.values():
        if len(member_indices) < 2:
            continue

        # ── Over-sized cluster protection ─────────────────────────────────────
        # Transitive chaining in Union-Find can produce monster clusters
        # (e.g., "Customer" absorbing 100+ loosely-related terms).
        # Split oversized clusters into tighter sub-groups using a higher threshold.
        if len(member_indices) > max_cluster_size:
            # Compute sub-matrix on demand (only for oversized clusters)
            idx_arr = np.array(member_indices)
            sub_vecs = vectors_normed[idx_arr]
            local_sim = sub_vecs @ sub_vecs.T
            sub_clusters = _split_oversized_cluster(
                member_indices, entities, local_sim, max_cluster_size, sim_threshold
            )
            clusters.extend(sub_clusters)
            continue

        variants = [entities[i] for i in member_indices]

        canonical = max(variants, key=len)

        idx_arr = np.array(member_indices)
        sub_vecs = vectors_normed[idx_arr]
        sub_matrix = sub_vecs @ sub_vecs.T
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
