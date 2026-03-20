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

# ── Fixtures ───────────────────────────────────────────────────────────────────


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


# ── extract_unique_entities ───────────────────────────────────────────────────


class TestExtractUniqueEntities:
    def test_deduplicates_subjects_and_objects(self) -> None:
        triplets = [
            _make_triplet("Customer", "Product"),
            _make_triplet("Customer", "Service"),  # Customer appears again
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


# ── block_entities ────────────────────────────────────────────────────────────


class TestBlockEntities:
    def test_identical_vectors_form_cluster(self) -> None:
        # Two entities with identical embeddings → cosine sim = 1.0
        vectors = {
            "Customer": [1.0, 0.0],
            "Customers": [1.0, 0.0],  # identical → should cluster
            "Product": [0.0, 1.0],  # orthogonal → different cluster
        }
        emb = _make_embeddings(vectors)
        clusters = block_entities(["Customer", "Customers", "Product"], emb, threshold=0.95)
        # Only "Customer" + "Customers" should cluster
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
        assert clusters[0].canonical_candidate == "Customer"  # longest

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


# ── Fixtures for LLM Judge ───────────────────────────────────────────────────────


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


# ── build_provenance_map ─────────────────────────────────────────────────────────


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


# ── judge_cluster ─────────────────────────────────────────────────────────────────


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
        assert decision.merge is False  # conservative

    def test_bad_json_returns_no_merge(self) -> None:
        cluster = _make_cluster("Customer", "Customers")
        llm = MagicMock()
        resp = MagicMock()
        resp.content = "Not JSON"
        llm.invoke.return_value = resp
        decision = judge_cluster(cluster, {}, llm)
        assert decision.merge is False


# ── cluster_to_entity ───────────────────────────────────────────────────────────


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


# ── Fixtures for Entity Resolver ───────────────────────────────────────────────


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


# ── resolve_entities ───────────────────────────────────────────────────────────


class TestResolveEntities:
    def test_empty_triplets_returns_empty(self) -> None:
        emb = MagicMock()
        llm = MagicMock()
        result = resolve_entities([], emb, llm)
        assert result == []

    def test_all_singletons_no_llm_call(self) -> None:
        """Orthogonal embeddings → no clusters → no LLM calls."""
        triplets = [
            _make_triplet_full("Customer", "Product"),
            _make_triplet_full("Order", "Invoice"),
        ]
        entities = ["Customer", "Product", "Order", "Invoice"]
        emb = _make_embeddings_orthogonal(entities)
        llm = MagicMock()
        result = resolve_entities(triplets, emb, llm)
        llm.invoke.assert_not_called()
        assert len(result) == 4  # all promoted as singletons

    def test_cluster_resolved_to_single_entity(self) -> None:
        """Identical embeddings → one big cluster → LLM merges to 'Customer'."""
        triplets = [
            _make_triplet_full("Customer", "CUST"),
            _make_triplet_full("Customers", "Product"),
        ]
        emb = _make_embeddings_identical(["Customer", "CUST", "Customers", "Product"])
        llm = _make_llm_merge("Customer")
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
        # Conservative no-merge → cluster preserved but not crashed
        assert len(result) >= 1


# ── Regression: zero-vector embeddings produce zero clusters ──────────────────
# This documents Bug 3: _MockEmbeddings returned [0.0]*1024 for all entities.
# cosine_similarity([0,0,...], [0,0,...]) → NaN/0 → no pair exceeds threshold
# → 0 clusters → ER is completely blind.


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
            "Customers": [1.0, 0.0, 0.0, 0.0],  # identical → should cluster
            "Order": [0.0, 1.0, 0.0, 0.0],  # orthogonal → no cluster
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

        # _MockEmbeddings and _get_embeddings must not exist in the module
        assert not hasattr(bg, "_MockEmbeddings"), (
            "_MockEmbeddings still present in builder_graph — Bug 3 not fixed"
        )
        assert not hasattr(bg, "_get_embeddings"), (
            "_get_embeddings still present in builder_graph — Bug 3 not fixed"
        )
