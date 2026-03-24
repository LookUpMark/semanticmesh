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
from datetime import datetime, timezone
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
# Ablation matrix — all 21 experiments (AB-00 … AB-20)
#
# run_ragas: Whether to run RAGAS evaluation for this study.
#   RAGAS is enabled for studies that directly impact the 4 core metrics.
#   Other studies use pipeline metrics only to reduce cost.
# ─────────────────────────────────────────────────────────────────────────────

ABLATION_MATRIX: dict[str, dict[str, Any]] = {
    # AB-00: Baseline with default settings
    "AB-00": {
        "description": "Baseline — default settings (hybrid retrieval, reranker ON, chunking 256/32)",
        "env_overrides": {},
        "primary_metric": "faithfulness",
        "run_ragas": True,
    },
    # AB-01, AB-02: Retrieval mode variations (impact all RAGAS metrics)
    "AB-01": {
        "description": "Vector-only retrieval — no BM25, no graph traversal",
        "env_overrides": {"RETRIEVAL_MODE": "vector"},
        "primary_metric": "context_precision",
        "run_ragas": True,
    },
    "AB-02": {
        "description": "BM25-only retrieval — no vector, no graph traversal",
        "env_overrides": {"RETRIEVAL_MODE": "bm25"},
        "primary_metric": "context_precision",
        "run_ragas": True,
    },
    # AB-03, AB-04, AB-05: Reranker variations
    "AB-03": {
        "description": "Reranker OFF — raw hybrid pool ranking",
        "env_overrides": {"ENABLE_RERANKER": "false"},
        "primary_metric": "context_precision",
        "run_ragas": True,
    },
    "AB-04": {
        "description": "Reranker top_k=5 — smaller reranking pool",
        "env_overrides": {"RERANKER_TOP_K": "5"},
        "primary_metric": "context_precision",
        "run_ragas": False,  # Minor variation, not worth RAGAS cost
    },
    "AB-05": {
        "description": "Reranker top_k=20 — larger reranking pool",
        "env_overrides": {"RERANKER_TOP_K": "20"},
        "primary_metric": "context_precision",
        "run_ragas": False,  # Minor variation, not worth RAGAS cost
    },
    # AB-06, AB-07, AB-08: Chunking strategies (impact context recall)
    "AB-06": {
        "description": "Chunking 128/16 — smaller chunks, more overlap",
        "env_overrides": {"CHUNK_SIZE": "128", "CHUNK_OVERLAP": "16"},
        "primary_metric": "context_recall",
        "run_ragas": True,
    },
    "AB-07": {
        "description": "Chunking 384/48 — larger chunks, more overlap",
        "env_overrides": {"CHUNK_SIZE": "384", "CHUNK_OVERLAP": "48"},
        "primary_metric": "context_recall",
        "run_ragas": True,
    },
    "AB-08": {
        "description": "Chunking 512/64 — largest chunks, more overlap",
        "env_overrides": {"CHUNK_SIZE": "512", "CHUNK_OVERLAP": "64"},
        "primary_metric": "context_recall",
        "run_ragas": True,
    },
    # AB-09, AB-10: Extraction max tokens variations
    "AB-09": {
        "description": "Extraction max tokens=4096 — conservative limit",
        "env_overrides": {"LLM_MAX_TOKENS_EXTRACTION": "4096"},
        "primary_metric": "faithfulness",
        "run_ragas": False,  # Performance tuning, not semantic impact
    },
    "AB-10": {
        "description": "Extraction max tokens=16384 — generous limit",
        "env_overrides": {"LLM_MAX_TOKENS_EXTRACTION": "16384"},
        "primary_metric": "faithfulness",
        "run_ragas": False,  # Performance tuning, not semantic impact
    },
    # AB-11, AB-12: Entity resolution threshold variations
    "AB-11": {
        "description": "ER similarity threshold=0.65 — more aggressive merging",
        "env_overrides": {"ER_SIMILARITY_THRESHOLD": "0.65"},
        "primary_metric": "context_precision",
        "run_ragas": False,  # Tuning parameter, minor impact
    },
    "AB-12": {
        "description": "ER similarity threshold=0.85 — conservative merging",
        "env_overrides": {"ER_SIMILARITY_THRESHOLD": "0.85"},
        "primary_metric": "context_precision",
        "run_ragas": False,  # Tuning parameter, minor impact
    },
    # AB-13, AB-14: ER blocking top_k variations
    "AB-13": {
        "description": "ER blocking top_k=5 — smaller candidate set",
        "env_overrides": {"ER_BLOCKING_TOP_K": "5"},
        "primary_metric": "context_precision",
        "run_ragas": False,  # Performance tuning, minor impact
    },
    "AB-14": {
        "description": "ER blocking top_k=20 — larger candidate set",
        "env_overrides": {"ER_BLOCKING_TOP_K": "20"},
        "primary_metric": "context_precision",
        "run_ragas": False,  # Performance tuning, minor impact
    },
    # AB-15, AB-16: Schema enrichment and critic validation (impact context precision/faithfulness)
    "AB-15": {
        "description": "Schema enrichment OFF — no LLM acronym expansion",
        "env_overrides": {"ENABLE_SCHEMA_ENRICHMENT": "false"},
        "primary_metric": "context_precision",
        "run_ragas": True,
    },
    "AB-16": {
        "description": "Actor-Critic validation OFF — accept all mapping proposals",
        "env_overrides": {"ENABLE_CRITIC_VALIDATION": "false"},
        "primary_metric": "context_precision",
        "run_ragas": True,
    },
    # AB-17, AB-18: Confidence threshold variations
    "AB-17": {
        "description": "Confidence threshold=0.70 — more HITL interrupts",
        "env_overrides": {"CONFIDENCE_THRESHOLD": "0.70"},
        "primary_metric": "faithfulness",
        "run_ragas": False,  # Tuning parameter, minor impact
    },
    "AB-18": {
        "description": "Confidence threshold=0.85 — fewer HITL interrupts",
        "env_overrides": {"CONFIDENCE_THRESHOLD": "0.85"},
        "primary_metric": "faithfulness",
        "run_ragas": False,  # Tuning parameter, minor impact
    },
    # AB-19, AB-20: Healing and grader variations
    "AB-19": {
        "description": "Cypher healing OFF — immediate fail on syntax error",
        "env_overrides": {"ENABLE_CYPHER_HEALING": "false"},
        "primary_metric": "faithfulness",
        "run_ragas": True,
    },
    "AB-20": {
        "description": "Hallucination grader OFF — return first answer",
        "env_overrides": {"ENABLE_HALLUCINATION_GRADER": "false"},
        "primary_metric": "faithfulness",
        "run_ragas": False,  # Disables the component being measured
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
    saved: dict[str, str | None] = {k: os.environ.get(k) for k in env_overrides}
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
    run_ragas: bool | None = None,
    doc_paths: list[Path] | None = None,
    ddl_paths: list[Path] | None = None,
    debug_trace: bool = False,
) -> dict[str, float]:
    """Run a single ablation experiment and return the measured metrics.

    The experiment consists of:
    1. Clear the Neo4j graph
    2. Run the Builder Graph (triplet extraction, ER, mapping, Cypher upsert)
    3. Run RAGAS evaluation on the gold-standard QA dataset

    Args:
        experiment_id: One of AB-00 … AB-20.
        dataset_path:  Path to the gold-standard QA JSON file.
            Defaults to tests/fixtures/gold_standard.json.
        run_ragas:    Whether to run RAGAS evaluation. If None, uses the value
            from ABLATION_MATRIX[experiment_id]["run_ragas"].
        doc_paths:    Paths to PDF/chunk documents. If None, uses default fixtures.
        ddl_paths:    Paths to DDL files. If None, uses default fixtures.
        debug_trace:  If True, enable detailed debug tracing of the pipeline.

    Returns:
        Dict of metric name → float, as returned by run_ragas_evaluation.
        When run_ragas=False, returns a dict with pipeline metrics only.

    Raises:
        ValueError: if experiment_id is not in ABLATION_MATRIX.
    """
    if experiment_id not in ABLATION_MATRIX:
        known = ", ".join(sorted(ABLATION_MATRIX))
        raise ValueError(f"Unknown experiment '{experiment_id}'. Known: {known}")

    config = ABLATION_MATRIX[experiment_id]
    description: str = config["description"]
    env_overrides: dict[str, str] = config["env_overrides"]

    # Use provided run_ragas or default to matrix value
    should_run_ragas = run_ragas if run_ragas is not None else config.get("run_ragas", False)

    logger.info("Starting ablation %s: %s", experiment_id, description)
    logger.info("Env overrides: %s", env_overrides)
    logger.info("RAGAS enabled: %s", should_run_ragas)

    with _settings_override(env_overrides):
        # Import here to avoid issues with cached settings
        from src.graph.builder_graph import run_builder

        # Use default fixtures if not provided
        if doc_paths is None:
            root = Path(__file__).parent.parent.parent
            fixture_dir = root / "tests" / "fixtures"
            doc_paths = [
                fixture_dir / "00_legacy" / "sample_docs" / "business_glossary.txt",
                fixture_dir / "00_legacy" / "sample_docs" / "data_dictionary.txt",
            ]
        if ddl_paths is None:
            root = Path(__file__).parent.parent.parent
            fixture_dir = root / "tests" / "fixtures"
            ddl_paths = [fixture_dir / "00_legacy" / "sample_ddl" / "complex_schema.sql"]

        # Run the builder graph
        logger.info("Running builder graph...")
        builder_state = run_builder(
            raw_documents=doc_paths,
            ddl_paths=ddl_paths,
            production=False,
            clear_graph=True,
            trace_enabled=debug_trace,
            study_id=experiment_id,
        )

        # Log builder results
        logger.info(
            "Builder complete: %d triplets, %d entities, %d tables",
            len(builder_state.get("triplets", [])),
            len(builder_state.get("entities", [])),
            len(builder_state.get("tables", [])),
        )

        # Run RAGAS evaluation
        metrics = run_ragas_evaluation(dataset_path, run_ragas=should_run_ragas)

        # Add builder metrics to results
        metrics["triplets"] = len(builder_state.get("triplets", []))
        metrics["entities"] = len(builder_state.get("entities", []))
        metrics["tables_parsed"] = len(builder_state.get("tables", []))
        metrics["tables_completed"] = len(builder_state.get("completed_tables", []))
        metrics["cypher_failed"] = builder_state.get("cypher_failed", False)

        # Generate comparison report if debug tracing is enabled
        if debug_trace:
            from src.config.tracing import ComparisonReport
            from src.config.settings import get_settings

            settings = get_settings()
            trace_dir = Path(settings.trace_output_dir) / experiment_id

            # Load query traces if they exist
            query_trace_file = trace_dir / f"query_traces_{experiment_id}.jsonl"
            query_traces = []
            if query_trace_file.exists():
                from src.config.tracing import load_query_traces

                query_traces = load_query_traces(query_trace_file)

            # Load ground truth dataset
            gt_path = dataset_path or Path("tests/fixtures/gold_standard.json")
            ground_truth = []
            if gt_path.exists():
                import json

                with open(gt_path) as f:
                    gt_data = json.load(f)
                    # Handle both formats: dict with "pairs" field or simple list
                    if isinstance(gt_data, dict):
                        ground_truth = gt_data.get("pairs", [])
                    elif isinstance(gt_data, list):
                        ground_truth = gt_data

            # Generate comparison report
            if query_traces and ground_truth:
                report = ComparisonReport(
                    study_id=experiment_id,
                    timestamp=datetime.now(timezone.utc).isoformat(),
                    dataset_path=str(gt_path),
                )
                report.generate_per_question_analysis(query_traces, ground_truth)
                report.generate_aggregate_metrics()
                report.identify_bottlenecks()
                report.generate_recommendations()

                report_path = trace_dir / f"comparison_report_{experiment_id}.md"
                report.save(trace_dir)
                logger.info(f"Comparison report saved to {report_path}")

    logger.info("Ablation %s complete: %s", experiment_id, metrics)
    return metrics
