"""Answer generation and hallucination grading nodes.

Nodes:
- _node_answer_generation: Generate answer with critique injection
- _node_grade_hallucination: Self-RAG hallucination detection
"""

from __future__ import annotations

import re
from typing import TYPE_CHECKING, Any

from src.config.llm_factory import get_midtier_llm, get_reasoning_llm
from src.config.logging import NodeTimer, get_logger, log_node_event
from src.config.settings import get_settings
from src.generation.answer_generator import generate_answer
from src.generation.hallucination_grader import grade_answer
from src.models.schemas import GraderDecision, RetrievedChunk
from src.models.state import QueryState

if TYPE_CHECKING:
    import logging

    from langchain_core.messages import BaseMessage

logger: logging.Logger = get_logger(__name__)

_TOKEN_RE = re.compile(r"[a-zA-Z0-9_]+")
_PRIORITY_STRUCTURE_TOKENS = ("references", "foreign key")


# ── Helper Functions ──


def _query_terms(query: str) -> set[str]:
    from src.utils.query_utils import query_terms as _qt

    return _qt(query)


def _has_priority_structure_tokens(text: str) -> bool:
    return any(token in text for token in _PRIORITY_STRUCTURE_TOKENS)


def _compose_generation_chunks(
    query: str,
    chunks: list[RetrievedChunk],
    max_core: int | None = None,
    max_support: int | None = None,
) -> list[RetrievedChunk]:
    """Build a balanced context window for answer generation.

    Strategy:
    - `core`: most query-relevant and structural chunks
    - `support`: additional diverse evidence from remaining chunks

    Enforces per-source soft caps to prevent any single retrieval channel
    from flooding the generation context.
    """
    if not chunks:
        return []

    settings = get_settings()
    _max_core = max_core if max_core is not None else settings.generation_max_core_chunks
    _max_support = (
        max_support if max_support is not None else settings.generation_max_support_chunks
    )

    terms = _query_terms(query)

    def _priority(chunk: RetrievedChunk) -> tuple[int, int, int, float]:
        text_l = chunk.text.lower()
        nid_l = chunk.node_id.lower()
        has_structure = int("→" in chunk.node_id or _has_priority_structure_tokens(text_l))
        keyword_hits = sum(1 for term in terms if term in text_l or term in nid_l)
        source_rank = 2 if chunk.source_type in {"vector", "bm25"} else 1
        return (keyword_hits, has_structure, source_rank, float(chunk.score))

    ranked = sorted(chunks, key=_priority, reverse=True)
    target = _max_core + _max_support

    source_caps: dict[str, int] = {
        "vector": min(6, target),
        "bm25": min(6, target),
        "graph": min(6, target),
    }

    selected: list[RetrievedChunk] = []
    selected_ids: set[str] = set()
    source_counts: dict[str, int] = {"vector": 0, "bm25": 0, "graph": 0}

    for chunk in ranked:
        if len(selected) >= target:
            break
        if chunk.node_id in selected_ids:
            continue
        cap = source_caps.get(chunk.source_type, target)
        if source_counts.get(chunk.source_type, 0) >= cap:
            continue
        selected.append(chunk)
        selected_ids.add(chunk.node_id)
        source_counts[chunk.source_type] = source_counts.get(chunk.source_type, 0) + 1

    if len(selected) < target:
        for chunk in ranked:
            if len(selected) >= target:
                break
            if chunk.node_id in selected_ids:
                continue
            selected.append(chunk)
            selected_ids.add(chunk.node_id)

    core = selected[:_max_core]
    support = selected[_max_core:target]
    return core + support


def _filter_chunks_by_source(
    chunks: list[RetrievedChunk], source_type: str
) -> list[RetrievedChunk]:
    return [c for c in chunks if c.source_type == source_type]


# ── Node Implementations ──


def _node_answer_generation(state: QueryState) -> dict[str, Any]:
    """Generate answer with optional critique injection for regeneration loop.

    Composes a balanced context window from reranked chunks, prioritizing
    query relevance and structural evidence while enforcing per-source caps.
    """
    with NodeTimer() as timer:
        llm = get_reasoning_llm()
        query: str = state["user_query"]
        chunks: list[RetrievedChunk] = state.get("reranked_chunks") or []
        generation_chunks = state.get("generation_chunks") or _compose_generation_chunks(
            query, chunks
        )
        critique: str | None = state.get("last_critique")
        sufficiency: str = state.get("context_sufficiency", "insufficient")

        # Extract conversation history from LangGraph-native messages state.
        # messages = [...prior turns..., HumanMessage(current_query)]
        # History = everything except the last message (the current user query).
        all_messages: list[BaseMessage] = list(state.get("messages") or [])
        history: list[BaseMessage] | None = all_messages[:-1] if len(all_messages) > 1 else None

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
            history=history,
        )
        iteration = state.get("iteration_count", 0) + 1
        log_node_event(
            logger,
            "answer_generation",
            f"iteration={iteration} chunks={len(generation_chunks)}",
            "answer generated",
            timer.elapsed_ms,
            model_used=get_settings().llm_model_reasoning,
        )
        return {
            "current_answer": answer,
            "iteration_count": iteration,
            "last_critique": None,
            "generation_chunks": generation_chunks,
        }


def _node_grade_hallucination(state: QueryState) -> dict[str, Any]:
    """Grade answer for hallucinations using Self-RAG paradigm.

    Implements loop guard: after max_hallucination_retries, forces acceptance
    to prevent infinite regeneration loops.
    """
    with NodeTimer() as timer:
        settings = get_settings()
        if not settings.enable_hallucination_grader:
            log_node_event(logger, "grade_hallucination", "disabled", "pass", timer.elapsed_ms)
            return {"grader_decision": GraderDecision(grounded=True, critique=None, action="pass")}
        llm = get_midtier_llm()
        query: str = state["user_query"]
        answer: str = state.get("current_answer") or ""
        chunks: list[RetrievedChunk] = (
            state.get("generation_chunks") or state.get("reranked_chunks") or []
        )
        iteration: int = state.get("iteration_count", 0)

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
        log_node_event(
            logger,
            "grade_hallucination",
            f"iteration={iteration}",
            f"action={decision.action}",
            timer.elapsed_ms,
        )
        return update
