# Part 5 — `src/mapping/validator.py`

## 1. Purpose & Context

**Epic:** EP-07 Mapping Validation & Actor-Critic  
**US-07-01** — Pydantic Schema Validation, **US-07-02** — LLM Actor-Critic Semantic Review

Two-layer validation for every `MappingProposal`:

1. **Pydantic layer** — catches structural errors (wrong types, missing fields, out-of-range confidence)
2. **LLM Critic layer** — catches semantic errors (syntactically valid but logically wrong mappings)

Failed validations produce a Reflection Prompt error string that is injected back into the mapper node for self-correction.

---

## 2. Prerequisites

- `src/models/schemas.py` — `MappingProposal`, `CriticDecision`, `TableSchema`, `Entity` (step 3)
- `src/prompts/templates.py` — `CRITIC_SYSTEM`, `CRITIC_USER`, `REFLECTION_TEMPLATE` (step 7)
- `src/config/logging.py` — `get_logger`

---

## 3. Public API

| Symbol | Signature | Description |
|---|---|---|
| `validate_schema` | `(proposal_dict: dict) -> tuple[MappingProposal \| None, str \| None]` | Pydantic validation; returns (obj, None) or (None, error_str) |
| `critic_review` | `(proposal: MappingProposal, table: TableSchema, entities: list[Entity], llm: LLMProtocol) -> CriticDecision` | LLM critic verdict |
| `build_reflection_prompt` | `(role: str, output_format: str, error: str, original_input: str) -> str` | Formats `REFLECTION_TEMPLATE` for a retry call |

---

## 4. Full Implementation

```python
"""Mapping validation — Pydantic schema check + LLM Actor-Critic.

EP-07: Two-layer validation to catch both structural and semantic errors
in MappingProposal objects before they proceed to Cypher generation.
"""

from __future__ import annotations

import json
import logging

from langchain_core.messages import HumanMessage, SystemMessage

from src.config.llm_client import LLMProtocol
from pydantic import ValidationError

from src.config.logging import get_logger
from src.models.schemas import CriticDecision, Entity, MappingProposal, TableSchema
from src.prompts.templates import CRITIC_SYSTEM, CRITIC_USER, REFLECTION_TEMPLATE

logger: logging.Logger = get_logger(__name__)


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
    entities_json = json.dumps(
        [{"name": e.name, "definition": e.definition, "synonyms": e.synonyms} for e in entities[:10]]
    )
    user_prompt = CRITIC_USER.format(
        proposal_json=proposal.model_dump_json(indent=2),
        table_ddl=table.ddl_source,
        entities_json=entities_json,
    )

    try:
        response = llm.invoke(
            [
                SystemMessage(content=CRITIC_SYSTEM),
                HumanMessage(content=user_prompt),
            ]
        )
        raw_json: str = response.content.strip()
    except Exception as exc:
        logger.warning(
            "Critic LLM call failed for table '%s': %s — approving by default.",
            table.table_name, exc,
        )
        return CriticDecision(approved=True)

    try:
        data = json.loads(raw_json)
        decision = CriticDecision(**data)
    except (json.JSONDecodeError, ValidationError) as exc:
        logger.warning("Critic response parse error: %s — approving by default.", exc)
        return CriticDecision(approved=True)

    logger.info(
        "Critic for '%s' → approved=%s, critique=%r",
        table.table_name, decision.approved, decision.critique,
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
```

---

## 5. Tests

