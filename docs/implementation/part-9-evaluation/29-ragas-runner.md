# Part 9 — `src/evaluation/ragas_runner.py`

## Status Update (Current Implementation)

RAGAS context metrics now consume `retrieved_contexts` (full reranked chunk text) returned by `run_query()`, not `sources` node IDs.

Current fallback behavior:

1. If `retrieved_contexts` is empty for a sample, fallback to `ground_truth_contexts`
2. Fallback is explicitly logged to make evaluation degradation visible

This change is critical for meaningful `context_precision` and `context_recall`.

## 1. Purpose & Context

**Epic:** EP-16 RAGAS Evaluation Pipeline  
**US-16-02** — RAGAS Metrics Computation

`ragas_runner` automates end-to-end evaluation of the Query Graph against a gold-standard dataset. For each sample it:

1. Invokes the Query Graph to produce `(answer, retrieved_contexts)`.
2. Packages data in the RAGAS `Dataset` format.
3. Computes four RAGAS metrics: `faithfulness`, `context_precision`, `context_recall`, `answer_relevancy`.
4. Collects custom metrics (`cypher_healing_rate`, `hitl_confidence_agreement`) from state logs.
5. Produces an `EvaluationReport` and saves it to `evaluation_reports/`.

**Target thresholds (from SPECS.md):**

| Metric | Target |
|---|---|
| `context_precision` | ≥ 0.85 |
| `context_recall` | ≥ 0.90 |
| `faithfulness` | ≥ 0.95 |
| `cypher_healing_rate` | ≥ 0.80 |
| `hitl_confidence_agreement` | ≥ 0.90 |

---

## 2. Prerequisites

- `src/models/schemas.py` — `EvaluationReport` (step 5)
- `src/generation/query_graph.py` — `build_query_graph` (step 28)
- `ragas` package — `evaluate`, `Dataset`, plus individual metrics
- `src/config/logging.py` — `get_logger`
- `tests/fixtures/gold_standard.json` — labelled evaluation samples

---

## 3. Public API

| Symbol | Signature | Description |
|---|---|---|
| `load_dataset` | `(path: str) -> list[dict]` | Load gold-standard JSON |
| `run_evaluation` | `(dataset, query_graph, custom_metrics) -> EvaluationReport` | Full evaluation pipeline |
| `save_report` | `(report: EvaluationReport, output_dir: str) -> Path` | JSON serialisation |

---

## 4. Full Implementation

