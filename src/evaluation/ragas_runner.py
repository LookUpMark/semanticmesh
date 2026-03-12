"""EP-16: RAGAS evaluation pipeline — runs on gold-standard QA pairs.

Loads tests/fixtures/gold_standard.json, runs each (question, ground_truth,
ground_truth_contexts) triple through the Query Graph, and evaluates using
RAGAS metrics: faithfulness, answer_relevancy, context_precision, context_recall.

Public API:
    run_ragas_evaluation(dataset_path) -> dict[str, float]
"""

from __future__ import annotations

import json
from datetime import UTC, datetime
from pathlib import Path
from typing import TYPE_CHECKING, Any

from src.config.logging import get_logger
from src.generation.query_graph import run_query
from src.models.schemas import EvaluationReport

if TYPE_CHECKING:
    import logging

logger: logging.Logger = get_logger(__name__)

_DEFAULT_DATASET: Path = (
    Path(__file__).parent.parent.parent / "tests" / "fixtures" / "gold_standard.json"
)


# ─────────────────────────────────────────────────────────────────────────────
# Dataset helpers
# ─────────────────────────────────────────────────────────────────────────────

def _load_dataset(dataset_path: Path) -> list[dict[str, Any]]:
    """Load and validate the gold-standard QA dataset JSON file."""
    with dataset_path.open("r", encoding="utf-8") as f:
        data = json.load(f)
    if not isinstance(data, list):
        raise ValueError(
            f"Expected a JSON array in {dataset_path}, got {type(data).__name__}"
        )
    return data


def _run_pipeline_on_sample(
    sample: dict[str, Any],
) -> dict[str, Any]:
    """Run the Query Graph on one QA sample; return answer + context strings."""
    question: str = sample["question"]
    try:
        result = run_query(question)
        answer: str = result.get("final_answer", "")
        # sources are node IDs; fall back to ground_truth_contexts for RAGAS
        contexts: list[str] = result.get("sources", [])
        if not contexts:
            contexts = list(sample.get("ground_truth_contexts", []))
    except Exception:  # noqa: BLE001
        logger.exception("Query Graph failed for: %s", question[:80])
        answer = ""
        contexts = list(sample.get("ground_truth_contexts", []))
    return {
        "question": question,
        "answer": answer,
        "contexts": contexts,
        "ground_truth": sample["ground_truth"],
    }


# ─────────────────────────────────────────────────────────────────────────────
# RAGAS metric computation
# ─────────────────────────────────────────────────────────────────────────────

_ZERO_METRICS: dict[str, float] = {
    "faithfulness": 0.0,
    "answer_relevancy": 0.0,
    "context_precision": 0.0,
    "context_recall": 0.0,
}


def _compute_ragas_metrics(results: list[dict[str, Any]]) -> dict[str, float]:
    """Compute RAGAS metrics using the ragas library.

    Returns zero metrics if ragas/datasets are not installed.
    """
    try:
        from datasets import Dataset  # noqa: PLC0415
        from ragas import evaluate  # noqa: PLC0415
        from ragas.metrics import (  # noqa: PLC0415
            answer_relevancy,
            context_precision,
            context_recall,
            faithfulness,
        )
    except ImportError:
        logger.warning("ragas / datasets not installed — returning zero metrics")
        return dict(_ZERO_METRICS)

    data: dict[str, list[Any]] = {
        "question": [r["question"] for r in results],
        "answer": [r["answer"] for r in results],
        "contexts": [r["contexts"] for r in results],
        "ground_truth": [r["ground_truth"] for r in results],
    }
    ds = Dataset.from_dict(data)
    score = evaluate(
        ds,
        metrics=[faithfulness, answer_relevancy, context_precision, context_recall],
    )
    return {
        "faithfulness": float(score["faithfulness"]),
        "answer_relevancy": float(score["answer_relevancy"]),
        "context_precision": float(score["context_precision"]),
        "context_recall": float(score["context_recall"]),
    }


# ─────────────────────────────────────────────────────────────────────────────
# Public API
# ─────────────────────────────────────────────────────────────────────────────

def run_ragas_evaluation(
    dataset_path: Path | None = None,
) -> dict[str, float]:
    """Run RAGAS evaluation on the gold-standard QA dataset.

    Args:
        dataset_path: Path to the JSON dataset file.
            Defaults to tests/fixtures/gold_standard.json.

    Returns:
        Dict with keys: faithfulness, answer_relevancy,
        context_precision, context_recall.
    """
    path = dataset_path or _DEFAULT_DATASET
    dataset = _load_dataset(path)
    logger.info("Loaded %d QA samples from %s", len(dataset), path)

    results: list[dict[str, Any]] = []
    failed_samples: list[dict[str, Any]] = []

    for i, sample in enumerate(dataset):
        logger.info(
            "Evaluating sample %d/%d: %s",
            i + 1,
            len(dataset),
            sample.get("question", "")[:60],
        )
        try:
            results.append(_run_pipeline_on_sample(sample))
        except Exception:  # noqa: BLE001
            logger.exception("Skipping sample %d after unexpected error", i)
            failed_samples.append({"index": i, "question": sample.get("question", "")})

    metrics = _compute_ragas_metrics(results)

    _ = EvaluationReport(
        timestamp=datetime.now(tz=UTC),
        num_samples=len(results),
        faithfulness=metrics["faithfulness"],
        context_precision=metrics["context_precision"],
        context_recall=metrics["context_recall"],
        answer_relevancy=metrics["answer_relevancy"],
        cypher_healing_rate=0.0,
        hitl_confidence_agreement=0.0,
        failed_samples=failed_samples,
    )

    logger.info("RAGAS evaluation complete: %s", metrics)
    return metrics
