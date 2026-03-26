"""Answer generation and web search fallback.

EP-14 / US-14-01 and US-14-03:
  * generate_answer       — LLM answer from reranked context chunks
  * web_search_fallback   — external search when graph context is empty/irrelevant
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from langchain_core.messages import HumanMessage, SystemMessage

from src.config.logging import get_logger
from src.utils.json_utils import extract_text_content
from src.prompts.templates import (
    ANSWER_SYSTEM_ADEQUATE,
    ANSWER_SYSTEM_INSUFFICIENT,
    ANSWER_SYSTEM_SPARSE,
    ANSWER_USER,
    ANSWER_WITH_CRITIQUE_USER,
)

if TYPE_CHECKING:
    import logging

    from src.config.llm_client import LLMProtocol
    from src.models.schemas import RetrievedChunk

logger: logging.Logger = get_logger(__name__)

_ABSTENTION_SENTINEL = "i cannot find this information in the knowledge graph."


def _is_abstention(answer: str) -> bool:
    return answer.strip().lower() == _ABSTENTION_SENTINEL


# ── Context Formatter ──


def format_context(chunks: list[RetrievedChunk]) -> str:
    """Format reranked chunks as a numbered list for the answer prompt.

    Args:
        chunks: Reranked ``RetrievedChunk`` list (score-descending order).

    Returns:
        Multi-line string with numbered chunks, types, and scores.
    """
    if not chunks:
        return "(no context retrieved)"
    lines: list[str] = []
    for i, chunk in enumerate(chunks, start=1):
        lines.append(f"[{i}] {chunk.text}  [type={chunk.node_type}, score={chunk.score:.3f}]")
    return "\n".join(lines)


# ── Answer Generator ──


def generate_answer(
    query: str,
    chunks: list[RetrievedChunk],
    llm: LLMProtocol,
    critique: str | None = None,
    context_sufficiency: str = "insufficient",
) -> str:
    """Generate a grounded natural-language answer from reranked context chunks.

    If ``critique`` is provided (from the Hallucination Grader on a retry), the
    alternative ``ANSWER_WITH_CRITIQUE_USER`` template is used, which embeds the
    previous critique before the question so the model can correct its answer.

    Args:
        query:    The user's natural-language question.
        chunks:   Reranked ``RetrievedChunk`` list.
        llm:      Reasoning LLM (temperature = ``settings.llm_temperature_generation``).
        critique: Optional Hallucination Grader critique from the previous attempt.

    Returns:
        The generated answer string.
    """
    context_block = format_context(chunks)

    if critique:
        user_prompt = ANSWER_WITH_CRITIQUE_USER.format(
            context_chunks=context_block,
            hallucination_critique=critique,
            user_query=query,
        )
    else:
        user_prompt = ANSWER_USER.format(
            context_chunks=context_block,
            user_query=query,
        )

    if context_sufficiency == "adequate":
        system_prompt = ANSWER_SYSTEM_ADEQUATE
    elif context_sufficiency == "sparse":
        system_prompt = ANSWER_SYSTEM_SPARSE
    else:
        system_prompt = ANSWER_SYSTEM_INSUFFICIENT

    logger.debug(
        "generate_answer: query='%s', %d chunks, critique=%s.",
        query[:60],
        len(chunks),
        "yes" if critique else "no",
    )
    response = llm.invoke(
        [
            SystemMessage(content=system_prompt),
            HumanMessage(content=user_prompt),
        ]
    )
    answer: str = extract_text_content(response.content).strip()

    if _is_abstention(answer) and chunks:
        top_score = max(float(c.score) for c in chunks)
        if top_score >= 0.2:
            logger.warning(
                "Abstention with non-empty context (chunks=%d, top_score=%.3f) — forcing best-effort rewrite.",
                len(chunks),
                top_score,
            )
            corrective_critique = (
                "The previous answer abstained despite available retrieved context. "
                "Provide the best grounded answer from context and explicitly state uncertainty "
                "for missing details. Do not use the generic abstention sentence unless context is empty."
            )
            corrective_prompt = ANSWER_WITH_CRITIQUE_USER.format(
                context_chunks=context_block,
                hallucination_critique=corrective_critique,
                user_query=query,
            )
            second_response = llm.invoke(
                [
                    SystemMessage(content=system_prompt),
                    HumanMessage(content=corrective_prompt),
                ]
            )
            answer = extract_text_content(second_response.content).strip()

    logger.info("Answer generated (%d chars).", len(answer))
    return answer
