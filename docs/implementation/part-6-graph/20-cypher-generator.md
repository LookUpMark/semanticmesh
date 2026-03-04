# Part 6 — `src/graph/cypher_generator.py`

## 1. Purpose & Context

**Epic:** EP-09 Cypher Generation & Healing  
**US-09-01** — Cypher Generation from Validated Mappings

`cypher_generator` converts an approved `MappingProposal` into a parameterised Neo4j `MERGE` statement. The LLM is prompted with:

- A fixed system persona (MERGE-only expert).
- Structured few-shot examples (`CypherExample` list).
- The validated mapping, table, and entity details.

Output is a **raw Cypher string** — no markdown fences, no explanation. The caller (`cypher_healer`) validates it before execution.

---

## 2. Prerequisites

- `src/models/schemas.py` — `MappingProposal`, `TableSchema`, `Entity`, `CypherExample` (step 5)
- `src/prompts/templates.py` — `CYPHER_SYSTEM`, `CYPHER_USER` (step 7)
- `src/prompts/few_shot.py` — `load_cypher_examples`, `format_cypher_examples` (step 8)
- `src/config/logging.py` — `get_logger`

---

## 3. Public API

| Symbol | Signature | Description |
|---|---|---|
| `generate_cypher` | `(mapping: MappingProposal, table: TableSchema, entity: Entity, few_shot: list[CypherExample], llm: LLMProtocol) -> str` | Call LLM, return raw Cypher string |
| `strip_cypher_fence` | `(raw: str) -> str` | Remove any accidental markdown fences |

---

## 4. Full Implementation

```python
"""Cypher generation from validated MappingProposal objects.

EP-09 / US-09-01: Prompts the reasoning LLM to generate MERGE-based
Neo4j Cypher statements from a validated mapping.
"""

from __future__ import annotations

import logging
import re

from langchain_core.messages import HumanMessage, SystemMessage

from src.config.llm_client import LLMProtocol

from src.config.logging import get_logger
from src.models.schemas import CypherExample, Entity, MappingProposal, TableSchema
from src.prompts.templates import CYPHER_SYSTEM, CYPHER_USER

logger: logging.Logger = get_logger(__name__)

# Matches optional triple-backtick markdown fences (with or without language tag)
_FENCE_RE = re.compile(r"^```[a-zA-Z]*\n?|```$", re.MULTILINE)


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
        parts.append(
            f"Example {i}:\n"
            f"DDL:\n{ex.ddl_snippet}\n\n"
            f"Cypher:\n{ex.cypher}"
        )
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
        mapping:  The validated ``MappingProposal`` for this table.
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
    user_prompt = CYPHER_USER.format(
        few_shot_examples=few_shot_block,
        table_ddl=table.ddl_source,
        concept_name=entity.name,
        concept_definition=entity.definition,
        concept_synonyms=", ".join(entity.synonyms) if entity.synonyms else "none",
        mapped_concept=mapping.mapped_concept,
        confidence=mapping.confidence,
        table_name=table.table_name,
        column_names=", ".join(c.name for c in table.columns),
        column_types=", ".join(c.data_type for c in table.columns),
        ddl_source=table.ddl_source,
        provenance_text=entity.provenance_text or "",
        source_doc=entity.source_doc or "",
    )

    logger.debug("Generating Cypher for table '%s' → '%s'.", table.table_name, mapping.mapped_concept)
    response = llm.invoke(
        [
            SystemMessage(content=CYPHER_SYSTEM),
            HumanMessage(content=user_prompt),
        ]
    )
    raw: str = response.content
    cypher = strip_cypher_fence(raw)
    logger.info(
        "Cypher generated for '%s' (%d chars).",
        table.table_name, len(cypher),
    )
    return cypher
```

---

## 5. Tests

