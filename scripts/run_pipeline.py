#!/usr/bin/env python3
"""Unified pipeline runner for ablation studies and evaluation.

Replaces run_ab00.py and run_ablation_full.py. Supports:
  - Single study, multiple studies, all studies, or AB-BEST mode
  - Single dataset, multiple datasets, or all datasets
  - Optional RAGAS evaluation, lazy extraction, smoke fixtures
  - Auto-start Neo4j via --auto-neo4j

Usage:
    python -m scripts.run_pipeline --best --dataset tests/fixtures/01_basics_ecommerce/gold_standard.json
    python -m scripts.run_pipeline --study AB-05 --all-datasets --ragas
    python -m scripts.run_pipeline --all-studies --max-samples 5 --smoke
    python -m scripts.run_pipeline --studies AB-01 AB-02 AB-03 --auto-neo4j
"""

from __future__ import annotations

import argparse
import json
import logging
import os
import re as _re
import sys
import time as _time
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from dotenv import load_dotenv  # type: ignore[import]

load_dotenv(ROOT / ".env")

# ── Constants ────────────────────────────────────────────────────────────────────

DATASETS = [
    "01_basics_ecommerce",
    "02_intermediate_finance",
    "03_advanced_healthcare",
    "04_complex_manufacturing",
    "05_edgecases_incomplete",
    "06_edgecases_legacy",
]

STUDY_IDS = [f"AB-{i:02d}" for i in range(21)]

FIXTURE_DIR = ROOT / "tests" / "fixtures"

# ── Helpers ──────────────────────────────────────────────────────────────────────


def _find_doc_files(fixture_dir: Path) -> list[str]:
    """Auto-detect business documentation files (.txt or .md)."""
    known_stems = ("business_glossary", "data_dictionary", "complex_scenarios")
    doc_files: list[str] = []
    for stem in known_stems:
        for ext in (".txt", ".md"):
            candidate = fixture_dir / f"{stem}{ext}"
            if candidate.exists():
                doc_files.append(str(candidate))
                break
    if not doc_files:
        skip = {"readme", "dataset_summary", "schema"}
        for f in sorted(fixture_dir.glob("*")):
            if f.suffix.lower() in (".txt", ".md") and f.stem.lower() not in skip:
                doc_files.append(str(f))
    return doc_files


def _ensure_neo4j() -> None:
    """Auto-start Neo4j Docker container if not already running."""
    from scripts.neo4j_lifecycle import start_neo4j  # noqa: PLC0415

    start_neo4j(register_stop_atexit=True)


def _discover_datasets() -> list[Path]:
    """Find all gold_standard.json under tests/fixtures/."""
    return sorted(FIXTURE_DIR.glob("*/gold_standard.json"))


def _select_fixtures(
    dataset_path: Path | None,
    smoke: bool,
) -> tuple[list[str], list[str]]:
    """Return (doc_paths, ddl_paths) for the given dataset or smoke defaults."""
    if smoke:
        d = FIXTURE_DIR / "01_basics_ecommerce"
        return (
            [str(d / "business_glossary.txt"), str(d / "data_dictionary.txt")],
            [str(d / "schema.sql")],
        )

    if dataset_path is not None:
        ds_dir = dataset_path.parent
        docs, ddls = [], []
        for name in ("business_glossary.txt", "business_glossary.md"):
            p = ds_dir / name
            if p.exists():
                docs.append(str(p))
                break
        for name in ("data_dictionary.txt", "data_dictionary.md"):
            p = ds_dir / name
            if p.exists():
                docs.append(str(p))
                break
        ddl = ds_dir / "schema.sql"
        if ddl.exists():
            ddls.append(str(ddl))
        if docs and ddls:
            return docs, ddls

    # Fallback to 01_basics_ecommerce
    d = FIXTURE_DIR / "01_basics_ecommerce"
    return (
        [str(d / "business_glossary.txt"), str(d / "data_dictionary.txt")],
        [str(d / "schema.sql")],
    )


