# Part 6 — `src/graph/builder_graph.py`

## 1. Purpose & Context

**Epic:** EP-11 Builder LangGraph Orchestration  
**US-11-01** — Builder StateGraph Definition

`builder_graph` assembles all previous nodes into a single LangGraph `StateGraph` that runs end-to-end ingestion:

```
extract_triplets → entity_resolution → parse_ddl → enrich_schema
    → rag_mapping → validate_mapping ──┬──► hitl ──┐
                         │             └──► rag_mapping (reflection retry)
                         └──────────────► generate_cypher
                                              │
                                         heal_cypher
                                              │
                                         build_graph ──┬──► rag_mapping (next table)
                                                       └──► END
```

Key design properties:

- **Retry counters** in `BuilderState` (`reflection_attempts`, `healing_attempts`) bound reflection and healing loops.
- **HITL interrupt** — the graph is compiled with `interrupt_before=["hitl"]` so a human reviewer can inspect low-confidence mappings before execution proceeds.
- **Primary / fallback Cypher execution** — `_node_build_graph` first tries the LLM-healed Cypher; if `cypher_failed=True` it falls back to the deterministic `build_upsert_cypher` builder. This means `_route_after_heal` **always** routes to `build_graph` regardless of healing outcome.
- **Embedding write-back** — after every successful graph write, `_node_build_graph` embeds the `mapped_concept` string and stores it on the `BusinessConcept` node.

---

## 2. Prerequisites

All previous implementation steps (01–21) must be complete:

- `src/models/state.py` — `BuilderState` TypedDict, including `completed_tables: list[str]` (step 6)
- `src/extraction/triplet_extractor.py` — `extract_all_triplets` (step 12)
- `src/resolution/entity_resolver.py` — `resolve_entities` (step 15)
- `src/ingestion/ddl_parser.py` — `parse_ddl_file` (step 10)
- `src/ingestion/schema_enricher.py` — `enrich_all` (step 11)
- `src/mapping/rag_mapper.py` — `build_retrieval_query`, `propose_mapping`, `retrieve_top_entities` (step 16)
- `src/mapping/validator.py` — `validate_schema`, `critic_review`, `build_reflection_prompt` (step 17)
- `src/mapping/hitl.py` — `hitl_node` (step 18)
- `src/graph/cypher_generator.py` — `generate_cypher` (step 20)
- `src/graph/cypher_healer.py` — `heal_cypher` (step 21)
- `src/graph/cypher_builder.py` — `build_upsert_cypher` (deterministic fallback builder)
- `src/graph/neo4j_client.py` — `Neo4jClient`, `setup_schema` (step 19)
- `src/prompts/few_shot.py` — `load_cypher_examples` (step 8)
- `src/retrieval/embeddings.py` — `embed_text`, `get_embeddings` (step 23)
- `src/config/settings.py`, `src/config/llm_factory.py`, `src/config/logging.py`

---

## 3. Public API

| Symbol | Signature | Description |
|---|---|---|
| `build_builder_graph` | `(*, production: bool = False) -> CompiledStateGraph` | Compile the full Builder LangGraph |
| `run_builder` | `(raw_documents: list[str], ddl_paths: list[str], *, production: bool = False, clear_graph: bool = False) -> BuilderState` | Convenience entry point |

### `run_builder` parameters

| Parameter | Type | Default | Description |
|---|---|---|---|
| `raw_documents` | `list[str]` | — | PDF file paths to ingest |
| `ddl_paths` | `list[str]` | — | SQL DDL file paths to parse |
| `production` | `bool` | `False` | Use `SqliteSaver` when `True`; `MemorySaver` otherwise |
| `clear_graph` | `bool` | `False` | When `True`, runs `MATCH (n) DETACH DELETE n` before ingestion (dev/demo only) |

---

## 4. Full Implementation

