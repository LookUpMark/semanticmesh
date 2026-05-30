"""Parallel mapping + validation for the Builder Graph.

When mapping_concurrency > 1, all tables are processed concurrently through
the mapping → critic validation loop using ThreadPoolExecutor. This avoids
the sequential bottleneck of processing 50+ tables one-by-one.

The function returns a dict[table_name, MappingProposal] that the LangGraph
loop can consume directly, skipping the expensive LLM calls.
"""

from __future__ import annotations

import logging
from concurrent.futures import ThreadPoolExecutor, as_completed

from src.config.llm_factory import get_midtier_llm
from src.config.logging import get_logger
from src.config.settings import get_settings
from src.mapping.rag_mapper import propose_mapping
from src.mapping.retrieval import build_retrieval_query, retrieve_top_entities
from src.mapping.validator import critic_review, validate_schema
from src.models.schemas import EnrichedTableSchema, Entity, MappingProposal
from src.prompts.few_shot import format_mapping_examples, load_mapping_examples
from src.retrieval.embeddings import get_embeddings

logger: logging.Logger = get_logger(__name__)


def _map_validate_single(
    table: EnrichedTableSchema,
    entities: list[Entity],
    few_shot: str,
) -> tuple[str, MappingProposal | None]:
    """Process a single table through mapping + critic validation with retries.

    Returns (table_name, proposal) — proposal may be None if all attempts fail.
    """
    settings = get_settings()
    llm = get_midtier_llm()
    embeddings = get_embeddings()
    max_attempts = settings.max_reflection_attempts

    query = build_retrieval_query(table)
    top_entities = retrieve_top_entities(
        query, entities, embeddings, top_k=settings.retrieval_vector_top_k
    )

    best_proposal: MappingProposal | None = None
    reflection_prompt: str | None = None

    for attempt in range(max_attempts + 1):
        # Propose mapping
        proposal = propose_mapping(
            table,
            top_entities,
            llm,
            few_shot_examples=few_shot,
            reflection_prompt=reflection_prompt,
        )

        # Pydantic validation
        validated, error = validate_schema(proposal.model_dump())
        if error:
            logger.warning(
                "Parallel mapping: Pydantic error for '%s' attempt %d: %s",
                table.table_name,
                attempt + 1,
                error,
            )
            if best_proposal is None:
                best_proposal = proposal
            reflection_prompt = error
            continue

        # Track best
        if best_proposal is None or (validated.confidence or 0.0) > (
            best_proposal.confidence or 0.0
        ):
            best_proposal = validated

        # Confidence gate — skip critic if already high
        if (validated.confidence or 0.0) >= settings.critic_confidence_gate:
            logger.info(
                "Parallel mapping: '%s' accepted (conf=%.2f >= gate=%.2f)",
                table.table_name,
                validated.confidence,
                settings.critic_confidence_gate,
            )
            return (table.table_name, validated)

        # Skip critic if disabled
        if not settings.enable_critic_validation:
            return (table.table_name, validated)

        # Critic review
        decision = critic_review(validated, table, top_entities, llm)
        if decision.approved:
            logger.info(
                "Parallel mapping: '%s' approved by critic (conf=%.2f)",
                table.table_name,
                validated.confidence,
            )
            return (table.table_name, validated)

        # Rejected — set reflection for next attempt
        reflection_prompt = decision.critique or "Mapping rejected by critic."
        logger.info(
            "Parallel mapping: '%s' rejected by critic (attempt %d/%d)",
            table.table_name,
            attempt + 1,
            max_attempts,
        )

    # Exhausted attempts — return best proposal
    logger.warning(
        "Parallel mapping: '%s' exhausted %d attempts — using best (conf=%.2f, concept='%s')",
        table.table_name,
        max_attempts,
        best_proposal.confidence if best_proposal else 0.0,
        best_proposal.mapped_concept if best_proposal else None,
    )
    return (table.table_name, best_proposal)


def parallel_map_all_tables(
    enriched_tables: list[EnrichedTableSchema],
    entities: list[Entity],
    concurrency: int | None = None,
) -> dict[str, MappingProposal]:
    """Map all tables in parallel using ThreadPoolExecutor.

    Args:
        enriched_tables: All enriched table schemas to process.
        entities: Resolved business entities for retrieval.
        concurrency: Max parallel workers (defaults to settings.mapping_concurrency).

    Returns:
        Dict mapping table_name → validated MappingProposal.
    """
    settings = get_settings()
    workers = concurrency or settings.mapping_concurrency

    if workers <= 1 or len(enriched_tables) <= 1:
        # Sequential fallback — don't use this function
        return {}

    few_shot = format_mapping_examples(load_mapping_examples())
    results: dict[str, MappingProposal] = {}

    logger.info(
        "Parallel mapping: processing %d tables with %d workers",
        len(enriched_tables),
        workers,
    )

    with ThreadPoolExecutor(max_workers=min(workers, len(enriched_tables))) as pool:
        futures = {
            pool.submit(_map_validate_single, table, entities, few_shot): table
            for table in enriched_tables
        }

        for future in as_completed(futures):
            table = futures[future]
            try:
                table_name, proposal = future.result()
                if proposal is not None:
                    results[table_name] = proposal
                    logger.info(
                        "Parallel mapping: ✓ '%s' → '%s' (%.2f) [%d/%d]",
                        table_name,
                        proposal.mapped_concept,
                        proposal.confidence,
                        len(results),
                        len(enriched_tables),
                    )
                else:
                    logger.warning("Parallel mapping: ✗ '%s' — no valid proposal", table_name)
            except Exception as exc:
                logger.error(
                    "Parallel mapping: ✗ '%s' — exception: %s",
                    table.table_name,
                    exc,
                )

    logger.info(
        "Parallel mapping complete: %d/%d tables mapped successfully",
        len(results),
        len(enriched_tables),
    )
    return results
