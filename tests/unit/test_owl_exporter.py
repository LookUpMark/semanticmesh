"""Unit tests for src.graph.owl_exporter — Neo4j mocked."""

from __future__ import annotations

import json
from pathlib import Path
from unittest.mock import patch

import pytest

from src.graph import owl_exporter


@pytest.fixture(autouse=True)
def _isolate_export_dir(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setattr(owl_exporter, "_EXPORT_DIR", tmp_path / "owl_exports")
    yield


def _fake_graph_dump():
    """Mirror kg_registry._export_graph() output without Neo4j."""
    nodes = [
        {"eid": "1", "labels": ["BusinessConcept"],
         "props": {"name": "Customer", "definition": "A buyer"}},
        {"eid": "2", "labels": ["PhysicalTable"],
         "props": {"table_name": "TB_CST", "ddl_source": "CREATE TABLE..."}},
    ]
    edges = [
        {"eid": "r1", "start_eid": "1", "end_eid": "2",
         "rel_type": "MAPPED_TO", "props": {"confidence": 0.9}},
    ]
    return nodes, edges


class TestExportToOwlFiles:
    def test_writes_four_owl_files_plus_metadata(self, tmp_path: Path) -> None:
        with patch.object(owl_exporter, "_dump_graph", return_value=_fake_graph_dump()):
            meta = owl_exporter.export_to_owl_files()
        out_dir = tmp_path / "owl_exports" / meta["export_id"]
        assert (out_dir / "entities.owl").exists()
        assert (out_dir / "tables.owl").exists()
        assert (out_dir / "mappings.owl").exists()
        assert (out_dir / "technical.owl").exists()
        assert (out_dir / "metadata.json").exists()

    def test_metadata_records_counts_and_checksums(self) -> None:
        with patch.object(owl_exporter, "_dump_graph", return_value=_fake_graph_dump()):
            meta = owl_exporter.export_to_owl_files()
        assert meta["nodes_count"] == 2
        assert meta["relationships_count"] == 1
        expected_files = {"entities.owl", "tables.owl", "mappings.owl", "technical.owl"}
        assert set(meta["checksums"]) == expected_files
        # checksum is a 64-char hex sha256
        assert all(len(h) == 64 for h in meta["checksums"].values())

    def test_metadata_json_round_trips(self, tmp_path: Path) -> None:
        with patch.object(owl_exporter, "_dump_graph", return_value=_fake_graph_dump()):
            meta = owl_exporter.export_to_owl_files()
        out_dir = tmp_path / "owl_exports" / meta["export_id"]
        loaded = json.loads((out_dir / "metadata.json").read_text())
        assert loaded["export_id"] == meta["export_id"]
        assert loaded["nodes_count"] == 2

    def test_empty_graph_raises(self) -> None:
        with (
            patch.object(owl_exporter, "_dump_graph", return_value=([], [])),
            pytest.raises(ValueError, match="no_data_to_export"),
        ):
            owl_exporter.export_to_owl_files()


class TestExportDirValidation:
    def test_rejects_traversal_id(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setattr(owl_exporter, "_EXPORT_DIR", tmp_path / "owl_exports")
        with pytest.raises(ValueError, match="invalid_export_id"):
            owl_exporter.export_dir("..")

    def test_rejects_malformed_id(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setattr(owl_exporter, "_EXPORT_DIR", tmp_path / "owl_exports")
        with pytest.raises(ValueError, match="invalid_export_id"):
            owl_exporter.export_dir("not-a-timestamp")

    def test_accepts_well_formed_id(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        exports = tmp_path / "owl_exports"
        exports.mkdir()
        (exports / "20260724_143022").mkdir()
        monkeypatch.setattr(owl_exporter, "_EXPORT_DIR", exports)
        assert owl_exporter.export_dir("20260724_143022").exists()


class TestCrossPartitionEdges:
    def test_cross_partition_edges_survive_file_split(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        # Regression: edges whose endpoints live in different label partitions
        # (e.g. Chunk→BusinessConcept MENTIONS, PhysicalTable→Attribute HAS_COLUMN)
        # were dropped because per-file RDF build only knew that file's nodes.
        # Each edge must carry both endpoint nodes into its partition file.
        from src.graph.owl_mapper import from_owl_documents

        monkeypatch.setattr(owl_exporter, "_EXPORT_DIR", tmp_path / "owl_exports")
        nodes = [
            {"eid": "1", "labels": ["BusinessConcept"], "props": {"name": "Customer"}},
            {"eid": "2", "labels": ["Chunk"], "props": {"chunk_index": 0, "source_doc": "g.pdf"}},
            {"eid": "3", "labels": ["PhysicalTable"], "props": {"table_name": "TB_CST"}},
            {"eid": "4", "labels": ["Attribute"], "props": {"name": "id"}},
        ]
        edges = [
            {"eid": "r1", "start_eid": "2", "end_eid": "1", "rel_type": "MENTIONS", "props": {}},
            {"eid": "r2", "start_eid": "3", "end_eid": "4", "rel_type": "HAS_COLUMN", "props": {}},
        ]
        with patch.object(owl_exporter, "_dump_graph", return_value=(nodes, edges)):
            meta = owl_exporter.export_to_owl_files()

        directory = owl_exporter.export_dir(meta["export_id"])
        texts = [p.read_text() for p in directory.glob("*.owl")]
        _out_nodes, out_edges = from_owl_documents(texts)
        rel_types = {e["rel_type"] for e in out_edges}
        assert rel_types == {"MENTIONS", "HAS_COLUMN"}
        assert len(out_edges) == 2
