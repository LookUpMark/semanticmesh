# Part 9 — `src/evaluation/ablation_runner.py`

## Status Update (Current Implementation)

This guide originally documented the early 6-experiment layout. The current codebase uses a larger matrix and two execution entry points:

1. `src/evaluation/ablation_runner.py` (programmatic runner): AB-00 … AB-20 (`ABLATION_MATRIX`, 21 studies)
2. `scripts/run_ablation_full.py` (full pipeline CLI): builder + query + optional RAGAS, with per-study logs and JSON outputs

Current output directory is:

- `notebooks/ablation/ablation_results/`

Canonical per-study artifacts are flat files in that directory:

- `AB-XX.log`
- `AB-XX.json`
- `ablation_summary.json`

Use `src/evaluation/ablation_runner.py` as the source of truth for study IDs, env overrides, and which studies enable RAGAS.

## 1. Purpose & Context

**Epic:** EP-17 Ablation Study  
**Ablation IDs:** AB-01 → AB-06

The ablation runner systematically disables one feature at a time, re-runs the full evaluation pipeline on the gold-standard dataset, and computes deltas against a full-pipeline baseline.

| ID | Feature toggled | Settings flag | Primary metric |
|---|---|---|---|
| AB-01 | Schema Enrichment | `ENABLE_SCHEMA_ENRICHMENT=False` | Mapping accuracy |
| AB-02 | Hybrid Retrieval → Vector Only | `RETRIEVAL_MODE="vector_only"` | Context relevancy |
| AB-03 | Cypher Healing | `ENABLE_CYPHER_HEALING=False` | Execution success rate |
| AB-04 | Critic Validation | `ENABLE_CRITIC_VALIDATION=False` | Mapping precision |
| AB-05 | Reranker | `ENABLE_RERANKER=False` | Context relevancy + NDCG@5 |
| AB-06 | Hallucination Grader | `ENABLE_HALLUCINATION_GRADER=False` | Faithfulness |

Statistical comparison uses the Wilcoxon signed-rank test (paired, non-parametric), appropriate for 3-run repeated measures.

---

## 2. Prerequisites

- `src/config/settings.py` — `Settings` singleton with all ablation flags (step 2)
- `src/evaluation/ragas_runner.py` — `run_evaluation`, `load_dataset`, `save_report` (step 29)
- `src/evaluation/custom_metrics.py` — `collect_builder_metrics` (step 30)
- `scipy` — `scipy.stats.wilcoxon` for statistical testing
- `src/generation/query_graph.py` — `build_query_graph`, `run_query` (step 28)

```
pip install scipy
```

---

## 3. Public API

