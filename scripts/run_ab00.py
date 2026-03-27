 #!/usr/bin/env python
"""Unified runner for ablation studies.

Supports multiple datasets and writes structured output:
  notebooks/ablation/ablation_results/{study_id}/{dataset_id}/
    run.json      — full results
    run.log       — full log
    analysis.md   — auto-generated deep-dive analysis

Usage:
    python scripts/run_ab00.py                         # LLM extraction, full pipeline, 01_basics_ecommerce
    python scripts/run_ab00.py --lazy                  # Heuristic extraction
    python scripts/run_ab00.py --max-samples 5         # Quick test
    python scripts/run_ab00.py --no-builder            # Query-only (reuse existing graph)
    python scripts/run_ab00.py --ragas                 # Enable RAGAS evaluation
    python scripts/run_ab00.py --dataset tests/fixtures/02_intermediate_finance/gold_standard.json
    python scripts/run_ab00.py --study-id AB-01        # Custom study ID
"""

from __future__ import annotations

import argparse
import json
import logging
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from dotenv import load_dotenv  # noqa: E402  # type: ignore[import]

load_dotenv(Path(__file__).parent.parent / ".env")


# ── Dataset helpers ────────────────────────────────────────────────────────────

def _find_doc_files(fixture_dir: Path) -> list[str]:
    """Auto-detect business documentation files (.txt or .md).

    Looks for standard stems first; falls back to any .md/.txt file that
    isn't a schema file (handles datasets like 07 that use complex_scenarios.md).
    """
    # Standard stems in priority order
    known_stems = ("business_glossary", "data_dictionary", "complex_scenarios")
    doc_files: list[str] = []
    found_stems: set[str] = set()

    for stem in known_stems:
        for ext in (".txt", ".md"):
            candidate = fixture_dir / f"{stem}{ext}"
            if candidate.exists():
                doc_files.append(str(candidate))
                found_stems.add(stem)
                break  # take first match per stem

    # Fallback: if we found nothing, grab all .md/.txt files (except README/schema)
    if not doc_files:
        skip = {"readme", "dataset_summary", "schema"}
        for f in sorted(fixture_dir.glob("*")):
            if f.suffix.lower() in (".txt", ".md") and f.stem.lower() not in skip:
                doc_files.append(str(f))

    return doc_files


def _load_pairs(dataset_path: Path) -> tuple[str, list[dict]]:
    """Load QA pairs from a gold standard JSON, handling all dataset schemas.

    Returns (dataset_id, normalized_pairs).
    """
    with open(dataset_path) as f:
        dataset = json.load(f)

    # Resolve dataset_id from multiple possible locations
    dataset_id: str = (
        dataset.get("dataset_id")
        or (dataset.get("dataset", {}).get("id") if isinstance(dataset.get("dataset"), dict) else None)
        or dataset_path.parent.name
    )

    # Try all known container keys for QA pairs
    pairs_raw = (
        dataset.get("pairs")
        or dataset.get("qa_pairs")
        or dataset.get("questions")
        or (dataset if isinstance(dataset, list) else None)
        or []
    )

    # Normalize each pair to canonical field names
    normalized: list[dict] = []
    for i, p in enumerate(pairs_raw):
        norm = dict(p)
        # query_id: prefer string, fall back to zero-padded index
        if "query_id" not in norm:
            raw_id = p.get("id", f"Q{i+1:03d}")
            norm["query_id"] = str(raw_id) if not isinstance(raw_id, str) else raw_id
        # expected_answer
        if "expected_answer" not in norm:
            norm["expected_answer"] = p.get("answer") or p.get("ground_truth") or ""
        # expected_sources (optional in some datasets)
        if "expected_sources" not in norm:
            norm["expected_sources"] = p.get("tables_involved") or p.get("relevant_tables") or []
        normalized.append(norm)

    return dataset_id, normalized


# ── Analysis Markdown Generator ────────────────────────────────────────────────

