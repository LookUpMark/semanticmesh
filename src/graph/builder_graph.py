"""Builder LangGraph — EP-11 / US-11-01.

Wires all ingestion nodes (extraction -> ER -> DDL -> enrichment -> mapping ->
validation -> HITL -> Cypher -> graph write) into a compiled StateGraph.
"""

from __future__ import annotations

import logging
import uuid
from pathlib import Path
from typing import Any

from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import END, StateGraph

from src.config.llm_factory import (
    get_extraction_llm,
    get_lightweight_llm,
    get_midtier_llm,
)
from src.config.logging import get_logger
from src.config.settings import get_settings
from src.config.tracing import BuilderTrace
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
from src.ingestion.file_registry import (
    check_file_status,
    compute_file_sha,
    get_orphaned_files,
    purge_file_data,
    register_file,
)
from src.ingestion.pdf_loader import chunk_documents_hierarchical, load_pdf
from src.ingestion.schema_enricher import enrich_all
from src.mapping.hitl import hitl_node
from src.mapping.rag_mapper import propose_mapping, propose_mapping_heuristic
from src.mapping.retrieval import build_retrieval_query, retrieve_top_entities
from src.models.schemas import EnrichedTableSchema, Entity
from src.models.state import BuilderState
from src.prompts.few_shot import format_mapping_examples, load_mapping_examples
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
    llm = get_lightweight_llm()  # kept for singleton definition synthesis (when enabled)
    triplets = state.get("triplets") or []
    source_doc = state.get("source_doc", "unknown")
    # ER judge itself uses midtier internally (see entity_resolver.resolve_entities)
    entities = resolve_entities(triplets, embeddings, llm, source_doc)
    return {"entities": entities}


def _node_parse_ddl(state: BuilderState) -> dict[str, Any]:
    """Parse DDL files into TableSchema objects."""
    ddl_paths: list[str] = state.get("ddl_paths") or []
    tables = []
    for path in ddl_paths:
        tables.extend(parse_ddl_file(Path(path)))
    return {"tables": tables}


def _node_enrich_schema(state: BuilderState) -> dict[str, Any]:
    """Enrich table schemas with acronym expansion and descriptions."""
    settings = get_settings()
    if not settings.enable_schema_enrichment:
        tables = state.get("tables") or []
        logger.info("Schema enrichment disabled — promoting raw parsed tables.")
        promoted = [EnrichedTableSchema.from_table_schema(t) for t in tables]
        return {"enriched_tables": promoted}
    llm = get_lightweight_llm()
    tables = state.get("tables") or []
    enriched = enrich_all(tables, llm)
    return {"enriched_tables": enriched}


def _node_rag_mapping(state: BuilderState) -> dict[str, Any]:
    """Generate RAG-augmented mapping proposal for current table."""
    settings = get_settings()
    use_lazy = bool(state.get("use_lazy_extraction", settings.use_lazy_extraction))
    llm = get_midtier_llm()
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
            few_shot_examples=format_mapping_examples(load_mapping_examples()),
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
    """Route after graph build: process next table or save_trace/END."""
    if state.get("pending_tables"):
        return "rag_mapping"
    # Always go through save_trace before END (saves trace if enabled, otherwise passes through)
    return "save_trace"


# ─────────────────────────────────────────────────────────────────────────────
# Debug Tracing Nodes
# ─────────────────────────────────────────────────────────────────────────────


