"""Build nodes for the Builder Graph.

This module contains the graph building logic, including Cypher generation,
healing, and execution with fallback strategies.
"""

from __future__ import annotations

import json as _json
import logging
from typing import Any

from src.config.llm_factory import get_reasoning_llm
from src.config.logging import get_logger
from src.config.settings import get_settings
from src.graph.cypher_builder import build_fk_cypher, build_upsert_cypher
from src.graph.cypher_generator import generate_cypher
from src.graph.cypher_healer import heal_cypher
from src.graph.neo4j_client import Neo4jClient
from src.models.schemas import EnrichedTableSchema, Entity, MappingProposal
from src.models.state import BuilderState
from src.prompts.few_shot import load_cypher_examples
from src.retrieval.embeddings import embed_text, get_embeddings

logger: logging.Logger = get_logger(__name__)


def _find_entity_for_concept(concept_name: str, entities: list[Entity]) -> Entity | None:
    """Find the resolved Entity matching a mapped concept name.

    Performs case-insensitive lookup, preferring exact match then substring.
    """
    if not concept_name or not entities:
        return None
    lower = concept_name.lower()
    for ent in entities:
        if ent.name.lower() == lower:
            return ent
    for ent in entities:
        if lower in ent.name.lower() or ent.name.lower() in lower:
            return ent
    return None


def _node_generate_cypher(state: BuilderState) -> dict[str, Any]:
    """Generate MERGE-based Cypher from mapping proposal."""
    settings = get_settings()
    if bool(state.get("use_lazy_extraction", settings.use_lazy_extraction)):
        logger.info("Lazy mode: skipping LLM Cypher generation.")
        return {"current_cypher": None, "healing_attempts": 0}

    llm = get_reasoning_llm()
    proposal: MappingProposal = state["mapping_proposal"]
    table = state.get("current_table")
    resolved = _find_entity_for_concept(
        proposal.mapped_concept or "", state.get("current_entities") or []
    )
    entity = resolved or Entity(
        name=proposal.mapped_concept or "Unknown",
        definition="",
        synonyms=[],
        provenance_text="",
        source_doc="",
    )
    few_shot = load_cypher_examples(settings.few_shot_cypher_examples)
    cypher = generate_cypher(proposal, table, entity, few_shot, llm)
    return {"current_cypher": cypher, "healing_attempts": 0}


def _node_heal_cypher(state: BuilderState) -> dict[str, Any]:
    """Validate and heal Cypher via dry-run + LLM reflection loop."""
    settings = get_settings()
    if bool(state.get("use_lazy_extraction", settings.use_lazy_extraction)):
        return {"cypher_failed": True, "current_cypher": None}

    if not settings.enable_cypher_healing:
        logger.info("Cypher healing disabled — using deterministic builder fallback.")
        return {"cypher_failed": True, "current_cypher": None}
    llm = get_reasoning_llm()
    cypher: str = state.get("current_cypher") or ""
    proposal: MappingProposal = state["mapping_proposal"]

    with Neo4jClient() as client:
        healed = heal_cypher(
            cypher,
            proposal,
            client.driver,
            llm,
            max_attempts=settings.max_cypher_healing_attempts,
        )

    if healed is None:
        logger.warning(
            "Cypher healing failed for table '%s' — using deterministic builder.",
            proposal.table_name,
        )
        return {"cypher_failed": True, "current_cypher": None}

    return {"current_cypher": healed, "cypher_failed": False}


def _build_llm_cypher_params(
    proposal: MappingProposal,
    table: EnrichedTableSchema,
    entity: Entity | None,
) -> dict[str, Any]:
    """Build a safety-net parameter dict for LLM-generated Cypher.

    The system prompt instructs the LLM to inline all values, but it sometimes
    emits ``$parameter``-style Cypher copied from few-shot examples.  Providing
    the full parameter set prevents ``Neo.ClientError.Statement.ParameterMissing``
    at execution time — unused parameters are silently ignored by the driver.
    """
    column_names = [c.name for c in table.columns]
    column_types = _json.dumps({c.name: c.data_type for c in table.columns})
    return {
        "concept_name": proposal.mapped_concept or "Unknown",
        "definition": entity.definition if entity else "",
        "mapping_reasoning": proposal.reasoning or "",
        "provenance_text": entity.provenance_text if entity else "",
        "source_doc": entity.source_doc if entity else "",
        "synonyms": entity.synonyms if entity else [],
        "confidence_score": proposal.confidence,
        "table_name": table.table_name,
        "schema_name": table.schema_name,
        "column_names": column_names,
        "column_types": column_types,
        "ddl_source": table.ddl_source or "",
        "confidence": proposal.confidence,
        "mapping_confidence": proposal.confidence,
        "validated_by": "llm_judge",
    }


