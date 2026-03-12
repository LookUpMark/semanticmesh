"""Unit tests for src/resolution/blocking.py — UT-05 (Stage 1)"""

from __future__ import annotations

from unittest.mock import MagicMock

from src.models.schemas import Triplet
from src.resolution.blocking import block_entities, extract_unique_entities

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
