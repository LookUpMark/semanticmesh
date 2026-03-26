 #!/usr/bin/env python
"""Unified runner for AB-00 ablation study.

Replaces the three separate scripts (run_ab00_debug.py, run_ab00_lazy.py,
run_ab00_logged.py) with a single CLI-driven entry point.

Usage:
    python scripts/run_ab00.py                         # LLM extraction, full pipeline
    python scripts/run_ab00.py --lazy                  # Heuristic extraction (no LLM)
    python scripts/run_ab00.py --max-samples 5         # Quick test with 5 questions
    python scripts/run_ab00.py --no-builder            # Query-only (reuse existing graph)
    python scripts/run_ab00.py --ragas                 # Enable RAGAS evaluation
    python scripts/run_ab00.py --run-tag my-run-v1     # Custom tag for trace files
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

    # Setup file logging
    log_dir = Path("notebooks/ablation/ablation_results/logs")
    log_dir.mkdir(parents=True, exist_ok=True)
    timestamp_str = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_file = log_dir / f"ab00_run_{timestamp_str}.log"

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler(sys.stdout),
        ],
    )
    run_logger = logging.getLogger("ab00_runner")

    # Now import src modules (after env vars are set)
    from src.config.settings import get_settings
    from src.generation.query_graph import run_query
    from src.graph.neo4j_client import Neo4jClient, setup_schema

    settings = get_settings()
    run_tag = args.run_tag or f"run-{timestamp_str}"
    extraction_mode = "heuristic (lazy)" if args.lazy else f"LLM ({settings.llm_model_extraction})"

    # Verify dataset exists
    if not args.dataset.exists():
        run_logger.error("Dataset not found: %s", args.dataset)
        for d in Path("tests/fixtures").glob("*/gold_standard.json"):
            run_logger.info("  Available: %s", d)
        sys.exit(1)

    # Print configuration
    run_logger.info("=" * 70)
    run_logger.info("%s ABLATION STUDY", args.study_id)
    run_logger.info("=" * 70)
    run_logger.info("Extraction:     %s", extraction_mode)
    run_logger.info("Reasoning:      %s", settings.llm_model_reasoning)
    run_logger.info("Dataset:        %s", args.dataset)
    run_logger.info("Max samples:    %s", args.max_samples or "All")
    run_logger.info("Builder:        %s", "SKIP" if args.no_builder else "ENABLED")
    run_logger.info("RAGAS:          %s", "ENABLED" if args.ragas else "DISABLED")
    run_logger.info("Debug trace:    ENABLED")
    run_logger.info("Run tag:        %s", run_tag)
    run_logger.info("Log file:       %s", log_file)
    run_logger.info("")

    # Load gold standard dataset
    with open(args.dataset) as f:
        dataset = json.load(f)
    pairs = dataset.get("pairs", dataset) if isinstance(dataset, dict) else dataset
    if args.max_samples:
        pairs = pairs[: args.max_samples]
    run_logger.info("Loaded %d QA pairs from dataset.", len(pairs))

    # ── STAGE 1: Builder Graph ──
    builder_state = None
    builder_trace_id = ""
    if not args.no_builder:
        run_logger.info("")
        run_logger.info("=" * 50)
        run_logger.info("STAGE 1: Builder Graph")
        run_logger.info("=" * 50)

        from src.graph.builder_graph import run_builder

        # Resolve fixture paths for 01_basics_ecommerce
        fixture_dir = args.dataset.parent
        doc_paths = [
            str(fixture_dir / "business_glossary.txt"),
            str(fixture_dir / "data_dictionary.txt"),
        ]
        ddl_paths = [str(fixture_dir / "schema.sql")]

        # Verify all fixture files exist
        for p in doc_paths + ddl_paths:
            if not Path(p).exists():
                run_logger.error("Fixture file not found: %s", p)
                sys.exit(1)

        builder_state = run_builder(
            raw_documents=doc_paths,
            ddl_paths=ddl_paths,
            production=False,
            clear_graph=True,
            trace_enabled=True,
            study_id="AB-00",
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
    run_logger.info("STAGE 2: Query Evaluation (%d questions)", len(pairs))
    run_logger.info("=" * 50)

    results = []
    grounded_count = 0
    for i, pair in enumerate(pairs):
        question = pair["question"]
        expected_answer = pair.get("expected_answer", "")
        expected_sources = pair.get("expected_sources", [])

        run_logger.info("")
        run_logger.info("[Q%03d] %s", i + 1, question)

        result = run_query(
            user_query=question,
            trace_enabled=True,
            query_index=i,
            builder_trace_id=builder_trace_id,
            study_id="AB-00",
        )

        answer = result.get("final_answer", "")
        sources = result.get("sources", [])
        gate = result.get("retrieval_gate_decision", "proceed")
        top_score = result.get("retrieval_quality_score", 0.0)
        chunk_count = result.get("retrieval_chunk_count", 0)
        grounded = result.get("semantic_verification_passed", True)
        overlap = result.get("semantic_verification_overlap", 0.0)

        if grounded and gate != "abstain_early":
            grounded_count += 1
            status = "GROUNDED"
        else:
            status = "ABSTAINED" if gate == "abstain_early" else "UNGROUNDED"

        # Check ground truth source coverage
        covered = [s for s in expected_sources if any(s.lower() in src.lower() for src in sources)]
        gt_coverage = len(covered) / len(expected_sources) if expected_sources else 1.0

        run_logger.info(
            "  %s | score=%.4f chunks=%d overlap=%.2f gt_coverage=%.0f%% (%d/%d)",
            status,
            top_score,
            chunk_count,
            overlap,
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
            "query_id": pair.get("query_id", f"Q{i+1:03d}"),
            "question": question,
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
            "overlap": overlap,
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

    # Save results JSON
    results_dir = Path("notebooks/ablation/ablation_results/runs")
    results_dir.mkdir(parents=True, exist_ok=True)
    results_file = results_dir / f"{args.study_id}.{run_tag}.json"
    summary = {
        "study_id": args.study_id,
        "run_tag": run_tag,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "config": {
            "extraction_mode": extraction_mode,
            "reasoning_model": settings.llm_model_reasoning,
            "extraction_model": settings.llm_model_extraction,
            "chunk_size": settings.chunk_size,
            "chunk_overlap": settings.chunk_overlap,
            "retrieval_mode": settings.retrieval_mode,
            "enable_reranker": settings.enable_reranker,
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
    with open(results_file, "w") as f:
        json.dump(summary, f, indent=2, default=str)

    run_logger.info("")
    run_logger.info("Results saved to: %s", results_file)
    run_logger.info("Log saved to:     %s", log_file)
    run_logger.info("Trace dir:        %s", settings.trace_output_dir)


if __name__ == "__main__":
    main()
