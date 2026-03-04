# Part 9 — `src/evaluation/custom_metrics.py`

## 1. Purpose & Context

**Epic:** EP-16 RAGAS Evaluation Pipeline  
**Supporting Evaluation Infrastructure**

`custom_metrics` computes two project-specific KPIs that RAGAS does not cover:

| Metric | Formula | What it measures |
|---|---|---|
| `cypher_healing_rate` | `healed / (healed + permanently_failed)` | Healing loop recovery effectiveness |
| `hitl_confidence_agreement` | `auto_correct / total_validated` | Human agreement with the system's auto-approved mappings |

Both metrics are collected from builder run state logs and passed to `run_evaluation` as `custom_metrics` dict.

Additionally, `custom_metrics` provides `recall_at_k` — a retrieval quality measure not in the default RAGAS metric set — for the ablation runner.

---

## 2. Prerequisites

- `src/models/schemas.py` — `EvaluationReport` (step 5)
- No external dependencies beyond `statistics` (stdlib)

---

## 3. Public API

| Symbol | Signature | Description |
|---|---|---|
| `cypher_healing_rate` | `(healed: int, permanently_failed: int) -> float` | Rate of Cypher errors recovered by healing loop |
| `hitl_confidence_agreement` | `(auto_correct: int, total_validated: int) -> float` | Fraction of system-approved mappings confirmed correct |
| `recall_at_k` | `(gold_chunks: list[str], retrieved_chunks: list[str], k: int) -> float` | % gold chunks present in Top-K retrieval |
| `collect_builder_metrics` | `(builder_state: dict) -> dict[str, float]` | Extract `cypher_healing_rate` + `hitl_confidence_agreement` from final BuilderState |

---

## 4. Full Implementation