```python
"""Unit tests for src/graph/cypher_generator.py — UT-16"""

from __future__ import annotations

from unittest.mock import MagicMock

import pytest

from src.graph.cypher_generator import generate_cypher, strip_cypher_fence
from src.models.schemas import ColumnSchema, CypherExample, Entity, MappingProposal, TableSchema


# ── Helpers ────────────────────────────────────────────────────────────────────

def _make_mapping(concept: str = "Customer") -> MappingProposal:
    return MappingProposal(
        table_name="TB_CST",
        mapped_concept=concept,
        confidence=0.97,
        reasoning="Primary key is CUST_ID.",
        alternative_concepts=[],
    )

def _make_table() -> TableSchema:
    return TableSchema(
        table_name="TB_CST",
        columns=[
            ColumnSchema(name="CUST_ID", data_type="INT", is_primary_key=True),
            ColumnSchema(name="CUST_NAME", data_type="VARCHAR", is_primary_key=False),
        ],
        ddl_source="CREATE TABLE TB_CST (CUST_ID INT PRIMARY KEY, CUST_NAME VARCHAR(100));",
    )

def _make_entity() -> Entity:
    return Entity(
        name="Customer", definition="A person who buys products.",
        synonyms=["Client"], provenance_text="Sales docs.", source_doc="sales.pdf",
    )

def _make_example() -> CypherExample:
    return CypherExample(
        ddl_snippet="CREATE TABLE ORDERS (ORD_ID INT PRIMARY KEY);",
        cypher="MERGE (bc:BusinessConcept {name: $concept_name})\nMERGE (pt:PhysicalTable {table_name: $table_name})\nMERGE (bc)-[:MAPPED_TO]->(pt)",
    )

def _make_llm(output: str) -> MagicMock:
    llm = MagicMock()
    resp = MagicMock()
    resp.content = output
    llm.invoke.return_value = resp
    return llm


# ── strip_cypher_fence ─────────────────────────────────────────────────────────

class TestStripCypherFence:
    def test_strips_cypher_fence(self) -> None:
        raw = "```cypher\nMERGE (n:X)\n```"
        assert strip_cypher_fence(raw) == "MERGE (n:X)"

    def test_strips_plain_fence(self) -> None:
        raw = "```\nMERGE (n:X)\n```"
        assert strip_cypher_fence(raw) == "MERGE (n:X)"

    def test_no_fence_unchanged(self) -> None:
        raw = "MERGE (n:Customer {name: $name})"
        assert strip_cypher_fence(raw) == raw

    def test_strips_trailing_whitespace(self) -> None:
        raw = "  MERGE (n:X)  "
        result = strip_cypher_fence(raw)
        assert result == "MERGE (n:X)"


# ── generate_cypher ────────────────────────────────────────────────────────────

class TestGenerateCypher:
    def test_returns_string(self) -> None:
        llm = _make_llm("MERGE (bc:BusinessConcept {name: $concept_name})")
        result = generate_cypher(_make_mapping(), _make_table(), _make_entity(), [], llm)
        assert isinstance(result, str)
        assert len(result) > 0

    def test_strips_fences_in_output(self) -> None:
        llm = _make_llm("```cypher\nMERGE (n:X)\n```")
        result = generate_cypher(_make_mapping(), _make_table(), _make_entity(), [], llm)
        assert "```" not in result
        assert "MERGE" in result

    def test_few_shot_injected_in_prompt(self) -> None:
        llm = _make_llm("MERGE (n:X)")
        examples = [_make_example()]
        generate_cypher(_make_mapping(), _make_table(), _make_entity(), examples, llm)
        call_args = llm.invoke.call_args[0][0]
        human_content = call_args[1].content
        assert "ORDERS" in human_content  # DDL snippet from example

    def test_llm_error_propagates(self) -> None:
        llm = MagicMock()
        llm.invoke.side_effect = RuntimeError("timeout")
        with pytest.raises(RuntimeError, match="timeout"):
            generate_cypher(_make_mapping(), _make_table(), _make_entity(), [], llm)
```

---

## 6. Smoke Test

```bash
python -c "
from src.graph.cypher_generator import strip_cypher_fence

raw = '\`\`\`cypher\nMERGE (n:BusinessConcept {name: \$name})\n\`\`\`'
print('Cleaned:', strip_cypher_fence(raw))
print('strip_cypher_fence OK')
"
```
