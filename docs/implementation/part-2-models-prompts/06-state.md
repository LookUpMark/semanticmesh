# Part 2 — `src/models/state.py`

## 1. Purpose & Context

**Epic:** EP-06 data models  
**US:** REQUIREMENTS.md §6 — Graph State Schemas

Defines `BuilderState` and `QueryState` — the typed dictionaries that flow through every LangGraph node in the two graphs (`builder_graph.py` and `query_graph.py`). Having these in a dedicated module prevents circular imports and makes graph topology self-documenting.

Both types extend `TypedDict` (compatible with LangGraph's `StateGraph`) rather than Pydantic, because LangGraph manages its own message serialisation.

---

## 2. Prerequisites

- `05-schemas.md` implemented → `src/models/schemas.py` exists
- `pyproject.toml` with `langgraph>=0.2`, `langchain-core>=0.3`

---

## 3. Public API

| Symbol | Type | Description |
|---|---|---|
| `BuilderState` | `TypedDict` | Mutable state for the **Knowledge Graph Builder** workflow |
| `QueryState` | `TypedDict` | Mutable state for the **Query/Answer** workflow |

### `BuilderState` fields

| Field | Type | Lifecycle |
|---|---|---|
| `ddl_paths` | `list[str]` | Entry-point input: paths to DDL files |
| `source_doc` | `str` | Entry-point input: path to the PDF document |
| `documents` | `list[Document]` | Set by `pdf_loader_node`; read by `triplet_extractor_node` |
| `chunks` | `list[Chunk]` | Set by `pdf_loader_node` after splitting |
| `triplets` | `list[Triplet]` | Accumulated across all chunks |
| `entities` | `list[Entity]` | Canonical entities post-Entity Resolution |
| `tables` | `list[TableSchema]` | Set by `ddl_parser_node` (raw DDL output) |
| `enriched_tables` | `list[EnrichedTableSchema]` | Set by `schema_enricher_node` |
| `pending_tables` | `list[EnrichedTableSchema]` | Queue of tables awaiting mapping |
| `current_table` | `EnrichedTableSchema \| None` | Table currently being mapped |
| `current_entities` | `list[Entity]` | Entities relevant to `current_table` |
| `mapping_proposal` | `MappingProposal \| None` | Proposal for `current_table`; singular |
| `reflection_prompt` | `str \| None` | Critique feedback fed to the re-map attempt |
| `reflection_attempts` | `int` | Counts re-map retries per table |
| `current_cypher` | `str \| None` | Cypher being healed |
| `healing_attempts` | `int` | Counts healing retries per Cypher statement |
| `cypher_failed` | `bool` | Set if healing exhausts retries |
| `hitl_flag` | `bool` | Set by `validator_node`; triggers HITL pause when True |
| `failed_mappings` | `list[str]` | Table names whose mapping failed permanently |
| `ingestion_errors` | `list[str]` | Error messages from any node; graph ends on non-empty |

### `QueryState` fields

| Field | Type | Lifecycle |
|---|---|---|
| `user_query` | `str` | Set by the entry point; never mutated |
| `retrieved_chunks` | `list[RetrievedChunk]` | Set by `hybrid_retriever_node` |
| `reranked_chunks` | `list[RetrievedChunk]` | Set by `reranker_node` |
| `current_answer` | `str` | Draft answer produced by `answer_generator_node` |
| `last_critique` | `str \| None` | Critique text from the hallucination grader |
| `grader_decision` | `GraderDecision \| None` | Structured decision from `hallucination_grader_node` |
| `final_answer` | `str` | Committed answer returned to the caller |
| `sources` | `list[str]` | Source node IDs backing the final answer |
| `iteration_count` | `int` | Counts regeneration cycles; max 2 before fallback |

---

## 4. Full Implementation

```python
"""LangGraph state schemas for builder_graph and query_graph.

Both use TypedDict (not Pydantic) so LangGraph can serialise them
with its built-in reducers. Use Optional / `| None` instead of
Field(default=...) here.
"""

from __future__ import annotations

from typing import TypedDict

from src.models.schemas import (
    Chunk,
    Document,
    Entity,
    EnrichedTableSchema,
    GraderDecision,
    MappingProposal,
    RetrievedChunk,
    TableSchema,
    Triplet,
)


class BuilderState(TypedDict, total=False):
    """Mutable state flowing through the Knowledge Graph Builder graph."""

    # Entry-point inputs
    ddl_paths: list[str]
    source_doc: str

    # Ingestion
    documents: list[Document]
    chunks: list[Chunk]

    # Extraction + Entity Resolution
    triplets: list[Triplet]
    entities: list[Entity]            # canonical, post-ER

    # Schema parsing
    tables: list[TableSchema]         # raw DDL output
    enriched_tables: list[EnrichedTableSchema]

    # Mapping (queue-based, one table at a time)
    pending_tables: list[EnrichedTableSchema]
    current_table: EnrichedTableSchema | None
    current_entities: list[Entity]
    mapping_proposal: MappingProposal | None
    reflection_prompt: str | None
    reflection_attempts: int

    # Cypher
    current_cypher: str | None
    healing_attempts: int
    cypher_failed: bool

    # Control
    hitl_flag: bool
    failed_mappings: list[str]
    ingestion_errors: list[str]


class QueryState(TypedDict, total=False):
    """Mutable state flowing through the Query/Answer graph."""

    # Input (set once, never mutated)
    user_query: str

    # Retrieval
    retrieved_chunks: list[RetrievedChunk]
    reranked_chunks: list[RetrievedChunk]

    # Generation + grading
    current_answer: str
    last_critique: str | None
    grader_decision: GraderDecision | None

    # Output
    final_answer: str
    sources: list[str]

    # Control
    iteration_count: int
```

---

## 5. Tests

```python
"""Unit tests for src/models/state.py"""

from __future__ import annotations

from src.models.state import BuilderState, QueryState


class TestBuilderState:
    def test_partial_init(self) -> None:
        # TypedDict with total=False allows any subset of keys
        state: BuilderState = {"documents": [], "ingestion_errors": []}
        assert state["documents"] == []
        assert state["ingestion_errors"] == []

    def test_empty_init(self) -> None:
        state: BuilderState = {}
        assert len(state) == 0

    def test_can_set_hitl_flag(self) -> None:
        state: BuilderState = {"hitl_flag": True}
        assert state["hitl_flag"] is True

    def test_can_accumulate_errors(self) -> None:
        state: BuilderState = {"ingestion_errors": []}
        state["ingestion_errors"].append("PDF load failed: file not found")
        assert len(state["ingestion_errors"]) == 1

    def test_mapping_queue_fields(self) -> None:
        state: BuilderState = {
            "pending_tables": [],
            "current_table": None,
            "mapping_proposal": None,
            "reflection_attempts": 0,
        }
        assert state["current_table"] is None
        assert state["reflection_attempts"] == 0


class TestQueryState:
    def test_user_query_only(self) -> None:
        state: QueryState = {"user_query": "What is a Customer?"}
        assert state["user_query"] == "What is a Customer?"

    def test_defaults_to_empty(self) -> None:
        state: QueryState = {}
        # 'final_answer' key not present — access should raise KeyError
        assert "final_answer" not in state

    def test_iteration_counter(self) -> None:
        state: QueryState = {"user_query": "Q", "iteration_count": 0}
        state["iteration_count"] += 1
        assert state["iteration_count"] == 1

    def test_full_workflow_fields(self) -> None:
        from src.models.schemas import GraderDecision, RetrievedChunk

        rc = RetrievedChunk(
            node_id="bc-1",
            node_type="BusinessConcept",
            text="Customer: end user",
            score=0.95,
            source_type="vector",
        )
        gd = GraderDecision(grounded=True, action="pass")
        state: QueryState = {
            "user_query": "Q",
            "retrieved_chunks": [rc],
            "reranked_chunks": [rc],
            "current_answer": "A Customer is an end user.",
            "last_critique": None,
            "grader_decision": gd,
            "final_answer": "A Customer is an end user.",
            "sources": ["bc-1"],
            "iteration_count": 1,
        }
        assert state["grader_decision"].grounded is True
        assert state["sources"] == ["bc-1"]
```

---

## 6. Smoke Test

```bash
python -c "
from src.models.state import BuilderState, QueryState
s: BuilderState = {'ddl_paths': [], 'documents': [], 'ingestion_errors': []}
print('BuilderState OK:', s)
q: QueryState = {'user_query': 'What is a Customer?', 'iteration_count': 0}
print('QueryState OK:', q)
"
```
