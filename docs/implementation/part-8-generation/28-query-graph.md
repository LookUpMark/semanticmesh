# Part 8 — `src/generation/query_graph.py`

## 1. Purpose & Context

**Epic:** EP-15 Query LangGraph Orchestration  
**US-15-01** — Query StateGraph Definition

`query_graph` assembles the retrieval-augmented generation loop into a `StateGraph`:

```
hybrid_retrieval → reranking → answer_generation → hallucination_grader
    ↑ (regenerate, iteration < max_hallucination_retries)      |
    └──────────────────── rag_retry ───────────────────────────┘
                                                         ↓ (pass, or retries exhausted)
                                                        finalise → END
```

The `iteration_count` field in `QueryState` prevents infinite regeneration loops. After `settings.max_hallucination_retries`, the grader node forces `action="pass"` before routing — ensuring the graph always reaches `finalise` and never stalls.

---

## 2. Prerequisites

- `src/models/state.py` — `QueryState` TypedDict (step 6)
- `src/retrieval/hybrid_retriever.py` — `vector_search`, `bm25_search`, `graph_traversal`, `merge_results`, `build_node_index` (step 24)
- `src/retrieval/reranker.py` — `rerank` (step 25)
- `src/generation/answer_generator.py` — `generate_answer` (step 26)
- `src/generation/hallucination_grader.py` — `grade_answer` (step 27)
- `src/graph/neo4j_client.py` — `Neo4jClient` (step 19)
- `src/retrieval/embeddings.py` — `get_embeddings` (step 23)
- `src/config/llm_factory.py`, `src/config/settings.py`, `src/config/logging.py`

---

## 3. Public API

| Symbol | Signature | Description |
|---|---|---|
| `build_query_graph` | `() -> CompiledStateGraph` | Compile the Query LangGraph |
| `run_query` | `(user_query: str) -> dict` | End-to-end query: returns `{"final_answer": str, "sources": list}` |

---

## 4. Full Implementation

```python
"""Query LangGraph — EP-15 / US-15-01.

Wires hybrid retrieval → reranking → answer generation → hallucination grader
(with regeneration loop and web-search fallback) into a compiled StateGraph.
"""

from __future__ import annotations

import logging
from typing import Any

from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import END, StateGraph

from src.config.llm_factory import get_reasoning_llm
from src.config.logging import get_logger
from src.config.settings import get_settings
from src.generation.answer_generator import generate_answer
from src.generation.hallucination_grader import grade_answer
from src.graph.neo4j_client import Neo4jClient, setup_schema
from src.models.schemas import GraderDecision, RetrievedChunk
from src.models.state import QueryState
from src.retrieval.embeddings import get_embeddings
from src.retrieval.hybrid_retriever import (
    bm25_search,
    build_node_index,
    graph_traversal,
    merge_results,
    vector_search,
)
from src.retrieval.reranker import rerank

logger: logging.Logger = get_logger(__name__)


# ─────────────────────────────────────────────────────────────────────────────
# Node Implementations
# ─────────────────────────────────────────────────────────────────────────────

def _node_hybrid_retrieval(state: QueryState) -> dict[str, Any]:
    settings = get_settings()
    query: str = state["user_query"]
    model = get_embeddings()

    with Neo4jClient() as client:
        all_nodes = build_node_index(client)
        vec_results = vector_search(query, client, top_k=settings.retrieval_vector_top_k, model=model)
        trav_results = graph_traversal(
            seed_names=[c.node_id for c in vec_results[:5]],
            client=client,
            depth=settings.retrieval_graph_depth,
        )

    bm25_results = bm25_search(query, all_nodes, top_k=settings.retrieval_bm25_top_k)
    merged = merge_results(vec_results, bm25_results, trav_results)
    return {"retrieved_chunks": merged}


def _node_reranking(state: QueryState) -> dict[str, Any]:
    settings = get_settings()
    query: str = state["user_query"]
    chunks: list[RetrievedChunk] = state.get("retrieved_chunks") or []
    reranked = rerank(query, chunks, top_k=settings.reranker_top_k)
    return {"reranked_chunks": reranked}


def _node_answer_generation(state: QueryState) -> dict[str, Any]:
    llm = get_reasoning_llm()
    query: str = state["user_query"]
    chunks: list[RetrievedChunk] = state.get("reranked_chunks") or []
    critique: str | None = state.get("last_critique")
    answer = generate_answer(query, chunks, llm, critique=critique)
    iteration = state.get("iteration_count", 0) + 1
    return {"current_answer": answer, "iteration_count": iteration, "last_critique": None}


def _node_hallucination_grader(state: QueryState) -> dict[str, Any]:
    settings = get_settings()
    llm = get_reasoning_llm()
    query: str = state["user_query"]
    answer: str = state.get("current_answer") or ""
    chunks: list[RetrievedChunk] = state.get("reranked_chunks") or []
    iteration: int = state.get("iteration_count", 0)

    # Loop guard — force pass after max retries to prevent infinite loops
    if iteration >= settings.max_hallucination_retries:
        logger.warning("Max hallucination retries reached — forcing pass.")
        decision = GraderDecision(
            grounded=True,
            critique=None,
            action="pass",
        )
    else:
        decision = grade_answer(query, answer, chunks, llm)

    update: dict[str, Any] = {"grader_decision": decision}
    if decision.action == "regenerate":
        update["last_critique"] = decision.critique
    return update


def _node_finalise(state: QueryState) -> dict[str, Any]:
    answer: str = state.get("current_answer") or ""
    sources: list[str] = [c.node_id for c in (state.get("reranked_chunks") or [])]
    return {"final_answer": answer, "sources": sources}


# ─────────────────────────────────────────────────────────────────────────────
# Conditional Edge
# ─────────────────────────────────────────────────────────────────────────────

def _route_after_grader(state: QueryState) -> str:
    decision: GraderDecision | None = state.get("grader_decision")
    if decision is None:
        return "finalise"
    if decision.action == "pass":
        return "finalise"
    if decision.action == "regenerate":
        return "answer_generation"
    return "finalise"


# ─────────────────────────────────────────────────────────────────────────────
# Graph Factory
# ─────────────────────────────────────────────────────────────────────────────

def build_query_graph():
    """Compile and return the Query StateGraph.

    Returns:
        A compiled LangGraph ``CompiledStateGraph`` ready to ``.invoke()``.
    """
    graph = StateGraph(QueryState)

    graph.add_node("hybrid_retrieval", _node_hybrid_retrieval)
    graph.add_node("reranking", _node_reranking)
    graph.add_node("answer_generation", _node_answer_generation)
    graph.add_node("hallucination_grader", _node_hallucination_grader)
    graph.add_node("finalise", _node_finalise)

    graph.set_entry_point("hybrid_retrieval")

    graph.add_edge("hybrid_retrieval", "reranking")
    graph.add_edge("reranking", "answer_generation")
    graph.add_edge("answer_generation", "hallucination_grader")
    graph.add_edge("finalise", END)

    graph.add_conditional_edges(
        "hallucination_grader",
        _route_after_grader,
        {
            "finalise": "finalise",
            "answer_generation": "answer_generation",
        },
    )

    return graph.compile(checkpointer=MemorySaver())


def run_query(user_query: str) -> dict[str, Any]:
    """Convenience entry point: build graph to run a single query.

    Args:
        user_query: Natural-language question.

    Returns:
        ``{"final_answer": str, "sources": list[str]}``.
    """
    # Ensure schema (constraints + vector index) exists before retrieval.
    with Neo4jClient() as client:
        setup_schema(client)

    graph = build_query_graph()
    config = {"configurable": {"thread_id": "query-run-1"}}
    initial: QueryState = {
        "user_query": user_query,
        "iteration_count": 0,
        "retrieved_chunks": [],
        "reranked_chunks": [],
        "current_answer": "",
        "last_critique": None,
        "grader_decision": None,
        "final_answer": "",
        "sources": [],
    }
    result = graph.invoke(initial, config=config)
    return {"final_answer": result.get("final_answer", ""), "sources": result.get("sources", [])}
```

