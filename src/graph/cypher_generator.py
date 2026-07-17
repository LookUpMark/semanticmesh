"""Cypher generation from validated MappingProposal objects.

EP-09 / US-09-01: Prompts the reasoning LLM to generate MERGE-based
Neo4j Cypher statements from a validated mapping.
"""

from __future__ import annotations

import logging
import re
from typing import TYPE_CHECKING

from langchain_core.messages import HumanMessage, SystemMessage

from src.config.logging import get_logger
from src.models.schemas import CypherExample, Entity, MappingProposal, TableSchema
from src.prompts.templates import CYPHER_SYSTEM, CYPHER_USER
from src.utils.json_utils import extract_text_content

if TYPE_CHECKING:
    from src.config.llm_client import LLMProtocol

logger: logging.Logger = get_logger(__name__)

_FENCE_RE = re.compile(r"^```[a-zA-Z]*\n?|```$", re.MULTILINE)


def _fix_apostrophes_in_cypher(cypher: str) -> str:
    """Convert SQL-style ``''`` apostrophe escaping to double-quoted strings.

    Neo4j Cypher does not support ``''`` as an escape for apostrophes inside
    single-quoted string literals (unlike SQL).  LLMs often produce this error
    when synonyms or descriptions contain possessive forms (e.g. "Customer's").

    Scans the Cypher character-by-character. For each single-quoted literal
    that contains one or more ``''`` sequences, rewrites it as a double-quoted
    string with ``''`` normalised to ``'``.  Literals without ``''`` are left
    untouched.

    Example::

        'Customer''s full name'  →  "Customer's full name"

    Args:
        cypher: Raw Cypher string (fences already stripped).

    Returns:
        Cypher string with problematic single-quoted literals rewritten.
    """
    result: list[str] = []
    i = 0
    n = len(cypher)
    while i < n:
        if cypher[i] == "'":
            j = i + 1
            has_double_apostrophe = False
            while j < n:
                if cypher[j] == "'":
                    if j + 1 < n and cypher[j + 1] == "'":
                        has_double_apostrophe = True
                        j += 2
                    else:
                        j += 1
                        break
                else:
                    j += 1
            if has_double_apostrophe and j < n:
                content = cypher[i + 1 : j - 1]
                content = content.replace("''", "'")
                content = content.replace('"', '\\"')
                result.append(f'"{content}"')
                i = j
            elif j < n:
                result.append(cypher[i:j])
                i = j
            else:
                # Unmatched quote — append rest of string unchanged
                # AUDIT-059: log warning about unmatched apostrophe in Cypher
                logger.warning(
                    "Unmatched single quote in Cypher at position %d — "
                    "remaining text appended unchanged: %.60s...",
                    i,
                    cypher[i:],
                )
                result.append(cypher[i:])
                break
        else:
            result.append(cypher[i])
            i += 1
    return "".join(result)


def _detect_multi_statement(cypher: str) -> bool:
    """Return True if ``cypher`` has >= 2 ``;``-separated statements at top level.

    A multi-statement emission (e.g. ``MERGE ...; MERGE ...;``) is rejected by
    the AUDIT-069 execution guard and forces a deterministic-builder fallback,
    which is the dominant source of wasted LLM-Cypher work (~38x per run before
    the prompt was strengthened). This quote-aware scan detects such emissions
    at generation time so they are observable *before* the downstream
    execute-time crash, instead of only surfacing in the fallback warning.

    Semicolons inside single- or double-quoted string literals are not counted
    as statement separators. A trailing ``;`` with nothing after it is treated
    as a single statement.

    Args:
        cypher: Raw Cypher string (fences stripped, apostrophes fixed).

    Returns:
        True if two or more non-empty ``;``-separated statements are present.
    """
    if not cypher or not cypher.strip():
        return False
    in_single = False
    in_double = False
    non_empty_parts = 0
    start = 0
    i = 0
    n = len(cypher)
    while i < n:
        ch = cypher[i]
        if in_single:
            if ch == "'":
                # SQL-style '' escape (should not occur after
                # _fix_apostrophes_in_cypher, but kept for robustness).
                if i + 1 < n and cypher[i + 1] == "'":
                    i += 2
                    continue
                in_single = False
        elif in_double:
            if ch == "\\":
                i += 2  # skip the escaped character
                continue
            if ch == '"':
                in_double = False
        else:
            if ch == "'":
                in_single = True
            elif ch == '"':
                in_double = True
            elif ch == ";":
                if cypher[start:i].strip():
                    non_empty_parts += 1
                    if non_empty_parts >= 2:
                        return True
                start = i + 1
        i += 1
    # Trailing segment after the final ';' (if any).
    if cypher[start:].strip():
        non_empty_parts += 1
    return non_empty_parts >= 2


