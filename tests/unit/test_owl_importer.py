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

    def test_two_single_key_endpoints_params_do_not_collide(self) -> None:
        # Regression: both endpoints are single-key nodes using $key. The rel
        # builder must namespace params (a_key / b_key) so they survive the merge
        # into one param dict — otherwise tgt overwrites src and the MATCH fails.
        client = MagicMock()
        with patch.object(owl_importer, "Neo4jClient") as mock_client, \
             patch.object(owl_importer, "setup_schema"):
            mock_client.return_value.__enter__.return_value = client
            owl_importer.import_from_owl_text(_owl_text(), strategy="clean")
        # The second execute_batch call carries the relationship statements.
        rel_batch = client.execute_batch.call_args_list[-1].args[0]
        assert len(rel_batch) == 1
        cypher, params = rel_batch[0]
        assert params["a_key"] == "Customer"
        assert params["b_key"] == "TB_CST"
        assert "$a_key" in cypher and "$b_key" in cypher

    def test_duplicate_pair_edges_distinguished_by_props(self) -> None:
        # Regression (DS07): two REFERENCES edges A→B with different FK columns
        # must get distinct MERGE patterns, else Neo4j collapses them into one
        # relationship. The distinguishing props go INSIDE [r:TYPE {...}].
        from src.graph.owl_mapper import to_owl_xml

        nodes = [
            {"eid": "1", "labels": ["PhysicalTable"], "props": {"table_name": "A"}},
            {"eid": "2", "labels": ["PhysicalTable"], "props": {"table_name": "B"}},
        ]
        edges = [
            {"eid": "r1", "start_eid": "1", "end_eid": "2", "rel_type": "REFERENCES",
             "props": {"column": "fk_a", "references_column": "id"}},
            {"eid": "r2", "start_eid": "1", "end_eid": "2", "rel_type": "REFERENCES",
             "props": {"column": "fk_b", "references_column": "id"}},
        ]
        client = MagicMock()
        with patch.object(owl_importer, "Neo4jClient") as mock_client, \
             patch.object(owl_importer, "setup_schema"):
            mock_client.return_value.__enter__.return_value = client
            owl_importer.import_from_owl_text(to_owl_xml(nodes, edges), strategy="clean")
        rel_batch = client.execute_batch.call_args_list[-1].args[0]
        assert len(rel_batch) == 2
        patterns = {cypher for cypher, _ in rel_batch}
        # both the distinguishing column params must appear, inside the rel brackets
        assert any("$rp_column" in c and "fk_a" not in c for c in patterns)
        assert all("$rp_column" in c for c in patterns)  # prop pattern present
        params_list = [p for _, p in rel_batch]
        assert {p["rp_column"] for p in params_list} == {"fk_a", "fk_b"}

