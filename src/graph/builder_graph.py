"""Builder LangGraph — EP-11 / US-11-01.

Wires all ingestion nodes (extraction → ER → DDL → enrichment → mapping →
validation → HITL → Cypher → graph write) into a compiled StateGraph.
"""

from __future__ import annotations

import logging
import uuid
from pathlib import Path
from typing import Any

from langchain_core.messages import SystemMessage
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import END, StateGraph
from langgraph.types import Command

from src.config.llm_factory import get_extraction_llm, get_reasoning_llm
from src.config.logging import get_logger
from src.config.settings import get_settings
from src.extraction.triplet_extractor import extract_all_triplets
from src.graph.cypher_builder import build_fk_cypher, build_upsert_cypher
from src.graph.cypher_generator import generate_cypher
from src.graph.cypher_healer import heal_cypher
from src.graph.neo4j_client import Neo4jClient, setup_schema
from src.ingestion.ddl_parser import parse_ddl_file
from src.ingestion.pdf_loader import load_and_chunk_pdf
from src.ingestion.schema_enricher import enrich_all
from src.mapping.hitl import hitl_node
from src.mapping.rag_mapper import build_retrieval_query, propose_mapping, retrieve_top_entities
from src.mapping.validator import build_reflection_prompt, critic_review, validate_schema
from src.models.schemas import Entity, MappingProposal
from src.models.state import BuilderState
from src.prompts.few_shot import load_cypher_examples
from src.retrieval.embeddings import embed_text, get_embeddings
from src.resolution.entity_resolver import resolve_entities

logger: logging.Logger = get_logger(__name__)


# ─────────────────────────────────────────────────────────────────────────────
# Node Implementations
# ─────────────────────────────────────────────────────────────────────────────

def _node_extract_triplets(state: BuilderState) -> dict[str, Any]:
    """Extract semantic triplets from document chunks."""
    llm = get_extraction_llm()
    chunks = state.get("chunks") or []
    triplets = extract_all_triplets(chunks, llm)
    return {"triplets": triplets}


def _node_entity_resolution(state: BuilderState) -> dict[str, Any]:
    """Resolve extracted triplets into canonical entities."""
    embeddings = get_embeddings()
    llm = get_reasoning_llm()
    triplets = state.get("triplets") or []
    source_doc = state.get("source_doc", "unknown")
    entities = resolve_entities(triplets, embeddings, llm, source_doc)
    return {"entities": entities}


def _node_parse_ddl(state: BuilderState) -> dict[str, Any]:
    """Parse DDL files into TableSchema objects."""
    ddl_paths: list[str] = state.get("ddl_paths") or []
    tables = []
    for path in ddl_paths:
        tables.extend(parse_ddl_file(path))
    return {"tables": tables}


def _node_enrich_schema(state: BuilderState) -> dict[str, Any]:
    """Enrich table schemas with acronym expansion and descriptions."""
    llm = get_reasoning_llm()
    tables = state.get("tables") or []
    enriched = enrich_all(tables, llm)
    return {"enriched_tables": enriched}


def _node_rag_mapping(state: BuilderState) -> dict[str, Any]:
    """Generate RAG-augmented mapping proposal for current table."""
    settings = get_settings()
    llm = get_reasoning_llm()
    embeddings = get_embeddings()
    enriched_tables = state.get("enriched_tables") or []
    entities: list[Entity] = state.get("entities") or []
    reflection_prompt: str | None = state.get("reflection_prompt")

    # Process next table from remaining queue, or retry current on reflection
    if reflection_prompt and state.get("current_table"):
        current_table = state["current_table"]
        remaining = list(state.get("pending_tables") or [])
    else:
        pending: list = list(state.get("pending_tables") or enriched_tables)
        if not pending:
            return {"pending_tables": [], "current_table": None}
        current_table = pending[0]
        remaining = pending[1:]

    query = build_retrieval_query(current_table)
    top_entities = retrieve_top_entities(query, entities, embeddings, top_k=settings.retrieval_vector_top_k)

    # If coming from a reflection retry, inject the critique into the proposal call
    proposal = propose_mapping(
        current_table, top_entities, llm,
        few_shot_examples="",  # TODO: Load from few_shot module
        reflection_prompt=reflection_prompt,
    )

    return {
        "mapping_proposal": proposal,
        "current_table": current_table,
        "current_entities": top_entities,
        "pending_tables": remaining,
        "reflection_prompt": None,  # reset after use
        "reflection_attempts": state.get("reflection_attempts", 0),
    }


