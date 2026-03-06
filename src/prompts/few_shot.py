"""Few-shot example loaders and formatters.

Loads validated Pydantic objects from src/data/ JSON files and
exposes string formatters for prompt injection.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from src.models.schemas import CypherExample, MappingExample

# Locate data files relative to this module's package root
_DATA_DIR = Path(__file__).parent.parent / "data"
_CYPHER_EXAMPLES_PATH = _DATA_DIR / "few_shot_cypher.json"
_MAPPING_EXAMPLES_PATH = _DATA_DIR / "few_shot_mapping.json"


def load_cypher_examples(n: int = 5) -> list[CypherExample]:
    """Load the first *n* Cypher few-shot examples from the JSON seed file.

    Args:
        n: Maximum number of examples to load.  Pass a smaller value during
           prompt budget-constrained calls.

    Returns:
        List of validated ``CypherExample`` objects.

    Raises:
        FileNotFoundError: If ``few_shot_cypher.json`` does not exist.
        pydantic.ValidationError: If a record fails schema validation.
    """
    raw: list[dict[str, Any]] = json.loads(_CYPHER_EXAMPLES_PATH.read_text(encoding="utf-8"))
    # Filter out null-concept entries (concept_name=None) — they yield no Cypher
    valid_raw = [r for r in raw if r.get("concept_name") is not None]
    return [CypherExample(**r) for r in valid_raw[:n]]


def load_mapping_examples(n: int = 3) -> list[MappingExample]:
    """Load the first *n* mapping few-shot examples from the JSON seed file.

    Args:
        n: Maximum number of examples to load.

    Returns:
        List of validated ``MappingExample`` objects.

    Raises:
        FileNotFoundError: If ``few_shot_mapping.json`` does not exist.
        pydantic.ValidationError: If a record fails schema validation.
    """
    raw: list[dict[str, Any]] = json.loads(_MAPPING_EXAMPLES_PATH.read_text(encoding="utf-8"))
    # Map JSON fields to Pydantic model fields
    # JSON: table_ddl, concept_name, reasoning
    # Model: ddl_snippet, concept_name, concept_definition, cypher
    mapped_examples = []
    for r in raw[:n]:
        mapped_examples.append(
            MappingExample(
                ddl_snippet=r["table_ddl"],
                concept_name=r["concept_name"],
                concept_definition="",  # Not stored in JSON, using empty string
                cypher=r["reasoning"],  # 'cypher' field stores reasoning in MappingExample
            )
        )
    return mapped_examples


def format_cypher_examples(examples: list[CypherExample]) -> str:
    """Format a list of CypherExample objects into a numbered plain-text block.

    The output is designed to replace the ``{few_shot_examples}`` placeholder
    in ``CYPHER_USER``.

    Example output (one example):
        Example 1: Customer master table mapping
        DDL: CREATE TABLE CUSTOMER_MASTER ...
        Concept: Customer
        Cypher:
        MERGE (bc:BusinessConcept {name: $concept_name}) ...
    """
    lines: list[str] = []
    for i, ex in enumerate(examples, start=1):
        lines.append(f"Example {i}: {ex.description}")
        lines.append(f"DDL: {ex.ddl_snippet}")
        lines.append(f"Concept: {ex.concept_name}")
        lines.append("Cypher:")
        lines.append(ex.cypher)
        lines.append("")  # blank line between examples
    return "\n".join(lines).rstrip()


def format_mapping_examples(examples: list[MappingExample]) -> str:
    """Format a list of MappingExample objects into a numbered plain-text block.

    The output is designed to replace the ``{few_shot_examples}`` placeholder
    in ``MAPPING_USER``.

    Example output (one example):
        Example 1:
        Table DDL: CUSTOMER_MASTER: CUST_ID (INT, PK) ...
        Concept: Customer
        Reasoning: CUSTOMER_MASTER stores individual customer identity data ...
    """
    lines: list[str] = []
    for i, ex in enumerate(examples, start=1):
        lines.append(f"Example {i}:")
        lines.append(f"Table DDL: {ex.ddl_snippet}")
        lines.append(f"Concept: {ex.concept_name}")
        lines.append(f"Reasoning: {ex.cypher}")  # 'cypher' field stores reasoning in MappingExample
        lines.append("")
    return "\n".join(lines).rstrip()
