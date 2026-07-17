"""Unit tests for src/graph/cypher_generator.py — UT-12"""

from __future__ import annotations

from unittest.mock import MagicMock, patch

import pytest

from src.graph.cypher_generator import (
    _detect_multi_statement,
    _format_few_shot,
    generate_cypher,
    strip_cypher_fence,
)
from src.models.schemas import CypherExample, Entity, MappingProposal, TableSchema
from src.prompts.templates import CYPHER_SYSTEM, CYPHER_USER

# ── Helpers ────────────────────────────────────────────────────────────────────


def _make_example(
    ddl: str = "CREATE TABLE test (id INT)",
    cypher: str = "MERGE (n:test)",
    description: str = "Test example",
    concept: str = "TestConcept",
) -> CypherExample:
    return CypherExample(
        description=description,
        ddl_snippet=ddl,
        concept_name=concept,
        cypher=cypher,
    )


def _make_mapping(
    table_name: str = "TB_CST",
    concept: str = "Customer",
    confidence: float = 0.95,
) -> MappingProposal:
    return MappingProposal(
        table_name=table_name,
        mapped_concept=concept,
        confidence=confidence,
        reasoning="Looks like customer data.",
        alternative_concepts=["Client"],
    )


def _make_entity(
    name: str = "Customer",
    definition: str = "A person who buys things.",
    synonyms: list[str] | None = None,
    provenance: str = "Business Glossary",
    source_doc: str = "test.pdf",
) -> Entity:
    return Entity(
        name=name,
        definition=definition,
        synonyms=synonyms or [],
        provenance_text=provenance,
        source_doc=source_doc,
    )


def _make_table(
    table_name: str = "TB_CST",
    columns: list | None = None,
    ddl: str = "CREATE TABLE TB_CST (id INT, name VARCHAR(100))",
) -> TableSchema:
    from src.models.schemas import ColumnSchema

    if columns is None:
        columns = [
            ColumnSchema(name="id", data_type="INT", nullable=False),
            ColumnSchema(name="name", data_type="VARCHAR(100)", nullable=True),
        ]
    return TableSchema(table_name=table_name, columns=columns, ddl_source=ddl)


def _make_llm_response(content: str) -> MagicMock:
    """Create a mock LLM response with the given content."""
    response = MagicMock()
    response.content = content
    return response


# ── strip_cypher_fence ──────────────────────────────────────────────────────────


class TestStripCypherFence:
    def test_removes_triple_backticks_with_cypher_lang(self) -> None:
        raw = "```cypher\nMERGE (n:Test)\n```"
        result = strip_cypher_fence(raw)
        assert result == "MERGE (n:Test)"

    def test_removes_triple_backticks_without_lang(self) -> None:
        raw = "```\nMERGE (n:Test)\n```"
        result = strip_cypher_fence(raw)
        assert result == "MERGE (n:Test)"

    def test_removes_only_opening_fence(self) -> None:
        raw = "```cypher\nMERGE (n:Test)"
        result = strip_cypher_fence(raw)
        assert result == "MERGE (n:Test)"

    def test_removes_only_closing_fence(self) -> None:
        raw = "MERGE (n:Test)\n```"
        result = strip_cypher_fence(raw)
        assert result == "MERGE (n:Test)"

    def test_removes_both_fences_multiline(self) -> None:
        raw = "```cypher\nMERGE (n:Test {id: $id})\nSET n.name = $name\n```"
        result = strip_cypher_fence(raw)
        assert result == "MERGE (n:Test {id: $id})\nSET n.name = $name"

    def test_passthrough_when_no_fences(self) -> None:
        raw = "MERGE (n:Test)"
        result = strip_cypher_fence(raw)
        assert result == "MERGE (n:Test)"

    def test_strips_surrounding_whitespace(self) -> None:
        # Note: The regex requires fence at line start (^ in MULTILINE)
        # Spaces before fence prevent opening fence removal
        # But closing fence at end of line IS removed by ```$ pattern
        # Then strip() removes remaining outer whitespace
        raw = "  ```cypher\nMERGE (n:Test)\n```  "
        result = strip_cypher_fence(raw)
        # Opening fence not matched (leading spaces), closing fence
        # matched, outer whitespace stripped
        assert result == "```cypher\nMERGE (n:Test)"

    def test_fences_at_line_start_are_removed(self) -> None:
        # Fences at actual line start (no leading spaces) are properly removed
        raw = "```cypher\nMERGE (n:Test)\n```"
        result = strip_cypher_fence(raw)
        assert result == "MERGE (n:Test)"

    def test_handles_empty_string(self) -> None:
        result = strip_cypher_fence("")
        assert result == ""

    def test_handles_fences_with_other_languages(self) -> None:
        raw = "```sql\nSELECT * FROM test\n```"
        result = strip_cypher_fence(raw)
        assert result == "SELECT * FROM test"


