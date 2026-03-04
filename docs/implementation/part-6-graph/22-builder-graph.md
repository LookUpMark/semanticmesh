# Part 6 — `src/graph/builder_graph.py`

## 1. Purpose & Context

**Epic:** EP-11 Builder LangGraph Orchestration  
**US-11-01** — Builder StateGraph Definition

`builder_graph` assembles all previous nodes into a single LangGraph `StateGraph` that runs end-to-end ingestion:

```
extract_triplets → entity_resolution → parse_ddl → enrich_schema
→ rag_mapping → validate_mapping [→ hitl] → generate_cypher
→ test+heal_cypher → build_graph → END
```

Retry counters in `BuilderState` (`reflection_attempts`, `healing_attempts`) prevent infinite loops. The graph is compiled with `interrupt_before=["hitl"]` so a human reviewer can pause execution when confidence is low.

---

## 2. Prerequisites

All previous implementation steps (01–21) must be complete:

- `src/models/state.py` — `BuilderState` TypedDict (step 6)
- `src/extraction/triplet_extractor.py` — `extract_all_triplets` (step 12)
- `src/resolution/entity_resolver.py` — `resolve_entities` (step 15)
- `src/ingestion/ddl_parser.py` — `parse_ddl_file` (step 10)
- `src/ingestion/schema_enricher.py` — `enrich_all` (step 11)
- `src/mapping/rag_mapper.py` — `propose_mapping` (step 16)
- `src/mapping/validator.py` — `validate_schema`, `critic_review`, `build_reflection_prompt` (step 17)
- `src/mapping/hitl.py` — `hitl_node` (step 18)
- `src/graph/cypher_generator.py` — `generate_cypher` (step 20)
- `src/graph/cypher_healer.py` — `heal_cypher` (step 21)
- `src/graph/neo4j_client.py` — `Neo4jClient`, `setup_schema` (step 19)
- `src/prompts/few_shot.py` — `load_cypher_examples` (step 8)
- `src/retrieval/embeddings.py` — `get_embeddings` (step 23)
- `src/config/settings.py`, `src/config/llm_factory.py`, `src/config/logging.py`

---

## 3. Public API

| Symbol | Signature | Description |
|---|---|---|
| `build_builder_graph` | `(*, production: bool = False) -> CompiledStateGraph` | Compile the full Builder LangGraph |
| `run_builder` | `(raw_documents: list[str], ddl_paths: list[str], *, production: bool = False) -> BuilderState` | Convenience entry point |

---

## 4. Full Implementation

