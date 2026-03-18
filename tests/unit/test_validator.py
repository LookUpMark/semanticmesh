"""Unit tests for src/mapping/validator.py — UT-08"""

from __future__ import annotations

import json
from unittest.mock import MagicMock

from src.mapping.validator import (
    build_reflection_prompt,
    critic_review,
    validate_schema,
)
from src.models.schemas import ColumnSchema, Entity, MappingProposal, TableSchema

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
        name=name,
        definition="A person who buys things.",
        synonyms=[],
        provenance_text="x",
        source_doc="test.pdf",
    )


def _make_critic_llm(approved: bool, critique: str | None = None) -> MagicMock:
    llm = MagicMock()
    resp = MagicMock()
    resp.content = json.dumps(
        {
            "approved": approved,
            "critique": critique,
            "suggested_correction": None,
        }
    )
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

    def test_limits_entities_to_20(self) -> None:
        table = _make_table()
        entities = [_make_entity(f"Entity{i}") for i in range(30)]
        llm = _make_critic_llm(approved=True)
        proposal = MappingProposal(**_valid_dict())

        critic_review(proposal, table, entities, llm)

        # Check that at most 20 entities were passed to the LLM
        call_args = llm.invoke.call_args
        user_message = call_args[0][0][1]  # Second message is HumanMessage
        content = user_message.content
        # Count how many "name" fields appear in the entities_json
        assert content.count('"name"') <= 20  # At most 20 entities serialized


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

    def test_contains_error_placeholder(self) -> None:
        prompt = build_reflection_prompt(
            role="expert",
            output_format="JSON",
            error="Invalid confidence value",
            original_input="input data",
        )
        # The template should include the error
        assert "Invalid confidence value" in prompt

    def test_contains_original_input(self) -> None:
        prompt = build_reflection_prompt(
            role="expert",
            output_format="JSON",
            error="error",
            original_input='{"table": "TB_CST"}',
        )
        assert '{"table": "TB_CST"}' in prompt
