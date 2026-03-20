"""Query LangGraph — EP-15 / US-15-01.

Wires hybrid retrieval → reranking → answer generation → hallucination grader
(with regeneration loop) into a compiled StateGraph.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

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
    fetch_all_concepts,
    fetch_fk_relationships,
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

    retrieval_mode = (settings.retrieval_mode or "hybrid").lower()
    with Neo4jClient() as client:
        all_nodes = build_node_index(client)
        if retrieval_mode == "vector":
            vec_results = vector_search(
                query, client, top_k=settings.retrieval_vector_top_k, model=model
            )
            merged = vec_results
        elif retrieval_mode == "bm25":
            bm25_results = bm25_search(query, all_nodes, top_k=settings.retrieval_bm25_top_k)
            merged = bm25_results
        else:
            vec_results = vector_search(
                query, client, top_k=settings.retrieval_vector_top_k, model=model
            )
            trav_results = graph_traversal(
                seed_names=[c.node_id for c in vec_results[:5]],
                client=client,
                depth=settings.retrieval_graph_depth,
            )
            all_concepts = fetch_all_concepts(client)
            fk_chunks = fetch_fk_relationships(client)
            bm25_results = bm25_search(query, all_nodes, top_k=settings.retrieval_bm25_top_k)
            merged = merge_results(
                vec_results, bm25_results, trav_results + all_concepts + fk_chunks
            )
    return {"retrieved_chunks": merged}


def _node_reranking(state: QueryState) -> dict[str, Any]:
    settings = get_settings()
    query: str = state["user_query"]
    chunks: list[RetrievedChunk] = state.get("retrieved_chunks") or []
    min_score_raw = getattr(settings, "retrieval_min_score", 0.0)
    try:
        min_score = float(min_score_raw)
    except (TypeError, ValueError):
        min_score = 0.0
    min_ratio_raw = getattr(settings, "retrieval_min_score_ratio", 0.0)
    try:
        min_ratio = float(min_ratio_raw)
    except (TypeError, ValueError):
        min_ratio = 0.0
    min_ratio = max(0.0, min(1.0, min_ratio))

    if not settings.enable_reranker:
        candidates = chunks[: settings.reranker_top_k]
    else:
        candidates = rerank(query, chunks, top_k=settings.reranker_top_k)

    valid = [c for c in candidates if c.node_id.strip() and c.text.strip()]
    if not valid:
        return {
            "reranked_chunks": [],
            "retrieval_quality_score": 0.0,
            "retrieval_chunk_count": 0,
            "retrieval_filtered_by_threshold": False,
            "context_sufficiency": "insufficient",
        }

    top_score = float(valid[0].score)
    if top_score < min_score:
        logger.info(
            "reranking: top score %.4f below min_score %.4f; dropping all contexts.",
            top_score,
            min_score,
        )
        return {
            "reranked_chunks": [],
            "retrieval_quality_score": top_score,
            "retrieval_chunk_count": 0,
            "retrieval_filtered_by_threshold": True,
            "context_sufficiency": "insufficient",
        }

    threshold = max(min_score, top_score * min_ratio)
    filtered = [c for c in valid if float(c.score) >= threshold]
    if not filtered:
        sufficiency = "insufficient"
    elif len(filtered) == 1 and float(filtered[0].score) < 0.6:
        sufficiency = "sparse"
    else:
        sufficiency = "adequate"
    return {
        "reranked_chunks": filtered,
        "retrieval_quality_score": top_score,
        "retrieval_chunk_count": len(filtered),
        "retrieval_filtered_by_threshold": len(filtered) < len(valid),
        "context_sufficiency": sufficiency,
    }


def _node_answer_generation(state: QueryState) -> dict[str, Any]:
    llm = get_reasoning_llm()
    query: str = state["user_query"]
    chunks: list[RetrievedChunk] = state.get("reranked_chunks") or []
    critique: str | None = state.get("last_critique")
    sufficiency: str = state.get("context_sufficiency", "insufficient")
    if chunks and sufficiency != "adequate":
        logger.warning(
            "Generating answer with %s context (chunks=%d).",
            sufficiency,
            len(chunks),
        )
    answer = generate_answer(
        query,
        chunks,
        llm,
        critique=critique,
        context_sufficiency=sufficiency,
    )
    iteration = state.get("iteration_count", 0) + 1
    return {"current_answer": answer, "iteration_count": iteration, "last_critique": None}


def _node_retrieval_quality_gate(state: QueryState) -> dict[str, Any]:
    settings = get_settings()
    if not getattr(settings, "enable_retrieval_quality_gate", True):
        return {"retrieval_gate_decision": "proceed"}

    top_score = float(state.get("retrieval_quality_score", 0.0))
    chunk_count = int(state.get("retrieval_chunk_count", 0))
    sufficiency = state.get("context_sufficiency", "insufficient")
    filtered = bool(state.get("retrieval_filtered_by_threshold", False))

    if chunk_count == 0:
        return {"retrieval_gate_decision": "abstain_early"}

    if sufficiency == "adequate" and top_score >= 0.2:
        return {"retrieval_gate_decision": "proceed"}

    if filtered and top_score < 0.05:
        logger.info("Retrieval gate: low-score filtered context; abstaining early.")
        return {"retrieval_gate_decision": "abstain_early"}

    return {"retrieval_gate_decision": "proceed_with_warning"}


def _node_semantic_verification(state: QueryState) -> dict[str, Any]:
    settings = get_settings()
    if not getattr(settings, "enable_semantic_verifier", True):
        return {
            "semantic_verification_overlap": 1.0,
            "semantic_verification_passed": True,
            "semantic_verification_warning": None,
        }

    answer = (state.get("current_answer") or "").lower()
    chunks: list[RetrievedChunk] = state.get("reranked_chunks") or []
    if not chunks:
        return {
            "semantic_verification_overlap": 0.0,
            "semantic_verification_passed": True,
            "semantic_verification_warning": None,
        }

    entity_names: set[str] = set()
    for chunk in chunks:
        head = chunk.text.split(":", 1)[0].strip().lower()
        if head:
            entity_names.add(head)
        if chunk.node_id.strip():
            entity_names.add(chunk.node_id.strip().lower())

    if not entity_names:
        return {
            "semantic_verification_overlap": 1.0,
            "semantic_verification_passed": True,
            "semantic_verification_warning": None,
        }

    overlap_hits = sum(1 for name in entity_names if name in answer)
    overlap = overlap_hits / len(entity_names)
    passed = overlap >= 0.2
    warning = None
    if not passed:
        warning = "Low lexical overlap between answer and retrieved entities."
        logger.warning("Semantic verifier warning: overlap=%.3f (%d/%d).", overlap, overlap_hits, len(entity_names))

    return {
        "semantic_verification_overlap": overlap,
        "semantic_verification_passed": passed,
        "semantic_verification_warning": warning,
    }


def _node_hallucination_grader(state: QueryState) -> dict[str, Any]:
    settings = get_settings()
    if not settings.enable_hallucination_grader:
        return {"grader_decision": GraderDecision(grounded=True, critique=None, action="pass")}
    llm = get_reasoning_llm()
    query: str = state["user_query"]
    answer: str = state.get("current_answer") or ""
    chunks: list[RetrievedChunk] = state.get("reranked_chunks") or []
    iteration: int = state.get("iteration_count", 0)

    # Loop guard — accept answer after max retries to avoid infinite loop
    if iteration >= settings.max_hallucination_retries:
        logger.warning("Max hallucination retries reached — accepting current answer.")
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
        update["grader_rejection_count"] = int(state.get("grader_rejection_count", 0)) + 1
    return update


def _node_grader_consistency_validator(state: QueryState) -> dict[str, Any]:
    settings = get_settings()
    if not getattr(settings, "enable_grader_consistency_validator", True):
        return {"grader_consistency_valid": True}

    decision: GraderDecision | None = state.get("grader_decision")
    if decision is None:
        return {"grader_consistency_valid": True}

    valid = not (decision.grounded and decision.action != "pass")
    if not valid:
        logger.warning(
            "Grader consistency validator detected invalid decision: grounded=%s action=%s",
            decision.grounded,
            decision.action,
        )
    return {"grader_consistency_valid": valid}


def _node_finalise(state: QueryState) -> dict[str, Any]:
    answer: str = state.get("current_answer") or ""
    gate_decision = state.get("retrieval_gate_decision", "proceed")
    if gate_decision == "abstain_early":
        answer = "I cannot find this information in the knowledge graph."
    reranked: list[RetrievedChunk] = state.get("reranked_chunks") or []
    sources: list[str] = [c.node_id for c in reranked]
    # retrieved_contexts: full texts used by RAGAS evaluation
    retrieved_contexts: list[str] = [c.text for c in reranked if c.text]
    return {
        "final_answer": answer,
        "sources": sources,
        "retrieved_contexts": retrieved_contexts,
        "retrieval_quality_score": float(state.get("retrieval_quality_score", 0.0)),
        "retrieval_chunk_count": int(state.get("retrieval_chunk_count", len(reranked))),
        "retrieval_filtered_by_threshold": bool(state.get("retrieval_filtered_by_threshold", False)),
        "context_sufficiency": state.get("context_sufficiency", "insufficient"),
        "retrieval_gate_decision": gate_decision,
        "semantic_verification_overlap": float(state.get("semantic_verification_overlap", 1.0)),
        "semantic_verification_passed": bool(state.get("semantic_verification_passed", True)),
        "semantic_verification_warning": state.get("semantic_verification_warning"),
        "grader_consistency_valid": bool(state.get("grader_consistency_valid", True)),
        "grader_rejection_count": int(state.get("grader_rejection_count", 0)),
    }


# ─────────────────────────────────────────────────────────────────────────────
# Conditional Edge
# ─────────────────────────────────────────────────────────────────────────────


def _route_after_grader(state: QueryState) -> str:
    """Route based on grader decision action."""
    decision: GraderDecision | None = state.get("grader_decision")
    if decision is None or decision.action == "pass":
        return "finalise"
    if decision.action == "regenerate":
        return "answer_generation"
    return "finalise"


def _route_after_retrieval_gate(state: QueryState) -> str:
    decision = state.get("retrieval_gate_decision", "proceed")
    if decision == "abstain_early":
        return "finalise"
    return "answer_generation"


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
    graph.add_node("retrieval_quality_gate", _node_retrieval_quality_gate)
    graph.add_node("answer_generation", _node_answer_generation)
    graph.add_node("semantic_verification", _node_semantic_verification)
    graph.add_node("hallucination_grader", _node_hallucination_grader)
    graph.add_node("grader_consistency_validator", _node_grader_consistency_validator)
    graph.add_node("finalise", _node_finalise)

    graph.set_entry_point("hybrid_retrieval")

    graph.add_edge("hybrid_retrieval", "reranking")
    graph.add_edge("reranking", "retrieval_quality_gate")
    graph.add_edge("answer_generation", "semantic_verification")
    graph.add_edge("semantic_verification", "hallucination_grader")
    graph.add_edge("hallucination_grader", "grader_consistency_validator")
    graph.add_edge("finalise", END)

    graph.add_conditional_edges(
        "retrieval_quality_gate",
        _route_after_retrieval_gate,
        {
            "finalise": "finalise",
            "answer_generation": "answer_generation",
        },
    )

    graph.add_conditional_edges(
        "grader_consistency_validator",
        _route_after_grader,
        {
            "finalise": "finalise",
            "answer_generation": "answer_generation",
        },
    )

    return graph.compile(checkpointer=MemorySaver())


def run_query(user_query: str) -> dict[str, Any]:
    """Convenience entry point: builds and runs the query graph for a single query.

    Args:
        user_query: Natural-language question.

    Returns:
        ``{"final_answer": str, "sources": list[str], "retrieved_contexts": list[str], "retrieval_quality_score": float, "retrieval_chunk_count": int, "retrieval_filtered_by_threshold": bool, "context_sufficiency": str}``.
    """
    graph = build_query_graph()
    config = {"configurable": {"thread_id": "query-run-1"}}
    # Ensure schema (vector index) exists before querying.
    with Neo4jClient() as client:
        setup_schema(client)
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
        "retrieved_contexts": [],
        "retrieval_quality_score": 0.0,
        "retrieval_chunk_count": 0,
        "retrieval_filtered_by_threshold": False,
        "context_sufficiency": "insufficient",
        "retrieval_gate_decision": "proceed",
        "semantic_verification_overlap": 1.0,
        "semantic_verification_passed": True,
        "semantic_verification_warning": None,
        "grader_consistency_valid": True,
        "grader_rejection_count": 0,
    }
    result = graph.invoke(initial, config=config)
    return {
        "final_answer": result.get("final_answer", ""),
        "sources": result.get("sources", []),
        "retrieved_contexts": result.get("retrieved_contexts", []),
        "retrieval_quality_score": result.get("retrieval_quality_score", 0.0),
        "retrieval_chunk_count": result.get("retrieval_chunk_count", 0),
        "retrieval_filtered_by_threshold": result.get("retrieval_filtered_by_threshold", False),
        "context_sufficiency": result.get("context_sufficiency", "insufficient"),
        "retrieval_gate_decision": result.get("retrieval_gate_decision", "proceed"),
        "semantic_verification_overlap": result.get("semantic_verification_overlap", 1.0),
        "semantic_verification_passed": result.get("semantic_verification_passed", True),
        "semantic_verification_warning": result.get("semantic_verification_warning"),
        "grader_consistency_valid": result.get("grader_consistency_valid", True),
        "grader_rejection_count": result.get("grader_rejection_count", 0),
    }