def _generate_analysis_md(summary: dict, dataset_id: str) -> str:
    """Generate a detailed per-dataset analysis markdown."""
    ts = summary.get("timestamp", "")[:19].replace("T", " ")
    cfg = summary.get("config", {})
    bld = summary.get("builder", {})
    qry = summary.get("query", {})
    ragas = summary.get("ragas", {})
    pq = summary.get("per_question", [])

    lines: list[str] = [
        f"# {summary.get('study_id', 'AB-00')} \u2014 {dataset_id} \u2014 Run Analysis",
        "",
        f"**Timestamp:** {ts}  ",
        f"**Run tag:** `{summary.get('run_tag', '')}`",
        "",
        "## Configuration",
        "",
        "| Parameter | Value |",
        "|-----------|-------|",
        f"| Extraction model | `{cfg.get('extraction_mode', '-')}` |",
        f"| Reasoning model | `{cfg.get('reasoning_model', '-')}` |",
        f"| Embedding model | `{cfg.get('embedding_model', '-')}` |",
        f"| Retrieval mode | `{cfg.get('retrieval_mode', '-')}` |",
        f"| Reranker | `{cfg.get('enable_reranker', '-')}` |",
        f"| Reranker top_k | `{cfg.get('reranker_top_k', '-')}` |",
        f"| Chunk size / overlap | `{cfg.get('chunk_size', '-')} / {cfg.get('chunk_overlap', '-')}` |",
        f"| ER similarity threshold | `{cfg.get('er_similarity_threshold', '-')}` |",
        "",
    ]

    if bld.get("triplets", 0) > 0:
        lines += [
            "## Builder Results",
            "",
            "| Metric | Value |",
            "|--------|-------|",
            f"| Triplets extracted | {bld.get('triplets', 0)} |",
            f"| Entities resolved | {bld.get('entities', 0)} |",
            f"| Tables parsed | {bld.get('tables_parsed', 0)} |",
            f"| Tables completed | {bld.get('tables_completed', 0)} |",
            "",
        ]
    else:
        lines += ["## Builder Results\n\nBuilder skipped (`--no-builder`).\n"]

    total = qry.get("total_questions", 0)
    grounded = qry.get("grounded_count", 0)
    rate = qry.get("grounded_rate", 0)
    lines += [
        "## Query Evaluation Summary",
        "",
        "| Metric | Value |",
        "|--------|-------|",
        f"| Questions | {total} |",
        f"| Grounded | **{grounded}/{total} ({rate:.0%})** |",
        (
            "| Avg GT Coverage | "
            + (f"{qry['avg_gt_coverage']:.0%}" if qry.get("avg_gt_coverage") is not None else "N/A")
            + " |"
        ),
        f"| Avg Top Score | {qry.get('avg_top_score', 0):.4f} |",
        f"| Avg Chunk Count | {qry.get('avg_chunk_count', 0):.1f} |",
        f"| Abstained | {qry.get('abstained_count', 0)} |",
        "",
    ]

    if ragas and "error" not in ragas:
        lines += [
            "## RAGAS Metrics",
            "",
            "| Metric | Value | Interpretation |",
            "|--------|-------|----------------|",
            f"| Faithfulness | **{ragas.get('faithfulness', 0):.4f}** | Answers grounded in context |",
            f"| Answer Relevancy | **{ragas.get('answer_relevancy', 0):.4f}** | Answers relevant to question |",
            f"| Context Precision | **{ragas.get('context_precision', 0):.4f}** | Retrieved chunks are on-topic |",
            f"| Context Recall | **{ragas.get('context_recall', 0):.4f}** | All needed context retrieved |",
            "",
        ]
    elif ragas and "error" in ragas:
        lines += [f"## RAGAS Metrics\n\n> \u26a0\ufe0f RAGAS failed: `{ragas['error']}`\n"]
    else:
        lines += ["## RAGAS Metrics\n\nRAGAS evaluation not enabled for this run.\n"]

    lines += ["## Per-Question Deep Dive", ""]
    anomalies: list[str] = []

    for r in pq:
        qid = r.get("query_id", "?")
        question = r.get("question", "")
        answer = r.get("answer", "")
        expected = r.get("expected_answer", "")
        grounded_flag = r.get("grounded", False)
        gt_cov = r.get("gt_coverage", 0)
        top_score = r.get("top_score", 0)
        gate = r.get("gate_decision", "proceed")
        sources = r.get("sources", [])
        contexts = r.get("contexts", [])
        rscores = r.get("ragas_scores") or {}

        if gate == "abstain_early":
            icon, status_label = "\u26d4", "ABSTAINED"
        elif not grounded_flag:
            icon, status_label = "\u274c", "UNGROUNDED"
        else:
            icon, status_label = "\u2705", "GROUNDED"

        lines += [
            f"### {icon} {qid} \u2014 {question}",
            "",
            f"**Status:** {status_label}  ",
            f"**GT Coverage:** {'N/A' if gt_cov is None else f'{gt_cov:.0%}'} | **Top Score:** {top_score:.4f} | **Gate:** `{gate}`",
            "",
            "**Expected answer:**",
            f"> {expected[:300]}{'…' if len(expected) > 300 else ''}",
            "",
            "**System answer:**",
            f"> {answer[:400]}{'…' if len(answer) > 400 else ''}",
            "",
        ]

        if rscores:
            ar = rscores.get("answer_relevancy", 0)
            lines += [
                "**RAGAS scores:**",
                "",
                "| f | ar | cp | cr |",
                "|---|----|----|-----|",
                f"| {rscores.get('faithfulness', 0):.2f} | {ar:.2f} | {rscores.get('context_precision', 0):.2f} | {rscores.get('context_recall', 0):.2f} |",
                "",
            ]

        if sources:
            lines += [
                f"**Sources retrieved ({len(sources)}):** "
                + ", ".join(f"`{s}`" for s in sources[:8]),
                "",
            ]

        if contexts:
            lines += ["**Context previews (first 3):**", ""]
            for j, ctx in enumerate(contexts[:3]):
                preview = ctx[:200].replace("\n", " ")
                lines += [f"{j + 1}. _{preview}\u2026_", ""]

        if not grounded_flag:
            anomalies.append(f"- **{qid}**: UNGROUNDED")
        if gate == "abstain_early":
            anomalies.append(f"- **{qid}**: ABSTAINED early")
        if rscores.get("faithfulness", 1.0) < 0.8:
            anomalies.append(f"- **{qid}**: Low faithfulness ({rscores['faithfulness']:.2f})")
        if rscores.get("context_precision", 1.0) < 0.2:
            anomalies.append(
                f"- **{qid}**: Very low context precision ({rscores.get('context_precision', 0):.2f})"
            )
        lines += ["---", ""]

    lines += ["## Anomalies & Observations", ""]
    if anomalies:
        lines += anomalies + [""]
    else:
        lines += ["No anomalies detected. All questions grounded with acceptable RAGAS scores.", ""]

    return "\n".join(lines)


