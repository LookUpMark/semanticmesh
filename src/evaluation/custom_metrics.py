"""EP-16: Custom evaluation metrics not covered by RAGAS.

Provides:
    cypher_healing_rate   — fraction of failed Cypher attempts recovered by healing
    hitl_confidence_agreement — Pearson correlation between mapping confidence
                                and gold-standard accuracy
"""

from __future__ import annotations

from src.models.schemas import MappingProposal  # noqa: TC001

# ─────────────────────────────────────────────────────────────────────────────
# Data types
# ─────────────────────────────────────────────────────────────────────────────


class HealingResult:
    """Result of one Cypher generation attempt (with optional healing retries)."""

    __slots__ = ("initial_success", "final_success")

    def __init__(self, *, initial_success: bool, final_success: bool) -> None:
        self.initial_success: bool = initial_success
        self.final_success: bool = final_success


class GoldMapping:
    """Ground-truth concept mapping for one physical table."""

    __slots__ = ("table_name", "correct_concept")

    def __init__(self, *, table_name: str, correct_concept: str) -> None:
        self.table_name: str = table_name
        self.correct_concept: str = correct_concept


# ─────────────────────────────────────────────────────────────────────────────
# Metric implementations
# ─────────────────────────────────────────────────────────────────────────────


def cypher_healing_rate(results: list[HealingResult]) -> float:
    """Fraction of initially-failed Cypher statements recovered by healing.

    Definition::

        healed = results where initial_success=False AND final_success=True
        failed = results where initial_success=False AND final_success=False
        rate   = healed / (healed + failed)

    Returns 0.0 when there are no healing attempts (all first-try successes or
    the list is empty).
    """
    healed = sum(1 for r in results if not r.initial_success and r.final_success)
    failed = sum(1 for r in results if not r.initial_success and not r.final_success)
    total_attempts = healed + failed
    if total_attempts == 0:
        return 0.0
    return healed / total_attempts


def hitl_confidence_agreement(
    proposals: list[MappingProposal],
    gold: list[GoldMapping],
) -> float:
    """Pearson correlation between mapping confidence scores and accuracy.

    For each proposal matched to a GoldMapping by table_name, computes:
      - ``confidence``: float ∈ [0, 1]
      - ``correct``:    1.0 if mapped_concept == gold correct_concept else 0.0

    Returns the Pearson r between those two vectors.
    Returns 0.0 if fewer than 2 matched proposals are found.
    """
    gold_dict: dict[str, str] = {g.table_name: g.correct_concept for g in gold}
    confidences: list[float] = []
    accuracies: list[float] = []
    for proposal in proposals:
        if proposal.table_name in gold_dict:
            confidences.append(proposal.confidence)
            correct = float(proposal.mapped_concept == gold_dict[proposal.table_name])
            accuracies.append(correct)
    if len(confidences) < 2:
        return 0.0
    return _pearson(confidences, accuracies)


def _pearson(x: list[float], y: list[float]) -> float:
    """Pearson correlation coefficient (pure Python, no scipy dependency)."""
    n = len(x)
    mu_x = sum(x) / n
    mu_y = sum(y) / n
    cov = sum((xi - mu_x) * (yi - mu_y) for xi, yi in zip(x, y, strict=False))
    std_x = sum((xi - mu_x) ** 2 for xi in x) ** 0.5
    std_y = sum((yi - mu_y) ** 2 for yi in y) ** 0.5
    if std_x == 0.0 or std_y == 0.0:
        return 0.0
    return cov / (std_x * std_y)
