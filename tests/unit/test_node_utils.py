"""Unit tests for src.retrieval.node_utils."""

from __future__ import annotations

from src.retrieval.node_utils import _node_to_text


class TestNodeToText:
    def test_basic_concept_node(self) -> None:
        node = {"name": "Customer", "definition": "A person who buys products"}
        result = _node_to_text(node)
        assert "customer" in result
        assert "person who buys products" in result

    def test_includes_synonyms(self) -> None:
        node = {"name": "Order", "definition": "Purchase", "synonyms": ["Transaction", "Sale"]}
        result = _node_to_text(node)
        assert "transaction" in result
        assert "sale" in result

    def test_includes_column_names(self) -> None:
        node = {"name": "Orders", "definition": "", "column_names": ["order_id", "customer_id"]}
        result = _node_to_text(node)
        assert "order_id" in result
        assert "customer_id" in result

    def test_uses_text_field_as_fallback(self) -> None:
        node = {"text": "This is a parent chunk text", "node_type": "ParentChunk"}
        result = _node_to_text(node)
        assert "parent chunk text" in result

    def test_empty_node_returns_empty(self) -> None:
        assert _node_to_text({}) == ""

    def test_output_is_lowercase(self) -> None:
        node = {"name": "UPPER_CASE", "definition": "MiXeD CaSe"}
        result = _node_to_text(node)
        assert result == result.lower()

    def test_handles_none_values(self) -> None:
        node = {"name": "Test", "definition": None, "synonyms": None, "column_names": None}
        result = _node_to_text(node)
        assert "test" in result