# ── Core pipeline ───────────────────────────────────────────────────────────────


def _run_single(
    study_id: str,
    dataset_path: Path,
    *,
    skip_builder: bool,
    run_ragas: bool,
    ragas_model: str,
    max_samples: int | None,
    run_tag: str,
    smoke: bool,
    output_dir: Path,
) -> dict[str, Any]:
    """Execute the full pipeline for one study on one dataset."""
    from src.config.settings import get_settings  # noqa: PLC0415
    from src.evaluation.ablation_runner import ABLATION_MATRIX, _settings_override  # noqa: PLC0415
    from src.evaluation.bundle_writer import write_evaluation_bundle  # noqa: PLC0415
    from src.evaluation.gold_standard_loader import load_gold_standard  # noqa: PLC0415
    from src.generation.query_graph import run_query  # noqa: PLC0415
    from src.utils.text_utils import normalize_source_name as _ns  # noqa: PLC0415

    config = ABLATION_MATRIX.get(study_id, {})
    env_overrides = config.get("env_overrides", {})

    ds_metadata, pairs = load_gold_standard(dataset_path)
    if max_samples:
        pairs = pairs[:max_samples]

    dataset_id = dataset_path.parent.name
    out = output_dir / study_id / "datasets" / dataset_id
    out.mkdir(parents=True, exist_ok=True)

    # Set up file logging for this run
    log_file = out / "run.log"
    file_handler = logging.FileHandler(log_file, mode="w", encoding="utf-8")
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(logging.Formatter("%(asctime)s %(name)s %(levelname)s %(message)s"))

    root_logger = logging.getLogger()
    original_handlers = root_logger.handlers.copy()
    for h in root_logger.handlers[:]:
        root_logger.removeHandler(h)
    console = logging.StreamHandler(sys.stdout)
    console.setLevel(logging.INFO)
    console.setFormatter(file_handler.formatter)
    root_logger.addHandler(console)
    root_logger.addHandler(file_handler)

    logger = logging.getLogger("pipeline")
    result: dict[str, Any] = {}
    try:
        with _settings_override(env_overrides):
            settings = get_settings()
            extraction_mode = f"LLM ({settings.llm_model_extraction})"

            logger.info("=" * 60)
            logger.info("%s \u2014 %s", study_id, dataset_id)
            logger.info("=" * 60)
            logger.info("Extraction: %s", extraction_mode)
            logger.info("Embedding:  %s", settings.embedding_model)
            logger.info("Reasoning:  %s", settings.llm_model_reasoning)
            logger.info(
                "Reranker:   %s (top_k=%d)",
                settings.reranker_model if settings.enable_reranker else "OFF",
                settings.reranker_top_k,
            )
            logger.info("Samples:    %d", len(pairs))

            # ── Stage 1: Builder ──
            builder_state = None
            builder_elapsed = 0.0

            if not skip_builder:
                logger.info("[1/3] Builder Graph")
                docs, ddls = _select_fixtures(dataset_path, smoke)

                if not docs:
                    raise FileNotFoundError(f"No doc files found in {dataset_path.parent}")
                if not all(Path(d).exists() for d in ddls):
                    raise FileNotFoundError(f"DDL not found: {ddls}")

                from src.graph.builder_graph import run_builder as _run_builder  # noqa: PLC0415

                t0 = _time.perf_counter()
                builder_state = _run_builder(
                    raw_documents=docs,
                    ddl_paths=ddls,
                    production=False,
                    clear_graph=True,
                    trace_enabled=True,
                    study_id=study_id,
                )
                builder_elapsed = _time.perf_counter() - t0

                logger.info(
                    "  Triplets: %d  Entities: %d  Tables: %d/%d  Elapsed: %.1fs",
                    len(builder_state.get("triplets", [])),
                    len(builder_state.get("entities", [])),
                    len(builder_state.get("completed_tables", [])),
                    len(builder_state.get("tables", [])),
                    builder_elapsed,
                )
            else:
                logger.info("[1/3] Builder SKIPPED")

            # ── Stage 2: Query ──
            logger.info("[2/3] Query Evaluation (%d questions)", len(pairs))
            t1 = _time.perf_counter()
            grounded_count = 0
            per_question: list[dict[str, Any]] = []
            gt_coverages: list[float] = []
            top_scores: list[float] = []
            chunk_counts: list[int] = []

            for i, pair in enumerate(pairs):
                question = pair.get("question", "")
                r = run_query(
                    user_query=question,
                    trace_enabled=True,
                    query_index=i,
                    study_id=study_id,
                )
                answer = r.get("final_answer", "")
                sources = list(r.get("sources", []))
                entity_names = list(r.get("entity_names", []))
                gate = r.get("retrieval_gate_decision", "proceed")
                has_answer = bool(answer and answer.strip())
                grounded = bool(r.get("grader_grounded", True)) and has_answer
                if not grounded and has_answer:
                    grounded = not (
                        answer.strip().lower().startswith("i cannot")
                        or answer.strip().lower().startswith("i don't")
                    )
                if grounded and gate != "abstain_early":
                    grounded_count += 1

                expected_sources = pair.get("expected_sources", [])
                covered_sources: list[str] = []
                if expected_sources:
                    # Build token-level index from entity_names + sources.
                    # entity_names may use "ConceptName→TABLE_NAME" format — expand both sides
                    # then split each normalized part into individual tokens.
                    norm_retrieved_tokens: set[str] = set()
                    for s in (*entity_names, *sources):
                        if s:
                            for part in s.split("→"):
                                norm_retrieved_tokens.update(_ns(part.strip()).split())
                    # Always extract section headers from retrieved contexts
                    # (e.g. "## Interest\n\n..." → "interest") to cover glossary
                    # chunks that appear in context but aren't BC node names.
                    _header_re = _re.compile(r"^##?\s+(.+?)(?:\n|$)", _re.MULTILINE)
                    for chunk in r.get("retrieved_contexts", []):
                        for header in _header_re.findall(str(chunk)):
                            norm_retrieved_tokens.update(_ns(header.strip()).split())
                    # Partial token overlap: a source is covered if at least one of its
                    # tokens appears in (or is a stem-prefix of) the retrieved token index.
                    for es in expected_sources:
                        es_tokens = set(_ns(str(es)).split())
                        if es_tokens and (
                            es_tokens & norm_retrieved_tokens
                            or any(
                                rt.startswith(et) or et.startswith(rt)
                                for et in es_tokens
                                for rt in norm_retrieved_tokens
                                if len(et) >= 3 and len(rt) >= 3
                            )
                        ):
                            covered_sources.append(str(es))
                # None when no expected_sources — metric is not applicable (not inflated to 1.0)
                gt_coverage: float | None = (
                    len(covered_sources) / len(expected_sources) if expected_sources else None
                )

                gt_coverages.append(gt_coverage)
                top_scores.append(r.get("retrieval_quality_score", 0.0))
                chunk_counts.append(r.get("retrieval_chunk_count", 0))

                status = (
                    "\u2705" if grounded else ("\u26d4" if gate == "abstain_early" else "\u274c")
                )
                logger.info(
                    "  [%d/%d] %s Q: %s | gt=%s score=%.4f",
                    i + 1,
                    len(pairs),
                    status,
                    question[:80],
                    f"{gt_coverage:.0%}" if gt_coverage is not None else "N/A",
                    r.get("retrieval_quality_score", 0),
                )

                per_question.append(
                    {
                        "query_id": pair.get("query_id", f"Q{i + 1:03d}"),
                        "question": question,
                        "expected_answer": pair.get("expected_answer", ""),
                        "generated_answer": answer,
                        "expected_sources": expected_sources,
                        "covered_sources": covered_sources,
                        "gt_coverage": round(gt_coverage, 4) if gt_coverage is not None else None,
                        "sources": sources,
                        "entity_names": entity_names,
                        "retrieved_contexts": list(r.get("retrieved_contexts", [])),
                        "grounded": grounded,
                        "query_type": pair.get("query_type", "unknown"),
                        "difficulty": pair.get("difficulty", "unknown"),
                        "retrieval_quality_score": r.get("retrieval_quality_score", 0.0),
                        "retrieval_chunk_count": r.get("retrieval_chunk_count", 0),
                        "retrieval_gate_decision": gate,
                        "context_sufficiency": r.get("context_sufficiency", "insufficient"),
                        "grader_consistency_valid": r.get("grader_consistency_valid", True),
                        "grader_rejection_count": r.get("grader_rejection_count", 0),
                    }
                )

            query_elapsed = _time.perf_counter() - t1
            _valid_gt = [x for x in gt_coverages if x is not None]
            avg_gt: float | None = sum(_valid_gt) / len(_valid_gt) if _valid_gt else None
            avg_score = sum(top_scores) / len(top_scores) if top_scores else 0.0
            avg_chunks = sum(chunk_counts) / len(chunk_counts) if chunk_counts else 0.0
            abstained = sum(
                1 for pq in per_question if pq.get("retrieval_gate_decision") == "abstain_early"
            )

            _avg_gt_display = f"{avg_gt * 100:.0f}%" if avg_gt is not None else "N/A"
            logger.info(
                "  Query done: %.1fs | Grounded: %d/%d | GT cov: %s",
                query_elapsed,
                grounded_count,
                len(pairs),
                f"{avg_gt:.0%}" if avg_gt is not None else "N/A",
            )

            # ── Stage 3: RAGAS (optional) ──
            ragas_metrics = None
            if run_ragas:
                logger.info("[3/3] RAGAS Evaluation")
                try:
                    from src.evaluation.ragas_runner import _compute_ragas_metrics  # noqa: PLC0415

                    ragas_rows = [
                        {
                            "question": pq["question"],
                            "answer": pq["generated_answer"],
                            "contexts": pq["retrieved_contexts"],
                            "ground_truth": pq["expected_answer"],
                            "sources": pq["sources"],
                        }
                        for pq in per_question
                    ]
                    ragas_trace: list[dict] = []
                    ragas_metrics = _compute_ragas_metrics(
                        ragas_rows,
                        evaluator_model=ragas_model,
                        trace_rows=ragas_trace,
                    )
                    for tr in ragas_trace:
                        idx = tr.get("sample_index")
                        if idx is not None and idx < len(per_question):
                            per_question[idx]["ragas_scores"] = tr.get("ragas_scores")
                    for k, v in ragas_metrics.items():
                        logger.info("  RAGAS %s: %.4f", k, v)
                except Exception as exc:
                    logger.error("RAGAS failed: %s", exc, exc_info=True)
                    ragas_metrics = {"error": str(exc)}
            else:
                logger.info("[3/3] RAGAS skipped")

            # ── Save outputs ──
            config_snapshot = {
                "extraction_mode": extraction_mode,
                "embedding_model": settings.embedding_model,
                "reasoning_model": settings.llm_model_reasoning,
                "extraction_model": settings.llm_model_extraction,
                "chunk_size": settings.chunk_size,
                "chunk_overlap": settings.chunk_overlap,
                "retrieval_mode": settings.retrieval_mode,
                "enable_reranker": settings.enable_reranker,
                "reranker_model": settings.reranker_model,
                "reranker_top_k": settings.reranker_top_k,
                "er_similarity_threshold": settings.er_similarity_threshold,
            }

            summary = {
                "study_id": study_id,
                "dataset_id": dataset_id,
                "run_tag": run_tag,
                "timestamp": datetime.now(UTC).isoformat(),
                "config": config_snapshot,
                "builder": {
                    "triplets": len(builder_state.get("triplets", [])) if builder_state else 0,
                    "entities": len(builder_state.get("entities", [])) if builder_state else 0,
                    "tables_parsed": len(builder_state.get("tables", [])) if builder_state else 0,
                    "tables_completed": len(builder_state.get("completed_tables", []))
                    if builder_state
                    else 0,
                    "elapsed_s": round(builder_elapsed, 1) if builder_state else None,
                },
                "query": {
                    "total_questions": len(pairs),
                    "grounded_count": grounded_count,
                    "grounded_rate": grounded_count / len(pairs) if pairs else 0,
                    "avg_gt_coverage": avg_gt,
                    "avg_top_score": avg_score,
                    "avg_chunk_count": avg_chunks,
                    "abstained_count": abstained,
                },
                "per_question": per_question,
            }
            if ragas_metrics is not None:
                summary["ragas"] = ragas_metrics

            # run.json
            (out / "run.json").write_text(
                json.dumps(summary, indent=2, default=str), encoding="utf-8"
            )

            # analysis.md
            (out / "analysis.md").write_text(
                _generate_analysis_md(summary, dataset_id), encoding="utf-8"
            )

            # evaluation_bundle.json
            builder_bundle = {
                "triplets_extracted": summary["builder"]["triplets"],
                "entities_resolved": summary["builder"]["entities"],
                "tables_parsed": summary["builder"]["tables_parsed"],
                "tables_completed": summary["builder"]["tables_completed"],
                "cypher_failed": bool(builder_state.get("cypher_failed", False))
                if builder_state
                else False,
                "failed_mappings": list(builder_state.get("failed_mappings", []))
                if builder_state
                else [],
                "ingestion_errors": list(builder_state.get("ingestion_errors", []))
                if builder_state
                else [],
            }

            pq_bundle = [
                {
                    "query_id": pq.get("query_id", ""),
                    "question": pq.get("question", ""),
                    "query_type": pq.get("query_type", ""),
                    "difficulty": pq.get("difficulty", ""),
                    "expected_answer": pq.get("expected_answer", ""),
                    "expected_sources": pq.get("expected_sources", []),
                    "generated_answer": pq.get("generated_answer", ""),
                    "sources_retrieved": pq.get("sources", []),
                    "contexts_retrieved": list(pq.get("retrieved_contexts", [])),
                    "covered_sources": pq.get("covered_sources", []),
                    "gt_coverage": pq.get("gt_coverage", 0.0),
                    "grounded": pq.get("grounded", False),
                    "gate_decision": pq.get("retrieval_gate_decision", "proceed"),
                    "retrieval_quality_score": pq.get("retrieval_quality_score", 0.0),
                    "chunk_count": pq.get("retrieval_chunk_count", 0),
                    "grader_rejection_count": pq.get("grader_rejection_count", 0),
                    "grader_consistency_valid": pq.get("grader_consistency_valid", True),
                    "context_sufficiency": pq.get("context_sufficiency", ""),
                }
                for pq in per_question
            ]

            with open(dataset_path) as f:
                dataset_raw = json.load(f)

            bundle_path = write_evaluation_bundle(
                output_dir=out,
                study_id=study_id,
                dataset_id=dataset_id,
                dataset_info=dataset_raw,
                config=config_snapshot,
                builder_info=builder_bundle,
                query_summary=summary.get("query", {}),
                per_question=pq_bundle,
                ragas_metrics=ragas_metrics,
            )

            # ── Thesis exports (CSV + plots) ──
            try:
                from src.evaluation.thesis_export import (  # noqa: PLC0415
                    export_run_csv,
                    export_run_plots,
                    export_run_summary_csv,
                )

                thesis_dir = out / "thesis"
                export_run_csv(summary, thesis_dir)
                export_run_summary_csv(summary, thesis_dir)
                plot_paths = export_run_plots(summary, thesis_dir / "plots")
                logger.info(
                    "  Thesis artifacts: 2 CSVs + %d plots in %s",
                    len(plot_paths),
                    thesis_dir,
                )
            except Exception as tex:
                logger.warning("Thesis export failed (non-fatal): %s", tex)

            logger.info("Outputs: run.json | analysis.md | %s | %s", bundle_path.name, log_file)

            result = {
                "study_id": study_id,
                "dataset_id": dataset_id,
                "success": True,
                "grounded_count": grounded_count,
                "grounded_rate": grounded_count / len(pairs) if pairs else 0,
                "avg_gt_coverage": avg_gt,
                "avg_top_score": avg_score,
                "ragas": ragas_metrics,
            }

    except Exception as exc:
        logger.error("Pipeline failed for %s/%s: %s", study_id, dataset_id, exc, exc_info=True)
        result = {
            "study_id": study_id,
            "dataset_id": dataset_id,
            "success": False,
            "error": str(exc),
        }
    finally:
        root_logger.removeHandler(console)
        root_logger.removeHandler(file_handler)
        file_handler.close()
        for h in original_handlers:
            root_logger.addHandler(h)

    return result


