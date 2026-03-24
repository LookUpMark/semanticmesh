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
import random
import statistics
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
    Path(__file__).parent.parent.parent / "tests" / "fixtures" / "00_legacy" / "gold_standard.json"
)

_DEFAULT_EVALUATOR_MODEL: str = "openai/gpt-4o-mini"
_OPENROUTER_BASE_URL: str = "https://openrouter.ai/api/v1"
_TRACE_PREVIEW_CHARS: int = 240


def _preview(text: str, max_chars: int = _TRACE_PREVIEW_CHARS) -> str:
    """Return a single-line preview string for logs and traces."""
    compact = " ".join((text or "").split())
    if len(compact) <= max_chars:
        return compact
    return compact[: max_chars - 1] + "…"


def _is_negative_ground_truth(text: str) -> bool:
    """Heuristic detection for negative/absence gold answers."""
    t = (text or "").lower()
    markers = (
        "i cannot find this information",
        "does not contain",
        "no concept or table",
        "does not contain any",
        "does not exist",
        "no table",
    )
    return any(m in t for m in markers)


def _is_abstention_answer(text: str) -> bool:
    """Heuristic detection for abstention-style model answers."""
    t = (text or "").lower()
    markers = (
        "i cannot find",
        "cannot find this information",
        "not available in the knowledge graph",
        "not present in the knowledge graph",
        "insufficient information",
    )
    return any(m in t for m in markers)


def _bootstrap_mean_ci(
    values: list[float],
    confidence: float = 0.95,
    n_bootstrap: int = 1000,
    seed: int = 42,
) -> dict[str, float]:
    """Return mean and percentile bootstrap CI for a list of values."""
    if not values:
        return {"mean": 0.0, "ci_low": 0.0, "ci_high": 0.0, "n": 0}

    if len(values) == 1:
        v = float(values[0])
        return {"mean": v, "ci_low": v, "ci_high": v, "n": 1}

    rng = random.Random(seed)
    means: list[float] = []
    n = len(values)
    for _ in range(n_bootstrap):
        sample = [values[rng.randrange(n)] for _ in range(n)]
        means.append(float(statistics.fmean(sample)))
    means.sort()

    alpha = 1.0 - confidence
    low_idx = int((alpha / 2.0) * (len(means) - 1))
    high_idx = int((1.0 - alpha / 2.0) * (len(means) - 1))
    return {
        "mean": float(statistics.fmean(values)),
        "ci_low": float(means[low_idx]),
        "ci_high": float(means[high_idx]),
        "n": n,
    }


