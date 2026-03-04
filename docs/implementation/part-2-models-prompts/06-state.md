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
| `documents` | `list[Document]` | Set by `pdf_loader_node`; read by `triplet_extractor_node` |
| `chunks` | `list[Chunk]` | Set by `pdf_loader_node` after splitting |
| `raw_tables` | `list[TableSchema]` | Set by `ddl_parser_node` |
| `enriched_tables` | `list[EnrichedTableSchema]` | Set by `schema_enricher_node` |
| `triplets` | `list[Triplet]` | Accumulated across all chunks |
| `entity_clusters` | `list[EntityCluster]` | Set by `blocking_node` |
| `canonical_entities` | `list[Entity]` | Set by `entity_resolver_node` after LLM judging |
| `mapping_proposals` | `list[MappingProposal]` | Set by `rag_mapper_node` |
| `critic_decisions` | `list[CriticDecision]` | Set by `validator_node`; used to re-run mapper or approve |
| `cypher_statements` | `list[CypherStatement]` | Set by `cypher_generator_node` |
| `ingestion_errors` | `list[str]` | Error messages from any node; graph ends on non-empty |
| `hitl_flag` | `bool` | Set by `validator_node`; triggers HITL pause when True |
| `current_step` | `str` | Human-readable log of the last completed node |

### `QueryState` fields

| Field | Type | Lifecycle |
|---|---|---|
| `question` | `str` | Set by the entry point; never mutated |
| `retrieved_chunks` | `list[RetrievedChunk]` | Set by `hybrid_retriever_node` |
| `reranked_chunks` | `list[RetrievedChunk]` | Set by `reranker_node` |
| `answer` | `str \| None` | Set by `answer_generator_node`; re-set after web_search fallback |
| `grader_decision` | `GraderDecision \| None` | Set by `hallucination_grader_node` |
| `web_search_result` | `str \| None` | Set by the web-search fallback node |
| `iteration` | `int` | Counts regeneration cycles; max 2 before fallback |
| `current_step` | `str` | Human-readable log of the last completed node |

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
    CanonicalEntityDecision,
    CriticDecision,
    CypherStatement,
    Document,
    Entity,
    EntityCluster,
    EnrichedTableSchema,
    GraderDecision,
    MappingProposal,
    RetrievedChunk,
    TableSchema,
    Triplet,
)


class BuilderState(TypedDict, total=False):
    """Mutable state flowing through the Knowledge Graph Builder graph."""

    # Ingestion
    documents: list[Document]
    chunks: list[Chunk]

    # Schema parsing
    raw_tables: list[TableSchema]
    enriched_tables: list[EnrichedTableSchema]

    # Triplet extraction
    triplets: list[Triplet]

    # Entity Resolution
    entity_clusters: list[EntityCluster]
    canonical_entities: list[Entity]

    # Mapping + validation
    mapping_proposals: list[MappingProposal]
    critic_decisions: list[CriticDecision]

    # Cypher
    cypher_statements: list[CypherStatement]

    # Control
    ingestion_errors: list[str]
    hitl_flag: bool
    current_step: str


class QueryState(TypedDict, total=False):
    """Mutable state flowing through the Query/Answer graph."""

    # Input (set once, never mutated)
    question: str

    # Retrieval
    retrieved_chunks: list[RetrievedChunk]
    reranked_chunks: list[RetrievedChunk]

    # Generation + grading
    answer: str | None
    grader_decision: GraderDecision | None

    # Fallback
    web_search_result: str | None

    # Control
    iteration: int
    current_step: str
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
        state: BuilderState = {"current_step": "start", "documents": []}
        assert state["current_step"] == "start"
        assert state["documents"] == []

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


class TestQueryState:
    def test_question_only(self) -> None:
        state: QueryState = {"question": "What is a Customer?"}
        assert state["question"] == "What is a Customer?"

    def test_defaults_to_empty(self) -> None:
        state: QueryState = {}
        # 'answer' key not present — access should raise KeyError
        assert "answer" not in state

    def test_iteration_counter(self) -> None:
        state: QueryState = {"question": "Q", "iteration": 0}
        state["iteration"] += 1
        assert state["iteration"] == 1

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
            "question": "Q",
            "retrieved_chunks": [rc],
            "reranked_chunks": [rc],
            "answer": "A Customer is an end user.",
            "grader_decision": gd,
            "iteration": 1,
            "current_step": "grader",
        }
        assert state["grader_decision"].grounded is True
```

---

## 6. Smoke Test

```bash
python -c "
from src.models.state import BuilderState, QueryState
s: BuilderState = {'current_step': 'init', 'documents': [], 'ingestion_errors': []}
print('BuilderState OK:', s)
q: QueryState = {'question': 'What is a Customer?', 'iteration': 0}
print('QueryState OK:', q)
"
```
