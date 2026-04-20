"""Unit tests for src/resolution/blocking.py (UT-05), src/resolution/llm_judge.py (UT-06),
and src/resolution/entity_resolver.py (UT-06).
"""

from __future__ import annotations

import json
from unittest.mock import MagicMock, patch

import numpy as np

from src.models.schemas import CanonicalEntityDecision, Entity, EntityCluster, Triplet
from src.resolution.blocking import block_entities, extract_unique_entities
from src.resolution.entity_resolver import resolve_entities
from src.resolution.llm_judge import (
    build_provenance_map,
    cluster_to_entity,
    judge_cluster,
)


def _make_triplet(subject: str, obj: str, confidence: float = 0.9) -> Triplet:
    return Triplet(
        subject=subject,
        predicate="is",
        object=obj,
        provenance_text=f"{subject} is {obj}.",
        confidence=confidence,
    )


def _make_embeddings(vectors: dict[str, list[float]]) -> MagicMock:
    """Mock embedder that returns fixed vectors for each entity string."""
    emb = MagicMock()
    emb.encode.side_effect = lambda texts, **kw: np.array([vectors[t] for t in texts])
    return emb


class TestExtractUniqueEntities:
    def test_deduplicates_subjects_and_objects(self) -> None:
        triplets = [
            _make_triplet("Customer", "Product"),
            _make_triplet("Customer", "Service"),
        ]
        result = extract_unique_entities(triplets)
        assert result.count("Customer") == 1

    def test_returns_sorted_list(self) -> None:
        triplets = [_make_triplet("Zebra", "Apple")]
        result = extract_unique_entities(triplets)
        assert result == sorted(result)

    def test_empty_triplets_returns_empty(self) -> None:
        assert extract_unique_entities([]) == []

    def test_strips_whitespace(self) -> None:
        t = Triplet(
            subject="  Customer  ",
            predicate="is",
            object="  Entity  ",
            provenance_text="x",
            confidence=0.9,
        )
        result = extract_unique_entities([t])
        assert "Customer" in result
        assert "Entity" in result


class TestBlockEntities:
    def test_identical_vectors_form_cluster(self) -> None:
        vectors = {
            "Customer": [1.0, 0.0],
            "Customers": [1.0, 0.0],
            "Product": [0.0, 1.0],
        }
        emb = _make_embeddings(vectors)
        clusters = block_entities(["Customer", "Customers", "Product"], emb, threshold=0.95)
        assert len(clusters) == 1
        assert set(clusters[0].variants) == {"Customer", "Customers"}

    def test_orthogonal_vectors_no_clusters(self) -> None:
        vectors = {
            "Customer": [1.0, 0.0],
            "Product": [0.0, 1.0],
        }
        emb = _make_embeddings(vectors)
        clusters = block_entities(["Customer", "Product"], emb, threshold=0.95)
        assert clusters == []

    def test_cluster_canonical_is_longest_string(self) -> None:
        vectors = {
            "Cust": [1.0, 0.0],
            "Customer": [1.0, 0.0],
            "CUST": [1.0, 0.0],
        }
        emb = _make_embeddings(vectors)
        clusters = block_entities(["Cust", "Customer", "CUST"], emb, threshold=0.95)
        assert len(clusters) == 1
        assert clusters[0].canonical_candidate == "Customer"

    def test_empty_entities_returns_empty(self) -> None:
        emb = MagicMock()
        result = block_entities([], emb)
        assert result == []

    def test_avg_similarity_in_range(self) -> None:
        vectors = {
            "Customer": [1.0, 0.0],
            "Customers": [0.99, 0.14],
        }
        emb = _make_embeddings(vectors)
        clusters = block_entities(["Customer", "Customers"], emb, threshold=0.9)
        if clusters:
            assert 0.0 <= clusters[0].avg_similarity <= 1.0


def _make_cluster(*variants: str) -> EntityCluster:
    return EntityCluster(
        canonical_candidate=max(variants, key=len),
        variants=list(variants),
        avg_similarity=0.95,
    )


