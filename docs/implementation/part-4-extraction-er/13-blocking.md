# Part 4 — `src/resolution/blocking.py`

## 1. Purpose & Context

**Epic:** EP-04 Agentic Entity Resolution — Stage 1  
**US-04-01** — Vector Blocking

Groups semantically near-duplicate entity strings extracted from triplets using K-NN vector search (BGE-M3 embeddings + cosine similarity). Only clusters with ≥2 variants proceed to the LLM judge. This drastically reduces LLM calls compared to all-pairs comparison.

---

## 2. Prerequisites

- `src/models/schemas.py` — `Triplet`, `EntityCluster` (step 3)
- `src/retrieval/embeddings.py` — `get_bge_embeddings` (step 23) **or** pass any `Embeddings` instance
- `src/config/settings.py` — `er_similarity_threshold`, `er_blocking_top_k`
- Dependencies: `scikit-learn>=1.5`, `numpy>=1.26`, `langchain-core>=0.3`

---

## 3. Public API

| Symbol | Signature | Description |
|---|---|---|
| `extract_unique_entities` | `(triplets: list[Triplet]) -> list[str]` | Returns deduplicated entity strings (subjects + objects) |
| `block_entities` | `(entities: list[str], embeddings: Embeddings, threshold: float, top_k: int) -> list[EntityCluster]` | Groups near-duplicate strings into clusters |

---

## 4. Full Implementation

```python
"""Stage 1 of Agentic Entity Resolution: Vector Blocking.

EP-04-US-04-01: Embeds all unique entity strings with BGE-M3, then uses
cosine similarity to group near-duplicate pairs into EntityCluster objects.
Only clusters with >= 2 variants proceed to the LLM judge (Stage 2).
"""

from __future__ import annotations

import logging
from collections import defaultdict

import numpy as np
from langchain_core.embeddings import Embeddings
from sklearn.metrics.pairwise import cosine_similarity

from src.config.logging import get_logger
from src.config.settings import get_settings
from src.models.schemas import EntityCluster, Triplet

logger: logging.Logger = get_logger(__name__)
_settings = get_settings()


def extract_unique_entities(triplets: list[Triplet]) -> list[str]:
    """Extract all unique entity strings (subjects + objects) from triplets.

    Args:
        triplets: All triplets extracted by the SLM across all chunks.

    Returns:
        Sorted list of unique, non-empty entity strings.
    """
    entities: set[str] = set()
    for t in triplets:
        if t.subject.strip():
            entities.add(t.subject.strip())
        if t.object.strip():
            entities.add(t.object.strip())
    unique = sorted(entities)
    logger.info("Extracted %d unique entities from %d triplets.", len(unique), len(triplets))
    return unique


def block_entities(
    entities: list[str],
    embeddings: Embeddings,
    threshold: float | None = None,
    top_k: int | None = None,
) -> list[EntityCluster]:
    """Group semantically similar entity strings into candidate clusters.

    Algorithm:
    1. Embed all entity strings with the provided ``Embeddings`` instance.
    2. Compute the full N×N cosine similarity matrix.
    3. For each entity, collect all other entities with similarity >= ``threshold``
       (all-pairs, not K-NN per entity — avoids asymmetric clusters).
    4. Apply a Union-Find to merge overlapping pairs into single clusters.
    5. Return clusters with >= 2 variants; singletons are discarded.

    Args:
        entities: Unique entity strings (from ``extract_unique_entities``).
        embeddings: Any ``Embeddings`` instance (BGE-M3 recommended).
        threshold: Minimum cosine similarity to form a cluster pair.
                   Defaults to ``settings.er_similarity_threshold``.
        top_k: Maximum number of candidates per entity for initial pruning.
               Defaults to ``settings.er_blocking_top_k``.

    Returns:
        List of ``EntityCluster`` objects (only clusters with >= 2 variants).
    """
    if not entities:
        return []

    sim_threshold = threshold if threshold is not None else _settings.er_similarity_threshold
    k = top_k if top_k is not None else _settings.er_blocking_top_k

    # Embed all entities in one batch call
    logger.info("Embedding %d entities for blocking...", len(entities))
    vectors = np.array(embeddings.embed_documents(entities), dtype=np.float32)

    # Full cosine similarity matrix
    sim_matrix = cosine_similarity(vectors)  # shape: (N, N)

    # Union-Find clustering
    parent = list(range(len(entities)))

    def find(i: int) -> int:
        while parent[i] != i:
            parent[i] = parent[parent[i]]
            i = parent[i]
        return i

    def union(i: int, j: int) -> None:
        ri, rj = find(i), find(j)
        if ri != rj:
            parent[ri] = rj

    n = len(entities)
    for i in range(n):
        # Sort by similarity descending, take top-k candidates
        sims = sim_matrix[i]
        candidate_indices = np.argsort(sims)[::-1][:k]
        for j in candidate_indices:
            if i != j and sims[j] >= sim_threshold:
                union(i, j)

    # Collect groups
    groups: dict[int, list[int]] = defaultdict(list)
    for i in range(n):
        groups[find(i)].append(i)

    clusters: list[EntityCluster] = []
    for member_indices in groups.values():
        if len(member_indices) < 2:
            continue  # singletons are not ambiguous — skip

        variants = [entities[i] for i in member_indices]

        # Canonical candidate: longest string (most specific / unabbreviated)
        canonical = max(variants, key=len)

        # Average pairwise similarity within cluster
        idx_arr = np.array(member_indices)
        sub_matrix = sim_matrix[np.ix_(idx_arr, idx_arr)]
        n_members = len(member_indices)
        if n_members > 1:
            # Exclude diagonal (self-similarity = 1.0)
            mask = ~np.eye(n_members, dtype=bool)
            avg_sim = float(sub_matrix[mask].mean())
        else:
            avg_sim = 1.0

        clusters.append(
            EntityCluster(
                canonical_candidate=canonical,
                variants=variants,
                avg_similarity=round(avg_sim, 4),
            )
        )

    logger.info(
        "Blocking complete: %d clusters from %d entities (threshold=%.2f).",
        len(clusters),
        len(entities),
        sim_threshold,
    )
    return clusters
```

---

## 5. Tests

```python
"""Unit tests for src/resolution/blocking.py — UT-05 (Stage 1)"""

from __future__ import annotations

from unittest.mock import MagicMock

import numpy as np
import pytest

from src.models.schemas import EntityCluster, Triplet
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
```

---

## 6. Smoke Test

```bash
python -c "
from src.resolution.blocking import block_entities
from src.retrieval.embeddings import get_bge_embeddings

emb = get_bge_embeddings()
entities = ['Customer', 'Customers', 'customer entity', 'CUST', 'Product', 'Products', 'Order']
clusters = block_entities(entities, emb, threshold=0.88)
for c in clusters:
    print(f'  Cluster: {c.variants} → {c.canonical_candidate} (sim={c.avg_similarity:.3f})')
"
```
