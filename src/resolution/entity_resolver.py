"""Full two-stage Agentic Entity Resolution pipeline.

EP-04: Orchestrates Stage 1 (vector blocking) and Stage 2 (LLM judge)
to produce a deduplicated, canonical list of Entity objects.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from langchain_core.embeddings import Embeddings  # noqa: TC002 (used at runtime)

from src.config.logging import get_logger
from src.models.schemas import Entity, Triplet
from src.resolution.blocking import block_entities, extract_unique_entities
from src.resolution.llm_judge import (
    build_provenance_map,
    cluster_to_entity,
    judge_cluster,
)

if TYPE_CHECKING:
    import logging

    from src.config.llm_client import LLMProtocol

logger: logging.Logger = get_logger(__name__)


def resolve_entities(
    triplets: list[Triplet],
    embeddings: Embeddings,
    llm: LLMProtocol,
    source_doc: str = "",
) -> list[Entity]:
    """Run the full two-stage entity resolution pipeline.

    Stage 1: Vector blocking — embed all entity strings, group near-duplicate
             pairs into ``EntityCluster`` objects using cosine similarity.

    Stage 2: LLM judge — for each cluster, call ``judge_cluster`` to decide
             whether the variants should merge into one canonical entity.

    Singletons (not in any cluster) are promoted directly to ``Entity``
    objects without an LLM call, preserving all extracted facts.

    Args:
        triplets: All triplets from the SLM extraction step.
        embeddings: Embedding model (BGE-M3 recommended).
        llm: Reasoning LLM for the judge step (temperature=0.0).
        source_doc: Source document name (stored on each Entity for provenance).

    Returns:
        List of canonical ``Entity`` objects, deduplicated and ready for
        embedding and storage in BuilderState.canonical_entities.
    """
    if not triplets:
        logger.warning("resolve_entities called with empty triplet list — returning empty.")
        return []

    # ── Stage 1: Blocking ──────────────────────────────────────────────────────
    all_entities = extract_unique_entities(triplets)
    clusters = block_entities(all_entities, embeddings)

    # Track which entities are covered by a cluster
    clustered_entities: set[str] = set()
    for cluster in clusters:
        clustered_entities.update(cluster.variants)

    # ── Stage 2: LLM Judge ────────────────────────────────────────────────────
    provenance_map = build_provenance_map(triplets)
    canonical_entities: list[Entity] = []

    for cluster in clusters:
        decision = judge_cluster(cluster, provenance_map, llm)
        entity = cluster_to_entity(cluster, decision, provenance_map)
        entity.source_doc = source_doc
        canonical_entities.append(entity)

    # ── Singletons: promote directly ──────────────────────────────────────────
    singleton_entities = [e for e in all_entities if e not in clustered_entities]
    for singleton in singleton_entities:
        provenance_texts = provenance_map.get(singleton, [])
        canonical_entities.append(
            Entity(
                name=singleton,
                definition="",
                synonyms=[],
                provenance_text=" | ".join(provenance_texts[:3]),  # cap at 3
                source_doc=source_doc,
            )
        )

    logger.info(
        "Entity resolution complete: %d clusters resolved, %d singletons "
        "promoted → %d total entities.",
        len(clusters),
        len(singleton_entities),
        len(canonical_entities),
    )
    return canonical_entities