```python
"""Custom evaluation metrics for the GraphRAG thesis pipeline.

Provides metrics not covered by RAGAS:
  - cypher_healing_rate        — recovery rate of the Cypher healing loop
  - hitl_confidence_agreement  — human review agreement with auto-approved mappings
  - recall_at_k                — retrieval recall at K candidates
  - collect_builder_metrics    — extract metrics from a completed BuilderState
"""

from __future__ import annotations

import logging

from src.config.logging import get_logger

logger: logging.Logger = get_logger(__name__)


# ── Cypher Healing Rate ────────────────────────────────────────────────────────

def cypher_healing_rate(healed: int, permanently_failed: int) -> float:
    """Compute the fraction of Cypher failures recovered by the healing loop.

    Args:
        healed:            Number of Cypher statements that failed initially
                           but were healed within ``max_cypher_healing_attempts``.
        permanently_failed: Number of statements that exhausted all healing
                           attempts without succeeding.

    Returns:
        ``healed / (healed + permanently_failed)`` as float in [0.0, 1.0].
        Returns 1.0 (perfect) when both counts are zero (no failures).
    """
    total = healed + permanently_failed
    if total == 0:
        return 1.0  # No failures — perfect score
    rate = healed / total
    logger.debug(
        "cypher_healing_rate: healed=%d, failed=%d → %.4f",
        healed, permanently_failed, rate,
    )
    return round(rate, 4)


# ── HITL Confidence Agreement ─────────────────────────────────────────────────

def hitl_confidence_agreement(auto_correct: int, total_validated: int) -> float:
    """Compute the fraction of auto-approved mappings confirmed correct.

    An auto-approved mapping has confidence ≥ threshold AND critic approved.
    ``auto_correct`` is the count that matched the gold-standard mapping;
    ``total_validated`` is all mappings that bypassed HITL.

    Args:
        auto_correct:     Count of auto-approved mappings matching gold standard.
        total_validated:  Total mappings that were auto-approved (no human review).

    Returns:
        ``auto_correct / total_validated`` as float.
        Returns 0.0 when ``total_validated`` is zero (all sent to HITL).
    """
    if total_validated == 0:
        logger.debug("hitl_confidence_agreement: no auto-approved mappings.")
        return 0.0
    rate = auto_correct / total_validated
    logger.debug(
        "hitl_confidence_agreement: correct=%d / validated=%d → %.4f",
        auto_correct, total_validated, rate,
    )
    return round(rate, 4)


# ── Recall@K ──────────────────────────────────────────────────────────────────

def recall_at_k(
    gold_chunks: list[str],
    retrieved_chunks: list[str],
    k: int,
) -> float:
    """Compute retrieval recall: fraction of gold chunks present in Top-K.

    Args:
        gold_chunks:      Ground-truth relevant chunk texts (from gold standard).
        retrieved_chunks: All retrieved candidate chunks (order preserved, sliced to k).
        k:                Number of top candidates to evaluate.

    Returns:
        ``|gold ∩ top_k| / |gold|`` as float.
        Returns 1.0 if ``gold_chunks`` is empty (vacuously true).
    """
    if not gold_chunks:
        return 1.0
    top_k_set = set(retrieved_chunks[:k])
    gold_set = set(gold_chunks)
    overlap = len(gold_set & top_k_set)
    recall = overlap / len(gold_set)
    return round(recall, 4)


# ── BuilderState Metric Extraction ────────────────────────────────────────────

def collect_builder_metrics(builder_state: dict) -> dict[str, float]:
    """Extract custom metrics from a completed BuilderState dict.

    Reads the ``healed_cypher_count``, ``failed_cypher_count``,
    ``auto_approved_correct``, and ``auto_approved_total`` counters that the
    builder graph nodes accumulate during a run.

    If these counters are absent (e.g., partial run), returns safe defaults.

    Args:
        builder_state: The final state dict returned by ``graph.invoke()``.

    Returns:
        Dict with keys ``"cypher_healing_rate"`` and ``"hitl_confidence_agreement"``.
    """
    healed = int(builder_state.get("healed_cypher_count", 0))
    failed = int(builder_state.get("failed_cypher_count", 0))
    auto_correct = int(builder_state.get("auto_approved_correct", 0))
    auto_total = int(builder_state.get("auto_approved_total", 0))

    metrics = {
        "cypher_healing_rate": cypher_healing_rate(healed, failed),
        "hitl_confidence_agreement": hitl_confidence_agreement(auto_correct, auto_total),
    }
    logger.info("Builder metrics: %s", metrics)
    return metrics
```

---

## 5. Tests