def _run_study(
    study_id: str,
    datasets: list[Path],
    *,
    skip_builder: bool,
    run_ragas: bool,
    ragas_model: str,
    max_samples: int | None,
    run_tag: str,
    smoke: bool,
    output_dir: Path,
) -> list[dict[str, Any]]:
    """Run a study across multiple datasets."""
    from src.evaluation.ablation_runner import ABLATION_DESC  # noqa: PLC0415

    desc = ABLATION_DESC.get(study_id, {})
    print()
    print("=" * 60)
    print(f"  {desc.get('title', study_id)}")
    print(f"  {len(datasets)} dataset(s)")
    print("=" * 60)

    results = []
    for ds_path in datasets:
        print(f"\n  [{ds_path.parent.name}]")
        r = _run_single(
            study_id,
            ds_path,
            skip_builder=skip_builder,
            run_ragas=run_ragas,
            ragas_model=ragas_model,
            max_samples=max_samples,
            run_tag=run_tag,
            smoke=smoke,
            output_dir=output_dir,
        )
        results.append(r)
        status = "\u2705" if r.get("success") else "\u274c"
        print(
            f"  {status} {study_id}/{r.get('dataset_id', '?')}: grounded={r.get('grounded_rate', 0):.0%}"
        )

    return results


# ── CLI ─────────────────────────────────────────────────────────────────────────


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Unified pipeline runner for ablation studies and evaluation",
    )

    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--study", type=str, metavar="AB-XX", help="Run a specific study")
    mode.add_argument("--studies", nargs="+", metavar="AB-XX", help="Run multiple studies")
    mode.add_argument("--all-studies", action="store_true", help="Run AB-00 through AB-20")
    mode.add_argument("--best", action="store_true", help="Run AB-BEST (best known config)")

    ds = parser.add_mutually_exclusive_group()
    ds.add_argument("--dataset", type=Path, default=None, help="Single gold_standard.json")
    ds.add_argument(
        "--datasets", nargs="+", type=Path, metavar="PATH", help="Multiple dataset paths"
    )
    ds.add_argument(
        "--all-datasets", action="store_true", help="Discover all datasets under tests/fixtures/"
    )

    parser.add_argument("--no-builder", action="store_true", help="Skip builder, query only")
    parser.add_argument("--ragas", action="store_true", help="Enable RAGAS evaluation")
    parser.add_argument(
        "--ragas-model", type=str, default="gpt-4.1-mini", help="RAGAS evaluator model"
    )
    parser.add_argument("--lazy", action="store_true", help="Use heuristic extraction")
    parser.add_argument("--max-samples", type=int, default=None, help="Limit QA pairs per dataset")
    parser.add_argument("--run-tag", type=str, default=None, help="Custom run tag")
    parser.add_argument("--smoke", action="store_true", help="Use smoke fixtures")
    parser.add_argument("--auto-neo4j", action="store_true", help="Auto-start Neo4j if not running")
    parser.add_argument(
        "--output-dir", type=Path, default=Path("outputs/ablation"), help="Base output directory"
    )
    args = parser.parse_args()

    # Apply lazy extraction before any imports
    if args.lazy:
        os.environ["USE_LAZY_EXTRACTION"] = "true"

    # Auto-start Neo4j
    if args.auto_neo4j:
        _ensure_neo4j()

    # Determine studies
    from src.evaluation.ablation_runner import ABLATION_MATRIX  # noqa: PLC0415

    if args.best:
        studies = ["AB-BEST"]
    elif args.study:
        if args.study not in ABLATION_MATRIX:
            print(
                f"Error: Unknown study '{args.study}'. Available: {', '.join(sorted(ABLATION_MATRIX))}"
            )
            sys.exit(1)
        studies = [args.study]
    elif args.studies:
        for s in args.studies:
            if s not in ABLATION_MATRIX:
                print(f"Error: Unknown study '{s}'")
                sys.exit(1)
        studies = args.studies
    elif args.all_studies:
        studies = STUDY_IDS
    else:
        studies = ["AB-00"]

    # Determine datasets
    if args.datasets:
        datasets = args.datasets
    elif args.all_datasets:
        datasets = _discover_datasets()
    elif args.dataset:
        if not args.dataset.exists():
            print(f"Error: Dataset not found: {args.dataset}")
            for d in _discover_datasets():
                print(f"  Available: {d}")
            sys.exit(1)
        datasets = [args.dataset]
    else:
        datasets = [FIXTURE_DIR / "01_basics_ecommerce" / "gold_standard.json"]

    # Validate datasets exist
    for d in datasets:
        if not d.exists():
            print(f"Error: Dataset not found: {d}")
            sys.exit(1)

    # Build run tag
    timestamp_str = datetime.now().strftime("%Y%m%d_%H%M%S")
    run_tag = args.run_tag or f"run-{timestamp_str}"

    # Run
    from src.config.llm_factory import reconfigure_from_env  # noqa: PLC0415
    from src.config.logging import setup_notebook_logging  # noqa: PLC0415

    reconfigure_from_env()
    setup_notebook_logging()

    all_results: list[dict[str, Any]] = []
    total_start = _time.perf_counter()

    for study_id in studies:
        results = _run_study(
            study_id,
            datasets,
            skip_builder=args.no_builder,
            run_ragas=args.ragas,
            ragas_model=args.ragas_model,
            max_samples=args.max_samples,
            run_tag=run_tag,
            smoke=args.smoke,
            output_dir=args.output_dir,
        )
        all_results.extend(results)

    total_elapsed = _time.perf_counter() - total_start
    successful = sum(1 for r in all_results if r.get("success"))

    # ── Cross-study thesis exports (if all_scores_full.json exists) ──
    all_scores_path = args.output_dir / "all_scores_full.json"
    if all_scores_path.exists() and len(studies) > 1:
        try:
            from src.evaluation.ablation_runner import ABLATION_DESC  # noqa: PLC0415
            from src.evaluation.thesis_export import generate_all_thesis_artifacts  # noqa: PLC0415

            thesis_dir = args.output_dir / "thesis"
            generate_all_thesis_artifacts(all_scores_path, thesis_dir, ablation_desc=ABLATION_DESC)
        except Exception as tex:
            print(f"  ⚠ Cross-study thesis export failed (non-fatal): {tex}")

    print()
    print("=" * 60)
    print(f"  COMPLETE: {successful}/{len(all_results)} runs successful")
    print(f"  Elapsed: {total_elapsed:.1f}s ({total_elapsed / 60:.1f}m)")
    print("=" * 60)


if __name__ == "__main__":
    main()
