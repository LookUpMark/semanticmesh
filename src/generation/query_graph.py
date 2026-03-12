"""Query LangGraph — EP-15 / US-15-01.

Wires hybrid retrieval → reranking → answer generation → hallucination grader
(with regeneration loop and web-search fallback) into a compiled StateGraph.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import END, StateGraph

from src.config.llm_factory import get_reasoning_llm
from src.config.logging import get_logger
from src.config.settings import get_settings
from src.generation.answer_generator import generate_answer, web_search_fallback
from src.generation.hallucination_grader import grade_answer
from src.graph.neo4j_client import Neo4jClient
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

if TYPE_CHECKING:
    import logging

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
        vec_results = vector_search(
            query, client, top_k=settings.retrieval_vector_top_k, model=model
        )
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

    # Loop guard — force web_search after max retries
    if iteration >= settings.max_hallucination_retries:
        logger.warning("Max hallucination retries reached — forcing web_search.")
        decision = GraderDecision(
            grounded=False,
            critique="Max retries exceeded.",
            action="web_search",
        )
    else:
        decision = grade_answer(query, answer, chunks, llm)

    update: dict[str, Any] = {"grader_decision": decision}
    if decision.action == "regenerate":
        update["last_critique"] = decision.critique
    return update


def _node_web_search(state: QueryState) -> dict[str, Any]:
    query: str = state["user_query"]
    result = web_search_fallback(query)
    return {"final_answer": result, "sources": ["web_search"]}


def _node_finalise(state: QueryState) -> dict[str, Any]:
    answer: str = state.get("current_answer") or ""
    sources: list[str] = [c.node_id for c in (state.get("reranked_chunks") or [])]
    return {"final_answer": answer, "sources": sources}


# ─────────────────────────────────────────────────────────────────────────────
# Conditional Edge
# ─────────────────────────────────────────────────────────────────────────────

def _route_after_grader(state: QueryState) -> str:
    """Route based on grader decision action."""
    decision: GraderDecision | None = state.get("grader_decision")
    if decision is None:
        return "finalise"
    if decision.action == "pass":
        return "finalise"
    if decision.action == "regenerate":
        return "answer_generation"
    if decision.action == "web_search":
        return "web_search"
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
    graph.add_node("web_search", _node_web_search)
    graph.add_node("finalise", _node_finalise)

    graph.set_entry_point("hybrid_retrieval")

    graph.add_edge("hybrid_retrieval", "reranking")
    graph.add_edge("reranking", "answer_generation")
    graph.add_edge("answer_generation", "hallucination_grader")
    graph.add_edge("web_search", END)
    graph.add_edge("finalise", END)

    graph.add_conditional_edges(
        "hallucination_grader",
        _route_after_grader,
        {
            "finalise": "finalise",
            "answer_generation": "answer_generation",
            "web_search": "web_search",
        },
    )

    return graph.compile(checkpointer=MemorySaver())


def run_query(user_query: str) -> dict[str, Any]:
    """Convenience entry point: builds and runs the query graph for a single query.

    Args:
        user_query: Natural-language question.

    Returns:
        ``{"final_answer": str, "sources": list[str]}``.
    """
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
