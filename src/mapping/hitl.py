"""Human-in-the-Loop breakpoint node for the Builder Graph.

EP-08 / US-08-01: Calls langgraph.types.interrupt() to suspend the graph
and wait for human input (approve / correct / reject).
"""

from __future__ import annotations

import logging
from typing import Literal

from langgraph.types import Command, interrupt

from src.config.logging import get_logger
from src.config.settings import get_settings
from src.models.schemas import Entity, MappingProposal
from src.models.state import BuilderState

logger: logging.Logger = get_logger(__name__)
_settings = get_settings()

HumanAction = Literal["approve", "correct", "reject"]


# ── Pure Predicate ─────────────────────────────────────────────────────────────


def should_interrupt(state: BuilderState) -> bool:
    """Return True if the HITL breakpoint must fire.

    Triggers when:
    - the graph's ``hitl_flag`` is explicitly set to True, OR
    - the current mapping proposal has confidence below ``settings.confidence_threshold``.

    This function is used both inside ``hitl_node`` and as a conditional edge
    predicate so the graph can skip the node entirely on high-confidence runs.
    """
    if state.get("hitl_flag", False):
        return True
    proposal: MappingProposal | None = state.get("mapping_proposal")
    if proposal is not None and proposal.confidence < _settings.confidence_threshold:
        return True
    return False


# ── Payload Builder ────────────────────────────────────────────────────────────


def build_interrupt_payload(
    proposal: MappingProposal,
    entities: list[Entity],
) -> dict:
    """Assemble the structured payload delivered to the human reviewer.

    Args:
        proposal: The candidate mapping from ``propose_mapping``.
        entities: All resolved entities available; used to list alternatives.

    Returns:
        A plain ``dict`` that the checkpoint store serialises for the reviewer.
        Keys:
        - ``table_name`` — table being mapped
        - ``proposed_concept`` — chosen business concept
        - ``confidence`` — [0.0, 1.0] score
        - ``reasoning`` — LLM rationale
        - ``alternative_concepts`` — up to 4 other candidates
        - ``provenance_text`` — concatenated provenance texts from top entities
    """
    all_concept_names: list[str] = [e.name for e in entities if e.name != proposal.mapped_concept]
    alternatives: list[str] = (proposal.alternative_concepts or []) + all_concept_names
    unique_alternatives: list[str] = list(dict.fromkeys(alternatives))[:4]

    provenance_texts: list[str] = [e.provenance_text for e in entities[:3] if e.provenance_text]

    return {
        "table_name": proposal.table_name,
        "proposed_concept": proposal.mapped_concept,
        "confidence": proposal.confidence,
        "reasoning": proposal.reasoning,
        "alternative_concepts": unique_alternatives,
        "provenance_text": " | ".join(provenance_texts),
    }


# ── HITL LangGraph Node ────────────────────────────────────────────────────────


def hitl_node(state: BuilderState) -> Command:
    """LangGraph node that suspends execution pending human review.

    If ``should_interrupt`` is False the node skips the interrupt and returns a
    ``Command(goto="Generate_Cypher")`` immediately (pass-through).

    When interrupted, the graph resumes only after a human sends a ``Command``
    resumption value with structure::

        {
            "action": "approve" | "correct" | "reject",
            "mapped_concept": "<str>"   # only required for "correct"
        }

    On ``"approve"`` — routes to ``"Generate_Cypher"`` unchanged.
    On ``"correct"`` — patches ``mapping_proposal.mapped_concept`` and routes to ``"Generate_Cypher"``.
    On ``"reject"``  — marks ``rejected=True`` and routes to ``"End"``.

    Args:
        state: Current ``BuilderState`` snapshot.

    Returns:
        A LangGraph ``Command`` that updates state and selects the next node.
    """
    proposal: MappingProposal | None = state.get("mapping_proposal")
    entities: list[Entity] = state.get("current_entities") or []

    # ── Pass-through if no interrupt needed ──
    if not should_interrupt(state):
        logger.debug(
            "HITL pass-through: confidence=%.2f ≥ %.2f",
            proposal.confidence if proposal else 0.0,
            _settings.confidence_threshold,
        )
        return Command(goto="Generate_Cypher")

    if proposal is None:
        logger.warning("HITL triggered but mapping_proposal is None — routing to End.")
        return Command(update={"rejected": True}, goto="End")

    payload = build_interrupt_payload(proposal, entities)
    logger.info(
        "HITL interrupt fired for table '%s' (confidence=%.2f).",
        proposal.table_name,
        proposal.confidence,
    )

    # ── Suspend and wait for human input ──────────────────────────────────────
    human_response: dict = interrupt(payload)
    # Execution resumes only after a Command is submitted by the human.
    # ``human_response`` is whatever dict the reviewer provides.

    action: HumanAction = human_response.get("action", "approve")

    if action == "approve":
        logger.info("HITL: human approved mapping '%s'.", proposal.mapped_concept)
        return Command(goto="Generate_Cypher")

    if action == "correct":
        corrected_concept: str | None = human_response.get("mapped_concept")
        if not corrected_concept:
            logger.warning("HITL 'correct' action has no mapped_concept — treating as approve.")
            return Command(goto="Generate_Cypher")

        corrected_proposal = proposal.model_copy(
            update={"mapped_concept": corrected_concept, "confidence": 1.0}
        )
        logger.info(
            "HITL: human corrected '%s' → '%s'.",
            proposal.mapped_concept,
            corrected_concept,
        )
        return Command(
            update={"mapping_proposal": corrected_proposal},
            goto="Generate_Cypher",
        )

    if action == "reject":
        logger.info("HITL: human rejected mapping for table '%s'.", proposal.table_name)
        return Command(update={"rejected": True}, goto="End")

    logger.warning("Unknown HITL action '%s' — treating as approve.", action)
    return Command(goto="Generate_Cypher")
