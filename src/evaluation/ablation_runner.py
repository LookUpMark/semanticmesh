"""EP-16: Ablation experiment runner.

Implements run_ablation(experiment_id) which:
  1. Looks up the ablation configuration for the given AB-XX id
  2. Overrides the relevant Settings flags via environment variables
  3. Clears the settings lru_cache so new values take effect
  4. Runs the appropriate evaluation pipeline
  5. Restores the original environment and clears the cache again
  6. Returns a dict[str, float] of measured metrics

Also provides:
  - run_all_ablations() — runs every experiment in ABLATION_MATRIX
  - save_ablation_report() — persists results to a JSON file
  - main() — CLI entry point for ``python -m src.evaluation.ablation_runner``

See docs/draft/ABLATION.md for the full experiment plan.
"""

from __future__ import annotations

import json
import os
from contextlib import contextmanager
from datetime import UTC, datetime
from pathlib import Path
from typing import TYPE_CHECKING, Any

from src.config.logging import get_logger
from src.config.settings import get_settings
from src.evaluation.ragas_runner import run_ragas_evaluation

if TYPE_CHECKING:
    import logging
    from collections.abc import Generator

logger: logging.Logger = get_logger(__name__)


# ─────────────────────────────────────────────────────────────────────────────
# Ablation matrix — all 6 experiments (AB-01 … AB-06)
# ─────────────────────────────────────────────────────────────────────────────

ABLATION_MATRIX: dict[str, dict[str, Any]] = {
    "AB-01": {
        "description": "Schema Enrichment disabled — measures downstream retrieval impact",
        "env_overrides": {"ENABLE_SCHEMA_ENRICHMENT": "false"},
        "primary_metric": "context_precision",
    },
    "AB-02": {
        "description": "Vector-only retrieval — no BM25, no cross-encoder reranker",
        "env_overrides": {"RETRIEVAL_MODE": "vector", "ENABLE_RERANKER": "false"},
        "primary_metric": "context_precision",
    },
    "AB-03": {
        "description": "Cypher Healing disabled — immediate fail on syntax error",
        "env_overrides": {"ENABLE_CYPHER_HEALING": "false"},
        "primary_metric": "faithfulness",
    },
    "AB-04": {
        "description": "Actor-Critic Validation disabled — accept all mapping proposals",
        "env_overrides": {"ENABLE_CRITIC_VALIDATION": "false"},
        "primary_metric": "context_precision",
    },
    "AB-05": {
        "description": "Cross-Encoder Reranker disabled — raw hybrid pool ranking",
        "env_overrides": {"ENABLE_RERANKER": "false"},
        "primary_metric": "context_precision",
    },
    "AB-06": {
        "description": "Hallucination Grader disabled — return first answer without grading",
        "env_overrides": {"ENABLE_HALLUCINATION_GRADER": "false"},
        "primary_metric": "faithfulness",
    },
}


# ─────────────────────────────────────────────────────────────────────────────
# Settings override context manager
# ─────────────────────────────────────────────────────────────────────────────

@contextmanager
def _settings_override(
    env_overrides: dict[str, str],
) -> Generator[None, None, None]:
    """Context manager that temporarily overrides env vars and clears the
    Settings lru_cache before and after the block.
    """
    saved: dict[str, str | None] = {
        k: os.environ.get(k) for k in env_overrides
    }
    try:
        os.environ.update(env_overrides)
        get_settings.cache_clear()
        yield
    finally:
        for k, v in saved.items():
            if v is None:
                os.environ.pop(k, None)
            else:
                os.environ[k] = v
        get_settings.cache_clear()


# ─────────────────────────────────────────────────────────────────────────────
# Public API
# ─────────────────────────────────────────────────────────────────────────────

