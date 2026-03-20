"""RAG Semantic Mapping node.

EP-06: Map-Reduce RAG — for each physical table, retrieve relevant business
concepts via embedding similarity, then call the LLM to propose a mapping.
"""

from __future__ import annotations

import json
import logging
import re
from typing import TYPE_CHECKING, Any

import numpy as np
from langchain_core.messages import HumanMessage, SystemMessage
from pydantic import ValidationError
from sklearn.metrics.pairwise import cosine_similarity

from src.config.logging import NodeTimer, get_logger
from src.config.settings import get_settings
from src.models.schemas import (
    EnrichedTableSchema,
    Entity,
    MappingProposal,
    TableSchema,
)
from src.prompts.templates import MAPPING_SYSTEM, MAPPING_USER, REFLECTION_TEMPLATE
from src.retrieval.embeddings import embed_text, embed_texts

if TYPE_CHECKING:
    from src.config.llm_client import LLMProtocol

logger: logging.Logger = get_logger(__name__)
_settings = get_settings()

# Matches optional triple-backtick markdown fences (with or without language tag)
_FENCE_RE = re.compile(r"^```[a-zA-Z]*\n?|```$", re.MULTILINE)


def _clean_json(raw: str) -> str:
    """Strip markdown fences from LLM output before JSON parsing."""
    return _FENCE_RE.sub("", raw).strip()


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


def propose_mapping(
    table: TableSchema,
    entities: list[Entity],
    llm: LLMProtocol,
    few_shot_examples: str = "",
    reflection_prompt: str | None = None,
) -> MappingProposal:
    """Call the LLM to propose a semantic mapping for a single table.

    Args:
        table: The physical table (raw or enriched — both work).
        entities: The pre-retrieved subset of business entities (top-k).
        llm: Reasoning LLM (temperature=0.0).
        few_shot_examples: Formatted string from ``format_mapping_examples``
                           to inject into ``MAPPING_USER``.
        reflection_prompt: Optional Reflection Prompt critique from the validator;
                           prepended to ``few_shot_examples`` on retry calls.

    Returns:
        A validated ``MappingProposal``.  On any failure, returns a
        conservative ``MappingProposal`` with ``mapped_concept=None``
        and ``confidence=0.0`` — never crashes the pipeline.
    """
    entities_json = json.dumps(
        [
            {
                "name": e.name,
                "definition": e.definition,
                "synonyms": e.synonyms,
                "provenance_text": e.provenance_text[:300],
            }
            for e in entities
        ]
    )
    # Prepend reflection critique when this is a retry call
    effective_few_shot = (
        f"[REFLECTION CRITIQUE — correct the following error before generating]\n"
        f"{reflection_prompt}\n\n{few_shot_examples}"
        if reflection_prompt
        else few_shot_examples
    )
    user_prompt = MAPPING_USER.format(
        few_shot_examples=effective_few_shot,
        table_ddl=table.ddl_source,
        entities_json=entities_json,
    )

    with NodeTimer() as timer:
        try:
            response = llm.invoke(
                [
                    SystemMessage(content=MAPPING_SYSTEM),
                    HumanMessage(content=user_prompt),
                ]
            )
            raw_json: str = response.content.strip()
        except Exception as exc:
            logger.warning(
                "LLM mapping call failed for table '%s': %s — returning null mapping.",
                table.table_name,
                exc,
            )
            return MappingProposal(
                table_name=table.table_name,
                mapped_concept=None,
                confidence=0.0,
                reasoning=f"LLM call failed: {exc}",
            )

    logger.debug(
        "Mapping LLM call for '%s' completed in %.0f ms",
        table.table_name,
        timer.elapsed_ms,
    )

    # Parse and validate — with self-reflection on failure
    settings = get_settings()
    max_attempts: int = settings.max_reflection_attempts

    for attempt in range(1, max_attempts + 1):
        try:
            data = json.loads(_clean_json(raw_json))
        except json.JSONDecodeError as exc:
            logger.warning(
                "Non-JSON mapping response for '%s' (attempt %d/%d): %s",
                table.table_name,
                attempt,
                max_attempts,
                exc,
            )
            if attempt == max_attempts:
                return MappingProposal(
                    table_name=table.table_name,
                    mapped_concept=None,
                    confidence=0.0,
                    reasoning="JSON parse error after self-reflection exhausted.",
                )
            raw_json = llm.invoke(
                [
                    HumanMessage(
                        content=REFLECTION_TEMPLATE.format(
                            role="senior data governance expert",
                            output_format='JSON object matching {"table_name":…,"mapped_concept":…,"confidence":…,"reasoning":…,"alternative_concepts":[…]}',
                            error_or_critique=str(exc),
                            original_input=raw_json,
                        )
                    )
                ]
            ).content.strip()
            continue

        try:
            proposal = MappingProposal(**data)
        except ValidationError as exc:
            logger.warning(
                "Pydantic validation error for mapping of '%s' (attempt %d/%d): %s",
                table.table_name,
                attempt,
                max_attempts,
                exc,
            )
            if attempt == max_attempts:
                return MappingProposal(
                    table_name=table.table_name,
                    mapped_concept=None,
                    confidence=0.0,
                    reasoning=f"Pydantic validation error after self-reflection exhausted: {exc}",
                )
            raw_json = llm.invoke(
                [
                    HumanMessage(
                        content=REFLECTION_TEMPLATE.format(
                            role="senior data governance expert",
                            output_format='JSON object matching {"table_name":…,"mapped_concept":…,"confidence":…,"reasoning":…,"alternative_concepts":[…]}',
                            error_or_critique=str(exc),
                            original_input=json.dumps(data),
                        )
                    )
                ]
            ).content.strip()
            continue

        logger.info(
            "Proposed mapping: '%s' → '%s' (confidence=%.2f)",
            table.table_name,
            proposal.mapped_concept,
            proposal.confidence,
        )
        return proposal

    # Unreachable — loop always returns
    return MappingProposal(
        table_name=table.table_name, mapped_concept=None, confidence=0.0, reasoning="Exhausted."
    )


