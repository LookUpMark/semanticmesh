"""Evaluation Bundle Writer — produces evaluation_bundle.json for AI-as-Judge analysis.

The bundle is a self-contained JSON file containing all data an AI agent needs
to qualitatively evaluate a pipeline run without requiring RAGAS or any external
evaluation framework.
"""

from __future__ import annotations

import json
from datetime import UTC, datetime
from pathlib import Path  # noqa: TC003
from typing import Any


def write_evaluation_bundle(
    output_dir: Path,
    study_id: str,
    dataset_id: str,
    dataset_info: dict[str, Any],
    config: dict[str, Any],
    builder_info: dict[str, Any],
    query_summary: dict[str, Any],
    per_question: list[dict[str, Any]],
    ragas_metrics: dict[str, Any] | None = None,
) -> Path:
    """Write a structured evaluation_bundle.json for AI-as-Judge analysis.

    Args:
        output_dir: Directory to write the bundle file.
        study_id: Experiment identifier (e.g. "AB-00").
        dataset_id: Dataset identifier (e.g. "01_basics_ecommerce").
        dataset_info: Raw dataset JSON (contains domain, complexity, pairs).
        config: Pipeline configuration snapshot.
        builder_info: Builder stage results dict.
        query_summary: Query stage aggregate metrics dict.
        per_question: Per-question detailed results.
        ragas_metrics: Optional RAGAS metrics (empty dict if not run).

    Returns:
        Path to the written evaluation_bundle.json file.
    """
    bundle = _build_bundle(
        study_id=study_id,
        dataset_id=dataset_id,
        dataset_info=dataset_info,
        config=config,
        builder_info=builder_info,
        query_summary=query_summary,
        per_question=per_question,
        ragas_metrics=ragas_metrics or {},
    )

    output_dir.mkdir(parents=True, exist_ok=True)
    bundle_path = output_dir / "evaluation_bundle.json"
    bundle_path.write_text(
        json.dumps(bundle, indent=2, ensure_ascii=False, default=str),
        encoding="utf-8",
    )
    return bundle_path


def _build_bundle(
    study_id: str,
    dataset_id: str,
    dataset_info: dict[str, Any],
    config: dict[str, Any],
    builder_info: dict[str, Any],
    query_summary: dict[str, Any],
    per_question: list[dict[str, Any]],
    ragas_metrics: dict[str, Any],
) -> dict[str, Any]:
    """Assemble the complete evaluation bundle dict."""

    # ── Meta ──────────────────────────────────────────────────────────────
    meta = {
        "study_id": study_id,
        "dataset_id": dataset_id,
        "timestamp": datetime.now(tz=UTC).isoformat(),
        "bundle_version": "1.0",
    }

    # ── Dataset Info ──────────────────────────────────────────────────────
    pairs = (
        dataset_info.get("pairs")
        or dataset_info.get("qa_pairs")
        or dataset_info.get("questions")
        or []
    )
    query_types: dict[str, int] = {}
    difficulties: dict[str, int] = {}
    for p in pairs:
        qt = p.get("query_type", "unknown")
        query_types[qt] = query_types.get(qt, 0) + 1
        diff = p.get("difficulty", "unknown")
        difficulties[diff] = difficulties.get(diff, 0) + 1

    ds_info = {
        "dataset_id": dataset_id,
        "dataset_name": dataset_info.get("dataset_name", ""),
        "domain": dataset_info.get("domain", ""),
        "complexity": dataset_info.get("complexity", ""),
        "total_pairs": len(pairs),
        "query_type_distribution": query_types,
        "difficulty_distribution": difficulties,
    }

    # ── Builder Report ────────────────────────────────────────────────────
    builder_report = {
        "triplets_extracted": builder_info.get("triplets_extracted", 0),
        "entities_resolved": builder_info.get("entities_resolved", 0),
        "tables_parsed": builder_info.get("tables_parsed", 0),
        "tables_completed": builder_info.get("tables_completed", 0),
        "cypher_failed": builder_info.get("cypher_failed", False),
        "failed_mappings": builder_info.get("failed_mappings", []),
        "ingestion_errors": builder_info.get("ingestion_errors", []),
        "parent_chunks": builder_info.get("parent_chunks", 0),
        "child_chunks": builder_info.get("child_chunks", 0),
        "elapsed_s": builder_info.get("elapsed_s", 0),
        "all_tables_completed": (
            builder_info.get("tables_completed", 0) == builder_info.get("tables_parsed", 0)
            and builder_info.get("tables_parsed", 0) > 0
        ),
        "builder_skipped": not bool(builder_info),
    }

    # ── Query Report ──────────────────────────────────────────────────────
    query_report = {
        "total_questions": query_summary.get("total_questions", 0),
        "grounded_count": query_summary.get("grounded_count", 0),
        "grounded_rate": query_summary.get("grounded_rate", 0.0),
        "abstained_count": query_summary.get("abstained_count", 0),
        "avg_gt_coverage": query_summary.get("avg_gt_coverage", 0.0),
        "avg_top_score": query_summary.get("avg_top_score", 0.0),
        "avg_chunk_count": query_summary.get("avg_chunk_count", 0.0),
        "elapsed_s": query_summary.get("elapsed_s", 0),
    }

    # ── Per-Question Detail ───────────────────────────────────────────────
    # Already structured by the caller; include as-is
    pq_detail = per_question

    # ── Pipeline Health Indicators ────────────────────────────────────────
    total_grader_rejections = sum(pq.get("grader_rejection_count", 0) for pq in per_question)
    grader_inconsistencies = sum(
        1 for pq in per_question if not pq.get("grader_consistency_valid", True)
    )
    gate_abstentions = sum(1 for pq in per_question if pq.get("gate_decision") == "abstain_early")
    low_retrieval = sum(1 for pq in per_question if pq.get("retrieval_quality_score", 1.0) < 0.2)

    pipeline_health = {
        "total_grader_rejections": total_grader_rejections,
        "grader_inconsistencies": grader_inconsistencies,
        "gate_abstentions": gate_abstentions,
        "questions_with_low_retrieval_score": low_retrieval,
        "cypher_failed": builder_report["cypher_failed"],
        "failed_mappings_count": len(builder_report["failed_mappings"]),
        "ingestion_errors_count": len(builder_report["ingestion_errors"]),
    }

    # ── RAGAS (optional) ─────────────────────────────────────────────────
    ragas_section: dict[str, Any] | None = None
    if ragas_metrics:
        ragas_section = {
            "enabled": True,
            "metrics": ragas_metrics,
        }

    # ── Assemble ──────────────────────────────────────────────────────────
    return {
        "meta": meta,
        "config": config,
        "dataset_info": ds_info,
        "builder_report": builder_report,
        "query_report": query_report,
        "per_question": pq_detail,
        "pipeline_health": pipeline_health,
        "ragas": ragas_section,
    }
