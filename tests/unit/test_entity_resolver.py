"""Unit tests for src/resolution/blocking.py (UT-05) and src/resolution/llm_judge.py (UT-06)."""

from __future__ import annotations

import json
from unittest.mock import MagicMock

from src.models.schemas import CanonicalEntityDecision, EntityCluster, Triplet
from src.resolution.blocking import block_entities, extract_unique_entities
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
    """Mock Embeddings that returns fixed vectors for each entity string."""
    emb = MagicMock()

    def embed_documents(texts: list[str]) -> list[list[float]]:
        return [vectors[t] for t in texts]

    emb.embed_documents.side_effect = embed_documents
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
            subject="  Customer  ", predicate="is", object="  Entity  ",
            provenance_text="x", confidence=0.9,
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
            "Product": [0.0, 1.0],   # orthogonal → different cluster
        }
        emb = _make_embeddings(vectors)
        clusters = block_entities(["Customer", "Customers", "Product"], emb, threshold=0.95)
        # Only "Customer" + "Customers" should cluster
        assert len(clusters) == 1
        assert set(clusters[0].variants) == {"Customer", "Customers"}

    def test_orthogonal_vectors_no_clusters(self) -> None:
        vectors = {
            "Customer": [1.0, 0.0],
            "Product":  [0.0, 1.0],
        }
        emb = _make_embeddings(vectors)
        clusters = block_entities(["Customer", "Product"], emb, threshold=0.95)
        assert clusters == []

    def test_cluster_canonical_is_longest_string(self) -> None:
        vectors = {
            "Cust":      [1.0, 0.0],
            "Customer":  [1.0, 0.0],
            "CUST":      [1.0, 0.0],
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
        subject=subject, predicate="is", object=obj,
        provenance_text=provenance,
        confidence=0.9,
    )


def _make_merge_llm(merge: bool, canonical: str) -> MagicMock:
    llm = MagicMock()
    resp = MagicMock()
    resp.content = json.dumps({
        "merge": merge,
        "canonical_name": canonical,
        "reasoning": "test reasoning",
    })
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
