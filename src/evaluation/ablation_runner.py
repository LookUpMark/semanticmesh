"""EP-16: Ablation experiment runner.

Implements run_ablation(experiment_id) which:
  1. Looks up the ablation configuration for the given AB-XX id
  2. Overrides the relevant Settings flags via environment variables
  3. Clears the settings lru_cache so new values take effect
  4. Runs the appropriate evaluation pipeline
  5. Restores the original environment and clears the cache again
  6. Returns a dict[str, float] of measured metrics

See docs/draft/ABLATION.md for the full experiment plan.
"""

from __future__ import annotations

import os
from contextlib import contextmanager
from typing import TYPE_CHECKING, Any

from src.config.logging import get_logger
from src.config.settings import get_settings
from src.evaluation.ragas_runner import run_ragas_evaluation

if TYPE_CHECKING:
    import logging
    from collections.abc import Generator
    from pathlib import Path

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