def run_ablation(
    experiment_id: str,
    dataset_path: Path | None = None,
) -> dict[str, float]:
    """Run a single ablation experiment and return the measured metrics.

    Args:
        experiment_id: One of AB-01 … AB-06.
        dataset_path:  Path to the gold-standard QA JSON file.
            Defaults to tests/fixtures/gold_standard.json.

    Returns:
        Dict of metric name → float, as returned by run_ragas_evaluation.

    Raises:
        ValueError: if experiment_id is not in ABLATION_MATRIX.
    """
    if experiment_id not in ABLATION_MATRIX:
        known = ", ".join(sorted(ABLATION_MATRIX))
        raise ValueError(
            f"Unknown experiment '{experiment_id}'. Known: {known}"
        )

    config = ABLATION_MATRIX[experiment_id]
    description: str = config["description"]
    env_overrides: dict[str, str] = config["env_overrides"]

    logger.info("Starting ablation %s: %s", experiment_id, description)
    logger.info("Env overrides: %s", env_overrides)

    with _settings_override(env_overrides):
        metrics = run_ragas_evaluation(dataset_path)

    logger.info("Ablation %s complete: %s", experiment_id, metrics)
    return metrics


def run_all_ablations(
    dataset_path: Path | None = None,
) -> dict[str, dict[str, float]]:
    """Run every experiment in ABLATION_MATRIX and return all results.

    Args:
        dataset_path: Path to the gold-standard QA JSON file.
            Defaults to tests/fixtures/gold_standard.json.

    Returns:
        Mapping of experiment_id -> metric dict, ordered AB-01 ... AB-06.
    """
    results: dict[str, dict[str, float]] = {}
    for experiment_id in ABLATION_MATRIX:
        logger.info("Running ablation experiment %s ...", experiment_id)
        results[experiment_id] = run_ablation(experiment_id, dataset_path=dataset_path)
    logger.info("All ablation experiments complete.")
    return results


def save_ablation_report(
    results: dict[str, dict[str, float]],
    output_dir: Path | str = "ablation_reports",
) -> Path:
    """Persist ablation results to a timestamped JSON file.

    Args:
        results: Mapping of experiment_id -> metric dict.
        output_dir: Directory in which to write the report.
            Created automatically if it does not exist.

    Returns:
        Path to the written file.
    """
    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)
    ts = datetime.now(tz=UTC).strftime("%Y%m%dT%H%M%SZ")
    file_path = out / f"ablation_report_{ts}.json"
    payload: dict[str, Any] = {
        "timestamp": ts,
        "experiments": results,
    }
    file_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    logger.info("Ablation report saved to '%s'.", file_path)
    return file_path


# ---------------------------------------------------------------------------
# CLI entry point
# ---------------------------------------------------------------------------

def main() -> None:
    """CLI entry point for running ablation studies.

    Usage::

        python -m src.evaluation.ablation_runner [--ablation AB-05] [--dataset PATH] [--output DIR]
    """
    import argparse  # noqa: PLC0415

    parser = argparse.ArgumentParser(
        description="Run GraphRAG ablation studies using RAGAS.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "--ablation",
        default="all",
        choices=[*sorted(ABLATION_MATRIX), "all"],
        help="Ablation experiment ID to run, or 'all' for the full suite.",
    )
    parser.add_argument(
        "--dataset",
        default=None,
        help="Path to the gold-standard JSON dataset file.",
    )
    parser.add_argument(
        "--output",
        default="ablation_reports",
        help="Directory for saving the ablation report.",
    )
    args = parser.parse_args()

    dataset_path: Path | None = Path(args.dataset) if args.dataset else None

    if args.ablation == "all":
        results = run_all_ablations(dataset_path=dataset_path)
    else:
        metrics = run_ablation(args.ablation, dataset_path=dataset_path)
        results = {args.ablation: metrics}

    report_path = save_ablation_report(results, output_dir=args.output)
    print(f"Ablation report saved: {report_path}")
    print(json.dumps(results, indent=2))


if __name__ == "__main__":
    main()