# ── _format_few_shot ───────────────────────────────────────────────────────────


class TestFormatFewShot:
    def test_formats_single_example(self) -> None:
        examples = [_make_example("CREATE TABLE test (id INT)", "MERGE (n:test)")]
        result = _format_few_shot(examples)
        assert "Example 1:" in result
        assert "DDL:" in result
        assert "CREATE TABLE test (id INT)" in result
        assert "Cypher:" in result
        assert "MERGE (n:test)" in result

    def test_formats_multiple_examples(self) -> None:
        examples = [
            _make_example("CREATE TABLE a (id INT)", "MERGE (n:a)"),
            _make_example("CREATE TABLE b (name VARCHAR)", "MERGE (n:b)"),
        ]
        result = _format_few_shot(examples)
        assert "Example 1:" in result
        assert "Example 2:" in result
        assert "---" in result  # Separator between examples

    def test_empty_list_returns_placeholder(self) -> None:
        result = _format_few_shot([])
        assert result == "(no examples provided)"

    def test_separator_between_examples(self) -> None:
        examples = [
            _make_example("DDL A", "CYPHER A"),
            _make_example("DDL B", "CYPHER B"),
        ]
        result = _format_few_shot(examples)
        # Check separator exists between examples
        parts = result.split("\n\n---\n\n")
        assert len(parts) == 2

    def test_preserves_newlines_in_content(self) -> None:
        examples = [_make_example("CREATE TABLE test (\n  id INT\n)", "MERGE\n  (n:test)")]
        result = _format_few_shot(examples)
        assert "id INT" in result
        assert "MERGE" in result


# ── generate_cypher ────────────────────────────────────────────────────────────


