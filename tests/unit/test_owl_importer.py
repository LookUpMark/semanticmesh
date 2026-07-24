"""Unit tests for src.graph.owl_importer — Neo4j mocked."""

from __future__ import annotations

from unittest.mock import MagicMock, patch

import pytest

from src.graph import owl_importer
from src.graph.owl_mapper import to_owl_xml


def _owl_text():
    nodes = [
        {"eid": "1", "labels": ["BusinessConcept"], "props": {"name": "Customer"}},
        {"eid": "2", "labels": ["PhysicalTable"], "props": {"table_name": "TB_CST"}},
    ]
    edges = [
        {"eid": "r1", "start_eid": "1", "end_eid": "2",
         "rel_type": "MAPPED_TO", "props": {"confidence": 0.9}},
    ]
    return to_owl_xml(nodes, edges)


class TestImportFromOwlText:
    def test_clean_strategy_clears_then_writes(self) -> None:
        client = MagicMock()
        with patch.object(owl_importer, "Neo4jClient") as mock_client, \
             patch.object(owl_importer, "setup_schema"):
            mock_client.return_value.__enter__.return_value = client
            result = owl_importer.import_from_owl_text(_owl_text(), strategy="clean")
        # DELETE must run before any write
        calls = [c.args[0] for c in client.execute_cypher.call_args_list]
        assert any("DETACH DELETE" in c for c in calls)
        assert client.execute_batch.called
        assert result["nodes_merged"] == 2
        assert result["relationships_merged"] == 1

    def test_merge_strategy_does_not_clear(self) -> None:
        client = MagicMock()
        with patch.object(owl_importer, "Neo4jClient") as mock_client, \
             patch.object(owl_importer, "setup_schema"):
            mock_client.return_value.__enter__.return_value = client
            owl_importer.import_from_owl_text(_owl_text(), strategy="merge")
        calls = [c.args[0] for c in client.execute_cypher.call_args_list]
        assert not any("DETACH DELETE" in c for c in calls)

    def test_versioned_strategy_snapshots_first(self) -> None:
        # save_snapshot is late-imported from kg_registry inside import_from_owl_text,
        # so patch it at its source module.
        client = MagicMock()
        with patch.object(owl_importer, "Neo4jClient") as mock_client, \
             patch.object(owl_importer, "setup_schema"), \
             patch("src.graph.kg_registry.save_snapshot",
                   return_value={"id": "snap-backup-1"}) as save:
            mock_client.return_value.__enter__.return_value = client
            result = owl_importer.import_from_owl_text(_owl_text(), strategy="versioned")
        save.assert_called_once()
        assert result["backup_snapshot_id"] == "snap-backup-1"
        # and it still cleared + wrote
        calls = [c.args[0] for c in client.execute_cypher.call_args_list]
        assert any("DETACH DELETE" in c for c in calls)

    def test_invalid_strategy_raises(self) -> None:
        with pytest.raises(ValueError, match="unsupported_strategy"):
            owl_importer.import_from_owl_text(_owl_text(), strategy="bogus")
