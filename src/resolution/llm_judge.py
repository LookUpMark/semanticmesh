"""Stage 2 of Agentic Entity Resolution: LLM Canonicalization Judge.

EP-04-US-04-02: For each EntityCluster, calls the LLM judge with the
cluster variants and their provenance texts from the original triplets.
Returns CanonicalEntityDecision (merge/keep separate + canonical name).
"""

from __future__ import annotations

import json
import re
from collections import defaultdict
from typing import TYPE_CHECKING

from langchain_core.messages import HumanMessage, SystemMessage
from pydantic import ValidationError

from src.config.logging import NodeTimer, get_logger
from src.config.settings import get_settings
from src.models.schemas import (
    CanonicalEntityDecision,
    Entity,
    EntityCluster,
    Triplet,
)
from src.prompts.templates import ER_JUDGE_SYSTEM, ER_JUDGE_USER, REFLECTION_TEMPLATE

if TYPE_CHECKING:
    import logging

    from src.config.llm_client import LLMProtocol

logger: logging.Logger = get_logger(__name__)

# Matches optional triple-backtick markdown fences (with or without language tag)
_FENCE_RE = re.compile(r"^```[a-zA-Z]*\n?|```$", re.MULTILINE)


def _clean_json(raw: str) -> str:
    """Strip markdown fences and leading/trailing whitespace from LLM output.

    Many models wrap JSON in ```json ... ``` despite instructions. This strips
    those fences so ``json.loads`` can parse the payload cleanly.
    """
    return _FENCE_RE.sub("", raw).strip()


def _no_merge_decision(cluster: EntityCluster, reasoning: str) -> CanonicalEntityDecision:
    return CanonicalEntityDecision(
        merge=False,
        canonical_name=cluster.canonical_candidate,
        reasoning=reasoning,
    )


def _reflection_prompt(fmt: str, error_or_critique: str, original_input: str) -> str:
    return REFLECTION_TEMPLATE.format(
        role="semantic disambiguation expert",
        output_format=f"JSON object matching {fmt}",
        error_or_critique=error_or_critique,
        original_input=original_input,
    )


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
    settings = get_settings()
    if settings.use_lazy_extraction:
        threshold = float(getattr(settings, "er_judge_threshold", 0.80))
        merge = float(cluster.avg_similarity) >= threshold
        canonical = cluster.canonical_candidate
        logger.info(
            "ER heuristic judge: cluster '%s' avg_similarity=%.3f threshold=%.3f merge=%s",
            cluster.canonical_candidate,
            cluster.avg_similarity,
            threshold,
            merge,
        )
        return CanonicalEntityDecision(
            merge=merge,
            canonical_name=canonical,
            reasoning=(
                f"Heuristic ER decision by similarity threshold: "
                f"{cluster.avg_similarity:.3f} {'>=' if merge else '<'} {threshold:.3f}"
            ),
        )

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
                return _no_merge_decision(
                    cluster,
                    "LLM returned non-string content — conservative no-merge default.",
                )
            raw_json: str = content.strip()
        except Exception as exc:
            logger.warning(
                "LLM judge call failed for cluster %s: %s — defaulting to no-merge.",
                cluster.canonical_candidate,
                exc,
            )
            return _no_merge_decision(cluster, "LLM call failed — conservative no-merge default.")

    logger.debug(
        "ER judge for cluster '%s' completed in %.0f ms",
        cluster.canonical_candidate,
        timer.elapsed_ms,
    )

    _no_merge = _no_merge_decision(cluster, "Conservative no-merge default.")

    # Parse JSON + Pydantic validation with self-reflection on failure
    max_attempts: int = settings.max_reflection_attempts
    _fmt = '{"merge": <bool>, "canonical_name": "<str>", "reasoning": "<str>"}'

    for attempt in range(1, max_attempts + 1):
        try:
            data = json.loads(_clean_json(raw_json))
        except json.JSONDecodeError as exc:
            logger.warning(
                "Non-JSON ER judge response for cluster '%s' (attempt %d/%d): %s",
                cluster.canonical_candidate,
                attempt,
                max_attempts,
                exc,
            )
            if attempt == max_attempts:
                return _no_merge
            raw_json = llm.invoke(
                [HumanMessage(content=_reflection_prompt(_fmt, str(exc), raw_json))]
            ).content.strip()
            continue

        try:
            decision = CanonicalEntityDecision(**data)
        except ValidationError as exc:
            logger.warning(
                "Pydantic validation failed for ER judge cluster '%s' (attempt %d/%d): %s",
                cluster.canonical_candidate,
                attempt,
                max_attempts,
                exc,
            )
            if attempt == max_attempts:
                return _no_merge
            raw_json = llm.invoke(
                [HumanMessage(content=_reflection_prompt(_fmt, str(exc), json.dumps(data)))]
            ).content.strip()
            continue

        logger.info(
            "ER judge: cluster '%s' → merge=%s, canonical='%s'",
            cluster.canonical_candidate,
            decision.merge,
            decision.canonical_name,
        )
        return decision

    return _no_merge


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
        definition="",  # filled by Schema Enrichment / HITL
        synonyms=synonyms,
        provenance_text=provenance_text[:1000],  # cap at 1000 chars for Neo4j property
        source_doc="",  # filled by the node that calls this function
    )