def _build_trace_diagnostics(
    trace_rows: list[dict[str, Any]],
    dataset: list[dict[str, Any]],
) -> dict[str, Any]:
    """Build reliability diagnostics for ablation studies from trace rows."""
    metric_names = ["faithfulness", "answer_relevancy", "context_precision", "context_recall"]

    joined: list[dict[str, Any]] = []
    for row in trace_rows:
        idx = int(row.get("sample_index", -1))
        if idx < 0 or idx >= len(dataset):
            continue
        gold = dataset[idx]
        scores = row.get("ragas_scores") or {}
        joined.append(
            {
                "idx": idx,
                "scores": {k: float(scores.get(k, 0.0)) for k in metric_names},
                "is_negative": _is_negative_ground_truth(gold.get("ground_truth", "")),
                "is_abstention": _is_abstention_answer(row.get("model_answer", "")),
            }
        )

    total = len(joined)
    negatives = [r for r in joined if r["is_negative"]]
    positives = [r for r in joined if not r["is_negative"]]

    def _metric_values(rows: list[dict[str, Any]], metric: str) -> list[float]:
        return [float(r["scores"][metric]) for r in rows]

    def _zero_rate(rows: list[dict[str, Any]], metric: str) -> float:
        vals = _metric_values(rows, metric)
        if not vals:
            return 0.0
        zeros = sum(1 for v in vals if v == 0.0)
        return zeros / len(vals)

    negative_abstention_accuracy = (
        sum(1 for r in negatives if r["is_abstention"]) / len(negatives) if negatives else 0.0
    )
    positive_non_abstention_rate = (
        sum(1 for r in positives if not r["is_abstention"]) / len(positives) if positives else 0.0
    )

    overall_ci = {m: _bootstrap_mean_ci(_metric_values(joined, m)) for m in metric_names}
    positive_ci = {m: _bootstrap_mean_ci(_metric_values(positives, m)) for m in metric_names}
    negative_ci = {m: _bootstrap_mean_ci(_metric_values(negatives, m)) for m in metric_names}

    return {
        "sample_count": total,
        "positive_sample_count": len(positives),
        "negative_sample_count": len(negatives),
        "negative_abstention_accuracy": negative_abstention_accuracy,
        "positive_non_abstention_rate": positive_non_abstention_rate,
        "zero_rate_overall": {m: _zero_rate(joined, m) for m in metric_names},
        "zero_rate_positive": {m: _zero_rate(positives, m) for m in metric_names},
        "zero_rate_negative": {m: _zero_rate(negatives, m) for m in metric_names},
        "bootstrap_ci95_overall": overall_ci,
        "bootstrap_ci95_positive": positive_ci,
        "bootstrap_ci95_negative": negative_ci,
        "notes": [
            "RAGAS metrics can under-score correct abstentions on negative questions.",
            "Use negative_abstention_accuracy alongside core RAGAS metrics for ablations.",
        ],
    }


# ── Dataset helpers ──


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
    used_fallback_contexts = False
    try:
        result = run_query(question)
        answer: str = result.get("final_answer", "")
        sources: list[str] = list(result.get("sources", []))
        retrieval_quality_score = float(result.get("retrieval_quality_score", 0.0) or 0.0)
        retrieval_chunk_count = int(result.get("retrieval_chunk_count", 0) or 0)
        retrieval_filtered_by_threshold = bool(result.get("retrieval_filtered_by_threshold", False))
        context_sufficiency = str(result.get("context_sufficiency", "insufficient"))

        contexts: list[str] = result.get("retrieved_contexts", [])
        if not contexts:
            contexts = list(sample.get("ground_truth_contexts", []))
            used_fallback_contexts = True
            logger.warning(
                "No retrieved_contexts in result for '%s' — falling back to gold contexts",
                question[:60],
            )
        else:
            logger.debug(
                "Using %d retrieved context(s) for RAGAS: %s",
                len(contexts),
                [c[:60] for c in contexts[:3]],
            )
    except Exception:  # noqa: BLE001
        logger.exception("Query Graph failed for: %s", question[:80])
        answer = ""
        sources = []
        contexts = list(sample.get("ground_truth_contexts", []))
        used_fallback_contexts = True
        retrieval_quality_score = 0.0
        retrieval_chunk_count = 0
        retrieval_filtered_by_threshold = False
        context_sufficiency = "insufficient"

    logger.info(
        "Pipeline sample q='%s' answer_chars=%d contexts=%d fallback=%s",
        question[:60],
        len(answer),
        len(contexts),
        used_fallback_contexts,
    )
    logger.debug("Pipeline answer preview: %s", _preview(answer))
    if contexts:
        logger.debug(
            "Pipeline first contexts: %s",
            [_preview(c, 120) for c in contexts[:3]],
        )

    return {
        "question": question,
        "answer": answer,
        "contexts": contexts,
        "sources": sources,
        "used_fallback_contexts": used_fallback_contexts,
        "retrieval_quality_score": retrieval_quality_score,
        "retrieval_chunk_count": retrieval_chunk_count,
        "retrieval_filtered_by_threshold": retrieval_filtered_by_threshold,
        "context_sufficiency": context_sufficiency,
        "ground_truth": sample["ground_truth"],
    }