```python
"""Builder LangGraph — EP-11 / US-11-01.

Wires all ingestion nodes (extraction → ER → DDL → enrichment → mapping →
validation → HITL → Cypher → graph write) into a compiled StateGraph.
"""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Any

from langchain_core.documents import Document as LCDocument
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import END, StateGraph
from langgraph.types import Command

from src.config.llm_factory import get_extraction_llm, get_reasoning_llm
from src.config.logging import get_logger
from src.config.settings import get_settings
from src.extraction.triplet_extractor import extract_all_triplets
from src.graph.cypher_generator import generate_cypher
from src.graph.cypher_healer import heal_cypher
from src.graph.neo4j_client import Neo4jClient, setup_schema
from src.ingestion.ddl_parser import parse_ddl_file
from src.ingestion.pdf_loader import load_and_chunk_pdf
from src.ingestion.schema_enricher import enrich_all
from src.mapping.hitl import hitl_node, should_interrupt
from src.mapping.rag_mapper import propose_mapping, retrieve_top_entities, build_retrieval_query
from src.mapping.validator import build_reflection_prompt, critic_review, validate_schema
from src.models.schemas import Entity, MappingProposal, TableSchema
from src.models.state import BuilderState
from src.prompts.few_shot import load_cypher_examples
from src.resolution.entity_resolver import resolve_entities
from src.retrieval.embeddings import get_embeddings

logger: logging.Logger = get_logger(__name__)


# ─────────────────────────────────────────────────────────────────────────────
# Node Implementations
# ─────────────────────────────────────────────────────────────────────────────

def _node_extract_triplets(state: BuilderState) -> dict[str, Any]:
    settings = get_settings()
    llm = get_extraction_llm()
    chunks = state.get("chunks") or []
    triplets = extract_all_triplets(chunks, llm)
    return {"triplets": triplets}


def _node_entity_resolution(state: BuilderState) -> dict[str, Any]:
    settings = get_settings()
    embeddings = get_embeddings()
    llm = get_reasoning_llm()
    triplets = state.get("triplets") or []
    source_doc = state.get("source_doc", "unknown")
    entities = resolve_entities(triplets, embeddings, llm, source_doc)
    return {"entities": entities}


def _node_parse_ddl(state: BuilderState) -> dict[str, Any]:
    ddl_paths: list[str] = state.get("ddl_paths") or []
    tables: list[TableSchema] = []
    for path in ddl_paths:
        tables.extend(parse_ddl_file(path))
    return {"tables": tables}


def _node_enrich_schema(state: BuilderState) -> dict[str, Any]:
    llm = get_reasoning_llm()
    tables = state.get("tables") or []
    enriched = enrich_all(tables, llm)
    return {"enriched_tables": enriched}


def _node_rag_mapping(state: BuilderState) -> dict[str, Any]:
    settings = get_settings()
    llm = get_reasoning_llm()
    embeddings = get_embeddings()
    enriched_tables = state.get("enriched_tables") or []
    entities: list[Entity] = state.get("entities") or []
    reflection_prompt: str | None = state.get("reflection_prompt")

    # Process next table from remaining queue
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
        few_shot_examples="",  # loaded from disk; simplified here
        reflection_prompt=reflection_prompt,
    )

    return {
        "mapping_proposal": proposal,
        "current_table": current_table,
        "current_entities": top_entities,
        "pending_tables": remaining,
        "reflection_prompt": None,          # reset after use
        "reflection_attempts": state.get("reflection_attempts", 0),
    }


def _node_validate_mapping(state: BuilderState) -> dict[str, Any]:
    settings = get_settings()
    llm = get_reasoning_llm()
    proposal: MappingProposal | None = state.get("mapping_proposal")
    table: TableSchema | None = state.get("current_table")
    entities: list[Entity] = state.get("current_entities") or []
    attempts: int = state.get("reflection_attempts", 0)

    if proposal is None:
        return {"validation_error": "no proposal", "reflection_attempts": attempts + 1}

    # Layer 1: Pydantic
    validated, error = validate_schema(proposal.model_dump())
    if error:
        if attempts >= settings.max_reflection_attempts:
            return {"hitl_flag": True, "reflection_attempts": 0}
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
            return {"hitl_flag": True, "reflection_attempts": 0}
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
        "hitl_flag": validated.confidence < 0.9,
    }


def _node_generate_cypher(state: BuilderState) -> dict[str, Any]:
    settings = get_settings()
    llm = get_reasoning_llm()
    proposal: MappingProposal = state["mapping_proposal"]
    table: TableSchema = state["current_table"]
    entities: list[Entity] = state.get("current_entities") or []
    entity = entities[0] if entities else Entity(
        name=proposal.mapped_concept or "Unknown",
        definition="", synonyms=[], provenance_text="", source_doc="",
    )
    few_shot = load_cypher_examples(settings.few_shot_cypher_examples)
    cypher = generate_cypher(proposal, table, entity, few_shot, llm)
    return {"current_cypher": cypher, "healing_attempts": 0}


def _node_heal_cypher(state: BuilderState) -> dict[str, Any]:
    settings = get_settings()
    llm = get_reasoning_llm()
    cypher: str = state.get("current_cypher") or ""
    proposal: MappingProposal = state["mapping_proposal"]

    with Neo4jClient() as client:
        healed = heal_cypher(
            cypher, proposal, client._driver, llm,
            max_attempts=settings.max_cypher_healing_attempts,
        )

    if healed is None:
        logger.critical("Cypher permanently failed for table '%s'.", proposal.table_name)
        return {"cypher_failed": True, "current_cypher": None}

    return {"current_cypher": healed, "cypher_failed": False}


def _node_build_graph(state: BuilderState) -> dict[str, Any]:
    cypher: str | None = state.get("current_cypher")
    proposal: MappingProposal = state["mapping_proposal"]

    if not cypher:
        logger.warning("No valid Cypher to execute for '%s' — skipping.", proposal.table_name)
        return {}

    with Neo4jClient() as client:
        client.execute_cypher(cypher)
        logger.info("Graph updated for table '%s'.", proposal.table_name)

    completed = list(state.get("completed_tables") or [])
    completed.append(proposal.table_name)
    return {"completed_tables": completed}


# ─────────────────────────────────────────────────────────────────────────────
# Conditional Edge Predicates
# ─────────────────────────────────────────────────────────────────────────────

def _route_after_validate(state: BuilderState) -> str:
    if state.get("hitl_flag"):
        return "hitl"
    if state.get("reflection_prompt"):
        return "rag_mapping"  # retry with reflection
    return "generate_cypher"


def _route_after_heal(state: BuilderState) -> str:
    if state.get("cypher_failed"):
        # Try next table if any remain
        return "rag_mapping" if state.get("pending_tables") else END
    return "build_graph"


def _route_after_build(state: BuilderState) -> str:
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
        {"build_graph": "build_graph", "rag_mapping": "rag_mapping", END: END},
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
) -> BuilderState:
    """Convenience wrapper: compile graph and invoke with document paths.

    Args:
        raw_documents: List of file paths to PDF documents.
        ddl_paths:     List of file paths to DDL SQL files.
        production:    Compile with ``SqliteSaver`` if True.

    Returns:
        Final ``BuilderState`` after graph completion.
    """
    settings = get_settings()
    chunks = []
    for doc_path in raw_documents:
        chunks.extend(load_and_chunk_pdf(doc_path))

    graph = build_builder_graph(production=production)
    initial: BuilderState = {
        "chunks": chunks,
        "ddl_paths": ddl_paths,
        "source_doc": raw_documents[0] if raw_documents else "unknown",
        "triplets": [],
        "entities": [],
        "tables": [],
        "enriched_tables": [],
        "pending_tables": [],
        "completed_tables": [],
    }
    config = {"configurable": {"thread_id": "builder-run-1"}}
    final_state: BuilderState = graph.invoke(initial, config=config)
    return final_state
```