```python
"""Unit tests for src/mapping/validator.py — UT-08"""

from __future__ import annotations

import json
from unittest.mock import MagicMock

import pytest

from src.mapping.validator import (
    build_reflection_prompt,
    critic_review,
    validate_schema,
)
from src.models.schemas import ColumnSchema, CriticDecision, Entity, MappingProposal, TableSchema


# ── Fixtures ───────────────────────────────────────────────────────────────────

def _valid_dict(concept: str = "Customer", confidence: float = 0.9) -> dict:
    return {
        "table_name": "TB_CST",
        "mapped_concept": concept,
        "confidence": confidence,
        "reasoning": "Test reasoning.",
        "alternative_concepts": [],
    }


def _make_table() -> TableSchema:
    return TableSchema(
        table_name="TB_CST",
        columns=[ColumnSchema(name="CUST_ID", data_type="INT", is_primary_key=True)],
        ddl_source="CREATE TABLE TB_CST (CUST_ID INT PRIMARY KEY);",
    )


def _make_entity(name: str = "Customer") -> Entity:
    return Entity(
        name=name, definition="A person who buys things.",
        synonyms=[], provenance_text="x", source_doc="test.pdf",
    )


def _make_critic_llm(approved: bool, critique: str | None = None) -> MagicMock:
    llm = MagicMock()
    resp = MagicMock()
    resp.content = json.dumps({
        "approved": approved,
        "critique": critique,
        "suggested_correction": None,
    })
    llm.invoke.return_value = resp
    return llm


# ── validate_schema ───────────────────────────────────────────────────────────

class TestValidateSchema:
    def test_valid_proposal_returns_object(self) -> None:
        proposal, error = validate_schema(_valid_dict())
        assert proposal is not None
        assert error is None
        assert isinstance(proposal, MappingProposal)

    def test_missing_required_field_returns_error(self) -> None:
        bad = {"mapped_concept": "Customer"}  # missing table_name, confidence, reasoning
        proposal, error = validate_schema(bad)
        assert proposal is None
        assert error is not None
        assert "table_name" in error.lower() or "confidence" in error.lower()

    def test_confidence_out_of_range_returns_error(self) -> None:
        bad = _valid_dict(confidence=1.5)
        proposal, error = validate_schema(bad)
        assert proposal is None
        assert error is not None

    def test_null_concept_allowed(self) -> None:
        d = _valid_dict()
        d["mapped_concept"] = None
        d["confidence"] = 0.0
        proposal, error = validate_schema(d)
        assert proposal is not None
        assert proposal.mapped_concept is None


# ── critic_review ─────────────────────────────────────────────────────────────

class TestCriticReview:
    def test_approved_decision(self) -> None:
        table = _make_table()
        entities = [_make_entity()]
        llm = _make_critic_llm(approved=True)
        proposal = MappingProposal(**_valid_dict())
        decision = critic_review(proposal, table, entities, llm)
        assert decision.approved is True

    def test_rejected_with_critique(self) -> None:
        table = _make_table()
        entities = [_make_entity()]
        critic_msg = "TB_CST has product columns, not customer columns."
        llm = _make_critic_llm(approved=False, critique=critic_msg)
        proposal = MappingProposal(**_valid_dict())
        decision = critic_review(proposal, table, entities, llm)
        assert decision.approved is False
        assert decision.critique == critic_msg

    def test_llm_error_defaults_to_approved(self) -> None:
        table = _make_table()
        llm = MagicMock()
        llm.invoke.side_effect = RuntimeError("timeout")
        proposal = MappingProposal(**_valid_dict())
        decision = critic_review(proposal, table, [], llm)
        assert decision.approved is True  # conservative default

    def test_bad_json_defaults_to_approved(self) -> None:
        table = _make_table()
        llm = MagicMock()
        resp = MagicMock()
        resp.content = "not json at all"
        llm.invoke.return_value = resp
        proposal = MappingProposal(**_valid_dict())
        decision = critic_review(proposal, table, [], llm)
        assert decision.approved is True


# ── build_reflection_prompt ───────────────────────────────────────────────────

class TestBuildReflectionPrompt:
    def test_all_placeholders_filled(self) -> None:
        prompt = build_reflection_prompt(
            role="data governance expert",
            output_format="JSON mapping proposal",
            error="confidence must be ≤ 1.0",
            original_input='{"table_name": "T"}',
        )
        assert "data governance expert" in prompt
        assert "JSON mapping proposal" in prompt
        assert "confidence must be" in prompt
        assert '{"table_name": "T"}' in prompt

    def test_returns_non_empty_string(self) -> None:
        prompt = build_reflection_prompt("role", "format", "error", "input")
        assert len(prompt) > 100
```

---

## 6. Smoke Test

```bash
python -c "
from src.mapping.validator import validate_schema, build_reflection_prompt

proposal, err = validate_schema({
    'table_name': 'CUSTOMER_MASTER',
    'mapped_concept': 'Customer',
    'confidence': 0.97,
    'reasoning': 'Primary key is CUST_ID.',
    'alternative_concepts': [],
})
print('Valid proposal:', proposal.mapped_concept if proposal else err)

ref = build_reflection_prompt(
    role='data governance expert',
    output_format='JSON mapping proposal',
    error='confidence must be <= 1.0, got 1.5',
    original_input='{\"table_name\": \"T\", \"confidence\": 1.5}',
)
print('Reflection prompt length:', len(ref), 'chars')
"
```
