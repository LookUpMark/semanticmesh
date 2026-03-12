"""Unit tests for src/graph/cypher_healer.py — UT-13"""

from __future__ import annotations

from unittest.mock import MagicMock

import neo4j.exceptions
import pytest

from src.graph.cypher_healer import fix_cypher, heal_cypher, validate_cypher
from src.models.schemas import MappingProposal


# ── Helpers ────────────────────────────────────────────────────────────────────

GOOD_CYPHER = "MERGE (bc:BusinessConcept {name: $name})"
BAD_CYPHER = "MERGE (bc:BusinessConcept name: $name)"  # missing braces


def _mapping(table: str = "TB_CST") -> MappingProposal:
    return MappingProposal(
        table_name=table,
        mapped_concept="Customer",
        confidence=0.97,
        reasoning="Test.",
        alternative_concepts=[],
    )


def _make_driver(*, should_fail: bool = False, error_msg: str = "syntax error") -> MagicMock:
    driver = MagicMock()
    session = MagicMock()
    session.__enter__ = MagicMock(return_value=session)
    session.__exit__ = MagicMock(return_value=False)

    if should_fail:
        result = MagicMock()
        result.consume.side_effect = neo4j.exceptions.CypherSyntaxError(error_msg)
        session.run.return_value = result
    else:
        result = MagicMock()
        result.consume.return_value = None
        session.run.return_value = result

    driver.session.return_value = session
    return driver


def _make_llm(fixed_cypher: str) -> MagicMock:
    llm = MagicMock()
    resp = MagicMock()
    resp.content = fixed_cypher
    llm.invoke.return_value = resp
    return llm


# ── validate_cypher ────────────────────────────────────────────────────────────

class TestValidateCypher:
    def test_valid_cypher_returns_true(self) -> None:
        driver = _make_driver(should_fail=False)
        ok, err = validate_cypher(GOOD_CYPHER, driver)
        assert ok is True
        assert err is None

    def test_invalid_cypher_returns_false_with_error(self) -> None:
        driver = _make_driver(should_fail=True, error_msg="Invalid syntax near 'name'")
        ok, err = validate_cypher(BAD_CYPHER, driver)
        assert ok is False
        assert err is not None
        assert len(err) > 0

    def test_explain_prefix_added(self) -> None:
        driver = _make_driver(should_fail=False)
        session = driver.session.return_value
        validate_cypher(GOOD_CYPHER, driver)
        call_arg = session.run.call_args[0][0]
        assert call_arg.startswith("EXPLAIN ")

    def test_generic_exception_returns_false(self) -> None:
        driver = MagicMock()
        session = MagicMock()
        session.__enter__ = MagicMock(return_value=session)
        session.__exit__ = MagicMock(return_value=False)
        result = MagicMock()
        result.consume.side_effect = Exception("network error")
        session.run.return_value = result
        driver.session.return_value = session
        ok, err = validate_cypher(GOOD_CYPHER, driver)
        assert ok is False
        assert "network error" in err


# ── fix_cypher ────────────────────────────────────────────────────────────────

class TestFixCypher:
    def test_returns_stripped_cypher(self) -> None:
        llm = _make_llm("```cypher\n" + GOOD_CYPHER + "\n```")
        result = fix_cypher(BAD_CYPHER, "syntax error", _mapping(), llm)
        assert "```" not in result
        assert "MERGE" in result

    def test_error_injected_in_prompt(self) -> None:
        llm = _make_llm(GOOD_CYPHER)
        fix_cypher(BAD_CYPHER, "CypherSyntaxError: expected { near name", _mapping(), llm)
        call = llm.invoke.call_args[0][0]
        human_content = call[1].content
        assert "CypherSyntaxError" in human_content

    def test_llm_failure_propagates(self) -> None:
        llm = MagicMock()
        llm.invoke.side_effect = RuntimeError("LLM down")
        with pytest.raises(RuntimeError):
            fix_cypher(BAD_CYPHER, "error", _mapping(), llm)


# ── heal_cypher ───────────────────────────────────────────────────────────────

class TestHealCypher:
    def test_passes_on_first_try(self) -> None:
        driver = _make_driver(should_fail=False)
        llm = MagicMock()
        result = heal_cypher(GOOD_CYPHER, _mapping(), driver, llm, max_attempts=3)
        assert result == GOOD_CYPHER
        llm.invoke.assert_not_called()

    def test_heals_on_second_attempt(self) -> None:
        call_count = 0

        def _side_effect(stmt):
            nonlocal call_count
            call_count += 1
            mock_result = MagicMock()
            if call_count == 1:
                mock_result.consume.side_effect = neo4j.exceptions.CypherSyntaxError("bad")
            else:
                mock_result.consume.return_value = None
            return mock_result

        driver = MagicMock()
        session = MagicMock()
        session.__enter__ = MagicMock(return_value=session)
        session.__exit__ = MagicMock(return_value=False)
        session.run.side_effect = _side_effect
        driver.session.return_value = session

        llm = _make_llm(GOOD_CYPHER)
        result = heal_cypher(BAD_CYPHER, _mapping(), driver, llm, max_attempts=3)
        assert result == GOOD_CYPHER

    def test_exhaustion_returns_none(self) -> None:
        driver = _make_driver(should_fail=True)
        llm = _make_llm(BAD_CYPHER)  # LLM keeps returning bad Cypher
        result = heal_cypher(BAD_CYPHER, _mapping(), driver, llm, max_attempts=3)
        assert result is None

    def test_max_attempts_respected(self) -> None:
        driver = _make_driver(should_fail=True)
        llm = _make_llm(BAD_CYPHER)
        heal_cypher(BAD_CYPHER, _mapping(), driver, llm, max_attempts=2)
        # test called 2 times, fix called 1 time (no fix on last attempt)
        assert llm.invoke.call_count == 1

    def test_fix_llm_failure_returns_none(self) -> None:
        driver = _make_driver(should_fail=True)
        llm = MagicMock()
        llm.invoke.side_effect = RuntimeError("LLM error")
        result = heal_cypher(BAD_CYPHER, _mapping(), driver, llm, max_attempts=3)
        assert result is None
