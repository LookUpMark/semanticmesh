"""Build nodes for the Builder Graph.

This module contains the graph building logic, including Cypher generation,
healing, and execution with fallback strategies.
"""

from __future__ import annotations

import json as _json
import logging
from typing import Any

from src.config.llm_factory import get_reasoning_llm
from src.config.logging import NodeTimer, get_logger, log_node_event
from src.config.settings import get_settings
from src.graph.cypher_builder import build_attribute_cypher, build_fk_cypher, build_upsert_cypher
from src.graph.cypher_generator import generate_cypher
from src.graph.cypher_healer import heal_cypher
from src.graph.neo4j_client import Neo4jClient
from src.models.schemas import EnrichedTableSchema, Entity, MappingProposal
from src.models.state import BuilderState
from src.prompts.few_shot import load_cypher_examples
from src.retrieval.embeddings import embed_text, get_embeddings
from src.utils.text_utils import is_valid_entity_name, normalize_concept_name

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


def _entity_from_table(concept_name: str, table: EnrichedTableSchema) -> Entity:
    """Build a best-effort Entity from table metadata when entity resolution yields no match.

    This prevents BusinessConcept nodes from being written with empty properties
    when the RAG Mapper produces a concept name that doesn't match any resolved
    entity (e.g. because the LLM normalised 'SALES_ORDER_HDR' → 'SalesOrder').
    The table's LLM-enriched description and DDL source are rich enough to
    populate definition, provenance_text, and source_doc meaningfully.
    """
    definition = getattr(table, "table_description", None) or table.comment or ""
    provenance_text = (table.ddl_source or "")[: get_settings().provenance_max_chars].strip()
    return Entity(
        name=concept_name,
        definition=definition,
        synonyms=[],
        provenance_text=provenance_text,
        source_doc=table.source_file or "",
    )


def _node_generate_cypher(state: BuilderState) -> dict[str, Any]:
    """Generate MERGE-based Cypher from mapping proposal."""
    with NodeTimer() as timer:
        settings = get_settings()
        if bool(state.get("use_lazy_extraction", settings.use_lazy_extraction)):
            logger.info("Lazy mode: skipping LLM Cypher generation.")
            log_node_event(logger, "generate_cypher", "lazy mode", "skipped", timer.elapsed_ms)
            return {"current_cypher": None, "healing_attempts": 0}

        proposal: MappingProposal | None = state.get("mapping_proposal")
        if not proposal:
            logger.warning("No mapping_proposal in generate_cypher — skipping.")
            log_node_event(logger, "generate_cypher", "no proposal", "skipped", timer.elapsed_ms)
            return {"current_cypher": None, "healing_attempts": 0}

        llm = get_reasoning_llm()
        table = state.get("current_table")
        resolved = _find_entity_for_concept(
            proposal.mapped_concept or "", state.get("current_entities") or []
        )
        entity = resolved or _entity_from_table(proposal.mapped_concept or "Unknown", table)
        few_shot = load_cypher_examples(settings.few_shot_cypher_examples)
        cypher = generate_cypher(proposal, table, entity, few_shot, llm)
        log_node_event(
            logger,
            "generate_cypher",
            f"table={proposal.table_name}",
            "cypher generated",
            timer.elapsed_ms,
            model_used=settings.llm_model_reasoning,
        )
        return {"current_cypher": cypher, "healing_attempts": 0}


