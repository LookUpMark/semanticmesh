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

import threading
import warnings
from pathlib import Path
from typing import TYPE_CHECKING, Any

# Suppress LangGraph msgpack deserialisation warnings for types that are
# registered below via the serde configuration. These warnings appear when
# checkpoint data created before the serde registration is replayed.
warnings.filterwarnings(
    "ignore",
    message=r"Deserializing unregistered type.*RetrievedChunk|GraderDecision|QueryTrace",
    category=UserWarning,
    module=r"langgraph\.checkpoint\.serde\.jsonplus",
)

from langchain_core.messages import AIMessage, HumanMessage
from langgraph.graph import END, StateGraph

# Re-export for backward compatibility with tests
from src.config.logging import NodeTimer, get_logger, log_node_event
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

_CONVERSATIONS_DB = Path(__file__).parent.parent.parent / "data" / "memory" / "conversations.db"
_QUERY_GRAPH_CHECKPOINT_CONN: Any = None


def _make_checkpointer():
    """Return a SqliteSaver backed by data/memory/conversations.db.

    Falls back to in-process MemorySaver if the package is not installed,
    so the server still starts without the optional dependency.

    The connection is reused on subsequent calls (singleton pattern).
    """
    global _QUERY_GRAPH_CHECKPOINT_CONN
    # Register custom types so LangGraph msgpack serialiser does not warn
    try:
        from langgraph.checkpoint.serde.jsonplus import JsonPlusSerializer  # type: ignore[import]

        _ALLOWED_MODULES = [
            ("src.models.schemas", "RetrievedChunk"),
            ("src.models.schemas", "GraderDecision"),
            ("src.config.tracing", "QueryTrace"),
        ]
        serde = JsonPlusSerializer()
        existing: list = getattr(serde, "allowed_msgpack_modules", []) or []
        for entry in _ALLOWED_MODULES:
            if entry not in existing:
                existing.append(entry)
        serde.allowed_msgpack_modules = existing  # type: ignore[attr-defined]
    except Exception:
        serde = None  # type: ignore[assignment]

    try:
        import sqlite3

        from langgraph.checkpoint.sqlite import SqliteSaver
        _CONVERSATIONS_DB.parent.mkdir(parents=True, exist_ok=True)
        if _QUERY_GRAPH_CHECKPOINT_CONN is None:
            _QUERY_GRAPH_CHECKPOINT_CONN = sqlite3.connect(str(_CONVERSATIONS_DB), check_same_thread=False)
        kwargs = {"serde": serde} if serde is not None else {}
        return SqliteSaver(_QUERY_GRAPH_CHECKPOINT_CONN, **kwargs)
    except (ImportError, TypeError):
        from langgraph.checkpoint.memory import MemorySaver
        logger.warning(
            "langgraph-checkpoint-sqlite not installed — using in-memory checkpointer. "
            "Run: pip install langgraph-checkpoint-sqlite"
        )
        kwargs = {"serde": serde} if serde is not None else {}
        try:
            return MemorySaver(**kwargs)
        except TypeError:
            return MemorySaver()


# ─────────────────────────────────────────────────────────────────────────────
# Singleton compiled graph
# ─────────────────────────────────────────────────────────────────────────────
# The same checkpointer instance must be reused across calls so that
# checkpoints (= per-session conversation history) survive across requests.
# build_query_graph() is called only once; tests may call it directly to
# get a fresh graph with an isolated checkpointer.

_QUERY_GRAPH: Any = None
_GRAPH_LOCK = threading.Lock()