def _make_triplet_with_provenance(subject: str, obj: str, provenance: str) -> Triplet:
    return Triplet(
        subject=subject,
        predicate="is",
        object=obj,
        provenance_text=provenance,
        confidence=0.9,
    )


def _make_merge_llm(merge: bool, canonical: str) -> MagicMock:
    llm = MagicMock()
    resp = MagicMock()
    resp.content = json.dumps(
        {
            "merge": merge,
            "canonical_name": canonical,
            "reasoning": "test reasoning",
        }
    )
    llm.invoke.return_value = resp
    return llm


class TestBuildProvenanceMap:
    def test_maps_subjects_and_objects(self) -> None:
        triplets = [
            _make_triplet_with_provenance("Customer", "Product", "A Customer buys a Product."),
        ]
        pmap = build_provenance_map(triplets)
        assert "Customer" in pmap
        assert "Product" in pmap
        assert "A Customer buys a Product." in pmap["Customer"]

    def test_multiple_triplets_accumulate_provenance(self) -> None:
        t1 = _make_triplet_with_provenance("Customer", "Order", "Customer places an Order.")
        t2 = _make_triplet_with_provenance("Customer", "Invoice", "Customer receives an Invoice.")
        pmap = build_provenance_map([t1, t2])
        assert len(pmap["Customer"]) == 2

    def test_empty_returns_empty_dict(self) -> None:
        assert build_provenance_map([]) == {}


class TestJudgeCluster:
    @patch("src.resolution.llm_judge.get_settings")
    def test_lazy_mode_uses_threshold_no_llm(self, mock_get_settings) -> None:
        cluster = EntityCluster(
            canonical_candidate="Customer",
            variants=["Customer", "Customers"],
            avg_similarity=0.91,
        )
        mock_get_settings.return_value = MagicMock(
            use_lazy_extraction=True,
            er_judge_threshold=0.80,
            max_reflection_attempts=3,
        )
        llm = MagicMock()

        decision = judge_cluster(cluster, {}, llm)

        assert decision.merge is True
        assert decision.canonical_name == "Customer"
        llm.invoke.assert_not_called()

    def test_merge_true_decision(self) -> None:
        cluster = _make_cluster("Customer", "Customers")
        pmap = {"Customer": ["A Customer buys things."], "Customers": ["Customers are registered."]}
        llm = _make_merge_llm(merge=True, canonical="Customer")
        decision = judge_cluster(cluster, pmap, llm)
        assert decision.merge is True
        assert decision.canonical_name == "Customer"

    def test_merge_false_decision(self) -> None:
        cluster = _make_cluster("Apple (company)", "Apple (fruit)")
        pmap: dict[str, list[str]] = {}
        llm = _make_merge_llm(merge=False, canonical="Apple (company)")
        decision = judge_cluster(cluster, pmap, llm)
        assert decision.merge is False

    def test_llm_error_returns_conservative_no_merge(self) -> None:
        cluster = _make_cluster("Customer", "Customers")
        llm = MagicMock()
        llm.invoke.side_effect = RuntimeError("timeout")
        decision = judge_cluster(cluster, {}, llm)
        assert decision.merge is False

    def test_bad_json_returns_no_merge(self) -> None:
        cluster = _make_cluster("Customer", "Customers")
        llm = MagicMock()
        resp = MagicMock()
        resp.content = "Not JSON"
        llm.invoke.return_value = resp
        decision = judge_cluster(cluster, {}, llm)
        assert decision.merge is False


