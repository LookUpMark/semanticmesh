"""Unit tests for src/mapping/hitl.py — UT-09"""

from __future__ import annotations

from unittest.mock import patch

from src.mapping.hitl import (
    build_interrupt_payload,
    hitl_node,
    should_interrupt,
)
from src.models.schemas import Entity, MappingProposal
from src.models.state import BuilderState

# ── Helpers ────────────────────────────────────────────────────────────────────


def _proposal(
    concept: str = "Customer", confidence: float = 0.95, alternatives: list[str] | None = None
) -> MappingProposal:
    return MappingProposal(
        table_name="TB_CST",
        mapped_concept=concept,
        confidence=confidence,
        reasoning="Looks like customer data.",
        alternative_concepts=alternatives if alternatives is not None else ["Client"],
    )


def _entity(name: str, prov: str = "Source A") -> Entity:
    return Entity(
        name=name,
        definition="A definition.",
        synonyms=[],
        provenance_text=prov,
        source_doc="test.pdf",
    )


# ── should_interrupt ───────────────────────────────────────────────────────────


class TestShouldInterrupt:
    def test_hitl_flag_true_triggers(self) -> None:
        state: BuilderState = {"hitl_flag": True, "mapping_proposal": _proposal()}  # type: ignore
        assert should_interrupt(state) is True

    def test_low_confidence_triggers(self) -> None:
        state: BuilderState = {"hitl_flag": False, "mapping_proposal": _proposal(confidence=0.5)}  # type: ignore
        assert should_interrupt(state) is True

    def test_high_confidence_no_flag_no_interrupt(self) -> None:
        state: BuilderState = {"hitl_flag": False, "mapping_proposal": _proposal(confidence=0.95)}  # type: ignore
        assert should_interrupt(state) is False

    def test_no_proposal_no_flag_no_interrupt(self) -> None:
        state: BuilderState = {"hitl_flag": False}  # type: ignore
        assert should_interrupt(state) is False

    def test_exactly_at_threshold_no_interrupt(self) -> None:
        # Default threshold is 0.90
        state: BuilderState = {"hitl_flag": False, "mapping_proposal": _proposal(confidence=0.90)}  # type: ignore
        assert should_interrupt(state) is False


# ── build_interrupt_payload ────────────────────────────────────────────────────


class TestBuildInterruptPayload:
    def test_required_keys_present(self) -> None:
        prop = _proposal()
        payload = build_interrupt_payload(prop, [_entity("Customer"), _entity("Client")])
        for key in (
            "table_name",
            "proposed_concept",
            "confidence",
            "reasoning",
            "alternative_concepts",
            "provenance_text",
        ):
            assert key in payload

    def test_proposed_excluded_from_alternatives(self) -> None:
        prop = _proposal(concept="Customer")
        entities = [_entity("Customer"), _entity("Client"), _entity("Account")]
        payload = build_interrupt_payload(prop, entities)
        assert "Customer" not in payload["alternative_concepts"]

    def test_alternatives_capped_at_four(self) -> None:
        prop = _proposal()
        entities = [_entity(f"E{i}") for i in range(10)]
        payload = build_interrupt_payload(prop, entities)
        assert len(payload["alternative_concepts"]) <= 4

    def test_provenance_text_joined(self) -> None:
        prop = _proposal()
        entities = [_entity("X", prov="Prov A"), _entity("Y", prov="Prov B")]
        payload = build_interrupt_payload(prop, entities)
        assert "Prov A" in payload["provenance_text"]
        assert "Prov B" in payload["provenance_text"]

    def test_includes_llm_alternatives(self) -> None:
        prop = _proposal(alternatives=["Item", "SKU"])
        entities = [_entity("Product")]
        payload = build_interrupt_payload(prop, entities)
        # Should include both LLM alternatives and entity names
        assert "Item" in payload["alternative_concepts"] or "SKU" in payload["alternative_concepts"]


# ── hitl_node ─────────────────────────────────────────────────────────────────


class TestHitlNode:
    def _state_high_conf(self) -> BuilderState:
        return {  # type: ignore
            "hitl_flag": False,
            "mapping_proposal": _proposal(confidence=0.99),
            "current_entities": [_entity("Customer")],
        }

    def _state_low_conf(self) -> BuilderState:
        return {  # type: ignore
            "hitl_flag": False,
            "mapping_proposal": _proposal(confidence=0.5),
            "current_entities": [_entity("Client")],
        }

    def test_pass_through_on_high_confidence(self) -> None:
        cmd = hitl_node(self._state_high_conf())
        assert cmd.goto == "Generate_Cypher"

    def test_approve_routes_to_generate_cypher(self) -> None:
        with patch("src.mapping.hitl.interrupt", return_value={"action": "approve"}):
            cmd = hitl_node(self._state_low_conf())
        assert cmd.goto == "Generate_Cypher"

    def test_correct_updates_proposal(self) -> None:
        with patch(
            "src.mapping.hitl.interrupt",
            return_value={"action": "correct", "mapped_concept": "Account"},
        ):
            cmd = hitl_node(self._state_low_conf())
        assert cmd.goto == "Generate_Cypher"
        assert cmd.update["mapping_proposal"].mapped_concept == "Account"
        assert cmd.update["mapping_proposal"].confidence == 1.0

    def test_reject_routes_to_end(self) -> None:
        with patch("src.mapping.hitl.interrupt", return_value={"action": "reject"}):
            cmd = hitl_node(self._state_low_conf())
        assert cmd.goto == "End"
        assert cmd.update["rejected"] is True

    def test_unknown_action_defaults_to_approve(self) -> None:
        with patch("src.mapping.hitl.interrupt", return_value={"action": "???"}):
            cmd = hitl_node(self._state_low_conf())
        assert cmd.goto == "Generate_Cypher"

    def test_none_proposal_routes_to_end(self) -> None:
        state: BuilderState = {"hitl_flag": True, "mapping_proposal": None, "current_entities": []}  # type: ignore
        cmd = hitl_node(state)
        assert cmd.goto == "End"

    def test_correct_without_concept_treats_as_approve(self) -> None:
        with patch("src.mapping.hitl.interrupt", return_value={"action": "correct"}):
            cmd = hitl_node(self._state_low_conf())
        assert cmd.goto == "Generate_Cypher"
        # Should not update the proposal (update is None or doesn't contain mapping_proposal)
        assert cmd.update is None or "mapping_proposal" not in cmd.update
