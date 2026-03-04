# Part 2 — `src/prompts/few_shot.py`

## 1. Purpose & Context

**Epic:** EP-06 data models  
**US:** REQUIREMENTS.md §8 — Few-shot example injection

Loads, validates, and formats the seed few-shot examples from `src/data/` into string blocks ready to be injected into `MAPPING_USER` and `CYPHER_USER` at runtime. Intentionally thin: all business logic (which examples to pick, cosine similarity selection) lives in the calling node.

---

## 2. Prerequisites

- `src/models/schemas.py` (`CypherExample`, `MappingExample`) — step 3
- `src/data/few_shot_cypher.json` — populated in fixtures
- `src/data/few_shot_mapping.json` — populated in fixtures

---

## 3. Public API

| Function | Signature | Returns |
|---|---|---|
| `load_cypher_examples` | `(n: int = 5) -> list[CypherExample]` | First `n` Cypher examples from `few_shot_cypher.json`, validated as `CypherExample` |
| `load_mapping_examples` | `(n: int = 3) -> list[MappingExample]` | First `n` mapping examples from `few_shot_mapping.json`, validated as `MappingExample` |
| `format_cypher_examples` | `(examples: list[CypherExample]) -> str` | Plain-text block ready to inject into `{few_shot_examples}` in `CYPHER_USER` |
| `format_mapping_examples` | `(examples: list[MappingExample]) -> str` | Plain-text block ready to inject into `{few_shot_examples}` in `MAPPING_USER` |

---

## 4. Full Implementation

```python
"""Few-shot example loaders and formatters.

Loads validated Pydantic objects from src/data/ JSON files and
exposes string formatters for prompt injection.
"""

from __future__ import annotations

import json
from pathlib import Path

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
    raw: list[dict] = json.loads(_CYPHER_EXAMPLES_PATH.read_text(encoding="utf-8"))
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
    raw: list[dict] = json.loads(_MAPPING_EXAMPLES_PATH.read_text(encoding="utf-8"))
    return [MappingExample(**r) for r in raw[:n]]


def format_cypher_examples(examples: list[CypherExample]) -> str:
    """Format a list of CypherExample objects into a numbered plain-text block.

    The output is designed to replace the ``{few_shot_examples}`` placeholder
    in ``CYPHER_USER``.

    Example output (one example):
        Example 1: Customer master table mapping
        DDL: CREATE TABLE CUSTOMER_MASTER ...
        Concept: Customer - An individual or organisation ...
        Cypher:
        MERGE (bc:BusinessConcept {name: $concept_name}) ...
    """
    lines: list[str] = []
    for i, ex in enumerate(examples, start=1):
        lines.append(f"Example {i}: {ex.description}")
        lines.append(f"DDL: {ex.ddl_snippet}")
        lines.append(f"Concept: {ex.concept_name} - {ex.concept_definition}")
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
```

> **Note on `MappingExample.cypher`:** The `MappingExample` schema reuses the `cypher` field to store the mapping reasoning text (see `05-schemas.md`). This is intentional — it keeps the schema generic and avoids adding a `reasoning` synonym field.

---

## 5. Tests

```python
"""Unit tests for src/prompts/few_shot.py"""

from __future__ import annotations

import pytest

from src.models.schemas import CypherExample, MappingExample
from src.prompts.few_shot import (
    format_cypher_examples,
    format_mapping_examples,
    load_cypher_examples,
    load_mapping_examples,
)


class TestLoadCypherExamples:
    def test_loads_default_five(self) -> None:
        examples = load_cypher_examples()
        # The seed file has 5 examples; null-concept ones are filtered out
        assert len(examples) >= 1
        assert all(isinstance(e, CypherExample) for e in examples)

    def test_respects_n_limit(self) -> None:
        examples = load_cypher_examples(n=2)
        assert len(examples) <= 2

    def test_no_null_concept(self) -> None:
        examples = load_cypher_examples(n=10)
        for ex in examples:
            assert ex.concept_name is not None

    def test_returns_validated_objects(self) -> None:
        examples = load_cypher_examples(n=1)
        assert examples[0].ddl_snippet != ""
        assert examples[0].cypher.startswith("MERGE")

    def test_n_zero_returns_empty(self) -> None:
        examples = load_cypher_examples(n=0)
        assert examples == []


class TestLoadMappingExamples:
    def test_loads_default_three(self) -> None:
        examples = load_mapping_examples()
        assert len(examples) == 3
        assert all(isinstance(e, MappingExample) for e in examples)

    def test_respects_n_limit(self) -> None:
        examples = load_mapping_examples(n=1)
        assert len(examples) == 1

    def test_first_example_is_customer(self) -> None:
        examples = load_mapping_examples(n=1)
        assert examples[0].concept_name == "Customer"


class TestFormatCypherExamples:
    def test_single_example_contains_required_fields(self) -> None:
        ex = CypherExample(
            description="Test example",
            ddl_snippet="CREATE TABLE T (ID INT PRIMARY KEY)",
            concept_name="TestConcept",
            concept_definition="A test concept.",
            cypher="MERGE (bc:BusinessConcept {name: $concept_name})",
        )
        result = format_cypher_examples([ex])
        assert "Example 1: Test example" in result
        assert "TestConcept" in result
        assert "MERGE" in result

    def test_multiple_examples_are_numbered(self) -> None:
        examples = load_cypher_examples(n=3)
        result = format_cypher_examples(examples)
        assert "Example 1:" in result
        assert "Example 2:" in result
        assert "Example 3:" in result

    def test_empty_returns_empty_string(self) -> None:
        assert format_cypher_examples([]) == ""


class TestFormatMappingExamples:
    def test_contains_table_and_concept(self) -> None:
        examples = load_mapping_examples(n=1)
        result = format_mapping_examples(examples)
        assert "Example 1:" in result
        assert "Customer" in result

    def test_multiple_examples_numbered(self) -> None:
        examples = load_mapping_examples(n=3)
        result = format_mapping_examples(examples)
        assert "Example 3:" in result
```

---

## 6. Data File Reference

The seed few-shot examples live at:

- `src/data/few_shot_cypher.json` — schema: `{id, description, ddl_snippet, concept_name, concept_definition, mapping_confidence, cypher, validated_by, tags}`
- `src/data/few_shot_mapping.json` — schema: `{id, table_ddl, concept_name, confidence, reasoning}`

Both are pre-populated with gold-standard fixtures. New examples can be appended after HITL validation.

---

## 7. Smoke Test

```bash
python -c "
from src.prompts.few_shot import load_cypher_examples, format_cypher_examples
exs = load_cypher_examples(n=3)
print(f'Loaded {len(exs)} Cypher examples')
block = format_cypher_examples(exs)
print(block[:400])
"
```
