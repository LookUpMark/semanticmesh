"""Integration test: build a tiny KG, export to OWL, re-import losslessly.

Requires a live Neo4j reachable via the project settings (NEO4J_URI/USER/PASSWORD).
Skipped in the default unit run via the ``integration`` marker:

    .venv/bin/python -m pytest tests/integration/test_owl_flow.py -m integration -q
"""

from __future__ import annotations

import pytest

pytestmark = pytest.mark.integration


@pytest.fixture()
def clean_graph():
    from src.graph.neo4j_client import Neo4jClient

    with Neo4jClient() as client:
        client.execute_cypher("MATCH (n) DETACH DELETE n")
        yield client
        client.execute_cypher("MATCH (n) DETACH DELETE n")


def test_export_then_import_roundtrip(clean_graph) -> None:
    from src.graph.neo4j_client import Neo4jClient, setup_schema

    # Seed: one BusinessConcept + one PhysicalTable + MAPPED_TO edge.
    with Neo4jClient() as client:
        setup_schema(client)
        client.execute_batch([
            ("MERGE (bc:BusinessConcept {name: $name}) "
             "SET bc.definition = $def, bc.synonyms = $syn",
             {"name": "Customer", "def": "A buyer", "syn": ["Client"]}),
            ("MERGE (pt:PhysicalTable {table_name: $tn}) "
             "SET pt.ddl_source = $ddl",
             {"tn": "TB_CST", "ddl": "CREATE TABLE TB_CST (id INT)"}),
            ("MATCH (bc:BusinessConcept {name: 'Customer'}), "
             "(pt:PhysicalTable {table_name: 'TB_CST'}) "
             "MERGE (bc)-[:MAPPED_TO]->(pt)",
             {}),
        ])

    # Export
    from src.graph.owl_exporter import export_dir, export_to_owl_files

    meta = export_to_owl_files()
    assert meta["nodes_count"] >= 2
    assert meta["relationships_count"] >= 1

    # Read exported OWL, wipe graph, re-import clean.
    directory = export_dir(meta["export_id"])
    owl_texts = [p.read_text() for p in directory.glob("*.owl")]

    from src.graph.owl_importer import import_from_owl_text

    result = import_from_owl_text(owl_texts, strategy="clean")
    assert result["nodes_merged"] >= 2
    assert result["relationships_merged"] >= 1

    # Verify restored nodes + edge.
    with Neo4jClient() as client:
        bc = client.execute_cypher(
            "MATCH (bc:BusinessConcept {name: 'Customer'}) RETURN bc.definition AS d"
        )
        assert bc and bc[0]["d"] == "A buyer"
        rel = client.execute_cypher(
            "MATCH (:BusinessConcept {name: 'Customer'})-[:MAPPED_TO]->"
            "(pt:PhysicalTable {table_name: 'TB_CST'}) RETURN count(*) AS c"
        )
        assert rel[0]["c"] == 1