```python
"""RAGAS evaluation pipeline — EP-16.

Runs the Query Graph against a gold-standard dataset and computes
RAGAS metrics + custom KPIs defined in custom_metrics.py.

CLI usage::

    python -m src.evaluation.ragas_runner \
        --dataset tests/fixtures/gold_standard.json \
        --output evaluation_reports/
"""

from __future__ import annotations

import json
import logging
from datetime import datetime, timezone
from pathlib import Path

from src.config.logging import get_logger
from src.models.schemas import EvaluationReport

logger: logging.Logger = get_logger(__name__)

# Target thresholds for pass/fail classification
THRESHOLDS: dict[str, float] = {
    "faithfulness": 0.95,
    "context_precision": 0.85,
    "context_recall": 0.90,
    "answer_relevancy": 0.75,
    "cypher_healing_rate": 0.80,
    "hitl_confidence_agreement": 0.90,
}


# ── Dataset Loading ────────────────────────────────────────────────────────────

def load_dataset(path: str) -> list[dict]:
    """Load the gold-standard evaluation dataset from a JSON file.

    Each item must have: ``question``, ``ground_truth``,
    ``ground_truth_context`` (list of strings).

    Args:
        path: Absolute or relative path to the JSON file.

    Returns:
        List of sample dicts.

    Raises:
        FileNotFoundError: If the file does not exist.
        ValueError: If the file is not valid JSON or missing required keys.
    """
    file_path = Path(path)
    if not file_path.exists():
        raise FileNotFoundError(f"Gold-standard dataset not found: {path}")

    with file_path.open("r", encoding="utf-8") as fp:
        data = json.load(fp)

    if not isinstance(data, list) or not data:
        raise ValueError(f"Expected a non-empty JSON array in {path}.")

    required_keys = {"question", "ground_truth", "ground_truth_context"}
    for i, sample in enumerate(data):
        missing = required_keys - set(sample.keys())
        if missing:
            raise ValueError(f"Sample {i} missing required keys: {missing}")

    logger.info("Loaded %d evaluation samples from '%s'.", len(data), path)
    return data


# ── Query Execution ────────────────────────────────────────────────────────────

def _run_query_graph(query_graph, question: str) -> tuple[str, list[str]]:
    """Run the compiled Query Graph for one question.

    Args:
        query_graph: Compiled LangGraph from ``build_query_graph()``.
        question:    The evaluation question.

    Returns:
        ``(answer, contexts)`` where contexts are the retrieved chunk texts.
    """
    config = {"configurable": {"thread_id": f"eval-{abs(hash(question))}"}}
    initial = {
        "user_query": question,
        "iteration_count": 0,
        "retrieved_chunks": [],
        "reranked_chunks": [],
        "current_answer": "",
        "last_critique": None,
        "grader_decision": None,
        "final_answer": "",
        "sources": [],
    }
    try:
        result = query_graph.invoke(initial, config=config)
        answer: str = result.get("final_answer") or result.get("current_answer") or ""
        chunks = result.get("reranked_chunks") or []
        contexts: list[str] = [c.text for c in chunks]
        return answer, contexts
    except Exception as exc:
        logger.error("Query graph failed for question '%s': %s", question[:60], exc)
        return "", []


# ── RAGAS Evaluation ──────────────────────────────────────────────────────────

def run_evaluation(
    dataset: list[dict],
    query_graph,
    custom_metrics: dict[str, float] | None = None,
) -> EvaluationReport:
    """Execute the full RAGAS evaluation pipeline.

    Args:
        dataset:        Gold-standard samples (from ``load_dataset``).
        query_graph:    Compiled Query Graph from ``build_query_graph()``.
        custom_metrics: Pre-computed dict with keys ``cypher_healing_rate``
                        and ``hitl_confidence_agreement`` (from builder logs).
                        Defaults to 0.0 if not provided.

    Returns:
        ``EvaluationReport`` with all RAGAS + custom metric values.
    """
    try:
        from datasets import Dataset as HFDataset
        from ragas import evaluate
        from ragas.metrics import (
            answer_relevancy,
            context_precision,
            context_recall,
            faithfulness,
        )
    except ImportError as exc:
        raise ImportError(
            "ragas and datasets are required. Run: pip install ragas datasets"
        ) from exc

    logger.info("Running RAGAS evaluation on %d samples...", len(dataset))

    questions: list[str] = []
    answers: list[str] = []
    contexts: list[list[str]] = []
    ground_truths: list[str] = []
    failed_samples: list[dict] = []

    for i, sample in enumerate(dataset):
        question = sample["question"]
        ground_truth = sample["ground_truth"]
        logger.debug("Evaluating sample %d/%d: '%s'", i + 1, len(dataset), question[:60])

        answer, retrieved_contexts = _run_query_graph(query_graph, question)

        if not answer:
            logger.warning("Empty answer for sample %d — marking as failed.", i)
            failed_samples.append({"sample_index": i, "question": question, "error": "empty_answer"})
            answer = "N/A"
            retrieved_contexts = ["N/A"]

        questions.append(question)
        answers.append(answer)
        contexts.append(retrieved_contexts or ["N/A"])
        ground_truths.append(ground_truth)

    # Build HuggingFace Dataset for RAGAS
    ragas_dataset = HFDataset.from_dict({
        "question": questions,
        "answer": answers,
        "contexts": contexts,
        "ground_truth": ground_truths,
    })

    try:
        ragas_result = evaluate(
            ragas_dataset,
            metrics=[faithfulness, context_precision, context_recall, answer_relevancy],
        )
        metrics_dict = ragas_result.to_pandas().mean().to_dict()
    except Exception as exc:
        logger.error("RAGAS evaluation failed: %s — using zero scores.", exc)
        metrics_dict = {
            "faithfulness": 0.0,
            "context_precision": 0.0,
            "context_recall": 0.0,
            "answer_relevancy": 0.0,
        }

    custom = custom_metrics or {}
    report = EvaluationReport(
        timestamp=datetime.now(tz=timezone.utc),
        num_samples=len(dataset),
        faithfulness=float(metrics_dict.get("faithfulness", 0.0)),
        context_precision=float(metrics_dict.get("context_precision", 0.0)),
        context_recall=float(metrics_dict.get("context_recall", 0.0)),
        answer_relevancy=float(metrics_dict.get("answer_relevancy", 0.0)),
        cypher_healing_rate=float(custom.get("cypher_healing_rate", 0.0)),
        hitl_confidence_agreement=float(custom.get("hitl_confidence_agreement", 0.0)),
        failed_samples=failed_samples,
    )

    logger.info(
        "Evaluation complete: faithfulness=%.3f, context_precision=%.3f, "
        "context_recall=%.3f, answer_relevancy=%.3f",
        report.faithfulness, report.context_precision,
        report.context_recall, report.answer_relevancy,
    )
    return report


# ── Report Persistence ────────────────────────────────────────────────────────

def save_report(report: EvaluationReport, output_dir: str = "evaluation_reports") -> Path:
    """Serialise the EvaluationReport to a timestamped JSON file.

    Args:
        report:     The completed ``EvaluationReport``.
        output_dir: Directory path; created if absent.

    Returns:
        Path to the saved JSON file.
    """
    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)
    stamp = report.timestamp.strftime("%Y%m%d_%H%M%S")
    file_path = out / f"report_{stamp}.json"
    file_path.write_text(report.model_dump_json(indent=2), encoding="utf-8")
    logger.info("Report saved to '%s'.", file_path)
    return file_path


# ── CLI Entry Point ───────────────────────────────────────────────────────────

if __name__ == "__main__":
    import argparse
    from src.generation.query_graph import build_query_graph

    parser = argparse.ArgumentParser(description="Run RAGAS evaluation pipeline.")
    parser.add_argument("--dataset", required=True, help="Path to gold_standard.json")
    parser.add_argument("--output", default="evaluation_reports", help="Output directory")
    args = parser.parse_args()

    samples = load_dataset(args.dataset)
    qg = build_query_graph()
    result = run_evaluation(samples, qg)
    saved = save_report(result, args.output)
    print(f"Report saved: {saved}")
    print(result.model_dump_json(indent=2))
```