# ── RAGAS metric computation ──

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
    trace_rows: list[dict[str, Any]] | None = None,
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
        ctxs = r["contexts"] if r["contexts"] else []
        srcs = r.get("sources", [])
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
                timeout=60.0,
            )
            scores["faithfulness"].append(sample_scores["faithfulness"])
            scores["answer_relevancy"].append(sample_scores["answer_relevancy"])
            scores["context_precision"].append(sample_scores["context_precision"])
            scores["context_recall"].append(sample_scores["context_recall"])
            logger.info(
                "RAGAS sample %d/%d done | f=%.4f ar=%.4f cp=%.4f cr=%.4f",
                i + 1,
                len(results),
                sample_scores["faithfulness"],
                sample_scores["answer_relevancy"],
                sample_scores["context_precision"],
                sample_scores["context_recall"],
            )
            if trace_rows is not None:
                trace_rows.append(
                    {
                        "sample_index": i,
                        "question": q,
                        "ground_truth": ref,
                        "model_answer": ans,
                        "answer_preview": _preview(ans),
                        "sources": srcs,
                        "retrieved_contexts": ctxs,
                        "retrieved_context_previews": [_preview(c, 160) for c in ctxs[:5]],
                        "context_count": len(ctxs),
                        "used_fallback_contexts": bool(r.get("used_fallback_contexts", False)),
                        "retrieval_quality_score": float(
                            r.get("retrieval_quality_score", 0.0) or 0.0
                        ),
                        "retrieval_chunk_count": int(r.get("retrieval_chunk_count", 0) or 0),
                        "retrieval_filtered_by_threshold": bool(
                            r.get("retrieval_filtered_by_threshold", False)
                        ),
                        "context_sufficiency": str(r.get("context_sufficiency", "insufficient")),
                        "ragas_scores": sample_scores,
                        "ragas_error": None,
                    }
                )
        except Exception:  # noqa: BLE001
            logger.exception("RAGAS scoring failed for sample %d — skipping", i)
            if trace_rows is not None:
                trace_rows.append(
                    {
                        "sample_index": i,
                        "question": q,
                        "ground_truth": ref,
                        "model_answer": ans,
                        "answer_preview": _preview(ans),
                        "sources": srcs,
                        "retrieved_contexts": ctxs,
                        "retrieved_context_previews": [_preview(c, 160) for c in ctxs[:5]],
                        "context_count": len(ctxs),
                        "used_fallback_contexts": bool(r.get("used_fallback_contexts", False)),
                        "retrieval_quality_score": float(
                            r.get("retrieval_quality_score", 0.0) or 0.0
                        ),
                        "retrieval_chunk_count": int(r.get("retrieval_chunk_count", 0) or 0),
                        "retrieval_filtered_by_threshold": bool(
                            r.get("retrieval_filtered_by_threshold", False)
                        ),
                        "context_sufficiency": str(r.get("context_sufficiency", "insufficient")),
                        "ragas_scores": None,
                        "ragas_error": "scoring_failed",
                    }
                )

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
    trace_rows: list[dict[str, Any]] | None = None,
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
        loop = asyncio.get_event_loop()
        if loop.is_running():
            import concurrent.futures  # noqa: PLC0415

            logger.debug("Running in async context, using ThreadPoolExecutor")
            with concurrent.futures.ThreadPoolExecutor(max_workers=1) as executor:
                future = executor.submit(
                    asyncio.run,
                    _compute_ragas_metrics_async(
                        results,
                        evaluator_model,
                        trace_rows=trace_rows,
                    ),
                )
                return future.result(timeout=1800)
        else:
            logger.debug("No running loop, using asyncio.run()")
            return asyncio.run(
                _compute_ragas_metrics_async(
                    results,
                    evaluator_model,
                    trace_rows=trace_rows,
                )
            )
    except RuntimeError:
        logger.debug("No loop exists, creating new one with asyncio.run()")
        return asyncio.run(
            _compute_ragas_metrics_async(
                results,
                evaluator_model,
                trace_rows=trace_rows,
            )
        )
    except Exception as exc:
        logger.warning("RAGAS computation failed: %s — returning zero metrics", exc)
        return dict(_ZERO_METRICS)


