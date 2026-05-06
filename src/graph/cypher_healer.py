"""Cypher healing — dry-run test via EXPLAIN + LLM self-correction loop.

EP-09 / US-09-02 and US-09-03:
  * test_cypher   — validate without executing (EXPLAIN prefix)
  * fix_cypher    — inject Neo4j error into Reflection Prompt
  * heal_cypher   — up to max_attempts test→fix iterations
"""

from __future__ import annotations

import logging
import re

import neo4j.exceptions
from langchain_core.messages import HumanMessage, SystemMessage
from neo4j import Driver

from src.config.llm_client import LLMProtocol
from src.config.logging import get_logger
from src.config.settings import get_settings
from src.graph.cypher_generator import _fix_apostrophes_in_cypher, strip_cypher_fence
from src.models.schemas import MappingProposal
from src.prompts.templates import CYPHER_FIX_USER, CYPHER_SYSTEM
from src.utils.json_utils import extract_text_content

logger: logging.Logger = get_logger(__name__)


def _deterministic_prefix_fix(cypher: str, error: str) -> str | None:
    """Apply cheap, deterministic fixes before spending an LLM call.

    Handles the most common Cypher errors that don't require semantic understanding:
    - Backtick-wrapped label/property names that Neo4j rejects (e.g. ``name``)
    - Double-escaped backslashes in string literals
    - Leading/trailing whitespace or stray semicolons

    Returns the fixed Cypher string, or None if no deterministic fix applies.
    """
    fixed = cypher.strip().rstrip(";")

    # Remove backticks around simple alphanumeric identifiers (LLM often copies
    # from few-shot examples that use backticks; Neo4j rejects them in some positions)
    candidate = re.sub(r"`([A-Za-z_][A-Za-z0-9_]*)`", r"\1", fixed)

    # Fix double-escaped backslashes inside string literals (\\\\ → \\)
    candidate = candidate.replace("\\\\", "\\")

    changed = candidate != cypher.strip().rstrip(";")
    if not changed:
        return None

    logger.debug("deterministic_prefix_fix: applied heuristic Cypher correction.")
    return candidate


def validate_cypher(cypher: str, driver: Driver) -> tuple[bool, str | None]:
    """Validate a Cypher statement without executing any writes.

    Uses Neo4j's ``EXPLAIN`` prefix which parses and plans the query but
    does not run it, so no data is written or read.

    Args:
        cypher: The generated Cypher string to validate.
        driver: An open ``neo4j.Driver`` instance.

    Returns:
        ``(True, None)`` if Neo4j accepts the query plan.
        ``(False, error_message)`` on ``CypherSyntaxError``, ``ClientError``,
        or any other driver exception. The ``error_message`` is injected into
        the Reflection Prompt verbatim.
    """
    # Safety: reject Cypher containing destructive or admin operations.
    _BLOCKED_KEYWORDS = (
        "DROP ",
        "DETACH DELETE",
        "DELETE ",
        "REMOVE ",
        "CALL dbms.",
        "CALL db.index.fulltext.drop",
        "CREATE USER",
        "ALTER USER",
        "DROP USER",
        "CREATE ROLE",
        "ALTER ROLE",
        "DROP ROLE",
        "GRANT ",
        "REVOKE ",
        "DENY ",
        "CREATE DATABASE",
        "DROP DATABASE",
        "LOAD CSV",
    )
    upper = cypher.upper()
    for kw in _BLOCKED_KEYWORDS:
        if kw in upper:
            msg = f"Cypher contains blocked keyword '{kw.strip()}' — rejecting."
            logger.warning(msg)
            return False, msg

    # Positive allowlist: first keyword must be a safe read/write operation
    _ALLOWED_FIRST_KEYWORDS = ("MERGE", "MATCH", "WITH", "UNWIND", "RETURN", "OPTIONAL", "CALL {")
    stripped = cypher.strip().upper()
    if not any(stripped.startswith(kw) for kw in _ALLOWED_FIRST_KEYWORDS):
        msg = "Cypher does not start with an allowed keyword — rejecting."
        logger.warning(msg)
        return False, msg

    explain_stmt = f"EXPLAIN {cypher}"
    try:
        with driver.session() as session:
            session.run(explain_stmt).consume()
        logger.debug("test_cypher: EXPLAIN passed.")
        return True, None
    except neo4j.exceptions.CypherSyntaxError as exc:
        logger.warning("Cypher syntax error: %s", exc)
        return False, str(exc)
    except neo4j.exceptions.ClientError as exc:
        logger.warning("Cypher client error: %s", exc)
        return False, str(exc)
    except Exception as exc:
        logger.warning("Cypher test unexpected error: %s", exc)
        return False, str(exc)


