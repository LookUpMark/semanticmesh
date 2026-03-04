# Part 4 — `src/resolution/llm_judge.py`

## 1. Purpose & Context

**Epic:** EP-04 Agentic Entity Resolution — Stage 2  
**US-04-02** — LLM Canonicalization Judge

For each `EntityCluster` produced by Stage 1 (blocking), calls an LLM judge to decide: do all variants refer to the **same** real-world concept? If yes (`merge=True`), all variants collapse to `canonical_name`. If no, variants remain as distinct entities.

The provenance texts from the original triplets are the critical disambiguation signal — without them, "Apple" (company) vs "Apple" (fruit) cannot be distinguished.

---

## 2. Prerequisites

- `src/models/schemas.py` — `Triplet`, `EntityCluster`, `CanonicalEntityDecision`, `Entity` (step 3)
- `src/prompts/templates.py` — `ER_JUDGE_SYSTEM`, `ER_JUDGE_USER` (step 7)
- `src/config/logging.py` — `get_logger`, `NodeTimer`
- LLM arg: caller passes `LLMProtocol` from `src/config/llm_client` (see step 4b)

---

## 3. Public API

| Symbol | Signature | Description |
|---|---|---|
| `judge_cluster` | `(cluster: EntityCluster, provenance_map: dict[str, list[str]], llm: LLMProtocol) -> CanonicalEntityDecision` | Calls LLM once per cluster; returns merge decision |
| `cluster_to_entity` | `(cluster: EntityCluster, decision: CanonicalEntityDecision, provenance_map: dict[str, list[str]]) -> Entity` | Builds an `Entity` object from a cluster + judge decision |
| `build_provenance_map` | `(triplets: list[Triplet]) -> dict[str, list[str]]` | Maps each entity string to its provenance texts from triplets |

---

## 4. Full Implementation

```python
"""Stage 2 of Agentic Entity Resolution: LLM Canonicalization Judge.

EP-04-US-04-02: For each EntityCluster, calls the LLM judge with the
cluster variants and their provenance texts from the original triplets.
Returns CanonicalEntityDecision (merge/keep separate + canonical name).
"""

from __future__ import annotations

import json
import logging
from collections import defaultdict

from langchain_core.messages import HumanMessage, SystemMessage

from src.config.llm_client import LLMProtocol
from pydantic import ValidationError

from src.config.logging import NodeTimer, get_logger
from src.models.schemas import (
    CanonicalEntityDecision,
    Entity,
    EntityCluster,
    Triplet,
)
from src.prompts.templates import ER_JUDGE_SYSTEM, ER_JUDGE_USER

logger: logging.Logger = get_logger(__name__)


def build_provenance_map(triplets: list[Triplet]) -> dict[str, list[str]]:
    """Build a mapping from entity string → list of provenance texts.

    Both subjects and objects of every triplet are included.  Used to
    provide the LLM judge with grounding context for each entity variant.

    Args:
        triplets: All triplets from SLM extraction.

    Returns:
        Dict mapping ``entity_string → [provenance_text_1, ...]``.
        Multiple triplets may contribute provenance for the same entity.
    """
    provenance: dict[str, list[str]] = defaultdict(list)
    for t in triplets:
        if t.subject.strip():
            provenance[t.subject.strip()].append(t.provenance_text)
        if t.object.strip():
            provenance[t.object.strip()].append(t.provenance_text)
    return dict(provenance)


def judge_cluster(
    cluster: EntityCluster,
    provenance_map: dict[str, list[str]],
    llm: LLMProtocol,
) -> CanonicalEntityDecision:
    """Call the LLM judge for a single EntityCluster.

    Args:
        cluster: Candidate cluster from Stage 1 blocking.
        provenance_map: Maps entity string → provenance texts (from ``build_provenance_map``).
        llm: Reasoning-class LLM (use ``get_reasoning_llm()``).

    Returns:
        ``CanonicalEntityDecision`` with ``merge`` flag and ``canonical_name``.
        On any failure, returns a conservative "do not merge" decision to
        preserve information (never crashes the pipeline).
    """
    # Build the two JSON structures for the prompt
    variants_json = json.dumps(cluster.variants)
    provenance_entries = []
    for variant in cluster.variants:
        contexts = provenance_map.get(variant, ["<no provenance available>"])
        # Use first 2 provenance texts max to keep prompt bounded
        provenance_entries.append({"variant": variant, "context": " | ".join(contexts[:2])})
    provenance_json = json.dumps(provenance_entries)

    user_prompt = ER_JUDGE_USER.format(
        variants_json=variants_json,
        provenance_json=provenance_json,
    )

    with NodeTimer() as timer:
        try:
            response = llm.invoke(
                [
                    SystemMessage(content=ER_JUDGE_SYSTEM),
                    HumanMessage(content=user_prompt),
                ]
            )
            raw_json: str = response.content.strip()
        except Exception as exc:
            logger.warning(
                "LLM judge call failed for cluster %s: %s — defaulting to no-merge.",
                cluster.canonical_candidate, exc,
            )
            return CanonicalEntityDecision(
                merge=False,
                canonical_name=cluster.canonical_candidate,
                reasoning="LLM call failed — conservative no-merge default.",
            )

    logger.debug(
        "ER judge for cluster '%s' completed in %.0f ms",
        cluster.canonical_candidate, timer.elapsed_ms,
    )

    # Parse JSON
    try:
        data = json.loads(raw_json)
    except json.JSONDecodeError as exc:
        logger.warning("Non-JSON ER judge response: %s — defaulting to no-merge.", exc)
        return CanonicalEntityDecision(
            merge=False,
            canonical_name=cluster.canonical_candidate,
            reasoning="JSON parse error — conservative no-merge default.",
        )

    # Validate with Pydantic
    try:
        decision = CanonicalEntityDecision(**data)
    except ValidationError as exc:
        logger.warning("Pydantic validation failed for ER judge response: %s", exc)
        return CanonicalEntityDecision(
            merge=False,
            canonical_name=cluster.canonical_candidate,
            reasoning="Pydantic validation error — conservative no-merge default.",
        )

    logger.info(
        "ER judge: cluster '%s' → merge=%s, canonical='%s'",
        cluster.canonical_candidate, decision.merge, decision.canonical_name,
    )
    return decision


def cluster_to_entity(
    cluster: EntityCluster,
    decision: CanonicalEntityDecision,
    provenance_map: dict[str, list[str]],
) -> Entity:
    """Convert a cluster + judge decision into a canonical Entity object.

    Args:
        cluster: The ``EntityCluster`` from Stage 1.
        decision: The ``CanonicalEntityDecision`` from the LLM judge.
        provenance_map: For building provenance and synonyms.

    Returns:
        A ``Entity`` ready to be stored in ``BuilderState.canonical_entities``.
    """
    canonical = decision.canonical_name if decision.merge else cluster.canonical_candidate
    synonyms = [v for v in cluster.variants if v != canonical]

    # Collect provenance texts for the canonical entity
    all_provenance: list[str] = provenance_map.get(canonical, [])
    for variant in synonyms:
        all_provenance.extend(provenance_map.get(variant, []))
    provenance_text = " | ".join(dict.fromkeys(all_provenance))  # deduplicated, order-preserving

    return Entity(
        name=canonical,
        definition="",          # filled by Schema Enrichment / HITL
        synonyms=synonyms,
        provenance_text=provenance_text[:1000],  # cap at 1000 chars for Neo4j property
        source_doc="",          # filled by the node that calls this function
    )
```