class TestClusterToEntity:
    def test_canonical_name_from_decision(self) -> None:
        cluster = _make_cluster("Cust", "Customer", "CUST")
        decision = CanonicalEntityDecision(merge=True, canonical_name="Customer", reasoning="ok")
        entity = cluster_to_entity(cluster, decision, {})
        assert entity.name == "Customer"

    def test_synonyms_exclude_canonical(self) -> None:
        cluster = _make_cluster("Cust", "Customer")
        decision = CanonicalEntityDecision(merge=True, canonical_name="Customer", reasoning="ok")
        entity = cluster_to_entity(cluster, decision, {})
        assert "Customer" not in entity.synonyms
        assert "Cust" in entity.synonyms

    def test_provenance_aggregated_from_all_variants(self) -> None:
        cluster = _make_cluster("Customer", "CUST")
        decision = CanonicalEntityDecision(merge=True, canonical_name="Customer", reasoning="ok")
        pmap = {
            "Customer": ["A Customer is a buyer."],
            "CUST": ["CUST table stores customer data."],
        }
        entity = cluster_to_entity(cluster, decision, pmap)
        assert "A Customer is a buyer." in entity.provenance_text
        assert "CUST table stores" in entity.provenance_text

    def test_no_merge_uses_canonical_candidate(self) -> None:
        cluster = _make_cluster("Apple company", "Apple fruit")
        decision = CanonicalEntityDecision(
            merge=False, canonical_name="Apple company", reasoning="different contexts"
        )
        entity = cluster_to_entity(cluster, decision, {})
        assert entity.name == "Apple company"


def _make_triplet_full(subject: str, obj: str, prov: str = "") -> Triplet:
    return Triplet(
        subject=subject,
        predicate="is",
        object=obj,
        provenance_text=prov or f"{subject} is {obj}.",
        confidence=0.9,
    )


def _make_embeddings_orthogonal(entities: list[str]) -> MagicMock:
    """Each entity gets a unique orthogonal unit vector — no clusters form."""
    emb = MagicMock()
    dim = max(len(entities), 2)

    def encode(texts: list[str], **kw: object) -> np.ndarray:
        vecs = []
        for i, _t in enumerate(texts):
            v = [0.0] * dim
            v[i % dim] = 1.0
            vecs.append(v)
        return np.array(vecs)

    emb.encode.side_effect = encode
    return emb


def _make_embeddings_identical(entities: list[str]) -> MagicMock:
    """All entities share the same vector — max clustering."""
    emb = MagicMock()
    emb.encode.side_effect = lambda texts, **kw: np.array([[1.0, 0.0]] * len(texts))
    return emb


def _make_llm_merge(canonical: str) -> MagicMock:
    llm = MagicMock()
    resp = MagicMock()
    resp.content = json.dumps({"merge": True, "canonical_name": canonical, "reasoning": "test"})
    llm.invoke.return_value = resp
    return llm


def _make_llm_no_merge(canonical: str) -> MagicMock:
    llm = MagicMock()
    resp = MagicMock()
    resp.content = json.dumps({"merge": False, "canonical_name": canonical, "reasoning": "test"})
    llm.invoke.return_value = resp
    return llm


class TestResolveEntities:
    def test_empty_triplets_returns_empty(self) -> None:
        emb = MagicMock()
        llm = MagicMock()
        result = resolve_entities([], emb, llm)
        assert result == []

    @patch("src.resolution.entity_resolver.get_settings")
    def test_all_singletons_llm_called_for_definitions(self, mock_get_settings) -> None:
        """Orthogonal embeddings → no clusters → LLM called for singleton definition synthesis."""
        mock_get_settings.return_value = MagicMock(
            enable_singleton_llm_definitions=True,
            extraction_concurrency=5,
        )
        triplets = [
            _make_triplet_full("Customer", "Product"),
            _make_triplet_full("Order", "Invoice"),
        ]
        entities = ["Customer", "Product", "Order", "Invoice"]
        emb = _make_embeddings_orthogonal(entities)
        llm = MagicMock()
        # Simulate LLM returning a valid definition JSON for each singleton
        llm.invoke.return_value = MagicMock(content='{"definition": "A business entity."}')
        result = resolve_entities(triplets, emb, llm)
        # LLM is called once per singleton that has provenance texts
        assert llm.invoke.call_count >= 1
        assert len(result) == 4

    @patch("src.resolution.entity_resolver.get_settings")
    @patch("src.config.llm_factory.get_midtier_llm")
    def test_cluster_resolved_to_single_entity(self, mock_get_midtier, mock_get_settings) -> None:
        """Identical embeddings → one big cluster → LLM merges to 'Customer'."""
        mock_get_settings.return_value = MagicMock(
            extraction_concurrency=5,
            enable_singleton_llm_definitions=False,
        )
        judge_llm = _make_llm_merge("Customer")
        mock_get_midtier.return_value = judge_llm
        triplets = [
            _make_triplet_full("Customer", "CUST"),
            _make_triplet_full("Customers", "Product"),
        ]
        emb = _make_embeddings_identical(["Customer", "CUST", "Customers", "Product"])
        llm = MagicMock()  # passed but not used for judge (code uses get_midtier_llm)
        result = resolve_entities(triplets, emb, llm)
        assert any(e.name == "Customer" for e in result)

    def test_returns_entity_objects(self) -> None:
        triplets = [_make_triplet_full("Customer", "Product")]
        emb = _make_embeddings_orthogonal(["Customer", "Product"])
        llm = MagicMock()
        result = resolve_entities(triplets, emb, llm)
        assert all(isinstance(e, Entity) for e in result)

    def test_source_doc_set_on_entities(self) -> None:
        triplets = [_make_triplet_full("Customer", "Order")]
        emb = _make_embeddings_orthogonal(["Customer", "Order"])
        llm = MagicMock()
        result = resolve_entities(triplets, emb, llm, source_doc="glossary.pdf")
        for entity in result:
            assert entity.source_doc == "glossary.pdf"

    def test_llm_failure_in_judge_does_not_crash(self) -> None:
        """If LLM judge fails for one cluster, pipeline continues."""
        triplets = [_make_triplet_full("Customer", "CUST")]
        emb = _make_embeddings_identical(["Customer", "CUST"])
        llm = MagicMock()
        llm.invoke.side_effect = RuntimeError("timeout")
        result = resolve_entities(triplets, emb, llm)
        assert len(result) >= 1