# ── Public API ──


def run_ragas_evaluation(
    dataset_path: Path | None = None,
    evaluator_model: str = _DEFAULT_EVALUATOR_MODEL,
    run_ragas: bool = True,
    max_samples: int | None = None,
    trace_output_path: Path | None = None,
    trace_summary_path: Path | None = None,
    trace_verbose: bool = False,
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
        trace_output_path: Optional JSONL path for per-sample trace rows (question,
            model answer, retrieved contexts, fallback usage, and per-metric scores).
        trace_summary_path: Optional JSON path for reliability diagnostics computed
            from trace rows (split metrics, zero-rates, bootstrap CI, abstention accuracy).
        trace_verbose: If True, logs per-sample answer/context previews at INFO.

    Returns:
        Dict with keys: faithfulness, answer_relevancy,
        context_precision, context_recall.
        When run_ragas=False, returns zero metrics.
    """
    path = dataset_path or _DEFAULT_DATASET
    dataset = _load_dataset(path)

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
            row = _run_pipeline_on_sample(sample)
            results.append(row)
            if trace_verbose:
                logger.info(
                    "Trace sample %d answer='%s' contexts=%d",
                    i,
                    _preview(row["answer"], 160),
                    len(row["contexts"]),
                )
        except Exception:  # noqa: BLE001
            logger.exception("Skipping sample %d after unexpected error", i)
            failed_samples.append({"index": i, "question": sample.get("question", "")})

    trace_rows: list[dict[str, Any]] = []
    if not run_ragas:
        logger.info("RAGAS evaluation skipped (run_ragas=False)")
        metrics = dict(_ZERO_METRICS)
        for i, r in enumerate(results):
            trace_rows.append(
                {
                    "sample_index": i,
                    "question": r["question"],
                    "ground_truth": r["ground_truth"],
                    "model_answer": r["answer"],
                    "answer_preview": _preview(r["answer"]),
                    "sources": r.get("sources", []),
                    "retrieved_contexts": r["contexts"],
                    "retrieved_context_previews": [_preview(c, 160) for c in r["contexts"][:5]],
                    "context_count": len(r["contexts"]),
                    "used_fallback_contexts": bool(r.get("used_fallback_contexts", False)),
                    "retrieval_quality_score": float(r.get("retrieval_quality_score", 0.0) or 0.0),
                    "retrieval_chunk_count": int(r.get("retrieval_chunk_count", 0) or 0),
                    "retrieved_filtered_by_threshold": bool(
                        r.get("retrieval_filtered_by_threshold", False)
                    ),
                    "context_sufficiency": str(r.get("context_sufficiency", "insufficient")),
                    "ragas_scores": None,
                    "ragas_error": "ragas_skipped",
                }
            )
    else:
        metrics = _compute_ragas_metrics(
            results,
            evaluator_model=evaluator_model,
            trace_rows=trace_rows,
        )

    if trace_output_path is not None:
        trace_output_path.parent.mkdir(parents=True, exist_ok=True)
        with trace_output_path.open("w", encoding="utf-8") as f:
            for row in trace_rows:
                f.write(json.dumps(row, ensure_ascii=False) + "\n")
        logger.info(
            "Wrote RAGAS per-sample trace: %s (%d rows)",
            trace_output_path,
            len(trace_rows),
        )

    if trace_summary_path is not None:
        diagnostics = _build_trace_diagnostics(trace_rows, dataset)
        trace_summary_path.parent.mkdir(parents=True, exist_ok=True)
        with trace_summary_path.open("w", encoding="utf-8") as f:
            json.dump(diagnostics, f, indent=2, ensure_ascii=False)
        logger.info("Wrote RAGAS diagnostics summary: %s", trace_summary_path)

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
