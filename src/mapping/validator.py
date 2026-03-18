"""Mapping validation — Pydantic schema check + LLM Actor-Critic.

EP-07: Two-layer validation to catch both structural and semantic errors
in MappingProposal objects before they proceed to Cypher generation.
"""

from __future__ import annotations

import json
import logging
import time
from concurrent.futures import ThreadPoolExecutor, TimeoutError as FutureTimeoutError
from typing import TYPE_CHECKING

from langchain_core.messages import HumanMessage, SystemMessage
from pydantic import ValidationError

from src.config.logging import get_logger
from src.models.schemas import CriticDecision, Entity, MappingProposal, TableSchema
from src.prompts.templates import CRITIC_SYSTEM, CRITIC_USER, REFLECTION_TEMPLATE

if TYPE_CHECKING:
    from src.config.llm_client import LLMProtocol

logger: logging.Logger = get_logger(__name__)
_CRITIC_TIMEOUT_SECONDS = 120


# ── Layer 1: Pydantic Schema Validation ───────────────────────────────────────


def validate_schema(
    proposal_dict: dict,
) -> tuple[MappingProposal | None, str | None]:
    """Validate a raw LLM-produced dict as a MappingProposal.

    Args:
        proposal_dict: Raw dict from JSON parsing of the LLM response.

    Returns:
        ``(MappingProposal, None)`` on success.
        ``(None, error_string)`` on ``ValidationError``; the error string is
        the full Pydantic error representation, ready to inject into REFLECTION_TEMPLATE.
    """
    try:
        proposal = MappingProposal(**proposal_dict)
        return proposal, None
    except ValidationError as exc:
        error_str = str(exc)
        logger.warning("MappingProposal schema validation failed: %s", error_str)
        return None, error_str


# ── Layer 2: LLM Actor-Critic ─────────────────────────────────────────────────


def critic_review(
    proposal: MappingProposal,
    table: TableSchema,
    entities: list[Entity],
    llm: LLMProtocol,
) -> CriticDecision:
    """Call the LLM critic to audit a semantically valid MappingProposal.

    The critic checks whether the proposed business concept is logically
    consistent with the table's column structure and entity definitions.
    An ``approved=False`` decision triggers a Reflection Prompt retry in the
    mapping node.

    Args:
        proposal: A structurally valid (Pydantic-passed) ``MappingProposal``.
        table: The original DDL table.
        entities: All canonical entities available for mapping.
        llm: Reasoning LLM (temperature=0.0 — adversarial, deterministic).

    Returns:
        ``CriticDecision`` with ``approved`` flag and optional critique.
        On any failure, returns ``approved=True`` to avoid infinite retry loops
        (the pipeline logs the failure as a warning).
    """
    # Sort by name length so high-level concept names (short, e.g. "Customer")
    # appear before attribute-level entries (long, e.g. "unique numeric identifier
    # for the customer") in the critic context window. Take top 20 for coverage.
    safe_entities = entities or []
    sorted_entities = sorted(safe_entities, key=lambda e: len(getattr(e, "name", "")))[:20]
    entities_json = json.dumps(
        [
            {"name": e.name, "definition": e.definition, "synonyms": e.synonyms}
            for e in sorted_entities
        ]
    )
    user_prompt = CRITIC_USER.format(
        proposal_json=proposal.model_dump_json(indent=2),
        table_ddl=table.ddl_source,
        entities_json=entities_json,
    )

    logger.info(
        "Critic call start for '%s' (entities=%d, prompt_chars=%d)",
        table.table_name,
        len(sorted_entities),
        len(user_prompt),
    )
    start = time.perf_counter()
    try:
        messages = [
            SystemMessage(content=CRITIC_SYSTEM),
            HumanMessage(content=user_prompt),
        ]
        with ThreadPoolExecutor(max_workers=1) as executor:
            future = executor.submit(llm.invoke, messages)
            response = future.result(timeout=_CRITIC_TIMEOUT_SECONDS)
        raw_json: str = response.content.strip()
    except FutureTimeoutError:
        elapsed = time.perf_counter() - start
        logger.warning(
            "Critic LLM timeout for table '%s' after %.1fs — approving by default.",
            table.table_name,
            elapsed,
        )
        return CriticDecision(approved=True)
    except Exception as exc:
        elapsed = time.perf_counter() - start
        logger.warning(
            "Critic LLM call failed for table '%s' after %.1fs: %s — approving by default.",
            table.table_name,
            elapsed,
            exc,
        )
        return CriticDecision(approved=True)
    elapsed = time.perf_counter() - start
    logger.info("Critic call end for '%s' in %.1fs", table.table_name, elapsed)

    try:
        data = json.loads(raw_json)
        decision = CriticDecision(**data)
    except (json.JSONDecodeError, ValidationError) as exc:
        logger.warning("Critic response parse error: %s — approving by default.", exc)
        return CriticDecision(approved=True)

    logger.info(
        "Critic for '%s' → approved=%s, critique=%r",
        table.table_name,
        decision.approved,
        decision.critique,
    )
    return decision


# ── Reflection Prompt Builder ─────────────────────────────────────────────────


def build_reflection_prompt(
    role: str,
    output_format: str,
    error: str,
    original_input: str,
) -> str:
    """Format the universal REFLECTION_TEMPLATE for an LLM retry call.

    Args:
        role: LLM persona (e.g., "data governance expert").
        output_format: Expected output description (e.g., "JSON mapping proposal").
        error: The exact error or critique to correct.
        original_input: The original data the LLM must re-process.

    Returns:
        Formatted reflection prompt string, ready to pass as a ``HumanMessage``.
    """
    return REFLECTION_TEMPLATE.format(
        role=role,
        output_format=output_format,
        error_or_critique=error,
        original_input=original_input,
    )
