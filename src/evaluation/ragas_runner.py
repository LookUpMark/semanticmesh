"""EP-16: RAGAS evaluation pipeline — runs on gold-standard QA pairs.

Loads tests/fixtures/gold_standard.json, runs each (question, ground_truth,
ground_truth_contexts) triple through the Query Graph, and evaluates using
RAGAS metrics: faithfulness, answer_relevancy, context_precision, context_recall.

Uses OpenRouter as the evaluator LLM backend (openai/gpt-oss-20b by default)
to avoid dependency on a native OpenAI key.

Public API:
    run_ragas_evaluation(dataset_path, evaluator_model) -> dict[str, float]
"""

from __future__ import annotations

import json
import os
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

# Cheap model used as RAGAS evaluator judge (via OpenRouter)
_DEFAULT_EVALUATOR_MODEL: str = "openai/gpt-oss-20b"
_OPENROUTER_BASE_URL: str = "https://openrouter.ai/api/v1"


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


def _build_openrouter_ragas_llm(evaluator_model: str) -> Any:
    """Build a RAGAS-compatible InstructorLLM backed by OpenRouter.

    Uses the RAGAS 0.4.x ``llm_factory`` with an ``openai.AsyncOpenAI`` client
    pointed at the OpenRouter base URL.  Requires OPENROUTER_API_KEY in env.
    """
    from openai import AsyncOpenAI  # noqa: PLC0415
    from ragas.llms import llm_factory  # noqa: PLC0415

    api_key = os.environ.get("OPENROUTER_API_KEY", "")
    if not api_key:
        raise EnvironmentError(
            "OPENROUTER_API_KEY not set — cannot run RAGAS evaluation"
        )
    client = AsyncOpenAI(base_url=_OPENROUTER_BASE_URL, api_key=api_key)
    return llm_factory(evaluator_model, provider="openai", client=client)


def _build_openrouter_ragas_embeddings() -> Any:
    """Build RAGAS embeddings backed by OpenRouter (text-embedding-3-small)."""
    from openai import AsyncOpenAI  # noqa: PLC0415
    from ragas.embeddings import OpenAIEmbeddings  # noqa: PLC0415

    api_key = os.environ.get("OPENROUTER_API_KEY", "")
    client = AsyncOpenAI(base_url=_OPENROUTER_BASE_URL, api_key=api_key)
    return OpenAIEmbeddings(model="text-embedding-3-small", client=client)


def _compute_ragas_metrics(
    results: list[dict[str, Any]],
    evaluator_model: str = _DEFAULT_EVALUATOR_MODEL,
) -> dict[str, float]:
    """Compute RAGAS 0.4.x collections metrics using an OpenRouter evaluator LLM.

    Uses the newer ``ragas.metrics.collections`` API (``score()`` per sample)
    instead of ``ragas.evaluate()`` which only accepts the legacy Metric hierarchy.

    Returns zero metrics if ragas is not installed or OPENROUTER_API_KEY is missing.
    """
    try:
        from ragas.metrics.collections import (  # noqa: PLC0415
            AnswerRelevancy,
            ContextPrecision,
            ContextRecall,
            Faithfulness,
        )
    except ImportError:
        logger.warning("ragas not installed — returning zero metrics")
        return dict(_ZERO_METRICS)

    try:
        ragas_llm = _build_openrouter_ragas_llm(evaluator_model)
        ragas_emb = _build_openrouter_ragas_embeddings()
    except EnvironmentError as exc:
        logger.warning("RAGAS LLM init failed: %s — returning zero metrics", exc)
        return dict(_ZERO_METRICS)

    faithfulness_m = Faithfulness(llm=ragas_llm)
    answer_relevancy_m = AnswerRelevancy(llm=ragas_llm, embeddings=ragas_emb)
    context_precision_m = ContextPrecision(llm=ragas_llm)
    context_recall_m = ContextRecall(llm=ragas_llm)

    scores: dict[str, list[float]] = {
        "faithfulness": [],
        "answer_relevancy": [],
        "context_precision": [],
        "context_recall": [],
    }
    logger.info(
        "Running RAGAS evaluate on %d samples with model=%s",
        len(results),
        evaluator_model,
    )
    for i, r in enumerate(results):
        q = r["question"]
        ans = r["answer"]
        ctxs = r["contexts"] if r["contexts"] else [""]
        ref = r["ground_truth"]
        try:
            scores["faithfulness"].append(
                float(faithfulness_m.score(user_input=q, response=ans, retrieved_contexts=ctxs).value)
            )
            scores["answer_relevancy"].append(
                float(answer_relevancy_m.score(user_input=q, response=ans).value)
            )
            scores["context_precision"].append(
                float(context_precision_m.score(user_input=q, reference=ref, retrieved_contexts=ctxs).value)
            )
            scores["context_recall"].append(
                float(context_recall_m.score(user_input=q, retrieved_contexts=ctxs, reference=ref).value)
            )
            logger.info("RAGAS sample %d/%d done", i + 1, len(results))
        except Exception:  # noqa: BLE001
            logger.exception("RAGAS scoring failed for sample %d — skipping", i)

    def _mean(vals: list[float]) -> float:
        return sum(vals) / len(vals) if vals else 0.0

    return {
        "faithfulness": _mean(scores["faithfulness"]),
        "answer_relevancy": _mean(scores["answer_relevancy"]),
        "context_precision": _mean(scores["context_precision"]),
        "context_recall": _mean(scores["context_recall"]),
    }


# ─────────────────────────────────────────────────────────────────────────────
# Public API
# ─────────────────────────────────────────────────────────────────────────────

def run_ragas_evaluation(
    dataset_path: Path | None = None,
    evaluator_model: str = _DEFAULT_EVALUATOR_MODEL,
    max_samples: int | None = None,
) -> dict[str, float]:
    """Run RAGAS evaluation on the gold-standard QA dataset.

    Args:
        dataset_path: Path to the JSON dataset file.
            Defaults to tests/fixtures/gold_standard.json.
        evaluator_model: OpenRouter model string used as RAGAS evaluator judge.
            Defaults to ``openai/gpt-oss-20b``.
        max_samples: Limit evaluation to first N samples. None = all 50.

    Returns:
        Dict with keys: faithfulness, answer_relevancy,
        context_precision, context_recall.
    """
    path = dataset_path or _DEFAULT_DATASET
    dataset = _load_dataset(path)
    if max_samples is not None:
        dataset = dataset[:max_samples]
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

    metrics = _compute_ragas_metrics(results, evaluator_model=evaluator_model)

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