class TestZeroVectorRegressionBug3:
    """Regression guard for the mock-embeddings bug in entity resolution.

    When all embedding vectors are zero, cosine similarity is undefined (0/0)
    and sklearn returns 0.0 for all pairs. No pair exceeds the blocking
    threshold, so entity resolution produces 0 clusters regardless of how
    semantically similar the entity strings are.

    Real BGE-M3 embeddings produce unit-norm vectors where cosine similarity
    correctly reflects semantic similarity.
    """

    def _make_zero_embeddings(self) -> MagicMock:
        emb = MagicMock()
        emb.encode.side_effect = lambda texts, **kw: np.array([[0.0] * 4 for _ in texts])
        return emb

    def _make_similar_embeddings(self) -> MagicMock:
        """'Customer' and 'Customers' share the same vector — cos sim = 1.0."""
        emb = MagicMock()
        vectors = {
            "Customer": [1.0, 0.0, 0.0, 0.0],
            "Customers": [1.0, 0.0, 0.0, 0.0],
            "Order": [0.0, 1.0, 0.0, 0.0],
        }
        emb.encode.side_effect = lambda texts, **kw: np.array([vectors[t] for t in texts])
        return emb

    def test_zero_vectors_produce_zero_clusters(self) -> None:
        """Demonstrates the original bug: zero vectors → no clusters ever form."""
        entities = ["Customer", "Customers", "Order"]
        clusters = block_entities(entities, self._make_zero_embeddings(), threshold=0.85)
        assert clusters == [], "Zero vectors must produce 0 clusters (bug demonstration)"

    def test_real_similar_vectors_produce_clusters(self) -> None:
        """Fix verification: meaningful vectors → similar entities cluster correctly."""
        entities = ["Customer", "Customers", "Order"]
        clusters = block_entities(entities, self._make_similar_embeddings(), threshold=0.85)
        assert len(clusters) == 1
        assert set(clusters[0].variants) == {"Customer", "Customers"}

    def test_node_entity_resolution_calls_get_embeddings_not_mock(self) -> None:
        """Regression: _node_entity_resolution must use get_embeddings(), not _MockEmbeddings."""
        import src.graph.builder_graph as bg

        assert not hasattr(bg, "_MockEmbeddings"), (
            "_MockEmbeddings still present in builder_graph — Bug 3 not fixed"
        )
        assert not hasattr(bg, "_get_embeddings"), (
            "_get_embeddings still present in builder_graph — Bug 3 not fixed"
        )
