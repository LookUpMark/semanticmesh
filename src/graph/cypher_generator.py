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
                result.append(cypher[i:])
                break
        else:
            result.append(cypher[i])
            i += 1
    return "".join(result)


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
    logger.info(
        "Cypher generated for '%s' (%d chars).",
        table.table_name,
        len(cypher),
    )
    return cypher
