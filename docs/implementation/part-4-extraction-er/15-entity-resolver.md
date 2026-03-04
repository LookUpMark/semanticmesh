# Part 4 — `src/resolution/entity_resolver.py`

## 1. Purpose & Context

**Epic:** EP-04 Agentic Entity Resolution  
**US-04-01 + US-04-02** — Full Resolution Pipeline

Orchestrates the two-stage entity resolution pipeline:

1. **Stage 1** (`blocking.py`): embed all entities, group near-duplicates into clusters
2. **Stage 2** (`llm_judge.py`): for each cluster, call the LLM judge and output a canonical `Entity`

Singletons (entities not in any cluster) are promoted directly to `Entity` without an LLM call. The final list of `Entity` objects is what gets embedded and stored as `BuilderState.canonical_entities`.

---

## 2. Prerequisites

- `src/resolution/blocking.py` — `extract_unique_entities`, `block_entities` (step 13)
- `src/resolution/llm_judge.py` — `build_provenance_map`, `judge_cluster`, `cluster_to_entity` (step 14)
- `src/retrieval/embeddings.py` — `get_bge_embeddings` (step 23) **or** any `Embeddings`
- `src/config/settings.py` — `er_similarity_threshold`, `er_blocking_top_k`
- `src/config/logging.py` — `get_logger`

---

## 3. Public API

| Symbol | Signature | Description |
|---|---|---|
| `resolve_entities` | `(triplets: list[Triplet], embeddings: Embeddings, llm: LLMProtocol, source_doc: str) -> list[Entity]` | Full two-stage resolution pipeline |

---

## 4. Full Implementation

```python
"""Full two-stage Agentic Entity Resolution pipeline.

EP-04: Orchestrates Stage 1 (vector blocking) and Stage 2 (LLM judge)
to produce a deduplicated, canonical list of Entity objects.
"""

from __future__ import annotations

import logging

from langchain_core.embeddings import Embeddings

from src.config.llm_client import LLMProtocol

from src.config.logging import get_logger
from src.models.schemas import Entity, EntityCluster, Triplet
from src.resolution.blocking import block_entities, extract_unique_entities
from src.resolution.llm_judge import (
    build_provenance_map,
    cluster_to_entity,
    judge_cluster,
)

logger: logging.Logger = get_logger(__name__)


def resolve_entities(
    triplets: list[Triplet],
    embeddings: Embeddings,
    llm: LLMProtocol,
    source_doc: str = "",
) -> list[Entity]:
    """Run the full two-stage entity resolution pipeline.

    Stage 1: Vector blocking — embed all entity strings, group near-duplicate
             pairs into ``EntityCluster`` objects using cosine similarity.

    Stage 2: LLM judge — for each cluster, call ``judge_cluster`` to decide
             whether the variants should merge into one canonical entity.

    Singletons (not in any cluster) are promoted directly to ``Entity``
    objects without an LLM call, preserving all extracted facts.

    Args:
        triplets: All triplets from the SLM extraction step.
        embeddings: Embedding model (BGE-M3 recommended).
        llm: Reasoning LLM for the judge step (temperature=0.0).
        source_doc: Source document name (stored on each Entity for provenance).

    Returns:
        List of canonical ``Entity`` objects, deduplicated and ready for
        embedding and storage in BuilderState.canonical_entities.
    """
    if not triplets:
        logger.warning("resolve_entities called with empty triplet list — returning empty.")
        return []

    # ── Stage 1: Blocking ──────────────────────────────────────────────────────
    all_entities = extract_unique_entities(triplets)
    clusters = block_entities(all_entities, embeddings)

    # Track which entities are covered by a cluster
    clustered_entities: set[str] = set()
    for cluster in clusters:
        clustered_entities.update(cluster.variants)

    # ── Stage 2: LLM Judge ────────────────────────────────────────────────────
    provenance_map = build_provenance_map(triplets)
    canonical_entities: list[Entity] = []

    for cluster in clusters:
        decision = judge_cluster(cluster, provenance_map, llm)
        entity = cluster_to_entity(cluster, decision, provenance_map)
        entity.source_doc = source_doc
        canonical_entities.append(entity)

    # ── Singletons: promote directly ──────────────────────────────────────────
    singleton_entities = [e for e in all_entities if e not in clustered_entities]
    for singleton in singleton_entities:
        provenance_texts = provenance_map.get(singleton, [])
        canonical_entities.append(
            Entity(
                name=singleton,
                definition="",
                synonyms=[],
                provenance_text=" | ".join(provenance_texts[:3]),  # cap at 3
                source_doc=source_doc,
            )
        )

    logger.info(
        "Entity resolution complete: %d clusters resolved, %d singletons promoted → %d total entities.",
        len(clusters),
        len(singleton_entities),
        len(canonical_entities),
    )
    return canonical_entities
```