def _generate_analysis_md(summary: dict, dataset_id: str) -> str:
    """Generate a detailed analysis markdown from a run summary dict."""
    ts = summary.get("timestamp", "")[:19].replace("T", " ")
    cfg = summary.get("config", {})
    bld = summary.get("builder", {})
    qry = summary.get("query", {})
    ragas = summary.get("ragas", {})
    pq = summary.get("per_question", [])

    lines: list[str] = []

    # Header
    lines += [
        f"# {summary.get('study_id', 'AB-00')} \u2014 {dataset_id} \u2014 Run Analysis",
        "",
        f"**Timestamp:** {ts}  ",
        f"**Run tag:** `{summary.get('run_tag', '')}`",
        "",
    ]

    # Configuration
    lines += [
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

    # Builder
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

    # Query summary
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
        f"| Avg GT Coverage | {qry.get('avg_gt_coverage', 0):.0%} |",
        f"| Avg Top Score | {qry.get('avg_top_score', 0):.4f} |",
        f"| Avg Chunk Count | {qry.get('avg_chunk_count', 0):.1f} |",
        f"| Abstained | {qry.get('abstained_count', 0)} |",
        "",
    ]

    # RAGAS metrics
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

    # Per-question deep dive
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
            f"**GT Coverage:** {gt_cov:.0%} | **Top Score:** {top_score:.4f} | **Gate:** `{gate}`",
            "",
            "**Expected answer:**",
            f"> {expected[:300]}{'\u2026' if len(expected) > 300 else ''}",
            "",
            "**System answer:**",
            f"> {answer[:400]}{'\u2026' if len(answer) > 400 else ''}",
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
                f"**Sources retrieved ({len(sources)}):** " + ", ".join(f"`{s}`" for s in sources[:8]),
                "",
            ]

        if contexts:
            lines += ["**Context previews (first 3):**", ""]
            for j, ctx in enumerate(contexts[:3]):
                preview = ctx[:200].replace("\n", " ")
                lines += [f"{j+1}. _{preview}\u2026_", ""]

        if not grounded_flag:
            anomalies.append(f"- **{qid}**: UNGROUNDED \u2014 answer could not be verified against context")
        if gate == "abstain_early":
            anomalies.append(f"- **{qid}**: ABSTAINED early \u2014 retrieval quality gate rejected all chunks")
        if rscores.get("faithfulness", 1.0) < 0.8:
            anomalies.append(f"- **{qid}**: Low faithfulness ({rscores['faithfulness']:.2f}) \u2014 answer may hallucinate")
        if rscores.get("context_precision", 1.0) < 0.2:
            anomalies.append(f"- **{qid}**: Very low context precision ({rscores.get('context_precision', 0):.2f}) \u2014 many off-topic chunks retrieved")

        lines += ["---", ""]

    lines += ["## Anomalies & Observations", ""]
    if anomalies:
        lines += anomalies + [""]
    else:
        lines += ["No anomalies detected. All questions grounded with acceptable RAGAS scores.", ""]

    return "\n".join(lines)