class TestGenerateCypher:
    def test_happy_path_returns_cypher(self) -> None:
        mapping = _make_mapping()
        table = _make_table()
        entity = _make_entity()
        few_shot = [_make_example()]

        llm_mock = MagicMock()
        llm_mock.invoke.return_value = _make_llm_response("MERGE (n:Customer {name: $name})")

        result = generate_cypher(mapping, table, entity, few_shot, llm_mock)

        assert result == "MERGE (n:Customer {name: $name})"
        llm_mock.invoke.assert_called_once()

    def test_strips_fences_from_llm_output(self) -> None:
        mapping = _make_mapping()
        table = _make_table()
        entity = _make_entity()
        few_shot = [_make_example()]

        llm_mock = MagicMock()
        llm_mock.invoke.return_value = _make_llm_response("```cypher\nMERGE (n:Test)\n```")

        result = generate_cypher(mapping, table, entity, few_shot, llm_mock)

        assert result == "MERGE (n:Test)"

    def test_includes_few_shot_examples_in_prompt(self) -> None:
        mapping = _make_mapping()
        table = _make_table()
        entity = _make_entity()
        examples = [
            _make_example("CREATE TABLE test (id INT)", "MERGE (n:test {id: $id})"),
        ]

        llm_mock = MagicMock()
        llm_mock.invoke.return_value = _make_llm_response("MERGE (n:Customer)")

        generate_cypher(mapping, table, entity, examples, llm_mock)

        # Verify invoke was called
        assert llm_mock.invoke.called
        # The prompt should include the example
        call_args = llm_mock.invoke.call_args
        messages = call_args[0][0]
        user_content = messages[1].content
        assert "CREATE TABLE test (id INT)" in user_content
        assert "MERGE (n:test {id: $id})" in user_content

    def test_empty_synonyms_becomes_empty_text(self) -> None:
        entity = _make_entity(synonyms=[])
        table = _make_table()
        mapping = _make_mapping()
        few_shot = []

        llm_mock = MagicMock()
        llm_mock.invoke.return_value = _make_llm_response("MERGE (n:Customer)")

        generate_cypher(mapping, table, entity, few_shot, llm_mock)

        call_args = llm_mock.invoke.call_args
        user_content = call_args[0][0][1].content
        # Empty synonyms should NOT produce the string "none"
        assert "synonyms: none" not in user_content.lower()

    def test_synonyms_joined_with_comma(self) -> None:
        entity = _make_entity(synonyms=["Client", "Buyer"])
        table = _make_table()
        mapping = _make_mapping()
        few_shot = []

        llm_mock = MagicMock()
        llm_mock.invoke.return_value = _make_llm_response("MERGE (n:Customer)")

        generate_cypher(mapping, table, entity, few_shot, llm_mock)

        call_args = llm_mock.invoke.call_args
        user_content = call_args[0][0][1].content
        assert "Client, Buyer" in user_content

    def test_empty_provenance_becomes_empty_string(self) -> None:
        entity = _make_entity(provenance="")
        table = _make_table()
        mapping = _make_mapping()
        few_shot = []

        llm_mock = MagicMock()
        llm_mock.invoke.return_value = _make_llm_response("MERGE (n:Test)")

        generate_cypher(mapping, table, entity, few_shot, llm_mock)

        # Should not raise, should handle empty provenance gracefully
        call_args = llm_mock.invoke.call_args
        assert llm_mock.invoke.called

    def test_llm_error_raises_runtime_error(self) -> None:
        mapping = _make_mapping()
        table = _make_table()
        entity = _make_entity()
        few_shot = []

        llm_mock = MagicMock()
        llm_mock.invoke.side_effect = Exception("LLM timeout")

        with pytest.raises(RuntimeError, match="LLM call failed"):
            generate_cypher(mapping, table, entity, few_shot, llm_mock)

    @patch("src.graph.cypher_generator.logger")
    def test_logs_generation_start(self, mock_logger: MagicMock) -> None:
        mapping = _make_mapping(table_name="TB_CUSTOMER")
        table = _make_table(table_name="TB_CUSTOMER")
        entity = _make_entity()
        few_shot = []

        llm_mock = MagicMock()
        llm_mock.invoke.return_value = _make_llm_response("MERGE (n:Customer)")

        generate_cypher(mapping, table, entity, few_shot, llm_mock)

        # Check debug log was called with table name
        assert any(
            "TB_CUSTOMER" in str(call) and "Customer" in str(call)
            for call in mock_logger.debug.call_args_list
        )

    @patch("src.graph.cypher_generator.logger")
    def test_logs_generation_complete_with_length(self, mock_logger: MagicMock) -> None:
        mapping = _make_mapping()
        table = _make_table()
        entity = _make_entity()
        few_shot = []

        llm_mock = MagicMock()
        llm_mock.invoke.return_value = _make_llm_response("MERGE (n:Customer)")

        generate_cypher(mapping, table, entity, few_shot, llm_mock)

        # Check info log was called with length
        assert any(
            "Cypher generated" in str(call) and "chars" in str(call)
            for call in mock_logger.info.call_args_list
        )


# ── Cypher prompt contract (point 3: single-statement enforcement) ────────────


