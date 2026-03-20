"""Query LangGraph — EP-15 / US-15-01.

Wires hybrid retrieval → reranking → answer generation → hallucination grader
(with regeneration loop) into a compiled StateGraph.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any
import re

from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import END, StateGraph

from src.config.llm_factory import get_reasoning_llm
from src.config.logging import get_logger
from src.config.settings import get_settings
from src.generation.answer_generator import generate_answer
from src.generation.hallucination_grader import grade_answer
from src.generation.lazy_expander import (
    collect_seed_names_for_expansion,
    should_trigger_lazy_expansion,
)
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

_TOKEN_RE = re.compile(r"[a-zA-Z0-9_]+")
_NOISE_MARKERS = (
    "heuristic embedding mapping score=",
    "adjusted_confidence=",
    "best_candidate=",
)


def _has_structural_relationship_evidence(chunks: list[RetrievedChunk]) -> bool:
    """Return True when chunks carry explicit relational/schema evidence."""
    for chunk in chunks:
        node_id = chunk.node_id.strip().lower()
        text = chunk.text.strip().lower()
        if "→" in node_id:
            return True
        if any(token in text for token in ("references", "foreign key", "fk ", " fk", "joins", "join ")):
            return True
    return False


def _query_terms(query: str) -> set[str]:
    stop = {
        "what",
        "which",
        "where",
        "when",
        "how",
        "does",
        "the",
        "this",
        "that",
        "with",
        "into",
        "from",
        "table",
        "database",
        "business",
        "concept",
        "information",
        "schema",
        "knowledge",
        "graph",
    }
    terms = {
        t.lower()
        for t in _TOKEN_RE.findall(query)
        if len(t) > 2 and t.lower() not in stop
    }
    return terms


def _is_noise_chunk(chunk: RetrievedChunk) -> bool:
    text = chunk.text.lower()
    if any(marker in text for marker in _NOISE_MARKERS):
        return True
    if len(chunk.text.strip()) < 18 and "→" not in chunk.node_id:
        return True
    return False


def _pre_filter_rerank_pool(
    chunks: list[RetrievedChunk],
    query: str,
    max_candidates: int,
) -> list[RetrievedChunk]:
    if not chunks:
        return []

    terms = _query_terms(query)

    def _chunk_priority(chunk: RetrievedChunk) -> tuple[int, int, int, float]:
        text_l = chunk.text.lower()
        nid_l = chunk.node_id.lower()
        has_structure = int("→" in chunk.node_id or any(k in text_l for k in ("references", "foreign key")))
        keyword_hits = int(any(term in text_l or term in nid_l for term in terms))
        source_rank = 2 if chunk.source_type in {"vector", "bm25"} else 1
        return (has_structure, keyword_hits, source_rank, float(chunk.score))

    selected: list[RetrievedChunk] = []
    dropped_noise = 0
    for chunk in chunks:
        if not chunk.node_id.strip() or not chunk.text.strip():
            continue
        if _is_noise_chunk(chunk):
            dropped_noise += 1
            continue
        selected.append(chunk)

    if not selected:
        # Never starve downstream nodes: keep original valid chunks when filter is too strict.
        selected = [c for c in chunks if c.node_id.strip() and c.text.strip()]

    selected.sort(key=_chunk_priority, reverse=True)
    limited = selected[:max_candidates]
    if dropped_noise:
        logger.info(
            "Pre-rerank quality filter dropped %d noisy chunk(s); kept %d/%d candidates.",
            dropped_noise,
            len(limited),
            len(chunks),
        )
    return limited


def _compose_generation_chunks(
    query: str,
    chunks: list[RetrievedChunk],
    max_core: int = 6,
    max_support: int = 4,
) -> list[RetrievedChunk]:
    """Build a balanced context window for answer generation.

    Strategy:
    - `core`: most query-relevant and structural chunks
    - `support`: additional diverse evidence from remaining chunks
    """
    if not chunks:
        return []

    terms = _query_terms(query)

    def _priority(chunk: RetrievedChunk) -> tuple[int, int, int, float]:
        text_l = chunk.text.lower()
        nid_l = chunk.node_id.lower()
        has_structure = int("→" in chunk.node_id or any(k in text_l for k in ("references", "foreign key")))
        keyword_hits = int(any(term in text_l or term in nid_l for term in terms))
        source_rank = 2 if chunk.source_type in {"vector", "bm25"} else 1
        return (keyword_hits, has_structure, source_rank, float(chunk.score))

    ranked = sorted(chunks, key=_priority, reverse=True)
    core = ranked[:max_core]

    support: list[RetrievedChunk] = []
    core_ids = {c.node_id for c in core}
    seen_sources = {c.source_type for c in core}
    for chunk in ranked[max_core:]:
        if chunk.node_id in core_ids:
            continue
        # Prefer source diversity in support evidence.
        if len(support) < max_support:
            if chunk.source_type not in seen_sources or len(seen_sources) < 2:
                support.append(chunk)
                seen_sources.add(chunk.source_type)
                continue
            if len(support) < max_support:
                support.append(chunk)

    composed = core + support[:max_support]
    return composed


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

            if getattr(settings, "enable_lazy_expansion", False):
                top_score = float(merged[0].score) if merged else 0.0
                if should_trigger_lazy_expansion(
                    top_score,
                    len(merged),
                    float(getattr(settings, "lazy_expansion_confidence_threshold", 0.40)),
                ):
                    seeds = collect_seed_names_for_expansion(merged, limit=8)
                    extra = graph_traversal(
                        seed_names=seeds,
                        client=client,
                        depth=max(1, settings.retrieval_graph_depth + 1),
                    )
                    merged = merge_results(vec_results, bm25_results, trav_results + extra + all_concepts + fk_chunks)
    return {"retrieved_chunks": merged}


def _node_reranking(state: QueryState) -> dict[str, Any]:
    settings = get_settings()
    query: str = state["user_query"]
    chunks: list[RetrievedChunk] = state.get("retrieved_chunks") or []
    max_pool = max(settings.reranker_top_k * 4, settings.reranker_top_k)
    pool = _pre_filter_rerank_pool(chunks, query=query, max_candidates=max_pool)

    if not settings.enable_reranker:
        candidates = pool[: settings.reranker_top_k]
    else:
        candidates = rerank(query, pool, top_k=settings.reranker_top_k)

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
    if len(valid) == 1:
        sufficiency = "sparse"
    else:
        sufficiency = "adequate"

    return {
        "reranked_chunks": valid,
        "retrieval_quality_score": top_score,
        "retrieval_chunk_count": len(valid),
        "retrieval_filtered_by_threshold": False,
        "context_sufficiency": sufficiency,
    }


def _node_answer_generation(state: QueryState) -> dict[str, Any]:
    llm = get_reasoning_llm()
    query: str = state["user_query"]
    chunks: list[RetrievedChunk] = state.get("reranked_chunks") or []
    generation_chunks = _compose_generation_chunks(query, chunks)
    critique: str | None = state.get("last_critique")
    sufficiency: str = state.get("context_sufficiency", "insufficient")
    if generation_chunks and sufficiency != "adequate":
        logger.warning(
            "Generating answer with %s context (chunks=%d).",
            sufficiency,
            len(generation_chunks),
        )
    answer = generate_answer(
        query,
        generation_chunks,
        llm,
        critique=critique,
        context_sufficiency=sufficiency,
    )
    iteration = state.get("iteration_count", 0) + 1
    return {
        "current_answer": answer,
        "iteration_count": iteration,
        "last_critique": None,
        "generation_chunks": generation_chunks,
    }


def _node_retrieval_quality_gate(state: QueryState) -> dict[str, Any]:
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
    settings = get_settings()
    if not getattr(settings, "enable_semantic_verifier", True):
        return {
            "semantic_verification_overlap": 1.0,
            "semantic_verification_passed": True,
            "semantic_verification_warning": None,
        }

    answer = (state.get("current_answer") or "").lower()
    chunks: list[RetrievedChunk] = state.get("reranked_chunks") or []
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