def _node_heal_cypher(state: BuilderState) -> dict[str, Any]:
    """Validate and heal Cypher via dry-run + LLM reflection loop."""
    with NodeTimer() as timer:
        settings = get_settings()
        if bool(state.get("use_lazy_extraction", settings.use_lazy_extraction)):
            log_node_event(logger, "heal_cypher", "lazy mode", "skipped", timer.elapsed_ms)
            return {"cypher_failed": True, "current_cypher": None}

        if not settings.enable_cypher_healing:
            logger.info("Cypher healing disabled — using deterministic builder fallback.")
            log_node_event(logger, "heal_cypher", "disabled", "fallback", timer.elapsed_ms)
            return {"cypher_failed": True, "current_cypher": None}

        proposal: MappingProposal | None = state.get("mapping_proposal")
        if not proposal:
            logger.warning("No mapping_proposal in heal_cypher — marking as failed.")
            log_node_event(logger, "heal_cypher", "no proposal", "failed", timer.elapsed_ms)
            return {"cypher_failed": True, "current_cypher": None}

        llm = get_reasoning_llm()
        cypher: str = state.get("current_cypher") or ""

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
            log_node_event(
                logger,
                "heal_cypher",
                f"table={proposal.table_name}",
                "healing failed",
                timer.elapsed_ms,
            )
            return {"cypher_failed": True, "current_cypher": None}

        log_node_event(
            logger, "heal_cypher", f"table={proposal.table_name}", "healed", timer.elapsed_ms
        )
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

    enriched_cols_json = ""
    if hasattr(table, "enriched_columns") and table.enriched_columns:
        enriched_cols_json = _json.dumps(
            [
                {"original": ec.original_name, "enriched": ec.enriched_name}
                for ec in table.enriched_columns
            ]
        )

    return {
        "concept_name": normalize_concept_name(proposal.mapped_concept or "Unknown"),
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
        "source_file": table.source_file or "",
        "table_comment": table.comment or "",
        "enriched_table_name": getattr(table, "enriched_table_name", None),
        "enriched_columns": enriched_cols_json,
        "table_description": getattr(table, "table_description", None) or "",
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
    with NodeTimer() as timer:
        proposal: MappingProposal | None = state.get("mapping_proposal")
        table: EnrichedTableSchema | None = state.get("current_table")

        if not proposal or not table:
            logger.warning("Missing proposal or table in build_graph — skipping.")
            log_node_event(logger, "build_graph", "no proposal/table", "skipped", timer.elapsed_ms)
            return {}

        llm_cypher: str | None = state.get("current_cypher")
        cypher_failed: bool = state.get("cypher_failed", False)
        lazy_mode: bool = bool(state.get("use_lazy_extraction", get_settings().use_lazy_extraction))

        # Normalize the concept name to Title Case before any graph writes
        concept_name: str = normalize_concept_name(proposal.mapped_concept or "Unknown")

        # Reject concept names that are still garbage after normalization
        # Fallback to enriched_table_name (e.g. "Shipment" for SHIPMENT) instead of skipping entirely
        if not is_valid_entity_name(concept_name):
            fallback_name = normalize_concept_name(
                getattr(table, "enriched_table_name", None) or table.table_name
            )
            if is_valid_entity_name(fallback_name):
                logger.warning(
                    "Concept name '%s' (raw: '%s') rejected by quality gate — "
                    "falling back to enriched table name '%s'.",
                    concept_name,
                    proposal.mapped_concept,
                    fallback_name,
                )
                concept_name = fallback_name
            else:
                logger.warning(
                    "Concept name '%s' (raw: '%s') rejected by quality gate — skipping graph write.",
                    concept_name,
                    proposal.mapped_concept,
                )
                log_node_event(
                    logger,
                    "build_graph",
                    f"table={proposal.table_name}",
                    "rejected concept name",
                    timer.elapsed_ms,
                )
                completed = list(state.get("completed_tables") or [])
                completed.append(proposal.table_name)
                return {"completed_tables": completed}

        # Resolve entity early — needed for both LLM and fallback paths.
        # If no matching resolved entity exists (e.g. the RAG Mapper normalised the
        # concept name differently from what entity resolution produced), fall back
        # to a best-effort Entity built from the table's enriched metadata so that
        # BusinessConcept nodes are never written with empty properties.
        resolved = _find_entity_for_concept(concept_name, state.get("current_entities") or [])
        entity_for_write = resolved or _entity_from_table(concept_name, table)
        if resolved is None:
            logger.warning(
                "No resolved entity matched concept '%s' — using table metadata as fallback "
                "(definition from table_description, provenance from ddl_source).",
                concept_name,
            )

        if llm_cypher and not cypher_failed and not lazy_mode:
            blocked_keywords = ("DETACH DELETE", "DROP ", "REMOVE ", "DELETE ")
            upper_cypher = llm_cypher.upper()
            for kw in blocked_keywords:
                if kw in upper_cypher:
                    logger.warning(
                        "LLM Cypher contains blocked keyword '%s' — falling back to deterministic builder.",
                        kw.strip(),
                    )
                    cypher_failed = True
                    break
            if not cypher_failed:
                logger.info("Executing LLM-healed Cypher for '%s'.", proposal.table_name)
                exec_cypher = llm_cypher
                # Safety-net params: the system prompt tells the LLM to inline values,
                # but it sometimes copies parameterised style from few-shot examples.
                # Providing the params avoids ParameterMissing errors at runtime.
                exec_params = _build_llm_cypher_params(proposal, table, entity_for_write)
        else:
            logger.info(
                "LLM Cypher failed for '%s' — falling back to deterministic builder.",
                proposal.table_name,
            )
            exec_cypher, exec_params = build_upsert_cypher(proposal, table, entity=entity_for_write)

        with Neo4jClient() as client:
            try:
                client.execute_cypher(exec_cypher, exec_params)
            except Exception as cypher_exec_err:
                # LLM Cypher may use CREATE instead of MERGE, causing constraint
                # violations when the same BusinessConcept already exists.
                # Fallback to deterministic builder which always uses MERGE.
                from neo4j.exceptions import ConstraintError

                if isinstance(cypher_exec_err, ConstraintError):
                    logger.warning(
                        "LLM Cypher failed with constraint error for '%s' — "
                        "retrying with deterministic builder: %s",
                        proposal.table_name,
                        cypher_exec_err,
                    )
                    fallback_cypher, fallback_params = build_upsert_cypher(
                        proposal, table, entity=entity_for_write
                    )
                    client.execute_cypher(fallback_cypher, fallback_params)
                else:
                    raise
            logger.info("Graph updated for table '%s'.", proposal.table_name)

            # ── Normalize BusinessConcept name created by LLM Cypher ──────────
            # The LLM Cypher may create the BusinessConcept with a name that
            # differs from our quality-gated `concept_name`. Force-rename it.
            if proposal.mapped_concept:
                client.execute_cypher(
                    "MATCH (bc:BusinessConcept)-[:MAPPED_TO]->(pt:PhysicalTable) "
                    "WHERE toLower(pt.table_name) = toLower($tbl) AND bc.name <> $target "
                    "SET bc.name = $target",
                    {"tbl": table.table_name, "target": concept_name},
                )
                # ── Ensure MAPPED_TO edge exists (LLM Cypher may omit it) ─────
                client.execute_cypher(
                    "MATCH (bc:BusinessConcept {name: $bc_name}) "
                    "MATCH (pt:PhysicalTable) WHERE toLower(pt.table_name) = toLower($tbl) "
                    "MERGE (bc)-[r:MAPPED_TO]->(pt) "
                    "ON CREATE SET r.confidence = $conf, r.validated_by = 'llm_judge', r.created_at = datetime() "
                    "ON MATCH SET r.confidence = $conf, r.updated_at = datetime()",
                    {"bc_name": concept_name, "tbl": table.table_name, "conf": proposal.confidence},
                )

            # ── Consolidate property updates into single Cypher call ──────────
            # Combines: normalization, source_file stamp, enriched metadata
            set_clauses: list[str] = ["pt.table_name = $canonical", "pt.name = $canonical"]
            merged_params: dict[str, Any] = {
                "name": table.table_name,
                "canonical": table.table_name,
            }
            if table.source_file:
                set_clauses.append("pt.source_file = $source_file")
                merged_params["source_file"] = table.source_file
            if getattr(table, "enriched_table_name", None):
                set_clauses.append("pt.enriched_table_name = $etn")
                merged_params["etn"] = table.enriched_table_name
            if getattr(table, "table_description", None):
                set_clauses.append("pt.table_description = $td")
                merged_params["td"] = table.table_description
            if getattr(table, "enriched_columns", None):
                set_clauses.append("pt.enriched_columns = $ec")
                merged_params["ec"] = _json.dumps(
                    [
                        {"original": ec.original_name, "enriched": ec.enriched_name}
                        for ec in table.enriched_columns
                    ]
                )
            if table.comment:
                set_clauses.append("pt.comment = $cmt")
                merged_params["cmt"] = table.comment

            client.execute_cypher(
                "MATCH (pt:PhysicalTable) "
                "WHERE toLower(pt.table_name) = toLower($name) "
                f"SET {', '.join(set_clauses)}",
                merged_params,
            )

            fk_statements = build_fk_cypher(table)
            if fk_statements:
                try:
                    client.execute_batch(fk_statements)
                    logger.info(
                        "FK edges: %d batched for table '%s'.", len(fk_statements), table.table_name
                    )
                except Exception as exc:
                    logger.warning("Could not write FK edges for '%s': %s", table.table_name, exc)

            # ── Attribute nodes: one per column for fine-grained retrieval ──
            attr_statements = build_attribute_cypher(table)
            if attr_statements:
                try:
                    client.execute_batch(attr_statements)
                    logger.info(
                        "Attribute nodes: %d upserted for table '%s'.",
                        len(attr_statements),
                        table.table_name,
                    )
                    # Set embeddings on Attribute nodes
                    model = get_embeddings()
                    attr_texts = [params["description"] for _, params in attr_statements]
                    attr_names = [params["attr_name"] for _, params in attr_statements]
                    vectors = model.encode(attr_texts, batch_size=len(attr_texts))
                    for attr_name, vec in zip(attr_names, vectors):
                        client.execute_cypher(
                            "MATCH (a:Attribute {name: $name}) SET a.embedding = $emb",
                            {"name": attr_name, "emb": vec.tolist()},
                        )
                    logger.info("Embeddings set for %d Attribute nodes.", len(attr_names))
                except Exception as exc:
                    logger.warning(
                        "Could not write Attribute nodes for '%s': %s", table.table_name, exc
                    )

            if proposal.mapped_concept:
                try:
                    model = get_embeddings()
                    vector = embed_text(concept_name, model=model)
                    for _attempt in range(3):
                        try:
                            client.execute_cypher(
                                "MATCH (c:BusinessConcept {name: $name}) SET c.embedding = $emb",
                                {"name": concept_name, "emb": vector},
                            )
                            logger.info("Embedding set for BusinessConcept '%s'.", concept_name)
                            break
                        except Exception:
                            if _attempt == 2:
                                raise
                except Exception as exc:
                    logger.warning("Could not set embedding for '%s': %s", concept_name, exc)
                    state.setdefault("embedding_failures", []).append(concept_name)

            # ── MENTIONS edges: link Chunk nodes to this BusinessConcept ──
            if proposal.mapped_concept:
                triplets = state.get("triplets") or []
                concept_lower = concept_name.lower()
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
                            {"idxs": list(chunk_indexes), "concept": concept_name},
                        )
                        logger.info(
                            "MENTIONS edges: %d chunks → '%s' (batch).",
                            len(chunk_indexes),
                            concept_name,
                        )
                    except Exception as exc:
                        logger.warning(
                            "Could not create MENTIONS edges → '%s': %s",
                            concept_name,
                            exc,
                        )

        completed = list(state.get("completed_tables") or [])
        completed.append(proposal.table_name)
        log_node_event(
            logger,
            "build_graph",
            f"table={proposal.table_name}",
            f"{len(completed)} completed",
            timer.elapsed_ms,
        )
        return {"completed_tables": completed}


def _route_after_heal(state: BuilderState) -> str:
    """Route after Cypher healing: always proceed to build_graph.

    ``build_graph`` implements a primary/fallback strategy internally:
    - ``cypher_failed=False`` -> LLM-healed Cypher executed directly
    - ``cypher_failed=True``  -> deterministic builder used as fallback
    """
    return "build_graph"
