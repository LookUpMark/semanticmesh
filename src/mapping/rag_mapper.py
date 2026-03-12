"""RAG Semantic Mapping node.

EP-06: Map-Reduce RAG — for each physical table, retrieve relevant business
concepts via embedding similarity, then call the LLM to propose a mapping.
"""

from __future__ import annotations

import json
import logging
from typing import TYPE_CHECKING

import numpy as np
from langchain_core.embeddings import Embeddings
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
from src.prompts.templates import MAPPING_SYSTEM, MAPPING_USER

if TYPE_CHECKING:
    from src.config.llm_client import LLMProtocol

logger: logging.Logger = get_logger(__name__)
_settings = get_settings()


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
    embeddings: Embeddings,
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

    query_vec = np.array(embeddings.embed_query(query), dtype=np.float32).reshape(1, -1)

    entity_texts = [f"{e.name}: {e.definition}" if e.definition else e.name for e in entities]
    entity_vecs = np.array(embeddings.embed_documents(entity_texts), dtype=np.float32)

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
                table.table_name, exc,
            )
            return MappingProposal(
                table_name=table.table_name,
                mapped_concept=None,
                confidence=0.0,
                reasoning=f"LLM call failed: {exc}",
            )

    logger.debug(
        "Mapping LLM call for '%s' completed in %.0f ms",
        table.table_name, timer.elapsed_ms,
    )

    # Parse and validate
    try:
        data = json.loads(raw_json)
    except json.JSONDecodeError:
        logger.warning("Non-JSON mapping response for '%s'", table.table_name)
        return MappingProposal(
            table_name=table.table_name, mapped_concept=None, confidence=0.0,
            reasoning="JSON parse error.",
        )

    try:
        proposal = MappingProposal(**data)
    except ValidationError as exc:
        logger.warning("Pydantic validation error for mapping of '%s': %s", table.table_name, exc)
        return MappingProposal(
            table_name=table.table_name, mapped_concept=None, confidence=0.0,
            reasoning=f"Pydantic validation error: {exc}",
        )

    logger.info(
        "Proposed mapping: '%s' → '%s' (confidence=%.2f)",
        table.table_name, proposal.mapped_concept, proposal.confidence,
    )
    return proposal