def _node_save_trace(state: BuilderState) -> dict[str, Any]:
    """No-op graph node — trace is saved AFTER graph.invoke() in run_builder().

    This node exists only to provide a terminal routing target for
    _route_after_build. The actual trace.save() happens after the trace
    has been fully populated with final state data.
    """
    return {}


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
    graph.add_node("save_trace", _node_save_trace)

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
            "save_trace": "save_trace",
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
        {"rag_mapping": "rag_mapping", "save_trace": "save_trace"},
    )
    graph.add_edge("save_trace", END)

    # Checkpointer
    if production:
        try:
            import sqlite3
            from langgraph.checkpoint.sqlite import SqliteSaver

            settings = get_settings()
            conn = sqlite3.connect(settings.sqlite_checkpoint_path, check_same_thread=False)
            checkpointer = SqliteSaver(conn)
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
    force_rebuild: bool = False,
    use_lazy_extraction: bool | None = None,
    trace_enabled: bool = False,
    study_id: str = "manual",
    job_id: str | None = None,
) -> BuilderState:
    """Convenience wrapper: compile graph and invoke with document paths.

    Args:
        raw_documents:  List of file paths to PDF documents.
        ddl_paths:      List of file paths to DDL SQL files.
        production:     Compile with ``SqliteSaver`` if True.
        clear_graph:    If True, delete all nodes and relationships before running.
                        Use in development/demo to avoid stale data from prior runs.
        force_rebuild:  If True, bypass SHA-256 change detection and re-ingest all
                        files regardless of whether their content has changed.
        trace_enabled:  If True, enable detailed debug tracing of the pipeline.
        study_id:       Study ID for trace naming (e.g., "AB-00").

    Returns:
        Final ``BuilderState`` after graph completion.
    """
    from src.retrieval.bm25_retriever import invalidate_bm25_cache  # local import avoids cycle

    settings = get_settings()

    # ── Incremental ingestion: SHA-based change detection ────────────────────
    # When clear_graph=True the whole graph is wiped, so all files are new.
    # When force_rebuild=True we skip the SHA check and re-ingest everything.
    skipped_files: list[str] = []
    docs_to_ingest: list[str] = list(raw_documents)

    if not clear_graph and not force_rebuild and raw_documents:
        with Neo4jClient() as reg_client:
            # current_paths includes both doc files AND DDL files so that
            # DDL entries in the SourceFile registry are never mistaken for orphans.
            current_paths: set[str] = {str(Path(p).resolve()) for p in ddl_paths}
            filtered_docs: list[str] = []
            for doc_path in raw_documents:
                canonical = str(Path(doc_path).resolve())
                current_paths.add(canonical)
                try:
                    sha = compute_file_sha(doc_path)
                    status = check_file_status(reg_client, canonical, sha)
                except FileNotFoundError:
                    logger.warning("File not found, skipping: %s", doc_path)
                    continue

                if status == "unchanged":
                    logger.info("Skipping unchanged file: %s", doc_path)
                    skipped_files.append(doc_path)
                else:
                    if status == "modified":
                        logger.info(
                            "File modified — purging stale data and re-ingesting: %s", doc_path
                        )
                        purge_file_data(reg_client, canonical)
                    filtered_docs.append(doc_path)

            # Purge files that existed in a previous run but are absent now
            orphans = get_orphaned_files(reg_client, current_paths)
            for orphan_path in orphans:
                logger.info("Purging orphaned file data: %s", orphan_path)
                purge_file_data(reg_client, orphan_path)

            docs_to_ingest = filtered_docs

    # ── DDL SHA check — skip unchanged schema files too ──────────────────────
    ddl_to_ingest: list[str] = list(ddl_paths)
    if not clear_graph and not force_rebuild and ddl_paths:
        with Neo4jClient() as reg_client:
            filtered_ddl: list[str] = []
            for ddl_path in ddl_paths:
                canonical = str(Path(ddl_path).resolve())
                try:
                    sha = compute_file_sha(ddl_path)
                    status = check_file_status(reg_client, canonical, sha)
                except FileNotFoundError:
                    logger.warning("DDL file not found, skipping: %s", ddl_path)
                    continue
                if status == "unchanged":
                    logger.info("Skipping unchanged DDL: %s", ddl_path)
                    skipped_files.append(ddl_path)
                elif status == "modified":
                    logger.info(
                        "DDL modified — purging stale tables and re-processing: %s",
                        ddl_path,
                    )
                    purge_file_data(reg_client, canonical)
                    filtered_ddl.append(ddl_path)
                else:
                    filtered_ddl.append(ddl_path)
            ddl_to_ingest = filtered_ddl


    if not docs_to_ingest and not ddl_to_ingest:
        logger.info(
            "All %d file(s) unchanged — nothing to re-ingest. "
            "Skipped: %s",
            len(skipped_files),
            skipped_files,
        )
        # Return a minimal state so callers can observe skipped_files count
        return BuilderState(  # type: ignore[call-arg]
            chunks=[],
            ddl_paths=[],
            source_doc="",
            triplets=[],
            entities=[],
            tables=[],
            enriched_tables=[],
            pending_tables=[],
            completed_tables=[],
            skipped_files=skipped_files,
        )

    # ── Load and chunk only the files that need (re-)ingestion ───────────────
    # Load all documents first, then chunk in one pass so parent_chunk_index is
    # globally unique across all source files (avoids index collisions in Neo4j).
    # PDF loading is I/O-bound so we parallelise across files.
    all_docs: list = []
    if len(docs_to_ingest) > 1:
        from concurrent.futures import ThreadPoolExecutor, as_completed
        with ThreadPoolExecutor(max_workers=min(4, len(docs_to_ingest))) as _pool:
            futures = {_pool.submit(load_pdf, Path(p)): p for p in docs_to_ingest}
            for fut in as_completed(futures):
                all_docs.extend(fut.result())
    else:
        for doc_path in docs_to_ingest:
            all_docs.extend(load_pdf(Path(doc_path)))
    all_parents, all_children = chunk_documents_hierarchical(all_docs)

    # Triplet extraction and MENTIONS edges operate on parents (richer 512-tok context).
    chunks = all_parents

    # Initialize trace if enabled
    builder_trace: BuilderTrace | None = None
    if trace_enabled:
        doc_paths = [Path(p) for p in raw_documents]
        ddl_path_objs = [Path(p) for p in ddl_paths]
        builder_trace = BuilderTrace.create(
            study_id=study_id,
            settings=settings,
            doc_paths=doc_paths,
            ddl_paths=ddl_path_objs,
        )
        # Record initial chunks (parents used for extraction)
        chunk_dicts = [
            {
                "chunk_id": i,
                "text": c.text,
                "source": c.metadata.get("source", ""),
                "page": c.metadata.get("page", 0),
                "token_count": c.metadata.get("token_count", 0),
            }
            for i, c in enumerate(chunks)
        ]
        builder_trace.record_chunks(chunk_dicts)
        logger.info(f"Debug tracing enabled for study {study_id}")

    # Ensure Neo4j schema (constraints + vector index) exists before writing.
    with Neo4jClient() as client:
        if clear_graph:
            client.execute_cypher("MATCH (n) DETACH DELETE n")
            logger.info("Graph cleared before builder run.")
        setup_schema(client)

        # ── Persist parent chunks — single UNWIND batch ───────────────────────
        if all_parents:
            client.execute_cypher(
                "UNWIND $rows AS row "
                "MERGE (pc:ParentChunk {parent_chunk_index: row.idx, source_doc: row.src}) "
                "ON CREATE SET pc.text = row.text, pc.page = row.page, pc.created_at = datetime() "
                "ON MATCH  SET pc.text = row.text, pc.updated_at = datetime()",
                {"rows": [
                    {
                        "idx": p.chunk_index,
                        "src": p.metadata.get("source", ""),
                        "text": p.text,
                        "page": p.metadata.get("page", ""),
                    }
                    for p in all_parents
                ]},
            )
            logger.info("Persisted %d ParentChunk nodes (batch).", len(all_parents))

        # ── Persist child chunks with embeddings — single UNWIND batch ────────
        if all_children:
            emb_model = get_embeddings()
            child_texts = [c.text for c in all_children]
            vectors = emb_model.encode(child_texts, batch_size=32)
            client.execute_cypher(
                "UNWIND $rows AS row "
                "MERGE (c:Chunk {chunk_index: row.idx, source_doc: row.src}) "
                "ON CREATE SET c.text = row.text, c.page = row.page, "
                "c.embedding = row.emb, c.created_at = datetime() "
                "ON MATCH  SET c.text = row.text, c.embedding = row.emb, c.updated_at = datetime()",
                {"rows": [
                    {
                        "idx": child.chunk_index,
                        "src": child.metadata.get("source", ""),
                        "text": child.text,
                        "page": child.metadata.get("page", ""),
                        "emb": vectors[i].tolist(),
                    }
                    for i, child in enumerate(all_children)
                ]},
            )
            logger.info("Persisted %d Chunk nodes with embeddings (batch).", len(all_children))

        # ── Wire CHILD_OF edges — single UNWIND batch ─────────────────────────
        edge_rows = [
            {
                "cidx": child.chunk_index,
                "pidx": child.parent_chunk_index,
                "src": child.metadata.get("source", ""),
            }
            for child in all_children
            if child.parent_chunk_index is not None
        ]
        if edge_rows:
            client.execute_cypher(
                "UNWIND $rows AS row "
                "MATCH (c:Chunk {chunk_index: row.cidx, source_doc: row.src}) "
                "MATCH (pc:ParentChunk {parent_chunk_index: row.pidx, source_doc: row.src}) "
                "MERGE (c)-[:CHILD_OF]->(pc)",
                {"rows": edge_rows},
            )
            logger.info("Created CHILD_OF edges for %d children (batch).", len(edge_rows))

        # ── Register ingested files in the SourceFile registry ────────────────
        # Always register after a successful ingestion so that subsequent
        # incremental runs (clear_graph=False) can skip unchanged files.
        # Only skip when force_rebuild=True (explicit bypass of change detection).
        if not force_rebuild:
            # Group child chunks by source_doc to get per-file child count
            from collections import Counter as _Counter  # local import
            child_counts: dict[str, int] = _Counter(
                c.metadata.get("source", "") for c in all_children
            )
            for doc_path in docs_to_ingest:
                canonical = str(Path(doc_path).resolve())
                try:
                    sha = compute_file_sha(doc_path)
                    # Use canonical path as source_doc key (matches what load_pdf stores)
                    src_key = Path(doc_path).name  # basename only, as stored in metadata
                    count = child_counts.get(src_key, child_counts.get(canonical, 0))
                    register_file(client, canonical, sha, count)
                except Exception as exc:  # noqa: BLE001
                    logger.warning("Could not register file '%s': %s", doc_path, exc)
            # Also register DDL files (chunk_count=0 — they produce nodes, not chunks)
            for ddl_path in ddl_to_ingest:
                canonical = str(Path(ddl_path).resolve())
                try:
                    sha = compute_file_sha(ddl_path)
                    register_file(client, canonical, sha, 0)
                except Exception as exc:  # noqa: BLE001
                    logger.warning("Could not register DDL '%s': %s", ddl_path, exc)

    graph = build_builder_graph(production=production)
    lazy_mode = settings.use_lazy_extraction if use_lazy_extraction is None else use_lazy_extraction
    initial: BuilderState = {
        "chunks": chunks,
        "ddl_paths": ddl_to_ingest,
        "source_doc": str(docs_to_ingest[0]) if docs_to_ingest else "unknown",
        "use_lazy_extraction": lazy_mode,
        "triplets": [],
        "entities": [],
        "tables": [],
        "enriched_tables": [],
        "pending_tables": [],
        "completed_tables": [],
        "skipped_files": skipped_files,
        "skip_hitl": not production,  # bypass interrupt() in non-production runs
        "trace_enabled": trace_enabled,
        "builder_trace": builder_trace,
        "trace_output_dir": settings.trace_output_dir if trace_enabled else "",
    }
    config = {"configurable": {"thread_id": f"builder-{uuid.uuid4().hex[:8]}"}}

    # Use graph.stream() so each completed node is visible for SSE step tracking.
    # The loop collects the last emitted state as the final_state.
    if job_id is not None:
        from src.api.jobs import set_step as _set_step  # local import avoids circular dep
        final_state: BuilderState = {}  # type: ignore[assignment]
        for node_output in graph.stream(initial, config=config):
            # node_output is {node_name: state_delta}
            node_name = next(iter(node_output))
            _set_step(job_id, node_name)
            node_delta = node_output[node_name]
            if node_delta is not None:
                final_state = {**final_state, **node_delta}
    else:
        final_state = graph.invoke(initial, config=config)

    # ── MENTIONS edge repair for PDF-only incremental updates ─────────────────
    # When PDFs changed but DDL was unchanged (ddl_to_ingest=[]), the graph exits
    # early after triplet extraction without running the per-table mapping loop,
    # so MENTIONS edges are not created for the new chunks.  Repair them here by
    # matching triplet subject/object against ALL existing BusinessConcepts.
    if docs_to_ingest and not ddl_to_ingest:
        triplets_for_repair = final_state.get("triplets") or []
        new_basenames = {Path(p).name for p in docs_to_ingest}
        logger.info(
            "PDF-only change: repairing MENTIONS edges for %d triplet(s) "
            "against existing BusinessConcepts (sources: %s).",
            len(triplets_for_repair),
            new_basenames,
        )
        with Neo4jClient() as repair_client:
            bc_rows = repair_client.execute_cypher(
                "MATCH (bc:BusinessConcept) RETURN bc.name AS name"
            )
            bc_names: list[str] = [r["name"] for r in bc_rows if r.get("name")]
            mentions_count = 0
            for bc_name in bc_names:
                concept_lower = bc_name.lower()
                chunk_indexes: set[int] = set()
                for t in triplets_for_repair:
                    if t.source_chunk_index is not None and (
                        concept_lower in t.subject.lower()
                        or concept_lower in t.object.lower()
                    ):
                        chunk_indexes.add(t.source_chunk_index)
                for idx in chunk_indexes:
                    try:
                        repair_client.execute_cypher(
                            "MATCH (ch:Chunk {chunk_index: $idx}) "
                            "WHERE ch.source_doc IN $srcs "
                            "MATCH (bc:BusinessConcept {name: $concept}) "
                            "MERGE (ch)-[:MENTIONS]->(bc)",
                            {
                                "idx": idx,
                                "concept": bc_name,
                                "srcs": list(new_basenames),
                            },
                        )
                        mentions_count += 1
                    except Exception as exc:  # noqa: BLE001
                        logger.warning(
                            "MENTIONS repair: could not link chunk %d → '%s': %s",
                            idx, bc_name, exc,
                        )
            logger.info("MENTIONS repair: created %d edge(s).", mentions_count)

    # Invalidate BM25 cache — graph contents may have changed
    try:
        invalidate_bm25_cache()
    except Exception:  # noqa: BLE001
        pass

    # Populate trace with final state data
    if trace_enabled and builder_trace:
        # Record triplets
        triplets = final_state.get("triplets", [])
        triplet_dicts = [
            {
                "chunk_index": t.source_chunk_index,
                "subject": t.subject,
                "predicate": t.predicate,
                "object": t.object,
                "confidence": t.confidence,
            }
            for t in triplets
        ]
        builder_trace.record_triplets(triplet_dicts)

        # Record entities
        entities = final_state.get("entities", [])
        entity_dicts = [
            {
                "name": e.name,
                "definition": e.definition,
                "synonyms": e.synonyms,
                "provenance_text": e.provenance_text,
                "source_doc": e.source_doc,
            }
            for e in entities
        ]
        builder_trace.entities_post_resolution = entity_dicts[:100]
        builder_trace.resolution_summary = {
            "entities_post": len(entities),
        }

        # Record schema processing
        tables = final_state.get("tables", [])
        enriched_tables = final_state.get("enriched_tables", [])
        table_dicts = [
            {
                "name": t.table_name,
                "columns": [{"name": c.name, "type": c.data_type} for c in t.columns],
            }
            for t in tables
        ]
        # Convert enriched tables to dicts for tracing
        enriched_table_dicts = [
            {
                "name": t.enriched_table_name or t.table_name,
                "description": t.table_description or "",
            }
            for t in enriched_tables
        ]
        builder_trace.record_schema_processing(table_dicts, enriched_table_dicts)

        # Record graph stats
        with Neo4jClient() as client:
            node_count = client.execute_cypher("MATCH (n) RETURN count(n) as count")[0]["count"]
            rel_count = client.execute_cypher("MATCH ()-[r]->() RETURN count(r) as count")[0][
                "count"
            ]
            builder_trace.neo4j_summary = {
                "total_nodes": node_count,
                "total_relationships": rel_count,
                "completed_tables": len(final_state.get("completed_tables", [])),
            }

        # Save trace AFTER it has been fully populated (fixes timing bug)
        output_dir = Path(settings.trace_output_dir)
        trace_path = builder_trace.save(output_dir)
        logger.info("Builder trace saved to %s", trace_path)

    return final_state