| Symbol | Signature | Description |
|---|---|---|
| `ABLATION_REGISTRY` | `dict[str, dict]` | Maps ablation IDs to `{flag, value, description, primary_metric}` |
| `run_ablation_condition` | `(ablation_id, dataset, *, baseline=False) -> AblationResult` | Applies flag override, runs 3 eval passes, averages |
| `compare_conditions` | `(baseline: AblationResult, variant: AblationResult) -> dict` | Delta + Wilcoxon p-value + effect-size (Cohen's d) |
| `run_all_ablations` | `(dataset) -> list[dict]` | Loops all 6 experiments against shared baseline |
| `save_ablation_report` | `(results, output_dir) -> Path` | Timestamped JSON report |

---

## 4. Full Implementation

```python
"""Ablation study runner for the GraphRAG thesis pipeline.

Experiments AB-01 through AB-06 each disable one feature, re-run evaluation,
and compare against a full-pipeline baseline.  Statistical comparison uses the
Wilcoxon signed-rank test (3 repeated runs, paired non-parametric).

Usage (CLI):
    python -m src.evaluation.ablation_runner \\
        --dataset tests/fixtures/gold_standard.json \\
        --ablation AB-01 \\
        --runs 3 \\
        --output reports/
"""

from __future__ import annotations

import argparse
import json
import logging
import statistics
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from scipy.stats import wilcoxon

from src.config.logging import get_logger
from src.config.settings import Settings
from src.evaluation.custom_metrics import collect_builder_metrics
from src.evaluation.ragas_runner import EvaluationReport, load_dataset, run_evaluation
from src.generation.query_graph import build_query_graph, run_query

logger: logging.Logger = get_logger(__name__)


# ── Ablation Registry ─────────────────────────────────────────────────────────

ABLATION_REGISTRY: dict[str, dict[str, Any]] = {
    "AB-01": {
        "description": "Disable schema enrichment",
        "flag": "ENABLE_SCHEMA_ENRICHMENT",
        "value": False,
        "primary_metric": "hitl_confidence_agreement",
    },
    "AB-02": {
        "description": "Vector-only retrieval (disable BM25 + graph traversal)",
        "flag": "RETRIEVAL_MODE",
        "value": "vector_only",
        "primary_metric": "context_precision",
    },
    "AB-03": {
        "description": "Disable Cypher healing loop",
        "flag": "ENABLE_CYPHER_HEALING",
        "value": False,
        "primary_metric": "cypher_healing_rate",
    },
    "AB-04": {
        "description": "Disable LLM critic validation",
        "flag": "ENABLE_CRITIC_VALIDATION",
        "value": False,
        "primary_metric": "hitl_confidence_agreement",
    },
    "AB-05": {
        "description": "Disable cross-encoder reranker",
        "flag": "ENABLE_RERANKER",
        "value": False,
        "primary_metric": "context_precision",
    },
    "AB-06": {
        "description": "Disable hallucination grader",
        "flag": "ENABLE_HALLUCINATION_GRADER",
        "value": False,
        "primary_metric": "faithfulness",
    },
}

# Thresholds for pass/fail assessment (replicated from ragas_runner for portability)
THRESHOLDS: dict[str, float] = {
    "faithfulness": 0.95,
    "context_precision": 0.85,
    "context_recall": 0.90,
    "answer_relevancy": 0.85,
    "cypher_healing_rate": 0.80,
    "hitl_confidence_agreement": 0.90,
}


# ── Data Types ────────────────────────────────────────────────────────────────

class AblationResult:
    """Aggregated metrics for one ablation condition (averaged over N runs)."""

    def __init__(
        self,
        ablation_id: str,
        is_baseline: bool,
        run_scores: list[dict[str, float]],
    ) -> None:
        self.ablation_id = ablation_id
        self.is_baseline = is_baseline
        self.run_scores: list[dict[str, float]] = run_scores
        self.mean_scores: dict[str, float] = _mean_scores(run_scores)

    def to_dict(self) -> dict:
        return {
            "ablation_id": self.ablation_id,
            "is_baseline": self.is_baseline,
            "run_scores": self.run_scores,
            "mean_scores": self.mean_scores,
        }


def _mean_scores(run_scores: list[dict[str, float]]) -> dict[str, float]:
    """Average per-metric scores across repeated runs."""
    if not run_scores:
        return {}
    all_keys = set().union(*run_scores)
    return {
        key: round(statistics.mean(r[key] for r in run_scores if key in r), 4)
        for key in all_keys
    }


# ── Settings Override Context Manager ─────────────────────────────────────────

class _SettingsOverride:
    """Temporarily patch a settings field, restore on exit."""

    def __init__(self, flag: str, value: Any) -> None:
        self._flag = flag
        self._value = value
        self._original: Any = None

    def __enter__(self) -> "_SettingsOverride":
        settings = Settings()
        self._original = getattr(settings, self._flag, None)
        try:
            setattr(settings, self._flag, self._value)
        except Exception:
            # Pydantic v2 models may be frozen; override via object.__setattr__
            object.__setattr__(settings, self._flag, self._value)
        logger.info("Ablation override: %s = %r (was %r)", self._flag, self._value, self._original)
        return self

    def __exit__(self, *_: Any) -> None:
        settings = Settings()
        try:
            setattr(settings, self._flag, self._original)
        except Exception:
            object.__setattr__(settings, self._flag, self._original)
        logger.info("Restored: %s = %r", self._flag, self._original)


# ── Single Condition Runner ────────────────────────────────────────────────────

def run_ablation_condition(
    ablation_id: str,
    dataset: list[dict],
    *,
    baseline: bool = False,
    n_runs: int = 3,
) -> AblationResult:
    """Run one ablation condition N times and average scores.

    Args:
        ablation_id: One of "AB-01" … "AB-06" or "baseline".
        dataset:     Gold-standard dataset loaded via :func:`load_dataset`.
        baseline:    When True, no settings flag is modified.
        n_runs:      Number of repeated evaluation passes (default 3).

    Returns:
        :class:`AblationResult` with per-run and averaged metric scores.
    """
    if ablation_id not in ABLATION_REGISTRY and not baseline:
        raise ValueError(
            f"Unknown ablation_id '{ablation_id}'. "
            f"Valid ids: {list(ABLATION_REGISTRY.keys())}"
        )

    run_scores: list[dict[str, float]] = []

    for run_idx in range(n_runs):
        logger.info(
            "Running %s run %d/%d (baseline=%s)",
            ablation_id, run_idx + 1, n_runs, baseline,
        )
        if baseline:
            scores = _single_evaluation_pass(dataset)
        else:
            entry = ABLATION_REGISTRY[ablation_id]
            with _SettingsOverride(flag=entry["flag"], value=entry["value"]):
                scores = _single_evaluation_pass(dataset)
        run_scores.append(scores)

    return AblationResult(
        ablation_id="baseline" if baseline else ablation_id,
        is_baseline=baseline,
        run_scores=run_scores,
    )


def _single_evaluation_pass(dataset: list[dict]) -> dict[str, float]:
    """Run the full evaluation pipeline once and return metric dict."""
    query_graph = build_query_graph()

    enriched: list[dict] = []
    for row in dataset:
        result = run_query(row["question"])
        enriched.append({
            "question": row["question"],
            "answer": result.get("answer", ""),
            "contexts": result.get("contexts", []),
            "ground_truth": row.get("ground_truth", ""),
        })

    report: EvaluationReport = run_evaluation(
        dataset=enriched,
        query_graph=query_graph,
        custom_metrics={},
    )
    return {
        "faithfulness": report.faithfulness,
        "context_precision": report.context_precision,
        "context_recall": report.context_recall,
        "answer_relevancy": report.answer_relevancy,
        "cypher_healing_rate": report.cypher_healing_rate or 0.0,
        "hitl_confidence_agreement": report.hitl_confidence_agreement or 0.0,
    }


# ── Statistical Comparison ────────────────────────────────────────────────────

def _cohens_d(a: list[float], b: list[float]) -> float:
    """Compute Cohen's d effect size between two paired samples."""
    if len(a) < 2:
        return 0.0
    diffs = [ai - bi for ai, bi in zip(a, b)]
    mean_diff = statistics.mean(diffs)
    try:
        pooled_std = statistics.stdev(diffs)
    except statistics.StatisticsError:
        pooled_std = 0.0
    if pooled_std == 0.0:
        return 0.0
    return round(mean_diff / pooled_std, 4)


def compare_conditions(
    baseline: AblationResult,
    variant: AblationResult,
) -> dict[str, Any]:
    """Compute deltas and Wilcoxon signed-rank p-values for each metric.

    Args:
        baseline: Full-pipeline :class:`AblationResult`.
        variant:  Ablated :class:`AblationResult`.

    Returns:
        Dict with keys: ``ablation_id``, ``deltas``, ``p_values``, ``effect_sizes``,
        ``primary_metric``, ``primary_delta``.
    """
    ablation_id = variant.ablation_id
    entry = ABLATION_REGISTRY.get(ablation_id, {})
    primary_metric: str = entry.get("primary_metric", "faithfulness")

    deltas: dict[str, float] = {}
    p_values: dict[str, float] = {}
    effect_sizes: dict[str, float] = {}

    all_metrics = set(baseline.mean_scores) | set(variant.mean_scores)

    for metric in sorted(all_metrics):
        base_vals = [r.get(metric, 0.0) for r in baseline.run_scores]
        var_vals = [r.get(metric, 0.0) for r in variant.run_scores]

        delta = round(
            (variant.mean_scores.get(metric, 0.0)
             - baseline.mean_scores.get(metric, 0.0)),
            4,
        )
        deltas[metric] = delta

        if len(base_vals) >= 3 and sum(abs(b - v) for b, v in zip(base_vals, var_vals)) > 0:
            try:
                stat, p = wilcoxon(base_vals, var_vals, alternative="two-sided")
                p_values[metric] = round(float(p), 6)
            except Exception:
                p_values[metric] = 1.0
        else:
            p_values[metric] = 1.0

        effect_sizes[metric] = _cohens_d(base_vals, var_vals)

    return {
        "ablation_id": ablation_id,
        "description": entry.get("description", ""),
        "baseline_scores": baseline.mean_scores,
        "variant_scores": variant.mean_scores,
        "deltas": deltas,
        "p_values": p_values,
        "effect_sizes": effect_sizes,
        "primary_metric": primary_metric,
        "primary_delta": deltas.get(primary_metric, 0.0),
        "primary_p_value": p_values.get(primary_metric, 1.0),
    }


# ── Full Ablation Suite ────────────────────────────────────────────────────────

def run_all_ablations(
    dataset: list[dict],
    *,
    n_runs: int = 3,
) -> list[dict[str, Any]]:
    """Run baseline + all 6 ablation conditions and compare each to baseline.

    Args:
        dataset: Gold-standard dataset list.
        n_runs:  Repeated runs per condition (default 3).

    Returns:
        List of comparison dicts, one per ablation ID.
    """
    logger.info("Starting ablation study: %d experiments × %d runs", 6, n_runs)

    logger.info("Running baseline condition …")
    baseline = run_ablation_condition(
        "baseline", dataset, baseline=True, n_runs=n_runs
    )

    results: list[dict] = []
    for ablation_id in ABLATION_REGISTRY:
        logger.info("Running %s …", ablation_id)
        variant = run_ablation_condition(ablation_id, dataset, n_runs=n_runs)
        comparison = compare_conditions(baseline, variant)
        results.append(comparison)
        logger.info(
            "%s primary_metric=%s delta=%.4f p=%.4f",
            ablation_id,
            comparison["primary_metric"],
            comparison["primary_delta"],
            comparison["primary_p_value"],
        )

    return results


# ── Report Persistence ────────────────────────────────────────────────────────

def save_ablation_report(
    results: list[dict[str, Any]],
    output_dir: str = "reports",
) -> Path:
    """Persist the ablation comparison results to a timestamped JSON file.

    Args:
        results:    List of comparison dicts from :func:`run_all_ablations`.
        output_dir: Directory for output (created if absent).

    Returns:
        :class:`Path` to the saved report file.
    """
    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now(tz=timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    report_path = out / f"ablation_{timestamp}.json"
    payload = {
        "generated_at": timestamp,
        "n_experiments": len(results),
        "experiments": results,
    }
    report_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    logger.info("Ablation report saved → %s", report_path)
    return report_path


# ── CLI Entry Point ───────────────────────────────────────────────────────────

def _build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Run GraphRAG ablation study",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "--dataset",
        required=True,
        help="Path to gold-standard JSON dataset",
    )
    parser.add_argument(
        "--ablation",
        default="all",
        choices=[*list(ABLATION_REGISTRY.keys()), "all"],
        help="Ablation ID to run, or 'all' to run full suite",
    )
    parser.add_argument(
        "--runs",
        type=int,
        default=3,
        help="Number of repeated evaluation runs per condition",
    )
    parser.add_argument(
        "--output",
        default="reports",
        help="Directory for saving the ablation report",
    )
    return parser


def main() -> None:
    """CLI entry-point."""
    parser = _build_arg_parser()
    args = parser.parse_args()

    dataset = load_dataset(args.dataset)

    if args.ablation == "all":
        results = run_all_ablations(dataset, n_runs=args.runs)
    else:
        baseline = run_ablation_condition(
            args.ablation, dataset, baseline=True, n_runs=args.runs
        )
        variant = run_ablation_condition(
            args.ablation, dataset, n_runs=args.runs
        )
        results = [compare_conditions(baseline, variant)]

    report_path = save_ablation_report(results, output_dir=args.output)
    print(f"Ablation report saved to: {report_path}")


if __name__ == "__main__":
    main()
```

---

## 5. Tests

```python
"""Unit tests for src/evaluation/ablation_runner.py — UT-26"""

from __future__ import annotations

import json
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from src.evaluation.ablation_runner import (
    ABLATION_REGISTRY,
    AblationResult,
    _cohens_d,
    _mean_scores,
    compare_conditions,
    save_ablation_report,
)


# ── ABLATION_REGISTRY ─────────────────────────────────────────────────────────

class TestAblationRegistry:
    def test_all_six_ids_present(self) -> None:
        for i in range(1, 7):
            assert f"AB-0{i}" in ABLATION_REGISTRY

    def test_each_entry_has_required_keys(self) -> None:
        required = {"description", "flag", "value", "primary_metric"}
        for ablation_id, entry in ABLATION_REGISTRY.items():
            missing = required - entry.keys()
            assert not missing, f"{ablation_id} missing keys: {missing}"

    def test_ab01_disables_schema_enrichment(self) -> None:
        entry = ABLATION_REGISTRY["AB-01"]
        assert entry["flag"] == "ENABLE_SCHEMA_ENRICHMENT"
        assert entry["value"] is False

    def test_ab02_sets_vector_only(self) -> None:
        entry = ABLATION_REGISTRY["AB-02"]
        assert entry["flag"] == "RETRIEVAL_MODE"
        assert entry["value"] == "vector_only"

    def test_ab03_disables_healing(self) -> None:
        assert ABLATION_REGISTRY["AB-03"]["flag"] == "ENABLE_CYPHER_HEALING"

    def test_ab06_disables_hallucination_grader(self) -> None:
        assert ABLATION_REGISTRY["AB-06"]["flag"] == "ENABLE_HALLUCINATION_GRADER"


# ── _mean_scores ──────────────────────────────────────────────────────────────

class TestMeanScores:
    def test_single_run_returns_same_values(self) -> None:
        run_scores = [{"faithfulness": 0.9, "context_precision": 0.8}]
        means = _mean_scores(run_scores)
        assert means["faithfulness"] == pytest.approx(0.9)
        assert means["context_precision"] == pytest.approx(0.8)

    def test_averages_across_runs(self) -> None:
        run_scores = [
            {"faithfulness": 0.8},
            {"faithfulness": 0.9},
            {"faithfulness": 1.0},
        ]
        means = _mean_scores(run_scores)
        assert means["faithfulness"] == pytest.approx(0.9, abs=1e-4)

    def test_empty_returns_empty(self) -> None:
        assert _mean_scores([]) == {}


# ── _cohens_d ─────────────────────────────────────────────────────────────────

class TestCohensD:
    def test_no_difference_returns_zero(self) -> None:
        assert _cohens_d([0.9, 0.9, 0.9], [0.9, 0.9, 0.9]) == 0.0

    def test_positive_delta(self) -> None:
        # baseline higher than variant → positive d
        d = _cohens_d([1.0, 1.0, 1.0], [0.5, 0.5, 0.5])
        assert d > 0

    def test_single_sample_returns_zero(self) -> None:
        assert _cohens_d([0.9], [0.8]) == 0.0


# ── AblationResult ────────────────────────────────────────────────────────────

class TestAblationResult:
    def test_mean_scores_computed(self) -> None:
        run_scores = [
            {"faithfulness": 0.8, "context_precision": 0.7},
            {"faithfulness": 1.0, "context_precision": 0.9},
        ]
        result = AblationResult("AB-01", False, run_scores)
        assert result.mean_scores["faithfulness"] == pytest.approx(0.9, abs=1e-4)

    def test_to_dict_keys(self) -> None:
        result = AblationResult("AB-01", False, [{"faithfulness": 0.9}])
        d = result.to_dict()
        assert set(d.keys()) == {"ablation_id", "is_baseline", "run_scores", "mean_scores"}


# ── compare_conditions ────────────────────────────────────────────────────────

class TestCompareConditions:
    def _make_result(self, ablation_id: str, scores: list[dict], baseline: bool) -> AblationResult:
        return AblationResult(ablation_id, baseline, scores)

    def test_returns_required_keys(self) -> None:
        base_scores = [{"faithfulness": 0.95, "context_precision": 0.85, "context_recall": 0.90, "answer_relevancy": 0.85, "cypher_healing_rate": 0.80, "hitl_confidence_agreement": 0.90}] * 3
        var_scores = [{"faithfulness": 0.75, "context_precision": 0.65, "context_recall": 0.70, "answer_relevancy": 0.75, "cypher_healing_rate": 0.70, "hitl_confidence_agreement": 0.80}] * 3
        baseline = self._make_result("baseline", base_scores, True)
        variant = self._make_result("AB-06", var_scores, False)
        comparison = compare_conditions(baseline, variant)
        required = {"ablation_id", "deltas", "p_values", "effect_sizes", "primary_metric", "primary_delta"}
        assert required.issubset(comparison.keys())

    def test_negative_delta_for_ablation(self) -> None:
        base_scores = [{"faithfulness": 0.95}] * 3
        var_scores = [{"faithfulness": 0.80}] * 3
        baseline = self._make_result("baseline", base_scores, True)
        variant = self._make_result("AB-06", var_scores, False)
        comparison = compare_conditions(baseline, variant)
        assert comparison["deltas"]["faithfulness"] == pytest.approx(-0.15, abs=1e-3)

    def test_primary_metric_for_ab06_is_faithfulness(self) -> None:
        base_scores = [{"faithfulness": 0.95}] * 3
        var_scores = [{"faithfulness": 0.80}] * 3
        baseline = self._make_result("baseline", base_scores, True)
        variant = self._make_result("AB-06", var_scores, False)
        comparison = compare_conditions(baseline, variant)
        assert comparison["primary_metric"] == "faithfulness"


# ── save_ablation_report ──────────────────────────────────────────────────────

class TestSaveAblationReport:
    def test_creates_file(self, tmp_path: Path) -> None:
        results = [{"ablation_id": "AB-01", "deltas": {}, "p_values": {}}]
        path = save_ablation_report(results, output_dir=str(tmp_path))
        assert path.exists()

    def test_file_is_valid_json(self, tmp_path: Path) -> None:
        results = [{"ablation_id": "AB-02", "primary_delta": -0.1}]
        path = save_ablation_report(results, output_dir=str(tmp_path))
        payload = json.loads(path.read_text())
        assert "experiments" in payload
        assert payload["n_experiments"] == 1

    def test_filename_contains_timestamp(self, tmp_path: Path) -> None:
        path = save_ablation_report([], output_dir=str(tmp_path))
        assert "ablation_" in path.name
        assert path.suffix == ".json"
```

---

## 6. Smoke Test

```bash
# Dry-run against the fixtures dataset (single ablation, 1 run)
python -m src.evaluation.ablation_runner \
    --dataset tests/fixtures/gold_standard.json \
    --ablation AB-06 \
    --runs 1 \
    --output /tmp/ablation_smoke

# Verify report structure
python -c "
import json, pathlib, glob
reports = sorted(glob.glob('/tmp/ablation_smoke/ablation_*.json'))
assert reports, 'No report generated'
data = json.loads(pathlib.Path(reports[-1]).read_text())
print('experiments:', data['n_experiments'])
print('AB-06 primary_metric:', data['experiments'][0]['primary_metric'])
print('Ablation runner smoke test passed.')
"
```
