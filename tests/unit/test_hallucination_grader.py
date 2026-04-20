"""Unit tests for src/generation/hallucination_grader.py — UT-15"""

from __future__ import annotations

import json
from unittest.mock import MagicMock

from src.generation.hallucination_grader import grade_answer
from src.models.schemas import RetrievedChunk

# ── Helpers ───────────────────────────────────────────────────────────────────


def _chunk(name: str) -> RetrievedChunk:
    return RetrievedChunk(
        node_id=name,
        node_type="BusinessConcept",
        text=f"{name}: definition text",
        score=0.85,
        source_type="vector",
        metadata={},
    )


def _make_llm(decision: dict) -> MagicMock:
    llm = MagicMock()
    resp = MagicMock()
    resp.content = json.dumps(decision)
    llm.invoke.return_value = resp
    return llm


# ── grade_answer ──────────────────────────────────────────────────────────────


class TestGradeAnswer:
    def test_pass_verdict(self) -> None:
        llm = _make_llm({"grounded": True, "critique": None, "action": "pass"})
        decision = grade_answer("Query?", "Answer.", [_chunk("X")], llm)
        assert decision.grounded is True
        assert decision.action == "pass"
        assert decision.critique is None

    def test_regenerate_verdict(self) -> None:
        llm = _make_llm(
            {
                "grounded": False,
                "critique": "TB_ORDERS is not in any retrieved chunk.",
                "action": "regenerate",
            }
        )
        decision = grade_answer("Query?", "TB_ORDERS stores orders.", [_chunk("Customer")], llm)
        assert decision.grounded is False
        assert decision.action == "regenerate"
        assert "TB_ORDERS" in decision.critique

    def test_ungrounded_verdict_defaults_to_regenerate(self) -> None:
        verdict = {"grounded": False, "critique": "No relevant context.", "action": "regenerate"}
        llm = _make_llm(verdict)
        decision = grade_answer("Obscure query?", "I don't know.", [], llm)
        assert decision.action == "regenerate"

    def test_llm_failure_defaults_to_pass(self) -> None:
        llm = MagicMock()
        llm.invoke.side_effect = RuntimeError("LLM unavailable")
        decision = grade_answer("?", "Answer.", [], llm)
        assert decision.action == "pass"
        assert decision.grounded is True

    def test_bad_json_defaults_to_pass(self) -> None:
        llm = MagicMock()
        resp = MagicMock()
        resp.content = "not json"
        llm.invoke.return_value = resp
        decision = grade_answer("?", "Answer.", [], llm)
        assert decision.action == "pass"

    def test_inconsistent_grounded_true_with_non_pass_is_corrected(self) -> None:
        llm = _make_llm({"grounded": True, "critique": None, "action": "regenerate"})
        decision = grade_answer("?", "Answer.", [_chunk("X")], llm)
        assert decision.action == "pass"

    def test_context_injected_in_prompt(self) -> None:
        llm = _make_llm({"grounded": True, "critique": None, "action": "pass"})
        grade_answer("What is Customer?", "Customer buys goods.", [_chunk("Customer")], llm)
        call_args = llm.invoke.call_args[0][0]
        human_content = call_args[1].content
        assert "Customer" in human_content

    def test_answer_injected_in_prompt(self) -> None:
        llm = _make_llm({"grounded": True, "critique": None, "action": "pass"})
        grade_answer("Q?", "My special answer text.", [_chunk("X")], llm)
        call_args = llm.invoke.call_args[0][0]
        human_content = call_args[1].content
        assert "My special answer text." in human_content

    def test_system_message_is_first(self) -> None:
        from langchain_core.messages import SystemMessage

        llm = _make_llm({"grounded": True, "critique": None, "action": "pass"})
        grade_answer("?", "Answer.", [], llm)
        call_args = llm.invoke.call_args[0][0]
        assert isinstance(call_args[0], SystemMessage)