---

## 5. Tests

```python
"""Unit tests for src/resolution/llm_judge.py — UT-05 (Stage 2)"""

from __future__ import annotations

import json
from unittest.mock import MagicMock

import pytest

from src.models.schemas import CanonicalEntityDecision, EntityCluster, Triplet
from src.resolution.llm_judge import (
    build_provenance_map,
    cluster_to_entity,
    judge_cluster,
)


# ── Fixtures ───────────────────────────────────────────────────────────────────

def _make_cluster(*variants: str) -> EntityCluster:
    return EntityCluster(
        canonical_candidate=max(variants, key=len),
        variants=list(variants),
        avg_similarity=0.95,
    )


def _make_triplet(subject: str, obj: str, provenance: str = "") -> Triplet:
    return Triplet(
        subject=subject, predicate="is", object=obj,
        provenance_text=provenance or f"{subject} is {obj}.",
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


# ── build_provenance_map ──────────────────────────────────────────────────────

class TestBuildProvenanceMap:
    def test_maps_subjects_and_objects(self) -> None:
        triplets = [
            _make_triplet("Customer", "Product", "A Customer buys a Product."),
        ]
        pmap = build_provenance_map(triplets)
        assert "Customer" in pmap
        assert "Product" in pmap
        assert "A Customer buys a Product." in pmap["Customer"]

    def test_multiple_triplets_accumulate_provenance(self) -> None:
        t1 = _make_triplet("Customer", "Order", "Customer places an Order.")
        t2 = _make_triplet("Customer", "Invoice", "Customer receives an Invoice.")
        pmap = build_provenance_map([t1, t2])
        assert len(pmap["Customer"]) == 2

    def test_empty_returns_empty_dict(self) -> None:
        assert build_provenance_map([]) == {}


# ── judge_cluster ──────────────────────────────────────────────────────────────

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
        pmap = {}
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


# ── cluster_to_entity ─────────────────────────────────────────────────────────

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
```

---

## 6. Smoke Test

```bash
python -c "
from src.resolution.llm_judge import build_provenance_map, judge_cluster, cluster_to_entity
from src.models.schemas import Triplet, EntityCluster
from src.config.llm_factory import get_reasoning_llm

triplets = [
    Triplet(subject='Customer', predicate='has', object='ID', provenance_text='A Customer has a unique ID.', confidence=0.9),
    Triplet(subject='Customers', predicate='purchase', object='Products', provenance_text='Customers purchase Products.', confidence=0.85),
]
pmap = build_provenance_map(triplets)
cluster = EntityCluster(canonical_candidate='Customer', variants=['Customer', 'Customers'], avg_similarity=0.96)
llm = get_reasoning_llm()
decision = judge_cluster(cluster, pmap, llm)
print(f'Merge: {decision.merge}, Canonical: {decision.canonical_name}')
entity = cluster_to_entity(cluster, decision, pmap)
print(f'Entity: {entity.name}, Synonyms: {entity.synonyms}')
"
```
