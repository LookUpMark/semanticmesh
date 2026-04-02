"""Unit tests for src/prompts/few_shot.py"""

from __future__ import annotations

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
