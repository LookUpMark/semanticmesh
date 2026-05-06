"""Full two-stage Agentic Entity Resolution pipeline.

EP-04: Orchestrates Stage 1 (vector blocking) and Stage 2 (LLM judge)
to produce a deduplicated, canonical list of Entity objects.
"""

from __future__ import annotations

import json
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import TYPE_CHECKING, Any

from langchain_core.messages import HumanMessage, SystemMessage

from src.config.logging import get_logger
from src.config.settings import get_settings
from src.models.schemas import Entity, Triplet
from src.prompts.templates import ENTITY_DEFINITION_SYSTEM, ENTITY_DEFINITION_USER
from src.resolution.blocking import block_entities, extract_unique_entities
from src.resolution.llm_judge import (
    build_provenance_map,
    cluster_to_entity,
    judge_cluster,
)
from src.utils.json_utils import clean_json, extract_text_content
from src.utils.text_utils import normalize_concept_name

if TYPE_CHECKING:
    import logging

    from src.config.llm_client import LLMProtocol

logger: logging.Logger = get_logger(__name__)


def _infer_singleton_definition(
    entity_name: str,
    provenance_texts: list[str],
    llm: LLMProtocol,
) -> str:
    """Synthesize a one-sentence definition for a singleton entity via the LLM.

    Uses the ENTITY_DEFINITION_SYSTEM/USER prompts to produce a concise,
    human-readable definition grounded in provenance context.  Falls back
    to the first raw provenance sentence on any failure.

    Args:
        entity_name: Canonical entity name string.
        provenance_texts: Context sentences from the original triplets.
        llm: Lightweight LLM (nano model) to keep cost minimal.

    Returns:
        A one-sentence definition string, or the first provenance sentence
        as a fallback when the LLM call fails.
    """
    if not provenance_texts:
        return entity_name
    provenance_joined = " | ".join(provenance_texts[:3])
    user_msg = ENTITY_DEFINITION_USER.format(
        entity_name=entity_name,
        provenance_text=provenance_joined,
    )
    try:
        response = llm.invoke(
            [
                SystemMessage(content=ENTITY_DEFINITION_SYSTEM),
                HumanMessage(content=user_msg),
            ]
        )
        raw = clean_json(extract_text_content(response.content))
        data = json.loads(raw)
        definition = data.get("definition") or ""
        return str(definition) if definition else provenance_texts[0]
    except Exception as exc:
        logger.debug(
            "Definition inference failed for '%s': %s — using provenance fallback.",
            entity_name,
            exc,
        )
        return provenance_texts[0]


def _infer_singleton_definitions_batch(
    singleton_data: list[tuple[str, list[str]]],
    llm: LLMProtocol,
    concurrency: int = 5,
) -> dict[str, str]:
    """Batch-synthesize definitions for multiple singleton entities in parallel.

    Args:
        singleton_data: List of (entity_name, provenance_texts) pairs.
        llm: Lightweight LLM used for synthesis.
        concurrency: Max parallel LLM calls (default 5 to respect rate limits).

    Returns:
        Dict mapping entity_name → synthesized definition string.
    """
    # Only call LLM for entities that have provenance context to work from
    callables = [(name, texts) for name, texts in singleton_data if texts]
    if not callables:
        return {}

    logger.info(
        "Synthesizing definitions for %d singleton entities (concurrency=%d).",
        len(callables),
        concurrency,
    )
    results: dict[str, str] = {}
    with ThreadPoolExecutor(max_workers=concurrency) as pool:
        futures = {
            pool.submit(_infer_singleton_definition, name, texts, llm): name
            for name, texts in callables
        }
        for future in as_completed(futures):
            name = futures[future]
            try:
                results[name] = future.result()
            except Exception as exc:
                logger.debug("Definition batch item failed for '%s': %s", name, exc)
                results[name] = ""
    return results


def resolve_entities(
    triplets: list[Triplet],
    embeddings: Any,
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

    # ── Stage 2: LLM Judge (parallelised) ───────────────────────────────────
    provenance_map = build_provenance_map(triplets)
    canonical_entities: list[Entity] = []

    if clusters:
        settings_er = get_settings()
        concurrency = settings_er.extraction_concurrency
        # Use midtier LLM for the judge (binary merge task, no full reasoning tier needed)
        from src.config.llm_factory import get_midtier_llm as _get_midtier_llm

        judge_llm = _get_midtier_llm()
        cluster_results: dict[int, Entity] = {}
        with ThreadPoolExecutor(max_workers=min(concurrency, len(clusters))) as pool:
            future_to_idx = {
                pool.submit(judge_cluster, cluster, provenance_map, judge_llm): i
                for i, cluster in enumerate(clusters)
            }
            for future in as_completed(future_to_idx):
                i = future_to_idx[future]
                cluster = clusters[i]
                try:
                    decision = future.result()
                except Exception as exc:
                    logger.warning(
                        "LLM judge failed for cluster '%s': %s", cluster.canonical_candidate, exc
                    )
                    from src.models.schemas import CanonicalEntityDecision

                    decision = CanonicalEntityDecision(
                        merge=False,
                        canonical_name=cluster.canonical_candidate,
                        reasoning=f"Judge error: {exc}",
                    )
                entity = cluster_to_entity(cluster, decision, provenance_map)
                entity.source_doc = source_doc
                entity.name = normalize_concept_name(entity.name)
                cluster_results[i] = entity
        canonical_entities = [cluster_results[i] for i in range(len(clusters))]

    # ── Singletons: promote — optionally with LLM-synthesized definitions ──────
    singleton_entities = [e for e in all_entities if e not in clustered_entities]
    settings = get_settings()

    if settings.enable_singleton_llm_definitions:
        singleton_definitions = _infer_singleton_definitions_batch(
            [(e, provenance_map.get(e, [])) for e in singleton_entities],
            llm,
            concurrency=settings.extraction_concurrency,
        )
    else:
        singleton_definitions = {}  # use provenance text directly — free, no LLM call

    for singleton in singleton_entities:
        provenance_texts = provenance_map.get(singleton, [])
        # Prefer LLM-synthesized definition; fall back to joined provenance sentences
        definition = singleton_definitions.get(singleton) or " | ".join(provenance_texts[:3])
        canonical_entities.append(
            Entity(
                name=normalize_concept_name(singleton),
                definition=definition,
                synonyms=[],
                provenance_text=" | ".join(provenance_texts[:3]),
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
