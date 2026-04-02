"""Unit tests for src/prompts/templates.py — UT-16"""

from __future__ import annotations

from src.prompts import templates


class TestTemplateConstants:
    """Verify all expected constants are present and have required placeholders."""

    # (constant_name, required_placeholders)
    SYSTEM_CONSTANTS = [
        "EXTRACTION_SYSTEM",
        "ER_JUDGE_SYSTEM",
        "MAPPING_SYSTEM",
        "ENRICHMENT_SYSTEM",
        "CRITIC_SYSTEM",
        "CYPHER_SYSTEM",
        "ANSWER_SYSTEM",
        "GRADER_SYSTEM",
    ]
    USER_CONSTANTS_WITH_VARS = [
        ("EXTRACTION_USER", ["chunk_text"]),
        ("ER_JUDGE_USER", ["variants_json", "provenance_json"]),
        ("MAPPING_USER", ["few_shot_examples", "table_ddl", "entities_json"]),
        ("ENRICHMENT_USER", ["table_name", "columns_text"]),
        ("CRITIC_USER", ["proposal_json", "table_ddl", "entities_json"]),
        ("REFLECTION_TEMPLATE", ["role", "output_format", "error_or_critique", "original_input"]),
        ("CYPHER_USER", ["few_shot_examples", "concept_name", "table_ddl"]),
        ("CYPHER_FIX_USER", ["broken_cypher", "error_message"]),
        ("ANSWER_USER", ["context_chunks", "user_query"]),
        ("ANSWER_WITH_CRITIQUE_USER", ["hallucination_critique", "context_chunks", "user_query"]),
        ("GRADER_USER", ["context_chunks", "generated_answer", "user_query"]),
    ]

    def test_all_system_constants_exist(self) -> None:
        for name in self.SYSTEM_CONSTANTS:
            assert hasattr(templates, name), f"Missing: {name}"
            assert isinstance(getattr(templates, name), str)
            assert len(getattr(templates, name)) > 50, f"Too short: {name}"

    def test_all_user_constants_have_placeholders(self) -> None:
        for name, required in self.USER_CONSTANTS_WITH_VARS:
            tmpl = getattr(templates, name)
            for var in required:
                assert f"{{{var}}}" in tmpl, f"Missing placeholder {{{var}}} in {name}"

    def test_few_shot_mapping_examples_not_empty(self) -> None:
        assert len(templates.FEW_SHOT_MAPPING_EXAMPLES) > 100

    def test_few_shot_mapping_examples_contains_all_three_examples(self) -> None:
        fse = templates.FEW_SHOT_MAPPING_EXAMPLES
        assert "CUSTOMER_MASTER" in fse
        assert "TB_PRODUCT" in fse
        assert "SYS_AUDIT_LOG" in fse


class TestTemplateFormatting:
    """Verify templates can be formatted with dummy values without KeyError."""

    def test_extraction_user_format(self) -> None:
        result = templates.EXTRACTION_USER.format(chunk_text="Test passage.")
        assert "Test passage." in result

    def test_reflection_template_format(self) -> None:
        result = templates.REFLECTION_TEMPLATE.format(
            role="Cypher expert",
            output_format="Cypher statement",
            error_or_critique="Syntax error on line 1",
            original_input="MERGE (n:Node)",
        )
        assert "Cypher expert" in result
        assert "Syntax error on line 1" in result

    def test_answer_with_critique_user_format(self) -> None:
        result = templates.ANSWER_WITH_CRITIQUE_USER.format(
            hallucination_critique="TB_X not in context",
            context_chunks="[1] Customer: ...",
            user_query="What is a Customer?",
        )
        assert "TB_X not in context" in result
        assert "What is a Customer?" in result

    def test_cypher_system_bans_bare_create(self) -> None:
        assert "Never use bare CREATE" in templates.CYPHER_SYSTEM

    def test_grader_system_has_two_actions(self) -> None:
        for action in ("pass", "regenerate"):
            assert action in templates.GRADER_SYSTEM
        assert "web_search" not in templates.GRADER_SYSTEM
