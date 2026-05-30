"""Routing functions for the query graph conditional edges."""

from __future__ import annotations

from src.models.schemas import GraderDecision
from src.models.state import QueryState


def _route_after_grader(state: QueryState) -> str:
    """Route based on grader decision action.

    Returns:
        "finalise" if answer is grounded or max retries reached
        "answer_generation" if regeneration is needed
    """
    decision: GraderDecision | None = state.get("grader_decision")
    if decision is None or decision.action == "pass":
        return "finalise"
    if decision.action == "regenerate":
        return "answer_generation"
    return "finalise"


def _route_after_retrieval_gate(state: QueryState) -> str:
    """Route after retrieval quality gate.

    Returns:
        "finalise" if retrieval quality is too low (abstain_early)
        "context_distillation" if retrieval is adequate
    """
    decision = state.get("retrieval_gate_decision", "proceed")
    if decision == "abstain_early":
        return "finalise"
    return "context_distillation"


def _route_after_consistency_validator(state: QueryState) -> str:
    # AUDIT-089: When grounded=True but action!="pass", we intentionally route
    # to regeneration (via _route_after_grader) rather than auto-correcting to
    # action="pass". This is the safer choice: the grader's inconsistency signals
    # uncertainty, and regenerating is preferable to accepting a potentially flawed answer.
    return _route_after_grader(state)