---

## 5. Tests

```python
"""Unit tests for src/resolution/entity_resolver.py — UT-06"""

from __future__ import annotations

import json
from unittest.mock import MagicMock

import numpy as np
import pytest

from src.models.schemas import Entity, Triplet
from src.resolution.entity_resolver import resolve_entities


# ── Fixtures ───────────────────────────────────────────────────────────────────

def _make_triplet(subject: str, obj: str, prov: str = "") -> Triplet:
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

    def embed_documents(texts: list[str]) -> list[list[float]]:
        vecs = []
        for i, t in enumerate(texts):
            v = [0.0] * dim
            v[i % dim] = 1.0
            vecs.append(v)
        return vecs

    emb.embed_documents.side_effect = embed_documents
    return emb


def _make_embeddings_identical(entities: list[str]) -> MagicMock:
    """All entities share the same vector — max clustering."""
    emb = MagicMock()

    def embed_documents(texts: list[str]) -> list[list[float]]:
        return [[1.0, 0.0]] * len(texts)

    emb.embed_documents.side_effect = embed_documents
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


# ── resolve_entities ──────────────────────────────────────────────────────────

class TestResolveEntities:
    def test_empty_triplets_returns_empty(self) -> None:
        emb = MagicMock()
        llm = MagicMock()
        result = resolve_entities([], emb, llm)
        assert result == []

    def test_all_singletons_no_llm_call(self) -> None:
        """Orthogonal embeddings → no clusters → no LLM calls."""
        triplets = [_make_triplet("Customer", "Product"), _make_triplet("Order", "Invoice")]
        entities = ["Customer", "Product", "Order", "Invoice"]
        emb = _make_embeddings_orthogonal(entities)
        llm = MagicMock()
        result = resolve_entities(triplets, emb, llm)
        llm.invoke.assert_not_called()
        assert len(result) == 4  # all promoted as singletons

    def test_cluster_resolved_to_single_entity(self) -> None:
        """Identical embeddings → one big cluster → LLM merges to 'Customer'."""
        triplets = [_make_triplet("Customer", "CUST"), _make_triplet("Customers", "Product")]
        emb = _make_embeddings_identical(["Customer", "CUST", "Customers", "Product"])
        llm = _make_llm_merge("Customer")
        result = resolve_entities(triplets, emb, llm)
        assert any(e.name == "Customer" for e in result)

    def test_returns_entity_objects(self) -> None:
        triplets = [_make_triplet("Customer", "Product")]
        emb = _make_embeddings_orthogonal(["Customer", "Product"])
        llm = MagicMock()
        result = resolve_entities(triplets, emb, llm)
        assert all(isinstance(e, Entity) for e in result)

    def test_source_doc_set_on_entities(self) -> None:
        triplets = [_make_triplet("Customer", "Order")]
        emb = _make_embeddings_orthogonal(["Customer", "Order"])
        llm = MagicMock()
        result = resolve_entities(triplets, emb, llm, source_doc="glossary.pdf")
        for entity in result:
            assert entity.source_doc == "glossary.pdf"

    def test_llm_failure_in_judge_does_not_crash(self) -> None:
        """If LLM judge fails for one cluster, pipeline continues."""
        triplets = [_make_triplet("Customer", "CUST")]
        emb = _make_embeddings_identical(["Customer", "CUST"])
        llm = MagicMock()
        llm.invoke.side_effect = RuntimeError("timeout")
        result = resolve_entities(triplets, emb, llm)
        # Conservative no-merge → cluster preserved but not crashed
        assert len(result) >= 1
```

---

## 6. Smoke Test

```bash
python -c "
from src.resolution.entity_resolver import resolve_entities
from src.retrieval.embeddings import get_bge_embeddings
from src.config.llm_factory import get_reasoning_llm
from src.models.schemas import Triplet

triplets = [
    Triplet(subject='Customer', predicate='has', object='ID', provenance_text='Customer has unique ID.', confidence=0.9),
    Triplet(subject='Customers', predicate='purchase', object='Products', provenance_text='Customers buy Products.', confidence=0.8),
    Triplet(subject='Product', predicate='has', object='SKU', provenance_text='Each Product has a SKU.', confidence=0.95),
]
emb = get_bge_embeddings()
llm = get_reasoning_llm()
entities = resolve_entities(triplets, emb, llm, source_doc='glossary.pdf')
for e in entities:
    print(f'  Entity: {e.name} | synonyms={e.synonyms}')
"
```
