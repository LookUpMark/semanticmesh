"""Hallucination grader — adversarial LLM audit of generated answers.

EP-14 / US-14-02:
Determines if the generated answer is grounded in the retrieved context.
Returns a GraderDecision driving the Query Graph routing.
"""

from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor, TimeoutError as FutureTimeoutError
import json
from typing import TYPE_CHECKING

from langchain_core.messages import HumanMessage, SystemMessage
from pydantic import ValidationError

from src.config.logging import get_logger
from src.config.settings import get_settings
from src.generation.answer_generator import format_context
from src.prompts.templates import GRADER_SYSTEM, GRADER_USER, REFLECTION_TEMPLATE

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

    _pass = GraderDecision(
        grounded=True,
        critique=None,
        action="pass",
        timeout_occurred=False,
        parse_attempts=1,
        consistency_corrections=0,
        certainty=0.5,
    )
    _fmt = '{"grounded": <bool>, "critique": "<str|null>", "action": "<pass|regenerate>"}'

    context_block = format_context(chunks)
    user_prompt = GRADER_USER.format(
        context_chunks=context_block,
        generated_answer=answer,
        user_query=query,
    )

    settings = get_settings()

    def _invoke_with_timeout(messages: list[SystemMessage | HumanMessage]) -> str:
        timeout_seconds = float(getattr(settings, "grader_timeout_seconds", 12.0))
        with ThreadPoolExecutor(max_workers=1) as executor:
            future = executor.submit(llm.invoke, messages)
            response = future.result(timeout=timeout_seconds)
        return str(response.content).strip()

    try:
        raw_json = _invoke_with_timeout(
            [
                SystemMessage(content=GRADER_SYSTEM),
                HumanMessage(content=user_prompt),
            ]
        )
    except FutureTimeoutError:
        logger.warning("Grader timed out — defaulting to pass.")
        return GraderDecision(
            grounded=True,
            critique=None,
            action="pass",
            timeout_occurred=True,
            parse_attempts=0,
            consistency_corrections=0,
            certainty=0.2,
        )
    except Exception as exc:
        logger.warning("Grader LLM call failed (%s) — defaulting to pass.", exc)
        return _pass

    max_attempts: int = settings.max_reflection_attempts
    parse_attempts = 0
    consistency_corrections = 0
    corrected_once = False

    for attempt in range(1, max_attempts + 1):
        parse_attempts = attempt
        try:
            data: dict = json.loads(raw_json)
            decision = GraderDecision(**data)
        except (json.JSONDecodeError, ValidationError) as exc:
            logger.warning(
                "Grader response parse/validation error (attempt %d/%d): %s",
                attempt,
                max_attempts,
                exc,
            )
            if attempt == max_attempts:
                return GraderDecision(
                    grounded=True,
                    critique=None,
                    action="pass",
                    timeout_occurred=False,
                    parse_attempts=parse_attempts,
                    consistency_corrections=consistency_corrections,
                    certainty=0.3,
                )
            try:
                raw_json = _invoke_with_timeout(
                    [
                        HumanMessage(
                            content=REFLECTION_TEMPLATE.format(
                                role="strict factual auditor",
                                output_format=f"JSON object matching {_fmt}",
                                error_or_critique=str(exc),
                                original_input=raw_json,
                            )
                        )
                    ]
                )
            except FutureTimeoutError:
                logger.warning("Grader reflection timed out — defaulting to pass.")
                return GraderDecision(
                    grounded=True,
                    critique=None,
                    action="pass",
                    timeout_occurred=True,
                    parse_attempts=parse_attempts,
                    consistency_corrections=consistency_corrections,
                    certainty=0.2,
                )
            continue

        # Consistency check: grounded=True must have action="pass"
        if decision.grounded and decision.action != "pass":
            logger.warning(
                "Grader inconsistency (grounded=True but action=%s) — requesting one correction.",
                decision.action,
            )
            if corrected_once:
                return GraderDecision(
                    grounded=True,
                    critique=None,
                    action="pass",
                    timeout_occurred=False,
                    parse_attempts=parse_attempts,
                    consistency_corrections=consistency_corrections,
                    certainty=0.3,
                )

            corrected_once = True
            consistency_corrections += 1
            correction_prompt = REFLECTION_TEMPLATE.format(
                role="strict factual auditor",
                output_format=f"JSON object matching {_fmt}",
                error_or_critique=(
                    "Your JSON is internally inconsistent: grounded=true requires action='pass'. "
                    "Return a corrected decision now."
                ),
                original_input=json.dumps(data),
            )
            try:
                raw_json = _invoke_with_timeout([HumanMessage(content=correction_prompt)])
            except FutureTimeoutError:
                logger.warning("Grader consistency correction timed out — defaulting to pass.")
                return GraderDecision(
                    grounded=True,
                    critique=None,
                    action="pass",
                    timeout_occurred=True,
                    parse_attempts=parse_attempts,
                    consistency_corrections=consistency_corrections,
                    certainty=0.2,
                )
            continue

        decision.parse_attempts = parse_attempts
        decision.consistency_corrections = consistency_corrections

        logger.info(
            "Grader verdict: grounded=%s, action=%s, certainty=%.2f, parse_attempts=%d, critique=%r.",
            decision.grounded,
            decision.action,
            decision.certainty,
            decision.parse_attempts,
            (decision.critique or "")[:120],
        )
        return decision

    return _pass