def _get_query_graph():
    """Return (and lazily build) the singleton compiled query graph."""
    global _QUERY_GRAPH
    if _QUERY_GRAPH is None:
        with _GRAPH_LOCK:
            if _QUERY_GRAPH is None:
                _QUERY_GRAPH = build_query_graph()
    return _QUERY_GRAPH


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
    with NodeTimer() as timer:
        settings = get_settings()
        if not getattr(settings, "enable_retrieval_quality_gate", True):
            log_node_event(logger, "retrieval_quality_gate", "disabled", "proceed", timer.elapsed_ms)
            return {"retrieval_gate_decision": "proceed"}

        top_score = float(state.get("retrieval_quality_score", 0.0))
        chunk_count = int(state.get("retrieval_chunk_count", 0))
        sufficiency = state.get("context_sufficiency", "insufficient")
        query = str(state.get("user_query", ""))
        reranked: list[RetrievedChunk] = state.get("reranked_chunks") or []
        has_structural_evidence = _has_structural_relationship_evidence(reranked)
        relation_query = any(k in query.lower() for k in ("related", "relationship", "linked", "link"))

        if chunk_count == 0:
            log_node_event(logger, "retrieval_quality_gate", f"score={top_score:.4f} chunks=0", "abstain_early", timer.elapsed_ms)
            return {"retrieval_gate_decision": "abstain_early"}

        if chunk_count == 1 and (has_structural_evidence or relation_query):
            logger.info(
                "Retrieval gate: preserving sparse but structured evidence (score %.4f).",
                top_score,
            )
            log_node_event(logger, "retrieval_quality_gate", f"score={top_score:.4f} chunks=1 structured", "proceed_with_warning", timer.elapsed_ms)
            return {"retrieval_gate_decision": "proceed_with_warning"}

        if sufficiency == "adequate" and top_score >= 0.2:
            log_node_event(logger, "retrieval_quality_gate", f"score={top_score:.4f} chunks={chunk_count}", "proceed", timer.elapsed_ms)
            return {"retrieval_gate_decision": "proceed"}

        if top_score < 0.02 and not has_structural_evidence and chunk_count <= 2:
            logger.info(
                "Retrieval gate: near-zero score (%.4f) without structural evidence (chunks=%d); abstaining early.",
                top_score,
                chunk_count,
            )
            log_node_event(logger, "retrieval_quality_gate", f"score={top_score:.4f} chunks={chunk_count}", "abstain_early", timer.elapsed_ms)
            return {"retrieval_gate_decision": "abstain_early"}

        if top_score < 0.05 and has_structural_evidence:
            logger.info(
                "Retrieval gate: low-score but structural evidence present (chunks=%d); proceeding with warning.",
                chunk_count,
            )
            log_node_event(logger, "retrieval_quality_gate", f"score={top_score:.4f} chunks={chunk_count} structured", "proceed_with_warning", timer.elapsed_ms)
            return {"retrieval_gate_decision": "proceed_with_warning"}

        log_node_event(logger, "retrieval_quality_gate", f"score={top_score:.4f} chunks={chunk_count}", "proceed_with_warning", timer.elapsed_ms)
        return {"retrieval_gate_decision": "proceed_with_warning"}


def _node_grader_consistency_validator(state: QueryState) -> dict[str, Any]:
    """Validate grader decision consistency.

    Ensures that if a decision is marked as grounded, its action is "pass".
    Inconsistent decisions are logged as warnings.
    """
    with NodeTimer() as timer:
        settings = get_settings()
        if not getattr(settings, "enable_grader_consistency_validator", True):
            log_node_event(logger, "grader_consistency_validator", "disabled", "valid", timer.elapsed_ms)
            return {"grader_consistency_valid": True}

        from src.models.schemas import GraderDecision

        decision: GraderDecision | None = state.get("grader_decision")
        if decision is None:
            log_node_event(logger, "grader_consistency_validator", "no decision", "valid", timer.elapsed_ms)
            return {"grader_consistency_valid": True}

        valid = not (decision.grounded and decision.action != "pass")
        if not valid:
            logger.warning(
                "Grader consistency validator detected invalid decision: grounded=%s action=%s",
                decision.grounded,
                decision.action,
            )
        log_node_event(logger, "grader_consistency_validator", f"grounded={decision.grounded} action={decision.action}", f"valid={valid}", timer.elapsed_ms)
        return {"grader_consistency_valid": valid}