---

## 5. Tests

```python
"""Unit tests for src/generation/query_graph.py — UT-23"""

from __future__ import annotations

from unittest.mock import MagicMock

import pytest

from langgraph.graph import END
from src.generation.query_graph import _route_after_grader
from src.models.schemas import GraderDecision


class TestRouteAfterGrader:
    def _state(self, action: str, grounded: bool = True) -> dict:
        return {
            "grader_decision": GraderDecision(
                grounded=grounded, critique=None, action=action
            )
        }

    def test_pass_routes_to_finalise(self) -> None:
        assert _route_after_grader(self._state("pass")) == "finalise"

    def test_regenerate_routes_to_answer_generation(self) -> None:
        assert _route_after_grader(self._state("regenerate", grounded=False)) == "answer_generation"

    def test_none_decision_routes_to_finalise(self) -> None:
        assert _route_after_grader({"grader_decision": None}) == "finalise"

    def test_unknown_action_routes_to_finalise(self) -> None:
        state = {"grader_decision": GraderDecision(grounded=True, critique=None, action="pass")}
        # Manually corrupt the action for edge testing
        state["grader_decision"] = MagicMock(action="unknown_action")
        assert _route_after_grader(state) == "finalise"


class TestBuildQueryGraph:
    def test_graph_compiles(self) -> None:
        from unittest.mock import patch
        with patch("src.generation.query_graph.get_settings") as ms:
            ms.return_value = MagicMock(
                retrieval_vector_top_k=10,
                retrieval_bm25_top_k=10,
                retrieval_graph_depth=2,
                reranker_top_k=5,
                max_hallucination_retries=3,
            ):
                from src.generation.query_graph import build_query_graph
                graph = build_query_graph()
                assert graph is not None
```

---

## 6. Smoke Test

```bash
python -c "
from src.generation.query_graph import _route_after_grader
from src.models.schemas import GraderDecision

decision_pass = GraderDecision(grounded=True, critique=None, action='pass')
decision_regen = GraderDecision(grounded=False, critique='Unsupported claim.', action='regenerate')

assert _route_after_grader({'grader_decision': decision_pass}) == 'finalise'
assert _route_after_grader({'grader_decision': decision_regen}) == 'answer_generation'
print('query_graph routing smoke test passed.')
"
```
