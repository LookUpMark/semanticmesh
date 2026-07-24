"""Unit tests for src.graph.owl_mapper — pure dict↔RDF mapping, no Neo4j."""

from __future__ import annotations

from rdflib import Graph, Literal
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


class TestEdgeToRdf:
    def test_known_edge_emits_predicate(self) -> None:
        eid_to_uri = {
            "1": owl_mapper.SM["concept/Customer"],
            "2": owl_mapper.SM["table/TB_CST"],
        }
        edge = {
            "eid": "r1",
            "start_eid": "1",
            "end_eid": "2",
            "rel_type": "MAPPED_TO",
            "props": {"confidence": 0.9},
        }
        g = Graph()
        ok = owl_mapper.edge_to_rdf(edge, g, eid_to_uri)
        assert ok is True
        assert (
            owl_mapper.SM["concept/Customer"],
            owl_mapper.SM.MAPPED_TO,
            owl_mapper.SM["table/TB_CST"],
        ) in g

    def test_unknown_rel_type_skipped(self) -> None:
        eid_to_uri = {"1": owl_mapper.SM["concept/A"], "2": owl_mapper.SM["table/B"]}
        edge = {"start_eid": "1", "end_eid": "2", "rel_type": "WEIRD", "props": {}}
        g = Graph()
        assert owl_mapper.edge_to_rdf(edge, g, eid_to_uri) is False
        assert len(g) == 0

    def test_missing_endpoint_skipped(self) -> None:
        eid_to_uri = {"1": owl_mapper.SM["concept/A"]}  # endpoint 2 unknown
        edge = {"start_eid": "1", "end_eid": "2", "rel_type": "MAPPED_TO", "props": {}}
        g = Graph()
        assert owl_mapper.edge_to_rdf(edge, g, eid_to_uri) is False

    def test_edge_props_attached_as_reification(self) -> None:
        eid_to_uri = {"1": owl_mapper.SM["concept/A"], "2": owl_mapper.SM["table/B"]}
        edge = {
            "start_eid": "1",
            "end_eid": "2",
            "rel_type": "MAPPED_TO",
            "props": {"confidence": 0.9},
        }
        g = Graph()
        owl_mapper.edge_to_rdf(edge, g, eid_to_uri)
        # confidence lives on the reified statement
        assert (None, owl_mapper.SM["confidence"], Literal(0.9)) in g


class TestRoundTrip:
    def test_serialize_and_parse_roundtrips_nodes(self) -> None:
        nodes = [
            {
                "eid": "1",
                "labels": ["BusinessConcept"],
                "props": {"name": "Customer", "definition": "A buyer", "synonyms": ["Client"]},
            },
            {
                "eid": "2",
                "labels": ["PhysicalTable"],
                "props": {"table_name": "TB_CST", "ddl_source": "CREATE TABLE TB_CST (id INT)"},
            },
        ]
        edges: list[dict] = []
        text = owl_mapper.to_owl_xml(nodes, edges)
        out_nodes, out_edges = owl_mapper.from_owl_xml(text)
        assert len(out_nodes) == 2
        names = {n["props"].get("name") or n["props"].get("table_name") for n in out_nodes}
        assert names == {"Customer", "TB_CST"}

    def test_roundtrip_preserves_definition_and_synonyms(self) -> None:
        nodes = [
            {
                "eid": "1",
                "labels": ["BusinessConcept"],
                "props": {
                    "name": "Order",
                    "definition": "A purchase",
                    "synonyms": ["Purchase", "Sale"],
                },
            }
        ]
        text = owl_mapper.to_owl_xml(nodes, edges=[])
        out_nodes, _ = owl_mapper.from_owl_xml(text)
        bc = [n for n in out_nodes if "BusinessConcept" in n["labels"]][0]
        assert bc["props"]["definition"] == "A purchase"
        assert set(bc["props"]["synonyms"]) == {"Purchase", "Sale"}

    def test_roundtrip_edges_with_props(self) -> None:
        nodes = [
            {"eid": "1", "labels": ["BusinessConcept"], "props": {"name": "Customer"}},
            {"eid": "2", "labels": ["PhysicalTable"], "props": {"table_name": "TB_CST"}},
        ]
        edges = [
            {"eid": "r1", "start_eid": "1", "end_eid": "2", "rel_type": "MAPPED_TO",
             "props": {"confidence": 0.9}},
        ]
        text = owl_mapper.to_owl_xml(nodes, edges)
        out_nodes, out_edges = owl_mapper.from_owl_xml(text)
        assert len(out_edges) == 1
        e = out_edges[0]
        assert e["rel_type"] == "MAPPED_TO"
        assert e["props"]["confidence"] == 0.9

    def test_roundtrip_slashes_in_paths_and_special_chars(self) -> None:
        # Real-world guard: SourceFile paths and Chunk source_doc contain "/",
        # and names may contain special chars. The sm: URI must encode "/" so
        # the segment separator stays unambiguous on parse.
        nodes = [
            {"eid": "1", "labels": ["SourceFile"], "props": {"path": "src/data/docs/guide.pdf"}},
            {"eid": "2", "labels": ["Chunk"],
             "props": {"chunk_index": 7, "source_doc": "sub/dir/guide.pdf"}},
            {"eid": "3", "labels": ["BusinessConcept"],
             "props": {"name": "A/B #1 & Co", "definition": "x"}},
        ]
        text = owl_mapper.to_owl_xml(nodes, edges=[])
        out_nodes, _ = owl_mapper.from_owl_xml(text)
        by_label = {tuple(n["labels"]): n["props"] for n in out_nodes}
        assert by_label[("SourceFile",)]["path"] == "src/data/docs/guide.pdf"
        chunk = by_label[("Chunk",)]
        assert chunk["chunk_index"] == 7
        assert isinstance(chunk["chunk_index"], int)
        assert chunk["source_doc"] == "sub/dir/guide.pdf"
        assert by_label[("BusinessConcept",)]["name"] == "A/B #1 & Co"

    def test_from_owl_documents_merges_multiple_xml_files(self) -> None:
        # An export produces 4 complete XML documents. Concatenating their text
        # is invalid XML; from_owl_documents must parse each and union the triples.
        doc1 = owl_mapper.to_owl_xml(
            [{"eid": "1", "labels": ["BusinessConcept"], "props": {"name": "Customer"}}],
            edges=[],
        )
        doc2 = owl_mapper.to_owl_xml(
            [{"eid": "2", "labels": ["PhysicalTable"], "props": {"table_name": "TB_CST"}}],
            edges=[],
        )
        out_nodes, _ = owl_mapper.from_owl_documents([doc1, doc2])
        names = {n["props"].get("name") or n["props"].get("table_name") for n in out_nodes}
        assert names == {"Customer", "TB_CST"}

    def test_non_synonyms_list_prop_roundtrips_as_list(self) -> None:
        # Any list-typed prop (not just synonyms) must survive round-trip as a
        # list — a backup tool must not silently drop multi-value data.
        nodes = [
            {"eid": "1", "labels": ["BusinessConcept"],
             "props": {"name": "Order", "tags": ["urgent", "intl", "b2b"]}},
        ]
        text = owl_mapper.to_owl_xml(nodes, edges=[])
        out_nodes, _ = owl_mapper.from_owl_xml(text)
        # RDF triples are set-backed, so multi-value order is not preserved —
        # the data is what matters.
        assert set(out_nodes[0]["props"]["tags"]) == {"urgent", "intl", "b2b"}


