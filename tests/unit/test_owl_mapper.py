"""Unit tests for src.graph.owl_mapper — pure dict↔RDF mapping, no Neo4j."""

from __future__ import annotations

from rdflib import Graph, Literal, URIRef
from rdflib.namespace import RDF, RDFS, SKOS

from src.graph import owl_mapper


class TestNodeToRdf:
    def test_business_concept_mapped_to_sm_concept(self) -> None:
        node = {
            "eid": "1",
            "labels": ["BusinessConcept"],
            "props": {"name": "Customer", "definition": "A buyer", "synonyms": ["Client"]},
        }
        g = Graph()
        uri = owl_mapper.node_to_rdf(node, g)
        assert uri is not None
        assert uri == owl_mapper.SM["concept/Customer"]
        assert (uri, RDF.type, owl_mapper.SM.Concept) in g
        assert (uri, RDFS.label, Literal("Customer")) in g
        assert (uri, SKOS.definition, Literal("A buyer")) in g
        assert (uri, SKOS.altLabel, Literal("Client")) in g

    def test_physical_table_uses_table_name_key(self) -> None:
        node = {
            "eid": "2",
            "labels": ["PhysicalTable"],
            "props": {"table_name": "TB_CST", "ddl_source": "CREATE TABLE..."},
        }
        g = Graph()
        uri = owl_mapper.node_to_rdf(node, g)
        assert uri == owl_mapper.SM["table/TB_CST"]
        assert (uri, RDF.type, owl_mapper.SM.PhysicalTable) in g
        # unknown props land in the sm: namespace, lossless
        assert (uri, owl_mapper.SM["ddl_source"], Literal("CREATE TABLE...")) in g

    def test_compound_key_chunk_uri(self) -> None:
        node = {
            "eid": "3",
            "labels": ["Chunk"],
            "props": {"chunk_index": 4, "source_doc": "guide.pdf"},
        }
        g = Graph()
        uri = owl_mapper.node_to_rdf(node, g)
        assert uri == owl_mapper.SM["chunk/4/guide.pdf"]

    def test_embedding_dropped_by_default(self) -> None:
        node = {
            "eid": "4",
            "labels": ["BusinessConcept"],
            "props": {"name": "X", "embedding": [0.1, 0.2]},
        }
        g = Graph()
        owl_mapper.node_to_rdf(node, g)
        assert (None, owl_mapper.SM.embedding, None) not in g

    def test_embedding_kept_when_flag_set(self) -> None:
        node = {
            "eid": "4",
            "labels": ["BusinessConcept"],
            "props": {"name": "X", "embedding": [0.1, 0.2]},
        }
        g = Graph()
        owl_mapper.node_to_rdf(node, g, include_embeddings=True)
        assert (None, owl_mapper.SM["embedding"], None) in g

    def test_unknown_label_returns_none(self) -> None:
        node = {"eid": "5", "labels": ["Mystery"], "props": {"name": "X"}}
        g = Graph()
        assert owl_mapper.node_to_rdf(node, g) is None

    def test_missing_key_returns_none(self) -> None:
        node = {"eid": "6", "labels": ["BusinessConcept"], "props": {}}
        g = Graph()
        assert owl_mapper.node_to_rdf(node, g) is None