def _node_finalise(state: QueryState) -> dict[str, Any]:
    """Finalize query response and collect metadata for evaluation.

    Compiles the final answer with sources and retrieval metrics for RAGAS evaluation.
    Also appends the accepted AIMessage to the LangGraph-native messages state so it
    is persisted in the checkpoint and available as history for the next turn.
    """
    with NodeTimer() as timer:
        answer: str = state.get("current_answer") or ""
        gate_decision = state.get("retrieval_gate_decision", "proceed")
        if gate_decision == "abstain_early":
            answer = "I cannot find this information in the knowledge graph."
        reranked: list[RetrievedChunk] = state.get("reranked_chunks") or []
        generated_with: list[RetrievedChunk] = state.get("generation_chunks") or reranked
        sources: list[str] = [c.node_id for c in generated_with]
        # Entity names from vector/graph retrieval — used for GT coverage comparison
        entity_names: list[str] = list({
            c.node_id for c in reranked if c.source_type in ("vector", "graph")
        })
        # retrieved_contexts: full texts used by RAGAS evaluation
        retrieved_contexts: list[str] = [c.text for c in generated_with if c.text]
        log_node_event(logger, "finalise", f"gate={gate_decision} sources={len(sources)}", "finalised", timer.elapsed_ms)
        return {
        # Persist accepted answer as AIMessage via add_messages reducer.
        # Next invocation will see [..., HumanMessage(prev_q), AIMessage(prev_a), HumanMessage(curr_q)].
        "messages": [AIMessage(content=answer)],
        "final_answer": answer,
        "sources": sources,
        "entity_names": entity_names,
        "retrieved_contexts": retrieved_contexts,
        "retrieval_quality_score": float(state.get("retrieval_quality_score", 0.0)),
        "retrieval_chunk_count": int(state.get("retrieval_chunk_count", len(reranked))),
        "retrieval_filtered_by_threshold": bool(
            state.get("retrieval_filtered_by_threshold", False)
        ),
        "context_sufficiency": state.get("context_sufficiency", "insufficient"),
        "retrieval_gate_decision": gate_decision,
        "grader_grounded": bool(getattr(state.get("grader_decision"), "grounded", True)),
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
    graph.add_edge("answer_generation", "hallucination_grader")
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

    return graph.compile(checkpointer=_make_checkpointer())


# ─────────────────────────────────────────────────────────────────────────────
# Debug Tracing
# ─────────────────────────────────────────────────────────────────────────────


def _node_save_query_trace(state: QueryState) -> dict[str, Any]:
    """No-op graph node — query trace is saved AFTER graph.invoke() in run_query().

    This node exists only as a terminal graph node before END.
    The actual trace save happens after the trace has been fully populated.
    """
    return {}


def run_query(
    user_query: str,
    *,
    trace_enabled: bool = False,
    query_index: int = 0,
    builder_trace_id: str = "",
    study_id: str = "manual",
    session_id: str | None = None,
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
            "entity_names": list[str],
            "retrieved_contexts": list[str],
            "retrieval_quality_score": float,
            "retrieval_chunk_count": int,
            "retrieval_filtered_by_threshold": bool,
            "context_sufficiency": str,
            "retrieval_gate_decision": str,
            "semantic_verification_overlap": float,
            "semantic_verification_passed": bool,
            "semantic_verification_warning": str | None,
            "grader_consistency_valid": bool,
            "grader_rejection_count": int,
        }``
    """
    from src.config.settings import get_settings
    from src.config.tracing import QueryTrace

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

    # Use the singleton graph so the MemorySaver persists checkpoints across calls.
    # Tests that call build_query_graph() directly are unaffected (fresh graph).
    graph = _get_query_graph()
    thread_id = session_id if session_id else f"query-run-{query_index}"
    config = {"configurable": {"thread_id": thread_id}}
    # Ensure schema (vector index) exists before querying.
    with Neo4jClient() as client:
        setup_schema(client)
    initial: QueryState = {
        # Seed current user message; add_messages appends it to the checkpoint.
        "messages": [HumanMessage(content=user_query)],
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
        "entity_names": [],
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
        "query_trace_enabled": trace_enabled,
        "query_trace": query_trace,
        "query_index": query_index,
        "builder_trace_id": builder_trace_id,
        "trace_output_dir": settings.trace_output_dir if trace_enabled else "",
    }
    result = graph.invoke(initial, config=config)

    # Populate trace with final state data and save
    if trace_enabled and query_trace:
        from pathlib import Path

        # Record retrieval details from final state
        retrieved = result.get("retrieved_chunks", [])
        query_trace.record_retrieval(
            rrf_fused=[
                {"node": r.node_id, "rrf_score": r.score, "sources": [r.source_type]}
                for r in retrieved
            ],
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
            contexts=[
                {"node": c.node_id, "text": c.text, "source": c.source_type}
                for c in generation_chunks
            ],
            context_limit=None,
        )

        # Record generation attempts
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

        # Save trace to JSONL
        output_dir = Path(settings.trace_output_dir)
        trace_file = output_dir / f"query_traces_{study_id}.jsonl"
        query_trace.save(trace_file)
        logger.info("Query trace saved to %s", trace_file)

    return {
        "final_answer": result.get("final_answer", ""),
        "sources": result.get("sources", []),
        "entity_names": result.get("entity_names", []),
        "retrieved_contexts": result.get("retrieved_contexts", []),
        "retrieval_quality_score": result.get("retrieval_quality_score", 0.0),
        "retrieval_chunk_count": result.get("retrieval_chunk_count", 0),
        "retrieval_filtered_by_threshold": result.get("retrieval_filtered_by_threshold", False),
        "context_sufficiency": result.get("context_sufficiency", "insufficient"),
        "retrieval_gate_decision": result.get("retrieval_gate_decision", "proceed"),
        "semantic_verification_overlap": result.get("semantic_verification_overlap", 1.0),
        "semantic_verification_passed": result.get("semantic_verification_passed", True),
        "semantic_verification_warning": result.get("semantic_verification_warning"),
        "grader_grounded": bool(
            getattr(result.get("grader_decision"), "grounded", True)
        ),
        "grader_consistency_valid": result.get("grader_consistency_valid", True),
        "grader_rejection_count": result.get("grader_rejection_count", 0),
    }
