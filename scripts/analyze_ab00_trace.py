#!/usr/bin/env python
"""Analyze AB-00 debug trace files to identify pipeline bottlenecks.

This script loads builder and query traces from an AB-00 run and generates
detailed analysis including:
- Per-question coverage analysis
- Retrieval quality breakdown
- Entity mapping issues
- Answer divergence points
- Bottleneck identification

Usage:
    python scripts/analyze_ab00_trace.py <trace_directory>

Example:
    python scripts/analyze_ab00_trace.py notebooks/ablation/ablation_results/traces/debug/AB-00/
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


def load_builder_trace(trace_dir: Path) -> dict[str, Any] | None:
    """Load builder trace from directory."""
    trace_files = list(trace_dir.glob("builder_trace_*.json"))
    if not trace_files:
        print(f"⚠️  No builder trace found in {trace_dir}")
        return None

    trace_file = trace_files[0]
    print(f"📖 Loading builder trace from {trace_file.name}")

    with open(trace_file) as f:
        return json.load(f)


def load_query_traces(trace_dir: Path, study_id: str = "AB-00") -> list[dict[str, Any]]:
    """Load query traces from directory."""
    trace_file = trace_dir / f"query_traces_{study_id}.jsonl"
    if not trace_file.exists():
        print(f"⚠️  No query trace found at {trace_file}")
        return []

    print(f"📖 Loading query traces from {trace_file.name}")

    traces = []
    with open(trace_file) as f:
        for line in f:
            if line.strip():
                traces.append(json.loads(line))

    print(f"   Loaded {len(traces)} query traces")
    return traces


def load_ground_truth(dataset_path: Path) -> dict[str, Any] | None:
    """Load ground truth dataset."""
    if not dataset_path.exists():
        print(f"⚠️  Ground truth file not found: {dataset_path}")
        return None

    print(f"📖 Loading ground truth from {dataset_path}")

    with open(dataset_path) as f:
        return json.load(f)


def analyze_builder_trace(builder_trace: dict[str, Any]) -> dict[str, Any]:
    """Analyze builder trace and return summary."""
    print("\n🔍 Builder Trace Analysis")
    print("=" * 60)

    summary = {
        "chunks_analyzed": 0,
        "triplets_extracted": 0,
        "entities_resolved": 0,
        "tables_parsed": 0,
        "tables_completed": 0,
        "cypher_queries": 0,
        "cypher_failures": 0,
        "healing_attempts": 0,
    }

    # Chunking analysis
    chunks = builder_trace.get("chunks", [])
    summary["chunks_analyzed"] = len(chunks)
    chunk_summary = builder_trace.get("chunking_summary", {})
    print(f"  📦 Chunks: {len(chunks)}")
    print(f"     - Total tokens: {chunk_summary.get('total_tokens', 0):,}")
    print(f"     - Avg tokens per chunk: {chunk_summary.get('avg_tokens', 0):.1f}")

    # Extraction analysis
    triplets = builder_trace.get("triplets", [])
    summary["triplets_extracted"] = len(triplets)
    extraction_summary = builder_trace.get("extraction_summary", {})
    print(f"  🔗 Triplets extracted: {len(triplets)}")
    print(f"     - Avg confidence: {extraction_summary.get('avg_confidence', 0):.3f}")
    print(f"     - Extraction errors: {extraction_summary.get('extraction_errors', 0)}")

    # Entity resolution analysis
    entities = builder_trace.get("entities_post_resolution", [])
    summary["entities_resolved"] = len(entities)
    resolution_summary = builder_trace.get("resolution_summary", {})
    print(f"  🏷️  Entities resolved: {len(entities)}")
    print(f"     - Pre-resolution: {resolution_summary.get('entities_pre', 0)}")
    print(f"     - Reduction rate: {resolution_summary.get('reduction_rate', 0):.1%}")

    # Schema processing
    tables = builder_trace.get("tables_parsed", [])
    summary["tables_parsed"] = len(tables)
    summary["tables_completed"] = builder_trace.get("neo4j_summary", {}).get("completed_tables", 0)
    schema_summary = builder_trace.get("schema_summary", {})
    print(f"  📋 Tables parsed: {len(tables)}")
    print(f"     - Tables enriched: {schema_summary.get('tables_enriched', 0)}")
    print(f"     - Total columns: {schema_summary.get('total_columns', 0)}")

    # Mapping analysis
    mappings = builder_trace.get("table_mappings", [])
    mapping_summary = builder_trace.get("mapping_summary", {})
    print(f"  🔗 Table mappings: {len(mappings)}")
    if mapping_summary:
        print(f"     - Avg confidence: {mapping_summary.get('avg_confidence', 0):.3f}")
        print(f"     - Low confidence (<0.7): {mapping_summary.get('low_confidence_count', 0)}")

    # Cypher and graph analysis
    cypher_queries = builder_trace.get("cypher_queries", [])
    summary["cypher_queries"] = len(cypher_queries)
    for cq in cypher_queries:
        if not cq.get("success", True):
            summary["cypher_failures"] += 1
        summary["healing_attempts"] += cq.get("healing_attempts", 0)

    neo4j_summary = builder_trace.get("neo4j_summary", {})
    print(f"  🗄️  Neo4j operations:")
    print(f"     - Queries executed: {len(cypher_queries)}")
    print(f"     - Successful: {summary['cypher_queries'] - summary['cypher_failures']}")
    print(f"     - Failures: {summary['cypher_failures']}")
    print(f"     - Healing attempts: {summary['healing_attempts']}")
    print(f"     - Total nodes: {neo4j_summary.get('total_nodes', 0)}")
    print(f"     - Total relationships: {neo4j_summary.get('total_relationships', 0)}")

    return summary


def analyze_query_traces(
    query_traces: list[dict[str, Any]],
    ground_truth: dict[str, Any] | None,
) -> dict[str, Any]:
    """Analyze query traces and return summary."""
    print("\n🔍 Query Trace Analysis")
    print("=" * 60)

    if not query_traces:
        return {}

    summary = {
        "total_queries": len(query_traces),
        "grounded_count": 0,
        "abstained_count": 0,
        "avg_verification_score": 0.0,
        "avg_retrieval_count": 0.0,
        "coverage_issues": [],
        "low_quality_retrievals": [],
    }

    gt_pairs = ground_truth.get("pairs", []) if ground_truth else []

    for i, trace in enumerate(query_traces):
        question = trace.get("question", "")
        grounded = trace.get("grounded", False)
        verification_score = trace.get("verification_score", 0.0)
        sources = trace.get("sources", [])

        if grounded:
            summary["grounded_count"] += 1
        else:
            summary["abstained_count"] += 1

        summary["avg_verification_score"] += verification_score

        # Analyze retrieval
        retrieval_summary = trace.get("retrieval_summary", {})
        fused_count = retrieval_summary.get("fused_count", 0)
        summary["avg_retrieval_count"] += fused_count

        # Coverage analysis if ground truth available
        if i < len(gt_pairs):
            gt_pair = gt_pairs[i]
            expected_sources = gt_pair.get("expected_sources", [])

            # Check which expected sources are in retrieved results
            retrieved_nodes = sources
            covered = [es for es in expected_sources if any(es in node for node in retrieved_nodes)]
            missing = [es for es in expected_sources if not any(es in node for node in retrieved_nodes)]

            coverage_rate = len(covered) / len(expected_sources) if expected_sources else 1.0

            if coverage_rate < 0.5:
                summary["coverage_issues"].append({
                    "index": i,
                    "question": question[:60] + "..." if len(question) > 60 else question,
                    "expected_sources": expected_sources,
                    "retrieved_nodes": retrieved_nodes[:5],
                    "coverage_rate": coverage_rate,
                })

            if fused_count == 0 and expected_sources:
                summary["low_quality_retrievals"].append({
                    "index": i,
                    "question": question[:60] + "..." if len(question) > 60 else question,
                })

    # Calculate averages
    if query_traces:
        summary["avg_verification_score"] /= len(query_traces)
        summary["avg_retrieval_count"] /= len(query_traces)

    # Print summary
    print(f"  📊 Total queries: {len(query_traces)}")
    print(f"  ✅ Grounded: {summary['grounded_count']} ({summary['grounded_count'] / len(query_traces):.1%})")
    print(f"  ⚠️  Not grounded: {summary['abstained_count']} ({summary['abstained_count'] / len(query_traces):.1%})")
    print(f"  📈 Avg verification score: {summary['avg_verification_score']:.3f}")
    print(f"  📦 Avg retrieval count: {summary['avg_retrieval_count']:.1f}")

    if summary["coverage_issues"]:
        print(f"\n  ⚠️  Coverage Issues ({len(summary['coverage_issues'])} queries):")
        for issue in summary["coverage_issues"][:5]:  # Show first 5
            print(f"     Q{issue['index']}: {issue['question']}")
            print(f"        Expected: {issue['expected_sources']}")
            print(f"        Coverage: {issue['coverage_rate']:.1%}")

    if summary["low_quality_retrievals"]:
        print(f"\n  ❌ Zero Retrievals ({len(summary['low_quality_retrievals'])} queries):")
        for issue in summary["low_quality_retrievals"][:5]:
            print(f"     Q{issue['index']}: {issue['question']}")

    return summary


def identify_bottlenecks(
    builder_summary: dict[str, Any],
    query_summary: dict[str, Any],
) -> list[dict[str, Any]]:
    """Identify potential bottlenecks in the pipeline."""
    print("\n🔍 Bottleneck Identification")
    print("=" * 60)

    bottlenecks = []

    # Check extraction
    if builder_summary.get("extraction_errors", 0) > 0:
        bottlenecks.append({
            "stage": "extraction",
            "severity": "medium",
            "issue": f"{builder_summary['extraction_errors']} chunks had extraction errors",
            "recommendation": "Review chunk preprocessing or LLM extraction prompts",
        })

    # Check entity resolution reduction rate
    reduction_rate = builder_summary.get("resolution_summary", {}).get("reduction_rate", 0)
    if reduction_rate > 0.8:
        bottlenecks.append({
            "stage": "entity_resolution",
            "severity": "high",
            "issue": f"Very aggressive merging: {reduction_rate:.1%} reduction rate",
            "recommendation": "Consider lowering er_similarity_threshold to preserve more entities",
        })

    # Check mapping confidence
    low_conf = builder_summary.get("mapping_summary", {}).get("low_confidence_count", 0)
    if low_conf > 0:
        bottlenecks.append({
            "stage": "mapping",
            "severity": "medium",
            "issue": f"{low_conf} tables mapped with low confidence (<0.7)",
            "recommendation": "Review business glossary or enable schema_enrichment",
        })

    # Check Cypher failures
    if builder_summary.get("cypher_failures", 0) > 0:
        bottlenecks.append({
            "stage": "cypher_generation",
            "severity": "high",
            "issue": f"{builder_summary['cypher_failures']} Cypher queries failed",
            "recommendation": "Review Cypher generation prompts or enable cypher_healing",
        })

    # Check query grounding
    if query_summary:
        grounded_rate = query_summary["grounded_count"] / query_summary["total_queries"]
        if grounded_rate < 0.8:
            bottlenecks.append({
                "stage": "answer_generation",
                "severity": "high",
                "issue": f"Low grounding rate: {grounded_rate:.1%}",
                "recommendation": "Review context selection or answer generation prompts",
            })

        # Check coverage issues
        if len(query_summary.get("coverage_issues", [])) > 0:
            bottlenecks.append({
                "stage": "retrieval",
                "severity": "high",
                "issue": f"{len(query_summary['coverage_issues'])} queries have <50% source coverage",
                "recommendation": "Increase retrieval_top_k or improve entity mapping",
            })

    # Print bottlenecks
    if bottlenecks:
        print(f"\n  🔴 Found {len(bottlenecks)} potential bottlenecks:\n")
        for i, b in enumerate(bottlenecks, 1):
            print(f"  {i}. {b['stage'].replace('_', ' ').title()} ({b['severity'].upper()})")
            print(f"     Issue: {b['issue']}")
            print(f"     Recommendation: {b['recommendation']}")
            print()
    else:
        print("  ✅ No major bottlenecks identified!")

    return bottlenecks


def main() -> None:
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Analyze AB-00 debug trace files to identify pipeline bottlenecks"
    )
    parser.add_argument(
        "trace_dir",
        type=Path,
        help="Directory containing trace files (builder_trace_*.json, query_traces_*.jsonl)",
    )
    parser.add_argument(
        "--dataset",
        type=Path,
        default=None,
        help="Path to ground truth JSON file for coverage analysis",
    )
    parser.add_argument(
        "--study-id",
        type=str,
        default="AB-00",
        help="Study ID for trace file naming (default: AB-00)",
    )

    args = parser.parse_args()

    trace_dir = args.trace_dir
    if not trace_dir.exists():
        print(f"❌ Error: Trace directory does not exist: {trace_dir}")
        return

    print("=" * 60)
    print("🔬 AB-00 Trace Analysis")
    print("=" * 60)
    print(f"📁 Trace directory: {trace_dir}")

    # Load traces
    builder_trace = load_builder_trace(trace_dir)
    query_traces = load_query_traces(trace_dir, args.study_id)

    # Load ground truth (if provided or try default)
    gt_path = args.dataset
    if not gt_path:
        # Try to find ground truth in default locations
        for candidate in [
            trace_dir / "../../../../../tests/fixtures/01_basics_ecommerce/gold_standard.json",
            Path("tests/fixtures/01_basics_ecommerce/gold_standard.json"),
            Path("tests/fixtures/gold_standard.json"),
        ]:
            if candidate.exists():
                gt_path = candidate
                break

    ground_truth = None
    if gt_path:
        ground_truth = load_ground_truth(gt_path)

    # Analyze
    builder_summary = analyze_builder_trace(builder_trace) if builder_trace else {}
    query_summary = analyze_query_traces(query_traces, ground_truth) if query_traces else {}

    # Identify bottlenecks
    bottlenecks = identify_bottlenecks(builder_summary, query_summary)

    # Save summary
    summary_path = trace_dir / "analysis_summary.json"
    summary_data = {
        "builder_summary": builder_summary,
        "query_summary": query_summary,
        "bottlenecks": bottlenecks,
    }
    with open(summary_path, "w") as f:
        json.dump(summary_data, f, indent=2)
    print(f"\n💾 Analysis summary saved to {summary_path}")


if __name__ == "__main__":
    main()