---

## 5. Tests

```python
"""Unit tests for src/evaluation/ragas_runner.py — UT-24"""

from __future__ import annotations

import json
import tempfile
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from src.evaluation.ragas_runner import load_dataset, save_report
from src.models.schemas import EvaluationReport
from datetime import datetime, timezone


# ── load_dataset ───────────────────────────────────────────────────────────────

class TestLoadDataset:
    def _write_samples(self, samples: list[dict]) -> str:
        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            json.dump(samples, f)
            return f.name

    def test_loads_valid_dataset(self) -> None:
        path = self._write_samples([
            {"question": "Q?", "ground_truth": "A.", "ground_truth_context": ["ctx"]},
        ])
        data = load_dataset(path)
        assert len(data) == 1
        assert data[0]["question"] == "Q?"

    def test_missing_file_raises(self) -> None:
        with pytest.raises(FileNotFoundError):
            load_dataset("/nonexistent/path/dataset.json")

    def test_missing_required_key_raises(self) -> None:
        path = self._write_samples([{"question": "Q?"}])
        with pytest.raises(ValueError, match="missing required keys"):
            load_dataset(path)

    def test_empty_array_raises(self) -> None:
        path = self._write_samples([])
        with pytest.raises(ValueError):
            load_dataset(path)


# ── save_report ────────────────────────────────────────────────────────────────

class TestSaveReport:
    def _make_report(self) -> EvaluationReport:
        return EvaluationReport(
            timestamp=datetime.now(tz=timezone.utc),
            num_samples=10,
            faithfulness=0.97,
            context_precision=0.88,
            context_recall=0.91,
            answer_relevancy=0.85,
            cypher_healing_rate=0.82,
            hitl_confidence_agreement=0.93,
            failed_samples=[],
        )

    def test_creates_output_directory(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            out_dir = str(Path(tmpdir) / "reports" / "nested")
            path = save_report(self._make_report(), output_dir=out_dir)
            assert path.exists()

    def test_json_is_valid(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            path = save_report(self._make_report(), output_dir=tmpdir)
            data = json.loads(path.read_text())
            assert "faithfulness" in data
            assert data["num_samples"] == 10

    def test_filename_contains_timestamp(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            path = save_report(self._make_report(), output_dir=tmpdir)
            assert "report_" in path.name
            assert path.suffix == ".json"
```

---

## 6. Smoke Test

```bash
python -c "
from src.evaluation.ragas_runner import load_dataset, save_report
from src.models.schemas import EvaluationReport
from datetime import datetime, timezone
import tempfile, json, pathlib

# Write a minimal dataset
samples = [{'question': 'Q?', 'ground_truth': 'A.', 'ground_truth_context': ['ctx']}]
with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
    json.dump(samples, f)
    path = f.name

data = load_dataset(path)
print('Loaded samples:', len(data))

report = EvaluationReport(
    timestamp=datetime.now(tz=timezone.utc),
    num_samples=1, faithfulness=0.97, context_precision=0.88,
    context_recall=0.91, answer_relevancy=0.85,
    cypher_healing_rate=0.82, hitl_confidence_agreement=0.93,
    failed_samples=[],
)
with tempfile.TemporaryDirectory() as tmpdir:
    saved = save_report(report, output_dir=tmpdir)
    print('Report saved:', saved.name)
print('ragas_runner smoke test passed.')
"
```
