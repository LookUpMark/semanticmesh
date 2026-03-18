"""Unit tests for src/generation/answer_generator.py — UT-14"""

from __future__ import annotations

from unittest.mock import MagicMock

from src.generation.answer_generator import format_context, generate_answer
from src.models.schemas import RetrievedChunk

# ── Helpers ───────────────────────────────────────────────────────────────────


def _chunk(name: str, text: str, score: float = 0.9) -> RetrievedChunk:
    return RetrievedChunk(
        node_id=name,
        node_type="BusinessConcept",
        text=text,
        score=score,
        source_type="vector",
        metadata={},
    )


def _make_llm(response: str) -> MagicMock:
    llm = MagicMock()
    resp = MagicMock()
    resp.content = response
    llm.invoke.return_value = resp
    return llm


# ── format_context ────────────────────────────────────────────────────────────


class TestFormatContext:
    def test_numbered_list(self) -> None:
        chunks = [_chunk("C", "Customer: buyer"), _chunk("P", "Product: item")]
        result = format_context(chunks)
        assert "[1]" in result
        assert "[2]" in result

    def test_empty_returns_placeholder(self) -> None:
        assert "no context" in format_context([]).lower()

    def test_score_in_output(self) -> None:
        result = format_context([_chunk("X", "X: text", score=0.753)])
        assert "0.753" in result

    def test_node_type_in_output(self) -> None:
        result = format_context([_chunk("X", "X: text")])
        assert "BusinessConcept" in result


# ── generate_answer ───────────────────────────────────────────────────────────


class TestGenerateAnswer:
    def test_returns_string(self) -> None:
        llm = _make_llm("The customer table stores buyer info.")
        answer = generate_answer("What is customer?", [_chunk("Customer", "Customer: buyer")], llm)
        assert isinstance(answer, str)
        assert len(answer) > 0

    def test_no_chunks_uses_placeholder_context(self) -> None:
        llm = _make_llm("I cannot find this information.")
        generate_answer("What is X?", [], llm)
        call_args = llm.invoke.call_args[0][0]
        assert "no context" in call_args[1].content.lower()

    def test_critique_uses_alternative_template(self) -> None:
        llm = _make_llm("Corrected answer.")
        critique = "You mentioned TB_ORDERS which is unsupported."
        generate_answer("?", [_chunk("X", "X")], llm, critique=critique)
        call_args = llm.invoke.call_args[0][0]
        human_content = call_args[1].content
        assert "TB_ORDERS" in human_content

    def test_strips_whitespace_from_response(self) -> None:
        llm = _make_llm("  Answer with spaces  ")
        answer = generate_answer("?", [], llm)
        assert answer == "Answer with spaces"

    def test_no_critique_does_not_include_critique_template(self) -> None:
        llm = _make_llm("answer")
        generate_answer("?", [_chunk("X", "X")], llm, critique=None)
        call_args = llm.invoke.call_args[0][0]
        # ANSWER_USER template should not contain critique placeholder
        assert "critique" not in call_args[1].content.lower()

    def test_system_message_is_first(self) -> None:
        from langchain_core.messages import SystemMessage

        llm = _make_llm("answer")
        generate_answer("?", [], llm)
        call_args = llm.invoke.call_args[0][0]
        assert isinstance(call_args[0], SystemMessage)
