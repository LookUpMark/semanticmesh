"""Hallucination grader — adversarial LLM audit of generated answers.

EP-14 / US-14-02:
Determines if the generated answer is grounded in the retrieved context.
Returns a GraderDecision driving the Query Graph routing.
"""

from __future__ import annotations

import json
from typing import TYPE_CHECKING

from langchain_core.messages import HumanMessage, SystemMessage
from pydantic import ValidationError

from src.config.logging import get_logger
from src.generation.answer_generator import format_context
from src.prompts.templates import GRADER_SYSTEM, GRADER_USER

if TYPE_CHECKING:
    import logging

    from src.config.llm_client import LLMProtocol
    from src.models.schemas import GraderDecision, RetrievedChunk

logger: logging.Logger = get_logger(__name__)


def grade_answer(
    query: str,
    answer: str,
    chunks: list[RetrievedChunk],
    llm: LLMProtocol,
) -> GraderDecision:
    """Audit a generated answer for unsupported claims against the context chunks.

    The grader LLM receives the user's original question, the generated answer,
    and all context chunks in numbered format. It returns a JSON object matching
    ``GraderDecision``. On any parse or validation error the grader defaults to
    ``grounded=True, action="pass"`` to avoid blocking the pipeline.

    Args:
        query:   The user's natural-language question.
        answer:  The generated answer to audit.
        chunks:  Reranked context chunks used during generation.
        llm:     Reasoning LLM — temperature MUST be 0.0 (deterministic audit).

    Returns:
        ``GraderDecision`` with ``grounded``, ``critique``, and ``action`` fields.
    """
    from src.models.schemas import GraderDecision  # noqa: PLC0415

    context_block = format_context(chunks)
    user_prompt = GRADER_USER.format(
        context_chunks=context_block,
        generated_answer=answer,
        user_query=query,
    )

    try:
        response = llm.invoke(
            [
                SystemMessage(content=GRADER_SYSTEM),
                HumanMessage(content=user_prompt),
            ]
        )
        raw_json: str = response.content.strip()
    except Exception as exc:
        logger.warning("Grader LLM call failed (%s) — defaulting to pass.", exc)
        return GraderDecision(grounded=True, critique=None, action="pass")

    try:
        data: dict = json.loads(raw_json)
        decision = GraderDecision(**data)
    except (json.JSONDecodeError, ValidationError) as exc:
        logger.warning("Grader response parse error (%s) — defaulting to pass.", exc)
        return GraderDecision(grounded=True, critique=None, action="pass")

    # Consistency check: grounded=True must have action="pass"
    if decision.grounded and decision.action != "pass":
        logger.warning(
            "Grader inconsistency (grounded=True but action=%s) — forcing pass.",
            decision.action,
        )
        return GraderDecision(grounded=True, critique=None, action="pass")

    logger.info(
        "Grader verdict: grounded=%s, action=%s, critique=%r.",
        decision.grounded, decision.action,
        (decision.critique or "")[:120],
    )
    return decision