def propose_mapping_heuristic(
    table: EnrichedTableSchema,
    entities: list[Entity],
    embeddings: Any,
    top_k: int | None = None,
    min_confidence: float | None = None,
) -> MappingProposal:
    """Embedding-first mapping proposal without LLM calls.

    This is the lazy-mode mapping path. It ranks entities by cosine similarity
    and turns the best score into a calibrated confidence value.
    """
    settings = get_settings()
    threshold = (
        float(min_confidence)
        if min_confidence is not None
        else float(getattr(settings, "heuristic_mapping_confidence_threshold", 0.60))
    )

    query = build_retrieval_query(table)
    ranked = retrieve_top_entities(query, entities, embeddings, top_k=top_k)
    if not ranked:
        return MappingProposal(
            table_name=table.table_name,
            mapped_concept=None,
            confidence=0.0,
            reasoning="No candidate entities available for heuristic mapping.",
            alternative_concepts=[],
        )

    q_vec = np.array(embed_text(query, model=embeddings), dtype=np.float32).reshape(1, -1)

    generic_noise_tokens = {
        "business",
        "dictionary",
        "description",
        "decimal",
        "status",
        "examples",
        "contains",
        "provides",
        "usage",
        "multiple",
        "negative",
    }
    table_column_names = {c.name.upper() for c in table.columns}

    def _normalize_candidate_name(name: str) -> str:
        cleaned = re.sub(r"^the\s+", "", name.strip(), flags=re.IGNORECASE)
        cleaned = re.sub(r"\s+business\s+concept$", "", cleaned, flags=re.IGNORECASE)
        cleaned = cleaned.strip(" .")
        return cleaned

    def _is_attribute_like(name: str) -> bool:
        n = name.strip()
        n_tokens = [t for t in re.split(r"[^a-zA-Z0-9]+", n.lower()) if t]
        if n.upper() in table_column_names:
            return True
        if re.fullmatch(r"[A-Z0-9_]{4,}", n) and "_" in n:
            return True
        if len(n_tokens) == 0 or len(n_tokens) > 8:
            return True
        if n.lower() in generic_noise_tokens:
            return True
        return False

    table_tokens = {
        t
        for t in re.split(r"[^a-zA-Z0-9]+", (table.enriched_table_name or table.table_name).lower())
        if t
    }

    best_name: str | None = None
    best_similarity = -1.0
    best_confidence = 0.0
    best_adjusted = -1.0

    for candidate in ranked[: max(5, top_k or 0)]:
        candidate_text = (
            f"{candidate.name}: {candidate.definition}" if candidate.definition else candidate.name
        )
        e_vec = np.array(embed_text(candidate_text, model=embeddings), dtype=np.float32).reshape(1, -1)
        similarity = float(cosine_similarity(q_vec, e_vec)[0][0])
        base_confidence = max(0.0, min(1.0, (similarity + 1.0) / 2.0))

        name = _normalize_candidate_name(candidate.name)
        lower_name = name.lower()
        name_tokens = [t for t in re.split(r"[^a-zA-Z0-9]+", lower_name) if t]

        penalty = 0.0
        bonus = 0.0

        if name.upper() in table_column_names:
            penalty += 0.25
        if re.fullmatch(r"[A-Z0-9_]{4,}", name) and "_" in name:
            penalty += 0.20
        if lower_name in generic_noise_tokens:
            penalty += 0.20
        if len(name_tokens) > 8 or len(name_tokens) == 0:
            penalty += 0.10

        overlap = len(set(name_tokens) & table_tokens)
        if overlap:
            bonus += min(0.12, overlap * 0.04)

        adjusted = max(0.0, min(1.0, base_confidence - penalty + bonus))

        if adjusted > best_adjusted:
            best_adjusted = adjusted
            best_name = name
            best_similarity = similarity
            best_confidence = adjusted

    mapped_concept = best_name if best_confidence >= threshold else None

    if mapped_concept is not None and _is_attribute_like(mapped_concept):
        mapped_concept = None

    if mapped_concept is None:
        fallback_name = _normalize_candidate_name(table.enriched_table_name or table.table_name)
        if fallback_name and not _is_attribute_like(fallback_name):
            mapped_concept = fallback_name
            best_confidence = max(best_confidence, max(0.0, threshold - 0.05))

    return MappingProposal(
        table_name=table.table_name,
        mapped_concept=mapped_concept,
        confidence=round(best_confidence, 3),
        reasoning=(
            f"Heuristic embedding mapping score={best_similarity:.3f}, "
            f"adjusted_confidence={best_confidence:.3f}, threshold={threshold:.3f}, "
            f"best_candidate='{best_name}'."
        ),
        alternative_concepts=[e.name for e in ranked[1:3]],
    )