```python
"""Unit tests for src/evaluation/custom_metrics.py — UT-25"""

from __future__ import annotations

import pytest

from src.evaluation.custom_metrics import (
    collect_builder_metrics,
    cypher_healing_rate,
    hitl_confidence_agreement,
    recall_at_k,
)


# ── cypher_healing_rate ────────────────────────────────────────────────────────

class TestCypherHealingRate:
    def test_perfect_rate_no_failures(self) -> None:
        assert cypher_healing_rate(0, 0) == 1.0

    def test_all_healed(self) -> None:
        assert cypher_healing_rate(10, 0) == 1.0

    def test_none_healed(self) -> None:
        assert cypher_healing_rate(0, 5) == pytest.approx(0.0)

    def test_mixed(self) -> None:
        assert cypher_healing_rate(8, 2) == pytest.approx(0.8)

    def test_returns_four_decimal_precision(self) -> None:
        rate = cypher_healing_rate(1, 3)
        assert rate == pytest.approx(0.25, abs=1e-4)

    def test_range_is_0_to_1(self) -> None:
        for h, f in [(0, 1), (3, 0), (5, 5), (100, 1)]:
            rate = cypher_healing_rate(h, f)
            assert 0.0 <= rate <= 1.0


# ── hitl_confidence_agreement ─────────────────────────────────────────────────

class TestHitlConfidenceAgreement:
    def test_zero_total_returns_zero(self) -> None:
        assert hitl_confidence_agreement(0, 0) == 0.0

    def test_all_correct(self) -> None:
        assert hitl_confidence_agreement(10, 10) == pytest.approx(1.0)

    def test_none_correct(self) -> None:
        assert hitl_confidence_agreement(0, 10) == pytest.approx(0.0)

    def test_partial_agreement(self) -> None:
        assert hitl_confidence_agreement(9, 10) == pytest.approx(0.9)

    def test_range_is_0_to_1(self) -> None:
        for correct, total in [(0, 5), (5, 5), (3, 7)]:
            rate = hitl_confidence_agreement(correct, total)
            assert 0.0 <= rate <= 1.0


# ── recall_at_k ───────────────────────────────────────────────────────────────

class TestRecallAtK:
    def test_perfect_recall(self) -> None:
        gold = ["A", "B"]
        retrieved = ["A", "B", "C"]
        assert recall_at_k(gold, retrieved, k=3) == pytest.approx(1.0)

    def test_zero_recall(self) -> None:
        gold = ["X", "Y"]
        retrieved = ["A", "B", "C"]
        assert recall_at_k(gold, retrieved, k=3) == pytest.approx(0.0)

    def test_partial_recall(self) -> None:
        gold = ["A", "B", "C"]
        retrieved = ["A", "D", "E", "B"]
        assert recall_at_k(gold, retrieved, k=4) == pytest.approx(2 / 3, abs=1e-4)

    def test_empty_gold_returns_one(self) -> None:
        assert recall_at_k([], ["A", "B"], k=2) == 1.0

    def test_k_slices_retrieved(self) -> None:
        gold = ["B"]
        retrieved = ["A", "B", "C"]
        # B is at index 1, within k=2
        assert recall_at_k(gold, retrieved, k=2) == pytest.approx(1.0)
        # B is outside k=1
        assert recall_at_k(gold, retrieved, k=1) == pytest.approx(0.0)


# ── collect_builder_metrics ───────────────────────────────────────────────────

class TestCollectBuilderMetrics:
    def test_returns_both_keys(self) -> None:
        state = {
            "healed_cypher_count": 4,
            "failed_cypher_count": 1,
            "auto_approved_correct": 9,
            "auto_approved_total": 10,
        }
        metrics = collect_builder_metrics(state)
        assert "cypher_healing_rate" in metrics
        assert "hitl_confidence_agreement" in metrics

    def test_correct_values(self) -> None:
        state = {
            "healed_cypher_count": 8,
            "failed_cypher_count": 2,
            "auto_approved_correct": 18,
            "auto_approved_total": 20,
        }
        metrics = collect_builder_metrics(state)
        assert metrics["cypher_healing_rate"] == pytest.approx(0.8)
        assert metrics["hitl_confidence_agreement"] == pytest.approx(0.9)

    def test_missing_counters_default_to_safe_values(self) -> None:
        metrics = collect_builder_metrics({})
        assert metrics["cypher_healing_rate"] == 1.0       # no failures → perfect
        assert metrics["hitl_confidence_agreement"] == 0.0  # no auto-approved → 0
```

---

## 6. Smoke Test

```bash
python -c "
from src.evaluation.custom_metrics import cypher_healing_rate, hitl_confidence_agreement, recall_at_k, collect_builder_metrics

print('cypher_healing_rate(8, 2):', cypher_healing_rate(8, 2))
print('hitl_confidence_agreement(9, 10):', hitl_confidence_agreement(9, 10))
print('recall_at_k([A,B], [A,C,D,B], k=4):', recall_at_k(['A','B'], ['A','C','D','B'], k=4))

state = {'healed_cypher_count': 8, 'failed_cypher_count': 2, 'auto_approved_correct': 9, 'auto_approved_total': 10}
print('Builder metrics:', collect_builder_metrics(state))
print('custom_metrics smoke test passed.')
"
```
