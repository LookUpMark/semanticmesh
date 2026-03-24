"""Query LangGraph — EP-15 / US-15-01.

Wires hybrid retrieval → reranking → answer generation → hallucination grader
(with regeneration loop) into a compiled StateGraph.

This module serves as the orchestration layer for the query pipeline,
integrating nodes from:
- retrieval_nodes: Hybrid retrieval and reranking
- generation_nodes: Answer generation and hallucination grading
- expansion_nodes: Context distillation and lazy expansion
- routing: Conditional edge routing logic
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import END, StateGraph

# Re-export for backward compatibility with tests
from src.config.logging import get_logger
from src.config.settings import get_settings
from src.generation.nodes import (
    _node_answer_generation,
    _node_context_distillation,
    _node_grade_hallucination,
    _node_rerank,
    _node_retrieve,
)
from src.generation.routing import (
    _route_after_consistency_validator,
    _route_after_retrieval_gate,
)
from src.graph.neo4j_client import Neo4jClient

# Backward compatibility: expose node functions with original names
_node_hybrid_retrieval = _node_retrieve
_node_reranking = _node_rerank
_node_hallucination_grader = _node_grade_hallucination
from src.graph.neo4j_client import setup_schema
from src.models.schemas import RetrievedChunk
from src.models.state import QueryState

if TYPE_CHECKING:
    import logging

logger: logging.Logger = get_logger(__name__)


# ─────────────────────────────────────────────────────────────────────────────
# Helper Functions (moved from nodes, used by quality gate/verifier)
# ─────────────────────────────────────────────────────────────────────────────


def _has_structural_relationship_evidence(chunks: list[RetrievedChunk]) -> bool:
    """Return True when chunks carry explicit relational/schema evidence."""
    for chunk in chunks:
        node_id = chunk.node_id.strip().lower()
        text = chunk.text.strip().lower()
        if "→" in node_id:
            return True
        # Relation tokens from retrieval_nodes
        relation_tokens = ("references", "foreign key", "fk ", " fk", "joins", "join ")
        if any(token in text for token in relation_tokens):
            return True
    return False


def _active_chunks(state: QueryState) -> list[RetrievedChunk]:
    """Get active chunks for generation (generation_chunks or reranked_chunks)."""
    return state.get("generation_chunks") or state.get("reranked_chunks") or []


# ─────────────────────────────────────────────────────────────────────────────
# Quality Gate and Verification Nodes
# ─────────────────────────────────────────────────────────────────────────────


def _node_retrieval_quality_gate(state: QueryState) -> dict[str, Any]:
    """Gate retrieval quality to avoid generating answers from insufficient context.

    Returns:
        "proceed": Adequate retrieval quality
        "proceed_with_warning": Low quality but usable
        "abstain_early": Insufficient context, abort early
    """

    settings = get_settings()
    if not getattr(settings, "enable_retrieval_quality_gate", True):
        return {"retrieval_gate_decision": "proceed"}

    top_score = float(state.get("retrieval_quality_score", 0.0))
    chunk_count = int(state.get("retrieval_chunk_count", 0))
    sufficiency = state.get("context_sufficiency", "insufficient")
    query = str(state.get("user_query", ""))
    reranked: list[RetrievedChunk] = state.get("reranked_chunks") or []
    has_structural_evidence = _has_structural_relationship_evidence(reranked)
    relation_query = any(k in query.lower() for k in ("related", "relationship", "linked", "link"))

    if chunk_count == 0:
        return {"retrieval_gate_decision": "abstain_early"}

    if chunk_count == 1 and (has_structural_evidence or relation_query):
        logger.info(
            "Retrieval gate: preserving sparse but structured evidence (score %.4f).",
            top_score,
        )
        return {"retrieval_gate_decision": "proceed_with_warning"}

    if sufficiency == "adequate" and top_score >= 0.2:
        return {"retrieval_gate_decision": "proceed"}

    if top_score < 0.015 and chunk_count <= 1 and not has_structural_evidence:
        logger.info(
            "Retrieval gate: very low-score context without structural evidence and sparse evidence; abstaining early."
        )
        return {"retrieval_gate_decision": "abstain_early"}

    if top_score < 0.015 and chunk_count >= 2:
        logger.info(
            "Retrieval gate: very low-score but multi-chunk evidence available (chunks=%d); proceeding with warning.",
            chunk_count,
        )
        return {"retrieval_gate_decision": "proceed_with_warning"}

    return {"retrieval_gate_decision": "proceed_with_warning"}


def _node_semantic_verification(state: QueryState) -> dict[str, Any]:
    """Verify semantic overlap between answer and retrieved entities.

    Checks if the answer mentions the entities/concepts found in retrieved chunks.
    Low overlap may indicate hallucination or irrelevant answer.
    """

    settings = get_settings()
    if not getattr(settings, "enable_semantic_verifier", True):
        return {
            "semantic_verification_overlap": 1.0,
            "semantic_verification_passed": True,
            "semantic_verification_warning": None,
        }

    answer = (state.get("current_answer") or "").lower()
    chunks: list[RetrievedChunk] = _active_chunks(state)
    query = str(state.get("user_query", ""))
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
    has_structural_evidence = _has_structural_relationship_evidence(chunks)
    relation_query = any(k in query.lower() for k in ("related", "relationship", "linked", "link"))
    min_overlap = 0.2
    if relation_query or has_structural_evidence:
        # Relationship-focused answers often paraphrase entity labels.
        min_overlap = 0.1

    passed = overlap >= min_overlap
    warning = None
    if not passed:
        warning = "Low lexical overlap between answer and retrieved entities."
        logger.warning(
            "Semantic verifier warning: overlap=%.3f (%d/%d, min=%.2f).",
            overlap,
            overlap_hits,
            len(entity_names),
            min_overlap,
        )

    return {
        "semantic_verification_overlap": overlap,
        "semantic_verification_passed": passed,
        "semantic_verification_warning": warning,
    }


def _node_grader_consistency_validator(state: QueryState) -> dict[str, Any]:
    """Validate grader decision consistency.

    Ensures that if a decision is marked as grounded, its action is "pass".
    Inconsistent decisions are logged as warnings.
    """

    settings = get_settings()
    if not getattr(settings, "enable_grader_consistency_validator", True):
        return {"grader_consistency_valid": True}

    from src.models.schemas import GraderDecision

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
    """Finalize query response and collect metadata for evaluation.

    Compiles the final answer with sources and retrieval metrics for RAGAS evaluation.
    """
    answer: str = state.get("current_answer") or ""
    gate_decision = state.get("retrieval_gate_decision", "proceed")
    if gate_decision == "abstain_early":
        answer = "I cannot find this information in the knowledge graph."
    reranked: list[RetrievedChunk] = state.get("reranked_chunks") or []
    generated_with: list[RetrievedChunk] = state.get("generation_chunks") or reranked
    sources: list[str] = [c.node_id for c in generated_with]
    # retrieved_contexts: full texts used by RAGAS evaluation
    retrieved_contexts: list[str] = [c.text for c in generated_with if c.text]
    return {
        "final_answer": answer,
        "sources": sources,
        "retrieved_contexts": retrieved_contexts,
        "retrieval_quality_score": float(state.get("retrieval_quality_score", 0.0)),
        "retrieval_chunk_count": int(state.get("retrieval_chunk_count", len(reranked))),
        "retrieved_filtered_by_threshold": bool(
            state.get("retrieval_filtered_by_threshold", False)
        ),
        "context_sufficiency": state.get("context_sufficiency", "insufficient"),
        "retrieval_gate_decision": gate_decision,
        "semantic_verification_overlap": float(state.get("semantic_verification_overlap", 1.0)),
        "semantic_verification_passed": bool(state.get("semantic_verification_passed", True)),
        "semantic_verification_warning": state.get("semantic_verification_warning"),
        "grader_consistency_valid": bool(state.get("grader_consistency_valid", True)),
        "grader_rejection_count": int(state.get("grader_rejection_count", 0)),
    }


# ─────────────────────────────────────────────────────────────────────────────
# Graph Factory
# ─────────────────────────────────────────────────────────────────────────────


def build_query_graph():
    """Compile and return the Query StateGraph.

    The query graph implements an Agentic RAG pipeline with:
    - Hybrid retrieval (vector + BM25 + graph traversal)
    - Cross-encoder reranking
    - Retrieval quality gate
    - Context distillation
    - Answer generation with critique loop
    - Semantic verification
    - Hallucination grading (Self-RAG)
    - Consistency validation

    Returns:
        A compiled LangGraph ``CompiledStateGraph`` ready to ``.invoke()``.
    """
    graph = StateGraph(QueryState)

    # Add nodes
    graph.add_node("hybrid_retrieval", _node_retrieve)
    graph.add_node("reranking", _node_rerank)
    graph.add_node("retrieval_quality_gate", _node_retrieval_quality_gate)
    graph.add_node("context_distillation", _node_context_distillation)
    graph.add_node("answer_generation", _node_answer_generation)
    graph.add_node("semantic_verification", _node_semantic_verification)
    graph.add_node("hallucination_grader", _node_grade_hallucination)
    graph.add_node("grader_consistency_validator", _node_grader_consistency_validator)
    graph.add_node("finalise", _node_finalise)
    graph.add_node("save_query_trace", _node_save_query_trace)

    # Set entry point
    graph.set_entry_point("hybrid_retrieval")

    # Add edges
    graph.add_edge("hybrid_retrieval", "reranking")
    graph.add_edge("reranking", "retrieval_quality_gate")
    graph.add_edge("context_distillation", "answer_generation")
    graph.add_edge("answer_generation", "semantic_verification")
    graph.add_edge("semantic_verification", "hallucination_grader")
    graph.add_edge("hallucination_grader", "grader_consistency_validator")
    graph.add_edge("finalise", "save_query_trace")
    graph.add_edge("save_query_trace", END)

    # Add conditional edges
    graph.add_conditional_edges(
        "retrieval_quality_gate",
        _route_after_retrieval_gate,
        {
            "finalise": "finalise",
            "context_distillation": "context_distillation",
        },
    )

    graph.add_conditional_edges(
        "grader_consistency_validator",
        _route_after_consistency_validator,
        {
            "finalise": "finalise",
            "answer_generation": "answer_generation",
        },
    )

    return graph.compile(checkpointer=MemorySaver())


# ─────────────────────────────────────────────────────────────────────────────
# Debug Tracing
# ─────────────────────────────────────────────────────────────────────────────


def _node_save_query_trace(state: QueryState) -> dict[str, Any]:
    """Save debug query trace if enabled."""
    if not state.get("query_trace_enabled"):
        return {}

    from pathlib import Path

    trace = state.get("query_trace")
    if not trace:
        logger.warning("Query trace enabled but no trace object found in state.")
        return {}

    output_dir = Path(state.get("trace_output_dir", "notebooks/ablation/ablation_results/traces/debug"))
    trace_file = output_dir / f"query_traces_{trace.study_id}.jsonl"
    trace.save(trace_file)
    logger.info(f"Query trace saved to {trace_file}")

    return {}


def run_query(
    user_query: str,
    *,
    trace_enabled: bool = False,
    query_index: int = 0,
    builder_trace_id: str = "",
    study_id: str = "manual",
) -> dict[str, Any]:
    """Convenience entry point: builds and runs the query graph for a single query.

    Args:
        user_query: Natural-language question.
        trace_enabled: If True, enable detailed debug tracing of the query pipeline.
        query_index: Index of this query in the batch (for trace naming).
        builder_trace_id: ID of the builder trace to link with.
        study_id: Study ID for trace naming (e.g., "AB-00").

    Returns:
        ``{
            "final_answer": str,
            "sources": list[str],
            "retrieved_contexts": list[str],
            "retrieval_quality_score": float,
            "retrieval_chunk_count": int,
            "retrieved_filtered_by_threshold": bool,
            "context_sufficiency": str,
            "retrieval_gate_decision": str,
            "semantic_verification_overlap": float,
            "semantic_verification_passed": bool,
            "semantic_verification_warning": str | None,
            "grader_consistency_valid": bool,
            "grader_rejection_count": int,
        }``
    """
    from src.config.tracing import QueryTrace
    from src.config.settings import get_settings

    settings = get_settings()

    # Initialize query trace if enabled
    query_trace: QueryTrace | None = None
    if trace_enabled:
        query_trace = QueryTrace.create(
            study_id=study_id,
            question=user_query,
            query_index=query_index,
            builder_trace_id=builder_trace_id,
        )
        logger.info(f"Query tracing enabled for query {query_index}")

    graph = build_query_graph()
    config = {"configurable": {"thread_id": f"query-run-{query_index}"}}
    # Ensure schema (vector index) exists before querying.
    with Neo4jClient() as client:
        setup_schema(client)
    initial: QueryState = {
        "user_query": user_query,
        "iteration_count": 0,
        "retrieved_chunks": [],
        "reranked_chunks": [],
        "generation_chunks": [],
        "current_answer": "",
        "last_critique": None,
        "grader_decision": None,
        "final_answer": "",
        "sources": [],
        "retrieved_contexts": [],
        "retrieval_quality_score": 0.0,
        "retrieval_chunk_count": 0,
        "retrieved_filtered_by_threshold": False,
        "context_sufficiency": "insufficient",
        "retrieval_gate_decision": "proceed",
        "semantic_verification_overlap": 1.0,
        "semantic_verification_passed": True,
        "semantic_verification_warning": None,
        "grader_consistency_valid": True,
        "grader_rejection_count": 0,
        "query_trace_enabled": trace_enabled,
        "query_trace": query_trace,
        "query_index": query_index,
        "builder_trace_id": builder_trace_id,
        "trace_output_dir": settings.trace_output_dir if trace_enabled else "",
    }
    result = graph.invoke(initial, config=config)

    # Populate trace with final state data
    if trace_enabled and query_trace:
        # Record retrieval details
        retrieved = result.get("retrieved_chunks", [])
        query_trace.record_retrieval(
            vector_results=None,  # Would need to be tracked in retrieval node
            bm25_results=None,
            graph_results=None,
            rrf_fused=[{"node": r.node_id, "rrf_score": r.score, "sources": []} for r in retrieved],
        )

        # Record reranking
        reranked = result.get("reranked_chunks", [])
        query_trace.record_reranking(
            pre_rerank=[{"node": r.node_id, "score": r.score} for r in retrieved],
            post_rerank=[{"node": r.node_id, "score": r.score} for r in reranked],
            model=settings.reranker_model if settings.enable_reranker else "disabled",
        )

        # Record context preparation
        generation_chunks = result.get("generation_chunks", reranked)
        query_trace.record_context_preparation(
            contexts=[{"node": c.node_id, "text": c.text, "source": c.source} for c in generation_chunks],
            context_limit=None,
        )

        # Record generation attempts (simplified - would need more detailed tracking)
        query_trace.record_generation_attempt(
            answer=result.get("current_answer", result.get("final_answer", "")),
            critique=result.get("last_critique", ""),
            grader_decision=str(result.get("grader_decision", "")),
            attempt_number=result.get("iteration_count", 0) + 1,
        )
        query_trace.record_generation_summary()

        # Record final output
        query_trace.record_output(
            answer=result.get("final_answer", ""),
            grounded=result.get("semantic_verification_passed", True),
            verification_score=result.get("semantic_verification_overlap", 0.0),
            grader_decision=str(result.get("grader_decision", "")),
            sources=result.get("sources", []),
        )

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