---

## 5. Tests

```python
"""Integration tests for src/graph/builder_graph.py — IT-01 (subset)"""

from __future__ import annotations

from unittest.mock import MagicMock, patch

import pytest

from src.graph.builder_graph import _route_after_build, _route_after_heal, _route_after_validate
from langgraph.graph import END


# ── Conditional edge routing ───────────────────────────────────────────────────

class TestRouteAfterValidate:
    def test_routes_to_hitl_when_flag(self) -> None:
        state = {"hitl_flag": True, "reflection_prompt": None}
        assert _route_after_validate(state) == "hitl"

    def test_routes_to_rag_mapping_for_reflection(self) -> None:
        state = {"hitl_flag": False, "reflection_prompt": "Please fix..."}
        assert _route_after_validate(state) == "rag_mapping"

    def test_routes_to_generate_cypher_on_success(self) -> None:
        state = {"hitl_flag": False, "reflection_prompt": None}
        assert _route_after_validate(state) == "generate_cypher"


class TestRouteAfterHeal:
    def test_routes_to_build_on_success(self) -> None:
        state = {"cypher_failed": False}
        assert _route_after_heal(state) == "build_graph"

    def test_routes_to_rag_mapping_if_pending_tables(self) -> None:
        state = {"cypher_failed": True, "pending_tables": [MagicMock()]}
        assert _route_after_heal(state) == "rag_mapping"

    def test_routes_to_end_if_no_pending_tables(self) -> None:
        state = {"cypher_failed": True, "pending_tables": []}
        assert _route_after_heal(state) == END


class TestRouteAfterBuild:
    def test_routes_to_rag_mapping_if_pending(self) -> None:
        state = {"pending_tables": [MagicMock()]}
        assert _route_after_build(state) == "rag_mapping"

    def test_routes_to_end_when_empty(self) -> None:
        state = {"pending_tables": []}
        assert _route_after_build(state) == END


# ── build_builder_graph ────────────────────────────────────────────────────────

class TestBuildBuilderGraph:
    def test_graph_compiles_without_error(self) -> None:
        with patch("src.graph.builder_graph.get_settings") as ms:
            ms.return_value = MagicMock(
                few_shot_cypher_examples=3,
                max_reflection_attempts=3,
                max_cypher_healing_attempts=3,
                retrieval_vector_top_k=10,
                sqlite_checkpoint_path=":memory:",
            ):
                from src.graph.builder_graph import build_builder_graph
                graph = build_builder_graph(production=False)
                assert graph is not None
```

---

## 6. Smoke Test

```bash
python -c "
from src.graph.builder_graph import _route_after_validate, _route_after_heal, _route_after_build
from langgraph.graph import END

# Test routing logic without a running Neo4j or LLM
assert _route_after_validate({'hitl_flag': True}) == 'hitl'
assert _route_after_validate({'hitl_flag': False, 'reflection_prompt': None}) == 'generate_cypher'
assert _route_after_heal({'cypher_failed': False}) == 'build_graph'
assert _route_after_build({'pending_tables': []}) == END
print('Builder graph routing smoke test passed.')
"
```