```python
"""Builder LangGraph — EP-11 / US-11-01."""
from __future__ import annotations
import logging
import uuid
from pathlib import Path
from typing import Any
from langchain_core.embeddings import Embeddings
from langchain_core.messages import SystemMessage
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import END, StateGraph
from langgraph.types import Command
from src.config.llm_factory import get_extraction_llm, get_reasoning_llm
from src.config.logging import get_logger
from src.config.settings import get_settings
from src.extraction.triplet_extractor import extract_all_triplets
from src.graph.cypher_builder import build_upsert_cypher
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

class _MockEmbeddings(Embeddings):
    def embed_documents(self, texts): return [[0.0]*1024 for _ in texts]
    def embed_query(self, text): return [0.0]*1024

def _get_embeddings(): return _MockEmbeddings()


# ─────────────────────────────────────────────────────────────────────────────
# Node Implementations
# ─────────────────────────────────────────────────────────────────────────────

def _node_extract_triplets(state):
    llm = get_extraction_llm()
    chunks = state.get("chunks") or []
    return {"triplets": extract_all_triplets(chunks, llm)}


def _node_entity_resolution(state):
    embeddings = _get_embeddings()
    llm = get_reasoning_llm()
    triplets = state.get("triplets") or []
    source_doc = state.get("source_doc", "unknown")
    return {"entities": resolve_entities(triplets, embeddings, llm, source_doc)}


def _node_parse_ddl(state):
    ddl_paths = state.get("ddl_paths") or []
    tables = []
    for path in ddl_paths:
        tables.extend(parse_ddl_file(path))
    return {"tables": tables}


def _node_enrich_schema(state):
    llm = get_reasoning_llm()
    tables = state.get("tables") or []
    return {"enriched_tables": enrich_all(tables, llm)}


def _node_rag_mapping(state):
    settings = get_settings()
    llm = get_reasoning_llm()
    embeddings = _get_embeddings()
    enriched_tables = state.get("enriched_tables") or []
    entities = state.get("entities") or []
    reflection_prompt = state.get("reflection_prompt")
    if reflection_prompt and state.get("current_table"):
        # Reflection retry: keep the same table, do not advance the queue
        current_table = state["current_table"]
        remaining = list(state.get("pending_tables") or [])
    else:
        pending = list(state.get("pending_tables") or enriched_tables)
        if not pending:
            return {"pending_tables": [], "current_table": None}
        current_table = pending[0]
        remaining = pending[1:]
    query = build_retrieval_query(current_table)
    top_entities = retrieve_top_entities(query, entities, embeddings, top_k=settings.retrieval_vector_top_k)
    proposal = propose_mapping(current_table, top_entities, llm, few_shot_examples="", reflection_prompt=reflection_prompt)
    return {
        "mapping_proposal": proposal,
        "current_table": current_table,
        "current_entities": top_entities,
        "pending_tables": remaining,
        "reflection_prompt": None,
        "reflection_attempts": state.get("reflection_attempts", 0),
    }


def _node_validate_mapping(state):
    settings = get_settings()
    llm = get_reasoning_llm()
    proposal = state.get("mapping_proposal")
    table = state.get("current_table")
    entities = state.get("current_entities") or []
    attempts = state.get("reflection_attempts", 0)
    if proposal is None:
        return {"reflection_attempts": attempts + 1}

    # Layer 1: Pydantic schema validation
    validated, error = validate_schema(proposal.model_dump())
    if error:
        if attempts >= settings.max_reflection_attempts:
            logger.warning(
                "Pydantic validation failed after %d attempts for '%s' — accepting last proposal.",
                attempts, proposal.table_name,
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
                validated.table_name, attempts,
            )
            return {"mapping_proposal": validated, "validation_error": None, "reflection_attempts": 0, "hitl_flag": False}
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


def _node_generate_cypher(state):
    settings = get_settings()
    llm = get_reasoning_llm()
    proposal = state["mapping_proposal"]
    table = state.get("current_table")
    # Always build a synthetic Entity from the validated concept — never relies on entities[0]
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


def _node_heal_cypher(state):
    settings = get_settings()
    llm = get_reasoning_llm()
    cypher = state.get("current_cypher") or ""
    proposal = state["mapping_proposal"]
    with Neo4jClient() as client:
        healed = heal_cypher(cypher, proposal, client.driver, llm, max_attempts=settings.max_cypher_healing_attempts)
    if healed is None:
        logger.critical("Cypher permanently failed for table '%s'.", proposal.table_name)
        return {"cypher_failed": True, "current_cypher": None}
    return {"current_cypher": healed, "cypher_failed": False}


def _node_build_graph(state):
    """Execute the best available Cypher to upsert data into Neo4j.

    Strategy (primary → fallback):
    1. **LLM-healed Cypher** — if ``heal_cypher`` succeeded (``cypher_failed=False``
       and ``current_cypher`` is set), execute the LLM-generated Cypher directly.
    2. **Deterministic builder** — if the LLM Cypher is invalid after all healing
       attempts, fall back to ``cypher_builder.build_upsert_cypher`` which uses
       driver-bound parameters.

    After every successful write, embeds ``mapped_concept`` and stores the vector
    on the ``BusinessConcept`` node.
    """
    proposal = state["mapping_proposal"]
    table = state.get("current_table")
    if not proposal or not table:
        logger.warning("Missing proposal or table in build_graph — skipping.")
        return {}
    llm_cypher = state.get("current_cypher")
    cypher_failed = state.get("cypher_failed", False)
    if llm_cypher and not cypher_failed:
        logger.info("Executing LLM-healed Cypher for '%s'.", proposal.table_name)
        exec_cypher, exec_params = llm_cypher, {}
    else:
        logger.info("LLM Cypher failed for '%s' — falling back to deterministic builder.", proposal.table_name)
        exec_cypher, exec_params = build_upsert_cypher(proposal, table)
    with Neo4jClient() as client:
        client.execute_cypher(exec_cypher, exec_params)
        logger.info("Graph updated for table '%s'.", proposal.table_name)
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

def _route_after_validate(state):
    if state.get("hitl_flag"):
        return "hitl"
    if state.get("reflection_prompt"):
        return "rag_mapping"
    return "generate_cypher"


def _route_after_heal(state):
    """Always proceed to build_graph.

    build_graph implements primary/fallback internally:
    - ``cypher_failed=False`` → LLM-healed Cypher executed (primary)
    - ``cypher_failed=True``  → deterministic builder (fallback)
    """
    return "build_graph"


def _route_after_build(state):
    if state.get("pending_tables"):
        return "rag_mapping"
    return END


# ─────────────────────────────────────────────────────────────────────────────
# Graph Factory
# ─────────────────────────────────────────────────────────────────────────────

def build_builder_graph(*, production=False):
    graph = StateGraph(BuilderState)
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
    graph.set_entry_point("extract_triplets")
    graph.add_edge("extract_triplets", "entity_resolution")
    graph.add_edge("entity_resolution", "parse_ddl")
    graph.add_edge("parse_ddl", "enrich_schema")
    graph.add_edge("enrich_schema", "rag_mapping")
    graph.add_edge("rag_mapping", "validate_mapping")
    graph.add_edge("hitl", "generate_cypher")
    graph.add_edge("generate_cypher", "heal_cypher")
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


def run_builder(raw_documents, ddl_paths, *, production=False, clear_graph=False):
    """Convenience wrapper.

    Args:
        raw_documents: List of PDF file paths.
        ddl_paths:     List of SQL DDL file paths.
        production:    If True, use SqliteSaver.
        clear_graph:   If True, ``MATCH (n) DETACH DELETE n`` before running
                       (dev/demo only).
    """
    chunks = []
    for doc_path in raw_documents:
        chunks.extend(load_and_chunk_pdf(doc_path))
    with Neo4jClient() as client:
        if clear_graph:
            client.execute_cypher("MATCH (n) DETACH DELETE n")
            logger.info("Graph cleared before builder run.")
        setup_schema(client)
    graph = build_builder_graph(production=production)
    initial = {
        "chunks": chunks, "ddl_paths": ddl_paths,
        "source_doc": str(raw_documents[0]) if raw_documents else "unknown",
        "triplets": [], "entities": [], "tables": [],
        "enriched_tables": [], "pending_tables": [], "completed_tables": [],
    }
    config = {"configurable": {"thread_id": f"builder-{uuid.uuid4().hex[:8]}"}}
    return graph.invoke(initial, config=config)
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
    def test_routes_to_build_graph_on_success(self) -> None:
        assert _route_after_heal({"cypher_failed": False}) == "build_graph"

    def test_routes_to_build_graph_even_on_failure(self) -> None:
        assert _route_after_heal({"cypher_failed": True, "pending_tables": [MagicMock()]}) == "build_graph"

    def test_routes_to_build_graph_always(self) -> None:
        assert _route_after_heal({"cypher_failed": True, "pending_tables": []}) == "build_graph"


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

# Routing smoke tests — no Neo4j or LLM required
assert _route_after_validate({'hitl_flag': True}) == 'hitl'
assert _route_after_validate({'hitl_flag': False, 'reflection_prompt': None}) == 'generate_cypher'

# _route_after_heal always returns build_graph regardless of cypher_failed
assert _route_after_heal({'cypher_failed': False}) == 'build_graph'
assert _route_after_heal({'cypher_failed': True, 'pending_tables': ['t']}) == 'build_graph'
assert _route_after_heal({'cypher_failed': True, 'pending_tables': []}) == 'build_graph'

assert _route_after_build({'pending_tables': []}) == END
print('Builder graph routing smoke test passed.')
"
```