def _node_validate_mapping(state: BuilderState) -> dict[str, Any]:
    """Two-layer validation: Pydantic schema + LLM Critic."""
    settings = get_settings()
    llm = get_reasoning_llm()
    proposal: MappingProposal | None = state.get("mapping_proposal")
    table = state.get("current_table")
    entities: list[Entity] = state.get("current_entities") or []
    attempts: int = state.get("reflection_attempts", 0)

    if proposal is None:
        return {"reflection_attempts": attempts + 1}

    # Layer 1: Pydantic
    validated, error = validate_schema(proposal.model_dump())
    if error:
        if attempts >= settings.max_reflection_attempts:
            logger.warning(
                "Pydantic validation failed after %d attempts for '%s' — accepting last proposal.",
                attempts,
                proposal.table_name,
            )
            return {"reflection_attempts": 0, "hitl_flag": False}
        ref_prompt = build_reflection_prompt(
            role="data governance expert",
            output_format="JSON mapping proposal",
            error=error,
            original_input=proposal.model_dump_json(),
        )
        return {"reflection_prompt": ref_prompt, "reflection_attempts": attempts + 1}

    # Layer 2: LLM Critic
    decision = critic_review(validated, table, entities, llm)
    if not decision.approved:
        critique = decision.critique or "Mapping rejected by critic."
        if attempts >= settings.max_reflection_attempts:
            logger.warning(
                "Critic rejected mapping for '%s' after %d attempts — accepting best proposal.",
                validated.table_name,
                attempts,
            )
            return {
                "mapping_proposal": validated,
                "validation_error": None,
                "reflection_attempts": 0,
                "hitl_flag": False,
            }
        ref_prompt = build_reflection_prompt(
            role="data governance expert",
            output_format="JSON mapping proposal",
            error=critique,
            original_input=proposal.model_dump_json(),
        )
        return {"reflection_prompt": ref_prompt, "reflection_attempts": attempts + 1}

    return {
        "mapping_proposal": validated,
        "validation_error": None,
        "reflection_attempts": 0,
        "hitl_flag": validated.confidence < settings.confidence_threshold,
    }


