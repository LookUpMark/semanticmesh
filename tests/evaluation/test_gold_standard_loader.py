"""Unit tests for gold_standard_loader."""

from __future__ import annotations

import json
from pathlib import Path  # noqa: TC003

import pytest

from src.evaluation.gold_standard_loader import load_gold_standard


# ─────────────────────────────────────────────────────────────────────────────
# Helpers
# ─────────────────────────────────────────────────────────────────────────────

def _write(path: Path, data: object) -> None:
    path.write_text(json.dumps(data), encoding="utf-8")


# ─────────────────────────────────────────────────────────────────────────────
# Format: DS01-style  {"pairs": [...]}
# ─────────────────────────────────────────────────────────────────────────────


class TestDS01Style:
    def test_loads_pairs_key(self, tmp_path: Path) -> None:
        p = tmp_path / "gs.json"
        _write(p, {
            "dataset_name": "DS01",
            "domain": "ecommerce",
            "pairs": [
                {"id": 1, "question": "What customers exist?", "expected_answer": "3 customers",
                 "expected_sources": ["Customer"], "query_type": "fact", "difficulty": "easy"},
            ],
        })
        meta, pairs = load_gold_standard(p)
        assert meta["dataset_name"] == "DS01"
        assert len(pairs) == 1
        assert pairs[0]["query_id"] == "1"
        assert pairs[0]["expected_answer"] == "3 customers"

    def test_normalizes_id_to_query_id(self, tmp_path: Path) -> None:
        p = tmp_path / "gs.json"
        _write(p, {"pairs": [{"id": 42, "question": "q"}]})
        _, pairs = load_gold_standard(p)
        assert pairs[0]["query_id"] == "42"

    def test_auto_generates_query_id(self, tmp_path: Path) -> None:
        p = tmp_path / "gs.json"
        _write(p, {"pairs": [{"question": "q"}]})
        _, pairs = load_gold_standard(p)
        assert pairs[0]["query_id"] == "Q001"


# ─────────────────────────────────────────────────────────────────────────────
# Format: DS02-style  {"qa_pairs": [...]} with variant field names
# ─────────────────────────────────────────────────────────────────────────────


class TestDS02Style:
    def test_loads_qa_pairs_key(self, tmp_path: Path) -> None:
        p = tmp_path / "gs.json"
        _write(p, {
            "dataset_name": "DS02",
            "qa_pairs": [
                {"question": "Total revenue?", "answer": "$1M",
                 "entities": ["Revenue"], "category": "aggregate", "difficulty": "medium"},
            ],
        })
        meta, pairs = load_gold_standard(p)
        assert len(pairs) == 1
        assert pairs[0]["expected_answer"] == "$1M"
        assert pairs[0]["expected_sources"] == ["Revenue"]
        assert pairs[0]["query_type"] == "aggregate"

    def test_falls_back_on_missing_fields(self, tmp_path: Path) -> None:
        p = tmp_path / "gs.json"
        _write(p, {"qa_pairs": [{"question": "q?"}]})
        _, pairs = load_gold_standard(p)
        assert pairs[0]["expected_answer"] == ""
        assert pairs[0]["expected_sources"] == []
        assert pairs[0]["query_type"] == "unknown"
        assert pairs[0]["difficulty"] == "unknown"


# ─────────────────────────────────────────────────────────────────────────────
# Format: DS03-style  {"qa_pairs": [...]} with "complexity" instead of "difficulty"
# ─────────────────────────────────────────────────────────────────────────────


class TestDS03Style:
    def test_complexity_maps_to_difficulty(self, tmp_path: Path) -> None:
        p = tmp_path / "gs.json"
        _write(p, {
            "qa_pairs": [
                {"question": "q?", "expected_answer": "a",
                 "expected_sources": ["T"], "query_type": "multi_hop", "complexity": "hard"},
            ],
        })
        _, pairs = load_gold_standard(p)
        assert pairs[0]["difficulty"] == "hard"
        assert pairs[0]["query_type"] == "multi_hop"


# ─────────────────────────────────────────────────────────────────────────────
# Format: bare JSON array
# ─────────────────────────────────────────────────────────────────────────────


class TestBareArray:
    def test_loads_bare_array(self, tmp_path: Path) -> None:
        p = tmp_path / "gs.json"
        _write(p, [
            {"question": "q1", "ground_truth": "a1"},
            {"question": "q2", "answer": "a2"},
        ])
        meta, pairs = load_gold_standard(p)
        assert meta == {}
        assert len(pairs) == 2
        assert pairs[0]["expected_answer"] == "a1"
        assert pairs[1]["expected_answer"] == "a2"

    def test_empty_array(self, tmp_path: Path) -> None:
        p = tmp_path / "gs.json"
        _write(p, [])
        meta, pairs = load_gold_standard(p)
        assert pairs == []


# ─────────────────────────────────────────────────────────────────────────────
# Edge cases
# ─────────────────────────────────────────────────────────────────────────────


class TestEdgeCases:
    def test_dict_without_recognized_keys_returns_empty(self, tmp_path: Path) -> None:
        p = tmp_path / "gs.json"
        _write(p, {"random_key": [1, 2, 3]})
        meta, pairs = load_gold_standard(p)
        assert len(pairs) == 0

    def test_non_dict_items_skipped(self, tmp_path: Path) -> None:
        p = tmp_path / "gs.json"
        _write(p, {"pairs": ["not a dict", {"question": "valid"}, 42]})
        _, pairs = load_gold_standard(p)
        assert len(pairs) == 1
        assert pairs[0]["question"] == "valid"

    def test_answer_priority_order(self, tmp_path: Path) -> None:
        """expected_answer takes priority over answer and ground_truth."""
        p = tmp_path / "gs.json"
        _write(p, {"pairs": [{
            "question": "q",
            "expected_answer": "first",
            "answer": "second",
            "ground_truth": "third",
        }]})
        _, pairs = load_gold_standard(p)
        assert pairs[0]["expected_answer"] == "first"

    def test_answer_falls_through_to_ground_truth(self, tmp_path: Path) -> None:
        p = tmp_path / "gs.json"
        _write(p, {"pairs": [{
            "question": "q",
            "ground_truth": "fallback",
        }]})
        _, pairs = load_gold_standard(p)
        assert pairs[0]["expected_answer"] == "fallback"

    def test_sources_falls_through_to_tables_involved(self, tmp_path: Path) -> None:
        p = tmp_path / "gs.json"
        _write(p, {"pairs": [{
            "question": "q",
            "tables_involved": ["Orders", "Customers"],
        }]})
        _, pairs = load_gold_standard(p)
        assert pairs[0]["expected_sources"] == ["Orders", "Customers"]

    def test_invalid_json_raises(self, tmp_path: Path) -> None:
        p = tmp_path / "gs.json"
        p.write_text("not json", encoding="utf-8")
        with pytest.raises(json.JSONDecodeError):
            load_gold_standard(p)