def _node_build_graph(state: BuilderState) -> dict[str, Any]:
    """Execute the best available Cypher to upsert data into Neo4j.

    Strategy (primary -> fallback):
    1. LLM-healed Cypher — if ``heal_cypher`` succeeded (``cypher_failed=False``
       and ``current_cypher`` is set), execute the LLM-generated Cypher directly.
    2. Deterministic builder — if the LLM Cypher is invalid after all healing
       attempts, fall back to ``cypher_builder.build_upsert_cypher`` which uses
       driver-bound parameters and is immune to quoting/escaping issues.

    In both cases the BusinessConcept embedding is populated afterwards so the
    vector index can serve Query Graph requests.
    """
    proposal: MappingProposal | None = state.get("mapping_proposal")
    table: EnrichedTableSchema | None = state.get("current_table")

    if not proposal or not table:
        logger.warning("Missing proposal or table in build_graph — skipping.")
        return {}

    llm_cypher: str | None = state.get("current_cypher")
    cypher_failed: bool = state.get("cypher_failed", False)
    lazy_mode: bool = bool(state.get("use_lazy_extraction", get_settings().use_lazy_extraction))

    # Resolve entity early — needed for both LLM and fallback paths.
    resolved = _find_entity_for_concept(
        proposal.mapped_concept or "", state.get("current_entities") or []
    )

    if llm_cypher and not cypher_failed and not lazy_mode:
        logger.info("Executing LLM-healed Cypher for '%s'.", proposal.table_name)
        exec_cypher = llm_cypher
        # Safety-net params: the system prompt tells the LLM to inline values,
        # but it sometimes copies parameterised style from few-shot examples.
        # Providing the params avoids ParameterMissing errors at runtime.
        exec_params = _build_llm_cypher_params(proposal, table, resolved)
    else:
        logger.info(
            "LLM Cypher failed for '%s' — falling back to deterministic builder.",
            proposal.table_name,
        )
        exec_cypher, exec_params = build_upsert_cypher(proposal, table, entity=resolved)

    with Neo4jClient() as client:
        client.execute_cypher(exec_cypher, exec_params)
        logger.info("Graph updated for table '%s'.", proposal.table_name)

        # Normalize PhysicalTable.table_name to canonical UPPERCASE
        # (LLM Cypher may use lowercase from DDL source text, while
        # build_fk_cypher always uses the UPPERCASE name from the parser)
        client.execute_cypher(
            "MATCH (pt:PhysicalTable) "
            "WHERE toLower(pt.table_name) = toLower($name) "
            "SET pt.table_name = $canonical",
            {"name": table.table_name, "canonical": table.table_name},
        )

        # Always stamp source_file regardless of which Cypher path was used
        # (LLM-generated Cypher doesn't know about this property)
        if table.source_file:
            client.execute_cypher(
                "MATCH (pt:PhysicalTable) "
                "WHERE toLower(pt.table_name) = toLower($name) "
                "SET pt.source_file = $source_file",
                {"name": table.table_name, "source_file": table.source_file},
            )

        fk_statements = build_fk_cypher(table)
        for fk_cypher, fk_params in fk_statements:
            try:
                client.execute_cypher(fk_cypher, fk_params)
                logger.info(
                    "FK edge: %s.%s -> %s",
                    table.table_name,
                    fk_params["fk_column"],
                    fk_params["tgt_table"],
                )
            except Exception as exc:
                logger.warning(
                    "Could not write FK edge for %s.%s: %s",
                    table.table_name,
                    fk_params["fk_column"],
                    exc,
                )

        if proposal.mapped_concept:
            try:
                model = get_embeddings()
                vector = embed_text(proposal.mapped_concept, model=model)
                client.execute_cypher(
                    "MATCH (c:BusinessConcept {name: $name}) SET c.embedding = $emb",
                    {"name": proposal.mapped_concept, "emb": vector},
                )
                logger.info("Embedding set for BusinessConcept '%s'.", proposal.mapped_concept)
            except Exception as exc:
                logger.warning("Could not set embedding for '%s': %s", proposal.mapped_concept, exc)

        # ── MENTIONS edges: link Chunk nodes to this BusinessConcept ──
        if proposal.mapped_concept:
            triplets = state.get("triplets") or []
            concept_lower = proposal.mapped_concept.lower()
            chunk_indexes: set[int] = set()
            for t in triplets:
                if t.source_chunk_index is not None and (
                    concept_lower in t.subject.lower() or concept_lower in t.object.lower()
                ):
                    chunk_indexes.add(t.source_chunk_index)
            if chunk_indexes:
                try:
                    client.execute_cypher(
                        "UNWIND $idxs AS idx "
                        "MATCH (ch:Chunk {chunk_index: idx}) "
                        "MATCH (bc:BusinessConcept {name: $concept}) "
                        "MERGE (ch)-[:MENTIONS]->(bc)",
                        {"idxs": list(chunk_indexes), "concept": proposal.mapped_concept},
                    )
                    logger.info(
                        "MENTIONS edges: %d chunks → '%s' (batch).",
                        len(chunk_indexes),
                        proposal.mapped_concept,
                    )
                except Exception as exc:
                    logger.warning(
                        "Could not create MENTIONS edges → '%s': %s",
                        proposal.mapped_concept,
                        exc,
                    )

    completed = list(state.get("completed_tables") or [])
    completed.append(proposal.table_name)
    return {"completed_tables": completed}


def _route_after_heal(state: BuilderState) -> str:
    """Route after Cypher healing: always proceed to build_graph.

    ``build_graph`` implements a primary/fallback strategy internally:
    - ``cypher_failed=False`` -> LLM-healed Cypher executed directly
    - ``cypher_failed=True``  -> deterministic builder used as fallback
    """
    return "build_graph"