def _node_generate_cypher(state: BuilderState) -> dict[str, Any]:
    """Generate MERGE-based Cypher from mapping proposal."""
    settings = get_settings()
    llm = get_reasoning_llm()
    proposal: MappingProposal = state["mapping_proposal"]
    table = state.get("current_table")
    # Build a synthetic Entity from the proposal so the concept name and
    # definition in the generated Cypher match the validated mapping exactly,
    # rather than an arbitrary entity retrieved during the mapping step.
    entity = Entity(
        name=proposal.mapped_concept or "Unknown",
        definition=proposal.reasoning or "",
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
    llm = get_reasoning_llm()
    cypher: str = state.get("current_cypher") or ""
    proposal: MappingProposal = state["mapping_proposal"]

    with Neo4jClient() as client:
        healed = heal_cypher(
            cypher, proposal, client.driver, llm,
            max_attempts=settings.max_cypher_healing_attempts,
        )

    if healed is None:
        logger.warning("Cypher healing failed for table '%s' — using deterministic builder.", proposal.table_name)
        return {"cypher_failed": True, "current_cypher": None}

    return {"current_cypher": healed, "cypher_failed": False}


def _node_build_graph(state: BuilderState) -> dict[str, Any]:
    """Execute the best available Cypher to upsert data into Neo4j.

    Strategy (primary → fallback):
    1. **LLM-healed Cypher** — if ``heal_cypher`` succeeded (``cypher_failed=False``
       and ``current_cypher`` is set), execute the LLM-generated Cypher directly.
       This is the "happy path" that exercises the full thesis loop: generate →
       self-reflect → heal → execute.
    2. **Deterministic builder** — if the LLM Cypher is invalid after all healing
       attempts, fall back to ``cypher_builder.build_upsert_cypher`` which uses
       driver-bound parameters and is immune to quoting/escaping issues.

    In both cases the BusinessConcept embedding is populated afterwards so the
    vector index can serve Query Graph requests.
    """
    proposal: MappingProposal = state["mapping_proposal"]
    table: EnrichedTableSchema | None = state.get("current_table")

    if not proposal or not table:
        logger.warning("Missing proposal or table in build_graph — skipping.")
        return {}

    llm_cypher: str | None = state.get("current_cypher")
    cypher_failed: bool = state.get("cypher_failed", False)

    if llm_cypher and not cypher_failed:
        # Primary path: LLM-healed Cypher passed Neo4j EXPLAIN — execute it.
        logger.info("Executing LLM-healed Cypher for '%s'.", proposal.table_name)
        exec_cypher, exec_params = llm_cypher, {}
    else:
        # Fallback path: healing exhausted or no Cypher produced.
        logger.info(
            "LLM Cypher failed for '%s' — falling back to deterministic builder.",
            proposal.table_name,
        )
        exec_cypher, exec_params = build_upsert_cypher(proposal, table)

    with Neo4jClient() as client:
        client.execute_cypher(exec_cypher, exec_params)
        logger.info("Graph updated for table '%s'.", proposal.table_name)

        # Write FK edges: PhysicalTable -[:REFERENCES]-> PhysicalTable
        fk_statements = build_fk_cypher(table)
        for fk_cypher, fk_params in fk_statements:
            try:
                client.execute_cypher(fk_cypher, fk_params)
                logger.info(
                    "FK edge: %s.%s -> %s",
                    table.table_name, fk_params["fk_column"], fk_params["tgt_table"],
                )
            except Exception as exc:
                logger.warning("Could not write FK edge for %s.%s: %s", table.table_name, fk_params["fk_column"], exc)

        # Populate the BGE-M3 embedding so the vector index can serve queries.
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

    completed = list(state.get("completed_tables") or [])
    completed.append(proposal.table_name)
    return {"completed_tables": completed}


# ─────────────────────────────────────────────────────────────────────────────
# Conditional Edge Predicates
# ─────────────────────────────────────────────────────────────────────────────

def _route_after_validate(state: BuilderState) -> str:
    """Route after validation: HITL, retry mapping, or proceed to Cypher."""
    if state.get("hitl_flag"):
        return "hitl"
    if state.get("reflection_prompt"):
        return "rag_mapping"  # retry with reflection
    return "generate_cypher"


def _route_after_heal(state: BuilderState) -> str:
    """Route after Cypher healing: always proceed to build_graph.

    ``build_graph`` implements a primary/fallback strategy internally:
    - ``cypher_failed=False`` → LLM-healed Cypher executed directly (primary)
    - ``cypher_failed=True``  → deterministic builder used as fallback
    """
    return "build_graph"


def _route_after_build(state: BuilderState) -> str:
    """Route after graph build: process next table or END."""
    if state.get("pending_tables"):
        return "rag_mapping"
    return END


# ─────────────────────────────────────────────────────────────────────────────
# Graph Factory
# ─────────────────────────────────────────────────────────────────────────────

def build_builder_graph(*, production: bool = False):
    """Compile and return the full Builder StateGraph.

    Args:
        production: If True, uses ``SqliteSaver`` for persistence; otherwise
                    ``MemorySaver`` (in-process, ephemeral).

    Returns:
        A compiled LangGraph ``CompiledStateGraph`` ready to ``.invoke()``.
    """
    graph = StateGraph(BuilderState)

    # Nodes
    graph.add_node("extract_triplets", _node_extract_triplets)
    graph.add_node("entity_resolution", _node_entity_resolution)
    graph.add_node("parse_ddl", _node_parse_ddl)
    graph.add_node("enrich_schema", _node_enrich_schema)
    graph.add_node("rag_mapping", _node_rag_mapping)
    graph.add_node("validate_mapping", _node_validate_mapping)
    graph.add_node("hitl", hitl_node)
    graph.add_node("generate_cypher", _node_generate_cypher)
    graph.add_node("heal_cypher", _node_heal_cypher)
    graph.add_node("build_graph", _node_build_graph)

    # Entry
    graph.set_entry_point("extract_triplets")

    # Linear edges
    graph.add_edge("extract_triplets", "entity_resolution")
    graph.add_edge("entity_resolution", "parse_ddl")
    graph.add_edge("parse_ddl", "enrich_schema")
    graph.add_edge("enrich_schema", "rag_mapping")
    graph.add_edge("rag_mapping", "validate_mapping")
    graph.add_edge("hitl", "generate_cypher")
    graph.add_edge("generate_cypher", "heal_cypher")

    # Conditional edges
    graph.add_conditional_edges(
        "validate_mapping",
        _route_after_validate,
        {"hitl": "hitl", "rag_mapping": "rag_mapping", "generate_cypher": "generate_cypher"},
    )
    graph.add_conditional_edges(
        "heal_cypher",
        _route_after_heal,
        {"build_graph": "build_graph"},
    )
    graph.add_conditional_edges(
        "build_graph",
        _route_after_build,
        {"rag_mapping": "rag_mapping", END: END},
    )

    # Checkpointer
    if production:
        try:
            from langgraph.checkpoint.sqlite import SqliteSaver
            settings = get_settings()
            checkpointer = SqliteSaver.from_conn_string(settings.sqlite_checkpoint_path)
        except ImportError:
            logger.warning("SqliteSaver not available — falling back to MemorySaver.")
            checkpointer = MemorySaver()
    else:
        checkpointer = MemorySaver()

    return graph.compile(checkpointer=checkpointer, interrupt_before=["hitl"])


def run_builder(
    raw_documents: list[str],
    ddl_paths: list[str],
    *,
    production: bool = False,
    clear_graph: bool = False,
) -> BuilderState:
    """Convenience wrapper: compile graph and invoke with document paths.

    Args:
        raw_documents: List of file paths to PDF documents.
        ddl_paths:     List of file paths to DDL SQL files.
        production:    Compile with ``SqliteSaver`` if True.
        clear_graph:   If True, delete all nodes and relationships before running.
                       Use in development/demo to avoid stale data from prior runs.

    Returns:
        Final ``BuilderState`` after graph completion.
    """
    chunks = []
    for doc_path in raw_documents:
        chunks.extend(load_and_chunk_pdf(doc_path))

    # Ensure Neo4j schema (constraints + vector index) exists before writing.
    with Neo4jClient() as client:
        if clear_graph:
            client.execute_cypher("MATCH (n) DETACH DELETE n")
            logger.info("Graph cleared before builder run.")
        setup_schema(client)

    graph = build_builder_graph(production=production)
    initial: BuilderState = {
        "chunks": chunks,
        "ddl_paths": ddl_paths,
        "source_doc": str(raw_documents[0]) if raw_documents else "unknown",
        "triplets": [],
        "entities": [],
        "tables": [],
        "enriched_tables": [],
        "pending_tables": [],
        "completed_tables": [],
    }
    config = {"configurable": {"thread_id": f"builder-{uuid.uuid4().hex[:8]}"}}
    final_state: BuilderState = graph.invoke(initial, config=config)
    return final_state
