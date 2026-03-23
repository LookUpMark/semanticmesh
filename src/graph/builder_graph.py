"""Builder LangGraph — EP-11 / US-11-01.

Wires all ingestion nodes (extraction -> ER -> DDL -> enrichment -> mapping ->
validation -> HITL -> Cypher -> graph write) into a compiled StateGraph.
"""

from __future__ import annotations

import logging
import uuid
from typing import Any

from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import END, StateGraph

from src.config.llm_factory import get_extraction_llm, get_reasoning_llm
from src.config.logging import get_logger
from src.config.settings import get_settings
from src.extraction.heuristic_extractor import extract_all_triplets_heuristic
from src.extraction.triplet_extractor import extract_all_triplets
from src.graph.build_nodes import (
    _node_build_graph,
    _node_generate_cypher,
    _node_heal_cypher,
    _route_after_heal,
)
from src.graph.neo4j_client import Neo4jClient, setup_schema
from src.graph.validation_nodes import _node_validate_mapping, _route_after_validate
from src.ingestion.ddl_parser import parse_ddl_file
from src.ingestion.pdf_loader import load_and_chunk_pdf
from src.ingestion.schema_enricher import enrich_all
from src.mapping.hitl import hitl_node
from src.mapping.rag_mapper import propose_mapping, propose_mapping_heuristic
from src.mapping.retrieval import build_retrieval_query, retrieve_top_entities
from src.models.schemas import Entity
from src.models.state import BuilderState
from src.resolution.entity_resolver import resolve_entities
from src.retrieval.embeddings import get_embeddings

logger: logging.Logger = get_logger(__name__)


# ─────────────────────────────────────────────────────────────────────────────
# Node Implementations
# ─────────────────────────────────────────────────────────────────────────────


def _node_extract_triplets(state: BuilderState) -> dict[str, Any]:
    """Extract semantic triplets from document chunks."""
    settings = get_settings()
    use_lazy = bool(state.get("use_lazy_extraction", settings.use_lazy_extraction))
    chunks = state.get("chunks") or []

    if use_lazy:
        logger.info("Lazy extraction enabled — using heuristic triplet extractor.")
        triplets = extract_all_triplets_heuristic(chunks)
    else:
        llm = get_extraction_llm()
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
    settings = get_settings()
    if not settings.enable_schema_enrichment:
        tables = state.get("tables") or []
        logger.info("Schema enrichment disabled — forwarding raw parsed tables.")
        return {"enriched_tables": tables}
    llm = get_reasoning_llm()
    tables = state.get("tables") or []
    enriched = enrich_all(tables, llm)
    return {"enriched_tables": enriched}


def _node_rag_mapping(state: BuilderState) -> dict[str, Any]:
    """Generate RAG-augmented mapping proposal for current table."""
    settings = get_settings()
    use_lazy = bool(state.get("use_lazy_extraction", settings.use_lazy_extraction))
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
    top_entities = retrieve_top_entities(
        query, entities, embeddings, top_k=settings.retrieval_vector_top_k
    )

    if use_lazy:
        proposal = propose_mapping_heuristic(
            current_table,
            entities,
            embeddings,
            top_k=settings.retrieval_vector_top_k,
            min_confidence=settings.heuristic_mapping_confidence_threshold,
        )
        top_entities = retrieve_top_entities(
            build_retrieval_query(current_table),
            entities,
            embeddings,
            top_k=settings.retrieval_vector_top_k,
        )
    else:
        # If coming from a reflection retry, inject the critique into the proposal call
        proposal = propose_mapping(
            current_table,
            top_entities,
            llm,
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


# ─────────────────────────────────────────────────────────────────────────────
# Conditional Edge Predicates
# ─────────────────────────────────────────────────────────────────────────────


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
        {
            "hitl": "hitl",
            "rag_mapping": "rag_mapping",
            "generate_cypher": "generate_cypher",
            "build_graph": "build_graph",
        },
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

    return graph.compile(checkpointer=checkpointer, interrupt_before=["hitl"] if production else [])


def run_builder(
    raw_documents: list[str],
    ddl_paths: list[str],
    *,
    production: bool = False,
    clear_graph: bool = False,
    use_lazy_extraction: bool | None = None,
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
    settings = get_settings()
    lazy_mode = settings.use_lazy_extraction if use_lazy_extraction is None else use_lazy_extraction
    initial: BuilderState = {
        "chunks": chunks,
        "ddl_paths": ddl_paths,
        "source_doc": str(raw_documents[0]) if raw_documents else "unknown",
        "use_lazy_extraction": lazy_mode,
        "triplets": [],
        "entities": [],
        "tables": [],
        "enriched_tables": [],
        "pending_tables": [],
        "completed_tables": [],
        "skip_hitl": not production,  # bypass interrupt() in non-production runs
    }
    config = {"configurable": {"thread_id": f"builder-{uuid.uuid4().hex[:8]}"}}
    final_state: BuilderState = graph.invoke(initial, config=config)
    return final_state