def main() -> None:
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Run AB-00 ablation study with full tracing"
    )
    parser.add_argument(
        "--dataset",
        type=Path,
        default=Path("tests/fixtures/01_basics_ecommerce/gold_standard.json"),
        help="Path to gold standard dataset",
    )
    parser.add_argument(
        "--max-samples",
        type=int,
        default=None,
        help="Limit evaluation to N samples",
    )
    parser.add_argument(
        "--lazy",
        action="store_true",
        help="Use heuristic extraction (bypass LLM for extraction)",
    )
    parser.add_argument(
        "--ragas",
        action="store_true",
        help="Enable RAGAS evaluation",
    )
    parser.add_argument(
        "--ragas-model",
        type=str,
        default="gpt-4.1-mini",
        help="Model for RAGAS evaluator (must support max_tokens, not reasoning-only)",
    )
    parser.add_argument(
        "--no-builder",
        action="store_true",
        help="Skip builder, only run query evaluation (requires existing graph)",
    )
    parser.add_argument(
        "--run-tag",
        type=str,
        default=None,
        help="Custom run tag for trace file naming",
    )
    parser.add_argument(
        "--study-id",
        type=str,
        default="AB-00",
        help="Study ID prefix for output files (default: AB-00)",
    )
    args = parser.parse_args()

    # Set lazy extraction BEFORE importing anything from src
    if args.lazy:
        os.environ["USE_LAZY_EXTRACTION"] = "true"

    # Verify dataset exists before doing anything else
    if not args.dataset.exists():
        print(f"ERROR: Dataset not found: {args.dataset}")
        for d in Path("tests/fixtures").glob("*/gold_standard.json"):
            print(f"  Available: {d}")
        sys.exit(1)

    # Load pairs and resolve dataset_id BEFORE setting up logging
    dataset_id, all_pairs = _load_pairs(args.dataset)
    if args.max_samples:
        all_pairs = all_pairs[: args.max_samples]

    # ── Structured output directory (study_id / dataset_id) ──
    timestamp_str = datetime.now().strftime("%Y%m%d_%H%M%S")
    run_tag = args.run_tag or f"run-{timestamp_str}"
    out_dir = Path("notebooks/ablation/ablation_results") / args.study_id / dataset_id
    out_dir.mkdir(parents=True, exist_ok=True)
    log_file = out_dir / "run.log"

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[
            logging.FileHandler(log_file, mode="w"),
            logging.StreamHandler(sys.stdout),
        ],
    )
    run_logger = logging.getLogger("ab00_runner")

    # Now import src modules (after env vars are set)
    from src.config.settings import get_settings
    from src.generation.query_graph import run_query
    from src.graph.neo4j_client import Neo4jClient, setup_schema

    settings = get_settings()
    extraction_mode = "heuristic (lazy)" if args.lazy else f"LLM ({settings.llm_model_extraction})"

    # Print configuration
    run_logger.info("=" * 70)
    run_logger.info("%s ABLATION STUDY \u2014 %s", args.study_id, dataset_id)
    run_logger.info("=" * 70)
    run_logger.info("Extraction:     %s", extraction_mode)
    run_logger.info("Embedding:      %s", settings.embedding_model)
    run_logger.info("Reasoning:      %s", settings.llm_model_reasoning)
    run_logger.info("Reranker:       %s (top_k=%d)", settings.reranker_model if settings.enable_reranker else "OFF", settings.reranker_top_k)
    run_logger.info("Dataset:        %s", args.dataset)
    run_logger.info("Dataset ID:     %s", dataset_id)
    run_logger.info("Samples:        %d", len(all_pairs))
    run_logger.info("Builder:        %s", "SKIP" if args.no_builder else "ENABLED")
    run_logger.info("RAGAS:          %s", "ENABLED" if args.ragas else "DISABLED")
    run_logger.info("Output dir:     %s", out_dir)
    run_logger.info("")

    run_logger.info("Loaded %d QA pairs from dataset.", len(all_pairs))

    # ── STAGE 1: Builder Graph ──
    builder_state = None
    builder_trace_id = ""
    if not args.no_builder:
        run_logger.info("")
        run_logger.info("=" * 50)
        run_logger.info("STAGE 1: Builder Graph")
        run_logger.info("=" * 50)

        from src.graph.builder_graph import run_builder

        fixture_dir = args.dataset.parent
        doc_paths = _find_doc_files(fixture_dir)
        ddl_paths = [str(fixture_dir / "schema.sql")]

        if not doc_paths:
            run_logger.error("No business_glossary or data_dictionary files found in %s", fixture_dir)
            sys.exit(1)
        for p in ddl_paths:
            if not Path(p).exists():
                run_logger.error("DDL file not found: %s", p)
                sys.exit(1)

        run_logger.info("Doc files: %s", doc_paths)
        run_logger.info("DDL files: %s", ddl_paths)

        builder_state = run_builder(
            raw_documents=doc_paths,
            ddl_paths=ddl_paths,
            production=False,
            clear_graph=True,
            trace_enabled=True,
            study_id=args.study_id,
        )

        triplets = builder_state.get("triplets", [])
        entities = builder_state.get("entities", [])
        tables = builder_state.get("tables", [])
        completed = builder_state.get("completed_tables", [])

        run_logger.info("")
        run_logger.info("Builder Results:")
        run_logger.info("  Triplets extracted:  %d", len(triplets))
        run_logger.info("  Entities resolved:   %d", len(entities))
        run_logger.info("  Tables parsed:       %d", len(tables))
        run_logger.info("  Tables completed:    %d", len(completed))
        run_logger.info("  Cypher failed:       %s", builder_state.get("cypher_failed", False))

        trace = builder_state.get("builder_trace")
        if trace:
            builder_trace_id = trace.trace_id

        # Log sample entities for quality check
        if entities:
            run_logger.info("")
            run_logger.info("  Sample entities (first 10):")
            for e in entities[:10]:
                run_logger.info("    - %s: %s", e.name, (e.definition or "")[:80])
    else:
        run_logger.info("Builder SKIPPED (--no-builder). Using existing graph.")
        with Neo4jClient() as client:
            setup_schema(client)
            node_count = client.execute_cypher("MATCH (n) RETURN count(n) as c")[0]["c"]
            run_logger.info("  Existing graph: %d nodes", node_count)

    # ── STAGE 2: Query Evaluation ──
    run_logger.info("")
    run_logger.info("=" * 50)
    run_logger.info("STAGE 2: Query Evaluation (%d questions)", len(all_pairs))
    run_logger.info("=" * 50)

    results: list[dict] = []
    grounded_count = 0
    for i, pair in enumerate(all_pairs):
        question = pair["question"]
        expected_answer = pair.get("expected_answer", "")
        expected_sources = pair.get("expected_sources", [])

        run_logger.info("")
        run_logger.info("[%s] %s", pair.get("query_id", f"Q{i+1:03d}"), question)

        result = run_query(
            user_query=question,
            trace_enabled=True,
            query_index=i,
            builder_trace_id=builder_trace_id,
            study_id=args.study_id,
        )

        answer = result.get("final_answer", "")
        sources = result.get("sources", [])
        gate = result.get("retrieval_gate_decision", "proceed")
        top_score = result.get("retrieval_quality_score", 0.0)
        chunk_count = result.get("retrieval_chunk_count", 0)
        grader_grounded = result.get("grader_grounded", True)
        context_sufficiency = result.get("context_sufficiency", "")
        grounded = grader_grounded

        if grounded and gate != "abstain_early":
            grounded_count += 1
            status = "GROUNDED"
        else:
            status = "ABSTAINED" if gate == "abstain_early" else "UNGROUNDED"

        # Check ground truth source coverage
        covered = [s for s in expected_sources if any(s.lower() in src.lower() for src in sources)]
        gt_coverage = len(covered) / len(expected_sources) if expected_sources else 1.0

        run_logger.info(
            "  %s | score=%.4f chunks=%d gt_coverage=%.0f%% (%d/%d)",
            status,
            top_score,
            chunk_count,
            gt_coverage * 100,
            len(covered),
            len(expected_sources),
        )
        run_logger.info("  Answer: %s", answer[:200])
        if expected_sources:
            missing = [s for s in expected_sources if s not in covered]
            if missing:
                run_logger.info("  Missing sources: %s", missing)

        results.append({
            "query_id": pair.get("query_id", str(pair.get("id", f"Q{i+1:03d}"))),
            "question": question,
            "query_type": pair.get("query_type", ""),
            "difficulty": pair.get("difficulty", ""),
            "answer": answer,
            "sources": sources,
            "contexts": result.get("retrieved_contexts", []),
            "expected_answer": expected_answer,
            "expected_sources": expected_sources,
            "covered_sources": covered,
            "gt_coverage": gt_coverage,
            "grounded": grounded,
            "top_score": top_score,
            "chunk_count": chunk_count,
            "gate_decision": gate,
            "context_sufficiency": context_sufficiency,
        })

    # ── STAGE 3: RAGAS Evaluation (optional) ──
    ragas_metrics = None
    if args.ragas:
        run_logger.info("")
        run_logger.info("=" * 50)
        run_logger.info("STAGE 3: RAGAS Evaluation (%d samples)", len(results))
        run_logger.info("=" * 50)

        from src.evaluation.ragas_runner import _compute_ragas_metrics  # noqa: E402

        ragas_rows = [
            {
                "question": r["question"],
                "answer": r["answer"],
                "contexts": r["contexts"],
                "ground_truth": r["expected_answer"],
                "sources": r["sources"],
            }
            for r in results
        ]
        try:
            ragas_trace: list[dict] = []
            ragas_metrics = _compute_ragas_metrics(
                ragas_rows,
                evaluator_model=args.ragas_model,
                trace_rows=ragas_trace,
            )
            # Merge per-question RAGAS scores into results
            for tr in ragas_trace:
                idx = tr.get("sample_index")
                if idx is not None and idx < len(results):
                    results[idx]["ragas_scores"] = tr.get("ragas_scores")
            run_logger.info("RAGAS Results:")
            for metric_name, metric_val in ragas_metrics.items():
                run_logger.info("  %-25s %.4f", metric_name, metric_val)
        except Exception as exc:
            run_logger.error("RAGAS evaluation failed: %s", exc, exc_info=True)
            ragas_metrics = {"error": str(exc)}

    # ── STAGE 4: Summary ──
    run_logger.info("")
    run_logger.info("=" * 70)
    run_logger.info("RESULTS SUMMARY")
    run_logger.info("=" * 70)
    run_logger.info("  Questions:        %d", len(results))
    run_logger.info("  Grounded:         %d/%d (%.0f%%)", grounded_count, len(results), grounded_count / len(results) * 100 if results else 0)

    avg_gt_coverage = sum(r["gt_coverage"] for r in results) / len(results) if results else 0
    avg_score = sum(r["top_score"] for r in results) / len(results) if results else 0
    avg_chunks = sum(r["chunk_count"] for r in results) / len(results) if results else 0
    abstained = sum(1 for r in results if r["gate_decision"] == "abstain_early")

    run_logger.info("  Avg GT coverage:  %.0f%%", avg_gt_coverage * 100)
    run_logger.info("  Avg top score:    %.4f", avg_score)
    run_logger.info("  Avg chunks:       %.1f", avg_chunks)
    run_logger.info("  Abstained:        %d", abstained)

    if builder_state:
        run_logger.info("")
        run_logger.info("  Builder:")
        run_logger.info("    Triplets:       %d", len(builder_state.get("triplets", [])))
        run_logger.info("    Entities:       %d", len(builder_state.get("entities", [])))
        run_logger.info("    Tables done:    %d/%d", len(builder_state.get("completed_tables", [])), len(builder_state.get("tables", [])))

    # ── Save results JSON ──
    summary = {
        "study_id": args.study_id,
        "dataset_id": dataset_id,
        "run_tag": run_tag,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "config": {
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
        },
        "builder": {
            "triplets": len(builder_state.get("triplets", [])) if builder_state else 0,
            "entities": len(builder_state.get("entities", [])) if builder_state else 0,
            "tables_parsed": len(builder_state.get("tables", [])) if builder_state else 0,
            "tables_completed": len(builder_state.get("completed_tables", [])) if builder_state else 0,
        },
        "query": {
            "total_questions": len(results),
            "grounded_count": grounded_count,
            "grounded_rate": grounded_count / len(results) if results else 0,
            "avg_gt_coverage": avg_gt_coverage,
            "avg_top_score": avg_score,
            "avg_chunk_count": avg_chunks,
            "abstained_count": abstained,
        },
        "per_question": results,
    }
    if ragas_metrics is not None:
        summary["ragas"] = ragas_metrics

    results_file = out_dir / "run.json"
    with open(results_file, "w") as f:
        json.dump(summary, f, indent=2, default=str)

    # Generate analysis.md
    analysis_md = _generate_analysis_md(summary, dataset_id)
    analysis_file = out_dir / "analysis.md"
    analysis_file.write_text(analysis_md, encoding="utf-8")

    # Generate evaluation_bundle.json for AI-as-Judge analysis
    from src.evaluation.bundle_writer import write_evaluation_bundle  # noqa: E402

    # Re-load raw dataset for bundle metadata
    with open(args.dataset) as f_ds:
        dataset_raw = json.load(f_ds)

    builder_bundle_info = {
        "triplets_extracted": len(builder_state.get("triplets", [])) if builder_state else 0,
        "entities_resolved": len(builder_state.get("entities", [])) if builder_state else 0,
        "tables_parsed": len(builder_state.get("tables", [])) if builder_state else 0,
        "tables_completed": len(builder_state.get("completed_tables", [])) if builder_state else 0,
        "cypher_failed": bool(builder_state.get("cypher_failed", False)) if builder_state else False,
        "failed_mappings": list(builder_state.get("failed_mappings", [])) if builder_state else [],
        "ingestion_errors": list(builder_state.get("ingestion_errors", [])) if builder_state else [],
    }

    # Normalize per_question results for the bundle
    pq_for_bundle = []
    for r in results:
        pq_for_bundle.append({
            "query_id": r.get("query_id", ""),
            "question": r.get("question", ""),
            "query_type": r.get("query_type", ""),
            "difficulty": r.get("difficulty", ""),
            "expected_answer": r.get("expected_answer", ""),
            "expected_sources": r.get("expected_sources", []),
            "generated_answer": r.get("answer", ""),
            "sources_retrieved": r.get("sources", []),
            "contexts_retrieved": [c[:500] for c in r.get("contexts", [])],
            "covered_sources": r.get("covered_sources", []),
            "gt_coverage": r.get("gt_coverage", 0.0),
            "grounded": r.get("grounded", False),
            "gate_decision": r.get("gate_decision", "proceed"),
            "retrieval_quality_score": r.get("top_score", 0.0),
            "chunk_count": r.get("chunk_count", 0),
            "grader_rejection_count": 0,
            "grader_consistency_valid": True,
            "context_sufficiency": r.get("context_sufficiency", ""),
        })

    bundle_path = write_evaluation_bundle(
        output_dir=out_dir,
        study_id=args.study_id,
        dataset_id=dataset_id,
        dataset_info=dataset_raw,
        config=summary.get("config", {}),
        builder_info=builder_bundle_info,
        query_summary=summary.get("query", {}),
        per_question=pq_for_bundle,
        ragas_metrics=ragas_metrics,
    )

    run_logger.info("")
    run_logger.info("Results saved to:  %s", results_file)
    run_logger.info("Analysis saved to: %s", analysis_file)
    run_logger.info("Bundle saved to:   %s", bundle_path)
    run_logger.info("Log saved to:      %s", log_file)


if __name__ == "__main__":
    main()
