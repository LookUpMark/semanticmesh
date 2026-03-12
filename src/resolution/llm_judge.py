"""Stage 2 of Agentic Entity Resolution: LLM Canonicalization Judge.

EP-04-US-04-02: For each EntityCluster, calls the LLM judge with the
cluster variants and their provenance texts from the original triplets.
Returns CanonicalEntityDecision (merge/keep separate + canonical name).
"""

from __future__ import annotations

import json
from collections import defaultdict
from typing import TYPE_CHECKING

from langchain_core.messages import HumanMessage, SystemMessage
from pydantic import ValidationError

from src.config.logging import NodeTimer, get_logger
from src.models.schemas import (
    CanonicalEntityDecision,
    Entity,
    EntityCluster,
    Triplet,
)
from src.prompts.templates import ER_JUDGE_SYSTEM, ER_JUDGE_USER

if TYPE_CHECKING:
    import logging

    from src.config.llm_client import LLMProtocol

logger: logging.Logger = get_logger(__name__)


def build_provenance_map(triplets: list[Triplet]) -> dict[str, list[str]]:
    """Build a mapping from entity string → list of provenance texts.

    Both subjects and objects of every triplet are included.  Used to
    provide the LLM judge with grounding context for each entity variant.

    Args:
        triplets: All triplets from SLM extraction.

    Returns:
        Dict mapping ``entity_string → [provenance_text_1, ...]``.
        Multiple triplets may contribute provenance for the same entity.
    """
    provenance: dict[str, list[str]] = defaultdict(list)
    for t in triplets:
        if t.subject.strip():
            provenance[t.subject.strip()].append(t.provenance_text)
        if t.object.strip():
            provenance[t.object.strip()].append(t.provenance_text)
    return dict(provenance)


def judge_cluster(
    cluster: EntityCluster,
    provenance_map: dict[str, list[str]],
    llm: LLMProtocol,
) -> CanonicalEntityDecision:
    """Call the LLM judge for a single EntityCluster.

    Args:
        cluster: Candidate cluster from Stage 1 blocking.
        provenance_map: Maps entity string → provenance texts (from ``build_provenance_map``).
        llm: Reasoning-class LLM (use ``get_reasoning_llm()``).

    Returns:
        ``CanonicalEntityDecision`` with ``merge`` flag and ``canonical_name``.
        On any failure, returns a conservative "do not merge" decision to
        preserve information (never crashes the pipeline).
    """
    # Build the two JSON structures for the prompt
    variants_json = json.dumps(cluster.variants)
    provenance_entries = []
    for variant in cluster.variants:
        contexts = provenance_map.get(variant, ["<no provenance available>"])
        # Use first 2 provenance texts max to keep prompt bounded
        provenance_entries.append({"variant": variant, "context": " | ".join(contexts[:2])})
    provenance_json = json.dumps(provenance_entries)

    user_prompt = ER_JUDGE_USER.format(
        variants_json=variants_json,
        provenance_json=provenance_json,
    )

    with NodeTimer() as timer:
        try:
            response = llm.invoke(
                [
                    SystemMessage(content=ER_JUDGE_SYSTEM),
                    HumanMessage(content=user_prompt),
                ]
            )
            content = response.content
            if not isinstance(content, str):
                logger.warning(
                    "LLM returned non-string content for cluster %s — returning no-merge decision.",
                    cluster.canonical_candidate,
                )
                return CanonicalEntityDecision(
                    merge=False,
                    canonical_name=cluster.canonical_candidate,
                    reasoning="LLM returned non-string content — conservative no-merge default.",
                )
            raw_json: str = content.strip()
        except Exception as exc:
            logger.warning(
                "LLM judge call failed for cluster %s: %s — defaulting to no-merge.",
                cluster.canonical_candidate, exc,
            )
            return CanonicalEntityDecision(
                merge=False,
                canonical_name=cluster.canonical_candidate,
                reasoning="LLM call failed — conservative no-merge default.",
            )

    logger.debug(
        "ER judge for cluster '%s' completed in %.0f ms",
        cluster.canonical_candidate, timer.elapsed_ms,
    )

    # Parse JSON
    try:
        data = json.loads(raw_json)
    except json.JSONDecodeError as exc:
        logger.warning("Non-JSON ER judge response: %s — defaulting to no-merge.", exc)
        return CanonicalEntityDecision(
            merge=False,
            canonical_name=cluster.canonical_candidate,
            reasoning="JSON parse error — conservative no-merge default.",
        )

    # Validate with Pydantic
    try:
        decision = CanonicalEntityDecision(**data)
    except ValidationError as exc:
        logger.warning("Pydantic validation failed for ER judge response: %s", exc)
        return CanonicalEntityDecision(
            merge=False,
            canonical_name=cluster.canonical_candidate,
            reasoning="Pydantic validation error — conservative no-merge default.",
        )

    logger.info(
        "ER judge: cluster '%s' → merge=%s, canonical='%s'",
        cluster.canonical_candidate, decision.merge, decision.canonical_name,
    )
    return decision


def cluster_to_entity(
    cluster: EntityCluster,
    decision: CanonicalEntityDecision,
    provenance_map: dict[str, list[str]],
) -> Entity:
    """Convert a cluster + judge decision into a canonical Entity object.

    Args:
        cluster: The ``EntityCluster`` from Stage 1.
        decision: The ``CanonicalEntityDecision`` from the LLM judge.
        provenance_map: For building provenance and synonyms.

    Returns:
        A ``Entity`` ready to be stored in ``BuilderState.canonical_entities``.
    """
    canonical = decision.canonical_name if decision.merge else cluster.canonical_candidate
    synonyms = [v for v in cluster.variants if v != canonical]

    # Collect provenance texts for the canonical entity
    all_provenance: list[str] = provenance_map.get(canonical, [])
    for variant in synonyms:
        all_provenance.extend(provenance_map.get(variant, []))
    provenance_text = " | ".join(dict.fromkeys(all_provenance))  # deduplicated, order-preserving

    return Entity(
        name=canonical,
        definition="",          # filled by Schema Enrichment / HITL
        synonyms=synonyms,
        provenance_text=provenance_text[:1000],  # cap at 1000 chars for Neo4j property
        source_doc="",          # filled by the node that calls this function
    )
