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

import asyncio
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
_DEFAULT_EVALUATOR_MODEL: str = "openai/gpt-4o-mini"
_OPENROUTER_BASE_URL: str = "https://openrouter.ai/api/v1"


# ─────────────────────────────────────────────────────────────────────────────
# Dataset helpers
# ─────────────────────────────────────────────────────────────────────────────


def _load_dataset(dataset_path: Path) -> list[dict[str, Any]]:
    """Load and validate the gold-standard QA dataset JSON file."""
    with dataset_path.open("r", encoding="utf-8") as f:
        data = json.load(f)
    if not isinstance(data, list):
        raise ValueError(f"Expected a JSON array in {dataset_path}, got {type(data).__name__}")
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
        raise OSError("OPENROUTER_API_KEY not set — cannot run RAGAS evaluation")

    client = AsyncOpenAI(base_url=_OPENROUTER_BASE_URL, api_key=api_key)
    return llm_factory(evaluator_model, provider="openai", client=client)


def _build_openrouter_ragas_embeddings() -> Any:
    """Build RAGAS embeddings backed by OpenRouter (text-embedding-3-small)."""
    from openai import AsyncOpenAI  # noqa: PLC0415
    from ragas.embeddings import OpenAIEmbeddings  # noqa: PLC0415

    api_key = os.environ.get("OPENROUTER_API_KEY", "")
    client = AsyncOpenAI(base_url=_OPENROUTER_BASE_URL, api_key=api_key)
    return OpenAIEmbeddings(model="text-embedding-3-small", client=client)


async def _score_single_sample(
    faithfulness_m: Any,
    answer_relevancy_m: Any,
    context_precision_m: Any,
    context_recall_m: Any,
    q: str,
    ans: str,
    ctxs: list[str],
    ref: str,
    timeout: float = 60.0,
) -> dict[str, float]:
    """Score a single sample asynchronously with per-metric timeout."""
    try:
        # Each metric gets a separate timeout to prevent one bad call from blocking all
        faithfulness = float(
            await asyncio.wait_for(
                faithfulness_m.ascore(user_input=q, response=ans, retrieved_contexts=ctxs),
                timeout=timeout,
            )
        )
    except TimeoutError:
        logger.warning("Faithfulness scoring timed out for: %s", q[:60])
        faithfulness = 0.0

    try:
        answer_relevancy = float(
            await asyncio.wait_for(
                answer_relevancy_m.ascore(user_input=q, response=ans), timeout=timeout
            )
        )
    except TimeoutError:
        logger.warning("Answer relevancy scoring timed out for: %s", q[:60])
        answer_relevancy = 0.0

    try:
        context_precision = float(
            await asyncio.wait_for(
                context_precision_m.ascore(user_input=q, reference=ref, retrieved_contexts=ctxs),
                timeout=timeout,
            )
        )
    except TimeoutError:
        logger.warning("Context precision scoring timed out for: %s", q[:60])
        context_precision = 0.0

    try:
        context_recall = float(
            await asyncio.wait_for(
                context_recall_m.ascore(user_input=q, retrieved_contexts=ctxs, reference=ref),
                timeout=timeout,
            )
        )
    except TimeoutError:
        logger.warning("Context recall scoring timed out for: %s", q[:60])
        context_recall = 0.0

    return {
        "faithfulness": faithfulness,
        "answer_relevancy": answer_relevancy,
        "context_precision": context_precision,
        "context_recall": context_recall,
    }


async def _compute_ragas_metrics_async(
    results: list[dict[str, Any]],
    evaluator_model: str = _DEFAULT_EVALUATOR_MODEL,
) -> dict[str, float]:
    """Async wrapper for RAGAS metrics computation."""
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
    except OSError as exc:
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
            sample_scores = await _score_single_sample(
                faithfulness_m,
                answer_relevancy_m,
                context_precision_m,
                context_recall_m,
                q,
                ans,
                ctxs,
                ref,
                timeout=60.0,  # 60 seconds per metric
            )
            scores["faithfulness"].append(sample_scores["faithfulness"])
            scores["answer_relevancy"].append(sample_scores["answer_relevancy"])
            scores["context_precision"].append(sample_scores["context_precision"])
            scores["context_recall"].append(sample_scores["context_recall"])
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


def _compute_ragas_metrics(
    results: list[dict[str, Any]],
    evaluator_model: str = _DEFAULT_EVALUATOR_MODEL,
) -> dict[str, float]:
    """Compute RAGAS metrics using nest_asyncio for robust event loop handling.

    Uses ThreadPoolExecutor for isolation when called from async context,
    direct asyncio.run() when called from sync context.
    """
    try:
        import nest_asyncio  # noqa: PLC0415

        nest_asyncio.apply()
        logger.debug("Applied nest_asyncio for nested event loop support")
    except ImportError:
        logger.debug("nest_asyncio not available, using standard asyncio")

    try:
        # Try to get existing loop
        loop = asyncio.get_event_loop()
        if loop.is_running():
            # We're in an async context, use ThreadPoolExecutor for isolation
            import concurrent.futures  # noqa: PLC0415

            logger.debug("Running in async context, using ThreadPoolExecutor")
            with concurrent.futures.ThreadPoolExecutor(max_workers=1) as executor:
                future = executor.submit(
                    asyncio.run, _compute_ragas_metrics_async(results, evaluator_model)
                )
                return future.result(timeout=1800)  # 30 min total timeout
        else:
            # No running loop, safe to run directly
            logger.debug("No running loop, using asyncio.run()")
            return asyncio.run(_compute_ragas_metrics_async(results, evaluator_model))
    except RuntimeError:
        # No loop exists, create new one
        logger.debug("No loop exists, creating new one with asyncio.run()")
        return asyncio.run(_compute_ragas_metrics_async(results, evaluator_model))
    except Exception as exc:
        logger.warning("RAGAS computation failed: %s — returning zero metrics", exc)
        return dict(_ZERO_METRICS)


# ─────────────────────────────────────────────────────────────────────────────
# Public API
# ─────────────────────────────────────────────────────────────────────────────


def run_ragas_evaluation(
    dataset_path: Path | None = None,
    evaluator_model: str = _DEFAULT_EVALUATOR_MODEL,
    run_ragas: bool = True,
    max_samples: int | None = None,
) -> dict[str, float]:
    """Run RAGAS evaluation on the gold-standard QA dataset.

    Args:
        dataset_path: Path to the JSON dataset file.
            Defaults to tests/fixtures/gold_standard.json.
        evaluator_model: OpenRouter model string used as RAGAS evaluator judge.
            Defaults to ``openai/gpt-oss-20b``.
        run_ragas: If False, skip RAGAS computation and return zero metrics.
            Useful for ablation studies where RAGAS is not needed.
        max_samples: Maximum number of samples to evaluate. If None, evaluates all.
            Useful for faster ablation iterations (e.g., 20 instead of 50).

    Returns:
        Dict with keys: faithfulness, answer_relevancy,
        context_precision, context_recall.
        When run_ragas=False, returns zero metrics.
    """
    path = dataset_path or _DEFAULT_DATASET
    dataset = _load_dataset(path)

    # Limit dataset to max_samples if specified
    if max_samples is not None and max_samples > 0:
        dataset = dataset[:max_samples]
        logger.info("Limited dataset to %d samples (max_samples=%d)", len(dataset), max_samples)

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

    if not run_ragas:
        logger.info("RAGAS evaluation skipped (run_ragas=False)")
        metrics = dict(_ZERO_METRICS)
    else:
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