def fix_cypher(
    cypher: str,
    error: str,
    mapping: MappingProposal,
    llm: LLMProtocol,
) -> str:
    """Ask the LLM to correct a Cypher statement given the Neo4j error.

    Uses ``CYPHER_FIX_USER`` — a Reflection Prompt variant that embeds the
    broken Cypher and the exact Neo4j error message.

    Args:
        cypher:  The failing Cypher string.
        error:   The raw Neo4j error string from ``test_cypher``.
        mapping: The ``MappingProposal`` that produced the Cypher (for context).
        llm:     Reasoning LLM (temperature=0.0).

    Returns:
        A corrected Cypher string (markdown fences stripped).

    Raises:
        RuntimeError: If the LLM call itself fails.
    """
    user_prompt = CYPHER_FIX_USER.format(
        broken_cypher=cypher,
        error_message=error,
    )
    response = llm.invoke(
        [
            SystemMessage(content=CYPHER_SYSTEM),
            HumanMessage(content=user_prompt),
        ]
    )
    fixed = _fix_apostrophes_in_cypher(strip_cypher_fence(extract_text_content(response.content)))
    logger.debug("fix_cypher: LLM returned %d-char fix.", len(fixed))
    return fixed


def heal_cypher(
    cypher: str,
    mapping: MappingProposal,
    driver: Driver,
    llm: LLMProtocol,
    max_attempts: int | None = None,
) -> str | None:
    """Iteratively test and fix a Cypher statement until it passes or is exhausted.

    Attempt sequence:
    1. ``validate_cypher`` — if passes, return immediately.
    2. ``fix_cypher``  — inject error into LLM Reflection Prompt.
    3. Repeat up to ``max_attempts`` total test+fix cycles.

    On exhaustion after ``max_attempts`` failures the function returns ``None``
    and logs a CRITICAL warning.  The builder graph should then set
    ``cypher_failed=True`` for this mapping and continue with the next table.

    Args:
        cypher:       Initial Cypher string from ``generate_cypher``.
        mapping:      The ``MappingProposal`` that produced the Cypher.
        driver:       An open ``neo4j.Driver`` for ``test_cypher``.
        llm:          Reasoning LLM for ``fix_cypher``.
        max_attempts: Override ``settings.max_cypher_healing_attempts`` (default 3).

    Returns:
        A valid Cypher string, or ``None`` if all attempts failed.
    """
    settings = get_settings()
    limit: int = max_attempts if max_attempts is not None else settings.max_cypher_healing_attempts

    current: str = cypher
    for attempt in range(1, limit + 1):
        ok, error = validate_cypher(current, driver)
        if ok:
            logger.info(
                "Cypher healed for '%s' after %d attempt(s).",
                mapping.table_name,
                attempt,
            )
            return current

        logger.warning(
            "Cypher attempt %d/%d failed for '%s': %s",
            attempt,
            limit,
            mapping.table_name,
            error,
        )

        if attempt == limit:
            logger.warning(
                "Cypher healing exhausted for table '%s'. Falling back to deterministic builder.",
                mapping.table_name,
            )
            return None

        # Try a cheap deterministic fix first; only call LLM if that doesn't help
        det_fix = _deterministic_prefix_fix(current, error)
        if det_fix is not None:
            ok2, _ = validate_cypher(det_fix, driver)
            if ok2:
                logger.info(
                    "Cypher healed via deterministic fix for '%s' (no LLM call).",
                    mapping.table_name,
                )
                return det_fix
            current = det_fix  # use as starting point for LLM repair

        try:
            current = fix_cypher(current, error, mapping, llm)
        except Exception as exc:
            logger.error("fix_cypher LLM call failed: %s — aborting healing.", exc)
            return None

    # Should be unreachable; guard for static analysis
    return None
