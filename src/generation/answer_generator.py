"""Answer generation and web search fallback.

EP-14 / US-14-01 and US-14-03:
  * generate_answer       — LLM answer from reranked context chunks
  * web_search_fallback   — external search when graph context is empty/irrelevant
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from langchain_core.messages import HumanMessage, SystemMessage

from src.config.logging import get_logger
from src.prompts.templates import ANSWER_SYSTEM, ANSWER_USER, ANSWER_WITH_CRITIQUE_USER

if TYPE_CHECKING:
    import logging

    from src.config.llm_client import LLMProtocol
    from src.models.schemas import RetrievedChunk

logger: logging.Logger = get_logger(__name__)


# ── Context Formatter ─────────────────────────────────────────────────────────

def format_context(chunks: list[RetrievedChunk]) -> str:
    """Format reranked chunks as a numbered list for injection into the answer prompt.

    Args:
        chunks: Reranked ``RetrievedChunk`` list (passed in score-descending order).

    Returns:
        Multi-line string like::

            [1] Customer: A person who buys products. (score=0.97)
            [2] Order: A purchase transaction. (score=0.88)
    """
    if not chunks:
        return "(no context retrieved)"
    lines: list[str] = []
    for i, chunk in enumerate(chunks, start=1):
        lines.append(f"[{i}] {chunk.text}  [type={chunk.node_type}, score={chunk.score:.3f}]")
    return "\n".join(lines)


# ── Answer Generator ──────────────────────────────────────────────────────────

def generate_answer(
    query: str,
    chunks: list[RetrievedChunk],
    llm: LLMProtocol,
    critique: str | None = None,
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

    logger.debug(
        "generate_answer: query='%s', %d chunks, critique=%s.",
        query[:60], len(chunks), "yes" if critique else "no",
    )
    response = llm.invoke(
        [
            SystemMessage(content=ANSWER_SYSTEM),
            HumanMessage(content=user_prompt),
        ]
    )
    answer: str = response.content.strip()
    logger.info("Answer generated (%d chars).", len(answer))
    return answer