class TestCypherPromptContract:
    """The prompt must steer the LLM toward ONE Cypher statement.

    Multi-statement output (``;``-separated) is rejected by the AUDIT-069
    guard and forces a deterministic-builder fallback (~38×/run before this
    fix). The prompt is the primary, correctness-safe lever to reduce that.
    """

    def test_system_prompt_requires_single_statement(self) -> None:
        lower = CYPHER_SYSTEM.lower()
        assert "single" in lower or "one statement" in lower or "one cypher" in lower

    def test_system_prompt_warns_against_semicolons(self) -> None:
        lower = CYPHER_SYSTEM.lower()
        assert "semicolon" in lower or "no `;`" in lower or "do not separate" in lower

    def test_user_prompt_uses_singular_statement(self) -> None:
        # The user prompt historically said "statements" (plural), which nudges
        # the LLM toward emitting multiple ;-separated statements.
        assert "Cypher statement for the following mapping" in CYPHER_USER


# ── _detect_multi_statement ───────────────────────────────────────────────────


class TestDetectMultiStatement:
    def test_single_statement_returns_false(self) -> None:
        assert _detect_multi_statement("MERGE (n:Test {id: 1}) SET n.x = 1") is False

    def test_two_statements_returns_true(self) -> None:
        cypher = "MERGE (n:A {id: 1}); MERGE (n:B {id: 2})"
        assert _detect_multi_statement(cypher) is True

    def test_three_statements_returns_true(self) -> None:
        cypher = "MERGE (c:C {id: 1}); MERGE (t:T {id: 2}); MERGE (c)-[:R]->(t)"
        assert _detect_multi_statement(cypher) is True

    def test_trailing_semicolon_is_single_statement(self) -> None:
        # A trailing ';' with nothing after it is still one statement.
        assert _detect_multi_statement("MERGE (n:Test {id: 1});") is False

    def test_semicolon_inside_single_quoted_string_returns_false(self) -> None:
        cypher = "MERGE (n:Test {id: 1}) SET n.desc = 'a; b; c'"
        assert _detect_multi_statement(cypher) is False

    def test_semicolon_inside_double_quoted_string_returns_false(self) -> None:
        cypher = 'MERGE (n:Test {id: 1}) SET n.desc = "a; b; c"'
        assert _detect_multi_statement(cypher) is False

    def test_empty_string_returns_false(self) -> None:
        assert _detect_multi_statement("") is False

    def test_only_whitespace_returns_false(self) -> None:
        assert _detect_multi_statement("   \n\t  ") is False


# ── generate_cypher: multi-statement observability ────────────────────────────


class TestGenerateCypherMultiStatement:
    @patch("src.graph.cypher_generator.logger")
    def test_logs_warning_when_llm_emits_multi_statement(self, mock_logger: MagicMock) -> None:
        mapping = _make_mapping(table_name="TB_CST")
        table = _make_table(table_name="TB_CST")
        entity = _make_entity()
        few_shot = []

        llm_mock = MagicMock()
        llm_mock.invoke.return_value = _make_llm_response(
            "MERGE (n:A {id: 1}); MERGE (n:B {id: 2})"
        )

        generate_cypher(mapping, table, entity, few_shot, llm_mock)

        # A source-level warning must fire so the emission is observable before
        # the downstream AUDIT-069 execute-time rejection.
        assert any(
            "TB_CST" in str(call) and "multi-statement" in str(call).lower()
            for call in mock_logger.warning.call_args_list
        )

    @patch("src.graph.cypher_generator.logger")
    def test_no_multi_statement_warning_for_single_statement(
        self, mock_logger: MagicMock
    ) -> None:
        mapping = _make_mapping()
        table = _make_table()
        entity = _make_entity()
        few_shot = []

        llm_mock = MagicMock()
        llm_mock.invoke.return_value = _make_llm_response("MERGE (n:Customer {id: 1})")

        generate_cypher(mapping, table, entity, few_shot, llm_mock)

        assert not any(
            "multi-statement" in str(call).lower()
            for call in mock_logger.warning.call_args_list
        )