def strip_cypher_fence(raw: str) -> str:
    """Remove accidental markdown code fences from LLM-generated Cypher.

    Some models wrap output in ```cypher ... ``` despite instructions. This
    function strips those fences so the plain Cypher can be parsed.

    Args:
        raw: The raw string returned by the LLM.

    Returns:
        The cleaned Cypher string.
    """
    return _FENCE_RE.sub("", raw).strip()


def _format_few_shot(examples: list[CypherExample]) -> str:
    """Render ``CypherExample`` objects as numbered prompt blocks.

    Args:
        examples: Up to ``n`` validated few-shot pairs.

    Returns:
        A multi-line string ready to embed in the user prompt.
    """
    if not examples:
        return "(no examples provided)"
    parts: list[str] = []
    for i, ex in enumerate(examples, start=1):
        parts.append(f"Example {i}:\nDDL:\n{ex.ddl_snippet}\n\nCypher:\n{ex.cypher}")
    return "\n\n---\n\n".join(parts)


def generate_cypher(
    mapping: MappingProposal,
    table: TableSchema,
    entity: Entity,
    few_shot: list[CypherExample],
    llm: LLMProtocol,
) -> str:
    """Call the LLM to produce a MERGE-based Cypher statement for one mapping.

    The generated Cypher uses only parameterised ``MERGE`` statements so that
    repeated ingestion is idempotent.  If the LLM wraps output in markdown
    fences they are stripped automatically.

    Args:
        mapping: The validated ``MappingProposal`` for this table.
        table:    The original DDL ``TableSchema`` (supplies ``ddl_source``).
        entity:   The canonical ``Entity`` the table maps to.
        few_shot: Up to ``settings.few_shot_cypher_examples`` labelled examples.
        llm:      Reasoning LLM — temperature must be 0.0 for determinism.

    Returns:
        Raw Cypher string ready to pass to ``test_cypher``.

    Raises:
        RuntimeError: If the LLM call fails (caller should handle and retry).
    """
    few_shot_block = _format_few_shot(few_shot)
    safe_ddl = (table.ddl_source or "").replace("'", '"')
    safe_definition = (entity.definition or "").replace("'", '"')
    safe_provenance = (entity.provenance_text or "").replace("'", '"')
    user_prompt = CYPHER_USER.format(
        few_shot_examples=few_shot_block,
        table_ddl=safe_ddl,
        concept_name=entity.name,
        concept_definition=safe_definition,
        synonyms=", ".join(entity.synonyms) if entity.synonyms else "",
        provenance_text=safe_provenance,
        source_doc=entity.source_doc or "",
        mapping_confidence=mapping.confidence,
        validated_by="llm_judge",
    )

    logger.debug(
        "Generating Cypher for table '%s' → '%s'.", table.table_name, mapping.mapped_concept
    )
    try:
        response = llm.invoke(
            [
                SystemMessage(content=CYPHER_SYSTEM),
                HumanMessage(content=user_prompt),
            ]
        )
    except Exception as exc:
        raise RuntimeError(f"LLM call failed for table '{table.table_name}': {exc}") from exc
    raw: str = extract_text_content(response.content)
    cypher = _fix_apostrophes_in_cypher(strip_cypher_fence(raw))
    if _detect_multi_statement(cypher):
        logger.warning(
            "LLM emitted multi-statement Cypher for '%s' — rejected by the "
            "AUDIT-069 guard and will fall back to the deterministic builder. "
            "The prompt instructs a single statement; this emission means the "
            "LLM ignored that constraint.",
            table.table_name,
        )
    logger.info(
        "Cypher generated for '%s' (%d chars).",
        table.table_name,
        len(cypher),
    )
    return cypher
